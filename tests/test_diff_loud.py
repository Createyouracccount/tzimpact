"""A zone that cannot be parsed must never be dropped silently.

The diff of two releases is only trustworthy if every zone that exists in both
was actually compared. Before this test existed, ``diff()`` swallowed parse
errors per zone (``except Exception: continue``) and Asia/Tehran vanished from
every 2020a-2022a diff without a trace (docs/verify/GATE.md, row 12).
"""

import datetime as dt
import pathlib
import shutil

import pytest

from tzimpact import cli, releases
from tzimpact.diff import diff as run_diff

SYSTEM_UTC = pathlib.Path("/usr/share/zoneinfo/UTC")
WHEN = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)


@pytest.fixture
def two_releases(tmp_path, monkeypatch):
    """Fake releases A and B: one good zone, one zone that is not a TZif file."""
    for v in ("A", "B"):
        zi = tmp_path / v
        (zi / "Good").mkdir(parents=True)
        (zi / "Bad").mkdir(parents=True)
        shutil.copy(SYSTEM_UTC, zi / "Good" / "Zone")
        (zi / "Bad" / "Zone").write_bytes(b"NOT A TZIF FILE" + bytes(60))
    monkeypatch.setattr(releases, "compile", lambda v: tmp_path / v)
    return tmp_path


def test_unparseable_zone_is_reported_not_dropped(two_releases):
    result = run_diff("A", "B", start=WHEN, years=1)
    assert [u.zone for u in result.unparseable] == ["Bad/Zone"], result
    assert "TZif" in result.unparseable[0].error
    assert result.changes == []  # UTC never changes; the good zone was compared


def test_cli_diff_warns_and_fails_on_unparseable(two_releases, capsys):
    rc = cli.main(["diff", "A", "B"])
    err = capsys.readouterr().err
    assert rc != 0, "an unparseable zone must not yield a success exit code"
    assert "Bad/Zone" in err and "NOT covered" in err


def test_cli_diff_json_carries_unparseable(two_releases, capsys):
    import json

    rc = cli.main(["diff", "A", "B", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert rc != 0
    assert [u["zone"] for u in out["unparseable"]] == ["Bad/Zone"]
