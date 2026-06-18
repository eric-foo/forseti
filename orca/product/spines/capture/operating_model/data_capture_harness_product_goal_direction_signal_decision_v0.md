# Data Capture Harness Product Goal Direction Signal Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Records the accepted demotion of the current manual Data Capture harness plus BT2-04 dry run to a direction signal, and states the product goal for the eventual Data Capture Harness.
use_when:
  - Deciding how to treat the current manual Data Capture harness and BT2-04 dry run.
  - Preparing the later Data Capture obligation-baseline accept/reject/patch decision.
  - Checking whether future Data Capture harness, architecture, patch, ECR, Cleaning, Judgment, or runtime work is being overclaimed.
open_next:
  - .agents/workflow-overlay/product-proof.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md
stale_if:
  - Owner later accepts, rejects, patches, or supersedes this Data Capture Harness Direction Signal decision.
  - Owner later accepts, rejects, or patches the Data Capture obligation baseline.
  - The manual harness or BT2-04 dry run is materially patched after this decision.
  - A later Data Capture harness architecture artifact supersedes this product-goal statement.
authority_boundary: retrieval_only
```

## Status And Owner Decision

Status: `ACCEPTED_DIRECTION_SIGNAL_DECISION_V0`.

Owner decision: the current manual Data Capture harness plus BT2-04 dry run is
accepted as `Data Capture Harness Direction Signal v0`.

This is a demotion, not a promotion. The current manual harness plus BT2-04 dry
run is not controlling architecture, not validation, and not the final harness.
It is accepted only as a direction signal for what the eventual Data Capture
Harness must make reliable, inspectable, and buyer-trustworthy.

Opus advisory input is adopted only on the demotion and product-goal frame:
demote the current manual harness plus BT2-04 dry run to direction signal, and
aim the eventual harness at buyer-trustworthy, obligation-discharging,
inspectable, layer-disciplined, failure-visible commissioned capture.

Opus's premature recommendation to apply P2 patches is not adopted here. Harness
patches are deferred until after this decision and the later
obligation-baseline decision.

## Source Loading Surface

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S2/S4 Data Capture product-decision pack
  edit_permission: docs-write
  target_scope: docs-only product artifact recording accepted demotion and product goal
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README; source-of-truth; source-loading; artifact-roles; retrieval-metadata; product-proof; named product and review sources
```

Primary authority for the accepted demotion is the current owner instruction.
The product context comes from Orca's product thesis, offer hypothesis, buyer
proof packet, Core Spine product contract, information-production foundation,
Data Capture/Cleaning boundary note, Data Capture pressure-test usage note, and
the adversarial review of the manual harness plus BT2-04 dry run.

Worktree status was dirty when this artifact was written, including modified
overlay/product files and untracked Data Capture-related artifacts. This file
does not convert dirty or untracked sources into source-of-truth authority.

Do not use this artifact for validation, readiness, source-of-truth promotion,
architecture control, patch authorization, obligation-baseline acceptance, or
implementation authorization.

## Product Goal Of The Data Capture Harness

The eventual Data Capture Harness should make commissioned capture
buyer-trustworthy before any ECR, Cleaning, Judgment, memo, appendix, or deck
depends on it.

Its product goal is:

```text
Buyer-trustworthy, obligation-discharging, inspectable, layer-disciplined,
failure-visible commissioned capture.
```

That means the harness should let a skeptical decision owner or reviewer see
what was commissioned, what was searched or inspected, what was captured, what
was not captured, what failed, what was inaccessible, what was post-window or
boundary-unsafe, what archive/cutoff posture exists, and what must remain
unknown before downstream judgment begins.

## Why The Harness Exists For Orca's Greatest Gain

Orca's greatest gain is not maximum source volume or premature source-system
machinery. Orca's gain comes from turning messy public signals into clean,
source-backed, constrained decision evidence that a buyer can inspect and trust
before internal data is conclusive.

The harness exists because Data Capture is the first trust-bearing point in
that chain. If capture is vague, over-summarized, source-map-driven,
failure-hiding, or judgment-contaminated, every later memo, appendix, and deck
inherits that weakness. If capture is commissioned, obligation-bound,
failure-visible, and layer-disciplined, then later Orca artifacts have a
credible basis for buyer-facing decision accountability.

The harness should therefore maximize Orca's ability to say, without theater:

```text
This is what was asked for, this is what was found, this is what was not found,
this is what failed, this is what remains unsafe or unknown, and this is the
bounded captured-signal basis available for downstream work.
```

## What The Harness Must Maximize

The eventual Data Capture Harness must maximize:

- Commission discipline: every run starts from a bounded decision frame,
  source boundary, cutoff/window posture, and capture purpose.
- Obligation discharge: capture obligations are made visible and cannot be
  silently collapsed into success language.
- Inspectability: source-visible language, raw observables, source identity,
  access path, timing, preservation posture, and capture context remain
  reconstructable enough for downstream review.
- Failure visibility: inaccessible, failed, degraded, fallback, not-attempted,
  unavailable, post-window, and boundary-unsafe states are recorded as signal,
  not hidden as operator inconvenience.
- Negative-space discipline: rejected, discarded, not-needed, out-of-scope, or
  unsafe candidates are recorded enough to prevent false completeness.
- Archive and cutoff posture: historical availability, archive attempts,
  fallback carriers, mixed current-page state, and post-cutoff leakage risks
  remain visible per material source slice when states differ.
- Layer separation: Data Capture records capture facts and blockers; it does
  not perform ECR schema design, Cleaning transformations, Signal Integrity,
  Signal Use Classification, Decision Strength, Action Ceiling, or memo/deck
  claims.
- Reusable operating pressure: a run can reveal where the harness, obligation
  baseline, or source-family guidance needs future work without turning one
  run's convenience into core law.

## What The Harness Must Not Become

The Data Capture Harness must not become:

- a source map;
- a source inventory;
- a scraper plan;
- an API or adapter plan;
- a dashboard or monitoring concept;
- a storage schema;
- an ECR field architecture;
- a Cleaning transformation ledger;
- a Judgment rubric;
- a source-quality scoring system;
- a proof-run validator;
- a buyer-proof artifact by itself;
- a backtest outcome claim;
- a runtime, tooling, package, test, or implementation plan;
- the final harness before obligation-baseline and architecture decisions.

The harness may expose pressure for these later lanes. It must not design or
authorize them.

## Direction Signal Status

`Data Capture Harness Direction Signal v0` consists of the current manual Data
Capture harness plus the BT2-04 dry run, interpreted through the adversarial
review and the owner demotion decision in this artifact.

Its accepted role is directional:

- It shows what a commissioned manual capture envelope should try to make
  visible.
- It demonstrates why a harness is needed before downstream layers can trust
  captured material.
- It surfaces pressure points that should inform later obligation-baseline,
  harness architecture, and patch decisions.
- It does not control those later decisions.

The adversarial review's `PATCH_BEFORE_NEXT_DRY_RUN` verdict remains advisory
input. This artifact does not apply, accept, or reject the P2 patches.

## What The Direction Signal Proves / Does Not Prove

What it proves as a direction signal:

- A commissioned, obligation-first manual harness can expose source candidates,
  capture notes, timing/window posture, archive failures, negative space,
  captured-but-unusable material, and layer-boundary discipline in one dry run.
- The manual harness plus BT2-04 run revealed useful pressure on discard
  vocabulary, per-slice obligation ledgers, raw-observable preservation, and
  archive/timing rollups.
- The direction of travel should be commissioned capture with visible failures
  and non-collapse, not generic data farming or source-map accumulation.

What it does not prove:

- It does not validate the harness.
- It does not validate Data Capture Spine.
- It does not accept the obligation baseline.
- It does not prove the obligation contract is hardened.
- It does not prove the BT2-04 captured sources are valid, credible,
  admissible, representative, or decision-useful.
- It does not prove buyer proof, commercial readiness, product readiness,
  feature readiness, implementation readiness, Core Spine validation, or Data
  Capture closure.
- It does not prove the final harness shape, source-family coverage, runtime
  feasibility, tooling feasibility, source rights, automation feasibility, or
  repeatability.

## Deferred Decisions

Deferred decision: obligation baseline accept/reject/patch.

The later obligation-baseline decision must decide whether the current Data
Capture obligation baseline candidate is accepted, rejected, or patched. This
artifact does not decide it.

Deferred decision: harness architecture planning.

The eventual harness architecture may use this direction signal as input, but
it must wait for the obligation-baseline decision and explicit authorization.
This artifact does not architecture-plan the harness.

Deferred decision: harness patches.

P2 and P3 patch candidates from the adversarial review remain deferred. They
must not be applied from this artifact. They may be considered only after the
later obligation-baseline decision and a bounded patch authorization.

Deferred decision: ECR, Cleaning, Judgment, and runtime work.

ECR, Cleaning, Judgment, source maps, scrapers, APIs, dashboards, automation,
schemas, tests, packages, runtime tooling, and implementation remain out of
scope. This artifact creates no authority to design or build them.

## Non-Claims

This artifact does not claim:

- validation;
- readiness;
- source-of-truth promotion;
- buyer proof;
- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- commercial readiness;
- product readiness;
- feature readiness;
- implementation readiness;
- Core Spine v0 validation;
- Data Capture Spine completion;
- final harness acceptance;
- obligation-baseline acceptance;
- harness patch acceptance;
- architecture acceptance;
- ECR, Cleaning, Judgment, or runtime readiness.

It does not authorize patches, architecture planning, proof runs, source maps,
scrapers, APIs, dashboards, automation, schemas, tests, packages,
implementation, deployment, commits, pushes, or PRs.

## Next Authorized Step

The next authorized step is a later docs-only obligation-baseline decision:
accept, reject, or patch the Data Capture obligation baseline candidate.

That step should use this artifact only as a product-goal and demotion
constraint. It should not treat the current manual harness plus BT2-04 dry run
as controlling architecture, validation, or final harness authority.
