# Distillation Binding — Product-Proof / Buyer-Proof Harness (prepare-only draft)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: per-spine distillation binding for the Orca product-proof / buyer-proof harness (trust state, claim tier, zero-spoiler)
use_when:
  - Distilling a product-proof lesson into a carried rule.
  - Reasoning about buyer skepticism, claim-tier promotion, or participant-packet spoilers.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - .agents/workflow-overlay/product-proof.md
  - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
```

**Status: PREPARE-ONLY DRAFT** (see the index). Orca's **actor-carried (judgment) pole** — the
closest analog to the jb maximize binding: there is **no deterministic substrate**, so every cell
competes for the always-on budget and each owes VERIFY FIRING. Reads recorded outcomes; edits no
overlay or product file; makes no buyer-proof or judgment-quality claim.

## Harness bound

The agent authoring or reviewing Orca product-proof / buyer-proof artifacts (discovery, qualification,
memo, deck, backtest, calibration). Governed actor: the agent. Decision nodes are the trust-state
call, the claim-tier classification, and the participant-packet reveal boundary.

## Pole / key finding

**Pure actor-carried.** Classification (objection vs refusal, which claim tier, pull vs praise) is
judgment with no checkable surface; a keyword scan over spoilers is an explicit **OVER-EDGE** (a
green scan would falsely read as "no leak"). So `VERIFY FIRING` actually bites here, and CONFLICT-
CHECK is a distill-time discipline only.

## A1 — outcome → cell pairs (real, cited)

### GUARD skepticism-not-kill  (actor-carried)
- decision_node: `node:skepticism-classification`
- `GUARD skepticism-not-kill: WHEN a buyer is skeptical but willing to evaluate evidence quality/examples/mechanism → classify trust_objection (proof material), do NOT kill → UNLESS trust_refusal: the buyer says public-signal evidence cannot affect the decision regardless of evidence.`
- outcome_class: initial buyer skepticism is treated as a disqualifier (kill) instead of proof material
- causal_miss: collapsing `trust_objection` (willing to evaluate) into `trust_refusal` (categorical)
- verification: under-case (skeptical-but-willing) → `trust_objection`, proceed; over-edge (categorical refusal) → `trust_refusal`, may kill
- substrate: actor-carried (judgment; no lint)
- PROV: `product-proof.md:69` "Kill criteria must not fire on initial skepticism."; `:39-43` trust_refusal definition. tier: accepted-orca-gate.

### GUARD claim-tier-no-upward-carry  (actor-carried)
- decision_node: `node:claim-tier-classification`
- `GUARD claim-tier-no-upward-carry: WHEN classifying evidence → apply the weakest-cleared-gate; product_learning must NOT carry its claim up to buyer_proof / judgment_quality without the stronger tier's promotion gate → UNLESS that gate's receipt is satisfied.`
- outcome_class: product-learning evidence is reused as buyer-proof / judgment-quality merely because it is persuasive or useful
- causal_miss: missing distinction — lower-tier evidence may inform design but must not carry its claim upward
- verification: under-case (manual advisory output) → caps at `product_learning` / `no_durable_evidence`; over-edge (a completed buyer-proof receipt) → may claim `buyer_proof`
- substrate: actor-carried; PARTIAL — a `closeout_state` co-reference can be schema-checked for presence (not truth)
- PROV: `product-proof.md:114-117` "Lower-tier evidence may inform the design ... but it must not carry its claim upward."; recorded instance `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` (`no_durable_evidence`). tier: accepted-orca-gate.

### GUARD zero-spoiler-rebuild-not-edit  (actor-carried; OVER-EDGE)
- decision_node: `node:participant-packet-reveal`
- `GUARD zero-spoiler-rebuild-not-edit: WHEN spoiler material enters participant-facing text before the blind judgment is sealed → mark the packet contaminated and rebuild from clean pre-cutoff sources; do NOT delete sentences in place → UNLESS the blind judgment is already sealed.`
- outcome_class: a contaminated participant packet is "repaired" by in-place deletion and reused, leaking decision/outcome
- causal_miss: missing boundary — a contaminated packet must be rebuilt, not edited; the contaminated material stays out of the participant path
- verification: under-case (post-cutoff fact in participant text) → contaminated + rebuilt; over-edge (sealed judgment) → reveal allowed
- substrate: actor-carried; **OVER-EDGE** — a keyword leak-scan must never be treated as a clear (EP-28); at most a noisy advisory tripwire
- PROV: `product-proof.md:170-174` "rebuild a clean zero-spoiler packet from pre-cutoff sources and keep the contaminated material out of the participant path."; recorded instances `docs/_inbox/contaminated_method_validation_replay_outputs_2026_05_21*`. tier: accepted-orca-gate.

## A2 — core size / budget

Pure-LLM, so the rule-count budget **binds here** — every cell competes for the always-on budget with
no code-enforcement escape valve. All three are `silent-wrong-output`-class (a wrongly-killed buyer,
an inflated claim tier, a leaked spoiler are silent defensibility losses) → prune-exempt from
frequency-only retirement. Budget model-dependent; not fixed here. One-in / one-out is tighter here.

## A3 — spine / decision nodes

`node:skepticism-classification` · `node:claim-tier-classification` · `node:pull-vs-praise` ·
`node:participant-packet-reveal` · `node:non-claims-closeout`. Cells index by `decision_node`.
(The zero-spoiler cell is the canonical home; the Core-Spine method-validation binding references it
rather than copying.)

## A4 — slots filled

- **intervention-type set** (closed; owner-extensible): `GUARD`, `RUBRIC` (claim-tier ladder), `SOURCE-RULE`.
- **verification substrate**: de-correlated review of proof artifacts; the evidence-ladder claim-tier classification; **no deterministic engine** (the maximize-pole property).
- **fire-log capability**: MODERATE — the assert/withhold of a claim is observable per artifact (does it claim buyer-proof?), but only at the output; **complied-but-inert** is the live risk.
- **tier enum**: {accepted-orca-gate, probed, asserted}.
- **review window**: owner sets (per proof run).
- **owner map**: the product-proof / buyer-proof owner.

## Secondary finding

This is where `VERIFY FIRING` earns its keep: "the rule is in the prompt" is genuinely not "the
agent classified `trust_objection`" — the only signal is the artifact's actual classification and
claim tier. The natural home for an output-level firing audit if one is ever built.

## Scaffold (no cell invented)

The pull-versus-praise gate names a real failure mode (treating praise/curiosity as pull) but no
recorded *instance* of the error was found this pass; it is a slot (codified rule), not distilled as
a recorded-outcome cell until an instance is recorded.

## Non-claims

Prepare-only; edits no overlay or product file; not buyer validation, willingness-to-pay,
repeatability, product/feature/implementation/commercial readiness, or Core-Spine validation;
placement is not authority.
```
