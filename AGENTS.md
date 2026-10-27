# Repository guidance

- Keep this a static PDF hosting site. New manuals need only a PDF upload and a
  QR code pointing directly to its permanent HTTPS address. Do not add a build,
  framework, embedded viewer, asset hashing, or per-document HTML generation.
- Updates replace the PDF at the same path. No version query or update command
  is required. Browser and GitHub Pages caches can briefly retain an older file.
- Preserve published PDF paths, `CNAME`, and the existing printed QR address
  `/01/hy-alarm`. Its small HTML redirect must continue to point to
  `pdf/Kundenanleitung_HY_Alarm.pdf` with a visible matching link.
- Preserve `01/qr_01_HY-Alarm.png` byte-for-byte: it encodes the already printed
  `http://qr.wue.ch/01/hy-alarm`. Generated downloads are separate artifacts.
- New QR images should encode the PDF URL, not an intermediary or QR-provider URL.
- The Python 3.9+ standard-library checker is read-only. Run
  `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v`.
- iOS Safari crops embedded PDFs in this layout. Direct PDF navigation uses the
  browser's native reader; verify opening, zoom and scrolling when changing routing.
- Preview with `python3 -m http.server 8765 --bind 127.0.0.1`, using `.html` for
  the legacy alias locally. Stop temporary previews afterward.

- QR generation uses pinned Segno from `scripts/qr-requirements.txt` only in tooling.
  `scripts/generate_qr.py --output /tmp/qr-codes` creates PNG/SVG and links.tsv
  for `*/pdf/*.pdf`; URLs remain independent of PDF contents. Run tests after
  installing that requirements file. Keep generated images out of source commits.
- CI uploads QR downloads as a 90-day artifact without repository write access.
  Fork runs use their GitHub Pages URL, original runs use CNAME. Never distribute
  fork preview QR codes as production codes.
