# Creator Graphing Scan Behavior Notes - 2026-07-07

```yaml
retrieval_header_version: 1
artifact_role: Review input artifact (creator graphing scan behavior note)
scope: Behavioral notes for TikTok creator graphing scans after the Fragranceknowledge probe.
use_when:
  - Planning or executing creator graphing scans that start from TikTok profiles.
  - Deciding how to record link hubs, sibling channels, suggested-account target expansion, and capture status.
  - Avoiding metric zero-fill, screenshot-heavy reporting, or registry insertion before preflight.
authority_boundary: retrieval_only
```

## Scope

Operational behavior note for the creator graphing / creator scanning lane after the Fragranceknowledge probe. This note is a review-input working artifact until promoted into the owning Creator Registry and platform capture specs.

## Accepted Behavior Changes

1. **Single intended browser surface.** Before a TikTok creator scan, identify the intended active capture surface, such as the warmed CloakBrowser CDP session and auth-state label. Close or avoid duplicate ordinary Chrome TikTok profile tabs so the operator does not accidentally read from a logged-out/wrong-fingerprint surface. Do not close the intended CloakBrowser session at lane end unless the user asks.

2. **Parent-platform capture in the same pass.** If graphing starts from or enters a parent platform page such as TikTok, preserve a bounded parent-platform receipt in that same scan pass. Do not leave the parent platform visit as an unreceipted diagnostic and require a later recapture request. Use the same warmed browser/session; do not relaunch just to capture what is already open.

3. **Refresh failure handling.** If TikTok shows a source-visible grid failure with a Refresh control, click Refresh once in the same session, then record the outcome. Do not loop, deep-refresh, rotate sessions, solve challenges, or fabricate grid availability.

4. **Token-efficient reporting.** Do not emit screenshots into chat by default. Store screenshots locally only when the capture lane or visual debugging needs them, and report the receipt path plus compact facts such as grid-link count, final URL, refresh-clicked flag, and limitations. Prefer text/DOM/JSON receipts for chat reporting.

5. **Link hub remains identity evidence.** Linktree or similar hubs can prove candidate sibling channels and source-visible region text, but they do not create platform metrics. Missing metrics stay null/not_attempted/not available, never zero.

6. **Registry/UI capture status.** The registry index already exposes capture_state. UI should display per-channel capture badges derived from capture_state plus current_metric_rollups: e.g. metric seed available, profile packet only, capture not started, blocked/stale when future freshness producers exist. The identity ledger should not absorb metric or capture-run state beyond source-backed account linkage.

7. **Seed-handle disambiguation before registry use.** Screenshot OCR, search rows, and shorthand operator labels can point to the wrong public account when used as a literal handle. Before graphing or registry mutation, open/check the literal handle and compare source-visible account facts against the seed intent: display name, follower/like scale, bio topic, content presence, and any existing frontier/registry evidence. If the literal handle is wrong or low-confidence, record the rejected literal handle and the source-backed corrected handle. Do not merge those accounts unless source-visible evidence supports it.

8. **Ordinary Chrome is a fallback, not the TikTok/Instagram scouting norm.** For TikTok/Instagram creator graphing, a warmed CloakBrowser or equivalent intended browser surface is the default because platform state, login state, and fingerprint posture can materially change what appears. If ordinary Chrome is used because the operator left a specific tab open, record it as a fallback/owner-supplied surface and preserve capture limitations such as logged-out prompts, generic suggested accounts, missing platform state, or lower grid/social-link visibility.

9. **Same-surface suggested graphing follows parent TikTok capture.** When a scan enters a TikTok creator page on the intended CloakBrowser/equivalent surface and captures the parent profile/grid, the next action is to perform at most one owner-authorized root Follow click if source-visible, verify the resulting state, and capture source-visible suggested-account rows. If profile Suggested shows `View all`, click it once and capture the expanded rows. If the profile carousel is absent, open `Following` or `Followers`, switch to `Suggested`, and record suggested-account rows or a blocked/empty outcome before moving to link hubs, sibling channels, or registry work. This keeps the platform recommendation context fresh and prevents the parent-grid packet from closing out without frontier expansion.

## Fragranceknowledge Probe Result To Carry Forward

- Intended TikTok surface: existing CloakBrowser CDP 9223.
- Wrong surface closed: ordinary Chrome logged-out TikTok profile tab.
- Corrected parent-platform receipt: forseti-harness/_test_runs/creator_graph_fragranceknowledge_tiktok_grid_cloakbrowser_cdp_20260707/receipt.json.
- Corrected receipt observed 35 TikTok grid video links.
- No metric rollup was admitted from this scan; do not zero-fill compute.

## Next Creator Scan Checklist

1. Verify only the intended platform surface is active.
2. Navigate the intended browser/session to the seed platform profile.
3. Capture parent profile/grid receipt immediately.
4. If source-visible and owner-authorized, click the seed creator Follow button once and verify the resulting state.
5. On the same CloakBrowser/equivalent surface, record profile suggested rows; if `View all` is present, click it once and capture the expanded rows; if profile suggestions are absent, open `Following` or `Followers`, switch to `Suggested`, and record suggested rows or a blocked/empty outcome.
6. Extract public bio link hub and source-visible region text.
7. Direct-HTTP capture the link hub first; browser fallback only if needed.
8. Record sibling IG/YT/TikTok handles with evidence basis.
9. Run registry preflight before inserting/updating accounts.
10. Present per-channel capture status as captured/profile-only/not-started without metric zero-fill.
11. When a literal seed handle resolves to a low-confidence or wrong account, preserve the disambiguation in the scan receipt/register and route the corrected handle through Creator Registry preflight before insertion/update.
12. If the scan used ordinary Chrome instead of the intended CloakBrowser/equivalent surface, diagnose whether missing links, missing suggestions, login prompts, or generic recommendations are browser-surface limitations before treating them as account facts.

## Registry Capture Coverage Correction

The current registry index has capture_state, but creator graphing needs a stricter display distinction:

- identity_observed_linkhub_only: account was found from Linktree or another official hub; the platform itself has not been captured.
- platform_profile_capture_available: the account's own platform profile page has a source receipt.
- platform_grid_capture_available: the account's platform grid/listing has a source receipt.
- metric_rollup_available: source-backed metric rollup exists.
- platform_capture_not_started: the account is linked/known, but no platform capture has begun.
- platform_capture_blocked_or_failed: an attempted platform capture produced a source-visible failure state.

For UI, show these as channel-level capture badges. Do not overload identity linkage state or metric_state to mean platform capture state. For Fragranceknowledge specifically, YouTube has prior metric seed coverage, TikTok now has a parent-platform grid receipt from the CloakBrowser scan, and Instagram should still present as linked-from-hub / platform capture not started unless an IG profile/grid receipt is added.

## Data-Lake Placement Correction

Parent-platform captures belong in the source-capture/data-lake lane when they are packet-grade. Creator graphing artifacts should store only compact extracted linkage evidence, preflight status, and source pointers to the lake packet or local receipt. Do not make the creator graphing folder the durable home for raw TikTok grid/profile evidence.

If the scan only produces an ad hoc diagnostic receipt, keep it labeled as scratch and do not promote it as lake truth. For the next seamless creator scan, the order should be: intended browser/session -> parent platform capture packet to data lake -> extracted graphing evidence -> registry preflight/update routing.

## Fragranceknowledge Lake Correction

The Fragranceknowledge TikTok grid observation from the existing CloakBrowser CDP scan was admitted to the data lake as a narrow profile-grid observation packet, not as a TikTok batch/comment packet:

- packet_id: 01KWYMDCZMSB4S5HBERVBYJQNG
- raw_path: F:\orca-data-lake\raw\4e6\01KWYMDCZMSB4S5HBERVBYJQNG
- source_surface: tiktok_profile_grid_existing_cloakbrowser_cdp
- preserved: raw/01_tiktok_profile_grid_observation.json and raw/02_tiktok_profile_visible_text.txt
- observed grid links: 35
- non-claim: not /api/post/item_list body preservation, not comment capture, not metric rollup


## Suggested-Account Expansion Rule

When a creator profile exposes TikTok Suggested accounts, treat them as target-expansion candidates only. Capture the current suggested-account list from DOM/text into a packet-grade observation where possible, then write compact graph edges from the root creator to candidate handles. The edge type is TikTok recommendation output; it is not a follower/following graph edge, endorsement, region signal, or registry identity proof.

If the Followers or Following modal is open and exposes a Suggested tab, click Suggested only as a bounded scan action in the same intended session, then paginate/scroll with a small explicit bound and record the bound used. Do not repeatedly follow/unfollow to force recommendations. Dedupe exact handles before candidate capture, and keep registry insertion behind exact-match preflight plus owner authorization.

Current Fragranceknowledge target-expansion source artifact: docs/review-inputs/fragranceknowledge_tiktok_suggested_target_graph_20260708.json.

Canonical frontier-register projection for that pass: docs/review-inputs/fragranceknowledge_tiktok_creator_discovery_frontier_register_20260708.json. Future repeated TikTok suggested-account scans should prefer the TikTok Creator Discovery Frontier Register shape from forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md.

Enforcement-placement classification before further scouting: forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md.
