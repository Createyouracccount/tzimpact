"""tzimpact CLI."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from .diff import DiffResult, diff
from .scan import index_changes, scan_sqlite

EXIT_INCOMPLETE = 2  # some zones could not be compared; the answer is not complete


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


def cmd_scan(args) -> int:
    result = diff(args.from_version, args.to_version, years=args.years)
    hits, total = scan_sqlite(
        args.sqlite, args.table, args.id_col, args.utc_col, args.tz_col, result.changes
    )
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
    _warn_incomplete(result)
    return EXIT_INCOMPLETE if result.unparseable else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tzimpact", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("diff", help="which zones changed for future instants")
    d.add_argument("from_version")
    d.add_argument("to_version")
    d.add_argument("--years", type=int, default=10)
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_diff)

    s = sub.add_parser("scan", help="which stored rows are affected")
    s.add_argument("--from", dest="from_version", required=True)
    s.add_argument("--to", dest="to_version", required=True)
    s.add_argument("--sqlite", required=True)
    s.add_argument("--table", required=True)
    s.add_argument("--id-col", default="id")
    s.add_argument("--utc-col", required=True)
    s.add_argument("--tz-col", required=True)
    s.add_argument("--years", type=int, default=10)
    s.set_defaults(func=cmd_scan)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
