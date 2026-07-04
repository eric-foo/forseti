---
retrieval_header_version: 1
artifact_role: Facilitator-side source-provenance record (NOT contestant-visible; not a band input)
scope: >
  Per-evidence-unit provenance for case topicals_retail_expansion_2021_v0: what is archive-captured
  (the org-motion hiring signal), what is a case-stated construction premise (the brand/channel/expansion
  context), and what is a general base rate. Records the honest sourcing limits behind the participant
  packets' source_manifest, and binds each org-motion captured claim to a body-verified span in the
  captured snapshot body.
use_when:
  - Auditing what each E-unit (E1-E6) is actually sourced from.
  - Checking the org-motion L2 span bindings against the captured body.
  - Confirming org-motion is the only baseline-vs-augmented arm delta.
authority_boundary: retrieval_only
open_next:
  - docs/research/orgmotion_topicals_capture_feasibility_v0.md
  - source_captures/e6_careers_20210303/receipt.md
---

# Source Provenance Notes — topicals_retail_expansion_2021_v0 (v0)

Facilitator-side record. This is **not** part of the contestant-visible packet and is **not** a band
input. It documents, honestly, what each evidence unit is sourced from, so the fixture is not frozen
asserting provenance it does not have. The org-motion evidence is a Wayback archive snapshot preserved as
a `SourceCapturePacket`
(`source_captures/e6_careers_20210303/`, packet ID
`01KV2M7XPZENAJJ74H1QVWCW6E`); the brand/channel/expansion context is asserted facilitator-side as the
scenario's ground truth (not archive-sourced).

## L3 provenance taxonomy — per evidence unit

| E | what it sources | L3 class | sourcing |
| --- | --- | --- | --- |
| E1 | Topicals founded 2020 by Olamide Olowe and Claudia Teng; DTC skincare brand for chronic skin conditions | **case-stated-premise** | facilitator-asserted; real-in-the-world pre-cutoff fact, no captured artifact |
| E2 | Launched 2020-08-07 selling online (own DTC site) + via Nordstrom; ~7 months past launch at cutoff | **case-stated-premise** | facilitator-asserted; real-in-the-world pre-cutoff fact, no captured artifact |
| E3 | National beauty-retail (wholesale shelf-presence) account is an available next-stage distribution path for a young DTC beauty brand | **case-stated-premise** | facilitator-asserted; real-in-the-world situational fact, no captured artifact |
| E4 | DTC→wholesale raises operational demand and is a commitment/execution-risk growth lever | **general-base-rate** | standing analytic prior; asserted, not retrieved (sentinel) |
| E5 | Comparable DTC→retail expansions exist across the consumer/beauty market | **general-base-rate** | standing analytic prior; asserted, not retrieved (sentinel) |
| E6 | Org-motion arm (augmented only) — careers page, 2021-03-03 snapshot, 1 open role: Supply Chain Manager (Full Time), with its full overview/experience/qualities body | **captured-source** | body-verified `SourceCapturePacket` (see L2 spans below) |

## Captured evidence (real SourceCapturePacket, body-verified) — E6

| field | value |
| --- | --- |
| original URL | `https://mytopicals.com/pages/careers` |
| snapshot URL | `https://web.archive.org/web/20210303084505/https://mytopicals.com/pages/careers` |
| snapshot timestamp | `20210303084505` (2021-03-03, pre-cutoff) |
| status | `200` |
| CDX digest | `675QC7DKLKWUKTCKBEETER6UQSMYBEMA` |
| body file | `raw/02_archive_snapshot_body.bin` |
| body sha256 | `db147fc02195e872957d588be376a935aee0fda584960dbd10d063912a0d981b` (129,094 bytes) |
| snapshot_count ≤cutoff | 1 (single pre-cutoff snapshot; no earlier careers capture exists) |

Capture posture: `pre_cutoff`; archive/history posture `archived`; served body equals the selected
snapshot (status 200, no availability≠body redirect). Per the gate-0 feasibility record, this is the
**only** archive-backtestable org-motion surface ≤cutoff — no public ATS board (Greenhouse/Lever/Ashby/
Workable) and no pre-cutoff LinkedIn company-page coverage exist for Topicals.

## L2 claim-support — body-verified spans (E6 / org-motion)

Each atomic quotable org-motion claim in the augmented packet binds to a span present in
`raw/02_archive_snapshot_body.bin`. Spans are page-grain presence checks (verbatim substrings of the
captured body); byte offsets are into the UTF-8 decode of the body.

| # | atomic claim (as used in augmented packet) | body-verified span (verbatim substring present in body) | location in body |
| --- | --- | --- | --- |
| C1 | One open role, titled Supply Chain Manager (Full Time) | `Supply Chain Manager (Full Time)` | visible page body at byte ~76,205 (also present in `<title>`/meta/og/twitter description blocks ~4,571–6,354) |
| C2 | Job Overview: improve all aspects of the supply chain department by reviewing current methodology and processes | `Seek to improve all aspects of the supply chain department by reviewing current methodology and processes` | visible body ~76,300 |
| C3 | Works closely with CEO and CPO to create databases to manage/organize inventory | `Work closely with CEO and CPO to create effective databases to manage and organize inventory` | visible body ~76,420 |
| C4 | Train future members of the Supply Chain team | `Train and instruct future members of the Supply Chain team` | visible body ~76,520 |
| C5 | Maintain vendor relationships while promoting company initiatives | `Maintain a friendly and professional relationship with vendors while promoting company initiatives and values` | visible body ~76,580 |
| C6 | Research cost-efficient shipment procedures | `Research and seek out the most cost-efficient shipment procedures and methods` | visible body ~76,700 |
| C7 | Oversee inventory via a detailed database of available inventory and expected usage | `Organize and oversee inventory by keeping a detailed database of available inventory and expected usage per project` | visible body ~76,780 |
| C8 | Negotiate best-price contracts with partner companies to increase revenue | `Research partner companies and seek to negotiate best-price contracts to increase business revenue` | visible body ~76,900 |
| C9 | Plan/implement supply chain optimization projects | `Plan and implement supply chain optimization projects` | visible body ~77,010 |
| C10 | Ally with the CEO to identify/execute company growth opportunities | `See ways for the company to grow, and ally with the CEO to identify, articulate and execute on those opportunities` | visible body ~77,120 |
| C11 | Requires 2–4 years experience in Supply Chain Management or relevant role | `2-4 years experience in Supply Chain Management or relevant role` | Experience block, visible body ~77,800 |
| C12 | Requires database experience using Google Sheets | `Experience working in and maintaining databases using Google Sheets` | Experience block, visible body ~77,900 |
| C13 | Qualities: self-starter, planner, organized, leader who creates structure for the department | `Be a leader - ability to create out of nothing + create your own structure for the department` | Qualities block, visible body ~80,000 |

Verification method: the captured body was decoded UTF-8 and each span above confirmed present as a
verbatim substring (page-grain presence). The role count was confirmed by a single occurrence of
`(Full Time)` / `Job Overview` in the visible page-body region (offsets ≥75,000), with only the site
footer following the listing — i.e. exactly **one** visible role on the snapshot. (The earlier
duplicate occurrences of the role text at offsets ~4,571–6,354 are the page's `<title>`, `meta
description`, Open Graph, and Twitter-card tags echoing the same single listing, not additional roles.)

## E1 / E2 / E3 — case-stated construction premises (facilitator-asserted, honestly labeled)

The brand identity (E1), the launch date / channel state (E2), and the retail-expansion opportunity
framing (E3) are **not archive-sourced** in this case. They are **case-stated construction premises** —
real-in-the-world pre-cutoff facts, asserted facilitator-side as the scenario's ground truth per the
packet's `permitted_assumptions` ("Treat the founding, launch, product line, and channel facts in the
evidence as real"). They are **not** dressed up as captured evidence: no `SourceCapturePacket` backs
them, their `source_manifest` entries carry `case_type case_stated_premise` with
`not_applicable_case_stated_premise` sentinels for `retrieval_timestamp`/`hash`, and this note records
the limitation so the freeze does not encode a false sourcing claim. The contestant-visible
`source_manifest` is kept neutral (it asserts these as case premises, not as captured artifacts).

## E4 / E5 — general base rates (asserted priors)

Not retrieved documents. `source_type: general_base_rate` — standing analytic priors, true at and before
the cutoff by construction; `retrieval_timestamp` and `hash` carry the sentinel
`not_applicable_base_rate`.

## Org-motion is the only arm delta

Baseline and augmented packets are **identical** except that the augmented packet adds the org-motion
arm: the `E6` manifest entry plus the "Organizational Motion Signal" prose block carrying the captured
Supply Chain Manager listing as raw facts. No other evidence unit, framing, option set, or uncertainty
differs between the two arms. Per the anti-steering rule, the org-motion signal is presented as raw facts
(the single role, its function, its single-snapshot timing, its stated responsibilities) and never as an
editorialized reading of intent or confidence; the thinness (n=1 snapshot, 1 role, no earlier baseline)
travels with the signal in the packet.

## Non-claims

Not validation, not readiness, not a band input, not contestant-visible, not a scoring-key change. The
org-motion evidence is a feasibility/repeatability capture at product-learning tier, N=1. JSG-01 posture
unchanged (ECR derives integrity context; binds no `EvidenceUnit`). The post-cutoff outcome is not stated
or referenced anywhere in this record.
