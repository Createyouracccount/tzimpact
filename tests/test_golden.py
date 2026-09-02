"""Golden tests: the diff must reproduce what each release's NEWS file claims.

This is the project's trust anchor. If these fail, nothing else matters.
Network-dependent (downloads tzdb releases); skipped when unreachable.
"""

import datetime as dt

import pytest

from tzimpact import releases
from tzimpact.diff import diff

WHEN = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)

# (from, to, expected changed zones) — expectations transcribed from NEWS
CASES = [
    ("2025b", "2025c", set()),  # "Several code changes for compatibility with FreeBSD"
    ("2025c", "2026a", {"Europe/Chisinau", "Europe/Tiraspol"}),  # Moldova
    ("2026a", "2026b", {"America/Vancouver", "Canada/Pacific"}),  # British Columbia
    (
        "2026b",
        "2026c",
        {  # Alberta + Morocco
            "America/Edmonton", "America/Yellowknife", "Canada/Mountain",
            "Africa/Casablanca", "Africa/El_Aaiun",
        },
    ),
]


@pytest.fixture(scope="session")
def network():
    try:
        releases.fetch("2026c")
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"tzdb releases unreachable: {exc}")


@pytest.mark.parametrize("frm,to,expected", CASES)
def test_matches_news(network, frm, to, expected):
    changes = diff(frm, to, start=WHEN, years=5)
    assert {c.zone for c in changes} == expected


def test_alberta_difference_is_winter_only(network):
    """2026b kept Alberta on DST, so summer offsets agree; only winter differs.
    A sampling implementation reports one long window and gets this wrong."""
    changes = [c for c in diff("2026b", "2026c", start=WHEN, years=5) if c.zone == "America/Edmonton"]
    assert len(changes) > 1, "expected discrete winter windows, not one continuous range"
    for c in changes:
        assert c.shift_seconds == 3600
        start_month = dt.datetime.fromtimestamp(c.start_utc, dt.timezone.utc).month
        assert start_month == 11, f"windows should open in November, got month {start_month}"


def test_identical_release_has_no_changes(network):
    assert diff("2026c", "2026c", start=WHEN, years=5) == []
