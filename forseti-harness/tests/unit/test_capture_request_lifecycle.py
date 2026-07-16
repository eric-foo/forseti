from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from capture_spine.capture_request_lifecycle import (
    CaptureRequestLifecycleError,
    validate_capture_request_lifecycle,
)
from data_lake.root import DataLakeRoot
from harness_utils import hash_file
from source_capture import known_fact, write_local_source_capture_packet


def _packet(root: DataLakeRoot, tmp_path: Path, name: str, source_family: str) -> tuple[str, str]:
    body = tmp_path / f"{name}.html"
    body.write_text(f"<html>{name}</html>", encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body],
        source_family=source_family,
        source_surface="public_web",
        source_locator=known_fact(f"https://example.test/{name}"),
        decision_question="What public buyer-language evidence was preserved?",
        capture_context="capture request lifecycle unit test",
        cutoff_posture=known_fact("pre_cutoff"),
    )
    return result.packet.packet_id, hash_file(Path(result.manifest_path))


def _ledger(tmp_path: Path) -> tuple[dict, DataLakeRoot]:
    root = DataLakeRoot.for_test((tmp_path / "lake").resolve())
    parfumo_id, parfumo_sha = _packet(root, tmp_path, "parfumo", "fragrance_native_database")
    reddit_id, reddit_sha = _packet(root, tmp_path, "reddit", "forums_community")
    requests = [
        {
            "request_id": "cr_parfumo",
            "source_family": "fragrance_native_database",
            "venue": "Parfumo",
            "urls": ["https://example.test/parfumo"],
            "demand_origin_eligible": True,
        },
        {
            "request_id": "cr_reddit",
            "source_family": "forums_community",
            "venue": "Reddit",
            "urls": ["https://example.test/reddit"],
            "demand_origin_eligible": True,
        },
    ]
    events: list[dict] = []
    for offset, (request_id, packet_id, manifest_sha) in enumerate(
        (("cr_parfumo", parfumo_id, parfumo_sha), ("cr_reddit", reddit_id, reddit_sha))
    ):
        base = offset * 4
        for step, state in enumerate(("requested", "route_bound", "captured", "handoff_ready")):
            events.append(
                {
                    "event_id": f"evt_{request_id}_{state}",
                    "request_id": request_id,
                    "state": state,
                    "observed_at": f"2026-07-16T00:00:{base + step:02d}Z",
                    "evidence_refs": [f"docs/research/{request_id}_{state}.md"],
                    "reason_or_none": None,
                    "mode_ladder_receipt_or_none": None,
                    "packet_id_or_none": packet_id if state in {"captured", "handoff_ready"} else None,
                    "manifest_sha256_or_none": manifest_sha if state == "handoff_ready" else None,
                }
            )
    cost_yield = [
        {
            "stage_id": "scan",
            "stage_type": "scan",
            "request_id_or_none": None,
            "source_family_or_none": None,
            "wall_clock_seconds": 12.5,
            "token_cost_posture": "unknown_with_reason",
            "token_count_or_none": None,
            "token_unknown_reason_or_none": "local scan instrumentation did not expose token usage",
            "venues_touched": 2,
            "requests_emitted": 2,
            "requests_fulfilled": 2,
            "requests_declined": 0,
            "packets_handoff_ready": 2,
        }
    ]
    for request in requests:
        cost_yield.append(
            {
                "stage_id": f"capture_{request['request_id']}",
                "stage_type": "capture",
                "request_id_or_none": request["request_id"],
                "source_family_or_none": request["source_family"],
                "wall_clock_seconds": 3.0,
                "token_cost_posture": "unknown_with_reason",
                "token_count_or_none": None,
                "token_unknown_reason_or_none": "capture runner did not use a metered model",
                "venues_touched": 1,
                "requests_emitted": 0,
                "requests_fulfilled": 1,
                "requests_declined": 0,
                "packets_handoff_ready": 1,
            }
        )
    return (
        {
            "schema_version": "capture_request_lifecycle_v0",
            "commission_id": "p0_fixture",
            "subject": "Imaginary Authors",
            "source_scan": "docs/research/fixture_scan.md",
            "requests": requests,
            "events": events,
            "cost_yield": cost_yield,
        },
        root,
    )


def test_terminal_p0_ledger_verifies_real_packets(tmp_path: Path) -> None:
    ledger, root = _ledger(tmp_path)

    validate_capture_request_lifecycle(
        ledger,
        require_p0=True,
        data_root=root,
        require_packet_verification=True,
    )


def test_skipped_transition_fails(tmp_path: Path) -> None:
    ledger, _ = _ledger(tmp_path)
    ledger["events"] = [event for event in ledger["events"] if event["state"] != "route_bound"]

    with pytest.raises(CaptureRequestLifecycleError, match="cannot transition") as exc_info:
        validate_capture_request_lifecycle(ledger)
    assert exc_info.value.code == "invalid_transition"


def test_nonterminal_request_fails(tmp_path: Path) -> None:
    ledger, _ = _ledger(tmp_path)
    ledger["events"] = ledger["events"][:-1]

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(ledger)
    assert exc_info.value.code == "nonterminal_requests"


def test_decline_requires_mode_ladder_receipt(tmp_path: Path) -> None:
    ledger, _ = _ledger(tmp_path)
    first = ledger["events"][0]
    ledger["events"] = [
        first,
        {
            **first,
            "event_id": "evt_declined",
            "state": "declined",
            "observed_at": "2026-07-16T00:00:01Z",
            "reason_or_none": "route remained unsafe",
            "mode_ladder_receipt_or_none": None,
        },
        *ledger["events"][4:],
    ]

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(ledger)
    assert exc_info.value.code == "invalid_string"


def test_p0_rejects_one_origin_family(tmp_path: Path) -> None:
    ledger, _ = _ledger(tmp_path)
    ledger["requests"][1]["source_family"] = "fragrance_native_database"
    ledger["cost_yield"][2]["source_family_or_none"] = "fragrance_native_database"

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(ledger, require_p0=True)
    assert exc_info.value.code == "insufficient_independent_origin_families"


def test_cost_yield_must_match_terminal_outcomes(tmp_path: Path) -> None:
    ledger, _ = _ledger(tmp_path)
    ledger["cost_yield"][0]["requests_fulfilled"] = 1

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(ledger)
    assert exc_info.value.code == "scan_cost_yield_mismatch"


def test_tampered_packet_cannot_be_handoff_ready(tmp_path: Path) -> None:
    ledger, root = _ledger(tmp_path)
    packet_id = ledger["events"][3]["packet_id_or_none"]
    packet_dir = root.find_packet(packet_id)
    assert packet_dir is not None
    preserved = next(
        path
        for path in packet_dir.rglob("*")
        if path.is_file() and path.name not in {"manifest.json", "receipt.md"}
    )
    preserved.write_bytes(b"tampered")

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(
            ledger,
            require_p0=True,
            data_root=root,
            require_packet_verification=True,
        )
    assert exc_info.value.code == "handoff_packet_invalid"


def test_structural_handoff_cannot_claim_packet_verification_without_root(tmp_path: Path) -> None:
    ledger, _ = _ledger(tmp_path)

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(ledger, require_packet_verification=True)
    assert exc_info.value.code == "packet_verification_unavailable"


def test_packet_source_family_must_match_request(tmp_path: Path) -> None:
    ledger, root = _ledger(tmp_path)
    ledger["requests"][1]["source_family"] = "wrong_family"
    ledger["cost_yield"][2]["source_family_or_none"] = "wrong_family"

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(
            ledger,
            data_root=root,
            require_packet_verification=True,
        )
    assert exc_info.value.code == "handoff_source_family_mismatch"


def test_packet_locator_must_match_a_requested_url(tmp_path: Path) -> None:
    """A packet from the right family is still the wrong evidence for another URL."""
    ledger, root = _ledger(tmp_path)
    ledger["requests"][0]["urls"] = ["https://example.test/a-url-nobody-captured"]

    with pytest.raises(CaptureRequestLifecycleError) as exc_info:
        validate_capture_request_lifecycle(
            ledger,
            data_root=root,
            require_packet_verification=True,
        )
    assert exc_info.value.code == "handoff_source_locator_mismatch"
