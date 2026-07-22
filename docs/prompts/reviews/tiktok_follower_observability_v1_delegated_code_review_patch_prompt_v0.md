# TikTok Follower Observability v1 Delegated Code Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: delegated_review_dispatch_prompt
scope: >
  Operator-courier commission for a different-vendor controller to review and
  bounded-patch the TikTok follower-aware promotion observability implementation.
use_when:
  - Dispatching the commissioned review before the implementation PR is merged.
authority_boundary: retrieval_only
output_mode: paste-ready-chat
branch_or_commit: codex/tiktok-follower-observability-v1 implementation revision 2909672627d5e3ff26f05396a96e839c05a7144b
stale_if:
  - The named implementation files change after the pinned revision and before review binding.
  - The branch is merged, closed, rebased, or concurrently written before review binding.
```

## Paste-ready operator courier prompt

````text
You are the independent controller for a Forseti delegated code review-and-bounded-patch pass.

This prompt is preparation-only until you bind as an eligible receiver.

Commission receipt:
```yaml
target_kind: delegated_code_review_and_patch
author_vendor: OpenAI
delegate_vendor: operator_to_fill
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
access: repo
delivery: operator_courier_only
execution_route: five_phase_fast_path_if_eligible
review_diff_route: review_report_mechanics_if_durable_report_embeds_diff
de_correlation_bar: cross_vendor_discovery
dispatch_mode: external_controller_courier
receiver_binding:
  receiver_class: receiver_to_bind
  effective_target: C:\tmp\forseti-tiktok-follower-observability-v1
  branch: codex/tiktok-follower-observability-v1
  required_revision: 2909672627d5e3ff26f05396a96e839c05a7144b
  revision_mode: exact
  direct_write_proof: receiver_to_observe
```

Before reading target source, state your upstream model vendor and model family. You are eligible only if the upstream vendor is different from OpenAI and you have direct read/write access to the exact repository worktree below. Same-vendor, unknown-lineage, no-repo, self, and Codex-managed substitutes are invalid. This is a who-constraint, not a model recommendation. If eligibility cannot be proven, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` or `BLOCKED_DIRECT_REPO_ACCESS` and stop.

Goal and done condition:
- Review whether TikTok promotion Stage 1 follower observability exposes follower count, coarse follower band, and reliable weekly reach per 1,000 followers in promotion decisions and append-only Frontier notes without changing promotion/defer decisions, ranking, Registry behavior, or production lake state.
- Done means you either find no material false-success or persistence seam, or leave a bounded uncommitted patch that closes each local material finding and passes the named validation. Your findings, diff, and verdict remain claims for the home Chief Architect to adjudicate.

Receiver binding and revision:
- repository: `https://github.com/eric-foo/forseti.git`
- effective target worktree: `C:\tmp\forseti-tiktok-follower-observability-v1`
- branch: `codex/tiktok-follower-observability-v1`
- base revision: `1ff9fe27cb799ecd2a87112e87602e6bf89db10d`
- required implementation revision: `2909672627d5e3ff26f05396a96e839c05a7144b`
- revision_mode: `exact`
- carrier HEAD: receiver_to_observe; it may be a later prompt-only commit, but the required implementation revision must be its ancestor and the Named Target Set must be byte-unchanged since that revision
- clean-at-bind: required; only your commissioned edits may make the tree dirty afterward
- no concurrent writer: required

Your first action is one combined binding check:

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse 2909672627d5e3ff26f05396a96e839c05a7144b
git merge-base --is-ancestor 2909672627d5e3ff26f05396a96e839c05a7144b HEAD
git diff --name-only 2909672627d5e3ff26f05396a96e839c05a7144b..HEAD -- forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier_selector.py forseti-harness/tests/unit/test_tiktok_creator_onboarding.py forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_lake_authority_contract_v1.md
```

Proceed only if the branch matches, the required revision resolves exactly, it is an ancestor of carrier HEAD, the named-target diff since it is empty, the tree is clean, and no concurrent writer exists. Otherwise return `BLOCKED_TARGET_STATE` with observed facts. Do not review a summary, pasted diff, alternate checkout, or recreated source as a substitute.

Read these authority pointers before judging behavior:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`, especially `delegated_code_review_and_patch`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/validation-gates.md`
- the actual implementation diff: `git diff 1ff9fe27cb799ecd2a87112e87602e6bf89db10d..2909672627d5e3ff26f05396a96e839c05a7144b`

Use `workflow-code-review` as the review method if it is available in your runtime. If it is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not silently emulate a stricter lane.

Named Target Set - these are the only patchable files:
- `[policy]` `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py`
- `[runner]` `forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py`
- `[policy-tests]` `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier_selector.py`
- `[runner-tests]` `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`
- `[contract]` `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_lake_authority_contract_v1.md`

Everything outside that set is read-only and flag-only. Do not edit generated inventory, other tests, workflow sources, AGENTS.md, lake data, or production state. A fix requiring an unnamed file is a finding for home adjudication, not permission to widen scope.

Attack at least these plausible near-misses:
1. The new follower diagnostics change promotion/defer decisions, reason codes, cleared thresholds, ranking, or replay behavior.
2. Follower counts that are missing, zero, boolean, malformed, or absent from `profile_metrics` are treated as real values or block promotion.
3. Coarse follower bands mishandle exact boundaries at 10,000, 50,000, or 250,000 followers.
4. `reliable_weekly_reach_per_1k_followers` is computed from rounded weekly reach instead of the decision value, divides by the wrong denominator, or emits a misleading value when followers are unavailable.
5. Decision JSON contains follower diagnostics but the explicit single-handle Frontier write omits or changes them in durable lake notes.
6. The contract implies follower diagnostics are a new promotion gate, calibration, or production-readiness claim rather than Stage 1 observability.

Patch authority:
- Patch only a local, decision-consistent defect inside the Named Target Set.
- Keep edits uncommitted.
- Preserve append-only lake semantics and visible failures.
- Do not add a database, calibration service, follower-band threshold, policy framework, approval workflow, or new browser behavior.
- If the defect is architectural or needs scope expansion, revert any partial patch and return `NEEDS_ARCHITECTURE_PASS` with findings only.

Required validation from the worktree root:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider --basetemp C:\tmp\pytest_tiktok_follower_obs_delegate -q forseti-harness\tests\unit\test_tiktok_creator_discovery_frontier_selector.py forseti-harness\tests\unit\test_tiktok_creator_onboarding.py
python .agents\hooks\check_shared_helper_duplication.py --hook
git diff --check
```

Also repeat a browser-free temporary-lake dogfood using these already captured inputs when present:
- `C:\tmp\forseti-swole-fragrance-promotion-grid-20260722\swole_fragrance.grid.json`
- `C:\tmp\forseti-apfrags-promotion-grid-20260722-1836\apfrags.grid.json`

Seed each temporary-lake candidate with a current `deferred/low_potential/new_signal` v1 disposition, run the explicit promotion path, and verify exactly two current `eligible/normal/other` heads whose notes carry follower diagnostics. Swole must still clear both p25 dimensions and report `followers=66800`, `follower_band=50k_250k`; Apfrags must still clear weekly reach alone and report `followers=46500`, `follower_band=10k_50k`. Never resolve or write `F:\forseti-data-lake`. If a machine-local input is absent, report that dogfood `NOT_RUN` rather than substituting production or inventing success.

Run real validation after any patch. Report every failure and every not-run item without masking it. Do not claim deployment, production readiness, approval, or merge readiness.

Lifecycle hard stop:
- Do not commit, amend, push, open/update/close a PR, merge, stash, reset, clean, delete, retire a worktree, mutate production lake state, or perform repository hygiene.
- Stop after leaving the bounded working-tree diff and returning the review packet. The home Chief Architect alone adjudicates what is kept and reruns final validation before landing.

Return exactly one `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` with:
1. `receiver_receipt`: observed vendor/model family, de-correlation result, access proof, worktree, branch, carrier HEAD, reviewed implementation revision, clean-state and no-concurrent-writer observations.
2. `findings`: severity, confidence, target label/path/lines, concrete failure mode, neutral source citations, status `patched` or `flag_only`, minimum closure condition, and next authorized action.
3. `considered_and_defended`: attacked paths that held, with concise evidence.
4. `working_tree_diff`: complete diff and per-file summary; say `none` if unchanged.
5. `validation`: exact commands, exit codes/counts, dogfood facts, failures, and not-run items.
6. `verdict`: findings-first and explicitly subordinate to home adjudication.
7. `residual_risk`: remaining uncertainty and untested boundaries.
8. `adjudicator_next_move`: accept/modify/reject each finding and patch, rerun affected validation, then decide lifecycle action.

The returned diff, citations, and verdict are decision input only. Keep nothing by inertia.
````
