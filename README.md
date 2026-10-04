# Python CI/CD Rechner

## Was macht das Projekt?

Dieses Projekt ist eine kleine Python-Anwendung mit einfachen mathematischen Funktionen für Summe, Durchschnitt und Prozentberechnung.

Das Ziel des Projekts ist die Umsetzung einer CI/CD-Pipeline mit GitHub Actions. Die Anwendung wird automatisch getestet, als ZIP-Datei gebaut und anschließend über eine GitHub Release veröffentlicht.

## Pipeline im Überblick

Die Pipeline besteht aus zwei Jobs: `test` und `deploy`.

### Job: test

Der `test`-Job führt folgende Schritte aus:

1. Repository mit `actions/checkout` auschecken
2. Python 3.12 einrichten
3. Pip-Cache verwenden
4. Dependencies aus `requirements.txt` installieren
5. Automatisierte Tests mit `pytest` ausführen
6. `rechner.zip` erstellen
7. ZIP-Datei als Artifact hochladen

Der Cache verwendet `hashFiles('requirements.txt')`. Dadurch kann bei Änderungen der Dependencies ein neuer Cache erzeugt werden.

### Job: deploy

Der `deploy`-Job ist mit `needs: test` vom erfolgreichen `test`-Job abhängig.

Er führt folgende Schritte aus:

1. Artifact `rechner.zip` herunterladen
2. Environment `production` verwenden
3. `DEPLOY_TOKEN` und `DEPLOY_TARGET` verwenden
4. Auf die Freigabe des Production-Deployments warten
5. Eine GitHub Release erstellen
6. `rechner.zip` als Release-Asset veröffentlichen

Die Pipeline läuft in folgender Reihenfolge:

```text
Push / Pull Request
        |
        v
      test
        |
        v
   Tests + Build
        |
        v
  Artifact Upload
        |
        v
      deploy
        |
        v
 Artifact Download
        |
        v
 Production-Freigabe
        |
        v
   GitHub Release
```

Die Berechtigungen sind eingeschränkt. Standardmäßig wird `contents: read` verwendet. Der `deploy`-Job erhält zusätzlich die benötigten Rechte für die Erstellung der Release.

## Trigger

Die Pipeline startet automatisch bei:

- einem Push auf den Branch `main`
- einem Pull Request auf den Branch `main`

Das Deployment wird nur bei einem Push auf `main` ausgeführt.

Dafür wird folgende Bedingung verwendet:

```yaml
if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

Bei einem Pull Request kann der `test`-Job ausgeführt werden, während das Production-Deployment übersprungen wird.

## Secrets und Environment

Für das Projekt wird folgendes Secret verwendet:

```text
DEPLOY_TOKEN
```

Der Wert des Secrets wird nicht im Repository gespeichert und nicht in den Logs ausgegeben.

Zusätzlich wird folgende Repository Variable verwendet:

```text
DEPLOY_TARGET
```

Sie enthält das Deployment-Ziel `staging`.

Für das Deployment wird das GitHub Environment

```text
production
```

verwendet.

Das Environment besitzt eine Protection Rule mit erforderlicher Freigabe vor dem Deployment. Das Deployment ist außerdem auf den Branch `main` beschränkt.

## Deployment

Nach erfolgreichen Tests erstellt die Pipeline das Build-Artefakt:

```text
rechner.zip
```

Dieses wird zunächst als GitHub Actions Artifact gespeichert.

Der `deploy`-Job lädt dasselbe Artifact wieder herunter. Nach der Freigabe des Environments `production` erstellt die Pipeline automatisch eine GitHub Release.

`rechner.zip` wird dabei als Release-Asset veröffentlicht.

Das erfolgreiche Deployment kann auf der Releases-Seite des GitHub-Repositories überprüft werden.

## Lokal ausführen

Virtuelle Python-Umgebung erstellen:

```bash
python3 -m venv .venv
```

Virtuelle Umgebung unter macOS/Linux aktivieren:

```bash
source .venv/bin/activate
```

Dependencies installieren:

```bash
python -m pip install -r requirements.txt
```

Tests ausführen:

```bash
python -m pytest -v
```

Build lokal erstellen:

```bash
zip -r rechner.zip src README.md
```

Die Anwendung enthält drei automatisierte Tests für die Funktionen `summe`, `durchschnitt` und `prozent`.

## Abschluss-Challenge

Die sechs Probleme der Abschluss-Challenge sowie ihre Ursachen und Lösungen sind separat dokumentiert in:

```
ABSCHLUSS_CHALLENGE.md
```