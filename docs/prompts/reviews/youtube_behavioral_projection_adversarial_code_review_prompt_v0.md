# YouTube Behavioral Projection Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated adversarial implementation/code
  review of PR #424, the YouTube behavioral projection bridge.
use_when:
  - Commissioning an independent reviewer to inspect PR #424 before the owner keeps or lands it.
  - Checking the review source binding, de-correlation bar, and output contract for this PR review.
authority_boundary: retrieval_only
source_repo: https://github.com/eric-foo/orca
source_pr: https://github.com/eric-foo/orca/pull/424
source_branch: codex/youtube-behavioral-completion
source_base: main at bba52fd54641f40534ed83d13a794d46f770fa5d
source_head: 6c225137a0961959cc46f22b8bab2b29b88660fc
target_blob_ids:
  orca-harness/youtube_capture/behavioral_projection.py: b1ddcf19f94655fbec7fda572e3a3b126d987e8d
  orca-harness/tests/unit/test_youtube_behavioral_projection.py: 4e114a62e9c278e22a8a8231aa38916d016bc9b3
intended_report_path: docs/review-outputs/youtube_behavioral_projection_adversarial_code_review_v0.md
stale_if:
  - PR #424 head differs from 6c225137a0961959cc46f22b8bab2b29b88660fc.
  - Either target blob id differs from the values above.
  - The receiver cannot inspect the pinned source and diff directly.
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write for this prompt only; receiving reviewer is read-only
  target_scope: PR #424 implementation/code diff for the two target files only
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

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/youtube_behavioral_projection_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local repo-code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Route decision: explicit `workflow-delegated-review-patch` was invoked, but the target is a multi-file implementation/code diff. Per `.agents/workflow-overlay/delegated-review-patch.md`, do not stretch the provisional single-artifact review-and-patch convention. Route through adversarial implementation/code review instead.
- Edit permission: reviewer is read-only. Do not edit files, emit patch queue, commit, push, open PRs, or run live capture.
- Reviews: findings-first advisory code review. Do not claim formal PASS, readiness, approval, validation, or mandatory remediation authority.
- Doctrine change: none authorized. If a doctrine or architecture change appears required, flag `NEEDS_ARCHITECTURE_PASS`; do not patch.

## Commission

Run a de-correlated adversarial code review of PR #424, commit `6c225137a0961959cc46f22b8bab2b29b88660fc`, before the home lane treats the YouTube behavioral projection bridge as keepable. The review purpose is to find blocker or major correctness, scope, validation, boundary, or false-confidence issues in the projection bridge and tests.

Target files:

- `orca-harness/youtube_capture/behavioral_projection.py`
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py`

Do not review or redesign the whole shared capture core. Do not require IG and YouTube to use the same acquisition method, priority ladder, data shape, storage schema, or browser machinery. The behavioral objective is enough parity for downstream capture judgment: availability, transcript modality, metadata/comment visibility, extraction eligibility, failures, and correlation must be explicit enough to compare and adjudicate.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor/model lineage to claim `cross_vendor_discovery`.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing or same-vendor, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` if available. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Confirm the checked source is PR #424 at head `6c225137a0961959cc46f22b8bab2b29b88660fc`. If unavailable, wrong revision, or dirty in a way that changes target files, return `SOURCE_CONTEXT_INCOMPLETE`.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and unavailable tools.
5. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce findings-first implementation/code review.
6. If `workflow-code-review` is unavailable, use findings-first advisory code-review semantics from this prompt and mark strict review claims `NOT_CLAIMED`.

## Required Reads

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`

Then inspect the pinned PR source:

```powershell
git status --short --branch
git rev-parse HEAD
git diff bba52fd54641f40534ed83d13a794d46f770fa5d..6c225137a0961959cc46f22b8bab2b29b88660fc -- orca-harness/youtube_capture/behavioral_projection.py orca-harness/tests/unit/test_youtube_behavioral_projection.py
git ls-tree 6c225137a0961959cc46f22b8bab2b29b88660fc -- orca-harness/youtube_capture/behavioral_projection.py orca-harness/tests/unit/test_youtube_behavioral_projection.py
```

Read adjacent context as needed, but do not widen the target:

- `orca-harness/youtube_capture/capture_youtube_v0.py`
- `orca-harness/youtube_capture/shorts_scroll_capture_v0.py`
- `orca-harness/source_capture/transcript/youtube_captions.py`
- `orca-harness/source_capture/transcript/caption_packet.py`
- `orca-harness/source_capture/transcript/asr_packet.py`
- `orca-harness/runners/run_transcript_product_extract.py`
- `orca-harness/source_capture/ig_reels_grid.py`
- `orca-harness/source_capture/ig_reels_deep_capture.py`
- `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
- `orca-harness/tests/unit/test_youtube_caption_product_extract.py`
- `orca-harness/tests/unit/test_transcript_product_lake.py`
- `orca-harness/tests/contract/test_no_llm_imports.py`

## Validation Evidence To Inspect

The author reported these checks passed:

```powershell
python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_youtube_behavioral orca-harness/tests/unit/test_youtube_behavioral_projection.py
python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_youtube_behavioral_existing orca-harness/tests/unit/test_youtube_caption_product_extract.py orca-harness/tests/unit/test_transcript_product_lake.py orca-harness/tests/contract/test_no_llm_imports.py
```

Reported outputs were `7 passed` and `20 passed`. You may rerun read-only tests if your environment permits. If you do not rerun them, report validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

- Does the projection bridge preserve true failure visibility, especially mixed `failed`, `not_attempted`, `present`, and `missing` states?
- Are captions and ASR represented as distinct transcript sources without duplicate anchor/source-key ambiguity?
- Does failed ASR become source-problem or noneligible posture where appropriate, instead of being hidden by caption success?
- Are metadata, comments, transcript, extraction, and video availability correlated by explicit keys or anchors, not by human convention?
- Does the code avoid importing Cleaning, ECR, LLM, live browser, network, persistence, or IG machinery?
- Does `rebuild_availability` stay opt-in and side-effect-free for callers that only project existing capture outputs?
- Do tests cover source-key mismatch, metadata/video mismatch, failed-ASR accounting, mixed rollups, and no-LLM import boundaries?
- Does the implementation stay YT-only and avoid locking the future shared core into YouTube-specific schema or IG machinery parity?

## Strict-Claim Boundary

This review is decision input only. Do not claim approval, readiness, validation, formal pass/fail, mandatory remediation, or patch authority. Do not emit `patch_queue_entry`.

If you find no blocker or major issue, say so and state residual risks or validation gaps. If you find an issue, findings lead the report and include:

- finding id
- severity as `blocker`, `major`, or `minor` for prioritization only, not formal Orca verdict authority
- target file and stable line or anchor
- evidence from the implementation
- concrete impact
- minimum closure condition
- next authorized action
- validation expectation

## Output Contract

Write the full review report to:

`docs/review-outputs/youtube_behavioral_projection_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- open questions and residual risk
- validation evidence inspected and validation not-run gaps
- review-use boundary: findings are decision input only, not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

After writing the report, return only a compact summary plus:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/youtube_behavioral_projection_adversarial_code_review_v0.md
  commission: adversarial implementation/code review of PR #424 YouTube behavioral projection bridge
  target:
    - orca-harness/youtube_capture/behavioral_projection.py
    - orca-harness/tests/unit/test_youtube_behavioral_projection.py
  authority: advisory implementation/code review; formal review verdict NOT_CLAIMED
  decision_criteria: behavioral completeness, failure visibility, source correlation, boundary hygiene, offline test adequacy
  evidence_summary: <short source-backed summary>
  reviewer_verdict: NOT_CLAIMED
  finding_ids: []
  minimum_closure_conditions: []
  next_authorized_action: home model adjudicates findings before keeping or landing PR #424
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not patch authority
    - not live capture execution
```
