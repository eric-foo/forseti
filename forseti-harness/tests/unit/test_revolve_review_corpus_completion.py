from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from runners import run_revolve_review_corpus_completion as runner
from source_capture.adapters.browser_snapshot import BrowserPageResponse
from source_capture.revolve_pdp_content import RevolvePdpAggregateContentRecord
from source_capture.revolve_review_corpus_completion import (
    RevolveReviewCorpusReceipt,
    capture_revolve_recent_review_corpus,
    group_revolve_review_corpora,
)


_STORE_ID = "b4k4hvSXVzfPzX41MmcY1NO4yJyOAtVxDGEh4bxA"


def _record(
    style_id: str, *, review_count: int | None
) -> RevolvePdpAggregateContentRecord:
    return RevolvePdpAggregateContentRecord(
        source_url=f"https://www.revolve.com/example/dp/{style_id}/",
        style_id=style_id,
        product={"sku": style_id, "name": style_id},
        offer={"price": "24.00", "priceCurrency": "USD"},
        review_substrate={
            "provider": "yotpo",
            "store_id": _STORE_ID,
            "product_id": style_id,
            "review_count": review_count,
            "qna_exposed": False,
        },
        input_hashes={"rendered_dom": "a" * 64, "visible_text": "b" * 64},
    )


def _response(
    url: str,
    *,
    total: int,
    start: int,
    count: int,
) -> BrowserPageResponse:
    reference = date(2026, 7, 25)
    reviews = [
        {
            "id": f"review-{index}",
            "createdAt": (
                reference - timedelta(days=index - 1)
            ).isoformat()
            + "T12:00:00+00:00",
            "content": f"Review {index}",
        }
        for index in range(start, start + count)
    ]
    page = int(parse_qs(urlparse(url).query)["page"][0])
    return BrowserPageResponse(
        requested_url=url,
        final_url=url,
        status=200,
        ok=True,
        body_text=json.dumps(
            {
                "pagination": {"page": page, "perPage": 10, "total": total},
                "reviews": reviews,
            },
            separators=(",", ":"),
        ),
        response_headers={"content-type": "application/json"},
    )


def test_recent_corpus_capture_requests_only_date_order_and_admits_bound() -> None:
    requested: list[str] = []

    def fetcher(urls, _timeout_seconds, _max_response_bytes):
        requested.extend(urls)
        return [
            _response(
                url,
                total=25,
                start=(page - 1) * 10 + 1,
                count=min(10, 25 - (page - 1) * 10),
            )
            for page, url in enumerate(urls, start=1)
        ]

    receipt = capture_revolve_recent_review_corpus(
        content_records=[_record("SUMR-WU1", review_count=25)],
        review_limit=30,
        reference_date=date(2026, 7, 25),
        fetcher=fetcher,
    )

    assert receipt.status == "complete"
    assert receipt.actual_ordering == "Most Recent"
    assert len(receipt.captured_review_ids) == 25
    assert receipt.onboarding_assessment is not None
    assert receipt.onboarding_assessment["status"] == "source_exhausted"
    assert all(parse_qs(urlparse(url).query)["sort"] == ["date"] for url in requested)


def test_zero_row_corpus_is_complete_without_transport() -> None:
    called = False

    def fetcher(_urls, _timeout_seconds, _max_response_bytes):
        nonlocal called
        called = True
        return []

    receipt = capture_revolve_recent_review_corpus(
        content_records=[_record("SUMR-WU2", review_count=0)],
        fetcher=fetcher,
    )

    assert receipt.status == "complete"
    assert receipt.declared_review_count == 0
    assert receipt.captured_review_ids == []
    assert called is False


def test_missing_pdp_count_is_discovered_from_bound_yotpo_response() -> None:
    calls: list[list[str]] = []

    def fetcher(urls, _timeout_seconds, _max_response_bytes):
        calls.append(list(urls))
        if not urls:
            return []
        return [
            _response(urls[0], total=5, start=1, count=5)
        ]

    receipt = capture_revolve_recent_review_corpus(
        content_records=[_record("SUMR-WU4", review_count=None)],
        review_limit=30,
        reference_date=date(2026, 7, 25),
        fetcher=fetcher,
    )

    assert receipt.status == "complete"
    assert receipt.declared_review_count == 5
    assert len(receipt.captured_review_ids) == 5
    assert len(calls) == 1


def test_grouping_collapses_duplicate_listing_packets_for_one_corpus() -> None:
    record = _record("SUMR-WU3", review_count=5)

    groups = group_revolve_review_corpora([record, record.model_copy(deep=True)])

    assert len(groups) == 1
    assert len(groups[0]) == 2


def test_runner_accounts_every_listing_and_corpus(
    tmp_path: Path,
    monkeypatch,
) -> None:
    pdp_root = tmp_path / "pdp"
    for style_id in ("SUMR-WU1", "SUMR-WU2"):
        packet = pdp_root / style_id
        packet.mkdir(parents=True)
        (packet / "manifest.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        runner,
        "_load_revolve_pdp_record",
        lambda packet: _record(
            packet.name,
            review_count=5 if packet.name == "SUMR-WU1" else 0,
        ),
    )

    def capture(*, content_records, review_limit):
        record = content_records[0]
        count = int(record.review_substrate["review_count"])
        return RevolveReviewCorpusReceipt(
            provider_tenant_store=_STORE_ID,
            collection_context=f"product/{record.style_id}",
            corpus_key=f"review_corpus_{record.style_id.lower()}",
            source_product_ids=[record.style_id],
            source_urls=[record.source_url],
            requested_limit=review_limit,
            declared_review_count=count,
            captured_review_ids=(
                [f"{record.style_id}-review-1"] if count else []
            ),
            onboarding_assessment={
                "admitted": True,
                "status": "source_exhausted",
            },
            transport_posture="caller_supplied_unverified",
            proxy_used=None,
            status="complete",
        )

    monkeypatch.setattr(runner, "capture_revolve_recent_review_corpus", capture)
    output_root = tmp_path / "output"

    exit_code, receipt = runner.run_revolve_review_corpus_completion(
        pdp_root=pdp_root,
        output_root=output_root,
        max_workers=2,
    )

    assert exit_code == 0
    assert receipt.status == "complete"
    assert receipt.requested_listing_count == 2
    assert receipt.verified_listing_count == 2
    assert receipt.distinct_corpus_count == 2
    assert receipt.completed_corpus_count == 2
    assert receipt.row_positive_corpus_count == 1
    assert receipt.zero_row_corpus_count == 1
    assert receipt.captured_review_occurrence_count == 1
    assert receipt.unique_review_id_count == 1
    assert receipt.cross_corpus_duplicate_review_ids == []
    assert receipt.corpus_overlap_pairs == []
    assert receipt.independent_corpus_family_count == 2


def test_runner_reports_cross_corpus_overlap_without_failing_completion(
    tmp_path: Path,
    monkeypatch,
) -> None:
    pdp_root = tmp_path / "pdp"
    for style_id in ("SUMR-WU1", "SUMR-WU14"):
        packet = pdp_root / style_id
        packet.mkdir(parents=True)
        (packet / "manifest.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        runner,
        "_load_revolve_pdp_record",
        lambda packet: _record(packet.name, review_count=5),
    )

    def capture(*, content_records, review_limit):
        record = content_records[0]
        return RevolveReviewCorpusReceipt(
            provider_tenant_store=_STORE_ID,
            collection_context=f"product/{record.style_id}",
            corpus_key=f"review_corpus_{record.style_id.lower()}",
            source_product_ids=[record.style_id],
            source_urls=[record.source_url],
            requested_limit=review_limit,
            declared_review_count=5,
            captured_review_ids=["shared-review-id"],
            onboarding_assessment={
                "admitted": True,
                "status": "source_exhausted",
            },
            transport_posture="caller_supplied_unverified",
            proxy_used=None,
            status="complete",
        )

    monkeypatch.setattr(runner, "capture_revolve_recent_review_corpus", capture)

    exit_code, receipt = runner.run_revolve_review_corpus_completion(
        pdp_root=pdp_root,
        output_root=tmp_path / "output",
        max_workers=2,
    )

    assert exit_code == 0
    assert receipt.status == "complete"
    assert receipt.captured_review_occurrence_count == 2
    assert receipt.unique_review_id_count == 1
    assert receipt.cross_corpus_duplicate_review_ids == ["shared-review-id"]
    assert receipt.independent_corpus_family_count == 1
    assert len(receipt.corpus_overlap_pairs) == 1
    assert receipt.corpus_overlap_pairs[0].source_product_ids == [
        "SUMR-WU1",
        "SUMR-WU14",
    ]
