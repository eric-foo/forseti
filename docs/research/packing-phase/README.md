# Forseti Packing Phase

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Initial boundary note for the Packing Phase between Cleaning outputs and Judgment Harness inputs.
use_when:
  - Deciding whether cleaned evidence is ready to become a judgment-facing packet or harness fixture.
  - Separating Cleaning responsibilities from Judgment Harness responsibilities.
  - Checking whether a packet, evidence registry, or leakage boundary is being produced by the right layer.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_thesis_v0.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
```

The Packing Phase turns cleaned, source-backed evidence material into judgment-ready case artifacts.

It sits between Cleaning and Judgment Harness work:

```text
Data Capture
-> Evidence Candidate Record
-> Cleaning / normalization / dedupe / source integrity
-> Packing Phase / decision packet construction
-> Judgment Harness case preparation
-> blind judgment, scoring, and failure logging
```

## Purpose

The Packing Phase exists because cleaned evidence and judgment-ready packets are different objects.

Cleaning can establish that material has been normalized, deduped, translated, source-backed, and traced. It should not decide what a blind participant sees, which uncertainties matter to the decision, or how facilitator-only material is separated from participant-facing material.

The Packing Phase prepares the case surface that Judgment work can consume without absorbing Data Capture, ECR, or Cleaning responsibilities.

## Owns

The Packing Phase owns draft construction and readiness checks for:

- participant packet shape;
- evidence registry shape;
- source manifest shape;
- known uncertainty and source-gap sections;
- permitted assumptions and forbidden-information notices;
- cutoff and spoiler boundaries;
- participant-facing versus facilitator-only separation;
- leakage notes that must later map into a facilitator ledger;
- unresolved evidence-adapter decisions such as source-visibility gaps.

It may use LLMs as drafting or proposal assistants, but an LLM draft is not a frozen packet, accepted evidence registry, or harness-ready fixture by itself.

## Does Not Own

The Packing Phase does not own:

- source acquisition or preservation obligations;
- raw captured-signal receipt fields;
- normalization, dedupe, translation, or transformation trace;
- source-integrity scoring mechanics;
- frozen facilitator-ledger labels;
- final band-input labels;
- action-band mapping;
- scoring;
- probe execution;
- model runs;
- failure-event logging;
- lesson promotion;
- product-proof claims.

Those remain with their respective layers.

## Judgment Harness Handoff Boundary

Judgment Harness work should consume frozen or explicitly draft-labeled packet artifacts from the Packing Phase.

If provenance, source hashes, retrieval timestamps, cleaning trace, cutoff safety, participant/facilitator separation, or unresolved source gaps are missing, the harness should block or mark the input draft-only. It should not silently repair upstream preparation by acting as Data Capture, Cleaning, or Packing.

## Current Status

```yaml
status: INITIAL_BOUNDARY_NOTE
implementation_authorized: no
runtime_authorized: no
validation_or_readiness_claim: not_proven
```

This README creates a folder and boundary vocabulary only. It does not accept a full Packing Spine, authorize implementation, validate any packet, or make any harness fixture ready for blind use or scoring.
