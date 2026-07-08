# Handoff Packet - Creator Ledger Placement ELI5

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-27T15:32:00+08:00
- created_by_lane: Codex current thread; provenance only, not authority.
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/hygiene/creator_ledger_placement_eli5_handoff_v0.md`
- expected_branch: `codex/ig-reels-capture-spine`
- expected_head: `20e0f42855579ab499c8793e49dfadb61e363eea`
- expected_dirty_state_including_handoff_file: tracked files were clean before writing this packet; branch upstream reported `[gone]`; this handoff file is expected to be untracked or modified after write; unrelated untracked scratch/handoff/worktree artifacts exist in the parent checkout and must not be treated as creator-ledger evidence.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Keep Orca's beauty-first Instagram creator-momentum work anchored in the correct spine-first product home without confusing product contracts, operational ledger rows, runtime storage, or hygiene checkpoints.
- anchor_goal: Produce a plain-English ELI5 answer for the owner explaining where the creator ledger belongs, what already exists, what the first actual ledger artifact should be called, and what not to build yet.
- success_signal: The owner can read the answer and immediately understand the placement distinction: contract/spec in the IG Capture source-family product tree; first static ledger artifact beside it; no runtime/database/crawler/data-lake move yet.

## Open Decision / Fork

- decision: Where should the actual creator ledger live after the existing creator roster/frontier ledger spec?
  - options:
    - Put the product contract/spec in `orca/product/spines/capture/core/source_families/social_media/instagram/` and place the first static docs-only ledger artifact beside it.
    - Put operational ledger rows in `orca-harness/` as runtime code/data.
    - Put the ledger in `docs/hygiene/`, `docs/workflows/`, `docs/decisions/`, ECR, Cleaning, or Data Lake.
  - already constrained / off the table: no runtime database, no runner, no crawler, no scheduler, no capture execution, no ECR/Cleaning/Judgment binding, no public creator directory, no outreach/lead list, no broad 1,000-creator execution.
  - trade-offs: product-tree adjacency preserves the source-family contract and lets the first static ledger instantiate it; runtime/data-lake placement would imply implementation/storage decisions the current spec explicitly leaves open; hygiene/workflows would make a product artifact look like transient process state.
  - owner of the call: owner can redirect, but absent redirect the spine-first product tree is the correct placement.
  - recommendation and why: recommend `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_v0.md` for the first docs-only/static ledger, because the existing spec is already in that folder and explicitly says first implementation should be static ledger model or fixture validator, not capture execution.

## Drift Guard

- invariant, non-goal, or scope boundary: Do not treat this packet, any hygiene handoff, or the prior noisy PR/hygiene work as authority for creator-ledger placement.
  - why it matters: the current thread drifted into PR cleanup; the receiver must re-ground in the product tree and overlay before giving advice.
  - what violating it would break: it could put product source under a transient folder or turn a placement question into runtime implementation.
- invariant, non-goal, or scope boundary: Do not build the ledger runtime, database, runner, crawler, source capture, scheduler, ECR, Cleaning, Judgment, or data-lake storage.
  - why it matters: the existing spec says those are non-goals or open questions.
  - what violating it would break: it would silently decide storage and implementation before the owner accepts the placement/ELI5 answer.
- invariant, non-goal, or scope boundary: Keep ELI5 simple, but do not soften the key distinction between a ledger contract, a static/manual ledger artifact, and future runtime storage.
  - why it matters: the owner asked to refocus because the thread became noisy.
  - what violating it would break: a vague answer would recreate the confusion.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` via `.agents/workflow-overlay/README.md`
- targets to enter the ladder:
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/artifact-folders.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/README.md`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- already loaded (weak orientation, freshness-marked; not authority): current sender read these files in the parent checkout on 2026-06-27; compare targets are listed in the source ledger.
- must load first (before strict or actionable steps): reread the overlay README, artifact folders, source-of-truth, and the IG creator roster/frontier ledger spec.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Product artifacts live under `orca/product/` unless they are decisions, prompts, workflow records, review artifacts, migration records, research, or hygiene.
  - decided in: `.agents/workflow-overlay/artifact-folders.md`
  - compare target: git blob `e4011ed4a89a9ed95c9e62568e4e4c92634d3252`
  - verify before: strict placement advice
- decision, framing, profile, or convention: Checkpoint/handoff artifacts under `docs/hygiene/` are convenience copies, never source of truth.
  - decided in: `.agents/workflow-overlay/source-of-truth.md`
  - compare target: git blob `fd42a38eb206327ff474fa83a2a5c90165c12a59`
  - verify before: treating any handoff as authority
- decision, framing, profile, or convention: The existing IG creator roster/frontier ledger spec is a proposed current-main ledger contract in the Instagram source-family product folder.
  - decided in: `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
  - compare target: git blob `d11271bc4f5c13375b9c40820969a50ac0756aa7`
  - verify before: naming or placing the first actual ledger artifact
- decision, framing, profile, or convention: The Source Capture Armory README indexes the IG creator roster/frontier ledger spec as the current proposed IG beauty creator roster/frontier ledger contract.
  - decided in: `orca/product/spines/capture/core/source_capture_toolbox/README.md`
  - compare target: git blob `f7859aff8ff46008118da6fdcc61d6ce8d510c9e`
  - verify before: saying the spec is discoverable from current maps

## Active Objective

Create an ELI5 answer for the owner about creator-ledger placement. Do not implement, move, rename, commit, push, or open a PR unless the owner explicitly redirects.

## Exact Next Authorized Action

1. Reread the load-bearing sources named above and compare their current content to the recorded blob targets or rerun `git rev-parse HEAD:<path>`.
2. Produce a concise ELI5 answer with this shape:
   - "The ledger spec already lives at <path>."
   - "The first actual static/manual ledger should live beside it at <suggested path>."
   - "Hygiene/workflows are for handoffs and maps, not the product ledger."
   - "Harness/data lake/runtime storage are later implementation/storage decisions, not now."
3. Stop after the ELI5 answer unless the owner explicitly asks for an edit or artifact creation.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` supplied in chat; load-bearing yes; compare target `reread-required` if strict behavior claims are needed.
- Overlay or equivalent authority: `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/artifact-folders.md`, `.agents/workflow-overlay/source-of-truth.md`.
- User constraints: current user said "workflow-handoff for this ledger thing - too noisy here. get them to eli5"; load-bearing yes; compare target is current chat.
- Source-read ledger:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint
    - Load-bearing: yes
    - Compare target: git blob `57cbc892dcd79d4d57686db465900ad042769174`
    - Last checked: 2026-06-27 current thread
    - Reuse rule: reread before strict claims
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: placement authority
    - Load-bearing: yes
    - Compare target: git blob `e4011ed4a89a9ed95c9e62568e4e4c92634d3252`
    - Last checked: 2026-06-27 current thread
    - Reuse rule: reread before placement advice
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: source hierarchy and checkpoint boundary
    - Load-bearing: yes
    - Compare target: git blob `fd42a38eb206327ff474fa83a2a5c90165c12a59`
    - Last checked: 2026-06-27 current thread
    - Reuse rule: reread before authority claims
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
    - Role: current proposed creator roster/frontier ledger contract
    - Load-bearing: yes
    - Compare target: git blob `d11271bc4f5c13375b9c40820969a50ac0756aa7`
    - Last checked: 2026-06-27 current thread
    - Reuse rule: reread before answering where the ledger belongs
  - `orca/product/spines/capture/core/source_capture_toolbox/README.md`
    - Role: Source Capture Armory index
    - Load-bearing: yes
    - Compare target: git blob `f7859aff8ff46008118da6fdcc61d6ce8d510c9e`
    - Last checked: 2026-06-27 current thread
    - Reuse rule: reread before saying the spec is current/indexed
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
    - Role: retrieval-only data capture map
    - Load-bearing: no for final placement, useful for route context
    - Compare target: git blob `a5d84a44e098490d5d352452bdb29a6913618f57`
    - Last checked: 2026-06-27 current thread
    - Reuse rule: reread only if map-routing claims matter
- Source gaps: no owner-approved actual static ledger artifact was found in the current loaded sources; receiver should confirm with `rg -n "ig_creator_roster_frontier_ledger_v0|creator_roster_entry" orca docs` if creating or naming a new artifact.
- Strict-only blockers: if the existing spec moved, was superseded, or changed its non-goals/open questions, do not reuse this placement answer without re-deriving it.
- Not-proven boundaries: this handoff does not prove readiness, validation, buyer proof, capture authorization, or runtime/storage design.

## Current Task State

- Completed: current thread identified the existing spec path and the likely placement distinction.
- Partially completed: no artifact edit for the actual ledger has been requested in the new lane; only ELI5 answer is authorized.
- Broken or uncertain: the parent checkout has lots of unrelated untracked material and an old branch upstream gone; ignore that noise unless the owner asks for cleanup.

## Workspace State

- Branch: `codex/ig-reels-capture-spine`
- Head: `20e0f42855579ab499c8793e49dfadb61e363eea`
- Dirty or untracked state before handoff: `git status --short --branch --untracked-files=no` returned `## codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine [gone]`; tracked files clean.
- Dirty or untracked state after writing the handoff file: this handoff file should be untracked or modified; receiver must run `git status --short --branch --untracked-files=all` before editing.
- Target files or artifacts: no target edit authorized; possible future static artifact path is `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_v0.md`.
- Related worktrees or branches: PR #409 for IG reels projection is separate and not the active creator-ledger lane.

## Changed / Inspected / Tested Files

- `docs/hygiene/creator_ledger_placement_eli5_handoff_v0.md`
  - Status: newly written handoff packet
  - Role: cold-lane continuation artifact, not authority
  - Important observations: routes receiver to ELI5 answer only
  - Symbols or sections: all packet sections
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
  - Status: inspected
  - Role: existing ledger contract/spec
  - Important observations: says it is docs-only/proposed; non-goals include database, runner, crawler, monitoring job, scraping, ECR/Cleaning/Judgment; open question asks YAML fixtures vs SQLite vs typed Python model first.
  - Symbols or sections: Status, Reconciliation Decision, Roster Entry Contract, Non-Goals, Open Questions, Recommendation
- `.agents/workflow-overlay/artifact-folders.md`
  - Status: inspected
  - Role: placement authority
  - Important observations: product artifacts belong under `orca/product/`; hygiene is for triage/cleanup notes.
  - Symbols or sections: Accepted Folders, Rules

## Frozen Decisions

- Decision: The creator-ledger spec/contract home is the Instagram source-family product folder.
  - Evidence: existing spec path and Source Capture Armory README index.
  - Consequence: do not relocate the spec to hygiene/workflows/runtime folders.
- Decision: First actual ledger artifact, if docs-only/static, should be adjacent to the spec.
  - Evidence: artifact-folders product-tree rule plus spec recommendation for static ledger model/fixture validator before implementation.
  - Consequence: recommended future path is `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_v0.md`.

## Mutable Questions

- Question: Should the later implementation be YAML fixture, SQLite table, or typed Python data model first?
  - Why still mutable: the existing spec names it as an open question.
  - What would resolve it: owner-approved implementation prompt or decision.
- Question: Which first commercial beauty sub-niche anchors the 250-record first gate?
  - Why still mutable: existing spec names it as open.
  - What would resolve it: owner selection or accepted product/capture artifact.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: using `docs/product/source_capture_toolbox/...` as the current path.
  - Why stale or dangerous: spine-first migration moved current product files into `orca/product/...`.
  - Current replacement: `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`.
- Stale instruction, idea, artifact, or finding: treating the earlier PR/hygiene branch work as the creator-ledger lane.
  - Why stale or dangerous: it concerns IG reels projection/hygiene and created noise.
  - Current replacement: answer only the creator-ledger placement ELI5.

## Commands And Verification Evidence

- Command:
  ```powershell
  git branch --show-current
  ```
  Result:
  - Passed: `codex/ig-reels-capture-spine`
  - Re-run target so the receiver can confirm rather than trust: same command in workspace root.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed: `20e0f42855579ab499c8793e49dfadb61e363eea`
  - Re-run target so the receiver can confirm rather than trust: same command in workspace root.
- Command:
  ```powershell
  git status --short --branch --untracked-files=no
  ```
  Result:
  - Passed: `## codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine [gone]`
  - Re-run target so the receiver can confirm rather than trust: same command plus `--untracked-files=all` before edits.
- Command:
  ```powershell
  git rev-parse HEAD:<path>
  ```
  Result:
  - Passed for the source ledger blob targets listed above.
  - Re-run target so the receiver can confirm rather than trust: rerun for every load-bearing source.

## Blockers And Risks

- Blocker or risk: receiver answers from this packet alone without rereading the spec.
  - Evidence: handoff packets are weak context by overlay rule.
  - Likely next action: reread load-bearing sources first.
- Blocker or risk: receiver overbuilds by creating runtime storage or a database.
  - Evidence: existing spec makes database/runner/crawler non-goals and leaves representation open.
  - Likely next action: stop at ELI5 unless owner redirects.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Current product artifact placement rule.
  - Existing spec path and status.
  - Existing spec non-goals and open questions.
  - Current branch/head and dirty state if editing.
- Compare target for each:
  - Git blob hashes in the source ledger, plus fresh reads of current files.
- Load outcomes and what each means:
  - `REUSE`: hashes/path/status still match; produce ELI5 answer.
  - `STALE_REREAD_REQUIRED`: source changed but can be re-read; re-derive answer.
  - `BLOCKED_DRIFT`: source moved or contradicts the packet; report the conflict.
  - `BLOCKED_UNVERIFIABLE`: source unavailable and no pasted capsule; do not answer strictly.
- Sources that must be reread if drift is detected:
  - `.agents/workflow-overlay/artifact-folders.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/README.md`

## Do Not Forget

- The owner asked for ELI5 because this thread got noisy. Answer simply, then stop.
