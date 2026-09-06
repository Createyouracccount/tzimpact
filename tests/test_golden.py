"""Golden tests: the diff must reproduce what each release's NEWS file claims.

This is the project's trust anchor. If these fail, nothing else matters.
Network-dependent (downloads tzdb releases); skipped only when the network is
unreachable — every other failure must fail the run (see conftest.py guard).

Every consecutive release pair from 2020a to 2026c is covered. For each pair,
``expected`` is transcribed from the *to* release's NEWS entry ("Changes to
future timestamps" and "Changes to past and future timestamps", plus past
entries whose corrected rule persists into the future), restricted to changes
that fall inside the diff window: the release date and the ten years after it.
Region names in NEWS were mapped to zone names via the release's own source
files (Rule/Zone lines), never guessed. Zone names are compared after
resolving ``Link`` aliases of the *to* release, so NEWS's canonical names
(America/Edmonton) match the diff's aliases (Canada/Mountain).

Zones that are *new* in the *to* release (America/Coyhaique in 2025b,
America/Ciudad_Juarez in 2022g) cannot appear in a diff of common zones and are
therefore excluded from ``expected``.
"""

import datetime as dt
import socket
import urllib.error

import pytest

from tzimpact import releases
from tzimpact.diff import diff

pytestmark = pytest.mark.golden

WHEN = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)
YEARS = 10

# (from, to, to-release date, expected canonical zones, NEWS note)
CASES = [
    ("2020a", "2020b", "2020-10-06",
     {"Africa/Casablanca", "Africa/El_Aaiun", "Antarctica/Casey", "Antarctica/Macquarie"},
     "Morocco post-Ramadan prediction (first altered 2023); Casey +11 from 2020-10-04; Macquarie in sync with Tasmania"),
    ("2020b", "2020c", "2020-10-16", {"Pacific/Fiji"}, "Fiji DST starts 2020-12-20 not 11-08"),
    ("2020c", "2020d", "2020-10-21", {"Asia/Gaza", "Asia/Hebron"}, "Palestine ends DST 10-24; future Sat-before-last-Sunday rule"),
    ("2020d", "2020e", "2020-12-22", {"Europe/Volgograd"}, "Volgograd +04 -> +03 on 2020-12-27"),
    ("2020e", "2020f", "2020-12-29", set(), "build procedure only"),
    ("2020f", "2021a", "2021-01-24", {"Africa/Juba"}, "South Sudan +03 -> +02 on 2021-02-01"),
    ("2021a", "2021b", "2021-09-24", {"Asia/Amman", "Pacific/Apia"}, "Jordan DST from Feb last Thursday; Samoa no DST"),
    ("2021b", "2021c", "2021-10-01", set(), "Link directives only"),
    ("2021c", "2021d", "2021-10-15", {"Pacific/Fiji"}, "Fiji suspends DST 2021/2022"),
    ("2021d", "2021e", "2021-10-21", {"Asia/Gaza", "Asia/Hebron"}, "Palestine falls back 10-29 not 10-30"),
    ("2021e", "2022a", "2022-03-15", {"Asia/Gaza", "Asia/Hebron"}, "Palestine springs 03-27; new prediction rules"),
    ("2022a", "2022b", "2022-08-10", {"America/Santiago", "Pacific/Easter", "Asia/Tehran"},
     "Chile DST start delayed to 09-11 (Rule Chile: Santiago, Easter); Iran stops DST after 2022-09-21"),
    ("2022b", "2022c", "2022-08-15", set(), "code only"),
    ("2022c", "2022d", "2022-09-23", {"Asia/Gaza", "Asia/Hebron"}, "Palestine 02:00 first Saturday on/after Mar 24 / Oct 24"),
    ("2022d", "2022e", "2022-10-11", {"Asia/Amman", "Asia/Damascus"}, "Jordan and Syria permanent +03"),
    ("2022e", "2022f", "2022-10-28",
     {"America/Bahia_Banderas", "America/Chihuahua", "America/Mazatlan", "America/Merida",
      "America/Mexico_City", "America/Monterrey", "America/Ojinaga", "Pacific/Fiji"},
     "Mexico ends DST (Rule Mexico users + Chihuahua/Ojinaga to fixed -06; Tijuana/Matamoros keep US rules); Fiji DST suspended"),
    ("2022f", "2022g", "2022-11-29", {"America/Ojinaga", "America/Nuuk"},
     "Ojinaga observes US DST from 2023 (Ciudad_Juarez is a new zone, not diffable); Nuuk stays -02 after 2023-03-25"),
    ("2022g", "2023a", "2023-03-22",
     {"Africa/Cairo", "Africa/Casablanca", "Africa/El_Aaiun", "Asia/Gaza", "Asia/Hebron", "America/Nuuk"},
     "Egypt DST from 2023; Morocco 2023 spring-forward Apr 23; Palestine Ramadan delay; Nuuk -02/-01 from 2023-10-29"),
    ("2023a", "2023b", "2023-03-23", {"Asia/Beirut"}, "Lebanon springs forward Apr 20/21"),
    ("2023b", "2023c", "2023-03-28", {"Asia/Beirut"}, "Lebanon reverted to 2023a data"),
    ("2023c", "2023d", "2023-12-21", {"America/Scoresbysund", "Antarctica/Vostok", "Antarctica/Casey"},
     "Ittoqqortoormiit -02/-01 from 2024-03-31; Vostok +05 from 2023-12-18; Casey +08 (Palestine 2072-2075 fix is outside the 10-year window)"),
    ("2023d", "2024a", "2024-02-01", {"Asia/Almaty", "Asia/Qostanay", "Asia/Gaza", "Asia/Hebron"},
     "Kazakhstan unifies on +05 from 2024-03-01; Palestine second Saturday after Ramadan"),
    ("2024a", "2024b", "2024-09-04", set(), "past timestamps only (Choibalsan alias, Mexico/Portugal history)"),
    ("2024b", "2025a", "2025-01-15", {"America/Asuncion"}, "Paraguay permanent -03 (timestamps from 2025-03-22)"),
    ("2025a", "2025b", "2025-03-22", set(), "Aysen becomes new zone America/Coyhaique (not diffable); Santiago unchanged"),
    ("2025b", "2025c", "2025-12-10", set(), "past timestamps only (Baja California 1953-1975)"),
    ("2025c", "2026a", "2026-03-01", {"Europe/Chisinau"}, "Moldova uses EU transition times (Tiraspol is a link)"),
    ("2026a", "2026b", "2026-04-22", {"America/Vancouver"}, "British Columbia permanent -07 (modelled 2026-11-01)"),
    ("2026b", "2026c", "2026-07-08", {"America/Edmonton", "Africa/Casablanca", "Africa/El_Aaiun"},
     "Alberta permanent -06 (modelled 2026-11-01; Yellowknife/Canada/Mountain are links); Morocco permanent +00 from 2026-09-20"),
]

# Only a genuine network failure may skip the golden suite. Anything else
# (zic failure, TZif parse error, corrupt cache, HTTP 4xx/5xx for a known
# release) is a real failure and must surface as such.
NETWORK_ERRORS = (urllib.error.URLError, ConnectionError, TimeoutError, socket.gaierror)


def _versions_under_test() -> list[str]:
    return sorted({v for case in CASES for v in case[:2]})


@pytest.fixture(scope="session")
def network():
    for version in _versions_under_test():
        try:
            releases.fetch(version)
        except urllib.error.HTTPError:
            raise  # the release exists; an HTTP error is not "unreachable"
        except NETWORK_ERRORS as exc:
            pytest.skip(f"tzdb releases unreachable: {exc!r}")


def _link_map(version: str) -> dict[str, str]:
    """name -> target for every ``Link`` line in the release's compiled region files."""
    src = releases.fetch(version)
    links: dict[str, str] = {}
    for region in releases.REGIONS:
        f = src / region
        if not f.exists():
            continue
        for line in f.read_text(errors="replace").splitlines():
            line = line.split("#", 1)[0].strip()
            parts = line.split()
            if len(parts) >= 3 and parts[0] == "Link":
                links[parts[2]] = parts[1]
    return links


def _canonical(zone: str, links: dict[str, str]) -> str:
    seen = set()
    while zone in links and zone not in seen:
        seen.add(zone)
        zone = links[zone]
    return zone


@pytest.mark.parametrize("frm,to,date,expected,note", CASES, ids=[f"{c[0]}-{c[1]}" for c in CASES])
def test_matches_news(network, frm, to, date, expected, note):
    when = dt.datetime.fromisoformat(date).replace(tzinfo=dt.timezone.utc)
    links = _link_map(to)
    result = diff(frm, to, start=when, years=YEARS)
    assert result.unparseable == [], f"{frm}->{to}: zones NOT compared: {result.unparseable}"
    found = {_canonical(c.zone, links) for c in result.changes}
    assert found == expected, (
        f"{frm}->{to} ({note})\n  diff finds: {sorted(found)}\n  NEWS says:  {sorted(expected)}"
    )


def test_alberta_difference_is_winter_only(network):
    """2026b kept Alberta on DST, so summer offsets agree; only winter differs.
    A sampling implementation reports one long window and gets this wrong."""
    changes = [c for c in diff("2026b", "2026c", start=WHEN, years=5).changes if c.zone == "America/Edmonton"]
    assert len(changes) > 1, "expected discrete winter windows, not one continuous range"
    for c in changes:
        assert c.shift_seconds == 3600
        start_month = dt.datetime.fromtimestamp(c.start_utc, dt.timezone.utc).month
        assert start_month == 11, f"windows should open in November, got month {start_month}"


def test_identical_release_has_no_changes(network):
    assert diff("2026c", "2026c", start=WHEN, years=5).changes == []
