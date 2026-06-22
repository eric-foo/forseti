# Data Capture Obligation Baseline Decision Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the proposed Data Capture obligation-baseline decision before owner acceptance.
use_when:
  - Reading the adversarial findings on the proposed `ACCEPT_BASELINE` decision.
  - Checking whether harness/dry-run/synthesis classifications in the decision artifact survived adversarial scrutiny.
  - Routing the owner's accept/patch/reject choice on the Data Capture obligation baseline.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/operating_model/data_capture_obligation_baseline_decision_v0.md
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
branch_or_commit: main@b7627d3 with dirty/untracked workspace sources
stale_if:
  - The reviewed decision artifact is materially revised.
  - Owner accepts, rejects, or patches the Data Capture obligation-baseline decision.
  - The obligation contract or direction-signal decision is superseded.
  - A later adversarial review of this decision supersedes this report.
```

- Review lane: adversarial artifact review.
- Review target: `docs/product/data_capture_obligation_baseline_decision_v0.md`.
- Review prompt: `docs/prompts/reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_prompt_v0.md`.
- Output mode: review-report.
- Reviewer edit permission: read-only except writing this report.
- Patch queue authorized: no.
- Patch execution authorized: no.
- Harness architecture authorized: no.
- Runtime/source-system/ECR/Cleaning/Judgment work authorized: no.
- Created: 2026-05-28.

## 1. Review Summary

Recommendation: `accept_with_friction`.

Findings count: 3 (all advisory, minor severity).

Blocking findings: none.

Advisory findings:

- `AR-01` — Source-Family Promotion satisfaction route for the archive/history patch is implicit in the decision artifact, and would benefit from one explicit sentence connecting `ACCEPT_BASELINE` to owner sign-off under the contract's promotion rule.
- `AR-02` — The obligation contract's own "hardening" criterion (3-5 real commissioned captures) is distinct from "baseline-stable for later architecture planning"; the decision artifact uses "baseline" to mean the weaker claim, but the distinction could be one line clearer.
- `AR-03` — The decision artifact's `ACCEPT_BASELINE` rests on a chain through the synthesis and the synthesis review rather than on a standalone adversarial review of the obligation contract; that chain dependency is not surfaced in the artifact and is closed only by reviews that read the contract directly, such as this one.

Prior findings remediated: none in scope (the artifact is the proposed decision under first review).

Next action: route this review to the owner. The owner may accept the baseline decision as-is, accept with the optional clarifications above, accept with a bounded patch to surface the chain dependencies more explicitly, or reject and request reframing. No ECR / Cleaning / Judgment / runtime / harness-architecture work should begin from this artifact without separate authorization.

## 2. Source Readiness

`SOURCE_CONTEXT_READY`.

Preflight receipt:

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 bounded baseline-decision review pack
  edit_permission: read-only review plus review-report write only
  target_scope:
    - docs/product/data_capture_obligation_baseline_decision_v0.md
  report_path:
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  worktree_branch: main
  worktree_head: b7627d3
  dirty_state_allowance: dirty and untracked named sources in scope as working evidence; do not authorize acceptance from dirty state alone.
```

Compact source ledger:

| Source | Why read | Claim supported | Status note |
| --- | --- | --- | --- |
| Current review prompt | Controlling task, lane bindings, output path, severity vocabulary, recommendation vocabulary | Adversarial artifact review of the proposed baseline decision is authorized; report-only output | user-stated |
| `AGENTS.md` | Orca authority and overlay binding | Docs-only review; no implementation; overlay wins for Orca facts | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | Overlay sections own concrete Orca facts | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | No `jb` or generic authority imported into Orca review | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack discipline, dirty-state and not-proven boundaries | Dirty/untracked working evidence may support advisory findings but cannot prove acceptance, validation, or readiness | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Review report role binding | Adversarial review report goes under `docs/review-outputs/adversarial-artifact-reviews/`; reviewer is read-only except for the report write | modified |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial artifact review lane rules | Findings-first; severity labels are finding-priority only; review-use boundary required | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-Gated Method Contract; review-report output mode | REFERENCE-LOAD then APPLY; YAML-only chat is valid only after durable report write | modified |
| `.agents/workflow-overlay/communication-style.md` | Adversarial review summary YAML shape | Compact `review_summary` block used after durable write | modified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | Header uses `retrieval_only` and avoids forbidden status fields | clean in named-path status |
| `.agents/workflow-overlay/product-proof.md` | Product-proof non-claims | No buyer validation, willingness-to-pay, repeatability, or commercial proof claimed by the decision under review | untracked |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Review target | The artifact proposes `ACCEPT_BASELINE` with bounded non-claims and explicit owner-acceptance gating | untracked |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Direction-signal demotion context | Manual harness + BT2-04 accepted as demoted direction signal only; harness patches deferred; architecture deferred | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Baseline candidate | Contract defines 16 core obligations, capture modes, captured-but-unusable, forbidden outputs, source-family promotion rule, pressure-test requirement | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Layer architecture | Data Capture records visible facts; layer split preserved; runtime deferred | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md` | Sublane status and recheck recipe | Pressure-test sublane is "stable enough for advisory use, subject to owner acceptance"; obligation-contract sublane is the only sublane this packet stabilizes | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md` | Fixture coverage and patch incorporation evidence | Five fixtures landed; one core defect (archive/history) patched narrowly; satellite guidance accumulated and bounded | clean in named-path status |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer ownership and core-vs-satellite rules | Data Capture owns capture/preservation; ECR/Cleaning/Judgment own their own layers; promotion rule for source-family heuristics | clean in named-path status |
| `docs/product/core_spine_v0_product_contract.md` | Core Spine product rule and frozen primitives | Decision Frame mandatory; Evidence Unit inspectable; non-implementation boundary | modified |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | Evidence Unit standard and production sequence | Capture supports downstream inspectability without performing Cleaning, Judgment, or ECR | clean in named-path status |
| `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md` | Synthesis adversarial review | Recommendation `ACCEPT_AS_ADVISORY_INPUT`; 5 P2/P3 clarity findings; no required patch | clean in named-path status |
| `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md` | Manual harness + BT2-04 dry-run adversarial review | Verdict `PATCH_BEFORE_NEXT_DRY_RUN`; 4 P2 findings (harness vocabulary, harness H-09 rollup, CS-08 paraphrase, dry-run H-09 rollup); all classified as harness-template or dry-run-execution defects, not obligation-contract defects | untracked |

Dirty/untracked source caveats:

- Many target and supporting sources are dirty or untracked at HEAD `b7627d3`. This is allowed by the prompt's dirty-state scope. Findings here are advisory critique grounded in repo-visible evidence.
- Dirty/untracked status does not by itself promote any artifact to source-of-truth, validation, readiness, owner-accepted, or implementation-authorized status, and this report inherits that limit.
- Material source gaps for this review: none. The named source pack was sufficient to answer the review questions.

Method invocation:

- `workflow-deep-thinking`: REFERENCE-LOADed before source loading; APPLIED after `SOURCE_CONTEXT_READY` to frame the boundary problem (whether the contract is stable enough as a controlling product-method obligation surface for later operating-model architecture, distinct from "hardened for production capture" or "validated"), decision criteria (correct issue classification, no overclaim, dirty-state discipline, downstream boundary), and failure modes (misclassification, implicit promotion-rule discharge, leakage into runtime/ECR/Cleaning/Judgment authorization).
- `workflow-adversarial-artifact-review`: REFERENCE-LOADed before source loading; APPLIED after `SOURCE_CONTEXT_READY` to produce findings. Phase 1 (correctness) and Phase 2 (friction) attack surfaces were tested before findings were listed.

## 3. Commission And Target

Commission: read-only adversarial artifact review of the proposed Data Capture obligation-baseline decision. Maximally adversarial about decision-relevant failure modes inside that scope; advisory critique only; no formal validation, readiness, or patch-execution authority.

Target artifact: `docs/product/data_capture_obligation_baseline_decision_v0.md`.

Explicit non-targets:

- The obligation contract itself is not the primary target of this review. It is read as a backing source to test whether the decision artifact's claims about it survive scrutiny.
- The full-fixture synthesis is not the primary target. It is read as cited evidence.
- The manual harness and BT2-04 dry run are not the primary targets. They are read as cited evidence.
- ECR, Cleaning, Judgment, runtime, source-system, scraper, API, dashboard, storage, schema, test, package, deployment, commit, push, PR, and harness operating-model architecture work are out of scope.

This review does not re-review the full Data Capture Spine, the synthesis, or the harness/BT2-04 pair. It does not architecture-plan the harness. It does not patch any artifact.

## 4. Decision Criteria

The review applied these criteria from the prompt, framed through deep-thinking discipline:

1. Is `ACCEPT_BASELINE` justified by the artifact's cited sources, or is a contract-level defect hidden that should force `PATCH_BEFORE_ACCEPTANCE` or `REJECT_BASELINE`?
2. Did the artifact correctly classify manual-harness and BT2-04 P2 findings as harness-template or dry-run-execution defects rather than baseline-contract blockers?
3. Did the artifact handle full-fixture synthesis adversarial findings as synthesis-clarity or optional-hardening rather than baseline blockers?
4. Does the artifact rely on dirty or untracked working evidence in a way that weakens owner acceptance, source-of-truth promotion, validation, or readiness claims?
5. Does the downstream implication stay tight enough to prevent a later harness architecture lane from drifting into runtime, ECR, Cleaning, Judgment, source systems, scrapers, APIs, dashboards, storage, automation, schemas, tests, packages, commits, pushes, or PRs?
6. Does the artifact preserve the accepted direction-signal demotion and avoid letting BT2-04 become controlling architecture?
7. Does the artifact overclaim validation, readiness, approval, buyer proof, commercial proof, implementation authority, or source-of-truth promotion?

Failure modes named in advance:

- Misclassifying a contract-level defect as harness-level.
- Treating dirty/untracked working evidence as acceptance authority.
- Letting `ACCEPT_BASELINE` smuggle in stronger claims (validation, readiness, implementation authority, ECR/Cleaning permission).
- Implicit discharge of the contract's Source-Family Promotion rule for the archive/history patch.
- Permitting a later architecture lane to interpret `ACCEPT_BASELINE` as runtime authorization.
- Underplaying Milwaukee depth or pressure-test/commissioned-capture distinction.

## 5. Findings

All findings are advisory and minor. None block owner acceptance. Each finding states the minimum closure condition for clarity remediation (if the owner chooses to apply one) and the next authorized action.

### AR-01 — Source-Family Promotion satisfaction route is implicit (minor; correctness)

- Phase: correctness.
- Location: Issue Classification table row "Archive/history and recapture rollup defect found during Unity fixture pressure testing"; Decision Rationale paragraph two ("That defect was patched narrowly in the current obligation contract"); Non-Claims and Next Authorized Step.
- Source authority used: obligation contract section "Source-Family Promotion" ("Promotion to core requires one of: comparison across at least two non-overlapping source families; or owner sign-off for one specific invariant claim"); synthesis review finding AR-04 ("Source-family-promotion rule satisfaction route for the archive patch is implicit rather than explicit"); synthesis Section 4 ("not proven across a broader archive corpus or accepted as final"); fixture synthesis Section 10 archive/history core bullet.
- Issue: The decision artifact treats the Unity-derived archive/history patch as "Baseline-level, already patched before this decision. No remaining blocker." However, under the obligation contract's Source-Family Promotion rule, the patch's elevation to a core obligation depends on either cross-family comparison or owner sign-off. The cross-family observation from Kubernetes is partial (Kubernetes did not independently force the patch), and owner sign-off is precisely what `ACCEPT_BASELINE` would discharge. The decision artifact does not connect those dots explicitly.
- Evidence: The synthesis explicitly defers archive-patch sufficiency to owner acceptance, and the synthesis review's AR-04 was surfaced as a clarity finding rather than a contract defect because the synthesis's not-proven boundary partially mitigates it. The decision artifact inherits the not-proven boundary in its Non-Claims section ("owner acceptance" is listed) but does not say that `ACCEPT_BASELINE`, if granted, is also the owner sign-off step under the Source-Family Promotion rule for the archive patch.
- Impact: A reader scanning Issue Classification might treat the archive patch as fully discharged into core. In fact, the patch is in core text but its source-family-promotion route is one fixture (Unity) plus partial cross-family observation (Kubernetes) plus reasoning, awaiting owner acceptance. The current artifact does not surface that owner acceptance of this decision is part of how the Source-Family Promotion rule gets satisfied for the archive patch. This is friction, not invalidity: the artifact correctly defers acceptance to the owner, and the contract's promotion rule explicitly accepts owner sign-off for a specific invariant as a route.
- Minimum closure condition: The decision artifact (or owner-acceptance follow-on) makes the promotion route explicit: archive/history per-slice posture and recapture-relationship rule reached core through Unity-driven patch + Kubernetes cross-family observation + generalization reasoning, with owner acceptance of this decision serving as the contract's owner-sign-off prong for the specific archive/history invariant.
- Next authorized action: owner decision. The owner may accept the decision as-is given the contract's promotion rule explicitly allows owner sign-off, accept with an optional one-line clarification surfacing the promotion route, or request a small bounded patch to make the linkage explicit. No patch queue is authorized by this review.
- Recommended advisory direction: insert one sentence in Decision Rationale or Downstream Implication noting that owner acceptance of `ACCEPT_BASELINE` includes owner sign-off for the archive/history invariant under the Source-Family Promotion rule, with Unity + Kubernetes as the cross-family evidence the rule otherwise allows. No core obligation change; no patch queue.

### AR-02 — "Baseline" vs "hardened" distinction is correct but compressed (minor; friction)

- Phase: friction.
- Location: "Real Decision" section ("whether the current Data Capture obligation contract is stable enough to become the baseline that a later Data Capture Harness operating-model architecture lane may design against"); "Baseline Under Review" section paragraph after the file list ('Here, "baseline" means a controlling product-method obligation surface for a later harness operating-model architecture lane, if owner accepted'); Decision Rationale.
- Source authority used: obligation contract section "Pressure-Test Requirement" ("This v0 contract should not be treated as hardened until tested against 3-5 real commissioned captures"); synthesis Section 4 ("These were product-method pressure tests, not buyer Decision Frames or ECR-ready captures"); pressure-test usage note Section 1 ("Overpowered enough for an owner acceptance decision as the Data Capture obligation baseline candidate. That is an engineering-quality classification, not a formal lifecycle claim").
- Issue: The obligation contract names its own "hardened" criterion as testing against 3-5 real commissioned captures. The five planned fixtures are setup pressure tests, not real commissioned captures. The decision artifact uses "baseline" to mean a weaker stability claim than "hardened" — appropriate, but the distinction is not stated in those terms inside the artifact.
- Evidence: The Real Decision section correctly says "stable enough to become the baseline that a later... lane may design against." Baseline Under Review correctly says "controlling product-method obligation surface... if owner accepted." It does not, however, contrast this with the contract's own hardened criterion or explicitly note that the available evidence is product-method pressure-test fixtures rather than real commissioned captures.
- Impact: A future reader could read `ACCEPT_BASELINE` as a stronger lifecycle claim than the contract's own hardening criterion, even though the artifact's Non-Claims section already disclaims validation, source-of-truth promotion, and similar. The risk is friction, not invalidity, because the artifact's Non-Claims section is comprehensive and the Baseline Under Review paragraph already gives a tight definition.
- Minimum closure condition: The decision artifact (or the owner-acceptance follow-on note) states once that "baseline" here is distinct from the contract's "hardened" criterion: hardened requires 3-5 real commissioned captures; baseline allows later operating-model architecture planning against the obligation surface that pressure tests showed mostly held, with owner acceptance as the gate.
- Next authorized action: owner decision. Owner may accept as-is given Non-Claims already disclaims validation and hardening implicitly, or accept with the optional clarification.
- Recommended advisory direction: one sentence in Baseline Under Review or Patch Requirements If Any, clarifying that the contract's "hardened" criterion remains pending future real commissioned captures and that this decision does not promote the contract to hardened, only to baseline-stable for later architecture planning.

### AR-03 — Chain-of-inference behind `ACCEPT_BASELINE` not surfaced (minor; correctness)

- Phase: correctness.
- Location: Decision Rationale section (four numbered pillars); Source Readiness ledger.
- Source authority used: synthesis review section 1 ("Reviewed artifact: docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md"); manual harness + BT2-04 review section 3 ("Pair under review: ... harness ... dry run"); decision artifact "Decision Rationale" paragraph three ("the adversarial review of the full-fixture synthesis found no required patch before advisory use").
- Issue: The decision artifact's confidence that the obligation contract is stable enough as a baseline rests on three chains: (1) the synthesis says the contract mostly held; (2) the synthesis review found no required patch on the synthesis; (3) the harness/BT2-04 review classified its findings as harness/dry-run-level. The obligation contract itself has not been the primary target of a standalone adversarial review prompt outside this baseline-decision review. The decision artifact does not state this chain dependency.
- Evidence: The synthesis adversarial review's review header explicitly names the synthesis (not the contract) as the reviewed artifact and lists "target_artifact: docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md". The harness/BT2-04 review explicitly names the harness and dry run as the pair under review. Neither names the obligation contract as primary target.
- Impact: A future reader could read the four-pillar Decision Rationale as implying the contract has been independently adversarially reviewed. In fact, the contract has been pressure-tested by the fixture set and read in scope of the synthesis/harness/BT2-04 reviews; this review (the one writing this report) is the first review that reads the contract directly in scope of a contract-level decision. This dependency is closed by the current review, but the decision artifact itself does not say it.
- Minimum closure condition: The decision artifact (or owner-acceptance follow-on) notes once that the obligation contract has been read in scope of the synthesis review, the harness/BT2-04 review, the pressure-test synthesis itself, and this baseline-decision adversarial review, but has not been the primary target of an isolated contract adversarial review. Owner acceptance is the gate, and this baseline-decision review serves as the contract-target read.
- Next authorized action: owner decision. Owner may accept as-is, accept with the optional clarification, or commission a separate isolated contract adversarial review before granting acceptance.
- Recommended advisory direction: optional one-paragraph note in Decision Rationale clarifying which adversarial reviews touched the contract and which did not, plus a statement that this baseline-decision review reads the contract directly. No new artifact is required.

## 6. Non-Findings / Confirmed Boundaries

These high-risk attack surfaces were tested and no material defect was found. They are recorded so the owner can see the surface that was checked, not only what produced findings.

1. **Manual harness and BT2-04 P2 finding classification.** Each of the four P2 items from the harness/BT2-04 review was tested against the obligation contract:
   - H-P2-01 (harness discard-reason vocabulary `post_window_for_current_commission` vs `post_cutoff_for_at_cutoff_use`): the obligation contract does not bind a discard-reason vocabulary in core; this is a harness-template detail. Correctly classified as harness-level.
   - H-P2-02 (harness H-09 rollup design does not force per-slice rows): contract section "Archive / Historical Posture" already requires per-slice posture when "cutoff, deletion, edit, cache, prior-window, archive-only, migration, fallback, or visibility-shift risk is load-bearing" and multiple states coexist, and "A rollup archive posture is allowed only when it does not hide a failed, degraded, unavailable, not-attempted, fallback, migrated, or conflicting source state." The harness template did not encode this operationally. The contract has the rule; the harness must operationalize it. Correctly classified as harness-level.
   - D-P2-01 (CS-08 raw observable is paraphrase-only): contract section "Raw Observable Preservation" already requires "preserve what the source showed or said, not only Orca's summary" and warns that "summaries... do not by themselves preserve the raw observable when source meaning depends on thread context, modality, layout, edits, related replies, or visible source structure." The dry run violated this existing rule. Correctly classified as dry-run execution-level.
   - D-P2-02 (dry-run H-09 run-level archive/timing rollups): same as H-P2-02 — the contract requires per-slice; the dry run rolled up. Correctly classified as dry-run execution-level.

   The decision artifact's classification table handles all four correctly. No P2 finding from the harness/BT2-04 review escalates to a baseline-contract defect.

2. **Full-fixture synthesis adversarial finding classification.** The synthesis review's five P2/P3 findings (AR-01 bundled-offer cross-family phrasing; AR-02 patch-incorporation framing; AR-03 "Held" wording vs partial discharge; AR-04 archive promotion route implicit; AR-05 satellite section restates core) were tested against the obligation contract. All five concern phrasing or sectional framing inside the synthesis artifact, not contract obligations. Each is correctly classified in the decision artifact's Issue Classification table as "synthesis clarity," "optional hardening," or equivalent. The contract's own section structure (16 core obligations, capture modes, captured-but-unusable, forbidden outputs, source-family promotion, pressure-test requirement, rejected patterns, non-claims, open design knobs) was not strained by any of the five findings.

3. **Direction-signal demotion preserved.** The decision artifact's Issue Classification rows for manual harness and BT2-04 P2 items list them as harness-level / dry-run execution-level / harness/dry-run optional hardening. The Decision Rationale paragraph four states explicitly: "the manual harness plus BT2-04 dry run was explicitly demoted to a direction signal... They do not show that the obligation contract itself would misdirect future harness architecture." This is consistent with the direction-signal decision's status `ACCEPTED_DIRECTION_SIGNAL_DECISION_V0` and its explicit demotion language. BT2-04 is not treated as controlling architecture or as validation.

4. **Non-claims comprehensive.** The decision artifact's Non-Claims section disclaims: owner acceptance, validation, source-of-truth promotion, Data Capture Spine completion, final harness acceptance, manual harness validation, BT2-04 source validity / credibility / admissibility / representativeness / decision usefulness, ECR / Cleaning / Judgment readiness or design, Signal Use Classification / Decision Strength / Action Ceiling readiness, buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, commercial readiness, runtime feasibility, source rights / data-rights sufficiency, source-system architecture, source maps, scraper/API/dashboard/storage/automation/schema/test/package/deployment/commit/push/PR authorization. The artifact also notes that "Review consensus, model agreement, fixture count, and lack of P0/P1 findings are not treated as validation or acceptance." This closes the most common overclaim paths.

5. **Dirty-source discipline.** The source ledger correctly marks each source by status. The artifact's "Material source gaps" line states: "Dirty or untracked named sources remain working evidence only; they do not prove owner acceptance, source-of-truth promotion, validation, readiness, or implementation authority." No strict claim is anchored to dirty-source authority in the artifact.

6. **Downstream implication scope.** The Downstream Implication section explicitly limits the later harness architecture lane: "must not treat this baseline decision as runtime, ECR, Cleaning, Judgment, source-system, scraper, API, dashboard, storage, automation, schema, test, package, implementation, deployment, commit, push, or PR authority." The scope is tight enough to prevent later architecture from leaking into runtime/ECR/Cleaning/Judgment authority on the strength of this decision alone. The artifact also states that "Until owner acceptance occurs, this artifact is a recommendation only," which prevents premature treatment of the decision as accepted authority.

7. **Retrieval header hygiene.** The decision artifact's retrieval header uses `retrieval_header_version: 1`, `artifact_role: Product artifact`, `authority_boundary: retrieval_only`, and includes only the triggered fields `open_next` and `stale_if`. No forbidden field (approval status, validation status, readiness status, lifecycle state, deployment/install/resolver/publication state, edit permission, executor authorization, review verdict, source-of-truth promotion) appears in the header. The header is bounded to retrieval value.

8. **Pressure-test usage note alignment.** The pressure-test usage note explicitly says the packet "stabilizes one sublane: Obligation-contract pressure testing" and "does not finish the whole Data Capture Spine." The decision artifact respects this scope. It does not claim the broader Data Capture Spine is complete; it claims only that the obligation contract is stable enough as baseline for later operating-model architecture, subject to owner acceptance.

9. **Captured-but-unusable boundary preserved.** Neither the obligation contract nor the decision artifact converts captured signals into credibility, discounting, exclusion, Signal Use Classification, Decision Strength, or Action Ceiling claims. The contract's "Forbidden Outputs From Capture" section is intact, and the decision artifact does not authorize crossing this line.

## 7. Residual Risks

These risks remain after this review and are not eliminated by `ACCEPT_BASELINE`:

- The contract's own "hardened" criterion (3-5 real commissioned captures) is not yet satisfied. Baseline acceptance authorizes architecture planning, not capture-production hardening. Future real commissioned captures may surface defects that require contract patches.
- Raw source-level capture sufficiency for Milwaukee remains not proven. Full public-sector raw package text was not captured in the Milwaukee fixture; the fixture used a reveal readout. Future Milwaukee-style cases may need a deeper fixture.
- Multimodal/dynamic-page capture is in the contract as an obligation but is not pressure-tested by a dedicated fixture. The synthesis lists this as open.
- The Source-Family Promotion rule's owner-sign-off prong is the route by which `ACCEPT_BASELINE` discharges the archive/history patch promotion; the decision artifact does not state this linkage explicitly (see AR-01).
- The decision artifact relies on a chain through the synthesis and synthesis review; the contract is not the primary target of a standalone adversarial review prompt (see AR-03). This review reads the contract directly and surfaces no contract-level defect, but a separate isolated contract adversarial review is allowable if the owner wants tighter chain-independence.
- A later harness operating-model architecture lane must enforce its own scope; this baseline decision states the boundary but cannot itself prevent scope drift in a later prompt. The owner-acceptance step should re-state the boundary or rely on the next prompt to bind it.
- Dirty/untracked status of several named sources (notably the manual harness, BT2-04 dry run, harness/BT2-04 adversarial review report, and direction-signal decision artifact) means strict claims about those sources remain "not proven." This review's findings, like the decision artifact itself, are advisory under dirty-source discipline.
- Owner acceptance is the gate. Until granted, `ACCEPT_BASELINE` is a recommendation only.

## 8. Review-Use Boundary

This read-only adversarial artifact review is decision input only. Its findings and non-findings are not:

- owner acceptance, rejection, or patching of the Data Capture obligation baseline decision;
- formal validation of the obligation contract, the synthesis, the harness, the dry run, or any cited artifact;
- readiness, completion, hardening, or source-of-truth promotion for any artifact;
- mandatory remediation or patch authority over any artifact;
- executor-ready remediation handoff;
- authorization for harness operating-model architecture, ECR, Cleaning, Judgment, runtime, source-system, scraper, API, dashboard, storage, automation, schema, test, package, deployment, commit, push, or PR work;
- buyer proof, willingness-to-pay, repeatability, product/feature/implementation/commercial readiness, or any product-proof claim.

Severity labels (`critical`, `major`, `minor`) are finding-priority indicators only. They do not by themselves create approval, rejection, validation, readiness, mandatory remediation, or patch authority. The recommendation `accept_with_friction` is decision input to the owner; only the owner can accept, reject, or patch the proposed baseline decision. Only a separately authorized Orca decision, patch lane, or execution lane can convert the advisory findings AR-01..AR-03 into source edits, formal verdicts, or executor-ready handoff.

This report does not edit, patch, or mutate the decision artifact, the obligation contract, the synthesis, the harness, the BT2-04 dry run, or any other artifact. It writes only this durable report under `docs/review-outputs/adversarial-artifact-reviews/` per the bound review-report output mode.

Next authorized step: route this review to the owner. The owner may accept the decision as-is (the recommendation), accept with one or more of the optional clarifications above, accept with a bounded patch to surface chain dependencies, or reject and request reframing. No downstream architecture, ECR, Cleaning, Judgment, runtime, or implementation work should begin from the baseline decision without owner acceptance, regardless of this review.
