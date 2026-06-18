# Judgment Spine Thesis Operating Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Operating contract for consuming, protecting, and applying the Judgment Spine thesis before future Judgment Spine work.
use_when:
  - Opening the Judgment Spine thesis before CA prompts, harness changes, case additions, or lesson-promotion decisions.
  - Checking whether proposed Judgment Spine work is thesis-aligned or drifting into implementation, proof, product, or adjacent-layer work.
  - Preserving parent Judgment Spine boundaries when using the v0.14 Judgment Harness spec or case-learning artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_thesis_v0.md
  - docs/research/judgment-spine/README.md
  - docs/research/judgment-spine/manifest_v0.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
```

- Status: WORKING_CONTRACT_V0
- Artifact type: Thesis operating contract
- Source basis: `docs/prompts/deep-thinking/judgment_spine_thesis_operating_contract_ca_prompt_v0.md`, `docs/research/judgment-spine/judgment_spine_thesis_v0.md`, Judgment Spine README and manifest, v0.14 harness index and thesis, Core Spine Data Capture/Cleaning boundary note, targeted IPF boundary sections, and Orca overlay source-loading and prompt-orchestration rules.
- Implementation authorized: no
- Runtime, automation, package, test, commit, push, PR, proof-run, or feature-planning authorized: no
- Strict readiness, validation, approval, and source-of-truth promotion claims: not proven

## Source Context Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Judgment Spine thesis operating-contract targets
  edit_permission: docs-write
  target_scope: Create the Judgment Spine thesis operating contract and narrow discovery pointers.
  dirty_state_checked: yes
  blocked_if_missing: no
source_context_status: SOURCE_CONTEXT_READY
source_context_caveat: >
  Workspace state was dirty before this artifact was written, and the Judgment
  Spine source tree was untracked. This contract can guide working-thesis lanes,
  but it does not prove acceptance, validation, readiness, approval, or
  source-of-truth promotion.
goal_fit:
  anchor_goal_fit: yes
  success_signal_fit: yes
bounded_patch_classification:
  thesis_open_next_addition: thesis_consumption_patch
  rationale: >
    Classified as a thesis patch that clarifies how future lanes consume the
    thesis, not as a navigation patch under the README/manifest/repo-map list.
```

## Purpose

This contract tells future lanes how to use the Judgment Spine thesis without turning it into a second architecture manual.

The thesis is the north-star artifact. This contract is the operating guardrail: it says how to consume the thesis, what work fits it, what work drifts, and where owner decisions or separate authorization are required.

## What The Thesis Optimizes For

The thesis optimizes Judgment Spine work for **right-sized action under evidence constraints**.

Future work should improve the surrounding judgment system: case-law-quality examples, clean decision frames, sealed blind judgments, deterministic comparisons where applicable, failure logs, reveal calibration, and guarded lesson promotion.

The scarce asset is accumulated correction. A useful lane preserves where judgment overreached, underreached, ignored evidence, relied on unsupported claims, failed to escalate, or abstained when bounded action was warranted.

## How Future Lanes Must Consume The Thesis

Before acting, a future lane should:

1. Open the parent thesis, then this contract.
2. Name the lane type: thesis governance, parent Judgment Spine architecture, v0.14 harness work, case-learning work, failure-log work, lesson-promotion work, or adjacent boundary work.
3. State the proposed output path, output mode, edit authority, and whether implementation or runtime work is authorized.
4. State the decision frame, evidence boundary, spoiler state, and reveal state when case material is involved.
5. Check the proposal against the thesis non-claims and layer boundaries before producing recommendations or patches.
6. Preserve blind/reveal separation: do not let revealed outcomes contaminate participant-facing packets or blind judgments.
7. Treat dirty, untracked, prompt-local, or thread-local material as working context unless an accepted Orca source makes it controlling authority.
8. Stop before claims of validation, readiness, approval, product proof, superiority, source-of-truth promotion, or implementation authorization unless controlling authority explicitly supports the claim.

If the proposed work cannot state its lane type, authority, source boundary, and non-claims, it is not ready to use the thesis.

## Thesis-Aligned Work

Work is thesis-aligned when it makes right-sized judgment under evidence constraints easier, stricter, or more reusable.

Aligned work includes:

- clarifying the parent Judgment Spine goal, boundaries, or non-claims;
- preparing bounded CA prompts that require the thesis before downstream work;
- selecting, indexing, or improving case-learning artifacts with explicit cutoff, spoiler, reveal, and missing-artifact status;
- preserving blind judgments, owner critiques, reveal readouts, failure events, and outcome calibration;
- refining action-band, Action Floor, Action Ceiling, overreach, underreach, escalation, abstention, and unsupported-claim categories;
- guarding lesson promotion so case-local insight does not become doctrine prematurely;
- making v0.14 harness work consume the parent thesis without treating the harness as the whole Judgment Spine;
- clarifying Data Capture / ECR / Cleaning / Judgment boundaries when a Judgment Spine lane risks crossing them.

## Thesis Drift

Work is drifting when it uses the thesis to justify a broader or different lane than the thesis supports.

Drift includes:

- turning the thesis into implementation planning, runtime architecture, package design, source maps, scrapers, tests, dashboards, automation, commits, pushes, or PRs;
- claiming Judgment Spine validation, product readiness, buyer proof, commercial readiness, feature readiness, implementation readiness, model-training readiness, or harness superiority;
- forcing all Judgment Spine material into the v0.14 harness;
- letting the v0.14 harness define parent Judgment Spine strategy by default;
- importing Data Capture Spine, Evidence Candidate Record, or Cleaning Spine ownership into Judgment Spine;
- letting Cleaning own credibility, discounting, Decision Strength, Action Ceiling, or exclusion effects;
- treating source availability, collection volume, or source capture as evidence validity;
- turning single-case insight into reusable doctrine without transfer evidence or explicit owner exception;
- using revealed outcomes to improve blind packets without labeling contamination;
- treating failure logs as promoted rules before promotion conditions are met;
- using the thesis as marketing residue instead of judgment infrastructure.

## Owner Decisions Required

Stop and request owner decision before:

- changing the long-term Judgment Spine optimization target;
- redefining layer ownership between Data Capture, Evidence Candidate Record, Cleaning, Judgment, Decision Artifact, or Outcome Memory;
- relaxing spoiler-safety, blind/reveal separation, or cutoff discipline;
- promoting a single-case lesson into reusable guidance without transfer evidence;
- asserting validation, readiness, approval, product proof, buyer proof, commercial readiness, implementation readiness, or superiority;
- authorizing implementation, runtime design, schemas, packages, tests, automation, deployment, commits, pushes, or PRs;
- replacing the v0.14 harness contract or treating another harness version as controlling;
- converting side context, adjacent context, prompt-local context, or thread-local goals into Orca source authority.

## Relationship To Other Judgment Spine Work

### Parent Judgment Spine

The parent Judgment Spine owns the long-term judgment-improvement thesis, case-law loop, spoiler safety, transferable lesson promotion, and the relationship between qualitative case learning and mechanical harness scoring.

Use the thesis to decide whether a proposed move serves right-sized action under evidence constraints. Use this contract to decide how to apply that thesis without widening the lane.

### v0.14 Judgment Harness

The v0.14 Judgment Harness is one executable-spec candidate inside the parent Judgment Spine. It owns Phase 1 harness schemas, action-band mapping, scorer formulas, runner contracts, case protocol, memorization probe behavior, and failure-event logging for that spec version.

Harness work should consume the thesis, but the harness must not swallow parent Judgment Spine work. Qualitative case learning, owner critique, reveal readouts, and provisional lessons can remain parent Judgment Spine material before they become harness fixtures.

### Case-Learning Artifacts

Case-learning artifacts should preserve the decision frame, cutoff, source or participant packet boundary, spoiler state, blind judgment, owner critique, reveal/readout, failure mode, and lesson status.

Partial cases are allowed only when their missing pieces are named directly. A case page, famous client, or consulting-firm artifact is not decision-grade by default.

### Failure Logs And Promoted Lessons

Failure logs record what went wrong. They do not automatically promote rules.

Lessons move toward reusable guidance only when they appear across cases, explain a major revealed outcome without hindsight contamination, fix a repeated operator or model failure, improve a later blind judgment or harness result, or name where the lesson does not apply. Single-case lessons remain provisional unless transfer is shown or the owner explicitly accepts the exception.

### Data Capture / ECR / Cleaning Boundaries

Judgment Spine owns inference and decision-use effects: Signal Integrity effects; Signal Use Classification; uncertainty and alternative explanations; counterevidence; discounting and exclusion; Decision Strength; Action Floor, Action Ceiling, and action-band judgment; overreach, underreach, escalation, abstention, and unsupported-claim failure modes; and reusable lessons from blind judgment versus reveal.

It must not own source acquisition, raw-signal preservation, Evidence Candidate Record receipt fields, transformation ledgers, normalization, dedupe, translation, summarization, runtime storage, source APIs, source maps, or capture operations.

When dedupe, clustering, source visibility, or preservation affects independence, credibility, uncertainty, exclusion, Decision Strength, or Action Ceiling, the effect belongs to Judgment Spine. The capture, receipt, and transformation mechanics remain outside it.

### Implementation Authorization

The thesis and this contract do not authorize implementation. They may help future prompts name implementation boundaries, but code, tests, packages, automation, runtime design, deployment, commits, pushes, and PRs require separate bounded authorization in the current turn or an accepted handoff.

## Applying The Thesis To Future Outputs

For CA prompts, require the thesis and this contract as reads, preserve source-gated method sequencing, name exact output mode and paths, and carry thread-local goals only as orientation unless accepted Orca authority says otherwise.

For harness changes, state which v0.14 file owns the changed behavior, how the change preserves parent Judgment Spine goals, and which strict claims remain not proven.

For case additions, state learnability tier, decision owner, decision question, cutoff, spoiler state, reveal state, missing artifacts, and whether the material is eligible for blind reuse.

For lesson promotion, state the promotion condition, scope of reuse, counterconditions, and whether the lesson is case-local, provisional, transferred, or owner-accepted as an exception.

For boundary decisions, state which layer owns the proposed effect and which adjacent layers must not be absorbed.

## Must Not Be Used To Claim

This contract must not be used to claim:

- Judgment Spine validation;
- v0.14 harness validation or superiority;
- buyer validation, willingness-to-pay, product readiness, feature readiness, commercial readiness, or proof-run readiness;
- implementation readiness, model-training readiness, memory compounding, or source-of-truth promotion;
- approval, acceptance, lifecycle completion, deployment status, resolver behavior, or installed behavior;
- authorization for runtime design, schemas, scrapers, automation, tests, packages, commits, pushes, PRs, or feature planning.

## Stale Or Recheck Conditions

Recheck this contract when:

- the parent Judgment Spine thesis is materially patched;
- a new harness version supersedes v0.14;
- Orca accepts a different Data Capture / ECR / Cleaning / Judgment boundary;
- a future owner decision authorizes implementation or runtime work from a Judgment Spine lane;
- lesson-promotion rules are accepted, rejected, or replaced.

## Next Authorized Step

The next authorized thesis-lane step is review or refinement of this operating contract and its narrow navigation pointers. This contract does not route to harness implementation.
