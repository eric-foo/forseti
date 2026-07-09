# Source Capture Packet Receipt

- Packet ID: `01KV5TA8D3HF3ASS14JT59T1TS`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `archive_org`
- Source surface: `archive_org_wayback`
- Session identity: `01KV5TA8D3K11N8SRK3DJ2PQ6E`
- Capture mode: `archive/history`
- Visible mode changes: none
- Operator category: `archive_org_cli_operator`
- Receipt generated at: `2026-06-15T14:17:37Z`

## Summary

Archive.org packet with availability metadata and snapshot body preserved for 20230530100738.

## Requested Context

- Decision question: Backtest: at the ~Aug 2024 SKU-kill decision, did Imaginary Authors' pre-cutoff public site show Whispered Myths + Telegrama as live products? (known later outcome: both quietly discontinued Aug 2024, low-sales rationale)
- Capture context: Pre-cutoff backtest evidence capture (capture-spine deliverable; INV-1 facts+limits only; feeds a future judgment-spine fixture)
- Source locator: https://imaginaryauthors.com/
- Actor/audience context: unknown_with_reason (actor or audience context was not supplied to the archive runner)

## Timing

- Source publication or event timing: unknown_with_reason (Archive.org adapter did not infer original source publication or event timing)
- Source edit or version timing: Archive.org snapshot timestamp 20230530100738
- Capture timing: 2026-06-15T14:17:37Z
- Re-capture timing: not_applicable (archive packet did not model an earlier capture by default)
- Cutoff posture: pre_cutoff

## Posture

- Access posture: archive_org availability metadata and selected snapshot body preserved
- Archive/history posture: archived
- Media/modality posture: not_applicable (archive runner does not retrieve linked media assets)
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this archive capture)

## Preserved Files

- `file_01` -> `raw/01_archive_availability_metadata.json` (sha256 `332d1191d6ae5c628a505020e32f65bf453130fabd7e8e56bd99adad84326576`, 4559 bytes)
- `file_02` -> `raw/02_archive_snapshot_body.bin` (sha256 `eeb6e602bf12854e2566116f50927993aa6bdfa406a3d317f6f8c88d7528d4c9`, 162646 bytes)
- `file_03` -> `raw/03_archive_snapshot_body_metadata.json` (sha256 `5dc5cb51c819a12b07f15050240d83cfeee38508527d1e53d17b4a9879b4546d`, 908 bytes)

## Warnings

- direct_http followed redirect from https://web.archive.org/web/20230530100738/http://imaginaryauthors.com/ to https://web.archive.org/web/20230601090132/https://imaginaryauthors.com/

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
