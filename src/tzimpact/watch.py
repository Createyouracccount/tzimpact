"""Detect a tzdb release newer than the committed dataset.

Pure functions, so the decision the bot makes is unit-testable without the
network; the CLI (`tzimpact watch`) wires them to IANA's index and to
``$GITHUB_OUTPUT``. The bot only *proposes* an update (a pull request); it
never pushes to main and nothing here merges anything.
"""

from __future__ import annotations

import json
import os
import pathlib
import re

_NAME = re.compile(r"^\d{4}[a-z]$")


def _valid(name: str) -> str:
    if not _NAME.match(name):
        raise ValueError(f"not a tzdb release name: {name!r}")
    return name


def committed_latest(index: dict) -> str:
    """The newest release the committed dataset covers (max 'to' over pairs)."""
    pairs = index.get("pairs") or []
    if not pairs:
        raise ValueError("index has no pairs")
    return max(_valid(p["to"]) for p in pairs)


def available_latest(names: list[str]) -> str:
    if not names:
        raise ValueError("no releases listed")
    return max(_valid(n) for n in names)


def update_needed(committed: str, available: str) -> bool:
    """tzdb names sort lexicographically: 2026b < 2026c < 2027a."""
    return _valid(available) > _valid(committed)


def check(index_path: str | pathlib.Path, names: list[str]) -> dict:
    index = json.loads(pathlib.Path(index_path).read_text())
    committed, available = committed_latest(index), available_latest(names)
    return {
        "committed": committed,
        "available": available,
        "update_needed": update_needed(committed, available),
        "missing": sorted(n for n in names if _valid(n) > committed),
    }


def write_github_output(result: dict, path: str | None = None) -> None:
    """Append key=value lines for a workflow step; a no-op outside GitHub Actions."""
    path = path or os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"update_needed={'true' if result['update_needed'] else 'false'}\n")
        f.write(f"committed={result['committed']}\n")
        f.write(f"available={result['available']}\n")
