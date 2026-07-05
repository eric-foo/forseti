# Source Capture Packet Receipt

- Packet ID: `01KV5T5V98R33CXAEA8643N8W3`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5T5V98BW1XMT2DH6ZB0HJM`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:15:12Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20230127114711.

## Requested Context

- Decision question: Backtest: at the Feb 2023 Target repricing entry, did Selfless by Hyram's pre-cutoff DTC site signal the mass-retail channel shift? (known later outcome: Target exit Apr 2025)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://us.selflessbyhyram.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20230127114711
- Capture timing: 2026-06-15T14:15:12Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `3eb0475fc710468d1f47101c637e7c47f28699ef691de1a29a5f5784c5b06c4e`, 4623 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `42a754dbc28b921408b9815e5c18c6dea89a5db33369372b0eca8abb463c4d77`, 251307 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `b3c8daeacc79f701c20a459519f96390cd60fa8c34a49e0883780afdf4f6f624`, 921 bytes)

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
