# Source Capture Packet Receipt

- Packet ID: `01KV5RR15ZKN8J8JPW52WZ2WAM`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RR15ZK6KRSR7GA5BNT3Z0`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:50:11Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250428095103.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff how-it-works (product mechanics) page signal the retail-vs-DTC trajectory? (known later outcome: retail retreat + DTC pivot)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/pages/how-it-works-2023
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250428095103
- Capture timing: 2026-06-15T13:50:11Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `792a688a89c426915ca6caa64d7341498b41ea9e7962000f8996012d815dc338`, 3309 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `e5df8ca7b3faaf8e10fb50833dad30389e9931d643b5ea8ab340ebf65745f859`, 276320 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `9108483a5e57e7594c6c2f5bc1ac127eb8e1104c5e6f346be07cda05e5eb6707`, 1006 bytes)

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
