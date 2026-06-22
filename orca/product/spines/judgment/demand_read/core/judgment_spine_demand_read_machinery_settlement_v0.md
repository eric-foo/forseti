# Judgment-Spine Demand-Read Machinery Settlement v0

```yaml
retrieval_header_version: 1
artifact_role: Product and architecture doctrine settlement for Orca demand-read machinery
scope: >
  Settles demand-read naming, C0-C4 behavior, C2/C3 interaction, action ceiling,
  monitoring/durability boundary, proof status, and patch implications.
use_when:
  - Deciding how Orca names and operates durable, transient, and manufactured demand reads.
  - Routing downstream Capture, ECR, Cleaning, Judgment, Product Lead, Outcome Memory, or satellite demand-read work.
  - Checking whether a demand-read surface is using stale vocabulary or overclaiming proof.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
  - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
  - orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
  - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
stale_if:
  - The owner amends the demand-state model, C2/C3 contracts, action vocabulary, buyer-proof hard gate, or monitoring/durability rule.
  - A later accepted demand-read settlement supersedes this artifact.
```

## Status

`SOURCE_CONTEXT_READY`.

This is a settlement artifact for product and architecture doctrine. It is not
validation, buyer proof, judgment-quality proof, readiness, implementation
authorization, capture authorization, or a scoring engine. It authorizes no
runtime, scraping, automation, scheduler, database, dashboard, source-system,
capture route, or API work.

## Start Preflight Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_S3_demand_read_machinery
  edit_permission: docs-write
  target_scope: product doctrine + architecture doctrine settlement for demand-read machinery only
  dirty_state_checked: yes
  dirty_state_result: clean worktree, branch codex/demand-read-machinery-settlement-prompt, origin/main ancestor of HEAD
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
    - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
    - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
    - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
    - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
```

Cynefin route: `complicated`. The safe decomposition is layer-based: source-load
the controlling product and Judgment sources, then settle naming and operating
boundaries. Disallowed move: implementation, capture, monitoring-service design,
or broad downstream patching from this artifact.

## Source Context

Read as controlling sources:

- `docs/decisions/orca_product_thesis_consumer_demand_v0.md`: status, active
  reading, thesis, value proposition, central read, product boundary, falsifiers,
  and non-claims.
- `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md`:
  status, function, signal layers, read types, calling sequence, and non-claims.
- `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`:
  consumer-demand refinement, demand-substrate hard gate, proof standard, target
  buyer, evaluation rubric, buyer pull, kill criteria, graduation criteria,
  what must not be built yet, and not-proven boundaries.
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`:
  status, target architecture, C0-C4 core, shell plug points, invariants,
  deferred implementation implications, non-claims, and claim classification.
- `orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md`:
  status, input basis, required behavior, Rule 3, acceptance criteria,
  checking posture, claim classification, and non-claims.
- `orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`:
  status, 2026-06-20 amendments, input basis, required behavior, interfaces,
  acceptance criteria, claim classification, and non-claims.

Read as procedural or boundary sources:

- `AGENTS.md`.
- `.agents/workflow-overlay/README.md`.
- `.agents/workflow-overlay/decision-routing.md`.
- `.agents/workflow-overlay/source-loading.md`.
- `.agents/workflow-overlay/prompt-orchestration.md`.
- `.agents/workflow-overlay/source-of-truth.md`.
- `.agents/workflow-overlay/product-proof.md`.
- `.agents/workflow-overlay/retrieval-metadata.md`.
- `.agents/skills/orca-product-lead/SKILL.md` as task-local method guidance only.

Excluded by default:

- Closed PR #260 historical durability-probe artifacts.
- Broad review outputs.
- Prompts other than the commissioning prompt.
- Proof-run packets.
- Runtime, source-capture, scraping, automation, and implementation files.

## Human Summary

Orca should keep `transient demand` as the internal canonical term. It is the
precise state: demand is real, but persistence has not been earned or the signal
is expected to decay. For buyer-facing prose, use `real-but-short-window demand`
on first mention and `short-window demand` once realness is already clear.

Do not use `trendy` as a demand-state label. It sounds like fashionability,
creator buzz, or category heat. That is exactly the wrong frame: a trend can be
durable, transient, or manufactured, and "trendy" invites social-listening
interpretation instead of decision-grade demand classification.

The two-axis model stays: persistence is `durable | transient`; integrity is
`real | manufactured`. The first real-demand call opens conservative as
transient unless the read already contains observed post-trigger persistence.
Durable is earned by monitored persistence, not predicted upfront. The live
action vocabulary remains exactly seven verbs: `monitor`, `probe`, `commit`,
`hold`, `scale`, `avoid`, `reduce`.

## Naming Decision

Internal canonical term:

- `transient demand`.

Buyer-facing term:

- Formal first mention: `real-but-short-window demand`.
- Short form after realness is established: `short-window demand`.
- Internal or technical appendix language may still say `transient demand`.

Rejected terms:

- `trendy`: rejected hard. It confuses demand state with fashion/buzz, does not
  distinguish real from manufactured, and weakens Orca's separation from trend
  feeds.
- `spike demand`: allowed only as an example of a transient pattern, not as the
  canonical label. A spike can be manufactured; the term overweights volume.
- `momentum demand`: rejected as canonical because momentum may persist or decay.
- `in-window demand`: acceptable as operating prose for action timing, but too
  opaque as a buyer-facing state label.
- `hollow`: forbidden as a live demand-state label. It is retired because it
  conflated real-but-decaying demand with manufactured demand.
- `discount` as an action verb: forbidden in the action-ceiling vocabulary. It
  may remain as C2 risk-weighting language only where it means a qualitative
  trust discount, not an action ceiling.

Rationale:

`Transient` preserves the current source model and keeps the persistence axis
separate from integrity. Buyer-facing `short-window` translates the implication:
there is a real decision window, but the evidence has not earned durable scale.

## Demand-State Model

Confirmed without amendment:

```text
integrity axis:   real | manufactured
persistence axis: durable | transient
```

The actionable external states are:

- `real + durable`: demand has persisted past the trigger; commitment may deepen
  as the evidence ceiling permits.
- `real + transient`: demand is real, but unearned for durability or observed as
  decaying; act in-window and monitor.
- `manufactured`: the demand is not real enough to support entry; avoid or hold
  below material commitment as upstream disposition permits.

Manufactured demand is not a third persistence state. It is the integrity-axis
failure that protects both real states.

## Calling Sequence

Confirmed without amendment:

1. First call opens transient for real demand unless observed persistence is
   already inside the information set.
2. The initial action is immediate and evidence-capped. It does not wait for a
   monitor if an in-window decision exists.
3. Monitoring observes whether the signal persists past the trigger.
4. Durable is earned only after monitored persistence holds. It is never asserted
   at trigger time because it "feels durable."
5. If monitored demand decays, the read stays transient and the action path moves
   toward `reduce`, `hold`, `probe`, or `avoid` depending on position and evidence.

## Machinery Decision: C0-C4

The demand-read machinery is one Judgment core consumed by existing shells, not
a new runtime system.

| Step | Settled behavior | Owner boundary |
| --- | --- | --- |
| C0 Frame | A demand read starts inside a concrete Decision Frame: buyer/context, decision family, timing, consequence, and live or historical information set. | Product Lead and Judgment consume the frame; Product Lead owns buyer/proof framing; Judgment owns read execution boundaries. |
| C1 Allow | Apply the Demand-Substrate Hard Gate: qualifying demand origin, gradeable costly behavior floor, integrity labels, and enough de-correlated origins for the commitment claimed. | Buyer-proof packet owns the gate; Capture/ECR/Cleaning provide provenance, source, entity, and integrity inputs; Judgment routes to the gate and consumes the disposition. |
| C2 Weight | Qualitatively weight allowed signals by de-correlating origin chains, reading divergence as signal, consulting the ledger within `decision_family`, carrying caveats, and applying Rule 3. | Judgment owns C2 trace behavior; ledger/lesson owners provide track record; no numeric scoring or deterministic table. |
| C3 Verdict + Action Ceiling | Emit the two-axis verdict and exactly one action verb from `monitor`, `probe`, `commit`, `hold`, `scale`, `avoid`, `reduce`. Default to transient absent observed persistence. Cap by weakest load-bearing evidence. | Judgment owns verdict and ceiling. Product Lead owns buyer-facing action communication and proof constraints. |
| C4 Counterfactual | State what evidence would change the answer, including what must be monitored, what discriminator must run, or what buyer/proof fact would reopen the call. | Judgment owns the counterfactual trace; Product Lead uses it in memo/deck/readback; Outcome Memory consumes it later. |

## Source-Owner Boundaries

- Product Lead owns buyer-facing framing, first-proof gating, buyer pull versus
  praise, trust-objection semantics, proof kill/graduation, and the memo/deck
  packaging boundary.
- Capture owns source access, route bindings, source packets, attended/bounded
  capture operations, and measured-risk route decisions. This settlement does
  not authorize capture.
- ECR and Cleaning own source-side record integrity, provenance, entity
  resolution, de-duplication, and prepared evidence surfaces.
- Judgment owns the C0-C4 read procedure, qualitative trace, no-scoring
  invariant, C2/C3 behavior, and C4 counterfactual.
- Outcome Memory owns observed persistence, decay, resolution, and calibration
  feedback once a read is monitored or resolved.
- Satellites own vertical-specific signal tells and discriminator families.
  They do not rename the core states or mint new action verbs.

## C2/C3 Settlement

C2 and C3 split cleanly:

- C2 answers how much each allowed signal should matter, qualitatively, inside a
  decision family.
- C2 Rule 3 handles manufactured-axis integrity risks: confirmed present caps,
  unconfirmed discounts by reversibility, confirmed absent returns to neutral.
- Persistence-axis patterns are not manufactured-axis caps. C2 passes them to C3
  as evidence for a transient verdict.
- C3 answers the demand-state verdict and action ceiling.
- C3 cannot call durable unless observed post-trigger persistence is in the
  information set.
- C3 cannot emit a verb outside the seven-verb set.
- C3 cannot exceed the weakest load-bearing evidence. `commit` and `scale` need
  the material bar: gradeable costly behavior plus enough effectively independent
  converging origins. A single independent origin caps below material commitment,
  usually at `monitor`, `probe`, or `hold`.

No-scoring invariant:

- No numeric score, ordinal weight, deterministic threshold table, or formula may
  map signal counts or ledger rows to a verdict or verb.
- The only count-like structural rule preserved here is the source-independence
  bar for material commitment. It is a gate/ceiling condition, not a score.

## Action Ceiling

Confirmed complete set:

- `monitor`: observe; no position taken.
- `probe`: small reversible action to learn.
- `commit`: take a real position, reversible by default unless context makes it
  material or irreversible.
- `hold`: maintain current stance or hold off before committing.
- `scale`: increase an existing commitment; earned by monitored persistence or
  exceptional integrity-cleared outburst.
- `avoid`: do not enter or discount as an action path.
- `reduce`: wind down existing exposure as real demand decays.

No separate horizon output is allowed for C3. Horizon accretes through monitoring:
`scale` earns longer-horizon conviction; `reduce` handles decay.

## Proof Status

What is designed or proposed:

- Demand-read taxonomy: proposed grammar.
- Demand-read core architecture: design/product-learning context.
- C2 ledger read contract: proposed behavior/contract spec, product-learning
  tier, no real row or run.
- C3 verdict/action ceiling contract: proposed behavior/contract spec, product
  learning tier, no executed verdict.
- This settlement: doctrine settlement for naming and machinery boundaries.

What is owner-adopted or owner-locked in the loaded sources:

- Product thesis direction and central read.
- The demand-read C0-C4 core as an adopted step shape according to C2/C3 input
  bases.
- The seven-verb action vocabulary as current operative action-ceiling vocabulary.
- The two-axis demand-state model as current operative model.

What remains gated:

- Buyer proof requires qualified live decision, memo plus evidence appendix,
  readback, and pull-versus-praise classification.
- Judgment-quality proof requires the separate harness-grade gates.
- Durable-demand confidence requires observed persistence, not a naming decision.
- Runtime feasibility, capture feasibility, source-system feasibility, and
  automation readiness are not proven.

## Proof-Side Demand Read

The proof side does read demand; it just reads demand under a buyer-proof gate.
The buyer-proof packet owns the target buyer, live decision trigger,
Demand-Substrate Hard Gate, memo/evidence appendix, readback, pull standard,
kill criteria, and graduation criteria. The demand-read machinery supplies the
substantive read inside that proof artifact:

- Is the visible demand real or manufactured?
- If real, is it durable or real-but-short-window?
- What evidence-supported action ceiling can the buyer use now?
- What would change the answer after monitoring or outcome memory?

Proof-side language should therefore translate internal `transient demand` as
`real-but-short-window demand` or `short-window demand` in buyer-facing prose,
while technical proof artifacts may retain `transient demand` when naming the
internal state. A buyer using a memo is buyer-proof evidence only when the
buyer-proof packet's live-decision, memo, readback, and pull gates are satisfied;
it is not proof that the demand-read model is validated.

## Monitoring And Durability Rule

A read can upgrade from transient to durable only when the monitoring loop
observes persistence past the trigger in the same Decision Frame or a clearly
linked continuation. The observation must preserve:

- dated post-trigger evidence;
- gradeable costly behavior, not attention volume alone;
- de-correlated origin logic for any material action;
- integrity labels and manufactured-risk disposition;
- the original C3 counterfactual or a dated amendment explaining why the
  evidence would change the answer;
- a trace that distinguishes persistence from a repeated manufactured or
  laundered signal.

Unknown threshold:

- The exact cadence, minimum duration, number of observations, and persistence
  threshold are not settled here. They are an owner/product-learning decision
  for the first monitored series or outcome-memory lane.
- Until that threshold exists, durable upgrades are allowed only case-by-case
  when the information set visibly contains post-trigger persistence evidence.
  There is no hidden default monitor duration.

## Robustness Path

Smallest path to test whether the demand read is actually strong:

1. Run by-hand C0-C4 reads on a small set of cases or qualified live decisions
   using the current seven-verb ceiling and no-scoring invariant.
2. Record the C3 verdict, C4 counterfactual, evidence caps, and uncertainty in
   a memo plus evidence appendix.
3. For transient calls, create a monitored series or outcome-memory record that
   checks the exact counterfactual: persistence, decay, or manufactured failure.
4. Use buyer readback only after a qualified decision owner and live decision
   exist; classify pull versus praise under the buyer-proof packet.
5. Use judgment-quality backtest only when the frozen-packet and scoring gates
   are separately satisfied.

The strongest near-term test is not a dashboard. It is a by-hand read plus
outcome memory on whether the transient/durable call and action ceiling survive
observed persistence or decay.

## Code-Enforceable Versus Judgment-Only Obligations

Code-enforceable or mechanically checkable:

- Retrieval header presence and controlled `authority_boundary`.
- C3 output schema using one of the seven verbs.
- No C3 `horizon` output field when the field means action horizon.
- Search gates for forbidden live action verbs: `act`, `phase`, `narrow`,
  `defend`, or `commit | move` as the old verb/horizon interface.
- Search gates for `hollow` where it is not explicitly a retirement/history note.
- Search gates for `discount / avoid` where it appears as action-ceiling
  vocabulary instead of C2 risk-weighting language.
- Required trace fields in future read artifacts, if a schema exists:
  verdict, persistence basis, ceiling verb, cap reasons, signals used, and
  counterfactual.

Judgment-only:

- Whether costly behavior is gradeable.
- Whether venue origins are effectively independent.
- Whether evidence discriminates between durable, transient, and manufactured.
- Whether an ambiguous caveat is cap, discount, or neutral.
- Whether persistence has actually held past the trigger.
- Whether buyer behavior is pull rather than praise.
- Whether a satellite's vertical tell is strong enough to matter.

## Propagation Result

Applied in this lane after owner follow-up:

- `orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md`:
  manufactured-demand read action parenthetical changed from `discount / avoid`
  to `avoid`.
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`:
  manufactured-demand heading changed from `discount / avoid` to `avoid`.
- `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`:
  live target-selection wording changed from `suspected hollow or manufactured
  demand` to `suspected transient or manufactured demand`.
- `orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md`:
  live target-selection wording changed from `suspected hollow or manufactured
  demand` to `suspected transient or manufactured demand`, and the first-proof
  buyer-facing answer now uses `real-but-short-window` instead of internal-only
  `transient`.
- `orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md`:
  `forecast_records.horizon` renamed to `forecast_window` after inspection
  showed the field belongs to forecast records, not the C3 action-ceiling
  horizon removed by the C3 contract.

Remaining inspect-before-patching item:

- `orca/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md`:
  `hollow` usages are in manufactured-demand integrity design language outside
  the settlement's required read pack. They need a separate source-loaded pass
  before mechanical replacement because some may distinguish manufactured
  demand subtypes.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Demand-read machinery settlement confirms the current two-axis demand-state
    model, keeps internal `transient demand` as canonical, binds buyer-facing
    `real-but-short-window demand` / `short-window demand` as the preferred
    external label, rejects `trendy`, confirms the seven-verb action vocabulary,
    and records C0-C4, C2/C3, monitoring, proof, and patch boundaries without
    authorizing implementation or capture work.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_settlement_v0.md
    - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
    - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
    - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
    - orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
  downstream_surfaces_checked:
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
    - orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
    - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
    - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    - orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
    - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    - orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
    - orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
    - orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md
    - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md
      reason: >
        Outside the required read pack for this settlement; its `hollow` usages
        appear in manufactured-demand integrity design and need a separate
        source-loaded pass to preserve subtype distinctions.
  stale_language_search: >
    rg -n -i "act \| phase|phase \||narrow, hold|defend\}|long-horizon|short-horizon|horizon:|commit \| move|Excluded .* Watch|durable vs hollow|durable-vs-hollow|trendy|trendiness"
    docs/decisions/orca_product_thesis_consumer_demand_v0.md
    orca/product/spines/foundation/demand_read_taxonomy/orca_demand_read_taxonomy_v0.md
    orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md
    orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md
    orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md
    orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
    orca/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md
    orca/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md
    orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
  stale_language_search_result: >
    Executed 2026-06-22 in branch codex/demand-read-machinery-settlement-prompt
    before and after propagation. Pre-propagation live hits were
    `discount / avoid` in taxonomy + scan-core, `suspected hollow` in
    buyer-proof + offer, and `forecast_records.horizon` in the fragrance
    skeleton. Those were patched in this lane. Remaining hits are preserved
    history/retirement text, C2 risk-weighting `discount` language, C3
    supersession text, and this settlement's own rejected-term / propagation
    evidence.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality proof
    - not implementation authorization
    - not capture authorization
    - not a scoring engine
```

## Next Authorized Action

After this propagation pass, the next authorized action is owner review of the
updated draft PR or a separate source-loaded pass on manufactured-demand
integrity wording if that surface should also retire `hollow`. No runtime,
capture, automation, dashboard, source-system, scheduler, database, API, or
scoring work follows from this artifact.

## Non-Claims

- Not validation.
- Not buyer proof.
- Not willingness-to-pay proof.
- Not judgment-quality proof.
- Not product readiness.
- Not feature readiness.
- Not implementation readiness.
- Not commercial readiness.
- Not capture authorization.
- Not runtime feasibility.
- Not source-system feasibility.
- Not dashboard, feed, or monitoring-service authorization.
- Not a scoring engine.
