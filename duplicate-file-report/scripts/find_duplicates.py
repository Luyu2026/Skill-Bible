#!/usr/bin/env python3
"""Read-only exact duplicate report. Python 3.9+, standard library only.

SPDX-License-Identifier: Apache-2.0
"""
import argparse
from collections import defaultdict
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

CHUNK = 1024 * 1024


def signature(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


@contextmanager
def checked_open(item):
    path = item['paths'][0]
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
                 | getattr(os, 'O_NONBLOCK', 0))
    with os.fdopen(fd, 'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise OSError('file is no longer regular')
        if signature(os.fstat(stream.fileno())) != item['signature']:
            raise OSError('file changed since enumeration')
        yield stream
        if signature(os.fstat(stream.fileno())) != item['signature']:
            raise OSError('file changed while reading')


def digest(item):
    h = hashlib.sha256()
    with checked_open(item) as stream:
        for block in iter(lambda: stream.read(CHUNK), b''):
            h.update(block)
    return h.hexdigest()


def same_bytes(a, b):
    with checked_open(a) as left, checked_open(b) as right:
        while True:
            x, y = left.read(CHUNK), right.read(CHUNK)
            if x != y:
                return False
            if not x:
                return True


def scan(roots):
    errors, skipped = [], []
    inodes, visited = {}, set()

    def error(path, exc):
        errors.append({'path': str(path), 'reason': str(exc)})

    def visit(path):
        key = str(path)
        if key in visited:
            return
        visited.add(key)
        try:
            s = path.lstat()
            if stat.S_ISLNK(s.st_mode):
                skipped.append({'path': key, 'reason': 'symbolic link'})
            elif stat.S_ISDIR(s.st_mode):
                with os.scandir(path) as entries:
                    children = sorted((Path(e.path) for e in entries), key=str)
                for child in children:
                    visit(child)
            elif stat.S_ISREG(s.st_mode):
                inode = (s.st_dev, s.st_ino) if s.st_ino else ('path', key)
                if inode not in inodes:
                    inodes[inode] = {'paths': [], 'size_bytes': s.st_size,
                                     'link_count': s.st_nlink, 'signature': signature(s)}
                elif signature(s) != inodes[inode]['signature']:
                    raise OSError('hard-linked file changed during enumeration')
                inodes[inode]['paths'].append(key)
            else:
                skipped.append({'path': key, 'reason': 'not a regular file or directory'})
        except OSError as exc:
            error(path, exc)

    for root in roots:
        visit(root)
    by_size = defaultdict(list)
    for item in inodes.values():
        item['paths'].sort()
        by_size[item['size_bytes']].append(item)

    groups = []
    for size, items in sorted(by_size.items()):
        if len(items) < 2:
            continue
        by_hash = defaultdict(list)
        for item in items:
            try:
                by_hash[digest(item)].append(item)
            except OSError as exc:
                error(item['paths'][0], exc)
        for sha, candidates in sorted(by_hash.items()):
            if len(candidates) < 2:
                continue
            # Compare bytes as well: a digest match alone is not the final verdict.
            partitions = []
            for item in candidates:
                try:
                    for partition in partitions:
                        if same_bytes(partition[0], item):
                            partition.append(item)
                            break
                    else:
                        partitions.append([item])
                except OSError as exc:
                    error(item['paths'][0], exc)
            for partition in partitions:
                stable = []
                for item in partition:
                    try:
                        for path in item['paths']:
                            if signature(os.lstat(path)) != item['signature']:
                                raise OSError('file changed before report')
                        stable.append(item)
                    except OSError as exc:
                        error(item['paths'][0], exc)
                if len(stable) > 1:
                    groups.append({'size_bytes': size, 'sha256': sha,
                                   'independent_files': len(stable),
                                   'logical_redundant_bytes': size * (len(stable) - 1),
                                   'files': [{k: v for k, v in x.items() if k != 'signature'}
                                             for x in stable]})
    groups.sort(key=lambda g: (-g['logical_redundant_bytes'], g['files'][0]['paths'][0]))
    return {'schema_version': 1, 'roots': [str(r) for r in roots],
            'complete': not errors, 'regular_paths': sum(len(x['paths']) for x in inodes.values()),
            'independent_files': len(inodes), 'duplicate_groups': len(groups),
            'logical_redundant_bytes': sum(g['logical_redundant_bytes'] for g in groups),
            'groups': groups,
            'hardlink_sets': [{'paths': x['paths'], 'link_count': x['link_count']}
                              for x in inodes.values() if x['link_count'] > 1],
            'skipped': skipped, 'errors': errors,
            'space_note': 'Logical content bytes only; not guaranteed reclaimable disk space. '
                          'Hardlinks, clones, compression, sparse files and snapshots affect storage.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('roots', nargs='+', help='Explicit directories to scan recursively (including hidden files)')
    parser.add_argument('--output', required=True, help='New JSON file outside all scanned roots')
    args = parser.parse_args()
    try:
        roots = []
        for value in args.roots:
            path = Path(value).absolute()
            if path.is_symlink() or not path.is_dir():
                raise ValueError('each root must be an existing non-symlink directory: ' + value)
            roots.append(path.resolve())
        roots = sorted(set(roots), key=str)
        output = Path(args.output).absolute()
        if os.path.lexists(output):
            raise ValueError('output already exists; choose a new path')
        resolved_output = output.resolve()
        if any(resolved_output == r or r in resolved_output.parents for r in roots):
            raise ValueError('output must be outside scanned roots')
        if not output.parent.is_dir():
            raise ValueError('output parent directory does not exist')
        report = scan(roots)
        with output.open('x', encoding='utf-8') as stream:
            json.dump(report, stream, ensure_ascii=True, indent=2)
            stream.write('\n')
        print(json.dumps({'output': str(output), 'complete': report['complete'],
                          'duplicate_groups': report['duplicate_groups'],
                          'logical_redundant_bytes': report['logical_redundant_bytes']}))
        return 0 if report['complete'] else 1
    except (OSError, ValueError, RecursionError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
