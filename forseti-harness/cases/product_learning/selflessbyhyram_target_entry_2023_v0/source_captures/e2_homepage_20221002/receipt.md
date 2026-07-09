# Source Capture Packet Receipt

- Packet ID: `01KV5T6Q8DZ4ZH0YHBFH5SJ9ZX`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5T6Q8DSTJ0MP82RWKW5FY8`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:15:41Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20221006233301.

## Requested Context

- Decision question: Backtest: at the Feb 2023 Target repricing entry, did Selfless by Hyram's pre-cutoff DTC site signal the mass-retail channel shift? (known later outcome: Target exit Apr 2025)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://us.selflessbyhyram.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20221006233301
- Capture timing: 2026-06-15T14:15:41Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `d266933c13d2b2bdcb53cfc8be93df05e145a9d1535b1340b7b7ac7299dc5487`, 4621 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `f54f94f1d3318ad08d3af640ba7c0b7cfe2619473b1018bbf04e3a065516d5d2`, 255222 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `3fee0bb26254f97514456e241ccdc549adbddbac201a8dc852ad09df0b98d97d`, 921 bytes)

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
