#!/usr/bin/env python3
# Copyright 2026 Skill-Bible contributors
# SPDX-License-Identifier: Apache-2.0
"""Read-only keyed CSV comparison. Python standard library only."""
import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys


def load(path, encoding, delimiter):
    with path.open(encoding=encoding, newline='') as stream:
        reader = csv.reader(stream, delimiter=delimiter, strict=True)
        header = next(reader, None)
        if not header or any(not h.strip() for h in header) or len(set(header)) != len(header):
            raise ValueError('Each file needs nonempty, unique column names')
        records = []
        for index, row in enumerate(reader, 1):
            if len(row) != len(header):
                raise ValueError(f'{path.name}: record {index} has {len(row)} fields; expected {len(header)}')
            records.append({'record': index, 'values': dict(zip(header, row))})
        return header, records


def group(records, keys):
    groups, invalid = defaultdict(list), []
    for row in records:
        key = tuple(row['values'][k] for k in keys)
        if any(not part.strip() for part in key):
            invalid.append(row)
        else:
            groups[key].append(row)
    return groups, invalid


def numeric_value(value):
    if len(value) > 200:
        raise ValueError('numeric text exceeds 200 characters')
    try:
        number = Decimal(value)
    except InvalidOperation:
        raise ValueError('not a decimal') from None
    if not number.is_finite():
        raise ValueError('not a finite decimal')
    if abs(number.as_tuple().exponent) > 1000:
        raise ValueError('numeric exponent exceeds supported range')
    return number


def within_tolerance(left, right, tolerance):
    # Integer arithmetic over decimal coefficients avoids Decimal context rounding.
    triples = [number.as_tuple() for number in (left, right, tolerance)]
    exponent = min(t.exponent for t in triples)
    integers = []
    for t in triples:
        coefficient = 0
        for digit in t.digits:
            coefficient = coefficient * 10 + digit
        integers.append((-1 if t.sign else 1) * coefficient * 10 ** (t.exponent - exponent))
    return abs(integers[0] - integers[1]) <= integers[2]


def compare(left, right, keys, columns, numeric):
    lg, li = group(left, keys)
    rg, ri = group(right, keys)
    report = {'matched': [], 'changed': [], 'only_left': [], 'only_right': [],
              'ambiguous': [], 'invalid_key_left': li, 'invalid_key_right': ri, 'invalid_pairs': []}
    for key in sorted(lg.keys() | rg.keys()):
        lrows, rrows = lg.get(key, []), rg.get(key, [])
        if len(lrows) > 1 or len(rrows) > 1:
            report['ambiguous'].append({'key': list(key), 'left': lrows, 'right': rrows})
            continue
        if not lrows:
            report['only_right'].extend(rrows)
            continue
        if not rrows:
            report['only_left'].extend(lrows)
            continue
        lrow, rrow = lrows[0], rrows[0]
        changes, errors = [], []
        for col in columns:
            lv, rv = lrow['values'][col], rrow['values'][col]
            if col in numeric:
                try:
                    equal = within_tolerance(numeric_value(lv), numeric_value(rv), numeric[col])
                except ValueError:
                    errors.append({'column': col, 'left': lv, 'right': rv, 'reason': 'invalid_numeric'})
                    continue
            else:
                equal = lv == rv
            if not equal:
                changes.append({'column': col, 'left': lv, 'right': rv})
        pair = {'key': list(key), 'left_record': lrow['record'], 'right_record': rrow['record']}
        if errors:
            report['invalid_pairs'].append({**pair, 'errors': errors, 'changes': changes})
        elif changes:
            report['changed'].append({**pair, 'changes': changes})
        else:
            report['matched'].append(pair)
    summary = {'left_rows': len(left), 'right_rows': len(right),
               'matched_rows': len(report['matched']), 'changed_rows': len(report['changed']),
               'invalid_pair_rows': len(report['invalid_pairs']), 'ambiguous_keys': len(report['ambiguous'])}
    for side in ('left', 'right'):
        summary[f'only_{side}_rows'] = len(report[f'only_{side}'])
        summary[f'invalid_key_{side}_rows'] = len(report[f'invalid_key_{side}'])
        summary[f'ambiguous_{side}_rows'] = sum(len(x[side]) for x in report['ambiguous'])
        accounted = sum(summary[k] for k in ('matched_rows', 'changed_rows', 'invalid_pair_rows',
                        f'only_{side}_rows', f'invalid_key_{side}_rows', f'ambiguous_{side}_rows'))
        if accounted != summary[f'{side}_rows']:
            raise ValueError('Internal row accounting failure')
    denominator = summary['matched_rows'] + summary['changed_rows']
    summary['match_rate'] = summary['matched_rows'] / denominator if denominator else None
    return report, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path)
    parser.add_argument('--key', action='append', required=True)
    parser.add_argument('--compare', action='append')
    parser.add_argument('--numeric', action='append', default=[])
    parser.add_argument('--delimiter', default=',')
    parser.add_argument('--encoding', default='utf-8-sig')
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        delimiter = '\t' if args.delimiter == 'tab' else args.delimiter
        if len(delimiter) != 1 or delimiter in '\r\n\x00':
            raise ValueError('delimiter must be a single non-newline character')
        if len(args.key) != len(set(args.key)):
            raise ValueError('Duplicate --key arguments')
        lh, left = load(args.left, args.encoding, delimiter)
        rh, right = load(args.right, args.encoding, delimiter)
        if not set(args.key) <= set(lh) & set(rh):
            raise ValueError('Every key column must exist in both files')
        columns = args.compare if args.compare is not None else [h for h in lh if h in rh and h not in args.key]
        if len(columns) != len(set(columns)) or not set(columns) <= (set(lh) & set(rh)) - set(args.key):
            raise ValueError('Comparison columns must be unique, common, and non-key')
        numeric = {}
        for spec in args.numeric:
            col, separator, value = spec.rpartition('=')
            if not separator or col not in columns or col in numeric:
                raise ValueError('Each numeric rule must uniquely name a comparison column: COL=TOL')
            tolerance = numeric_value(value)
            if tolerance < 0:
                raise ValueError('Tolerance cannot be negative')
            numeric[col] = tolerance
        report, summary = compare(left, right, args.key, columns, numeric)
        schema = {'columns_only_left': [h for h in lh if h not in rh],
                  'columns_only_right': [h for h in rh if h not in lh],
                  'uncompared_columns': [h for h in lh if h in rh and h not in args.key and h not in columns]}
        needs_review = bool(report['ambiguous'] or report['invalid_key_left'] or report['invalid_key_right']
                            or report['invalid_pairs'] or not (left or right))
        different = bool(report['changed'] or report['only_left'] or report['only_right']
                         or schema['columns_only_left'] or schema['columns_only_right'])
        status = 'needs_review' if needs_review else ('different' if different else 'same')
        result = {'status': status, 'scope': {'keys': args.key, 'compare': columns,
                  'numeric_absolute_tolerance': {c: str(t) for c, t in numeric.items()},
                  'encoding': args.encoding, 'delimiter': delimiter},
                  'schema': schema, 'summary': summary, 'details': report}
        payload = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        # Keep raw strings in JSON; fenced JSON prevents Markdown/HTML injection in summaries.
        overview = {k: result[k] for k in ('status', 'scope', 'schema', 'summary')}
        safe_overview = json.dumps(overview, ensure_ascii=True, indent=2).replace('`', '\\u0060').replace('<', '\\u003c')
        markdown = ('# CSV 核对摘要\n\n以下结论仅适用于所列字段与口径。'
                    'match_rate 仅以成功比较的唯一键配对为分母。\n\n```json\n' + safe_overview + '\n```\n\n'
                    '完整差异见 report.json；record 为数据记录序号，并非物理行号。\n')
        args.out_dir.mkdir(parents=True, exist_ok=False)
        (args.out_dir / 'report.json').write_text(payload, encoding='utf-8')
        (args.out_dir / 'summary.md').write_text(markdown, encoding='utf-8')
        print(json.dumps({'status': status, 'summary': summary}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, LookupError, csv.Error) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
