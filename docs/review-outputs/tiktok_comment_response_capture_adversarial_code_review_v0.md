# TikTok Comment Response Capture Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (adversarial code review, read-only)
scope: >
  De-correlated read-only adversarial code review of PR #559 (TikTok live comment
  response capture hardening) at head f8a30acccaa61b18c144872d8fe28191cfeaa84b.
use_when:
  - Deciding whether PR #559 is safe, scoped, and honestly claimed before merge.
  - Checking the comment-response metadata + page-owned filter change and its tests.
authority_boundary: retrieval_only
stale_if:
  - PR #559 head commit changes.
  - Any target source/test file changes after f8a30acccaa61b18c144872d8fe28191cfeaa84b.
```

## Provenance

- `reviewed_by`: claude-fable-5 (Anthropic / Claude lineage)
- `authored_by`: OpenAI/GPT-family Codex
- `de_correlation_bar`: cross_vendor_discovery
- controller lineage vs. author lineage: cross-vendor (Anthropic reviewing OpenAI-authored patch) — discovery bar satisfied.
- commission prompt: `docs/prompts/reviews/tiktok_comment_response_capture_adversarial_code_review_prompt_v0.md`
- target: PR https://github.com/eric-foo/orca/pull/559, branch `codex/tiktok-comment-body-capture-probe`, head `f8a30acccaa61b18c144872d8fe28191cfeaa84b`
- verdict: `SAFE_TO_MERGE_AFTER_GREEN` (advisory; decision input only, not approval/validation/merge authority)

## Confirm-Do-Not-Trust load contract (verified from repo)

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| `git rev-parse HEAD` | `f8a30acc...eaa84b` | `f8a30acccaa61b18c144872d8fe28191cfeaa84b` | MATCH |
| branch | `codex/tiktok-comment-body-capture-probe` | `codex/tiktok-comment-body-capture-probe` (tracking `origin/...`) | MATCH |
| dirty state | prompt/report docs may be dirty; target files clean | only untracked `docs/prompts/reviews/...prompt_v0.md`; four target files unmodified | MATCH |
| diff `0b17593a..HEAD` | exactly the four files | browser_snapshot.py, live_batch_probe.py, test_source_capture_browser_snapshot.py, test_tiktok_live_batch_probe.py | MATCH |

Target scope and base match the prompt; no `BLOCKED_TARGET_MISMATCH`.

## Source-read ledger

| Source | Why read | Supports |
| --- | --- | --- |
| `AGENTS.md`, `.agents/workflow-overlay/README.md`, `source-loading.md`, `review-lanes.md`, `validation-gates.md`, `prompt-orchestration.md` | Authority/lane/gate bindings | Findings-first, read-only lane, provenance fields, de-correlation bar |
| `source_capture_playbook_v0.md`, `capture_recon_index_v0.md`, `tiktok_capture_lane_spec_v0.md` | Capture doctrine + lane invariants (C1–C8', secret hygiene, footprint cap) | Checks 3/5/6/9; footprint finding |
| `orca-harness/source_capture/adapters/browser_snapshot.py:97-113,960-1023,645-800` | `BrowserPageResponse` fields; `_response_request_metadata`; response collection + post-load ordering | Checks 1/2/5 |
| `orca-harness/source_capture/tiktok/live_batch_probe.py` (full) | Filter, telemetry, receipts, challenge-stop | Checks 3/4/5/6/7 |
| `orca-harness/source_capture/tiktok/admission.py` (full), `batch_packet.py` (full) | Downstream consumption / schema compatibility | Check 9 |
| `orca-harness/tests/unit/test_source_capture_browser_snapshot.py:103-121,821-834`; `test_tiktok_live_batch_probe.py:1-246,377-390` | Test red-green + live-dependency | Check 8 |
| `C:\tmp\orca-tiktok-live-smoke-output\tiktok_control_patch_probe_20260702T000000Z\tiktok_live_cadence_result.json`; `...patch_probe_wait_...\tiktok_live_cadence_result.json` | Verify claimed runtime evidence | Check 7; residual risk |
| smoke-output tree (sensitive-marker scan) | Verify no-leak claim | Check 1; secret hygiene |

`SOURCE_CONTEXT_READY` was declared before applying `workflow-deep-thinking` and `workflow-code-review`.

## Method status

- `workflow-deep-thinking`: REFERENCE-LOADED, then APPLIED after source readiness to frame highest-risk failure modes (secret leak via new fields; over-broad capture; over-restrictive filter dropping legit responses; false-success signal; live-capture overclaim; metadata-extraction robustness; footprint/human-rate).
- `workflow-code-review`: REFERENCE-LOADED, then APPLIED as zero-config findings-only advisory review against repo-visible evidence. No formal overlay verdict, severity-taxonomy authority, patch queue, or executor handoff is asserted.

## Findings (severity-ordered)

No `critical` and no `major` findings. The metadata fields carry no secret-bearing content, the new page-owned filter is strictly more selective than the prior URL-only match while remaining backward-compatible, and no false-success path was found. Three `minor` advisory items follow.

### MINOR-1 — Per-video comment-response footprint (lane C3 ≈3-request / ≤1-pagination cap) is not enforced in code
- **Location**: `orca-harness/source_capture/tiktok/live_batch_probe.py:398-402` (`comment_responses` list comprehension) and `:214` (single `post_load_action_script` click; no pagination/scroll).
- **Issue**: `comment_responses` admits *every* collected response passing `_is_page_owned_comment_list_response`. Collection dedups only by `(url, status)` (`browser_snapshot.py:970-973`); a second comment page has a different `cursor` query → different URL → not deduped. If the page auto-loads more than one `/api/comment/list` page during the fixed 2500 ms post-load wait, multiple responses are admitted and `matched_comment_response_count` grows accordingly.
- **Evidence/basis**: lane spec C3 ("Hard cap ≈ 3 page-emitted requests per video … first page + at most ONE pagination") in `tiktok_capture_lane_spec_v0.md`; code enforces the cap only implicitly (one click, no explicit response cap).
- **Impact**: bounded over-capture vs. the intended footprint; potential mild detectability/scope drift. Not a correctness or secret-safety defect — downstream `_best_comment_response` still selects one response per video, and body size is capped at `max_response_bytes` (5 MB) with omission-on-exceed.
- **minimum_closure_condition**: either an explicit cap on admitted `/api/comment/list` responses per video (≤2), or a recorded owner decision that the single-click/no-pagination shape already satisfies C3 for this first live staging producer.
- **next_authorized_action**: owner decision (accept as-designed vs. queue a follow-up hardening patch in the authoring lane). No patch requested by this read-only review.

### MINOR-2 — `_response_request_metadata` failure branches are untested
- **Location**: `orca-harness/source_capture/adapters/browser_snapshot.py:1010-1023`; test only at `test_source_capture_browser_snapshot.py:828-833` (happy path).
- **Issue**: the three defensive `try/except` branches (missing `.request`, `.method`/`.resource_type` raising or empty) have no test exercising them; only `method="GET"/resource_type="fetch"` is covered.
- **Evidence/basis**: `_FakeObservationRequest` always supplies both attributes (`test_source_capture_browser_snapshot.py:106-110`); no fake omits `.request` or raises.
- **Impact**: review-confidence only. The defensive code is correct on inspection (each failure returns `None` and never drops the response, preserving body collection), but the "does not mask page-response collection" guarantee is asserted by reading, not by a regression test.
- **minimum_closure_condition**: a unit case with a response object lacking `.request` (or whose `.request` raises) asserting `(None, None)` and that the response is still preserved with its `body_text`.
- **next_authorized_action**: optional test-hardening in the authoring lane; non-blocking.

### MINOR-3 — Fixed 2500 ms post-load wait is a magic constant decoupled from configured timing, and live comment capture is unproven
- **Location**: `orca-harness/source_capture/tiktok/live_batch_probe.py:43-64` (`TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT`, `await sleep(2500)`).
- **Issue**: the wait that gives the page time to emit `/api/comment/list` after the click is a hardcoded 2500 ms, unrelated to `settle_seconds`/`timeout_seconds`. In the one live control run made under this patched code, that window produced `response_count=0` / `matched_comment_response_count=0` — i.e., zero comment responses captured (see Runtime evidence).
- **Evidence/basis**: `tiktok_control_patch_probe_20260702T000000Z/tiktok_live_cadence_result.json` (`response_count: 0`, `comment_responses: []`, `completed_count: 1`).
- **Impact**: the patch's *new* capability (capturing comment-list responses) is exercised only by fake-engine tests with injected responses; it is not demonstrated live. This is a claim-scope caveat, not a code defect.
- **minimum_closure_condition**: an owner-gated live run that actually captures ≥1 real page-owned comment-list response, before any "comment capture works" claim is made; the wait may then be tuned/derived rather than fixed.
- **next_authorized_action**: keep the PR's honest scope (plumbing + metadata/filter + first live staging producer); do not upgrade to a comment-capture-proven claim. No patch requested.

## Explicit answers to the Review Checks

1. **Do `request_method`/`resource_type` leak secrets?** No. `_response_request_metadata` (`browser_snapshot.py:1010-1023`) reads only `request.method` (HTTP verb, upper-cased) and `request.resource_type` (Playwright resource-type enum, lower-cased). Neither can carry headers, cookies, URLs, storage paths, proxy data, or auth state. Existing header sanitization (drop `set-cookie`/`cookie`, `:974-978`) is preserved. Independent sensitive-marker scan over the smoke-output tree returned no matches.
2. **Is `_response_request_metadata` robust without masking response collection?** Yes. Every access is wrapped; any failure yields `None`, and the function is called inside `_read_observed_page_responses` (`:979`) *before* the body read, so a metadata failure never drops or truncates a response — the response is still preserved with `body_text`. (Robustness verified by inspection; failure branches untested — MINOR-2.)
3. **Does the `/api/comment/list` filter correctly select page-owned responses and exclude OPTIONS/preflight, unrelated APIs, HTML, pixels, beacons, third-party?** Yes. `is_tiktok_comment_list_url` (`live_batch_probe.py:337-344`) requires scheme http(s), host `tiktok.com` or `*.tiktok.com` (rejects `tiktok.com.evil.com`), and exact path `/api/comment/list` after trailing-slash strip (excludes `/api/comment/list/reply`, unrelated APIs, HTML, pixels). `_is_page_owned_comment_list_response` (`:439-448`) then rejects non-GET (drops OPTIONS/preflight) and non-`fetch`/`xhr` resource types (drops `document`/navigation, `preflight`, beacons) when metadata is present.
4. **Does it avoid dropping legitimate responses when metadata is unavailable?** Yes. Both guards are `if <value> and <value> not allowed` — when `request_method`/`resource_type` is `None` (older adapters, tests without metadata), the empty-string is falsy and the guard is skipped, so URL match alone governs. Backward-compatible.
5. **Is the async comment-open post-load script safe under lane constraints?** Mostly. It performs one click on a comment-labelled control, records sanitized `{candidate_count, clicked}` telemetry to `window.__orcaTikTokCommentAction`, waits 2500 ms, and returns; no secret persistence, no raw UI text persistence. `page.evaluate` awaits the async function, so the wait elapses before responses are read (`browser_snapshot.py:742-760`). Stop-on-challenge is preserved and independent of this script (`detect_tiktok_challenge` on `final_url`/`title`/`visible_text`, `live_batch_probe.py:241-253,347-357`); the empty/stripped-shell path also stops (`:255-273`). Caveats: no explicit per-video request cap (MINOR-1) and a fixed magic wait (MINOR-3).
6. **Does `comment_action` telemetry stay sanitized and non-misleading?** Yes. `_comment_action_summary` (`:428-437`) emits only `candidate_count` (int) and `clicked` (bool) via `_drop_none`; no raw text. `clicked: true` only asserts a matching button was clicked, not that comments were captured. The real signal (`matched_comment_response_count`) is computed separately from the filtered list, so telemetry cannot manufacture a success signal.
7. **Does the live evidence support only the narrow plumbing/challenge-stop claim, not real comment capture?** Yes — and this is the key caveat. Verified artifacts: the patched control run captured video/grid metadata + subtitle metadata and wrote admission-compatible staging with `response_count=0`, `matched_comment_response_count=0`, `comment_responses=[]`, `completed_count=1`, `challenge_count=0`; the wait-variant run stopped on `platform_challenge_observed` with `completed_count=0`, `challenge_count=1`, `results=[]`. No 3–5 creator micro-batch ran (stop-on-challenge). So the evidence supports "zero-response staging/admission plumbing works and challenge-stop fires" only; it does **not** establish live comment capture (MINOR-3).
8. **Do the tests fail under old behavior and exercise new behavior without live deps?** Yes, using a fake engine (no browser/network). `test_live_probe_filters_non_get_comment_list_responses_when_method_available` injects an OPTIONS + a GET response and asserts `response_count==2`, `matched_comment_response_count==1`, `len(comment_responses)==1`; under the old URL-only filter both would pass, so `len==1` fails pre-patch — a proper regression (red-green reasoned, not executed, since the read-only lane does not revert source). `test_read_observed_page_responses_omits_cookie_headers` now asserts `request_method=="GET"`/`resource_type=="fetch"`, which have no pre-patch fields. Gap: the OPTIONS body is empty, so the filter — not body content — is what the regression pins (adequate); metadata-failure branches remain untested (MINOR-2).
9. **Does the patch break prior TikTok batch behavior / packet schema / summaries?** No. The two new fields are additive to `BrowserPageResponse` (defaulted `None`) and to `comment_responses`/`capture_receipt` staging. `batch_packet.py` consumers (`_normalize_comment`, `_normalize_comments`, `_best_comment_response`, `_validate_staging_contracts`, `_summarize_contracts`) do not read `request_method`/`resource_type`/`comment_action`; `capture_contract` keys are unchanged. Confirmed by 70/70 offline tests including batch admission/coverage/projection/video-admission, and by `orca-harness-tests` passing on CI.
10. **Any design-level issue warranting `NEEDS_ARCHITECTURE_PASS`?** No. All observations are localized to the reviewed diff; MINOR-1/2/3 are bounded hardening or claim-scope items, not doctrine or architecture changes.

## Validation commands and observed outputs

| Command | Result |
| --- | --- |
| `python -m compileall -q <4 target files>` | exit 0 (run) |
| `python -m pytest -q <admission/coverage/projection/video/live_batch_probe/browser_snapshot>` | 70 selected, all passed (`[100%]`), exit 0 (run) |
| `git diff --check` | exit 0, no whitespace errors (run) |
| `gh pr checks 559` | `orca-harness-tests  pass  1m32s` (run) |
| sensitive-marker scan over `C:\tmp\orca-tiktok-live-smoke-output` | No matches (run) |

## Residual risks

- **Live comment capture unproven** (MINOR-3): the patched live control run captured zero comment responses; only fake-injected responses exercise the parse/filter path. Do not read admission-compatibility or challenge-stop as evidence that real comment bodies are captured.
- **Footprint not code-capped** (MINOR-1): admitted `/api/comment/list` responses per video are unbounded in count (body size is capped); relies on single-click/no-pagination behavior to honor lane C3.
- **Selector heuristic brittleness** (out-of-diff-adjacent): the comment-open click targets any button/link whose text contains "comment(s)"; a mislabeled or localized control may not open comments (would surface as `clicked:false`/`response_count:0`, i.e., fail-visible, not fail-silent). Noted, not a finding.
- **Detection ceiling remains UNMEASURED** per the lane spec; nothing in this patch changes that, and this review does not measure it.

## Review-use boundary

This review is decision input only. It is not approval, validation, readiness, mandatory remediation, implementation authorization, merge authority, or executor-ready patch authority until separately accepted or authorized by the Orca owner / Chief Architect. No source files were edited; only this report was written.
