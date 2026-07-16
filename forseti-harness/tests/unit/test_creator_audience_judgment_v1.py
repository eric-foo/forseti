from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

import judgment.creator_audience as creator_audience
from data_lake.root import DataLakeRoot
from evidence_binding.instagram_audience_triangulation import (
    build_instagram_creator_audience_evidence_bundle,
)
from judgment.creator_audience import (
    METHOD_DECK_RELATIVE_PATH,
    build_capability_manifest,
    build_compact_judgment_view,
    build_creator_audience_prompt,
    load_method_deck,
    parse_creator_audience_response,
)
from judgment.tiktok_audience_triangulation import TriangulationValidationError
from runners.run_instagram_creator_audience_triangulation import (
    prepare_instagram_subscription_judgment,
)
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    REEL_TRANSCRIPT_LANE,
)


def _bundle(*, platform: str = "tiktok", eligible: bool = True) -> dict:
    _, method_hash = load_method_deck()
    return {
        "schema_version": "creator_audience_evidence_bundle_v0",
        "creator_id": f"{platform}:@alpha",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": f"platform_account:{platform}:alpha",
        "platform_scope": platform,
        "raw_anchor": "01AUDIENCEV1TEST",
        "question": "Who should hire this creator and why?",
        "evidence_cutoff": "2026-07-16T00:00:00Z",
        "method_deck_path": METHOD_DECK_RELATIVE_PATH,
        "method_deck_sha256": method_hash,
        "capture_scope": {"selected_video_ids": ["v1", "v2"]},
        "transcript_evidence": [
            {
                "evidence_id": "content-1",
                "video_id": "v1",
                "text": "I compare the product side by side.",
                "start_ms": 0,
                "end_ms": 1200,
                "source_pointer": "/private/audit/path/1",
            }
        ],
        "comment_evidence": [
            {
                "evidence_id": "comment-1",
                "video_id": "v1",
                "comment_id": "c1",
                "text": "Please compare the next release too.",
                "comment_likes": 25,
                "comment_like_rank_within_captured": 1,
                "temporal_alignment": (
                    "same_capture_observation" if eligible else "unproven"
                ),
                "comment_attention_record_id": "attention-1" if eligible else None,
                "source_pointer": "/private/audit/path/2",
            },
            {
                "evidence_id": "comment-2",
                "video_id": "v2",
                "comment_id": "c2",
                "text": "This made the trade-off easy to understand.",
                "comment_likes": 10,
                "comment_like_rank_within_captured": 2,
                "temporal_alignment": (
                    "same_capture_observation" if eligible else "unproven"
                ),
                "comment_attention_record_id": "attention-2" if eligible else None,
                "source_pointer": "/private/audit/path/3",
            },
        ],
        "bundle_id": "bundle-v1",
        "bundle_hash": "sha256:" + "a" * 64,
    }


def _semantic_response(bundle: dict, *, engagement: bool = False) -> dict:
    manifest = build_capability_manifest(bundle)
    content = [
        alias
        for alias, row in manifest["evidence"].items()
        if row["kind"] == "creator_content"
    ][0]
    comments = [
        alias
        for alias, row in manifest["evidence"].items()
        if row["kind"] == "observed_comment"
    ]
    point = {"statement": "Hire Alpha to make a difficult comparison easy to choose.", "claim_keys": ["decision"]}
    return {
        "schema_version": "creator_audience_semantic_response_v1",
        "generated_at": "2026-07-16T01:00:00Z",
        "claims": [
            {
                "claim_key": "decision",
                "axis": "purchase_decision_stage",
                "statement": "The comparison format resolves concrete trade-offs.",
                "commercial_implication": "Use Alpha when a buyer needs decision confidence.",
                "relation": "agreement",
                "representative_evidence_aliases": [content, comments[0]],
                "all_support_evidence_aliases": [content, *comments],
                "counterevidence_aliases": [],
                "limitation": "Captured comments are not a platform census.",
                "engagement_salience_relied_on": engagement,
            }
        ],
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
        "limitations": ["Captured comments are selected and incomplete."],
        "non_claims": ["not conversion evidence"],
        "actual_audience_demographics": "not_estimated",
    }


def test_prompt_embeds_method_and_compact_view_but_not_named_examples() -> None:
    bundle = _bundle()
    method_text, _ = load_method_deck()
    prompt = build_creator_audience_prompt(bundle, method_text=method_text)
    view = build_compact_judgment_view(bundle)

    assert f"METHOD_DECK_PATH: {METHOD_DECK_RELATIVE_PATH}" in prompt
    assert "METHOD_DECK_SHA256: sha256:" in prompt
    assert "category_knowledge|purchase_decision_stage|price_value_posture" in prompt
    assert "one allowed axis" not in prompt
    assert "1-5 representative aliases" in prompt
    assert "robustness_stamp to null unless a named ablation" in prompt
    assert "Hire <creator> when <campaign job>" in prompt
    assert "anywhere in the buyer-facing projection" in prompt
    assert "Hire Funmi" not in prompt
    assert "Hire Noel" not in prompt
    assert "/private/audit/path/1" not in prompt
    # Durable evidence IDs stay out of the model context: aliases only.
    assert "content-1" not in prompt
    assert "comment-1" not in prompt
    assert "capability_manifest" not in view
    assert len(view["evidence"]) == 3
    assert {row["text"] for row in view["evidence"]} == {
        row["text"]
        for key in ("transcript_evidence", "comment_evidence")
        for row in bundle[key]
    }


def test_prompt_rejects_method_text_outside_bundle_binding() -> None:
    with pytest.raises(ValueError, match="does not match the audience bundle"):
        build_creator_audience_prompt(_bundle(), method_text="tampered method")


def test_semantic_compile_uses_bundle_method_binding_without_reload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bundle = _bundle()

    def unexpected_reload() -> tuple[str, str]:
        raise AssertionError("submit-time compilation reloaded the method deck")

    monkeypatch.setattr(creator_audience, "load_method_deck", unexpected_reload)
    snapshot = parse_creator_audience_response(
        json.dumps(_semantic_response(bundle)), bundle
    )
    assert snapshot.method_deck_path == bundle["method_deck_path"]
    assert snapshot.method_deck_sha256 == bundle["method_deck_sha256"]


def test_manifest_fails_closed_on_duplicate_evidence_ids() -> None:
    bundle = _bundle()
    bundle["comment_evidence"] = [
        *bundle["comment_evidence"],
        dict(bundle["comment_evidence"][0]),
    ]
    with pytest.raises(ValueError, match="duplicate evidence_id"):
        build_capability_manifest(bundle)


def test_snapshot_rejects_blank_generated_at() -> None:
    bundle = _bundle()
    response = _semantic_response(bundle)
    response["generated_at"] = "   "
    with pytest.raises(ValidationError, match="non-blank"):
        parse_creator_audience_response(json.dumps(response), bundle)


def test_compiler_derives_clerical_fields_and_source_item_closure() -> None:
    bundle = _bundle()
    snapshot = parse_creator_audience_response(
        json.dumps(_semantic_response(bundle)), bundle
    )
    claim = snapshot.judgment_claim_set.claims[0]

    assert snapshot.schema_version == "creator_audience_triangulation_snapshot_v1"
    assert snapshot.snapshot_id.startswith("cats_")
    assert snapshot.method_deck_path == METHOD_DECK_RELATIVE_PATH
    assert claim.claim_id.startswith("cac_")
    assert claim.modality == "fused"
    assert claim.support_scope == "mixed_multi_item"
    assert claim.source_item_ids == ["v1", "v2"]
    assert snapshot.judgment_claim_set.agreements == [claim.statement]


def test_capability_manifest_and_validator_share_engagement_boundary() -> None:
    bundle = _bundle(platform="instagram", eligible=False)
    manifest = build_capability_manifest(bundle)
    assert not any(
        row["engagement_salience_eligible"]
        for row in manifest["evidence"].values()
        if row["kind"] == "observed_comment"
    )
    with pytest.raises(TriangulationValidationError, match="unavailable engagement"):
        parse_creator_audience_response(
            json.dumps(_semantic_response(bundle, engagement=True)), bundle
        )


def _instagram_records() -> tuple[list[dict], list[dict]]:
    comments = [
        {
            "record_id": "comments-r1",
            "reel_shortcode": "R1",
            "comments": [
                {
                    "comment_id": "c1",
                    "text": "Compare this with the original.",
                    "like_count": 7,
                }
            ],
        },
        {
            "record_id": "comments-r2",
            "reel_shortcode": "R2",
            "comments": [
                {
                    "comment_id": "c2",
                    "text": "I understand the difference now.",
                    "like_count": 3,
                }
            ],
        },
    ]
    transcripts = [
        {
            "record_id": "transcript-r1",
            "reel_shortcode": "R1",
            "cues": [{"start_ms": 0, "end_ms": 900, "text": "First comparison"}],
        },
        {
            "record_id": "transcript-r2",
            "reel_shortcode": "R2",
            "cues": [{"start_ms": 0, "end_ms": 900, "text": "Second comparison"}],
        },
    ]
    return comments, transcripts


def test_instagram_adapter_preserves_all_selected_evidence_without_elevation() -> None:
    comments, transcripts = _instagram_records()
    _, method_hash = load_method_deck()
    bundle = build_instagram_creator_audience_evidence_bundle(
        creator_id="@alpha",
        profile_subject_id="platform_account:instagram:alpha",
        primary_raw_anchor="01INSTAGRAMAUDIENCE",
        comment_records=comments,
        transcript_records=transcripts,
        question="Who should hire Alpha?",
        evidence_cutoff="2026-07-16T00:00:00Z",
        method_deck_path=METHOD_DECK_RELATIVE_PATH,
        method_deck_sha256=method_hash,
    )

    assert bundle["platform_scope"] == "instagram"
    assert bundle["creator_id"] == "instagram:@alpha"
    assert bundle["method_deck_path"] == METHOD_DECK_RELATIVE_PATH
    assert bundle["method_deck_sha256"] == method_hash
    assert bundle["capture_scope"]["selected_source_item_ids"] == ["R1", "R2"]
    assert len(bundle["transcript_evidence"]) == 2
    assert len(bundle["comment_evidence"]) == 2
    assert all(row["temporal_alignment"] == "unproven" for row in bundle["comment_evidence"])
    assert len(bundle["source_refs"]["compatibility_residuals"]) == 4


def test_instagram_prepare_writes_prompt_bundle_and_assembly_receipt(tmp_path: Path) -> None:
    comments, transcripts = _instagram_records()
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    comment_paths = [
        data_root.append_record(
            subtree="derived",
            raw_anchor=str(record["reel_shortcode"]),
            lane=AUDIENCE_COMMENTS_LANE,
            record_id=str(record["record_id"]),
            data=json.dumps(record).encode("utf-8") + b"\n",
        )
        for record in comments
    ]
    transcript_paths = [
        data_root.append_record(
            subtree="derived",
            raw_anchor=str(record["reel_shortcode"]),
            lane=REEL_TRANSCRIPT_LANE,
            record_id=str(record["record_id"]),
            data=json.dumps(record).encode("utf-8") + b"\n",
        )
        for record in transcripts
    ]
    bundle_path = tmp_path / "bundle.json"
    prompt_path = tmp_path / "prompt.txt"
    result = prepare_instagram_subscription_judgment(
        data_root=data_root,
        creator_id="instagram:@alpha",
        profile_subject_id="platform_account:instagram:alpha",
        primary_raw_anchor="R1",
        comment_record_paths=comment_paths,
        transcript_record_paths=transcript_paths,
        question="Who should hire Alpha?",
        evidence_cutoff="2026-07-16T00:00:00Z",
        bundle_out=bundle_path,
        prompt_out=prompt_path,
    )

    assert result["status"] == "SUBSCRIPTION_JUDGMENT_REQUIRED"
    assert result["model_api_calls"] == 0
    assert bundle_path.is_file()
    assert "BEGIN_METHOD_DECK" in prompt_path.read_text(encoding="utf-8")
    receipt = data_root.record_path(
        subtree="derived",
        raw_anchor="R1",
        lane="creator_audience_evidence_assembly_receipt",
        record_id=result["assembly_receipt_record_id"],
    )
    assert receipt.is_file()

    with pytest.raises(ValueError, match="primary_raw_anchor must be the raw anchor"):
        prepare_instagram_subscription_judgment(
            data_root=data_root,
            creator_id="instagram:@alpha",
            profile_subject_id="platform_account:instagram:alpha",
            primary_raw_anchor="01INSTAGRAMAUDIENCE",
            comment_record_paths=comment_paths,
            transcript_record_paths=transcript_paths,
            question="Who should hire Alpha?",
            evidence_cutoff="2026-07-16T00:00:00Z",
            bundle_out=tmp_path / "foreign.bundle.json",
            prompt_out=tmp_path / "foreign.prompt.txt",
        )


def test_instagram_prepare_rejects_records_outside_silver_lanes(tmp_path: Path) -> None:
    comments, transcripts = _instagram_records()
    comment_path = tmp_path / "comments.json"
    transcript_path = tmp_path / "transcript.json"
    comment_path.write_text(json.dumps(comments[0]), encoding="utf-8")
    transcript_path.write_text(json.dumps(transcripts[0]), encoding="utf-8")

    with pytest.raises(ValueError, match="outside the admitted Silver lane"):
        prepare_instagram_subscription_judgment(
            data_root=DataLakeRoot.for_test(tmp_path / "lake"),
            creator_id="instagram:@alpha",
            profile_subject_id="platform_account:instagram:alpha",
            primary_raw_anchor="01INSTAGRAMAUDIENCE",
            comment_record_paths=[comment_path],
            transcript_record_paths=[transcript_path],
            question="Who should hire Alpha?",
            evidence_cutoff="2026-07-16T00:00:00Z",
            bundle_out=tmp_path / "bundle.json",
            prompt_out=tmp_path / "prompt.txt",
        )
