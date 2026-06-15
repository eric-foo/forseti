# Source Capture Packet Receipt

- Packet ID: `01KV5RY47RTRTGESKX9KM9G1H7`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RY47R7TZM7Y0AZFEPZ07T`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:53:31Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250428061256.

## Requested Context

- Decision question: Backtest: at the ~June 2025 pricing decision, did Saie's pre-cutoff public prices/positioning signal whether a +$1-4 increase would stick? (known later outcome: increase PERSISTED into 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://saiehello.com/collections/all
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250428061256
- Capture timing: 2026-06-15T13:53:31Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `87ed5ea31ae8e7b2c806e0bffff15d19f9b6c9299b3368b6bf036177523b2e64`, 4786 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `a47a3a8090626494fb4afc4804df27656a8d3282f1c9c31aef9c8987e18f5223`, 4125876 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `b3303b05c961bd25f316f436d9cd49f11a20eaac89417f461803bc0c2c407426`, 953 bytes)

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
