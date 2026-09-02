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


def _local(ts: int, offset: int) -> str:
    return dt.datetime.fromtimestamp(ts + offset, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


def index_changes(changes: list[Change]) -> dict[str, list[Change]]:
    by_zone: dict[str, list[Change]] = {}
    for c in changes:
        by_zone.setdefault(c.zone, []).append(c)
    return by_zone


def match(row_id, zone: str, stored_utc: int, by_zone: dict[str, list[Change]]) -> Affected | None:
    for c in by_zone.get(zone, ()):
        if c.start_utc <= stored_utc and (c.end_utc is None or stored_utc < c.end_utc):
            return Affected(
                row_id, zone, stored_utc,
                _local(stored_utc, c.old_offset),
                _local(stored_utc, c.new_offset),
                c.shift_seconds,
            )
    return None


def scan_sqlite(
    db: str, table: str, id_col: str, utc_col: str, tz_col: str, changes: list[Change]
) -> tuple[list[Affected], int]:
    by_zone = index_changes(changes)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(f"SELECT {id_col}, {utc_col}, {tz_col} FROM {table}").fetchall()
    hits = []
    for r in rows:
        raw = r[utc_col]
        ts = int(raw) if isinstance(raw, (int, float)) else int(
            dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00")).timestamp()
        )
        hit = match(r[id_col], r[tz_col], ts, by_zone)
        if hit:
            hits.append(hit)
    conn.close()
    return hits, len(rows)
