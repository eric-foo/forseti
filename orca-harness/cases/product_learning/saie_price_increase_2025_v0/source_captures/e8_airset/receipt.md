# Source Capture Packet Receipt

- Packet ID: `01KV5RQMSD89005DAZVPSX6TW9`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5RQMSDCJ6FCX54TMQPWF3S`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:49:58Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20250428045316.

## Requested Context

- Decision question: Backtest: at the ~June 2025 pricing decision, did Saie's pre-cutoff public prices/positioning signal whether a +$1-4 increase would stick? (known later outcome: increase PERSISTED into 2026)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://saiehello.com/products/airset
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20250428045316
- Capture timing: 2026-06-15T13:49:58Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `37bbef42fdefefe169deec47707c4ca3a1f754f1c4d48991c7a3f688ebcbb1aa`, 4785 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `ddce3c3b4172705115d1aed52adb4ab3f9ebf7ca3b21c1de55fe8a7d56d24b0f`, 1005173 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `80651e312b43f3e24d7929f80136489a6c6ad16347367aad640c9cd50500f2c4`, 952 bytes)

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
