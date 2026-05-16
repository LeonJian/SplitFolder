# SplitFolder — Intelligentes Werkzeug zum Aufteilen von Foto-Ordnern

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a>
</p>

---

Teilt Fotodateien (RAW, HIF, XMP usw.) in einem Ordner basierend auf Foto-IDs in gleichmäßig verteilte Unterordner auf. Unterstützt SMB-Freigaben, Vorschau-Modus und erneutes Aufteilen bestehender Partitionen. Perfekt zum Verteilen großer Fotosammlungen auf mehrere Laufwerke oder Netzwerkspeicher.

## Funktionen

- **Foto-bewusste Gruppierung** — Dateien mit derselben Foto-ID (z.B. `DSC00001.ARW`, `DSC00001.HIF`, `DSC00001.XMP`) bleiben zusammen
- **Natürliche Sortierung** — `DSC2` kommt vor `DSC10`, nicht lexikografisch
- **Gleichmäßige Verteilung** — Fotogruppen werden möglichst gleichmäßig auf Zielordner verteilt
- **Vorschau-Modus** — Mit `--dry-run` das Ergebnis ohne Dateiverschiebung anzeigen
- **Erneutes Aufteilen** — Bestehende `part_*`-Ordner werden erkannt und können neu verteilt werden
- **Rekursives Scannen** — Optional den gesamten Verzeichnisbaum scannen
- **SMB-kompatibel** — Verwendet `os.rename` im selben Dateisystem, mit Kopieren+Löschen als Fallback
- **macOS-Junk-Filter** — Überspringt automatisch `.DS_Store`- und `._*`-Dateien
- **Duplikatschutz** — Falls ein Dateiname bereits existiert, wird er in `xxx__dupN.ext` umbenannt
- **Leere-Ordner-Bereinigung** — Entfernt leere alte `part_*`-Ordner nach der Neuverteilung

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
python3 main.py /pfad/zum/quellordner -n 10
```

Teilt alle Fotodateien im Quellordner in 10 Unterordner auf: `part_001_*`, `part_002_*`, …, `part_010_*`.

### Beispiele

```bash
# In 5 Teile aufteilen, mit Vorschau
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# In 20 Teile aufteilen, mit benutzerdefiniertem Präfix
python3 main.py /Volumes/Media/DCIM -n 20 --prefix batch_

# Rekursiv alle Unterverzeichnisse scannen
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# Bestehende part-Ordner neu aufteilen (standardmäßig erkannt)
python3 main.py /Volumes/Media/DCIM -n 40

# Bereinigung leerer Ordner überspringen
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
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
2. **Gruppieren** — Gruppiert Dateien nach Foto-ID (z.B. `DSC00001.ARW` + `DSC00001.XMP` → Gruppe `DSC00001`)
3. **Sortieren** — Sortiert Gruppen mit natürlicher numerischer Reihenfolge
4. **Verteilen** — Verteilt Fotogruppen gleichmäßig auf N Zielordner
5. **Verschieben** — Verschiebt Dateien in ihre Zielordner unter Beibehaltung der Dateinamen
6. **Bereinigen** — Entfernt geleerte alte `part_*`-Ordner

### Ordner-Benennungskonvention

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

Jeder Ordnername zeigt den enthaltenen Foto-ID-Bereich an — so sind die Inhalte auf einen Blick erkennbar.

## Lizenz

MIT License.
