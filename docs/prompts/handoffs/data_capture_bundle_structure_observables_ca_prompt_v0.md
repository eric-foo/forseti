# Data Capture Bundle Structure Observables CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: ca_handoff_prompt
scope: Handoff prompt for deciding whether the Data Capture Spine must preserve bundle structure, concession framing, and packaging-as-signal observables.
use_when:
  - Running a Data Capture CA follow-up after the Milwaukee WRS tactical-read finding.
  - Deciding whether bundled-offer source material needs explicit capture obligations.
  - Preparing a bounded docs-only patch to Data Capture Spine artifacts.
authority_boundary: retrieval_only
```

## Operator Prompt

Use `workflow-deep-thinking` before acting. If you decide a docs patch is
warranted, use `workflow-implementation-scoping` before editing.

You are continuing Orca product-proof work in a fresh thread. This is a
Data Capture Spine follow-up, not a Judgment Spine backtest and not a product
feature plan.

## Objective

Decide whether the Data Capture Spine should explicitly preserve bundle
structure and concession framing when source material includes a counterparty
offer, package, settlement, public-sector deal, regulatory bargain, or similar
multi-term proposal.

If yes, make the smallest complete docs-only patch so future case construction
does not flatten load-bearing negotiation evidence into a plain list of terms.

## Context

The Milwaukee fiscal-crossroads reveal readout surfaced a tactical read that
the earlier case-learning layer did not carry strongly enough:

- WRS/new-hire pension reform appearing inside the state package is not merely
  "a good mechanism inside a bad package."
- Its placement inside the bundle is also observable evidence about how the
  counterparty may frame what Milwaukee values and what it expects to trade for
  broader oversight or governance constraints.
- This does not prove state motive. It does mean that packaging is information.

Data Capture implication: if a source packet records only "WRS reform was in
the package," it can lose the tactical judgment signal. The raw observable must
preserve how terms were bundled, which terms were framed as concessions,
requirements, restrictions, safeguards, or sweeteners, and what dependencies or
tradeoffs the source text makes visible.

## Required Reads

Read only targeted sections needed for this decision:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md`

Do not read contaminated archive bodies. Do not run public web research unless
the current user turn explicitly authorizes it.

## Decision To Answer

Should Data Capture Spine v0 add an explicit obligation for bundled-offer
observables?

Answer in one of these statuses:

- `PATCH_DATA_CAPTURE_CONTRACT`
- `PATCH_CONTEXT_NOTE_ONLY`
- `DEFER_TO_SOURCE_FAMILY_SATELLITE`
- `NO_PATCH`

## Evaluation Criteria

Treat the patch as justified only if it improves future judgment capture without
turning Data Capture into analysis.

A good Data Capture obligation should preserve:

- bundle membership: which terms appear together in the same offer or package
- term text: the source's own wording for each material term, using short
  compliant excerpts or precise paraphrase with source location when full
  quotation is not appropriate
- source framing: concession, requirement, restriction, safeguard, sweetener,
  penalty, condition, or optionality
- term dependencies: what must be accepted together, what can be severed, what
  is conditional, and what expires or sunsets
- counterparty language: the words the source uses to describe why the term is
  included
- sequence: when the term entered the package and whether it changed across
  drafts, votes, memos, or negotiations
- evidence boundary: observed framing versus inferred motive

A bad patch would:

- infer counterparty intent as fact
- require every ordinary source packet to become a negotiation analysis
- add schema or implementation work
- overfit Milwaukee instead of naming a reusable source-observable rule

## Patch Scope If Accepted

Allowed target files:

- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`

Prefer the smallest complete patch. Do not create runtime code, schemas,
automation, scraping, data infrastructure, fine-tuning plans, deck artifacts, or
product feature plans.

## Output Requirements

Return:

1. Verdict status.
2. Changed artifact path(s), if any.
3. SHA256 for each changed artifact, if any.
4. One-sentence core thesis.
5. What obligation was added or why no patch was needed.
6. Why this belongs in Data Capture rather than Judgment Spine.
7. What remains deferred.
8. Explicit non-claims.

## Non-Claims

Do not claim:

- product readiness
- feature readiness
- implementation readiness
- data-pipeline readiness
- model-training readiness
- buyer validation
- willingness-to-pay proof
- repeatability proof
- that Milwaukee proves the rule across cases
- that any counterparty motive is known unless the source directly states it
