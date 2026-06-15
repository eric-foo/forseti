# Source Capture Packet Receipt

- Packet ID: `01KV5R882K06FFC3DNFZTFD09K`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5R882KM0Y13V0NF62VNHFD`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:41:34Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250530192304.

## Requested Context

- Decision question: Backtest: at the ~June 2025 tariff-pressure pricing decision, did cocokind's pre-cutoff public prices/positioning signal whether holding price would stick? (known later outcome: price HELD through 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://cocokind.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250530192304
- Capture timing: 2026-06-15T13:41:34Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `fb5efabab08804a1d1871db2a1e8eccd94f7b1b109b7f09accdd64a55bb78a06`, 4451 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `22ab4e993b9ba4773fdae4d5540f06d60f65a999b2f0f8df7823ef9f3cd6420d`, 883383 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `fdea4f26f78161f5b4fc607addabe8bfe3e6cec40efb61c77bb7710b1dca28da`, 887 bytes)

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
