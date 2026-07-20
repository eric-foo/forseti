"""The non-silver record role validator enforces the no-blur NEGATIVE mirror.

Runs the REAL Fragrantica cleaning-audit and projection producer output through
``validate_non_silver_record`` (so a producer that starts blurring is caught), and
proves the validator actually bites: each crafted blur -- a Silver marker on a
non-silver record, a dropped role posture, a smuggled Judgment -- must raise. Also
pins the list-record path (ECR / signal-content write a JSON list) and the
silver-role misuse guard.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from cleaning.fragrantica_lake import derive_fragrantica_cleaning_into_lake
from data_lake.lane_registry import LaneRole, role_of
from data_lake.non_silver_record import (
    NonSilverRecordError,
    validate_non_silver_record,
)
from data_lake.root import DataLakeRoot
from source_capture.fragrantica_projection import (
    PROJECTION_FRAGRANTICA_LANE,
    build_fragrantica_projection,
)
from source_capture.models import (
    PacketTiming,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet

_LOCATOR = "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
_CAPTURE_TIME = "2026-06-28T18:57:58Z"


@pytest.fixture
def real_records(tmp_path: Path) -> dict[str, object]:
    """The REAL current Fragrantica non-silver records: the cleaning-audit pack and
    the mechanical projection, both built by the live producers from a committed
    fixture packet."""
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    result = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)
    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))

    loaded = root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    ).model_dump(mode="json")

    return {"audit": audit, "projection": projection}


# --- The live producers pass the validator (regression guard) -------------------


def test_registry_roles_match_the_validator_expectations() -> None:
    assert role_of("cleaning_fragrantica_audit") is LaneRole.CLEANING_AUDIT
    assert role_of(PROJECTION_FRAGRANTICA_LANE) is LaneRole.RETIRED_CAPTURE_PROJECTION


def test_real_cleaning_audit_pack_passes(real_records: dict[str, object]) -> None:
    validate_non_silver_record(LaneRole.CLEANING_AUDIT, real_records["audit"])


def test_real_projection_passes(real_records: dict[str, object]) -> None:
    validate_non_silver_record(LaneRole.PROJECTION, real_records["projection"])


# --- #3: a non-silver record must not masquerade as a Silver fact ---------------


def test_audit_pack_with_silver_schema_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["audit"])
    blurred["schema_version"] = "silver_vault_record_v0"
    with pytest.raises(NonSilverRecordError, match="masquerade as a Silver fact"):
        validate_non_silver_record(LaneRole.CLEANING_AUDIT, blurred)


def test_projection_with_closed_record_kind_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["projection"])
    blurred["record_kind"] = "observation"
    with pytest.raises(NonSilverRecordError, match="closed Silver record_kind"):
        validate_non_silver_record(LaneRole.PROJECTION, blurred)


# --- #4: positive role posture --------------------------------------------------


def test_audit_pack_missing_record_family_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["audit"])
    del blurred["record_family"]
    with pytest.raises(NonSilverRecordError, match="processing_audit"):
        validate_non_silver_record(LaneRole.CLEANING_AUDIT, blurred)


def test_audit_pack_missing_transform_ledger_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["audit"])
    blurred["payload"].pop("cleaning_packet", None)
    blurred["payload"].pop("transform_ledger", None)
    with pytest.raises(NonSilverRecordError, match="transform ledger"):
        validate_non_silver_record(LaneRole.CLEANING_AUDIT, blurred)


def test_projection_missing_certification_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["projection"])
    blurred.pop("certification", None)
    with pytest.raises(NonSilverRecordError, match="not_cleaned"):
        validate_non_silver_record(LaneRole.PROJECTION, blurred)


# --- #10: Cleaning must not smuggle Judgment ------------------------------------


def test_audit_pack_missing_not_judgment_boundary_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["audit"])
    blurred["non_claims"] = [c for c in blurred["non_claims"] if c != "not_judgment"]
    with pytest.raises(NonSilverRecordError, match="Judgment boundary"):
        validate_non_silver_record(LaneRole.CLEANING_AUDIT, blurred)


def test_audit_pack_with_smuggled_judgment_record_raises(real_records: dict[str, object]) -> None:
    blurred = copy.deepcopy(real_records["audit"])
    blurred["payload"]["judgment"] = {"decision": "buy", "resolved": True}
    with pytest.raises(NonSilverRecordError, match="resolved Judgment record"):
        validate_non_silver_record(LaneRole.CLEANING_AUDIT, blurred)


# --- list records (ECR / signal-content persist a JSON list of dicts) -----------


def test_posture_list_record_passes_and_blurred_member_raises() -> None:
    postures = [
        {"epistemic_kind": "timing", "status": "known"},
        {"epistemic_kind": "identity", "status": "unknown_with_reason"},
    ]
    validate_non_silver_record(LaneRole.ECR, postures)

    blurred = copy.deepcopy(postures)
    blurred[1]["schema_version"] = "silver_vault_record_v0"
    with pytest.raises(NonSilverRecordError, match="masquerade as a Silver fact"):
        validate_non_silver_record(LaneRole.ECR, blurred)


# --- hardening from the de-correlated review of #506 (adjudicated) --------------


def test_list_record_with_non_mapping_member_raises() -> None:
    # F1: a non-mapping member of a list record is invalid, not silently skipped --
    # skipping it would let a malformed member evade the #3 envelope check.
    postures = [{"epistemic_kind": "timing", "status": "known"}, ["nested", "list"]]
    with pytest.raises(NonSilverRecordError, match="only mappings"):
        validate_non_silver_record(LaneRole.ECR, postures)


def test_projection_certification_substring_lookalike_is_rejected(
    real_records: dict[str, object],
) -> None:
    # F2: exact-token match, not substring -- a lookalike cert that does not actually
    # assert the posture must not pass.
    blurred = copy.deepcopy(real_records["projection"])
    blurred["certification"] = "view_only; not_cleaned_up; not_judgment_readyish"
    with pytest.raises(NonSilverRecordError, match="not_cleaned"):
        validate_non_silver_record(LaneRole.PROJECTION, blurred)


def test_audit_pack_with_deeply_nested_judgment_raises(
    real_records: dict[str, object],
) -> None:
    # F4: a resolved Judgment nested below payload.* (here under cleaning_packet) must
    # not slip past a shallow top-level/payload-only boundary check.
    blurred = copy.deepcopy(real_records["audit"])
    blurred["payload"]["cleaning_packet"]["judgment"] = {"decision": "buy"}
    with pytest.raises(NonSilverRecordError, match="resolved Judgment record"):
        validate_non_silver_record(LaneRole.CLEANING_AUDIT, blurred)


def test_audit_pack_with_empty_transform_ledger_passes(
    real_records: dict[str, object],
) -> None:
    # F3 adjudication (rejected): a packet with nothing to clean (e.g. no reviews)
    # emits a legitimate audit whose transform_ledger is empty -- empty is not a blur,
    # so the validator must NOT reject it. This pins the decision against a re-add of
    # a non-empty requirement.
    audit = copy.deepcopy(real_records["audit"])
    audit["payload"]["cleaning_packet"]["transform_ledger"] = []
    validate_non_silver_record(LaneRole.CLEANING_AUDIT, audit)


# --- misuse + shape guards ------------------------------------------------------


def test_silver_role_is_rejected_as_misuse() -> None:
    with pytest.raises(NonSilverRecordError, match="non-silver roles only"):
        validate_non_silver_record(
            LaneRole.SILVER_ENVELOPE,
            {"schema_version": "silver_vault_record_v0", "record_kind": "observation"},
        )


def test_non_mapping_non_list_record_raises() -> None:
    with pytest.raises(NonSilverRecordError, match="mapping or a list of mappings"):
        validate_non_silver_record(LaneRole.SIGNAL_CONTENT, 42)


# --- known-good fixture (compact; mirrors the Fragrantica cleaning pilot) --------


def _commit_fragrantica_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML, encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")

    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact(_CAPTURE_TIME),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    source_slice = SourceCaptureSlice(
        slice_id="slice_01",
        locator=known_fact(_LOCATOR),
        timing=timing,
        access_posture=known_fact("direct HTTP fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("linked media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        limitations=[],
        warning_notes=[],
        preserved_file_ids=["file_01", "file_02"],
    )
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="fragrantica_product_page_direct_http",
        source_locator=known_fact(_LOCATOR),
        decision_question="batch2 non-silver record conformance",
        capture_context="non-silver record role conformance",
        source_slices=[source_slice],
    )
    return result.packet.packet_id


_HTML = """
<html><head>
  <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
  <title>Baccarat Rouge 540 Maison Francis Kurkdjian perfume</title>
</head><body>
  <div id="perfume-description-content" itemprop="description">
    <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance. Baccarat Rouge 540 was launched in 2015.</p>
  </div>
  <p itemprop="aggregateRating"><span itemprop="ratingValue">3.76</span><span itemprop="bestRating">5</span><span itemprop="ratingCount" content="28808">28,808</span></p>
  <span>Reviews (<span>3.9K</span>)</span>
  <button data-tab="all-reviews" data-active="true">All reviews by date</button>
  <div class="review-tab-panel" id="all-reviews">
    <div id="parent3090334" class="cell tw-review-card tw-gradient-rose" itemprop="review" itemscope>
      <user-perfume-votes-new :perfume-votes="{&quot;rating&quot;:5,&quot;winter&quot;:0,&quot;spring&quot;:0,&quot;summer&quot;:0,&quot;autumn&quot;:0,&quot;day&quot;:0,&quot;night&quot;:0,&quot;longevity&quot;:3,&quot;sillage&quot;:2,&quot;gender&quot;:&quot;female_unisex&quot;,&quot;relation&quot;:&quot;have&quot;}"></user-perfume-votes-new>
      <meta itemprop="name" content="Rimazy"/>
      <span itemprop="datePublished" content="2026-06-25">06/25/26 18:41</span>
      <div id="review_3090334"><p>This perfume died young.</p></div>
      <vote-buttons-new initial-status="neutral" item-id="33519" comment-id="3090334" vote-for="perfumeReview"></vote-buttons-new>
      <share-new path="/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html?ccid=3090334#focus-zone"></share-new>
    </div>
    <reviews-infinity-new :perfume-id="33519" sentiment="all" :is-logged="false" login-url="/board/login.php"
      :lang-strings="{&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;}">
    </reviews-infinity-new>
  </div>
</body></html>
"""
