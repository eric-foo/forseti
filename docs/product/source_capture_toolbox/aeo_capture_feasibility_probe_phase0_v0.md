# AEO Answer-Capture Feasibility Probe (Phase 0) — Report v0

```yaml
retrieval_header_version: 1
artifact_role: Probe feasibility report (capture-spine Phase-0 AEO answer-capture)
scope: >
  Records a BOUNDED Phase-0 live feasibility probe of AI answer engines (ChatGPT
  logged-out, then Google AI Overviews) to determine whether the answer —
  surfaced brands/products + cited sources + issued queries — can be reliably AND
  automatably captured via devtools (F12 / DOM + network) inspection for a small
  frozen US-fragrance query set. Deliverable: GO / RE-ROUTE verdict + reusable
  extraction pattern + failure characterization. NOT a scaled capture run; NOT
  sourcing authorization.
use_when:
  - Deciding whether to build an automated AEO answer-capture lane for ChatGPT / Google AI Overviews.
  - Reusing the extraction pattern (selectors / network signatures) that worked.
  - Checking the measured not-shown rate, volatility, and bot-detection findings before scaling.
authority_boundary: retrieval_only
status: PROBE_EXECUTED_2026-06-17_AWAITING_LANE_ADJUDICATION
adjudication_route: capture-spine lane reviews this report; owner decides GO / RE-ROUTE and any scaled-build authorization.
model_lane: unbound
deliverable_state: PROPOSED
stale_if:
  - Answer-engine DOM/network surfaces change (selectors break) — re-probe.
  - A cross-date repeat is run (closes the one UNMEASURED leg below).
  - Owner amends the source-access posture this probe operated under.
```

## TL;DR Verdict

**GO (qualified)** — for BOTH engines, on the core feasibility question
("can the answer be reliably **and** automatably captured via devtools?"):

- **Google AI Overviews (PRIMARY target): GO.** AI Overview fired on **10/10**
  fragrance queries (8 distinct + 2 repeats) on 2026-06-17; surfaced brands +
  cited sources are reliably extractable from the rendered DOM; **0 CAPTCHA / bot
  block** across 10 rapid logged-out searches; issued query is in the URL.
- **ChatGPT (logged-out / anon): GO.** **5/5** runs performed a live web search
  and rendered cited sources + surfaced brands/products (incl. structured product
  cards with price/rating/merchant); reliably DOM-extractable.

**The one GO-criterion NOT satisfied is `≥2 dates`** — the probe ran on a single
calendar date (2026-06-17). Cross-date volatility is **UNMEASURED / deferred**, a
scheduling limit, not a feasibility failure. A single confirmatory re-run on a
later date closes it. See [Verdict](#go--re-route-verdict) and
[What is UNMEASURED](#what-is-unmeasured--deferred).

---

## 1. Authorization, posture, conditions

- **Owner authorization:** owner confirmed the bounded live probe **at dispatch**
  (in-thread, 2026-06-17). Live observation was owner-gated; confirmation was
  obtained before any live request.
- **Source-access classification** (under
  `docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md`):
  **publicly-viewable, in-bounds, measured-risk / disclosable.** The probe was
  **read-only observation** of public answer-engine surfaces (logged-out
  `chatgpt.com`; logged-out `google.com/search`). No account actions, no
  purchases, no posting, no auth-gate defeat, no CAPTCHA solving. Human-rate, no
  bursting. **No ToS / legal sufficiency is claimed** (explicitly per posture).
- **Conditions:** US (`hl=en&gl=us`), **logged-out**, single date 2026-06-17,
  single machine/IP. ChatGPT logged-out was reached via a fresh Chrome profile
  not signed into ChatGPT (the operator's default profile was signed into ChatGPT
  Pro and was **not** used for probing, to honor the logged-out condition and
  avoid personalization + private chat history).
- **Tooling:** Chrome via the Claude-in-Chrome extension (DOM read via injected
  JS = the F12 Elements equivalent; `read_network_requests` = the F12 Network
  equivalent). "Sessions" = 2 passes within the same logged-out profile (anon
  cookie persisted) — see UNMEASURED for the session-independence caveat.

## 2. Frozen query set v1 (recorded verbatim, locked before probing)

Public / category-seeded US fragrance category questions. **No first-party / Core-seed terms** (taint rule honored).

| ID | Query |
|----|-------|
| Q01 | best niche fragrance brands for men 2026 |
| Q02 | top indie perfume brands in the US |
| Q03 | best long lasting natural perfumes |
| Q04 | affordable alternatives to expensive designer fragrances |
| Q05 | best clean fragrance brands |
| Q06 | best vanilla perfumes for women |
| Q07 | best unisex fragrances 2026 |
| Q08 | best small batch perfume brands USA |
| Q09 | long lasting fragrances for summer |
| Q10 | best oud fragrances for beginners |
| Q11 | best fragrance subscription boxes |
| Q12 | where to buy indie perfumes online |

**Probed this session (feasibility subset):** ChatGPT — Q01, Q02, Q03, Q05 (+ Q01
repeat). Google AIO — Q01, Q02, Q03, Q05, Q07, Q09, Q11, Q12 (+ Q01, Q02
repeats). Q04/Q06/Q08/Q10 were left unprobed (frozen for the next pass);
coverage is disclosed honestly — this is a feasibility probe, not full-set
capture.

## 3. ChatGPT (logged-out / anon) — per-probe records

| Run | Query | Web search fired | Cited? | Surfaced brands/products (sample) | Cited source hosts (host+path in DOM) | Answer format |
|-----|-------|:---:|:---:|---|---|---|
| Q01a | best niche fragrance brands for men 2026 | yes | yes | Amouage Reflection Man ($456.38, 4.6/1.2K); Aventus Creed ($487.47, 4.4); ROJA Enigma Pour Homme; Xerjoff Naxos ($372.00, 4.6); Layton / Parfums de Marly ($372) | fragrenza.com, reddit.com (r/Colognes, r/Perfumes), colognecapitol.com, argosfragrances.com, youtube.com | product cards |
| Q02 | top indie perfume brands in the US | yes | yes | Imaginary Authors (Memoirs of a Trespasser, Cape Heartache, The Cobra and the Canary); Aftelier Perfumes | scento.com, reddit.com, youtube.com, theguardian.com | brand list |
| Q03 | best long lasting natural perfumes | yes | yes | Abel (Green Cedar); Hiram Green (Hyde, Moon Bloom) | prosodylondon.com, vogue.co.uk, reddit.com, nenefragrance.com | brand list |
| Q05 | best clean fragrance brands | yes | yes | Henry Rose (Queens & Monsters, Jake's House); Clean Reserve; Skylar (Salt Air, Vanilla Sky); Ellis Brooklyn; Phlur | healthline.com, reddit.com, fountainof30.com, tscentral.com, the-ethos.co, byrosiejane.com, sustainablykindliving.com **+ brand sites** henryrose.com, skylar.com, ellisbrooklyn.com, phlur.com, the7virtues.com, abelodor.com, hereticparfum.com, dedcool.com (22 links total) | brand list w/ links |
| Q01b (repeat) | best niche fragrance brands for men 2026 | yes | yes | Ormonde Jayne Montabaco ($87.52); Tom Ford Oud Wood ($465.00); Roja Vetiver ($470.00); Ex Nihilo Citizen X ($440.00); narrative: Creed, Xerjoff, Amouage, Maison Francis Kurkdjian | colognecapitol.com, youtube.com, aromatrail.com, instyle.com, reddit.com, fragrantix.com | product cards |

**ChatGPT result: 5/5 search-fired + cited + extractable. `not_shown` = 0/5.**

## 4. Google AI Overviews (logged-out, fresh profile, US) — per-probe records

| Run | Query | AIO fired (`not_shown`?) | CAPTCHA | Distinct source domains | Sample surfaced brands / cited sources |
|-----|-------|:---:|:---:|:---:|---|
| Q01a | best niche fragrance brands for men 2026 | fired | none | 9 (19 links) | Creed/Aventus/Green Irish Tweed, Amouage/Interlude Man, Xerjoff/1861 Naxos · prosodylondon, harrods, fluxurymagazine, felisafragrances, youtube, fzine, beautinow, perfumebays, parfumeriedaquitaine |
| Q02a | top indie perfume brands in the US | fired | none | 23 | D.S. & Durga, Imaginary Authors · fashionista, cafleurebon, theperfumestylist, glossy, reddit, fragrancelord, libertylondon, instyle |
| Q03 | best long lasting natural perfumes | fired | none | 22 | thegoodtrade, prosodylondon, orientfragance, bondiwash, sensoriam, scentbird, mcaffeine, maison21g, scento, reddit |
| Q05 | best clean fragrance brands | fired | none | 17 | ulta, cleanbeauty, sephora, organicbeautylover, vogue, the-ethos, youtube, crueltyfreekitty, reddit, credobeauty |
| Q07 | best unisex fragrances 2026 | fired | none | 13 | fragrantica, fragranceoutlet, shoppexcorp, absolutelymagazines, lemon8, prosodylondon, perfumebox, fragrancemarket |
| Q09 | long lasting fragrances for summer | fired | none | 10 | theperfumeshop, oakcha, maisonmargiela-fragrances, newyou, smytten, blancoparfumes, reddit, youtube |
| Q11 | best fragrance subscription boxes | fired | none | 13 | Scentbird, ScentBox · instyle, byrdie, scentbox, luxsb, olfactif, skylar, scentbird, community.sephora, perfume.com |
| Q12 | where to buy indie perfumes online | fired | none | 15 | Luckyscent, Ministry of Scent, Twisted Lily · indigoperfumery, alkemiaperfumes, indiescents, fragrancelord, fragrantica, 50-ml, tiktok |
| Q01b (repeat) | best niche fragrance brands for men 2026 | fired | none | 12 | jomashop, maxaroma, beautinow, harrods, prosodylondon, edenperfumes, vitivinci, lemon8, mahadiperfumes, resident |
| Q02b (repeat) | top indie perfume brands in the US | fired | none | 21 | fragrancelord, reddit, fashionista, tigerlilyperfumery, scenttrunk, wwd, scento, perfumerflavorist, 50-ml, robbreport, harveynichols |

**Google AIO result: 10/10 fired. `not_shown` = 0/10 (0%) for fragrance queries
this date/session, including commercial/navigational intent (Q11, Q12). 0 CAPTCHA
across 10 rapid searches.**

## 5. Reusable extraction pattern (the deliverable artifact)

### 5.1 ChatGPT (logged-out / anon)
- **Answer surface (DOM):** assistant turn = `[data-message-author-role="assistant"]` (last one).
- **Cited sources:** `<turn> a[href]` → real source URLs are present in the static
  DOM (no hover/click needed). Includes both citation sources and surfaced-brand
  official sites. **Extract host + path; strip query strings** (see Failure F1).
- **Surfaced products (rich):** product cards render as `[role="button"]` / `button`
  whose `innerText` carries `name · $price · rating`. Filter for `/\$|\d\.\d/`.
- **Issued search query:** **server-side, NOT client-visible** — no `search_query`
  / `q` param in any client request (grep over the full network dump: 0 hits).
- **Network signature:** main answer stream `POST backend-anon/f/conversation`
  (SSE) + `backend-anon/conversation/init`, `backend-anon/f/conversation/prepare`;
  anti-abuse `backend-anon/sentinel/chat-requirements/{prepare,finalize}` +
  frequent `backend-anon/sentinel/ping`.

### 5.2 Google AI Overviews
- **Detect AIO fired vs `not_shown`:** locate container element whose
  `innerText` **startsWith `"AI Overview"`** (length 150–8000). Found reliably on
  10/10. **Full Overview text + all source links are in the DOM even while the
  "Show more" expander is collapsed** — no interaction needed to extract.
- **Surfaced brands:** the AIO container `innerText`.
- **Cited sources:** external `a[href]` within the AIO container, filtered to drop
  `google.*` / `gstatic`; reduce to hostnames.
- **Issued search query:** trivially in the page URL (`?q=...`).
- **Self-polling note:** AIO can stream in over a few seconds — poll up to ~6 s
  for the container before declaring `not_shown` (avoids false negatives).
- **Selector fragility:** Google's class names are obfuscated/randomized; this
  pattern anchors on the **visible "AI Overview" label text** (locale-dependent)
  and on `a[href]`. Durable automation needs a more resilient anchor (e.g.
  the sparkle-icon container or a structural attribute) and locale handling.

## 6. Failure / friction taxonomy (honest)

| ID | Engine | Event | Type | Impact on automation |
|----|--------|-------|------|----------------------|
| F1 | both (extraction-side) | MCP/devtools output blocked `[BLOCKED: Cookie/query string data]` when returning hrefs with tracking query strings (`?utm_source=chatgpt.com` etc.) | extraction-tool guard (not engine block) | Return host+path only; strip query strings. Trivial to handle. |
| F2 | ChatGPT | "Clear current chat?" confirm modal on **New chat** (logged-out) | UI gate | Must click "Clear chat" between queries. Deterministic. |
| F3 | ChatGPT | "Thanks for trying ChatGPT" soft login modal after ~5 logged-out queries | soft login-wall (dismissable via "Stay logged out") | Recurring; automation must detect + dismiss. Not a hard block. |
| F4 | ChatGPT | `sentinel/chat-requirements` proof-of-work + `sentinel/ping` | anti-automation | A real browser satisfies it; a naive headless script must solve the PoW. Real engineering hurdle for headless scale. |
| F5 | ChatGPT | issued search query not client-visible | observability gap | "Issued queries" leg not capturable for ChatGPT (server-side). Brands+sources still fully capturable. |
| F6 | both | run-to-run **volatility**: same query → partially different brands/sources | data-quality | Capture per-run; never treat a single capture as the canonical answer. Firing + extractability are stable; the *set* is not. |
| — | Google AIO | **No** CAPTCHA, **no** consent banner, **no** `not_shown` observed | (no failure) | 0/10 over rapid human-rate searches, single IP. |

### Volatility evidence (same query, two same-day passes)
- **ChatGPT Q01:** pass A "best overall" = Amouage Reflection; pass B = Ormonde
  Jayne Montabaco. Source-host overlap ≈ 3/5.
- **Google AIO Q01:** source-host overlap ≈ 4 of 9–12. **Q02:** overlap ≈ 3.
- AIO *fired* on both passes of both repeated queries (firing is stable).

## 7. Automatability assessment

The real question was not "can a human see it" (yes, trivially) but "can it be
**automated reliably at a human-rate, ToS-aware cadence?**":

- **Google AIO (PRIMARY): strongly automatable.** Deterministic DOM presence,
  query in URL, no bot block at human rate, 0% not-shown for this vertical. Main
  engineering cost = a resilient selector against the obfuscated/randomized DOM +
  locale handling + treating volatility as expected.
- **ChatGPT: automatable with handled friction.** Reliable search+cite+extract,
  but automation must (a) dismiss F2/F3 modals, (b) satisfy the F4 sentinel
  proof-of-work (a real browser context does; a naive headless client does not),
  (c) accept that issued queries are not observable (F5).

## 8. GO / RE-ROUTE verdict

**GO (qualified) for both engines**, with Google AI Overviews as the confirmed
PRIMARY automatable target and ChatGPT as a viable secondary.

Rationale: the Phase-0 GO bar — surfaced brands/products + cited sources (+ issued
queries where visible) reliably **and** automatably extractable across repeats,
raw observable preserved, shown/`not_shown` recorded, failure taxonomy logged,
source access classified — is met for both engines on every dimension probed,
**except the `≥2 dates` repeat**, which was physically impossible in a single
session and is deferred (low-risk).

No RE-ROUTE is warranted on current evidence: neither engine is "not yet
automatable," and AIO did not drop to manual-only (it was the strongest surface).

## 9. What is UNMEASURED / deferred

These do not contradict the GO; they bound it honestly.

1. **Cross-date volatility (`≥2 dates`)** — only 2026-06-17 probed. **The single
   open GO-criterion.** Recommended: one confirmatory re-run on a later date.
2. **Session/identity independence** — 2 passes shared one anon cookie / one IP /
   one machine. Multi-IP / multi-device / cold-session behavior is unprobed.
3. **Sustained-volume bot-detection** — clean to ~10 ChatGPT and ~10 Google
   requests at human rate; behavior at higher volume/cadence is unprobed (and out
   of scope — scaling is not authorized here).
4. **Personalization delta** — logged-out only; logged-in/personalized surfaces
   not compared (deliberately, to honor the frozen condition).
5. **Full query-set + Gemini** — Q04/Q06/Q08/Q10 unprobed; Gemini (optional
   secondary) not probed.

## 10. Raw observable preservation

- **Structured per-run extractions** (surfaced brands/products, cited source
  host+paths, AIO fired/`not_shown`, CAPTCHA flag, network signature) are
  transcribed verbatim in §3–§4 above and preserved as machine-readable JSON in
  the companion file
  `aeo_capture_feasibility_probe_phase0_v0_evidence.json` (same folder).
- **Screenshots** of the logged-out ChatGPT answer surface (product cards,
  citations, soft-login modal) and the Google AIO surface were captured live
  during the probe (in-session visual record).
- **Byte-exact HTML preservation was constrained by F1** (the MCP guard blocks
  raw output carrying URL query strings); preserved observables are therefore
  text + host+path + structured fields, which carry the load-bearing content.

## Non-claims

Feasibility probe only. **Not** a capture-run authorization, **not** sourcing
authorization (AR-04 stays owner-gated), **not** validation / readiness /
buyer-proof, **not** a ToS / legal-sufficiency claim. Deliverable is `PROPOSED`;
`model_lane: unbound`. The GO verdict authorizes nothing by itself — a scaled
automated capture build requires separate explicit owner authorization naming the
bounded implementation scope.
