# ILIA Beauty Phase 1 — Fresh Scan Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Evidence-only scan and capture receipt
scope: >
  Historical typed source-access outcomes, packet receipts, route failures,
  stopping rationale, and parent-dimension friction for the 2026-07-18 ILIA
  Beauty Phase 1 run.
use_when:
  - Auditing the evidence base and capture failures behind the withdrawn ILIA Phase 1 report.
  - Distinguishing captured source content from discovery-only or blocked routes.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_ilia_phase1_commission_board_v0.md
stale_if:
  - Always for current ILIA evidence or route-exhaustion claims; the associated report was withdrawn from decision-facing use on 2026-07-19.
  - A later ILIA scan supersedes this bounded 2026-07-18 run.
```

> **Historical capture receipt only.** This receipt remains the audit trail for
> `docs/research/forseti_beauty_ilia_phase1_company_competitive_intelligence_report_v0.md`;
> it does not make that withdrawn report current, and it does not claim a
> replacement run or exhausted capture routes.

## Run receipt

```yaml
scan_receipt:
  scan_id: ilia_beauty_phase1_20260718
  subject: ILIA Beauty
  pool_id: USBEAUTY-021
  resolved_parent_input: Famille C
  mode: forward
  time_posture: recency_first
  as_of_date: "2026-07-18"
  started_at: "2026-07-18T03:30:00Z"
  capture_window_observed: "2026-07-18T04:00:01Z/2026-07-18T04:06:12Z"
  effective_target_worktree: C:/Users/vmon7/Desktop/projects/orca/.claude/worktrees/beauty-tower28-ci-gtm-handoff-f8650b
  starting_revision: 34c8153240a8af2bddabe8f7f6bab76ca822df1a
  starting_branch: claude/ilia-phase1-commission-handoff
  preexisting_untracked_artifact: tmp_tower28_compare/
  preexisting_untracked_handling: not_opened_not_modified
  tower28_synthesis_loaded: false
  login_wall_crossed: false
  cart_interaction: false
  scheduler_or_monitor_created: false
```

The worktree’s pre-existing `tmp_tower28_compare/` was treated as another
author’s artifact and was not inspected. The scan used only the ILIA handoff,
the ratified CSB contract, the capture recon index, public-source discovery, and
ILIA-specific source content.

## Capture and access ledger

| Receipt | Route and source | Outcome | Durable locator / typed limitation |
| --- | --- | --- | --- |
| CAP-001 | Anonymous CloakBrowser; ILIA homepage | `captured` | Packet `01KXSP35CM9B5N4W3GPV5EFHDZ`; rendered DOM, visible text, screenshot, and metadata. The page resolved to an SG-localized context, so locale-sensitive price/SPF text is not treated as US state. |
| CAP-002 | Anonymous CloakBrowser; ILIA Super Serum Skin Tint PDP | `captured` | Packet `01KXSP35THSK9RTFTW82P5W1BK`; USD price, current claims, review aggregate, visible substantive review text, and verified-buyer/incentive markers preserved. |
| CAP-003 | Anonymous CloakBrowser; ILIA warranty | `captured` | Packet `01KXSP35CMGVAN71CSZYMDW0P0`; current authorized-Amazon-reseller rule preserved. |
| CAP-004 | Anonymous CloakBrowser; FashionNetwork acquisition article | `captured` | Packet `01KXSP356CJA353PJ1SD0V91DQ`; dated 2022 acquisition and historical ownership/independence language preserved. |
| CAP-005 | Sephora PDP distribution profile | `packet_written_sufficiency_failed` | Packet `01KXSP5MEEJPNS8C19JS6PV1H7`; requested PDP redirected to a redacted search surface. Profile also demanded unrelated LANEIGE literals such as `Lip Sleeping Mask`. No Sephora review classification was admitted. |
| CAP-006 | Ulta brand-grid profile | `blocked_after_capture_runtime` | Runner hit a missing lake availability-index record and returned exit `3`; no Ulta packet was found in the permitted target inspection. Current Ulta pages were visible through public search discovery only. |
| CAP-007 | Ulta PDP distribution profile | `timeout_terminated_no_packet_observed` | The bounded job exceeded its wait and was terminated. The single target inspection found no Ulta packet. No retry was made. |
| CAP-008 | Amazon PDP distribution profile with delivery ZIP `10001` | `packet_written_us_pin_failed` | Packet `01KXSP5CP0B7YYBDSSJ21XXHPK`; Amazon redirected to `amazon.sg`, the delivery widget could not be opened, USD/ZIP anchors were absent, and seller of record was not established. The profile also carried unrelated sufficiency literals. |
| CAP-009 | ILIA careers page | `blocked_lake_index` | Browser retrieval reached the route, but the writer hit a missing availability-index record; no packet was found. Public search discovery exposed the official careers surface, but no organizational-motion conclusion depends on it. |
| CAP-010 | DailyMed ILIA label | `blocked_lake_index` | The packet writer hit the same missing availability-index record; no packet was found. The official DailyMed record was visible through public search discovery and is used only as corroboration with an explicit preservation gap. |
| CAP-011 | Old Reddit direct HTTP; r/Sephora skin-tint comparison thread | `captured` | Packet `01KXSPE6E9MMH9WTVE0DCFB2QW`; HTTP 200; `raw/01_content_record.json` contains 182 parsed comments. |
| CAP-012 | Old Reddit direct HTTP; r/Sephora skin-tint recommendation thread | `captured` | Packet `01KXSPEAQVCXYG0EPVD95MZPBY`; HTTP 200; `raw/01_content_record.json` contains 82 parsed comments. |
| CAP-013 | Old Reddit direct HTTP; r/MakeupAddiction Multi-Stick thread | `captured` | Packet `01KXSPEEK3BSBGJQMGDWD0EJAG`; HTTP 200; `raw/01_content_record.json` contains 34 parsed comments. |
| CAP-014 | Reddit batch consolidation | `receipt_contradiction_visible` | `C:/tmp/forseti-ilia-phase1-reddit/batch_summary.json` reports three successful lake commits but also `raw_html_missing` and `content_record_preserved: false`. Fresh packet manifests show the content records present; the manifests and files are the primary observation. |
| CAP-015 | Quora experimental scout | `blocked` | Public search reported a non-retryable `robots.txt` block. No login, persistent profile, or bypass was attempted. |
| CAP-016 | CIPO trademark record | `discovery_source_backed_not_packetized` | Official Canadian trademark record for ILIA was visible and names current owner `Ilia Inc.`; no capture packet was written. |
| CAP-017 | Leaping Bunny directory check | `source_backed_currentness_limited` | A Leaping Bunny-hosted company list contains `ILIA Inc.`, but the document’s currentness is ambiguous. It corroborates historical listing only, not current annual certification status. |
| CAP-018 | Public search discovery for Ulta and Sephora | `checked_evidence_found_not_packetized` | Current product/brand pages were visible, supporting present retail availability and assortment pointers. Locale-sensitive prices, review rates, sales, and inventory depth are not claimed. |

## Operator and runner friction

Two initial direct-HTTP batches failed before network acquisition because the
timing field was supplied first as free text and then as both a value and a
reason; both forms violate the packet schema. The corrected route uses
`--cutoff-posture-unknown-reason` alone for a forward commission. Retail
profiles also require the `cloakbrowser_snapshot` source-surface literal and
their owning CloakBrowser runner.

The retailer sufficiency profiles still contain subject-specific literals from
an unrelated product. This affected Sephora and Amazon exit status after real
packets were written. The raw packet contents were inspected under the handoff’s
documented workaround; the sufficiency failures remain visible and were not
converted into success.

## Fresh-scan evidence bounds

- The brand-owned PDP exposed current review bodies and verified-buyer markers,
  but the visible rows were not a randomized or representative sample and some
  were explicitly incentivized.
- The three Reddit threads are bounded, venue-specific customer-world samples.
  They establish that named experiences and comparisons exist; they do not
  establish prevalence, demand, population rates, or cross-brand superiority.
- The Amazon packet is an SG redirect, not a US vantage. The only US-authorized
  seller fact comes from ILIA’s own warranty page; current Amazon seller of
  record and diversion state remain unknown.
- Current Ulta and Sephora availability is supported by public discovery, not a
  successful durable retailer packet. No inventory, sell-through, or revenue
  claim follows.
- The acquisition article is a 2022 historical source. Its then-current CEO,
  minority stakes, and independence language are not silently relabeled as
  current.

## Parent-dimension friction feedback

The contract’s single `subject_identity` object can resolve ILIA as a `brand`,
but it cannot simultaneously encode three distinct layers:

1. ILIA Beauty as the market-facing brand;
2. `Ilia Inc.` as the current trademark owner visible in an official registry;
3. Famille C as majority owner in the 2022 acquisition reporting, with Clarins,
   the founder, and then-management described as minority holders.

This run therefore uses `subject_kind: brand` and `identity_state: resolved`,
then carries the parent and entity chain in observations, limitations, and
`GAP-001`. It does not rewrite the CSB contract and does not infer that Clarins
is the operating entity. The exact current legal ownership chain from Famille C
to Ilia Inc. remains unverified by a current official ownership tree.

## Necessary-completeness stop

The scan stopped because every required decision-neutral lens has either
source-backed evidence or a typed gap:

- current positioning, hero claims, direct commerce, reviews, and sustainability;
- retail availability pointers plus preservation limitations;
- bounded customer-world mechanisms and substitutes;
- acquisition chronology and current trademark-owner context;
- authorized-Amazon-reseller rule plus failed current US seller verification;
- seal claim plus directory-currentness limitation;
- explicit Quora, careers, DailyMed, Sephora, Ulta, and Amazon route outcomes.

Further acquisition would mainly add more instances to already-visible
mechanisms or retry exhausted routes. It would not remove the load-bearing
entity-chain or retail-packet gaps without a new authorized run. The next step
is owner adjudication; no next pool company is commissioned.
