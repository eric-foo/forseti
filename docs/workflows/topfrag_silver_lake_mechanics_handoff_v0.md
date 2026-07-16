# TopFrag Silver-Lake Mechanics Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: workflow handoff packet
scope: >
  Cold-lane handoff for testing Forseti TikTok Silver/Vault mechanics against
  the completed TopFrag eight-video creator-onboarding staging set.
use_when:
  - Starting the isolated TopFrag silver-lake mechanics test lane.
authority_boundary: retrieval_only
stale_if:
  - branch codex/topfrag-silver-lake-mechanics no longer descends from c776a493ab291187a01cd18ef561f61e6dd82c3e
  - any pinned TopFrag staging artifact hash changes
  - TikTok silver producer or Silver Vault contracts change before load
```

## Load Contract

- packet_version: 0
- mode: max
- created_at: 2026-07-12 Asia/Singapore
- created_by_lane: creator-onboarding sender lane; provenance only
- workspace: `C:\tmp\forseti-topfrag-silver-lake`
- handoff_path: `docs/workflows/topfrag_silver_lake_mechanics_handoff_v0.md`
- expected_branch: `codex/topfrag-silver-lake-mechanics`
- expected_head: branch tip must contain this packet and descend from `c776a493ab291187a01cd18ef561f61e6dd82c3e`
- expected_dirty_state_including_handoff_file: clean after the packet commit
- load_rule: confirm-don't-trust; re-verify every load-bearing fact before acting

## Goal Handoff

Terminology note (2026-07-14): this packet's historical “Silver mechanics”
shorthand means record integrity, lineage, idempotency/supersession, and reader
selection. It does not classify Projection, ECR, Cleaning audit artifacts, or
scratch analytics as Silver Authority. Current work should use the Silver/Vault
contract's Silver Authority and Silver Retrieval terms.

- long_term_goal: Make creator capture usable through a trustworthy, lineage-closed Forseti Silver read layer.
- anchor_goal: Exercise the existing TikTok Silver producer and reader mechanics against TopFrag's completed eight-video staging evidence in an isolated scratch lake.
- success_signal: All eight selected videos can be deterministically represented or explicitly rejected by the Silver mechanics, with raw anchors, policy fingerprints, reader selection, idempotency/supersession behavior, and residuals verified without mutating the live lake or Creator Registry.

## Open Decision / Fork

- decision: How far should this test proceed after the scratch-lake mechanics are proven?
  - options:
    - stop with a verified scratch-lake report;
    - patch a confirmed bounded Silver producer/reader defect and open a PR;
    - request owner authorization for a later live-lake write.
  - already constrained / off the table: no live/prod lake write, no Creator Registry mutation, and no new source capture in this lane.
  - trade-offs: scratch proves mechanics safely; live write proves integration but is externally stateful and requires new owner authorization.
  - owner of the call: receiving agent owns scratch mechanics and bounded repo fixes; user owns any live-lake write.
  - recommendation and why: prove scratch mechanics first and stop unless a confirmed repo defect requires a bounded patch.

## Drift Guard

- Do not open TikTok, recapture TopFrag, solve challenges, or modify capture cadence.
  - why it matters: this lane consumes already captured evidence; it is not another source-access lane.
  - what violating it would break: footprint and lane separation.
- Do not write to the machine's live Forseti data root or legacy Orca root.
  - why it matters: the user requested a mechanics test, not production mutation.
  - what violating it would break: reversible scratch-only test boundary.
- Do not mutate Creator Registry, infer private identity/contact data, or create Gold/Judgment claims.
  - why it matters: Silver is a mechanical derived/read layer, not registry or Judgment truth.
  - what violating it would break: product and epistemic boundaries.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `forseti-harness/capture_spine/creator_profile_current/tiktok_silver_metric_producer.py`
  - `forseti-harness/runners/run_tiktok_batch_metric_rollup_producer.py`
  - `forseti-harness/data_lake/silver_record.py`
  - `forseti-harness/data_lake/silver_lineage.py`
  - `forseti-harness/capture_spine/creator_profile_current/silver_metric_reader.py`
  - `forseti-harness/tests/unit/test_tiktok_creator_metric_silver_producer.py`
  - `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `docs/decisions/silver_vault_goal_frame_ratification_v0.md`
- already loaded: sender inspected only search results and artifact receipts; weak orientation, not authority.
- must load first: `AGENTS.md`, overlay README/source-loading, Silver goal/contract, TikTok producer/runner/tests, then the pinned staging artifacts.
- load rule: rerun progressive source loading; this packet only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Silver is the trustworthy mechanical read layer: lineage-anchored, policy-fingerprinted, explicit about supersession and residuals.
  - decided in: `docs/decisions/silver_vault_goal_frame_ratification_v0.md`
  - compare target: reread-required
  - verify before: making any Silver readiness or record-shape claim
- The TopFrag capture set is staging-only and must not be treated as Creator Registry truth.
  - decided in: the three pinned cadence receipts and original onboarding receipt
  - compare target: hashes below
  - verify before: deriving or describing Silver outputs

## Active Objective

Test the existing TikTok Silver production, lineage, idempotency/supersession,
and reader-selection mechanics using the complete TopFrag eight-video staging
set in an isolated scratch data root. Patch only confirmed bounded defects.

## Exact Next Authorized Action

1. Confirm branch/ancestry, clean state, packet readability, and every pinned staging hash.
2. Read the Silver/Vault contract, TikTok silver producer/runner, lineage front door, reader, and focused tests in full.
3. Determine the existing supported input seam for the three cadence receipts plus the frozen grid/selection; do not invent a new format if an existing batch seam works.
4. Run the producer in an isolated temporary/scratch data root and verify record count, subject identity, raw-anchor lineage, policy fingerprint, durable hashes, idempotent rerun, supersession behavior, and reader selection.
5. If a confirmed repo defect blocks the mechanics, apply the smallest complete patch with focused red/green tests. Otherwise write a durable test report. Do not write to the live lake.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`
- Overlay authority: `.agents/workflow-overlay/README.md`
- User constraints: test silver mechanics with TopFrag in a separate lane; live-lake mutation not granted.
- Source-read ledger:
  - `C:\tmp\topfrag-onboarding-proper-20260712-v1\tiktok_grid_window.json`
    - Role: frozen 32-video grid window
    - Load-bearing: yes
    - Compare target: SHA256 `4804CEAC143F83DD9AC61A22B59D4F2027A84118DEB5618181DD2A4ABC43E97C`
    - Last checked: 2026-07-12
    - Reuse rule: hash must match
  - `C:\tmp\topfrag-onboarding-proper-20260712-v1\tiktok_grid_video_selection.json`
    - Role: selected top-eight order and policy receipt
    - Load-bearing: yes
    - Compare target: SHA256 `7986567F5C863923EA874B26486D95A48739C619B4E05BBC500991E720A816F1`
    - Last checked: 2026-07-12
    - Reuse rule: hash must match
  - `C:\tmp\topfrag-onboarding-transcript-backfill-20260712-v4\tiktok_live_cadence_result.json`
    - Role: completed captures for selected videos 1-5, including comments and transcripts
    - Load-bearing: yes
    - Compare target: SHA256 `E5A5895D4924CF8E74222F8CC0C0E261291D325B8E43FED3EFBEA90307ED0295`
    - Last checked: 2026-07-12
    - Reuse rule: hash must match
  - `C:\tmp\topfrag-onboarding-partial-20260712-v3\tiktok_live_cadence_result.json`
    - Role: completed capture for selected video 6, including comments and transcript
    - Load-bearing: yes
    - Compare target: SHA256 `7751E9F4916B88FF4F5E1834BFA93F9A74C5A707636000BC17B650D20C50D680`
    - Last checked: 2026-07-12
    - Reuse rule: hash must match
  - `C:\tmp\topfrag-onboarding-recovery-20260712-v2\tiktok_live_cadence_result.json`
    - Role: completed captures for selected videos 7-8, including comments and transcripts; also contains an earlier failed attempt for video 6
    - Load-bearing: yes
    - Compare target: SHA256 `7673DA9253B8ED744548E291B596BE6B17AE01BAFF4F7B55B46729CD52BFEF08`
    - Last checked: 2026-07-12
    - Reuse rule: use only the two completed rows; video 6's later v3 completion supersedes its failed v2 attempt
- Source gaps: exact supported multi-receipt Silver input seam must be re-derived from current code.
- Strict-only blockers: any hash mismatch, missing staging file, live-root-only producer requirement, or ambiguous subject identity.
- Not-proven boundaries: not live-lake readiness, not Creator Registry readiness, not Gold/Judgment validity.

## Current Task State

- Completed: TopFrag 32-video window frozen; top eight selected; all eight have staged comments and transcripts across v4/v3/v2 receipts.
- Partially completed: fresh suggested-account View All attempt was blocked/empty; irrelevant to this Silver metric mechanics test.
- Broken or uncertain: no consolidated eight-video cadence file exists; the receiver must use an existing supported multi-input seam or stop rather than hand-merge silently.

## Workspace State

- Branch: `codex/topfrag-silver-lake-mechanics`
- Head: required ancestry `c776a493ab291187a01cd18ef561f61e6dd82c3e` plus this packet commit
- Dirty or untracked state before handoff: clean before packet creation
- Dirty or untracked state after writing the handoff file: packet staged/committed before dispatch; receiver must confirm clean
- Target files or artifacts: packet, pinned TopFrag staging inputs, Silver producer/reader sources
- Related worktrees or branches: creator-onboarding work is already merged through PR #885; do not modify that lane

## Changed / Inspected / Tested Files

- `docs/workflows/topfrag_silver_lake_mechanics_handoff_v0.md`
  - Status: new handoff packet
  - Role: cold-lane continuation state
  - Important observations: scratch-only mechanics test; no live-lake authority
- Silver producer/reader files
  - Status: not yet read in full or changed
  - Role: receiving lane targets
  - Important observations: must be source-loaded before claims

## Frozen Decisions

- Decision: use TopFrag's eight selected videos; do not rerank or recapture.
  - Evidence: pinned grid and selection receipts.
  - Consequence: Silver test scope is fixed.
- Decision: scratch data root only.
  - Evidence: current user requested a mechanics test, not live mutation.
  - Consequence: any live-root requirement is a blocker/owner decision.
- Decision: v3 supersedes the failed video-6 attempt in v2; v2 remains authoritative for its two completed later videos.
  - Evidence: staged receipt outcomes and hashes.
  - Consequence: do not double-count video 6.

## Mutable Questions

- Question: Does the existing TikTok silver runner accept multiple cadence receipts directly?
  - Why still mutable: sender did not inspect the runner in full.
  - What would resolve it: source-load runner/producer/tests.
- Question: Is a bounded patch needed for multi-receipt discovery or partial/superseded input handling?
  - Why still mutable: only real execution can expose it.
  - What would resolve it: scratch producer run plus focused tests.

## Superseded / Dangerous-To-Reuse Context

- The original onboarding receipt reports only five completed captures.
  - Why stale or dangerous: later v2/v3/v4 recovery/backfill receipts complete all eight.
  - Current replacement: use v4 for videos 1-5, v3 for video 6, and the two completed v2 rows for videos 7-8.
- Any legacy Orca data-root environment variable or path.
  - Why stale or dangerous: this is Forseti and live-root mutation is not authorized.
  - Current replacement: explicit isolated scratch root only.

## Commands And Verification Evidence

- Command: focused capture unit suites and contract suites were run in the sender lane.
  Result:
  - Passed: yes, but this is prior-thread evidence only.
  - Re-run target: receiver runs Silver-specific producer/reader tests; do not inherit capture validation as Silver validation.

## Blockers And Risks

- Risk: multiple staging receipts may lack an existing consolidation seam.
  - Evidence: no consolidated eight-video cadence file exists.
  - Likely next action: use a supported multi-input producer seam or stop and patch only if the gap is confirmed.
- Risk: accidentally writing to a live root.
  - Evidence: Silver runners may accept explicit data roots.
  - Likely next action: bind a temporary root and assert its resolved path before execution.

## Confirm-Don't-Trust Load Checklist

- Re-verify branch ancestry, clean state, packet path, five artifact hashes, and source file existence.
- Reread Silver goal/contract and producer/reader code before strict claims.
- `REUSE`: all load-bearing facts match; start the exact next action.
- `PARTIAL_REUSE`: only non-load-bearing context drifted.
- `STALE_REREAD_REQUIRED`: code/head drift can be safely reread.
- `BLOCKED_DRIFT`: branch, authority, dirty state, or artifact hashes conflict.
- `BLOCKED_MISSING_PACKET`: this packet is absent.
- `BLOCKED_UNVERIFIABLE`: a required source/input cannot be checked.

## Do Not Forget

- The lane tests Silver mechanics; it does not recapture, mutate registry, or write the live lake.
