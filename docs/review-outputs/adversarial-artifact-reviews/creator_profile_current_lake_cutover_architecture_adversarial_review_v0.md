# Creator Profile Current Lake Cut-Over Architecture Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: adversarial architecture review
scope: >
  Source-backed adversarial architecture review of PR #488's creator_profile_current
  lake cut-over proposal and bounded code context. Reviews the design only and
  does not patch source, implement code, validate readiness, or decide acceptance.
use_when:
  - Adjudicating the creator_profile_current lake cut-over architecture proposal before ratification.
  - Revising the frozen rollup snapshot, live-lake reconciliation, latest-selection, or provenance design.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md
  - docs/prompts/reviews/creator_profile_current_lake_cutover_delegated_adversarial_architecture_review_prompt_v0.md
  - orca-harness/capture_spine/creator_profile_current/materialize.py
  - orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/data_lake/root.py
branch_or_commit: claude/creator-lake-cutover-architecture@a058e4983c30fb7f4da56aabc3b4ddccf076c341
stale_if:
  - The proposal is revised or superseded.
  - select_latest_rollup_per_account, silver_metric_snapshot.py, or the live-lake reconciliation gate is implemented.
  - DataLakeRoot availability/discovery semantics or creator raw source_family values change.
```

## Findings

### AR-01 - Proposed lake-wide discovery misses the actual raw packet families

Severity: blocker

Precise claim attacked: "Lake-wide discovery: `list_available(source_family=\"social_media\")` -> per packet `lane_dir(...)`. No new lake API." The proposal also says YouTube fold-in is platform-keyed and purely additive.

Evidence:
- Proposal names `list_available(source_family="social_media")` as the discovery route for rollup records, with no new lake API: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:160-166`.
- `DataLakeRoot.list_available` filters raw availability entries by the raw packet manifest's `source_family`, not by derived Silver record metadata: `orca-harness/data_lake/root.py:893-903`.
- IG reels-grid packets are written with `source_family="instagram_creator"`: `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py:297-303`; the IG projection code enforces the same family: `orca-harness/source_capture/ig_reels_grid_projection.py:1-5` and `orca-harness/source_capture/ig_reels_grid_projection.py:217-220`.
- YouTube watch and caption packets use `source_family="youtube"`: `orca-harness/source_capture/youtube_watch_packet.py:178-184` and `orca-harness/source_capture/transcript/caption_packet.py:113-117`.

Strongest defense: the proposal uses "social_media" as a conceptual umbrella, and the Silver creator metric records themselves carry `_SOURCE_FAMILY = "social_media"` in the producer.

Why that defense fails: the proposed discovery call happens before reading derived records. It is filtering raw packet availability, and the available raw families are platform-specific. A conceptual umbrella does not exist in the current availability index, so the live selector can find zero anchors, miss IG/YT anchors, or require undocumented out-of-band platform enumeration.

Recommended design change: bind discovery to current raw families explicitly, for example `instagram_creator` and `youtube`, or introduce a real derived-record discovery/index surface before claiming "no new lake API." The live gate must fail closed on an empty or incomplete expected account set; it must not treat "no discovered rollups" as a valid latest set.

Minimum closure condition: the proposal names an implemented discovery contract that can find the current IG and future YT rollup records from the real lake and fails on missing expected accounts.

Next authorized action: home model adjudicates and revises the proposal; this review is not patch authority.

Patch queue: not authorized.

### AR-02 - The accepted staleness residual still leaves manual staleness as the operating mode

Severity: blocker

Precise claim attacked: the architecture "actually retires manual staleness" through an operator-regenerated snapshot and live-lake reconciliation gate.

Evidence:
- The proposal's stated goal is to make metrics derive from Silver records so the registry stops going manually stale: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:40-46`.
- It acknowledges real-lake drift is catchable only off-CI: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:69-75`.
- The live-lake gate is green-by-skip when `ORCA_DATA_ROOT` is unset and load-bearing only on an operator box or future scheduled job: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:115-120`.
- The proposal makes the scheduled job an opt-in follow-on, not part of the recommended cut-over: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:186-190`.
- The cited YouTube precedent is explicitly skipped when `ORCA_DATA_ROOT` is absent: `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py:116-121`.

Strongest defense: the proposal is honest that CI cannot see the external lake, and a committed snapshot plus operator gate is the only deterministic seam available.

Why that defense fails: honesty about the residual is not the same as closing it. If regeneration and reconciliation remain manual/optional, the registry can still go stale exactly as before; only the source of stale numbers changes from hand-kept seed rollups to hand-regenerated snapshots. The fitness reference requires either actually retiring manual staleness or naming precisely where it does not. The proposal names the residual, but then still recommends the snapshot cut as if staleness retirement is achieved.

Recommended design change: make a freshness trigger part of the accepted v0, not a follow-on. That can be a required operator release gate with a durable receipt before merging snapshot updates, or a scheduled operator-box job that fails loudly and opens/updates a visible issue. If the owner declines that, downgrade the architecture claim to "lake-verifiable committed snapshot" rather than "manual staleness retired."

Minimum closure condition: the proposal binds a non-optional live-lake freshness mechanism, its failure surface, cadence/trigger, and required evidence before the cut-over can claim staleness retirement.

Next authorized action: home model adjudicates the owner fork and revises the proposal.

Patch queue: not authorized.

### AR-03 - The CI equivalence gate is a no-drift adapter test, not a lake-sourced correctness proof

Severity: major

Precise claim attacked: the first IG snapshot being byte-equal to today's seed rollups makes the regenerated view byte-identical and is "the cut-over's correctness proof."

Evidence:
- The proposal calls the seed-equal snapshot the cut-over correctness proof: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:96-100`.
- The CI equivalence gate asserts producer -> reader reconstruction equals committed seed rollups equals committed snapshot and "proves internal consistency": `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:111-114`.
- The producer reuses the existing Instagram seed computation from projection files: `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py:112-116`.
- The record contract states the producer does not compute metrics and rollup numbers equal the seed computation exactly: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md:43-45` and `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md:105-111`.
- Existing reader tests prove the temp-lake round trip equals the seed rollup the producer wrapped, while noting the committed view, seeds, and CI are untouched: `orca-harness/tests/unit/test_creator_metric_silver_reader.py:1-10` and `orca-harness/tests/unit/test_creator_metric_silver_reader.py:124-133`.

Strongest defense: the proposal itself says the CI gate proves internal consistency, and that is a real requirement.

Why that defense fails: the same paragraph also calls byte equality the cut-over's correctness proof. The gate can detect adapter drift, shape drift, and snapshot/seed divergence, but it cannot prove the committed snapshot was generated from the live external lake or is current relative to the append-only lake. A stale but internally consistent snapshot can pass.

Recommended design change: split the gate names and claims. Keep the CI gate as `adapter_no_drift_gate` or `snapshot_seed_equivalence_gate`. Make live-lake freshness a separate gate with a required receipt before any "lake-fed" or "correctness proof" claim. The proposal should not let CI equality stand in for source freshness.

Minimum closure condition: the proposal stops calling CI equivalence a cut-over correctness proof and binds the live-lake gate as the only proof of external-lake freshness.

Next authorized action: home model revises the proof language and gate responsibilities.

Patch queue: not authorized.

### AR-04 - Latest-per-account selection trusts a producer timestamp that can regress

Severity: major

Precise claim attacked: select max `payload.observation.computed_at`, tie-break `record_id` descending, and fail closed on same-`computed_at` content conflict.

Evidence:
- The proposed rule selects max computed_at and says `computed_at` equals producer-run `generated_at_utc`: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:122-137`.
- The producer accepts `generated_at_utc` from the caller and feeds it into seed generation: `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py:100-116`.
- The rollup record copies `seed_rollup["computed_at"]` into both `observed_at`/`captured_at` and payload `computed_at`, while `record_id` is generated separately: `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py:266-282` and `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py:307-318`.
- `generate_ulid()` uses the current wall-clock millisecond plus randomness: `orca-harness/harness_utils.py:111-114`.
- `DataLakeRoot.append_record` is write-once but does not add an append timestamp or monotonic sequence that the selector can use: `orca-harness/data_lake/root.py:559-575`.

Strongest defense: same-`computed_at` different-content records fail closed, so record-id ordering is not allowed to hide a real same-time conflict.

Why that defense fails: the harder failure is not same-time conflict. It is non-monotonic or manually supplied `generated_at_utc`: a later append can carry an older `computed_at`, and then max-computed_at selects the older semantic timestamp forever. The live gate recomputes the same flawed selection, so it can agree with a stale snapshot. ULID order is only useful if the design says append order, not semantic computation time, defines latest; the proposal does not say that.

Recommended design change: define latest using a lake-controlled append/run freshness field or a snapshot-run manifest, and fail closed when per-account `computed_at` regresses relative to a newer append/run record. If `computed_at` remains the semantic metric window timestamp, it should not be the only latest selector.

Minimum closure condition: the proposal defines an ordering that cannot silently ignore a newer appended rollup with a regressed or manually reused `computed_at`.

Next authorized action: home model revises the latest-selection rule and its tests.

Patch queue: not authorized.

### AR-05 - The "smallest input swap" under-scopes the view provenance/schema migration

Severity: major

Precise claim attacked: `_collect_metric_rollup_records` can read snapshot rollups while downstream profile-building remains unchanged, and `source_inputs`/`source_drill_back` can simply flip from seed to snapshot pointers with stronger provenance.

Evidence:
- The proposal says the snapshot carries `source_record` blocks and materialize downstream profile-building is unchanged; view `source_inputs` and `source_drill_back` flip to the snapshot pointer and "now resolves to a real lake record content-hash": `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:83-95`.
- Current materialization builds a `metric_rollup_pointer` from `metric_seed_pointer` and wrapper name: `orca-harness/capture_spine/creator_profile_current/materialize.py:206-218`, then writes `metric_seed_pointer` into `source_drill_back`: `orca-harness/capture_spine/creator_profile_current/materialize.py:254-262`.
- The validator only allows `identity_ledger_pointer`, `metric_rollup_pointer`, `metric_seed_pointer`, and `source_metric_observation_ids` in `source_drill_back`: `orca-harness/capture_spine/creator_profile_current/validation.py:137-144` and `orca-harness/capture_spine/creator_profile_current/validation.py:359-375`.
- The validator also only allows source inputs with `source_pointer`, `sha256`, and `role`: `orca-harness/capture_spine/creator_profile_current/validation.py:42` and `orca-harness/capture_spine/creator_profile_current/validation.py:220-231`.

Strongest defense: the richer lake `source_record` can live in the snapshot artifact, while the committed view only points into the snapshot.

Why that defense only partially holds: that can be a valid design, but the proposal has not specified it. As written, it implies the view's drill-back itself becomes lake-record aware while also claiming downstream shape stays unchanged. The existing field name `metric_seed_pointer` becomes semantically false if it points to a snapshot, and any attempt to add `source_record` to the view would be rejected by the validator.

Recommended design change: explicitly define the v0 provenance surface. Either keep lake record details solely inside the snapshot and rename/extend the view pointer fields accordingly, or update the view schema/spec/tests to carry `metric_snapshot_pointer` and source-record references. Do not smuggle a snapshot pointer through a field still named `metric_seed_pointer`.

Minimum closure condition: the proposal names the exact view/source-drill-back schema delta or explicitly states that the view only points to the snapshot while lake record provenance is resolved by opening the snapshot.

Next authorized action: home model revises the materialize/schema scope before implementation.

Patch queue: not authorized.

### AR-06 - YouTube fold-in is not "zero registry changes" once the seed oracle disappears

Severity: major

Precise claim attacked: YouTube fold-in is "purely additive" with "zero registry changes"; the gates extend automatically.

Evidence:
- The proposal says adding a YouTube snapshot costs one producer plus one snapshot file and zero registry changes: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:151-158`.
- Current view tests are explicitly built around current YouTube and Instagram seed files: `orca-harness/tests/unit/test_creator_profile_current_static_view.py:214-221` and `orca-harness/tests/unit/test_creator_profile_current_static_view.py:224-234`.
- The current view expects 30 YouTube plus 3 Instagram accounts and only three observed engagement-rate profiles, while YouTube engagement remains unavailable: `orca-harness/tests/unit/test_creator_profile_current_static_view.py:134-175` and `orca-harness/tests/unit/test_creator_profile_current_static_view.py:264-282`.
- The migration plan itself says YouTube repeats the IG cut-over and retires the YT seed from the rollup path later: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:201-206`.

Strongest defense: if YouTube emits exactly the same rollup shape, `materialize` can remain platform-agnostic at the rollup consumption layer.

Why that defense fails as stated: platform-agnostic consumption is not the whole registry surface. The cut-over still changes default runner inputs, source hashes, view source inputs, drift-witness strategy, and the no-drift oracle once the YouTube seed is no longer authoritative for rollups. Since there is no YouTube producer in this PR, the gate extension is an assumption, not an automatic property.

Recommended design change: treat YouTube as a second cut-over stage with its own producer contract, snapshot equivalence/freshness gates, and seed-retirement rule. The proposal may say "no profile-building branch expected," but should not claim zero registry changes or automatic gate extension.

Minimum closure condition: the proposal separates IG v0 acceptance from YouTube fold-in acceptance and names what evidence replaces the YouTube seed oracle.

Next authorized action: home model revises the YouTube scope language and owner fork.

Patch queue: not authorized.

### AR-07 - Reversibility is asserted by implication but not designed

Severity: minor

Precise claim attacked: the architecture is low-lock-in because the snapshot is a flat step toward Creator Vault and materialize changes by one input swap.

Evidence:
- The proposal frames the materialize change as the smallest input swap: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:89-95`.
- It says the flat snapshot can later be promoted without reworking materialize: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:172-180`.
- The migration changes test expected paths and `--check`: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:192-205`.

Strongest defense: as a design proposal, it does not need a full rollback runbook.

Why that defense only partially holds: the prompt explicitly asks to attack reversibility and lock-in. Once the view source pointers, snapshot files, runner defaults, and tests flip, reverting is not just one function input if the snapshot has become the committed source-of-record for metrics. The one-way parts are manageable, but unnamed.

Recommended design change: add a short rollback section naming which files/claims revert together, what happens to committed snapshots, and whether live-lake freshness receipts remain historical evidence or are discarded.

Minimum closure condition: the proposal names the reversible surfaces and the non-reversible evidence history before calling the cut low-lock-in.

Next authorized action: home model decides whether to patch proposal prose.

Patch queue: not authorized.

## Overall Verdict

`needs_architecture_rework`

Load-bearing reason: the recommended snapshot cut is directionally defensible, but the design has two pre-ratification blockers. First, the proposed lake-wide discovery filter does not match current raw packet source families, so the live selector/gate may not find the records it is supposed to certify. Second, the freshness mechanism that would actually retire manual staleness is left manual or follow-on, so the architecture currently achieves a lake-verifiable committed snapshot, not durable staleness retirement.

Scope-fork opinion: do not retreat to certify-only; that would knowingly keep the registry seed-fed. Do not jump to full Creator Vault now; the current mapping contract already names that as the end state, and building it before proving snapshot discovery/freshness would add lock-in around an unproven selector. The right cut is still a frozen rollup snapshot, but only after the discovery contract and non-optional freshness trigger are redesigned.

## review_summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_lake_cutover_architecture_adversarial_review_v0.md
  recommendation: reject
  reviewed_by: gpt-5-codex
  authored_by: unrecorded
  de_correlation_bar: cross_vendor_discovery
  verdict: needs_architecture_rework
  blocker_count: 2
  major_count: 4
  minor_count: 1
  biggest_single_risk: "The live-lake discovery path filters on source_family=social_media, but current raw packet availability uses platform-specific families, so the freshness gate can miss the records it must certify."
  scope_fork_opinion: "Frozen snapshot remains the right v0 shape after redesign; certify-only under-delivers and full Creator Vault now is premature lock-in."
  blocking_findings:
    - AR-01
    - AR-02
  advisory_findings:
    - AR-03
    - AR-04
    - AR-05
    - AR-06
    - AR-07
  prior_findings_remediated: []
  next_action: "Home model should revise the proposal's discovery and freshness-trigger design before ratification or implementation scoping."
```

## Source and Authority Notes

orca_start_preflight:
- agents_read: yes, supplied in current task context.
- overlay_read: yes, `.agents/workflow-overlay/README.md` read.
- source_pack: custom S3 target deepening.
- edit_permission: docs-write for this review report only; reviewed prompt/proposal/code are read-only.
- target_scope: adversarial architecture review of PR #488 proposal and bounded code context.
- dirty_state_checked: yes.
- blocked_if_missing: report path, proposal, prompt, target branch/PR head, or bounded code pack.

Authority and output binding:
- Active branch/worktree reviewed: `claude/creator-lake-cutover-architecture` in `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-profile-silver-repoint`.
- PR #488 confirmed through GitHub connector: open, base `main` at `ccdc3bb4d914c4999db72572e21b0f45858cc9cb`, head `claude/creator-lake-cutover-architecture` at `a058e4983c30fb7f4da56aabc3b4ddccf076c341`, changed files are the proposal and review prompt.
- Local branch and origin ref both resolved to `a058e4983c30fb7f4da56aabc3b4ddccf076c341`.
- Dirty source note: target worktree had one unrelated untracked file, `docs/prompts/handoffs/youtube_creator_metric_silver_producer_build_handoff_v0.md`; it was not read or relied on.
- Output mode: filesystem-output, required path named by prompt.
- Validation evidence: ran `python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\orca_creator_lake_review_pytest orca-harness\tests\unit\test_creator_metric_silver_producer.py orca-harness\tests\unit\test_creator_metric_silver_reader.py orca-harness\tests\unit\test_creator_profile_current_static_view.py`; result: `27 passed`. This confirms existing current-code baselines only; it is not validation, readiness, or architecture acceptance.

Source-read ledger:
- `docs/prompts/reviews/creator_profile_current_lake_cutover_delegated_adversarial_architecture_review_prompt_v0.md`: commission, fitness reference, output contract; clean at PR head.
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md`: reviewed proposal; clean at PR head.
- `orca-harness/capture_spine/creator_profile_current/materialize.py`: current materializer/source-drill-back behavior; clean at PR head.
- `orca-harness/capture_spine/creator_profile_current/silver_metric_reader.py`: current reader scope and anchor-based scanning; clean at PR head.
- `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`: current producer timestamp, content hash, and lineage behavior; clean at PR head.
- `orca-harness/data_lake/root.py`: `DataLakeRoot.resolve`, `append_record`, `lane_dir`, and `list_available` semantics; clean at PR head.
- `orca-harness/tests/unit/test_creator_profile_current_static_view.py`, `orca-harness/tests/unit/test_creator_metric_silver_producer.py`, `orca-harness/tests/unit/test_creator_metric_silver_reader.py`, `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py`: current gates and skip pattern; clean at PR head.
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md` and `creator_metric_silver_record_contract_v0.md`: adjacent architecture contracts for end-state Creator Vault and creator metric Silver records; clean at PR head.
- Targeted supporting code reads: `orca-harness/harness_utils.py`, `orca-harness/runners/run_creator_profile_current_materialize.py`, `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`, `orca-harness/source_capture/ig_reels_grid_projection.py`, `orca-harness/source_capture/ig_reels_behavioral_lake.py`, `orca-harness/source_capture/youtube_watch_packet.py`, `orca-harness/source_capture/transcript/caption_packet.py`; clean at PR head.

Not-proven boundaries:
- This review does not prove the proposal is accepted, rejected by the owner, validated, ready to implement, or ready to merge.
- This review did not read or reconcile the real external lake at `ORCA_DATA_ROOT`.
- This review did not inspect untracked handoff material in the target worktree.
- This review did not produce patch-queue entries or authorize code/document patches.

Review-use boundary: findings are decision input only. They are not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized by the owner/home model.
