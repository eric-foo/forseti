---
artifact_role: R2 packet construction receipt — outcome-blind construction chain record
scope: >
  Documents the construction chain for the nueco_fragrance_pivot_v0 participant
  packet under the Batch 2 outcome-blind construction rule (conductor addendum v1
  R2). Records the neutralized build capsule, the outcome-blind builder, the
  withheld material, the R6 leakage review, the facilitator band adoption, and the
  packet/ledger hashes for audit. This case's contestant-facing case_id is
  NEUTRALIZED (b2_holdout_h7_v0) per the slice-2 handoff's explicit instruction;
  the case lives in cases/product_learning/nueco_fragrance_pivot_v0/.
authority_boundary: retrieval_only
---

# Packet Construction Receipt — nueco_fragrance_pivot_v0 (contestant-facing case_id: b2_holdout_h7_v0)

## Neutralized identity

- Real case (dir / batch home): `nueco_fragrance_pivot_v0` (The Nue Co. — owner-included
  Batch 2 border holdout, 7th holdout).
- Contestant-facing case_id used in `participant_packet.md`, `facilitator_ledger.yaml`,
  `blind_judgement.yaml`, and the machine-generated `case_report.yaml`:
  **`b2_holdout_h7_v0`** (neutral; carries no outcome cue).
- Why: the directory name `..._fragrance_pivot_...` and the capture-side provenance
  state the post-cutoff outcome. The slice-2 handoff explicitly required a neutralized
  case-id for nueco so the contestant is not cued by the case name. Because the
  participant_packet hash binds exactly the text the contestant judged, the neutral
  case_id is carried in the committed artifacts themselves (not stripped at run time).
  Consequence: the generated case report lands at
  `reports/product_learning/b2_holdout_h7_v0/case_report.yaml` (keyed by case_id), while
  packet/evidence/run/findings live in `cases/product_learning/nueco_fragrance_pivot_v0/`.
  This is a deliberate, documented deviation from slice-1 (which used outcome-hinting
  case_ids); it strengthens contestant blindness for this border case.

## Construction chain

| Step | Actor | Session | Outcome-aware? |
|------|-------|---------|---------------|
| R2: Blind packet build | Outcome-blind subagent (Agent tool, `claude-sonnet`, separate fresh context) | batch2-exec-slice2 worktree session | No — neutralized bodies-only capsule; outcome withheld |
| Band-input structural read | Same outcome-blind subagent (`decision_structure_notes.md`) | same as R2 | No — 14-axis read derived from the pre-cutoff evidence only |
| R6: Pre-freeze leakage review | Orchestrator (Opus, outcome-aware) | same session | No — review only checked for outcome leakage; confirmed clean |
| Band adoption (facilitator) | Orchestrator | same session | Outcome-aware actor, but adopted the blind builder's structural read **verbatim** (no outcome-tuned adjustment); owner ratification pending |

## Neutralized build capsule (what the blind builder received)

The blind builder received ONLY:
- the 7 raw archived HTML page bodies (`raw/02_archive_snapshot_body.bin`), copied to
  neutral scratch paths `captures/E1.html` … `E7.html`;
- a neutral facts table per unit (source URL, snapshot timestamp, raw-body SHA-256,
  byte size) — all pre-cutoff capture facts;
- a neutral case-id (`b2_holdout_h7_v0`), a 2020-01-01 cutoff, and a symmetric,
  non-presupposing decision framing.

It did NOT receive: the case directory name, the capture `manifest.json` / `receipt.md`
(see Withheld), the `source_provenance_notes_v0.md`, or any post-cutoff fact.

## Withheld material

The following outcome-containing material was held by the orchestrator and never passed
to the blind builder or included in the participant packet:

- **Primary (roster-stated, held, not independently verified here):** after the
  2020-01-01 cutoff, fragrance grew from ~20% to ~65% of revenue; customer-acquisition
  cost roughly halved; an Ulta retail exclusive was entered. (The brand "pivoted to
  fragrance-first.")
- **Capture-metadata leak, excluded:** every nueco capture's `manifest.json` and
  `receipt.md` carry a `requested_decision_context` / "Decision question" string that
  states the fragrance pivot and the ~20%→~65% revenue shift. These files were excluded
  from the build capsule; only the raw body + body-metadata (which carry no outcome) were
  provided.
- **Directory-name hint:** `nueco_fragrance_pivot_v0` — replaced with `b2_holdout_h7_v0`.
- **Capture-side provenance:** `source_provenance_notes_v0.md` (roster outcome section).

## R6 review result

**Clean — no outcome leakage.** The blind builder framed a symmetric strategic question
(deepen DTC subscription vs broaden range / channels / geography) and explicitly stated
the evidence does not establish the chosen path or its outcome. "Functional Fragrance"
appears only as one pre-cutoff SKU among 17+ (gut-health / skin / sleep / energy /
immunity / stress-led), i.e. a legitimate observed pre-cutoff signal, not a directional
hint toward the held outcome. `forbidden_information_notice` is whitelist-only with no
directional enumeration. Evidence YAML schema is correct as built (`source_type:
archive_org_wayback`, `hash_basis: raw_stored_bytes`, `pre_decision_status:
verified_pre_decision`); no orchestrator schema rewrite was required. All seven
`source_manifest` / evidence hashes bind verbatim to the real capture bodies.

## Band (facilitator key, adopted from the outcome-blind structural read)

- frozen_band_inputs: adopted verbatim from the blind builder's `decision_structure_notes.md`.
- derived band: **action_floor 3, action_ceiling 5, band_status normal** (band_width 2).
- ledger_freeze_hash: `a9150d51b5150a4b2e69f93b335494cc1fce1058cf5bae9cf885be609e6a54c4`
- Rationale for verbatim adoption: the facilitator is outcome-aware, so adopting the
  blind, outcome-free structural read (rather than authoring the key under outcome
  knowledge) removes any outcome-tuning of the answer key. Owner ratification of the
  band is **pending** (`second_labeler: owner (pending)`).

## Memorization / fame note (carried to the run)

The Nue Co. is a recognizable DTC wellness brand; the facilitator ledger flags
`memorization_probe_required: true` and `known_fame_risk`. Recognition was collected from
the contestant at run time (see findings); the scorer's `memorization_probe_result`
remains `not_run` (the structural probe is not implemented in the scorer).

## Packet hash

| Artifact | SHA-256 |
|----------|---------|
| `participant_packet.md` | `2a04dacc2fc870fc8048b9e15c96ee9d2bbc854e1cbecd248cf9799bc3677037` |

## Non-claims

Not validation, not readiness, not buyer-proof. Plumbing-grade product-learning fixture.
Cutoff-date uncertainty (2020-01-01 is a defensible supplements-led-era anchor, not a
confirmed pre-majority-fragrance date) and BORDER US/UK status are carried from the
capture-side provenance and remain real limitations.
