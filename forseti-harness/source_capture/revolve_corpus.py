"""Pure completeness verification for a REVOLVE brand-product corpus."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Literal, Sequence
from urllib.parse import urlsplit, urlunsplit

from pydantic import Field, model_validator

from schemas.case_models import StrictModel
from source_capture.retail_grid_projection import RetailGridProjectionPacket
from source_capture.revolve_pdp_content import (
    RevolvePdpAggregateContentRecord,
    extract_revolve_style_id_from_url,
)
from source_capture.revolve_yotpo_deep_capture import (
    RevolveYotpoDeepCaptureReceipt,
)


REVOLVE_CORPUS_RECEIPT_VERSION = "revolve_corpus_verification_v1"
_REVOLVE_HOSTS = frozenset({"revolve.com", "www.revolve.com"})


class RevolveCorpusUrlMismatch(StrictModel):
    style_id: str
    expected_url: str
    observed_urls: list[str] = Field(default_factory=list)


class RevolveCorpusVerificationReceipt(StrictModel):
    schema_version: Literal["revolve_corpus_verification_v1"] = (
        REVOLVE_CORPUS_RECEIPT_VERSION
    )
    status: Literal["complete", "partial"]
    grid_style_count: int = Field(ge=0)
    pdp_record_count: int = Field(ge=0)
    verified_style_ids: list[str] = Field(default_factory=list)
    missing_style_ids: list[str] = Field(default_factory=list)
    extra_style_ids: list[str] = Field(default_factory=list)
    duplicate_pdp_style_counts: dict[str, int] = Field(default_factory=dict)
    grid_identity_mismatches: list[str] = Field(default_factory=list)
    pdp_url_mismatches: list[RevolveCorpusUrlMismatch] = Field(default_factory=list)
    deep_candidate_style_id: str | None = None
    deep_candidate_source_url: str | None = None
    deep_binding_mismatches: list[str] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_status(self) -> "RevolveCorpusVerificationReceipt":
        defect_fields_present = any(
            (
                self.missing_style_ids,
                self.extra_style_ids,
                self.duplicate_pdp_style_counts,
                self.grid_identity_mismatches,
                self.pdp_url_mismatches,
                self.deep_binding_mismatches,
            )
        )
        if self.status == "complete":
            if self.residuals or defect_fields_present:
                raise ValueError(
                    "complete REVOLVE corpus receipt cannot carry residuals or mismatches"
                )
            if self.grid_style_count == 0:
                raise ValueError("complete REVOLVE corpus receipt requires grid styles")
            if len(self.verified_style_ids) != self.grid_style_count:
                raise ValueError(
                    "complete REVOLVE corpus receipt must verify every grid style"
                )
            if self.pdp_record_count != self.grid_style_count:
                raise ValueError(
                    "complete REVOLVE corpus receipt requires exactly one PDP per grid style"
                )
            if (
                self.deep_candidate_style_id is None
                or self.deep_candidate_source_url is None
            ):
                raise ValueError(
                    "complete REVOLVE corpus receipt requires a bound deep candidate"
                )
        elif not self.residuals:
            raise ValueError("partial REVOLVE corpus receipt requires residuals")
        return self


def verify_revolve_corpus(
    *,
    grid_projection: RetailGridProjectionPacket,
    pdp_records: Sequence[RevolvePdpAggregateContentRecord],
    deep_receipt: RevolveYotpoDeepCaptureReceipt,
) -> RevolveCorpusVerificationReceipt:
    """Reconcile a projected REVOLVE grid, its PDP records, and one deep receipt."""
    residuals: list[str] = []
    grid_identity_mismatches: list[str] = []
    deep_binding_mismatches: list[str] = []

    grid_retailer = grid_projection.source_visible_grid_facts.get("retailer")
    if grid_retailer != "revolve":
        residuals.append(
            f"revolve_corpus_projection_retailer_mismatch:observed={grid_retailer!r}"
        )
    if grid_projection.completeness.status != "complete":
        residuals.append(
            "revolve_corpus_grid_projection_incomplete:"
            f"status={grid_projection.completeness.status}"
        )

    grid_by_style: dict[str, tuple[str, int, int]] = {}
    for row in grid_projection.rows:
        fields = row.source_visible_fields
        source_product_id = fields.get("source_product_id")
        style_id = fields.get("style_id")
        product_url = fields.get("product_url")
        review_count = fields.get("review_count")
        grid_position = fields.get("grid_position")

        row_mismatches: list[str] = []
        if row.retailer != "revolve":
            row_mismatches.append(f"retailer={row.retailer!r}")
        if not isinstance(style_id, str) or not style_id:
            row_mismatches.append(f"style_id={style_id!r}")
        if source_product_id != style_id:
            row_mismatches.append(
                f"source_product_id={source_product_id!r}:style_id={style_id!r}"
            )
        url_style_id = (
            extract_revolve_style_id_from_url(product_url)
            if isinstance(product_url, str)
            else None
        )
        if url_style_id != style_id:
            row_mismatches.append(
                f"product_url_style_id={url_style_id!r}:style_id={style_id!r}"
            )
        canonical_url = (
            _canonical_revolve_url(product_url)
            if isinstance(product_url, str)
            else None
        )
        if canonical_url is None:
            row_mismatches.append(f"invalid_product_url={product_url!r}")
        if (
            not isinstance(review_count, int)
            or isinstance(review_count, bool)
            or review_count < 0
        ):
            row_mismatches.append(f"review_count={review_count!r}")
        if (
            not isinstance(grid_position, int)
            or isinstance(grid_position, bool)
            or grid_position < 1
        ):
            row_mismatches.append(f"grid_position={grid_position!r}")
        if isinstance(style_id, str) and style_id in grid_by_style:
            row_mismatches.append(f"duplicate_grid_style_id={style_id}")

        if row_mismatches:
            marker = f"{row.row_id}:" + "|".join(row_mismatches)
            grid_identity_mismatches.append(marker)
            residuals.append(f"revolve_corpus_grid_identity_mismatch:{marker}")
            continue
        assert isinstance(style_id, str)
        assert isinstance(canonical_url, str)
        assert isinstance(review_count, int)
        assert isinstance(grid_position, int)
        grid_by_style[style_id] = (canonical_url, review_count, grid_position)

    expected_styles = set(grid_by_style)
    if not expected_styles:
        residuals.append("revolve_corpus_grid_styles_absent")

    pdps_by_style: dict[str, list[RevolvePdpAggregateContentRecord]] = defaultdict(list)
    for record in pdp_records:
        pdps_by_style[record.style_id].append(record)
    observed_styles = set(pdps_by_style)
    missing_style_ids = sorted(expected_styles - observed_styles)
    extra_style_ids = sorted(observed_styles - expected_styles)
    duplicate_pdp_style_counts = {
        style_id: count
        for style_id, count in sorted(
            Counter(record.style_id for record in pdp_records).items()
        )
        if count > 1
    }
    residuals.extend(
        f"revolve_corpus_missing_pdp:{style_id}" for style_id in missing_style_ids
    )
    residuals.extend(
        f"revolve_corpus_extra_pdp:{style_id}" for style_id in extra_style_ids
    )
    residuals.extend(
        f"revolve_corpus_duplicate_pdp:{style_id}:count={count}"
        for style_id, count in duplicate_pdp_style_counts.items()
    )

    verified_style_ids: list[str] = []
    pdp_url_mismatches: list[RevolveCorpusUrlMismatch] = []
    for style_id in sorted(expected_styles):
        records = pdps_by_style.get(style_id, [])
        if len(records) != 1:
            continue
        expected_url = grid_by_style[style_id][0]
        record = records[0]
        observed_url = _canonical_revolve_url(record.source_url)
        if observed_url != expected_url:
            mismatch = RevolveCorpusUrlMismatch(
                style_id=style_id,
                expected_url=expected_url,
                observed_urls=[record.source_url],
            )
            pdp_url_mismatches.append(mismatch)
            residuals.append(
                "revolve_corpus_pdp_url_mismatch:"
                f"{style_id}:expected={expected_url}:observed={observed_url!r}"
            )
            continue
        verified_style_ids.append(style_id)

    candidate_style_id: str | None = None
    candidate_source_url: str | None = None
    if expected_styles:
        candidate_style_id = min(
            expected_styles,
            key=lambda style_id: (
                -grid_by_style[style_id][1],
                grid_by_style[style_id][2],
                style_id,
            ),
        )
        candidate_source_url = grid_by_style[candidate_style_id][0]
        candidate_records = pdps_by_style.get(candidate_style_id, [])
        candidate_pdp = candidate_records[0] if len(candidate_records) == 1 else None

        if deep_receipt.style_id != candidate_style_id:
            deep_binding_mismatches.append(
                "style_id:"
                f"expected={candidate_style_id}:observed={deep_receipt.style_id}"
            )
        deep_source_url = _canonical_revolve_url(deep_receipt.source_url)
        if deep_source_url != candidate_source_url:
            deep_binding_mismatches.append(
                "source_url:"
                f"expected={candidate_source_url}:observed={deep_source_url!r}"
            )
        if candidate_pdp is None:
            deep_binding_mismatches.append("candidate_pdp_not_unique")
        else:
            substrate = candidate_pdp.review_substrate
            expected_store_id = substrate.get("store_id")
            expected_review_count = substrate.get("review_count")
            if deep_receipt.store_id != expected_store_id:
                deep_binding_mismatches.append(
                    "store_id:"
                    f"expected={expected_store_id!r}:observed={deep_receipt.store_id!r}"
                )
            if deep_receipt.declared_review_count != expected_review_count:
                deep_binding_mismatches.append(
                    "declared_review_count:"
                    f"expected={expected_review_count!r}:"
                    f"observed={deep_receipt.declared_review_count}"
                )
        if deep_receipt.status != "complete":
            deep_binding_mismatches.append(
                f"status:expected=complete:observed={deep_receipt.status}"
            )
        if deep_receipt.qna_posture == "exposed_not_captured":
            deep_binding_mismatches.append("qna_exposed_not_captured")

    residuals.extend(
        f"revolve_corpus_deep_binding_mismatch:{mismatch}"
        for mismatch in deep_binding_mismatches
    )
    residuals = list(dict.fromkeys(residuals))
    return RevolveCorpusVerificationReceipt(
        status="partial" if residuals else "complete",
        grid_style_count=len(expected_styles),
        pdp_record_count=len(pdp_records),
        verified_style_ids=verified_style_ids,
        missing_style_ids=missing_style_ids,
        extra_style_ids=extra_style_ids,
        duplicate_pdp_style_counts=duplicate_pdp_style_counts,
        grid_identity_mismatches=grid_identity_mismatches,
        pdp_url_mismatches=pdp_url_mismatches,
        deep_candidate_style_id=candidate_style_id,
        deep_candidate_source_url=candidate_source_url,
        deep_binding_mismatches=deep_binding_mismatches,
        residuals=residuals,
    )


def _canonical_revolve_url(value: str) -> str | None:
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return None
    hostname = (parsed.hostname or "").lower()
    if parsed.scheme.lower() != "https" or hostname not in _REVOLVE_HOSTS:
        return None
    if port not in (None, 443):
        return None
    path = parsed.path.rstrip("/")
    if not path:
        path = "/"
    return urlunsplit(("https", "www.revolve.com", path, "", ""))


__all__ = [
    "REVOLVE_CORPUS_RECEIPT_VERSION",
    "RevolveCorpusUrlMismatch",
    "RevolveCorpusVerificationReceipt",
    "verify_revolve_corpus",
]
