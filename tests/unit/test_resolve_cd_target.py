from pathlib import Path

from noteagator.fsutils import resolve_cd_target


def test_entry_path_dir_returns_itself(tmp_path: Path):
    base = tmp_path.as_posix()
    cwd = (tmp_path / "a").as_posix()
    entry = (tmp_path / "a" / "b").as_posix()
    assert resolve_cd_target("3", entry, "dir", cwd, base) == entry


def test_entry_path_file_returns_parent(tmp_path: Path):
    base = tmp_path.as_posix()
    cwd = (tmp_path / "a").as_posix()
    file_path = (tmp_path / "a" / "note.md").as_posix()
    expected_parent = (tmp_path / "a").as_posix()
    assert resolve_cd_target("7", file_path, "file", cwd, base) == expected_parent


def test_dotdot_moves_up_when_not_at_base(tmp_path: Path):
    base = (tmp_path / "root").as_posix()
    cwd = (tmp_path / "root" / "x" / "y").as_posix()
    expected = (tmp_path / "root" / "x").as_posix()
    assert resolve_cd_target("..", None, None, cwd, base) == expected


def test_dotdot_stays_when_at_base(tmp_path: Path):
    base = (tmp_path / "root").as_posix()
    cwd = base
    assert resolve_cd_target("..", None, None, cwd, base) == base


def test_slash_goes_to_base(tmp_path: Path):
    base = (tmp_path / "root").as_posix()
    cwd = (tmp_path / "root" / "a").as_posix()
    assert resolve_cd_target("/", None, None, cwd, base) == base


def test_unknown_value_without_entry_keeps_cwd(tmp_path: Path):
    base = (tmp_path / "root").as_posix()
    cwd = (tmp_path / "root" / "a").as_posix()
    assert resolve_cd_target("123", None, None, cwd, base) == cwd
