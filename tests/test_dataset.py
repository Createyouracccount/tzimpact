"""The dataset must say exactly what the golden suite says, for every pair.

Golden CASES are the NEWS-transcribed truth; the dataset is a machine-readable
projection of the same diff. If they disagree, the projection is wrong.
"""

import json

import pytest

from tzimpact import dataset, releases
from test_golden import CASES

pytestmark = pytest.mark.golden  # counts toward the "zero golden tests executed" guard


@pytest.mark.parametrize("frm,to,date,expected,note", CASES, ids=[f"{c[0]}-{c[1]}" for c in CASES])
def test_dataset_matches_golden(frm, to, date, expected, note):
    doc = dataset.build(frm, to)
    assert doc["from"] == frm and doc["to"] == to
    assert doc["released"] == date, "released date must come from the NEWS header"
    zones = {e["zone"] for e in doc["changed_zones"]}
    assert zones == expected, f"{frm}->{to}: dataset {sorted(zones)} vs NEWS {sorted(expected)}"
    link_map = releases.links(to)
    for e in doc["changed_zones"]:
        assert e["zone"] == releases.canonical(e["zone"], link_map), "entries must be canonical"
        assert e["shift_seconds"] == e["new_offset"] - e["old_offset"]
        assert e["from_utc"].endswith("Z") and (e["to_utc"] is None or e["to_utc"] > e["from_utc"])
        for a in e["aliases"]:
            assert releases.canonical(a, link_map) == e["zone"]
    json.dumps(doc)  # serialisable


def test_aliases_fold_links():
    doc = dataset.build("2026b", "2026c")
    edm = [e for e in doc["changed_zones"] if e["zone"] == "America/Edmonton"]
    assert edm and set(edm[0]["aliases"]) >= {"America/Yellowknife", "Canada/Mountain"}
    assert not any(e["zone"] in ("America/Yellowknife", "Canada/Mountain") for e in doc["changed_zones"])
    assert len(edm) == 10  # ten discrete winter windows, as the golden alberta test requires


def test_write_all_and_index(tmp_path):
    files = dataset.write_all(["2026a", "2026b", "2026c"], tmp_path)
    assert [f.name for f in files] == ["2026a-2026b.json", "2026b-2026c.json"]
    index = json.loads((tmp_path / "index.json").read_text())
    assert [p["file"] for p in index["pairs"]] == ["2026a-2026b.json", "2026b-2026c.json"]
    assert index["pairs"][1]["changed_zone_count"] == 3
