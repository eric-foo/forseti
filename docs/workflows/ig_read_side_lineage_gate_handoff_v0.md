# IG Read-Side Lineage Gate Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet
scope: Cold-reader continuation packet for the IG read-side source-backed lineage gate after PR #467.
use_when:
  - Continuing the IG/YT behavioral-sync lane after the read-side lineage gate PR.
  - Verifying why IG product-mention extraction must be source-backed by Silver lineage before behavior can be complete.
  - Planning the next cross-source product-mention consumer sweep.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md
  - orca-harness/data_lake/silver_lineage.py
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/source_capture/ig_reels_behavioral_projection.py
  - orca-harness/tests/unit/test_ig_reels_behavioral_lake.py
  - orca-harness/tests/unit/test_silver_lineage.py
stale_if:
  - PR #467 is merged, closed, or superseded.
  - Any named IG behavioral lake/projection or Silver lineage files materially change.
  - A later handoff or validation receipt supersedes this packet.
```

## Load Contract

- packet_version: workflow-handoff max v0
- mode: max
- created_at: 2026-06-29T23:10:07.9231967+08:00
- created_by_lane: Codex worktree `codex/ig-read-side-lineage-gate`; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-read-side-lineage-gate`
- handoff_path: `docs/workflows/ig_read_side_lineage_gate_handoff_v0.md`
- expected_branch: `codex/ig-read-side-lineage-gate`
- expected_head: `98be1c50d77c26ea419e238317ef25b3fd385983` at PR #467 creation; verify current state before acting
- expected_dirty_state_including_handoff_file: code branch clean at `98be1c50`; this handoff file may be untracked locally because it was written after PR creation to avoid moving the review branch
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: Make Instagram Reels behaviorally complete to the same standard as the fully built YouTube lane, without requiring identical capture mechanics.
- anchor_goal: Ensure IG behavioral projections only treat product-mention extraction as complete evidence when the consumed Silver product-mention record is source-backed complete by lineage.
- success_signal: A persisted IG product-mention record with complete record-set markers but missing, invalid, or limitations-only lineage is residualized and cannot produce a complete IG behavioral claim; lineage-bearing records from the canonical F lake still project successfully.

## Open Decision / Fork

- decision: What follows PR #467 after it lands.
  - options: merge PR #467 then run a cross-source consumer sweep; or patch PR #467 first if CI/review finds issues.
  - already constrained / off the table: no shared IG/YT capture core, no media capture, no historical lake rewrite, no shared-driver required-argument break.
  - trade-offs: a generic read helper plus one IG consumer is narrow and testable; a broad all-Silver migration before this PR lands would blur failure boundaries.
  - owner of the call: owner for merge/sequence; agent may patch CI or review findings on PR #467.
  - recommendation and why: land/fix PR #467 first, then sweep other `silver__cleaning__product_mentions` consumers.

## Drift Guard

- behavioral completeness parity means same evidence discipline, not identical IG/YT capture mechanics.
- source-backed completeness is a read-side eligibility claim, not merely record-set membership.
- old product records without lineage must not be silently grandfathered as complete evidence.
- do not add live capture, media preservation, shared core, or scheduler work in this lane unless explicitly redirected.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder: PR #467 metadata, `orca-harness/source_capture/ig_reels_behavioral_lake.py`, `orca-harness/data_lake/silver_lineage.py`, and `docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md`
- already loaded (weak orientation, freshness-marked; not authority): project instructions supplied in-thread; overlay README/source-loading/decision-routing; workflow-handoff skill; Silver lineage helper; IG lake/projection/tests; canonical F receipt
- must load first: project instructions, overlay README, source-loading/decision-routing for planning or patching, then the exact target files above
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder

### Earlier-decided concepts and behaviors

- PR #460 made IG product-mention records lineage-bearing, which unblocked this read-side gate.
  - decided in: PR #460 and `docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md`
  - compare target: PR #460 merge commit `aa0f01b5d42d2201c3c0559dc65ef8adceb16acc`
  - verify before: claiming IG lineage write-adoption exists on current main
- `complete_with_residuals` is the correct overall IG status when extraction is complete but grid/source residuals remain.
  - decided in: `orca-harness/source_capture/ig_reels_behavioral_projection.py`
  - compare target: `_behavioral_status` downgrades complete plus residuals
  - verify before: claiming behavioral-complete semantics

## Active Objective

PR #467 implements the read-side lineage eligibility gate for IG behavioral projection. A cold reader should verify PR/CI state, then either patch PR #467 if needed or proceed to the post-gate cross-source consumer sweep after merge.

## Exact Next Authorized Action

1. Verify PR #467 with `gh pr view 467 --json state,headRefOid,mergeable,isDraft,url` and `gh pr checks 467`.
2. If checks/review fail, patch only the read-side gate lane files and rerun validation.
3. If PR #467 is merged, continue with the cross-source sweep for other consumers of `silver__cleaning__product_mentions`; do not alter capture mechanics or media preservation in that sweep.

## Authority And Source Ledger

- `AGENTS.md` / supplied project instructions
  - Role: repository behavior kernel
  - Load-bearing: yes
  - Compare target: reread current project instructions if available
  - Last checked: 2026-06-29
  - Reuse rule: strict claims require reread or supplied current text
- `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/decision-routing.md`
  - Role: Orca overlay/source-loading/routing authority
  - Load-bearing: yes
  - Compare target: current workspace files
  - Last checked: 2026-06-29
  - Reuse rule: reread before new planning, prompt, or repo-changing work
- `orca-harness/data_lake/silver_lineage.py`
  - Role: generic Silver lineage grammar and new read-side status helper
  - Load-bearing: yes
  - Compare target: PR #467 head `98be1c50d77c26ea419e238317ef25b3fd385983`
  - Last checked: 2026-06-29
  - Reuse rule: reread before changing lineage status semantics
- `orca-harness/source_capture/ig_reels_behavioral_lake.py`
  - Role: IG read model consuming product-mention records
  - Load-bearing: yes
  - Compare target: PR #467 head `98be1c50d77c26ea419e238317ef25b3fd385983`
  - Last checked: 2026-06-29
  - Reuse rule: reread before claiming the gate's consumer behavior
- `docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md`
  - Role: bounded canonical F-lake receipt proving IG lineage-bearing product records exist
  - Load-bearing: yes
  - Compare target: file at PR #460 merge state; reread-required if changed
  - Last checked: 2026-06-29
  - Reuse rule: orientation until fresh-read or rerun for strict validation claims

## Current Task State

- Completed: PR #460 confirmed merged; new branch `codex/ig-read-side-lineage-gate` created from current main; PR #467 opened.
- Completed: `silver_record_source_backed_status()` added to reconstruct persisted top-level Silver lineage fields and classify `source_backed_complete`, `source_lineage_missing`, `source_lineage_incomplete`, or `source_lineage_invalid`.
- Completed: IG behavioral lake adapter downgrades a complete product-mention record-set to the lineage problem status when the record is not source-backed complete.
- Completed: IG projection surfaces lineage problem statuses and `source_backed_status` in extraction source statuses.
- Broken or uncertain: GitHub CI for PR #467 was pending at last check, not passed.

## Workspace State

- Branch: `codex/ig-read-side-lineage-gate`
- Head: `98be1c50d77c26ea419e238317ef25b3fd385983`
- Dirty or untracked state before handoff: clean after PR creation
- Dirty or untracked state after writing the handoff file: expected untracked `docs/workflows/ig_read_side_lineage_gate_handoff_v0.md`
- Target files or artifacts: PR #467 plus this handoff file
- Related worktrees or branches: prior merged PR #460 branch `codex/ig-deep-capture-review-closures-main`

## Changed / Inspected / Tested Files

- `orca-harness/data_lake/silver_lineage.py`
  - Status: changed in PR #467
  - Role: generic read-side status helper over persisted lineage fields
- `orca-harness/source_capture/ig_reels_behavioral_lake.py`
  - Status: changed in PR #467
  - Role: IG read-side gate application
- `orca-harness/source_capture/ig_reels_behavioral_projection.py`
  - Status: changed in PR #467
  - Role: status vocabulary and surfaced source-backed status
- `orca-harness/tests/unit/test_ig_reels_behavioral_lake.py`
  - Status: changed in PR #467
  - Role: valid-lineage and missing-lineage consumer coverage
- `orca-harness/tests/unit/test_silver_lineage.py`
  - Status: changed in PR #467
  - Role: generic persisted-field status coverage

## Frozen Decisions

- Gate source-backed completeness at the read-model consumer, not by adding a required shared-driver argument.
- Treat complete record-set membership as insufficient for behavior-complete evidence when lineage is missing, invalid, or limitations-only.
- Preserve IG/YT behavioral parity by evidence semantics, not identical capture mechanics.

## Mutable Questions

- Which non-IG consumers of `silver__cleaning__product_mentions` should adopt the same helper next?
- Should old no-lineage product records be backfilled/re-extracted or left as explicit residuals until naturally regenerated?

## Superseded / Dangerous-To-Reuse Context

- Superseded: the pre-PR #460 idea of building a read-side gate first. It was premature because the existing IG consumer did not yet read lineage-bearing product records.
- Dangerous: treating `is_record_set_complete` as source-backed completeness. It proves member presence only.

## Commands And Verification Evidence

- Command: `python -m pytest -q orca-harness/tests/unit/test_silver_lineage.py orca-harness/tests/unit/test_ig_reels_behavioral_lake.py orca-harness/tests/unit/test_ig_reels_behavioral_projection.py orca-harness/tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py`
  - Result: passed, `............................................... [100%]`
  - Re-run target: same command
- Command: wide IG/transcript pytest slice ending with `test_no_llm_imports.py`
  - Result: passed, progress reached `[100%]`
  - Re-run target: command from PR #467 body
- Command: canonical F-lake read through `DataLakeRoot.resolve(explicit='F:\orca-data-lake')`
  - Result: `DEntAFPpiCv` complete with `source_backed_complete`; `DZ69knlsDb1` and `DaA8n7EhqTR` retained existing residuals while complete product records read as `source_backed_complete`
  - Re-run target: rerun the inline Python projection read against F lake after loading PR branch
- Command: `gh pr view 467 --json number,state,isDraft,baseRefName,headRefName,headRefOid,title,url,mergeable`
  - Result: PR #467 open, not draft, mergeable, head `98be1c50d77c26ea419e238317ef25b3fd385983`
  - Re-run target: same command
- Command: `gh pr checks 467`
  - Result: `orca-harness-tests pending` at last observation
  - Re-run target: same command

## Blockers And Risks

- Blocker or risk: PR #467 CI was pending at last check.
  - Evidence: `gh pr checks 467` returned pending for `orca-harness-tests`.
  - Likely next action: wait/check; patch only if CI fails.
- Blocker or risk: historical complete product records without lineage will now residualize if consumed.
  - Evidence: gate intentionally returns `source_lineage_missing` for records without top-level `lineage_schema_version`.
  - Likely next action: leave as visible residuals unless owner authorizes backfill/re-extraction.

## Confirm-Don't-Trust Load Checklist

- Re-verify branch/head/PR #467 state.
- Reread `silver_lineage.py`, `ig_reels_behavioral_lake.py`, and `ig_reels_behavioral_projection.py` before patching.
- Rerun focused tests after any code change.
- Treat F-lake validation as observed evidence only after rerunning against the current branch.
- If PR #467 has merged or changed head, classify packet as `STALE_REREAD_REQUIRED` and re-derive current state.

## Do Not Forget

This lane is about behavioral completeness gates. It is not shared-core capture, live media preservation, scheduler readiness, or a historical lake rewrite.