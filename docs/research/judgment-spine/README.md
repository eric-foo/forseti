# Judgment Spine v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Parent contract for Orca's case-based judgment-learning spine.
use_when:
  - Choosing whether a public case is suitable for consultant-grade judgment learning.
  - Adding, indexing, or reviewing Judgment Spine cases.
  - Preserving cross-case consulting lessons without creating a skill, model-training dataset, or product feature.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_thesis_v0.md
  - docs/research/judgment-spine/manifest_v0.md
  - docs/research/judgment-spine/harness/README.md
  - docs/prompts/deep-thinking/orca_judgment_spine_case_learning_preservation_prompt_v0.md
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S1 plus target Judgment Spine artifacts
  edit_permission: docs-write
  target_scope: Create the Judgment Spine parent contract, manifest, Milwaukee case index, and navigation pointer.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Purpose

The Judgment Spine is Orca's case-law layer for sharpening consultant-grade decision judgment.

It captures how a decision was framed, what a blind judgment recommended before reveal, what the owner saw differently, what the revealed action or outcome clarified, and which lessons deserve reuse.

This is not model fine-tuning, a data pipeline, a software feature, a miner, or a product-readiness claim. The scarce asset is case-law-quality judgment: specific corrections on real decisions, preserved in a form that can sharpen both the operator's mind and later AI behavior.

## Thesis

The parent thesis lives at `docs/research/judgment-spine/judgment_spine_thesis_v0.md`.

Use it as the north-star goal before Judgment Spine architecture, CA setup, harness changes, case-learning work, or lesson-promotion decisions.

The thesis operating contract lives at `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`.

Open it after the thesis when a future lane needs to consume, protect, or apply the thesis without drifting into implementation, proof, product-readiness, or adjacent-layer work.

## Judgment Harness Area

The Judgment Harness specs live under `docs/research/judgment-spine/harness/`.

`docs/research/judgment-spine/harness/v0_14/` is the working v0.14 Judgment Harness spec. It governs harness schemas, scoring, runner contracts, case construction, memorization probe behavior, and failure logging for that spec version.

Adjacent context may live under `docs/research/judgment-spine/harness/adjacent-context/`, but side context does not supersede the v0.14 spec and does not make Data Capture Spine, Evidence Candidate Record, or Cleaning Spine part of the Judgment Harness.

## Case Unit

A complete Judgment Spine case should eventually contain:

- case frame and decision question
- cutoff timestamp
- clean pre-cutoff source packet or participant packet
- spoiler safety receipt
- sealed blind judgment or judgments
- owner critique or owner judgment
- reveal readout or outcome calibration
- distilled reusable lessons
- optional improved rewrite after reveal

Partial cases are allowed only when the missing pieces are named directly in the case index and manifest.

## Learnability Tiers

Use tiers to judge how much a case can sharpen decision-making and consulting edge, not how famous the client or firm is.

| Tier | Meaning | Use |
| --- | --- | --- |
| Tier 0 | Decision-grade case with a real owner, clear cutoff, material tradeoff, enough pre-cutoff evidence, revealed action or outcome, and lessons that expose judgment misses or sharpen executive advice. | Full blind backtest, owner critique, reveal calibration, reusable lesson extraction. |
| Tier 1 | Useful but incomplete case with a real decision and some revealed outcome, but weaker source depth, thinner economics, weaker owner visibility, or limited recommendation logic. | Focused judgment drill or partial lesson extraction, with explicit gaps. |
| Tier 2 | Low-leverage or auxiliary material: anonymized, marketing-heavy, thought-leadership-like, source-thin, outcome-light, or too generic to support a sealed decision test. | Reject-pattern map, source-hunting lead, or background only. Do not treat as proof. |

A consulting-firm case page is not Tier 0 by default. It becomes Tier 0 only if public surrounding records make the decision reconstructable before reveal and the case can teach a specific decision mechanism.

## Case Loop

1. Select a candidate case for learnability, not brand prestige.
2. Define the decision owner, decision question, and cutoff.
3. Build or identify a clean pre-cutoff packet.
4. Seal a blind judgment before consulting recommendations, outcomes, or post-cutoff facts are exposed.
5. Capture owner critique or owner judgment.
6. Reveal the actual action, recommendation, or outcome.
7. Calibrate what the blind judgment got right, missed, or overfit.
8. Distill reusable consulting lessons.
9. Promote only lessons that survive transfer checks.
10. Optionally create an improved memo or deck after the learning record is sealed.

## Promotion Rules

A lesson may be promoted toward Orca's reusable consulting playbook only when it satisfies at least one strong condition and does not overfit the source case:

- appears across multiple cases
- strongly explains one major revealed outcome
- fixes a repeated AI or operator failure mode
- improves owner blind judgment in a later case
- names where the rule should not apply

Single-case lessons remain provisional unless later cases show transfer.

## Spoiler Safety

Before a blind judgment is sealed, do not expose actual decisions, consulting recommendations, implementation actions, post-cutoff facts, outcomes, result quality, or leaking source titles, snippets, or URLs.

If leakage occurs before sealing, the participant-facing packet is contaminated and must be rebuilt from clean pre-cutoff sources before blind use.

After reveal, index files may identify the revealed state, but they must still label the spoiler status so future agents do not accidentally reuse revealed material as blind input.

## Non-Claims

- No buyer validation.
- No willingness-to-pay proof.
- No repeatability proof.
- No product readiness.
- No feature readiness.
- No implementation readiness.
- No commercial readiness.
- No model-training readiness.
- No fine-tuning readiness.
- No data-center, GPU, scraping, automation, or miner need proven.
