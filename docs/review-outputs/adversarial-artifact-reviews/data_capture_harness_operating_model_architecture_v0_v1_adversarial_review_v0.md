# Data Capture Harness Operating Model Architecture v0/v1 Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Read-only adversarial artifact review comparing the v0 and v1 proposed Data Capture Harness operating-model architecture artifacts before owner acceptance.
use_when:
  - Deciding whether to accept, patch, hybridize, or reject the proposed Data Capture Harness operating-model architecture.
  - Checking whether v1 CPOE-ARC creates review theater, hidden Judgment authority, ECR/Cleaning leakage, or premature operating-model weight.
  - Preserving v0 strengths that should travel into any accepted v1-derived architecture.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_prompt_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v1.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md
stale_if:
  - Either v0 or v1 architecture artifact is materially revised or superseded.
  - A later owner decision accepts, patches, rejects, or hybridizes v0/v1.
  - The Data Capture obligation baseline or obligation contract is amended or superseded.
```

## Findings

### AR-01 - Reviewer checkpoint can become hidden approval/refusal authority

- Phase: `correctness`
- Severity: `major`
- Target: `v1`
- Location or stable search key: `Adversarial reviewer / second-operator`; `approves close, requires a fix and re-declaration`
- Issue: v1 correctly tries to counter silent omission, rollups, agent creep, and raw-observable loss, but the reviewer role is currently framed with too much closure authority. The role may "refuse session close," "approve close," and "require a fix and re-declaration." Even though v1 says this is not credibility judgment, the verbs create an operating path where reviewer pass/fail becomes hidden approval, mandatory remediation, or a quasi-Judgment gate.
- Evidence: v1 names CPOE-ARC and adds "a per-obligation discharge visibility commitment at session close" plus an adversarial reviewer with explicit refusal authority. The role is an "Independent verifier at session close" and can refuse close on several conditions; the session lifecycle then says the reviewer either approves close, requires a fix and re-declaration, or escalates to a stop condition. The controlling obligation contract permits Capture to record visible facts and limitations, but forbids credibility labels, exclusion decisions, Signal Use Classification, Decision Strength, Action Ceiling, Cleaning transformations, final ECR architecture, source-quality scores, source maps as core architecture, and runtime implementation plans. The Data Capture / Cleaning boundary note assigns integrity exclusion and decision-use downgrade to Judgment, not Capture.
- Impact: This is the main owner-acceptance risk in v1. CPOE-ARC could become review theater or hidden Judgment if operators treat reviewer approval as capture validation, source usefulness, admissibility, inclusion, or downstream readiness. It also risks blurring Orca artifact-review vocabulary with the product-method second-operator role.
- Minimum closure condition: The accepted architecture must state that the second-operator checkpoint can only record capture-owned closure blockers or visible non-blocking limitations. It must not approve sources, certify quality, decide inclusion/admissibility/use, require downstream Judgment changes, authorize patches, or create acceptance/readiness. The role should be bounded as a capture-visibility checker, not a general adversarial reviewer.
- Next authorized action: Owner may authorize a bounded docs patch or hybridization pass that keeps v1's stronger obligation-discharge checkpoint while importing v0's simpler "control surface, not primary architecture and not a Judgment lane" framing.

### AR-02 - v1 overweights the operating model before real pressure tests

- Phase: `friction`
- Severity: `major`
- Target: `v0_vs_v1`
- Location or stable search key: `CPOE-ARC`; `Core Operating Model commits to nine surfaces`; `operator-roster and pressure-test commissioning decision`
- Issue: v1 is stronger than v0, but it also hardens the language surface before the 3-5 commissioned pressure tests the obligation contract requires for hardening. The named CPOE-ARC architecture, "locked now" invariants, minimum role set, nine operating surfaces, refusal charter, and next-step operator-roster decision create a heavier acceptance target than the evidence supports.
- Evidence: The accepted baseline authorizes bounded architecture planning but does not claim the contract is hardened, validated, product-ready, runtime/tooling-authorized, implementation-ready, or commercially ready. The obligation contract says it should not be treated as hardened until tested against 3-5 real commissioned captures and says pressure tests should update the contract only after failures are compared. v1 itself says pressure-testing remains the path to hardening, but its target name and role architecture read more final than v0's simpler "contract-pinned obligation-discharge operating envelope."
- Impact: An owner could accept process weight instead of accepting the smallest architecture needed for pressure testing. The pressure test could then become compliance with CPOE-ARC rather than learning whether the operating model is too heavy, too light, or mis-shaped.
- Minimum closure condition: Before owner acceptance, the acceptance base must distinguish stable inherited obligations from pressure-test candidate operating controls. It should preserve v1's obligation-discharge and per-slice safeguards, but keep role count, reviewer checkpoint naming, discharge-exposure form, and operator-roster details mutable until pressure-test evidence returns.
- Next authorized action: Owner may authorize a v0/v1 hybrid artifact that uses v1 as the stronger base while carrying forward v0's lighter acceptance surface and explicit owner-routing first step.

### AR-03 - "locked now" wording overclaims the current architecture status

- Phase: `correctness`
- Severity: `minor`
- Target: `v1`
- Location or stable search key: `Core invariants (locked now)`
- Issue: v1 says its core invariants are "locked now" because they are already obligation-contract core and pressure-test evidence is not required to confirm them. That is too strong for a proposed architecture artifact whose controlling baseline is accepted only for bounded operating-model architecture planning and whose own non-claims deny hardening and validation.
- Evidence: v1 status is `PROPOSED_ARCHITECTURE_V0` and says owner acceptance is required before it becomes controlling. The baseline decision states the obligation surface is stable enough for architecture planning, not validated, hardened, or production-proven. The obligation contract requires pressure testing before hardening.
- Impact: The phrase can create avoidable confusion between inherited baseline obligations and accepted/hardened architecture commitments. It is unlikely to invalidate v1, but it weakens source discipline in an artifact meant to be accepted or patched.
- Minimum closure condition: The accepted artifact should replace "locked now" with language such as "inherited from the current accepted baseline for this proposed architecture" and preserve that later pressure-test evidence can amend the architecture or obligation contract.
- Next authorized action: Include this wording cleanup in any bounded v1 patch or v0/v1 hybridization pass.

## Source Readiness

`SOURCE_CONTEXT_READY`

The required review prompt, overlay sources, review targets, and controlling product-method sources were loaded sufficiently for this read-only adversarial review. No conditional expansion was needed: the findings are supported by the required targets and controlling sources. No implementation folders, `_inbox`, broad product folders, broad prompt folders, research corpus, proof packets, or method-validation replay material were read.

Preflight receipt:

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 Data Capture Harness v0/v1 adversarial review pack
  edit_permission: read-only review; write only this review report
  target_scope:
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_harness_operating_model_architecture_v0.md
    - docs/product/data_capture_harness_operating_model_architecture_v1.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Revision and hash preflight:

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Branch | `main` | `main` | match |
| HEAD | `b7627d3` | `b7627d3` | match |
| v0 SHA256 | `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2` | `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2` | match |
| v1 SHA256 | `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF` | `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF` | match |
| Report path collision | must not pre-exist | did not pre-exist | clear |

## Source-Read Ledger

| Source | Why read | Review claim supported | Status note |
| --- | --- | --- | --- |
| Current user instruction | Launched the review prompt by path | Current turn authorizes prompt execution under its output contract | user-stated |
| `AGENTS.md` | Orca project entry instructions | Overlay required; docs/reviews allowed; no implementation without bounded authorization | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Orca overlay controls project facts and missing authority must be reported | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | User instruction, AGENTS, overlay, then Orca docs control; no `jb` import | modified |
| `.agents/workflow-overlay/source-loading.md` | Source pack, dirty-source, and not-proven rules | Bounded read pack; dirty/untracked sources may support advisory review but not strict readiness or validation | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Review report and product artifact destinations | Review report may be written under `docs/review-outputs/`; reviewed product artifacts remain read-only | modified |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial review lane and read-only boundary | Read-only adversarial artifact review may write report only; no patch queue or patch execution | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | `review-report` output mode and source-gated method sequence | Durable report required before courier YAML; source readiness before applying review method | modified |
| `.agents/workflow-overlay/communication-style.md` | Review closeout pattern | Compact courier YAML after durable report write | modified |
| `.agents/workflow-overlay/validation-gates.md` | Completion and review prompt gates | No validation/readiness/pass claim from dirty/untracked source state | modified |
| `.agents/workflow-overlay/product-proof.md` | Product-proof non-claims | No buyer proof, readiness, repeatability proof, or product validation claims | untracked |
| `workflow-deep-thinking` | Reference-loaded reasoning discipline | Framed boundary problem and failure modes after source readiness | installed method copy; procedural only |
| `workflow-adversarial-artifact-review` | Reference-loaded artifact-review mechanics | Findings-first, source-backed, read-only adversarial review flow | installed method copy; procedural only |
| `docs/prompts/reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_prompt_v0.md` | Review commission and output path | v1 presumptive candidate; compare v0/v1; exact recommendation vocabulary | untracked |
| `docs/product/data_capture_harness_operating_model_architecture_v0.md` | Reviewed target | v0's simpler contract-pinned operating envelope and safer second-operator framing | untracked; hash matched |
| `docs/product/data_capture_harness_operating_model_architecture_v1.md` | Reviewed target | v1 CPOE-ARC target, reviewer checkpoint, role/lifecycle, deferred implications, next step | untracked; hash matched |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted baseline and non-claims | Baseline accepted for bounded architecture planning only; no hardening/readiness/runtime authority | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | Six discharge states, categorical handoff, agent allow/forbid split, forbidden Capture outputs, source-family promotion, pressure-test requirement | clean in named-path status |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Direction-signal decision | Manual harness and BT2-04 dry run are direction signal only; harness must maximize obligation discharge, inspectability, failure visibility, and layer separation | untracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary | Capture, ECR, Cleaning, Judgment, artifact, and outcome-memory ownership must stay separated | clean in named-path status |

Dirty/untracked caveat: the worktree is broadly dirty. Modified overlay files and untracked prompt/product sources are allowed by the review prompt for advisory review. They do not support strict validation, readiness, acceptance, source-of-truth promotion, product proof, or implementation authority.

## Review Boundary And Excluded Scope

This was a read-only adversarial artifact review. It compared v0 and v1 as proposed product artifacts. It did not patch either architecture artifact, accept an architecture, create a patch queue, execute pressure tests, design runtime/source systems, design ECR/Cleaning/Judgment, create schemas, stage, commit, push, or open a PR.

Excluded scope:

- implementation, runtime, source-system, scraper, API, dashboard, archive-tool, screenshot, storage, schema, package, test, deployment, commit, push, or PR work;
- ECR field architecture, Cleaning transformations, Judgment rules, Signal Use Classification, Decision Strength, Action Ceiling, credibility, exclusion, discounting, or source-quality scoring;
- source-family playbooks or satellite registry creation;
- patch execution against v0, v1, the obligation contract, the manual harness, or the BT2-04 dry run.

## Comparison Frame

The real review question is not whether v1 is more detailed than v0. It is whether v1 is safe enough to become the owner-accepted operating-model architecture, or whether its added reviewer checkpoint, role surface, and pressure-test routing need to be patched or hybridized with v0's lighter model first.

Decision criteria used:

- Preserve the accepted obligation baseline without mutating it.
- Keep Capture separate from ECR, Cleaning, Judgment, runtime, source maps, and implementation.
- Make every obligation discharge state visible without converting completeness into fake success.
- Preserve raw observables, per-slice posture, source limits, failures, not-attempted states, and recapture relationships.
- Avoid review theater and hidden Judgment through the reviewer checkpoint.
- Avoid hardening the operating model before 3-5 real commissioned pressure tests.
- Preserve source-family satellite discipline and the promotion rule.

## Non-Findings That Matter

- v1 is materially stronger than v0 on source-backed evidence mode. It uses delegated-three-subagent evidence, records source-readiness receipts, and explicitly states that subagent agreement is not validation or acceptance. That does not prove correctness, but it is stronger than v0's local fallback.
- v1 does not directly design ECR, Cleaning, Judgment, runtime, source maps, schemas, or tools. Its leakage risk is mostly role-authority and operating-weight leakage, not explicit downstream design content.
- v1 preserves the source-family satellite rule in text and correctly names the archive/history per-slice invariant as the only currently promoted source-family invariant.
- v0 is not preferable as-is. It is simpler and safer in several surfaces, but it lacks v1's delegated evidence, explicit per-slice counterweights, and stronger operational counterparty to known harness failures.

## v0 Strengths Worth Preserving

- v0 frames the target as a "contract-pinned obligation-discharge operating envelope" without naming a heavyweight acronym or treating a reviewer checkpoint as the architecture's brand.
- v0 states that the second operator or reviewer is a control surface, not the primary architecture and not a Judgment lane.
- v0's next authorized step is a clean owner routing decision: accept, patch, reject, or review the proposed architecture. This is safer before moving into operator-roster or pressure-test commissioning.
- v0 explicitly names review/audit theater as a bloat-cut item: operators should not optimize for pass language instead of obligation discharge.

## v1 Strengths Worth Preserving

- v1 is the stronger base because it uses delegated-three-subagent evidence and records source-readiness for directional, adversarial, and grounding lanes.
- v1 explicitly confronts the known failure modes from the manual harness direction signal: state collapse, rollups that should be per-slice, raw-observable paraphrase, agent-assistance creep, checklist theater, ECR/Cleaning/Judgment leakage, and runtime/tool gravity.
- v1's per-obligation discharge visibility commitment is the right architecture-level invariant, so long as its artifact form stays deferred and its review checkpoint does not become validation.
- v1's bloat-cut queue is stronger than v0's and should travel forward: it excludes field schemas, data models, source-family playbooks, runtime tooling, ECR sketches, Cleaning transformations, Judgment rules, scoring, training, templates, automation diagrams, and ECR/Cleaning/Judgment intake redesign.

## Not-Proven Boundaries

This review does not prove:

- owner acceptance of v0, v1, or a hybrid;
- architecture validation, hardening, product readiness, feature readiness, implementation readiness, commercial readiness, buyer proof, or repeatability proof;
- Data Capture Spine completion;
- runtime feasibility, tooling feasibility, source-system feasibility, source rights, or data-rights sufficiency;
- ECR readiness, Cleaning readiness, Judgment readiness, or any downstream lane design;
- that the delegated subagents in v1 are independently verifiable from this review report beyond v1's own source-readiness receipts;
- that any finding is mandatory remediation or patch authority.

## Advisory Recommendation

`hybridize_v0_v1_before_acceptance`

v1 should remain the presumptive base because it is more source-grounded, more explicit about known operating failure modes, and more protective against per-slice flattening and downstream leakage. It should not be accepted as-is. Before owner acceptance, v1 should be patched or hybridized with v0's simpler second-operator framing and cleaner owner-routing posture so the reviewer checkpoint cannot become hidden approval, hidden Judgment, or a heavyweight process proxy for pressure-test evidence.

## Smallest Next Authorized Step

The smallest next authorized step is an owner routing decision: authorize a bounded docs-only v0/v1 hybridization patch, explicitly accept v1 with the findings unresolved, reject v1 in favor of v0, or commission another read-only review. This report does not itself authorize patches, architecture acceptance, pressure-test execution, implementation, runtime, ECR, Cleaning, Judgment, source-family registry work, commits, pushes, or PRs.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, readiness, source-of-truth promotion, mandatory remediation, patch authority, architecture execution, implementation authority, or runtime/tooling authorization.
