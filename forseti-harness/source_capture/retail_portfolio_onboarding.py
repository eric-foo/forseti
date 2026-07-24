"""Compose owned census, verified retail grids, and raw PDP baselines."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Literal
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from pydantic import Field, field_validator, model_validator
from schemas.case_models import StrictModel
from source_capture.models import VisibleFactStatus
from source_capture.retail_capture_profiles import (
    extract_retailer_product_identity_from_url,
    extract_retailer_variant_identity_from_url,
)
from source_capture.retail_grid_projection import (
    RetailGridProjectionInputError,
    build_retail_grid_projection,
    detect_retail_grid_retailer,
    load_verified_source_capture_packet_directory,
)

SCHEMA_VERSION = "retail_portfolio_onboarding_v2"
Retailer = str
AuthorizationStatus = Literal[
    "OFFICIALLY_NAMED", "NOT_OFFICIALLY_NAMED", "UNKNOWN"
]
OutcomeStatus = Literal["GRID_CAPTURED_COMPLETE", "GRID_CAPTURED_INCOMPLETE",
    "NOT_LISTED", "ROUTE_BLOCKED", "MARKET_UNPINNED", "SURFACE_NOT_EXPOSED"]
ListingKind = Literal["PARENT", "VARIANT_URL", "BUNDLE_SET"]
MatchStatus = Literal["EXACT", "AMBIGUOUS", "UNMATCHED"]
FamilyMemberRole = Literal["PRIMARY_PARENT", "VARIANT_AS_PARENT"]
NonFamilyKind = Literal[
    "BUNDLE_SET", "SAMPLE_GIFT", "MERCHANDISE", "LEGACY_OTHER"
]
_RETAILER_SLUG = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
_SHA256 = re.compile(r"(?:sha256:)?[0-9a-fA-F]{64}")
_STABLE_IDENTITY_RETAILERS = frozenset(
    {"amazon", "revolve", "sephora", "target", "ulta"}
)
_VARIANT_IDENTITY_RETAILERS = frozenset({"sephora", "target", "ulta"})

class RetailPortfolioOnboardingError(ValueError):
    """Inputs cannot produce truthful deterministic coverage."""

class OwnedParent(StrictModel):
    owned_parent_id: str
    name: str
    owned_url: str
    category: str | None = None
    franchise: str | None = None
    material_variant_ids: list[str] = Field(default_factory=list)

class OwnedCensus(StrictModel):
    source_packet_id: str
    parents: list[OwnedParent] = Field(min_length=1)


class IdentityEvidenceRef(StrictModel):
    artifact_path: str
    artifact_sha256: str
    locator: str

    @field_validator("artifact_path", "locator")
    @classmethod
    def reject_blank_value(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("identity evidence fields must be non-empty")
        return value

    @field_validator("artifact_sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        if _SHA256.fullmatch(value) is None:
            raise ValueError("artifact_sha256 must be a 64-character SHA-256 digest")
        return value.removeprefix("sha256:").lower()


class NormalizedFamilyMember(StrictModel):
    owned_parent_id: str
    role: FamilyMemberRole
    evidence_refs: list[IdentityEvidenceRef] = Field(min_length=1)


class NormalizedProductFamily(StrictModel):
    normalized_family_id: str
    display_name: str
    members: list[NormalizedFamilyMember] = Field(min_length=1)

    @field_validator("normalized_family_id", "display_name")
    @classmethod
    def reject_blank_value(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("normalized family fields must be non-empty")
        return value

    @model_validator(mode="after")
    def unique_members_and_primary(self) -> "NormalizedProductFamily":
        member_ids = [item.owned_parent_id for item in self.members]
        if len(member_ids) != len(set(member_ids)):
            raise ValueError("a normalized family cannot repeat an owned parent")
        primary_count = sum(item.role == "PRIMARY_PARENT" for item in self.members)
        if primary_count > 1:
            raise ValueError("a normalized family can name at most one primary parent")
        return self


class NonFamilySourceObject(StrictModel):
    owned_parent_id: str
    kind: NonFamilyKind
    component_family_ids: list[str] = Field(default_factory=list)
    evidence_refs: list[IdentityEvidenceRef] = Field(min_length=1)

    @model_validator(mode="after")
    def valid_components(self) -> "NonFamilySourceObject":
        if len(self.component_family_ids) != len(set(self.component_family_ids)):
            raise ValueError("component_family_ids must be unique")
        if self.kind != "BUNDLE_SET" and self.component_family_ids:
            raise ValueError("only BUNDLE_SET objects may name component families")
        return self

class RetailerAuthorization(StrictModel):
    retailer: Retailer
    status: AuthorizationStatus
    evidence_refs: list[str] = Field(min_length=1)

    @field_validator("retailer")
    @classmethod
    def valid_retailer_slug(cls, value: str) -> str:
        return _retailer_slug(value)

class RetailerOutcome(StrictModel):
    retailer: Retailer
    status: OutcomeStatus
    evidence_refs: list[str] = Field(min_length=1)
    grid_packet_directory: str | None = None

    @field_validator("retailer")
    @classmethod
    def valid_retailer_slug(cls, value: str) -> str:
        return _retailer_slug(value)

    @model_validator(mode="after")
    def captured_status_has_grid(self) -> "RetailerOutcome":
        captured = self.status.startswith("GRID_CAPTURED_")
        if captured != (self.grid_packet_directory is not None):
            raise ValueError("grid_packet_directory is required exactly for captured outcomes")
        return self

class ListingReconciliation(StrictModel):
    retailer: Retailer
    grid_row_id: str
    source_product_id: str
    listing_url: str
    listing_kind: ListingKind
    match_status: MatchStatus
    owned_parent_ids: list[str] = Field(default_factory=list)
    material_variant_ids: list[str] = Field(default_factory=list)
    retailer_variant_id: str | None = None

    @field_validator("retailer")
    @classmethod
    def valid_retailer_slug(cls, value: str) -> str:
        return _retailer_slug(value)

    @field_validator("retailer_variant_id")
    @classmethod
    def reject_blank_retailer_variant_id(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("retailer_variant_id must be non-empty when supplied")
        return value

    @model_validator(mode="after")
    def match_cardinality(self) -> "ListingReconciliation":
        if (
            self.retailer_variant_id is not None
            and self.retailer not in _VARIANT_IDENTITY_RETAILERS
        ):
            raise ValueError(
                "retailer_variant_id is not supported for retailer "
                f"{self.retailer!r}"
            )
        parents = set(self.owned_parent_ids)
        if len(parents) != len(self.owned_parent_ids):
            raise ValueError("owned_parent_ids must be unique")
        if self.match_status == "EXACT" and not parents:
            raise ValueError("EXACT reconciliation requires an owned parent")
        if self.match_status == "EXACT" and self.listing_kind != "BUNDLE_SET" and len(parents) != 1:
            raise ValueError("an exact parent or variant URL maps to one owned parent")
        if self.match_status == "AMBIGUOUS" and len(parents) < 2:
            raise ValueError("AMBIGUOUS reconciliation requires two candidate parents")
        if self.match_status == "UNMATCHED" and parents:
            raise ValueError("UNMATCHED reconciliation cannot name an owned parent")
        return self

class PdpBaseline(StrictModel):
    retailer: Retailer
    source_product_id: str
    packet_directory: str

    @field_validator("retailer")
    @classmethod
    def valid_retailer_slug(cls, value: str) -> str:
        return _retailer_slug(value)

class PortfolioCommission(StrictModel):
    company_id: str
    owned_census: OwnedCensus
    retailer_authorizations: list[RetailerAuthorization] = Field(min_length=1)
    primary_retailer: Retailer | None = None
    retailer_outcomes: list[RetailerOutcome] = Field(min_length=1)
    listing_reconciliations: list[ListingReconciliation] = Field(default_factory=list)
    pdp_baselines: list[PdpBaseline] = Field(default_factory=list)
    normalized_product_families: list[NormalizedProductFamily] = Field(
        default_factory=list
    )
    non_family_source_objects: list[NonFamilySourceObject] = Field(
        default_factory=list
    )

    @field_validator("primary_retailer")
    @classmethod
    def valid_primary_retailer_slug(cls, value: str | None) -> str | None:
        return None if value is None else _retailer_slug(value)

    @model_validator(mode="after")
    def official_first_selection_and_unique_parents(self) -> "PortfolioCommission":
        authorizations = [item.retailer for item in self.retailer_authorizations]
        if len(authorizations) != len(set(authorizations)):
            raise ValueError("retailer_authorizations must name each retailer once")
        if "sephora" not in authorizations:
            raise ValueError("retailer_authorizations must explicitly resolve sephora")
        officially_named = {
            item.retailer
            for item in self.retailer_authorizations
            if item.status == "OFFICIALLY_NAMED"
        }
        retailers = [item.retailer for item in self.retailer_outcomes]
        if len(retailers) != len(set(retailers)):
            raise ValueError("retailer_outcomes must name each selected retailer once")
        unconfirmed = sorted(set(retailers) - officially_named)
        if unconfirmed:
            raise ValueError(
                "retailer_outcomes require company-owned official evidence: "
                f"{unconfirmed}"
            )
        outcomes = {item.retailer: item for item in self.retailer_outcomes}
        if "sephora" in officially_named and "sephora" not in outcomes:
            raise ValueError("officially named sephora must remain in retailer_outcomes")
        complete = {
            item.retailer
            for item in self.retailer_outcomes
            if item.status == "GRID_CAPTURED_COMPLETE"
        }
        if self.primary_retailer is None and complete:
            raise ValueError("primary_retailer is required when a complete grid exists")
        if self.primary_retailer is not None and self.primary_retailer not in complete:
            raise ValueError("primary_retailer must have GRID_CAPTURED_COMPLETE")
        if (
            "sephora" in officially_named
            and outcomes["sephora"].status == "GRID_CAPTURED_COMPLETE"
            and self.primary_retailer != "sephora"
        ):
            raise ValueError(
                "officially named, route-complete sephora must be primary_retailer"
            )
        selected = set(retailers)
        attached = {
            item.retailer
            for item in (*self.listing_reconciliations, *self.pdp_baselines)
        }
        if not attached.issubset(selected):
            raise ValueError(
                "reconciliations and baselines must use selected retailer_outcomes"
            )
        ids = [item.owned_parent_id for item in self.owned_census.parents]
        if len(ids) != len(set(ids)):
            raise ValueError("owned_parent_id values must be unique")
        parent_ids = set(ids)
        family_ids = [
            item.normalized_family_id for item in self.normalized_product_families
        ]
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("normalized_family_id values must be unique")
        family_members = [
            member.owned_parent_id
            for family in self.normalized_product_families
            for member in family.members
        ]
        if len(family_members) != len(set(family_members)):
            raise ValueError("an owned parent may belong to only one normalized family")
        non_family_ids = [
            item.owned_parent_id for item in self.non_family_source_objects
        ]
        if len(non_family_ids) != len(set(non_family_ids)):
            raise ValueError("non-family source objects must name each parent once")
        overlap = sorted(set(family_members) & set(non_family_ids))
        if overlap:
            raise ValueError(
                f"owned parents cannot be both family and non-family objects: {overlap}"
            )
        unknown = sorted((set(family_members) | set(non_family_ids)) - parent_ids)
        if unknown:
            raise ValueError(f"product identity names unknown owned parents: {unknown}")
        unknown_components = sorted(
            {
                component
                for item in self.non_family_source_objects
                for component in item.component_family_ids
            }
            - set(family_ids)
        )
        if unknown_components:
            raise ValueError(
                f"bundle components name unknown normalized families: {unknown_components}"
            )
        return self

def load_portfolio_commission(path: Path) -> PortfolioCommission:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RetailPortfolioOnboardingError("commission must be a JSON object")
    _reject_judgment_keys(raw)
    return PortfolioCommission.model_validate(raw)

def build_retail_portfolio_onboarding(*, commission: PortfolioCommission, base_directory: Path) -> dict[str, Any]:
    _verify_identity_evidence_refs(
        commission=commission, base_directory=base_directory
    )
    parents = {item.owned_parent_id: item for item in commission.owned_census.parents}
    outcomes = {item.retailer: item for item in commission.retailer_outcomes}
    retailers = _retailer_order(commission)
    grid_rows: dict[tuple[str, str], Any] = {}
    outcome_rows: list[dict[str, Any]] = []
    for retailer in retailers:
        outcome = outcomes[retailer]
        rendered: dict[str, Any] = {"retailer": retailer, "status": outcome.status,
            "evidence_refs": outcome.evidence_refs, "grid_packet_id": None,
            "grid_completeness": None, "grid_row_count": 0}
        if outcome.grid_packet_directory is not None:
            packet, raw_file_bytes_by_file_id = load_verified_source_capture_packet_directory(
                _resolve(base_directory, outcome.grid_packet_directory))
            try:
                packet_retailer = detect_retail_grid_retailer(packet)
            except RetailGridProjectionInputError as exc:
                raise RetailPortfolioOnboardingError(
                    f"{retailer} outcome points to a packet without an admitted grid retailer locator"
                ) from exc
            if packet_retailer != retailer:
                raise RetailPortfolioOnboardingError(
                    f"{retailer} outcome points to a {packet_retailer} packet")
            projection = build_retail_grid_projection(
                packet=packet, raw_file_bytes_by_file_id=raw_file_bytes_by_file_id)
            complete = projection.completeness.status == "complete"
            if (outcome.status == "GRID_CAPTURED_COMPLETE") != complete:
                raise RetailPortfolioOnboardingError(f"{retailer} status contradicts projection completeness")
            rendered.update(grid_packet_id=projection.packet_id,
                grid_completeness=projection.completeness.model_dump(mode="json"),
                grid_row_count=len(projection.rows))
            for row in projection.rows:
                row_keys = [(retailer, row.row_id)]
                if retailer == "target":
                    row_prefix = row.row_id.rsplit(":", 2)[0]
                    product_id = str(row.source_visible_fields["source_product_id"])
                    row_keys.extend(
                        (
                            retailer,
                            f"{row_prefix}:{placement.grid_position - 1}:{product_id}",
                        )
                        for placement in row.placements
                    )
                for key in dict.fromkeys(row_keys):
                    existing = grid_rows.get(key)
                    if existing is not None and existing.row_id != row.row_id:
                        raise RetailPortfolioOnboardingError(f"duplicate grid row: {key}")
                    grid_rows[key] = row
        outcome_rows.append(rendered)

    reconciled: dict[tuple[str, str], ListingReconciliation] = {}
    for item in commission.listing_reconciliations:
        key = (item.retailer, item.grid_row_id)
        if key in reconciled:
            raise RetailPortfolioOnboardingError(f"duplicate reconciliation: {key}")
        row = grid_rows.get(key)
        if row is None:
            raise RetailPortfolioOnboardingError(f"reconciliation has no grid row: {key}")
        fields = row.source_visible_fields
        if item.source_product_id != str(fields["source_product_id"]):
            raise RetailPortfolioOnboardingError(f"product identity mismatch: {key}")
        _validate_retail_identity(
            retailer=item.retailer,
            source_product_id=item.source_product_id,
            expected_url=item.listing_url,
            observed_url=str(fields["product_url"]),
            retailer_variant_id=item.retailer_variant_id,
            context=f"listing URL mismatch: {key}",
        )
        unknown = set(item.owned_parent_ids) - set(parents)
        if unknown:
            raise RetailPortfolioOnboardingError(f"unknown owned parents: {sorted(unknown)}")
        for parent_id in item.owned_parent_ids:
            bad = set(item.material_variant_ids) - set(parents[parent_id].material_variant_ids)
            if bad:
                raise RetailPortfolioOnboardingError(f"{key} names non-census variants: {sorted(bad)}")
        reconciled[key] = item
    missing = sorted(set(grid_rows) - set(reconciled))
    if missing:
        raise RetailPortfolioOnboardingError(f"every verified grid row requires reconciliation: {missing}")

    groups: dict[tuple[str, str], list[ListingReconciliation]] = {}
    residuals: list[str] = []
    for item in commission.listing_reconciliations:
        groups.setdefault((item.retailer, item.source_product_id), []).append(item)
        if item.listing_kind != "PARENT":
            residuals.append(f"{item.listing_kind}:{item.retailer}:{item.source_product_id}:{item.grid_row_id}")
        if item.match_status != "EXACT":
            residuals.append(f"{item.match_status}_MATCH:{item.retailer}:{item.source_product_id}:{item.grid_row_id}")

    exact_keys: set[tuple[str, str]] = set()
    identities: list[dict[str, Any]] = []
    for key, rows in sorted(groups.items()):
        if len(rows) > 1:
            residuals.append(f"DUPLICATE_LISTING:{key[0]}:{key[1]}:occurrences={len(rows)}")
        exact = [row for row in rows if row.match_status == "EXACT" and row.listing_kind != "BUNDLE_SET"]
        exact_parents = sorted({parent for row in exact for parent in row.owned_parent_ids})
        if len(exact_parents) > 1:
            raise RetailPortfolioOnboardingError(f"one listing maps exactly to multiple parents: {key}")
        if exact:
            exact_keys.add(key)
        identities.append({"retailer": key[0], "source_product_id": key[1],
            "occurrence_row_ids": sorted(row.grid_row_id for row in rows),
            "listing_kinds": sorted({row.listing_kind for row in rows}),
            "match_statuses": sorted({row.match_status for row in rows}),
            "exact_owned_parent_ids": exact_parents})

    baselines: dict[tuple[str, str], PdpBaseline] = {}
    for item in commission.pdp_baselines:
        key = (item.retailer, item.source_product_id)
        if key in baselines:
            raise RetailPortfolioOnboardingError(f"duplicate PDP baseline: {key}")
        baselines[key] = item
    if set(baselines) != exact_keys:
        raise RetailPortfolioOnboardingError("PDP baselines must equal exact non-bundle listings; "
            f"missing={sorted(exact_keys-set(baselines))}; extra={sorted(set(baselines)-exact_keys)}")

    verified_baselines: list[dict[str, Any]] = []
    for key in sorted(exact_keys):
        ref = baselines[key]
        packet, _ = load_verified_source_capture_packet_directory(
            _resolve(base_directory, ref.packet_directory))
        if packet.source_family != "retail_pdp":
            raise RetailPortfolioOnboardingError(f"baseline is not retail_pdp: {packet.packet_id}")
        if packet.source_locator.status != VisibleFactStatus.KNOWN or packet.source_locator.value is None:
            raise RetailPortfolioOnboardingError(f"baseline locator is unknown: {packet.packet_id}")
        exact_rows = [
            row
            for row in groups[key]
            if row.match_status == "EXACT" and row.listing_kind != "BUNDLE_SET"
        ]
        if not any(
            _retail_identity_matches(
                retailer=row.retailer,
                source_product_id=row.source_product_id,
                expected_url=row.listing_url,
                observed_url=packet.source_locator.value,
                retailer_variant_id=row.retailer_variant_id,
            )
            for row in exact_rows
        ):
            raise RetailPortfolioOnboardingError(
                f"baseline locator does not bind {key}: {packet.packet_id}"
            )
        verified_baselines.append({"retailer": ref.retailer, "source_product_id": ref.source_product_id,
            "packet_id": packet.packet_id, "source_locator": packet.source_locator.value,
            "preserved_file_count": len(packet.preserved_files)})

    coverage: list[dict[str, Any]] = []
    for retailer in retailers:
        rows = [row for row in commission.listing_reconciliations if row.retailer == retailer]
        covered = sorted({parent for row in rows if row.match_status == "EXACT"
            and row.listing_kind != "BUNDLE_SET" for parent in row.owned_parent_ids})
        if not outcomes[retailer].status.startswith("GRID_CAPTURED_"):
            residuals.append(f"RETAILER_OUTCOME:{retailer}:{outcomes[retailer].status}")
        else:
            for parent_id in sorted(set(parents)-set(covered)):
                residuals.append(f"PARENT_NOT_LISTED:{retailer}:{parent_id}")
            observed: dict[str, set[str]] = {}
            for row in rows:
                if row.match_status == "EXACT" and row.listing_kind != "BUNDLE_SET":
                    for parent_id in row.owned_parent_ids:
                        observed.setdefault(parent_id, set()).update(row.material_variant_ids)
            for parent_id in covered:
                for variant in sorted(set(parents[parent_id].material_variant_ids)-observed.get(parent_id,set())):
                    residuals.append(f"MISSING_MATERIAL_VARIANT:{retailer}:{parent_id}:{variant}")
        coverage.append({"retailer": retailer, "outcome_status": outcomes[retailer].status,
            "owned_parent_denominator": len(parents), "covered_owned_parent_ids": covered,
            "covered_owned_parent_count": len(covered),
            "exact_listing_count": sum(1 for key in exact_keys if key[0] == retailer)})

    family_members = {
        member.owned_parent_id
        for family in commission.normalized_product_families
        for member in family.members
    }
    non_family_ids = {
        item.owned_parent_id for item in commission.non_family_source_objects
    }
    unresolved_parent_ids = sorted(set(parents) - family_members - non_family_ids)
    family_denominator_complete = not unresolved_parent_ids
    product_identity = {
        "source_parent_count": len(parents),
        "resolved_family_count": len(commission.normalized_product_families),
        "normalized_family_count": (
            len(commission.normalized_product_families)
            if family_denominator_complete
            else None
        ),
        "family_denominator_state": (
            "COMPLETE" if family_denominator_complete else "PARTIAL"
        ),
        "family_member_parent_count": len(family_members),
        "variant_as_parent_count": sum(
            member.role == "VARIANT_AS_PARENT"
            for family in commission.normalized_product_families
            for member in family.members
        ),
        "material_variant_id_count": sum(
            len(parent.material_variant_ids) for parent in parents.values()
        ),
        "bundle_set_parent_count": sum(
            item.kind == "BUNDLE_SET"
            for item in commission.non_family_source_objects
        ),
        "non_product_parent_count": sum(
            item.kind != "BUNDLE_SET"
            for item in commission.non_family_source_objects
        ),
        "unresolved_parent_count": len(unresolved_parent_ids),
        "unresolved_owned_parent_ids": unresolved_parent_ids,
        "normalized_product_families": [
            item.model_dump(mode="json")
            for item in sorted(
                commission.normalized_product_families,
                key=lambda value: value.normalized_family_id,
            )
        ],
        "non_family_source_objects": [
            item.model_dump(mode="json")
            for item in sorted(
                commission.non_family_source_objects,
                key=lambda value: value.owned_parent_id,
            )
        ],
    }

    return {"schema_version": SCHEMA_VERSION,
        "certification": "coverage_composition_only; not_depth_selection; not_judgment",
        "company_id": commission.company_id,
        "retailer_authorizations": [
            item.model_dump(mode="json")
            for item in sorted(
                commission.retailer_authorizations, key=lambda value: value.retailer
            )
        ],
        "primary_retailer": commission.primary_retailer,
        "owned_census_source_packet_id": commission.owned_census.source_packet_id,
        "owned_parent_count": len(parents),
        "owned_parents": [item.model_dump(mode="json") for item in sorted(
            commission.owned_census.parents, key=lambda value: value.owned_parent_id)],
        "product_identity": product_identity,
        "retailer_outcomes": outcome_rows,
        "listing_reconciliations": [item.model_dump(mode="json") for item in sorted(
            commission.listing_reconciliations, key=lambda value: (value.retailer,value.grid_row_id))],
        "listing_identities": identities, "pdp_baselines": verified_baselines,
        "coverage_by_retailer": coverage, "coverage_residuals": sorted(set(residuals)),
        "non_claims": ["not a complete global SKU graph", "not inferred from product names or categories",
            "a PARTIAL family denominator is not a complete normalized product count",
            "not sales or internal economics",
            "not hero, growth, or weak-link selection",
            "typed route failure receives no coverage credit"]}

def write_retail_portfolio_onboarding(*, commission_path: Path, output_path: Path) -> dict[str, Any]:
    if output_path.exists():
        raise RetailPortfolioOnboardingError(f"output already exists; refusing overwrite: {output_path}")
    result = build_retail_portfolio_onboarding(
        commission=load_portfolio_commission(commission_path),
        base_directory=commission_path.parent.resolve())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{json.dumps(result,indent=2,sort_keys=True)}\n",encoding="utf-8")
    return result

def _resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (base/path).resolve()


def _verify_identity_evidence_refs(
    *, commission: PortfolioCommission, base_directory: Path
) -> None:
    refs = {
        (
            evidence.artifact_path,
            evidence.artifact_sha256,
            evidence.locator,
        )
        for family in commission.normalized_product_families
        for member in family.members
        for evidence in member.evidence_refs
    }
    refs.update(
        (
            evidence.artifact_path,
            evidence.artifact_sha256,
            evidence.locator,
        )
        for item in commission.non_family_source_objects
        for evidence in item.evidence_refs
    )
    verified_files: set[tuple[Path, str]] = set()
    for artifact_path, expected_sha256, locator in sorted(refs):
        resolved = _resolve(base_directory, artifact_path)
        if not resolved.is_file():
            raise RetailPortfolioOnboardingError(
                "product identity evidence artifact is not a readable file: "
                f"{artifact_path} ({locator})"
            )
        file_key = (resolved, expected_sha256)
        if file_key in verified_files:
            continue
        actual_sha256 = hashlib.sha256(resolved.read_bytes()).hexdigest()
        if actual_sha256 != expected_sha256:
            raise RetailPortfolioOnboardingError(
                "product identity evidence hash mismatch: "
                f"{artifact_path} ({locator})"
            )
        verified_files.add(file_key)


def _canonical(value: str) -> str:
    parsed=urlparse(value.strip())
    return urlunparse((parsed.scheme.lower(),parsed.netloc.lower(),parsed.path.rstrip("/"),"",
        urlencode(sorted(parse_qsl(parsed.query,keep_blank_values=True))),""))


def _retail_identity_matches(
    *,
    retailer: str,
    source_product_id: str,
    expected_url: str,
    observed_url: str,
    retailer_variant_id: str | None,
) -> bool:
    if retailer not in _STABLE_IDENTITY_RETAILERS:
        return _canonical(expected_url) == _canonical(observed_url)
    expected_route = urlparse(expected_url.strip())
    observed_route = urlparse(observed_url.strip())
    if (
        expected_route.scheme.lower() != "https"
        or observed_route.scheme.lower() != "https"
        or expected_route.netloc.lower() != observed_route.netloc.lower()
    ):
        return False
    expected_product = extract_retailer_product_identity_from_url(
        retailer, expected_url
    )
    observed_product = extract_retailer_product_identity_from_url(
        retailer, observed_url
    )
    if (
        expected_product is None
        or observed_product is None
        or expected_product != source_product_id
        or observed_product != source_product_id
    ):
        return False
    if retailer_variant_id is None:
        return True
    return (
        extract_retailer_variant_identity_from_url(retailer, expected_url)
        == retailer_variant_id
        and extract_retailer_variant_identity_from_url(retailer, observed_url)
        == retailer_variant_id
    )


def _validate_retail_identity(
    *,
    retailer: str,
    source_product_id: str,
    expected_url: str,
    observed_url: str,
    retailer_variant_id: str | None,
    context: str,
) -> None:
    if not _retail_identity_matches(
        retailer=retailer,
        source_product_id=source_product_id,
        expected_url=expected_url,
        observed_url=observed_url,
        retailer_variant_id=retailer_variant_id,
    ):
        raise RetailPortfolioOnboardingError(context)

def _retailer_slug(value: str) -> str:
    if _RETAILER_SLUG.fullmatch(value) is None:
        raise ValueError("retailer must be a lowercase slug")
    return value

def _retailer_order(commission: PortfolioCommission) -> list[str]:
    retailers = sorted(item.retailer for item in commission.retailer_outcomes)
    if commission.primary_retailer is None:
        return retailers
    return [commission.primary_retailer] + [
        retailer for retailer in retailers if retailer != commission.primary_retailer
    ]

def _reject_judgment_keys(value: Any, path: str = "$") -> None:
    if isinstance(value,dict):
        for key,child in value.items():
            normalized=str(key).lower().replace("-","_")
            if any(token in normalized for token in ("hero","growth","weak_link","weaklink")):
                raise RetailPortfolioOnboardingError(f"forbidden Judgment key at {path}.{key}")
            _reject_judgment_keys(child,f"{path}.{key}")
    elif isinstance(value,list):
        for index,child in enumerate(value):
            _reject_judgment_keys(child,f"{path}[{index}]")
