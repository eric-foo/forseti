# Fragrance Purchase-Review Retailer Recon v0

```yaml
artifact_role: Capture recon / route pin
scope: Single-fixture source-capture recon for niche fragrance retailer PDP purchase-review surfaces.
use_when:
  - Capturing purchase reviews from fragrance-specialist retailers.
  - Deciding whether to use Direct HTTP or CloakBrowser before downstream review integrity analysis.
  - Explaining why a sampled retailer is GO, PARTIAL, or fixture-positive for row-level review capture.
authority_boundary: Retrieval-only. This artifact does not score review integrity, infer sentiment, normalize products, or certify source-wide completeness.
open_next:
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
stale_if:
  - Retailer review vendor, PDP template, or anti-bot posture changes materially.
  - CloakBrowser or Direct HTTP packet schema changes.
  - A later fixture contradicts the sampled verdict below.
```

## Boundary

This is a capture-routing artifact. It records observed source-access posture,
working runner/rung, substrate location, and a pinned recipe for the current
fragrance purchase-review lane.

In scope:

- Public niche fragrance retailer PDPs selected by the owner: Luckyscent /
  Scent Bar, Twisted Lily, ZGO Perfumery, Indigo Perfumery, and Ministry of
  Scent.
- Review-row substrate visibility: body text, rating, date, reviewer/verified
  buyer labels, source-app labels, and product/variant context where source-visible.
- Runner choice and minimum observed flags.

Out of scope:

- Reddit, community, forum, editorial, and CSB-style lanes.
- Brand DTC sources except on-demand follow-up.
- Any bypass of authentication, CAPTCHA, Cloudflare challenge, paid account, or
  private review portal.
- Review quality, demand inference, review fraud scoring, or cleaning/ECR claims.

## Route

- Cynefin route: complicated with a complex access edge.
- Bottleneck: source-access and substrate uncertainty per retailer.
- Riskiest assumption: fragrance-specialist retailers expose review bodies on
  public PDP pages, not only aggregate counts or vendor-widget shells.
- Stop/pivot condition: auth/CAPTCHA/private gate, or no review-row substrate on
  a sampled PDP after one bounded Direct HTTP plus rendered re-probe.
- Isolation: worktree branch `codex/fragrance-purchase-review-probes`.

## Probe Inputs

Original sampled PDPs:

| Retailer | Sampled PDP |
| --- | --- |
| Luckyscent / Scent Bar | `https://www.luckyscent.com/products/memoirs-of-a-trespasser-by-imaginary-authors` |
| Twisted Lily | `https://twistedlily.com/products/essential-parfums-discovery-set-1` |
| ZGO Perfumery | `https://zgoperfumery.com/products/diptyque-orpheon-eau-de-parfum` |
| Indigo Perfumery | `https://indigoperfumery.com/products/memoirs-of-a-trespasser` |
| Ministry of Scent | `https://ministryofscent.com/products/memoirs-of-a-trespasser` |

Known-reviewed fixture re-probe PDPs:

| Retailer | Capture fixture |
| --- | --- |
| ZGO Perfumery | `https://zgoperfumery.com/products/d-s-durga-concrete-lightning-eau-de-parfum` |
| Indigo Perfumery | `https://indigoperfumery.com/products/indigo-perfumery-sampler-set` |

The re-probe used bounded public-site fixture discovery: Shopify search-suggest
queries for candidate products, exact PDP reads for candidates, then one packeted
known-reviewed fixture per rescue site. It was not a crawl, scaled scrape, auth
bypass, or challenge-solving run.

## Observed Verdicts

| Retailer | Direct HTTP observation | Rendered observation | Verdict | Route pin |
| --- | --- | --- | --- | --- |
| Luckyscent / Scent Bar | HTTP 200 PDP body preserved. Static HTML exposed aggregate JSON-LD review substrate (`ratingValue: 3.71`, `reviewCount: 14`) and review anchors, but no review-body rows. | CloakBrowser render plus progressive scroll exposed row-level review text and metadata: sampled DOM/text showed 10 review bodies, titles, dates, reviewer names, country labels, variant labels, `data-verified-buyer`, and store-invitation labels. | `GO_ROW_LEVEL_RENDERED` | CloakBrowser packet with `--settle-seconds 5 --scroll-step-px 500 --scroll-passes 4`. |
| Twisted Lily | HTTP 200 PDP body preserved. Static HTML exposed Shopify/vendor review config and aggregate count substrate, but not usable row text. | CloakBrowser render plus progressive scroll exposed row-level review text and metadata: sampled visible text showed 6 reviews, rating summary, reviewer names, dates, verified labels, locations, and Shop App labels. | `GO_ROW_LEVEL_RENDERED` | CloakBrowser packet with `--settle-seconds 5 --scroll-step-px 500 --scroll-passes 4`. Variant URL normalization may append `?variant=...`; record actual final URL. |
| ZGO Perfumery | Original sampled fixture: HTTP 200 PDP body preserved, but Yotpo/widget config had zero-count/no row bodies. Known-reviewed fixture: Direct HTTP packet preserved static HTML with one Yotpo review row. Later widget-generation diagnosis found the row-positive Yotpo v3 storefront route with native review id, created datetime, verified-buyer flag, aggregate rating, star distribution, and media absence diagnostics. | CloakBrowser was not needed for the known-reviewed fixture. Original rendered fixture remained row-empty; older Yotpo v1 widget endpoints also remained row-empty. | `GO_ROW_LEVEL_YOTPO_V3_KNOWN_REVIEWED_FIXTURE` | Preferred route is `GET https://api-cdn.yotpo.com/v3/storefront/store/LotcNgdZUJLtOh7iQPZPMJPRTLfGpWs2nlS5U8eh/product/10788875403567/reviews?page=1&perPage=10`; Direct HTTP static section is fallback. Do not reuse the original Orpheon zero-count fixture for row capture. |
| Indigo Perfumery | Original sampled fixture: Direct HTTP failed before packet write with local certificate verification error. curl_cffi reached HTTP 200 during diagnosis but did not expose row bodies on the original fixture. | Known-reviewed fixture: CloakBrowser render+scroll preserved rendered DOM with five JSON-LD / Judge.me `Review` objects carrying `reviewBody`, rating, date, author, review title/name, and product binding. Visible text still showed only the `CUSTOMER REVIEW` section label and no visible row bodies. | `GO_ROW_LEVEL_RENDERED_SCHEMA_ONLY_KNOWN_REVIEWED_FIXTURE` | CloakBrowser packet with `--settle-seconds 5 --scroll-step-px 500 --scroll-passes 4` on `https://indigoperfumery.com/products/indigo-perfumery-sampler-set`; carry a visible-row residual. |
| Ministry of Scent | HTTP 200 PDP body preserved. Static HTML exposed Judge.me review rows directly, including `jdgm-rev__body`, titles, verified-buyer labels, dates, product title, review source labels, and thumbs counts. | Not needed for the sampled fixture. | `GO_ROW_LEVEL_DIRECT_HTTP` | Direct HTTP packet is sufficient first rung. Escalate to CloakBrowser only if a later product uses lazy-loaded rows. |

## Rung-1 / Rung-2 Recheck

The first pass used Direct HTTP and CloakBrowser. After owner challenge, two
intermediate rungs were checked explicitly:

| Rung | Status in this lane | Result |
| --- | --- | --- |
| `anti_blocking_http` rung 1 | Built packet runner. Wrote scratch packets for Luckyscent, Twisted Lily, ZGO, and Ministry; Indigo failed with the same local certificate verification error as Direct HTTP. | Did not add row-level signal beyond the original verdicts. Luckyscent remained aggregate-only; Twisted Lily exposed review-widget/Judge.me configuration strings but not review rows; original ZGO fixture remained zero-count/widget-shell; Ministry still exposed Judge.me rows. |
| `curl_cffi` rung 2 | Installed locally, but no shared Source Capture packet runner is built in this branch; the documented shared rung is gated/unbuilt. A read-only ad hoc `curl_cffi` diagnostic was run with Chrome impersonation, so it is diagnostic evidence, not packeted Armory output. | HTTP 200 for all five original sampled fixtures. It did not expose additional row bodies: Luckyscent remained aggregate-only, Twisted Lily remained config-only, original ZGO remained widget/zero-count only, original Indigo returned the Shopify review container but no rows, and Ministry still exposed rows. |

Impact: rung 1 and the ad hoc rung 2 diagnostic did not unlock the original
ZGO/Indigo fixtures. The correct next move was known-reviewed fixture discovery,
not declaring those sites worthless. That re-probe found row-positive fixtures
for both sites.

## Fixture Evidence Packets

Scratch packet evidence was written under
`orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/`:

| Retailer | Packet path | Fresh-read row evidence |
| --- | --- | --- |
| ZGO Perfumery | `zgo_known_reviewed/direct_http_packet`; later `zgo_completion_probe_20260629/v3_validation_probe` | Original raw HTTP body had the static Yotpo section. Later v3 validation confirmed 1 total row, native review id, created datetime, verified flag, 5.0 average, 5-star distribution, 99-word body, and zero review media. |
| Indigo Perfumery | `indigo_known_review_candidate/cloakbrowser_packet` | Rendered DOM existed at 390136 bytes; visible text existed at 1092 bytes; DOM contained five `reviewBody` occurrences inside JSON-LD / Judge.me `Review` objects and zero visible review-row markers. |

## Recipe Notes

1. Start with Direct HTTP when the page body is the target. For this lane, Direct
   HTTP is enough for Ministry of Scent and remains a useful ZGO fallback, but
   the preferred ZGO completion route is now the Yotpo v3 storefront endpoint.
   Direct HTTP is still useful for detecting aggregate-only substrates on Luckyscent, Twisted Lily, and the original ZGO fixture.
2. Escalate to CloakBrowser for rendered review widgets or rendered structured
   review rows. For Luckyscent, Twisted Lily, and the selected Indigo fixture,
   the working recipe is a rendered packet with `--settle-seconds 5
   --scroll-step-px 500 --scroll-passes 4`.
3. Treat zero-count sampled PDPs as bad fixtures, not source-wide failures. The
   original ZGO and Indigo fixtures were row-empty; known-reviewed fixture
   selection changed the operating status.
4. Keep `--recapture-relationship` to an accepted enum such as `supplement`.
   Prose in that field fails runner validation and is an operator error, not a
   source-access fact.
5. Keep `--cutoff-posture` to accepted closed values such as `pre_cutoff`.
   Prose belongs in `capture_context`.
6. Clear `ORCA_DATA_ROOT` for scratch probes when an explicit `--output` path is
   intended. The Direct HTTP runner honors the environment data root ahead of
   the supplied scratch output path.

## Non-Claims

- This recon does not say the five retailers are the best sources for review
  quality. It says which sampled retailer PDP fixtures can currently be captured
  with enough row-level purchase-review data for downstream integrity and
  pain/pleasure-point analysis.
- This recon does not certify broad retailer coverage. It pins the observed
  route for one row-producing fixture per retailer.
- This recon does not authorize scaled scraping or any challenge bypass.
