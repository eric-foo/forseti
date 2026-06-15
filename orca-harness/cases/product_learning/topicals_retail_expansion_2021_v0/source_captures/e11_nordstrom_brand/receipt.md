# Source Capture Packet Receipt

- Packet ID: `01KV5RFVXNPD4S3454QY9ZF9E0`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RFVXNXXF8Q8Y3P7YBMFZ5`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:45:44Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20201109194021.

## Requested Context

- Decision question: Topicals retail-distribution decision <=2021-03-15: independent third-party retail-presence signal from Nordstrom
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://www.nordstrom.com/brands/topicals--21693
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20201109194021
- Capture timing: 2026-06-15T13:45:44Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `fa808374959843540ee277bd3600422879542de318a772affb69dd85d9b23f9d`, 1901 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `8a03c41ad0ae268bd431eabee82614214649e6f9aa868c3f8c99d11713db07a0`, 149390 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `b787f88d689ebc684a949d3ad4356b3397d0e0d4e1a2f796e672210599777f6f`, 1006 bytes)

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
