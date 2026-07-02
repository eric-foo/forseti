```yaml
retrieval_header_version: 1
artifact_role: Orca architecture-planning prompt
scope: >
  Architecture planning for the Orca recurring lane poller: deciding whether to
  replace per-lane scheduled-task sprawl with one thin scheduler/orchestrator
  that checks the F: data lake and dispatches lane-specific workers for IG,
  YouTube transcript product extraction, and future bounded tasks.
use_when:
  - Commissioning a read-only architecture pass before implementing recurring data-lake automation.
  - Checking whether "one checker for all tasks" should instead be one scheduler plus per-lane workers.
  - Deciding how Codex app/CLI recurring automation, Windows scheduled tasks, durable status logs, and lane configs should be separated.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/safety-rules.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/template-registry.md
  - orca-harness/runners/run_transcript_product_extract.py
  - orca-harness/runners/run_ig_reels_product_extract.py
  - orca/product/spines/data_lake/README.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
stale_if:
  - The current user redirects from architecture planning into implementation or scheduled-task setup.
  - A lane-poller architecture decision or implementation handoff already supersedes this prompt.
  - The IG/YouTube product-extraction runners or data-lake authority docs change materially after this prompt is written.
```

# Orca Lane Poller Architecture Prompt v0

## Orca Prompt Preflight

- Output mode: `file-write` for this prompt artifact; receiving architecture output is `chat-only` unless the operator explicitly asks for a filed architecture report.
- Template kind: `none`; architecture prompt authored directly under the Orca prompt contract because no dedicated architecture template is bound in the template registry.
- Edit permission for the receiving pass: `read-only`; no source edits, no scheduled-task changes, no Codex automation creation, no commits, no pushes.
- Authorization basis: current owner request to first check whether the recurring data-lake checker idea is the right direction, then proceed with an architecture-planning prompt if it is.
- Target scope: recurring data-lake automation architecture for product-extraction lanes, starting with IG Reels and YouTube transcripts, while staying extensible to other bounded tasks.
- Branch/workspace: use the current Orca workspace supplied by the operator; verify current branch, commit, and dirty state before making strict repo claims.
- Dirty state allowance: dirty/untracked work may be used only as orientation if explicitly named by the operator or present in the required source pack; do not treat it as mainline authority.
- Reviews: not a review prompt; do not emit formal review findings or verdicts.
- Doctrine change: do not change doctrine. If a recommended architecture would require workflow, validation, or data-lake doctrine changes, name the propagation surfaces and stop at recommendation.
- Isolation decision for this prompt artifact: authored in an isolated worktree off `origin/main` because the originating checkout was dirty.
- Prompt artifact path: `docs/prompts/architecture/orca_lane_poller_architecture_prompt_v0.md`.

## Executor Target

First decide whether the proposed direction is right:

> Move from per-lane scheduled-task sprawl toward one recurring scheduler/orchestrator that checks the Orca data lake and dispatches separate lane workers/configs for enabled tasks.

If that direction is materially wrong, say so and return the better direction. If it is materially right, proceed to a source-backed target architecture.

Done looks like: the owner can decide whether to authorize a later implementation-scoping pass for a lane poller without re-deciding the scheduler-vs-worker boundary, logging/status boundary, Codex app/CLI/Windows Task boundary, or lane-extension model.

## Mandatory Method Handling

If you have repo/filesystem access, open and re-read every required load-bearing source below before making strict or actionable claims.

If you do not have repo/filesystem access, stop and request a pasted source capsule or no-repo handoff. Do not infer the architecture from this prompt alone.

REFERENCE-LOAD `workflow-architecture-planning` if it is available in the receiving environment. Do not APPLY it yet.

Then SOURCE-LOAD the task sources listed below. Declare exactly one:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

Only after that declaration, APPLY architecture planning in `standard` profile.

Run the Cynefin router from `.agents/workflow-overlay/decision-routing.md` before architecture synthesis. Expected initial classification: `complicated` with `complex` risk. You may change that classification if the sources justify it.

Use three advisory perspectives. If the environment supports subagents, launch three advisory subagents:

1. Scheduler/orchestrator architect.
2. Lane-worker/config architect.
3. Adversarial operations architect.

If subagents are unavailable or unsafe in the environment, run the three perspectives locally and disclose the fallback. Advisory perspectives are inputs only, not verdicts.

Each advisory lane must return this terse schema, one line per field:

```text
perspective:
direction_check:
architecture_recommendation:
strongest_reason:
strongest_risk:
core_boundary:
lane_boundary:
scheduler_boundary:
status_logging_boundary:
codex_app_or_windows_task_position:
not_proven:
source_cites:
```

Every load-bearing source claim needs a local file/path cite when available. Use `unknown` for absent fields.

## Required Source Pack

Read:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/template-registry.md`
- `orca/product/spines/data_lake/README.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md`
- `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`
- `orca-harness/runners/run_transcript_product_extract.py`
- `orca-harness/runners/run_ig_reels_product_extract.py`

Also inspect these if present:

- `docs/workflows/data_lake_r2_continuation_handoff_v0.md`
- `orca-harness/runners/run_source_capture_youtube_caption_packet.py`
- `orca-harness/runners/run_source_capture_youtube_asr_packet.py`
- any current lane-specific poller wrapper, especially `poll_and_extract.ps1`
- any current scheduled-task docs, automation notes, or data-lake operational logs referenced by the operator

Do not bulk-read unrelated scratch, captured media, cookies, storage state, raw third-party response bodies, or full data-lake payload bodies. This is an architecture pass, not a capture or extraction run.

If `F:\orca-data-lake` is accessible, verify only non-invasive root identity/status facts needed for architecture, such as root existence and marker/UUID. Do not write to the lake and do not scan the lake contents broadly. If it is not accessible, treat the data-lake facts below as operator-supplied context and keep claims qualified.

## Operator-Supplied Current Context To Verify, Not Trust

- Data lake target: `F:\orca-data-lake`.
- Data lake root UUID observed 2026-07-02: `01KW7N6ERSVVANCEZ8SD6YW3EQ` (v4.1 forward epoch, re-initialized 2026-06-28 under `epoch_policy: clean_forward_epoch`; the prior v0 root `01KW1E6N133JT0XCN2KCN0V5A4` is preserved at `F:\orca-data-lake-legacy-v0-20260628T174129Z`). Epoch changes retire root identity without migrating packets; the poller architecture must account for that.
- Current IG recurring setup: the Windows scheduled task `OrcaIGExtract` (15-minute repetition) was disabled by owner direction on 2026-07-02. Its recorded action still points at a poller copy in a since-removed worktree (`worktrees\ig-reels-extract-routine\...`), so re-enabling the lane also requires re-pointing the task action. The repo poller is `orca-harness/runners/poll_and_extract.ps1`, re-pinned to the v4.1 root on 2026-07-02 with a loud `blocked_root_uuid_mismatch` status on lake-identity drift.
- Normal desired behavior after debugging: no focus-stealing recurring shell windows; durable lake/status/log evidence should make the automation observable without interrupting the operator.
- The YouTube product-extraction lane should use the GPT-family/Codex route like the IG extraction setup, not a Sonnet/browser recurring process.
- The earlier Sonnet/browser work was a separate one-off quality-check/extraction lane, not the desired recurring automation shape.
- The owner wants flexibility: this should support future bounded tasks, not only IG and YouTube.

If you find that any of those facts are wrong in the current repo or operating environment, report the mismatch and let it affect the architecture.

## Current Working Facts To Verify, Not Trust

Treat these as hypotheses until confirmed:

- `run_transcript_product_extract.py` is daemon-ready for YouTube transcripts: it scans the lake for committed YouTube transcript packets, skips completed mention record-sets, isolates corrupt-packet and per-transcript failures, and returns status rows.
- `run_ig_reels_product_extract.py` is the IG analogue: it scans committed IG Reels audio packets, uses ASR-derived transcript records, skips completed mention record-sets, and returns status rows.
- The extraction runners are no-LLM zones; live model/API transport is injected by the caller.
- This shape suggests a thin scheduler can call lane workers without becoming a domain-specific extractor.
- Current lane wrappers may live outside `origin/main` or in dirty worktree material; do not treat them as accepted architecture unless verified.

## Direction Check

Answer this before full architecture synthesis:

1. Is the right direction one scheduler/orchestrator with separate lane workers/configs?
2. Or should Orca keep separate scheduled tasks per lane?
3. Or should Orca build one giant all-knowing checker?
4. Or should the scheduler choice be abstracted so either Codex app automation or Windows Task Scheduler can trigger the same poller entrypoint?

Expected but not binding prior: the likely right direction is **one thin scheduler/orchestrator plus per-lane workers/configs**. Push back if the sources show otherwise.

## Architecture Questions

Answer these directly if the direction survives the gate:

1. What is the core architecture: scheduler adapter, poller core, task registry, lane worker, status ledger, lock model, and operator view?
2. What belongs in the shared core versus per-lane satellite code/config?
3. How should a lane declare: enabled/disabled, cadence eligibility, pending check, command/entrypoint, cwd, model/provider config, batch limit, timeout, lock key, done marker, partial/failure semantics, and status output?
4. How should the scheduler avoid becoming a giant checker while still supporting future tasks?
5. Should Codex app automation, Codex CLI, Windows Task Scheduler, or another trigger own the 15-minute recurrence? Should the architecture isolate this behind a scheduler adapter?
6. How should debugging mode differ from normal mode? Specifically, when is a persistent visible PowerShell acceptable, and what durable logs/status should replace it later?
7. What is the minimum durable status/log format needed so the owner can tell what happened without being tabbed out?
8. How should locks prevent overlapping runs when a 15-minute tick fires while a prior extraction is still running?
9. What is the failure policy: partial record-set detected, corrupt packet, missing API key, no pending work, model call failure, Codex/CLI unavailable, data lake unavailable?
10. What is the smallest complete implementation route after this architecture pass, if the owner accepts the direction?

## Non-Goals And Guardrails

- Do not implement anything.
- Do not modify scheduled tasks or Codex app automations.
- Do not run extraction.
- Do not write to `F:\orca-data-lake`.
- Do not create a queue service, dashboard, database, web server, or generic workflow platform unless the sources prove the thin model cannot work.
- Do not collapse lane-specific semantics into a fake universal schema. Use a small shared status envelope and let lanes own their domain statuses.
- Do not hardcode Sonnet/browser as the recurring extraction mechanism.
- Do not claim validation, readiness, deployment, production safety, or successful automation setup.
- Do not re-open YouTube public capture transport decisions except where they affect this poller boundary.

## Expected Architecture Output

Return:

```text
Human Summary:
Direction Check:
Decision:
Target Architecture:
Why This Wins:
Core / Satellite Boundary:
Scheduler Boundary:
Lane Registry Shape:
Status / Logging / Operator Visibility:
Debug Mode vs Normal Mode:
Codex App / CLI / Windows Task Position:
Failure And Locking Policy:
Deferred Implementation Implications:
What We Are Not Doing:
Blockers / Not-Proven Boundaries:
Next Authorized Routing Object:

Agent Detail:
Profile / Evidence Mode / Source Mode:
Cynefin Routing Result:
Subagents Launched:
Source-Read Ledger:
Questions Answered:
Decision Criteria:
Risks Accepted:
Direction-Change Surfaces If Any:
```

The `Decision` field must be exactly one of:

- `TARGET_RECOMMENDED`
- `DIRECTION_REJECTED`
- `OPTIONS_COMPARED_NO_SELECTION`
- `SOURCE_CONTEXT_INCOMPLETE`

The `Next Authorized Routing Object` must be planning-only unless the current operator explicitly authorizes implementation. If implementation is recommended, name it as a future implementation-scoping pass, not as work to begin immediately.
