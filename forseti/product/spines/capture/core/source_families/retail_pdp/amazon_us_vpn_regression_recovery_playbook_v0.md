# Amazon US VPN Regression Recovery Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Cold-agent Retail/PDP recovery playbook
scope: >
  Routes one Amazon US delivery-pinned capture that lands on Amazon Singapore
  through the owner-authorized Surfshark US / New York retry while preserving
  both outcomes and retaining Amazon-owned admission checks.
use_when:
  - The CloakBrowser packet runner emits amazon_us_vpn_fallback_required.
  - A cold agent must distinguish the authorized SG recovery from selector drift or another marketplace failure.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
  - forseti-harness/tests/unit/test_durability_us_storefront_pin_wiring.py
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
stale_if:
  - The Amazon delivery-pin failure tokens, Surfshark route, or retailer-owned admission conjunction changes.
```

## Purpose and boundary

This is the cold-agent front door for one narrow recovery:

```text
direct Amazon US attempt
  -> preserved final Amazon Singapore marketplace
  -> amazon_us_vpn_fallback_required
  -> observe and activate pre-existing Surfshark US / New York route
  -> repeat the same capture once
  -> admit only on Amazon-owned US / USD / ZIP 10001 evidence
  -> preserve both packets
  -> disconnect Surfshark
```

The capture runner classifies the recovery condition; it does **not** activate,
authenticate, or independently verify Surfshark. VPN geography is transport
posture, not storefront or delivery-pin evidence.

Owner authorization provenance: on 2026-07-19 Asia/Singapore, the owner
authorized one Surfshark-backed Amazon capture when a delivery-pinned Amazon US
attempt regresses to Singapore. This artifact narrows that authorization to the
machine-visible trigger and single retry below. A receiving agent must still
follow its active Windows-control confirmation and safety rules; this playbook
does not override them.

Do not use this route for:

- an Amazon.com page that merely fails to display ZIP `10001`;
- selector drift, a missing location widget, an access block, CAPTCHA, or
  generic content insufficiency;
- Amazon Canada, UK, or any non-Singapore marketplace;
- a capture that did not commission `--delivery-zip`;
- a second VPN retry after the first VPN-backed result fails.

Those are typed stops, not permission to broaden the recovery.

## Machine-visible trigger

For a capture with `--delivery-zip`, the runner emits the recovery only when
the preserved final hostname is exactly `amazon.sg` or `www.amazon.sg`.

The same packet carries:

```yaml
stderr_token: amazon_us_vpn_fallback_required
manifest_visible_mode_change: amazon_us_vpn_fallback_required
manifest_limitation_prefix: amazon_us_vpn_fallback_required
browser_metadata:
  amazon_us_vpn_fallback_required: true
  amazon_us_vpn_fallback_trigger: final_marketplace_host_amazon_sg
```

It also retains `amazon_delivery_zip_pin_failed`, exits nonzero, and remains
inadmissible as Amazon US evidence. The new token does not replace or weaken
that failure.

## Cold-agent fast path

### 1. Preserve and verify the direct failure

Fresh-read the failed packet before changing network posture:

- packet ID and output directory;
- requested and final URL;
- `manifest.json` file hashes and byte lengths;
- `raw/04_cloakbrowser_snapshot_metadata.json`;
- both failure tokens in `visible_mode_changes`;
- final hostname `amazon.sg` or `www.amazon.sg`;
- `pin_confirmed=false`;
- `amazon_us_vpn_fallback_required=true`.

If any binding is absent or contradictory, stop with
`AMAZON_VPN_RECOVERY_TRIGGER_NOT_PROVEN`. Do not activate the VPN.

Retain the exact original capture command. The retry must keep the same:

- subject and requested Amazon.com URL;
- retail capture profile and subject-specific sufficiency checks;
- delivery ZIP `10001`;
- settle, scroll, timeout, and access posture;
- no-cart, no-login, and no-cookie-injection boundary.

Only the output destination and the two retry annotations below may differ.

### 2. Activate Surfshark through the existing desktop app

Use the available Windows-control mechanism and the pre-existing Surfshark
installation. Do not add a CLI wrapper, install software, expose account
details, automate login, or handle credentials.

1. Select the uniquely returned Surfshark window.
2. Observe its current connection state before clicking.
3. Select `United States` / `New York`.
4. Connect once.
5. Refresh the Surfshark window and require its own UI to show the selected
   United States / New York connection as active.

If Surfshark is signed out, asks for authentication or permissions, exposes no
US / New York route, or does not visibly confirm the connection, stop with
`AMAZON_VPN_RECOVERY_NETWORK_POSTURE_UNAVAILABLE`. Never infer connection from
the requested click.

### 3. Repeat the exact capture once

Run the original capture command once with a fresh output destination and
append:

```text
--visible-mode-change operator_observed_surfshark_us_new_york
--limitation "external Surfshark US / New York posture was observed in the desktop app; the capture runner did not activate or independently verify the VPN; Amazon-owned final-page signals decide admission"
```

Do not remove the original `--delivery-zip 10001`, retail profile, or
subject-specific checks. Do not substitute another product, Amazon host,
stored browser profile, cookie, login, cart interaction, or proxy.

### 4. Decide the retry from preserved evidence

A VPN-backed retry is admissible only when all commissioned signals pass:

- runner exit code is zero;
- final hostname is `amazon.com` or `www.amazon.com`;
- browser metadata has `pin_confirmed=true`;
- browser metadata has `amazon_us_vpn_fallback_required=false`;
- the packet has no `amazon_delivery_zip_pin_failed` or
  `amazon_us_vpn_fallback_required` mode change;
- Amazon's rendered location anchor binds delivery ZIP `10001`;
- Amazon's rendered marketplace state binds Amazon US;
- the original profile or subject-specific sufficiency checks bind exact
  `USD` and the commissioned subject/product.

VPN route, IP address, `.com`, dollar glyph, or successful page load cannot
substitute for any of those signals.

If the retry fails, preserve it and return
`AMAZON_US_VPN_RETRY_FAILED_TYPED_STOP`. Do not loop, rotate servers, change
products, weaken checks, or promote either packet.

### 5. Close the bounded network posture

After the retry packet is durably preserved—success or failure—return to the
same Surfshark window, disconnect, refresh, and require the app UI to show the
VPN is no longer connected. If disconnect state cannot be verified, report
`SURFSHARK_DISCONNECT_STATE_UNVERIFIED`; do not claim normal network posture.

The capture result and the network closeout are separate claims. A successful
Amazon packet does not prove Surfshark was disconnected afterward.

## Fixed historical failure case

Use this case to verify cold-agent classification and documentation. Do not
rewrite its historical packet:

```yaml
case_id: AMAZON_US_TO_SG_MAKEWAVES_20260718
subject: Tower 28 MakeWaves Mascara
requested_url: https://www.amazon.com/dp/B0BGMBRQP7
final_url: https://www.amazon.sg/dp/B0BGMBRQP7?ref_=mr_direct_us_sg_sg&showmri=undefined&th=1
packet_id: 01KXRPD65YCFHVDTMV3QV0HPA7
packet_locator: F:\forseti-data-lake\raw\e99\01KXRPD65YCFHVDTMV3QV0HPA7
observed_metadata:
  delivery_zip_requested: "10001"
  final_marketplace: amazon.sg
  pin_confirmed: false
  proxy_used: false
  geoip_used: false
  persistent_profile_loaded: false
typed_outcome_at_capture: GEO_REDIRECT_US_SELLER_UNOBSERVABLE
current_recovery_classification: amazon_us_vpn_fallback_required
```

Fresh reads showed that the preserved packet requested Amazon.com, landed on
Amazon.sg, displayed Singapore-dollar state, and did not retain the ZIP or
seller binding needed for the US read. The packet predates the new recovery
token, so its immutable manifest does not carry that token retroactively. Its
preserved requested/final URL pair is the ground truth for backtesting the
current classifier.

Expected cold-agent decision:

```yaml
direct_packet: preserve_and_reject
vpn_action: one_surfshark_us_new_york_retry_authorized
retry_subject: same_makewaves_asin
retry_admission: amazon_owned_us_usd_zip_10001_and_subject_binding
retry_limit: 1
post_retry: disconnect_and_verify
```

## Failure-case recording for future examples

For every later SG regression, record:

- direct packet ID and requested/final URLs;
- runner token and metadata trigger;
- subject, ASIN, and original capture profile;
- whether Surfshark US / New York connection was observed or unavailable;
- retry packet ID and admission result;
- exact failed admission signal when the retry stops;
- disconnect verification state.

Never record Surfshark account details, credentials, session secrets, or a VPN
exit IP as pin proof. Append a new case only after both packet receipts are
fresh-read; do not convert an unpreserved scouting observation into a case.

## Non-claims

This playbook is not a claim that VPN use avoids Amazon controls, guarantees a
US storefront, establishes delivery availability, or proves price, seller
authorization, demand, velocity, revenue, sell-through, market share, or
commercial performance.
