"""Generator internals: local-time resolution (gap/fold), stored-format mirroring, quoting."""

import datetime as dt

import pytest

from tzimpact import corrections as corr
from tzimpact.scan import Affected
from tzimpact.tzif import Tz

UTC = dt.timezone.utc


def _ts(*a):
    return int(dt.datetime(*a, tzinfo=UTC).timestamp())


# A synthetic US-East-like zone for 2027: -05 -> -04 at 2027-03-14 07:00Z, back at 2027-11-07 06:00Z.
NY2027 = Tz(transitions=[_ts(2027, 3, 14, 7), _ts(2027, 11, 7, 6)], offsets=[-4 * 3600, -5 * 3600],
            initial_offset=-5 * 3600, posix=None)


def test_resolve_wall_unique_gap_and_fold():
    assert corr.resolve_wall(NY2027, _ts(2027, 6, 1, 12)) == [_ts(2027, 6, 1, 16)]      # 12:00 EDT
    assert corr.resolve_wall(NY2027, _ts(2027, 3, 14, 2, 30)) == []                       # gap
    assert corr.resolve_wall(NY2027, _ts(2027, 11, 7, 1, 30)) == [_ts(2027, 11, 7, 5, 30), _ts(2027, 11, 7, 6, 30)]  # fold


def _hit(row_id, wall_local, old_off, new_off, raw=None):
    stored = wall_local - old_off
    return Affected(row_id, "Synthetic/Zone", stored, "", "", new_off - old_off, old_off, new_off, raw if raw is not None else stored)


def test_plan_routes_gap_and_fold_to_manual_review():
    hits = [
        _hit(1, _ts(2027, 6, 1, 12), -5 * 3600, -4 * 3600),     # unique -> correction
        _hit(2, _ts(2027, 3, 14, 2, 30), -5 * 3600, -4 * 3600), # gap -> review
        _hit(3, _ts(2027, 11, 7, 1, 30), -5 * 3600, -4 * 3600), # fold -> review
    ]
    fixes, reviews = corr.plan(hits, "unused", tz_loader=lambda zone: NY2027)
    assert [c.row_id for c in fixes] == [1]
    assert fixes[0].new_utc == _ts(2027, 6, 1, 16)
    assert [(r.row_id, r.reason) for r in reviews] == [(2, "nonexistent"), (3, "ambiguous")]
    sql = corr.render_sql(fixes, reviews, table="t", id_col="id", utc_col="at", tz_col="tz",
                          from_version="A", to_version="B", semantics=corr.WALL_CLOCK)
    assert sum(l.startswith("UPDATE ") for l in sql.splitlines()) == 1 and "MANUAL REVIEW" in sql and "(gap)" in sql and "(fold)" in sql


def test_plan_instant_semantics_is_empty():
    assert corr.plan([_hit(1, _ts(2027, 6, 1, 12), -5 * 3600, -4 * 3600)], "B", semantics=corr.INSTANT) == ([], [])


@pytest.mark.parametrize(
    "raw,expected",
    [
        (1780000000, 1780003600),
        ("2026-09-20T06:13:00Z", "2026-09-20T07:13:00Z"),
        ("2026-09-20T06:13:00+00:00", "2026-09-20T07:13:00+00:00"),
        ("2026-09-20 06:13:00+00:00", "2026-09-20 07:13:00+00:00"),
        ("2026-09-20T06:13:00.000Z", "2026-09-20T07:13:00.000Z"),
        ("2026-09-20T08:13:00+02:00", "2026-09-20T09:13:00+02:00"),
    ],
)
def test_format_like_mirrors_stored_representation(raw, expected):
    base = int(dt.datetime(2026, 9, 20, 6, 13, tzinfo=UTC).timestamp()) if isinstance(raw, str) else raw
    assert corr.format_like(raw, base + 3600) == expected


def test_identifiers_and_literals_are_quoted():
    fixes = [corr.Correction(row_id="ap'1", zone="Z", old_raw="2026-01-01T00:00:00Z", new_raw="2026-01-01T01:00:00Z",
                             old_utc=0, new_utc=3600, intended_local="x", displayed_local="y", shift_seconds=-3600)]
    sql = corr.render_sql(fixes, [], table='odd"name', id_col="row id", utc_col="starts at", tz_col="tz",
                          from_version="A", to_version="B", semantics=corr.WALL_CLOCK)
    assert '"odd""name"' in sql and '"starts at"' in sql and '"row id"' in sql
    assert "'ap''1'" in sql
