# Creator Profile Validator Structure Architecture Planning Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca architecture-planning prompt
scope: >
  Architecture planning prompt for deciding the creator-profile / creator-ledger
  validator structure after PR #439: full validator framework now versus a
  smaller layered validator architecture with shared source-input primitives,
  source-rebuild validation, and named Mini God Tier accepted residuals.
use_when:
  - Commissioning a read-only architecture pass on creator-profile validator structure.
  - Deciding whether full validation infrastructure should be built now or deferred.
  - Preparing the next creator-ledger validation move after PR #439 CI and validator hardening.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - orca-harness/capture_spine/creator_profile_current/validation.py
  - orca-harness/capture_spine/youtube_creator_observation/validation.py
  - orca-harness/capture_spine/linkedin_lane/shared_validation.py
  - orca-harness/tests/unit/test_creator_profile_current_static_view.py
  - orca-harness/tests/unit/test_youtube_creator_metric_seed.py
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - docs/review-outputs/creator_profile_current_validator_adversarial_code_review_v0.md
source_base_revision: codex/creator-metric-source-audit @ ad2e18869005ff2db983310e7022c554b23de169
stale_if:
  - PR #439 is rebased, amended, or superseded.
  - The creator-profile validator, YouTube observation validator, or creator metric seed tests change.
  - The owner redirects from architecture planning into implementation or SQLite/lake runtime work.
```

## Orca Prompt Preflight

```yaml
output_mode: file-write
prompt_artifact_path: docs/prompts/architecture/creator_profile_validator_structure_architecture_planning_prompt_v0.md
receiver_output_mode: chat-only architecture report for courier back to the owner
receiver_write_permission: read-only; no repo edits; no implementation; no commits; no pushes
template_kind: full-prompt; architecture-planning style; no model-specific template
edit_permission_targets_branch: >
  Receiver is read-only. Target workspace is the Orca repo or the PR #439 worktree
  on codex/creator-metric-source-audit at, or descended from,
  ad2e18869005ff2db983310e7022c554b23de169.
reviews: not a formal review prompt; findings-first risks are still useful but no review verdict is requested
doctrine_change: >
  Receiver may recommend a later validator architecture decision, but must not
  claim doctrine changed, validation passed, readiness, source promotion, or
  implementation authority.
destinations: >
  Prompt artifact is this file. Receiver returns a chat architecture report; no
  durable output path is required unless separately requested.
```

## Objective

Decide the best creator-ledger validator architecture after PR #439.

The owner question is:

```text
Why should we not aim for the full validator structure right off the bat?
Apply Mini God Tier and Smallest Complete Intervention. If full structure is
actually the right target, say so and name the accepted residuals.
```

The goal is not to avoid ambition. The goal is to decide whether "full validator
structure now" is the Mini God Tier target or whether it is premature maximal
infrastructure that should be replaced by a smaller layered architecture.

## Mandatory Method Handling

REFERENCE-LOAD `workflow-architecture-planning` if available. Do not APPLY it yet.

REFERENCE-LOAD `workflow-deep-thinking` if available. Do not APPLY it yet.

Then SOURCE-LOAD the required source pack below. Declare exactly one:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

Only after that declaration, APPLY architecture planning in `standard` profile.
Use local directional, adversarial, and grounding perspectives. If subagents are
available and explicitly authorized by the receiving environment, they may be
used, but subagents are not required.

## Required Source Pack

Read:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/decision-routing.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`
- `orca-harness/capture_spine/creator_profile_current/validation.py`
- `orca-harness/capture_spine/youtube_creator_observation/validation.py`
- `orca-harness/capture_spine/linkedin_lane/shared_validation.py`
- `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_lake_native_record_mapping_v0.md`
- `docs/review-outputs/creator_profile_current_validator_adversarial_code_review_v0.md`

If any file is absent, do not substitute memory. Mark the missing file under
`SOURCE_CONTEXT_INCOMPLETE` and continue only for advisory option comparison if
the remaining source is enough.

Do not browse the web. Do not use external architecture patterns as authority.

## Current Working Context To Verify, Not Trust

Treat these as hypotheses until confirmed from sources:

- PR #439 currently has a static creator-profile current view over 30 YouTube
  platform-account profiles with account-scoped aggregate metric rollups.
- The profile view is not the source of truth for individual reels, comments, or
  full creator intelligence. It is a current aggregate/profile view over lower
  source records.
- The recent validator hardening closed false-passes where metrics could be
  smuggled into `identity_evidence_summary` or `source_drill_back`, where
  `ideal_audience_profile` / `wind_calling_summary` accepted arbitrary objects,
  where source-drill observation IDs could drift, and where `bool` passed as a
  numeric metric.
- PR #439 CI failed because source-input hashes were recorded as Windows CRLF
  bytes while CI checked out LF repo text. The fix normalized source hash checks
  to LF repo-text bytes and updated source-input hashes.
- `youtube_creator_observation.validation` already has reusable source-input
  hash and live-lake validation concepts.
- `linkedin_lane.shared_validation` is a precedent for shared validation
  primitives used by multiple capture-spine slices.
- The next candidate move proposed by the current lane is: extract shared
  source-input/hash primitives first, then add a reusable creator-profile
  source-rebuild validator, and defer a full cross-family validation framework
  unless architecture planning says the framework is necessary now.

## Architecture Question

What validator structure should Orca target for creator ledger / creator profile
current after PR #439?

Compare at least these options:

1. **Patch-local continuation**: keep validation logic local to
   `creator_profile_current`, adding only the next missing checks.
2. **Layered Mini God Tier validator**: shared validation primitives for
   source-input resolution/hash policy; reusable creator-profile source-rebuild
   validator; optional live-lake validator kept separate; full framework deferred.
3. **Full validator framework now**: a cross-family validation substrate for
   structural checks, source-input hashing, source rebuilds, live-lake checks,
   metric rollups, identity joins, and future dashboards.
4. **Lake-first / SQLite-first validator**: move validation around physicalized
   lake or SQLite state now, with static JSON as derived output.

You may add a better hybrid if the sources justify it.

## Questions This Must Answer

1. Why not aim for full validator structure immediately?
2. If full structure is actually right, what evidence makes it worth the lock-in?
3. What is the stable core invariant that future creator intelligence must preserve?
4. What belongs in shared validation primitives versus creator-profile-specific
   validation?
5. Should source-input hash resolution be shared now, and what exact boundary
   prevents another CRLF/LF bug?
6. Should creator-profile source-rebuild validation be a reusable code path now,
   or remain fixture-test-only for one more step?
7. Should live-lake validation remain optional/operator-local, or be part of the
   main validator?
8. What should stay satellite or deferred: SQLite, dashboard validation,
   cross-platform identity stitching, engagement-rate derivation, target audience
   summaries, wind-calling summaries, and full lake-native derivation?
9. What MGT accepted residuals are named if we choose the layered path?
10. What MGT accepted residuals are named if we choose the full-framework path?
11. What is the smallest complete next routing object after the architecture pass?

## Required Analysis Discipline

- Apply Mini God Tier as a target lens, not as proof or scope expansion.
- Apply Smallest Complete Intervention to each recommended next move.
- Push back hard if "full validator structure" is really a framework-shaped
  answer to a two-surface problem.
- Push back hard if the smaller path quietly drops a material residual without
  naming it.
- Distinguish structural validation, source-backedness validation, live-lake
  validation, and product/dashboard readiness.
- Keep operator-local live-lake checks separate unless the sources prove they
  must be merged into the normal validator.
- Do not turn architecture implications into implementation steps or patch queues.
- Do not claim validation, readiness, approval, SQLite readiness, dashboard
  readiness, or data-lake physicalization.

## Expected Output

Return:

```text
Human Summary:
Decision:
Why Not Full Structure Now:
When Full Structure Would Be Right:
Target Architecture:
Why This Wins Under MGT:
Accepted Residuals:
Core / Satellite Boundary:
Shared Validator Primitives:
Creator-Profile-Specific Validator:
Source-Rebuild Validator:
Live-Lake Validator Boundary:
Deferred Implementation Implications:
What We Are Not Doing:
Blockers / Not-Proven Boundaries:
Next:

Agent Detail:
Profile / Evidence Mode / Source Mode:
Subagents Launched:
Source-Read Ledger:
Questions Answered:
Architecture Option Comparison:
Target Architecture Detail:
Validation / Failure Implications:
Bloat-Cut Queue:
What Would Change The Recommendation:
```

Use exactly one architecture result:

- `TARGET_RECOMMENDED`
- `OPTIONS_COMPARED_NO_SELECTION`
- `NEEDS_SOURCE_CONTEXT`
- `NEEDS_FEATURE_PLANNING`
- `DEFER_OR_REJECT`
- `AUTHORITY_BLOCKED`

These are planning results only. They are not validation, readiness, approval,
implementation authority, merge safety, source promotion, or production
clearance.

## Forbidden Outputs

Do not produce:

- source edits;
- migration code;
- SQLite schema;
- dashboard implementation;
- live capture execution;
- GitHub merge/PR actions;
- a patch queue;
- source-of-truth promotion;
- validation/readiness claims;
- model recommendations or model rankings.
