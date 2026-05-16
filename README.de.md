# SplitFolder — Werkzeug zum Aufteilen überfüllter Ordner

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a>
</p>

---

Teilt Dateien in überfüllten Ordnern mit zu vielen Dateien anhand des Dateinamens in gleichmäßig verteilte Unterordner auf — entwickelt, um das Problem zu lösen, dass Finder / Explorer bei zu großen Ordnern ewig laden. Funktioniert mit allen Dateitypen: Fotos, Dokumente, Archive, Logs, Datensätze und mehr. Unterstützt SMB-Freigaben, Vorschau-Modus und erneutes Aufteilen bestehender Partitionen.

## Funktionen

- **Namensbasierte Gruppierung** — Zusammengehörige Dateien mit gleichem Präfix+Nummer (z.B. `report_001.pdf`, `report_001.xlsx`) bleiben zusammen
- **Natürliche Sortierung** — `file2` kommt vor `file10`, nicht lexikografisch
- **Gleichmäßige Verteilung** — Dateigruppen werden möglichst gleichmäßig auf Zielordner verteilt
- **Vorschau-Modus** — Mit `--dry-run` das Ergebnis ohne Dateiverschiebung anzeigen
- **Erneutes Aufteilen** — Bestehende `part_*`-Ordner werden erkannt und können neu verteilt werden
- **Rekursives Scannen** — Optional den gesamten Verzeichnisbaum scannen
- **SMB-kompatibel** — Verwendet `os.rename` im selben Dateisystem, mit Kopieren+Löschen als Fallback
- **macOS-Junk-Filter** — Überspringt automatisch `.DS_Store`- und `._*`-Dateien
- **Duplikatschutz** — Falls ein Dateiname bereits existiert, wird er in `xxx__dupN.ext` umbenannt
- **Leere-Ordner-Bereinigung** — Entfernt leere alte `part_*`-Ordner nach der Neuverteilung

## Anwendungsfälle

- **Überfüllte Ordner** — Ein Ordner mit über 10.000 Dateien, der ewig zum Öffnen braucht? In kleinere Teile aufteilen.
- **Fotosammlungen** — RAW/ARW/HIF/XMP-Dateien auf mehrere Laufwerke oder Netzwerkspeicher verteilen.
- **Log-Archive** — Millionen von Logdateien nach Namensbereich partitionieren, um die Übersicht zu behalten.
- **Datensatz-Vorbereitung** — Trainingsdaten in ausgewogene Shards aufteilen.
- **Jeder große flache Ordner** — Wenn ein Ordner zu groß zum Laden ist, kann SplitFolder helfen.

## Voraussetzungen

- Python 3.7+

Keine externen Abhängigkeiten — verwendet nur die Standardbibliothek.

## Installation

```bash
git clone https://github.com/LeonJian/SplitFolder.git
cd SplitFolder
```

## Verwendung

```bash
python3 main.py /pfad/zum/großen/ordner -n 10
```

Teilt alle Dateien im Quellordner in 10 Unterordner auf: `part_001_*`, `part_002_*`, …, `part_010_*`.

### Beispiele

```bash
# In 5 Teile aufteilen, mit Vorschau
python3 main.py /Volumes/Data/Archive -n 5 --dry-run

# In 20 Teile aufteilen, mit benutzerdefiniertem Präfix
python3 main.py /Volumes/Data/Archive -n 20 --prefix batch_

# Rekursiv alle Unterverzeichnisse scannen
python3 main.py /Volumes/Data/Archive -n 10 --recursive

# Bestehende part-Ordner neu aufteilen (standardmäßig erkannt)
python3 main.py /Volumes/Data/Archive -n 40

# Bereinigung leerer Ordner überspringen
python3 main.py /Volumes/Data/Archive -n 10 --no-clean-empty
```

### Befehlszeilenoptionen

| Option | Standard | Beschreibung |
|--------|----------|--------------|
| `source` | *(erforderlich)* | Pfad zum Quellordner |
| `-n, --parts` | *(erforderlich)* | Anzahl der Ziel-Unterordner |
| `--prefix` | `part_` | Präfix für die Namen der Ausgabeordner |
| `--recursive` | aus | Gesamten Verzeichnisbaum rekursiv scannen |
| `--dry-run` | aus | Nur Vorschau — keine Dateien verschieben |
| `--no-clean-empty` | aus | Bereinigung leerer alter `part_*`-Ordner überspringen |

## Funktionsweise

1. **Scannen** — Sammelt alle Dateien aus dem Quellordner (und optional Unterverzeichnissen)
2. **Gruppieren** — Gruppiert Dateien nach Präfix+Nummer (z.B. `report_001.pdf` + `report_001.xlsx` → Gruppe `report_001`)
3. **Sortieren** — Sortiert Gruppen mit natürlicher numerischer Reihenfolge
4. **Verteilen** — Verteilt Dateigruppen gleichmäßig auf N Zielordner
5. **Verschieben** — Verschiebt Dateien in ihre Zielordner unter Beibehaltung der Dateinamen
6. **Bereinigen** — Entfernt geleerte alte `part_*`-Ordner

### Ordner-Benennungskonvention

```
part_001_report_0001-report_0500/
part_002_report_0501-report_1000/
part_003_report_1001-report_1500/
...
```

Jeder Ordnername zeigt den enthaltenen Dateigruppen-Bereich an.

## Lizenz

[Apache License 2.0](LICENSE)
