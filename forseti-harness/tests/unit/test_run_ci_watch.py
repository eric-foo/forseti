import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from runners import run_ci_watch as cli


HEAD = "a" * 40


def fake_gh(monkeypatch, *, checks=None, watch_code=0, heads=None, timeout=False, view_code=0):
    calls = []
    heads = iter(heads or [HEAD, HEAD, HEAD])
    checks = [{"name": "tests", "bucket": "pass", "state": "SUCCESS"}] if checks is None else checks

    def run(argv, *, stdout, stderr, timeout, check, shell):
        assert shell is False
        calls.append(argv)
        if "view" in argv:
            stdout.write(json.dumps({"headRefOid": next(heads), "state": "OPEN"}))
            return SimpleNamespace(returncode=view_code)
        if "--watch" in argv:
            if watch_timeout:
                raise subprocess.TimeoutExpired(argv, timeout)
            stdout.write("intermediate output\n" * 1000)
            return SimpleNamespace(returncode=watch_code)
        stdout.write(json.dumps(checks))
        return SimpleNamespace(returncode=0)

    watch_timeout = timeout
    monkeypatch.setattr(cli.subprocess, "run", run)
    return calls


def observe(tmp_path):
    return cli.observe(repo="owner/repo", pr=1, head=HEAD, output_dir=tmp_path)


def test_pass_keeps_poll_output_on_disk_and_never_merges(tmp_path, monkeypatch):
    calls = fake_gh(monkeypatch)
    result, code = observe(tmp_path)
    assert code == 0 and result["status"] == "passed"
    assert len(calls) == 5
    assert sum("--watch" in call for call in calls) == 1
    assert all("merge" not in call for call in calls)
    saved = json.loads(Path(result["record_path"]).read_text())
    assert saved["checks"][0]["name"] == "tests"
    assert len(Path(saved["commands"][1]["stdout_path"]).read_text()) > 10000
    assert "intermediate output" not in json.dumps(result)


@pytest.mark.parametrize("checks,watch_code,expected", [
    ([], 0, "blocked"),
    ([{"bucket": "fail"}], 1, "failed"),
    ([{"bucket": "pending"}], 0, "blocked"),
    ([{"bucket": "skipping"}], 0, "blocked"),
    ([{"bucket": "mystery"}], 0, "blocked"),
    ([{"bucket": "pass"}], 1, "blocked"),
])
def test_near_misses_cannot_report_green(tmp_path, monkeypatch, checks, watch_code, expected):
    fake_gh(monkeypatch, checks=checks, watch_code=watch_code)
    result, code = observe(tmp_path)
    assert code == 1 and result["status"] == expected


@pytest.mark.parametrize("heads", [["b" * 40], [HEAD, "b" * 40, "b" * 40], [HEAD, HEAD, "b" * 40]])
def test_head_mismatch_never_succeeds(tmp_path, monkeypatch, heads):
    calls = fake_gh(monkeypatch, heads=heads)
    result, code = observe(tmp_path)
    assert code == 1 and result["status"] == "blocked"
    if len(heads) == 1:
        assert len(calls) == 1


def test_timeout_visible_and_later_fresh_watch_can_recover(tmp_path, monkeypatch):
    fake_gh(monkeypatch, timeout=True)
    result, code = observe(tmp_path)
    assert code == 1 and result["status"] == "timeout" and result["watch_exit_code"] == 124
    fake_gh(monkeypatch)
    recovered, code = observe(tmp_path)
    assert code == 0 and recovered["record_path"] != result["record_path"]
    assert json.loads(Path(result["record_path"]).read_text())["status"] == "timeout"
