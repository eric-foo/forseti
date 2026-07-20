"""Raw-preserving Sephora Bazaarvoice companion capture.

This module is intentionally retailer-specific.  It consumes a hash-verified
rendered Sephora PDP packet, reads the API configuration declared by that page,
and captures a bounded ``Most Answers`` Q&A window plus exact
non-incentivized-review age counts.  Network access stays in this acquisition
seam; the packet summary is derived in flight from preserved response bytes.
"""

from __future__ import annotations

import html as html_lib
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from urllib.parse import unquote

from data_lake.root import DataLakeRoot, LoadedRawPacket
from harness_utils import utc_now_z
from source_capture.adapters.sephora_bazaarvoice import (
    BAZAARVOICE_API_HOST,
    ApiFetcher,
    ApiRequestSpec,
    ApiResponse,
    BazaarvoiceReadConfig,
    fetch_bazaarvoice_api_response,
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


SEPHORA_ONBOARDING_SOURCE_SURFACE = "sephora_bazaarvoice_onboarding"
SEPHORA_ONBOARDING_PARSER_VERSION = "sephora_bazaarvoice_onboarding_v1"
SEPHORA_AGE_BUCKETS: tuple[str, ...] = ("20s", "30s", "40s", "50s +")
DEFAULT_QUESTION_LIMIT = 100


class SephoraOnboardingCaptureError(RuntimeError):
    """Fail-closed acquisition or content-qualification error."""


@dataclass(frozen=True)
class AgeBucketSpec:
    display_label: str
    api_value: str


_AGE_BUCKET_SPECS: tuple[AgeBucketSpec, ...] = (
    AgeBucketSpec("20s", "20s"),
    AgeBucketSpec("30s", "30s"),
    AgeBucketSpec("40s", "40s"),
    AgeBucketSpec("50s +", "50s"),
)


@dataclass(frozen=True)
class ParentContext:
    packet_id: str
    file_id: str
    file_sha256: str
    product_id: str
    allowed_product_ids: tuple[str, ...]
    product_url: str
    review_config: BazaarvoiceReadConfig
    question_config: BazaarvoiceReadConfig


def capture_sephora_onboarding_packet(
    *,
    data_root: DataLakeRoot,
    parent_packet_id: str,
    question_limit: int = DEFAULT_QUESTION_LIMIT,
    timeout_seconds: float = 20.0,
    max_bytes: int = 8_000_000,
    fetcher: ApiFetcher | None = None,
) -> tuple[int, dict[str, Any]]:
    """Capture and commit one Sephora review/Q&A companion packet.

    Exit 0 is a content-qualification success. Exit 4 means one or more HTTP responses
    were non-2xx. Exit 5 means raw responses were acquired but summary adaptation failed;
    those raw bytes are still committed with an explicit failure artifact.
    Pre-acquisition parent/config failures raise and write nothing.
    """
    if data_root.readonly:
        raise SephoraOnboardingCaptureError("capture requires a writable DataLakeRoot")
    if not 1 <= question_limit <= 100:
        raise ValueError("question_limit must be between 1 and 100")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")

    parent = _parent_context(data_root.load_raw_packet(parent_packet_id), parent_packet_id)
    request_specs = _request_specs(parent.product_id, question_limit)
    api_fetcher = fetcher or fetch_bazaarvoice_api_response
    captured: list[tuple[ApiRequestSpec, ApiResponse]] = []
    acquisition_failure: dict[str, Any] | None = None

    for spec in request_specs:
        config = parent.question_config if spec.config_kind == "questions" else parent.review_config
        try:
            response = api_fetcher(spec, config, timeout_seconds, max_bytes)
        except Exception as exc:  # acquisition failure must be recorded without secret URLs
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "error_type": type(exc).__name__,
                "error": _safe_error_text(exc),
            }
            break
        if config.token.encode("utf-8") in response.body:
            raise SephoraOnboardingCaptureError(
                f"{spec.artifact_name} response echoed the page-declared read token; "
                "refusing to persist secret-bearing bytes"
            )
        captured.append((spec, response))
        if not 200 <= response.status < 300:
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "http_status": response.status,
                "reason": response.reason,
            }
            break

    request_manifest = _request_manifest(parent, request_specs, captured)
    artifacts: list[tuple[str, bytes]] = [
        (spec.artifact_name, response.body) for spec, response in captured
    ]
    artifacts.append(
        (
            "sephora_request_manifest.json",
            _json_bytes(request_manifest),
        )
    )

    limitations: list[str] = []
    exit_code = 0
    if acquisition_failure is not None:
        exit_code = 4
        limitations.append(
            "structured API acquisition did not complete; every response body acquired "
            "before the failure is preserved and no successful summary is claimed"
        )
        summary: dict[str, Any] = {
            "record_kind": "sephora_bazaarvoice_onboarding_capture_failure_v1",
            "parser_version": SEPHORA_ONBOARDING_PARSER_VERSION,
            "parent_packet_id": parent.packet_id,
            "product_id": parent.product_id,
            "failure": acquisition_failure,
            "raw_failure_fallback": {
                "status": "preserved_partial_responses",
                "preserved_response_count": len(captured),
                "expected_response_count": len(request_specs),
            },
        }
        artifacts.append(("sephora_capture_failure.json", _json_bytes(summary)))
    else:
        try:
            summary = build_sephora_onboarding_summary(
                parent=parent,
                captured_responses=captured,
                question_limit=question_limit,
            )
            limitations.extend(entry["detail"] for entry in summary["loss_ledger"])
            artifacts.append(("sephora_onboarding_summary.json", _json_bytes(summary)))
        except Exception as exc:
            exit_code = 5
            limitations.append(
                "onboarding summary adaptation failed after acquisition; all exact raw API "
                "response bytes are preserved as the required raw fallback"
            )
            summary = {
                "record_kind": "sephora_bazaarvoice_onboarding_adaptation_failure_v1",
                "parser_version": SEPHORA_ONBOARDING_PARSER_VERSION,
                "parent_packet_id": parent.packet_id,
                "product_id": parent.product_id,
                "failure": {
                    "error_type": type(exc).__name__,
                    "error": _safe_error_text(exc),
                },
                "raw_failure_fallback": {
                    "status": "all_responses_preserved",
                    "preserved_response_count": len(captured),
                    "expected_response_count": len(request_specs),
                },
            }
            artifacts.append(("sephora_adaptation_failure.json", _json_bytes(summary)))

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
        "output_directory": written.output_directory,
        "summary": summary,
    }


def build_sephora_onboarding_summary(
    *,
    parent: ParentContext,
    captured_responses: Sequence[tuple[ApiRequestSpec, ApiResponse]],
    question_limit: int,
) -> dict[str, Any]:
    """Build a capture summary exclusively from preserved response bytes."""
    by_name = {
        spec.artifact_name: _load_api_document(response.body, spec.artifact_name)
        for spec, response in captured_responses
    }
    expected_names = {spec.artifact_name for spec in _request_specs(parent.product_id, question_limit)}
    if set(by_name) != expected_names:
        raise SephoraOnboardingCaptureError(
            "summary adaptation requires the complete declared response set"
        )

    questions_doc = by_name["questions_most_answers_offset_000.json"]
    question_rows = _require_list(questions_doc, "Results", "questions")
    _validate_result_product_ids(
        question_rows,
        allowed_product_ids=(parent.product_id,),
        label="questions",
    )
    question_total = _require_nonnegative_int(questions_doc, "TotalResults", "questions")
    includes = questions_doc.get("Includes", questions_doc.get("Included", {}))
    if not isinstance(includes, Mapping):
        raise SephoraOnboardingCaptureError("questions Includes must be an object")
    raw_answers = includes.get("Answers", {})
    if isinstance(raw_answers, Mapping):
        included_answers = list(raw_answers.values())
    elif isinstance(raw_answers, list):
        included_answers = raw_answers
    else:
        raise SephoraOnboardingCaptureError("questions Includes.Answers must be an object or list")
    if any(not isinstance(answer, Mapping) for answer in included_answers):
        raise SephoraOnboardingCaptureError("questions included answer rows must be objects")

    question_inventory: list[dict[str, Any]] = []
    answer_count_sum = 0
    for index, raw_row in enumerate(question_rows):
        if not isinstance(raw_row, Mapping):
            raise SephoraOnboardingCaptureError(f"question row {index} must be an object")
        answer_count = _mapping_nonnegative_int(raw_row, "TotalAnswerCount", f"question row {index}")
        answer_count_sum += answer_count
        question_summary = _optional_string(raw_row.get("QuestionSummary"))
        question_details = _optional_string(raw_row.get("QuestionDetails"))
        if question_summary is None and question_details is None:
            raise SephoraOnboardingCaptureError(
                f"question row {index} has neither QuestionSummary nor QuestionDetails"
            )
        question_inventory.append(
            {
                "rank": index + 1,
                "question_id": _optional_string(raw_row.get("Id")),
                "question_text": _display_text(question_details or question_summary),
                "question_text_source": question_details or question_summary,
                "question_summary": question_summary,
                "question_details": question_details,
                "total_answer_count": answer_count,
                "submission_time": _optional_string(raw_row.get("SubmissionTime")),
                "user_nickname": _optional_string(raw_row.get("UserNickname")),
            }
        )

    non_incentivized_total = _total_results(
        by_name["reviews_non_incentivized_total.json"],
        "non-incentivized reviews",
    )
    _validate_result_product_ids(
        _require_list(
            by_name["reviews_non_incentivized_total.json"],
            "Results",
            "non-incentivized reviews",
        ),
        allowed_product_ids=parent.allowed_product_ids,
        label="non-incentivized reviews",
    )
    age_counts: dict[str, int] = {}
    for bucket in _AGE_BUCKET_SPECS:
        age_document = by_name[_age_artifact_name(bucket.display_label)]
        age_counts[bucket.display_label] = _total_results(
            age_document,
            f"non-incentivized reviews age {bucket.display_label}",
        )
        _validate_result_product_ids(
            _require_list(
                age_document,
                "Results",
                f"non-incentivized reviews age {bucket.display_label}",
            ),
            allowed_product_ids=parent.allowed_product_ids,
            label=f"non-incentivized reviews age {bucket.display_label}",
            allow_empty=age_counts[bucket.display_label] == 0,
        )
    declared_age_total = sum(age_counts.values())
    if declared_age_total > non_incentivized_total:
        raise SephoraOnboardingCaptureError(
            "sum of live age-bucket counts exceeds non-incentivized review total"
        )

    age_breakdown = [
        {
            "bucket": bucket.display_label,
            "api_value": bucket.api_value,
            "count": age_counts[bucket.display_label],
            "share_of_declared_age_subset_pct": _percentage(
                age_counts[bucket.display_label], declared_age_total
            ),
            "share_of_all_non_incentivized_reviews_pct": _percentage(
                age_counts[bucket.display_label], non_incentivized_total
            ),
        }
        for bucket in _AGE_BUCKET_SPECS
    ]
    questions_not_captured = max(question_total - len(question_rows), 0)
    answers_not_included = max(answer_count_sum - len(included_answers), 0)
    reviews_without_live_age_bucket = non_incentivized_total - declared_age_total

    loss_ledger = [
        {
            "field": "questions_beyond_bounded_window",
            "count": questions_not_captured,
            "detail": (
                f"Most Answers capture preserves {len(question_rows)} of {question_total} "
                f"questions; {questions_not_captured} lower-ranked questions remain outside "
                "this bounded onboarding packet"
            ),
        },
        {
            "field": "answers_not_returned_in_includes",
            "count": answers_not_included,
            "detail": (
                f"captured question rows declare {answer_count_sum} answers and the response "
                f"Includes block preserves {len(included_answers)}; difference={answers_not_included}"
            ),
        },
        {
            "field": "non_incentivized_reviews_without_live_age_bucket",
            "count": reviews_without_live_age_bucket,
            "detail": (
                f"{reviews_without_live_age_bucket} of {non_incentivized_total} exact "
                "non-incentivized reviews do not contribute to the four live age buckets; "
                "the demographic composition is not a percentage of all reviewers"
            ),
        },
    ]

    return {
        "record_kind": "sephora_bazaarvoice_onboarding_summary_v1",
        "parser_version": SEPHORA_ONBOARDING_PARSER_VERSION,
        "parent_packet": {
            "packet_id": parent.packet_id,
            "file_id": parent.file_id,
            "file_sha256": parent.file_sha256,
        },
        "product": {
            "product_id": parent.product_id,
            "allowed_product_and_sku_ids": list(parent.allowed_product_ids),
            "product_url": parent.product_url,
        },
        "questions": {
            "sort": "TotalAnswerCount:desc",
            "offset": 0,
            "requested_limit": question_limit,
            "total_questions": question_total,
            "captured_question_rows": len(question_rows),
            "captured_included_answer_rows": len(included_answers),
            "captured_question_declared_answer_sum": answer_count_sum,
            "question_inventory": question_inventory,
        },
        "reviews": {
            "filter": "ContextDataValue_IncentivizedReview:eq:False",
            "exact_non_incentivized_total": non_incentivized_total,
            "live_age_bucket_values": list(SEPHORA_AGE_BUCKETS),
            "declared_age_subset_total": declared_age_total,
            "declared_age_coverage_pct": _percentage(
                declared_age_total, non_incentivized_total
            ),
            "without_live_age_bucket_count": reviews_without_live_age_bucket,
            "without_live_age_bucket_pct": _percentage(
                reviews_without_live_age_bucket, non_incentivized_total
            ),
            "age_breakdown": age_breakdown,
        },
        "content_qualification": {
            "status": "passed",
            "response_documents": len(by_name),
            "age_bucket_vocabulary_exact": list(age_counts) == list(SEPHORA_AGE_BUCKETS),
        },
        "row_accounting": {
            "question_rows_raw": len(question_rows),
            "question_rows_summarized": len(question_inventory),
            "question_rows_equal": len(question_rows) == len(question_inventory),
            "answer_count_declared_by_captured_questions": answer_count_sum,
            "answer_rows_preserved_in_raw_includes": len(included_answers),
            "answers_equal": answer_count_sum == len(included_answers),
            "age_counts_source": "raw TotalResults from one exact filtered response per bucket",
        },
        "raw_failure_fallback": {
            "status": "armed",
            "behavior": (
                "if summary adaptation raises after acquisition, commit every acquired raw response "
                "plus sephora_adaptation_failure.json and return exit 5"
            ),
        },
        "loss_ledger": loss_ledger,
    }


def _parent_context(loaded: LoadedRawPacket, packet_id: str) -> ParentContext:
    manifest = loaded.manifest
    if manifest.get("source_family") != "retail_pdp":
        raise SephoraOnboardingCaptureError(
            f"parent packet {packet_id} is not source_family=retail_pdp"
        )
    locator = manifest.get("source_locator")
    product_url = (
        str(locator.get("value"))
        if isinstance(locator, Mapping) and locator.get("status") == "known"
        else ""
    )
    product_id_from_url = _product_id_from_url(product_url)

    candidates: list[tuple[str, bytes]] = []
    for file_id, body in loaded.bodies.items():
        if b'id="linkStore"' in body and b"Sephora.configurationSettings" in body:
            candidates.append((file_id, body))
    if len(candidates) != 1:
        raise SephoraOnboardingCaptureError(
            f"parent packet {packet_id} requires exactly one rendered DOM with "
            "linkStore and Sephora.configurationSettings"
        )
    file_id, body = candidates[0]
    text = body.decode("utf-8", errors="replace")
    product = _link_store_product(text)
    product_id = _required_string(product.get("productId"), "linkStore.page.product.productId")
    if product_id != product_id_from_url:
        raise SephoraOnboardingCaptureError(
            f"parent product mismatch: URL={product_id_from_url}, linkStore={product_id}"
        )
    preserved = next(
        (
            item
            for item in manifest.get("preserved_files", [])
            if isinstance(item, Mapping) and item.get("file_id") == file_id
        ),
        None,
    )
    if not isinstance(preserved, Mapping) or not isinstance(preserved.get("sha256"), str):
        raise SephoraOnboardingCaptureError("parent DOM preserved-file hash is unavailable")
    allowed_product_ids = _sephora_product_and_sku_ids(product)
    return ParentContext(
        packet_id=packet_id,
        file_id=file_id,
        file_sha256=str(preserved["sha256"]),
        product_id=product_id,
        allowed_product_ids=allowed_product_ids,
        product_url=product_url,
        review_config=_read_config(text, "bvApi_rwdRating_desktop_read"),
        question_config=_read_config(text, "bvApi_rwdQandA_desktop_read"),
    )


def _link_store_product(html: str) -> Mapping[str, Any]:
    match = re.search(
        r"<script\b[^>]*\bid=[\"']linkStore[\"'][^>]*>([\s\S]*?)</script\s*>",
        html,
        flags=re.IGNORECASE,
    )
    if match is None:
        raise SephoraOnboardingCaptureError("rendered DOM is missing linkStore")
    try:
        payload = json.loads(match.group(1).strip())
        product = payload["page"]["product"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise SephoraOnboardingCaptureError(
            "rendered DOM has no valid linkStore.page.product"
        ) from exc
    if not isinstance(product, Mapping):
        raise SephoraOnboardingCaptureError("linkStore.page.product must be an object")
    return product


def _read_config(html: str, key: str) -> BazaarvoiceReadConfig:
    match = re.search(
        rf'"{re.escape(key)}"\s*:\s*(\{{[^{{}}]*\}})',
        html,
    )
    if match is None:
        raise SephoraOnboardingCaptureError(f"page-declared read config is missing: {key}")
    try:
        raw = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise SephoraOnboardingCaptureError(
            f"page-declared read config is malformed: {key}"
        ) from exc
    host = _required_string(raw.get("host"), f"{key}.host")
    version = _required_string(raw.get("version"), f"{key}.version")
    token = _required_string(raw.get("token"), f"{key}.token")
    if host != BAZAARVOICE_API_HOST:
        raise SephoraOnboardingCaptureError(
            f"{key}.host must be the allowlisted {BAZAARVOICE_API_HOST}"
        )
    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        raise SephoraOnboardingCaptureError(f"{key}.version is invalid")
    return BazaarvoiceReadConfig(host=host, version=version, token=token)


def _sephora_product_and_sku_ids(product: Mapping[str, Any]) -> tuple[str, ...]:
    ids: list[str] = [_required_string(product.get("productId"), "product.productId")]
    current_sku = product.get("currentSku")
    if isinstance(current_sku, Mapping):
        sku_id = _optional_string(current_sku.get("skuId"))
        if sku_id is not None:
            ids.append(sku_id)
    for key in ("regularChildSkus", "onSaleChildSkus"):
        raw_skus = product.get(key, [])
        if not isinstance(raw_skus, list):
            continue
        for raw_sku in raw_skus:
            if not isinstance(raw_sku, Mapping):
                continue
            sku_id = _optional_string(raw_sku.get("skuId"))
            if sku_id is not None:
                ids.append(sku_id)
    return tuple(dict.fromkeys(ids))


def _request_specs(product_id: str, question_limit: int) -> tuple[ApiRequestSpec, ...]:
    common_review = (
        ("Filter", f"ProductId:eq:{product_id}"),
        ("Filter", "ContextDataValue_IncentivizedReview:eq:False"),
        ("Limit", "1"),
        ("Offset", "0"),
    )
    specs = [
        ApiRequestSpec(
            artifact_name="questions_most_answers_offset_000.json",
            endpoint="questions.json",
            config_kind="questions",
            parameters=(
                ("Filter", f"ProductId:eq:{product_id}"),
                ("Include", "Answers"),
                ("Limit", str(question_limit)),
                ("Offset", "0"),
                ("Sort", "TotalAnswerCount:desc"),
            ),
        ),
        ApiRequestSpec(
            artifact_name="reviews_non_incentivized_total.json",
            endpoint="reviews.json",
            config_kind="reviews",
            parameters=common_review,
        ),
    ]
    for bucket in _AGE_BUCKET_SPECS:
        specs.append(
            ApiRequestSpec(
                artifact_name=_age_artifact_name(bucket.display_label),
                endpoint="reviews.json",
                config_kind="reviews",
                parameters=(
                    *common_review[:2],
                    ("Filter", f"ContextDataValue_ageRange:eq:{bucket.api_value}"),
                    *common_review[2:],
                ),
            )
        )
    return tuple(specs)


def _request_manifest(
    parent: ParentContext,
    specs: Sequence[ApiRequestSpec],
    captured: Sequence[tuple[ApiRequestSpec, ApiResponse]],
) -> dict[str, Any]:
    response_by_name = {spec.artifact_name: response for spec, response in captured}
    return {
        "record_kind": "sephora_bazaarvoice_request_manifest_v1",
        "parent_packet_id": parent.packet_id,
        "parent_file_id": parent.file_id,
        "parent_file_sha256": parent.file_sha256,
        "product_id": parent.product_id,
        "product_url": parent.product_url,
        "credential_posture": (
            "page-declared read tokens used in flight; tokens and secret-bearing request URLs "
            "are not persisted"
        ),
        "requests": [
            {
                "artifact_name": spec.artifact_name,
                "endpoint": f"https://{BAZAARVOICE_API_HOST}/data/{spec.endpoint}",
                "api_version": (
                    parent.question_config.version
                    if spec.config_kind == "questions"
                    else parent.review_config.version
                ),
                "parameters": [
                    {"name": name, "value": value} for name, value in spec.parameters
                ],
                "response": (
                    {
                        "status": response_by_name[spec.artifact_name].status,
                        "reason": response_by_name[spec.artifact_name].reason or None,
                        "content_type": response_by_name[spec.artifact_name].content_type,
                        "byte_count": len(response_by_name[spec.artifact_name].body),
                        "captured_at": response_by_name[spec.artifact_name].captured_at,
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
    parent: ParentContext,
    artifacts: Sequence[tuple[str, bytes]],
    captured: Sequence[tuple[ApiRequestSpec, ApiResponse]],
    limitations: Sequence[str],
    summary: Mapping[str, Any],
):
    file_ids = staged_file_id_map(artifacts)
    captured_at = captured[-1][1].captured_at if captured else utc_now_z()
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "Bazaarvoice responses do not declare a single source publication time"
        ),
        source_edit_or_version=unknown_with_reason(
            "Bazaarvoice responses do not declare a product-level edit version"
        ),
        capture_time=known_fact(captured_at),
        recapture_time=known_fact(captured_at),
        cutoff_posture=known_fact("post_cutoff"),
    )
    access = known_fact(
        "page-declared Bazaarvoice read API attempted; exact acquired response bytes preserved"
    )
    archive = not_attempted("structured companion capture did not query archive/history")
    media = not_attempted("structured companion capture did not fetch linked review media")
    recapture = known_fact("supplement")
    return stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="sephora_review_qa_onboarding",
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
                preserved_file_ids=[file_ids[name] for name, _content in artifacts],
            )
        ],
        source_family="retail_pdp",
        source_surface=SEPHORA_ONBOARDING_SOURCE_SURFACE,
        source_locator=known_fact(parent.product_url),
        decision_question=(
            "What does Sephora expose in a bounded Most Answers Q&A window, and what "
            "is the exact live age-bucket composition of non-incentivized reviews?"
        ),
        capture_context=(
            f"structured companion capture from hash-verified parent packet "
            f"{parent.packet_id}; parser={SEPHORA_ONBOARDING_PARSER_VERSION}"
        ),
        actor_audience_context=unknown_with_reason(
            "reviewer demographic fields are self-reported source context; audience "
            "representativeness is not established"
        ),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="sephora_onboarding_cli_operator",
        session_identity=None,
        visible_mode_changes=[
            "questions_sort_total_answer_count_desc",
            "reviews_filter_non_incentivized_false",
            "review_age_bucket_inventory_20s_30s_40s_50s_plus",
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
            f"Sephora onboarding companion for {parent.product_id}: "
            f"{summary.get('record_kind', 'unknown result')}; exact API response bytes "
            "and a token-free request manifest are preserved."
        ),
        receipt_non_claims=[
            "not the complete Q&A corpus",
            "not reviewer population representativeness",
            "not an age estimate for reviews without a live age bucket",
            "not review-body normalization or Judgment",
            "not a replacement for the parent rendered PDP packet",
        ],
    )


def _load_api_document(body: bytes, label: str) -> Mapping[str, Any]:
    try:
        document = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SephoraOnboardingCaptureError(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(document, Mapping):
        raise SephoraOnboardingCaptureError(f"{label} JSON root must be an object")
    errors = document.get("Errors")
    if errors:
        raise SephoraOnboardingCaptureError(f"{label} declares API errors")
    return document


def _require_list(document: Mapping[str, Any], key: str, label: str) -> list[Any]:
    value = document.get(key)
    if not isinstance(value, list):
        raise SephoraOnboardingCaptureError(f"{label}.{key} must be a list")
    return value


def _require_nonnegative_int(
    document: Mapping[str, Any], key: str, label: str
) -> int:
    value = document.get(key)
    if type(value) is not int or value < 0:
        raise SephoraOnboardingCaptureError(
            f"{label}.{key} must be a nonnegative integer"
        )
    return value


def _mapping_nonnegative_int(document: Mapping[str, Any], key: str, label: str) -> int:
    value = document.get(key)
    if type(value) is not int or value < 0:
        raise SephoraOnboardingCaptureError(f"{label}.{key} must be a nonnegative integer")
    return value


def _validate_result_product_ids(
    rows: Sequence[Any],
    *,
    allowed_product_ids: Sequence[str],
    label: str,
    allow_empty: bool = False,
) -> None:
    if not rows:
        if allow_empty:
            return
        raise SephoraOnboardingCaptureError(
            f"{label}.Results is empty; served product identity cannot be verified"
        )
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise SephoraOnboardingCaptureError(f"{label}.Results[{index}] must be an object")
        product_id = _required_string(
            row.get("ProductId"),
            f"{label}.Results[{index}].ProductId",
        )
        if product_id not in allowed_product_ids:
            raise SephoraOnboardingCaptureError(
                f"{label}.Results[{index}] product mismatch: "
                f"expected one of {list(allowed_product_ids)}, got {product_id}"
            )


def _total_results(document: Mapping[str, Any], label: str) -> int:
    return _require_nonnegative_int(document, "TotalResults", label)


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SephoraOnboardingCaptureError(f"{label} must be a non-empty string")
    return value.strip()


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _product_id_from_url(url: str) -> str:
    match = re.search(r"-P(\d+)(?:[/?#]|$)", url, flags=re.IGNORECASE)
    if match is None:
        raise SephoraOnboardingCaptureError(
            "parent source locator is not a Sephora product URL with a product ID"
        )
    return f"P{match.group(1)}"


def _age_artifact_name(bucket: str) -> str:
    slug = bucket.lower().replace(" ", "").replace("+", "_plus")
    return f"reviews_non_incentivized_age_{slug}.json"


def _percentage(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator * 100.0 / denominator, 2)


def _display_text(value: str) -> str:
    return " ".join(html_lib.unescape(unquote(value)).split())


def _safe_error_text(exc: Exception) -> str:
    text = str(exc)
    if "passkey=" in text or "token=" in text:
        return "secret-bearing acquisition error suppressed"
    return text[:300]


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


__all__ = [
    "ApiRequestSpec",
    "ApiResponse",
    "BazaarvoiceReadConfig",
    "DEFAULT_QUESTION_LIMIT",
    "ParentContext",
    "SEPHORA_AGE_BUCKETS",
    "SEPHORA_ONBOARDING_PARSER_VERSION",
    "SEPHORA_ONBOARDING_SOURCE_SURFACE",
    "SephoraOnboardingCaptureError",
    "build_sephora_onboarding_summary",
    "capture_sephora_onboarding_packet",
]
