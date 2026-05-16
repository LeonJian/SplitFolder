# SplitFolder

<p align="center">
  <a href="README.zh-TW.md">繁體中文</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.de.md">Deutsch</a>
</p>

---

Intelligently split photo files (RAW, HIF, XMP, etc.) within a folder into evenly distributed subfolders based on photo IDs. Supports SMB shares, dry-run preview, and re-splitting of existing partitions. Perfect for distributing large photo collections across multiple drives or network shares.

## Features

- **Photo-aware grouping** — Files sharing the same photo ID (e.g., `DSC00001.ARW`, `DSC00001.HIF`, `DSC00001.XMP`) stay together
- **Natural sort** — `DSC2` sorts before `DSC10`, not lexicographically
- **Even distribution** — Photo groups are spread as evenly as possible across target folders
- **Dry-run mode** — Preview the result without moving any files
- **Re-splitting** — Already-split `part_*` folders are detected and can be re-distributed
- **Recursive scanning** — Optionally scan the entire directory tree
- **SMB / network share safe** — Uses `os.rename` for same-filesystem moves, falling back to copy+delete
- **macOS junk filtering** — Automatically skips `.DS_Store` and `._*` files
- **Duplicate protection** — If a filename already exists in the target, renames to `xxx__dupN.ext`
- **Empty folder cleanup** — Removes empty old `part_*` folders after redistribution

## Requirements

- Python 3.7+

No external dependencies — uses only the standard library.

## Installation

```bash
git clone https://github.com/LeonJian/SplitFolder.git
cd SplitFolder
```

## Usage

```bash
python3 main.py /path/to/source/folder -n 10
```

Splits all photo files into 10 subfolders: `part_001_*`, `part_002_*`, ..., `part_010_*`.

### Examples

```bash
# Split into 5 parts with dry-run preview
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# Split into 20 parts with custom prefix
python3 main.py /Volumes/Media/DCIM -n 20 --prefix batch_

# Recursively scan all subdirectories
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# Re-split existing part folders (detected by default)
python3 main.py /Volumes/Media/DCIM -n 40

# Skip empty folder cleanup
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `source` | *(required)* | Path to the source folder |
| `-n, --parts` | *(required)* | Number of target subfolders |
| `--prefix` | `part_` | Prefix for output folder names |
| `--recursive` | off | Recursively scan the entire directory tree |
| `--dry-run` | off | Preview only — do not move files |
| `--no-clean-empty` | off | Skip cleaning empty old `part_*` folders |

## How It Works

1. **Scan** — Collects all files from the source folder (and optionally subdirectories)
2. **Group** — Groups files by photo ID (e.g., `DSC00001.ARW` + `DSC00001.XMP` → group `DSC00001`)
3. **Sort** — Sorts groups using natural number ordering
4. **Distribute** — Evenly spreads groups across N target folders
5. **Move** — Moves files into their target folders, preserving filenames
6. **Cleanup** — Removes empty old `part_*` folders

### Folder Naming Convention

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

Each folder name shows the range of photo IDs it contains.

## License

MIT License.
