# SPDX-License-Identifier: Apache-2.0
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/stack_csv.py'


class StackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def run_files(self, files, args=(), raw=False):
        paths = []
        for name, data in files.items():
            path = self.base / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data if raw else data.encode('utf-8'))
            paths.append(path)
        before = [p.read_bytes() for p in paths]
        output = self.base / 'result.csv'
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, paths), '--output', str(output), *args], capture_output=True, text=True)
        self.assertEqual(before, [p.read_bytes() for p in paths])
        self.assertFalse(list(self.base.glob('.csv-stack-*')))
        return result, output

    def test_realistic_cases(self):
        cases = json.loads((ROOT / 'evals/evals.json').read_text())['evals'][:3]
        for case in cases:
            with self.subTest(case=case['id']):
                result, output = self.run_files(case['inputs'], case['args'])
                if 'expected_error' in case:
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn(case['expected_error'], result.stderr)
                    self.assertFalse(output.exists())
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    with output.open(encoding='utf-8-sig', newline='') as stream:
                        self.assertEqual(list(csv.reader(stream)), case['expected_rows'])
                    report = json.loads(result.stdout)
                    self.assertEqual([x['rows'] for x in report['files']], case['expected_counts'])
                    self.assertEqual(report['total_rows'], len(case['expected_rows']) - 1)
                    if case['id'] == 'store-union':
                        self.assertEqual([f['missing_columns'] for f in report['files']], [['券码'], ['实收']])
                    output.unlink()

    def test_refuses_mismatch(self):
        result, output = self.run_files({'a.csv': 'id,amount\n01,2\n', 'b.csv': 'id,paid\n02,3\n'})
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())

    def test_bad_headers_and_quotes(self):
        for bad in ['', 'id,id\n1,2\n', 'id, \n1,2\n', 'id,v\n1,"open\n']:
            with self.subTest(data=bad):
                result, output = self.run_files({'a.csv': 'id,v\n1,2\n', 'b.csv': bad})
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertFalse(output.exists())

    def test_existing_output(self):
        out = self.base / 'result.csv'
        out.write_bytes(b'keep me')
        result, _ = self.run_files({'a.csv': 'x\n1\n', 'b.csv': 'x\n2\n'})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(out.read_bytes(), b'keep me')

    def test_encoding_and_delimiter(self):
        result, output = self.run_files({'a.csv': '编号;金额\n001;3.00\n'.encode('gb18030'), 'b.csv': '金额;编号\n2.00;002\n'.encode('gb18030')}, ['--encoding', 'gb18030', '--delimiter', ';'], raw=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        with output.open(encoding='utf-8-sig', newline='') as stream:
            self.assertEqual(list(csv.reader(stream))[-1], ['002', '2.00', 'b.csv'])

    def test_invalid_utf8(self):
        result, output = self.run_files({'a.csv': b'x\n1\n', 'b.csv': b'x\n\xff\n'}, raw=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())

    def test_source_collision(self):
        files = {'a.csv': '_source_file,x\na,1\n', 'b.csv': 'x,_source_file\n2,b\n'}
        result, output = self.run_files(files)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())
        result, output = self.run_files(files, ['--source-column', 'input_name'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['columns'], ['_source_file', 'x', 'input_name'])

    def test_duplicate_basename(self):
        result, output = self.run_files({'one/data.csv': 'x\n1\n', 'two/data.csv': 'x\n2\n'})
        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())

    def test_hardlink_duplicate_input(self):
        a, b = self.base / 'a.csv', self.base / 'b.csv'
        a.write_text('x\n1\n')
        os.link(a, b)
        result = subprocess.run([sys.executable, str(SCRIPT), str(a), str(b), '--output', str(self.base / 'out.csv')], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / 'out.csv').exists())

    def test_bom_empty_values_and_formula_text(self):
        result, output = self.run_files({'a.csv': '\ufeffx\n\n""\n=2+2\n', 'b.csv': 'x\n'})
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['total_rows'], 2)
        self.assertEqual(report['files'][0]['blank_lines_skipped'], 1)
        with output.open(encoding='utf-8-sig', newline='') as stream:
            self.assertEqual(list(csv.reader(stream)), [['x', '_source_file'], ['', 'a.csv'], ['=2+2', 'a.csv']])

    def test_output_symlink(self):
        target = self.base / 'protected.txt'
        target.write_text('keep')
        (self.base / 'result.csv').symlink_to(target)
        result, output = self.run_files({'a.csv': 'x\n1\n', 'b.csv': 'x\n2\n'})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(target.read_text(), 'keep')
        self.assertTrue(output.is_symlink())


if __name__ == '__main__':
    unittest.main()
