# YouTube RSS Monitor Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: delegated_review_report
scope: >
  Delegated adversarial code review-and-patch return for the YT tier-1 RSS
  daily-monitor lane (PR #613, reviewed head ffeeb131): three major findings
  (channel-identity gate, fail-closed prior state, retrieval-time latest-prior
  selection), all patched within the commissioned target set and adjudicated
  by the commissioning CA (all accepted; adjudication recorded on the lane PR).
use_when:
  - Checking what the delegated review of the RSS monitor found, patched, and
    left as accepted residuals.
  - Auditing the lane's review-routing disposition evidence.
stale_if:
  - The RSS monitor runner's identity, prior-state, or latest-prior semantics
    are materially changed by a later lane.
authority_boundary: retrieval_only
```

```yaml
reviewed_by: OpenAI GPT-5 Codex
authored_by: Anthropic Claude (Claude Code lane)
reviewed_head_sha: ffeeb13179a72e4aacafb69267d9e6fa7c2d261a
review_mode: delegated_code_review_and_patch
commission_source: docs/prompts/reviews/youtube_rss_monitor_delegated_adversarial_code_review_patch_prompt_v0.md
source_context_state: SOURCE_CONTEXT_INCOMPLETE
patch_state: working_tree_uncommitted
validation_command: python -m pytest
validation_result: 2479 passed, 7 skipped, 1 warning
formal_pass_claim: none
```

## Source Context

SOURCE_CONTEXT_INCOMPLETE.

Loaded target set:

- [rss-parser] `orca-harness/source_capture/youtube_channel_rss.py`
- [rss-runner] `orca-harness/runners/run_source_capture_youtube_rss_monitor.py`
- [parser-tests] `orca-harness/tests/unit/test_youtube_channel_rss.py`
- [runner-tests] `orca-harness/tests/unit/test_youtube_rss_monitor.py`
- [seam-decl] `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- [inventory-decl] `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`

Loaded context reads:

- `orca-harness/runners/run_source_capture_youtube_watch_batch.py`
- `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/packet_assembly.py`
- `orca-harness/data_lake/root.py`
- `orca-harness/data_lake/inventory.py`
- `orca-harness/capture_spine/creator_profile_current/youtube_watch_packet_metric_document.py`
- `orca-harness/youtube_capture/behavioral_projection.py`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_grid_tier_assessment_v0.md`

Missing required context read:

- `docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md` was absent in the reviewed worktree and not found by filename search. The assessment receipt above carries the relevant owner-direction and probe-evidence quotes used for this review, but this report records the missing source as a context gap.

## Findings

### F-01 major - RSS feed identity was not bound to the requested roster channel

Location: [rss-runner] `_capture_channel` before patch.

Evidence: the runner fetched `feeds/videos.xml?channel_id=<requested>`, parsed the feed, and then wrote the packet with `channel_id` copied from the ledger request. The parsed feed's `feed_channel_id_as_served` and `entry_channel_ids` were only recorded in `rss_monitor_entries.json`; they did not gate packet write. The parser already exposes both identifiers. The assessment receipt says feed-level `yt:channelId` may omit `UC`, while entry-level `yt:channelId` carries the full ID.

Impact: a redirected, mis-served, mocked, or otherwise wrong feed could be committed as exact metrics for the requested roster channel. That is a silent attribution failure: the packet would look trustworthy, and downstream spike decisions could stand on another channel's newest uploads.

Minimum closure condition: before any packet write, the served feed identity must match the requested roster channel, accepting only the observed feed-level no-`UC` prefix variant; mismatched or missing feed identity must surface as a visible per-channel failure and write no packet.

Next authorized action: patched within [rss-runner] and covered by [runner-tests]. CA should adjudicate whether to keep the strict missing-identity fail-closed posture.

Patch and citations:

- [rss-runner] Added `_validate_parsed_channel_identity()` and `_feed_channel_id_matches_request()`, called immediately after parsing. Source basis: parser exposes `feed_channel_id_as_served` and `entry_channel_ids`; assessment receipt records the feed-level no-`UC` quirk.
- [runner-tests] Updated RSS fixtures to carry feed-level and entry-level `yt:channelId`; added `test_feed_channel_identity_mismatch_is_visible_failure` proving mismatch exits 2 and writes no packet.

### F-02 major - prior-state readback failure silently collapsed first-seen state

Location: [rss-runner] `_entries_artifact_payload` and `_latest_channel_states` before patch.

Evidence: `_entries_artifact_payload` caught every exception and returned `None`; `_latest_channel_states` then continued scanning. If no usable prior packet remained, `_capture_channel` treated the channel as baseline. If `known_video_ids_cumulative` was malformed, the old code used an empty set. Both cases could turn unknown prior state into baseline or all-new first-seen flags.

Impact: a packet could carry silently wrong `first_seen` values, including false baselines and false new-video flags. This directly violates the monitor goal: first-seen state is supposed to be lake-derived, not invented when readback is corrupt.

Minimum closure condition: an unreadable, undecodable, missing, or malformed prior RSS entries artifact for this surface must block new packet writes and surface a visible failure; it must not downgrade to baseline, older state, or an empty known set.

Next authorized action: patched within [rss-runner] and covered by [runner-tests].

Patch and citations:

- [rss-runner] Changed `_entries_artifact_payload()` to raise a state-derivation error on load, decode, non-object, or missing-artifact failures.
- [rss-runner] Changed `_latest_channel_states()` to reject missing `channel_id`, missing/invalid `retrieval_time_utc`, and invalid `known_video_ids_cumulative`.
- [rss-runner] Changed `run_youtube_rss_monitor()` to convert prior-state derivation errors into visible per-channel `capture_failed` rows with exit 2 and no fetch/write.
- [runner-tests] Added `test_prior_state_readback_failure_is_visible_not_baseline`, proving corruption prevents a new fetch/write and records the failure.

### F-03 major - latest-prior selection depended on packet-id ordering, not capture time

Location: [rss-runner] `_latest_channel_states` before patch.

Evidence: the old docstring stated that packet IDs are ULIDs and availability ordering is commit-time order. The lake context confirms `list_available()` sorts availability JSON filenames and returns packet IDs; it does not provide channel-state authority. The old scan stopped after the first packet found for each channel. Same-millisecond or otherwise ambiguous prior packets could choose by packet-id order rather than the entries artifact's `retrieval_time_utc`.

Impact: a packet could compute `first_seen` against the wrong prior state. The risk is rare in daily operation but real in tests, manual reruns, and same-clock captures; when it occurs, the output is silently wrong.

Minimum closure condition: latest state must be selected from the RSS entries artifact's capture time, and equal-timestamp ambiguity must fail visibly rather than guessing.

Next authorized action: patched within [rss-runner] and covered by [runner-tests].

Patch and citations:

- [rss-runner] `_latest_channel_states()` now loads candidates for this surface, parses `retrieval_time_utc`, selects by that time, and raises on equal-timestamp ambiguity.
- [runner-tests] Added `test_equal_prior_retrieval_times_fail_visible_not_packet_id_guess`, proving equal prior retrieval times exit 2 and write no new packet.

## Non-Findings

- Metric honesty: [rss-parser] uses strict integer parsing and represents absent/unparseable views/starRating as `None` plus limitation notes. [rss-runner] emits `MetricPosture.OBSERVED` only with real values and `UNAVAILABLE_WITH_REASON` for missing view/like/comment fields.
- starRating provenance: [rss-runner] records starRating as `like_count` only with a packet-level provenance limitation naming the feed source and N=2 validation basis.
- Consumer isolation: existing YouTube live consumers read `youtube_watch_metadata_comments`; the new `youtube_channel_rss_feed` surface does not collide with those filters.
- Declarations: [seam-decl] includes `run_source_capture_youtube_rss_monitor.py` in `EXPECTED_BRONZE_WRITER_RUNNERS`; [inventory-decl] records it as a direct raw packet writer with `a2_fork_impact: manifest_shape`.
- Run mechanics: existing tests cover exit 0/2/4, cooldown refusal, visible per-channel failures, null-channel-id visibility, and real packet write/readback.

## Not-Proven Boundaries

- The missing handoff source means owner-direction context is not fully source-complete, though the loaded assessment receipt carries the needed direction and probe evidence.
- No live HTTP/RSS fetch was run in this review; validation is unit/contract/integration harness only.
- The patch intentionally does not claim operating-envelope safety, scheduler readiness, spike threshold correctness, or registry readiness.
- The stricter prior-state scan loads all prior packets for the RSS surface to avoid packet-id ordering authority. That is acceptable for trustworthiness here, but large future history may justify a separate indexed state design.

## Validation

Targeted command:

```text
python -m pytest tests\unit\test_youtube_rss_monitor.py -q
```

Observed result:

```text
12 passed
```

Full commissioned command from `orca-harness/`:

```text
python -m pytest
```

Observed result:

```text
2479 passed, 7 skipped, 1 warning in 207.08s (0:03:27)
```

Warning observed:

```text
PytestUnknownMarkWarning: Unknown pytest.mark.integration in tests\integration\test_reddit_screening_read_live.py:17
```

## Working-Tree Diff Summary

Diff left uncommitted in the lane worktree:

```text
[rss-runner] orca-harness/runners/run_source_capture_youtube_rss_monitor.py
[runner-tests] orca-harness/tests/unit/test_youtube_rss_monitor.py
```

Observed `git diff --stat` before this report file was written:

```text
.../run_source_capture_youtube_rss_monitor.py      | 167 ++++++++++++++++-----
.../tests/unit/test_youtube_rss_monitor.py         | 107 ++++++++++++-
2 files changed, 235 insertions(+), 39 deletions(-)
```

The working-tree unified diff is intentionally left in the repository for CA adjudication; no commit, push, merge, or acceptance action was performed.

## Overall Verdict

MATERIAL_SEAMS_FOUND_AND_PATCHED_WITHIN_SCOPE.

The patched seams were channel attribution, prior-state corruption, and ambiguous latest-prior selection. Residual risk is bounded to CA adjudication of the stricter fail-closed behavior and future performance if the RSS packet history grows large. This is not PASS, readiness, validation authority, or acceptance.

## DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- Original commission: YT tier-1 RSS monitor delegated adversarial code review-and-patch.
- Reviewed head: `ffeeb13179a72e4aacafb69267d9e6fa7c2d261a` on `claude/yt-rss-tier1-monitor`.
- Reviewed files: [rss-parser], [rss-runner], [parser-tests], [runner-tests], [seam-decl], [inventory-decl], plus the context reads listed above.
- Findings: F-01, F-02, F-03, all patched within the named target set.
- Proposed patch: uncommitted working-tree diff in [rss-runner] and [runner-tests].
- Citations: included per finding above.
- Validation: targeted RSS monitor tests and full `python -m pytest` passed as observed.
- Residual risk: missing handoff source; stricter fail-closed state scan may need future indexing if history grows.
- Non-claims: no PASS, no readiness, no acceptance, no commit, no push.
