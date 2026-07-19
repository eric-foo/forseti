from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_LANE,
    COMMENT_ATTENTION_POLICY_FINGERPRINT,
    build_comment_attention_records,
)
from evidence_binding.tiktok_audience_triangulation import (
    ASSEMBLY_RECEIPT_LANE,
    build_assembly_receipt,
    build_creator_audience_evidence_bundle,
)
from judgment.creator_audience import (
    LEGACY_V0_METHOD_PATH,
    LEGACY_V0_METHOD_SHA256,
    METHOD_DECK_RELATIVE_PATH,
    build_compact_judgment_view,
    load_method_deck,
    parse_creator_audience_response,
)
from judgment.tiktok_audience_triangulation import (
    TriangulationValidationError,
    build_triangulation_prompt,
    parse_triangulation_response,
    validate_triangulation_snapshot,
)
from data_lake.root import DataLakeRoot
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    SilverRecordError,
    SilverSourceAuthority,
    append_silver_record,
    classify_silver_vault_record_sources,
    silver_content_hash,
    validate_silver_vault_record_for_write,
)
from runners.run_tiktok_comment_attention_producer import run_comment_attention
from runners.run_creator_profile_current_materialize import _verify_audience_judgment_outcomes
from runners.run_tiktok_creator_audience_triangulation import (
    _silver_eligibility_residual,
    prepare_subscription_judgment,
    select_current_audience_silver_records,
    submit_subscription_judgment,
)
from _silver_compatibility_fixture_lake import materialize_fixture_lake
import runners.run_tiktok_creator_audience_triangulation as triangulation_runner
from runners.run_tiktok_creator_onboarding_coordinator import prepare_onboarding
import runners.run_tiktok_creator_onboarding_coordinator as onboarding_coordinator
from runners.run_tiktok_grid_observation_producer import run_tiktok_grid_observations
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from source_capture.tiktok.grid_packet import write_tiktok_grid_packet
from schemas.creator_audience_models import (
    CreatorAudienceJudgmentOutcomeV1 as CreatorAudienceJudgmentOutcome,
)
from test_tiktok_batch_admission import (
    PROFILE_URL,
    _cadence_payload,
    _grid_payload,
    _onboarding_evidence_payloads,
)


OBSERVED = "2026-07-12T00:00:00Z"
RAW_ANCHOR = "01TESTAUDIENCEPACKET"
_, METHOD_DECK_SHA256 = load_method_deck()


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
        method_deck_path=METHOD_DECK_RELATIVE_PATH,
        method_deck_sha256=METHOD_DECK_SHA256,
    )


def test_tiktok_bundle_carries_prepare_time_method_binding() -> None:
    bundle = _bundle()
    assert bundle["method_deck_path"] == METHOD_DECK_RELATIVE_PATH
    assert bundle["method_deck_sha256"] == METHOD_DECK_SHA256


def _persist_assembly_receipt(data_root: DataLakeRoot, bundle: dict) -> None:
    receipt = build_assembly_receipt(bundle)
    data_root.append_record(
        subtree="derived",
        raw_anchor=bundle["raw_anchor"],
        lane=ASSEMBLY_RECEIPT_LANE,
        record_id=receipt["record_id"],
        data=(
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode(
                "utf-8"
            )
            + b"\n"
        ),
    )


def test_silver_eligibility_preserves_historical_compatibility_reason(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(
        triangulation_runner,
        "classify_silver_vault_record_sources",
        lambda _root, _record: SilverSourceAuthority(
            "historical_compatible",
            "legacy_tiktok_comment_attention_v1_bytes_verified",
        ),
    )

    residual = _silver_eligibility_residual(
        root, {"record_id": "legacy-v1.json"}, lane=COMMENT_ATTENTION_LANE
    )

    assert residual == {
        "lane": COMMENT_ATTENTION_LANE,
        "record_id": "legacy-v1.json",
        "status": "historical_compatible",
        "reason_code": "legacy_tiktok_comment_attention_v1_bytes_verified",
    }


def test_known_time_tiktok_v1_stays_current_write_retired_and_policy_excluded(
    tmp_path: Path,
) -> None:
    """Composed v1 regression (PR #1006 F-3): a known-time TikTok v1 record is
    physically current_source_backed, is closed to new writes, and is excluded
    by the current triangulation reader with a policy_mismatch residual, while
    the null-time v1 sibling stays a historical_compatible residual."""
    root = DataLakeRoot.for_test(tmp_path / "lake")
    seeded = materialize_fixture_lake(root)
    null_time, _null_path = seeded["tiktok_comment_attention_v1"]
    known_time = copy.deepcopy(null_time)
    known_time["record_id"] = "comment_attention_known_time_fixture.json"
    known_time["observed_at"] = known_time["payload"]["observation"]["temporal_pairing"][
        "video_stats_observed_at"
    ]
    known_time["content_hash"] = f"sha256:{silver_content_hash(known_time)}"

    authority = classify_silver_vault_record_sources(root, known_time)
    assert authority.status == CURRENT_SOURCE_BACKED_AUTHORITY

    with pytest.raises(SilverRecordError, match="read-only compatibility"):
        validate_silver_vault_record_for_write(known_time)

    v1_fingerprint = known_time["provenance"]["policy_fingerprint_sha256"]
    assert v1_fingerprint != COMMENT_ATTENTION_POLICY_FINGERPRINT

    attention, grid, residuals = select_current_audience_silver_records(
        data_root=root,
        comment_attention_records=[known_time, null_time],
        grid_observation_records=[],
    )
    assert attention == []
    assert grid == []
    assert residuals == [
        {
            "lane": COMMENT_ATTENTION_LANE,
            "record_id": known_time["record_id"],
            "status": "policy_mismatch",
            "actual_policy_version": "tiktok_comment_attention_ratio_v1",
            "actual_policy_fingerprint_sha256": v1_fingerprint,
        },
        {
            "lane": COMMENT_ATTENTION_LANE,
            "record_id": null_time["record_id"],
            "status": "historical_compatible",
            "reason_code": "legacy_tiktok_comment_attention_v1_bytes_verified",
        },
    ]


def _validated_submission(tmp_path: Path) -> tuple[Path, Path]:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle = _bundle()
    _persist_assembly_receipt(data_root, bundle)
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
    snapshot_path = tmp_path / "snapshot.json"
    result = submit_subscription_judgment(
        data_root=data_root,
        bundle_path=bundle_path,
        response_bytes=json.dumps(_response(bundle)).encode("utf-8"),
        snapshot_out=snapshot_path,
    )
    return snapshot_path, Path(result["judgment_outcome_path"])
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


def test_bundle_preserves_raw_duplicate_lineage_and_compact_view_dedupes() -> None:
    bundle = _bundle(duplicate_text=True)
    assert len(bundle["transcript_evidence"]) == 2
    assert len(bundle["comment_evidence"]) == 2
    assert bundle["exact_duplicate_clusters"][0]["multiplicity"] == 2
    assert all(row["comment_attention_record_id"] for row in bundle["comment_evidence"])
    assert all(row["temporal_alignment"] == "same_capture_observation" for row in bundle["comment_evidence"])
    view = build_compact_judgment_view(bundle)
    compact_comments = [
        row for row in view["evidence"] if row["kind"] == "observed_comment"
    ]
    assert len(compact_comments) == 1
    assert compact_comments[0]["duplicate_multiplicity"] == 2
    assert compact_comments[0]["source_item_ids"] == ["v1", "v2"]
    assert len(compact_comments[0]["comment_mechanics"]) == 2
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
            method_deck_path=METHOD_DECK_RELATIVE_PATH,
            method_deck_sha256=METHOD_DECK_SHA256,
        )


def test_subscription_prompt_has_no_api_path_and_validator_closes_evidence() -> None:
    bundle = _bundle()
    prompt = build_triangulation_prompt(bundle)
    assert "Omit snapshot_id" in prompt
    assert "do not use the word ritual" in prompt
    assert "For relation missing" in prompt
    assert "counterevidence does not count toward support scope" in prompt
    snapshot = parse_triangulation_response(json.dumps(_response(bundle)), bundle)
    assert snapshot.snapshot_id.startswith("cats_")
    assert snapshot.input_bundle_hash == bundle["bundle_hash"]


def test_validator_accepts_uncited_missing_claim_but_keeps_supported_claims_strict() -> None:
    bundle = _bundle()
    response = _response(bundle)
    missing_claim = {
        "claim_id": "missing-1",
        "axis": "purchase_decision_stage",
        "statement": "Conversion and attribution evidence is missing.",
        "commercial_implication": "Do not forecast sales from this capture.",
        "modality": "fused",
        "relation": "missing",
        "support_scope": "content_only",
        "representative_evidence_ids": [],
        "all_support_evidence_ids": [],
        "counterevidence_ids": [],
        "limitation": "No transaction, click, code-use, or lift data was supplied.",
    }
    response["judgment_claim_set"]["claims"].append(missing_claim)

    snapshot = parse_triangulation_response(json.dumps(response), bundle)

    accepted = snapshot.judgment_claim_set.claims[-1]
    assert accepted.relation == "missing"
    assert accepted.source_video_ids == []

    supported_without_evidence = _response(bundle)
    claim = supported_without_evidence["judgment_claim_set"]["claims"][0]
    claim["representative_evidence_ids"] = []
    claim["all_support_evidence_ids"] = []
    with pytest.raises(
        TriangulationValidationError, match="non-missing claims require"
    ):
        parse_triangulation_response(json.dumps(supported_without_evidence), bundle)


def test_validator_rejects_evidence_citations_on_missing_claim() -> None:
    bundle = _bundle()
    response = _response(bundle)
    claim = response["judgment_claim_set"]["claims"][0]
    claim["relation"] = "missing"
    with pytest.raises(
        TriangulationValidationError, match="missing claims must not cite evidence"
    ):
        parse_triangulation_response(json.dumps(response), bundle)



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
        "grid_packet_id": packet_id,
        "comment_attention": "already_current",
        "comment_packet_id": packet_id,
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


def test_coordinator_reuses_batch_evidence_with_separate_current_grid_packet(
    tmp_path: Path,
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    grid_window, _selection = _onboarding_evidence_payloads()
    code, admitted = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        data_root=data_root,
        capture_timestamp="2026-06-30T17:02:46Z",
    )
    assert code == 0
    batch_packet_id = Path(admitted).name
    code, grid_admitted = write_tiktok_grid_packet(
        grid_window_json=grid_window,
        data_root=data_root,
        observed_at_utc="2026-07-19T11:42:13Z",
    )
    assert code == 0
    grid_packet_id = Path(grid_admitted).name
    assert run_comment_attention(
        data_root=data_root,
        packet_ids=[batch_packet_id],
    )[0]["status"] == "derived"
    assert run_tiktok_grid_observations(
        data_root=data_root,
        packet_ids=[grid_packet_id],
    )[0]["status"] == "derived"

    coordinated = prepare_onboarding(
        data_root=data_root,
        packet_id=batch_packet_id,
        grid_packet_id=grid_packet_id,
        creator_id="tiktok:@funmimonet",
        profile_subject_id="platform_account:tiktok:funmimonet",
        question="What should a matching brand hire this creator to accomplish?",
        evidence_cutoff="2026-06-30T17:02:46Z",
        work_dir=tmp_path / "coordinated-reuse",
    )

    assert coordinated["status"] == "awaiting_judgment"
    assert coordinated["recapture_required"] is False
    assert coordinated["grid_packet_id"] == grid_packet_id
    assert coordinated["silver_prerequisites"] == {
        "grid_observation": "already_current",
        "grid_packet_id": grid_packet_id,
        "comment_attention": "already_current",
        "comment_packet_id": batch_packet_id,
    }
    bundle = json.loads(Path(coordinated["bundle_out"]).read_text(encoding="utf-8"))
    assert bundle["raw_anchor"] == batch_packet_id
    assert bundle["source_refs"]["raw_packet_id"] == batch_packet_id
    assert {
        row["raw_anchor"] for row in bundle["source_refs"]["grid_observation_refs"]
    } == {grid_packet_id}


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
            method_deck_path=METHOD_DECK_RELATIVE_PATH,
            method_deck_sha256=METHOD_DECK_SHA256,
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
    _persist_assembly_receipt(data_root, bundle)
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


def test_submission_blocks_non_string_evidence_references(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle = _bundle()
    _persist_assembly_receipt(data_root, bundle)
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")

    response = _response(bundle)
    response["judgment_claim_set"]["claims"][0]["all_support_evidence_ids"] = [{"evil": 1}]
    response_bytes = json.dumps(response).encode("utf-8")

    result = submit_subscription_judgment(
        data_root=data_root,
        bundle_path=bundle_path,
        response_bytes=response_bytes,
        snapshot_out=tmp_path / "snapshot.json",
    )

    assert result["status"] == "blocked"
    assert any(
        "non-string evidence references" in error for error in result["validation_errors"]
    )
    outcome = CreatorAudienceJudgmentOutcome.model_validate(
        json.loads(Path(result["judgment_outcome_path"]).read_text(encoding="utf-8"))
    )
    assert outcome.status == "blocked"
    assert base64.b64decode(outcome.response_bytes_b64) == response_bytes


def test_submission_rejects_bundle_whose_hash_does_not_close_over_content(tmp_path) -> None:
    bundle = _bundle()
    fabricated = dict(bundle["comment_evidence"][0])
    fabricated["evidence_id"] = "ttce_fabricated"
    fabricated["text"] = "I bought this immediately."
    bundle["comment_evidence"] = [*bundle["comment_evidence"], fabricated]
    bundle_path = tmp_path / "tampered.bundle.json"
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")

    with pytest.raises(ValueError, match="does not close over bundle content"):
        submit_subscription_judgment(
            data_root=DataLakeRoot.for_test(tmp_path / "lake"),
            bundle_path=bundle_path,
            response_bytes=json.dumps(_response(bundle)).encode("utf-8"),
            snapshot_out=tmp_path / "snapshot.json",
        )




def test_submission_rejects_rehashed_bundle_without_persisted_receipt(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bundle = _bundle()
    _persist_assembly_receipt(data_root, bundle)

    fabricated = dict(bundle["comment_evidence"][0])
    fabricated["evidence_id"] = "ttce_fabricated"
    fabricated["text"] = "I bought this immediately."
    bundle["comment_evidence"] = [*bundle["comment_evidence"], fabricated]
    core = {
        key: value
        for key, value in bundle.items()
        if key not in {"bundle_hash", "bundle_id", "serialized_utf8_bytes"}
    }
    canonical_core = json.dumps(
        core, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    bundle["bundle_hash"] = f"sha256:{hashlib.sha256(canonical_core).hexdigest()}"
    identity = f'{bundle["raw_anchor"]}\0{bundle["bundle_hash"]}'.encode("utf-8")
    bundle["bundle_id"] = f"caeb_{hashlib.sha256(identity).hexdigest()[:20]}"
    serialized = {
        key: value for key, value in bundle.items() if key != "serialized_utf8_bytes"
    }
    bundle["serialized_utf8_bytes"] = len(
        json.dumps(
            serialized, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )
    bundle_path = tmp_path / "rehashed.bundle.json"
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")

    with pytest.raises(ValueError, match="persisted audience assembly receipt is missing"):
        submit_subscription_judgment(
            data_root=data_root,
            bundle_path=bundle_path,
            response_bytes=json.dumps(_response(bundle)).encode("utf-8"),
            snapshot_out=tmp_path / "snapshot.json",
        )


def test_complete_onboarding_publishes_only_verified_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    snapshot_path, outcome_path = _validated_submission(tmp_path)
    output_path = tmp_path / "creator_profile_current.json"
    previous = b'{"previous":true}\n'
    output_path.write_bytes(previous)

    def fake_materialize(argv: list[str]) -> int:
        candidate = Path(argv[argv.index("--output") + 1])
        candidate.write_text('{"creator_profile_current_view":{}}', encoding="utf-8")
        return 0

    monkeypatch.setattr(onboarding_coordinator, "materialize_main", fake_materialize)
    with pytest.raises(ValueError, match="no profiles list"):
        onboarding_coordinator.complete_onboarding(
            snapshot_path=snapshot_path,
            outcome_path=outcome_path,
            output_path=output_path,
            account_ledger_path=tmp_path / "ledger.json",
            creator_registry_index_path=tmp_path / "registry.json",
            metric_seed_paths=(),
            generated_at_utc=None,
            preflight_receipt_path=None,
        )

    assert output_path.read_bytes() == previous
    assert not list(tmp_path.glob(f".{output_path.name}.*.candidate"))


def test_complete_onboarding_preserves_retained_audience_pairs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    snapshot_path, outcome_path = _validated_submission(tmp_path)
    retained_snapshot = tmp_path / "retained_snapshot.json"
    retained_outcome = tmp_path / "retained_outcome.json"
    output_path = tmp_path / "creator_profile_current.json"
    output_path.write_text(
        '{"creator_profile_current_view":{"profiles":[]}}\n',
        encoding="utf-8",
    )
    observed_argv: list[str] = []
    outcome = json.loads(outcome_path.read_text(encoding="utf-8"))

    def fake_materialize(argv: list[str]) -> int:
        observed_argv.extend(argv)
        candidate = Path(argv[argv.index("--output") + 1])
        candidate.write_text(
            json.dumps(
                {
                    "creator_profile_current_view": {
                        "profiles": [
                            {
                                "profile_subject_id": outcome["profile_subject_id"],
                                "audience_triangulation": {
                                    "snapshot_id": outcome["snapshot_id_or_none"],
                                    "input_bundle_hash": outcome["bundle_hash"],
                                },
                            }
                        ]
                    }
                }
            ),
            encoding="utf-8",
        )
        return 0

    monkeypatch.setattr(onboarding_coordinator, "materialize_main", fake_materialize)
    result = onboarding_coordinator.complete_onboarding(
        snapshot_path=snapshot_path,
        outcome_path=outcome_path,
        retained_snapshot_paths=(retained_snapshot,),
        retained_outcome_paths=(retained_outcome,),
        output_path=output_path,
        account_ledger_path=tmp_path / "ledger.json",
        creator_registry_index_path=tmp_path / "registry.json",
        metric_seed_paths=(),
        generated_at_utc=None,
        preflight_receipt_path=None,
    )

    assert result["stage_reached"] == "verified_materialization"
    snapshot_values = [
        observed_argv[index + 1]
        for index, value in enumerate(observed_argv)
        if value == "--audience-triangulation-snapshot"
    ]
    outcome_values = [
        observed_argv[index + 1]
        for index, value in enumerate(observed_argv)
        if value == "--audience-judgment-outcome"
    ]
    assert snapshot_values == [str(retained_snapshot), str(snapshot_path)]
    assert outcome_values == [str(retained_outcome), str(outcome_path)]


def test_retained_audience_pairs_are_discovered_from_hash_bound_source_inputs(
    tmp_path: Path,
) -> None:
    registry_dir = (
        Path(__file__).resolve().parents[3]
        / "forseti/product/spines/capture/core/source_families/social_media"
        / "creator_registry"
    )
    snapshot_path = (
        registry_dir
        / "ak_fragrances1_creator_audience_triangulation_snapshot_v1.json"
    )
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    previous_document = {
        "creator_profile_current_view": {
            "profiles": [
                {
                    "profile_subject_id": snapshot["profile_subject_id"],
                    "audience_triangulation": snapshot,
                }
            ],
            "source_inputs": [
                {
                    "role": (
                        "validated transcript/comment audience triangulation snapshots"
                    ),
                    "source_pointer": str(snapshot_path),
                    "sha256": hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
                }
            ],
        }
    }

    snapshots, outcomes = (
        onboarding_coordinator._discover_retained_audience_pairs(
            previous_document=previous_document,
            target_profile_subject_id="platform_account:tiktok:new_creator",
        )
    )

    assert snapshots == (snapshot_path,)
    assert len(outcomes) == 1
    assert outcomes[0].name == (
        "ak_fragrances1_creator_audience_judgment_outcome_v1.json"
    )

    isolated_snapshot = tmp_path / snapshot_path.name
    isolated_snapshot.write_bytes(snapshot_path.read_bytes())
    previous_document["creator_profile_current_view"]["source_inputs"][0].update(
        {
            "source_pointer": str(isolated_snapshot),
            "sha256": hashlib.sha256(isolated_snapshot.read_bytes()).hexdigest(),
        }
    )
    with pytest.raises(ValueError, match="exactly one successful sibling"):
        onboarding_coordinator._discover_retained_audience_pairs(
            previous_document=previous_document,
            target_profile_subject_id="platform_account:tiktok:new_creator",
        )


@pytest.mark.parametrize("perturbation", ["missing", "changed"])
def test_complete_onboarding_refuses_existing_audience_join_loss_or_change(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    perturbation: str,
) -> None:
    snapshot_path, outcome_path = _validated_submission(tmp_path)
    output_path = tmp_path / "creator_profile_current.json"
    previous_join = {
        "snapshot_id": "cats_existing",
        "input_bundle_hash": "sha256:" + "1" * 64,
    }
    previous_document = {
        "creator_profile_current_view": {
            "profiles": [
                {
                    "profile_subject_id": "acct_existing",
                    "audience_triangulation": previous_join,
                }
            ]
        }
    }
    previous_bytes = (
        json.dumps(previous_document, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    output_path.write_bytes(previous_bytes)
    outcome = json.loads(outcome_path.read_text(encoding="utf-8"))

    def fake_materialize(argv: list[str]) -> int:
        candidate = Path(argv[argv.index("--output") + 1])
        profiles = [
            {
                "profile_subject_id": outcome["profile_subject_id"],
                "audience_triangulation": {
                    "snapshot_id": outcome["snapshot_id_or_none"],
                    "input_bundle_hash": outcome["bundle_hash"],
                },
            }
        ]
        if perturbation == "changed":
            profiles.append(
                {
                    "profile_subject_id": "acct_existing",
                    "audience_triangulation": {
                        **previous_join,
                        "snapshot_id": "cats_changed",
                    },
                }
            )
        candidate.write_text(
            json.dumps(
                {"creator_profile_current_view": {"profiles": profiles}},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return 0

    monkeypatch.setattr(onboarding_coordinator, "materialize_main", fake_materialize)
    with pytest.raises(
        ValueError,
        match=(
            "existing audience_triangulation join was not preserved.*"
            f"join is missing" if perturbation == "missing" else
            "existing audience_triangulation join was not preserved.*join changed"
        ),
    ):
        onboarding_coordinator.complete_onboarding(
            snapshot_path=snapshot_path,
            outcome_path=outcome_path,
            retained_snapshot_paths=(tmp_path / "retained.snapshot.json",),
            retained_outcome_paths=(tmp_path / "retained.outcome.json",),
            output_path=output_path,
            account_ledger_path=tmp_path / "ledger.json",
            creator_registry_index_path=tmp_path / "registry.json",
            metric_seed_paths=(),
            generated_at_utc=None,
            preflight_receipt_path=None,
        )

    assert output_path.read_bytes() == previous_bytes


def test_complete_onboarding_rejects_unpaired_retained_inputs(tmp_path: Path) -> None:
    snapshot_path, outcome_path = _validated_submission(tmp_path)

    with pytest.raises(
        ValueError,
        match="retained audience snapshot and Judgment outcome counts must match",
    ):
        onboarding_coordinator.complete_onboarding(
            snapshot_path=snapshot_path,
            outcome_path=outcome_path,
            retained_snapshot_paths=(tmp_path / "retained_snapshot.json",),
            retained_outcome_paths=(),
            output_path=tmp_path / "creator_profile_current.json",
            account_ledger_path=tmp_path / "ledger.json",
            creator_registry_index_path=tmp_path / "registry.json",
            metric_seed_paths=(),
            generated_at_utc=None,
            preflight_receipt_path=None,
        )


def test_complete_onboarding_preserves_materializer_diagnostic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    snapshot_path, outcome_path = _validated_submission(tmp_path)
    output_path = tmp_path / "creator_profile_current.json"
    previous = b'{"previous":true}\n'
    output_path.write_bytes(previous)

    def failing_materialize(argv: list[str]) -> int:
        candidate = Path(argv[argv.index("--output") + 1])
        candidate.write_text("partial", encoding="utf-8")
        print("specific preflight blocker", file=sys.stderr)
        raise SystemExit(2)

    monkeypatch.setattr(onboarding_coordinator, "materialize_main", failing_materialize)
    with pytest.raises(ValueError, match="specific preflight blocker"):
        onboarding_coordinator.complete_onboarding(
            snapshot_path=snapshot_path,
            outcome_path=outcome_path,
            output_path=output_path,
            account_ledger_path=tmp_path / "ledger.json",
            creator_registry_index_path=tmp_path / "registry.json",
            metric_seed_paths=(),
            generated_at_utc=None,
            preflight_receipt_path=None,
        )

    assert output_path.read_bytes() == previous
    assert not list(tmp_path.glob(f".{output_path.name}.*.candidate"))
def test_validator_rejects_source_video_ids_that_do_not_close_over_support() -> None:
    bundle = _bundle()
    snapshot = parse_triangulation_response(json.dumps(_response(bundle)), bundle)

    tampered = snapshot.model_copy(deep=True)
    tampered.judgment_claim_set.claims[0].source_video_ids = ["v1", "v2", "v9"]

    with pytest.raises(TriangulationValidationError, match="do not close over support"):
        validate_triangulation_snapshot(tampered, bundle)


def test_legacy_v0_upgrade_does_not_claim_current_method_deck() -> None:
    bundle = _bundle()
    snapshot = parse_creator_audience_response(json.dumps(_response(bundle)), bundle)

    assert snapshot.schema_version == "creator_audience_triangulation_snapshot_v1"
    assert snapshot.method_deck_path == LEGACY_V0_METHOD_PATH
    assert snapshot.method_deck_sha256 == LEGACY_V0_METHOD_SHA256
    assert snapshot.method_deck_path != METHOD_DECK_RELATIVE_PATH


def _legacy_v0_outcome(tmp_path: Path, bundle: dict) -> tuple[Path, Path]:
    """Hand-build a persisted pre-cutover v0 Judgment outcome document."""

    response_bytes = json.dumps(_response(bundle)).encode("utf-8")
    snapshot = parse_triangulation_response(response_bytes.decode("utf-8"), bundle)
    snapshot_document = snapshot.model_dump(mode="json")
    snapshot_text = (
        json.dumps(snapshot_document, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    )
    outcome = {
        "schema_version": "creator_audience_judgment_outcome_v0",
        "record_id": "cajo_" + "0" * 20,
        "raw_anchor": bundle["raw_anchor"],
        "creator_id": bundle["creator_id"],
        "profile_subject_id": bundle["profile_subject_id"],
        "bundle_id": bundle["bundle_id"],
        "bundle_hash": bundle["bundle_hash"],
        "status": "validated",
        "response_sha256": f"sha256:{hashlib.sha256(response_bytes).hexdigest()}",
        "response_size_bytes": len(response_bytes),
        "response_bytes_b64": base64.b64encode(response_bytes).decode("ascii"),
        "validation_errors": [],
        "snapshot_id_or_none": snapshot_document["snapshot_id"],
        "snapshot_sha256_or_none": (
            f"sha256:{hashlib.sha256(snapshot_text.encode('utf-8')).hexdigest()}"
        ),
        "snapshot_or_none": snapshot_document,
        "model_api_calls": 0,
    }
    outcome_path = tmp_path / "outcome_v0.json"
    outcome_path.write_text(
        json.dumps(outcome, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    snapshot_path = tmp_path / "snapshot_v0.json"
    snapshot_path.write_text(snapshot_text, encoding="utf-8")
    return snapshot_path, outcome_path


def test_complete_onboarding_still_reads_persisted_v0_outcome(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    snapshot_path, outcome_path = _legacy_v0_outcome(tmp_path, _bundle())
    output_path = tmp_path / "creator_profile_current.json"

    def fake_materialize(argv: list[str]) -> int:
        candidate = Path(argv[argv.index("--output") + 1])
        candidate.write_text('{"creator_profile_current_view":{}}', encoding="utf-8")
        return 0

    monkeypatch.setattr(onboarding_coordinator, "materialize_main", fake_materialize)
    # Reaching the materialized-view check proves the v0 outcome document was
    # accepted; before the version dispatch this failed at outcome validation.
    with pytest.raises(ValueError, match="no profiles list"):
        onboarding_coordinator.complete_onboarding(
            snapshot_path=snapshot_path,
            outcome_path=outcome_path,
            output_path=output_path,
            account_ledger_path=tmp_path / "ledger.json",
            creator_registry_index_path=tmp_path / "registry.json",
            metric_seed_paths=(),
            generated_at_utc=None,
            preflight_receipt_path=None,
        )
