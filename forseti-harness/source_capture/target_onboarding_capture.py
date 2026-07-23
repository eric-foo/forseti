"""Raw-preserving Target Bazaarvoice onboarding companion capture."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

from data_lake.root import DataLakeRoot, LoadedRawPacket
from harness_utils import utc_now_z
from source_capture.adapters.bazaarvoice_api import (
    BAZAARVOICE_API_HOST,
    ApiFetcher,
    ApiRequestSpec,
    ApiResponse,
    fetch_bazaarvoice_api_response,
)
from source_capture.adapters.target_bazaarvoice import (
    ConfigFetcher,
    TargetBazaarvoiceResolution,
    resolve_target_bazaarvoice_config,
    validate_target_deployment_url,
)
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map


TARGET_ONBOARDING_SOURCE_SURFACE = "target_bazaarvoice_onboarding"
TARGET_ONBOARDING_PARSER_VERSION = "target_bazaarvoice_onboarding_v2"
DEFAULT_QUESTION_LIMIT = 100
DEFAULT_REVIEW_LIMIT = 100
_TARGET_PRODUCT_PATH = re.compile(r"^/p/(?:[^/]+/)?-/A-(?P<tcin>[0-9]+)/?$")
_DEPLOYMENT_URL = re.compile(
    r"https://apps\.bazaarvoice\.com/deployments/"
    r"targetcom/main_site/production/en_US/bv\.js"
)
_RETAILER_NATIVE_REVIEW_ENDPOINT = (
    "https://cdui-orchestrations.target.com/cdui_orchestrations/v1/pages/pdp"
)


class TargetOnboardingCaptureError(RuntimeError):
    """Fail-closed acquisition or content-qualification error."""


@dataclass(frozen=True)
class TargetParentContext:
    packet_id: str
    file_id: str
    file_sha256: str
    product_url: str
    tcin: str
    product: Mapping[str, Any]
    deployment_url: str
    retailer_native_review_endpoint: str


def capture_target_onboarding_packet(
    *,
    data_root: DataLakeRoot,
    parent_packet_id: str,
    question_limit: int = DEFAULT_QUESTION_LIMIT,
    review_limit: int = DEFAULT_REVIEW_LIMIT,
    timeout_seconds: float = 20.0,
    max_bytes: int = 8_000_000,
    config_fetcher: ConfigFetcher | None = None,
    api_fetcher: ApiFetcher | None = None,
) -> tuple[int, dict[str, Any]]:
    """Capture Target Helpful, Recent, and Q&A responses as one companion packet."""
    if data_root.readonly:
        raise TargetOnboardingCaptureError("capture requires a writable DataLakeRoot")
    if not 1 <= question_limit <= 100:
        raise ValueError("question_limit must be between 1 and 100")
    if not 1 <= review_limit <= 100:
        raise ValueError("review_limit must be between 1 and 100")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")

    parent = _parent_context(data_root.load_raw_packet(parent_packet_id), parent_packet_id)
    resolution = resolve_target_bazaarvoice_config(
        deployment_url=parent.deployment_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        fetcher=config_fetcher,
    )
    specs = _request_specs(
        tcin=parent.tcin,
        display_code=resolution.display_code,
        question_limit=question_limit,
        review_limit=review_limit,
    )
    fetch_api = api_fetcher or fetch_bazaarvoice_api_response
    captured: list[tuple[ApiRequestSpec, ApiResponse]] = []
    acquisition_failure: dict[str, Any] | None = None
    for spec in specs:
        try:
            response = fetch_api(
                spec,
                resolution.config,
                timeout_seconds,
                max_bytes,
            )
        except Exception as exc:
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "error_type": type(exc).__name__,
                "error": _safe_error_text(exc),
            }
            break
        if resolution.config.token.encode("utf-8") in response.body:
            raise TargetOnboardingCaptureError(
                f"{spec.artifact_name} echoed the public read passkey; refusing "
                "to persist credential-bearing response bytes"
            )
        captured.append((spec, response))
        if not 200 <= response.status < 300:
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "http_status": response.status,
                "reason": response.reason,
            }
            break

    request_manifest = _request_manifest(parent, resolution, specs, captured)
    artifacts: list[tuple[str, bytes]] = [
        (spec.artifact_name, response.body) for spec, response in captured
    ]
    artifacts.append(("target_request_manifest.json", _json_bytes(request_manifest)))

    exit_code = 0
    limitations: list[str] = []
    if acquisition_failure is not None:
        exit_code = 4
        limitations.append(
            "structured API acquisition did not complete; every response acquired "
            "before failure is preserved and no successful summary is claimed"
        )
        summary: dict[str, Any] = {
            "record_kind": "target_bazaarvoice_onboarding_capture_failure_v1",
            "parser_version": TARGET_ONBOARDING_PARSER_VERSION,
            "provider": "bazaarvoice",
            "parent_packet_id": parent.packet_id,
            "target_tcin": parent.tcin,
            "failure": acquisition_failure,
            "raw_failure_fallback": {
                "status": "preserved_partial_responses",
                "preserved_response_count": len(captured),
                "expected_response_count": len(specs),
            },
        }
        artifacts.append(("target_capture_failure.json", _json_bytes(summary)))
    else:
        try:
            summary = build_target_onboarding_summary(
                parent=parent,
                resolution=resolution,
                captured_responses=captured,
            )
            limitations.extend(entry["detail"] for entry in summary["loss_ledger"])
            artifacts.append(("target_onboarding_summary.json", _json_bytes(summary)))
        except Exception as exc:
            exit_code = 5
            limitations.append(
                "Target onboarding adaptation failed after acquisition; every exact "
                "Bazaarvoice response is preserved as the required raw fallback"
            )
            summary = {
                "record_kind": "target_bazaarvoice_onboarding_adaptation_failure_v1",
                "parser_version": TARGET_ONBOARDING_PARSER_VERSION,
                "provider": "bazaarvoice",
                "parent_packet_id": parent.packet_id,
                "target_tcin": parent.tcin,
                "failure": {
                    "error_type": type(exc).__name__,
                    "error": _safe_error_text(exc),
                },
                "raw_failure_fallback": {
                    "status": "all_responses_preserved",
                    "preserved_response_count": len(captured),
                    "expected_response_count": len(specs),
                },
            }
            artifacts.append(("target_adaptation_failure.json", _json_bytes(summary)))

    written = _write_packet(
        data_root=data_root,
        parent=parent,
        artifacts=artifacts,
        captured=captured,
        limitations=limitations,
        summary=summary,
    )
    return exit_code, {
        "packet_id": written.packet.packet_id,
        "output_directory": str(written.output_directory),
        "summary": summary,
    }


def build_target_onboarding_summary(
    *,
    parent: TargetParentContext,
    resolution: TargetBazaarvoiceResolution,
    captured_responses: Sequence[tuple[ApiRequestSpec, ApiResponse]],
) -> dict[str, Any]:
    by_name = {
        spec.artifact_name: (spec, response)
        for spec, response in captured_responses
    }
    expected = {
        "questions_most_answers_offset_000.json",
        "reviews_most_helpful_offset_000.json",
        "reviews_most_recent_offset_000.json",
    }
    if set(by_name) != expected:
        raise TargetOnboardingCaptureError(
            "Target summary requires exactly one Helpful, Recent, and Q&A response"
        )

    question_name = "questions_most_answers_offset_000.json"
    helpful_name = "reviews_most_helpful_offset_000.json"
    recent_name = "reviews_most_recent_offset_000.json"
    questions = _load_document(by_name[question_name][1].body, question_name)
    helpful = _load_document(by_name[helpful_name][1].body, helpful_name)
    recent = _load_document(by_name[recent_name][1].body, recent_name)
    question_rows = _result_rows(questions, question_name, parent.tcin)
    helpful_rows = _result_rows(helpful, helpful_name, parent.tcin)
    recent_rows = _result_rows(recent, recent_name, parent.tcin)
    _require_descending(
        question_rows,
        "TotalAnswerCount",
        question_name,
    )
    _require_descending(
        helpful_rows,
        "TotalPositiveFeedbackCount",
        helpful_name,
    )
    _require_time_descending(recent_rows, recent_name)
    _require_unique_ids(question_rows, question_name)
    _require_unique_ids(helpful_rows, helpful_name)
    _require_unique_ids(recent_rows, recent_name)

    declared_answer_ids = [
        str(answer_id)
        for row in question_rows
        for answer_id in _list_value(row.get("AnswerIds"))
    ]
    question_includes = questions.get("Includes")
    if not isinstance(question_includes, Mapping):
        raise TargetOnboardingCaptureError(
            f"{question_name}.Includes.Answers must be an object"
        )
    answer_values = question_includes.get("Answers")
    if "Answers" not in question_includes:
        answers: Mapping[str, Any] = {}
    elif isinstance(answer_values, Mapping):
        answers = answer_values
    else:
        raise TargetOnboardingCaptureError(
            f"{question_name}.Includes.Answers must be an object"
        )
    missing_answer_ids = sorted(set(declared_answer_ids) - set(answers))
    if missing_answer_ids:
        raise TargetOnboardingCaptureError(
            f"{question_name} omitted declared answer IDs: {missing_answer_ids[:5]}"
        )
    product = _included_mapping(helpful, "Products", helpful_name).get(parent.tcin)
    if not isinstance(product, Mapping):
        raise TargetOnboardingCaptureError(
            f"{helpful_name} does not include ProductId {parent.tcin}"
        )
    statistics = product.get("ReviewStatistics")
    filtered_statistics = product.get("FilteredReviewStatistics")
    if not isinstance(statistics, Mapping) or not isinstance(
        filtered_statistics, Mapping
    ):
        raise TargetOnboardingCaptureError(
            f"{helpful_name} is missing review aggregate statistics"
        )

    answer_rows = [
        value for value in answers.values() if isinstance(value, Mapping)
    ]
    context_dimensions = sorted(
        {
            str(key)
            for row in (*helpful_rows, *recent_rows)
            for key in _mapping_value(row.get("ContextDataValues"))
        }
    )
    badge_ids = sorted(
        {
            str(key)
            for row in (*helpful_rows, *recent_rows)
            for key in _mapping_value(row.get("Badges"))
        }
    )
    source_clients = sorted(
        {
            str(row["SourceClient"])
            for row in (*helpful_rows, *recent_rows)
            if row.get("SourceClient") is not None
        }
    )
    summary: dict[str, Any] = {
        "record_kind": "target_bazaarvoice_onboarding_summary_v1",
        "parser_version": TARGET_ONBOARDING_PARSER_VERSION,
        "provider": "bazaarvoice",
        "retailer": "Target",
        "parent_packet": {
            "packet_id": parent.packet_id,
            "file_id": parent.file_id,
            "file_sha256": parent.file_sha256,
            "product_url": parent.product_url,
            "raw_file_reference": f"{parent.packet_id}:{parent.file_id}",
        },
        "identity": {
            "target_tcin": parent.tcin,
            "bazaarvoice_product_id": str(product.get("Id")),
            "mapping_equal": str(product.get("Id")) == parent.tcin,
            "deployment": resolution.deployment,
            "display_code": resolution.display_code,
            "api_version": resolution.config.version,
        },
        "configuration": {
            "deployment_url": resolution.deployment_url,
            "legacy_config_url": resolution.legacy_config_url,
            "public_config_receipts": [
                receipt.as_dict() for receipt in resolution.config_receipts
            ],
            "credential_posture": (
                "page-declared public read passkey used only in flight; passkey and "
                "credential-bearing request URLs are not persisted"
            ),
        },
        "product": {
            "target_parent_source_fields": sorted(parent.product),
            "target_parent_raw_file_reference": f"{parent.packet_id}:{parent.file_id}",
            "bazaarvoice_source_fields": sorted(product),
            "id": str(product.get("Id")),
            "name": product.get("Name"),
            "brand": product.get("Brand"),
            "brand_external_id": product.get("BrandExternalId"),
            "category_id": product.get("CategoryId"),
            "family_ids": product.get("FamilyIds"),
            "upcs": product.get("UPCs"),
            "product_page_url": product.get("ProductPageUrl"),
        },
        "questions": {
            "total_questions": _nonnegative_int(
                questions.get("TotalResults"),
                f"{question_name}.TotalResults",
            ),
            "captured_question_rows": len(question_rows),
            "declared_answer_rows": len(declared_answer_ids),
            "captured_included_answer_rows": len(answer_rows),
            "question_source_fields": _field_inventory(question_rows),
            "answer_source_fields": _field_inventory(answer_rows),
            "question_inventory": [
                _question_row_summary(row, question_name, rank)
                for rank, row in enumerate(question_rows, start=1)
            ],
            "answer_inventory": [
                _answer_row_summary(row, question_name)
                for row in sorted(answer_rows, key=lambda item: str(item.get("Id")))
            ],
            "raw_file": question_name,
        },
        "reviews": {
            "most_helpful": _review_view_summary(
                helpful,
                helpful_rows,
                helpful_name,
                role="most_helpful",
            ),
            "most_recent": _review_view_summary(
                recent,
                recent_rows,
                recent_name,
                role="most_recent",
            ),
            "last_seen_review_id": (
                str(recent_rows[0].get("Id")) if recent_rows else None
            ),
            "review_statistics": statistics,
            "filtered_review_statistics": filtered_statistics,
            "context_dimension_keys": context_dimensions,
            "badge_ids": badge_ids,
            "source_clients": source_clients,
        },
        "retailer_native_observation": {
            "provider": "Target",
            "endpoint": parent.retailer_native_review_endpoint,
            "status": "embedded_response_observed",
            "roles_observed": [
                "most_recent_review_bodies",
                "review_statistics",
                "review_media_references",
            ],
            "provenance_note": (
                "This Target-owned endpoint is not labelled or counted as Bazaarvoice."
            ),
        },
        "extraction_target_matrix": [
            {
                "information_class": "product_identity_variant_offer_claims_and_media",
                "status": "present_in_parent_embedded_page_state",
                "raw_reference": f"{parent.packet_id}:{parent.file_id}",
            },
            {
                "information_class": "most_helpful_reviews",
                "status": "present_in_bazaarvoice",
                "raw_reference": helpful_name,
            },
            {
                "information_class": "most_recent_reviews_and_anchor",
                "status": "present_in_bazaarvoice",
                "raw_reference": recent_name,
            },
            {
                "information_class": "review_aggregates",
                "status": "present_in_bazaarvoice",
                "raw_reference": helpful_name,
            },
            {
                "information_class": "age_skin_type_skin_concern_distributions",
                "status": "missing_from_observed_target_bazaarvoice_response",
                "raw_reference": helpful_name,
            },
            {
                "information_class": "source_proven_non_incentivized_filter",
                "status": "missing",
                "raw_reference": helpful_name,
            },
            {
                "information_class": "answer_rich_qa",
                "status": (
                    "present_in_bazaarvoice"
                    if question_rows and answer_rows
                    else "missing_from_observed_target_bazaarvoice_response"
                ),
                "raw_reference": question_name,
            },
        ],
        "row_accounting": {
            "question_rows_equal": len(question_rows)
            == len(_result_list(questions, question_name)),
            "answers_equal": len(declared_answer_ids) == len(answer_rows),
            "helpful_rows_equal": len(helpful_rows)
            == len(_result_list(helpful, helpful_name)),
            "recent_rows_equal": len(recent_rows)
            == len(_result_list(recent, recent_name)),
        },
        "loss_ledger": [
            {
                "category": "incentive_semantics",
                "detail": (
                    "Target exposed no source-proven non-incentivized filter or "
                    "incentive marker in the bounded response; no incentive claim is made."
                ),
            },
            {
                "category": "demographics",
                "detail": (
                    "Target returned no age, skin-type, or skin-concern context "
                    "distribution in the bounded Helpful response."
                ),
            },
            {
                "category": "bounded_window",
                "detail": (
                    "Helpful and Recent preserve one bounded response each; this is "
                    "not the complete historical review corpus."
                ),
            },
            {
                "category": "linked_media",
                "detail": (
                    "Review photo/video references are preserved in raw responses; "
                    "linked media bytes were not fetched."
                ),
            },
            {
                "category": "audience",
                "detail": (
                    "Reviewer attributes and recommendations are source observations, "
                    "not a representative population estimate."
                ),
            },
        ],
        "content_qualification": {
            "status": "passed",
            "provider_identity": "bazaarvoice",
            "product_mapping_bound": str(product.get("Id")) == parent.tcin,
            "three_response_roles_present": True,
            "all_declared_answers_preserved": len(declared_answer_ids)
            == len(answer_rows),
            "exact_raw_response_bytes_preserved": True,
            "summary_duplicates_review_or_answer_bodies": False,
        },
    }
    if not summary["identity"]["mapping_equal"]:
        raise TargetOnboardingCaptureError(
            "Target TCIN does not equal the included Bazaarvoice ProductId"
        )
    return summary


def _parent_context(loaded: LoadedRawPacket, packet_id: str) -> TargetParentContext:
    manifest = loaded.manifest
    if manifest.get("source_family") != "retail_pdp":
        raise TargetOnboardingCaptureError(
            f"parent packet {packet_id} is not source_family=retail_pdp"
        )
    locator = manifest.get("source_locator")
    product_url = (
        str(locator.get("value"))
        if isinstance(locator, Mapping) and locator.get("status") == "known"
        else ""
    )
    tcin_from_url = _target_tcin_from_url(product_url)
    candidates: list[tuple[str, bytes]] = []
    for file_id, body in loaded.bodies.items():
        if b'id="__NEXT_DATA__"' in body and b"targetcom/main_site/production" in body:
            candidates.append((file_id, body))
    if len(candidates) != 1:
        raise TargetOnboardingCaptureError(
            f"parent packet {packet_id} requires exactly one Target rendered DOM "
            "with __NEXT_DATA__ and public Bazaarvoice deployment"
        )
    file_id, body = candidates[0]
    text = body.decode("utf-8", errors="strict")
    next_data = _next_data(text)
    product = _target_product(next_data)
    tcin = _required_text(product.get("tcin"), "Target product.tcin")
    if tcin != tcin_from_url:
        raise TargetOnboardingCaptureError(
            f"parent product mismatch: URL={tcin_from_url}, embedded={tcin}"
        )
    deployment_urls = set(_DEPLOYMENT_URL.findall(text))
    if len(deployment_urls) != 1:
        raise TargetOnboardingCaptureError(
            "Target parent must expose exactly one admitted Bazaarvoice deployment"
        )
    deployment_url = validate_target_deployment_url(next(iter(deployment_urls)))
    native_endpoint = _target_native_review_endpoint(next_data)
    preserved = next(
        (
            item
            for item in manifest.get("preserved_files", [])
            if isinstance(item, Mapping) and item.get("file_id") == file_id
        ),
        None,
    )
    if not isinstance(preserved, Mapping) or not isinstance(
        preserved.get("sha256"), str
    ):
        raise TargetOnboardingCaptureError("parent DOM preserved-file hash is unavailable")
    return TargetParentContext(
        packet_id=packet_id,
        file_id=file_id,
        file_sha256=str(preserved["sha256"]),
        product_url=product_url,
        tcin=tcin,
        product=product,
        deployment_url=deployment_url,
        retailer_native_review_endpoint=native_endpoint,
    )


def _target_tcin_from_url(url: str) -> str:
    parsed = urlparse(url)
    match = _TARGET_PRODUCT_PATH.fullmatch(parsed.path)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "www.target.com"
        or match is None
    ):
        raise TargetOnboardingCaptureError(
            "Target parent URL must be HTTPS www.target.com /p/.../-/A-<tcin>"
        )
    return match.group("tcin")


def _next_data(html: str) -> Mapping[str, Any]:
    matches = re.findall(
        r'<script\b[^>]*\bid=["\']__NEXT_DATA__["\'][^>]*>([\s\S]*?)</script\s*>',
        html,
        flags=re.IGNORECASE,
    )
    if len(matches) != 1:
        raise TargetOnboardingCaptureError(
            "Target parent requires exactly one __NEXT_DATA__ document"
        )
    try:
        value = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise TargetOnboardingCaptureError("Target __NEXT_DATA__ is malformed") from exc
    if not isinstance(value, Mapping):
        raise TargetOnboardingCaptureError("Target __NEXT_DATA__ must be an object")
    return value


def _target_query_data(
    next_data: Mapping[str, Any],
) -> tuple[Mapping[str, Any], ...]:
    props = next_data.get("props")
    dehydrated_state = (
        props.get("dehydratedState") if isinstance(props, Mapping) else None
    )
    queries = (
        dehydrated_state.get("queries")
        if isinstance(dehydrated_state, Mapping)
        else None
    )
    if not isinstance(queries, list):
        return ()

    query_data: list[Mapping[str, Any]] = []
    for query in queries:
        if not isinstance(query, Mapping):
            continue
        state = query.get("state")
        data = state.get("data") if isinstance(state, Mapping) else None
        if isinstance(data, Mapping):
            query_data.append(data)
    return tuple(query_data)


def _target_product(next_data: Mapping[str, Any]) -> Mapping[str, Any]:
    products: list[Mapping[str, Any]] = []
    for data in _target_query_data(next_data):
        payload = data.get("data")
        modules = (
            payload.get("data_source_modules")
            if isinstance(payload, Mapping)
            else None
        )
        if not isinstance(modules, list):
            continue
        for module in modules:
            if (
                isinstance(module, Mapping)
                and module.get("module_type")
                == "ProductDetailWebDatasourceCore"
            ):
                module_data = module.get("module_data")
                module_payload = (
                    module_data.get("data")
                    if isinstance(module_data, Mapping)
                    else None
                )
                product = (
                    module_payload.get("product")
                    if isinstance(module_payload, Mapping)
                    else None
                )
                if isinstance(product, Mapping):
                    products.append(product)
    if len(products) != 1:
        raise TargetOnboardingCaptureError(
            "Target parent requires exactly one ProductDetailWebDatasourceCore product"
        )
    return products[0]


def _target_native_review_endpoint(next_data: Mapping[str, Any]) -> str:
    endpoints: set[str] = set()
    for data in _target_query_data(next_data):
        metadata = data.get("metadata")
        url = metadata.get("url") if isinstance(metadata, Mapping) else None
        if not isinstance(url, str):
            continue
        parsed = urlparse(url)
        endpoint = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if endpoint == _RETAILER_NATIVE_REVIEW_ENDPOINT:
            endpoints.add(endpoint)
    if endpoints != {_RETAILER_NATIVE_REVIEW_ENDPOINT}:
        raise TargetOnboardingCaptureError(
            "Target parent did not expose the admitted retailer-owned review endpoint"
        )
    return next(iter(endpoints))


def _request_specs(
    *,
    tcin: str,
    display_code: str,
    question_limit: int,
    review_limit: int,
) -> tuple[ApiRequestSpec, ...]:
    locale_filters = (
        ("Filter", f"ProductId:eq:{tcin}"),
        ("Filter", "ContentLocale:eq:en*,en_US"),
    )
    review_common = (
        ("displaycode", display_code),
        ("Filter", "IsRatingsOnly:eq:false"),
        *locale_filters,
    )
    return (
        ApiRequestSpec(
            artifact_name="questions_most_answers_offset_000.json",
            endpoint="questions.json",
            config_kind="questions",
            parameters=(
                ("displaycode", display_code),
                *locale_filters,
                ("Sort", "TotalAnswerCount:desc"),
                ("Stats", "Questions"),
                ("FilteredStats", "Questions"),
                ("Include", "Authors,Products,Answers"),
                ("Filter_Questions", "ContentLocale:eq:en*,en_US"),
                ("Filter_Answers", "ContentLocale:eq:en*,en_US"),
                ("Limit", str(question_limit)),
                ("Offset", "0"),
                ("Limit_Answers", "20"),
            ),
        ),
        ApiRequestSpec(
            artifact_name="reviews_most_helpful_offset_000.json",
            endpoint="reviews.json",
            config_kind="reviews",
            parameters=(
                *review_common,
                ("Sort", "TotalPositiveFeedbackCount:desc"),
                ("Stats", "Reviews"),
                ("FilteredStats", "Reviews"),
                ("Include", "Authors,Products,Comments"),
                ("Filter_Reviews", "ContentLocale:eq:en*,en_US"),
                ("Filter_ReviewComments", "ContentLocale:eq:en*,en_US"),
                ("Limit", str(review_limit)),
                ("Offset", "0"),
                ("Limit_Comments", "3"),
            ),
        ),
        ApiRequestSpec(
            artifact_name="reviews_most_recent_offset_000.json",
            endpoint="reviews.json",
            config_kind="reviews",
            parameters=(
                *review_common,
                ("Sort", "SubmissionTime:desc"),
                ("Include", "Authors,Comments"),
                ("Filter_Reviews", "ContentLocale:eq:en*,en_US"),
                ("Filter_ReviewComments", "ContentLocale:eq:en*,en_US"),
                ("Limit", str(review_limit)),
                ("Offset", "0"),
                ("Limit_Comments", "3"),
            ),
        ),
    )


def _request_manifest(
    parent: TargetParentContext,
    resolution: TargetBazaarvoiceResolution,
    specs: Sequence[ApiRequestSpec],
    captured: Sequence[tuple[ApiRequestSpec, ApiResponse]],
) -> dict[str, Any]:
    response_by_name = {spec.artifact_name: response for spec, response in captured}
    return {
        "record_kind": "target_bazaarvoice_request_manifest_v1",
        "provider": "bazaarvoice",
        "retailer": "Target",
        "parent_packet_id": parent.packet_id,
        "parent_file_id": parent.file_id,
        "parent_file_sha256": parent.file_sha256,
        "product_url": parent.product_url,
        "target_tcin": parent.tcin,
        "bazaarvoice_product_id": parent.tcin,
        "deployment": resolution.deployment,
        "display_code": resolution.display_code,
        "public_config_receipts": [
            receipt.as_dict() for receipt in resolution.config_receipts
        ],
        "credential_posture": (
            "page-declared public read passkey used in flight; passkey and "
            "credential-bearing request URLs are not persisted"
        ),
        "requests": [
            {
                "artifact_name": spec.artifact_name,
                "endpoint": f"https://{BAZAARVOICE_API_HOST}/data/{spec.endpoint}",
                "api_version": resolution.config.version,
                "parameters": [
                    {"name": name, "value": value} for name, value in spec.parameters
                ],
                "response": (
                    {
                        "status": response_by_name[spec.artifact_name].status,
                        "reason": response_by_name[spec.artifact_name].reason or None,
                        "content_type": response_by_name[
                            spec.artifact_name
                        ].content_type,
                        "byte_count": len(response_by_name[spec.artifact_name].body),
                        "captured_at": response_by_name[
                            spec.artifact_name
                        ].captured_at,
                    }
                    if spec.artifact_name in response_by_name
                    else None
                ),
            }
            for spec in specs
        ],
    }


def _write_packet(
    *,
    data_root: DataLakeRoot,
    parent: TargetParentContext,
    artifacts: Sequence[tuple[str, bytes]],
    captured: Sequence[tuple[ApiRequestSpec, ApiResponse]],
    limitations: Sequence[str],
    summary: Mapping[str, Any],
):
    file_ids = staged_file_id_map(artifacts)
    captured_at = captured[-1][1].captured_at if captured else utc_now_z()
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "Bazaarvoice responses do not declare one source publication time"
        ),
        source_edit_or_version=unknown_with_reason(
            "Bazaarvoice responses do not declare a product-level edit version"
        ),
        capture_time=known_fact(captured_at),
        recapture_time=known_fact(captured_at),
        cutoff_posture=known_fact("post_cutoff"),
    )
    access = known_fact(
        "Target page-declared public Bazaarvoice API attempted; exact acquired "
        "response bytes preserved"
    )
    archive = not_attempted("structured companion did not query archive/history")
    media = not_attempted("structured companion did not fetch linked review media")
    recapture = known_fact("supplement")
    return stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="target_bazaarvoice_review_qa_onboarding",
                locator=known_fact(parent.product_url),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                locale_pin=known_fact("US"),
                currency_pin=known_fact("USD"),
                limitations=list(limitations),
                warning_notes=[],
                preserved_file_ids=[file_ids[name] for name, _ in artifacts],
            )
        ],
        source_family="retail_pdp",
        source_surface=TARGET_ONBOARDING_SOURCE_SURFACE,
        source_locator=known_fact(parent.product_url),
        decision_question=(
            "What does Target expose through one bounded Bazaarvoice Most Helpful "
            "response with aggregates, one Most Recent response, and one answer-rich "
            "Q&A response, and which Sephora target fields remain absent?"
        ),
        capture_context=(
            f"Target-specific structured companion from hash-verified parent packet "
            f"{parent.packet_id}; parser={TARGET_ONBOARDING_PARSER_VERSION}"
        ),
        actor_audience_context=unknown_with_reason(
            "reviewer attributes are source-visible observations; audience "
            "representativeness is not established"
        ),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="target_bazaarvoice_onboarding_cli_operator",
        session_identity=None,
        visible_mode_changes=[
            "target_public_bazaarvoice_config_resolved",
            "target_tcin_bound_to_bazaarvoice_product_id",
            "questions_sort_total_answer_count_desc",
            "reviews_sort_total_positive_feedback_count_desc",
            "reviews_sort_submission_time_desc",
            "token_free_request_manifest",
        ],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=list(limitations),
        receipt_summary=(
            f"Target Bazaarvoice onboarding companion for TCIN {parent.tcin}: "
            f"{summary.get('record_kind', 'unknown result')}; exact API response "
            "bytes and a token-free request manifest are preserved."
        ),
        receipt_non_claims=[
            "not a retailer-native endpoint",
            "not a complete review corpus",
            "not a non-incentivized review population",
            "not reviewer population representativeness",
            "not linked-media preservation",
            "not review or answer body normalization or Judgment",
            "not a replacement for the parent rendered Target PDP packet",
        ],
    )


def _load_document(body: bytes, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TargetOnboardingCaptureError(f"{label} is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise TargetOnboardingCaptureError(f"{label} must be a JSON object")
    if value.get("HasErrors") is not False:
        raise TargetOnboardingCaptureError(f"{label} reports Bazaarvoice errors")
    return value


def _result_list(document: Mapping[str, Any], label: str) -> list[Any]:
    rows = document.get("Results")
    if not isinstance(rows, list):
        raise TargetOnboardingCaptureError(f"{label}.Results must be an array")
    return rows


def _result_rows(
    document: Mapping[str, Any],
    label: str,
    product_id: str,
) -> list[Mapping[str, Any]]:
    rows = _result_list(document, label)
    if not all(isinstance(row, Mapping) for row in rows):
        raise TargetOnboardingCaptureError(f"{label}.Results contains a non-object row")
    typed = [row for row in rows if isinstance(row, Mapping)]
    mismatches = sorted(
        {
            str(row.get("ProductId"))
            for row in typed
            if str(row.get("ProductId")) != product_id
        }
    )
    if mismatches:
        raise TargetOnboardingCaptureError(
            f"{label} contains foreign ProductId values: {mismatches}"
        )
    return typed


def _included_mapping(
    document: Mapping[str, Any],
    name: str,
    label: str,
) -> Mapping[str, Any]:
    includes = document.get("Includes")
    value = includes.get(name) if isinstance(includes, Mapping) else None
    if not isinstance(value, Mapping):
        raise TargetOnboardingCaptureError(f"{label}.Includes.{name} must be an object")
    return value


def _require_descending(
    rows: Sequence[Mapping[str, Any]],
    field: str,
    label: str,
) -> None:
    values = [_nonnegative_int(row.get(field), f"{label}.{field}") for row in rows]
    if values != sorted(values, reverse=True):
        raise TargetOnboardingCaptureError(f"{label} is not ordered by {field} desc")


def _require_time_descending(
    rows: Sequence[Mapping[str, Any]],
    label: str,
) -> None:
    values = [
        _parse_time(_required_text(row.get("SubmissionTime"), f"{label}.SubmissionTime"))
        for row in rows
    ]
    if values != sorted(values, reverse=True):
        raise TargetOnboardingCaptureError(
            f"{label} is not ordered by SubmissionTime desc"
        )


def _require_unique_ids(rows: Sequence[Mapping[str, Any]], label: str) -> None:
    ids = [_required_text(row.get("Id"), f"{label}.Id") for row in rows]
    if len(ids) != len(set(ids)):
        raise TargetOnboardingCaptureError(f"{label} contains duplicate row IDs")


def _review_view_summary(
    document: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    raw_file: str,
    *,
    role: str,
) -> dict[str, Any]:
    return {
        "role": role,
        "total_results": _nonnegative_int(
            document.get("TotalResults"),
            f"{raw_file}.TotalResults",
        ),
        "captured_review_rows": len(rows),
        "captured_review_bodies": sum(bool(row.get("ReviewText")) for row in rows),
        "source_fields": _field_inventory(rows),
        "review_inventory": [
            _review_row_summary(row, raw_file, rank)
            for rank, row in enumerate(rows, start=1)
        ],
        "raw_file": raw_file,
    }


def _review_row_summary(
    row: Mapping[str, Any],
    raw_file: str,
    rank: int,
) -> dict[str, Any]:
    return {
        "rank": rank,
        "review_id": _required_text(row.get("Id"), f"{raw_file}.Id"),
        "product_id": _required_text(row.get("ProductId"), f"{raw_file}.ProductId"),
        "submission_time": row.get("SubmissionTime"),
        "rating": row.get("Rating"),
        "title_present": bool(row.get("Title")),
        "body_present": bool(row.get("ReviewText")),
        "nickname_present": bool(row.get("UserNickname")),
        "is_recommended": row.get("IsRecommended"),
        "is_syndicated": row.get("IsSyndicated"),
        "source_client": row.get("SourceClient"),
        "syndication_source": row.get("SyndicationSource"),
        "badge_ids": sorted(_mapping_value(row.get("Badges"))),
        "context_dimension_keys": sorted(
            _mapping_value(row.get("ContextDataValues"))
        ),
        "positive_feedback_count": row.get("TotalPositiveFeedbackCount"),
        "negative_feedback_count": row.get("TotalNegativeFeedbackCount"),
        "photo_count": len(_list_value(row.get("Photos"))),
        "video_count": len(_list_value(row.get("Videos"))),
        "client_response_count": row.get("TotalClientResponseCount"),
        "raw_file": raw_file,
    }


def _question_row_summary(
    row: Mapping[str, Any],
    raw_file: str,
    rank: int,
) -> dict[str, Any]:
    return {
        "rank": rank,
        "question_id": _required_text(row.get("Id"), f"{raw_file}.Id"),
        "product_id": _required_text(row.get("ProductId"), f"{raw_file}.ProductId"),
        "submission_time": row.get("SubmissionTime"),
        "summary_present": bool(row.get("QuestionSummary")),
        "details_present": bool(row.get("QuestionDetails")),
        "declared_answer_count": row.get("TotalAnswerCount"),
        "answer_ids": [str(value) for value in _list_value(row.get("AnswerIds"))],
        "raw_file": raw_file,
    }


def _answer_row_summary(row: Mapping[str, Any], raw_file: str) -> dict[str, Any]:
    return {
        "answer_id": _required_text(row.get("Id"), f"{raw_file}.Answer.Id"),
        "question_id": row.get("QuestionId"),
        "submission_time": row.get("SubmissionTime"),
        "body_present": bool(row.get("AnswerText")),
        "is_best_answer": row.get("IsBestAnswer"),
        "is_brand_answer": row.get("IsBrandAnswer"),
        "raw_file": raw_file,
    }


def _field_inventory(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    return sorted({str(key) for row in rows for key in row})


def _mapping_value(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TargetOnboardingCaptureError(f"{label} must be a nonnegative integer")
    return value


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise TargetOnboardingCaptureError(f"{label} must be nonempty text")
    text = str(value).strip()
    if not text:
        raise TargetOnboardingCaptureError(f"{label} must be nonempty text")
    return text


def _parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TargetOnboardingCaptureError(
            f"invalid Bazaarvoice timestamp: {value}"
        ) from exc


def _safe_error_text(exc: Exception) -> str:
    text = str(exc)
    return re.sub(
        r"(?i)(passkey|token|api[_-]?key)=([^&\s]+)",
        r"\1=[REDACTED]",
        text,
    )[:500]


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


__all__ = [
    "ApiRequestSpec",
    "ApiResponse",
    "DEFAULT_QUESTION_LIMIT",
    "DEFAULT_REVIEW_LIMIT",
    "TARGET_ONBOARDING_PARSER_VERSION",
    "TARGET_ONBOARDING_SOURCE_SURFACE",
    "TargetOnboardingCaptureError",
    "TargetParentContext",
    "build_target_onboarding_summary",
    "capture_target_onboarding_packet",
]
