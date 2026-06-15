# Source Capture Packet Receipt

- Packet ID: `01KV5RP7EHM3W7J9Z55K1PKTGQ`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RP7EH6KM2T0N7P3TZT4SS`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:49:12Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250501155815.

## Requested Context

- Decision question: Backtest: at the ~June 2025 tariff-pressure pricing decision, did cocokind's pre-cutoff public prices/positioning signal whether holding price would stick? (known later outcome: price HELD through 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://cocokind.com/products/ceramide-lip-blur-balm
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250501155815
- Capture timing: 2026-06-15T13:49:12Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `47cfcaa2d8ee0dc22784b1197427ec8e5a1ef484b1a411f21151acc7c8e94e0c`, 3789 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `a07288ceab2c13da358604bdd212893b2f6c18ad8b075bfda82fc19d23ae11bd`, 940189 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `9ad07aab52fc858d8412459bb7606005c31d832bf50380ab9a7e29ccf4b6f0ab`, 1042 bytes)

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
