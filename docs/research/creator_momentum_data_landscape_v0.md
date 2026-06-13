```yaml
retrieval_header_version: 1
artifact_role: Research reference — creator-momentum data landscape + durable-vs-transient proof plan (non-authorizing)
scope: >
  Consolidated, verified landscape of HISTORICAL creator/influencer engagement data sources
  (free/academic + commercial), the durable-vs-transient creator-momentum proof plan, the
  forward-capture / moat reality (and why a capture farm is NOT required), and the license split
  that governs commercial use. Distilled from two de-correlated research passes (2026-06)
  + a third verification pass (2026-06-13, live-fetch confirmed).
use_when:
  - Choosing a data source to prove or develop the durable-vs-transient creator-momentum judgment.
  - Deciding buy-vs-capture for forward creator-engagement data, and whether a capture farm is needed.
  - Checking the license posture (research-only vs commercial-clear) of a creator dataset before use.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - A new creator-engagement dataset or provider materially changes the menu.
  - The owner accepts a wedge / proof decision that supersedes this plan.
  - License terms verified directly with a provider differ from what is recorded here.
```

# Creator-Momentum Data Landscape + Durable-vs-Transient Proof Plan (v0)

## The one verdict (two independent research passes; refined by a third verification pass, 2026-06-13)

**No open, post-2022, RICH-ENGAGEMENT creator-level longitudinal panel exists for the core
surfaces (TikTok / Instagram)** — repeated *engagement* (likes/comments/shares) on the *same*
creators across months/years. That precise intersection — trajectory + engagement-quality, over
time, on TikTok/IG, post-2022, open-license — is still not on the shelf.

**Refinement (third pass, 2026-06-13 — verified by live fetch):** the earlier blanket "nothing
exists anywhere" was too strong. Two open, CC-BY **YouTube** longitudinal panels DO exist (now in
the table below): **YouNiverse** (rich engagement — weekly subs+views + per-video likes/comments —
but ends Sep 2019, so method-training/calibration, not the live window) and **TubeCensus** (106M
channels, subscriber trajectory 2006–2023, i.e. *post-2022* — but subscriber-count only, no
engagement). Neither hits the post-2022 × rich-engagement × core-surface intersection; both are
usable. On the commercial side, **Tubular Labs** carries post-2022 multi-platform early-velocity
engagement (views/engagement at days 1/2/3/7/30 post-upload) on the same creators — but its API ToS
forbids redistributing/reselling the data, so it is a validation/internal input, not a
ship-the-data source.

**Consequence:** the durable-vs-transient *trajectory* signal is **build-forward**. But the **moat
is the JUDGMENT** (durable-vs-transient, once proven discriminable) + your derived quality-over-time
score — **not** exclusive data and **not** a capture farm. Anyone can buy the raw forward data; no
one else has the judgment.

## The proof is free (~$0) — the stack that matters, by role

| Dataset | Role | Platform | Real trajectory? | Engagement-quality signal | License | Cost |
|---|---|---|---|---|---|---|
| **Global YouTube Trending 2022–25** (Illinois Data Bank) | **backtest spine** | YouTube | **Yes** (3-yr daily, same videos) | views + comments (no likes/shares) | **CC BY 4.0 — commercial-clear** | free |
| **ksb2043** (Kim, WWW'20) | IG validation | Instagram | No (single scrape) | likes + comments; beauty-categorized | **research-only** (form) | free |
| **TikTok-10M** (HF, The-data-company) | quality classifier | TikTok | No (snapshot) | richest free: plays/likes/comments/shares/saves | "other" → treat **research-only** | free |
| **tarekmasryo YT/TikTok Trends 2025** | commercial quality benchmark | YT + TikTok | No (snapshot) | like/comment/share/**save**-rate | **CC BY 4.0 — commercial-clear** | free |
| **"Climbing Influence Tiers"** (ICWSM'24) | TikTok tier structure | TikTok + YT-Shorts | No | likes; 5,000 creators stratified Nano→Mega | unconfirmed (research) | free (hydrate) |
| **YouNiverse** (EPFL, ICWSM'21) | method training/calibration | YouTube | **Yes** (weekly, ~2.8 yr) but →Sep 2019 | weekly subs+views deltas + per-video likes/comments | **CC BY 4.0 — commercial-clear** | free (~112 GB) |
| **TubeCensus** (ICWSM'26) | post-2022 subscriber-trajectory panel | YouTube | **Yes** (subscriber snapshots 2006–2023) | **subscribers only** (no engagement) | **CC BY 4.0 — commercial-clear** | free (~16 GB; `pip install tubecensus`) |

**The 3-step proof plan:**
1. **Discriminability backtest** — Global-YT-Trending (real visibility trajectory) + ksb2043 (IG; label outcomes by looking creators up *now*) → does early signal sort durable from transient, beating the "hottest-now" baseline. *(Caveat: Global-YT-Trending is trending-list **presence**, a proxy for durable momentum, not organic follower trajectory — defensible, but a proxy, and YouTube not your core surface. It proves the **method**.)*
2. **Quality classifier** — develop "what high-quality engagement looks like" on the snapshot sets (TikTok-10M / tarekmasryo).
3. **Trajectory + quality-over-time** — **forward-build** (the moat). No one sells it *open*; the closest, Tubular Labs, is ToS-locked against redistribution (see vendors below).

**Additionally surfaced (2026-06-13 scout pass, NOT yet fetch-verified — leads for a next pass, not menu entries):** TikTok-200K (lingbow, HF; daily engagement sub-tables, CC-BY-NC) · BlueTempNet (Bluesky, 1-yr temporal) · Patreon creator-economy panel (ICWSM'22; patron-count trajectories, contact-author) · Traackr (multi-platform vendor, ~$32–55k/yr) · 400-creator IG 12-yr panel (Bertaglia'24, blocked by CrowdTangle's 2024 shutdown).

## Do we need a capture farm? No — forward capture is buyable / outsourceable

TikTok's Research API is **research-only (no commercial use)** — which is exactly why you go to
*commercial* vendors, **not** a self-run evasion farm:

| Provider | What it's for | Trajectory | License posture | Rough cost |
|---|---|---|---|---|
| **CreatorDB** | history + quality in one feed *(if verified)* | claims 4+ yr | application-gated | from ~$79/mo |
| **Social Blade** | retrospective follower/like *surface* history | Yes (daily, ≤10 yr) | commercial-ish (inquiry) | by inquiry |
| **Exolyt** | **forward** TikTok history (prospective) | Yes (from start; Advanced ≥1 yr) | commercial-positioned | ~$680/mo (Advanced) |
| **Pentos** | **forward** TikTok history (prospective) | Yes (prospective) | commercial-positioned | ~$49–99/mo |
| **Bright Data** | commercial-clear **current** TikTok data | No (snapshot, monthly) | **commercial-clear**; vendor bears ToS | $250 / 100k records |
| **Apify** | scrape-infra to **build your own** forward trajectory | build-your-own | commercial platform; ToS risk on operator | from ~$1.70 / 1k |
| **HypeAuditor** | current authenticity audit (a possible input) | n/a | sales-led | ~$3k/yr+ |
| **Tubular Labs** | early-velocity engagement (views/eng at days 1/2/3/7/30 post-upload), multi-platform, same-creator | Yes (multi-yr, longitudinal) | **NOT redistributable** — API ToS forbids resale/syndication/3rd-party use; validation/internal only or bespoke license | sales-gated, not public (~$27.5k/yr median, Vendr) |

- **Buy/outsource forward** (Exolyt/Pentos prospective · Bright Data current · Apify build-your-own), **or** self-capture *modestly* (sentinel+zoom + a few **genuinely-independent** accounts at human rate).
- A **simulated-independence farm** is only a question at *exhaustive + high-frequency self-capture* — and even there the answer is "pay a vendor," not "build a farm." The line stays: genuinely-independent accounts = fine; proxy-puppets-faking-independence = no.

## License split (the load-bearing buy-time gotcha)

- **Commercial-clear (use for anything that ships):** Global-YT-Trending (CC BY) · tarekmasryo (CC BY) · **YouNiverse (CC BY)** · **TubeCensus (CC BY)** · Bright Data · Exolyt/Pentos (commercial-positioned — confirm ToS in writing).
- **Research-only / redistribution-restricted (validation/learning only, or get written commercial terms):** ksb2043 · TikTok Research API · TikTok-10M ("other" → treat as research-only) · **Tubular Labs (API ToS forbids redistribution/resale — internal validation only without a bespoke license)**.
- **Rule:** prove/develop on commercial-clear data for the shippable product; treat research-only sets as validation only. Get any commercial license **in writing** before relying on it.
- **ksb2043 access:** a Google Form (to Seungbae Kim, UCLA) that requires agreeing to *research/education only* → it is a research/validation corpus, not commercial product data, unless commercial terms are cleared separately.

## Sources

- [Global YouTube Trending 2022–25 (Illinois Data Bank)](https://databank.illinois.edu/datasets/IDB-9307654) · [paper](https://arxiv.org/abs/2510.23645)
- [ksb2043 (GitHub)](https://github.com/ksb2043/instagram_influencer_dataset) · [request page](https://sites.google.com/site/sbkimcv/dataset/instagram-influencer-dataset)
- [TikTok-10M (HF)](https://huggingface.co/datasets/The-data-company/TikTok-10M) · [tarekmasryo YT/TikTok Trends 2025](https://www.kaggle.com/datasets/tarekmasryo/youtube-shorts-and-tiktok-trends-2025)
- [Climbing Influence Tiers on TikTok (ICWSM'24)](https://ojs.aaai.org/index.php/ICWSM/article/view/31405)
- [YouNiverse (Zenodo 4650046)](https://zenodo.org/records/4650046) · [code](https://github.com/epfl-dlab/YouNiverse) · [paper](https://arxiv.org/abs/2012.10378)
- [TubeCensus (Zenodo 18267682)](https://zenodo.org/records/18267682) · [paper](https://arxiv.org/abs/2605.06999) · [code](https://github.com/blast-cu/tubecensus)
- [Tubular Intelligence](https://tubularlabs.com/products/tubular-intelligence/) · [API ToS — no redistribution](https://tubularlabs.com/tubular-labs-online-api-terms-of-service/)
- [TikTok Research API](https://developers.tiktok.com/products/research-api/) · [Research Tools ToS (commercial prohibited)](https://www.tiktok.com/legal/page/global/terms-of-service-research-api/en)
- [Exolyt pricing](https://exolyt.com/pricing) · [Pentos](https://pentos.co) · [Bright Data TikTok influencers](https://brightdata.com/products/datasets/tiktok/influencers) · [Apify TikTok scraper](https://apify.com/clockworks/tiktok-scraper) · [Social Blade dev](https://socialblade.com/developers) · [CreatorDB Data API](https://creatordb.app/dataapi/)

## Non-claims

Reference only; not validation/readiness/acceptance/legal advice. Licenses are as-found in 2026-06
research and **must be confirmed with each provider before commercial use**. Verdicts are
as-reported by the cited sources; the "no longitudinal panel exists" finding is a search result
(absence of evidence), not a proof of non-existence.
