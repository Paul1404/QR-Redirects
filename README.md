# QR Redirect

Verwaltung von Kurzlinks für QR-Codes

## Konzept
Anleitungen können Mittels QR Code als pdf geöffnet werden, damit wir sicherstellen können, dass dieser immer gültig ist, verwalten wir diesen unter qr.wue.ch.

qr.wue.ch ist auf unser git repo redirected (public)
01/hy-alarm ist eine html Seite auf unserem git repo
diese Seite öffnet dann ein bestimmtes pdf


## Ordner Verzeichnis
01 - Anleitungen
...

## Neue Files hinzufügen
Um eine neue Anleitung hinzuzufügen muss im eine neue .html Datei angelegt werden (möglichst kurzer Name) code von pdf_viewer_template.html kopieren
und ein pdf mit der Anleitung erstellt werden. Das pdf wird unter qr.wue.ch/xx/produkt_name im Vollscreen angezeigt.

## File aktualisieren
Neuste Version unter dem gleichen Namen ablegen, dann noch den Parameter v (Version) im html ergänzen, damit wird auch sicher das Neuste geladen.
Kann etwas dauern, bis vom Browser die neue html Seite geladen wird.

## Redirects hinzufügen
Um auf eine Anleitung unter einer anderen Domain zu verweisen muss eine Kopie von redirect_template.html (mit möglichst kurzem Namen) erstellt werden und dort muss dann der Link der Ziel Adresse eingegeben werden. Die neue Adresse wird automatisch unter qr.wue.ch/produkt_name geöffnet

## QR Code erstellen
https://genqrcode.com/
Sicherstellen, dass der qr auf qr.wue.ch zeigt und nicht auf die Seite des QR Anbieters

http://qr.wue.ch/01/hy-alarm