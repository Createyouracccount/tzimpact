"""Parser correctness against the system zoneinfo, which Python already trusts."""

import datetime as dt
import zoneinfo

import pytest

from tzimpact import tzif

SYSTEM = "/usr/share/zoneinfo"
ZONES = [
    "America/New_York", "America/Edmonton", "Europe/Berlin", "Asia/Seoul",
    "Africa/Casablanca", "Australia/Sydney", "Pacific/Auckland", "UTC",
    "Asia/Kolkata", "America/Sao_Paulo", "Europe/Dublin", "Asia/Tehran",
]
# every 37 days for 12 years: crosses DST edges in both hemispheres
INSTANTS = [
    dt.datetime(2026, 1, 1, 3, 17, tzinfo=dt.timezone.utc) + dt.timedelta(days=37 * i)
    for i in range(120)
]


@pytest.mark.parametrize("zone", ZONES)
def test_offsets_match_zoneinfo(zone):
    parsed = tzif.read(f"{SYSTEM}/{zone}")
    ref = zoneinfo.ZoneInfo(zone)
    for when in INSTANTS:
        expected = int(when.astimezone(ref).utcoffset().total_seconds())
        assert parsed.offset_at(int(when.timestamp())) == expected, f"{zone} @ {when}"


@pytest.mark.parametrize("zone", ["America/New_York", "Europe/Berlin", "Australia/Sydney"])
def test_rule_transitions_land_on_real_changes(zone):
    """Every boundary the parser reports must be an instant where the offset
    actually changes — otherwise the diff would emit phantom windows."""
    parsed = tzif.read(f"{SYSTEM}/{zone}")
    start = int(dt.datetime(2030, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    end = int(dt.datetime(2036, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    bounds = parsed.boundaries(start, end)
    assert bounds, f"{zone} should still transition after the explicit table ends"
    for b in bounds:
        assert parsed.offset_at(b - 1) != parsed.offset_at(b), f"{zone} phantom boundary at {b}"
