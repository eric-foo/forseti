# CP0 — e.l.f. Bronzing Drops Understanding Replay Packet

```yaml
retrieval_header_version: 1
artifact_role: Review input
scope: Cumulative replay packet at the R0 boundary for the e.l.f. Bronzing Drops Understanding acquisition.
use_when:
  - Replaying only the evidence and receipts available at CP0.
  - Auditing the blocked cutoff-resolution boundary without later acquisition.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_elf_bronzing_drops_understanding_scan_receipt_v0.md
  - docs/workflows/forseti_beauty_elf_bronzing_drops_understanding_acquisition_seal_v0.md
```

## Boundary

- `cycle_id`: `elf_bronzing_drops_understanding_20260719`
- `commission_id`: `elf_bronzing_drops_understanding_csb_20260719`
- checkpoint: `CP0`
- atomic job: `R0`
- replay state: `BLOCKED_R0_TIMESTAMP_UNPROVED`
- source/access date: `2026-07-19`

This packet contains only observations and receipts available when R0 stopped.
It carries no R1-R6 evidence, future evidence, stopping-policy instruction, or
stopping recommendation.

## Included Observation IDs

- `OBS-001` — first-party Beauty Squad page content:
  `https://www.elfcosmetics.com/join-beautysquad-bronzing-drops`.
  Exact locator: “OUR MOST-WANTED DROP EVER IS COMING SOON,” followed by the
  statement that Beauty Squad members could be first to shop on `4/11 at 12PM
  EST/9AM PST`. Limitation: this is a shopping-access time, not a page
  publication timestamp.
- `OBS-002` — later first-party June 10, 2024 release:
  `https://investor.elfbeauty.com/stock-and-financial/press-releases/landing-news/2024/06-10-2024-050119999`.
  Exact locator: headline and paragraphs describing the community-request
  attribution, $12 price, three shades, and company/Target/Walmart channels.
  Limitation: later company evidence only; not the earliest announcement.

## Included Receipt IDs

- `ACCESS-001` — current source-specific direct-HTTP probe of the exact Beauty
  Squad URL returned HTTP 404 on `2026-07-19`.
- `EQ-001` / `M01` / `NEG-001` — one bounded canonical Wayback CDX query for
  the exact URL, limited to 2024 status-200 records, returned an empty response
  and no timestamp record.
- `ACCESS-002` — publisher time-zone wording preserved verbatim; no inferred
  daylight-saving correction or UTC conversion.

## Known Gaps

- `GAP-001`: no source-native or served-time-verified publication timestamp
  establishes the earliest first-party public launch announcement.
- The April shopping-access time cannot substitute for that timestamp.
- No cutoff is bound.
- No R1-R6 route was run.

## Route State At CP0

| Route | State | Receipt |
| --- | --- | --- |
| Exact first-party page, cached public content | `PARTIAL` | `OBS-001`, `ACCESS-001` |
| Exact-URL Wayback CDX discovery | `ZERO_YIELD_NOT_EXHAUSTION` | `EQ-001`, `M01`, `NEG-001` |
| Later first-party press release | `BOUNDED_LATER_EVIDENCE` | `OBS-002` |
| R1-R6 | `NOT_RUN_PREREQUISITE_BLOCKED` | `GAP-001` |

## CP0 Disposition

`INCONCLUSIVE_CAPTURE_BLOCKED`.

This packet does not establish an earliest announcement timestamp, cutoff,
acquisition closure, or material-contribution inference.
