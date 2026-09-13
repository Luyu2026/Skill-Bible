#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Append CSV records by exact column name, preserving strings and provenance."""
import argparse
import csv
import json
import os
from pathlib import Path
import sys
import tempfile


class InputError(ValueError):
    pass


def signature(path):
    stat = path.stat()
    return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)


def header(reader, path):
    fields = next(reader, None)
    if not fields or any(not name.strip() for name in fields):
        raise InputError(f'{path.name}: missing or blank column name')
    if len(set(fields)) != len(fields):
        raise InputError(f'{path.name}: duplicate column name')
    return fields


def stack(inputs, output, mode='strict', encoding='utf-8-sig', delimiter=',', source_column='_source_file'):
    if len(inputs) < 2:
        raise InputError('Provide at least two CSV files')
    if len(delimiter) != 1 or delimiter in '\r\n\x00"':
        raise InputError('Delimiter must be one character other than quote, NUL or newline')
    if mode not in ('strict', 'union'):
        raise InputError('Mode must be strict or union')
    if not source_column.strip():
        raise InputError('Source column must not be blank')
    paths = [Path(p).resolve(strict=True) for p in inputs]
    out = Path(output).absolute()
    if os.path.lexists(out):
        raise InputError('Output already exists; choose a new path')
    schemas, fingerprints, columns, identities = [], [], [], set()
    names = [p.name for p in paths]
    if len(set(names)) != len(names):
        raise InputError('Input basenames must be unique for unambiguous source labels')
    for path in paths:
        if not path.is_file():
            raise InputError(f'{path.name}: input is not a regular file')
        stamp = signature(path)
        if stamp[:2] in identities:
            raise InputError('Same input file supplied more than once')
        identities.add(stamp[:2])
        with path.open('r', encoding=encoding, newline='') as stream:
            fields = header(csv.reader(stream, delimiter=delimiter, strict=True), path)
        if source_column in fields:
            raise InputError(f'{path.name}: source column conflicts with input; choose --source-column')
        if schemas and mode == 'strict' and set(fields) != set(schemas[0]):
            raise InputError(f'{path.name}: columns differ; review schemas before using --mode union')
        columns.extend(name for name in fields if name not in columns)
        schemas.append(fields)
        fingerprints.append(stamp)
    # Stage in output's filesystem, then publish by exclusive hard link. Never truncate an existing path.
    temp_path = None
    reports = []
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig', newline='',
                                         dir=out.parent, prefix='.csv-stack-', delete=False) as dest:
            temp_path = Path(dest.name)
            writer = csv.writer(dest, lineterminator='\n')
            writer.writerow(columns + [source_column])
            for path, fields, stamp in zip(paths, schemas, fingerprints):
                if signature(path) != stamp:
                    raise InputError(f'{path.name}: input changed during processing')
                count = blanks = 0
                with path.open('r', encoding=encoding, newline='') as stream:
                    reader = csv.reader(stream, delimiter=delimiter, strict=True)
                    if header(reader, path) != fields:
                        raise InputError(f'{path.name}: header changed during processing')
                    for row in reader:
                        if not row:
                            blanks += 1
                            continue
                        if len(row) != len(fields):
                            raise InputError(f'{path.name}: record ending at line {reader.line_num} has {len(row)} cells; expected {len(fields)}')
                        values = dict(zip(fields, row))
                        writer.writerow([values.get(name, '') for name in columns] + [path.name])
                        count += 1
                if signature(path) != stamp:
                    raise InputError(f'{path.name}: input changed during processing')
                reports.append({'file': path.name, 'rows': count, 'blank_lines_skipped': blanks,
                                'columns': fields, 'missing_columns': [c for c in columns if c not in fields]})
            dest.flush()
            os.fsync(dest.fileno())
        os.link(temp_path, out)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    return {'output': str(out), 'mode': mode, 'columns': columns + [source_column],
            'total_rows': sum(r['rows'] for r in reports), 'files': reports,
            'values': 'text preserved; no type conversion, deduplication or formula escaping'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--output', required=True, help='New CSV path; parent directory must exist')
    parser.add_argument('--mode', choices=['strict', 'union'], default='strict')
    parser.add_argument('--encoding', default='utf-8-sig', help='Shared input encoding; default UTF-8 with optional BOM')
    parser.add_argument('--delimiter', default=',', help='Shared input delimiter; output is always comma-separated')
    parser.add_argument('--source-column', default='_source_file')
    args = parser.parse_args()
    try:
        report = stack(**vars(args))
    except (OSError, ValueError, csv.Error, LookupError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
