# Data Capture Obligation Baseline Decision Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Prompt for deciding whether the current Data Capture obligation contract should be accepted, patched before acceptance, or rejected as the baseline for later harness operating-model architecture.
use_when:
  - Opening the upstream Data Capture obligation-baseline decision lane.
  - Deciding whether harness architecture may later plan against the current obligation contract.
  - Separating obligation-contract baseline defects from defects in the demoted manual harness direction signal.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - orca/product/spines/capture/core/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - The Data Capture obligation contract is materially revised, superseded, accepted, or rejected by owner decision.
  - The Data Capture Harness Direction Signal decision is superseded.
  - A later obligation-baseline decision prompt supersedes this prompt.
```

- Prompt target: Claude Opus or another source-grounded product decision lane.
- Downstream output mode: `file-write`.
- Downstream target artifact: `docs/product/data_capture_obligation_baseline_decision_v0.md`.
- Created: 2026-05-28.
- Implementation authorized: no.
- Runtime/source-system design authorized: no.
- ECR/Cleaning/Judgment design authorized: no.
- Harness architecture planning authorized by this prompt: no.
- Source-of-truth promotion claimed: no.

## Prompt Construction Notes

This is a product decision prompt, not a patch prompt and not an architecture
prompt. Its job is to force a clean owner-decision surface around the Data
Capture obligation baseline before any harness operating-model architecture
lane opens.

The prompt is intentionally strict about one failure mode: defects in the
demoted manual harness and BT2-04 dry run are evidence about use under pressure,
but they are not automatically defects in the obligation baseline. The receiver
must decide whether each issue is contract-level, harness-level, fixture-level,
or downstream-lane-level before recommending `PATCH_BEFORE_ACCEPTANCE`.

## Paste-Ready Prompt

```text
<role>
You are Claude Opus working for Orca as an independent product-method decision
architect. Your task is to decide whether Orca should accept, patch before
acceptance, or reject the current Data Capture obligation baseline candidate
before any Data Capture Harness architecture lane proceeds.
</role>

<operating_mode>
Reason carefully from the provided Orca sources. Return source-grounded
conclusions, decisive rationale, assumptions, source gaps, and non-claims.

Do not expose private chain-of-thought. If reasoning is complex, summarize the
decision logic and the evidence that drove it.

This is a docs-only product decision lane. It is not patch execution, not
harness architecture planning, not ECR design, not Cleaning design, not Judgment
design, and not runtime/tooling design.
</operating_mode>

<orca_authority>
Use the Orca source hierarchy:
1. Current user instruction for this prompt.
2. Orca `AGENTS.md`.
3. Orca overlay under `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow methods only for generic mechanics, not Orca facts.

Do not import `jb` rules, paths, lifecycle mechanics, product policy, validation
habits, handoff rules, or artifact roles as Orca authority.
</orca_authority>

<current_context>
Orca has accepted a directional reset for the Data Capture Harness lane:

- The current manual Data Capture harness plus BT2-04 dry run is demoted to
  `Data Capture Harness Direction Signal v0`.
- That direction signal remains useful real product-method pressure evidence.
- It is not the controlling architecture, not validation, not final harness
  authority, and not a reason to silently overfit future harness architecture to
  BT2-04.
- The next upstream question is the Data Capture obligation baseline: should
  the current obligation contract become the baseline that later harness
  operating-model architecture may design against?

Your job is not to assume the baseline is good because prior artifacts sounded
positive, and not to reject it because the manual harness has P2 defects. Decide
which source claims actually bear on the obligation baseline itself.
</current_context>

<repo_preflight>
Before source analysis, record an `orca_start_preflight` receipt:

orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: custom S3/S4 bounded Data Capture obligation-baseline pack
  edit_permission: docs-write for the target product artifact only
  target_scope:
    - docs/product/data_capture_obligation_baseline_decision_v0.md
  dirty_state_checked: yes/no
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md

Check the worktree state for named target/source files. Modified or untracked
sources may be used as current working evidence when explicitly named here, but
they do not prove source-of-truth promotion, validation, readiness, or acceptance
unless the current user instruction or controlling source explicitly grants that
status.
</repo_preflight>

<required_source_loading>
If you have filesystem access, read the sources below before answering. If you
do not have filesystem access, return `SOURCE_CONTEXT_INCOMPLETE` and ask for
the smallest source capsule needed to answer. Do not substitute generic product
or architecture intuition for Orca source grounding.

Control and operating sources:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/product-proof.md`

Product and boundary sources:
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`

Baseline candidate sources:
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`

Direction-signal pressure evidence:
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`

Optional expansion only if a concrete source gap could change the decision:
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/decisions/turn_08_product_thesis_v0.md`

Default exclusions:
- Do not read `docs/_inbox/`.
- Do not bulk-load all product, prompt, review, research, workflow, or replay
  files.
- Do not read implementation folders or create implementation scope.
- Do not widen into ECR, Cleaning, Judgment, runtime, automation, source-system,
  scraper, API, dashboard, storage, schema, tests, package, or deployment work.
</required_source_loading>

<source_readiness_gate>
Before producing the decision, declare one of:
- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

If ready, include a compact source-read ledger: source, why read, and what claim
it supports.

If incomplete, name missing sources, what claims cannot be made, and the
smallest complete source capsule needed. Do not write the target product
artifact if the missing source could change the baseline decision.
</source_readiness_gate>

<task>
Create a docs-only product decision artifact at:

`docs/product/data_capture_obligation_baseline_decision_v0.md`

The artifact must answer:

Should Orca accept the current Data Capture obligation contract as the Data
Capture obligation baseline candidate for later harness operating-model
architecture, patch it before acceptance, or reject it?

Use exactly one primary decision:
- `ACCEPT_BASELINE`
- `PATCH_BEFORE_ACCEPTANCE`
- `REJECT_BASELINE`

Important: If the current launch instruction does not explicitly say the owner
is accepting the decision, write the artifact as a recommendation or proposed
decision and state that owner acceptance remains required. Use an accepted
status only when the current owner instruction explicitly authorizes acceptance.
</task>

<decision_criteria>
Evaluate the baseline candidate against these criteria:

- Does it define what commissioned Data Capture must make visible without
  smuggling in ECR, Cleaning, Judgment, Decision Strength, or Action Ceiling?
- Does it preserve Orca's product goal: buyer-trustworthy, obligation-
  discharging, inspectable, layer-disciplined, failure-visible commissioned
  capture?
- Does it cleanly separate capture obligations from capture modes, source-family
  playbooks, source maps, scrapers, dashboards, and runtime tooling?
- Does it require explicit obligation states such as `met`, `partial`,
  `blocked`, `unavailable_by_source`, `not_applicable`, and `not_attempted`
  rather than allowing silent omission?
- Does it preserve raw observable, source identity where knowable, source
  visibility/access limits, decomposed timing, archive/history posture, related
  context, cutoff posture, recapture semantics, and blocker/failure visibility?
- Do the fixture synthesis and adversarial review expose contract-level defects
  that must be patched before acceptance?
- Do the manual harness / BT2-04 P2 defects reveal defects in the obligation
  baseline itself, or only in the demoted direction-signal harness artifact?
- Is the baseline stable enough for a bounded future harness operating-model
  architecture lane without implying validation, product readiness, buyer proof,
  or implementation authority?
</decision_criteria>

<decision_rules>
Choose `ACCEPT_BASELINE` only if:
- the obligation contract itself is stable enough to serve as the controlling
  baseline for later harness operating-model architecture;
- remaining issues are harness-level, fixture-level, wording-level, optional
  hardening, or downstream-lane issues rather than baseline blockers;
- the artifact clearly limits acceptance to a baseline decision, not validation,
  readiness, source-of-truth promotion, or implementation authorization.

Choose `PATCH_BEFORE_ACCEPTANCE` if:
- a defect in the obligation contract would misdirect future harness
  architecture, allow layer leakage, hide capture failure, overfit one source
  family, or weaken buyer-trustable inspection;
- the needed patch can be named as a contract-level requirement without
  executing the patch in this lane.

Choose `REJECT_BASELINE` only if:
- the obligation contract is wrong at the product-method level, not merely
  incomplete, unaccepted, or imperfect;
- it would point Orca toward source theater, source-volume metrics, runtime
  tooling, source maps, ECR/Cleaning/Judgment leakage, or bespoke consulting
  evidence.

Do not choose `PATCH_BEFORE_ACCEPTANCE` merely because the demoted manual harness
needs patches. First classify each issue as baseline-level, harness-level,
fixture-level, downstream-level, or optional hardening.
</decision_rules>

<hard_boundaries>
Do not:
- patch the obligation contract;
- patch the manual harness or BT2-04 dry run;
- architecture-plan the Data Capture Harness;
- design ECR fields, Cleaning transformations, Judgment rules, Decision
  Strength, Action Ceiling, runtime systems, source systems, scrapers, APIs,
  dashboards, storage, automation, schemas, tests, packages, commits, pushes, or
  PRs;
- claim buyer validation, willingness to pay, paid pilot conversion, product
  readiness, feature readiness, implementation readiness, commercial readiness,
  formal validation, deployment, install, resolver status, source-of-truth
  promotion, or owner acceptance unless a controlling Orca source or current
  owner instruction explicitly binds that claim;
- treat review consensus, model agreement, or lack of objections as validation;
- treat the demoted direction signal as controlling architecture.
</hard_boundaries>

<target_artifact_contract>
Write a Markdown artifact with this structure:

1. Title
   - `# Data Capture Obligation Baseline Decision v0`

2. Retrieval Header
   - Use the Orca retrieval header shape from
     `.agents/workflow-overlay/retrieval-metadata.md`.
   - `artifact_role: Product artifact`
   - `authority_boundary: retrieval_only`
   - Include `open_next` only for genuinely useful controlling sources.

3. Status And Decision
   - State whether the artifact is proposed/recommended or owner-accepted.
   - State exactly one primary decision:
     - `ACCEPT_BASELINE`
     - `PATCH_BEFORE_ACCEPTANCE`
     - `REJECT_BASELINE`

4. Source Readiness
   - `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
   - Compact source ledger and material source gaps.

5. Real Decision
   - Name the upstream decision and why it must precede harness architecture.

6. Baseline Under Review
   - Identify the obligation contract and related synthesis/review artifacts.
   - State what "baseline" means and what it does not mean.

7. Product Criteria
   - Summarize the criteria used to judge the baseline.

8. Issue Classification
   - Classify material issues as:
     - baseline-level
     - harness-level
     - fixture-level
     - downstream-level
     - optional hardening
   - Explain which issues do or do not affect the baseline decision.

9. Decision Rationale
   - Explain why the selected decision follows from the sources.

10. Patch Requirements If Any
   - If `PATCH_BEFORE_ACCEPTANCE`, list required contract-level patch
     requirements only.
   - Do not execute the patch.
   - If `ACCEPT_BASELINE` or `REJECT_BASELINE`, state why no patch list is being
     executed in this artifact.

11. Downstream Implication
   - State whether a later Data Capture Harness operating-model architecture
     lane may plan against this baseline.
   - Preserve limits: no runtime, ECR, Cleaning, Judgment, source-system, scraper,
     API, dashboard, storage, automation, schema, tests, package, or implementation
     authority.

12. Non-Claims
   - List strict claims not made.

13. Next Authorized Step
   - Name the smallest next action allowed after this artifact.
</target_artifact_contract>

<artifact_write_rules>
If `docs/product/data_capture_obligation_baseline_decision_v0.md` already
exists:
- read it first;
- do not silently overwrite it;
- either update only with explicit owner authorization or create the next
  versioned filename and report the collision.

After writing, return a compact chat summary with:
- artifact path;
- selected decision;
- whether owner acceptance is claimed or still required;
- any source gaps or dirty/untracked-source caveats;
- next authorized step.

Do not stage, commit, push, or open a PR unless separately instructed.
</artifact_write_rules>

<self_check>
Before finalizing, check the artifact against these failure modes:

- treating a demoted harness P2 as a baseline blocker without classification;
- accepting the baseline while silently claiming validation, readiness, or
  source-of-truth promotion;
- rejecting the baseline because it is not a harness architecture;
- patching or rewriting the obligation contract inside this decision lane;
- smuggling ECR, Cleaning, Judgment, runtime, scraper, API, dashboard, storage,
  automation, schema, tests, or package design into the artifact;
- turning "baseline" into buyer proof, product readiness, or commercial proof;
- letting BT2-04 shape become the controlling architecture;
- widening source loading into broad Orca history instead of the bounded
  obligation-baseline pack.
</self_check>
```
