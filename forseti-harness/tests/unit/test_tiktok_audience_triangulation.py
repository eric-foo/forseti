from __future__ import annotations

import base64
import copy
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_LANE,
    build_comment_attention_records,
)
from evidence_binding.tiktok_audience_triangulation import (
    build_assembly_receipt,
    build_creator_audience_evidence_bundle,
)
from judgment.tiktok_audience_triangulation import (
    TriangulationValidationError,
    build_triangulation_prompt,
    parse_triangulation_response,
)
from data_lake.root import DataLakeRoot
from data_lake.silver_record import append_silver_record, silver_content_hash
from runners.run_tiktok_comment_attention_producer import run_comment_attention
from runners.run_creator_profile_current_materialize import _verify_audience_judgment_outcomes
from runners.run_tiktok_creator_audience_triangulation import (
    prepare_subscription_judgment,
    submit_subscription_judgment,
)
from runners.run_tiktok_creator_onboarding_coordinator import prepare_onboarding
from runners.run_tiktok_grid_observation_producer import run_tiktok_grid_observations
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from schemas.tiktok_audience_evidence_models import CreatorAudienceJudgmentOutcome
from test_tiktok_batch_admission import (
    PROFILE_URL,
    _cadence_payload,
    _grid_payload,
    _onboarding_evidence_payloads,
)


OBSERVED = "2026-07-12T00:00:00Z"
RAW_ANCHOR = "01TESTAUDIENCEPACKET"


def _video(video_id: str, comment_id: str, text: str, likes: int) -> dict:
    return {
        "video_id": video_id,
        "stats_observed_utc": OBSERVED,
        "stats": {"playCount": 10_000, "diggCount": 1_000, "commentCount": 100},
        "subtitles": {
            "transcript_text_sha256": f"sha256:{video_id}",
            "cues": [{"start_ms": 0, "end_ms": 1200, "text": f"compare product {video_id}"}],
        },
        "comments": {
            "observed_utc": OBSERVED,
            "comments": [
                {
                    "cid": comment_id,
                    "source_order": 0,
                    "text": text,
                    "digg_count": likes,
                    "reply_comment_total": 0,
                }
            ],
        },
    }


def _payload(*, duplicate_text: bool = False, transcript: bool = True) -> dict:
    first = "This comparison is unforgettable"
    second = first if duplicate_text else "Do this comparison again"
    videos = [_video("v1", "c1", first, 100), _video("v2", "c2", second, 80)]
    if not transcript:
        for video in videos:
            video["subtitles"]["cues"] = []
    return {"creator_handle": "alpha", "capture_timestamp": OBSERVED, "videos": videos}


def _bundle(*, duplicate_text: bool = False, transcript: bool = True) -> dict:
    payload = _payload(duplicate_text=duplicate_text, transcript=transcript)
    attention = build_comment_attention_records(
        raw_anchor=RAW_ANCHOR,
        batch_payload=payload,
        raw_file_ref={
            "file_id": "raw-file",
            "relative_packet_path": "raw/tiktok.json",
            "sha256": "a" * 64,
        },
    )
    return build_creator_audience_evidence_bundle(
        creator_id="tiktok:@alpha",
        profile_subject_id="platform_account:tiktok:alpha",
        raw_anchor=RAW_ANCHOR,
        batch_payload=payload,
        comment_attention_records=attention,
        grid_observation_refs=[{"record_id": "grid-1", "video_id": "v1"}],
        question="Who is this creator commercially useful for?",
        evidence_cutoff=OBSERVED,
    )


def _response(bundle: dict) -> dict:
    comment_ids = [row["evidence_id"] for row in bundle["comment_evidence"]]
    claim = {
        "claim_id": "claim-1",
        "axis": "engagement_memorability_effect",
        "statement": "The recurring comparison format generates engagement.",
        "commercial_implication": "Use it to make compared products memorable.",
        "modality": "engagement_elevated",
        "relation": "audience_emergent",
        "support_scope": "multi_video",
        "representative_evidence_ids": comment_ids,
        "all_support_evidence_ids": comment_ids,
        "counterevidence_ids": [],
        "source_video_ids": ["v1", "v2"],
        "limitation": "Captured top-level comments, not a platform census.",
    }
    point = {
        "statement": "Makes compared products impossible to ignore and easy to recall.",
        "claim_ids": ["claim-1"],
    }
    return {
        "schema_version": "creator_audience_triangulation_snapshot_v0",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": bundle["profile_subject_id"],
        "platform_account_id": bundle["profile_subject_id"],
        "creator_id": bundle["creator_id"],
        "platform_scope": "tiktok",
        "generated_at": "2026-07-14T00:00:00Z",
        "evidence_cutoff": bundle["evidence_cutoff"],
        "input_bundle_id": bundle["bundle_id"],
        "input_bundle_hash": bundle["bundle_hash"],
        "judgment_claim_set": {
            "claims": [claim],
            "agreements": [],
            "contradictions": [],
            "missing_evidence": ["No purchase conversion evidence."],
        },
        "creator_signal_projection": {
            "hire_verdict": point,
            "product_advantage": point,
            "creator_specific_execution": point,
            "observed_audience_response": point,
            "strongest_campaign_jobs": [point],
            "briefing_instructions": [point],
            "wrong_hire_boundary": point,
            "robustness_stamp": None,
        },
        "limitations": ["Captured comments are ranked or truncated."],
        "non_claims": ["not guaranteed conversion"],
        "actual_audience_demographics": "not_estimated",
    }


def test_bundle_uses_persisted_silver_and_preserves_duplicate_cluster() -> None:
    bundle = _bundle(duplicate_text=True)
    assert len(bundle["transcript_evidence"]) == 2
    assert len(bundle["comment_evidence"]) == 2
    assert bundle["exact_duplicate_clusters"][0]["multiplicity"] == 2
    assert all(row["comment_attention_record_id"] for row in bundle["comment_evidence"])
    assert all(row["temporal_alignment"] == "same_capture_observation" for row in bundle["comment_evidence"])
    receipt = build_assembly_receipt(bundle)
    assert receipt["judgment_status"] == "not_evaluated"
    assert len(receipt["evidence_index"]) == 4
    assert {row["evidence_id"] for row in receipt["evidence_index"]} == {
        row["evidence_id"]
        for row in [*bundle["transcript_evidence"], *bundle["comment_evidence"]]
    }


def test_bundle_fails_loud_when_either_modality_is_missing() -> None:
    with pytest.raises(ValueError, match="INCOMPLETE_AUDIENCE_EVIDENCE.*transcript"):
        _bundle(transcript=False)
    payload = _payload()
    with pytest.raises(ValueError, match="missing persisted Silver"):
        build_creator_audience_evidence_bundle(
            creator_id="tiktok:@alpha",
            profile_subject_id="platform_account:tiktok:alpha",
            raw_anchor=RAW_ANCHOR,
            batch_payload=payload,
            comment_attention_records=[],
            grid_observation_refs=[],
            question="q",
            evidence_cutoff=OBSERVED,
        )


def test_subscription_prompt_has_no_api_path_and_validator_closes_evidence() -> None:
    bundle = _bundle()
    prompt = build_triangulation_prompt(bundle)
    assert "Omit snapshot_id" in prompt
    assert "do not use the word ritual" in prompt
    snapshot = parse_triangulation_response(json.dumps(_response(bundle)), bundle)
    assert snapshot.snapshot_id.startswith("cats_")
    assert snapshot.input_bundle_hash == bundle["bundle_hash"]


def test_validator_rejects_majority_language_and_single_video_effect_claim() -> None:
    bundle = _bundle()
    response = _response(bundle)
    response["creator_signal_projection"]["hire_verdict"]["statement"] = "Most of the audience wants this."
    with pytest.raises(ValueError, match="majority language"):
        parse_triangulation_response(json.dumps(response), bundle)

    response = _response(bundle)
    claim = response["judgment_claim_set"]["claims"][0]
    first = bundle["comment_evidence"][0]
    claim["representative_evidence_ids"] = [first["evidence_id"]]
    claim["all_support_evidence_ids"] = [first["evidence_id"]]
    claim["source_video_ids"] = [first["video_id"]]
    claim["support_scope"] = "single_video"
    with pytest.raises(ValueError, match="needs two videos"):
        parse_triangulation_response(json.dumps(response), bundle)

    response = _response(bundle)
    claim = response["judgment_claim_set"]["claims"][0]
    first = bundle["comment_evidence"][0]
    claim["statement"] = "The comparison format generates observed engagement."
    claim["representative_evidence_ids"] = [first["evidence_id"]]
    claim["all_support_evidence_ids"] = [first["evidence_id"]]
    claim["source_video_ids"] = [first["video_id"]]
    claim["support_scope"] = "single_video"
    with pytest.raises(ValueError, match="needs two videos"):
        parse_triangulation_response(json.dumps(response), bundle)


def test_prepare_reads_packet_scoped_persisted_silver_and_uses_no_api(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    grid_window, selection = _onboarding_evidence_payloads()
    code, admitted = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        grid_window_json=grid_window,
        selection_result_json=selection,
        data_root=data_root,
        capture_timestamp="2026-06-30T17:02:46Z",
    )
    assert code == 0
    packet_id = admitted.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    assert run_tiktok_grid_observations(data_root=data_root, packet_ids=[packet_id])[0]["status"] == "derived"
    assert run_comment_attention(data_root=data_root, packet_ids=[packet_id])[0]["status"] == "derived"

    attention_dir = data_root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=COMMENT_ATTENTION_LANE
    )
    current_attention_path = next(path for path in attention_dir.iterdir() if path.is_file())
    current_attention = json.loads(current_attention_path.read_text())
    stale_attention = copy.deepcopy(current_attention)
    stale_attention["record_id"] = "stale_comment_attention_policy"
    stale_attention["provenance"]["calculation_recipe_version"] = "stale_recipe"
    stale_attention["provenance"]["policy_fingerprint_sha256"] = "0" * 64
    stale_attention["content_hash"] = f"sha256:{silver_content_hash(stale_attention)}"
    append_silver_record(
        data_root,
        raw_anchor=packet_id,
        lane=COMMENT_ATTENTION_LANE,
        record_id=stale_attention["record_id"],
        record=stale_attention,
    )

    bundle_out = tmp_path / "bundle.json"
    prompt_out = tmp_path / "prompt.txt"
    receipt = prepare_subscription_judgment(
        data_root=data_root,
        packet_id=packet_id,
        creator_id="tiktok:@funmimonet",
        profile_subject_id="platform_account:tiktok:funmimonet",
        question="What should a matching brand hire this creator to accomplish?",
        evidence_cutoff="2026-06-30T17:02:46Z",
        bundle_out=bundle_out,
        prompt_out=prompt_out,
    )

    assert receipt["status"] == "SUBSCRIPTION_JUDGMENT_REQUIRED"
    assert receipt["model_api_calls"] == 0
    assert receipt["silver_selection_residual_count"] == 1
    bundle = json.loads(bundle_out.read_text(encoding="utf-8"))
    assert bundle["source_refs"]["silver_selection_residuals"] == [{
        "actual_policy_fingerprint_sha256": "0" * 64,
        "actual_policy_version": "stale_recipe",
        "lane": COMMENT_ATTENTION_LANE,
        "record_id": "stale_comment_attention_policy",
        "status": "policy_mismatch",
    }]
    assert bundle_out.exists() and prompt_out.exists()
    coordinated = prepare_onboarding(
        data_root=data_root,
        packet_id=packet_id,
        creator_id="tiktok:@funmimonet",
        profile_subject_id="platform_account:tiktok:funmimonet",
        question="What should a matching brand hire this creator to accomplish?",
        evidence_cutoff="2026-06-30T17:02:46Z",
        work_dir=tmp_path / "coordinated",
    )
    assert coordinated["status"] == "awaiting_judgment"
    assert coordinated["stage_reached"] == "judgment_prepared"
    assert coordinated["silver_prerequisites"] == {
        "grid_observation": "already_current",
        "comment_attention": "already_current",
    }
    assert coordinated["recapture_required"] is False

    current_attention["raw_refs"][0]["sha256"] = "0" * 64
    current_attention["content_hash"] = f"sha256:{silver_content_hash(current_attention)}"
    current_attention_path.write_text(json.dumps(current_attention), encoding="utf-8")
    with pytest.raises(ValueError, match="missing persisted Silver comment attention"):
        prepare_subscription_judgment(
            data_root=data_root,
            packet_id=packet_id,
            creator_id="tiktok:@funmimonet",
            profile_subject_id="platform_account:tiktok:funmimonet",
            question="What should a matching brand hire this creator to accomplish?",
            evidence_cutoff="2026-06-30T17:02:46Z",
            bundle_out=tmp_path / "tampered-bundle.json",
            prompt_out=tmp_path / "tampered-prompt.txt",
        )


def test_bundle_incomplete_when_comments_absent_but_transcript_present() -> None:
    payload = _payload()
    for video in payload["videos"]:
        video["comments"]["comments"] = []
    with pytest.raises(ValueError, match=r"INCOMPLETE_AUDIENCE_EVIDENCE.*comment"):
        build_creator_audience_evidence_bundle(
            creator_id="tiktok:@alpha",
            profile_subject_id="platform_account:tiktok:alpha",
            raw_anchor=RAW_ANCHOR,
            batch_payload=payload,
            comment_attention_records=[],
            grid_observation_refs=[{"record_id": "grid-1", "video_id": "v1"}],
            question="Who is this creator commercially useful for?",
            evidence_cutoff=OBSERVED,
        )


def test_validator_rejects_claim_citing_unknown_evidence() -> None:
    bundle = _bundle()
    response = _response(bundle)
    claim = response["judgment_claim_set"]["claims"][0]
    claim["all_support_evidence_ids"] = claim["all_support_evidence_ids"] + ["ttce_absent"]
    claim["representative_evidence_ids"] = ["ttce_absent"]
    with pytest.raises(ValueError, match="cites unknown evidence"):
        parse_triangulation_response(json.dumps(response), bundle)


def test_validator_rejects_response_for_a_different_creator() -> None:
    bundle = _bundle()
    response = _response(bundle)
    response["creator_id"] = "tiktok:@someoneelse"
    with pytest.raises(ValueError, match="does not match evidence bundle"):
        parse_triangulation_response(json.dumps(response), bundle)


def test_validator_rejects_guaranteed_outcome_language() -> None:
    bundle = _bundle()
    response = _response(bundle)
    response["creator_signal_projection"]["hire_verdict"]["statement"] = (
        "Hire her for guaranteed conversion."
    )
    with pytest.raises(ValueError, match="guarantees an unobserved outcome"):
        parse_triangulation_response(json.dumps(response), bundle)


def test_validator_rejects_non_not_estimated_demographics() -> None:
    bundle = _bundle()
    response = _response(bundle)
    response["actual_audience_demographics"] = "mostly_women_25_34"
    with pytest.raises(ValueError):
        parse_triangulation_response(json.dumps(response), bundle)


def test_validator_language_guards_cover_robustness_stamp() -> None:
    bundle = _bundle()
    response = _response(bundle)
    response["creator_signal_projection"]["robustness_stamp"] = (
        "Held after removing the top-liked comment; guaranteed conversion persists."
    )
    with pytest.raises(ValueError, match="guarantees an unobserved outcome"):
        parse_triangulation_response(json.dumps(response), bundle)

    response = _response(bundle)
    response["creator_signal_projection"]["robustness_stamp"] = (
        "Held for most of the audience after removing the top-liked comment."
    )
    with pytest.raises(ValueError, match="majority language"):
        parse_triangulation_response(json.dumps(response), bundle)

def test_validator_derives_source_video_ids_from_support() -> None:
    bundle = _bundle()
    response = _response(bundle)
    response["judgment_claim_set"]["claims"][0].pop("source_video_ids")

    snapshot = parse_triangulation_response(json.dumps(response), bundle)

    assert snapshot.judgment_claim_set.claims[0].source_video_ids == ["v1", "v2"]


def test_validator_reports_all_independent_relational_defects() -> None:
    bundle = _bundle()
    response = _response(bundle)
    claim = response["judgment_claim_set"]["claims"][0]
    claim["all_support_evidence_ids"].append("ttce_absent")
    claim["representative_evidence_ids"] = [
        bundle["transcript_evidence"][0]["evidence_id"]
    ]
    response["creator_signal_projection"]["hire_verdict"]["statement"] = (
        "Most of the audience will convert."
    )

    with pytest.raises(TriangulationValidationError) as captured:
        parse_triangulation_response(json.dumps(response), bundle)

    assert any("cites unknown evidence" in error for error in captured.value.errors)
    assert any(
        "representative evidence is outside full support" in error
        for error in captured.value.errors
    )
    assert any("unsupported majority language" in error for error in captured.value.errors)

    schema_response = _response(bundle)
    schema_claim = schema_response["judgment_claim_set"]["claims"][0]
    schema_claim["all_support_evidence_ids"] = ["ttce_absent"]
    schema_claim["representative_evidence_ids"] = ["ttce_absent"]
    with pytest.raises(TriangulationValidationError) as schema_captured:
        parse_triangulation_response(json.dumps(schema_response), bundle)
    assert any(
        "cites unknown evidence" in error for error in schema_captured.value.errors
    )
    assert any(
        "source_video_ids" in error for error in schema_captured.value.errors
    )


def test_submission_persists_exact_bytes_and_gates_materialization(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle = _bundle()
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")

    blocked_response = _response(bundle)
    blocked_claim = blocked_response["judgment_claim_set"]["claims"][0]
    blocked_claim["all_support_evidence_ids"].append("ttce_absent")
    blocked_response["creator_signal_projection"]["hire_verdict"]["statement"] = (
        "Most of the audience will convert."
    )
    blocked_bytes = json.dumps(blocked_response).encode("utf-8")
    blocked_snapshot = tmp_path / "blocked.snapshot.json"
    blocked = submit_subscription_judgment(
        data_root=data_root,
        bundle_path=bundle_path,
        response_bytes=blocked_bytes,
        snapshot_out=blocked_snapshot,
    )

    assert blocked["status"] == "blocked"
    assert blocked["recapture_required"] is False
    assert len(blocked["validation_errors"]) >= 2
    assert not blocked_snapshot.exists()
    blocked_outcome = CreatorAudienceJudgmentOutcome.model_validate(
        json.loads(Path(blocked["judgment_outcome_path"]).read_text(encoding="utf-8"))
    )
    assert base64.b64decode(blocked_outcome.response_bytes_b64) == blocked_bytes

    valid_bytes = json.dumps(_response(bundle)).encode("utf-8")
    snapshot_path = tmp_path / "validated.snapshot.json"
    validated = submit_subscription_judgment(
        data_root=data_root,
        bundle_path=bundle_path,
        response_bytes=valid_bytes,
        snapshot_out=snapshot_path,
    )
    repeated = submit_subscription_judgment(
        data_root=data_root,
        bundle_path=bundle_path,
        response_bytes=valid_bytes,
        snapshot_out=snapshot_path,
    )

    assert validated == repeated
    outcome_path = Path(validated["judgment_outcome_path"])
    _verify_audience_judgment_outcomes((snapshot_path,), (outcome_path,))

    snapshot_path.write_bytes(snapshot_path.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="bytes do not match"):
        _verify_audience_judgment_outcomes((snapshot_path,), (outcome_path,))
