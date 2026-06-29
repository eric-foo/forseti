---
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt
scope: >
  Commission prompt for a de-correlated adversarial mixed implementation
  review-and-patch pass on the creator public-handle linkage ledger v0 static
  fixture/validator lane; CA/home model adjudicates the working-tree diff
  before keep.
use_when:
  - Reviewing the creator public-handle linkage ledger v0 branch before any
    downstream ledger population or SQLite migration work.
  - Checking whether the validator, synthetic fixture, tests, and propagated
    docs preserve the public-handle-only identity-stitching boundary.
authority_boundary: retrieval_only
review_type: delegated_adversarial_mixed_implementation_review_patch
access: repo
dispatch_mode: external-controller-courier
output_mode: review-report
edit_permission: patch-only
target_commit: ecfcee8f17c7b3c622b8620c10033aaf9347c4cf
durable_report_destination: docs/review-outputs/creator_public_handle_linkage_ledger_delegated_adversarial_code_review_patch_v0.md
authored_by: GPT-5 / Codex home model
reviewed_by: unrecorded
---

# Creator Public-Handle Linkage Ledger Delegated Adversarial Code Review-And-Patch Prompt v0

> Provisional Orca delegated review-and-patch convention
> (`.agents/workflow-overlay/delegated-review-patch.md`). This is a commissioned,
> bounded-executor pass. The delegate's diff, citations, and verdict are
> decision input only: not validation, not readiness, not approval, and not
> auto-keep. The commissioning Chief Architect/home model adjudicates every hunk
> before anything is kept.

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: patch-only within submitted target files
  target_scope: creator public-handle linkage ledger v0 static fixture, validator, tests, and propagation docs
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, .agents/workflow-overlay/README.md, target files, validation evidence below
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 -- constants bound; deltas stated in this prompt.
authorization_basis: current owner request to run workflow-delegated-review-patch after the fused implementation.
objective / intended_decision: decide whether the v0 static ledger/validator is safe to keep as the pre-SQLite public-handle linkage substrate, or whether it needs patching / architecture rework.
output_mode: review-report, with paste-ready courier summary back to the commissioning CA.
doctrine_change_decision: no new doctrine change requested; patch only the named branch implementation/prose. If a needed fix changes capture/privacy/ledger doctrine, return NEEDS_ARCHITECTURE_PASS.
isolation_decision: existing isolated worktree branch off main; review target is the implementation branch below.
thread_operating_target_continuity: no visible active thread_operating_target carried; this prompt continues the creator-linkage ledger workstream by explicit owner request.
```

Workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-ledger-static-fixture`
Expected branch: `codex/creator-ledger-static-fixture`
Implementation target commit: `ecfcee8f17c7b3c622b8620c10033aaf9347c4cf`

Dirty-state allowance: the prompt file itself may exist in the worktree after
this commission is filed. Review and patch only the target files listed below.
Do not treat this prompt file as review scope.

## Receiving Actor / De-Correlation Receipt

- author / CA / home model family: GPT-5 / Codex home model, OpenAI lineage
- required controller: different vendor / model lineage from the author/home
  model; unknown or undisclosed lineage does not satisfy cross-vendor discovery
- current receiving actor role: controller, if this prompt is pasted directly
  to the reviewer; otherwise home-dispatcher must route to a de-correlated
  controller
- controller model family: `operator_to_fill`
- de-correlation status: controller must verify before review; if not
  satisfied, return `BLOCKED_CONTROLLER_NOT_DECORRELATED`
- model choice is a who-constraint only, not a recommendation, ranking, or
  runtime-routing rule

## What This Is For

This branch adds the v0 static substrate for creator cross-platform public-handle
linkage before any SQLite promotion:

- a source-cited, table-shaped JSON ledger contract for linking public creator
  accounts across platforms;
- a validator package that blocks private/contact/legal/person-demographic/raw
  social graph fields and rejects LLM-only final links;
- a synthetic fixture and adversarial tests;
- propagation docs so future ledger and audience work do not misread the public
  handle linkage surface as a broader identity or demographic dossier.

Done looks like: the implementation makes it hard to fake a same-creator link,
hard to store forbidden person/audience data in the linkage ledger, and easy to
promote the same table shape to SQLite later without changing semantics.

## Required Method Sequence

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/source-loading.md`,
   `.agents/workflow-overlay/review-lanes.md`,
   `.agents/workflow-overlay/delegated-review-patch.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`, and
   `.agents/workflow-overlay/safety-rules.md`.
4. REFERENCE-LOAD `workflow-deep-thinking`; do not apply it before source
   readiness.
5. REFERENCE-LOAD `workflow-code-review` and
   `workflow-adversarial-artifact-review`; do not apply either before source
   readiness.
6. SOURCE-LOAD the target files, read-only context files, and validation
   evidence listed below.
7. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
8. After `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame failure
   modes, then APPLY `workflow-code-review` to validator/test behavior and
   `workflow-adversarial-artifact-review` to the specs/docs.
9. Patch only material findings inside the submitted target files. Do not stage,
   commit, push, install, deploy, run live capture, call external services, or
   start SQLite migration work.

If either review skill is unavailable in the controller runtime, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` for the missing lane rather than emulating a
strict review inline.

## Editable Target Files

Patch only these files:

- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca-harness/capture_spine/creator_public_handle_linkage/__init__.py`
- `orca-harness/capture_spine/creator_public_handle_linkage/models.py`
- `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`
- `orca-harness/tests/fixtures/creator_public_handle_linkage/valid_synthetic_ledger.json`
- `orca-harness/tests/unit/test_creator_public_handle_linkage.py`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/orca_repo_map_v0.md`
- `orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/README.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`

Everything else is read-only / flag-only. If the correct fix lies outside these
paths, return a finding and do not edit that file.

## Read-Only Context To Inspect

Read when material to a finding:

- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md`
- `orca-harness/schemas/audience_inference_models.py`
- `orca-harness/scoring/audience_fusion.py`
- `docs/prompts/deep-thinking/creator_ledger_cross_platform_identity_architecture_prompt_v0.md`
- `.agents/workflow-overlay/validation-gates.md`

The ideal-audience sources are context, not patch scope. Use them to catch a
specific failure mode: the public-handle linkage ledger must not silently absorb
Tier-2-A aggregate audience demographics. If a ledger home for ideal-audience or
aggregate-audience attributes is needed, flag it as a separate architecture
decision instead of patching it into this linkage ledger.

## Validation Evidence To Inspect

The author reported these focused checks after the implementation:

```powershell
python -m pytest -q tests\unit\test_creator_public_handle_linkage.py
```

Observed output summary:

```text
15 passed
```

```powershell
python -m pytest -q tests\unit\test_creator_public_handle_linkage.py tests\unit\test_reddit_graph_frontier.py tests\unit\test_linkedin_graph_frontier.py tests\unit\test_linkedin_lane.py
```

Observed output summary:

```text
87 passed
```

```powershell
python .agents\hooks\check_retrieval_header.py --changed --strict
```

Observed result: passed.

```powershell
python .agents\hooks\check_repo_map_freshness.py --changed --strict --message "repo-map-ack: isolated worktree path is workspace scaffolding, not a product navigation target"
```

Observed result: passed.

```powershell
git diff --check
```

Observed result: passed with CRLF warnings only.

```powershell
python .agents\hooks\check_placement.py --strict
```

Observed result: failed on pre-existing repository placement debt and
legacy/warn-only harness classifications; do not treat that as success. Verify
whether any new linkage file represents a material placement blocker. If yes,
flag or patch within scope; if no, report the residual clearly.

You may rerun focused Python tests and static checks. Do not run network, live
social-media capture, browser automation, package installs, SQLite migrations,
or external API calls.

## Review Questions

Prioritize blocker and major issues. Patch minor issues only when the patch is
small and directly reduces false-success or boundary-drift risk.

1. Does the validator actually enforce the spec's public-handle-only boundary,
   or can forbidden fields slip through under nested structures, alternate key
   names, metadata blobs, evidence payloads, or future platform extensions?
2. Does it correctly reject `confirmed_public_account_link`, LLM-only final
   links, final links with disconfirming evidence, and probable links without
   three independent weak evidence types plus human review?
3. Are the strong / weak / disconfirming evidence rules encoded in a way that
   matches the spec, including independence requirements and source-pointer
   expectations?
4. Can a synthetic fixture accidentally contain real creator handles, URLs, or
   source pointers? Does synthetic mode block real-looking data without
   becoming so broad that useful synthetic tests are impossible?
5. Does the schema preserve a clean migration path to SQLite: stable table-like
   records, durable IDs, no denormalized ambiguity that would force a later
   semantic rewrite?
6. Do tests fail for the important negative cases, or are they asserting only
   happy-path parsing? Add focused adversarial tests if a material gap exists.
7. Do docs and propagation surfaces correctly state that Tier-2-B public
   handle-to-public-handle stitching is activated only for public handles, while
   non-public-handle joins and Tier-3 person/contact/private data remain
   forbidden?
8. Did any propagation wording accidentally authorize runtime capture, live
   identity resolution, SQLite migration, demographic inference, audience graph
   storage, or commercial readiness?
9. Does the ideal-audience lane stay separate? The right pushback is likely:
   Tier-1 ideal-audience profile and Tier-2-A aggregate audience demographics
   may need an adjacent ledger/schema home, but not inside the public-handle
   linkage ledger rows.
10. Is there a design-level issue that cannot be patched locally, such as the
    ledger needing a different entity model, provenance model, or audience home?
    If yes, return `NEEDS_ARCHITECTURE_PASS` and stop patching that issue.

## Patch Scope

Allowed:

- patch the editable target files only;
- add or adjust tests in `orca-harness/tests/unit/test_creator_public_handle_linkage.py`;
- adjust the synthetic fixture when needed to prove boundary behavior;
- tighten wording in the linkage spec and listed propagation docs to remove
  ambiguity introduced by this branch.

Forbidden:

- edits outside the target files;
- staging, committing, pushing, PR creation, deployment, package installs, live
  capture, browser automation, external API calls, SQLite migration, or database
  file creation;
- broad refactors, new runtime surfaces, new platform capture routes, or moving
  docs between folders;
- adding real creator handles, real source URLs, private/contact/legal/person
  data, raw social graph data, per-follower/commenter records, or actual-audience
  claims to fixtures or docs;
- using the public-handle linkage ledger as the home for ideal-audience or
  aggregate demographic attributes.

If the correct fix requires an architecture pass or a new ledger/schema home,
return `NEEDS_ARCHITECTURE_PASS` and do not force a local patch.

## Required Output

Write the full review report to:

`docs/review-outputs/creator_public_handle_linkage_ledger_delegated_adversarial_code_review_patch_v0.md`

The report must include:

- source context status;
- deep-thinking risk frame before findings;
- findings first, ordered by severity with file/line references;
- for each finding: `severity`, `location`, `failure_mode`, `evidence`,
  `impact`, `minimum_closure_condition`, and `next_authorized_action`;
- patches applied, if any;
- unified diff or precise changed-file summary;
- validation run or explicit not-run status;
- residual risk;
- verdict: `PATCHED_FOR_CA_ADJUDICATION`,
  `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, or
  `BLOCKED_*`;
- provenance fields: `authored_by` from this prompt and
  `reviewed_by: <actual controller model+version>` or `unrecorded` if the
  operator cannot provide it;
- non-claims: no validation, no readiness, no approval, no auto-keep, no
  deployment, no runtime capture, no SQLite migration, no live social-media
  access, and no audience-demographics activation.

After writing the report, return only a compact courier summary and the report
path in chat. The reviewer output is decision input for CA adjudication, not
automatically kept truth.

## CA-Side Adjudication Note

The commissioning Chief Architect/home model will adjudicate the returned
working-tree diff hunk-by-hunk against the controller's citations and this
branch's intent. The CA may accept, modify, or reject any change, including an
individually defensible one, before anything is kept.
