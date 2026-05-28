# Data Capture Source-Access Method Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Docs-only method plan comparing candidate source-access methods against the loosened boundary standard and recommending approaches per blocked source. No build authorization.
use_when:
  - Evaluating or selecting source-access methods for Orca Data Capture.
  - Scoping a build of source-access tooling after receiving explicit owner authorization to exit the non-implementation phase.
  - Checking which methods are in-bounds under the public-data + disclosable standard.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_source_access_boundary_decision_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
stale_if:
  - The boundary decision is amended or superseded.
  - The obligation contract's Obligation 2 is materially revised.
  - The owner explicitly authorizes building source-access tooling (this plan is superseded by the build authorization at that point).
  - Pressure-test evidence surfaces access patterns this plan did not anticipate.
```

---

## Status

`ACCEPTED_SOURCE_ACCESS_METHOD_PLAN_V0` — patched 2026-05-28 to reflect full loosening (all methods in-bounds under public-data + disclosable standard).

Artifact type: Product artifact — docs-only method plan.
Produced: 2026-05-28. Patched: 2026-05-28.
Phase: Orca non-implementation phase. No build, no install, no runtime authorized.
Edit permission: docs-write (this file only).
Controlling standard: `docs/product/data_capture_source_access_boundary_decision_v0.md`.

---

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes — AGENTS.md read
  overlay_read: yes — .agents/workflow-overlay/README.md + safety-rules.md read
  source_pack: source-access method planning pack
  workspace: C:\Users\vmon7\Desktop\projects\orca
  dirty_state_allowance: dirty/untracked expected; not treated as validation
  edit_permission: docs-write (plan artifact only)
  target_scope:
    - docs/product/data_capture_source_access_method_plan_v0.md
  sources_loaded:
    - docs/product/data_capture_source_access_boundary_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/README.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
```

---

## The Controlling Standard

From `docs/product/data_capture_source_access_boundary_decision_v0.md` (patched 2026-05-28 to `LOOSEN_SOURCE_ACCESS_TO_PUBLIC_DATA_DISCLOSABLE`):

A method is **in-bounds** when **both** hold:

1. It accesses **public / market-level data only** — no authentication bypass, no paywall circumvention, no private or non-public data.
2. Orca would **fully disclose exactly how the data was obtained** if asked — no method Orca would need to conceal. "We scraped their public site" is a complete and acceptable answer.

**This permits:** scraping of public pages; JS-rendering headless browsers; rate-limited or aggressive fetching; official or sanctioned APIs; archive/cache access; **and anti-blocking techniques — anti-detect / "cloaked" browsers, user-agent and fingerprint configuration, residential or rotating proxies, and CAPTCHA / JS-challenge handling — used to reach public data a site attempts to block.**

**This still excludes (hard line, not risk-tolerance):** authentication bypass, paywall circumvention, and access to private / non-public data. These are out regardless of disclosure — accessing non-public data is not made defensible by admitting it.

**Owner-accepted risk posture:** anti-blocking techniques carry real Terms-of-Service, reputational, and (for actively-enforcing sources) litigation risk. The owner has accepted this as a deliberate, disclosable posture. Accepted risk is not a boundary question — it is recorded as an explicit owner decision and must be visible in Orca's provenance. Real legal counsel is advisable before commercializing.

---

## Blocked Sources and Root Problems

Identified in `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/README.md`:

| Source | Block type | Root problem |
|---|---|---|
| tealhq.com | HTTP 403 to all WebFetch attempts | Active bot-blocking by Teal's server |
| reddit.com / www.reddit.com / old.reddit.com | Host-level block in WebFetch | Claude Code's WebFetch tool blocks Reddit hosts entirely (tool constraint, not internet restriction) |
| wallstreetoasis.com | HTTP 403 on WebFetch | Active bot-blocking by WSO |
| web.archive.org (content) | Tool-layer block in WebFetch | Claude Code's WebFetch blocks archive.org content fetches; the availability JSON API still works |
| mergersandinquisitions.com | Not blocked; fetches OK | WebFetch returns paraphrase, not verbatim content — violates Obligation 6 (Raw Observable Preservation) |

Note on the archive.org block: the Wayback Machine availability API (`archive.org/wayback/available`) is not blocked and successfully returns snapshot metadata. Only the snapshot content URLs are blocked at the WebFetch tool layer. This is a Claude Code tooling constraint, not an archive.org access restriction. The archive is publicly accessible via any standard HTTP client or browser.

---

## Candidate Methods — Boundary Analysis

### Method 1: Official / Sanctioned APIs

**What it is:** Using a source's own publicly documented API with registered credentials. For this source pack, Reddit has an official public API; Teal and WSO do not.

**Boundary test:**
1. Public data only: YES — the Reddit API provides read access to public subreddit content.
2. Full disclosure: YES — "We accessed this source via its official API with registered app credentials" is fully defensible and disclosable.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** Reddit (r/FinancialCareers, r/CFA, and any public subreddit). No known sanctioned API for Teal or WSO.

**Practical notes:** Reddit's API provides a free tier (approximately 100 requests/minute, 1,000/day). This tier is sufficient for pressure-test-scale capture. Bulk commercial use at scale may require Reddit's data licensing program. The official API is the best available method for Reddit specifically.

**Risk:** Low for pressure-test use. Medium for commercialization — Reddit's data licensing terms should be reviewed before any product that surfaces Reddit content at scale.

---

### Method 2: Honest JS-Rendering Headless Browser

**What it is:** Automated browser (Playwright, Puppeteer, Selenium) configured with an honest user-agent that identifies as a bot, respects robots.txt, and applies crawl delays. Does not spoof fingerprints.

**Boundary test:**
1. Public data only: YES — rendering public pages.
2. Full disclosure: YES — "We used an automated browser with honest identification to fetch public pages."

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** Potentially Teal and WSO if their 403 responses are user-agent-based rather than fingerprint- or IP-based. Solves the M&I verbatim problem if configured to return raw HTML. Does not solve the archive.org WebFetch tool constraint (that block is in the tool, not the destination).

**Practical notes:** An honest headless browser may still be blocked by sites detecting headless browser signatures (Chrome DevTools Protocol flags). It is uncertain without testing whether Teal or WSO's 403s would respond to an honest UA. Worth testing before escalating to anti-detect methods.

**Risk:** Low-Medium. Some sites' ToS prohibit any automated access; hiQ v. LinkedIn provides meaningful protection for honest automated access to public data.

---

### Method 3: Anti-Detect / Stealth Browser

**What it is:** Browser automation that actively spoofs fingerprints — user-agent, canvas, WebGL, automation flags (`window.webdriver`), timing signatures — to make a bot look like a human browsing session. Tools include Playwright-Stealth, undetected-chromedriver, Browserless stealth mode.

**Boundary test:**
1. Public data only: YES — accesses public pages.
2. Full disclosure: YES under the updated standard — "We used a browser configured to bypass bot detection to scrape your public site" is a complete and disclosable answer. Orca's accepted posture is that obtaining *public* data is defensible including with anti-blocking techniques.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** Most effective against Teal and WSO, where the 403 blocks are likely fingerprint- or UA-based. The primary tool for breaking through aggressive bot-detection on public pages.

**Risk:** Medium-High. Carries real ToS, reputational, and potential litigation risk (CFAA-adjacent arguments in some jurisdictions when circumventing active anti-bot measures). The owner has explicitly accepted this risk posture. Must be disclosed in Orca's capture provenance — capture mode should record "automated extraction / anti-detect browser" under Obligation 4. Real legal counsel recommended before commercializing against actively-enforcing sources.

---

### Method 4: Residential Proxy Rotation

**What it is:** Routing HTTP requests through a pool of residential IP addresses (Bright Data, Oxylabs, Smartproxy, similar) so that traffic appears to originate from residential connections rather than a datacenter or identified bot operator.

**Boundary test:**
1. Public data only: YES — if used only for public pages.
2. Full disclosure: YES under the updated standard — "We routed requests through residential proxies to reach your public site" is a disclosable method. Orca's accepted posture covers this explicitly.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** Directly addresses IP-based blocking. Teal and WSO's 403s may be IP-range blocks (datacenter IPs) as much as bot detection — residential proxies route around this. Most effective when combined with an honest or anti-detect browser.

**Practical notes:** Residential proxies are typically combined with a browser or HTTP client. As a standalone transport layer they do not render JS; pair with a headless browser for JS-heavy pages. Many commercial services offer both proxy pools and managed browser rendering in one product (e.g., Bright Data's Web Unlocker).

**Risk:** Medium-High. Same owner-accepted risk posture as anti-detect browsers. ToS violation likely for actively-blocking sources. Disclosure to Orca's provenance chain required. Proxy provider costs are per-GB or per-request at commercial scale. Real legal counsel recommended before commercializing.

---

### Method 5: Rate-Limited Polite Fetching with Honest Identification

**What it is:** Direct HTTP GET requests with an honest user-agent string (identifying Orca or "OrcaDataBot"), crawl delay, and robots.txt compliance. No browser rendering.

**Boundary test:**
1. Public data only: YES.
2. Full disclosure: YES — trivially defensible.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** Works for sources that do not block bots (M&I for non-JS pages). Will not break through 403 blocks. Does not solve Teal, Reddit (WebFetch tool block), or WSO. Does solve the verbatim problem for static M&I pages (raw HTTP returns raw HTML, not a paraphrase).

**Practical notes:** The simplest programmatic method and the correct starting point for sources that allow bot access. For M&I production use, this may be sufficient for static pricing and product pages.

**Risk:** Very Low.

---

### Method 6: Archive / Cache Access

**What it is:** Accessing publicly available snapshots through archival services:
- Wayback Machine (archive.org): availability API works now; content accessible via browser or any standard HTTP client (only blocked in Claude Code's WebFetch tool)
- archive.ph / archive.today: User-submitted snapshots; useful for some URLs, not systematic
- Common Crawl: Open public dataset; monthly snapshots, not real-time
- Bing Cache (`cache:` operator): Occasionally available, unreliable; Google Cache largely eliminated as of 2024

**Boundary test:**
1. Public data only: YES — accessing publicly available archival copies.
2. Full disclosure: YES — "We accessed historical snapshots via the Wayback Machine / archive.ph" is fully disclosable.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:**
- Teal: Wayback Machine has snapshots of tealhq.com. Useful for historical pricing/feature state (Obligation 10).
- Reddit: Coverage of specific thread chains may be incomplete. The official API is a better route for current content.
- WSO: Wayback Machine has extensive WSO thread coverage. Useful for historical thread state, edit/deletion posture.
- archive.org content (tool block): Accessible via human browser or any HTTP client; the WebFetch tool constraint does not apply outside Claude Code.
- M&I: Wayback Machine snapshots provide the 12-24 month pricing history required by the commissioning plan's slot 1 (essential for Obligation 10).

**Practical notes:** Archive access is a complement to live fetching, not a replacement. For current-state captures, archives may lag. For historical window obligations (Obligation 10), archives are often the only option.

**Risk:** Very Low. The Internet Archive's ToS supports research and non-commercial use; commercial use is generally tolerated.

---

### Method 7: Commercial Fetch / Scraping Services

**What it is:** Third-party API services that fetch and parse web content on the operator's behalf. Includes:
- **Firecrawl**: API-first scraper, honest operation, raw content or structured data
- **Diffbot**: Structured web data extraction, self-identified crawler
- **ScrapingBee, Bright Data Web Unlocker, Zyte Smart Proxy**: Services that bundle browser rendering, proxy rotation, and anti-detect into managed APIs

**Boundary test:**
1. Public data only: YES if configured for public pages.
2. Full disclosure: YES — "We used [service] to fetch this public page" is disclosable. Under the updated standard, services that include anti-detect or proxy features are in-bounds because the underlying technique (anti-detect / proxy for public data) is itself in-bounds.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** May break through 403 blocks if the service's IP infrastructure or anti-detect handling bypasses what blocked WebFetch. For Teal and WSO specifically, managed services that include anti-detect and proxy rotation are likely the most operationally reliable production path.

**Practical notes:** Verify: (a) the service's own ToS permits Orca's use case; (b) the service's methods are logged in Orca's capture provenance as a third-party dependency (Obligation 3, Obligation 4). Reliance on a managed service means the access method is partially opaque — Orca should be able to describe at the category level what the service does (browser rendering + proxy rotation) even if exact implementation details are the service's own.

**Risk:** Medium. Cost (per-request or subscription). Third-party supply-chain dependency in the provenance chain. ToS risk inherited from the underlying techniques. Choose a service that can be named and described in Orca's provenance without requiring concealment.

---

### Method 8: Manual Human-Browser Capture

**What it is:** A human operator opens URLs in a standard web browser, reads the content, and copies verbatim text into the capture artifact. No automation.

**Boundary test:**
1. Public data only: YES — viewing publicly visible pages.
2. Full disclosure: YES — trivially and completely defensible. "A person read and copied the publicly visible content."

**Boundary verdict: IN-BOUNDS** — the most defensible method available.

**Works for which sources:** ALL blocked sources. Teal, Reddit, WSO, archive.org content, and M&I are all accessible in a standard browser. Solves both the access problem and the verbatim problem.

**Practical notes:** The obligation contract designates "human-led capture as allowed and expected for v0 bootstrap." This is not a fallback — it is the canonical mode for the current phase. The operator naturally preserves verbatim language, can capture modality (screenshots where layout matters), and directly observes page structure.

**Risk:** Very Low. Operator time is the cost. No legal, ToS, or reputational risk beyond what any reader of a public webpage incurs.

---

### Method 9: SERP APIs (Search-Engine Result Pages)

**What it is:** Services (SerpAPI, Serper.dev, etc.) providing programmatic access to search engine results. Returns snippets, titles, and URLs — not full page content.

**Boundary test:**
1. Public data only: YES — search results are public.
2. Full disclosure: YES.

**Boundary verdict: IN-BOUNDS** for URL enumeration and snippet access.

**Works for which sources:** Partial. Useful for enumerating target URLs across all source families. Already used functionally in the pressure-test via WebSearch. Not suitable as a primary capture method — search snippets cannot satisfy Obligation 6 (Raw Observable Preservation).

**Risk:** Low. Cost is per-search for most SERP API providers.

---

### Method 10: Chrome Automation via MCP (Browser-Driven)

**What it is:** An MCP tool driving a real Chrome browser instance to navigate pages, render JavaScript, and extract content. Uses a full real Chrome instance rather than a headless rendering engine.

**Boundary test:**
1. Public data only: YES if accessing public pages.
2. Full disclosure: YES — "We used automated Chrome to access this public page" is disclosable and defensible under the updated standard.

**Boundary verdict: IN-BOUNDS**

**Works for which sources:** Potentially Teal and WSO. A real Chrome instance may not expose headless browser signatures (Chrome DevTools Protocol flags are browser-controlled), making it more likely to succeed against fingerprint-based blocking than a standard Playwright headless browser.

**Practical notes:** Whether the `window.webdriver` flag is suppressed depends on the specific MCP implementation. If it is suppressed, this is substantively equivalent to anti-detect browser automation (Method 3) and inherits the same risk profile. If it is not suppressed, it behaves like an honest headless browser (Method 2). Orca should note which behavior the specific implementation exhibits in the capture provenance.

**Risk:** Low-Medium depending on implementation. Automation flag suppression moves this toward the anti-detect risk profile.

---

## Candidate Methods Summary Table

| Method | Boundary Verdict | Access Blocked Sources? | Verbatim Content? | Risk |
|---|---|---|---|---|
| Official/Sanctioned API (Reddit) | **IN-BOUNDS** | Yes (Reddit only) | Yes | Low |
| Honest Headless Browser | **IN-BOUNDS** | Maybe (UA-based blocks only) | Yes (raw HTML) | Low-Medium |
| Anti-Detect / Stealth Browser | **IN-BOUNDS** | Yes (most blocks) | Yes | Medium-High (owner-accepted) |
| Residential Proxy Rotation | **IN-BOUNDS** | Yes (IP-based blocks) | Yes (with browser) | Medium-High (owner-accepted) |
| Rate-Limited Polite Fetching | **IN-BOUNDS** | No (still blocked) | Yes (raw HTML) | Very Low |
| Archive / Cache Access | **IN-BOUNDS** | Partial (historical state) | Yes | Very Low |
| Commercial Scraping Service | **IN-BOUNDS** | Likely (managed anti-detect) | Yes | Medium |
| Manual Human-Browser Capture | **IN-BOUNDS** | Yes (all sources) | Yes (operator copies) | Very Low |
| SERP API | **IN-BOUNDS** (enumeration only) | Partial (snippets) | No (snippets only) | Low |
| Chrome MCP Automation | **IN-BOUNDS** | Likely | Yes | Low-Medium |

---

## Method-to-Source Recommendations

### Slot 1 — M&I (mergersandinquisitions.com) — paraphrase, not verbatim

**Root problem:** WebFetch returns paraphrased content, not verbatim source language. This is a tool-layer rendering and post-processing behavior, not a bot-blocking issue.

**Recommended method for pressure-test:**
1. **Human-led browser capture** (primary) — operator opens M&I pages in browser, copies verbatim pricing and product language directly into capture Markdown. Solves the verbatim problem completely.
2. **Archive/Wayback Machine** (required complement) — the slot-1 commissioning plan requires 12-24 month pricing history. The operator navigates archive.org snapshots in a browser to capture historical state for Obligation 10.

**Recommended method for production:**
- Direct HTTP client (Python requests / Node.js fetch) — returns raw HTML without post-processing; parse with BeautifulSoup or equivalent. Honest, in-bounds, solves the verbatim problem programmatically.
- Rate-limited polite fetching with honest UA for static pages.
- Honest headless browser for JS-rendered pages if needed.

---

### Slot 2 — Teal (tealhq.com) — full 403 block

**Root problem:** Teal's server actively blocks all bot-identified requests with HTTP 403. No public API exists.

**Recommended method for pressure-test:**
1. **Human-led browser capture** (primary) — Teal is publicly accessible in any standard browser. Operator opens pricing pages, feature pages, and related public docs; copies verbatim.
2. **Archive/Wayback Machine** (complement) — navigate archive.org Teal snapshots in browser for Obligation 10 (historical pricing/feature changes).

**Recommended method for production (ranked by defensibility and reliability):**
1. **Honest headless browser** — test first. If Teal's 403 is UA-based, this succeeds without requiring anti-detect tooling.
2. **Anti-detect headless browser (Playwright-Stealth) or managed commercial service** — if honest headless fails, anti-detect is the next step. Owner-accepted risk. Record access method in capture provenance.
3. **Residential proxy + headless browser** — if IP-blocking is the mechanism (datacenter IP ranges being blocked). Combine with anti-detect for robustness.
4. **Human capture** — valid for infrequent high-value Teal state checks regardless of tooling.

---

### Slot 3 — Reddit (r/FinancialCareers, r/CFA) — tool-layer block

**Root problem:** Claude Code's WebFetch tool blocks Reddit hosts entirely. This is a tool constraint, not a network restriction. Reddit is accessible via any standard HTTP client, browser, or the Reddit API.

**Recommended method for pressure-test:**
1. **Reddit official API** (primary) — the sanctioned route. Public subreddit content (posts, comments, threads) is accessible via the API at the free tier (100 req/min). Returns verbatim text, not paraphrases.
2. **Human-led browser capture** (alternative / complement) — operator opens thread URLs in a real browser; copies verbatim OP, signal-bearing comments, related chain context per Obligation 12.

**Recommended method for production:**
- Reddit official API with registered credentials. This is the cleanest, most defensible, and most scalable method for Reddit. Anti-detect or proxy methods are unnecessary here since the Reddit API is the sanctioned path.
- If data licensing for commercial use is required at scale, review before productizing Reddit content.

Note: Reddit API app registration (admin step, not a code build) can proceed in parallel with slot-1 discipline testing at the owner's discretion.

---

### Slot 3 — Wall Street Oasis (wallstreetoasis.com) — 403 Forbidden

**Root problem:** WSO actively blocks bot requests with HTTP 403.

**Recommended method for pressure-test:**
1. **Human-led browser capture** (primary) — WSO is publicly accessible in any browser. Operator opens enumerated thread URLs, copies verbatim thread content including original post, signal-bearing replies, and related chain context per Obligation 12.
2. **Archive/Wayback Machine** (complement) — the Wayback Machine has extensive WSO thread coverage. Essential for Obligation 10 (editing, deletion, locking posture) and prior-window content.

**Recommended method for production (ranked):**
1. **Honest headless browser** — test first.
2. **Anti-detect headless browser or managed commercial service** — if honest headless fails. Owner-accepted risk. Record in provenance.
3. **Residential proxy + browser** — if IP-based blocking is the mechanism.
4. **Human capture** — appropriate for high-value thread capture regardless of tooling.

---

### web.archive.org content — tool-layer block

**Root problem:** Claude Code's WebFetch tool blocks archive.org content URLs. This is a tooling constraint only — the Internet Archive has no bot-detection posture.

**Recommended method:**
1. **Human browser access to archive.org** (immediate) — operator navigates archive.org in a standard browser; accesses snapshot content directly.
2. **Direct HTTP client in production** — archive.org is accessible via standard HTTP without any anti-bot measures. A direct HTTP fetch completely bypasses the WebFetch tool constraint.

---

## What a Build Would Entail (Named, Not Built)

Nothing here authorizes building, installing, or running anything. Orca is in its non-implementation phase.

### Build 1: Reddit API Access

**Dependencies:**
- Reddit account (free) with app registration at `reddit.com/prefs/apps`
- OAuth2 "script" app type for server-side read-only access
- PRAW (Python Reddit API Wrapper) — `pip install praw` — or direct HTTP with `requests` + OAuth2 token flow

**What the build does:**
- Authenticate with Reddit OAuth2 using client credentials
- Enumerate subreddit posts by time range and keyword
- Fetch specific thread IDs including full comment trees
- Return verbatim post text and comment text

**Rough effort:** Low — 2 to 4 hours.
**Rough cost:** Free at pressure-test scale. Commercial bulk access at scale likely requires Reddit's data licensing.
**Legal / ToS flags:** Reddit Developer Terms reviewed before commercializing. Real legal counsel recommended before any product that surfaces Reddit content.

---

### Build 2: Honest Headless Browser (Playwright)

**Dependencies:**
- Node.js or Python environment
- `npm install playwright` or `pip install playwright`
- Playwright browser binaries — `playwright install chromium`

**What the build does:**
- Launch Chromium with honest user-agent identifying as an automated crawler
- Navigate to target URL; wait for page load including JS execution
- Extract `document.body.innerText` or specific DOM elements for verbatim content
- Apply crawl delay; close browser

**Rough effort:** Medium — 4 to 8 hours per source family.
**Rough cost:** Free (open source).
**Legal / ToS flags:** ToS violation risk per source; hiQ v. LinkedIn provides meaningful protection for honest access to public data. Evaluate per source before production.

**Note:** An honest headless browser will not break through IP-based blocks. Test against Teal and WSO before deciding whether to escalate to anti-detect.

---

### Build 3: Direct HTTP Client (M&I Verbatim Fix)

**Dependencies:**
- Python `requests` or `httpx`; or Node.js `node-fetch`
- HTML parser (BeautifulSoup for Python; Cheerio for Node.js)

**What the build does:**
- GET request to target URL with honest user-agent
- Parse raw HTML to extract verbatim pricing text, course names, bundle structures
- No LLM post-processing (the source of the WebFetch paraphrase problem)

**Rough effort:** Low — 2 to 4 hours per source family.
**Rough cost:** Free.
**Legal / ToS flags:** Lowest risk of any programmatic method. Static HTTP GET to public pages.

---

### Build 4: Archive.org CDX API + Content Fetch

**Dependencies:**
- Python `requests` or equivalent
- CDX API at `cdx.api.web.archive.org/cdx/search/cdx` (no authentication required)

**What the build does:**
- Query CDX API for snapshot availability and timestamps for a given URL
- Fetch snapshot content from `web.archive.org/web/{timestamp}/{url}` via direct HTTP GET
- Parse archived HTML for verbatim historical content

**Rough effort:** Low — 2 to 3 hours.
**Rough cost:** Free.
**Legal / ToS flags:** Very low. Internet Archive terms support research and non-commercial use; commercial use is generally tolerated.

---

### Build 5: Transparent Commercial Scraping Service Integration

**Dependencies:**
- API key for chosen service (Firecrawl, Diffbot, or equivalent)
- Service-provided SDK or direct HTTP API

**What the build does:**
- Submit target URLs to the service's API
- Receive structured or raw content in response
- Service handles browser rendering, network transport, and content extraction

**Rough effort:** Low to Medium — 2 to 6 hours depending on the service's SDK quality.
**Rough cost:** Per-request or subscription pricing. Low at pressure-test scale; material at production scale.
**Legal / ToS flags:** Verify: (a) service ToS permits Orca's use case; (b) access method is described in Orca's capture provenance at category level ("managed scraping service with browser rendering and proxy rotation"); (c) service can be named without concealment.

---

### Build 6: Anti-Detect Browser (Playwright-Stealth or Equivalent)

**Dependencies:**
- Node.js or Python environment
- `npm install playwright playwright-stealth` or `pip install playwright-stealth`
- Chromium binaries

**What the build does:**
- Launch Chromium with fingerprint spoofing (UA, canvas, WebGL, webdriver flag suppression)
- Bypass bot-detection checks on Teal, WSO, and similar actively-blocking sources
- Navigate to target URL; extract verbatim content

**Rough effort:** Low-Medium — 3 to 6 hours. Anti-detect configurations may need tuning per source.
**Rough cost:** Free (open source). Compute cost for browser instances.
**Legal / ToS flags:** Owner-accepted risk. ToS violation likely for actively-blocking sources. Potential CFAA-adjacent exposure in some jurisdictions. Must be disclosed in capture provenance as "automated extraction / anti-detect browser." Real legal counsel recommended before commercializing against actively-enforcing sources.

---

### Build 7: Residential Proxy + Browser Integration

**Dependencies:**
- Account and API credentials with a residential proxy provider (Bright Data, Oxylabs, Smartproxy, or similar)
- A browser or HTTP client that routes traffic through the proxy endpoint
- Managed services (e.g., Bright Data Web Unlocker) bundle both proxy and browser rendering in one API

**What the build does:**
- Routes HTTP or browser traffic through residential IP pool
- Bypasses IP-range blocks (datacenter IP blacklisting) on Teal, WSO, and similar sources
- Combined with a headless or anti-detect browser for JS rendering and fingerprint handling

**Rough effort:** Low-Medium — 2 to 4 hours to integrate a proxy endpoint; more if building a managed rotation layer.
**Rough cost:** Per-GB or per-request pricing. Residential proxies are materially more expensive than datacenter proxies ($5-15/GB retail for residential vs. $0.50-2/GB for datacenter). Factor into production economics.
**Legal / ToS flags:** Owner-accepted risk. Same risk profile as anti-detect browsers. Proxy provider's own ToS review required. Must be disclosed in capture provenance. Real legal counsel recommended before commercializing.

---

## Legal / ToS / Reputational Risk Flags Per Source

These are risk flags, not legal opinions. Real legal counsel is advisable before commercializing any automated web-access capability.

### Reddit

- **API ToS:** Reddit's Developer Terms prohibit large-scale automated access except via the API. The free API tier permits public data access at rate limits appropriate for research. Bulk commercial redistribution likely requires a data license.
- **Direct scraping:** Reddit's `robots.txt` restricts scrapers. Anti-detect and proxy methods bypass this; under the updated standard this is in-bounds, but litigation risk (Reddit has shown willingness to enforce) is real.
- **Reputational:** Disclosing "official API with registered credentials" is a stronger provenance claim than scraping. For Reddit specifically, the API is clearly the right method — anti-detect scraping is unnecessary.
- **Recommendation:** Use the official API. Review Reddit Developer Terms before productizing. Legal counsel before commercializing content sourced from Reddit at scale.

### Teal

- **ToS:** Standard SaaS ToS prohibits automated scraping. Active 403 responses signal enforcement intent.
- **Data type:** Public pricing and feature data. Low sensitivity.
- **Anti-detect / proxy risk:** Teal's small size means litigation risk is low, but ToS violation is likely. Owner-accepted posture applies.
- **Recommendation:** Honest headless browser first; anti-detect if needed. Legal counsel before commercializing.

### Wall Street Oasis

- **ToS:** Likely prohibits bulk automated access. Active 403 enforcement.
- **Data type:** Public forum posts on career topics. No private data.
- **Community posture:** WSO is a known community. Capture use is market research / competitive intelligence, not AI training on their content — this distinction may matter in any disputes.
- **Recommendation:** Human capture for pressure tests; honest headless then anti-detect for production. Archive access for historical content. Legal counsel before commercializing at scale.

### Mergers & Inquisitions / BIWS

- **ToS:** Standard ToS likely prohibits automated copying.
- **Data type:** Public pricing and product structure — standard competitive intelligence.
- **Verbatim problem:** WebFetch paraphrases; direct HTTP or human capture solves this without needing anti-detect.
- **Recommendation:** Human capture for pressure tests; direct HTTP client for production. Very low risk given data type.

### web.archive.org / Wayback Machine

- **ToS:** Nonprofit providing public archival access. Terms support research and analysis.
- **Risk:** Very Low.

---

## Sequencing Recommendation

**Recommendation: Defer tooling builds; complete the pressure-test batch via human capture.**

The commissioning plan prohibits runtime tooling during the pressure-test phase. Human capture is both the authorized mode and the most obligation-compliant path for v0 bootstrap.

**Reasons to defer:**

1. **Obligation architecture validation first.** The critical near-term question is whether the 16-obligation architecture holds under real source mess. This is independent of tooling. Building tooling before validating the architecture risks building against the wrong capture requirements.

2. **Human capture is viable for the 3-batch test.** All five blocked source targets are accessible in a standard browser. The pressure-test batch can complete with human capture for all three slots.

3. **The Reddit API registration is the one exception.** Creating a Reddit account and registering an app is an administrative step that does not cross the implementation-phase boundary. If the owner chooses to do this in parallel with slot-1 capture, it is legitimate. The decision is the owner's.

4. **Tooling scope will be informed by the pressure tests.** If the 3-slot batch surfaces obligation failures or access patterns this plan did not anticipate, the build requirements may change.

**Recommended sequence:**

```
Step 1 (now): Run slot-1 M&I capture via human-led browser + Wayback Machine browser access.
              Complete obligation-discipline capture Markdown. Run LLM checker.

Step 2 (parallel or after slot-1): Run slot-2 Teal + slot-3 Reddit/WSO via human-led capture.
              Use the enumerated URL lists from the pressure-test subagent outputs.

Step 3 (after 3-slot batch): Evaluate whether patchable or architecture-threatening
              findings exist. Decide whether to harden or rebuild.

Step 4 (separately authorized): Build tooling for the recommended methods above.
              Reddit API is the highest-priority build. Honest headless second.
              Anti-detect and residential proxy if honest headless fails against Teal/WSO.
```

---

## Validation Gates

- [x] Preflight complete: AGENTS.md read, overlay read, safety-rules read, source pack loaded, edit permission is docs-write for this file only, target scope named, dirty state acknowledged.
- [x] Boundary standard (public-data + disclosable) applied to all 10 candidate methods.
- [x] All 10 candidate methods in-bounds under the updated standard. No method rejected except the hard-line exclusions (auth bypass, paywall, private data access) — none of the enumerated methods cross that hard line.
- [x] Owner-accepted risk posture for anti-blocking techniques recorded explicitly and not treated as a boundary question.
- [x] No build, install, runtime, or tooling action taken or authorized in this document.
- [x] Non-claims stated explicitly below.

---

## Non-Claims

This artifact does not claim:

- Implementation authorization. This plan does not authorize building, installing, running, testing, or deploying any source-access tooling.
- Exit from the non-implementation phase. Orca remains in its non-implementation / proof-setup phase per `safety-rules.md`. This plan does not change that.
- Legal sufficiency. The legal/ToS flags above are not legal opinions. Orca should obtain real legal counsel before commercializing any capability that relies on automated web access.
- Data-rights sufficiency. Access to public content does not resolve questions about rights to process, store, or commercially use that content.
- Authorization of any specific source access. Each method/source pair must still pass the standard; this plan names recommendations but does not execute or authorize them.
- Source-access method validation or hardening. These recommendations are based on pre-build analysis. Testing may surface access realities that change the recommendations.
- Pressure-test discharge. This plan informs how source access should work for the pressure tests; it does not discharge or validate the pressure-test batch.
- Readiness claims of any kind.
- Authorization for commits, pushes, PRs, stages, or installs.

---

## Next Authorized Step

Proceed to the 3-slot pressure-test batch using human-led capture:

1. Open slot-1 M&I capture. Use the enumerated URL list from `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot1_mi_subagent_output.md`. Navigate pages in a real browser; copy verbatim content. Navigate Wayback Machine snapshots for historical state. Produce a capture Markdown artifact using the commissioning plan template.
2. For Reddit: evaluate whether Reddit API app registration (admin step, no code) should proceed in parallel or after slot-1. Owner decision.
3. For Teal and WSO: human capture via browser.
4. After the 3-slot batch: evaluate findings. If the architecture is patchable, request a separate owner authorization to exit the non-implementation phase for bounded tooling builds per the named builds above.

Building source-access tooling requires a separate, explicit owner authorization to exit the non-implementation phase. That authorization is not granted here.

---

## Human Summary

**What changed in this patch:**

The boundary decision was already updated to `LOOSEN_SOURCE_ACCESS_TO_PUBLIC_DATA_DISCLOSABLE`. This plan has been patched to match. The standard is now two conditions — public data, full disclosure — rather than the previous three-part "confidently defensible" test. Anti-detect browsers, residential proxy rotation, and Chrome automation with fingerprint handling are all in-bounds. The previous OUT-OF-BOUNDS and BORDERLINE verdicts for Methods 3, 4, and 10 are corrected to IN-BOUNDS.

**What this means for the pressure tests:** nothing changes. Human-led capture remains the right mode for v0 bootstrap — it is the most obligation-compliant path regardless of boundary width.

**What changes for production:** the full toolkit is available. If honest headless browsers fail against Teal or WSO, Orca can proceed to anti-detect and residential proxies without a boundary question. The question is now purely risk management (ToS, litigation, cost) — owner-accepted and disclosed — not an in/out-of-bounds gate.

**The hard line that stays:** authentication bypass, paywall circumvention, and private/non-public data access. These are out regardless of any risk-tolerance setting.

---

## Path / Status Receipt

```text
artifact_written_to: docs/product/data_capture_source_access_method_plan_v0.md
status: ACCEPTED_SOURCE_ACCESS_METHOD_PLAN_V0
patch_date: 2026-05-28
patch_reason: Boundary decision updated to public-data + disclosable standard; all methods now in-bounds
phase: Orca non-implementation — no build authorized
boundary_standard_applied: yes, to all 10 candidate methods
methods_out_of_bounds: none (all access public data and are disclosable)
hard_line_exclusions: auth bypass / paywall / private data — unchanged
recommended_for_pressure_tests: human-led browser capture (all slots); Reddit official API (parallel admin step, owner decision)
build_authorization: NOT GRANTED — requires separate owner decision to exit non-implementation phase
commits_pushes_prs: NOT authorized — docs-write only
legal_counsel_advisory: recommended before commercializing any automated web-access capability
produced_by: Claude Sonnet 4.6 under source-access method planning prompt v0
```
