# YouTube Capture Recon v0 (first live probe)

```yaml
retrieval_header_version: 1
artifact_role: capture recon card (source-family: YouTube)
scope: >
  First live feasibility-recon findings for YouTube public capture (long-form /watch and Shorts
  /shorts), banking the served-HTML embedded-state route evidence. Recon-grade, not packet-grade,
  not a capture-shape contract.
use_when:
  - Choosing or judging a YouTube capture route.
  - Updating the YouTube capture surface-split decision with probe evidence.
authority_boundary: retrieval_only
stale_if:
  - A later probe (esp. the browser/continuation comments probe) changes a route verdict.
  - YouTube changes the served-HTML embedded-state shape or access posture.
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/orca_creator_monitoring_policy_architecture_v0.md
```

## Placement / path-authority note (AR-02)

Filed as a sibling of the as-built `source_families/social_media/instagram/`. The capture-spine
migration plan still frames the `social_media/` grouping as a **proposed amendment** and names the
flat `source_families/youtube/` as the formally-accepted member path; this placement follows the
as-built IG-sibling convention and **does not by itself ratify the grouping**. Per the migration
convention, this recon artifact is the authorized trigger that legitimizes the YouTube family home.

## Authorization / boundary

- Owner authorized **live probes** (2026-06-21). This card records probe findings only.
- Source-access posture: `ACCEPTED_SOURCE_ACCESS_BOUNDARY_DECISION_V0` permits public-surface
  fetching of discoverable pages (owner-accepted ToS/litigation risk; "obtain legal counsel before
  commercializing scraping" caveat travels).
- This card does **not** authorize the runner build, the capture-shape freeze, folder/runtime
  systems, or storage/scheduling. Those need separate bounded implementation authorization.
- Step-0 access classification: public `/watch` and `/shorts` pages are publicly viewable
  (no login, no auth/access-control defeat).

## Probe receipts (observed, not inferred)

Method: raw HTTPS GET of the served HTML (logged-out, desktop Chrome UA), `curl --compressed -L`;
exact-value anchors grep-extracted from the inline `ytInitialPlayerResponse` JSON. No JS executed,
no login, single egress IP, 2026-06-21. **Recon-grade evidence** (field anchors), not a packet.

### P1 — long-form `/watch?v=dQw4w9WgXcQ`
- ACCESS: HTTP 200, final URL = requested watch URL; `consent.youtube.com`=0, "Sign in to confirm"=0. Publicly viewable.
- SUBSTRATE: `ytInitialPlayerResponse` present (3), `ytInitialData` present (2); served HTML 1,278,238 bytes.
- EXACT FIELDS (from embedded state): `viewCount:"1785036537"` (exact integer, not abbreviated), `lengthSeconds:"213"`, `publishDate:"2009-10-24T23:57:33-07:00"` (absolute ISO), `uploadDate` same, `channelId:"UCuAXFkgsw1L7xaCfnd5JJOw"`, `author:"Rick Astley"`, `shortDescription` present (full text).
- META: og:title (full), og:image (maxres thumbnail), og:url, og:site_name present.
- COMMENTS: `commentCount`=0 in initial HTML; one continuation marker present → comments are NOT in served HTML (continuation/XHR, browser-only). Untested here.

### P2 — watch-equivalence-by-id `/shorts/dQw4w9WgXcQ` (a long-form id under the shorts path)
- RESULT: HTTP 200 but **redirected to `/watch?v=dQw4w9WgXcQ`** (final URL), serving long-form embedded state. → YouTube routes by id-type; a long-form id does not serve the Shorts player.

### P3 — channel Shorts enumeration `/@RickAstleyYT/shorts`
- ACCESS: HTTP 200; `ytInitialData` present (2); 729,763 bytes.
- ENUMERATION: 48 distinct `/shorts/<id>` ids extracted; also 48 distinct `/watch?v=<id>` (count parity suggests each Short carries both URL forms — interpretation, not verified). → channel Shorts tab enumerates Shorts; `surface_type` should key on **duration**, not URL form, since a Short also has a `/watch?v=` URL.

### P4 — genuine Short `/shorts/-0FVExAgmps`
- ACCESS: HTTP 200, stays on `/shorts/` (no redirect). 1,323,395 bytes.
- SUBSTRATE: `ytInitialPlayerResponse` present (2) — **same route as long-form**.
- EXACT FIELDS (same JSON paths as long-form): `viewCount:"31993"` (exact), `lengthSeconds:"39"` (Shorts duration band), `publishDate:"2026-05-11T10:54:13-07:00"` (**absolute ISO — same semantics as long-form, not relative**), `channelId` (same channel), `author`.
- COMMENTS: `commentCount`=0 in initial HTML (same posture as long-form).

### P5 — comments via `youtubei/v1/next` continuation (both surfaces)
- ROUTE: comments absent from served HTML; reachable by POSTing the comments engagement-panel continuation token (extracted from `ytInitialData`) to `https://www.youtube.com/youtubei/v1/next` with the page's `INNERTUBE_API_KEY` + client version. **Same route on both surfaces.**
- LONGFORM `dQw4w9WgXcQ`: 20 comments returned, next-page continuation present; sample `publishedTime:"1 year ago"`, author `@YouTube`, like `257K`.
- SHORT `-0FVExAgmps`: 20 comments returned, next-page continuation present; sample `publishedTime:"1 month ago"`, author `@JustEme_F`, like `27`.
- TIMESTAMPS: comment `publishedTime` is **relative-only** ("1 year ago") on both surfaces — no source-native absolute comment time observed.
- LIKES: abbreviated at scale ("257K"), exact for small counts (27).

## Route verdict

| Surface | Route | Verdict |
| --- | --- | --- |
| long-form `/watch` | embedded-state (`ytInitialPlayerResponse`) in served HTML | **GO** for video+channel identity, exact view count, exact duration, absolute publish date, description, thumbnail |
| Shorts `/shorts` | same embedded-state route, same JSON paths | **GO** for the same field set |
| both | comments via `youtubei/v1/next` (panel-scoped continuation) | **GO** — same route/shape/parser both surfaces; 20/page, pagination token present |
| both | like count | **PARTIAL** — abbreviated at scale ("257K"); exact for small counts (27) |
| both | comment `publishedTime` | **relative-only** ("1 year ago") — minute-resolution windows NOT defensible from comment time alone |

## Split-decision update (evidence-based)

The probe **strengthens the unified decision** (one runner, `surface_type` switch). Against the split triggers:
- (a) different fields/timestamp semantics → **refuted for embedded-state fields**: long-form and Shorts expose the same JSON paths and **both** carry absolute-ISO `publishDate`. (Comment timestamps still untested.)
- (e) one parser misleading across surfaces → **refuted for metadata**: a single `ytInitialPlayerResponse` parser reads both.
- (b) incompatible comments route → **refuted**: both surfaces use the same `youtubei/v1/next` panel-scoped continuation, same payload shape, same parser, same pagination.
- (d) divergent per-surface verdict → not observed; both GO on metadata and comments.

**Conclusion: no observed split trigger fires.** All probed signals (substrate, field paths, video-timestamp semantics, comments route, comment-timestamp semantics) are identical across long-form and Shorts. The **unified one-runner + `surface_type` switch** design is probe-supported; a two-runner split is not indicated by any observed evidence (subject to the small-n caveat). `surface_type` discriminator: **duration band** (+ id-type redirect behavior), not URL form.

## Broadened sample (n=10: 5 creators × 2 surfaces)

Creators: MrBeast (mega-vlog), NASA (institutional), TED (talks), MKBHD (tech), BBC News (news); one long-form + one Short each.

**Generalizes (10/10):** `ytInitialPlayerResponse` embedded-state present; exact `viewCount` (366 → 58.6M), `lengthSeconds`, `author`; **absolute ISO `publishDate` on every video, both surfaces**. Comments via the same `youtubei/v1/next` route wherever enabled.

Edge cases observed (runner must handle):
- **Comments disabled** — NASA long-form + Short returned no comment panel → record a `comments_disabled` posture, not a failure. Distinct from TED long-form `comments=0` (panel present, empty/held).
- **`surface_type` discriminator** — Shorts up to ~165s seen (MKBHD), overlapping short long-form → duration band alone is insufficient; use the **serving surface** (does `/shorts/<id>` stay on `/shorts/` vs redirect to `/watch`) as the robust discriminator.
- **Fresh-content comment granularity** — relative `publishedTime` reaches minutes/hours for recent posts ("35 minutes ago", BBC) → early-window comment recency is partially recoverable for fresh videos, though still relative, not absolute.

## Route decision + dislikes + po_token (external-research-backed, 2026-06-21)

**Capture route: HYBRID escalation ladder (decided).** Raw-HTTP (served-HTML embedded state + `youtubei/v1/next`) is the **default rung** — cheapest, proven; escalate to the browser rung (CloakBrowser) **only on a detected block** (consent wall, "confirm you're not a bot", 429, empty continuation). Fold YouTube into Orca's existing anti-block HTTP ladder; do not browser-everything (wasteful) or auth-session for public data (no gain, adds risk). Per-IP **pace** governance (not volume) is the throttle lever (IG lesson).

**`po_token` risk (the durable-break watch).** External research (yt-dlp PO-token guide, Mar 2026) confirms YouTube Proof-of-Origin attestation gates **playback / player / subtitle / GVS-media** flows, but is **NOT** currently a universal gate on `youtubei/v1/next` / `browse` **comment continuations** — consistent with our successful raw comments probe. The raw comments route works **now** but is a known future-break surface if enforcement spreads → motivates a **durable canary probe** (route-health check, below).

**Dislikes — not publicly capturable; labeled routes only.** `statistics.dislikeCount` exists but returns data **only to the video owner**; the new June-2026 `videos.batchGetStats` omits dislikes; anonymous payloads keep the dislike *button* but not the *number*.
- **Creator-OAuth (ground truth)** — exact dislikes only when authenticated as the owner; strong signal, limited to consenting creators. The only ground-truth route.
- **Return YouTube Dislike API (ESTIMATE, low-weight)** — public `GET /votes?videoId=`. Pre-2021-11-10 videos ≈ archived real (±1-2%); post-cutoff = extrapolated from RYD-user telemetry (±15-25%, worse for small/new; <24h unreliable); self-selected, gameable. **Ingest only as an explicitly-labeled estimate** carrying `rawLikes`/`rawDislikes`/retrieval-time/era — never a hard authenticity threshold.
- **ArchiveTeam Dec-2021 crawl** — exact pre-cutoff snapshot; historical baseline feature only.

**Decided: adopt the RYD estimate as a low-weight labeled signal** (a `dislikes_estimate` block on packets), with creator-OAuth as the future ground-truth route for consenting creators.

**Route-health: no standalone monitor (owner decision, 2026-06-21).** A standalone canary and an inline capture guard were both prototyped and then **dropped as redundant**: at real capture *volume* a broken route surfaces directly in the output (errors, empty-continuations, walls/429s), and for Shorts it shows during normal active capture/browsing. Route-health is read from **per-packet posture receipts** (`captured` / `empty` / `disabled`) plus a volume run's wall-detection, not a separate probe. Residual: a silent-empty (`po_token`) break can mimic a genuinely comment-disabled video on a *single* item — distinguished at volume (a run of `empty` across many items = a wall; scattered `disabled` = normal). Durable/at-volume behavior is probed by the Shorts volume-scroll runner.

## Non-claims / what is NOT proven

- Sample now n=10 across 5 creators × 2 surfaces; the unified-route conclusion held 10/10. **Rare edge cases not yet sampled**: live/premiere, age-restricted, members-only, region-blocked, EU-consent-wall egress.
- Comments route, pagination, and timestamp semantics **tested** and consistent across both surfaces; comment `publishedTime` is **relative-only** (no absolute comment time observed) → minute-resolution comment windows not defensible from comment time alone.
- like count abbreviated at scale; `watch_time` not present in embedded state (consistent with creator-analytics-only; not hard-checked).
- Comment samples were read **in-memory for feasibility only — not captured/persisted** as a corpus.
- Single logged-out egress IP; EU/other egresses may hit a `consent.youtube.com` interstitial not seen here.
- Recon-grade field anchors, not packet-grade raw-body preservation.
- No GO claim is a build/runtime authorization; the runner and capture-shape freeze remain separately gated.

## Next probes (ordered)

1. Broaden the channel/video sample (multiple creators) to lift small-n on the unified-route conclusion.
2. Register this card in `capture_recon_index_v0.md` (separate, careful edit to the shared index).
3. Confirm `watch_time` absence + like-count fidelity ceiling across more videos.
```
