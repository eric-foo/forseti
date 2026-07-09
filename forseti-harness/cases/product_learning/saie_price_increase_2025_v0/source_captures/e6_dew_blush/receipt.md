# Source Capture Packet Receipt

- Packet ID: `01KV5RMQJH4ES2PK1EAS6KF2X5`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RMQJH8J12VPEQK49QWAWW`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:48:23Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250514080038.

## Requested Context

- Decision question: Backtest: at the ~June 2025 pricing decision, did Saie's pre-cutoff public prices/positioning signal whether a +$1-4 increase would stick? (known later outcome: increase PERSISTED into 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://saiehello.com/products/dew-blush
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250514080038
- Capture timing: 2026-06-15T13:48:23Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `6161e6b8432cf1fda861c5abffb103b2ed8a7d03d90cb02cb34135cef14f60b6`, 4863 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `3483537934e342f60293f3db2457391ddc8492b0417257616c166843896d21af`, 1230136 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `7b95e5ccb3017f3595e8accf35a2494df9431a7ba95ad394e30a36306e59dab0`, 967 bytes)

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
