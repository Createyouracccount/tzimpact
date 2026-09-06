"""The bot's decision, pinned without the network."""

import json

import pytest

from tzimpact import cli, watch

INDEX = {"schema": "tzimpact-data/1", "pairs": [
    {"from": "2026a", "to": "2026b", "released": "2026-04-22", "file": "2026a-2026b.json", "changed_zone_count": 1},
    {"from": "2026b", "to": "2026c", "released": "2026-07-08", "file": "2026b-2026c.json", "changed_zone_count": 3},
]}


def test_up_to_date(tmp_path):
    p = tmp_path / "index.json"; p.write_text(json.dumps(INDEX))
    r = watch.check(p, ["2025c", "2026a", "2026b", "2026c"])
    assert r == {"committed": "2026c", "available": "2026c", "update_needed": False, "missing": []}


def test_newer_release_detected_across_year_boundary(tmp_path):
    p = tmp_path / "index.json"; p.write_text(json.dumps(INDEX))
    r = watch.check(p, ["2026b", "2026c", "2026d", "2027a"])
    assert r["update_needed"] is True and r["available"] == "2027a" and r["missing"] == ["2026d", "2027a"]


def test_ordering_is_by_name_not_position():
    assert watch.update_needed("2026c", "2027a") and not watch.update_needed("2027a", "2026c")
    assert watch.available_latest(["2027a", "2026c", "2026d"]) == "2027a"
    assert watch.committed_latest({"pairs": [{"to": "2026c"}, {"to": "2026b"}]}) == "2026c"


@pytest.mark.parametrize("bad", ["2026", "26c", "tzdata2026c", ""])
def test_malformed_names_are_loud(bad):
    with pytest.raises(ValueError):
        watch.update_needed("2026c", bad)
    with pytest.raises(ValueError):
        watch.available_latest([bad])


def test_empty_index_is_loud(tmp_path):
    p = tmp_path / "index.json"; p.write_text(json.dumps({"pairs": []}))
    with pytest.raises(ValueError):
        watch.check(p, ["2026c"])


def test_cli_writes_github_output(tmp_path, capsys, monkeypatch):
    p = tmp_path / "index.json"; p.write_text(json.dumps(INDEX))
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    rc = cli.main(["watch", "--index", str(p), "--names", "2026c", "2027a"])
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["update_needed"] is True
    assert out.read_text().splitlines() == ["update_needed=true", "committed=2026c", "available=2027a"]


def test_cli_without_github_output_writes_nothing(tmp_path, capsys, monkeypatch):
    p = tmp_path / "index.json"; p.write_text(json.dumps(INDEX))
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    assert cli.main(["watch", "--index", str(p), "--names", "2026c"]) == 0
    assert json.loads(capsys.readouterr().out)["update_needed"] is False


def test_committed_index_is_consistent_with_itself():
    """The real data/index.json must parse and name a real latest release."""
    import pathlib
    r = watch.check(pathlib.Path("data/index.json"), ["2020a", "2026c"])
    assert r["committed"] == "2026c" and r["update_needed"] is False
