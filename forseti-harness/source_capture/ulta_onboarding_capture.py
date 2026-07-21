"""Raw-preserving Ulta PowerReviews onboarding companion capture.

Ulta's structured review surface is PowerReviews, not Bazaarvoice. This
capture consumes one admitted rendered Ulta PDP parent packet, resolves the
page-declared public display configuration, preserves bounded Most Helpful,
Most Recent, and Q&A display responses with a token-free request manifest, and
enforces the Gate 1 native-ID invariant (``review_id == ugc_id``) plus the
parent identity binding on every returned row. The unfiltered source baseline
is preserved: no incentive or syndication filter is applied or claimed.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

from data_lake.root import DataLakeRoot, LoadedRawPacket
from harness_utils import utc_now_z
from source_capture.adapters.ulta_powerreviews import (
    POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX,
    PowerReviewsFetcher,
    PowerReviewsReadConfig,
    PowerReviewsRequestSpec,
    PowerReviewsResponse,
    fetch_powerreviews_display_response,
    resolve_ulta_powerreviews_config,
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


ULTA_ONBOARDING_SOURCE_SURFACE = "ulta_powerreviews_onboarding"
ULTA_ONBOARDING_PARSER_VERSION = "ulta_powerreviews_onboarding_v1"
DEFAULT_REVIEW_PAGE_SIZE = POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX
DEFAULT_PAGES_PER_ROLE = 4
DEFAULT_QUESTION_LIMIT = POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX
_MAX_PAGES_PER_ROLE = 4
_ULTA_PRODUCT_PATH = re.compile(r"^/p/[A-Za-z0-9%.~-]*?-(?P<pid>(?:xlsImpprod|pimprod|prod)[A-Za-z0-9]+)/?$")
_PIN_ASSERTION = "ulta_us_market_assertion"

# Observed rendered control labels on the reference PDP for these API sort
# values. Context for readers of the summary, not a claim that the widget and
# the display route share one vocabulary.
_RENDERED_SORT_LABEL_REFERENCE = {
    "MostHelpful": "Most Helpful",
    "Newest": "Most Recent",
}


class UltaOnboardingCaptureError(RuntimeError):
    """Fail-closed acquisition or content-qualification error."""


@dataclass(frozen=True)
class UltaParentContext:
    packet_id: str
    dom_file_id: str
    dom_file_sha256: str
    product_url: str
    url_product_id: str
    pin_metadata: Mapping[str, Any]


def capture_ulta_onboarding_packet(
    *,
    data_root: DataLakeRoot,
    parent_packet_id: str,
    review_page_size: int = DEFAULT_REVIEW_PAGE_SIZE,
    pages_per_role: int = DEFAULT_PAGES_PER_ROLE,
    question_limit: int = DEFAULT_QUESTION_LIMIT,
    timeout_seconds: float = 30.0,
    max_bytes: int = 8_000_000,
    api_fetcher: PowerReviewsFetcher | None = None,
) -> tuple[int, dict[str, Any]]:
    """Capture Ulta Helpful, Recent, and Q&A display responses as one packet."""
    if data_root.readonly:
        raise UltaOnboardingCaptureError("capture requires a writable DataLakeRoot")
    if not 1 <= review_page_size <= POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX:
        raise ValueError(
            "review_page_size must be between 1 and "
            f"{POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX}"
        )
    if not 1 <= pages_per_role <= _MAX_PAGES_PER_ROLE:
        raise ValueError(f"pages_per_role must be between 1 and {_MAX_PAGES_PER_ROLE}")
    if not 1 <= question_limit <= POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX:
        raise ValueError(
            "question_limit must be between 1 and "
            f"{POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX}"
        )
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")

    loaded = data_root.load_raw_packet(parent_packet_id)
    parent = _parent_context(loaded, parent_packet_id)
    dom_text = loaded.bodies[parent.dom_file_id].decode("utf-8", errors="strict")
    config = resolve_ulta_powerreviews_config(dom_text)
    if config.page_id != parent.url_product_id:
        raise UltaOnboardingCaptureError(
            "Ulta parent product mismatch: "
            f"URL={parent.url_product_id}, page-declared={config.page_id}"
        )

    fetch_api = api_fetcher or fetch_powerreviews_display_response
    captured: list[tuple[PowerReviewsRequestSpec, PowerReviewsResponse]] = []
    acquisition_failure: dict[str, Any] | None = None

    def _acquire(spec: PowerReviewsRequestSpec) -> Mapping[str, Any] | None:
        """Fetch one spec; return its parsed document, or None on recorded failure."""
        nonlocal acquisition_failure
        try:
            response = fetch_api(spec, config, timeout_seconds, max_bytes)
        except Exception as exc:
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "error_type": type(exc).__name__,
                "error": _safe_error_text(exc),
            }
            return None
        _require_secret_free(response, config, spec.artifact_name)
        captured.append((spec, response))
        if not 200 <= response.status < 300:
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "http_status": response.status,
                "reason": response.reason,
            }
            return None
        try:
            return _load_document(response.body, spec.artifact_name)
        except UltaOnboardingCaptureError as exc:
            acquisition_failure = {
                "artifact_name": spec.artifact_name,
                "error_type": type(exc).__name__,
                "error": _safe_error_text(exc),
            }
            return None

    for role, sort in (("most_helpful", "MostHelpful"), ("most_recent", "Newest")):
        if acquisition_failure is not None:
            break
        total: int | None = None
        for page_index in range(pages_per_role):
            offset = page_index * review_page_size
            if total is not None and offset >= total:
                break
            document = _acquire(
                _review_spec(
                    role=role,
                    sort=sort,
                    page_size=review_page_size,
                    offset=offset,
                )
            )
            if document is None:
                break
            try:
                total = _total_results(document, f"reviews_{role}_offset_{offset:03d}.json")
            except UltaOnboardingCaptureError as exc:
                acquisition_failure = {
                    "artifact_name": f"reviews_{role}_offset_{offset:03d}.json",
                    "error_type": type(exc).__name__,
                    "error": _safe_error_text(exc),
                }
                break
    if acquisition_failure is None:
        _acquire(_question_spec(question_limit))

    request_manifest = _request_manifest(parent, config, captured)
    artifacts: list[tuple[str, bytes]] = [
        (spec.artifact_name, response.body) for spec, response in captured
    ]
    artifacts.append(("ulta_request_manifest.json", _json_bytes(request_manifest)))

    exit_code = 0
    limitations: list[str] = []
    if acquisition_failure is not None:
        exit_code = 4
        limitations.append(
            "structured display acquisition did not complete; every response "
            "acquired before failure is preserved and no successful summary is claimed"
        )
        summary: dict[str, Any] = {
            "record_kind": "ulta_powerreviews_onboarding_capture_failure_v1",
            "parser_version": ULTA_ONBOARDING_PARSER_VERSION,
            "provider": "powerreviews",
            "parent_packet_id": parent.packet_id,
            "ulta_product_id": parent.url_product_id,
            "failure": acquisition_failure,
            "raw_failure_fallback": {
                "status": "preserved_partial_responses",
                "preserved_response_count": len(captured),
            },
        }
        artifacts.append(("ulta_capture_failure.json", _json_bytes(summary)))
    else:
        try:
            summary = build_ulta_onboarding_summary(
                parent=parent,
                config=config,
                captured_responses=captured,
            )
            limitations.extend(entry["detail"] for entry in summary["loss_ledger"])
            artifacts.append(("ulta_onboarding_summary.json", _json_bytes(summary)))
        except Exception as exc:
            exit_code = 5
            limitations.append(
                "Ulta onboarding adaptation failed after acquisition; every exact "
                "PowerReviews response is preserved as the required raw fallback"
            )
            summary = {
                "record_kind": "ulta_powerreviews_onboarding_adaptation_failure_v1",
                "parser_version": ULTA_ONBOARDING_PARSER_VERSION,
                "provider": "powerreviews",
                "parent_packet_id": parent.packet_id,
                "ulta_product_id": parent.url_product_id,
                "failure": {
                    "error_type": type(exc).__name__,
                    "error": _safe_error_text(exc),
                },
                "raw_failure_fallback": {
                    "status": "all_responses_preserved",
                    "preserved_response_count": len(captured),
                },
            }
            artifacts.append(("ulta_adaptation_failure.json", _json_bytes(summary)))

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


def build_ulta_onboarding_summary(
    *,
    parent: UltaParentContext,
    config: PowerReviewsReadConfig,
    captured_responses: Sequence[tuple[PowerReviewsRequestSpec, PowerReviewsResponse]],
) -> dict[str, Any]:
    helpful_pages = _role_documents(captured_responses, "most_helpful")
    recent_pages = _role_documents(captured_responses, "most_recent")
    question_docs = [
        (spec, _load_document(response.body, spec.artifact_name))
        for spec, response in captured_responses
        if spec.resource == "questions"
    ]
    if not helpful_pages or not recent_pages or len(question_docs) != 1:
        raise UltaOnboardingCaptureError(
            "Ulta summary requires Most Helpful, Most Recent, and Q&A responses"
        )

    helpful_rows = _review_rows(helpful_pages, config.page_id)
    recent_rows = _review_rows(recent_pages, config.page_id)
    _require_native_id_invariant(helpful_rows + recent_rows)
    _require_unique_ids(helpful_rows, "most_helpful")
    _require_unique_ids(recent_rows, "most_recent")
    _require_nonincreasing(
        [_row_int(row, "metrics", "helpful_votes") for row, _name in helpful_rows],
        "most_helpful",
        "metrics.helpful_votes",
    )
    _require_nonincreasing(
        [_row_int(row, "details", "created_date") for row, _name in recent_rows],
        "most_recent",
        "details.created_date",
    )

    rollup = _rollup(recent_pages[0][1], recent_pages[0][0].artifact_name)
    totals = {
        spec.artifact_name: _total_results(document, spec.artifact_name)
        for spec, document in (*helpful_pages, *recent_pages)
    }
    total_disagreement = sorted(set(totals.values()))

    question_spec, question_document = question_docs[0]
    question_rows = _question_rows(
        question_document, question_spec.artifact_name, config.page_id
    )
    included_answer_counts = [
        len(_list_value(row.get("answer"))) for row in question_rows
    ]
    declared_answer_counts = [
        _nonnegative_int(row.get("answer_count"), "questions.answer_count")
        for row in question_rows
    ]

    summary: dict[str, Any] = {
        "record_kind": "ulta_powerreviews_onboarding_summary_v1",
        "parser_version": ULTA_ONBOARDING_PARSER_VERSION,
        "provider": "powerreviews",
        "retailer": "Ulta",
        "parent_packet": {
            "packet_id": parent.packet_id,
            "file_id": parent.dom_file_id,
            "file_sha256": parent.dom_file_sha256,
            "product_url": parent.product_url,
            "raw_file_reference": f"{parent.packet_id}:{parent.dom_file_id}",
        },
        "identity": {
            "ulta_product_id": parent.url_product_id,
            "powerreviews_page_id": config.page_id,
            "mapping_equal": config.page_id == parent.url_product_id,
            "merchant_id": config.merchant_id,
            "merchant_group_id": config.merchant_group_id,
            "locale": config.locale,
            "native_review_id_semantics": (
                "review_id equals ugc_id on every captured row; the separate Gate 1 "
                "cross-check established that structured review_id corresponds to the "
                "rendered pr-rd-review-headline-<id> suffix on the reference PDP"
            ),
        },
        "configuration": {
            "config_anchor": (
                "script#PowerReviewsRender POWERREVIEWS.display.render block in "
                "the parent rendered DOM"
            ),
            "display_host": config.host,
            "credential_posture": (
                "page-declared public display api key used only in flight; the key "
                "and credential-bearing request URLs are not persisted"
            ),
            "parent_pin_metadata": {
                "pre_capture": parent.pin_metadata.get("pre_capture"),
                "pin_confirmed": parent.pin_metadata.get("pin_confirmed"),
                "access_blocked": parent.pin_metadata.get("access_blocked"),
                "proxy_used": parent.pin_metadata.get("proxy_used"),
                "geoip_used": parent.pin_metadata.get("geoip_used"),
            },
        },
        "review_aggregates": {
            "rollup_raw_file": recent_pages[0][0].artifact_name,
            "average_rating": rollup.get("average_rating"),
            "rating_count": rollup.get("rating_count"),
            "review_count": rollup.get("review_count"),
            "rating_histogram": rollup.get("rating_histogram"),
            "recommended_ratio": rollup.get("recommended_ratio"),
            "native_review_count": rollup.get("native_review_count"),
            "native_sampling_review_count": rollup.get(
                "native_sampling_review_count"
            ),
            "native_sweepstakes_review_count": rollup.get(
                "native_sweepstakes_review_count"
            ),
            "native_community_content_review_count": rollup.get(
                "native_community_content_review_count"
            ),
            "syndicated_review_count": rollup.get("syndicated_review_count"),
            "faceoff_positive_present": rollup.get("faceoff_positive") is not None,
            "faceoff_negative_present": rollup.get("faceoff_negative") is not None,
            "per_response_total_results": totals,
            "total_results_disagreement": (
                total_disagreement if len(total_disagreement) > 1 else None
            ),
        },
        "reviews": {
            "most_helpful": _review_view_summary(helpful_pages, helpful_rows, "most_helpful"),
            "most_recent": _review_view_summary(recent_pages, recent_rows, "most_recent"),
            "last_seen_review_id": (
                str(recent_rows[0][0]["review_id"]) if recent_rows else None
            ),
        },
        "questions": {
            "total_questions": _total_results(
                question_document, question_spec.artifact_name
            ),
            "captured_question_rows": len(question_rows),
            "declared_answer_rows": sum(declared_answer_counts),
            "captured_included_answer_rows": sum(included_answer_counts),
            "question_source_fields": _field_inventory(question_rows),
            "question_inventory": [
                _question_row_summary(row, question_spec.artifact_name, rank)
                for rank, row in enumerate(question_rows, start=1)
            ],
            "raw_file": question_spec.artifact_name,
        },
        "extraction_target_matrix": [
            {
                "information_class": "product_identity_variant_offer_claims_and_media",
                "status": "observed",
                "raw_reference": f"{parent.packet_id}:{parent.dom_file_id}",
                "detail": "carried by the admitted parent rendered PDP packet",
            },
            {
                "information_class": "most_helpful_reviews",
                "status": "observed",
                "raw_reference": helpful_pages[0][0].artifact_name,
            },
            {
                "information_class": "most_recent_reviews_and_anchor",
                "status": "observed",
                "raw_reference": recent_pages[0][0].artifact_name,
            },
            {
                "information_class": "review_aggregates",
                "status": "observed",
                "raw_reference": recent_pages[0][0].artifact_name,
            },
            {
                "information_class": "per_row_incentive_disclosure",
                "status": "observed",
                "raw_reference": recent_pages[0][0].artifact_name,
                "detail": (
                    "details.disclosure_code per disclosed row plus rollup "
                    "native_sampling_review_count; unfiltered baseline preserved"
                ),
            },
            {
                "information_class": "source_proven_non_incentivized_filter",
                "status": "not_exposed",
                "raw_reference": recent_pages[0][0].artifact_name,
                "detail": (
                    "no display-route incentive filter is proven; none is applied "
                    "or claimed"
                ),
            },
            {
                "information_class": "aggregate_reviewer_demographic_distributions",
                "status": "not_exposed",
                "raw_reference": recent_pages[0][0].artifact_name,
                "detail": (
                    "no aggregate age/skin distributions with denominators; per-row "
                    "Describe Yourself / Skin Type properties are preserved in raw "
                    "rows when present"
                ),
            },
            {
                "information_class": "answer_rich_qa",
                "status": "observed",
                "raw_reference": question_spec.artifact_name,
            },
        ],
        "row_accounting": {
            "helpful_rows_equal": len(helpful_rows)
            == sum(
                len(_document_reviews(document, spec.artifact_name))
                for spec, document in helpful_pages
            ),
            "recent_rows_equal": len(recent_rows)
            == sum(
                len(_document_reviews(document, spec.artifact_name))
                for spec, document in recent_pages
            ),
            "question_rows_equal": len(question_rows)
            == len(_document_questions(question_document, question_spec.artifact_name)),
            "included_answers_match_declared": included_answer_counts
            == declared_answer_counts,
        },
        "loss_ledger": _loss_ledger(
            helpful_captured=len(helpful_rows),
            recent_captured=len(recent_rows),
            totals=totals,
            included_answer_counts=included_answer_counts,
            declared_answer_counts=declared_answer_counts,
            total_disagreement=total_disagreement,
        ),
        "content_qualification": {
            "status": "passed",
            "provider_identity": "powerreviews",
            "product_mapping_bound": config.page_id == parent.url_product_id,
            "three_response_roles_present": True,
            "native_review_id_invariant_held": True,
            "exact_raw_response_bytes_preserved": True,
            "summary_duplicates_review_or_answer_bodies": False,
        },
    }
    if not summary["identity"]["mapping_equal"]:
        raise UltaOnboardingCaptureError(
            "Ulta product id does not equal the page-declared PowerReviews page_id"
        )
    return summary


def _parent_context(loaded: LoadedRawPacket, packet_id: str) -> UltaParentContext:
    manifest = loaded.manifest
    if manifest.get("source_family") != "retail_pdp":
        raise UltaOnboardingCaptureError(
            f"parent packet {packet_id} is not source_family=retail_pdp"
        )
    locator = manifest.get("source_locator")
    product_url = (
        str(locator.get("value"))
        if isinstance(locator, Mapping) and locator.get("status") == "known"
        else ""
    )
    url_product_id = _ulta_product_id_from_url(product_url)
    dom_candidates = [
        (file_id, body)
        for file_id, body in loaded.bodies.items()
        if b"PowerReviewsRender" in body and b"POWERREVIEWS.display.render" in body
    ]
    if len(dom_candidates) != 1:
        raise UltaOnboardingCaptureError(
            f"parent packet {packet_id} requires exactly one Ulta rendered DOM "
            "with a PowerReviewsRender configuration block"
        )
    dom_file_id, _dom_body = dom_candidates[0]
    pin_candidates = []
    for _file_id, body in loaded.bodies.items():
        if _PIN_ASSERTION.encode("utf-8") not in body:
            continue
        try:
            document = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if (
            isinstance(document, Mapping)
            and document.get("pre_capture") == _PIN_ASSERTION
        ):
            pin_candidates.append(document)
    if len(pin_candidates) != 1:
        raise UltaOnboardingCaptureError(
            f"parent packet {packet_id} requires exactly one preserved "
            f"{_PIN_ASSERTION} metadata document"
        )
    pin_metadata = pin_candidates[0]
    if pin_metadata.get("pin_confirmed") is not True:
        raise UltaOnboardingCaptureError(
            f"parent packet {packet_id} did not confirm the Ulta US/USD market pin"
        )
    if pin_metadata.get("access_blocked") is not False:
        raise UltaOnboardingCaptureError(
            f"parent packet {packet_id} recorded an access block"
        )
    preserved = next(
        (
            item
            for item in manifest.get("preserved_files", [])
            if isinstance(item, Mapping) and item.get("file_id") == dom_file_id
        ),
        None,
    )
    if not isinstance(preserved, Mapping) or not isinstance(
        preserved.get("sha256"), str
    ):
        raise UltaOnboardingCaptureError(
            "parent DOM preserved-file hash is unavailable"
        )
    return UltaParentContext(
        packet_id=packet_id,
        dom_file_id=dom_file_id,
        dom_file_sha256=str(preserved["sha256"]),
        product_url=product_url,
        url_product_id=url_product_id,
        pin_metadata=pin_metadata,
    )


def _ulta_product_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    match = _ULTA_PRODUCT_PATH.fullmatch(parsed.path)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "www.ulta.com"
        or match is None
    ):
        raise UltaOnboardingCaptureError(
            "Ulta parent URL must be an HTTPS www.ulta.com /p/<slug>-<product id> PDP"
        )
    return match.group("pid")


def _review_spec(
    *,
    role: str,
    sort: str,
    page_size: int,
    offset: int,
) -> PowerReviewsRequestSpec:
    return PowerReviewsRequestSpec(
        artifact_name=f"reviews_{role}_offset_{offset:03d}.json",
        resource="reviews",
        parameters=(
            ("paging.size", str(page_size)),
            ("paging.from", str(offset)),
            ("sort", sort),
        ),
    )


def _question_spec(question_limit: int) -> PowerReviewsRequestSpec:
    return PowerReviewsRequestSpec(
        artifact_name="questions_display_offset_000.json",
        resource="questions",
        parameters=(
            ("paging.size", str(question_limit)),
            ("paging.from", "0"),
        ),
    )


def _require_secret_free(
    response: PowerReviewsResponse,
    config: PowerReviewsReadConfig,
    artifact_name: str,
) -> None:
    if config.api_key.encode("utf-8") in response.body:
        raise UltaOnboardingCaptureError(
            f"{artifact_name} echoed the public display key; refusing to persist "
            "credential-bearing response bytes"
        )


def _role_documents(
    captured_responses: Sequence[tuple[PowerReviewsRequestSpec, PowerReviewsResponse]],
    role: str,
) -> list[tuple[PowerReviewsRequestSpec, Mapping[str, Any]]]:
    return [
        (spec, _load_document(response.body, spec.artifact_name))
        for spec, response in captured_responses
        if spec.resource == "reviews" and spec.artifact_name.startswith(f"reviews_{role}_")
    ]


def _review_rows(
    pages: Sequence[tuple[PowerReviewsRequestSpec, Mapping[str, Any]]],
    page_id: str,
) -> list[tuple[Mapping[str, Any], str]]:
    rows: list[tuple[Mapping[str, Any], str]] = []
    for spec, document in pages:
        page_rows = _document_reviews(document, spec.artifact_name)
        total = _total_results(document, spec.artifact_name)
        if not page_rows and total > 0:
            raise UltaOnboardingCaptureError(
                f"{spec.artifact_name} returned zero rows although the source "
                f"declares {total} results; the display route silently empties "
                "out-of-bounds requests"
            )
        for row in page_rows:
            declared_page = str(
                _mapping_value(row.get("details")).get("product_page_id")
            )
            if declared_page != page_id:
                raise UltaOnboardingCaptureError(
                    f"{spec.artifact_name} contains a row bound to foreign "
                    f"product_page_id {declared_page!r}"
                )
            rows.append((row, spec.artifact_name))
    return rows


def _require_native_id_invariant(
    rows: Sequence[tuple[Mapping[str, Any], str]],
) -> None:
    for row, artifact_name in rows:
        review_id = row.get("review_id")
        ugc_id = row.get("ugc_id")
        if review_id is None or str(review_id) != str(ugc_id):
            raise UltaOnboardingCaptureError(
                f"{artifact_name} violates the native review-id invariant "
                "(review_id must equal ugc_id)"
            )


def _require_unique_ids(
    rows: Sequence[tuple[Mapping[str, Any], str]],
    role: str,
) -> None:
    ids = [str(row["review_id"]) for row, _name in rows]
    if len(ids) != len(set(ids)):
        raise UltaOnboardingCaptureError(
            f"{role} responses contain duplicate review IDs"
        )


def _require_nonincreasing(
    values: Sequence[int],
    role: str,
    field: str,
) -> None:
    if list(values) != sorted(values, reverse=True):
        raise UltaOnboardingCaptureError(
            f"{role} responses are not ordered by {field} descending"
        )


def _review_view_summary(
    pages: Sequence[tuple[PowerReviewsRequestSpec, Mapping[str, Any]]],
    rows: Sequence[tuple[Mapping[str, Any], str]],
    role: str,
) -> dict[str, Any]:
    sort_value = dict(pages[0][0].parameters)["sort"]
    return {
        "role": role,
        "api_sort_parameter": sort_value,
        "rendered_control_label_reference": _RENDERED_SORT_LABEL_REFERENCE.get(
            sort_value
        ),
        "total_results": _total_results(pages[0][1], pages[0][0].artifact_name),
        "captured_review_rows": len(rows),
        "captured_review_bodies": sum(
            bool(_mapping_value(row.get("details")).get("comments"))
            for row, _name in rows
        ),
        "source_fields": _field_inventory([row for row, _name in rows]),
        "review_inventory": [
            _review_row_summary(row, artifact_name, rank)
            for rank, (row, artifact_name) in enumerate(rows, start=1)
        ],
        "raw_files": [spec.artifact_name for spec, _document in pages],
    }


def _review_row_summary(
    row: Mapping[str, Any],
    raw_file: str,
    rank: int,
) -> dict[str, Any]:
    details = _mapping_value(row.get("details"))
    metrics = _mapping_value(row.get("metrics"))
    badges = _mapping_value(row.get("badges"))
    return {
        "rank": rank,
        "review_id": str(row.get("review_id")),
        "ugc_id_equal": str(row.get("review_id")) == str(row.get("ugc_id")),
        "internal_review_id": row.get("internal_review_id"),
        "legacy_id": row.get("legacy_id"),
        "created_date": details.get("created_date"),
        "updated_date": details.get("updated_date"),
        "rating": metrics.get("rating"),
        "headline_present": bool(details.get("headline")),
        "body_present": bool(details.get("comments")),
        "nickname_present": bool(details.get("nickname")),
        "location_present": bool(details.get("location")),
        "bottom_line": details.get("bottom_line"),
        "disclosure_code": details.get("disclosure_code"),
        "is_verified_buyer": badges.get("is_verified_buyer"),
        "is_verified_reviewer": badges.get("is_verified_reviewer"),
        "is_staff_reviewer": badges.get("is_staff_reviewer"),
        "helpful_votes": metrics.get("helpful_votes"),
        "not_helpful_votes": metrics.get("not_helpful_votes"),
        "helpful_score": metrics.get("helpful_score"),
        "media_count": len(_list_value(row.get("media"))),
        "property_keys": sorted(
            {
                str(prop.get("key"))
                for prop in _list_value(details.get("properties"))
                if isinstance(prop, Mapping) and prop.get("key") is not None
            }
        ),
        "product_variant": details.get("product_variant"),
        "locale": details.get("locale"),
        "raw_file": raw_file,
    }


def _question_rows(
    document: Mapping[str, Any],
    label: str,
    page_id: str,
) -> list[Mapping[str, Any]]:
    rows = _document_questions(document, label)
    total = _total_results(document, label)
    if not rows and total > 0:
        raise UltaOnboardingCaptureError(
            f"{label} returned zero rows although the source declares {total} results"
        )
    for row in rows:
        if row.get("question_id") is None and row.get("ugc_id") is None:
            raise UltaOnboardingCaptureError(
                f"{label} contains a question row without an identifier"
            )
        declared_page = str(
            _mapping_value(row.get("details")).get("product_page_id")
        )
        if declared_page != page_id:
            raise UltaOnboardingCaptureError(
                f"{label} contains a question bound to foreign "
                f"product_page_id {declared_page!r}"
            )
    return rows


def _question_row_summary(
    row: Mapping[str, Any],
    raw_file: str,
    rank: int,
) -> dict[str, Any]:
    details = _mapping_value(row.get("details"))
    answers = _list_value(row.get("answer"))
    return {
        "rank": rank,
        "question_id": str(row.get("question_id") or row.get("ugc_id")),
        "ugc_id": row.get("ugc_id"),
        "created_date": details.get("created_date"),
        "text_present": bool(details.get("text")),
        "is_seeded": details.get("is_seeded"),
        "declared_answer_count": row.get("answer_count"),
        "included_answer_rows": len(answers),
        "answer_inventory": [
            {
                "answer_id": str(
                    answer.get("answer_id") or answer.get("ugc_id")
                ),
                "author_type": _mapping_value(answer.get("details")).get(
                    "author_type"
                ),
                "is_expert": _mapping_value(answer.get("details")).get("is_expert"),
                "brand_name_present": bool(
                    _mapping_value(answer.get("details")).get("brand_name")
                ),
                "body_present": bool(
                    _mapping_value(answer.get("details")).get("text")
                ),
                "helpful_votes": _mapping_value(answer.get("metrics")).get(
                    "helpful_votes"
                ),
            }
            for answer in answers
            if isinstance(answer, Mapping)
        ],
        "raw_file": raw_file,
    }


def _loss_ledger(
    *,
    helpful_captured: int,
    recent_captured: int,
    totals: Mapping[str, int],
    included_answer_counts: Sequence[int],
    declared_answer_counts: Sequence[int],
    total_disagreement: Sequence[int],
) -> list[dict[str, str]]:
    total = max(totals.values()) if totals else 0
    ledger = [
        {
            "category": "bounded_window",
            "detail": (
                f"Helpful and Recent preserve {helpful_captured} and "
                f"{recent_captured} bounded rows of {total} declared reviews; the "
                "display route caps each response at "
                f"{POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX} rows and this is not the "
                "complete historical review corpus"
            ),
        },
        {
            "category": "incentive_semantics",
            "detail": (
                "Ulta exposes no source-proven non-incentivized filter on the "
                "display route; the unfiltered baseline is preserved with per-row "
                "disclosure_code and rollup sampling counts, and no incentive "
                "filter is applied or claimed"
            ),
        },
        {
            "category": "syndication_filter",
            "detail": (
                "the display-route native/syndicated filter parameter is "
                "unverified; rollup syndicated_review_count is preserved and no "
                "syndication filter is applied or claimed"
            ),
        },
        {
            "category": "demographics",
            "detail": (
                "Ulta returned no aggregate reviewer age/skin distributions with "
                "denominators; per-row Describe Yourself / Skin Type properties "
                "remain only in raw rows"
            ),
        },
        {
            "category": "linked_media",
            "detail": (
                "review and answer media references are preserved in raw "
                "responses; linked media bytes were not fetched"
            ),
        },
        {
            "category": "audience",
            "detail": (
                "reviewer attributes and recommendations are source observations, "
                "not a representative population estimate"
            ),
        },
    ]
    if included_answer_counts != list(declared_answer_counts):
        ledger.append(
            {
                "category": "qa_answer_inclusion",
                "detail": (
                    "at least one question declares more answers than the display "
                    "response included; declared and included counts are both "
                    "preserved"
                ),
            }
        )
    if len(total_disagreement) > 1:
        ledger.append(
            {
                "category": "in_flight_count_drift",
                "detail": (
                    "total_results disagreed across bounded responses captured in "
                    "one run; every observed value is preserved: "
                    f"{list(total_disagreement)}"
                ),
            }
        )
    return ledger


def _write_packet(
    *,
    data_root: DataLakeRoot,
    parent: UltaParentContext,
    artifacts: Sequence[tuple[str, bytes]],
    captured: Sequence[tuple[PowerReviewsRequestSpec, PowerReviewsResponse]],
    limitations: Sequence[str],
    summary: Mapping[str, Any],
):
    file_ids = staged_file_id_map(artifacts)
    captured_at = captured[-1][1].captured_at if captured else utc_now_z()
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "PowerReviews display responses do not declare one source publication time"
        ),
        source_edit_or_version=unknown_with_reason(
            "PowerReviews display responses do not declare a product-level edit version"
        ),
        capture_time=known_fact(captured_at),
        recapture_time=known_fact(captured_at),
        cutoff_posture=known_fact("post_cutoff"),
    )
    access = known_fact(
        "Ulta page-declared public PowerReviews display route attempted; exact "
        "acquired response bytes preserved"
    )
    archive = not_attempted("structured companion did not query archive/history")
    media = not_attempted("structured companion did not fetch linked review media")
    recapture = known_fact("supplement")
    return stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="ulta_powerreviews_review_qa_onboarding",
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
        source_surface=ULTA_ONBOARDING_SOURCE_SURFACE,
        source_locator=known_fact(parent.product_url),
        decision_question=(
            "What does Ulta expose through bounded PowerReviews Most Helpful, "
            "Most Recent, and Q&A display responses, and which Sephora target "
            "fields remain absent?"
        ),
        capture_context=(
            f"Ulta-specific PowerReviews structured companion from hash-verified "
            f"parent packet {parent.packet_id}; "
            f"parser={ULTA_ONBOARDING_PARSER_VERSION}"
        ),
        actor_audience_context=unknown_with_reason(
            "reviewer attributes are source-visible observations; audience "
            "representativeness is not established"
        ),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="ulta_powerreviews_onboarding_cli_operator",
        session_identity=None,
        visible_mode_changes=[
            "ulta_page_declared_powerreviews_display_config_resolved",
            "ulta_product_id_bound_to_powerreviews_page_id",
            "reviews_sort_most_helpful",
            "reviews_sort_newest",
            "questions_display_default_order",
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
            f"Ulta PowerReviews onboarding companion for {parent.url_product_id}: "
            f"{summary.get('record_kind', 'unknown result')}; exact display "
            "response bytes and a token-free request manifest are preserved."
        ),
        receipt_non_claims=[
            "not a Bazaarvoice route",
            "not a complete review corpus",
            "not a non-incentivized review population",
            "not reviewer population representativeness",
            "not linked-media preservation",
            "not review or answer body normalization or Judgment",
            "not monitoring, scheduling, or production readiness",
            "not a replacement for the parent rendered Ulta PDP packet",
        ],
    )


def _request_manifest(
    parent: UltaParentContext,
    config: PowerReviewsReadConfig,
    captured: Sequence[tuple[PowerReviewsRequestSpec, PowerReviewsResponse]],
) -> dict[str, Any]:
    return {
        "record_kind": "ulta_powerreviews_request_manifest_v1",
        "provider": "powerreviews",
        "retailer": "Ulta",
        "parent_packet_id": parent.packet_id,
        "parent_file_id": parent.dom_file_id,
        "parent_file_sha256": parent.dom_file_sha256,
        "product_url": parent.product_url,
        "ulta_product_id": parent.url_product_id,
        "powerreviews_page_id": config.page_id,
        "merchant_id": config.merchant_id,
        "merchant_group_id": config.merchant_group_id,
        "locale": config.locale,
        "display_host": config.host,
        "credential_posture": (
            "page-declared public display api key used in flight; the key and "
            "credential-bearing request URLs are not persisted"
        ),
        "requests": [
            {
                "artifact_name": spec.artifact_name,
                "endpoint": (
                    f"https://{config.host}/m/{config.merchant_id}/l/"
                    f"{config.locale}/product/{config.page_id}/{spec.resource}"
                ),
                "parameters": [
                    {
                        "name": "apikey",
                        "value": "[REDACTED_PAGE_DECLARED_PUBLIC_DISPLAY_KEY]",
                    },
                    *(
                        {"name": name, "value": value}
                        for name, value in spec.parameters
                    ),
                ],
                "response": {
                    "status": response.status,
                    "reason": response.reason or None,
                    "content_type": response.content_type,
                    "byte_count": len(response.body),
                    "captured_at": response.captured_at,
                },
            }
            for spec, response in captured
        ],
    }


def _load_document(body: bytes, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UltaOnboardingCaptureError(f"{label} is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise UltaOnboardingCaptureError(f"{label} must be a JSON object")
    return value


def _document_reviews(
    document: Mapping[str, Any],
    label: str,
) -> list[Mapping[str, Any]]:
    results = document.get("results")
    if not isinstance(results, list) or len(results) != 1:
        raise UltaOnboardingCaptureError(
            f"{label}.results must be an array with exactly one product result"
        )
    result = results[0]
    if not isinstance(result, Mapping):
        raise UltaOnboardingCaptureError(f"{label}.results[0] must be an object")
    rows = result.get("reviews")
    if not isinstance(rows, list):
        raise UltaOnboardingCaptureError(f"{label}.results[0].reviews must be an array")
    if not all(isinstance(row, Mapping) for row in rows):
        raise UltaOnboardingCaptureError(f"{label} contains a non-object review row")
    return [row for row in rows if isinstance(row, Mapping)]


def _document_questions(
    document: Mapping[str, Any],
    label: str,
) -> list[Mapping[str, Any]]:
    results = document.get("results")
    if not isinstance(results, list):
        raise UltaOnboardingCaptureError(f"{label}.results must be an array")
    if not all(isinstance(row, Mapping) for row in results):
        raise UltaOnboardingCaptureError(f"{label} contains a non-object question row")
    return [row for row in results if isinstance(row, Mapping)]


def _rollup(document: Mapping[str, Any], label: str) -> Mapping[str, Any]:
    results = document.get("results")
    if not isinstance(results, list) or not results or not isinstance(
        results[0], Mapping
    ):
        raise UltaOnboardingCaptureError(f"{label} is missing its product result")
    rollup = results[0].get("rollup")
    if not isinstance(rollup, Mapping):
        raise UltaOnboardingCaptureError(f"{label} is missing review rollup aggregates")
    return rollup


def _total_results(document: Mapping[str, Any], label: str) -> int:
    paging = document.get("paging")
    if not isinstance(paging, Mapping):
        raise UltaOnboardingCaptureError(f"{label}.paging must be an object")
    return _nonnegative_int(paging.get("total_results"), f"{label}.paging.total_results")


def _field_inventory(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    names: set[str] = set()
    for row in rows:
        for key, value in row.items():
            names.add(str(key))
            if isinstance(value, Mapping):
                names.update(f"{key}.{child}" for child in value)
    return sorted(names)


def _row_int(row: Mapping[str, Any], section: str, field: str) -> int:
    value = _mapping_value(row.get(section)).get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        raise UltaOnboardingCaptureError(
            f"review row {section}.{field} must be an integer"
        )
    return value


def _mapping_value(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise UltaOnboardingCaptureError(f"{label} must be a nonnegative integer")
    return value


def _safe_error_text(exc: Exception) -> str:
    text = str(exc)
    return re.sub(
        r"(?i)(apikey|api[_-]?key|passkey|token)=([^&\s]+)",
        r"\1=[REDACTED]",
        text,
    )[:500]


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


__all__ = [
    "DEFAULT_PAGES_PER_ROLE",
    "DEFAULT_QUESTION_LIMIT",
    "DEFAULT_REVIEW_PAGE_SIZE",
    "ULTA_ONBOARDING_PARSER_VERSION",
    "ULTA_ONBOARDING_SOURCE_SURFACE",
    "UltaOnboardingCaptureError",
    "UltaParentContext",
    "build_ulta_onboarding_summary",
    "capture_ulta_onboarding_packet",
]
