# Source Capture Packet Receipt

- Packet ID: `01KV5REKE0K6PDTXVX75TQ696P`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5REKE07WH9XG1G6J4X57AD`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:45:02Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250523181013.

## Requested Context

- Decision question: Backtest: at the ~June 2025 tariff-pressure pricing decision, did cocokind's pre-cutoff public prices/positioning signal whether holding price would stick? (known later outcome: price HELD through 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://cocokind.com/collections/bestsellers
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250523181013
- Capture timing: 2026-06-15T13:45:02Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `87856d425026eaa329442fbda28ed8d9f6e9a14f76a97c950a1aec81f88e1d47`, 5055 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `11bbd8fd41d3a2906ee114cd4813bcdc269db7ff2b34ba26634ba570c846a966`, 489734 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `9e9b81fb098842f3b7f2635c98ed73e4bd9e2aba9b5a1dcc8e068df5ff4ce5f2`, 1002 bytes)

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
