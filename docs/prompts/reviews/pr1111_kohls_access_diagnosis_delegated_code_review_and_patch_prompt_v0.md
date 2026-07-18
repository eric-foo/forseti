# PR #1111 Kohl's Access Diagnosis Delegated Code Review-and-Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready cross-vendor commission to review the exact merged PR #1111
  Akamai classifier and Kohl's evidence-record diff, freeze findings before
  exposure to the prior in-session review, and apply bounded fixes.
use_when:
  - Couriering PR #1111 to an operator-selected non-OpenAI controller with direct repository access.
  - Completing the paired observation in the PR #1111 review-method comparison case.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/workflows/efficiency/pr1111_success_implement_vs_delegated_review_case_v0.md
stale_if:
  - The exact target commit is rewritten or unavailable.
  - The receiving worktree is not clean and pinned exactly to the target commit.
```

## Forseti Prompt Preflight

```yaml
output_mode: paste-ready-chat
controller_output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/pr1111_kohls_access_diagnosis_delegated_code_review_v0.md
template_kind: none
edit_permission: patch-only
target_kind: delegated_code_review_and_patch
repository: https://github.com/eric-foo/forseti
required_revision: ab276fca3bdaf2735b6240fa67f089c943526888
revision_mode: exact
expected_initial_dirty_state: clean
reviews:
  posture: findings-first and coverage-first
  code_method: workflow-code-review
  evidence_artifact_method: workflow-adversarial-artifact-review
  severity_labels: [critical, major, minor]
  formal_verdicts: [issues_found, no_material_findings, NEEDS_ARCHITECTURE_PASS]
doctrine_change: none_authorized
destinations:
  input_prompt: docs/prompts/reviews/pr1111_kohls_access_diagnosis_delegated_code_review_and_patch_prompt_v0.md
  output_report: docs/review-outputs/adversarial-artifact-reviews/pr1111_kohls_access_diagnosis_delegated_code_review_v0.md
  comparison_record: docs/workflows/efficiency/pr1111_success_implement_vs_delegated_review_case_v0.md
delivery: operator_courier_only
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
author_vendor: OpenAI
delegate_vendor: operator_to_fill
execution_route: five_phase_fast_path_if_eligible
review_diff_route: review_report_mechanics_if_durable_report_embeds_diff
current_receiving_actor_role: controller
preparation_state: >
  Preparation-only until the operator selects a non-OpenAI controller with
  direct repository access and fills target_worktree and delegate_vendor.
  This prompt does not authorize dispatch or prove receiver eligibility.
```

## Paste-ready commission

````markdown
You are the external controller for one REPO-MODE DELEGATED CODE REVIEW AND BOUNDED PATCH.

Goal: independently determine whether Forseti PR #1111 correctly and narrowly
classifies the preserved Akamai denial and records the Kohl's capture gap
without false positives, evidence overclaim, pin promotion, or cross-artifact
drift. Done means the home Chief Architect can adjudicate frozen blind findings,
their overlap with the earlier in-session review, any bounded delegate edits,
real validation, and explicit residuals.

WHO-CONSTRAINT — bind before source loading:
- The implementation author vendor is OpenAI.
- The operator must select a NON-OpenAI controller: different upstream vendor
  lineage, not another OpenAI model or tier.
- If you are OpenAI lineage, your lineage is unknown, or you cannot directly
  read and write the target worktree, return only
  `BLOCKED_DE_CORRELATION_OR_REPO_ACCESS` and stop.
- This is a commission constraint, not a runtime model recommendation.

Receiver binding:
```yaml
receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  target_worktree: operator_to_fill
  repository: https://github.com/eric-foo/forseti
  required_revision: ab276fca3bdaf2735b6240fa67f089c943526888
  revision_mode: exact
  expected_initial_dirty_state: clean
  direct_write_capability: receiver_to_observe
  no_concurrent_writer: receiver_to_observe
```

Before source loading, perform one fresh target-state read:

1. Resolve the target worktree rather than assuming the launch checkout.
2. Verify `HEAD` is exactly
   `ab276fca3bdaf2735b6240fa67f089c943526888`.
3. Verify the worktree is clean and no other worktree has this exact checkout
   as a concurrently written branch.
4. Prove direct write capability with one harmless probe artifact inside the
   worktree, then remove only that probe.
5. Verify no Git lock or concurrent writer is present.
6. Record the observed root, HEAD, dirty set, direct-write result, and
   author/delegate vendor receipt in the report.

Required operating reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`: The loop; Access
  selection rule; De-correlation; Code-diff target kind; Delegate lifecycle
  hard stop; Adjudication closeout
- `.agents/workflow-overlay/review-lanes.md`: code review and adversarial
  artifact review methods, Review Doctrine, and Rules
- `.agents/workflow-overlay/prompt-orchestration.md`: Lane-Scoped Delegated
  Patch Prompt Default, Review Prompt Defaults, and Prompt Validation Gates
- the installed `workflow-code-review` and
  `workflow-adversarial-artifact-review` skills if resolvable; otherwise use
  their project-owned lane contracts above

## Contamination control

Phase A must be completed before you read any prior-review conclusion.

- Do not read PR #1111 discussion, reviews, the merge commit body,
  `docs/workflows/efficiency/pr1111_success_implement_vs_delegated_review_case_v0.md`,
  or any chat summary of the earlier review during Phase A.
- Inspect the target with `git diff
  ab276fca3bdaf2735b6240fa67f089c943526888^
  ab276fca3bdaf2735b6240fa67f089c943526888 -- <named-targets>` or an equivalent
  diff-only command that does not display the commit body.
- Review the code and evidence artifacts, then write and freeze the Phase A
  finding list in the report before proceeding. Each candidate must have a
  stable finding ID, severity, confidence, file:line evidence, impact, minimum
  closure condition, and next authorized action.
- Record `phase_a_findings_frozen: true` plus the finding IDs. Do not silently
  add a new Phase A finding after reading the baseline; later discoveries are
  labelled `post_unblind_candidate`.

After Phase A is frozen, read
`docs/workflows/efficiency/pr1111_success_implement_vs_delegated_review_case_v0.md`.
Map every frozen finding and the recorded baseline as `overlap`,
`unique_to_delegated`, or `baseline_only`. This mapping is descriptive; the
home Chief Architect decides which findings are accepted.

## Target and review scope

Review the exact five-file diff at
`ab276fca3bdaf2735b6240fa67f089c943526888^..ab276fca3bdaf2735b6240fa67f089c943526888`.

The only patchable source files are:

1. `forseti-harness/source_capture/rendered_access.py`
2. `forseti-harness/tests/unit/test_rendered_access.py`
3. `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
4. `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
5. `forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md`

The report destination is separately authorized output, not source-patch
scope. Every other path, this prompt, the comparison record, generated or
hash-pinned artifacts, Git metadata, and lifecycle state are read-only /
flag-only.

Use `workflow-code-review` for the Python implementation and tests. After
source context is ready, use `workflow-adversarial-artifact-review` for the
three evidence artifacts. Do not merge the two methods or treat prose review as
a substitute for code review.

Read-only fitness context:

- the target file history and adjacent classifier tests needed to understand
  `classify_rendered_access`;
- `.agents/workflow-overlay/validation-gates.md` only for applicable test and
  document gates;
- the named lake packets in the three evidence artifacts, only if the
  controller can directly access `F:\forseti-data-lake`.

If the lake is unavailable, report
`EVIDENCE_SUBSTRATE_UNAVAILABLE_FOR_FRESH_READ`; do not treat absence as
evidence that the recorded packet claims are false, and do not invent or
substitute fixtures.

Attack at least these failure classes without narrowing review to them:

- Akamai classifier false positives and false negatives: title normalization,
  marker conjunction, signal placement across title / visible text / DOM, and
  collision with ordinary retailer or troubleshooting content.
- Test discrimination: whether tests fail when the required conjunction is
  weakened, split, malformed, or missing, rather than merely mirroring the
  implementation.
- Evidence admission: preserved packet-backed observations versus unpreserved
  scouting, route-liveness controls, search snippets, dollar glyphs, `.com`,
  proxy geography, and entitled feeds.
- Cross-artifact consistency across the beauty results, recon index, and pin
  registry for what is exhausted, what remains scouting, current pin status,
  and the exact next admissible experiment.
- Subject and route binding: no Kohl's, Tower 28, product, policy, country,
  currency, or access conclusion may exceed the retailer-owned bytes actually
  preserved.
- Non-claims: no demand, velocity, revenue, sell-through, market performance,
  authorization, or pin inference may leak from access diagnosis.

Patch rules:

- Apply only finding-supported fixes inside the five patchable files.
- Preserve the smallest complete intervention; do not add a retailer adapter,
  capture route, proxy machinery, schema, crawler, API, monitoring surface, or
  unrelated cleanup.
- Do not rerun live retailer captures, use a proxy, inject cookies, log in,
  interact with a cart, or mutate delivery state.
- If closure needs design changes, new evidence, or any file outside scope,
  return `NEEDS_ARCHITECTURE_PASS`, findings only, and quarantine every partial
  source diff.
- Never weaken a classifier or test merely to obtain green output.

Validation obligations after any patch:

1. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit/test_rendered_access.py`
2. `pwsh -NoProfile -File .github/scripts/run-doc-gates.ps1`
3. `git diff --check`
4. Verify the final dirty set contains only authorized patch targets plus the
   report.
5. After the final report write:
   `python .agents/hooks/check_review_output_provenance.py --strict
   docs/review-outputs/adversarial-artifact-reviews/pr1111_kohls_access_diagnosis_delegated_code_review_v0.md`

Report actual commands, exit codes, and relevant output. If a command fails or
is not run, say so. Do not claim PASS, readiness, approval, mergeability, or
closure from this commission.

Write the durable report to:
`docs/review-outputs/adversarial-artifact-reviews/pr1111_kohls_access_diagnosis_delegated_code_review_v0.md`

The report must contain, in order:

1. provenance and receiver binding;
2. a concise review summary;
3. the frozen Phase A findings and contamination-control receipt;
4. the Phase B overlap mapping;
5. every finding with severity, confidence, file:line evidence, impact,
   minimum closure condition, and next authorized action;
6. `considered_and_defended` candidates that survived attack;
7. the exact bounded unified diff of delegate-authored edits in a real
   multiline `diff` fence, with neutral source citations per hunk;
8. validation commands and observed results;
9. verdict and residual risk;
10. comparison measurements: findings total, overlap count, unique material
    candidates, patch hunks, elapsed time and token use when directly
    observable, otherwise `not_captured`;
11. the adjudicator boundary: findings, measurements, edits, verdict, and
    residuals are claims for the home Chief Architect to adjudicate.

Delegate lifecycle hard stop:

- Do not commit, stage, push, open or update a PR, merge, stash, reset, clean,
  remove a worktree, run repository hygiene, or otherwise edit Git lifecycle
  state.
- Do not patch outside the named five-file set.
- Stop after writing and validating the report, then return its path and a
  compact summary to the operator.

The home Chief Architect must adjudicate every finding, diff hunk, verdict,
residual, and comparison measurement before anything is kept or counted. It
then closes per `.agents/workflow-overlay/communication-style.md` -> Review
Adjudication Next Step.
````

## Operator courier note

Paste the commission body into an operator-selected **non-OpenAI** controller
with direct access to a clean worktree pinned exactly to
`ab276fca3bdaf2735b6240fa67f089c943526888`. Fill `target_worktree`,
`delegate_vendor`, and the observed receiver receipt before execution. Return
the complete report and working-tree diff to the home Chief Architect for
adjudication. No same-vendor, no-repo, self-review, or Codex-managed fallback
satisfies this commission.
