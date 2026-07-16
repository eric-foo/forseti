# TikTok Grid Longitudinal Silver — Delegated Adversarial Review-and-Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code and artifact review-and-patch commission
scope: >
  Different-vendor review and bounded patch pass for the TikTok grid-only
  Bronze admission, packet-grain Silver observation set, exact-policy history
  reader, consumption seam, tests, registrations, and documentation-only
  Instagram/YouTube follow-on.
use_when:
  - Reviewing branch codex/topfrag-silver-analytics after the implementation commit.
authority_boundary: retrieval_only
```

## Forseti Start Preflight

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: current branch diff from b6a3903c84ed84ac89499d790ff0347c40bd07ac
  edit_permission: bounded implementation-authorized review patch
  target_scope: the 21 named implementation, registration, test, and follow-on files below
  dirty_state_checked: yes; authoring state contains exactly the named change set plus this prompt; controller execution requires a clean committed branch tip
  blocked_if_missing: exact target branch/ancestry, clean controller-start state, named targets, pinned TopFrag artifacts, required review lanes, or validation route
```

## Goal And Success Signal

Goal: adversarially verify and, only for confirmed defects, patch the smallest
complete TikTok longitudinal grid path so source-native grid observations are
preserved in immutable Bronze, deterministically materialized as one strict
Silver observation set per packet, and retrieved across captures by native
video ID under an exact policy fingerprint.

Done means the controller has inspected the real diff and relevant owning
sources, reported coverage-first findings, applied only bounded fixes, rerun the
named validation, and returned neutral citations, diff, verdict, and residuals
for Chief Architect adjudication. No returned change is kept automatically.

## Lane And Actor Binding

- target_kind: `delegated_mixed_review_and_patch`
- access: `repo`
- code_review_lane: `workflow-code-review`
- artifact_review_lane: `workflow-adversarial-artifact-review`
- mode: `base-subagent`
- operating_contract: `.agents/workflow-overlay/delegated-review-patch.md`
- author_home_model_family: OpenAI / GPT-5 Codex
- controller_model_family: `operator_to_fill`; it must be a non-OpenAI vendor/family
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- de_correlation_status: satisfied only after the controller records a family different from OpenAI
- no tester/testee shortcut: an OpenAI-family receiver returns
  `BLOCKED_CONTROLLER_NOT_DECORRELATED`; it does not self-review or spawn a
  replacement reviewer.

## Target-State Preflight

- worktree: `C:\Users\vmon7\.codex\worktrees\f75f\orca`
- branch: `codex/topfrag-silver-analytics`
- required ancestry/review base: `b6a3903c84ed84ac89499d790ff0347c40bd07ac`
- review range: that base through branch HEAD observed at controller start
- controller-start dirty state: clean; no untracked files
- environment baseline:
  `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md#environment_baseline`

If the launch checkout differs, inspect registered worktrees and use the unique
worktree satisfying this branch and ancestry. Do not substitute a summary,
context pack, recreated copy, alternate branch, or live data lake.

## Editable Scope

The controller may patch only these submitted targets:

```text
[follow-on] docs/workflows/social_grid_longitudinal_followon_v0.md
[reader] forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py
[producer] forseti-harness/capture_spine/creator_profile_current/tiktok_grid_observation_producer.py
[registry] forseti-harness/data_lake/inventory.py
[registry] forseti-harness/data_lake/lake_touchpoint_inventory_v0.json
[registry] forseti-harness/data_lake/lane_registry.py
[schema] forseti-harness/data_lake/silver_record.py
[cadence] forseti-harness/runners/run_seam_cadence.py
[bronze-runner] forseti-harness/runners/run_source_capture_tiktok_grid_packet.py
[silver-runner] forseti-harness/runners/run_tiktok_grid_observation_producer.py
[onboarding] forseti-harness/source_capture/tiktok/creator_onboarding.py
[bronze] forseti-harness/source_capture/tiktok/grid_packet.py
[selection] forseti-harness/source_capture/tiktok/grid_video_selection.py
[contract-test] forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
[contract-test] forseti-harness/tests/contract/test_catchup_runner_seam_coverage.py
[contract-test] forseti-harness/tests/contract/test_silver_reader_selection_gate.py
[unit-test] forseti-harness/tests/unit/test_silver_record.py
[unit-test] forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
[unit-test] forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py
[unit-test] forseti-harness/tests/unit/test_tiktok_grid_packet.py
[unit-test] forseti-harness/tests/unit/test_tiktok_grid_video_selection.py
```

The durable review report may be created at the output path below. Everything
else is read-only and flag-only. Do not widen into live capture, scheduler
deployment, live-lake writes, Creator Registry, SQL/Parquet, schema migration,
backfill, cross-platform implementation, velocity/virality judgment, Gold, or
unrelated cleanup. A correct fix requiring architecture or off-scope edits
returns `NEEDS_ARCHITECTURE_PASS`, reverts partial controller edits, and reports
findings only.

## Required Reads And Method Order

Read before strict findings:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- targeted sections of `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/workflows/topfrag_silver_lake_mechanics_handoff_v0.md`
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
- the complete diff from the required base and every submitted target
- directly called packet, lake-root, consumption, lineage, and existing Silver
  reader/producer sources where a candidate finding depends on them

Apply `workflow-deep-thinking` after source loading. Apply
`workflow-code-review` to code and tests, and
`workflow-adversarial-artifact-review` to the follow-on document's factual and
scope claims. If a required lane is unavailable, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Fitness Contract

The required behavior is:

1. TikTok onboarding retains every creator-owned grid row and its exact
   source-visible `stats`, including real zeros and rows ineligible for ranking.
2. Ranking excludes unusable rows without erasing them; it fails only when too
   few eligible rows can satisfy the requested selection count, and its changed
   policy version is explicit.
3. The grid-only Bronze runner admits an already-captured complete grid without
   opening TikTok and preserves its supplied bytes exactly, bound to creator
   handle, native video IDs, canonical video URLs, and a source-backed UTC
   capture time.
4. One eligible Bronze grid packet produces exactly one atomic strict
   `MetricObservationSet` under a deterministic record ID and content hash.
5. Rows key identity by TikTok video ID, never grid position; capture time comes
   from Bronze, and every value retains source-field provenance.
6. Literal zero is observed zero. Missing, invalid, or negative source metrics
   carry null value plus an explicit non-observed reason and are never
   zero-filled.
7. Silver lineage names the exact packet, file, stored-byte hash, source
   surface, producer schema, and policy fingerprint.
8. The seam acknowledges target packets only after byte readback and validation,
   explicitly acknowledges non-target TikTok packets, exposes failures without
   acknowledgement, and is idempotent on rerun.
9. The reader discovers anchors only through rebuildable availability, resolves
   exact deterministic authority records by key, requires an explicit policy
   fingerprint, validates schema/content hash/lineage, orders history by capture
   time, and fails on ambiguous equal-time siblings rather than guessing.
10. The Instagram/YouTube artifact documents only confirmed current seams and
    future changes/success signals; it makes no implementation or live-readiness
    claim.

Attack this as an alignment axis, not a pass-if-matches checklist.

## Adversarial Questions

- Can an unrelated creator row, duplicate native ID, URL mismatch, incomplete
  grid, malformed timestamp, or altered preserved body enter Bronze?
- Can source-visible stats be erased or transformed by the onboarding change,
  especially zero, missing, non-integer, or future unknown fields?
- Can selection accidentally rank an ineligible row or silently shrink the
  requested selection?
- Can a target packet be acknowledged before the Silver bytes and exact lineage
  are verifiably durable? Can a non-target packet loop forever?
- Can malformed row count, duplicate subject, posture/value coupling, source
  field, policy fingerprint, content hash, or raw anchor pass validation?
- Can the reader return a stale/wrong-policy sibling, consult a non-authoritative
  derived view, collapse two native IDs, fabricate a missing day, or choose an
  equal-time winner?
- Does the packet-grain set materially weaken the existing Silver envelope or
  create an unnecessary platform-specific core abstraction?
- Are inventory, lane, cadence, Bronze-writer, seam-consumer, and reader-selection
  gates complete and generated inventory byte-identical?
- Does the follow-on overstate Instagram or YouTube Bronze metric availability,
  especially YouTube `starRating` and comment count?
- Do tests prove lineage, policy, counts, idempotency, failure-before-ack,
  missing-versus-zero, tamper failure, and longitudinal retrieval rather than
  only a happy-path write?

Report every issue found with severity (`critical|major|minor`) and confidence
(`high|medium|low`). Each actionable finding includes evidence, impact,
`minimum_closure_condition`, and `next_authorized_action`. Put defeated
candidates in `considered_and_defended`. Use searchable target labels on
findings, citations, and diff hunks.

## Validation

Authoring-lane evidence to verify, not inherit:

- focused TikTok/Silver unit suite: 95 passed
- pinned TopFrag scratch: 1 passed; 32 Bronze rows, 32 Silver rows, 32 native-ID
  history points, exact pinned raw hash, current policy fingerprint, empty
  pending surface, empty idempotent rerun
- five pinned TopFrag staging SHA-256 values matched the handoff
- tracked-source registration/contract subset: 45 passed after staging the full
  implementation surface; controller must rerun from the clean committed tip
- pre-existing TikTok Silver producer/analytics/comment-attention regressions,
  shared Silver snapshot/discovery tests, and the complete contract directory:
  pass with two pre-existing skips
- Silver lane registry strict hook: pass
- `git diff --check`: pass

After any patch, and before a verdict, run at least:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q --basetemp pytest_grid_review_unit forseti-harness/tests/unit/test_silver_record.py forseti-harness/tests/unit/test_tiktok_creator_onboarding.py forseti-harness/tests/unit/test_tiktok_grid_video_selection.py forseti-harness/tests/unit/test_tiktok_grid_packet.py forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py forseti-harness/tests/unit/test_tiktok_batch_admission.py
python -m pytest -p no:cacheprovider -q --basetemp pytest_grid_review_contract forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py forseti-harness/tests/contract/test_catchup_runner_seam_coverage.py forseti-harness/tests/contract/test_seam_cadence_coverage.py forseti-harness/tests/contract/test_silver_reader_selection_gate.py forseti-harness/tests/contract/test_data_lake_inventory_gate.py
python .agents/hooks/check_silver_lane_registry.py --strict
git diff --check
```

Every command reports pass, fail, blocked, or not run with reason. Missing
tooling and failed checks remain failures, never synthetic success.

## Mini God Tier Residuals To Challenge, Not Silently Widen

- This is scratch proof, not live cadence or 2,500-creator throughput proof.
- Availability scanning is sufficient authority-preserving retrieval now; no SQL
  materialization or performance claim is made.
- Explicit supersession edges are deferred until a second policy exists; exact
  policy selection and collision failure are implemented now.
- The grid-only Bronze admission checks artifact-internal creator/video binding,
  not independent source-served authorship of an operator-supplied artifact.
- Instagram and YouTube adapters are documented, not implemented.
- Missing days and videos outside a bounded window remain sparse history, not
  negative observations or carried-forward values.

Treat a residual as material only when it breaks the bounded fitness contract;
otherwise report it without expanding scope.

## Output Contract

Output mode: `review-report`.

Write the durable report to:

`docs/review-outputs/tiktok_grid_longitudinal_silver_delegated_adversarial_review_v0.md`

Record `reviewed_by` and `authored_by` from observed provenance; use
`unrecorded` rather than fabrication. Include findings first,
considered-and-defended candidates, bounded working-tree diff, validation
evidence, verdict, and residual risks. Run the applicable provenance checker.

Return a compact courier summary. Findings, citations, diff, verdict, and
residuals are claims for the Chief Architect to accept, modify, or reject. The
Chief Architect adjudicates every material change before anything is kept.

## Lifecycle Hard Stop

Do not commit, push, create or update a PR, merge, stash, reset, clean the
worktree, remove a worktree, or perform repository hygiene. Do not run live
TikTok/browser capture, write a live data lake, or mutate Creator Registry.
Stop after the bounded patch, validation, durable report, and courier summary.
