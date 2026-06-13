# Source Capture Packet Receipt

- Packet ID: `01KTZY6FF77Q27RWN806CGPK3R`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KTZY6FF7ZGNYK5SEZZZDC70A`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-13T07:30:01Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20221201032019.

## Requested Context

- Decision question: Beauty Pie membership tier structure (£5/£10 monthly, £59 annual, spending limits), pre-2023-02-28 cutoff (E2 provenance)
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://www.beautypie.com/how-it-works
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20221201032019
- Capture timing: 2026-06-13T07:30:01Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `0cb12d61745ca52236d97bf7726700744aacf43ec9f08840db477ac02d11890b`, 4139 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `07aab0838c202da050881c51407f0144dfccfb694cc811f51be87aca415ef425`, 227843 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `97dbeee2048bf312e3d991ec3f4c55564e94dca5111f1c896011ba417089ec76`, 956 bytes)

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
