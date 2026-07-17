from __future__ import annotations

import json
from pathlib import Path

import pytest

from source_capture.tiktok.grid_packet import (
    TIKTOK_GRID_PACKET_SOURCE_SURFACE,
    TIKTOK_GRID_WINDOW_JSON_NAME,
    write_tiktok_grid_packet,
)


def _grid_bytes(
    *,
    observed_at: str | None = "2026-07-13T01:02:03Z",
    profile_metrics: bool = False,
) -> bytes:
    payload = {
        "creator_handle": "creator",
        "window_size": 2,
        "complete": True,
        "items": [
            {
                "video_id": "101",
                "video_url": "https://www.tiktok.com/@creator/video/101",
                "stats": {
                    "playCount": 0,
                    "diggCount": 0,
                    "commentCount": 4,
                },
            },
            {
                "video_id": "102",
                "video_url": "https://www.tiktok.com/@creator/video/102",
                "stats": {"playCount": 50, "diggCount": 5},
            },
        ],
        "collection_receipt": {"capture_timestamp": observed_at},
    }
    if profile_metrics:
        payload["profile_metric_capture_policy_version"] = "tiktok_profile_metric_capture_v0"
        payload["profile_metrics"] = {
            "follower_count": {
                "source_field": "followerCount",
                "exact_value_or_none": 1_234,
                "posture": "observed",
                "reason_or_none": None,
                "source_route": "profile_hydration:profile_user_info_stats",
                "raw_text_or_none": "1234",
            },
            "profile_total_like_count": {
                "source_field": "heartCount",
                "exact_value_or_none": None,
                "posture": "unavailable_with_reason",
                "reason_or_none": "profile_header_dom_compact_or_non_integer",
                "source_route": "profile_header_dom",
                "raw_text_or_none": "1.2M",
            },
        }
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def test_grid_packet_preserves_supplied_grid_bytes_exactly(tmp_path: Path) -> None:
    raw = _grid_bytes()
    output = tmp_path / "packet"

    code, packet_dir_text = write_tiktok_grid_packet(
        grid_window_json=raw,
        output_directory=output,
    )

    assert code == 0
    packet_dir = Path(packet_dir_text)
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    preserved = next(
        row
        for row in manifest["preserved_files"]
        if Path(row["relative_packet_path"]).name.endswith(TIKTOK_GRID_WINDOW_JSON_NAME)
    )
    assert manifest["source_surface"] == TIKTOK_GRID_PACKET_SOURCE_SURFACE
    assert (packet_dir / preserved["relative_packet_path"]).read_bytes() == raw


def test_grid_packet_emits_typed_profile_metric_observations(tmp_path: Path) -> None:
    code, packet_dir_text = write_tiktok_grid_packet(
        grid_window_json=_grid_bytes(profile_metrics=True),
        output_directory=tmp_path / "profile-metrics",
    )

    assert code == 0
    manifest = json.loads(
        (Path(packet_dir_text) / "manifest.json").read_text(encoding="utf-8")
    )
    observations = {
        row["metric"]: row
        for row in manifest["source_slices"][0]["metric_observations"]
    }
    assert observations["follower_count"]["posture"] == "observed"
    assert observations["follower_count"]["value"] == 1_234
    assert observations["profile_total_like_count"]["posture"] == (
        "unavailable_with_reason"
    )
    assert observations["profile_total_like_count"]["value"] is None


def test_grid_packet_rejects_partial_profile_metric_contract(tmp_path: Path) -> None:
    payload = json.loads(_grid_bytes(profile_metrics=True))
    del payload["profile_metrics"]["profile_total_like_count"]

    with pytest.raises(ValueError, match="exactly the two profile metrics"):
        write_tiktok_grid_packet(
            grid_window_json=json.dumps(payload).encode("utf-8"),
            output_directory=tmp_path / "partial-profile-metrics",
        )


def test_grid_packet_preserves_supplied_session_identity(tmp_path: Path) -> None:
    code, packet_dir_text = write_tiktok_grid_packet(
        grid_window_json=_grid_bytes(),
        output_directory=tmp_path / "packet-with-session",
        session_identity="01TESTHEARTBEATATTEMPT",
    )

    assert code == 0
    manifest = json.loads(
        (Path(packet_dir_text) / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["session_identity"] == "01TESTHEARTBEATATTEMPT"


def test_grid_packet_requires_explicit_observed_time_when_receipt_has_none(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="source-backed UTC capture time"):
        write_tiktok_grid_packet(
            grid_window_json=_grid_bytes(observed_at=None),
            output_directory=tmp_path / "missing-time",
        )

    code, _ = write_tiktok_grid_packet(
        grid_window_json=_grid_bytes(observed_at=None),
        observed_at_utc="2026-07-13T01:02:03Z",
        output_directory=tmp_path / "explicit-time",
    )
    assert code == 0


def test_grid_packet_rejects_explicit_time_conflicting_with_receipt(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="conflicts with"):
        write_tiktok_grid_packet(
            grid_window_json=_grid_bytes(observed_at="2026-07-13T01:02:03Z"),
            observed_at_utc="2026-07-14T00:00:00Z",
            output_directory=tmp_path / "conflicting-time",
        )


def test_grid_packet_accepts_explicit_time_matching_receipt_instant(
    tmp_path: Path,
) -> None:
    code, _ = write_tiktok_grid_packet(
        grid_window_json=_grid_bytes(observed_at="2026-07-13T01:02:03Z"),
        observed_at_utc="2026-07-13T01:02:03+00:00",
        output_directory=tmp_path / "matching-time",
    )
    assert code == 0


def test_grid_packet_rejects_malformed_receipt_time_even_with_override(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError):
        write_tiktok_grid_packet(
            grid_window_json=_grid_bytes(observed_at="yesterday"),
            observed_at_utc="2026-07-13T01:02:03Z",
            output_directory=tmp_path / "malformed-receipt-time",
        )


def test_grid_packet_rejects_video_url_on_non_tiktok_host(tmp_path: Path) -> None:
    payload = json.loads(_grid_bytes().decode("utf-8"))
    payload["items"][0]["video_url"] = "https://evil.example/@creator/video/101"
    with pytest.raises(ValueError, match="does not bind"):
        write_tiktok_grid_packet(
            grid_window_json=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
            output_directory=tmp_path / "wrong-host",
        )
