"""Evidence-selected retail depth and deterministic cross-retailer review linkage.

Capture remains raw-canonical. This Cleaning-owned seam consumes a verified
portfolio onboarding result plus source-backed candidate review rows, preserves
every native occurrence, and emits replayable planning/linkage records. It does
not assign portfolio roles, estimate sales, or mutate Capture packets.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Literal
import unicodedata

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel
from source_capture.retail_grid_projection import (
    load_verified_source_capture_packet_directory,
)

DEPTH_SELECTION_SCHEMA_VERSION = "retail_review_depth_selection_v0"
REVIEW_LINKAGE_SCHEMA_VERSION = "retail_review_overlap_linkage_v1"
LINKAGE_ALGORITHM_VERSION = "retail_review_overlap_exact_v1"
PORTFOLIO_SCHEMA_VERSIONS = frozenset(
    {
        "retail_portfolio_onboarding_v0",
        "retail_portfolio_onboarding_v1",
        "retail_portfolio_onboarding_v2",
    }
)

DepthTrigger = Literal[
    "ESTABLISHED_PROMINENCE",
    "AGE_ADJUSTED_VELOCITY",
    "FOUNDING_OR_STRATEGIC_CENTRALITY",
    "RECENT_INVESTMENT_OR_ADJACENCY",
    "COMPLAINT_CONCENTRATION",
    "PLAUSIBLE_WEAK_LINK",
    "CONTRADICTION",
    "INCIDENT",
]
DepthSurface = Literal["REVIEWS", "QA"]
ProminenceStatus = Literal["PROMINENT", "NOT_PROMINENT", "UNKNOWN"]
Retailer = str
ReviewSelectionPolicy = Literal[
    "SEPHORA_EXISTING_POLICY", "NON_SEPHORA_MOST_RECENT"
]
_RETAILER_SLUG = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")


class RetailReviewOverlapError(ValueError):
    """Inputs cannot produce a truthful deterministic Step-4 record."""


class DepthSelectionJob(StrictModel):
    job_id: str
    trigger: DepthTrigger
    information_job: str
    decision_use: str
    evidence_refs: list[str] = Field(min_length=1)
    depth_surfaces: list[DepthSurface] = Field(min_length=1)

    @field_validator("job_id", "information_job", "decision_use")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("depth-selection job text fields must be non-empty")
        return value

    @model_validator(mode="after")
    def unique_surfaces(self) -> "DepthSelectionJob":
        if len(set(self.depth_surfaces)) != len(self.depth_surfaces):
            raise ValueError("depth_surfaces must be unique within a job")
        return self


class DepthCandidate(StrictModel):
    owned_parent_id: str
    prominence_status: ProminenceStatus
    jobs: list[DepthSelectionJob] = Field(default_factory=list)

    @field_validator("owned_parent_id")
    @classmethod
    def reject_blank_parent(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("owned_parent_id must be non-empty")
        return value


class DepthSelectionCommission(StrictModel):
    company_id: str
    portfolio_onboarding_path: str
    candidates: list[DepthCandidate] = Field(min_length=1)

    @field_validator("company_id", "portfolio_onboarding_path")
    @classmethod
    def reject_blank_binding(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("selection commission bindings must be non-empty")
        return value

    @model_validator(mode="after")
    def unique_candidates_and_jobs(self) -> "DepthSelectionCommission":
        parents = [item.owned_parent_id for item in self.candidates]
        if len(set(parents)) != len(parents):
            raise ValueError("selection candidates must name each owned parent once")
        job_ids = [job.job_id for item in self.candidates for job in item.jobs]
        if len(set(job_ids)) != len(job_ids):
            raise ValueError("depth-selection job_id values must be globally unique")
        return self


class ReviewRawRef(StrictModel):
    packet_directory: str
    packet_id: str
    slice_id: str
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    raw_row_anchor: str

    @field_validator(
        "packet_directory",
        "packet_id",
        "slice_id",
        "file_id",
        "relative_packet_path",
        "hash_basis",
        "raw_row_anchor",
    )
    @classmethod
    def reject_blank_ref_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("review raw-ref fields must be non-empty")
        return value

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        digest = value.removeprefix("sha256:")
        if re.fullmatch(r"[0-9a-fA-F]{64}", digest) is None:
            raise ValueError("review raw-ref sha256 must be a 64-character digest")
        return value


class ReviewOccurrence(StrictModel):
    occurrence_id: str
    owned_parent_id: str
    retailer: Retailer
    capture_job_id: str
    source_product_id: str
    provider: str
    provider_tenant_store: str
    collection_context: str
    provider_evidence_refs: list[str] = Field(min_length=1)
    selection_policy: ReviewSelectionPolicy
    actual_ordering: str
    ordering_fallback: str | None = None
    source_native_review_id: str | None = None
    origin_review_id: str | None = None
    explicit_syndication_key: str | None = None
    syndication_source_text: str | None = None
    rating_value: str | int | float | None = None
    review_date_source_text: str | None = None
    reviewer_display_label: str | None = None
    review_title_verbatim: str | None = None
    review_body_verbatim: str
    raw_refs: list[ReviewRawRef] = Field(min_length=1)
    per_field_residuals: list[str] = Field(default_factory=list)
    row_scope_residuals: list[str] = Field(default_factory=list)

    @field_validator("retailer")
    @classmethod
    def validate_retailer_slug(cls, value: str) -> str:
        return _retailer_slug(value)

    @field_validator(
        "occurrence_id",
        "owned_parent_id",
        "capture_job_id",
        "source_product_id",
        "provider",
        "provider_tenant_store",
        "collection_context",
        "actual_ordering",
        "review_body_verbatim",
    )
    @classmethod
    def reject_blank_occurrence_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("review occurrence identity/provider/body must be non-empty")
        return value

    @field_validator(
        "source_native_review_id",
        "origin_review_id",
        "explicit_syndication_key",
        "syndication_source_text",
        "review_date_source_text",
        "reviewer_display_label",
        "review_title_verbatim",
        "ordering_fallback",
    )
    @classmethod
    def reject_blank_optional_text(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("optional review text must be absent rather than blank")
        return value

    @field_validator("provider_evidence_refs")
    @classmethod
    def reject_blank_provider_evidence_refs(cls, value: list[str]) -> list[str]:
        if any(not item.strip() for item in value):
            raise ValueError("provider evidence refs must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_selection_policy(self) -> "ReviewOccurrence":
        expected = (
            "SEPHORA_EXISTING_POLICY"
            if self.retailer == "sephora"
            else "NON_SEPHORA_MOST_RECENT"
        )
        if self.selection_policy != expected:
            raise ValueError("review selection policy contradicts retailer")
        if (
            self.retailer != "sephora"
            and not _is_most_recent_ordering(self.actual_ordering)
            and self.ordering_fallback is None
        ):
            raise ValueError(
                "non-Sephora ordering fallback is required when Most Recent is unavailable"
            )
        return self

    @field_validator("rating_value")
    @classmethod
    def reject_non_finite_rating(
        cls, value: str | int | float | None
    ) -> str | int | float | None:
        if value is None:
            return value
        try:
            numeric = Decimal(str(value))
        except InvalidOperation:
            return value
        if not numeric.is_finite():
            raise ValueError("rating_value must be finite")
        return value


class NativeReviewTotal(StrictModel):
    owned_parent_id: str
    retailer: Retailer
    capture_job_id: str
    source_product_id: str
    native_total: int = Field(ge=0)
    corpus_window: str
    observed_at: str
    raw_refs: list[ReviewRawRef] = Field(min_length=1)

    @field_validator("retailer")
    @classmethod
    def validate_retailer_slug(cls, value: str) -> str:
        return _retailer_slug(value)

    @field_validator(
        "owned_parent_id",
        "capture_job_id",
        "source_product_id",
        "corpus_window",
        "observed_at",
    )
    @classmethod
    def reject_blank_total_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("native-total bindings must be non-empty")
        return value


class ReviewLinkageCommission(StrictModel):
    company_id: str
    selection_output_path: str
    corpus_label: str
    occurrences: list[ReviewOccurrence] = Field(min_length=1)
    native_review_totals: list[NativeReviewTotal] = Field(default_factory=list)

    @field_validator("company_id", "selection_output_path", "corpus_label")
    @classmethod
    def reject_blank_linkage_bindings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("review-linkage bindings must be non-empty")
        return value

    @model_validator(mode="after")
    def unique_occurrences_and_totals(self) -> "ReviewLinkageCommission":
        occurrences = [item.occurrence_id for item in self.occurrences]
        if len(set(occurrences)) != len(occurrences):
            raise ValueError("occurrence_id values must be unique")
        totals = [
            (item.owned_parent_id, item.retailer, item.corpus_window)
            for item in self.native_review_totals
        ]
        if len(set(totals)) != len(totals):
            raise ValueError("native review totals must be unique by product/retailer/window")
        return self


def load_depth_selection_commission(path: Path) -> DepthSelectionCommission:
    return DepthSelectionCommission.model_validate(
        _load_json_object(path, "selection commission")
    )


def load_review_linkage_commission(path: Path) -> ReviewLinkageCommission:
    return ReviewLinkageCommission.model_validate(
        _load_json_object(path, "linkage commission")
    )


def build_depth_selection(
    *, commission: DepthSelectionCommission, base_directory: Path
) -> dict[str, Any]:
    portfolio_path = _resolve(base_directory, commission.portfolio_onboarding_path)
    portfolio_bytes = portfolio_path.read_bytes()
    portfolio = _decode_json_object(portfolio_bytes, "portfolio onboarding")
    if portfolio.get("schema_version") not in PORTFOLIO_SCHEMA_VERSIONS:
        raise RetailReviewOverlapError(
            "selection requires a supported retail_portfolio_onboarding schema"
        )
    if portfolio.get("company_id") != commission.company_id:
        raise RetailReviewOverlapError("selection and portfolio company_id values differ")

    parent_ids = {
        str(item.get("owned_parent_id"))
        for item in _object_list(portfolio, "owned_parents")
    }
    unknown = sorted(
        item.owned_parent_id
        for item in commission.candidates
        if item.owned_parent_id not in parent_ids
    )
    if unknown:
        raise RetailReviewOverlapError(
            f"selection names unknown owned parents: {unknown}"
        )

    baselines: dict[tuple[str, str], dict[str, Any]] = {}
    for item in _object_list(portfolio, "pdp_baselines"):
        key = (str(item.get("retailer")), str(item.get("source_product_id")))
        if key in baselines:
            raise RetailReviewOverlapError(
                f"portfolio has duplicate PDP baseline: {key}"
            )
        if not _non_blank_text(item.get("packet_id")) or not _non_blank_text(
            item.get("source_locator")
        ):
            raise RetailReviewOverlapError(
                f"portfolio PDP baseline lacks a verified packet binding: {key}"
            )
        baselines[key] = item

    listings_by_parent: dict[str, list[dict[str, Any]]] = {
        key: [] for key in parent_ids
    }
    seen_listings: set[tuple[str, str]] = set()
    for item in _object_list(portfolio, "listing_identities"):
        retailer = str(item.get("retailer"))
        source_product_id = str(item.get("source_product_id"))
        if (retailer, source_product_id) in seen_listings:
            raise RetailReviewOverlapError(
                "portfolio has duplicate listing identity: "
                f"{(retailer, source_product_id)}"
            )
        seen_listings.add((retailer, source_product_id))
        baseline = baselines.get((retailer, source_product_id))
        for parent_id in item.get("exact_owned_parent_ids", []):
            if parent_id not in listings_by_parent:
                raise RetailReviewOverlapError(
                    f"portfolio listing identity names unknown owned parent: {parent_id}"
                )
            if baseline is None:
                raise RetailReviewOverlapError(
                    "exact listing has no verified PDP baseline: "
                    f"{(retailer, source_product_id)}"
                )
            listings_by_parent[parent_id].append(
                {
                    "retailer": retailer,
                    "source_product_id": source_product_id,
                    "baseline_packet_id": baseline.get("packet_id"),
                    "source_locator": baseline.get("source_locator"),
                }
            )

    selected_products: list[dict[str, Any]] = []
    not_selected_products: list[dict[str, Any]] = []
    capture_jobs: list[dict[str, Any]] = []
    residuals: list[str] = []
    for candidate in sorted(
        commission.candidates, key=lambda item: item.owned_parent_id
    ):
        if not candidate.jobs:
            not_selected_products.append(
                {
                    "owned_parent_id": candidate.owned_parent_id,
                    "prominence_status": candidate.prominence_status,
                    "reason": "NO_NAMED_NON_DUPLICATIVE_JOB",
                }
            )
            continue
        selected_products.append(
            {
                "owned_parent_id": candidate.owned_parent_id,
                "prominence_status": candidate.prominence_status,
                "selection_jobs": [
                    job.model_dump(mode="json")
                    for job in sorted(candidate.jobs, key=lambda item: item.job_id)
                ],
            }
        )
        listings = sorted(
            listings_by_parent[candidate.owned_parent_id],
            key=lambda item: (item["retailer"], item["source_product_id"]),
        )
        if not listings:
            residuals.append(
                "SELECTED_PRODUCT_HAS_NO_EXACT_RETAIL_LISTING:"
                + candidate.owned_parent_id
            )
        for job in sorted(candidate.jobs, key=lambda item: item.job_id):
            for listing in listings:
                for surface in sorted(job.depth_surfaces):
                    basis = "|".join(
                        (
                            commission.company_id,
                            candidate.owned_parent_id,
                            job.job_id,
                            listing["retailer"],
                            listing["source_product_id"],
                            surface,
                        )
                    )
                    capture_jobs.append(
                        {
                            "capture_job_id": "depth_"
                            + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24],
                            "owned_parent_id": candidate.owned_parent_id,
                            "retailer": listing["retailer"],
                            "source_product_id": listing["source_product_id"],
                            "source_locator": listing["source_locator"],
                            "baseline_packet_id": listing["baseline_packet_id"],
                            "surface": surface,
                            "selection_job_id": job.job_id,
                            "trigger": job.trigger,
                            "information_job": job.information_job,
                            "decision_use": job.decision_use,
                            "evidence_refs": sorted(job.evidence_refs),
                            "failure_posture": (
                                "PRESERVE_TYPED_FAILURE; NO_COMPLETION_CREDIT"
                            ),
                        }
                    )

    return {
        "schema_version": DEPTH_SELECTION_SCHEMA_VERSION,
        "algorithm_version": "evidence_selected_depth_v0",
        "company_id": commission.company_id,
        "portfolio_source": {
            "schema_version": str(portfolio.get("schema_version")),
            "sha256": hashlib.sha256(portfolio_bytes).hexdigest(),
        },
        "selected_products": selected_products,
        "not_selected_products": not_selected_products,
        "companion_onboarding_jobs": sorted(
            capture_jobs, key=lambda item: item["capture_job_id"]
        ),
        "selection_residuals": sorted(residuals),
        "non_claims": [
            "prominence alone does not select a product",
            "selection is not a portfolio-role or sales judgment",
            "a capture job is not successful acquisition",
            "typed route failure receives no completion credit",
        ],
    }


def build_review_linkage(
    *, commission: ReviewLinkageCommission, base_directory: Path
) -> dict[str, Any]:
    selection_path = _resolve(base_directory, commission.selection_output_path)
    selection_bytes = selection_path.read_bytes()
    selection = _decode_json_object(selection_bytes, "depth selection")
    if selection.get("schema_version") != DEPTH_SELECTION_SCHEMA_VERSION:
        raise RetailReviewOverlapError(
            "linkage requires retail_review_depth_selection_v0"
        )
    if selection.get("company_id") != commission.company_id:
        raise RetailReviewOverlapError("linkage and selection company_id values differ")
    selected_ids = {
        str(item.get("owned_parent_id"))
        for item in _object_list(selection, "selected_products")
    }
    occurrence_parent_ids = {item.owned_parent_id for item in commission.occurrences}
    total_parent_ids = {
        item.owned_parent_id for item in commission.native_review_totals
    }
    outside = sorted((occurrence_parent_ids | total_parent_ids) - selected_ids)
    if outside:
        raise RetailReviewOverlapError(
            f"linkage rows name products not selected for depth: {outside}"
        )
    review_job_bindings: dict[str, tuple[str, str, str, str]] = {}
    seen_capture_job_ids: set[str] = set()
    for item in _object_list(selection, "companion_onboarding_jobs"):
        capture_job_id = item.get("capture_job_id")
        owned_parent_id = item.get("owned_parent_id")
        retailer = item.get("retailer")
        source_product_id = item.get("source_product_id")
        surface = item.get("surface")
        if not all(
            _non_blank_text(value)
            for value in (
                capture_job_id,
                owned_parent_id,
                retailer,
                source_product_id,
                surface,
            )
        ):
            raise RetailReviewOverlapError(
                "selection has a malformed companion job binding"
            )
        if _RETAILER_SLUG.fullmatch(retailer) is None or surface not in {
            "REVIEWS",
            "QA",
        }:
            raise RetailReviewOverlapError(
                "selection has a malformed companion job binding"
            )
        if owned_parent_id not in selected_ids:
            raise RetailReviewOverlapError(
                "selection companion job names an unselected owned parent"
            )
        if capture_job_id in seen_capture_job_ids:
            raise RetailReviewOverlapError(
                f"selection has duplicate capture_job_id: {capture_job_id}"
            )
        seen_capture_job_ids.add(capture_job_id)
        if surface == "REVIEWS":
            review_job_bindings[capture_job_id] = (
                owned_parent_id,
                retailer,
                source_product_id,
                surface,
            )

    def require_exact_review_job(
        item: ReviewOccurrence | NativeReviewTotal,
    ) -> None:
        expected = (
            item.owned_parent_id,
            item.retailer,
            item.source_product_id,
            "REVIEWS",
        )
        if review_job_bindings.get(item.capture_job_id) != expected:
            raise RetailReviewOverlapError(
                "linkage row does not exactly match its selected REVIEWS "
                f"companion job: {item.capture_job_id}"
            )

    for occurrence in commission.occurrences:
        require_exact_review_job(occurrence)
    for total in commission.native_review_totals:
        require_exact_review_job(total)

    verified_refs: set[
        tuple[str, str, str, str, str, str, str]
    ] = set()
    claimed_raw_rows: dict[tuple[str, str, str], str] = {}
    for occurrence in commission.occurrences:
        for raw_ref in occurrence.raw_refs:
            _verify_raw_ref(raw_ref, base_directory, verified_refs)
            row_key = (
                raw_ref.packet_id,
                raw_ref.file_id,
                raw_ref.raw_row_anchor,
            )
            claimant = claimed_raw_rows.setdefault(
                row_key, occurrence.occurrence_id
            )
            if claimant != occurrence.occurrence_id:
                raise RetailReviewOverlapError(
                    "one raw review row backs more than one occurrence: "
                    f"{row_key} claimed by {claimant} and "
                    f"{occurrence.occurrence_id}"
                )
    for total in commission.native_review_totals:
        for raw_ref in total.raw_refs:
            _verify_raw_ref(raw_ref, base_directory, verified_refs)

    occurrences = sorted(
        commission.occurrences, key=lambda item: item.occurrence_id
    )
    occurrence_by_id = {item.occurrence_id: item for item in occurrences}
    ambiguous: list[dict[str, Any]] = []
    blocked_pairs: set[frozenset[str]] = set()
    link_candidates: list[tuple[int, str, str, str]] = []
    for index, left in enumerate(occurrences):
        for right in occurrences[index + 1 :]:
            if left.owned_parent_id != right.owned_parent_id:
                continue
            basis = _match_basis(left, right)
            conflicts = (
                _conflicting_fields(left, right)
                + _identity_conflicts(left, right, basis)
                if basis
                else []
            )
            near_conflicts = _near_match_conflicts(left, right)
            if conflicts or near_conflicts:
                candidate_basis = basis or "NORMALIZED_NEAR_MATCH"
                fields = sorted(set(conflicts + near_conflicts))
                pair = frozenset((left.occurrence_id, right.occurrence_id))
                blocked_pairs.add(pair)
                ambiguous.append(
                    {
                        "occurrence_ids": sorted(pair),
                        "candidate_basis": candidate_basis,
                        "conflicting_fields": fields,
                        "status": "AMBIGUOUS_NOT_MERGED",
                    }
                )
            elif basis:
                link_candidates.append(
                    (
                        _basis_priority(basis),
                        left.occurrence_id,
                        right.occurrence_id,
                        basis,
                    )
                )

    parent = {item.occurrence_id: item.occurrence_id for item in occurrences}

    def find(item: str) -> str:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def members(root: str) -> set[str]:
        return {item for item in parent if find(item) == root}

    accepted_links: list[dict[str, Any]] = []
    for _, left_id, right_id, basis in sorted(link_candidates):
        left_root, right_root = find(left_id), find(right_id)
        if left_root == right_root:
            accepted_links.append(
                {"occurrence_ids": [left_id, right_id], "match_basis": basis}
            )
            continue
        left_members, right_members = members(left_root), members(right_root)
        if any(
            frozenset((left, right)) in blocked_pairs
            for left in left_members
            for right in right_members
        ):
            ambiguous.append(
                {
                    "occurrence_ids": sorted(left_members | right_members),
                    "candidate_basis": basis,
                    "conflicting_fields": ["TRANSITIVE_CONFLICT"],
                    "status": "AMBIGUOUS_NOT_MERGED",
                }
            )
            continue
        parent[right_root] = left_root
        accepted_links.append(
            {"occurrence_ids": [left_id, right_id], "match_basis": basis}
        )

    groups: list[dict[str, Any]] = []
    for owned_parent_id in sorted(occurrence_parent_ids):
        product_ids = [
            item.occurrence_id
            for item in occurrences
            if item.owned_parent_id == owned_parent_id
        ]
        roots = sorted({find(item) for item in product_ids})
        for root in roots:
            group_members = sorted(item for item in product_ids if find(item) == root)
            member_links = [
                link
                for link in accepted_links
                if set(link["occurrence_ids"]).issubset(group_members)
            ]
            bases = sorted(
                {link["match_basis"] for link in member_links},
                key=_basis_priority,
            )
            unique_basis = "|".join((owned_parent_id, *group_members))
            groups.append(
                {
                    "unique_review_id": "review_"
                    + hashlib.sha256(unique_basis.encode("utf-8")).hexdigest()[:24],
                    "owned_parent_id": owned_parent_id,
                    "occurrence_ids": group_members,
                    "match_bases": bases or ["SINGLE_OCCURRENCE"],
                    "linkage_evidence": sorted(
                        member_links,
                        key=lambda item: (
                            _basis_priority(item["match_basis"]),
                            item["occurrence_ids"],
                        ),
                    ),
                }
            )

    metrics: list[dict[str, Any]] = []
    for owned_parent_id in sorted(occurrence_parent_ids):
        product_occurrences = [
            item
            for item in occurrences
            if item.owned_parent_id == owned_parent_id
        ]
        product_groups = [
            item for item in groups if item["owned_parent_id"] == owned_parent_id
        ]
        native_occurrence_total = len(product_occurrences)
        unique_total = len(product_groups)
        overlap_rate = Decimal(native_occurrence_total - unique_total) / Decimal(
            native_occurrence_total
        )
        by_retailer = [
            {
                "retailer": retailer,
                "captured_native_occurrence_total": sum(
                    1
                    for item in product_occurrences
                    if item.retailer == retailer
                ),
            }
            for retailer in sorted(
                {item.retailer for item in product_occurrences}
            )
            if any(item.retailer == retailer for item in product_occurrences)
        ]
        ambiguous_candidate_count = sum(
            1
            for item in ambiguous
            if any(
                occurrence_by_id[occurrence_id].owned_parent_id
                == owned_parent_id
                for occurrence_id in item["occurrence_ids"]
            )
        )
        metrics.append(
            {
                "owned_parent_id": owned_parent_id,
                "captured_native_occurrence_total": native_occurrence_total,
                "unique_captured_review_total": unique_total,
                "unique_captured_review_total_semantics": (
                    "EXACT_FOR_CAPTURED_WINDOW"
                    if ambiguous_candidate_count == 0
                    else "UPPER_BOUND"
                ),
                "overlap_occurrence_total": native_occurrence_total - unique_total,
                "captured_window_overlap_rate": f"{overlap_rate:.6f}",
                "captured_window_overlap_rate_semantics": (
                    "EXACT_FOR_CAPTURED_WINDOW"
                    if ambiguous_candidate_count == 0
                    else "LOWER_BOUND"
                ),
                "ambiguous_candidate_count": ambiguous_candidate_count,
                "native_occurrences_by_retailer": by_retailer,
            }
        )

    return {
        "schema_version": REVIEW_LINKAGE_SCHEMA_VERSION,
        "algorithm_version": LINKAGE_ALGORITHM_VERSION,
        "company_id": commission.company_id,
        "corpus_label": commission.corpus_label,
        "selection_source": {
            "schema_version": DEPTH_SELECTION_SCHEMA_VERSION,
            "sha256": hashlib.sha256(selection_bytes).hexdigest(),
        },
        "occurrences": [item.model_dump(mode="json") for item in occurrences],
        "native_review_totals": [
            item.model_dump(mode="json")
            for item in sorted(
                commission.native_review_totals,
                key=lambda value: (
                    value.owned_parent_id,
                    value.retailer,
                    value.corpus_window,
                ),
            )
        ],
        "unique_review_groups": sorted(
            groups,
            key=lambda item: (item["owned_parent_id"], item["unique_review_id"]),
        ),
        "ambiguous_queue": sorted(
            ambiguous,
            key=lambda item: (item["occurrence_ids"], item["candidate_basis"]),
        ),
        "metrics_by_product": metrics,
        "non_claims": [
            "native retailer totals are retained as separate source series and are never summed",
            "unique counts and overlap rates describe only the captured occurrence window",
            "ambiguous candidates are not merged",
            "when ambiguity remains, unique_captured_review_total is an upper bound and captured_window_overlap_rate is a lower bound; without ambiguity both are exact for the captured window",
            "not sales, demand, reviewer identity, authenticity, or portfolio-role judgment",
        ],
    }


def write_depth_selection(
    *, commission_path: Path, output_path: Path
) -> dict[str, Any]:
    return _write_once(
        output_path,
        build_depth_selection(
            commission=load_depth_selection_commission(commission_path),
            base_directory=commission_path.parent.resolve(),
        ),
    )


def write_review_linkage(
    *, commission_path: Path, output_path: Path
) -> dict[str, Any]:
    return _write_once(
        output_path,
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=commission_path.parent.resolve(),
        ),
    )


def _verify_raw_ref(
    raw_ref: ReviewRawRef,
    base_directory: Path,
    verified: set[tuple[str, str, str, str, str, str, str]],
) -> None:
    key = (
        raw_ref.packet_directory,
        raw_ref.packet_id,
        raw_ref.slice_id,
        raw_ref.file_id,
        raw_ref.relative_packet_path,
        raw_ref.sha256.removeprefix("sha256:").lower(),
        raw_ref.hash_basis,
    )
    if key in verified:
        return
    packet, _ = load_verified_source_capture_packet_directory(
        _resolve(base_directory, raw_ref.packet_directory)
    )
    if packet.source_family != "retail_pdp":
        raise RetailReviewOverlapError(
            "review raw ref packet source_family must be retail_pdp"
        )
    if packet.packet_id != raw_ref.packet_id:
        raise RetailReviewOverlapError(
            "review raw ref points to a different packet"
        )
    source_slice = next(
        (
            item
            for item in packet.source_slices
            if item.slice_id == raw_ref.slice_id
        ),
        None,
    )
    if source_slice is None or raw_ref.file_id not in source_slice.preserved_file_ids:
        raise RetailReviewOverlapError(
            "review raw ref is not bound to its claimed slice"
        )
    preserved = next(
        (
            item
            for item in packet.preserved_files
            if item.file_id == raw_ref.file_id
        ),
        None,
    )
    if preserved is None:
        raise RetailReviewOverlapError(
            "review raw ref names an unknown preserved file"
        )
    actual = (
        raw_ref.relative_packet_path,
        raw_ref.sha256.removeprefix("sha256:").lower(),
        raw_ref.hash_basis,
    )
    expected = (
        preserved.relative_packet_path,
        preserved.sha256.lower(),
        preserved.hash_basis,
    )
    if actual != expected:
        raise RetailReviewOverlapError(
            "review raw ref does not match the verified packet manifest"
        )
    verified.add(key)


def _match_basis(left: ReviewOccurrence, right: ReviewOccurrence) -> str | None:
    if _same_provider_id(left, right, "origin_review_id"):
        return "PROVIDER_ORIGIN_ID"
    if _same_provider_id(left, right, "source_native_review_id"):
        return "PROVIDER_NATIVE_ID"
    left_syndication = _qualified_syndication_key(left)
    if (
        left_syndication is not None
        and left_syndication == _qualified_syndication_key(right)
    ):
        return "EXPLICIT_SYNDICATION"
    if _exact_fingerprint(left) == _exact_fingerprint(right):
        return "NORMALIZED_EXACT_FINGERPRINT"
    return None


def _same_provider_id(
    left: ReviewOccurrence, right: ReviewOccurrence, field: str
) -> bool:
    left_id = _normalize_text(getattr(left, field))
    same_provider = (
        _normalize_text(left.provider) == _normalize_text(right.provider)
    )
    same_native_corpus = (
        field != "source_native_review_id"
        or (
            left.retailer == right.retailer
            and _normalize_text(left.provider_tenant_store)
            == _normalize_text(right.provider_tenant_store)
            and _normalize_text(left.collection_context)
            == _normalize_text(right.collection_context)
        )
    )
    return bool(
        left_id
        and left_id == _normalize_text(getattr(right, field))
        and same_provider
        and same_native_corpus
    )


def _qualified_syndication_key(item: ReviewOccurrence) -> str | None:
    key = _normalize_text(item.explicit_syndication_key)
    return f"{_normalize_text(item.provider)}|{key}" if key else None


def _exact_fingerprint(item: ReviewOccurrence) -> str:
    fields = (
        _normalize_rating(item.rating_value),
        _normalize_text(item.review_date_source_text),
        _normalize_text(item.reviewer_display_label),
        _normalize_text(item.review_title_verbatim),
        _normalize_text(item.review_body_verbatim),
    )
    return hashlib.sha256("\x1f".join(fields).encode("utf-8")).hexdigest()


def _near_match_conflicts(
    left: ReviewOccurrence, right: ReviewOccurrence
) -> list[str]:
    left_signature = (
        _normalize_text(left.review_date_source_text),
        _normalize_text(left.reviewer_display_label),
        _normalize_text(left.review_title_verbatim),
        _normalize_text(left.review_body_verbatim),
    )
    right_signature = (
        _normalize_text(right.review_date_source_text),
        _normalize_text(right.reviewer_display_label),
        _normalize_text(right.review_title_verbatim),
        _normalize_text(right.review_body_verbatim),
    )
    if (
        left_signature == right_signature
        and _normalize_rating(left.rating_value)
        != _normalize_rating(right.rating_value)
    ):
        return ["rating_value"]
    return []


_IDENTITY_TIERS: tuple[tuple[str, str, bool], ...] = (
    ("origin_review_id", "PROVIDER_ORIGIN_ID", False),
    ("source_native_review_id", "PROVIDER_NATIVE_ID", True),
    ("explicit_syndication_key", "EXPLICIT_SYNDICATION", False),
)


def _identity_conflicts(
    left: ReviewOccurrence, right: ReviewOccurrence, basis: str
) -> list[str]:
    """Provider identity fields that outrank ``basis`` and disagree.

    A weaker match never overrides a stronger identity signal: when the same
    provider gives the two rows different ids, the provider itself calls them
    different reviews, so the pair belongs in the ambiguous queue rather than a
    merged unique review. Native ids are retailer-scoped because one syndicated
    review legitimately carries a different native id at each retailer.
    """
    if _normalize_text(left.provider) != _normalize_text(right.provider):
        return []
    basis_priority = _basis_priority(basis)
    conflicts: list[str] = []
    for field, tier, retailer_scoped in _IDENTITY_TIERS:
        if _basis_priority(tier) >= basis_priority:
            continue
        if retailer_scoped and left.retailer != right.retailer:
            continue
        left_value = _normalize_text(getattr(left, field))
        right_value = _normalize_text(getattr(right, field))
        if left_value and right_value and left_value != right_value:
            conflicts.append(field)
    return conflicts


def _conflicting_fields(
    left: ReviewOccurrence, right: ReviewOccurrence
) -> list[str]:
    comparisons = {
        "rating_value": (
            _normalize_rating(left.rating_value),
            _normalize_rating(right.rating_value),
        ),
        "review_date_source_text": (
            _normalize_text(left.review_date_source_text),
            _normalize_text(right.review_date_source_text),
        ),
        "reviewer_display_label": (
            _normalize_text(left.reviewer_display_label),
            _normalize_text(right.reviewer_display_label),
        ),
        "review_title_verbatim": (
            _normalize_text(left.review_title_verbatim),
            _normalize_text(right.review_title_verbatim),
        ),
        "review_body_verbatim": (
            _normalize_text(left.review_body_verbatim),
            _normalize_text(right.review_body_verbatim),
        ),
    }
    return sorted(
        field
        for field, (left_value, right_value) in comparisons.items()
        if left_value and right_value and left_value != right_value
    )


def _basis_priority(basis: str) -> int:
    return {
        "PROVIDER_ORIGIN_ID": 0,
        "PROVIDER_NATIVE_ID": 1,
        "EXPLICIT_SYNDICATION": 2,
        "NORMALIZED_EXACT_FINGERPRINT": 3,
        "NORMALIZED_NEAR_MATCH": 4,
        "SINGLE_OCCURRENCE": 5,
    }.get(basis, 99)


def _normalize_text(value: object) -> str:
    if value is None:
        return ""
    return " ".join(
        unicodedata.normalize("NFKC", str(value)).split()
    ).casefold()


def _normalize_rating(value: object) -> str:
    if value is None:
        return ""
    try:
        normalized = Decimal(str(value)).normalize()
    except InvalidOperation:
        return _normalize_text(value)
    if not normalized.is_finite():
        raise RetailReviewOverlapError("rating_value must be finite")
    return format(normalized, "f")


def _is_most_recent_ordering(value: str) -> bool:
    normalized = _normalize_text(value)
    return any(
        token in normalized
        for token in ("most recent", "newest", "date desc", "submissiontime desc")
    )


def _non_blank_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _retailer_slug(value: str) -> str:
    if _RETAILER_SLUG.fullmatch(value) is None:
        raise ValueError("retailer must be a lowercase slug")
    return value


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    return _decode_json_object(path.read_bytes(), label)


def _decode_json_object(body: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RetailReviewOverlapError(
            f"{label} is not valid UTF-8 JSON"
        ) from exc
    if not isinstance(value, dict):
        raise RetailReviewOverlapError(f"{label} must be a JSON object")
    return value


def _object_list(
    value: dict[str, Any], field: str
) -> list[dict[str, Any]]:
    items = value.get(field)
    if not isinstance(items, list) or any(
        not isinstance(item, dict) for item in items
    ):
        raise RetailReviewOverlapError(
            f"{field} must be a list of objects"
        )
    return items


def _resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _write_once(
    output_path: Path, result: dict[str, Any]
) -> dict[str, Any]:
    if output_path.exists():
        raise RetailReviewOverlapError(
            f"output already exists; refusing overwrite: {output_path}"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
        + chr(10),
        encoding="utf-8",
    )
    return result


__all__ = [
    "DEPTH_SELECTION_SCHEMA_VERSION",
    "LINKAGE_ALGORITHM_VERSION",
    "REVIEW_LINKAGE_SCHEMA_VERSION",
    "DepthSelectionCommission",
    "RetailReviewOverlapError",
    "ReviewLinkageCommission",
    "build_depth_selection",
    "build_review_linkage",
    "load_depth_selection_commission",
    "load_review_linkage_commission",
    "write_depth_selection",
    "write_review_linkage",
]
