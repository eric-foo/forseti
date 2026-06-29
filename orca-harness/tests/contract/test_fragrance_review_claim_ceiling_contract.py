"""Claim-ceiling contract for the fragrance purchase-review producers.

The fragrance review capture lane preserves raw widget-response bytes and
re-derives views from them. It is deliberately NOT a durable, typed Attachment
Record: no AR physicalization, no data-lake "7 acceptance checks", no closure --
the typed AR entry stays data-lake-lane work.

That ceiling currently lives only as a default ``non_claims`` entry on each
producer, which a future edit could silently drop and thereby upgrade the claim
past the honesty boundary. This contract locks it in code: every fragrance
review producer must keep declaring "not durable Attachment Records", so the
upgrade cannot happen without consciously changing this test.
"""
from __future__ import annotations

from pydantic import BaseModel

from source_capture.fragrance_rendered_widget_companion import (
    FragranceRenderedWidgetCompanionReceipt,
)
from source_capture.fragrance_review_coverage import FragranceReviewCoverageReceipt
from source_capture.fragrance_review_lake import FRAGRANCE_REVIEW_LAKE_NON_CLAIMS

_ATTACHMENT_RECORD_NON_CLAIM = "not durable Attachment Records"


def _default_non_claims(model: type[BaseModel]) -> list[str]:
    """The model's declared default ``non_claims``, whether set via a
    ``default_factory`` or a plain ``default`` (robust to either field style)."""
    field = model.model_fields["non_claims"]
    if field.default_factory is not None:
        return list(field.default_factory())
    return list(field.default)


def test_fragrance_review_lake_non_claims_disclaim_attachment_records() -> None:
    assert _ATTACHMENT_RECORD_NON_CLAIM in FRAGRANCE_REVIEW_LAKE_NON_CLAIMS


def test_fragrance_rendered_widget_companion_receipt_disclaims_attachment_records() -> None:
    assert _ATTACHMENT_RECORD_NON_CLAIM in _default_non_claims(FragranceRenderedWidgetCompanionReceipt)


def test_fragrance_review_coverage_receipt_disclaims_attachment_records() -> None:
    assert _ATTACHMENT_RECORD_NON_CLAIM in _default_non_claims(FragranceReviewCoverageReceipt)
