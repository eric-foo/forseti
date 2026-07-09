# Source Capture Packet Receipt

- Packet ID: `01KV5RFAF12FG9N1KWBEER92AM`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RFAF1H1GRTSP9BT6JM27Z`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:45:26Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250428084930.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff store-locator (retail-door footprint) signal the retail-vs-DTC trajectory? (known later outcome: retreat from ~1,000 CVS + ~250 Target doors, DTC pivot)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/pages/store-locator
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250428084930
- Capture timing: 2026-06-15T13:45:26Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `9c1ac4f6e597a723c62ed97f5545a94cc52ef32c82fc3c255f8aeb89b51ddd97`, 4278 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `3386964f56292300754dc335cb522af6eabdf64464e74c2835b493393991acd5`, 254248 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `9c475eaa4ad2eabd7e4049c50b89e03516d776d69627c87e43382423a38e92a9`, 986 bytes)

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
