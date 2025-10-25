import os
import pathlib

import pytest

import noteagator.fsutils as fsutils
from noteagator.fsutils import print_directory_structure


def make_file(p: pathlib.Path, text: str = "dummy"):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


@pytest.fixture(autouse=True)
def stub_return_description(monkeypatch):
    monkeypatch.setattr(fsutils, "return_description", lambda path: " - desc")
    yield


def test_print_directory_structure_orders_dirs_before_files_case_insensitive(
    tmp_path, capsys
):
    # Arrange: create structure
    # root/
    #   a/ (contains subfile.txt)
    #   b/
    #   .git/ (should be skipped)
    #   A.txt
    #   z.txt
    (tmp_path / ".git").mkdir()
    make_file(tmp_path / ".git" / "ignore.txt", "ignored")

    (tmp_path / "a").mkdir()
    make_file(tmp_path / "a" / "subfile.txt", "note: one")

    (tmp_path / "b").mkdir()

    make_file(tmp_path / "A.txt", "note: A")
    make_file(tmp_path / "z.txt", "note: Z")

    structure = print_directory_structure(
        c_cwd=str(tmp_path),
        c_base=str(tmp_path),
        max_depth=None,
    )
    out = capsys.readouterr().out

    assert "Notebook Directory:" in out
    assert ".git" not in out

    idx_a_dir = out.find("📁 a")
    idx_b_dir = out.find("📁 b")
    idx_A_txt = out.find("📄 A.txt")
    idx_z_txt = out.find("📄 z.txt")

    assert idx_a_dir != -1 and idx_b_dir != -1 and idx_A_txt != -1 and idx_z_txt != -1
    assert idx_a_dir < idx_A_txt
    assert idx_b_dir < idx_A_txt
    assert idx_A_txt < idx_z_txt

    assert isinstance(structure, dict) and len(structure) >= 4
    has_dir = any(
        v.get("type") == "dir" and os.path.isabs(v.get("absolute_path", ""))
        for v in structure.values()
    )
    has_file = any(
        v.get("type") == "file" and os.path.isabs(v.get("absolute_path", ""))
        for v in structure.values()
    )
    assert has_dir and has_file


def test_print_directory_structure_respects_max_depth_1(tmp_path, capsys):
    (tmp_path / "a").mkdir()
    make_file(tmp_path / "a" / "subfile.txt", "inside a")
    make_file(tmp_path / "root.txt", "at root")

    _ = print_directory_structure(
        c_cwd=str(tmp_path),
        c_base=str(tmp_path),
        max_depth=1,
    )
    out = capsys.readouterr().out

    assert "📁 a" in out
    assert "subfile.txt" not in out
    assert "📄 root.txt" in out


def test_print_directory_structure_structure_indices_are_sequential(tmp_path):
    (tmp_path / "d").mkdir()
    make_file(tmp_path / "f1.txt", "x")
    make_file(tmp_path / "f2.txt", "y")

    structure = print_directory_structure(
        c_cwd=str(tmp_path),
        c_base=str(tmp_path),
        max_depth=1,
    )

    keys = sorted(structure.keys())
    assert keys == list(range(1, len(keys) + 1))

    for v in structure.values():
        assert v["type"] in {"dir", "file"}
        assert isinstance(v["absolute_path"], str)
        assert os.path.isabs(v["absolute_path"])
