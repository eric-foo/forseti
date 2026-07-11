# Handoff Packet — Cross-Family Memory + Cost Model Design (Research Engine)

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet (cold cross-lane design commission; not implementation authorization)
scope: >
  Durable cold-reader handoff commissioning the design of the research engine's
  cross-family compounding-memory + cost-instrumentation state model (strategy
  weaknesses W4/W5). Consolidates the sender's SCI + MGT reasoning; instructs
  the receiver to DEEP-THINK ALTERNATIVE STATE MODELS FIRST (owner direction)
  before weighing the sender's candidate. Design-only; authorizes no build.
use_when:
  - Starting the cross-family memory/cost state-model design lane cold.
  - Checking what is frozen vs open before proposing a state model.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_research_engine_god_tier_target_v0.md
  - docs/research/forseti_research_engine_god_tier_strategy_v0.md
  - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
  - docs/decisions/forseti_venue_registry_rejection_decision_v0.md
stale_if:
  - The receiver's design record is owner-adjudicated (this packet is then history).
  - The god-tier target or ECR-onwards deferral is superseded.
```

Prompt preflight (inline core): output mode = durable handoff artifact (this
file); template kind = handoff packet (workflow-handoff), couriered separately;
receiver edit permission = docs-write ONLY (one new design record; no code-root,
overlay, or doctrine edits); reviews = findings-first if the receiver routes its
design for review; no runtime-model routing is implied by any wording here;
doctrine change = none made by this packet (the receiver's design record, if
adopted, carries its own direction-change propagation receipt at adoption);
destinations = this packet at
`docs/prompts/handoffs/research_engine_cross_family_memory_cost_model_design_handoff_v0.md`,
receiver output suggested at
`docs/research/forseti_research_engine_cross_family_memory_cost_model_design_v0.md`
(receiver confirms placement per `.agents/workflow-overlay/artifact-folders.md`).

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-10
- created_by_lane: `claude/research-engine-strategy-3a7619` (research-engine strategy lane; provenance only, not authority)
- workspace: the Forseti repository (receiver: fresh lane/worktree off `main` after PR #837 merges; the packet travels in that PR)
- handoff_path: `docs/prompts/handoffs/research_engine_cross_family_memory_cost_model_design_handoff_v0.md`
- expected_branch: sender lane `claude/research-engine-strategy-3a7619`; receiver works off current `main`
- expected_head: sender head at packet write `bdbe5e6e` (receiver: any `main` containing PR #837)
- expected_dirty_state_including_handoff_file: sender tree clean except this packet (untracked at write, committed in the same turn); receiver expects a clean tree
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: the research-engine god-tier target — any commissioned
  decision question turns into fresh, provenance-hashed, multi-venue-family,
  ECR-handoff-ready evidence with coverage that compounds run over run and cost
  that measures itself (`docs/decisions/forseti_research_engine_god_tier_target_v0.md`, owner-set 2026-07-10).
- anchor_goal: design ONE cross-family state model that gives the engine
  compounding memory (W4) and cost instrumentation (W5) across ALL source
  families (IG, TikTok, YouTube, Reddit, fragrance-native DBs, retail/PDP,
  vendor pricing, SERP, Quora) plus Scanning venue-memory and CSB row status —
  not a CSB/scan-only improvement.
- success_signal: a deep-think design record that (1) generates and compares at
  least two genuinely alternative state models BEFORE weighing the sender's
  candidate, (2) recommends one with named MGT accepted residuals, (3) is
  owner-adjudicable as-is, and (4) implements nothing.

## Open Decision / Fork

- decision: which cross-family state model the research engine adopts for
  compounding memory + cost instrumentation.
  - owner instruction (2026-07-10, verbatim intent): consolidate the sender's
    MGT/SCI reasoning, hand off, and "ask them to deep think and suggest
    alternative states first. it will be a cross family model."
  - options (receiver: generate your own alternatives FIRST; the list below is
    orientation, not a menu to pick from):
    - A — sender's prior candidate ("P0 carries the seeds"): capture-owned
      route-state ledger (one YAML, controlled enum per family × venue × mode,
      dated evidence pointers) + CSB board lineage (prompt amendment) + a
      `run_cost:` row convention in scan artifacts and capture receipts.
      Weakness the owner flagged: shaped around CSB/scanning; family coverage
      bolted on rather than native.
    - B — unified cross-family entity-state model: one shared state vocabulary
      over (family × entity × access-mode × capability), with typed
      family-local extensions; single SSOT or per-family files sharing the enum.
    - C — event-log model: append-only capture/scan observation events; states
      DERIVED at read time, never stored (mirrors the repo's existing
      re-derive-never-migrate doctrine in ECR/packet schema-evolution).
    - D — registry-extension model: extend the two existing memory prototypes
      (creator registry pattern; capture recon index) family-by-family with a
      shared maturity enum — no new artifact kind at all.
  - already constrained / off the table (see Drift Guard for cites): a
    scanning-authority venue atlas; standing crawlers/schedulers/dashboards;
    anything that moves route-binding ownership out of Capture; implementation
    in this lane.
  - trade-offs (sender's read, to be re-derived): A is cheapest but
    CSB/scan-centric; B is the most coherent cross-family shape but risks
    schema lock-in (the exact failure MGT guards against); C best matches
    existing derivation doctrine and is most audit-friendly, but read-time
    derivation needs a small deriver (code) eventually; D is lowest-novelty and
    reuses proven patterns but may fragment the vocabulary per family.
  - owner of the call: the owner, via adjudication of the receiver's design record.
  - recommendation: none binding. The sender's candidate A is explicitly a
    hypothesis; the owner has directed alternatives-first deep thinking.

## Drift Guard

- Deep-think FIRST, design-only. The deliverable is a design record with
  alternatives compared; no code, no checker edits, no ledger files, no prompt
  amendments, no doctrine edits. Violating this converts an owner design fork
  into unauthorized build.
- Cross-family is the bar. A model that only serves CSB/scanning repeats the
  exact miss the owner corrected; every capture source family must be a
  first-class citizen of the state model.
- NOT a venue atlas: `docs/decisions/forseti_venue_registry_rejection_decision_v0.md`
  rejected the maximal standing-registry shape once already. Any proposal that
  recreates a scanning-authority atlas or standing infrastructure whose
  maintenance eats the speed advantage will be rejected on precedent.
- Ownership boundary: Capture owns route binding; Scanning cites route state
  (`forseti/product/spines/scanning/README.md`, Load Order item 5). A state
  model must not move that boundary.
- MGT discipline is mandatory: target ~90-95% of the maximal model's practical
  value; the foregone slice must be NAMED as accepted residuals with upgrade
  triggers (`docs/decisions/forseti_mini_god_tier_doctrine_v0.md`). No
  residual list = not adoptable.
- Scope: research engine only (CSB, Scanning, Capture). ECR-onwards is
  deferred (`docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md`);
  do not design downstream consumption. IG/TikTok durable media preservation
  is an owner-accepted residual (2026-07-10, in-thread) — do not reopen it.
- P0 is independent: the P0 golden thread
  (`docs/research/forseti_research_engine_p0_golden_thread_commission_v0.md`)
  proceeds with its own minimal per-commission capture_request lifecycle
  ledger and STEP-5 instrumentation. The cross-family model must COMPOSE with
  P0's outputs, not block or re-scope P0.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
  (enter via `.agents/workflow-overlay/README.md` per `AGENTS.md`)
- targets to enter the ladder: the four `open_next` files above, plus
  `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`,
  `forseti/product/spines/capture/core/source_families/README.md`,
  `forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md`,
  `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md`,
  `docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`
- already loaded (weak orientation, sender-read 2026-07-10; not authority): all
  of the above, summarized in the ledger below
- must load first (before any strict or actionable step): the strategy record's
  W4/W5 sections + fork list, the MGT doctrine, the venue-registry rejection
- load rule: receiver re-runs progressive source loading per overlay; this
  packet's loaded-set only seeds the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Research-engine-only scope; ECR-onwards deferred (kept, not retired) —
  decided in `docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md`;
  compare target: its Status line `OWNER_SEQUENCING_DECISION_V0 — owner-directed 2026-07-10`;
  verify before scoping the model.
- Capture v0 is commissioned-capture-only; standing collection is a separate
  proposal-only Corpus Intake lane — decided in the capture obligation contract
  and `forseti/product/spines/capture/README.md` ("Capture v0 is
  commissioned-capture-only"); verify before proposing any standing cadence.
- Fork 4 (legacy scan closeout enum) already resolved = version-scoped
  grandfather; forks 1 (narrow standing cadence) and 5/6 remain open elsewhere —
  recorded in `docs/research/forseti_research_engine_god_tier_strategy_v0.md`
  ("Owner Forks" section); verify before restating forks.
- "Blocked is a hypothesis, not a verdict" is the corpus's dominant
  false-diagnosis lesson, currently prose-only — recorded in
  `capture_recon_index_v0.md` (cross-cutting patterns, ~lines 41-49); the state
  model should make this class of error structurally harder; verify the exact
  wording before citing.

## Active Objective

Produce one owner-adjudicable design record for the research engine's
cross-family compounding-memory + cost-instrumentation state model,
alternatives-first, MGT-calibrated, implementing nothing.

## Exact Next Authorized Action

1. Run the confirm-don't-trust load protocol below; re-verify the load-bearing
   ledger entries against their compare targets on current `main`.
2. Invoke `workflow-deep-thinking`. Generate alternative cross-family state
   models FIRST (at least two beyond the sender's candidate A), naming for each:
   state vocabulary, granularity (family/entity/mode/capability), storage shape,
   update discipline (who writes, when), cost-row integration, and how it makes
   the "blocked is a hypothesis" failure class structurally harder.
3. Compare against decision-relevant criteria (compounding value captured,
   lock-in/maintenance burden, cross-family nativeness, composition with P0,
   enforcement-placement fit) and recommend one, with MGT accepted residuals
   named per residual (what is foregone, why acceptable, risk, upgrade trigger).
4. Write the design record (suggested:
   `docs/research/forseti_research_engine_cross_family_memory_cost_model_design_v0.md`;
   confirm placement per `.agents/workflow-overlay/artifact-folders.md`), land
   it via the per-lane PR flow, and stop for owner adjudication. Stop condition:
   no implementation, no doctrine edits, no checker changes.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (+ `.agents/workflow-overlay/README.md` before project work)
- Overlay authority: `.agents/workflow-overlay/` (source-of-truth, source-loading, artifact-folders, prompt-orchestration)
- User constraints (owner, 2026-07-10, this thread): cross-family model;
  alternatives-first deep think; consolidate SCI/MGT reasoning; design via handoff.
- Source-read ledger (all sender-read 2026-07-10 at lane head `bdbe5e6e`):
  - `docs/research/forseti_research_engine_god_tier_strategy_v0.md`
    - Role: weakness evidence (W4/W5), fork list, owner-decisions section
    - Load-bearing: yes
    - Compare target: section headings "Weakness Map (ranked)" W4/W5 and "Owner Decisions Applied (2026-07-10)"; reread-required on current main
    - Reuse rule: evidence base for the design; the P3 sketch inside it is a superseded candidate (see below)
  - `docs/decisions/forseti_research_engine_god_tier_target_v0.md`
    - Role: the owner-set bar the model serves (done-conditions 1, 4, 5, 6 are the memory/cost gates)
    - Load-bearing: yes
    - Compare target: "Measurable Done-Conditions" items 1/4/5/6; reread-required
    - Reuse rule: target calibration only; not readiness
  - `docs/decisions/forseti_mini_god_tier_doctrine_v0.md`
    - Role: MGT lens (90-95%, mandatory accepted residuals)
    - Load-bearing: yes
    - Compare target: quoted phrase "roughly 90-95% of the practical capability value"; reread-required
    - Reuse rule: binds the design's calibration section
  - `docs/decisions/forseti_venue_registry_rejection_decision_v0.md`
    - Role: rejected maximal-shape precedent
    - Load-bearing: yes
    - Compare target: reread-required (sender read it only via the MGT doctrine's citation — receiver MUST open the primary)
    - Reuse rule: drift-guard precedent; any registry-like proposal must distinguish itself from what this rejected
  - `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
    - Role: existing capture memory prototype + "blocked" false-diagnosis evidence
    - Load-bearing: yes
    - Compare target: cross-cutting pattern text near lines 41-49 ("blocked" dominant false diagnosis); reread-required
    - Reuse rule: candidate substrate for option D
  - `forseti/product/spines/capture/core/source_families/README.md` + `.../creator_registry/README.md`
    - Role: family lane catalog; creator registry ("not a live capture runner" static ledger) — the other memory prototype
    - Load-bearing: yes
    - Compare target: reread-required
    - Reuse rule: the model must be native to every family listed there
  - `.../obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
    - Role: open recapture/freshness design knob the model may (or may not) absorb
    - Load-bearing: yes
    - Compare target: open question "what recapture threshold is high enough to avoid churn..." (~lines 735-736); reread-required
    - Reuse rule: name explicitly whether the model answers or defers this knob
  - `docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md`
    - Role: product floor (>=2 independent venue families, 30-90d window) the memory model must serve
    - Load-bearing: yes
    - Compare target: reread-required
    - Reuse rule: demand-side anchor, not a capture rule
  - Cost-evidence negative (sender-observed): no scan or capture run records
    tokens/wall-clock/cost anywhere; only per-query timestamps in two SERP batch
    receipts (`docs/research/search_surface_mgt_pilot_p0_receipts_v0/`)
    - Load-bearing: yes
    - Compare target: reread-required (spot-check 2-3 scan artifacts + capture receipts for absence of cost fields)
    - Reuse rule: the W5 baseline claim; re-verify, do not trust
- Source gaps: the sender never opened the venue-registry rejection primary; no
  cross-family cost data exists anywhere to calibrate the cost-row fields.
- Strict-only blockers: none for design work; implementation is out of scope.
- Not-proven boundaries: nothing in this packet asserts validation, readiness, or adoption.

## Current Task State

- Completed (sender lane): weakness map + god-tier target + ECR-onwards
  deferral + P0 commission + hygiene-rider fixes + adjudicated review patch,
  all on PR #837.
- Partially completed: the memory/cost DESIGN — sender produced candidate A in
  chat; owner redirected to cross-family, alternatives-first (this handoff).
- Broken or uncertain: none for this design lane.

## Workspace State

- Branch: `claude/research-engine-strategy-3a7619` (sender); receiver: fresh lane off `main`
- Head: `bdbe5e6e` at packet write
- Dirty/untracked before handoff: clean
- After writing the handoff file: this packet untracked, then committed on the sender lane in the same turn
- Target files or artifacts: receiver CREATES one design record; edits nothing else
- Related worktrees or branches: PR #837 carries this packet to `main`

## Changed / Inspected / Tested Files

- None to change. Receiver's only write is the new design record.

## Frozen Decisions

- Research-engine-only scope; ECR-onwards deferred — evidence:
  `docs/decisions/forseti_research_engine_ecr_onwards_deferral_v0.md`;
  consequence: the state model covers CSB/Scanning/Capture and stops at the
  Capture→ECR handoff obligation.
- Owner direction (2026-07-10, in-thread): cross-family model; deep-think
  alternatives first — consequence: candidate A may not be adopted by default.
- Capture owns route binding; Scanning cites — evidence: scanning README front
  door; consequence: state-model write authority sits capture-side.
- MGT accepted-residuals requirement — evidence: MGT doctrine; consequence: a
  design without a residual list is incomplete.
- IG/TikTok durable media preservation stays an accepted residual (owner,
  2026-07-10, in-thread: cost too high, demand pull minimal) — consequence: the
  state model does not track media-preservation state beyond what packets
  already record.

## Mutable Questions

- Granularity: family × venue? × entity? × access-mode? × capability? What
  compounds fastest without churn?
- Storage: one SSOT file vs per-family files sharing one enum vs event log?
- Update discipline: per-run closeout step (manual, staleness risk) vs
  checker-nudged vs derived-from-receipts?
- Cost rows: which fields are real at capture time (tokens are agent estimates,
  not metered) — what is honest to record?
- Does CSB board lineage live inside this model or as a separate CSB prompt
  amendment?
- How does the model bind the "blocked is a hypothesis" mode-ladder receipt —
  as a state-transition precondition, or a separate gate?
- Relation to open fork 1 (narrow standing cadence): does the model need
  cadence fields now, or additive later?

## Superseded / Dangerous-To-Reuse Context

- The sender's chat proposal "P0 carries the seeds" (route-state ledger + board
  lineage + cost-row, presented 2026-07-10) — why dangerous: it reads like an
  adopted plan but the owner explicitly redirected to a cross-family,
  alternatives-first design; current replacement: this handoff's open decision.
- Strategy-doc forks 2 and 3 ("Route-State Ledger", "CSB board lineage") — why
  stale: subsumed by this design commission; current replacement: the
  receiver's design record.

## Commands And Verification Evidence

- None load-bearing. This is a design lane; no commands were run whose output
  the receiver must trust. Verification for the receiver = the source ledger's
  compare targets.

## Blockers And Risks

- Risk: anchoring on candidate A (it is the most fleshed-out option in the
  packet) — mitigation: the owner instruction and step 2 order alternatives
  first; the deep-think verification pass should explicitly check for this
  anchor.
- Risk: designing a maximal registry that repeats the venue-registry rejection —
  mitigation: read the rejection primary before drafting.
- Risk: schema lock-in via premature enum hardening — mitigation: SCI lock-in
  tiebreaker; prefer shapes that stay deletable until P0/P4 volume proves them.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: the W4/W5 evidence claims (strategy record), the
  MGT 90-95% phrasing, the venue-registry rejection's actual scope (primary
  read), the recon-index "blocked" pattern text, the cost-evidence negative.
- Compare targets: as per ledger above (quoted excerpts + reread-required).
- Load outcomes: `REUSE` only after ledger verification; `STALE_REREAD_REQUIRED`
  if the strategy/target docs changed on main; `BLOCKED_UNVERIFIABLE` if the
  venue-registry rejection record cannot be located (do not proceed on the
  sender's characterization of it).
- Reread on drift: strategy record, GT target, MGT doctrine.

## Do Not Forget

- The owner's sequencing sentence is the contract: "ask them to deep think and
  suggest alternative states first. it will be a cross family model."
  Alternatives come BEFORE evaluation of the sender's candidate — in that order.

## Non-Claims

This packet is a continuation artifact: not validation, readiness, approval,
adoption of any state model, capture/source-access authorization, or
implementation authorization. The receiver's design record binds nothing until
owner adjudication.
