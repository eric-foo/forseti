# Source Capture Packet Receipt

- Packet ID: `01KV5RRCQM9YCHB6GC8P6M5FWF`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RRCQMFAJEJW2RNCYEMEQ2`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:50:23Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240415133415.

## Requested Context

- Decision question: Backtest: just before Joah Beauty's mid-2024 line-kill (CVS-exclusive K-beauty line wound down; socials wiped after June 2024), did its pre-cutoff public site signal the wind-down trajectory? (known later outcome: April 2025 closure + liquidation)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.joahbeauty.com/pages/bundles
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240415133415
- Capture timing: 2026-06-15T13:50:23Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `05a8c4e2204736e97c83c05698e9830b9ca2990a39e805c2e2091244f0dd991a`, 1837 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `9d1f102775a340da9b9a64bba786bacd57ec76a5a279231e89c49ab7b236438c`, 172136 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `1f168e2ede85a21b713b298d7f970128e65337f3e07c2c0e650634ba854a4276`, 966 bytes)

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
