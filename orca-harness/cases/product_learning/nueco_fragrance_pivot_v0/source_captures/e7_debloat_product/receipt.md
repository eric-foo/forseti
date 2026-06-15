# Source Capture Packet Receipt

- Packet ID: `01KV5TP016XD6SCNBD4W8MR6FG`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TP016DECJVMFB7B9Q5PY4`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:24:02Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20191219074139.

## Requested Context

- Decision question: Backtest: in the supplements-led era before The Nue Co. pivoted to fragrance-first (fragrance grew from ~20% to ~65% of revenue), what did the pre-cutoff public site signal about the brand's product positioning?
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.thenueco.com/collections/all/products/debloat-food-prebiotic-1
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20191219074139
- Capture timing: 2026-06-15T14:24:02Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `5953ecbbe11950da9a2677510353adc16390eb6980d692200d83b1966f3027f7`, 2121 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `3c6dcc777557884808dc4e20999979b1a778875c17ed069629458083c01a4ffd`, 155577 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `eaa813d6a19ad5966734bbb491b291a7d9f55197d97046814ed69a2853c11b85`, 1136 bytes)

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
