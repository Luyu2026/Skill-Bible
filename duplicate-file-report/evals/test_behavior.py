#!/usr/bin/env python3
"""Anonymous filesystem scenarios. SPDX-License-Identifier: Apache-2.0"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / 'scripts/find_duplicates.py'
spec = importlib.util.spec_from_file_location('finder', SCRIPT)
finder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finder)


class Behavior(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.root = self.base / 'input'
        self.root.mkdir()
        self.out = self.base / 'report.json'

    def put(self, name, data=b'same'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def run_cli(self, roots=None, output=None):
        result = subprocess.run([sys.executable, str(SCRIPT),
                                 *map(str, roots or [self.root]), '--output', str(output or self.out)],
                                capture_output=True, text=True)
        return result

    def test_realistic_cases(self):
        cases = json.loads((SKILL / 'evals/cases.json').read_text())['cases']
        for case in cases:
            with self.subTest(case=case['id']):
                scope = self.root / case['id']
                for name, value in case['files'].items():
                    self.put(case['id'] + '/' + name, value.encode())
                before = {p: p.read_bytes() for p in scope.rglob('*') if p.is_file()}
                roots = [scope]
                if case['id'] == 'backup-archives':
                    roots += [scope / 'backup-a', scope]
                report_path = self.base / (case['id'] + '.json')
                result = self.run_cli(roots, report_path)
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(report_path.read_text())
                actual = {frozenset(str(Path(p).relative_to(scope)) for f in g['files'] for p in f['paths'])
                          for g in report['groups']}
                self.assertEqual(actual, {frozenset(g) for g in case['expected_groups']})
                expected_bytes = sum(len(case['files'][g[0]].encode()) * (len(g) - 1)
                                     for g in case['expected_groups'])
                self.assertEqual(report['logical_redundant_bytes'], expected_bytes)
                self.assertEqual(report['regular_paths'], len(case['files']))
                self.assertEqual(before, {p: p.read_bytes() for p in scope.rglob('*') if p.is_file()})

    def test_hardlinks(self):
        a = self.put('original')
        os.link(a, self.root / 'alias')
        self.put('independent-copy')
        report = finder.scan([self.root])
        self.assertEqual(report['independent_files'], 2)
        self.assertEqual(report['logical_redundant_bytes'], 4)
        self.assertEqual(len(report['hardlink_sets']), 1)

    def test_only_hardlinks_are_not_duplicates(self):
        os.link(self.put('original'), self.root / 'alias')
        report = finder.scan([self.root])
        self.assertEqual(report['duplicate_groups'], 0)
        self.assertEqual(report['logical_redundant_bytes'], 0)

    def test_symlinks_and_fifo(self):
        outside = self.base / 'outside'
        outside.mkdir()
        (outside / 'secret').write_bytes(b'same')
        self.put('a')
        (self.root / 'dir-link').symlink_to(outside, target_is_directory=True)
        (self.root / 'file-link').symlink_to(outside / 'secret')
        (self.root / 'broken').symlink_to(outside / 'missing')
        os.mkfifo(self.root / 'pipe')
        report = finder.scan([self.root])
        self.assertEqual(report['regular_paths'], 1)
        self.assertEqual(len(report['skipped']), 4)
        self.assertEqual(report['duplicate_groups'], 0)

    def test_output_protection(self):
        self.out.write_text('keep me')
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(self.out.read_text(), 'keep me')
        bad = self.root / 'new.json'
        self.assertEqual(self.run_cli(output=bad).returncode, 2)
        self.assertFalse(bad.exists())

    def test_missing_root(self):
        self.assertEqual(self.run_cli([self.base / 'missing']).returncode, 2)
        self.assertFalse(self.out.exists())

    def test_empty_and_unique(self):
        self.assertEqual(finder.scan([self.root])['duplicate_groups'], 0)
        self.put('a', b'A')
        self.put('b', b'BC')
        with patch.object(finder, 'digest', side_effect=AssertionError('unique sizes should not hash')):
            self.assertEqual(finder.scan([self.root])['duplicate_groups'], 0)

    def test_read_error_is_partial(self):
        self.put('a')
        self.put('b')
        with patch.object(finder, 'digest', side_effect=PermissionError('anonymous denied fixture')):
            report = finder.scan([self.root])
        self.assertFalse(report['complete'])
        self.assertEqual(len(report['errors']), 2)

    def test_digest_collision_requires_bytes(self):
        self.put('a', b'AAAA')
        self.put('b', b'BBBB')
        with patch.object(finder, 'digest', return_value='simulated-collision'):
            self.assertEqual(finder.scan([self.root])['duplicate_groups'], 0)

    def test_changed_file_excluded(self):
        self.put('a')
        target = self.put('b')
        real_digest = finder.digest
        def change_after_hash(item):
            value = real_digest(item)
            if item['paths'][0] == str(target):
                target.write_bytes(b'edit')
            return value
        with patch.object(finder, 'digest', side_effect=change_after_hash):
            report = finder.scan([self.root])
        self.assertFalse(report['complete'])
        self.assertEqual(report['duplicate_groups'], 0)

    def test_partial_cli_status(self):
        self.put('a')
        self.put('b')
        with patch.object(finder, 'digest', side_effect=PermissionError('denied')):
            with patch.object(sys, 'argv', [str(SCRIPT), str(self.root), '--output', str(self.out)]):
                self.assertEqual(finder.main(), 1)
        self.assertFalse(json.loads(self.out.read_text())['complete'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
