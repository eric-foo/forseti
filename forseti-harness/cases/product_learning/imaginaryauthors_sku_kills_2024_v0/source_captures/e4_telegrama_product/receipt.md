# Source Capture Packet Receipt

- Packet ID: `01KV5TKYBMGVN3WHCP5097K514`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TKYBM7VE35VE9RJ1WF4KC`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:22:54Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20240304233916.

## Requested Context

- Decision question: Backtest: at the ~Aug 2024 SKU-kill decision, did Imaginary Authors' pre-cutoff public site show Whispered Myths + Telegrama as live products? (known later outcome: both quietly discontinued Aug 2024, low-sales rationale)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://imaginaryauthors.com/products/telegrama
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20240304233916
- Capture timing: 2026-06-15T14:22:54Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `9fc7fdfd3ff7ad38b49f753390d36bebc757c14bb276362d9bc093295f27666a`, 5045 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `87513690b4c4ade71779f54a5bbb1dc0519404052f8871ae06b516f68bd5ee88`, 170274 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `c55b772f4ef5abad1e609ad0d7acf0e8519aee32296d29e7467a5b7af3a5fcf7`, 1001 bytes)

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
