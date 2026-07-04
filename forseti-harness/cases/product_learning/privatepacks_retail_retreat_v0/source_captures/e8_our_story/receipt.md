# Source Capture Packet Receipt

- Packet ID: `01KV5RKV42N4VK3Z8QP5Q9G9S0`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RKV42MBGYW343FH3YE0P5`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:47:54Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250219222920.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff brand/about page signal the retail-vs-DTC trajectory? (known later outcome: retail retreat + DTC pivot)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/pages/our-story-2023
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250219222920
- Capture timing: 2026-06-15T13:47:54Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `cb556e4baf3355dac9bdb63d39f72b9ba920109b3bb683bcc7e8f8db45f006c5`, 3261 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `644b2fa1a7a0c3c6e9256e01d23850b404078ecc3d65fd86a5b19ddff0e7410f`, 243114 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `813b322afe9189098dde1f5b587b6bef0bee949ed54c6d1683b040dfcae40582`, 991 bytes)

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
