# Source Capture Packet Receipt

- Packet ID: `01KV5RJM22XJJ1S9W5GHRYDPJV`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RJM22NEGSSDEAPC97E6HJ`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:47:14Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250522232519.

## Requested Context

- Decision question: Backtest: at the ~June 2025 tariff-pressure pricing decision, did cocokind's pre-cutoff public prices/positioning signal whether holding price would stick? (known later outcome: price HELD through 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://cocokind.com/products/ceramide-barrier-serum
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250522232519
- Capture timing: 2026-06-15T13:47:14Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `a932877cd85fb31335a9001ee98ea6adca253a410b7d3830aa0bd6eba33bb5aa`, 5263 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `f74b527479d09854ae46d8a01678245ab195c870978608bc13a6ac0919ba8a9f`, 469144 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `89f3984676b6760dd7b31fd6dab4072edb8a5ea1a244e745cd1ab7f7495f61aa`, 1042 bytes)

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
