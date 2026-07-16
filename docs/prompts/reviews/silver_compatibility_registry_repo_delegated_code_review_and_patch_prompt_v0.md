# Silver Compatibility Registry — Repo Delegated Code Review and Patch Commission

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready cross-vendor commission to adversarially review the Silver
  compatibility registry implementation (stable-vs-current validation split,
  closed seven-tuple registry, byte-faithful fixtures, two-way equality gate)
  and apply bounded fixes inside the explicitly named file set.
use_when:
  - Couriering this exact implementation revision to an operator-selected non-Anthropic controller with direct repository access.
  - Re-running the same commission only after verifying the required revision remains an ancestor and the target state is clean.
authority_boundary: retrieval_only
```

## Forseti Prompt Preflight

```yaml
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/silver_compatibility_registry_delegated_code_review_v0.md
template_kind: none
edit_permission: patch-only
branch: claude/silver-compatibility-registry-f01c62
required_revision: 7d51b5a43207c16f4d72325221ab5e13f4ba0219
revision_mode: ancestor
dirty_state_allowance: clean at receiver bind; after work, only named patch targets plus the report may be dirty
reviews:
  posture: findings-first and coverage-first
  severity_labels: [critical, major, minor]
  formal_verdicts: [issues_found, no_material_findings, NEEDS_ARCHITECTURE_PASS]
doctrine_change: none_authorized; return NEEDS_ARCHITECTURE_PASS for design-level changes
destinations:
  input_prompt: docs/prompts/reviews/silver_compatibility_registry_repo_delegated_code_review_and_patch_prompt_v0.md
  output_report: docs/review-outputs/adversarial-artifact-reviews/silver_compatibility_registry_delegated_code_review_v0.md
delivery: operator_courier_only
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
authored_by_vendor: Anthropic
delegate_vendor: operator_to_fill
current_receiving_actor_role: controller
receiver_class: receiver_to_bind
preparation_state: >
  Preparation-only until the operator selects a non-Anthropic controller with
  direct repository access and fills target_worktree and delegate_vendor. Not a
  dispatch-readiness claim. Receiver source loading is blocked until the
  receiving controller completes the fresh target-state read below.
```

## Paste-ready commission

````markdown
You are the external controller for one REPO-MODE DELEGATED CODE REVIEW AND BOUNDED PATCH.

Goal: determine whether the Silver compatibility registry implementation is the smallest complete closure of the immutable-record-vs-validator-evolution trap: permanent envelope/hash validation split from current-write semantics, one closed code-owned registry keyed by (producer_id, producer_schema_version, lane_namespace) covering exactly seven persisted tuples, byte-faithful fixtures with a deterministic two-way equality gate, and fail-closed treatment of every undeclared legacy-looking form — all without weakening validation for new records. Patch every real issue that can be closed inside the named file set. Done means the home Chief Architect can adjudicate with findings, exact bounded edits, real validation, and residuals visible.

WHO-CONSTRAINT — bind before source loading:
- The implementation author vendor is Anthropic.
- The operator must select a NON-Anthropic controller (different upstream vendor lineage, not a different tier) for this cross-vendor discovery pass.
- If you are Anthropic lineage, your lineage is unknown, or you cannot directly read and write the target worktree, return only `BLOCKED_DE_CORRELATION_OR_REPO_ACCESS` and stop.
- This is an observed commission constraint, not a model recommendation.

Receiver binding:
```yaml
receiver_binding:
  receiver_class: external_controller   # bound from receiver_to_bind when the operator couriers this prompt
  target_worktree: operator_to_fill
  repository: https://github.com/eric-foo/forseti
  branch: claude/silver-compatibility-registry-f01c62
  required_revision: 7d51b5a43207c16f4d72325221ab5e13f4ba0219
  revision_mode: ancestor
  expected_initial_dirty_state: clean
  direct_write_capability: receiver_to_observe
  no_concurrent_writer: receiver_to_observe
```

Before source loading, perform exactly one fresh target-state read:
1. Resolve the target worktree above, not merely your launch checkout.
2. Verify branch, HEAD, and that required revision `7d51b5a43207c16f4d72325221ab5e13f4ba0219` is an ancestor of HEAD.
3. Verify the worktree is clean and this branch is checked out in only this worktree.
4. Prove direct write capability by creating and removing only your own harmless probe artifact inside the target worktree.
5. Verify no Git lock or concurrent writer is present.
6. Record the observed branch, HEAD, dirty set, and author/delegate vendor receipt in the report.

Required operating reads:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`: The loop, Access selection rule, De-correlation, Code-diff target kind, Delegate lifecycle hard stop, Adjudication closeout
- `.agents/workflow-overlay/review-lanes.md`: Current Lanes, Review Doctrine, Rules
- `.agents/workflow-overlay/prompt-orchestration.md`: Lane-Scoped Delegated Patch Prompt Default, Review Prompt Defaults, Prompt Validation Gates
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`: `environment_baseline`
- the installed `workflow-code-review` skill instructions if resolvable; otherwise follow the code-review lane contract in `.agents/workflow-overlay/review-lanes.md` as carried lane text

Authority context (read, not review targets):
- `docs/review-outputs/silver_vault_pr1006_postmerge_delegated_code_review_adjudication_v0.md` — the adjudication that commissioned this work; F-1 (full-shape fixtures) and F-3 (composed reader regression) are the review gaps this implementation must close.
- `docs/decisions/silver_vault_legacy_record_convergence_v0.md` — strict-writes-vs-declared-legacy-reads doctrine.

Review the real implementation diff at `e489e75ffae43fde148516b6e5d43ef78537e3f2...7d51b5a43207c16f4d72325221ab5e13f4ba0219`. Do not review a summary as a substitute.

Review all changed surfaces. The only patchable files are:

1. `forseti-harness/data_lake/silver_compatibility.py`
2. `forseti-harness/data_lake/silver_record.py`
3. `forseti-harness/tests/fixtures/silver_compatibility/creator_metric_observation_projection_v0.json`
4. `forseti-harness/tests/fixtures/silver_compatibility/creator_metric_observation_youtube_v0.json`
5. `forseti-harness/tests/fixtures/silver_compatibility/creator_metric_rollup_projection_v0.json`
6. `forseti-harness/tests/fixtures/silver_compatibility/creator_metric_rollup_youtube_v0.json`
7. `forseti-harness/tests/fixtures/silver_compatibility/fragrantica_metric_v0.json`
8. `forseti-harness/tests/fixtures/silver_compatibility/fragrantica_text_v0.json`
9. `forseti-harness/tests/fixtures/silver_compatibility/tiktok_comment_attention_v1.json`
10. `forseti-harness/tests/unit/_silver_compatibility_fixture_lake.py`
11. `forseti-harness/tests/unit/test_silver_compatibility_registry.py`
12. `forseti-harness/tests/unit/test_silver_record.py`
13. `forseti-harness/tests/unit/test_tiktok_audience_triangulation.py`
14. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

Read-only and flag-only:
- this commission prompt, all other repository files, generated or hash-pinned artifacts, installed or user-level skills, Git metadata, and lifecycle state.
- `F:\forseti-data-lake` and every external data root: do not read or write the live lake. The author-run read-only census evidence below is authorship evidence you verify for plausibility against code, not a command you re-run.
- The report destination is separately authorized output, not patch scope.

Attack at least these failure classes without narrowing the review to them:
- Registry closure soundness: can any record dodge stricter validation by claiming or losing a registry tuple? Check that unknown, contradictory, partial, or hybrid legacy-looking shapes classify invalid rather than borrowing a neighboring grammar, and that no compatibility tuple can pass `validate_silver_vault_record_for_write` or `append_silver_record`/`append_silver_record_set`.
- Stable-layer scope creep in either direction: a permanent check that actually belongs to current semantics (future tightening trap re-created), or a current-semantic check silently dropped from the write path during the refactor. Diff the pre/post acceptance sets for strict records, not just the tests.
- Classification order: original envelope and content hash must validate before tuple selection, profile semantics before physical verification, and stored records must never be mutated; verify the reordered error precedence does not change census counts or authority outcomes for well-formed records.
- Fixture byte-faithfulness: each fixture must reproduce the persisted key sets, value types, and serialization semantics of the live tuple it pins (the author verified live-lake uniformity on 2026-07-16; check the fixtures against the shapes encoded in the profile validators and producers). The TikTok v1 fixture must pin captured_at, derived_refs, and the closed 12-key observation set (PR #1006 F-1).
- Equality-gate completeness: both directions of the registry/fixture one-to-one mapping must be able to fail; mutation coverage must include every discriminating field family, not a token subset; hash-before-inference must be provable.
- TikTok v1 semantics: null-time stays historical-compatible only under the exact immutable shape; known-time stays physically current, write-retired, and excluded by the current triangulation reader with a `policy_mismatch` residual (PR #1006 F-3); the v2 sibling and every other current producer version must take the strict path with no registry entry.
- Creator-metric and Fragrantica strategy fidelity: lineage-index pass-through statuses/reasons and legacy Fragrantica raw/audit inference must behave exactly as before the refactor, including rollup content-hash reconciliation and fail-closed archive ambiguity.
- Contract-doc truthfulness: the updated contract section and DCP receipt must describe what the code actually does, and the replaced residual must not overclaim.
- Tests must fail for meaningful contract breaks rather than merely mirroring the implementation.

Author-observed validation before this commission (verify claims you can re-run; do not re-run the live census):
- focused Silver/creator-metric/TikTok/census/lane/contract suites -> 311 passed, 2 skipped.
- `python -m pytest -q` in `forseti-harness/` -> exit 0, progress [100%], no failures.
- `git diff --check` -> clean.
- official read-only Silver census against the live lake at fingerprint `07f5e0caeaf23720a9e33271d945279f72fac290382eb64e4d5b122b720b611d` -> 8518 silver_records, 8067 current_source_backed, 319 historical_compatible, 226 creator_metric_historical_compatible, 0 unclassified, 0 errors (exactly the accepted pre-change state).

Patch rules:
- Apply only fixes supported by a finding and contained in the 14 patchable files.
- Preserve the smallest complete intervention. Do not add speculative abstractions, a plugin surface, a policy DSL, another registry, or unrelated cleanup.
- If the problem is design-level or needs files outside scope, return `NEEDS_ARCHITECTURE_PASS`, findings only, and quarantine any partial diff.
- Never mask a failing test, weaken a gate, fabricate success, or broaden legacy acceptance merely to obtain green output.

Validation obligations after any patch:
1. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit/test_silver_compatibility_registry.py forseti-harness/tests/unit/test_silver_record.py forseti-harness/tests/unit/test_silver_census_behavior.py forseti-harness/tests/unit/test_tiktok_audience_triangulation.py forseti-harness/tests/unit/test_creator_metric_lineage.py`
2. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/contract/test_data_lake_inventory_gate.py forseti-harness/tests/contract/test_policy_module_version_pins.py`
3. `pwsh -NoProfile -File .github/scripts/run-doc-gates.ps1`
4. If any Python source changed, `python -m pytest -p no:cacheprovider -q forseti-harness/tests`
5. `git diff --check`; verify the final dirty set contains only authorized patch targets plus the report.
6. After the final report write, `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/silver_compatibility_registry_delegated_code_review_v0.md`

Report real exit codes and outputs. If a command fails or is not run, say so directly. Do not claim PASS, readiness, approval, or closure from this commission.

Write the durable report to:
`docs/review-outputs/adversarial-artifact-reviews/silver_compatibility_registry_delegated_code_review_v0.md`

The report must include, in order:
1. provenance: `reviewed_by`, `authored_by`, author vendor, delegate vendor, de-correlation bar, observed target branch and HEAD;
2. concise review summary YAML;
3. every finding, including uncertain and minor findings, with severity, confidence, file:line evidence, impact, minimum closure condition, and next authorized action;
4. `considered_and_defended` for candidates that survived the attack;
5. the exact bounded unified diff of delegate-authored edits in a real multiline `diff` fence, with neutral source citations per hunk;
6. validation commands and observed results;
7. verdict and residual risk;
8. adjudicator boundary: findings and edits are claims for the home Chief Architect to adjudicate; nothing is kept merely because this report recommends it.

Delegate lifecycle hard stop:
- Do not commit, push, open or update a PR, merge, stash, reset, clean the worktree, remove a worktree, run repository hygiene, or edit Git state.
- Do not patch outside the named 14-file set.
- Stop after writing and validating the report and return its path plus a compact summary to the operator.

The home Chief Architect must adjudicate findings, diff, verdict, and residuals before any change is kept, then close per `.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next Step. Self-closable accepted issues are closed during adjudication; design-level blockers route through `NEEDS_ARCHITECTURE_PASS`; lifecycle actions remain home-CA authority.
````

## Operator courier note

Paste the commission body into an operator-selected NON-Anthropic controller with direct access to a clean checkout of branch `claude/silver-compatibility-registry-f01c62`. Fill `target_worktree` and `delegate_vendor` before pasting. Return the full review result to the home Chief Architect for adjudication. No same-vendor, no-repo, self-review, or Codex-managed fallback satisfies this commission.
