"""ICS judge: every DTSTART;TZID event must be classified exactly as the standard
library's zoneinfo (reading the compiled 2026b/2026c files) classifies it.

Independent criterion: an event is affected iff the instant its stated local
time resolved to under the old release displays as a *different* local time
under the new release. Also: nothing is written, and everything that cannot be
assessed is surfaced.
"""

import datetime as dt
import zoneinfo

import pytest

from tzimpact import cli, releases
from tzimpact.diff import diff
from tzimpact.ics import events, scan_ics, scan_ics_report, unfold

FROM, TO = "2026b", "2026c"
WHEN = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)
UTC = dt.timezone.utc


@pytest.fixture(scope="module")
def changes():
    r = diff(FROM, TO, start=WHEN, years=10)
    assert r.unparseable == []
    return r.changes


def _ics_local(ts_local_as_utc: int) -> str:
    return dt.datetime.fromtimestamp(ts_local_as_utc, UTC).strftime("%Y%m%dT%H%M%S")


def _zi(version, zone):
    with open(releases.compile(version) / zone, "rb") as f:
        return zoneinfo.ZoneInfo.from_file(f, key=zone)


@pytest.fixture
def calendar(tmp_path, changes):
    cas = [c for c in changes if c.zone == "Africa/Casablanca"][0]
    edm = [c for c in changes if c.zone == "America/Edmonton"][0]
    cas_start_local = cas.start_utc + cas.old_offset  # local wall time at the window start
    edm_end_local = edm.end_utc + edm.old_offset
    tzid = [
        ("cas-inside", "Africa/Casablanca", "20261001T100000"),
        ("cas-window-start", "Africa/Casablanca", _ics_local(cas_start_local)),   # exactly on the boundary
        ("cas-before", "Africa/Casablanca", _ics_local(cas_start_local - 60)),     # one minute before
        ("edm-winter", "America/Edmonton", "20261215T090000"),
        ("edm-window-end", "America/Edmonton", _ics_local(edm_end_local)),         # exclusive end
        ("edm-last-minute", "America/Edmonton", _ics_local(edm_end_local - 60)),
        ("edm-summer", "America/Edmonton", "20270701T120000"),
        ("nyc", "America/New_York", "20261201T120000"),
        ("berlin-folded", "Europe/Berlin", "20270115T090000"),
    ]
    body = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//tzimpact test//EN"]
    for uid, zone, local in tzid:
        line = f"DTSTART;TZID={zone}:{local}"
        if uid == "berlin-folded":  # RFC 5545 line folding must be handled
            line = line[:20] + "\r\n " + line[20:]
        body += ["BEGIN:VEVENT", f"UID:{uid}", f"SUMMARY:{uid}", line, "END:VEVENT"]
    body += [
        "BEGIN:VEVENT", "UID:utc-z", "DTSTART:20261001T090000Z", "END:VEVENT",
        "BEGIN:VEVENT", "UID:all-day", "DTSTART;VALUE=DATE:20261001", "END:VEVENT",
        "BEGIN:VEVENT", "UID:floating", "DTSTART:20261001T100000", "END:VEVENT",
        "BEGIN:VEVENT", "UID:windows-tzid", "DTSTART;TZID=Morocco Standard Time:20261001T100000", "END:VEVENT",
        "BEGIN:VEVENT", "UID:malformed", "DTSTART;TZID=Africa/Casablanca:2026-10-01 10:00", "END:VEVENT",
        "BEGIN:VEVENT", "UID:no-dtstart", "SUMMARY:nothing", "END:VEVENT",
        "BEGIN:VEVENT", "UID:recurring", "DTSTART;TZID=Africa/Casablanca:20261005T100000",
        "RRULE:FREQ=WEEKLY;COUNT=10", "END:VEVENT",
        "END:VCALENDAR",
    ]
    path = tmp_path / "bookings.ics"
    path.write_text("\r\n".join(body) + "\r\n")
    return path, tzid


def test_unfold_and_events_parse_folded_lines(calendar):
    path, _ = calendar
    evs = events(path.read_text())
    berlin = next(e for e in evs if e["UID"][1] == "berlin-folded")
    assert berlin["DTSTART"] == ({"TZID": "Europe/Berlin"}, "20270115T090000")
    assert len(unfold("A:1\r\n b\r\nC:2")) == 2


def test_ics_matches_zoneinfo_independently(calendar, changes):
    path, tzid = calendar
    known = releases.zones(releases.compile(TO))
    report = scan_ics_report(str(path), changes, FROM, TO, known_zones=known)

    # Independent criterion: the instant the stated local time resolves to (PEP 495
    # fold=0 in both) differs between the releases.
    all_tzid = tzid + [("recurring", "Africa/Casablanca", "20261005T100000")]
    expected_affected = set()
    for uid, zone, local in all_tzid:
        naive = dt.datetime.strptime(local, "%Y%m%dT%H%M%S")
        old_instant = naive.replace(tzinfo=_zi(FROM, zone)).timestamp()
        new_instant = naive.replace(tzinfo=_zi(TO, zone)).timestamp()
        if old_instant != new_instant:
            expected_affected.add(uid)
    # sanity of the oracle itself (the window-end event sits in 2026b's spring-forward gap)
    assert expected_affected == {"cas-inside", "cas-window-start", "edm-winter", "edm-window-end", "edm-last-minute", "recurring"}
    got = {h.row_id for h in report.hits}
    assert got == expected_affected, (got, expected_affected)

    # per-event values agree with zoneinfo at the reported instant
    stated = {u: l for u, _, l in all_tzid}
    for h in report.hits:
        naive = dt.datetime.strptime(stated[h.row_id], "%Y%m%dT%H%M%S")
        old_instant = int(naive.replace(tzinfo=_zi(FROM, h.zone)).timestamp())
        new_instant = int(naive.replace(tzinfo=_zi(TO, h.zone)).timestamp())
        assert h.stored_utc == old_instant and h.stored_utc - h.shift_seconds == new_instant, h
        old_shown = dt.datetime.fromtimestamp(h.stored_utc, _zi(FROM, h.zone)).strftime("%Y-%m-%d %H:%M")
        new_shown = dt.datetime.fromtimestamp(h.stored_utc, _zi(TO, h.zone)).strftime("%Y-%m-%d %H:%M")
        assert (h.old_local, h.new_local) == (old_shown, new_shown), h
        assert h.shift_seconds in (-3600, 3600)

    # everything else is accounted for, nothing silently dropped
    assert report.total == len(tzid) + 7
    assert report.utc_events == 1 and report.all_day_events == 1 and report.recurring_events == 1
    reasons = {u.event_id: u.reason for u in report.unparseable}
    assert set(reasons) == {"floating", "windows-tzid", "malformed", "no-dtstart"}
    assert "floating" in reasons["floating"] and "not a tzdb zone" in reasons["windows-tzid"]
    assert report.total == len(report.hits) + report.utc_events + report.all_day_events + len(report.unparseable) + 4  # 4 assessed, unaffected: cas-before, edm-summer, nyc, berlin-folded


def test_scan_ics_contract(calendar, changes):
    path, _ = calendar
    hits, total = scan_ics(str(path), changes, FROM, TO)
    assert total == 16 and {h.row_id for h in hits} >= {"cas-inside", "edm-winter"}


def test_cli_ics_is_read_only_and_loud(calendar, tmp_path, capsys, monkeypatch):
    path, _ = calendar
    monkeypatch.chdir(tmp_path)
    before = path.read_bytes()
    rc = cli.main(["scan", "--from", FROM, "--to", TO, "--ics", str(path)])
    out, err = capsys.readouterr()
    assert rc == 2, "unassessable events must not yield a success exit code"
    assert "NOT covered" in err and "floating" in err and "windows-tzid" in err
    assert "cas-inside" in out and "read-only" in out and "recurrences are not expanded" in out
    assert path.read_bytes() == before, ".ics must not be rewritten"
    assert not (tmp_path / "corrections.sql").exists(), "no SQL for a calendar"


def test_cli_ics_clean_file_exits_zero(tmp_path, capsys):
    path = tmp_path / "clean.ics"
    path.write_text("BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nUID:a\r\nDTSTART;TZID=Africa/Casablanca:20261001T100000\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
    rc = cli.main(["scan", "--from", FROM, "--to", TO, "--ics", str(path)])
    out, err = capsys.readouterr()
    assert rc == 0 and "1 events affected" in out and err == ""


def test_cli_ics_rejects_table_flags(tmp_path, capsys):
    path = tmp_path / "x.ics"; path.write_text("BEGIN:VCALENDAR\r\nEND:VCALENDAR\r\n")
    rc = cli.main(["scan", "--from", FROM, "--to", TO, "--ics", str(path), "--table", "t"])
    assert rc == 1 and "do not apply" in capsys.readouterr().err
