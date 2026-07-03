# Delegated Adversarial Code Review + Adjudication — IG Reels Seam Migration (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review-and-patch of the IG reels seam migration
  (runners/run_ig_reels_product_extract.py + tests) and the home-CA
  adjudication that closed it: the two findings, per-change dispositions,
  the CA closure checks, the class sweep that names the SAME two defect
  classes in the YouTube runner (flag-only, queued follow-up), and the
  pre-patch-ack residual disposition.
use_when:
  - Checking what the IG seam-migration review found and what the CA kept or rejected.
  - Scoping the queued YouTube-runner mirror follow-up (same F1/F2 classes).
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 in Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit 7c216b18abf83900c926634fbbf688de658ca439 read at
    PR #637 head; both commissioned SHA256 pins confirmed by reviewer; delegate
    applied the patch directly in the lane worktree — no commit/push, per commission)
  dispatch: docs/prompts/reviews/ig_reels_seam_migration_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: patch-level (no NEEDS_ARCHITECTURE_PASS)
  findings: 2
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. No live-lake run or live-ack verification was performed.
```

## Adjudication (per finding: claim → verification → decision)

1. **F1 — malformed/unreadable packet ASR records were silently skipped,
   allowing a `no_extractable_transcripts` ack over damaged transcript input —
   ACCEPTED.** Verified against the pre-patch source: `_asr_records` caught
   `(OSError, ValueError)` with `continue`, so a damaged `transcript_asr`
   record was invisible to BOTH the obligation snapshot and the transcript
   scan — the packet would ack as transcript-less: a fake completion fact,
   silent forever. Applied fix verified: `_asr_records` now raises on
   unreadable/invalid-JSON/non-dict records (→ `discovery_failed`, packet
   never acked, re-surfaces every run), while the new
   `_asr_record_obligation_entries` keeps the obligation snapshot CHEAP and
   NON-RAISING (an `OSError` becomes an `unreadable:<type>` marker entry) —
   load-bearing, because an exception inside `pickup`'s `obligation_fn`
   would abort the entire pickup loop, and a repair changes the fingerprint
   so the packet re-surfaces.
2. **F2 — packet obligations omitted the extractor rubric token, so a
   rubric/policy change left an old ack falsely current — ACCEPTED.** The
   seam contract's minimum obligation envelope names "the processing-policy
   tokens whose change must re-trigger work (e.g. a model or rubric
   version)". Verified: `EXTRACTOR_RUBRIC_VERSION` ("0.4") is a pre-existing
   policy constant in `cleaning/transcript_product_extractor.py` (already
   persisted per mentions record by the lake writer) — the delegate imported
   it, invented nothing. Semantics verified and test-pinned: a rubric change
   re-surfaces the packet for a RE-CHECK and re-ack under the new
   fingerprint; it does NOT re-run extraction (the deterministic mentions
   record id keys on model, not rubric — whether a rubric change should
   force re-extraction is a Cleaning-owned record-id decision, out of scope
   and named here, not smuggled in).

**Hunk dispositions:** all hunks ACCEPTED (delegate-applied in the lane
worktree; the CA verified the applied content directly against the working
tree, not the couriered summary). Nothing modified; nothing rejected.

## CA closure checks (gate discharge)

- **Byte/scope check:** `git status` shows exactly the two commissioned files
  modified (88 insertions / 15 deletions); `git diff --check` clean;
  read-only surfaces untouched.
- **Fresh test run (CA's own, not the delegate's claim):** targeted 50 passed
  / 0 failed — IG runner suite (15, incl. both new regression tests),
  operator runner, seam conformance, seam-coverage + inventory gates; full
  suite result recorded in the landing PR. Touchpoint inventory regenerated
  byte-identical.
- **Class sweep (F1's class — damaged input silently skipped on a path that
  feeds a completion fact):** ONE further member found:
  `runners/run_transcript_product_extract.py::_asr_records` has the same
  `except (OSError, ValueError): continue`, so a damaged YouTube ASR record
  can vanish into a `no_extractable_transcripts` ack the same way. Outside
  the commissioned patchable set — FLAGGED, queued as the YouTube-mirror
  follow-up unit. Non-members verified: the eval runner and SoV readout
  count unreadable records and never ack; the behavioral lake adapter is a
  read-only projection with residuals; the IG deep-capture route surfaces
  `discovery_failed` and never acks.
- **Class sweep (F2's class — policy token missing from an obligation
  envelope):** ONE further member:
  `runners/run_transcript_product_extract.py::_packet_obligation` omits
  `rubric_version`. Same follow-up unit. Consequence when mirrored: every
  previously acked YouTube packet re-surfaces once for a re-check and
  re-ack under the new fingerprint (benign, bounded churn; no
  re-extraction).
- Per the delegated-review-patch overlay, this repo-mode pass plus the
  checks above discharge the independent-review gate for the patched set.

## Residual disposition (pre-patch acks)

The reviewer's residual — pre-patch acks over damaged ASR records are
untrustworthy without retraction — is resolved by substrate state for IG:
this runner's seam code has never executed against the live lake (born and
patched in this change set; live runs are owner-gated), so the untrusted-ack
class is EMPTY for IG. For YouTube: whether any live daemon runs wrote acks
since the YT seam migration (#580) is UNKNOWN from the repo alone; if such
acks exist they carry the same F1/F2 class risk, and the seam's append-only
retraction facts are the correction mechanism. Checking is part of the
queued YouTube-mirror follow-up (live-lake read requires a fresh owner
grant).

## Reviewer read-budget audit (as returned)

Target runner/tests: full; seam contract, consumption.py, YT runner pattern,
deep-capture lake, operator runner, transcript_product_lake, AGENTS.md: read
per commission; validation: focused IG suite + commission set run with real
results; `git diff --check` clean; worktree readback confirmed two modified
files, no commit/push.
