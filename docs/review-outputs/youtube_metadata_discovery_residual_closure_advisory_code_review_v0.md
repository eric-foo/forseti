# YouTube Metadata Discovery Residual Closure — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (advisory code review)
scope: >
  Read-only cross-vendor adversarial code review of PR #440 Batch 4: closing the
  delegated-review findings F1/F2 from the Batch 3 lake metadata bridge review so
  that loadable-but-uninterpretable YouTube watch metadata packets become a
  fail-visible metadata-discovery residual instead of collapsing to ordinary
  `youtube_metadata_packet_absent` alone.
authority_boundary: retrieval_only
review_authority_boundary: advisory_only
commission_prompt: docs/prompts/reviews/youtube_metadata_discovery_residual_closure_adversarial_code_review_prompt_v0.md
branch_or_commit: codex/youtube-capture-spine-sync @ 3ffc251b (Batch 4 diff = single commit over base 0c56ebe2)
review_mode: workflow-code-review, zero-config findings-only advisory, adversarial posture
output_class: findings-first advisory; no formal verdict, no patch queue, no readiness/approval, no severity authority, no runtime-model recommendation, no no-new-seam claim
```

## Method Order Declaration

- REFERENCE-LOADED (not pre-applied): `workflow-deep-thinking`, `workflow-code-review`.
- SOURCE-LOAD result: **`SOURCE_CONTEXT_READY`** (ledger below). No material source gap blocks the named review axes.
- Applied `workflow-deep-thinking` to frame failure modes, then `workflow-code-review` (zero-config findings-only advisory mode — the commission disclaims formal verdict/patch-queue/readiness and the output is named `advisory`) for findings-first review.
- `workflow-code-review` was available and applied → no `BLOCKED_REVIEW_LANE_UNAVAILABLE`.

## What The Patch Does (confirmed against source)

The Batch 4 diff (commit `3ffc251b`, base `0c56ebe2`) touches four files. Two are excluded from findings per the commission: the review prompt artifact (`docs/prompts/reviews/youtube_metadata_discovery_residual_closure_adversarial_code_review_prompt_v0.md`) and the prior review-output report (`docs/review-outputs/youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md`). The two implementation targets:

- `orca-harness/youtube_capture/behavioral_projection.py` — splits the public lookup `metadata_packet_for_video(...)` (`:119-131`) from a new private `_metadata_packet_for_video(...)` (`:134-184`) that returns `tuple[dict | None, list[str]]` (packet, discovery residuals). `_watch_metadata_packet(...)` is re-typed to `tuple[dict | None, str | None]` and now returns a classified reason instead of bare `None`: `missing_capture_json` (`:740-741`), `invalid_capture_json` (`:744-745`), `capture_payload_not_object` (`:746-747`). The scan loop turns a classified reason, and a parsed-but-`None`-video-id packet, into `youtube_metadata_packet_discovery_failed:<packet_id>:<reason>` residuals via `_metadata_discovery_failed_residual(...)` (`:768-769`) and `_append_residual_once` (`:714-716`). `project_youtube_behavioral_item(...)` gains a keyword-only `metadata_discovery_residuals: Sequence[str] = ()` param (`:273`) merged into the residual list before the `youtube_metadata_packet_absent` append (`:292-298`); `project_youtube_behavioral_item_from_lake(...)` captures and threads those residuals (`:360-368`).
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py` — adds `_rewrite_preserved_body(...)` (`:109-121`), which overwrites a preserved file's bytes **and** updates the manifest `size_bytes`/`sha256` to stay coherent, plus `test_projection_from_lake_residualizes_uninterpretable_watch_metadata_packet` (`:264-283`).

This implements the home-model-adjudicated closure of accepted findings F1 (failure-visibility) and F2 (test coverage) from `youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md:39-60`, and aligns with the completion spec's acceptance criterion 5 — legacy metadata packets are "bridged into the correlation contract or explicitly kept as a **named residual** with a deterministic programmatic lookup path keyed by `platform_video_id`" (`youtube_first_behavioral_completion_spec_v0.md:234-237`).

---

## Closure Assessment (accepted F1/F2 + correctly-deferred F3/F4/F5)

### Accepted F1 (loadable-but-uninterpretable must be fail-visible, not `absent` alone) — **CLOSED as accepted**

- **Evidence:** When a watch-surface packet loads cleanly (`load_raw_packet` does not raise) but its `youtube_watch_capture.json` is missing / non-UTF-8-JSON / not a JSON object / carries no usable video id, `_metadata_packet_for_video` now appends a distinct `youtube_metadata_packet_discovery_failed:<packet_id>:<reason>` residual (`:153-169`) instead of the prior silent `continue`. When that uninterpretable packet was the video's only metadata packet, no candidate survives → `metadata=None` → `project_youtube_behavioral_item` appends `youtube_metadata_packet_absent` **in addition to** the discovery-failed residual (`:292-298`). Both residuals coexist and `metadata_capture is None` (`:333`).
- **Verified against the accepted wording:** the adjudication required the condition "must become fail-visible and must not collapse to ordinary `youtube_metadata_packet_absent` alone." The new test asserts exactly the both-present shape (`test:281-282`). The condition is no longer laundered into `absent` alone.
- **Channel choice (cleared axis):** the patch reuses the existing per-video `behavioral_completeness.residuals` channel (the same one transcript discovery residuals use) and does **not** introduce a lane/global residual architecture or claim one. The prior review floated a lane/global channel as one option (`prior:47`, contract `:287-288`); the patch took the narrower, lower-lock-in, target-projected option, consistent with the commission's non-goal ("do not introduce lane/global residual architecture").

### Accepted F2 (add coverage for the uninterpretable path with a real lake-backed packet) — **CLOSED as accepted**

- **Evidence:** `test_projection_from_lake_residualizes_uninterpretable_watch_metadata_packet` (`test:264-283`) commits a real watch packet via `write_youtube_watch_packet(...)` (through `_commit_watch_metadata`), rewrites the committed `youtube_watch_capture.json` body to `b"{not-json"` while keeping the manifest `size_bytes`/`sha256` coherent (`test:109-121,270`), and asserts the distinct `…:invalid_capture_json` residual, the co-present `youtube_metadata_packet_absent`, `metadata_capture is None`, and `complete is True`.
- **The test exercises the intended subclass, verified decisively:** `load_raw_packet` fail-closes on a preserved-file size mismatch (`data_lake/root.py:866-870`) and sha256 mismatch (`:877-881`). Therefore, without the manifest size/sha update, `b"{not-json"` would raise `DataLakeRootError` and the loop would `continue` (`behavioral_projection.py:148-149`) with **no** discovery residual — the `…:invalid_capture_json` assertion would fail. Because that residual is reachable **only after** a successful load (`_watch_metadata_packet:744-745`), the green run proves the packet loaded and the loadable-but-uninterpretable path was hit — not a `DataLakeRootError` integrity failure. This is the precise distinction the existing `test_transcript_discovery_residualizes_corrupt_youtube_packet...` (`test:286-320`) draws by corrupting the **manifest** instead; the two tests deliberately target different subclasses.

### F3 (SHA-pinned merged-main contract record stale) — **correctly not implemented**
The diff makes no change to `youtube_behavioral_contract_from_merged_main_v0.md` and creates no contradictory current-source claim in code. Consistent with the deferral ("retrieval-only; do not require for this patch").

### F4 (lexicographic `capture_timestamp` ordering) — **correctly not implemented / not overconstrained**
The latest-selection key `max(..., key=lambda p: (capture_timestamp or "", capture_packet_id or ""))` is unchanged (`:175-184`). No normalization or assertion was added; the latent risk is neither fixed nor worsened. Consistent with "no action."

### F5 (double scan/load per projection) — **correctly not implemented / not overconstrained**
`project_youtube_behavioral_item_from_lake` still independently calls `_metadata_packet_for_video` and `transcript_sources_for_video`, each scanning `list_available(source_family="youtube")` and `load_raw_packet`-ing every packet (`:360-371`). The patch adds only a per-failure `_append_residual_once` on the metadata path; no material efficiency change. Consistent with "efficiency advisory, not required."

---

## Findings (ordered by materiality)

### N1 — Minor / advisory (test coverage): three of the four new discovery-failure reasons are unverified; the one behavior-changing branch (`missing_platform_video_id`) is untested

- **Commissioned target / purpose:** `behavioral_projection.py` + `test_youtube_behavioral_projection.py` — does the closure's verification cover the failure branches it introduced, so a future refactor cannot silently regress them?
- **Anchor:** new reasons at `behavioral_projection.py:740-741` (`missing_capture_json`), `:746-747` (`capture_payload_not_object`), and `:160-169` (`missing_platform_video_id`); single new test asserts only `invalid_capture_json` (`test:281`).
- **Implementation evidence:** The patch introduces four discovery-failure reasons. The new test (`test:264-283`) exercises exactly one (`invalid_capture_json`). The other three are unguarded. The most material of these is **`missing_platform_video_id`**, which is a genuine **semantic change**: in the Batch 3 code a parsed packet with no usable video id fell through the `packet_video_id != platform_video_id` guard and was silently skipped; Batch 4 now emits a distinct residual for it (`:160-169`). That new visible-failure branch — the same *class* of behavior F2 was created to lock down — has no test. (`missing_capture_json` and `capture_payload_not_object` are lower-risk sibling branches of the tested decode path.)
- **Authority / evidence basis:** Accepted F2's literal minimum closure was "add the F1 verification test" with a verification expectation naming the uninterpretable-capture-JSON case (`prior:49,58`); that singular case **is** covered, so F2 is closed as accepted. This finding is the *additional* coverage gap the closure surfaced, against the same visible-failure contract the suite already enshrines for transcripts (`prior:56`). Repo-visible evidence only; not an overlay-bound severity.
- **Impact (review-confidence):** A future refactor could silently drop the `missing_platform_video_id` residual (reverting to the old silent skip) or the missing/non-object branches without any test failing — re-opening a narrower instance of the F1 regression for the untested reasons.
- **`minimum_closure_condition`:** Add coverage that commits a watch packet whose capture JSON parses to an object lacking `platform_video_id`/`video_id` and asserts `youtube_metadata_packet_discovery_failed:<id>:missing_platform_video_id`; ideally also assert `missing_capture_json` and `capture_payload_not_object`. Treat closed once the behavior-changing `missing_platform_video_id` branch is guarded.
- **`next_authorized_action`:** Operator / home-model decision to commission the additional coverage (advisory; this review lane is read-only and cannot itself add tests).
- **Verification expectation:** Same-check red-green — the proposed assertions fail against the unfixed `missing_platform_video_id` branch only if it is removed/regressed; they pass against the current code. (Not run here; no patch authorized.)
- **`patch_queue_entry`:** no.

---

## Axes Checked And Cleared (no defect found)

- **Public lookup shape preserved:** `metadata_packet_for_video` still returns `dict | None` (`:119-131`); the tuple is an internal `_metadata_packet_for_video` detail whose residuals the public wrapper discards (`:126`). Within `orca-harness`, the only callers of `metadata_packet_for_video`, `_watch_metadata_packet`, and `project_youtube_behavioral_item` are inside `behavioral_projection.py` itself (no external importer of `metadata_packet_for_video` anywhere in the worktree). The new `metadata_discovery_residuals` parameter is keyword-only with a default, so the test-file caller and any future external caller are source-compatible. Clean.
- **No laundering into `absent` alone:** verified above (Closure F1); both residuals co-present, `metadata_capture is None`. Clean.
- **Healthy discovery / latest-selection / explicit override unchanged:** the happy-path discovery (`test:226-248`) and latest-selection (`test:250-261`) tests are unchanged and pass; selection key is byte-identical (`:175-184`); the override path (`metadata_packet` passed non-`None`) skips discovery so `metadata_discovery_residuals` stays `()` (`:360-368`) — no discovery residual is fabricated when the caller supplies metadata. Clean.
- **Transcript-source discovery unchanged:** `transcript_sources_for_video` is untouched; its DataLakeRootError → `discovery_failed` source path (`:204-213`) and the two existing corruption/read-error tests (`test:286-358`) are unchanged and pass. Clean.
- **Completeness stays transcript-scoped; no metadata-completeness overstatement:** `behavioral_completeness.complete = rollup["status"] == "complete"` (`:340-344`), and `_extraction_rollup` derives `status` purely from transcript sources — the pre-existing `residuals` list is only appended to inside the rollup, never read into the status computation (`:501-567`). Metadata-discovery residuals therefore cannot change `complete`. The `complete is True` in the new test is honest: completion is documented as transcript-extraction-scoped (spec criterion 7 `:239-240`; commission fitness reference), and the metadata failure is surfaced via two residuals rather than hidden. Clean (see Open Question 1 on `status` vs `residuals`).
- **Corruption test exercises loadable-but-uninterpretable, not a `DataLakeRootError`:** verified decisively above against `load_raw_packet`'s size/sha guards. Clean.
- **Residual target-projection matches the transcript pattern; no new architecture:** the discovery-failed residual lands in the same per-video `behavioral_completeness.residuals` channel as transcript residuals, surfaced on the projected video even when the uninterpretable packet cannot prove its own video id — the documented transcript behavior (contract `:287`). No lane/global channel is introduced or claimed. Clean.
- **F3/F4/F5 not accidentally implemented or overconstrained:** verified above. Clean.
- **No unauthorized scope claims:** the diff adds no imports and no shared-core / IG-parity / live-capture / Cleaning / Judgment / scheduler / dashboard / production-runtime / buyer-proof reference. The no-runtime-imports contract test passes within the 29 (`test_youtube_behavioral_projection_no_runtime_imports.py`). Clean.

## Source-Read Ledger

Primary sources read at `codex/youtube-capture-spine-sync @ 3ffc251b`:

- Batch 4 commit `git show 3ffc251b` (file stat + full diff) and the focused base→HEAD diff of the two implementation targets — reviewed.
- `orca-harness/youtube_capture/behavioral_projection.py` — full read (implementation target).
- `orca-harness/tests/unit/test_youtube_behavioral_projection.py` — full read (implementation target).
- `orca-harness/data_lake/root.py` — targeted read of `find_packet` (`:791-795`), `load_raw_packet` (`:797-883`, esp. size/sha integrity guards `:861-881`), `list_available` (`:893-903`), and `DataLakeRootError` (`:106`).
- `orca-harness/source_capture/youtube_watch_packet.py` — targeted read of preserved-file naming (`CAPTURE_JSON_NAME` `:38`, `WATCH_HTML_NAME` `:37`, comment-page regex `:329`) to prove `_body_ending_with("youtube_watch_capture.json")` is unambiguous.
- `docs/review-outputs/youtube_behavioral_lake_metadata_bridge_advisory_code_review_v0.md` — full read (prior delegated review; F1/F2 accepted, F3/F4/F5 dispositions, minimum closure conditions). Excluded from findings.
- `docs/workflows/youtube_first_behavioral_completion_spec_v0.md` — targeted read (acceptance criteria `:219-247`, esp. criterion 5 named-residual `:234-237` and criterion 7 transcript-compat `:239-240`).
- The commission prompt — read in full from the worktree.
- Caller grep across the worktree (`metadata_packet_for_video` / `_watch_metadata_packet` / `project_youtube_behavioral_item` / importers of `behavioral_projection`).

Listed-but-not-line-read: `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md` (F3 context; relied on the prior review's verbatim citations `:94,:287-288` and confirmed the diff makes no contract-doc change). Not a material gap for the named axes.

## Validation Run Status

**Reproduced (not merely trusted).** Reviewer ran the prompt's focused command with `orca-harness` on `PYTHONPATH` (no `conftest.py`/`pytest.ini` present; imports resolve via that root):

```
tests/unit/test_youtube_behavioral_projection.py
tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py
tests/unit/test_source_capture_youtube_watch_packet.py
tests/unit/test_youtube_watch_runner_output_mode.py
tests/unit/test_youtube_caption_runner_output_mode.py
```

Observed: **29 passed in 1.74s** (exit 0) — matches the dispatcher-reported `29 passed`. The lane-adjacent `tests/contract/test_capture_runner_lake_seam_coverage.py` → **5 passed in 0.55s** (exit 0), matching the dispatcher-reported `5 passed`. The 29 = the prior Batch 3 review's reproduced **28 passed** + exactly one new test, corroborating that exactly one test was added and no existing test regressed. This is evidence the changed behavior is green; it is **not** a formal validation/readiness claim, and it does not exercise the three untested discovery-failure reasons in N1.

## Strict-Only Blockers / Not-Proven Boundaries

- No blocker-class or major defect found. No formal verdict, severity authority, approval, readiness, or pass/fail completion claim is issued (out of authority for this advisory commission).
- Strict-only (would require a bound review lane/packet/gate, absent here): overlay-bound severity taxonomy, patch-queue/executor handoff, mandatory-remediation, and pass/fail validation status. Named as strict-only blockers, not claimed.
- **Not proven:** behavior of the three untested discovery reasons — `missing_capture_json`, `capture_payload_not_object`, and the behavior-changing `missing_platform_video_id` (N1) — no test exercises them.
- **Not proven:** the mixed case (an uninterpretable packet co-existing with a healthy metadata packet for the projected video, where the discovery residual should appear *without* `youtube_metadata_packet_absent`). The code path supports it (`:297` guards on `metadata is None`) but no test asserts it.
- Not assessed (excluded by scope): IG parity, shared capture-core, live capture, transcript extraction quality, Cleaning/Judgment/scheduler/dashboard/production runtime, buyer-proof.

## Open Questions

1. Is it intended that `behavioral_completeness.status` reports `complete` (not `complete_with_residuals`) when a metadata-discovery residual is present? The patch preserves the pre-existing transcript-scoped status semantics — metadata residuals (including `youtube_metadata_packet_absent`, which already behaved this way pre-patch) do not flip `status`. A downstream consumer keying only on `status`/`complete` would not observe the metadata failure without reading `residuals`. If that is the intended contract, no change is needed; if not, the rollup status mapping (`:543-558`) would need to account for metadata residuals.
2. Should the **load-error** subclass of a watch packet (corrupt manifest / size or sha mismatch / unreadable bytes → `DataLakeRootError` swallowed at `:148-149`) also emit a *metadata*-channel residual? Today it is surfaced only via the transcript channel as `youtube_transcript_source_discovery_failed:<packet_id>:…`, which labels a metadata packet as a transcript source. This is pre-existing, explicitly outside the accepted F1 scope (the adjudication scoped F1 to *loadable-but-uninterpretable*), and **not** introduced or worsened by Batch 4 — raised only so the home model can decide whether the cross-channel labeling is acceptable or warrants a follow-up.

## Residual Risk

Low. The closure is narrow, target-projected, and faithful to the accepted F1/F2 scope; the public lookup shape, completeness scoping, latest-selection, override behavior, and transcript discovery are all preserved, and F3/F4/F5 are correctly left untouched. The concentrated residual is N1 (the behavior-changing `missing_platform_video_id` branch and two sibling reasons are unverified), plus the two pre-existing, out-of-scope channel/status questions above. None blocks the patch's stated purpose.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized. No patch, diff, exact edits, formal verdict, severity authority, patch queue, or no-new-seam claim is made (`NOT_CLAIMED`). De-correlation is a who-constraint: this review does not recommend, rank, or imply any runtime model choice.

## Provenance

```yaml
reviewed_by: Anthropic Claude (Opus 4.8) acting as delegated reviewer; operator to record acceptance
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery (reviewer lineage Anthropic; author lineage OpenAI/Codex — known, different upstream families)
same_vendor_rationale: not_applicable
```

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- Original commission: read-only adversarial code review of PR #440 Batch 4 — YouTube metadata-discovery residual closure of accepted findings F1/F2 (prompt: docs/prompts/reviews/youtube_metadata_discovery_residual_closure_adversarial_code_review_prompt_v0.md).
- Implementation context / diff / reviewed files: commit 3ffc251b over base 0c56ebe2 on codex/youtube-capture-spine-sync; behavioral_projection.py (split public metadata_packet_for_video from private _metadata_packet_for_video returning (packet, residuals); _watch_metadata_packet now returns classified reasons missing_capture_json / invalid_capture_json / capture_payload_not_object; new missing_platform_video_id residual; metadata_discovery_residuals threaded through project_youtube_behavioral_item[_from_lake]) and test_youtube_behavioral_projection.py (new _rewrite_preserved_body keeping manifest size/sha coherent + test_projection_from_lake_residualizes_uninterpretable_watch_metadata_packet). Context: data_lake/root.py (load_raw_packet size/sha integrity guards), source_capture/youtube_watch_packet.py (preserved-file naming), the prior Batch 3 review, the completion spec.
- Findings + evidence: Accepted F1 CLOSED as accepted (uninterpretable-but-loadable watch packets now emit youtube_metadata_packet_discovery_failed:<id>:<reason> AND co-present youtube_metadata_packet_absent; metadata_capture is None; reuses existing per-video residual channel, no lane/global architecture). Accepted F2 CLOSED as accepted (real lake-backed test exercises the loadable-but-uninterpretable subclass; proven distinct from DataLakeRootError because invalid_capture_json is only reachable post-load and load_raw_packet fail-closes on size/sha mismatch). F3/F4/F5 correctly not implemented or overconstrained. One new advisory finding N1 (Minor): three of four new discovery-failure reasons are untested, most materially the behavior-changing missing_platform_video_id branch (previously a silent skip). Axes for public lookup shape, no-absent-laundering, healthy/latest/override discovery, transcript intactness, transcript-scoped completeness, corruption-test authenticity, residual target-projection, F3/F4/F5 non-implementation, and no-unauthorized-claims all checked clean.
- Proposed patch / diff / exact edits: NOT_CLAIMED (read-only commission).
- Citations: file:line anchors throughout; primary sources in the source-read ledger.
- Reviewer verdict: NOT_CLAIMED (advisory findings only; no approval/readiness/severity authority).
- Validation evidence / not-run: reproduced focused pytest = 29 passed (exit 0) and lane-adjacent seam = 5 passed (exit 0); 29 = prior 28 + 1 new test, no regression; the three untested N1 reasons and the mixed-case path are not exercised.
- Residual risk: low, concentrated in N1 plus two pre-existing out-of-scope questions (status-vs-residuals semantics; load-error subclass surfaced only via the transcript channel).
- Blockers / off-scope / not-proven: no blocker-class defect; missing_platform_video_id / missing_capture_json / capture_payload_not_object branches and the mixed-case path are not proven; IG/shared-core/live/Cleaning/Judgment/runtime excluded by scope.
```
