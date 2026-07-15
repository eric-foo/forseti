# TikTok Grid Transcript Source Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  De-correlated adversarial code review of the bounded TikTok profile-grid
  transcript-source working-tree diff on the codex/tiktok-grid-transcript-source-20260715 lane.
use_when:
  - Adjudicating the returned findings for the TikTok grid transcript-source lane.
  - Checking what the delegated pass did and did not verify before closeout.
authority_boundary: retrieval_only
branch_or_commit: codex/tiktok-grid-transcript-source-20260715 at 3e24ff41e272e67f015e8ba47188f741ec23739a with the four dirty targets at their commissioned hashes
downstream_consumers:
  - Commissioning Chief Architect adjudicating findings before any keep or land step.
stale_if: >
  The lane HEAD, the allowed dirty-file set, or any target hash changes.
```

## Commission, target, authority, decision criteria

- **Commission**: `docs/prompts/reviews/tiktok_grid_transcript_source_adversarial_code_review_and_patch_prompt_v0.md`, target kind `delegated_code_review_and_patch`, access mode `repo`.
- **Exact target**: worktree `C:\tmp\orca-tt-grid-subs-20260715`, branch `codex/tiktok-grid-transcript-source-20260715`, HEAD `3e24ff41e272e67f015e8ba47188f741ec23739a`. All four target hashes were verified byte-identical to the manifest before source loading.
- **Authority**: patch-only on the four named targets; everything else read-only / flag-only. Review method is `workflow-code-review` (reference-loaded, then applied after source readiness). `workflow-deep-thinking` intentionally omitted per the commission.
- **Decision criteria**: the frozen behavior contract in the commission — exact-video binding, source precedence (overlay item metadata, then exact profile-grid item metadata, then matched overlay DOM track), loud rejection of a present unsupported URL, ephemeral raw subtitle URLs, distinct grid provenance, and no regression to direct-video behavior.

## Provenance

```yaml
reviewed_by: claude-opus-4.8
authored_by: openai_gpt5_codex
de_correlation_bar: cross_vendor_discovery
observed_vendor_receipt:
  author_vendor: OpenAI
  controller_vendor: Anthropic
  differ: true
  bar_satisfied: true
receiver_binding:
  receiver_class: external_direct_write
  binding_state: receiver_verified
  launch_checkout: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\tiktok-grid-adversarial-review-5af0c8
  effective_target_worktree: C:\tmp\orca-tt-grid-subs-20260715
  capability_proof: direct file write plus delete probe executed in the effective target worktree
  no_concurrent_writer_state: >
    No index.lock, MERGE_HEAD, REBASE_HEAD, CHERRY_PICK_HEAD, or BISECT_LOG present;
    dirty set byte-identical to the commissioned manifest at review start and unchanged at review end.
```

## Verdict

`issues_found` — three findings, all minor. No critical or major failure mode survived verification. **No patch hunks are proposed**; the reasoning for authoring no diff is recorded under each finding and in *Patch decision* below.

## Findings

### FINDING-1 — Direct-route subtitle provenance can assert a DOM track that was never matched

- **Severity**: minor. **Confidence**: high.
- **Location**: `forseti-harness/source_capture/tiktok/live_batch_probe.py:1707-1711` (new in this diff).
- **Evidence**: the diff replaces a constant `field_provenance["subtitles"]` value (`source_native_track_or_item_struct_when_available`) with a computed label. On the direct route the new ternary resolves to `matched_visible_video_dom_track` whenever `item_struct is None`, with no check that any DOM track exists. Executing the branch's exact expression against `_subtitle_source_from_dom_tracks({"subtitle_tracks": []})` yields provenance `matched_visible_video_dom_track` while the resolved source carries `subtitleInfos == []` — a receipt asserting a matched track where none was matched. The overlay route labels that identical state honestly as `no_source_native_subtitle_metadata` (`live_batch_probe.py:2391`), so the two routes describe the same real state differently.
- **Reachability (this is what holds severity at minor)**: the false branch is currently unreachable. `live_batch_probe.py:795-813` breaks the direct route with `missing_video_detail_hydration` when `item_struct is None`, and `live_batch_probe.py:870` already asserts `item_struct is not None` on that same path before the row is built. `_cadence_row_from_capture` has exactly one call site (`live_batch_probe.py:876`). The defect is therefore latent, not live.
- **Impact**: provenance-truth trap on a durable capture receipt. No functional or security impact today; a repo-wide search found no consumer of `field_provenance["subtitles"]` or `hydration.subtitle_metadata_source` outside the tests added by this diff. The trap activates if the direct route's hydration guard is ever relaxed the way the grid route's was.
- **minimum_closure_condition**: either the unreachable branch is removed so the direct-route label cannot be false, or it reports metadata presence truthfully as the overlay route already does.
- **next_authorized_action**: Chief Architect adjudication. Self-closable inside the commissioned scope in the adjudication turn.

### FINDING-2 — No single test proves the cold onboarding to deep-capture to parsed-WebVTT result

- **Severity**: minor. **Confidence**: medium.
- **Location**: `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py:697-712` and `:791-807`; `forseti-harness/tests/unit/test_tiktok_live_batch_probe.py:3092-3160`.
- **Evidence**: the onboarding test stubs `deep_capture_fn`, so it proves only that onboarding hands the correct sources dict to the deep-capture boundary. The probe test proves that such a dict produces a fetched URL and a parsed WebVTT cue. The objective's end-to-end claim is covered as two halves joined by a literal dict shape asserted on both sides, not by one test that drives onboarding through a real deep capture.
- **Impact**: the seam is genuinely covered — this is a coverage-shape observation, not a false-success test. Both halves assert real behavior and would fail on a one-sided contract change. Residual: a coordinated drift of both halves would escape.
- **minimum_closure_condition**: either an accepted rationale that the two-half seam proof is sufficient for this lane, or one test driving onboarding through a real `run_tiktok_live_batch_probe` deep capture to a parsed-WebVTT row.
- **next_authorized_action**: Chief Architect adjudication (accept as sufficient, or commission a seam test).

### FINDING-3 — Duplicate video ids across item_list pages silently first-win with no discard receipt

- **Severity**: minor. **Confidence**: low.
- **Location**: `forseti-harness/source_capture/tiktok/creator_onboarding.py:2296-2303`.
- **Evidence**: `sources.setdefault(video_id, ...)` keeps the first observed subtitle metadata for a video id. If the same video appears in two item_list responses or in both a response and the hydration payload with differing `subtitleInfos`, the later record is dropped with no receipt.
- **Impact**: deterministic and consistent with the incumbent convention — `_dedupe_metric_items` (`creator_onboarding.py:2353`) is also first-wins — so this is not novel behavior introduced by the diff. Low practical risk because subtitle metadata for one video id is not expected to vary within a single grid capture.
- **minimum_closure_condition**: accepted as consistent with the incumbent dedupe convention, or the discard is made visible.
- **next_authorized_action**: Chief Architect adjudication; likely accept as-is.

## considered_and_defended

- **Unsupported-host fallthrough** — probed directly: an overlay item struct carrying an unsupported-host URL wins precedence and is loudly rejected (`unsupported_subtitle_url_host_live_probe_v0`, `attempted: False`); a supported profile-grid URL is *not* silently substituted, and no fetch occurs. This is exactly the frozen contract.
- **Cross-video / cross-creator metadata reuse** — blocked four independent ways: the `video_id not in requested_video_ids` bind (`live_batch_probe.py:490`), source-id/key equality (`:486`), the overlay identity gate that requires `overlay_video_id == expected`, `final_url_video_id == expected`, and creator match, and breaks before any row is built (`:777`, `:2337-2343`), and the exact-key lookup at `:879`.
- **Permissive author check** (an item lacking `author` is accepted) — identical to the incumbent `_metric_items_from_payload` convention (`creator_onboarding.py:2376`), and defeated in practice by the exact video-id binding above.
- **Handle-case mismatch** — `creator_onboarding._normalize_handle` lowercases (`:2567`) and the observed `author_handle` is lowercased before comparison; no uppercase-handle drop path exists.
- **Raw signed-URL persistence** — the sources dict flows only into the deep-capture call (`creator_onboarding.py:779-831`) and is never written to an artifact; `_sanitize_subtitle_infos` reduces URLs to `url_present_but_redacted` (`live_batch_probe.py:2456`); the three new `ValueError` messages carry ids only, never URLs; the probe test asserts the URL is absent from the whole serialized result.
- **Endpoint provenance** — the grid capture is response-filtered by `response_url_predicate=is_tiktok_profile_item_list_url` (`creator_onboarding.py:1787`), so the `profile_grid_item_list_item_struct` label is truthful for the response path.
- **Public-call / recursion compatibility** — the cloakbrowser re-entry forwards the new keyword (`live_batch_probe.py:436-441`), and `DeepCaptureFn = Callable[..., dict[str, Any]]` (`creator_onboarding.py:500`) absorbs it without a signature break.
- **`item_struct_present` truth** — unchanged (`item_struct is not None`, `:1756`); grid metadata carries the distinct `profile_grid_item_list_item_struct` provenance, satisfying the contract's distinct-provenance requirement.
- **Direct-route validation drift** — `requested_video_ids` derives from URLs already normalized at `:452-454`, so `_video_id_from_tiktok_url` cannot raise a new error there.
- **`video_id` loop-variable shadowing** between the new validation loop (`:482`) and the capture loop (`:563`, `:611`) — the validation loop completes before the capture loop rebinds.
- **`dict(raw_source)` shallow copy** shares the nested `subtitleInfos` list with the caller — no mutation path exists on either side.
- **Precedence ordering under partial metadata** — probed: an overlay struct with metadata but no URL correctly yields to a profile-grid source that has one; with nothing anywhere, the honest `no_source_native_subtitle_metadata` label is returned.

## Patch decision

No diff is proposed. FINDING-1 is the only candidate whose fix would fit wholly inside the named targets, and it was deliberately not patched: the branch is provably unreachable through the public surface, so no same-check red-green proof is available for a fix, and a test pinning the branch would durably pin dead code. Under the commission's "patch only when cited evidence supports it", an unverifiable edit to unreachable code is not directly supported. The closure sits inside the adjudicator's own authority and scope.

## Validation evidence

Run from `C:\tmp\orca-tt-grid-subs-20260715\forseti-harness` unless noted.

| Gate | Result | Observed |
| --- | --- | --- |
| Focused TikTok files | GATE PASS | 103 passed, exit 0 |
| All TikTok unit tests | GATE PASS | 337 passed, exit 0, two pre-existing deprecation warnings |
| Complete harness suite | NOT RUN | The commission conditions this gate on "after any code patch"; no code patch was authored, so the condition did not fire. The author-observed baseline (3,287 passed, 7 skipped) stands unchallenged because the four targets are byte-unchanged. |
| `git diff --check` | GATE PASS | exit 0 |

Both executed gates match the author-observed baseline exactly, which is expected: this pass authored no edits. Passing gates are evidence that the reviewed diff does not fail them; they are not evidence that the diff is correct.

## Residual risks

- The controller authored no hunks in this pass, so the usual "delegate authored the patch" residual does not apply. The inverse residual does: FINDING-1 remains open in the working tree unless the adjudicator closes it.
- Gate 3 (complete harness suite) was not run by this pass. Any claim about the full suite rests on the author's pre-commission baseline, not on a controller observation.
- Review was bounded to the four named targets at one exact revision. Adjacent production source was read only to verify findings; defects wholly outside the named set would not have been reported as findings.
- The cross-vendor discovery bar is satisfied (OpenAI author, Anthropic controller), but a novel failure class shared across both vendors and absent from the attacked set is caught by neither this pass nor the author's own review. Bounded, named, not zero.
- Reachability for FINDING-1 was established by reading the single call site and its guards, not by an exhaustive dynamic proof.

## Review-use boundary

These findings, the verdict, and the residual risks are decision input only. They are not approval, not validation, not mandatory remediation, and not executor-ready patch authority, and they do not establish readiness or any keep/land authority. The commissioning Chief Architect adjudicates every finding as a claim before anything is kept or landed.
