from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel


FRAGRANCE_REVIEW_COVERAGE_METHOD = "fragrance_review_focused_coverage"
FRAGRANCE_REVIEW_COVERAGE_VERSION = "v0"
FRAGRANCE_REVIEW_COVERAGE_CERTIFICATION = (
    "source_visible_focused_coverage; not_cleaned; not_judgment_ready"
)

_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES = frozenset(
    {
        "action_ceiling",
        "action_supporting",
        "authenticity",
        "buyer_proof",
        "credibility",
        "decision_strength",
        "demand",
        "discount",
        "exclude",
        "excluded",
        "inclusion",
        "integrity",
        "judgment",
        "pain",
        "pleasure",
        "salience",
        "sentiment",
        "signal_use",
        "strength",
        "strong",
        "weak",
    }
)

_VOID_HTML_TAGS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)


class FragranceReviewCoverageInputError(ValueError):
    """A local review coverage input cannot be parsed without losing visibility."""


class FragranceReviewAggregateCompanion(StrictModel):
    source: Literal["pdp_json_ld", "widget_json", "absent"] = "absent"
    rating_value: float | None = None
    review_count: int | None = None
    best_rating: int | None = None
    worst_rating: int | None = None
    residuals: list[str] = Field(default_factory=list)


class FragranceReviewCoverageRow(StrictModel):
    row_id: str
    row_ordinal: int
    row_source: Literal["judgeme_widget_html", "widget_json_review", "yotpo_v3_review"]
    source_native_review_id: str | None = None
    candidate_review_key: str
    review_key_status: Literal["native_id_present", "candidate_key_only"]
    review_title_verbatim: str | None = None
    review_body_verbatim: str | None = None
    review_body_sha256: str | None = None
    review_body_word_count: int = Field(ge=0)
    review_length_bucket: Literal["lt20", "20_39", "40_74", "75_plus"]
    rating_value: int | None = None
    rating_scale: int = 5
    review_timestamp_source: str | None = None
    review_month: str | None = None
    reviewer_display_label: str | None = None
    verified_purchase_flag: bool | None = None
    media_attached_flag: bool = False
    helpful_positive_count: int | None = None
    helpful_negative_count: int | None = None
    source_app_label: str | None = None
    transparency_badge_type: str | None = None
    product_title: str | None = None
    product_url: str | None = None
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    selected_for_reader: bool = False
    selection_reasons: list[str] = Field(default_factory=list)
    skip_reasons: list[str] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_interpretation_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "fragrance review coverage source_visible_fields may carry source facts only; "
                f"forbidden interpretation field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_body_hash(self) -> "FragranceReviewCoverageRow":
        if self.review_body_verbatim and not self.review_body_sha256:
            raise ValueError("review_body_sha256 is required when review_body_verbatim is present")
        return self


class FragranceReviewCoverageSummary(StrictModel):
    total_rows: int = Field(ge=0)
    widget_total_count: int | None = None
    selected_count: int = Field(ge=0)
    skipped_count: int = Field(ge=0)
    rating_counts: dict[str, int] = Field(default_factory=dict)
    month_counts: dict[str, int] = Field(default_factory=dict)
    length_counts: dict[str, int] = Field(default_factory=dict)
    native_review_id_count: int = Field(ge=0)
    verified_true_count: int = Field(ge=0)
    media_true_count: int = Field(ge=0)
    review_body_captured_count: int = Field(ge=0)
    review_body_absent_count: int = Field(ge=0)
    selected_review_body_absent_count: int = Field(ge=0)
    source_media_filter_count: int | None = None


class FragranceReviewCoverageReceipt(StrictModel):
    coverage_method: Literal["fragrance_review_focused_coverage"] = FRAGRANCE_REVIEW_COVERAGE_METHOD
    coverage_version: Literal["v0"] = FRAGRANCE_REVIEW_COVERAGE_VERSION
    certification: Literal["source_visible_focused_coverage; not_cleaned; not_judgment_ready"] = (
        FRAGRANCE_REVIEW_COVERAGE_CERTIFICATION
    )
    source_id: str
    source_site: str
    product_url: str
    widget_route: dict[str, Any | None] = Field(default_factory=dict)
    aggregate_companion: FragranceReviewAggregateCompanion
    coverage_summary: FragranceReviewCoverageSummary
    rows: list[FragranceReviewCoverageRow] = Field(default_factory=list)
    selected_row_ids: list[str] = Field(default_factory=list)
    skipped_row_ids: list[str] = Field(default_factory=list)
    route_health: list[str] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(
        default_factory=lambda: [
            "not source-wide review coverage",
            "not a full public review archive",
            "not durable Attachment Records",
            "not ECR, Cleaning, Judgment, pain/pleasure labeling, or review-integrity scoring",
        ]
    )


@dataclass
class _MutableReview:
    attrs: dict[str, str]
    ordinal: int
    row_source: Literal["judgeme_widget_html", "widget_json_review", "yotpo_v3_review"]
    text: dict[str, list[str]] = field(default_factory=lambda: {"title": [], "body": [], "author": [], "timestamp": []})
    rating_value: int | None = None
    timestamp_source: str | None = None
    media_attached: bool = False
    helpful_positive_count: int | None = None
    helpful_negative_count: int | None = None
    transparency_badge_type: str | None = None


@dataclass
class _Frame:
    text_targets: tuple[str, ...] = ()
    media_container: bool = False


class _JudgeMeReviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.reviews: list[_MutableReview] = []
        self._current: _MutableReview | None = None
        self._depth = 0
        self._frames: list[_Frame] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_name = tag.lower()
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        classes = set(attrs_dict.get("class", "").split())

        if self._current is None:
            if tag_name == "div" and "jdgm-rev" in classes:
                self._current = _MutableReview(
                    attrs=attrs_dict,
                    ordinal=len(self.reviews) + 1,
                    row_source="judgeme_widget_html",
                )
                self._depth = 1
                self._frames = [_Frame()]
                self._capture_attrs(tag_name, attrs_dict, classes)
            return

        parent_media = any(frame.media_container for frame in self._frames)
        media_container = parent_media or bool(
            classes
            & {
                "jdgm-rev__pics",
                "jdgm-rev__pic",
                "jdgm-rev__pic-link",
                "jdgm-rev__vids",
                "jdgm-rev__video",
            }
        )
        if media_container and tag_name in {"img", "picture", "source", "video"}:
            self._current.media_attached = True

        if tag_name in _VOID_HTML_TAGS:
            self._capture_attrs(tag_name, attrs_dict, classes)
            return

        self._depth += 1
        self._frames.append(_Frame(text_targets=_text_targets(classes), media_container=media_container))
        self._capture_attrs(tag_name, attrs_dict, classes)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in _VOID_HTML_TAGS:
            self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._current is None:
            return
        if not data.strip():
            return
        for frame in self._frames:
            for target in frame.text_targets:
                self._current.text[target].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._current is None:
            return
        if self._depth == 1:
            self.reviews.append(self._current)
            self._current = None
            self._frames = []
            self._depth = 0
            return
        if self._frames:
            self._frames.pop()
        self._depth -= 1

    def _capture_attrs(self, tag: str, attrs: Mapping[str, str], classes: set[str]) -> None:
        if self._current is None:
            return
        rating = attrs.get("data-score")
        if rating is not None and ("jdgm-rev__rating" in classes or self._current.rating_value is None):
            self._current.rating_value = _int_or_none(rating)
        timestamp = attrs.get("data-content")
        if timestamp and "jdgm-rev__timestamp" in classes:
            self._current.timestamp_source = timestamp
        if attrs.get("data-thumb-up-count") is not None:
            self._current.helpful_positive_count = _int_or_none(attrs.get("data-thumb-up-count"))
        if attrs.get("data-thumb-down-count") is not None:
            self._current.helpful_negative_count = _int_or_none(attrs.get("data-thumb-down-count"))
        badge = attrs.get("data-badge-type")
        if badge:
            self._current.transparency_badge_type = badge


class _JsonLdScriptParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._in_json_ld = False
        self._buffer: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "script":
            return
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        if attrs_dict.get("type", "").lower() == "application/ld+json":
            self._in_json_ld = True
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_json_ld:
            self.scripts.append("".join(self._buffer))
            self._in_json_ld = False
            self._buffer = []


class _TextOnlyHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip_depth and data.strip():
            self.parts.append(data)

    def text(self) -> str:
        return _compact_text(" ".join(self.parts))

def build_fragrance_review_coverage_from_files(
    *,
    widget_response_paths: Sequence[Path],
    pdp_html_path: Path | None = None,
    source_id: str,
    source_site: str,
    product_url: str,
    widget_route: Mapping[str, Any | None] | None = None,
    as_of_date: date | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
) -> FragranceReviewCoverageReceipt:
    widget_responses = [path.read_text(encoding="utf-8") for path in widget_response_paths]
    pdp_html = pdp_html_path.read_text(encoding="utf-8") if pdp_html_path else None
    return build_fragrance_review_coverage(
        widget_responses=widget_responses,
        pdp_html=pdp_html,
        source_id=source_id,
        source_site=source_site,
        product_url=product_url,
        widget_route=widget_route,
        as_of_date=as_of_date,
        max_selected_rows=max_selected_rows,
        source_media_filter_count=source_media_filter_count,
    )

def write_fragrance_review_coverage(
    *,
    widget_response_paths: Sequence[Path],
    output_path: Path,
    pdp_html_path: Path | None = None,
    source_id: str,
    source_site: str,
    product_url: str,
    widget_route: Mapping[str, Any | None] | None = None,
    as_of_date: date | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
) -> FragranceReviewCoverageReceipt:
    receipt = build_fragrance_review_coverage_from_files(
        widget_response_paths=widget_response_paths,
        pdp_html_path=pdp_html_path,
        source_id=source_id,
        source_site=source_site,
        product_url=product_url,
        widget_route=widget_route,
        as_of_date=as_of_date,
        max_selected_rows=max_selected_rows,
        source_media_filter_count=source_media_filter_count,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"{json.dumps(receipt.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return receipt

def build_fragrance_review_coverage(
    *,
    widget_responses: Sequence[str],
    pdp_html: str | None = None,
    source_id: str,
    source_site: str,
    product_url: str,
    widget_route: Mapping[str, Any | None] | None = None,
    as_of_date: date | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
) -> FragranceReviewCoverageReceipt:
    route_health: list[str] = []
    residuals: list[str] = []
    raw_reviews: list[_MutableReview] = []
    widget_total_count: int | None = None
    widget_aggregate: FragranceReviewAggregateCompanion | None = None

    for index, raw_response in enumerate(widget_responses, start=1):
        try:
            parsed = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise FragranceReviewCoverageInputError(f"widget response {index} is not parseable JSON") from exc
        if not isinstance(parsed, dict):
            raise FragranceReviewCoverageInputError(f"widget response {index} is not a JSON object")
        parsed_total_count = _widget_total_count_from_response(parsed)
        if parsed_total_count is not None:
            widget_total_count = max(widget_total_count or 0, parsed_total_count)
        parsed_aggregate = _widget_aggregate_from_response(parsed)
        if parsed_aggregate is not None:
            widget_aggregate = parsed_aggregate
        if isinstance(parsed.get("html"), str):
            route_health.append(f"widget_response_{index}:html_present")
            raw_reviews.extend(_parse_judgeme_html_reviews(parsed["html"]))
        elif isinstance(parsed.get("reviews"), list):
            route_health.append(f"widget_response_{index}:reviews_json_present")
            raw_reviews.extend(
                _parse_json_reviews(
                    parsed["reviews"],
                    start_ordinal=len(raw_reviews) + 1,
                    row_source=_json_review_row_source(parsed),
                )
            )
        else:
            residuals.append(f"widget_response_{index}:review_rows_absent")

    rows = _dedupe_rows(
        _normalize_reviews(
            raw_reviews,
            source_id=source_id,
            product_url=product_url,
        )
    )
    selected_rows = _apply_selection_policy(
        rows,
        as_of_date=as_of_date or date.today(),
        max_selected_rows=max_selected_rows,
    )

    aggregate = _aggregate_from_pdp_html(pdp_html) if pdp_html is not None else FragranceReviewAggregateCompanion()
    if aggregate.source == "absent" and widget_aggregate is not None:
        aggregate = widget_aggregate
    if aggregate.source == "absent":
        residuals.append("aggregate_companion_absent")
    if widget_total_count is not None:
        route_health.append("widget_total_count_present")
    elif rows:
        residuals.append("widget_total_count_absent_completeness_unverified")
    if widget_total_count is not None and widget_total_count != len(rows):
        residuals.append("widget_total_count_deduped_row_count_mismatch")
    if any(_product_url_mismatch(row.product_url, product_url) for row in rows):
        residuals.append("review_product_url_mismatch")
    if (
        widget_total_count is not None
        and aggregate.review_count is not None
        and aggregate.review_count != widget_total_count
    ):
        residuals.append("aggregate_review_count_widget_total_count_mismatch")
    if rows and all(row.source_native_review_id for row in rows):
        route_health.append("native_review_ids_present")
    if rows and all(row.rating_value is not None for row in rows):
        route_health.append("ratings_present")
    if rows and all(row.review_month is not None for row in rows):
        route_health.append("review_months_present")
    media_true_count = sum(1 for row in rows if row.media_attached_flag)
    if source_media_filter_count == 0:
        if media_true_count:
            residuals.append("media_filter_row_scan_mismatch")
        else:
            route_health.append("media_absence_confirmed_by_filter_and_rows")
    elif source_media_filter_count is not None and source_media_filter_count > 0 and media_true_count == 0:
        residuals.append("media_filter_row_scan_mismatch")

    summary = _coverage_summary(
        selected_rows,
        widget_total_count=widget_total_count,
        source_media_filter_count=source_media_filter_count,
    )
    if summary.review_body_absent_count:
        residuals.append("review_body_absent_rows_present")
    if summary.selected_review_body_absent_count:
        residuals.append("selected_review_body_absent_rows_present")
    return FragranceReviewCoverageReceipt(
        source_id=source_id,
        source_site=source_site,
        product_url=product_url,
        widget_route=dict(widget_route or {}),
        aggregate_companion=aggregate,
        coverage_summary=summary,
        rows=selected_rows,
        selected_row_ids=[row.row_id for row in selected_rows if row.selected_for_reader],
        skipped_row_ids=[row.row_id for row in selected_rows if not row.selected_for_reader],
        route_health=route_health,
        residuals=residuals,
    )

def _parse_judgeme_html_reviews(html: str) -> list[_MutableReview]:
    parser = _JudgeMeReviewParser()
    parser.feed(html)
    return parser.reviews

def _parse_json_reviews(
    reviews: Sequence[object],
    *,
    start_ordinal: int,
    row_source: Literal["widget_json_review", "yotpo_v3_review"] = "widget_json_review",
) -> list[_MutableReview]:
    parsed: list[_MutableReview] = []
    for offset, item in enumerate(reviews):
        if not isinstance(item, Mapping):
            continue
        native_id = item.get("id") or item.get("review_id") or item.get("uuid") or item.get("sourceReviewId")
        verified = item.get("verified_buyer")
        if verified is None:
            verified = item.get("verifiedBuyer")
        user = item.get("user") if isinstance(item.get("user"), Mapping) else {}
        attrs = {
            "data-review-id": _string_or_empty(native_id),
            "data-verified-buyer": _string_or_empty(verified),
            "data-product-title": _string_or_empty(item.get("product_title")),
            "data-product-url": _string_or_empty(item.get("product_url")),
        }
        body = item.get("body") or item.get("content")
        if item.get("body_html") is not None:
            html_body = _html_to_text(_string_or_empty(item.get("body_html")))
            if html_body:
                body = html_body
        review = _MutableReview(
            attrs=attrs,
            ordinal=start_ordinal + offset,
            row_source=row_source,
            rating_value=_int_or_none(item.get("rating") or item.get("score")),
            timestamp_source=_string_or_none(item.get("created_at") or item.get("createdAt") or item.get("date")),
            media_attached=_json_review_has_media(item),
            helpful_positive_count=_int_or_none(item.get("thumb_up") or item.get("votesUp")),
            helpful_negative_count=_int_or_none(item.get("thumb_down") or item.get("votesDown")),
        )
        review.text["title"].append(_string_or_empty(item.get("title")))
        review.text["body"].append(_string_or_empty(body))
        review.text["author"].append(
            _string_or_empty(item.get("reviewer_name") or item.get("user_name") or user.get("displayName"))
        )
        badges = item.get("transparency_badges")
        if isinstance(badges, list) and badges:
            review.transparency_badge_type = _string_or_none(badges[0])
        parsed.append(review)
    return parsed

def _normalize_reviews(
    reviews: Sequence[_MutableReview],
    *,
    source_id: str,
    product_url: str,
) -> list[FragranceReviewCoverageRow]:
    rows: list[FragranceReviewCoverageRow] = []
    for review in reviews:
        ordinal = review.ordinal
        body = _compact_text(" ".join(review.text["body"]))
        title = _compact_text(" ".join(review.text["title"])) or None
        author = _compact_text(" ".join(review.text["author"])) or None
        timestamp = review.timestamp_source or _compact_text(" ".join(review.text["timestamp"])) or None
        body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest() if body else None
        candidate_key = _candidate_review_key(
            source_id=source_id,
            product_url=product_url,
            ordinal=ordinal,
            timestamp=timestamp,
            author=author,
            rating=review.rating_value,
            body_hash=body_hash,
        )
        native_id = review.attrs.get("data-review-id") or None
        row_id = _row_token(native_id or candidate_key)
        word_count = _word_count(body)
        verified = _bool_or_none(review.attrs.get("data-verified-buyer"))
        source_visible_fields = {
            key: value
            for key, value in {
                "source_widget": _source_widget_label(review.row_source),
                "data_review_id": native_id,
                "data_verified_buyer": verified,
                "data_product_title": review.attrs.get("data-product-title") or None,
                "data_product_url": review.attrs.get("data-product-url") or None,
                "data_badge_type": review.transparency_badge_type,
            }.items()
            if value is not None
        }
        residuals = [] if body else ["review_body_absent"]
        if not native_id:
            source_visible_fields["candidate_key_basis"] = {
                "source_id": source_id,
                "product_url": product_url,
                "row_ordinal": ordinal,
                "review_timestamp_source": timestamp,
                "reviewer_display_label": author,
                "rating_value": review.rating_value,
                "review_body_sha256": body_hash,
            }
            residuals.append("candidate_key_only_weaker_than_native_id")
        rows.append(
            FragranceReviewCoverageRow(
                row_id=row_id,
                row_ordinal=ordinal,
                row_source=review.row_source,
                source_native_review_id=native_id,
                candidate_review_key=candidate_key,
                review_key_status="native_id_present" if native_id else "candidate_key_only",
                review_title_verbatim=title,
                review_body_verbatim=body or None,
                review_body_sha256=body_hash,
                review_body_word_count=word_count,
                review_length_bucket=_length_bucket(word_count),
                rating_value=review.rating_value,
                review_timestamp_source=timestamp,
                review_month=_review_month(timestamp),
                reviewer_display_label=author,
                verified_purchase_flag=verified,
                media_attached_flag=review.media_attached,
                helpful_positive_count=review.helpful_positive_count,
                helpful_negative_count=review.helpful_negative_count,
                transparency_badge_type=review.transparency_badge_type,
                product_title=review.attrs.get("data-product-title") or None,
                product_url=review.attrs.get("data-product-url") or None,
                source_visible_fields=source_visible_fields,
                residuals=residuals,
            )
        )
    return rows

def _dedupe_rows(rows: Sequence[FragranceReviewCoverageRow]) -> list[FragranceReviewCoverageRow]:
    deduped: list[FragranceReviewCoverageRow] = []
    seen: set[str] = set()
    for row in rows:
        key = row.source_native_review_id or row.candidate_review_key
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped

def _apply_selection_policy(
    rows: Sequence[FragranceReviewCoverageRow],
    *,
    as_of_date: date,
    max_selected_rows: int | None,
) -> list[FragranceReviewCoverageRow]:
    has_one_star = any(row.rating_value == 1 for row in rows)
    selected_ids: set[str] = set()
    rows_with_reasons: list[FragranceReviewCoverageRow] = []
    for row in rows:
        reasons = _selection_reasons(row, as_of_date=as_of_date, has_one_star=has_one_star)
        selected = bool(reasons)
        updated = row.model_copy(
            update={
                "selected_for_reader": selected,
                "selection_reasons": reasons,
                "skip_reasons": [] if selected else ["below_focused_policy_threshold"],
                "review_title_verbatim": row.review_title_verbatim if selected else None,
                "review_body_verbatim": row.review_body_verbatim if selected else None,
            }
        )
        rows_with_reasons.append(updated)
        if selected:
            selected_ids.add(updated.row_id)

    if max_selected_rows is not None and len(selected_ids) > max_selected_rows:
        kept = {
            row.row_id
            for row in sorted(
                (row for row in rows_with_reasons if row.selected_for_reader),
                key=lambda item: _selection_priority(item, as_of_date=as_of_date),
            )[:max_selected_rows]
        }
        capped: list[FragranceReviewCoverageRow] = []
        for row in rows_with_reasons:
            if row.selected_for_reader and row.row_id not in kept:
                capped.append(
                    row.model_copy(
                        update={
                            "selected_for_reader": False,
                            "skip_reasons": ["adaptive_cap_excluded"],
                            "review_title_verbatim": None,
                            "review_body_verbatim": None,
                        }
                    )
                )
            else:
                capped.append(row)
        rows_with_reasons = capped

    return rows_with_reasons

def _selection_reasons(
    row: FragranceReviewCoverageRow,
    *,
    as_of_date: date,
    has_one_star: bool,
) -> list[str]:
    reasons: list[str] = []
    recent = _is_recent(row.review_month, as_of_date=as_of_date, months=12)
    if row.rating_value == 1:
        reasons.append("core_rating_1")
    if row.rating_value == 4:
        reasons.append("core_rating_4")
    if row.media_attached_flag:
        reasons.append("review_media_attached")
    if row.review_body_word_count >= 75:
        reasons.append("length_75_plus")
    if row.rating_value in {2, 3} and (recent or row.review_body_word_count >= 75):
        reasons.append("control_rating_2_3_recent_or_75_plus")
    if row.rating_value == 2 and not has_one_star and recent and "recent_low_rating_without_1_star" not in reasons:
        reasons.append("recent_low_rating_without_1_star")
    if row.rating_value == 5 and (recent or row.review_body_word_count >= 75):
        reasons.append("rating_5_recent_or_75_plus")
    if recent and reasons:
        reasons.append("recent_12m")
    return reasons

def _selection_priority(row: FragranceReviewCoverageRow, *, as_of_date: date) -> tuple[int, int, int, str]:
    reason_priority = {
        "core_rating_1": 0,
        "core_rating_4": 1,
        "review_media_attached": 2,
        "length_75_plus": 3,
        "recent_low_rating_without_1_star": 4,
        "rating_5_recent_or_75_plus": 6,
        "control_rating_2_3_recent_or_75_plus": 7,
        "recent_12m": 8,
    }
    priority = min((reason_priority.get(reason, 9) for reason in row.selection_reasons), default=9)
    verified_rank = 0 if row.verified_purchase_flag is True else 1
    month_rank = -_month_index(row.review_month) if row.review_month else 0
    return (priority, verified_rank, month_rank, row.row_id)

def _coverage_summary(
    rows: Sequence[FragranceReviewCoverageRow],
    *,
    widget_total_count: int | None,
    source_media_filter_count: int | None,
) -> FragranceReviewCoverageSummary:
    selected_count = sum(1 for row in rows if row.selected_for_reader)
    rating_counts = Counter(str(row.rating_value) for row in rows if row.rating_value is not None)
    month_counts = Counter(row.review_month for row in rows if row.review_month)
    length_counts = Counter(row.review_length_bucket for row in rows)
    return FragranceReviewCoverageSummary(
        total_rows=len(rows),
        widget_total_count=widget_total_count,
        selected_count=selected_count,
        skipped_count=len(rows) - selected_count,
        rating_counts=dict(sorted(rating_counts.items())),
        month_counts=dict(sorted(month_counts.items())),
        length_counts=dict(sorted(length_counts.items())),
        native_review_id_count=sum(1 for row in rows if row.source_native_review_id),
        verified_true_count=sum(1 for row in rows if row.verified_purchase_flag is True),
        media_true_count=sum(1 for row in rows if row.media_attached_flag),
        review_body_captured_count=sum(1 for row in rows if row.review_body_sha256),
        review_body_absent_count=sum(1 for row in rows if not row.review_body_sha256),
        selected_review_body_absent_count=sum(
            1 for row in rows if row.selected_for_reader and not row.review_body_sha256
        ),
        source_media_filter_count=source_media_filter_count,
    )

def _aggregate_from_pdp_html(pdp_html: str | None) -> FragranceReviewAggregateCompanion:
    if not pdp_html:
        return FragranceReviewAggregateCompanion(residuals=["pdp_html_absent"])
    parser = _JsonLdScriptParser()
    parser.feed(pdp_html)
    residuals: list[str] = []
    for script in parser.scripts:
        try:
            parsed = json.loads(script.strip())
        except json.JSONDecodeError:
            residuals.append("json_ld_parse_error")
            continue
        for item in _walk_dicts(parsed):
            aggregate = item.get("aggregateRating")
            if isinstance(aggregate, Mapping):
                return FragranceReviewAggregateCompanion(
                    source="pdp_json_ld",
                    rating_value=_float_or_none(aggregate.get("ratingValue")),
                    review_count=_int_or_none(aggregate.get("reviewCount")),
                    best_rating=_int_or_none(aggregate.get("bestRating")),
                    worst_rating=_int_or_none(aggregate.get("worstRating")),
                    residuals=list(residuals),
                )
    residuals.append("aggregate_rating_absent")
    return FragranceReviewAggregateCompanion(residuals=residuals)

def _widget_total_count_from_response(parsed: Mapping[str, object]) -> int | None:
    for key in ("total_count", "number_of_reviews"):
        value = _int_or_none(parsed.get(key))
        if value is not None:
            return value
    pagination = parsed.get("pagination")
    if isinstance(pagination, Mapping):
        value = _int_or_none(pagination.get("total"))
        if value is not None:
            return value
    bottomline = parsed.get("bottomline")
    if isinstance(bottomline, Mapping):
        for key in ("totalReview", "totalReviews"):
            value = _int_or_none(bottomline.get(key))
            if value is not None:
                return value
    return None

def _widget_aggregate_from_response(parsed: Mapping[str, object]) -> FragranceReviewAggregateCompanion | None:
    if parsed.get("average_rating") is not None or parsed.get("number_of_reviews") is not None:
        return FragranceReviewAggregateCompanion(
            source="widget_json",
            rating_value=_float_or_none(parsed.get("average_rating")),
            review_count=_int_or_none(parsed.get("number_of_reviews")),
        )
    bottomline = parsed.get("bottomline")
    if isinstance(bottomline, Mapping):
        return FragranceReviewAggregateCompanion(
            source="widget_json",
            rating_value=_float_or_none(bottomline.get("averageScore")),
            review_count=_int_or_none(bottomline.get("totalReview") or bottomline.get("totalReviews")),
        )
    return None

def _json_review_row_source(parsed: Mapping[str, object]) -> Literal["widget_json_review", "yotpo_v3_review"]:
    if isinstance(parsed.get("bottomline"), Mapping) and isinstance(parsed.get("pagination"), Mapping):
        return "yotpo_v3_review"
    return "widget_json_review"

def _json_review_has_media(item: Mapping[str, object]) -> bool:
    for key in (
        "pictures",
        "pictures_urls",
        "videos",
        "video_external_ids",
        "imagesData",
        "videosData",
        "media_platform_hosted_video_infos",
    ):
        value = item.get(key)
        if isinstance(value, list) and value:
            return True
    return False

def _html_to_text(html: str) -> str:
    parser = _TextOnlyHtmlParser()
    parser.feed(html)
    return parser.text()

def _product_url_mismatch(row_url: str | None, target_url: str) -> bool:
    if not row_url:
        return False
    row_text = row_url.strip()
    if not row_text:
        return False
    target = urlparse(target_url)
    row = urlparse(row_text)
    if row.netloc and target.netloc and row.netloc.lower() != target.netloc.lower():
        return True
    row_path = row.path if row.scheme or row.netloc else row_text.split("?", 1)[0].split("#", 1)[0]
    target_path = target.path
    if not row_path or not target_path:
        return False
    return row_path.rstrip("/") != target_path.rstrip("/")

def _source_widget_label(row_source: str) -> str:
    if row_source == "yotpo_v3_review":
        return "yotpo"
    return "judge_me"

def _walk_dicts(value: object) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(_walk_dicts(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_walk_dicts(child))
    return found

def _text_targets(classes: set[str]) -> tuple[str, ...]:
    targets: list[str] = []
    if "jdgm-rev__title" in classes:
        targets.append("title")
    if "jdgm-rev__body" in classes:
        targets.append("body")
    if "jdgm-rev__author" in classes:
        targets.append("author")
    if "jdgm-rev__timestamp" in classes:
        targets.append("timestamp")
    return tuple(targets)

def _candidate_review_key(
    *,
    source_id: str,
    product_url: str,
    ordinal: int,
    timestamp: str | None,
    author: str | None,
    rating: int | None,
    body_hash: str | None,
) -> str:
    basis = "|".join(
        [
            source_id,
            product_url,
            str(ordinal),
            timestamp or "",
            author or "",
            str(rating) if rating is not None else "",
            body_hash or "",
        ]
    )
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()

def _review_month(timestamp: str | None) -> str | None:
    if timestamp is None:
        return None
    match = re.search(r"\b(\d{4})-(\d{2})\b", timestamp)
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    return None

def _is_recent(review_month: str | None, *, as_of_date: date, months: int) -> bool:
    if review_month is None:
        return False
    delta = _month_index(f"{as_of_date.year:04d}-{as_of_date.month:02d}") - _month_index(review_month)
    return 0 <= delta <= months

def _month_index(review_month: str | None) -> int:
    if not review_month:
        return -1
    year, month = review_month.split("-", 1)
    return int(year) * 12 + int(month)

def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))

def _length_bucket(word_count: int) -> Literal["lt20", "20_39", "40_74", "75_plus"]:
    if word_count < 20:
        return "lt20"
    if word_count < 40:
        return "20_39"
    if word_count < 75:
        return "40_74"
    return "75_plus"

def _compact_text(text: str) -> str:
    return " ".join(text.split())

def _bool_or_none(value: object) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    return None

def _int_or_none(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).replace(",", "")))
    except (TypeError, ValueError):
        return None

def _float_or_none(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None

def _string_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None

def _string_or_empty(value: object) -> str:
    return "" if value is None else str(value)

def _row_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", value) or "unknown"

def _is_forbidden_field_name(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(
        token == normalized or normalized.startswith(f"{token}_")
        for token in _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES
    )

def parse_as_of_date(value: str | None) -> date | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--as-of-date must be YYYY-MM-DD") from exc


__all__ = [
    "FRAGRANCE_REVIEW_COVERAGE_CERTIFICATION",
    "FRAGRANCE_REVIEW_COVERAGE_METHOD",
    "FRAGRANCE_REVIEW_COVERAGE_VERSION",
    "FragranceReviewAggregateCompanion",
    "FragranceReviewCoverageInputError",
    "FragranceReviewCoverageReceipt",
    "FragranceReviewCoverageRow",
    "FragranceReviewCoverageSummary",
    "build_fragrance_review_coverage",
    "build_fragrance_review_coverage_from_files",
    "parse_as_of_date",
    "write_fragrance_review_coverage",
]
