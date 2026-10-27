# Repository guidance

- Keep this a static GitHub Pages site without an embedded PDF viewer, framework,
  server or database. The generated site is the deployment artifact, not source commits.
- Printed QR codes must use permanent short addresses such as `/01/produkt1`,
  never PDF filenames or a QR-provider URL. The short page opens the PDF directly
  in the browser reader. An HTTPS website target can later replace the PDF target.
- `scripts/generate_qr.py` derives short addresses from `*/pdf/*.pdf` (remove
  Kundenanleitung prefix, normalize spelling) and applies `redirects.json` overrides.
  It produces HTML redirects with matching fallback links, PNG/SVG QR downloads,
  and links.tsv. Colliding names fail instead of reassigning an address.
- Preserve existing short addresses when renaming/removing PDFs by recording their
  new target in redirects.json first. Never repurpose a printed address for another product.
- Preserve CNAME, the original HY-Alarm PDF and its path, `/01/hy-alarm` and
  `/01/hy-alarm.html`. The JSON mapping pins this route explicitly.
  Keep `01/qr_01_HY-Alarm.png` byte-for-byte: it encodes the printed
  `http://qr.wue.ch/01/hy-alarm`. Generated downloads must not replace this file.
- PDF updates replace the same filename. No hash/version parameters are required;
  Pages/browser caches can briefly retain an older file. Inspect after publication.
- QR tooling uses pinned Segno from scripts/qr-requirements.txt. Validation uses
  Python 3.9+ standard library. Run unit tests, source check, build, built-site check.
- `python3 scripts/generate_qr.py --output /tmp/qr-codes --site-output /tmp/qr-site`
  requires a new site output directory outside source. `--base-url` supports previews.
- GitHub Pages must use Source GitHub Actions. CI checks and builds before deployment;
  only default-branch pushes/manual runs deploy. Fork manual runs can explicitly
  enable the preview input. Pull requests never deploy. Repository write access is
  unnecessary. Pages and OIDC permissions belong only to the deployment job.
- Fork builds use their project Pages prefix and omit the original CNAME. Production
  retains the existing domain. Fork QR downloads are test codes, not production labels.
- Local server previews need `.html` URLs because Python's HTTP server does not
  resolve extensionless Pages routes. Use an isolated port and stop afterward.
- Routing changes need browser navigation checks including zoom, page 12 and rotation
  on iOS Safari. Existing simulator harnesses are fork-only test branches.
