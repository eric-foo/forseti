# Source Capture Packet Receipt

- Packet ID: `01KV5QYC20HJ4XSWZGH64546MY`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5QYC20NYEYCXXPQHJ3EZN2`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:36:10Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20210303081931.

## Requested Context

- Decision question: Topicals near-term distribution/growth (DTC -> national beauty retail) at <=2021-03-15 cutoff: wind-caller signal (which skin-influencers the brand associates with pre-cutoff)
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://mytopicals.com/blogs/skindex/top-skininfluencers-post-1
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20210303081931
- Capture timing: 2026-06-15T13:36:10Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `35f1042d3f175fb35e1a2abc4766b034b2855a5c29fe602cfee13e6b8abae607`, 2027 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `d2c5605995bc898bce3ade75849ff81438d75eac4d488db8ba2c805ec7df4471`, 132761 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `2e4a6bc190c1020d08f3f817b54903bfcb7c280d2b8479a9f9bd415217554364`, 1081 bytes)

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
