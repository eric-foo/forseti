# Source Capture Packet Receipt

- Packet ID: `01KVZF02BWJEFC3CH1JH97CPKQ`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `instagram_creator`
- Source surface: `ig_reels_grid_dom_passive_json`
- Session identity: `01KVZF02BW7H0KFHMZWWXQ8J98`
- Capture mode: `automated extraction`
- Visible mode changes: ig_reels_grid_no_item_fanout:rows=12:json_candidates=36:passive_json=5, ig_reels_grid_metrics:views=12:likes=12:comments=12, ig_reels_grid_bandwidth_mode:block_heavy_assets
- Operator category: `ig_reels_grid_cli_operator`
- Receipt generated at: `2026-06-25T13:20:04Z`

## Summary

IG reels-grid packet for https://www.instagram.com/esthertakumi/reels/: 12 DOM row(s), 36 passive JSON media candidate(s), 12 observed view_count metric(s); no item pages visited.

## Requested Context

- Decision question: diagnostic: join-yield cause + pinned recency-inversion validation (2026-06-25)
- Capture context: logged-out IG public /reels/ grid capture; one page load; no hover/click/item-page fan-out; passive page-load JSON preserved when observed
- Source locator: https://www.instagram.com/esthertakumi/reels/
- Actor/audience context: public creator profile; logged-out capture; internal creator-monitoring calibration

## Timing

- Source publication or event timing: unknown_with_reason (profile grid slice is the enumeration source, not a dated post)
- Source edit or version timing: unknown_with_reason (IG reels-grid runner did not infer source edit/version timing)
- Capture timing: 2026-06-25T13:20:04Z
- Re-capture timing: not_applicable (IG reels-grid packet does not model an earlier capture by default)
- Cutoff posture: unknown_with_reason (IG reels-grid runner did not receive cutoff posture metadata)

## Posture

- Access posture: ig_logged_out_reels_grid_browser_capture; public DOM and passive page-load JSON
- Archive/history posture: not_attempted (IG reels-grid runner does not query archive or history services)
- Media/modality posture: DOM media-anchor text and passive JSON metadata preserved; raw media bytes are out of scope
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this IG reels-grid capture)

## Preserved Files

- `file_01` -> `raw/01_ig_reels_grid_capture.json` (sha256 `38805ac55b9f9790f7791b07c3efde31810bb91ae06b6a79a273dd66bf408e83`, 1049671 bytes)

## Warnings

- none

## Limitations

- heavy_asset_blocking_enabled: image/media/font requests aborted to reduce bandwidth; scripts and JSON/XHR left intact; content sufficiency not asserted

## Non-Claims

- not content sufficiency proof
- not login or session capture
- not stored profile or cookie use
- not anti-detect behavior
- not proxy endpoint or credential disclosure
- not proxy exit IP disclosure
- not CAPTCHA solving
- not crawler or scheduled monitoring
- not item-page fan-out
- not comment text capture
- not full-history backfill
- not static/main-grid comparison capture
- not full momentum curve
- not projection fold
- not media byte preservation
- not API SDK use
- not ECR design
- not Cleaning implementation
- not Judgment scoring
- not buyer proof
- not commercial-readiness logic
