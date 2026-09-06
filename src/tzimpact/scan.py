"""Map release changes onto stored rows.

The pattern that breaks: a row stores an instant (UTC) that was computed from
a local wall-clock intent plus a zone. When the zone's rules change, the stored
instant still means the same *absolute* moment but no longer the same *local*
moment — so the appointment shows up an hour off.
"""

from __future__ import annotations

import datetime as dt
import sqlite3
from dataclasses import dataclass

from .diff import Change


@dataclass(frozen=True)
class Affected:
    row_id: object
    zone: str
    stored_utc: int
    old_local: str
    new_local: str
    shift_seconds: int
    old_offset: int = 0
    new_offset: int = 0
    stored_raw: object = None  # the cell exactly as stored; corrections must match it


def _local(ts: int, offset: int) -> str:
    return dt.datetime.fromtimestamp(ts + offset, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


def index_changes(changes: list[Change]) -> dict[str, list[Change]]:
    by_zone: dict[str, list[Change]] = {}
    for c in changes:
        by_zone.setdefault(c.zone, []).append(c)
    return by_zone


def match(
    row_id, zone: str, stored_utc: int, by_zone: dict[str, list[Change]], stored_raw: object = None
) -> Affected | None:
    for c in by_zone.get(zone, ()):
        if c.start_utc <= stored_utc and (c.end_utc is None or stored_utc < c.end_utc):
            return Affected(
                row_id, zone, stored_utc,
                _local(stored_utc, c.old_offset),
                _local(stored_utc, c.new_offset),
                c.shift_seconds,
                c.old_offset, c.new_offset, stored_raw,
            )
    return None


def _ident(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def to_instant(raw: object, naive_is_utc: bool) -> int:
    """Stored cell -> UTC epoch seconds.

    Integers/floats are epoch seconds. datetimes and ISO strings with an offset
    (or 'Z') are exact. A *naive* value is interpreted as UTC for Postgres
    (`timestamp without time zone` under a --utc-col flag) and, for SQLite, as
    the machine's local time - the historical behaviour, see RISKS R15.
    """
    if isinstance(raw, bool):
        raise TypeError("boolean stored instant")
    if isinstance(raw, (int, float)):
        return int(raw)
    if isinstance(raw, dt.datetime):
        if raw.tzinfo is None:
            return int(raw.replace(tzinfo=dt.timezone.utc).timestamp()) if naive_is_utc else int(raw.timestamp())
        return int(raw.timestamp())
    parsed = dt.datetime.fromisoformat(str(raw).strip().replace("Z", "+00:00"))
    if parsed.tzinfo is None and naive_is_utc:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return int(parsed.timestamp())


def scan_sqlite(
    db: str, table: str, id_col: str, utc_col: str, tz_col: str, changes: list[Change]
) -> tuple[list[Affected], int]:
    by_zone = index_changes(changes)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        f"SELECT {_ident(id_col)}, {_ident(utc_col)}, {_ident(tz_col)} FROM {_ident(table)}"
    ).fetchall()
    hits = []
    for r in rows:
        raw = r[utc_col]
        hit = match(r[id_col], r[tz_col], to_instant(raw, naive_is_utc=False), by_zone, stored_raw=raw)
        if hit:
            hits.append(hit)
    conn.close()
    return hits, len(rows)


def scan_postgres(
    dsn: str, table: str, id_col: str, utc_col: str, tz_col: str, changes: list[Change]
) -> tuple[list[Affected], int]:
    """Same contract as scan_sqlite. Read-only: one SELECT, no writes, no temp objects.

    Requires the optional dependency psycopg (`pip install tzimpact[postgres]`).
    `timestamptz` and epoch integers are exact; `timestamp without time zone`
    is read as UTC, which is what a --utc-col column is declared to hold.
    """
    try:
        import psycopg
    except ImportError as exc:  # loud, not silent
        raise RuntimeError("Postgres scanning needs psycopg: pip install 'tzimpact[postgres]'") from exc
    by_zone = index_changes(changes)
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {_ident(id_col)}, {_ident(utc_col)}, {_ident(tz_col)} FROM {_ident(table)}")
            rows = cur.fetchall()
    hits = []
    for row_id, raw, zone in rows:
        hit = match(row_id, zone, to_instant(raw, naive_is_utc=True), by_zone, stored_raw=raw)
        if hit:
            hits.append(hit)
    return hits, len(rows)
