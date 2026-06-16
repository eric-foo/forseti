from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from runners import run_source_capture_ig_calls_packet as ig_runner
from runners.run_source_capture_ig_calls_packet import run_source_capture_ig_calls_packet
from source_capture.adapters.browser_snapshot import BrowserSnapshotFailure, BrowserSnapshotFailureKind, BrowserSnapshotSuccess
from source_capture.ig_momentum_harvest import (
    IgMediaMetricRecord,
    IgMomentumResponseRecord,
    IgProfileMomentumCapture,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"ig_calls_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _success(*, requested_url: str, rendered_dom: str, final_url: str | None = None,
             title: str = "Instagram", visible_text: str = "body") -> BrowserSnapshotSuccess:
    return BrowserSnapshotSuccess(
        requested_url=requested_url,
        final_url=final_url or requested_url,
        title=title,
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        screenshot_png=b"\x89PNG\r\n\x1a\nig",
        metadata={"capture_timestamp": "2026-06-14T01:02:03Z"},
        warning_notes=[],
        limitation_notes=[],
    )


PROFILE_URL = "https://www.instagram.com/hyram/"
_PROFILE_DOM = (
    '<html><head>'
    '<meta property="og:description" content="724K Followers, 2,339 Following, 321 Posts - See">'
    "</head><body>"
    '<a href="/hyram/p/AAA/">1</a>'
    '<a href="/hyram/reel/BBB/">2</a>'
    '<a href="/hyram/p/CCC/">3</a>'
    '<a href="/explore/">x</a>'
    "</body></html>"
)
_POST_DOM = (
    '<meta property="og:description" '
    'content="1,693 likes, 26 comments - hyram on August 1, 2024: &quot;A post caption #fun&quot;. ">'
)
_REEL_DOM = (
    '<meta property="og:description" '
    'content="1,047 likes, 43 comments - hyram on September 11, 2024: &quot;#ad sponsored thing&quot;. ">'
)
_NO_OG_DOM = "<html><body>no meta description here</body></html>"
_GARBLED_OG_DOM = '<meta property="og:description" content="Instagram photos and videos">'


def _route_fake(url: str) -> BrowserSnapshotSuccess:
    if "/p/AAA/" in url:
        return _success(requested_url=url, rendered_dom=_POST_DOM)
    if "/reel/BBB/" in url:
        return _success(requested_url=url, rendered_dom=_REEL_DOM)
    if "/p/CCC/" in url:
        return _success(requested_url=url, rendered_dom=_NO_OG_DOM)
    return _success(requested_url=url, rendered_dom=_PROFILE_DOM)


def _route_garbled(url: str) -> BrowserSnapshotSuccess:
    if "/p/AAA/" in url:
        return _success(requested_url=url, rendered_dom=_GARBLED_OG_DOM)
    return _success(requested_url=url, rendered_dom=_PROFILE_DOM)


def _momentum_capture(**_kwargs) -> IgProfileMomentumCapture:
    return IgProfileMomentumCapture(
        username="hyram",
        numeric_id="5802114508",
        follower_count=724000,
        media_by_shortcode={
            "AAA": IgMediaMetricRecord(
                shortcode="AAA",
                is_video=False,
                video_view_count=None,
                like_count=1693,
                comment_count=26,
                caption="A post caption #fun",
                taken_at_timestamp=1722470400,
            ),
            "BBB": IgMediaMetricRecord(
                shortcode="BBB",
                is_video=True,
                video_view_count=104700,
                like_count=1047,
                comment_count=43,
                caption="#ad sponsored thing",
                taken_at_timestamp=1726012800,
            ),
        },
        raw_responses=[
            IgMomentumResponseRecord(
                request_id="web_profile_info",
                requested_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                final_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                status=200,
                ok=True,
                body_text='{"data":{"user":{"id":"5802114508"}}}',
            )
        ],
    )


def test_ig_calls_runner_writes_packet_with_profile_and_call_slices(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr(ig_runner, "fetch_browser_snapshot_capture", lambda **kw: _route_fake(kw["url"]))
    monkeypatch.setattr(ig_runner, "fetch_ig_profile_momentum", _momentum_capture)
    output_dir = scratch_dir / "packet"

    exit_code, message = run_source_capture_ig_calls_packet(
        profile_url=PROFILE_URL,
        output_directory=output_dir,
        decision_question="Which recent calls did this wind-caller make?",
        cadence_random_seed=7,
        sleep_fn=sleeps.append,
    )

    assert exit_code == 0
    assert message == str(output_dir.resolve())
    # XHR gaps plus cadence between the 3 enumerated items (2 inter-item gaps), human-mimicking.
    assert len(sleeps) == 4
    assert sleeps[:2] == [ig_runner.DEFAULT_XHR_REQUEST_GAP_SECONDS, ig_runner.DEFAULT_XHR_REQUEST_GAP_SECONDS]
    assert all(s > 0 for s in sleeps)

    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_surface"] == "ig_calls_browser_snapshot"
    assert manifest["capture_mode"] == "automated extraction"
    assert "ig_browser_context_view_count_capture:observed=1" in manifest["visible_mode_changes"]
    slice_ids = [s["slice_id"] for s in manifest["source_slices"]]
    assert slice_ids == ["ig_profile_00", "ig_call_01", "ig_call_02", "ig_call_03"]
    assert manifest["receipt_metadata"]["non_claims"] == ig_runner.IG_CALLS_NON_CLAIMS
    # 2 of 3 captured (CCC has no og:description -> no_signal), surfaced honestly.
    assert any("partial_capture: 2/3" in lim for lim in manifest["limitations"])
    assert any("ig_metric_registry_version=" in lim for lim in manifest["limitations"])

    profile_slice = manifest["source_slices"][0]
    post_slice = manifest["source_slices"][1]
    reel_slice = manifest["source_slices"][2]
    missing_slice = manifest["source_slices"][3]
    assert profile_slice["metric_observations"] == [
        {
            "coverage_window": {"end": "2026-06-14T01:02:03Z", "start": None},
            "metric": "follower_count",
            "posture": "observed",
            "reason": None,
            "value": 724000,
        }
    ]
    assert {
        (obs["metric"], obs["posture"], obs["value"], obs["reason"])
        for obs in post_slice["metric_observations"]
    } == {
        ("like_count", "observed", 1693, None),
        ("comment_count", "observed", 26, None),
        ("view_count", "not_applicable", None, "IG profile-feed JSON marks this media as non-video"),
    }
    assert any(
        obs["metric"] == "view_count" and obs["posture"] == "observed" and obs["value"] == 104700
        for obs in reel_slice["metric_observations"]
    )
    assert any(
        obs["metric"] == "view_count" and obs["posture"] == "unavailable_with_reason"
        for obs in missing_slice["metric_observations"]
    )
    missing_view_count = next(
        obs for obs in missing_slice["metric_observations"] if obs["metric"] == "view_count"
    )
    assert missing_view_count["reason"] == (
        "item status=no_signal; view_count not attributed because the item did not produce a captured call signal"
    )

    raw = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in (output_dir / "raw").iterdir() if p.suffix == ".json"}
    post = next(v for k, v in raw.items() if "ig_call_01" in k)
    reel = next(v for k, v in raw.items() if "ig_call_02" in k)
    missing = next(v for k, v in raw.items() if "ig_call_03" in k)
    profile = next(v for k, v in raw.items() if "ig_profile.json" in k)
    momentum = next(v for k, v in raw.items() if "ig_profile_momentum" in k)
    assert post["status"] == "captured" and post["likes"] == 1693 and post["is_ad"] is False
    assert reel["status"] == "captured" and reel["is_ad"] is True and reel["date"] == "September 11, 2024"
    assert missing["status"] == "no_signal"
    assert profile["stats"] == {"followers": "724K", "following": "2,339", "posts": "321"}
    assert momentum["media"]["BBB"]["video_view_count"] == 104700


def test_ig_calls_runner_respects_item_cap(scratch_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ig_runner, "fetch_browser_snapshot_capture", lambda **kw: _route_fake(kw["url"]))
    output_dir = scratch_dir / "packet"
    exit_code, _ = run_source_capture_ig_calls_packet(
        profile_url=PROFILE_URL,
        output_directory=output_dir,
        decision_question="q",
        max_items=2,
        cadence_random_seed=1,
        capture_view_counts=False,
        sleep_fn=lambda _s: None,
    )
    assert exit_code == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    call_slices = [s for s in manifest["source_slices"] if s["slice_id"].startswith("ig_call_")]
    assert len(call_slices) == 2  # capped at max_items, not all 3 enumerated


def test_ig_calls_runner_rejects_item_cap_above_bounded_default(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="max_items must be no greater than"):
        run_source_capture_ig_calls_packet(
            profile_url=PROFILE_URL,
            output_directory=scratch_dir / "packet",
            decision_question="q",
            max_items=ig_runner.DEFAULT_MAX_ITEMS + 1,
            capture_view_counts=False,
            sleep_fn=lambda _s: None,
        )


def test_ig_calls_runner_does_not_mark_garbled_og_as_captured(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(ig_runner, "fetch_browser_snapshot_capture", lambda **kw: _route_garbled(kw["url"]))
    output_dir = scratch_dir / "packet"

    exit_code, _ = run_source_capture_ig_calls_packet(
        profile_url=PROFILE_URL,
        output_directory=output_dir,
        decision_question="q",
        max_items=1,
        cadence_random_seed=1,
        capture_view_counts=False,
        sleep_fn=lambda _s: None,
    )

    assert exit_code == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert any("partial_capture: 0/1" in lim for lim in manifest["limitations"])
    raw = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in (output_dir / "raw").iterdir() if p.suffix == ".json"}
    item = next(v for k, v in raw.items() if "ig_call_01" in k)
    assert item["status"] == "partial_signal"
    assert "minimum call signal" in item["message"]


def test_ig_calls_runner_returns_nogo_when_profile_redirects_to_login(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def blocked(**kw):
        return _success(
            requested_url=kw["url"],
            final_url="https://www.instagram.com/accounts/login/",
            rendered_dom="<html><body>Log in</body></html>",
        )

    monkeypatch.setattr(ig_runner, "fetch_browser_snapshot_capture", blocked)
    output_dir = scratch_dir / "packet"
    exit_code, message = run_source_capture_ig_calls_packet(
        profile_url=PROFILE_URL,
        output_directory=output_dir,
        decision_question="q",
        capture_view_counts=False,
        sleep_fn=lambda _s: None,
    )
    assert exit_code == 3
    assert "access-blocked" in message and "redirected_to_login" in message
    assert not output_dir.exists()


def test_ig_calls_runner_returns_nogo_when_no_permalinks(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ig_runner,
        "fetch_browser_snapshot_capture",
        lambda **kw: _success(requested_url=kw["url"], rendered_dom="<html><body>empty profile</body></html>"),
    )
    output_dir = scratch_dir / "packet"
    exit_code, message = run_source_capture_ig_calls_packet(
        profile_url=PROFILE_URL,
        output_directory=output_dir,
        decision_question="q",
        capture_view_counts=False,
        sleep_fn=lambda _s: None,
    )
    assert exit_code == 3
    assert "no /p/ or /reel/ permalinks" in message
    assert not output_dir.exists()


def test_ig_calls_runner_returns_3_on_profile_capture_failure(
    scratch_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        ig_runner,
        "fetch_browser_snapshot_capture",
        lambda **kw: BrowserSnapshotFailure(
            requested_url=kw["url"], failure_kind=BrowserSnapshotFailureKind.DEPENDENCY_UNAVAILABLE,
            message="Playwright is not installed",
        ),
    )
    output_dir = scratch_dir / "packet"
    exit_code, message = run_source_capture_ig_calls_packet(
        profile_url=PROFILE_URL,
        output_directory=output_dir,
        decision_question="q",
        capture_view_counts=False,
        sleep_fn=lambda _s: None,
    )
    assert exit_code == 3
    assert "profile capture failed" in message
    assert not output_dir.exists()


def test_ig_calls_runner_no_secret_or_session_cli_flags() -> None:
    parser = ig_runner._build_parser()
    options = {opt for action in parser._actions for opt in action.option_strings}
    forbidden = {"--password", "--username", "--token", "--cookie", "--storage-state-path", "--state-label", "--session-mode"}
    assert options.isdisjoint(forbidden)
