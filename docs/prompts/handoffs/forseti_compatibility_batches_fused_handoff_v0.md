# Forseti Compatibility Batches Fused Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Fused-ready handoff for Forseti rename Step 4 runtime/tooling repair and Step 5 stale-reference audit.
use_when:
  - Invoking /fused for the remaining Forseti rename runtime/tooling and audit batches.
  - Handing a fresh implementation lane the bounded compatibility migration boundary.
  - Checking that a proposed fused lane does not run a broad path/package rename.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/decisions/forseti_compatibility_migration_boundary_v0.md
  - docs/workflows/forseti_rename_residual_inventory_v0.md
```

## Prompt Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized only when the operator explicitly invokes /fused with this handoff; otherwise docs-write/read-only
  target_scope: Forseti rename Step 4 runtime/tooling bounded repair and Step 5 classified stale-reference audit
  dirty_state_checked: yes
  blocked_if_missing: docs/decisions/forseti_compatibility_migration_boundary_v0.md
output_mode: file-write
prompt_artifact_path: docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md
template_kind: handoff
workspace: C:\Users\vmon7\Desktop\projects\orca
authoring_worktree: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-compat-scope
authoring_branch: codex/forseti-compat-scope
base_commit_observed: 351fe2ac Rename live project authority to Forseti (#646)
workflow_sequence_policy: overlay_owned
workflow_sequence_source: explicit_user_instruction
workflow_sequence_status: bound
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable
reviews: findings-first if review is commissioned; no runtime-model recommendation
doctrine_change: no new doctrine; obey docs/decisions/forseti_compatibility_migration_boundary_v0.md
```

## Receiving Prompt

You are receiving a bounded fused work unit for the Forseti rename continuation.

Do not execute this handoff unless the operator explicitly invokes `/fused` or otherwise grants bounded implementation authorization for this handoff. If invoked, perform the smallest complete Step 4/5 work under the boundary below.

## Required Reads

Read these sources before editing:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/decision-routing.md`
6. `.agents/workflow-overlay/prompt-orchestration.md`
7. `.agents/workflow-overlay/validation-gates.md`
8. `.agents/workflow-overlay/review-lanes.md`
9. `docs/decisions/forseti_rename_migration_policy_v0.md`
10. `docs/decisions/forseti_compatibility_migration_boundary_v0.md`
11. `docs/workflows/forseti_rename_residual_inventory_v0.md`
12. `docs/workflows/orca_repo_map_v0.md`
13. `repo-structure.yaml`
14. `.agents/workflow-overlay/skill-adoption.md`
15. `.github/workflows/ci.yml`
16. `.github/workflows/auto-merge.yml`

Do not bulk-load `docs/prompts/**`, `docs/review-outputs/**`, `docs/review-inputs/**`, `docs/_inbox/**`, or all product files by default. Use targeted search and classify hits.

## Source-Gated Method Contract

REFERENCE-LOAD these method instructions first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-assumption-gate`
- `fused` only if `/fused` was explicitly invoked by the operator

Use the methods only to prepare neutral source-reading questions until task sources are loaded.

After the required sources above and the target-scope searches are read, declare one of:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`, with missing sources, source gaps, excluded sources, and conflicts

Only after that declaration may you APPLY the loaded methods to classify, patch, validate, or recommend next actions.

## Objective

Complete the remaining Forseti rename batches without creating a hidden path/package migration:

1. Step 4 runtime/tooling bounded repair.
2. Step 5 final stale-reference audit.

## Hard Boundary

Preserve these compatibility identifiers unless a separate owner-accepted migration plan exists in the current turn:

- `orca/product/`
- `orca-harness/`
- `docs/workflows/orca_repo_map_v0.md`
- `orca-product-lead`
- `orca_start_preflight`
- lowercase `orca_*` filenames, package/import paths, and external identifiers
- CI/check identifiers such as `orca-harness-tests`

Do not rename directories, packages, imports, hook IDs, skill IDs, CI job/check IDs, or live route-map file paths. Do not rewrite historical prompts, review outputs, DCP receipts, migration notes, or scratch/inbox material by word match.

## Step 4 Runtime/Tooling Work

Allowed:

- Patch live human-facing runtime/tooling labels only when they imply Orca remains the current project/product name.
- Add a short compatibility note where a live runtime/tooling surface would otherwise confuse the current name with the legacy path.
- Keep exact paths, package names, working directories, CI check IDs, and skill IDs unchanged.

Candidate surfaces to inspect first:

- `orca-harness/README.md`
- `.github/workflows/ci.yml`
- `.github/workflows/auto-merge.yml`
- `.github/workflows/pr-risk-router.yml`
- `.agents/hooks/**` live messages only, not historical receipts
- `.agents/skills/orca-product-lead/SKILL.md`

Default likely outcome:

- `orca-harness/README.md` may need a title or first-paragraph compatibility note.
- CI names and working directories should probably remain unchanged.
- `orca-product-lead` should remain unchanged except for clear current-name prose defects.

## Step 5 Stale-Reference Audit

Run a classified audit for remaining content hits:

```powershell
rg -n -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml
```

Classify each remaining hit, at least by grouped surface, as one of:

- `historical_provenance`
- `explicit_legacy_alias`
- `transitional_compatibility`
- `scratch_or_inbox`
- `live_defect`

Patch `live_defect` hits only. If classification volume is too large to inspect every line in one lane, write a final audit report with grouped counts, representative examples, exact remaining defect queue, and non-claims. Do not claim all hits are clean unless you actually classified them.

## Forbidden Validation Retry

Do not run `registration_integrity.py --selftest` in this fused lane. A prior delegated review reported that command as blocked by an unrelated `tempfile.TemporaryDirectory` root cause and did not re-attempt it per commission. If a validation need appears adjacent to that checker, record it as `NOT_RUN - forbidden retry from prior stalled command` and use only bounded source inspection unless the operator separately reauthorizes a corrected command.

## Validation Gates

Run the smallest complete gates for the actual edits:

```powershell
git diff --check
python .agents/hooks/header_index.py --strict
python .agents/hooks/check_dcp_receipt.py --strict
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_handoff_pointers.py --strict
```

If code roots are touched (`orca-harness/`, `.agents/hooks/`), also satisfy review-routing disposition:

```powershell
python .agents/hooks/check_review_routing.py --strict
```

If prompt artifacts are touched, run the prompt provenance gate for each touched prompt path:

```powershell
python .agents/hooks/check_prompt_provenance.py --strict <prompt-path>
```

If runtime code/tests are changed, run the narrow relevant tests. If only README/prose is changed under a code root, explain why tests were not run and still satisfy review-routing disposition.

## Output Contract

Return a concise completion report with:

```yaml
fused_summary:
  status: completed | blocked | partial
  branch:
  base_commit:
  files_changed:
    - path:line - summary
  step_4_result:
    edited:
    preserved_compatibility_ids:
    blocked_or_deferred:
  step_5_audit:
    historical_provenance:
    explicit_legacy_alias:
    transitional_compatibility:
    scratch_or_inbox:
    live_defect:
  validation:
    - command: result and reason
  forbidden_retry:
    registration_integrity_selftest: not_run
  review_routing_status:
  next_authorized_action:
```

## Non-Claims

- This handoff is not validation, readiness, source promotion, path/package migration, or implementation execution by itself.
- Runtime implementation authority exists only if the operator invokes `/fused` or separately grants bounded implementation authorization.
- A remaining Orca hit is not a defect until classified under the rename policy and boundary decision.
