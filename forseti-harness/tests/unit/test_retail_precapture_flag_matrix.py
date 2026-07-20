"""Pairwise coverage for the retail pre-capture site-specific-preference exclusion,
plus argparse ``choices`` enforcement for the market flags that previously only had
an echo-only happy-path CLI test.

The writer (``runners/run_source_capture_cloakbrowser_packet.py``) allows at most
one of six site-specific pre-capture preferences per invocation (delivery_zip,
nordstrom_country, luckyscent_market, sephora_market, ulta_market, target_zip).
Each site's own test file previously proved only one pair (its flag vs. one other
flag), leaving most of the C(6, 2) = 15 possible pairs unproven anywhere. This file
completes the matrix. It also proves, for the market flags that previously only had
an echo-only CLI test (walmart, ulta, credo), that an invalid value is rejected by
argparse's ``choices`` enforcement -- not just that a valid one round-trips.
"""
from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from runners import run_source_capture_http_packet as http_writer


_URL = "https://example.com/products/pdp-fixture"


def _run_writer(tmp_path: Path, **overrides: Any) -> tuple[int, str]:
    kwargs: dict[str, Any] = {
        "url": _URL,
        "source_family": "retail_pdp",
        "source_surface": "cloakbrowser_snapshot",
        "decision_question": "Does the bound PDP render?",
        "output_directory": tmp_path / "packet",
        "capture_context": "offline test",
        "operator_category": "test",
        "capture_mode": cloak_writer.CaptureModeCategory.MULTIMODAL,
        "session_id": None,
        "proxy_profile": None,
        "actor_audience_context": cloak_writer.unknown_with_reason("not needed"),
        "visible_mode_changes": [],
        "source_publication_or_event": cloak_writer.unknown_with_reason("not needed"),
        "source_edit_or_version": cloak_writer.unknown_with_reason("not needed"),
        "cutoff_posture": cloak_writer.unknown_with_reason("not needed"),
        "recapture_time": cloak_writer.not_applicable("not needed"),
        "re_capture_relationship": cloak_writer.not_applicable("not needed"),
        "warnings": [],
        "limitations": [],
        "timeout_seconds": 30,
        "wait_until": "load",
        "viewport_width": 1920,
        "viewport_height": 1080,
        "max_artifact_bytes": 5_000_000,
        "block_heavy_assets": False,
    }
    kwargs.update(overrides)
    return cloak_writer.run_source_capture_cloakbrowser_packet(**kwargs)


# --- pairwise site-specific pre-capture preference matrix ---

_SITE_SPECIFIC_PRE_CAPTURE_FLAGS = (
    "delivery_zip",
    "nordstrom_country",
    "luckyscent_market",
    "sephora_market",
    "ulta_market",
    "target_zip",
)
_SITE_SPECIFIC_PRE_CAPTURE_FLAG_VALUES = {
    "delivery_zip": "10001",
    "nordstrom_country": "US",
    "luckyscent_market": "US",
    "sephora_market": "US",
    "ulta_market": "US",
    "target_zip": "10001",
}


@pytest.mark.parametrize(
    ("flag_a", "flag_b"),
    list(itertools.combinations(_SITE_SPECIFIC_PRE_CAPTURE_FLAGS, 2)),
)
def test_writer_rejects_every_site_specific_pre_capture_pair(
    tmp_path: Path, flag_a: str, flag_b: str
) -> None:
    with pytest.raises(ValueError, match="only one site-specific pre-capture"):
        _run_writer(
            tmp_path,
            **{
                flag_a: _SITE_SPECIFIC_PRE_CAPTURE_FLAG_VALUES[flag_a],
                flag_b: _SITE_SPECIFIC_PRE_CAPTURE_FLAG_VALUES[flag_b],
            },
        )


# --- CLI ``choices=["US"]`` enforcement for previously echo-only market flags ---

_ULTA_CLI_BASE_ARGS = [
    "--url",
    "https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2645443",
    "--decision-question",
    "Ulta US/USD?",
    "--output",
    "packet",
    "--ulta-market",
]
_WALMART_CLI_BASE_ARGS = [
    "--url",
    "https://www.walmart.com/ip/Vitamasques-Cherry-Vegan-Collagen-Lip-Mask-"
    "Moisturise-Plump-One-Patch/2150828728",
    "--decision-question",
    "Walmart US/USD?",
    "--output",
    "packet",
    "--retail-capture-profile",
    "walmart_pdp_aggregate",
    "--walmart-market",
]
_CREDO_CLI_BASE_ARGS = [
    "--url",
    "https://credobeauty.com/products/sos-save-our-skin-daily-rescue-facial-spray",
    "--source-family",
    "retail_pdp",
    "--decision-question",
    "Credo US/USD?",
    "--output",
    "packet",
    "--credo-market",
]


@pytest.mark.parametrize(
    ("writer_module", "dest_attr", "base_args"),
    [
        pytest.param(cloak_writer, "ulta_market", _ULTA_CLI_BASE_ARGS, id="ulta"),
        pytest.param(http_writer, "walmart_market", _WALMART_CLI_BASE_ARGS, id="walmart"),
        pytest.param(http_writer, "credo_market", _CREDO_CLI_BASE_ARGS, id="credo"),
    ],
)
def test_market_flag_cli_accepts_us_and_rejects_other_choice(
    writer_module: Any, dest_attr: str, base_args: list[str]
) -> None:
    parser = writer_module._build_parser()

    args = parser.parse_args([*base_args, "US"])
    assert getattr(args, dest_attr) == "US"

    with pytest.raises(SystemExit):
        parser.parse_args([*base_args, "CA"])
