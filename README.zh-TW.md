# SplitFolder — 智能照片資料夾均分工具

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.de.md">Deutsch</a>
</p>

---

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
git clone https://github.com/LeonJian/SplitFolder.git
cd SplitFolder
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

## 授權

MIT License。
