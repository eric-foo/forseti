# Data Capture Obligation Baseline Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Accepted owner decision that the current Data Capture obligation contract is the baseline for later bounded harness operating-model architecture.
use_when:
  - Checking the accepted Data Capture obligation baseline before later harness operating-model architecture.
  - Separating Data Capture obligation-baseline defects from manual-harness or dry-run defects.
  - Checking the non-claims attached to the accepted Data Capture obligation baseline.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md
  - orca/product/spines/capture/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
stale_if:
  - A later owner decision amends, rejects, or supersedes this accepted decision.
  - A later patch supersedes this version.
  - The Data Capture obligation contract is materially revised or superseded.
  - The Data Capture Harness Direction Signal decision is superseded.
  - A later Data Capture obligation-baseline decision supersedes this artifact.
```

## Status And Decision

Status: `ACCEPTED_BASELINE_DECISION_V0`.

Primary decision: `ACCEPT_BASELINE`.

This artifact records owner acceptance of the current Data Capture obligation
contract as the Data Capture obligation baseline for later bounded harness
operating-model architecture.

Owner decision recorded 2026-05-28:

```text
Owner decision: ACCEPT_BASELINE.

I accept `docs/product/data_capture_obligation_baseline_decision_v0.md` as
patched as the Data Capture obligation-baseline decision for Orca.

This acceptance includes owner sign-off for the archive/history per-slice
posture and recapture-relationship invariant under the obligation contract's
Source-Family Promotion rule.

This acceptance authorizes a future bounded Data Capture Harness
operating-model architecture lane to plan against the current obligation
contract baseline.

This does not claim the obligation contract is hardened, validated,
product-ready, source-of-truth-promoted beyond this decision, buyer-proven,
ECR/Cleaning/Judgment-ready, runtime/tooling-authorized,
implementation-ready, or commercially ready.
```

Post-review patch note: the read-only adversarial review of the pre-acceptance
version of this decision recommended `accept_with_friction`, found no blocking
findings, and identified three minor clarifications. This patched version
surfaces those clarifications and is now owner-accepted under the decision
above.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 bounded Data Capture obligation-baseline pack
  edit_permission: docs-write for the target product artifact only
  target_scope:
    - docs/product/data_capture_obligation_baseline_decision_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Compact source ledger:

| Source | Why read | Claim supported | Status note |
| --- | --- | --- | --- |
| Current user instruction | Launched the prompt artifact and bounded the lane | Docs-only decision artifact requested | user-stated |
| Current owner decision | Accepted the patched decision artifact | `ACCEPT_BASELINE`; owner sign-off for the archive/history invariant; bounded future harness operating-model architecture may plan against this baseline | user-stated |
| `AGENTS.md` | Orca project authority and overlay requirement | Docs-only default and no implementation without explicit scope | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | Orca overlay wins for Orca facts | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and missing-source rules | No `jb` or generic authority imported | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack, preflight, dirty-state, and not-proven rules | Dirty/untracked named sources may be working evidence but do not prove acceptance or promotion | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact role and write boundary | `docs/product/` is a docs-write product artifact destination | modified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | Header uses `retrieval_only` and avoids forbidden status fields | clean in named-path status |
| `.agents/workflow-overlay/product-proof.md` | Product-proof non-claims | No buyer validation, readiness, or commercial proof claimed | untracked |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Current status of manual harness plus BT2-04 dry run | Direction signal is accepted as demoted input, not architecture or validation | untracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary | Data Capture records capture facts and limits; ECR, Cleaning, and Judgment remain separate | clean in named-path status |
| `docs/product/core_spine_v0_product_contract.md` | Core Spine product rule and non-goals | Decision-frame discipline, Evidence Unit (EvidenceUnit) inspectability, and no runtime/platform drift | modified |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | Evidence Unit and downstream inference boundary | Capture must support inspectability but not perform Judgment | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Data Capture architecture | Capture is the obligation; mode is subordinate; commissioned capture only | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Baseline candidate under review | Current contract defines obligations, discharge states, layer limits, and non-claims | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md` | Current pressure-test interpretation | Contract appears stable enough for an owner baseline decision, subject to acceptance | clean in named-path status |
| `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md` | Fixture-synthesis evidence | Planned fixtures exposed one material core defect, already patched narrowly | clean in named-path status |
| `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md` | Adversarial review of the synthesis | No required patch before advisory use; only optional clarity findings | clean in named-path status |
| `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md` | Direction-signal pressure evidence | P2 findings are harness or dry-run execution defects, not baseline-contract blockers | untracked |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md` | Pre-acceptance adversarial review of this decision | `accept_with_friction`; no blocking findings; AR-01 through AR-03 clarifications are incorporated here | untracked |

Material source gaps: none for this decision. Optional expansion sources were
not read because the required pack was sufficient to decide the obligation
baseline question. Dirty or untracked named sources remain working evidence
only; owner acceptance is supplied by the current owner decision, not by dirty
or untracked source status. This acceptance does not prove validation,
hardening, readiness, implementation authority, or source-of-truth promotion
beyond this decision.

## Real Decision

The upstream decision is whether the current Data Capture obligation contract
is stable enough to become the baseline that a later Data Capture Harness
operating-model architecture lane may design against.

This decision must precede harness architecture because the harness should
implement and operationalize capture obligations. If the obligation baseline is
wrong, the harness architecture would encode the wrong layer boundary, hide
capture failures, overfit a source family, or drift into ECR, Cleaning,
Judgment, source maps, or runtime design.

## Baseline Under Review

The baseline candidate is:

```text
docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Related evidence:

- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md`
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`

Here, "baseline" means a controlling product-method obligation surface for a
later bounded harness operating-model architecture lane. It does
not mean validation, Data Capture closure, source-of-truth promotion, ECR
readiness, Cleaning readiness, Judgment readiness, buyer proof, runtime
feasibility, implementation readiness, or permission to build tooling.

Baseline is also weaker than the obligation contract's own hardening criterion.
The contract is not hardened until tested against future real commissioned
captures. This decision concerns whether the obligation surface is stable
enough for later harness operating-model architecture planning, not whether the
contract is validated, hardened, or production-proven.

## Product Criteria

The baseline was judged against whether it:

- Defines what commissioned Data Capture must make visible without smuggling in ECR, Cleaning, Judgment, Decision Strength, or Action Ceiling.
- Preserves buyer-trustworthy, obligation-discharging, inspectable, layer-disciplined, failure-visible commissioned capture.
- Separates capture obligations from capture modes, source-family playbooks, source maps, scrapers, dashboards, and runtime tooling.
- Requires explicit obligation states: `met`, `partial`, `blocked`, `unavailable_by_source`, `not_applicable`, and `not_attempted`.
- Preserves raw observables, source identity where knowable, visibility/access limits, decomposed timing, archive/history posture, related context, cutoff posture, recapture semantics, and blocker/failure visibility.
- Treats fixture and review evidence as pressure evidence, not validation.
- Classifies manual harness and BT2-04 defects before treating them as baseline defects.
- Stays stable enough for future architecture without implying validation, readiness, buyer proof, or implementation authority.

## Issue Classification

| Issue | Classification | Baseline effect |
| --- | --- | --- |
| Archive/history and recapture rollup defect found during Unity fixture pressure testing | Baseline-level, already patched before this decision | No remaining blocker. The current contract now requires per-slice or per-locator posture when mixed source states would otherwise be hidden. Owner acceptance in this decision also serves as owner sign-off for this specific archive/history invariant under the contract's Source-Family Promotion rule, backed by the Unity-driven defect, Kubernetes cross-family pressure signal, synthesis evidence, and adversarial review. |
| Full-fixture synthesis AR-01 bundled-offer cross-family phrasing caveat | Fixture/synthesis-level clarity issue | Does not require obligation-contract patch before baseline acceptance; Milwaukee depth remains not proven and should stay caveated. |
| Full-fixture synthesis AR-02 patch-history framing | Synthesis-level clarity issue | Does not affect the contract's baseline suitability. |
| Full-fixture synthesis AR-03 "Held" wording versus partial fixture discharge | Synthesis-level clarity issue | Does not show a missing obligation; it warns future readers not to treat fixture pressure as full raw capture validation. |
| Full-fixture synthesis AR-04 archive patch promotion route implicit | Optional hardening / synthesis clarity | Does not require another contract patch. This artifact now states the promotion route explicitly, and owner acceptance is recorded for strict baseline status. |
| Full-fixture synthesis AR-05 satellite section restates some core obligations | Synthesis-level clarity issue | Does not blur the contract itself, which retains the core/satellite split. |
| Manual harness discard vocabulary mismatch | Harness-level | Patch before next dry run, but not a baseline-contract blocker. |
| Manual harness H-09 rollup design does not force per-slice rows | Harness-level | Confirms the harness must better implement the contract; the contract already contains the needed rollup prohibition. |
| BT2-04 CS-08 raw observable is paraphrase-only | Dry-run execution-level | Shows a capture execution defect, not an obligation baseline defect. |
| BT2-04 H-09 run-level archive/timing rollups | Dry-run execution-level | Shows the dry run failed to expose per-slice states in the ledger; the obligation contract already requires that visibility. |
| BT2-04 minor provenance, timing, boundary, and numbering issues | Harness/dry-run optional hardening | Not baseline blockers. |
| Need for later operating model, human/agent roles, source-family reference layer, and possible multimodal fixtures | Downstream-level | Important future work, but not grounds to reject or patch the obligation baseline now. |

## Decision Rationale

`ACCEPT_BASELINE` follows from four source-grounded conclusions.

First, the obligation contract itself defines a coherent commissioned-capture
contract. It starts from a Decision Frame, rejects standing corpus capture in
v0, requires explicit discharge states, preserves raw observable and source
context, separates source claim from Orca interpretation, records timing,
cutoff, archive, access, recapture, and failure states, and forbids Capture
from emitting ECR schema, Cleaning transformations, Judgment labels, Decision
Strength, Action Ceiling, source maps, or runtime plans.

Second, the pressure-test synthesis reports that the planned fixture set
mostly held and found one material core defect: archive/history and recapture
were too coarse when mixed source states coexist. That defect was patched
narrowly in the current obligation contract. The synthesis keeps source-family
guidance in satellite and preserves not-proven boundaries for Milwaukee depth,
raw source-level sufficiency, archive-corpus breadth, multimodal coverage, and
owner acceptance.

The Source-Family Promotion route for that archive/history invariant is now
explicit: Unity exposed the core defect, Kubernetes supplied a cross-family
pressure signal, the synthesis generalized the invariant narrowly, and owner
acceptance of this `ACCEPT_BASELINE` decision serves as owner sign-off for that
specific invariant under the contract's promotion rule.

Third, the adversarial review of the full-fixture synthesis found no required
patch before advisory use. Its highest findings are P2/P3 clarity issues about
phrasing, patch-history framing, per-fixture discharge nuance, implicit archive
promotion route, and core/satellite labelling. Those findings are decision
input, not blockers to using the current obligation contract as baseline.

This decision relies on a chain of evidence rather than a prior standalone
adversarial review whose sole target was the obligation contract: the contract
was pressure-tested through the fixture synthesis, the synthesis was reviewed,
the manual harness / BT2-04 direction signal was reviewed, and the later
adversarial review of this decision read the contract directly and found no
blocking defect in `ACCEPT_BASELINE`. That chain is sufficient for a baseline
decision, but it is not a validation or hardening claim.

Fourth, the manual harness plus BT2-04 dry run was explicitly demoted to a
direction signal. Its P2 findings are real but they point to harness template
and dry-run execution patches: discard vocabulary, ledger rollup design, raw
observable preservation in one source slice, and per-slice H-09 archive/timing
rows. Those defects show that the manual harness did not always operationalize
the obligation contract. They do not show that the obligation contract itself
would misdirect future harness architecture.

Therefore, the current obligation contract is stable enough to serve as the
Data Capture obligation baseline, now owner-accepted here with strict limits
on what baseline acceptance authorizes.

## Patch Requirements If Any

No obligation-contract patch list is executed in this artifact.

Because the selected decision is `ACCEPT_BASELINE`, this artifact does not
name required baseline patches. The remaining issues are harness-level,
dry-run-level, synthesis-clarity-level, downstream-level, or optional
hardening. They may require later patch prompts or architecture inputs, but
they do not block baseline acceptance.

This artifact does not patch the obligation contract, the manual harness, the
BT2-04 dry run, the synthesis, or any review artifact.

## Downstream Implication

Because the owner has accepted this decision, a later Data Capture Harness
operating-model architecture lane may plan against the current obligation
contract as the baseline.

That later lane must remain bounded to harness operating-model architecture
unless separately authorized otherwise. It must not treat this baseline
decision as runtime, ECR, Cleaning, Judgment, source-system, scraper, API,
dashboard, storage, automation, schema, test, package, implementation,
deployment, commit, push, or PR authority.

This acceptance authorizes only bounded harness operating-model architecture
planning against the obligation baseline. A later architecture prompt must
carry this boundary explicitly.

## Non-Claims

This artifact does not claim:

- validation;
- source-of-truth promotion beyond this decision;
- Data Capture Spine completion;
- final harness acceptance;
- manual harness validation;
- BT2-04 source validity, credibility, admissibility, representativeness, or decision usefulness;
- ECR readiness or design;
- Cleaning readiness or design;
- Judgment readiness or design;
- Signal Use Classification, Decision Strength, or Action Ceiling readiness;
- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- runtime feasibility;
- source rights or data-rights sufficiency;
- source-system architecture;
- source maps;
- scraper, API, dashboard, storage, automation, schema, test, package, deployment, commit, push, or PR authorization.

Review consensus, model agreement, fixture count, and lack of P0/P1 findings
are not treated as validation or acceptance.

## Next Authorized Step

The smallest next authorized step is a bounded Data Capture Harness
operating-model architecture prompt against the accepted obligation baseline.
No ECR, Cleaning, Judgment, runtime, tooling, or implementation work is
authorized by this artifact.
