# Aphrodite × Silver Integration — Direction Handoff (v0)

```yaml
retrieval_header_version: 1
artifact_role: Lane handoff prompt (docs/prompts/handoffs/; owner-steered direction packet layering on the unit (b) census packet)
scope: >
  Records the owner's 2026-07-04 hyperfocus steer — integrate the Aphrodite
  (Creator Signal carveout) lanes with the silver read layer — and converts it
  into the executable first move: run silver/vault unit (b) (the read-only
  silver census gating read) WITH an added Aphrodite panel-consumption column,
  and carry the owner-endorsed candidate that an Aphrodite panel reader
  becomes the unit (c) selection-design probe. Layers on the unit (b) packet;
  duplicates none of it.
use_when:
  - Launching the Aphrodite × silver integration direction in a fresh lane (this packet + the unit (b) packet together).
  - Checking what the owner steered on 2026-07-04 about Aphrodite/silver sequencing and what stays gated.
stale_if:
  - The unit (b) ledger (with the Aphrodite column) has been delivered and owner-steered.
  - The owner re-steers the Aphrodite/silver sequencing or the unit (c) probe choice.
authority_boundary: retrieval_only
```

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (unit (b) packet + ratification record + Aphrodite charter/
    depth handoff + silver parent handoff; all compare targets resolve on origin/main)
  edit_permission: docs-write (this handoff artifact only)
  target_scope: docs/prompts/handoffs/aphrodite_silver_integration_direction_handoff_v0.md
  dirty_state_checked: yes (authored on claude/aphrodite-silver-direction off origin/main @ 14e604fd)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound by the artifact-folders overlay file and the in-repo handoff pattern.
```

## Load Contract

- packet_version: v0
- mode: max (thin by design — the base contract lives in the unit (b) packet; this packet carries only the direction delta)
- created_at: 2026-07-04
- created_by_lane: bronze census closure lane (provenance only, not authority)
- workspace: the receiving lane's own fresh checkout/worktree off `origin/main`
- handoff_path: docs/prompts/handoffs/aphrodite_silver_integration_direction_handoff_v0.md
- expected_branch: read-only census work from `origin/main`; durable deliverables on a fresh docs branch
- expected_head: `origin/main` at or after this packet's merge — run `git fetch origin` FIRST (three receiving lanes have now failed on stale local refs; the census record, ratification record, and this packet all landed on 2026-07-04)
- expected_dirty_state_including_handoff_file: clean tree; this packet is committed, not dirty
- load_rule: confirm-don't-trust — re-verify every load-bearing fact against its compare target before acting

## Owner steer (2026-07-04, recorded)

The owner directed: "let's hyperfocus on Aphrodite lanes for silver runners'
integration", accepting the sequencing assessment that integration CODE is
premature until the silver selection rule exists, and that the fastest honest
path is census-first. Concretely steered:

1. **Unit (b) runs now, with an Aphrodite column** (the redirect below).
2. **Candidate, not decided:** an Aphrodite panel reader may become the
   unit (c) selection-design probe (instead of, or before, the default
   `instagram_metric_seed` candidate) — a new reader can be BORN on the
   selection rule instead of migrated to it. The choice stays with the owner
   at unit (c), with the ledger in hand.
3. **Unchanged gates:** the Aphrodite depth-layer build authorization remains
   OPEN (its packet is a planning artifact, not a build grant); no silver
   integration code, no selection design, no schema tokens in this unit.

## The redirect (execute unit (b) with this delta)

Execute `docs/prompts/handoffs/data_lake_silver_census_gating_read_handoff_v0.md`
under its own load contract and drift guard — its ratification gate resolves
against `docs/decisions/silver_vault_goal_frame_ratification_v0.md` (same
2026-07-04 landing) — with ONE addition to the ledger deliverable:

**Aphrodite panel-consumption column.** For each silver writer/reader row,
record which of the five Vetting Sprint evidence panels — fit, ad-reception,
purchase-intent, brand-adjacency, momentum (charter §4) — would plausibly
consume that lane's records, or `none`. Momentum deserves particular care:
it is the time-layer's first product and reads the creator-profile silver
metric lanes. Where a panel's needs are NOT met by any existing silver lane,
record the gap as a `missing-silver-lane` row (that is build-ledger input,
not a build authorization).

The column is classification from the charter's panel definitions plus the
code — it needs no Aphrodite build, no capture, and no live-lake access
beyond what the base unit already scopes.

## Open Decision / Fork (carried to unit (c), not decided here)

- decision: which reader probes the unit (c) selection design —
  `instagram_metric_seed` (the F-IGRC-001 motivated default) vs a new
  Aphrodite panel reader (born on the rule; owner-endorsed candidate) vs
  both in sequence.
  - owner of the call: owner, at unit (c), with the ledger delivered.
  - already constrained: unit (c) remains a high-lock-in owner-steered fork;
    nothing in this packet pre-decides the selection mechanism.

## Drift Guard (delta over the unit (b) packet's own guard)

- No Aphrodite build work of any kind: the depth-layer hard gate (explicit
  owner build authorization) is OPEN; the rehearsal research (PR #665) and
  sub-ontology handoff are context, not authorization.
- The Aphrodite column is CLASSIFICATION only — recording a `missing-silver-lane`
  gap authorizes nothing.
- Everything in the unit (b) packet's drift guard applies unchanged.
- The Capture ↔ Creator Signal ownership boundary (spine promotion binding)
  is untouched by this direction: silver lanes stay capture/computation-side;
  Aphrodite owns display/claim rules only.

## Inherited Context (does NOT flow to a new lane)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
  (read `AGENTS.md` + overlay README first, always).
- **Base contract**: `docs/prompts/handoffs/data_lake_silver_census_gating_read_handoff_v0.md`
  (on `origin/main`; its gate-resolution amendment lands with THIS packet's
  PR — if its "RATIFICATION GATE" section still says "do this first /
  PROPOSAL", fetch again; the amended form says "resolved — confirm, don't
  re-ask"). Load-bearing: yes; reread-required.
- **Ratification record**: `docs/decisions/silver_vault_goal_frame_ratification_v0.md`
  (same PR). Load-bearing: yes; reread-required.
- **Aphrodite charter**: `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md`
  — §3 (two-layer moat), §4 (the five panels — the column's definition
  source), §6 (stratified capture policy). Load-bearing: yes (for the
  column); reread-required. NOTE: the charter and depth handoff may cite
  `orca/product/...` paths — resolve under `forseti/product/...` (PR #666
  rename).
- **Depth-layer build handoff**: `docs/prompts/handoffs/aphrodite_depth_layer_build_handoff_v1.md`
  (supersedes the v0 packet, which landed via PR #661) — historical context
  for what Aphrodite was built to consume. The v1 packet's `stale_if` fired
  when the rehearsal completed, so its former OPEN gates do not bind current
  work. Load-bearing: yes (historical build context); reread-required.
- **Silver parent handoff**: `docs/prompts/handoffs/data_lake_silver_vault_lane_handoff_prompt_v0.md`
  (on `origin/main` via PR #662) — unit queue (b)/(c)/(d) definitions.
  Load-bearing: yes; reread-required.
- Additional substrate (orientation; verify before citing): the
  single-creator depth rehearsal research landed via PR #665
  (jeremyfragrance); a fragrance sub-ontology build handoff exists at
  `docs/prompts/handoffs/aphrodite_fragrance_subontology_build_handoff_v0.md`;
  bronze is closed by executable claim
  (`docs/decisions/bronze_consumer_census_closure_record_v0.md`, "Closure
  observed" section).

## Active Objective

Deliver the unit (b) build-vs-classify ledger WITH the Aphrodite
panel-consumption column, so the owner can steer unit (c) — including the
probe-reader choice — with both the silver evidence and the Aphrodite demand
side on one page.

## Exact Next Authorized Action

1. `git fetch origin`; read `AGENTS.md` + overlay README; state isolation.
2. Open the unit (b) packet; run its load checklist (its gate resolves
   against the ratification record).
3. Execute unit (b) per its own contract, building the Aphrodite column
   alongside (charter §4 as the panel-definition source).
4. Deliver the ledger (chat-first; durable copy per overlay if asked) with
   per-row build-vs-classify recommendations, the Aphrodite column, and any
   `missing-silver-lane` gap rows. STOP — unit (c) and any Aphrodite build
   remain owner-gated.

## Superseded / Dangerous-To-Reuse Context

- Any statement that the silver goal frame is "a proposal pending
  ratification" — superseded by the ratification record (2026-07-04).
- Any `orca/product/...` path — resolve under `forseti/product/...`.
- The unit (b) packet's original expected-head note referencing unmerged
  PRs #662/#679 — all merged as of this packet.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: the ratification record resolves; the unit (b)
  packet's gate section reads "resolved — confirm, don't re-ask"; the
  charter's §4 panel list; the depth handoff's gate table (build
  authorization still OPEN unless the owner has since granted it).
- Load outcomes: `REUSE` after those verify; a missing ratification record or
  old gate text → `STALE_REREAD_REQUIRED` (fetch current main); anything
  requiring Aphrodite build work → stop, owner-gated.

## Do Not Forget

The point of census-first: a new Aphrodite reader born on the selection rule
never joins the F-IGRC-001 class; one built before the rule does. Deliver
evidence, stop, let the owner pick the probe.
