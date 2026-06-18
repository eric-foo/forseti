```yaml
retrieval_header_version: 1
artifact_role: capture recon finding (non-authorizing) — IG suggested-accounts discovery edge
scope: >
  Phase-1 feasibility recon for discovery mechanism 1 (the suggested/related-accounts
  graph) of the IG creator-momentum pipeline: is the edge reachable LOGGED-OUT, on which
  surface, populated, and snowball-able? Records the GO verdict, the exact substrate, the
  node shape, the rate behaviour, and the residuals Phase 2 must close. A recon GO, not a
  build go, validation, or at-scale claim.
use_when:
  - Scoping or building the discovery snowball (Phase 2) or the roster-assembly stage.
  - Checking where the related-accounts edge lives and what each node carries.
  - Resolving whether discovery needs an off-IG dependency (it does not).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/source_families/instagram/ig_creator_discovery_spec_v0.md
  - orca/product/spines/capture/source_families/instagram/ig_capture_findings_consolidated_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
stale_if:
  - Phase 2 (snowball depth / sub-niche coherence / follower bands / crawler-strip retry) lands.
  - IG changes the web_profile_info payload or moves edge_related_profiles behind auth.
  - The crawler-strip empty-cause (vs account opt-out) is disambiguated.
status: GO (logged-out) — Phase 1 (reachability, n=3) + Phase 2 (bounded snowball) feasibility-proven; production needs a sub-niche filter (gating) + rising-tier depth + at-scale posture
```

# Instagram Creator Discovery — Suggested-Accounts Edge Recon (Phase 1, v0)

## Headline

**The related/suggested-accounts edge is reachable and populated LOGGED-OUT.** It lives at
`data.user.edge_related_profiles` in the **`web_profile_info` JSON** — the same tolerant,
200-cookieless surface already used for calls, profile stats, and reel view counts. So
discovery mechanism 1 (the rising-creator spine) needs **no off-IG dependency and no
session**: the entire 3-capability pipeline can run on one IG substrate. Recon GO, n=3,
feasibility only — not a build, validation, or at-scale claim.

## Evidence (n=3, logged-out, 2026-06-15)

| Seed (sub-niche) | `edge_related_profiles.edges` | Outcome |
| --- | --- | --- |
| jeremyfragrance (fragrance) | **19 accounts** | populated logged-out |
| nikkietutorials (makeup) | **32 accounts** | populated logged-out |
| hyram (skincare) | **0** (empty + login-wall variant) | crawler-strip / opt-out (see Caveat 1) |

Each related node carries, logged-out: `username`, `full_name`, `is_verified`, `is_private`,
`id`, `profile_pic_url`. The set is **sub-niche-coherent** — jeremyfragrance's 19 are all
fragrance accounts (amouageofficial, azzaro_parfums, lattafa_perfumes, rojalondon,
nishane.official, afnanperfumes, fragranticaofficial …). `username`+`id` per node means the
**snowball is feasible** (feed each back into `web_profile_info` for the next hop).

Raw evidence (gitignored, not committed): `orca-harness/_test_runs/related_accounts/<handle>/`
(`web_profile_info.json`, `profile.html`, `sniffed_responses.jsonl`, `summary.json`) +
`aggregate.json`.

## Method (the widened substrate net)

Disposable logged-out Playwright probe (`orca-harness/_scratch/related_accounts_probe.py`).
Per seed it inspected **three** surfaces so a negative is surface-bounded, not a wrong-surface
false miss:
- (a) `web_profile_info` JSON via in-page `fetch` (`X-IG-App-ID: 936619743392459`, `credentials:'include'`);
- (b) the profile HTML / initial state (`page.content()`);
- (c) every text/json XHR fired during profile load (`page.on('response')`).

Detection enumerated candidate keys **generically** (recursive scan for `/related|chain|suggest|recommend/i`
over all discovered key names, not a fixed-list bet — the prior naive-detector lesson), and a
negative is trusted **only** after confirming the enumerator finds a known-present control key
(`edge_owner_to_timeline_media`). Control key found for all 3 seeds → results trustworthy.

## Rate behaviour

6 `web_profile_info` requests, **all HTTP 200, no 401/429.** The tolerant surface held; this
also **re-confirms live** that `web_profile_info` is 200-cookieless in a browser context. The
~35-anon-req/window 401 ceiling is a **grid `graphql/query`** property and did not bite here
(no grid calls; no snowball). The wpi endpoint's **own** ceiling at ~25–30 consecutive reads
is untested → a Phase-2 measurement.

## Caveats (both are Phase-2 inputs; neither blocks the GO)

1. **Logged-out anti-crawler variability (the empty `hyram`).** hyram's profile page redirected
   to `/accounts/login` and its `edge_related_profiles` came back **empty**. The JS bundle
   carries the flag `should_remove_related_profiles_for_crawlers`, so IG plausibly served the
   crawler-strip variant — **or** hyram has the account-level "show similar accounts" opt-out.
   On n=1 the cause is **not disambiguated** (a single clean re-fetch of hyram's wpi, without
   the profile-page nav, would settle it). Either way it is a **known empties source Phase 2
   must detect-and-retry**, not a reachability failure. A pure-wpi snowball (no profile-page
   nav) is the likely mitigation, since the wpi fetch stayed 200 even when the HTML nav walled.
2. **No follower count in the node.** Follower-band filtering needs one extra `web_profile_info`
   hop per candidate (`edge_followed_by.count`) — which is the snowball anyway (1 call/profile).

## Measurement note (recon Pattern 1 discipline)

The probe's `base_ok` check conflated the profile-HTML login redirect with the wpi surface's
reachability, so hyram was marked `VOID` even though its wpi returned a clean 200 carrying the
(empty) edge. A probe-logic artifact, **not** an IG failure — and a useful one, since it
exposed the crawler-strip correlation. **Not** fixed-and-rerun: the evidence is already
conclusive (2 cleanly-populated GOs + 1 explained empty). Recorded, per the reel-recon
discipline (*"'blocked/limited/empty' is a hypothesis — verify the mechanism before recording
a verdict"*).

## Phase 2 — bounded snowball (2026-06-15): GO mechanics + two design requirements

Pure-wpi walk from `jeremyfragrance` (fragrance), 15 logged-out reads, 2-hop BFS, hard cap.
Raw: `orca-harness/_test_runs/related_snowball/{nodes.jsonl, summary.json}`.

**Mechanics — GO:**
- **Pure-wpi populates `edge_related_profiles` WITHOUT a profile-page nav** → sidesteps the
  crawler-strip (Caveat 1 mitigated); empty rate fell to **1/15** (`elijahfragrance`, likely an
  account opt-out — so the strip was nav-triggered, not a wpi property).
- **15 consecutive wpi reads, all HTTP 200, no 401/429** → wpi's own logged-out ceiling is **≥15**.
- **Follower count per node** (`edge_followed_by.count`) confirmed → follower-band filter runs on
  the same fetch.
- **Expansion + saturation:** 15 fetches → **243 unique accounts**; **69 appear in >1 related set**
  → the sub-niche community **closes on itself** (converges, not infinite sprawl).

**Two design requirements (not blockers):**
- **Sub-niche coherence degrades at depth via bridge nodes → a coherence filter is GATING, not
  polish.** A single legitimate-but-off-niche neighbor (`@Bible`, a real `jeremyfragrance`
  relation — he posts Christian content) injected a whole **religious cluster** at depth-2;
  **skincare** also bled in (cerave, eucerin, neutrogena). Raw snowball without a sub-niche
  classifier/pruner produces a poisoned roster (owner 2026-06-15: *"worthless without polish, we
  definitely need so"*). This **elevates the sub-niche classification layer from nice-to-have to
  required** (ontology `SubNiche` / keyword filter / bridge-node pruning).
- **A mega seed surfaces mid-tier, not the rising cohort.** Follower **min 184k / median 438k /
  max 3.1M** — none micro/nano. Reaching the rising tier (**working def: micro ~10k–100k**; owner
  proposed 50k–100k; momentum is really *trajectory*, not absolute size) needs **deeper snowball
  from smaller nodes / smaller seeds**, not a one-hop walk from a mega account.

## Residuals / not-proven (post-Phase-2)

- **Sub-niche coherence filter DESIGN** — now gating; how to classify/prune bridge nodes
  (ontology `SubNiche` / keyword) is unbuilt.
- **Rising-tier reach** — deeper snowball from smaller seeds to surface ~10k–100k; untested.
- **Production at-scale** — n=3 (Phase 1) + 15 reads (Phase 2) are feasibility, **not** an at-scale
  validation; wpi's ceiling beyond ~15 consecutive reads is unmeasured.
- **Discovery-read posture** — whether production roster-building read volume is governed by the
  carve-out (owner-owned, open).
- **Empty-cause** — `elijahfragrance`/`hyram` empties: account opt-out vs strip not fully
  disambiguated (pure-wpi made it rare, ~1/15).

## Posture

Ran under the same **attended, disposable, logged-out recon** posture as the reel-view-count
recon (`docs/decisions/wind_caller_calibration_carveout_v0.md`). Phase-2 / production discovery
**read volume** (enumerating many candidate profiles to build a roster) is the open posture
question flagged in the discovery spec — owner-owned, to settle before any at-scale discovery
run.

## Non-claims

A recon GO (n=3), not a build go, validation, readiness, acceptance, at-scale, or legal claim.
Free-/account-level behaviour (opt-out vs crawler-strip) is **inferred, not confirmed**. Nothing
committed beyond this finding + the spec status flip + the recon-index row; the probe and raw
bodies are gitignored disposable scratch.
```
