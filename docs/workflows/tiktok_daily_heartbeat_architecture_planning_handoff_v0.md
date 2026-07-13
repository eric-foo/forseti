# TikTok Daily Heartbeat Architecture-Planning Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: workflow handoff packet
scope: >
  Cold-lane, planning-only handoff for choosing the target architecture of a
  daily TikTok creator-grid heartbeat while preserving platform-specific
  capture behavior and the existing Bronze-to-Silver longitudinal seam.
use_when:
  - Planning TikTok daily creator monitoring after the TikTok longitudinal Silver proof.
  - Comparing a shared social heartbeat control core with a TikTok-specific control stack.
authority_boundary: retrieval_only
stale_if:
  - branch codex/tiktok-heartbeat-architecture-handoff no longer descends from b6a98016ad53732b55cca23753ee3449fd78a822
  - any load-bearing source hash below changes before load
  - Instagram heartbeat, TikTok capture, or TikTok grid-observation behavior changes before load
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/prompt-orchestration.md
```

## Load Contract

- packet_version: 0
- mode: max
- created_at: 2026-07-14 Asia/Singapore
- created_by_lane: architecture-handoff sender lane; provenance only
- workspace_at_authoring: `C:\tmp\forseti-tiktok-heartbeat-architecture-handoff`
- handoff_path: `docs/workflows/tiktok_daily_heartbeat_architecture_planning_handoff_v0.md`
- expected_branch: `codex/tiktok-heartbeat-architecture-handoff`
- expected_head_before_packet_commit: `b6a98016ad53732b55cca23753ee3449fd78a822`
- expected_ancestry: the packet commit must descend from `b6a98016ad53732b55cca23753ee3449fd78a822`
- expected_dirty_state_after_packet_commit: clean
- load_rule: confirm-don't-trust; re-read named sources and re-verify repository state before strict or actionable claims
- receiver_output_mode: chat-only architecture result
- receiver_edit_permission: read-only; no repository edits
- implementation_authority: none
- live_operation_authority: none

## Goal Handoff

- long_term_goal: Make creator capture usable through a trustworthy, lineage-closed Forseti Silver read layer.
- anchor_goal: Choose the target architecture for a TikTok daily creator-grid heartbeat that reuses proven Instagram heartbeat control behavior and existing TikTok Bronze/Silver seams without duplicating or collapsing platform-specific capture responsibilities.
- success_signal: The receiver compares materially different architectures; selects or explicitly defers one; identifies the shared core, platform satellites, contracts, invariants, failure semantics, and deferred runtime boundary; preserves existing lineage and source-policy boundaries; and names the smallest next planning object without implementing or operating anything.

## Active Objective

Perform a standard, read-only architecture-planning pass for TikTok daily
heartbeat parity. Decide whether TikTok should use a platform-neutral social
account-window heartbeat control core with platform-specific capture adapters,
or a TikTok-specific operator stack, and define where durable Bronze commitment,
receipts, retries, Silver derivation, and future scheduling belong.

This is architecture planning, not feature implementation, runtime scheduling,
or live-capture authorization.

## Open Decision / Architecture Fork

### Decision to make

Is a TikTok daily grid heartbeat best modeled as:

1. a manual TikTok grid-capture operation followed by the current Bronze and
   Silver runners, with no heartbeat control layer;
2. a TikTok-specific clone of the existing Instagram heartbeat controller,
   run-control, and operator wrapper;
3. a shared platform-neutral **social account-window heartbeat run-control
   core** with Instagram and TikTok capture adapters/satellites; or
4. a standing scheduler/service that owns both live capture and downstream
   derivation?

The receiver may recommend a bounded hybrid, but it must locate that hybrid
within the options above and state what is shared versus platform-owned.

### Sender's provisional recommendation, to challenge

Option 3 is the leading hypothesis, narrowly defined:

- share only proven run-control mechanics: immutable daily plan, deterministic
  bucketing/lane assignment, attempt ledger, lease and retry semantics,
  duplicate prevention, bounded budgets, receipts, access-gap reporting, and
  daily/session summaries;
- keep source access and capture semantics in platform satellites;
- define heartbeat success at a verified, committed Bronze packet plus an
  honest control receipt;
- keep Silver derivation downstream through the existing seam-cadence/producer
  machinery, optionally invoked after Bronze commitment but not made part of
  source-capture success;
- remain scheduler-ready but do not introduce a standing scheduler or service
  in this decision.

This recommendation is not frozen. Reject it if the current Instagram
run-control contracts are too coupled to Instagram or if extraction would cost
more and create more drift than a TikTok-specific stack for the bound outcome.

### Trade-offs the recommendation must resolve

| Question | Shared-core pressure | Platform-specific pressure |
| --- | --- | --- |
| Planning and retry | Daily plan, bucket, lease, attempt, retry, summary, and duplicate-prevention semantics should not drift by platform. | Platform access failures and completion signals differ. |
| Capture scope | Both lanes observe a bounded creator account window and emit one capture result per creator attempt. | Instagram is first-visible grid/no scroll; TikTok's useful grid window has historically required controlled scrolling. |
| Session/egress | Stable lane partitioning, bounded work, and stop-on-access-risk are reusable controls. | Instagram and TikTok use different browser/session/access postures; TikTok currently depends on retained Chrome CDP state. |
| Bronze | Both should preserve immutable source evidence and source capture time. | Packet schemas and source-surface evidence remain platform-specific. |
| Silver | Packet-grain account-window observation sets and exact-policy readers are reusable concepts. | TikTok has the implemented adapter; Instagram/YouTube are documented follow-ons, not current parity. |
| Scheduling | An operator-controlled command can later be scheduled. | No current evidence supports a permanent service, automated challenge handling, or proven 2,500-creator throughput. |

### Owner and reversal condition

- architecture owner: receiving planning lane recommends; user accepts or redirects
- implementation owner: none in this handoff
- reversal condition: prefer a TikTok-specific stack if source inspection shows
  the apparent shared run-control is materially bound to Instagram data shapes,
  browser semantics, or policy in ways that cannot be separated without a
  speculative framework or high ongoing maintenance burden

## Drift Guard

- Do not implement, edit runtime code, add schemas, patch tests, or create a
  patch queue.
  - why: the commissioned act is architecture selection.
  - breakage if violated: substitutes build decisions for the owner-facing
    architecture decision and exceeds the receiving lane's authority.
- Do not run live TikTok or Instagram capture, open platform sessions, solve
  challenges, configure proxies/egress, or register a scheduled task.
  - why: no live-operation authority is present.
  - breakage if violated: changes external state and confuses planning with
    access validation.
- Do not write Bronze, Silver, Creator Registry, Cleaning, ECR, Gold, or
  Judgment data.
  - why: source and data-lake mutations are outside the planning lane.
- Do not treat the existing TikTok onboarding runner as a heartbeat runner.
  - why: it always performs suggested-account discovery, grid capture,
    top-eight selection, and deep capture in one retained browser context.
- Do not treat the current TikTok grid-packet runner as live capture.
  - why: it admits one already-created `tiktok_grid_window.json` as Bronze.
- Do not collapse Instagram and TikTok into one source-policy or one capture
  adapter.
  - why: their window, scrolling, browser, challenge, and evidence semantics
    differ.
- Do not infer that Instagram's heartbeat is a standing scheduler.
  - why: it is an operator-run controller plus run-control and wrapper; the
    runbook's Windows Task Scheduler example is optional and disabled.
- Do not treat the 2,500-creators/day direction as measured capacity.
  - why: scale, access safety, storage economics, and throughput are unproven.
- Do not widen into Instagram/YouTube adapter implementation.
  - why: those platforms are future consumers that inform the core boundary,
    not current build scope.
- Do not recommend a broad social scheduler/framework merely for future-proofing.
  - why: sharing must be justified by present repeated mechanics, not an
    imagined platform estate.
- Do not change Silver record contracts or reconcile cross-platform metrics.
  - why: existing TikTok longitudinal mechanics are a constraint and evidence,
    not a redesign invitation.

## Exact Next Authorized Action

1. Confirm repository path, branch, ancestry, clean state, packet readability,
   and every load-bearing source hash.
2. Read `AGENTS.md` and the overlay README, source-loading, decision-routing,
   and prompt-orchestration sources.
3. **REFERENCE-LOAD** the architecture-planning skill contract. Do not apply it
   until the source-loading declaration below is complete.
4. **SOURCE-LOAD** the named Instagram heartbeat, TikTok capture/Bronze/Silver,
   data-lake boundary, tests, follow-on, and prior review sources.
5. Declare exactly one of:
   - `SOURCE_CONTEXT_READY`: all decisive sources are available and current;
   - `SOURCE_CONTEXT_INCOMPLETE`: name what is missing and stop with
     `NEEDS_SOURCE_CONTEXT` if the missing source could change the decision.
6. If ready, run three local, de-correlated passes:
   - directional: identify the smallest architecture that fully serves daily
     TikTok account-window monitoring;
   - adversarial: attack clone drift, premature abstraction, false scheduler
     assumptions, hidden platform coupling, and failure masking;
   - grounding: map each proposed responsibility to current code, doctrine, or
     an explicit future contract.
7. Compare the four architecture options and return exactly one architecture
   result in chat. Do not edit the repository.

## Required Architecture Output

Return one of the architecture-planning skill's allowed result states, with
`TARGET_RECOMMENDED` preferred only when evidence supports a selection. The
chat response must include:

1. **Decision** — one sentence naming the target architecture or the reason no
   selection can yet be made.
2. **Why this shape** — decisive present-tense evidence, not generic platform
   theory.
3. **Options compared** — all four options, including why each rejected option
   fails the bound outcome or has worse maintenance/lock-in.
4. **Core/satellite boundary** — a table or compact map of:
   - shared heartbeat run-control core;
   - Instagram capture satellite;
   - TikTok capture satellite;
   - Bronze packet writers;
   - Silver derivation/readers;
   - future scheduler/runtime shell.
5. **End-to-end event sequence** — plan freeze through capture attempt,
   committed Bronze, receipt/acknowledgement, retry/access gap, optional Silver
   catch-up, and queryable history.
6. **Contracts and invariants** — identities, time, idempotency, leases,
   duplicate prevention, completion, acknowledgement, lineage, missingness,
   and fail-loud behavior.
7. **Failure ownership** — which layer owns challenge/access failure, partial
   packet, retry, malformed Bronze, failed Silver derivation, and query
   ambiguity.
8. **Maintenance burden** — current extraction/build cost and long-term cost at
   many platforms and roughly 2,500 creators, with unproven estimates clearly
   labeled.
9. **Accepted residuals** — every limitation preserved by the recommended
   architecture and why it is acceptable now.
10. **Reversal triggers** — evidence that would justify cloning, sharing more,
    or introducing a standing scheduler later.
11. **Smallest next planning object** — the minimum implementation-scoping or
    thin-spec artifact needed after owner acceptance; do not author it.

Do not include implementation steps, file diffs, code, test commands to run as
part of implementation, PR instructions, or a readiness claim.

## Forseti Start Preflight

```yaml
forseti_start_preflight:
  workspace: C:\tmp\forseti-tiktok-heartbeat-architecture-handoff
  branch: codex/tiktok-heartbeat-architecture-handoff
  base_head_before_packet_commit: b6a98016ad53732b55cca23753ee3449fd78a822
  dirty_state_before_authoring: clean
  agents_read: yes
  overlay_read: yes
  source_pack: bounded_custom
  repo_map_decision: loaded
  repo_map_reason: >
    The map routes Data Capture and docs/workflows; the named owning sources,
    not the map summary, remain authoritative for architecture facts.
  target: TikTok daily creator-grid heartbeat target architecture
  authoring_edit_permission: docs-only, this handoff packet
  receiver_edit_permission: read-only
  receiver_output_mode: chat-only
  doctrine_change_posture: none; advisory target architecture only
  external_source_boundary: Forseti only; no jb rules or artifacts
  validation_expectation: >
    Confirm source hashes and state, then compare options using local
    directional, adversarial, and grounding passes. No runtime validation.
```

## Inherited Context (Does Not Flow Automatically)

### What has already been proven

- TikTok grid-only Bronze admission exists for a previously captured grid
  window.
- One eligible TikTok grid Bronze packet can deterministically produce one
  packet-grain Silver `MetricObservationSet`.
- The exact-policy longitudinal reader retrieves repeated observations by
  platform-native video ID, not grid position.
- The earlier TopFrag metric-mechanics proof admitted one eight-video batch
  packet and ran its metric producer twice append-only, producing 80
  `MetricObservation` records and two rollup siblings; lineage, policy
  fingerprints, record counts, read idempotency, supersession selection, and
  reader selection passed. This was not the later packet-grain grid-observation
  shape.
- The separate grid-longitudinal lane used the pinned 32-row TopFrag grid
  artifact in its authoring scratch proof. The delegated post-patch review
  re-hashed and checked artifact compatibility but explicitly did not rerun that
  end-to-end scratch execution; it did run 102 focused unit tests and 45
  contract tests successfully.
- TikTok Silver is therefore not the missing layer. The missing layer is the
  live daily grid-capture/run-control path that supplies committed Bronze
  packets safely and repeatedly.

Re-read the report and implementation before repeating these as current facts.

### What exists for Instagram

Instagram daily heartbeat is a three-layer operator-controlled system:

1. `run_source_capture_ig_daily_heartbeat.py` reads a roster, assigns stable
   lanes, runs bounded first-visible-grid capture, and emits per-creator
   receipts/access gaps.
2. `run_source_capture_ig_daily_heartbeat_control.py` freezes the daily plan,
   assigns deterministic buckets, maintains the attempt ledger, prevents
   duplicate attempts, manages leases/retries, and emits session/daily
   summaries.
3. `run_source_capture_ig_daily_heartbeat_operator.py` ensures the plan, runs
   one bucket/lane, and summarizes the result in one operator invocation.

It explicitly does not register schedules, choose egress, solve challenges,
or add Silver/Gold monitoring logic. Operators can schedule repeated
invocations externally; that does not make the runner a standing service.

The policy direction is one daily first-visible Reels-grid heartbeat per
active creator, with no pagination, scroll expansion, item fan-out, comments,
or platform writes. Deep capture is triggered separately from external
breakout candidates.

### What exists for TikTok

- The creator-onboarding runner is not cadence-safe: it performs suggested
  accounts, grid capture, top-eight selection, and deep capture in one retained
  Chrome CDP context.
- The grid packet runner is not a browser runner: it admits one already-created
  `tiktok_grid_window.json` into immutable Bronze.
- TikTok onboarding currently depends on a retained authenticated Chrome CDP
  session/user-data posture. Source policy distinguishes an owner-authorized
  bounded X/Close follow-through from an unresolved challenge; unresolved
  challenges stop the account/context, and no puzzle solving is authorized.
- The useful grid target has historically been a 32-row window and may require
  controlled scrolling, unlike Instagram's first-visible-only policy.
- Daily heartbeat must exclude comments, subtitles/transcripts, deep capture,
  suggested-account discovery, top-eight selection, and item fan-out.
- Comments and subtitles are performance-triggered enrichment and generally
  captured once, not daily.

### Bronze and Silver ownership boundary

- Bronze owns immutable source evidence and the capture-time account window.
- Silver owns deterministic, lineage-closed normalized observations and
  retrieval across repeated packets.
- A missing capture day produces no Silver observation.
- A video absent from a later bounded window is not zero and is not carried
  forward.
- Stable history identity is platform/account/content-native ID; source grid
  position is audit evidence only.
- A successful live heartbeat should not be reported before the Bronze packet
  is committed and verified.
- A failed Silver derivation must remain visible, but it should not cause a
  second live source capture of the same successfully committed account window.

### Existing downstream cadence

`run_seam_cadence.py` runs derived catch-up, including TikTok grid observations
and comment attention. It is not a live-capture scheduler. Architecture must
decide whether a heartbeat operator merely leaves committed Bronze for this
downstream cadence or invokes it as a post-commit step while preserving the
separate success/failure domains.

### Future-platform pressure

The documented longitudinal follow-on names the portable unit as an
**account-window observation packet**, not a grid:

- Instagram already has a Reels-grid Bronze seam but not the shared
  packet-grain Silver adapter.
- YouTube's cheap daily surface is channel RSS, not a grid, and lacks comment
  count.
- These are evidence that shared control should not depend on the word “grid”
  or a TikTok packet schema.
- They do not authorize building Instagram/YouTube adapters now.

## Architecture Constraints and Invariants

### Control-plane invariants

- A daily plan is frozen and auditable before work begins.
- Creator-to-bucket/lane assignment is deterministic for a plan.
- At most one live attempt may own a creator/plan/lane unit at a time.
- Leases expire visibly; retry eligibility is explicit.
- A retry cannot silently become a duplicate successful capture.
- Time and creator budgets are bounded.
- Stop/pause conditions remain platform-specific and fail visible.
- A receipt distinguishes completed capture, access gap, challenge, skipped,
  retryable failure, terminal failure, and budget exhaustion as supported by
  the actual sources; do not fabricate unsupported states.

### Data-plane invariants

- Source capture time comes from the capture event, not downstream producer
  wall-clock time.
- Bronze is immutable and preserves the platform-specific source evidence.
- Packet admission and Silver acknowledgement occur only after durable write
  and readback validation.
- Non-target packets are acknowledged explicitly without being treated as
  produced records.
- Deterministic record IDs and policy fingerprints make reruns idempotent.
- Silver lineage binds exact packet/file IDs and stored-byte hashes.
- Readers require the exact policy fingerprint and deterministic record ID;
  they do not guess latest.
- Equal-time distinct records for the same subject/policy fail closed.
- Missing, hidden, unsupported, literal zero, and unparseable metrics retain
  distinct postures.

### Platform-bound invariants

- Instagram: first-visible Reels grid, no scroll/pagination/fan-out.
- TikTok: controlled creator-grid window under retained CDP access; no
  discovery, comments, transcripts, deep capture, or item fan-out.
- YouTube future pressure: account-window can be RSS enumeration rather than a
  grid or browser operation.
- Platform-native content ID is identity; position is never identity.

## Architecture Options to Compare

### AO-1 — Manual TikTok live grid capture plus current Bronze/Silver runners

- shape: an operator performs/produces `tiktok_grid_window.json`, then invokes
  grid packet admission and existing Silver derivation
- attraction: smallest immediate code surface
- risk: no frozen plan, attempt ledger, stable bucketing, lease/retry control,
  duplicate prevention, or fleet-level missingness/access-gap visibility
- decision test: can this honestly satisfy daily multi-creator monitoring, or
  only one-off proof?

### AO-2 — TikTok-specific clone of the Instagram heartbeat stack

- shape: copy/adapt controller, run-control, and operator wrapper into TikTok
  files
- attraction: bounded platform ownership and low initial extraction work
- risk: duplicated plan/lease/retry/receipt semantics drift, multiplied fixes,
  and future Instagram/TikTok divergence in generic control behavior
- decision test: is the existing control logic materially Instagram-bound
  enough that duplication has lower compounded cost?

### AO-3 — Shared account-window heartbeat run-control core plus platform satellites

- shape: common plan/bucket/attempt/lease/retry/receipt/summary contracts;
  platform adapters own roster-to-capture invocation, session/access behavior,
  window policy, Bronze packet formation, and platform failure mapping
- attraction: one control truth while preserving source-family boundaries
- risk: premature abstraction, lowest-common-denominator capture contract, or
  hidden leakage of Instagram assumptions into TikTok
- decision test: can the common core be described entirely in platform-neutral
  terms already proven by at least Instagram and needed immediately by TikTok?

### AO-4 — Standing scheduler/service owns capture and downstream processing

- shape: durable service schedules creators, selects lanes/egress, runs live
  capture, commits Bronze, invokes Silver, and monitors the fleet
- attraction: maximum automation and centralized operations
- risk: unproven access safety/throughput, service lifecycle and state-store
  burden, coupled live and derived failures, higher lock-in, and scope far
  beyond the current operator-controlled evidence
- decision test: what bound requirement becomes false without a standing
  service now? If none, defer it.

## Failure-Ownership Questions the Receiver Must Answer

| Failure | Candidate owner | Required behavior |
| --- | --- | --- |
| Browser/session unavailable | platform capture satellite | fail visible; no fake packet; retry posture explicit |
| Platform challenge/access gap | platform capture satellite mapped into shared receipt | stop/pause according to platform policy; do not solve challenge automatically |
| Budget exhausted before creator attempt | shared run-control | record unattempted/deferred posture distinctly from capture failure |
| Partial or malformed capture artifact | platform capture/Bronze admission | do not acknowledge completion or emit partial Silver |
| Bronze commit/readback failure | Bronze writer/admission | live attempt not complete; durable failure remains queryable |
| Bronze committed, Silver derivation fails | Silver producer/cadence | preserve Bronze success and derived failure; do not recapture source automatically |
| Duplicate operator invocation | shared run-control | lease/ledger prevents duplicate owner or duplicate successful attempt |
| Exact-policy history ambiguity | Silver reader | fail closed; never choose by packet order |
| Content leaves bounded account window | no failure; data semantics | no new row, no zero, no carry-forward |

## Known Residuals and Review Findings

Treat these as architecture inputs, not patch requests:

- TikTok handle case preservation can split histories; normalization is an
  owner decision and is not part of this architecture lane.
- Dual admission of the same grid state can create equal-time ambiguous Silver
  siblings; the current operational mitigation is to prevent dual admission.
- TikTok grid producer target matching uses a filename-suffix check with a
  hypothetical collision risk.
- Malformed legacy receipt time has no retirement path.
- A separate comment-attention runner can return success on an availability
  reconciliation failure; this is not a grid-heartbeat blocker.
- TikTok live source scale and account safety are unproven.
- Bounded grid windows produce sparse longitudinal history; absence is not a
  negative observation.
- Storage, retention, and 2,500-creator throughput economics have not been
  validated.

The architecture should avoid making these worse and should name any one that
becomes load-bearing for the selected design. It must not patch them.

## Authority and Source Ledger

All file hashes are SHA-256 at base head
`b6a98016ad53732b55cca23753ee3449fd78a822`. Re-read every load-bearing source;
a matching hash confirms bytes, not understanding.

### Project and workflow authority

- `AGENTS.md`
  - role: canonical project instruction source
  - compare target: reread-required
  - verify before: any planning or output
- `.agents/workflow-overlay/README.md`
  - role: Forseti workflow overlay front door
  - compare target: reread-required
- `.agents/workflow-overlay/source-loading.md`
  - role: progressive source-load contract
  - compare target: reread-required
- `.agents/workflow-overlay/decision-routing.md`
  - role: planning/delegation/isolation route
  - compare target: reread-required
- `.agents/workflow-overlay/prompt-orchestration.md`
  - role: durable handoff and model-routing boundary
  - compare target: reread-required
- architecture-planning skill contract
  - role: output mechanics only; project sources remain authoritative
  - compare target: reread-required from the receiver's available skill source

### Capture toolbox and TikTok source-family authority

- `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - role: capture lifecycle and operating boundary
  - compare target: reread-required
- `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
  - role: current recon routing/status
  - compare target: reread-required
- `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md`
  - role: TikTok source-family front door; staging, scale, and account-safety posture
  - SHA256: `82F36630605F275DC84EC4F2287C957E0A280C69699BFADCAE416067A9E98021`
- `forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  - role: TikTok capture policy and lane contract
  - SHA256: `DEBA165F1609C6ADA28C102874910BBC25E58F1BA64EF4DBA387261A87E2097F`

### Instagram heartbeat evidence

- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`
  - role: daily scope, source footprint, scale direction, and exclusions
  - SHA256: `DCE5831C1A9BA6F4E35C822C1C72E1103DA8BBA167DF73BAB182F75601C5569D`
- `forseti-harness/runners/run_source_capture_ig_daily_heartbeat.py`
  - role: roster/lane controller, bounded capture, receipts/access gaps
  - SHA256: `AA2D8624B6A979491A5F9644C355B8CE403A55972A44A5509AF9264D5E7D3E85`
- `forseti-harness/runners/run_source_capture_ig_daily_heartbeat_control.py`
  - role: frozen plans, buckets, attempt ledger, duplicate prevention, leases, retries, summaries
  - SHA256: `9071CE9A7DF8E0EFCB9F00441B357D898E0F7CF75BECB410FE6D200918A406B6`
- `forseti-harness/runners/run_source_capture_ig_daily_heartbeat_operator.py`
  - role: one-invocation operator wrapper and explicit non-scheduler boundary
  - SHA256: `6FDCA63BFCF0F3134C8523A5C649D4946B1C411E793D706319A3CCA3B3B362EE`
- `docs/workflows/ig_daily_heartbeat_operator_runbook_v0.md`
  - role: operator procedure and optional disabled scheduler template
  - SHA256: `25E344B30876251AD648BE19B216FE04DDFC801474CAD38CBBC50FF88D4AA5AE`
- `forseti-harness/tests/unit/test_ig_daily_heartbeat_runner.py`
  - role: executable evidence for controller behavior
  - SHA256: `2211FC600F923731F67ADF6C282F4C228659FEF571BFBDE135F4F9901717CEB1`
- `forseti-harness/tests/unit/test_ig_daily_heartbeat_control.py`
  - role: executable evidence for plan/ledger/lease/retry behavior
  - SHA256: `2D9D4A23A0742F27BC90BE6530C17178E552787D03B32D6E538FAD6CC6D50B26`

### TikTok live-capture and Bronze evidence

- `forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py`
  - role: current all-in-one onboarding entry point; proves it is not heartbeat-safe
  - SHA256: `206C5EB04C520B9C9A150DF0E76BB54FCA555AE351FBA3227862C479FD9141DA`
- `forseti-harness/source_capture/tiktok/creator_onboarding.py`
  - role: retained CDP session and suggested/grid/select/deep-capture sequence
  - SHA256: `0BEB91518E1277F83715FDD68451FCE5F9D9E68ED712BBA8BD91CA8751C76883`
- `forseti-harness/runners/run_source_capture_tiktok_grid_packet.py`
  - role: CLI admitting an existing grid window, not live capture
  - SHA256: `5E42E8B192CF150777C5A68C1C49AF06CB6F3E2A0F35908558E5B72531380A0C`
- `forseti-harness/source_capture/tiktok/grid_packet.py`
  - role: grid-only Bronze packet validation and durable write
  - SHA256: `CBD27F1B223A13AA178CEE19F758F257F9DDC83DFCAA2C10224933FDE6778EF3`
- `forseti-harness/tests/unit/test_tiktok_grid_packet.py`
  - role: executable Bronze-admission behavior
  - SHA256: `A830895B925B28B8D81F037C462672C81D7F98937A72AEF8FABB9ECF452B429B`

### TikTok Silver and retrieval evidence

- `forseti-harness/runners/run_tiktok_grid_observation_producer.py`
  - role: packet acknowledgement, target selection, deterministic derivation, readback
  - SHA256: `A8627A51E7C4662A6154FD1C55371E947D64EA27DCCAA6C142C325655EF47A37`
- `forseti-harness/capture_spine/creator_profile_current/tiktok_grid_observation_producer.py`
  - role: policy fingerprint, deterministic record, row shape, lineage, content hash
  - SHA256: `24C548D70407ED6DEC769883CACBD76FA61CAEBD42BCE6807DDF7FEFCE529997`
- `forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py`
  - role: exact-policy longitudinal selection and ambiguity failure
  - SHA256: `E954E66825841E7004CD15365CDB7E5E03BC3309854226B55102591D0361EA30`
- `forseti-harness/runners/run_seam_cadence.py`
  - role: derived catch-up registration; explicitly not live scheduling
  - SHA256: `F80E36E427FE4B0B8061E6CDC84892256E73655EF3B3EFDE5370302D392D4356`
- `forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py`
  - role: executable producer and idempotency evidence
  - SHA256: `84EE98BD6BE04CADE59E7AB73DE66981BBBCAA4B11D4B565CD1B7BCD9E8E4577`
- `forseti-harness/tests/contract/test_silver_reader_selection_gate.py`
  - role: reader selection, fingerprint, and ambiguity gate
  - SHA256: `6F7DBD0FE48CC00309A658E3C35353AF7764435E0CDB979C7AF4F87CFD111DD1`

### Architecture, contract, proof, and review context

- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - role: Silver record/lineage/idempotency/selection authority
  - SHA256: `A43ABF02E63270262248948D9128806FF8BBE41C527335929CC3127E8A6AD026`
- `forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  - role: Capture/Silver/Cleaning ownership boundary
  - SHA256: `0CAF4B40D9DD141503E64F8E4D3A260CE4FB0B67AFCAA0431F19DE74BF75B50A`
- `docs/workflows/social_grid_longitudinal_followon_v0.md`
  - role: account-window abstraction and Instagram/YouTube future pressure
  - SHA256: `A45B203E525810BBF4F7E6F9ADD4A5B8AED99C7ACBF90632A002A0085EB5CC69`
- `docs/workflows/topfrag_silver_lake_mechanics_test_report_v0.md`
  - role: scratch-only proof and exact observed counts
  - SHA256: `0C0DBCE95237E4CBBC1ECFFFF639DB0C3986DD8368BC8ED826EF6EDAE2816434`
- `docs/review-outputs/tiktok_grid_longitudinal_silver_delegated_adversarial_review_v0.md`
  - role: accepted implementation and residual findings
  - SHA256: `D77E8D161162B48E5B680CFCE019076E226FB4E36DE4A942750F68A023F9303C`

## Frozen Decisions

- Decision: daily heartbeat is grid/account-window monitoring only.
  - consequence: discovery, selection, deep capture, comments, and transcripts
    stay outside the daily runner.
- Decision: use platform-native content ID, never grid position, for history.
  - consequence: reordering and window movement do not create new identities.
- Decision: preserve immutable Bronze timepoints and derive Silver separately.
  - consequence: no in-place metric update and no recapture to repair downstream
    derivation.
- Decision: account-window is the portable concept; grid is platform-specific.
  - consequence: a shared control core cannot require browser-grid semantics.
- Decision: no standing scheduler is authorized or proven.
  - consequence: target architecture should expose a scheduler-ready operator
    seam and defer the runtime shell unless current evidence proves it necessary.
- Decision: no cross-platform metric reconciliation in this lane.
  - consequence: `view_count`, `like_count`, and `comment_count` postures remain
    source-policy-specific even when the control plane is shared.

## Mutable Questions

- Can Instagram's plan/ledger/lease/receipt types be extracted without carrying
  Instagram source policy into the core?
- Is the smallest complete route an extraction used by both Instagram and
  TikTok immediately, or a common contract first with Instagram migration
  deferred?
- Does TikTok need one live grid-capture runner plus the existing Bronze writer,
  or should its adapter own capture-and-admission as one atomic operator action?
- Does operator success stop at verified Bronze, or report separate Bronze and
  Silver post-commit statuses in one invocation?
- Which identity owns the daily plan: creator-registry linkage, platform-native
  account ID/handle, or an immutable roster sidecar? Current code must decide
  what can be reused without registry mutation.
- Which retry states are genuinely common, and which are platform error
  mappings into a smaller shared vocabulary?
- Is egress/lane assignment generic control metadata while session selection
  remains platform-owned?
- What minimum state store is required at 2,500 creators: current file-backed
  plan/ledger, a partitioned file layout, or a database? Do not recommend a
  migration without evidence that the current bound outcome becomes false.

## Superseded or Dangerous-to-Reuse Context

- “TikTok onboarding runner can be scheduled daily.”
  - why dangerous: it performs deep capture and discovery/select work.
  - replacement: a new bounded grid-only live capture seam is required.
- “TikTok grid packet runner captures the grid.”
  - why dangerous: it only admits a supplied JSON artifact.
  - replacement: distinguish live capture adapter from Bronze admission.
- “Instagram heartbeat is our scheduled heartbeat runner.”
  - why dangerous: it is operator-controlled; scheduler registration is absent.
  - replacement: treat it as scheduler-ready run-control evidence.
- “Silver should overwrite the latest view/like count.”
  - why dangerous: it destroys time-series evidence.
  - replacement: immutable Bronze packet per capture and immutable Silver
    observation set per eligible packet/policy.
- “One shared social grid runner.”
  - why dangerous: YouTube RSS and TikTok/Instagram access policies disprove
    grid as a portable acquisition abstraction.
  - replacement: shared account-window control plus platform satellites, if
    option comparison confirms it.
- “2,500 creators/day is proven.”
  - why dangerous: it is an owner direction without measured live evidence.
  - replacement: design for bounded partitioning while retaining an explicit
    unproven scale residual.

## Current Task and Repository State

- Completed before this handoff:
  - TikTok grid Bronze admission and packet-grain Silver longitudinal adapter
    merged through PR #896 (`4ffaf718`).
  - technical diagnostics direct repo-map route merged through PR #907; base
    head is `b6a98016`.
  - TopFrag scratch proof completed with no live-lake or registry mutation.
- Not completed:
  - no TikTok daily live grid-only heartbeat controller;
  - no TikTok plan/ledger/operator run-control;
  - no registered scheduler/service;
  - no proven 2,500-creator live throughput;
  - no Instagram/YouTube packet-grain Silver parity.
- Workspace before packet authoring:
  - `C:\tmp\forseti-tiktok-heartbeat-architecture-handoff`
  - branch `codex/tiktok-heartbeat-architecture-handoff`
  - head `b6a98016ad53732b55cca23753ee3449fd78a822`
  - clean and tracking `origin/main`
- Receiver must freshly verify branch, ancestry, dirty state, packet commit,
  source hashes, and all absence claims against current code.

## Changed / Inspected / Tested

### Changed

- `docs/workflows/tiktok_daily_heartbeat_architecture_planning_handoff_v0.md`
  - status: new docs-only cold-lane handoff
  - authority: retrieval and task routing only; not architecture doctrine

### Inspected by sender

- All hashed sources in the ledger were located and selectively read for the
  facts summarized here.
- Instagram controller, control, operator wrapper, and runbook were compared.
- TikTok onboarding, grid admission, Silver producer/reader, seam cadence,
  proof report, follow-on, and delegated review were compared.

### Tested

- No runtime tests were run for this documentation-only handoff.
- Prior test/proof claims in the packet are inherited evidence and must be
  re-read at their named sources; they are not validation of a future
  architecture or implementation.

## Confirm-Don't-Trust Load Checklist

1. Confirm the repository/worktree named by the receiver is the intended
   Forseti workspace.
2. Confirm the handoff exists, is committed, and descends from the expected
   base head.
3. Confirm clean state or classify every dirty/untracked file before proceeding.
4. Recompute every supplied hash; if any load-bearing source differs, reread it
   and classify the drift rather than silently reusing this packet.
5. Reread project/overlay authority and the architecture-planning contract.
6. Reread the Instagram control stack, TikTok capture/Bronze/Silver stack, and
   the proof/review/contract sources.
7. Verify the key absence claims with current code: no TikTok grid-only live
   heartbeat, no scheduler registration, no current Instagram/YouTube
   packet-grain parity.
8. Declare one load outcome:
   - `REUSE`: all load-bearing facts match;
   - `PARTIAL_REUSE`: only non-decisive context drifted;
   - `STALE_REREAD_REQUIRED`: current sources supersede packet summaries but
     can be safely reloaded;
   - `BLOCKED_DRIFT`: branch, authority, dirty state, or source conflict changes
     the decision problem;
   - `BLOCKED_MISSING_PACKET`: packet cannot be opened;
   - `BLOCKED_UNVERIFIABLE`: a decisive source cannot be checked.

## Do Not Forget

- The missing capability is **daily live TikTok grid-only capture and
  run-control**, not TikTok Silver longitudinal storage.
- Instagram provides behavioral evidence for heartbeat control, but it is not
  a standing scheduler and its capture policy is not TikTok policy.
- TikTok onboarding and TikTok grid Bronze admission are two different seams;
  neither is the desired heartbeat by itself.
- Bronze completion and Silver derivation are separate failure domains.
- Share control only where present evidence proves repetition; keep source
  access, window policy, raw evidence, and platform failure mapping in
  satellites.
- The receiver plans and reports in chat only. No repository or external-state
  mutation is authorized.
