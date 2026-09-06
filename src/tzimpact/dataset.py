"""tzimpact-data: machine-readable diff of every consecutive tzdb release pair.

One JSON document per pair, schema (docs/05_implementation_plan.md §2 C):

    {"from": "2026b", "to": "2026c", "released": "2026-07-08",
     "changed_zones": [{"zone": "Africa/Casablanca", "from_utc": "...Z", "to_utc": "...Z"|null,
                        "old_offset": 3600, "new_offset": 0, "shift_seconds": -3600,
                        "aliases": ["..."]}]}

Zones are canonical (Link aliases folded into ``aliases``); one entry per
change window; the window is the release date plus ten years, the same
window the golden tests use. A pair with an unparseable zone is refused,
never published incomplete.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib

from . import __version__, releases
from .diff import diff

WINDOW_YEARS = 10
_UTC = dt.timezone.utc


def _iso(ts: int | None) -> str | None:
    return None if ts is None else dt.datetime.fromtimestamp(ts, _UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def build(from_version: str, to_version: str) -> dict:
    label, released = releases.release_header(to_version)
    when = dt.datetime.fromisoformat(released).replace(tzinfo=_UTC)
    result = diff(from_version, to_version, start=when, years=WINDOW_YEARS)
    if result.unparseable:
        raise RuntimeError(
            f"{from_version}->{to_version}: {len(result.unparseable)} zone(s) could not be parsed; "
            f"refusing to publish an incomplete diff: {result.unparseable}"
        )
    link_map = releases.links(to_version)
    by_canonical: dict[str, dict[tuple[int, int | None, int, int], dict]] = {}
    for c in result.changes:
        zone = releases.canonical(c.zone, link_map)
        key = (c.start_utc, c.end_utc, c.old_offset, c.new_offset)
        by_canonical.setdefault(zone, {}).setdefault(key, {
            "zone": zone, "from_utc": _iso(c.start_utc), "to_utc": _iso(c.end_utc),
            "old_offset": c.old_offset, "new_offset": c.new_offset, "shift_seconds": c.shift_seconds,
        })
    changed = []
    for zone in sorted(by_canonical):
        aliases = sorted(a for a in link_map if releases.canonical(a, link_map) == zone)
        for key in sorted(by_canonical[zone]):
            entry = dict(by_canonical[zone][key])
            entry["aliases"] = aliases
            changed.append(entry)
    return {
        "schema": "tzimpact-data/1",
        "generator": f"tzimpact {__version__}",
        "from": from_version,
        "to": to_version,
        "released": released,
        "news_header_label": label,  # differs from "to" when upstream mislabeled the header (2026b)
        "window": {"since": when.strftime("%Y-%m-%dT%H:%M:%SZ"), "years": WINDOW_YEARS},
        "changed_zones": changed,
    }


def pairs(versions: list[str]) -> list[tuple[str, str]]:
    return list(zip(versions, versions[1:]))


def write_all(versions: list[str], out: pathlib.Path) -> list[pathlib.Path]:
    out.mkdir(parents=True, exist_ok=True)
    written = []
    index = []
    for frm, to in pairs(versions):
        doc = build(frm, to)
        path = out / f"{frm}-{to}.json"
        path.write_text(json.dumps(doc, indent=2) + "\n")
        written.append(path)
        index.append({"from": frm, "to": to, "released": doc["released"], "file": path.name,
                      "changed_zone_count": len({e["zone"] for e in doc["changed_zones"]})})
    (out / "index.json").write_text(json.dumps({"schema": "tzimpact-data/1", "pairs": index}, indent=2) + "\n")
    return written
