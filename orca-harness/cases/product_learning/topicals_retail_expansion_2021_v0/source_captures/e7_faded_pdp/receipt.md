# Source Capture Packet Receipt

- Packet ID: `01KV5QBAE86F1QVWSNK8ECSK3X`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5QBAE8MBEZZBXP1J2BQ1WW`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:25:46Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20210210010815.

## Requested Context

- Decision question: Topicals near-term distribution/growth (DTC -> national beauty retail) at <=2021-03-15 cutoff: buy-side demand-pressure signal (reviews/availability) from the Faded product page
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://mytopicals.com/collections/shop-all/products/faded
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20210210010815
- Capture timing: 2026-06-15T13:25:46Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `7c2c28398344b044ef053f3f887d75c91081cf7545d8afc8d88b945efd9d3945`, 1993 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `49b3ecabd81a5052e15febd87270d19d7775e1179b81ebea3ba79459ded32154`, 242414 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `5a42ae0b9c149ab603d679e6ffc159069ad38ccc82075bda0577e0ea1726f1ef`, 1056 bytes)

## Warnings

- none

## Limitations

- none

## Non-Claims

- not archive completeness proof
- not source-state truth proof
- not browser automation
- not API SDK use
- not Archive.org package use
- not HTML meaning extraction
- not OCR or image analysis
- not scraper framework use
- not proxy or session injection
- not ECR design
- not Cleaning implementation
- not Judgment scoring
- not buyer proof
- not commercial-readiness logic
