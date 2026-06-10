"""Rung-1.5 price payload extraction for JS-hydrated SPA pricing sources.

Deterministic, browser-free recovery of displayed pricing INFORMATION (tiers +
amounts + effective/settling signal) from the structured payloads that a rung-1
HTTP capture already preserves -- WITHOUT a headless browser and WITHOUT
hand-parsing rendered HTML. Two structured payloads are parsed:

  1. The React Router v7 hydration turbo-stream embedded in the page HTML
     (``window.__reactRouterContext.streamController.enqueue("...")``). This
     carries the Contentful CMS tier STRUCTURE: card names, order, ``priceToken``
     references, price descriptors, and per-entry ``updatedAt`` timestamps. The
     displayed price AMOUNT is NOT here -- the page renders an empty
     ``tabular-nums`` span and resolves it client-side from the ``priceToken``.

  2. The static ``prices`` object compiled into one of the page's linked JS
     module assets (``u1e = {prices: {"<token>": {"<currency>": <minor_units>}}}``).
     This carries the per-currency AMOUNTS in minor units. It is a static asset
     fetchable over rung-1 -- an embedded payload, not an XHR endpoint, and not
     render-time-only.

Joining (1) and (2) by ``priceToken`` reconstructs the displayed tiers + amounts.

Honesty contract: this module is a parser, not a network or trust layer. It does
NOT weaken ``block_shell`` (every fetched body keeps its block-shell class). The
"certified content" claim a caller may record is an explicit, checkable
interpretation-layer discriminator over already-recorded rung-1 provenance --
see ``certify_extraction`` -- analogous to the PDF container discriminator in the
anti-block ladder usage guide.

All parsing is anchored on stable, content-derived markers (the ``priceToken``
namespace, ``prices:{"chatgpt.``), never on minification-unstable identifiers or
asset hashes, so it survives redeploys; the prices chunk is discovered by content
anchor, not by hash.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


# --------------------------------------------------------------------------- #
# 1. React Router v7 turbo-stream decode
# --------------------------------------------------------------------------- #

_ENQUEUE_RE = re.compile(r"streamController\.enqueue\(")
# turbo-stream negative sentinels we observe in this payload (undefined / null).
_TURBO_SENTINELS = {-5: None, -7: None}


def _read_js_string_literal(s: str, start: int) -> str:
    """Return the JSON-decodable JS double-quoted string literal starting at ``start``."""
    assert s[start] == '"', f"expected opening quote at {start}, got {s[start]!r}"
    out = ['"']
    i = start + 1
    n = len(s)
    while i < n:
        c = s[i]
        out.append(c)
        if c == "\\":
            if i + 1 < n:
                out.append(s[i + 1])
            i += 2
            continue
        if c == '"':
            return "".join(out)
        i += 1
    raise ValueError("unterminated JS string literal while reading enqueue chunk")


def decode_react_router_stream(html: str) -> Any:
    """Decode the embedded React Router turbo-stream into a Python object graph.

    Raises ``ValueError`` if no stream / no decodable payload is present (an
    honest miss, never a silent empty result).
    """
    chunks: list[str] = []
    for m in _ENQUEUE_RE.finditer(html):
        p = m.end()
        while p < len(html) and html[p] in " \n\r\t":
            p += 1
        if p < len(html) and html[p] == '"':
            lit = _read_js_string_literal(html, p)
            chunks.append(json.loads(lit))
    payload = "".join(chunks)
    if not payload:
        raise ValueError("no react-router stream payload (streamController.enqueue) found")
    values, _end = json.JSONDecoder().raw_decode(payload)
    if not isinstance(values, list):
        raise ValueError("react-router stream root is not the expected flattened array")

    def resolve(idx: Any, seen: tuple[int, ...] = ()) -> Any:
        if isinstance(idx, bool):
            return idx
        if isinstance(idx, int):
            if idx < 0:
                return _TURBO_SENTINELS.get(idx, None)
            if idx in seen or len(seen) > 200:
                return None  # cycle / depth guard
            return _resolve_value(values[idx], seen + (idx,))
        return idx

    def _resolve_value(v: Any, seen: tuple[int, ...]) -> Any:
        if isinstance(v, dict):
            out: dict[str, Any] = {}
            for k, val in v.items():
                if isinstance(k, str) and k.startswith("_"):
                    key = resolve(int(k[1:]), seen)
                else:
                    key = k
                out[str(key)] = resolve(val, seen)
            return out
        if isinstance(v, list):
            return [resolve(e, seen) for e in v]
        return v

    return resolve(0)


# --------------------------------------------------------------------------- #
# 2. CMS tier structure
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class TierPrice:
    price_token: str
    description: str | None
    price_header: str | None
    label: str | None
    cms_name: str | None
    updated_at: str | None


@dataclass(frozen=True)
class Tier:
    name: str
    cms_name: str | None
    display_order: int
    prices: tuple[TierPrice, ...]
    static_price: str | None  # e.g. "Custom pricing" / "Usage pricing" (no token)


_CONSUMER_CARD = "chatGPTPricingCard"
_BUSINESS_CARD = "combinedPricingCard"


def _iter_objects(node: Any):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _iter_objects(v)
    elif isinstance(node, list):
        for e in node:
            yield from _iter_objects(e)


def _as_price(obj: dict) -> TierPrice:
    return TierPrice(
        price_token=obj.get("priceToken"),
        description=obj.get("description"),
        price_header=obj.get("priceHeader"),
        label=obj.get("label"),
        cms_name=obj.get("cmsName"),
        updated_at=obj.get("updatedAt"),
    )


def extract_tier_structure(root: Any) -> list[Tier]:
    """Pull the displayed pricing cards (consumer + business) in CMS document order.

    Card order follows first-encounter order in the resolved graph, which mirrors
    the CMS card-row layout. Each card keeps its ``priceToken`` references and any
    ``staticPrice`` label (Custom / Usage pricing) for tiers without a numeric
    token.
    """
    tiers: list[Tier] = []
    order = 0
    for obj in _iter_objects(root):
        tn = obj.get("__typename") if isinstance(obj, dict) else None
        if tn not in (_CONSUMER_CARD, _BUSINESS_CARD):
            continue
        name = obj.get("name")
        if not name:
            continue
        prices: list[TierPrice] = []
        raw_prices = obj.get("prices")
        if isinstance(raw_prices, list):
            for p in raw_prices:
                if isinstance(p, dict) and p.get("priceToken"):
                    prices.append(_as_price(p))
        static_price = None
        sp = obj.get("staticPrice")
        if isinstance(sp, dict):
            static_price = sp.get("title") or sp.get("cmsName")
        suffix = obj.get("nameSuffix")
        display_name = f"{name} ({suffix})" if suffix else name
        tiers.append(Tier(
            name=display_name,
            cms_name=obj.get("cmsName"),
            display_order=order,
            prices=tuple(prices),
            static_price=static_price,
        ))
        order += 1
    if not tiers:
        raise ValueError("no pricing cards (chatGPTPricingCard / combinedPricingCard) in CMS graph")
    return tiers


# --------------------------------------------------------------------------- #
# 3. Static JS-module prices object
# --------------------------------------------------------------------------- #

PRICES_ANCHOR = re.compile(r'prices:\{"chatgpt\.')
_TOKEN_LIST_RE = re.compile(r"\[(`chatgpt\.[a-z0-9.]+`(?:,`[^`]+`)*)\]")
_UNQUOTED_KEY_RE = re.compile(r"([{,])\s*([A-Za-z_$][\w$]*)\s*:")


def chunk_contains_prices(js: str) -> bool:
    return PRICES_ANCHOR.search(js) is not None


def _match_braces(s: str, start: int) -> tuple[int, int]:
    depth = 0
    i = start
    instr: str | None = None
    while i < len(s):
        c = s[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == instr:
                instr = None
        else:
            if c in "\"'`":
                instr = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return start, i + 1
        i += 1
    raise ValueError("unbalanced braces while extracting prices object")


def extract_object_at_anchor(text: str, anchor: "re.Pattern[str] | str") -> dict:
    """Extract the brace-delimited JS object literal that begins at a content anchor.

    Source-agnostic spine primitive: the caller supplies the stable content
    marker (regex or compiled pattern) for the object it wants -- an OpenAI price
    adapter passes ``prices:{"chatgpt.``. The object is brace-matched from the
    first ``{`` at/after the anchor, JS unquoted keys are quoted, and the literal
    is parsed as JSON. Raises ``ValueError`` if the object is absent or
    unparseable -- an honest miss, never a silent empty result.
    """
    pattern = re.compile(anchor) if isinstance(anchor, str) else anchor
    m = pattern.search(text)
    if not m:
        raise ValueError(f"anchor {pattern.pattern!r} not present in text")
    brace_start = text.index("{", m.start())
    start, end = _match_braces(text, brace_start)
    normalised = _UNQUOTED_KEY_RE.sub(r'\1"\2":', text[start:end])
    obj = json.loads(normalised)
    if not isinstance(obj, dict) or not obj:
        raise ValueError("parsed object is empty or not an object")
    return obj


def extract_prices_object(js: str) -> dict[str, dict[str, float]]:
    """OpenAI price adapter over :func:`extract_object_at_anchor`.

    Recovers ``{token: {currency: minor_units}}`` from a JS module's
    ``prices:{"chatgpt.`` object. The generic recovery (anchor -> brace-match ->
    JS-to-JSON) lives in :func:`extract_object_at_anchor`; this wrapper only
    binds the OpenAI price anchor, so the spine carries no price/vendor specifics.
    """
    return extract_object_at_anchor(js, PRICES_ANCHOR)


def extract_token_list(js: str) -> list[str]:
    """The canonical price-token array compiled alongside the prices object."""
    m = _TOKEN_LIST_RE.search(js)
    if not m:
        return []
    return re.findall(r"`([^`]+)`", m.group(1))


# --------------------------------------------------------------------------- #
# 4. Join + format
# --------------------------------------------------------------------------- #

# Minor-unit exponent per currency (ISO 4217 minor units). Default 2.
_ZERO_DECIMAL = {"jpy", "krw", "clp", "vnd", "isk", "huf", "twd", "ugx", "tzs"}


def minor_units_to_display(minor: float, currency: str) -> str:
    cur = currency.lower()
    if cur in _ZERO_DECIMAL:
        return f"{int(round(minor)):,}"
    return f"{minor / 100:,.2f}"


@dataclass
class ResolvedTierPrice:
    price_token: str
    descriptor: str | None
    price_header: str | None
    label: str | None
    amount_minor: float | None
    amount_display: str | None
    token_updated_at: str | None
    resolved: bool


@dataclass
class ResolvedTier:
    name: str
    display_order: int
    prices: list[ResolvedTierPrice] = field(default_factory=list)
    static_price: str | None = None


def join_tiers_with_amounts(
    tiers: list[Tier],
    prices: dict[str, dict[str, float]],
    *,
    currency: str = "usd",
) -> list[ResolvedTier]:
    out: list[ResolvedTier] = []
    for tier in tiers:
        rt = ResolvedTier(name=tier.name, display_order=tier.display_order,
                          static_price=tier.static_price)
        for tp in tier.prices:
            cur_map = prices.get(tp.price_token)
            amount = None
            if isinstance(cur_map, dict):
                amount = cur_map.get(currency)
            resolved = isinstance(amount, (int, float)) and not isinstance(amount, bool)
            rt.prices.append(ResolvedTierPrice(
                price_token=tp.price_token,
                descriptor=tp.description,
                price_header=tp.price_header,
                label=tp.label,
                amount_minor=amount if resolved else None,
                amount_display=(minor_units_to_display(amount, currency) if resolved else None),
                token_updated_at=tp.updated_at,
                resolved=resolved,
            ))
        out.append(rt)
    return out


# --------------------------------------------------------------------------- #
# 5. Effective date from a Next.js RSC announcement (structured)
# --------------------------------------------------------------------------- #

_NEXT_F_RE = re.compile(r"self\.__next_f\.push\(\[\d+,")
_PUBDATE_RE = re.compile(r'"publicationDateText":"([^"]+)"')


def extract_announcement_effective_date(html: str) -> str | None:
    """Structured ``publicationDateText`` from a Next.js RSC announcement body."""
    chunks: list[str] = []
    for m in _NEXT_F_RE.finditer(html):
        p = m.end()
        while p < len(html) and html[p] in " \n\r\t":
            p += 1
        if p < len(html) and html[p] == '"':
            try:
                chunks.append(json.loads(_read_js_string_literal(html, p)))
            except ValueError:
                pass
    rsc = "".join(c for c in chunks if isinstance(c, str))
    m = _PUBDATE_RE.search(rsc)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# 6. Certification discriminator (interpretation-layer; does NOT touch block_shell)
# --------------------------------------------------------------------------- #

@dataclass
class CertificationCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class PayloadBody:
    """One fetched body backing a certified payload (source-agnostic).

    ``label`` namespaces this body's checks (``{label}_not_block_shell`` and
    ``{label}_body_inspectable``); an OpenAI price capture passes ``page`` and
    ``prices_chunk``. ``detail_label`` preserves a legacy human-readable label in
    serialized check DETAILS when it differs from ``label`` (e.g. the "prices
    chunk" wording vs the ``prices_chunk`` check namespace); defaults to ``label``.
    """
    label: str
    block_class: str
    status: int
    block_signal: str | None
    detail_label: str | None = None


_GENERIC_DISCRIMINATOR_NOTE = (
    "interpretation-layer INTERNAL-CONSISTENCY discriminator over rung-1 provenance: "
    "asserts at least one backing body is present and every one is inspectable, 2xx, and "
    "not a block/empty shell, the payload parsed cleanly, and at least one caller-supplied "
    "domain check is present and all passed. Does NOT assert freshness or completeness "
    "(recorded as provenance, not certified) and does NOT weaken block_shell"
)


@dataclass
class CertificationVerdict:
    certified: bool
    checks: list[CertificationCheck]
    discriminator: str = "embedded_payload_v0"
    discriminator_note: str | None = None
    resolved_tier_count: int | None = None
    priced_tier_count: int | None = None

    def as_dict(self) -> dict:
        out: dict = {"certified_content": self.certified}
        if self.resolved_tier_count is not None:
            out["resolved_tier_count"] = self.resolved_tier_count
        if self.priced_tier_count is not None:
            out["priced_tier_count"] = self.priced_tier_count
        out["discriminator"] = self.discriminator
        out["discriminator_note"] = self.discriminator_note or _GENERIC_DISCRIMINATOR_NOTE
        out["checks"] = [
            {"check": c.name, "passed": c.passed, "detail": c.detail}
            for c in self.checks
        ]
        return out


def certify_payload(
    *,
    bodies: list[PayloadBody],
    payload_parsed: bool,
    domain_checks: list[CertificationCheck],
    discriminator: str = "embedded_payload_v0",
    discriminator_note: str | None = None,
    payload_check_name: str = "payload_parsed",
    payload_check_detail: str | None = None,
) -> CertificationVerdict:
    """Source-agnostic certification scaffold for a recovered embedded payload.

    Certifies INTERNAL CONSISTENCY only: at least one backing ``PayloadBody`` is
    present and every one is 2xx, NOT a block/empty shell, and INSPECTABLE (not
    an undecoded/encoded body); the payload parsed; and at least one
    caller-supplied ``domain_checks`` entry is present and all passed. A 200 is
    never certified as content on its own, an encoded/uninspectable body always
    refuses, and a parsed payload with NO backing body or NO domain check cannot
    certify (no vacuous pass). Does NOT assert freshness or completeness. The
    domain layer (e.g. price coherence) lives entirely in ``domain_checks``, so
    this scaffold carries no price/vendor semantics.

    ``payload_check_name`` / ``payload_check_detail`` let an adapter preserve a
    legacy serialized name/detail for the parse check (the OpenAI price path
    keeps ``prices_object_parsed``).
    """
    checks: list[CertificationCheck] = []
    if not bodies:
        checks.append(CertificationCheck(
            "body_provenance_present",
            False,
            "at least one backing body is required; a parsed payload without "
            "provenance cannot certify",
        ))
    for body in bodies:
        detail_label = body.detail_label or body.label
        checks.append(CertificationCheck(
            f"{body.label}_not_block_shell",
            body.block_class == "content_unverified" and 200 <= body.status < 300,
            f"{detail_label} HTTP {body.status}, block_shell={body.block_class}",
        ))
    for body in bodies:
        detail_label = body.detail_label or body.label
        checks.append(CertificationCheck(
            f"{body.label}_body_inspectable",
            body.block_signal != "encoded_body_uninspectable",
            f"{detail_label} block_shell signal={body.block_signal!r} "
            "(content cannot be certified from an undecoded/encoded body)",
        ))
    checks.append(CertificationCheck(
        payload_check_name,
        bool(payload_parsed),
        (payload_check_detail if payload_check_detail is not None
         else f"structured payload parsed: {bool(payload_parsed)}"),
    ))
    if not domain_checks:
        checks.append(CertificationCheck(
            "domain_checks_present",
            False,
            "at least one caller-supplied domain check is required for "
            "internal-consistency certification",
        ))
    checks.extend(domain_checks)
    return CertificationVerdict(
        certified=all(c.passed for c in checks),
        checks=checks,
        discriminator=discriminator,
        discriminator_note=discriminator_note,
    )


def _price_domain_checks(
    *,
    token_list: list[str],
    prices: dict[str, dict[str, float]],
    resolved_tiers: list[ResolvedTier],
    currency: str = "usd",
) -> tuple[list[CertificationCheck], int, int]:
    """OpenAI price-domain checks for :func:`certify_payload` (the price adapter).

    Returns ``(domain_checks, priced_tier_count, resolved_tier_count)``. The
    checks: a non-empty canonical token list whose tokens are all present in the
    prices object; every displayed token covered by that list (two-way
    coherence); EVERY consumer tier with a numeric token resolved in the target
    currency; at least one paid tier priced; and every resolved amount within a
    plausible range (>= 0, below a sane ceiling). A custom/usage static price
    (Enterprise) is an honest non-numeric tier, not a failure.
    """
    checks: list[CertificationCheck] = []

    # An ABSENT token list is a missing cross-check input, not a confirmed match:
    # fail (was a vacuous pass) so a payload reshape that drops the token array
    # cannot silently certify a prices object that lacks the displayed tiers.
    tokens_in_prices = bool(token_list) and all(t in prices for t in token_list)
    checks.append(CertificationCheck(
        "token_list_consistent_with_prices",
        tokens_in_prices,
        ("canonical token list absent — cross-check input missing"
         if not token_list
         else f"canonical token list ({len(token_list)}) all present in prices object: {tokens_in_prices}"),
    ))

    numeric_tier_prices = [
        rp for rt in resolved_tiers for rp in rt.prices
    ]

    # Two-way coherence: every DISPLAYED price token must be covered by the
    # canonical token list (completing displayed ⊆ token_list ⊆ prices). The
    # one-way token_list ⊆ prices check alone could pass a wrong/partial list.
    displayed_tokens = [rp.price_token for rp in numeric_tier_prices]
    displayed_in_list = bool(token_list) and all(t in token_list for t in displayed_tokens)
    missing_from_list = (
        [t for t in displayed_tokens if t not in token_list] if token_list else displayed_tokens
    )
    checks.append(CertificationCheck(
        "displayed_tokens_in_token_list",
        displayed_in_list,
        (f"all {len(displayed_tokens)} displayed price tokens covered by the canonical token list"
         if displayed_in_list
         else f"displayed tokens NOT covered by canonical token list: {missing_from_list}"),
    ))

    unresolved = [rp.price_token for rp in numeric_tier_prices if not rp.resolved]
    all_tokens_resolved = len(unresolved) == 0 and len(numeric_tier_prices) > 0
    checks.append(CertificationCheck(
        "all_displayed_tokens_resolved",
        all_tokens_resolved,
        (f"{len(numeric_tier_prices) - len(unresolved)}/{len(numeric_tier_prices)} "
         f"token-bearing tier prices resolved to {currency}"
         + (f"; unresolved={unresolved}" if unresolved else "")),
    ))

    priced = sum(
        1 for rt in resolved_tiers
        if any(rp.resolved and (rp.amount_minor or 0) > 0 for rp in rt.prices)
    )
    checks.append(CertificationCheck(
        "at_least_one_paid_tier_priced",
        priced >= 1,
        f"{priced} tiers resolved to a positive {currency} amount",
    ))

    # Plausibility floor/ceiling on resolved amounts: catches garbage from a
    # payload reshape (a negative, or an epoch/timestamp grabbed instead of a
    # price). $0 is a legitimate amount (Free tier), so the floor is 0, not >0.
    max_plausible_minor = 100_000_000  # $1,000,000 in 2-dp minor units
    implausible = [
        rp.price_token for rp in numeric_tier_prices
        if rp.resolved and not (0 <= (rp.amount_minor or 0) < max_plausible_minor)
    ]
    resolved_amount_count = sum(1 for rp in numeric_tier_prices if rp.resolved)
    checks.append(CertificationCheck(
        "resolved_amounts_plausible",
        not implausible,
        (f"all {resolved_amount_count} resolved amounts within [0, {max_plausible_minor}) minor units"
         + (f"; implausible={implausible}" if implausible else "")),
    ))

    resolved_count = sum(1 for rt in resolved_tiers if rt.prices or rt.static_price)
    return checks, priced, resolved_count


_PRICE_DISCRIMINATOR_NOTE = (
    "interpretation-layer INTERNAL-CONSISTENCY discriminator over rung-1 provenance: "
    "asserts the payload parsed cleanly and cross-checks (two-way token list, all "
    "displayed tokens resolved, amounts plausible). Does NOT assert freshness or "
    "completeness (recorded as provenance, not certified) and does NOT weaken block_shell"
)


def certify_extraction(
    *,
    page_block_class: str,
    page_status: int,
    page_block_signal: str | None,
    chunk_block_class: str,
    chunk_status: int,
    chunk_block_signal: str | None,
    token_list: list[str],
    prices: dict[str, dict[str, float]],
    resolved_tiers: list[ResolvedTier],
    currency: str = "usd",
) -> CertificationVerdict:
    """OpenAI price adapter over :func:`certify_payload`.

    Binds the two OpenAI bodies (page + prices chunk) and the price-domain
    checks, preserving the ``rung15_price_payload_v0`` discriminator. Behaviour
    is identical to the pre-isolation certifier; the generic scaffold and the
    price checks are now separable so a non-price adapter can reuse the scaffold.
    """
    domain_checks, priced, resolved_count = _price_domain_checks(
        token_list=token_list, prices=prices,
        resolved_tiers=resolved_tiers, currency=currency,
    )
    verdict = certify_payload(
        bodies=[
            PayloadBody("page", page_block_class, page_status, page_block_signal),
            PayloadBody("prices_chunk", chunk_block_class, chunk_status,
                        chunk_block_signal, detail_label="prices chunk"),
        ],
        payload_parsed=len(prices) > 0,
        domain_checks=domain_checks,
        discriminator="rung15_price_payload_v0",
        discriminator_note=_PRICE_DISCRIMINATOR_NOTE,
        payload_check_name="prices_object_parsed",
        payload_check_detail=f"{len(prices)} price tokens parsed from JS-module prices object",
    )
    verdict.resolved_tier_count = resolved_count
    verdict.priced_tier_count = priced
    return verdict


__all__ = [
    "decode_react_router_stream",
    "Tier", "TierPrice", "extract_tier_structure",
    "PRICES_ANCHOR", "chunk_contains_prices",
    "extract_object_at_anchor", "extract_prices_object", "extract_token_list",
    "ResolvedTier", "ResolvedTierPrice", "join_tiers_with_amounts", "minor_units_to_display",
    "extract_announcement_effective_date",
    "PayloadBody", "CertificationVerdict", "CertificationCheck",
    "certify_payload", "certify_extraction",
]
