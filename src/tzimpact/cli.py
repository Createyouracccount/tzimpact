"""tzimpact CLI."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from . import corrections as corr
from . import dataset, releases
from .diff import DiffResult, diff
from .ics import scan_ics_report
from .scan import index_changes, scan_postgres, scan_sqlite

EXIT_INCOMPLETE = 2  # some zones could not be compared; the answer is not complete


def _fmt_ts(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _fmt(ts: int | None) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d") if ts else "open"


def _warn_incomplete(result: DiffResult) -> None:
    """Loud, on stderr, and reflected in the exit code: never a silent 'no change'."""
    if not result.unparseable:
        return
    n = len(result.unparseable)
    print(
        f"WARNING: {n} zone{'s' if n != 1 else ''} could not be parsed and {'are' if n != 1 else 'is'} "
        "NOT covered by this result:",
        file=sys.stderr,
    )
    for u in result.unparseable:
        print(f"  {u.zone}: {u.error}", file=sys.stderr)


def cmd_diff(args) -> int:
    result = diff(args.from_version, args.to_version, years=args.years)
    changes = result.changes
    if args.json:
        json.dump(
            {
                "from": args.from_version,
                "to": args.to_version,
                "changes": [c.as_dict() for c in changes],
                "unparseable": [u.as_dict() for u in result.unparseable],
            },
            sys.stdout,
            indent=2,
        )
        print()
        _warn_incomplete(result)
        return EXIT_INCOMPLETE if result.unparseable else 0
    zones = sorted({c.zone for c in changes})
    if not zones:
        print(f"{args.from_version} -> {args.to_version}: no future offsets changed")
        _warn_incomplete(result)
        return EXIT_INCOMPLETE if result.unparseable else 0
    print(f"{len(zones)} zones changed for future instants ({args.from_version} -> {args.to_version}):")
    for z in zones:
        cs = [c for c in changes if c.zone == z]
        first, last = cs[0], cs[-1]
        shift = first.shift_seconds / 3600
        print(
            f"  {z:28} {_fmt(first.start_utc)} .. {_fmt(last.end_utc)}  "
            f"{first.old_offset/3600:+.0f}h -> {first.new_offset/3600:+.0f}h "
            f"({shift:+.0f}h, {len(cs)} window{'s' if len(cs) != 1 else ''})"
        )
    _warn_incomplete(result)
    return EXIT_INCOMPLETE if result.unparseable else 0


def _scan_ics(args, result: DiffResult) -> int:
    """Read-only: reports affected events, writes nothing (there is no SQL for a file)."""
    known = releases.zones(releases.compile(args.to_version))
    report = scan_ics_report(args.ics, result.changes, args.from_version, args.to_version, known_zones=known)
    print(f"{args.ics}: {report.total:,} events scanned")
    print(
        f"  {len(report.hits):,} events affected"
        + (f" ({len(report.hits) / report.total * 100:.1f}%)" if report.total else "")
    )
    for h in report.hits:
        print(
            f"    {h.zone:26} {str(h.row_id)[:40]:40} local {h.old_local}  "
            f"instant {_fmt_ts(h.stored_utc)} under {args.from_version} -> "
            f"{_fmt_ts(h.stored_utc - h.shift_seconds)} under {args.to_version}"
        )
    print(
        f"  not affected by definition: {report.utc_events} UTC (Z) events, {report.all_day_events} all-day events"
    )
    if report.recurring_events:
        print(f"  {report.recurring_events} recurring events: only DTSTART assessed, recurrences are not expanded")
    print("  read-only: tzimpact does not rewrite .ics files; no corrections file is produced for a calendar")
    incomplete = bool(report.unparseable or result.unparseable)
    if report.unparseable:
        n = len(report.unparseable)
        print(f"WARNING: {n} event{'s' if n != 1 else ''} could not be assessed and {'are' if n != 1 else 'is'} NOT covered:", file=sys.stderr)
        for u in report.unparseable:
            print(f"  {u.event_id}: {u.reason}", file=sys.stderr)
    _warn_incomplete(result)
    return EXIT_INCOMPLETE if incomplete else 0


def cmd_scan(args) -> int:
    result = diff(args.from_version, args.to_version, years=args.years)
    if args.ics:
        if args.table or args.utc_col or args.tz_col:
            print("--ics scans DTSTART;TZID events; --table/--utc-col/--tz-col do not apply", file=sys.stderr)
            return 1
        return _scan_ics(args, result)
    if not (args.table and args.utc_col and args.tz_col):
        print("--table, --utc-col and --tz-col are required with --sqlite/--pg", file=sys.stderr)
        return 1
    if args.pg:
        hits, total = scan_postgres(args.pg, args.table, args.id_col, args.utc_col, args.tz_col, result.changes)
    else:
        hits, total = scan_sqlite(args.sqlite, args.table, args.id_col, args.utc_col, args.tz_col, result.changes)
    print(f"{args.table}: {total:,} rows scanned")
    print(f"  {len(hits):,} rows affected ({len(hits)/total*100:.1f}%)" if total else "  empty")
    from collections import Counter

    for z, n in Counter(h.zone for h in hits).most_common():
        sh = next(h.shift_seconds for h in hits if h.zone == z) / 3600
        print(f"    {z:26} {n:>7,} rows   {sh:+.0f}h")
    if hits:
        e = min(hits, key=lambda h: h.stored_utc)
        print(f"  earliest affected: row {e.row_id} in {e.zone}")
        print(f"    was {e.old_local}  ->  now {e.new_local}")
    fixes, reviews = corr.plan(hits, args.to_version, semantics=args.semantics)
    sql = corr.render_sql(
        fixes, reviews, table=args.table, id_col=args.id_col, utc_col=args.utc_col, tz_col=args.tz_col,
        from_version=args.from_version, to_version=args.to_version, semantics=args.semantics, affected=hits,
    )
    with open(args.corrections, "w", encoding="utf-8") as f:
        f.write(sql)
    if args.semantics == corr.INSTANT:
        print(f"  -> {args.corrections}: instant semantics, no corrections (stored instants are kept)")
    else:
        print(
            f"  -> corrections written to {args.corrections} "
            f"({len(fixes)} UPDATE, {len(reviews)} manual review) - review before applying"
        )
        print(
            "  ONE-SHOT: scan once per release upgrade. Do not scan again after applying the file: "
            "corrected rows are re-detected and a regenerated file would move them a second time."
        )
    _warn_incomplete(result)
    return EXIT_INCOMPLETE if result.unparseable else 0


def cmd_dataset(args) -> int:
    import pathlib

    versions = releases.list_releases(since=args.from_version)
    if args.to_version:
        versions = [v for v in versions if v <= args.to_version]
    if len(versions) < 2:
        print(f"need at least two releases from {args.from_version}; got {versions}", file=sys.stderr)
        return 1
    written = dataset.write_all(versions, pathlib.Path(args.out))
    print(f"wrote {len(written)} pair files + index.json to {args.out} ({versions[0]} .. {versions[-1]})")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tzimpact", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("diff", help="which zones changed for future instants")
    # positional for the short form, --from/--to to match `scan` and `dataset`
    d.add_argument("from_version", nargs="?", metavar="FROM")
    d.add_argument("to_version", nargs="?", metavar="TO")
    d.add_argument("--from", dest="from_flag", metavar="FROM")
    d.add_argument("--to", dest="to_flag", metavar="TO")
    d.add_argument("--years", type=int, default=10)
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_diff)

    s = sub.add_parser("scan", help="which stored rows are affected")
    s.add_argument("--from", dest="from_version", required=True)
    s.add_argument("--to", dest="to_version", required=True)
    src = s.add_mutually_exclusive_group(required=True)
    src.add_argument("--sqlite", help="path to a SQLite database")
    src.add_argument("--pg", metavar="DSN", help="Postgres DSN, e.g. postgresql://user:pw@host/db (needs tzimpact[postgres])")
    src.add_argument("--ics", metavar="PATH", help="an iCalendar file; DTSTART;TZID events are assessed (read-only)")
    s.add_argument("--table", help="(--sqlite/--pg) table to scan")
    s.add_argument("--id-col", default="id")
    s.add_argument("--utc-col", help="(--sqlite/--pg) column holding the stored UTC instant")
    s.add_argument("--tz-col", help="(--sqlite/--pg) column holding the IANA zone name")
    s.add_argument("--years", type=int, default=10)
    s.add_argument(
        "--semantics", choices=corr.SEMANTICS, default=corr.WALL_CLOCK,
        help="wall-clock (default): rows keep the local time they were booked for, the stored instant moves; "
             "instant: stored instants are correct, only their displayed local time changes (no UPDATEs)",
    )
    s.add_argument("--corrections", default="corrections.sql", help="where to write the SQL (never executed)")
    s.set_defaults(func=cmd_scan)

    ds = sub.add_parser("dataset", help="write tzimpact-data JSON for every consecutive release pair")
    ds.add_argument("--from", dest="from_version", default="2020a")
    ds.add_argument("--to", dest="to_version", default=None, help="last release to include (default: newest on IANA)")
    ds.add_argument("--out", default="data")
    ds.set_defaults(func=cmd_dataset)

    args = p.parse_args(argv)
    if args.func is cmd_diff:
        for name in ("from", "to"):
            flag, pos = getattr(args, f"{name}_flag"), getattr(args, f"{name}_version")
            if flag and pos:
                p.error(f"--{name} and the positional {name.upper()} are the same argument; give one")
            setattr(args, f"{name}_version", flag or pos)
        missing = [n.upper() for n in ("from", "to") if not getattr(args, f"{n}_version")]
        if missing:
            p.error(f"diff needs {' and '.join(missing)} (positional or --from/--to)")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
