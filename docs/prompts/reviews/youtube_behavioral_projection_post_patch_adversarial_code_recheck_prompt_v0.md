# YouTube Behavioral Projection Post-Patch Adversarial Code Recheck Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated post-patch adversarial code recheck
  of PR #424 after home-lane closure of F-01 through F-04.
use_when:
  - Commissioning a different-vendor reviewer to re-check PR #424 after commit 7c7a64a8235741f65c4a1f03642019c437070b95.
  - Verifying whether accepted review findings F-01, F-02, F-03, and F-04 were closed or correctly residualized.
authority_boundary: retrieval_only
source_repo: https://github.com/eric-foo/orca
source_pr: https://github.com/eric-foo/orca/pull/424
source_branch: codex/youtube-behavioral-completion
source_base: main at bba52fd54641f40534ed83d13a794d46f770fa5d
source_head: 7c7a64a8235741f65c4a1f03642019c437070b95
prior_review_prompt: docs/prompts/reviews/youtube_behavioral_projection_adversarial_code_review_prompt_v0.md
prior_review_findings: [F-01, F-02, F-03, F-04]
target_blob_ids:
  orca-harness/youtube_capture/behavioral_projection.py: d38366fffdaed007fe5ba081d4f2214fc5a5730a
  orca-harness/tests/unit/test_youtube_behavioral_projection.py: 2fea059ac493da13f5528bf67f51c2089a4ab83a
  orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py: 86ee164e9645847909cbe92d346b8c529100c927
intended_report_path: docs/review-outputs/youtube_behavioral_projection_post_patch_adversarial_code_recheck_v0.md
stale_if:
  - PR #424 head differs from 7c7a64a8235741f65c4a1f03642019c437070b95.
  - Any target blob id differs from the values above.
  - The receiver cannot inspect the pinned source and diff directly.
```

## Thread Operating Target Continuity

This continues the active thread-local target: make YouTube the first complete reviewed behavioral lane, then use it to guide IG sync/core design. This target is orientation only, not source authority, validation evidence, readiness, approval, lifecycle completion, or edit permission.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write for this prompt only; receiving reviewer is read-only
  target_scope: PR #424 post-patch code recheck for F-01 through F-04 only
  dirty_state_checked: yes, prompt lane clean at creation
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/safety-rules.md
```

## Commission

Run a de-correlated, read-only adversarial code recheck of PR #424 at commit `7c7a64a8235741f65c4a1f03642019c437070b95`. This is a post-patch recheck, not a new broad review. Focus on whether the accepted prior findings were closed without new false-success paths:

- F-01: corrupt/unreadable YouTube packet during discovery no longer aborts healthy video projection and leaves visible source-discovery residual evidence.
- F-02: pure-projection no-acquisition/no-LLM import boundary is guarded for `youtube_capture/behavioral_projection.py` without wrongly banning acquisition modules elsewhere in `youtube_capture/`.
- F-03: stale availability-index behavior is explicit and covered; default projection remains read-only and rebuild remains opt-in.
- F-04: targeted offline tests cover the decision-relevant closure branches.

Do not review or redesign the shared capture core. Do not require IG and YouTube to share acquisition method, priority ladder, storage schema, or browser machinery. Do not run live capture unless a source-backed reason shows the offline closure evidence cannot answer the recheck question.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the patch lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor/model lineage to claim `cross_vendor_discovery`.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing or same-vendor, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` if available. Do not APPLY them yet.
2. Read required Orca authority: `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/safety-rules.md`.
3. Confirm the checked source is PR #424 at head `7c7a64a8235741f65c4a1f03642019c437070b95` and that target blob IDs match the header. If not, return `SOURCE_CONTEXT_INCOMPLETE`.
4. Inspect the PR diff and the three target files. Read adjacent context only if needed to adjudicate F-01 through F-04 closure.
5. Only after source readiness, APPLY deep-thinking to look for missed closure or new false-success paths, then APPLY workflow-code-review for findings-first recheck.

## Validation Evidence To Inspect

The home lane reported these commands passed after the patch:

```powershell
python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_youtube_behavioral_patch orca-harness/tests/unit/test_youtube_behavioral_projection.py
python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_youtube_behavioral_contract orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py
python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_youtube_behavioral_existing orca-harness/tests/unit/test_youtube_caption_product_extract.py orca-harness/tests/unit/test_transcript_product_lake.py orca-harness/tests/contract/test_no_llm_imports.py
git diff --check
git diff --cached --check
python .agents\hooks\check_repo_map_freshness.py --changed
```

Reported outputs were `9 passed`, `3 passed`, `20 passed`, and clean diff/repo-map checks. Treat these as author-supplied unless independently rerun.

## Output Contract

Write the full recheck report to:

`docs/review-outputs/youtube_behavioral_projection_post_patch_adversarial_code_recheck_v0.md`

The report must include `reviewed_by`, `authored_by: gpt-family-codex`, `de_correlation_bar`, source-read ledger, `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, findings first, closure status for F-01 through F-04, validation evidence inspected, validation not-run gaps, and review-use boundary. Do not emit `patch_queue_entry`; do not edit files; do not claim approval, validation, readiness, or patch authority.

After writing the report, return only a compact summary plus:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/youtube_behavioral_projection_post_patch_adversarial_code_recheck_v0.md
  commission: post-patch adversarial code recheck of PR #424 F-01 through F-04 closure
  target:
    - orca-harness/youtube_capture/behavioral_projection.py
    - orca-harness/tests/unit/test_youtube_behavioral_projection.py
    - orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py
  authority: advisory implementation/code recheck; formal review verdict NOT_CLAIMED
  decision_criteria: accepted finding closure without new false-success paths
  evidence_summary: <short source-backed summary>
  reviewer_verdict: NOT_CLAIMED
  finding_ids: []
  minimum_closure_conditions: []
  next_authorized_action: home model adjudicates recheck before keeping or landing PR #424
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not patch authority
    - not live capture execution
```
