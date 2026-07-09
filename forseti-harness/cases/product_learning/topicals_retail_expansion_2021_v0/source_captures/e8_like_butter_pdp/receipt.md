# Source Capture Packet Receipt

- Packet ID: `01KV5QSNN9FPV5J9BM481SY228`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5QSNN9X1E7X7ZQABM229D4`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:33:36Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20210303090202.

## Requested Context

- Decision question: Topicals near-term distribution/growth (DTC -> national beauty retail) at <=2021-03-15 cutoff: buy-side demand-pressure signal (reviews/availability) from the Like Butter product page
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://mytopicals.com/collections/shop-all/products/like-butter
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20210303090202
- Capture timing: 2026-06-15T13:33:36Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `a4fb9e272d26b8b7ee11380e19dac9fb2967007b3e8aeabe55d464f3e2485e15`, 3193 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `ff2db40f4359009784388df6bdecf1a0d452bae31a2f456a5ee86690043497b2`, 243892 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `34645c618e1f19b91ce95340de31429233ff84d86fa953009af4d720def26414`, 1086 bytes)

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
