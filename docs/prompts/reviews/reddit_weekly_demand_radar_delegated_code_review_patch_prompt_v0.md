# Reddit Weekly Demand Radar — Delegated Code Review-And-Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated_code_review_and_patch commission)
scope: >
  Commission for a de-correlated, different-vendor code review-and-patch pass
  over the weekly demand radar evidence layer (observe verb, grid projection
  v2, grid runner retention rules, materializer surface stamping, weekly
  reader), with Chief Architect adjudication before any change is kept.
use_when:
  - Couriering the delegated review of the weekly demand radar build.
  - Checking which failure classes this commission was raised against, or
    adjudicating its return.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_weekly_demand_radar_spec_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/prompts/reviews/reddit_subreddit_registry_lake_cutover_delegated_code_review_patch_prompt_v0.md
```

## Status

`COMMISSIONED — NOT DISPATCHED`. This artifact is the commission and courier
body, not a review result; it asserts no verdict, validation, or readiness.

Output mode: `paste-ready-chat` — this file is the courier body. The
controller's return goes to chat or the lane PR comment and writes no durable
report under `docs/review-outputs/` unless separately commissioned.

**Freeze discipline (learned from the prior run's `BLOCKED_CONCURRENT_WRITER`):
the commissioning lane must not commit between the courier paste and the
controller's return. The reviewed revision is the lane branch head at paste
time; the controller records that hash in its return.**

## Actor / model-family receipt

- Author / home model family: Anthropic (Claude). Dispatch mode:
  operator-couriered. **Who-constraint: the paste target must be a different
  vendor lineage (non-Anthropic); a same-vendor tier is not de-correlated.**
- Current receiving actor: controller (the model this prompt is pasted into).
  Verify you are not Anthropic-lineage before proceeding; if you are, return
  `BLOCKED_CONTROLLER_NOT_DECORRELATED` and stop.

## Why this was commissioned

Raised under the owner's standing `delegate patch after` instruction for this
build. The activating condition: material failure modes in the diff share
their assumptions with the tests that validate them, so passing CI proves
little for exactly these classes:

1. **Hand-rolled HTML depth tracking** in `grid_projection.py` (`_titlebox`,
   `_users_online`, new `_age_span` and flair capture): the counters advance on
   every non-void start tag and decrement on every end tag, a heuristic, not a
   real DOM stack. The fixture proves the happy path on real markup; it cannot
   prove no cross-capture bleed (a flair captured from an adjacent element, a
   created-datetime read from a non-sidebar `span.age`) on malformed or
   differently-nested pages. There is no independent oracle for this parser.
2. **Retention rule interactions** in `run_reddit_grid_capture.py`: the
   rotating raw sample (`(iso.year*100 + iso.week) % len(sorted(names))`) and
   the anomaly-raise path (extractor raises -> `raw_failure` fallback) were
   authored and tested by the same hand. Check rotation coverage (does the
   modulo visit all roster members across weeks or bias?), the anomaly
   predicate's false-positive/negative surface, and whether a raw_failure
   packet flows correctly through the materializer's raw re-projection path.
3. **Weekly reader window/dedupe semantics** in
   `run_reddit_weekly_demand_read.py`: newest-packet-per-sub via
   `(observed_at, packet_id)` tuple compare, the 7-day window boundary, and
   silent-drop paths (`rows_dropped_unparsed`, non-roster subs, non-top-week
   listings). The reader is the lane's coverage claim; a silent under-read is
   the named defect class.
4. **Reach observation row effects** in `data_lake/reddit_subreddit_registry.py`
   (`append_reach_observation`): asserts NO status/capture_state effects and
   relies on provenance-pointer dedupe shared with grid observations. Check
   fold interactions with mixed old-shape/new-shape observation dicts.

## Commissioned scope (editable; everything else is flag-only)

- `forseti-harness/data_lake/reddit_subreddit_registry.py` (append_reach_observation only)
- `forseti-harness/capture_spine/reddit_subreddit_grid/grid_projection.py`
- `forseti-harness/capture_spine/reddit_subreddit_grid/materializer.py` (surface stamping only)
- `forseti-harness/runners/run_reddit_grid_capture.py`
- `forseti-harness/runners/run_reddit_weekly_demand_read.py`
- `forseti-harness/runners/run_reddit_subreddit_registry_refresh.py`
- Their tests: `tests/unit/test_reddit_subreddit_registry_lake.py`,
  `tests/unit/test_reddit_subreddit_grid.py`, and the fixture under
  `tests/fixtures/reddit_subreddit_grid/`.

Owner contract for intent: `forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_weekly_demand_radar_spec_v0.md`.

## Controller instructions

1. Inspect the pinned lane branch (`claude/reddit-graphing-lane-d07de4`)
   directly; no summaries or recreated source. Record the head hash you review.
2. Run the code-review lane contract carried by this repository
   (`.agents/workflow-overlay/review-lanes.md` and the kernel code-review
   doctrine it names); findings need file/line citations and a concrete
   failure scenario each.
3. Patch only within the commissioned scope, working-tree edits only — no
   commit, push, PR, stash, reset, or branch surgery.
4. Validation: `python -m pytest tests/unit/test_reddit_subreddit_grid.py
   tests/unit/test_reddit_subreddit_registry_lake.py -q` plus the contract
   gates `tests/contract -k "seam or inventory"`. State what ran and what did
   not.
5. Return: unified diff, per-change citations, one verdict, residual-risk
   note. On a design-level problem, revert any partial diff and return
   `NEEDS_ARCHITECTURE_PASS` with findings only.
6. The Chief Architect adjudicates before anything is kept; your diff is a
   claim, not a merge.
