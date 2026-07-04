# Source Capture Packet Receipt

- Packet ID: `01KV5RGJYASADNBHFWWPAQCHV2`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RGJYA3R3CEW8EB0GVT0DJ`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:46:07Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250219222723.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff wholesale/retail-partner page signal the retail-vs-DTC trajectory? (known later outcome: retail retreat + DTC pivot)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/pages/wholesale
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250219222723
- Capture timing: 2026-06-15T13:46:07Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `ec16d9fd0458c9769d221ccf3a8b5378d4b03863db633740c37b3aab1ddca56c`, 2509 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `36bf14b2727337f92411b4319c193aa6c394dc12232b5577b1654c417831e03f`, 237178 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `a3b52e0271e562a469c837b01077bde381043df7e1caf32f79865bbd3955dbd0`, 966 bytes)

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
