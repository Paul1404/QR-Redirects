# Repository guidance

- Keep this as a static GitHub Pages site. Do not add a framework, package manager,
  PDF library, or build step for the existing redirect and PDF pages.
- Preserve published HTML paths, PDF paths, and `CNAME`; printed QR codes depend
  on stable URLs. New QR images should encode the HTTPS HTML route.
- PDF pages must offer a visible direct link to the same PDF URL as their iframe.
  Open it in a new tab with `rel="noopener"` so the original viewer stays loaded.
- After changing a PDF, run `python3 scripts/check.py --update` and commit the PDF
  and updated HTML together. Run `python3 scripts/check.py` and
  `python3 -m unittest discover -s tests -v` before committing.
- Validation uses Python 3.9+ and its standard library only. The PDF template's
  `file_path.pdf` placeholder is intentionally exempt from file-existence checks.
- Preview with `python3 -m http.server 8765 --bind 127.0.0.1`, using `.html` URLs.
  Check desktop and mobile layouts and stop the server afterward. A local check
  does not verify GitHub Pages deployment or real-device PDF support.

## Fork preview

- `Paul1404/QR-Redirects` publishes this fork-only `gh-pages` branch at
  `https://paul1404.github.io/QR-Redirects/` using branch publishing from `/`.
- `CNAME` is intentionally absent on this branch. Do not claim the upstream
  custom domain. Keep this preview-only change out of the upstream proposal.
- This is a snapshot of the fix branch, not an automatic per-PR deployment.
  After refreshing it, validate the published manual route and direct PDF link.
