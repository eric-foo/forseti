# Source Capture Packet Receipt

- Packet ID: `01KV0H0VC8K2T0Y4HA79KEW1R9`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `greenhouse_ats_board`
- Source surface: `greenhouse_public_jobs_board`
- Session identity: `01KV0H0VC8SN9J5SQA15CN56T8`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-13T12:58:59Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20220123234700.

## Requested Context

- Decision question: At the 2023-02-28 cutoff, how aggressively should Beauty Pie restructure membership pricing (eliminate GBP5/mo entry tier, double to GBP10/mo, scrap monthly spending limits)?
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://boards.eu.greenhouse.io/beautypie
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20220123234700
- Capture timing: 2026-06-13T12:58:59Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `c261abf8f9b8ce344e30e3fa02d572abe3739f21012615ea57751ebcea983c96`, 1839 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `096e5f113658bbb344b310a37216d46eac17af589467afcabc8a1533c864c7ef`, 14907 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `28efdfb88df58977e591ff8307c8f62ffe4f57a733808a93e5e6df959910956e`, 970 bytes)

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
