"""Read-only iCalendar (RFC 5545) scan: which VEVENTs change instant.

An ICS event with ``DTSTART;TZID=<zone>:<local>`` states its *local* time
explicitly, so its intent is known. What changes under a tzdb release is the
instant that local time resolves to. An event is affected when the instant it
resolves to under the old release differs from the instant it resolves to
under the new release. Both resolutions use the same convention as Python's
zoneinfo with ``fold=0``: an ambiguous local time is its earlier occurrence,
and a local time inside a spring-forward gap is shifted forward using the
offset in force before the gap. Zones that the diff reports unchanged are not
resolved at all (their rules agree over the whole window), which keeps the
scan cheap.

Nothing here writes to the file. Events that cannot be assessed are reported,
never dropped:

* ``DTSTART`` missing or malformed         -> unparseable
* floating date-time (no TZID, no Z)       -> unparseable (no zone to assess in)
* TZID that is not a known tzdb zone        -> unparseable (Windows names, vendor prefixes)
* ``...Z`` (UTC form)                       -> instant semantics, counted, not affected
* ``VALUE=DATE`` (all-day)                  -> counted, not affected (dates do not shift)
* ``RRULE`` present                         -> only DTSTART is assessed; counted as recurring
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from . import releases, tzif
from .corrections import resolve_wall
from .diff import Change
from .scan import Affected, _local, index_changes

_UTC = dt.timezone.utc


@dataclass(frozen=True)
class Unassessable:
    event_id: str
    reason: str


@dataclass
class IcsReport:
    hits: list[Affected] = field(default_factory=list)
    total: int = 0  # every VEVENT seen
    utc_events: int = 0  # DTSTART in Z form: instant semantics
    all_day_events: int = 0  # VALUE=DATE
    recurring_events: int = 0  # RRULE present; only DTSTART assessed
    unparseable: list[Unassessable] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return not self.unparseable


def unfold(text: str) -> list[str]:
    """RFC 5545 section 3.1: a line starting with SPACE or HTAB continues the previous line."""
    lines: list[str] = []
    for raw in text.splitlines():
        if raw[:1] in (" ", "\t") and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    return lines


def _split_property(line: str) -> tuple[str, dict[str, str], str] | None:
    """'DTSTART;TZID=Africa/Casablanca:20261001T100000' -> ('DTSTART', {'TZID': ...}, value)."""
    in_quotes = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_quotes = not in_quotes
        elif ch == ":" and not in_quotes:
            head, value = line[:i], line[i + 1 :]
            break
    else:
        return None
    parts = head.split(";")
    name = parts[0].upper()
    params: dict[str, str] = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            params[k.upper()] = v.strip('"')
    return name, params, value


def events(text: str) -> list[dict]:
    """Each VEVENT as {'_lineno': int, 'DTSTART': (params, value), 'UID': (params, value), ...}."""
    out: list[dict] = []
    current: dict | None = None
    for n, line in enumerate(unfold(text), 1):
        if line.strip().upper() == "BEGIN:VEVENT":
            current = {"_lineno": n}
            continue
        if line.strip().upper() == "END:VEVENT":
            if current is not None:
                out.append(current)
            current = None
            continue
        if current is None:
            continue
        prop = _split_property(line)
        if prop is None:
            continue
        name, params, value = prop
        current.setdefault(name, (params, value.strip()))
    return out


def _parse_local(value: str) -> int:
    """'20261001T100000' -> seconds since epoch as if UTC (a naive wall-clock number)."""
    if len(value) != 15 or value[8] != "T":
        raise ValueError(f"not a DATE-TIME: {value!r}")
    d = dt.datetime.strptime(value, "%Y%m%dT%H%M%S").replace(tzinfo=_UTC)
    return int(d.timestamp())


def resolve_fold0(tz: tzif.Tz, wall: int) -> int:
    """Local wall-clock (seconds as if UTC) -> instant, zoneinfo fold=0 semantics.

    Ambiguous: the earlier instant. Nonexistent (gap): use the offset in force
    just before the gap, so the instant lands after the transition.
    """
    candidates = resolve_wall(tz, wall)
    if candidates:
        return candidates[0]
    for t in tz.boundaries(wall - 2 * 86400, wall + 2 * 86400):
        before, after = tz.offset_at(t - 1), tz.offset_at(t)
        if after > before and t + before <= wall < t + after:  # inside this gap
            return wall - before
    raise ValueError("local time has no resolution and is not inside a gap")


def _vendor_stripped(tzid: str) -> str:
    """'/mozilla.org/20050126_1/Africa/Casablanca' -> 'Africa/Casablanca'."""
    if tzid.startswith("/") and tzid.count("/") >= 2:
        return "/".join(tzid.split("/")[-2:])
    return tzid


def scan_ics_report(
    path: str,
    changes: list[Change],
    from_version: str,
    to_version: str,
    known_zones: set[str] | None = None,
) -> IcsReport:
    by_zone = index_changes(changes)
    zi_from, zi_to = releases.compile(from_version), releases.compile(to_version)
    cache: dict[str, tuple[tzif.Tz, tzif.Tz]] = {}
    report = IcsReport()
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    for ev in events(text):
        report.total += 1
        uid = ev.get("UID", ({}, ""))[1] or ev.get("SUMMARY", ({}, ""))[1] or f"line {ev['_lineno']}"
        if "RRULE" in ev:
            report.recurring_events += 1
        if "DTSTART" not in ev:
            report.unparseable.append(Unassessable(uid, "no DTSTART"))
            continue
        params, value = ev["DTSTART"]
        if params.get("VALUE", "").upper() == "DATE":
            report.all_day_events += 1
            continue
        if value.endswith("Z"):
            try:
                _parse_local(value[:-1])
            except ValueError as exc:
                report.unparseable.append(Unassessable(uid, f"malformed UTC DTSTART {value!r}: {exc}"))
                continue
            report.utc_events += 1
            continue
        tzid = params.get("TZID")
        if not tzid:
            report.unparseable.append(Unassessable(uid, f"floating DTSTART {value!r}: no TZID, cannot be assessed"))
            continue
        zone = _vendor_stripped(tzid)
        if known_zones is not None and zone not in known_zones:
            report.unparseable.append(Unassessable(uid, f"TZID {tzid!r} is not a tzdb zone"))
            continue
        try:
            wall = _parse_local(value)
        except ValueError as exc:
            report.unparseable.append(Unassessable(uid, f"malformed DTSTART {value!r}: {exc}"))
            continue
        if zone not in by_zone:
            continue  # the diff says this zone's rules agree over the window: cannot be affected
        if zone not in cache:
            try:
                cache[zone] = (tzif.read(str(zi_from / zone)), tzif.read(str(zi_to / zone)))
            except Exception as exc:  # surfaced, never dropped
                report.unparseable.append(
                    Unassessable(uid, f"zone {zone} could not be read: {type(exc).__name__}: {exc}")
                )
                continue
        tz_from, tz_to = cache[zone]
        try:
            old_instant, new_instant = resolve_fold0(tz_from, wall), resolve_fold0(tz_to, wall)
        except ValueError as exc:
            report.unparseable.append(Unassessable(uid, f"{value!r} in {zone}: {exc}"))
            continue
        if old_instant == new_instant:
            continue
        old_off, new_off = tz_from.offset_at(old_instant), tz_to.offset_at(old_instant)
        report.hits.append(
            Affected(
                uid, zone, old_instant, _local(old_instant, old_off), _local(old_instant, new_off),
                old_instant - new_instant, old_off, tz_to.offset_at(new_instant), value,
            )
        )
    return report


def scan_ics(
    path: str, changes: list[Change], from_version: str, to_version: str, known_zones: set[str] | None = None
) -> tuple[list[Affected], int]:
    """Same (hits, total) contract as scan_sqlite/scan_postgres; the full report is scan_ics_report()."""
    r = scan_ics_report(path, changes, from_version, to_version, known_zones)
    return r.hits, r.total
