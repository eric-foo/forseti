from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.sephora_onboarding_capture import (
    ApiRequestSpec,
    ApiResponse,
    BazaarvoiceReadConfig,
    SEPHORA_AGE_BUCKETS,
    SephoraOnboardingCaptureError,
    capture_sephora_onboarding_packet,
)
from source_capture.writer import write_local_source_capture_packet


_PRODUCT_URL = (
    "https://www.sephora.com/product/lip-sleeping-mask-P420652"
    "?country_switch=us&lang=en"
)
_REVIEW_TOKEN = "review-read-token"
_QUESTION_TOKEN = "question-read-token"


def _parent_packet(
    root: DataLakeRoot,
    tmp_path: Path,
    *,
    link_store_product_id: str = "P420652",
) -> str:
    link_store = {
        "page": {
            "product": {
                "productId": link_store_product_id,
                "currentSku": {"skuId": "2961324"},
                "regularChildSkus": [
                    {"skuId": "1966258"},
                    {"skuId": "2902831"},
                ],
                # The old generic configuration is intentionally present. It is
                # not the rendered live age-filter authority.
                "reviewFilters": [
                    {
                        "id": "age",
                        "values": ["13-17", "18-24", "25-34", "35-44", "45-54", "Over54"],
                    }
                ],
            }
        }
    }
    config = {
        "bvApi_rwdRating_desktop_read": {
            "host": "api.bazaarvoice.com",
            "version": "5.4",
            "token": _REVIEW_TOKEN,
        },
        "bvApi_rwdQandA_desktop_read": {
            "host": "api.bazaarvoice.com",
            "version": "5.4",
            "token": _QUESTION_TOKEN,
        },
    }
    html = (
        '<script id="linkStore" type="text/json">'
        + json.dumps(link_store, separators=(",", ":"))
        + "</script><script>Sephora.configurationSettings="
        + json.dumps(config, separators=(",", ":"))
        + ";</script>"
    )
    source = tmp_path / f"parent-{link_store_product_id}.html"
    source.write_text(html, encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[source],
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_PRODUCT_URL),
        decision_question="test Sephora parent",
        capture_context="rendered Sephora sample packet",
    )
    return result.packet.packet_id


def _question_document() -> dict:
    return {
        "HasErrors": False,
        "TotalResults": 1390,
        "Results": [
            {
                "Id": "q1",
                "ProductId": "P420652",
                "QuestionSummary": "First?",
                "QuestionDetails": "First question details",
                "TotalAnswerCount": 2,
                "SubmissionTime": "2026-01-01T00:00:00Z",
                "UserNickname": "one",
            },
            {
                "Id": "q2",
                "ProductId": "P420652",
                "QuestionSummary": "Second?",
                "QuestionDetails": "Second question details",
                "TotalAnswerCount": 1,
                "SubmissionTime": "2026-01-02T00:00:00Z",
                "UserNickname": "two",
            },
        ],
        "Includes": {
            "Answers": {
                "a1": {"Id": "a1", "AnswerText": "A"},
                "a2": {"Id": "a2", "AnswerText": "B"},
                "a3": {"Id": "a3", "AnswerText": "C"},
            }
        },
    }


def _fake_fetcher(*, corrupt_age: str | None = None):
    totals = {
        "reviews_non_incentivized_total.json": 14327,
        "reviews_non_incentivized_age_20s.json": 244,
        "reviews_non_incentivized_age_30s.json": 338,
        "reviews_non_incentivized_age_40s.json": 130,
        "reviews_non_incentivized_age_50s_plus.json": 563,
    }

    def fetch(
        spec: ApiRequestSpec,
        config: BazaarvoiceReadConfig,
        _timeout_seconds: float,
        _max_bytes: int,
    ) -> ApiResponse:
        assert config.host == "api.bazaarvoice.com"
        if spec.config_kind == "questions":
            assert config.token == _QUESTION_TOKEN
            document = _question_document()
        else:
            assert config.token == _REVIEW_TOKEN
            if spec.artifact_name == "reviews_non_incentivized_age_50s_plus.json":
                assert (
                    "Filter",
                    "ContextDataValue_ageRange:eq:50s",
                ) in spec.parameters
            document = {
                "HasErrors": False,
                "TotalResults": totals[spec.artifact_name],
                "Results": [{"Id": "r1", "ProductId": "P420652"}],
            }
        if spec.artifact_name == corrupt_age:
            body = b"{invalid-json"
        else:
            body = json.dumps(document, separators=(",", ":")).encode("utf-8")
        return ApiResponse(
            status=200,
            reason="OK",
            body=body,
            content_type="application/json",
            captured_at="2026-07-20T00:00:00Z",
        )

    return fetch


def _artifact_json(loaded, suffix: str) -> dict:
    preserved = next(
        item
        for item in loaded.manifest["preserved_files"]
        if item["relative_packet_path"].endswith(suffix)
    )
    return json.loads(loaded.bodies[preserved["file_id"]].decode("utf-8"))


def test_success_preserves_raw_and_projects_exact_age_breakdown(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_sephora_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        fetcher=_fake_fetcher(),
    )

    assert exit_code == 0
    loaded = root.load_raw_packet(result["packet_id"])
    assert loaded.manifest["source_surface"] == "sephora_bazaarvoice_onboarding"
    summary = _artifact_json(loaded, "sephora_onboarding_summary.json")
    assert summary["reviews"]["live_age_bucket_values"] == list(SEPHORA_AGE_BUCKETS)
    assert summary["reviews"]["exact_non_incentivized_total"] == 14327
    assert summary["reviews"]["declared_age_subset_total"] == 1275
    assert summary["reviews"]["declared_age_coverage_pct"] == 8.9
    assert summary["reviews"]["without_live_age_bucket_pct"] == 91.1
    assert summary["reviews"]["age_breakdown"] == [
        {
            "bucket": "20s",
            "api_value": "20s",
            "count": 244,
            "share_of_declared_age_subset_pct": 19.14,
            "share_of_all_non_incentivized_reviews_pct": 1.7,
        },
        {
            "bucket": "30s",
            "api_value": "30s",
            "count": 338,
            "share_of_declared_age_subset_pct": 26.51,
            "share_of_all_non_incentivized_reviews_pct": 2.36,
        },
        {
            "bucket": "40s",
            "api_value": "40s",
            "count": 130,
            "share_of_declared_age_subset_pct": 10.2,
            "share_of_all_non_incentivized_reviews_pct": 0.91,
        },
        {
            "bucket": "50s +",
            "api_value": "50s",
            "count": 563,
            "share_of_declared_age_subset_pct": 44.16,
            "share_of_all_non_incentivized_reviews_pct": 3.93,
        },
    ]
    assert summary["questions"]["total_questions"] == 1390
    assert summary["questions"]["captured_question_rows"] == 2
    assert summary["questions"]["captured_included_answer_rows"] == 3
    assert summary["row_accounting"]["answers_equal"] is True
    assert summary["content_qualification"]["status"] == "passed"

    names = {
        Path(item["original_path"]).name
        for item in loaded.manifest["preserved_files"]
    }
    assert "questions_most_answers_offset_000.json" in names
    assert "sephora_request_manifest.json" in names
    assert "sephora_onboarding_summary.json" in names
    persisted = b"".join(loaded.bodies.values())
    assert _REVIEW_TOKEN.encode() not in persisted
    assert _QUESTION_TOKEN.encode() not in persisted


def test_adaptation_failure_commits_every_raw_response_as_fallback(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_sephora_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        fetcher=_fake_fetcher(corrupt_age="reviews_non_incentivized_age_40s.json"),
    )

    assert exit_code == 5
    loaded = root.load_raw_packet(result["packet_id"])
    names = [
        Path(item["original_path"]).name
        for item in loaded.manifest["preserved_files"]
    ]
    assert len([name for name in names if name.endswith(".json")]) == 8
    assert "sephora_adaptation_failure.json" in names
    failure = _artifact_json(loaded, "sephora_adaptation_failure.json")
    assert failure["raw_failure_fallback"] == {
        "expected_response_count": 6,
        "preserved_response_count": 6,
        "status": "all_responses_preserved",
    }
    assert any(
        "exact raw API response bytes are preserved"
        in limitation
        for limitation in loaded.manifest["limitations"]
    )


def test_parent_product_identity_mismatch_fails_before_fetch(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path, link_store_product_id="P999999")
    calls = 0

    def fetch(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        raise AssertionError("must not fetch")

    with pytest.raises(SephoraOnboardingCaptureError, match="parent product mismatch"):
        capture_sephora_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            fetcher=fetch,
        )
    assert calls == 0
