"""Round trip on a real Postgres (throwaway Docker container, psql applies the file).

This judge does not skip: if Docker or psycopg is unavailable it FAILS with a
clear message (gate A lesson: a skipped judge is a green lie).
"""

import datetime as dt
import shutil
import subprocess
import time
import zoneinfo

import pytest

from tzimpact import cli, releases
from tzimpact.diff import diff
from tzimpact.scan import scan_postgres, to_instant

FROM, TO = "2026b", "2026c"
WHEN = dt.datetime(2026, 8, 30, tzinfo=dt.timezone.utc)
UTC = dt.timezone.utc
IMAGE = "postgres:16-alpine"


@pytest.fixture(scope="module")
def pg():
    """(dsn, container id). Fails loudly when the judge cannot run."""
    try:
        import psycopg
    except ImportError:
        pytest.fail("Postgres judge unavailable: psycopg not installed (pip install 'tzimpact[postgres]')")
    if shutil.which("docker") is None:
        pytest.fail("Postgres judge unavailable: docker not installed")
    run = subprocess.run(
        ["docker", "run", "-d", "--rm", "-e", "POSTGRES_PASSWORD=tz", "-p", "127.0.0.1::5432", IMAGE],
        capture_output=True, text=True,
    )
    if run.returncode != 0:
        pytest.fail(f"Postgres judge unavailable: docker run failed: {run.stderr.strip()}")
    cid = run.stdout.strip()
    try:
        port = subprocess.run(["docker", "port", cid, "5432/tcp"], capture_output=True, text=True, check=True).stdout
        port = port.strip().splitlines()[0].rsplit(":", 1)[1]
        dsn = f"postgresql://postgres:tz@127.0.0.1:{port}/postgres"
        deadline = time.time() + 90
        last = None
        while time.time() < deadline:
            try:
                with psycopg.connect(dsn, connect_timeout=3) as conn:
                    conn.execute("SELECT 1")
                break
            except Exception as exc:  # container still starting
                last = exc
                time.sleep(1)
        else:
            pytest.fail(f"Postgres judge unavailable: container never became ready: {last!r}")
        yield dsn, cid
    finally:
        subprocess.run(["docker", "rm", "-f", cid], capture_output=True)


def _psql(cid: str, sql: str) -> None:
    subprocess.run(
        ["docker", "exec", "-i", cid, "psql", "-U", "postgres", "-q", "-v", "ON_ERROR_STOP=1"],
        input=sql, text=True, check=True, capture_output=True,
    )


def _rows(dsn, table):
    import psycopg

    with psycopg.connect(dsn) as conn:
        return conn.execute(f'SELECT id, starts_at, tz FROM "{table}" ORDER BY id').fetchall()


def _local(zi, zone, ts):
    with open(zi / zone, "rb") as f:
        return dt.datetime.fromtimestamp(ts, zoneinfo.ZoneInfo.from_file(f, key=zone)).replace(tzinfo=None)


COLUMN_TYPES = {
    "appt_tz": "timestamptz",
    "appt_epoch": "bigint",
    "appt_naive": "timestamp",  # without time zone: read as UTC
}


@pytest.mark.parametrize("table", list(COLUMN_TYPES))
def test_round_trip_postgres(pg, table, tmp_path):
    import psycopg

    dsn, cid = pg
    changes = diff(FROM, TO, start=WHEN, years=10).changes
    cas = [c for c in changes if c.zone == "Africa/Casablanca"]
    edm = [c for c in changes if c.zone == "America/Edmonton"]
    c0, e0 = cas[0], edm[0]
    instants = [
        (1, c0.start_utc + 6 * 3600, "Africa/Casablanca", True),
        (2, c0.start_utc, "Africa/Casablanca", True),
        (3, c0.start_utc - 1, "Africa/Casablanca", False),
        (4, e0.start_utc + 12 * 3600, "America/Edmonton", True),
        (5, e0.end_utc, "America/Edmonton", False),
        (6, e0.end_utc - 1, "America/Edmonton", True),
        (7, int(dt.datetime(2027, 7, 1, 12, tzinfo=UTC).timestamp()), "America/Edmonton", False),
        (8, int(dt.datetime(2026, 12, 1, 12, tzinfo=UTC).timestamp()), "America/New_York", False),
    ]
    coltype = COLUMN_TYPES[table]

    def cell(ts):
        if coltype == "bigint":
            return ts
        d = dt.datetime.fromtimestamp(ts, UTC)
        return d if coltype == "timestamptz" else d.replace(tzinfo=None)

    with psycopg.connect(dsn) as conn:
        conn.execute(f'DROP TABLE IF EXISTS "{table}"')
        conn.execute(f'CREATE TABLE "{table}" (id integer PRIMARY KEY, starts_at {coltype}, tz text)')
        with conn.cursor() as cur:
            cur.executemany(f'INSERT INTO "{table}" VALUES (%s, %s, %s)', [(i, cell(ts), z) for i, ts, z, _ in instants])
        conn.commit()
    expected = {i: aff for i, _, _, aff in instants}
    before = {r[0]: r for r in _rows(dsn, table)}

    hits, total = scan_postgres(dsn, table, "id", "starts_at", "tz", changes)
    assert total == len(instants)
    assert {h.row_id for h in hits} == {i for i, a in expected.items() if a}

    sql_path = tmp_path / f"{table}.sql"
    rc = cli.main(["scan", "--from", FROM, "--to", TO, "--pg", dsn, "--table", table,
                   "--utc-col", "starts_at", "--tz-col", "tz", "--corrections", str(sql_path)])
    assert rc == 0
    sql = sql_path.read_text()
    assert sum(l.startswith("UPDATE ") for l in sql.splitlines()) == sum(expected.values())

    _psql(cid, sql)  # the realistic path: psql -f corrections.sql
    after = {r[0]: r for r in _rows(dsn, table)}
    for i, aff in expected.items():
        if not aff:
            assert after[i] == before[i], f"{table} row {i} touched"
        else:
            assert after[i][1] != before[i][1] and type(after[i][1]) is type(before[i][1])

    _psql(cid, sql)  # idempotent
    assert {r[0]: r for r in _rows(dsn, table)} == after

    zi_from, zi_to = releases.compile(FROM), releases.compile(TO)
    for i, aff in expected.items():
        if not aff:
            continue
        zone = before[i][2]
        old_utc, new_utc = to_instant(before[i][1], True), to_instant(after[i][1], True)
        intended = _local(zi_from, zone, old_utc)
        assert _local(zi_to, zone, new_utc) == intended, f"{table} row {i}"
        assert _local(zi_to, zone, old_utc) != intended
