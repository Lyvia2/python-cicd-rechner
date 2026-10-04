# Python CI/CD Rechner

## Projektbeschreibung

Dieses Projekt ist ein kleines Python-Projekt zur Demonstration einer vollständigen CI/CD-Pipeline mit GitHub Actions.

Die Anwendung stellt einfache mathematische Funktionen zur Verfügung. Die Pipeline führt automatisierte Tests aus, erstellt ein Build-Artefakt und veröffentlicht dieses anschließend automatisch als GitHub Release.

---

## Funktionen der Anwendung

Die Anwendung enthält folgende mathematische Funktionen:

- Summe
- Durchschnitt
- Prozentberechnung

Der Quellcode befindet sich in:

```text
src/rechner.py
```

Die automatisierten Tests befinden sich in:

```text
tests/test_rechner.py
```

---

## Projektstruktur

```text
python-cicd-rechner/
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── src/
│   └── rechner.py
├── tests/
│   └── test_rechner.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Lokale Installation

Zuerst wird eine virtuelle Python-Umgebung erstellt:

```bash
python3 -m venv .venv
```

Unter macOS oder Linux wird sie folgendermaßen aktiviert:

```bash
source .venv/bin/activate
```

Danach werden die benötigten Abhängigkeiten installiert:

```bash
python -m pip install -r requirements.txt
```

---

## Tests lokal ausführen

Die automatisierten Tests werden mit `pytest` ausgeführt:

```bash
python -m pytest -v
```

Das Projekt enthält Tests für:

- `summe`
- `durchschnitt`
- `prozent`

Alle Tests müssen erfolgreich sein, bevor das Deployment durchgeführt werden kann.

---

## CI/CD-Pipeline

Die CI/CD-Pipeline wird mit GitHub Actions umgesetzt.

Die Workflow-Datei befindet sich unter:

```text
.github/workflows/pipeline.yml
```

Die Pipeline wird automatisch bei folgenden Ereignissen gestartet:

- Push auf den Branch `main`
- Pull Request auf den Branch `main`

---

## Aufbau der Pipeline

Die Pipeline besteht aus zwei Jobs:

```text
Push / Pull Request
        |
        v
      test
        |
        | Tests erfolgreich
        v
   Build ZIP
        |
        v
 Upload Artifact
        |
        v
      deploy
        |
        v
 Download Artifact
        |
        v
 Production Environment
        |
        v
 GitHub Release
```

---

## Job 1: test

Der erste Job führt die Continuous-Integration-Schritte aus.

Er führt folgende Aktionen durch:

1. Repository mit `actions/checkout` laden
2. Python installieren
3. Abhängigkeiten aus `requirements.txt` installieren
4. Automatisierte Tests mit `pytest` ausführen
5. Build als ZIP-Datei erstellen
6. ZIP-Datei als GitHub Actions Artifact hochladen

Die erzeugte Datei heißt:

```text
rechner.zip
```

Wenn die Tests fehlschlagen, wird der nachfolgende Deploy-Job nicht ausgeführt.

---

## Artifact

Nach erfolgreichen Tests wird ein Build erstellt:

```text
rechner.zip
```

Das ZIP-Archiv enthält den Quellcode der Anwendung und wird mit `actions/upload-artifact` als Artifact gespeichert.

Der Deploy-Job lädt dasselbe Artifact anschließend mit `actions/download-artifact` herunter.

Dadurch wird das Build-Ergebnis zwischen den Jobs weitergegeben.

---

## Job 2: deploy

Der zweite Job ist für das Deployment verantwortlich.

Er ist vom erfolgreichen Test-Job abhängig:

```yaml
needs: test
```

Der Deploy-Job:

1. lädt das zuvor erzeugte Artifact herunter,
2. verwendet das Environment `production`,
3. verwendet das konfigurierte Secret `DEPLOY_TOKEN`,
4. wartet auf die Freigabe des Production-Deployments,
5. erstellt eine GitHub Release,
6. veröffentlicht `rechner.zip` als Release-Asset.

---

## Deployment-Bedingung

Das Deployment wird nur bei einem Push auf den Branch `main` ausgeführt.

Die Bedingung im Workflow lautet:

```yaml
if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

Bei einem Pull Request können die Tests ausgeführt werden, aber das Production-Deployment wird übersprungen.

---

## Environment

Für das Deployment wird das GitHub Environment

```text
production
```

verwendet.

Für dieses Environment wurde eine Deployment Protection Rule konfiguriert.

Das Production-Deployment benötigt eine Freigabe, bevor der Deploy-Job fortgesetzt werden kann.

Zusätzlich ist das Deployment auf den Branch `main` beschränkt.

---

## Secret

Für das Projekt wurde folgendes Secret konfiguriert:

```text
DEPLOY_TOKEN
```

Das Secret wird über GitHub Actions verwendet.

Der Wert des Secrets wird weder im Repository gespeichert noch in den Workflow-Logs ausgegeben.

Im Workflow wird lediglich geprüft, ob das Secret verfügbar ist.

---

## GitHub Release

Nach erfolgreichen Tests und der Freigabe des Production-Deployments erstellt die Pipeline automatisch eine GitHub Release.

Die Release wird mit GitHub CLI erstellt.

Beispiel:

```bash
gh release create
```

Die erzeugte Datei

```text
rechner.zip
```

wird als Release-Asset veröffentlicht.

---

## Verwendete Technologien

- Python
- pytest
- Git
- GitHub
- GitHub Actions
- YAML
- GitHub CLI
- CI/CD

---

## Zusammenfassung

Dieses Projekt demonstriert einen vollständigen einfachen CI/CD-Prozess:

```text
Code
  ↓
Git Push
  ↓
GitHub Actions
  ↓
Automatisierte Tests
  ↓
Build
  ↓
Artifact
  ↓
Production-Freigabe
  ↓
Deployment
  ↓
GitHub Release
```

Damit werden Tests, Build, Artifact-Weitergabe und Deployment automatisiert über GitHub Actions durchgeführt.