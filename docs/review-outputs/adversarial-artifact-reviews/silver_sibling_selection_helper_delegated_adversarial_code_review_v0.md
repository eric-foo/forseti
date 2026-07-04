# Delegated Adversarial Code Review + Adjudication — Silver Sibling-Selection Helper + IG Metric Seed Migration (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review of silver/vault unit (c) — the fail-closed sibling-selection rule
  (data_lake/sibling_selection.py), the instagram_metric_seed migration off
  its F-IGRC-001 lexical tie-break, the projection lane's declared derivation
  rank, and the catch-up runner prefix single-sourcing — and the home-CA
  adjudication that closed it: one accepted finding (F-SSS-001 — the seed
  summarized each projection's capture time by raw string max, so offset-form
  ISO timestamps could enter the fail-closed selector as a wrong
  representative instant), the kept patch, the CA-strengthened regression
  test, the class sweep, and the residuals carried forward.
use_when:
  - Checking what the unit (c) selection-helper review found and how the F-SSS-001 keep decision was verified.
  - Citing the discharge of the per-unit independent-review gate for the commissioned eight-file set at commit 6713adb7.
  - Inheriting the F-SSS-001 convention (timestamps are ordered as parsed instants at EVERY layer that summarizes or selects, never as strings — including layers that only FEED a correct selector).
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-family controller (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit 6713adb7696e745c00a6e0f8c24e4f0caa9ee05c on
    branch claude/silver-selection-helper; the return states the full target
    set and controlling sources were read at the lane; per-file SHA256
    confirmation was not stated in the return and is recorded as not confirmed)
  dispatch: docs/prompts/reviews/silver_sibling_selection_helper_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: one accepted code finding, bounded 2-file patch, no NEEDS_ARCHITECTURE_PASS
  findings: 1
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

**F-SSS-001 `[seed]` (major).** Claim: `_projection_summary` summarized each
projection's capture time with raw string `max(...)`, so offset-form ISO
timestamps could be ordered incorrectly BEFORE entering the fail-closed
sibling selector — the selector's recency stage is only as honest as the
representative instant each projection feeds it. CA verification (not
inherited): confirmed at the pre-patch source (`instagram_metric_seed.py`,
`"capture_time": max(str(value) for value in capture_times)`) with a concrete
counterexample — `2026-07-02T00:15:00+03:00` (= 2026-07-01T21:15Z) sorts
lexically above `2026-07-01T23:30:00-02:00` (= 2026-07-02T01:30Z) while being
the older instant, so a projection's recency is understated and a genuinely
newer capture can lose cross-anchor selection. This is a residual member of
the exact string-ordering class the unit exists to kill, one layer above the
new rule. Patch (delegate-authored): parse each row capture time via
`parse_capture_instant`, take the max aware instant, store its isoformat; a
malformed row capture_time now raises loudly at summary time instead of being
lexically ordered as garbage (failure-visibility-consistent behavior change,
accepted). **Decision: code hunk ACCEPTED unmodified.**

**Delegate regression test — MODIFIED by the CA before keep.** The returned
test gave each fixture projection a uniform timestamp, so the
within-projection string max (the actual bug site) never disagreed with the
instant — verified non-discriminating: the pre-patch code also passes it,
because the candidate layer already parses offsets correctly. The kept test
plants mixed-offset rows WITHIN one projection (lexical row max = older
instant decoy) so a string-max summary loses selection and a parsed-instant
summary wins. Discrimination proven mechanically: with the seed module
reverted to the pre-patch commit state the kept test FAILS; on the kept state
it passes.

**CA class sweep (same adjudication):** swept production code for lexical
ordering of timestamp fields (`max(str(`, string max/min/sort on
capture/observed/captured fields): no other members. The selection layers
already parse (`sibling_selection.parse_capture_instant`,
`silver_metric_reader._parse_instant`, `sov_readout._parse_ts`). F-SSS-001's
class was contained to the seed's summary layer.

**Validation (CA's own run, kept state):** full suite via `--junitxml` with
`ORCA_DATA_ROOT` cleared: **2854 tests, 0 failures, 0 errors, 7 skipped**
(baseline 2853 + the kept regression test). Delegate-reported results
(commission set `67 passed`; full suite `2847 passed, 7 skipped`, run outside
its sandbox) are consistent and were treated as claims, not inherited.

**Commissioned stakes with zero findings:** fail-closed correctness of the
rule's input space (rank ties, missing/equal instants, cross-anchor identical-
content collapse); selection-change blast radius (new raises judged honest);
declared-rank faithfulness to the F-IGRC-001 adjudication; consumer-guard
fidelity; the pin-gate declaration-only decision; seed-document honesty;
scope discipline. No `NEEDS_ARCHITECTURE_PASS`.

## Residual disposition

- **Same-rank ambiguous catch-up siblings fail closed** (`ambiguous_sibling_derivation`):
  two distinct zz_-class re-derivations for one anchor would fail the
  materializer loudly. Adjudicated honest — a silent pick would be the
  F-IGRC-001 class again. Selecting "current policy" among same-rank siblings
  needs an explicit policy-generation ordering signal; that is unit (c)
  selection-design input for the owner, not a patch. Carried forward.
- **Committed seed JSON carries the old prose policy text** — off-scope flag,
  correctly not edited by the delegate. Already a named operator step:
  re-materialization needs an owner-granted lake read; the committed artifact
  truthfully describes the rule it was actually built with. Carried forward.
- **Malformed row capture_time now raises at summary time** — accepted
  behavior change (loud, local, names the file); recorded so a future
  operator failure is recognized as designed fail-closed behavior.

## Adjudication landing

Kept patch landed as commit `60ecb9e8` on `claude/silver-selection-helper`
(2 files, +74/−1: the seed summary fix unmodified; the regression test as
modified by the CA). Nothing else from the return required landing; no hunks
were rejected (one was modified as described).
