#!/usr/bin/env python3
"""Check static page targets; --update refreshes PDF versions from file contents."""

import argparse
import hashlib
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]


def local_target(page, url):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path:
        return None
    target = ((ROOT / unquote(parts.path).lstrip('/')) if parts.path.startswith('/')
              else page.parent / unquote(parts.path)).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError(f'{page.relative_to(ROOT)}: target outside repository: {url}')
    return target


def pdf_version(target):
    return hashlib.sha256(target.read_bytes()).hexdigest()[:12]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.pdf_frames = []
        self.anchors = []
        self.redirects = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src', 'data'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'iframe' and attrs.get('src'):
            self.pdf_frames.append(attrs['src'])
        if tag == 'a' and attrs.get('href'):
            self.anchors.append(attrs['href'])
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            match = re.search(r'url=(.+)', attrs.get('content', ''), re.IGNORECASE)
            if match:
                self.redirects.append(match.group(1).strip())


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--update', action='store_true', help='Update PDF cache versions before checking')
    options = args.parse_args()
    errors = []
    pages = sorted(ROOT.glob('**/*.html')) + sorted(ROOT.glob('**/*.htm'))
    for page in pages:
        if '.git' in page.relative_to(ROOT).parts:
            continue
        template = page.relative_to(ROOT).parts[0] == '00_templates'
        source = page.read_text(encoding='utf-8')
        if options.update and not template:
            def update(match):
                url = unescape(match.group(2))
                target = local_target(page, url)
                if target is None or target.suffix.lower() != '.pdf' or not target.is_file():
                    return match.group(0)
                parts = urlsplit(url)
                query = [(key, value) for key, value in parse_qsl(parts.query) if key != 'v']
                query.append(('v', pdf_version(target)))
                versioned = urlunsplit(parts._replace(query=urlencode(query)))
                return match.group(1) + escape(versioned, quote=True) + match.group(3)
            source = re.sub(r'((?:href|src)=")([^"]*)(")', update, source)
            page.write_text(source, encoding='utf-8')
        parsed = Page()
        parsed.feed(source)
        for url in parsed.links:
            # This placeholder is replaced when copying the PDF template.
            if template and url == 'file_path.pdf':
                continue
            target = local_target(page, url)
            if target is None:
                continue
            if not target.is_file():
                errors.append(f'{page.relative_to(ROOT)}: missing target: {url}')
            elif target.suffix.lower() == '.pdf' and not template:
                versions = dict(parse_qsl(urlsplit(url).query))
                if versions.get('v') != pdf_version(target):
                    errors.append(f'{page.relative_to(ROOT)}: stale PDF version: run python3 scripts/check.py --update')
        for url in parsed.redirects:
            if not url.startswith('https://') or url not in parsed.anchors:
                errors.append(f'{page.relative_to(ROOT)}: redirect needs a matching HTTPS fallback link')
        for url in parsed.pdf_frames:
            if urlsplit(url).path.lower().endswith('.pdf') and url not in parsed.anchors:
                errors.append(f'{page.relative_to(ROOT)}: PDF iframe needs a direct link to the same URL')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Checked {len(pages)} HTML pages: targets, PDF versions, and fallback links OK.')


if __name__ == '__main__':
    main()
