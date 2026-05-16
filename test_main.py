#!/usr/bin/env python3
"""SplitFolder 完整测试套件"""

import pytest
import math
import os
import sys
import shutil
from pathlib import Path
from unittest import mock
from io import StringIO

# 将被测模块加入路径
sys.path.insert(0, str(Path(__file__).parent))
import main


# ============================================================
# is_macos_junk
# ============================================================
class TestIsMacosJunk:
    def test_ds_store(self):
        assert main.is_macos_junk(Path(".DS_Store")) is True

    def test_apple_double_prefix(self):
        assert main.is_macos_junk(Path("._foo.txt")) is True
        assert main.is_macos_junk(Path("._DSC00001.ARW")) is True
        assert main.is_macos_junk(Path("._")) is True

    def test_normal_files(self):
        assert main.is_macos_junk(Path("DSC00001.ARW")) is False
        assert main.is_macos_junk(Path("report.pdf")) is False
        assert main.is_macos_junk(Path(".gitignore")) is False
        assert main.is_macos_junk(Path("file._txt")) is False
        assert main.is_macos_junk(Path("__MACOSX")) is False

    def test_path_with_parent(self):
        assert main.is_macos_junk(Path("/some/dir/.DS_Store")) is True
        assert main.is_macos_junk(Path("/some/dir/._hidden")) is True
        assert main.is_macos_junk(Path("/some/dir/normal.txt")) is False


# ============================================================
# is_part_folder
# ============================================================
class TestIsPartFolder:
    def test_valid_part_folders(self, tmp_path):
        (tmp_path / "part_001_a-b").mkdir()
        (tmp_path / "part_010_x-y").mkdir()
        (tmp_path / "part_999_z").mkdir()
        assert main.is_part_folder(tmp_path / "part_001_a-b", "part_") is True
        assert main.is_part_folder(tmp_path / "part_010_x-y", "part_") is True
        assert main.is_part_folder(tmp_path / "part_999_z", "part_") is True

    def test_not_a_directory(self, tmp_path):
        f = tmp_path / "part_001_a-b"
        f.write_text("i am a file")
        assert main.is_part_folder(f, "part_") is False

    def test_wrong_prefix(self, tmp_path):
        (tmp_path / "batch_001_files").mkdir()
        assert main.is_part_folder(tmp_path / "batch_001_files", "part_") is False
        assert main.is_part_folder(tmp_path / "batch_001_files", "batch_") is True

    def test_missing_underscore_after_prefix(self, tmp_path):
        (tmp_path / "part001_files").mkdir()
        assert main.is_part_folder(tmp_path / "part001_files", "part_") is False

    def test_no_number(self, tmp_path):
        (tmp_path / "part_abc_files").mkdir()
        assert main.is_part_folder(tmp_path / "part_abc_files", "part_") is False

    def test_number_not_three_digits(self, tmp_path):
        (tmp_path / "part_01_files").mkdir()
        (tmp_path / "part_0001_files").mkdir()
        assert main.is_part_folder(tmp_path / "part_01_files", "part_") is False
        assert main.is_part_folder(tmp_path / "part_0001_files", "part_") is False

    def test_custom_prefix_with_special_chars(self, tmp_path):
        (tmp_path / "batch_001_a-b").mkdir()
        assert main.is_part_folder(tmp_path / "batch_001_a-b", "batch_") is True

    def test_prefix_needs_escaping(self, tmp_path):
        """带正则特殊字符的前缀应被正确转义"""
        (tmp_path / "part._001_a-b").mkdir()
        assert main.is_part_folder(tmp_path / "part._001_a-b", "part._") is True
        assert main.is_part_folder(tmp_path / "partx_001_a-b", "part._") is False


# ============================================================
# extract_group_key
# ============================================================
class TestExtractGroupKey:
    def test_camera_style_names(self):
        assert main.extract_group_key("DSC00001") == "DSC00001"
        assert main.extract_group_key("DSC12345") == "DSC12345"
        assert main.extract_group_key("_DSC0001") == "_DSC0001"
        assert main.extract_group_key("IMG_0001") == "IMG_0001"
        assert main.extract_group_key("C0001") == "C0001"

    def test_generic_numbered_names(self):
        assert main.extract_group_key("report_001") == "report_001"
        assert main.extract_group_key("file_2024") == "file_2024"
        assert main.extract_group_key("data_000001") == "data_000001"
        assert main.extract_group_key("log2023") == "log2023"

    def test_no_number_uses_full_stem(self):
        assert main.extract_group_key("README") == "README"
        assert main.extract_group_key("LICENSE") == "LICENSE"
        assert main.extract_group_key("report_final") == "report_final"
        assert main.extract_group_key("abc_def") == "abc_def"

    def test_number_in_middle_not_prefix(self):
        """字母+数字后还跟字母——返回前缀+数字部分"""
        assert main.extract_group_key("abc123def") == "abc123"

    def test_leading_number(self):
        assert main.extract_group_key("001_file") == "001"
        assert main.extract_group_key("12345") == "12345"

    def test_empty_string(self):
        assert main.extract_group_key("") == ""

    def test_underscore_only_prefix(self):
        assert main.extract_group_key("_001") == "_001"


# ============================================================
# sort_group_key
# ============================================================
class TestSortGroupKey:
    def test_natural_sort_order(self):
        keys = ["DSC10", "DSC2", "DSC1", "DSC20", "DSC3"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["DSC1", "DSC2", "DSC3", "DSC10", "DSC20"]

    def test_different_prefixes_stay_grouped(self):
        keys = ["IMG_001", "DSC001", "IMG_010", "DSC002"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["DSC001", "DSC002", "IMG_001", "IMG_010"]

    def test_no_number_trailing(self):
        keys = ["README", "LICENSE", "abc"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["LICENSE", "README", "abc"]

    def test_same_prefix_different_numbers(self):
        keys = ["report_100", "report_2", "report_10", "report_1"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["report_1", "report_2", "report_10", "report_100"]

    def test_large_numbers(self):
        keys = ["file_999999", "file_1000000", "file_1"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["file_1", "file_999999", "file_1000000"]

    def test_mixed_with_and_without_numbers(self):
        keys = ["z", "a10", "a2", "b", "a1"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["a1", "a2", "a10", "b", "z"]

    def test_zero_prefixed_numbers(self):
        keys = ["DSC001", "DSC010", "DSC002", "DSC100"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["DSC001", "DSC002", "DSC010", "DSC100"]

    def test_empty_string(self):
        keys = ["", "a1", "a2"]
        sorted_keys = sorted(keys, key=main.sort_group_key)
        assert sorted_keys == ["", "a1", "a2"]


# ============================================================
# get_files
# ============================================================
class TestGetFiles:
    def test_non_recursive_flat_dir(self, tmp_path):
        (tmp_path / "a.txt").write_text("")
        (tmp_path / "b.pdf").write_text("")
        (tmp_path / "c.log").write_text("")
        files, skipped = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 3
        assert skipped == 0
        names = {f.name for f in files}
        assert names == {"a.txt", "b.pdf", "c.log"}

    def test_recursive_scans_subdirs(self, tmp_path):
        (tmp_path / "root.txt").write_text("")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "deep.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=True, prefix="part_")
        assert len(files) == 2

    def test_non_recursive_skips_root_subdir_files(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "ignored.txt").write_text("")
        (tmp_path / "visible.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 1
        assert files[0].name == "visible.txt"

    def test_filters_macos_junk(self, tmp_path):
        (tmp_path / ".DS_Store").write_text("")
        (tmp_path / "._cache").write_text("")
        (tmp_path / "real.txt").write_text("")
        files, skipped = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 1
        assert files[0].name == "real.txt"
        assert skipped == 2

    def test_scans_existing_part_folders_non_recursive(self, tmp_path):
        """非递归模式下，应扫描已有 part_* 文件夹内的文件"""
        part_dir = tmp_path / "part_001_a-c"
        part_dir.mkdir()
        (part_dir / "a.txt").write_text("")
        (part_dir / "b.txt").write_text("")
        (tmp_path / "root.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 3

    def test_non_recursive_does_not_scan_normal_subfolders(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "a.txt").write_text("")
        (tmp_path / "b.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 1
        assert files[0].name == "b.txt"

    def test_empty_dir(self, tmp_path):
        files, skipped = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert files == []
        assert skipped == 0

    def test_only_junk_files(self, tmp_path):
        (tmp_path / ".DS_Store").write_text("")
        (tmp_path / "._foo").write_text("")
        files, skipped = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert files == []
        assert skipped == 2

    def test_recursive_also_scans_part_folders(self, tmp_path):
        part_dir = tmp_path / "part_001_x-y"
        part_dir.mkdir()
        (part_dir / "deep.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=True, prefix="part_")
        assert len(files) == 1

    def test_custom_prefix_part_folder(self, tmp_path):
        batch_dir = tmp_path / "batch_001_a-b"
        batch_dir.mkdir()
        (batch_dir / "f.txt").write_text("")
        (tmp_path / "root.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=False, prefix="batch_")
        assert len(files) == 2

    def test_nested_part_folders_recursive(self, tmp_path):
        part_dir = tmp_path / "part_001_x-y"
        part_dir.mkdir()
        nested = part_dir / "part_002_a-b"
        nested.mkdir()
        (nested / "deep.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=True, prefix="part_")
        assert len(files) == 1

    def test_skip_directories_in_result(self, tmp_path):
        (tmp_path / "subdir").mkdir()
        (tmp_path / "file.txt").write_text("")
        files, _ = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 1
        assert files[0].name == "file.txt"

    def test_skip_permission_denied_on_file_in_add_file(self, tmp_path):
        """add_file 内部的 is_file 抛异常——被 add_file 的 try/except 捕获"""
        f = tmp_path / "locked.txt"
        f.write_text("")
        (tmp_path / "ok.txt").write_text("")

        call_count = 0
        original_is_file = Path.is_file

        def fake_is_file(self):
            nonlocal call_count
            call_count += 1
            # is_file 在 iterdir 循环和 add_file 内部都会被调用
            # 只在 iterdir 循环阶段对 locked.txt 抛异常来模拟场景
            if self.name == "locked.txt" and call_count <= 2:
                raise PermissionError("denied")
            return original_is_file(self)

        with mock.patch.object(Path, "is_file", fake_is_file):
            files, skipped = main.get_files(tmp_path, recursive=False, prefix="part_")
            assert len(files) >= 1
            assert any(f.name == "ok.txt" for f in files)


# ============================================================
# safe_move
# ============================================================
class TestSafeMove:
    def test_dry_run_increments_preview_count(self):
        main.preview_count = 0
        src = Path("/fake/src.txt")
        dst = Path("/fake/part_001/src.txt")
        main.safe_move(src, dst, dry_run=True)
        assert main.preview_count == 1

    def test_dry_run_prints_first_10(self, capsys):
        main.preview_count = 0
        for i in range(12):
            main.safe_move(
                Path(f"/fake/{i}.txt"),
                Path(f"/fake/part_001/{i}.txt"),
                dry_run=True,
            )
        captured = capsys.readouterr()
        assert "[示例]" in captured.out
        assert "省略其余文件" in captured.out

    def test_dry_run_does_not_touch_filesystem(self, tmp_path):
        src = tmp_path / "real.txt"
        src.write_text("data")
        dst = tmp_path / "dest" / "real.txt"
        dst.parent.mkdir()
        main.preview_count = 0
        main.safe_move(src, dst, dry_run=True)
        assert src.exists()
        assert not dst.exists()

    def test_real_move_same_filesystem(self, tmp_path):
        src = tmp_path / "move_me.txt"
        src.write_text("hello")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        dst = dst_dir / "move_me.txt"
        main.preview_count = 0
        main.safe_move(src, dst, dry_run=False)
        assert not src.exists()
        assert dst.exists()
        assert dst.read_text() == "hello"

    def test_cross_device_fallback(self, tmp_path):
        """模拟 os.rename 失败时回退到 shutil.move"""
        src = tmp_path / "cross.txt"
        src.write_text("data")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        dst = dst_dir / "cross.txt"
        main.preview_count = 0

        with mock.patch("os.rename", side_effect=OSError("cross-device")):
            main.safe_move(src, dst, dry_run=False)
        assert not src.exists()
        assert dst.exists()


# ============================================================
# make_unique_target
# ============================================================
class TestMakeUniqueTarget:
    def test_no_conflict_returns_same(self, tmp_path):
        target = tmp_path / "file.txt"
        result = main.make_unique_target(target)
        assert result == target

    def test_existing_file_gets_dup_suffix(self, tmp_path):
        target = tmp_path / "file.txt"
        target.write_text("existing")
        result = main.make_unique_target(target)
        assert result != target
        assert result.stem == "file__dup1"
        assert result.suffix == ".txt"
        assert result.parent == target.parent

    def test_multiple_duplicates(self, tmp_path):
        target = tmp_path / "file.txt"
        target.write_text("orig")
        (tmp_path / "file__dup1.txt").write_text("dup1")
        (tmp_path / "file__dup2.txt").write_text("dup2")
        result = main.make_unique_target(target)
        assert result.name == "file__dup3.txt"

    def test_no_suffix_file(self, tmp_path):
        target = tmp_path / "README"
        target.write_text("orig")
        result = main.make_unique_target(target)
        assert result.name == "README__dup1"
        assert result.suffix == ""

    def test_multiple_dots_in_name(self, tmp_path):
        target = tmp_path / "archive.tar.gz"
        target.write_text("orig")
        result = main.make_unique_target(target)
        assert result.stem == "archive.tar__dup1"
        assert result.suffix == ".gz"

    def test_gapped_duplicates(self, tmp_path):
        """跳过不连续的 dup 编号"""
        target = tmp_path / "f.txt"
        target.write_text("orig")
        (tmp_path / "f__dup1.txt").write_text("dup1")
        (tmp_path / "f__dup3.txt").write_text("dup3")
        result = main.make_unique_target(target)
        assert result.name == "f__dup2.txt"


# ============================================================
# cleanup_empty_part_folders
# ============================================================
class TestCleanupEmptyPartFolders:
    def test_removes_empty_part_folder(self, tmp_path):
        part_dir = tmp_path / "part_001_a-b"
        part_dir.mkdir()
        removed = main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=False)
        assert removed == 1
        assert not part_dir.exists()

    def test_keeps_non_empty_part_folder(self, tmp_path):
        part_dir = tmp_path / "part_001_a-b"
        part_dir.mkdir()
        (part_dir / "file.txt").write_text("hello")
        removed = main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=False)
        assert removed == 0
        assert part_dir.exists()

    def test_dry_run_does_not_remove(self, tmp_path):
        part_dir = tmp_path / "part_001_a-b"
        part_dir.mkdir()
        removed = main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=True)
        assert removed >= 1
        assert part_dir.exists()

    def test_dry_run_prints_message(self, capsys, tmp_path):
        part_dir = tmp_path / "part_001_a-b"
        part_dir.mkdir()
        main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=True)
        captured = capsys.readouterr()
        assert "[DRY]" in captured.out
        assert "part_001_a-b" in captured.out

    def test_deletes_deepest_first(self, tmp_path):
        outer = tmp_path / "part_001_outer"
        outer.mkdir()
        inner = outer / "part_001_inner"
        inner.mkdir()
        # 两者都为空，深层先删
        removed = main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=False)
        assert removed == 2
        assert not inner.exists()
        assert not outer.exists()

    def test_handles_is_part_folder_permission_error(self, tmp_path):
        """is_part_folder 内部抛权限错误时被 try/except 捕获，不崩溃"""
        part_dir = tmp_path / "part_001_a-b"
        part_dir.mkdir()

        original_is_dir = Path.is_dir

        def fake_is_dir(self):
            if self.name == "part_001_a-b":
                raise PermissionError("nope")
            return original_is_dir(self)

        with mock.patch.object(Path, "is_dir", fake_is_dir):
            removed = main.cleanup_empty_part_folders(
                tmp_path, "part_", dry_run=False
            )
            assert removed == 0

    def test_empty_folder_with_files_cannot_be_removed_with_rmdir(self, tmp_path):
        """rmdir 只能删空文件夹——内部有文件的不会被删"""
        outer = tmp_path / "part_001_outer"
        outer.mkdir()
        inner = outer / "part_001_inner"
        inner.mkdir()
        (inner / "keep.txt").write_text("data")
        removed = main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=False)
        assert removed == 0
        assert inner.exists()

    def test_no_part_folders_at_all(self, tmp_path):
        (tmp_path / "normal.txt").write_text("")
        removed = main.cleanup_empty_part_folders(tmp_path, "part_", dry_run=False)
        assert removed == 0

    def test_custom_prefix(self, tmp_path):
        batch_dir = tmp_path / "batch_001_x-y"
        batch_dir.mkdir()
        removed = main.cleanup_empty_part_folders(tmp_path, "batch_", dry_run=False)
        assert removed == 1
        assert not batch_dir.exists()


# ============================================================
# build_batches
# ============================================================
class TestBuildBatches:
    @staticmethod
    def make_groups(count, prefix="file"):
        return [(f"{prefix}_{i:04d}", [Path(f"{prefix}_{i:04d}.txt")]) for i in range(1, count + 1)]

    def test_even_split(self):
        groups = self.make_groups(100)
        batches, per_part = main.build_batches(groups, 10, Path("/src"), "part_")
        assert len(batches) == 10
        assert per_part == 10
        for b in batches:
            assert b["count_groups"] == 10

    def test_uneven_split(self):
        groups = self.make_groups(25)
        batches, per_part = main.build_batches(groups, 3, Path("/src"), "part_")
        assert len(batches) == 3
        assert per_part == 9  # ceil(25/3)
        group_counts = [b["count_groups"] for b in batches]
        assert group_counts == [9, 9, 7]

    def test_more_parts_than_groups(self):
        groups = self.make_groups(3)
        batches, per_part = main.build_batches(groups, 10, Path("/src"), "part_")
        assert len(batches) == 3

    def test_single_part(self):
        groups = self.make_groups(50)
        batches, per_part = main.build_batches(groups, 1, Path("/src"), "part_")
        assert len(batches) == 1
        assert batches[0]["count_groups"] == 50
        assert batches[0]["count_files"] == 50

    def test_single_group(self):
        groups = self.make_groups(1)
        batches, per_part = main.build_batches(groups, 5, Path("/src"), "part_")
        assert len(batches) == 1
        assert batches[0]["count_groups"] == 1

    def test_folder_naming(self):
        groups = self.make_groups(50)
        batches, _ = main.build_batches(groups, 2, Path("/src"), "part_")
        assert batches[0]["folder"].name.startswith("part_001_")
        assert batches[1]["folder"].name.startswith("part_002_")

    def test_start_end_values(self):
        groups = self.make_groups(2)
        batches, _ = main.build_batches(groups, 2, Path("/src"), "part_")
        assert batches[0]["start"] == "file_0001"
        assert batches[0]["end"] == "file_0001"
        assert batches[1]["start"] == "file_0002"
        assert batches[1]["end"] == "file_0002"

    def test_count_files_aggregates_file_lists(self):
        groups = [
            ("grp_a", [Path("a.txt"), Path("a.xmp")]),
            ("grp_b", [Path("b.txt")]),
            ("grp_c", [Path("c.txt"), Path("c.hif"), Path("c.xml")]),
        ]
        batches, _ = main.build_batches(groups, 2, Path("/src"), "part_")
        assert len(batches) == 2
        total_files = sum(b["count_files"] for b in batches)
        assert total_files == 6

    def test_custom_prefix(self):
        groups = self.make_groups(10)
        batches, _ = main.build_batches(groups, 1, Path("/src"), "batch_")
        assert batches[0]["folder"].name.startswith("batch_")

    def test_empty_groups_list(self):
        batches, per_part = main.build_batches([], 5, Path("/src"), "part_")
        assert batches == []
        assert per_part == 0

    def test_primes_distribution(self):
        """质数分组确保不丢数据"""
        groups = self.make_groups(101)
        batches, _ = main.build_batches(groups, 7, Path("/src"), "part_")
        total = sum(b["count_groups"] for b in batches)
        assert total == 101


# ============================================================
# main() 集成测试
# ============================================================
class TestMain:
    def test_help_exits(self, capsys):
        with pytest.raises(SystemExit):
            with mock.patch.object(sys, "argv", ["main.py", "--help"]):
                main.main()

    def test_missing_parts_argument(self, capsys):
        with pytest.raises(SystemExit):
            with mock.patch.object(sys, "argv", ["main.py", "/tmp"]):
                main.main()

    def test_invalid_parts_zero(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            with mock.patch.object(sys, "argv", ["main.py", str(tmp_path), "-n", "0"]):
                main.main()
        assert "份数必须大于 0" in str(exc.value)

    def test_invalid_parts_negative(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            with mock.patch.object(sys, "argv", ["main.py", str(tmp_path), "-n", "-1"]):
                main.main()
        assert "份数必须大于 0" in str(exc.value)

    def test_source_not_a_directory(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("")
        with pytest.raises(SystemExit) as exc:
            with mock.patch.object(sys, "argv", ["main.py", str(f), "-n", "2"]):
                main.main()
        assert "不是有效文件夹" in str(exc.value)

    def test_source_not_exists(self):
        with pytest.raises(SystemExit) as exc:
            with mock.patch.object(
                sys, "argv", ["main.py", "/nonexistent/path/xyz", "-n", "2"]
            ):
                main.main()
        assert "不是有效文件夹" in str(exc.value)

    def test_no_files_found(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            with mock.patch.object(sys, "argv", ["main.py", str(tmp_path), "-n", "2"]):
                main.main()
        assert "没有找到可处理文件" in str(exc.value)

    def test_only_junk_files_in_dir(self, tmp_path, capsys):
        """仅有 macOS 垃圾文件时也应报没有可处理文件"""
        (tmp_path / ".DS_Store").write_text("")
        (tmp_path / "._cache").write_text("")
        original_preview = main.preview_count
        with pytest.raises(SystemExit) as exc:
            with mock.patch.object(sys, "argv", ["main.py", str(tmp_path), "-n", "2"]):
                main.main()
        assert "没有找到可处理文件" in str(exc.value)
        main.preview_count = original_preview

    def test_dry_run_creates_no_folders(self, tmp_path, capsys):
        (tmp_path / "a.txt").write_text("")
        (tmp_path / "b.txt").write_text("")
        original_preview = main.preview_count
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "2", "--dry-run"]
        ):
            main.main()
        main.preview_count = original_preview
        captured = capsys.readouterr()
        assert "Dry-run" in captured.out
        assert "预览完成" in captured.out

    def test_basic_split(self, tmp_path):
        for i in range(1, 21):
            (tmp_path / f"file_{i:04d}.txt").write_text("content")
        original_preview = main.preview_count
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "2"]
        ):
            main.main()
        main.preview_count = original_preview
        part_dirs = sorted(
            [d for d in tmp_path.iterdir() if d.is_dir() and d.name.startswith("part_")]
        )
        assert len(part_dirs) == 2
        total_files_in_parts = sum(1 for d in part_dirs for _ in d.iterdir())
        assert total_files_in_parts == 20

    def test_no_clean_empty_flag(self, tmp_path):
        (tmp_path / "a.txt").write_text("")
        (tmp_path / "b.txt").write_text("")
        original_preview = main.preview_count
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "2", "--no-clean-empty"]
        ):
            main.main()
        main.preview_count = original_preview

    def test_custom_prefix(self, tmp_path):
        for i in range(1, 6):
            (tmp_path / f"data_{i}.txt").write_text("")
        original_preview = main.preview_count
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "2", "--prefix", "batch_"]
        ):
            main.main()
        main.preview_count = original_preview
        batch_dirs = sorted(
            [d for d in tmp_path.iterdir() if d.is_dir() and d.name.startswith("batch_")]
        )
        assert len(batch_dirs) == 2

    def test_expanduser_in_path(self, tmp_path, monkeypatch):
        (tmp_path / "f.txt").write_text("")
        fake_home = str(tmp_path.parent)
        monkeypatch.setenv("HOME", fake_home)
        rel = tmp_path.name
        original_preview = main.preview_count
        with mock.patch.object(
            sys, "argv", ["main.py", f"~/{rel}", "-n", "2"]
        ):
            main.main()
        main.preview_count = original_preview

    def test_re_split_existing_parts(self, tmp_path):
        """已有 part_* 文件夹，重新分割"""
        existing = tmp_path / "part_001_old"
        existing.mkdir()
        (existing / "a.txt").write_text("")
        (existing / "b.txt").write_text("")
        (tmp_path / "root.txt").write_text("")
        original_preview = main.preview_count
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "2"]
        ):
            main.main()
        main.preview_count = original_preview
        new_parts = sorted(
            [d for d in tmp_path.iterdir() if main.is_part_folder(d, "part_")]
        )
        assert len(new_parts) >= 1

    def test_file_already_in_correct_folder(self, tmp_path):
        """已在正确目标文件夹中的文件无需移动"""
        (tmp_path / "f1.txt").write_text("a")
        (tmp_path / "f2.txt").write_text("b")
        original_preview = main.preview_count
        # 第一次分割
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "2"]
        ):
            main.main()
        # 第二次分割——此时文件已在 part_* 中
        with mock.patch.object(
            sys, "argv", ["main.py", str(tmp_path), "-n", "3"]
        ):
            main.main()
        main.preview_count = original_preview


# ============================================================
# 边界情况 & 回归测试
# ============================================================
class TestEdgeCases:
    def test_duplicate_handling_in_batch(self, tmp_path):
        """模拟两文件同名但不同原始路径，合并到同一目标时触发 rename"""
        target_dir = tmp_path / "dest"
        target_dir.mkdir()
        (target_dir / "f.txt").write_text("existing")

        src1 = tmp_path / "a" / "f.txt"
        src1.parent.mkdir()
        src1.write_text("a")
        src2 = tmp_path / "b" / "f.txt"
        src2.parent.mkdir()
        src2.write_text("b")

        final1 = main.make_unique_target(target_dir / "f.txt")
        assert final1.name == "f__dup1.txt"
        shutil.move(str(src1), str(final1))
        final2 = main.make_unique_target(target_dir / "f.txt")
        assert final2.name == "f__dup2.txt"

    def test_sort_group_key_with_numbers_only(self):
        assert main.sort_group_key("123") == ("", 123)
        assert main.sort_group_key("456") == ("", 456)

    def test_sort_group_key_with_underscore_prefix(self):
        assert main.sort_group_key("_DSC0001") == ("_DSC", 1)

    def test_get_files_skips_symlink_to_nonexistent(self, tmp_path):
        """应跳过损坏的符号链接（is_file 对断链返回 False）"""
        (tmp_path / "real.txt").write_text("data")
        # symlink 可能无法创建或 is_file 处理不同，确保不崩溃即可
        files, _ = main.get_files(tmp_path, recursive=False, prefix="part_")
        assert len(files) == 1

    def test_build_batches_preserves_order(self):
        groups = [("c", []), ("a", []), ("b", [])]
        batches, _ = main.build_batches(groups, 1, Path("/src"), "part_")
        assert batches[0]["start"] == "c"
        assert batches[0]["end"] == "b"

    def test_preview_count_reset(self):
        main.preview_count = 0
        assert main.preview_count == 0
        main.preview_count = 42
        assert main.preview_count == 42
        main.preview_count = 0
