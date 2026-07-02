# TikTok Bounded Pointer Action — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (adversarial code review)
scope: >
  Read-only adversarial code review of the TikTok bounded pointer-action implementation:
  typed browser pointer action (BrowserPagePointerAction), TikTok live-probe wiring to the
  typed pointer action, and the capped page-owned /api/comment/list admission.
use_when:
  - Deciding whether the bounded pointer-action PR is safe, scoped, and truthfully claimed before merge.
authority_boundary: retrieval_only
reviewed_by: claude-fable-5 (Anthropic)
authored_by: OpenAI/GPT-family Codex (exact version unrecorded)
de_correlation_bar: cross_vendor_discovery
target_commit: d392d3226d1510ab7ff9f2070c9b025d3adce979
target_branch: codex/tiktok-bounded-pointer-action
pr: https://github.com/eric-foo/orca/pull/575 (prompt-stated draft; PR state not independently observed)
recommendation: patch_before_merge
```

## Commission and de-correlation

- **Commission**: filed cross-recipient read-only adversarial code review per
  `docs/prompts/reviews/tiktok_bounded_pointer_action_adversarial_code_review_prompt_v0.md`.
- **De-correlation**: the reviewed patch was authored by an OpenAI/GPT-family Codex agent. This
  review is performed by an Anthropic/Claude controller (`claude-fable-5`), which is a different
  vendor/model lineage from OpenAI/GPT — the `cross_vendor_discovery` bar is satisfied. This is a
  who-constraint receipt, not a runtime model recommendation.
- **Method**: `workflow-deep-thinking` and `workflow-code-review` were REFERENCE-LOADed before
  source loading, then APPLIED after `SOURCE_CONTEXT_READY`. Both methods were available; strict
  findings below rest on source-verified evidence, not on this prompt's orientation text.

## Confirm-do-not-trust verification (repo state)

- `git rev-parse HEAD` → `d392d3226d1510ab7ff9f2070c9b025d3adce979` (reviewed target commit).
- `git status --short --branch` → on `codex/tiktok-bounded-pointer-action`, up to date with its
  origin remote, working tree clean (0 modified, 0 untracked). Target source/test files are clean
  relative to this head.
- `git diff --name-only origin/main...HEAD` → exactly five paths, all in declared scope:
  - `docs/prompts/reviews/tiktok_bounded_pointer_action_adversarial_code_review_prompt_v0.md` (this prompt artifact)
  - `orca-harness/source_capture/adapters/browser_snapshot.py`
  - `orca-harness/source_capture/tiktok/live_batch_probe.py`
  - `orca-harness/tests/unit/test_source_capture_browser_snapshot.py`
  - `orca-harness/tests/unit/test_tiktok_live_batch_probe.py`
- No target-scope mismatch; `BLOCKED_TARGET_MISMATCH` does not apply.

## Source-read ledger

Authority (read before strict findings):

- `AGENTS.md` — agent kernel, smallest-complete-intervention, real-failure-visibility rules.
- `.agents/workflow-overlay/README.md` — overlay authority and binding rule.
- `.agents/workflow-overlay/source-loading.md` — targeted-read/claim-level source discipline.
- `.agents/workflow-overlay/prompt-orchestration.md` — review-prompt defaults; provenance fields.
- `.agents/workflow-overlay/review-lanes.md:22-144` — findings-first default, severity labels
  (`critical`/`major`/`minor`) for priority only, `reviewed_by`/`authored_by`, two-bar
  de-correlation (family = vendor).
- `.agents/workflow-overlay/validation-gates.md` — gate buckets; git-status reporting.
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` — Step 0
  access gate, C6 block-vs-infra, secret hygiene, no-forged-signatures.
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md:144-198` —
  TikTok partial-slice status; Funmi N30 comment/subtitle admission evidence.
- `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`
  — C1–C8', ride-page's-own-requests, ≤3 requests/video, comments = first page + ≤1 pagination,
  C7 secret hygiene, stop-on-challenge, `fetch_browser_page_observation_capture` as the reuse seam.

Code under review + compatibility context:

- `orca-harness/source_capture/adapters/browser_snapshot.py:29-40` (`BrowserPagePointerAction`),
  `:386-475` (`fetch_browser_page_observation_capture` incl. mutual-exclusion),
  `:665-836` (engine `capture_page_observation` incl. pointer-action ordering),
  `:1052-1199` (`_POINTER_ACTION_TARGET_SCRIPT`, `_normalize_pointer_action`, `_run_pointer_action`),
  `:986-1049` (`_read_observed_page_responses`, `_response_request_metadata`).
- `orca-harness/source_capture/tiktok/live_batch_probe.py:43-45` (cap constant),
  `:132-316` (`run_tiktok_live_batch_probe`), `:342-363` (pointer action + stable seed),
  `:437-486` (page-owned comment-list cap + method/resource filter), `:747-772` (capture contract /
  non-claims), `:887-898` (`__all__`).
- `orca-harness/tests/unit/test_source_capture_browser_snapshot.py` (pointer order/no-target/receipt
  sanitation, mutual exclusion, cap-adjacent behavior).
- `orca-harness/tests/unit/test_tiktok_live_batch_probe.py` (wiring, cap, method filter,
  stop-on-challenge, missing-hydration, no-secret runner flags, batch-admission compatibility).
- `orca-harness/source_capture/tiktok/batch_packet.py`, `orca-harness/source_capture/tiktok/admission.py`
  (read-only compatibility context), `orca-harness/source_capture/tiktok/__init__.py:39-46`
  (explicit re-exports, no `import *`).

Status: `SOURCE_CONTEXT_READY`. All target and required-authority sources loaded and clean.

## Findings (severity-ordered)

No `critical` or `major` findings. One `minor` correctness/hygiene defect confirmed.

### F1 (minor, CONFIRMED) — `__all__` exports a symbol this PR deleted; `import *` is broken

- **Severity**: minor.
- **Location**: `orca-harness/source_capture/tiktok/live_batch_probe.py:891` (the
  `"TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT"` entry in `__all__`).
- **Issue**: This PR replaced the old DOM-`click()` post-load script
  (`TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT = r"""async () => { … }"""`) with the typed
  `_tiktok_open_comments_pointer_action(...)`, deleting the constant's definition, but left the
  constant listed in `__all__`. `__all__` now names a symbol that does not exist in the module.
- **Evidence**:
  - Diff removed the definition: `git diff origin/main...HEAD -- …/live_batch_probe.py` shows
    `-TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT = r"""` / `-async () => {` removed and the call site
    switched to `post_load_pointer_action=_tiktok_open_comments_pointer_action(...)`.
  - Symbol now appears only in `__all__` (line 891) plus two historical docs
    (`docs/workflows/tiktok_comment_response_capture_pr559_adjudication_handoff_v0.md:286`,
    `docs/review-outputs/tiktok_comment_response_capture_adversarial_code_review_v0.md:80`); it has
    no definition in the module.
  - `source_capture/tiktok/__init__.py:39-46` re-exports explicit names (not `import *`), so nothing
    in-tree currently triggers the break — impact is latent, not active.
- **Failure scenario (reproduced)**: from `orca-harness`, `python -c "from
  source_capture.tiktok.live_batch_probe import *"` raises
  `AttributeError: module 'source_capture.tiktok.live_batch_probe' has no attribute
  'TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT'`. Any future `import *` from this module (or tooling that
  iterates `__all__`) fails; the declared public API misrepresents the module and carries a dead
  reference to the replaced approach.
- **Impact**: correctness/hygiene. Breaks `import *`; misstates public API; leaves a stale pointer
  to the removed DOM-click design. Does not affect compileall or the current test suite (both pass)
  because no code path does `import *`.
- **minimum_closure_condition**: `__all__` lists only names defined in the module —
  i.e. the stale `TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT` entry is removed (or a real symbol of that
  name is intentionally reintroduced) — such that `from …live_batch_probe import *` succeeds.
- **next_authorized_action**: authoring lane applies a one-line `__all__` fix (owner-accepted);
  this read-only review does not patch. Advisory remediation direction: delete line 891.
- **patch requested from authoring lane**: yes (advisory; no `patch_queue_entry` emitted — this is a
  read-only lane).

## Answers to the Review Checks

1. **Deterministic / bounded / observable pointer action?** Yes. `BrowserPagePointerAction`
   (`browser_snapshot.py:29-40`) is validated by `_normalize_pointer_action` (`:1095-1133`):
   non-blank name/selector, ≥1 text marker, `wait_after_ms ≥ 0`, `move_steps_min/max > 0` and
   `min ≤ max`, `target_fraction` in `[0,1]` with `min ≤ max`, `random_seed` coerced to int.
   `_run_pointer_action` (`:1136-1199`) does exactly one seeded `mouse.move(steps=…)` + one
   `mouse.click` + one bounded wait — no loops, no retries. Movement/click stay inside the located
   box via a seeded `random.Random(random_seed)`, so output is deterministic per seed. No unbounded
   movement path exists; invalid config raises at normalization rather than producing motion.
2. **Leakage of raw text / coordinates / secrets?** No leak found. `_POINTER_ACTION_TARGET_SCRIPT`
   (`:1052-1092`) reads `aria-label`/`title`/`textContent` only to test marker membership and
   returns counts + box + `target_kind` — never the matched text. `_run_pointer_action` uses the box
   to compute click coordinates but the persisted receipt contains only `action_name`,
   `candidate_count`, `matched_count`, `target_found`, `clicked`, `move_steps`, `wait_ms`,
   `target_kind`, and (on failure) a generic `failure` string — no `x`/`y`/box/text
   (test asserts `"x"`/`"y"` absent, `test_source_capture_browser_snapshot.py:918-919`). Cookie/
   set-cookie headers are stripped in `_read_observed_page_responses` (`:1000-1004`). Storage-state
   path is passed to the engine but recorded only as `storage_state_loaded: bool`. The live probe
   additionally runs `assert_no_sensitive_tiktok_material` over every staged row and the whole
   payload (`live_batch_probe.py:284-315`), and the probe test asserts the endpoint URL, `body_text`,
   auth-root, and storage path are absent from serialized output (`test_tiktok_live_batch_probe.py:145-148`).
3. **Mutual exclusion with `post_load_action_script`?** Yes and correct. `fetch_browser_page_observation_capture`
   raises `ValueError("post_load_action_script and post_load_pointer_action are mutually exclusive")`
   (`browser_snapshot.py:430-431`) when both are supplied, and preserves the script path when only a
   script is given (engine still runs `page.evaluate(post_load_action_script, …)` at `:764-765`).
   The typed pointer path runs only when a pointer action is supplied (`:766-767`). Covered by
   `test_fetch_browser_page_observation_capture_threads_lazy_load_scroll_controls_to_engine` and the
   `"mutually exclusive"` case in `test_…rejects_negative_lazy_load_scroll_controls`.
4. **Failures visible as sanitized receipt failures, not fake success?** Yes. Lookup exception →
   `failure: "pointer_action_lookup_failed"` with `clicked=False`; non-dict result → same;
   malformed/degenerate box → same; click exception → `failure: "pointer_action_click_failed"` with
   `clicked=False` (`:1155-1195`). `clicked=True` asserts only that a click was issued, never that
   comments were captured — capture success is separately and truthfully recorded via
   `matched_comment_response_count` / `admitted_comment_response_count`. No fake-success path.
5. **TikTok wiring uses only the typed pointer action, no anti-detection claims?** Yes.
   `run_tiktok_live_batch_probe` passes `post_load_pointer_action=_tiktok_open_comments_pointer_action(...)`
   and no `post_load_action_script` (`live_batch_probe.py:194-197`); the probe test asserts
   `post_load_action_script is None` and a `BrowserPagePointerAction` is threaded
   (`test_tiktok_live_batch_probe.py:159-167`). `_capture_contract` (`:747-762`) records only factual
   postures (`captcha_solving: false`, `stop_on_challenge: true`, …) and makes no human-mimicry /
   anti-detection / evasion / survivability claim; `_non_claims` (`:765-772`) explicitly disclaims
   scale and ceiling.
6. **Seeded movement without becoming an evasion/scale/safety claim?** Yes. The stepped move exists
   to click inside the target within the narrow need to open the comment panel; it is deterministic
   (seeded) and its only durable trace is a `move_steps` integer. No code comment, receipt field,
   contract key, or non-claim asserts detection avoidance, human mimicry, or survivability. Within
   scope and honestly labeled.
7. **Comment-list cap admits first two page-owned GET fetch/xhr responses while truthfully counting?**
   Yes. `TIKTOK_COMMENT_LIST_RESPONSE_CAP = 2` (`:44`). `_is_page_owned_comment_list_response`
   (`:477-486`) requires the TikTok `/api/comment/list` URL, GET (when method is known), and
   `resource_type ∈ {fetch, xhr}` (when known). `_page_owned_comment_list_responses` (`:437-447`)
   admits in observed order and breaks at 2. The receipt records `matched_comment_response_count`
   (all page-owned matches, uncapped) and `admitted_comment_response_count` (≤2) separately
   (`:426-430`). `test_live_probe_caps_admitted_comment_list_responses` proves matched=3 / admitted=2
   with preserved order (`cid` `["7290","7291"]`); `test_live_probe_filters_non_get_comment_list_responses_when_method_available`
   proves an OPTIONS response is not admitted.
8. **Batch admission still compatible with the probe's staged rows?** Yes. The probe emits
   `grid_result.response_items` + `cadence_result.results/attempted_count/completed_count/
   challenge_count/capture_contract/run_complete_utc`, which `write_tiktok_batch_packet`
   consumes: `_validate_staging_contracts` (`batch_packet.py:460-474`) passes because the probe's
   contract sets all forbidden keys `false`; `_summarize_batch` requires
   `completed_count == len(videos)` (`:421-424`), which holds since each completed row has a
   `video_id`. End-to-end proven by
   `test_live_probe_writes_sanitized_staging_compatible_with_batch_admission` (writes probe staging,
   then admits it: `video_count=1`, `captured_comment_count=1`, subtitle posture
   `source_native_subtitle_not_captured`, url redacted).
9. **Do tests fail under the old behavior and cover the intended surfaces offline?** Yes. Tests
   assert `post_load_action_script is None` and a typed pointer action (would fail against the old
   DOM-script wiring); they exercise pointer lookup→move→click→wait ordering
   (`test_playwright_page_observation_runs_pointer_action_before_dom_and_reads_responses`), the
   no-target no-click path, receipt sanitation (no `x`/`y`), TikTok wiring, GET/OPTIONS method
   filtering, the 2-response cap, stop-on-challenge, missing-hydration stop, and no-secret runner
   flags — all with fake engines / fake Playwright, no live browser or network. Coverage gap
   (optional, non-blocking): no test drives the `pointer_action_lookup_failed` (evaluate raises),
   `pointer_action_click_failed` (mouse raises), or malformed-box branches; see residual R3.
10. **Any design-level (`NEEDS_ARCHITECTURE_PASS`) concern?** No. Findings are code-local; the
    design (typed bounded pointer action, ride-the-page comment capture, cap with truthful counts,
    staging→admission split) is consistent with the TikTok lane spec C2/C3/C6/C7 and the capture
    playbook. `NEEDS_ARCHITECTURE_PASS` is not returned.

## Validation (offline, from the reviewed worktree at HEAD d392d3226)

```powershell
python -m compileall -q orca-harness\source_capture\adapters\browser_snapshot.py orca-harness\source_capture\tiktok\live_batch_probe.py orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py
```
Observed: exit 0 (pass).

```powershell
python -m pytest -q orca-harness\tests\unit\test_source_capture_browser_snapshot.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_tiktok_video_admission.py
```
Observed: `60 passed`, exit 0.

```powershell
git diff --check
```
Observed: exit 0 (no whitespace/conflict markers).

Additional confirmation for F1 (star-import integrity), run from `orca-harness` with the harness on
`PYTHONPATH`:
```
python -c "from source_capture.tiktok.live_batch_probe import *"
→ AttributeError: module 'source_capture.tiktok.live_batch_probe' has no attribute 'TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT'
```

`gh pr checks`: `not_run` (GitHub state not independently observed; optional per prompt).

No live TikTok / browser / network capture, auth-state refresh, cookie/storage inspection, proxy
change, or micro-batch was performed. Offline tests were not upgraded into live-capture,
cross-creator, account-safety, or product-value claims.

## Residual risks (advisory, not findings)

- **R1 — (url, status) dedup precedes method filtering.** In `_read_observed_page_responses`
  (`browser_snapshot.py:993-999`) responses are deduped by `(url, status)` before
  `_is_page_owned_comment_list_response` applies the GET/resource-type filter. If a non-GET and a GET
  response shared an identical URL and status, the earlier one could shadow the later. For the actual
  target this is not reachable: TikTok `/api/comment/list` is same-origin (no CORS-preflight OPTIONS),
  and first-page vs pagination carry distinct `cursor` query params (distinct URLs). The dedup is
  pre-existing (not introduced by this PR) and adds no confirmed defect here; flagged only so a
  future cross-origin or retry variant re-checks ordering.
- **R2 — `clicked=True` does not verify the comment panel opened.** This is intentional and honest
  (capture success is measured by the comment-list response counts, not by `clicked`), but a live run
  should still rely on `admitted_comment_response_count`, not `clicked`, when judging whether comments
  were obtained.
- **R3 — pointer failure branches lack direct tests.** `pointer_action_lookup_failed` and
  `pointer_action_click_failed` are correct by inspection but uncovered; adding two fake-engine tests
  is optional hardening, not required for merge.
- **R4 — survivability unproven (spec-level, unchanged).** Per the TikTok lane spec and recon index,
  detection ceiling / cross-creator coverage remain UNMEASURED. This review certifies code behavior
  only, not live capture safety or scale.

## Review-use boundary

This review is decision input only. It is not approval, validation, readiness, mandatory
remediation, implementation authorization, merge authority, or executor-ready patch authority until
separately accepted or authorized by the Orca owner / Chief Architect. No source files were edited;
only this report was written.
