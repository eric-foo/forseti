# Source Capture Packet Receipt

- Packet ID: `01KV5R93C29BJPXKKX23Z95D3G`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5R93C21XGVKRHX776WWE7B`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:42:02Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20231214015359.

## Requested Context

- Decision question: Backtest: just before Joah Beauty's mid-2024 line-kill (CVS-exclusive K-beauty line wound down; socials wiped after June 2024), did its pre-cutoff public site signal the wind-down trajectory? (known later outcome: April 2025 closure + liquidation)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.joahbeauty.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20231214015359
- Capture timing: 2026-06-15T13:42:02Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `0d536ee09a7c063e4d83e3bc610ded6a26a45a71de34a0c16e0e0dd769402929`, 4514 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `90736cf88dc09ced4f9ac1b75dcf4c6f47f219892f047ca6008bb8c5f2c49211`, 400329 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `fd162266bd83ca0eb53a3357f83789ff97fa62c61bb5f2438f7addf93f292935`, 901 bytes)

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
