# Search-Surface Google Parameterized-US Route Adversarial Code/Artifact Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Strict route-out prompt for de-correlated adversarial review of the
  parameterized Google Search-surface route guard, doctrine record, and
  repository wiring.
use_when:
  - Commissioning an independent efficacy review of the Google search-surface route enforcement patch.
  - Checking whether code-enforced behavior and doctrine boundaries match the Search-Surface MGT capture-efficacy goal.
  - Routing a mixed code/config/artifact review without pretending the single-artifact delegated-review-patch convention fully applies.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md
branch_or_commit:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\search-param-us-enforcement
  branch: codex/search-param-us-enforcement
  base_head_at_prompt_creation: c4cc9e3e3cb0a6f1b647575fd18e12d0cc9950d1
stale_if:
  - The branch changes materially before the delegated review runs.
  - The Google search-surface route decision, validation-gates enforcement placement, delegated-review-patch convention, or prompt-orchestration contract changes.
  - The review purpose expands beyond capture-efficacy route enforcement into crawler, monitoring, proxy/VPN, durable-demand, Judgment, or Product Lead proof work.
```

## Prompt Status

Status: `STRICT_ROUTE_OUT_PROMPT_READY_WITH_OPERATOR_FIELDS`.

This prompt was created after an explicit owner request to keep the
US-parameterized Google Search route and add behavioral enforcement plus a
doctrine record, then run a delegated efficacy review.

Boundary: the provisional delegated-review-patch convention is single-artifact
by default. This target is a mixed code/config/doctrine branch patch, so the
prompt routes to a mixed adversarial code + artifact review. Patch authority is
available only if the receiving controller has repo access and the operator
explicitly selects repo patch mode below. Otherwise, the reviewer writes
findings only.

This prompt does not run the review, does not accept any delegated diff, does
not make the route physically US-local, and does not create validation,
readiness, demand proof, Judgment evidence, or Product Lead evidence.
Non-claim phrase for any durable route-using artifact: US-parameterized is not
physically US-local.

## Launch Prompt

````text
You are the de-correlated controller for an Orca adversarial code/artifact review-and-patch efficacy pass.

## Commission

Review whether the submitted branch makes the right smallest-complete move after the proxy/VPN route proved operationally poor: keep the US-parameterized Google Search route as the default capture-efficacy route, enforce the mechanically checkable shell in code, and preserve the non-checkable physical-locality boundary in doctrine.

Do not evaluate or build a crawler, monitor, dashboard, score, proxy/VPN system, AEO/GEO product lane, durable-demand proof route, Judgment evidence route, or Product Lead action route.

Required durable review report path:
- docs/review-outputs/adversarial-artifact-reviews/search_surface_google_parameterized_us_route_enforcement_adversarial_review_patch_v0.md

Workspace:
- C:\Users\vmon7\Desktop\projects\orca\worktrees\search-param-us-enforcement

Expected branch:
- codex/search-param-us-enforcement

Base HEAD at prompt creation:
- c4cc9e3e3cb0a6f1b647575fd18e12d0cc9950d1

Dirty-state allowance:
- The current uncommitted branch diff is the review target.
- The prompt artifact itself may be present and untracked/modified; read it as commission context, not as a patch target unless the review cannot run without fixing the prompt.
- Do not create, clone, request, or switch to another worktree.
- If the named workspace or branch is unavailable, return `BLOCKED_TARGET_UNAVAILABLE`.

## Actor / Model-Family Receipt

Before reviewing or patching, record:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: operator_to_fill_repo_or_no_repo
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  same_vendor_rationale: required_if_same_vendor_sanity
  de_correlation_status: satisfied | blocked | limited
```

This is a who-constraint, not a runtime model recommendation. If the controller
is not de-correlated, return the limitation before findings and do not claim
cross-vendor discovery. Same-vendor sanity may still produce advisory findings,
but it cannot claim the no-new-seam discovery bar.

## Output Mode And Permission

Output mode: `review-report`.

Template kind: review.

Edit permission:
- `repo` access mode with operator-selected patch execution: patch-only inside the editable scope below.
- `no_repo` access mode or no explicit patch selection: read-only; write findings only.

Do not stage, commit, push, open a PR, run live Google Search, invoke browsers,
use proxies/VPNs, perform web research, or edit outside the editable scope.

Editable scope if and only if repo patch mode is selected:
- .agents/hooks/check_search_surface_google_route.py
- .claude/settings.json
- .codex/hooks.json
- .github/workflows/ci.yml
- .agents/hooks/README.md
- .agents/workflow-overlay/validation-gates.md
- docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md
- docs/workflows/orca_repo_map_v0.md

Read-only context:
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
- docs/workflows/orca_repo_map_v0.md
- docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md

## Source-Gated Method Contract

REFERENCE-LOAD these methods before source loading:
- workflow-deep-thinking
- workflow-code-review
- workflow-adversarial-artifact-review

Do not APPLY any method yet. Use them only to prepare a neutral source-reading lens.

SOURCE-LOAD the required Orca sources and target files. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, source gaps, excluded sources, source conflicts, and dirty/untracked notes.

Only after `SOURCE_CONTEXT_READY`, APPLY:
1. workflow-deep-thinking to frame the boundary problem, false-success modes, overclaim risk, and efficacy criteria.
2. workflow-code-review to review the Python hook, hook event parsing, CLI modes, strict mode, CI integration, and JSON wiring.
3. workflow-adversarial-artifact-review to review the decision record, validation-gate note, repo-map note, and claim boundaries.

If a required method is unavailable, unresolved, or cannot be applied after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` or a clearly marked advisory-only partial result. Do not emulate a formal lane inline.

## Efficacy Bar

The branch is effective only if it materially reduces the chance that future Orca agents will:

- preserve a Google Search capture URL without `hl=en`, `gl=us`, and `pws=0`;
- call US-parameterized capture physically US-local without separate evidence;
- commit Google block pages with visible exit-IP content into durable docs;
- mistake route-shape enforcement for physical locality, source sufficiency, validation, readiness, demand proof, Judgment evidence, or Product Lead evidence;
- default back to proxy/VPN infrastructure after the observed side-by-side block;
- turn Search-Surface MGT capture-efficacy work into crawler, monitor, dashboard, score, durable-demand proof, or product-lane work.

The branch is ineffective if the checker is too brittle to catch the main failure modes, too broad and likely to block ordinary durable docs, wired in a way that will not run, or paired with doctrine that lets the same overclaim reappear in prose.

## Review Questions

Find material defects, false-success paths, false-blocking risks, missing validation, or doctrine drift. Focus especially on:

1. Does `check_search_surface_google_route.py` correctly scope durable docs and avoid `_inbox`, `_scratch`, snapshots, code, and unrelated historical backlog?
2. Does URL parsing catch real Google Search capture URLs without flagging non-capture Google surfaces that should remain out of scope?
3. Are the required params enforced robustly enough for changed durable docs?
4. Is the physical-locality non-claim detector broad enough without allowing weak substitutes?
5. Does the Google block-page/IP rule catch the dangerous durable-preservation case without storing or requiring sensitive proxy details?
6. Are `--hook`, `--changed --strict`, `--strict`, `--check`, and `--selftest` behavior coherent and failure-visible?
7. Is the CI diff-scoped gate correct, and does it fail open only where the repo's existing forward-only gate pattern permits?
8. Are `.claude/settings.json` and `.codex/hooks.json` wired to the correct command paths for their harnesses?
9. Does the doctrine record state the route decision and non-claims sharply enough?
10. Do validation-gates, repo map, and hook README point future agents to the rule without duplicating or weakening it?
11. Is any broader Capture, Scanning, Judgment, Product Lead, source-capture playbook, or prompt-orchestration update actually required for this pilot, or would that be scope creep?
12. Are the proposed validation commands sufficient for this branch?

## Patch Boundary

Patch only material issues that affect enforcement efficacy, route doctrine, harness wiring, or discoverability within the editable scope. Keep fixes smallest-complete.

If the correct fix requires a new Google runner, proxy/VPN infrastructure, browser automation, source-capture packet schema, scoring system, durable-demand doctrine, Judgment lane change, or Product Lead route, do not patch. Return `NEEDS_ARCHITECTURE_PASS` or `OUT_OF_SCOPE_FOR_THIS_PATCH` with evidence.

## Required Validation

Run these after any patch, or state exactly why a command could not be run:

```powershell
python .agents/hooks/check_search_surface_google_route.py --selftest
python .agents/hooks/check_search_surface_google_route.py --strict --base main
python -m json.tool .claude/settings.json
python -m json.tool .codex/hooks.json
python .agents/hooks/check_prompt_provenance.py --selftest
python .agents/hooks/check_repo_map_freshness.py --changed
python .agents/hooks/header_index.py --strict --base main
python .agents/hooks/check_map_links.py --strict
git diff --check
```

Use a short timeout for the new checker smoke before any broader gate. Do not run live Google, web, proxy, VPN, browser, or capture-packet commands.

## Output Contract

Write the durable review report to:
- docs/review-outputs/adversarial-artifact-reviews/search_surface_google_parameterized_us_route_enforcement_adversarial_review_patch_v0.md

The report must include:

1. `reviewed_by` and `authored_by`; use `unrecorded` only when the operator did not supply the value.
2. The actor/model-family receipt above.
3. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Findings first, ordered by severity.
5. For each finding: affected file/line, evidence, risk, minimum closure condition, whether you patched it, and next authorized action.
6. Patch summary, if any.
7. Unified diff, if any.
8. Validation commands and observed outputs, or not-run reasons.
9. Residual risk.
10. Verdict: `PATCHED_FOR_CA_ADJUDICATION`, `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, `ADVISORY_ONLY_NO_REPO`, or `BLOCKED`.

Your findings, diff, and verdict are decision input only. The Chief Architect/home lane adjudicates what is kept.
````

## Prompt Authoring Receipt

```yaml
orca_prompt_preflight:
  output_mode: review-report
  template_kind: review
  template_source: prompt-orchestrator_full_contract_plus_orca_review_doctrine
  edit_permission: patch-only_if_repo_access_mode_selected_else_read-only
  target_branch: codex/search-param-us-enforcement
  target_workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\search-param-us-enforcement
  dirty_state_allowance: current branch diff is the review target
  review_report_destination: docs/review-outputs/adversarial-artifact-reviews/search_surface_google_parameterized_us_route_enforcement_adversarial_review_patch_v0.md
  doctrine_change: no_new_doctrine_from_prompt; prompt commissions review of the branch doctrine/enforcement change
  runtime_model_routing: not_bound_not_recommended
  validation_expectation: receiver runs listed checks after any patch
  non_claims:
    - prompt not executed
    - not validation
    - not readiness
    - not physical-locality proof
    - not demand proof
    - not Judgment evidence
    - not Product Lead evidence
```
