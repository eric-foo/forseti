# Step-3 Cadence Runner — No-Repo Adversarial Code Review Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Paste-ready wrapper for the no-repo external controller adversarial CODE review of the demand-durability cadence runner (PR #132).
use_when:
  - Launching the repo-blind cross-vendor advisory code review from the prepared step-3 review-input bundle.
authority_boundary: retrieval_only
branch_or_commit: demand-durability-cadence-runner-step3 @ 3cfdeeb494170d4d79783979f50d6cf7d001feed
input_hashes:
  docs/review-inputs/step3_cadence_runner_no_repo_adversarial_code_review_bundle_v0/README.md: 65a4239c1f7d19711449419f08755fabf2ea9e2ba90e997ad4338df595536073
  step3_target_scope.diff: 9089133d7ceaf30f06eb30e72b2bdcdabe9730b38389d129162121d9ef52926c
```

```text
You are the external controller for an Orca no-repo delegated adversarial CODE review.

Wrapped source (read and execute it — it is self-contained):
`docs/review-inputs/step3_cadence_runner_no_repo_adversarial_code_review_bundle_v0/README.md`
plus its attachments: `step3_target_scope.diff` and the two `after/…` source files. The README
carries the commission, the authority excerpts the change must conform to (AGENTS kernel, Ob.1
commissioning gate, Ob.17, the step-3 drift guard), the highest-value checks, the review method, and
the output contract. You need nothing else — no repo, no skills, no overlay. If you cannot open the
in-bundle files, ask for the diff + after-state files + authority excerpts to be inlined.

Workspace: not available to you; use only the attached bundle files.
Expected target: `demand-durability-cadence-runner-step3 @ 3cfdeeb` (PR #132, base main).
Output mode: chat-return-to-CA; advisory findings only. Edit permission: read-only — do NOT patch.
Target scope: the 2 bundle files only (the runner + its test); the step-2 writer, `cadence.py`,
`models.py`, and all else are flag-only authority context, not edit targets.

Preflight: confirm each attachment matches its README SHA256 (target diff `9089133d…`); on mismatch
return `BLOCKED_PREFLIGHT`. Controller who-constraint: you satisfy cross-vendor discovery only if your
upstream model vendor differs from Anthropic (the change's author ran on a Claude model) — record
`de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`. Who-constraint,
not a runtime model recommendation.

Method: if your runtime has `workflow-code-review`, reference-load it first and say so; else state
`review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback`. Declare
SOURCE_CONTEXT_READY before applying it.

Task: adversarially review the bounded change for correctness / validation / bounded-commissioned /
INV-1 / gap-handling / review-confidence failure modes, using the README's Highest-Value Checks —
especially: (1) gap ≠ no-change on BOTH paths (operator skip AND fetch failure); (2) bounded to
slot_count + Decision-Frame-tied, cannot drift into an open crawler; (3) INV-1 — no score/rank/verdict/
trend anywhere; (4) correct reuse of `cadence.build_cadence_plan` + the step-2 writer's flags, no
re-invented cadence/pin math; (5) `SystemExit`-from-writer handled as an un-observed fetch_failed gap,
not a crash or false success; (6) additive, no manifest/schema change; (7) not standing — no cron/
daemon/loop; (8) series-state integrity (init refuses overwrite; no silent overwrite); (9) failure
visibility / no false success; (10) do the 9 tests actually prove these.

Return: findings-first advisory report per the README Output Contract — reviewed_by / authored_by,
de_correlation_bar, source_context_status, review_lane_status, attachment hash status, findings
(critical → major → minor) each with location, evidence (source line + conflicting authority excerpt),
impact, minimum_closure_condition, next_authorized_action, advisory remediation; plus off-scope flags,
residual risk, not-proven boundaries. Return `NEEDS_ARCHITECTURE_PASS` if the problem is design-level.

Review-use boundary: your output is decision input only — not approval, validation, readiness, or
patch authority. Landing PR #132 to main stays owner-gated.
```
