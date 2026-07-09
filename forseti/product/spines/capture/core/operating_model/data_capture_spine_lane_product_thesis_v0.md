# Data Capture Spine Lane Product Thesis v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Lane-specific product thesis for Orca's Data Capture Spine, using the patched Data Capture Harness operating-model architecture v2 as the operating-model basis.
use_when:
  - Checking what Data Capture Spine is meant to accomplish inside Orca.
  - Preparing pressure-test commissioning planning for the Data Capture Harness.
  - Guarding Data Capture work against source-system, ECR, Cleaning, Judgment, dashboard, proof, or runtime drift.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/decisions/turn_08_product_thesis_v0.md
stale_if:
  - The Data Capture Harness operating-model architecture v2 is rejected, materially patched, or superseded.
  - The Data Capture obligation baseline or obligation contract is amended or superseded.
  - Orca authorizes standing or opportunistic corpus capture inside Data Capture Spine.
  - An accepted ECR architecture changes the categorical handoff boundary.
```

## Status

Status: `DATA_CAPTURE_SPINE_LANE_THESIS_V0`.

This artifact states the product thesis for the Data Capture Spine lane only. It does not restate the whole Orca product thesis, replace the buyer proof packet, accept pressure-test execution, design ECR, design Cleaning, design Judgment, or authorize runtime/tooling/implementation.

Architecture basis: patched `docs/product/data_capture_harness_operating_model_architecture_v2.md`, including the independent-review patches for `capture_closure_blocker` resolution authority and pressure-test classification of v2 primitives.

Strict status boundary: this thesis treats v2 as the owner-directed operating-model basis for this lane. It does not by itself prove validation, hardening, product readiness, source-of-truth promotion beyond named decisions, buyer proof, repeatability, runtime feasibility, or implementation authority.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S2/S3 Data Capture Spine lane thesis pack
  edit_permission: docs-write for this product artifact only
  target_scope:
    - docs/product/data_capture_spine_lane_product_thesis_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_harness_operating_model_architecture_v2.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
```

Compact source ledger:

| Source | Why read | Claim supported | Status note |
| --- | --- | --- | --- |
| Current owner instruction | Authorized patching independent-review findings and writing this lane thesis | Product thesis may use the patched harness architecture as lane basis | user-stated |
| `AGENTS.md` | Orca project authority | Docs-only work allowed; implementation requires explicit bounded authorization | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Orca overlay controls project facts | modified |
| `docs/decisions/turn_08_product_thesis_v0.md` | Overall Orca thesis | Orca turns messy public market signals into clean, source-backed, constrained decision evidence | clean in named-path status |
| `docs/product/orca_offer_hypothesis_v0.md` | Offer and buyer-facing artifact shape | Deck is buyer-facing; memo plus evidence appendix are substrate | untracked/modified status not reclassified here |
| `docs/product/orca_buyer_proof_packet_v0.md` | Buyer proof and non-build boundary | Manual memo plus evidence appendix; no source systems, dashboards, pipelines, source maps, automation, or feature planning | untracked/modified status not reclassified here |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Data Capture Spine product-method blueprint | Capture is the obligation; mode is subordinate; commissioned-capture-only | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | Six discharge states, 16 obligations, forbidden Capture outputs, pressure-test requirement | clean in named-path status |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted obligation baseline | Baseline accepted for bounded harness operating-model architecture only | untracked |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Harness product goal and demotion decision | Manual harness is direction signal only; harness goal is buyer-trustworthy, obligation-discharging, inspectable, layer-disciplined, failure-visible commissioned capture | untracked |
| `docs/product/data_capture_harness_operating_model_architecture_v2.md` | Operating-model architecture basis | Contract-pinned obligation-discharge operating envelope with second-operator capture-visibility check | untracked/modified |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md` | Independent review of v2 | v2 is strongest candidate; F-01/F-02 patched in current v2 | untracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary | Data Capture, ECR, Cleaning, Judgment, Decision Artifact, and Outcome Memory remain separate | clean in named-path status |

Dirty/untracked caveat: this workspace is dirty and many Data Capture artifacts are untracked. This thesis may use them as current owner-directed working product artifacts. It does not convert dirty or untracked sources into validation, readiness, commercial proof, or implementation authority.

## Thesis

Data Capture Spine is Orca's trust-bearing intake layer for public and external signals.

Its job is to turn commissioned, decision-framed source material into an inspectable captured basis that downstream ECR, Cleaning, Judgment, memo, evidence appendix, and executive deck work can use without recollecting source history or trusting source theater.

The lane thesis:

```text
Data Capture Spine is Orca's first candidate durable product advantage: the layer most likely to compound into defensible buyer trust if real commissioned pressure tests show that obligation-visible capture can repeat across source families, operators, and decision frames.
```

The lane is valuable because public signals are not evidence when they are merely found, scraped, summarized, counted, or shown in a deck. They become Orca evidence only when the capture layer makes visible what was commissioned, what source state was observed, what raw observable was preserved, what was partial or blocked, what failed, what remained unknown, what cutoff/archive posture applies, and what downstream layers must not infer yet.

## Product Role Inside Orca

Overall Orca turns messy, noisy, contradictory public market signals into clean, source-backed, constrained decision evidence for high-stakes decisions.

Data Capture Spine owns the first conversion:

```text
messy public/external signal
-> commissioned captured signal with visible obligations, limits, source posture, optional mechanical source projection, and handoff state
```

It does not own the later conversions:

```text
captured signal
-> Evidence Candidate Record
-> Cleaning
-> Judgment
-> memo plus evidence appendix
-> executive decision deck
```

The buyer sees value downstream as a memo, evidence appendix, and executive deck. Data Capture Spine is mostly invisible to the buyer, but it is what prevents those buyer-facing artifacts from becoming presentation theater. When a trust-objecting buyer asks "where did this come from, what could be wrong with it, and how do you know you did not lose context," Data Capture Spine is the layer that makes the answer possible.

## Harness Architecture As Mechanism

The Data Capture Harness is the operating envelope for this lane.

Current operating-model basis:

```text
Contract-pinned obligation-discharge operating envelope
with second-operator capture-visibility check
```

This architecture turns the lane thesis into operating commitments:

- Every capture is commissioned by a Decision Frame.
- Every core obligation is explicitly discharged as `met`, `partial`, `blocked`, `unavailable_by_source`, `not_applicable`, or `not_attempted`.
- Silent omission is forbidden.
- Capture mode is disclosed, but mode never defines evidence quality by itself.
- Raw observable, source identity, timing, cutoff posture, archive/history posture, related context, failure state, and re-capture relationship remain visible where applicable and knowable.
- When raw source format is transport-heavy, a Data Capture Projection Packet may expose mechanical source-projected rows while preserving raw source custody and projection warnings.
- Mixed source states are preserved per slice when rollup would hide differences.
- The second operator records capture-owned blockers and visible limitations, but does not approve, refuse, validate, score, or decide downstream use.
- Capture hands off categorically to ECR without defining ECR fields.

The harness architecture matters because the obligation contract alone can remain a paper standard. The harness makes the standard operational across operators, sessions, interruptions, agent assistance, and source families without turning it into runtime tooling.

## What Data Capture Spine Must Maximize

The lane must maximize properties that compound downstream decision quality:

- Commission discipline: no free-floating capture, standing corpus intake, or source collection without a Decision Frame.
- Obligation visibility: every obligation has a visible state, including blocked, partial, unavailable, and not attempted.
- Raw observable preservation: source language, modality, layout, bundle structure, and related context remain inspectable when they carry meaning.
- Failure visibility: failed access, archive failure, fallback use, source limits, unknowns, and not-attempted routes are explicit.
- Cutoff and archive posture: source state is bounded against decision timing, including post-window, mixed, archive-only, deleted, edited, cached, fallback, migrated, and prior-window conditions.
- Multi-operator repeatability: another operator can inspect what was done and why without relying on the first operator's memory.
- Layer discipline: Capture records visible facts and limits; downstream layers decide cleaning, credibility, discounting, exclusion, signal use, Decision Strength, and Action Ceiling.
- Projection discipline: source-envelope noise may be removed from a working view, but evidence rows are not removed because they look low-value, low-score, repetitive, deleted, or unhelpful.
- Buyer trust answerability: the downstream artifact can answer source-trust objections without defensive narration or source-volume theater.

## What Data Capture Spine Must Not Become

Data Capture Spine must not become:

- a source map;
- a source inventory;
- a source-volume engine;
- a standing corpus intake lane;
- a scraper, API, dashboard, archive tool, storage system, or runtime plan;
- an Evidence Candidate Record schema;
- a Cleaning transformation system;
- a Judgment rubric;
- a source-quality scoring system;
- a buyer-proof artifact by itself;
- an adversarial defense layer;
- a presentation-theater enabler;
- a permanent human research checklist.

The lane may expose pressure for these later decisions. It must not absorb them.

> **Standing/opportunistic corpus capture now has an obligation home (2026-06-15).**
> The stale_if "Orca authorizes standing or opportunistic corpus capture inside
> Data Capture Spine" has fired: standing/opportunistic corpus capture is now
> governed by the owner-ratified Corpus Intake (standing-capture) obligation
> contract,
> `forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md`
> (the standing sibling of the v0 commissioned obligation contract). This lane's
> commissioned-only discipline above is unchanged; standing capture remains "not
> ECR-ready evidence until rebound or recaptured under a Decision Frame," now
> governed by that contract rather than absorbed here.

## Product Bet

The product bet for this lane is:

```text
If Orca can repeatedly capture public/external signals under a commissioned, obligation-visible, failure-visible operating model, then downstream memo, appendix, and deck work can be both more trusted and more constrained than generic research or dashboard outputs.
```

This is the first place Orca's product moat can collapse or compound.

It collapses if Capture hides source limits, loses raw context, collapses mixed states, lets agents pre-filter relevance, or starts deciding credibility and usefulness.

It compounds if Capture makes source limits cheap to inspect, makes failure non-embarrassing and visible, preserves raw source context, exposes mechanical projections without evidence-row filtering, and gives downstream layers a clean categorical handoff.

## Data Capture Spine Success Signal

This lane is succeeding when a commissioned capture can be inspected by a second operator and later by downstream layers, and the following are true:

- The Decision Frame is visible.
- The source boundary is visible.
- The capture mode and material mode changes are visible.
- Each core obligation has one of the six discharge states.
- `partial`, `blocked`, `unavailable_by_source`, and `not_attempted` are as visible as `met`.
- Raw observable and source-visible context are preserved enough that ECR can reconstruct what the source was claiming without recollecting source history.
- When a mechanical source projection is used, raw source, source-projected rows, and projection receipt warnings remain traceable as one Data Capture Projection Packet.
- Failure and fallback paths are visible.
- Per-slice posture is preserved when source states differ.
- The handoff to ECR is categorical, not schema-designed.
- No Capture output contains credibility, exclusion, discounting, Signal Use, Decision Strength, Action Ceiling, Cleaning transformation, ECR field architecture, source-quality score, source map, or runtime implementation plan.

This is not validation. It is the product-method success signal the pressure tests should inspect.

## Pressure-Test Thesis

The next proof of this lane is not building software. It is pressure-testing the patched harness architecture against 3-5 real commissioned captures.

The pressure tests should learn whether:

- the obligation states are usable without becoming checklist theater;
- `capture_closure_blocker` and `visible_capture_limitation` preserve capture facts without creating reviewer pass/fail culture;
- the five-role model is too heavy, too light, or correct;
- source-family satellite guidance can stay satellite;
- per-slice archive/history and recapture posture survives real source mess;
- downstream ECR, Cleaning, and Judgment can proceed without recollecting source history;
- operators can run the model without drifting into source maps, runtime design, or bespoke consulting labor.

Pressure-test evidence may patch the architecture or obligation contract later. It must not be treated as validation merely because no blocker appears.

## Core/Satellite Boundary

Core Data Capture Spine owns market-agnostic capture accountability:

- commissioned frame;
- boundary compliance;
- capture-event provenance;
- capture mode and mode changes;
- raw observable;
- source identity and actor context;
- decomposed timing and cutoff posture;
- archive/history and access posture;
- related context;
- bundled-offer structure;
- failure visibility;
- re-capture semantics;
- categorical handoff sufficiency.

Satellites own source-family and decision-family adaptation:

- threaded forum context conventions;
- review-surface recency, moderation, incentive, and sorting conventions;
- changelog, docs, pricing, API, policy, cache, and versioning conventions;
- bundled-offer and multi-term proposal conventions;
- multimodal and dynamic-page handling notes;
- per-family human-led defaults;
- per-family source feasibility and blind spots.

Satellite guidance pressures core only through the Source-Family Promotion Rule: cross-family evidence across at least two non-overlapping families, or owner sign-off for one specific invariant claim.

## Downstream Promise

If this lane works, Orca downstream layers should receive captured signals with enough context to proceed without recollecting source history.

That enables:

- ECR to receipt captured signal context without becoming source discovery.
- Cleaning to verify and normalize raw-to-projected-to-cleaned traceability without losing raw source context.
- Judgment to decide credibility, source integrity, discounting, exclusion, Signal Use, Decision Strength, and Action Ceiling without Capture having pre-decided those effects.
- The memo and evidence appendix to stay inspectable.
- The executive deck to stay derived from evidence rather than leading it.

The downstream promise is not "capture proves the decision." It is "capture makes the decision evidence inspectable and bounded enough for downstream judgment to work."

## Open Questions

- Which 3-5 commissioned captures should pressure-test this operating model?
- Which source families must be represented in the pressure-test batch?
- Whether the five-role model is too heavy for v0 pressure tests.
- Whether `capture_closure_blocker` and `visible_capture_limitation` should survive as permanent vocabulary.
- What minimal artifact form exposes obligation states without becoming ECR schema or runtime design.
- Which source families require archive attempts rather than posture-only recording.
- Where Snapshot Integrity Class belongs: Data Capture, ECR, or later Judgment/ECR consolidation.
- When, if ever, runtime/source-system planning becomes authorized.

## Next Authorized Step

The next appropriate step is a bounded pressure-test commissioning plan for Data Capture Spine:

- select 3-5 real commissioned captures;
- name source-family coverage targets;
- name operator categories without staffing or training curriculum;
- pin the obligation contract and patched harness architecture version;
- define the minimal non-runtime artifact form for exposing obligation states;
- preserve `capture_closure_blocker` as a capture-owned visible condition, not reviewer pass/fail;
- preserve all non-claims.

This thesis does not authorize pressure-test execution. It authorizes only using the patched architecture as the product basis for later bounded planning if the owner chooses that route.

## Non-Claims

This artifact does not claim:

- buyer validation;
- willingness to pay;
- repeatable demand;
- commercial readiness;
- product readiness;
- feature readiness;
- implementation readiness;
- Data Capture Spine validation;
- Data Capture Spine completion;
- harness validation;
- pressure-test discharge;
- ECR readiness or design;
- Cleaning readiness or design;
- Judgment readiness or design;
- source-system feasibility;
- data rights;
- runtime feasibility;
- source-of-truth promotion beyond named accepted decisions;
- authorization for pressure-test execution, runtime, tooling, source systems, source maps, dashboards, scrapers, APIs, storage, automation, schemas, tests, packages, deployment, commits, pushes, PRs, buyer-facing decks, or proof runs.

The thesis is a lane-specific product stance and routing artifact, not proof that the lane works.
