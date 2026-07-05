# Source Capture Packet Receipt

- Packet ID: `01KV5RQ8W2WNKP0Y67HZ8DFZR9`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RQ8W2KPPYTWDVWNJ4MEYV`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:49:46Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240415133307.

## Requested Context

- Decision question: Backtest: just before Joah Beauty's mid-2024 line-kill (CVS-exclusive K-beauty line wound down; socials wiped after June 2024), did its pre-cutoff public site signal the wind-down trajectory? (known later outcome: April 2025 closure + liquidation)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.joahbeauty.com/pages/joah-la-pop-up
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240415133307
- Capture timing: 2026-06-15T13:49:46Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `095f53025d2917279b03d4f5085216d9236a1cafe2e7a6f08f2a27ef47e824ce`, 1893 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `c8d4d2947846eea909dd1f2431d064ce1b94d9de8ac3aaf1b821230056cb4489`, 158160 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `8e9090f108f5cb33c891b7603561548c31b513e66720536fcdbc1e0719d984f6`, 1001 bytes)

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
