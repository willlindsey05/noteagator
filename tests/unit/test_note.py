from pathlib import Path

from noteagator.note import Note


def _mk(tmp_path: Path, text: str, name: str = "note.md") -> str:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_no_front_matter_returns_raw_body_and_note_metadata(tmp_path: Path):
    raw = "Hello\nWorld\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"note": path}
    assert n.body == raw
    assert n.raw_note == raw


def test_parses_basic_front_matter_unix_newlines(tmp_path: Path):
    raw = "---\n" "title: Sample\n" "tags: [a, b]\n" "---\n" "Body starts here\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"title": "Sample", "tags": ["a", "b"], "note": path}
    assert n.body == "Body starts here\n"


def test_supports_empty_front_matter_block(tmp_path: Path):
    raw = "---\n" "---\n" "Just body\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"note": path}
    assert n.body == "Just body\n"


def test_trims_single_leading_blank_line_after_closing_fence(tmp_path: Path):
    raw = "---\n" "x: 1\n" "---\n" "\n" "Body\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.body == "Body\n"


def test_non_dict_yaml_coerced_to_note_only_metadata(tmp_path: Path):
    raw = "---\n" "- a\n" "- b\n" "---\n" "List was not a mapping\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"note": path}
    assert "List was not a mapping" in n.body


def test_malformed_yaml_yields_note_only_metadata_not_exception(tmp_path: Path):
    raw = "---\n" "title NotYAML\n" "---\n" "Fallback body\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"note": path}
    assert n.body == "Fallback body\n"


def test_bom_before_opening_fence_is_ignored(tmp_path: Path):
    raw = "\ufeff---\n" "title: BOM Test\n" "---\n" "Body\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"title": "BOM Test", "note": path}
    assert n.body == "Body\n"


def test_missing_closing_fence_treated_as_no_front_matter(tmp_path: Path):
    raw = (
        "---\n"
        "title: Missing fence\n"
        "still meta-ish but no closing fence\n"
        "Body that should be raw\n"
    )
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert n.metadata == {"note": path}
    assert n.body == raw


def test_properties_are_never_none_and_types_are_consistent(tmp_path: Path):
    raw = "No meta, just text"
    path = _mk(tmp_path, raw)
    n = Note(path)
    assert isinstance(n.metadata, dict)
    assert isinstance(n.body, str)
    assert n.metadata == {"note": path}
    assert n.body == raw


def test_idempotent_access(tmp_path: Path):
    raw = "---\n" "k: v\n" "---\n" "content\n"
    path = _mk(tmp_path, raw)
    n = Note(path)
    first_meta, first_body = n.metadata, n.body
    second_meta, second_body = n.metadata, n.body
    assert first_meta == {"k": "v", "note": path} and second_meta == {
        "k": "v",
        "note": path,
    }
    assert first_body == "content\n" and second_body == "content\n"


def test_description_from_metadata_and_default_empty(tmp_path: Path):
    raw1 = "---\n" "description: Hello\n" "---\n" "body\n"
    p1 = _mk(tmp_path, raw1, "d1.md")
    n1 = Note(p1)
    assert n1.description == "Hello"

    p2 = _mk(tmp_path, "plain\n", "d2.md")
    n2 = Note(p2)
    assert n2.description == ""


def test_raw_note_setter_reparses_and_invalidates_cache(tmp_path: Path):
    raw1 = "---\n" "title: First\n" "---\n" "one\n"
    path = _mk(tmp_path, raw1)
    n = Note(path)
    assert n.metadata["title"] == "First"
    assert n.metadata["note"] == path
    assert n.body == "one\n"

    raw2 = "---\n" "title: Second\n" "description: changed\n" "---\n" "two\n"
    n.raw_note = raw2
    assert n.metadata == {"title": "Second", "description": "changed", "note": path}
    assert n.body == "two\n"
    assert n.description == "changed"
