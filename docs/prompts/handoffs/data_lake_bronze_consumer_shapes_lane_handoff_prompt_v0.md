# Bronze-Consumer Shapes Lane — Fresh-Thread Handoff (v0)

```yaml
retrieval_header_version: 1
artifact_role: Handoff prompt artifact (fresh-lane takeover, docs/prompts/handoffs/)
scope: >
  Cold handoff for a fresh thread with none of the prior lane's context: bring
  EVERY lane that lands into or derives from the bronze lake to the state
  where it finds its own work and records completion through the consumption
  seam (or is explicitly classified out of the seam's domain with a recorded
  reason) — so the silver lane/vault supports any analytics easily and
  cadence runs become possible. Carries the four-shape census, the ordered
  work queue, and the ROBUST per-shape success signals the new lane must
  optimise for.
use_when:
  - Starting the fresh bronze-consumer shapes lane (paste the wrapper or open this file first).
  - Checking whether a given lane still needs a seam catch-up entrypoint.
stale_if:
  - The census classifications change (a lane gains/loses a scanning mode).
  - The seam contract or lane_registry namespace rule changes.
authority_boundary: retrieval_only
non_claims:
  - not validation, readiness, or acceptance; the success signals define what WOULD count, they assert nothing has passed
```

```yaml
goal_handoff:
  anchor_goal: >
    Silver lane/vault at a level where any analytics can easily be performed,
    and every runner (ECR, Cleaning, projections, extraction) synced with the
    bronze GT shape so it picks up new committed evidence BY ITSELF — which
    is what enables cadence runs. (Owner framing, 2026-07-03.)
  success_signal: >
    Census closure: every derived-record writer over the lake is either on
    the seam (scanning or catch-up mode) with the per-lane behavioral signals
    below passing as tests, or carries a recorded shape-3/4 classification
    with its reason; and a two-consecutive-cycle cadence dry-run over an
    unchanged lake performs zero work the second time. Artifact existence,
    green tests alone, or docs claiming sync do NOT satisfy this signal.
  lifecycle_status: active_thread_local
```

## Mission in one paragraph

The consumption seam (contract:
`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`;
helper: `orca-harness/data_lake/consumption.py`) makes a derived lane
discover committed bronze work by key and record completion as append-only,
evidence-bearing ack facts, so cadence runs are idempotent and cheap. Two
lanes are migrated and adjudication-hardened: YouTube transcript extraction
(#580) and IG reels extraction (#637 — read it as the PATTERN, including its
adjudicated F1/F2 patch). The remaining work is NOT "migrate more scanning
runners" (a census found none left); it is (1) mirroring two known defect
classes onto the YouTube runner, and (2) giving the per-packet derivers —
ECR, the review/fragrance Cleaning lanes, the appending projections — a
seam-shaped CATCH-UP entrypoint, because today they derive records only when
an operator points them at one packet: they have NO discovery at all, and a
packet nobody points at never gets its derived records.

## The four shapes (census, 2026-07-03, from source)

Evidence instruments: `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`
(the checked-in touchpoint census; regenerate via `data_lake.inventory`),
`tests/contract/test_capture_runner_lake_seam_coverage.py`, plus greps for
`list_available(` (scanning) and `append_record(_set)?(` (derived writers).

1. **Lake-scanning derivers (seam home turf) — 2 exist, 2 migrated:**
   `runners/run_transcript_product_extract.py` (YT),
   `runners/run_ig_reels_product_extract.py` (IG packet route). No other
   non-test `list_available` caller writes derived records.
2. **Per-packet derivers with NO catch-up mode — the open backlog:**
   `ecr/lake.py` (ECR record sets), `cleaning/{fragrantica,basenotes,parfumo}_lake.py`,
   `source_capture/fragrance_review_lake.py` (purchase-review tee+projection),
   appending projections (`source_capture/ig_reels_grid_projection.py`,
   `retail_pdp_projection.py`, `{fragrantica,basenotes,parfumo,ig}_projection.py`),
   ASR writers (`source_capture/transcript/{asr_packet,ig_reels_audio_packet}.py`
   — capture-time today; a "transcribe the untranscribed backlog" mode is a
   candidate, LLM/ASR cost is owner-gated).
3. **Read-only analytics — correctly seam-free BY CONTRACT (do not "sync"):**
   `data_lake/sov_readout.py`, `runners/run_sov_extraction_quality_eval.py`,
   `data_lake/derived_retrieval_views.py`, behavioral projections
   (`source_capture/ig_reels_behavioral_lake.py`, `youtube_capture/behavioral_projection.py`).
   Views/readouts never ack and pickup never consults them (view-independence).
4. **Out of seam domain:** `runners/run_source_capture_youtube_rss_monitor.py`
   (work = external feed entries, not bronze) and
   `capture_spine/creator_profile_current/*` (repo-materialized view with its
   own freshness gate). Correct as-is; record the classification, change nothing.

## Ordered work queue

1. **(a) YouTube-runner mirror** — the adjudication class sweep
   (`docs/review-outputs/adversarial-artifact-reviews/ig_reels_seam_migration_delegated_adversarial_code_review_v0.md`)
   names both classes in `run_transcript_product_extract.py`: F1
   (`_asr_records` silently `continue`s on damaged records → a
   `no_extractable_transcripts` ack can cover damaged input) and F2
   (obligation lacks `rubric_version`). Mirror the #637 adjudicated fixes
   (cheap obligation entries stay NON-RAISING; transcript reads fail loud).
   Includes checking whether live YT acks exist (live-lake read = fresh owner
   grant) and stating the pre-patch-ack disposition.
2. **(g-ECR) seam catch-up entrypoint for ECR** — first gating read is
   `ecr/lake.py` + its callers: what a packet's ECR obligation snapshot must
   contain is UNVERIFIED (do not inherit the extraction lane's snapshot shape
   blindly). Ack namespace must be ECR's registered output lane in
   `data_lake/lane_registry.py::LANE_ROLES`.
3. **(g-reviews/cleaning) catch-up for the fragrance/review Cleaning lanes** —
   same shape, one lane per unit; order by which case family the owner wants
   cadence-fed first.
4. **(g-projections) appending projections** — opportunistic, same shape.
5. **Census-closure record** — small durable record classifying every
   derived-record writer into shapes 1-4 with reasons; this is what makes
   "done" checkable (see the completion signal).

Parked owner-gated items this lane must NOT absorb: deep-capture anchoring
decision (input doc:
`docs/workflows/ig_reels_deep_capture_anchoring_decision_input_v0.md`),
brand/line catalog, pilot cohort + first real SoV readout, cadence
activation, movement_threshold_crossings contract, ground-truth labeling.

## ROBUST success signals — optimise for THESE, per migrated/catch-up lane

Behavioral proofs in tests, not artifact existence. A unit claiming success
must show, in its own test suite over a temp lake:

- **S1 Finds its own backlog (the anti-drift signal — the actual gap):**
  commit a packet of the lane's family WITHOUT invoking the per-packet
  command; ONE catch-up run derives the output and acks with evidence.
- **S2 Does nothing twice:** an immediate second run over the unchanged lake
  emits ZERO status entries and performs ZERO lake writes (assert the lake
  tree is byte-unchanged, not merely "no failures").
- **S3 Growth re-surfaces:** append a late input record (and separately bump
  a policy token, e.g. rubric/model): the SAME anchor re-surfaces and re-acks
  under the new fingerprint; unchanged anchors stay silent.
- **S4 Damage is loud:** corrupt one input record: typed failure status,
  NO ack, re-surfaces every run (never a silent skip that lets the anchor
  ack as input-less — the F1 class).
- **S5 Failure blocks the ack:** an induced per-item failure leaves the
  anchor unacknowledged while the batch continues (isolation + no fake done).
- **S6 Boundaries hold:** ack namespace ∈ `LANE_ROLES`; zero acks under
  non-committed anchors; obligation snapshot is cheap and NON-RAISING
  (a raising `obligation_fn` aborts the whole pickup); read-only lanes
  (shape 3) still never ack.
- **S7 Gates:** full orca-harness suite green with JUnit-verified counts
  stated; touchpoint inventory regenerated (byte-identical or updated with
  the counter test); review disposition routed per the repo-mode cross-vendor
  convention; CI green on the PR.

**Lane-completion signal (when the whole lane is done):** the census-closure
record exists with zero unclassified derived-record writers, every shape-1/2
entry points at its passing S1-S7 tests, AND a two-consecutive-cycle cadence
dry-run (test lake, all catch-up entrypoints invoked in sequence, twice)
performs zero work on the second cycle.

**Anti-signals (do NOT count):** green tests without S1; acks existing in a
lake; a green run over an empty lake; docs or commit messages asserting
sync; inventory regeneration alone; any claim about the live lake without a
granted read.

## Authority, constraints, conventions (binding)

- Read `AGENTS.md` + `.agents/workflow-overlay/README.md` first; the overlay
  owns project rules. Disciplined pattern is STANDING for every
  implementation unit in this lane: workflow-assumption-gate → /fused.
- Never write to `F:\orca-data-lake`; live-lake READS need a fresh owner
  grant each turn; LLM/ASR runs are owner-gated.
- Fresh branch off origin/main per unit; explicit `git push -u origin <lane>`
  (bare `git push` is guard-blocked); owner merges PRs; never continue
  committing on a branch whose PR merged.
- Review loop: repo-mode cross-vendor commission (pattern:
  `docs/prompts/reviews/ig_reels_seam_migration_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md`;
  pin fresh commit SHA + LF-blob SHA256s per dispatch), owner couriers,
  home-CA adjudication, adjudication record under
  `docs/review-outputs/adversarial-artifact-reviews/` with the
  `review_use_boundary` header field (CI gate). Commit bodies carry
  `review_routing_status: routed <existing path>` when touching code roots.
- Validation quirk: the PowerShell pipeline eats pytest's summary line and
  exit code — use `--junitxml` + ElementTree parse for verified counts; run
  with `ORCA_DATA_ROOT` cleared; invoke `python`, never `python3`.

## Gating reads per unit (order matters)

Seam contract + `data_lake/consumption.py` + the #637 runner AND its tests
(`tests/unit/test_ig_reels_product_extract.py` — S1-S6 shapes exist there as
worked examples) BEFORE any design; then the target lane's writer + callers;
then `lane_registry.py`. For (a): also the adjudication record's F1/F2
verification notes.

## Frozen decisions — do not reopen

- Deep-capture route stays OUT of the seam until the owner decides anchoring
  (no acks under uncommitted shortcode anchors, ever).
- On-demand-first metrics; views are rebuildable caches; pickup never reads
  views; views never ack.
- Ack namespace = a lane already in `LANE_ROLES` (no new registry).
- Obligation envelopes carry `obligation_schema`, `consumer`, and the policy
  tokens whose change must re-trigger work (model + rubric_version per the
  adjudicated F2).
- SoV numerator is mention-level; malformed evidence is rejected-and-counted,
  never repaired.
```

## Paste-ready fresh-thread wrapper

````markdown
Read and execute the handoff at
docs/prompts/handoffs/data_lake_bronze_consumer_shapes_lane_handoff_prompt_v0.md
(branch: main). Goal and success signals are inside — optimise for the
behavioral signals S1-S7 and the census-closure completion signal, not for
artifact existence. Start with unit (a) (YouTube-runner F1/F2 mirror) under
the standing disciplined pattern (assumption-gate → fused) on a fresh branch
off origin/main. Owner merges PRs; live-lake reads need my per-turn grant.
````
