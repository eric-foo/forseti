# Source Capture Packet Receipt

- Packet ID: `01KV5RM1CYDDNTEC9BEFK1H70C`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RM1CY7PDJYA9ZFT0EEXH0`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:48:00Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250522005448.

## Requested Context

- Decision question: Backtest: at the ~June 2025 pricing decision, did Saie's pre-cutoff public prices/positioning signal whether a +$1-4 increase would stick? (known later outcome: increase PERSISTED into 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://saiehello.com/collections/bestsellers
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250522005448
- Capture timing: 2026-06-15T13:48:00Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `faf78a344992ee77c4001b0096eefd1c3e01d24522da8dceeffd99b21108afd4`, 4993 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `b2db2d0c68dfd29fc835d76d2623983a58b3d3b9124c945e2a44fa1e98e2d6f3`, 3524557 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `955e3fbbd15a9fee15d8886b85cc54e1798a2bc7072a7a715f92b92354426efd`, 992 bytes)

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
