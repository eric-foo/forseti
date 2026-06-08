# Data Capture Spine Reddit Candidate URL Intake Default Policy Delegated Adversarial Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Strict delegated adversarial review-and-patch prompt for the bounded Reddit Candidate URL Intake default-policy decision artifact.
use_when:
  - Launching a de-correlated controller to harden the Reddit Candidate URL Intake default-policy decision before owner acceptance.
  - Checking the commission, patch boundary, report destination, and CA adjudication contract for that delegated pass.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
input_hashes:
  target_sha256: 437BA729A30A00B75E0ADFA40669E1B106461C1608E77C49802904FE75A0D9B8
branch_or_commit:
  branch: ecr-sp3-timing-deriver-slice1
  head: d857c581257ec74cc5eac8b53e7357556c2d1887
stale_if:
  - The target default-policy decision artifact changes before the delegated review runs.
  - The parent Candidate URL Intake contract, Reddit Candidate URL Intake architecture, Data Capture sub-map, or Reddit CloakBrowser/proxy allowance changes.
  - Orca delegated-review-patch, prompt-orchestration, or review-lane overlay authority changes.
```

## Prompt Status

Status: `STRICT_PROMPT_READY_WITH_DECORRELATION_PREFLIGHT_REQUIRED`.

This prompt was created from an explicit Chief Architect commission to run the
provisional Orca Delegated Review-and-Patch convention for one high-stakes
authored artifact.

This prompt does not run the review. It does not apply a patch. It does not
accept any delegated diff. It does not mark the default policy accepted,
validated, implementation-ready, or owner-approved.

The receiving controller must prove the de-correlation receipt before review or
patch work starts. If it cannot, it must return
`BLOCKED_DECORRELATION_RECEIPT_MISSING` or
`BLOCKED_CONTROLLER_NOT_DECORRELATED`.

## Launch Prompt

```text
You are the delegated controller for an Orca delegated adversarial review-and-patch hardening pass.

## Commission

Chief Architect commission: harden exactly one high-stakes authored artifact before owner acceptance.

Target artifact:
- docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md

Required durable review report path:
- docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_reddit_candidate_url_intake_default_policy_delegated_adversarial_review_patch_v0.md

Workspace:
- C:\Users\vmon7\Desktop\projects\orca

Pinned source state at prompt creation:
- branch: ecr-sp3-timing-deriver-slice1
- head: d857c581257ec74cc5eac8b53e7357556c2d1887
- target_sha256: 437BA729A30A00B75E0ADFA40669E1B106461C1608E77C49802904FE75A0D9B8

Dirty-state allowance:
- The target artifact and related Reddit Candidate URL Intake docs may be modified or untracked in the working tree.
- Read the current working tree in place. Do not create, clone, request, or switch to another worktree.
- If the target file is missing, inaccessible, or has been replaced by an unrelated artifact, return `BLOCKED_TARGET_UNAVAILABLE`.
- If the target hash differs, do not block automatically. Report the observed hash and continue only if the file is still the same named Reddit Candidate URL Intake default-policy decision artifact.

## Actor / Model-Family Receipt

Before reading source-heavy material or patching, record:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex current lane
  controller_model_family: <fill with your actual model family/vendor>
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied | blocked
```

The controller must be a different vendor or family from the author/home family.
This is a who-constraint, not a model recommendation. Do not include a
`Recommended model` block. If the receipt is missing, same-family, ambiguous, or
cannot prove de-correlation, stop before review and return the nearest blocker:
`BLOCKED_DECORRELATION_RECEIPT_MISSING` or
`BLOCKED_CONTROLLER_NOT_DECORRELATED`.

## Authority And Required Reads

Read and follow:
- AGENTS.md
- .agents/workflow-overlay/README.md
- .agents/workflow-overlay/decision-routing.md
- .agents/workflow-overlay/source-of-truth.md
- .agents/workflow-overlay/source-loading.md
- .agents/workflow-overlay/retrieval-metadata.md
- .agents/workflow-overlay/artifact-roles.md
- .agents/workflow-overlay/review-lanes.md
- .agents/workflow-overlay/delegated-review-patch.md
- .agents/workflow-overlay/prompt-orchestration.md
- .agents/workflow-overlay/validation-gates.md
- .agents/workflow-overlay/communication-style.md

Then read the target:
- docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md

Read these grounding artifacts only to the extent needed to verify the target:
- docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
- docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
- docs/workflows/data_capture_spine_consolidation_map_v0.md
- docs/workflows/orca_repo_map_v0.md
- docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
- docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md

Do not bulk-load unrelated prompts, review outputs, `_inbox`, research corpus,
method-validation replay artifacts, implementation code, or harness runtime
files unless a directly material source gap would otherwise prevent the review.

## Source-Gated Method Contract

REFERENCE-LOAD these methods before source loading:
- workflow-deep-thinking
- workflow-adversarial-artifact-review

Do not APPLY either method yet. Use them only to prepare the source-reading
lens.

SOURCE-LOAD the required Orca sources. Declare `SOURCE_CONTEXT_READY` or
`SOURCE_CONTEXT_INCOMPLETE` with missing sources, source gaps, excluded sources,
source conflicts, and dirty/untracked notes.

Only after `SOURCE_CONTEXT_READY`, APPLY:
1. workflow-deep-thinking to frame the boundary problem, failure modes, and decision criteria.
2. workflow-adversarial-artifact-review to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`.
Do not emulate the review lane inline and do not patch.

## Cynefin Routing

Run Orca Cynefin routing before reviewing or patching. The expected route is:
- Smallest complete outcome: harden only the target default-policy decision artifact and write the review report.
- Regime: complicated.
- Decomposition: layer-based with adversarial boundary checks.
- Current bottleneck: preventing the default policy from silently authorizing broad Reddit crawling, same-run expansion, capture, packet output, auto-promotion, or live execution.
- Riskiest assumption: that the default caps/surfaces/outbound/continuation rules are complete enough for no-live-access implementation scoping without being mistaken for sufficiency, coverage, or runtime authorization.
- Stop or pivot condition: if the defect is design-level across the parent contract or Reddit architecture rather than patchable inside the target, return `NEEDS_ARCHITECTURE_PASS` and do not patch.
- Allowed next move: review and patch only the target artifact.
- Disallowed next move: patch any other file, run live Reddit access, invoke CloakBrowser/proxies, emit Source Capture Packets, promote candidates, or perform implementation scoping.

## Patch Authority

Patch authority is granted only for:
- docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md

Everything else is read-only and flag-only, including:
- Orca overlay files.
- AGENTS.md and CLAUDE.md.
- repo maps and sub-maps.
- parent Candidate URL Intake contract.
- Reddit Candidate URL Intake architecture.
- Source Capture Armory docs.
- harness code, runners, tests, and runtime files.
- installed/user/plugin skills and external workflow source.

Patch only when the issue is materially decision-relevant and patchable inside
the target. If the correct fix belongs in another artifact, flag it and do not
edit that other artifact.

Do not commit. Do not stage. Do not run live external network access. Do not
invoke Reddit, CloakBrowser, proxies, packet runners, browser snapshots,
storage, scheduler, dashboard, deployment, ECR, Cleaning, Judgment, fixture
admission, source-quality scoring, or commercial-use paths.

## Review Criteria

Be maximally adversarial about whether the target policy could be misused to:
- become broad Reddit crawling or open-ended discovery;
- follow related subreddits, recommendations, cross-posts, "more like this," or outbound links in the same run;
- capture Reddit bodies, comments, profiles, users, raw HTML, screenshots, hidden session state, or secrets;
- emit Source Capture Packets or imply Source Capture Armory execution;
- auto-promote candidate URLs into capture units or Data Capture Spine handoff;
- treat caps reached, top-N rows, blocked results, or empty results as completion, sufficiency, or coverage proof;
- widen after blocked, empty, or capped outcomes without a new run or explicit scope amendment preserving the prior stop reason;
- use CloakBrowser/proxy approval as intake-run execution authority rather than downstream promoted-capture posture;
- authorize monitoring without a Decision Frame, cadence, stop date, max runs, max rows/run, and reason it remains candidate intake;
- claim owner acceptance, validation, readiness, implementation authorization, legal sufficiency, commercial rights, source-access boundary amendment, ECR, Cleaning, Judgment, fixture admission, or source-quality scoring.

Also check whether the target contains enough default policy for no-live-access
implementation scoping to avoid inventing:
- default run modes and caps;
- default-on and default-off candidate surfaces;
- outbound-link caps and source-family handoff rule;
- repeated-run and monitoring default;
- continuation and widening rule;
- promotion receipt owner;
- listing-provenance fields;
- implementation-scoping gate and hard non-authorizations.

## Output Contract

Write the full delegated review-and-patch report to:
- docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_reddit_candidate_url_intake_default_policy_delegated_adversarial_review_patch_v0.md

The report must include:
1. Commission and receipt.
2. Source context status.
3. Cynefin routing result.
4. Findings first, ordered by severity: critical, major, minor.
5. For each finding: location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and whether patched.
6. Unified diff for any target-file changes.
7. Per-change citations that are neutral in tone and decision-sufficient in substance.
8. Verdict relative to the commissioned target.
9. Residual-risk note.
10. Off-scope flags, if any.
11. Review-use boundary.

If no patch is needed, write the report with the no-patch verdict and residual
risks.

If a design-level problem is found, return `NEEDS_ARCHITECTURE_PASS`, leave no
kept partial patch, write findings only, and state the architecture question.

After successfully writing the report, return a compact chat summary with:
- report path;
- whether the target file was patched;
- changed files;
- verdict;
- residual risk;
- next action: Chief Architect adjudication of the delegated diff before anything is kept.

## CA Adjudication Boundary

Your diff, citations, verdict, and residual-risk note are claims to adjudicate,
not premises to inherit. The Chief Architect/home model decides what is kept and
may accept, modify, or reject each change. Nothing you write is owner
acceptance, validation, readiness, implementation authorization, or automatic
promotion.
```

## Prompt-Orchestrator Receipt

```yaml
prompt_orchestrator_receipt:
  requested_template_kind: review
  selected_template_source: docs/prompts/templates/review/adversarial_artifact_review_v0.md plus delegated-review-patch overlay contract
  output_mode: saved-artifact
  downstream_review_output_mode: review-report
  downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_reddit_candidate_url_intake_default_policy_delegated_adversarial_review_patch_v0.md
  workflow_sequence_status: bound_by_explicit_ca_commission_and_orca_overlay
  patch_authority: single target artifact only
  strict_blocker_carried_forward: de-correlated controller receipt must be recorded before execution
  non_claims:
    - delegated review not run by this prompt artifact
    - target patch not applied by this prompt artifact
    - no owner acceptance
    - no validation or readiness
    - no implementation authorization
    - no live Reddit, CloakBrowser, proxy, or Source Capture Armory execution authorization
```
