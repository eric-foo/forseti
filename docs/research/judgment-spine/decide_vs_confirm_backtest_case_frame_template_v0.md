# Decide-vs-Confirm Backtest Case-Frame Template v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine case-frame template / test-design scaffold
scope: >
  Reusable frame template + test design for two decide-vs-confirm backtest cases
  (one repricing, one clean-substrate competitor-displacement), to be authored as
  Judgment Spine cases when the proof lane resumes. Captures the test design,
  scoring frame, four-lane structure, and subject-selection gate. Holds NO real
  subjects, evidence, or outcomes — those are NEEDS_SUBJECT / NEEDS_CAPTURE.
use_when:
  - Resuming Judgment Spine case work on the decide-vs-confirm crux test.
  - Authoring the two crux backtests once obscure subjects are identified.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md
  - docs/research/judgment-spine/manifest_v0.md
  - docs/decisions/orca_moat_judgment_quality_proof_path_decision_chain_v0.md
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md
stale_if:
  - The construction protocol four-lane structure or acceptance criteria change.
  - The decide-vs-confirm crux is resolved or withdrawn.
  - Subjects are identified and real case folders are authored (this template is consumed).
```

## Status

`TEMPLATE_PENDING_SUBJECTS_AND_CAPTURE`. This is a test-design scaffold, not two
runnable cases. It contains no real subjects, evidence units, or outcomes; those
are marked `NEEDS_SUBJECT`, `NEEDS_CAPTURE`, `NEEDS_OUTCOME` and are filled only
when the lane resumes. It fabricates nothing, authorizes no capture / discovery /
build / run, and asserts no proof. Product-learning cap; no buyer contact.

**Why subjects are deferred (recorded honestly):** the cases must be
memorization-resistant — obscure enough that frontier models have NOT memorized
the outcome. A case the authoring model can recall in detail is, by that fact,
probably memorized and therefore disqualified. So subjects must be sourced *below*
the model's recall threshold — by the case finder or external research — not
free-associated by the authoring model. See the moat→proof decision chain (D4).

## What this test is

The decide-vs-confirm crux: does clean public signal **DECIDE** a high-stakes
call, or merely **CONFIRM** one after the fact? This is the open question the
pricing-first wedge and the decision chain (D2) rest on — untested, not proven.

Two cases:

- **Case A — pricing / repricing:** does competitor price/packaging signal DECIDE
  a repricing move, or only confirm it?
- **Case B — clean-substrate competitor-displacement:** can clean *non-review*
  public signal carry the "why are customers leaving competitor X" read?

Each is a Judgment Spine backtest scored on decide-vs-confirm. **Capped at
`product_learning`** (run by-hand, or later via the middle-rung path). Not
buyer-proof, not judgment-quality, until the controlling gates are separately met.

## Decide-vs-confirm scoring frame (the load-bearing design)

This is the reusable IP this template preserves.

1. Seal an at-cutoff blind judgment built from **clean pre-cutoff public signal
   only** (zero-spoiler; no outcome, no post-cutoff facts).
2. The blind judgment yields a recommended action level; the sealed facilitator
   ledger yields the deterministic action band (floor/ceiling). Standard band
   scoring gives in-band / over / under.
3. Layer the decide-vs-confirm read **on top** of band scoring:
   - **DECIDE** = the at-cutoff public-signal read would have *moved the decision*
     — named the action the decision-maker actually took (or a defensibly better
     one), on evidence available *before* cutoff that a decision-maker could have
     acted on without internal/private data.
   - **CONFIRM** = the read only *agrees after the fact*, or the pre-cutoff signal
     was insufficient to drive the call (it merely fails to contradict it).
   - Discriminator question: seeing only Orca's at-cutoff read, would the owner
     have made the move — or would they still have needed more / internal data?
4. **AR-S2 substrate-newness probe (required):** for newly-set / first-time
   prices, record whether the competitor-price substrate was decision-grade *at
   cutoff*, or whether it required at least one observable pricing
   iteration/anchor. Do not let "publicly rich" pass as "decision-grade."
5. Preserve all backtest result labels (useful, wrong, early, late,
   over/under-confident, blocked, inconclusive) as calibration input.

## Four-lane structure (per construction protocol — fill on resume)

Per `judgement_case_construction_protocol.md`, each case folder is
`cases/<batch>/<case_id>/` with:

- `participant_packet.md` — zero-spoiler, with required frontmatter (case_id,
  decision_question, decision_date_or_cutoff, role_frame, authority/capability
  constraints, permitted_assumptions, forbidden_information_notice,
  source_manifest). MUST EXCLUDE actual outcome, actual decision (if avoidable),
  frozen band inputs, derived floor/ceiling, must-address items, post-decision
  interpretation.
- `facilitator_ledger.yaml` — sealed (scorer/operator only): frozen band inputs,
  second-label diffs, must-address items, `underreach_observability`, and a
  `leakage_audit` (memorization_probe_required, known_fame_risk,
  spoiler_inventory), plus `ledger_freeze_hash`.
- `evidence/*.yaml` — real pre-cutoff evidence units (id, source, type, timestamp,
  retrieval_timestamp, hash, pre_decision_status, summary).
- `runs/`, `scores/`.

## Subject-selection gate (apply when identifying subjects)

A subject qualifies only if ALL hold:

- **Memorization-resistant:** obscure / low public fame / below model recall — the
  gate that makes the blind judgment actually blind.
- **Selection-Rule-for-Case-2 (manifest):** reconstructable decision, clean
  cutoff, visible tradeoff, revealed action/outcome, enough pre-cutoff source
  depth to expose judgment misses.
- **Decision-family match:** Case A = pricing/packaging/monetization repricing;
  Case B = clean-substrate competitor-displacement (carried by non-review public
  signal).
- **Zero-spoiler feasibility:** a clean pre-cutoff packet can be built without the
  outcome leaking.
- **Decide-vs-confirm tension:** at cutoff the outcome was genuinely not obvious.

## Case slots (NEEDS_SUBJECT — fill on resume)

### Case A — repricing
- subject: `NEEDS_SUBJECT`
- decision_question / owner_context / cutoff: `NEEDS_SUBJECT` (cutoff = replay gate, `NEEDS_VERIFICATION` until confirmed)
- decision_family: pricing / repricing / packaging / monetization
- decide_vs_confirm_hypothesis: `NEEDS_SUBJECT`
- evidence_units: `NEEDS_CAPTURE` (capture lane; cutoff-disciplined)
- sealed_outcome: `NEEDS_OUTCOME` (facilitator-only)
- anti_cherry_pick_rationale / post_window_exclusion_rule: `NEEDS_SUBJECT`

### Case B — clean-substrate competitor-displacement
- subject: `NEEDS_SUBJECT`
- decision_question / owner_context / cutoff: `NEEDS_SUBJECT` (`NEEDS_VERIFICATION`)
- decision_family: competitor-displacement / why-customers-leave read on non-review public signal
- decide_vs_confirm_hypothesis: `NEEDS_SUBJECT`
- evidence_units: `NEEDS_CAPTURE`
- sealed_outcome: `NEEDS_OUTCOME`
- anti_cherry_pick_rationale / post_window_exclusion_rule: `NEEDS_SUBJECT`

## Resume recipe (when the lane resumes)

1. The case finder (D4) or external research surfaces 2 obscure subjects passing
   the gate above — not authorable from the model's own memory.
2. Frame-lock each (fill the slots), mirroring the existing Core-Spine
   method-validation case-frame-lock pattern; keep cutoff fields
   `NEEDS_VERIFICATION` until confirmed.
3. Capture real pre-cutoff evidence units (capture lane; cutoff-disciplined).
4. Seal the facilitator ledger with the real outcome, band inputs, and freeze hash.
5. Run per the chosen evidence path (middle rung, D6) in a fresh thread; wire the
   memorization probe.
6. Score decide-vs-confirm; classify the claim tier with a
   `judgment_spine_claim_classification` record (product-learning cap).
7. Register the real cases in `manifest_v0.md`; this template is then consumed.

## Dependencies / blockers

- **Subjects:** the case finder (D4) or external research — NOT authorable from
  model memory (memorization paradox above).
- **Evidence:** the capture lane (cutoff-disciplined); gated.
- **Judgment-quality via middle rung:** ECR up (D7). A product-learning by-hand
  decide-vs-confirm read may precede that.

## Non-Claims

Not two real cases. No subject, evidence, outcome, cutoff, or source is asserted
or implied. Not validation, willingness-to-pay, buyer proof, judgment-quality, or
ICP-proven. Product-learning cap. Authorizes no capture, discovery, build, or run.
Freezes nothing.

Dirty-state: written on the current ECR branch (`ecr-sp3-timing-deriver-slice1`),
untracked; durable-home reconciliation to the product/judgment lane is a separate
step.
