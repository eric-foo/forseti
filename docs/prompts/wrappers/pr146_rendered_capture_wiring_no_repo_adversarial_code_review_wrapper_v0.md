# PR #146 Rendered-Capture Wiring — No-Repo Adversarial Code Review Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Paste-ready wrapper for the no-repo external-controller adversarial CODE review of the multi-retailer rendered-capture wiring (PR #146).
use_when:
  - Launching the repo-blind cross-vendor advisory code review from the prepared PR #146 review-input bundle.
authority_boundary: retrieval_only
branch_or_commit: rendered-multiretailer-capture-v0 @ c1c51144467fa5ee95c4b260011f4655ac67bb27a
input_hashes:
  docs/review-inputs/pr146_rendered_capture_wiring_no_repo_adversarial_code_review_bundle_v0/README.md: 239d2497c3a2289185f326545e2c0472590ec449ecefb069e80cf8fba2bee481
  pr146_target_scope.diff: 9e2f1920135493e3791b622c1c87bbc0c443301c0bee499f8666d1576122aab5
```

````markdown
You are the external controller for an Orca no-repo delegated adversarial CODE review.

Wrapped source (read and execute it — it is self-contained):
`docs/review-inputs/pr146_rendered_capture_wiring_no_repo_adversarial_code_review_bundle_v0/README.md`
plus its attachments: `pr146_target_scope.diff` and the five `after/…` source files. The README
carries the commission, the authority excerpts the change must conform to (AGENTS kernel; the
multi-retailer spec's same-interface + Ob.17 + no-state-model/manifest rules; the commission hard
constraints; the no-runtime-acquisition import contract), the highest-value checks, the review
method, and the output contract. You need nothing else — no repo, no skills, no overlay. If you
cannot open the in-bundle files, ask for the diff + after-state files + authority excerpts to be
inlined.

Workspace: not available to you; use only the attached bundle files.

Expected target branch/revision:
`rendered-multiretailer-capture-v0 @ c1c51144` (PR #146, base main).

Output mode: chat-return-to-CA; advisory findings only.

Edit permission: read-only. Do NOT patch files. (no_repo mode: you return findings; the CA applies
accepted changes within the 5 bounded files and runs a bounded same-vendor post-patch recheck.)

Target scope: the 5 files in the bundle only (cli_support.py, the two writers
run_source_capture_cloakbrowser_packet.py / run_source_capture_http_packet.py, the cadence runner
run_source_capture_durability_series.py, and the test). `models.py`, `writer.py`, `cadence.py`,
`packet_assembly.py`, the cloakbrowser adapter, and all other sources are flag-only authority
context, not edit targets.

Preflight: confirm each attachment you use matches the SHA256 in the README (target diff
`9e2f1920…`). If a required attachment is missing or mismatched, return `BLOCKED_PREFLIGHT` with the
exact mismatch. If you cannot compute hashes, state that and proceed advisory-only only if the
content is readable.

Controller who-constraint: you satisfy the cross-vendor discovery bar only if your upstream model
vendor differs from Anthropic (the change's author ran on a Claude model). Record
`de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`. Who-constraint,
not a runtime model recommendation.

Method: if your runtime can use `workflow-code-review`, reference-load it first and say so; if not,
state `review_lane_status: workflow-code-review unavailable; advisory_no_skill_fallback` and perform
a findings-only code review from the attached diff + files. Declare `SOURCE_CONTEXT_READY` /
`SOURCE_CONTEXT_INCOMPLETE` before applying any method.

Task: adversarially review the bounded wiring change for material correctness / validation /
back-compat / INV-1 / security / review-confidence failure modes, using the README's Highest-Value
Checks — especially: (1) same-interface guarantee — does the rendered writer accept EVERY durability
flag the cadence runner forwards, and is the drift-guard test actually exhaustive (not just a
substring filter)? (2) behavior-preserving refactor — are the extracted `cli_support` helpers
byte-equivalent to the deleted local copies, so the already-merged `direct_http` writer does not
regress? (3) no state-model / schema / manifest change from `--writer` / `--writer-arg` /
`writer_extra_argv`; (4) Ob.17 placement — pins on the slice, series/cadence/postures on the packet,
never `capture_context`, honest gaps not fabricated; (5) `--writer-arg` passthrough safety — can a
verbatim-appended arg override a forwarded pin, defeat a gate, or redirect `--url`/`--output`?
(6) import safety — does importing the cloakbrowser writer's `main` at module top transitively import
`cloakbrowser`/`playwright` at load (it must not)? (7) gap ≠ no-change preserved on every rendered
failure path (dependency-unavailable, access-block, timeout, argparse reject); (8) INV-1 — no
weight/score/verdict smuggled; (9) back-compat — default `--writer` = direct_http unchanged;
non-durability rendered capture leaves Ob.17 None; (10) do the 7 tests actually prove the claims or
are any shallow / false-passable?

Return: findings-first advisory report per the README Output Contract — reviewed_by / authored_by,
de_correlation_bar, source_context_status, review_lane_status, attachment hash status, findings
(critical → major → minor) each with location, evidence (source line + conflicting authority excerpt),
impact, minimum_closure_condition, next_authorized_action, advisory remediation direction; plus
off-scope flags, residual risk, not-proven boundaries. Return `NEEDS_ARCHITECTURE_PASS` if the
problem is design-level.

Review-use boundary: your output is decision input only — not approval, validation, readiness,
mandatory remediation, executor-ready patch authority, or a no-new-seam claim. Landing PR #146 to
main stays owner-gated.
````
