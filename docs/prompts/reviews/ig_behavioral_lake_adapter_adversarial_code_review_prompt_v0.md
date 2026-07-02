# IG Behavioral Lake Adapter Delegated Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: Repo-bound adversarial code review prompt for PR #441, the IG behavioral lake adapter.
use_when:
  - Commissioning a de-correlated adversarial implementation review of PR #441.
  - Reconstructing the target worktree, source pack, output contract, and non-claims for the IG behavioral lake adapter review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md
branch_or_commit: codex/ig-behavioral-lake-adapter @ 0265c0275bd30e7309f6ef53b287149c730058c9
stale_if:
  - PR #441 head commit changes.
  - The target files, Orca review rules, prompt rules, or IG behavioral sync contract change.
```

## Prompt Orchestrator Receipt

```yaml
output_mode: file-write prompt artifact plus paste-ready-chat copy
template_kind: review
template_source: workflow-prompt-orchestrator generic review template, Orca-bound by overlay prompt rules
review_route: workflow-deep-thinking then workflow-code-review after SOURCE_CONTEXT_READY
delegated_review_patch_route: >
  The user invoked workflow-delegated-review-patch, but the inferred target is a
  multi-file implementation/code diff, not a single high-stakes authored artifact.
  Per .agents/workflow-overlay/delegated-review-patch.md, route this as an
  adversarial implementation/code review unless a separate bounded patch-execution
  commission is explicitly bound.
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT-family, operator_to_confirm
  controller_model_family: operator_to_fill; must be a different upstream vendor or model lineage
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_confirm_before_review
repo_map_decision: not_needed
repo_map_reason: Accepted prompt and review-output folders are directly bound by the overlay; target files are named by PR #441.
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 plus delegated-review/prompt/review overlays and PR target sources
  edit_permission: read-only for receiving reviewer; docs-write only for this prompt artifact
  target_scope: PR #441 implementation diff
  dirty_state_checked: yes
  blocked_if_missing: target worktree, expected HEAD, review-output path, or required review skills
```

## Paste-Ready Review Prompt

You are the independent de-correlated controller for a repo-bound adversarial implementation/code review. This is a who-constraint, not a model recommendation: the controller/reviewer must be a different upstream vendor or model lineage from the author/home implementation lane. If you cannot establish that de-correlation, record the limitation and return a blocked or advisory-only result; do not claim cross-vendor discovery.

Actor-family receipt: author/home family is recorded as OpenAI / GPT-family, operator_to_confirm. Before review, the operator or controller must fill the controller family and confirm it differs. If that cannot be confirmed, do not claim the delegated cross-vendor discovery bar.

### Commission

Review PR #441, "Add IG behavioral lake adapter", for material bugs, behavioral-regression risk, false completeness, missing tests, or source-boundary violations. The implementation goal is behavioral completeness parity with the already-built YouTube behavioral lane, not identical IG/YT capture mechanics and not a shared-core refactor.

This is not a patch-execution commission. Do not edit files. Do not emit executor-ready patch queues. Findings may include advisory remediation direction, but any patching requires a later CA-adjudicated execution assignment.

### Required Worktree Preflight

- Source-of-truth worktree: `C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-behavioral-lake-adapter`
- Expected branch: `codex/ig-behavioral-lake-adapter`
- Expected HEAD: `0265c0275bd30e7309f6ef53b287149c730058c9`
- PR: `https://github.com/eric-foo/orca/pull/441`
- Dirty-state allowance: clean worktree only, no local modifications in target files.
- If the worktree is unavailable, the branch/HEAD does not match, or dirty state is violated, return the nearest blocker instead of reviewing a substitute checkout or summary.

### Required Output Binding

Write the durable review report to:

`docs/review-outputs/ig_behavioral_lake_adapter_adversarial_code_review_v0.md`

After writing the report, return only a compact summary plus the `review_summary` YAML shape from `.agents/workflow-overlay/communication-style.md`. If the report cannot be written, return `status: failed`, `review_location: chat_only_current_thread`, and `recommendation: blocked`; do not claim a report path exists.

The durable report must include `reviewed_by` and `authored_by`. If either value is not operator/tooling-supplied, use `unrecorded`; never fabricate provenance.

### Source-Gated Method Contract

1. REFERENCE-LOAD these method instructions only: `workflow-deep-thinking`, then `workflow-code-review`. Do not APPLY either method yet.
2. SOURCE-LOAD the task sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and exclusions.
4. Only after source readiness, APPLY `workflow-deep-thinking` to frame boundary problems, failure modes, and decision criteria.
5. Then APPLY `workflow-code-review` findings-first to the loaded source context.

### Required Source Pack

Read these authority and route sources:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`

Read these IG/YT behavioral contract sources:

- `docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md`
- `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
- `docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md`

Read the PR target and adjacent code sources:

- `orca-harness/source_capture/ig_reels_behavioral_lake.py`
- `orca-harness/source_capture/ig_reels_behavioral_projection.py`
- `orca-harness/tests/unit/test_ig_reels_behavioral_lake.py`
- `orca-harness/tests/unit/test_ig_reels_behavioral_projection.py`
- `orca-harness/tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py`
- `orca-harness/data_lake/root.py`
- `orca-harness/source_capture/transcript/ig_reels_audio_packet.py`
- `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
- `orca-harness/runners/run_ig_reels_product_extract.py`
- `orca-harness/cleaning/transcript_product_lake.py`

Inspect the PR diff against `origin/main`; do not rely on this prompt's summary as a substitute for source reads.

### Validation Evidence To Inspect

The implementation lane reported these checks before PR creation. Treat them as evidence to verify or contextualize, not as a reason to skip review:

- Focused local: `python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp .pytest_tmp_ig_behavioral_lake tests/unit/test_ig_reels_behavioral_lake.py tests/unit/test_ig_reels_behavioral_projection.py tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py -q` -> 17 passed.
- Broader IG local: `python -m pytest -p no:cacheprovider --override-ini addopts='' --basetemp .pytest_tmp_ig_behavioral_lake_full tests/unit/test_ig_reels_behavioral_lake.py tests/unit/test_ig_reels_behavioral_projection.py tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py tests/unit/test_ig_reels_product_extract.py tests/unit/test_source_capture_ig_reels_projection.py tests/unit/test_ig_reels_audio_packet.py tests/unit/test_ig_reels_deep_capture.py tests/unit/test_ig_reels_deep_capture_lake.py -q` -> 91 passed.
- GitHub CI: `orca-harness-tests` completed successfully on PR #441.

### Decision Criteria

Attack these axes:

- Does the lake adapter preserve the existing behavioral projection contract rather than inventing a new completeness rule?
- Does it discover real persisted IG records through durable lake paths and inject record IDs from path or record-set metadata without relying on body fields that real writers do not emit?
- Does it keep runtime/capture/ASR/product-extraction/LLM/network work out of the adapter?
- Does it surface residuals instead of hiding unreadable, incomplete, missing, or non-extraction-eligible states?
- Do the tests use real lake writer shapes enough to catch fake-pass body-only or synthetic-record assumptions?
- Does the implementation avoid prematurely creating a shared IG/YT core or copying YouTube capture mechanics into IG?
- Are there material untested paths, especially grid-derived inputs, product extraction correlation, deep-capture completion markers, adapter residual behavior, and corrupt/unreadable records?

### Report Shape

Write findings first, ordered by severity and grounded in file/line references. Use `critical`, `major`, and `minor` only as finding priority labels; they do not imply approval, readiness, validation, or mandatory remediation by themselves.

Each actionable finding must include:

- finding id;
- severity;
- file and line reference;
- why it matters;
- minimum_closure_condition;
- next_authorized_action.

Also include:

- non-findings that matter for CA adjudication;
- validation evidence inspected and validation gaps;
- residual risk;
- `review_summary` YAML at the top of the report and in the chat closeout.

Do not claim approval, readiness, merge approval, or validation beyond observed evidence. Review findings are decision input only; the CA/home model adjudicates what is kept.
