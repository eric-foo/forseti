# Content-Mode Lane Flip Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold handoff packet for the all-lanes content-packet flip
scope: >
  Hands ownership of the repo-wide capture-artifact-mode flip (content packets
  as standard posture) to the next lane owner: per-lane survey of every
  projection lane, flip order, retirement semantics for post-hoc projection,
  validation route, and stop conditions.
use_when:
  - Starting or resuming the Phase B content-mode flip for any source family.
  - Deciding whether a post-hoc projection runner or module can retire.
  - Checking which capture runner a family uses before wiring ContentCaptureSpec.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
stale_if:
  - ContentCaptureSpec seam shape changes (forseti-harness/source_capture/content_capture.py).
  - Any lane listed below flips, retires its post-hoc path, or changes capture mechanism.
  - The cloakbrowser packet runner gains or rejects a content-capture seam.
```

## Objective

Make capture-time content packets the standard capture posture for every
projection lane and future incoming source (owner direction, 2026-07-17:
"we want this way for all lanes and future incoming sources too"), retiring the
post-hoc projection lane as the standard path for each exact surface that
flips. Efficiency-first: flips happen as lanes are next touched, never waiting
for volume pressure.

## Authority and Currentness

- The content-mode standard is owned by
  `source_capture_playbook_v0.md` ("Capture artifact mode — content-mode
  standard"). The generic HTTP-seam reference implementation and semantics
  (content/sample/raw modes, provenance floor, raw-fallback, parser-version
  discipline, parser-fit drift check) remain the Reddit lane: design doc
  `reddit_radar_grid_capture_maintenance_design_v0.md`, seam
  `forseti-harness/source_capture/content_capture.py`, runner
  `forseti-harness/runners/run_source_capture_http_packet.py`.
- Parfumo's pinned targeted-rendered product-page surface is a second,
  family-owned implementation because its projector consumes multiple local
  browser artifacts. Its contract is
  `docs/workflows/parfumo_targeted_capture_contract_v0.md`; this does not
  establish a generic multi-artifact seam.
- Basenotes' pinned persistent-Chrome product-page surface is the next
  family-owned implementation. It confirms the same lifecycle with a browser
  metadata provenance artifact and trigger-controlled screenshot acquisition.
  The second implementation is evidence for a later shared-mechanics extraction,
  not authority to extract one in this work unit; parsers and schemas remain
  family-owned.
- Fragrantica's two rendered CloakBrowser slices are the third implementation
  and the first caller of the shared rendered retention/fallback seam in
  `run_source_capture_cloakbrowser_packet.py`. The seam owns only artifact-mode,
  hashing, retention, metadata, and raw-fallback mechanics. Fragrantica's
  content schema and parser remain family-owned. Its direct-HTTP slice remains
  an unchanged raw canary.
- Retail's first exact flip is `sephora_pdp_aggregate`. It reuses only the
  shared CloakBrowser mode/hash/retention/fallback lifecycle and retains a
  Sephora-owned schema, parser-fit checker, and exact country-continuation
  preflight. The US/USD market pin, absent country dialog, access, source-detail
  sufficiency, and projection must all pass before DOM/text are discarded.
  Screenshots remain active-capture evidence. Every sibling retail PDP/grid
  profile remains raw.
- Retail's second exact flip is `luckyscent_pdp_aggregate`. It reuses the same
  shared CloakBrowser lifecycle with a Luckyscent-owned schema and parser-fit
  checker. The assertion-only default-storefront pin must bind one serialized
  `country=US` + `market=market-us` + `currency=USD` context; failed pin,
  access, sufficiency, or projection preserves DOM/text and exits nonzero.
  The content record carries all three target variants and all eight rendered
  target reviews without normalizing the shared Retail/PDP schema. The Direct
  HTTP brand grid and every other sibling retail profile remain raw.
- "Projection spine" was never an accepted spine. The operating-model v2
  Bloat-Cut Queue explicitly excludes a "Standalone Projection Spine …
  or any projection practice that drops evidence rows before ECR/Cleaning"
  (`data_capture_harness_operating_model_architecture_v2.md`). There is
  nothing to take down as a spine; retirement is per-family retirement of
  post-hoc projection runners/invocations. Content mode is compatible with
  the bloat-cut clause: it discards raw bytes with hash provenance, never
  evidence rows.
- Retirement semantics: projector code may remain shared between capture-time
  and post-hoc invocation. What retires is post-hoc projection as the standard
  path for the exact surface that flipped. The shared invocation survives for
  sample-mode drift checks, legacy/raw packets, and any unflipped canary or
  sibling surface. Bump the family's parser version on any projector behavior
  change.

## Seam Hardening Provenance

PR #1057 (Reddit Phase A) merged at head `fd93b6c3` before its adjudicated
delegated-review patch could land (a harness outage blocked the apply). The
patch (3 accepted findings: projector-output type guard before raw discard;
honest parse-in-flight reporting on non-2xx fallback; parser-fit checker
trust hardening) lands in the same work unit that carries this packet. If
this packet is readable on main, the hardening is in; further lane flips
build on the hardened seam.

## Lane Survey (verified in-repo, 2026-07-17)

| Lane | Capture mechanism | Post-hoc projection | Flip feasibility |
| --- | --- | --- | --- |
| Reddit grid + threads | HTTP packet seam | `source_capture/reddit_projection.py` (legacy), consolidation | DONE (content mode default; PR #1057) |
| Parfumo targeted-rendered product page | Local operator-visible Chrome artifact bundle (`run_parfumo_mgt_capture.py --targeted-rendered`) | `parfumo_projection.py`, cleaning catchup | PINNED ROUTE FLIPPED: family-owned hybrid content adapter; direct HTTP remains a raw canary; shared projection runner remains for raw/legacy/canary packets |
| Fragrantica MGT | 3 slices: direct HTTP + 2 CloakBrowser (initial viewport, deep scroll) (`run_fragrantica_mgt_capture.py`) | `fragrantica_projection.py`, cleaning catchup | RENDERED SLICES FLIPPED: both CloakBrowser packets default to content mode through the shared rendered retention seam; direct HTTP remains a raw canary; raw/sample/legacy projection remains supported |
| Basenotes MGT | Persistent Chrome current-window bundle or credential-free loopback CDP (`run_basenotes_mgt_capture.py`) | `basenotes_projection.py`, cleaning catchup | PINNED ROUTE FLIPPED: family-owned content adapter; browser metadata retained; screenshot acquisition requires a named visual trigger; raw/legacy projection runner remains |
| Retail PDP / retail grid | CloakBrowser packets over retailer PDPs | `retail_pdp_projection.py`, `retail_grid_projection.py` (deterministic per-packet, excerpt-carrying anchors) | THREE PINNED ROUTES FLIPPED: `sephora_pdp_aggregate`, `luckyscent_pdp_aggregate`, and `nordstrom_pdp_aggregate` default to retailer-owned content records after their distinct US/USD, access, sufficiency, parser-fit, and Projection/Silver gates pass; raw/sample/legacy remain supported; Direct HTTP grids and every sibling PDP/grid profile remain raw. Luckyscent and Nordstrom delivery remain explicitly unpinned. |
| IG reels grid / calls / momentum | Live browser session, passive JSON responses; runner already extracts observations at capture time | `ig_reels_grid_projection.py` (+ catchup with record-id derivation ranks re-reading raw payloads) | DESIGN PASS REQUIRED: catchup semantics depend on raw; do not flip until catchup is re-specified against content records |
| TikTok batch | Video packets (media + metadata) | `tiktok/batch_projection.py` aggregates coverage ACROSS packets | NOT A FLIP TARGET: cross-packet aggregation, media raw is the evidence |
| YouTube behavioral | Metadata packets + captions + ASR across lake | `youtube_capture/behavioral_projection.py` aggregates | NOT A FLIP TARGET as a whole; only per-page watch-metadata parse is candidate |
| LinkedIn live adapter | Live-session runtime extraction | `linkedin_live_adapter/projection.py` per-observation | Already effectively capture-time; audit raw retention posture only |

## Flip Order (recommended)

1. Parfumo pinned targeted-rendered surface: flipped with a family-owned
   multi-input adapter after live parser-fit, Cleaning-equivalence, retention,
   and size-reduction gates. Direct HTTP remains an unflipped raw canary.
2. Basenotes pinned persistent-Chrome surface: flipped with a family-owned
   multi-input adapter after live parser-fit, Cleaning-equivalence, retention,
   screenshot-economy, and size-reduction gates.
3. Fragrantica rendered slices: flipped. Direct HTTP remains a raw canary.
   Shared CloakBrowser mechanics are limited to mode/hash/retention/fallback;
   the Fragrantica parser and schema remain family-owned.
4. CloakBrowser content capture seam: added for the selected Fragrantica
   rendered route. Retail may reuse this lifecycle only with a retailer-owned
   parser-fit and Projection/Silver-equivalence proof.
5. Sephora aggregate PDP: flipped with a retailer-owned schema/parser and exact
   country-continuation preflight after parser-fit and Projection/Silver
   equivalence proof. US/USD market, country-dialog absence, access,
   sufficiency, and projection failures preserve DOM/text. Other retail
   profiles remain raw.
6. Luckyscent aggregate PDP: flipped with a retailer-owned schema/parser and
   assertion-only default US/USD storefront pin. All three target variants and
   all eight rendered target reviews remain carried; delivery is unpinned and
   the Direct HTTP brand grid remains raw.
7. Nordstrom aggregate PDP: flipped with a retailer-owned schema/parser after
   the country-preference flow confirms selected US/USD plus the US shopper
   context. The setup tries Nordstrom's homepage control first and may use the
   same semantic country control on the exact commissioned PDP when the
   homepage control is absent; final rendered state remains the admission
   authority. The requested numeric PDP id binds the offer/review substrate;
   `Shipping to 518225` stays a residual and never becomes US-delivery proof.
8. Re-point each flipped surface's cleaning catchup consumers at content
   records, then retire that surface's post-hoc lane as its standard path in
   the same work unit (reconcile the family design doc and any playbook
   mention).
8. IG family: separate design pass for catchup/derivation-rank semantics
   before any flip. TikTok/YouTube aggregation lanes stay as they are — they
   are not raw-to-derived projections.

## Edit Authority, Validation Route, Stop Conditions

- Each flip is one bounded work unit per family requiring explicit owner
  authorization per AGENTS.md (this packet is survey + order, not standing
  implementation authority).
- Validation per flip: family unit tests + full
  `python -X utf8 -m pytest forseti-harness/tests/unit -p no:warnings -q`
  + one live dogfood capture with parser-fit `match` before the default flips.
- Stop and surface to the owner if: a projector needs inputs unavailable at
  capture time; a downstream consumer reads raw bytes directly; the
  cloakbrowser seam extension would change packet manifest semantics for
  existing packets; or a family's raw is itself the evidence (media).

## Non-Claims

Not validation, readiness, owner acceptance of the flip order, ECR/Cleaning
authority, or authorization to implement any flip without a bounded owner
instruction.
