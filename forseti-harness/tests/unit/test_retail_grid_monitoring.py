from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from harness_utils import generate_ulid
from runners import run_retail_grid_monitor as monitor_runner
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_grid_monitoring import (
    MonitorRoute,
    RetailGridCaptureAttempt,
    RetailGridMonitorManifest,
    compare_observations,
    load_monitor_manifest,
    monitor_routes,
    run_monitor_round,
)
from source_capture.retail_grid_projection import (
    RetailGridProjectionPacket,
    append_retail_grid_observation_into_lake,
)


_PROFILE = {
    "sephora": "sephora_grid_aggregate",
    "ulta": "ulta_grid_aggregate",
    "target": "target_grid_aggregate",
    "amazon": "amazon_grid_aggregate",
}


def _manifest(*, url: str = "https://www.amazon.com/s?k=Tower+28+Beauty", version: int = 1):
    return RetailGridMonitorManifest.model_validate(
        {
            "manifest_version": "retail_grid_monitor_manifest_v0",
            "brands": [
                {
                    "brand_id": "tower-28-beauty",
                    "name": "Tower 28 Beauty",
                    "retailers": {
                        "amazon": {
                            "url": url,
                            "page_count": 2,
                            "series_version": version,
                        }
                    },
                }
            ],
        }
    )


def _observation(
    *,
    root: DataLakeRoot,
    route: MonitorRoute,
    raw_sample: bool,
    products: list[dict[str, Any]],
    series_id: str | None = None,
    completeness_residuals: list[str] | None = None,
) -> tuple[Path, Path | None]:
    event_id = generate_ulid()
    raw_path = root.allocate_raw_packet_dir(event_id) if raw_sample else None
    anchor = (
        {
            "file_id": "file_01",
            "relative_packet_path": "raw/content_record.json",
            "sha256": "a" * 64,
            "hash_basis": "exact_file_bytes",
            "anchor_kind": "json_pointer",
            "anchor_value": "/products/0",
        }
        if raw_sample
        else None
    )
    rows = []
    placement_count = 0
    for index, product in enumerate(products, 1):
        placements = product.get(
            "placements",
            [{"grid_position": index, "page": 1, "page_position": index}],
        )
        placement_count += len(placements)
        rows.append(
            {
                "row_id": f"row-{index}",
                "retailer": route.retailer,
                "raw_ref": (
                    {"packet_id": event_id, "slice_id": "slice_001"}
                    if raw_sample
                    else None
                ),
                "raw_anchor": anchor,
                "placements": [
                    {**placement, "raw_anchor": anchor} for placement in placements
                ],
                "source_visible_fields": {
                    "source_product_id": product["id"],
                    "product_url": f"https://example.test/{product['id']}",
                    "name": product.get("name", product["id"]),
                    "price_display": product.get("price"),
                },
            }
        )
    observation = RetailGridProjectionPacket.model_validate(
        {
            "projection_version": "v1",
            "capture_event": {
                "capture_event_id": event_id,
                "captured_at": "2026-07-22T00:00:00Z",
                "requested_url": route.url,
                "final_url": route.url,
                "capture_profile": route.profile,
                "parser_version": "fixture-v1",
                "series_id": series_id or route.series_id,
                "raw_sample_packet_id": event_id if raw_sample else None,
            },
            "rows": rows,
            "source_visible_grid_facts": {},
            "completeness": {
                "status": "complete",
                "page_declared_result_count": len(rows),
                "extracted_unique_parent_count": len(rows),
                "extracted_placement_count": placement_count,
                "duplicate_placement_count": placement_count - len(rows),
                "subject_binding_confirmed": True,
                "termination": "requested_page_window_reconciled",
                "residuals": completeness_residuals or [],
            },
            "loss_ledger": {
                "preserved_evidence_rows": len(rows),
                "structure_preserved": bool(rows),
            },
        }
    )
    projection_path = append_retail_grid_observation_into_lake(
        data_root=root, observation=observation
    )
    return projection_path, raw_path


def _success_capture(
    root: DataLakeRoot,
    products_by_call: list[list[dict[str, Any]]],
    calls: list[tuple[str, bool]],
):
    def capture(route: MonitorRoute, retain_raw: bool) -> RetailGridCaptureAttempt:
        calls.append((route.series_id, retain_raw))
        products = products_by_call[len(calls) - 1]
        projection, raw = _observation(
            root=root,
            route=route,
            raw_sample=retain_raw,
            products=products,
        )
        return RetailGridCaptureAttempt(
            exit_code=0,
            message="fixture success",
            projection_path=projection,
            raw_packet_path=raw,
        )

    return capture


def test_checked_in_manifest_defines_four_individual_proven_routes() -> None:
    manifest = load_monitor_manifest(
        Path(__file__).resolve().parents[2] / "config" / "retail_grid_monitored_brands.json"
    )
    routes = monitor_routes(manifest)

    assert [(item.brand_id, item.retailer) for item in routes] == [
        ("summer-fridays", "sephora"),
        ("clinique", "ulta"),
        ("elf-cosmetics", "target"),
        ("tower-28-beauty", "amazon"),
    ]
    assert [item.profile for item in routes] == [
        "sephora_grid_aggregate",
        "ulta_grid_aggregate",
        "target_grid_aggregate",
        "amazon_grid_aggregate",
    ]


@pytest.mark.parametrize(
    ("retailer", "route", "message"),
    [
        ("amazon", {"url": "https://www.amazon.com/s?k=Tower+28"}, "page_count"),
        (
            "sephora",
            {"url": "https://www.sephora.com/brand/tower-28", "page_count": 2},
            "only for amazon",
        ),
        ("target", {"url": "https://example.com/brand/elf"}, "requires hostname"),
    ],
)
def test_manifest_rejects_incoherent_retailer_routes(
    retailer: str, route: dict[str, Any], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        RetailGridMonitorManifest.model_validate(
            {
                "brands": [
                    {
                        "brand_id": "test-brand",
                        "name": "Test Brand",
                        "retailers": {retailer: route},
                    }
                ]
            }
        )


def test_first_success_samples_raw_then_next_round_compares_derived_only(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    state_dir = tmp_path / "monitor"
    calls: list[tuple[str, bool]] = []
    capture = _success_capture(
        root,
        [
            [{"id": "A", "price": "$24.00"}],
            [
                {
                    "id": "A",
                    "price": "$26.00",
                    "placements": [{"grid_position": 17, "page": 2, "page_position": 1}],
                },
                {"id": "B", "price": "$18.00"},
            ],
        ],
        calls,
    )

    first_code, first_report_path, first_report = run_monitor_round(
        manifest=_manifest(),
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-22",
        qa_samples=set(),
        capture_route=capture,
    )
    second_code, second_report_path, second_report = run_monitor_round(
        manifest=_manifest(),
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-23",
        qa_samples=set(),
        capture_route=capture,
    )

    assert first_code == second_code == 0
    assert calls == [
        ("retail-grid:tower-28-beauty:amazon:v1", True),
        ("retail-grid:tower-28-beauty:amazon:v1", False),
    ]
    first_result = first_report["results"][0]
    assert first_result["comparison"]["comparison_status"] == "baseline"
    assert first_result["raw_packet_path"] is not None
    assert first_result["comparison"]["current_completeness_residuals"] == []
    second_result = second_report["results"][0]
    assert second_result["raw_packet_path"] is None
    comparison = second_result["comparison"]
    assert comparison["products_added"][0]["source_product_id"] == "B"
    assert comparison["placement_changes"][0]["source_product_id"] == "A"
    assert comparison["price_display_changes"][0] == {
        "source_product_id": "A",
        "name": "A",
        "before": "$24.00",
        "after": "$26.00",
    }
    assert comparison["previous_completeness_residuals"] == []
    assert comparison["current_completeness_residuals"] == []
    assert first_report_path.is_file()
    assert second_report_path.is_file()
    assert len(list((state_dir / "series").rglob("*.json"))) == 2


def test_failure_is_a_gap_and_same_round_retry_does_not_repeat_other_success(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    state_dir = tmp_path / "monitor"
    route = monitor_routes(_manifest())[0]
    first_projection, first_raw = _observation(
        root=root,
        route=route,
        raw_sample=True,
        products=[{"id": "A", "price": "$24.00"}],
    )
    outcomes = [
        RetailGridCaptureAttempt(0, "baseline", first_projection, first_raw),
        RetailGridCaptureAttempt(7, "access failed; packet preserved", None, None),
    ]
    calls: list[bool] = []

    def capture(_route: MonitorRoute, retain_raw: bool) -> RetailGridCaptureAttempt:
        calls.append(retain_raw)
        if outcomes:
            return outcomes.pop(0)
        projection, raw = _observation(
            root=root,
            route=route,
            raw_sample=retain_raw,
            products=[{"id": "A", "price": "$25.00"}],
        )
        return RetailGridCaptureAttempt(0, "recovered", projection, raw)

    assert run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-22", qa_samples=set(), capture_route=capture
    )[0] == 0
    failed_code, _, failed_report = run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-23", qa_samples=set(), capture_route=capture
    )
    assert failed_code == 4
    assert failed_report["results"][0]["status"] == "failure"

    recovered_code, _, recovered_report = run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-23", qa_samples=set(), capture_route=capture
    )
    assert recovered_code == 0
    assert recovered_report["results"][0]["comparison"]["intervening_failure_rounds"] == 0

    calls_before_skip = len(calls)
    skipped_code, _, skipped_report = run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-23", qa_samples=set(), capture_route=capture
    )
    assert skipped_code == 0
    assert len(calls) == calls_before_skip
    assert skipped_report["results"][0]["status"] == "already_successful"
    assert calls == [True, False, False]


def test_failed_day_is_visible_in_next_successful_comparison(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    state_dir = tmp_path / "monitor"
    route = monitor_routes(_manifest())[0]
    calls = 0

    def capture(_route: MonitorRoute, retain_raw: bool) -> RetailGridCaptureAttempt:
        nonlocal calls
        calls += 1
        if calls == 2:
            return RetailGridCaptureAttempt(7, "blocked")
        projection, raw = _observation(
            root=root,
            route=route,
            raw_sample=retain_raw,
            products=[{"id": "A", "price": f"${23 + calls}.00"}],
        )
        return RetailGridCaptureAttempt(0, "ok", projection, raw)

    for round_id in ("2026-07-22", "2026-07-23"):
        run_monitor_round(
            manifest=_manifest(), data_root=root, state_dir=state_dir,
            round_id=round_id, qa_samples=set(), capture_route=capture
        )
    _, _, report = run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-24", qa_samples=set(), capture_route=capture
    )
    assert report["results"][0]["comparison"]["intervening_failure_rounds"] == 1


def test_one_pair_failure_does_not_stop_others_and_retry_only_runs_failure(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    manifest = RetailGridMonitorManifest.model_validate(
        {
            "brands": [
                {
                    "brand_id": "summer-fridays",
                    "name": "Summer Fridays",
                    "retailers": {
                        "sephora": {
                            "url": (
                                "https://www.sephora.com/brand/summer-fridays"
                                "?country_switch=us"
                            )
                        }
                    },
                },
                {
                    "brand_id": "tower-28-beauty",
                    "name": "Tower 28 Beauty",
                    "retailers": {
                        "amazon": {
                            "url": "https://www.amazon.com/s?k=Tower+28+Beauty",
                            "page_count": 2,
                        }
                    },
                },
            ]
        }
    )
    phase = "baseline"
    calls: list[tuple[str, str, bool]] = []

    def capture(route: MonitorRoute, retain_raw: bool) -> RetailGridCaptureAttempt:
        calls.append((phase, route.retailer, retain_raw))
        if phase == "partial" and route.retailer == "amazon":
            return RetailGridCaptureAttempt(7, "amazon blocked")
        projection, raw = _observation(
            root=root,
            route=route,
            raw_sample=retain_raw,
            products=[{"id": f"{route.retailer}-A", "price": "$20.00"}],
        )
        return RetailGridCaptureAttempt(0, "ok", projection, raw)

    state_dir = tmp_path / "monitor"
    run_monitor_round(
        manifest=manifest, data_root=root, state_dir=state_dir,
        round_id="2026-07-22", qa_samples=set(), capture_route=capture
    )
    phase = "partial"
    code, _, report = run_monitor_round(
        manifest=manifest, data_root=root, state_dir=state_dir,
        round_id="2026-07-23", qa_samples=set(), capture_route=capture
    )
    assert code == 4
    assert [item["status"] for item in report["results"]] == ["success", "failure"]

    phase = "retry"
    retry_start = len(calls)
    code, _, report = run_monitor_round(
        manifest=manifest, data_root=root, state_dir=state_dir,
        round_id="2026-07-23", qa_samples=set(), capture_route=capture
    )
    assert code == 0
    assert calls[retry_start:] == [("retry", "amazon", False)]
    assert [item["status"] for item in report["results"]] == [
        "already_successful",
        "success",
    ]


def test_forced_qa_sample_overrides_same_round_skip(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    calls: list[tuple[str, bool]] = []
    capture = _success_capture(
        root,
        [[{"id": "A"}], [{"id": "A"}]],
        calls,
    )
    state_dir = tmp_path / "monitor"
    run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-22", qa_samples=set(), capture_route=capture
    )
    _, _, report = run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-22", qa_samples={"tower-28-beauty:amazon"}, capture_route=capture
    )
    assert calls[-1][1] is True
    assert report["results"][0]["raw_packet_path"] is not None


def test_route_change_requires_series_version_bump(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    calls: list[tuple[str, bool]] = []
    capture = _success_capture(root, [[{"id": "A"}]], calls)
    state_dir = tmp_path / "monitor"
    run_monitor_round(
        manifest=_manifest(), data_root=root, state_dir=state_dir,
        round_id="2026-07-22", qa_samples=set(), capture_route=capture
    )

    with pytest.raises(ValueError, match="series_version bump"):
        run_monitor_round(
            manifest=_manifest(url="https://www.amazon.com/s?k=Tower+28+Beauty&page=1"),
            data_root=root,
            state_dir=state_dir,
            round_id="2026-07-23",
            qa_samples=set(),
            capture_route=capture,
        )

    bumped_calls: list[tuple[str, bool]] = []
    bumped_capture = _success_capture(root, [[{"id": "A"}]], bumped_calls)
    _, _, report = run_monitor_round(
        manifest=_manifest(
            url="https://www.amazon.com/s?k=Tower+28+Beauty&page=1", version=2
        ),
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-23",
        qa_samples=set(),
        capture_route=bumped_capture,
    )
    assert bumped_calls[0][1] is True
    assert report["results"][0]["comparison"]["comparison_status"] == "baseline"


def test_failed_only_route_can_be_corrected_without_version_bump(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    state_dir = tmp_path / "monitor"
    original = _manifest()
    corrected = _manifest(url="https://www.amazon.com/s?k=Tower+28+Beauty&page=1")

    code, _, _ = run_monitor_round(
        manifest=original,
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-22",
        qa_samples=set(),
        capture_route=lambda _route, _retain: RetailGridCaptureAttempt(7, "blocked"),
    )
    assert code == 4

    calls: list[tuple[str, bool]] = []
    capture = _success_capture(root, [[{"id": "A"}]], calls)
    code, _, report = run_monitor_round(
        manifest=corrected,
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-22",
        qa_samples=set(),
        capture_route=capture,
    )
    assert code == 0
    assert calls[0][1] is True
    assert report["results"][0]["comparison"]["comparison_status"] == "baseline"


def test_projection_series_mismatch_fails_without_advancing_success(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    route = monitor_routes(_manifest())[0]
    projection, raw = _observation(
        root=root,
        route=route,
        raw_sample=True,
        products=[{"id": "A"}],
        series_id="wrong-series",
    )

    code, _, report = run_monitor_round(
        manifest=_manifest(),
        data_root=root,
        state_dir=tmp_path / "monitor",
        round_id="2026-07-22",
        qa_samples=set(),
        capture_route=lambda _route, _retain: RetailGridCaptureAttempt(
            0, "wrong", projection, raw
        ),
    )
    assert code == 4
    assert report["results"][0]["status"] == "failure"
    assert "series mismatch" in report["results"][0]["runner_message"]
    assert report["results"][0]["comparison"] is None


def test_capture_crash_is_one_visible_gap_not_a_lost_round(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    state_dir = tmp_path / "monitor"
    manifest = RetailGridMonitorManifest.model_validate(
        {
            "brands": [
                {
                    "brand_id": "summer-fridays",
                    "name": "Summer Fridays",
                    "retailers": {
                        "sephora": {
                            "url": (
                                "https://www.sephora.com/brand/summer-fridays"
                                "?country_switch=us"
                            )
                        }
                    },
                },
                {
                    "brand_id": "tower-28-beauty",
                    "name": "Tower 28 Beauty",
                    "retailers": {
                        "amazon": {
                            "url": "https://www.amazon.com/s?k=Tower+28+Beauty",
                            "page_count": 2,
                        }
                    },
                },
            ]
        }
    )

    def capture(route: MonitorRoute, retain_raw: bool) -> RetailGridCaptureAttempt:
        if route.retailer == "sephora":
            raise RuntimeError("browser driver exploded")
        projection, raw = _observation(
            root=root,
            route=route,
            raw_sample=retain_raw,
            products=[{"id": "amazon-A", "price": "$20.00"}],
        )
        return RetailGridCaptureAttempt(0, "ok", projection, raw)

    code, report_path, report = run_monitor_round(
        manifest=manifest,
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-22",
        qa_samples=set(),
        capture_route=capture,
    )

    assert code == 4
    assert report_path.is_file()
    assert [item["status"] for item in report["results"]] == ["failure", "success"]
    assert "monitor_capture_raised: RuntimeError: browser driver exploded" in (
        report["results"][0]["runner_message"]
    )
    assert report["results"][0]["comparison"] is None


def test_comparison_always_surfaces_current_completeness_advisories(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    route = monitor_routes(_manifest())[0]
    previous_path, _ = _observation(
        root=root,
        route=route,
        raw_sample=False,
        products=[{"id": "A"}],
    )
    current_path, _ = _observation(
        root=root,
        route=route,
        raw_sample=False,
        products=[{"id": "A"}],
        completeness_residuals=[
            "target_grid_declared_count_changed_during_traversal:minimum=240:maximum=247"
        ],
    )
    previous = RetailGridProjectionPacket.model_validate_json(
        previous_path.read_text(encoding="utf-8")
    )
    current = RetailGridProjectionPacket.model_validate_json(
        current_path.read_text(encoding="utf-8")
    )

    comparison = compare_observations(
        previous, current, intervening_failure_rounds=0
    )

    assert comparison["current_completeness_residuals"] == [
        "target_grid_declared_count_changed_during_traversal:minimum=240:maximum=247"
    ]
    assert comparison["completeness_changes"]["residuals"]["after"] == (
        comparison["current_completeness_residuals"]
    )


def test_projection_validation_failure_keeps_only_a_verified_raw_pointer(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    state_dir = tmp_path / "monitor"
    raw_path = root.allocate_raw_packet_dir(generate_ulid())
    outside_raw = tmp_path / "not-the-lake" / "packet"
    outside_raw.mkdir(parents=True)
    invalid_projection = tmp_path / "outside-derived.json"
    invalid_projection.write_text("{}", encoding="utf-8")
    attempts = iter(
        (
            RetailGridCaptureAttempt(0, "bad projection", invalid_projection, raw_path),
            RetailGridCaptureAttempt(4, "failed packet", None, outside_raw),
        )
    )

    def capture(_route: MonitorRoute, _retain_raw: bool) -> RetailGridCaptureAttempt:
        return next(attempts)

    _, _, first_report = run_monitor_round(
        manifest=_manifest(),
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-22",
        qa_samples=set(),
        capture_route=capture,
    )
    _, _, second_report = run_monitor_round(
        manifest=_manifest(),
        data_root=root,
        state_dir=state_dir,
        round_id="2026-07-23",
        qa_samples=set(),
        capture_route=capture,
    )

    assert first_report["results"][0]["raw_packet_path"] == str(raw_path.resolve())
    assert second_report["results"][0]["raw_packet_path"] is None
    assert "monitor_raw_path_validation_failed" in (
        second_report["results"][0]["runner_message"]
    )


def test_runner_builds_retailer_owned_pins_and_parses_structured_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    route = monitor_routes(_manifest())[0]
    raw_path = root.allocate_raw_packet_dir(generate_ulid())
    projection_path = root.path / "derived" / "projection.json"
    projection_path.write_text("{}", encoding="utf-8")
    seen: list[str] = []

    def fake_main(argv: list[str]) -> int:
        seen.extend(argv)
        print(
            f"raw sample preserved at {raw_path}; "
            f"derived observation preserved at {projection_path}"
        )
        print("post-capture diagnostic")
        return 0

    monkeypatch.setattr(monitor_runner, "cloakbrowser_main", fake_main)
    result = monitor_runner.capture_route(route, True, data_root=root)

    assert result.exit_code == 0
    assert result.raw_packet_path == raw_path
    assert result.projection_path == projection_path
    assert seen[seen.index("--delivery-zip") + 1] == "10001"
    assert seen[seen.index("--amazon-grid-page-count") + 1] == "2"
    assert "--retain-retail-grid-raw-sample" in seen
    assert "--block-heavy-assets" in seen


def test_runner_derives_all_retailer_profiles_and_pins_from_manifest(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    manifest = load_monitor_manifest(
        Path(__file__).resolve().parents[2] / "config" / "retail_grid_monitored_brands.json"
    )
    argv_by_retailer = {
        route.retailer: monitor_runner._capture_argv(
            route=route, data_root=root, retain_raw_sample=False
        )
        for route in monitor_routes(manifest)
    }

    assert argv_by_retailer["sephora"][
        argv_by_retailer["sephora"].index("--sephora-market") + 1
    ] == "US"
    assert argv_by_retailer["sephora"][
        argv_by_retailer["sephora"].index("--timeout-seconds") + 1
    ] == "90"
    assert get_retail_capture_profile("sephora_grid_aggregate").wait_until == (
        "domcontentloaded"
    )
    assert argv_by_retailer["ulta"][
        argv_by_retailer["ulta"].index("--ulta-market") + 1
    ] == "US"
    assert argv_by_retailer["ulta"][
        argv_by_retailer["ulta"].index("--timeout-seconds") + 1
    ] == "90"
    assert "--target-zip" not in argv_by_retailer["target"]
    assert argv_by_retailer["target"][
        argv_by_retailer["target"].index("--timeout-seconds") + 1
    ] == "240"
    assert argv_by_retailer["amazon"][
        argv_by_retailer["amazon"].index("--delivery-zip") + 1
    ] == "10001"
    amazon_route = next(
        route for route in monitor_routes(manifest) if route.retailer == "amazon"
    )
    assert amazon_route.page_count == 2
    # AmazonSearchGridPlugin bounds its whole multi-page walk with this value and
    # defaults to 60s on its own; the monitor must never hand it a smaller budget.
    assert float(
        argv_by_retailer["amazon"][
            argv_by_retailer["amazon"].index("--timeout-seconds") + 1
        ]
    ) >= 60.0 * amazon_route.page_count
    for route in monitor_routes(manifest):
        argv = argv_by_retailer[route.retailer]
        assert argv[argv.index("--retail-capture-profile") + 1] == _PROFILE[route.retailer]
        assert argv[argv.index("--series-id") + 1] == route.series_id
