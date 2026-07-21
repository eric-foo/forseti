from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from source_capture.adapters.ulta_powerreviews import (
    PowerReviewsReadConfig,
    PowerReviewsRequestSpec,
    PowerReviewsResponse,
    UltaPowerReviewsConfigError,
    resolve_ulta_powerreviews_config,
)
from source_capture.models import known_fact
from source_capture.ulta_onboarding_capture import (
    UltaOnboardingCaptureError,
    capture_ulta_onboarding_packet,
)
from source_capture.writer import write_local_source_capture_packet


_PRODUCT_ID = "pimprod2046225"
_PRODUCT_URL = (
    f"https://www.ulta.com/p/night-shift-overnight-lip-mask-{_PRODUCT_ID}"
)
_API_KEY = "daa0f241-c242-4483-afb7-4449942d1a2b"
_MERCHANT_ID = "6406"


def _render_block(page_id: str = _PRODUCT_ID, api_key: str = _API_KEY) -> str:
    return (
        '<script id="PowerReviewsRender">'
        "POWERREVIEWS.display.render({"
        "ENABLE_CLIENT_SIDE_STRUCTURED_DATA: false,"
        f"api_key: '{api_key}',"
        "locale: 'en_US',"
        "merchant_group_id: '11984',"
        f"merchant_id: '{_MERCHANT_ID}',"
        f"page_id: '{page_id}',"
        "components: {ReviewList: 'reviewsList'}"
        "})"
        "</script>"
    )


def _parent_packet(
    root: DataLakeRoot,
    tmp_path: Path,
    *,
    page_id: str = _PRODUCT_ID,
    pin_confirmed: bool = True,
    include_pin_metadata: bool = True,
    include_render_block: bool = True,
) -> str:
    html = "<html><body>Night Shift Overnight Lip Mask"
    if include_render_block:
        html += _render_block(page_id=page_id)
    html += "</body></html>"
    files = []
    dom = tmp_path / f"ulta-parent-{page_id}.html"
    dom.write_text(html, encoding="utf-8")
    files.append(dom)
    if include_pin_metadata:
        metadata = {
            "pre_capture": "ulta_us_market_assertion",
            "pin_confirmed": pin_confirmed,
            "access_blocked": False,
            "proxy_used": False,
            "geoip_used": False,
        }
        metadata_file = tmp_path / f"ulta-parent-{page_id}-metadata.json"
        metadata_file.write_text(json.dumps(metadata), encoding="utf-8")
        files.append(metadata_file)
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=files,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_PRODUCT_URL),
        decision_question="test Ulta parent",
        capture_context="rendered Ulta sample packet",
    )
    return result.packet.packet_id


def _review_row(
    review_id: int,
    *,
    created: int,
    helpful: int,
    page_id: str = _PRODUCT_ID,
    ugc_id: int | None = None,
    disclosure: str | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "ugc_id": ugc_id if ugc_id is not None else review_id,
        "review_id": review_id,
        "internal_review_id": review_id + 1_000_000,
        "legacy_id": review_id,
        "details": {
            "comments": f"Body {review_id}",
            "headline": f"Headline {review_id}",
            "nickname": f"user-{review_id}",
            "locale": "en_US",
            "location": "Somewhere",
            "created_date": created,
            "updated_date": created,
            "product_page_id": page_id,
            "bottom_line": "Yes",
            "properties": [
                {"key": "pros", "label": "Pros", "value": ["Hydrating"]}
            ],
        },
        "badges": {
            "is_staff_reviewer": False,
            "is_verified_buyer": True,
            "is_verified_reviewer": True,
        },
        "media": [],
        "metrics": {
            "helpful_votes": helpful,
            "not_helpful_votes": 0,
            "rating": 5,
            "helpful_score": helpful * 100,
        },
    }
    if disclosure is not None:
        row["details"]["disclosure_code"] = disclosure
    return row


def _reviews_document(
    rows: list[dict[str, Any]],
    *,
    total: int,
) -> dict[str, Any]:
    return {
        "name": "review",
        "paging": {
            "total_results": total,
            "pages_total": 1,
            "page_size": len(rows),
            "current_page_number": 1,
        },
        "results": [
            {
                "rollup": {
                    "average_rating": 4.31,
                    "rating_count": total,
                    "review_count": total,
                    "rating_histogram": [10, 10, 40, 120, 492],
                    "recommended_ratio": 0.85,
                    "native_review_count": total,
                    "native_sampling_review_count": 460,
                    "native_sweepstakes_review_count": 0,
                    "native_community_content_review_count": 0,
                    "syndicated_review_count": 0,
                    "faceoff_positive": {"headline": "Great"},
                    "faceoff_negative": {"headline": "Sticky"},
                },
                "reviews": rows,
            }
        ],
    }


def _questions_document() -> dict[str, Any]:
    return {
        "name": "question",
        "paging": {"total_results": 1},
        "results": [
            {
                "ugc_id": 555338720,
                "question_id": "10993814",
                "details": {
                    "nickname": "asker",
                    "created_date": 1750304118163,
                    "text": "Is this petroleum free?",
                    "product_page_id": _PRODUCT_ID,
                    "is_seeded": False,
                },
                "answer": [
                    {
                        "ugc_id": 555886396,
                        "answer_id": "555886396",
                        "details": {
                            "nickname": "Liv",
                            "text": "No it is not.",
                            "is_expert": True,
                            "author_type": "EXPERT",
                            "brand_name": "Ulta Beauty Collection",
                            "created_date": 1750880577016,
                        },
                        "metrics": {"helpful_votes": 1, "not_helpful_votes": 0},
                    }
                ],
                "answer_count": 1,
            }
        ],
    }


def _api_fetcher(
    *,
    corrupt_recent: bool = False,
    recent_status: int = 200,
    foreign_recent_page_id: bool = False,
    break_native_id: bool = False,
    total: int = 40,
):
    def fetch(
        spec: PowerReviewsRequestSpec,
        config: PowerReviewsReadConfig,
        _timeout_seconds: float,
        _max_bytes: int,
    ) -> PowerReviewsResponse:
        assert config.merchant_id == _MERCHANT_ID
        assert config.page_id == _PRODUCT_ID
        assert config.api_key == _API_KEY
        parameters = dict(spec.parameters)
        offset = int(parameters.get("paging.from", "0"))
        page_size = int(parameters["paging.size"])
        if spec.resource == "questions":
            document: dict[str, Any] = _questions_document()
        elif parameters["sort"] == "MostHelpful":
            rows = [
                _review_row(
                    100 + offset + index,
                    created=1_700_000_000_000 - index,
                    helpful=50 - offset - index,
                    disclosure="sampling" if index == 0 else None,
                )
                for index in range(min(page_size, total - offset))
            ]
            document = _reviews_document(rows, total=total)
        else:
            assert parameters["sort"] == "Newest"
            rows = [
                _review_row(
                    500 - offset - index,
                    created=1_800_000_000_000 - (offset + index) * 1000,
                    helpful=1,
                    page_id=(
                        "pimprod9999999"
                        if foreign_recent_page_id and offset == 0 and index == 0
                        else _PRODUCT_ID
                    ),
                    ugc_id=(
                        999
                        if break_native_id and offset == 0 and index == 0
                        else None
                    ),
                )
                for index in range(min(page_size, total - offset))
            ]
            document = _reviews_document(rows, total=total)
        if corrupt_recent and spec.artifact_name == "reviews_most_recent_offset_000.json":
            body = b"{invalid-json"
        else:
            body = json.dumps(document, separators=(",", ":")).encode()
        status = (
            recent_status
            if spec.artifact_name == "reviews_most_recent_offset_000.json"
            else 200
        )
        return PowerReviewsResponse(
            status=status,
            reason="OK" if status == 200 else "Server Error",
            body=body,
            content_type="application/json",
            captured_at="2026-07-21T00:00:00Z",
        )

    return fetch


def _artifact_json(loaded, suffix: str) -> dict[str, Any]:
    preserved = next(
        item
        for item in loaded.manifest["preserved_files"]
        if item["relative_packet_path"].endswith(suffix)
    )
    return json.loads(loaded.bodies[preserved["file_id"]].decode())


def _artifact_names(loaded) -> set[str]:
    return {
        item["relative_packet_path"].rsplit("/", 1)[-1].split("_", 1)[-1]
        for item in loaded.manifest["preserved_files"]
    }


def test_success_preserves_three_roles_without_body_or_key_duplication(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_ulta_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        review_page_size=25,
        pages_per_role=2,
        api_fetcher=_api_fetcher(total=40),
    )
    assert exit_code == 0
    summary = result["summary"]
    assert summary["record_kind"] == "ulta_powerreviews_onboarding_summary_v1"
    assert summary["identity"]["mapping_equal"] is True
    assert summary["reviews"]["last_seen_review_id"] == "500"
    assert summary["reviews"]["most_helpful"]["captured_review_rows"] == 40
    assert summary["reviews"]["most_recent"]["captured_review_rows"] == 40
    assert (
        summary["review_aggregates"]["native_sampling_review_count"] == 460
    )
    assert summary["questions"]["captured_included_answer_rows"] == 1
    assert summary["content_qualification"]["native_review_id_invariant_held"] is True

    loaded = root.load_raw_packet(result["packet_id"])
    manifest_doc = _artifact_json(loaded, "ulta_request_manifest.json")
    summary_doc = _artifact_json(loaded, "ulta_onboarding_summary.json")
    all_bytes = b"".join(loaded.bodies.values())
    manifest_bytes = json.dumps(manifest_doc).encode()
    summary_bytes = json.dumps(summary_doc).encode()
    assert _API_KEY.encode() not in manifest_bytes
    assert _API_KEY.encode() not in summary_bytes
    assert b"Body 500" in all_bytes  # exact raw response bytes preserved
    assert b"Body 500" not in summary_bytes  # summary carries no review bodies
    inventory_row = summary_doc["reviews"]["most_recent"]["review_inventory"][0]
    assert inventory_row["review_id"] == "500"
    assert inventory_row["body_present"] is True
    helpful_first = summary_doc["reviews"]["most_helpful"]["review_inventory"][0]
    assert helpful_first["disclosure_code"] == "sampling"


def test_acquisition_failure_preserves_partial_sequence_and_fails_loud(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_ulta_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        pages_per_role=2,
        api_fetcher=_api_fetcher(recent_status=500, total=40),
    )
    assert exit_code == 4
    summary = result["summary"]
    assert summary["record_kind"] == "ulta_powerreviews_onboarding_capture_failure_v1"
    assert summary["failure"]["http_status"] == 500
    loaded = root.load_raw_packet(result["packet_id"])
    names = _artifact_names(loaded)
    assert "reviews_most_helpful_offset_000.json" in names
    assert "reviews_most_recent_offset_000.json" in names  # failing bytes preserved
    assert "ulta_capture_failure.json" in names
    assert "ulta_onboarding_summary.json" not in names


def test_adaptation_failure_preserves_all_raw_responses(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_ulta_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        pages_per_role=1,
        api_fetcher=_api_fetcher(break_native_id=True, total=20),
    )
    assert exit_code == 5
    summary = result["summary"]
    assert (
        summary["record_kind"]
        == "ulta_powerreviews_onboarding_adaptation_failure_v1"
    )
    assert "native review-id invariant" in summary["failure"]["error"]
    loaded = root.load_raw_packet(result["packet_id"])
    names = _artifact_names(loaded)
    assert "reviews_most_recent_offset_000.json" in names
    assert "ulta_adaptation_failure.json" in names


def test_foreign_product_row_fails_adaptation_with_raw_fallback(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_ulta_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        pages_per_role=1,
        api_fetcher=_api_fetcher(foreign_recent_page_id=True, total=20),
    )
    assert exit_code == 5
    assert "foreign" in result["summary"]["failure"]["error"]


def test_parent_identity_mismatch_fails_before_any_api_read(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path, page_id="pimprod9999999")

    def _forbidden_fetch(*_args: Any, **_kwargs: Any) -> PowerReviewsResponse:
        raise AssertionError("no display request may be issued on identity mismatch")

    with pytest.raises(UltaOnboardingCaptureError, match="product mismatch"):
        capture_ulta_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            api_fetcher=_forbidden_fetch,
        )


def test_unpinned_parent_fails_before_any_api_read(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path, pin_confirmed=False)

    def _forbidden_fetch(*_args: Any, **_kwargs: Any) -> PowerReviewsResponse:
        raise AssertionError("no display request may be issued without a pin")

    with pytest.raises(UltaOnboardingCaptureError, match="US/USD market pin"):
        capture_ulta_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            api_fetcher=_forbidden_fetch,
        )


def test_parent_without_render_config_fails_sufficiency(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path, include_render_block=False)

    with pytest.raises(
        UltaOnboardingCaptureError, match="PowerReviewsRender configuration"
    ):
        capture_ulta_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            api_fetcher=_api_fetcher(),
        )


def test_key_echoing_response_is_refused_entirely(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    def _echoing_fetch(
        spec: PowerReviewsRequestSpec,
        _config: PowerReviewsReadConfig,
        _timeout_seconds: float,
        _max_bytes: int,
    ) -> PowerReviewsResponse:
        return PowerReviewsResponse(
            status=200,
            reason="OK",
            body=f'{{"echo": "{_API_KEY}"}}'.encode(),
            content_type="application/json",
            captured_at="2026-07-21T00:00:00Z",
        )

    with pytest.raises(UltaOnboardingCaptureError, match="echoed the public display key"):
        capture_ulta_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            api_fetcher=_echoing_fetch,
        )


def test_review_page_size_above_route_cap_is_rejected(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)
    with pytest.raises(ValueError, match="review_page_size"):
        capture_ulta_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            review_page_size=26,
            api_fetcher=_api_fetcher(),
        )


def test_corrupt_response_is_preserved_as_acquisition_failure(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_ulta_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        pages_per_role=1,
        api_fetcher=_api_fetcher(corrupt_recent=True, total=20),
    )
    assert exit_code == 4
    summary = result["summary"]
    assert summary["record_kind"] == "ulta_powerreviews_onboarding_capture_failure_v1"
    loaded = root.load_raw_packet(result["packet_id"])
    assert "reviews_most_recent_offset_000.json" in _artifact_names(loaded)


def test_config_resolution_requires_exactly_one_render_block() -> None:
    with pytest.raises(UltaPowerReviewsConfigError, match="exactly one"):
        resolve_ulta_powerreviews_config("<html>no config here</html>")
    doubled = _render_block() + _render_block()
    with pytest.raises(UltaPowerReviewsConfigError, match="exactly one"):
        resolve_ulta_powerreviews_config(doubled)


def test_config_resolution_rejects_invalid_key_shape() -> None:
    with pytest.raises(UltaPowerReviewsConfigError, match="invalid shape"):
        resolve_ulta_powerreviews_config(_render_block(api_key="not-a-key"))


def test_config_resolution_reads_page_declared_values() -> None:
    config = resolve_ulta_powerreviews_config(_render_block())
    assert config.merchant_id == _MERCHANT_ID
    assert config.merchant_group_id == "11984"
    assert config.page_id == _PRODUCT_ID
    assert config.locale == "en_US"
    assert config.api_key == _API_KEY
