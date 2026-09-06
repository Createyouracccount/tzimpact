"""Round trip: scan -> corrections.sql -> apply (test harness) -> rescan = 0 rows.

The SQL file is the product. tzimpact itself never executes it; this test does,
on a synthetic SQLite database, and then checks with the standard library's
zoneinfo (an independent TZif implementation) that every corrected row shows
the same wall-clock time under the new release as it did under the old one.
"""

import datetime as dt
import sqlite3
import zoneinfo

import pytest

from tzimpact import cli, releases
from tzimpact.diff import diff
from tzimpact.scan import scan_sqlite

FROM, TO = "2026b", "2026c"
WHEN = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)
UTC = dt.timezone.utc


def _iso_z(ts):
    return dt.datetime.fromtimestamp(ts, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _iso_off(ts):
    return dt.datetime.fromtimestamp(ts, UTC).isoformat()


def _parse(raw):
    if isinstance(raw, (int, float)):
        return int(raw)
    return int(dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00")).timestamp())


@pytest.fixture(scope="module")
def changes():
    result = diff(FROM, TO, start=WHEN, years=10)
    assert result.unparseable == []
    return result.changes


@pytest.fixture
def synthetic_db(tmp_path, changes):
    """Affected, unaffected, other-zone and boundary rows, in mixed stored formats."""
    cas = [c for c in changes if c.zone == "Africa/Casablanca"]
    edm = [c for c in changes if c.zone == "America/Edmonton"]
    c0, c3, e0 = cas[0], cas[3], edm[0]
    between = cas[0].end_utc + (cas[1].start_utc - cas[0].end_utc) // 2  # both releases agree here
    rows = [
        # id, stored value, zone, expected-affected
        (1, _iso_z(c0.start_utc + 6 * 3600), "Africa/Casablanca", True),
        (2, c0.start_utc, "Africa/Casablanca", True),                 # exactly on window start
        (3, _iso_off(c0.start_utc - 1), "Africa/Casablanca", False),   # one second before
        (4, _iso_z(e0.start_utc + 12 * 3600), "America/Edmonton", True),
        (5, e0.end_utc, "America/Edmonton", False),                    # exactly on window end (exclusive)
        (6, e0.end_utc - 1, "America/Edmonton", True),                 # last second inside
        (7, "2027-07-01T12:00:00Z", "America/Edmonton", False),        # summer: both -06
        (8, "2026-12-01T12:00:00Z", "America/New_York", False),        # other zone
        (9, int(dt.datetime(2027, 1, 15, 9, tzinfo=UTC).timestamp()), "Europe/Berlin", False),
        (10, _iso_z(c3.start_utc + 3600), "Africa/Casablanca", True),  # a later window
        (11, _iso_z(between), "Africa/Casablanca", False),             # between two windows
    ]
    db = tmp_path / "bookings.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE appointments (id INTEGER PRIMARY KEY, starts_at, tz TEXT)")
    conn.executemany("INSERT INTO appointments VALUES (?,?,?)", [(i, v, z) for i, v, z, _ in rows])
    conn.commit()
    conn.close()
    return db, {i: aff for i, _, _, aff in rows}


def _dump(db):
    conn = sqlite3.connect(db)
    out = conn.execute("SELECT id, starts_at, typeof(starts_at), tz FROM appointments ORDER BY id").fetchall()
    conn.close()
    return out


def _scan(db, changes):
    hits, _ = scan_sqlite(str(db), "appointments", "id", "starts_at", "tz", changes)
    return hits


def _apply(db, sql_path):
    conn = sqlite3.connect(db)
    conn.executescript(sql_path.read_text())
    conn.commit()
    conn.close()


def test_scan_classifies_boundaries(synthetic_db, changes):
    db, expected = synthetic_db
    assert {h.row_id for h in _scan(db, changes)} == {i for i, aff in expected.items() if aff}


def test_round_trip_wall_clock(synthetic_db, changes, tmp_path):
    db, expected = synthetic_db
    before = {r[0]: r for r in _dump(db)}
    sql_path = tmp_path / "corrections.sql"

    rc = cli.main([
        "scan", "--from", FROM, "--to", TO, "--sqlite", str(db), "--table", "appointments",
        "--utc-col", "starts_at", "--tz-col", "tz", "--corrections", str(sql_path),
    ])
    assert rc == 0 and sql_path.exists()
    sql = sql_path.read_text()
    assert "wall-clock" in sql and "UPDATE" in sql
    assert '"appointments"' in sql and '"starts_at"' in sql  # identifiers are quoted

    _apply(db, sql_path)
    after = {r[0]: r for r in _dump(db)}

    # 1. Re-scan. NOTE (measured, see docs/verify/NOTES-fix2.md §3): a corrected
    # instant still lies inside the change window, so the scan - which has no
    # notion of intent - flags exactly the same rows again. "0 residual rows"
    # is therefore not attainable by any scan; the round-trip judge is #5 below.
    reflagged = {h.row_id for h in _scan(db, changes)}
    assert reflagged == {i for i, aff in expected.items() if aff}
    # 2. unaffected and other-zone rows are byte-identical (value and storage class)
    for i, aff in expected.items():
        if not aff:
            assert after[i] == before[i], f"row {i} was touched"
    # 3. affected rows keep their storage class and changed value
    for i, aff in expected.items():
        if aff:
            assert after[i][2] == before[i][2], f"row {i} storage class changed"
            assert after[i][1] != before[i][1], f"row {i} was not corrected"
    # 4. idempotent: applying the same file again changes nothing
    _apply(db, sql_path)
    assert _dump(db) == list(after.values())

    # 5. independent oracle: stdlib zoneinfo on the compiled releases
    zi_from, zi_to = releases.compile(FROM), releases.compile(TO)
    for i, aff in expected.items():
        if not aff:
            continue
        zone = before[i][3]
        with open(zi_from / zone, "rb") as f:
            tz_from = zoneinfo.ZoneInfo.from_file(f, key=zone)
        with open(zi_to / zone, "rb") as f:
            tz_to = zoneinfo.ZoneInfo.from_file(f, key=zone)
        old_utc, new_utc = _parse(before[i][1]), _parse(after[i][1])
        intended = dt.datetime.fromtimestamp(old_utc, tz_from).replace(tzinfo=None)
        displayed_uncorrected = dt.datetime.fromtimestamp(old_utc, tz_to).replace(tzinfo=None)
        corrected = dt.datetime.fromtimestamp(new_utc, tz_to).replace(tzinfo=None)
        assert corrected == intended, f"row {i} {zone}: {corrected} != intended {intended}"
        assert displayed_uncorrected != intended, f"row {i} was not actually affected"


def test_instant_semantics_emits_no_updates(synthetic_db, tmp_path):
    db, _ = synthetic_db
    sql_path = tmp_path / "instant.sql"
    rc = cli.main([
        "scan", "--from", FROM, "--to", TO, "--sqlite", str(db), "--table", "appointments",
        "--utc-col", "starts_at", "--tz-col", "tz", "--corrections", str(sql_path), "--semantics", "instant",
    ])
    assert rc == 0
    sql = sql_path.read_text()
    assert not any(l.startswith("UPDATE ") for l in sql.splitlines())
    assert "instant" in sql and "Africa/Casablanca" in sql
    before = _dump(db)
    _apply(db, sql_path)
    assert _dump(db) == before


def test_documented_limitation_regenerate_after_apply_double_shifts(synthetic_db, changes, tmp_path, capsys):
    """This is a *documented limitation*, pinned so it cannot change silently.

    After applying corrections.sql, the corrected instants still sit inside the
    change windows; a second scan re-detects them and a regenerated file would
    move them again. If this test ever fails, the README "Limitations" section,
    the SQL header and the CLI warning must be updated together.
    """
    db, expected = synthetic_db
    affected = {i for i, aff in expected.items() if aff}
    args = ["scan", "--from", FROM, "--to", TO, "--sqlite", str(db), "--table", "appointments",
            "--utc-col", "starts_at", "--tz-col", "tz"]
    first = tmp_path / "first.sql"
    assert cli.main(args + ["--corrections", str(first)]) == 0
    assert "ONE-SHOT" in capsys.readouterr().out
    assert "ONE-SHOT" in first.read_text()
    _apply(db, first)
    corrected = {r[0]: r for r in _dump(db)}

    # re-detected: same rows
    assert {h.row_id for h in _scan(db, changes)} == affected
    second = tmp_path / "second.sql"
    assert cli.main(args + ["--corrections", str(second)]) == 0
    _apply(db, second)
    moved_again = {r[0]: r for r in _dump(db)}
    assert all(moved_again[i] != corrected[i] for i in affected), "regeneration no longer double-shifts: update the docs"
    assert all(moved_again[i] == corrected[i] for i in expected if i not in affected)
