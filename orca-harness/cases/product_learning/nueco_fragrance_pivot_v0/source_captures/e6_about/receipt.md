# Source Capture Packet Receipt

- Packet ID: `01KV5TM9EWKMEC50KSX96WJ4VF`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TM9EWDG9GHN5CP4G5HMF0`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:23:06Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20190219231622.

## Requested Context

- Decision question: Backtest: in the supplements-led era before The Nue Co. pivoted to fragrance-first (fragrance grew from ~20% to ~65% of revenue), what did the pre-cutoff public site signal about the brand's product positioning?
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://www.thenueco.com/pages/about
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20190219231622
- Capture timing: 2026-06-15T14:23:06Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `f547b13fa60445534c5e56cbb46bd5be8ec98aa9adda07bc35eb38332a24f023`, 2133 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `d2bdc3133e9da336fefe774442289e24a743c698b734d92cf13a18ecd0a7dbec`, 108587 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `02410669e7207e08dc74dcf2b4822499618c4e7a69870ba6727dac4c6bbc24e8`, 946 bytes)

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
