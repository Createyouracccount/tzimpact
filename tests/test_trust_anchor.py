"""The golden suite must never turn a real failure into a green run.

Two properties, checked by running the golden suite in a subprocess with
``releases.fetch`` replaced:

1. A non-network error (zic failure, parse error, corrupt cache) must surface as
   an ERROR/FAIL, not a skip.
2. A genuine network error may skip the golden tests, but a session in which
   zero golden tests executed must still exit non-zero (skip-total guard).
"""

import pathlib

HERE = pathlib.Path(__file__).parent
GOLDEN_SRC = (HERE / "test_golden.py").read_text()
CONFTEST_SRC = (HERE / "conftest.py").read_text()


def _run_golden_with(pytester, patch: str):
    pytester.makeconftest(CONFTEST_SRC + "\n\n# --- injected by test_trust_anchor ---\n" + patch)
    pytester.makepyfile(test_golden_copy=GOLDEN_SRC)
    return pytester.runpytest_subprocess("-p", "no:cacheprovider", "-q", "-rs")


def test_non_network_error_is_a_failure_not_a_skip(pytester):
    res = _run_golden_with(
        pytester,
        "import tzimpact.releases as _r\n"
        "def _boom(version):\n"
        "    raise RuntimeError('zic failed (simulated non-network error)')\n"
        "_r.fetch = _boom\n",
    )
    out = res.parseoutcomes()
    assert out.get("skipped", 0) == 0, f"non-network error was swallowed as skip: {out}"
    assert out.get("errors", 0) + out.get("failed", 0) > 0, out
    assert res.ret != 0


def test_network_error_may_skip_but_session_must_not_pass(pytester):
    res = _run_golden_with(
        pytester,
        "import urllib.error, tzimpact.releases as _r\n"
        "def _down(version):\n"
        "    raise urllib.error.URLError('simulated: network unreachable')\n"
        "_r.fetch = _down\n",
    )
    out = res.parseoutcomes()
    assert out.get("passed", 0) == 0 and out.get("skipped", 0) > 0, out
    assert res.ret != 0, f"0 golden tests executed yet the session passed: {out}"
