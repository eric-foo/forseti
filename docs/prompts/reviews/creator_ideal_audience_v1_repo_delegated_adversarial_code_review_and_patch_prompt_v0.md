# Creator Ideal Audience v1 — Repo Delegated Adversarial Code Review and Patch Commission

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready cross-vendor commission to adversarially review the media-neutral
  creator ideal-audience Judgment implementation and apply bounded fixes inside
  the explicitly named source set.
use_when:
  - Couriering this exact implementation revision to the owner-selected external Anthropic controller.
  - Re-running the same commission only after verifying the required revision remains an ancestor and the target state is clean.
authority_boundary: retrieval_only
```

## Forseti Prompt Preflight

```yaml
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/creator_ideal_audience_v1_delegated_adversarial_code_review_v0.md
template_kind: none
edit_permission: patch-only
branch: codex/creator-ideal-audience-core
required_revision: 19263b8595a943d42d9317d99e9bce49e45a92ce
revision_mode: ancestor
dirty_state_allowance: clean at receiver bind; after work, only named patch targets plus the report may be dirty
reviews:
  posture: findings-first and coverage-first
  severity_labels: [critical, major, minor]
  formal_verdicts: [issues_found, no_material_findings, NEEDS_ARCHITECTURE_PASS]
doctrine_change: none_authorized; return NEEDS_ARCHITECTURE_PASS for design-level changes
destinations:
  input_prompt: docs/prompts/reviews/creator_ideal_audience_v1_repo_delegated_adversarial_code_review_and_patch_prompt_v0.md
  output_report: docs/review-outputs/adversarial-artifact-reviews/creator_ideal_audience_v1_delegated_adversarial_code_review_v0.md
delivery: operator_courier_only
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
authored_by_vendor: OpenAI
delegate_vendor: Anthropic
current_receiving_actor_role: controller
```

## Paste-ready commission

````markdown
You are the external controller for one REPO-MODE DELEGATED ADVERSARIAL CODE REVIEW AND BOUNDED PATCH.

Goal: determine whether the new media-neutral creator ideal-audience lane is the smallest complete fix for the prior slow, ceremony-heavy TikTok judgment path, without weakening evidence ceilings, provenance, registry compatibility, or failure visibility. Patch every real issue that can be closed inside the named source set. Done means the implementation can be safely adjudicated by the home Chief Architect with findings, exact bounded edits, real validation, and residuals visible.

WHO-CONSTRAINT — bind before source loading:
- The implementation author vendor is OpenAI.
- The owner selected an Anthropic controller for this cross-vendor discovery pass.
- If you are not Anthropic lineage, your lineage is unknown, or you cannot directly read and write the target worktree, return only `BLOCKED_DE_CORRELATION_OR_REPO_ACCESS` and stop.
- This is an observed commission constraint, not a model recommendation.

Receiver binding:
```yaml
receiver_binding:
  receiver_class: external_controller
  target_worktree: C:/tmp/forseti-creator-ideal-audience-core
  repository: https://github.com/eric-foo/orca
  branch: codex/creator-ideal-audience-core
  required_revision: 19263b8595a943d42d9317d99e9bce49e45a92ce
  revision_mode: ancestor
  expected_initial_dirty_state: clean
  direct_write_capability: receiver_to_observe
  no_concurrent_writer: receiver_to_observe
```

Before source loading, perform exactly one fresh target-state read:
1. Resolve the target worktree above, not merely your launch checkout.
2. Verify branch, HEAD, and that required revision `19263b8595a943d42d9317d99e9bce49e45a92ce` is an ancestor of HEAD.
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
- the installed `workflow-code-review` skill instructions

Review the real implementation diff at `origin/main...19263b8595a943d42d9317d99e9bce49e45a92ce`. Do not review a summary as a substitute.

Review all changed implementation surfaces. The only patchable files are:

1. `.agents/skills/creator-audience-triangulation/SKILL.md`
2. `docs/workflows/forseti_repo_map_v0.md`
3. `forseti-harness/capture_spine/creator_profile_current/audience_triangulation_snapshot.py`
4. `forseti-harness/capture_spine/creator_profile_current/materialize.py`
5. `forseti-harness/evidence_binding/instagram_audience_triangulation.py`
6. `forseti-harness/judgment/creator_audience.py`
7. `forseti-harness/runners/run_instagram_creator_audience_triangulation.py`
8. `forseti-harness/runners/run_tiktok_creator_audience_triangulation.py`
9. `forseti-harness/runners/run_tiktok_creator_onboarding_coordinator.py`
10. `forseti-harness/schemas/creator_audience_models.py`
11. `forseti-harness/tests/unit/test_creator_audience_judgment_v1.py`
12. `forseti-harness/tests/unit/test_tiktok_audience_triangulation.py`
13. `forseti/product/spines/creator_signal/README.md`
14. `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md`
15. `forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md`
16. `forseti/product/spines/creator_signal/creator_ideal_audience_calibration_examples_v0.md`
17. `forseti/product/spines/creator_signal/creator_ideal_audience_distillation_deck_v0.md`

Read-only and flag-only:
- `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json` is generated. Review its diff and gate consistency, but do not hand-edit it. If a patch changes discovered touchpoints, report that the home CA must regenerate it after adjudication.
- this commission prompt, all other repository files, generated or hash-pinned artifacts, external data roots, installed or user-level skills, Git metadata, and lifecycle state.
- The report destination is separately authorized output, not patch scope.

Attack at least these failure classes without narrowing the review to them:
- The routine prompt must contain every schema choice needed by a cold agent. The first cold probe found that allowed claim axes were omitted; the author added the schema-derived axis list and regression coverage. Try to find the next omitted semantic choice or hidden contract dependency.
- The compact prompt must materially reduce context while preserving every evidence text and decision field required by the distillation method. Detect accidental evidence loss, private path leakage, example contamination, or prompt instructions derived from evidence data.
- The deterministic compiler must own IDs, modality, support scope, source-item closure, summaries, hashes, and snapshot identity. Find any model-controlled route into durable clerical fields or any compiler inference that can overstate support.
- Engagement salience must fail closed unless every cited comment has the admitted alignment and attention capability. Check mixed citations, counterevidence, aliases, duplicates, missing claims, and platform differences.
- Instagram input must be admitted Silver from the exact data root lane. Attack path traversal, copied or renamed envelopes, legacy compatibility records, anchor mismatches, stale lineage, and arbitrary JSON acceptance.
- TikTok v0 remains readable while new writes are v1. Check registry projection, materialization, coordinator wiring, legacy response upgrade, and cross-platform identity isolation.
- The method deck and named calibration examples are split so routine judgment loads the method only. Check repo-map discoverability, compatibility pointers, contradictory authority, and accidental named-example loading.
- The lane must not estimate demographics, fuse platform accounts, imply majority prevalence, guarantee commercial outcomes, or turn engagement into truth.
- Latency and ceremony are part of correctness here. The prior AK prompt was 192,978 bytes; the new prompt was 90,071 bytes. The Jeremy Instagram prompt was 41,249 bytes. Two corrected cold-agent retries produced no output within the bounded wait and were interrupted. Determine whether that residual points to prompt ambiguity, unnecessary output burden, or only execution latency. Do not invent a cause.
- Tests must fail for meaningful contract breaks rather than merely validate fixtures that mirror implementation.

Author-observed validation before this commission:
- `python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit/test_creator_audience_judgment_v1.py forseti-harness/tests/unit/test_tiktok_audience_triangulation.py` -> 28 passed.
- creator-profile registry/materialization focused tests -> 32 passed.
- `python -m pytest -p no:cacheprovider -q forseti-harness/tests` -> exit 0.
- all 16 existing Jeremy Instagram comment/transcript Silver records passed the new source-valid lane gate.
- the first committed doc-gate run exposed missing generated touchpoint inventory entries; the author regenerated the inventory. Treat the final gate results you run as authoritative.
- cold-use residual: the corrected retries did not complete within the bounded wait, so end-to-end cold Judgment success is not claimed.

Patch rules:
- Apply only fixes supported by a finding and contained in the 17 patchable files.
- Preserve the smallest complete intervention. Do not add speculative abstractions, another registry, another maintenance surface, or unrelated cleanup.
- If the problem is design-level or needs files outside scope, return `NEEDS_ARCHITECTURE_PASS`, findings only, and quarantine any partial diff.
- Never mask a failing test, weaken a gate, fabricate success, or broaden legacy acceptance merely to obtain green output.

Validation obligations after any patch:
1. Run the focused 28-test command above.
2. Run `python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit/test_creator_profile_current_static_view.py forseti-harness/tests/unit/test_creator_profile_materialize_preflight.py forseti-harness/tests/unit/test_schema_validation.py`.
3. Run `python -m pytest -p no:cacheprovider -q forseti-harness/tests/contract/test_data_lake_inventory_gate.py`.
4. Run `pwsh -NoProfile -File .github/scripts/run-doc-gates.ps1`.
5. If any Python source changed, run `python -m pytest -p no:cacheprovider -q forseti-harness/tests`.
6. Run `git diff --check` and verify the final dirty set contains only authorized patch targets plus the report.
7. After the final report write, run `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/creator_ideal_audience_v1_delegated_adversarial_code_review_v0.md`.

Report real exit codes and outputs. If a command fails or is not run, say so directly. Do not claim PASS, readiness, approval, or closure from this commission.

Write the durable report to:
`docs/review-outputs/adversarial-artifact-reviews/creator_ideal_audience_v1_delegated_adversarial_code_review_v0.md`

The report must include, in order:
1. provenance: `reviewed_by`, `authored_by`, author vendor, delegate vendor, de-correlation bar, observed target branch and HEAD;
2. concise review summary YAML;
3. every finding, including uncertain and minor findings, with severity, confidence, target label, file:line evidence, impact, minimum closure condition, and next authorized action;
4. `considered_and_defended` for candidates that survived the attack;
5. the exact bounded unified diff of delegate-authored edits in a real multiline `diff` fence, with neutral source citations per hunk;
6. validation commands and observed results;
7. verdict and residual risk, including the cold-use latency residual;
8. adjudicator boundary: findings and edits are claims for the home Chief Architect to adjudicate; nothing is kept merely because this report recommends it.

Delegate lifecycle hard stop:
- Do not commit, push, open or update a PR, merge, stash, reset, clean the worktree, remove a worktree, run repository hygiene, or edit Git state.
- Do not patch outside the named 17-file set.
- Stop after writing and validating the report and return its path plus a compact summary to the operator.

The home Chief Architect must adjudicate findings, diff, verdict, and residuals before any change is kept. Self-closable accepted issues are closed during adjudication; design-level blockers route through `NEEDS_ARCHITECTURE_PASS`; lifecycle actions remain home-CA authority.
````

## Operator courier note

Paste the commission body into the owner-selected Anthropic controller with direct access to the target worktree. Return the full review result to the home Chief Architect for adjudication. No same-vendor, no-repo, self-review, or Codex-managed fallback satisfies this commission.
