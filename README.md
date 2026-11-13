# QR-Redirects

Dieses Repository enthält kurze Adressen für QR-Codes auf Produktanleitungen. Die Seiten unter `01/` öffnen die zugehörigen PDFs oder leiten auf eine andere Anleitung weiter. Die gewünschte Domain steht in `CNAME`; die Pages-Domain muss in GitHub entsprechend eingerichtet sein.

## Anleitung hinzufügen

1. Das PDF im passenden Ordner ablegen.
2. `00_templates/pdf_viewer_template.html` kopieren und den PDF-Pfad anpassen. Für eine externe Zielseite `00_templates/redirect_template.html` verwenden.
3. Die HTML-Datei unter einem kurzen, dauerhaften Namen speichern und die veröffentlichte Adresse prüfen.
4. Einen QR-Code für diese Adresse erstellen und vor dem Druck testen.

## Anleitung aktualisieren

Die neue PDF-Version unter demselben Namen ablegen und den Versionsparameter in der HTML-Seite ändern. Bereits gedruckte Adressen und QR-Codes müssen erhalten bleiben; auch Browser und Pages können ältere Inhalte vorübergehend zwischenspeichern.

Die bestehende HY-Alarm-Anleitung liegt unter `01/hy-alarm.html`, das PDF unter `01/pdf/`. Die vorhandene QR-Grafik `01/qr_01_HY-Alarm.png` darf nicht überschrieben werden.
