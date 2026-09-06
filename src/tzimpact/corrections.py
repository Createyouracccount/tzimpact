"""Correction SQL: turn scan hits into reviewable, idempotent UPDATE statements.

tzimpact never executes this SQL. It is written to a file for a human to
review and apply. Two properties are non-negotiable:

* wall-clock semantics are resolved, not assumed: the intended local time is
  re-resolved under the new release; a local time that no longer exists (gap)
  or exists twice (fold) becomes a MANUAL REVIEW entry, never a guess;
* every UPDATE matches only a row that still holds its pre-correction value,
  so applying the file twice changes nothing.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Callable

from . import releases, tzif
from .scan import Affected

WALL_CLOCK = "wall-clock"
INSTANT = "instant"
SEMANTICS = (WALL_CLOCK, INSTANT)

_UTC = dt.timezone.utc


@dataclass(frozen=True)
class Correction:
    row_id: object
    zone: str
    old_raw: object
    new_raw: object
    old_utc: int
    new_utc: int
    intended_local: str  # the local time the row was booked for (old release)
    displayed_local: str  # what the stored instant now shows (new release)
    shift_seconds: int


@dataclass(frozen=True)
class ManualReview:
    row_id: object
    zone: str
    old_raw: object
    intended_local: str
    reason: str  # "nonexistent" | "ambiguous" | "already-correct"
    candidates: tuple[int, ...]


def resolve_wall(tz: tzif.Tz, wall: int) -> list[int]:
    """UTC instants at which `tz` shows the naive wall-clock time `wall`
    (expressed as seconds since epoch as if it were UTC).

    0 results: the local time does not exist (spring-forward gap).
    2 results: it exists twice (fall-back fold). 1: unique.
    """
    probes = {tz.offset_at(wall + d) for d in (-2 * 86400, -86400, 0, 86400, 2 * 86400)}
    found = set()
    for off in probes:
        utc = wall - off
        if tz.offset_at(utc) == off:
            found.add(utc)
    return sorted(found)


def _local_str(seconds_as_utc: int) -> str:
    return dt.datetime.fromtimestamp(seconds_as_utc, _UTC).strftime("%Y-%m-%d %H:%M")


def format_like(raw: object, utc_ts: int) -> object:
    """Render `utc_ts` in the same representation the stored cell used."""
    if isinstance(raw, bool):
        raise TypeError("boolean stored instant")
    if isinstance(raw, int):
        return int(utc_ts)
    if isinstance(raw, float):
        return float(utc_ts)
    s = str(raw)
    text = s.strip()
    sep = "T" if "T" in text else " "
    ends_z = text.endswith("Z")
    parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    frac_digits = 0
    time_part = text[11:]
    if "." in time_part:
        digits = time_part.split(".", 1)[1]
        frac_digits = len(digits.rstrip("Z").split("+")[0].split("-")[0])
    if parsed.tzinfo is None:
        # scan interpreted a naive string as machine-local time; mirror that exactly
        new = dt.datetime.fromtimestamp(utc_ts)
    else:
        new = dt.datetime.fromtimestamp(utc_ts, parsed.tzinfo)
    out = new.strftime(f"%Y-%m-%d{sep}%H:%M:%S")
    if frac_digits:
        out += "." + "0" * frac_digits
    if parsed.tzinfo is not None:
        if ends_z:
            out += "Z"
        else:
            off = parsed.utcoffset() or dt.timedelta(0)
            sign = "-" if off < dt.timedelta(0) else "+"
            total = abs(int(off.total_seconds()))
            out += f"{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"
    return out


def ident(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def literal(v: object) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, (bytes, bytearray)):
        return "X'" + bytes(v).hex() + "'"
    return "'" + str(v).replace("'", "''") + "'"


def _sort_key(h: Affected):
    return (h.zone, type(h.row_id).__name__, h.row_id)


def plan(
    hits: list[Affected],
    to_version: str,
    semantics: str = WALL_CLOCK,
    tz_loader: Callable[[str], tzif.Tz] | None = None,
) -> tuple[list[Correction], list[ManualReview]]:
    """Decide, per affected row, the corrected instant — or that it needs a human."""
    if semantics not in SEMANTICS:
        raise ValueError(f"unknown semantics {semantics!r}; expected one of {SEMANTICS}")
    if semantics == INSTANT:
        return [], []
    if tz_loader is None:
        zi = releases.compile(to_version)

        def tz_loader(zone: str) -> tzif.Tz:
            return tzif.read(str(zi / zone))

    cache: dict[str, tzif.Tz] = {}
    corrections: list[Correction] = []
    reviews: list[ManualReview] = []
    for h in sorted(hits, key=_sort_key):
        tz = cache.get(h.zone)
        if tz is None:
            tz = cache[h.zone] = tz_loader(h.zone)
        wall = h.stored_utc + h.old_offset  # the local time the user picked
        candidates = resolve_wall(tz, wall)
        if len(candidates) != 1:
            reviews.append(
                ManualReview(
                    h.row_id, h.zone, h.stored_raw, _local_str(wall),
                    "nonexistent" if not candidates else "ambiguous", tuple(candidates),
                )
            )
            continue
        new_utc = candidates[0]
        if new_utc == h.stored_utc:
            reviews.append(ManualReview(h.row_id, h.zone, h.stored_raw, _local_str(wall), "already-correct", (new_utc,)))
            continue
        corrections.append(
            Correction(
                h.row_id, h.zone, h.stored_raw, format_like(h.stored_raw, new_utc),
                h.stored_utc, new_utc, _local_str(wall), _local_str(h.stored_utc + h.new_offset),
                h.shift_seconds,
            )
        )
    return corrections, reviews


def render_sql(
    corrections: list[Correction],
    reviews: list[ManualReview],
    *,
    table: str,
    id_col: str,
    utc_col: str,
    tz_col: str,
    from_version: str,
    to_version: str,
    semantics: str,
    affected: list[Affected] | None = None,
    now: dt.datetime | None = None,
) -> str:
    """The file a human reviews. Comments carry zone, intended/displayed local time and shift."""
    from . import __version__

    stamp = (now or dt.datetime.now(_UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"-- tzimpact corrections: {from_version} -> {to_version}",
        f"-- table {ident(table)}  instant column {ident(utc_col)}  zone column {ident(tz_col)}  id column {ident(id_col)}",
        f"-- generated {stamp} by tzimpact {__version__}. REVIEW BEFORE APPLYING. tzimpact never executes this file.",
    ]
    if semantics == INSTANT:
        n = len(affected or [])
        lines += [
            "-- semantics: instant (stored instants are correct as they are; only their displayed local time changes)",
            f"-- No UPDATE statements are generated under instant semantics. {n} row{'s' if n != 1 else ''} will display differently:",
        ]
        for h in sorted(affected or [], key=_sort_key):
            lines.append(
                f"--   {h.zone}  row {h.row_id}  was {h.old_local}  now {h.new_local}  ({h.shift_seconds / 3600:+.0f}h)"
            )
        return "\n".join(lines) + "\n"

    lines += [
        "-- semantics: wall-clock (each row keeps the local time it was booked for; the stored instant moves)",
        "-- Every UPDATE matches only a row still holding its pre-correction value, so applying this file twice changes nothing.",
        "-- ONE-SHOT: run `tzimpact scan` once per release upgrade. After applying this file do NOT scan and regenerate:",
        "-- corrected instants still lie inside the change windows and a regenerated file would move them again.",
        f"-- corrections: {len(corrections)} row{'s' if len(corrections) != 1 else ''}  |  manual review: {len(reviews)}",
    ]
    if corrections:
        lines.append("BEGIN;")
        for c in corrections:
            lines.append(
                f"-- {c.zone}  row {c.row_id}  intended {c.intended_local}  currently shows {c.displayed_local}  "
                f"shift {c.shift_seconds / 3600:+.0f}h"
            )
            lines.append(
                f"UPDATE {ident(table)} SET {ident(utc_col)} = {literal(c.new_raw)} "
                f"WHERE {ident(id_col)} = {literal(c.row_id)} AND {ident(utc_col)} = {literal(c.old_raw)};"
            )
        lines.append("COMMIT;")
    if reviews:
        lines.append("-- MANUAL REVIEW (no UPDATE generated; decide these by hand):")
        for r in reviews:
            what = {
                "nonexistent": f"intended {r.intended_local} does not exist under {to_version} (gap)",
                "ambiguous": f"intended {r.intended_local} occurs twice under {to_version} (fold)",
                "already-correct": f"intended {r.intended_local} already resolves to the stored instant",
            }[r.reason]
            cands = ", ".join(dt.datetime.fromtimestamp(t, _UTC).strftime("%Y-%m-%dT%H:%M:%SZ") for t in r.candidates) or "none"
            lines.append(f"--   {r.zone}  row {r.row_id}  {what}; candidates: {cands}")
    return "\n".join(lines) + "\n"
