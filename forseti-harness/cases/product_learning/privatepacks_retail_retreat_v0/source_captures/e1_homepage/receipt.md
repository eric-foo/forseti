# Source Capture Packet Receipt

- Packet ID: `01KV5RAQJR4A86C52V3TZNETQY`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RAQJR1DXJ43W97J8RX9VV`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:42:55Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250428091259.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff public site signal the retail-vs-DTC trajectory (CVS ~1,000 + Target ~250 doors, velocity miss)? (known later outcome: retail retreat + DTC pivot, ~$100K retail infra written off)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250428091259
- Capture timing: 2026-06-15T13:42:55Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `6502b68aca7a5721c56ea24be264080c15667c9d0b6cada6993eff43f0b0ba64`, 4463 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `f12b75412f7576e6d3529e8ce04606b0d2da65a1659494683a3eefbabd0947b1`, 263306 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `c2955fb0fd96e71c7c12883f714be571490d35077cb98683ed65ba60c65f2d65`, 891 bytes)

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
