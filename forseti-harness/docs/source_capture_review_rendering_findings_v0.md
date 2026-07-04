# Source-Capture Finding — Bazaarvoice PDP Reviews Are Capturable (Progressive-Scroll Trigger) v0

**Status:** corrects a prior false limitation claim; reviews confirmed capturable; small adapter enhancement scoped separately.
**Date:** 2026-06-11.
**Method:** 5 live read-only probes (proxied + one unproxied control), public fingerprint detectors. No target writes, no adapter changes.
**Supersedes:** the earlier claim (commit `ec4133d`) that these reviews are anti-bot-gated and unreachable. That root cause was **wrong** — see Correction.

---

## Correction of the prior claim

The first version of this finding claimed reviews were unreachable due to Kasada/anti-bot gating (`/auth/v2/session` 403, token denied). Deeper probes **refute** that:

- A valid bot token **is** minted (`x-kpsdk-ct`, 175 chars); `/auth/v2/session` returns **200**; **proxied == unproxied**. The `429` on `/fp` is the *normal sensor handshake* (the token is returned in that same response), not a block.
- Runtime/TLS fingerprints are clean: `navigator.webdriver: false`, **CDP not detected**, JA3/JA4/HTTP2 = standard Chrome (`t13d1516h2_8daaf6152771…`), real GPU, and `bot.sannysoft.com` passes every check.

The anti-bot wall is real (Akamai `ak_bmsc` cookies + kpsdk token flow) but **we pass it.** It was never the blocker.

---

## What is actually true (pinned, with evidence)

- Reviews are served by **Bazaarvoice's API** — `api.bazaarvoice.com/data/reviews.json?Filter=ProductId:P427414&...&Limit=6&Offset=...` (**200**), plus `questions.json` (Q&A) and `photos-us.bazaarvoice.com` (review images, ×24). Called by Sephora's **own first-party JS** and **rendered into the main DOM as first-party text.** So "Bazaarvoice" was right all along — as an **API, not an iframe.**
- The reviews section **lazy-loads via an IntersectionObserver** when it enters the viewport.
- **Why every prior capture failed:** the adapter's `scroll_passes` does `window.scrollTo(0, document.body.scrollHeight)` (`source_capture/adapters/cloakbrowser_snapshot.py:366`) — an **instant jump to the footer that overshoots the reviews section**, so the observer never fires and the BV API is never called.
- **Proof:** with **incremental scroll** (350px steps, dwelling) + a real trusted click, `reviews.json` returned **200**, 24 review photos loaded, and real review text rendered — **body `7.5 KB → 14.9 KB`**, a dated "verified" review captured. Corroboration: in that run the Sephora `session` endpoint returned **403** yet reviews **still loaded** — because they come from Bazaarvoice, not the Sephora session.

---

## Implication

- Reviews **are capturable** with the existing armory plus a **progressive/incremental scroll** (step through the page so lazy-load observers fire) instead of jump-to-bottom. No anti-bot defeat, no iframe traversal, no direct API client — `page.content()` captures the first-party-rendered reviews once the section loads.
- The BV API is paginated (`Limit=6`), so capturing **all** reviews (vs the first page) reopens the bounded-enumeration question inside the review section — relevant to how the enhancement is structured.
- **Not yet isolated:** whether the incremental scroll *alone* or the trusted click was decisive (to confirm during scoping).

## What this retires

- "Cross-origin iframe" hypothesis — false (no review iframe).
- "Anti-bot-gated / unreachable" hypothesis (the v0 claim) — false (we pass the wall; reviews load).
- Approaches A (frame traversal) and B (direct Bazaarvoice API client) — unnecessary; first-party render capture works.

## Provenance / boundaries

- All probing was **read-only**; no adapter or runner changes.
- **Distinct from** the bounded-enumeration move-#1 work (`capture-spine-bounded-enumeration` @ `63520d0`) and the cloak features (PR #22 geo/settle, PR #23 scroll/load-more).
