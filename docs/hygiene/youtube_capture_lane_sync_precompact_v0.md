# Pre-Compact Checkpoint

## Current objective

Precompact before starting the next goal: sync the current YouTube metadata/comments/availability capture lane into the broader `source_capture` spine, without forcing shared acquisition machinery. The next work should make YouTube watch-page metadata/comments a first-class capture adapter/output with explicit availability states, metric route receipts, no zero-filling, and downstream creator-ledger trustability.

## Current state

- What has been completed:
  - PR #432 is merged. Verified with `gh pr view 432`: state `MERGED`, merge commit `658ac473c2164bc3f4da4840ee80c3f568733d03`, merged at `2026-06-28T18:26:36Z`, head OID `5afa46609549d384235ffc9072680f44919e933b`.
  - `git fetch origin` updated `origin/main` from `820165fe` to `493ba1d861afdef977fabe2a241eb69db4d8a147`.
  - `git merge-base --is-ancestor 658ac473c2164bc3f4da4840ee80c3f568733d03 origin/main` confirmed the PR #432 merge commit is contained in `origin/main`.
  - YouTube behavioral contract and IG start handoff from PR #432 are now on `origin/main`.
  - Source split was checked: YouTube caption and ASR transcript capture are already under `source_capture/transcript`; YouTube watch-page metadata/comments capture still lives under legacy-adjacent `youtube_capture/`.
- What is partially completed:
  - YouTube behavioral projection exists and bridges legacy metadata/comment packet shapes plus transcript packet anchors. It does not acquire data.
  - The existing YouTube watch-page runner extracts useful metadata/comments, but it is not yet a first-class `source_capture` adapter with posture-state and route-receipt discipline.
- What is currently broken or uncertain:
  - Root workspace is on `codex/ig-reels-capture-spine` with many unrelated untracked files. Do not start the next implementation from that dirty root.
  - The PR #432 worktree is clean but is now a merged PR branch, not the best base for new work. Start a fresh branch/worktree from updated `origin/main`.
  - Need source refresh before editing because the root branch lacked some merged files; rely on `origin/main` or a fresh worktree, not root branch state.

## Important files and symbols

- `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
  - Relevant functions/classes/components: N/A, workflow record.
  - Current role in the task: source-backed contract for YouTube behavioral projection semantics after PR #432.
  - Important changes or observations: now merged to `origin/main`; use as behavior reference, not acquisition recipe.
- `docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md`
  - Relevant functions/classes/components: N/A, workflow handoff packet.
  - Current role in the task: IG start handoff from PR #432; useful context, but next goal is YT capture sync first.
  - Important changes or observations: says compare behavior, not machinery; re-read named load-bearing sources.
- `orca-harness/youtube_capture/capture_youtube_v0.py`
  - Relevant functions/classes/components: `ytinit`, `ytplayer`, `comment_panel_token`, `youtubei_next`, `player_view_count`, `extract_view_count`.
  - Current role in the task: incumbent watch-page metadata/comments capture logic to migrate or wrap into `source_capture`.
  - Important changes or observations: extracts `ytInitialPlayerResponse`, uses `youtubei/v1/next`, gets `view_count`, `view_count_source_path`, `like_count_text`, `comment_count_text`, comments sample, sampled comment likes/replies; current posture collapses missing comment token to `disabled`, which is too blunt.
- `orca-harness/youtube_capture/shorts_scroll_capture_v0.py`
  - Relevant functions/classes/components: imports helpers from `capture_youtube_v0.py`.
  - Current role in the task: Shorts-specific incumbent capture path; inspect before changing shared helper behavior.
  - Important changes or observations: likely shares the same incomplete comments posture semantics.
- `orca-harness/youtube_capture/behavioral_projection.py`
  - Relevant functions/classes/components: `normalize_youtube_metadata_packet`, `transcript_sources_for_video`, `project_youtube_behavioral_item`.
  - Current role in the task: projection layer over already-captured inputs.
  - Important changes or observations: docstring says it deliberately does not acquire anything; normalizes `view_count`, `view_count_source_path`, `like_count_text`, `comments_posture`, `comment_count_text`, sample comments, transcript sources, and extraction rollups.
- `orca-harness/source_capture/transcript/caption_packet.py`
  - Relevant functions/classes/components: `write_caption_packet`.
  - Current role in the task: already-on-capture-rails YouTube caption transcript packet writer.
  - Important changes or observations: writes `SourceCapturePacket`; `source_surface="youtube_captions"`.
- `orca-harness/source_capture/transcript/asr_packet.py`
  - Relevant functions/classes/components: `write_asr_transcript`.
  - Current role in the task: already-on-capture-rails YouTube audio ASR packet and derived transcript writer.
  - Important changes or observations: writes `SourceCapturePacket`; `source_surface="youtube_audio"`; derived transcript is under data lake, not capture preserved bytes.
- `orca-harness/runners/run_source_capture_youtube_caption_packet.py`
  - Relevant functions/classes/components: CLI wrapper for caption packet.
  - Current role in the task: existing runner pattern for source-capture YouTube transcript capture.
  - Important changes or observations: public caption capture into SourceCapturePacket.
- `orca-harness/runners/run_source_capture_youtube_asr_packet.py`
  - Relevant functions/classes/components: CLI wrapper for audio ASR packet.
  - Current role in the task: existing runner pattern for source-capture YouTube ASR fallback.
  - Important changes or observations: data-lake mode only, public data only.
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - Relevant functions/classes/components: capture-method playbook.
  - Current role in the task: required read before live/source capture activity.
  - Important changes or observations: load before any live YouTube probe; network/tool escalation still applies.

## Decisions made

- Decision: Sync YouTube metadata/comments into `source_capture`; do not treat the current legacy runner as already fully synced.
  - Reason: transcript capture is already on capture rails, but watch-page metadata/comments are still under `youtube_capture/` with lean packets and weaker posture semantics.
  - Consequence: next patch should focus on a platform-specific YouTube metadata/comments capture adapter or packet writer, not transcript rails.
- Decision: Use platform-specific route receipts and availability states rather than one shared acquisition ladder.
  - Reason: user explicitly wants behavior similarity without enforcing acquisition method, priority, shape, or route.
  - Consequence: preserve `ytInitialPlayerResponse`, `microformat`, `youtubei_next`, rendered-browser if used, etc. as metric source routes.
- Decision: No zero-filling.
  - Reason: hitting a video page does not guarantee total comment count, likes, comments token, or every metric.
  - Consequence: distinguish `comments_disabled` from `comments_not_exposed`; distinguish sample count from total count; keep absent as absent with reason.
- Decision: Start next implementation from fresh `origin/main`, not the root workspace or merged PR branch.
  - Reason: root worktree is dirty and stale relative to merged files; PR #432 is merged and should be consumed through `origin/main`.
  - Consequence: create a fresh worktree/branch for the sync work.

## Superseded / Ignore

- Prior instruction, idea, artifact, or finding: "YouTube lane is fully in capture lane already."
  - Why superseded: source check shows only caption/ASR transcript capture is under `source_capture`; metadata/comments are still under `youtube_capture/`.
  - Current replacement: treat YouTube as partially synced; sync watch-page metadata/comments/availability next.
- Prior instruction, idea, artifact, or finding: old PR #432 branch as working surface.
  - Why superseded: PR #432 is merged.
  - Current replacement: start from updated `origin/main` at or after `493ba1d861afdef977fabe2a241eb69db4d8a147`.
- Prior instruction, idea, artifact, or finding: comment-token absence means comments disabled.
  - Why superseded: user correctly pushed that route non-exposure and disabled comments are different states.
  - Current replacement: add explicit states such as `comments_disabled`, `comments_not_exposed`, `comments_sample_captured`.

## Commands and results

- Command:
  ```bash
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: root is `codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine` with many unrelated untracked files.
- Command:
  ```bash
  git -C .codex/worktrees/youtube-contract-review-adjudication status --short --branch
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: PR #432 worktree clean on `codex/youtube-contract-review-adjudication`.
- Command:
  ```bash
  gh pr view 432 --json number,state,isDraft,mergedAt,mergeCommit,baseRefName,headRefName,headRefOid,url,title
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `state=MERGED`, `mergeCommit.oid=658ac473c2164bc3f4da4840ee80c3f568733d03`, `headRefOid=5afa46609549d384235ffc9072680f44919e933b`.
- Command:
  ```bash
  git fetch origin
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `origin/main` updated `820165fe..493ba1d8`.
- Command:
  ```bash
  git rev-parse origin/main
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: `493ba1d861afdef977fabe2a241eb69db4d8a147`.
- Command:
  ```bash
  git merge-base --is-ancestor 658ac473c2164bc3f4da4840ee80c3f568733d03 origin/main
  ```
  Result:
  - Passed/failed/not run: passed.
  - Important output: merge commit is ancestor of `origin/main`.
- Command:
  ```bash
  rg -n 'ytInitialPlayerResponse|youtubei/v1/next|view_count|like_count_text|comment_count_text|comments_posture|SourceCapturePacket|source_surface|behavioral projection|deliberately does not acquire' <YT files>
  ```
  Result:
  - Passed/failed/not run: passed in `.codex/worktrees/youtube-contract-review-adjudication`.
  - Important output: confirmed transcript capture files use `SourceCapturePacket`; `behavioral_projection.py` says it does not acquire; legacy runner extracts watch-page metadata/comments routes and fields.

## Known issues and risks

- Issue: Root worktree is dirty and stale relative to merged `origin/main`.
  - Evidence: root `git status` shows many unrelated untracked files; root search could not find merged YouTube files that exist in PR worktree/origin.
  - Likely next action: create a fresh worktree off `origin/main` for the YouTube sync branch.
- Issue: Existing YouTube metadata/comments runner has weak state vocabulary.
  - Evidence: no comment panel token currently maps to `comments_posture = "disabled"` in `capture_youtube_v0.py`; user/live-probe context says missing token can mean route non-exposure, not disabled.
  - Likely next action: introduce explicit availability/comment exposure states and tests.
- Issue: Total comment count is not guaranteed.
  - Evidence: user-provided live probe: 2 playable videos had view counts and 10/12 comment samples but no reliable total comment count; 1 video removed by uploader.
  - Likely next action: store `comment_sample_count`, sampled comment likes/replies, and `total_comment_count` only when source-native count is exposed.
- Issue: Shared core overreach risk.
  - Evidence: prior planning and user clarification both reject copying YT acquisition methods into IG or forcing shared acquisition machinery.
  - Likely next action: keep this patch YouTube-specific and source-capture-shaped; defer shared core.

## Constraints and user preferences

- Constraint/preference: Push back hard when the user's framing is technically wrong or risky.
  - Source or reason: `AGENTS.md` user/project instruction.
- Constraint/preference: Smallest complete intervention.
  - Source or reason: `AGENTS.md`; do the complete sync slice without unrelated refactors.
- Constraint/preference: MGT and SCI lens.
  - Source or reason: prior user instruction; name accepted residuals, avoid fake completeness, avoid lock-in.
- Constraint/preference: Behavior parity, not acquisition uniformity.
  - Source or reason: user clarified not to enforce same acquisition method/priority/shape.
- Constraint/preference: Live capture using source capture playbook was authorized earlier, but must still load the playbook and use tool/network escalation when needed.
  - Source or reason: prior user instruction plus overlay source-loading capture-method rule.
- Constraint/preference: Do not implement shared core yet.
  - Source or reason: prior handoff/Drift Guard; current next goal is YouTube capture sync into source-capture lane.

## Next steps

1. Create a fresh worktree/branch off updated `origin/main`, e.g. `codex/youtube-capture-spine-sync`, and verify it contains PR #432 merge content.
2. Run assumption gate/fused for the bounded implementation: YouTube watch-page metadata/comments capture as a `source_capture` adapter/output with explicit availability states and route receipts.
3. Re-read capture playbook, `capture_youtube_v0.py`, `shorts_scroll_capture_v0.py`, `behavioral_projection.py`, transcript packet writers/runners, and focused YouTube tests.
4. Patch the smallest complete slice:
   - likely add/modify a SourceCapturePacket-shaped YouTube metadata/comments writer or adapter;
   - add explicit states: `playable`, `removed_by_uploader`, `private`, `age_restricted`, `login_required`, `region_blocked`, `comments_disabled`, `comments_not_exposed`, `comments_sample_captured`;
   - add route receipts per metric;
   - separate sample counts from total counts;
   - update projection/tests only as needed to consume the synced output.
5. Run focused unit/contract tests and `git diff --check`; add docs/update notes only if needed for behavior contract drift.

## Do not forget

- Critical detail: YouTube transcript capture is already under `source_capture`; do not rework that unless the metadata/comments sync requires a narrow integration.
- Critical detail: YouTube metadata/comments capture is not yet fully in `source_capture`; that is the next goal.
- Critical detail: Hitting a YouTube video page does not guarantee likes, total comments, or comments token; no zero-filling and no fake disabled state.
- Critical detail: Start from fresh `origin/main`, not the dirty root workspace.
