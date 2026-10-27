# Produktanleitungen per QR-Code

## Neue Anleitung veröffentlichen

1. Die PDF in `01/pdf/` hochladen und speichern. Einen dauerhaften Dateinamen
   ohne Datum oder Versionsnummer wählen, beispielsweise `produkt.pdf`.
2. Unter **Actions → Check static pages** den erfolgreichen Lauf öffnen und
   unten das Artefakt **qr-codes** herunterladen. Es enthält zu jeder PDF einen
   QR-Code als PNG und SVG sowie `links.tsv` mit den Zieladressen.
3. Den QR-Code scannen, die Anleitung prüfen und anschließend drucken.

Dafür ist keine HTML-Seite, Kopiervorlage oder externe QR-Code-Website erforderlich.
Die SVG eignet sich für den Druck in beliebiger Größe. Den weißen Rand erhalten.
Nach 90 Tagen läuft der Download ab; ein neuer Lauf erzeugt dieselben Codes erneut.

Im Originalrepository verwenden die Codes die Domain aus `CNAME`, aktuell
`https://qr.wue.ch`. **Im Fork zeigen sie auf dessen GitHub-Pages-Vorschau und sind
nur zum Testen bestimmt.** Vor dem Druck immer die Zieladresse kontrollieren.
Der Lauf erstellt die Bilder als Download und schreibt keine Dateien zurück ins
Repository. Die Website bleibt unverändert statisch.

## Anleitung aktualisieren

Die vorhandene PDF durch die neue Fassung **unter demselben Namen im selben
Ordner ersetzen**. Weitere Dateien müssen nicht bearbeitet werden. Die Adresse
bleibt gleich und bereits gedruckte QR-Codes bleiben gültig.

GitHub Pages und Browser können noch kurz eine vorherige Fassung anzeigen.
Nach der Veröffentlichung neu laden und die neue Fassung kontrollieren.

## Bereits gedruckte QR-Codes

Die bestehende Adresse <https://qr.wue.ch/01/hy-alarm> bleibt erhalten.
`01/hy-alarm.html` leitet automatisch auf die unveränderte PDF-Adresse weiter:

<https://qr.wue.ch/01/pdf/Kundenanleitung_HY_Alarm.pdf>

Diese kleine Weiterleitung wird beim Austausch der PDF nicht angepasst.
Auch die vorhandene Bilddatei `01/qr_01_HY-Alarm.png` bleibt unverändert.
Sie enthält `http://qr.wue.ch/01/hy-alarm`. GitHub Pages leitet diese Adresse
bereits auf HTTPS um; die bestehende HTML-Adresse öffnet anschließend die PDF.
Gedruckte Codes müssen nicht ausgetauscht werden.

Die automatisch erzeugten QR-Downloads sind davon unabhängig und zeigen für
neue Ausdrucke direkt auf die PDF. Beim Aktualisieren weder die alte
HTML-Adresse noch den PDF-Pfad umbenennen oder entfernen.

## Betrieb und Prüfung

Die Website besteht aus statischen Dateien. GitHub Pages veröffentlicht `main`
aus dem Stammverzeichnis; `CNAME` legt die bestehende Domain fest.
Die Startseite leitet weiterhin zu <https://wue.ch> weiter.

Die automatische Prüfung meldet fehlende lokale Dateien, unpassende
Weiterleitungslinks und Dateien ohne PDF-Kennung. Sie verändert keine Dateien
und benötigt keine zusätzlichen Python-Pakete. Nur die QR-Erzeugung verwendet
das fest versionierte Python-Paket Segno 1.6.6. Die Erzeugung läuft lokal
im GitHub-Runner, ohne externe API.

Für die lokale Prüfung mit Python 3.9 oder neuer:

```sh
python3 -m pip install -r scripts/qr-requirements.txt
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

`00_templates/redirect_template.html` ist nur für optionale Weiterleitungen
auf externe Adressen vorgesehen. Für neue PDF-Anleitungen wird sie nicht benötigt.

Eine lokale Vorschau lässt sich mit
`python3 -m http.server 8765 --bind 127.0.0.1` starten. Die bestehende Weiterleitung
lokal unter <http://127.0.0.1:8765/01/hy-alarm.html> testen, da der einfache Server
keine endungslosen HTML-Adressen auflöst. Anschließend die Vorschau mit Strg+C
beenden.

Ein Fork übernimmt die Domain des Originals nicht. Für Vorschauen keine fremde
Domain konfigurieren.

QR-Codes lokal erzeugen, beispielsweise zum Prüfen der Vorschau:

```sh
python3 scripts/generate_qr.py --base-url https://paul1404.github.io/QR-Redirects --output /tmp/qr-codes
```

Ohne `--base-url` wird die Domain aus `CNAME` verwendet.
