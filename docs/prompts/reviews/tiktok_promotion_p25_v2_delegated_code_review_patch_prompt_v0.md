# TikTok Promotion P25 v2 Delegated Code Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: delegated_review_dispatch_prompt
scope: >
  Operator-courier commission for a different-vendor controller to review and
  bounded-patch the TikTok bottom-quartile promotion-policy v2 implementation.
use_when:
  - Dispatching the commissioned review before the implementation PR is merged.
authority_boundary: retrieval_only
output_mode: paste-ready-chat
branch_or_commit: codex/tiktok-promotion-p25-v2 implementation revision 3cb0e140013fe428fbbad34d8d31a4b347d65655
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
  effective_target: C:\tmp\forseti-tiktok-promotion-p25-v2
  branch: codex/tiktok-promotion-p25-v2
  required_revision: 3cb0e140013fe428fbbad34d8d31a4b347d65655
  revision_mode: exact
  direct_write_proof: receiver_to_observe
```

Before reading target source, state your upstream model vendor and model family. You are eligible only if the upstream vendor is different from OpenAI and you have direct read/write access to the exact repository worktree below. Same-vendor, unknown-lineage, no-repo, self, and Codex-managed substitutes are invalid. This is a who-constraint, not a model recommendation. If eligibility cannot be proven, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` or `BLOCKED_DIRECT_REPO_ACCESS` and stop.

Goal and done condition:
- Review whether TikTok promotion policy v2 truly excludes only creators weak on both calibrated p25 dimensions, records an exact reason in decision output and append-only Frontier state, preserves owner/non-performance disposition precedence, keeps batch evaluation read-only, and replays idempotently.
- Done means you either find no material false-success or persistence seam, or leave a bounded uncommitted patch that closes each local material finding and passes the named validation. Your findings, diff, and verdict remain claims for the home Chief Architect to adjudicate.

Receiver binding and revision:
- repository: `https://github.com/eric-foo/forseti.git`
- effective target worktree: `C:\tmp\forseti-tiktok-promotion-p25-v2`
- branch: `codex/tiktok-promotion-p25-v2`
- base revision: `a9a50f2c0fc36356d3a4b8994880f42b3df47f41`
- required implementation revision: `3cb0e140013fe428fbbad34d8d31a4b347d65655`
- revision_mode: `exact`
- carrier HEAD: receiver_to_observe; it may be a later prompt-only commit, but the required implementation revision must be its ancestor and the Named Target Set must be byte-unchanged since that revision
- clean-at-bind: required; only your commissioned edits may make the tree dirty afterward
- no concurrent writer: required

Your first action is one combined binding check:

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse 3cb0e140013fe428fbbad34d8d31a4b347d65655
git merge-base --is-ancestor 3cb0e140013fe428fbbad34d8d31a4b347d65655 HEAD
git diff --name-only 3cb0e140013fe428fbbad34d8d31a4b347d65655..HEAD -- forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier_selector.py forseti-harness/tests/unit/test_tiktok_creator_onboarding.py forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_lake_authority_contract_v1.md
```

Proceed only if the branch matches, the required revision resolves exactly, it is an ancestor of carrier HEAD, the named-target diff since it is empty, the tree is clean, and no concurrent writer exists. Otherwise return `BLOCKED_TARGET_STATE` with observed facts. Do not review a summary, pasted diff, alternate checkout, or recreated source as a substitute.

Read these authority pointers before judging behavior:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`, especially `delegated_code_review_and_patch`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`, specifically `environment_baseline`, `lifecycle_hard_stop`, and `decorrelation_commission`
- the actual implementation diff: `git diff a9a50f2c0fc36356d3a4b8994880f42b3df47f41..3cb0e140013fe428fbbad34d8d31a4b347d65655`

Use `workflow-code-review` as the review method if it is available in your runtime. If it is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not silently emulate a stricter lane.

Named Target Set — these are the only patchable files:
- `[policy]` `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py`
- `[runner]` `forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py`
- `[policy-tests]` `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier_selector.py`
- `[runner-tests]` `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`
- `[contract]` `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_lake_authority_contract_v1.md`

Everything outside that set is read-only and flag-only. Do not edit generated inventory, other tests, workflow sources, AGENTS.md, lake data, or production state. A fix requiring an unnamed file is a finding for home adjudication, not permission to widen scope.

Attack at least these plausible near-misses:
1. The threshold changed to p25 but the gate still effectively requires both dimensions, mishandles equality, or promotes a missing-quality/weak-weekly candidate.
2. Decision JSON explains non-promotion, but explicit single-handle operation fails to persist the same semantics to Frontier or mutates Frontier during an unscoped batch run.
3. Exact replay creates a new head, or a performance reclassification can silently supersede rejection, `non_us_market`, `owner_choice`, or another non-performance disposition.
4. A failure is reported for the wrong reason—for example, an earlier Registry/browser preflight masks the promotion or persistence boundary under test.
5. Pinned posts, cadence capping, or the recovered calibration provenance drift while the apparent threshold assertions still pass.
6. The runner writes operational state before it has proven the explicit handle appears exactly once in the evaluated grids, or a partial output/lake failure can be mistaken for complete success.

Patch authority:
- Patch only a local, decision-consistent defect inside the Named Target Set.
- Keep edits uncommitted.
- Preserve append-only lake semantics and visible failures.
- Do not add a database, generic policy framework, calibration service, approval workflow, or new browser behavior.
- If the defect is architectural or needs scope expansion, revert any partial patch and return `NEEDS_ARCHITECTURE_PASS` with findings only.

Required validation from the worktree root:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider --basetemp C:\tmp\pytest_tiktok_promotion_p25_delegate -q forseti-harness\tests\unit\test_creator_frontier_dispositions.py forseti-harness\tests\unit\test_creator_registry_lake.py forseti-harness\tests\unit\test_creator_registry_onboarding.py forseti-harness\tests\unit\test_tiktok_creator_discovery_frontier.py forseti-harness\tests\unit\test_tiktok_creator_discovery_frontier_selector.py forseti-harness\tests\unit\test_tiktok_creator_onboarding.py forseti-harness\tests\contract\test_capture_runner_lake_seam_coverage.py forseti-harness\tests\contract\test_data_lake_inventory_gate.py
python .agents\hooks\check_shared_helper_duplication.py --hook
git diff --check
```

Also repeat a browser-free temporary-lake dogfood using these already captured inputs when present:
- `C:\tmp\forseti-swole-fragrance-promotion-grid-20260722\swole_fragrance.grid.json`
- `C:\tmp\forseti-apfrags-promotion-grid-20260722-1836\apfrags.grid.json`

Seed each temporary-lake candidate with a current `deferred/low_potential/new_signal` v1 disposition, run the explicit v2 promotion path, and verify exactly two current `eligible/normal/other` heads, each superseding exactly one prior record. Swole must clear both p25 dimensions; Apfrags must clear weekly reach alone. Never resolve or write `F:\forseti-data-lake`. If a machine-local input is absent, report that dogfood `NOT_RUN` rather than substituting production or inventing success.

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
