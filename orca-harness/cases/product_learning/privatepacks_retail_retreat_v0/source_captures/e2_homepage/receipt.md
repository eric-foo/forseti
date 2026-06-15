# Source Capture Packet Receipt

- Packet ID: `01KV5RBYY3N9NC095C59PY8B0E`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RBYY3NGZS8AZSEENYRK74`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:43:36Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240816063059.

## Requested Context

- Decision question: Backtest: at the ~2025 retail-retreat/DTC-pivot decision, did Private Packs' pre-cutoff public site signal the retail-vs-DTC trajectory (CVS ~1,000 + Target ~250 doors, velocity miss)? (known later outcome: retail retreat + DTC pivot, ~$100K retail infra written off)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://privatepacks.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240816063059
- Capture timing: 2026-06-15T13:43:36Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `34064f051cb6b1ce0c294ae8a88ff171a33c2be1433dd7805f33c34103720865`, 4473 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `a5c3fb522bae5094bad01969a15130cae8b2b09d18b9c7f84ab75abbe0d580cf`, 363904 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `2f301af11716241ef357e7213efdf1b5103bbfc3391d679d0fc39a4d01e16a21`, 888 bytes)

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
