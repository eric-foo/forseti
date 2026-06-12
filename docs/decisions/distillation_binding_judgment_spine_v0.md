# Distillation Binding — Judgment Spine Harness (prepare-only draft)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: per-spine distillation binding for the Judgment Spine harness (gates JSG-01..JSG-10: probe, isolation, sealed output, scoring, calibration)
use_when:
  - Distilling a Judgment Spine lesson into a carried rule.
  - Reasoning about how a probe/isolation/gate outcome should route or cap a claim.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
```

**Status: PREPARE-ONLY DRAFT** (see the index). Distills recorded Judgment Spine outcomes. **Reconcile
against the live conductor + gate ownership map** before any real binding — that lane is active and
carries gates beyond these cells. Reads recorded outcomes; edits no Judgment Spine file; makes no
proof, fixture-admission, scoring, blind-use, or judgment-quality claim.

## Harness bound

The agent running or planning a case through the Judgment Spine gates JSG-01…JSG-10 (source identity
/ pre-decision status → packet freeze → no-tools isolation → memorization probe → sealed output →
scoring → reveal/calibration → classification → closeout). Decision nodes are the gates.

## Pole / key finding

**Actor-carried with gate scaffolding.** The gates are structurally named and the conductor halts on
`indeterminate_until_authored`, but the load-bearing decisions (how to route a failed probe, whether
to carry an isolation caveat, whether a by-hand field is gate-clearing) are judgment with no
deterministic check. One partial substrate exists (the band scorer hardcodes
`memorization_probe_result="not_run"`), which is why the by-hand cap is partly code-held.

## A1 — outcome → cell pairs (real, cited)

### GUARD probe-gate-no-promote  (actor-carried)
- decision_node: `node:memorization-probe-gate`
- `GUARD probe-gate-no-promote: WHEN no selected target family clears the memorization-probe gate → record the blocker and withhold blind-use / fixture-admission → UNLESS a family clears with verified isolation.`
- outcome_class: a failed/blocked probe gets read as advanceable instead of a hard blocker on stronger claims
- causal_miss: missing distinction — access-blocked or unproven-isolation is `not_cleared`, not a pass
- verification: under-case (no family cleared) → blind-use/fixture-admission withheld; over-edge (a cleared family with proven isolation) → may proceed
- substrate: actor-carried gate-outcome decision (partial: scorer's hardcoded `not_run` blocks an automatic proof claim)
- PROV: `docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md:83` "No selected target family cleared the Daimler memorization-probe gate." tier: probed (recorded gate run). date 2026-06.

### GUARD isolation-caveat-propagate  (actor-carried)
- decision_node: `node:gate-outcome-routing`
- `GUARD isolation-caveat-propagate: WHEN a probe result is recorded with unverified tool-isolation → carry the isolation caveat forward into the gate-outcome decision and the closeout → UNLESS isolation was structurally verified.`
- outcome_class: the gate-outcome decision drops the isolation caveat, so downstream consumers see an unqualified `failed_memorization_probe` with no signal that isolation was unverified
- causal_miss: missing trigger — provenance of *how* an isolation status was obtained must route to closeout
- verification: under-case (unverified isolation) → caveat present in gate outcome + closeout; over-edge (verified isolation) → no caveat needed
- substrate: actor-carried; fire-log: none (no code check blocks an uncaveated label)
- PROV: `docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md:391` "Gate outcome decision carries no isolation caveat. Downstream consumers see [an unqualified label]" (finding TI-05). tier: probed (review finding). date 2026-06.

### GUARD by-hand-not-self-cert  (actor-carried; PARTIAL)
- decision_node: `node:no-tools-isolation-provenance`
- `GUARD by-hand-not-self-cert: WHEN isolation_result is a hand-typed proven with no authorized auditable live-execution provenance → treat it as indeterminate and cap the run at product-learning → UNLESS an authorized runner emits the provenance.`
- outcome_class: a by-hand `isolation_result == proven` is treated as gate-clearing though it cannot bind auditable provenance
- causal_miss: missing distinction — self-asserted execution provenance is not self-certifying (EP-29 lineage)
- verification: under-case (hand-typed proven) → caps at product-learning; over-edge (runner-emitted provenance) → may lift the cap
- substrate: PARTIAL — the band scorer hardcodes `memorization_probe_result="not_run"` (code-held); truth of any hand-typed field stays resident
- PROV: `docs/product/judgment_quality_promotion_operating_model_v0.md:307` "By-hand execution cannot bind the authorized, auditable live-execution provenance..." tier: accepted-orca-gate. date 2026-06.

## A2 — core size / budget

Mostly actor-carried, so these cells compete for the budget (one partial is code-held). Each is
`silent-wrong-output`-class (a wrong claim-tier promotion is a silent defensibility loss), so each is
**prune-exempt from frequency-only retirement** — low firing frequency is the steady state of a
working rare-but-catastrophic gate cell. Budget model-dependent; not fixed here.

## A3 — spine / decision nodes

`node:source-identity-finalization` (JSG-01) · `node:packet-freeze` · `node:no-tools-isolation-provenance`
(JSG-04) · `node:memorization-probe-gate` (JSG-05) · `node:gate-outcome-routing` · `node:sealed-output`
· `node:scoring` · `node:reveal-calibration` (JSG-08) · `node:closeout`. Cells index by `decision_node`.

## A4 — slots filled

- **intervention-type set** (closed; owner-extensible): `GUARD`, `GATE-OUTCOME`, `ESCALATION` (blocker), `SOURCE-RULE`.
- **verification substrate**: the conductor's `indeterminate_until_authored` halt + the band scorer's hardcoded `not_run`; otherwise human review of gate-outcome decisions.
- **fire-log capability**: MODERATE — gate outcomes are recorded per run (the conductor names blockers and halts), but there is no deterministic pass/fail engine, so telemetry comes from run records; **complied-but-inert** is the live risk (a gate nominally satisfied without the action changing).
- **tier enum**: {accepted-orca-gate, probed, asserted}; recorded cells are probed / accepted-orca-gate.
- **review window**: owner sets (per case run / gate-map change).
- **owner map**: the Judgment Spine owner (conductor + gate ownership map).

## Secondary finding

`VERIFY FIRING` earns its keep here: a gate can be present and verbally satisfied (the conductor
labels `ACT/UNDER`) while the actual claim-tier outcome does not change — a textbook
present-≠-firing surface. This spine is the natural home for an output-level firing audit if one is
ever built (doctrine §2 f-iii, owner-gated).

## Scaffold (no cell invented)

JSG-01 source-identity finalization is `indeterminate_until_authored` (the cross-family
Judgment-authority finalizer is unstaffed). That is a recorded **blocker**, not an outcome where an
agent took a wrong action, so it is named as a scaffold slot, not distilled into a cell.

## Non-claims

Prepare-only; edits no Judgment Spine file; not proof, readiness, validation, scoring,
fixture-admission, blind-use, or judgment-quality evidence; placement is not authority.
```
