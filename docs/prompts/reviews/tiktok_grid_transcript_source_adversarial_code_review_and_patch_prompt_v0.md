# TikTok Grid Transcript Source Adversarial Code Review-and-Patch Prompt v0

~~~yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Fused pre-closeout commission for a de-correlated review-and-patch pass over
  the bounded TikTok profile-grid transcript-source implementation diff.
use_when:
  - Reviewing the uncommitted TikTok grid transcript-source lane before closeout.
  - Resuming the fused lane after the delegated controller returns.
authority_boundary: retrieval_only
branch_or_commit: codex/tiktok-grid-transcript-source-20260715 at 3e24ff41e272e67f015e8ba47188f741ec23739a with the exact dirty-file hashes below
downstream_consumers:
  - Independent de-correlated controller with direct access to the named worktree.
  - Commissioning Chief Architect adjudicating the returned findings and diff.
stale_if: >
  The branch, HEAD, allowed dirty-file set, or any target hash differs before
  receiver source loading.
~~~

## Run status

This prompt is preparation_only_receiver_to_bind. It is not dispatch-ready
until the receiving controller records a concrete receiver binding, proves
direct write capability in the exact effective target worktree, confirms no
concurrent writer, and proves the controller vendor differs from the OpenAI
author vendor. Do not source-load or review from a summary, alternate checkout,
or recreated diff.

## Forseti prompt preflight

~~~yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_S0_plus_target_diff_and_targeted_review_bindings
  edit_permission: patch-only
  target_scope:
    target_kind: delegated_code_review_and_patch
    worktree: C:\tmp\orca-tt-grid-subs-20260715
    branch: codex/tiktok-grid-transcript-source-20260715
    head: 3e24ff41e272e67f015e8ba47188f741ec23739a
    base_commit: 3e24ff41e272e67f015e8ba47188f741ec23739a
  dirty_state_checked: yes
  blocked_if_missing: >
    Block before source loading if receiver binding, exact target identity,
    direct write capability, no-concurrent-writer state, or cross-vendor
    de-correlation cannot be proven.

preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
repo_map_decision: not_needed
repo_map_reason: Exact code/test targets and controlling overlay sections are already bound.
authorization_basis: >
  Current owner-invoked /fused implementation turn, whose scoping gate requires
  delegated adversarial review before closeout.
objective: >
  Ensure normal TikTok creator onboarding can recover source-native WebVTT from
  the exact selected profile item-list record when the grid overlay lacks
  itemStruct and DOM tracks, without direct navigation, cross-video reuse, or
  raw signed-URL persistence.
intended_decision: >
  Return evidence-backed findings and any smallest-complete bounded fixes for
  Chief Architect adjudication; do not decide what is kept.
output_mode: review-report
input_prompt_source: docs/prompts/reviews/tiktok_grid_transcript_source_adversarial_code_review_and_patch_prompt_v0.md
output_artifact_path: docs/review-outputs/tiktok_grid_transcript_source_adversarial_code_review_v0.md
template_kind: none
template_reason: repo code review uses workflow-code-review and the delegated code-diff convention; no registered code-review template is bound.
doctrine_change_decision: no
isolation_decision: existing isolated worktree off origin/main; review patches only this lane.
controlling_source_state: clean at authoring read; only named code/test targets and this prompt are dirty.
moving_base_note: >
  origin/main advanced to 7f690fbf9aa2f3c07d5ed957a2697042f19309e9 after this
  lane started. Review the dirty diff against the exact base commit above; do
  not rebase or retarget before adjudication.
thread_operating_target_continuity: no durable thread operating target was supplied; omitted without inventing one.
~~~

## Receiver binding — complete before source loading

~~~yaml
receiver_binding:
  commissioned_act: repo-changing delegated code review-and-patch
  receiver_class: receiver_to_bind
  launch_checkout: receiver_to_observe
  effective_target_worktree: C:\tmp\orca-tt-grid-subs-20260715
  expected_branch: codex/tiktok-grid-transcript-source-20260715
  expected_head: 3e24ff41e272e67f015e8ba47188f741ec23739a
  target_identity_semantics: exact HEAD plus exact allowed dirty-file hashes
  direct_write_capability_proof: receiver_to_observe
  no_concurrent_writer: receiver_to_observe
  status: preparation_only
  source_loading_blocked_until: >
    Rebind to a concrete receiver class allowed by
    .agents/workflow-overlay/decision-routing.md and verify every field above.

actor_model_family_receipt:
  author_or_home_role: author_and_commissioning_CA
  author_vendor: OpenAI
  authored_by: openai_gpt5_codex
  controller_role: de_correlated_controller
  controller_vendor: operator_to_fill
  current_receiving_actor_role: receiver_to_bind
  dispatch_mode: independent_repo_controller
  required_de_correlation_bar: cross_vendor_discovery
  de_correlation_status: blocked_until_controller_vendor_is_observed_and_differs_from_OpenAI
  boundary: This is a who-constraint, not runtime-model recommendation or selection.
~~~

If the controller vendor is OpenAI, unknown, or undisclosed, stop with
BLOCKED_DE_CORRELATION_UNPROVEN. Do not substitute self-review or a same-turn
subagent and do not claim cross-vendor discovery.

## Exact target manifest and permissions

~~~yaml
target_manifest:
  - path: forseti-harness/source_capture/tiktok/creator_onboarding.py
    sha256: ed64ee6b336f0efbe42d7ae44b2c79317e7dc8d5c3c35e2178af92a90190dd65
    permission: patch-only
  - path: forseti-harness/source_capture/tiktok/live_batch_probe.py
    sha256: d5dacee5a5176759120d53cb78e3d32ce8f8af1061d43512dc8c559d025c3ce4
    permission: patch-only
  - path: forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
    sha256: 64b7885e97247f351ed8929e95dec2b28101526ccb02364695a8cc65b68fa37a
    permission: patch-only
  - path: forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
    sha256: 3fddc0b67cd22aa0ceffb192f50b9410ffe68bc9c8570f5f5bbb1551bbc831d1
    permission: patch-only
prompt_artifact:
  path: docs/prompts/reviews/tiktok_grid_transcript_source_adversarial_code_review_and_patch_prompt_v0.md
  permission: read-only
review_report:
  path: docs/review-outputs/tiktok_grid_transcript_source_adversarial_code_review_v0.md
  permission: docs-write
~~~

The four target-manifest files are the entire patchable implementation scope.
The report path is separately authorized only as the review-output artifact.
Everything else is read-only and flag-only. Do not widen the patch set; a
correct fix outside it requires re-commissioning. Preserve all pre-existing user
work and stop on any additional modified or untracked path.

## Why patch-capable review is commissioned

Ordinary source-read-only review would detect defects but force another
correlated authoring round across a source-critical extraction seam. The fused
gate commissions one de-correlated controller to review the complete bounded
diff and author only directly supported fixes, after which the OpenAI home
model adjudicates every finding and hunk before anything is kept.

## Required reads and method sequence

1. Read AGENTS.md and .agents/workflow-overlay/README.md.
2. Read the environment_baseline constant in
   docs/prompts/templates/shared/forseti_preflight_defaults_v0.md.
3. Read the targeted commissioning sections in
   .agents/workflow-overlay/delegated-review-patch.md: When it applies, The
   loop, Access selection rule, De-correlation, Code-diff target kind, and
   Overlay Interface.
4. Read .agents/workflow-overlay/review-lanes.md sections Current Lanes, Review
   Doctrine, and Rules.
5. REFERENCE-LOAD workflow-code-review. Do not APPLY it yet. If unavailable,
   return BLOCKED_REVIEW_LANE_UNAVAILABLE and make no patch.
6. SOURCE-LOAD the exact branch diff and four target files in place. Read
   adjacent production source only to verify a finding; it remains read-only.
7. Declare SOURCE_CONTEXT_READY, or return SOURCE_CONTEXT_INCOMPLETE with the
   exact missing source or conflict.
8. Only after readiness, APPLY workflow-code-review to the bounded diff.

workflow-deep-thinking is intentionally omitted: this is an exact-revision,
bounded technical review with settled behavior, file scope, patch authority,
and validation route. Do not reopen product or acquisition-route scope.

## Frozen behavior contract

- A profile-grid to selected-tile overlay onboarding run captures a transcript
  when the exact selected /api/post/item_list/ item exposes a supported
  source-native subtitle URL, even if overlay hydration and DOM tracks do not.
- Source priority for the overlay route is matching overlay item metadata, then
  exact profile-grid item metadata, then the matched overlay DOM track. A
  present unsupported URL remains a loud rejection and is never fetched.
- Raw subtitle URLs are ephemeral. They must not appear in the grid window,
  selection, cadence result, admitted packet, review report, logs, or errors.
- item_struct_present describes overlay/direct hydration only; grid metadata
  must have distinct provenance.
- Exact video-ID binding, creator checks, supported-host enforcement,
  sensitive-material guards, comments, cadence, and direct-video behavior must
  not regress.
- Videos with no subtitle URL remain valid captures with the existing explicit
  non-attempt reason.
- Out of scope: direct-video fallback navigation, mini-player automation,
  speech-to-text, transcript inference, a second acquisition route, broad
  capture refactors, or unrelated cleanup.

## Adversarial review focus

Be findings-first and coverage-first within the named scope. Attack:

- cross-video or cross-creator metadata reuse, missing identity checks, and
  duplicate/cursor ordering;
- raw signed-URL persistence through artifacts, exceptions, assertions, reprs,
  reports, or provenance;
- source-precedence errors, especially unsupported-host fallthrough and direct
  route behavior drift;
- false-success tests that do not prove the cold onboarding to deep-capture to
  parsed-WebVTT result;
- nested TikTok payload shapes, malformed metadata, and no-subtitle behavior;
- public-call/recursion compatibility and capture-contract/provenance truth;
- security, account-safety, comment admission, cadence, and packet regressions.

Report every issue with severity (critical, major, minor) and confidence (high,
medium, low). Each actionable finding includes exact file/line evidence,
minimum_closure_condition, and next_authorized_action. Put steelman-defeated
candidates in considered_and_defended; label optional hardening optional and
non-required. Do not emit patch_queue_entry.

## Patch authority

Patch only when the finding is real, the smallest complete fix fits wholly
inside the four named targets, and cited evidence supports it. Keep a unified
diff and per-change neutral citations. If the defect is design-level or needs
any off-scope file, return NEEDS_ARCHITECTURE_PASS, revert/quarantine any
partial patch, and return findings only.

## Validation

Validation preserves failure visibility: GATE PASS means exit zero; GATE FAIL
means nonzero and must not be masked; BLOCKED names the exact blocker; NOT RUN
requires a concrete reason.

Run from C:\tmp\orca-tt-grid-subs-20260715\forseti-harness:

1. After review edits:
   $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --basetemp C:/tmp/pytest-tt-grid-review-focused tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py -q
2. After review edits:
   $files = rg --files tests/unit | rg 'test_tiktok_.*\.py$'; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --basetemp C:/tmp/pytest-tt-grid-review-all $files -q
3. After any code patch, unless blocked:
   $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest --basetemp C:/tmp/pytest-tt-grid-review-full -n 4 --dist=loadfile
4. Always: git diff --check.
5. After final report write, from the worktree root:
   python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/tiktok_grid_transcript_source_adversarial_code_review_v0.md

Author-observed baseline before commission: focused TikTok files 103 passed;
all TikTok unit tests 337 passed with two pre-existing deprecation warnings;
complete harness suite 3,287 passed, 7 skipped, 67 warnings; strict harness
coupling exited zero with an expected scope skip. Inspect this evidence; do not
assume it after a patch.

## Durable report and return contract

Write docs/review-outputs/tiktok_grid_transcript_source_adversarial_code_review_v0.md
with retrieval metadata and:

- commission, exact target, authority, and decision criteria;
- reviewed_by and authored_by (unrecorded only when genuinely unavailable);
- de_correlation_bar: cross_vendor_discovery and the observed vendor receipt;
- findings first, then considered_and_defended;
- unified diff for working-tree edits, with per-change neutral citations;
- validation evidence with pass/fail/blocked/not-run distinctions;
- overall verdict: clean, issues_found, or NEEDS_ARCHITECTURE_PASS;
- residual risks, including that the controller authored any proposed hunks and
  the home model has not adjudicated them;
- review-use boundary: findings, diff, and verdict are decision input only, not
  approval, validation, mandatory remediation, readiness, or keep/land authority.

After the report and provenance checker succeed, return compact review_summary
YAML with report path, reviewer/author provenance, finding counts, verdict,
validation state, residual risk, and next_action:
Return to the commissioning Chief Architect for adjudication.

## Chief Architect adjudication and lifecycle hard stop

The commissioning Chief Architect must adjudicate findings, diff, verdict, and
residuals as claims before any hunk is kept; close self-closable material issues
in that adjudication turn. Once no unresolved material issue remains, batch
commit, push, and PR preparation into exactly one named land step, then evaluate
material next moves only against a visible active goal. If none exists, record
no_visible_active_goal.

The delegate must not commit, push, open/update a PR, merge, stash, reset,
clean, remove or move a worktree, run repository hygiene, or otherwise advance
lifecycle state.
