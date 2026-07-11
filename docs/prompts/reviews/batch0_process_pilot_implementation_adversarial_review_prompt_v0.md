# Batch 0 Process Pilot Implementation Adversarial Review Prompt v0

Output mode: review-report

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: De-correlated post-implementation review-and-patch commission for the Batch 0 process pilot diff.
use_when:
  - Running the fused post-implementation adversarial review handoff for codex/batch0-process-pilot.
authority_boundary: retrieval_only
stale_if:
  - The target branch changes after the reviewer records its observed HEAD.
  - The Batch 0 receipt schema, threshold, or notification target changes outside this commission.
```

## Prompt preflight

- `output_mode`: `review-report`
- `template_kind`: `adversarial-artifact-review`, with the code portions also reviewed through `workflow-code-review`
- `template_source`: `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- `prompt_source`: `docs/prompts/reviews/batch0_process_pilot_implementation_adversarial_review_prompt_v0.md`
- `report_destination`: `docs/review-outputs/adversarial-artifact-reviews/batch0_process_pilot_implementation_adversarial_review_v0.md`
- `authorization_basis`: fused post-implementation recommended-review handoff authorized by the owner-requested Batch 0 implementation turn
- `workspace_path`: `C:\Users\vmon7\Desktop\projects\orca\worktrees\codex-batch0-process`
- `branch`: `codex/batch0-process-pilot`
- `base_revision`: `origin/main@ed1966a1`
- `head_revision`: reviewer records the observed PR head before review; block if the branch is not the expected branch
- `isolation_decision`: dedicated worktree off freshly fetched `origin/main`
- `dirty_state_allowance`: begin from the committed PR head; controller-created bounded target edits may be dirty after review starts; unrelated dirt is blocked
- `edit_permission`: `patch-only`, limited to the named target set below; do not commit, push, merge, or open another PR
- `review_default`: findings-first; no runtime-model recommendation or ranking
- `doctrine_change_decision`: the target changes temporary workflow, review, output, and notification boundaries; verify the included propagation receipt rather than inventing a second one
- `preflight_defaults_note`: the shared defaults file currently names a different workspace path, so this prompt binds the observed worktree explicitly instead of inheriting that path
- `thread_operating_target_continuity`: no visible durable thread target was supplied; none carried

## Objective and success signal

Adversarially test whether the Batch 0 diff actually starts all four probes,
fails closed on malformed or duplicated review receipts, counts exactly one
completion per CA-adjudicated material review, and notifies the repository owner
once at the tenth valid receipt without creating a new review authority or a
fake success path.

Success means the reviewer can either return a bounded corrected diff with
evidence for every change, or identify a precise blocker/design issue. A clean
review is decision input only; it is not validation, readiness, acceptance, or
proof that Batch 0 improves outcomes.

## Cynefin route

Before applying review methods, classify this as a mixed code/workflow-contract
review. The current bottleneck is false-success behavior at the receipt counter,
CI enforcement, issue deduplication, and temporary-doctrine retirement seam.
Allowed next move: inspect and patch only the named target set. Disallowed next
move: widen into general review-process redesign, worktree cleanup, Batch 1, or
unrelated repository hygiene.

## De-correlation and lane receipt

- `mode`: `base-subagent`
- `access`: `repo`
- `author_home_model_family`: `OpenAI`
- `controller_model_family`: `operator_to_fill`; it must be a different upstream vendor/model lineage from OpenAI
- `current_receiving_actor_role`: `controller`
- `dispatch_mode`: `external-controller-courier`
- `de_correlation_status`: the controller records `satisfied` before review; unknown or same-vendor lineage blocks the cross-vendor discovery claim
- This is a who-constraint, not a runtime-model recommendation.
- The controller must not launch a replacement controller or unrelated subagent.

## Source-gated method contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD, but do not yet APPLY:
   - `workflow-deep-thinking`;
   - `workflow-code-review` for Python and GitHub Actions behavior;
   - `workflow-adversarial-artifact-review` for overlay and workflow records.
3. SOURCE-LOAD the bounded source pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, naming any missing or conflicting source.
5. Only after readiness, APPLY deep-thinking, then the code and artifact review methods to their respective claims.
6. Verify every finding and patch against the loaded source and observed diff.

## Bounded source pack

Required authority:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/batch0-process-pilot.md`

Targets and patch bounds:

- `[overlay-index]` `.agents/workflow-overlay/README.md` — Batch 0 pointer only
- `[review-binding]` `.agents/workflow-overlay/review-lanes.md` — temporary Batch 0 receipt obligation only
- `[pilot-owner]` `.agents/workflow-overlay/batch0-process-pilot.md` — temporary pilot contract and propagation receipt
- `[tracker]` `.github/scripts/batch0_process_tracker.py` — schema validation, uniqueness, threshold, output, and self-test behavior
- `[notifier]` `.github/workflows/batch0-owner-notify.yml` — validation and one-time owner issue behavior
- `[ci]` `.github/workflows/ci.yml` — the two Batch 0 validation steps only
- `[front-door]` `docs/workflows/process_improvement_batch0/README.md`
- `[deep-benchmark]` `docs/workflows/process_improvement_batch0/deep_thinking_benchmark_v0.md`
- `[resident-audit]` `docs/workflows/process_improvement_batch0/resident_rule_firing_audit_v0.md`
- `[worktree-audit]` `docs/workflows/process_improvement_batch0/worktree_lifecycle_audit_v0.md`
- `[receipt-guide]` `docs/workflows/process_improvement_batch0/review_receipts/README.md`
- `[receipt-template]` `docs/workflows/process_improvement_batch0/review_receipts/_template.json`
- `[map-note]` `docs/workflows/repo_map_recent_changes/batch0_process_pilot_v0.md`

Everything outside this set is read-only and flag-only. Do not patch generated,
canonical, historical review-output, test, hash-pinned, external, installed-skill,
or user-level paths. If the correct fix requires a design change or off-scope
file, return `NEEDS_ARCHITECTURE_PASS`, revert any partial patch, and report
findings only.

## Review axes

1. **Counting truth** — malformed, invalid, or duplicated receipts never count;
   `0`, `9`, `10`, and `11` have the specified eligibility; errors cannot be
   masked by later commands.
2. **Completion semantics** — one counted unit is one material review after CA
   adjudication, not a prompt/report/patch/verdict or copied receipt.
3. **Evidence integrity** — referenced report/evidence paths exist; provenance
   may be honestly `unrecorded`; no identity is fabricated.
4. **CI enforcement** — the tracker runs inside the existing named CI job used
   by the repository's merge controls; the separate workflow does not create a
   bypass or contradictory result.
5. **Notification truth** — issue permissions are least-privilege; eligibility
   is derived from validated receipts; exact-title deduplication prevents a
   second issue; creation or assignment failure is visible.
6. **Workflow trigger coverage** — the tenth receipt merged to `main` triggers
   notification; pull requests validate without sending owner notifications;
   manual dispatch cannot bypass validation.
7. **Temporary doctrine** — the review obligation retires after owner synthesis;
   threshold completion does not authorize Batch 1, lesson promotion, validation,
   readiness, or cleanup.
8. **Probe honesty** — deep-thinking candidates remain eligibility-pending,
   resident-rule results remain unknown until observed, and worktree counts are
   treated as volatile snapshots rather than cleanup authority.
9. **Scope and retrieval** — headers, paths, current Forseti naming, map note,
   and propagation surfaces resolve without importing stale Orca authority.
10. **Operational cost** — flag any field or step that creates ceremony without
    changing selection, adjudication, closure, or owner notification.

## Validation evidence to inspect and rerun

- `python .github/scripts/batch0_process_tracker.py --self-test`
- `python .github/scripts/batch0_process_tracker.py --json`
- Python AST parse and YAML parse of the tracker/workflows
- `git diff --check`
- `python .agents/hooks/check_retrieval_header.py --changed --strict`
- `python .agents/hooks/check_map_links.py --strict`
- `python .agents/hooks/check_placement.py --strict`
- `python .agents/hooks/check_repo_map_freshness.py --changed --strict --message "repo-map-ack: Batch 0 uses existing mapped overlay/workflow/GitHub areas; recent-change note added."`

Report actual results. A skipped, unavailable, failing, or timed-out check stays
visible and cannot be rewritten as success. Do not create a live GitHub issue as
part of review.

## Controller output and patch contract

Write the durable report to the bound report destination. Findings come first,
ordered by priority. Each finding carries its target label, severity, confidence,
location, issue, evidence, impact, minimum closure condition, and next authorized
action. Low-confidence/minor findings may use the compact one-line form.

Patch only the named target set, do not commit, and return:

- unified diff, with target labels in the accompanying finding/change map;
- neutral, decision-sufficient citations for each proposed change;
- one overall verdict plus materially different per-target sub-verdicts;
- residual risk and validation gaps;
- `NEEDS_ARCHITECTURE_PASS` with no retained partial patch for design-level problems.

The home/CA model adjudicates every finding and hunk before anything is kept.
The controller's report, diff, and verdict are claims to adjudicate, not premises.

After the final report write, run:

`python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/batch0_process_pilot_implementation_adversarial_review_v0.md`

If the report changes afterward, rerun the check. This is report-shape/integrity
evidence only, not approval or review-quality proof.

Close chat with the compact `review_summary` shape from
`.agents/workflow-overlay/communication-style.md`. The review is decision input
only, not approval, validation, readiness, mandatory remediation, or automatic
patch authority beyond this bounded commission.
