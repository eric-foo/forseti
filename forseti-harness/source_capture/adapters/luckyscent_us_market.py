"""Luckyscent default US/USD storefront-market assertion for CloakBrowser capture.

Luckyscent does not expose a country selector. Its public Hydrogen storefront instead
serves one canonical route and records storefront market state in the serialized
``i18n`` loader context. This plugin performs no preference mutation: it confirms the
default US/USD market fail-closed after the main page renders.

``buyerCountry`` is deliberately excluded. It is a separate origin-derived shopper
signal and may remain non-US even while the retailer serves its US/USD storefront.
Delivery location is not established by this assertion.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


_ENQUEUE_ARGUMENT_RE = re.compile(
    r"window\.__reactRouterContext\.streamController\.enqueue\("
    r"(?P<argument>\"(?:\\.|[^\"\\])*\")\s*\)",
    flags=re.DOTALL,
)


@dataclass(frozen=True)
class LuckyscentUSMarketPlugin:
    """Confirm Luckyscent's canonical route is serving its US/USD market."""

    country_code: str = "US"
    currency_code: str = "USD"

    def __post_init__(self) -> None:
        if self.country_code != "US" or self.currency_code != "USD":
            raise ValueError("Luckyscent market assertion currently supports only US/USD")

    @property
    def humanize(self) -> bool:
        return False

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        del page, setup_timeout_ms
        return PreCaptureOutcome(
            attempted=True,
            steps_completed=True,
            reason=None,
            warning_notes=[],
        )

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        return confirm_luckyscent_us_market(rendered_dom)

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "luckyscent_us_market_assertion",
            "country_code_requested": self.country_code,
            "currency_code_requested": self.currency_code,
            "market_preference_action": "none_default_market_assertion",
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        if confirmation.confirmed:
            return (
                "declared_storefront_market: Luckyscent canonical route CONFIRMED as "
                f"US/USD ({confirmation.detail}); shopper origin and delivery location "
                "remain un-pinned"
            )
        reason = confirmation.detail
        if not outcome.steps_completed and outcome.reason is not None:
            reason = f"pre-capture assertion setup failed: {outcome.reason}; {reason}"
        return (
            "declared_storefront_market: Luckyscent US/USD default-market assertion NOT "
            f"confirmed ({reason}); treat storefront country and currency as un-pinned "
            "(honest gap)"
        )


def confirm_luckyscent_us_market(rendered_dom: str) -> PinConfirmation:
    """Require one serialized Luckyscent i18n object to bind US, market-us, and USD."""
    for context in _iter_i18n_contexts(rendered_dom or ""):
        if (
            context.get("country") == "US"
            and context.get("market") == "market-us"
            and context.get("currency") == "USD"
        ):
            return PinConfirmation(
                confirmed=True,
                detail=(
                    "one Luckyscent i18n loader context bound country=US, "
                    "market=market-us, and currency=USD"
                ),
            )
    return PinConfirmation(
        confirmed=False,
        detail=(
            "required single-object Luckyscent i18n conjunction absent from rendered "
            "DOM (country=US, market=market-us, currency=USD)"
        ),
    )


def _iter_i18n_contexts(rendered_dom: str) -> list[dict[str, Any]]:
    contexts: list[dict[str, Any]] = []
    for match in _ENQUEUE_ARGUMENT_RE.finditer(rendered_dom):
        try:
            chunk = json.loads(match.group("argument"))
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(chunk, str) or '"i18n"' not in chunk:
            continue
        payload_start = chunk.find("[")
        if payload_start < 0:
            continue
        try:
            table = json.loads(chunk[payload_start:].strip())
        except json.JSONDecodeError:
            continue
        if not isinstance(table, list):
            continue
        contexts.extend(_contexts_from_devalue_table(table))
    return contexts


def _contexts_from_devalue_table(table: list[Any]) -> list[dict[str, Any]]:
    contexts: list[dict[str, Any]] = []
    i18n_indexes = {
        index for index, value in enumerate(table) if value == "i18n"
    }
    if not i18n_indexes:
        return contexts

    for candidate in table:
        if not isinstance(candidate, dict):
            continue
        for i18n_index in i18n_indexes:
            context_ref = candidate.get(f"_{i18n_index}")
            context = _resolve_object_reference(table, context_ref)
            if context is not None:
                contexts.append(context)
    return contexts


def _resolve_object_reference(
    table: list[Any], reference: Any
) -> dict[str, Any] | None:
    if not isinstance(reference, int) or reference < 0 or reference >= len(table):
        return None
    encoded = table[reference]
    if not isinstance(encoded, dict):
        return None

    resolved: dict[str, Any] = {}
    for encoded_key, value_reference in encoded.items():
        if not isinstance(encoded_key, str) or not encoded_key.startswith("_"):
            return None
        try:
            key_index = int(encoded_key[1:])
        except ValueError:
            return None
        if (
            key_index < 0
            or key_index >= len(table)
            or not isinstance(table[key_index], str)
            or not isinstance(value_reference, int)
            or value_reference < 0
            or value_reference >= len(table)
        ):
            return None
        resolved[table[key_index]] = table[value_reference]
    return resolved
