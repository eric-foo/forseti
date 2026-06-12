# Data Capture Harness Product Goal Opus Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Paste-ready Opus prompt for deriving the Data Capture Harness product goal and operating contract from Orca product sources.
use_when:
  - Running an Opus lane before Data Capture Harness architecture planning.
  - Checking whether the current manual harness should be demoted to direction signal rather than treated as controlling architecture.
  - Creating a product-grounded harness goal before feature, implementation, ECR, Cleaning, Judgment, or runtime work.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/product/product_lead/orca_offer_hypothesis_v0.md
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md
stale_if:
  - Orca product thesis, offer hypothesis, buyer-proof packet, or Core Spine product contract is materially revised.
  - The current Data Capture manual harness artifacts are promoted, rejected, or superseded by owner decision.
  - A later Data Capture Harness product-goal prompt supersedes this prompt.
```

- Prompt target: Claude Opus.
- Output mode: `paste-ready-chat`.
- Created: 2026-05-27.
- Implementation authorized: no.
- Runtime/source-system design authorized: no.
- ECR/Cleaning/Judgment design authorized: no.
- Source-of-truth promotion claimed: no.

## Prompt Construction Notes

This prompt is tailored for Claude Opus rather than copied from the GPT-5.5
generic template. Local Orca search found no registered Opus-specific prompt
template. The structure uses explicit role, source-read gates, XML sections,
and a bounded output contract because Anthropic's current Claude prompting
guidance recommends clear instructions, context, XML structuring, explicit
roles, long-context structure, and self-checking for complex source-grounded
work.

## Paste-Ready Prompt

```text
<role>
You are Claude Opus acting as an independent product-architecture Chief
Architect for Orca. Your task is to reason from Orca's product documents and
produce a product-grounded Data Capture Harness goal / operating contract
candidate.
</role>

<operating_mode>
Use high-quality architectural judgment. Reason carefully from the source
documents, but do not expose private chain-of-thought. Return source-grounded
conclusions, decisive rationale, assumptions, and non-claims.

This is an upstream product-goal lane, not implementation planning and not full
harness architecture planning.
</operating_mode>

<orca_authority>
Use this Orca source hierarchy:
1. Current user instruction for this prompt.
2. Orca AGENTS.md.
3. Orca overlay under `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow methods only for generic mechanics, not Orca facts.

Do not import `jb` rules, paths, lifecycle mechanics, product policy, or
validation habits as Orca authority.
</orca_authority>

<current_user_decision_context>
The owner is considering a directional reset:
- The current Data Capture manual harness and BT2-04 dry run should not be
  treated as the controlling final harness architecture.
- They may still be valuable as real product-method pressure evidence.
- A candidate label is "Data Capture Harness Direction Signal v0".
- Before architecture planning the harness, the owner wants Opus to derive the
  ultimate product goal of a Data Capture Harness from Orca product documents.

Your job is not to agree with this framing automatically. Treat it as a
candidate and pressure-test it against the sources.
</current_user_decision_context>

<required_source_loading>
If you have filesystem access, read these sources in this order. If you do not
have filesystem access, return `SOURCE_CONTEXT_INCOMPLETE` and ask for a source
capsule containing these files or targeted sections. Do not substitute generic
product intuition.

Control and loading sources:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/product-proof.md`

Product goal sources:
- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Data Capture direction-signal sources:
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`

Default exclusions:
- Do not read `docs/_inbox/`.
- Do not read method-validation replay history unless a loaded source proves it
  is necessary for this product-goal question.
- Do not read all research corpus files.
- Do not widen into Judgment Harness specs unless you find a source conflict
  that directly affects Data Capture Harness product goal.
</required_source_loading>

<source_readiness_gate>
Before producing the product-goal answer, declare one of:
- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

If incomplete, name the missing sources and explain what claims cannot be made.
If ready, provide a compact source-read ledger: source, why read, and the claim
it supports. Keep the ledger compact; do not paste full documents.
</source_readiness_gate>

<task>
Answer this question:

What is the ultimate product goal of a Data Capture Harness in Orca, for the
greatest product gain, based on the product documents?

Then decide whether the current Data Capture manual harness / BT2-04 dry run
should be demoted to a direction signal, preserved as a prototype, rejected, or
treated as current controlling architecture.
</task>

<decision_criteria>
Use criteria that distinguish product gain, not generic architecture quality:
- Does the harness increase buyer trust in Orca's decision artifact?
- Does it protect the memo/evidence appendix/deck from source theater?
- Does it make public signals inspectable, bounded, and failure-visible?
- Does it preserve the Core Spine layer split?
- Does it prevent Data Capture from becoming a source map, scraper plan,
  dashboard, generic OSINT workflow, or bespoke research checklist?
- Does it support repeatable decision-evidence production without requiring
  software, automation, dashboards, source systems, or collection pipelines?
- Does it preserve trust-objection and buyer-proof non-claims?
- Does it keep downstream ECR, Cleaning, Judgment, Decision Strength, and
  Action Ceiling outside Capture?
</decision_criteria>

<hard_boundaries>
Do not:
- design the final harness architecture;
- write ECR fields, schemas, keys, tables, storage, or record formats;
- design Cleaning, Judgment, runtime, source-system, scraper, API, dashboard,
  automation, or implementation architecture;
- claim buyer validation, willingness to pay, product readiness, feature
  readiness, implementation readiness, commercial readiness, formal validation,
  source-of-truth promotion, or owner acceptance;
- treat the existing manual harness review as validation;
- average source conflicts or seek consensus for its own sake.
</hard_boundaries>

<output_contract>
Return a decision-bearing product-goal memo with these sections:

1. Source Readiness
   - `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
   - Compact source ledger and material gaps.

2. Real Decision
   - State the actual upstream decision this prompt is resolving.

3. Product Anchors
   - Name the Orca product promises and constraints that matter most.

4. Ultimate Harness Goal
   - One sentence.
   - Then 3-6 paragraphs explaining the goal in product terms.

5. Greatest-Gain Thesis
   - Explain where the harness creates the most Orca value.
   - Distinguish buyer value, operator value, and strategic moat.

6. What The Harness Must Maximize
   - Use bullets.
   - Include only properties that directly support the product goal.

7. What The Harness Must Not Become
   - Use bullets.
   - Tie each forbidden direction to the product risk it creates.

8. Status Of The Current Manual Harness
   - Choose one:
     - `DEMOTE_TO_DIRECTION_SIGNAL`
     - `PRESERVE_AS_PROTOTYPE`
     - `REJECT_AS_WRONG_DIRECTION`
     - `TREAT_AS_CONTROLLING_ARCHITECTURE`
   - Recommend the best label, such as `Data Capture Harness Direction Signal v0`,
     or a better one.
   - Explain what evidence it provides and what it does not prove.

9. Missing Product Decisions Before Architecture
   - Name the owner decisions or operating-contract choices needed before a
     full harness architecture plan.

10. Architecture-Planning Readiness
   - Say whether Orca should architecture-plan the harness next.
   - If yes, state the exact scope of that architecture lane.
   - If no, state the smallest upstream artifact still missing.

11. Non-Claims
   - List strict claims not made.

12. Final Recommendation
   - A concise recommendation for the owner.
</output_contract>

<self_check>
Before finalizing, check your answer for these failure modes:
- overfitting the product goal to BT2-04;
- treating more sources as automatically better evidence;
- making Data Capture responsible for Judgment;
- turning the harness into a tool architecture;
- calling the direction signal validated;
- shrinking Orca's product promise to internal proof mechanics;
- ignoring buyer-facing executive-deck value;
- failing to preserve memo/evidence appendix as the proof substrate.
</self_check>
```
