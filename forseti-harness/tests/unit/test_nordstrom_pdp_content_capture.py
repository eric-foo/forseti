from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import pytest

from runners import run_source_capture_cloakbrowser_packet as runner
from runners.run_nordstrom_pdp_parser_fit_check import (
    ParserFitCheckError,
    check_nordstrom_pdp_parser_fit,
    run_nordstrom_pdp_parser_fit_check,
)
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.content_capture import RenderedContentCaptureSpec
from source_capture.models import SourceCapturePacket
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_pdp_projection import (
    NORDSTROM_PDP_CONTENT_RECORD_KIND,
    NORDSTROM_PDP_PARSER_VERSION,
    build_nordstrom_pdp_aggregate_content_record,
    build_retail_pdp_projection_from_packet_directory,
)
from source_capture.retail_pdp_silver import build_retail_pdp_silver_records


_URL = "https://www.nordstrom.com/s/the-lip-balm/8260802"
_UNRELATED_URL = "https://www.nordstrom.com/s/unrelated-product/9999999"
_PRODUCT = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "The Lip Balm",
    "brand": {"@type": "Brand", "name": "Nécessaire"},
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 4.6,
        "reviewCount": 118,
    },
    "offers": {
        "@type": "Offer",
        "price": "28.00",
        "availability": "http://schema.org/InStock",
        "priceCurrency": "USD",
        "url": _URL,
    },
    "description": "<b>What it is:</b> Relief for dry lips.",
}
_PRODUCT_DUPLICATE = {
    **_PRODUCT,
    "offers": {
        "@type": "Offer",
        "price": "28.00",
        "availability": "http://schema.org/InStock",
        "priceCurrency": "USD",
    },
}
_UNRELATED = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "Recommendation Product",
    "brand": {"@type": "Brand", "name": "Other Brand"},
    "offers": {
        "@type": "Offer",
        "price": "999.00",
        "availability": "http://schema.org/InStock",
        "priceCurrency": "USD",
        "url": _UNRELATED_URL,
    },
}

_DOM = f"""<!doctype html>
<html><body>
<a href="/s/the-lip-balm/8260802">The Lip Balm</a>
<script type="application/ld+json">{json.dumps(_PRODUCT, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(_PRODUCT_DUPLICATE, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(_UNRELATED, ensure_ascii=False)}</script>
<div id="product-page-reviews">
  <span itemprop="review" itemtype="https://schema.org/Review">
    <span itemprop="name" content="Just okay"></span>
    <span itemprop="author" content="Cfmcl"></span>
    <meta itemprop="datePublished" content="2025-09-16T10:54:39.000+00:00">
    <span itemprop="reviewRating"><span itemprop="ratingValue" content="3"></span></span>
    <span itemprop="reviewBody" content="It is average but source-visible."></span>
  </span>
  <span itemprop="review" itemtype="https://schema.org/Review">
    <span itemprop="name" content="Sticky and nothing special"></span>
    <span itemprop="author" content="DogMom72"></span>
    <meta itemprop="datePublished" content="2025-03-09T10:54:39.000+00:00">
    <span itemprop="reviewRating"><span itemprop="ratingValue" content="2"></span></span>
    <span itemprop="reviewBody" content="It is sticky and gets on my mug."></span>
  </span>
  <span itemprop="review" itemtype="https://schema.org/Review">
    <span itemprop="name" content="Amazing lip balm"></span>
    <span itemprop="author" content="Cendully"></span>
    <meta itemprop="datePublished" content="2026-03-16T17:22:14.000+00:00">
    <span itemprop="reviewRating"><span itemprop="ratingValue" content="5"></span></span>
    <span itemprop="reviewBody" content="The metal applicator feels cooling."></span>
  </span>
  <span itemprop="review" itemtype="https://schema.org/Review">
    <span itemprop="name" content="BEST LIP BALM EVER"></span>
    <span itemprop="author" content="Amazinggggggg"></span>
    <meta itemprop="datePublished" content="2025-07-10T10:54:39.000+00:00">
    <span itemprop="reviewRating"><span itemprop="ratingValue" content="5"></span></span>
    <span itemprop="reviewBody" content="Hydrating with a lip gloss appearance."></span>
  </span>
  <span itemprop="review" itemtype="https://schema.org/Review">
    <span itemprop="name" content="Best ever used"></span>
    <span itemprop="author" content="spotintheshade"></span>
    <meta itemprop="datePublished" content="2025-04-19T10:54:39.000+00:00">
    <span itemprop="reviewRating"><span itemprop="ratingValue" content="5"></span></span>
    <span itemprop="reviewBody" content="It relieves chapped lips."></span>
  </span>
  <span itemprop="review" itemtype="https://schema.org/Review">
    <span itemprop="name" content="Excellent"></span>
    <span itemprop="author" content="Vicki C."></span>
    <meta itemprop="datePublished" content="2026-06-13T10:54:39.000+00:00">
    <span itemprop="reviewRating"><span itemprop="ratingValue" content="5"></span></span>
    <span itemprop="reviewBody" content="This balm is soft and lasts."></span>
  </span>
  <div id="sort-by-filter-8260802-anchor"><span>Sort by <strong>Most Helpful</strong></span></div>
  <div id="review-1"><span><strong>9</strong></span><span>found this helpful</span></div>
  <div id="review-2"><span><strong>4</strong></span><span>found this helpful</span></div>
  <div id="review-3"><span><strong>2</strong></span><span>found this helpful</span></div>
  <div id="review-4"><span><strong>2</strong></span><span>found this helpful</span></div>
  <div id="review-5"><span><strong>1</strong></span><span>found this helpful</span></div>
  <div id="review-6"><span>Be the first to find this helpful</span></div>
  <a href="?page=2">Load 6 more reviews</a>
</div>
<button>Add to Bag</button>
<footer>Nordstrom Card &amp; Rewards</footer>
</body></html>
"""

_VISIBLE_TEXT = """Main content
Home
Beauty
(118)
The Lip Balm
Nécessaire
$28.00
Current Price $28.00
One Size
Sold by Nordstrom
Select fulfillment method
Pickup at choose store
No stores found near your location
Shipping to 518225
Add to Bag
You Might Also Like
Highlights
Cruelty-free
Hypoallergenic
Hyaluronic acid
Details & care
What it is: A lip balm that's instant relief for dry, chapped or compromised lips.
What it does: Essential ceramides and niacinamide help repair dryness.
How to use: Use when needed, day and night.
Dermatologist tested
Hypoallergenic
Noncomedogenic
Cruelty-free
Item #10743748
Core Product ID 333333SNBL
Ingredients
Shea Butter, Niacinamide
Shipping & returns
Free shipping. Free returns.
Gift options
Reviews
(118)
4.6 out of 5
Write a Review
5 stars
81%
4 stars
7%
3 stars
3%
2 stars
5%
1 star
3%
Sort by Most Helpful
Load 6 more reviews
Recommended for You
"""


def _success(
    *,
    pin_confirmed: bool = True,
    rendered_dom: str = _DOM,
    visible_text: str = _VISIBLE_TEXT,
) -> CloakBrowserSnapshotSuccess:
    return CloakBrowserSnapshotSuccess(
        requested_url=_URL,
        final_url=_URL,
        title="The Lip Balm",
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        screenshot_png=b"\x89PNG\r\n\x1a\nnordstrom",
        metadata={
            "capture_timestamp": "2026-07-19T00:00:00Z",
            "requested_url": _URL,
            "final_url": _URL,
            "pin_confirmed": pin_confirmed,
            "proxy_used": False,
            "persistent_profile_loaded": False,
            "storage_state_loaded": False,
        },
        warning_notes=[],
        limitation_notes=[],
    )


def _run(
    *,
    output: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str | None,
    capture_factory: Callable[[], CloakBrowserSnapshotSuccess] = _success,
    projector=None,
) -> tuple[int, str]:
    monkeypatch.setattr(
        runner, "fetch_cloakbrowser_snapshot_capture", lambda **_kwargs: capture_factory()
    )
    content_capture = (
        None
        if mode is None
        else RenderedContentCaptureSpec(
            capture_artifact_mode=mode,
            parser_version=NORDSTROM_PDP_PARSER_VERSION,
            projector=projector
            or (
                lambda rendered_dom, visible_text, final_url: (
                    build_nordstrom_pdp_aggregate_content_record(
                        rendered_dom=rendered_dom,
                        visible_text=visible_text,
                        source_url=final_url,
                    )
                )
            ),
        )
    )
    return runner.run_source_capture_cloakbrowser_packet(
        url=_URL,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="What target-bound Nordstrom PDP facts are visible?",
        output_directory=output,
        capture_context="Nordstrom content-mode unit proof",
        operator_category="unit_test",
        capture_mode=runner.CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=runner.unknown_with_reason("not supplied"),
        visible_mode_changes=[],
        source_publication_or_event=runner.unknown_with_reason("not supplied"),
        source_edit_or_version=runner.unknown_with_reason("not supplied"),
        cutoff_posture=runner.unknown_with_reason("not supplied"),
        recapture_time=runner.not_applicable("first capture"),
        re_capture_relationship=runner.not_applicable("first capture"),
        warnings=[],
        limitations=[],
        retail_capture_profile=get_retail_capture_profile(
            "nordstrom_pdp_aggregate"
        ),
        timeout_seconds=30,
        wait_until="domcontentloaded",
        viewport_width=1920,
        viewport_height=1080,
        max_artifact_bytes=10_000_000,
        block_heavy_assets=False,
        settle_seconds=5,
        scroll_passes=1,
        scroll_step_px=500,
        nordstrom_country="US",
        series_id="nordstrom_necessaire_lip_balm_us_v0",
        locale_pin=runner.known_fact("en-US"),
        currency_pin=runner.known_fact("USD"),
        variant_pin=runner.known_fact("product_id=8260802"),
        content_capture=content_capture,
    )


def _manifest(packet_dir: Path) -> dict[str, Any]:
    return json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))


def _logical_name(relative_path: str) -> str:
    name = Path(relative_path.replace("\\", "/")).name
    return name[3:] if len(name) > 3 and name[:2].isdigit() and name[2] == "_" else name


def _artifact_path(packet_dir: Path, filename: str) -> Path:
    return next(
        packet_dir / item["relative_packet_path"]
        for item in _manifest(packet_dir)["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == filename
    )


def _packet(packet_dir: Path) -> SourceCapturePacket:
    return SourceCapturePacket.model_validate(_manifest(packet_dir))


def _rewrite_artifact_and_manifest(
    packet_dir: Path, filename: str, body: bytes
) -> None:
    manifest = _manifest(packet_dir)
    item = next(
        item
        for item in manifest["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == filename
    )
    (packet_dir / item["relative_packet_path"]).write_bytes(body)
    item["sha256"] = hashlib.sha256(body).hexdigest()
    item["size_bytes"] = len(body)
    (packet_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _mutate_json(
    packet_dir: Path, filename: str, mutate: Callable[[dict[str, Any]], None]
) -> None:
    payload = json.loads(_artifact_path(packet_dir, filename).read_text(encoding="utf-8"))
    mutate(payload)
    _rewrite_artifact_and_manifest(
        packet_dir,
        filename,
        (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(
            "utf-8"
        ),
    )


@pytest.mark.parametrize(
    ("mode", "raw_inputs_present", "record_present"),
    [("content", False, True), ("sample", True, True), ("raw", True, False)],
)
def test_nordstrom_capture_artifact_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    raw_inputs_present: bool,
    record_present: bool,
) -> None:
    packet_dir = tmp_path / mode
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=mode)[0] == 0
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert ("cloakbrowser_rendered_dom.html" in names) is raw_inputs_present
    assert ("cloakbrowser_visible_text.txt" in names) is raw_inputs_present
    assert ("content_record.json" in names) is record_present
    assert "content_capture_metadata.json" in names
    assert "cloakbrowser_snapshot_metadata.json" in names
    assert "cloakbrowser_viewport_screenshot.png" in names


def test_nordstrom_profile_defaults_to_content_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet_dir = tmp_path / "default"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=None)[0] == 0
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert "content_record.json" in names
    assert "cloakbrowser_rendered_dom.html" not in names
    assert "cloakbrowser_visible_text.txt" not in names


def test_cli_defaults_nordstrom_profile_to_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        runner, "fetch_cloakbrowser_snapshot_capture", lambda **_kwargs: _success()
    )
    packet_dir = tmp_path / "cli"
    assert (
        runner.main(
            [
                "--url",
                _URL,
                "--source-family",
                "retail_pdp",
                "--source-surface",
                "cloakbrowser_snapshot",
                "--decision-question",
                "What target-bound Nordstrom facts are visible?",
                "--output",
                str(packet_dir),
                "--retail-capture-profile",
                "nordstrom_pdp_aggregate",
                "--nordstrom-country",
                "US",
            ]
        )
        == 0
    )
    assert str(packet_dir) in capsys.readouterr().out
    assert _artifact_path(packet_dir, "content_record.json").is_file()
    assert not any(
        _logical_name(item["relative_packet_path"])
        == "cloakbrowser_rendered_dom.html"
        for item in _manifest(packet_dir)["preserved_files"]
    )


def test_nordstrom_record_is_deterministic_target_scoped_and_complete() -> None:
    first = build_nordstrom_pdp_aggregate_content_record(
        rendered_dom=_DOM.encode(),
        visible_text=_VISIBLE_TEXT.encode(),
        source_url=_URL,
    )
    second = build_nordstrom_pdp_aggregate_content_record(
        rendered_dom=_DOM.encode(),
        visible_text=_VISIBLE_TEXT.encode(),
        source_url=_URL,
    )
    assert first == second
    assert first["record_kind"] == NORDSTROM_PDP_CONTENT_RECORD_KIND
    serialized = json.dumps(first, ensure_ascii=False, sort_keys=True)
    assert "Recommendation Product" not in serialized
    assert "999.00" not in serialized
    assert "content_record_unbound" not in serialized
    assert "content_input_rendered_dom" not in serialized

    offer = next(
        row["source_visible_fields"]
        for row in first["rows"]
        if row["row_kind"] == "retail_variant_offer"
    )
    review = next(
        row["source_visible_fields"]
        for row in first["rows"]
        if row["row_kind"] == "retail_review_substrate"
    )
    assert offer["product_id"] == "8260802"
    assert offer["product_name"] == "The Lip Balm"
    assert offer["brand"] == "Nécessaire"
    assert offer["price"] == "28.00"
    assert offer["seller"] == "Nordstrom"
    assert offer["shipping_destination_display"] == "Shipping to 518225"
    assert offer["shipping_availability"] is None
    assert review["rating"] == "4.6"
    assert review["review_count"] == "118"
    assert review["rating_distribution_buckets"] == {
        "5": "81%",
        "4": "7%",
        "3": "3%",
        "2": "5%",
        "1": "3%",
    }
    assert review["review_sort_posture"] == "Most Helpful"
    assert review["rendered_review_count"] == 6
    assert review["rendered_reviews"][0]["body"] == "It is average but source-visible."
    assert [
        item["helpful_count"] for item in review["rendered_reviews"]
    ] == ["9", "4", "2", "2", "1", None]
    assert [
        item["source_display_position"] for item in review["rendered_reviews"]
    ] == [1, 2, 3, 4, 5, 6]
    assert review["rendered_reviews"][1]["author"] == "DogMom72"
    assert review["rendered_reviews"][1]["helpful_count"] == "4"
    assert review["review_load_more_control_text"] == "Load 6 more reviews"
    assert review["review_load_more_batch_size"] == 6
    assert review["review_continuation_available"] is True
    assert "nordstrom_shipping_destination_display_is_not_delivery_pin" in first[
        "residuals"
    ]


def test_wrong_product_and_incomplete_review_substrate_fail_projection() -> None:
    with pytest.raises(ValueError, match="offer and one review|product id"):
        build_nordstrom_pdp_aggregate_content_record(
            rendered_dom=_DOM.encode(),
            visible_text=_VISIBLE_TEXT.encode(),
            source_url=_UNRELATED_URL,
        )
    with pytest.raises(ValueError, match="review"):
        build_nordstrom_pdp_aggregate_content_record(
            rendered_dom=_DOM.replace('id="product-page-reviews"', 'id="other"').encode(),
            visible_text=_VISIBLE_TEXT.encode(),
            source_url=_URL,
        )


def test_projection_failure_and_pin_failure_preserve_raw_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*_args):
        raise RuntimeError("fixture drift")

    projection_dir = tmp_path / "projection"
    assert (
        _run(
            output=projection_dir,
            monkeypatch=monkeypatch,
            mode="content",
            projector=fail,
        )[0]
        == runner.CONTENT_PROJECTION_FAILED_EXIT_CODE
    )
    pin_dir = tmp_path / "pin"
    assert (
        _run(
            output=pin_dir,
            monkeypatch=monkeypatch,
            mode="content",
            capture_factory=lambda: _success(pin_confirmed=False),
        )[0]
        == runner.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    )
    for packet_dir in (projection_dir, pin_dir):
        names = {
            _logical_name(item["relative_packet_path"])
            for item in _manifest(packet_dir)["preserved_files"]
        }
        assert "cloakbrowser_rendered_dom.html" in names
        assert "cloakbrowser_visible_text.txt" in names
        assert "cloakbrowser_viewport_screenshot.png" in names


def test_browser_secret_rejected_before_persistence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet_dir = tmp_path / "secret"
    with pytest.raises(ValueError, match="browser-secret"):
        _run(
            output=packet_dir,
            monkeypatch=monkeypatch,
            mode="content",
            capture_factory=lambda: _success(
                rendered_dom=_DOM + "<script>cf_clearance=secret</script>"
            ),
        )
    assert not packet_dir.exists()


def _semantic_projection(projection) -> dict[str, Any]:
    payload = projection.model_dump(mode="json")
    payload.pop("packet_id")
    for row in payload["rows"]:
        row.pop("raw_ref")
        row.pop("raw_anchor")
    for binding in payload["binding_map"]:
        binding.pop("raw_ref")
        binding.pop("raw_anchor")
    for entry in payload["loss_ledger"]["collapsed"]:
        entry.pop("raw_anchor")
    return payload


def _without_lineage(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_lineage(item)
            for key, item in value.items()
            if key not in {"raw_refs", "derived_refs"}
        }
    if isinstance(value, list):
        return [_without_lineage(item) for item in value]
    return value


def test_raw_and_content_projection_and_silver_are_equal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    raw_dir = tmp_path / "raw"
    content_dir = tmp_path / "content"
    assert _run(output=raw_dir, monkeypatch=monkeypatch, mode="raw")[0] == 0
    assert _run(output=content_dir, monkeypatch=monkeypatch, mode="content")[0] == 0
    raw_projection = build_retail_pdp_projection_from_packet_directory(
        packet_directory=raw_dir
    )
    content_projection = build_retail_pdp_projection_from_packet_directory(
        packet_directory=content_dir
    )
    assert _semantic_projection(raw_projection) == _semantic_projection(
        content_projection
    )
    assert all(
        row.raw_anchor.anchor_kind == "json_pointer"
        and row.raw_anchor.anchor_value.startswith("/rows/")
        for row in content_projection.rows
    )
    raw_silver = build_retail_pdp_silver_records(
        packet=_packet(raw_dir),
        projection=raw_projection,
        projection_record_id="projection.json",
        projection_sha256="a" * 64,
    )
    content_silver = build_retail_pdp_silver_records(
        packet=_packet(content_dir),
        projection=content_projection,
        projection_record_id="projection.json",
        projection_sha256="b" * 64,
    )
    assert [_without_lineage(record["payload"]) for record in raw_silver] == [
        _without_lineage(record["payload"]) for record in content_silver
    ]
    assert [record.get("residuals") for record in raw_silver] == [
        record.get("residuals") for record in content_silver
    ]


def test_parser_fit_match_and_fact_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet_dir = tmp_path / "sample"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    assert check_nordstrom_pdp_parser_fit(
        packet_or_manifest_path=packet_dir
    )["status"] == "match"

    _mutate_json(
        packet_dir,
        "content_record.json",
        lambda payload: next(
            row
            for row in payload["rows"]
            if row["row_kind"] == "retail_variant_offer"
        )["source_visible_fields"].update({"price": "29.00"}),
    )
    drift = check_nordstrom_pdp_parser_fit(packet_or_manifest_path=packet_dir)
    assert drift["status"] == "drift"
    assert drift["difference"]["path"].endswith("/price")


@pytest.mark.parametrize(
    ("filename", "mutate", "code"),
    [
        (
            "content_capture_metadata.json",
            lambda payload: payload.update({"parser_version": "old"}),
            "parser_version_mismatch",
        ),
        (
            "cloakbrowser_snapshot_metadata.json",
            lambda payload: payload["retail_capture_profile"].update(
                {"name": "sephora_pdp_aggregate"}
            ),
            "profile_mismatch",
        ),
        (
            "content_record.json",
            lambda payload: payload.update({"source_url": _UNRELATED_URL}),
            "source_mismatch",
        ),
    ],
)
def test_parser_fit_rejects_metadata_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    filename: str,
    mutate: Callable[[dict[str, Any]], None],
    code: str,
) -> None:
    packet_dir = tmp_path / code
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    _mutate_json(packet_dir, filename, mutate)
    with pytest.raises(ParserFitCheckError) as exc:
        check_nordstrom_pdp_parser_fit(packet_or_manifest_path=packet_dir)
    assert exc.value.code == code


def test_parser_fit_rejects_bad_hash_malformed_and_non_sample(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bad_hash = tmp_path / "bad-hash"
    assert _run(output=bad_hash, monkeypatch=monkeypatch, mode="sample")[0] == 0
    _artifact_path(bad_hash, "cloakbrowser_rendered_dom.html").write_bytes(b"drift")
    with pytest.raises(ParserFitCheckError) as exc:
        check_nordstrom_pdp_parser_fit(packet_or_manifest_path=bad_hash)
    assert exc.value.code == "preserved_file_mismatch"

    malformed = tmp_path / "malformed"
    assert _run(output=malformed, monkeypatch=monkeypatch, mode="sample")[0] == 0
    _rewrite_artifact_and_manifest(malformed, "content_record.json", b"[]\n")
    with pytest.raises(ParserFitCheckError) as exc:
        check_nordstrom_pdp_parser_fit(packet_or_manifest_path=malformed)
    assert exc.value.code == "content_record_shape"

    for mode in ("raw", "content"):
        packet_dir = tmp_path / mode
        assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=mode)[0] == 0
        exit_code, report = run_nordstrom_pdp_parser_fit_check(
            packet_paths=[packet_dir]
        )
        assert exit_code == 1
        assert report["results"][0]["status"] == "failure"
