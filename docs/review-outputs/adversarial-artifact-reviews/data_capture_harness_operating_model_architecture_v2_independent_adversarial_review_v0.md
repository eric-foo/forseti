# Data Capture Harness Operating Model Architecture v2 Independent Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Independent read-only adversarial artifact review of the proposed Data Capture Harness operating-model architecture v2, conducted under explicit exclusion of the prior v2 narrow self-review as evidence.
use_when:
  - Deciding whether to owner-accept, accept-with-watch-items, patch, or reject the proposed Data Capture Harness operating-model architecture v2.
  - Checking whether v2 actually closes AR-01 (hidden reviewer authority), AR-02 (premature operating-model weight), and AR-03 ("locked now" wording).
  - Avoiding tester-examiner bias from the local v2 narrow review.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_prompt_v0.md
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
stale_if:
  - `docs/product/data_capture_harness_operating_model_architecture_v2.md` is materially revised or superseded.
  - The Data Capture obligation baseline or obligation contract is amended or superseded.
  - Owner accepts, patches, rejects, or supersedes v2.
  - A later independent adversarial review supersedes this one.
```

## Review Summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
  recommendation: accept_v2_with_watch_items
  summary: "v2 substantively closes AR-01/AR-02/AR-03 and is the strongest acceptance candidate among v0, v1, and v2; two residual material risks (capture_closure_blocker resolution authority and primitive-stability classification) should travel with acceptance as watch items or be patched first."
  findings_count: 2
  blocking_findings: []
  advisory_findings:
    - F-01: capture_closure_blocker resolution authority is undefined
    - F-02: New v2 architecture primitives not classified as stable or candidate
  prior_findings_remediated:
    - AR-01: partially_closed
    - AR-02: closed
    - AR-03: closed
  next_action: "Owner routing decision: accept v2 with the two watch items, patch v2 before acceptance, or commission another bounded review. No pressure-test execution, operator-roster execution, implementation, or runtime work is authorized by this report."
```

## Reviewer Independence Preflight

```yaml
reviewer_independence_preflight:
  did_you_author_v2: no
  did_you_author_the_v2_narrow_review: no
  are_you_in_the_same_local_thread_that_authored_v2_or_the_narrow_review: no
  have_you_read_the_v2_narrow_self_review_before_this_prompt: no
  independence_result: INDEPENDENT
```

The excluded contaminated artifact (`docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md`) was not opened, cited, summarized, or used. Its existence in the repo was observed only via directory listing for collision check.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 v2 independent adversarial review pack (per review prompt)
  edit_permission: read-only review; write only the required review report
  target_scope:
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_harness_operating_model_architecture_v2.md
    - docs/product/data_capture_harness_operating_model_architecture_v0.md
    - docs/product/data_capture_harness_operating_model_architecture_v1.md
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md
```

Method discipline: `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were reference-loaded before source reading. They were applied only after `SOURCE_CONTEXT_READY` to frame the boundary problem, decision criteria, and findings.

### Revision and hash preflight

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Branch | `main` | `main` | match |
| HEAD | `b7627d3` | `b7627d3` | match |
| v2 SHA256 | `4DE2F89A7B6B48192F9F734516BA3723D20BBB0550EF80BEBB23A6467EBEBB46` | `4DE2F89A7B6B48192F9F734516BA3723D20BBB0550EF80BEBB23A6467EBEBB46` | match |
| v0/v1 review SHA256 | `A7E0E9FA7E5DED92C3A37914E6871AC251AECF8D8ABF8B2066614755ABFF775E` | `A7E0E9FA7E5DED92C3A37914E6871AC251AECF8D8ABF8B2066614755ABFF775E` | match |
| v0 SHA256 | `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2` | `F43238167562437D26FCC5FCCFCE9152B83C8FD383AE750B9A21990089F5E3A2` | match |
| v1 SHA256 | `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF` | `BCC62DAC605ADA7BC5AA5A79482E0FBBEECC47322339DEC83E0CF234678BC8CF` | match |
| Obligation baseline SHA256 | `51D74EF534117744C5B4506393D0BA43927E636B4DA821E9A7BDE35A33728387` | `51D74EF534117744C5B4506393D0BA43927E636B4DA821E9A7BDE35A33728387` | match |
| Obligation contract SHA256 | `A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF` | `A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF` | match |
| Data/Cleaning boundary SHA256 | `0FCC5DD4048EB3B03B96F644B3EF545D82C6F5EEC212301B4C0F28E34F04B166` | `0FCC5DD4048EB3B03B96F644B3EF545D82C6F5EEC212301B4C0F28E34F04B166` | match |
| Direction-signal decision SHA256 | `1C3370C714BEF951FB3B424BC651251C63CE48AA88E680A4D1CB6CBD77775D94` | `1C3370C714BEF951FB3B424BC651251C63CE48AA88E680A4D1CB6CBD77775D94` | match |
| Output report path | must not pre-exist | clear before write | clear |

## Source-Read Ledger

| Source | Why read | Review claim supported | Status note |
| --- | --- | --- | --- |
| Current user instruction | Launched the v2 independent adversarial review prompt by path | Current turn authorizes the prompt's output contract | user-stated |
| `AGENTS.md` | Orca project entry instructions | Overlay required; docs/reviews allowed; no implementation without bounded authorization | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | Orca overlay controls project facts | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | User instruction, AGENTS, overlay, then Orca docs control; no jb import | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack budgets, preflight, dirty-state, not-proven boundaries | Bounded read pack permitted; dirty/untracked supports advisory review only | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Review report and product artifact destinations | Review report may be written under `docs/review-outputs/`; reviewed product artifacts remain read-only | modified |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial review lane, severity vocabulary, read-only boundary | Read-only adversarial artifact review may write report only; critical/major/minor allowed; no patch queue | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | `review-report` output mode and source-gated method sequence | Durable report required before courier YAML; source readiness before method application | modified |
| `.agents/workflow-overlay/communication-style.md` | Review closeout pattern and courier YAML shape | Compact courier YAML after durable report write | modified |
| `.agents/workflow-overlay/validation-gates.md` | Completion and review prompt gates | No validation/readiness/pass claim from dirty/untracked state | modified |
| `workflow-deep-thinking` | Reference-loaded reasoning discipline | Boundary problem, failure modes, decision criteria framed after source readiness | installed method copy; procedural only |
| `workflow-adversarial-artifact-review` | Reference-loaded artifact-review mechanics | Findings-first, source-backed, read-only adversarial review flow | installed method copy; procedural only |
| `docs/prompts/reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_prompt_v0.md` | Review commission, output path, exclusion of narrow self-review | Independent lane; recommendation vocabulary; finding shape | user-stated |
| `docs/product/data_capture_harness_operating_model_architecture_v2.md` | Primary review target | v2 hybridization decision, role model, lifecycle, stable vs candidate split, bloat-cut, non-claims, next step | untracked; hash matched |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md` | Prior findings (AR-01/AR-02/AR-03) as decision input only | Closure-condition language; not binding authority | untracked; hash matched |
| `docs/product/data_capture_harness_operating_model_architecture_v0.md` | Targeted comparison (search keys) | v0 second-operator framing; v0 bloat-cut review-theater item | untracked; hash matched |
| `docs/product/data_capture_harness_operating_model_architecture_v1.md` | Targeted comparison (search keys) | v1 CPOE-ARC reviewer charter; refusal-authority verbs; "locked now" | untracked; hash matched |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted baseline scope and non-claims | Baseline accepted for bounded architecture planning only; no hardening/readiness | untracked; hash matched |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | 16 obligations, six discharge states, agent allow/forbid split, forbidden Capture outputs, source-family promotion, pressure-test requirement | clean in named-path status; hash matched |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary | Capture / ECR / Cleaning / Judgment ownership must stay separate | clean in named-path status; hash matched |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Direction-signal decision and product goal | Manual harness + BT2-04 is direction signal only; product goal is buyer-trustworthy obligation-discharging inspectable failure-visible commissioned capture | untracked; hash matched |

Excluded contaminated source (per prompt): `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_narrow_adversarial_review_v0.md` — not opened, not cited, not summarized.

Other excluded-by-default sources not opened: broad `docs/review-outputs/`, broad `docs/prompts/`, broad `docs/product/`, `docs/_inbox/`, method-validation replays, proof-run packets, research corpus, implementation/runtime folders.

Dirty/untracked caveat: the worktree is broadly dirty. Modified overlay files and untracked product, prompt, and review artifacts are allowed for advisory review per the prompt. They do not support strict validation, readiness, source-of-truth promotion, product proof, or implementation authority. All target product files have hash-matched content versus the prompt's expected SHA256 pins.

## Review Boundary And Excluded Scope

This is a read-only independent adversarial artifact review. The review target is `docs/product/data_capture_harness_operating_model_architecture_v2.md`. The review compares v2 against the prior v0/v1 adversarial review findings, the accepted obligation baseline decision, the obligation contract, the data/cleaning spine boundary, the direction-signal decision, and v0/v1 themselves (targeted reads only).

Excluded scope:

- patching v2, v0, v1, the obligation contract, the manual harness, the BT2-04 dry run, the obligation baseline, the direction-signal decision, or any review artifact;
- accepting or rejecting v2 on behalf of the owner;
- designing ECR, Cleaning, Judgment, source systems, runtime, schemas, tools, dashboards, scrapers, APIs, automation, tests, packages, deployment, commits, pushes, or PRs;
- designing operator rosters, pressure-test cases, templates, forms, or execution plans;
- claiming validation, hardening, readiness, buyer proof, product readiness, source-of-truth promotion, implementation authority, or commercial readiness;
- reading or relying on the excluded v2 narrow self-review;
- emitting `patch_queue_entry` or executor-ready patch authority.

## Decision Criteria

The review applied these criteria, framed after `SOURCE_CONTEXT_READY` using `workflow-deep-thinking`:

- AR-01 closure: does v2 actually eliminate hidden reviewer approval/refusal authority, or does `capture_closure_blocker` recreate pass/fail authority under a softer name?
- AR-02 closure: did v2 cut v1's operating-model weight appropriately by distinguishing baseline obligations from pressure-test candidate controls, or did it become too thin to pressure-test?
- AR-03 closure: did v2 replace "locked now" with language that correctly attributes stability to the accepted baseline rather than to v2's own architecture?
- Counterparty pressure preservation: does v2 still expose silent omission, per-slice flattening, raw-observable loss, agent-assistance creep, hidden mode changes, and forbidden Capture outputs?
- Layer separation: does v2 keep Capture separate from ECR, Cleaning, Judgment, source maps, runtime/source systems, proof execution, operator scoring, and implementation?
- Source-family discipline: does v2 preserve source-family satellite status and the Source-Family Promotion Rule?
- Buyer-trustable output without theater: does v2 avoid turning the harness into review theater, source theater, or defensive audit armor?
- Next-step authorization scope: does v2's next step authorize only bounded planning, or does it silently authorize pressure-test execution, operator-roster execution, templates, forms, implementation, or runtime work?
- New failure modes: did v2's hybridization introduce a new architecture failure mode the prior review did not catch?
- Best acceptance candidate: is v2 better than v0 and v1 for owner acceptance, or should the owner prefer v0, v1-with-patch, another hybrid, or a reopened architecture lane?

## Findings

### F-01 - `capture_closure_blocker` resolution authority is undefined

- finding id: F-01
- severity: `major`
- phase: `correctness`
- target location or stable search key: `docs/product/data_capture_harness_operating_model_architecture_v2.md` § "Role Model" (lines 159-184) and § "Session Lifecycle" (lines 187-197); search keys `capture_closure_blocker`, `capture-owned condition`, `correction, a stop, a rerun`
- issue: v2 substantively removes the v1 reviewer's pass/fail verbs ("approve close," "refuse close," "require a fix and re-declaration") and restricts the second operator to recording two output categories (`capture_closure_blocker`, `visible_capture_limitation`). v2 states that when a `capture_closure_blocker` exists, "the reason the session cannot cleanly hand off is the capture-owned condition, not second-operator refusal authority. The capture operator records a correction, a stop, a rerun, or a re-capture posture under the architecture's stop conditions." v2 does not name who decides when a recorded blocker has been resolved enough for handoff. The Session Lifecycle places the second-operator check (step 6) immediately before categorical handoff or visible stop (step 7), but does not specify whether second-operator re-verification is required after the capture operator records remediation. The handoff rule ("only when capture-owned handoff preconditions are visibly satisfied") leaves the deciding party unnamed.
- source evidence: v2 § "Role Model" enumerates only two second-operator outputs and explicitly forbids approval/certification/validation/inclusion authority; v2 § "Session Lifecycle" sequences second-operator check before categorical handoff; v0/v1 adversarial review AR-01 minimum closure condition requires the role be bounded as a capture-visibility checker without approval/refusal authority; obligation contract § "Categorical Handoff Sufficiency" (Obligation 16) requires handoff conditions to be visibly satisfied but does not name a deciding role; data/cleaning spine boundary note assigns integrity exclusion and decision-use downgrade to Judgment, not Capture.
- impact: AR-01's verbal authority is closed, but the underlying mechanism is partially open. Operating practice during pressure testing could converge on a norm where the second operator re-verifies after recorded blockers are addressed and tacitly approves close by not recording further blockers. That recreates the hidden approval/refusal authority AR-01 was meant to eliminate, via the back door of recording authority. The risk is not at owner acceptance — v2 itself does not create the hidden authority — but at operating-practice formation during the 3-5 commissioned pressure tests.
- minimum_closure_condition: v2 or the pressure-test commissioning lane must name the closure-decision authority for a `capture_closure_blocker`. The required end state is that the deciding party (capture operator unilaterally, owner/commissioner adjudication, or another explicitly named non-second-operator authority) is identified, and the second operator's role remains limited to recording with no re-approval gate over remediation adequacy.
- next_authorized_action: Owner routing decision. The owner may (a) accept v2 with a watch item that the pressure-test commissioning lane must name closure-decision authority before pressure-test runs begin, or (b) authorize a bounded docs-only patch to v2 that names the closure-decision authority directly before acceptance.
- advisory remediation direction: a single sentence in v2's Role Model or Session Lifecycle section naming the capture operator (or the commissioner) as the deciding party for whether a recorded `capture_closure_blocker` has been addressed enough for handoff, with an explicit statement that the second operator does not re-approve. This is a wording-level addition, not a structural change. It does not require revising the obligation contract, the baseline decision, or v0/v1.

### F-02 - New v2 architecture primitives are not classified as stable or candidate

- finding id: F-02
- severity: `minor`
- phase: `friction`
- target location or stable search key: `docs/product/data_capture_harness_operating_model_architecture_v2.md` § "Stable Inherited Baseline Obligations" (lines 130-142), § "Pressure-Test Candidate Operating Controls" (lines 144-156), § "Role Model" (lines 159-184), § "Session Lifecycle" (lines 187-197); search keys `Stable Inherited`, `Pressure-Test Candidate`, `capture_closure_blocker`, `visible_capture_limitation`
- issue: v2's Stable Inherited list contains 9 items, all traceable to obligation-contract content. v2's Pressure-Test Candidate list names role count, second-operator check name/ceremony, per-obligation discharge declaration shape, exact handoff ceremony, operator-roster categories, numeric re-architecture thresholds, and minimum continuity artifact shape as mutable. But v2 also concretely specifies (a) a 5-role model (Commissioner, Capture operator, Agent assistant, Second operator / capture-visibility checker, Downstream receiver), (b) a two-output vocabulary for the second operator (`capture_closure_blocker`, `visible_capture_limitation`), and (c) a remediation vocabulary for the capture operator ("correction, a stop, a rerun, or a re-capture posture"). These primitives are part of v2's proposed architecture but the artifact does not explicitly mark them as stable inherited (they are not in the contract) or as pressure-test candidates (the candidate list mentions role count and ceremony in the abstract but the artifact reads as if the 5-role set and the two-output vocabulary are settled).
- source evidence: v2 § "Role Model" specifies 5 roles concretely and gives the second operator exactly two output categories; v2 § "Pressure-Test Candidate Operating Controls" lists role count and ceremony as mutable; obligation contract has no `capture_closure_blocker`, `visible_capture_limitation`, "correction," "stop," "rerun," or "re-capture posture" output vocabulary — these are v2 inventions; v0/v1 adversarial review AR-02 minimum closure condition requires the acceptance base to distinguish stable inherited obligations from pressure-test candidate operating controls.
- impact: Owner could accept the 5-role set and the two-output vocabulary as settled architecture rather than as candidate primitives to pressure-test. That softens the pressure-test discipline AR-02 was meant to preserve and could let v2-derived operating practice ossify before the 3-5 commissioned captures return evidence. The risk is moderate friction, not a boundary break — the primitives are coherent and grounded in the obligation contract's spirit, but their stability classification is left implicit.
- minimum_closure_condition: v2 or the pressure-test commissioning lane must explicitly classify the 5-role set, the two-output second-operator vocabulary (`capture_closure_blocker`, `visible_capture_limitation`), and the capture-operator remediation vocabulary (correction / stop / rerun / re-capture posture) as either stable inherited (traceable to baseline) or pressure-test candidate primitives. The required end state is that no v2 primitive sits in an unclassified zone between baseline-derived stability and candidate mutability.
- next_authorized_action: Owner routing decision. The owner may accept v2 with a watch item that the pressure-test commissioning lane must classify the primitives before pressure-test runs begin, or authorize a bounded docs-only patch to v2 that adds two sentences to the Pressure-Test Candidate Operating Controls section noting that the role-set and output vocabulary are candidate primitives.
- advisory remediation direction: add two clarifying sentences to v2's Pressure-Test Candidate Operating Controls section — one acknowledging that the 5-role model and the two-output second-operator vocabulary are pressure-test candidate primitives, and one acknowledging that the capture-operator remediation vocabulary is candidate. This is a wording-level addition. It does not require restructuring the architecture or reopening v1.

## Non-Findings That Matter

- AR-01 is substantively closed in label and largely in mechanism. v2 removes the v1 reviewer verbs ("approve close," "refuse close," "require a fix and re-declaration"), drops the "Independent verifier at session close" framing, drops the CPOE-ARC acronym, drops the refusal-authority charter, and restricts the second operator's outputs to recording-only categories. The residual risk is the closure-authority gap (F-01), not a relabeled refusal authority.
- AR-02 is closed. v2 explicitly distinguishes the Stable Inherited Baseline Obligations list (9 items, all contract-traceable) from the Pressure-Test Candidate Operating Controls list (7 items named as mutable until 3-5 pressure tests return evidence). The residual is a classification-coherence friction (F-02), not a failure to draw the line.
- AR-03 is closed. v2 replaces "locked now" with "inherited from the current accepted baseline for this proposed architecture" and adds "they are not newly validated by this artifact and are not hardened by this artifact." This correctly attributes stability to the accepted baseline and not to v2's own architecture status.
- v2 preserves counterparty pressure on the known failure modes. Stop Conditions And Re-Architecture Triggers explicitly cover silent omission (`hidden failure was hidden instead of recorded`, `forbidden Capture output appeared`), per-slice flattening (`per-slice posture required by the contract collapsed into a rollup`), raw-observable loss (`raw observable was replaced by paraphrase or summary that loses source language, structure, or modality where it carries signal`), agent-assistance creep (`agent assistance crossed a forbidden verb`), hidden mode changes (`mode change occurred but was not made visible`), and forbidden Capture outputs (named explicitly). The counterparty mechanism shifted from reviewer refusal to capture-owned stop conditions, but the failure-mode coverage is preserved.
- v2 keeps Capture separate from ECR, Cleaning, Judgment, source maps, runtime/source systems, proof execution, operator scoring, and implementation. The Handoff Boundary section names what must be inspectable without designing ECR; the Bloat-Cut Queue excludes detailed field schemas, key shapes, IDs, receipt structures, ledgers, forms, data models, source maps as harness core, source-family playbooks as core, runtime tooling references, ECR field architecture, Cleaning transformations, Judgment rules, credibility labels, discounting, exclusion, Signal Use Classification, Decision Strength, Action Ceiling, proof-run/buyer-proof/validation/readiness/commercial claims, operator scoring, certification, training curriculum, performance rubrics, detailed templates, triage instructions, and re-architecture of ECR/Cleaning/Judgment intake.
- v2 preserves the source-family satellite boundary. The Source-Family Satellite Boundary section keeps source-family content satellite by default and names the archive/history per-slice posture and recapture-relationship invariant as the only currently promoted source-family invariant. Promotion routes (two non-overlapping source families surface the same gap, or owner sign-off on a specific invariant claim) are preserved verbatim.
- v2's Next Authorized Step bounds the next move to a narrow read-only adversarial review of v2. It explicitly states that no implementation, runtime, ECR, Cleaning, Judgment, source-system, scraper, API, dashboard, archive tooling, storage, schema, test, package, deployment, commit, push, PR, buyer-facing appendix, source-family registry, pressure-test execution, or operator-roster execution is authorized by the artifact. Owner acceptance of v2 would accept the target operating architecture for pressure testing without authorizing pressure-test execution.
- v2's Non-Claims section is comprehensive. It explicitly denies owner acceptance of v2, validation, hardening, readiness, source-of-truth promotion beyond the accepted obligation baseline, Data Capture Spine completion, final harness acceptance, manual harness validation, BT2-04 source validity / credibility / admissibility / representativeness / decision usefulness, all ECR/Cleaning/Judgment readiness and design, buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, commercial readiness, all runtime/tooling/source-system authorizations, source rights or data-rights sufficiency, source-system architecture or source maps, pressure-test discharge against 3-5 real commissioned captures, and supersession of v0 or v1 unless and until owner acceptance. It also denies that subagent agreement, model agreement, perspective consensus, review recommendation, fixture count, and lack of P0/P1 findings constitute validation or acceptance.
- The hybridization did not introduce new ECR/Cleaning/Judgment leakage. The Handoff Boundary lists what must be inspectable categorically without naming ECR fields. The Stop Conditions explicitly block discharge-state justification from importing credibility, integrity, discounting, exclusion, Signal Use, Decision Strength, or Action Ceiling vocabulary. Forbidden Capture outputs (credibility labels, integrity classifications, discounting decisions, exclusion decisions, Signal Use Classification, Decision Strength, Action Ceiling, semantic dedupe or clustering effects, Cleaning transformations, final ECR field architecture, source-quality scores, source maps as core architecture, runtime implementation plans) are preserved from the obligation contract verbatim in spirit.
- The Direction Signal product goal (buyer-trustworthy, obligation-discharging, inspectable, layer-disciplined, failure-visible commissioned capture) is preserved implicitly via v2's Failure And Limitation Visibility section, the Obligation-Discharge Visibility Commitment, the layer separation, and the second-operator capture-visibility check. v2 does not restate the product goal as a header but the architectural commitments are aligned with it.

## Comparison To v0 And v1

This comparison is decision-relevant for the recommendation between accept_v2, prefer_v0, prefer_v1_with_patch, or reopen.

- v0 vs v2: v0 already treated the second-operator role as a control surface without naming a refusal charter (v0 § Role model lines 357-360). v2 strengthens this by restricting the second operator to two recording-only output categories and explicitly forbidding approval/certification/validation/inclusion/admissibility/credibility/usefulness/scoring authority. v0 lacked v1's per-obligation discharge visibility commitment, the stronger bloat-cut queue, and the explicit named failure-mode coverage. v2 keeps those v1 strengths. v0 is not preferable as-is because it is thinner on operating-failure-mode counterparty coverage than v2.
- v1 vs v2: v1's CPOE-ARC name, refusal-authority charter ("approves close, requires a fix and re-declaration, or escalates to a stop condition"), and "locked now" invariants language are all removed in v2. v1's per-obligation discharge visibility commitment (the right architecture-level invariant per the v0/v1 review's Non-Findings) is preserved in v2. v1's stronger bloat-cut queue is carried forward and expanded. v1 is not preferable as-is because it carries the AR-01 and AR-03 defects the prior review flagged. v1-with-patch would essentially be v2.
- Hybridization soundness: v2's bounded approach (v1 base, import v0's softer second-operator framing, add the inherited-vs-candidate split, replace "locked now") is the smallest patch that closes AR-01/AR-02/AR-03 without losing v1's strengths or v0's safety. The two residual findings here (F-01, F-02) are wording-level and pressure-test-commissioning-level, not architecture-level.
- Acceptance discipline: owner acceptance of v2 (with or without watch items) authorizes the target operating architecture for pressure testing but not pressure-test execution, operator-roster execution, runtime, or any implementation lane. Acceptance of v0 or v1 would carry the AR-01/AR-02/AR-03 risks the prior review flagged. Reopening architecture would discard the v2 closure work without source-grounded reason to do so.

## Not-Proven Boundaries

This review does not prove:

- owner acceptance of v2 or any other architecture proposal;
- validation, hardening, readiness, source-of-truth promotion, buyer proof, repeatability proof, product readiness, feature readiness, implementation readiness, or commercial readiness;
- Data Capture Spine completion;
- ECR readiness, Cleaning readiness, Judgment readiness, or any downstream lane design;
- runtime feasibility, tooling feasibility, source-system feasibility, source rights, or data-rights sufficiency;
- pressure-test discharge against 3-5 real commissioned captures;
- mandatory remediation, patch authority, or executor-ready instructions;
- that the second operator's resolution authority is correctly bounded by operating practice — that is a pressure-test learning, not an architecture decision provable in advance;
- that the v2 primitives (5-role set, two-output vocabulary, capture-operator remediation vocabulary) survive 3-5 commissioned pressure tests without revision;
- that the manual harness, BT2-04 dry run, or any prior fixture set constitutes validation of v2.

This review also does not prove a negative about the excluded v2 narrow self-review. That artifact was not read by this reviewer in this run and its content is not used as evidence. Whether it agrees, disagrees, or surfaces additional findings is unknown to this report.

## Final Recommendation

`accept_v2_with_watch_items`

v2 is the best acceptance candidate among v0, v1, and v2. It substantively closes AR-01 (verbal authority removed, output restricted, refusal-authority charter dropped), closes AR-02 (explicit inherited-vs-candidate split), and closes AR-03 ("locked now" replaced with correctly attributed inherited-baseline language). It preserves v1's strengths (per-obligation discharge visibility commitment, strong bloat-cut queue, named failure-mode counterparty coverage) and imports v0's safer second-operator framing.

Two residual material risks should travel with acceptance as watch items, or be patched into v2 before acceptance:

1. F-01: the pressure-test commissioning lane must name the closure-decision authority for `capture_closure_blocker` before pressure-test runs begin, so that operating practice does not re-create hidden second-operator approval authority via the recording mechanism.
2. F-02: the pressure-test commissioning lane must classify the v2-introduced primitives (5-role set, two-output second-operator vocabulary, capture-operator remediation vocabulary) as stable inherited or pressure-test candidate before pressure-test runs begin, so the pressure-test discipline AR-02 protects is preserved.

Owner may instead authorize a bounded docs-only patch to v2 that addresses F-01 and F-02 before acceptance. Either path is consistent with the review-lane authority of this report.

The smallest next authorized step is an owner routing decision among: (a) accept v2 with the two watch items carried forward into pressure-test commissioning; (b) authorize a bounded docs-only patch to v2 addressing F-01 and F-02, then accept; (c) commission another bounded review; or (d) reject v2 and reopen architecture. This report does not select among these on the owner's behalf.

## Review-Use Boundary

These findings and this recommendation are decision input only. They are not approval, validation, readiness, source-of-truth promotion, mandatory remediation, patch authority, architecture execution, implementation authority, pressure-test commissioning authority, operator-roster authorization, runtime authorization, tooling authorization, ECR/Cleaning/Judgment design authorization, or buyer-facing authorization. Owner acceptance, patch authorization, pressure-test commissioning, and any implementation/runtime work require separate explicit authorization. This review does not itself patch v2, v0, v1, the obligation contract, the obligation baseline decision, the direction-signal decision, the manual harness, the BT2-04 dry run, or any other artifact.
