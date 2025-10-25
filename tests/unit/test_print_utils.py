import re

import noteagator.print_utils as putils


def test_add_colors_replaces_all_tags():
    text = "A <red>red<end> and <blue>blue<end> and <green>green<end> line."
    out = putils.add_colors(text)
    for key in ["<red>", "<blue>", "<green>", "<end>"]:
        assert key not in out
        assert putils.NOTE_COLORS[key] in out


def test_replace_placeholders_basic():
    body = "cmd -i hello -j ok"
    repl = {"i": "HELLO", "j": None, "k": "X"}
    meta = {"placeholders": {"i": "hello", "j": "ok"}}
    out = putils.replace_placeholders(body, repl, meta)
    assert out == "cmd -i HELLO -j ok"


def test_replace_placeholders_missing_placeholders_key_is_noop():
    body = "body -i a"
    repl = {"-i": "B"}
    meta = {}
    assert putils.replace_placeholders(body, repl, meta) == body


def test_get_code_by_number_markdown_finds_block():
    md = "--copy 1\n```bash\nls -la\n```\n" "--copy 2\n```python\nprint('hi')\n```"
    code = putils.get_code_by_number_markdown(md, 2)
    assert code == "print('hi')"


def test_get_code_by_number_markdown_not_found_returns_none():
    md = "--copy 1\n```bash\necho ok\n```"
    assert putils.get_code_by_number_markdown(md, 3) is None


def test_add_copy_markers_markdown_numbers_blocks_and_preserves_content():
    md = "Before\n```bash\necho A\n```\nMiddle\n```python\nprint('B')\n```\nAfter"
    out = putils.add_copy_markers_markdown(md)
    assert re.search(r"--copy 1\n```bash\necho A\n```", out)
    assert re.search(r"--copy 2\n```python\nprint\('B'\)\n```", out)
    assert "Before" in out and "Middle" in out and "After" in out


def test_print_note_markdown_copies_requested_block(monkeypatch, capsys):
    copied = {"val": None}
    monkeypatch.setattr(putils.pyperclip, "copy", lambda s: copied.update(val=s))

    md = "```bash\necho A\n```\n```python\nprint('B')\n```"
    putils.print_note_markdown(md, copy=2)

    captured = capsys.readouterr()
    assert captured.out
    assert copied["val"] == "print('B')"


def test_add_copy_markers_slim_formats_shell_like_blocks_alignment():
    body = (
        "Intro\n"
        "```bash\n"
        "echo A\n"
        "ls\n"
        "```\n"
        "Between\n"
        "```python\n"
        "print('B')\n"
        "```\n"
        "Outro"
    )
    out = putils.add_copy_markers_slim(body)
    lines = out.splitlines()
    assert "--copy 1 $ echo A" in lines
    cont_prefix = " " * len("--copy 1 ") + "$ "
    assert f"{cont_prefix}ls" in lines
    assert "--copy 2 $ print('B')" in out
    assert "Intro" in out and "Between" in out and "Outro" in out


def test_extract_copy_block_grabs_exact_block_and_stops():
    slim = (
        "--copy 1 $ echo A\n"
        "         $ ls\n"
        "Between\n"
        "--copy 2 $ line1\n"
        "         $ line2\n"
        "--copy 3 $ other\n"
    )
    got = putils.extract_copy_block(slim, 2)
    assert got == "line1\nline2"
    assert putils.extract_copy_block(slim, 99) == ""


def test_print_note_slim_copies_and_prints(monkeypatch, capsys):
    copied = {"val": None}
    monkeypatch.setattr(putils.pyperclip, "copy", lambda s: copied.update(val=s))

    body = "```bash\necho A\n```\n```bash\nB\n```"
    putils.print_note_slim(body, copy=2)

    cap = capsys.readouterr()
    assert "--copy 1 $ echo A" in cap.out
    assert "--copy 2 $ B" in cap.out
    assert copied["val"] == "B"


def test_print_note_slim_no_block_found_prints_error(monkeypatch, capsys):
    monkeypatch.setattr(putils.pyperclip, "copy", lambda s: None)
    body = "```bash\necho A\n```"
    putils.print_note_slim(body, copy=9)
    cap = capsys.readouterr()
    assert "No --copy 9 block found." in cap.out


def test_format_note_body_integration_colors_and_option_replace(monkeypatch):
    body = "<red>HEAD<end> -i foo body"
    meta = {"placeholders": {"i": "foo"}}
    out = putils.format_note_body(
        body, meta, i="BAR", j=None, k=None, u=None, d=None, p=None
    )

    assert putils.NOTE_COLORS["<red>"] in out and putils.NOTE_COLORS["<end>"] in out
    assert "-i BAR" in out
