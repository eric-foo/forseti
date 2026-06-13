# Source Capture Packet Receipt

- Packet ID: `01KTZY021ESR87PW3FDFQ4YCK0`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KTZY021EW3EMQ31JJ2J1QDSM`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-13T07:26:30Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20230225210430.

## Requested Context

- Decision question: Beauty Pie membership model + pricing structure, pre-2023-02-28 cutoff (E1/E2 provenance)
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://www.beautypie.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20230225210430
- Capture timing: 2026-06-13T07:26:30Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `24d2dc900f4a3e6fd00d86f9197e43156ba4f27a5c7365ed075ce6304fc77591`, 4447 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `1dad75a206688f81309e71af41f4f4c7576f30e1b9760cc7e29627cd0c03745d`, 391937 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `36196fe891e253b8ce7ba1deccf150187c7a86c5dc0dcc29ba97f17a9407bf53`, 877 bytes)

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
