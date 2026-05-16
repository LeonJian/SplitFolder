# SplitFolder

<p align="center">
  <b>English</b> | <a href="#繁體中文">繁體中文</a> | <a href="#简体中文">简体中文</a> | <a href="#日本語">日本語</a> | <a href="#español">Español</a> | <a href="#deutsch">Deutsch</a>
</p>

---

Split photo files (RAW, HIF, XMP, etc.) within a folder into evenly distributed subfolders based on photo IDs. Supports SMB shares, dry-run preview, and re-splitting of existing partitions. Perfect for distributing large photo collections across multiple drives or network shares.

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
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SplitFolder.git
cd SplitFolder

# Or just download main.py
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/SplitFolder/main/main.py
```

## Usage

```bash
python3 main.py /path/to/source/folder -n 10
```

This splits all photo files in `/path/to/source/folder` into 10 subfolders: `part_001_*`, `part_002_*`, ..., `part_010_*`.

### Basic Examples

```bash
# Split into 5 parts with dry-run preview
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# Split into 20 parts with custom prefix
python3 main.py /Volumes/Media/DCIM -n 20 --prefix batch_

# Recursively scan all subdirectories
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# Re-split existing part folders (already detected by default)
python3 main.py /Volumes/Media/DCIM -n 40

# Skip empty folder cleanup
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### Command-line Options

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
2. **Group** — Groups files by their photo ID (e.g., `DSC00001.ARW` + `DSC00001.XMP` → group `DSC00001`)
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

Each folder name shows the range of photo IDs it contains, making it easy to identify contents at a glance.

---

## 繁體中文

# SplitFolder — 智能照片資料夾均分工具

將資料夾中的照片檔案（RAW、HIF、XMP 等）按照片編號均分到多個子資料夾。支援 SMB 網路共享、預覽模式、以及對已分資料夾的二次重分。適合將大量照片集合分散到多個硬碟或網路位置。

## 功能特點

- **照片感知分組** — 同一照片編號的不同副檔名（如 `DSC00001.ARW`、`DSC00001.HIF`、`DSC00001.XMP`）會保持在一起
- **自然排序** — `DSC2` 排在 `DSC10` 前面，而非字串字典序
- **均勻分配** — 照片組盡可能平均分佈到各個目標資料夾
- **預覽模式** — 使用 `--dry-run` 預覽結果，不實際移動檔案
- **支援重分** — 自動偵測已有的 `part_*` 資料夾，可重新分配其中的檔案
- **遞迴掃描** — 可選擇掃描整個目錄樹
- **SMB 安全** — 同檔案系統內使用 `os.rename` 快速移動，跨裝置時自動退回到複製+刪除
- **macOS 垃圾檔案過濾** — 自動跳過 `.DS_Store` 和 `._*` 檔案
- **重名保護** — 目標已存在同名檔案時，自動改名為 `xxx__dupN.ext`
- **空資料夾清理** — 重分完成後自動清理空的舊 `part_*` 資料夾

## 環境需求

- Python 3.7+

無需安裝任何外部依賴，僅使用標準庫。

## 安裝方式

```bash
# 克隆倉庫
git clone https://github.com/YOUR_USERNAME/SplitFolder.git
cd SplitFolder

# 或直接下載 main.py
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/SplitFolder/main/main.py
```

## 使用方式

```bash
python3 main.py /path/to/source/folder -n 10
```

將來源資料夾中的所有照片檔案均分到 10 個子資料夾：`part_001_*`、`part_002_*`……`part_010_*`。

### 常用範例

```bash
# 分成 5 份，先預覽不實際移動
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# 分成 20 份，使用自訂前綴
python3 main.py /Volumes/Media/DCIM -n 20 --prefix batch_

# 遞迴掃描所有子目錄
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# 重新分配已有的 part 資料夾（預設就會自動偵測）
python3 main.py /Volumes/Media/DCIM -n 40

# 不清理空的舊資料夾
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### 命令列參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `source` | *(必填)* | 來源資料夾路徑 |
| `-n, --parts` | *(必填)* | 目標子資料夾數量 |
| `--prefix` | `part_` | 輸出資料夾名稱前綴 |
| `--recursive` | 關 | 遞迴掃描整個目錄樹 |
| `--dry-run` | 關 | 僅預覽，不移動檔案 |
| `--no-clean-empty` | 關 | 跳過清理空的舊 `part_*` 資料夾 |

## 運作原理

1. **掃描** — 收集來源資料夾（及可選子目錄）中的所有檔案
2. **分組** — 按照片 ID 將檔案分組（如 `DSC00001.ARW` + `DSC00001.XMP` → 組 `DSC00001`）
3. **排序** — 使用自然數字排序
4. **分配** — 將照片組均勻分散到 N 個目標資料夾
5. **移動** — 將檔案移動到目標資料夾，保留原始檔名
6. **清理** — 移除已清空的舊 `part_*` 資料夾

### 資料夾命名規則

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

每個資料夾名稱顯示了其所包含的照片編號範圍，一目了然。

---

## 简体中文

# SplitFolder — 智能照片文件夹均分工具

将文件夹中的照片文件（RAW、HIF、XMP 等）按照片编号均分到多个子文件夹。支持 SMB 网络共享、预览模式、以及已分文件夹的二次重分。适合将大量照片集合分散到多个硬盘或网络位置。

## 功能特点

- **照片感知分组** — 同一照片编号的不同扩展名（如 `DSC00001.ARW`、`DSC00001.HIF`、`DSC00001.XMP`）会保持在一起
- **自然排序** — `DSC2` 排在 `DSC10` 前面，而非字符串字典序
- **均匀分配** — 照片组尽可能平均分布到各个目标文件夹
- **预览模式** — 使用 `--dry-run` 预览结果，不实际移动文件
- **支持重分** — 自动检测已有的 `part_*` 文件夹，可重新分配其中的文件
- **递归扫描** — 可选择扫描整个目录树
- **SMB 安全** — 同文件系统内使用 `os.rename` 快速移动，跨设备时自动退回到复制+删除
- **macOS 垃圾文件过滤** — 自动跳过 `.DS_Store` 和 `._*` 文件
- **重名保护** — 目标已存在同名文件时，自动改名为 `xxx__dupN.ext`
- **空文件夹清理** — 重分完成后自动清理空的旧 `part_*` 文件夹

## 环境需求

- Python 3.7+

无需安装任何外部依赖，仅使用标准库。

## 安装方式

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/SplitFolder.git
cd SplitFolder

# 或直接下载 main.py
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/SplitFolder/main/main.py
```

## 使用方式

```bash
python3 main.py /path/to/source/folder -n 10
```

将来源文件夹中的所有照片文件均分到 10 个子文件夹：`part_001_*`、`part_002_*`……`part_010_*`。

### 常用示例

```bash
# 分成 5 份，先预览不实际移动
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# 分成 20 份，使用自定义前缀
python3 main.py /Volumes/Media/DCIM -n 20 --prefix batch_

# 递归扫描所有子目录
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# 重新分配已有的 part 文件夹（默认就会自动检测）
python3 main.py /Volumes/Media/DCIM -n 40

# 不清理空的旧文件夹
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `source` | *(必填)* | 来源文件夹路径 |
| `-n, --parts` | *(必填)* | 目标子文件夹数量 |
| `--prefix` | `part_` | 输出文件夹名称前缀 |
| `--recursive` | 关 | 递归扫描整个目录树 |
| `--dry-run` | 关 | 仅预览，不移动文件 |
| `--no-clean-empty` | 关 | 跳过清理空的旧 `part_*` 文件夹 |

## 工作原理

1. **扫描** — 收集来源文件夹（及可选子目录）中的所有文件
2. **分组** — 按照片 ID 将文件分组（如 `DSC00001.ARW` + `DSC00001.XMP` → 组 `DSC00001`）
3. **排序** — 使用自然数字排序
4. **分配** — 将照片组均匀分散到 N 个目标文件夹
5. **移动** — 将文件移动到目标文件夹，保留原始文件名
6. **清理** — 移除已清空的旧 `part_*` 文件夹

### 文件夹命名规则

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

每个文件夹名称显示了其所包含的照片编号范围，一目了然。

---

## 日本語

# SplitFolder — スマート写真フォルダ分割ツール

フォルダ内の写真ファイル（RAW、HIF、XMP など）を写真番号に基づいて均等に複数のサブフォルダに分割します。SMB ネットワーク共有、ドライランプレビュー、既存パーティションの再分割をサポート。大量の写真コレクションを複数のドライブやネットワークに分散するのに最適です。

## 機能

- **写真認識グルーピング** — 同じ写真 ID の異なる拡張子（`DSC00001.ARW`、`DSC00001.HIF`、`DSC00001.XMP` など）を一緒に保持
- **自然ソート** — `DSC2` が `DSC10` より前にソートされます（文字列辞書順ではありません）
- **均等分配** — 写真グループを可能な限り均等に各フォルダに分散
- **ドライランモード** — `--dry-run` でファイルを移動せずに結果をプレビュー
- **再分割対応** — 既存の `part_*` フォルダを自動検出し、再分配が可能
- **再帰的スキャン** — ディレクトリ全体を再帰的にスキャン可能
- **SMB 対応** — 同一ファイルシステム内では `os.rename` で高速移動、異なるデバイス間ではコピー+削除にフォールバック
- **macOS ジャンクファイルフィルタ** — `.DS_Store` や `._*` ファイルを自動スキップ
- **重複保護** — ターゲットに同名ファイルが存在する場合、`xxx__dupN.ext` にリネーム
- **空フォルダクリーンアップ** — 再分配後に空の古い `part_*` フォルダを自動削除

## 要件

- Python 3.7+

外部依存なし — 標準ライブラリのみを使用。

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/SplitFolder.git
cd SplitFolder

# または main.py を直接ダウンロード
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/SplitFolder/main/main.py
```

## 使い方

```bash
python3 main.py /path/to/source/folder -n 10
```

ソースフォルダの全写真ファイルを 10 個のサブフォルダに分割：`part_001_*`、`part_002_*`……`part_010_*`。

### 使用例

```bash
# 5 分割、ドライランでプレビュー
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# 20 分割、カスタムプレフィックス
python3 main.py /Volumes/Media/DCIM -n 20 --prefix batch_

# 全サブディレクトリを再帰的にスキャン
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# 既存の part フォルダを再分割（デフォルトで自動検出）
python3 main.py /Volumes/Media/DCIM -n 40

# 空フォルダのクリーンアップをスキップ
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### コマンドラインオプション

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `source` | *(必須)* | ソースフォルダのパス |
| `-n, --parts` | *(必須)* | 分割先フォルダ数 |
| `--prefix` | `part_` | 出力フォルダ名の接頭辞 |
| `--recursive` | オフ | ディレクトリ全体を再帰的にスキャン |
| `--dry-run` | オフ | プレビューのみ — ファイルを移動しない |
| `--no-clean-empty` | オフ | 空の古い `part_*` フォルダのクリーンアップをスキップ |

## 動作の仕組み

1. **スキャン** — ソースフォルダ（およびオプションでサブディレクトリ）から全ファイルを収集
2. **グルーピング** — 写真 ID でファイルをグループ化（例：`DSC00001.ARW` + `DSC00001.XMP` → グループ `DSC00001`）
3. **ソート** — 自然数値順でソート
4. **分配** — 写真グループを N 個のフォルダに均等に分散
5. **移動** — ファイルをターゲットフォルダに移動し、ファイル名を保持
6. **クリーンアップ** — 空になった古い `part_*` フォルダを削除

### フォルダ命名規則

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

各フォルダ名には含まれる写真番号の範囲が表示され、内容を一目で識別できます。

---

## Español

# SplitFolder — Herramienta inteligente para dividir carpetas de fotos

Divide archivos de fotos (RAW, HIF, XMP, etc.) dentro de una carpeta en subcarpetas distribuidas uniformemente según los IDs de las fotos. Compatible con recursos compartidos SMB, modo de vista previa (dry-run) y redistribución de particiones existentes. Ideal para distribuir grandes colecciones de fotos en múltiples discos o ubicaciones de red.

## Características

- **Agrupación por foto** — Archivos con el mismo ID de foto (ej. `DSC00001.ARW`, `DSC00001.HIF`, `DSC00001.XMP`) se mantienen juntos
- **Ordenación natural** — `DSC2` va antes de `DSC10`, no lexicográficamente
- **Distribución uniforme** — Los grupos de fotos se distribuyen lo más equitativamente posible
- **Modo de vista previa** — Usa `--dry-run` para previsualizar sin mover archivos
- **Redistribución** — Las carpetas `part_*` existentes se detectan y pueden redistribuirse
- **Escaneo recursivo** — Opcionalmente, escanea todo el árbol de directorios
- **Compatible con SMB** — Usa `os.rename` en el mismo sistema de archivos, con respaldo de copia+eliminación entre dispositivos
- **Filtro de archivos basura de macOS** — Omite automáticamente `.DS_Store` y archivos `._*`
- **Protección contra duplicados** — Si un archivo ya existe, lo renombra a `xxx__dupN.ext`
- **Limpieza de carpetas vacías** — Elimina las carpetas `part_*` viejas y vacías

## Requisitos

- Python 3.7+

Sin dependencias externas — solo usa la biblioteca estándar.

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/YOUR_USERNAME/SplitFolder.git
cd SplitFolder

# O descargar solo main.py
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/SplitFolder/main/main.py
```

## Uso

```bash
python3 main.py /ruta/a/carpeta/origen -n 10
```

Divide todos los archivos de fotos en 10 subcarpetas: `part_001_*`, `part_002_*`, ..., `part_010_*`.

### Ejemplos básicos

```bash
# Dividir en 5 partes con vista previa
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# Dividir en 20 partes con prefijo personalizado
python3 main.py /Volumes/Media/DCIM -n 20 --prefix lote_

# Escanear recursivamente todos los subdirectorios
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# Redistribuir carpetas part existentes (detectado por defecto)
python3 main.py /Volumes/Media/DCIM -n 40

# Omitir limpieza de carpetas vacías
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### Opciones de línea de comandos

| Opción | Valor predeterminado | Descripción |
|--------|---------------------|-------------|
| `source` | *(obligatorio)* | Ruta a la carpeta de origen |
| `-n, --parts` | *(obligatorio)* | Número de subcarpetas de destino |
| `--prefix` | `part_` | Prefijo para los nombres de las carpetas |
| `--recursive` | desactivado | Escanea recursivamente todo el árbol de directorios |
| `--dry-run` | desactivado | Solo vista previa — no mueve archivos |
| `--no-clean-empty` | desactivado | Omite la limpieza de carpetas `part_*` vacías |

## Cómo funciona

1. **Escanear** — Recopila todos los archivos de la carpeta de origen (y subdirectorios opcionales)
2. **Agrupar** — Agrupa archivos por su ID de foto (ej. `DSC00001.ARW` + `DSC00001.XMP` → grupo `DSC00001`)
3. **Ordenar** — Ordena los grupos usando ordenación numérica natural
4. **Distribuir** — Distribuye uniformemente los grupos en N carpetas de destino
5. **Mover** — Mueve los archivos a sus carpetas de destino, conservando los nombres
6. **Limpiar** — Elimina las carpetas `part_*` vacías antiguas

### Convención de nombres de carpetas

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

Cada nombre de carpeta muestra el rango de IDs de fotos que contiene.

---

## Deutsch

# SplitFolder — Intelligentes Werkzeug zum Aufteilen von Foto-Ordnern

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
# Repository klonen
git clone https://github.com/YOUR_USERNAME/SplitFolder.git
cd SplitFolder

# Oder nur main.py herunterladen
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/SplitFolder/main/main.py
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

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with Python ❖ No dependencies ❖ Works on macOS, Linux, Windows</sub>
</p>
