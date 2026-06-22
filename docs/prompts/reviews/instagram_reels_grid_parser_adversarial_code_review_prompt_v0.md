# Instagram Reels Grid Parser Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review prompt for the IG public /reels/ grid parser
  slice: DOM row normalization, passive JSON media candidate extraction, and
  shortcode-keyed source-surface-preserving joins.
use_when:
  - Commissioning a bounded review of the IG reels grid parser before runner or packet-writer wiring.
  - Checking whether the parser can preserve public /reels/ engagement metadata without overclaiming canonical counts, dates, captions, or ad status.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_target_parser_slice
  repo_map_decision: not_needed
  repo_map_reason: Target files and owning capture-spine context were already named by the current workstream.
  edit_permission: read-only
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\source_capture\ig_reels_grid.py
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\tests\unit\test_ig_reels_grid.py
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\orca\product\spines\capture\core\source_families\social_media\instagram\ig_profile_grid_dom_engagement_recon_and_spec_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\docs\prompts\architecture\instagram_reels_profile_metadata_capture_architecture_prompt_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\source_capture\ig_momentum_harvest.py
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\tests\unit\test_ig_momentum_harvest.py
      - C:\Users\vmon7\Desktop\projects\orca\orca-harness\tests\unit\test_source_capture_ig_calls_packet.py
  dirty_state_checked: yes_by_dispatcher
  branch_or_commit_reference: main @ 3ecc2ee6, dirty worktree allowed only for the named untracked parser slice and named context artifacts
  controlling_source_state: mixed_dirty_worktree; strict readiness and formal pass claims are not authorized
  output_mode: file-write
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: filesystem-output_preferred
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\instagram_reels_grid_parser_advisory_code_review_v0.md
  doctrine_change_decision: no doctrine change requested; review prompt only
  isolation_decision: read-only review; do not create or switch branches/worktrees
  validation_gates:
    - inspect parser and tests
    - optionally rerun focused pytest command if repo execution is available
  blocked_if_missing:
    - target parser or tests are unavailable
    - reviewer cannot distinguish source code findings from live IG/proxy/runner behavior
```

## Commission

Run a read-only adversarial code review of the parser slice. The review target is the implementation code plus its tests, not the live Instagram probe, not Playwright, not proxy/CloakBrowser behavior, and not a packet writer.

This prompt was routed from an explicit delegated-review-patch request, but Orca's delegated-review-patch overlay marks multi-file implementation/code diffs as non-eligible for that provisional bounded patch convention unless separate patch execution is bound. Therefore this is a read-only `workflow-code-review` commission with adversarial posture. No patch execution, patch queue, formal verdict, readiness claim, or runtime model recommendation is authorized.

Fitness reference:

- Goal: make the parser safe to wire into a low-interaction public `/reels/` runner without silently corrupting engagement metadata.
- Done looks like: the review identifies whether shortcode joins, source-surface preservation, counts, dates, captions, ad-signal fields, and no-hover DOM engagement parsing are correct enough for the next runner-wiring slice, with concrete closure conditions for any material finding.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.85\skills\workflow-deep-thinking\SKILL.md`
- `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.85\skills\workflow-code-review\SKILL.md`

Then SOURCE-LOAD the target files and the context-only files listed in preflight. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` for findings-first review.

## Review Axes To Attack

Focus on concrete correctness or review-confidence failures. In particular, inspect:

- Whether recursive JSON candidate discovery can misclassify non-media nodes with `shortcode` or `code`, duplicate nested media, or attach counts/captions from the wrong payload layer.
- Whether source-surface labeling preserves distinctions among DOM grid engagement, passive page JSON, `/api/v1/clips/user/`, `web_profile_info`, `profile_feed`, and item-page metadata without selecting a false canonical count.
- Whether shortcode extraction and DOM path filtering handle `/reel/`, `/p/`, profile-prefixed paths, absolute `href`, query strings, duplicates, and wrong-profile rows.
- Whether hidden DOM numeric extraction can wrongly treat unrelated numeric text as likes/comments, especially when DOM order changes or a visible views number appears multiple times.
- Whether count extraction precedence risks dropping valid zero values, confusing play/view/count fields, or over-trusting `device_timestamp` as publish time.
- Whether caption, sponsor, affiliate, and ad-term parsing preserve evidence without overclaiming that a reel is or is not an ad.
- Whether tests cover the real intended invariants, including no-hover parsing, source conflict preservation, timestamp conversion, and known IG source-surface labels.
- Whether any API, browser, proxy, stealth, token-cost, runner, storage, projection, or ad-classification behavior is accidentally implied by this pure parser slice.

## Validation Evidence To Inspect

Dispatcher-observed focused validation from the implementation turn:

```powershell
cd C:\Users\vmon7\Desktop\projects\orca\orca-harness
python -m pytest -q tests/unit/test_ig_reels_grid.py tests/unit/test_ig_momentum_harvest.py tests/unit/test_source_capture_ig_calls_packet.py
```

Observed result in that turn: `23 passed`.

Treat this as evidence to inspect, not as a formal validation claim. If you have repo execution access, rerun the command and report the observed result. If you cannot run it, report `validation_not_run` and review from source.

## Output Contract

Preferred reviewer output is a durable report at:

`C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\instagram_reels_grid_parser_advisory_code_review_v0.md`

If filesystem write is unavailable, return the same findings-first report in chat and set `review_location: chat_only_current_thread`. Do not claim chat is equivalent to a missing durable report.

Report findings first, ordered by materiality. Each finding must include:

- `finding_id`
- commissioned target and purpose
- file and line or stable structural anchor
- implementation evidence
- authority or evidence basis
- correctness, validation, runtime, or review-confidence impact
- `minimum_closure_condition`
- `next_authorized_action`
- verification expectation
- whether `patch_queue_entry` is authorized: always `no` for this prompt

Also include:

- source-read ledger
- strict-only blockers and `not proven` boundaries
- validation run status
- open questions
- residual risk
- review-use boundary: findings are decision input only; they are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

Use these provenance fields in the durable report or chat output:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: operator_to_fill_or_unrecorded
de_correlation_bar: operator_to_fill_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate model identity. Do not recommend, prescribe, rank, or imply runtime model choice.

Close with this courier block so the home model can adjudicate later:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

For this prompt, `proposed patch`, `diff`, `exact requested edits`, formal verdict, severity authority, readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner instruction binds them.
