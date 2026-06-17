# Commission Signal Board Spine Pilot Reconciliation Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Handoff prompt (docs-write commission to the Commission Signal Board lane)
scope: >
  Commission the Commission Signal Board lane to reconcile stale "commission
  gate" language into Commission Signal Board doctrine, then deep-think and plan
  the spine-first pull-out of related documents into a Commission Signal Board
  pilot spine.
use_when:
  - Dispatching a fresh Commission Signal Board lane to clean up gate-shaped stale language.
  - Planning the Commission Signal Board pilot migration toward a whole-spine workspace.
  - Asking a downstream lane to inventory related subsidiary documents and decide what belongs inside the new spine.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
  - docs/workflows/commission_signal_board_playbook_v0.md
  - docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md
  - docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - Commission Signal Board artifacts are moved or renamed.
  - A later prompt supersedes the Commission Signal Board pilot migration route.
```

## Orca Start Preflight For This Prompt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (S0 overlay prompt mechanics + repo map + Commission Signal Board playbook/prompt/adjudication packet + spine-first proposal)
  repo_map_decision: loaded
  repo_map_reason: Commission Signal Board and structure proposal routing are repo-map discoverability concerns.
  preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated here.
  workspace_path: C:/Users/vmon7/Desktop/projects/orca
  authoring_worktree: C:/Users/vmon7/Desktop/projects/orca/.codex/worktrees/commission-spine-structure
  authoring_branch: codex/commission-spine-structure
  intended_receiving_base: branch containing PR #239 / this prompt, or a successor after it lands
  dirty_state_allowance: receiving lane must start from a fresh worktree and report dirty state before edits
  controlling_source_state: checked during prompt authoring; receiving lane must re-check fresh
  target_scope: docs-write prompt artifact; downstream docs-write reconciliation and migration planning
  edit_permission: docs-write for the receiving lane; implementation/runtime work not authorized
  output_mode: file-write
  doctrine_change_decision: >
    Prompt authoring is not itself the structure change. The commissioned work
    may change product doctrine, architecture doctrine, workflow authority, and
    output authority if it edits binding surfaces or creates the pilot spine; it
    must carry a direction_change_propagation receipt or blocker.
  blocked_if_missing: >
    Block before live spine moves if the receiving lane cannot load the
    spine-first proposal or cannot bind authority for a new top-level `orca/`
    product workspace.
```

## Fitness Reference

**Goal:** make the commission lane correctly read as **Commission Signal Board**
rather than "commission gate", and prepare the lowest-risk pilot for a
whole-spine workspace.

**Done looks like:** active Commission Signal Board artifacts no longer route
future agents through gate-shaped stale language; related documents are
inventoried and classified; the lane has a source-backed plan for pulling the
right documents into a Commission Signal Board spine without breaking the
current repo binding.

## Commission

You are the **Commission Signal Board lane CA**. Your job is to reconcile the
current commission lane into the correct product object and prepare the first
spine-first pilot.

The important correction: this is **not a Commission Gate**. The durable object
is **Commission Signal Board** - an evidence and signal organization surface
that sits upstream of capture/retrieval, demand classification, forecasting,
weighting, and judgment. It does not admit, reject, score, forecast, judge,
prove demand, construct a graph, or make buyer-proof claims.

The branch/worktree name `commission-gate` may remain a factual legacy branch
name. Do not pretend branch names were different. Do correct active doctrine,
prompt, workflow, and map language when it semantically treats the board as a
gate.

## Source-Gated Method Contract

REFERENCE-LOAD these methods first:

- `workflow-deep-thinking`
- `workflow-assumption-gate`

Do not APPLY them yet. Use them only to prepare a neutral source-reading lens.

Then SOURCE-LOAD the required sources below. Declare one of:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

Only after source context is ready may you APPLY:

- `workflow-deep-thinking` to decide the right scope and option set for the
  reconciliation and spine pull-out.
- `workflow-assumption-gate` before any physical move, binding edit, or claim
  that the Commission Signal Board spine is ready to create.

## Required Reads

Read these before source-backed decisions:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/decision-routing.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/source-of-truth.md`
6. `.agents/workflow-overlay/artifact-folders.md`
7. `.agents/workflow-overlay/prompt-orchestration.md`
8. `repo-structure.yaml`
9. `docs/decisions/orca_repo_structure_binding_v0.md`
10. `docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md`
11. `docs/workflows/orca_repo_map_v0.md`
12. `docs/workflows/commission_signal_board_playbook_v0.md`
13. `docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md`
14. `docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md`
15. `.agents/hooks/check_commission_signal_board_output.py`
16. `orca-harness/tests/unit/test_commission_signal_board_output_validator.py`
17. `orca-harness/tests/fixtures/commission_signal_board_outputs/`

Targeted searches you must run before edits:

```powershell
rg -n "commission gate|commission-gate|Commission Gate|gate" docs .agents orca-harness repo-structure.yaml
rg -n "Commission Signal Board|commission_signal_board|signal board" docs .agents orca-harness repo-structure.yaml
rg --files | rg "commission_signal_board|commission-gate|commission_gate|signal_board"
```

Treat "commission" as a generic English word in many prompts and reviews. Do not
bulk-replace generic "commission" language that is unrelated to this lane.

## Subagent Use

Spawn subagents when they reduce risk or parallelize non-blocking inventory.
Keep them read-only unless you explicitly split disjoint write scopes.

Recommended subagent fanout:

1. **Naming inventory explorer** - find stale "commission gate" / gate-shaped
   language and classify each hit as `must_change`, `must_preserve_factual`,
   `historical_do_not_touch`, or `unrelated`.
2. **Artifact inventory explorer** - list every Commission Signal Board artifact,
   its role, current path, and proposed spine target.
3. **Binding impact explorer** - identify exactly which binding surfaces must
   change before `orca/product/spines/commission_signal_board/` can become live.

Subagent return shape must be terse and schema-bound:

```yaml
subagent_return:
  source_context: ready | incomplete
  verdict:
  file_line_cites:
    - path:line - claim
  must_change:
  must_preserve:
  unknowns:
  blocker:
```

Reject or re-prompt any subagent result that gives prose without file/line
cites for load-bearing claims.

## Deliverables

### D1 - Start-State Receipt

Create a compact start-state section in your output:

- worktree path;
- branch and HEAD;
- base branch;
- dirty/untracked state;
- whether PR #239 / the spine-first proposal is present;
- whether the target branch is `codex/commission-gate`,
  `codex/commission-spine-structure`, or a successor;
- source context status.

If the spine-first proposal is absent, block live spine work and either:

- ask to rebase/merge/cherry-pick the proposal; or
- produce only the naming reconciliation plan against the current commission
  branch.

### D2 - Naming Reconciliation

Patch active stale language from "Commission Gate" / "commission gate" into
**Commission Signal Board** where the text semantically describes this product
object.

Do not change:

- factual branch/worktree names such as `codex/commission-gate`, except to add a
  note that the name is legacy;
- historical provenance records where the old phrase is intentionally recording
  what happened at the time;
- generic "commission" words in review prompts, handoffs, or operator language
  unrelated to the board.

Your closeout must include:

- the exact stale-language search commands;
- the remaining intentional hits;
- why each remaining hit was preserved.

### D3 - Commission Signal Board Artifact Inventory

Produce a table with:

| Current path | Artifact role | Move? | Proposed spine target | Reason |
| --- | --- | --- | --- | --- |

Classify at least:

- adjudication packet;
- board prompt;
- playbook;
- validator;
- validator tests;
- validator fixtures;
- repo-map entries;
- any related migration notes or review reports you discover.

### D4 - Spine Pull-Out Plan

APPLY `workflow-deep-thinking` to compare these options:

1. Stay in current `docs/product` / `docs/prompts` / `docs/workflows` layout.
2. Create only a docs-side spine folder.
3. Create the proposed `orca/product/spines/commission_signal_board/` pilot.
4. Create `orca/product/spines/commission_signal_board/` plus future
   `orca/docs/` global-docs split.

Use the criteria that actually matter here:

- agent discoverability;
- migration blast radius;
- stale-reference risk;
- fit with the current binding;
- fit with the MGT spine-first target;
- ability to leave historical records intact;
- whether runtime/code stays out of scope.

Produce a recommended route and a blocked/allowed next-action boundary.

### D5 - Pilot Spine Skeleton Or Migration Plan

If and only if the receiving lane has explicit owner or accepted-source
authority to create a live top-level `orca/` product workspace, then create the
Commission Signal Board pilot spine and update the required binding surfaces.

Minimum live-pilot scope:

```text
orca/product/spines/commission_signal_board/
  README.md
  spine.yaml
  authority/
  prompts/
  workflows/
  harness/
  tests/
  migrations/
```

Required binding surfaces before a live move:

- `docs/decisions/orca_repo_structure_binding_v0.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `repo-structure.yaml`
- `docs/STRUCTURE.md`
- `docs/workflows/orca_repo_map_v0.md`
- placement-checker expectations if they assert the closed root set

If that authority is not bound, do not create the live `orca/` root. Instead
write a docs-only migration plan under a bound current folder, for example:

```text
docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md
```

The plan must include:

- proposed final tree;
- file-by-file move table;
- stubs or moved-path-index strategy;
- reference rewrite exclusions;
- validation commands;
- rollback/reverse plan;
- open owner decisions.

### D6 - Closeout And Propagation

If you change product doctrine, architecture doctrine, workflow authority,
output authority, validation philosophy, or lifecycle boundary, include a
`direction_change_propagation` receipt or blocker per
`.agents/workflow-overlay/source-of-truth.md`.

Closeout must state:

- what was renamed/reconciled;
- what was not changed and why;
- what belongs inside the Commission Signal Board spine;
- what remains global/shared;
- whether the physical spine was created or deferred;
- next authorized step.

## Validation

Run the checks relevant to the actual edits:

```powershell
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_placement.py --check
git diff --check
```

If you edit the validator or its test/fixture paths, also run:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
cd orca-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py
```

If checks are not run, state why. A placement warning is not validation,
readiness, or acceptance; report it as structure evidence only.

## Hard Constraints

- Do not run a Commission Signal Board case.
- Do not retrieve external evidence.
- Do not classify demand.
- Do not forecast, weight, judge, score, or recommend.
- Do not build graph infrastructure.
- Do not turn the validator into evidence truth, demand proof, CI readiness, or
  buyer proof.
- Do not bulk-move Judgment, Capture, ECR, Signal Content, or Source Capture.
- Do not create a live `orca/` root unless the receiving lane has explicit
  authority and updates the binding surfaces.
- Do not treat the proposed spine-first structure decision as accepted until it
  is accepted by owner or later binding source.

## Output Mode

`file-write` for the receiving lane.

Expected durable outputs are either:

- active naming reconciliation plus a docs-only migration plan; or
- active naming reconciliation plus a live pilot spine and binding updates, only
  if authority is explicitly bound.

Do not return only a chat summary unless blocked before edits. If blocked,
return a compact blocker with the missing authority, what remains allowed, and
the smallest next authorization needed.
