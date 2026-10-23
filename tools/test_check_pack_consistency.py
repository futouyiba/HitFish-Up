"""Issue #34 regression tests; all data is generated in isolated temporary roots."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('check_pack_consistency.py').resolve()
spec = importlib.util.spec_from_file_location('pack_consistency', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
MARKERS = ('待裁', '未裁', '未决', '未冻结')


class ConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pack = self.root / 'pack'
        self.pack.mkdir()

    def write(self, name, text):
        path = self.pack / name
        path.write_text(text, encoding='utf-8')
        return str(path)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), *map(str, args)],
                              cwd=self.root, capture_output=True, text=True)

    def parse(self, proc, code):
        self.assertEqual(proc.returncode, code, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result['exit_code'], code)
        self.assertEqual(result['status'], 'completed' if code == 0 else 'error')
        self.assertNotIn('SELFTEST', proc.stdout if code == 0 else '')
        self.assertIn('候选发现器', result['boundary'])
        if code == 2:
            self.assertIsNone(result['checks'])
            self.assertTrue(result['error'])
        return result

    def test_each_marker_positive_and_negative(self):
        claim = self.write('claim.md', '**零项待裁**\n')
        for marker in MARKERS:
            with self.subTest(marker=marker):
                reg = self.write('reg.md', '| ADJ-12 | %s |\n' % marker)
                claims, regs, bad = checker.check_c2([claim, reg])
                self.assertEqual(regs, 1)
                self.assertEqual(bad, [('claim.md:1', '零项待裁')])
                self.assertEqual(checker.check_c2([reg])[1:], (1, []))
                self.write('reg.md', '| ADJ-12 | %s，已作废 |\n' % marker)
                self.assertEqual(checker.check_c2([claim, reg])[1:], (0, []))

    def test_zero_claim_is_not_registration(self):
        path = self.write('claim.md', '**十三项已裁，零项待裁**\n')
        claims, regs, bad = checker.check_c2([path])
        self.assertEqual(len(claims), 2)
        self.assertEqual((regs, bad), (0, []))

    def test_qualified_zero_claim_stays_non_candidate(self):
        for marker in MARKERS:
            with self.subTest(marker=marker):
                path = self.write('qualified.md', '零项待裁，另有 ADJ-12 %s。\n' % marker)
                self.assertEqual(checker.check_c2([path]), ([], 1, []))

    def test_quoted_zero_claim_stays_non_candidate(self):
        claim = self.write('claim.md', '影响「零项待裁」的读数。\n')
        for marker in MARKERS:
            with self.subTest(marker=marker):
                reg = self.write('reg.md', '| ADJ-12 | %s |\n' % marker)
                self.assertEqual(checker.check_c2([claim, reg]), ([], 1, []))

    def test_selftest_passes_without_a_caller_repo(self):
        result = checker.selftest()
        self.assertTrue(result)
        self.assertTrue(all(value is True for value in result.values()), result)
        self.assertIn('REAL-DEFECT-must-flag', result)

    def test_selftest_detects_degenerate_checkers(self):
        # Mutants live only in memory; production files are never changed.
        mutants = [
            ('check_c1', [], 'opposite-polarity-must-flag'),
            ('check_c1', [('anything', [])], 'same-polarity-must-pass'),
            ('check_c2', ([], 0, []), 'REAL-DEFECT-must-flag'),
            ('check_c2', ([], 1, [('any', '零项待裁')]), 'zero-claim-must-pass'),
            ('check_c3', ([], []), 'missing-path-must-flag'),
            ('check_c3', ([], [('any', 'missing')]), 'existing-path-must-pass'),
        ]
        for name, value, key in mutants:
            with self.subTest(name=name, key=key), patch.object(checker, name, return_value=value):
                self.assertIs(checker.selftest()[key], False)

    def test_json_clean_success(self):
        self.write('clean.md', '**零项待裁**\n')
        proc = self.run_cli('--pack', self.pack, '--json')
        result = self.parse(proc, 0)
        self.assertEqual(result['checks']['c2']['open_blocks'], 0)
        self.assertEqual(result['checks']['c1']['candidates'], [])
        self.assertEqual(result['checks']['c3']['missing'], [])
        self.assertIn('SELFTEST', proc.stderr)

    def test_json_candidates_keep_success_exit(self):
        self.write('claim.md', '**零项待裁**\n\n`WidgetFoo` 已裁。\n')
        self.write('reg.md', '| ADJ-12 | 待裁 |\n\n`WidgetFoo` 未裁。\n\n见 `docs/missing.md`。\n')
        result = self.parse(self.run_cli('--pack', self.pack, '--json'), 0)
        for check in ('c1', 'c2'):
            self.assertTrue(result['checks'][check]['candidates'])
        self.assertTrue(result['checks']['c3']['missing'])

    def test_json_input_and_argument_failures(self):
        bad_encoding = self.root / 'bad_encoding'
        bad_encoding.mkdir()
        (bad_encoding / 'bad.md').write_bytes(b'\xff')
        cases = [('--pack', self.pack), ('--pack', self.root / 'absent'),
                 ('--pack', bad_encoding), (), ('--pack',),
                 ('--pack', self.pack, '--unknown')]
        for args in cases:
            with self.subTest(args=args):
                self.parse(self.run_cli('--json', *args), 2)

    def test_json_selftest_failure_does_not_scan(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(checker, 'selftest', return_value={'probe': False}), \
                patch.object(checker.os, 'listdir', side_effect=AssertionError('must not scan')), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = checker.main(['--json', '--pack', str(self.pack)])
        self.assertEqual(code, 2)
        result = json.loads(stdout.getvalue())
        self.assertEqual(result['status'], 'error')
        self.assertIsNone(result['checks'])
        self.assertIn('SELFTEST FAILED', stderr.getvalue())

    def test_two_repo_orders_match_success_and_failure(self):
        first, second = self.root / 'repo-a', self.root / 'repo-b'
        for repo in (first, second):
            (repo / 'docs').mkdir(parents=True)
        (first / 'docs' / 'one.md').write_text('one', encoding='utf-8')
        (second / 'docs' / 'two.md').write_text('two', encoding='utf-8')
        self.write('refs.md', '见 `docs/one.md` 与 `docs/two.md`。\n')
        for pack, code in ((self.pack, 0), (self.root / 'missing-pack', 2)):
            for json_mode in (False, True):
                with self.subTest(pack=pack, json=json_mode):
                    args = ['--pack', pack] + (['--json'] if json_mode else [])
                    forward = self.run_cli(*args, '--repo', first, '--repo', second)
                    reverse = self.run_cli(*args, '--repo', second, '--repo', first)
                    self.assertEqual((forward.returncode, forward.stdout, forward.stderr),
                                     (reverse.returncode, reverse.stdout, reverse.stderr))
                    self.assertEqual(forward.returncode, code)
                    if json_mode:
                        result = self.parse(forward, code)
                        if code == 0:
                            self.assertEqual(result['checks']['c3']['paths'], ['docs/one.md', 'docs/two.md'])
                            self.assertEqual(result['checks']['c3']['missing'], [])
        # Removing either root must expose the other root's reference.
        result = self.parse(self.run_cli('--pack', self.pack, '--repo', first, '--json'), 0)
        self.assertEqual(result['checks']['c3']['missing'], [['refs.md', 'docs/two.md']])


if __name__ == '__main__':
    unittest.main()
