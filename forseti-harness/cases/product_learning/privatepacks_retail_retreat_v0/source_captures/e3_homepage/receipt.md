# Source Capture Packet Receipt

- Packet ID: `01KV5RE7S193VM45525YNPJQ0T`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RE7S1KN7SQVRMCMZ92Q1V`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:44:50Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240522203854.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff public site signal the retail-vs-DTC trajectory (CVS ~1,000 + Target ~250 doors, velocity miss)? (known later outcome: retail retreat + DTC pivot, ~$100K retail infra written off)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240522203854
- Capture timing: 2026-06-15T13:44:50Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `a1cdb392a9164f84c2aa29c031708b2df368664f5275907e6d6b2237874e8604`, 4473 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `53f37f7d8d7400985b8eeeab45c86410e245decf79106875531771b52fd581aa`, 358264 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `043fa36dec44f540747c4bac113ace6be1f36d509548e8e9d610a3cc87485420`, 891 bytes)

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
