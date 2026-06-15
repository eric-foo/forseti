# Source Capture Packet Receipt

- Packet ID: `01KV5RMT1HZM0JA581QKTZWDTN`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RMT1HGHTB766ENP55JWC7`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:48:26Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250522221905.

## Requested Context

- Decision question: Backtest: at the ~June 2025 tariff-pressure pricing decision, did cocokind's pre-cutoff public prices/positioning signal whether holding price would stick? (known later outcome: price HELD through 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://cocokind.com/products/beginner-retinol-gel
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250522221905
- Capture timing: 2026-06-15T13:48:26Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `f68867c8505600824031fd434911f19d7b3739b7f99b7fe250928cf4251688bd`, 5211 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `78bb8600542f97899b132f3be713ccb0ea05592375662d48c0dca7413a772eb2`, 416943 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `b9f28dba0c2fe3f08fc396c4fd0076625c10e3a7bfc744c88d0cb17eca05d37d`, 1032 bytes)

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
