# Delegated Review-Patch Prompt -- Repo-Access Default / Adjudication Next-Step Fix v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (delegated review-and-patch commission -- review family)
scope: >
  Commissions one de-correlated adversarial review-and-patch pass on the Orca
  doctrine/prompt patch that restores repo access as the delegated-review default
  and binds clean review adjudication to deep-thought material next steps while
  treating admin as exactly one land step.
use_when:
  - Dispatching the adversarial review-and-patch pass requested on 2026-06-30 after the repo-access default patch is written.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/template-registry.md
  - docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md
  - docs/prompts/templates/review/delegated_review_return_adjudication_v0.md
  - docs/prompts/reviews/ontology_commission_refresh_delegated_review_patch_prompt_v0.md
  - docs/prompts/reviews/ontology_backbone_architecture_delegated_review_prompt_v0.md
  - docs/decisions/dcp_receipts_archive_v0.md
stale_if:
  - branch codex/delegated-review-repo-access-fix is rebased, amended, or superseded.
  - any named target file changes before controller dispatch.
```

## Orca Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: delegated-review-patch repo-mode prompt pack
  edit_permission: patch-only when all commission receipt fields are filled and de-correlation is satisfied; otherwise read-only blocked return
  target_scope: named doctrine/prompt/doc files only
  dirty_state_checked: yes
  blocked_if_missing:
    - de-correlation receipt
    - repo access to the pinned worktree; this commission uses repo mode unless explicitly recommissioned
    - output report destination write permission
    - SOURCE_CONTEXT_READY over the named files and owning overlay sources
```

- Output mode for this prompt artifact: `file-write` under `docs/prompts/reviews/`, with paste-ready-chat copy allowed for dispatch.
- Downstream controller output mode: `review-report` plus bounded working-tree diff when `access_mode: repo`; no_repo is allowed only if the operator explicitly records why repository access is unavailable or intentionally excluded.
- Template kind: delegated review-and-patch commission using the registered `adversarial-artifact-review` method posture; CA return adjudication uses `delegated-review-return-adjudication`.
- Branch/worktree: `codex/delegated-review-repo-access-fix` at `C:\Users\vmon7\Desktop\projects\orca\worktrees\delegated-review-repo-access-fix`.
- Base revision at prompt creation: `28ca1a50cd2f84c345b6328da013646f7b2a7b61`.
- Dirty-state allowance for controller: the named target files may already be modified by this patch and may be further modified by the delegated patch pass. Unrelated dirty/untracked files are out of scope and must be flagged, not touched.
- Report destination: `docs/review-outputs/adversarial-artifact-reviews/delegated_review_repo_access_default_patch_adversarial_review_v0.md`.
- Doctrine change decision: this prompt reviews a doctrine/prompt patch and carries the DCP receipt already added to `.agents/workflow-overlay/delegated-review-patch.md`.
- Isolation decision: use the existing worktree above; do not review a substitute checkout or pasted-only package when repo access exists.
- Validation gates: target-file scope check, stale-language search, `git diff --check`, report write verification, and final diff summary. Do not commit, stage, push, or open a PR.
- Thread operating target continuity: no visible active `thread_operating_target`; omitted for `no_visible_active_target`.

## Delegated Review-And-Patch Commission Receipt

This is a repo-mode commission. Before starting review or patch work, the operator or receiving lane must replace every `operator_to_fill` value below or return the nearest blocker.

```yaml
lane_binding:
  overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lane: artifact via workflow-adversarial-artifact-review after SOURCE_CONTEXT_READY
  mode: base-subagent
  target_kind: bounded_authored_artifact_patch_set
  access_mode: repo
  no_repo_rule: no_repo may be selected only by explicit operator override plus reason repository access is unavailable or intentionally excluded
  actor_model_family_receipt:
    author_home_model_family: OpenAI/GPT-family Codex lane authored the target patch; exact model/version operator_to_fill or unrecorded
    controller_model_family: operator_to_fill_must_differ_from_author_home_family_for_cross_vendor_discovery
    current_receiving_actor_role: controller
    dispatch_mode: repo-access external-controller-courier or runtime controller with repo access
    de_correlation_status: operator_to_fill(satisfied | blocked)
  de_correlation_bar: operator_to_fill(cross_vendor_discovery | same_vendor_sanity | self_fallback)
  no_model_recommendation: true
```

Hard block rules:

- If the controller cannot inspect the worktree directly, stop and ask the operator to either provide repo access or explicitly recommission as `no_repo`. Do not silently downgrade this prompt to no_repo.
- If the controller vendor/model lineage is not known to differ from the author family, do not claim the cross-vendor discovery bar. A same-family pass may return sanity findings only if the operator explicitly accepts that weaker bar.
- Do not patch outside the named target files. This commission prompt is dispatch machinery, not a patch target; flag defects in it separately.
- Do not edit protected, generated, frozen, canonical, or unrelated files unless they are named target files below.
- If the patch needs architecture or owner direction rather than bounded wording/source repair, return `NEEDS_ARCHITECTURE_PASS` and stop patching.

## Target Patch Scope

Patch only these files:

- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/template-registry.md`
- `docs/prompts/templates/portable/adversarial_artifact_review_portable_method_v0.md`
- `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`
- `docs/prompts/reviews/ontology_commission_refresh_delegated_review_patch_prompt_v0.md`
- `docs/prompts/reviews/ontology_backbone_architecture_delegated_review_prompt_v0.md`
- `docs/decisions/dcp_receipts_archive_v0.md`

Treat every other path as read-only / flag-only.

Fitness reference:

- `repo` is the assumed delegated review-and-patch access mode whenever the controller can inspect the repository/worktree.
- `no_repo` remains valid only as an explicit access constraint with a recorded reason; cross-vendor, external, couriered, paste-ready, or portable delivery does not imply repo-blindness.
- Review-return adjudication must adjudicate findings/diff/verdict/residuals first. If material issues remain, the next step is closure for those issues. If no material issue remains, admin is exactly one land step and the next 1-3 material moves receive deep thinking.
- This is a Smallest Complete Intervention patch. It is not a Mini God Tier claim, readiness claim, validation claim, or scope-expansion license.

## Required Controller Flow

1. Read `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/decision-routing.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, and `.agents/workflow-overlay/communication-style.md` before judging the patch.
2. SOURCE-LOAD every named target file and declare `SOURCE_CONTEXT_READY`, or return `SOURCE_CONTEXT_INCOMPLETE` with the exact missing source.
3. Run deep thinking before findings: identify the boundary problem, stale-assumption failure modes, adjudication-sequencing failure modes, and DCP/registry/template propagation risks.
4. Review adversarially for underfix, overreach, stale no_repo assumptions, contradictory package wording, missing repository-access propagation, bad adjudication next-step sequencing, DCP receipt inaccuracy, wrong registry/template classification, and ungrounded MGT/readiness/validation claims.
5. Patch only bounded wording/source issues inside the target files. Preserve Orca source hierarchy and avoid broader cleanup.
6. Run and report these checks:
   - `git status --short --branch`
   - stale-language search: `rg --hidden --glob '!worktrees/**' --glob '!.git/**' --glob '!docs/review-inputs/**' -n "no_repo[^\n]{0,80}(default|expected)|expected dispatch|repo-blind cross-vendor|cross-family / external / no-repo|repo-agnostic / cross-family|The reviewer needs nothing else -- no repo|The reviewer needs nothing else — no repo" .agents docs AGENTS.md`
   - positive-binding search: `rg -n "repo-mode by default|Access selection rule|selection_rule|delegated-review-return-adjudication|admin is exactly one|post_return_adjudication|explicit no_repo" .agents docs/prompts/templates docs/prompts/reviews`
   - `git diff --check`

## Output Contract

Write the durable report to `docs/review-outputs/adversarial-artifact-reviews/delegated_review_repo_access_default_patch_adversarial_review_v0.md` and return a chat summary with:

```yaml
review_summary:
  status: completed | blocked | needs_architecture_pass
  reviewed_by: operator_to_fill_or_unrecorded
  authored_by: OpenAI/GPT-family Codex lane, exact model/version operator_to_fill_or_unrecorded
  access_mode: repo
  de_correlation_status: satisfied | blocked | weaker_same_vendor_sanity
  findings_count: 0
  blocking_findings: []
  patch_files_touched: []
  checks_run: []
  residual_risks: []
  next_authorized_action: Chief Architect adjudicates the returned findings/diff/verdict as claims using delegated-review-return-adjudication.
```

Findings are findings-first. Use `critical`, `major`, and `minor` only as finding-priority labels. For each actionable finding include `minimum_closure_condition` and `next_authorized_action`. Do not claim PASS, validation, readiness, approval, mergeability, or no-new-seam unless the commission and evidence explicitly support that claim.