"""Unit tests for the generic Silver lineage grammar/validator (data_lake.silver_lineage).

Covers the adjudicated review findings that are load-bearing here: AR-01 (refs live in
top-level header-shaped fields, never a nested silver_lineage block), AR-02 (derived refs
can carry a projection row_locator), AR-04 (source_object uses `kind`). Plus the write-boundary
mechanical rules: exact derived lane+record_id, raw-ref hash-checkability, ref-or-limitation,
controlled limitation tokens, and the source-backed-completeness gate.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from data_lake.silver_lineage import (
    SILVER_LINEAGE_SCHEMA_VERSION,
    SOURCE_BACKED_COMPLETE_STATUS,
    SOURCE_LINEAGE_INCOMPLETE_STATUS,
    SOURCE_LINEAGE_INVALID_STATUS,
    SOURCE_LINEAGE_MISSING_STATUS,
    SilverDerivedRef,
    SilverLineage,
    SilverLineageLimitation,
    SilverLineageLimitationReason,
    SilverRawRef,
    SilverRowLocator,
    SilverSourceObject,
    is_silver_record_source_backed_complete,
    silver_record_source_backed_status,
    validate_silver_lineage,
)


def _derived_lineage(**over) -> SilverLineage:
    base = dict(
        producer_id="p",
        producer_schema_version="0.4",
        source_surface="youtube_audio",
        source_object=SilverSourceObject(namespace="youtube", kind="transcript", native_id="vid12345678"),
        derived_refs=[
            SilverDerivedRef(
                raw_anchor="ANCHOR123", lane="transcript_asr", record_id="asr_x__abc",
                sha256="a" * 64, hash_basis="derived_record_bytes",
            )
        ],
    )
    base.update(over)
    return SilverLineage(**base)


# --- AR-01: one home -- top-level header fields, never a nested wrapper -------


def test_to_record_fields_emits_top_level_refs_not_nested_block() -> None:
    fields = _derived_lineage().to_record_fields()
    assert "silver_lineage" not in fields            # never a nested second home
    assert isinstance(fields["derived_refs"], list)  # the single, top-level home
    assert fields["derived_refs"][0]["lane"] == "transcript_asr"
    assert fields["derived_refs"][0]["record_id"] == "asr_x__abc"
    # the block version is exposed as lineage_schema_version, never a record schema_version
    assert fields["lineage_schema_version"] == SILVER_LINEAGE_SCHEMA_VERSION
    assert "schema_version" not in fields


def test_source_object_uses_kind_not_object_type() -> None:  # AR-04
    fields = _derived_lineage().to_record_fields()
    assert fields["source_object"]["kind"] == "transcript"
    assert "object_type" not in fields["source_object"]


# --- exactness of derived refs (the same-shortcode crux) ---------------------


@pytest.mark.parametrize("field", ["raw_anchor", "lane", "record_id"])
def test_derived_ref_requires_exact_identity(field: str) -> None:
    kwargs = dict(raw_anchor="A", lane="transcript_asr", record_id="r")
    kwargs[field] = "   "
    with pytest.raises(ValidationError):
        SilverDerivedRef(**kwargs)


# --- raw ref resolvability / hash-checkability -------------------------------


def test_raw_ref_with_file_id_requires_sha256() -> None:
    with pytest.raises(ValidationError):
        SilverRawRef(packet_id="P", file_id="f1")  # a named file is hash-checkable


def test_raw_ref_sha_without_basis_rejected() -> None:
    with pytest.raises(ValidationError):
        SilverRawRef(packet_id="P", sha256="a" * 64)  # hash with no stated basis


def test_raw_ref_packet_level_without_hash_ok() -> None:
    ref = SilverRawRef(packet_id="P")  # packet-level ref, no specific file -> hash optional
    assert ref.packet_id == "P"


# --- ref-or-limitation + completeness gate -----------------------------------


def test_empty_lineage_rejected() -> None:
    with pytest.raises(ValidationError):
        SilverLineage(producer_id="p", producer_schema_version="v", source_surface="s")


def test_limitations_only_is_valid_but_not_complete() -> None:
    lin = SilverLineage(
        producer_id="p", producer_schema_version="v", source_surface="s",
        lineage_limitations=[
            SilverLineageLimitation(reason=SilverLineageLimitationReason.TRANSIENT_SOURCE_NOT_PERSISTED)
        ],
    )
    assert lin.is_source_backed_complete() is False


def test_ref_backed_lineage_is_complete() -> None:
    assert _derived_lineage().is_source_backed_complete() is True


def test_silver_record_source_backed_status_reads_persisted_fields() -> None:
    fields = _derived_lineage().to_record_fields()

    assert silver_record_source_backed_status(fields) == SOURCE_BACKED_COMPLETE_STATUS
    assert is_silver_record_source_backed_complete(fields) is True


def test_silver_record_source_backed_status_flags_missing_lineage() -> None:
    assert (
        silver_record_source_backed_status({"mention_count": 0}) == SOURCE_LINEAGE_MISSING_STATUS
    )
    assert is_silver_record_source_backed_complete({"mention_count": 0}) is False


def test_silver_record_source_backed_status_flags_invalid_lineage() -> None:
    fields = _derived_lineage().to_record_fields()
    fields["producer_id"] = "  "

    assert silver_record_source_backed_status(fields) == SOURCE_LINEAGE_INVALID_STATUS


def test_silver_record_source_backed_status_flags_limitations_only() -> None:
    fields = SilverLineage(
        producer_id="p",
        producer_schema_version="v",
        source_surface="s",
        lineage_limitations=[
            SilverLineageLimitation(reason=SilverLineageLimitationReason.TRANSIENT_SOURCE_NOT_PERSISTED)
        ],
    ).to_record_fields()

    assert silver_record_source_backed_status(fields) == SOURCE_LINEAGE_INCOMPLETE_STATUS


# --- row locator (AR-02) -----------------------------------------------------


def test_row_locator_requires_both_fields() -> None:
    with pytest.raises(ValidationError):
        SilverRowLocator(row_id="r1", row_kind="  ")


def test_derived_ref_carries_row_locator() -> None:
    ref = SilverDerivedRef(
        raw_anchor="A", lane="projection_retail_pdp", record_id="rec1",
        row_locator=SilverRowLocator(row_id="row7", row_kind="retail_variant_offer"),
    )
    assert ref.model_dump(mode="json")["row_locator"] == {
        "row_id": "row7", "row_kind": "retail_variant_offer"
    }


# --- controlled limitation tokens (AR-06) ------------------------------------


def test_limitation_other_requires_detail() -> None:
    with pytest.raises(ValidationError):
        SilverLineageLimitation(reason=SilverLineageLimitationReason.OTHER)


def test_limitation_other_with_detail_ok() -> None:
    lim = SilverLineageLimitation(reason=SilverLineageLimitationReason.OTHER, detail="novel limit")
    assert lim.detail == "novel limit"


def test_limitation_rejects_unknown_reason() -> None:
    with pytest.raises(ValidationError):
        SilverLineageLimitation(reason="totally_made_up")  # not in the controlled set


# --- StrictModel forbids extra fields + validator hook -----------------------


def test_strict_model_forbids_extra_fields() -> None:
    with pytest.raises(ValidationError):
        SilverDerivedRef(raw_anchor="A", lane="l", record_id="r", bogus="x")


def test_validate_silver_lineage_roundtrips() -> None:
    lin = _derived_lineage()
    assert validate_silver_lineage(lin).to_record_fields() == lin.to_record_fields()
