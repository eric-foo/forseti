from __future__ import annotations

import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urlparse


_VIEWED_COUNT_RE = re.compile(r"You have viewed\s+(?P<viewed>\d+)\s+of\s+(?P<total>\d+)", re.IGNORECASE)
_RATING_RE = re.compile(
    r"(?P<rating>\d+(?:\.\d+)?)\s+out of 5 stars\s*;\s*"
    r"(?P<reviews>\d[\d,]*)\s+reviews?",
    re.IGNORECASE,
)
_VARIANT_RE = re.compile(r"(?P<count>\d+)\s+(?:colou?rs?|sizes?)", re.IGNORECASE)
_PRODUCT_ID_RE = re.compile(r"-([A-Za-z][A-Za-z0-9]*\d+)$")
_VOID_TAGS = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
)
# Ulta serializes stale continuation state (for example an earlier
# `productsViewedLabel`) inside `<script id="apollo_state">`. That CDATA is not
# rendered text, so it must never reach the visible-text or card captures.
_NON_RENDERED_TEXT_TAGS = frozenset({"script", "style"})


class UltaBrandGridStateError(ValueError):
    """The rendered Ulta brand grid could not be parsed deterministically."""


@dataclass(frozen=True)
class UltaBrandGridCard:
    grid_position: int
    source_product_id: str | None
    selected_sku_id: str | None
    product_url: str | None
    brand_name: str | None
    name: str | None
    price_display: str | None
    average_rating: str | None
    review_count: int | None
    visible_variant_count: int | None
    visible_variant_label: str | None
    badges: tuple[str, ...]


@dataclass(frozen=True)
class UltaBrandGridState:
    brand_name: str | None
    viewed_count: int | None
    declared_count: int | None
    cards: tuple[UltaBrandGridCard, ...]
    load_more_control_present: bool
    explicit_currency_codes: tuple[str, ...]


@dataclass
class _CardBuilder:
    grid_position: int
    selected_sku_id: str | None
    product_url: str | None = None
    brand_name: str | None = None
    name: str | None = None
    price_display: str | None = None
    rating_text: str | None = None
    variant_text: str | None = None
    badges: list[str] = field(default_factory=list)


@dataclass
class _Capture:
    field_name: str
    tag: str
    depth: int
    parts: list[str] = field(default_factory=list)


class _UltaBrandGridParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.current_card: _CardBuilder | None = None
        self.card_start_depth: int | None = None
        self.captures: list[_Capture] = []
        self.cards: list[UltaBrandGridCard] = []
        self.visible_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.h1_depth: int | None = None
        self.load_more_control_present = False
        self.explicit_currency_codes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered_tag = tag.lower()
        attributes = {key.lower(): value or "" for key, value in attrs}
        if lowered_tag not in _VOID_TAGS:
            self.stack.append(lowered_tag)
        depth = len(self.stack)
        currency = attributes.get("data-currency", "").strip()
        if currency:
            self.explicit_currency_codes.append(currency)

        if (
            self.current_card is None
            and lowered_tag == "li"
            and attributes.get("data-test") == "products-list-item"
        ):
            self.current_card = _CardBuilder(
                grid_position=len(self.cards) + 1,
                selected_sku_id=attributes.get("data-sku-id") or None,
            )
            self.card_start_depth = depth
            return

        if self.current_card is not None:
            href = attributes.get("href")
            if lowered_tag == "a" and href and "/p/" in href and self.current_card.product_url is None:
                self.current_card.product_url = (
                    f"https://www.ulta.com{href}" if href.startswith("/") else href
                )
            field_name = _capture_field(attributes.get("class", ""))
            if field_name is not None:
                self.captures.append(_Capture(field_name=field_name, tag=lowered_tag, depth=depth))
            return

        if lowered_tag == "h1" and self.h1_depth is None:
            self.h1_depth = depth
        if lowered_tag == "button" and "LoadContent__button" in _class_tokens(attributes.get("class", "")):
            self.load_more_control_present = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self.stack and self.stack[-1] in _NON_RENDERED_TEXT_TAGS:
            return
        text = " ".join(data.split())
        if not text:
            return
        self.visible_parts.append(text)
        if self.h1_depth is not None:
            self.h1_parts.append(text)
        for capture in self.captures:
            capture.parts.append(text)

    def handle_endtag(self, tag: str) -> None:
        lowered_tag = tag.lower()
        depth = len(self.stack)
        for capture in list(self.captures):
            if capture.tag == lowered_tag and capture.depth == depth:
                self._finish_capture(capture)
                self.captures.remove(capture)
        if self.h1_depth == depth and lowered_tag == "h1":
            self.h1_depth = None
        if self.current_card is not None and lowered_tag == "li" and self.card_start_depth == depth:
            self.cards.append(_finish_card(self.current_card))
            self.current_card = None
            self.card_start_depth = None
            self.captures.clear()
        if self.stack:
            if self.stack[-1] == lowered_tag:
                self.stack.pop()
            elif lowered_tag in self.stack:
                match_index = len(self.stack) - 1 - self.stack[::-1].index(lowered_tag)
                del self.stack[match_index:]

    def _finish_capture(self, capture: _Capture) -> None:
        if self.current_card is None:
            return
        value = " ".join(capture.parts).strip() or None
        if value is None:
            return
        if capture.field_name == "badge":
            self.current_card.badges.append(value)
        elif getattr(self.current_card, capture.field_name) is None:
            setattr(self.current_card, capture.field_name, value)


def load_ulta_brand_grid_state(rendered_dom: str) -> UltaBrandGridState | None:
    parser = _UltaBrandGridParser()
    try:
        parser.feed(rendered_dom or "")
        parser.close()
    except Exception as exc:
        raise UltaBrandGridStateError(
            f"Ulta brand-grid rendered DOM is malformed: {type(exc).__name__}"
        ) from exc
    if not parser.cards:
        return None
    count_matches = list(_VIEWED_COUNT_RE.finditer(" ".join(parser.visible_parts)))
    viewed_count: int | None = None
    declared_count: int | None = None
    if count_matches:
        viewed_count = int(count_matches[-1].group("viewed"))
        declared_count = int(count_matches[-1].group("total"))
    return UltaBrandGridState(
        brand_name=" ".join(parser.h1_parts).strip() or None,
        viewed_count=viewed_count,
        declared_count=declared_count,
        cards=tuple(parser.cards),
        load_more_control_present=parser.load_more_control_present,
        explicit_currency_codes=tuple(dict.fromkeys(parser.explicit_currency_codes)),
    )


def _finish_card(card: _CardBuilder) -> UltaBrandGridCard:
    rating_match = _RATING_RE.search(card.rating_text or "")
    variant_match = _VARIANT_RE.search(card.variant_text or "")
    return UltaBrandGridCard(
        grid_position=card.grid_position,
        source_product_id=_product_id_from_url(card.product_url),
        selected_sku_id=card.selected_sku_id,
        product_url=card.product_url,
        brand_name=card.brand_name,
        name=card.name,
        price_display=card.price_display,
        average_rating=rating_match.group("rating") if rating_match else None,
        review_count=int(rating_match.group("reviews").replace(",", "")) if rating_match else None,
        visible_variant_count=int(variant_match.group("count")) if variant_match else None,
        visible_variant_label=card.variant_text,
        badges=tuple(dict.fromkeys(card.badges)),
    )


def _product_id_from_url(value: str | None) -> str | None:
    if value is None:
        return None
    parsed = urlparse(value)
    if (parsed.hostname or "").lower() not in {"ulta.com", "www.ulta.com"}:
        return None
    match = _PRODUCT_ID_RE.search(parsed.path.rstrip("/"))
    return match.group(1) if match else None


def _capture_field(class_value: str) -> str | None:
    tokens = _class_tokens(class_value)
    if "pal-c-ProductCardBody--brandName" in tokens:
        return "brand_name"
    if "pal-c-ProductCardBody--title" in tokens:
        return "name"
    if "pal-c-ProductCardBody--price" in tokens:
        return "price_display"
    if "pal-c-ProductCardHeader__variant" in tokens:
        return "variant_text"
    if "sr-only" in tokens:
        return "rating_text"
    if any("badge" in token.lower() for token in tokens):
        return "badge"
    return None


def _class_tokens(value: str) -> frozenset[str]:
    return frozenset(value.split())


__all__ = [
    "UltaBrandGridCard",
    "UltaBrandGridState",
    "UltaBrandGridStateError",
    "load_ulta_brand_grid_state",
]
