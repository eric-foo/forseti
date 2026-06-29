# Creator Metric Silver Producer Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: adversarial code review-and-patch report
scope: >
  Cross-vendor delegated review-and-patch result for the creator-metric Silver
  producer, its unit test, and producer-owned MetricRollupObservation contract.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 Codex
authored_by: Anthropic Claude (version unrecorded)
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: null
reviewed_branch: claude/creator-silver-metric-producer
reviewed_head_for_targets: c862c42f1098b1ea2207ff1f08d1634868856414
review_prompt_head: 729845c3590ab0dbe3888f7551cf0d92195a8a06
reviewed_diff: 74373bb093d3cecd11f5e24a9d2dd2cecbc96223..c862c42f1098b1ea2207ff1f08d1634868856414
report_written_at: 2026-06-30
```

## 1. Commission, Lane Binding, And Receipt

Commission: execute `docs/prompts/reviews/creator_metric_silver_producer_delegated_adversarial_code_review_patch_prompt_v0.md` as a repo-mode, delegated code review-and-patch pass.

Target set:

- `[silver-metric-producer]` `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
- `[silver-metric-producer-tests]` `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
- `[creator-metric-silver-contract]` `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`

Authority: patch-only inside the three named files. All Silver Vault contracts, lake writer, seed computation, validators, product specs, overlay files, source ledgers, real lake writes, live capture, commits, pushes, and PR work stayed read-only / flag-only.

Actor receipt: author/home family is Anthropic / Claude; controller family is OpenAI / GPT-5 Codex. The cross-vendor discovery bar is satisfied for this review. This is a who-constraint, not a runtime model recommendation.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

Required method sources were reference-loaded before task-source analysis: `workflow-delegated-review-patch`, `workflow-deep-thinking`, `workflow-code-review`, and `workflow-adversarial-artifact-review`.

Required task sources were loaded from `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer`: `AGENTS.md`, `.agents/workflow-overlay/README.md`, `source-loading.md`, `review-lanes.md`, `delegated-review-patch.md`, `prompt-orchestration.md`, `decision-routing.md`, `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`, the pinned target diff, the three target files, Silver Vault record/layout contracts, `fragrantica_lake.py`, `data_lake/root.py`, `instagram_metric_seed.py`, the Instagram seed JSON, `validation.py`, and `creator_profile_current_lake_native_record_mapping_v0.md`.

No required source was missing. Excluded by commission: unrelated review outputs, all prompt files, all product files, all data-lake directories, live capture artifacts, external workflow source, and all non-target code except the named reference files.

## 3. Findings

### F1 - major - `[creator-metric-silver-contract]` / `[silver-metric-producer]` - Patched

Location: `creator_metric_silver_record_contract_v0.md` Posture rule; `silver_metric_producer.py` `build_metric_rollup_record` payload shape.

Issue: The original target intentionally reused `metric_posture.kind: observed` for computed rollup aggregates. That is defensible only if consumers can see, in-band, that the value is a computed aggregate whose posture means source-input support, not raw source visibility of the aggregate itself. The original record had `payload_kind: MetricRollupObservation`, `rollup_kind`, `calculation_recipe_version`, and `derived_refs`, but no explicit posture-semantics marker. A downstream consumer extracting metric posture from `metric_rollups` could misread `observed` as raw observed aggregate value.

Evidence:

- Silver Vault metric observations define `observed` as value-present / no reason and require missing/not-attempted states to be posture + reason, not zero (`core_spine_v0_data_lake_silver_vault_record_contract_v0.md`, Metric Observation Records).
- The creator mapping says per-account/window rollups are computed from MetricObservation records and must carry recipe, source ids, sample support, and limitations (`creator_profile_current_lake_native_record_mapping_v0.md`, Metric Derivation Rule).
- The seed emits computed `average_views`, `median_views`, `engagement_rate`, `average_like_count`, and `average_comment_count` with posture `observed`, while `posting_cadence` and `recent_velocity` are `not_attempted` (`instagram_metric_seed.py` and `instagram_reels_creator_metric_seed_v0.json`).
- The original producer copied the seed posture into each rollup metric without adding a local derivation/posture-semantics marker.

Impact: Without the marker, the new producer-owned `MetricRollupObservation` schema could blur the raw-observed versus computed-derived boundary even while otherwise preserving lineage. That is the highest-risk design seam in this target.

Minimum closure condition: Every rollup record must carry explicit in-band derivation semantics stating that the rollup is computed from source MetricObservation records and that `metric_posture` describes source-input support, not raw aggregate visibility.

Next authorized action: Patch the three target files only; do not change the Silver Vault posture vocabulary or validator.

Patch applied: Yes. The producer now emits `payload.observation.derivation` with `kind: computed_metric_rollup`, `source_record_ref_kind: derived_refs`, `metric_posture_semantics: source_input_support_not_raw_aggregate_visibility`, and the calculation recipe version. The contract defines the marker as required, and the unit test asserts it.

### F2 - major - `[silver-metric-producer]` / `[silver-metric-producer-tests]` / `[creator-metric-silver-contract]` - Patched

Location: `silver_metric_producer.py` `_observation_subject` and `_rollup_subject`; `test_creator_metric_silver_producer.py` subject-shaping coverage; contract accepted residuals.

Issue: The original producer could emit an `entity_key` with `native_id: null` for a malformed content metric observation if `content_id_or_none` was absent, and could emit a rollup account subject with `native_id: null` if account-handle derivation broke. The contract said v0 omits entity/relationship records and relies on self-describing `entity_key` refs, so a missing native id makes the subject under-identified.

Evidence:

- The producer originally assigned public content object `native_id` from `seed_observation.get("content_id_or_none")` and rollup account `native_id` from `account_handle` without fail-closed checks.
- The seed computation skips missing content ids for rollup aggregation, but still emits metric observations for source rows; therefore the producer can encounter a content observation with no native id.
- The lake-native mapping permits entity-key subjects but relies on metric observations and rollups preserving safe subject identity and source refs.

Impact: A malformed Silver record with a null subject key could pass the original producer tests and later be indistinguishable from a weakly identified subject rather than failing at the producer boundary.

Minimum closure condition: The producer must fail closed before emitting any account or content `entity_key` with an absent or blank `native_id`, and the test must cover at least one malformed content-subject branch.

Next authorized action: Patch the producer, test, and producer-owned contract only.

Patch applied: Yes. `_required_subject_native_id` now rejects missing/blank native IDs for profile, content, publisher, and rollup account subjects. The test mutates a reel row to remove `content_shortcode` and asserts the producer raises instead of emitting a record. The contract records fail-closed native-id behavior as part of the v0 residual boundary.

## 4. Unified Diff

```diff
diff --git a/orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py b/orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
index b3868c7a..88c84f30 100644
--- a/orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
+++ b/orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
@@ -291,6 +291,12 @@ def build_metric_rollup_record(
                 "rollup_window": seed_rollup["rollup_window"],
                 "rollup_window_description": seed_rollup["rollup_window_description"],
                 "content_kind_inclusion_rule": seed_rollup["content_kind_inclusion_rule"],
+                "derivation": {
+                    "kind": "computed_metric_rollup",
+                    "source_record_ref_kind": "derived_refs",
+                    "metric_posture_semantics": "source_input_support_not_raw_aggregate_visibility",
+                    "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
+                },
                 "metric_rollups": {
                     name: _rollup_metric(metric, what=f"rollup {seed_rollup.get('metric_rollup_id')!r} metric {name!r}")
                     for name, metric in seed_rollup["metric_rollups"].items()
@@ -322,14 +328,23 @@ def _observation_subject(seed_observation: Mapping[str, Any]) -> dict[str, Any]:
         ref: dict[str, Any] = {
             "namespace": _PLATFORM_NAMESPACE,
             "kind": "platform_public_account",
-            "native_id": seed_observation["platform_subject_key"],
+            "native_id": _required_subject_native_id(
+                seed_observation.get("platform_subject_key"),
+                what=f"observation {seed_observation.get('metric_observation_id')!r} account subject",
+            ),
         }
     else:
         ref = {
             "namespace": _PLATFORM_NAMESPACE,
             "kind": "public_content_object",
-            "native_id": seed_observation.get("content_id_or_none"),
-            "published_by_account_native_id": seed_observation["platform_subject_key"],
+            "native_id": _required_subject_native_id(
+                seed_observation.get("content_id_or_none"),
+                what=f"observation {seed_observation.get('metric_observation_id')!r} content subject",
+            ),
+            "published_by_account_native_id": _required_subject_native_id(
+                seed_observation.get("platform_subject_key"),
+                what=f"observation {seed_observation.get('metric_observation_id')!r} publisher subject",
+            ),
         }
     ref["orca_platform_account_id"] = seed_observation["platform_account_id"]
     return {"ref_type": "entity_key", "ref": ref}
@@ -339,12 +354,21 @@ def _rollup_subject(seed_rollup: Mapping[str, Any], account_handle: str | None)
     ref: dict[str, Any] = {
         "namespace": _PLATFORM_NAMESPACE,
         "kind": "platform_public_account",
-        "native_id": account_handle,
+        "native_id": _required_subject_native_id(
+            account_handle,
+            what=f"rollup {seed_rollup.get('metric_rollup_id')!r} account subject",
+        ),
         "orca_platform_account_id": seed_rollup["profile_subject_id"],
     }
     return {"ref_type": "entity_key", "ref": ref}
 
 
+def _required_subject_native_id(value: Any, *, what: str) -> str:
+    if not isinstance(value, str) or not value.strip():
+        raise ValueError(f"{what} requires a non-empty entity_key native_id")
+    return value
+
+
 def _metric_posture(kind: str, reason: str | None) -> dict[str, Any]:
     return {"kind": kind, "reason_code": None, "reason_detail": reason}
 
diff --git a/orca-harness/tests/unit/test_creator_metric_silver_producer.py b/orca-harness/tests/unit/test_creator_metric_silver_producer.py
index 83cb129c..4a605cf6 100644
--- a/orca-harness/tests/unit/test_creator_metric_silver_producer.py
+++ b/orca-harness/tests/unit/test_creator_metric_silver_producer.py
@@ -12,6 +12,8 @@ import hashlib
 import json
 from pathlib import Path
 
+import pytest
+
 from capture_spine.creator_profile_current.silver_metric_producer import (
     METRIC_OBSERVATION_LANE,
     METRIC_OBSERVATION_PAYLOAD_KIND,
@@ -185,6 +187,12 @@ def test_rollup_record_lineage_and_no_drift(tmp_path: Path) -> None:
 
     # no-drift: the rollup record's numbers equal the reused seed computation.
     payload = rollup["payload"]["observation"]
+    assert payload["derivation"] == {
+        "kind": "computed_metric_rollup",
+        "source_record_ref_kind": "derived_refs",
+        "metric_posture_semantics": "source_input_support_not_raw_aggregate_visibility",
+        "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
+    }
     assert payload["observation_count"] == seed_rollup["observation_count"] == 6
     assert payload["view_count_min"] == seed_rollup["view_count_min"] == 100
     assert payload["view_count_max"] == seed_rollup["view_count_max"] == 300
@@ -214,3 +222,19 @@ def test_rollup_metric_posture_value_coupling(tmp_path: Path) -> None:
         else:
             assert metric["metric_value"] is None
             assert posture["reason_detail"]
+
+
+def test_content_subject_missing_native_id_fails_closed(tmp_path: Path) -> None:
+    rows = _projection_rows()
+    rows[1] = dict(rows[1], content_shortcode=None)
+    projection = tmp_path / "projection.json"
+    projection.write_text(json.dumps({"packet_id": PACKET_ID, "rows": rows}), encoding="utf-8")
+    data_root = DataLakeRoot.for_test(tmp_path / "lake")
+
+    with pytest.raises(ValueError, match="content subject requires a non-empty entity_key native_id"):
+        derive_creator_metric_silver_records_from_projections(
+            data_root=data_root,
+            projection_paths=[projection],
+            account_ledger=_account_ledger(),
+            generated_at_utc=GENERATED_AT,
+        )
diff --git a/orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md b/orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
index 03d9503b..7ec85ec0 100644
--- a/orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
+++ b/orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
@@ -70,9 +70,9 @@ Anchored to its source projection's raw packet via `raw_refs`.
 
 `payload.observation` carries: `subject` (the platform-account `entity_key`),
 `rollup_kind`, `platform_scope`, `platform_account_ids`, `rollup_window`,
-`rollup_window_description`, `content_kind_inclusion_rule`, `metric_rollups`
-(named aggregates, each `{metric_value, metric_posture, unit}`),
-`observation_count`, `view_count_min`/`view_count_max`,
+`rollup_window_description`, `content_kind_inclusion_rule`, `derivation`,
+`metric_rollups` (named aggregates, each `{metric_value, metric_posture,
+unit}`), `observation_count`, `view_count_min`/`view_count_max`,
 `calculation_recipe_version`, `computed_at`, `freshness_state`,
 `sample_support`, `limitations`, `source_metric_observation_ids`. Lane
 `creator_metric_rollup_silver`. The rollup's `derived_refs` carry one
@@ -91,8 +91,16 @@ This reuses the posture model the existing seeds and `validation.py` already
 apply to the same aggregates (Instagram `average_views`/`engagement_rate:
 observed`; YouTube `engagement_rate: unavailable_with_reason`). It is the
 load-bearing contract choice in this v0 — applying the *observed* posture,
-defined for source-visible facts, to a *computed* aggregate. It is named here
-for the delegated review rather than assumed silently.
+defined for source-visible facts, to a *computed* aggregate. To prevent that
+posture from being mistaken for raw aggregate visibility, every
+MetricRollupObservation also carries `payload.observation.derivation` with:
+
+- `kind: computed_metric_rollup`;
+- `source_record_ref_kind: derived_refs`;
+- `metric_posture_semantics: source_input_support_not_raw_aggregate_visibility`;
+- `calculation_recipe_version` matching the rollup recipe.
+
+That marker is part of the v0 payload contract, not optional prose.
 
 ## Conformance and no-drift
 
@@ -107,7 +115,8 @@ for the delegated review rather than assumed silently.
 - v0 emits MetricObservation + MetricRollupObservation only. It does NOT emit
   PlatformAccountEntity / public_content_object entity records or the
   `content_published_by_account` relationship; the metric subject is carried as
-  a self-describing `entity_key` reference.
+  a self-describing `entity_key` reference. The producer must fail closed rather
+  than emit an `entity_key` whose `native_id` is absent or blank.
 - Observations carry `raw_refs` to the raw packet; the intermediate IG
   reels-grid projection is recorded in `provenance`, not a formal `derived_refs`
   edge, because the reused seed observation does not carry the projection
```

## 5. Neutral Source Citations

- `[creator-metric-silver-contract]` The Silver Vault common header requires `record_kind`, `payload_kind`, `content_hash`, `raw_refs`, and `derived_refs` semantics; metric observations require posture/value/reason coupling and missing/not-attempted values as posture + reason, not zero (`core_spine_v0_data_lake_silver_vault_record_contract_v0.md`, Common Record Header and Metric Observation Records).
- `[silver-metric-producer]` The existing Fragrantica Silver producer computes `content_hash` by canonical JSON excluding `content_hash`, uses `sha256:` storage, and places lineage in `derived_refs` for records generated from prior derived records (`orca-harness/cleaning/fragrantica_lake.py`, Silver record builder and hash helper).
- `[silver-metric-producer]` `DataLakeRoot.append_record` writes append-only records at `<subtree>/<anchor_shard>/<raw_anchor>/<lane>/<record_id>` and validates path segments (`orca-harness/data_lake/root.py`, `append_record`).
- `[silver-metric-producer]` The Instagram metric seed reuses selected projection rows, computes rollups from complete observed reel metrics, marks unavailable/not-attempted metrics with reason-bearing non-observed posture, and carries sample support and limitations (`instagram_metric_seed.py`, seed builder and rollup helpers).
- `[silver-metric-producer-tests]` `validation.py` enforces current rollup posture/value coupling, source observation id counts, sample support, and representativeness limits for the read model (`validation.py`, rollup validation helpers).
- `[creator-metric-silver-contract]` The lake-native creator mapping defines rollups as computed from MetricObservation records with recipe, source ids, sample support, limitations, and non-claims; it does not make rollups raw source facts (`creator_profile_current_lake_native_record_mapping_v0.md`, Metric Derivation Rule).

## 6. Controller Verdict And Residual Risk

Recommendation: `patch_before_acceptance`.

The patched target is materially better and the two major review findings are closed by bounded changes inside the commissioned files. The remaining decision is CA adjudication: keep, modify, or reject the patch. If kept, the observed-posture-for-computed-rollup choice is acceptable for this v0 because the record now carries an explicit derivation marker and source-input posture semantics. Residual risk: future generic consumers must still respect `payload_kind: MetricRollupObservation` and the derivation marker rather than flattening all `metric_posture.kind: observed` values as raw observations.

No `NEEDS_ARCHITECTURE_PASS` is recommended after the patch because the posture ambiguity was closable inside the producer-owned rollup payload contract without changing the Silver Vault posture vocabulary, the lake writer, the seed computation, or the validator.

## 7. Validation Run Status

Commands run:

```text
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -q -p no:cacheprovider tests\unit\test_creator_metric_silver_producer.py
```

Observed result: `..... [100%]` (5 tests passed).

```text
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer\orca-harness
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -q -p no:cacheprovider tests\unit\test_creator_registry_index.py tests\unit\test_creator_public_handle_linkage.py tests\unit\test_creator_profile_current_static_view.py tests\unit\test_instagram_reels_creator_metric_seed.py tests\unit\test_youtube_creator_metric_seed.py
```

Observed result: `.................................................... [100%]` (52 tests passed).

```text
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer
git diff --check
```

Observed result: exit code 0. Output contained only Git autocrlf warnings that LF will be replaced by CRLF for the three touched target files; no whitespace errors were reported.

```text
cd C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer
$env:PYTHONDONTWRITEBYTECODE=1; python .agents\hooks\check_map_links.py --strict
```

Observed result: `check_map_links --strict: OK (0 findings)`; annotated nonresolving: 33 debt, not failures.

Not run: `python orca-harness\runners\run_creator_profile_current_materialize.py --check`, because this patch does not touch the read-model materializer and the prompt's patch validation list required the producer suite, baseline creator suites, `git diff --check`, and strict map links after the contract change.

## 8. Off-Scope Flags

No off-scope source edit was made. The following remain read-only / future-work surfaces:

- Silver Vault record contract and derived-layout contracts.
- `instagram_metric_seed.py`, the Instagram seed JSON, and `validation.py` posture vocabulary.
- Real lake physicalization, live capture, schedulers, dashboards, SQLite/backend choice, and `creator_profile_current` re-pointing.
- Entity/relationship record emission and cross-platform identity stitching.

## 9. Review-Use Boundary

This report, its patch, citations, and recommendation are decision input for the commissioning Chief Architect. They are not owner acceptance, validation proof, readiness, deployment, live-lake authorization, source-capture authorization, SQLite/backend adoption, or permission to keep the patch without home-model adjudication.

Adjudicator next move: decide whether to keep the bounded patch; only after that decision should the CA decide whether STEP-03 (`creator_profile_current` re-pointing onto Silver records) may proceed.