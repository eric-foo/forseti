# Delegated Adversarial Code Review + Adjudication — Fragrance-Review Projection Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated code
  review of the fragrance-review projection seam catch-up unit (the first
  projection-family lane on the consumption seam: coverage policy constants,
  capture-date as-of resolver, catch-up runner, test suite) and the home-CA
  adjudication that closed it: one accepted test-only finding (F-FRP-001, a
  run-date coincidence that weakened the determinism test), the kept patch,
  the CA verification, and the residuals carried forward.
use_when:
  - Checking what the fragrance-review projection catch-up review found and how the F-FRP-001 keep decision was verified.
  - Citing the discharge of the independent-review gate for the commissioned four-file set.
  - Inheriting the F-FRP-001 convention (date-relative determinism tests must pin fixture dates away from the run date) in future date-sensitive lanes.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 via Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit bcc2c863c9dee55b1e60e9bbc9484f1432915308; all four
    commissioned SHA256 pins matched by reviewer; patch applied in the worktree,
    test-only, verified by the CA to touch nothing outside the [tests] target)
  dispatch: docs/prompts/reviews/fragrance_review_projection_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  reviewer_recommendation: one major test-only finding; no production defect; no NEEDS_ARCHITECTURE_PASS
  findings: 1
review_use_boundary: >
  The reviewer's findings, diff, verdict, and test claims are decision input
  for the home-CA adjudication only — not approval, not validation, not
  mandatory remediation, not executor-ready patch authority, and not
  readiness. What was kept is recorded by the adjudication below.
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, or
  acceptance. No live-lake run was performed by either party; this runner has
  never executed outside temp-lake tests.
```

## Adjudication (claim → verification → decision)

**F-FRP-001 `[tests]` (major, test-only).** Claim: the as-of determinism test
could pass if the runner regressed to a `date.today()` projection path,
because the synthetic packet's capture time is created during the same test
run — capture date, run date, and `today()` all coincide. CA verification
(not inherited): confirmed against the pre-patch test source — every date
assertion in the original test compared values that would be equal under
either the pinned-capture-date path or a today() regression. The reviewer's
patch rewrites the committed manifest's `capture_time` to a fixed non-run
date (valid: the runner's per-packet reconcile re-derives the availability
entry from the manifest, so the hash-verified manifest read still passes) and
adds a recording wrapper asserting exactly that date reaches
`project_fragrance_review_into_lake`, plus the existing evidence assertions
now pin the non-run date end to end.

**Decision: ACCEPTED unmodified**, landed as commit `10076f1b`
(test(projection): pin the as-of determinism test away from the run date).

**CA verification of the return (fresh, not inherited):** `git status` +
`git diff --stat` showed exactly one modified file (the `[tests]` target);
the other three commissioned blobs re-hashed to their commission pins
(d50f706f…, f5eeaf43…, 58a49c58…), confirming the reviewer changed nothing
else; the applied diff byte-matched the couriered diff; and the CA's own
fresh full-suite run over the patched worktree: **2691 tests, 0 failures,
0 errors, 7 skipped**, JUnit-verified (`ORCA_DATA_ROOT` cleared).

**Class sweep:** no other catch-up lane (ECR, fragrantica/basenotes/parfumo
cleaning, YT, IG) has a date-relative derivation policy, so the F-FRP-001
class has no members outside this suite. Within the suite, the sibling
byte-determinism test shares the run-date coincidence in isolation, but the
regression it could miss (a surviving today() path) is now directly caught by
the strengthened assertion; extending the pin there was considered and not
needed for closure. Convention carried forward: any future lane whose
derivation is date-relative must pin its determinism fixtures away from the
run date.

**Commissioned stakes with zero findings:** determinism completeness of the
production capture-date pin (the reviewer found no other run-date- or
environment-dependent input and no production defect making this runner's
acks untrustworthy); the envelope boundary (enumerated selection constants
vs coverage_version-covered builder internals) survived the commissioned
challenge unchanged; single-surface F-FRAG-002 instantiation; upstream
refactor safety; ack honesty; reconcile fidelity; scope discipline.

Per the delegated-review-patch overlay, this repo-mode cross-vendor discovery
pass discharges the independent-review gate for the commissioned four-file
set as patched.

## Residual disposition

- No live-lake execution evidence exists for this runner (consistent with the
  lane's rule: live-lake reads need a per-turn owner grant; none this unit).
- The envelope boundary line (builder internals ride `coverage_version` with
  comment-bound bump discipline) is unchanged — it remains a member of the
  standing comment-bound version-bump-discipline residual, queued for a
  mechanical backstop (policy-module hash ↔ version-token gate) in the
  code-vs-doctrine hardening follow-up.
- Standing lane residuals unchanged: the now-six-copy per-packet reconcile
  pattern queued for consolidation with the YT/IG follow-up; the
  operator-pointed projection path still defaults to `date.today()`
  (deliberate; catch-up path pins).

## Reviewer read-budget audit (as returned)

Full commission; overlay routing, delegated-review-patch and code-review
sources, all four target files, seam contract, consumption/root helpers,
writer/packet assembly, cleaning precedent reports, lane registry, relevant
lake/coverage tests, seam-coverage and inventory gate sources. Reviewer-run
validation: the named obligation set plus seam-coverage and inventory gates,
observed `77 passed in 22.12s`.
