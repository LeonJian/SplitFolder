#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import argparse
import math
import os
import re
import shutil


preview_count = 0


def is_macos_junk(path: Path) -> bool:
    name = path.name

    if name == ".DS_Store":
        return True

    if name.startswith("._"):
        return True

    return False


def is_part_folder(path: Path, prefix: str) -> bool:
    if not path.is_dir():
        return False

    pattern = rf"^{re.escape(prefix)}\d{{3}}_.*"
    return re.match(pattern, path.name) is not None


def extract_photo_id(stem: str) -> str:
    """
    将 DSC00001.ARW / DSC00001.HIF / DSC00001.XMP 归为 DSC00001。
    对普通文件则使用 stem 本身。
    """

    # 常见相机命名：DSC00001, C0001, IMG_0001, _DSC1234 等
    m = re.match(r"^([A-Za-z_]*\d+)", stem)

    if m:
        return m.group(1)

    return stem


def sort_photo_key(photo_id: str):
    """
    让 DSC2 排在 DSC10 前面，而不是纯字符串排序。
    """

    m = re.match(r"^(.*?)(\d+)$", photo_id)

    if not m:
        return (photo_id, -1)

    prefix = m.group(1)
    number = int(m.group(2))

    return (prefix, number)


def get_files(source: Path, recursive: bool, prefix: str):
    """
    扫描文件。

    规则：
    - 如果 recursive=False：
      只扫描 source 根目录下的文件；
      但如果发现已有 part_* 文件夹，会扫描这些 part_* 文件夹内部文件，
      用于支持二次重分。
    - 如果 recursive=True：
      扫描整个 source 树。
    """

    result = []
    skipped = 0

    def add_file(p: Path):
        nonlocal skipped

        try:
            if not p.is_file():
                return

            if is_macos_junk(p):
                skipped += 1
                return

            result.append(p)

        except (PermissionError, OSError):
            skipped += 1
            print(f"跳过无权限文件: {p}")

    if recursive:
        iterator = source.rglob("*")

        for p in iterator:
            add_file(p)

    else:
        # 1. 扫描根目录直接文件
        try:
            for p in source.iterdir():
                if p.is_file():
                    add_file(p)

        except (PermissionError, OSError) as e:
            print(f"扫描根目录失败: {e}")

        # 2. 扫描已有 part_* 文件夹，用于重分
        try:
            for folder in source.iterdir():
                if is_part_folder(folder, prefix):
                    for p in folder.rglob("*"):
                        add_file(p)

        except (PermissionError, OSError) as e:
            print(f"扫描已有 part 文件夹失败: {e}")

    return result, skipped


def safe_move(src: Path, dst: Path, dry_run: bool):
    global preview_count

    if dry_run:
        if preview_count < 10:
            print(f"[示例] {src.name} → {dst.parent.name}")
        elif preview_count == 10:
            print("...(省略其余文件)")
        preview_count += 1
        return

    try:
        # 同一个 SMB 共享 / 同一文件系统内，通常只是改目录项，不复制文件内容
        os.rename(src, dst)

    except OSError:
        # 跨设备时才会退化为复制 + 删除
        shutil.move(str(src), str(dst))


def make_unique_target(target: Path) -> Path:
    """
    避免覆盖已有文件。
    正常相机素材不应该重名。
    如果目标已存在，生成 xxx__dup1.ext。
    """

    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    parent = target.parent

    i = 1

    while True:
        candidate = parent / f"{stem}__dup{i}{suffix}"

        if not candidate.exists():
            return candidate

        i += 1


def cleanup_empty_part_folders(source: Path, prefix: str, dry_run: bool):
    """
    清理空的旧 part_* 文件夹。
    从深到浅删除。
    """

    candidates = []

    for p in source.rglob("*"):
        try:
            if is_part_folder(p, prefix):
                candidates.append(p)
        except (PermissionError, OSError):
            pass

    candidates.sort(key=lambda x: len(x.parts), reverse=True)

    removed = 0

    for folder in candidates:
        try:
            if any(folder.iterdir()):
                continue

            if dry_run:
                print(f"[DRY] 将删除空文件夹: {folder.name}")
            else:
                folder.rmdir()

            removed += 1

        except (PermissionError, OSError):
            pass

    return removed


def build_batches(photo_groups, parts: int, source: Path, prefix: str):
    total_groups = len(photo_groups)

    per_part = math.ceil(total_groups / parts)

    batches = []

    for i in range(parts):
        start = i * per_part
        end = min(start + per_part, total_groups)

        if start >= total_groups:
            break

        batch = photo_groups[start:end]

        first = batch[0][0]
        last = batch[-1][0]

        folder_name = f"{prefix}{i + 1:03d}_{first}-{last}"
        folder = source / folder_name

        batches.append(
            {
                "folder": folder,
                "batch": batch,
                "start": first,
                "end": last,
                "count_groups": len(batch),
                "count_files": sum(len(x[1]) for x in batch),
            }
        )

    return batches, per_part


def main():
    parser = argparse.ArgumentParser(
        description="将文件夹内文件按照片编号均分到多个文件夹，支持 SMB、dry-run、重复重分。"
    )

    parser.add_argument("source", help="源文件夹路径，例如 /Volumes/home/Media/DCIM")

    parser.add_argument(
        "-n", "--parts", type=int, required=True, help="目标份数，例如 10、20、40"
    )

    parser.add_argument("--prefix", default="part_", help="输出文件夹前缀，默认 part_")

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="递归扫描整个目录树。默认只扫描根目录文件和已有 part_* 文件夹。",
    )

    parser.add_argument("--dry-run", action="store_true", help="只预览，不移动文件")

    parser.add_argument(
        "--no-clean-empty", action="store_true", help="不清理空的旧 part_* 文件夹"
    )

    args = parser.parse_args()

    if args.parts <= 0:
        raise SystemExit("错误：份数必须大于 0")

    source = Path(args.source).expanduser().resolve()

    if not source.is_dir():
        raise SystemExit(f"错误：不是有效文件夹: {source}")

    print("扫描文件中...")

    files, skipped = get_files(
        source=source, recursive=args.recursive, prefix=args.prefix
    )

    if not files:
        raise SystemExit("没有找到可处理文件")

    groups = defaultdict(list)

    for file in files:
        photo_id = extract_photo_id(file.stem)
        groups[photo_id].append(file)

    photo_groups = sorted(groups.items(), key=lambda x: sort_photo_key(x[0]))

    total_groups = len(photo_groups)
    total_files = len(files)

    batches, per_part = build_batches(
        photo_groups=photo_groups, parts=args.parts, source=source, prefix=args.prefix
    )

    print()
    print(f"源文件夹: {source}")
    print(f"照片组数量: {total_groups}")
    print(f"文件总数: {total_files}")
    print(f"目标份数: {args.parts}")
    print(f"实际创建份数: {len(batches)}")
    print(f"每份约: {per_part} 组")
    print(f"跳过 macOS/无权限文件: {skipped}")
    print()

    print("将创建/使用以下文件夹:")

    for b in batches:
        print(f"{b['folder'].name} ({b['count_groups']} 组, {b['count_files']} 文件)")

    print()

    if args.dry_run:
        print("Dry-run 模式：不会移动文件，不会创建文件夹。")
    else:
        for b in batches:
            b["folder"].mkdir(exist_ok=True)

    print()
    print("处理中...")

    moved = 0
    unchanged = 0
    duplicated = 0
    failed = 0

    for b in batches:
        target_folder = b["folder"]

        for _, file_list in b["batch"]:
            file_list.sort(key=lambda p: p.name)

            for file in file_list:
                target = target_folder / file.name

                # 已经在正确文件夹里
                if file.parent == target_folder:
                    unchanged += 1
                    continue

                # 避免覆盖
                final_target = make_unique_target(target)

                if final_target != target:
                    duplicated += 1

                try:
                    safe_move(src=file, dst=final_target, dry_run=args.dry_run)

                    moved += 1

                except Exception as e:
                    failed += 1
                    print(f"失败: {file}")
                    print(e)

    print()

    removed_empty = 0

    if not args.no_clean_empty:
        print("清理空的旧 part_* 文件夹...")

        removed_empty = cleanup_empty_part_folders(
            source=source, prefix=args.prefix, dry_run=args.dry_run
        )

    print()

    if args.dry_run:
        print("预览完成")
    else:
        print("完成")

    print(f"移动文件数: {moved}")
    print(f"已在正确位置: {unchanged}")
    print(f"重名改名数: {duplicated}")
    print(f"失败数: {failed}")
    print(f"空旧文件夹清理数: {removed_empty}")


if __name__ == "__main__":
    main()
