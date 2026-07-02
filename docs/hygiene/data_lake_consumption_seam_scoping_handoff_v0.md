# Handoff Packet

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff checkpoint
scope: >
  Seed packet for a NEW Data Lake consumption-seam lane: scope (docs-only
  route) the shared derived-lane pickup/acknowledgement helper contract, the
  derived_retrieval rebuild command, and the on-demand-first metrics policy,
  so Silver/ECR/cleaning/projection lanes integrate with Bronze through one
  tested seam. Runs concurrently with, and independent of, the Gate ADR
  ratification path.
use_when:
  - Starting the consumption-seam scoping lane in a fresh thread or worktree.
  - Checking what the seam is, what already exists, and what is deliberately missing.
  - Checking the drift guard before any seam design or implementation-scoping step.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
stale_if:
  - The seam scoping route is authored and accepted (this packet is then history).
  - The Storage, Physicality-Location, Derived-Layout, or Write-Boundary contract changes the seam boundary.
  - The owner redirects away from consumption-seam work.
```

## Load Contract

- packet_version: workflow-handoff max v0
- mode: max
- created_at: 2026-07-02
- created_by_lane: Anthropic/Claude session lane (Gate ADR batch thread); provenance only, not authority
- workspace: receiver creates a FRESH worktree/branch off `origin/main`; do not use the Gate ADR lane worktree
- handoff_path: `docs/hygiene/data_lake_consumption_seam_scoping_handoff_v0.md`
- expected_branch: authored on `claude/gate-adr-b5-adjudication` pre-PR; receiver must verify this packet is reachable on `origin/main` (`git ls-tree origin/main -- docs/hygiene/data_lake_consumption_seam_scoping_handoff_v0.md`) before continuing
- expected_dirty_state_including_handoff_file: receiver's fresh worktree should be clean
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: The Data Lake feeds product surfaces (creator-signal, judgment) with provable, source-backed facts without weakening raw authority or making the lake smart.
- anchor_goal: Produce an accepted, docs-only implementation-scoping route ("consumption seam v0") covering exactly three pieces: (1) a shared derived-lane pickup/acknowledgement helper contract, (2) the `indexes/derived_retrieval/` rebuild command, (3) an on-demand-first precompute policy for the first required metric families.
- success_signal:
  - core_success: An implementation lane could execute the route after explicit bounded owner authorization, and every derived lane (Silver, ECR, cleaning, projection) would pick up committed Bronze work the same tested way, with metrics views rebuildable and never authoritative.
  - boundary: The route itself authorizes nothing; scoping output is a decision artifact, not implementation, validation, or readiness.
  - drift_cue: The lane is drifting if it starts writing runtime code, designs a queue/event system as truth, edits lake-core primitives, or selects a backend.

## Open Decision / Fork

- decision: Which metric families / consumers seed the first read models?
  - options: creator-signal-facing metrics (creator/content view-count style families over IG/YouTube/TikTok); movement-threshold (spike-alert) derivations; or scoping the seam plumbing first with metric families left as a named placeholder.
  - already constrained / off the table: SQL query-table implementation stays governance/latency-gated by the derived-layout contract; on-demand computation is the default posture; precomputed views are rebuildable caches only.
  - owner of the call: Owner. This input was requested and not yet supplied — mark `operator_to_fill` in the route if still absent.
  - recommendation: scope the plumbing (pickup helper + rebuild command) unconditionally; scope the metric-policy piece against whichever family the owner names, else as a parameterized placeholder.

## Drift Guard

- No queue, scheduler, event bus, or notification system may become the truth for pickup; by-key discovery over committed state plus lane-owned acknowledgements is the authority (storage contract). A queue may only ever be a later optimization.
- Pickup logic stays lane-side. Nothing in the lake core (`DataLakeRoot`, catalog, availability) gains scheduling, routing, retry, or lane-calling behavior.
- All read models / metrics views live under `indexes/derived_retrieval/`, rebuildable and non-authoritative, manifest-backed per the Silver Vault contract.
- No backend/engine selection anywhere in this lane; no Gate ADR territory (AR body layout, retention/erasure) may be touched.
- This lane is SCOPING ONLY (docs-write). Implementation requires a later explicit bounded owner authorization; the route must say so.
- Do not interfere with the Gate ratification path; the seam consumes only public Bronze surfaces, which the Gate 1 ADR pins as stable.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`; hierarchy: `.agents/workflow-overlay/source-of-truth.md`.
- targets to enter the ladder: `AGENTS.md`; overlay README; then the ledger below.
- already loaded by sender (weak orientation, 2026-07-02; not authority): storage, physicality-location, AR-implementation, Silver Vault contracts; two-family consumer-proof closeout; Gate 1/2 ADRs.
- must load first (before strict or actionable steps): the derived-layout + index-rebuild contract and the write-boundary enforcement contract — the sender did NOT read these in full, and they OWN the seam's two central questions (derived addressing/rebuild governance; write-boundary enforcement and ack discipline).
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- By-key discovery is authority before any queue; a future queue only optimizes notification.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md` (Write And Read Discipline; success signal 4)
  - compare target: reread-required | verify before: any pickup-design claim.
- Acknowledgement Log = append-only lane-owned completion facts keyed to raw; must not become lake-consumed control flow.
  - decided in: storage contract Record-Kind Slots; physicality contract Directory Slot Contract (`acknowledgements/`)
  - compare target: reread-required | verify before: ack-discipline design.
- `indexes/derived_retrieval/` rebuild command is a named MGT accepted residual with upgrade trigger "first consumer needs a reverse lookup"; build is governance/scan-latency-gated by the derived-layout contract; medallion posture prefers on-demand.
  - decided in: physicality contract MGT Accepted Residuals; derived-layout + index-rebuild contract (sender did not read the latter — treat its exact governance as unknown until read)
  - compare target: reread-required | verify before: claiming the rebuild command is unblocked.
- Owner stated (this thread, 2026-07-02, user-stated not source-proven): metrics are now required ("precompute / on demand metrics we require") — the sender treats this as the rebuild-command trigger arguably firing; the receiving lane must confirm against the derived-layout contract's actual trigger wording.
- Silver Vault v4.1 record contract is spec-complete (`SPEC_COMPLETE_READY_FOR_SCOPING`) with generated read models under `indexes/derived_retrieval/silver_vault/...`, manifest-row obligations, and posture rules preventing missing-evidence-as-zero.
  - decided in: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - compare target: reread-required | verify before: read-model or manifest design claims.
- Gate 1 ADR (awaiting ratification) pins the public Bronze read surfaces (`source_surface_catalog_rows`, `load_attachment_record_body`) as the only consumer resolution path — which is what makes seam work gate-independent.
  - decided in: `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md` (output 4)
  - compare target: reread-required | verify before: relying on surface stability.

## Active Objective

Scope "consumption seam v0" as a non-executing implementation route: shared pickup/ack helper contract for all derived lanes, the derived_retrieval rebuild command, and the on-demand-first metrics policy for the owner-named metric families.

## Exact Next Authorized Action

1. Create a fresh worktree/branch off `origin/main`; verify this packet is on main; run the overlay start preflight.
2. Read the derived-layout + index-rebuild contract and write-boundary enforcement contract in full; reread the storage-contract sections cited above.
3. Ask the owner (or read a newer instruction) for the first metric families/consumers; else parameterize.
4. Run `workflow-implementation-scoping` (read-only) to produce the seam route with ordered STEP-* entries, touch points, validation, stop conditions, and the explicit implementation-authorization boundary.
5. Stop condition: any step that would edit lake-core primitives, add queue-as-truth semantics, or select a backend is a blocker, not a design choice.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`; overlay: `.agents/workflow-overlay/README.md` — Load-bearing: yes; reread-required.
- User constraints: owner wants derived lanes to "pick up work seamlessly" and "precompute / on-demand metrics we require" (user-stated, 2026-07-02); scoping may proceed concurrently with Gate ratification; implementation needs a separate owner go.
- Source-read ledger: the six pointer entries in Inherited Context above (all Load-bearing: yes, compare target reread-required, last checked 2026-07-02).
- Code surfaces the route will name but the sender did not read this session (reread-required before citing behavior): `orca-harness/data_lake/root.py`, `orca-harness/data_lake/lane_registry.py`, `orca-harness/data_lake/catalog.py`, `orca-harness/data_lake/silver_record.py`.
- Source gaps: derived-layout + write-boundary contracts unread by sender; metric families unnamed.
- Strict-only blockers: no implementation, validation, readiness, backend, or full-GT claim may be made from this packet.

## Current Task State

- Completed (sender side): seam concept mapped onto contract-sanctioned pieces; owner confirmed direction and concurrency; this packet.
- Not started: everything in the receiving lane — the scoping route itself.

## Workspace State

- Authored on branch `claude/gate-adr-b5-adjudication` (Gate lane landing branch, pre-PR); this handoff file is untracked at authoring and lands via that lane's PR.
- Receiver state: fresh worktree off `origin/main`, clean.

## Frozen Decisions

- The seam is lane-side infrastructure consuming public Bronze surfaces; the lake stays dumb. Evidence: storage contract no-smart-lake rules. Consequence: any design putting pickup/notify/retry inside the lake is rejected at review.
- On-demand-first for metrics; precompute only as rebuildable manifest-backed caches. Evidence: medallion posture + Silver Vault read-model rules. Consequence: no view may become load-bearing.

## Mutable Questions

- Which metric families first (owner input).
- Whether the derived-layout contract's rebuild trigger has formally fired (receiver confirms against its text).
- Whether the pickup helper is one shared library surface or a per-lane convention with a shared test contract (scoping decides).

## Superseded / Dangerous-To-Reuse Context

- The sender's chat-level seam explanation (arrivals board / done-list metaphor) is orientation only; the contracts govern. Replacement: the ledger sources above.

## Commands And Verification Evidence

- Verify packet on main: `git ls-tree origin/main -- docs/hygiene/data_lake_consumption_seam_scoping_handoff_v0.md` (expect one blob row).
- Start preflight: `git status --short --branch`; `git rev-parse HEAD`.

## Blockers And Risks

- Metric families unnamed: route may need an `operator_to_fill` placeholder. Next action: ask owner once, then parameterize.
- Derived-layout contract governance unknown to sender: could reshape piece 2. Next action: read it first (Exact Next Authorized Action step 2).

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: packet reachable on main; the six ledger pointers still say what the gists claim (reread); Gate 1 ADR output 4 still pins the public surfaces; derived-layout trigger wording.
- Load outcomes: REUSE (all verified) -> continue at Exact Next Authorized Action step 3; STALE_REREAD_REQUIRED (contracts moved) -> reread then continue; BLOCKED_UNVERIFIABLE (a gist cannot be re-derived) -> stop, report.

## Do Not Forget

The seam's entire safety story is that it touches Bronze only through the public surfaces. If any design step needs a private path, layout fact, or lake-core change, that is the signal the design is wrong — stop and re-read the drift guard.
