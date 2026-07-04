# Source Capture Packet Receipt

- Packet ID: `01KV5R6FE4E5W93EYV8X72TDSH`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5R6FE4YXR04F2D6981P8PW`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:40:36Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240520112307.

## Requested Context

- Decision question: Backtest: just before Joah Beauty's mid-2024 line-kill (CVS-exclusive K-beauty line wound down; socials wiped after June 2024), did its pre-cutoff public site signal the wind-down trajectory? (known later outcome: April 2025 closure + liquidation)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.joahbeauty.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240520112307
- Capture timing: 2026-06-15T13:40:36Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `0863e29ac2afd83e27108b3729b693b58c7b2405404dfb2a179f13b31186f208`, 4509 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `ae32bab28a9af24c7eeea4f79df49465a91b167b6224877d2f6917d0118954f6`, 421060 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `140ac68dbd744c2fe1d759d60cee4c5951da566c1a74e7764c9a2718fb05e58d`, 901 bytes)

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
