# Delegated Adversarial Code Review + Adjudication — IG Reels-Grid Projection Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review of the ig-reels-grid projection seam catch-up unit and the home-CA
  adjudication that closed it: two accepted major findings (F-IGRC-001 — the
  downstream creator-metric seed's lexical tie-break could select a stale
  Bronze-catalog sibling over a newer catch-up record; F-IGRC-002 — the
  obligation omitted the runner's own surface-gate policy, so reclassified
  surfaces would leave old out-of-scope acks trusted), the kept patches, the
  CA class sweep that extended F-IGRC-002's fix to all four other
  surface-gated catch-up runners, and the residuals carried forward.
use_when:
  - Checking what the grid-projection catch-up review found and how the F-IGRC-001/002 keep decisions were verified.
  - Citing the discharge of the independent-review gate for the commissioned five-file set.
  - Inheriting the F-IGRC-001 convention (record-id policy is consumer-visible when a downstream tie-break is lexical) and the F-IGRC-002 convention (surface-gate policy is fingerprinted obligation input) in future catch-up lanes.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 via Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit 393cc21e738bb69fe3f5d1e9876ac09bdf86f78c; all five
    commissioned SHA256 pins matched by reviewer; patch applied in the
    worktree to the [runner] and [tests] targets only, verified by the CA)
  dispatch: docs/prompts/reviews/ig_reels_grid_projection_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: two major findings, bounded patch, no NEEDS_ARCHITECTURE_PASS
  findings: 2
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. No live-lake run was performed by either party.
```

## Adjudication (claim → verification → decision)

**F-IGRC-001 `[runner]` (major).** Claim: the catch-up's default ULID record
ids interact badly with the downstream creator-metric seed, whose per-username
selection breaks equal row-count/capture-time ties by LEXICALLY GREATEST
projection path — and the Bronze-catalog proof path writes stable
`bronze_catalog…` ids that sort after ULIDs (`01…`), so a stale catalog
sibling could outrank a newer catch-up re-derivation and feed the seed stale
values. CA verification (not inherited): confirmed at the source —
`_select_projection_per_username` uses `max(…, str(path))`
(`instagram_metric_seed.py:218-224`), and `"bronze_catalog…" > "01…"`
lexically. The patch gives catch-up records a `zz_`-prefixed id with a fresh
ULID suffix (sibling semantics and crash-safety unchanged) and adds a
consumer-level test that plants a stale catalog sibling and asserts the seed
selects the catch-up record. **Decision: ACCEPTED unmodified.**

**F-IGRC-002 `[runner]` (major).** Claim: the obligation envelope omitted the
runner's own surface-gate policy (family, in-scope surface, known-out-of-scope
set, record-id policy) even though that policy decides derive vs out-of-scope
ack vs visible-unsupported — so reclassifying a surface would leave prior
out-of-scope acks trusted instead of re-surfacing the packets. CA
verification: confirmed against the original envelope and the seam contract's
rule that inputs whose change alters the work must re-fingerprint. The patch
fingerprints the gate and adds a re-surface regression. **Decision: ACCEPTED
unmodified.** Both landed as commit `91a993fb`.

**CA verification of the return (fresh, not inherited):** `git status` +
`git diff --stat` showed exactly the two patchable files modified (+95/−1
matching the couriered stat); the other three commissioned blobs verified
against the pins at the pinned commit; and the CA's own fresh full-suite run
over the patched worktree (including the class sweep below): **2736 tests,
0 failures, 0 errors, 7 skipped**, JUnit-verified (`ORCA_DATA_ROOT` cleared).

**CA class sweep (landed in the same adjudication, commit `748b1b03`):**
F-IGRC-002's class has members — every other surface-gated catch-up runner
(fragrantica, basenotes, parfumo cleaning; fragrance-review projection) had
the same unfingerprinted gate. All four envelopes now carry source family +
in-scope surface(s) + known-out-of-scope set (where one exists), each with a
re-surface regression in its suite. ECR is family-agnostic (its pickups pass
no `source_family` and it has no surface gate) and is not a class member.
Landed now rather than queued because NO live acks exist for any lane yet:
the fingerprint change is free before the first live cadence run and would
orphan every ack after it. F-IGRC-001's class is contained to this lane (the
only lane with dual batch entrypoints and a lexical-tie-break consumer).

**Commissioned stakes with zero findings:** three-entrypoint record-shape
coherence beyond the tie-break (same serialization path); consumer row
parsing on catch-up records; envelope completeness of the projection policy
constants; out-of-scope surface-set completeness (writer sweep); rider
adequacy (poisoned-transport runtime tests); reconcile fidelity; scope
discipline. No NEEDS_ARCHITECTURE_PASS.

## Residual disposition

- Reviewer-stated residual (accepted): the F-IGRC-001 fix relies on the
  consumer's CURRENT lexical-path tie-breaker. If a future lane writer uses a
  lexically later prefix than `zz_…`, or the consumer's selection policy
  changes, this seam must be re-reviewed. Carried to the census record as a
  named coupling between `projection_ig_reels_grid` record-id policy and
  `instagram_metric_seed` selection policy.
- The pin-gate/`IG_REELS_PROJECTION_VERSION` boundary is unchanged; the
  envelope now also carries the runner-owned gate policy directly.
- No live-lake execution evidence exists for this runner (standing; live
  reads remain per-turn owner-granted).
- Reviewer-observed warning class (pre-existing, out of scope):
  `datetime.utcnow()` deprecation in `ig_reels_audio_packet.py:193`.

## Reviewer read-budget audit (as returned)

Full/targeted read of the prompt, pinned targets, root AGENTS, overlay
routing/review contracts, seam contract, consumption helper, projection
writer/catalog path, the real metric-seed consumer, family surface writers,
YT/IG extract runners, lane registry, fragrance/seam adjudication records;
grep sweep for IG family surfaces. Reviewer-run validation: the commissioned
set plus producer seam and inventory gates, observed `112 passed, 13 warnings
in 25.26s`; `git diff --check` clean.
