# Judgment Spine Consolidation Map v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (Judgment Spine consolidation map / orientation submap)
scope: Single always-findable entry point that orients a reader across the whole Judgment Spine corpus — which spans docs/research/judgment-spine/ and docs/product/judgment_spine_* — and routes one hop into the owner sources. Map only; not source-of-truth.
use_when:
  - Orienting to the Judgment Spine before ECR, Cleaning, harness, or case work.
  - Finding which owner doc owns a given spine area (thesis, cases, conductor, gates, ladder, reveal, harness).
  - Checking what a run can actually claim today before relying on it.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/README.md
  - docs/research/judgment-spine/manifest_v0.md
stale_if:
  - An owner source renames/retires a spine area or its owning doc moves trees.
  - The evidence ladder changes claim tiers or closeout states.
  - The conductor changes its invariants, the five seams, or the outcome precedence.
  - A contestant-execution runner lands and lifts the by-hand cap (then author v1).
```

> **What this is.** A retrieval map. It tells a cold reader what the Judgment Spine
> areas are, what each can claim today, and which owner doc to open. It is one hop
> in and one hop out. **It is the map, not the territory:** on any conflict with a
> pointed-to source, the source wins and this map is stale for that point. It never
> carries doctrine, gate semantics, claim vocabulary, or case facts — it points to them.
>
> **Do not use** this map as source-of-truth, validation, proof, gate clearance,
> fixture admission, or authority for any claim. Nothing here is proven; **artifact
> volume is not readiness**.

## Fast Route ("I need to…")

| I need to… | Open | Tree |
| --- | --- | --- |
| Know the north-star / what "good judgment" means here | `judgment_spine_thesis_v0.md` | research |
| Find the case inventory + per-case artifact status | `manifest_v0.md` | research |
| Run or plan a case through gates JSG-01→JSG-10 | `docs/product/judgment_quality_promotion_operating_model_v0.md` (conductor) | product |
| Know who owns a gate + its required receipts | `docs/product/judgment_spine_gate_ownership_map_v0.md` | product |
| Know what a run/artifact can **claim** (tiers, closeout states, caps) | `docs/product/judgment_spine_evidence_ladder_architecture_v0.md` | product |
| Apply the JSG-08 reveal/calibration receipt | `docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md` | product |
| Work from the harness spec (schemas, scorer, runner, probe) | `harness/v0_14/index.md` | research |
| Understand no-tools isolation for JSG-04/05/06 | `harness/v0_14/contestant_no_tools_execution_contract_v0.md` | research |
| Know what machinery is built vs a named gap (build-state) | `judgment_spine_machinery_build_state_gap_map_v0.md` | research |
| Read the SP-5 finalization-receipt contract | `sp5_finalization_receipt_spec_v0.md` | research |

## Current Reality Snapshot (as of v0, refreshed 2026-06-09 — verify each against its owner)

- **Conductor exists and is test-worthy, not proven** — it routes/verifies receipts and computes nothing (→ conductor non-claims).
- **By-hand cap is in force:** there is no contestant-execution runner, so JSG-04/05/06 run by-hand and a run **caps at product-learning** (→ conductor, Seam 3).
- **JSG-01 stays FROZEN (`indeterminate_until_authored`)** — for narrower reasons than v0 stated. The ECR SP-1/2/3/6 derivers **are built** (`orca-harness/ecr/deriver.py`: timing / inspectability / identity / source-visibility postures off the `SourceCapturePacket`; they bind no `EvidenceUnit` and make no JSG-01 claim). AR-01 (who finalizes `pre_decision_status`) is **resolved** — distinct cross-family act, operator-for-now (→ `docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md`). What still gates an unfreeze: the **SP-5 finalizer mechanism built** + a **case packet carrying the derived fields** (ECR slice-2). (→ conductor JSG-01 row, **now corrected to match** — derivers built, AR-01 resolved; commit `d2cac45`.)
- **Current cases are pre-cutoff** and cap at qualitative / product-learning; none is a scoreable fixture. Which cases exist → manifest (the inventory owner); what each can claim → evidence ladder. (This map does not list cases — that would inherit the manifest's drift.)
- **Judgment-quality lane — where we are / next** (orientation, refreshed 2026-06-10; verify against the lane records, which own the detail):
  - *Tier:* capped at **product-learning** (by-hand); "almost judgment-quality" is a proximity description, **not** a minted tier → `ideal_judgment_quality_run_and_current_position_v0.md`.
  - *Settled this lane:* AR-01 staffing, option C → `docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md`; ground-truth-before-absence/build-state kernel rule → `docs/decisions/ground_truth_check_before_absence_or_build_state_claims_v0.md`; conductor hardened to Round-18 (F5 fix); gate predicates exercised mechanically checkable → `conductor_per_gate_predicate_exercise_canoo_walmart_v0.md`; the SP-5 A2 finalization-receipt **spec** authored + reviewed (design done; build still gated) → `sp5_finalization_receipt_spec_v0.md`; the review-tier de-correlation doctrine (family=vendor + two-bar) cross-vendor-reviewed + landed (`.agents/workflow-overlay/delegated-review-patch.md` + `review-lanes.md`); the conductor JSG-01 build-state corrected (derivers built, AR-01 resolved) + same-vendor blast-radius checked.
  - *Design tail complete* (SP-5 spec, review-tier doctrine, conductor correction all landed). **Next is owner-owned:** the **invest-vs-bank / authorize-a-real-run** decision (Step 4), informed by the build-state gap map → `judgment_spine_machinery_build_state_gap_map_v0.md`. Gated/deferred (need implementation authorization): the SP-5 finalizer **build**, the JSG-01 `EvidenceUnit` binding (ECR slice-2), the contestant-execution / authorized-live-execution path, and the case-finder.
  - *JQ gap (named build work, not yet authorized):* authorized live blind-judgment execution under isolation + SP-5 finalizer + JSG-01 `EvidenceUnit` binding + case-finder. (Scoring and the memorization-probe runner are **built** — see `judgment_spine_machinery_build_state_gap_map_v0.md`.)

## Areas (each → one owner; summaries are locational, never evaluative)

### Thesis & optimization goal
- summary: The north-star — why the spine exists and what it optimizes.
- status: `WORKING_THESIS_V0` (doc self-declared working).
- pointer: `docs/research/judgment-spine/judgment_spine_thesis_v0.md` (research).

### Case-law loop & inventory
- summary: The operating loop and the current case/artifact inventory + residue. **The manifest owns the inventory; this map does not reproduce it.**
- status: working retrieval index.
- pointer: `docs/research/judgment-spine/manifest_v0.md` (research).

### Conductor — how a case walks the gates
- summary: Sequences JSG-01→JSG-10, checks each gate's receipt, routes between them. Holds routing/lifecycle only.
- status: working operating model; the **path toward** judgment-quality evidence, not proof of it.
- pointer: `docs/product/judgment_quality_promotion_operating_model_v0.md` (product).

### Gate ownership
- summary: Who owns each gate, its required receipts, and gate dependencies.
- status: controlling doctrine.
- pointer: `docs/product/judgment_spine_gate_ownership_map_v0.md` (product).

### Evidence ladder — what a run can claim
- summary: Claim tiers (product_learning / buyer_proof / judgment_quality), closeout states, weakest-cleared-gate + sub-floor caps.
- status: controlling doctrine.
- pointer: `docs/product/judgment_spine_evidence_ladder_architecture_v0.md` (product).

### JSG-08 reveal / calibration owner contract
- summary: The reveal/calibration receipt shape and its satisfaction states the conductor reads at JSG-08.
- status: controlling doctrine.
- pointer: `docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md` (product).

### Harness v0.14 spec (+ no-tools isolation)
- summary: Phase-1 code-readiness spec — schemas, action bands, scorer, runner contracts, probe; the no-tools contract owns JSG-04/05/06 isolation.
- status: Phase-1 spec; does not authorize implementation by itself.
- pointer: `docs/research/judgment-spine/harness/v0_14/index.md` and `.../contestant_no_tools_execution_contract_v0.md` (research).

## Status Vocabularies (owner-defined — this map points, never redefines)

- **Run/case claim tiers, closeout states, and caps** → evidence ladder. Report status as a **cap, not an achievement** (e.g. *capped at* product-learning, not "achieved").
- **JSG-08 satisfaction states** (churn-prone — pointer-only, not listed here) → JSG-08 owner contract.
- **Run lifecycle states** (e.g. `sealed_awaiting_outcome`, `halted_no_completed_closeout`) → conductor, Seam 4.
- **Universal floor:** `not proven`; *artifact volume is not readiness*.

## Frozen Orientation Primitives

Excerpts only, for cold-reader orientation. Each carries its source; **the source wins on any conflict**. No content hashes — the corpus is multi-baseline and dirty, so a hash would imply a clean reference that does not exist; verify against the source path + section.

- **Thesis** — verify against `judgment_spine_thesis_v0.md` ("Thesis" / "Long-Term Optimization Goal"); `WORKING_THESIS_V0`:
  "the durable judgment-improvement layer for turning bounded approved evidence into **right-sized action**." Goal: "**right-sized action under evidence constraints**."
- **Invariant A** — verify against conductor ("No-Authority Invariant"):
  "The conductor, and any LLM acting as conductor, is supporting cast… **It is never the gavel.**" A run that needs the conductor to exercise judgment to clear a gate has not cleared it.
- **Invariant B** — verify against conductor ("Route, Don't Restate"):
  Routing/lifecycle only; every predicate checks an owner-produced field; "**If this conductor and a controlling source disagree, the controlling source wins.**"
- **The five seams** (NAMES only — the contents churn, so pointer-only) — verify against conductor:
  Seam 1 predicate-binding · Seam 2 total fail/blocked transitions · Seam 3 by-hand cap · Seam 4 named run states · Seam 5 closeout self-dependency terminal route.
- **Outcome precedence** (verbatim alphabet; the routing rules over it churn) — verify against conductor ("Transition Function"):
  `[cleared, contaminated_or_blocked, held, not_cleared_or_indeterminate]`

## Reuse Note (local hypothesis — not yet doctrine)

This map's shape — *thin door + one rich `retrieval_only` orientation submap + source owners; per-area {summary, status, one pointer}; single hop in and out; frozen-sliver-with-verify-label; status-by-reading-the-owner* — is a **reusable pattern candidate** for other spines (e.g. Capture). It is **one instance = a hypothesis, not proven doctrine**; do not promote it to a shared template until a second spine needs it. Precedent: the evidence ladder's Core/Satellite Boundary and the conductor's Scaling Rule.

## One-Way Authority & Deferred Items

- **One-way:** authority flows map → source only. The breach signal is this map being **cited as authority by, or listed as a `downstream_consumer` of, an owner source** (see queue, ORCA-HYGIENE-006). A maintenance pass that edits this map may list it in its own `controlling_sources_updated` — that is upkeep, not a breach.
- **Deferred routing/hardening** (triggers tracked, not forgotten) → `docs/hygiene/queue.md`: repo-map pointer + scatter retirement, README trim, harness-README up-pointer, product-tree reach (ORCA-HYGIENE-008); one-way restraint hardening (ORCA-HYGIENE-006); pattern promotion (ORCA-HYGIENE-007).

## Non-Claims

- Not source-of-truth, validation, readiness, buyer proof, judgment-quality evidence, fixture admission, scoring, or gate clearance.
- Not authorization for implementation, model/probe execution, commits, or pushes.
- A map of the corpus; every load-bearing claim lives in, and is owned by, the pointed-to source.
