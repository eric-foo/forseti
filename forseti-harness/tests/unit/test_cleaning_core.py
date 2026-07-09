from __future__ import annotations

import pytest
from pydantic import ValidationError

from cleaning import (
    REQUIRED_NON_CLAIMS,
    CleaningInputGrain,
    CleaningInputHandle,
    CleaningPacket,
    CleaningPreservationCheck,
    CleaningProjectionRef,
    CleaningRawAnchor,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
    derive_exact_identity_duplicate_groups,
)
from source_capture.reddit_projection import (
    REDDIT_PROJECTION_CERTIFICATION,
    REDDIT_PROJECTION_METHOD,
    REDDIT_PROJECTION_VERSION,
)
from source_capture.retail_pdp_projection import (
    RETAIL_PDP_PROJECTION_CERTIFICATION,
    RETAIL_PDP_PROJECTION_METHOD,
    RETAIL_PDP_PROJECTION_VERSION,
)


def _preservation() -> CleaningPreservationCheck:
    return CleaningPreservationCheck(
        originals_addressable=True,
        source_identity_preserved=True,
        timing_preserved=True,
        hierarchy_preserved=True,
        semantic_binding_preserved=True,
        counts_preserved=True,
    )


def _handle(
    handle_id: str,
    *,
    source_family: str = "reddit",
    source_surface: str = "reddit_api_comments",
    packet_id: str = "packet_01",
    slice_id: str = "slice_01",
    file_id: str = "file_01",
    relative_packet_path: str = "raw/body.json",
    sha256: str = "abc123",
    hash_basis: str = "raw_stored_bytes",
    anchor_kind: str = "json_pointer",
    anchor_value: str | None = None,
    json_pointer: str | None = "/data/children/0",
    projection_method: str = REDDIT_PROJECTION_METHOD,
    projection_version: str = REDDIT_PROJECTION_VERSION,
    projection_certification: str = REDDIT_PROJECTION_CERTIFICATION,
    row_id: str = "row_01",
    row_kind: str = "reddit_comment",
) -> CleaningInputHandle:
    return CleaningInputHandle(
        handle_id=handle_id,
        source_family=source_family,
        source_surface=source_surface,
        raw_anchor=CleaningRawAnchor(
            packet_id=packet_id,
            slice_id=slice_id,
            file_id=file_id,
            relative_packet_path=relative_packet_path,
            sha256=sha256,
            hash_basis=hash_basis,
            anchor_kind=anchor_kind,
            anchor_value=anchor_value,
            json_pointer=json_pointer,
        ),
        projection_ref=CleaningProjectionRef(
            projection_method=projection_method,
            projection_version=projection_version,
            certification=projection_certification,
            packet_id=packet_id,
            row_id=row_id,
            row_kind=row_kind,
        ),
    )


def test_handles_keep_reddit_and_retail_projection_refs_distinct_from_raw() -> None:
    reddit = _handle("h_reddit")
    retail = _handle(
        "h_retail",
        source_family="web_page",
        source_surface="cloakbrowser_snapshot",
        packet_id="retail_packet_01",
        slice_id="cloakbrowser_snapshot_01",
        file_id="html_01",
        relative_packet_path="raw/rendered_dom.html",
        sha256="htmlsha",
        anchor_kind="html_selector",
        anchor_value="#averageCustomerReviews",
        json_pointer=None,
        projection_method=RETAIL_PDP_PROJECTION_METHOD,
        projection_version=RETAIL_PDP_PROJECTION_VERSION,
        projection_certification=RETAIL_PDP_PROJECTION_CERTIFICATION,
        row_id="retail_review_01",
        row_kind="retail_review_substrate",
    )

    packet = CleaningPacket(handles=[reddit, retail])

    assert packet.handles[0].raw_anchor.packet_id == "packet_01"
    assert packet.handles[0].projection_ref is not None
    assert packet.handles[0].projection_ref.projection_method == REDDIT_PROJECTION_METHOD
    assert packet.handles[1].raw_anchor.anchor_kind == "html_selector"
    assert packet.handles[1].projection_ref is not None
    assert packet.handles[1].projection_ref.projection_method == RETAIL_PDP_PROJECTION_METHOD


def test_transform_ledger_requires_preservation_and_non_claims() -> None:
    entry = CleaningTransformLedgerEntry(
        input_handle_id="h1",
        transform=CleaningTransform(
            transform_class=CleaningTransformClass.NORMALIZATION,
            rule_scope=CleaningRuleScope.SOURCE_INVARIANT_CORE,
            method_or_rule="whitespace_trim",
            input_grain=CleaningInputGrain.ROW,
            original_value="  text  ",
            transformed_value="text",
        ),
        preservation=_preservation(),
    )

    assert set(REQUIRED_NON_CLAIMS) <= set(entry.non_claims)
    assert entry.raw_pull_triggers == []


def test_transform_rejects_judgment_vocabulary_in_method() -> None:
    with pytest.raises(ValidationError, match="Judgment vocabulary"):
        CleaningTransform(
            transform_class=CleaningTransformClass.NORMALIZATION,
            rule_scope=CleaningRuleScope.SOURCE_INVARIANT_CORE,
            method_or_rule="credibility_score_cleanup",
            input_grain=CleaningInputGrain.ROW,
            original_value="x",
            transformed_value="x",
        )


def test_core_v0_rejects_deferred_near_match_and_clustering_mechanics() -> None:
    with pytest.raises(ValidationError, match="exact_identity"):
        CleaningTransform(
            transform_class=CleaningTransformClass.DEDUPE_MECHANICS,
            rule_scope=CleaningRuleScope.SOURCE_INVARIANT_CORE,
            method_or_rule="near_match_similarity",
            input_grain=CleaningInputGrain.ROW,
        )

    # Use a valid transform class so the deferred-token guard fires, not the invalid-enum guard.
    with pytest.raises(ValidationError, match="deferred"):
        CleaningTransform(
            transform_class=CleaningTransformClass.PROPAGATION,
            rule_scope=CleaningRuleScope.UNRESOLVED_CANDIDATE,
            method_or_rule="cluster_by_topic",
            input_grain=CleaningInputGrain.GROUP,
        )


def test_preservation_check_rejects_hidden_loss() -> None:
    with pytest.raises(ValidationError, match="source_identity_preserved"):
        CleaningPreservationCheck(
            originals_addressable=True,
            source_identity_preserved=False,
            timing_preserved=True,
            hierarchy_preserved=True,
            semantic_binding_preserved=True,
            counts_preserved=True,
        )


def test_packet_rejects_unknown_transform_handle() -> None:
    handle = _handle("h1")
    entry = CleaningTransformLedgerEntry(
        input_handle_id="missing",
        transform=CleaningTransform(
            transform_class=CleaningTransformClass.PROPAGATION,
            rule_scope=CleaningRuleScope.SOURCE_INVARIANT_CORE,
            method_or_rule="warning_propagation",
            input_grain=CleaningInputGrain.ROW,
        ),
        preservation=_preservation(),
        warnings=["projection anchor missing"],
        raw_pull_triggers=["inspect raw row before Judgment"],
    )

    with pytest.raises(ValidationError, match="unknown input_handle_id"):
        CleaningPacket(handles=[handle], transform_ledger=[entry])


def test_exact_identity_dedupe_groups_only_full_raw_anchor_matches() -> None:
    first = _handle("h1", row_id="row_1")
    duplicate = _handle("h2", row_id="row_2")
    same_file_different_pointer = _handle("h3", row_id="row_3", json_pointer="/data/children/1")

    groups = derive_exact_identity_duplicate_groups([same_file_different_pointer, duplicate, first])

    assert len(groups) == 1
    assert groups[0].basis.value == "raw_anchor_identity"
    assert groups[0].member_handle_ids == ["h1", "h2"]
    assert groups[0].instance_count == 2


def test_transform_ledger_rejects_judgment_vocabulary_in_warnings() -> None:
    with pytest.raises(ValidationError, match="Judgment vocabulary"):
        CleaningTransformLedgerEntry(
            input_handle_id="h1",
            transform=CleaningTransform(
                transform_class=CleaningTransformClass.PROPAGATION,
                rule_scope=CleaningRuleScope.SOURCE_INVARIANT_CORE,
                method_or_rule="warning_propagation",
                input_grain=CleaningInputGrain.ROW,
            ),
            preservation=_preservation(),
            warnings=["signal_integrity_violated"],
        )


def test_projection_ref_must_not_claim_cleaned_or_judgment_ready() -> None:
    with pytest.raises(ValidationError, match="not cleaned"):
        CleaningProjectionRef(
            projection_method="bad_projection",
            projection_version="v0",
            certification="cleaned; judgment_ready",
            packet_id="p1",
            row_id="r1",
        )
