# Delegated Adversarial Code Review + Adjudication — SoV Extraction-Quality Eval (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review-and-patch of the SoV extraction-quality eval
  (runners/run_sov_extraction_quality_eval.py + tests) and the home-CA
  adjudication that closed it: the three findings, per-change dispositions,
  the CA closure checks, and the adjudicated live-lake rerun that CONFIRMED
  the published baseline numbers under strict ref checking.
use_when:
  - Checking what the eval-runner review found and what the CA kept or rejected.
  - Verifying whether the published eval baseline survived the F1 mismatch class.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit 2822d2c11ae98aeb5e399f9f379643d2b9a2ee87 read;
    both commissioned SHA256 pins confirmed by reviewer; delegate reviewed from a
    pinned temp checkout and returned the diff in chat — the CA applied it)
  dispatch: docs/prompts/reviews/sov_extraction_quality_eval_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: patch-level (no NEEDS_ARCHITECTURE_PASS)
  findings: 1 high + 2 medium
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. Extractor recall/precision remain unmeasured (ground-truth unit
  deferred).
```

## Adjudication (per finding: claim → verification → decision)

1. **F1 (high) — suffix fallback could scan the WRONG transcript — ACCEPTED.**
   Verified: the caption writer records exact `file_id`/`relative_packet_path`/
   `sha256` per raw ref (`run_transcript_product_extract.py`), and
   `SilverRawRef` requires the hash whenever `file_id` is set — so exact-ref
   matching costs nothing on conforming records, while the removed fallback
   (first `.json3` in the packet) could have produced a false present/leak
   verdict from a stale or mismatched ref. Applied: exact file_id + path +
   sha256 match required; mismatches are counted dispositions
   (`invalid_raw_transcript_ref`, `raw_transcript_ref_mismatch`,
   `raw_transcript_ref_hash_mismatch`), never substitute scans.
2. **F2 (medium) — `per_brand` read like an all-mentions breakdown but only
   tallied scanned ones — ACCEPTED.** Applied: per-brand tally is now
   `{mentions, scanned, leaked, unscannable}`; `eval_schema_version` bumped
   to 2.
3. **F3 (medium) — gate-excluded mention entries and no-named-mention records
   lacked explicit dispositions — ACCEPTED.** Applied:
   `substrate.mentions_excluded_not_source_backed` and the
   `not_attempted_no_named_mentions` transcript disposition.

**Hunk dispositions:** all hunks ACCEPTED (applied by the CA as its own edits,
wording-aligned; the couriered diff was abridged, so equivalence was
established per change, not byte-blind). Nothing modified; nothing rejected.

## Baseline disposition (the reviewer's residual, resolved)

The reviewer flagged the published baseline as not adjudication-safe until
rerun against the F1 mismatch class. **Adjudicated rerun executed** (same day,
read-only, schema v2): all 23 previously-resolved records resolve identically
under exact-ref discipline — 0 mismatches — and every headline number is
CONFIRMED (leak rate 8.8% upper bound, 93/102 present, unknown-brand 16.4%).
The report (`docs/workflows/sov_extraction_quality_eval_report_v0.md`) carries
the rerun provenance inline.

## CA closure checks (gate discharge)

- **Byte/scope check:** changes confined to the two commissioned files
  (runner + tests); read-only surfaces (report doc, inventory, seam counter)
  untouched by the patch.
- **Fresh test run:** 37 passed — eval suite (6, incl. the two new regression
  tests), seam-coverage (16), inventory gate (15); full suite result recorded
  in the landing PR.
- **Class sweep (F1's class — unverified substitute-source fallback):** the
  removed fallback was the only member in the eval; `sov_readout.py` reads only
  the anchor's own manifest (no substitution); `by_mention` resolves no
  transcripts. No further members.
- **Class sweep (F2's class — partial tallies under total-sounding names):**
  eval fields now name their denominators (`scanned` vs `mentions` vs
  `unscannable`); no other eval field claims a broader denominator than it
  computes.
- Per the delegated-review-patch overlay, this repo-mode pass plus the checks
  above discharge the independent-review gate for the patched set.

## Reviewer read-budget audit (as returned)

Target runner/tests, AGENTS.md, silver_lineage, transcript_product_lake,
sov_readout, extract runner, report doc, both gate tests: full; root.py:
targeted (load_raw_packet, by-key semantics); overlay README, decision-routing,
delegated-review-patch: read.
