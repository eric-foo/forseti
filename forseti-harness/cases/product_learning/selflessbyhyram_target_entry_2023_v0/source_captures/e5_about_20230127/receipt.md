# Source Capture Packet Receipt

- Packet ID: `01KV5TA4YEAM6J4AYBFR5ZBQMQ`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TA4YEB15RTBY5RF0SFTGA`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:17:33Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20230127104100.

## Requested Context

- Decision question: Backtest: at the Feb 2023 Target repricing entry, did Selfless by Hyram's pre-cutoff DTC site signal the mass-retail channel shift? (known later outcome: Target exit Apr 2025)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://us.selflessbyhyram.com/pages/about-us
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20230127104100
- Capture timing: 2026-06-15T14:17:33Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `83b8789a6ce38eb804c08c921a6df1a596318d2523c0933cb957e859bd53ec0f`, 4300 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `eacedc47cad0bcc6730ee95b650795c499091d97f745fa9bf62b74e99914dbe2`, 191661 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `a3d2fbc9336bd3ebffeebd6c8edad7dbe6388272bc5cb57ea29863a05d4ff371`, 991 bytes)

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
