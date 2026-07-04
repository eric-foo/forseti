# Source Capture Packet Receipt

- Packet ID: `01KV5RE06G9KW3ZPMK4QYK4BFQ`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RE06GQYAE7S5R9E8Y71JJ`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:44:42Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240520131758.

## Requested Context

- Decision question: Backtest: just before Joah Beauty's mid-2024 line-kill (CVS-exclusive K-beauty line wound down; socials wiped after June 2024), did its pre-cutoff public site signal the wind-down trajectory? (known later outcome: April 2025 closure + liquidation)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.joahbeauty.com/collections
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240520131758
- Capture timing: 2026-06-15T13:44:42Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `3ae096d5450d05871f021287ea96ec7372a6164958d33b8ef803f6ebac6a3f89`, 2147 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `49336b3820f7cd430f42a140b9e70fb94088869bc0a615b3cb34dcb720b6c6ae`, 339494 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `584fea7e4089a3e1118f3bae4e8c01fec57eb5a6d61f8c8771ecd753f84a4d21`, 956 bytes)

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
