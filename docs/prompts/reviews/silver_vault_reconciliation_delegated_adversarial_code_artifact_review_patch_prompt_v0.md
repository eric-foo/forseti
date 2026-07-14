# Silver/Vault Reconciliation Delegated Adversarial Code + Artifact Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (operator-couriered delegated code/artifact review-and-patch commission)
scope: >
  Repo-mode, different-family adversarial review and bounded patch of the
  Silver/Vault reconciliation diff: legacy-lineage freeze, reader census,
  policy-module pins, and authority/navigation reconciliation.
use_when:
  - Dispatching the Silver/Vault reconciliation branch to an independent reviewer before home-lane adjudication.
authority_boundary: retrieval_only
stale_if:
  - The branch no longer descends from 34e5066dbb585f9b2b48054f3397d88972aa1e8b.
  - The named target set or validation route changes before dispatch.
```

## What this is for

**Goal:** independently attack whether the reconciliation prevents new legacy
Silver grammar, finds direct derived-tree readers, binds output-shaping TikTok
policy modules, and gives a cold reader one truthful Silver/Vault model.

**Done looks like:** every material defect in the named diff is either corrected
within the bounded target set or returned with a precise closure condition; the
home/CA can adjudicate the findings and diff against cited source and real test
evidence without treating the review as automatic acceptance.

This goal and success signal are the executor target and review axis to attack,
not a pass-if-matches bar.

## Prompt preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (Silver/Vault authority + changed code/docs + targeted review/prompt doctrine)
  edit_permission: patch-only
  target_scope: the 13 labeled files under Named target set only
  dirty_state_checked: yes
  blocked_if_missing: named branch/ancestry, target diff, Silver/Vault authority, or either required review skill
repo_map_decision: loaded
repo_map_reason: the change updates the T1 Silver/Vault fast route and the review must verify that route against its owning contracts.
workspace_or_repo: C:\Users\vmon7\.codex\worktrees\f75f\orca
branch_or_commit_reference:
  branch: codex/silver-vault-reconciliation
  required_ancestry: 34e5066dbb585f9b2b48054f3397d88972aa1e8b
  semantics: advancing lane head; review origin/main...HEAD after the dispatcher pushes this prompt and implementation
dirty_state_allowance: clean target branch at receiver start; no unrelated modified or untracked files
controlling_source_state: modified only by this commissioned reconciliation diff; strict acceptance/readiness is not claimed
authorization_basis: owner-invoked fused implementation plus fused recommended-review checkpoint
doctrine_change_decision: yes - architecture terminology and currentness; DCP receipts are in the changed medallion and Cleaning-deferral sources
isolation_decision: existing solo branch off origin/main; no parallel writer is commissioned
output_mode: paste-ready-chat
input_prompt_source: this file on codex/silver-vault-reconciliation
delegate_return_destination: chat or the lane PR review/comment; no durable report required
receiver_mechanism: operator-couriered independent controller with repo access
verified_receiver_write_root: operator_to_fill; the receiver must prove it is rooted in or can write the named worktree before any patch
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
```

## Actor and lane binding

- target kind: `delegated_code_review_and_patch`, mixed code/documentation target.
- review methods: `workflow-code-review` for implementation/tests and
  `workflow-adversarial-artifact-review` for the authority/navigation documents.
  Because architecture doctrine changed, `workflow-deep-thinking` frames the
  shared boundary only after source readiness; it does not widen scope.
- mode: base controller, `access: repo`.
- author/home family: OpenAI GPT/Codex family.
- controller family: `operator_to_fill`, but it must be a different upstream
  vendor/model family from OpenAI. Unknown lineage cannot satisfy de-correlation.
- receiving actor role: controller. Do not launch a replacement reviewer.
- dispatch mode: external-controller-courier.
- patch authority: only the named target set below. Everything else is
  read-only/flag-only.
- home/CA adjudication is mandatory before any returned edit is kept.
- design-level conflict: return `NEEDS_ARCHITECTURE_PASS`, revert any partial
  edit, and return findings only.
- lifecycle hard stop: no commit, push, PR creation/update, merge, stash, reset,
  worktree cleanup, or repository-hygiene action.

## Named target set

Every finding, citation, and diff hunk must carry its label.

- `[legacy-gate]` `forseti-harness/data_lake/lane_registry.py`
- `[legacy-gate-tests]` `forseti-harness/tests/unit/test_silver_lane_registry_guard.py`
- `[reader-census]` `forseti-harness/data_lake/inventory.py`
- `[reader-census-tests]` `forseti-harness/tests/contract/test_silver_reader_selection_gate.py`
- `[policy-pins]` `forseti-harness/tests/contract/test_policy_module_version_pins.py`
- `[medallion]` `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
- `[lake-front-door]` `forseti/product/spines/data_lake/README.md`
- `[mechanics-map]` `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`
- `[cleaning-boundary]` `forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `[cleaning-deferral]` `docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md`
- `[repo-map]` `docs/workflows/forseti_repo_map_v0.md`
- `[topfrag-handoff]` `docs/workflows/topfrag_silver_lake_mechanics_handoff_v0.md`
- `[topfrag-report]` `docs/workflows/topfrag_silver_lake_mechanics_test_report_v0.md`

Why read-only review is insufficient: the commission is intended to close
confirmed bounded defects in this exact reconciliation without a second patch
round. Patch only a defect supported by cited authority; do not improve prose or
refactor code opportunistically.

## Paste-ready commission

````markdown
You are the independent controller for a repo-mode delegated adversarial CODE +
ARTIFACT REVIEW AND BOUNDED PATCH. Another lane authored the target.

Gate yourself first. The author/home model is OpenAI GPT/Codex-family. You must
be a different upstream vendor/model family; hosting platform, wrapper, or tier
does not establish de-correlation. If you are OpenAI-family or your lineage is
unknown/undisclosable, return `BLOCKED_DECORRELATION` and stop. This is a
who-constraint, not a model recommendation. Record `reviewed_by` and
`authored_by: OpenAI GPT/Codex-family` in your return; use `unrecorded` rather
than inventing a version.

PRE-FLIGHT THE REAL TARGET:

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Confirm the worktree/branch and required ancestry stated in this prompt.
   Review `origin/main...HEAD`. The target branch should be clean; if it has
   unrelated dirt, stop with `BLOCKED_DIRTY_TARGET`.
3. Confirm your actual runtime can write the named worktree before patching. A
   path printed in this prompt is not capability proof. If you can read but not
   write it, return findings without a patch and state
   `BLOCKED_RECEIVER_REROOT_REQUIRED`.
4. Read the named target files directly. Do not substitute a summary, alternate
   checkout, recreated copy, or context packet.

REFERENCE-LOAD, but do not APPLY yet:

- the targeted commissioning rules in
  `.agents/workflow-overlay/delegated-review-patch.md`;
- `workflow-deep-thinking`;
- `workflow-code-review`;
- `workflow-adversarial-artifact-review`.

Then SOURCE-LOAD the real target diff and these load-bearing sources:

- `docs/decisions/silver_vault_goal_frame_ratification_v0.md`;
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`;
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`;
- `.agents/workflow-overlay/source-of-truth.md` (DCP contract);
- `.agents/workflow-overlay/validation-gates.md` (Current Gates);
- the actual output-shaping modules newly pinned by `[policy-pins]`;
- `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py`.

Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, naming missing
sources and conflicts. Only after readiness, APPLY deep-thinking to the shared
Silver classification boundary, APPLY `workflow-code-review` to code/tests, and
APPLY `workflow-adversarial-artifact-review` to the documentation claims. If a
required review skill is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`;
do not emulate a strict result inline.

Attack these questions coverage-first:

- Does the exact legacy baseline actually fail on an added or removed
  `SILVER_LINEAGE` lane, while preserving deliberate migration visibility? Can
  a new Silver lane still bypass the official envelope silently?
- Does direct-root detection find every current `data_root.path / "derived"`
  traversal that selects or audits siblings? Identify false negatives and false
  positives in the AST rule. Is the rollup revalidator truthfully classified as
  `all_siblings`?
- Are all newly added policy pins truly output-shaping policy owners? Are any
  audited TikTok output-shaping modules still unpinned? Are every named version
  token and current LF hash correct? Do not demand a token bump merely because a
  pin is added; no pinned producer source changed in this diff.
- Do the architecture docs now state one coherent distinction: Silver Authority
  is governed source-backed entity/relationship/observation facts; Silver
  Retrieval is rebuildable read state; Projection/ECR/SCR/Cleaning audit
  artifacts are not automatically Silver? Look for contradictory current-tense
  residue, not historical receipts clearly labeled historical.
- Is the 2026-07-14 Cleaning deferral amendment supported by current writer code,
  bounded to the three source-specific writers, and complete under DCP? Does it
  accidentally authorize cross-packet dedupe, similarity, or retrieval?
- Does the repo-map T1 row earn admission as a decisive fast route, and do the
  Data Lake/Cleaning retrieval headers now make the owning contracts findable?
- Are TopFrag terminology notes historical clarification only, without rewriting
  its observed test claims?
- Can any test pass while the intended guard is broken? Require failure-visible
  negative cases, not only current-state equality.

Patch only the 13 labeled target files, and only when a finding proves the
smallest complete correction. Everything else is read-only/flag-only. A
design-level conflict returns `NEEDS_ARCHITECTURE_PASS`, no kept partial diff.
Do not commit, push, open/update a PR, merge, stash, reset, or clean a worktree.

Run these validations after any patch; report actual exit/output, `failed`,
`blocked`, or `not_run` honestly:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q --basetemp 'C:\tmp\pytest_silver_reconciliation_review' forseti-harness/tests/unit/test_silver_lane_registry_guard.py forseti-harness/tests/contract/test_silver_reader_selection_gate.py forseti-harness/tests/contract/test_policy_module_version_pins.py forseti-harness/tests/contract/test_data_lake_inventory_gate.py forseti-harness/tests/unit/test_rollup_formula_revalidation.py forseti-harness/tests/unit/test_silver_record.py
python .agents/hooks/check_silver_lane_registry.py --selftest
python .agents/hooks/check_silver_lane_registry.py --strict
python .agents/hooks/check_retrieval_header.py --changed --strict
python .agents/hooks/check_repo_map_freshness.py --changed --strict
python .agents/hooks/check_map_links.py --strict
git diff --check
```

RETURN IN THIS ORDER:

1. `reviewed_by`, `authored_by`, source readiness, target revision, and read
   disposition.
2. Findings first. Report every issue found, including minor/low-confidence
   issues. Each finding: label, severity (`critical|major|minor`), confidence
   (`high|medium|low`), `file:line`, issue, evidence, impact,
   `minimum_closure_condition`, and `next_authorized_action`.
3. `considered_and_defended`: one line per steelman-defeated candidate.
4. Unified diff for accepted bounded fixes, each hunk labeled and backed by a
   neutral, decision-sufficient citation. If none, say `no_patch`.
5. Validation results, including every not-run check.
6. Verdict relative to this commission plus residual risk. No validation,
   readiness, approval, merge, or acceptance claim.
7. Adjudicator tail: your findings, diff, citations, tests, and verdict are
   claims to adjudicate. The home/CA accepts, modifies, or rejects each change
   before anything is kept, then performs one land step only after material
   findings are closed.
````

## Dispatch and non-claims

- Paste the commission into an independent, different-family controller whose
  runtime can inspect the branch. `operator_to_fill` fields must be resolved at
  dispatch; they are not evidence of a completed preflight.
- The controller returns findings and any bounded working-tree diff only. The
  home/CA adjudicates the return.
- This prompt does not claim review completion, correctness, validation,
  readiness, acceptance, or permission to migrate historical Silver records.
