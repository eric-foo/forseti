"""Compose owned census, verified retail grids, and raw PDP baselines."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Literal
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from pydantic import Field, model_validator
from schemas.case_models import StrictModel
from source_capture.models import VisibleFactStatus
from source_capture.retail_grid_projection import (
    build_retail_grid_projection_from_packet_directory,
    load_verified_source_capture_packet_directory,
)

SCHEMA_VERSION = "retail_portfolio_onboarding_v0"
LADDER = ("sephora", "ulta", "target", "amazon")
Retailer = Literal["sephora", "ulta", "target", "amazon"]
OutcomeStatus = Literal["GRID_CAPTURED_COMPLETE", "GRID_CAPTURED_INCOMPLETE",
    "NOT_LISTED", "ROUTE_BLOCKED", "MARKET_UNPINNED", "SURFACE_NOT_EXPOSED"]
ListingKind = Literal["PARENT", "VARIANT_URL", "BUNDLE_SET"]
MatchStatus = Literal["EXACT", "AMBIGUOUS", "UNMATCHED"]

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

class RetailerOutcome(StrictModel):
    retailer: Retailer
    status: OutcomeStatus
    evidence_refs: list[str] = Field(min_length=1)
    grid_packet_directory: str | None = None

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

    @model_validator(mode="after")
    def match_cardinality(self) -> "ListingReconciliation":
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

class PortfolioCommission(StrictModel):
    company_id: str
    owned_census: OwnedCensus
    retailer_outcomes: list[RetailerOutcome]
    listing_reconciliations: list[ListingReconciliation] = Field(default_factory=list)
    pdp_baselines: list[PdpBaseline] = Field(default_factory=list)

    @model_validator(mode="after")
    def exact_ladder_and_unique_parents(self) -> "PortfolioCommission":
        retailers = [item.retailer for item in self.retailer_outcomes]
        if len(retailers) != len(set(retailers)) or set(retailers) != set(LADDER):
            raise ValueError("retailer_outcomes must contain the four ladder retailers once")
        ids = [item.owned_parent_id for item in self.owned_census.parents]
        if len(ids) != len(set(ids)):
            raise ValueError("owned_parent_id values must be unique")
        return self

def load_portfolio_commission(path: Path) -> PortfolioCommission:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RetailPortfolioOnboardingError("commission must be a JSON object")
    _reject_judgment_keys(raw)
    return PortfolioCommission.model_validate(raw)

def build_retail_portfolio_onboarding(*, commission: PortfolioCommission, base_directory: Path) -> dict[str, Any]:
    parents = {item.owned_parent_id: item for item in commission.owned_census.parents}
    outcomes = {item.retailer: item for item in commission.retailer_outcomes}
    grid_rows: dict[tuple[str, str], Any] = {}
    outcome_rows: list[dict[str, Any]] = []
    for retailer in LADDER:
        outcome = outcomes[retailer]
        rendered: dict[str, Any] = {"retailer": retailer, "status": outcome.status,
            "evidence_refs": outcome.evidence_refs, "grid_packet_id": None,
            "grid_completeness": None, "grid_row_count": 0}
        if outcome.grid_packet_directory is not None:
            projection = build_retail_grid_projection_from_packet_directory(
                packet_directory=_resolve(base_directory, outcome.grid_packet_directory))
            row_retailers = {row.retailer for row in projection.rows}
            if row_retailers and row_retailers != {retailer}:
                raise RetailPortfolioOnboardingError(f"{retailer} outcome points to {sorted(row_retailers)}")
            complete = projection.completeness.status == "complete"
            if (outcome.status == "GRID_CAPTURED_COMPLETE") != complete:
                raise RetailPortfolioOnboardingError(f"{retailer} status contradicts projection completeness")
            rendered.update(grid_packet_id=projection.packet_id,
                grid_completeness=projection.completeness.model_dump(mode="json"),
                grid_row_count=len(projection.rows))
            for row in projection.rows:
                key = (retailer, row.row_id)
                if key in grid_rows:
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
        if _canonical(item.listing_url) != _canonical(str(fields["product_url"])):
            raise RetailPortfolioOnboardingError(f"listing URL mismatch: {key}")
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
        locators = {_canonical(row.listing_url) for row in groups[key]
            if row.match_status == "EXACT" and row.listing_kind != "BUNDLE_SET"}
        if _canonical(packet.source_locator.value) not in locators:
            raise RetailPortfolioOnboardingError(f"baseline locator does not bind {key}: {packet.packet_id}")
        verified_baselines.append({"retailer": ref.retailer, "source_product_id": ref.source_product_id,
            "packet_id": packet.packet_id, "source_locator": packet.source_locator.value,
            "preserved_file_count": len(packet.preserved_files)})

    coverage: list[dict[str, Any]] = []
    for retailer in LADDER:
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
                if row.match_status == "EXACT":
                    for parent_id in row.owned_parent_ids:
                        observed.setdefault(parent_id, set()).update(row.material_variant_ids)
            for parent_id in covered:
                for variant in sorted(set(parents[parent_id].material_variant_ids)-observed.get(parent_id,set())):
                    residuals.append(f"MISSING_MATERIAL_VARIANT:{retailer}:{parent_id}:{variant}")
        coverage.append({"retailer": retailer, "outcome_status": outcomes[retailer].status,
            "owned_parent_denominator": len(parents), "covered_owned_parent_ids": covered,
            "covered_owned_parent_count": len(covered),
            "exact_listing_count": sum(1 for key in exact_keys if key[0] == retailer)})

    return {"schema_version": SCHEMA_VERSION,
        "certification": "coverage_composition_only; not_depth_selection; not_judgment",
        "company_id": commission.company_id,
        "owned_census_source_packet_id": commission.owned_census.source_packet_id,
        "owned_parent_count": len(parents),
        "owned_parents": [item.model_dump(mode="json") for item in sorted(
            commission.owned_census.parents, key=lambda value: value.owned_parent_id)],
        "retailer_outcomes": outcome_rows,
        "listing_reconciliations": [item.model_dump(mode="json") for item in sorted(
            commission.listing_reconciliations, key=lambda value: (value.retailer,value.grid_row_id))],
        "listing_identities": identities, "pdp_baselines": verified_baselines,
        "coverage_by_retailer": coverage, "coverage_residuals": sorted(set(residuals)),
        "non_claims": ["not a complete global SKU graph", "not sales or internal economics",
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

def _canonical(value: str) -> str:
    parsed=urlparse(value.strip())
    return urlunparse((parsed.scheme.lower(),parsed.netloc.lower(),parsed.path.rstrip("/"),"",
        urlencode(sorted(parse_qsl(parsed.query,keep_blank_values=True))),""))

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
