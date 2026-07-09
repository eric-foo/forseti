# Forseti Data Lake Rename And Creator Scanner Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: workflow handoff packet
scope: >
  Cold-lane handoff for renaming the populated external data lake from the
  legacy F:\orca-data-lake physical path to F:\forseti-data-lake, then batching
  creator-scanner hardening, registry preflight, and onboarding capture strategy.
use_when:
  - Continuing the physical data-lake rename work in a fresh lane.
  - Planning scanner runner hardening after the Charlie Frags TikTok scan miss.
  - Deciding the next creator onboarding batch depth after registry preflight.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: handoff_v0
- mode: max
- created_at: 2026-07-10T01:45:07+08:00
- created_by_lane: Codex lane in `C:\Users\vmon7\.codex\worktrees\9881\orca`
- workspace: `C:\Users\vmon7\.codex\worktrees\9881\orca`
- handoff_path: `docs/workflows/forseti_data_lake_rename_and_creator_scanner_handoff_v0.md`
- expected_branch: `origin/codex/forseti-data-lake-rename-handoff`
- expected_head: `reread-required`; fetch the branch and verify the remote ref before acting because this packet is committed on its own retrieval branch.
- expected_dirty_state_including_handoff_file: before this handoff, `git status --short --branch` showed branch tracking `origin/codex/tiktok-charlie-frags-scan`, untracked `_scratch/`, and permission-denied warnings for `pytest-cache-files-kpj82v99/`, `pytest-cache-files-v9c1b3mh/`, and `tmp1bgdt18q/`. After this handoff is written, this file is also untracked or modified until committed by an authorized lane.
- load_rule: confirm-don't-trust. Re-verify every load-bearing fact against its compare target before acting. This packet is orientation, not authority, validation, or live-filesystem authorization.

## Goal Handoff

- long_term_goal: Make Forseti creator scanning and data-lake operations reliable enough that cold agents can run safe, complete scans without silently missing browser sessions, link hubs, lake writes, registry preflight, or routine-scan storage boundaries.
- anchor_goal: Plan the lake physical rename and the creator-scanner batching sequence so the next lane can safely execute the smallest complete work units in order.
- success_signal: The receiving lane produces either a verified live-rename plan awaiting owner approval, or owner-approved patches/execution with no duplicate live roots, no ad hoc lake writes, no routine scan PR churn, and a scanner flow that captures TikTok parent grid, suggested graph, link hub siblings, region evidence, and registry preflight before onboarding.

## Open Decision / Fork

- decision: How to make `F:\forseti-data-lake` the primary populated lake while deprecating `F:\orca-data-lake`.
  - options:
    - Recommended: same-volume rename `F:\orca-data-lake` to `F:\forseti-data-lake`, promote primary `.forseti-*` markers while preserving the existing root UUID, configure `FORSETI_DATA_ROOT`, and leave the old path absent or as a tombstone without a valid root marker.
    - Downgraded: copy/sync to `F:\forseti-data-lake` and keep `F:\orca-data-lake` live. This creates duplicate writable roots and identity drift risk.
    - Rejected unless a later review proves otherwise: junction/symlink from old path to new path. `DataLakeRoot._within()` rejects symlinked components under the root, and an alias keeps the deprecated path behaviorally alive.
  - already constrained / off the table:
    - Do not mutate or rename the live external lake without explicit current owner approval for that protected filesystem action.
    - Do not leave two writable roots.
    - Do not treat historical `F:\orca-data-lake` evidence paths as current root authority.
  - trade-offs:
    - Rename plus tombstone makes the break obvious and lowers split-brain risk, but old absolute historical paths stop resolving directly.
    - Copy/sync is less disruptive short term, but materially increases future confusion and stale writes.
  - owner of the call: user/operator.
  - recommendation and why: use rename plus primary marker promotion and old-path tombstone. It matches the user's stated long-term preference and minimizes duplicate-root risk.

- decision: How deep creator onboarding capture should go after registry preflight.
  - options:
    - Scan-only: capture TikTok parent grid, suggestions, bio/link hub, sibling handles, region evidence, and preflight. Fastest and safest; not enough for onboarding quality.
    - Shallow onboarding batch: after preflight, rank candidates and capture grid-level packets for the top 20-25 percent only. Recommended first batch.
    - Deep capture all grid videos for every candidate: expensive and likely wasteful; only justified after ranking or event-triggered breakout evidence.
  - already constrained / off the table:
    - Top 20-25 percent is an onboarding cap, not a daily monitoring trigger.
    - No private identity/contact enrichment.
    - No bot evasion, proxy rotation, captcha solving, or standing crawler.
  - trade-offs:
    - Deep capture gives better evidence but can dominate runtime and token budget.
    - Grid capture plus link hub/preflight gives enough structure to rank before spending deep-capture budget.
  - owner of the call: user/operator.
  - recommendation and why: run preflight and grid capture first, rank, then deep-capture only the selected top slice or event-triggered breakouts.

## Drift Guard

- invariant, non-goal, or scope boundary: `F:\forseti-data-lake` should become the one current primary root, not a second root beside `F:\orca-data-lake`.
  - why it matters: two live roots create split-brain raw truth, stale tests, stale absolute paths, and false registry/capture claims.
  - what violating it would break: DataLakeRoot identity assumptions, live-lake tests, packet retrieval, and operator trust.
- invariant, non-goal, or scope boundary: routine creator scans should write lake/operational outputs, not open a PR per scan.
  - why it matters: per-scan PRs turn operating work into repo churn and block fast scouting.
  - what violating it would break: review queue hygiene and the distinction between raw observations and schema/code/doctrine changes.
- invariant, non-goal, or scope boundary: a visible TikTok bio link hub must be captured or explicitly blocked/deferred before scanner closeout.
  - why it matters: Charlie Frags had a Linktree and the prior scan silently skipped sibling-channel graphing.
  - what violating it would break: cross-platform creator graph completeness and registry candidate quality.
- invariant, non-goal, or scope boundary: registry mutation needs current exact-match preflight and explicit registry-write authorization.
  - why it matters: opening a TikTok profile proves an account exists, not that it is a new canonical creator row or duplicate-free.
  - what violating it would break: Creator Registry dedupe and public-handle linkage boundaries.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: read `AGENTS.md` and `.agents/workflow-overlay/README.md` before repo work; use `.agents/workflow-overlay/decision-routing.md` for doctrine/code/lane-routing work.
- targets to enter the ladder:
  - `forseti-harness/data_lake/root.py`
  - `forseti/product/spines/data_lake/README.md`
  - `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
  - `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/`
  - `forseti-harness/runners/run_creator_registry_match_preflight.py`
- already loaded (weak orientation, not authority):
  - Current branch/head and dirty state listed above.
  - Fresh path checks observed `F:\forseti-data-lake => False`, `F:\orca-data-lake => True`, `F:\orca-data-lake\.orca-data-root => True`.
  - Current legacy root marker observed `root_uuid=01KW7N6ERSVVANCEZ8SD6YW3EQ`, `contract_version=v4.1`, `label=orca-canonical-v4-1`.
- must load first before strict or actionable steps:
  - Re-read root markers and current filesystem state.
  - Re-read `root.py` marker and resolver logic.
  - Re-run `rg` for `F:\orca-data-lake`, `ORCA_DATA_ROOT`, `.orca-data-root`, and `.orca-lake-epoch.json`.
  - Inspect active live-capture processes before any rename.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded set only seeds the ladder.

### Earlier-decided concepts and behaviors

- decision, framing, profile, or convention: Data Lake is Forseti's raw-truth shared-foundation spine; physical root is external and resolved fail-closed.
  - decided in: `forseti/product/spines/data_lake/README.md`
  - compare target: SHA256 `20127D12F4AF1B24E373FDBA5F244EA9DF628F5A61E9C20EF283C71B3C72C018`
  - verify before: any strict claim about lake ownership, capability, or rename shape.
- decision, framing, profile, or convention: `DataLakeRoot.resolve()` prefers `FORSETI_DATA_ROOT`, accepts legacy `ORCA_DATA_ROOT`, reads `.forseti-data-root` before `.orca-data-root`, and reads `.forseti-lake-epoch.json` before `.orca-lake-epoch.json`.
  - decided in: `forseti-harness/data_lake/root.py`
  - compare target: SHA256 `815889C6E2D086A92327194A701462587E8F79B4692EEEADE103F2773F5702CF`
  - verify before: marker promotion, env migration, test expectations, or filesystem rename.
- decision, framing, profile, or convention: Creator Registry match preflight is exact-match enforcement before new social creator/account capture; it is not fuzzy duplicate detection or cross-platform identity proof.
  - decided in: `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
  - compare target: SHA256 `AA98B62AB4021C4A2EF4AAED8F60BDE6089269087709D7EA5A1317B14D05684E`
  - verify before: registry insertion, new-capture handoff, or onboarding batch mutation.
- decision, framing, profile, or convention: TikTok scanning must not silently skip suggested accounts, bio region evidence, or source-visible link hubs when a parent profile is opened.
  - decided in: current user instruction and prior observed Charlie Frags miss; source file enforcement is not yet complete.
  - compare target: reread-required; inspect current `tiktok_creator_discovery_frontier` models/validators before patching.
  - verify before: scanner runner code changes or scan closeout claims.

## Active Objective

Prepare the next lane to handle two coupled workstreams without mixing them: first, safely migrate the physical lake root name to `F:\forseti-data-lake`; second, harden the creator scanner so future TikTok creator runs capture parent grid, suggested graph, source-visible bio/region, Linktree or equivalent sibling handles, data-lake packet pointers, and registry preflight before onboarding decisions.

## Exact Next Authorized Action

1. Start a fresh branch or worktree from current `main` for any repo-changing work. Do not stack rename/scanner changes on the Charlie scan artifact PR branch.
2. Dispatch or emulate three read-only subagents before any live mutation:
   - Lake conflict audit: verify whether `F:\forseti-data-lake` exists, read `F:\orca-data-lake` markers, inspect `.staging`, check root UUID/epoch, and list active processes likely using the lake.
   - Repo reference audit: classify current `orca-data-lake`, `ORCA_DATA_ROOT`, `.orca-*`, and historical evidence references into live config, compatibility, provenance, tests, and stale docs.
   - Scanner contract audit: inspect TikTok frontier models/validators/runners and source-capture writers to propose the smallest code surface for session probe, link-hub outcome, no-routine-PR output, and lake writer integration.
3. Produce a live-rename runbook. Stop for explicit owner approval before renaming, moving, deleting, creating tombstones, or writing live markers.
4. After rename approval, execute with a quiesce window: no live capture, no scanner writes, no process using old root, and a rollback/restoration note.
5. Patch scanner code/doctrine separately: session resolver, visible-link-hub required outcome, lake packet writer use, routine-scan lake-only default, and registry preflight candidate matrix.
6. For creator onboarding: run preflight first, rank candidates, then deep-capture only the selected top 20-25 percent or event-triggered breakouts.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Forseti project instruction entrypoint.
    - Load-bearing: yes.
    - Compare target: SHA256 `0AE058B6E0E3BC75E43C3E93E8A0251A5A777CB5B3E6DC522414AA9AE08BA641`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before repo work.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: SHA256 `049403E4908C3FF5F0562893967897A4F754F2F771B843734D2DBCA57059DB11`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before repo work.
  - `.agents/workflow-overlay/decision-routing.md`
    - Role: Cynefin routing and enforcement-placement principle.
    - Load-bearing: yes.
    - Compare target: SHA256 `688AAC653FCE6AA5DBDD4D5050946509B998B1CAC6421520408E029719895C1E`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before planning or patching.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: accepted artifact folders and data_lake spine placement.
    - Load-bearing: yes.
    - Compare target: SHA256 `A82F24C8290362CA2A07A8D50E107F714127DBDF9B8A4530F6C246E47FA61D44`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before writing durable docs.
- Data lake sources:
  - `forseti/product/spines/data_lake/README.md`
    - Role: lake spine front door.
    - Load-bearing: yes.
    - Compare target: SHA256 `20127D12F4AF1B24E373FDBA5F244EA9DF628F5A61E9C20EF283C71B3C72C018`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before strict lake claims.
  - `forseti-harness/data_lake/root.py`
    - Role: root resolver, markers, and write guard.
    - Load-bearing: yes.
    - Compare target: SHA256 `815889C6E2D086A92327194A701462587E8F79B4692EEEADE103F2773F5702CF`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before rename code or marker work.
  - `F:\orca-data-lake\.orca-data-root`
    - Role: current legacy root marker.
    - Load-bearing: yes.
    - Compare target: SHA256 `C98CA7E4C3DDA6DA4E0F0780E4ABFDDBFA568E4C4F6100AFB35D666283072D78`; observed root_uuid `01KW7N6ERSVVANCEZ8SD6YW3EQ`.
    - Last checked: 2026-07-10.
    - Reuse rule: re-read immediately before any rename.
  - `F:\orca-data-lake\.orca-lake-epoch.json`
    - Role: current legacy epoch marker.
    - Load-bearing: yes.
    - Compare target: SHA256 `95F0EDDD9B6D0C4B151D4058DE7B5D41CD6DA65CDA7C154937920A3CABD19B4E`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read immediately before any rename.
- Creator Registry source:
  - `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
    - Role: exact-match preflight rules.
    - Load-bearing: yes.
    - Compare target: SHA256 `AA98B62AB4021C4A2EF4AAED8F60BDE6089269087709D7EA5A1317B14D05684E`
    - Last checked: 2026-07-10.
    - Reuse rule: re-read before registry mutation or new-capture claims.
- Source gaps:
  - No current process audit has been run for live lake users.
  - No root-size or raw-packet census has been run in this handoff lane.
  - No `F:\forseti-data-lake` marker exists as of the last check; re-check before acting.
  - No scanner runner patch exists yet for link-hub required outcome.
- Strict-only blockers:
  - Live rename is blocked until the user explicitly approves the protected filesystem operation and the receiver verifies no conflicting root/process state.
  - Registry insertion is blocked until exact-match preflight and registry-write authorization are current.
- Not-proven boundaries:
  - This packet does not prove lake health, packet completeness, CI status, creator quality, roster readiness, or metric validity.

## Current Task State

- Completed:
  - Verified `F:\forseti-data-lake` did not exist and `F:\orca-data-lake` did exist during this lane.
  - Read current root marker and epoch marker from `F:\orca-data-lake`.
  - Verified DataLakeRoot code already prefers `FORSETI_DATA_ROOT` and `.forseti-*` markers, with legacy `ORCA_DATA_ROOT` and `.orca-*` fallback.
  - Established scanner miss: Charlie Frags had a visible Linktree; prior frontier scan captured parent TikTok grid and suggestions but did not expand the link hub.
  - Established Creator Registry preflight meaning: exact-match dedupe before new capture; not fuzzy identity proof or registry mutation.
- Partially completed:
  - Charlie Frags TikTok parent grid/suggested scan artifacts were PR'd separately on the current branch, but that PR should not become the routine scanner pattern.
  - Code/doctrine hardening for scanner omissions has been reasoned but not patched in this handoff.
- Broken or uncertain:
  - Physical root still uses legacy path/markers.
  - Many docs and tests still mention old physical path as historical evidence, compatibility, or live root assumptions; not classified in this packet.
  - Scanner has no single first-class runner that owns session resolution, parent grid, suggestions, link hub, lake packet write, and registry preflight.

## Workspace State

- Branch: packet retrieval branch `codex/forseti-data-lake-rename-handoff`; the scan artifacts remain on `codex/tiktok-charlie-frags-scan`.
- Head: `reread-required`; verify the fetched `origin/codex/forseti-data-lake-rename-handoff` ref before acting.
- Dirty or untracked state before handoff:
  - `?? _scratch/`
  - permission denied warnings for `pytest-cache-files-kpj82v99/`, `pytest-cache-files-v9c1b3mh/`, `tmp1bgdt18q/`
- Dirty or untracked state after writing the handoff file:
  - expected additional untracked or modified file: `docs/workflows/forseti_data_lake_rename_and_creator_scanner_handoff_v0.md`
- Target files or artifacts:
  - `forseti-harness/data_lake/root.py`
  - `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/`
  - `forseti-harness/runners/`
  - `forseti/product/spines/capture/core/source_families/social_media/creator_registry/`
  - external root `F:\orca-data-lake`, intended future root `F:\forseti-data-lake`
- Related worktrees or branches:
  - Packet retrieval branch is `codex/forseti-data-lake-rename-handoff`. Do not stack scanner hardening or live-rename execution onto the Charlie scan artifact branch; use a fresh branch/worktree off current `main` for repo-changing implementation.

## Changed / Inspected / Tested Files

- `docs/workflows/forseti_data_lake_rename_and_creator_scanner_handoff_v0.md`
  - Status: added by this handoff.
  - Role: continuation packet only.
  - Important observations: not validation, not live rename authorization.
- `forseti-harness/data_lake/root.py`
  - Status: inspected.
  - Role: resolver/marker/write-boundary code.
  - Important observations: primary env/markers are Forseti; legacy Orca names are fallback compatibility.
- `forseti/product/spines/data_lake/README.md`
  - Status: inspected.
  - Role: Data Lake spine front door.
  - Important observations: data_lake is a shared-foundation spine and raw-truth layer.
- `creator_registry_match_preflight_usage_v0.md`
  - Status: inspected.
  - Role: preflight usage doctrine.
  - Important observations: preflight is exact-match enforcement, not fuzzy duplicate or identity proof.

## Frozen Decisions

- Decision: Physical lake should move toward `F:\forseti-data-lake` as the primary root.
  - Evidence: user explicitly requested the main root become `forseti-data-lake` by renaming the populated root.
  - Consequence: future work should not normalize on `F:\orca-data-lake` as current.
- Decision: Routine scanner runs should not open a PR by default.
  - Evidence: user agreed per-scan PRs are too heavy.
  - Consequence: scanner output defaults to lake/operational registers; repo PRs are for code, schema, doctrine, fixtures, or curated review bundles.
- Decision: Link hub capture must be enforced when visible.
  - Evidence: Charlie Frags miss exposed that doctrine-only behavior did not fire.
  - Consequence: scanner receipt/validator should fail silent link-hub omission.
- Decision: Preflight should be done for creator onboarding.
  - Evidence: user accepted preflight should happen; source doctrine requires it before new social creator/account capture.
  - Consequence: opened TikTok creators become registry candidates only after exact-match preflight and evidence attachment.

## Mutable Questions

- Question: Should the old path become absent, a tombstone folder, or a short-lived compatibility alias?
  - Why still mutable: symlink/junction likely conflicts with guard posture, but old absolute historical paths may become harder to inspect.
  - What would resolve it: conflict-audit subagent plus owner decision after seeing exact impact.
- Question: Should `.orca-*` marker files remain inside the renamed root after primary `.forseti-*` markers are written?
  - Why still mutable: code tolerates legacy fallback, but primary markers should own current identity; duplicate marker files may confuse humans.
  - What would resolve it: root.py/read-code audit and a marker migration plan that preserves root UUID and epoch semantics.
- Question: How many videos per top creator should receive deep capture?
  - Why still mutable: depends on runtime cost, platform sensitivity, and whether grid metrics are enough for initial onboarding.
  - What would resolve it: pilot on a small selected batch after scanner runner hardening.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "There is no controllable TikTok/CloakBrowser session" from the failed handoff attempt.
  - Why stale or dangerous: later CDP probing found the Chowdakr/CloakBrowser-equivalent session at `127.0.0.1:9223`.
  - Current replacement: scanner session resolver must check known CDP endpoints before declaring the browser unavailable.
- Stale instruction, idea, artifact, or finding: treating `F:\orca-data-lake` as the desired long-term current root.
  - Why stale or dangerous: user now wants the primary root renamed to `F:\forseti-data-lake`.
  - Current replacement: use `FORSETI_DATA_ROOT` and primary `.forseti-*` markers after the planned migration.
- Stale instruction, idea, artifact, or finding: "opened creator means registry row is automatically safe."
  - Why stale or dangerous: opened profile proves source visibility, not duplicate-free registry identity.
  - Current replacement: opened profile becomes a candidate; exact-match preflight and evidence routing decide insert/update/stop.

## Commands And Verification Evidence

- Command:
  ```powershell
  git branch --show-current
  ```
  Result:
  - Passed; output `codex/tiktok-charlie-frags-scan`.
  - Re-run target: branch before acting.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed; output `5e934f4079135d346af57361a32dc7381ac1cf1c`.
  - Re-run target: HEAD before acting.
- Command:
  ```powershell
  $paths=@('F:\forseti-data-lake','F:\forseti-data-lake\.forseti-data-root','F:\orca-data-lake','F:\orca-data-lake\.forseti-data-root','F:\orca-data-lake\.orca-data-root'); foreach($p in $paths){ '{0} => {1}' -f $p,(Test-Path -LiteralPath $p) }
  ```
  Result:
  - Passed; observed `F:\forseti-data-lake => False`, `F:\forseti-data-lake\.forseti-data-root => False`, `F:\orca-data-lake => True`, `F:\orca-data-lake\.forseti-data-root => False`, `F:\orca-data-lake\.orca-data-root => True`.
  - Re-run target: immediately before rename.
- Command:
  ```powershell
  Get-Content -Raw 'F:\orca-data-lake\.orca-data-root'
  ```
  Result:
  - Passed; observed contract `v4.1`, label `orca-canonical-v4-1`, root_uuid `01KW7N6ERSVVANCEZ8SD6YW3EQ`.
  - Re-run target: immediately before rename.
- Command:
  ```powershell
  Get-Content -Raw 'F:\orca-data-lake\.orca-lake-epoch.json'
  ```
  Result:
  - Passed; observed `lake_epoch=v4.1`, `epoch_policy=clean_forward_epoch`, `compatibility_migration=false`, legacy root list containing `F:\orca-data-lake-legacy-v0-20260628T174129Z`.
  - Re-run target: immediately before rename.

## Blockers And Risks

- Blocker or risk: live filesystem rename could race active capture or projection processes.
  - Evidence: no process audit was run here.
  - Likely next action: read-only subagent/process audit, then quiesce window before owner-approved rename.
- Blocker or risk: old absolute paths appear across docs/prompts as historical evidence and live-root instructions.
  - Evidence: `rg` returned many `F:\orca-data-lake` and `ORCA_DATA_ROOT` hits.
  - Likely next action: classify references before any mass edit; preserve historical provenance while changing live defaults.
- Blocker or risk: scanner hardening could over-constrain live scouting.
  - Evidence: TikTok/IG are sensitive surfaces; user prefers warmed CloakBrowser/browser behavior.
  - Likely next action: enforce only deterministic omissions: session probe outcome, parent grid packet, suggested status, link-hub outcome, lake writer receipt, registry preflight status.
- Blocker or risk: deep capture too early wastes time and increases platform friction.
  - Evidence: current run already showed many steps per creator.
  - Likely next action: grid/linkhub/preflight first; deep capture top 20-25 percent or event-triggered breakouts only.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Current branch/head and whether work is on a clean branch/worktree off `main`.
  - `F:\forseti-data-lake` existence and marker state.
  - `F:\orca-data-lake` existence, root UUID, epoch marker, and staging state.
  - Active processes/jobs using either root.
  - Current `root.py` resolver and marker logic.
  - Current Creator Registry preflight usage.
  - Current TikTok frontier runner/model/validator fields.
- Compare target for each:
  - Hashes and command outputs recorded above, or `reread-required` where no stable source file exists.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts re-verified; continue with read-only audits and runbook.
  - `PARTIAL_REUSE`: optional context drifted; rederive scanner details before patching.
  - `STALE_REREAD_REQUIRED`: root markers, branch, or runner files changed; re-read before acting.
  - `BLOCKED_DRIFT`: `F:\forseti-data-lake` now exists with conflicting marker/data, old root UUID changed, or active writer cannot be quiesced.
  - `BLOCKED_UNVERIFIABLE`: live root or required source files cannot be read.
- Sources that must be reread if drift is detected:
  - `forseti-harness/data_lake/root.py`
  - `forseti/product/spines/data_lake/README.md`
  - `creator_registry_match_preflight_usage_v0.md`
  - current root marker and epoch files.

## Do Not Forget

- Do not execute the physical rename as part of scanner work. The rename is a protected live-data operation and needs an explicit approval moment.
- Do not create a second writable root.
- Do not use a junction/symlink as the compatibility answer unless root guard behavior is explicitly tested and accepted.
- Do not deep-capture every visible grid video for every discovered creator by default.
- Do not registry-insert Charlie Frags, Top Frag, Archer, or any opened creator without current exact-match preflight and registry-write authorization.
- Do not let the next scanner receipt pass if a visible bio link hub is skipped without a captured/blocked/deferred outcome.
