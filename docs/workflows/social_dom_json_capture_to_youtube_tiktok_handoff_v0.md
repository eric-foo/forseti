# Social DOM JSON Capture To YouTube TikTok Handoff

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet
scope: >
  Cold-reader handoff for YouTube and TikTok social-source capture lanes, split
  from the IG reels downstream packet. Carries generic DOM/passive-JSON capture
  lessons without copying Instagram selectors, endpoints, JSON keys, or count semantics.
use_when:
  - Starting or reviewing a YouTube public source-family lane.
  - Starting or reviewing a TikTok public source-family probe lane.
  - Reusing IG social DOM/passive-JSON lessons while forcing source-family-specific proof.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md
stale_if:
  - YouTube recon/playbook changes route, field, posture, or implementation-boundary claims.
  - A TikTok recon card or source-family playbook is created and supersedes the probe-first state.
  - IG reels-grid capture changes the generic DOM/passive-JSON method lessons recorded here.
  - The source capture playbook changes Step 0 access-control, route catalog, or receipt rules.
```

## Load Contract

- packet_version: workflow-handoff-v1
- mode: split-social-source-family-transfer
- created_at: 2026-06-22T20:48:29.4850791+08:00
- created_by_lane: Codex IG public reels capture closeout lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md`
- split_from_packet: `docs/workflows/ig_reels_capture_to_projection_ecr_cleaning_handoff_v0.md`
- expected_branch: `codex/ig-reels-capture-spine`
- expected_head_before_split_edit: `088b8d39`
- expected_dirty_state_before_split_edit: dirty working tree with unrelated pre-existing modified/untracked files; this split must touch only the two docs/workflows handoff packets unless the current user redirects.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Authoring Preflight

- output_mode: `file-write`; destination `docs/workflows/social_dom_json_capture_to_youtube_tiktok_handoff_v0.md`.
- template_kind: `handoff`.
- edit_permission: `docs-write`; target scope is this handoff packet only.
- reviews: no formal review verdict is created by this packet.
- doctrine_change: none intended; this is a handoff split, not a rule change.
- downstream_destination: YouTube/TikTok lanes must write their own recon card, playbook update, scoped plan, code patch, or blocked result under their lane's current authorization.

## Goal Handoff

- long_term_goal: Reuse the social DOM/passive-JSON capture method across public creator/video platforms while preserving platform-specific proof and lane boundaries.
- anchor_goal: Start YouTube and TikTok work from generic capture invariants, then force each source family to prove its own public route, identity join, count semantics, timestamp posture, and block markers.
- success_signal: A cold YouTube or TikTok lane can avoid relearning the IG DOM/JSON lessons while also avoiding the false shortcut of importing IG selectors, IG endpoints, IG count semantics, or IG behavioral limits.

## Current Source-Family State

- YouTube is not a blank slate in the current repo. The recon index points to `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md`, and that recon reports logged-out public long-form plus Shorts feasibility with served-HTML embedded state and a shared comments-continuation route. It is recon-grade, not packet-grade capture, and not tracked runner authorization.
- YouTube also has `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_agent_playbook_v0.md`, which separates source-family method from code-enforced and agent-followed conventions. Load it before making YouTube route or implementation claims.
- TikTok remains probe-first based on the currently loaded recon index: do not claim a route, selector, count meaning, timestamp posture, or anti-block envelope until a TikTok-specific probe records it.
- Instagram is method precedent only. Its `/reels/` DOM/passive JSON findings are not a source of truth for YouTube or TikTok selectors, endpoints, JSON keys, count names, or block behavior.

## Drift Guard

- Public surfaces only. If a surface is behind login, private access, CAPTCHA-gated access-control, or creator/account-only analytics, stop or use an owner-authorized entitled route; do not defeat access control.
- Do not serialize cookies, `set-cookie`, proxy endpoint, proxy credentials, exit IP, browser profile path, storage state, raw media bytes, or private session material into packets.
- Do not classify ads, sponsorship, paid behavior, bots, fake engagement, demand, credibility, integrity, or action support in Capture, Projection, ECR, or Cleaning.
- Do not copy IG selectors, endpoints, JSON keys, route cadence, visible tile counts, pinned behavior, or count semantics into YouTube or TikTok.
- Do not copy YouTube route findings into TikTok. A YouTube-proven embedded-state route is evidence for YouTube only.
- This handoff does not authorize live probes, network calls, runner builds, scheduling, data-lake writes, or tracked implementation. Those need current-lane authorization.

## Generic Social DOM/JSON Capture Learning Capsule

Use this as method transfer for YouTube and TikTok lanes. It is not a platform claim.

- Start with a public creator/channel listing or item surface a human can view without authentication, such as videos, shorts, reels, uploads, or a profile grid.
- First prove what is visible without item-page fan-out: visible count text, hidden DOM text, item permalinks, profile snapshot fields, route/block state, and final URL.
- Treat rendered DOM and passive page-load JSON as separate source surfaces. Do not collapse them into one truth field.
- Join only by stable item identity: video ID, canonical permalink path, platform item ID, shortcode, or a source-native canonical URL. Never use grid index as identity across days.
- Preserve candidate values before selecting. If DOM count, passive JSON count, profile-feed count, or item-page count disagree, emit candidates with `source_surface`, `capture_mode`, and limitation reason.
- Selection policy must be versioned and visible. A chosen `view_count`, `like_count`, `comment_count`, or timestamp without source provenance is a downstream-evidence bug.
- Passive JSON may include more items than the visible grid because pages preload. Useful, but not guaranteed; record candidate count and overlap count.
- Viewport, zoom, route, locale, egress, and browser bucket can change source depth or wall behavior. Record them as behavioral variables, not correctness proof.
- Captions, descriptions, hashtags, sounds, paid labels, affiliate fields, sponsor users, pinned markers, and product fields are source-visible candidates. They are not ad/sponsorship conclusions.
- Engagement counts are raw public traction inputs, not demand, credibility, integrity, or action signals by themselves.
- Repeated brand/product mentions are Projection/Cleaning mechanical signals: count them, normalize them, link originals, and defer meaning.
- Exact timestamps come from joined source data only. Do not extrapolate exact publish dates from listing position.
- Platform-specific lanes should discover their own source-surface vocabulary, for example `dom_grid_engagement`, `passive_page_json_metadata`, `player_or_initial_state_json`, `profile_json_metadata`, `item_page_metadata`, `comments_continuation_json`, or `listing_embedded_state`.
- Every source-family probe should return a route status even when blocked: final URL, login/challenge/interstitial markers, parsed item count, source-surface count, candidate/overlap counts, and limitations.

## Code-Enforceable Items To Carry Into Social Capture Designs

- Stable item identity must be required before longitudinal joins.
- Every numeric/count/timestamp candidate must carry source provenance and parse status.
- Runner output must preserve candidate values before chosen values.
- Packets must strip or omit cookies, `set-cookie`, proxy endpoint, proxy credentials, exit IP, browser profile path, storage state, and raw session material.
- Route status must be explicit for success, partial success, blocked, empty, disabled, not attempted, and access-gated outcomes.
- Source-surface names, selection policy version, viewport/route/browser bucket, and final URL must be recorded in any packet-grade output.
- Static/image, short-video, long-video, comment, profile, and listing surfaces must not be silently merged unless a source-family recon proves the identity and semantics are shared.
- Packet fields must use neutral mechanical names. Ban conclusion-shaped field names outside Judgment-owned work.

## Behavioral Items To Refresh Per Platform

- DOM selectors, class names, and hidden text ordering.
- Embedded-state JSON location, keys, path stability, and whether it is served in HTML or loaded after client-side work.
- Listing depth, preload depth, and overlap between visible DOM rows and passive JSON records.
- Count semantics: view vs play vs impression-like counters; like/comment exactness vs abbreviation; disabled/hidden/comment-moderated posture.
- Timestamp semantics: absolute, relative, missing, edited, scheduled, stream/premiere, or item-vs-comment granularity.
- Block/wall behavior by route, locale, egress, browser bucket, pace, and account/session state.
- Whether source-visible paid, affiliate, sponsor, music/sound, product, or pinned labels are present and how they are represented.

## Exact Next Authorized Action

1. YouTube lane: source-load this packet, the capture playbook, the recon index, `youtube_capture_recon_v0.md`, and `youtube_capture_agent_playbook_v0.md`. Do not run a blank-slate YouTube probe before reconciling those files. Return a source-surface table, residual list, and a code-enforceable vs behavioral split for any next implementation proposal.
2. TikTok lane: source-load this packet, the capture playbook, and the recon index. Prepare the first public-surface probe plan from Step 0 access classification and the generic capsule. Run live TikTok only if the current user explicitly authorizes the live/network probe in that lane.
3. Cross-platform architecture lane: keep the shared interface at the candidate/source-surface/identity/provenance level. Do not build a platform-generic parser that assumes one platform's selectors, endpoints, or count semantics.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`, SHA256 `4296E7617D8B2675881780CD7BE0704A00DCB17ADF7758243008DE956070940B`.
- Overlay authority:
  - `.agents/workflow-overlay/README.md`, SHA256 `7A30709D6011BD3F6458E926570B7164B91C7F3BF8BAE7DBD5A612A08DE81FDA`.
  - `.agents/workflow-overlay/source-loading.md`, SHA256 `58994CA788F1754DEA49277750B64C592DE0A4B7B19DBF495CE675DDB9C08181`.
  - `.agents/workflow-overlay/artifact-folders.md`, SHA256 `42D4F554DAF4BE6F0A4A9BCBE3C67FD74EEFCC063FC72B03E53E11242EDC7AE9`.
  - `.agents/workflow-overlay/decision-routing.md`, SHA256 `8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E`.
- Capture method ledger:
  - Source capture playbook: SHA256 `E08595503E5C579E2FCDBE7F957BE3103B2FD0C03BC72877AC1092013FD4A5FD`, load-bearing yes for access-control and route receipt rules.
  - Capture recon index: SHA256 `FA3F6FCCB6CA85479A01404092400EB11049F6D2AEC503F14061FCAD4CCB1E31`, load-bearing yes for current social recon inventory.
  - IG reels-grid spec: SHA256 `09E3149A332625F3FDF9A4AFABD560CED07AFFFF1DA95F35EE3CF93C951CCCD9`, method precedent only, not YouTube/TikTok authority.
  - YouTube recon card: SHA256 `39B003459AFBBA9D1825EE9F83DE0182659BF84F8AA377CAD01B1FD8AF3D094B`, load-bearing yes for YouTube route claims.
  - YouTube agent playbook: SHA256 `758C72CF52E714CB514D5DDEA109B815ED63F89BFF07237850495D2FBA2C7437`, load-bearing yes for YouTube operating boundary claims.
- Source gaps: TikTok-specific technical recon remains absent from this packet; YouTube capture is recon/playbook-backed but not promoted here to packet-grade tracked implementation.
- Not-proven boundaries: no TikTok route, no cross-platform selector/key stability, no scaled operating envelope, no ad/sponsorship/bot/demand/credibility classification, no legal advice.

## Commands And Verification Evidence

- Source context checks during split:
  - `rg` over the capture recon index found current IG, YouTube, and TikTok social-state notes.
  - `Get-Content -Raw` read `youtube_capture_recon_v0.md` and `youtube_capture_agent_playbook_v0.md` before this packet was authored.
  - `Get-FileHash -Algorithm SHA256` produced the hashes recorded in the Authority And Source Ledger.
- Re-run target: before acting, rerun source loading and rehash the target source-family files. For this docs-only split, `git diff --check` over the two touched packet files is the relevant local check.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - branch/head and dirty state;
  - source capture playbook Step 0 and route receipt rules;
  - capture recon index social-network rows;
  - YouTube recon and playbook route/status claims before any YouTube work;
  - TikTok absence/presence of a source-family recon card before any TikTok claim;
  - IG spec only when using IG as method precedent.
- Compare target for each:
  - hashes in Authority And Source Ledger;
  - fresh `git status --short --branch`;
  - fresh `git rev-parse --short HEAD`;
  - targeted `rg`/fresh reads of source-family files.
- Load outcomes and what each means:
  - `REUSE`: all load-bearing facts match; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional or non-load-bearing facts drifted; reuse verified lane boundaries and refresh the rest.
  - `STALE_REREAD_REQUIRED`: material source drifted but can be reread and re-derived.
  - `BLOCKED_DRIFT`: drift conflicts with scope, ownership, or dirty-state safety.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim lacks a compare target and cannot be re-derived.

## Do Not Forget

The transferable lesson is not an Instagram implementation. It is the discipline: public access gate first, separate DOM from passive JSON, join by stable item identity, preserve candidates with source provenance, record route status even when blocked, and defer meaning to downstream Judgment-owned work.
