"""Bounded, fail-closed traversal of Sephora Bestselling category PageJSON."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)
from source_capture.adapters.sephora_us_market import SephoraUSMarketPlugin
from source_capture.sephora_catalog_grid import (
    SEPHORA_CATALOG_MAX_PAGE,
    extract_sephora_catalog_request,
    load_sephora_catalog_linkstore_page,
)


_COUNTRY_DIALOG_SELECTOR = '[role="dialog"][aria-modal="true"][data-at="modal_dialog"]'
_COUNTRY_DIALOG_DIAGNOSTIC = "This site does not ship to your country."
_COUNTRY_DIALOG_POST_NAV_WAIT_MS = 2_000
_COUNTRY_DIALOG_PERSISTED_REASON = (
    "Sephora country dialog remained visible after explicit continuation"
)
_COUNTRY_DIALOG_PERSISTED_WARNING = (
    "Sephora geo/shipping dialog persisted after explicit continuation; "
    "grid admission certifies only the retailer-serialized US country route, "
    "while origin country and delivery eligibility remain unpinned"
)


@dataclass
class SephoraCatalogTraversalPlugin:
    """Capture consecutive 60-product PageJSON payloads in one anonymous tab."""

    target_url: str
    page_count: int = 2
    traversal_timeout_seconds: float = 90.0
    _grid_page_doms: list[str] = field(default_factory=list, init=False, repr=False)
    _grid_page_urls: list[str] = field(default_factory=list, init=False, repr=False)
    _grid_observation: dict[str, object] = field(default_factory=dict, init=False, repr=False)
    _geo_dialog_observed: bool = field(default=False, init=False, repr=False)
    _geo_dialog_persisted_after_continue: bool = field(
        default=False, init=False, repr=False
    )
    _geo_dialog_warning_emitted: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        request = extract_sephora_catalog_request(self.target_url)
        if request is None or request[1] != 1:
            raise ValueError(
                "Sephora catalog traversal requires a currentPage=1 "
                "BEST_SELLING /shop/<category> URL"
            )
        if self.page_count < 1 or self.page_count > SEPHORA_CATALOG_MAX_PAGE:
            raise ValueError(
                f"sephora_catalog_page_count must be in [1,{SEPHORA_CATALOG_MAX_PAGE}]"
            )
        if self.traversal_timeout_seconds <= 0:
            raise ValueError("Sephora catalog traversal timeout must be positive")

    @property
    def humanize(self) -> bool:
        return True

    @property
    def grid_page_doms(self) -> tuple[str, ...]:
        return tuple(self._grid_page_doms)

    @property
    def grid_page_urls(self) -> tuple[str, ...]:
        return tuple(self._grid_page_urls)

    @property
    def grid_observation(self) -> dict[str, object]:
        return dict(self._grid_observation)

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        """Reuse the established same-tab Sephora country-continuation preflight."""

        outcome = SephoraUSMarketPlugin(
            target_url=self.target_url,
            page_kind="grid",
        ).before(
            page,
            setup_timeout_ms=min(setup_timeout_ms, 30_000),
        )
        if (
            not outcome.steps_completed
            and outcome.reason == _COUNTRY_DIALOG_PERSISTED_REASON
        ):
            self._geo_dialog_observed = True
            self._geo_dialog_persisted_after_continue = True
            self._geo_dialog_warning_emitted = True
            return _outcome(warning=_COUNTRY_DIALOG_PERSISTED_WARNING)
        return outcome

    def before_snapshot(
        self, page: object, *, setup_timeout_ms: float
    ) -> PreCaptureOutcome:
        deadline = time.monotonic() + self.traversal_timeout_seconds
        seen_ids: set[str] = set()
        page_observations: list[dict[str, object]] = []
        total_products: int | None = None
        try:
            page.wait_for_timeout(  # type: ignore[union-attr]
                min(
                    _COUNTRY_DIALOG_POST_NAV_WAIT_MS,
                    int(setup_timeout_ms),
                    _remaining_ms(deadline),
                )
            )
            dialog = page.locator(_COUNTRY_DIALOG_SELECTOR).filter(  # type: ignore[union-attr]
                has_text=_COUNTRY_DIALOG_DIAGNOSTIC
            )
            if dialog.count() and dialog.is_visible():
                self._geo_dialog_observed = True
                self._geo_dialog_persisted_after_continue = True
            for expected_page in range(1, self.page_count + 1):
                requested_page_url = _catalog_page_url(
                    self.target_url, page=expected_page
                )
                if expected_page > 1:
                    remaining_ms = _remaining_ms(deadline)
                    page.goto(  # type: ignore[union-attr]
                        requested_page_url,
                        wait_until="domcontentloaded",
                        timeout=remaining_ms,
                    )
                    page.wait_for_timeout(  # type: ignore[union-attr]
                        min(1_000, _remaining_ms(deadline))
                    )
                rendered_dom = page.content()  # type: ignore[union-attr]
                state = load_sephora_catalog_linkstore_page(
                    rendered_dom, source_url=requested_page_url
                )
                if state.requested_page != expected_page:
                    return self._failed(
                        f"page discontinuity: expected {expected_page}, "
                        f"observed {state.requested_page}",
                        page_observations,
                    )
                if state.serialized_country != "US":
                    return self._failed(
                        f"page {expected_page} did not serialize country=US",
                        page_observations,
                    )
                if total_products is None:
                    total_products = state.total_products
                elif state.total_products != total_products:
                    return self._failed(
                        f"declared total changed on page {expected_page}",
                        page_observations,
                    )
                page_ids = [
                    str(product.get("productId") or "").strip()
                    for product in state.products
                ]
                if any(not product_id for product_id in page_ids):
                    return self._failed(
                        f"page {expected_page} exposed an empty product identity",
                        page_observations,
                    )
                overlap = seen_ids.intersection(page_ids)
                if overlap:
                    return self._failed(
                        f"duplicate product identities crossed page {expected_page}",
                        page_observations,
                    )
                seen_ids.update(page_ids)
                self._grid_page_doms.append(rendered_dom)
                self._grid_page_urls.append(requested_page_url)
                page_observations.append(
                    {
                        "page": expected_page,
                        "productCount": len(page_ids),
                        "resultId": state.result_id,
                        "finalUrl": str(page.url),  # type: ignore[union-attr]
                    }
                )
                if len(seen_ids) >= state.total_products:
                    break
        except Exception as exc:
            return self._failed(
                f"traversal failed ({type(exc).__name__}: {exc})",
                page_observations,
            )
        termination = (
            "retailer_terminal_reconciled"
            if total_products is not None and len(seen_ids) >= total_products
            else "requested_page_window_reconciled"
        )
        self._grid_observation = {
            "requestedPageCount": self.page_count,
            "capturedPageCount": len(self._grid_page_doms),
            "extractedUniqueParentCount": len(seen_ids),
            "duplicatePlacementCount": 0,
            "pageObservations": page_observations,
            "termination": termination,
            "geoShippingDialogObserved": self._geo_dialog_observed,
            "geoShippingDialogPersistedAfterContinue": (
                self._geo_dialog_persisted_after_continue
            ),
        }
        warning = (
            _COUNTRY_DIALOG_PERSISTED_WARNING
            if (
                self._geo_dialog_persisted_after_continue
                and not self._geo_dialog_warning_emitted
            )
            else None
        )
        self._geo_dialog_warning_emitted = bool(
            self._geo_dialog_warning_emitted or warning
        )
        return _outcome(warning=warning)

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        del rendered_dom
        confirmed = bool(self._grid_page_doms) and all(
            load_sephora_catalog_linkstore_page(dom, source_url=url).serialized_country
            == "US"
            for dom, url in zip(self._grid_page_doms, self._grid_page_urls)
        )
        return PinConfirmation(
            confirmed=confirmed,
            detail=(
                "every retained Sephora PageJSON page serialized country=US; "
                "origin country, currency, and delivery eligibility remain unpinned"
                if confirmed
                else "retained Sephora PageJSON pages did not unanimously bind country=US"
            ),
        )

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        reason = confirmation.detail
        if not outcome.steps_completed and outcome.reason:
            reason = f"{outcome.reason}; {reason}"
        return (
            "declared_storefront_country: Sephora catalog route CONFIRMED as US "
            f"({reason})"
            if confirmation.confirmed
            else f"declared_storefront_country: Sephora catalog route NOT confirmed ({reason})"
        )

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "sephora_catalog_bounded_pagejson_traversal",
            "market_page_kind": "grid",
            "country_code_requested": "US",
            "currency_code_requested": None,
            "market_confirmation_scope": "retailer_serialized_country_route_only",
            "market_preference_action": (
                "explicit_continue_attempt_then_serialized_country_validation"
            ),
            **self._grid_observation,
        }

    def _failed(
        self, reason: str, observations: list[dict[str, object]]
    ) -> PreCaptureOutcome:
        self._grid_observation = {
            "requestedPageCount": self.page_count,
            "capturedPageCount": len(self._grid_page_doms),
            "extractedUniqueParentCount": len(
                {
                    str(product.get("productId"))
                    for dom, url in zip(self._grid_page_doms, self._grid_page_urls)
                    for product in load_sephora_catalog_linkstore_page(
                        dom, source_url=url
                    ).products
                }
            ),
            "pageObservations": list(observations),
            "termination": "unproven",
            "failure": reason,
            "geoShippingDialogObserved": self._geo_dialog_observed,
            "geoShippingDialogPersistedAfterContinue": (
                self._geo_dialog_persisted_after_continue
            ),
        }
        return _outcome(reason=reason)


def _catalog_page_url(url: str, *, page: int) -> str:
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["currentPage"] = str(page)
    query["sortBy"] = "BEST_SELLING"
    return urlunparse(parsed._replace(query=urlencode(query)))


def _remaining_ms(deadline: float) -> int:
    remaining = int((deadline - time.monotonic()) * 1000)
    if remaining <= 0:
        raise TimeoutError("Sephora catalog traversal timeout exhausted")
    return remaining


def _outcome(
    *, reason: str | None = None, warning: str | None = None
) -> PreCaptureOutcome:
    return PreCaptureOutcome(
        attempted=True,
        steps_completed=reason is None,
        reason=reason,
        warning_notes=[warning] if warning else [],
    )


__all__ = ["SephoraCatalogTraversalPlugin"]
