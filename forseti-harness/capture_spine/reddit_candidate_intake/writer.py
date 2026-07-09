from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capture_spine.reddit_candidate_intake.models import (
    CandidateSubredditRow,
    CandidateThreadUrlRow,
    OutboundUrlCandidateRow,
    RunEnvelope,
    RunProvenanceReceipt,
)
from capture_spine.reddit_candidate_intake.validation import (
    assert_no_forbidden_output_fields,
    validate_candidate_row_mapping,
    validate_old_reddit_listing_url,
    validate_old_reddit_thread_url,
    validate_run_envelope,
)


def build_candidate_intake_output(
    *,
    envelope: RunEnvelope,
    provenance: RunProvenanceReceipt,
    candidate_subreddits: list[CandidateSubredditRow] | None = None,
    candidate_threads: list[CandidateThreadUrlRow] | None = None,
    outbound_urls: list[OutboundUrlCandidateRow] | None = None,
) -> dict[str, Any]:
    validate_run_envelope(envelope)
    candidate_subreddits = candidate_subreddits or []
    candidate_threads = candidate_threads or []
    outbound_urls = outbound_urls or []

    subreddit_rows = [row.to_dict() for row in candidate_subreddits]
    thread_rows = [row.to_dict() for row in candidate_threads]
    outbound_rows = [row.to_dict() for row in outbound_urls]

    for row in subreddit_rows:
        validate_old_reddit_listing_url(row["source_url"])
        validate_candidate_row_mapping(row)
    for row in thread_rows:
        validate_old_reddit_thread_url(row["candidate_thread_url"])
        validate_candidate_row_mapping(row)
    for row in outbound_rows:
        validate_old_reddit_thread_url(row["originating_reddit_url"])
        validate_candidate_row_mapping(row)
        if row.get("requires_separate_source_family_intake") is not True:
            raise ValueError("outbound URL candidates require separate source-family intake")

    output = {
        "reddit_candidate_url_intake": {
            "envelope": envelope.to_dict(),
            "candidate_subreddits": subreddit_rows,
            "candidate_threads": thread_rows,
            "outbound_urls": outbound_rows,
            "provenance": provenance.to_dict(),
            "non_claims": list(provenance.non_claims),
        }
    }
    assert_no_forbidden_output_fields(output)
    return output


def write_candidate_intake_output(
    *,
    output: dict[str, Any],
    output_directory: Path,
    json_name: str = "reddit_candidate_url_intake.json",
    receipt_name: str = "reddit_candidate_url_intake_receipt.md",
) -> dict[str, str]:
    assert_no_forbidden_output_fields(output)
    output_directory.mkdir(parents=True, exist_ok=True)
    json_path = output_directory / json_name
    receipt_path = output_directory / receipt_name
    json_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt_path.write_text(_render_receipt(output), encoding="utf-8")
    return {"json_path": str(json_path), "receipt_path": str(receipt_path)}


def _render_receipt(output: dict[str, Any]) -> str:
    intake = output["reddit_candidate_url_intake"]
    envelope = intake["envelope"]
    provenance = intake["provenance"]
    return "\n".join(
        [
            "# Reddit Candidate URL Intake Receipt",
            "",
            f"Run ID: {envelope['run_id']}",
            f"Cap type: {envelope['cap_type']}",
            f"Coverage claim: {envelope['coverage_claim']}",
            f"Stop reason: {provenance['stop_reason']}",
            f"Candidate subreddits: {len(intake['candidate_subreddits'])}",
            f"Candidate threads: {len(intake['candidate_threads'])}",
            f"Outbound URL candidates: {len(intake['outbound_urls'])}",
            "",
            "Non-claims:",
            *[f"- {non_claim}" for non_claim in intake["non_claims"]],
            "",
        ]
    )
