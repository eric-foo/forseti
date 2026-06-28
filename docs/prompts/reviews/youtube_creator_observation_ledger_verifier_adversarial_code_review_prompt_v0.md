# YouTube Creator Observation Ledger Verifier Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated adversarial implementation/code
  review of the YouTube creator observation ledger verifier hardening commit.
use_when:
  - Commissioning an external controller to inspect the verifier/test hardening
    commit before relying on the YouTube creator observation ledger as a static
    source-backed creator observation substrate.
  - Checking the prompt source, target scope, and output binding for the
    creator observation verifier review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: 77f0ade583b84acfd300385fa02037364508b74f..5295778eb024a3ba5ffe280df163a4c555390b52
prompt_carrier_note: >
  This prompt may be committed after the implementation commit. The
  implementation target under review ends at
  5295778eb024a3ba5ffe280df163a4c555390b52; prompt-only carrier commits do not
  change the implementation target unless they modify the named target files.
stale_if:
  - Any named implementation target file changes after 5295778eb024a3ba5ffe280df163a4c555390b52 and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor is not de-correlated from the OpenAI/GPT-family author but still claims cross_vendor_discovery.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/youtube_creator_observation_ledger_verifier_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local implementation/code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-ledger-static-fixture`, branch `codex/creator-ledger-static-fixture`, implementation range `77f0ade583b84acfd300385fa02037364508b74f..5295778eb024a3ba5ffe280df163a4c555390b52`, dirty state allowed only for this prompt artifact or later prompt-carrier commits that do not touch target files.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended. This prompt routes a review; it does not alter review, prompt, Data Capture, Creator Signal, Data Lake, SQLite, social capture, or metric-rollup doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/youtube_creator_observation_ledger_verifier_adversarial_code_review_v0.md`.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: read-only
  target_scope: YouTube creator observation ledger verifier hardening commit
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, .agents/workflow-overlay/README.md, target files, validation evidence below
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 -- constants bound; deltas stated in this prompt.
authorization_basis: current owner invocation of workflow-delegated-review-patch after the fused verifier/test hardening turn.
objective / intended_decision: decide whether the verifier/test hardening commit catches the material false-success and scope-drift risks for the v0 static YouTube creator observation ledger, or whether the CA should patch, reroute, or hold for architecture.
output_mode: review-report, with paste-ready courier summary back to the commissioning CA.
doctrine_change_decision: no new doctrine change requested. If a needed fix changes Creator Signal, Data Capture, Data Lake, metric-rollup, identity-linkage, or SQLite doctrine, return the design-level blocker instead of treating it as a local code issue.
isolation_decision: existing isolated worktree branch off main; review target is the implementation branch and commit range above.
thread_operating_target_continuity: no visible active thread_operating_target carried; this prompt continues the creator-ledger verifier workstream by explicit owner request.
```

## Commission

Run an adversarial implementation/code review of the YouTube creator observation
ledger verifier hardening commit ending at
`5295778eb024a3ba5ffe280df163a4c555390b52`.

This prompt follows `workflow-delegated-review-patch` route-out, but the target
is a multi-file implementation/code change packet. Per Orca
`.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the
single-artifact delegated review-and-patch convention. Route it through
implementation/code review instead. The reviewer is read-only and must not patch
source files.

Review purpose:

1. Attack whether the verifier actually prevents false confidence in the static
   YouTube creator observation ledger.
2. Verify whether the tests cover the material negative cases, including source
   rebuild drift, live-lake mismatch, duplicate IDs, channel mismatch, metric
   smuggling, cross-platform identity smuggling, and transcript-body smuggling.
3. Check whether docs and propagation surfaces accurately state the verifier's
   claim boundary without implying metric readiness, cross-platform linkage,
   SQLite readiness, or live capture.
4. Scan only the touched implementation scope plus named context for blocker or
   major issues. Minor findings are allowed, but do not widen into unrelated
   Creator Signal, Capture, Data Lake, Cleaning, Judgment, UI/dashboard, or
   product-proof review.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: operator_to_fill.
- current_receiving_actor_role: controller if this prompt is pasted directly to the reviewer; otherwise home-dispatcher must route to a de-correlated controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `cross_vendor_discovery` only if the reviewer is a different upstream vendor / model lineage from OpenAI/GPT-family; otherwise use `same_vendor_sanity` or `self_fallback` and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt. The family requirement is a who-constraint only.

If the reviewer cannot access the named repo/worktree and commit range directly,
return `SOURCE_CONTEXT_INCOMPLETE` and ask the operator for a no-repo source
capsule. Do not review a summary, recreated source, alternate checkout, or pasted
diff as a substitute for the pinned repo target.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` if
   available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing
   sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure
   modes, then APPLY workflow-code-review to produce findings-first
   implementation/code review.
5. If `workflow-code-review` is unavailable, use its zero-config findings-only
   advisory semantics from this prompt, but mark strict review claims
   `NOT_CLAIMED`.

## Required Reads

Read these authority and boundary files first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`

Then read the review target:

- `orca-harness/capture_spine/youtube_creator_observation/__init__.py`
- `orca-harness/capture_spine/youtube_creator_observation/validation.py`
- `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/orca_repo_map_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/README.md`

Read this source-owned context as needed to judge the verifier:

- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`
- `orca-harness/tests/unit/test_creator_public_handle_linkage.py`

Do not widen into the full data lake, all source-capture families, dashboard
work, SQLite planning, or live capture unless a specific finding needs a narrow
read and you name the reason.

## Target Diff And Dirty-State Allowance

Implementation target range:

```text
77f0ade583b84acfd300385fa02037364508b74f..5295778eb024a3ba5ffe280df163a4c555390b52
```

Target commit:

```text
5295778eb024a3ba5ffe280df163a4c555390b52 test: harden youtube creator observation ledger
```

Observed target files in that range:

```text
M docs/workflows/data_capture_spine_consolidation_map_v0.md
M docs/workflows/orca_repo_map_v0.md
A orca-harness/capture_spine/youtube_creator_observation/__init__.py
A orca-harness/capture_spine/youtube_creator_observation/validation.py
M orca-harness/tests/unit/test_youtube_creator_observation_ledger.py
M orca/product/spines/capture/core/source_capture_toolbox/README.md
M orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
```

Use:

```powershell
git diff 77f0ade583b84acfd300385fa02037364508b74f..5295778eb024a3ba5ffe280df163a4c555390b52 -- docs/workflows/data_capture_spine_consolidation_map_v0.md docs/workflows/orca_repo_map_v0.md orca-harness/capture_spine/youtube_creator_observation/__init__.py orca-harness/capture_spine/youtube_creator_observation/validation.py orca-harness/tests/unit/test_youtube_creator_observation_ledger.py orca/product/spines/capture/core/source_capture_toolbox/README.md orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
```

If the branch contains a later prompt-only commit, verify whether the target
files above still match `5295778eb024a3ba5ffe280df163a4c555390b52`. If they
changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if
the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The author observed these checks after the verifier hardening commit.

Portable no-live-lake suite:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp 'pytest_creator_observation_tmp_portable' 'orca-harness\tests\unit\test_youtube_creator_observation_ledger.py' 'orca-harness\tests\unit\test_creator_public_handle_linkage.py'
```

Observed output summary:

```text
31 passed, 1 skipped in 0.23s
```

Live-lake reconciliation suite:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; $env:ORCA_DATA_ROOT='F:\orca-data-lake'; python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp 'pytest_creator_observation_tmp_live' 'orca-harness\tests\unit\test_youtube_creator_observation_ledger.py' 'orca-harness\tests\unit\test_creator_public_handle_linkage.py'
```

Observed output summary:

```text
32 passed in 0.30s
```

Compile check:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m py_compile 'orca-harness\capture_spine\youtube_creator_observation\validation.py' 'orca-harness\capture_spine\youtube_creator_observation\__init__.py'
```

Observed result: passed with no output.

Observed hook/static checks:

- `git diff --check`: passed; prior staged run had only standard Windows CRLF warning text.
- `.agents\hooks\check_retrieval_header.py --staged --strict`: passed.
- `.agents\hooks\header_index.py --staged --strict`: passed.
- `.agents\hooks\check_map_links.py --staged --strict`: passed with zero findings and existing annotated nonresolving debt.
- `.agents\hooks\check_dcp_receipt.py --staged --strict`: passed after the YouTube spec DCP trigger was fixed to `product_doctrine`.
- `.agents\hooks\check_repo_map_freshness.py --changed --strict --message "repo-map updated for YouTube creator observation ledger verifier"`: passed.
- `.agents\hooks\check_placement.py --changed --strict`: failed on known repo-wide placement debt and legacy/warn-only harness classifications; reviewer should check whether any new target file creates a material placement blocker.

You may rerun focused Python tests and static checks. Do not run network, live
social-media capture, browser automation, package installs, SQLite migrations,
database writes, or external API calls. If you do not rerun validation, report
validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

- Does `validation.py` fail closed on all unknown or forbidden fields the spec
  claims to block, including nested dictionaries, optional sections, source
  rebuild inputs, evidence payloads, live-lake metadata, or future extensions?
- Does it prevent metric smuggling into the v0 observation ledger while allowing
  the explicit current non-claim that average views and engagement rate are not
  computed here yet?
- Does it prevent cross-platform identity/linkage smuggling, such as TikTok,
  Instagram, email, contact, person-demographic, legal, private, transcript-body,
  or raw social-graph fields?
- Does source rebuild validation actually prove that source-owned fields match
  `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json`, or could
  hand-edited ledger fields drift while the test still passes?
- Does live-lake validation reconcile the right UUID, manifest, packet refs,
  video IDs, and channel metadata under `F:\orca-data-lake`, or is the optional
  `ORCA_DATA_ROOT` test too easy to skip while still implying stronger coverage?
- Do duplicate observation IDs, duplicate video IDs, duplicate packet refs,
  missing packet refs, packet/video misalignment, invalid packet relpaths, and
  channel mismatches fail in the verifier for the right reasons?
- Do tests mutate the ledger deeply enough to prove negative cases, or do they
  mostly test top-level wrappers and leave nested or source-rebuild gaps?
- Does the verifier produce useful, non-silent failures for reviewer/operator
  debugging, or are error messages too broad to route a data problem quickly?
- Do the spec and propagation docs accurately state that this is a static
  observation ledger, not a one-stop creator dashboard, metric-rollup table,
  cross-platform identity graph, SQLite store, or public-facing product surface?
- Does any wording in the docs overclaim validation, readiness, live-lake
  coverage, creator influence scoring, average views, engagement rate,
  cross-platform stitching, or commercial/buyer-facing readiness?
- Does the package placement make sense for the current harness/product split:
  reusable verifier in `orca-harness`, product contract/spec in `orca/product`,
  ledger JSON under the YouTube source-family product surface, and prompt/review
  artifacts under `docs/`?
- Is there a design-level issue that cannot be fixed locally, such as the
  ledger needing a different entity model, metric rollup home, SQLite schema,
  Creator Signal surface, or identity-stitching boundary? If yes, report that as
  a design blocker; do not treat it as a code nit.

## Intended Hardening Closure Check

Treat these hardening goals as claims to verify, not accepted truth:

- H-01 portable verifier: the ledger validates without live lake access and
  rejects known false-success patterns.
- H-02 source rebuild: source-owned fields can be rebuilt from the source
  creator ledger and compared against the static observation ledger.
- H-03 live-lake optional reconciliation: with `ORCA_DATA_ROOT=F:\orca-data-lake`,
  packet/video/channel refs reconcile to observed lake metadata.
- H-04 boundary preservation: no metric rollups, cross-platform linkage,
  transcript bodies, private/contact/person data, or creator dashboard claims are
  admitted by the verifier or docs.

For each, report one of:

- `closed`: implementation and tests now cover the failure mode.
- `partially_closed`: some protection exists but a material variant remains.
- `not_closed`: the original failure mode remains.
- `not_assessed`: source or environment prevented assessment.

If `partially_closed` or `not_closed`, include evidence and a minimum closure
condition.

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness,
acceptance, validation, or pass/fail verdict unless Orca overlay authority is
supplied separately. Use findings-only advisory review. Do not emit
`patch_queue_entry`; do not edit source files; do not commit, push, PR, or run
live capture.

If you find no blocker or major issue, say so and state residual risks or
validation gaps. If you find an issue, findings lead the report and must include:

- finding id
- severity as `blocker`, `major`, or `minor` for prioritization only, not formal Orca verdict authority
- target file and stable line/anchor
- evidence from the implementation
- authority or evidence basis
- concrete impact
- minimum closure condition
- next authorized action
- validation expectation

## Output Contract

Write the full review report to:

`docs/review-outputs/youtube_creator_observation_ledger_verifier_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill_actual_controller_identity`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery` only if the reviewer is a different upstream vendor / model lineage from OpenAI/GPT-family; otherwise use `same_vendor_sanity` or `self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- intended hardening closure table for H-01/H-02/H-03/H-04
- open questions and residual risk
- validation rerun status
- strict-only blockers and non-claims
- `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block

Do not write outside that report path. If the report path already exists, stop
and report `BLOCKED_OUTPUT_DESTINATION_COLLISION` unless the operator explicitly
provides a new output path.

## Delegated Code Review Return Courier

Append this block at the end of the report:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- intended hardening closure statuses for H-01/H-02/H-03/H-04
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```
