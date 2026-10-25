"""Exercise the validator against small, isolated publishing mistakes."""

import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check.py'


class PublishingChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        shutil.copy2(SCRIPT, self.root / 'scripts' / 'check.py')
        (self.root / '01' / 'pdf').mkdir(parents=True)
        self.pdf = self.root / '01' / 'pdf' / 'manual.pdf'
        self.pdf.write_bytes(b'%PDF-1.4\nfixture\n%%EOF\n')
        self.page = self.root / '01' / 'manual.html'
        self.url = 'pdf/manual.pdf?v=' + hashlib.sha256(self.pdf.read_bytes()).hexdigest()[:12]
        self.valid = (f'<a href="{self.url}" target="_blank" rel="noopener">Open PDF</a>'
                      f'<iframe src="{self.url}" title="Manual"></iframe>')
        self.page.write_text(self.valid, encoding='utf-8')

    def check(self, *args):
        return subprocess.run([sys.executable, str(self.root / 'scripts' / 'check.py'), *args],
                              capture_output=True, text=True)

    def reject(self, message):
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)

    def test_valid_manual(self):
        self.assertEqual(self.check().returncode, 0)

    def test_deleted_pdf_is_rejected(self):
        self.pdf.unlink()
        self.reject('missing target')

    def test_replaced_pdf_requires_new_versions(self):
        self.pdf.write_bytes(self.pdf.read_bytes() + b'updated')
        self.reject('stale PDF version')
        result = self.check('--update')
        self.assertEqual(result.returncode, 0, result.stderr)
        version = hashlib.sha256(self.pdf.read_bytes()).hexdigest()[:12]
        self.assertEqual(self.page.read_text().count('v=' + version), 2)
        self.assertEqual(self.check().returncode, 0)

    def test_update_is_idempotent(self):
        self.assertEqual(self.check('--update').returncode, 0)
        before = self.page.read_bytes()
        self.assertEqual(self.check('--update').returncode, 0)
        self.assertEqual(self.page.read_bytes(), before)

    def test_missing_pdf_fallback_is_rejected(self):
        self.page.write_text(f'<iframe src="{self.url}"></iframe>')
        self.reject('needs a direct link')

    def test_fallback_to_different_pdf_is_rejected(self):
        other = self.pdf.with_name('other.pdf')
        shutil.copy2(self.pdf, other)
        self.page.write_text(self.valid.replace('href="pdf/manual', 'href="pdf/other'))
        self.reject('needs a direct link')

    def test_fallback_must_keep_original_viewer_open(self):
        self.page.write_text(self.valid.replace('target="_blank"', 'target="_self"'))
        self.reject('must open a new tab')

    def test_fallback_must_isolate_opener(self):
        self.page.write_text(self.valid.replace('rel="noopener"', ''))
        self.reject('with noopener')

    def test_redirect_must_match_visible_link(self):
        self.page.write_text('<meta http-equiv="refresh" content="0; url=https://example.com">'
                             '<a href="https://other.example">Continue</a>')
        self.reject('matching HTTPS fallback')

    def test_redirect_must_use_https(self):
        self.page.write_text('<meta http-equiv="refresh" content="0; url=http://example.com">'
                             '<a href="http://example.com">Continue</a>')
        self.reject('matching HTTPS fallback')

    def test_template_placeholder_stays_unchanged(self):
        folder = self.root / '00_templates'
        folder.mkdir()
        template = folder / 'pdf.html'
        template.write_text(self.valid.replace(self.url, 'file_path.pdf'))
        before = template.read_bytes()
        self.assertEqual(self.check('--update').returncode, 0)
        self.assertEqual(template.read_bytes(), before)

    def test_placeholder_in_product_page_is_rejected(self):
        self.page.write_text(self.valid.replace(self.url, 'file_path.pdf'))
        self.reject('missing target')

    def test_update_handles_single_quotes_and_escaped_query(self):
        self.page.write_text(self.valid.replace(self.url, 'pdf/manual.pdf?lang=de&amp;v=old#page=2')
                             .replace('"', "'"))
        result = self.check('--update')
        self.assertEqual(result.returncode, 0, result.stderr)
        source = self.page.read_text()
        self.assertEqual(source.count('lang=de&amp;v='), 2)
        self.assertEqual(source.count('#page=2'), 2)
        self.assertNotIn('v=old', source)

    def test_target_cannot_escape_repository(self):
        self.page.write_text('<a href="../../../outside.pdf">Outside</a>')
        self.reject('target outside repository')

    def test_url_encoded_local_filename(self):
        spaced = self.pdf.with_name('manual de.pdf')
        self.pdf.rename(spaced)
        self.page.write_text(self.valid.replace('manual.pdf', 'manual%20de.pdf'))
        self.assertEqual(self.check().returncode, 0)


if __name__ == '__main__':
    unittest.main()
