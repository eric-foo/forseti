# Source Capture Packet Receipt

- Packet ID: `01KV5QVKXMN5GCHRBPT9TSNERA`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5QVKXM43C8DJC67ND3ZT1B`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T13:34:40Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20210303074312.

## Requested Context

- Decision question: Topicals near-term distribution/growth (DTC -> national beauty retail) at <=2021-03-15 cutoff: wind-caller / press-coverage signal (which independent outlets covered Topicals pre-cutoff)
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://mytopicals.com/blogs/press
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20210303074312
- Capture timing: 2026-06-15T13:34:40Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `7c50768fbea6628bd7423f7080f9814b6e6a83e4f58850c82bd36597e313f960`, 1789 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `02664e7f037153bc9be6b4e9457be9989c6e7a74a0149b43e44cb6cb7e42cb5c`, 128478 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `6215ae5c0808378d870e4758aa4dcfbc034ffd1dd16b9229a688dde3368cfb88`, 936 bytes)

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
