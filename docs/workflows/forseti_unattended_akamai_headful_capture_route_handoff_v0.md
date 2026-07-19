# Unattended Akamai Capture Route — Headful Chrome under Xvfb — Runbook v1

```yaml
retrieval_header_version: 1
artifact_role: Implemented route record and operator runbook for unattended rung-7 real-Chrome capture
scope: >
  The implemented unattended Kohl's x Tower 28 capture route: a temporary
  headful real Chrome under Xvfb, the one-shot runner that captures the bound
  PDP and policy, the observed proof, failure behavior, and the paid fallback.
use_when:
  - Running or maintaining the unattended Kohl's route.
  - Reusing the Xvfb real-Chrome container for another sensor-walled source.
  - Deciding whether the paid Web Unlocker fallback is needed.
authority_boundary: retrieval_only
open_next:
  - forseti-harness/runners/run_kohls_unattended_capture.py
  - forseti-harness/containers/realchrome_xvfb/Dockerfile
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
stale_if:
  - Either unattended runner or the Xvfb container changes.
  - The bound Kohl's PDP or policy wording changes.
  - Akamai blocks the unattended route.
```

## TL;DR (the decision)

The self-hosted unattended route is implemented and passed live on 2026-07-20.
Run:

```powershell
python forseti-harness/runners/run_kohls_unattended_capture.py `
  --data-root "$env:FORSETI_DATA_ROOT"
```

The command builds its Chrome image only when missing, starts one temporary
headful Chrome under Xvfb, captures the bound product and policy pages through
the existing packet writer, and stops the container. A private Docker volume
keeps the browser profile between runs. The browser-control port is published
only to host loopback.

This is an unattended **one-shot**, not a forever-running service. No recurrence
is registered because the owner has not selected a capture frequency, and every
run creates two durable packets. An external scheduler may call this exact
command after that cadence is chosen.

The paid Web Unlocker remains the fallback if this route begins failing.

## What the proof does and does not establish

Akamai's Bot Manager serves a JavaScript **sensor** that must execute in the page
to earn a valid `_abck` session cookie. It fingerprints the browser on dozens of
signals. The User-Agent string is the *most visible* tell but **not** the
detector — changing the UA does not help.

Earlier desktop measurements suggested a real GPU might be load-bearing. The
unattended proof disproved that stronger claim. The passing Docker Desktop run
had no usable WebGL context at all:

| Signal | Passing unattended Xvfb Chrome | Earlier denied headless Chrome |
| --- | --- | --- |
| `navigator.webdriver` | `False` | `False` if launched plainly, but... |
| WebGL | unavailable / blocklisted | software SwiftShader in the measured arm |
| `navigator.plugins.length` | `5` | `0` in the measured arm |
| display surface | Xvfb `1280x800x24` | no display |
| UA `HeadlessChrome` token | absent | present in the measured `--headless=new` arm |

The current evidence supports a narrower statement: the passing route is full
Google Chrome, headful under a display surface, launched normally and then
attached over CDP. It does **not** isolate which one of those signals Akamai
requires, and it does not support “real GPU required.”

Two observed differences from the denied automation routes remain useful:

- **`navigator.webdriver = False`** — because the runner **attaches** (Playwright
  `connect_over_cdp`) to a Chrome launched *normally*, rather than launching it
  through automation (`.launch()` adds `--enable-automation`, which sets
  `webdriver = true` and is an instant tell).
- **A real display surface and normal browser plugins** — Xvfb supplies the
  display even though the proof host exposed no usable WebGL renderer.

Changing only the User-Agent remains unsupported: it does not turn a headless
browser into the observed passing environment.

## Proven starting evidence (fresh-read the sources before trusting)

| Route | Result | Where |
| --- | --- | --- |
| Direct HTTP, header-complete HTTP | Akamai 403 | probe-results Kohl's section; block packets `01KXT02…`, `01KXTZ76…` etc. |
| CloakBrowser (headless & headed, stealth+humanize), on SG residential **and** US datacenter VPN | Akamai `Access Denied` | probe-results; block packets `01KXXBP2…`, `01KXXBVY…` |
| Real Chrome `--headless=new` (cold) | Akamai `Access Denied` (UA sent `HeadlessChrome/150`) | scouting (2026-07-20) |
| **Headful real Chrome via CDP** (rung 7), even over plain SG | **reaches content** — Tower 28 LipSoftie, schema.org Offer `price=16`/`priceCurrency=USD`, US-shipping policy | runner-backed GO packets `01KXXK9PJTA2KBRS2CM1MZDV1H` (PDP), `01KXXKA9RJBP6SVT455DTR0K08` (policy) |
| **Unattended headful Chrome under Xvfb** | **reaches both bound surfaces** with no usable WebGL context; HTTP 200 and no access block | packets `01KXXV920Z8PQVHP6DN16335DF` (PDP) and `01KXXVA8B5EHY86N4EJZ7Y6360` (policy), captured 2026-07-20 |

Full detail: `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
(Kohl's sections), and the Kohl's rows of `retail_storefront_pin_registry_v0.md`
and `capture_recon_index_v0.md`. The runner is
`forseti-harness/runners/run_source_capture_realchrome_cdp_packet.py`.

## Completed first proof

The required two-page gate passed on Windows Docker Desktop:

- Google Chrome `150.0.7871.128`, full/headful under Xvfb;
- normal Linux Chrome UA, `navigator.webdriver=false`, five plugins;
- WebGL unavailable and blocklisted;
- Chrome's inner sandbox disabled because Docker Desktop denied its namespace
  setup; Docker remained the outer isolation boundary;
- PDP packet `01KXXV920Z8PQVHP6DN16335DF`: HTTP 200, no access block,
  `LipSoftie`, and `priceCurrency=USD`;
- policy packet `01KXXVA8B5EHY86N4EJZ7Y6360`: HTTP 200, no access block, and
  Kohl's US/APO/FPO-only shipping statement.

Both packets record `browser_provisioning=unattended_xvfb`,
`persistent_profile_loaded=true`, and
`operator_category=unattended_real_browser_cdp`.

## Implemented container and one-shot

The owning files are:

- `forseti-harness/containers/realchrome_xvfb/Dockerfile`;
- `forseti-harness/containers/realchrome_xvfb/start-chrome.sh`;
- `forseti-harness/containers/realchrome_xvfb/run-xvfb-chrome.sh`;
- `forseti-harness/runners/run_kohls_unattended_capture.py`.

The implementation includes details the original recipe omitted:

- installs `xauth`, which `xvfb-run` requires;
- runs Chrome as a non-root user;
- uses a private relay because Chrome 150 binds its debugging socket to
  container loopback even when asked to listen on all interfaces;
- asks Docker for a random host port bound to `127.0.0.1`, preventing a public
  browser-control port;
- persists the Chrome profile in a named Docker volume;
- captures both surfaces independently so one failure does not erase evidence
  from the other;
- stops and removes only the container created by that invocation.

On Windows Docker Desktop, `--chrome-no-sandbox` defaults on because the observed
Chrome namespace setup was denied. On Linux it defaults off. The packet records
the Windows limitation when used.

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
  automation browsers. The passing browser environment mattered more than the
  tested IP change. (A
  residential egress may still matter if a *server/datacenter* IP is reputation-
  blocked — check during the First-task probe.)

## Open questions / residuals (carry forward)

- **Cause not isolated:** the route passes, but the proof does not identify the
  exact Akamai signal that separates it from denied browsers.
- **Session/cookie lifecycle:** how often `_abck`/`AKA_*` need re-warming; whether
  a persistent profile materially cuts challenge frequency.
- **Server IP reputation:** whether a datacenter host IP is blocked where the
  desktop's residential IP was not (may force a residential egress for the server).
- **Linux sandbox path:** the Windows Docker Desktop proof required Chrome's
  inner sandbox to be disabled; the default Linux path has not been run live.
- **Cadence:** no recurrence is registered. Choosing one creates two durable
  packets and two public page loads per run, so frequency remains an owner
  decision rather than a hidden default.
- **Non-claim:** this proves the bound Kohl's unattended capture route on the
  observed host. It does not prove arbitrary Akamai sites, datacenter egress,
  delivery location, projection coverage, or commercial readiness.
```
