from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from cleaning.retail_review_overlap import (
    RetailReviewOverlapError,
    build_depth_selection,
    build_review_linkage,
    load_depth_selection_commission,
    load_review_linkage_commission,
    write_depth_selection,
    write_review_linkage,
)
from source_capture.models import known_fact
from source_capture.retail_grid_projection import (
    load_verified_source_capture_packet_directory,
)
from source_capture.writer import write_local_source_capture_packet

_LADDER = ("sephora", "ulta", "target", "amazon")


def test_selection_requires_a_named_job_and_can_select_a_non_prominent_product(
    tmp_path: Path,
) -> None:
    portfolio_path = _portfolio_output(tmp_path)
    commission_path = tmp_path / "selection-commission.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "portfolio_onboarding_path": str(portfolio_path),
            "candidates": [
                {
                    "owned_parent_id": "famous",
                    "prominence_status": "PROMINENT",
                    "jobs": [],
                },
                {
                    "owned_parent_id": "complaint-product",
                    "prominence_status": "NOT_PROMINENT",
                    "jobs": [
                        {
                            "job_id": "complaints",
                            "trigger": "COMPLAINT_CONCENTRATION",
                            "information_job": "Test whether complaints repeat across retailers",
                            "decision_use": "Change the plausible weak-link assessment",
                            "evidence_refs": ["portfolio:complaint-concentration"],
                            "depth_surfaces": ["REVIEWS", "QA"],
                        }
                    ],
                },
            ],
        },
    )

    commission = load_depth_selection_commission(commission_path)
    first = build_depth_selection(
        commission=commission,
        base_directory=tmp_path,
    )
    second = build_depth_selection(
        commission=commission,
        base_directory=tmp_path,
    )

    assert first == second
    assert [item["owned_parent_id"] for item in first["selected_products"]] == [
        "complaint-product"
    ]
    assert first["not_selected_products"] == [
        {
            "owned_parent_id": "famous",
            "prominence_status": "PROMINENT",
            "reason": "NO_NAMED_NON_DUPLICATIVE_JOB",
        }
    ]
    jobs = first["companion_onboarding_jobs"]
    assert len(jobs) == 8
    assert {(item["retailer"], item["surface"]) for item in jobs} == {
        (retailer, surface)
        for retailer in _LADDER
        for surface in ("REVIEWS", "QA")
    }
    assert len({item["capture_job_id"] for item in jobs}) == len(jobs)
    assert all(
        item["baseline_packet_id"] == f"{item['retailer']}-baseline-packet"
        for item in jobs
    )
    assert all(
        item["failure_posture"]
        == "PRESERVE_TYPED_FAILURE; NO_COMPLETION_CREDIT"
        for item in jobs
    )


def test_selection_accepts_product_identity_v2_without_changing_parent_jobs(
    tmp_path: Path,
) -> None:
    portfolio_path = _portfolio_output(
        tmp_path, schema_version="retail_portfolio_onboarding_v2"
    )
    commission_path = tmp_path / "selection-v2.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "portfolio_onboarding_path": str(portfolio_path),
            "candidates": [
                {
                    "owned_parent_id": "famous",
                    "prominence_status": "NOT_PROMINENT",
                    "jobs": [],
                }
            ],
        },
    )

    result = build_depth_selection(
        commission=load_depth_selection_commission(commission_path),
        base_directory=tmp_path,
    )

    assert result["not_selected_products"] == [
        {
            "owned_parent_id": "famous",
            "prominence_status": "NOT_PROMINENT",
            "reason": "NO_NAMED_NON_DUPLICATIVE_JOB",
        }
    ]
def test_selection_write_is_write_once(tmp_path: Path) -> None:
    portfolio_path = _portfolio_output(tmp_path)
    commission_path = tmp_path / "selection-commission.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "portfolio_onboarding_path": str(portfolio_path),
            "candidates": [
                {
                    "owned_parent_id": "complaint-product",
                    "prominence_status": "NOT_PROMINENT",
                    "jobs": [
                        {
                            "job_id": "incident",
                            "trigger": "INCIDENT",
                            "information_job": "Resolve the incident",
                            "decision_use": "Change the incident interpretation",
                            "evidence_refs": ["event:incident"],
                            "depth_surfaces": ["REVIEWS"],
                        }
                    ],
                }
            ],
        },
    )
    output_path = tmp_path / "selection.json"
    write_depth_selection(
        commission_path=commission_path,
        output_path=output_path,
    )
    with pytest.raises(RetailReviewOverlapError, match="refusing overwrite"):
        write_depth_selection(
            commission_path=commission_path,
            output_path=output_path,
        )


def test_linkage_is_deterministic_preserves_occurrences_and_queues_conflicts(
    tmp_path: Path,
) -> None:
    selection_path = _selection_output(tmp_path)
    refs = {
        retailer: _review_packet(tmp_path, retailer)
        for retailer in ("sephora", "target", "ulta", "amazon")
    }
    occurrences = [
        _occurrence(
            "o1",
            "sephora",
            refs["sephora"],
            provider="Bazaarvoice",
            native_id="sephora-1",
            origin_id="origin-1",
            rating=5,
            date="2026-01-01",
            author="Alex",
            title="Great",
            body="Works   all day.",
        ),
        _occurrence(
            "o2",
            "target",
            refs["target"],
            provider="bazaarvoice",
            native_id="target-9",
            origin_id="ORIGIN-1",
            rating="5.0",
            date="2026-01-01",
            author="alex",
            title="great",
            body="works all day.",
        ),
        _occurrence(
            "o3",
            "ulta",
            refs["ulta"],
            provider="PowerReviews",
            native_id=None,
            origin_id=None,
            rating=5,
            date="2026-01-01",
            author="Alex",
            title="Great",
            body="Works all day.",
        ),
        _occurrence(
            "o4",
            "amazon",
            refs["amazon"],
            provider="amazon-native",
            native_id="amazon-4",
            origin_id=None,
            rating=4,
            date="2026-01-01",
            author="Alex",
            title="Great",
            body="Works all day.",
        ),
        _occurrence(
            "o5",
            "sephora",
            refs["sephora"],
            provider="Bazaarvoice",
            native_id="sephora-2",
            origin_id=None,
            rating=4,
            date="2026-02-01",
            author="Bea",
            title="Good",
            body="A second review.",
            syndication_key="syndicated-2",
        ),
        _occurrence(
            "o6",
            "target",
            refs["target"],
            provider="bazaarvoice",
            native_id="target-2",
            origin_id=None,
            rating=4,
            date="2026-02-01",
            author=None,
            title="Good",
            body="A second review.",
            syndication_key="SYNDICATED-2",
        ),
    ]
    native_totals = [
        _native_total("sephora", 1000, refs["sephora"]),
        _native_total("target", 900, refs["target"]),
    ]
    commission_path = tmp_path / "linkage-commission.json"
    payload = {
        "company_id": "example-company",
        "selection_output_path": str(selection_path),
        "corpus_label": "bounded onboarding windows",
        "occurrences": occurrences,
        "native_review_totals": native_totals,
    }
    _write_json(commission_path, payload)
    commission = load_review_linkage_commission(commission_path)

    first = build_review_linkage(
        commission=commission,
        base_directory=tmp_path,
    )
    second = build_review_linkage(
        commission=commission,
        base_directory=tmp_path,
    )

    assert first == second
    assert [item["occurrence_id"] for item in first["occurrences"]] == [
        "o1",
        "o2",
        "o3",
        "o4",
        "o5",
        "o6",
    ]
    output_refs = {
        item["occurrence_id"]: item["raw_refs"]
        for item in first["occurrences"]
    }
    assert output_refs == {
        item["occurrence_id"]: item["raw_refs"]
        for item in occurrences
    }
    assert [item["native_total"] for item in first["native_review_totals"]] == [
        1000,
        900,
    ]

    groups = [
        set(item["occurrence_ids"])
        for item in first["unique_review_groups"]
    ]
    assert {"o1", "o2", "o3"} in groups
    assert {"o4"} in groups
    assert {"o5", "o6"} in groups
    three_way = next(
        item
        for item in first["unique_review_groups"]
        if set(item["occurrence_ids"]) == {"o1", "o2", "o3"}
    )
    assert three_way["match_bases"] == [
        "PROVIDER_ORIGIN_ID",
        "NORMALIZED_EXACT_FINGERPRINT",
    ]
    syndicated = next(
        item
        for item in first["unique_review_groups"]
        if set(item["occurrence_ids"]) == {"o5", "o6"}
    )
    assert syndicated["match_bases"] == ["EXPLICIT_SYNDICATION"]

    ambiguous_pairs = {
        tuple(item["occurrence_ids"])
        for item in first["ambiguous_queue"]
        if item["candidate_basis"] == "NORMALIZED_NEAR_MATCH"
    }
    assert ("o1", "o4") in ambiguous_pairs
    assert ("o2", "o4") in ambiguous_pairs
    assert ("o3", "o4") in ambiguous_pairs
    metrics = first["metrics_by_product"][0]
    assert metrics["captured_native_occurrence_total"] == 6
    assert metrics["unique_captured_review_total"] == 3
    assert metrics["unique_captured_review_total_semantics"] == "UPPER_BOUND"
    assert metrics["overlap_occurrence_total"] == 3
    assert metrics["captured_window_overlap_rate"] == "0.500000"
    assert metrics["captured_window_overlap_rate_semantics"] == "LOWER_BOUND"
    assert any(
        "unique_captured_review_total is an upper bound" in item
        for item in first["non_claims"]
    )


def test_revolve_yotpo_context_and_same_corpus_sorts_dedupe_by_native_id(
    tmp_path: Path,
) -> None:
    selection_path = _selection_output(tmp_path)
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    job = next(
        item
        for item in selection["companion_onboarding_jobs"]
        if item["retailer"] == "target" and item["surface"] == "REVIEWS"
    )
    job["retailer"] = "revolve"
    job["source_product_id"] = "revolve-complaint-product"
    job["capture_job_id"] = _capture_job_id(
        "revolve", "revolve-complaint-product"
    )
    _write_json(selection_path, selection)
    raw_ref = _review_packet(tmp_path, "revolve")
    common = {
        "provider": "Yotpo",
        "native_id": "yotpo-review-1",
        "origin_id": None,
        "rating": 5,
        "date": "2026-07-24",
        "author": "Alex",
        "title": "Great",
        "body": "Works all day.",
        "provider_tenant_store": "revolve:b4k4hv",
        "collection_context": "REVOLVE PDP SUMR-WU76 reviews",
        "provider_evidence_refs": ["raw:yotpo-store-id"],
    }
    commission_path = tmp_path / "revolve-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "REVOLVE Yotpo bounded sort windows",
            "occurrences": [
                _occurrence(
                    "recent",
                    "revolve",
                    raw_ref,
                    actual_ordering="Most Recent",
                    **common,
                ),
                _occurrence(
                    "relevant",
                    "revolve",
                    raw_ref,
                    actual_ordering="Most Relevant",
                    ordering_fallback="historical comparison capture",
                    **common,
                ),
            ],
        },
    )

    result = build_review_linkage(
        commission=load_review_linkage_commission(commission_path),
        base_directory=tmp_path,
    )

    assert len(result["unique_review_groups"]) == 1
    assert result["unique_review_groups"][0]["occurrence_ids"] == [
        "recent",
        "relevant",
    ]
    assert result["occurrences"][0]["provider"] == "Yotpo"
    assert result["occurrences"][0]["provider_evidence_refs"] == [
        "raw:yotpo-store-id"
    ]


def test_linkage_reverifies_raw_hash_and_refuses_overwrite(tmp_path: Path) -> None:
    selection_path = _selection_output(tmp_path)
    raw_ref = _review_packet(tmp_path, "sephora")
    payload = {
        "company_id": "example-company",
        "selection_output_path": str(selection_path),
        "corpus_label": "bounded onboarding window",
        "occurrences": [
            _occurrence(
                "o1",
                "sephora",
                raw_ref,
                provider="Bazaarvoice",
                native_id="r1",
                origin_id=None,
                rating=5,
                date="2026-01-01",
                author="Alex",
                title="Great",
                body="Works all day.",
            )
        ],
        "native_review_totals": [
            _native_total("sephora", 1000, raw_ref)
        ],
    }
    bad_payload = copy.deepcopy(payload)
    bad_payload["occurrences"][0]["raw_refs"][0]["sha256"] = "0" * 64
    bad_path = tmp_path / "bad-linkage.json"
    _write_json(bad_path, bad_payload)
    with pytest.raises(RetailReviewOverlapError, match="verified packet manifest"):
        build_review_linkage(
            commission=load_review_linkage_commission(bad_path),
            base_directory=tmp_path,
        )

    commission_path = tmp_path / "linkage.json"
    output_path = tmp_path / "linkage-output.json"
    _write_json(commission_path, payload)
    write_review_linkage(
        commission_path=commission_path,
        output_path=output_path,
    )
    with pytest.raises(RetailReviewOverlapError, match="refusing overwrite"):
        write_review_linkage(
            commission_path=commission_path,
            output_path=output_path,
        )


def test_linkage_reverifies_same_file_when_slice_claim_changes(
    tmp_path: Path,
) -> None:
    selection_path = _selection_output(tmp_path)
    valid_ref = _review_packet(tmp_path, "sephora")
    invalid_ref = dict(valid_ref)
    invalid_ref["slice_id"] = "bogus-slice"
    commission_path = tmp_path / "bogus-slice-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    valid_ref,
                    provider="Bazaarvoice",
                    native_id="r1",
                    origin_id=None,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Works all day.",
                )
            ],
            "native_review_totals": [
                _native_total("sephora", 1000, invalid_ref)
            ],
        },
    )

    with pytest.raises(
        RetailReviewOverlapError,
        match="not bound to its claimed slice",
    ):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


def test_linkage_rejects_non_retail_pdp_source_family(tmp_path: Path) -> None:
    selection_path = _selection_output(tmp_path)
    raw_ref = _review_packet(
        tmp_path,
        "sephora",
        source_family="reddit",
    )
    commission_path = tmp_path / "wrong-family-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    raw_ref,
                    provider="Bazaarvoice",
                    native_id="r1",
                    origin_id=None,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Works all day.",
                )
            ],
            "native_review_totals": [],
        },
    )

    with pytest.raises(
        RetailReviewOverlapError,
        match="source_family must be retail_pdp",
    ):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


def test_linkage_refuses_to_merge_conflicting_provider_ids(tmp_path: Path) -> None:
    """A weaker fingerprint match must not override a stronger identity signal."""
    selection_path = _selection_output(tmp_path)
    raw_ref = _review_packet(tmp_path, "sephora")
    commission_path = tmp_path / "conflicting-id-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    occurrence_id,
                    "sephora",
                    raw_ref,
                    provider="Bazaarvoice",
                    native_id=native_id,
                    origin_id=origin_id,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Works all day.",
                )
                for occurrence_id, native_id, origin_id in (
                    ("o1", "sephora-1", "origin-A"),
                    ("o2", "sephora-2", "origin-B"),
                )
            ],
            "native_review_totals": [],
        },
    )

    result = build_review_linkage(
        commission=load_review_linkage_commission(commission_path),
        base_directory=tmp_path,
    )

    assert [
        item["occurrence_ids"] for item in result["unique_review_groups"]
    ] == [["o1"], ["o2"]]
    assert result["ambiguous_queue"] == [
        {
            "occurrence_ids": ["o1", "o2"],
            "candidate_basis": "NORMALIZED_EXACT_FINGERPRINT",
            "conflicting_fields": ["origin_review_id", "source_native_review_id"],
            "status": "AMBIGUOUS_NOT_MERGED",
        }
    ]
    metrics = result["metrics_by_product"][0]
    assert metrics["captured_native_occurrence_total"] == 2
    assert metrics["unique_captured_review_total"] == 2
    assert metrics["captured_window_overlap_rate"] == "0.000000"


def test_linkage_still_merges_one_syndicated_review_across_retailers(
    tmp_path: Path,
) -> None:
    """Retailer-local native ids differ for one syndicated review; still merge."""
    selection_path = _selection_output(tmp_path)
    commission_path = tmp_path / "syndicated-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    _review_packet(tmp_path, "sephora"),
                    provider="Bazaarvoice",
                    native_id="sephora-1",
                    origin_id="origin-1",
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Works all day.",
                ),
                _occurrence(
                    "o2",
                    "ulta",
                    _review_packet(tmp_path, "ulta"),
                    provider="bazaarvoice",
                    native_id="ulta-7",
                    origin_id="ORIGIN-1",
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Works all day.",
                ),
            ],
            "native_review_totals": [],
        },
    )

    result = build_review_linkage(
        commission=load_review_linkage_commission(commission_path),
        base_directory=tmp_path,
    )

    assert [
        item["occurrence_ids"] for item in result["unique_review_groups"]
    ] == [["o1", "o2"]]
    assert result["ambiguous_queue"] == []
    metrics = result["metrics_by_product"][0]
    assert (
        metrics["unique_captured_review_total_semantics"]
        == "EXACT_FOR_CAPTURED_WINDOW"
    )
    assert (
        metrics["captured_window_overlap_rate_semantics"]
        == "EXACT_FOR_CAPTURED_WINDOW"
    )


def test_linkage_rejects_a_retailer_without_a_selected_reviews_job(
    tmp_path: Path,
) -> None:
    selection_path = _qa_only_selection_output(tmp_path)
    commission_path = tmp_path / "unbound-retailer-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "ulta",
                    _review_packet(tmp_path, "ulta"),
                    provider="PowerReviews",
                    native_id="ulta-1",
                    origin_id=None,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Unbound retailer row.",
                )
            ],
            "native_review_totals": [],
        },
    )

    with pytest.raises(
        RetailReviewOverlapError,
        match="does not exactly match",
    ):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


def test_linkage_rejects_wrong_capture_job_id(tmp_path: Path) -> None:
    selection_path = _selection_output(tmp_path)
    commission_path = tmp_path / "wrong-capture-job-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    _review_packet(tmp_path, "sephora"),
                    provider="Bazaarvoice",
                    native_id="r1",
                    origin_id=None,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Wrong capture job.",
                    capture_job_id="depth_not_emitted",
                )
            ],
            "native_review_totals": [],
        },
    )
    with pytest.raises(RetailReviewOverlapError, match="does not exactly match"):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


def test_linkage_rejects_wrong_source_product_id_on_native_total(
    tmp_path: Path,
) -> None:
    selection_path = _selection_output(tmp_path)
    raw_ref = _review_packet(tmp_path, "sephora")
    correct_product_id = "sephora-complaint-product"
    commission_path = tmp_path / "wrong-source-product-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    raw_ref,
                    provider="Bazaarvoice",
                    native_id="r1",
                    origin_id=None,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Correct occurrence.",
                )
            ],
            "native_review_totals": [
                _native_total(
                    "sephora",
                    1000,
                    raw_ref,
                    capture_job_id=_capture_job_id(
                        "sephora", correct_product_id
                    ),
                    source_product_id="sephora-other-product",
                )
            ],
        },
    )
    with pytest.raises(RetailReviewOverlapError, match="does not exactly match"):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


@pytest.mark.parametrize(
    ("mutation", "match"),
    (
        ("missing", "malformed companion job binding"),
        ("duplicate", "duplicate capture_job_id"),
        ("malformed", "malformed companion job binding"),
    ),
)
def test_linkage_rejects_invalid_selection_job_bindings(
    tmp_path: Path,
    mutation: str,
    match: str,
) -> None:
    selection_path = _selection_output(tmp_path)
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    jobs = selection["companion_onboarding_jobs"]
    review_job = next(item for item in jobs if item["surface"] == "REVIEWS")
    if mutation == "missing":
        review_job.pop("capture_job_id")
    elif mutation == "duplicate":
        jobs.append(dict(review_job))
    else:
        review_job["source_product_id"] = " "
    _write_json(selection_path, selection)
    commission_path = tmp_path / f"{mutation}-job-binding-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    _review_packet(tmp_path, "sephora"),
                    provider="Bazaarvoice",
                    native_id="r1",
                    origin_id=None,
                    rating=5,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Selection binding validation.",
                )
            ],
            "native_review_totals": [],
        },
    )
    with pytest.raises(RetailReviewOverlapError, match=match):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


def test_linkage_rejects_one_raw_row_backing_two_occurrences(
    tmp_path: Path,
) -> None:
    selection_path = _selection_output(tmp_path)
    raw_ref = _review_packet(tmp_path, "sephora")
    shared = [
        _occurrence(
            occurrence_id,
            "sephora",
            raw_ref,
            provider="Bazaarvoice",
            native_id=occurrence_id,
            origin_id=None,
            rating=rating,
            date="2026-01-01",
            author="Alex",
            title="Great",
            body=body,
        )
        for occurrence_id, rating, body in (
            ("o1", 5, "First row."),
            ("o2", 4, "Second row."),
        )
    ]
    for item in shared:
        item["raw_refs"][0]["raw_row_anchor"] = "reviews[0]:sephora"
    commission_path = tmp_path / "shared-row-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": shared,
            "native_review_totals": [],
        },
    )

    with pytest.raises(
        RetailReviewOverlapError,
        match="backs more than one occurrence",
    ):
        build_review_linkage(
            commission=load_review_linkage_commission(commission_path),
            base_directory=tmp_path,
        )


@pytest.mark.parametrize(
    "rating",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
        "NaN",
        "sNaN",
        "Infinity",
        "-Infinity",
        "+Infinity",
    ),
)
def test_linkage_rejects_non_finite_ratings(
    tmp_path: Path,
    rating: object,
) -> None:
    selection_path = _selection_output(tmp_path)
    commission_path = tmp_path / "non-finite-rating-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    "o1",
                    "sephora",
                    _review_packet(tmp_path, "sephora"),
                    provider="Bazaarvoice",
                    native_id="r1",
                    origin_id=None,
                    rating=rating,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Finite ratings only.",
                )
            ],
            "native_review_totals": [],
        },
    )
    with pytest.raises(ValueError, match="rating_value must be finite"):
        load_review_linkage_commission(commission_path)


def test_numeric_and_string_ratings_normalize_deterministically(
    tmp_path: Path,
) -> None:
    selection_path = _selection_output(tmp_path)
    raw_ref = _review_packet(tmp_path, "sephora")
    commission_path = tmp_path / "finite-rating-linkage.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "selection_output_path": str(selection_path),
            "corpus_label": "bounded onboarding window",
            "occurrences": [
                _occurrence(
                    occurrence_id,
                    "sephora",
                    raw_ref,
                    provider="Bazaarvoice",
                    native_id=None,
                    origin_id=None,
                    rating=rating,
                    date="2026-01-01",
                    author="Alex",
                    title="Great",
                    body="Equivalent finite rating.",
                )
                for occurrence_id, rating in (("o1", 5), ("o2", "5.0"))
            ],
            "native_review_totals": [],
        },
    )
    result = build_review_linkage(
        commission=load_review_linkage_commission(commission_path),
        base_directory=tmp_path,
    )
    assert [
        item["occurrence_ids"] for item in result["unique_review_groups"]
    ] == [["o1", "o2"]]
    metrics = result["metrics_by_product"][0]
    assert (
        metrics["unique_captured_review_total_semantics"]
        == "EXACT_FOR_CAPTURED_WINDOW"
    )
    assert (
        metrics["captured_window_overlap_rate_semantics"]
        == "EXACT_FOR_CAPTURED_WINDOW"
    )


def test_selection_rejects_a_baseline_without_a_verified_packet_binding(
    tmp_path: Path,
) -> None:
    portfolio_path = tmp_path / "unbound-portfolio.json"
    _write_json(
        portfolio_path,
        {
            "schema_version": "retail_portfolio_onboarding_v1",
            "company_id": "example-company",
            "owned_parents": [{"owned_parent_id": "complaint-product"}],
            "listing_identities": [
                {
                    "retailer": "sephora",
                    "source_product_id": "sephora-complaint-product",
                    "exact_owned_parent_ids": ["complaint-product"],
                }
            ],
            "pdp_baselines": [
                {
                    "retailer": "sephora",
                    "source_product_id": "sephora-complaint-product",
                    "source_locator": "https://www.sephora.com/product/x",
                }
            ],
        },
    )

    with pytest.raises(
        RetailReviewOverlapError,
        match="lacks a verified packet binding",
    ):
        build_depth_selection(
            commission=load_depth_selection_commission(
                _selection_commission(tmp_path, portfolio_path)
            ),
            base_directory=tmp_path,
        )


def test_selection_rejects_a_duplicate_portfolio_listing_identity(
    tmp_path: Path,
) -> None:
    portfolio_path = tmp_path / "duplicate-portfolio.json"
    listing = {
        "retailer": "sephora",
        "source_product_id": "sephora-complaint-product",
        "exact_owned_parent_ids": ["complaint-product"],
    }
    _write_json(
        portfolio_path,
        {
            "schema_version": "retail_portfolio_onboarding_v0",
            "company_id": "example-company",
            "owned_parents": [{"owned_parent_id": "complaint-product"}],
            "listing_identities": [listing, dict(listing)],
            "pdp_baselines": [
                {
                    "retailer": "sephora",
                    "source_product_id": "sephora-complaint-product",
                    "packet_id": "sephora-baseline-packet",
                    "source_locator": "https://www.sephora.com/product/x",
                }
            ],
        },
    )

    with pytest.raises(
        RetailReviewOverlapError,
        match="duplicate listing identity",
    ):
        build_depth_selection(
            commission=load_depth_selection_commission(
                _selection_commission(tmp_path, portfolio_path)
            ),
            base_directory=tmp_path,
        )


def _selection_commission(tmp_path: Path, portfolio_path: Path) -> Path:
    commission_path = tmp_path / "malformed-selection-commission.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "portfolio_onboarding_path": str(portfolio_path),
            "candidates": [
                {
                    "owned_parent_id": "complaint-product",
                    "prominence_status": "NOT_PROMINENT",
                    "jobs": [
                        {
                            "job_id": "incident",
                            "trigger": "INCIDENT",
                            "information_job": "Resolve the incident",
                            "decision_use": "Change the incident interpretation",
                            "evidence_refs": ["event:incident"],
                            "depth_surfaces": ["REVIEWS"],
                        }
                    ],
                }
            ],
        },
    )
    return commission_path


def _qa_only_selection_output(tmp_path: Path) -> Path:
    commission_path = tmp_path / "qa-only-selection-commission.json"
    output_path = tmp_path / "qa-only-selection.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "portfolio_onboarding_path": str(_portfolio_output(tmp_path)),
            "candidates": [
                {
                    "owned_parent_id": "complaint-product",
                    "prominence_status": "NOT_PROMINENT",
                    "jobs": [
                        {
                            "job_id": "qa-only",
                            "trigger": "CONTRADICTION",
                            "information_job": "Resolve a stated contradiction",
                            "decision_use": "Change the contradiction reading",
                            "evidence_refs": ["portfolio:contradiction"],
                            "depth_surfaces": ["QA"],
                        }
                    ],
                }
            ],
        },
    )
    write_depth_selection(
        commission_path=commission_path,
        output_path=output_path,
    )
    return output_path


def _portfolio_output(
    tmp_path: Path,
    *,
    schema_version: str = "retail_portfolio_onboarding_v1",
) -> Path:
    output_path = tmp_path / "portfolio-onboarding.json"
    _write_json(
        output_path,
        {
            "schema_version": schema_version,
            "company_id": "example-company",
            "owned_parents": [
                {"owned_parent_id": "complaint-product"},
                {"owned_parent_id": "famous"},
            ],
            "listing_identities": [
                {
                    "retailer": retailer,
                    "source_product_id": f"{retailer}-complaint-product",
                    "exact_owned_parent_ids": ["complaint-product"],
                }
                for retailer in _LADDER
            ],
            "pdp_baselines": [
                {
                    "retailer": retailer,
                    "source_product_id": f"{retailer}-complaint-product",
                    "packet_id": f"{retailer}-baseline-packet",
                    "source_locator": (
                        f"https://www.{retailer}.com/product/complaint-product"
                    ),
                }
                for retailer in _LADDER
            ],
        },
    )
    return output_path


def _selection_output(tmp_path: Path) -> Path:
    commission_path = tmp_path / "fixture-selection-commission.json"
    output_path = tmp_path / "fixture-selection.json"
    _write_json(
        commission_path,
        {
            "company_id": "example-company",
            "portfolio_onboarding_path": str(_portfolio_output(tmp_path)),
            "candidates": [
                {
                    "owned_parent_id": "complaint-product",
                    "prominence_status": "NOT_PROMINENT",
                    "jobs": [
                        {
                            "job_id": "review-linkage",
                            "trigger": "COMPLAINT_CONCENTRATION",
                            "information_job": (
                                "Test whether complaint rows overlap across retailers"
                            ),
                            "decision_use": (
                                "Change the observed weak-link assessment"
                            ),
                            "evidence_refs": ["portfolio:complaint-concentration"],
                            "depth_surfaces": ["REVIEWS"],
                        }
                    ],
                }
            ],
        },
    )
    write_depth_selection(
        commission_path=commission_path,
        output_path=output_path,
    )
    return output_path


def _review_packet(
    tmp_path: Path,
    retailer: str,
    *,
    source_family: str = "retail_pdp",
) -> dict[str, str]:
    source_path = tmp_path / f"{retailer}-review-rows.json"
    _write_json(
        source_path,
        {
            "retailer": retailer,
            "reviews": [{"fixture_row": f"{retailer}-review-row"}],
        },
    )
    packet_directory = tmp_path / f"{retailer}-review-packet"
    write_local_source_capture_packet(
        output_directory=packet_directory,
        input_files=[source_path],
        source_family=source_family,
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(
            f"https://www.{retailer}.com/product/example/reviews"
        ),
        decision_question="unit test retail review overlap",
        capture_context="unit test source-backed review fixture",
    )
    packet, _ = load_verified_source_capture_packet_directory(packet_directory)
    preserved = packet.preserved_files[0]
    source_slice = next(
        item
        for item in packet.source_slices
        if preserved.file_id in item.preserved_file_ids
    )
    return {
        "packet_directory": str(packet_directory),
        "packet_id": packet.packet_id,
        "slice_id": source_slice.slice_id,
        "file_id": preserved.file_id,
        "relative_packet_path": preserved.relative_packet_path,
        "sha256": preserved.sha256,
        "hash_basis": preserved.hash_basis,
        "raw_row_anchor": f"reviews[0]:{retailer}",
    }


def _occurrence(
    occurrence_id: str,
    retailer: str,
    raw_ref: dict[str, str],
    *,
    provider: str,
    native_id: str | None,
    origin_id: str | None,
    rating: object,
    date: str,
    author: str | None,
    title: str,
    body: str,
    syndication_key: str | None = None,
    capture_job_id: str | None = None,
    source_product_id: str | None = None,
    provider_tenant_store: str | None = None,
    collection_context: str | None = None,
    provider_evidence_refs: list[str] | None = None,
    actual_ordering: str | None = None,
    ordering_fallback: str | None = None,
) -> dict[str, object]:
    row_ref = dict(raw_ref)
    # One raw review row backs at most one occurrence, so fixture anchors are
    # row-precise rather than file-level.
    row_ref["raw_row_anchor"] = f"{row_ref['raw_row_anchor']}:{occurrence_id}"
    source_product_id = source_product_id or f"{retailer}-complaint-product"
    return {
        "occurrence_id": occurrence_id,
        "owned_parent_id": "complaint-product",
        "retailer": retailer,
        "capture_job_id": (
            capture_job_id or _capture_job_id(retailer, source_product_id)
        ),
        "source_product_id": source_product_id,
        "provider": provider,
        "provider_tenant_store": (
            provider_tenant_store or f"{provider}:{retailer}-tenant"
        ),
        "collection_context": (
            collection_context or f"{retailer}:{source_product_id}:reviews"
        ),
        "provider_evidence_refs": (
            provider_evidence_refs or ["provider:" + raw_ref["packet_id"]]
        ),
        "selection_policy": (
            "SEPHORA_EXISTING_POLICY"
            if retailer == "sephora"
            else "NON_SEPHORA_MOST_RECENT"
        ),
        "actual_ordering": (
            actual_ordering
            or ("Most Helpful" if retailer == "sephora" else "Most Recent")
        ),
        "ordering_fallback": ordering_fallback,
        "source_native_review_id": native_id,
        "origin_review_id": origin_id,
        "explicit_syndication_key": syndication_key,
        "rating_value": rating,
        "review_date_source_text": date,
        "reviewer_display_label": author,
        "review_title_verbatim": title,
        "review_body_verbatim": body,
        "raw_refs": [row_ref],
    }


def _native_total(
    retailer: str,
    total: int,
    raw_ref: dict[str, str],
    *,
    capture_job_id: str | None = None,
    source_product_id: str | None = None,
) -> dict[str, object]:
    source_product_id = source_product_id or f"{retailer}-complaint-product"
    return {
        "owned_parent_id": "complaint-product",
        "retailer": retailer,
        "capture_job_id": (
            capture_job_id or _capture_job_id(retailer, source_product_id)
        ),
        "source_product_id": source_product_id,
        "native_total": total,
        "corpus_window": "retailer-visible fixture aggregate",
        "observed_at": "2026-01-01T00:00:00Z",
        "raw_refs": [dict(raw_ref)],
    }


def _capture_job_id(retailer: str, source_product_id: str) -> str:
    basis = "|".join(
        (
            "example-company",
            "complaint-product",
            "review-linkage",
            retailer,
            source_product_id,
            "REVIEWS",
        )
    )
    return "depth_" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24]


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + chr(10),
        encoding="utf-8",
    )
