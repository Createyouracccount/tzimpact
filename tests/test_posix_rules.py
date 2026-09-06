"""POSIX TZ rule forms: Mm.w.d, Jn (leap day never counted), n (leap day counted).

These are the three date forms POSIX.1 allows in a TZ string. tzdb emits Jn for
zones whose transitions fall on fixed calendar dates (Iran: 'J79/24,J263/24'),
which the parser used to reject — and the diff used to drop the zone silently.
"""

import datetime as dt

import pytest

from tzimpact import tzif
from tzimpact.tzif import JulianRule, MonthWeekDayRule, ZeroBasedJulianRule


def _utc(y, m, d, hh=0, mm=0):
    return int(dt.datetime(y, m, d, hh, mm, tzinfo=dt.timezone.utc).timestamp())


@pytest.mark.parametrize(
    "text,expected",
    [
        ("M3.2.0", MonthWeekDayRule(3, 2, 0, 7200)),
        ("M11.1.0/2:00", MonthWeekDayRule(11, 1, 0, 7200)),
        ("M10.5.0/3", MonthWeekDayRule(10, 5, 0, 10800)),
        ("M3.5.0/-2", MonthWeekDayRule(3, 5, 0, -7200)),
        ("J79/24", JulianRule(79, 86400)),
        ("J263/24", JulianRule(263, 86400)),
        ("J1", JulianRule(1, 7200)),
        ("J365/0", JulianRule(365, 0)),
        ("0", ZeroBasedJulianRule(0, 7200)),
        ("59/1:30", ZeroBasedJulianRule(59, 5400)),
        ("365", ZeroBasedJulianRule(365, 7200)),
    ],
)
def test_parse_rule_forms(text, expected):
    assert tzif._parse_rule(text) == expected


@pytest.mark.parametrize("text", ["J0", "J366", "366", "M13.1.0", "M3.6.0", "M3.1.7", "M3.1", "X5", ""])
def test_parse_rule_rejects_out_of_range_and_unknown(text):
    with pytest.raises(ValueError):
        tzif._parse_rule(text)


def test_parse_posix_iran_footer():
    p = tzif.parse_posix("<+0330>-3:30<+0430>,J79/24,J263/24")
    assert p.std_offset == 12600 and p.dst_offset == 16200
    assert p.start == JulianRule(79, 86400) and p.end == JulianRule(263, 86400)


def test_parse_posix_refuses_dst_name_without_rules():
    with pytest.raises(ValueError):
        tzif.parse_posix("EST5EDT")
    with pytest.raises(ValueError):
        tzif.parse_posix("EST5EDT,M3.2.0")


def test_julian_rule_skips_february_29():
    """J60 is March 1 in every year; J59 is February 28 in every year."""
    for year in (2023, 2024):  # 2024 is a leap year
        assert JulianRule(60, 0).transition_utc(year, 0) == _utc(year, 3, 1)
        assert JulianRule(59, 0).transition_utc(year, 0) == _utc(year, 2, 28)
        assert JulianRule(365, 0).transition_utc(year, 0) == _utc(year, 12, 31)


def test_zero_based_julian_counts_february_29():
    """Day 59 is February 29 in a leap year and March 1 otherwise."""
    assert ZeroBasedJulianRule(59, 0).transition_utc(2024, 0) == _utc(2024, 2, 29)
    assert ZeroBasedJulianRule(59, 0).transition_utc(2023, 0) == _utc(2023, 3, 1)
    assert ZeroBasedJulianRule(0, 0).transition_utc(2023, 0) == _utc(2023, 1, 1)


def test_iran_rule_matches_its_known_transitions():
    """J79/24 with UTC+3:30 before: 2023-03-21 24:00 local = 2023-03-21 20:30 UTC;
    J263/24 with UTC+4:30 before: 2023-09-20 24:00 local = 2023-09-20 19:30 UTC.
    (2023 is not a leap year, so J79 = March 20 and J263 = September 20.)"""
    start, end = JulianRule(79, 86400), JulianRule(263, 86400)
    assert start.transition_utc(2023, 12600) == _utc(2023, 3, 20, 20, 30)
    assert end.transition_utc(2023, 16200) == _utc(2023, 9, 20, 19, 30)
    # leap year 2024: J79 is still March 20 (Feb 29 not counted)
    assert start.transition_utc(2024, 12600) == _utc(2024, 3, 20, 20, 30)


def test_month_week_day_rule_unchanged():
    """US rules must still resolve exactly as before the refactor."""
    assert MonthWeekDayRule(3, 2, 0, 7200).transition_utc(2026, -5 * 3600) == _utc(2026, 3, 8, 7)
    assert MonthWeekDayRule(11, 1, 0, 7200).transition_utc(2026, -4 * 3600) == _utc(2026, 11, 1, 6)
