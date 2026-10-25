# QR Redirect

Stabile Kurzlinks für QR-Codes und Produktanleitungen unter <https://qr.wue.ch>.
Die Website besteht aus statischen HTML-Seiten und PDFs. GitHub Pages
veröffentlicht den Inhalt von `main` im Stammverzeichnis. Es gibt keinen Build
und keine Laufzeitabhängigkeiten.

## Bestehende Links

- <https://qr.wue.ch/> leitet auf <https://wue.ch> weiter.
- <https://qr.wue.ch/01/hy-alarm> öffnet die HY-Alarm-Anleitung mit einem
  zusätzlichen direkten PDF-Link in einem neuen Tab. Auf kleineren Bildschirmen
  und Touch-Geräten öffnet dieser Link die Anleitung im PDF-Reader des Browsers;
  größere Bildschirme bieten zusätzlich die eingebettete Vorschau.

Die Adresse auf einem gedruckten QR-Code muss dauerhaft bestehen bleiben.
Deshalb die HTML-Seite beim Austausch einer Anleitung nicht umbenennen oder
löschen. `CNAME` legt die Domain fest und darf nicht versehentlich geändert werden.

## Neue Anleitung hinzufügen

1. `00_templates/pdf_viewer_template.html` nach beispielsweise
   `01/produkt.html` kopieren.
2. Die PDF-Datei unter `01/pdf/` ablegen.
3. In der HTML-Seite den Produktnamen im Seitentitel und im iframe-Titel
   eintragen. Den Platzhalter `file_path.pdf` an beiden Stellen durch denselben
   relativen PDF-Pfad ersetzen, zum Beispiel `pdf/Produkt.pdf`.
4. Im Repository ausführen:

   ```sh
   python3 scripts/check.py --update
   python3 scripts/check.py
   python3 -m unittest discover -s tests -v
   ```

5. HTML und PDF gemeinsam committen. Nach der Veröffentlichung die vollständige
   HTTPS-Adresse aufrufen und den direkten PDF-Link prüfen. Erst danach den
   QR-Code erstellen und auf einem Smartphone testen.

## Anleitung aktualisieren

Die PDF unter ihrem bestehenden Namen ersetzen und
`python3 scripts/check.py --update` ausführen. Der Befehl berechnet die Version
`?v=...` aus dem SHA-256-Inhalt der PDF und aktualisiert sowohl den Viewer als
auch den direkten Link. PDF und geänderte HTML-Datei gemeinsam committen.

`python3 scripts/check.py` und die GitHub-Actions-Prüfung melden fehlende lokale
Dateien, veraltete PDF-Versionen und fehlende direkte PDF-Links. Die Prüfung
verwendet nur die Python-Standardbibliothek (Python 3.9 oder neuer) und benötigt
keine zusätzlichen Pakete.

Die neue Version wird angefordert, sobald die aktualisierte HTML-Seite geladen
wird. GitHub Pages und Browser können die HTML-Seite selbst noch zwischenspeichern.
Ein Versionsparameter erzwingt deshalb keine sofortige Aktualisierung bei allen
Besuchern. Nach dem Deployment neu laden und die veröffentlichte Version prüfen.

## Externe Weiterleitung hinzufügen

`00_templates/redirect_template.html` kopieren. Die HTTPS-Zieladresse sowohl
im `meta`-Refresh als auch im sichtbaren Link anpassen und den Seitentitel
aktualisieren. Anschließend die lokale Prüfung ausführen und die Weiterleitung
nach der Veröffentlichung testen.

## QR-Code erstellen

Der QR-Code muss direkt die stabile HTTPS-Adresse enthalten, zum Beispiel
`https://qr.wue.ch/01/hy-alarm`. Keine PDF-Adresse, Versionsparameter oder
Weiterleitungsadresse eines QR-Anbieters verwenden. Der gespeicherte Code
`01/qr_01_HY-Alarm.png` verwendet diese HTTPS-Adresse. Bereits gedruckte
HTTP-Codes funktionieren weiterhin über die bestehende HTTPS-Weiterleitung.

## Vorlagen und lokale Vorschau

`00_templates/` enthält Kopiervorlagen und ein einfaches HTML-Beispiel. Die
Vorlagen sind keine fertigen Produktseiten. Platzhalter vor dem Veröffentlichen
einer kopierten Seite ersetzen. Keine Word-HTML-Exporte mit fehlenden
Begleitdateien übernehmen.

Für eine lokale Vorschau `python3 -m http.server 8765 --bind 127.0.0.1` ausführen
und <http://127.0.0.1:8765/01/hy-alarm.html> öffnen. Ein einfacher lokaler Server
bietet die endungslosen GitHub-Pages-Adressen nicht an, daher lokal `.html`
verwenden. Die Vorschau anschließend mit Strg+C beenden.

Ein Fork übernimmt durch `CNAME` nicht die Domain des Originals. GitHub Pages
im Fork nur bei Bedarf separat konfigurieren und dafür keine fremde Domain
beanspruchen.
