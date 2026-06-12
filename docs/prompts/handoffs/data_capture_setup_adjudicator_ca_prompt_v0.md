# Data Capture Setup Adjudicator CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Chief Architect adjudication prompt for consolidating two blind Data Capture Spine setup CA outputs into one source-grounded recommendation.
use_when:
  - Adjudicating Opus and GPT blind Chief Architect outputs for Orca Data Capture Spine setup.
  - Resolving conflicts between Data Capture setup recommendations without averaging them.
  - Producing a final owner-facing recommendation before an Evidence Candidate Record / Evidence Unit prompt is launched.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - Orca renames Data Capture Spine, Evidence Candidate Record, Cleaning Spine, or Judgment Spine.
  - The Data Capture Spine CA read pack changes.
  - The two blind CA outputs were generated from a materially different prompt than the one described here.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `handoff`.

Target actor: Adjudicating Chief Architect.

Output mode for downstream adjudicator: `chat-only`.

Edit permission for downstream adjudicator:
Read-only. Do not create or edit files. Do not write schemas, source maps,
source inventories, APIs, adapters, scrapers, storage designs, dashboards,
automation, tests, implementation plans, or runtime specs.

## What You Are Adjudicating

You are adjudicating two blind Chief Architect outputs for Orca's **Data Capture
Spine setup**. You are not producing a third independent brainstorm. You are
deciding which arguments survive source grounding, where the outputs agree,
where they conflict, which argument is stronger, and what final recommendation
Orca should carry forward.

Do not average the two outputs. Do not accept consensus as proof. Treat each
lane output as an argument to inspect against Orca sources and the prompt
contract.

Paste the two lane outputs below before running:

```text
LANE_A_OUTPUT:
<paste Opus or lane A output here>

LANE_B_OUTPUT:
<paste GPT or lane B output here>
```

## Fixed Boundary For This Adjudication

Use this current boundary unless loaded Orca sources directly contradict it:

```text
Data Capture Spine
-> Evidence Candidate Record
-> Cleaning Spine
-> Judgment Spine
-> Decision Artifact
-> Outcome Memory
```

Working meanings:

- **Data Capture Spine** owns evidence-grade signal discovery, access posture,
  capture obligations, preservation posture, source visibility, source identity,
  event/capture timing, cutoff/archive posture, capture fidelity, multimodal
  capture obligations, and categorical handoff requirements into Evidence
  Candidate Record.
- **Evidence Candidate Record** is the pre-cleaning captured-signal receipt /
  content contract. It should receive enough capture context to let later
  cleaning and judgment inspect the signal, but this adjudication must not
  design ECR fields, schemas, keys, or data types.
- **Cleaning Spine** owns raw-to-cleaned transformation traceability,
  normalization, translation, summarization, dedupe, clustering, and related
  cleaning mechanics. It does not own credibility, uncertainty, or action
  ceilings.
- **Judgment Spine** owns integrity labels, credibility effects, discounting,
  exclusion for integrity or decision-use reasons, Signal Use Classification,
  Decision Strength, Action Ceiling, counterevidence, and valid claim use.

If either lane uses the stale meaning "Data Spine = EOM / Evidence Unit content
contract only," mark that as a contamination risk unless it explicitly
reconciles with the current Data Capture Spine boundary.

## Source-Gated Method Contract

Follow Orca's Source-Gated Method Contract.

REFERENCE-LOAD method instructions only:

- `workflow-deep-thinking`
- `workflow-architecture-planning`, standard profile, as a local perspective
  structure only

Do not APPLY either method before source readiness.

Before `SOURCE_CONTEXT_READY`, you may only prepare a neutral source-reading
lens. Do not frame the problem, rank lanes, identify winners, produce findings,
or recommend a target architecture before source loading is complete.

After source loading, declare either:

```text
SOURCE_CONTEXT_READY
sources_read:
targeted_sections_read:
sources_missing_or_unavailable:
sources_excluded_by_rule:
source_conflicts:
```

or:

```text
SOURCE_CONTEXT_INCOMPLETE
sources_read:
targeted_sections_read:
sources_missing_or_unavailable:
sources_excluded_by_rule:
source_conflicts:
impact_on_adjudication:
```

Only after that declaration, APPLY the methods to adjudicate the two outputs.

## Required Source Loading

Read Orca authority and source-loading policy first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md`
4. `.agents/workflow-overlay/prompt-orchestration.md`

Then follow `.agents/workflow-overlay/source-loading.md`, especially the
**Data Capture Spine CA Read Pack**.

Use the targeted sections only:

- `docs/decisions/turn_08_product_thesis_v0.md`: thesis, value proposition,
  strategic center, and current theory sections.
- `docs/product/orca_offer_hypothesis_v0.md`: core offer hypothesis,
  mechanism, fit diagnostic, and non-claims sections.
- `docs/product/orca_buyer_proof_packet_v0.md`: proof standard, target buyer,
  signal surface, disqualifiers, and not-build boundaries.
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`:
  purpose, decision, layer rules, and future ECR/Evidence Unit boundaries.
- `docs/product/core_spine_v0_product_contract.md`: product bet, core rule,
  frozen primitives, and explicit non-goals only.
- `docs/product/core_spine_v0_information_production_foundation_v0.md`:
  Evidence Unit standard and boundary rules only.

Do not read these files in full by default. Use headings/search and targeted
sections. Expand only if a source gap would materially change adjudication.

Default exclusions:

- `docs/_inbox/`
- all review outputs
- all method-validation replays
- all proof-run packets
- all research corpus files
- all historical prompts
- all source maps or source inventories unless the loaded prompt explicitly
  made them decision-bearing

## What Counts As A Strong Answer

A strong adjudication should preserve the Data Capture focus:

- Data Capture setup should make high-quality captured signal available to ECR.
- It should be future-runtime-aware, but non-implementation.
- It may compare capture postures such as structured access, autonomous
  extraction, archive/cutoff, agent-directed discovery, human-assisted capture,
  multimodal-priority capture, and hybrid evidence-grade capture.
- It must not collapse into generic OSINT, social listening, scraper-first
  tooling, source inventory planning, or implementation architecture.
- It must not design ECR fields or the Cleaning/Judgment Spine.
- It must not let source availability determine decision validity.

Useful but often overvalued:

- exhaustive source catalogs;
- named scraper/API tools;
- "use every source" answers;
- broad agentic collection without capture accountability;
- source maps that become collection plans;
- implementation confidence from the fact that scrapers are easy.

Often undervalued but important:

- capture fidelity and preservation obligations;
- event time vs capture time vs visibility time;
- source identity and source carrier separation;
- volatile/deleted/edited/dynamic-page handling;
- archive/cutoff posture;
- multimodal capture obligations;
- evidence-grade handoff requirements into ECR;
- capture failure visibility and non-captured-signal accounting;
- source blind spots and satellite-owned adaptation boundaries.

## Required Adjudication Output

Return:

1. **Source Readiness**: `SOURCE_CONTEXT_READY` or
   `SOURCE_CONTEXT_INCOMPLETE`, with read ledger and gaps.
2. **Lane Compliance Check**: whether each lane followed Data Capture focus,
   non-implementation boundary, source loading, and ECR/Cleaning/Judgment
   boundaries.
3. **Agreement Map**: where both lanes agree and whether the agreement is
   source-backed, merely plausible, or weak.
4. **Material Conflicts**: exact conflicts, why they matter, and which source
   or criterion decides them.
5. **Stronger Arguments**: for each major conflict, name the stronger lane or
   stronger hybrid and why. Do not average.
6. **Final Data Capture Setup Recommendation**: the architecture/setup posture
   Orca should carry forward, stated as a target shape and operating logic, not
   implementation design.
7. **Core vs Satellite Boundary**: what Data Capture must own centrally versus
   what buyer/industry/decision/source-family satellites adapt.
8. **Handoff To Evidence Candidate Record**: state what the handoff must
   accomplish categorically. Do not name fields, schema keys, data types,
   tables, IDs, or final ECR field lists.
9. **What To Reject Or Defer**: reject wrong architectures and defer runtime,
   source systems, ECR design, Cleaning Spine design, Judgment Spine design,
   feature planning, and implementation planning.
10. **Smallest Next Artifact**: name the smallest next artifact to create or
    patch after adjudication, if any.
11. **Remaining Owner Decisions**: decisions the owner must make before the
    next architecture or prompt lane.
12. **Rerun Warning**: if either lane is contaminated by stale Data Spine/EOM
    naming, source-free method application, or implementation leakage, say
    whether to discard it, partially salvage it, or rerun it.

## Hard Boundaries

- Do not create or edit files.
- Do not write schemas, ECR fields, APIs, adapters, scrapers, storage designs,
  dashboards, automation, tests, implementation plans, or deployment plans.
- Do not design the Cleaning Spine, Judgment Spine, Evidence Candidate Record,
  or source inventories.
- Do not claim buyer validation, willingness to pay, product readiness, feature
  readiness, implementation readiness, commercial readiness, validation,
  approval, or source-of-truth promotion.
- Do not use prior Orca chat memory as authority when local source contradicts
  it.

## Final Decision Standard

The final recommendation should answer:

```text
What Data Capture Spine setup gives Orca the strongest evidence-grade signal
acquisition and preservation posture, while making ECR/Cleaning/Judgment easier
and more accountable, without turning Orca into a generic source-collection,
OSINT, scraper, or dashboard platform?
```

If the two blind CA outputs are both weak, say so and recommend rerun rather
than manufacturing a synthesis.
