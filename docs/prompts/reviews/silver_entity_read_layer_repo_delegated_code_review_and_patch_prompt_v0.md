# Silver Entity Read Layer — Repo Delegated Code Review and Patch Commission

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready cross-vendor commission to adversarially review the generated
  Silver entity read layer (gate-opened by_creator view, widened by_mention
  view with native product pages, scoped lookup runner, reader-selection
  posture declaration, consumption seam contract update) and apply bounded
  fixes inside the explicitly named file set.
use_when:
  - Couriering this exact implementation revision to an operator-selected non-Anthropic controller with direct repository access.
  - Re-running the same commission only after verifying the required revision remains an ancestor and the target state is clean.
authority_boundary: retrieval_only
```

## Forseti Prompt Preflight

```yaml
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/silver_entity_read_layer_delegated_code_review_v0.md
template_kind: none
edit_permission: patch-only
branch: claude/silver-entity-read-layer
required_revision: ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f
revision_mode: ancestor
dirty_state_allowance: clean at receiver bind; after work, only named patch targets plus the report may be dirty
reviews:
  posture: findings-first and coverage-first
  severity_labels: [critical, major, minor]
  formal_verdicts: [issues_found, no_material_findings, NEEDS_ARCHITECTURE_PASS]
doctrine_change: none_authorized; return NEEDS_ARCHITECTURE_PASS for design-level changes
destinations:
  input_prompt: docs/prompts/reviews/silver_entity_read_layer_repo_delegated_code_review_and_patch_prompt_v0.md
  output_report: docs/review-outputs/adversarial-artifact-reviews/silver_entity_read_layer_delegated_code_review_v0.md
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

Goal: determine whether the generated Silver entity read layer is a correct, smallest complete implementation of the gate-opened derived-retrieval design: a by_creator view built from one classified whole-lake sweep, a by_mention view widened with native product pages, a read-only scoped lookup runner, a declared reader-selection posture, and a truthful consumption seam contract update — all while the views stay object-level, deterministic, byte-rebuildable, and never become pickup/retrieval authority. Done means the home Chief Architect can adjudicate with findings, exact bounded edits, real validation, and residuals visible.

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
  branch: claude/silver-entity-read-layer
  required_revision: ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f
  revision_mode: ancestor
  expected_initial_dirty_state: clean
  direct_write_capability: receiver_to_observe
  no_concurrent_writer: receiver_to_observe
```

Before source loading, perform exactly one fresh target-state read:
1. Resolve the target worktree above, not merely your launch checkout.
2. Verify branch, HEAD, and that required revision `ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f` is an ancestor of HEAD.
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
- `docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md` — the ratified view definitions, gate opening, and staged SQL trigger this implementation must satisfy without widening.
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md` — rebuild-runner exclusivity, prove-rebuildability semantics (regenerate under stored stamps, byte-compare, never self-compare), write-root confinement.
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` — Generated Read Models rules, authority classification, missing-evidence-never-zero.

Review the real implementation diff at `039171df173dbeedc9ed8cba6ec183b8ecee7219...ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f`. Do not review a summary as a substitute.

Review all changed surfaces. The only patchable files are:

1. `forseti-harness/data_lake/derived_retrieval_views.py`
2. `forseti-harness/data_lake/inventory.py`
3. `forseti-harness/runners/run_derived_retrieval_lookup.py`
4. `forseti-harness/tests/test_data_lake_indexes_rebuild.py`
5. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`

Read-only and flag-only:
- this commission prompt, all other repository files, generated or hash-pinned artifacts, installed or user-level skills, Git metadata, and lifecycle state.
- `F:\forseti-data-lake` and every external data root: do not read or write the live lake, do not run the rebuild runner, the prove-rebuildability check, the census, or the lookup runner against it. The author-run live evidence below is authorship evidence you verify for plausibility against code, not a command you re-run. Test-suite runs against pytest tmp roots are allowed and expected.
- The report destination is separately authorized output, not patch scope.

Attack at least these failure classes without narrowing the review to them:
- Classification fidelity: `_classified_silver_sweep` must reuse the shared Silver authority classifier with zero reimplementation drift — no locally re-derived status logic, no lane filtering that silently drops records the census would count, and honest residuals for anything skipped. Diff its acceptance/status behavior against the classifier and census semantics, not just the tests.
- by_creator key soundness: `_account_subject_keys` must capture every persisted account-subject shape (platform_public_account subjects and public_content_object publisher keys). Hunt for missed shapes, cross-platform key collisions, and normalization that falsely merges or falsely splits creators.
- Native product pages: brand/line identity derivation from Fragrantica projection rows must not conflate distinct products or fabricate identity from partial rows; the `if entry not in entries` dedup must be order-stable and complete; `zero_rows_meaning` must state what absence actually means, never implying evidence of zero.
- Determinism and rebuildability: outputs must be byte-stable across rebuilds — check for unsorted iteration, dict-order leaks, timestamp leakage outside the generation stamp, and any way `prove_derived_retrieval_rebuildability` could pass by self-comparison or stamp reuse rather than genuine regeneration.
- Authority boundary: nothing in the changed surfaces may position the views as pickup, retrieval, or discovery authority; the rebuild path must write only under the contract-pinned derived root; the lookup runner must be strictly read-only with no fallback that touches authority state.
- Lookup runner contract: normalized matching must not produce false positives across creators/brands or false negatives on exact known identities; exit codes 0/1/2 must be honest; generation provenance and staleness must be surfaced to the caller, not swallowed.
- Reader-selection posture: the new `SILVER_READER_SELECTION_POSTURES` entry for `derived_retrieval_views.py` must grant no wider walk than the module actually performs; check the gate test still discriminates.
- Contract-doc truthfulness: the consumption seam contract update and DCP receipt must describe what the code actually does — built views, entry point, residuals — and the new residual (whole-lake classification per rebuild; SQL stays latency-gated) must not overclaim or underclaim.
- Tests must fail for meaningful contract breaks (schema-version regressions, BUILT_VIEWS closure, dropped key families, dedup regressions) rather than merely mirroring the implementation.

Author-observed validation before this commission (verify claims you can re-run in tmp roots; do not re-run anything against the live lake):
- `python -m pytest -q` in `forseti-harness/` at the required revision -> exit 0, no failures.
- `git diff --check` -> clean.
- author-run live rebuild via the contract-pinned runner -> 294.9–299.5s, writes confined to exactly six files under `indexes/derived_retrieval/silver_vault/core`.
- author-run `prove_derived_retrieval_rebuildability` -> 632.2s, all three views `rebuildable`.
- author-run read-only lookups -> creator query 0.56s returning 38 refs all current_source_backed (matches independent ground-truth scan); mention query 0.35s returning anchor plus 840 current records; live views cover 41 creators and 6 product brands.

Patch rules:
- Apply only fixes supported by a finding and contained in the 5 patchable files.
- Preserve the smallest complete intervention. Do not add speculative abstractions, an incremental cache, a SQL engine, new views, or unrelated cleanup; those are recorded triggers owned elsewhere.
- If the problem is design-level or needs files outside scope, return `NEEDS_ARCHITECTURE_PASS`, findings only, and quarantine any partial diff.
- Never mask a failing test, weaken a gate, fabricate success, or loosen the authority boundary merely to obtain green output.

Validation obligations after any patch:
1. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/test_data_lake_indexes_rebuild.py`
2. `python -m pytest -p no:cacheprovider -q forseti-harness/tests/contract/test_data_lake_inventory_gate.py forseti-harness/tests/contract/test_silver_reader_selection_gate.py forseti-harness/tests/contract/test_policy_module_version_pins.py`
3. `pwsh -NoProfile -File .github/scripts/run-doc-gates.ps1`
4. If any Python source changed, `python -m pytest -p no:cacheprovider -q forseti-harness/tests`
5. `git diff --check`; verify the final dirty set contains only authorized patch targets plus the report.
6. After the final report write, `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/silver_entity_read_layer_delegated_code_review_v0.md`

Report real exit codes and outputs. If a command fails or is not run, say so directly. Do not claim PASS, readiness, approval, or closure from this commission.

Write the durable report to:
`docs/review-outputs/adversarial-artifact-reviews/silver_entity_read_layer_delegated_code_review_v0.md`

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
- Do not patch outside the named 5-file set.
- Stop after writing and validating the report and return its path plus a compact summary to the operator.

The home Chief Architect must adjudicate findings, diff, verdict, and residuals before any change is kept, then close per `.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next Step. Self-closable accepted issues are closed during adjudication; design-level blockers route through `NEEDS_ARCHITECTURE_PASS`; lifecycle actions remain home-CA authority.
````

## Operator courier note

Paste the commission body into an operator-selected NON-Anthropic controller with direct access to a clean checkout of branch `claude/silver-entity-read-layer`. Fill `target_worktree` and `delegate_vendor` before pasting. Return the full review result to the home Chief Architect for adjudication. No same-vendor, no-repo, self-review, or Codex-managed fallback satisfies this commission.
