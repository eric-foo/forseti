# Data Capture Spine Pressure-Test Commissioning Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Bounded pressure-test commissioning plan for the Data Capture Spine lane against the accepted intake-surface target, accepted v2 operating-model architecture, and current obligation contract.
use_when:
  - Preparing to run 3 real commissioned Data Capture pressure tests against the accepted intake-surface target and patched harness architecture.
  - Checking which obligations, vocabularies, and roles the pressure tests are meant to expose.
  - Checking what the pressure tests will not cover in v0.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_execution_authorization_v0.md
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2.md
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
  - docs/product/data_capture_spine/data_capture_spine_lane_product_thesis_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
  - docs/product/data_capture_spine/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - The Data Capture intake-surface consolidation is rejected, narrowed, or superseded.
  - The Data Capture Harness v2 acceptance is amended, rejected, or superseded.
  - v2 is materially patched or superseded.
  - The Data Capture obligation contract is materially revised or superseded.
  - Pressure-test evidence triggers re-architecture per v2's Stop Conditions And Re-Architecture Triggers.
  - The owner names specific decision frames for the pressure-test batch (this plan should then be paired with an execution authorization artifact).
```

## Status

Status: `PROPOSED_COMMISSIONING_PLAN_FRAMES_NAMED_V0`.

This artifact plans the next bounded pressure-test commissioning step against the owner-accepted intake-surface target and v2 architecture. Owner-named frames for all three slots are pinned in the Pressure-Test Batch Shape section. It does not authorize pressure-test execution by itself. Execution now depends on the paired owner-decision artifact `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`, while this plan remains the commissioning-shape source.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 pressure-test commissioning planning pack
  edit_permission: docs-write for this product artifact only
  target_scope:
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_harness_operating_model_architecture_v2.md
    - docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
```

## Controlling Versions

The pressure tests run against:

| Controlling artifact | Reference | Hash |
| --- | --- | --- |
| Intake-surface target | `docs/product/data_capture_spine_intake_surface_consolidation_v0.md` | accepted as bounded pressure-test target 2026-05-30 |
| Operating-model architecture | `docs/product/data_capture_harness_operating_model_architecture_v2.md` | `B0AAF782227C79198F6343F45B81ECCCCD3D76BF1572162C77C822BDB1339509` |
| Obligation contract | `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | current version in named-path status |
| Obligation baseline acceptance | `docs/product/data_capture_obligation_baseline_decision_v0.md` | accepted 2026-05-28 |
| v2 acceptance for this scope | `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md` | accepted 2026-05-28; MSP amendment accepted 2026-05-30 |

If any of these is materially patched or superseded before execution, this plan is stale and must be re-pinned.

## Pressure-Test Batch Shape

The first batch is 3 real commissioned captures, not 5. Five remains useful for a later batch if the first 3 do not surface architecture-threatening evidence; starting with 3 keeps ceremony low and forces the lane to learn from real source mess instead of fixture rehearsal.

The 3 frames must differ in source-family stress. Each slot is bound to a real, decision-tied frame; inventing a frame to fill a slot is fixture rehearsal and is forbidden.

| Slot | Source-family stress | Owner-named real frame | Decision tie |
| --- | --- | --- | --- |
| Slot 1 | Bundled-offer + archive/history + pricing-page version, finance-specialized content lane | **Mergers & Inquisitions** pricing / product / bundle posture across a 12-24 month window (`mergersandinquisitions.com`, course catalog, pricing pages, archive snapshots, retired/announced courses) | jb pricing decision; competitive positioning on the finance-specialized resume-content flank |
| Slot 2 | Changelog / pricing / feature version + recent edit posture, AI-generic resume-tool lane | **Teal** (`tealhq.com`) public docs, pricing tiers, feature posture, and recent change history across ~12 months | jb competitive positioning vs the AI-generic resume-tool flank; broader-market AI-resume reference for pricing |
| Slot 3 | Forum threading + anonymous actor identity + deletion/edit/lock posture + review-surface recency | **Non-target US-domestic candidate** forum/review discourse on **resume-driven interview-getting pain**, primary venues Reddit (`r/FinancialCareers`, `r/CFA`) and Wall Street Oasis non-target threads, cutoff Q2 2026 | Validate non-target US-domestic + resume-gap as jb's VP target; capture avatar language; identify reach venues |

The three frames are deliberately structured as two competitive flanks (slot 1 finance-specialized, slot 2 AI-generic) plus customer-pain validation (slot 3). Slot 3 stays inside jb's actual current product scope (resume building) and marks out-of-scope adjacent pain branches (networking, technical interviews, credential choice) as visible related context but not the captured signal.

Frame-selection criteria:

- The frame must be tied to a decision someone actually has to make (real Decision Frame), not a synthetic scenario.
- The decision question, owner or owner-context, consequence, cutoff posture, and downstream-use intent must be known enough for capture obligations to be evaluated (per Obligation 1).
- The source boundary must stay inside the current Orca source-access boundary: discoverable source material, free/account-created access, entitled paid/client/coworker access, disclosable access method, no use of obvious cross-account/private/admin spillover once noticed, and no hard-stop access path (per Obligation 2).
- The frame must plausibly stress at least one obligation that is not trivially `met` or `not_applicable` (otherwise the test has no signal).

If only 2 real frames can be named at execution time, the batch may run as 2; do not invent the third. If only 1 real frame can be named, the batch is not ready and the plan should be re-paced.

## Deferred Source-Family Coverage

With frames now named, the original deferral list narrows.

The first batch covers:

- **bundled-offer structure (obligation 13)** primarily through slot 1 (M&I sells individual courses and bundles) and mildly through slot 2 (Teal's free/paid tier structure). This is a deliberate departure from the earlier "deferred" framing: M&I is too good a substitute pricing reference to skip, and obligation 13 is too load-bearing to leave unstressed in batch 1.
- **archive/history per slice (obligation 10)** across all three slots: M&I has 10+ years of pricing and product history; Teal has recent pricing and feature edits; forum threads carry real deletion, edit, and lock posture. A separate archive-history-only frame is no longer needed for batch 1.

The first batch deliberately does not stress:

- **multimodal capture (capture mode):** none of the three slots primarily stresses multimodal source material. This remains queued for batch 2 if batch 1 is patchable. If batch 1 surfaces architecture-threatening evidence (per the Invalidation Criteria), multimodal pressure-testing is paused pending re-architecture.

## Capture-Session Markdown Template

The first obligation-discharge artifact form is a short structured Markdown note per capture. Markdown is chosen over spreadsheet to resist schema gravity and to keep ECR design out of Capture. The template is the smallest shape that still exposes every obligation state.

```markdown
# Capture: <decision frame slug> / <source-family slug> / <date>

## Decision Frame
- Decision question:
- Owner or owner-context:
- Consequence:
- Allowed decision verbs (if relevant):
- Cutoff posture:
- Downstream-use intent:

## Source Boundary
- Source surfaces in scope:
- Boundary compliance (discoverable-or-entitled / free or account-created / disclosable / no obvious spillover once noticed / no hard-stop access path):
- Out-of-bounds material observed and excluded:

## Capture Mode
- Initial mode (human-led / agent-assisted / structured access / archive-history / automated extraction / multimodal / mixed):
- Material mode changes during the session (each with reason):

## Per-Obligation Discharge States

| # | Obligation | State | Reason (required for non-`met`) |
| --- | --- | --- | --- |
| 1 | Commissioning Gate | | |
| 2 | Boundary Compliance | | |
| 3 | Capture-Event Provenance | | |
| 4 | Capture Mode Disclosure | | |
| 5 | Mode-Change Rule | | |
| 6 | Raw Observable Fidelity | | |
| 7 | Source Identity And Actor Context | | |
| 8 | Decomposed Timing | | |
| 9 | Cutoff Posture | | |
| 10 | Archive / Historical Posture | | |
| 11 | Source Visibility And Access Limits | | |
| 12 | Related Context Preservation | | |
| 13 | Bundled-Offer Structure Observables | | |
| 14 | Capture Failure And Blocker Visibility | | |
| 15 | Re-Capture Semantics | | |
| 16 | Categorical Handoff Readiness | | |

Allowed states per cell: `met`, `partial`, `assessed_not_met`, `cannot_assess`, `access_failed`, `blocked`, `unavailable_by_source`, `not_applicable`, `not_attempted`. A blank cell is forbidden. A `met` cell does not require a reason; every other state requires a visible reason.

## Per-Slice Posture (where states differ)
- Archive/history per slice:
- Source visibility/access per slice:
- Related context per slice:
- Re-capture relationship per slice:

## Raw Observable Pointers
- Pointers to preserved source-visible language, layout, modality, thread/related-chain context, and bundled-offer structure where it carries signal:
- Notes on modality preservation where text-only would lose signal:

## Failures, Blockers, and Limitations
- Capture-owned failures observed:
- Visible limitations to travel downstream:
- Out-of-bounds material treated as out of bounds (not worked around):

## Agent-Assistance Context
- Allowed agent verbs used:
- Discarded candidates and discard reason categories:
- Any cross of the allow/forbid line (must be `blocked` on the relevant obligation):

## Categorical Handoff Or Visible Stop
- Handoff state: `categorical_handoff_to_ECR` / `visible_stop` / `visible_blocker` / `rerun` / `re-capture_posture`
- Reason if not categorical_handoff_to_ECR:

## LLM Capture-Visibility Checker Output
- Output: `capture_closure_blocker` / `visible_capture_limitation` / `vocabulary_divergence` / `vocabulary_consistent`
- Specifics (which obligation, which slice, what is missing or smuggled):
- Remediation taken by capture operator (if any):
- Post-remediation re-invocation output (if any):
```

If Markdown under-records during the pressure tests, pressure-test evidence can justify a more structured form. Start at the least-runtime shape that still exposes every obligation state.

## LLM Capture-Visibility Checker

The second-operator capture-visibility check is performed in v0 by an LLM with a single manual prompt invocation per capture. This is the second-operator role in v2's Role Model, fulfilled by an LLM rather than a human, scoped as a partial visibility control.

Model selection: **GPT-5.5** via manual paste in a separate UI conversation from the capture operator's working session. The capture operator uses Claude as agent assistant during capture; the LLM checker uses GPT-5.5 in a separate conversation. The cross-family separation strengthens the "second operator distinct from primary operator" property.

Pinned prompt: `docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md`. The checker is invoked using that prompt verbatim followed by the completed capture Markdown artifact. The output is copied back to the capture artifact's "LLM Capture-Visibility Checker Output" section.

Pinned subagent allow-list template: `docs/prompts/templates/data_capture_spine_pressure_test_subagent_allow_list_template_v0.md`. For agent-assisted enumerate/fetch/archive/transcribe/link/mechanically-group work during capture sessions, the capture operator adapts this template per slot per task. The subagent operates under the obligation contract's allow/forbid line; its outputs are raw material the capture operator inspects, not capture-state declarations.

### Scope Constraints

For v0 pressure tests, the LLM capture-visibility checker operates under three constraints:

1. **Artifact-internal only.** The LLM inspects the completed capture Markdown artifact for visible obligation discharge, missing states, forbidden Capture outputs (Judgment language), hidden failures, rollup flattening where per-slice posture is required, and handoff-boundary violations. It does not verify source fidelity, source completeness, multimodal preservation, or bundled-offer structure against the original source.
2. **Manual prompt only.** One manual prompt invocation per capture. No wrapper, automation, integration, schema, dashboard, source tool, or test harness is authorized. The output is copied back as operating evidence, not runtime output. Post-remediation re-invocation is one additional manual prompt invocation; iteration beyond that is not authorized in v0.
3. **No re-capture / no source corpus access.** The LLM does not receive the same source corpus the capture operator inspected. Source access would let the LLM silently re-capture in different terms, which contaminates the test by making artifact-vs-LLM disagreement uninterpretable. Source access can be a later pressure-test variant only if v0 evidence shows artifact-internal checking is insufficient.

Explicit partial-coverage non-claim: source-fidelity failures, multimodal preservation failures, bundled-offer structure loss against source, and related-context fairness against source may go uncaught in v0. If pressure-test evidence later shows these were the dominant failure modes, that is itself evidence to consider a different second-operator shape in v1.

### Inspection Questions

The LLM checker inspects the capture artifact against six questions:

1. Are all 16 per-obligation states declared with one of the nine allowed values, with reasons for non-`met` states?
2. Is any source/context/failure/mode/cutoff/archive posture silently missing or only present at rollup level when per-slice posture is required?
3. Did Capture smuggle in Judgment, Cleaning, or downstream-use vocabulary (credibility, integrity, discounting, exclusion, Signal Use, Decision Strength, Action Ceiling, source-quality scoring, source maps, runtime plans)?
4. Did the operator collapse mixed source states into a rollup where the contract requires per-slice posture (archive/history, source visibility/access, related context, re-capture semantics)?
5. Is raw observable missing where the source modality, language, layout, or thread context carries signal?
6. Is the handoff state categorical without designing ECR fields, IDs, schemas, or storage?

### Output Vocabulary

The LLM checker outputs only one of:

- `capture_closure_blocker`: a capture-owned omission or boundary violation that prevents clean categorical handoff (silent omission, hidden mode change, per-slice rollup where states differ, raw-observable loss, hidden failure, forbidden agent verb, forbidden Capture output, smuggled Judgment language).
- `visible_capture_limitation`: a non-blocking capture limitation that must travel downstream (source-limited actor identity, failed archive attempt, fallback access, unknown timing, partial related context, modality limitation).
- `vocabulary_divergence`: a checker-visible mismatch between contract vocabulary and artifact language that is not clearly labeled as a proposal.
- `vocabulary_consistent`: checker-visible contract vocabulary appears consistent for the checked surface. It is not capture adequacy, validation, readiness, approval, source adequacy, or proof.

The LLM checker must not output: `approved`, `validated`, `pass`, `fail`, credibility ratings, source-quality scores, inclusion/exclusion advice, downstream-use advice, buyer-proof claims, or any evaluative language outside the four-token vocabulary plus the question-specific specifics that justify the output.

### Coupled-Hypothesis Recording

Pressure tests are testing v2-with-LLM-checker, not v2-with-arbitrary-second-operator. If the LLM checker drifts into reviewer authority or fails to discriminate, that evidence concerns both the architecture's fragility and the LLM-checker shape; the two should be diagnosed separately, not collapsed into either a pure-architecture or pure-LLM-choice finding.

### F-01 In LLM Context

v2's F-01 patch (blocker-resolution authority) still holds with an LLM checker:

- The capture operator owns remediation of capture-owned blockers.
- The commissioner owns Decision Frame, source-boundary, or commission stop/re-scope decisions when a blocker exposes an upstream frame problem.
- The LLM checker (as second operator) does not approve remediation, certify closure, refuse closure, validate the capture, or decide downstream use. Post-remediation re-invocation may record a newly visible `capture_closure_blocker` or `visible_capture_limitation`, but that record remains evidence of a capture-owned condition, not LLM-checker approval or refusal authority.

## Invalidation Criteria

Pressure-test evidence must be classifiable before tests run. Motivated reclassification after the fact is forbidden.

### Patchable

A patchable finding is a one-off issue that the obligation contract, architecture, vocabulary, or artifact form can absorb without changing the architecture's shape:

- one-off vocabulary roughness (a single capture where vocabulary is awkward but the obligation is still exposed);
- artifact-form friction (a single capture where the Markdown template feels heavy or under-structured but is still complete);
- source-family-specific adaptation (a single capture where a satellite source-family rule needs adjustment without core change);
- one-off operator confusion that is corrected within the session;
- single-frame partial coverage (one slot of the batch did not stress an obligation that other slots covered).

### Architecture-Threatening

An architecture-threatening finding suggests v2's shape, not operator practice, is wrong. The list:

- repeated hidden Judgment language across captures, where operators or agents pre-filter relevance, classify credibility, decide inclusion, or import downstream-use vocabulary;
- repeated inability to preserve raw observable or related context without the operator wanting tooling, schema, or runtime support;
- the LLM capture-visibility checker role collapsing into approval/refusal authority (e.g., its output is being interpreted as a pass/fail label, or its `vocabulary_consistent` is being read as certification);
- operators needing source maps, source inventories, dashboards, or runtime to function (any capture that cannot complete without forbidden runtime gravity);
- downstream layers needing to recollect source history because the captured artifact did not actually carry enough categorical context;
- repeated stop conditions firing at the same obligations across captures (per v2's Stop Conditions And Re-Architecture Triggers — stops are not failures, but *repeated* stops at the same obligation suggest the architecture is mis-shaped at that obligation);
- uniform clean LLM checker output across all 3 captures with zero `capture_closure_blocker`, zero `visible_capture_limitation`, and zero `vocabulary_divergence` records (the rubber-stamp signal — the role's value depends on finding real things; uniform clean is more likely to mean the role is decorative than that capture is uniformly excellent).

### Count Thresholds For This Small-N Batch

With 3 captures, the thresholds for treating evidence as a pattern:

- 1 of 3 = patchable, unless the failure is unambiguous and severe in itself (e.g., a single capture where Judgment language saturates the artifact);
- 2 of 3 = architecture-threatening signal, requires pause before further pressure tests and a deliberate review of which architecture-threatening criterion fired;
- 3 of 3 = architecture-threatening confirmed; v2's controlling status yields under the Re-Architecture Trigger Clause of the v2 acceptance decision.

A single capture failure does not invalidate v2. A 2-of-3 or 3-of-3 pattern does. Saying so explicitly here protects against post-hoc reclassification.

## Speed Discipline

The owner is driving for public release ASAP, with the constraint that the full Spine (Capture → ECR → Cleaning → Judgment → Decision Artifact → Outcome Memory) must be in place before buyer-facing commercial test. This plan respects that pace by:

- starting with 3 frames, not 5;
- using Markdown, not schema;
- using an LLM checker, not staffing a separate human role;
- forbidding runtime, tooling, and ceremony;
- pinning invalidation criteria before tests run so evidence can be acted on quickly.

What this plan refuses to compress for speed:

- a Spine layer's actual obligations (any capture that skips obligation states for speed destroys the lane thesis);
- per-slice posture where states differ (rollup-for-speed is exactly the failure the architecture defends against);
- raw-observable preservation (paraphrase-for-speed is exactly what BT2-04 surfaced);
- the layer boundary (capture-time Judgment for speed is exactly what the obligation contract forbids).

A half-built Spine is worse than a delayed release. The plan paces for speed only by removing what was already ceremony, not by removing what is load-bearing.

## What This Plan Does Not Do

- Authorize pressure-test execution.
- Name specific decision frames (requires owner input).
- Build any runtime, tooling, automation, scraper, API, dashboard, schema, storage, package, test, or deployment.
- Design ECR fields, Cleaning transformations, Judgment rules, memo or appendix format, deck content, or outcome-memory representation.
- Validate the obligation contract, harness architecture, manual harness, BT2-04 dry run, or thesis.
- Promote any v2 Pressure-Test Candidate Operating Control (five-role model, two-output second-operator vocabulary, capture-operator remediation vocabulary) to stable inherited obligation.
- Make buyer-proof, commercial-readiness, or willingness-to-pay claims.
- Source-of-truth-promote any artifact beyond the named decisions.

## Non-Claims

This artifact does not claim:

- validation;
- hardening;
- readiness of any kind;
- buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, commercial readiness;
- final harness acceptance;
- Data Capture Spine completion;
- ECR, Cleaning, Judgment, memo, evidence appendix, executive deck, or outcome-memory readiness or design;
- runtime feasibility, runtime authorization, tooling authorization, scraper authorization, API authorization, dashboard authorization, archival-tool authorization, storage authorization, automation authorization, schema authorization, test authorization, package authorization, deployment authorization, commit/push/PR authorization;
- source rights or data-rights sufficiency;
- source-system architecture or source maps;
- pressure-test discharge;
- promotion of any candidate operating control to stable;
- buyer-facing artifact authority.

## Next Authorized Step

Frames are now named in the Pressure-Test Batch Shape section, and bounded
execution authority is now supplied by
`docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`.

This plan remains the agreed commissioning shape with named frames.

Execution stays bounded as follows:

- v2 remains the controlling architecture for this scope per the acceptance decision;
- only the three named captures are authorized to execute;
- no runtime, no tooling, and no ECR/Cleaning/Judgment design work is authorized by this plan.
