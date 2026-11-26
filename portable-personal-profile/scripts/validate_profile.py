#!/usr/bin/env python3
"""Validate portable profile structure, provenance, conflicts and obvious leaks."""
import argparse
import datetime
import json
import re
import unicodedata
from pathlib import Path

FILES = ('facts', 'preferences', 'projects', 'open-questions')
SOURCE_ID = re.compile(r'[a-z][a-z0-9._-]*')
SOURCE_REF = re.compile(r'[a-z][a-z0-9._-]*(?:#[A-Za-z0-9._-]+)?')

def has_control(value):
    return any(unicodedata.category(c).startswith('C') or c in '\u2028\u2029' for c in value)

STATES = {'confirmed', 'current', 'inferred', 'unconfirmed', 'expired', 'superseded', 'conflict'}
SECRET = re.compile(r'(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{16,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|(?:token|cookie|password|secret|验证码|设备码)\s*[=:：]\s*["\x27]?[A-Za-z0-9_+/=-]{6,})', re.I)
ABS = re.compile(r'(?:^|[\s"\x27(=])(?:/(?!/)[^\s"\x27<>]+|[A-Za-z]:[\\/]|\\\\|~/)')

def valid_time(value):
    try:
        datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError, TypeError):
        return False

def validate(directory):
    root = Path(directory)
    errors, data = [], {}
    def err(where, message): errors.append(f'{where}: {message}')
    if root.is_symlink(): return ['directory: remove symlink; choose a self-contained directory'], {}
    if not root.is_dir(): return ['directory: choose an existing profile directory'], {}
    for path in root.rglob('*'):
        if '.git' in path.relative_to(root).parts: continue
        if path.is_symlink():
            err(str(path.relative_to(root)), 'remove symlink; profile must be self-contained')
            continue
        if path.is_file():
            try: content = path.read_text(encoding='utf-8')
            except (OSError, UnicodeError):
                err(str(path.relative_to(root)), 'use readable UTF-8 text files'); continue
            # Report location only, never echo secret-bearing contents.
            for n, line in enumerate(content.splitlines(), 1):
                if SECRET.search(line): err(f'{path.name}:{n}', 'possible secret; remove it and rotate if real')
                if ABS.search(line): err(f'{path.name}:{n}', 'absolute/local path; replace with a relative reference')
    def load(name, lines=False):
        path = root / name
        if path.is_symlink(): return [] if lines else {}
        try:
            text = path.read_text(encoding='utf-8')
            obj = [json.loads(line) for line in text.splitlines() if line.strip()] if lines else json.loads(text)
            return obj
        except (OSError, ValueError, UnicodeError):
            err(name, 'missing or invalid JSON/JSONL; repair syntax'); return [] if lines else {}
    manifest = load('manifest.json')
    if not isinstance(manifest, dict): manifest = {}; err('manifest.json', 'must be an object')
    if manifest.get('schema_version') != 1 or manifest.get('visibility') != 'private' or not isinstance(manifest.get('version'), str):
        err('manifest.json', 'require schema_version=1, visibility=private and string version')
    sources = load('sources.json')
    if not isinstance(sources, list): sources = []; err('sources.json', 'must be an array')
    source_ids = set()
    for s in sources:
        if not isinstance(s, dict): err('sources.json', 'source must be an object'); continue
        sid = s.get('id')
        if not isinstance(sid, str) or has_control(sid) or not SOURCE_ID.fullmatch(sid):
            err('sources.json', 'invalid source id: require ^[a-z][a-z0-9._-]*$; no newline/control characters'); continue
        if sid in source_ids:
            err('sources.json', 'source ids must be unique'); continue
        source_ids.add(sid)
        if s.get('type') not in ('document', 'user', 'ai', 'import') or not valid_time(s.get('collected_at')):
            err(sid, 'require source type and ISO collected_at')
        ref = s.get('path')
        if not isinstance(ref, str) or not ref or '\\' in ref or Path(ref).is_absolute() or '..' in Path(ref).parts:
            err(sid, 'source path must be relative within profile')
        elif not (root / ref).is_file(): err(sid, 'source file missing; include a sanitized local excerpt')
    seen = set()
    def provenance(obj, where):
        if obj.get('source_type') not in ('document', 'user', 'ai', 'import'): err(where, 'invalid source_type')
        refs = obj.get('source_refs')
        if not isinstance(refs, list) or not refs:
            err(where, 'source_refs must be a nonempty list'); return
        for ref in refs:
            if not isinstance(ref, str) or has_control(ref) or not SOURCE_REF.fullmatch(ref):
                err(where, 'invalid source ref: require source id with optional #[A-Za-z0-9._-]+; no newline/control characters')
            elif ref.split('#')[0] not in source_ids:
                err(where, 'source_refs must point to registered source ids (optional #section)')
    for name in FILES:
        records = load(name + '.jsonl', True)
        data[name] = records
        for n, r in enumerate(records, 1):
            where = f'{name}:{n}'
            if not isinstance(r, dict): err(where, 'record must be an object'); continue
            rid = r.get('id')
            if not isinstance(rid, str) or not re.fullmatch(r'[a-z][a-z0-9.-]*', rid) or rid in seen:
                err(where, 'id must be stable, globally unique lowercase identifier; consolidate duplicate values as conflict')
            else: seen.add(rid)
            for key in ('category', 'content', 'review_trigger'):
                if not isinstance(r.get(key), str) or not r[key].strip(): err(where, f'require nonempty {key}')
            if not valid_time(r.get('collected_at')): err(where, 'collected_at must be ISO date/time')
            status = r.get('status')
            if not isinstance(status, str) or status not in STATES: err(where, 'invalid status')
            confidence = r.get('confidence')
            if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                err(where, 'confidence must be a number in [0,1]')
            if not isinstance(r.get('sensitive'), bool): err(where, 'sensitive must be explicit boolean')
            provenance(r, where)
            variants = r.get('variants')
            if status == 'conflict':
                if not isinstance(variants, list) or len(variants) < 2: err(where, 'conflict requires at least two sourced variants')
                else:
                    values = []
                    for v in variants:
                        if not isinstance(v, dict): err(where, 'variant must be an object'); continue
                        if not isinstance(v.get('content'), str) or not v['content'].strip(): err(where, 'variant needs content')
                        values.append(str(v.get('content')))
                        provenance(v, where)
                    if len(set(values)) < 2: err(where, 'conflict needs distinct values')
                if r.get('resolution') != 'pending_user': err(where, 'conflict resolution must be pending_user')
            elif variants is not None: err(where, 'variants require status=conflict; do not silently choose a value')
    data['manifest'] = manifest
    data['sources'] = sources
    return errors, data

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    a = p.parse_args()
    errors, data = validate(a.directory)
    for e in errors: print('ERROR ' + e)
    if errors: return 1
    count = sum(r.get('status') == 'conflict' for k in FILES for r in data[k])
    print(f'VALID: {count} explicitly registered conflict(s) pending user decision; not approved for external claims.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
