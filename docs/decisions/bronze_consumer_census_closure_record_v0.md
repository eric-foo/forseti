# Bronze Consumer Census Closure Record (v0)

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record (docs/decisions/; bronze derived-record writer census closure)
scope: >
  Closes the bronze-consumer shapes lane census: classifies every known
  derived-record writer over the data lake into the four census shapes with
  reasons, records the classify-outs, names the executable completion signal
  (runners/run_seam_cadence.py) and its gates, carries the accumulated
  residual ledger, and states the live dry-run status.
use_when:
  - Checking whether a derived-record writer is on the consumption seam, classified out, or unclassified.
  - Adding a new bronze-deriving lane (classify it here AND in the cadence coverage gate).
  - Preparing or adjudicating the bronze cadence live dry-run.
stale_if:
  - A derived-record writer is added, retired, or changes its scanning mode (the coverage gates fail first; update both).
  - The live dry-run completes and its result record supersedes the dry-run status below.
authority_boundary: retrieval_only
```

## What this record closes

The bronze-consumer shapes lane (predecessor; handoff
`docs/prompts/handoffs/data_lake_bronze_consumer_shapes_lane_handoff_prompt_v0.md` on PR #639, branch `claude/bronze-consumer-shapes-handoff`)
required a census-closure record classifying every derived-record
writer into its four shapes, plus a two-consecutive-cycle cadence dry-run
performing zero work the second time. This record is that census. The cadence
is now an executable — `orca-harness/runners/run_seam_cadence.py` — so the
completion signal no longer needs an agent at steady state.

Shape definitions: predecessor handoff (above). Classifications below are
verified against the current gates and code on `origin/main` @ `1b551e48`
(consumer gate `tests/contract/test_catchup_runner_seam_coverage.py`, producer
gate `tests/contract/test_capture_runner_lake_seam_coverage.py`, and the
writers/runners named per row), except rows explicitly marked as carried
secondary reports.

## Shape 1 — lake-scanning derivers (own discovery, on seam)

| Writer | Status |
| --- | --- |
| `runners/run_transcript_product_extract.py` | Seam consumer (consumer gate member). Classified OUT of the compute-free cadence: owner-gated per-turn LLM extraction; backlog visible via its own `--check`. |
| `runners/run_ig_reels_product_extract.py` | Same classification, same reason. |

## Shape 2 — per-packet derivers, now closed by seam catch-up entrypoints

Every formerly discovery-less per-packet deriver now has a seam catch-up
entrypoint, each a consumer-gate member with its own behavioral test suite:

| Writer | Catch-up entrypoint | Behavioral tests |
| --- | --- | --- |
| `ecr/lake.py` | `runners/run_ecr_catchup.py` | `tests/unit/test_ecr_catchup.py` |
| `cleaning/fragrantica_lake.py` | `runners/run_fragrantica_cleaning_catchup.py` | `tests/unit/test_fragrantica_cleaning_catchup.py` |
| `cleaning/basenotes_lake.py` | `runners/run_basenotes_cleaning_catchup.py` | `tests/unit/test_basenotes_cleaning_catchup.py` |
| `cleaning/parfumo_lake.py` | `runners/run_parfumo_cleaning_catchup.py` | `tests/unit/test_parfumo_cleaning_catchup.py` |
| `source_capture/fragrance_review_lake.py` | `runners/run_fragrance_review_projection_catchup.py` | `tests/unit/test_fragrance_review_projection_catchup.py` |
| `source_capture/ig_reels_grid_projection.py` | `runners/run_ig_reels_grid_projection_catchup.py` | `tests/unit/test_ig_reels_grid_projection_catchup.py` |
| `source_capture/transcript/asr_packet.py` + `ig_reels_audio_packet.py` | `runners/run_asr_transcript_catchup.py` (owner-operated local ASR compute) | `tests/unit/test_asr_transcript_catchup.py` |

Classified out of shape-2 catch-up (no committed-record consumer exists):

- `projection_{fragrantica,basenotes,parfumo,ig,retail_pdp}` appending
  projections — zero committed-record consumers: Cleaning rebuilds its
  projections in memory by design, and the retail flows consume operator
  files. No catch-up entrypoint is owed until a committed-record consumer
  appears (which would fail the coverage gates first).

## Shape 3 — read-only analytics, seam-free by contract

`data_lake/sov_readout.py`, `runners/run_sov_extraction_quality_eval.py`,
`data_lake/derived_retrieval_views.py`,
`source_capture/ig_reels_behavioral_lake.py`,
`youtube_capture/behavioral_projection.py`. Views and readouts never ack, and
pickup never consults them (view-independence, seam contract). Do not "sync"
these.

## Shape 4 — out of seam domain

`runners/run_source_capture_youtube_rss_monitor.py` (its work is external feed
entries, not bronze) and `capture_spine/creator_profile_current/*` (a
repo-materialized view with its own freshness gate). Correct as-is; recorded,
unchanged.

## Family notes

- `web_page` and `reddit` families: no family-specific deriving lane consumes
  them; the family-agnostic ECR catch-up covers every committed packet
  regardless of family (verified: `run_ecr_catchup.py` pickup carries no
  `source_family` filter; exercised in `tests/unit/test_seam_cadence.py`).
  Not a dry-run blocker.
- Deep-capture: off-seam by frozen decision (its transcripts are deep-capture
  record sets).

## The executable completion signal

`runners/run_seam_cadence.py`:

- `--run`: every cadence entrypoint executes twice; exit nonzero if the SECOND
  cycle performs any work or emits any status. Failures never satisfy the
  signal (unacknowledged work re-surfaces in cycle 2).
- `--skip-asr`: skips only ASR execution for compute-free cadences, printing a
  visible `skipped_asr_compute` marker with the live pending count EVERY
  cycle — never a silent skip.
- `--check`: compute-free per-entrypoint backlog counts.

Coverage is pinned, not assumed: `tests/contract/test_seam_cadence_coverage.py`
requires `CADENCE_ENTRYPOINTS` plus `CLASSIFIED_OUT_SEAM_CONSUMERS` (the two
shape-1 LLM extract runners) to exactly cover the discovered seam-consumer
surface, so a new seam consumer must be classified in or out here and in the
runner, loudly. Behavioral contract: `tests/unit/test_seam_cadence.py`.

Test-lake two-consecutive-cycle dry-run: passing as a unit test
(`test_backlog_drains_in_cycle_one_and_second_cycle_is_zero` — cycle 1 drains,
cycle 2 zero, byte-unchanged idempotence).

## Live dry-run status

**Blocked pending a per-turn owner live-lake read grant** (and owner-operated
ASR compute, or `--skip-asr`). Never simulated. Expected first-cycle work,
carried from the predecessor lane's granted read (secondary report — re-verify
at the dry-run, do not trust this copy): 6 fragrantica + 1 parfumo cleaning
derivations; fragrance-review / grid / ASR backlogs as found. Second cycle
must be zero.

## Residual ledger (accumulated, carried)

- Comment-bound version-bump discipline is mechanized by the pin gate
  (`test_policy_module_version_pins.py`); accepted residual: a pin can be
  updated without bumping — the ritual is directed, not automated.
- Transcript record shapes + `fragrance_review_lake` projection +
  `transcript_product_lake` ride no schema version token (weak-envelope
  class, pinned in the pin gate; closure is silver-lane unit (d)).
- `projection_ig_reels_grid` record-id policy is coupled to
  `instagram_metric_seed`'s lexical tie-break (F-IGRC-001 — re-review if
  either side changes).
- Partial record-set crashes still need operator cleanup (loud collision;
  lake write-boundary work).
- Private metric-spec import couplings (fragrantica/parfumo).
- Operator-pointed fragrance-review projections still default `as_of` to
  today() (the catch-up entrypoint pins it).
- Out-of-scope-surface ack convention (known non-target surfaces acked with
  explicit evidence; unknown surfaces stay visible and unacked).
- `datetime.utcnow()` deprecation class in transcript writers.

## Non-claims

- Not validation, readiness, acceptance, or a live-lake claim. Green tests and
  this record's existence do not close the bronze lane; the closure claim
  requires the owner-granted live dry-run showing second-cycle-zero.
- The carried live-lake census counts are secondary reports until re-verified
  under a fresh grant.
- Classification here is census shape only; each lane's correctness authority
  stays with its own tests, gates, and adjudication records.
