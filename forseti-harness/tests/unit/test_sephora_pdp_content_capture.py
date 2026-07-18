from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable

import pytest

from runners import run_source_capture_cloakbrowser_packet as runner
from runners.run_sephora_pdp_parser_fit_check import (
    ParserFitCheckError,
    check_sephora_pdp_parser_fit,
    run_sephora_pdp_parser_fit_check,
)
from source_capture import CaptureModeCategory
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.content_capture import RenderedContentCaptureSpec
from source_capture.models import SourceCapturePacket
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_pdp_projection import (
    SEPHORA_PDP_CONTENT_RECORD_KIND,
    SEPHORA_PDP_PARSER_VERSION,
    build_retail_pdp_projection_from_packet_directory,
    build_sephora_pdp_aggregate_content_record,
)
from source_capture.retail_pdp_silver import build_retail_pdp_silver_records


_URL = (
    "https://www.sephora.com/product/lip-sleeping-mask-P420652"
    "?country_switch=us&lang=en"
)
_LD_JSON = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "ProductGroup",
        "productGroupID": "P420652",
        "name": "Lip Sleeping Mask",
        "hasVariant": [
            {
                "@type": "Product",
                "sku": "2961324",
                "color": "Acai Mango Smoothie",
                "offers": {
                    "@type": "Offer",
                    "price": "25.00",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "seller": {"@type": "Organization", "name": "Sephora"},
                },
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "reviewCount": "22273",
            "ratingValue": "4.3",
        },
    },
    separators=(",", ":"),
)
_HISTOGRAM = "".join(
    f'<button><span class="Histogram-label">{rating}</span>'
    f'<div style="width: {percentage}%;"></div></button>'
    for rating, percentage in ((5, 69), (4, 12), (3, 7), (2, 6), (1, 6))
)
_DOM = f"""
<html><head>
  <script>Sephora.renderQueryParams={{"country":"US","language":"en"}};</script>
  <script type="application/ld+json">{_LD_JSON}</script>
</head><body>
  <main class="ProductHero">
    <div data-cnstrc-item-id="P420652" data-cnstrc-item-price="$25.00"
      data-cnstrc-item-variation-id="2961324"
      data-comp="ProductPage ProductPage BaseComponent"></div>
  </main>
  <h2 data-at="ratings_reviews_section">Ratings &amp; Reviews (22.1K)</h2>
  <div data-comp="ReviewsStats">{_HISTOGRAM}<span>22,069 Reviews*</span></div>
  <p>Beauty Insider members earn points.</p>
</body></html>
"""
_VISIBLE_TEXT = """
LANEIGE
Lip Sleeping Mask
Color
Acai Mango Smoothie
$25.00
Ratings & Reviews (22.1K)
Summary
5 4 3 2 1
4.3
22,069 Reviews*
Add to Bag
"""


def _logical_name(relative_packet_path: str) -> str:
    return re.sub(r"^\d+_", "", Path(relative_packet_path).name)


def _success(
    *,
    pin_confirmed: bool = True,
    visible_text: str = _VISIBLE_TEXT,
) -> CloakBrowserSnapshotSuccess:
    return CloakBrowserSnapshotSuccess(
        requested_url=_URL,
        final_url=_URL,
        title="Lip Sleeping Mask | Sephora",
        rendered_dom=_DOM,
        visible_text=visible_text,
        screenshot_png=b"\x89PNG\r\n\x1a\nsephora-active-capture",
        metadata={
            "capture_timestamp": "2026-07-18T00:00:00Z",
            "requested_url": _URL,
            "final_url": _URL,
            "pin_confirmed": pin_confirmed,
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
        runner,
        "fetch_cloakbrowser_snapshot_capture",
        lambda **_kwargs: capture_factory(),
    )
    content_capture = (
        None
        if mode is None
        else RenderedContentCaptureSpec(
            capture_artifact_mode=mode,
            parser_version=SEPHORA_PDP_PARSER_VERSION,
            projector=projector
            or (
                lambda rendered_dom, visible_text, final_url: (
                    build_sephora_pdp_aggregate_content_record(
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
        decision_question="What source-visible offer and review facts are present?",
        output_directory=output,
        capture_context="Sephora content-mode unit proof",
        operator_category="unit_test",
        capture_mode=CaptureModeCategory.MULTIMODAL,
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
            "sephora_pdp_aggregate"
        ),
        timeout_seconds=30,
        wait_until="load",
        viewport_width=1920,
        viewport_height=1080,
        max_artifact_bytes=10_000_000,
        block_heavy_assets=False,
        settle_seconds=5,
        scroll_passes=1,
        scroll_step_px=350,
        sephora_market="US",
        series_id="sephora_laneige_lipmask_us_v0",
        locale_pin=runner.known_fact("en-US"),
        currency_pin=runner.known_fact("USD"),
        variant_pin=runner.known_fact("sku=2961324"),
        content_capture=content_capture,
    )


def _manifest(packet_dir: Path) -> dict[str, Any]:
    return json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))


def _artifact_path(packet_dir: Path, filename: str) -> Path:
    manifest = _manifest(packet_dir)
    return next(
        packet_dir / item["relative_packet_path"]
        for item in manifest["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == filename
    )


def _packet(packet_dir: Path) -> SourceCapturePacket:
    return SourceCapturePacket.model_validate(_manifest(packet_dir))


def _rewrite_artifact_and_manifest(
    packet_dir: Path,
    filename: str,
    body: bytes,
) -> None:
    manifest = _manifest(packet_dir)
    match = next(
        item
        for item in manifest["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == filename
    )
    path = packet_dir / match["relative_packet_path"]
    path.write_bytes(body)
    match["sha256"] = hashlib.sha256(body).hexdigest()
    match["size_bytes"] = len(body)
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(manifest, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )


def _mutate_json_artifact(
    packet_dir: Path,
    filename: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    path = _artifact_path(packet_dir, filename)
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    _rewrite_artifact_and_manifest(
        packet_dir,
        filename,
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


@pytest.mark.parametrize(
    ("mode", "expected", "absent"),
    [
        (
            "content",
            {
                "content_record.json",
                "content_capture_metadata.json",
                "cloakbrowser_viewport_screenshot.png",
                "cloakbrowser_snapshot_metadata.json",
            },
            {"cloakbrowser_rendered_dom.html", "cloakbrowser_visible_text.txt"},
        ),
        (
            "sample",
            {
                "content_record.json",
                "content_capture_metadata.json",
                "cloakbrowser_rendered_dom.html",
                "cloakbrowser_visible_text.txt",
                "cloakbrowser_viewport_screenshot.png",
                "cloakbrowser_snapshot_metadata.json",
            },
            set(),
        ),
        (
            "raw",
            {
                "content_capture_metadata.json",
                "cloakbrowser_rendered_dom.html",
                "cloakbrowser_visible_text.txt",
                "cloakbrowser_viewport_screenshot.png",
                "cloakbrowser_snapshot_metadata.json",
            },
            {"content_record.json"},
        ),
    ],
)
def test_sephora_capture_artifact_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    expected: set[str],
    absent: set[str],
) -> None:
    packet_dir = tmp_path / mode
    exit_code, _message = _run(
        output=packet_dir,
        monkeypatch=monkeypatch,
        mode=mode,
    )

    assert exit_code == 0
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert names == expected
    assert names.isdisjoint(absent)
    metadata = json.loads(
        _artifact_path(packet_dir, "content_capture_metadata.json").read_text(
            encoding="utf-8"
        )
    )
    assert metadata["capture_artifact_mode"] == mode
    by_role = {item["role"]: item for item in metadata["inputs"]}
    assert by_role["screenshot"]["preserved"] is True
    assert by_role["browser_metadata"]["preserved"] is True
    assert by_role["rendered_dom"]["preserved"] is (mode != "content")
    assert by_role["visible_text"]["preserved"] is (mode != "content")


def test_sephora_profile_defaults_to_content_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "default"
    exit_code, _message = _run(
        output=packet_dir,
        monkeypatch=monkeypatch,
        mode=None,
    )

    assert exit_code == 0
    assert _artifact_path(packet_dir, "content_record.json").is_file()
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert "cloakbrowser_rendered_dom.html" not in names
    assert "cloakbrowser_visible_text.txt" not in names


def test_cli_capture_artifact_mode_is_distinct_from_capture_mode() -> None:
    args = runner._build_parser().parse_args(
        [
            "--url",
            _URL,
            "--decision-question",
            "What is visible?",
            "--output",
            "packet",
            "--capture-mode",
            "multimodal",
            "--capture-artifact-mode",
            "sample",
        ]
    )

    assert args.capture_mode == "multimodal"
    assert args.capture_artifact_mode == "sample"


def test_cli_defaults_pinned_sephora_profile_to_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        runner,
        "fetch_cloakbrowser_snapshot_capture",
        lambda **_kwargs: _success(),
    )
    packet_dir = tmp_path / "cli-content"

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
                "What source-visible offer and review facts are present?",
                "--output",
                str(packet_dir),
                "--retail-capture-profile",
                "sephora_pdp_aggregate",
                "--sephora-market",
                "US",
            ]
        )
        == 0
    )
    assert str(packet_dir) in capsys.readouterr().out
    assert _artifact_path(packet_dir, "content_record.json").is_file()
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert "cloakbrowser_rendered_dom.html" not in names


def test_cli_rejects_artifact_mode_for_other_retail_profile(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        runner.main(
            [
                "--url",
                _URL,
                "--source-family",
                "retail_pdp",
                "--source-surface",
                "cloakbrowser_snapshot",
                "--decision-question",
                "What is visible?",
                "--output",
                str(tmp_path / "packet"),
                "--retail-capture-profile",
                "sephora_pdp_distribution",
                "--capture-artifact-mode",
                "sample",
            ]
        )

    assert exc.value.code == 2
    assert "currently requires" in capsys.readouterr().err


def test_sephora_content_record_is_deterministic_and_has_no_fabricated_refs() -> None:
    first = build_sephora_pdp_aggregate_content_record(
        rendered_dom=_DOM.encode(),
        visible_text=_VISIBLE_TEXT.encode(),
        source_url=_URL,
    )
    second = build_sephora_pdp_aggregate_content_record(
        rendered_dom=_DOM.encode(),
        visible_text=_VISIBLE_TEXT.encode(),
        source_url=_URL,
    )

    assert first == second
    assert first["record_kind"] == SEPHORA_PDP_CONTENT_RECORD_KIND
    serialized = json.dumps(first, sort_keys=True)
    assert "content_record_unbound" not in serialized
    assert "content_input_rendered_dom" not in serialized
    assert "content_input_visible_text" not in serialized
    assert "cloakbrowser_rendered_dom.html" not in serialized
    assert "cloakbrowser_visible_text.txt" not in serialized


def test_projection_failure_preserves_all_inputs_and_returns_exit_4(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(*_args):
        raise RuntimeError("fixture drift")

    packet_dir = tmp_path / "projection_failure"
    exit_code, _message = _run(
        output=packet_dir,
        monkeypatch=monkeypatch,
        mode="content",
        projector=fail,
    )

    assert exit_code == 4
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert "cloakbrowser_rendered_dom.html" in names
    assert "cloakbrowser_visible_text.txt" in names
    assert "cloakbrowser_viewport_screenshot.png" in names
    assert "cloakbrowser_snapshot_metadata.json" in names
    assert "content_record.json" not in names


@pytest.mark.parametrize("failure_kind", ["market", "sufficiency"])
def test_failed_admission_preserves_dom_and_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_kind: str,
) -> None:
    capture_factory = (
        (lambda: _success(pin_confirmed=False))
        if failure_kind == "market"
        else (lambda: _success(visible_text="Lip Sleeping Mask"))
    )
    packet_dir = tmp_path / failure_kind
    exit_code, _message = _run(
        output=packet_dir,
        monkeypatch=monkeypatch,
        mode="content",
        capture_factory=capture_factory,
    )

    assert exit_code == runner.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    names = {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }
    assert "content_record.json" in names
    assert "cloakbrowser_rendered_dom.html" in names
    assert "cloakbrowser_visible_text.txt" in names


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


def _without_lineage_refs(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_lineage_refs(item)
            for key, item in value.items()
            if key not in {"raw_refs", "derived_refs"}
        }
    if isinstance(value, list):
        return [_without_lineage_refs(item) for item in value]
    return value


def test_content_projection_and_silver_match_raw_semantics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
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
        row.raw_ref.packet_id == _packet(content_dir).packet_id
        for row in content_projection.rows
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
        projection_sha256="raw-projection-sha",
    )
    content_silver = build_retail_pdp_silver_records(
        packet=_packet(content_dir),
        projection=content_projection,
        projection_record_id="projection.json",
        projection_sha256="content-projection-sha",
    )
    assert [_without_lineage_refs(record["payload"]) for record in raw_silver] == [
        _without_lineage_refs(record["payload"]) for record in content_silver
    ]
    assert [record.get("residuals") for record in raw_silver] == [
        record.get("residuals") for record in content_silver
    ]


def test_parser_fit_matches_sample_packet(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "sample"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0

    result = check_sephora_pdp_parser_fit(packet_or_manifest_path=packet_dir)

    assert result["status"] == "match"
    assert result["current_parser_version"] == SEPHORA_PDP_PARSER_VERSION
    exit_code, report = run_sephora_pdp_parser_fit_check(
        packet_paths=[packet_dir]
    )
    assert exit_code == 0
    assert report["results"][0]["status"] == "match"


def test_parser_fit_reports_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "sample"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    _mutate_json_artifact(
        packet_dir,
        "content_record.json",
        lambda payload: payload["rows"][0]["source_visible_fields"].update(
            {"drift_fixture": "changed"}
        ),
    )

    result = check_sephora_pdp_parser_fit(packet_or_manifest_path=packet_dir)

    assert result["status"] == "drift"
    assert result["difference"]["stored_sha256"] != result["difference"]["current_sha256"]


@pytest.mark.parametrize(
    ("filename", "mutate", "expected_code"),
    [
        (
            "content_capture_metadata.json",
            lambda payload: payload.update({"parser_version": "old_parser"}),
            "parser_version_mismatch",
        ),
        (
            "cloakbrowser_snapshot_metadata.json",
            lambda payload: payload["retail_capture_profile"].update(
                {"name": "sephora_pdp_distribution"}
            ),
            "profile_mismatch",
        ),
        (
            "content_record.json",
            lambda payload: payload.update(
                {"source_url": "https://www.sephora.com/product/other-P1"}
            ),
            "source_mismatch",
        ),
    ],
)
def test_parser_fit_rejects_metadata_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    filename: str,
    mutate: Callable[[dict[str, Any]], None],
    expected_code: str,
) -> None:
    packet_dir = tmp_path / expected_code
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    _mutate_json_artifact(packet_dir, filename, mutate)

    with pytest.raises(ParserFitCheckError) as exc:
        check_sephora_pdp_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc.value.code == expected_code


def test_parser_fit_rejects_input_hash_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "hash"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    body = _artifact_path(packet_dir, "cloakbrowser_rendered_dom.html").read_bytes()
    _rewrite_artifact_and_manifest(
        packet_dir,
        "cloakbrowser_rendered_dom.html",
        body + b"\n<!-- drift -->",
    )

    with pytest.raises(ParserFitCheckError) as exc:
        check_sephora_pdp_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc.value.code == "input_hash_mismatch"


def test_parser_fit_rejects_malformed_record(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "malformed"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    _rewrite_artifact_and_manifest(packet_dir, "content_record.json", b"[]\n")

    with pytest.raises(ParserFitCheckError) as exc:
        check_sephora_pdp_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc.value.code == "content_record_shape"


@pytest.mark.parametrize("mode", ["content", "raw"])
def test_parser_fit_rejects_non_sample_packets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
) -> None:
    packet_dir = tmp_path / mode
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=mode)[0] == 0

    with pytest.raises(ParserFitCheckError) as exc:
        check_sephora_pdp_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc.value.code in {"sample_required", "preserved_file_mismatch"}
    exit_code, report = run_sephora_pdp_parser_fit_check(
        packet_paths=[packet_dir]
    )
    assert exit_code == 1
    assert report["results"][0]["status"] == "failure"
