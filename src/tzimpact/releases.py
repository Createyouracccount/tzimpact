"""Download and compile IANA tzdb releases. Cached under ~/.cache/tzimpact."""

from __future__ import annotations

import os
import pathlib
import subprocess
import tarfile
import urllib.request

CACHE = pathlib.Path(os.environ.get("TZIMPACT_CACHE", pathlib.Path.home() / ".cache" / "tzimpact"))
BASE = "https://data.iana.org/time-zones/releases/tzdata{v}.tar.gz"
# the region files zic needs; 'backward' supplies the alias zones (Canada/Mountain etc.)
REGIONS = [
    "africa", "antarctica", "asia", "australasia", "europe",
    "northamerica", "southamerica", "etcetera", "backward",
]


def fetch(version: str) -> pathlib.Path:
    src = CACHE / "src" / version
    if src.exists() and (src / "northamerica").exists():
        return src
    src.mkdir(parents=True, exist_ok=True)
    url = BASE.format(v=version)
    tmp = CACHE / f"{version}.tar.gz"
    urllib.request.urlretrieve(url, tmp)
    with tarfile.open(tmp) as tf:
        tf.extractall(src, filter="data")
    tmp.unlink()
    return src


def compile(version: str) -> pathlib.Path:
    out = CACHE / "zi" / version
    if out.exists() and any(out.iterdir()):
        return out
    src = fetch(version)
    out.mkdir(parents=True, exist_ok=True)
    for region in REGIONS:
        f = src / region
        if f.exists():
            subprocess.run(["zic", "-d", str(out), str(f)], check=True, capture_output=True)
    return out


def zones(zi: pathlib.Path) -> set[str]:
    found = set()
    for p in zi.rglob("*"):
        if p.is_file():
            rel = p.relative_to(zi).as_posix()
            if rel[0].isupper():
                found.add(rel)
    return found


def news(version: str) -> str:
    return (fetch(version) / "NEWS").read_text(errors="replace")


def release_header(version: str) -> tuple[str, str]:
    """(label, 'YYYY-MM-DD') of the first NEWS header in the release's own NEWS.

    NEWS is cumulative and newest-first, so the first header is the release's
    own entry. The label is returned separately because upstream has shipped
    a mislabeled header: tzdata2026b's NEWS opens with
    "Release 2026a - 2026-04-22 23:06:43 -0700" (2026b's date, 2026a's name).
    """
    import re

    m = re.search(r"^Release (\S+) - (\d{4}-\d{2}-\d{2})", news(version), re.M)
    if not m:
        raise ValueError(f"no NEWS header in release {version}")
    return m.group(1), m.group(2)


def release_date(version: str) -> str:
    return release_header(version)[1]


def links(version: str) -> dict[str, str]:
    """alias -> target for every ``Link`` line in the release's region files."""
    src = fetch(version)
    out: dict[str, str] = {}
    for region in REGIONS:
        f = src / region
        if not f.exists():
            continue
        for line in f.read_text(errors="replace").splitlines():
            parts = line.split("#", 1)[0].split()
            if len(parts) >= 3 and parts[0] == "Link":
                out[parts[2]] = parts[1]
    return out


def canonical(zone: str, link_map: dict[str, str]) -> str:
    seen: set[str] = set()
    while zone in link_map and zone not in seen:
        seen.add(zone)
        zone = link_map[zone]
    return zone


INDEX = "https://data.iana.org/time-zones/releases/"


def list_releases(since: str = "2020a") -> list[str]:
    """Release names from the IANA index, ascending, from `since` on. Network."""
    import re

    with urllib.request.urlopen(INDEX) as resp:
        html = resp.read().decode("utf-8", "replace")
    names = sorted(set(re.findall(r"tzdata(\d{4}[a-z])\.tar\.gz", html)))
    return [n for n in names if n >= since]
