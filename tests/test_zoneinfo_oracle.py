"""Independent oracle #2: for every zone file of every release under test, the
offset tzif.read() computes must equal what the standard library's zoneinfo
computes from the same bytes, at monthly instants across the 2020-2036 window.

The zdump oracle checks four hand-picked zones. This one checks all of them,
because the defect it was written after (a DST offset of exactly zero treated
as "no DST") lived in three zones - Atlantic/Azores, Europe/Dublin and the
pre-2023d America/Scoresbysund - that no hand-picked list contained. The golden
suite did not see it either: it compares changed-zone *sets*, and Azores and
Dublin never changed, while Scoresbysund's winter windows kept it in the set.
"""

import datetime as dt
import hashlib
import pathlib
import socket
import urllib.error
from zoneinfo import ZoneInfo

import pytest

from tzimpact import releases, tzif

RELEASES = [
    "2020a", "2020b", "2020c", "2020d", "2020e", "2020f",
    "2021a", "2021b", "2021c", "2021d", "2021e",
    "2022a", "2022b", "2022c", "2022d", "2022e", "2022f", "2022g",
    "2023a", "2023b", "2023c", "2023d",
    "2024a", "2024b",
    "2025a", "2025b", "2025c",
    "2026a", "2026b", "2026c",
]
PROBES = [
    int(dt.datetime(y, m, 15, 12, tzinfo=dt.timezone.utc).timestamp())
    for y in range(2020, 2037)
    for m in range(1, 13)
]


NETWORK_ERRORS = (urllib.error.URLError, ConnectionError, TimeoutError, socket.gaierror)


@pytest.fixture(scope="module")
def network():
    """Skip only when IANA is unreachable; any other failure is a real failure."""
    for version in RELEASES:
        try:
            releases.fetch(version)
        except urllib.error.HTTPError:
            raise
        except NETWORK_ERRORS as exc:
            pytest.skip(f"tzdb releases unreachable: {exc!r}")


def _zone_files(root: pathlib.Path):
    for f in sorted(root.rglob("*")):
        if f.is_file() and f.read_bytes()[:4] == b"TZif":
            yield f


@pytest.mark.parametrize("release", RELEASES)
def test_offsets_match_zoneinfo_for_every_zone(release, network):
    root = releases.compile(release)
    seen: dict[str, str | None] = {}
    mismatches = []
    checked = 0
    for f in _zone_files(root):
        zone = str(f.relative_to(root))
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        if digest in seen:  # links are byte-identical copies; report, do not recompute
            if seen[digest]:
                mismatches.append(f"{zone}: {seen[digest]}")
            continue
        ours = tzif.read(str(f))
        theirs = ZoneInfo.from_file(open(f, "rb"), key=zone)
        checked += 1
        first = None
        for t in PROBES:
            want = int(theirs.utcoffset(dt.datetime.fromtimestamp(t, dt.timezone.utc)).total_seconds())
            got = ours.offset_at(t)
            if got != want:
                first = f"{dt.datetime.fromtimestamp(t, dt.timezone.utc):%Y-%m-%d} tzif={got} zoneinfo={want}"
                break
        seen[digest] = first
        if first:
            mismatches.append(f"{zone}: {first}")
    assert checked > 300, f"{release}: only {checked} distinct zone files - compile output looks incomplete"
    assert not mismatches, f"{release}: {len(mismatches)} zone(s) disagree with zoneinfo:\n  " + "\n  ".join(mismatches)
