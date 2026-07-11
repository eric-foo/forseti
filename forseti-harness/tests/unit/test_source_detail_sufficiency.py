from __future__ import annotations

import argparse

import pytest

from source_capture.source_detail_sufficiency import (
    SourceDetailSufficiencyRequirements,
    build_source_detail_sufficiency_requirements,
    evaluate_source_detail_sufficiency,
    source_detail_sufficiency_failure_message,
    source_detail_sufficiency_limitation,
    source_detail_sufficiency_mode_change,
)


def test_source_detail_sufficiency_disabled_passes_without_claim() -> None:
    result = evaluate_source_detail_sufficiency(
        requirements=None,
        access_block_reason="cloudflare_interstitial",
        visible_text="",
        rendered_dom="",
    )

    assert result.enabled is False
    assert result.passed is True
    assert source_detail_sufficiency_mode_change(result) is None
    assert source_detail_sufficiency_limitation(result) is None


def test_source_detail_sufficiency_reports_missing_required_details() -> None:
    result = evaluate_source_detail_sufficiency(
        requirements=SourceDetailSufficiencyRequirements(
            require_not_access_blocked=True,
            min_visible_text_bytes=10,
            visible_text_contains=("B2B question title",),
            visible_text_regexes=(r"customer discovery\?",),
            rendered_dom_regexes=(r"https://www\.quora\.com/.+B2B",),
        ),
        access_block_reason="cloudflare_interstitial",
        visible_text="short",
        rendered_dom="<html></html>",
    )

    assert result.enabled is True
    assert result.passed is False
    assert result.failure_reasons == (
        "access blocked: cloudflare_interstitial",
        "visible text too small: 5 bytes < required 10",
        "missing visible text literal: 'B2B question title'",
        "missing visible text regex: 'customer discovery\\\\?'",
        "missing rendered DOM regex: 'https://www\\\\.quora\\\\.com/.+B2B'",
    )
    assert source_detail_sufficiency_mode_change(result) == "source_detail_sufficiency_failed"
    assert source_detail_sufficiency_limitation(result).startswith("source_detail_sufficiency_failed")
    assert "packet-dir" in source_detail_sufficiency_failure_message(
        output_directory="packet-dir",
        result=result,
    )


def test_source_detail_sufficiency_passes_when_all_required_details_are_present() -> None:
    result = evaluate_source_detail_sufficiency(
        requirements=SourceDetailSufficiencyRequirements(
            require_not_access_blocked=True,
            min_visible_text_bytes=20,
            visible_text_contains=("Results for B2B questions",),
            visible_text_regexes=(r"customer discovery\?",),
            rendered_dom_regexes=(r"https://www\.quora\.com/.+B2B",),
        ),
        access_block_reason=None,
        visible_text="Results for B2B questions: customer discovery?",
        rendered_dom='<a href="https://www.quora.com/What-are-good-B2B-questions">link</a>',
    )

    assert result.enabled is True
    assert result.passed is True
    assert source_detail_sufficiency_mode_change(result) == "source_detail_sufficiency_passed"
    assert source_detail_sufficiency_limitation(result) is None


def test_source_detail_sufficiency_rejects_blank_and_bad_requirements() -> None:
    with pytest.raises(ValueError, match="must be non-negative"):
        build_source_detail_sufficiency_requirements(
            argparse.Namespace(
                require_not_access_blocked=False,
                require_min_visible_text_bytes=-1,
                require_visible_text=[],
                require_visible_regex=[],
                require_rendered_dom_text=[],
                require_rendered_dom_regex=[],
            )
        )

    with pytest.raises(ValueError, match="must not be blank"):
        build_source_detail_sufficiency_requirements(
            argparse.Namespace(
                require_not_access_blocked=False,
                require_min_visible_text_bytes=None,
                require_visible_text=[""],
                require_visible_regex=[],
                require_rendered_dom_text=[],
                require_rendered_dom_regex=[],
            )
        )

    with pytest.raises(ValueError, match="not a valid regex"):
        build_source_detail_sufficiency_requirements(
            argparse.Namespace(
                require_not_access_blocked=False,
                require_min_visible_text_bytes=None,
                require_visible_text=[],
                require_visible_regex=["["],
                require_rendered_dom_text=[],
                require_rendered_dom_regex=[],
            )
        )
