# Source Capture Packet Receipt

- Packet ID: `01KV2M7XPZENAJJ74H1QVWCW6E`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV2M7XPZEFZT9M4WCF0ECCY4`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-14T08:33:46Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20210303084505.

## Requested Context

- Decision question: Topicals hiring composition at <=2021-03 cutoff: org-motion signal for the DTC-to-nationwide-Sephora retail distribution decision
- Capture context: Archive.org availability/body source capture with Direct HTTP helper
- Source locator: https://mytopicals.com/pages/careers
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20210303084505
- Capture timing: 2026-06-14T08:33:46Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `0a8054bc334f6e3d65b3fc06ef9e6a9a218ebce81d84f5da109bca03ce3e9146`, 1805 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `db147fc02195e872957d588be376a935aee0fda584960dbd10d063912a0d981b`, 129094 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `7a66eb845f7b633ce4be6d35d0222e2b1f42d469763a2f5d5fc35886eb6b9529`, 946 bytes)

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
