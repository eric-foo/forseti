# Capture Recency / Current-State Preservation Blast-Radius Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet
scope: >
  Transfers the PR #354 recency/currentness package to a fresh Capture lane for
  bounded blast-radius review of preservation-priority wording and Capture-owned
  surfaces.
use_when:
  - Starting a fresh Capture lane to inspect or patch Capture-controlled docs
    after the CSB, Scanning, Capture, and Judgment recency/currentness package.
  - Re-establishing the branch state and source pack before Capture
    blast-radius work.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md
branch_or_commit: codex/scanning-broad-scout-recency-default @ 5a861ffe84d65e4af686f36a5ad559a7cd04630e
stale_if:
  - Branch codex/scanning-broad-scout-recency-default is rebased or amended after 5a861ffe84d65e4af686f36a5ad559a7cd04630e.
  - Any load-bearing source named in this packet changes before the receiver acts.
  - The current user redirects to scanning enforcement, source execution, or route implementation instead of Capture blast-radius review.
```

## Load Contract

- packet_version: 1
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-06-23 Asia/Singapore
- created_by_lane: Codex current thread, for provenance only; not an authority claim
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default`
- handoff_path: `docs/hygiene/capture_recency_current_state_preservation_blast_radius_handoff_v0.md`
- expected_branch: `codex/scanning-broad-scout-recency-default`
- expected_head: `5a861ffe84d65e4af686f36a5ad559a7cd04630e` before this handoff file is committed
- expected_dirty_state_including_handoff_file: clean before writing; after initial write, this handoff file is the only expected dirty or untracked path; if loaded from a later committed branch, re-run `git status --short --branch` and treat any unexplained drift as material
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: Keep Orca's discovery-to-capture-to-judgment pipeline coherent so Commission Signal Board and Scanning can prioritize recent/current public signal, Capture can preserve volatile states, and Judgment can read the evidence without converting freshness into proof or scoring.
- anchor_goal: Capture performs a bounded blast-radius review of the PR #354 recency/currentness package and patches only Capture-controlled surfaces if they need preservation-priority wording or schema alignment.
- success_signal: The Capture lane returns a source-backed no-change report or a narrow patch showing which Capture surfaces were inspected, what changed if anything, and that recency/currentness still affects preservation urgency only, not access, route binding, demand proof, scoring, or claim tier.

## Open Decision / Fork

- decision: Does Capture need more local propagation after the playbook's new "Recency / Current-State Preservation Priority" section, or is that section plus existing route/access doctrine enough?
  - options:
    - A. No-change blast-radius report: Capture confirms the playbook already covers the package and no additional Capture surfaces need edits.
    - B. Narrow docs patch: Capture adds or tightens wording in Capture-owned README, intake, source-family, or profile surfaces that a capture operator would actually open.
    - C. Code or schema enforcement: Capture adds a mechanical field/check only if an existing Capture-owned checker, schema, or intake surface already has a stable place for current-state preservation metadata.
  - already constrained / off the table:
    - No live source capture, web run, source-access change, route binding, crawler, monitor, registry, atlas, outreach, buyer contact, ECR execution, Cleaning execution, Judgment execution, or candidate minting.
    - No scanning enforcement pass in this handoff. The owner explicitly said scanning code-vs-doctrine enforcement comes after the Capture handoff.
    - No broad Capture rewrite. Patch only surfaces that would otherwise mis-handle preservation priority from Commission Signal Board or Scanning.
  - trade-offs:
    - A is lowest churn but may leave operator-facing Capture surfaces under-signposted.
    - B is likely the right default if a Capture surface consumes `capture_request`, retail product pages, social/current-state surfaces, or demand-durability profiles without mentioning preservation urgency.
    - C is only worth it when the field boundary already exists; otherwise it creates higher lock-in than the current request needs.
  - owner of the call: Chief Architect / current user after Capture lane reports findings.
  - recommendation and why: Start with B-biased inspection and land no patch unless a real Capture-controlled surface would confuse recency/currentness with route, access, proof, or ordinary priority. Do not build code unless an existing checker/schema makes enforcement cheap and local.

## Drift Guard

- invariant, non-goal, or scope boundary: Recency/currentness is preservation and attention priority only.
  - why it matters: The accepted package deliberately lets newer/current source states receive more attention while blocking proof, scoring, route, access, classifier, graph-weight, and claim-tier leakage.
  - what violating it would break: Capture could incorrectly treat a recent stockout, review, forum post, or partner page as demand proof or as authorization to use a route that Step 0 has not cleared.
- invariant, non-goal, or scope boundary: Capture still owns source access, route choice, acquisition method, provenance depth, and captured-state recording.
  - why it matters: Scanning may emit a `capture_request`; it cannot bind a route or authorize acquisition.
  - what violating it would break: Scanning would become an implicit capture runner, and the Source Capture Playbook's access-control gate would be bypassed.
- invariant, non-goal, or scope boundary: This packet is a checkpoint, not source of truth.
  - why it matters: Orca source-of-truth rules classify handoff packets as orientation only.
  - what violating it would break: A stale packet could override the playbook, repo map, overlay, or current user instruction.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`
  - `orca/product/spines/scanning/README.md`
  - `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- already loaded (weak orientation, freshness-marked; not authority): current thread loaded the workflow-handoff skill, Orca overlay entry points, source-loading, artifact-folders, source-of-truth, retrieval-metadata, validation-gates, hashes, and targeted excerpts on 2026-06-23.
- must load first (before strict or actionable steps): `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/source-loading.md`, this packet, the Capture playbook, and the current branch/diff state.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Commission Signal Board rows now carry `recency_status` and `recency_attention` as source-route priority metadata, not truth or proof.
  - decided in: `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
  - compare target: git hash `c39a9868db8329bd1aea8c6ba5b75bf8a95b8b7e`; targeted excerpt lines 293-307 define recency fields and source-route priority.
  - verify before: strict claim about what Commission Signal Board emits.
- decision, framing, profile, or convention: Scanning uses a default bounded broad-scout phase for CSB-first scans and treats recency/currentness as a hard attention-priority rule, not proof.
  - decided in: `orca/product/spines/scanning/README.md` and `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
  - compare targets: README hash `33e54d4bbe89bb105cd002e2d8b9a53ed48c168b`; MGT hash `f9a28a77b019a97d55f29b1053271273a720131f`; `rg` hits at MGT lines 69-110 and 169-181 show broad-scout and recency/current-state priority boundaries.
  - verify before: strict claim about scanning obligations or defaults.
- decision, framing, profile, or convention: Capture treats scanning or CSB recent/current-state markers as preservation urgency and source-drift risk only.
  - decided in: `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - compare target: git hash `49d54a77270f05f680a076afe3de6b0b472ee6ff`; targeted excerpt lines 257-270.
  - verify before: any Capture patch or no-change closeout.
- decision, framing, profile, or convention: Judgment treats recency/currentness as qualitative attention/relevance only, not proof, numeric weight, or scoring.
  - decided in: `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
  - compare target: git hash `dffad29cda6236dc894736a9c6f5f04feb335ade`; targeted excerpt lines 137-141 and 402-409.
  - verify before: any cross-lane claim that recency affects Judgment.
- decision, framing, profile, or convention: The cross-vendor adversarial review found no proof, gate, scoring, classifier, graph-weight, route-binding, or access-authorization leakage in the propagation package.
  - decided in: `docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`
  - compare target: git hash `af3dab9886ba46b0c462190dfbcb486874c3c63b`; targeted excerpt lines 108-140.
  - verify before: using the review as support for acceptance or no-change reasoning.

## Active Objective

Fresh Capture lane should determine whether Capture-controlled surfaces need narrow changes so recent/current-state source priority is operationally visible as preservation urgency without changing source access, route selection, proof semantics, scoring, or candidate promotion.

## Exact Next Authorized Action

1. Verify branch, head, and dirty state in `C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default`, or create a fresh worktree from branch `codex/scanning-broad-scout-recency-default` if editing in parallel.
2. Load the required sources named in this packet and inspect only Capture-controlled blast-radius surfaces that an operator or prompt would use for capture requests, route selection, retail product pages, social/current-state surfaces, demand-durability profiles, or source-access boundaries.
3. Return either a source-backed no-change report or a narrow patch. If patching, run `git diff --check`, `python .agents/hooks/check_retrieval_header.py --changed`, `python .agents/hooks/check_repo_map_freshness.py --changed`, `python .agents/hooks/check_map_links.py --strict`, `python .agents/hooks/check_placement.py --check`, and a targeted stale-language search for recency/currentness being converted into proof, scoring, access authorization, route binding, classifier mapping, graph weight, claim tier, crawler, monitor, registry, or atlas language.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca agent behavior kernel.
    - Load-bearing: yes.
    - Compare target: git hash `dab36cc46581c24e585044f241da135d8193f188`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before any strict workflow, commit, validation, or handoff claim.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: Orca overlay entrypoint and binding rule.
    - Load-bearing: yes.
    - Compare target: git hash `57cbc892dcd79d4d57686db465900ad042769174`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before project-authority or source-loading claims.
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: source hierarchy, conflict rules, and checkpoint-artifact lifecycle.
    - Load-bearing: yes.
    - Compare target: git hash `fd42a38eb206327ff474fa83a2a5c90165c12a59`; checkpoint-artifact section states handoffs are orientation only.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before treating this packet or any prior packet as reusable.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading budgets and Capture read-pack entry points.
    - Load-bearing: yes.
    - Compare target: git hash `57a6dd2d632b255e2852d27caa2bdb3ee5e94e1d`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before expanding beyond the named source pack.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted durable artifact folders; confirms `docs/hygiene/` as accepted.
    - Load-bearing: yes.
    - Compare target: git hash `fd7e203abbb76ae00005a0981bd71c9c5931bc86`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before moving or rehoming this packet.
  - `.agents/workflow-overlay/retrieval-metadata.md`
    - Role: retrieval-header contract.
    - Load-bearing: yes.
    - Compare target: git hash `f675c5dd9357d4c53000ff8beb040839b3e06343`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before changing this packet's header.
  - `.agents/workflow-overlay/validation-gates.md`
    - Role: validation expectations and enforcement-placement principle.
    - Load-bearing: yes.
    - Compare target: git hash `c7a2957634a3560017e513c28856e12b9bb5514b`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before claiming validation or deciding code-vs-doctrine enforcement.
- User constraints:
  - Current instruction: create a `workflow-handoff` for Capture to work with the package, then later inspect whether scanning can be enforced by code or doctrine.
    - Load-bearing: yes.
    - Compare target: current chat instruction, 2026-06-23.
    - Last checked: 2026-06-23.
    - Reuse rule: if user redirects, current instruction wins.
- Source-read ledger:
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: repo map and route summary for spines.
    - Load-bearing: yes.
    - Compare target: git hash `935641e6ae1017f11d49bd9549f28c7b11b32ab1`; targeted hits at lines 416, 420, 422, 549 route scanning, judgment, CSB, and Capture semantics.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before claiming current route map state.
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
    - Role: retrieval-only front door for Data Capture Spine / Source Capture Armory.
    - Load-bearing: yes.
    - Compare target: git hash `a5d84a44e098490d5d352452bdb29a6913618f57`.
    - Last checked: 2026-06-23.
    - Reuse rule: open first for broader Capture-spine navigation; do not treat as source-access authority.
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
    - Role: canonical Capture method and current recency/current-state preservation priority.
    - Load-bearing: yes.
    - Compare target: git hash `49d54a77270f05f680a076afe3de6b0b472ee6ff`; lines 257-270 carry the new rule.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before any Capture blast-radius verdict.
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
    - Role: Capture recon index and per-source probe map.
    - Load-bearing: yes.
    - Compare target: git hash `4328d946cfc7fbbae37ed530732a388e368465e8`.
    - Last checked: 2026-06-23.
    - Reuse rule: open when source-family or route-card impacts are material.
  - `docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`
    - Role: prior adversarial review report of the propagation package.
    - Load-bearing: yes.
    - Compare target: git hash `af3dab9886ba46b0c462190dfbcb486874c3c63b`; lines 108-140 summarize non-leakage.
    - Last checked: 2026-06-23.
    - Reuse rule: supporting evidence only; not authority and stale if targets changed.
  - `docs/prompts/reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_prompt_v0.md`
    - Role: review prompt provenance.
    - Load-bearing: no.
    - Compare target: git hash `3af159ba2b0042d487d956a377c0c01592c57f04`.
    - Last checked: 2026-06-23.
    - Reuse rule: open only if review scope must be audited.
  - `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
    - Role: CSB row schema and DCP receipt for recency/currentness.
    - Load-bearing: yes for cross-spine package semantics.
    - Compare target: git hash `c39a9868db8329bd1aea8c6ba5b75bf8a95b8b7e`; lines 293-307 and 605-613.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before strict claims about CSB outputs.
  - `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
    - Role: Judgment demand-read semantics for recency/currentness.
    - Load-bearing: yes for cross-spine package semantics.
    - Compare target: git hash `dffad29cda6236dc894736a9c6f5f04feb335ade`; lines 137-141 and 402-409.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before any Judgment claim.
  - `orca/product/spines/scanning/README.md`
    - Role: scanning front door and broad-scout/recency route.
    - Load-bearing: yes for package context.
    - Compare target: git hash `33e54d4bbe89bb105cd002e2d8b9a53ed48c168b`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before any scanning handoff or enforcement claim.
  - `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
    - Role: MGT operating model for intelligent walking, broad-scout, capture requests, and recency/current-state priority.
    - Load-bearing: yes for package context.
    - Compare target: git hash `f9a28a77b019a97d55f29b1053271273a720131f`.
    - Last checked: 2026-06-23.
    - Reuse rule: reread before any scanning handoff or enforcement claim.
- Source gaps:
  - Capture source-family files were listed by `rg --files` but not opened in this handoff. The receiver should inspect them only if they are in the blast radius of preservation priority.
  - PR metadata was not re-fetched for this packet. Branch/head and local sources are the load-bearing compare targets.
- Strict-only blockers:
  - If branch head, target files, or dirty state drift, do not reuse this packet as `REUSE`; return `STALE_REREAD_REQUIRED` or `BLOCKED_DRIFT`.
  - If the receiver cannot access the repo/filesystem, request a pasted source capsule instead of acting from this packet alone.
- Not-proven boundaries:
  - This packet is not validation, readiness, acceptance, merge approval, source-access authorization, capture authorization, route binding, code-enforcement authorization, or product proof.

## Current Task State

- Completed:
  - Scanning front door and MGT model were updated so CSB-first scans use a bounded broad-scout phase by default and prioritize recent/current-state source states as attention/relevance, not proof.
  - Commission Signal Board, Capture, Judgment, and repo map propagation was landed on this branch through commit `13a1becb3841a2596430dc345674c86fa697e098`.
  - A cross-vendor adversarial review report was added and CA-adjudicated through commit `5a861ffe84d65e4af686f36a5ad559a7cd04630e`; minor findings were patched.
- Partially completed:
  - Capture has the central playbook rule, but a dedicated Capture blast-radius pass has not yet checked source-family docs, intake surfaces, demand-durability profiles, or operator-facing Capture README/index surfaces for local propagation needs.
- Broken or uncertain:
  - No known correctness blocker.
  - Unknown whether Capture should add local wording to source-family or profile surfaces. That is the receiver's active decision.

## Workspace State

- Branch: `codex/scanning-broad-scout-recency-default`
- Head before this handoff file is committed: `5a861ffe84d65e4af686f36a5ad559a7cd04630e`
- Dirty or untracked state before handoff: clean; `git status --short --branch` returned only `## codex/scanning-broad-scout-recency-default...origin/codex/scanning-broad-scout-recency-default`
- Dirty or untracked state after writing the handoff file: this file is expected as a new dirty/untracked path until committed; receiver must verify live state
- Target files or artifacts:
  - `docs/hygiene/capture_recency_current_state_preservation_blast_radius_handoff_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - Capture-controlled source-family, contract, source-access, and demand-durability surfaces named by the receiver's blast-radius inspection
- Related worktrees or branches:
  - Current worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default`
  - Current branch: `codex/scanning-broad-scout-recency-default`

## Changed / Inspected / Tested Files

- `docs/hygiene/capture_recency_current_state_preservation_blast_radius_handoff_v0.md`
  - Status: new handoff packet.
  - Role: checkpoint artifact for Capture lane transfer; retrieval-only.
  - Important observations: must be consumed with confirm-don't-trust load protocol.
  - Symbols or sections: Load Contract, Goal Handoff, Open Decision / Fork, Drift Guard, Inherited Context, Active Objective, Exact Next Authorized Action.
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - Status: inspected targeted lines 257-270.
  - Role: canonical Capture method and controlling preservation-priority wording.
  - Important observations: recency/current-state priority is preservation urgency and source-drift risk only; no proof, access-gate change, route selection, or route binding.
  - Symbols or sections: `## Recency / Current-State Preservation Priority`.
- `docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`
  - Status: inspected targeted lines 1-180.
  - Role: adversarial review support.
  - Important observations: found no leakage; minor findings patched/adjudicated in later commit.
  - Symbols or sections: `### Non-Finding: No proof, gate, scoring, classifier, or route-binding leakage`, `### AR-01`.
- `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
  - Status: inspected targeted lines 286-310 and 598-620.
  - Role: CSB row metadata semantics.
  - Important observations: recency fields are source-route priority metadata, not truth.
  - Symbols or sections: row schema and DCP receipt.
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
  - Status: inspected targeted lines 132-146 and 396-412.
  - Role: Judgment semantics.
  - Important observations: attention-priority rule is not gate proof, numeric weight, or scoring shortcut.
  - Symbols or sections: C2 demand-mechanism read and DCP receipt.
- `orca/product/spines/scanning/README.md`
  - Status: searched targeted recency/broad-scout/capture_request terms.
  - Role: scanning front door.
  - Important observations: CSB-first scans use bounded broad-scout by default; Capture route binding remains Capture-owned.
  - Symbols or sections: retrieval header, broad-scout and recency language.
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
  - Status: searched targeted recency/broad-scout/capture_request terms.
  - Role: scanning MGT operating model.
  - Important observations: broad-scout returns are route-shaped and bounded; `capture_request` asks Capture to inspect, not to take a route.
  - Symbols or sections: Default CSB Broad-Scout Phase, Recency / Current-State Priority, Capture Request Contract.

## Frozen Decisions

- Decision: Preserve recency/currentness as attention and preservation priority only.
  - Evidence: Capture playbook lines 257-270; CSB prompt lines 303-307; Judgment lines 137-141; review report lines 108-140.
  - Consequence: Capture can prioritize volatile current-state preservation but cannot treat freshness as proof, route authorization, or access clearance.
- Decision: Scanning enforcement work is deferred out of this handoff.
  - Evidence: current user instruction says to hand off to Capture first, then later inspect scanning code-vs-doctrine enforcement.
  - Consequence: Receiver must not use this handoff to implement scanning checker changes.
- Decision: Handoff packets are checkpoint artifacts, not source of truth.
  - Evidence: `.agents/workflow-overlay/source-of-truth.md` checkpoint-artifact section.
  - Consequence: Receiver must verify load-bearing claims against primary sources before acting.

## Mutable Questions

- Question: Does Capture need local propagation beyond the central playbook?
  - Why still mutable: Source-family, intake, and demand-durability surfaces were not opened in this handoff.
  - What would resolve it: Receiver inspects targeted Capture surfaces and either reports no-change with citations or patches narrow stale/confusing language.
- Question: Should any part of the scanning recency/broad-scout package be enforced mechanically?
  - Why still mutable: The current handoff excludes scanning enforcement.
  - What would resolve it: A later scan of existing hooks, schemas, prompt validators, and doctrine surfaces to classify what is code-checkable versus judgment-bound.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "Every CSB scan gets a subagent by default" as a runtime requirement.
  - Why stale or dangerous: The accepted scanning model requires a bounded broad-scout phase by default, not mandatory subagent infrastructure.
  - Current replacement: Broad-scout phase is mandatory by default; how it is staffed is implementation/runtime-dependent and not bound by this packet.
- Stale instruction, idea, artifact, or finding: Precursor-first scanning.
  - Why stale or dangerous: Owner clarified scanning starts from CSB and asks venue value / hidden venue / buyer-language questions; precursor language is for routing venues, not the whole lane.
  - Current replacement: CSB-first venue-value scanning with bounded broad scout, exact-query gap testing, and capture requests where preservation is needed.
- Stale instruction, idea, artifact, or finding: Capture should treat recent/current findings as demand proof.
  - Why stale or dangerous: It would violate the playbook and the adversarial review's non-leakage boundary.
  - Current replacement: Capture treats them as preservation urgency/source-drift risk only.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed.
  - Important output: `## codex/scanning-broad-scout-recency-default...origin/codex/scanning-broad-scout-recency-default`
  - Re-run target so the receiver can confirm rather than trust: same command in the handoff worktree.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed.
  - Important output: `5a861ffe84d65e4af686f36a5ad559a7cd04630e`
  - Re-run target so the receiver can confirm rather than trust: same command before reuse.
- Command:
  ```powershell
  Test-Path docs\hygiene\capture_recency_current_state_preservation_blast_radius_handoff_v0.md
  ```
  Result:
  - Passed before writing.
  - Important output: `False`
  - Re-run target so the receiver can confirm rather than trust: `Test-Path` or `Get-Item` after checkout.
- Command:
  ```powershell
  git hash-object -- <named source file>
  ```
  Result:
  - Passed for every ledger source listed above.
  - Important output: hashes recorded in the Authority And Source Ledger.
  - Re-run target so the receiver can confirm rather than trust: repeat `git hash-object` for every load-bearing file.
- Command:
  ```powershell
  rg -n "broad scout|broad-scout|recency|currentness|current-state|capture_request|Capture" orca\product\spines\scanning\README.md orca\product\spines\scanning\scan_core\orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  ```
  Result:
  - Passed.
  - Important output: hits confirm accepted broad-scout, recency/current-state priority, and Capture route-binding boundaries.
  - Re-run target so the receiver can confirm rather than trust: same command or narrower line reads.

## Blockers And Risks

- Blocker or risk: Capture blast-radius scope could expand into scanning enforcement.
  - Evidence: user explicitly placed scanning code-vs-doctrine enforcement after the Capture handoff.
  - Likely next action: stop at Capture surfaces; create a separate enforcement plan later.
- Blocker or risk: A Capture surface may repeat stale "priority" wording without the preservation-only guard.
  - Evidence: only the central playbook has been read for Capture recency wording in this handoff.
  - Likely next action: targeted search across Capture for `recency`, `current-state`, `freshness`, `preservation`, `route`, `access`, `proof`, `score`, `capture_request`.
- Blocker or risk: Code enforcement may be tempting but overbuilt.
  - Evidence: no existing Capture schema/checker was identified in this handoff as a clear field boundary.
  - Likely next action: prefer docs patch unless an existing checker/schema makes enforcement cheap and local.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Branch/head and dirty state.
  - This packet path is present and readable.
  - Every load-bearing source hash in the Authority And Source Ledger.
  - Capture playbook lines 257-270 still carry preservation-only semantics.
  - Scanning README/MGT still make broad-scout default and Capture route binding non-authorizing.
  - CSB prompt still defines recency fields as source-route priority metadata, not truth.
  - Judgment still treats recency/currentness as attention-only, not proof/scoring/weight.
  - The review report is still applicable or marked stale if target sources changed.
- Compare target for each:
  - Git branch/head: `git status --short --branch`; `git rev-parse HEAD`.
  - File content: `git hash-object -- <path>` using hashes in this packet.
  - Key source claims: targeted line reads or equivalent `rg`/`Select-String` hits.
- Load outcomes and what each means:
  - `REUSE`: all required load-bearing facts re-verified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional/non-load-bearing facts drifted; reuse verified sections and re-derive the rest.
  - `STALE_REREAD_REQUIRED`: material source, head, target files, or hashes drifted but can be re-read safely.
  - `BLOCKED_DRIFT`: drift conflicts with user constraints, authority, target path, or dirty-state policy.
  - `BLOCKED_MISSING_PACKET`: packet path absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim lacks a usable compare target and cannot be re-derived.
- Sources that must be reread if drift is detected:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - `docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`

## Do Not Forget

Capture should have a productive blast-radius pass here, but its job is to preserve volatile source states under Capture-owned method, not to promote recent sources into proof or let scanning bind Capture's route.
