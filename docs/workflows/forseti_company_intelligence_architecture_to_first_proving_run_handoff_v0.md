# Forseti Company-Intelligence Architecture to First Proving Run — Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Transfers the accepted decision-first company-intelligence information
  architecture into a fresh lane that will select and frame the first proving
  decision before commissioning research.
use_when:
  - Continuing after the company-intelligence information architecture was accepted.
  - Selecting the first beauty decision-specific proving run.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_company_intelligence_information_architecture_v0.md
  - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
  - forseti/product/satellites/beauty/beauty_decision_adjudication_product_profile_v0.md
stale_if:
  - The owner changes the decision-first architecture or selects a proving decision elsewhere.
  - Current product, beauty, CSB, Scanning, or Company Surface authority changes materially.
```

## Load Contract

- `packet_version`: 0
- `mode`: lean
- `created_at`: 2026-07-16 Asia/Singapore
- `authority_status`: continuation packet only; confirm every load-bearing claim against the named controlling source
- `workspace`: `C:\Users\vmon7\Desktop\projects\orca`
- `authoring_worktree`: `C:\tmp\forseti-company-intelligence-information-architecture`
- `handoff_path`: `docs/workflows/forseti_company_intelligence_architecture_to_first_proving_run_handoff_v0.md`
- `expected_branch`: `codex/company-intelligence-outcome-contribution-handoff`
- `expected_head`: the immutable couriered commit containing this packet; verify from the courier rather than substituting the source baseline
- `source_baseline`: `origin/main` observed at `e300f2c96b1e21c5ba0940be1d76cad9f8cdd180` before this refresh
- `load_rule`: confirm-don't-trust; reread current authority and classify drift before making strict or actionable claims

## Goal Handoff

- `long_term_goal`: Establish which company information materially improves a consequential beauty-company decision and build reusable learning from the decision trace and later reveal.
- `anchor_goal`: Select and bind the first decision-specific proving run under the accepted company-intelligence information architecture.
- `success_signal`: One company, decision, owner proxy, deadline/cutoff, smallest-complete evidence world, paid-access posture, proxy ceilings, hold condition, and reveal path are accepted before research begins.

## Active Objective

Choose the first beauty decision family and proving case. Produce the Decision Frame and atomic information-requirements plan only. Stop for owner acceptance before commissioning CSB, Scanning, Capture, or external research.

## Open Decision

Which beauty decision gives Forseti the strongest honest first same-decision test?

Candidate families remain non-ranked until compared:

- positioning or claims;
- channel or retailer entry;
- launch intervention or inventory;
- competitive response; or
- another decision that satisfies the current product admission contract.

Compare no more than three candidates on:

1. named action, owner proxy, deadline, and consequence;
2. whether public or paid web evidence can establish a useful external baseline;
3. decisive internal facts and whether their absence causes a hold;
4. observable later action or outcome;
5. leakage-resistant cutoff/reveal feasibility;
6. repeated-work potential without inventing a monitoring product; and
7. an evidence path that distinguishes input use, plausible outcome contribution, and causal magnitude.

Recommend one or return `NO_PROVING_DECISION_CLEARS`.

## Outcome-Contribution Evidence Rule

Knowing that a company used an input makes that input more decision-relevant than a generic public clue. It does **not** establish that the input had a higher-than-normal effect on the final outcome.

Keep three claim levels separate:

1. `INPUT_USE_ESTABLISHED`: contemporaneous evidence shows the company used the information in the decision.
2. `MATERIAL_CONTRIBUTION_SUPPORTED`: time-ordered evidence supports the inference that the input materially helped or hurt the outcome after plausible alternative drivers and counterevidence are considered.
3. `CAUSAL_MAGNITUDE_ESTABLISHED`: a credible counterfactual or equivalent design supports how much outcome change the input caused. This will often remain unavailable.

The proving plan should seek the strongest feasible support for level 2 without pretending level 3 is always obtainable. Depending on the decision, useful support may include pre-decision prevalence and specificity of the input, whether the resulting action actually implemented it, adoption by the intended segment, sell-through or conversion against an appropriate baseline, repeat behavior, substitution, price response, and contemporaneous company attribution. It must also test alternative explanations such as distribution, promotion, creator spend, novelty, availability, seasonality, brand strength, or unrelated portfolio effects.

## Drift Guard

- Do not design a generic company report, data product, monitoring offer, GTM motion, buyer pitch, or price.
- Do not assume demand durability is the first module.
- Do not rank facts globally; rank them relative to the named decision.
- Do not treat Reddit, reviews, paid databases, or any other source as a fact.
- Do not treat paid evidence as inherently stronger than open evidence.
- Do not replace a decisive unavailable fact with a proxy.
- Do not infer above-normal outcome impact merely because an input entered the decision.
- Do not demand experimental causal proof when a bounded material-contribution claim is the strongest feasible ceiling; preserve that ceiling explicitly.
- Do not implement or mutate Company Surface.
- Do not run research before the owner accepts the Decision Frame and smallest-complete information requirements.

## Exact Next Authorized Action

1. Re-read `AGENTS.md`, the overlay front door and source-loading rules, this packet, the accepted architecture, current product thesis, beauty profile, and Core product contract.
2. Confirm current CSB and Scanning boundaries only as needed to ensure the proposed plan is commissionable.
3. Return one load outcome: `REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`, `BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.
4. After source readiness, present at most three candidate proving decisions on the seven comparison criteria above.
5. Recommend one candidate and write its proposed Decision Frame plus atomic information-requirements register, including open/paid/internal/unavailable access classes, rights needs, proxy ceilings, missing behavior, reveal path, and the evidence needed to distinguish input use from material outcome contribution.
6. Stop for owner adjudication. Do not commission or execute research.

## Forseti Prompt Preflight

1. `output mode`: chat-only.
2. `template kind`: handoff.
3. `edit permission / targets / branch`: read-only decision framing; no repo or external-system writes.
4. `reviews`: no review verdict or patch queue.
5. `doctrine change`: none authorized; proposed decision selection remains for owner sign-off.
6. `destinations`: receiving task chat; no durable output unless the owner asks.

## Confirm-Don't-Trust Checklist

1. Resolve the couriered commit and confirm this packet and the architecture record exist at their named paths.
2. Confirm current `origin/main`, branch/ref, and clean source state.
3. Reread the architecture rather than relying on this summary.
4. Reread the current product thesis, beauty profile, and Core product contract; do not reactivate superseded buyer or GTM bindings.
5. Check whether current CSB, Scanning, or Company Surface boundaries changed after the recorded baseline.
6. If a load-bearing source changed, re-derive the affected conclusion and return the appropriate load outcome.

## Do Not Forget

First decide what decision is being improved. Then identify the smallest complete set of facts that could change it. Only after that should Forseti decide where to search, what paid access is worth buying, and whether research can support an action or must return a hold.