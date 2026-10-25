"""Protect stable, correctly escaped PDF URLs in downloadable QR codes."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('generate_qr', Path(__file__).resolve().parents[1] / 'scripts/generate_qr.py')
qr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qr)


class QRPublishing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'site'
        self.output = Path(self.temp.name) / 'download'
        self.manual = self.root / '01/pdf/Anleitung Küche #1.pdf'
        self.manual.parent.mkdir(parents=True)
        self.manual.write_bytes(b'%PDF-1.4\nfirst version')

    def test_preview_url_is_encoded_and_outputs_both_formats(self):
        self.assertEqual(qr.generate(self.root, self.output, 'https://paul1404.github.io/QR-Redirects/'), 1)
        manifest = (self.output / 'links.tsv').read_text()
        self.assertIn('https://paul1404.github.io/QR-Redirects/01/pdf/Anleitung%20K%C3%BCche%20%231.pdf', manifest)
        self.assertTrue(Path(str(self.output / self.manual.relative_to(self.root)) + '.png').read_bytes().startswith(b'\x89PNG'))
        self.assertIn('<svg', Path(str(self.output / self.manual.relative_to(self.root)) + '.svg').read_text())

    def test_replacing_pdf_keeps_qr_identical(self):
        qr.generate(self.root, self.output, 'https://qr.wue.ch')
        before = {p.relative_to(self.output): p.read_bytes() for p in self.output.rglob('*') if p.is_file()}
        self.manual.write_bytes(b'%PDF-1.7\nreplacement')
        qr.generate(self.root, self.output, 'https://qr.wue.ch')
        self.assertEqual(before, {p.relative_to(self.output): p.read_bytes() for p in self.output.rglob('*') if p.is_file()})

    def test_same_filename_in_different_folders_does_not_collide(self):
        second = self.root / '02/pdf' / self.manual.name
        second.parent.mkdir(parents=True)
        second.write_bytes(self.manual.read_bytes())
        self.assertEqual(qr.generate(self.root, self.output, 'https://qr.wue.ch'), 2)
        self.assertEqual(len(list(self.output.rglob('*.png'))), 2)

    def test_invalid_base_addresses_are_rejected(self):
        for base in ('http://example.com', 'https://example.com/?x=1', 'https://example.com/#foo', 'https://user:pass@example.com', 'https:///missing-host'):
            with self.subTest(base=base), self.assertRaises(ValueError):
                qr.generate(self.root, self.output, base)

    def test_no_manuals_is_an_error(self):
        self.manual.unlink()
        with self.assertRaisesRegex(ValueError, 'no manuals'):
            qr.generate(self.root, self.output, 'https://qr.wue.ch')


if __name__ == '__main__':
    unittest.main()
