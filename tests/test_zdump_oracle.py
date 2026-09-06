"""Independent oracle: the transition instants tzif.read() produces must equal
what zdump (tzcode, the reference implementation) prints for the same file.

The golden suite shares its oracle (NEWS) with the thing under test; this one
does not. It also covers the case that was silently dropped before: the 2022a
Asia/Tehran file, whose footer uses the POSIX 'Jn' form.
"""

import datetime as dt
import pathlib
import shutil
import subprocess

import pytest

from tzimpact import releases, tzif

ZDUMP = shutil.which("zdump")
CASES = [
    # (release, zone, first year, last year inclusive) — control zones use Mm.w.d rules
    ("2022a", "Asia/Tehran", 2023, 2026),        # POSIX 'J79/24,J263/24'
    ("2022a", "America/New_York", 2023, 2026),   # 'M3.2.0,M11.1.0'
    ("2022a", "Australia/Sydney", 2023, 2026),   # southern hemisphere 'M10.1.0,M4.1.0/3'
    ("2026c", "America/Edmonton", 2026, 2036),   # explicit transitions end, then fixed
]


def _zdump_transitions(path: pathlib.Path, y0: int, y1: int) -> set[int]:
    """Instants where zdump -v reports the UTC offset changing, within [y0, y1]."""
    out = subprocess.run(
        [ZDUMP, "-v", "-c", f"{y0},{y1 + 1}", str(path)], check=True, capture_output=True, text=True
    ).stdout
    instants, prev_off = set(), None
    for line in out.splitlines():
        if " UT = " not in line or "NULL" in line or "failed" in line:
            continue
        left, right = line.split(" UT = ", 1)
        stamp = left.split(maxsplit=1)[1].strip()
        try:
            when = dt.datetime.strptime(stamp, "%a %b %d %H:%M:%S %Y").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue  # zdump also prints far-past/far-future sentinel rows (year -2147481748 etc.)
        if not (y0 <= when.year <= y1 + 1):
            continue
        off = int(right.rsplit("gmtoff=", 1)[1])
        if prev_off is not None and off != prev_off:
            instants.add(int(when.timestamp()))
        prev_off = off
    return instants


def _tzif_transitions(path: pathlib.Path, y0: int, y1: int) -> set[int]:
    tz = tzif.read(str(path))
    start = int(dt.datetime(y0, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    end = int(dt.datetime(y1 + 1, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    return {b for b in tz.boundaries(start, end) if tz.offset_at(b) != tz.offset_at(b - 1)}


@pytest.mark.skipif(ZDUMP is None, reason="zdump not installed")
@pytest.mark.parametrize("release,zone,y0,y1", CASES, ids=[f"{c[0]}-{c[1]}" for c in CASES])
def test_transitions_match_zdump(release, zone, y0, y1):
    path = releases.compile(release) / zone
    expected = _zdump_transitions(path, y0, y1)
    assert expected, "oracle produced no transitions; the window or the parser of zdump output is wrong"
    got = _tzif_transitions(path, y0, y1)
    assert got == expected, (
        f"{release} {zone}: tzif != zdump\n  only tzif:  {sorted(got - expected)}\n  only zdump: {sorted(expected - got)}"
    )


@pytest.mark.skipif(ZDUMP is None, reason="zdump not installed")
def test_tehran_2022a_has_the_dst_transitions_that_were_dropped():
    path = releases.compile("2022a") / "Asia/Tehran"
    assert len(_zdump_transitions(path, 2023, 2026)) == 8  # 2 per year × 4 years
    assert len(_tzif_transitions(path, 2023, 2026)) == 8
