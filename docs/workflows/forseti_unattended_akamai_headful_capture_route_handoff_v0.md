# Unattended Akamai Capture Route — Headful Chrome under Xvfb — Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Future-work handoff for running the rung-7 real-Chrome capture route unattended past Akamai bot walls
scope: >
  How to make the rung-7 real-Chrome CDP capture route (proven on Kohl's x Tower
  28) run UNATTENDED — no human, no monitor — using a headful real Chrome under a
  virtual display (Xvfb), why every headless flavor is ruled out, the paid
  Web-Unlocker fallback, and the empirical evidence behind each claim.
use_when:
  - Making the rung-7 route (or any Akamai-sensor-walled source) run unattended on a server.
  - Deciding between self-hosted Xvfb-headful and a paid Web Unlocker.
  - Judging whether a proposed "headless" idea for an Akamai wall is worth trying.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
stale_if:
  - The rung-7 runner (`run_source_capture_realchrome_cdp_packet.py`) CDP interface changes.
  - Akamai begins fingerprinting headful real Chrome under CDP (retest before trusting).
  - An unattended route is built and verified (this handoff becomes historical).
```

## TL;DR (the decision)

The Kohl's capture works today only because the rung-7 runner attaches to an
**operator-provided real Chrome** running on a desktop — i.e. it needs a human's
machine with Chrome up. To make it **unattended** (a server job, no human), the
two viable options are:

1. **Self-hosted, free: headful real Chrome under Xvfb** (a virtual framebuffer
   display) on a small Linux box/container. Chrome runs in *full headful mode*
   with a *real* GPU/display/rendering path — just no monitor and no human. The
   existing rung-7 runner drives it **unchanged** via `--cdp-endpoint`.
   **Recommended.** First task: *verify it clears Akamai before building around
   it* (see "First task").
2. **Turnkey, paid: a commercial Web Unlocker** (Bright Data / Zyte / Oxylabs /
   ScraperAPI). They run real browsers + residential IPs and solve the Akamai
   sensor, returning rendered HTML. Fully unattended, but costs money and is an
   external dependency (the "owner-approved paid provider" route already named in
   the storefront-pin registry).

**Headless is genuinely out** (proven below), so do not spend time on it.

## Why headless is out and headful works (the mechanism)

Akamai's Bot Manager serves a JavaScript **sensor** that must execute in the page
to earn a valid `_abck` session cookie. It fingerprints the browser on dozens of
signals. The User-Agent string is the *most visible* tell but **not** the
detector — changing the UA does not help.

Measured on the **working** real Chrome (the one that reaches Kohl's), via CDP:

| Signal | Working headful real Chrome | Headless Chrome (any flavor) |
| --- | --- | --- |
| `navigator.webdriver` | `False` | `False` if launched plainly, but... |
| GPU (WebGL renderer) | real hardware — `ANGLE (AMD Radeon ... Direct3D11)` | **software** — SwiftShader/`Google Inc.` |
| `navigator.plugins.length` | `5` | `0` |
| real display | yes | **no** |
| UA `HeadlessChrome` token | absent | present (even `--headless=new`) |

The load-bearing tells are the **software GPU, empty plugins, absent display, and
headless rendering quirks** — all of which persist regardless of UA. Stealth
frameworks (puppeteer-stealth, undetected-chromedriver, Patchright, CloakBrowser)
exist to patch every one of these; the CloakBrowser attempt (a serious anti-detect
browser) was still Akamai-denied. Spoofing signals is an arms race Akamai is
currently winning on this wall.

Two things the winning route gets for free, which a naive automation launch does
NOT:

- **`navigator.webdriver = False`** — because the runner **attaches** (Playwright
  `connect_over_cdp`) to a Chrome launched *normally*, rather than launching it
  through automation (`.launch()` adds `--enable-automation`, which sets
  `webdriver = true` and is an instant tell).
- **A real GPU/display/rendering path** — headful Chrome (even under Xvfb) uses
  the genuine graphics stack, so there is nothing to spoof.

**Answer to "can we do headless without the `HeadlessChrome/150` UA token?":** you
can override the UA (`--user-agent` or CDP `setUserAgentOverride`), but it changes
nothing — Akamai reads the software-GPU / empty-plugins / no-display signals via
the sensor, not the UA. Headful-under-Xvfb wins precisely because it does not
spoof anything; it *is* a real browser.

## Proven starting evidence (fresh-read the sources before trusting)

| Route | Result | Where |
| --- | --- | --- |
| Direct HTTP, header-complete HTTP | Akamai 403 | probe-results Kohl's section; block packets `01KXT02…`, `01KXTZ76…` etc. |
| CloakBrowser (headless & headed, stealth+humanize), on SG residential **and** US datacenter VPN | Akamai `Access Denied` | probe-results; block packets `01KXXBP2…`, `01KXXBVY…` |
| Real Chrome `--headless=new` (cold) | Akamai `Access Denied` (UA sent `HeadlessChrome/150`) | scouting (2026-07-20) |
| **Headful real Chrome via CDP** (rung 7), even over plain SG | **reaches content** — Tower 28 LipSoftie, schema.org Offer `price=16`/`priceCurrency=USD`, US-shipping policy | runner-backed GO packets `01KXXK9PJTA2KBRS2CM1MZDV1H` (PDP), `01KXXKA9RJBP6SVT455DTR0K08` (policy) |

Full detail: `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
(Kohl's sections), and the Kohl's rows of `retail_storefront_pin_registry_v0.md`
and `capture_recon_index_v0.md`. The runner is
`forseti-harness/runners/run_source_capture_realchrome_cdp_packet.py`.

## First task for the receiving lane (do NOT skip)

The Xvfb route is recommended **by mechanism** — it preserves exactly the factors
that made the desktop route work (real GPU/display, `webdriver=false`, headful) —
but it has **not been run end-to-end here** (this authoring box is Windows; no
Xvfb). So the first move is a **probe, not a build**:

1. Stand up the container below.
2. From the runner host, point the rung-7 runner at it and capture the bound Kohl's
   PDP + policy. If both come back non-blocked with the schema.org Offer and the
   US-shipping policy (same admission as the desktop packets), the route is proven
   — then build the schedule/automation around it.
3. If Akamai denies the Xvfb Chrome, capture the block packet and stop; fall back
   to the paid Web Unlocker. (Likely-but-not-certain failure modes to check:
   Xvfb Chrome still exposing a software GPU — force/confirm hardware or a
   convincing GL renderer; a datacenter server IP being reputation-blocked where
   the desktop's residential IP was not — try a residential/mobile egress.)

## Recipe: headful Chrome under Xvfb (container)

`Dockerfile`:

```dockerfile
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      wget gnupg ca-certificates xvfb fonts-liberation dumb-init \
  && wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt-get install -y /tmp/chrome.deb \
  && rm -rf /var/lib/apt/lists/* /tmp/chrome.deb
# NOTE: real google-chrome-stable, NOT chromium, NOT a stealth build.
ENTRYPOINT ["dumb-init","--"]
```

Launch (inside the container; nothing human, nothing monitored):

```bash
xvfb-run -a --server-args="-screen 0 1280x800x24" \
  google-chrome \
    --remote-debugging-port=9222 \
    --user-data-dir=/data/chrome-profile \
    --no-first-run --no-default-browser-check \
    --window-size=1280,800 \
    about:blank
```

Load-bearing rules (violating any one re-introduces a headless/automation tell):

- **Do NOT pass `--headless`.** The whole point is headful.
- **Do NOT launch Chrome via Playwright/Selenium `.launch()`** — that adds
  `--enable-automation` (`navigator.webdriver = true`). Launch Chrome the plain
  way above, then have the runner **attach** over CDP.
- **Keep the CDP port private.** `--remote-debugging-port` is full control of that
  browser and its cookies. Bind it to localhost / the private network only; never
  expose it publicly. Only add `--remote-debugging-address=0.0.0.0` if the runner
  is in a separate container, and firewall it.
- **Persist `/data/chrome-profile`** on a volume so the Akamai session cookies
  (`_abck`, `bm_sz`, `AKA_*`) survive restarts. A cold profile also worked in
  testing, so this is an optimization (fewer challenges), not a requirement.
- Verify inside the container that the WebGL renderer is **not** SwiftShader
  (`google-chrome` under Xvfb usually uses a real software-GL that differs from
  headless SwiftShader; confirm during the First-task probe, and if it looks like
  a headless GPU, add a GL/ANGLE flag or a virtual GPU).

Wire the existing runner to it (no code change):

```bash
python forseti-harness/runners/run_source_capture_realchrome_cdp_packet.py \
  --cdp-endpoint http://<xvfb-host>:9222 \
  --url "https://www.kohls.com/product/prd-6715879/tower-28-beauty-lipsoftie-hydrating-tinted-lip-treatment-balm.jsp" \
  --warm-hop-url "https://www.kohls.com/" \
  --source-family retail_pdp --decision-question "…" \
  --data-root "$FORSETI_DATA_ROOT" \
  --require-not-access-blocked --require-visible-text "LipSoftie" \
  --require-rendered-dom-regex 'priceCurrency"\s+content="USD"'
```

## Zero-maintenance fallback: paid Web Unlocker

If the self-hosted route is more ops than it is worth, a commercial Web Unlocker
(Bright Data Web Unlocker / Zyte / Oxylabs Web Unblocker / ScraperAPI) handles the
Akamai challenge (real browsers + residential IPs + sensor solving) and returns
rendered HTML. This is the registry's already-named "owner-approved paid provider"
route. Tradeoff: recurring cost + external dependency + you preserve *their*
rendered bytes (record provenance honestly). Would need its own thin adapter into
the packet seam.

## What will NOT work (do not spend time here)

- **Any headless** — Direct HTTP, header-complete HTTP, headless/headed CloakBrowser,
  Playwright headless Chromium, and now real-Chrome `--headless=new` are all
  Akamai-denied. Proven.
- **Pure HTTP / curl_cffi / TLS-JA3 impersonation alone** — Akamai's `_abck`
  requires the JS **sensor executed in a browser**; no browser means no sensor
  payload means denied. curl_cffi is only useful as a *cookie-replay add-on* after
  a real browser warms the session, and `_abck` re-validates/expires, so it is
  fragile and high-maintenance.
- **A residential IP by itself** — not the lever. The real headful Chrome cleared
  Kohl's over a plain SG residential IP; a US datacenter VPN did **not** help the
  automation browsers. The browser fingerprint is decisive, not the IP. (A
  residential egress may still matter if a *server/datacenter* IP is reputation-
  blocked — check during the First-task probe.)

## Open questions / residuals (carry forward)

- **Verification pending:** Xvfb-headful clearing Akamai is expected by mechanism
  but not yet empirically run — the First task settles it.
- **Session/cookie lifecycle:** how often `_abck`/`AKA_*` need re-warming; whether
  a persistent profile materially cuts challenge frequency.
- **Server IP reputation:** whether a datacenter host IP is blocked where the
  desktop's residential IP was not (may force a residential egress for the server).
- **Concurrency:** one Chrome instance can serve many tabs; separate profiles only
  for separate warmed identities or logins (see the browser-concurrency notes from
  the authoring session).
- **Non-claim:** this handoff is a design/ops route, not a validated capability.
  Nothing here promotes a pin, projection, or readiness claim; the current admitted
  Kohl's route remains the operator-gated rung-7 runner until an unattended route
  is built and verified.
```
