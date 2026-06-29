# Engagement Resonance Scanning Capture CSB Judgment Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-bound, operator-couriered adversarial review-and-patch prompt for the
  engagement-resonance propagation patch across Scanning, Capture, CSB, and
  Judgment surfaces.
use_when:
  - Commissioning a different-vendor reviewer to inspect and harden the 13-doc engagement-resonance propagation diff.
  - Checking that the propagation preserves public-reaction engagement as qualitative routing/resonance context without proof, score, source-access, readiness, or validation drift.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - orca/product/shared/engagement_registry/engagement_logic_registry_v0.md
```

## Operator Paste Instruction

Paste this prompt into an independent receiving lane whose controller is a different vendor / model lineage from the author/home family recorded below. This is a who-constraint, not a model recommendation.

If the receiving actor is not a de-correlated controller, or cannot access the worktree named below, return the nearest blocker instead of reviewing a summary.

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: patch-only for the 13 named target files if operator confirms repo-mode patch authority; otherwise read-only/advisory
  target_scope: engagement-resonance propagation patch across Scanning, Capture, CSB, and Judgment documentation surfaces
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-of-truth, source-loading, prompt-orchestration, review-lanes, delegated-review-patch overlay, engagement registry, target files, direct worktree access
```

## Commission

### Lane Binding

```yaml
delegated_review_patch:
  overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lane: adversarial artifact review via workflow-adversarial-artifact-review after source readiness
  mode: base-subagent / operator-couriered controller
  access: repo preferred; no_repo advisory fallback only if repo access is impossible
  actor_model_family_receipt:
    author_home_model_family: OpenAI / GPT-family (Codex GPT-5 current session)
    controller_model_family: operator_to_fill; must be different vendor / model lineage from OpenAI / GPT-family for cross-vendor discovery
    current_receiving_actor_role: controller, if and only if this prompt is pasted into the different-family receiving lane
    dispatch_mode: external-controller-courier
    de_correlation_status: satisfied only after the receiving actor records a different vendor / model lineage; otherwise blocked
  de_correlation_bar: cross_vendor_discovery when satisfied; same_vendor_sanity or self_fallback must not claim no-new-seam
```

No `Recommended model` block exists. Do not add one.

### Objective

Review and harden the current working-tree patch that propagates the engagement-resonance boundary into scanning, capture, Commission Signal Board, and Judgment surfaces.

The intended outcome is a smallest-complete docs patch that makes future agents preserve source-visible public-reaction engagement facts as qualitative routing/resonance context while preventing drift into demand proof, buyer proof, credibility, independence, source quality, source-access permission, Capture route binding, graph weight, final resonance weight, Action Ceiling, readiness, validation, scoring, or runtime infrastructure.

### Why Read-Only Review Is Insufficient

The patch changes several durable downstream surfaces that future agents will follow. A source-read-only critique may identify wording drift, but the useful hardening pass is to patch bounded wording defects directly when the fix is local, mechanical, and source-supported, then return a diff for home/CA adjudication. If the correct fix needs a broader doctrine redesign, return `NEEDS_ARCHITECTURE_PASS` instead of patching around it.

### Target Workspace

```yaml
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\search-surface-mgt-p0-captures
branch: codex/search-surface-mgt-p0-captures-ws
head_before_review_prompt: 394a9ec65f53bd39e643904b2ba9824d9a69746d
expected_dirty_state:
  modified_target_files: 13
  prompt_artifact_may_be_untracked_or_modified: docs/prompts/reviews/engagement_resonance_scanning_capture_csb_judgment_adversarial_review_patch_prompt_v0.md
  unrelated_untracked: docs/prompts/hygiene-queue/
review_target: the 13 named modified target files below and their diff from HEAD
commit_push_pr_authority: none
```

If the worktree path, branch, HEAD, or dirty-state allowance does not match, stop and return the nearest blocker. Do not review a pasted summary, alternate checkout, recreated source, or context pack as a substitute for the pinned worktree.

## Target Files And Bounded Patch Scope

Patch authority, if repo-mode is operator-confirmed, is limited to wording inside these files only. Everything else is read-only / flag-only.

- `[capture-runbook]` `orca-harness/docs/source_capture_agent_runbook.md` - source-visible engagement facts and must-not-overclaim boundaries only.
- `[capture-toolbox-index]` `orca/product/spines/capture/core/source_capture_toolbox/README.md` - playbook index row only.
- `[capture-playbook]` `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` - Recency / Current-State Preservation Priority section only.
- `[instagram-policy]` `orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md` - momentum/allocation boundary only.
- `[csb-readme]` `orca/product/spines/commission_signal_board/README.md` - boundaries paragraph only.
- `[judgment-first-read]` `orca/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md` - C3 Verdict / Action step only.
- `[scanning-readme]` `orca/product/spines/scanning/README.md` - Public-Reaction Engagement Boundary only.
- `[scan-core]` `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` - No Weak Reads By Accident bullet only.
- `[mgt-walk]` `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` - public-reaction engagement boundary only.
- `[aeo-search]` `orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md` - Decision B visibility/interest gate boundary only.
- `[linkedin-discovery]` `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md` - trajectory / candidate schema engagement-count boundary only.
- `[linkedin-watch]` `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md` - watch-ordering / visible-counts boundary only.
- `[linkedin-index]` `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md` - bounded-watch index pointer only.

Do not edit code, hooks, schemas, checkers, source-access rules, claim-ladder rules, scoring logic, runtime behavior, CI, or any file outside the listed target files. If you find an off-scope defect, flag it for CA adjudication.

## Required Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read these overlay authorities: `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/validation-gates.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/safety-rules.md`.
3. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-adversarial-artifact-review`. Do not APPLY either yet.
4. SOURCE-LOAD `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md` and the 13 target files from the worktree.
5. Inspect `git diff -- <13 target files>` directly.
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and conflicts.
7. Only after source readiness, APPLY `workflow-deep-thinking`, then APPLY `workflow-adversarial-artifact-review` to the loaded target diff.
8. Patch only local wording defects inside the bounded target scopes when repo-mode patch authority is confirmed. If patch authority is absent, return findings plus exact patch suggestions instead.

If `workflow-adversarial-artifact-review` is unavailable in the receiving lane, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Review Axes To Attack

- Does any added wording turn engagement/resonance into proof, buyer proof, demand proof, credibility, independence, source quality, Commit/Scale support, graph weight, final resonance weight, Action Ceiling, readiness, validation, source-access permission, Capture route binding, or a score?
- Does any Capture wording ask Capture to interpret meaning instead of preserving route-visible facts and urgency context?
- Does any Scanning wording bind Capture, clear a floor/gate, score a candidate, or make adapter counts authoritative beyond watch/routing priority?
- Does CSB stay separate from proof, Commit/Scale support, classifier mapping, final resonance weight, graph weight, and Action Ceiling?
- Does Judgment remain the only layer that interprets engagement's effect on Signal Integrity, Signal Use, Decision Strength, Action Ceiling, or claim-tier promotion?
- Are low/missing engagement cases preserved as non-disqualifying where the controlling source requires that?
- Does the patch avoid new schema/runtime/hook/checker behavior and stay docs-only?
- Are DCP hygiene findings material to keep/acceptance of this patch, or can they be carried as separate receipt-maintenance debt?

## Validation Evidence Already Observed By Home Lane

These are claims to verify or challenge, not premises to inherit:

- `git diff --check`: exit 0; Git emitted line-ending warnings for three markdown files.
- `python .agents/hooks/check_dcp_receipt_hygiene.py --selftest`: SELFTEST OK.
- `python .agents/hooks/check_registry_list_sync.py --selftest`: SELFTEST OK.
- `python .agents/hooks/check_engagement_stale_phrases.py --selftest`: SELFTEST OK.
- `python .agents/hooks/check_csb_scanning_artifact.py --selftest`: SELFTEST OK.
- `python .agents/hooks/check_review_output_provenance.py --selftest`: SELFTEST OK.
- `python .agents/hooks/check_commission_signal_board_output.py --selftest`: SELFTEST OK.
- `python .agents/hooks/check_engagement_stale_phrases.py --strict <13 target files>`: `engagement-stale-phrases: OK (12 file(s) checked, 1 skipped)`.
- `python .agents/hooks/check_dcp_receipt_hygiene.py --changed`: exit 0 advisory findings in `[capture-toolbox-index]`, `[capture-playbook]`, and `[linkedin-discovery]` for inline receipt backlog / missing archive pointers.

## Controller Output Contract

Return findings first. If you patch, leave changes in the working tree and do not commit.

Required output:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/engagement_resonance_scanning_capture_csb_judgment_adversarial_review_patch_report_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI GPT-5 / Codex current session
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  same_vendor_rationale: required only if de_correlation_bar is same_vendor_sanity
  summary: one sentence
  findings_count: integer
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: one concrete next step
```

Then include:

- `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE` declaration.
- Actor/model-family receipt and de-correlation status.
- Findings with severity `critical`, `major`, or `minor`, each carrying the target label, file path, line reference, source citation, minimum closure condition, and next authorized action.
- Unified diff for any patch applied, with target labels searchable in nearby hunk context.
- Per-change source citations, neutral in tone and decision-sufficient in substance.
- Verdict and residual-risk note.
- DCP hygiene disposition: accepted as separate debt, patched within scope, or blocks keep/acceptance.

The delegate's diff, citations, and verdict are claims to adjudicate, not premises to inherit. The home/CA model decides what is kept and may reject any change.

## Escalation And Hard Stops

Return `NEEDS_ARCHITECTURE_PASS` and stop patching if the patch needs a broader redesign of engagement doctrine, source-access authority, claim-tier semantics, scoring behavior, CSB schema, scan schema, Capture routing, or Judgment gates.

Return `BLOCKED_REVIEW_LANE_UNAVAILABLE` if the required review skill is unavailable.

Return `BLOCKED_CONTROLLER_NOT_DECORRELATED` if the controller is not a different vendor / model lineage from OpenAI / GPT-family and the operator asks for cross-vendor discovery.

Return `BLOCKED_WORKTREE_MISMATCH` if the worktree, branch, HEAD, or dirty-state allowance is not as specified.

## Review-Use Boundary

This review output is decision input only. It is not approval, validation, readiness, mandatory remediation, proof, source-of-truth promotion, merge permission, commit permission, push permission, or auto-keep authority. The home/CA adjudicates every proposed change before keep.