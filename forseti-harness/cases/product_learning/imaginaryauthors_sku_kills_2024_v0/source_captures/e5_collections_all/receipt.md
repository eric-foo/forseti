# Source Capture Packet Receipt

- Packet ID: `01KV5TQNXZPNA25SB2A95DW69Q`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TQNXZMFF08VBDZ8MH29Q2`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:24:57Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240324132249.

## Requested Context

- Decision question: Backtest: at the ~Aug 2024 SKU-kill decision, did Imaginary Authors' pre-cutoff public site show Whispered Myths + Telegrama as live products? (known later outcome: both quietly discontinued Aug 2024, low-sales rationale)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://imaginaryauthors.com/collections/all
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240324132249
- Capture timing: 2026-06-15T14:24:57Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `16cd9fca930a99ea17ca5d4dde1bf074a9083b7af9eda2540b4e37c78d454965`, 3933 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `cc135d032817de46c45953a4e706c0d4109e689405da4b7affcb15c7c48c3657`, 279547 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `414c7de2c1e64dda1f8ac5843981dd86be08b931f2c15aae9317e13b01269442`, 986 bytes)

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
