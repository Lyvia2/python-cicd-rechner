# Abschluss-Challenge

In der fehlerhaften Pipeline wurden sechs Probleme gefunden.
Für jedes Problem werden Symptom bzw. Risiko, Ursache und Lösung dokumentiert.

---

## 1. Falsche Python-Version

### 🔴 Symptom / Risiko
`setup-python` verwendet die falsche Python-Version und der Workflow kann abbrechen.

### 🔎 Ursache
Die Python-Version wurde ohne Anführungszeichen angegeben:

`python-version: 3.10`

Dadurch kann YAML die Versionsnummer falsch interpretieren.

### ✅ Fix
Die Python-Version wird als String angegeben:

`python-version: "3.10"`

Alternativ kann eine Environment-Variable verwendet werden.

---

## 2. Pytest ist nicht verfügbar

### 🔴 Symptom / Risiko
Der Test-Step schlägt mit folgender Meldung fehl:

`pytest: command not found`

### 🔎 Ursache
Die Tests werden ausgeführt, bevor die Dependencies installiert wurden.

### ✅ Fix
Zuerst werden die Dependencies installiert:

`python -m pip install -r requirements.txt`

Danach werden die Tests gestartet:

`python -m pytest -v`

---

## 3. Falscher Name der requirements-Datei

### 🔴 Symptom / Risiko
Die Pipeline kann die Datei mit den Dependencies nicht finden:

`Could not open requirements file`

### 🔎 Ursache
Im Workflow steht:

`requirement.txt`

Die tatsächliche Datei heißt jedoch:

`requirements.txt`

### ✅ Fix
Im Workflow wird der korrekte Dateiname verwendet:

`python -m pip install -r requirements.txt`

---

## 4. Fehler im Build-Job

### 🔴 Symptom / Risiko
Der Build-Job findet den Ordner `src/` nicht.

Außerdem könnte der Build unabhängig davon starten, ob die Tests erfolgreich waren.

### 🔎 Ursache
Im Build-Job fehlt `actions/checkout@v4`.

Außerdem fehlt die Abhängigkeit vom Test-Job.

### ✅ Fix
Der Code wird zuerst mit

`actions/checkout@v4`

ausgecheckt.

Zusätzlich wird der Build mit

`needs: test`

von erfolgreichen Tests abhängig gemacht.

---

## 5. Unsicheres Deployment

### 🔴 Symptom / Risiko
Das Deployment kann bei einem Pull Request ausgeführt werden.

Außerdem wird das Secret direkt im Log ausgegeben.

### 🔎 Ursache
Es fehlen eine Bedingung für das Deployment und ein geschütztes Environment.

Das Secret wird direkt mit `echo` ausgegeben.

### ✅ Fix
Das Deployment wird von erfolgreichen Tests abhängig gemacht:

`needs: test`

Es wird nur auf dem Branch `main` ausgeführt:

`if: github.ref == 'refs/heads/main'`

Zusätzlich wird das geschützte Environment verwendet:

`environment: production`

Das Secret wird nur über eine Environment-Variable verwendet und sein Wert wird nicht ausgegeben.

---

## 6. Statischer Cache-Key

### 🔴 Symptom / Risiko
Der Pip-Cache wird bei Änderungen an den Dependencies nicht automatisch aktualisiert.

Dadurch können veraltete Dependencies aus dem Cache verwendet werden.

### 🔎 Ursache
Der Cache verwendet einen statischen Key:

`pip-cache`

Änderungen an `requirements.txt` beeinflussen diesen Key nicht.

### ✅ Fix
Der Cache-Key berücksichtigt das Betriebssystem und den Inhalt von `requirements.txt`:

`${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}`

Dadurch wird bei einer Änderung der Dependencies ein neuer Cache erzeugt.

---

## Ergebnis

Die sechs Probleme wurden analysiert und behoben.

Die korrigierte CI/CD-Pipeline führt die Tests aus, erstellt ein Build-Artefakt und führt das Deployment nur nach erfolgreichen Tests und der Freigabe des Production-Environments aus.