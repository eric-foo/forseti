# Forseti Moat → Judgment-Quality → ECR Proof-Path Decision Chain v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (decision-chain capture)
scope: >
  Captures the chain of owner decisions and accepted framings linking Forseti's
  end-state moat ambition (Palantir-style lock / McKinsey-style reputation) to the
  judgment-quality evidence gate, the tooled-contestant harness change, the
  middle-rung evidence path, and ECR as critical-path rung-one. Decision-prep for
  owner sign-off; freezes nothing and amends no controlling source.
use_when:
  - Checking what was decided in the moat -> proof-path conversation before building.
  - Sequencing the judgment-quality proof path (middle rung) and the ECR critical path.
  - Preparing the downstream doctrine-change patches this chain implies.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_icp_wedge_pricing_first_v0.md
  - forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  - forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/manifest_v0.md
stale_if:
  - Owner signs off and the chain is promoted into the controlling product/harness sources.
  - The decide-vs-confirm crux test flips the pricing-first / judgment-quality framing.
  - The ECR critical-path mapping supersedes the middle-rung sequencing.
  - The Judgment Spine harness no-tools -> tooled change is formally propagated or rejected.
```

## Status

`DECISION_CHAIN_CAPTURED_PENDING_OWNER_SIGNOFF`. Captures owner decisions and
accepted framings made in conversation on 2026-06-09. It is decision-prep for
sign-off — not an accepted lock, not validation, not build authorization. It
amends no controlling source; the downstream doctrine patches it implies are
separately authorized.

Dirty-state: written on branch `ecr-sp3-timing-deriver-slice1` (an ECR
implementation branch, ahead 14), worktree dirty/untracked. Durable home is the
product lane on `main`; committing or moving there is a separate owner-authorized
step. Strict baseline claims remain not-proven until reconciled.

## The Chain (top to bottom)

### D1 — Moat ambition is downstream of pricing, not a pivot from it [accepted]

Palantir-style vendor lock and McKinsey-style reputation are not a different road
from pricing. Both are earned only after one scarce first deposit: Forseti makes a
real high-stakes call, the call is correct, and the outcome is recorded.

- McKinsey vector = judgment authority + reputation = a calibrated track record of
  correct calls. The posture is adoptable now; the reputation is a lagging,
  evidence-gated asset.
- Palantir vector = outcome-memory / data lock; defensible only if the recorded
  outcomes are calibrated correct calls.
- Both sit at the `judgment_quality` evidence tier.
- Pricing-first stays #1: it is the least-blocked, densest place to earn the first
  deposit. (Least-blocked, not proven.)

### D2 — The crux remains OPEN [not decided — the gating uncertainty]

Does public signal DECIDE a high-stakes call, or merely CONFIRM one after the
fact? Untested. Pricing-first wins by being least-blocked on the evidence, not by
being proven. No buyer has paid. This is the assumption everything downstream
rests on.

### D3 — Judgment-quality is the moat gate, and the spine cannot produce it yet [accepted]

Both moats require `judgment_quality`-tier evidence. Today every run caps at
`product_learning` (conductor Seam 3 by-hand cap): no contestant-execution runner,
`band_scorer` hardcodes `memorization_probe_result="not_run"`, JSG-01 is
`indeterminate` (no ECR field schema), no score-ready fixture. So the moats are
blocked at the evidence-production layer — not merely lagging.

### D4 — Build a standing, memorization-resistant case finder, connected to Core Spine discovery [decided]

The "same old cases" problem is contamination, not boredom: famous cases are
memorized by frontier models, so blind judgment isn't blind. The existing
heavyweight discovery selects FOR fame and was never operationalized or
selected-from; there is no standing finder. Decisions:

- Add an explicit memorization-resistance criterion to case selection (distinct
  from the existing anti-cherry-pick rule).
- Make case-finding a standing capability (build on the existing case-construction
  protocol + the manifest "Selection Rule for Case 2").
- Connect it to the Core Spine heavyweight discovery candidate universe.

### D5 — Harness change: test the tooled pipeline, not a no-tools strawman [decided — doctrine change]

- The pipeline is four quarters: capture -> ECR -> cleaning -> (mini-packing) -> judgment.
- Drop the contestant no-tools execution contract. Test Forseti's tooled pipeline,
  because that is the product. (Doctrine change to JSG-04/05/06 isolation, the
  no-tools contract, and the evidence-ladder judgment-quality definition.)
- Runtime isolation via fresh thread (clean context), not the heavy isolation
  contract. **Load-bearing caveat:** a fresh thread removes conversation leakage,
  NOT training memorization — so the memorization-resistance case criterion (D4)
  AND the wired memorization probe stay required. Drop the no-tools contract; do
  not drop the probe.

### D6 — Evidence path: MIDDLE RUNG [decided]

Contestant runs ECR -> cleaning -> packing -> judgment over a sealed, pre-vetted,
outcome-free source pool (Canoo/Walmart's existing source packet can seed it).
Leakage is controlled by one-time pool curation, not by live-capture
cutoff-cleanliness.

- Rejected for now: Option 1 (frozen-packet-only) — still ECR-blocked for
  judgment-quality, and tests only the back half of the pipeline.
- Named destination, gated: Option 2 (live capture) — the real end-to-end
  product-proof, gated on Data Capture Spine cutoff-cleanliness being proven
  separately in its own lane.
- Accepted tradeoff: attribution is muddier (a bad call could be ECR, cleaning,
  packing, or judgment) — mitigate with a per-quarter checkpoint.

### D7 — ECR is rung one [decided consequence]

The middle rung makes ECR the critical path: judgment-quality is gated on ECR
being up (at least the JSG-01 field schema). The current branch
`ecr-sp3-timing-deriver-slice1` is already that path. The first clean
judgment-quality score reduces to: get ECR up -> resume the paused judgment
behaviorals -> run one obscure sealed-pool case (Canoo/Walmart-seeded) through
ECR -> cleaning -> packing -> judgment -> score, probe wired, fresh thread.

## What Already Exists vs. Missing (verified context)

Exists: the v0.14 harness spec self-certifies "code-ready" (mapping, scorer
formulas, schemas, case-construction protocol, memorization-probe protocol,
no-tools contract — all as written specs); `band_scorer.py` is a real, heavily
exercised deterministic scorer; two draft fixtures (Unity, Canoo/Walmart);
Canoo/Walmart was walked through the full gate sequence by hand (capped at
qualitative learning); case-selection doctrine + several relatively obscure cases
(Milwaukee, Daimler, Canoo/Walmart).

Missing (now reframed by D5/D6): a TOOLED contestant runner (not no-tools);
memorization-probe wiring; a score-ready sealed pool/fixture; ECR up to the JSG-01
bar.

## Open Items (not decided)

- D2 crux (decide-vs-confirm) — untested; the cheap product-learning probe remains
  the gate on any judgment-quality investment.
- Owner of the sealed-pool curation step (a quiet bottleneck).
- What "ECR up enough" precisely means — the architecture-lane critical-path
  mapping (deferred).
- Whether to durably record/commit this chain to the product lane on `main`.
- Status of the earlier "Way 1" product-learning crux probe (still valid as the
  cheap gate) and "Way 2" cap-lift (now reframed around the middle rung + ECR-first).

## Doctrine-Change Propagation (flagged, NOT executed)

```yaml
direction_change_propagation_blocker:
  doctrine_changed: >
    Two coupled direction changes captured here: (product) moat / end-state
    framing + judgment-quality-as-gate + pricing-first-as-first-deposit-path
    (refines existing thesis/wedge; pricing #1 unchanged); and
    (judgment_spine_harness) the no-tools contestant contract is dropped in favor
    of a tooled pipeline + fresh-thread isolation + middle-rung evidence path +
    memorization-resistance case criterion.
  trigger: architecture_doctrine
  related_triggers: [product_doctrine, validation_philosophy]
  blocking_surface: >
    No controlling source amended; the affected surfaces are
    docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md,
    the v0_14 harness JSG-04/05/06 isolation + case-construction + memorization-probe
    protocols, docs/product/judgment_spine_evidence_ladder_architecture_v0.md
    (judgment_quality definition), docs/product/judgment_quality_promotion_operating_model_v0.md
    (by-hand cap framing), and docs/decisions/orca_icp_wedge_pricing_first_v0.md plus the
    product thesis (moat-gate framing).
  attempted_check: captured the chain in this record; no controlling source amended.
  allowed_next_step: >
    Owner-authorized routing to the architecture/implementation lane plus the
    Doctrine Change Propagation Contract; produce the standing case-finder frame
    and the ECR critical-path mapping under that authorization.
  non_claims: [not validation, not readiness, not judgment-quality proof, not buyer proof, not implementation authorization]
```

## Lane Note

This conversation descended from a product-strategy question to harness/ECR
architecture. This record is product-lead decision-CAPTURE only. The middle-rung
and ECR critical-path DESIGN, and any build, are architecture/implementation-lane
work requiring separate explicit authorization.

## Non-Claims

Not validation, willingness-to-pay, buyer proof, judgment-quality proof,
repeatability, product/commercial readiness, ICP-proven, or Core Spine v0
validation. Pricing-first is least-blocked, not proven. This record authorizes no
build (ECR, runner, finder, middle rung, fixture) and amends no controlling
source; each is a separately authorized step. Freezes nothing without explicit
owner sign-off.
