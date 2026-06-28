# YouTube Watch Source Capture — Advisory Code Review v0 (PR #440)

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Advisory code review output for PR #440's YouTube watch metadata/comments SourceCapturePacket sync.
use_when:
  - Adjudicating the delegated adversarial code review findings for PR #440.
  - Checking the review evidence behind the YouTube watch source-capture remediation patch.
authority_boundary: retrieval_only
```

```yaml
review_artifact: YouTube watch metadata/comments SourceCapturePacket sync — advisory code review
commission_source: docs/prompts/reviews/youtube_watch_source_capture_adversarial_code_review_prompt_v0.md
review_lane: read-only workflow-code-review (adversarial posture), zero-config findings-only advisory
pr: 440
branch: codex/youtube-capture-spine-sync
implementation_commit: 0ad8b3478460f981ff12be8438007a3da55c4629
prompt_commit: 52249cd4 (adds the review prompt only; excluded from review target)
output_mode: filesystem-output
required_output_path: docs/review-outputs/youtube_watch_source_capture_advisory_code_review_v0.md
reviewed_by: Claude (Anthropic), Opus 4.8 — claude-opus-4-8
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery (reviewer lineage Anthropic != author lineage OpenAI/Codex)
same_vendor_rationale: not_applicable (cross-vendor; same-vendor sanity not claimed)
non_claims: [no formal verdict, no severity authority, no readiness/approval, no validation pass/fail authority,
             no patch queue, no executor-ready handoff, no runtime model recommendation, no transcript/Cleaning/Judgment claim]
```

## Review Frame

- **Commission**: read-only adversarial review of PR #440's YouTube watch-page metadata/comments
  Source Capture sync. The prompt routed from `workflow-delegated-review-patch` but explicitly
  downgraded to a read-only `workflow-code-review` commission: no patch execution, patch queue,
  formal verdict, readiness claim, or no-new-seam claim is authorized.
- **Source-loading mode**: zero-config findings-only advisory review. No overlay verdict vocabulary,
  patch-queue routing, or validation-gate authority was bound into this lane; those are named below
  as strict-only blockers. Findings are decision input only.
- **Trigger gate**: explicit `workflow-code-review` commission with a repo-visible implementation diff
  → PASS.
- **Output binding**: `filesystem-output` with a bound `required_output_path` (this file) → satisfied.
- **Excluded from target** (per prompt): this review prompt artifact, unrelated IG capture, shared
  IG/YT capture-core architecture, live YouTube probing, and transcript/Cleaning/Judgment/scheduler/
  dashboard/production-runtime claims.

## Source-Loading Declaration

`SOURCE_CONTEXT_READY` — with one non-material context-only gap noted.

All implementation targets and the load-bearing core context were read at the pinned worktree:
`youtube_watch_packet.py`, `run_source_capture_youtube_watch_packet.py`, `capture_youtube_v0.py`,
`shorts_scroll_capture_v0.py`, `behavioral_projection.py`, the four named test files,
`source_capture/models.py`, `source_capture/writer.py`, `source_capture/packet_assembly.py`, and the
PR #440 diff for every modified file. Context-only docs **not** fully read (not load-bearing for any
finding below; flagged as a not-proven boundary for the "implied-authority" axis):
`transcript/caption_packet.py`, `transcript/asr_packet.py`, `source_capture_playbook_v0.md`,
`capture_recon_index_v0.md`, and the full `orca_repo_map_v0.md` (only its PR diff hunk was read).

## Validation Run Status

`validation_run` — reran the dispatcher's focused command at the pinned worktree:

```
python -m pytest -p no:cacheprovider -q tests/unit/test_source_capture_youtube_watch_packet.py \
  tests/unit/test_youtube_capture_view_count.py tests/unit/test_youtube_behavioral_projection.py \
  tests/contract/test_capture_runner_lake_seam_coverage.py
```

Observed: **19 passed, exit code 0** (one contiguous progress run of 19 `.`). This matches the
dispatcher's observed `19 passed`. The suite passing does **not** exercise the state/parse helpers
attacked in F1/F2 (see F3); two findings are reproduced by standalone execution of the verbatim PR
code (F1, F2). The additional hook checks listed in the prompt were not rerun (`validation_not_run`
for those; out of scope for code correctness).

---

## Findings (ordered by materiality)

### F1 — `detect_video_state` misclassifies non-playable videos: `login_required` shadows `region_blocked` and the 200/player playable fallback

- **commissioned_target_and_purpose**: availability-state correctness — "distinguish removed/private/
  age/login/region/unknown from playable … without brittle phrase overreach" (review axis 2).
- **anchor**: `orca-harness/youtube_capture/capture_youtube_v0.py:268`–`286` (`detect_video_state`);
  the decisive line is the login branch `capture_youtube_v0.py:280`, evaluated before the region
  branch (`:282`) and the `status == 200 and player` playable fallback (`:284`).
- **implementation_evidence**: the function builds `probe = f"{_playability_reason(player)}\n{html[:200000]}".lower()`
  and checks ordered substrings. After the authoritative early return `if play_status == "OK"`, the
  next discriminators are raw substring tests against ~200k chars of served HTML. `"sign in" in probe
  or "login" in probe` is checked **before** the region test and before the 200/player playable
  fallback. Reproduced by running the verbatim logic:
  - region-blocked player (`playabilityStatus.reason = "Video not available in your country"`) with a
    logged-out masthead → returns `("login_required", …)`, **not** `region_blocked`.
  - empty player (parse miss) + HTTP 200 + masthead → returns `login_required`, never reaching the
    `status == 200 and player` playable fallback.
- **authority_or_evidence_basis**: source + standalone repro of the PR's own code. The persisted
  `availability.video_state` is carried into the packet's slice limitations
  (`youtube_watch_packet.py:273`, `video_availability_state:{state}`) and `visible_mode_changes`
  (`youtube_watch_packet.py:201`, `video={video_state}`), so a misclassification is durably recorded.
- **impact** (correctness, review-confidence): for any video whose `playabilityStatus.status != "OK"`
  (genuinely unavailable videos, or a playable video whose `ytInitialPlayerResponse` failed to parse),
  the availability *state value* — not merely its reason string — is unreliable: `region_blocked` is
  effectively unreachable and the case collapses to `login_required`. The common playable case
  (`status == "OK"`) is unaffected, so this is a sub-classification defect on the not-playable branch,
  but it directly undercuts the PR's stated goal of trustworthy availability states.
- **not_proven boundary**: that real logged-out watch HTML *always* contains `"sign in"`/`"login"`
  within the first 200k chars is a well-grounded assumption (logged-out chrome renders a "Sign in"
  button; `"login"` appears as a substring of common config keys such as `"loginRequired"`) but is
  **not proven here** against a live body — no live probe is authorized. The ordering/shadowing defect
  itself is proven for any probe containing those substrings.
- **minimum_closure_condition**: state detection no longer lets generic chrome strings outrank specific
  signals — e.g. gate the `"sign in"/"login"` test on the authoritative `playabilityStatus` or the
  consent-redirect (`final_url`) rather than raw HTML substrings, restore reachability of
  `region_blocked` and the 200/player fallback, and prove it with fixtures for each non-OK state.
- **next_authorized_action**: report only (advisory). Remediation is owner/implementer-routed; this
  lane is read-only.
- **verification_expectation**: a same-check red-green proof is available cheaply — add fixture-HTML
  unit tests asserting `detect_video_state` returns `region_blocked` / `private` / `removed_by_uploader`
  / `age_restricted` for representative non-OK bodies that also contain masthead "Sign in"; they fail
  against current code and pass after the ordering fix.
- **patch_queue_entry authorized**: no.

### F2 — `parse_exact_count_text` converts abbreviated/decimal presentation text into a wrong exact `total_comment_count`

- **commissioned_target_and_purpose**: metric-receipt honesty — "avoid converting approximate or
  presentation text into exact counts" (review axis 3); `total_comment_count` is a source-native
  momentum metric.
- **anchor**: `orca-harness/youtube_capture/capture_youtube_v0.py:247`–`253` (`parse_exact_count_text`);
  consumed at `capture_youtube_v0.py:415`–`420`, which sets `engagement.total_comment_count` and then
  an `observed` metric receipt at `:445`–`450`.
- **implementation_evidence**: the regex `(?<![\d.])(\d[\d,]*)\s*(?:comments?|likes?|views?)?\b` matches
  a leading digit run but stops at a decimal point, so a `K/M/B`-abbreviated `countText` yields a
  truncated integer rather than `None`. Reproduced on the verbatim code:
  - `"1,234 Comments"` → `1234`, `"1,234,567 comments"` → `1234567` (correct, exact comma forms)
  - `"12K comments"` → `None` (correctly rejected)
  - `"1.2K comments"` → **`1`**, `"1.2K"` → **`1`**, `"2.5M views"` → **`2`** (wrong)
  When `countText` is abbreviated, `total_comment_count` is set to the bogus value and a
  `posture: "observed"` receipt with `source_path = youtubei_next.commentsHeaderRenderer.countText` is
  written — a fabricated exact count presented as observed.
- **authority_or_evidence_basis**: source + standalone repro; `source_capture/models.py:128`–`136` and
  `:183`–`198` name "absence / … never stored as an observed value" as the single irreversible,
  un-re-capturable lock-in, and storing rounded presentation text as an exact observed value is the
  same failure class.
- **impact** (correctness, latent): if `commentsHeaderRenderer.countText` is ever abbreviated, the
  packet records a silently-wrong exact momentum metric. Trigger probability is **low** for the
  current call shape — the youtubei request pins `hl=en, gl=US` WEB, where the comments header count
  is normally exact-with-separators — but the consequence class is exactly the named lock-in, and the
  guard is cheap.
- **minimum_closure_condition**: `parse_exact_count_text` rejects any value carrying a magnitude suffix
  (`K/M/B`) or decimal point (return `None` → fall through to `unavailable_with_reason`), so only a
  source-native exact integer becomes `total_comment_count`.
- **next_authorized_action**: report only (advisory).
- **verification_expectation**: same-check red-green — a unit test asserting
  `parse_exact_count_text("1.2K comments") is None` fails today and passes after the suffix/decimal
  guard; keep the exact-comma cases passing.
- **patch_queue_entry authorized**: no.

### F3 — The new availability/comment-state and count-parsing helpers have no unit coverage; the passing suite gives false confidence on the trust surface

- **commissioned_target_and_purpose**: "tests prove the load-bearing behavior" (review axis 8) and
  review confidence in the availability/metric honesty the PR claims.
- **anchor**: absence of any test reference to `detect_video_state`, `comments_disabled_signal`,
  `parse_exact_count_text`, `extract_like_count`/`player_like_count` (grep across
  `orca-harness/**` returns matches only in `capture_youtube_v0.py` and `shorts_scroll_capture_v0.py`,
  none under `tests/`). The watch-packet tests
  (`tests/unit/test_source_capture_youtube_watch_packet.py:63`–`68`) hard-code
  `availability.video_state = "playable"` and fixture comment states, so the state classifier and the
  count parser are never executed under test.
- **implementation_evidence**: `fetch_youtube_watch` (network) is not unit-tested; the writer/runner/
  projection tests inject fixtures with pre-decided states. F1 and F2 — both reproducible from source —
  pass the suite untouched, demonstrating the gap concretely.
- **authority_or_evidence_basis**: grep evidence + the green suite (19 passed) standing alongside two
  source-proven defects.
- **impact** (review-confidence, validation): the brittle, correctness-critical logic that produces the
  packet's availability and momentum receipts is exactly the part with no direct test; "19 passed" does
  not bound the honesty claims the PR rests on.
- **minimum_closure_condition**: network-free unit tests over fixture HTML / youtubei JSON for each
  `VIDEO_AVAILABILITY_STATES` value, each `COMMENT_AVAILABILITY_STATES` branch
  (`comments_disabled` vs `comments_not_exposed` vs `comments_sample_captured` vs api-key-missing),
  `comments_disabled_signal`, `parse_exact_count_text`, and `extract_like_count` present-vs-absent.
- **next_authorized_action**: report only (advisory).
- **verification_expectation**: the F1/F2 fixtures double as the start of this coverage; red-green as
  described in F1/F2.
- **patch_queue_entry authorized**: no.

### F4 — Shorts summary stat `captured_with_comments` is wired to a stale posture key and now always reports 0

- **commissioned_target_and_purpose**: "Shorts posture changes improve honesty without regressing
  existing … extraction" (review axis 7).
- **anchor**: `orca-harness/youtube_capture/shorts_scroll_capture_v0.py:110`
  (`"captured_with_comments": postures.get("captured", 0)`), against the posture vocabulary changed at
  `:58` and `:68` to `comments_sample_captured` / `comments_not_exposed` / `comments_disabled`.
- **implementation_evidence**: PR #440 renamed the Shorts comment postures from `"captured"`/`"empty"`/
  `"disabled"` to the new `comments_*` vocabulary (diff hunk at `shorts_scroll_capture_v0.py:49`–`69`),
  but the run summary still counts `postures.get("captured", 0)`. `"captured"` is no longer an emitted
  posture, so `captured_with_comments` is now structurally `0` on every run.
- **authority_or_evidence_basis**: source + diff. (Per-row comment sample extraction itself is **not**
  regressed — `comment_sample_count` and `comments` rows are still captured; only the rollup stat is
  stale.)
- **impact** (correctness, low materiality): a silently-wrong `0` in the volume/stress-run summary
  telemetry; not part of any SourceCapturePacket, so trust impact is confined to operator-facing
  Shorts-scroll run reports.
- **minimum_closure_condition**: count `postures.get("comments_sample_captured", 0)` (or derive from
  `comment_sample_count > 0`).
- **next_authorized_action**: report only (advisory).
- **verification_expectation**: a small test over a synthetic `rows` list asserting the summary counts
  sample-captured rows; red-green against the stale key.
- **patch_queue_entry authorized**: no.

---

## Risks / Residual Observations (not findings — lower confidence or pre-existing)

- **R1 — regex-first `viewCount` can attribute another video's count as `observed`/exact.**
  `extract_view_count`'s fallback `first(r'"viewCount":"([0-9]+)"', html, int)`
  (`capture_youtube_v0.py:190`) returns the first `viewCount` in the served HTML, which may belong to a
  recommended/related video, yet it is recorded as `posture: observed`. Mitigations: it is reached
  only when the player path yields nothing, and the receipt honestly labels `source_route =
  served_html.regex`. Pre-existing (incumbent extraction); flagged because the new receipt layer now
  stamps it `observed`.
- **R2 — `comment_sample_count = observed: 0` co-exists with `comments_state = comments_not_exposed`
  in the reachable-but-empty branch.** When a continuation token + api key resolve but no
  `commentEntityPayload` rows are found, `capture_youtube_v0.py:440`–`444` writes an `observed` receipt
  with value `0` while the state is `comments_not_exposed` (`:431`–`439`). Defensible as "we sampled
  and observed zero rows" (a capture artifact, not a source momentum metric), and the slice still
  carries a `comments_state:comments_not_exposed` limitation — but the observed-0 vs not-exposed pairing
  is a mixed signal a downstream reader could misread. Worth an explicit decision; not asserted as a
  no-zero-fill violation.
- **R3 — `extract_like_count` reads only `microformat.playerMicroformatRenderer.likeCount`, which is
  rarely populated for logged-out WEB.** Result: `like_count` will almost always be
  `unavailable_with_reason`, with the abbreviated `like_count_text` preserved separately. This is
  honest (no zero-fill) and arguably a strength, but the "exact like count" route is largely inert in
  practice — useful to know when reasoning about coverage.
- **R4 — `--comment-pages > 99` aborts the packet write.** Page filenames are
  `youtubei_next_page_{n:02d}.json` and `_validate_comment_page` requires exactly two digits
  (`youtube_watch_packet.py:304`), so a 100th page raises `ValueError`. Edge only (default 2, bounded).
- **R5 — legacy `capture()` now also writes `youtubei_next_page_*.json` to `./packets/<vid>/`.**
  A new disk side-effect versus the incumbent legacy path (which wrote only `raw_watch.html` +
  `packet.json`). Benign (captured data is gitignored), noted for the "preserve incumbent behavior"
  axis as an additive, not silent-semantic, change.

## Strict-Only Blockers and Not-Proven Boundaries

- No overlay review-lane id, verdict vocabulary, severity taxonomy, validation-gate semantics, or
  patch-queue routing was bound into this lane → strict formal review, formal verdict, severity
  authority, and any pass/fail or readiness claim are **blocked / not authorized** (by prompt design).
- "Live YouTube HTML always contains `sign in`/`login`" (F1) is **not proven** here — no live probe.
- The "implied-authority" axis (no unauthorized transcript/Cleaning/Judgment claim) is assessed only
  from code: the code is clean on this — `YOUTUBE_WATCH_NON_CLAIMS` (`youtube_watch_packet.py:40`–`52`),
  the writer's `NON_CLAIMS`, and the projection docstring ("deliberately does not acquire anything")
  explicitly disclaim those lanes. **Not proven** against the unread `source_capture_playbook_v0.md` /
  `capture_recon_index_v0.md`, so a doctrine-level overclaim beyond the code's explicit non-claims is
  neither confirmed nor refuted.

## Open Questions

1. Does `commentsHeaderRenderer.countText` on the pinned `hl=en, gl=US` WEB youtubei route ever return
   an abbreviated form? This sets F2's real-world trigger rate (latent vs active).
2. Is `comment_sample_count = observed: 0` the intended reading for reachable-but-empty comment
   captures, or should that case be `unavailable_with_reason`? (R2 decision.)
3. Is the legacy `capture()` writing comment-page JSON to `./packets/` intended, or an incidental
   coupling from sharing `fetch_youtube_watch`? (R5.)

## Residual Risk

The packet writer, runner lake seam, sample-vs-total separation, no-zero-fill discipline for `like_count`
/ `total_comment_count`, preserved-file referencing, and projection carry-through are correct and
genuinely covered by the 19-test suite. The residual risk concentrates in the **upstream extraction
layer** (`capture_youtube_v0.py`): availability sub-state classification (F1) and exact-count parsing
(F2) are brittle and untested (F3), so the packet can faithfully preserve an upstream-wrong availability
state or — under abbreviated count text — a fabricated exact `total_comment_count`. None of these block
owner review; they bound how far "trustworthy" currently extends.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, readiness, mandatory
remediation, or executor-ready patch authority, and they confer no severity or runtime-model authority,
until separately accepted or authorized by the owning lane. `patch_queue_entry` is `no` for every
finding in this prompt.

## Source-Read Ledger

| Source | Path | Mode |
| --- | --- | --- |
| Packet writer | `orca-harness/source_capture/youtube_watch_packet.py` | full |
| Runner | `orca-harness/runners/run_source_capture_youtube_watch_packet.py` | full |
| Live fetcher | `orca-harness/youtube_capture/capture_youtube_v0.py` | full + PR diff |
| Shorts volume capture | `orca-harness/youtube_capture/shorts_scroll_capture_v0.py` | full + PR diff |
| Behavioral projection | `orca-harness/youtube_capture/behavioral_projection.py` | full + PR diff |
| Watch packet tests | `orca-harness/tests/unit/test_source_capture_youtube_watch_packet.py` | full |
| View-count tests | `orca-harness/tests/unit/test_youtube_capture_view_count.py` | full |
| Projection tests | `orca-harness/tests/unit/test_youtube_behavioral_projection.py` | full |
| Lake-seam contract test | `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | full |
| Packet models | `orca-harness/source_capture/models.py` | full (context) |
| Local packet writer | `orca-harness/source_capture/writer.py` | full (context) |
| Stage/assemble helper | `orca-harness/source_capture/packet_assembly.py` | full (context) |
| PR diff | commit `0ad8b347` (all 8 changed files) | full |
| Repo map | `docs/workflows/orca_repo_map_v0.md` | PR hunk only |
| Transcript packets, playbook, recon index | (context-only) | not read (non-material; see not-proven) |

Evidence captured this pass: standalone repro of F1/F2 from verbatim PR code; grep confirming F3/F4;
focused pytest rerun = 19 passed (exit 0).

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- original commission or review target: read-only adversarial code review of PR #440 (YouTube watch
  metadata/comments SourceCapturePacket sync); target = the implementation + tests listed in the
  commissioning prompt; this prompt downgraded delegated-review-patch to read-only workflow-code-review
  (no patch execution/queue/verdict/readiness authorized).
- implementation context, diff, and reviewed files: branch codex/youtube-capture-spine-sync,
  implementation commit 0ad8b3478460f981ff12be8438007a3da55c4629 (8 files, +978/-20). Reviewed the new
  packet writer + runner, the heavily-extended live fetcher (capture_youtube_v0.py: +315), the Shorts
  capture change, the projection passthrough, the four named tests, and core context
  (models.py/writer.py/packet_assembly.py).
- findings and implementation evidence:
  - F1 (highest): detect_video_state (capture_youtube_v0.py:268-286) — the "sign in"/"login" branch at
    :280 shadows the region branch (:282) and the status==200/player playable fallback (:284). Repro:
    a region-blocked player + logged-out masthead returns login_required, not region_blocked. Persisted
    into the packet's availability state, slice limitations, and visible_mode_changes. Scope: non-OK
    videos only (status=="OK" returns playable early).
  - F2: parse_exact_count_text (:247-253) emits a truncated integer for abbreviated/decimal countText —
    "1.2K comments" -> 1, "2.5M views" -> 2 (repro) — written as an observed exact total_comment_count
    (:445-450). Latent (en/US WEB countText is usually exact-with-commas); consequence class = the
    irreversible observed-value lock-in named in models.py:128-136.
  - F3: detect_video_state / comments_disabled_signal / parse_exact_count_text / extract_like_count have
    no test references (grep); the 19-passed suite hard-codes availability/comment states, so it does
    not bound the PR's honesty claims.
  - F4: shorts_scroll_capture_v0.py:110 counts a stale posture key (postures.get("captured",0)) after
    the vocabulary moved to comments_sample_captured — captured_with_comments is now always 0.
  - Risks R1-R5 (regex-first viewCount as observed; observed-0 sample_count vs not_exposed state;
    inert microformat.likeCount route; >99 comment-pages filename abort; legacy capture() new disk
    side-effect).
- proposed patch, diff, or exact requested edits: NOT_CLAIMED (read-only commission).
- citations: file:line anchors above; standalone repro of F1/F2 from verbatim PR code; grep for F3/F4.
- reviewer verdict: NOT_CLAIMED as a formal verdict. Advisory read: the packet/runner/projection layer
  is correct and well-tested; residual trust risk is concentrated in the untested upstream extraction
  layer (F1/F2 amplified by F3). None blocks owner review.
- validation evidence and not-run checks: focused pytest rerun = 19 passed, exit 0 (matches dispatcher).
  Hook checks from the prompt not rerun (validation_not_run). No live YouTube probe (not authorized).
- residual risk: a faithfully-preserved but upstream-wrong availability state, or a fabricated exact
  total_comment_count under abbreviated count text.
- blockers, off-scope flags, and not-proven boundaries: no overlay verdict/severity/patch-queue lane
  bound (strict claims blocked by design); "live HTML always contains sign in/login" not proven without
  a probe; implied-authority axis assessed from code only (clean), not proven against the unread
  capture playbook / recon index.
- provenance: reviewed_by Claude (Anthropic) Opus 4.8; authored_by OpenAI/Codex GPT-5;
  de_correlation_bar cross_vendor_discovery; same_vendor_rationale not_applicable.
```

For this prompt, `proposed patch`, `diff`, `exact requested edits`, formal verdict, severity authority,
readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner
instruction binds them.
