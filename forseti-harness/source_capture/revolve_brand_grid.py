from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse


REVOLVE_GRID_CONTENT_RECORD_VERSION = "revolve_grid_content_v1"
REVOLVE_GRID_PARSER_VERSION = "revolve_grid_parser_v2"
_BRAND_GRID_PATH_RE = re.compile(
    r"/(?P<slug>[a-z0-9][a-z0-9-]*)/br/(?P<brand_id>[a-f0-9]{6})/?$",
    re.IGNORECASE,
)
_COUNT_RE = re.compile(r"(?P<count>\d[\d,]*)\s+Items?\b", re.IGNORECASE)
_RATING_RE = re.compile(
    r"(?P<rating>\d+(?:\.\d+)?)\s+out (?:of )?5 stars rating in total "
    r"(?P<count>\d[\d,]*)\s+reviews?",
    re.IGNORECASE,
)
_STYLE_RE = re.compile(r"^[A-Z0-9]{2,12}-[A-Z]{1,4}\d+$", re.IGNORECASE)
_VOID = frozenset(
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
_NON_RENDERED = frozenset({"script", "style"})


class RevolveBrandGridStateError(ValueError):
    """The rendered REVOLVE brand grid was absent or internally inconsistent."""


@dataclass(frozen=True)
class RevolveBrandGridCard:
    grid_position: int
    style_id: str
    product_url: str | None
    brand_name: str | None
    name: str | None
    price_display: str | None
    average_rating: str | None
    review_count: int
    color_names: tuple[str, ...]
    selected_color: str | None
    badges: tuple[str, ...]
    out_of_stock: bool | None
    image_urls: tuple[str, ...]


@dataclass(frozen=True)
class RevolveBrandGridState:
    brand_slug: str | None
    brand_id: str | None
    brand_name: str | None
    declared_count: int | None
    cards: tuple[RevolveBrandGridCard, ...]
    view_limit: int | None
    continuation_control_present: bool
    country_code: str | None
    currency_code: str | None
    content_record_version: str | None = None


@dataclass
class _Card:
    style_id: str
    grid_position: int
    product_url: str | None = None
    brand_name: str | None = None
    name: str | None = None
    price_display: str | None = None
    rating_label: str | None = None
    colors: list[str] = field(default_factory=list)
    selected_color: str | None = None
    badges: list[str] = field(default_factory=list)
    out_of_stock: bool | None = None
    images: list[str] = field(default_factory=list)


@dataclass
class _Capture:
    field: str
    tag: str
    depth: int
    parts: list[str] = field(default_factory=list)


class _GridParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.visible: list[str] = []
        self.h1_parts: list[str] = []
        self.h1_depth: int | None = None
        self.card: _Card | None = None
        self.card_depth: int | None = None
        self.captures: list[_Capture] = []
        self.cards: list[RevolveBrandGridCard] = []
        self.view_limit: int | None = None
        self.continuation = False
        self.preference_usd = False
        self.country_codes: list[str] = []
        self.brand_subjects: list[tuple[str, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        lowered = tag.lower()
        attributes = {key.lower(): value or "" for key, value in attrs}
        if lowered not in _VOID:
            self.stack.append(lowered)
        depth = len(self.stack)
        href = attributes.get("href", "")
        if lowered == "link" and "canonical" in attributes.get("rel", "").split():
            parsed_href = urlparse(href)
            subject = _BRAND_GRID_PATH_RE.fullmatch(parsed_href.path)
            if (
                parsed_href.scheme == "https"
                and (parsed_href.hostname or "").lower()
                in {"revolve.com", "www.revolve.com"}
                and subject is not None
            ):
                self.brand_subjects.append(
                    (
                        subject.group("slug").lower(),
                        subject.group("brand_id").lower(),
                    )
                )
        country = re.search(r"countryCode=([A-Za-z]{2})", href, re.IGNORECASE)
        if country:
            self.country_codes.append(country.group(1).upper())
        aria = attributes.get("aria-label", "")
        if "Country Preference: US" in aria:
            self.preference_usd = "$USD" in aria

        if self.card is None and lowered == "li":
            tokens = set(attributes.get("class", "").split())
            style_id = attributes.get("id", "")
            if "plp__product" in tokens and _STYLE_RE.fullmatch(style_id):
                self.card = _Card(
                    style_id=style_id.upper(),
                    grid_position=len(self.cards) + 1,
                )
                self.card_depth = depth
                return

        if self.card is not None:
            tokens = set(attributes.get("class", "").split())
            if (
                lowered == "a"
                and "product-link" in tokens
                and attributes.get("href")
                and self.card.product_url is None
            ):
                self.card.product_url = urljoin(
                    "https://www.revolve.com", attributes["href"]
                )
            field_name = None
            if "js-plp-name" in tokens:
                field_name = "name"
            elif "js-plp-brand" in tokens:
                field_name = "brand_name"
            elif "js-plp-prices-div" in tokens:
                field_name = "price_display"
            if field_name:
                self.captures.append(_Capture(field_name, lowered, depth))
            if lowered == "button":
                label = aria.strip()
                rating = _RATING_RE.search(label)
                if rating:
                    self.card.rating_label = label
                if label.upper().startswith(("PREORDER ", "QUICK VIEW ")):
                    self.card.badges.append(label.split(" ", 1)[0].upper())
                data_oos = attributes.get("data-oos")
                if data_oos in {"true", "false"}:
                    self.card.out_of_stock = data_oos == "true"
            if lowered == "input" and attributes.get("type") == "radio":
                label = aria.removeprefix("color:").strip()
                if label:
                    self.card.colors.append(label)
                    if "checked" in attributes:
                        self.card.selected_color = label
            if lowered == "img":
                for key in ("src", "data-lazy-src"):
                    value = attributes.get(key, "").strip()
                    if value and "revolveassets.com" in value:
                        self.card.images.append(value)
            return

        if lowered == "h1" and self.h1_depth is None:
            self.h1_depth = depth
        if lowered in {"button", "a"} and re.search(
            r"(?:load|show)\s+more|next\s+page", aria, re.IGNORECASE
        ):
            self.continuation = True

    def handle_data(self, data: str) -> None:
        if self.stack and self.stack[-1] in _NON_RENDERED:
            return
        text = " ".join(data.split())
        if not text:
            return
        self.visible.append(text)
        if self.h1_depth is not None:
            self.h1_parts.append(text)
        if self.card is not None:
            for capture in self.captures:
                capture.parts.append(text)
        view_match = re.fullmatch(r"View\s+(\d+)", text, flags=re.IGNORECASE)
        if view_match:
            self.view_limit = max(self.view_limit or 0, int(view_match.group(1)))

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        depth = len(self.stack)
        for capture in list(self.captures):
            if capture.tag == lowered and capture.depth == depth:
                if self.card is not None:
                    value = " ".join(capture.parts).strip() or None
                    if value is not None and getattr(self.card, capture.field) is None:
                        setattr(self.card, capture.field, value)
                self.captures.remove(capture)
        if self.h1_depth == depth and lowered == "h1":
            self.h1_depth = None
        if self.card is not None and self.card_depth == depth and lowered == "li":
            self.cards.append(_finish_card(self.card))
            self.card = None
            self.card_depth = None
            self.captures.clear()
        if self.stack:
            if self.stack[-1] == lowered:
                self.stack.pop()
            elif lowered in self.stack:
                index = len(self.stack) - 1 - self.stack[::-1].index(lowered)
                del self.stack[index:]


def load_revolve_brand_grid_state(
    rendered_dom: str,
) -> RevolveBrandGridState | None:
    compact = _load_compact(rendered_dom)
    if compact is not None:
        return compact
    parser = _GridParser()
    try:
        parser.feed(rendered_dom or "")
        parser.close()
    except Exception as exc:
        raise RevolveBrandGridStateError(
            f"REVOLVE brand-grid DOM is malformed: {type(exc).__name__}"
        ) from exc
    if not parser.cards:
        return None
    visible = " ".join(parser.visible)
    counts = list(_COUNT_RE.finditer(visible))
    declared = int(counts[-1].group("count").replace(",", "")) if counts else None
    first_url = next(
        (card.product_url for card in parser.cards if card.product_url), None
    )
    del first_url
    countries = set(parser.country_codes)
    subjects = set(parser.brand_subjects)
    brand_slug, brand_id = next(iter(subjects)) if len(subjects) == 1 else (None, None)
    preference_usd = parser.preference_usd or (
        "Country Preference: US" in visible and "$USD" in visible
    )
    return RevolveBrandGridState(
        brand_slug=brand_slug,
        brand_id=brand_id,
        brand_name=" ".join(parser.h1_parts).strip() or None,
        declared_count=declared,
        cards=tuple(parser.cards),
        view_limit=parser.view_limit,
        continuation_control_present=parser.continuation,
        country_code="US" if countries == {"US"} else None,
        currency_code="USD" if preference_usd else None,
    )


def build_revolve_brand_grid_content_record(
    *, rendered_dom: str, final_url: str
) -> dict[str, object]:
    state = load_revolve_brand_grid_state(rendered_dom)
    if state is None:
        raise RevolveBrandGridStateError(
            "REVOLVE brand-grid state is absent from the rendered DOM"
        )
    parsed = urlparse(final_url)
    match = re.fullmatch(
        r"/(?P<slug>[a-z0-9][a-z0-9-]*)/br/(?P<brand_id>[a-f0-9]{6})",
        parsed.path.rstrip("/"),
        flags=re.IGNORECASE,
    )
    if match is None:
        raise RevolveBrandGridStateError(
            "REVOLVE grid final URL does not bind a brand slug and id"
        )
    return {
        "content_record_version": REVOLVE_GRID_CONTENT_RECORD_VERSION,
        "retailer": "revolve",
        "final_url": final_url,
        "brand_slug": match.group("slug").lower(),
        "brand_id": match.group("brand_id").lower(),
        "brand_name": state.brand_name,
        "declared_count": state.declared_count,
        "view_limit": state.view_limit,
        "continuation_control_present": state.continuation_control_present,
        "country_code": state.country_code,
        "currency_code": state.currency_code,
        "cards": [
            {
                "grid_position": card.grid_position,
                "style_id": card.style_id,
                "product_url": card.product_url,
                "brand_name": card.brand_name,
                "name": card.name,
                "price_display": card.price_display,
                "average_rating": card.average_rating,
                "review_count": card.review_count,
                "color_names": list(card.color_names),
                "selected_color": card.selected_color,
                "badges": list(card.badges),
                "out_of_stock": card.out_of_stock,
                "image_urls": list(card.image_urls),
            }
            for card in state.cards
        ],
    }


def _finish_card(card: _Card) -> RevolveBrandGridCard:
    rating = _RATING_RE.search(card.rating_label or "")
    return RevolveBrandGridCard(
        grid_position=card.grid_position,
        style_id=card.style_id,
        product_url=card.product_url,
        brand_name=card.brand_name,
        name=card.name,
        price_display=card.price_display,
        average_rating=rating.group("rating") if rating else None,
        review_count=(
            int(rating.group("count").replace(",", "")) if rating else 0
        ),
        color_names=tuple(dict.fromkeys(card.colors)),
        selected_color=card.selected_color,
        badges=tuple(dict.fromkeys(card.badges)),
        out_of_stock=card.out_of_stock,
        image_urls=tuple(dict.fromkeys(card.images)),
    )


def _load_compact(value: str) -> RevolveBrandGridState | None:
    stripped = (value or "").lstrip()
    if not stripped.startswith("{"):
        return None
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or "content_record_version" not in payload:
        return None
    if payload.get("content_record_version") != REVOLVE_GRID_CONTENT_RECORD_VERSION:
        raise RevolveBrandGridStateError(
            "REVOLVE grid content record version is unsupported"
        )
    if payload.get("retailer") != "revolve":
        raise RevolveBrandGridStateError(
            "REVOLVE grid content record retailer binding is invalid"
        )
    cards_value = payload.get("cards")
    if not isinstance(cards_value, list) or not cards_value:
        raise RevolveBrandGridStateError(
            "REVOLVE grid content record cards must be non-empty"
        )
    cards: list[RevolveBrandGridCard] = []
    for index, item in enumerate(cards_value):
        if not isinstance(item, dict):
            raise RevolveBrandGridStateError(f"REVOLVE grid card {index} is not an object")
        style_id = item.get("style_id")
        position = item.get("grid_position")
        if (
            not isinstance(style_id, str)
            or not _STYLE_RE.fullmatch(style_id)
            or not isinstance(position, int)
            or isinstance(position, bool)
            or position < 1
        ):
            raise RevolveBrandGridStateError(
                f"REVOLVE grid card {index} has invalid identity"
            )
        cards.append(
            RevolveBrandGridCard(
                grid_position=position,
                style_id=style_id.upper(),
                product_url=_optional_text(item, "product_url", index),
                brand_name=_optional_text(item, "brand_name", index),
                name=_optional_text(item, "name", index),
                price_display=_optional_text(item, "price_display", index),
                average_rating=_optional_text(item, "average_rating", index),
                review_count=_required_int(item, "review_count", index),
                color_names=_string_tuple(item, "color_names", index),
                selected_color=_optional_text(item, "selected_color", index),
                badges=_string_tuple(item, "badges", index),
                out_of_stock=_optional_bool(item, "out_of_stock", index),
                image_urls=_string_tuple(item, "image_urls", index),
            )
        )
    return RevolveBrandGridState(
        brand_slug=_optional_text(payload, "brand_slug", -1),
        brand_id=_optional_text(payload, "brand_id", -1),
        brand_name=_optional_text(payload, "brand_name", -1),
        declared_count=_optional_int(payload, "declared_count", -1),
        cards=tuple(cards),
        view_limit=_optional_int(payload, "view_limit", -1),
        continuation_control_present=_required_bool(
            payload, "continuation_control_present", -1
        ),
        country_code=_optional_text(payload, "country_code", -1),
        currency_code=_optional_text(payload, "currency_code", -1),
        content_record_version=REVOLVE_GRID_CONTENT_RECORD_VERSION,
    )


def _optional_text(value: dict[str, object], key: str, index: int) -> str | None:
    item = value.get(key)
    if item is None or isinstance(item, str):
        return item
    raise RevolveBrandGridStateError(f"REVOLVE grid card {index} has invalid {key}")


def _optional_int(value: dict[str, object], key: str, index: int) -> int | None:
    item = value.get(key)
    if item is None or (
        isinstance(item, int) and not isinstance(item, bool) and item >= 0
    ):
        return item
    raise RevolveBrandGridStateError(f"REVOLVE grid card {index} has invalid {key}")


def _required_int(value: dict[str, object], key: str, index: int) -> int:
    item = _optional_int(value, key, index)
    if item is None:
        raise RevolveBrandGridStateError(f"REVOLVE grid card {index} lacks {key}")
    return item


def _optional_bool(value: dict[str, object], key: str, index: int) -> bool | None:
    item = value.get(key)
    if item is None or isinstance(item, bool):
        return item
    raise RevolveBrandGridStateError(f"REVOLVE grid card {index} has invalid {key}")


def _required_bool(value: dict[str, object], key: str, index: int) -> bool:
    item = _optional_bool(value, key, index)
    if item is None:
        raise RevolveBrandGridStateError(f"REVOLVE grid record lacks {key}")
    return item


def _string_tuple(value: dict[str, object], key: str, index: int) -> tuple[str, ...]:
    item = value.get(key)
    if isinstance(item, list) and all(isinstance(entry, str) for entry in item):
        return tuple(item)
    raise RevolveBrandGridStateError(f"REVOLVE grid card {index} has invalid {key}")


__all__ = [
    "REVOLVE_GRID_CONTENT_RECORD_VERSION",
    "REVOLVE_GRID_PARSER_VERSION",
    "RevolveBrandGridCard",
    "RevolveBrandGridState",
    "RevolveBrandGridStateError",
    "build_revolve_brand_grid_content_record",
    "load_revolve_brand_grid_state",
]
