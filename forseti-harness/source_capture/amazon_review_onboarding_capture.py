"""Raw-parent-backed Amazon PDP review onboarding companion.

Amazon does not expose a clean anonymous all-reviews route in the admitted
environment.  This module therefore consumes one hash-verified, US-pinned
Amazon PDP packet and inventories only the Amazon-native review rows already
present in that exact rendered DOM.  It never labels the route Bazaarvoice,
never claims Most Helpful/Most Recent ordering, and never duplicates review
bodies into the compact companion summary.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

from data_lake.root import DataLakeRoot, LoadedRawPacket
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map


AMAZON_REVIEW_ONBOARDING_SOURCE_SURFACE = "amazon_review_onboarding"
AMAZON_REVIEW_ONBOARDING_PARSER_VERSION = "amazon_pdp_review_onboarding_v1"

_ASIN_RE = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?#]|$)", re.I)
_RATING_RE = re.compile(r"(\d+(?:\.\d+)?)\s+out of 5 stars", re.I)
_DATE_RE = re.compile(r"^Reviewed in (.+?) on ([A-Z][a-z]+ \d{1,2}, \d{4})$")
_HELPFUL_RE = re.compile(r"([\d,]+)\s+people found this helpful", re.I)
_ONE_HELPFUL_RE = re.compile(r"one person found this helpful", re.I)
_REVIEW_COUNT_RE = re.compile(r"([\d,]+)\s+global ratings", re.I)
_BAZAARVOICE_RE = re.compile(r"bazaarvoice", re.I)
_MEDIA_URL_RE = re.compile(r"https?://[^\s\"'<>),]+", re.I)
_VOID_TAGS = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
)
_SECTION_IDS = {
    "localTopReviews": "top_reviews_united_states",
    "localTopReviewsList": "top_reviews_united_states",
    "internationalTopReviews": "top_reviews_other_countries",
    "internationalTopReviewsList": "top_reviews_other_countries",
}
_EXPECTED_SECTION_LABELS = {
    "top_reviews_united_states": "Top reviews from the United States",
    "top_reviews_other_countries": "Top reviews from other countries",
}
_MEDIA_HOOKS = {"review-image-tile", "media-popover-container", "reviewRichContentContainer"}


class AmazonReviewOnboardingCaptureError(RuntimeError):
    """Fail-closed parent binding or review adaptation error."""


@dataclass(frozen=True)
class AmazonReviewParent:
    packet_id: str
    product_url: str
    asin: str
    capture_time: str
    dom_file_id: str
    dom_file_sha256: str
    dom_relative_path: str
    dom: bytes
    visible_text_file_id: str
    visible_text_sha256: str
    visible_text_relative_path: str
    visible_text: bytes
    metadata_file_id: str
    metadata_file_sha256: str
    profile_name: str


@dataclass
class _Frame:
    tag: str
    attrs: dict[str, str]
    hook: str | None = None
    special: tuple[str, str] | None = None
    text_parts: list[str] = field(default_factory=list)


class _AmazonReviewParser(HTMLParser):
    """Streaming parser for the source-labelled Amazon top-review sections."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[_Frame] = []
        self.rows: list[dict[str, Any]] = []
        self.section_labels: dict[str, str] = {}
        self.histogram: dict[str, int] = {}
        self.aplus_question_count = 0
        self._current: dict[str, Any] | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        normalized_tag = tag.lower()
        attr_map = {str(key).lower(): value or "" for key, value in attrs}
        hook = attr_map.get("data-hook") or None
        section = self._section(attr_map.get("id"))
        special: tuple[str, str] | None = None

        if normalized_tag in {"h2", "h3"} and section is not None:
            special = ("section_heading", section)
        elif normalized_tag == "a" and "filterByStar=" in attr_map.get("href", ""):
            special = (
                "histogram",
                attr_map["href"] + "\n" + attr_map.get("aria-label", ""),
            )
        elif "aplus-question" in attr_map.get("class", "").split():
            special = ("aplus_question", "")

        if hook == "review":
            if self._current is not None:
                raise AmazonReviewOnboardingCaptureError("nested Amazon review rows are unsupported")
            review_id = attr_map.get("id", "").strip()
            if not re.fullmatch(r"R[A-Z0-9]{8,}", review_id):
                raise AmazonReviewOnboardingCaptureError(
                    "Amazon review row lacks a source-native-looking review id"
                )
            if section is None:
                raise AmazonReviewOnboardingCaptureError(
                    f"Amazon review {review_id} is outside a supported top-review section"
                )
            self._current = {
                "review_id": review_id,
                "section": section,
                "hook_text": {},
                "hook_attributes": {},
                "source_hooks": set(),
                "source_attribute_names": set(attr_map),
                "media_references": set(),
            }
            special = ("review_root", review_id)

        if self._current is not None:
            self._current["source_attribute_names"].update(attr_map)
            if hook:
                self._current["source_hooks"].add(hook)
                self._current["hook_attributes"].setdefault(hook, []).append(attr_map)
            active_media = hook in _MEDIA_HOOKS or any(
                frame.hook in _MEDIA_HOOKS for frame in self.stack
            )
            if active_media:
                for value in attr_map.values():
                    for match in _MEDIA_URL_RE.findall(value):
                        self._current["media_references"].add(match)

        frame = _Frame(
            tag=normalized_tag,
            attrs=attr_map,
            hook=hook,
            special=special,
        )
        if normalized_tag not in _VOID_TAGS:
            self.stack.append(frame)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in _VOID_TAGS:
            self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if not data:
            return
        for frame in self.stack:
            if frame.special is not None:
                frame.text_parts.append(data)
        if self._current is None:
            return
        for frame in self.stack:
            if frame.hook:
                self._current["hook_text"].setdefault(frame.hook, []).append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        index = next(
            (
                index
                for index in range(len(self.stack) - 1, -1, -1)
                if self.stack[index].tag == normalized
            ),
            None,
        )
        if index is None:
            return
        popped = self.stack[index:]
        del self.stack[index:]
        for frame in reversed(popped):
            self._finalize_special(frame)

    def close(self) -> None:
        super().close()
        for frame in reversed(self.stack):
            self._finalize_special(frame)
        self.stack.clear()
        if self._current is not None:
            raise AmazonReviewOnboardingCaptureError("unterminated Amazon review row")

    def _section(self, current_id: str | None = None) -> str | None:
        if current_id in _SECTION_IDS:
            return _SECTION_IDS[current_id]
        for frame in reversed(self.stack):
            frame_id = frame.attrs.get("id")
            if frame_id in _SECTION_IDS:
                return _SECTION_IDS[frame_id]
        return None

    def _finalize_special(self, frame: _Frame) -> None:
        if frame.special is None:
            return
        kind, value = frame.special
        text = _normalize_text(" ".join(frame.text_parts))
        if kind == "section_heading" and text:
            self.section_labels[value] = text
        elif kind == "histogram":
            star_match = re.search(r"filterByStar=(one|two|three|four|five)_star", value)
            pct_match = re.search(r"(\d{1,3}) percent", value, re.I)
            if pct_match is None:
                pct_match = re.search(r"(\d{1,3})%", text)
            if star_match and pct_match:
                star = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5"}[star_match.group(1)]
                self.histogram[star] = int(pct_match.group(1))
        elif kind == "aplus_question" and text:
            self.aplus_question_count += 1
        elif kind == "review_root":
            self._finish_review(value)

    def _finish_review(self, review_id: str) -> None:
        if self._current is None or self._current["review_id"] != review_id:
            raise AmazonReviewOnboardingCaptureError("Amazon review parser lost row identity")
        current = self._current
        self._current = None
        hook_text = {
            hook: _normalize_text(" ".join(parts))
            for hook, parts in current["hook_text"].items()
        }
        title = hook_text.get("reviewTitle")
        body = hook_text.get("reviewText")
        author = hook_text.get("review-by-line")
        date_text = hook_text.get("review-date")
        rating_text = hook_text.get("review-star-rating")
        if not all((title, body, author, date_text, rating_text)):
            missing = [
                name
                for name, value in {
                    "reviewTitle": title,
                    "reviewText": body,
                    "review-by-line": author,
                    "review-date": date_text,
                    "review-star-rating": rating_text,
                }.items()
                if not value
            ]
            raise AmazonReviewOnboardingCaptureError(
                f"Amazon review {review_id} is missing required source hooks: {missing}"
            )
        rating_match = _RATING_RE.search(rating_text)
        date_match = _DATE_RE.match(date_text)
        if rating_match is None or date_match is None:
            raise AmazonReviewOnboardingCaptureError(
                f"Amazon review {review_id} has unsupported rating/date text"
            )
        source_date = datetime.strptime(date_match.group(2), "%B %d, %Y").date().isoformat()
        helpful_text = hook_text.get("helpful-vote-statement")
        helpful_count: int | None = None
        if helpful_text:
            match = _HELPFUL_RE.search(helpful_text)
            if match:
                helpful_count = int(match.group(1).replace(",", ""))
            elif _ONE_HELPFUL_RE.search(helpful_text):
                helpful_count = 1
        badge_labels = sorted(
            {
                hook_text[name]
                for name in ("review-badges", "avp-badge")
                if hook_text.get(name)
            }
        )
        incentive_labels = [
            label
            for label in badge_labels
            if re.search(r"(?i)(vine|free product|incentiv)", label)
        ]
        self.rows.append(
            {
                "review_id": review_id,
                "section": current["section"],
                "title": title,
                "body": body,
                "author": author,
                "rating": float(rating_match.group(1)),
                "rating_text": rating_text,
                "source_date": source_date,
                "source_date_text": date_text,
                "review_location": date_match.group(1),
                "variant_text": hook_text.get("product-variation-attributes"),
                "verified_purchase": (
                    True if hook_text.get("avp-badge") == "Verified Purchase" else None
                ),
                "helpful_count": helpful_count,
                "helpful_text": helpful_text,
                "badge_labels": badge_labels,
                "incentive_labels": incentive_labels,
                "media_references": sorted(current["media_references"]),
                "source_hooks": sorted(current["source_hooks"]),
                "source_attribute_names": sorted(current["source_attribute_names"]),
            }
        )


def capture_amazon_review_onboarding_packet(
    *,
    data_root: DataLakeRoot,
    parent_packet_id: str,
) -> tuple[int, dict[str, Any]]:
    """Write a compact companion over one immutable Amazon PDP parent packet."""
    if data_root.readonly:
        raise AmazonReviewOnboardingCaptureError("capture requires a writable DataLakeRoot")
    parent = _parent_context(data_root.load_raw_packet(parent_packet_id), parent_packet_id)
    summary = build_amazon_review_onboarding_summary(parent)
    control_manifest = {
        "record_kind": "amazon_review_onboarding_control_manifest_v1",
        "parser_version": AMAZON_REVIEW_ONBOARDING_PARSER_VERSION,
        "provider": "amazon_native_rendered_pdp",
        "parent_packet_id": parent.packet_id,
        "parent_dom_file_id": parent.dom_file_id,
        "parent_dom_sha256": parent.dom_file_sha256,
        "parent_visible_text_file_id": parent.visible_text_file_id,
        "parent_visible_text_sha256": parent.visible_text_sha256,
        "product_url": parent.product_url,
        "asin": parent.asin,
        "profile_name": parent.profile_name,
        "credential_posture": "no credential, token, cookie, proxy, or new source request used",
    }
    artifacts = [
        ("amazon_review_onboarding_control_manifest.json", _json_bytes(control_manifest)),
        ("amazon_review_onboarding_summary.json", _json_bytes(summary)),
    ]
    written = _write_packet(data_root=data_root, parent=parent, artifacts=artifacts, summary=summary)
    return 0, {
        "packet_id": written.packet.packet_id,
        "output_directory": written.output_directory,
        "summary": summary,
    }


def build_amazon_review_onboarding_summary(parent: AmazonReviewParent) -> dict[str, Any]:
    """Build a body-free review inventory from exact parent DOM bytes."""
    try:
        html = parent.dom.decode("utf-8")
        visible_text = parent.visible_text.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AmazonReviewOnboardingCaptureError("Amazon parent text is not UTF-8") from exc
    parser = _AmazonReviewParser()
    parser.feed(html)
    parser.close()
    if not parser.rows:
        raise AmazonReviewOnboardingCaptureError("Amazon parent exposes no supported review rows")
    review_ids = [row["review_id"] for row in parser.rows]
    if len(set(review_ids)) != len(review_ids):
        raise AmazonReviewOnboardingCaptureError("Amazon parent contains duplicate review ids")
    for section, expected in _EXPECTED_SECTION_LABELS.items():
        if any(row["section"] == section for row in parser.rows):
            observed = parser.section_labels.get(section)
            if observed != expected:
                raise AmazonReviewOnboardingCaptureError(
                    f"Amazon review section label mismatch for {section}: {observed!r}"
                )

    rating_match = _RATING_RE.search(visible_text)
    count_match = _REVIEW_COUNT_RE.search(visible_text)
    inventory: list[dict[str, Any]] = []
    section_ranks: dict[str, int] = {}
    for rank, row in enumerate(parser.rows, start=1):
        section = row["section"]
        section_ranks[section] = section_ranks.get(section, 0) + 1
        body = row["body"]
        inventory.append(
            {
                "rank": rank,
                "section_rank": section_ranks[section],
                "section": section,
                "section_label": parser.section_labels[section],
                "review_id": row["review_id"],
                "title": row["title"],
                "body_present": True,
                "body_character_count": len(body),
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "rating": row["rating"],
                "rating_text": row["rating_text"],
                "source_date": row["source_date"],
                "source_date_text": row["source_date_text"],
                "author": row["author"],
                "review_location": row["review_location"],
                "variant_text": row["variant_text"],
                "verified_purchase": row["verified_purchase"],
                "helpful_count": row["helpful_count"],
                "helpful_text": row["helpful_text"],
                "badge_labels": row["badge_labels"],
                "incentive_labels": row["incentive_labels"],
                "media_reference_count": len(row["media_references"]),
                "media_references": row["media_references"],
                "source_hooks": row["source_hooks"],
                "source_attribute_names": row["source_attribute_names"],
                "raw_anchor": {
                    "parent_packet_id": parent.packet_id,
                    "file_id": parent.dom_file_id,
                    "relative_packet_path": parent.dom_relative_path,
                    "sha256": parent.dom_file_sha256,
                    "selector": f'#{row["review_id"]}[data-hook="review"]',
                },
            }
        )

    incentive_count = sum(bool(row["incentive_labels"]) for row in parser.rows)
    context_keys = sorted(
        {
            hook
            for row in parser.rows
            for hook in row["source_hooks"]
            if re.search(r"(?i)(profile|genome|demographic|skin|age)", hook)
        }
    )
    return {
        "record_kind": "amazon_review_onboarding_summary_v1",
        "parser_version": AMAZON_REVIEW_ONBOARDING_PARSER_VERSION,
        "provider": "amazon_native_rendered_pdp",
        "parent_packet": {
            "packet_id": parent.packet_id,
            "dom_file_id": parent.dom_file_id,
            "dom_file_sha256": parent.dom_file_sha256,
            "visible_text_file_id": parent.visible_text_file_id,
            "visible_text_sha256": parent.visible_text_sha256,
        },
        "identity": {
            "retailer": "amazon",
            "asin": parent.asin,
            "product_url": parent.product_url,
            "profile_name": parent.profile_name,
            "us_delivery_pin_confirmed": True,
        },
        "review_aggregate": {
            "rating": float(rating_match.group(1)) if rating_match else None,
            "rating_count": int(count_match.group(1).replace(",", "")) if count_match else None,
            "rating_distribution_percent": dict(sorted(parser.histogram.items(), reverse=True)),
            "source": "parent Amazon PDP rendered DOM and visible text",
        },
        "reviews": {
            "source_order_claim": "amazon_pdp_top_reviews_section_order",
            "most_helpful_available": False,
            "most_recent_available": False,
            "last_seen_monitoring_anchor_available": False,
            "captured_review_rows": len(inventory),
            "captured_review_bodies_in_parent_raw": len(inventory),
            "united_states_rows": section_ranks.get("top_reviews_united_states", 0),
            "other_countries_rows": section_ranks.get("top_reviews_other_countries", 0),
            "verified_purchase_rows": sum(row["verified_purchase"] is True for row in parser.rows),
            "rows_with_helpful_count": sum(row["helpful_count"] is not None for row in parser.rows),
            "rows_with_media_references": sum(bool(row["media_references"]) for row in parser.rows),
            "rows_with_incentive_marker": incentive_count,
            "context_hook_keys": context_keys,
            "review_inventory": inventory,
        },
        "questions": {
            "product_customer_q_and_a_status": "not_exposed_on_target_pdp",
            "captured_customer_questions": 0,
            "captured_customer_answers": 0,
            "excluded_brand_authored_aplus_faq_questions": parser.aplus_question_count,
        },
        "route_classification": {
            "bazaarvoice_marker_count": len(_BAZAARVOICE_RE.findall(html)),
            "winning_route": "amazon_native_rendered_pdp",
            "deep_review_route": "not_available_in_parent; separate route probes are outside this adapter",
        },
        "extraction_target_matrix": {
            "review_aggregate": "observed",
            "review_rows": "observed_bounded_pdp_top_reviews",
            "most_helpful": "not_exposed",
            "most_recent": "not_exposed_in_parent",
            "reviewer_demographics": "not_exposed",
            "incentive_semantics": (
                "observed_on_some_rows" if incentive_count else "not_exposed_on_captured_rows"
            ),
            "product_customer_q_and_a": "not_exposed",
            "exact_raw_source": "observed_in_hash_verified_parent_dom",
        },
        "content_qualification": {
            "status": "passed",
            "provider_identity": "amazon_native_rendered_pdp",
            "product_mapping_bound": True,
            "exact_parent_raw_hash_verified": True,
            "review_ids_unique": len(set(review_ids)) == len(review_ids),
            "review_order_preserved": review_ids == [row["review_id"] for row in inventory],
            "all_captured_bodies_remain_in_parent_raw": True,
            "summary_duplicates_review_bodies": False,
        },
        "loss_ledger": [
            {
                "category": "bounded_window",
                "detail": f"The parent PDP exposes {len(inventory)} source-ordered top-review rows; this is not the complete review corpus.",
            },
            {
                "category": "sort_and_monitoring",
                "detail": "The PDP labels rows as top reviews, not Most Helpful or Most Recent; no last-seen monitoring anchor is claimed.",
            },
            {
                "category": "demographics",
                "detail": "No age, skin-type, or skin-concern distributions are exposed on the captured Amazon review rows.",
            },
            {
                "category": "questions_and_answers",
                "detail": f"No customer product Q&A is exposed; {parser.aplus_question_count} brand-authored A+ FAQ questions are excluded from customer Q&A.",
            },
            {
                "category": "linked_media",
                "detail": "Review media references remain source-visible in the parent DOM; linked media bytes were not independently fetched.",
            },
            {
                "category": "provider",
                "detail": "The winning route is Amazon-native rendered PDP content and is not Bazaarvoice.",
            },
        ],
        "raw_failure_fallback": {
            "status": "parent_already_preserved",
            "behavior": "adaptation failure writes no companion and leaves the immutable hash-verified parent packet unchanged",
        },
    }


def _parent_context(loaded: LoadedRawPacket, packet_id: str) -> AmazonReviewParent:
    manifest = loaded.manifest
    if manifest.get("source_family") != "retail_pdp" or manifest.get("source_surface") != "cloakbrowser_snapshot":
        raise AmazonReviewOnboardingCaptureError(
            f"parent packet {packet_id} must be retail_pdp/cloakbrowser_snapshot"
        )
    locator = manifest.get("source_locator")
    product_url = (
        str(locator.get("value"))
        if isinstance(locator, Mapping) and locator.get("status") == "known"
        else ""
    )
    asin = _amazon_asin(product_url)
    if asin is None:
        raise AmazonReviewOnboardingCaptureError("parent source locator is not an Amazon PDP URL")

    preserved = {
        str(item.get("file_id")): item
        for item in manifest.get("preserved_files", [])
        if isinstance(item, Mapping) and isinstance(item.get("file_id"), str)
    }
    selected: dict[str, tuple[str, Mapping[str, Any], bytes]] = {}
    suffixes = {
        "dom": "cloakbrowser_rendered_dom.html",
        "visible": "cloakbrowser_visible_text.txt",
        "metadata": "cloakbrowser_snapshot_metadata.json",
    }
    for role, suffix in suffixes.items():
        matches = [
            (file_id, item, loaded.bodies[file_id])
            for file_id, item in preserved.items()
            if str(item.get("relative_packet_path", "")).replace("\\", "/").endswith(suffix)
            and file_id in loaded.bodies
        ]
        if len(matches) != 1:
            raise AmazonReviewOnboardingCaptureError(
                f"parent packet {packet_id} requires exactly one {suffix}"
            )
        selected[role] = matches[0]

    metadata_id, metadata_item, metadata_bytes = selected["metadata"]
    try:
        metadata = json.loads(metadata_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AmazonReviewOnboardingCaptureError("Amazon parent metadata is invalid") from exc
    profile = metadata.get("retail_capture_profile")
    profile_name = profile.get("name") if isinstance(profile, Mapping) else None
    if profile_name not in {"amazon_pdp_aggregate", "amazon_pdp_distribution"}:
        raise AmazonReviewOnboardingCaptureError("Amazon parent uses an unsupported capture profile")
    if metadata.get("access_blocked") is not False or metadata.get("pin_confirmed") is not True:
        raise AmazonReviewOnboardingCaptureError("Amazon parent is access-blocked or lacks a confirmed US delivery pin")
    final_url = str(metadata.get("final_url", ""))
    if _amazon_asin(final_url) != asin or urlparse(final_url).hostname not in {"amazon.com", "www.amazon.com"}:
        raise AmazonReviewOnboardingCaptureError("Amazon parent final URL does not bind the requested ASIN on amazon.com")

    dom_id, dom_item, dom = selected["dom"]
    visible_id, visible_item, visible = selected["visible"]
    if b'name="currencyOfPreference" value="USD"' not in dom:
        raise AmazonReviewOnboardingCaptureError("Amazon parent lacks exact USD rendered evidence")
    source_slices = manifest.get("source_slices", [])
    capture_time = next(
        (
            str(item.get("timing", {}).get("capture_time", {}).get("value"))
            for item in source_slices
            if isinstance(item, Mapping)
            and item.get("timing", {}).get("capture_time", {}).get("status") == "known"
        ),
        "",
    )
    if not capture_time:
        raise AmazonReviewOnboardingCaptureError("Amazon parent capture time is unavailable")
    return AmazonReviewParent(
        packet_id=packet_id,
        product_url=product_url,
        asin=asin,
        capture_time=capture_time,
        dom_file_id=dom_id,
        dom_file_sha256=str(dom_item["sha256"]),
        dom_relative_path=str(dom_item["relative_packet_path"]),
        dom=dom,
        visible_text_file_id=visible_id,
        visible_text_sha256=str(visible_item["sha256"]),
        visible_text_relative_path=str(visible_item["relative_packet_path"]),
        visible_text=visible,
        metadata_file_id=metadata_id,
        metadata_file_sha256=str(metadata_item["sha256"]),
        profile_name=str(profile_name),
    )


def _write_packet(
    *,
    data_root: DataLakeRoot,
    parent: AmazonReviewParent,
    artifacts: Sequence[tuple[str, bytes]],
    summary: Mapping[str, Any],
):
    file_ids = staged_file_id_map(artifacts)
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("Amazon PDP has no single publication timestamp"),
        source_edit_or_version=unknown_with_reason("Amazon PDP has no declared product-level source version"),
        capture_time=known_fact(parent.capture_time),
        recapture_time=known_fact(parent.capture_time),
        cutoff_posture=known_fact("post_cutoff"),
    )
    access = known_fact("local adaptation of a hash-verified anonymous Amazon US PDP parent; no new source request")
    archive = not_attempted("Amazon review companion did not query archive/history")
    media = not_attempted("Amazon review companion did not fetch linked review media")
    recapture = known_fact("supplement")
    return stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="amazon_pdp_review_onboarding",
                locator=known_fact(parent.product_url),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                locale_pin=known_fact("US"),
                currency_pin=known_fact("USD"),
                limitations=[entry["detail"] for entry in summary["loss_ledger"]],
                warning_notes=[],
                preserved_file_ids=[file_ids[name] for name, _body in artifacts],
            )
        ],
        source_family="retail_pdp",
        source_surface=AMAZON_REVIEW_ONBOARDING_SOURCE_SURFACE,
        source_locator=known_fact(parent.product_url),
        decision_question=(
            "Which exact Amazon-native review rows, aggregate facts, and product Q&A "
            "evidence are exposed by this bounded US-pinned PDP parent?"
        ),
        capture_context=(
            f"hash-verified Amazon PDP review companion from parent {parent.packet_id}; "
            f"parser={AMAZON_REVIEW_ONBOARDING_PARSER_VERSION}"
        ),
        actor_audience_context=unknown_with_reason(
            "Amazon reviewer rows are source observations; audience representativeness is not established"
        ),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="amazon_review_onboarding_cli_operator",
        session_identity=None,
        visible_mode_changes=[],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=[entry["detail"] for entry in summary["loss_ledger"]],
        receipt_summary=(
            f"Amazon-native PDP review companion for ASIN {parent.asin}: "
            f"{summary['reviews']['captured_review_rows']} source-ordered top-review rows; "
            "bodies remain only in the exact parent DOM."
        ),
        receipt_non_claims=[
            "not Bazaarvoice",
            "not Most Helpful or Most Recent",
            "not a complete historical review corpus",
            "not product customer Q&A",
            "not reviewer population representativeness",
            "not linked-media preservation",
            "not review-body normalization or Judgment",
        ],
    )


def _amazon_asin(url: str) -> str | None:
    match = _ASIN_RE.search(url)
    return match.group(1).upper() if match else None


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


__all__ = [
    "AMAZON_REVIEW_ONBOARDING_PARSER_VERSION",
    "AMAZON_REVIEW_ONBOARDING_SOURCE_SURFACE",
    "AmazonReviewOnboardingCaptureError",
    "AmazonReviewParent",
    "build_amazon_review_onboarding_summary",
    "capture_amazon_review_onboarding_packet",
]
