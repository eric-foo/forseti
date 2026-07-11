# Review-Report Mechanics — Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch prompt
scope: >
  Commission a de-correlated review of the bounded review-report mechanics
  implementation and allow patches only inside its three named implementation
  targets. The report records decision input for later home-model adjudication.
use_when:
  - Reviewing the completed codex/review-report-mechanics implementation diff.
  - Attacking fake-pass behavior and review-judgment boundary leakage before closeout.
authority_boundary: retrieval_only
```

**Goal:** catch mechanical false-success paths and any leakage into substantive
review judgment before the runner is relied on by cold review lanes.

**Done looks like:** the independent controller has inspected the exact branch
diff, run the bound checks, written a source-cited report, and either left a
bounded working-tree patch for home-model adjudication or returned a precise
blocker/escalation. This is the controller target and a review axis to attack,
not a pass-if-matched bar.

## Prompt Binding

- Prompt source: `docs/prompts/reviews/review_report_mechanics_adversarial_code_review_and_patch_prompt_v0.md`
- Template kind: `review`; the bundled generic review layout is used because
  the Forseti registry has no registered repo-code-review template. The current
  owner-authorized fused handoff binds this otherwise-unbound review kind.
- Output mode: `review-report`.
- Required report path:
  `docs/review-outputs/review_report_mechanics_adversarial_code_review_v0.md`.
- Edit permission: `patch-only` for the three named implementation targets;
  write permission also covers only the required review report. Do not commit.
- Review lane: `workflow-code-review`, with `workflow-deep-thinking` first.
- Model lane: unbound and not required. The different-vendor condition below is
  a de-correlation who-constraint, not a recommendation, ranking, or route.
- Access: `repo` mode. Inspect the pinned worktree directly; no context-pack,
  alternate checkout, clone, or recreated-source fallback is allowed.

```yaml
forseti_start_preflight:
  agents_read: required_on_intake
  overlay_read: required_on_intake
  source_pack: bounded_custom_review_report_mechanics
  edit_permission: patch-only
  target_scope: three named implementation files plus the exact review-report destination
  dirty_state_checked: required_on_intake
  blocked_if_missing: >
    exact worktree, expected branch, handoff base commit, clean dispatch state,
    named targets, checker interfaces, or available workflow-code-review lane
repo_map_decision: not_needed
repo_map_reason: "The handoff and this prompt exhaustively name the target and controlling sources."
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: ""
```

## Actor / Model-Family Receipt

Before any review or patch work, complete and report this receipt:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI GPT
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_confirm
```

The controller must be from a different upstream model vendor/family than the
recorded author/home family. If you cannot truthfully confirm that constraint,
return `BLOCKED_CONTROLLER_NOT_DECORRELATED` before reviewing. As the receiving
controller, do not launch a replacement controller or any recursive reviewer.

## Load Contract

- Source-of-truth worktree:
  `C:\Users\vmon7\.codex\worktrees\a8dd\orca`.
- Expected branch: `codex/review-report-mechanics`.
- Review base: handoff commit
  `722bb5fc3298c9170f011e91a9c6b44389540c22`.
- Expected review revision: the branch `HEAD` containing this prompt and the
  three named implementation targets. Record the observed `HEAD` before review.
- Dispatch dirty-state allowance: clean. After preflight, only the three named
  patch targets and the required report path may become modified/untracked.
- Source hierarchy: current user instruction, `AGENTS.md`, Forseti overlay,
  accepted Forseti docs, then task files. External workflow source and `jb` are
  read-only and are not Forseti authority.
- Doctrine change decision: none. This is a bounded implementation review; do
  not change product, workflow, validation, review, output, or lifecycle doctrine.

Confirm the worktree, branch, observed `HEAD`, clean state, base ancestry, and
target paths before review. If any differs, return the nearest precise blocker;
do not review an alternate checkout or summary.

## Method And Source Order

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review`. Do not
   APPLY either method yet; use them only to prepare a neutral reading lens.
3. SOURCE-LOAD this bounded pack:
   - `docs/prompts/handoffs/review_report_mechanics_fused_continuation_handoff_v0.md`
   - `.agents/workflow-overlay/source-loading.md` — rule, preflight, targeted-read protocol
   - `.agents/workflow-overlay/validation-gates.md` — Current Gates
   - `.agents/workflow-overlay/safety-rules.md`
   - `.agents/workflow-overlay/review-lanes.md` — Current Lanes and Rules
   - `.agents/workflow-overlay/delegated-review-patch.md` — code-diff sibling mode and interface
   - `.agents/hooks/check_review_output_provenance.py`
   - `.agents/hooks/check_review_summary.py`
   - `.github/scripts/review-report-mechanics.py`
   - `.github/scripts/README.md`
   - `forseti-harness/tests/unit/test_review_report_mechanics.py`
4. Inspect `git diff --stat 722bb5fc3298c9170f011e91a9c6b44389540c22...HEAD`
   and every changed hunk in the three named targets.
5. Declare `SOURCE_CONTEXT_READY`, or `SOURCE_CONTEXT_INCOMPLETE` with exact
   missing/conflicting sources. Do not produce findings before this declaration.
6. After source readiness, APPLY `workflow-deep-thinking` to frame failure modes,
   then APPLY `workflow-code-review` to the bounded implementation diff.

## Commissioned Target And Patch Boundary

Target kind: `delegated_code_review_and_patch`, base-subagent mode.

```yaml
targets:
  - label: "[runner]"
    path: .github/scripts/review-report-mechanics.py
    bounded_patch_scope: implementation defects in this file only
  - label: "[tests]"
    path: forseti-harness/tests/unit/test_review_report_mechanics.py
    bounded_patch_scope: focused test defects or missing proof for the frozen behavior only
  - label: "[discoverability]"
    path: .github/scripts/README.md
    bounded_patch_scope: incorrect or incomplete runner usage documentation only
why_read_only_insufficient: >
  The carried fused advisory commissions a different-family controller to find
  and, when safely local, patch false-pass or boundary defects before the home
  model decides what is kept.
off_scope: read-only; flag, do not edit
```

Do not edit the handoff, checker owners, overlay, prompt, CI, other tests, or any
other path. Do not add a command runner, manifest language, shell evaluation,
review classifier, patch applier, vulnerability scanner, or review-domain
decision output. A necessary off-scope or design-level change is a finding, not
permission to widen the patch.

## Frozen Boundary And Attack Axes

The runner may automate report assembly and mechanical verification only. It
must never discover/select findings or vulnerabilities, assign severity, render
review verdicts, choose remediation, or decide patch content.

Be maximally adversarial and coverage-first within the named target. In
particular, attack:

- false `GATE PASS` paths for Git, checker, permission, malformed-input,
  readback, atomic-write, and unknown/internal failures;
- tracked/untracked path classification, base-ref handling, path containment,
  ignored files, duplicate paths, empty diffs, and cross-platform Git behavior;
- exact byte preservation outside the unique token, diff determinism,
  CRLF/color/config leakage, zero-context output, and exact-once readback;
- whether strict provenance findings, summary strict findings, and advisory enum
  drift are consumed from their existing owners without predicate duplication;
- whether the compact receipt stays limited to observed paths, hashes, exit
  codes, and gate buckets and emits no substantive review decision;
- whether post-write failures remain visible, existing reports require explicit
  replacement, and verify mode is genuinely read-only;
- test honesty: reject mocked success that cannot catch integration or
  subprocess failures, Windows/Linux divergence, or checker interface drift.

Report every issue found, including minor or low-confidence issues. Use
`critical`, `major`, or `minor` only as finding priority, and `high`, `medium`,
or `low` for confidence. List steelman-defeated candidates compactly under
`considered_and_defended`; do not silently discard them.

For every actionable finding include:

- target label and precise `file:line` evidence;
- failure mechanism and user-visible consequence;
- severity and confidence;
- `minimum_closure_condition` as an end state, not implementation instructions;
- `next_authorized_action` within this commission;
- neutral, decision-sufficient source citations.

Patch valid, safely local findings directly in the named files and leave the
working-tree diff uncommitted. The diff, citations, and verdict are claims for
home-model adjudication, not premises to keep. On a design-level problem, return
`NEEDS_ARCHITECTURE_PASS`, revert any partial patch, and return findings only.

## Validation

Validation must preserve real exit codes and may fail. Run at minimum:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp C:\tmp\pytest-review-report-controller forseti-harness\tests\unit\test_review_report_mechanics.py -q
git diff --check
```

Inspect every final changed hunk. Record the exact commands, exit codes, and
not-run/blocker states. A green check is test evidence only, not approval,
readiness, or proof that no substantive defect exists.

## Required Durable Output

Write the full report to
`docs/review-outputs/review_report_mechanics_adversarial_code_review_v0.md`.
The report must include a retrieval header; observed `reviewed_by` and
`authored_by` values (`unrecorded` if operator/tooling did not supply one);
findings first; the controller's unified diff or explicit no-patch state;
per-change citations; overall verdict relative to the executor; validation
evidence; `considered_and_defended`; and residual risk.

State this review-use boundary explicitly: findings, diff, and verdict are
decision input only, not approval, validation, mandatory remediation, or
executor-ready patch authority. The home/CA model must accept, modify, or reject
each material change against the citations before anything is kept, then follow
`.agents/workflow-overlay/communication-style.md`'s Review Adjudication Next Step
tail. Do not commit, push, open a PR, merge, or claim readiness.

After the report write succeeds, return a compact human summary plus courier
YAML containing the report path, observed branch/HEAD, finding IDs, patch state,
validation exit codes, residual risk, and the next authorized action. If the
report write fails, return `FAILED_REVIEW_OUTPUT_WRITE` with
`review_location: chat_only_current_thread`; do not claim chat is an equivalent
artifact and do not emit a `report_path`.
