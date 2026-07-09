```yaml
retrieval_header_version: 1
artifact_role: proposed capability spec (non-authorizing) — IG creator discovery (creator-momentum pipeline, capability 1)
scope: >
  Proposed design for DISCOVER — capability 1 of the IG creator-momentum pipeline
  (discover -> deep-capture -> per-call curves). Builds a creator ROSTER organized
  by beauty SUB-NICHE and follower band, covering BOTH established and rising
  creators. Names the discovery spine (our own IG-native scraping), the backfill
  layer (free creator-DB tier), the sub-niche classification owner, and the one
  unproven gating dependency to probe first. Design only: not a finding, build-go,
  or validation.
use_when:
  - Scoping or building the discovery (roster-assembly) stage of the IG creator-momentum pipeline.
  - Deciding how rising vs established creators are sourced, or how sub-niche is assigned.
  - Before launching the suggested-accounts-edge feasibility probe (the gating unknown).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_reel_viewcount_capture_feasibility_recon_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
stale_if:
  - Phase 2 (snowball depth / sub-niche coherence / follower bands / crawler-strip retry) lands.
  - IG changes the web_profile_info payload or moves edge_related_profiles behind auth.
  - The ontology backbone is adopted and SubNiche becomes a live classifier (this doc's forward-link resolves).
  - The carve-out is further amended beyond the 2026-06-15 recording (≤10 ceiling on our own
    operating/capture accounts is now owner-accepted and recorded; subject roster uncapped — see
    carve-out 2026-06-15 amendment).
status: PROPOSED — discovery design; suggested-accounts edge FEASIBILITY-PROVEN logged-out (Phase 1 + 2); sub-niche filter is GATING; rising-tier depth + production at-scale pending
```

# Instagram Creator Discovery — Spec (proposed, v0)

## Where this sits

Capability **1 (DISCOVER)** of the 3-capability creator-momentum pipeline:
**discover → deep-capture → per-call curves.** Output is a creator **ROSTER**
organized by beauty **sub-niche** and **follower band**, covering **both
established and rising** creators. The roster feeds capability 2 (deep-capture of
each rostered creator's window) and capability 3 (repeat over time → momentum +
follower trajectory). This is the proposed design for capability 1 only — not a
finding, a build-go, or a validation.

## The requirement: both cohorts

- We need **established AND rising** creators (owner, 2026-06-15).
- Creator databases **systematically miss the rising cohort** — they index
  creators who have already arrived (media kits, established metrics). For a
  *momentum* product the rising cohort is the most valuable, so a DB-first spine
  points at the wrong cohort.
- Therefore: **our own IG-native scraping is the spine** (covers rising by
  construction); a **free creator-DB tier is backfill** (established tail +
  metrics). "Prefer free" (owner) is honored — the spine is IG-native (free) and
  backfill uses free DB tiers only.

## Discovery spine — our own scraping (the 3 mechanisms)

1. **Suggested-accounts edge** — IG's "similar accounts" graph. Seed a few known
   creators per sub-niche → expand to adjacent accounts, which skew *rising*
   (that's who the algorithm clusters as "similar but smaller").
   **FEASIBILITY-PROVEN logged-out (Phase 1, 2026-06-15, n=3):** the edge is
   `data.user.edge_related_profiles` in the `web_profile_info` JSON (the tolerant
   200-cookieless surface), populated logged-out (19 and 32 related accounts for
   two seeds; sub-niche-coherent), each node carrying `username`+`id` (so the
   snowball is feasible). See
   `ig_creator_discovery_suggested_accounts_recon_v0.md`. Snowball depth,
   sub-niche coherence at depth, follower bands, and the crawler-strip retry are
   **Phase 2**.
2. **Collab / mention traversal** — walk tagged collaborators and `@`-mentions
   from seed/rostered posts. Emerging creators collab to grow, so this snowballs
   the same sub-niche.
3. **Follower-band + sub-niche filter** — reduce the expanded set to the target
   momentum tier and confirm sub-niche (next section). **Rising-tier working
   definition: micro ~10k–100k** (owner proposed 50k–100k; momentum is really
   *trajectory*, not absolute size — adjustable). Phase 2 showed a mega seed
   surfaces only mid-tier (≥184k), so reaching the rising band needs **deeper
   snowball from smaller nodes/seeds**. Follower count is one wpi hop per candidate
   (`edge_followed_by.count`).

## Backfill layer — free creator-DB tier

- Free/freemium tools that enumerate by niche + follower count: **ShortsIntel**
  (free, no signup; filters by niche + follower size; returns handle, followers,
  engagement, niche tags), **Lessie AI** (free, country + niche), **HypeAuditor /
  Heepsy** free tools.
- **Role:** the established tail + clean follower/engagement metrics to enrich and
  cross-check the roster. **Complementary, not the spine.** Free tiers are capped
  (limited results/depth) and skew established — which is exactly why they are not
  the rising-cohort source.

## Sub-niche classification

**Phase 2 made this GATING, not polish.** A single off-niche bridge node (e.g.
`@Bible`, a real fragrance-creator relation) injects a foreign community at depth-2,
so raw snowball without a sub-niche filter produces a poisoned roster (owner
2026-06-15: *"worthless without polish, we definitely need so"*). The filter below
is a **build requirement**, not an enhancement.

- The roster unit is a beauty **sub-niche** (skincare, K-/J-beauty, fragrance,
  indie/clean, makeup-artistry, men's grooming, haircare, …), **not "beauty"
  broadly.**
- **Owned by the ontology, not hashtags.** Sub-niche classification is designed to
  live in the ontology's **`SubNiche`** object type — a candidate object in the
  ontology backbone commission
  (`docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md`).
  **Build-state caveat:** that ontology is a *not-yet-dispatched* commission
  (`AUTHORED_2026-06-13_AWAITING_DISPATCH`), so `SubNiche` is a **forward owner,
  not a shipped classifier.** Until adoption, classify by bio/caption keywords +
  the graph cluster itself, to be re-expressed in `SubNiche` terms on adoption.
- **Hashtags deprioritized.** Grounded 2026 state: IG's Mosseri — hashtags
  *"categorize content, they don't boost reach"*; a hard **5-tag cap** since Dec
  2025; so **hashtag-rate is a weak momentum feature** and a weak discovery axis.
  Keep hashtags only as a cheap *secondary corroboration* signal for the
  classifier — never the classifier itself, and not the discovery spine.

## Probe status

- **Phase 1 — reachability: DONE, GO logged-out** (2026-06-15, n=3). The edge is
  `data.user.edge_related_profiles` in `web_profile_info`, populated logged-out, no
  off-IG dependency. Full finding:
  `ig_creator_discovery_suggested_accounts_recon_v0.md`; recon-index row in
  `capture_recon_index_v0.md`.
- **Phase 2 — bounded snowball: DONE, GO mechanics** (2026-06-15, 15 logged-out
  reads). Pure-wpi walk (no profile nav) populates `edge_related_profiles` and
  sidesteps the crawler-strip; 15 reads all 200 (wpi ceiling ≥15); 15 fetches → 243
  unique accounts, 69 multi-set → bounded community. **Two design requirements
  surfaced** (see below): a sub-niche coherence filter (now gating) and rising-tier
  depth. Finding: `ig_creator_discovery_suggested_accounts_recon_v0.md`.
- **Still gated / unbuilt:** the sub-niche filter design, rising-tier reach (deeper
  snowball), production at-scale validation, and the owner discovery-read posture
  ruling.

## Posture / carve-out boundary

- Discovery enumerates a **candidate roster**, which may exceed the capture cap.
  Deep-capture/tracking (capabilities 2–3) operates at the carve-out account cap:
  the ≤10 ceiling on our OWN operating/capture accounts (ops start ≤5) is now
  **RECORDED** (carve-out 2026-06-15 amendment) and is load-bearing. The cap counts
  **our own capture/operating accounts, not subject creators** — the subject-creator
  roster is **uncapped** (all creators in the vertical are in scope).
  `docs/decisions/wind_caller_calibration_carveout_v0.md` is the authoritative cap doc.
- **Active/passive method posture (RESOLVED 2026-06-15):** ACTIVE (discovery + capture
  decisions) = attended (human-initiated). PASSIVE (monitoring already-flagged creators)
  = human-initiated, time-bounded, self-terminating — no discovery during passive
  monitoring; NOT a perpetual or scheduled standing crawler. Faster-than-human cadence;
  ToS-accepted.
- **Posture question on discovery-stage reading volume (RESOLVED 2026-06-15):** active
  discovery (building the roster) is governed by the active-attended posture — each
  discovery run is human-initiated. At-volume roster-building is therefore **permitted**
  under the active-attended posture (not a standing crawler; each run is owner-launched).
  Passive monitoring of already-flagged creators is bounded and self-terminating. No
  further flag needed before at-volume discovery runs conducted under the attended posture.
- *(direction_change_propagation 2026-06-15: carve-out 2026-06-15 amendment — cap now
  recorded/load-bearing; ≤10/start-5 counts own operating/capture accounts; subject-creator
  roster uncapped; active/passive method posture defined and the open discovery-reading
  posture question resolved by the active-attended ruling.)*

## Non-claims

Proposed capability design only — not a finding, build-go, validation, readiness,
or commercial/legal authorization. The suggested-accounts edge is
**feasibility-proven logged-out (Phase 1, n=3)** — a recon GO, not a build or
at-scale claim; snowball/Phase 2 is pending. Free-tool capabilities are **vendor
claims**, not verified by us. The sub-niche/ontology ownership is a **forward
design link** to a not-yet-adopted ontology.

## Grounding (external, 2026)

The "DBs miss rising creators," free-tool, and 2026-hashtag claims above are from
public web sources read 2026-06-15 (vendor/marketing and platform-guide pages —
treat as directional, not validated): Modash *"14 ways to find micro-influencers
(free & paid)"*; YouScan *"how to find micro-influencers in 2026"*; ShortsIntel /
Lessie AI free discovery tools; Later *"Instagram hashtags in 2026, the 5-tag
limit"* and funnl.ai *"do Instagram hashtags work in 2026."*
