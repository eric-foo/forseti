# TikTok Silver Pipeline — Delegated Review Adjudication (v0)

```yaml
retrieval_header_version: 1
artifact_role: Orca review output
reviewed_by: unrecorded
authored_by: unrecorded
scope: Delegated review adjudication record for PR #622 TikTok metric-parity Silver pipeline findings.
use_when:
  - Checking how the delegated review findings for PR #622 were adjudicated and fixed.
  - Auditing the TikTok metric-parity Silver pipeline review residuals before merge consideration.
authority_boundary: retrieval_only
```

- **Subject:** PR #622 / branch `claude/tiktok-silver-pipeline` — TikTok metric-parity Silver pipeline + shared silver-envelope core.
- **Review mode:** de-correlated adversarial review, couriered by the owner to a separate reviewer session; findings returned to the commissioning (home) session for adjudication.
- **Adjudication commit:** `fix(tiktok): close 3 delegated-review findings` (this change).
- **Non-authoring note:** this is a durable record of a review that occurred and how each finding was disposed. It is not itself a validation, readiness, or acceptance claim.
- **Review-use boundary:** these findings and dispositions are decision input only; they are not approval, validation, mandatory remediation, or executor-ready patch authority unless separately accepted or authorized.

## Findings and disposition

All three findings were re-verified against the code before acceptance (confirm-don't-trust); all three **ACCEPTED** and fixed.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | CRITICAL | `source_capture/tiktok/batch_packet.py` `_normalize_stats` used `_first_int(x, y, 0)`, synthesizing a `0` for any absent stat. The preserved packet could not distinguish absent from zero, so the metric seed read a fabricated observed `0` into engagement math. (Reviewer probe: deleting `diggCount` from a real-writer grid item yielded a preserved `diggCount 0`, seed `like_count observed 0`, contaminated engagement.) | FIXED — writer preserves only source-present stats (exact integer, digit-string coerced), omits absent keys so the seed emits a loud gap, and preserves a present non-exact value raw so the seed's non-integer guard fails closed. Batch-summary sums keep their separate display-only zero-default. End-to-end regression test added through the real `write_tiktok_batch_packet`. |
| 2 | HIGH | `rollup_formula_revalidation.py` `_recompute_tiktok` checked only equal per-metric counts, not per-`content_id` grouping — validating a mixed-subset rollup (view A + like B + comment A) and not matching the producer's complete-input-only recipe. | FIXED — group source rows by `content_id`, keep only complete trios, compute averages + engagement over those (mirrors the YT branch and the producer). Mixed-subset rejection + complete-groups-only tests added. |
| 3 | HIGH | `run_tiktok_batch_metric_rollup_producer.py` `resolve_account_map` ledger-ingestion loop assigned `mapping[key]` without the conflict check the CLI loop already had; a duplicate ledger handle silently picked the later account id. | FIXED — mirror the CLI conflict check for ledger rows; idempotent duplicates still allowed. Conflict + idempotent-duplicate tests added. |

## Reviewer negative results (accepted)

- No ledger writes or handle-based account inference in the runner (identity fence holds).
- Shared silver-envelope-core extraction is behavior-preserving (constants, posture coupling, canonical JSON, content hash, error strings) — no extraction-drift finding.
- Seed-level fail-closed guards held for missing/duplicate video id, unmapped handle, empty lake, latest-packet tie, and non-integer preserved stat. (The end-to-end non-integer/missing-stat path was the gap finding #1 fixed.)
- Real 30-video packet computes `sum_views=32458300`, `sum_likes=143695`, `sum_comments=4252`, `engagement_rate≈0.004558`; the test's pinned `0.146561` is correct for its 2-row fixture.

## Pre-existing residual (out of #622 scope)

`_recompute_ig` shares finding #2's count-only weakness, but IG grid data is always complete trios, so for IG it is a tamper-hardening gap rather than a live-data bug. Flagged for a separate follow-up; deliberately not folded into #622 to keep scope bounded.

## Validation

Full lake-free unit suite (`ORCA_DATA_ROOT` unset) from `orca-harness/`: exit 0. The six new regression tests pass explicitly.
