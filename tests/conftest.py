"""Skip-total guard for the golden suite.

The golden tests are the project's trust anchor. They may be skipped only when
tzdb releases are unreachable — but a run in which *zero* golden tests executed
must not report success, or a broken network silently turns into a green build.
"""

import pytest

pytest_plugins = ["pytester"]

_GOLDEN_IDS: set[str] = set()
_GOLDEN_OUTCOMES: dict[str, str] = {}


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        if item.get_closest_marker("golden"):
            _GOLDEN_IDS.add(item.nodeid)


def pytest_runtest_logreport(report):
    if report.nodeid not in _GOLDEN_IDS:
        return
    if report.skipped:
        _GOLDEN_OUTCOMES.setdefault(report.nodeid, "skipped")
    elif report.failed:
        _GOLDEN_OUTCOMES[report.nodeid] = "failed"
    elif report.when == "call" and report.passed:
        _GOLDEN_OUTCOMES[report.nodeid] = "passed"


def pytest_sessionfinish(session, exitstatus):
    if not _GOLDEN_IDS:
        return
    executed = sum(1 for o in _GOLDEN_OUTCOMES.values() if o in ("passed", "failed"))
    skipped = sum(1 for o in _GOLDEN_OUTCOMES.values() if o == "skipped")
    if executed == 0:
        tr = session.config.pluginmanager.get_plugin("terminalreporter")
        if tr is not None:
            tr.write_line(
                f"GOLDEN GUARD: 0 of {len(_GOLDEN_IDS)} golden tests executed "
                f"({skipped} skipped) - refusing to report success",
                red=True,
            )
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
