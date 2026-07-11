# Aphrodite Growth Strategy Map v0

```yaml
retrieval_header_version: 1
artifact_role: Growth/monetization strategy MAP — EXPLORATORY register (not ratified doctrine; the charter is the ratified spine)
scope: >
  Durable index + staging ground for Aphrodite's growth / monetization / expansion
  strategy that is NOT yet owner-ratified and NOT confined to one design lane: the
  two-company architecture (Aphrodite / Aphrodite Studio), the buyer ladder and
  price-tag scaling, the corpus/domination reasoning, the capture-and-media scope,
  and the no-registry-dump rule. Captures decisions made in-thread, indexes the
  active design lanes, and routes ratified content to the charter.
use_when:
  - Locating where an Aphrodite growth/monetization/expansion idea lives.
  - Checking what is decided (→ charter) vs exploratory (here) for growth strategy.
  - Sequencing the design lanes (Studio, rising-creators, capture) under one index.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md   # the RATIFIED spine — decided content lives there, not here
  - forseti/product/spines/creator_signal/creator_signal_market_sizing_v0.md
  - forseti/product/spines/creator_signal/creator_signal_product_architecture_v0.md
  - docs/research/aphrodite_creator_capture_strategy_v0.md
stale_if:
  - The owner ratifies a piece here (promote it to the charter via dated amendment; then its row points to the charter).
  - The charter supersedes or amends a routed decision.
  - A design lane is built and produces its own durable artifact (point to it).
```

## Status — EXPLORATORY, not ratified

This is the **staging ground** for Aphrodite growth strategy, not doctrine. The
**charter is the single ratified spine**; everything here is owner-explored or
proposed unless the Decided table below routes it to the charter. Nothing here is
a decision, validation, readiness, willingness-to-pay, or buyer-proof claim.
Authority **migrates out** of this map into the charter when ratified — it never
accumulates here. That is what keeps this from becoming shadow-doctrine.

## Decided (→ charter) vs Exploratory (here)

| Item | State | Home |
| --- | --- | --- |
| Moat = position not extraction (niche domination) | RATIFIED | charter §3 (sharpened 2026-07-08, PR #799) |
| Lead buyer lane = indie/DTC incl. clone houses | RATIFIED | charter §5 |
| First unit = paid Vetting Sprint (5 panels) | RATIFIED | charter §4 |
| Phases 0–3; foundation-first | RATIFIED | charter §2 |
| Two-company architecture (Aphrodite / Studio) | EXPLORATORY | §A below |
| Buyer ladder + price-tag scaling | EXPLORATORY | §B (pricing deferred → charter D-2) |
| Corpus/domination sizing (~2K → ~25–40K) | EXPLORATORY | §C (market-sizing deferred the resize) |
| Media/hooks capture scope | OWNER-DECIDED in-thread, NOT yet charter-amended | §D (needs §6 amendment + ToS re-gate) |
| No-registry-dump rule | EXPLORATORY (application of existing forbidden set) | §E |

## A. Two-company architecture
- **Aphrodite** — neutral creator intelligence; sells decisions/reads; keeps the forbidden set (no contact/outreach/lead-export).
- **Aphrodite Studio** — a SEPARATE company; a data-advantaged creator agency that *acts on* the alpha (enablement intel + rising-creator scouting). It does outreach/contact/management — which is *why* it must be separate: that surface is forbidden inside Aphrodite.
- **Firewall** — disclosure + provenance keep Aphrodite's neutrality while Studio runs a roster.
- **Consume-not-author** — Studio consumes derived decisions; the registry / data authority stays inside Aphrodite (prior placement: the capture-strategy doc).

## B. Buyer ladder + price-tag scaling
- **Ladder:** indie → challenger/scale-up DTC → big brands (a *displacement* sale vs CreatorIQ/Traackr, winnable on fragrance depth, not greenfield) → **VC/PE/diligence (high-ceiling, different sales motion; deferred, charter D-5)**.
- **Upstream vs downstream:** bigger tags come *upstream* (the same domination position sold to bigger wallets/decisions) or *downstream* (Studio acts on it) — never from overcharging indie brands (budget-capped) or from selling the registry.
- **Value-based pricing:** price on the decision de-risked; big numbers only where the decision is big → requires the buyer climb.
- **Ceiling honesty:** the retainer sits under CreatorIQ's ~$30–60k/yr because the *buyer's budget* differs, not because the data is worse. Aphrodite's creator increment (unlike a demand-intel product) does not shrink against a brand's internal data — it is outside-in and niche-complete.
- Pricing frame itself is **deferred → charter D-2**.

## C. Corpus + domination reasoning
- **Dominable corpus (primary/influential, not mention-based):** fragrance ~1.5–3K → **beauty ~25–40K**, conquered sub-niche by sub-niche (skincare/makeup/haircare each rebuild ontology depth). The ~300K "beauty creator" figure is *mention-based* noise, not the target.
- **Domination is achievable only in a niche small enough to fully capture, and defensible only in one too small for a horizontal incumbent to contest.** Expand by sequential sub-niche domination, not broad-shallow.
- The market-sizing doc deferred this cohort resize; this is the current read, not a re-derivation of that doc.

## D. Capture + media/hooks scope (owner-decided in-thread; needs charter §6 amendment)
- **Tiers:** T1 metadata (all videos, cheap) · T2 transcript + comments (stratified; YT text captions / TikTok captions / IG ASR) · **T3 first-3s hooks (NEW, stratified to breakouts)** feeding Studio's creator-enablement product.
- **Method:** real capture is **browser (cloakbrowser)**; **no segment/range fetch for TikTok/IG** (strict anti-bot); hooks are captured by **intercepting the media the browser already fetches during deep capture** (human footprint, no extra request, original bytes; re-encode acceptable).
- **Egress:** SG mobile-data SIMs via a SIM-bank/modem-pool (mobile-IP hygiene at consumer prices), 1 → 16 (up to 30) SIMs; one host drives many modems (no VM-per-SIM). **US egress only for the bounded TikTok-Shop US slice.** SG geo is fine for followed-content capture.
- **Cost shape:** capture is bandwidth-modest (metadata is text; hooks are 3s). The scaling costs are egress *count* (per-IP safe rate), the audience-geo data vendor, and LLM token processing (bounded by stratification + cheap-model-for-bulk + deterministic-where-possible).
- **⚠ Charter implication:** this consciously extends charter §6's media-light scope + re-opens the ToS-risk gate → needs a dated §6 amendment + a ToS re-check before any capture build. FLAGGED, not applied.

## E. No-registry-dump rule
Selling the raw registry (Excel/SQL) would convert the position-rent into a one-time sale and arm the buyer to not need you — and it is exactly the **lead-list export / person-level directory the charter's forbidden set already prohibits** (§3 moat protectors; spine README boundary). Sell **derived value** (reads, rankings, decisions) or controlled query access, never the dump. The only "sell the registry" that is right is at **acquisition** (selling the company/position). This is an *application* of existing doctrine, not a new rule.

## F. Design-lane index (current scaffolds — scratch, regenerable from this map)

| Lane | Status | Scaffold (ephemeral scratch) |
| --- | --- | --- |
| B2B outreach motion (first Vetting Sprints) | active | `docs/_inbox/aphrodite_b2b_outreach_lane_handoff_v0.md` |
| Aphrodite Studio design | exploratory | `docs/_inbox/aphrodite_studio_design_lane_handoff_v0.md` |
| Rising-creators / breakout (× ad-load) | exploratory; MGT/SCI-adjudicated input | `forseti/product/spines/creator_signal/aphrodite_breakout_acceleration_mgt_sci_adjudication_v0.md` (scratch scaffold: `docs/_inbox/aphrodite_rising_creators_breakout_lane_handoff_v0.md`) |
| Capture byte-measurement probe | active | `docs/_inbox/aphrodite_capture_lane_hooks_and_probe_handoff_v0.md` |
| Own-growth research-engine GTM (outreach inputs · SEO · AEO · CreatorIQ CI · inbound→gate) | design landed (Phase-0) | `forseti/product/spines/creator_signal/aphrodite_research_engine_gtm_design_v0.md` |
| D-2 pricing frame | deferred | charter register D-2 |
| D-5 diligence / evidence-buyer lane | deferred | charter register D-5 |

The scaffolds are ephemeral (they wipe on worktree recycle); their load-bearing
**decisions are captured in §A–E above**, so a lost scaffold is regenerable from
this map.

## Lifecycle (explore → ratify → amend-into-charter)
1. Strategy is explored here (exploratory).
2. Owner ratifies a piece.
3. It is promoted into the **charter** via a dated amendment + `direction_change_propagation` receipt (as the moat sharpening was, PR #799).
4. The Decided table above flips that row to point at the charter.

Ratified content leaves the map for the charter; the map only ever holds
exploratory + connective + index.

## Non-claims
Exploratory strategy map only; changes no ratified doctrine and carries no
`direction_change_propagation` receipt because it enacts none. Not validation,
readiness, willingness-to-pay, buyer proof, or a build / capture / outreach
authorization. Each design lane and each future charter amendment keeps its own
authorization boundary. The media/hooks scope (§D) is owner-decided in-thread but
is NOT charter-ratified until its §6 amendment + ToS re-check land.
