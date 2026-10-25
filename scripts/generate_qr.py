#!/usr/bin/env python3
"""Create downloadable QR images for every manual, without editing the site."""
import argparse
from pathlib import Path
from urllib.parse import quote, urlsplit

import segno

ROOT = Path(__file__).resolve().parents[1]


def generate(root, output, base_url):
    parts = urlsplit(base_url)
    if (parts.scheme != 'https' or not parts.hostname or parts.username
            or parts.password or parts.query or parts.fragment):
        raise ValueError('base URL must be an HTTPS address without credentials, query or fragment')
    manuals = sorted(root.glob('*/pdf/*'))
    rows = ['PDF\tURL\tPNG\tSVG']
    for pdf in manuals:
        if not pdf.is_file() or pdf.suffix.lower() != '.pdf':
            continue
        if not pdf.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'PDF points outside repository: {pdf}')
        relative = pdf.relative_to(root)
        url = base_url.rstrip('/') + '/' + quote(relative.as_posix(), safe='/')
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        qr = segno.make_qr(url, error='m')
        for kind in ('png', 'svg'):
            qr.save(str(target) + '.' + kind, scale=12, border=4, light='white', dark='black')
        rows.append(f'{relative}\t{url}\t{relative}.png\t{relative}.svg')
    if len(rows) == 1:
        raise ValueError('no manuals found in */pdf/')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'links.tsv').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    return len(rows) - 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=None)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = args.base_url or 'https://' + (ROOT / 'CNAME').read_text().strip()
    print(f'Generated QR codes for {generate(ROOT, args.output, base)} manuals: {base}')


if __name__ == '__main__':
    main()
