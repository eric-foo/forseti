# Cleaning Spine Live E2E Adversarial Code/Evidence Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Adversarial read-only review prompt for the Cleaning Spine live capture-to-ECR-to-Cleaning smoke implementation and run evidence.
use_when:
  - Commissioning a de-correlated reviewer to inspect the Cleaning Spine live E2E attempt and linked implementation changes.
  - Checking whether live raw capture, ECR receipts, Cleaning handles, and failure findings are truthfully connected without overclaiming readiness.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
```

## Orca Prompt Preflight

- output_mode: review-report; report destination `docs/review-outputs/cleaning_spine_live_e2e_adversarial_code_evidence_review_v0.md`.
- template_kind: review; custom mixed code/evidence prompt authored through `workflow-prompt-orchestrator` because the project registry does not bind a repo-code-review template and the target is not eligible for single-artifact delegated-review-patch.
- edit_permission: read-only for the reviewer. No patch queue and no source edits are authorized by this prompt.
- workspace: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`
- expected_branch: `codex/cleaning-spine-continuation`
- expected_head: `bc950cdfeeb3a02f33bf52217d71e049aa9093f2`
- dirty_state_allowance: dirty worktree expected; modified and untracked files listed below are in scope. Other dirty files are read-only context unless the reviewer proves they affect the target.
- agents_read: yes; `AGENTS.md` was fresh-read before this prompt was written.
- overlay_read: yes; `.agents/workflow-overlay/README.md` was fresh-read before this prompt was written.
- source_pack: custom S3 target-deepening: Orca overlay prompt/review/delegation rules, implementation diff targets, and live run evidence JSONs.
- repo_map_decision: not_needed for prompt routing; the user and active lane named the Cleaning Spine target, and the relevant files are in the current diff/run root.
- controlling_source_state: dirty and untracked target files are expected; do not treat dirty state as proof of completion, readiness, or acceptance.
- source_hierarchy: current user instruction, `AGENTS.md`, `.agents/workflow-overlay/**`, then named code/tests/run artifacts.
- external_source_boundary: no public web lookup is authorized or needed for this review. Inspect local captured packet artifacts only.
- doctrine_change: none intended by this prompt. If the reviewer finds doctrine drift, report it as a finding, do not patch doctrine.

## Why This Is Not A Strict Delegated-Review-Patch Target

The user invoked `workflow-delegated-review-patch` after item 5. Orca's overlay makes that provisional convention available only for an explicit CA commission on a single high-stakes authored artifact. This target is a multi-file implementation/code diff plus ignored live-run evidence, so the strict delegated-review-patch lane is non-eligible. Route the work as adversarial code/evidence review instead.

Preserve the de-correlation who-constraint as a review-quality axis: if the operator wants cross-vendor discovery, the receiving reviewer should be from a different upstream vendor/model lineage than the author/home family. This is a who-constraint, not a runtime model recommendation. If that cannot be established, record `de_correlation_bar: same_vendor_sanity` or `self_fallback` and state the limitation.

## Objective

Review whether the item 5 live capture-to-ECR-to-Cleaning smoke and the supporting implementation truthfully preserve the raw-to-cleaned linkage, ECR coupling, and failure visibility. The review must decide whether the code or run evidence lets bad live captures masquerade as usable Cleaning substrate, overclaims E2E readiness, loses raw/projection/ECR anchors, or hides the fact that retail PDP capture failed while Reddit capture succeeded.

Goal: make the Cleaning Spine live smoke honest enough to guide the next hardening decision.

Done looks like: a reviewer can cite the raw local evidence and code paths, state whether the current implementation preserves or overclaims the source-to-Cleaning chain, and name the smallest closure conditions for any blocker or major issue.

## Required Method Sequence

1. REFERENCE-LOAD `workflow-deep-thinking`, `workflow-code-review`, and `workflow-adversarial-artifact-review`. Do not APPLY them yet.
2. SOURCE-LOAD the required source context below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY deep-thinking to frame failure modes, then APPLY:
   - `workflow-code-review` for implementation code/tests and diff behavior.
   - `workflow-adversarial-artifact-review` for prompt/run-evidence claims and review-report hygiene.
5. If either review skill is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` for that portion and do not silently emulate a strict lane.

## Required Source Reads

Authority and review rules:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`

Implementation/code targets:
- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/tests/unit/test_retail_pdp_projection.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/tests/unit/test_cleaning_core.py`
- `docs/workflows/orca_repo_map_v0.md`

Live run evidence:
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/capture_ecr_cleaning_smoke_manifest.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/reddit_batch/batch_summary.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/stitched/smoke_summary.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/stitched/cleaning_packet.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/stitched/ecr_source_side_receipts.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/retail/sephora/retail_pdp_projection.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/retail/ulta/retail_pdp_projection.json`
- `orca-harness/_test_runs/cleaning_spine_live_e2e_20260621/retail/amazon/retail_pdp_projection.json`

## Evidence Hash Pins

- `stitched/smoke_summary.json`: `DB1A4B7B266EB6430013B7D924759F9E29C502ABD1DCA4756893315923B9771D`
- `stitched/cleaning_packet.json`: `78743DF262409F6CC3A2E9AEFEEC8CA640B25E6539721F8D630DF33D5EAF6222`
- `stitched/ecr_source_side_receipts.json`: `7461E2C086D42A3405B6F9C5BE0ECFC72E6EE5A00E8F77586180EC627DC3972F`
- `reddit_batch/batch_summary.json`: `04DBE77A6E2C13F5013EF32CED1CF18DFF84DC41266CB947C50A2ED02A580617`
- `retail/sephora/retail_pdp_projection.json`: `D35E310347D05BE3331E5DA27D1322690E9B8952797B507A30EBF50E8CF0AC44`
- `retail/ulta/retail_pdp_projection.json`: `263196B326AD006F1070FB3856A6043A46887FCECC0E270A4CBC2EBAA616A626`
- `retail/amazon/retail_pdp_projection.json`: `2D402AA0784F710050C92473E4D818C5262709BF6A2828C2A6A1252039D7C55C`

If a hash differs, report `SOURCE_CONTEXT_INCOMPLETE` for the changed evidence before making strict claims about the run.

## Known Run Facts To Verify, Not Trust

- The stitcher emitted a `CleaningPacket` that validates under `cleaning.models.CleaningPacket`.
- `smoke_summary.json` reports `cleaning_handles=25`, `ecr_receipts=6`, `reddit_sources=3`, `retail_sources=3`, and `cleaning_transform_entries=1`.
- Reddit live capture succeeded mechanically: 3 direct old-Reddit captures, 3 consolidations, 12 total comments.
- Retail live capture did not provide usable PDP product/offer/review substrate: all three retail sources are marked `capture_validity_supported=false`; Sephora and Ulta report `rendered_dom_error_or_block_page_marker` plus `required_retail_rows_all_null`; Amazon reports `rendered_dom_error_or_block_page_marker` plus `tiny_rendered_dom_with_error_marker`.
- The correct high-level interpretation is not "live capture-to-cleaning E2E is good to go." It is "the path stitches and preserves failure visibility; Reddit supplied usable substrate; retail did not."

## Review Questions

1. Does every Cleaning handle preserve enough raw/projection/ECR identity to trace from `cleaning_packet.json` back to the source packet, slice, file/hash anchor, projection row, and ECR receipt?
2. Does the stitcher or projection code ever treat unsupported retail captures as successful fragrance product evidence, or does it keep the unsupported status visible?
3. Are Reddit handles based on source-visible consolidated thread/comment substrate, and are any row-anchor downgrades reported rather than hidden?
4. Is the single transform ledger entry honest and mechanically scoped, or does it imply semantic Cleaning readiness?
5. Do the tests cover the failure modes that matter here: capture-validity findings, retail anchor verification/downgrade, ECR-ref packet-key coupling, Judgment-token exclusion, and raw-pull trigger validation?
6. Are the user-facing claims in docs/prompts/reviews or repo-map touched by this lane too strong for the observed run?
7. What is the smallest closure condition before claiming Cleaning live capture-to-cleaning E2E readiness?

## Output Contract

Write the durable report to:

`docs/review-outputs/cleaning_spine_live_e2e_adversarial_code_evidence_review_v0.md`

The report must be findings-first and include:

- `reviewed_by` and `authored_by` fields. Use operator-supplied values when available; otherwise use `unrecorded`, never fabricated.
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`; include `same_vendor_rationale` when relevant.
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- Findings ordered by severity: `critical`, `major`, `minor`. These are priority labels only, not approval or readiness authority.
- For each finding: target file/artifact, cited source evidence, impact, `minimum_closure_condition`, and `next_authorized_action`.
- Explicit non-findings for the retail failure visibility and Reddit capture questions if they hold.
- A final review-use boundary: findings are decision input only; this review is not approval, validation, readiness, mandatory remediation, or patch authority.

Do not write source patches. Do not emit `patch_queue_entry`. Advisory remediation direction is allowed, but executor-ready patch instructions require a separate patch/integration execution lane.

## Validation Evidence To Check

Observed before this prompt was written:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -B -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_retail_pdp_projection.py tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_cleaning_core.py tests\unit\test_ecr_identity_deriver.py tests\unit\test_ecr_inspectability_deriver.py tests\unit\test_ecr_timing_deriver.py tests\unit\test_ecr_source_visibility_deriver.py tests\unit\test_ecr_source_side_composition.py
```

Observed result: all selected tests passed.

Observed model validation after the live stitch:

```text
{'handles': 25, 'transform_ledger': 1, 'handles_with_ecr_ref': 25, 'cleaning_version': 'v0'}
```

The reviewer should rerun targeted checks only if needed to close a finding. Passing tests are evidence, not readiness.
