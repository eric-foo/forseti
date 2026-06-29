# Capture Runner Lake + Metric Truth — Advisory Code Review v0 (PR #440, Batch 1 + Batch 2)

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Advisory code review output for the Batch 1 + Batch 2 capture enforcement patch on
  PR #440: packet-runner lake seam / output-mode exclusivity contract, YouTube caption
  runner output-mode behavior, and YouTube watch metric-receipt truth / no-zero-fill
  enforcement.
use_when:
  - Adjudicating the delegated adversarial code review findings for the Batch 1 + Batch 2 patch.
  - Checking the review evidence behind the capture-runner storage and metric-truth enforcement.
authority_boundary: retrieval_only
```

```yaml
review_artifact: Capture runner lake + metric truth (Batch 1 + Batch 2) — advisory code review
commission_source: docs/prompts/reviews/capture_runner_lake_metric_truth_adversarial_code_review_prompt_v0.md
review_lane: read-only workflow-code-review (adversarial posture), zero-config findings-only advisory
pr: 440
branch: codex/youtube-capture-spine-sync
review_base: 03cefbe4bc4a8ad4934458c07a8aab1522af30a0
worktree_head_at_review: af1aa9b444841bae35278ec2af715a77d07e3dca
output_mode: filesystem-output
required_output_path: docs/review-outputs/capture_runner_lake_metric_truth_advisory_code_review_v0.md
reviewed_by: Claude (Anthropic), Opus 4.8 — claude-opus-4-8
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery (reviewer lineage Anthropic != author lineage OpenAI/Codex)
same_vendor_rationale: not_applicable (cross-vendor; same-vendor sanity not claimed)
non_claims: [no formal verdict, no severity authority, no readiness/approval, no validation pass/fail authority,
             no patch queue, no executor-ready handoff, no runtime model recommendation,
             no no-new-seam claim, no transcript/Cleaning/Judgment claim]
```

## Review Frame

- **Commission**: read-only adversarial review of the Batch 1 + Batch 2 capture enforcement patch on
  PR #440. The prompt routed from `workflow-delegated-review-patch` but was explicitly downgraded to a
  read-only `workflow-code-review` commission: no patch execution, patch queue, formal verdict,
  readiness claim, runtime-model recommendation, or no-new-seam claim is authorized.
- **Two contracts under review**:
  - **Batch 1 (storage/runner)** — packet-producing runners expose a data-lake seam, forward
    `data_root`, and keep `--output` local mode mutually exclusive with `--data-root`/`ORCA_DATA_ROOT`
    lake mode; the contract test detects thin packet-writer wrappers.
  - **Batch 2 (metric truth)** — YT watch metric observations must come from complete metric receipts;
    missing/hidden metrics must be explicit unavailable postures, never fallback observed values or
    zero-looking rollups.
- **Source-loading mode**: zero-config findings-only advisory review. No overlay verdict vocabulary,
  severity taxonomy, validation-gate authority, or patch-queue routing was bound into this lane; those
  are named below as strict-only blockers. Findings are decision input only.
- **Trigger gate**: explicit `workflow-code-review` commission with a repo-visible implementation diff →
  PASS.
- **Output binding**: `filesystem-output` with a bound `required_output_path` (this file) → satisfied.
- **Excluded from target** (per prompt): this review prompt artifact, unrelated IG acquisition route
  changes, shared IG/YT capture-core architecture or route unification, live YouTube/Instagram probing,
  and transcript-quality / Cleaning / Judgment / scheduler / dashboard / production-runtime / buyer-proof
  claims.

## Source-Loading Declaration

`SOURCE_CONTEXT_READY`.

All five implementation targets and all seven context-only sources were read at the pinned worktree, plus
the Batch 1 + Batch 2 diff for every changed file (`git diff 03cefbe4 -- …`) and the live fetcher
`youtube_capture/capture_youtube_v0.py` (context-only in the prompt; read in full because Batch 2 makes
the writer hard-reject incomplete receipts, so whether the real producer emits complete receipts is
material). Targets: `tests/contract/test_capture_runner_lake_seam_coverage.py`,
`runners/run_source_capture_youtube_caption_packet.py`, `source_capture/youtube_watch_packet.py`,
`tests/unit/test_source_capture_youtube_watch_packet.py`,
`tests/unit/test_youtube_caption_runner_output_mode.py`. Context: `runners/run_source_capture_youtube_watch_packet.py`,
`source_capture/models.py`, `source_capture/packet_assembly.py`, `source_capture/transcript/caption_packet.py`,
`youtube_capture/capture_youtube_v0.py`, and the prior review prompt + output. No material source gap for the
findings below.

## Validation Run Status

`validation_run` — reran the dispatcher's focused command at the pinned worktree:

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider \
  tests/contract/test_capture_runner_lake_seam_coverage.py \
  tests/unit/test_source_capture_youtube_watch_packet.py \
  tests/unit/test_youtube_caption_runner_output_mode.py \
  tests/unit/test_youtube_capture_metadata_helpers.py \
  tests/unit/test_youtube_capture_view_count.py \
  tests/unit/test_youtube_behavioral_projection.py
```

Observed: **33 passed in 2.02s, exit 0** — matches the dispatcher's `33 passed`.

Two additional standalone repros were run against the verbatim PR code (read-only; evidence, not a gate):

- **F1 repro** — confirms the writer's stale/mismatch/unsupported-posture rejection branches fire:
  - observed receipt value `1200` vs engagement `9999` → `code=5`, no dir, `"…value 1200 does not match engagement value 9999"`.
  - unavailable receipt while `engagement.like_count=34` → `code=5`, no dir, `"like_count has engagement value 34 but metric receipt posture is 'unavailable_with_reason'"`.
  - posture `not_applicable` → `code=5`, no dir, `"…has unsupported posture 'not_applicable'"`.
  - control: untouched valid packet → `code=0`, dir written.
- **F2 repro** — fed the contract test's own detector a synthetic runner: `import source_capture.youtube_watch_packet as ywp` + `ywp.write_youtube_watch_packet(…, data_root=root)` → **0 producer calls detected**; the from-import form → 1 detected.

`git diff --check` was not rerun by me (`validation_not_run` for that specific check; the dispatcher reported only a line-ending warning — immaterial to code correctness).

---

## Findings (ordered by materiality)

### F1 — The Batch 2 "stale/mismatch metric receipt" rejection is correct but has no test; a regression that dropped it would pass the 33-test suite

- **commissioned_target_and_purpose**: metric-truth enforcement — "Whether the writer correctly rejects
  stale/mismatched metric receipt values rather than silently using `engagement` fallbacks" (review axis
  6), a named load-bearing Batch 2 behavior.
- **reviewed_target / artifact_role**: `source_capture/youtube_watch_packet.py` packet writer (Batch 2
  implementation target) + `tests/unit/test_source_capture_youtube_watch_packet.py` (Batch 2 test target).
- **anchor**: `youtube_watch_packet.py:257`–`260` (observed value vs `engagement_value` mismatch raise),
  `:263`–`266` (non-observed posture while `engagement_value is not None` raise), `:267`–`268`
  (unsupported-posture raise). No corresponding assertion exists in
  `test_source_capture_youtube_watch_packet.py` (the rejection tests there cover only `:233`
  missing-receipt, `:255`–`256` incomplete-observed, `:274`–`275` missing-`routes_checked`).
- **implementation_evidence**: standalone repro on verbatim PR code (see Validation Run Status): all three
  branches return `code=5` with their distinct messages and write no directory; a control valid packet
  writes (`code=0`). The full test file was read end-to-end — no test references the substrings
  `does not match engagement value`, `has engagement value`, or `unsupported posture`. These three
  branches are reachable, working, and unasserted.
- **authority_or_evidence_basis**: source + standalone repro + full read of the test file.
  `source_capture/models.py:128`–`136` / `:183`–`198` names "absence … never stored as an observed value"
  as the single irreversible lock-in; the mismatch guards are precisely the code that stops a stale
  `engagement` value from overriding (or contradicting) a typed receipt, so they are load-bearing for the
  metric-truth claim — yet they are the part with no red-green proof.
- **impact** (review-confidence, validation): "33 passed" does **not** bound the stale/mismatch rejection
  that Batch 2's value proposition rests on. A refactor that removed the `engagement_value != value`
  check, or relaxed the unavailable-with-stale-value check back toward the pre-patch `engagement`
  fallback, would be green. This is the most direct gap between what the patch claims to enforce and what
  the tests prove.
- **minimum_closure_condition**: add unit tests that (a) build an observed receipt whose value differs
  from `engagement[metric]` and assert `code=5` + the mismatch message + `not output.exists()`; (b) build
  an `unavailable_with_reason` receipt while `engagement[metric]` still carries an int and assert `code=5`
  + that message; optionally (c) an unsupported posture asserts `code=5`. Each fails against pre-patch
  fallback behavior and passes against this patch.
- **next_authorized_action**: report only (advisory). Test authoring is owner/implementer-routed; this
  lane is read-only.
- **verification_expectation**: same-check red-green is cheap and available — the three repro fixtures
  above are the test bodies; they fail against the pre-Batch-2 `engagement`-fallback writer and pass
  against the patched writer.
- **patch_queue_entry authorized**: no.

### F2 — The lake-seam/exclusivity detector is a source-token heuristic; an `import module` + attribute-call wrapper is fully invisible (escapes both seam and exclusivity), so the docstring's "thin wrappers cannot bypass" is overstated

- **commissioned_target_and_purpose**: "Whether `test_capture_runner_lake_seam_coverage.py` now detects
  thin source-capture packet writer wrappers … without accidentally classifying non-packet … runners"
  and "Whether the widened lake-seam detector still protects every packet-producing runner" (review axes
  1–2).
- **reviewed_target / artifact_role**: `tests/contract/test_capture_runner_lake_seam_coverage.py`
  (Batch 1 contract test).
- **anchor**: `_imported_packet_writer_names` (`:110`–`121`) collects names only from `ast.ImportFrom`
  nodes whose module starts with `source_capture`; `_producer_calls` (`:124`–`139`) matches
  `_call_name` against that set. The module docstring (`:8`–`11`) asserts new thin wrappers
  "cannot bypass the seam contract just because they do not call `stage_and_write_packet` directly."
- **implementation_evidence**: fed the detector a synthetic runner using
  `import source_capture.youtube_watch_packet as ywp` then `ywp.write_youtube_watch_packet(…, data_root=root)`
  → **0 producer calls detected** (writer_names empty beyond the direct tokens), because `import … as`
  is an `ast.Import`, not `ast.ImportFrom`, so the wrapper name is never registered; the from-import form
  → 1 detected. A runner using the import-module idiom would not be seen as a packet producer at all, so
  it escapes **both** `test_every_packet_runner_is_lake_wired_or_acknowledged` **and**
  `test_packet_runner_output_modes_are_exclusive`. Two further heuristic seams in the same detector:
  `_EXPLICIT_PAIR_REJECT_TOKENS` includes the bare substring `add_mutually_exclusive_group`
  (`:31`), so an unrelated mutually-exclusive group elsewhere in a runner satisfies
  `rejects_output_and_data_root` regardless of which args are grouped; and all exclusivity/env tokens are
  exact source-string matches (`:23`–`31`), so a behaviorally-correct runner that phrases the env-fallback
  or rejection differently would false-positive-**fail** `test_packet_runner_output_modes_are_exclusive`,
  while the magic string sitting in a comment would false-negative-**pass**.
- **authority_or_evidence_basis**: source + standalone repro against the detector itself. The two real
  in-scope runners both use the from-import idiom and real exclusivity logic, so the current suite is
  honest for them; this finding bounds the **durability** of the guard, not its correctness today.
- **impact** (review-confidence): the contract test proves the presence of specific source tokens, not
  the presence of behavior. Its stated robustness goal ("thin wrappers cannot bypass") holds only for the
  from-import idiom; the "enforced version of the manual survey" is one non-idiomatic import style away
  from silently under-counting producers. No current runner is affected.
- **minimum_closure_condition**: either (a) tighten the claim — document that detection assumes the
  from-import idiom and exact exclusivity phrasing — or (b) strengthen detection (resolve `ast.Import` +
  attribute access; treat `add_mutually_exclusive_group` as evidence only when the grouped args are
  `--output`/`--data-root`; back the token checks with at least one behavioral test per runner, see F3).
- **next_authorized_action**: report only (advisory).
- **verification_expectation**: red-green available — a unit test over a synthetic import-module runner
  asserting it is detected as a producer fails today and passes after detection is hardened.
- **patch_queue_entry authorized**: no.

### F3 — The watch runner's `main()` output-mode exclusivity is asserted only by the source-token detector, not by a behavioral test (the caption runner got one; the watch runner did not)

- **commissioned_target_and_purpose**: "Whether the new output-mode exclusivity check catches both
  explicit `--output + --data-root` ambiguity and env fallback overriding explicit `--output`" (review
  axis 3) — for every packet runner, not just the caption runner.
- **reviewed_target / artifact_role**: `runners/run_source_capture_youtube_watch_packet.py` (Batch 1
  context target) vs `tests/unit/test_youtube_caption_runner_output_mode.py` (Batch 1 test target).
- **anchor**: caption runner exclusivity is behaviorally tested
  (`test_youtube_caption_runner_output_mode.py:12`–`50`: dual-reject exit 2 before fetch; env ignored
  when `--output` explicit). The watch runner's equivalent `main()` logic
  (`run_source_capture_youtube_watch_packet.py:82`–`94`: dual-reject, neither-reject, env-gated-on-output-omitted)
  has no behavioral test — `test_youtube_watch_runner_can_commit_to_data_lake`
  (`test_source_capture_youtube_watch_packet.py:225`–`252`) exercises the **inner**
  `run_source_capture_youtube_watch_packet(...)` with `data_root` only, never the arg-parsing exclusivity.
- **implementation_evidence**: traced the watch runner `main()` across all six arg combinations — the
  logic is correct (dual `--output --data-root` exits 2 via both the mutually-exclusive group and the
  explicit check; `ORCA_DATA_ROOT` is gated on `args.output is None`). But correctness is established here
  by reading, not by a test; the only automated assertion over it is F2's substring detector.
- **authority_or_evidence_basis**: source trace + the test inventory (full read of both test files).
- **impact** (review-confidence, coverage asymmetry): a Batch 1 behavior the prompt calls out is
  behaviorally proven for one of the two patched runners and token-only for the other. A regression in the
  watch runner's env-gating (e.g. dropping the `args.output is None` guard so `ORCA_DATA_ROOT` overrides an
  explicit `--output`) would still pass the suite as long as the magic substrings remain present.
- **minimum_closure_condition**: add a behavioral test for the watch runner `main()` mirroring the caption
  runner's two cases (dual-reject exit 2; env ignored when `--output` explicit), using a monkeypatched
  fetcher/writer so no network is required.
- **next_authorized_action**: report only (advisory).
- **verification_expectation**: red-green available — the new test fails if the watch runner's exclusivity
  guards are removed and passes as written.
- **patch_queue_entry authorized**: no.

---

## Risks / Residual Observations (not findings — scoping clarity or carried-forward lower-confidence)

- **R1 — Batch 2 enforces receipt completeness/consistency, not extraction correctness.** The writer
  accepts any structurally-complete `observed` receipt whose value matches `engagement`. It cannot detect
  that the value itself is wrong. Concretely, the prior review's R1 stands: `extract_view_count`'s regex
  fallback `first(r'"viewCount":"([0-9]+)"', html)` (`capture_youtube_v0.py:190`) can return a
  recommended/related video's count and stamp it `observed` with `source_route=served_html.regex`; Batch 2
  faithfully preserves it. "Metric truth" here means "every metric carries a complete, engagement-consistent
  typed receipt," which is narrower than "every observed value is correct." Worth stating so the contract
  is not over-read. `capture_youtube_v0.py` is context-only and outside this patch's target scope.
- **R2 — `comment_sample_count = observed: 0` co-exists with `comments_state = comments_not_exposed`.**
  In the fetcher's reachable-but-empty branch (`capture_youtube_v0.py:455`,`:464`–`468`), `got == []` yields
  `comments_state = comments_not_exposed` **and** an `observed` `comment_sample_count` receipt with value 0;
  the Batch 2 writer accepts it (value 0 matches `engagement` 0; the slice still carries a
  `comments_state:comments_not_exposed` limitation). Defensible as "we sampled and observed zero rows," but
  it is a zero-looking observed value that the metric-truth contract does **not** reject — a mixed signal a
  downstream reader could misread. Carried from the prior review's R2; Batch 2 does not adjudicate it.
- **R3 — The writer narrows accepted postures to `{observed, unavailable_with_reason}`; the model supports
  five.** `youtube_watch_packet.py:267`–`268` raises "unsupported posture" for `out_of_capture_window` /
  `not_attempted` / `not_applicable`, which `MetricPosture` (`models.py:138`–`143`) permits. No current
  producer emits them, so nothing breaks today, but a future surface that legitimately needs (e.g.)
  `not_applicable` for `total_comment_count` would be rejected until the writer is widened — a latent
  forward-constraint, not a current defect.
- **R4 — The contract test's exact-token coupling applies repo-wide, to every `run_*.py` packet producer,
  not just the two in scope.** A future correct runner that phrases exclusivity differently would fail
  `test_packet_runner_output_modes_are_exclusive` (false-positive failure). Currently all producers pass
  (33 green), so no live breakage; flagged as a maintenance coupling that grows with each new runner.
- **R5 — `--comment-pages > 99` aborts the packet write** (pre-existing). Page filenames are
  `youtubei_next_page_{n:02d}.json` and `_validate_comment_page` (`youtube_watch_packet.py:328`–`332`)
  requires exactly two digits, so a 100th page raises `ValueError`. Edge only (default 2). Unchanged by this
  patch; noted for completeness.

## Strict-Only Blockers and Not-Proven Boundaries

- No overlay review-lane id, verdict vocabulary, severity taxonomy, validation-gate semantics, or
  patch-queue routing was bound into this lane → strict formal review, formal verdict, severity authority,
  and any pass/fail or readiness claim are **blocked / not authorized** (by prompt design).
- The prior review's **F1** (`detect_video_state` login/region ordering, `capture_youtube_v0.py:279`–`310`)
  and **F2** are **outside this patch's target scope**. Note on F2: on this branch
  `parse_exact_count_text` (`capture_youtube_v0.py:247`–`264`) now carries explicit decimal and K/M/B guards
  (`:253`–`256`), so the prior abbreviated-text truncation no longer reproduces — the prior F2 appears
  remediated on this branch (observed by reading; not re-attacked here as it is out of the Batch 1+2 target).
- The integration claim "the real fetcher always satisfies the writer's new hard requirement" is **proven
  from source**: `fetch_youtube_watch` (`capture_youtube_v0.py:326`–`508`) sets complete `metric_receipts`
  for all four metrics in every comments branch (no-token, api-key, no-api-key) and unconditionally for
  view/like (`:366`–`383`), with `source_route`/`source_path`/`artifact` for observed and `routes_checked`
  for unavailable — so the writer's rejection path is not triggered on real captures. **Not proven against a
  live probe** (none authorized): that real served HTML/youtubei responses populate these as modeled.
- The implied-authority axis (no unauthorized transcript/Cleaning/Judgment/buyer-proof claim) is assessed
  from code only and is clean: `YOUTUBE_WATCH_NON_CLAIMS` (`youtube_watch_packet.py:41`–`53`) and
  `CAPTION_NON_CLAIMS` (`caption_packet.py:30`–`37`) explicitly disclaim those lanes. **Not proven** against
  any doctrine doc (none was in this prompt's context list).

## Open Questions

1. Is `comment_sample_count = observed: 0` (reachable-but-empty comments) the intended reading, or should
   that case be `unavailable_with_reason`? Batch 2 does not decide it (R2).
2. Is the writer's narrowing to two postures intentional for v0, or should `not_applicable` /
   `out_of_capture_window` be accepted for forward surfaces (R3)?
3. Is the seam detector's reliance on the from-import idiom + exact exclusivity phrasing considered
   sufficient, or should detection be hardened against import-module wrappers and unrelated
   mutually-exclusive groups (F2)?

## Residual Risk

The metric-truth writer logic and the caption runner exclusivity logic are correct (traced exhaustively and
exercised by the 33-test suite plus standalone repros), and the widened seam detector correctly follows
imported `write_*_packet` wrappers for the from-import idiom the real runners use. Residual risk concentrates
in **proof, not behavior**: the stale/mismatch rejection that is Batch 2's reason to exist has no test (F1);
the seam/exclusivity guard is a source-token heuristic whose "cannot bypass" claim is one import style from
under-counting (F2); and the watch runner's exclusivity is token-asserted, not behavior-tested (F3). Plus a
scoping caveat: "metric truth" guarantees receipt completeness/consistency, not extraction accuracy (R1) and
does not adjudicate the observed-0 sample case (R2). None of these block owner review; they bound how far the
patch's green suite actually proves its claims and what "trustworthy" currently covers.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, readiness, mandatory remediation,
or executor-ready patch authority, and they confer no severity or runtime-model authority, until separately
accepted or authorized by the owning lane. `patch_queue_entry` is `no` for every finding in this prompt.

## Source-Read Ledger

| Source | Path | Mode |
| --- | --- | --- |
| Lake-seam contract test (target) | `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py` | full + Batch 1 diff |
| Caption runner (target) | `orca-harness/runners/run_source_capture_youtube_caption_packet.py` | full + Batch 1 diff |
| Watch packet writer (target) | `orca-harness/source_capture/youtube_watch_packet.py` | full + Batch 2 diff |
| Watch packet tests (target) | `orca-harness/tests/unit/test_source_capture_youtube_watch_packet.py` | full + Batch 2 diff |
| Caption output-mode test (target) | `orca-harness/tests/unit/test_youtube_caption_runner_output_mode.py` | full (new file) |
| Watch runner (context) | `orca-harness/runners/run_source_capture_youtube_watch_packet.py` | full |
| Packet models (context) | `orca-harness/source_capture/models.py` | full |
| Stage/assemble helper (context) | `orca-harness/source_capture/packet_assembly.py` | full |
| Caption packet writer (context) | `orca-harness/source_capture/transcript/caption_packet.py` | full |
| Live fetcher (context) | `orca-harness/youtube_capture/capture_youtube_v0.py` | full |
| Prior review prompt (context) | `docs/prompts/reviews/youtube_watch_source_capture_adversarial_code_review_prompt_v0.md` | full |
| Prior review output (context) | `docs/review-outputs/youtube_watch_source_capture_advisory_code_review_v0.md` | full |
| Batch 1 + Batch 2 diff | `git diff 03cefbe4 -- orca-harness/{the 5 files}` | full |

Evidence captured this pass: focused pytest rerun = 33 passed (exit 0); standalone repro of F1's three
rejection branches (code=5, no dir) + control valid packet (code=0); detector repro for F2 (import-module
wrapper → 0 detected, from-import → 1).

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- original commission or review target: read-only adversarial code review of the Batch 1 + Batch 2 capture
  enforcement patch on PR #440 (packet-runner lake seam / output-mode exclusivity; YouTube caption runner
  output mode; YouTube watch metric-receipt truth / no-zero-fill). Target = the 5 implementation/test files
  listed in the commissioning prompt; this prompt downgraded delegated-review-patch to read-only
  workflow-code-review (no patch execution/queue/verdict/readiness/no-new-seam claim authorized).
- implementation context, diff, and reviewed files: branch codex/youtube-capture-spine-sync, review base
  03cefbe4, worktree HEAD af1aa9b4. Batch diff = 5 files, +282/-59: watch packet writer (metric-receipt
  hard-rejection + posture-summary visible_mode_change), caption runner (output-mode exclusivity), contract
  test (widened detector + new exclusivity test), watch packet test (3 new rejection tests), new caption
  output-mode test. Also read context: watch runner, models.py, packet_assembly.py, caption_packet.py, the
  live fetcher capture_youtube_v0.py, and the prior review prompt+output.
- findings and implementation evidence:
  - F1 (highest): the Batch 2 stale/mismatch/unsupported-posture rejection (youtube_watch_packet.py:257-268)
    is correct and reproduced (code=5, no dir) but has NO test in test_source_capture_youtube_watch_packet.py;
    the 33-green suite would stay green if those guards regressed to the pre-patch engagement fallback. This
    is the named load-bearing Batch 2 behavior (review axis 6). Cheap same-check red-green available.
  - F2: the seam/exclusivity detector (test_capture_runner_lake_seam_coverage.py) is a source-token
    heuristic. Reproduced: an `import module` + attribute-call packet-writer wrapper is detected as 0
    producers (escapes both seam and exclusivity), while the from-import form is detected as 1; the docstring
    "thin wrappers cannot bypass" holds only for the from-import idiom. Also: bare `add_mutually_exclusive_group`
    substring satisfies the reject token regardless of which args are grouped, and exact-string exclusivity
    tokens can false-positive-fail / comment-false-negative-pass. No current runner affected (both use
    from-import + real logic); bounds the guard's durability.
  - F3: the watch runner main() output-mode exclusivity (run_source_capture_youtube_watch_packet.py:82-94) is
    asserted only by F2's substring detector, not behaviorally — the caption runner got a behavioral test
    (test_youtube_caption_runner_output_mode.py) and the watch runner did not (its only test exercises the
    inner function with data_root). Logic traced correct; coverage asymmetric.
  - Risks R1-R5: Batch 2 enforces receipt completeness/consistency not extraction correctness (prior R1
    regex-grabbed viewCount still stamped observed); comment_sample_count=observed:0 vs comments_not_exposed
    accepted (R2); writer narrows to 2 of 5 postures (R3); contract-test exact-token coupling is repo-wide
    (R4); >99 comment-pages aborts write (R5, pre-existing).
- proposed patch, diff, or exact requested edits: NOT_CLAIMED (read-only commission).
- citations: file:line anchors above; standalone repro of F1 (3 rejection branches + control) and F2
  (detector import-style) from verbatim PR code; full read of both test files for the coverage claims.
- reviewer verdict: NOT_CLAIMED as a formal verdict. Advisory read: the metric-truth writer and caption
  exclusivity logic are correct and the real fetcher satisfies the new hard contract; residual risk is in
  proof coverage (F1/F3) and detector durability (F2), plus scoping clarity on what "metric truth" covers
  (R1/R2). None blocks owner review.
- validation evidence and not-run checks: focused pytest rerun = 33 passed, exit 0 (matches dispatcher).
  Standalone repros as above. git diff --check not rerun (validation_not_run; dispatcher saw only a
  line-ending warning). No live YouTube probe (not authorized).
- residual risk: a green suite that does not bound Batch 2's stale/mismatch rejection (F1) or the watch
  runner exclusivity (F3); a seam guard one import style from under-counting producers (F2); "metric truth"
  read more broadly than receipt completeness/consistency (R1/R2).
- blockers, off-scope flags, and not-proven boundaries: no overlay verdict/severity/patch-queue lane bound
  (strict claims blocked by design); prior F1/F2 (capture_youtube_v0.py) are off this patch's target scope —
  prior F2 appears remediated on-branch via parse_exact_count_text decimal/K-M-B guards (observed, not
  re-attacked); "real served HTML populates receipts as modeled" not proven without a live probe;
  implied-authority axis assessed from code only (clean non-claims), not proven against doctrine docs.
- provenance: reviewed_by Claude (Anthropic) Opus 4.8 — claude-opus-4-8; authored_by OpenAI/Codex GPT-5;
  de_correlation_bar cross_vendor_discovery; same_vendor_rationale not_applicable.
```

For this prompt, `proposed patch`, `diff`, `exact requested edits`, formal verdict, severity authority,
readiness, approval, validation pass/fail, and patch queue are `NOT_CLAIMED` unless a later owner
instruction binds them.
