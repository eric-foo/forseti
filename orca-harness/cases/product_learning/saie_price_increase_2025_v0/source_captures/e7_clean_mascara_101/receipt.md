# Source Capture Packet Receipt

- Packet ID: `01KV5RZWH3CPM5AJMEY0RR6NRJ`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RZWH37A1H4TGZH8H6ZA4T`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:54:29Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250428050840.

## Requested Context

- Decision question: Backtest: at the ~June 2025 pricing decision, did Saie's pre-cutoff public prices/positioning signal whether a +$1-4 increase would stick? (known later outcome: increase PERSISTED into 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://saiehello.com/products/clean-mascara-101
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250428050840
- Capture timing: 2026-06-15T13:54:29Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `ff14f91e1ceca8d5c53a6aa3ee44a8722f58172d199aed9955b159e1d4b5277d`, 5072 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `e088d95c1c9cfcaddd3c93670b77e19533485987e3a04c8cd3b581dd733bb001`, 1092995 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `ce7a7e84a2670a3bd5bad8a5b1e8a414b08bdbcf30533bc481cc529152b58c11`, 1008 bytes)

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
