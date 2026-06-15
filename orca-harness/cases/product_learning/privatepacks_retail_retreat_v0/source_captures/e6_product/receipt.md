# Source Capture Packet Receipt

- Packet ID: `01KV5RHHT5HVMZDWPTCJWJNGYB`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RHHT5W03PPEQ6FNJB2P0Z`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:46:39Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250316035548.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff core product page signal the retail-vs-DTC trajectory (the velocity-miss unit)? (known later outcome: retail retreat + DTC pivot)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/products/private-packs
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250316035548
- Capture timing: 2026-06-15T13:46:39Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `4763f5937e710809f3f39baee5757ac3c8028ea9f40645c4221e84faffe3dfe2`, 5047 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `2597a9919e067fd9e299f32479af0e61fef74dc95e6b69505add2e4c0c3033fd`, 417872 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `e003d14e3423c40a096caca3b9ef7da753b8e36950224a559213284b5a0dbfaf`, 1001 bytes)

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
