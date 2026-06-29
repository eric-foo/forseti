# YouTube Behavioral Lake Metadata Bridge — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (advisory code review)
scope: >
  Read-only cross-vendor adversarial code review of PR #440 Batch 3: the YouTube
  behavioral projection now discovers committed watch metadata/comment packets
  from DataLakeRoot by platform_video_id instead of requiring a manually passed
  metadata packet.
authority_boundary: retrieval_only
review_authority_boundary: advisory_only
commission_prompt: docs/prompts/reviews/youtube_behavioral_lake_metadata_bridge_adversarial_code_review_prompt_v0.md
branch_or_commit: codex/youtube-capture-spine-sync @ 0c56ebe2 (Batch 3 diff = single commit over base 5e36ba6e)
review_mode: workflow-code-review, adversarial posture
output_class: findings-first advisory; no formal verdict, no patch queue, no readiness/approval, no runtime-model recommendation
```

## Method Order Declaration

- REFERENCE-LOADED (not pre-applied): `workflow-deep-thinking`, `workflow-code-review`.
- SOURCE-LOAD result: **`SOURCE_CONTEXT_READY`** (ledger below). No material source gap blocks the named review axes.
- Applied `workflow-deep-thinking` to frame failure modes, then `workflow-code-review` for findings-first review.
- `workflow-code-review` was available and applied → no `BLOCKED_REVIEW_LANE_UNAVAILABLE`.

## What The Patch Does (confirmed against source)

The Batch 3 diff (commit `0c56ebe2`, base `5e36ba6e`) touches three files; the prompt artifact is excluded from findings per its own instruction. The two implementation targets:

- `orca-harness/youtube_capture/behavioral_projection.py` — adds `metadata_packet_for_video(...)` (lake discovery of the latest watch metadata/comment packet by video id), adds `_watch_metadata_packet(...)` (reconstructs the watch payload from `youtube_watch_capture.json`), wires `project_youtube_behavioral_item_from_lake(...)` to auto-discover metadata when no `metadata_packet` is passed, and extends `normalize_youtube_metadata_packet(...)` output with four capture-provenance keys.
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py` — adds real-commit discovery and latest-selection tests via `write_youtube_watch_packet(..., data_root=...)`.

This directly fulfills `youtube_first_behavioral_completion_spec_v0.md` acceptance criterion 5 (deterministic programmatic lookup keyed by `platform_video_id`, no manual convention) and criterion 8 (deterministic correlation given a video id), and matches the spec's "latest successful capture by capture time" rule (spec lines 185-186). The writer↔reader round-trip is consistent: surface name (`youtube_watch_metadata_comments`), capture-JSON filename (`youtube_watch_capture.json`), and payload keys all align between `source_capture/youtube_watch_packet.py` and the new reader.

---

## Findings (ordered by materiality)

### F1 — Major (failure-visibility): uninterpretable watch-metadata packets are silently downgraded to "absent"

- **Commissioned target / purpose:** `behavioral_projection.py` — does malformed/corrupt watch-metadata discovery stay fail-visible rather than be silently converted to a non-failure?
- **Anchor:** `metadata_packet_for_video` at `behavioral_projection.py:118-152` (esp. `except DataLakeRootError: continue` at `:130-133`, and `if packet is None: continue` at `:138-139`); `_watch_metadata_packet` at `:697-724` (silent `return None` on missing body `:698-700`, on JSON/decode error `:701-704`, on non-Mapping payload `:705-706`).
- **Implementation evidence:** For a packet whose `manifest.json` is intact and whose `source_surface == "youtube_watch_metadata_comments"` (so `load_raw_packet` does **not** raise), but whose `youtube_watch_capture.json` is unreadable as JSON, is not a Mapping, is missing, or carries a blank/missing `platform_video_id` (or a future schema drift), `_watch_metadata_packet` returns `None` and `metadata_packet_for_video` silently `continue`s. The same packet is **also** silently ignored by the sibling `transcript_sources_for_video`, because watch-surface packets have no `capture_metadata.json` (`youtube_watch_packet.py:113-116` stages only `raw_watch.html`, `youtube_watch_capture.json`, comment pages), so `meta_video_id` is `None` and the packet is dropped at the `meta_video_id != platform_video_id` guard (`:185-187`) before the surface dispatch — and that dispatch has no `else` branch anyway (`:188-220`). Net effect: `project_youtube_behavioral_item` receives `metadata=None` and emits residual **`youtube_metadata_packet_absent`** (`:260-261`), which is indistinguishable from "no watch packet was ever captured." Because `behavioral_completeness.complete` is derived **only** from the transcript rollup (`:303-307`), a video with a healthy extracted caption plus a *corrupt* watch packet is reported `complete = True` while the corruption is labeled merely "absent."
- **Authority / evidence basis:** The module's documented contract names this exact property as its strongest behavior. `youtube_behavioral_contract_from_merged_main_v0.md:94` ("The YouTube projection catches those failures at transcript discovery and turns them into source-level `discovery_failed` residuals instead of aborting") and `:287` ("Discovery failures are target-video-projected even when the unreadable packet cannot prove its own video id. This keeps failures visible"). The completion spec demands "explicit … failed … states instead of fake success" (`youtube_first_behavioral_completion_spec_v0.md:67-68`) and "preserve false-success visibility over cosmetic parity" (`:292`). The AGENTS kernel: "Preserve real failure visibility." The new metadata path is strictly *less* visible than the sibling transcript path it sits beside.
- **Impact:** Correctness/review-confidence. A real read/parse/shape failure on captured metadata is laundered into "absent," so an operator or downstream consumer cannot distinguish "never captured" from "captured but broken — needs recapture/cleanup." A corrupt metadata packet does not block `complete=True`.
- **Mitigations (stated to bound the severity):** (a) The *load-error* subclass — corrupt `manifest.json`, missing/size-mismatched/unreadable preserved bytes — still raises `DataLakeRootError` inside `load_raw_packet` (`data_lake/root.py:859-869`), which the **transcript** path surfaces as a `discovery_failed` source/residual; only the "loads-OK-but-uninterpretable-payload" subclass is fully invisible. (b) Completeness is transcript-scoped by contract, so this is not a zero-signal fake success — the wrong residual (`absent`) is present.
- **Minimum closure condition:** When `metadata_packet_for_video` encounters a watch-surface packet it cannot interpret (load error swallowed, missing/invalid capture JSON, or no usable video id), emit a fail-visible signal instead of silently dropping it — e.g. a `youtube_metadata_discovery_failed` / `youtube_metadata_packet_unreadable` residual, or a lake/global discovery-residual channel. Note the contract's own transfer note (`contract:287-288`) flags that target-video attribution of an unprovable packet is imprecise; a lane/global discovery residual may be the more honest shape than forcing target attribution. The fix should not silently convert the failure to "absent."
- **Next authorized action:** Operator/home-model decision on whether to bind a metadata-discovery residual (and which channel). Not auto-fixed here.
- **Verification expectation:** A unit test that commits a watch packet, makes its `youtube_watch_capture.json` uninterpretable while keeping the manifest/size valid, and asserts a distinct discovery/unreadable residual (not `youtube_metadata_packet_absent`).
- **`patch_queue_entry`:** no.

### F2 — Minor (test gap, paired with F1): no coverage of the watch-metadata corruption/uninterpretable path

- **Anchor:** `tests/unit/test_youtube_behavioral_projection.py:248-321` (the two corruption tests, `..._corrupt_youtube_packet...` and `..._preserved_file_read_error...`).
- **Implementation evidence:** Both corruption tests corrupt a **caption** packet (`video_id="other000000"`) and assert the **transcript** path residualizes it (`discovery_failed`). There is no test that commits a watch-metadata packet, corrupts/empties its capture JSON or drops its video id, and asserts the metadata-discovery behavior. The discovery happy-path (`:210-231`) and latest-selection (`:234-245`) tests are strong and use real `write_youtube_watch_packet(..., data_root=...)` commits, so the gap is specifically the failure path of the new code.
- **Authority / evidence basis:** Same as F1; the test suite already enshrines the visible-failure contract for transcripts but not for the new metadata path.
- **Impact:** The exact regression in F1 is unguarded; future refactors can silently re-introduce or worsen it.
- **Minimum closure condition:** Add the F1 verification test.
- **Next authorized action:** Bundle with F1 resolution.
- **`patch_queue_entry`:** no.

### F3 — Minor / advisory (doc drift): the merged-main contract record now under-describes `metadata_capture`

- **Anchor:** `normalize_youtube_metadata_packet` output keys `capture_packet_id`, `source_surface`, `capture_schema_version`, `capture_timestamp` at `behavioral_projection.py:94-97`; vs. `youtube_behavioral_contract_from_merged_main_v0.md:51-62` (lists `metadata_capture` fields without these four) and the contract's silence on a `metadata_packet_for_video` discovery path.
- **Implementation evidence:** The patch adds four always-present keys to `metadata_capture` and a new lake-discovery entry point. The contract record (whose `use_when` is "recovering the YouTube-side … semantics without rereading the full implementation") does not reflect either.
- **Authority / evidence basis:** The contract doc is explicitly `authority_boundary: retrieval_only` and SHA-pinned to `origin/main @ 6517dd10`, so it is descriptive, not a normative gate — this is **not** a contract violation. But it is now a stale load-bearing reference.
- **Impact:** Low. A reader trusting the record as the YouTube reference will miss the new provenance keys and the discovery path. Additive keys are backward-compatible (no existing key changed; the 28-test run passes), so no consumer breaks.
- **Minimum closure condition:** Either refresh the record to the post-bridge shape or add a note that it predates the Batch 3 bridge. Optional for this PR.
- **`patch_queue_entry`:** no.

### F4 — Minor / advisory (latent, not triggered today): lexicographic `capture_timestamp` ordering assumes homogeneous ISO-`Z` format

- **Anchor:** latest-selection key at `behavioral_projection.py:146-152` — `max(..., key=lambda p: (capture_timestamp or "", capture_packet_id or ""))`.
- **Implementation evidence:** Selection compares `capture_timestamp` as a raw string. The current writer always emits a UTC `…Z` ISO-8601 timestamp (`youtube_watch_packet.py:90,107` → `_utc_now_z()` / controlled `now_iso`), and `packet_id` is a time-sortable ULID (`data_lake/root.py:71`), so the tie-break resolves to true creation order. **Today this is deterministic and correct.** The latent risk: a future/foreign writer emitting a timezone *offset* form (e.g. `…+08:00`) would sort lexicographically out of chronological order, silently selecting a non-latest packet as "latest."
- **Authority / evidence basis:** Spec rule is "latest **successful** capture by **capture time**" (`completion_spec:185-186`) — a semantic (instant) comparison, which lexicographic string compare only approximates under a single normalized format.
- **Impact:** None under the current writer; a correctness risk only if timestamp formats diversify. Failure mode is a silently-stale "latest" pick, not a crash.
- **Minimum closure condition:** If heterogeneous timestamp formats ever become possible, parse to an instant before comparison (or assert/normalize the format at write time). No action required while the writer is the sole source.
- **`patch_queue_entry`:** no.

### F5 — Minor / advisory (efficiency): `project_youtube_behavioral_item_from_lake` loads every YouTube packet twice per call

- **Anchor:** `behavioral_projection.py:320-336` — the wrapper calls `metadata_packet_for_video(...)` and `transcript_sources_for_video(...)`, each independently iterating `data_root.list_available(source_family="youtube")` and calling `load_raw_packet` (which re-reads and integrity-checks all preserved bytes, `data_lake/root.py:797-869`) on every YouTube packet.
- **Implementation evidence:** Two full O(N) scans with full body reads per projection call; watch packets are loaded by both functions.
- **Authority / evidence basis:** Consistent with the pre-existing single-scan discovery design — not introduced as a regression, just doubled.
- **Impact:** I/O cost scales with lake size; correctness unaffected. Negligible for the current test/dev scale.
- **Minimum closure condition:** If projection-over-large-lake becomes hot, share one scan/load pass between metadata and transcript discovery. Premature now.
- **`patch_queue_entry`:** no.

---

## Axes Checked And Cleared (no defect found)

- **Surface isolation / no false matches:** `metadata_packet_for_video` filters strictly on `source_surface == WATCH_METADATA_SURFACE` (`:134`) and exact `platform_video_id` string match (`:140-142`); caption/audio packets cannot be mistaken for metadata. Clean.
- **No route-receipt laundering / identity preserved:** `_watch_metadata_packet` keeps the nested `packet` (carrying `receipts`, `metric_receipts`, `channel`, `metadata`, `engagement`, `comments`), and `setdefault`s identity from the validated top-level payload; it sets `capture_packet_id`/`source_surface` without dropping platform/video identity (`:707-724`). Writer preserves the full packet under `payload["packet"]` (`youtube_watch_packet.py:110`). Clean.
- **Explicit override respected; no implicit rebuild:** `project_youtube_behavioral_item_from_lake` uses the passed `metadata_packet` when non-None and only discovers otherwise (`:323-327`); `rebuild_availability` runs at most once at the top and both sub-calls pass `rebuild_availability=False` (`:321-322,326,331`) — no double rebuild, opt-in write preserved. Clean.
- **Transcript discovery / extraction matching / canonical selection intact:** `transcript_sources_for_video` logic is unchanged except the caller moved the (single) rebuild up; covered by the unchanged, passing tests. Clean.
- **Tests prove real behavior:** new discovery/latest tests commit through `write_youtube_watch_packet(..., data_root=...)` (`:82-105,210-245`), not a synthetic manual dict. Clean.
- **No unauthorized claims:** no shared-core / IG-parity / live-capture / Cleaning / Judgment / scheduler / dashboard / production-readiness / buyer-proof claim appears in the diff or new tests; the no-runtime-acquisition contract test passes and the module adds no forbidden import (only `json`, already present; `DataLakeRootError` already imported). Clean.

## Source-Read Ledger

Primary sources read at `codex/youtube-capture-spine-sync @ 0c56ebe2`:

- Batch 3 diff for `youtube_capture/behavioral_projection.py` (`git show 0c56ebe2`) — reviewed.
- `orca-harness/youtube_capture/behavioral_projection.py` — full read (implementation target).
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py` — full read (implementation target).
- `orca-harness/source_capture/youtube_watch_packet.py` — full read (context: writer; round-trip cross-check).
- `orca-harness/data_lake/root.py` — targeted read of packet-id grammar, `list_available`/`load_raw_packet`/`find_packet`/`record_availability`, and `load_raw_packet` integrity guards.
- `orca-harness/tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py` — full read (context: acquisition boundary).
- `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md` — full read (context: documented contract).
- `docs/workflows/youtube_first_behavioral_completion_spec_v0.md` — full read (context: fitness criteria).
- The commission prompt (read from commit `0c56ebe2`).

Listed-but-not-opened: `tests/unit/test_source_capture_youtube_watch_packet.py` (executed via pytest, passed; not line-read) and `docs/review-outputs/youtube_behavioral_projection_post_patch_adversarial_code_recheck_v0.md` (prior-review context). Neither is a material gap for the named axes.

## Validation Run Status

**Reproduced (not merely trusted).** Reviewer ran the prompt's focused command in the reviewed worktree:

```
tests/unit/test_youtube_behavioral_projection.py
tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py
tests/unit/test_source_capture_youtube_watch_packet.py
tests/unit/test_youtube_watch_runner_output_mode.py
tests/unit/test_youtube_caption_runner_output_mode.py
```

Observed: **28 passed** — matches the dispatcher-reported `28 passed`. This is evidence the changed behavior is green; it is not a formal validation/readiness claim, and it does not exercise the F1 failure path (which has no test).

## Strict-Only Blockers / Not-Proven Boundaries

- No blocker-class defect found; no formal verdict is issued (out of authority for this prompt).
- **Not proven:** behavior under a watch packet that loads cleanly but carries an uninterpretable/shape-drifted `youtube_watch_capture.json` (F1) — no test, and the code path is silent.
- **Not proven:** behavior under heterogeneous `capture_timestamp` formats (F4) — current writer never produces them.
- Not assessed (excluded by scope): IG parity, shared capture-core, live capture, transcript extraction quality, Cleaning/Judgment/scheduler/dashboard/runtime.

## Open Questions

1. Should an uninterpretable-but-loadable watch metadata packet residualize as a target-video metadata-discovery failure, or feed a lane/global discovery-residual channel (per the contract's `:287-288` transfer note)? (Drives the F1 fix shape.)
2. Is `behavioral_completeness.complete` intended to stay purely transcript-scoped, such that a broken metadata packet never affects completeness? If yes, F1's residual-accuracy fix is sufficient; if no, completeness may also need to react to metadata-discovery failure.

## Residual Risk

Low-to-moderate, concentrated in F1: silent metadata-discovery drops can mask a recapture/cleanup need while the lane still reads "complete." Remaining items (F3–F5) are advisory and low-impact. The happy-path bridge itself is sound, deterministic, and spec-aligned.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized. No patch, diff, exact edits, formal verdict, severity authority, or patch queue is claimed (`NOT_CLAIMED`).

## Provenance

```yaml
reviewed_by: Anthropic Claude (Opus 4.x) acting as delegated reviewer; operator to record acceptance
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery (reviewer lineage Anthropic; author lineage OpenAI/Codex — known, different upstream families)
same_vendor_rationale: not_applicable
```

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- Original commission: read-only adversarial code review of PR #440 Batch 3 — YouTube behavioral lake metadata bridge (prompt: docs/prompts/reviews/youtube_behavioral_lake_metadata_bridge_adversarial_code_review_prompt_v0.md).
- Implementation context / diff / reviewed files: commit 0c56ebe2 over base 5e36ba6e on codex/youtube-capture-spine-sync; behavioral_projection.py (+ new metadata_packet_for_video / _watch_metadata_packet / from_lake wiring / 4 normalize keys) and test_youtube_behavioral_projection.py; context: youtube_watch_packet.py, data_lake/root.py, the no-runtime-imports contract test, the merged-main contract record, and the completion spec.
- Findings + evidence: F1 Major (uninterpretable-but-loadable watch packets silently become youtube_metadata_packet_absent, no metadata-discovery residual, diverges from the module's documented visible-failure contract; load-error subclass still visible via transcript path; completeness is transcript-scoped). F2 Minor (no test for that failure path). F3 Minor/advisory (merged-main contract record stale re: 4 new metadata_capture keys + discovery path). F4 Minor/advisory/latent (lexicographic capture_timestamp ordering; sound today via ULID tie-break). F5 Minor/advisory (from_lake double-loads every YouTube packet). Axes for surface isolation, identity preservation, override/rebuild, transcript intactness, real-commit tests, and no-unauthorized-claims all checked clean.
- Proposed patch / diff / exact edits: NOT_CLAIMED (read-only commission).
- Citations: file:line anchors throughout; primary sources in the source-read ledger.
- Reviewer verdict: NOT_CLAIMED (advisory findings only; no approval/readiness/severity authority).
- Validation evidence / not-run: reproduced focused pytest = 28 passed; F1 failure path not exercised by any test.
- Residual risk: low-moderate, concentrated in F1.
- Blockers / off-scope / not-proven: no blocker-class defect; uninterpretable-loadable metadata payload behavior and heterogeneous-timestamp behavior are not proven; IG/shared-core/live/Cleaning/Judgment/runtime excluded by scope.
```
