# Source Capture Packet Receipt

- Packet ID: `01KTZY2VQBWMGJ0K7QDH5BR8T6`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KTZY2VQBWR5ZPT71G2EEET8G`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-13T07:28:02Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20230216220653.

## Requested Context

- Decision question: UK cost-of-living / elevated inflation early 2023 (E3 macro context), pre-2023-02-28 cutoff
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/january2023
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20230216220653
- Capture timing: 2026-06-13T07:28:02Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `2437e24283a9efa1f2064f0769bd53d7ce79a61462e53045fba44b10ea009d5b`, 6441 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `cd358676ff1ece94a31d1af771e57f29d3997928d75683a2ae5243664af5f3fe`, 143017 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `6e758e86fe5906dcfe00d60db8e2ac19f4b011880f4230e26f8e902e12a1077d`, 1265 bytes)

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
