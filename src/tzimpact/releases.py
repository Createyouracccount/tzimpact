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
