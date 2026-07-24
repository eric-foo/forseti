"""Complete bounded Most Recent acquisition across retained REVOLVE PDPs."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Sequence

from pydantic import Field

from harness_utils import hash_file
from schemas.case_models import StrictModel
from source_capture.retail_grid_projection import (
    load_verified_source_capture_packet_directory,
)
from source_capture.retail_pdp_content import load_retail_pdp_content_record
from source_capture.revolve_pdp_content import RevolvePdpAggregateContentRecord
from source_capture.revolve_review_corpus_completion import (
    RevolveReviewCorpusReceipt,
    capture_revolve_recent_review_corpus,
    group_revolve_review_corpora,
    review_corpus_key,
)


RUN_SCHEMA_VERSION = "revolve_review_corpus_completion_run_v1"


class RevolveReviewCorpusOutcome(StrictModel):
    corpus_key: str
    source_product_ids: list[str] = Field(min_length=1)
    declared_review_count: int | None
    status: str
    receipt_path: str | None = None
    receipt_sha256: str | None = None
    captured_review_count: int = 0
    failure: str | None = None


class RevolveReviewCorpusOverlapPair(StrictModel):
    corpus_keys: list[str] = Field(min_length=2, max_length=2)
    source_product_ids: list[str] = Field(min_length=2)
    shared_native_review_ids: list[str] = Field(min_length=1)


class RevolveReviewCorpusCompletionReceipt(StrictModel):
    schema_version: str = RUN_SCHEMA_VERSION
    retailer: str = "revolve"
    provider: str = "yotpo"
    source_pdp_root: str
    requested_ordering: str = "Most Recent"
    review_limit_per_corpus: int
    requested_listing_count: int
    verified_listing_count: int
    distinct_corpus_count: int
    completed_corpus_count: int
    row_positive_corpus_count: int
    zero_row_corpus_count: int
    partial_corpus_count: int
    failed_corpus_count: int
    captured_review_occurrence_count: int
    unique_review_id_count: int
    cross_corpus_duplicate_review_ids: list[str] = Field(default_factory=list)
    corpus_overlap_pairs: list[RevolveReviewCorpusOverlapPair] = Field(
        default_factory=list
    )
    independent_corpus_family_count: int
    listing_to_corpus: dict[str, str] = Field(default_factory=dict)
    outcomes: list[RevolveReviewCorpusOutcome] = Field(default_factory=list)
    interpretation_policy: str = (
        "complete_bounded_corpus_acquisition_then_selective_category_balanced_analysis"
    )
    status: str
    residuals: list[str] = Field(default_factory=list)


def run_revolve_review_corpus_completion(
    *,
    pdp_root: Path,
    output_root: Path,
    review_limit: int = 30,
    max_workers: int = 4,
) -> tuple[int, RevolveReviewCorpusCompletionReceipt]:
    if output_root.exists():
        raise ValueError(f"output root already exists; refusing overwrite: {output_root}")
    if not pdp_root.is_dir():
        raise ValueError(f"REVOLVE PDP root is not a directory: {pdp_root}")
    if not 1 <= max_workers <= 8:
        raise ValueError("max_workers must be between 1 and 8")
    output_root.mkdir(parents=True)
    corpus_root = output_root / "corpora"

    packet_directories = sorted(
        {
            manifest.parent
            for manifest in pdp_root.glob("*/manifest.json")
            if manifest.is_file()
        },
        key=lambda path: path.name,
    )
    records: list[RevolvePdpAggregateContentRecord] = []
    load_failures: list[str] = []
    for packet_directory in packet_directories:
        try:
            records.append(_load_revolve_pdp_record(packet_directory))
        except Exception as exc:
            load_failures.append(
                "revolve_review_corpus_pdp_load_failed:"
                f"{packet_directory.name}:{type(exc).__name__}:{exc}"
            )

    groups = group_revolve_review_corpora(records)
    listing_to_corpus: dict[str, str] = {}
    for group in groups:
        substrate = group[0].review_substrate
        key = review_corpus_key(
            provider_tenant_store=str(substrate["store_id"]),
            collection_context=f"product/{substrate['product_id']}",
        )
        for record in group:
            listing_to_corpus[record.style_id] = key

    outcomes: list[RevolveReviewCorpusOutcome] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _capture_and_write,
                group=group,
                corpus_root=corpus_root,
                review_limit=review_limit,
            ): group
            for group in groups
        }
        for future in as_completed(futures):
            group = futures[future]
            substrate = group[0].review_substrate
            key = review_corpus_key(
                provider_tenant_store=str(substrate["store_id"]),
                collection_context=f"product/{substrate['product_id']}",
            )
            declared_value = substrate.get("review_count")
            declared = (
                declared_value
                if isinstance(declared_value, int)
                and not isinstance(declared_value, bool)
                else None
            )
            try:
                outcomes.append(future.result())
            except Exception as exc:
                outcomes.append(
                    RevolveReviewCorpusOutcome(
                        corpus_key=key,
                        source_product_ids=sorted(
                            {record.style_id for record in group}
                        ),
                        declared_review_count=declared,
                        status="failed",
                        failure=(
                            "revolve_review_corpus_capture_failed:"
                            f"{type(exc).__name__}:{exc}"
                        ),
                    )
                )
    outcomes.sort(key=lambda item: item.corpus_key)

    all_review_ids: list[str] = []
    review_ids_by_corpus: dict[str, set[str]] = {}
    products_by_corpus: dict[str, list[str]] = {}
    for outcome in outcomes:
        if outcome.receipt_path is None:
            continue
        payload = json.loads(Path(outcome.receipt_path).read_text(encoding="utf-8"))
        ids = {str(item) for item in payload["captured_review_ids"]}
        review_ids_by_corpus[outcome.corpus_key] = ids
        products_by_corpus[outcome.corpus_key] = outcome.source_product_ids
        all_review_ids.extend(str(item) for item in payload["captured_review_ids"])
    counts: dict[str, int] = {}
    for review_id in all_review_ids:
        counts[review_id] = counts.get(review_id, 0) + 1
    cross_corpus_duplicates = sorted(
        review_id for review_id, count in counts.items() if count > 1
    )
    overlap_pairs: list[RevolveReviewCorpusOverlapPair] = []
    corpus_keys = sorted(review_ids_by_corpus)
    parents = {key: key for key in corpus_keys}

    def find(key: str) -> str:
        while parents[key] != key:
            parents[key] = parents[parents[key]]
            key = parents[key]
        return key

    def union(left: str, right: str) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[right_root] = left_root

    for index, left in enumerate(corpus_keys):
        for right in corpus_keys[index + 1 :]:
            shared = sorted(
                review_ids_by_corpus[left] & review_ids_by_corpus[right]
            )
            if not shared:
                continue
            union(left, right)
            overlap_pairs.append(
                RevolveReviewCorpusOverlapPair(
                    corpus_keys=[left, right],
                    source_product_ids=sorted(
                        {
                            *products_by_corpus[left],
                            *products_by_corpus[right],
                        }
                    ),
                    shared_native_review_ids=shared,
                )
            )
    independent_family_count = len({find(key) for key in corpus_keys})

    failed_count = sum(item.status == "failed" for item in outcomes)
    partial_count = sum(item.status == "partial" for item in outcomes)
    residuals = [
        *load_failures,
        *[
            f"{item.corpus_key}:{item.failure}"
            for item in outcomes
            if item.failure is not None
        ],
    ]
    if len(records) != len(packet_directories):
        residuals.append(
            "revolve_review_corpus_listing_load_incomplete:"
            f"requested={len(packet_directories)}:verified={len(records)}"
        )
    status = (
        "complete"
        if not residuals and failed_count == 0 and partial_count == 0
        else "partial"
    )
    receipt = RevolveReviewCorpusCompletionReceipt(
        source_pdp_root=str(pdp_root.resolve()),
        review_limit_per_corpus=review_limit,
        requested_listing_count=len(packet_directories),
        verified_listing_count=len(records),
        distinct_corpus_count=len(groups),
        completed_corpus_count=sum(item.status == "complete" for item in outcomes),
        row_positive_corpus_count=sum(
            item.status == "complete"
            and item.declared_review_count is not None
            and item.declared_review_count > 0
            for item in outcomes
        ),
        zero_row_corpus_count=sum(
            item.status == "complete" and item.declared_review_count == 0
            for item in outcomes
        ),
        partial_corpus_count=partial_count,
        failed_corpus_count=failed_count,
        captured_review_occurrence_count=len(all_review_ids),
        unique_review_id_count=len(counts),
        cross_corpus_duplicate_review_ids=cross_corpus_duplicates,
        corpus_overlap_pairs=overlap_pairs,
        independent_corpus_family_count=independent_family_count,
        listing_to_corpus=dict(sorted(listing_to_corpus.items())),
        outcomes=outcomes,
        status=status,
        residuals=residuals,
    )
    _write_new_json(
        output_root / "completion-receipt.json",
        receipt.model_dump(mode="json"),
    )
    return (0 if status == "complete" else 4), receipt


def _capture_and_write(
    *,
    group: Sequence[RevolvePdpAggregateContentRecord],
    corpus_root: Path,
    review_limit: int,
) -> RevolveReviewCorpusOutcome:
    receipt = capture_revolve_recent_review_corpus(
        content_records=group,
        review_limit=review_limit,
    )
    receipt_path = corpus_root / f"{receipt.corpus_key}.json"
    _write_new_json(receipt_path, receipt.model_dump(mode="json"))
    return RevolveReviewCorpusOutcome(
        corpus_key=receipt.corpus_key,
        source_product_ids=receipt.source_product_ids,
        declared_review_count=receipt.declared_review_count,
        status=receipt.status,
        receipt_path=str(receipt_path.resolve()),
        receipt_sha256=hash_file(receipt_path),
        captured_review_count=len(receipt.captured_review_ids),
        failure=(
            None
            if receipt.status == "complete"
            else ";".join(receipt.residuals)
        ),
    )


def _load_revolve_pdp_record(
    packet_directory: Path,
) -> RevolvePdpAggregateContentRecord:
    packet, bodies = load_verified_source_capture_packet_directory(packet_directory)
    loaded = load_retail_pdp_content_record(
        packet=packet,
        file_bytes_by_file_id=bodies,
    )
    if loaded is None or not isinstance(loaded[1], RevolvePdpAggregateContentRecord):
        raise ValueError(
            f"packet did not retain a REVOLVE PDP content record: {packet_directory}"
        )
    return loaded[1]


def _write_new_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one bounded Most Recent onboarding window for every "
            "distinct Yotpo corpus represented by retained REVOLVE PDP packets."
        )
    )
    parser.add_argument("--pdp-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--review-limit", type=int, default=30)
    parser.add_argument("--max-workers", type=int, default=4)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        exit_code, receipt = run_revolve_review_corpus_completion(
            pdp_root=args.pdp_root,
            output_root=args.output_root,
            review_limit=args.review_limit,
            max_workers=args.max_workers,
        )
    except Exception as exc:
        print(f"revolve-review-corpus-completion: {type(exc).__name__}: {exc}")
        return 3
    print(
        "revolve-review-corpus-completion:"
        f" status={receipt.status}"
        f" listings={receipt.verified_listing_count}/{receipt.requested_listing_count}"
        f" corpora={receipt.completed_corpus_count}/{receipt.distinct_corpus_count}"
        f" occurrences={receipt.captured_review_occurrence_count}"
        f" unique_ids={receipt.unique_review_id_count}"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
