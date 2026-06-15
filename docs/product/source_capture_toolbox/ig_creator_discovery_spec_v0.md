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
  - docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md
  - docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md
stale_if:
  - The suggested-accounts-edge feasibility probe lands (moves mechanism 1 from UNPROVEN to GO/NO-GO).
  - IG changes the suggested-accounts surface, the profile-feed payload, or the grid doc_id.
  - The ontology backbone is adopted and SubNiche becomes a live classifier (this doc's forward-link resolves).
  - The carve-out is amended (e.g. the floated <=10-account cap is recorded).
status: PROPOSED — discovery design; suggested-accounts-edge feasibility UNPROVEN (next probe)
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
   **UNPROVEN gating dependency:** does IG expose this edge **logged-out** (the
   way `web_profile_info` exposed the feed)? → the next probe, below. Same lane
   and shape as the reel-view-count recon.
2. **Collab / mention traversal** — walk tagged collaborators and `@`-mentions
   from seed/rostered posts. Emerging creators collab to grow, so this snowballs
   the same sub-niche.
3. **Follower-band + sub-niche filter** — reduce the expanded set to the target
   momentum tier (follower band) and confirm sub-niche (next section).

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

## Next probe (the one gating unknown)

**Suggested-accounts-edge feasibility, logged-out** — same template as the reel
recon (`ig_reel_viewcount_capture_feasibility_recon_v0.md`): does IG return the
related/suggested-accounts edge **cookieless** (on which surface/endpoint), and
how deep before the grid-style **~35-anon-req/window → HTTP 401** ceiling bites
(see the consolidated findings note). Probe-first, before any discovery build; the
result lands as a `capture_recon_index_v0.md` row. If it returns logged-out, the
whole pipeline runs on **one IG substrate** with no off-IG discovery dependency.

## Posture / carve-out boundary

- Discovery enumerates a **candidate roster**, which may exceed the capture cap.
  Deep-capture/tracking (capabilities 2–3) operates at the carve-out account cap:
  owner confirmed (2026-06-15) intent to raise it from **≤5** to **≤10** rotating
  accounts. This still needs a **recorded dated amendment** to
  `docs/decisions/wind_caller_calibration_carveout_v0.md` before it is
  load-bearing; the spec defers to that doc as the authoritative cap.
- **Open posture question (surfaced, not resolved):** whether discovery-stage
  *reading* volume (suggested-accounts/profile reads to build the roster) is
  itself governed by the carve-out, or only the **retained** capture set is. Flag
  for owner before any at-volume discovery run.

## Non-claims

Proposed capability design only — not a finding, build-go, validation, readiness,
or commercial/legal authorization. The suggested-accounts edge is **UNPROVEN**.
Free-tool capabilities are **vendor claims**, not verified by us. The
sub-niche/ontology ownership is a **forward design link** to a not-yet-adopted
ontology.

## Grounding (external, 2026)

The "DBs miss rising creators," free-tool, and 2026-hashtag claims above are from
public web sources read 2026-06-15 (vendor/marketing and platform-guide pages —
treat as directional, not validated): Modash *"14 ways to find micro-influencers
(free & paid)"*; YouScan *"how to find micro-influencers in 2026"*; ShortsIntel /
Lessie AI free discovery tools; Later *"Instagram hashtags in 2026, the 5-tag
limit"* and funnl.ai *"do Instagram hashtags work in 2026."*
