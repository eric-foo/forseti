# TikTok Zero-Wheel React Subtitle Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Cross-vendor review-and-patch commission for the bounded TikTok zero-wheel
  overlay subtitle-source repair discovered during AK Fragrance onboarding.
use_when:
  - Reviewing the uncommitted zero-wheel React subtitle repair before closeout.
  - Resuming AK Fragrance onboarding after the delegated controller returns.
authority_boundary: retrieval_only
branch_or_commit: codex/tiktok-zero-wheel-react-subtitles at 1ebcf4b6842052f824bf09c21b74e24fe593dd64 with the exact dirty-file hashes below
downstream_consumers:
  - Independent cross-vendor controller with direct access to the named worktree.
  - Commissioning Chief Architect adjudicating the returned findings and diff.
stale_if: >
  The branch, HEAD, allowed dirty-file set, or either implementation target hash
  differs before receiver source loading.
```

## Goal and done condition

Review and, only when directly supported, patch the smallest complete repair so
normal TikTok creator onboarding recovers source-native WebVTT metadata from the
exact open grid overlay even when the profile grid was already fully loaded and
no `/api/post/item_list/` response fires during capture.

Done means the exact-video React source is bounded, fail-closed, correctly
ordered, URL-safe, and regression-tested; all named gates report their real
exit state; and the controller returns findings and any bounded hunks for Chief
Architect adjudication. The controller does not decide what is kept or advance
lifecycle state.

## Forseti prompt preflight

```yaml
output_mode: review-report
template_kind: none
edit_permission: patch-only
target_worktree: C:\tmp\orca-tt-react-subs-20260715
target_branch: codex/tiktok-zero-wheel-react-subtitles
target_head: 1ebcf4b6842052f824bf09c21b74e24fe593dd64
base_commit: 1ebcf4b6842052f824bf09c21b74e24fe593dd64
allowed_dirty_state:
  - forseti-harness/source_capture/tiktok/live_batch_probe.py
  - forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
  - docs/prompts/reviews/tiktok_zero_wheel_react_subtitle_adversarial_code_review_and_patch_prompt_v0.md
reviews: findings-first, coverage-first, patch-capable, cross-vendor discovery
doctrine_change: no
input_prompt_source: docs/prompts/reviews/tiktok_zero_wheel_react_subtitle_adversarial_code_review_and_patch_prompt_v0.md
output_artifact_path: docs/review-outputs/tiktok_zero_wheel_react_subtitle_adversarial_code_review_v0.md
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
```

## Receiver binding — complete before source loading

```yaml
receiver_binding:
  commissioned_act: repo-changing delegated code review-and-patch
  receiver_class: receiver_to_bind
  launch_checkout: receiver_to_observe
  effective_target_worktree: C:\tmp\orca-tt-react-subs-20260715
  expected_branch: codex/tiktok-zero-wheel-react-subtitles
  expected_head: 1ebcf4b6842052f824bf09c21b74e24fe593dd64
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
```

If the controller vendor is OpenAI, unknown, or undisclosed, stop with
`BLOCKED_DE_CORRELATION_UNPROVEN`. Do not substitute self-review or a same-turn
subagent and do not claim cross-vendor discovery.

The receiver performs one fresh target-state read before source loading:
worktree path, branch, HEAD, dirty state, named files, target hashes, and the
validation commands below. Stop on any extra modified or untracked path.

## Exact target manifest and permissions

```yaml
target_manifest:
  - path: forseti-harness/source_capture/tiktok/live_batch_probe.py
    sha256: a1c7e1b048535852a261e95b84af9341caff63ad81d8f03d2bd4bc6b97db6093
    permission: patch-only
  - path: forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
    sha256: b5aa81edeff002855ceca184ce7f1dbc2a61b93e0fc44fcda263649b2cd462f6
    permission: patch-only
prompt_artifact:
  path: docs/prompts/reviews/tiktok_zero_wheel_react_subtitle_adversarial_code_review_and_patch_prompt_v0.md
  permission: read-only
review_report:
  path: docs/review-outputs/tiktok_zero_wheel_react_subtitle_adversarial_code_review_v0.md
  permission: docs-write
```

The two target-manifest files are the entire patchable implementation scope.
The report path is separately authorized only as the review output. Everything
else is read-only and flag-only. A correct fix outside this scope requires
`NEEDS_ARCHITECTURE_PASS`; do not widen the patch set.

## Required reads and sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read the `environment_baseline` constant in
   `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`.
3. Read the targeted sections in
   `.agents/workflow-overlay/delegated-review-patch.md`: `When it applies`,
   `The loop`, `Access selection rule`, `De-correlation`, `Code-diff target
   kind`, and `Overlay Interface`.
4. Read `.agents/workflow-overlay/review-lanes.md` sections `Current Lanes`,
   `Review Doctrine`, and `Rules`.
5. REFERENCE-LOAD `workflow-code-review`; do not APPLY it yet. If unavailable,
   return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and make no patch.
6. SOURCE-LOAD the exact dirty diff and both target files in place. Read
   adjacent production source only to verify a finding; it remains read-only.
7. Declare `SOURCE_CONTEXT_READY`, or return `SOURCE_CONTEXT_INCOMPLETE` with
   the exact missing source or conflict.
8. Only after readiness, APPLY `workflow-code-review` to the bounded diff.

`workflow-deep-thinking` is intentionally omitted: this is an exact-revision,
bounded technical repair with settled behavior, file scope, patch authority,
and validation route.

## Incident evidence and frozen behavior contract

Observed production evidence before this repair:

- AK Fragrance onboarding admitted Bronze packet
  `01KXJM74AH57YW7TSPEGZ5HDRF`, then correctly stopped before Silver,
  Judgment, or Registry because all eight rows lacked transcript cues.
- The grid already had 30 anchors, so capture required zero acquisition wheels
  and observed no `/api/post/item_list/` responses.
- A prior bounded probe showed six of those same eight exact video IDs carry
  source-native subtitle metadata in item-list records.
- A live read-only check of this repair on overlay video
  `7659469523459902753` bound the same overlay and React-source video ID, found
  one subtitle record with a URL field, detected the comment surface, and
  returned to the creator profile. No URL value was printed or persisted.

Required behavior:

- The grid-overlay route may read React-owned `videoInfo.subtitleInfos` only
  from the currently open overlay and only for an exact path video-ID match.
- Source priority is: matching overlay/direct `item_struct`, then exact overlay
  React video info, then exact profile item-list metadata, then matched visible
  DOM track.
- `item_struct_present` continues to describe hydration only. React metadata
  has distinct provenance: `overlay_react_video_info`.
- Raw subtitle URLs remain ephemeral. They must not appear in cadence results,
  admitted packets, logs, errors, assertions, review output, or provenance.
- A present unsupported subtitle host remains a loud rejection and must never
  be fetched or silently fall through to a lower-priority supported source.
- Missing or mismatched video identity fails closed; no cross-video or
  cross-creator metadata reuse is allowed.
- Videos with no usable subtitle URL retain the honest existing non-attempt
  outcome.
- No extra wheel, direct-video navigation, mini-player automation, account
  mutation, speech-to-text, second acquisition route, or broad refactor is in
  scope.
- Comment admission, cadence, blocker triage, sensitive-material guards, and
  direct-video behavior must not regress.

## Adversarial review focus

Report every failure mode found within scope, including uncertain or minor
ones. Attack at least:

- whether the JS walk can bind a nested object that merely resembles the
  current video, miss the actual React shape, cross overlay boundaries, or
  reuse stale props;
- whether the exact-ID check is independently preserved after serialization;
- boundedness and failure behavior of DOM-node property enumeration and the
  recursive object walk, including cycles, depth, object budget, getters,
  exceptions, and pathological overlay size;
- subtitle-field sanitization and every raw-URL leak surface;
- source precedence, especially unsupported-host fallthrough and metadata
  without a usable URL;
- false-success tests that bypass overlay readiness, fail to prove WebVTT fetch
  and parse, or do not prove URLs are absent from serialized output;
- public-call compatibility, direct-route drift, provenance truth, account
  safety, comments, cadence, and packet behavior.

Each finding includes severity (`critical`, `major`, `minor`), confidence
(`high`, `medium`, `low`), exact file/line evidence, a
`minimum_closure_condition`, and `next_authorized_action`. List steelman-defeated
candidates under `considered_and_defended`. Label optional hardening as optional
and non-required. Do not emit `patch_queue_entry`.

## Patch authority

Patch only when a finding is real, the smallest complete fix fits wholly inside
the two target files, and cited evidence supports it. Keep a unified diff and
per-change neutral citations. If the defect is design-level or needs any
off-scope file, return `NEEDS_ARCHITECTURE_PASS`, revert or quarantine any
partial patch, and return findings only.

## Validation

Run from `C:\tmp\orca-tt-react-subs-20260715\forseti-harness`. Preserve real
failure visibility: `GATE PASS` means exit zero; `GATE FAIL` means nonzero;
`BLOCKED` names the exact blocker; `NOT RUN` requires a concrete reason.

1. After review edits:
   `$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --basetemp C:/tmp/pytest-tt-react-review-focused tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_tiktok_live_batch_probe.py -q`
2. After review edits:
   `$files = rg --files tests/unit | rg 'test_tiktok_.*\.py$'; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --basetemp C:/tmp/pytest-tt-react-review-all $files -q`
3. After any code patch, unless blocked:
   `$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest --basetemp C:/tmp/pytest-tt-react-review-full -n 4 --dist=loadfile`
4. Always: `git diff --check`.
5. After the report write, from the worktree root:
   `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/tiktok_zero_wheel_react_subtitle_adversarial_code_review_v0.md`

Author-observed baseline before commission:

- focused files: 105 collected and passed, exit 0;
- all TikTok unit tests: 339 collected and passed, exit 0, with two existing
  datetime deprecation warnings;
- complete harness: 3,298 passed, 7 skipped, 67 warnings, exit 0;
- `git diff --check`: exit 0;
- live overlay extractor check: exact ID bound, one subtitle record found, no
  raw URL value printed or persisted.

Inspect this evidence; do not assume it after a patch. Passing gates show only
that the diff does not fail them; they do not prove correctness.

## Durable report and return contract

Write
`docs/review-outputs/tiktok_zero_wheel_react_subtitle_adversarial_code_review_v0.md`
with retrieval metadata and:

- commission, exact target, authority, and behavior criteria;
- `reviewed_by`, `authored_by`, `de_correlation_bar: cross_vendor_discovery`,
  and the observed vendor receipt;
- findings first, then `considered_and_defended`;
- unified diff for working-tree edits, with per-change neutral citations;
- validation evidence with pass/fail/blocked/not-run distinctions;
- verdict: `clean`, `issues_found`, or `NEEDS_ARCHITECTURE_PASS`;
- residual risks, including that returned hunks are not yet adjudicated; and
- the review-use boundary: findings, diff, and verdict are decision input only,
  not approval, validation, mandatory remediation, readiness, or keep/land
  authority.

After the report and provenance checker succeed, return compact
`review_summary` YAML with report path, reviewer/author provenance, finding
counts, verdict, validation state, residual risk, and `next_action: Return to
the commissioning Chief Architect for adjudication`.

## Chief Architect adjudication and lifecycle hard stop

The commissioning Chief Architect must adjudicate every finding, hunk, verdict,
and residual before anything is kept. Once no unresolved material issue remains,
the home lane may commit, push, and prepare one PR, then resume production
onboarding only after the repair is observed merged.

The delegate must not commit, push, open or update a PR, merge, stash, reset,
clean, remove or move a worktree, run repository hygiene, or otherwise advance
lifecycle state.
