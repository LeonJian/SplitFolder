# SplitFolder — 智能照片文件夹均分工具

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.de.md">Deutsch</a>
</p>

---

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
git clone https://github.com/LeonJian/SplitFolder.git
cd SplitFolder
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

## 授权

MIT License。
