"""Tests for the creator-momentum typed metric observation (IG capture-shape contract).

These exercise the CORE substrate landed by the IG typed-capture build: the ``MetricObservation``
value<->posture coupling, the ``MetricPosture`` set, and the additive-optional ``metric_observations``
field on ``SourceCaptureSlice``. The load-bearing invariant is that absence / out-of-window /
not-attempted / blocked / not-applicable can NEVER be stored as an observed value -- in particular,
never as an observed ``0`` -- while a genuine observed ``0`` is recordable. The field is additive and
optional, so existing v1 manifests stay valid with no manifest bump (back-compat tests below).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from source_capture.models import (
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    SourceCaptureSlice,
)

NON_OBSERVED = [
    MetricPosture.UNAVAILABLE_WITH_REASON,
    MetricPosture.OUT_OF_CAPTURE_WINDOW,
    MetricPosture.NOT_ATTEMPTED,
    MetricPosture.NOT_APPLICABLE,
]


def test_observed_metric_requires_value_and_no_reason() -> None:
    obs = MetricObservation(metric="view_count", posture=MetricPosture.OBSERVED, value=12345)
    assert obs.value == 12345
    assert obs.reason is None


def test_observed_zero_is_a_real_observed_value() -> None:
    # The whole point: a genuine 0 (a video with zero views) is an OBSERVED 0, not absence.
    obs = MetricObservation(metric="view_count", posture=MetricPosture.OBSERVED, value=0)
    assert obs.value == 0
    assert obs.posture == MetricPosture.OBSERVED


def test_observed_metric_without_value_is_rejected() -> None:
    with pytest.raises(ValidationError, match="observed metric requires a value"):
        MetricObservation(metric="view_count", posture=MetricPosture.OBSERVED)


def test_observed_metric_with_reason_is_rejected() -> None:
    with pytest.raises(ValidationError, match="observed metric must not carry a reason"):
        MetricObservation(
            metric="view_count", posture=MetricPosture.OBSERVED, value=10, reason="why"
        )


@pytest.mark.parametrize("posture", NON_OBSERVED)
def test_non_observed_metric_requires_reason_and_no_value(posture: MetricPosture) -> None:
    obs = MetricObservation(metric="view_count", posture=posture, reason="image post has no views")
    assert obs.value is None
    assert obs.reason


@pytest.mark.parametrize("posture", NON_OBSERVED)
def test_non_observed_metric_with_value_is_rejected(posture: MetricPosture) -> None:
    # Absence must never be stored as an observed value -- including the fake-momentum 0.
    with pytest.raises(ValidationError, match="must not carry a value"):
        MetricObservation(metric="view_count", posture=posture, value=0, reason="r")


@pytest.mark.parametrize("posture", NON_OBSERVED)
def test_non_observed_metric_without_reason_is_rejected(posture: MetricPosture) -> None:
    with pytest.raises(ValidationError, match="requires a reason"):
        MetricObservation(metric="view_count", posture=posture)


def test_not_applicable_is_distinct_from_a_value() -> None:
    # An image post genuinely has no view_count: not_applicable + reason, no value.
    obs = MetricObservation(
        metric="view_count",
        posture=MetricPosture.NOT_APPLICABLE,
        reason="image post carries no video_view_count",
    )
    assert obs.value is None
    assert obs.posture == MetricPosture.NOT_APPLICABLE


@pytest.mark.parametrize("blank", ["", "   ", "\t"])
def test_metric_identity_must_be_non_empty(blank: str) -> None:
    with pytest.raises(ValidationError, match="non-empty token"):
        MetricObservation(metric=blank, posture=MetricPosture.NOT_ATTEMPTED, reason="r")


def test_metric_identity_is_whitespace_normalized() -> None:
    # Surrounding whitespace is stripped so "  view_count  " and "view_count" are one identity.
    obs = MetricObservation(metric="  view_count  ", posture=MetricPosture.NOT_ATTEMPTED, reason="r")
    assert obs.metric == "view_count"


@pytest.mark.parametrize("posture", NON_OBSERVED)
def test_non_observed_whitespace_only_reason_is_rejected(posture: MetricPosture) -> None:
    # A blank / whitespace-only reason is no reason: a non-observed metric must carry a real one.
    with pytest.raises(ValidationError, match="requires a reason"):
        MetricObservation(metric="view_count", posture=posture, reason="   ")


def test_reason_is_whitespace_normalized_when_present() -> None:
    obs = MetricObservation(
        metric="view_count",
        posture=MetricPosture.NOT_APPLICABLE,
        reason="  image post has no views  ",
    )
    assert obs.reason == "image post has no views"


def test_coverage_window_is_optional_and_accepted() -> None:
    obs = MetricObservation(
        metric="view_count",
        posture=MetricPosture.OBSERVED,
        value=7,
        coverage_window=CoverageWindow(start="2026-06-01T00:00:00Z", end="2026-06-15T00:00:00Z"),
    )
    assert obs.coverage_window is not None
    assert obs.coverage_window.start == "2026-06-01T00:00:00Z"


def test_extra_keys_are_forbidden() -> None:
    with pytest.raises(ValidationError):
        MetricObservation(metric="view_count", posture="observed", value=1, bogus="x")


def test_observation_round_trips_through_model_dump() -> None:
    obs = MetricObservation(metric="like_count", posture=MetricPosture.OBSERVED, value=42)
    assert MetricObservation.model_validate(obs.model_dump()) == obs


def _minimal_slice_payload() -> dict[str, object]:
    unknown = {"status": "unknown_with_reason", "reason": "not supplied"}
    return {
        "slice_id": "slice_01",
        "locator": {"status": "known", "value": "https://example.test/p/1"},
        "timing": {
            "source_publication_or_event": unknown,
            "source_edit_or_version": unknown,
            "capture_time": {"status": "known", "value": "2026-06-15T00:00:00Z"},
            "recapture_time": {"status": "not_applicable", "reason": "first capture"},
            "cutoff_posture": unknown,
        },
        "access_posture": {"status": "known", "value": "logged_out_public"},
        "archive_history_posture": {"status": "not_attempted", "reason": "not queried"},
        "media_modality_posture": {"status": "not_attempted", "reason": "not assessed"},
        "re_capture_relationship": {"status": "not_applicable", "reason": "first capture"},
    }


def test_legacy_slice_without_observations_stays_valid() -> None:
    # Back-compat: a slice with NO metric_observations key (a legacy / non-momentum capture) still
    # validates under extra="forbid" and defaults to an empty list -- proving no manifest bump is
    # required to add the field.
    source_slice = SourceCaptureSlice.model_validate(_minimal_slice_payload())
    assert source_slice.metric_observations == []


def test_slice_with_observations_round_trips() -> None:
    payload = _minimal_slice_payload()
    payload["metric_observations"] = [
        {"metric": "view_count", "posture": "observed", "value": 12345},
        {
            "metric": "view_count",
            "posture": "not_applicable",
            "reason": "image post carries no video_view_count",
        },
    ]
    source_slice = SourceCaptureSlice.model_validate(payload)
    assert len(source_slice.metric_observations) == 2
    assert source_slice.metric_observations[0].value == 12345
    assert source_slice.metric_observations[1].value is None
    assert SourceCaptureSlice.model_validate(source_slice.model_dump()) == source_slice


def test_slice_rejects_an_observed_metric_with_no_value() -> None:
    # The coupling is enforced through the slice too (nested validation), not only standalone.
    payload = _minimal_slice_payload()
    payload["metric_observations"] = [{"metric": "view_count", "posture": "observed"}]
    with pytest.raises(ValidationError, match="observed metric requires a value"):
        SourceCaptureSlice.model_validate(payload)
