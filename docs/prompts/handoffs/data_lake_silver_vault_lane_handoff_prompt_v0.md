# Data Lake Silver/Vault Lane — Handoff Prompt (v0)

```yaml
retrieval_header_version: 1
artifact_role: Lane handoff prompt (docs/prompts/handoffs/; cold-start mission + queue for a new thread)
scope: >
  Cold-start handoff for the Data Lake SILVER/VAULT lane: make Silver the
  trustworthy read layer (lineage-complete, supersession-explicit,
  consumer-enumerated, vault-schema-versioned), plus the single bridge unit
  that closes the predecessor bronze-consumer shapes lane (census record +
  cadence dry-run). Carries the goal frame, behavioral signals, unit queue,
  inherited conventions (the F-* adjudication ledger), standing workflow
  pattern, security rules, and the accumulated residual ledger.
use_when:
  - Kicking off the silver/vault lane in a fresh thread (owner ratifies the goal frame at kickoff before any build).
  - Executing the bronze census-closure bridge unit.
stale_if:
  - The census-closure bridge unit has landed (then unit (a) is done history).
  - The owner re-frames the silver mission at kickoff (the frame below is a PROPOSAL).
authority_boundary: retrieval_only
```

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (bronze-consumer lane end-state + adjudication records +
    live touchpoint baselines in tests/contract/; all compare targets pinned in-repo)
  edit_permission: docs-write (this handoff artifact only)
  target_scope: docs/prompts/handoffs/data_lake_silver_vault_lane_handoff_prompt_v0.md
  dirty_state_checked: yes (authored on claude/silver-vault-lane-handoff off origin/main)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound by the artifact-folders overlay file and the in-repo handoff pattern.
```

## Read this first (cold start)

1. `AGENTS.md` + `.agents/workflow-overlay/README.md` (always).
2. The predecessor lane's adjudication records under
   `docs/review-outputs/adversarial-artifact-reviews/` — they ARE the
   convention ledger (F-ECR-001, F-FRAG-001/002, F-YT-001, F-SH-001,
   F-IGRC-001/002, F-FRP-001, F-ASR-001; each record's `use_when` says what
   it binds).
3. The three contract gates that mechanized those conventions:
   `orca-harness/tests/contract/test_catchup_runner_seam_coverage.py`,
   `test_cleaning_family_surface_partition.py`,
   `test_policy_module_version_pins.py` — a new lane mostly needs to "use
   the helper, pass the gates", not re-read doctrine.
4. The seam contract:
   `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`
   + `orca-harness/data_lake/consumption.py`.

## Predecessor end state (bronze-consumer shapes lane, verified facts)

Every known bronze-deriving lane is ON the consumption seam or CLASSIFIED
OUT with a recorded reason:

- On-seam catch-ups (all merged or in the final open PR): ECR
  (`run_ecr_catchup`), cleaning ×3 (`run_{fragrantica,basenotes,parfumo}_cleaning_catchup`),
  fragrance-review projection (`run_fragrance_review_projection_catchup`),
  ig-reels-grid projection (`run_ig_reels_grid_projection_catchup`), ASR
  transcripts (`run_asr_transcript_catchup`, PR #658), plus the YT/IG
  extract runners (already seam consumers; their swallowed reconciles fixed).
- Classified out (record the reasons in the census unit):
  `projection_{fragrantica,basenotes,parfumo,ig,retail_pdp}` — zero
  committed-record consumers (Cleaning rebuilds in memory by design; retail
  flows consume operator files); the `web_page` (18 pkts) and `reddit`
  (25 pkts) families — no deriving lane consumes them (all generic-surface
  packets live there; NOT a dry-run blocker); deep-capture — off-seam by
  frozen decision; read-only analytics — seam-free by contract.
- Live-lake census (from the granted read this lane): fragrance family = 6
  fragrantica + 1 parfumo packets, all named surfaces inside the partition;
  no unknown surfaces in any gated family.

## Unit (a) — BRIDGE: bronze census closure + cadence dry-run (do first)

The predecessor's completion signal is not yet emitted. Build, under the
standing pattern:

1. `runners/run_seam_cadence.py`: execute every seam catch-up entrypoint
   twice (`--check`/`--run` composition); exit nonzero if the SECOND cycle
   performs any work or emits any status. This makes the completion signal
   an executable — no agent needed at steady state. (ASR entry needs its
   `--model`/`--compute-type`; a `--skip-asr` flag with a VISIBLE skipped
   marker is acceptable for compute-free cadences — never a silent skip.)
2. The census-closure record (docs/decisions/ or the overlay-named home):
   classify every derived-record writer into the handoff shapes 1–4 with
   the classify-outs above and the residual ledger below.
3. Live dry-run needs a per-turn owner read grant (and owner-operated ASR
   compute if not skipped). Expected first-cycle work: 6 fragrantica + 1
   parfumo cleaning derivations, fragrance-review/grid/ASR backlogs as
   found; second cycle must be zero.

Residual ledger to carry into the census record (accumulated, verified):
comment-bound version-bump discipline now mechanized by the pin gate (its
accepted residual: a pin can be updated without bumping — the ritual is
directed, not automated); transcript record shapes + `fragrance_review_lake`
projection + `transcript_product_lake` ride no schema version token
(weak-envelope class, pinned); `projection_ig_reels_grid` record-id policy
is coupled to `instagram_metric_seed`'s lexical tie-break (F-IGRC-001 —
re-review if either side changes); partial record-set crashes still need
operator cleanup (loud collision, lake write-boundary work); private
metric-spec import couplings (fragrantica/parfumo); operator-pointed
fragrance-review projections still default `as_of` to today() (catch-up
pins); out-of-scope-surface ack convention; `datetime.utcnow()` deprecation
class in transcript writers.

## Proposed goal frame — Silver/Vault lane (owner ratifies at kickoff)

**Mission:** make Silver the trustworthy READ layer of the lake — every
silver record lineage-anchored and policy-fingerprinted, sibling
supersession EXPLICIT, every silver consumer enumerated and reading through
a defined selection rule, and the vault record shapes schema-versioned —
optimizing for behavioral signals, not artifact existence.

**Why this lane, why now (the predecessor's own findings argue it):**

1. Bronze consumption is closed; value now concentrates one layer up —
   product surfaces read silver (`sov_readout`, creator-profile
   `silver_metric_reader`, rollup producers), not bronze.
2. The seam's S3 behavior MULTIPLIES silver siblings by design: every
   policy bump re-derives fresh audit/silver/projection records. The
   predecessor proved consumers mishandle siblings — F-IGRC-001 was exactly
   a consumer selecting a STALE sibling via a lexical accident. Today no
   general supersession rule exists; every reader invents its own selection.
3. The weak-envelope residuals all live in silver-side record shapes (no
   schema version tokens) — the vault contract is where they get closed.
4. The doctrine→code machinery (seam helper, consumer gate, partition gate,
   pin gate) is hot and directly reusable one layer up.

**Behavioral signals (V-signals, drafts to ratify):**
- V1 lineage-closed: every committed silver record resolves to (raw anchor,
  deriving policy fingerprint) via `data_lake/silver_lineage.py` refs — no
  orphan silver.
- V2 selection-defined: for any (anchor, lane) with N siblings, one defined,
  tested rule names the current record; a policy bump changes what every
  reader sees, atomically per read (kills the F-IGRC-001 class generally).
- V3 consumer-enumerated: a silver census + a silver-reader contract gate
  (mirror of the consumer seam gate) — every reader of silver lanes is
  declared and uses the selection rule, never `lane_dir` free-walks.
- V4 vault-versioned: silver/vault record shapes carry schema version
  tokens (closing the weak-envelope class), pinned in the pin gate.
- V5 second-cycle-zero: silver derivation cadence (the bronze cadence
  runner already proves the deriving half).

**Starting census facts (from the tracked touchpoint baseline —
`EXPECTED_NON_RAW_LAKE_TOUCHPOINTS` in the producer gate is the
machine-checked source):** silver writers = `data_lake/silver_record.py`
(the helper), `cleaning/{fragrantica,basenotes,parfumo}_lake.py`,
`capture_spine/creator_profile_current/{silver,youtube_silver,tiktok_silver}_metric_producer.py`,
`cleaning/transcript_product_lake.py` (mentions record sets); silver/derived
readers = `capture_spine/.../silver_metric_reader.py` (lane_dir ×3),
`data_lake/sov_readout.py`, `runners/run_sov_extraction_quality_eval.py`,
`data_lake/derived_retrieval_views.py` (views), `instagram_metric_seed.py`
(derived walk). Verify by regenerating, never trust this copy.

**Unit queue after the bridge (owner-steerable):**
- (b) Silver census gating read: enumerate writers/readers from the live
  gates + code (NOT this handoff's copy), classify each reader's current
  selection behavior; bring the build-vs-classify ledger to the owner
  before writing code (the projection-sweep precedent: consumer tracing
  killed 5 of 6 planned builds).
- (c) Supersession/selection design: an owner-steered fork (high lock-in —
  a read-layer contract). Candidate shapes to weigh, not pre-decided:
  selection helper in `data_lake/` (read-side, like `consumption.py` was
  write-side) vs. supersession facts (append-only pointers) vs.
  latest-policy-fingerprint convention. Route through the assumption gate;
  probe with ONE reader (F-IGRC-001's `instagram_metric_seed` is the
  motivated candidate).
- (d) Vault schema-version tokens for the weak-envelope record shapes
  (closes that residual class; the pin gate already forces deliberateness).

## Standing workflow (inherit verbatim)

- Per implementation unit: fresh branch off origin/main;
  `workflow-assumption-gate` → `/fused`; full-suite validation via
  `--junitxml` + ElementTree parse with `ORCA_DATA_ROOT` cleared (PowerShell
  eats pytest summaries); **re-run tracked-scan gates AFTER committing new
  files** (the scanners read tracked source only — F-ASR-001 landing
  lesson); explicit `git push -u origin <lane>` (bare push is
  guard-blocked); owner merges PRs; never commit on a merged branch.
- Per unit: repo-mode cross-vendor delegated review commission (pin commit
  SHA + LF-blob SHA256s; labeled targets; non-Anthropic who-constraint;
  owner couriers; home-CA adjudicates with fresh verification, class sweep,
  byte/scope checks, own full-suite run; adjudication record under
  docs/review-outputs/ passing `check_review_output_provenance.py --strict`
  with the canonical review_use_boundary phrasing).
- Commission stakes worth naming every time: gate soundness (F-SH-001:
  verify visible USE of failure channels, never mere imports), engine
  identity vs enveloped policy (F-ASR-001), consumer-facing correctness
  (F-IGRC-001), envelope completeness (F-FRAG-001/F-IGRC-002).

## Security rules (verbatim, still binding)

Never write to `F:\orca-data-lake`. Live-lake READS need a fresh owner
grant each turn (the permission classifier enforces this — do not work
around it). LLM/ASR executions are owner-gated per turn (the ASR path is
non-API local compute but still owner-operated cadence).

## Anti-signals (inherit)

Green tests without the behavioral signal; docs asserting sync; any
live-lake claim without a granted read; a gate that can be satisfied by
import-only presence; "merged" claims not re-verified against GitHub;
absence/build-state claims not confirmed against the primary source.
