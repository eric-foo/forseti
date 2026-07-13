# TikTok Grid Longitudinal Silver — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code review report
scope: >
  Cross-vendor delegated review-and-patch return for the TikTok grid-only
  Bronze admission, packet-grain Silver observation set, exact-policy history
  reader, consumption seam, registrations, tests, and the documentation-only
  Instagram/YouTube follow-on (branch codex/topfrag-silver-analytics,
  b6a3903c..8037622d).
use_when:
  - Chief Architect adjudication of the delegated review-and-patch return.
authority_boundary: retrieval_only
```

## Provenance And Commission

```yaml
reviewed_by: claude-fable-5
authored_by: gpt-5-codex
de_correlation_bar: cross_vendor_discovery
```

- commission: `docs/prompts/reviews/tiktok_grid_longitudinal_silver_delegated_adversarial_code_review_patch_prompt_v0.md`
- target_kind: `delegated_mixed_review_and_patch` (code lane `workflow-code-review`; artifact lane `workflow-adversarial-artifact-review`; `workflow-deep-thinking` applied after source loading)
- reviewer vendor: Anthropic (`claude-fable-5`); author vendor: OpenAI (`gpt-5-codex`, per commission `author_home_model_family`) — vendors differ, cross-vendor discovery bar satisfied
- access: `repo`
- worktree: `C:\Users\vmon7\.codex\worktrees\f75f\orca`, branch `codex/topfrag-silver-analytics` at `8037622d`
- review base: `b6a3903c84ed84ac89499d790ff0347c40bd07ac` (verified ancestor of HEAD)
- controller-start state: tracked tree clean, no untracked files reported by `git status --porcelain`; two unreadable stale pytest scratch directories (`forseti-harness/.pytest_ci_895/`, `.pytest_ci_895_full_rebase/`) raise permission-denied warnings — outside the named scope, noted as a residual, not a blocker.

Sources read: the complete `b6a3903c..HEAD` diff and all 21 named targets; `AGENTS.md`; overlay README, `source-loading.md`, `review-lanes.md`, targeted `delegated-review-patch.md`; `docs/workflows/topfrag_silver_lake_mechanics_handoff_v0.md`; `core_spine_v0_data_lake_silver_vault_record_contract_v0.md`; directly-called sources `data_lake/consumption.py`, `data_lake/root.py` (write/read/availability methods), `data_lake/silver_lineage.py`, `capture_spine/creator_profile_current/silver_envelope_core.py`, `runners/run_seam_cadence.py`, `source_capture/tiktok/creator_onboarding.py` (grid window builder and URL binder), and — for the follow-on doc's factual claims — `run_source_capture_ig_reels_grid_packet.py`, `run_source_capture_youtube_rss_monitor.py`, `source_capture/youtube_channel_rss.py`. Sibling catch-up runners (`asr`, `fragrantica`, `basenotes`, `comment_attention`) were read at their exit-code paths for convention comparison.

## Findings

Severity `critical|major|minor`; confidence `high|medium|low`. Findings 1–5 were
patched inside the commissioned scope with same-check red/green proof: all
seven new/adjusted tests failed against the pre-fix implementation (observed
red run) and pass after the patches.

### F-01 [bronze] major / high — operator time override silently displaced the source-backed receipt capture time (patched)

- location: `forseti-harness/source_capture/tiktok/grid_packet.py` (`write_tiktok_grid_packet`, observed_at resolution)
- evidence: pre-patch `observed_at = _required_utc(observed_at_utc or receipt_time)` let an explicit `--observed-at-utc` win over a present `collection_receipt.capture_timestamp`, while the Silver runner `_observed_at` prefers the preserved receipt. The runner's own help text scopes the flag to "legacy grid artifacts whose collection receipt lacks capture_timestamp".
- impact: (a) Bronze manifest `capture_time` could be operator-supplied and diverge from the Silver `observed_at` derived from the same packet — breaking fitness items 3 ("source-backed UTC capture time") and 5 ("capture time comes from Bronze") at the lineage level; (b) a packet whose receipt timestamp was malformed could still be admitted under an override, then permanently fail Silver production on every catch-up run (Bronze is immutable), a poisoned-packet class.
- minimum_closure_condition: when the artifact carries a receipt capture timestamp, admission validates it as UTC and treats it as authoritative; a conflicting explicit override fails admission; a malformed receipt timestamp fails admission even with an override.
- next_authorized_action: Chief Architect adjudication of the applied patch.
- verification: red/green — `test_grid_packet_rejects_explicit_time_conflicting_with_receipt`, `test_grid_packet_rejects_malformed_receipt_time_even_with_override`, `test_grid_packet_accepts_explicit_time_matching_receipt_instant` (plus the adjusted missing-time test) failed pre-fix, pass post-fix. The pinned TopFrag grid artifact (SHA-256 verified `4804CEAC…E97C`) has no receipt timestamp, so its legacy override path is unchanged.

### F-02 [silver-runner] major / high — availability-reconcile failures exited 0 (patched)

- location: `forseti-harness/runners/run_tiktok_grid_observation_producer.py` (`main` exit computation)
- evidence: pre-patch `return 1 if any(row.get("status") == "failed" ...)`; `reconcile_availability_per_packet` emits rows with status `availability_reconcile_failed`, which therefore exited 0. A packet failing reconcile is absent from availability, is never picked up, and is never acked — with a success exit code for any cron/daemon consumer of this CLI. The allowlist siblings (`run_asr_transcript_catchup.py`, `run_fragrantica_cleaning_catchup.py`, `run_basenotes_cleaning_catchup.py`) fail on any non-healthy status; the seam-cadence docstring binds "Failures never satisfy the signal".
- impact: fake-success exit path for the standalone runner invocation (fitness item 8: the seam "exposes failures"). Mitigations that kept this from critical: the failure row remains visible in stdout JSON, `pending_packets` raises loudly on any reconcile failure, and the cadence orchestrator counts any cycle-2 status entry as work.
- minimum_closure_condition: any per-run status outside `{derived, not_applicable}` produces a nonzero exit.
- next_authorized_action: Chief Architect adjudication of the applied patch.
- verification: red/green — `test_main_exit_code_fails_on_availability_reconcile_failure` failed pre-fix (asserted 0 == 1), passes post-fix.

### F-03 [reader] minor / high — wrong-policy or misfiled record at the exact-policy path was silently skipped (patched)

- location: `forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py` (`read_social_metric_history`)
- evidence: the deterministic record id encodes the policy fingerprint, so any existing file at the computed exact-policy path must carry that fingerprint and that record id. Pre-patch, a fingerprint mismatch was `continue`-skipped (silent empty/partial history) and the embedded `record_id` was never compared to the path-computed id — both are misfile/tamper states the module docstring promises to fail loudly on.
- impact: an integrity-violating record (copy, partial migration, future producer bug) degraded to a silent no-data read instead of a loud failure (fitness item 9's fail-don't-guess axis).
- minimum_closure_condition: fingerprint or record_id disagreement at the exact-policy path raises; legitimate cross-account/cross-platform records in shared lanes remain skipped.
- next_authorized_action: Chief Architect adjudication of the applied patch.
- verification: red/green — `test_history_reader_fails_loud_on_wrong_policy_record_at_exact_policy_path` (record rewritten with a foreign fingerprint and a recomputed valid content hash) returned an empty history pre-fix, raises post-fix.

### F-04 [schema] minor / high — MetricObservationSet rows could carry a foreign platform namespace (patched)

- location: `forseti-harness/data_lake/silver_record.py` (`_validate_metric_observation_set`)
- evidence: the validator required the set-level subject namespace to equal `platform` but placed no such bound on row subjects; the reader joins rows by `native_id` alone, so a cross-platform row inside a set would be merged into the platform's history.
- impact: row-identity envelope gap contradicting the validator's stated purpose ("prevents a producer from ... weakening ... row identity") and fitness item 5 (identity by platform-native video ID). Current producer hard-codes `tiktok`, so exploitation requires a future producer — envelope-level hardening, not a live leak.
- minimum_closure_condition: every row subject namespace must equal the set's platform at the validating front door.
- next_authorized_action: Chief Architect adjudication of the applied patch.
- verification: red/green — `test_validate_metric_set_rejects_cross_platform_row_namespace` failed pre-fix, passes post-fix.

### F-05 [bronze] minor / high — URL binding accepted any host and scheme (patched)

- location: `forseti-harness/source_capture/tiktok/grid_packet.py` (`write_tiktok_grid_packet` item loop)
- evidence: pre-patch binding was `video_url.rstrip("/").endswith(f"/@{handle}/video/{id}")` — `https://evil.example/@creator/video/101` (or a non-http scheme) passed as a "canonical video URL". The grid-window builder's own `_is_creator_video_url` (creator_onboarding.py:708) already pins scheme http/https, host `tiktok.com`/`*.tiktok.com`, and the exact case-insensitive path; the admission gate was strictly weaker than the surface that produces the artifacts it admits.
- impact: fitness item 3 requires binding to "canonical video URLs"; the named MGT residual covers unproven source authorship, not non-TikTok hosts. Also removed a case-sensitivity inconsistency between builder and admission.
- minimum_closure_condition: admission enforces the same scheme/host/path binding as the builder.
- next_authorized_action: Chief Architect adjudication of the applied patch.
- verification: red/green — `test_grid_packet_rejects_video_url_on_non_tiktok_host` failed pre-fix, passes post-fix. All 32 URLs in the hash-pinned TopFrag grid artifact are canonical `www.tiktok.com` URLs, so the pinned scratch evidence is unaffected.

### F-06 [out-of-scope flag] minor / high — same exit-code weakness in the comment-attention runner (flag-only)

`forseti-harness/runners/run_tiktok_comment_attention_producer.py:165` uses the same `status == "failed"` denylist and exits 0 on `availability_reconcile_failed` rows. Outside the commissioned file set — flagged, not patched. minimum_closure_condition: same allowlist exit semantics as F-02. next_authorized_action: separate bounded commission.

### F-07 [silver-runner] minor / low — grid-window filename matched by suffix, not equality (flag-only)

`_grid_input` matches preserved files with `Path(...).name.endswith("tiktok_grid_window.json")`; a hypothetical sibling named e.g. `old_tiktok_grid_window.json` would trigger a spurious "multiple TikTok grid windows" failure (fail-loud, not silent). No current packet writer stages such a name (grid admission, onboarding, and batch packets all stage exactly `tiktok_grid_window.json`), so this stays a flagged tightening candidate, not a patched defect.

### F-08 [producer/reader] minor / medium — creator-handle case is preserved into Silver identity (flag-only)

The producer keys the account subject by the artifact's `creator_handle` with case preserved; the reader's `account_native_id` comparison is case-sensitive. The same creator onboarded under different casing would split into two histories. TikTok handles are case-insensitively unique; normalization is a policy/identity decision (it changes record semantics under the policy fingerprint), so this is routed to an owner decision rather than patched. minimum_closure_condition: an owner-decided handle-normalization rule for Silver account identity, or an explicit non-normalization decision recorded.

### F-09 [risk] minor / medium — dual admission of one grid artifact permanently fails that creator's reads (flag-only)

Both onboarding/batch packets and the new grid-only admission stage `tiktok_grid_window.json`, so the same grid state admitted through two packets with the same receipt timestamp yields two equal-time observation sets, and the reader (correctly) fails closed on ambiguous equal-time siblings — permanently, since supersession edges are an accepted deferred residual and Bronze is immutable. Operationally reachable via re-admission of an already-captured artifact. Mitigation until supersession exists is operational: do not dual-admit the same grid state.

### F-10 [risk] minor / low — already-committed packets with malformed receipt timestamps have no retirement path (flag-only)

Any legacy committed TikTok packet whose preserved receipt carries a malformed `capture_timestamp` will fail Silver production visibly on every run with no mechanism to retire it. F-01 closes the admission-side entry point; existing lake state (if any) would need an owner-decided skip/retire mechanism. No such packet is known to exist.

## Artifact Review — `docs/workflows/social_grid_longitudinal_followon_v0.md`

Reviewed under `workflow-adversarial-artifact-review` (Phase 1 correctness, Phase 2 friction). No material findings.

- Verified against named sources: IG seam (`source_family=instagram_creator`, `SOURCE_SURFACE="ig_reels_grid_dom_passive_json"`, preserved `ig_reels_grid_capture.json`, logged-out one-page-load capture posture) matches `run_source_capture_ig_reels_grid_packet.py`; YouTube seam (`source_family=youtube`, `source_surface=youtube_channel_rss_feed`, preserved feed XML + `rss_monitor_entries.json`, 15-entry window, exact views when parseable, `media:starRating count` carried as like_count with provenance, comment count explicitly unavailable) matches `run_source_capture_youtube_rss_monitor.py` and `youtube_channel_rss.py` — the specific overstatement risks named in the commission (starRating, comment count) are correctly stated, not overstated.
- All eight source-read-ledger paths and all four `open_next` paths exist in the tree.
- The document claims documentation-only status, names no implementation or live-readiness claim, keeps watch-packet vs RSS policies separate, and its residuals section matches the commission's MGT residual set. Retrieval header conforms to the overlay header contract.

## Considered And Defended

- Duplicate grid rows entering Bronze — builder dedups via a `seen` set with per-row URL binding; admission and producer independently re-reject duplicate video ids.
- Booleans admitted as observed integer metrics — `_metric` uses `type(value) is int`, excluding bool.
- Producer/reader content-hash asymmetry — `content_hash()` pops the `content_hash` field before hashing; round-trip proven by the tamper test.
- `row_count` spoofed with a bool — validator rejects bool before the equality check.
- Reader fabricating a missing day or carrying values forward — absent anchors contribute nothing; requested ids with no records return empty lists.
- Equal-time collision from one anchor — impossible; one deterministic record per anchor+policy.
- Non-target TikTok packet looping forever — explicit `not_applicable` ack against the manifest-fingerprint obligation; re-surfaces only if the manifest changes.
- Ack before durability — `derive_tiktok_grid_observation_set` validates and byte-reads back before `append_ack`; the failure path skips the ack (tested, including monkeypatched persistence failure).
- `stats` non-Mapping fallback to flat item mirrors — deliberate legacy-shape support (the hash-pinned TopFrag grid rows are flat); postures stay honest for absent fields.
- Packet-grain set weakening the Silver envelope (commission question 7) — the front-door validates every nested metric with the exact MetricObservation posture/value coupling; no platform-specific core abstraction was added (one lane registration + one payload kind).
- Empty-pickup no-work claim over an unreconciled surface — `pending_packets` reconciles first and raises loudly on any failure entry.
- Selection silently shrinking the requested count — `build_tiktok_grid_video_selection` raises on insufficient eligible rows; both policy versions were bumped (`…fixed_count_v1`, `…top_fraction_v3`), and ineligible rows are preserved with explicit `selection_ineligible:*` reasons.

## Bounded Working-Tree Diff

Applied only to commissioned targets; generated by `git diff` at the target
worktree after validation:

```diff
diff --git a/forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py b/forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py
index c5946dee..624968ce 100644
--- a/forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py
+++ b/forseti-harness/capture_spine/creator_profile_current/social_metric_history_reader.py
@@ -48,9 +48,11 @@ def read_social_metric_history(
     """Return ordered histories for the requested platform-native content IDs.

     ``policy_fingerprint`` and ``record_id_for_anchor`` are mandatory selection
-    inputs.  A record from any other policy is ignored rather than silently
-    substituted.  A malformed or integrity-invalid exact-policy record fails
-    the read loudly.
+    inputs.  A record for any other policy lives at a different deterministic
+    record id and is simply absent here; a record found at the exact-policy path
+    whose embedded record_id or policy fingerprint disagrees is a misfiled or
+    tampered record and fails the read loudly, as does any malformed or
+    integrity-invalid exact-policy record.
     """
     requested = {str(value).strip() for value in content_native_ids if str(value).strip()}
     histories: dict[str, list[SocialMetricHistoryPoint]] = defaultdict(list)
@@ -83,9 +85,14 @@ def read_social_metric_history(
             raise ValueError(f"social metric Silver raw_anchor mismatch: {path}")
         if record.get("payload_kind") != METRIC_OBSERVATION_SET_PAYLOAD_KIND:
             raise ValueError(f"unexpected social metric Silver payload kind: {path}")
+        if record.get("record_id") != record_id:
+            raise ValueError(f"social metric Silver record_id mismatch: {path}")
         observation = record["payload"]["observation"]
         if observation.get("policy_fingerprint_sha256") != policy_fingerprint:
-            continue
+            raise ValueError(
+                "social metric Silver record at the exact-policy path carries a "
+                f"different policy fingerprint: {path}"
+            )
         if observation.get("platform") != platform:
             continue
         account_ref = observation.get("subject", {}).get("ref", {})
diff --git a/forseti-harness/data_lake/silver_record.py b/forseti-harness/data_lake/silver_record.py
index 1669fc00..48eb17c0 100644
--- a/forseti-harness/data_lake/silver_record.py
+++ b/forseti-harness/data_lake/silver_record.py
@@ -229,6 +229,10 @@ def _validate_metric_observation_set(observation: Mapping[str, Any]) -> None:
             raise SilverRecordError(
                 f"MetricObservationSet row {index} requires namespace/kind/native_id identity."
             )
+        if identity[0] != platform:
+            raise SilverRecordError(
+                f"MetricObservationSet row {index} subject namespace must equal platform."
+            )
         if identity in seen_subjects:
             raise SilverRecordError(
                 f"MetricObservationSet contains duplicate row subject {identity!r}."
diff --git a/forseti-harness/runners/run_tiktok_grid_observation_producer.py b/forseti-harness/runners/run_tiktok_grid_observation_producer.py
index 7a36b984..5cb16d98 100644
--- a/forseti-harness/runners/run_tiktok_grid_observation_producer.py
+++ b/forseti-harness/runners/run_tiktok_grid_observation_producer.py
@@ -214,7 +214,9 @@ def main(argv: list[str] | None = None) -> int:
     except DataLakeRootError as exc:
         parser.exit(status=2, message=f"data lake unavailable: {exc}\n")
     print(json.dumps(results, indent=2, sort_keys=True))
-    return 1 if any(row.get("status") == "failed" for row in results) else 0
+    # Allowlist exit semantics (matching the catch-up siblings): any unexpected
+    # status -- including availability_reconcile_failed -- fails the exit code.
+    return 0 if all(row.get("status") in {"derived", "not_applicable"} for row in results) else 1


 if __name__ == "__main__":
diff --git a/forseti-harness/source_capture/tiktok/grid_packet.py b/forseti-harness/source_capture/tiktok/grid_packet.py
index 8df0ffe0..5ee04ffd 100644
--- a/forseti-harness/source_capture/tiktok/grid_packet.py
+++ b/forseti-harness/source_capture/tiktok/grid_packet.py
@@ -10,6 +10,7 @@ import json
 from datetime import datetime
 from pathlib import Path
 from typing import Any, Mapping
+from urllib.parse import urlparse

 from source_capture.models import (
     CaptureModeCategory,
@@ -59,10 +60,17 @@ def write_tiktok_grid_packet(
             raise ValueError(f"TikTok grid item {index} must be an object")
         video_id = _required_text(raw_item.get("video_id"), f"items[{index}].video_id")
         video_url = _required_text(raw_item.get("video_url"), f"items[{index}].video_url")
-        expected_suffix = f"/@{creator_handle}/video/{video_id}"
-        if not video_url.rstrip("/").endswith(expected_suffix):
+        parsed = urlparse(video_url)
+        host = parsed.hostname.lower() if parsed.hostname else ""
+        expected_path = f"/@{creator_handle}/video/{video_id}".lower()
+        if (
+            parsed.scheme not in {"http", "https"}
+            or not (host == "tiktok.com" or host.endswith(".tiktok.com"))
+            or parsed.path.rstrip("/").lower() != expected_path
+        ):
             raise ValueError(
-                f"TikTok grid item {index} URL does not bind creator_handle and video_id"
+                f"TikTok grid item {index} URL does not bind creator_handle and video_id "
+                "on a canonical TikTok host"
             )
         video_ids.append(video_id)
     if len(set(video_ids)) != len(video_ids):
@@ -70,7 +78,17 @@ def write_tiktok_grid_packet(

     receipt = grid.get("collection_receipt")
     receipt_time = receipt.get("capture_timestamp") if isinstance(receipt, Mapping) else None
-    observed_at = _required_utc(observed_at_utc or receipt_time)
+    if receipt_time is not None:
+        # The artifact's own collection receipt is the source-backed capture time;
+        # an explicit observed_at_utc may only confirm it, never replace it.
+        observed_at = _required_utc(receipt_time)
+        if observed_at_utc and _required_utc(observed_at_utc) != observed_at:
+            raise ValueError(
+                "TikTok grid observed_at_utc conflicts with the artifact's "
+                "collection_receipt capture_timestamp"
+            )
+    else:
+        observed_at = _required_utc(observed_at_utc)
     profile_url = f"https://www.tiktok.com/@{creator_handle}"
     staged_artifacts = [(TIKTOK_GRID_WINDOW_JSON_NAME, grid_window_json)]
     file_ids = staged_file_id_map(staged_artifacts)
@@ -165,7 +183,8 @@ def _required_text(value: object, field: str) -> str:
 def _required_utc(value: object) -> str:
     if not isinstance(value, str) or not value.strip():
         raise ValueError(
-            "TikTok grid admission requires observed_at_utc when the grid receipt lacks capture_timestamp"
+            "TikTok grid admission requires a source-backed UTC capture time "
+            "(collection_receipt.capture_timestamp, or observed_at_utc when the receipt lacks one)"
         )
     text = value.strip()
     parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
diff --git a/forseti-harness/tests/unit/test_silver_record.py b/forseti-harness/tests/unit/test_silver_record.py
index 35c2c79a..57c22967 100644
--- a/forseti-harness/tests/unit/test_silver_record.py
+++ b/forseti-harness/tests/unit/test_silver_record.py
@@ -120,6 +120,13 @@ def test_validate_metric_set_rejects_row_count_drift() -> None:
         validate_silver_vault_record(record)


+def test_validate_metric_set_rejects_cross_platform_row_namespace() -> None:
+    record = _metric_set_record()
+    record["payload"]["observation"]["rows"][0]["subject"]["ref"]["namespace"] = "instagram"
+    with pytest.raises(SilverRecordError, match="must equal platform"):
+        validate_silver_vault_record(record)
+
+
 def test_validate_metric_set_rejects_missing_source_field() -> None:
     record = _metric_set_record()
     del record["payload"]["observation"]["rows"][0]["metrics"]["view_count"][
diff --git a/forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py b/forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py
index e0488f27..038aa9eb 100644
--- a/forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py
+++ b/forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py
@@ -2,9 +2,11 @@ from __future__ import annotations

 import json
 from pathlib import Path
+from types import SimpleNamespace

 import pytest

+from capture_spine.creator_profile_current.silver_envelope_core import content_hash
 from capture_spine.creator_profile_current.social_metric_history_reader import (
     read_social_metric_history,
 )
@@ -200,6 +202,66 @@ def test_history_reader_rejects_tampered_exact_policy_record(tmp_path: Path) ->
         )


+def test_history_reader_fails_loud_on_wrong_policy_record_at_exact_policy_path(
+    tmp_path: Path,
+) -> None:
+    data_root = DataLakeRoot.for_test(tmp_path / "lake")
+    packet_id = _admit_grid(
+        data_root,
+        observed_at="2026-07-12T00:00:00Z",
+        play_count=100,
+        like_count=10,
+        comment_count=2,
+    )
+    assert all(row["status"] == "derived" for row in runner.run_catchup(data_root=data_root))
+    path = data_root.record_path(
+        subtree="derived",
+        raw_anchor=packet_id,
+        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
+        record_id=observation_set_record_id(packet_id),
+    )
+    record = json.loads(path.read_text(encoding="utf-8"))
+    record["payload"]["observation"]["policy_fingerprint_sha256"] = "f" * 64
+    record["content_hash"] = f"sha256:{content_hash(record)}"
+    path.write_text(json.dumps(record), encoding="utf-8")
+
+    with pytest.raises(ValueError, match="different policy fingerprint"):
+        read_social_metric_history(
+            data_root=data_root,
+            lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
+            policy_fingerprint=TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
+            record_id_for_anchor=observation_set_record_id,
+            platform="tiktok",
+            account_native_id="creator",
+            content_native_ids=["101"],
+        )
+
+
+def test_main_exit_code_fails_on_availability_reconcile_failure(
+    monkeypatch: pytest.MonkeyPatch,
+    capsys: pytest.CaptureFixture[str],
+) -> None:
+    monkeypatch.setattr(
+        runner,
+        "DataLakeRoot",
+        SimpleNamespace(resolve=lambda **_kwargs: object()),
+    )
+    monkeypatch.setattr(
+        runner,
+        "run_catchup",
+        lambda **_kwargs: [
+            {
+                "packet_id": "01PACKET",
+                "status": "availability_reconcile_failed",
+                "error": "OSError: simulated locked availability entry",
+            }
+        ],
+    )
+
+    assert runner.main(["--data-root", "ignored"]) == 1
+    assert "availability_reconcile_failed" in capsys.readouterr().out
+
+
 def test_history_reader_rejects_equal_time_siblings(tmp_path: Path) -> None:
     data_root = DataLakeRoot.for_test(tmp_path / "lake")
     for play_count in (100, 150):
diff --git a/forseti-harness/tests/unit/test_tiktok_grid_packet.py b/forseti-harness/tests/unit/test_tiktok_grid_packet.py
index 5693e679..79a23c72 100644
--- a/forseti-harness/tests/unit/test_tiktok_grid_packet.py
+++ b/forseti-harness/tests/unit/test_tiktok_grid_packet.py
@@ -62,7 +62,7 @@ def test_grid_packet_preserves_supplied_grid_bytes_exactly(tmp_path: Path) -> No
 def test_grid_packet_requires_explicit_observed_time_when_receipt_has_none(
     tmp_path: Path,
 ) -> None:
-    with pytest.raises(ValueError, match="requires observed_at_utc"):
+    with pytest.raises(ValueError, match="source-backed UTC capture time"):
         write_tiktok_grid_packet(
             grid_window_json=_grid_bytes(observed_at=None),
             output_directory=tmp_path / "missing-time",
@@ -74,3 +74,46 @@ def test_grid_packet_requires_explicit_observed_time_when_receipt_has_none(
         output_directory=tmp_path / "explicit-time",
     )
     assert code == 0
+
+
+def test_grid_packet_rejects_explicit_time_conflicting_with_receipt(
+    tmp_path: Path,
+) -> None:
+    with pytest.raises(ValueError, match="conflicts with"):
+        write_tiktok_grid_packet(
+            grid_window_json=_grid_bytes(observed_at="2026-07-13T01:02:03Z"),
+            observed_at_utc="2026-07-14T00:00:00Z",
+            output_directory=tmp_path / "conflicting-time",
+        )
+
+
+def test_grid_packet_accepts_explicit_time_matching_receipt_instant(
+    tmp_path: Path,
+) -> None:
+    code, _ = write_tiktok_grid_packet(
+        grid_window_json=_grid_bytes(observed_at="2026-07-13T01:02:03Z"),
+        observed_at_utc="2026-07-13T01:02:03+00:00",
+        output_directory=tmp_path / "matching-time",
+    )
+    assert code == 0
+
+
+def test_grid_packet_rejects_malformed_receipt_time_even_with_override(
+    tmp_path: Path,
+) -> None:
+    with pytest.raises(ValueError):
+        write_tiktok_grid_packet(
+            grid_window_json=_grid_bytes(observed_at="yesterday"),
+            observed_at_utc="2026-07-13T01:02:03Z",
+            output_directory=tmp_path / "malformed-receipt-time",
+        )
+
+
+def test_grid_packet_rejects_video_url_on_non_tiktok_host(tmp_path: Path) -> None:
+    payload = json.loads(_grid_bytes().decode("utf-8"))
+    payload["items"][0]["video_url"] = "https://evil.example/@creator/video/101"
+    with pytest.raises(ValueError, match="does not bind"):
+        write_tiktok_grid_packet(
+            grid_window_json=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
+            output_directory=tmp_path / "wrong-host",
+        )
```

## Validation Evidence

All commands ran in the target worktree at `8037622d` plus the bounded
working-tree patch, with `PYTHONDONTWRITEBYTECODE=1`:

- red baseline (pre-fix, new tests only): 7 failed / rest passed — the seven new or adjusted tests failed against the unpatched implementation (observed run, `pytest_grid_review_red` basetemp).
- `python -m pytest -p no:cacheprovider -q --basetemp pytest_grid_review_unit forseti-harness/tests/unit/test_silver_record.py forseti-harness/tests/unit/test_tiktok_creator_onboarding.py forseti-harness/tests/unit/test_tiktok_grid_video_selection.py forseti-harness/tests/unit/test_tiktok_grid_packet.py forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py forseti-harness/tests/unit/test_tiktok_batch_admission.py` — pass, exit 0, 102 tests (95 authoring baseline + 7 review tests).
- `python -m pytest -p no:cacheprovider -q --basetemp pytest_grid_review_contract forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py forseti-harness/tests/contract/test_catchup_runner_seam_coverage.py forseti-harness/tests/contract/test_seam_cadence_coverage.py forseti-harness/tests/contract/test_silver_reader_selection_gate.py forseti-harness/tests/contract/test_data_lake_inventory_gate.py` — pass, exit 0, 45 tests (matches the authoring-lane count, rerun from the committed tip plus patch).
- `python .agents/hooks/check_silver_lane_registry.py --strict` — pass ("OK, no silver-lane write violations"; 3 pre-existing statically-unresolved lane arguments noted by the hook itself).
- `git diff --check` — pass, exit 0 (CRLF conversion warnings only, no whitespace errors).
- Pinned TopFrag staging evidence: `tiktok_grid_window.json` re-hashed at `C:\tmp\topfrag-onboarding-proper-20260712-v1\` — SHA-256 `4804CEAC143F83DD9AC61A22B59D4F2027A84118DEB5618181DD2A4ABC43E97C`, matching the handoff pin; all 32 rows carry canonical `www.tiktok.com` URLs and the receipt has no `capture_timestamp`, so the applied patches leave the pinned scratch path behavior unchanged. The authoring lane's end-to-end 32-row scratch run itself was not re-executed (it is not part of the commissioned post-patch validation block); its compatibility with the patch was verified at the artifact level as above.
- Not run: full repository test suite beyond the commissioned subset; live capture; live-lake writes (all out of commission scope).

## Verdict

Reviewer verdict (decision input, not acceptance): the reviewed path satisfies
the bounded fitness contract after the five applied bounded patches — grid rows
and exact source stats are preserved into Bronze with real zeros; ranking
excludes without erasing and fails only on insufficient eligible rows under
explicitly bumped policy versions; grid-only admission preserves bytes exactly
and now binds canonical-host URLs and a receipt-authoritative source-backed UTC
capture time; one eligible packet deterministically yields one validated,
byte-read-back, policy-fingerprinted `MetricObservationSet`; identity is keyed
by native video ID with capture time from Bronze; missing never becomes zero;
the seam acks only after verification and now fails the exit code on any
non-healthy status; and the reader is exact-policy, integrity-checking, ordered
by capture time, and fails closed on ambiguity — with the flag-only findings
F-06..F-10 and the residuals below left open. No returned change is kept until
Chief Architect adjudication.

## Residual Risks

- Commission MGT residuals stand unchanged: scratch-only proof (no live cadence/throughput claim), availability-scan retrieval, deferred supersession edges, artifact-internal (not source-served) authorship binding, documented-only IG/YouTube adapters, sparse-history semantics.
- F-06 (comment-attention exit code), F-07 (filename suffix match), F-08 (handle-case identity), F-09 (dual-admission equal-time lock), F-10 (no retirement path for malformed-receipt legacy packets) remain open as flagged.
- The delegate's own patched lines are the one non-independent sliver of this pass; they are mechanically verifiable via the embedded diff plus the named red/green tests.
- Two permission-denied stale pytest scratch directories in the target worktree could not be inspected; review basetemp directories `pytest_grid_review_red/unit/contract` are untracked scratch left for the CA to clean or ignore.

## Review-Use Boundary

Findings, diff, verdict, and residuals are decision input for Chief Architect
adjudication only. They are not approval, validation status, readiness,
mandatory remediation, or executor-ready patch authority until separately
accepted. Adjudication closes per
`.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next
Step.

## Chief Architect Adjudication

`ACCEPTED_FOR_PR_UPDATE`, with one same-lane closure added by the home model.

- F-01 accepted. A present receipt timestamp is the source-backed clock; an
  operator value may confirm it but cannot replace or rescue it.
- F-02 accepted. The runner now allowlists only `derived` and `not_applicable`
  as healthy terminal statuses, so reconcile and future unknown failures cannot
  produce a success exit code.
- F-03 accepted. The exact deterministic path is already policy-selective, so
  an embedded record-id or fingerprint disagreement is corruption, not a
  candidate to skip.
- F-04 accepted. A set-level TikTok identity cannot truthfully contain rows in
  another platform namespace.
- F-05 accepted. Admission now matches the existing builder's TikTok
  scheme/host/path binding instead of treating a path suffix as canonicality.
- F-06 modified and self-closed. The exit-code patch is retained, and the home
  model also found that the comment-attention runner treated a new grid-only
  TikTok packet as a malformed deep batch. It now acknowledges non-batch TikTok
  packets as `not_applicable` before completion and treats that status as
  healthy. This is necessary interoperability for running all registered
  TikTok Silver consumers over the same lake.
- F-07 accepted as a low residual, not patched. Literal filename equality would
  reject every valid packet because the common writer preserves files as
  `NN_tiktok_grid_window.json`. Current registered writers do not emit the
  colliding sibling shape. Upgrade trigger: a registered producer can emit an
  overlapping suffix or a real packet is misclassified; then bind the exact
  staged-name grammar (and file id), not bare equality.
- F-08 accepted as an owner-gated identity residual, not patched. Reader-only
  case folding would silently merge identities under the current fingerprint.
  Upgrade trigger: an observed case-split identity or an owner-selected
  canonical-handle rule; apply it at ingress/production with an explicit policy
  version/fingerprint change.
- F-09 accepted with narrowed impact wording, not patched. Dual admission can
  block the default full history for affected content ids through the deliberate
  equal-time ambiguity guard; it does not block unrelated creators/content, and
  a caller can restrict `raw_anchors`. The current operating rule remains one
  admission per grid state. Durable dedupe or supersession requires an
  owner-defined equivalence rule that preserves sibling lineage.
- F-10 accepted as a low residual, not patched. F-01 prevents new malformed
  receipt timestamps from entering through this writer. A quarantine/retirement
  mechanism is justified only if a legacy poisoned packet is observed, because
  its acknowledgement and audit semantics are an owner decision.

The five delegate patches, the home-model F-06 closure, and this review record
are retained. The accepted residuals do not block the bounded scratch-proven
TikTok longitudinal Silver path; they remain non-claims about live cadence,
duplicate supersession, identity migration, or legacy-packet retirement.

Post-adjudication validation on the retained tree passed: 107 focused unit
tests; 45 seam/reader/inventory contract tests; the strict Silver lane registry
guard; this review output's strict provenance guard; and `git diff --check`.
The registry guard repeated its three pre-existing statically unresolved dynamic
lane-argument notes and reported no Silver-lane write violation.

`operator_closeout_source`: this adjudication section, the retained working-tree
diff, and the post-adjudication validation evidence on the lane branch. The next
authorized step is the single batched land step: commit, push, and update the
existing PR after all named checks remain green.
