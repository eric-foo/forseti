## Summary

This PR lands the IG reels-grid capture/projection spine.

It adds:
- a public logged-out IG `/reels/` grid capture packet runner
- DOM + passive JSON parsing for reels-grid engagement rows
- a source-surface-preserving IG reels-grid projection adapter
- a projection runner that can append by-key derived records into the Orca data lake
- DOM-grid fallback promotion in projection when passive JSON does not join, with explicit `dom_grid_engagement` provenance
- related IG/data-lake docs, review outputs, and repo-map routing

## Why

The creator-ledger lane needs source-backed per-creator/per-platform aggregate metrics. IG grid capture is enough to supply views, likes, and comments for reels when the projection preserves provenance: JSON-backed when available, DOM-grid-backed when JSON is absent.

This PR does not implement the creator ledger itself. It provides the IG capture/projection feeder layer the ledger can consume.

## Validation

Ran locally:

```powershell
python -m py_compile orca-harness\source_capture\ig_reels_grid_projection.py orca-harness\runners\run_ig_reels_grid_projection.py orca-harness\tests\unit\test_source_capture_ig_reels_projection.py
python -m pytest -q orca-harness\tests\unit\test_source_capture_ig_reels_projection.py orca-harness\tests\unit\test_source_capture_ig_reels_grid_packet.py orca-harness\tests\test_ig_projection_lake_pilot.py
```

Observed result: `28 passed`.

Live reprobe evidence written to `F:\orca-data-lake`:
- Existing DOM-only `vanzzcoser` packet reprojected to 36 observed media metric rows from `dom_grid_engagement`.
- Fresh `vanzzcoser` live reprobe captured raw packet `01KW9WD600VE4NXCKF364N8ZH9` and derived projection `01KW9WDN2BSPC5RM6X7EMC4HE8.json`.

## Boundaries

- No creator-ledger implementation in this PR.
- No Cleaning, ECR, Judgment, dashboard, scheduler, or buyer-facing claim.
- Raw Bronze packets remain immutable; projection records are append-only derived records.