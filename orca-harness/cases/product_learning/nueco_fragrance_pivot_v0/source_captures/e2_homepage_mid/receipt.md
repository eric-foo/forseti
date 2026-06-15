# Source Capture Packet Receipt

- Packet ID: `01KV5TBZYZ7HV37PTZHDQCWWP8`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TBZYZ9JX2BHJ9Q4NZ5ZSD`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:18:34Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20190626095434.

## Requested Context

- Decision question: Backtest: in the supplements-led era before The Nue Co. pivoted to fragrance-first (fragrance grew from ~20% to ~65% of revenue), what did the pre-cutoff public site signal about the brand's product positioning?
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.thenueco.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20190626095434
- Capture timing: 2026-06-15T14:18:34Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `4a55544c550ada6d615cda06b4c558ea8dab18d4a8ca8e36a6190dd4e9d0db1b`, 4448 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `872af5a24398ec2a4222c51a6034c7f2ce0e42282da2d92bb0554cab1a3d67da`, 109559 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `e66d0257bf5812040b9e7dbc0fd7523bd4acb2a1498f02176124a58225998fcf`, 891 bytes)

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
