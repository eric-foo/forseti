# Source Capture Packet Receipt

- Packet ID: `01KV5TE8GQHHJFSWH3JE7MDWNE`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TE8GQJSSMNQTGPMSWXHB8`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:19:48Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20230127110225.

## Requested Context

- Decision question: Backtest: at the Feb 2023 Target repricing entry, did Selfless by Hyram's pre-cutoff DTC site signal the mass-retail channel shift? (known later outcome: Target exit Apr 2025)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://us.selflessbyhyram.com/collections/eddies-routine
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20230127110225
- Capture timing: 2026-06-15T14:19:48Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `66401d068ea75fa8a7b0fcc8165142fabe3721d222b8b01cb2c72ea24d5eba6e`, 2713 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `88fbe0c51b3c39690e08c803aae4c988f68e4e65450b66eae3e0f8d971f15892`, 208107 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `1e7bc0375330aabe9b5b5c1f3a52ba1487cb8e216e350bde7ba91488d7143d62`, 1051 bytes)

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
