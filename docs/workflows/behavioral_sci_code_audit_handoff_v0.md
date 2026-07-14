# Behavioral SCI Code Audit Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Cold-lane commission for an aggregate behavioral smallest-complete-intervention evidence audit of live Forseti code.
use_when:
  - Starting the commissioned behavioral code audit in a fresh, repository-capable lane.
  - Reconstructing the audit boundary, evidence schema, or transport revision without authoring-chat context.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
  - docs/workflows/forseti_repo_map_v0.md
branch_or_commit: codex/behavioral-sci-audit-packet; parent 3b41ca9853b5ebf72fc37075d050494d35ddf00d
stale_if:
  - The couriered transport commit no longer resolves this exact path and byte content.
  - AGENTS.md or a load-bearing overlay source below changes before the receiver completes confirm-don't-trust loading.
  - The receiver cannot inspect the commissioned repository revision or cannot write only the named ledger path.
```

## Load Contract

- `packet_version`: `behavioral_sci_code_audit_handoff_v0`
- `mode`: `max`
- `source_loading_mode`: `repo-overlay-bound`
- `created_at`: `2026-07-14T19:20:58.3933148+08:00`
- `created_by_lane`: worktree-backed Codex authoring lane; provenance only, not authority
- `source_thread_id`: `019f567f-da4c-75f0-ba06-3e5addf4d7b1`
- `workspace`: `C:\Users\vmon7\Desktop\projects\forseti-worktrees\ef5d\orca`
- `handoff_path`: `docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
- `downstream_output`: `docs/workflows/behavioral_sci_code_audit_ledger_v0.md`
- `expected_branch`: `codex/behavioral-sci-audit-packet`
- `expected_parent`: `3b41ca9853b5ebf72fc37075d050494d35ddf00d`
- `expected_head`: the immutable transport commit couriered with this packet; verify that commit and resolve the packet with `git show <transport-commit>:docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
- `expected_dirty_state_including_handoff_file`:
  - before branch creation: detached, clean at `3b41ca9853b5ebf72fc37075d050494d35ddf00d`
  - after branch creation and before writing: clean on `codex/behavioral-sci-audit-packet`
  - after writing and before the transport commit: only `?? docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
  - dispatch-ready transport state: clean after the one packet commit; the courier must verify rather than infer this state
- `load_rule`: confirm-don't-trust; treat this packet as a weak context artifact and re-verify every load-bearing fact against its compare target before acting
- `authority_status`: user instruction controls this commission; `AGENTS.md` and the Forseti overlay control project facts; this packet creates no source-of-truth, approval, readiness, validation, implementation, publication, or merge claim
- `durable_destination_status`: bound workflow-record destination for single-use cold-lane transport
- `receiver_authorization_rule`: the receiver's current instruction must explicitly authorize the ledger audit and docs write; this packet alone does not grant edit permission

## Goal Handoff

- `long_term_goal`: Forseti code changes become smallest complete behavioral units—real behavior, integration, tests, lifecycle, and visible failure arrive together without duplicate ownership or chat reconstruction.
- `anchor_goal`: inspect current live Forseti code and produce an aggregate behavioral-SCI evidence ledger for later control selection.
- `success_signal`: every material finding is traceable to current file:line evidence; inspected and uninspected families are explicit; recurring gaps are separated from one-offs; mechanical vs resident vs no-standing-control candidates are prioritized without implementation.

## Open Decision / Fork

- `decision`: Which evidence-supported controls, if any, should later become deterministic gates, resident judgment, or no standing rule?
  - `options`:
    - `mechanical`: an objective fail-loud gate at a real tool, commit, CI, or runtime boundary
    - `resident_judgment`: a semantic review or authoring check whose correctness depends on context
    - `no_standing_control`: record and close the observed defect without creating a recurring maintenance surface
  - `already constrained / off the table`: this audit does not select, implement, activate, or approve a control; it does not change doctrine; literal artifact headers, per-code-file repo-map rows, and a universal orphan-code detector are excluded
  - `trade-offs`: mechanical controls can catch repeated defects early but create false-positive and maintenance cost; resident checks retain semantic judgment but depend on attention; no standing control avoids lock-in but leaves recurrence to existing owners
  - `owner of the call`: Forseti owner after reviewing the completed ledger evidence
  - `recommendation and why`: recommend an objective fail-loud gate only for a repeated high-impact defect whose enforcement boundary is real and whose false-positive risk is low; otherwise prefer resident judgment or no standing rule

## Drift Guard

- Audit behaviors, not files.
  - Why it matters: the unit of completeness is an observable consumer-facing or operator-facing behavior across wiring, ownership, state, tests, and failure semantics.
  - What violating it would break: a file inventory could look complete while behavioral seams remain missing or multiply owned.
- Do not add literal artifact headers or per-file repo-map rows for code.
  - Why it matters: retrieval metadata and the T1 repo map explicitly exclude per-code-file inventory.
  - What violating it would break: it would create duplicate maintenance surfaces and false route authority.
- Do not design or recommend a universal orphan-code detector.
  - Why it matters: dynamic activation, compatibility callers, and reflective wiring make universal mechanical detection structurally unreliable.
  - What violating it would break: it would hide uncertainty behind high false-positive or false-negative claims.
- Inspect live runtime by default, not historical migration, generated, ignored, or scratch corpus.
  - Why it matters: the owner asked for current live behavior and bounded source loading.
  - What violating it would break: findings would mix current execution truth with stale or non-authoritative material.
- Do not implement in the audit lane.
  - Why it matters: this lane is findings-first evidence collection and ledger authoring only.
  - What violating it would break: findings, adjudication, and implementation authority would collapse into one lane.
- Treat passing tests and import reachability as evidence, never proof of behavioral completeness.
  - Why it matters: mocked seams, missing lifecycle behavior, and unexercised consumers can survive both.
  - What violating it would break: the ledger would overclaim completeness or validation.
- Keep unknown, dynamic, and uninspected surfaces visible.
  - Why it matters: unknown is an allowed status and source-loading must remain bounded.
  - What violating it would break: coverage gaps would be silently converted into absence claims.
- Later control classifications are recommendations only.
  - Why it matters: no doctrine change or implementation is authorized.
  - What violating it would break: the audit would usurp the owner's open control-selection decision.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish (follows overlay doctrine)

- `overlay source-loading policy`: `.agents/workflow-overlay/source-loading.md`, especially Rule, Forseti Start Preflight, Targeted Read Protocol, Expansion Rules, and New Thread Triggers
- `targets to enter the ladder`:
  - area-level route: `docs/workflows/forseti_repo_map_v0.md` -> Forseti Harness Areas and Active Hooks
  - primary execution front doors: `forseti-harness/runners/`, then each runner's actually imported owners across `capture_spine`, `source_capture`, `youtube_capture`, `data_lake`, `cleaning`, `ecr`, `evidence_binding`, `schemas`, `scoring`, `reports`, and `source_observability`
  - matching evidence and activation surfaces: `forseti-harness/tests/`, `forseti-harness/pyproject.toml`, `forseti-harness/README.md`, `forseti-harness/config/`, and CLI/registry/config wiring discovered from current source
  - active-hook surfaces when they activate or validate behavior: `.agents/hooks/`, `.codex/hooks.json`, `.codex/hooks/`, `.githooks/`, and `.github/workflows/`
- `already loaded`: the authoring lane loaded only project authority, retrieval/transport rules, area-level repo-map routes, hook activation routes, and path inventory as of 2026-07-14; it did not inspect runtime implementation bodies or tests
- `must load first`: re-verify the packet transport commit, workspace, revision, dirt, edit permission, every load-bearing source hash below, the existence of the named ledger destination's parent, and the current runtime area/activation routes before reading implementation bodies
- `load rule`: rerun progressive source loading per the overlay; this packet's loaded set only seeds the ladder
- `source-heavy economy`: define one bounded behavioral family or seam per loading unit; append and seal that unit into the single ledger before expanding; record a compact in-ledger unit receipt and SHA256 rather than carrying full source or logs in chat

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- `Smallest Complete Intervention`: completeness means the whole requested behavior, including necessary integration and failure visibility, with no unrelated surface.
  - `decided in`: `AGENTS.md` -> Smallest Complete Intervention and Problem Integrity
  - `compare target`: raw SHA256 `ec1a51fde7f2ff5cc6aa2c321599ec6a0219103f522be9bea449523409b8b3d6`
  - `verify before`: defining behavioral units, minimum closure conditions, or later control candidates
- `Failure visibility`: do not create fake success paths; unknown, skipped, empty, degraded, failed, and complete states must not collapse without evidence.
  - `decided in`: `AGENTS.md` -> Agent Behavior Kernel
  - `compare target`: raw SHA256 `ec1a51fde7f2ff5cc6aa2c321599ec6a0219103f522be9bea449523409b8b3d6`
  - `verify before`: classifying failure/exit semantics or behavioral completeness
- `Source loading`: source hierarchy chooses authority; bounded claim-level loading chooses what to read; expand only when a missing source could change a finding.
  - `decided in`: `.agents/workflow-overlay/source-loading.md`
  - `compare target`: raw SHA256 `ddfd0751161a748b0f34a09c6f4e556c44f85b5382e92f92a756ad9f0a0acd30`
  - `verify before`: the first implementation-body read and every source-family expansion
- `Enforcement placement`: mechanically checkable load-bearing rules belong at a deterministic boundary; semantic rules remain resident judgment.
  - `decided in`: `.agents/workflow-overlay/decision-routing.md` -> Enforcement Placement
  - `compare target`: raw SHA256 `0b7a0309f6b4aa93bce5d81b27a82419867bc41da3cde892f9453a07ce24c387`
  - `verify before`: recommending any candidate control
- `Repo-map boundary`: the central map is a T1 area router, not a per-module or per-runner inventory; code and generated outputs do not gain authority from map/header treatment.
  - `decided in`: `docs/workflows/forseti_repo_map_v0.md` -> T1 Admission Control and Forseti Harness Areas
  - `compare target`: raw SHA256 `b017fcfe69478a57dc841a54eecdf52c6d0f98c6b8fc9ebeeacffdbe4126dc33`
  - `verify before`: expanding source routes or proposing retrieval controls
- `Handoff transport`: the packet commit is an immutable local transport handle; it is not publication and is not rewritten during transport.
  - `decided in`: `.agents/workflow-overlay/prompt-orchestration.md` -> Handoff Transport Versus Publication
  - `compare target`: raw SHA256 `adea53f9c485a2ad660a961b79951d178a9f36b883b1a62d2d463795733df21a`
  - `verify before`: accepting the packet revision or changing its transport route

## Forseti Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 plus targeted routing, handoff-transport, metadata, artifact-role, and active-hook routes
  edit_permission: docs-write
  target_scope: author the cold-lane packet only; receiver later writes only docs/workflows/behavioral_sci_code_audit_ledger_v0.md
  dirty_state_checked: yes
  blocked_if_missing: bound receiver root, exact transport revision, load-bearing source compare targets, ledger-only write authority, or live source access
```

## Forseti Prompt Preflight

1. `Output mode`: `file-write`; this packet writes only `docs/workflows/behavioral_sci_code_audit_handoff_v0.md`; the receiver writes only `docs/workflows/behavioral_sci_code_audit_ledger_v0.md`.
2. `Template kind`: `none`.
3. `Edit permission · targets · branch`: `docs-write`; packet branch `codex/behavioral-sci-audit-packet`; receiver must bind its own focused lane; clean-start allowance permits only its ledger to become dirty/untracked.
4. `Reviews`: findings-first behavioral evidence audit; no readiness, validation, approval, acceptance, or formal review verdict; severity and confidence describe findings only.
5. `Doctrine change`: none authorized; all later control classifications are recommendations pending owner selection.
6. `Destinations`: the receiver's current instruction plus this committed packet define the run input; the only receiver output is `docs/workflows/behavioral_sci_code_audit_ledger_v0.md`.

## Active Objective

Inspect current live Forseti execution behavior and write one aggregate evidence ledger that lets the owner later select the smallest justified controls without reconstructing chat, hiding uninspected surfaces, or treating tests/imports as completeness proof.

## Exact Next Authorized Action

1. Confirm-don't-trust load outcome before source work: return exactly one of `REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`; do not proceed on an unverified load-bearing fact.
2. Build the actual execution graph from entrypoints, imports, registries, config, tests, outputs, and active-hook/CI/local-Git wiring.
3. Audit in bounded source-loading units and seal each completed unit into `docs/workflows/behavioral_sci_code_audit_ledger_v0.md` before expanding to the next unit.
4. Write only `docs/workflows/behavioral_sci_code_audit_ledger_v0.md`; do not edit code, runtime, tests, hooks, CI, configuration, repo maps, overlay, prompts, or other documents.
5. Run doc placement, retrieval-header, repo-map, handoff-pointer, DCP-shape when applicable, citation-path, and diff checks; run only targeted existing tests needed to substantiate a ledger claim, and record not-run plus reason for tests not needed.
6. Commit, push, and open a focused ready pull request for the substantive ledger; do not merge it.

Stop and report a visible blocker if the receiver instruction does not authorize the ledger write, the target revision or dirt conflicts, a load-bearing source cannot be re-verified, the only way forward requires implementation, or source expansion crosses the packet's live-runtime boundary without owner direction.

## Audit Commission

### Unit of audit

A behavioral unit is the smallest consumer- or operator-visible behavior that has a distinguishable trigger, owner, inputs, outputs or side effects, wiring, failure/exit semantics, state/provenance behavior, and testable public seam. A file may contribute to many units; a unit may cross many files. Never substitute a file list for the execution graph.

Start from the current runner/activation surface, trace imports and registries to actual owners, and then trace forward into outputs, state, consumers, recovery behavior, and tests. Record dynamic or ambiguous edges as `unknown`; do not infer absence from static search alone.

### Required initial routes

1. `forseti-harness/runners/`: enumerate current tracked entrypoints at receiver load time; for each in-scope behavior, follow the actually imported owner rather than treating the runner filename as ownership.
2. Imported owners across `forseti-harness/capture_spine/`, `source_capture/`, `youtube_capture/`, `data_lake/`, `cleaning/`, `ecr/`, `evidence_binding/`, `schemas/`, `scoring/`, `reports/`, and `source_observability/`.
3. Matching `forseti-harness/tests/`, `forseti-harness/pyproject.toml`, `forseti-harness/README.md`, `forseti-harness/config/`, and discovered CLI, registry, environment, and config wiring.
4. `.agents/hooks/`, `.codex/hooks.json`, `.codex/hooks/`, `.githooks/`, and `.github/workflows/` only where they activate, enforce, validate, or claim to validate a behavior in the execution graph. Script presence is not activation proof; confirm tracked wiring.

The route list is an entry ladder, not a claim that every area is required for every unit. Mark any named family not inspected, and why, in the ledger coverage boundary.

### High-value blind spots to test explicitly

- entrypoint-to-owner reachability
- runner thinness versus duplicated business or lifecycle logic
- cross-stage seam completeness
- schema, version, producer, and consumer alignment
- failure taxonomy, including exit, empty, skip, degraded, blocked, retryable, terminal, and success distinctions
- timeout, cancellation, retry, and idempotency behavior
- side effects, atomicity, resume, rollback, and cleanup
- durable provenance and limitation reporting
- dynamic activation through registries, config, discovery, hooks, environment, or reflection
- compatibility, supersession, and current live callers
- test realism and seams mocked away from public behavior
- environment, path, dependency, authentication, and secret handling
- concurrency, backpressure, locking, and repeated runs
- operator diagnostics, recovery instructions, and failure locality
- CI/local boundary parity
- implemented but unwired behavior
- reachable code with no distinct consumer or independently justified owner
- behavior that depends on authoring-chat knowledge instead of durable input, contract, config, or diagnostics

For each blind spot, record observed evidence, `not_proven`, or `uninspected`; silence is not a negative result.

## Required Ledger Contract

### Opening boundary

The ledger must begin with a retrieval header and a compact opening that states:

- audited repository revision and branch/ref;
- coverage method and source-loading-unit method;
- inspected behavioral families and entrypoints;
- explicitly uninspected families;
- exclusions: historical migration, generated output, ignored/scratch corpus, and any owner-deferred route;
- unknown or dynamic surfaces;
- evidence date/time and commands used for graph inventory;
- review-use boundary: findings-first evidence only, no readiness/validation/approval verdict;
- not-proven boundaries, including the limits of tests, imports, static searches, and sampled runtime evidence.

### One row per behavioral unit

Use one row per behavioral unit. Do not merge materially different consumers, failure semantics, or ownership into one row merely because they share files.

| ID | Behavior / consumer | Entrypoint / owner | Inputs / outputs / side effects | Wiring cite | Test cite + public-seam depth | Failure / exit semantics | State / provenance / idempotency | Duplicate / superseded / orphan observations | Status | Severity | Confidence | Minimum closure condition | Candidate control | False-positive / lock-in risk | Not-proven boundaries |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `BSI-###` | observable behavior and named consumer | public trigger plus actual owning symbol/module | concrete inputs, durable/ephemeral outputs, and side effects | current repo-relative `file:line` citations for entry, wiring, and consumer | current repo-relative `file:line` test citations plus `unit|module_seam|public_seam|live_or_fixture_integration|none` | distinctions among success, empty, skip, degraded, blocked, retryable, terminal failure, and process exit | state transition, provenance persistence, retry/repeat behavior, idempotency or explicit unknown | evidence for duplicate ownership, supersession, compatibility, implemented-but-unwired, reachable-without-distinct-consumer, or `none_observed_not_proven_absent` | `behaviorally_complete|partial|unwired|duplicate_owner|unknown` | `critical|major|minor` | `high|medium|low` | required end state that would close the finding without prescribing implementation | `mechanical|resident_judgment|no_standing_control` | expected false positives, maintenance burden, and irreversible/expensive lock-in | explicit boundaries the row does not prove |

Row rules:

- Every material positive or negative claim needs current repo-relative `file:line` evidence; commands alone may establish path/reachability facts but not behavioral semantics.
- `behaviorally_complete` requires evidence across entrypoint, owner, integration/consumer, failure visibility, state/provenance when applicable, and a realistic public seam; if one material dimension is uninspected, use `partial` or `unknown`.
- `unwired` requires evidence that implementation exists and the expected live entry/config/registry/consumer edge is absent within a stated search boundary; it is not a universal orphan claim.
- `duplicate_owner` requires two or more live owners for materially the same behavior, not helper reuse or compatibility delegation by itself.
- Severity describes consequence if the evidence is correct. Confidence describes evidence strength. Neither is a readiness verdict.
- Minimum closure condition names the end state required to close the finding; it does not authorize or dictate an implementation.
- Candidate control is a recommendation only. A mechanical candidate must name the exact enforceable boundary and why objective detection has low false-positive risk.

### Cross-family synthesis

After the rows, include:

1. `Repeated versus isolated`: cluster recurring failure shapes across behavioral families; keep one-offs separate and cite every contributing row ID.
2. `Evidence-supported principles`: state only principles supported by more than one observed unit, or label a single-unit insight explicitly.
3. `Exact enforcement boundaries`: for each mechanical candidate, name the actual boundary—CLI exit, schema serialization, state transition, commit hook, CI diff, runtime handoff, or other observed seam—and the defect it would catch.
4. `Semantic resident checks`: name the judgment question, evidence needed, and why deterministic enforcement would be brittle.
5. `Rejected tempting proxies`: include at least literal artifact headers for code, per-file repo-map rows, a universal orphan-code detector, import reachability as completeness, and passing tests as completeness; add evidence-specific proxies rejected during the audit.
6. `Prioritized later implementation candidates`: recommendation order only, with `defect caught`, `proof target`, `maintenance cost`, and `smallest complete closure`; do not patch or bind owner acceptance.
7. `Residuals and upgrade triggers`: list unresolved unknowns, accepted sampling limits, dynamic surfaces, and the evidence that would justify deeper inspection or a stronger standing control.
8. `Control-selection summary`: separate `mechanical`, `resident_judgment`, and `no_standing_control` candidates, with row IDs, recurrence evidence, false-positive risk, and owner decision still open.

### Rerunnable command/evidence appendix

Include compact commands sufficient to reproduce graph inventory, citations, targeted tests, and validation. Record command, cwd, revision, exit code, and a short result; do not paste full logs. For a failed or incomplete command, preserve the failure and scope consequence. For source-heavy units, record the ledger SHA256 at unit seal so later synthesis can detect drift.

## Authority And Source Ledger

All SHA256 values below are raw file-byte hashes observed in the authoring worktree on 2026-07-14. A hash match proves byte identity only, never truth, authority beyond the source hierarchy, or semantic readiness.

| Path or source | Role | Load-bearing | Compare target | Last checked | Reuse rule |
| --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | canonical project behavior kernel | yes | SHA256 `ec1a51fde7f2ff5cc6aa2c321599ec6a0219103f522be9bea449523409b8b3d6` | 2026-07-14 | reread governing sections after hash match; block on drift until reconciled |
| `.agents/workflow-overlay/README.md` | overlay entrypoint | yes | SHA256 `3ae439bdd517986fff01fa4c029140c6d1d52d6968e113aba30a7a3e7ff87b90` | 2026-07-14 | re-establish overlay authority; block on conflict |
| `.agents/workflow-overlay/source-of-truth.md` | source hierarchy and checkpoint lifecycle | yes | SHA256 `084f69af15d8008027e55899a5078d16e6b359c18adf28bda8e4f8c061150d53` | 2026-07-14 | reread hierarchy and checkpoint sections before actionable use |
| `.agents/workflow-overlay/source-loading.md` | source budgets and targeted loading | yes | SHA256 `ddfd0751161a748b0f34a09c6f4e556c44f85b5382e92f92a756ad9f0a0acd30` | 2026-07-14 | rerun progressive loading; packet summary is not a substitute |
| `.agents/workflow-overlay/decision-routing.md` | receiver root and enforcement placement | yes | SHA256 `0b7a0309f6b4aa93bce5d81b27a82419867bc41da3cde892f9453a07ce24c387` | 2026-07-14 | reread receiver/write-root and enforcement sections before write/control claims |
| `.agents/workflow-overlay/prompt-orchestration.md` | preflight, transport, source-heavy economy, validation | yes | SHA256 `adea53f9c485a2ad660a961b79951d178a9f36b883b1a62d2d463795733df21a` | 2026-07-14 | reread named sections before accepting transport or authoring ledger |
| `.agents/workflow-overlay/artifact-folders.md` | placement authority | yes | SHA256 `a82f24c8290362ca2a07a8d50e107f714127dbdf9b8a4530f6c246e47fa61d44` | 2026-07-14 | confirm `docs/workflows/` remains accepted before writing |
| `.agents/workflow-overlay/artifact-roles.md` | workflow-record role and permission | yes | SHA256 `54b2b10554c3a41e44180cbb346c5c1888f2fb3b68b5d8a9e23c640e117b4a1b` | 2026-07-14 | confirm role/write boundary before writing |
| `.agents/workflow-overlay/retrieval-metadata.md` | retrieval-header contract | yes | SHA256 `5db6e666f30ac212fe766415da8c1d6af470785a60557ead504c0e4c58f7c505` | 2026-07-14 | reread header rules before ledger creation |
| `docs/workflows/artifact_retrievability_guide.md` | subordinate body/recheck guidance | no | SHA256 `ae07aa46e381fde6383fe454ff2f44365d161eae52dfbf9096676250c08d12e2` | 2026-07-14 | use only when shaping/reviewing the durable ledger; overlay wins |
| `docs/workflows/forseti_repo_map_v0.md` | T1 route map for live harness and hooks | yes | SHA256 `b017fcfe69478a57dc841a54eecdf52c6d0f98c6b8fc9ebeeacffdbe4126dc33` | 2026-07-14 | use for area entry only; inventory current source directly |
| `.agents/hooks/README.md` | checker behavior and activation-route guide | yes | SHA256 `f8370dd2825b4c256c3fff943c4c88b2625bf99f47a6d7fb96ab33b41d208a81` | 2026-07-14 | confirm activation in tracked config; script presence is insufficient |
| `.codex/hooks.json` | tracked Codex activation | yes when auditing Codex hook behavior | SHA256 `330ca8d3250867ec53996a0245cf85dc6d39531fc22fb4b6ee5a42f5c69ebe61` | 2026-07-14 | reread with adapter targets before activation claims |
| `.github/workflows/ci.yml` | tracked CI activation | yes when auditing CI behavior | SHA256 `df5f90f01f762f683763cb6c8151661e8345a79cbaa2649b4095a4aac643f4f6` | 2026-07-14 | inspect current workflow and exact event/diff wiring before parity claims |
| `.githooks/commit-msg` | tracked local commit adapter | yes when auditing local Git behavior | SHA256 `fadf5e64cef6c2d9460ce521b76d62d819327ace29189611cb3539ca36c788ea` | 2026-07-14 | verify installation/config separately; tracked presence is not activation |
| `.githooks/pre-push` | tracked local push adapter | yes when auditing local Git behavior | SHA256 `0ae4be6100b284e1322b4bc848afe1f38b8c6179e8e4c5e510cf4ffd99ee0519` | 2026-07-14 | verify installation/config separately; tracked presence is not activation |
| `repo-structure.yaml` | machine placement router | yes for placement checks only | SHA256 `cff001eeee573a1d5468b303498574d286e1e622fd96cdc84400674d78eb10f2` | 2026-07-14 | use only for placement shape; overlay remains authority |
| `C:\Users\vmon7\.codex\skills\workflow-handoff\SKILL.md` | task-local handoff mechanics | no | SHA256 `3ce84d0ac22fd8c24c7c99bdf8707de7f55e6981d005624acb6d6e71f9f81a34` | 2026-07-14 | optional orientation only; Forseti overlay owns project lifecycle |
| current commissioning instruction in source Codex task `019f567f-da4c-75f0-ba06-3e5addf4d7b1` | owner constraints and exact audit commission | yes | `reread-required`; no repository file hash exists | 2026-07-14 | receiver must have a current instruction authorizing the ledger; otherwise block |

- `source gaps`: runtime code bodies, tests, dynamic registrations, live callers, runtime state, environment state, and target ledger evidence were intentionally not loaded by the packet authoring lane.
- `strict-only blockers`: any load-bearing hash drift; missing current receiver authorization; revision/dirt mismatch; missing target path; source conflict; or inability to preserve unknown/uninspected states.
- `not-proven boundaries`: this packet does not prove runtime reachability, behavioral completeness, test realism, control suitability, hook activation, CI/local parity, code quality, readiness, validation, approval, or ledger findings.

## Current Task State

- `Completed`: packet preflight, branch isolation, targeted authority loading, route inventory, source hashes, parent-checkout danger-context verification, and the audit/ledger contract.
- `Partially completed`: staged packet validation is complete; the immutable transport commit and post-commit diff-scoped gate reruns are authoring-lane closeout actions, and the final courier receipt must carry their observed outputs and exact commit SHA.
- `Broken or uncertain`: no audit finding exists yet; dynamic activation and live runtime behavior are unknown; the separate parent checkout's `_scratch` enumeration was partially unreadable.

## Workspace State

- `Branch`: `codex/behavioral-sci-audit-packet`
- `Head before packet commit`: `3b41ca9853b5ebf72fc37075d050494d35ddf00d`
- `Dirty or untracked state before handoff authoring`: clean, detached at that SHA
- `Dirty or untracked state after branch creation`: clean
- `Dirty or untracked state after writing the handoff file and before commit`: only `?? docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
- `Required state after transport commit`: clean tracked/untracked state; verify with fresh `git status --porcelain=v2 --branch --untracked-files=all`
- `Target file`: `docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
- `Receiver output`: `docs/workflows/behavioral_sci_code_audit_ledger_v0.md`
- `Related authoring transport`: local branch/ref is sufficient for the next receiver; no push and no pull request for this packet
- `Separate parent checkout — dangerous to touch`: `C:\Users\vmon7\Desktop\projects\orca`, detached at `336773b7e77b133267d19494f6a406305c0b8076`, showed top-level untracked `_test_runs/`, `orca-worktrees/`, and `worktrees/`; these are presumptively authored/out-of-scope and must not be cleaned, moved, harvested, or edited by the audit lane
- `Parent-checkout uncertainty`: Git warned it could not open `_scratch/tmp80336k6l/` and `_scratch/tmpoty_35ul/`; do not claim the parent checkout has no other nested untracked material

## Changed / Inspected / Tested Files

- `docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
  - `Status`: new packet; only authorized repository change in this lane
  - `Role`: durable single-consumption cold-lane workflow record
  - `Important observations`: carries the exact audit commission, ledger schema, source pins, danger context, and receiver stop conditions
  - `Symbols or sections`: all max handoff sections in this document
- Project authority and routing sources in the Authority And Source Ledger
  - `Status`: inspected at targeted sections; unchanged
  - `Role`: bind source hierarchy, loading, placement, role, metadata, transport, active-hook routing, and validation commands
  - `Important observations`: source bodies are pinned by raw SHA256; source hierarchy still requires receiver reread
  - `Symbols or sections`: the named sections in the ledger and inherited context
- `forseti-harness/` runtime and tests
  - `Status`: not inspected beyond area/path inventory
  - `Role`: receiver-owned fresh audit sources
  - `Important observations`: no behavioral claim was derived in this authoring lane
  - `Symbols or sections`: none loaded
- Tests
  - `Status`: not run before packet authoring because this lane changes no code/runtime/test/hook/CI/config behavior; documentation gates remain required before commit

## Frozen Decisions

- `Decision`: audit behavior across execution seams, not files.
  - `Evidence`: current commissioning instruction and Goal Handoff.
  - `Consequence`: rows follow observable units and actual ownership, even when they cross directories.
- `Decision`: the receiver writes one aggregate ledger and nothing else.
  - `Evidence`: current commissioning instruction and Exact Next Authorized Action.
  - `Consequence`: no code, tests, hooks, CI, config, map, prompt, or supplemental audit artifact edits.
- `Decision`: live runtime is the default corpus.
  - `Evidence`: current commissioning instruction and Drift Guard.
  - `Consequence`: historical migration, generated outputs, ignored files, and scratch are excluded unless the owner later expands scope.
- `Decision`: audit output is findings-first evidence with no readiness, validation, approval, or acceptance verdict.
  - `Evidence`: current commissioning instruction and Prompt Preflight.
  - `Consequence`: statuses classify observed behavioral units only.
- `Decision`: no doctrine change or control implementation is authorized.
  - `Evidence`: current commissioning instruction.
  - `Consequence`: control rows are candidates for owner selection, not gates or adopted rules.
- `Decision`: packet publication is not justified merely for transport.
  - `Evidence`: prompt-orchestration handoff-transport rule and verified local receiver route.
  - `Consequence`: commit once locally; no push, PR, amend, rebase, or squash for this packet.

## Mutable Questions

- `Question`: which observed behavioral families will contain repeated high-impact defects?
  - `Why still mutable`: runtime sources and tests have not been inspected.
  - `What would resolve it`: completed rows plus repeated-versus-isolated synthesis.
- `Question`: which candidate controls, if any, have a real deterministic enforcement boundary and low false-positive risk?
  - `Why still mutable`: control choice depends on recurrence and seam evidence.
  - `What would resolve it`: exact boundary evidence, defect caught, proof target, maintenance cost, and owner decision.
- `Question`: which dynamic or environment-dependent routes can be established without live execution?
  - `Why still mutable`: static wiring may be insufficient and targeted tests may or may not exercise the public seam.
  - `What would resolve it`: bounded config/registry/environment inspection and only the targeted existing tests needed for the claim.

## Superseded / Dangerous-To-Reuse Context

- `Per-file code retrieval treatment`
  - `Why stale or dangerous`: literal headers and per-file repo-map rows would create duplicate ownership and violate code/header and T1-map boundaries.
  - `Current replacement`: behavior rows with `file:line` citations and the existing area-level repo map.
- `Universal orphan-code detection`
  - `Why stale or dangerous`: dynamic activation and compatibility routes prevent a reliable universal mechanical absence claim.
  - `Current replacement`: bounded `unwired`, duplicate, superseded, or reachable-without-distinct-consumer observations with explicit search boundaries.
- `Tests/imports imply completeness`
  - `Why stale or dangerous`: both can miss public seam, lifecycle, state, failure, and consumer behavior.
  - `Current replacement`: treat them as evidence dimensions inside a full behavioral row.
- `Historical, generated, ignored, or scratch corpus as live evidence`
  - `Why stale or dangerous`: it can be stale, non-authoritative, contaminated, or unrelated to current execution.
  - `Current replacement`: current tracked live runtime by default, with explicit exceptions only under later owner direction.
- `Separate parent checkout untracked directories`
  - `Why stale or dangerous`: `_test_runs/`, `orca-worktrees/`, and `worktrees/` are outside the verified receiver root and presumptively authored.
  - `Current replacement`: leave them untouched; operate only in the commissioned worktree.

## Commands And Verification Evidence

- `Command`: `git status --porcelain=v2 --branch --untracked-files=all`
  - `Passed/failed/not run`: passed before writing
  - `Important output`: clean detached checkout at `3b41ca9853b5ebf72fc37075d050494d35ddf00d`
  - `Re-run target`: receiver root before accepting packet state; authoring lane after commit
- `Command`: `git switch -c codex/behavioral-sci-audit-packet`
  - `Passed/failed/not run`: passed
  - `Important output`: switched to the named branch from the verified detached base
  - `Re-run target`: do not rerun; verify with `git branch --show-current` and `git rev-parse HEAD`
- `Command`: `git worktree list --porcelain`
  - `Passed/failed/not run`: passed
  - `Important output`: exact receiver root registered at the expected detached base before branch creation
  - `Re-run target`: only if receiver-root capability is in doubt
- `Command`: `Get-FileHash -Algorithm SHA256 <load-bearing-source>`
  - `Passed/failed/not run`: passed for every raw SHA256 in the Authority And Source Ledger
  - `Important output`: hashes recorded in the ledger above
  - `Re-run target`: every load-bearing file before source work
- `Command`: `git -c safe.directory=C:/Users/vmon7/Desktop/projects/orca -C C:\Users\vmon7\Desktop\projects\orca -c core.excludesFile= status --porcelain=v2 --branch --untracked-files=normal`
  - `Passed/failed/not run`: command exited `0` with warnings
  - `Important output`: parent detached at `336773b7e77b133267d19494f6a406305c0b8076`; top-level untracked `_test_runs/`, `orca-worktrees/`, `worktrees/`; two `_scratch` subdirectories unreadable
  - `Re-run target`: not required for the receiver; context is dangerous-to-touch only
- `Command`: `git diff --check` and `git diff --cached --check`
  - `Passed/failed/not run`: passed, exit `0`
  - `Important output`: no whitespace errors; staged name-status was only `A docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
  - `Re-run target`: final staged packet, then committed diff where applicable
- `Command`: `python .agents/hooks/check_placement.py --strict`
  - `Passed/failed/not run`: passed, exit `0`
  - `Important output`: `0 violation(s), 0 freshness, 1257 legacy-tolerated (warn-only), 72 scratch-excluded file(s)`
  - `Re-run target`: final packet tree; placement shape only
- `Command`: `python .agents/hooks/check_retrieval_header.py --staged --strict`
  - `Passed/failed/not run`: passed, exit `0`, no findings
  - `Important output`: the staged packet satisfies the forward-only retrieval-header shape check
  - `Re-run target`: final staged packet
- `Command`: generated-index reachability with `python .agents/hooks/header_index.py --index`
  - `Passed/failed/not run`: passed, exit `0`
  - `Important output`: generated index contained `path: docs/workflows/behavioral_sci_code_audit_handoff_v0.md`
  - `Re-run target`: post-commit `python .agents/hooks/header_index.py --strict` against the committed diff
- `Command`: `python .agents/hooks/check_repo_map_freshness.py --staged --strict`
  - `Passed/failed/not run`: passed, exit `0`, with an advisory to verify the existing `docs/workflows/` map description
  - `Important output`: the file is a workflow record already covered by the accepted-folder and T1 map descriptions; it adds no major area, active-hook route, or per-file T1 row, so no map edit is required
  - `Re-run target`: final staged packet
- `Command`: `python .agents/hooks/check_dcp_receipt_hygiene.py --staged --strict`
  - `Passed/failed/not run`: passed, exit `0`, no findings
  - `Important output`: no standalone or over-inline DCP receipt storage defect; no doctrine change or DCP receipt is present
  - `Re-run target`: final staged packet; run `check_dcp_receipt.py --strict` after commit so its diff scanner sees the packet
- `Command`: `python .agents/hooks/check_map_links.py --strict`
  - `Passed/failed/not run`: passed, exit `0`
  - `Important output`: `0 findings`; `36` annotated nonresolving debt entries were reported as non-failures
  - `Re-run target`: final packet tree
- `Command`: `python .agents/hooks/check_handoff_pointers.py --strict`
  - `Passed/failed/not run`: pre-commit invocation exited `0` but saw `0 changed file(s)` because this checker scans committed diffs, so it is not counted as packet validation yet
  - `Important output`: post-commit rerun is required against the actual packet commit
  - `Re-run target`: immediately after the one transport commit

Required packet validation commands:

```powershell
git diff --check
python .agents/hooks/check_placement.py --strict
python .agents/hooks/check_retrieval_header.py --staged --strict
$index = python .agents/hooks/header_index.py --index; $index | Select-String -SimpleMatch 'docs/workflows/behavioral_sci_code_audit_handoff_v0.md'
python .agents/hooks/check_repo_map_freshness.py --strict
python .agents/hooks/check_handoff_pointers.py --strict
python .agents/hooks/check_dcp_receipt.py --strict
python .agents/hooks/check_dcp_receipt_hygiene.py --staged --strict
python .agents/hooks/check_map_links.py --strict
```

The authoring lane must also inspect `git diff -- docs/workflows/behavioral_sci_code_audit_handoff_v0.md`, stage only that path, verify the staged diff, commit once, fresh-read `git show <commit>:docs/workflows/behavioral_sci_code_audit_handoff_v0.md`, compare its bytes to the committed packet SHA256, and verify clean tracked/untracked state, branch, and commit. Passing checks prove only their documented shape boundaries.

## Blockers And Risks

- `Load-bearing source drift`
  - `Evidence`: hash mismatch, missing source, or conflicting current instruction.
  - `Likely next action`: return `STALE_REREAD_REQUIRED` when safe to re-derive; otherwise `BLOCKED_DRIFT` or `BLOCKED_UNVERIFIABLE`.
- `Receiver authorization or write-root mismatch`
  - `Evidence`: current instruction does not authorize the ledger, observed root differs, or target cannot be written.
  - `Likely next action`: stop with `BLOCKED_RECEIVER_REROOT_REQUIRED` or the precise role/source blocker; do not source-load first.
- `Audit scope becomes source-heavy before a unit is sealed`
  - `Evidence`: multiple families or large evidence bodies accumulate without a ledger unit receipt/hash.
  - `Likely next action`: finish and seal the current unit, or stop as `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL` if context compacts first.
- `Static evidence cannot establish dynamic activation or absence`
  - `Evidence`: registries, reflection, environment, optional dependencies, or runtime discovery control the edge.
  - `Likely next action`: mark `unknown`, name the bounded evidence needed, and avoid a universal detector claim.
- `A finding appears to require implementation to verify`
  - `Evidence`: no existing test or read-only evidence can distinguish the behavior.
  - `Likely next action`: record the not-proven boundary and owner upgrade trigger; do not add a probe, test, hook, or runtime patch in this lane.

## Confirm-Don't-Trust Load Checklist

- `Packet identity`: resolve the couriered immutable commit and read `git show <transport-commit>:docs/workflows/behavioral_sci_code_audit_handoff_v0.md`; compare the result to the couriered packet SHA256.
- `Workspace`: confirm repository root, branch/ref, HEAD ancestry or exact revision, and tracked/untracked state.
- `Authority`: hash and reread every load-bearing project source in the Authority And Source Ledger; resolve conflicts by current instruction -> `AGENTS.md` -> overlay -> accepted docs.
- `Receiver capability`: confirm the receiver mechanism's actual root can write only the named ledger path before runtime source loading.
- `Runtime routes`: re-enumerate current runners, owners, tests, config, and activation surfaces; do not reuse the authoring lane's path inventory as code evidence.
- `Output boundary`: confirm `docs/workflows/behavioral_sci_code_audit_ledger_v0.md` is the only authorized write target and that no doctrine/control implementation is authorized.
- `Danger context`: confirm the commissioned worktree is distinct from the parent checkout; do not touch the parent's untracked directories.

Load outcomes:

- `REUSE`: every required load-bearing fact matches and the receiver can continue from Exact Next Authorized Action step 2.
- `PARTIAL_REUSE`: only optional/non-load-bearing context drifted; record and re-derive it while preserving verified constraints.
- `STALE_REREAD_REQUIRED`: a material source, revision, dirt state, target, or compare target drifted but can be safely re-derived before work.
- `BLOCKED_DRIFT`: drift conflicts with authority, user constraints, target path, dirty-state policy, or unknown edits.
- `BLOCKED_MISSING_PACKET`: packet path or couriered revision is absent or unreadable.
- `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be compared or re-derived; use `BLOCKED_MISSING_SOURCE` or `BLOCKED_STALE_OR_UNSTABLE_EVIDENCE` when that is the precise source-loading cause.

Sources to reread if drift is detected: the changed source itself, `AGENTS.md`, `.agents/workflow-overlay/source-of-truth.md`, the owning overlay section named in its retrieval header, and only the next route needed to resolve the conflict.

## Do Not Forget

The ledger is valuable only if a cold owner can distinguish what current evidence shows, what remains uninspected or dynamic, which gaps recur, and why a recommended control would catch the defect without creating a worse standing maintenance surface.
