# Data Capture Harness Operating Model Architecture v2 Acceptance Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Records owner acceptance of `docs/product/data_capture_harness_operating_model_architecture_v2.md` as the controlling Data Capture Harness operating-model architecture for bounded pressure-test commissioning planning only.
use_when:
  - Checking the controlling Data Capture Harness operating-model architecture for pressure-test commissioning planning.
  - Checking whether v2 has been validated, hardened, or product-ready (it has not).
  - Preparing pressure-test commissioning planning artifacts against v2.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2.md
  - docs/product/data_capture_spine/data_capture_spine_lane_product_thesis_v0.md
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
stale_if:
  - A later owner decision amends, rejects, or supersedes this acceptance.
  - v2 is materially patched or superseded.
  - The Data Capture obligation baseline or obligation contract is amended or superseded.
  - Pressure-test evidence fires v2's own Stop Conditions And Re-Architecture Triggers.
```

## Status And Decision

Status: `ACCEPTED_FOR_PRESSURE_TEST_COMMISSIONING_PLANNING_V0`.

Primary decision: `ACCEPT_V2_FOR_PRESSURE_TEST_COMMISSIONING_PLANNING`.

Current amendment: `MECHANICAL_SOURCE_PROJECTION_BOUNDARY_PATCH_2026_05_30`.

Current controlling v2 hash after amendment:

```text
B0AAF782227C79198F6343F45B81ECCCCD3D76BF1572162C77C822BDB1339509
```

Owner decision recorded 2026-05-28:

```text
Owner decision: ACCEPT_V2_FOR_PRESSURE_TEST_COMMISSIONING_PLANNING.

I accept `docs/product/data_capture_harness_operating_model_architecture_v2.md`
(SHA256 EF9CA7F6EAD00584782CC0C58DC2E4E2E31A7F038101C211524F9205DC3D2357) as the
controlling Data Capture Harness operating-model architecture for bounded
pressure-test commissioning planning only.

This is not validation, not hardening, not product readiness, not final harness
acceptance, and not authorization for runtime, tooling, ECR, Cleaning, Judgment,
source systems, source maps, dashboards, scrapers, APIs, storage, automation,
schemas, tests, packages, deployment, commits, pushes, PRs, or buyer-facing
artifacts.

Controlling status yields when v2's own Stop Conditions And Re-Architecture
Triggers fire from pressure-test evidence. v2 is the basis for the next bounded
planning step; it is not permanent.

The independent adversarial review found no blocking findings and the two watch
items F-01 and F-02 are patched in this v2. Further pre-pressure-test review is
not required to enable bounded pressure-test commissioning planning.
```

Owner amendment recorded 2026-05-30:

```text
Owner decision: ACCEPT_MECHANICAL_SOURCE_PROJECTION_BOUNDARY_PATCH.

Mechanical Source Projection is accepted as a Data Capture-owned helper for
turning transport-heavy raw source into inspectable source rows. It is not a
standalone spine layer, not Cleaning, not ECR schema design, and not Judgment.

Data Capture may carry a Data Capture Projection Packet consisting of preserved
raw source, source-projected rows, and projection receipt warnings. Projection
may remove source-envelope noise from the working view. It must not remove
evidence rows because they appear low-value, low-score, repetitive, deleted, or
unhelpful.

ECR receipts the captured source/projection packet categorically before
Cleaning. Cleaning later verifies and normalizes raw-to-projected-to-cleaned
traceability. Judgment later decides meaning, credibility, attention, exclusion,
discounting, Decision Strength, and Action Ceiling.

This amendment preserves v2's non-claims. It does not authorize runtime,
tooling, ECR schema design, Cleaning implementation, Judgment work, pressure-test
execution, or source-system work.
```

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 v2 acceptance routing pack
  edit_permission: docs-write for this product artifact only
  target_scope:
    - docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_harness_operating_model_architecture_v2.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Compact source ledger:

| Source | Why read | Claim supported | Status note |
| --- | --- | --- | --- |
| Current owner instruction | Authorized narrow acceptance and refused further pre-pressure-test review | v2 may be the controlling architecture for pressure-test commissioning planning only | user-stated |
| Current owner instruction on 2026-05-30 | Authorized documenting Mechanical Source Projection and doctrine propagation | Projection is a Data Capture-owned helper and packet, not Cleaning/Judgment/ECR schema | user-stated |
| `AGENTS.md` | Orca project authority | Docs-only decision is allowed; no implementation authorized | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Orca overlay controls project facts | modified |
| `docs/product/data_capture_harness_operating_model_architecture_v2.md` | The architecture being accepted and amended | Current hash `B0AAF782227C79198F6343F45B81ECCCCD3D76BF1572162C77C822BDB1339509`; selected target is `Contract-pinned obligation-discharge operating envelope with second-operator capture-visibility check`; F-01/F-02 and the Mechanical Source Projection boundary patch are incorporated | untracked |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md` | Independent review of first v2 draft | `accept_v2_with_watch_items`; no blocking findings; F-01/F-02 watch items addressed in current v2 | untracked |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted obligation baseline | Baseline accepted for bounded harness operating-model architecture only | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | Six discharge states, 16 obligations, forbidden Capture outputs, pressure-test requirement | clean in named-path status |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Direction-signal demotion | Manual harness and BT2-04 are direction signal only, not architecture or validation | untracked |
| `docs/product/data_capture_spine_lane_product_thesis_v0.md` | Lane thesis using v2 as operating-model basis | Thesis is a routing/stance artifact, not validation; depends on v2 acceptance to ground the mechanism | untracked |

Dirty/untracked caveat: the worktree is dirty and several Data Capture artifacts are untracked. This acceptance is supplied by the current owner decision, not by dirty or untracked source status. It does not promote any source to source-of-truth beyond this decision.

## Acceptance Scope

This acceptance authorizes:

- using v2 as the operating-model architecture basis for the next bounded pressure-test commissioning planning artifact;
- naming v2 (with hash) in downstream lane artifacts as the controlling architecture for that planning scope;
- referring to v2's Role Model, Session Lifecycle, Stable Inherited Baseline Obligations, Pressure-Test Candidate Operating Controls, Failure And Limitation Visibility, Source-Family Satellite Boundary, Handoff Boundary, and Stop Conditions And Re-Architecture Triggers as the architecture surface against which pressure tests are planned.
- treating Mechanical Source Projection as a Data Capture-owned helper that may produce a Data Capture Projection Packet before ECR, with evidence-row removal forbidden.

This acceptance does not authorize:

- pressure-test execution;
- treating v2's Pressure-Test Candidate Operating Controls (five-role model, two-output second-operator vocabulary, capture-operator remediation vocabulary) as stable, validated, or permanent;
- runtime, tooling, source systems, source maps, dashboards, scrapers, APIs, storage, automation, schemas, tests, packages, deployment, commits, pushes, or PRs;
- ECR, Cleaning, Judgment, memo, evidence appendix, executive deck, or outcome-memory design;
- standalone Projection Spine, Filtering Layer, source-purification layer, or any projection practice that drops evidence rows before ECR/Cleaning;
- buyer proof, buyer validation, willingness-to-pay proof, commercial readiness, product readiness, feature readiness, implementation readiness, repeatability proof, or source-of-truth promotion beyond this decision.

## Re-Architecture Trigger Clause

v2's controlling status is conditional on its own Stop Conditions And Re-Architecture Triggers. When any of the following fires from pressure-test evidence, v2's controlling status yields and a re-architecture lane is opened:

- the obligation contract is materially revised or superseded;
- pressure-test results from real commissioned captures show a recurring obligation the operating model cannot expose without modification;
- a satellite source-family rule is promoted to core through the Source-Family Promotion Rule;
- an accepted ECR architecture lane changes the categorical handoff boundary;
- owner-authorized capture modes require session-lifecycle changes;
- repeated stop conditions show that the architecture, not only operator practice, is mis-shaped.

"Controlling" in this acceptance means "the architecture against which the next bounded planning step works," not "the architecture for all future Data Capture Spine work."

## Non-Claims

This artifact does not claim:

- validation;
- hardening;
- readiness of any kind;
- final harness acceptance;
- manual harness validation;
- BT2-04 source validity, credibility, admissibility, representativeness, or decision usefulness;
- ECR readiness or design, Cleaning readiness or design, Judgment readiness or design;
- buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, commercial readiness;
- runtime feasibility, runtime authorization, tooling authorization, scraper authorization, API authorization, dashboard authorization, archival-tool authorization, storage authorization, automation authorization, schema authorization, test authorization, package authorization, deployment authorization, commit/push/PR authorization;
- source rights or data-rights sufficiency;
- source-system architecture or source maps;
- pressure-test discharge;
- supersession of any earlier accepted Data Capture decision unless the change is explicit;
- promotion of any v2 Pressure-Test Candidate Operating Control to stable inherited obligation.

Subagent agreement, model agreement, perspective consensus, review recommendation, fixture count, and lack of P0/P1 findings are not validation or acceptance beyond this narrow controlling-architecture scope.

## Next Authorized Step

The next authorized step is a bounded Data Capture Spine pressure-test commissioning planning artifact that:

- pins v2 (by hash) as the controlling operating-model architecture for planning;
- pins the current Data Capture obligation contract version as the controlling obligation surface;
- preserves all non-claims;
- does not authorize pressure-test execution by itself.

No execution, no runtime, no tooling, no ECR/Cleaning/Judgment work is authorized by this acceptance.
