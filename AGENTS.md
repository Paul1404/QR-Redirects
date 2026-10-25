# Repository guidance

- Keep this a static PDF hosting site. New manuals need only a PDF upload and a
  QR code pointing directly to its permanent HTTPS address. Do not add a build,
  framework, embedded viewer, asset hashing, or per-document HTML generation.
- Updates replace the PDF at the same path. No version query or update command
  is required. Browser and GitHub Pages caches can briefly retain an older file.
- Preserve published PDF paths, `CNAME`, and the existing printed QR address
  `/01/hy-alarm`. Its small HTML redirect must continue to point to
  `pdf/Kundenanleitung_HY_Alarm.pdf` with a visible matching link.
- New QR images should encode the PDF URL, not an intermediary or QR-provider URL.
- The Python 3.9+ standard-library checker is read-only. Run
  `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v`.
- iOS Safari crops embedded PDFs in this layout. Direct PDF navigation uses the
  browser's native reader; verify opening, zoom and scrolling when changing routing.
- Preview with `python3 -m http.server 8765 --bind 127.0.0.1`, using `.html` for
  the legacy alias locally. Stop temporary previews afterward.

## Fork preview

- `Paul1404/QR-Redirects` publishes this fork-only `gh-pages` branch at
  `https://paul1404.github.io/QR-Redirects/` using branch publishing from `/`.
- `CNAME` is intentionally absent on this branch. Do not claim the upstream
  custom domain. Keep this preview-only change out of the upstream proposal.
- This is a snapshot of the fix branch, not an automatic per-PR deployment.
  After refreshing it, validate the published manual route and direct PDF link.
