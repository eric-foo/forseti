from __future__ import annotations

import json

import pytest

from cleaning.audience_extractor import RawApiProvider
from evidence_binding.tiktok_audience_triangulation import build_gold_ready_audience_evidence
from runners.run_tiktok_creator_audience_triangulation import run_triangulation
from judgment.tiktok_audience_triangulation import (
    triangulate_audience,
    validate_triangulation_profile,
)


def _video(video_id: str, comment_id: str, text: str, likes: int) -> dict:
    observed = "2026-07-12T00:00:00Z"
    return {
        "video_id": video_id,
        "stats_observed_utc": observed,
        "stats": {"diggCount": 1000, "commentCount": 100},
        "comments": {
            "observed_utc": observed,
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


def _assembly(*, creator: str = "tiktok:@alpha", duplicate_text: bool = False) -> dict:
    text1 = "This comparison is unforgettable"
    text2 = text1 if duplicate_text else "Do this comparison again"
    payload = {
        "creator_handle": "alpha",
        "capture_timestamp": "2026-07-12T00:05:00Z",
        "videos": [_video("v1", "c1", text1, 100), _video("v2", "c2", text2, 80)],
    }
    evidence = [
        {
            "evidence_id": "ttae_1",
            "creator_id": creator,
            "video_id": "v1",
            "audience_layer": "addressed_audience",
            "dimension": "preferred_content_mechanism",
            "label": "comparison-led entertainment",
            "content_pillar": "comparisons",
            "vote": 1.0,
            "source_pointer": "compare these two",
            "possible_negation_or_irony": False,
        }
    ]
    return build_gold_ready_audience_evidence(
        creator_id=creator,
        batch_payloads=[payload],
        transcript_evidence=evidence,
        question="Who is this creator commercially useful for?",
        evidence_cutoff="2026-07-12T00:05:00Z",
        semantic_labels={"v1:c1": ["product_relevant"], "v2:c2": ["format_request"]},
    )


def _profile(assembly: dict) -> dict:
    comment_ids = [row["evidence_id"] for row in assembly["comment_evidence"]]
    claim = {
        "claim_id": "claim-1",
        "axis": "engagement_memorability_effect",
        "statement": "The recurring comparison format generates engagement.",
        "commercial_implication": "Use it to make compared products memorable.",
        "modality": "engagement_elevated",
        "relation": "agreement",
        "support_scope": "multi_video",
        "representative_evidence_ids": comment_ids,
        "all_support_evidence_ids": comment_ids,
        "counterevidence_ids": [],
        "source_video_ids": ["v1", "v2"],
        "limitation": "Captured top-level comments from selected videos, not a census.",
    }
    point = {"statement": "Comparison-led entertainment with product recall.", "claim_ids": ["claim-1"]}
    return {
        "schema_version": "creator_audience_triangulation_v0",
        "creator_id": assembly["creator_id"],
        "generated_at": "2026-07-14T00:00:00Z",
        "evidence_cutoff": assembly["evidence_cutoff"],
        "headline_points": [point],
        "commercial_points": [point],
        "strongest_campaign_jobs": [point],
        "fit_conditions": [point],
        "material_unknowns": ["Audience-wide prevalence is not estimated."],
        "claims": [claim],
        "actual_audience_demographics": "not_estimated",
    }


def test_assembly_is_creator_isolated_and_preserves_all_exact_duplicates() -> None:
    assembly = _assembly(duplicate_text=True)
    assert assembly["assembly_receipt"]["comment_evidence_count"] == 2
    assert len(assembly["exact_duplicate_clusters"]) == 1
    assert assembly["exact_duplicate_clusters"][0]["multiplicity"] == 2
    assert all(row["temporal_alignment"] == "same_capture_observation" for row in assembly["comment_evidence"])
    with pytest.raises(ValueError, match="mixes creators"):
        build_gold_ready_audience_evidence(
            creator_id="tiktok:@alpha",
            batch_payloads=[{"creator_handle": "alpha", "videos": [_video("v1", "c1", "x", 1)]}],
            transcript_evidence=[{**_assembly()["transcript_evidence"][0], "creator_id": "tiktok:@beta"}],
            question="q",
            evidence_cutoff="2026-07-12T00:00:00Z",
        )


def test_one_call_profile_closes_every_claim_over_allowed_evidence() -> None:
    assembly = _assembly()
    profile = _profile(assembly)

    class Transport:
        calls = 0

        def post_json(self, url, headers, body, timeout_seconds):
            self.calls += 1
            return json.dumps({"output_text": json.dumps(profile)})

    transport = Transport()
    result = triangulate_audience(
        assembly=assembly,
        transport=transport,
        provider=RawApiProvider.OPENAI_RESPONSES,
        model="model",
        api_key="secret",
    )
    assert result.creator_id == "tiktok:@alpha"
    assert transport.calls == 1


def test_validator_rejects_single_video_effect_and_majority_language() -> None:
    assembly = _assembly()
    profile = _profile(assembly)
    first_row = assembly["comment_evidence"][0]
    first_id = first_row["evidence_id"]
    claim = profile["claims"][0]
    claim["all_support_evidence_ids"] = [first_id]
    claim["representative_evidence_ids"] = [first_id]
    claim["source_video_ids"] = [first_row["video_id"]]
    claim["support_scope"] = "single_video"
    with pytest.raises(ValueError, match="needs two videos"):
        validate_triangulation_profile(profile, assembly)
    profile = _profile(assembly)
    profile["headline_points"][0]["statement"] = "Most of the audience wants this."
    with pytest.raises(ValueError, match="majority language"):
        validate_triangulation_profile(profile, assembly)


def test_validator_rejects_unclassified_comment_only_shopping_claim() -> None:
    assembly = _assembly()
    for row in assembly["comment_evidence"]:
        row["semantic_labels"] = []
        row["semantic_posture"] = "not_attempted"
    profile = _profile(assembly)
    first_row = assembly["comment_evidence"][0]
    claim = profile["claims"][0]
    claim.update(
        {
            "axis": "purchase_decision_stage",
            "statement": "The comment asks where to buy the product.",
            "commercial_implication": "Use an availability-led call to action.",
            "modality": "observed_comments",
            "relation": "audience_emergent",
            "support_scope": "single_comment",
            "representative_evidence_ids": [first_row["evidence_id"]],
            "all_support_evidence_ids": [first_row["evidence_id"]],
            "source_video_ids": [first_row["video_id"]],
        }
    )
    with pytest.raises(ValueError, match="unclassified comments"):
        validate_triangulation_profile(profile, assembly)

    first_row["semantic_labels"] = ["availability_or_ownership"]
    first_row["semantic_posture"] = "classified"
    validate_triangulation_profile(profile, assembly)


def test_runner_writes_two_new_scratch_files_and_counts_one_call(tmp_path) -> None:
    assembly = _assembly()
    profile = _profile(assembly)

    class Transport:
        calls = 0

        def post_json(self, url, headers, body, timeout_seconds):
            self.calls += 1
            return json.dumps({"output_text": json.dumps(profile)})

    transport = Transport()
    assembly_out = tmp_path / "assembly.json"
    profile_out = tmp_path / "profile.json"
    payload = {
        "creator_handle": "alpha",
        "capture_timestamp": "2026-07-12T00:05:00Z",
        "videos": [_video("v1", "c1", "This comparison is unforgettable", 100), _video("v2", "c2", "Do this comparison again", 80)],
    }
    result = run_triangulation(
        creator_id="tiktok:@alpha",
        batch_payloads=[payload],
        transcript_evidence=assembly["transcript_evidence"],
        question=assembly["question"],
        evidence_cutoff=assembly["evidence_cutoff"],
        semantic_labels={"v1:c1": ["product_relevant"], "v2:c2": ["format_request"]},
        assembly_out=assembly_out,
        profile_out=profile_out,
        transport=transport,
        provider=RawApiProvider.OPENAI_RESPONSES,
        model="model",
        api_key="secret",
    )
    assert transport.calls == 1
    assert result["run_receipt"]["gold_model_call_count"] == 1
    assert assembly_out.exists() and profile_out.exists()
    with pytest.raises(FileExistsError):
        run_triangulation(
            creator_id="tiktok:@alpha",
            batch_payloads=[payload],
            transcript_evidence=assembly["transcript_evidence"],
            question=assembly["question"],
            evidence_cutoff=assembly["evidence_cutoff"],
            semantic_labels=None,
            assembly_out=assembly_out,
            profile_out=profile_out,
            transport=transport,
            provider=RawApiProvider.OPENAI_RESPONSES,
            model="model",
            api_key="secret",
        )
