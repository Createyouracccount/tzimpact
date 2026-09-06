"""TZif (RFC 8536) reader: exact transition times, offsets, and POSIX footer rules.

Why parse the binary instead of using zoneinfo: we need the *transition
instants themselves* to diff two tzdb releases exactly. Sampling can miss a
change that starts and ends between two samples; enumerating transitions
cannot. zoneinfo deliberately hides them.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from datetime import date as _date

MAGIC = b"TZif"


def _local_midnight_utc(d: "_date") -> int:
    import datetime as _dt

    return int(_dt.datetime.combine(d, _dt.time(), tzinfo=_dt.timezone.utc).timestamp())


@dataclass(frozen=True)
class MonthWeekDayRule:
    """POSIX 'Mm.w.d/time': day d (0=Sunday) of week w (1..5, 5=last) of month m."""

    month: int
    week: int
    day: int
    seconds: int  # local time-of-day the transition happens (may be <0 or >=86400)

    def transition_utc(self, year: int, offset_before: int) -> int:
        import calendar
        import datetime as _dt

        if self.week == 5:
            last = calendar.monthrange(year, self.month)[1]
            d = _dt.date(year, self.month, last)
            d -= _dt.timedelta(days=(d.weekday() + 1 - self.day) % 7)
        else:
            d = _dt.date(year, self.month, 1)
            d += _dt.timedelta(days=(self.day - (d.weekday() + 1) % 7) % 7)
            d += _dt.timedelta(weeks=self.week - 1)
        return _local_midnight_utc(d) + self.seconds - offset_before


@dataclass(frozen=True)
class JulianRule:
    """POSIX 'Jn/time': Julian day n (1..365) with February 29 never counted,
    so J60 is always March 1 and J365 always December 31."""

    day: int
    seconds: int

    def transition_utc(self, year: int, offset_before: int) -> int:
        import calendar
        import datetime as _dt

        d = _dt.date(year, 1, 1) + _dt.timedelta(days=self.day - 1)
        if calendar.isleap(year) and self.day >= 60:
            d += _dt.timedelta(days=1)  # skip February 29
        return _local_midnight_utc(d) + self.seconds - offset_before


@dataclass(frozen=True)
class ZeroBasedJulianRule:
    """POSIX 'n/time': zero-based day n (0..365) with February 29 counted in
    leap years, so day 59 is February 29 in a leap year and March 1 otherwise."""

    day: int
    seconds: int

    def transition_utc(self, year: int, offset_before: int) -> int:
        import datetime as _dt

        d = _dt.date(year, 1, 1) + _dt.timedelta(days=self.day)
        return _local_midnight_utc(d) + self.seconds - offset_before


Rule = MonthWeekDayRule | JulianRule | ZeroBasedJulianRule
PosixRule = MonthWeekDayRule  # historical name


@dataclass(frozen=True)
class Posix:
    std_offset: int
    dst_offset: int | None
    start: Rule | None
    end: Rule | None

    @property
    def is_fixed(self) -> bool:
        return self.dst_offset is None


def _parse_offset(s: str) -> int:
    """POSIX TZ offsets are西-positive: 'EST5' means UTC-5."""
    sign = 1
    if s and s[0] in "+-":
        sign = -1 if s[0] == "-" else 1
        s = s[1:]
    parts = (s.split(":") + ["0", "0"])[:3]
    h, m, sec = (int(p or 0) for p in parts)
    return -sign * (h * 3600 + m * 60 + sec)


def _parse_time_of_day(time_part: str, default_seconds: int) -> int:
    if not time_part:
        return default_seconds
    neg = time_part.startswith("-")
    t = time_part.lstrip("+-")
    parts = (t.split(":") + ["0", "0"])[:3]
    hh, mm, ss = (int(p or 0) for p in parts)
    seconds = hh * 3600 + mm * 60 + ss
    return -seconds if neg else seconds


def _parse_rule(s: str, default_seconds: int = 7200) -> Rule:
    """One POSIX rule: 'Mm.w.d[/time]', 'Jn[/time]' or 'n[/time]'.

    Any other form raises; the caller (diff) surfaces that as an unparseable
    zone instead of skipping it.
    """
    date_part, _, time_part = s.partition("/")
    seconds = _parse_time_of_day(time_part, default_seconds)
    if date_part.startswith("M"):
        fields = date_part[1:].split(".")
        if len(fields) != 3:
            raise ValueError(f"malformed POSIX Mm.w.d rule: {s!r}")
        m, w, d = (int(x) for x in fields)
        if not (1 <= m <= 12 and 1 <= w <= 5 and 0 <= d <= 6):
            raise ValueError(f"POSIX Mm.w.d rule out of range: {s!r}")
        return MonthWeekDayRule(m, w, d, seconds)
    if date_part.startswith("J"):
        n = int(date_part[1:])
        if not (1 <= n <= 365):
            raise ValueError(f"POSIX Jn rule out of range (1..365): {s!r}")
        return JulianRule(n, seconds)
    if date_part.isdigit():
        n = int(date_part)
        if not (0 <= n <= 365):
            raise ValueError(f"POSIX n rule out of range (0..365): {s!r}")
        return ZeroBasedJulianRule(n, seconds)
    raise ValueError(f"unsupported POSIX rule form: {s!r}")


def parse_posix(tz: str) -> Posix | None:
    """Parse the TZif footer string, e.g. 'MST7MDT,M3.2.0,M11.1.0' or 'MST7'."""
    if not tz:
        return None
    i = 0

    def name(j: int) -> tuple[str, int]:
        if j < len(tz) and tz[j] == "<":
            k = tz.index(">", j)
            return tz[j + 1 : k], k + 1
        k = j
        while k < len(tz) and (tz[k].isalpha()):
            k += 1
        return tz[j:k], k

    _, i = name(i)
    j = i
    while j < len(tz) and (tz[j].isdigit() or tz[j] in "+-:"):
        j += 1
    std = _parse_offset(tz[i:j])
    i = j
    if i >= len(tz):
        return Posix(std, None, None, None)
    _, i = name(i)
    j = i
    while j < len(tz) and (tz[j].isdigit() or tz[j] in "+-:"):
        j += 1
    dst = _parse_offset(tz[i:j]) if j > i else std + 3600
    i = j
    if i < len(tz) and tz[i] == ",":
        rules = tz[i + 1 :].split(",")
        if len(rules) != 2:
            raise ValueError(f"POSIX TZ string needs exactly two rules: {tz!r}")
        return Posix(std, dst, _parse_rule(rules[0]), _parse_rule(rules[1]))
    # A DST name without rules is legal POSIX (implementation-defined default),
    # but tzdb never emits it; refusing is safer than guessing US rules.
    raise ValueError(f"POSIX TZ string has a DST name but no rules: {tz!r}")


@dataclass
class Tz:
    """A parsed TZif file."""

    transitions: list[int]  # UTC epoch seconds, sorted
    offsets: list[int]  # utcoffset in effect *at and after* transitions[i]
    initial_offset: int  # before the first transition
    posix: Posix | None

    def offset_at(self, t: int) -> int:
        """Exact UTC offset (seconds) at instant t."""
        if self.transitions and t >= self.transitions[-1] and self.posix and not self.posix.is_fixed:
            return self._posix_offset_at(t)
        if not self.transitions or t < self.transitions[0]:
            if not self.transitions and self.posix:
                return self._posix_offset_at(t)
            return self.initial_offset
        lo, hi = 0, len(self.transitions) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.transitions[mid] <= t:
                lo = mid
            else:
                hi = mid - 1
        return self.offsets[lo]

    def _posix_offset_at(self, t: int) -> int:
        import datetime as _dt

        p = self.posix
        assert p is not None
        if p.is_fixed or p.start is None or p.end is None:
            return p.std_offset
        year = _dt.datetime.fromtimestamp(t, _dt.timezone.utc).year
        s = p.start.transition_utc(year, p.std_offset)
        e = p.end.transition_utc(year, p.dst_offset)
        if s <= e:
            in_dst = s <= t < e
        else:  # southern hemisphere
            in_dst = t >= s or t < e
        return p.dst_offset if in_dst else p.std_offset

    def rule_transitions(self, start: int, end: int) -> list[int]:
        """Transitions generated by the POSIX footer rule within [start, end)."""
        import datetime as _dt

        p = self.posix
        if not p or p.is_fixed or p.start is None or p.end is None:
            return []
        out = []
        y0 = _dt.datetime.fromtimestamp(max(start, 0), _dt.timezone.utc).year
        y1 = _dt.datetime.fromtimestamp(max(end, 0), _dt.timezone.utc).year
        for y in range(y0 - 1, y1 + 2):
            for tt in (
                p.start.transition_utc(y, p.std_offset),
                p.end.transition_utc(y, p.dst_offset),
            ):
                if start <= tt < end:
                    out.append(tt)
        return sorted(out)

    def boundaries(self, start: int, end: int) -> list[int]:
        """Every instant in [start, end) where this zone's offset can change."""
        b = [t for t in self.transitions if start <= t < end]
        b += self.rule_transitions(start, end)
        return sorted(set(b))


def read(path: str) -> Tz:
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:4] != MAGIC:
        raise ValueError(f"not a TZif file: {path}")
    version = raw[4:5]

    def header(off: int):
        counts = struct.unpack_from(">6I", raw, off + 20)
        return counts, off + 44

    counts, pos = header(0)
    isutcnt, isstdcnt, leapcnt, timecnt, typecnt, charcnt = counts

    if version in (b"2", b"3", b"4"):
        # skip the 32-bit block entirely, then re-read the v2+ header
        pos += timecnt * 4 + timecnt + typecnt * 6 + charcnt + leapcnt * 8 + isstdcnt + isutcnt
        assert raw[pos : pos + 4] == MAGIC, "second TZif header not found"
        counts, pos = header(pos)
        isutcnt, isstdcnt, leapcnt, timecnt, typecnt, charcnt = counts
        tsize, lsize = 8, 12
    else:
        tsize, lsize = 4, 8

    fmt = ">%dq" % timecnt if tsize == 8 else ">%di" % timecnt
    transitions = list(struct.unpack_from(fmt, raw, pos)) if timecnt else []
    pos += timecnt * tsize
    idx = list(struct.unpack_from(">%dB" % timecnt, raw, pos)) if timecnt else []
    pos += timecnt

    ttinfo = []
    for i in range(typecnt):
        utoff, isdst, abbrind = struct.unpack_from(">i?B", raw, pos + i * 6)
        ttinfo.append(utoff)
    pos += typecnt * 6
    pos += charcnt + leapcnt * lsize + isstdcnt + isutcnt

    posix = None
    if version in (b"2", b"3", b"4"):
        footer = raw[pos:].decode("ascii", "replace").strip("\n")
        posix = parse_posix(footer.strip())

    offsets = [ttinfo[i] for i in idx]
    # the offset before the first transition: first non-DST type, else type 0
    initial = ttinfo[0] if ttinfo else 0
    return Tz(transitions, offsets, initial, posix)
