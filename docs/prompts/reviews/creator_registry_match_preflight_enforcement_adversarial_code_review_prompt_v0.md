# Creator Registry Match Preflight Enforcement Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Delegated adversarial code review and bounded patch prompt for the Creator
  Registry match preflight enforcement lane.
use_when:
  - Reviewing the creator registry exact-match preflight implementation before merge.
  - Hardening the scan-to-capture duplicate-prevention turnstile.
authority_boundary: retrieval_only
```

## Prompt Preflight

- Output mode: `review-report`; write the review report to `docs/review-outputs/adversarial-artifact-reviews/creator_registry_match_preflight_enforcement_adversarial_code_review_v0.md`.
- Template kind: `review`.
- Edit permission: bounded patch-only inside the submitted PR/worktree scope; do not commit, push, merge, or open/close PRs.
- Target workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-preflight-enforcement`.
- Target branch: `codex/creator-registry-preflight-enforcement`.
- Base: `origin/main`.
- Review lane: code implementation review; invoke `workflow-code-review` if available. If unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` rather than silently claiming that lane ran.
- Prompt source: this file.

## Objective

Perform an adversarial implementation review of the Creator Registry match
preflight enforcement diff, then apply only bounded patches for confirmed
defects. The implementation is meant to stop duplicate new-capture attempts
before a cold scan/capture lane creates another creator/account record.

## Source-Gated Method Contract

REFERENCE-LOAD any required method instructions first. Do not APPLY review
methods before source readiness. Then SOURCE-LOAD the task sources below,
declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, and only then
APPLY the review method to produce findings and patches.

Required authority/source reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/review-lanes.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
- `orca-harness/runners/run_creator_registry_match_preflight.py`
- `orca-harness/tests/unit/test_creator_registry_match_preflight.py`
- `orca-harness/tests/unit/test_creator_profile_current_static_view.py`

Before reviewing, confirm and report:

- current branch and HEAD SHA;
- dirty state;
- diff against `origin/main`;
- whether the expected target files exist.

If the worktree, branch, or source state does not match the submitted target,
return a blocker before reviewing.

## Review Focus

Review against the intended MGT v0 enforcement contract:

- exact registry preflight uses the structured `creator_profile_current` JSON, not the human Markdown projection;
- `new_capture` is blocked for exact existing registry matches;
- ambiguous exact-key conflicts fail closed;
- duplicate candidates inside a scan batch are rejected;
- genuinely new candidates can proceed;
- output receipt carries enough reason codes and matched registry identity for a cold agent to act;
- no fuzzy identity, cross-platform proof, web search, registry mutation, capture execution, live API, LLM, or silver refresh is introduced;
- tests prove the dangerous paths, not only happy paths.

Treat these as high-value failure modes:

- a malformed candidate silently passes as `new_candidate`;
- a known profile URL/handle/account id fails to match because normalization is wrong;
- a batch with one blocked candidate returns success in a way that could start unsafe capture;
- exact keys matching two different registry rows do not become `ambiguous_match`;
- the receipt or usage note overclaims fuzzy/cross-platform/metric-refresh capability;
- the runner writes outputs but exits with a misleading status;
- validation only tests synthetic behavior and misses current committed registry rows.

## Patch Scope

You may patch only:

- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
- `orca-harness/runners/run_creator_registry_match_preflight.py`
- `orca-harness/tests/unit/test_creator_registry_match_preflight.py`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`

Anything outside that scope is read-only. Flag it; do not edit it.

Return `NEEDS_ARCHITECTURE_PASS` if the correct fix requires a broader identity
architecture, fuzzy resolver, public-handle linkage redesign, capture
orchestration, or registry schema change.

## Validation

After any patch, run the tight gates:

```powershell
python -m py_compile orca-harness\capture_spine\creator_profile_current\registry_match_preflight.py orca-harness\runners\run_creator_registry_match_preflight.py
python -m pytest -q orca-harness\tests\unit\test_creator_registry_match_preflight.py
python -m pytest -q orca-harness\tests\unit\test_creator_profile_current_static_view.py
python orca-harness\runners\run_creator_profile_current_materialize.py --check
python -m pytest -q orca-harness\tests\contract\test_no_llm_imports.py
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\header_index.py --strict --base origin/main
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_review_routing.py --strict --base origin/main
git diff --check origin/main..HEAD
```

If any command is not run, state why. Do not claim validation for commands you
did not observe.

## Output Contract

Write the review report to the output path named above, then return:

```yaml
review_patch_summary:
  status: completed | blocked
  target_confirmed: true | false
  target_head_sha_observed: ""
  patched: true | false
  recommendation: accept | patch_before_acceptance | needs_architecture_pass | blocked
  findings:
    - id:
      severity:
      file:
      issue:
      action:
  validation:
    - command:
      result:
  residual_risks:
    - ""
  owner_decisions_needed:
    - ""
```

Findings are decision input only. The home/CA lane adjudicates any returned diff
before keeping it.
