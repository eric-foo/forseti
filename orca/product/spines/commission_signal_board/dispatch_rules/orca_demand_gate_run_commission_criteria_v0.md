# Orca Demand-Gate Run Commission Criteria - LEGACY NON-CONTROLLING v0

```yaml
retrieval_header_version: 1
artifact_role: Legacy non-controlling product artifact (superseded gate-run criteria)
status: legacy_non_controlling
scope: >
  Preserved historical gate-run criteria from before the Commission Signal
  Board was corrected into an evidence/signals-only board. This artifact is not
  a live CSB dispatch rule and must not be used to run a CSB board, produce a
  CSB classifier handoff, or infer current CSB admit/hold/fail behavior.
use_when:
  - Historical comparison only when investigating pre-CSB gate-run language.
  - Understanding why current CSB prompt/playbook artifacts explicitly reject gate verdicts.
authority_boundary: retrieval_only
superseded_by:
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
open_next:
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
```

## Supersession Notice

This file is retained only as historical context. It is not a live Commission
Signal Board authority surface.

Current CSB authority lives in the prompt and playbook listed above. Current CSB
behavior is an evidence/signals-only board plus graph retrieval brief and
demand-classifier handoff packet. The board must not output `admit`, `hold`,
`fail`, `pass`, `reject`, demand verdicts, buyer-proof claims, readiness claims,
forecast probabilities, graph scores, or judgment recommendations.

Any future demand-gate run belongs to the product-lead / buyer-proof surfaces
under their own authority. It does not live in the CSB spine unless the owner
explicitly re-authorizes that boundary in a new artifact.

## What This Is (and Is Not)

Historical content below is intentionally left intact for comparison. It is
non-controlling for current CSB work.

This artifact defines the **gate-run commission criteria**: the input, procedure,
and output shape for taking **one** candidate through the live Demand-Substrate
Hard Gate so a human-in-session can reach a determinate verdict. It
operationalizes **qualification objective #3** of the discovery brief
("Confirm the Demand-Substrate Hard Gate is satisfiable for this decision").

The controlling gate logic lives in the buyer-proof packet's **Demand-Substrate
Hard Gate** (G1 independence/verb-tiering, G2 gradeable costly-behavior floor,
G4 org-motion corroboration, integrity labels, divergence/defeater) and the
discovery brief (qualification objective #3 + slot table). This artifact does
**not** restate or re-derive that logic — it **references** it and defines how to
**run** it. On any conflict, the buyer-proof packet's gate controls.

It is **not**:

- an automated scoring or weighting engine (the single most expensive drift —
  forbidden; weighting stays qualitative / LLM-in-session until the owner
  explicitly lifts the boundary);
- a candidate scan (the scan is the **input**, produced by a separately
  authorized candidate-scan lane);
- a courier prompt that routes a lane to run the gate (that is authored
  separately via `.agents/workflow-overlay/prompt-orchestration.md`, and would
  **reference** these criteria);
- buyer proof, validation, readiness, or gate clearance for any actual
  candidate.

## Stage A — Scan (input)

A gate-run consumes exactly one **dated, provenance-noted candidate scan**
produced by an authorized candidate-scan lane (research artifact under
`docs/research/`, filename prefix `orca_discovery_candidate_scan_`; per the
discovery brief slot-fill rule). A gate-run is **never** run from memory, from
another lane's unverified summary, or from the backtest candidate pool.

The scan must carry enough for the gate-run to be decidable:

- candidate context: brand (Brand) + the live 30-90 day demand-allocation decision (DecisionEvent), and
  the decision family;
- the observed demand-venue signals (Observation), each with **origination provenance**
  (where it originated, and any `derived_from` / `diverges_from` links) so
  origin de-correlation can be applied;
- observed costly-behavior instance(s), if any, with enough to judge
  "gradeable" (attributable to buyer actions / direction + rough magnitude /
  corroborable);
- observed org-motion / retail-placement signals (corroboration material);
- any evidence bearing on durability projection or decay (observed recurrence,
  repeated costly behavior, post-trigger follow-through, analogue/base-rate
  support, event/seasonality, scarcity/panic, or explicit absence of such basis);
- the named decision owner and the concrete allocation consequence (or their
  absence).

If a required input is missing, the gate-run returns **insufficient-input**
(not a fail) and names what the scan must add — it does not guess.

## Stage B — Gate-Run (procedure)

Apply the live gate qualitatively, in-session, against the scan's evidence, in
this order. Each step is a judgment, not a number.

1. **Origin de-correlation (G1).** Map each demand signal to its origination
   event. Collapse to **one** origin any signals that derive from each other or
   trace to a common upstream origination event or a shared coordinated
   origination (laundered siblings collapse). Count the **independent
   demand-venue origins**. Today only forums/community is a sourced demand-family
   card; review-surface and search-interest are unsourced gaps; **org-motion and
   retail presence are corroboration (G4), excluded from the origin count.**
2. **Costly-behavior floor (G2).** Is there **≥1 gradeable** costly-behavior
   instance — attributable to identifiable buyer actions (not aggregate
   mood/attention), statable with a direction and rough magnitude, and
   corroborable — **evidenced in ≥1 qualifying demand-venue family**,
   distinguishable from attention volume? If **no**, the candidate **FAILS**
   (floor not cleared); engagement/attention/resonance volume alone never clears it.
3. **Integrity + divergence + defeater.** Apply integrity labels to each venue's
   evidence. Read divergence (`diverges_from`). Apply the **defeater**: if the
   divergence pattern indicates the costly-behavior instance is itself likely
   manufactured/coordinated (e.g., the only costly signal sits inside the same
   coordinated layer divergence flags), divergence **defeats the floor** → FAIL
   or hold, not merely a lower ceiling.
4. **Verb-tier the ceiling.** The independent-origin count tiers the action
   ceiling, not a binary pass: **one** independent origin (or laundered copies of
   one) → **hold / low-commitment** ceiling; **≥2 converging independent origins**
   → **material-action eligible** (commit or scale). Org-motion corroboration may
   raise confidence but does not raise the origin count. Transient/durable labels
   are not strength tiers here: weak, attention-only, or resonance-only input
   fails or holds; it is not transient demand. Durable remains a later Judgment horizon call that
   needs a named persistence-projection basis.
5. **Owner + consequence check.** A gate-run that clears the floor still requires
   the brief's other objectives for a slot to be live: a **named decision owner**
   and a **concrete allocation consequence**. Their absence is a hold/disqualify
   at the brief level even when the substrate clears.

## Stage C — Filled Discovery Slot (output)

Every gate-run yields **exactly one** determinate verdict with a one-line basis
citing the deciding step:

- **`admit @ <ceiling>`** — floor cleared, not defeated; ceiling set by the
  origin count (`hold/low-commitment` on one origin, `material-action eligible`
  on ≥2 converging independent origins), and a named owner + consequence present.
  If the scan carries a durability-projection basis or decay discriminator, pass
  it through; the gate-run does not itself emit the durable/transient verdict.
- **`hold`** — floor cleared but capped (single origin, owner/consequence not
  yet confirmed, or no durability-projection basis for the requested material
  horizon), or divergence caps without defeating.
- **`fail`** — floor not cleared (no gradeable costly-behavior instance, or no
  qualifying demand-venue origin at all), defeater triggered, or signal only via
  an out-of-bounds / absurd-risk route.

Routing:

- **`admit`** fills a discovery-brief **target slot** row, sourced from the dated
  scan (per the slot-fill rule), recording: candidate context; decision family;
  **independent demand-venue origins visible** (after collapse); costly-behavior
  evidence visible (gradeable y/n); org-motion route available (corroboration);
  named decision owner; status = `admit @ <ceiling>`.
- **`hold`** / **`fail`** do **not** fill a slot; they route to the proof-batch
  notes home (`docs/product/product_lead/orca_proof_batch_<n>_notes_v0.md`) as a
  hold / near-miss / disqualification record with the deciding-step basis.

A filled slot is **admissibility for a memo (Memo) at the stated ceiling** — it is not
buyer qualification, not paid-first willingness, and not buyer proof. Those are
separate objectives (#4–#6) and separate gates.

## Determinacy Contract

A valid gate-run is **decidable and auditable**: one verdict in
`{admit @ <ceiling>, hold, fail, insufficient-input}`, a one-line basis naming
the step that decided it, and a pointer to the dated scan it consumed. No numeric
score, weight, or threshold is produced or required — the determinacy comes from
the ordered qualitative decision points above, not from a scoring pipeline.

## Non-Claims

- PROPOSED design — owner ratification is owed before these criteria govern an
  actual commission; authoring them does not authorize running a candidate.
- Not a scoring engine, not automation, not a collection pipeline, not a
  dashboard. Weighting stays LLM-in-session / qualitative.
- Not validation, not readiness, not buyer proof, not gate clearance for any
  candidate. A gate-run `admit` is memo-admissibility at a ceiling, nothing more.
- Does not reopen or re-derive the ratified P2/P3/P4 gate decisions; it runs the
  gate the live instruments now carry.
```
