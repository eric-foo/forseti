# Scanning / CSB / Capture / Judgment Recency Attention Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial artifact review prompt for the PR #354 recency/currentness
  propagation changes across Scanning, Commission Signal Board, Capture, and
  Judgment.
use_when:
  - Commissioning a bounded adversarial review of commit 13a1becb on PR #354.
  - Checking whether recency/currentness was propagated as attention/preservation/read relevance without proof, scoring, classifier, graph-weight, or Capture-route leakage.
  - Verifying the CSB broad-scout/recency default remains coherent with downstream lane boundaries.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
branch_or_commit: codex/scanning-broad-scout-recency-default @ 13a1becb3841a2596430dc345674c86fa697e098
stale_if:
  - PR #354 is rebased or amended after commit 13a1becb.
  - Any target file below changes after this prompt is authored.
  - The review-lanes or prompt-orchestration overlay changes before execution.
```

## Prompt Contract

preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom review S3
  edit_permission: read-only review; write only the bound review report path
  target_scope: adversarial artifact review prompt for PR #354 recency/currentness propagation
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/review/adversarial_artifact_review_v0.md
    - target branch or commit 13a1becb3841a2596430dc345674c86fa697e098
```

Output mode: `review-report`.

Template kind: `adversarial-artifact-review`, bound by `.agents/workflow-overlay/template-registry.md` to `docs/prompts/templates/review/adversarial_artifact_review_v0.md`.

Review report destination:
`docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`

Edit permission: read-only for all source files. The reviewer may write exactly the review report above. Do not patch, stage, commit, push, open or update PRs, move files, rename files, or produce a patch queue.

Workspace and revision preflight:
- Expected workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default`.
- Expected branch: `codex/scanning-broad-scout-recency-default`.
- Expected commit: `13a1becb3841a2596430dc345674c86fa697e098`.
- Dirty-state allowance: clean or report-only dirty state. If target files are modified beyond commit `13a1becb`, return `blocked` unless the prompt runner explicitly says those modifications are in scope.
- If you do not have repo/filesystem access, stop and request a pasted source capsule. Do not review a substitute checkout or memory summary.

Thread operating target continuity:
```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable
```

Doctrine change decision: The reviewed artifact set is doctrine-bearing product/workflow review surface. The reviewer must inspect whether each changed file's `direction_change_propagation` receipt is internally honest and sufficient for the claimed propagation. The reviewer must not author new doctrine or decide acceptance.

Cynefin routing: This is a repo-aware adversarial review prompt and matches `.agents/workflow-overlay/decision-routing.md` trigger conditions. Before review findings, run the router and keep it compact. Allowed next move is read-only adversarial review plus report write. Disallowed next move is patching or widening into a full scanning-spine redesign.

## Review Objective

Perform a read-only adversarial artifact review of the PR #354 recency/currentness propagation changes at commit `13a1becb3841a2596430dc345674c86fa697e098`.

The intended decision for the Chief Architect is whether the propagation is safe to keep as CA input, needs a small patch before acceptance, or should be rejected/held because it leaks recency/currentness into proof, scoring, classifier mapping, graph weight, Capture route binding, access authorization, or Judgment claim-tier promotion.

Fitness reference:
- Goal: make recency/currentness increase attention and preservation priority across Scanning/CSB, Capture, and Judgment, without treating it as demand proof or downstream authority.
- Observable success signal: a fresh reader can start from Scanning/CSB, understand that newer/current URL-backed signals deserve more attention than same-strength older context, and see the exact downstream limits: CSB metadata only, Capture preservation urgency only, Judgment qualitative read attention only.
- Axis to attack: whether this is the right goal/signal and whether the patch actually achieves it without creating a hidden proof/scoring/route-binding shortcut.

## Required Method Sequence

1. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
2. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not APPLY it yet.
3. SOURCE-LOAD the required sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and conflicts.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame boundary risks and failure modes.
6. Then APPLY `workflow-adversarial-artifact-review` to produce findings.
7. If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after source readiness, return blocked or advisory-only. Do not emit strict review verdicts, severity authority, readiness claims, validation claims, mandatory remediation, patch queues, or executor-ready handoffs.

## Required Sources

Authority and review mechanics:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/communication-style.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

Target commit and changed files:
- Git commit `13a1becb3841a2596430dc345674c86fa697e098`
- `docs/workflows/orca_repo_map_v0.md`
- `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md`
- `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`

Adjacent sources to inspect only as needed for split-brain or stale-route claims:
- `orca/product/spines/scanning/README.md`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `.agents/hooks/check_commission_signal_board_output.py`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`
- `orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md`

Sources excluded by default:
- all review outputs not named by this prompt;
- all research corpus and source captures;
- all implementation/runtime code except the CSB validator script named above;
- all historical branch summaries unless needed to resolve an explicit contradiction.

## Review Questions

Attack these questions first:

1. Does the change keep recency/currentness as attention, preservation urgency, or qualitative read relevance only?
2. Does any wording imply recency/currentness is buyer proof, demand proof, gate clearance, classifier mapping, graph weight, numeric/ordinal weight, scoring shortcut, claim-tier evidence, Capture route selection, or access authorization?
3. Did the patch update the correct controlling sources and avoid duplicating doctrine into low-authority pointer/index surfaces where it would split later?
4. Are the `direction_change_propagation` receipts honest about controlling sources updated, downstream surfaces checked, intentionally-not-updated surfaces, stale-language search, and non-claims?
5. Does the CSB prompt schema change stay compatible with the CSB validator and board handoff expectations, or did optional metadata create a hidden required-column mismatch?
6. Does the Capture playbook wording preserve Capture's route choice and Step 0 access-control gate?
7. Does the Judgment demand-read wording preserve the no-scoring invariant and avoid evidence-ladder or gate-ownership drift?
8. Does the repo map update faithfully point future readers to the controlling source without overstating validation, readiness, or authority?
9. Did adding the CSB authority-packet amendment create a second source of truth, or is it a narrow pointer-level correction consistent with the durable prompt?
10. Is there any stale language in adjacent scanning/CSB/Capture/Judgment surfaces that would route future work by the old or wrong semantics?

## Severity Guidance

Use `critical`, `major`, and `minor` as finding-priority labels only.

Critical examples:
- A changed source makes recency/currentness proof, scoring, route binding, claim-tier evidence, or access authorization.
- The prompt/report claims validation/readiness/acceptance without authority.

Major examples:
- A controlling surface remains stale enough that future CSB, Capture, or Judgment runs could follow the wrong semantics.
- DCP receipts omit a material controlling source or falsely claim a check that was not supported by source evidence.
- CSB schema wording breaks or ambiguously changes mechanical handoff expectations.

Minor examples:
- Frictional wording that is unlikely to change behavior but should be tightened.
- Optional hardening that would reduce future review cost but is not required for safe acceptance.

Do not emit `patch_queue_entry`. Recommended corrections should be advisory remediation directions only.

For each finding include:
- severity;
- location with file:line citation;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- recommended correction or advisory remediation direction.

## Optional Validation / Search Checks

If available and cheap, rerun or inspect the same class of checks. Treat them as review evidence, not validation/readiness proof:

```powershell
git rev-parse HEAD
git diff 8e79d18d..13a1becb --stat
git diff 8e79d18d..13a1becb --check
python .agents/hooks/check_retrieval_header.py --changed
python .agents/hooks/check_repo_map_freshness.py --changed
python .agents/hooks/check_map_links.py --strict
python -B .agents/hooks/check_commission_signal_board_output.py --selftest
```

Also run a targeted stale/leakage search over the controlling sources if possible:

```powershell
rg -n -i "recency.*proof|recent.*proof|currentness.*proof|recency.*gate|recent.*gate|currentness.*gate|recency.*route binding|currentness.*route binding|recency.*scoring|currentness.*scoring|recency.*numeric|currentness.*numeric|recency.*graph weight|currentness.*graph weight|recency.*classifier mapping|currentness.*classifier mapping|same-strength.*proof|same-strength.*gate|same-strength.*scoring" orca/product/spines/commission_signal_board orca/product/spines/scanning orca/product/spines/capture/core/source_capture_toolbox orca/product/spines/capture/core/contracts orca/product/spines/capture/core/demand_durability_indicators orca/product/spines/judgment docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
```

If a command is unavailable, too noisy, or blocked, record `not_run` with why. Do not invent a pass.

## Required Report Shape

Write the durable report to:
`docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md`

The report must include:
- retrieval header;
- `reviewed_by` and `authored_by` fields near the top; use the real reviewer model/version if available, otherwise `unrecorded`; use `codex-gpt-5` for `authored_by` only if accepted as dispatcher-supplied provenance, otherwise `unrecorded`;
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded`;
- `same_vendor_rationale` when `de_correlation_bar: same_vendor_sanity`;
- source context status: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- exact commit/branch reviewed;
- sources read and sources intentionally not read;
- findings first, ordered by severity;
- residual risks/test gaps;
- review-use boundary.

After writing the report, return this exact compact YAML shape in chat, followed by a short findings summary:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: codex-gpt-5
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

If the required durable report cannot be written, use `status: failed`, replace `report_path` with `review_location: chat_only_current_thread`, set `recommendation: blocked`, and explain the write failure in `summary` or `next_action` without adding extra YAML keys.

## Review-Use Boundary

This is a read-only adversarial artifact review. Findings and non-findings are Chief Architect decision input only. They are not approval, validation, readiness, mandatory remediation, source-of-truth promotion, product proof, implementation authorization, or executor-ready patch authority unless a separate authorized Orca decision or execution lane accepts them.
