# Capture Spine Runner Data Lake Dump Audit Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet
scope: >
  Cold-lane handoff for a read-only audit of Capture Spine runners and whether
  each intended packet writer commits Source Capture Packet material into the
  Orca data lake correctly.
use_when:
  - Starting a parallel audit of capture-runner data-lake write compliance.
  - Checking which Source Capture runners still write only local output.
  - Reconciling live lake sharded path evidence with current DataLakeRoot code/tests.
  - Checking v4.1 forward-epoch lake-write compatibility.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca-harness/data_lake/root.py
  - orca-harness/source_capture/writer.py
stale_if:
  - Any capture runner gains or loses --data-root / ORCA_DATA_ROOT support.
  - DataLakeRoot raw pathing, availability index shape, or sharding behavior changes.
  - The Silver Vault contract is adopted or patched to settle physical sharding.
  - The v4.1 forward-epoch folder grammar changes.
```

## Load Contract

- packet_version: `workflow_handoff_max_v0`
- mode: max
- created_at: `2026-06-28T01:14:24.9718781+08:00`
- created_by_lane: Codex current thread, provenance only
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`
- expected_branch: `codex/ig-reels-capture-spine`
- expected_head: `3628dbacd968bb316031012e39d15a9b4d320355`
- expected_dirty_state_including_handoff_file: many unrelated untracked files already exist; this handoff file is newly untracked after writing.
- source_loading_mode: repo-overlay-bound
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Orca should be able to trust that capture runners land raw source evidence into the v4.1 lake consistently enough for downstream Silver Vault, ECR, Cleaning, and Judgment work to build on keyed raw truth.
- anchor_goal: Audit Capture Spine runner data-lake dump behavior against the v4.1 forward-epoch contract without touching the Silver Vault schema lane: identify which intended packet writers support v4.1 lake commit, which still local-output only, and where code/tests/docs conflict with the live lake.
- success_signal: A cold reader produces a v4.1 runner compliance matrix with file/line evidence, live-lake comparison, test coverage gaps, and a bounded patch recommendation, while making no Silver Vault edits and no live-lake writes.

## Open Decision / Fork

- decision:
  - options:
    - Read-only audit only, then return a gap matrix and patch plan.
    - Audit plus implementation patch to add v4.1 `--data-root` support across missing packet runners.
  - already constrained / off the table:
    - Do not write to `F:\orca-data-lake` during the audit.
    - Do not modify the Silver Vault record contract or generated read-model plan in this lane.
    - Do not treat projection-only, screening-only, bootstrap, or quality-report runners as packet writers unless code proves they emit Source Capture Packets.
  - trade-offs:
    - Read-only audit is lower-collision and surfaces the exact failure set.
    - Immediate patching may save a turn but risks broad implementation churn and may encode the wrong physical path if sharding is unresolved.
  - owner of the call: Orca owner / current user for broad implementation authorization.
  - recommendation and why: Start read-only. The live lake currently shows sharded raw paths while current `DataLakeRoot` code/tests still assert unsharded paths, so patching before reconciling that mismatch is the wrong lock-in.

## Drift Guard

- invariant, non-goal, or scope boundary: This lane audits capture-runner data-lake compliance only.
  - why it matters: The active Silver Vault lane is separately deciding semantic records and generated read models.
  - what violating it would break: Editing Silver Vault or read models here would create cross-lane drift and blur which lane owns schema decisions.
- invariant, non-goal, or scope boundary: Treat live-lake sharded path evidence as useful evidence, but the v4.1 contract as the forward authority.
  - why it matters: Current live `indexes/availability` entries reference sharded `raw/<shard>/<packet_id>` paths, while `orca-harness/data_lake/root.py` has unsharded legacy `raw/<packet_id>` literals; v4.1 expects canonical raw packet refs under `raw/<packet_shard>/<packet_id>/`.
  - what violating it would break: A premature patch could make tests pass against a legacy shape while missing the v4.1 canonical raw/derived/index forward contract.
- invariant, non-goal, or scope boundary: No network capture, no live runner execution, no F-drive writes by default.
  - why it matters: The requested lane is confirmation of dumping behavior, not new data acquisition.
  - what violating it would break: It would add operational side effects and require separate approvals.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - `orca-harness/data_lake/root.py`
  - `orca-harness/source_capture/writer.py`
  - `orca-harness/runners/`
  - `orca-harness/tests/`
- already loaded (weak orientation, freshness-marked; not authority):
  - Orca overlay README, artifact folder rules, retrieval metadata, source-loading, decision routing.
  - Data Capture Spine consolidation map, source capture playbook, capture recon index.
  - Data Lake core and derived layout/index contracts.
  - Current Silver Vault draft contract.
  - Runner and test scans dated `2026-06-28T01:14:24.9718781+08:00`.
- must load first (before strict or actionable steps):
  - `AGENTS.md` or current root instructions.
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `orca-harness/data_lake/root.py`
  - `orca-harness/source_capture/writer.py`
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: The data lake owns raw packet preservation and content-free availability, not Cleaning, ECR, Judgment, or orchestration.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
  - compare target: file exists and its header scope starts "Core responsibility contract for Orca's data lake".
  - verify before: strict claims about what the lake is allowed to own.
- decision, framing, profile, or convention: Derived records and indexes are append-only/rebuildable; `indexes/` is not authority.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
  - compare target: file size observed `10557`, mtime UTC `2026-06-21T08:46:40.5126897Z`.
  - verify before: claiming what derived/indexes can or cannot do.
- decision, framing, profile, or convention: Capture-spine work starts from the Data Capture Spine submap and source-capture playbook; runner docs may be ahead of implementation and code must be checked.
  - decided in: `.agents/workflow-overlay/source-loading.md` and `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - compare target: submap file size observed `43304`, mtime UTC `2026-06-21T16:31:13.1705949Z`.
  - verify before: choosing audit source pack or runner scope.

## Active Objective

Run a read-only Capture Spine runner audit that answers: for each intended Source Capture packet writer, does it support committing into the v4.1 Orca data lake via `--data-root` or `ORCA_DATA_ROOT`, does it use v4.1 `DataLakeRoot` semantics and refs, and is that behavior covered by tests?

The output is an audit report and patch recommendation, not a patch.

## Exact Next Authorized Action

1. Re-verify the workspace branch/head/dirty state and load the required overlay/source files named above, including the v4.1 forward-epoch contract.
2. Build a runner matrix from `orca-harness/runners/*.py`, separating:
   - Source Capture packet writers.
   - Source Capture bootstrap/config runners.
   - Projection/read-only/reporting runners.
   - Candidate-intake/frontier/screening runners that are not packet writers.
3. For each intended packet writer, record whether it has `--data-root`, `ORCA_DATA_ROOT`, mutual exclusion with `--output`, v4.1 root-marker checks, v4.1 raw/derived/index refs, shared `source_capture.writer.write_capture_packet` or equivalent staging/publish, content-free availability, and tests.
4. Reconcile code/test expected raw paths against live root observations from `F:\orca-data-lake`, without writing to that root.
5. Produce a report under `docs/review-outputs/` or another accepted review-output folder, with findings ordered by severity and a smallest-complete patch plan.
6. Stop before implementation unless the current user explicitly authorizes a bounded code patch.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Orca project behavior kernel and work authorization boundary.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: supplied in current thread context before this handoff.
    - Reuse rule: re-open before strict work if available.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint and binding rule.
    - Load-bearing: yes.
    - Compare target: header says `artifact_role: Orca overlay authority`; read `2026-06-28`.
    - Last checked: `2026-06-28T01:14:24.9718781+08:00` turn.
    - Reuse rule: re-read before acting.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading rule and capture-spine auto-load rule.
    - Load-bearing: yes.
    - Compare target: header scope starts "Source-loading budgets"; read `2026-06-28`.
    - Last checked: `2026-06-28T01:14:24.9718781+08:00` turn.
    - Reuse rule: re-read before source-pack decisions.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted artifact folders.
    - Load-bearing: yes.
    - Compare target: lists `docs/workflows/` and `docs/review-outputs/` as accepted folders.
    - Last checked: `2026-06-28T01:14:24.9718781+08:00` turn.
    - Reuse rule: re-read before writing the audit report.
- User constraints:
  - Current user asked to parallelize a separate data-lake lane focused on confirming capture-spine runners dump data into the lake appropriately.
  - Load-bearing: yes.
  - Compare target: current chat instruction; reread-required.
- Source-read ledger:
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
    - Role: Capture Spine navigation map.
    - Load-bearing: yes.
    - Compare target: file size `43304`, mtime UTC `2026-06-21T16:31:13.1705949Z`.
    - Last checked: `2026-06-28`.
    - Reuse rule: re-read relevant Fast Route and Harness Implementation sections.
  - `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
    - Role: capture-method playbook; non-authorizing doctrine.
    - Load-bearing: yes.
    - Compare target: file size `24611`, mtime UTC `2026-06-21T16:31:13.1972349Z`.
    - Last checked: `2026-06-28`.
    - Reuse rule: re-read before capture-spine route claims.
  - `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
    - Role: recon index for source capture evidence.
    - Load-bearing: no for runner audit; context only unless source-family claims enter the report.
    - Compare target: file size `25067`, mtime UTC `2026-06-22T09:13:27.0004197Z`.
    - Last checked: `2026-06-28`.
    - Reuse rule: optional context only.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
    - Role: derived/index rebuild authority.
    - Load-bearing: yes.
    - Compare target: file size `10557`, mtime UTC `2026-06-21T08:46:40.5126897Z`.
    - Last checked: `2026-06-28`.
    - Reuse rule: re-read before index/rebuildability claims.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
    - Role: current Silver Vault draft in neighboring lane.
    - Load-bearing: no for audit output, yes for drift guard.
    - Compare target: file size `18684`, mtime UTC `2026-06-27T17:03:54.4287899Z`; untracked.
    - Last checked: `2026-06-28`.
    - Reuse rule: do not edit in this lane.
  - `orca-harness/data_lake/root.py`
    - Role: DataLakeRoot implementation.
    - Load-bearing: yes.
    - Compare target: file size `33265`, mtime UTC `2026-06-21T19:01:37.2681043Z`; grep showed `raw_path`: `raw/{packet_id}` at line 202 and `manifest_relpath`: `raw/{packet_id}/manifest.json` at line 203.
    - Last checked: `2026-06-28`.
    - Reuse rule: re-open exact lines before claiming mismatch.
  - `orca-harness/source_capture/writer.py`
    - Role: shared Source Capture packet writer.
    - Load-bearing: yes.
    - Compare target: file size `14306`, mtime UTC `2026-06-21T12:14:44.3072679Z`; grep showed `stage_raw_packet` line 105, `publish_raw_packet` line 209, `record_availability` line 212.
    - Last checked: `2026-06-28`.
    - Reuse rule: re-open exact writer flow before scoring runners.
  - `F:\orca-data-lake`
    - Role: observed live external data root.
    - Load-bearing: yes for physical-state observations only.
    - Compare target: root marker has `root_uuid` `01KW1E6N133JT0XCN2KCN0V5A4`; observed counts raw manifests `241`, derived files `343`, availability files `241`, derived_retrieval files `0`; sample availability `raw_path` was `raw/67c/01KW4FKEA9ETHA7MRXWVS2MQ6C`.
    - Last checked: `2026-06-28T01:14:24.9718781+08:00` turn.
    - Reuse rule: read-only only; re-run counts before claiming current state.
- Source gaps:
  - Exact origin of live sharded root is not known from this packet.
  - Whether branch code is stale relative to another worktree or uncommitted runner is not known.
  - No live runner execution was performed in this lane.
- Strict-only blockers:
  - Implementation patch needs explicit bounded implementation authorization in the current turn or accepted handoff.
  - Writing to `F:\orca-data-lake` needs explicit owner/tool approval and is outside the read-only audit.
- Not-proven boundaries:
  - Not proven that current code produced all live lake packets.
  - Not proven that live sharded layout is the final accepted contract.
  - Not proven that every `run_source_capture_*` file is intended to write a lake packet.

## Current Task State

- Completed:
  - Current live lake inspected read-only.
  - Raw/derived/index counts observed.
  - Runner surface scanned for data-root support.
  - Handoff packet created for a parallel read-only audit lane.
- Partially completed:
  - Silver Vault draft exists and includes medallion label map, but still needs physical sharding reconciliation.
  - Runner scan is preliminary; it is not a full audit.
- Broken or uncertain:
  - Live lake availability is sharded, but current `DataLakeRoot` code/tests still show unsharded raw path literals.
  - Many `run_source_capture_*` runners appear local-output only by grep, but the receiver must verify if they call an abstraction not caught by grep.

## Workspace State

- Branch: `codex/ig-reels-capture-spine`
- Head: `20e0f42855579ab499c8793e49dfadb61e363eea`
- Dirty or untracked state before handoff:
  - Untracked examples included `.codex/hooks/run_orca_guard.py`, `_scratch/`, several `docs/hygiene/*_handoff_v0.md`, several `docs/prompts/*`, `docs/workflows/data_lake_r2_continuation_handoff_v0.md`, `docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md`, `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`, and `worktrees/`. # nonresolving: the untracked r2-continuation packet named here was never committed on any branch
- Dirty or untracked state after writing the handoff file:
  - This packet adds one new untracked file: `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`.
- Target files or artifacts:
  - Audit report target to be chosen by receiver, recommended under `docs/review-outputs/`.
- Related worktrees or branches:
  - Several `worktrees/` entries exist; do not treat them as current authority without explicitly entering and verifying them.

## Changed / Inspected / Tested Files

- `docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md`
  - Status: newly created handoff packet.
  - Role: cold-lane continuation state.
  - Important observations: not validation or readiness evidence.
  - Symbols or sections: all sections in this packet.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - Status: untracked draft in current lane.
  - Role: neighboring Silver Vault contract.
  - Important observations: should not be edited by audit lane.
  - Symbols or sections: medallion map, generated read model rules, Creator Vault guardrails.
- `orca-harness/data_lake/root.py`
  - Status: inspected by grep.
  - Role: data-lake root implementation.
  - Important observations: grep found unsharded `raw/{packet_id}` availability literals; verify exact code before reporting as defect.
  - Symbols or sections: `DataLakeRoot`, `stage_raw_packet`, `publish_raw_packet`, `record_availability`.
- `orca-harness/source_capture/writer.py`
  - Status: inspected by grep.
  - Role: shared packet writer.
  - Important observations: stages, publishes, and records availability when given `data_root`.
  - Symbols or sections: `write_capture_packet`.
- `orca-harness/runners/`
  - Status: preliminary grep matrix only.
  - Role: runner surface under audit.
  - Important observations: only `run_source_capture_packet.py`, `run_source_capture_http_packet.py`, and `run_source_capture_ig_reels_grid_packet.py` clearly mentioned `DataLakeRoot`/`ORCA_DATA_ROOT` in the preliminary scan; many other `run_source_capture_*` files showed `--output` only.
  - Symbols or sections: runner CLIs and data-root option handling.
- Tests:
  - Status: not run.
  - Reason: handoff authoring only; receiver must run targeted tests if auditing behavior or proposing patches.

## Frozen Decisions

- Decision: This handoff lane is read-only audit first.
  - Evidence: User asked to parallelize a separate data-lake confirmation lane; current project rules require explicit bounded implementation authorization for runtime work.
  - Consequence: Receiver reports findings and patch plan, then stops before implementation unless explicitly authorized.
- Decision: Audit scope includes all intended packet writers, not every runner.
  - Evidence: Projection, screening, quality, bootstrap, and register runners may not emit Source Capture Packets.
  - Consequence: Receiver must classify runner intent before scoring lake compliance.
- Decision: Live-lake sharding is a first-class audit item.
  - Evidence: Observed sample availability `raw_path` is `raw/67c/01KW4FKEA9ETHA7MRXWVS2MQ6C`; current code grep showed unsharded raw path literals.
  - Consequence: Do not let tests pass on unsharded assumptions without addressing the live root mismatch.

## Mutable Questions

- Question: Is the live sharded root produced by a newer writer, a different branch/worktree, or manual migration?
  - Why still mutable: Current branch code inspected by grep appears unsharded.
  - What would resolve it: Git/worktree search for sharding writer, recent commits, or a root writer provenance receipt.
- Question: Should all packet runners gain lake commit support now, or should only the main generic/HTTP/IG-grid paths support it until physical sharding is reconciled?
  - Why still mutable: Broad patching may be a high-churn implementation pass.
  - What would resolve it: Audit severity matrix plus owner authorization.
- Question: Which writer or branch produced the current sharded root, and how should current code catch up to v4.1 sharded `raw/<packet_shard>/<packet_id>/`?
  - Why still mutable: live root and current code/docs disagree; v4.1 gives the forward target but implementation has not caught up.
  - What would resolve it: v4.1 DataLakeRoot/runner implementation plus tests that write/read the forward raw/derived/index refs.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "raw is physically `raw/<packet_id>`" as an unqualified claim.
  - Why stale or dangerous: Live root sample shows `raw/<shard>/<packet_id>`.
  - Current replacement: Say "logical slot is `raw/`; v4.1 forward physical root is sharded as `raw/<packet_shard>/<packet_id>/`; code must be reconciled."
- Stale instruction, idea, artifact, or finding: "All `run_source_capture_*` runners already dump to the lake."
  - Why stale or dangerous: Preliminary scan found many source-capture runners with required `--output` and no apparent `DataLakeRoot` mention.
  - Current replacement: Verify per runner and classify intended writer status.
- Stale instruction, idea, artifact, or finding: "Derived retrieval exists already."
  - Why stale or dangerous: Live root observed `indexes/derived_retrieval` file count `0`.
  - Current replacement: Existing derived records exist, but retrieval/read models are not populated.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch; git rev-parse --abbrev-ref HEAD; git rev-parse HEAD
  ```
  Result:
  - Passed.
  - Important output: branch `codex/ig-reels-capture-spine`; head `20e0f42855579ab499c8793e49dfadb61e363eea`; many untracked files.
  - Re-run target so the receiver can confirm rather than trust: run exactly the command above.
- Command:
  ```powershell
  Get-ChildItem F:\orca-data-lake\raw -Recurse -Filter manifest.json -File
  ```
  Result:
  - Passed read-only.
  - Important output: `241` raw manifests.
  - Re-run target so the receiver can confirm rather than trust: repeat count command.
- Command:
  ```powershell
  Get-ChildItem F:\orca-data-lake\derived -Recurse -File
  ```
  Result:
  - Passed read-only.
  - Important output: `343` derived files.
  - Re-run target so the receiver can confirm rather than trust: repeat count command.
- Command:
  ```powershell
  Get-ChildItem F:\orca-data-lake\indexes\availability -File
  ```
  Result:
  - Passed read-only.
  - Important output: `241` availability files; sample entry used sharded `raw_path`.
  - Re-run target so the receiver can confirm rather than trust: read the newest availability file.
- Command:
  ```powershell
  Select-String -Path orca-harness\data_lake\root.py -Pattern 'raw_path|manifest_relpath|stage_raw_packet|publish_raw_packet'
  ```
  Result:
  - Passed.
  - Important output: grep found unsharded availability literals and staging/publish functions.
  - Re-run target so the receiver can confirm rather than trust: open the exact lines in `root.py`.
- Command:
  ```powershell
  Get-ChildItem orca-harness\runners -Filter *.py
  ```
  Result:
  - Passed.
  - Important output: preliminary table showed only three source-capture packet runners clearly mention data-root support by grep.
  - Re-run target so the receiver can confirm rather than trust: rebuild the matrix from source, not from this packet.

## Blockers And Risks

- Blocker or risk: Live root/code path mismatch.
  - Evidence: live availability sample has `raw/67c/<packet_id>`; `root.py` grep has `raw/{packet_id}`.
  - Likely next action: find the writer/migration that produced sharded root, or update code/tests/contract together under a bounded patch.
- Blocker or risk: Runner intent ambiguity.
  - Evidence: `run_source_capture_durability_series.py` emits multiple packet-like observation directories but preliminary grep did not show data-root support.
  - Likely next action: classify each runner by actual packet output semantics before requiring lake support.
- Blocker or risk: Implementation scope creep.
  - Evidence: Adding data-root support to many runners can touch CLI behavior, tests, and data-lake writer semantics.
  - Likely next action: report gap matrix first, then patch only the smallest complete set.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Current branch/head/dirty state.
  - Current live root counts and sharded availability sample.
  - `DataLakeRoot` raw path behavior in current code.
  - Shared writer staging/publish/availability behavior.
  - Which runners are intended packet writers.
  - Which packet writers support `--data-root` / `ORCA_DATA_ROOT`.
  - Test coverage for each packet writer's lake path.
- Compare target for each:
  - Git commands for branch/head/dirty.
  - `F:\orca-data-lake\.orca-data-root` and availability sample.
  - Exact `root.py` and `writer.py` lines.
  - Runner source files and tests.
- Load outcomes and what each means:
  - `REUSE`: all facts reverified; start audit matrix.
  - `PARTIAL_REUSE`: optional context drifted; rederive matrix and continue.
  - `STALE_REREAD_REQUIRED`: branch, live root, or runner code drifted; reread before reporting.
  - `BLOCKED_DRIFT`: current worktree changes conflict with audit target or unknown edits.
  - `BLOCKED_UNVERIFIABLE`: live root or source files unavailable and claims cannot be rederived.
- Sources that must be reread if drift is detected:
  - `orca-harness/data_lake/root.py`
  - `orca-harness/source_capture/writer.py`
  - `orca-harness/runners/*.py`
  - `orca-harness/tests/**/*data_lake*`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`

## Do Not Forget

The audit lane should preserve failure visibility. If a runner only writes `--output`, report that as a gap or intentional local-output runner; do not paper over it by saying "the writer can do it" unless the runner actually exposes the v4.1 lake path and writes v4.1-compatible refs.
