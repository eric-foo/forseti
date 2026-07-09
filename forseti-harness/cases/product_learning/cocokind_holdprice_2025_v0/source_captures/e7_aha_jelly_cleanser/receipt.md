# Source Capture Packet Receipt

- Packet ID: `01KV5RK996Z5X23ZZENWKA0S1M`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RK996DZ4FNA9XP0GBFKBJ`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:47:36Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250418123906.

## Requested Context

- Decision question: Backtest: at the ~June 2025 tariff-pressure pricing decision, did cocokind's pre-cutoff public prices/positioning signal whether holding price would stick? (known later outcome: price HELD through 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://cocokind.com/products/aha-jelly-cleanser
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250418123906
- Capture timing: 2026-06-15T13:47:36Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `e32dea6d811b1955179163e61586e250808c84947a749657e892a99ce8da8952`, 5159 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `7a3e1a9e3b929c4b6cb944865d70f2629d2250a7e08aafce95816df993373d10`, 380727 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `bc2e37c70f89d417d7aa052c1da2729b3f93381e45996d7430dc75af34e35216`, 1022 bytes)

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
