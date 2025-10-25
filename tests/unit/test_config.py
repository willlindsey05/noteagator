import json
from pathlib import Path

import pytest

from noteagator.config import Config


def read_cfg(cfg) -> dict:
    with open(cfg.config_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def cfg(tmp_path) -> Config:
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    return Config(home_dir=str(fake_home))


def test_bootstrap_creates_dirs_and_config(cfg: Config):
    assert Path(cfg.app_path).is_dir()
    assert Path(cfg.default_notebook_path).is_dir()
    assert Path(cfg.config_path).is_file()

    data = read_cfg(cfg)
    assert data["base"] == cfg.default_notebook_path
    assert data["cwd"] == cfg.default_notebook_path


def test_config_data_is_readonly(cfg: Config):
    view = cfg.config_data
    with pytest.raises(TypeError):
        view["base"] = "nope"


def test_config_data_setter_persists(cfg: Config):
    new_data = {"base": "B", "cwd": "C", "display_index": {"x": 1}}
    cfg.config_data = new_data
    assert dict(cfg.config_data) == new_data
    assert read_cfg(cfg) == new_data


def test_setters_update_and_persist(cfg: Config, tmp_path: Path):
    new_base = tmp_path / "nb"
    new_cwd = tmp_path / "cwd"
    new_base.mkdir()
    new_cwd.mkdir()

    cfg.notebook_base_dir = str(new_base)
    cfg.notebook_cwd = str(new_cwd)

    assert cfg.notebook_base_dir == str(new_base)
    assert cfg.notebook_cwd == str(new_cwd)

    data = read_cfg(cfg)
    assert data["base"] == str(new_base)
    assert data["cwd"] == str(new_cwd)


def test_ensure_config_path_does_not_overwrite_existing(cfg: Config):
    cfg.notebook_base_dir = cfg.notebook_base_dir + "_custom"
    cfg.notebook_cwd = cfg.notebook_cwd + "_custom"
    before = read_cfg(cfg)

    cfg.ensure_config_path()
    after = read_cfg(cfg)
    assert after == before


@pytest.mark.parametrize("base_val,cwd_val", [(None, None), ("", ""), (None, "")])
def test_ensure_config_keys_backfills_missing_or_falsy(cfg: Config, base_val, cwd_val):
    with open(cfg.config_path, "w", encoding="utf-8") as f:
        json.dump({"base": base_val, "cwd": cwd_val}, f)

    cfg._config_data = cfg._get_config()
    cfg.ensure_config_keys()

    data = read_cfg(cfg)
    assert data["base"] == cfg.default_notebook_path
    assert data["cwd"] == cfg.default_notebook_path


def test_display_index_round_trip_persists(cfg: Config, tmp_path: Path):
    f = tmp_path / "note.md"
    f.write_text("# hello", encoding="utf-8")

    payload = {
        "1": {"type": "file", "absolute_path": str(f)},
        "2": {"type": "dir", "absolute_path": str(tmp_path)},
    }
    cfg.display_index = payload
    assert cfg.display_index == payload
    assert read_cfg(cfg)["display_index"] == payload


def test_return_file_path_valid_file(cfg: Config, tmp_path: Path):
    f = tmp_path / "ok.md"
    f.write_text("ok", encoding="utf-8")
    cfg.display_index = {"1": {"type": "file", "absolute_path": str(f)}}
    assert cfg.return_file_path("1") == str(f)


def test_return_file_path_invalid_index_raises(cfg: Config):
    cfg.display_index = {}
    with pytest.raises(SystemExit) as exc:
        cfg.return_file_path("99")
    assert "Invalid Selection" in str(exc.value)


def test_return_file_path_non_file_raises(cfg: Config, tmp_path: Path):
    cfg.display_index = {"2": {"type": "dir", "absolute_path": str(tmp_path)}}
    with pytest.raises(SystemExit) as exc:
        cfg.return_file_path("2")
    assert "Invalid Selection" in str(exc.value)
