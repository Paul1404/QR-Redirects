# Produktanleitungen per QR-Code

## Neue Anleitung veröffentlichen

1. Die PDF in `01/pdf/` hochladen und speichern. Einen dauerhaften Dateinamen
   ohne Datum oder Versionsnummer wählen, beispielsweise `produkt.pdf`.
2. Nach der Veröffentlichung die PDF öffnen und ihre vollständige HTTPS-Adresse
   für den QR-Code verwenden. Beispiel: `https://qr.wue.ch/01/pdf/produkt.pdf`.
3. Den erzeugten QR-Code scannen und die Anleitung prüfen.

Dafür ist keine HTML-Seite oder Kopiervorlage erforderlich.

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
Der gespeicherte QR-Code `01/qr_01_HY-Alarm.png` zeigt für neue Ausdrucke direkt
auf die PDF. Alte HTTP-Codes funktionieren weiterhin über die bestehende
HTTPS-Weiterleitung.

## Betrieb und Prüfung

Die Website besteht aus statischen Dateien. GitHub Pages veröffentlicht `main`
aus dem Stammverzeichnis; `CNAME` legt die bestehende Domain fest.
Die Startseite leitet weiterhin zu <https://wue.ch> weiter.

Die automatische Prüfung meldet fehlende lokale Dateien, unpassende
Weiterleitungslinks und Dateien ohne PDF-Kennung. Sie verändert keine Dateien
und benötigt keine zusätzlichen Python-Pakete.

Für die lokale Prüfung mit Python 3.9 oder neuer:

```sh
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
