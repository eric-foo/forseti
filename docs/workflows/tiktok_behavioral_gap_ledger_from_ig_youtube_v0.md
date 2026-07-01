# TikTok Behavioral Gap Ledger From IG YouTube v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow gap ledger
scope: >
  Source-backed TikTok behavior-sync ledger after restoring the TikTok handoff
  from the IG/YT behavioral residual lane. Compares existing TikTok
  source-family spec/recon/probe sources against the IG/YT behavioral contract
  without authorizing live TikTok capture, TikTok code, or shared-core
  implementation.
use_when:
  - Deciding the next TikTok source-family behavior-sync move.
  - Checking which IG/YT behavioral completeness surfaces TikTok can match from
    existing source-family evidence.
  - Preventing stale "no TikTok recon" or logged-out-only assumptions from
    driving TikTok implementation.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md
  - docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md
  - docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  - docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md
  - orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md
  - docs/workflows/tiktok_sessioned_profile_grid_dom_receipt_v0.md
stale_if:
  - Any TikTok source-family spec, recon, warm-probe plan, capture playbook, or
    recon-index TikTok/social row changes.
  - A live TikTok probe runs and changes route, access, fingerprint, challenge,
    field, request-cap, or data-contract evidence.
  - A later IG/YT behavioral closeout changes the reference contract or
    residual boundaries.
  - The owner redirects from TikTok source-family behavior sync to live probing,
    implementation, vendor bulk data, or shared-core extraction.
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom TikTok behavior-sync pack
  edit_permission: docs-write
  target_scope: source-backed TikTok behavioral gap ledger and next-action decision; no live capture and no code edits
  dirty_state_checked: yes
  blocked_if_missing: handoff packet, source-loading overlay, decision-routing overlay, capture playbook, recon index, IG/YT closeout, current TikTok spec/recon/probe plan
```

Workspace basis:

```text
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-youtube-residual-burndown
branch: codex/ig-youtube-residual-burndown-pushable
head: 886769bc683d3162f3b00b35ee7acb8e9c7ade4d
dirty_state_before_this_ledger: one untracked handoff file, docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md
```

The root checkout at `C:\Users\vmon7\Desktop\projects\orca` was not used as the
strict state source: the requested packet path was absent there, and the current
root branch did not contain the TikTok source-family files.

## Cynefin Routing

Smallest complete outcome: produce a source-backed TikTok behavioral gap ledger
and next-action decision, without live TikTok work, code edits, or shared-core
implementation.

Regime: Complex.

Why: the route and data contract are partly source-backed, but TikTok's sessioned
access ceiling, challenge behavior, and transcript/audio posture remain
unmeasured and can change the next build route.

Decomposition: risk-first source refresh, then owner-gated live probe only if
the refreshed ledger shows live access is the bottleneck.

Current bottleneck: the current TikTok documents conflict in two places: the
source-family docs say TikTok recon/spec/warm-probe sources exist, while the
recon index still says no TikTok technical recon; and the TikTok spec has a
sessioned/cookied direction update while some body text still says logged-out
or "no auth".

Riskiest assumption: a warmed dedicated session will provide stable enough
page-owned metadata/comment capture to justify implementation.

Stop or pivot condition: any live probe challenge, account-risk refusal, missing
dedicated account/human login, or source update that changes the page-owned
blob/comment route.

Allowed next move: docs/spec synchronization for TikTok source-family state,
then owner-gated warm-session probe if the owner accepts account-ban and network
risk.

Disallowed next move: live TikTok capture, TikTok parser/runner/projection code,
shared-core code, forged TikTok signatures, deep comment pagination, or use of
IG/YouTube mechanics as TikTok acquisition templates.

## Confirm-Don't-Trust Load Outcome

Outcome: `PARTIAL_REUSE`.

What reverified cleanly:

- The handoff worktree branch and HEAD match the packet's expected lane state.
- Every load-bearing source named with a SHA256 compare target matched that
  target.
- The handoff packet, IG/YT closeout, YouTube corpus receipt, shared-core plan,
  social DOM/JSON handoff, capture playbook, TikTok spec, first-slice recon, and
  sessioned warm-probe plan were reread before this ledger was authored.

Why not full `REUSE`:

- The capture recon index still states "TikTok has no technical recon at all",
  but the same worktree contains current TikTok source-family spec, first-slice
  recon, and sessioned warm-probe plan. For TikTok-specific claims, this ledger
  treats the source-family TikTok files as fresher controlling sources and marks
  the recon-index TikTok row stale.
- The TikTok spec has a sessioned/cookied direction update, but some body text
  still says logged-out, `real_browser_logged_out`, or "C8 = no auth". Those are
  stale carryovers relative to C8' and the warm-probe plan.

## Source Read Ledger

| Source | Read result | Load-bearing use |
| --- | --- | --- |
| `docs/workflows/tiktok_behavioral_sync_from_ig_youtube_handoff_v0.md` | Found only in the lane worktree, not in root; reread. | Active objective, drift guard, source list, exact next action. |
| `.agents/workflow-overlay/source-loading.md` | Reread. | Capture-spine activity starts with playbook plus recon index; strict claims need controlling source. |
| `.agents/workflow-overlay/decision-routing.md` | Reread. | Cross-thread, messy-state, source-refresh work requires compact routing before planning. |
| `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md` | Hash matched `A3621D5A...35A8`; reread. | IG/YT reference is bounded: IG has residuals; YouTube caption-route is observed, platform-wide is not proven. |
| `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md` | Hash matched `B26F6DE6...3D0D`; reread. | YouTube caption-route observed complete at 31/31; ASR/no-caption and provider extraction remain residual. |
| `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md` | Hash matched `8C2A6239...E8AD`; reread. | Shared target is behavioral parity through a thin core, not shared acquisition machinery. |
| `docs/workflows/youtube_first_behavioral_completion_spec_v0.md` | Hash matched `D10F373E...A8`; reread. | Behavioral surfaces to compare: candidate identity, run receipt, metadata/stats, comments, transcript, persistence, extraction, residuals. |
| `docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md` | Hash matched `B9856FDD...3401`; reread. | Generic DOM/passive-JSON lessons transfer, but no IG/YouTube selectors, endpoints, or count semantics transfer. |
| `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | Hash matched `0B8C169F...796`; reread. | Step 0 access gate, route receipt, public-content risk posture, no-secret guardrails. |
| `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` | Hash matched `E5A583DB...79B`; reread. | Social recon inventory; TikTok row stale relative to current TikTok source-family docs. |
| `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md` | Hash matched `6ABF594A...F1C`; reread. | TikTok C1-C8' invariants, data contract, request cap, secret hygiene, sessioned direction. |
| `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_first_slice_probe_recon_v0.md` | Hash matched `F77A2972...BD3`; reread. | First-slice route evidence: real cookied browser exposes profile/video metadata and comments; detection ceiling unknown. |
| `orca/product/spines/capture/core/source_families/social_media/tiktok/tiktok_sessioned_capture_warm_probe_plan_v0.md` | Hash matched `013BA33A...88D`; reread. | Owner-gated dedicated-account warm-session probe preconditions, stop conditions, and measurement ledger. |
| `docs/workflows/tiktok_sessioned_profile_grid_dom_receipt_v0.md` | Added after the sessioned profile-grid DOM check. | Sessioned `@tiktok` profile grid: `webapp.user-detail`, stable profile/grid selectors, 31 visible post/view nodes, and 24 structured video anchors without visible login/challenge signals. |

## Behavioral Gap Ledger

| Surface | Current TikTok source-backed state | Classification | Gap / residual | Next implication |
| --- | --- | --- | --- | --- |
| Profile/listing grid | First-slice recon observed profile page fields and 16 video permalinks in a real cookied browser. The 2026-06-30 sessioned profile-grid DOM receipt then observed `@tiktok` with `webapp.user-detail`, selectors `user-title`/`user-bio`/`user-link`/`user-post-item`/`video-views`, 31 visible post/view nodes, and 24 structured video anchors without visible login/challenge signals. | `code-enforceable` plus `requires_live_probe` for depth/scale | Sessioned N=1 DOM route is measured for the locked fixture; grid pagination/depth, exact numeric view-count normalization, selector drift over time, and challenge rate remain unmeasured. | Keep profile/listing as TikTok adapter-owned. Enforce stable item IDs and source-surface provenance; do not borrow IG grid selectors or YouTube channel mechanics. Do not use listing position as identity. |
| Video detail | Spec and recon identify metadata in `#__UNIVERSAL_DATA_FOR_REHYDRATION__` under `webapp.video-detail.itemInfo.itemStruct`, with zero extra requests. | `code-enforceable` plus `requires_live_probe` | Field presence under a warmed authenticated session is expected but not measured by the warm-session plan yet. | Parser/spec can target page-owned blob fields; implementation should wait until stale logged-out/sessioned wording is reconciled and live route ceiling is owner-approved. |
| Stable identity | Source-backed identifiers include `video_id`, video URL/permalink, author `id`/`uniqueId`, comment `cid`, commenter `uid`/`unique_id`, and source-native comment cursor. | `code-enforceable` | No durable TikTok persistence layer exists yet; identity joins are specified, not implemented. | Require stable identity before longitudinal joins; never use listing position as identity. |
| Metadata/stats | Spec names raw integer video stats (`diggCount`, `shareCount`, `commentCount`, `playCount`, `collectCount`), author stats, music, textExtra, description, and exact `createTime`. | `code-enforceable` plus `requires_live_probe` | Detection ceiling and field drift are unmeasured; spec still has stale logged-out receipt language. | Keep all numeric candidates source-provenanced and raw. Do not infer demand, bot behavior, sponsorship, credibility, or action support in Capture. |
| Comments sample/posture | Recon observed page-owned `/api/comment/list` responses with exact comment fields; spec caps capture to first page plus at most one pagination and default relevance order. | `code-enforceable` plus `requires_live_probe` | Full comment census and chronological windows are out of scope; live sessioned challenge ceiling is unmeasured. | Enforce request cap, capture posture, response provenance, `has_more`/cursor, and sample limitations. Do not forge signatures or deep-paginate. |
| Exact timestamps | Video `createTime`, video-id-derived timestamp, and comment `create_time` provide exact source times in recon/spec. | `code-enforceable` | Rendered DOM time strings are lower fidelity; exact comment timestamps depend on the API response, not DOM. | Timestamp parser can be a hard contract when source fields exist; otherwise emit explicit missing/failed posture. |
| Transcript/audio/source text | Spec covers description, hashtags/mentions in `textExtra`, music metadata, and comments. It does not prove source-native captions, speech transcript, ASR route, durable media bytes, or audio extraction posture. | `blocked/unproven` for transcript/audio; `code-enforceable` for explicit source-text posture | TikTok transcript/audio behavior is not established. Treat media/audio bytes as out of scope until a separate owner decision and source read. | Do not route TikTok into the IG/YT transcript extraction contract yet. First update docs/spec to state source text vs transcript posture, then decide whether a probe should look for public captions/audio/transcript surfaces. |
| Run receipt | Spec requires source URL, retrieval time, response bytes/hash, request count, limitations, and non-claims; warm-probe plan requires account label, session mode, warm-up, batch ladder, challenge point, and no secrets. | `code-enforceable` | Spec receipt text still says `real_browser_logged_out`, conflicting with sessioned C8' and warm-probe `entitled_session`. | Patch docs/spec before any probe so execution receipts cannot preserve stale access posture. |
| Persistence/correlation anchors | Intended join key is video-level identity, with comment and user IDs beneath it; source-capture writer/packet rails are reusable but no TikTok persistence exists. | `code-enforceable` plus `requires_live_probe` | No TikTok packet/projection implementation has been found; no lake/F-lake behavior claim exists. | Implementation scoping should define packet anchors only after the warm-session evidence is accepted or explicitly bypassed by owner. |
| Extraction-feed readiness | IG/YT extraction is transcript-source based; TikTok currently has source text, comments, hashtags, music, and description, but no proven transcript source. | `blocked/unproven` | Feeding TikTok into the existing transcript product extractor would fake parity unless a transcript/caption/ASR source is proven. | Defer extraction-feed implementation. A docs/spec update should name candidate source-text surfaces and explicitly keep transcript/product extraction not proven. |
| Residual visibility | Current sources name block/challenge, empty/stripped shell, request cap, sample-not-census, no full comment pagination, no private surfaces, and no secret persistence. | `code-enforceable` | Residual vocabulary is split across spec, recon, and warm-probe plan; the recon index still has stale no-recon wording. | Consolidate residuals in TikTok spec/recon-index update; preserve visible failures instead of manufacturing completeness. |
| Fingerprint/access posture | Owner decision pivots from logged-out-primary to sessioned/cookied dedicated account: human login, no credentials by agent, no concurrent TikTok tabs, warmed account, public content only, stop on challenge, ban risk accepted. | `requires_live_probe` plus `behavioral/doctrine` | Actual per-account ceiling is unmeasured. Sessioning may reduce captcha but introduces account-ban risk. | Do not run live until owner gives current network authorization, dedicated account, human login, and account-risk acceptance. Do not solve challenges. |

## Decision

Next move: `DOCS_SPEC_SYNC_FIRST`, not live probe and not implementation.

Reason:

- There is enough TikTok source-family evidence to stop treating the lane as
  blank.
- There is not enough evidence to implement or claim readiness: the sessioned
  detection ceiling is unmeasured, transcript/audio behavior is unproven, and no
  TikTok code/persistence source was found.
- The docs contain execution-relevant stale language. Running a warm-session
  probe before cleaning that would risk receipts that say the wrong access
  posture, especially `real_browser_logged_out` instead of `entitled_session`.

Recommended docs/spec sync:

1. Update `capture_recon_index_v0.md` so the TikTok social row points to the
   current TikTok spec, first-slice recon, and sessioned warm-probe plan instead
   of saying no TikTok technical recon exists.
2. Update `tiktok_capture_lane_spec_v0.md` to remove stale logged-out/no-auth
   carryovers in body text and align receipts with C8' and the warm-probe plan:
   `entitled_session`, dedicated account, human login, public content only,
   no secret persistence, stop-on-challenge.
3. Add an explicit TikTok source-text/transcript boundary: description,
   textExtra, music metadata, and comments are source text; source-native
   captions/speech transcript/ASR/audio are not proven and remain out of scope
   unless a future probe targets them.

After that docs/spec sync, the next technical decision is owner-gated:

```text
owner_gated_warm_session_probe:
  required:
    - dedicated non-personal TikTok account
    - human-performed login
    - per-operation network approval
    - owner acceptance of account-ban and ToS risk for that account
  still_forbidden:
    - personal account use
    - agent-entered credentials
    - stored cookies/tokens/secrets in packets
    - private/access-controlled surfaces
    - captcha solving
    - forged msToken/X-Bogus/X-Gnarly/signature routes
```

## 2026-06-30 Live Probe Addendum

After this ledger was authored, the owner explicitly authorized live sessioned
TikTok DOM/hydration probing in the same lane. The current live receipt is
`docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_receipt_v0.md`,
with full structured payload in
`docs/workflows/tiktok_sessioned_dom_hydration_profile_comments_payload_v0.json`.

Current measured updates:

- Profile/listing grid: sessioned `@tiktok` route stayed clean through bounded
  scroll, exposed `webapp.user-detail`, 95 `user-post-item` / `video-views`
  nodes, and 94 unique video anchors.
- Video detail: pinned fixture `7642770753292635422` stayed clean and exposed
  `webapp.video-detail` with exact video `createTime`, raw stats, author, music,
  and mention metadata.
- Comments: the comments panel opened cleanly and exposed 20 visible top-level
  comment DOM rows, but one bounded comment-panel scroll did not expand the DOM
  sample.
- Packet boundary: `/api/comment/list` response bodies were not captured through
  the Chrome surface, so sessioned `cid`, `uid`, exact comment `create_time`,
  cursor, and `has_more` remain unproven.
- Existing-Chrome diagnostic: a later same-day pass reused the already-running
  logged-in Chrome tab and again rendered comments cleanly. The only supported
  extra Chrome capability was `pageAssets`, which exposes static/media assets but
  not XHR/fetch bodies; read-only page evaluation also lacked `performance`
  resource timing. This makes Chrome-extension DOM probing a dead end for
  packet-grade comment fields.

Updated next move: `PINNED_RESPONSE_CAPTURE_NEXT`. More DOM probing is now lower
value than a pinned harness run that observes the page-owned `/api/comment/list`
response body through `fetch_browser_page_observation_capture` plus the post-load
comments action. Only after that packet field proof should the lane run a
5-video ceiling rung.

## 2026-07-01 N30 Funmi Cadence Analysis Addendum

The prior `PINNED_RESPONSE_CAPTURE_NEXT` state is superseded for the Funmi
sessioned route by
`docs/workflows/tiktok_funmi_n30_comment_subtitle_cadence_analysis_v0.md`.

Current measured updates:

- Page-owned comment-list body route: N=1 proof succeeded, N=5 pilot succeeded,
  and the N=25 remaining rung succeeded. Combined Funmi/session rate: `30/30`
  completed, `0/30` challenges, `0/30` failures.
- Comment packet fields: the 30 videos preserved parsed public comment fields
  with body hashes, envelope `cursor`/`has_more`/`total`, source order, and the
  required per-comment `cid`, `text`, `create_time`, `digg_count`,
  `reply_comment_total`, `user.uid`, `user.unique_id`, and `user.nickname`.
- Source-native subtitle/WebVTT route: `26/30` videos had `subtitleInfos`, and
  `26/26` with metadata produced parsable WebVTT bodies. The four misses are
  `no_subtitleInfos_present`, not observed fetch failures.
- Source-text/disclosure analysis: 7/30 videos carried source-visible ad or
  partner signals in hashtags/transcript text; keep these separate from
  platform-rendered paid-partnership labels unless platform fields are captured.

Updated next move: `DURABLE_PACKETIZATION_AND_EXTRACTION_NEXT`. Do not spend the
next step on more same-creator live capture. Admit the N=30 staging outputs into
a durable sanitized batch artifact or packet family, then run typed extraction
over parsed captions/comments/source text. A later live rung should be
cross-creator or explicitly ceiling-oriented, with stop-on-challenge still
binding.

## Non-Claims

- Not TikTok validation, readiness, production scale, or reliable detection
  ceiling.
- Not live/network authorization.
- Not permission to use a personal TikTok account or store session material.
- Not a TikTok parser, runner, projection, persistence, extraction, ECR,
  Cleaning, Judgment, or shared-core implementation authorization.
- Not legal advice.
