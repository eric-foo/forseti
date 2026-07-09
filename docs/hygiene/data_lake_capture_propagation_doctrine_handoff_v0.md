# Data Lake Capture Propagation Doctrine Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet
scope: >
  Transfers the emerging need for a Data Lake / capture-lane propagation doctrine
  into a fresh planning lane, separating generic lake/runner mechanics from
  platform-specific behavioral parity.
use_when:
  - Starting a fresh lane to design propagation rules after a YT, IG, runner, or Data Lake change.
  - Deciding whether a source-family change should trigger same-class checks elsewhere.
  - Preventing YouTube-specific capture mechanics from becoming accidental generic doctrine.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/validation-gates.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  - forseti-harness/youtube_capture/behavioral_projection.py # nonresolving: retired or branch-only YouTube projection source; handoff keeps provenance only
stale_if:
  - Data Lake Bronze/Silver/Gold semantics change.
  - SourceCapturePacket runner lake-seam enforcement changes.
  - YouTube or Instagram behavioral projection contracts change.
  - A later accepted propagation doctrine supersedes this handoff.
```

## Load Contract

- packet_version: workflow-handoff max v0
- mode: max
- created_at: 2026-06-29T19:44:53.8107484+08:00
- created_by_lane: current Codex thread, provenance only; not an authority claim
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/hygiene/data_lake_capture_propagation_doctrine_handoff_v0.md`
- expected_branch: start a fresh branch/worktree from `origin/main` for any source-changing work; do not use the current dirty root branch unless the owner explicitly redirects
- expected_head: `origin/main` observed at `e5dfd03dcbfac6137cbb64a9a527d6b9186320c1`
- expected_dirty_state_including_handoff_file: current root checkout is `codex/ig-reels-capture-spine` with many pre-existing untracked files; this handoff file becomes an additional untracked `docs/hygiene/` artifact until staged or removed
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: Keep Orca's Data Lake, capture runners, and platform capture lanes coherent when one lane changes, without forcing identical acquisition machinery across platforms.
- anchor_goal: Design the smallest complete propagation doctrine that tells future agents when a YouTube, Instagram, runner, or Data Lake change requires same-class checks elsewhere.
- success_signal: A fresh lane can classify a change as generic lake/storage, generic packet-runner, platform behavioral parity, platform acquisition-local, or downstream-consumer-facing, then name which sources to inspect or patch without overgeneralizing.

## Open Decision / Fork

- decision: Whether the new rule should be a broad "Data Lake propagation doctrine" or a narrower capture/data-lake propagation classification contract.
  - options:
    - Broad Data Lake propagation doctrine: covers raw/derived storage, runner seams, platform behavior, projection consumers, and maybe Cleaning/Judgment adjacency.
    - Narrow capture/data-lake propagation classification contract: covers only Data Lake slot semantics, SourceCapturePacket runner seams, source-family behavioral parity, and projection-consumer residual handling.
    - No doctrine: keep handling YT/IG/runner propagation ad hoc.
  - already constrained / off the table:
    - Do not force IG, YT, TikTok, or other platforms to share acquisition methods, priority order, packet shape, browser route, API route, transcript route, or source-funnel strategy.
    - Do not apply `--output` / `--data-root` exact-one semantics to every runner; it applies generically only to raw `SourceCapturePacket` acquisition runners.
    - Do not let Silver or projection outputs smuggle Gold/Judgment meaning.
    - Do not patch doctrine or implementation from this handoff alone; re-read controlling sources first.
  - trade-offs:
    - Broad doctrine has better coverage but high drift and overreach risk.
    - Narrow classification is lower lock-in and matches the actual defect pattern: "what kind of change is this, and which peers must be checked?"
    - No doctrine preserves speed now but leaves future YT/IG and runner parity changes dependent on agent memory.
  - owner of the call: Orca owner / current user.
  - recommendation and why: Use the narrower classification contract first. It solves the observed propagation need while preserving platform-specific acquisition exploration.

## Drift Guard

- invariant, non-goal, or scope boundary: Propagate behavioral guarantees and storage/write-boundary rules by class, not source-specific acquisition routes.
  - why it matters: The YT lane deliberately completed behavioral truth contracts without making IG copy YT's served-HTML/caption-first machinery.
  - what violating it would break: It would turn useful YT-specific routes into accidental shared core and increase lock-in.
- invariant, non-goal, or scope boundary: Generic runner enforcement means raw `SourceCapturePacket` producers, not all runners.
  - why it matters: The repo has projection, report, diagnostics, bootstrap, and derived-only runners whose output contracts are intentionally different.
  - what violating it would break: It would create false failures and pressure unrelated runners into the wrong sink model.
- invariant, non-goal, or scope boundary: Bronze/Silver/Gold boundaries remain epistemic boundaries, not just folder names.
  - why it matters: Capture packets are raw evidence; projection and ASR/extraction are Silver; Judgment alone owns Gold meaning.
  - what violating it would break: Engagement facts could become demand, credibility, creator-quality, or action recommendations too early.
- invariant, non-goal, or scope boundary: This handoff is retrieval-only and single-consumption orientation.
  - why it matters: Checkpoint artifacts are not Orca source of truth under `.agents/workflow-overlay/source-of-truth.md`.
  - what violating it would break: A future lane could trust stale branch or doctrine facts from this file instead of re-verifying them.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/validation-gates.md`
  - `.agents/workflow-overlay/safety-rules.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
  - `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - `orca-harness/youtube_capture/behavioral_projection.py`
  - IG behavioral sources selected by the receiver from current `origin/main`; do not rely on this thread's untracked IG note as authority
- already loaded (weak orientation, freshness-marked; not authority):
  - The current thread read the overlay entrypoint, safety, source-loading, validation, source-of-truth, artifact folders, retrieval metadata, YT behavioral projection, YT watch/caption/ASR runners, Data Lake contracts, and packet-runner seam test from `origin/main`.
  - Two read-only subagents returned narrowed context: one generic runner/lake seam summary, one YouTube-specific capture/projection summary. Their outputs are orientation only.
- must load first (before strict or actionable steps):
  - Re-run `git fetch origin`.
  - Confirm `origin/main` HEAD and branch/worktree isolation.
  - Re-read the overlay and Data Lake contracts named above from current `origin/main`.
  - Re-read current YT and IG capture/projection sources before claiming parity gaps or writing a doctrine patch.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Online/external source-data capture routes through Source Capture Armory runners; emitted SourceCapturePackets double as capture-lane data.
  - decided in: `.agents/workflow-overlay/safety-rules.md`
  - compare target: `origin/main` blob `541c073bb96247387f13d5e3d1aa01793148ee17`
  - verify before: any strict claim about capture routing or no-ad-hoc evidence fetches
- decision, framing, profile, or convention: Data Lake owns raw packet preservation and by-key findability; downstream lanes write append-only derived results keyed back to raw.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
  - compare target: `origin/main` blob `e33cdab1bf37693775730e712c3562999690230d`
  - verify before: any strict claim about Data Lake propagation scope
- decision, framing, profile, or convention: Medallion semantics are Bronze raw, Silver mechanical derived, Pre-gold mechanical candidate alerts, Gold-ready decision-bounded assembly, and Gold Judgment-only.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
  - compare target: `origin/main` blob `a3f60ee173961f58dc49740611ce54c213222787`
  - verify before: any strict Bronze/Silver/Gold rule
- decision, framing, profile, or convention: Packet-producing capture runners must carry the Data Lake seam or be explicitly acknowledged as not synced.
  - decided in code/test: `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - compare target: `origin/main` blob `a16fe86583c821ba23af952648df1b00a440fe99`
  - verify before: any code-enforcement or runner-classification claim
- decision, framing, profile, or convention: YouTube behavioral projection is a Silver/read-side view over existing capture inputs and must not acquire network/source data.
  - decided in code/test: `orca-harness/youtube_capture/behavioral_projection.py`
  - compare target: `origin/main` blob `349549f945d22a3d4686bc6b477c32c0a52ab2b5`
  - verify before: any YT projection or YT-to-IG parity claim

## Active Objective

Create a source-backed propagation doctrine proposal for Orca's Data Lake and capture lanes. The proposal should classify which changes propagate generically, which propagate as platform behavioral parity checks, and which stay source-family-local.

## Exact Next Authorized Action

1. Start a fresh read-only or docs-write lane from current `origin/main`; use a worktree if source-changing work will run alongside the dirty IG branch.
2. Re-read the load-bearing sources listed in this packet and classify propagation triggers into at least: Data Lake storage/medallion, raw packet-runner seam, platform behavioral contract, platform acquisition route, and downstream consumer residual semantics.
3. Produce a short doctrine proposal or decision draft naming the controlling home before patching it. Stop for owner steering if the controlling home would be broad overlay doctrine rather than a Data Lake/capture-spine contract.
4. Only after owner acceptance, patch the controlling source with a Direction Change Propagation receipt and run the relevant retrieval/header/map/hygiene gates.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` supplied in current user context; load-bearing for behavior kernel, but receiver should re-read the workspace copy if making source changes.
- Overlay or equivalent authority: `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/validation-gates.md`, `.agents/workflow-overlay/safety-rules.md`.
- User constraints:
  - The user believes cross-lane propagation is becoming necessary when YT changes imply IG checks, or runner mechanics changes imply same-class runner checks.
  - The user asked to use `workflow-handoff`.
  - The user wants to avoid overgeneralizing platform acquisition machinery.
- Source-read ledger:
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: source hierarchy and doctrine-change propagation authority
    - Load-bearing: yes
    - Compare target: `origin/main` blob `fd42a38eb206327ff474fa83a2a5c90165c12a59`
    - Last checked: 2026-06-29
    - Reuse rule: reread before any doctrine-changing patch or strict source-of-truth claim
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading and capture-spine method start-read authority
    - Load-bearing: yes
    - Compare target: `origin/main` blob `6b02b3487ff27147e357df01470d31308fa5da12`
    - Last checked: 2026-06-29
    - Reuse rule: reread before defining source packs or receiver load contract
  - `.agents/workflow-overlay/validation-gates.md`
    - Role: validation and enforcement-placement authority
    - Load-bearing: yes
    - Compare target: `origin/main` blob `890b5afa04308ae0e610dfb750afaf0d0ad87114`
    - Last checked: 2026-06-29
    - Reuse rule: reread before claiming what belongs in code hooks versus resident doctrine
  - `.agents/workflow-overlay/safety-rules.md`
    - Role: capture safety/routing boundary
    - Load-bearing: yes
    - Compare target: `origin/main` blob `541c073bb96247387f13d5e3d1aa01793148ee17`
    - Last checked: 2026-06-29
    - Reuse rule: reread before capture-routing or implementation-authorization claims
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
    - Role: lake responsibility boundary
    - Load-bearing: yes
    - Compare target: `origin/main` blob `e33cdab1bf37693775730e712c3562999690230d`
    - Last checked: 2026-06-29
    - Reuse rule: reread before Data Lake doctrine proposal
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
    - Role: Silver/derived record and Creator Vault boundary
    - Load-bearing: yes
    - Compare target: `origin/main` blob `6551b3d675a80d821173497a84bf8319e2c1418f`
    - Last checked: 2026-06-29
    - Reuse rule: reread before Silver propagation claims
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
    - Role: Bronze/Silver/Gold semantics
    - Load-bearing: yes
    - Compare target: `origin/main` blob `a3f60ee173961f58dc49740611ce54c213222787`
    - Last checked: 2026-06-29
    - Reuse rule: reread before medallion propagation claims
  - `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
    - Role: current generic packet-runner seam enforcement
    - Load-bearing: yes
    - Compare target: `origin/main` blob `a16fe86583c821ba23af952648df1b00a440fe99`
    - Last checked: 2026-06-29
    - Reuse rule: reread before runner-class or code-enforcement claims
  - `orca-harness/youtube_capture/behavioral_projection.py`
    - Role: current YouTube behavioral projection behavior
    - Load-bearing: yes
    - Compare target: `origin/main` blob `349549f945d22a3d4686bc6b477c32c0a52ab2b5`
    - Last checked: 2026-06-29
    - Reuse rule: reread before YT behavioral parity claims
- Source gaps:
  - Current IG behavioral/projection sources were not re-read for this handoff. The receiver must read them from current `origin/main`.
  - `docs/workflows/ig_behavioral_live_validation_enforcement_log_v0.md` exists in the current working tree as untracked orientation, not `origin/main` authority in this checkout.
- Strict-only blockers:
  - No controlling doctrine home has been selected.
  - No owner acceptance yet for the exact propagation doctrine shape.
- Not-proven boundaries:
  - This handoff is not validation, readiness, acceptance, implementation authorization, or a doctrine change.

## Current Task State

- Completed:
  - YouTube capture/projection lane was observed merged into `origin/main` during the current thread.
  - Generic versus YouTube-specific enforcement was separated in chat: generic applies to raw `SourceCapturePacket` acquisition runners; YouTube-specific applies to YT availability, metrics, comments, transcript, and projection residual behavior.
  - Two subagents returned narrowed read-only summaries supporting that split.
- Partially completed:
  - The need for a propagation doctrine was identified but not designed or patched.
- Broken or uncertain:
  - The exact controlling artifact is unresolved. Candidate homes are a Data Lake/capture-spine contract, a workflow overlay rule, or a workflow decision record.

## Workspace State

- Branch: `codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine`
- Head: not re-read by SHA in this handoff; receiver should run `git rev-parse HEAD` if using the dirty root checkout
- Dirty or untracked state before handoff:
  - `.codex/hooks/run_orca_guard.py`
  - `_scratch/`
  - many untracked `docs/hygiene/`, `docs/prompts/`, and `docs/workflows/` artifacts, including `docs/workflows/ig_behavioral_live_validation_enforcement_log_v0.md`
  - `worktrees/`
- Dirty or untracked state after writing the handoff file:
  - all prior untracked entries remain, plus `docs/hygiene/data_lake_capture_propagation_doctrine_handoff_v0.md`
- Target files or artifacts:
  - This handoff file.
  - Future doctrine proposal path not selected.
- Related worktrees or branches:
  - Prior YouTube lane was `codex/youtube-capture-spine-sync`; its PR was reported/observed merged earlier.
  - Current root branch is an IG lane and should not be reused for unrelated doctrine patching without owner direction.

## Changed / Inspected / Tested Files

- `docs/hygiene/data_lake_capture_propagation_doctrine_handoff_v0.md`
  - Status: newly written handoff packet
  - Role: cold-lane continuation artifact
  - Important observations: retrieval-only; not authority
  - Symbols or sections: all sections
- `.agents/workflow-overlay/source-of-truth.md`
  - Status: inspected
  - Role: doctrine propagation and checkpoint lifecycle authority
  - Important observations: checkpoint artifacts are non-authoritative and single-consumption; doctrine-changing edits need Direction Change Propagation receipts
  - Symbols or sections: `Checkpoint Artifacts`, `Doctrine Change Propagation Contract`
- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - Status: inspected from `origin/main`
  - Role: generic packet-runner seam enforcement
  - Important observations: detector targets packet-producing runners and enforces lake seam / output-mode exclusivity
  - Symbols or sections: `test_every_packet_runner_is_lake_wired_or_acknowledged`, `test_packet_runner_output_modes_are_exclusive`
- `orca-harness/youtube_capture/behavioral_projection.py`
  - Status: inspected from `origin/main`
  - Role: YT behavioral projection contract in code
  - Important observations: projection discovers metadata/transcript sources from lake and carries residuals; no acquisition
  - Symbols or sections: `project_youtube_behavioral_item_from_lake`, `transcript_sources_for_video`

## Frozen Decisions

- Decision: Do not generalize YouTube acquisition mechanics to Instagram or all platforms.
  - Evidence: Current user explicitly pushed for exploration and behavior parity, not same acquisition method/priority/shape; YT code uses YT-specific watch/caption/ASR routes.
  - Consequence: Propagation doctrine must classify acquisition-route changes as source-family-local unless a separate core invariant is proven.
- Decision: Generic runner rule applies to raw packet-producing capture runners only.
  - Evidence: `test_capture_runner_lake_seam_coverage.py` detects packet writers, not every runner; current runner census includes projection/report/derived-only exceptions.
  - Consequence: A future doctrine must not say every runner needs `--data-root` and `--output`.
- Decision: Bronze/Silver/Gold must remain epistemic boundaries.
  - Evidence: Data Lake medallion contract.
  - Consequence: Propagation can require residual/metric truth checks but cannot promote engagement or projection facts into Judgment meaning.

## Mutable Questions

- Question: Where should the propagation doctrine live?
  - Why still mutable: It crosses Data Lake architecture, capture-spine workflow, runner enforcement, and platform behavioral parity.
  - What would resolve it: A source-backed proposal that compares candidate homes and owner selects one.
- Question: Which propagation classes become code-enforced?
  - Why still mutable: Some rules are deterministic at runner/projection boundaries; others are judgment-based doctrine.
  - What would resolve it: A per-rule enforcement-placement table using `.agents/workflow-overlay/validation-gates.md`.
- Question: Should the first implementation be a doctrine-only contract, a checker update, or both?
  - Why still mutable: Current packet-runner seam already has a checker; platform behavioral parity likely needs resident doctrine first.
  - What would resolve it: Owner acceptance of the proposed trigger table.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "Every runner should enforce exactly one of `--output` or `--data-root`."
  - Why stale or dangerous: The repo has derived-only, projection, report, diagnostics, and bootstrap runners with different output contracts.
  - Current replacement: Only raw `SourceCapturePacket` acquisition runners inherit that generic sink seam.
- Stale instruction, idea, artifact, or finding: "If YT changes, make the same code change to IG."
  - Why stale or dangerous: YT and IG acquisition methods intentionally differ.
  - Current replacement: If YT changes a behavioral truth contract or consumer-facing residual/completeness contract, trigger an IG parity review; if it changes a YT-only route, do not auto-patch IG.
- Stale instruction, idea, artifact, or finding: "This handoff proves current doctrine state."
  - Why stale or dangerous: Checkpoint artifacts are retrieval-only and can go stale immediately.
  - Current replacement: Receiver must confirm against current `origin/main` and controlling sources.

## Commands And Verification Evidence

- Command:
  ```powershell
  git fetch origin
  ```
  Result:
  - Passed.
  - Important output: `origin/main` advanced earlier in the thread to include the merged YT lane.
  - Re-run target so the receiver can confirm rather than trust: run before starting any fresh lane.
- Command:
  ```powershell
  git rev-parse origin/main
  ```
  Result:
  - Passed.
  - Important output: `e5dfd03dcbfac6137cbb64a9a527d6b9186320c1`
  - Re-run target so the receiver can confirm rather than trust: compare current `origin/main`.
- Command:
  ```powershell
  git ls-tree origin/main <load-bearing paths>
  ```
  Result:
  - Passed for the overlay, Data Lake, YT projection, and packet-runner seam-test paths named in the source ledger.
  - Important output: blob ids recorded in the source ledger.
  - Re-run target so the receiver can confirm rather than trust: re-run with the same paths.
- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed.
  - Important output: root checkout on `codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine` with many untracked files.
  - Re-run target so the receiver can confirm rather than trust: run before deciding whether to write in root or a fresh worktree.

## Blockers And Risks

- Blocker or risk: Controlling doctrine home is not selected.
  - Evidence: The candidate rule spans Data Lake, capture source-family contracts, runner enforcement, and overlay workflow authority.
  - Likely next action: Produce a short proposal comparing candidate homes before patching.
- Blocker or risk: Overgeneralization could force YT acquisition details onto IG/TikTok.
  - Evidence: Current YT-specific states/routes are watch-page, `youtubei_next`, captions, and ASR; current user explicitly wants behavioral parity, not acquisition sameness.
  - Likely next action: Put "acquisition route changes do not propagate automatically" in the drift guard of the proposal.
- Blocker or risk: Under-propagation could leave IG stale after YT truth-contract changes.
  - Evidence: User identified the exact failure mode: changing YT may require checking IG; runner profile/mechanics changes may require checking same-class runners.
  - Likely next action: Define a trigger table.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - `origin/main` HEAD.
  - Overlay authority files and blob ids.
  - Data Lake contracts and blob ids.
  - Packet-runner seam test and current runner landscape.
  - Current YT behavioral projection and current IG behavioral/projection sources.
  - Current dirty state and branch/worktree.
- Compare target for each:
  - Use the blob ids and `origin/main` SHA recorded above, or re-read current `origin/main` and treat drift as `STALE_REREAD_REQUIRED`.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts re-verified; continue with proposal design.
  - `PARTIAL_REUSE`: optional context drifted; re-derive drifted context and continue.
  - `STALE_REREAD_REQUIRED`: source files or `origin/main` drifted; reread before any strict or actionable claim.
  - `BLOCKED_DRIFT`: drift conflicts with owner constraints, target path, or source authority.
  - `BLOCKED_MISSING_PACKET`: this handoff path is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived; stop rather than trust this packet.
- Sources that must be reread if drift is detected:
  - All `open_next` sources in the retrieval header.
  - Current YT and IG capture/projection code from `origin/main`.
  - `docs/workflows/orca_repo_map_v0.md` if selecting a durable doctrine artifact home.

## Do Not Forget

- The real rule is propagation by class: storage mechanics, raw packet-runner seam, platform behavioral parity, acquisition-local details, and downstream consumer semantics.
- Start with a doctrine proposal, not code.
- Use this handoff once, then refresh or delete it per checkpoint lifecycle once the receiving lane re-establishes live state.
