from __future__ import annotations

import json
import gzip
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from source_capture.adapters.bazaarvoice_api import (
    ApiRequestSpec,
    ApiResponse,
    BazaarvoiceReadConfig,
)
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.adapters.target_bazaarvoice import (
    TargetBazaarvoiceConfigError,
    resolve_target_bazaarvoice_config,
)
from source_capture.models import known_fact
from source_capture.target_onboarding_capture import (
    TargetOnboardingCaptureError,
    capture_target_onboarding_packet,
)
from source_capture.writer import write_local_source_capture_packet


_TCIN = "80184023"
_PRODUCT_URL = f"https://www.target.com/p/-/A-{_TCIN}"
_DEPLOYMENT_URL = (
    "https://apps.bazaarvoice.com/deployments/"
    "targetcom/main_site/production/en_US/bv.js"
)
_LEGACY_URL = (
    "https://display.ugc.bazaarvoice.com/static/"
    "targetcom/main_site/en_US/bvapi.js"
)
_PASSKEY = "target-public-passkey-1234567890"
_NATIVE_URL = (
    "https://cdui-orchestrations.target.com/cdui_orchestrations/v1/pages/pdp"
    f"?key=public-target-key&tcin={_TCIN}&ratings_reviews_sort_by=most_recent"
)


def _parent_packet(
    root: DataLakeRoot,
    tmp_path: Path,
    *,
    embedded_tcin: str = _TCIN,
) -> str:
    next_data = {
        "props": {
            "dehydratedState": {
                "queries": [
                    {
                        "state": {
                            "data": {
                                "data": {
                                    "data_source_modules": [
                                        {
                                            "module_type": "ProductDetailWebDatasourceCore",
                                            "module_data": {
                                                "data": {
                                                    "product": {
                                                        "tcin": embedded_tcin,
                                                        "item": {
                                                            "product_description": {
                                                                "title": "Naturium Serum"
                                                            }
                                                        },
                                                        "ratings_and_reviews": {
                                                            "most_recent": []
                                                        },
                                                    }
                                                }
                                            },
                                        }
                                    ]
                                },
                                "metadata": {"url": _NATIVE_URL, "status": 200},
                            }
                        }
                    }
                ]
            }
        }
    }
    html = (
        '<script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(next_data, separators=(",", ":"))
        + "</script>"
        + f"<script>window.config={{bazaarvoice:{{baseUrl:'{_DEPLOYMENT_URL}'}}}};"
        + "</script>"
    )
    source = tmp_path / f"target-parent-{embedded_tcin}.html"
    source.write_text(html, encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[source],
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_PRODUCT_URL),
        decision_question="test Target parent",
        capture_context="rendered Target sample packet",
    )
    return result.packet.packet_id


def _config_fetcher(*, bad_passkey: bool = False, gzip_legacy: bool = False):
    def fetch(**kwargs: Any) -> DirectHttpCaptureSuccess:
        url = kwargs["url"]
        if url == _DEPLOYMENT_URL:
            body = f'const c={{legacyScoutUrl:"{_LEGACY_URL}"}};'.encode()
        elif url == _LEGACY_URL:
            passkey = "short" if bad_passkey else _PASSKEY
            body = (
                'deploymentId:"targetcom/main_site/PRODUCTION/en_US",'
                f'apiconfig:{{limit:10,passkey:"{passkey}",'
                'baseUrl:"//api.bazaarvoice.com/data/",'
                'displaycode:"19988-en_us"},'
                "prefetchConfigs:[{url:"
                '"https://api.bazaarvoice.com/data/batch.json?'
                'passkey=REDACTED&apiversion=5.5"}]'
            ).encode()
            if gzip_legacy:
                body = gzip.compress(body)
        else:
            raise AssertionError(f"unexpected config URL: {url}")
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=200,
            reason="OK",
            metadata={
                "capture_timestamp": "2026-07-21T00:00:00Z",
                "content_type": "application/javascript",
            },
            body=body,
            warning_notes=[],
            limitation_notes=[],
        )

    return fetch


def _review_row(
    review_id: str,
    submitted_at: str,
    text: str,
    *,
    positive: int,
    source_client: str = "targetcom",
    syndicated: bool = False,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "Id": review_id,
        "ProductId": _TCIN,
        "ReviewText": text,
        "Title": f"Title {review_id}",
        "SubmissionTime": submitted_at,
        "Rating": 5,
        "UserNickname": f"user-{review_id}",
        "IsRecommended": True,
        "IsSyndicated": syndicated,
        "SourceClient": source_client,
        "TotalPositiveFeedbackCount": positive,
        "TotalNegativeFeedbackCount": 1,
        "TotalClientResponseCount": 0,
        "Badges": {"verifiedPurchaser": {"Id": "verifiedPurchaser"}},
        "ContextDataValues": {},
        "Photos": [],
        "Videos": [],
    }
    if syndicated:
        row["SyndicationSource"] = {"Name": "Naturium"}
    return row


def _api_fetcher(*, corrupt_recent: bool = False, recent_status: int = 200):
    def fetch(
        spec: ApiRequestSpec,
        config: BazaarvoiceReadConfig,
        _timeout_seconds: float,
        _max_bytes: int,
    ) -> ApiResponse:
        assert config.host == "api.bazaarvoice.com"
        assert config.version == "5.5"
        assert config.token == _PASSKEY
        assert ("displaycode", "19988-en_us") in spec.parameters
        assert not any(
            "IncentivizedReview" in value for _name, value in spec.parameters
        )
        if spec.config_kind == "questions":
            assert ("Sort", "TotalAnswerCount:desc") in spec.parameters
            document = {
                "HasErrors": False,
                "TotalResults": 2,
                "Results": [
                    {
                        "Id": "q1",
                        "ProductId": _TCIN,
                        "QuestionSummary": "First?",
                        "QuestionDetails": "First details",
                        "TotalAnswerCount": 2,
                        "AnswerIds": ["a1", "a2"],
                        "SubmissionTime": "2026-01-01T00:00:00Z",
                    },
                    {
                        "Id": "q2",
                        "ProductId": _TCIN,
                        "QuestionSummary": "Second?",
                        "QuestionDetails": "Second details",
                        "TotalAnswerCount": 1,
                        "AnswerIds": ["a3"],
                        "SubmissionTime": "2026-01-02T00:00:00Z",
                    },
                ],
                "Includes": {
                    "Answers": {
                        "a1": {
                            "Id": "a1",
                            "QuestionId": "q1",
                            "AnswerText": "Answer one",
                            "SubmissionTime": "2026-01-03T00:00:00Z",
                            "IsBestAnswer": True,
                            "IsBrandAnswer": False,
                        },
                        "a2": {
                            "Id": "a2",
                            "QuestionId": "q1",
                            "AnswerText": "Answer two",
                            "SubmissionTime": "2026-01-04T00:00:00Z",
                            "IsBestAnswer": False,
                            "IsBrandAnswer": True,
                        },
                        "a3": {
                            "Id": "a3",
                            "QuestionId": "q2",
                            "AnswerText": "Answer three",
                            "SubmissionTime": "2026-01-05T00:00:00Z",
                            "IsBestAnswer": True,
                            "IsBrandAnswer": False,
                        },
                    },
                    "Products": {_TCIN: {"Id": _TCIN}},
                },
            }
        elif spec.artifact_name == "reviews_most_helpful_offset_000.json":
            assert ("Sort", "TotalPositiveFeedbackCount:desc") in spec.parameters
            document = {
                "HasErrors": False,
                "TotalResults": 758,
                "Results": [
                    _review_row(
                        "h1",
                        "2024-01-01T00:00:00Z",
                        "Helpful one",
                        positive=9,
                    ),
                    _review_row(
                        "h2",
                        "2024-02-01T00:00:00Z",
                        "Helpful two",
                        positive=4,
                    ),
                ],
                "Includes": {
                    "Products": {
                        _TCIN: {
                            "Id": _TCIN,
                            "Name": "Naturium Vitamin C Complex Serum",
                            "Brand": "Naturium",
                            "BrandExternalId": "naturium",
                            "CategoryId": "beauty",
                            "FamilyIds": [],
                            "UPCs": ["008100707001"],
                            "ProductPageUrl": _PRODUCT_URL,
                            "ReviewStatistics": {
                                "TotalReviewCount": 1096,
                                "AverageOverallRating": 4.35,
                                "RatingDistribution": [
                                    {"RatingValue": 5, "Count": 797}
                                ],
                                "RecommendedCount": 163,
                                "NotRecommendedCount": 80,
                                "TotalPhotoCount": 27,
                                "TotalVideoCount": 0,
                                "ContextDataDistribution": {},
                            },
                            "FilteredReviewStatistics": {
                                "TotalReviewCount": 758,
                                "AverageOverallRating": 4.19,
                                "ContextDataDistribution": {},
                            },
                        }
                    }
                },
            }
        else:
            assert spec.artifact_name == "reviews_most_recent_offset_000.json"
            assert ("Sort", "SubmissionTime:desc") in spec.parameters
            document = {
                "HasErrors": False,
                "TotalResults": 758,
                "Results": [
                    _review_row(
                        "r1",
                        "2026-06-11T00:00:00Z",
                        "Recent one",
                        positive=2,
                    ),
                    _review_row(
                        "r2",
                        "2026-06-10T00:00:00Z",
                        "Recent two",
                        positive=1,
                        source_client="naturium",
                        syndicated=True,
                    ),
                ],
                "Includes": {"Authors": {}, "Comments": {}},
            }
        if corrupt_recent and spec.artifact_name == "reviews_most_recent_offset_000.json":
            body = b"{invalid-json"
        else:
            body = json.dumps(document, separators=(",", ":")).encode()
        status = (
            recent_status
            if spec.artifact_name == "reviews_most_recent_offset_000.json"
            else 200
        )
        return ApiResponse(
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


def test_success_preserves_three_roles_without_body_or_passkey_duplication(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_target_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        review_limit=2,
        config_fetcher=_config_fetcher(),
        api_fetcher=_api_fetcher(),
    )

    assert exit_code == 0
    loaded = root.load_raw_packet(result["packet_id"])
    assert loaded.manifest["source_surface"] == "target_bazaarvoice_onboarding"
    summary = _artifact_json(loaded, "target_onboarding_summary.json")
    assert summary["provider"] == "bazaarvoice"
    assert summary["identity"]["target_tcin"] == _TCIN
    assert summary["identity"]["bazaarvoice_product_id"] == _TCIN
    assert summary["identity"]["mapping_equal"] is True
    assert summary["questions"]["captured_question_rows"] == 2
    assert summary["questions"]["captured_included_answer_rows"] == 3
    assert summary["reviews"]["last_seen_review_id"] == "r1"
    assert summary["reviews"]["source_clients"] == ["naturium", "targetcom"]
    assert summary["reviews"]["context_dimension_keys"] == []
    assert summary["retailer_native_observation"]["provider"] == "Target"
    assert "not labelled or counted as Bazaarvoice" in summary[
        "retailer_native_observation"
    ]["provenance_note"]
    assert summary["content_qualification"]["status"] == "passed"
    assert summary["row_accounting"] == {
        "answers_equal": True,
        "helpful_rows_equal": True,
        "question_rows_equal": True,
        "recent_rows_equal": True,
    }

    summary_text = json.dumps(summary)
    for body in (
        "Helpful one",
        "Helpful two",
        "Recent one",
        "Recent two",
        "Answer one",
        "Answer two",
        "Answer three",
        _PASSKEY,
    ):
        assert body not in summary_text
    request_manifest = _artifact_json(loaded, "target_request_manifest.json")
    assert _PASSKEY not in json.dumps(request_manifest)
    assert all(
        request["endpoint"].startswith("https://api.bazaarvoice.com/data/")
        for request in request_manifest["requests"]
    )
    assert not any(
        "IncentivizedReview" in parameter["value"]
        for request in request_manifest["requests"]
        for parameter in request["parameters"]
    )
    raw_bodies = b"".join(loaded.bodies.values())
    assert b"Helpful one" in raw_bodies
    assert b"Recent one" in raw_bodies
    assert b"Answer one" in raw_bodies


def test_adaptation_failure_preserves_all_raw_responses(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_target_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        review_limit=2,
        config_fetcher=_config_fetcher(),
        api_fetcher=_api_fetcher(corrupt_recent=True),
    )

    assert exit_code == 5
    loaded = root.load_raw_packet(result["packet_id"])
    failure = _artifact_json(loaded, "target_adaptation_failure.json")
    assert failure["raw_failure_fallback"] == {
        "expected_response_count": 3,
        "preserved_response_count": 3,
        "status": "all_responses_preserved",
    }
    assert any(body == b"{invalid-json" for body in loaded.bodies.values())


def test_http_failure_preserves_partial_sequence_and_fails_loud(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path)

    exit_code, result = capture_target_onboarding_packet(
        data_root=root,
        parent_packet_id=parent_id,
        review_limit=2,
        config_fetcher=_config_fetcher(),
        api_fetcher=_api_fetcher(recent_status=500),
    )

    assert exit_code == 4
    loaded = root.load_raw_packet(result["packet_id"])
    failure = _artifact_json(loaded, "target_capture_failure.json")
    assert failure["failure"]["artifact_name"] == "reviews_most_recent_offset_000.json"
    assert failure["failure"]["http_status"] == 500
    assert failure["raw_failure_fallback"]["preserved_response_count"] == 3


def test_parent_identity_mismatch_fails_before_config_or_api_reads(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent_id = _parent_packet(root, tmp_path, embedded_tcin="99999999")

    with pytest.raises(TargetOnboardingCaptureError, match="parent product mismatch"):
        capture_target_onboarding_packet(
            data_root=root,
            parent_packet_id=parent_id,
            config_fetcher=lambda **_kwargs: pytest.fail("config fetch must not run"),
            api_fetcher=lambda *_args: pytest.fail("API fetch must not run"),
        )


def test_public_config_resolution_rejects_invalid_passkey_shape() -> None:
    with pytest.raises(TargetBazaarvoiceConfigError, match="invalid shape"):
        resolve_target_bazaarvoice_config(
            deployment_url=_DEPLOYMENT_URL,
            timeout_seconds=20,
            max_bytes=1_000_000,
            fetcher=_config_fetcher(bad_passkey=True),
        )


def test_public_config_resolution_decodes_source_delivered_gzip() -> None:
    resolution = resolve_target_bazaarvoice_config(
        deployment_url=_DEPLOYMENT_URL,
        timeout_seconds=20,
        max_bytes=1_000_000,
        fetcher=_config_fetcher(gzip_legacy=True),
    )

    assert resolution.config.token == _PASSKEY
    assert resolution.config.version == "5.5"
    assert resolution.config_receipts[1].byte_count > 0
