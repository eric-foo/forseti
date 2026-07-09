# Demand Durability — US Storefront Pin Recon Verdict

```yaml
retrieval_header_version: 1
artifact_role: Recon verdict (INV-1 observed facts + limitations; GO verdict for US storefront pin via CloakBrowser delivery-zip widget)
scope: >
  Records the single-probe recon outcome for the demand-durability US storefront pin commission:
  whether a stateful CloakBrowser session (clean local IP, no proxy, humanize=True) can set a US
  delivery ZIP via amazon.com's public homepage widget and receive USD prices on a subsequent PDP
  without triggering a bot gate. Covers confirmed selectors, measured ToS posture, honest
  limitations, and what was built. No demand verdict, no scoring.
authority_boundary: retrieval_only
use_when:
  - Loading context before running live Amazon US storefront capture slots
  - Assessing whether PR #161 (access_failed detection) must land before Amazon slots run
  - Reviewing the declared_delivery_zip limitation note or delivery_zip_requested metadata field
stale_if:
  - Amazon delivery location widget DOM selectors change (check #nav-global-location-popover-link, #GLUXZipUpdateInput, #GLUXZipUpdate)
  - CloakBrowser version changes materially (current: 0.3.31)
  - A subsequent probe shows bot-interstitial on clean-IP homepage (verdict degrades to NO-GO)
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/demand_durability_multi_retailer_rendered_capture_spec_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
  - forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py
```

**Status:** `RECON_VERDICT_GO`
**Date:** 2026-06-16
**INV-1:** Observed facts + measured limitations only. No demand verdict, no scoring.

---

## Hypothesis

A stateful CloakBrowser session launched from the clean local IP (no proxy), with humanize
enabled, can navigate to amazon.com, set a US ZIP via the public delivery location widget, and
subsequently receive a US-storefront PDP (currencyOfPreference=USD) — without triggering a
bot-interstitial gate.

---

## Probe Parameters

| Field | Value |
|---|---|
| Tool | `probe_amazon_us_storefront_recon.py` (gitignored, `forseti-harness/_scratch/`) |
| CloakBrowser version | 0.3.31 |
| Launch mode | `stealth=True`, `humanize=True`, no proxy |
| US ZIP | `10001` (New York, NY) |
| Probe homepage | `https://www.amazon.com/` |
| Probe PDP | `https://www.amazon.com/dp/B07XXPHQZK` (single SKU) |
| Volume | Single session, one SKU, human-rate — no industrial scraping |

---

## Recon Steps and Observed Outcomes

### Step 1 — Homepage Access

**Result:** `PASS`

CloakBrowser navigated to `https://www.amazon.com/` without triggering the "Continue shopping"
bot interstitial or any Cloudflare challenge. The homepage rendered cleanly with the standard
delivery location widget visible.

Contrast: prior work (PR #160 verdicts doc) established that CloakBrowser + Decodo residential
proxy yielded the interstitial (5.5 KB page, no substrate). No proxy = no interstitial here.

### Step 2 — Delivery Location Widget

**Result:** `WIDGET_APPLY_CLICKED`

The delivery location widget was located, clicked, ZIP filled, and Apply submitted via normal
UI interaction. The confirmed selector path:

1. Open widget: `#nav-global-location-popover-link` (with fallback `#glow-ingress-block`)
2. Fill ZIP: `#GLUXZipUpdateInput` (with fallback `input[id*='zip' i][type='text']`)
3. Submit: `#GLUXZipUpdate` (with fallback `span.a-button-inner > input[type='submit']`; fallback: `page.keyboard.press("Return")`)

Setting a delivery location via the site's own public UI widget is in-bounds per the
`data_capture_source_access_boundary_decision_v0.md` (`ACCEPTED_SOURCE_ACCESS_BOUNDARY_DECISION_V0`):
normal account-free interaction with a publicly accessible page element.

### Step 3 — PDP Storefront Check

**Result:** `PASS`

After the delivery location session was established, navigating to the probe PDP
(`https://www.amazon.com/dp/B07XXPHQZK`) returned:

- `currencyOfPreference` hidden input: `value="USD"` (observed in rendered DOM)
- Delivery preamble: "Deliver to" (US delivery context confirmed)

Detected currency: **USD** (US storefront).

**Mechanism confirmed:** amazon.com geo-localization is session-cookie-based (delivery location),
not purely IP-based. A US ZIP set via the delivery location widget overrides the origin-IP
locale (Singapore IP → USD prices after widget set).

---

## Verdict

**GO.**

The stateful clean-IP CloakBrowser flow (homepage → delivery location widget → ZIP → PDP)
yields a US storefront (USD) without proxy, without auth, and without tripping any bot gate
observed in this probe.

---

## Measured ToS Posture

- **Mechanism:** Public-UI delivery location widget — the site's own account-free UI to set
  delivery ZIP. No credential reuse, no session injection, no gate bypass, no CAPTCHA solving.
- **Boundary:** `LOOSEN_SOURCE_ACCESS_TO_DISCOVERABLE_OR_ENTITLED_DISCLOSABLE` (in-bounds per
  `data_capture_source_access_boundary_decision_v0.md`).
- **Volume:** Single-session, single-SKU, human-rate. No industrial scraping.
- **Hard stops honored:** No auth wall, no "Continue shopping" interstitial, no Cloudflare
  challenge appeared in this probe. Commission rule: stop and record limitation if any of these
  appear; none did.

---

## Honest Limitations

1. **Selector fragility.** The delivery location widget selectors (`#nav-global-location-popover-link`,
   `#GLUXZipUpdateInput`, `#GLUXZipUpdate`) are stable Amazon UI elements but are not guaranteed
   across A/B tests or regional variants. The adapter falls back gracefully (warning_note added,
   capture proceeds without pin) if any selector fails.

2. **Humanize requirement.** The widget interaction flow requires `humanize=True` (human-like
   timing and mouse). Without it, widget clicks may be dropped or the submit may not register.
   The adapter sets `humanize=delivery_zip is not None` automatically; existing captures
   (no ZIP) retain `humanize=False`.

3. **Single-session, single-SKU probe.** This verdict is based on one probe session, one SKU.
   Whether the session cookie persists across a full durability-series cadence (multiple slots
   over days/weeks) is untested — each slot opens a fresh CloakBrowser session, so the
   delivery-zip widget interaction must run per slot (by design in the adapter).

4. **No proxy fallback.** This capability is explicitly no-proxy. If amazon.com IP-blocks the
   clean local IP in a future slot, the capture will degrade to SG storefront (or bot wall),
   not silently switch to proxy. The proxy route remains owner-gated.

5. **Bot wall risk remains.** This probe observed no bot interstitial from the clean local IP.
   That observation is single-point; repeated capture at industrial rate or from the same IP
   over a long period could change posture. The adapter detects access_failed (PR #161, merged
   or pending merge to main) and will refuse to record a blocked capture as an observed slot.

6. **Recon scope.** This doc records observed facts from a single recon probe. It does not
   assert demand durability, product read validity, or signal quality. Those remain scoped to
   their own lanes.

---

## What Was Built (Additive, No Schema Change)

Three additive code changes landed in this lane (branch `demand-durability-us-pin-recon-v0`):

### 1. `forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py`

- `fetch_cloakbrowser_snapshot_capture()` gains `delivery_zip: str | None = None`.
- When set: `humanize=True`, `_set_delivery_location()` runs before the PDP `page.goto()`.
- Limitation note added: `"declared_delivery_zip: Amazon delivery location set to {zip!r} via homepage widget..."`.
- Metadata field added: `"delivery_zip_requested": delivery_zip`.
- New helper: `_set_delivery_location(page, delivery_zip, timeout_ms, warning_notes)` — widget
  click, ZIP fill, Apply submit, with per-step fallbacks and graceful-degrade warning notes.

### 2. `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`

- `--delivery-zip` CLI flag added; forwarded to `fetch_cloakbrowser_snapshot_capture()`.

### 3. `forseti-harness/runners/run_source_capture_durability_series.py`

- `"--delivery-zip"` added to `_WRITER_ARG_KNOB_ALLOWLIST` so the cadence runner can
  pass it per-slot via `--writer-arg` without triggering the default-deny guard.

**Constraints preserved:** No schema change, no `SOURCE_CAPTURE_MANIFEST_VERSION` bump, no
runner state-model change, no proxy passthrough, no per-retailer adapter.

---

## Test Coverage

New test file: `forseti-harness/tests/unit/test_durability_us_storefront_pin_wiring.py`
8 offline tests (all green):

- Allowlist entry confirmed
- Proxy/identity flags excluded (regression)
- Writer CLI accepts and forwards `--delivery-zip`
- Writer CLI passes `None` when flag absent
- Packet manifest records limitation note
- Adapter writes `delivery_zip_requested` to metadata and adds limitation note
- Adapter no-pin path: metadata None, no limitation note
- Runner end-to-end: `--writer-arg=--delivery-zip 10001` passes allowlist and reaches writer

Existing test updated: `test_source_capture_cloakbrowser_snapshot.py` — added `"delivery_zip": None`
to expected kwargs in `test_fetch_cloakbrowser_snapshot_capture_with_fake_engine_records_method_provenance`.

---

## Next Steps (Owner-Gated)

- Land via PR to `main` (no self-merge).
- If demand-durability capture series is commissioned for Amazon US, pass `--writer-arg=--delivery-zip 10001`
  (or appropriate US ZIP) per slot in the cadence runner invocation.
- Monitor for selector drift in early slots; adapter will degrade gracefully and warn.
- Bot-wall posture (`access_failed`) enforcement depends on PR #161 (`cloakbrowser-block-detect-amazon-interstitial-v0`)
  landing before live Amazon capture slots run.
