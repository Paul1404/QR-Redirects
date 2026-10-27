# Produktanleitungen per QR-Code

## Neue Anleitung veröffentlichen

1. Die PDF in `01/pdf/` hochladen und speichern, beispielsweise
   `Kundenanleitung_Produkt1.pdf`.
2. GitHub erzeugt automatisch die kurze Adresse **`https://qr.wue.ch/01/produkt1`**,
   die zugehörige HTML-Weiterleitung und den passenden QR-Code als PNG und SVG.
3. Unter **Actions → Check static pages → erfolgreicher Lauf → Artifacts → qr-codes**
   die Bilder herunterladen. Nach der Veröffentlichung scannen, die Anleitung
   kontrollieren und erst dann drucken. Den weißen Rand um den QR-Code erhalten.

Die kurze Adresse bleibt auf dem Gerät. Dahinter kann heute die PDF liegen und
später eine Anleitung auf der neuen Website. Eine HTML-Kopiervorlage muss nicht
mehr bearbeitet werden. Es gibt keinen eingebetteten PDF-Viewer.

Die kurze Adresse entsteht aus Produktordner und Dateiname: Der Anfang
`Kundenanleitung_` entfällt, Buchstaben werden klein geschrieben, Umlaute als
`ae`, `oe`, `ue` ausgeschrieben und Leerzeichen durch Bindestriche ersetzt.
`01/pdf/Kundenanleitung_Produkt1.pdf` ergibt damit `01/produkt1`.
Doppelte kurze Adressen brechen die Prüfung ab und müssen durch unterschiedliche
Dateinamen vermieden werden.

Im Fork zeigen erzeugte Codes auf dessen GitHub-Pages-Vorschau. **Diese Codes
sind nur zum Testen bestimmt.** Im Original verwenden sie die Domain aus `CNAME`,
aktuell `qr.wue.ch`. Die Datei `links.tsv` im Download nennt jede kurze Adresse
und ihr Weiterleitungsziel. Downloads sind 90 Tage verfügbar und lassen sich mit
einem neuen Lauf erneut erzeugen.

## Anleitung aktualisieren

Die PDF unter **demselben Namen im selben Ordner ersetzen**. Die kurze Adresse
und der QR-Code bleiben gleich. Keine HTML-Datei anpassen.

GitHub Pages und Browser können kurz noch eine vorherige Fassung anzeigen.
Nach der Veröffentlichung die neue Fassung kontrollieren.

## Später auf die neue Website umstellen

In `redirects.json` das Ziel der kurzen Adresse eintragen oder ändern:

```json
{
  "01/hy-alarm": "01/pdf/Kundenanleitung_HY_Alarm.pdf",
  "01/produkt1": "https://wue.ch/anleitungen/produkt1"
}
```

Nach erfolgreicher Veröffentlichung führt **derselbe gedruckte Code** zur neuen
Website. Die kurze Adresse und das QR-Bild ändern sich dabei nicht. Externe Ziele
müssen HTTPS verwenden. Die Datei kann auch mehrere kurze Adressen zu derselben
Anleitung enthalten. Lokale Ziele sind Pfade ab dem Repository-Stamm.

Vor dem Umbenennen, Verschieben oder Entfernen einer bereits verteilten PDF die
bisherige kurze Adresse ausdrücklich in `redirects.json` festhalten und auf das
neue Ziel setzen. Sonst entfällt die automatisch abgeleitete Adresse beim nächsten
Veröffentlichen. Bereits gedruckte kurze Adressen niemals löschen oder für ein
anderes Produkt wiederverwenden.

## Bereits gedruckter HY-Alarm-Code

Die Bilddatei `01/qr_01_HY-Alarm.png` bleibt bytegenau unverändert. Ihr Inhalt ist
`http://qr.wue.ch/01/hy-alarm`. Die bestehende HTTP-zu-HTTPS-Weiterleitung bleibt
bestehen. Anschließend öffnet die kurze Adresse die PDF im Browser.

`01/hy-alarm` und `01/hy-alarm.html` bleiben erhalten. Die Weiterleitung besitzt
zusätzlich einen anklickbaren Link. Domain, PDF-Datei und PDF-Pfad bleiben im PR
unverändert. Die neu erzeugten Downloads werden separat bereitgestellt und
überschreiben das alte QR-Bild nicht.

## Einmalige Einrichtung beim Übernehmen des PR

Unter **Settings → Pages → Build and deployment → Source** die Quelle
**GitHub Actions** auswählen. Die bestehende Domain `qr.wue.ch` und die
HTTPS-Einstellung beibehalten. Anschließend den Workflow auf `main` ausführen.
Die Umstellung betrifft die Veröffentlichung, nicht Domain oder QR-Adressen.

Danach ist der Ablauf automatisch: Änderung speichern, prüfen, Weiterleitungen
und QR-Bilder erzeugen, erzeugte Website prüfen und veröffentlichen.
Ein fehlgeschlagener Prüflauf veröffentlicht keine neue Website.
Pull Requests erzeugen nur Prüfergebnisse und Downloads, keine Veröffentlichung.
Der bisherige Stand bleibt bis zu einer erfolgreichen Veröffentlichung verfügbar.

Die Website bleibt statisch. Im Quellrepository entstehen keine automatischen
Commits. Nur der Veröffentlichungsjob erhält `pages: write` und `id-token: write`;
Prüfung und QR-Erzeugung haben keinen Schreibzugriff auf das Repository.
Segno 1.6.6 ist das einzige gezielt hinzugefügte QR-Paket, ohne externe QR-API.
Die Startseite leitet weiterhin zu `https://wue.ch` weiter.

## Lokal prüfen

Python 3.9 oder neuer:

```sh
python3 -m pip install -r scripts/qr-requirements.txt
python3 -m unittest discover -s tests -v
python3 scripts/check.py
python3 scripts/generate_qr.py --output /tmp/qr-codes --site-output /tmp/qr-site
python3 scripts/check.py --root /tmp/qr-site
```

Das Website-Ausgabeverzeichnis muss neu sein und außerhalb des Quellrepositorys
liegen. Für eine Vorschau kann mit `--base-url` eine andere HTTPS-Basisadresse
angegeben werden. Im Fork wird keine fremde Domain veröffentlicht.

`python3 -m http.server 8765 --bind 127.0.0.1 --directory /tmp/qr-site` startet eine
lokale Vorschau. Dort `01/produkt1.html` verwenden, da der einfache Server keine
endungslosen HTML-Adressen auflöst. Anschließend mit Strg+C beenden.

Die statische Prüfung erkennt unter anderem fehlende lokale Ziele, unpassende
Weiterleitungslinks, Pfade außerhalb des Repositorys und Dateien ohne PDF-Kennung.
Das ist keine vollständige Prüfung des PDF-Inhalts.
