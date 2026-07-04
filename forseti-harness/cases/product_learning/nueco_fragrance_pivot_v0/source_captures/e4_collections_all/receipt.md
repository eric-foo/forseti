# Source Capture Packet Receipt

- Packet ID: `01KV5TDSMD87K6HWXY2JDNFV7H`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TDSMDWDCS9S368B30M3HB`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:19:33Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20191117093415.

## Requested Context

- Decision question: Backtest: in the supplements-led era before The Nue Co. pivoted to fragrance-first (fragrance grew from ~20% to ~65% of revenue), what did the pre-cutoff public site signal about the brand's product positioning?
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.thenueco.com/collections/all
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20191117093415
- Capture timing: 2026-06-15T14:19:33Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `bc5c5a25f576153bfb18f9f6dad7f719df1c4e8e0acf1f545a983597003bae46`, 2845 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `20c3e364e0fe6a040c2a17f70506fc7018051f83c95d2465125775b588f8240d`, 213104 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `e29bebd54d313f6ad917fe82bf2d47bb3e19f8e7423509798243d40decc35235`, 966 bytes)

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
