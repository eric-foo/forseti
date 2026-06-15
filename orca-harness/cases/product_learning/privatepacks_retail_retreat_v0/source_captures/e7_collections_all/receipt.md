# Source Capture Packet Receipt

- Packet ID: `01KV5RJ6Y071TK39ZQ2A0B26BK`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RJ6Y017K5K8NK1KM9K6WH`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:47:00Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250219205138.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff full catalog signal the retail-vs-DTC trajectory? (known later outcome: retail retreat + DTC pivot)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/collections/all
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250219205138
- Capture timing: 2026-06-15T13:47:00Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `3e7dea4db91438607e41009519fb24c805fd983c0adf051fba7e843f8e7bd8a8`, 3517 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `0bd2893d7e3a4772ebf87ccc778ba88b9b71464063ebb9d6316e1a0d76364847`, 260578 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `61a766df80ee75e9049a06009badaba577eab5bd5c533673eb75139137833e70`, 966 bytes)

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
