# Consumer-Demand Durability Probe — Stage-1 Feasibility Commission Prompt v0

> **CONSUMED (2026-06-12)**
> Executed same day on `consumer-demand-probe`. Intake found the lane already
> past this commission's premises: a committed v0 report records spec-v2
> Stage 1 as `STAGE1_COMPLETE — CONDITIONAL PASS` (2026-06-10; non-blind,
> product_learning) and a Stage-2 pair already selected and SEALED from the
> lane's own ledger (not the 2026-06-12 candidate pool). Per owner
> disposition the commission resolved as a thin read-only reconciliation +
> posture note (`consumer-demand-probe` @ `0a7af17`, local-only commit, not
> pushed). stale_if #2 fired — this prompt is consumed and retained as
> history. The open owner decisions it surfaced are recorded in
> `docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md`
> (second addendum).

```yaml
retrieval_header_version: 1
artifact_role: Product-planning lane prompt (probe-lane Stage-1 commission)
scope: >
  Commissions the consumer-demand durability probe lane to run STAGE 1 ONLY —
  feasibility of the spec-v2 blind test (candidate-pair census, archive/cutoff
  coverage, baselines, zero-spoiler buildability, posture recheck) — under the
  owner's ask-3 authorization of 2026-06-12. Stage 2 (blind momentum-matched
  pair execution) stays HELD until the owner reads the Stage-1 report and
  says go.
use_when:
  - Spinning up the probe lane's Stage-1 feasibility session on the consumer-demand-probe branch.
  - Checking what Stage 1 may and may not do before the owner's Stage-2 word.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md   # the authorization (Owner Decision Record, ask 3 + addendum)
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md               # OWNER_LOCKED; central read + falsifiers the probe tests
  - orca/product/case_families/product_learning/fragrance/consumer_demand_candidate_pool_handoff_v0.md   # candidate input (facilitator-side; outcome-bearing)
input_hashes:
  docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md: 7911CC00BDD486DC9661632B6A9C28D097A492A176646EF4B081899F2EC13195
  docs/decisions/orca_product_thesis_consumer_demand_v0.md: B119E24691066E4772E0CFD4051C3C9C8214ED3A91F8775658E45B77DB0723F1
  docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md: 19009D43A7C29858A719212C5F6E2E1DECD2E63C7B263A074D4EAC5E3F9645B9
branch_or_commit: >
  Inputs pinned on ecr-sp3-timing-deriver-slice1 @ 641a2a6 (memo + thesis
  committed; the candidate-pool handoff is UNTRACKED there — another lane's
  one-shot cut, "commit on owner word"; verify its hash and treat content as
  read, acceptance status as stated). The WORK runs on the
  consumer-demand-probe branch, which owns probe spec v2.
stale_if:
  - The owner amends ask 3's scope or says the Stage-2 word (the recorded outcome governs).
  - The Stage-1 feasibility report lands (this commission is consumed).
  - The candidate pool is superseded by a v1 cut or consumed by a batch ledger.
```

## Thread Operating Target

`Produce the Stage-1 feasibility report for the consumer-demand durability
probe: can spec v2's blind momentum-matched-pair test actually be built —
pairs, coverage, baselines, zero-spoiler packets — and what is the
go/no-go recommendation for Stage 2?`

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target   # new lane; commissioned by the ICP/product-direction lane post-ratification
  changed_from_input: no
  lifecycle_status: active_from_this_commission
```

Fitness reference: **goal** = a Stage-1 feasibility report the owner can read
in one sitting; **observable success signal** = the owner can say go/no-go on
Stage 2 because every spec prerequisite is checked with evidence, every
blocker is named, and no feasibility claim leaks into a probe-result claim.

## Cynefin Routing

Per `.agents/workflow-overlay/decision-routing.md` (run at commissioning,
2026-06-12): regime **Complicated**; layer-based decomposition (authorization
→ spec prerequisites → candidate census → coverage/baselines → report);
bottleneck = momentum-matched pair availability under the US-default
direction plus archive coverage at the needed windows; stop/pivot = a spec
prerequisite is unmeetable or the spec conflicts with the new capture
posture — report the blocker, do not improvise around the spec. Disallowed:
Stage-2 execution, blind runs, scoring, candidate admission, capture builds.
Re-run the router on intake if trigger conditions changed.

## Preflight

```text
orca_start_preflight:
  agents_read: required on intake (read fresh)
  overlay_read: required on intake (.agents/workflow-overlay/README.md)
  source_pack: custom (Source Pack below)
  edit_permission: docs-write on the consumer-demand-probe branch only (the Stage-1 report + dated lane notes; no main-working-branch edits)
  target_scope: Stage-1 feasibility report (deliverables 1-6 below)
  dirty_state_checked: required on intake (verify the three input_hashes above; on mismatch reread before relying; classify the pool handoff as untracked)
  blocked_if_missing: probe spec v2 unreadable on the probe branch, or the ask-3 authorization record unreadable
repo_map_decision: loaded (thesis row now routes to the ratified record)
doctrine_change: none (Stage 1 is feasibility evidence; if a spec amendment proves necessary, NAME it for the spec's own lane — do not apply it)
external_source_boundary: external workflow source is read-only; jb is not Orca authority.
```

## Authorization And Posture (verified state, 2026-06-12)

- **Ask 3 (owner, 2026-06-12): "yes thats okay"** to the recommendation as
  framed — Stage-1 feasibility authorized NOW; Stage 2 HELD until the owner
  reads the Stage-1 report. Full verbatim record:
  `docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md`
  (Owner Decision Record + Addendum). Keep-cleared review state is not
  execution authority; this record plus the spec's own gates are.
- Thesis is `OWNER_LOCKED` (2026-06-12, ask-1 amendment folded): the probe
  tests its central read (durable-vs-hollow persistence discrimination
  against momentum and category-prior baselines); a Stage-2 decide-grade
  fail is a named thesis falsifier.
- Capture posture (ask-1 amendment): measured ToS risk accepted;
  absurd-level approaches (e.g., Bright-Data-style industrial scraping)
  rejected; per-venue route bindings stay capture-lane-owned. **TikTok live
  = GO by owner word 2026-06-12** (re-confirmed after a verification flag;
  the owning capture-lane records still carry the pre-ratification NO-GO and
  owe their own dated alignment — treat the owner word as current).
- Geography: US-market first proof (thesis geography doctrine, 2026-06-12);
  NON-US candidate rows route to the owner or defer.
- Wedge co-ratified (beauty operator first door); pricing-first superseded
  and NOT a re-entry candidate (owner word 2026-06-12).

## Source Pack (read on intake; targeted, not bulk)

REFERENCE-LOAD any invoked workflow methods first; APPLY only after declaring
`SOURCE_CONTEXT_READY` over this pack
(`.agents/workflow-overlay/prompt-orchestration.md`, Source-Gated Method
Contract).

Full reads (3): the decision memo (authorization); probe spec v2 on the
consumer-demand-probe branch (`consumer_demand_durability_probe_spec_v2.md`,
status at last verification: `PROPOSED_PROBE_SPEC_V2 — KEEP-CLEARED`,
recheck-completed/re-kept — locate it on that branch, record its path + hash
at intake; BLOCKED if unreadable); the candidate-pool handoff (facilitator-
side input; see the contamination boundary below). Targeted reads: thesis
(Central Read, Falsifiers, Proof Doctrine, Vertical And Geography Doctrine
sections); `docs/product/core_spine/orca_memorization_resistant_case_finder_frame_v0.md`
(operative obscurity bar + probe protocol, as the pool's obligations cite
it). Available-not-read by default: batch-1 ledger (machinery exemplar —
open only if the spec requires its mechanics), screen ledgers (per-row
receipts — open only when a specific candidate's receipt is load-bearing for
feasibility).

## Contamination Boundary (read before touching the pool)

The candidate-pool handoff states OUTCOMES for its rows. It is
facilitator-side material under the zero-spoiler rules
(`.agents/workflow-overlay/product-proof.md`): whoever runs this Stage-1
census becomes outcome-exposed for those candidates and cannot later serve
as a blind contestant on them. Do not build, draft, or sketch any
participant-facing packet text in this lane; Stage 1 assesses buildability
only. Record this exposure in the report so the Stage-2 lane assigns clean
contestants.

## Commission (Stage-1 deliverables — feasibility report only)

1. **Spec-prerequisite census.** Enumerate spec v2's Stage-1/feasibility
   prerequisites verbatim and check each against evidence; the spec is the
   controlling document — where this commission and the spec disagree, the
   spec wins and the disagreement is reported.
2. **Candidate-pair feasibility.** From the pool (14 candidates + 2
   completions) and the spec's case requirements: can momentum-matched
   durable-vs-hollow PAIRS be formed? Apply the pool's consuming-batch
   obligations as constraints — US-default (NON-US rows 2, 6, 8, 10, 12
   route to the owner or defer; BORDER rows 5, 13 get an explicit call
   routed to the owner), FAME rows (6, 7) marked recognition-check-required
   per the finder frame (mark required; run probes only if the spec assigns
   them to Stage 1), WEAK row 14 source-depth check, CORR row 10 grade
   noted. Census and pairing-feasibility ONLY — admission, swap placement,
   and dev/holdout split belong to the consuming batch's own ledger, not
   this report.
3. **Archive / cutoff coverage check.** For each feasible pair: do the
   venues and windows the read needs exist at the needed cutoffs (typed
   snapshot times, CDX bounds, venue coverage)? Name gaps per pair.
4. **Baseline availability.** Momentum and category-prior baselines per the
   spec: do the data exist to construct them blind-safely?
5. **Posture recheck.** Re-check the spec's source assumptions against the
   2026-06-12 posture (measured ToS risk; TikTok live GO; US-default
   geography): name what newly unlocks (mainly forward/live legs), what
   stays archive-shaped for backtest legs, and any spec amendment this
   implies — NAMED for the spec's own lane, never applied here.
6. **Go/no-go recommendation for Stage 2** with blockers, the cleanest
   feasible pair set, contamination/exposure record, and what the owner must
   decide (NON-US/BORDER row calls; any spec amendment; Stage-2 word).

## Hard Constraints

- STAGE 1 ONLY: no blind execution, no sealed judgments, no scoring, no
  fixture admission, no reveal/calibration, no batch admission.
- No capture expansion or build; live-source or archive calls only as spec
  v2's feasibility provisions already authorize — where the spec is silent
  on a needed call, stop and route the question to the owner instead of
  improvising under the new posture.
- No outreach (gate closed, owner ask 4); no edits to main-working-branch
  records; no edits to the spec (dated lane notes only); never commit
  another lane's files.
- Claim discipline: everything in the report is `product_learning`-tier
  design/feasibility input; closeout state for any proof-shaped claim is
  `no_durable_evidence`. Feasibility is not a probe result; "buildable" is
  not "validated." Any externally-shaped sentence obeys claim-defense Row 1.

## Output Mode And Contract

`file-write` on the consumer-demand-probe branch: one durable Stage-1
feasibility report placed per that lane's conventions adjacent to spec v2
(proposed default name:
`consumer_demand_durability_probe_stage1_feasibility_report_v0.md`; confirm
against the lane's layout at intake), with a retrieval header per
`.agents/workflow-overlay/retrieval-metadata.md`. Chat closeout: headed human
summary first (go/no-go recommendation, blockers, owner decisions needed),
then path/hash/status receipts. Commit on that branch only per that lane's
conventions and the owner's word.

## Validation Gates

- `orca_start_preflight` recorded on intake; the three input hashes verified
  (drift → reread; silent reliance is a defect); spec path + hash recorded
  at intake.
- Judgment Spine claim-tier gate: classification inline in the report
  (product_learning; `no_durable_evidence` for proof-shaped claims;
  weakest-cleared-gate rule).
- Zero-spoiler gate: no participant-facing material produced; contamination
  exposure recorded.
- Prompt gates per `.agents/workflow-overlay/prompt-orchestration.md`; this
  commission's verdict at authoring: PASS_WITH_WARNINGS (warnings: the spec's
  exact path/hash on the probe branch is not pinnable from the commissioning
  branch — intake must locate, read, and pin it, blocked if missing; the
  candidate pool is untracked on the commissioning branch — hash-pinned
  above, acceptance status as stated in the document).

## Assumptions, Unknowns, Blocked Conditions

- Assumes spec v2 defines (or cleanly implies) a Stage-1/feasibility scope;
  if the spec has no separable feasibility stage, report that as the first
  finding and propose the smallest bounded census that respects the spec —
  do not invent a stage.
- Unknown: whether enough US-default rows survive the pairing constraints to
  form momentum-matched pairs without the NON-US rows; if not, the report
  routes exactly that to the owner (it is an owner call, not a workaround).
- Blocked if: the spec or the ask-3 record is unreadable; hash drift cannot
  be re-verified; or Stage-1 work would require a source call the spec does
  not authorize.

## Non-Claims

Commissions feasibility assessment only. Not probe execution, not Stage-2
authority, not validation, not buyer proof, not judgment-quality evidence,
not candidate admission, not capture authorization beyond the spec's own
provisions; ships no external claim; the verified-state capsule above is
orientation — the lane's own intake reads govern.
