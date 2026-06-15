# Source Capture Packet Receipt

- Packet ID: `01KV5TB3JEMP795CYXVPJ3PGC8`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TB3JE2WRHZ8TFM5HEFSFW`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:18:05Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20191221003425.

## Requested Context

- Decision question: Backtest: in the supplements-led era before The Nue Co. pivoted to fragrance-first (fragrance grew from ~20% to ~65% of revenue), what did the pre-cutoff public site signal about the brand's product positioning?
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.thenueco.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20191221003425
- Capture timing: 2026-06-15T14:18:05Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `57b1d8e1b6262217b98c0ba772b452aff423fcf0088ba1adb3527a3983d72706`, 4449 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `7a6204b583312a71488aaf397b4706079fbcec70cae5475a430d3093129174ec`, 153406 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `43677bbf49ea42f2242d0be6a6355828a126e708bcb44cfa7f2d7b3637341ff3`, 885 bytes)

## Warnings

- direct_http followed redirect from https://web.archive.org/web/20191221003425/http://thenueco.com:80/ to https://web.archive.org/web/20191214045845/https://www.thenueco.com/

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
