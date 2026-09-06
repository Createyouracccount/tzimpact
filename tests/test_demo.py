"""The Morocco demo must run end to end and agree with the committed dataset."""

import json
import pathlib
import subprocess
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
DATASET = json.loads((REPO / "data" / "2026b-2026c.json").read_text())


@pytest.fixture(scope="module")
def demo(tmp_path_factory):
    out = tmp_path_factory.mktemp("demo")
    run = subprocess.run(
        [sys.executable, str(REPO / "docs" / "demo" / "make_demo.py"), "--out", str(out), "--rows", "300"],
        capture_output=True, text=True, cwd=REPO,
    )
    assert run.returncode == 0, run.stderr
    return out, json.loads((out / "summary.json").read_text())


def test_demo_runs_and_writes_files(demo):
    out, summary = demo
    for name in ("clinic.db", "clinic.corrected.db", "corrections.sql", "scan.txt", "before_after.md", "summary.json"):
        assert (out / name).exists(), name
    assert summary["rows"] == 300 and summary["affected"] > 0
    assert summary["all_corrected_show_intended"] is True


def test_demo_zones_and_shifts_match_dataset(demo):
    _, summary = demo
    canonical = {e["zone"]: e for e in DATASET["changed_zones"]}
    aliases = {a: e["zone"] for e in DATASET["changed_zones"] for a in e["aliases"]}
    for zone, shifts in summary["shift_hours"].items():
        canon = aliases.get(zone, zone)
        assert canon in canonical, f"{zone} affected in the demo but not in the dataset"
        expected = canonical[canon]["shift_seconds"] / 3600
        # the dataset shift is new_offset - old_offset; the demo reports the instant move, which is its negative
        assert shifts == [-expected], (zone, shifts, expected)
    assert {"Africa/Casablanca", "America/Edmonton"} <= set(summary["per_zone"]), summary["per_zone"]
    assert "America/Vancouver" not in summary["per_zone"], "Vancouver changed in 2026a->2026b, not here"


def test_demo_scan_output_and_sql_are_consistent(demo):
    out, summary = demo
    scan = (out / "scan.txt").read_text()
    assert f"{summary['affected']:,} rows affected" in scan and "ONE-SHOT" in scan
    sql = (out / "corrections.sql").read_text()
    assert sum(l.startswith("UPDATE ") for l in sql.splitlines()) == summary["affected"]
