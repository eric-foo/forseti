# Source Capture Packet Receipt

- Packet ID: `01KV5TFGKKAHCKA1GDGJGKQ1MW`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TFGKK3QM8HVFAK0SK9WMF`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:20:29Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20191117120927.

## Requested Context

- Decision question: Backtest: in the supplements-led era before The Nue Co. pivoted to fragrance-first (fragrance grew from ~20% to ~65% of revenue), what did the pre-cutoff public site signal about the brand's product positioning?
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.thenueco.com/collections/best-sellers
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20191117120927
- Capture timing: 2026-06-15T14:20:29Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `68aeba2f267b7f9350fba06d88c5540030ae0039794549943bbf394acc33dd0e`, 2263 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `abc8d24811b108f055fba0c9fc2cf9098d524cde87b5d565a0b66bea8de064eb`, 237739 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `eb29de726fee4e697ec41409e96080b6b996e8d2d5c4e21e5a4f1a9f191483c4`, 1011 bytes)

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
