# Commission Signal Board Lane Handoff v0

---
retrieval_header_version: 1
artifact_role: Orca handoff packet
scope: Cold-thread continuation packet for the Commission Signal Board lane after spine-first repo migration and cleanup.
use_when:
  - Restarting Commission Signal Board work in a new thread after repo structure shifted.
  - Checking which current CSB spine sources must be reloaded before any edit.
  - Avoiding stale commission-gate, old worktree, or pre-migration path assumptions.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/artifact-folders.md
  - docs/workflows/orca_repo_map_v0.md
  - orca/product/spines/commission_signal_board/README.md
  - orca/product/spines/commission_signal_board/spine.yaml
branch_or_commit: main @ c449b0f97906b4be1ccfee7ef734ba54f5b55df1
stale_if:
  - The CSB spine is renamed, retired, merged into another spine, or moved out of orca/product/spines/commission_signal_board/.
  - A controller migration lands after 2026-06-20 and changes CSB canonical artifact paths.
  - The next thread is not operating from a freshly checked current branch/worktree.
---

## Confirm-Don't-Trust Load Contract

This packet is a restart pointer, not authority. A fresh thread must verify the
repo before acting:

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/source-loading.md`.
4. Read `.agents/workflow-overlay/artifact-folders.md`.
5. Run `git status --short --branch`.
6. Read `docs/workflows/orca_repo_map_v0.md` as the retrieval map.
7. Reopen the CSB spine entry points listed in `open_next`.
8. Treat every branch, worktree, stale-path, and missing-file claim below as
   untrusted until rechecked in the new thread.

Do not continue from memory of the old commission-gate lane. The repo has moved
through spine-first structure, ontology tagging, and cleanup passes.

## Goal Handoff

Derived from the owner request on 2026-06-20:

- Long-term goal: keep the Commission Signal Board lane continuable after repo
  migration without importing stale commission-gate or pre-spine assumptions.
- Anchor goal for the next thread: re-establish live CSB state from current
  sources, then decide the next bounded CSB action from the current repo shape.
- Success signal: a fresh agent can identify the current CSB spine, avoid old
  branches/paths, name open decisions, and continue only the CSB lane without
  moving files or claiming readiness.

## Open Decision / Fork

The next thread should decide where to continue from:

- Recommended default: start from the current Orca repo root and current branch
  state, then create or choose a clean worktree only if writing is needed.
- Do not use the old `commission-spine-structure` worktree. It was checked this
  turn and the path did not exist.
- Related worktrees exist or recently existed, but they are not automatically
  safe continuation targets:
  - `C:/Users/vmon7/Desktop/projects/orca/.codex/worktrees/w3b-commission-signal-board`
    was observed on `codex/w3b-commission-signal-board...origin/main [behind 73]`.
  - `C:/Users/vmon7/Desktop/projects/orca/.codex/worktrees/ontology-tag-commission-signal-board`
    was observed on `codex/ontology-tag-commission-signal-board...origin/codex/ontology-tag-commission-signal-board [gone]`.
  - `C:/Users/vmon7/Desktop/projects/orca-worktrees/csb-spine` was observed on
    `commission-signal-board-spine...origin/commission-signal-board-spine [gone]`.
- Open product/workflow fork: decide whether the old inventory artifact should
  be recovered/ported into the new structure, or whether the current CSB spine
  plus Phase-2 proposal supersedes it for controller input.

## Drift Guard

Stale or dangerous assumptions to avoid:

- Do not call this lane `commission gate` unless quoting legacy wording. Current
  semantics are Commission Signal Board: evidence and signal routing, not demand
  classification.
- Do not treat graph weight as signal weight. CSB may specify graph-relevant
  retrieval structure, but it does not construct a graph or score demand.
- Do not authorize retrieval, scraping, capture, graph construction, demand
  classification, forecasting, Judgment, buyer proof, validation, readiness, CI,
  hook wiring, or runtime work merely because a board exists.
- Do not assume old `docs/product/` or `docs/prompts/product-planning/` CSB paths
  are canonical. Current observed canonical spine path is
  `orca/product/spines/commission_signal_board/`.
- Do not use `docs/migration/commission_signal_board_migration_inventory_v0.md`
  or `docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md`
  as current-main source without rechecking; both were absent on current `main`
  during this handoff.
- Do not stage unrelated untracked files in the root worktree.

## Inherited Context

Current observed repo state before this packet was written:

```text
branch/status:
## main...origin/main [behind 3]
?? .codex/hooks/run_orca_guard.py
?? _scratch/
?? docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md
warning: could not open directory 'orca-harness/.pytest_tmp/': Permission denied

HEAD:
c449b0f97906b4be1ccfee7ef734ba54f5b55df1
```

Current CSB surfaces found by `rg --files` include:

```text
orca/product/spines/commission_signal_board/README.md
orca/product/spines/commission_signal_board/spine.yaml
orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
orca/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md
orca/product/spines/commission_signal_board/harness/validator.md
orca/product/spines/commission_signal_board/migrations/moved_paths_index.md
orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
orca/product/spines/commission_signal_board/tests/validator_tests.md
orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
docs/migration/phase2_proposals/commission_signal_board_w3a_proposal_v0.md
orca-harness/tests/unit/test_commission_signal_board_output_validator.py
orca-harness/tests/fixtures/commission_signal_board_outputs/
```

Repo-map confirmation observed at `docs/workflows/orca_repo_map_v0.md:396`:

```text
orca/product/spines/commission_signal_board/ | Commission Signal Board pilot spine: authority, dispatch_rules, harness + tests + migrations + prompts + workflows (#261).
```

## Current Source Snapshot

The current CSB spine entry point says the canonical artifacts are:

- `orca/product/spines/commission_signal_board/spine.yaml`
- `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md`
- `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
- `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
- `orca/product/spines/commission_signal_board/harness/validator.md`
- `orca/product/spines/commission_signal_board/tests/validator_tests.md`
- `orca/product/spines/commission_signal_board/migrations/moved_paths_index.md`

The CSB README and spine manifest still contain phrases like
`global_docs_migration: staged_not_executed`. That may now be stale relative to
the current spine-first repository state. The next thread must recheck against
the latest controller/structure sources before treating that phrase as current.

The current Phase-2 proposal observed at
`docs/migration/phase2_proposals/commission_signal_board_w3a_proposal_v0.md`
says:

- the scanned area is `orca/product/spines/commission_signal_board/`;
- no deletion candidates were found for the CSB spine area;
- ontology/doc-term scan was clean for this area.

Treat the Phase-2 proposal as an owner-adjudication input, not as validation or
readiness proof.

## Next Authorized Move

In the new thread:

1. Reload the load contract sources above.
2. Re-run status and confirm whether `main` is still behind, dirty, or shifted.
3. Confirm whether the current branch should be a read-only orientation pass or
   a new writing worktree.
4. If writing is authorized, create/use a clean CSB-specific worktree from the
   current accepted base. Do not write on a stale CSB worktree without explicit
   rebase/reconciliation decision.
5. Decide the next narrow CSB action. The likely next action is a reconciliation
   note or prompt that aligns the CSB spine, moved-path index, Phase-2 proposal,
   and any missing old inventory claims with the current repo structure.

## Non-Claims

This packet does not claim:

- CSB readiness;
- validation of the CSB board, validator, prompt, or playbook;
- successful controller migration;
- that the old inventory was superseded;
- that any branch is mergeable;
- that any test suite passed;
- that any worktree is safe to edit;
- that the repository is clean;
- that the old commission-gate language is fully removed.

## Fresh-Thread Checklist

Before acting, the next thread should be able to answer:

- What branch/worktree am I actually on?
- Is the current CSB canonical path still
  `orca/product/spines/commission_signal_board/`?
- Are `README.md`, `spine.yaml`, playbook, prompt, validator pointer, tests
  pointer, and moved-path index still present?
- Did the controller migration land more changes after this packet?
- Is old inventory or old migration-plan content needed, absent, superseded, or
  intentionally left out?
- What exact file(s) am I authorized to change now?

