# Source Capture Packet Receipt

- Packet ID: `01KVZGJWQN8YGZQGAGA2S2CQPV`
- Manifest version: `source_capture_packet_manifest_v1`
- Obligation contract version: `core_spine_v0_data_capture_spine_obligation_contract_v0`
- Source family: `instagram_creator`
- Source surface: `ig_reels_grid_dom_passive_json`
- Session identity: `01KVZGJWQNQKP9F7X2FKJBG9DA`
- Capture mode: `automated extraction`
- Visible mode changes: ig_reels_grid_no_item_fanout:rows=12:json_candidates=30:passive_json=5, ig_reels_grid_metrics:views=12:likes=12:comments=12, ig_reels_grid_bandwidth_mode:block_heavy_assets
- Operator category: `ig_reels_grid_cli_operator`
- Receipt generated at: `2026-06-25T13:47:49Z`

## Summary

IG reels-grid packet for https://www.instagram.com/jeremyfragrance/reels/: 12 DOM row(s), 30 passive JSON media candidate(s), 12 observed view_count metric(s); no item pages visited.

## Requested Context

- Decision question: reels-tab pin positive validation (clips_tab_pinned + grid recency inversion) 2026-06-25
- Capture context: logged-out IG public /reels/ grid capture; one page load; no hover/click/item-page fan-out; passive page-load JSON preserved when observed
- Source locator: https://www.instagram.com/jeremyfragrance/reels/
- Actor/audience context: public creator profile; logged-out capture; internal creator-monitoring calibration

## Timing

- Source publication or event timing: unknown_with_reason (profile grid slice is the enumeration source, not a dated post)
- Source edit or version timing: unknown_with_reason (IG reels-grid runner did not infer source edit/version timing)
- Capture timing: 2026-06-25T13:47:49Z
- Re-capture timing: not_applicable (IG reels-grid packet does not model an earlier capture by default)
- Cutoff posture: unknown_with_reason (IG reels-grid runner did not receive cutoff posture metadata)

## Posture

- Access posture: ig_logged_out_reels_grid_browser_capture; public DOM and passive page-load JSON
- Archive/history posture: not_attempted (IG reels-grid runner does not query archive or history services)
- Media/modality posture: DOM media-anchor text and passive JSON metadata preserved; raw media bytes are out of scope
- Re-capture relationship: not_applicable (no prior source capture packet was supplied for this IG reels-grid capture)

## Preserved Files

- `file_01` -> `raw/01_ig_reels_grid_capture.json` (sha256 `1d782de486a63d41bf4dc4f5143cc1269f0ce04dba669f0bc6156566fe27f700`, 974652 bytes)

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
