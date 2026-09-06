#!/usr/bin/env python3
"""Morocco 2026-09-20 demo: what tzdata 2026c silently changes in a bookings table.

Builds a realistic multi-zone appointments database (deterministic), runs
`tzimpact scan --from 2026b --to 2026c`, applies the generated corrections.sql
to a *copy* of the database (this script is the harness; tzimpact itself never
writes), and renders a before/after table using the standard library's
zoneinfo on the compiled 2026b/2026c files. Output goes to files only.

    python docs/demo/make_demo.py --out docs/demo/output
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import random
import shutil
import sqlite3
import subprocess
import sys
import zoneinfo
from collections import Counter

from tzimpact import releases
from tzimpact.scan import to_instant

FROM, TO = "2026b", "2026c"
UTC = dt.timezone.utc
ZONES = [  # (zone, weight) - a Moroccan clinic chain with some remote consults
    ("Africa/Casablanca", 12), ("Africa/El_Aaiun", 2), ("America/Edmonton", 3),
    ("America/Vancouver", 2), ("America/New_York", 3), ("Europe/Berlin", 3),
    ("Europe/London", 3), ("Europe/Madrid", 2), ("Asia/Dubai", 1), ("Asia/Seoul", 1),
]
SERVICES = ["dental check-up", "physio", "eye exam", "consultation", "follow-up", "vaccination"]
FIRST = ["Amina", "Youssef", "Fatima", "Omar", "Khadija", "Hamza", "Salma", "Mehdi", "Nadia", "Karim",
         "Emma", "Liam", "Sophie", "Noah", "Mia", "Lucas", "Jin", "Ayşe", "Ahmed", "Léa"]
LAST = ["Benali", "El Amrani", "Idrissi", "Bouzid", "Tazi", "Alaoui", "Schmidt", "Martin", "Smith",
        "Kim", "Lee", "Garcia", "Müller", "Brown", "Haddad"]


def _tz(version: str, zone: str) -> zoneinfo.ZoneInfo:
    with open(releases.compile(version) / zone, "rb") as f:
        return zoneinfo.ZoneInfo.from_file(f, key=zone)


def build_db(path: pathlib.Path, rows: int, seed: int) -> None:
    rng = random.Random(seed)
    zones, weights = zip(*ZONES)
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE appointments (id INTEGER PRIMARY KEY, patient TEXT, service TEXT, "
        "starts_at TEXT NOT NULL, tz TEXT NOT NULL)"
    )
    start_day = dt.date(2026, 9, 1)
    for i in range(1, rows + 1):
        zone = rng.choices(zones, weights)[0]
        day = start_day + dt.timedelta(days=rng.randrange(0, 480))  # Sep 2026 .. Dec 2027
        hour, minute = rng.choice([8, 9, 10, 11, 12, 14, 15, 16, 17]), rng.choice([0, 15, 30, 45])
        local = dt.datetime(day.year, day.month, day.day, hour, minute)
        # the app stored UTC computed under the rules it had at booking time (tzdata 2026b)
        stored = local.replace(tzinfo=_tz(FROM, zone)).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        conn.execute(
            "INSERT INTO appointments VALUES (?,?,?,?,?)",
            (i, f"{rng.choice(FIRST)} {rng.choice(LAST)}", rng.choice(SERVICES), stored, zone),
        )
    conn.commit()
    conn.close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="docs/demo/output")
    ap.add_argument("--rows", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260920)
    args = ap.parse_args(argv)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    db = out / "clinic.db"
    if db.exists():
        db.unlink()
    build_db(db, args.rows, args.seed)

    # 1. the tool: scan + corrections.sql (read-only)
    sql_path = out / "corrections.sql"
    cmd = [sys.executable, "-m", "tzimpact.cli", "scan", "--from", FROM, "--to", TO, "--sqlite", str(db),
           "--table", "appointments", "--utc-col", "starts_at", "--tz-col", "tz", "--corrections", str(sql_path)]
    run = subprocess.run(cmd, capture_output=True, text=True)
    (out / "scan.txt").write_text("$ tzimpact " + " ".join(cmd[3:]).replace(str(out) + "/", "") + "\n" + run.stdout + run.stderr)
    if run.returncode != 0:
        print(run.stdout, run.stderr, file=sys.stderr)
        return run.returncode

    # 2. the harness: apply to a copy, never to the original
    fixed = out / "clinic.corrected.db"
    shutil.copy(db, fixed)
    conn = sqlite3.connect(fixed)
    conn.executescript(sql_path.read_text())
    conn.commit()
    conn.close()

    # 3. before/after, judged with zoneinfo (independent of tzimpact's parser)
    def rows(p):
        c = sqlite3.connect(p)
        r = c.execute("SELECT id, patient, service, starts_at, tz FROM appointments ORDER BY id").fetchall()
        c.close()
        return r
    before = {r[0]: r for r in rows(db)}
    after = {r[0]: r for r in rows(fixed)}
    table, per_zone, shifts = [], Counter(), {}
    for i, b in before.items():
        a = after[i]
        old_utc, new_utc = to_instant(b[3], False), to_instant(a[3], False)
        zone = b[4]
        intended = dt.datetime.fromtimestamp(old_utc, _tz(FROM, zone)).replace(tzinfo=None)
        broken = dt.datetime.fromtimestamp(old_utc, _tz(TO, zone)).replace(tzinfo=None)
        corrected = dt.datetime.fromtimestamp(new_utc, _tz(TO, zone)).replace(tzinfo=None)
        if old_utc != new_utc or broken != intended:
            shift_h = (new_utc - old_utc) / 3600
            per_zone[zone] += 1
            shifts.setdefault(zone, set()).add(shift_h)
            table.append((i, b[1], b[2], zone, intended, broken, corrected, shift_h))
    lines = [
        f"# tzdata {FROM} -> {TO}: {len(table)} of {len(before)} appointments would silently show the wrong time",
        "",
        "Morocco (Africa/Casablanca, Africa/El_Aaiun) moves to permanent +00 on 2026-09-20; "
        "Alberta (America/Edmonton) to permanent -06 from 2026-11-01 (as modelled in tzdata).",
        "Column *shows after upgrade* is what the unchanged stored instant displays under 2026c; "
        "*after corrections.sql* is the same row after applying the generated file to a copy.",
        "",
        "| zone | affected rows | instant shift |",
        "|---|---:|---|",
    ]
    for zone, n in per_zone.most_common():
        lines.append(f"| {zone} | {n} | {', '.join(f'{s:+.0f}h' for s in sorted(shifts[zone]))} |")
    lines += ["", "| id | patient | service | zone | booked for (2026b) | shows after upgrade (2026c) | after corrections.sql | instant shift |",
              "|---:|---|---|---|---|---|---|---|"]
    for i, patient, service, zone, intended, broken, corrected, shift_h in table:
        lines.append(f"| {i} | {patient} | {service} | {zone} | {intended:%Y-%m-%d %H:%M} | {broken:%Y-%m-%d %H:%M} | {corrected:%Y-%m-%d %H:%M} | {shift_h:+.0f}h |")
    (out / "before_after.md").write_text("\n".join(lines) + "\n")
    summary = {
        "from": FROM, "to": TO, "rows": len(before), "affected": len(table),
        "per_zone": dict(per_zone), "shift_hours": {z: sorted(s) for z, s in shifts.items()},
        "all_corrected_show_intended": all(t[4] == t[6] for t in table),
        "seed": args.seed,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
