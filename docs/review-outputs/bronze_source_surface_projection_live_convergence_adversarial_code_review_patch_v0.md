# Bronze Source-Surface Projection Live Convergence — Delegated Adversarial Code Review & Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review output
reviewed_by: claude-opus-4.8
authored_by: OpenAI GPT-family Codex home model
scope: >
  De-correlated adversarial code review-and-patch of PR #508's merged Bronze
  source-surface downstream projection consumption path at head e9376ff9, plus
  read-only verification of the dispatcher-observed real-lake convergence evidence.
use_when:
  - Adjudicating whether the Bronze source-surface -> IG reels-grid projection path is trustworthy before building a derived/Silver retrieval index on the appended records.
  - Checking the fail-closed, verified-read, view-only, and append-only properties of project_ig_reels_grid_from_bronze_catalog and source_surface_catalog_rows.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_prompt_v0.md
```

## Provenance & Commission

| Field | Value |
| --- | --- |
| `reviewed_by` | `claude-opus-4.8` (receiving controller / reviewer) |
| `authored_by` | `OpenAI GPT-family Codex home model` |
| `de_correlation_bar` | `cross_vendor_discovery` (author = OpenAI/Codex; reviewer = Claude/Anthropic — different vendor lineage) |
| `same_vendor_rationale` | `not_applicable` (cross-vendor) |
| Commission | Delegated adversarial code review-and-patch of PR #508's Bronze source-surface projection path + real-lake convergence evidence |
| Review prompt | `docs/prompts/reviews/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_prompt_v0.md` |
| Target diff range | `86d7686a..e9376ff9` (PR #508 head; single commit "Add Bronze source-surface projection proof", +356/−3, 5 files) |
| PR | [eric-foo/orca#508](https://github.com/eric-foo/orca/pull/508) (MERGED into `codex/bronze-v41-clean-verify`) |
| Edit permission | `patch-only` within `reviewer_patch_scope.may_edit`; report-write to this path |
| Reviewer output | review report + one bounded **uncommitted working-tree** patch (catalog.py + its test) |

This review is **decision input for home-model / Chief Architect adjudication only.** It is not approval, validation pass/fail, readiness, mandatory remediation, source promotion, or merge authority. Every finding and every diff hunk is a claim to adjudicate, not a premise to inherit.

## Actor / Model-Family Receipt & De-correlation Status

```yaml
author_home_model_family: OpenAI/Codex
controller_model_family: Anthropic/Claude (Opus 4.8)
current_receiving_actor_role: controller
dispatch_mode: external-controller-courier
de_correlation_status: satisfied   # controller vendor/family differs from author -> cross_vendor_discovery
subagent_authority: no tester/testee shortcut used; the reviewing model is not the author/adjudicator of PR #508
```

## Review Target Integrity & Staleness

- Review base `86d7686a` and head `e9376ff9` both **present and reviewable** in the local object DB; the GitHub merge commit `c7743f72` is also present and is byte-identical to `e9376ff9` for all five target files (verified).
- The review was executed in an **isolated worktree checked out at `e9376ff9`** (`claude/bronze-projection-review-exec`), so read line numbers correspond to the pinned commit. `git status` empty before patch; `git diff --check` clean.
- `main` (HEAD `760fa28d`, includes PR #509) does **not** carry `data_lake/catalog.py` or `tests/test_data_lake_catalog.py`, and carries an older 3302-byte `run_ig_reels_grid_projection.py` (vs 4900 bytes at `e9376ff9`). **The reviewed Bronze-catalog projection path lives only on the `codex/bronze-v41-clean-verify` lineage, not on `main`.** Any code patch therefore targets that lineage, not `main` — consistent with the prompt's isolation decision. No staleness triggered: target files match the pins.

## Target Hash Verification

All five pins **match** (SHA256 of the CRLF working-tree checkout at `e9376ff9`; verified by byte-accurate `\n`->`\r\n` conversion of the git blob). The runner has no final newline, which broke a naive `sed` CRLF pass — the byte-accurate conversion matches.

| Target file | Pinned SHA256 (CRLF) | Result |
| --- | --- | --- |
| `data_lake/catalog.py` | `1F790C9A…EF02559` | ✅ match |
| `source_capture/ig_reels_grid_projection.py` | `15836206…EABFE04` | ✅ match |
| `runners/run_ig_reels_grid_projection.py` | `4F355F22…43F450FAE` | ✅ match |
| `tests/test_data_lake_catalog.py` | `D2B179D0…C2BA01BE` | ✅ match |
| `tests/unit/test_source_capture_ig_reels_projection.py` | `2AFFC8A5…F4A66874` | ✅ match |

No `HASH_MISMATCH`.

## Source Context Status — `SOURCE_CONTEXT_READY`

All pinned targets, the PR #508 diff, and the load-bearing dependencies were read. Material support files were read or their contract verified at call sites.

Source-read ledger:

| Source | Why | Status |
| --- | --- | --- |
| `data_lake/catalog.py` | Review target (`source_surface_catalog_rows`, AR-body resolution, path guards) | read @ `e9376ff9` |
| `source_capture/ig_reels_grid_projection.py` | Review target (`project_ig_reels_grid_from_bronze_catalog`, append, build) | read @ `e9376ff9` |
| `runners/run_ig_reels_grid_projection.py` | Review target (CLI branching) | read @ `e9376ff9` |
| `tests/test_data_lake_catalog.py` | Review target (catalog/AR/source-surface tests) | read @ `e9376ff9` |
| `tests/unit/test_source_capture_ig_reels_projection.py` | Review target (projection/runner tests) | read @ `e9376ff9` |
| `data_lake/root.py` | Support: `append_record` create-only semantics, `load_raw_packet` verification, sharding | read @ `e9376ff9` |
| `source_capture/models.py`, `ig_projection.py`, `ig_reels_grid.py`, `schemas/case_models.py`, `source_capture/writer.py` | Support: model shapes, forbidden-name guard, capture constants | **not separately opened**; contracts inferred from call sites + passing tests (disclosed gap — see Residual Risk) |
| `AGENTS.md`, `.agents/workflow-overlay/*` | Behavior kernel / review-lane / safety doctrine | supplied in context / overlay README read |

Method order honored: methods reference-loaded first; `SOURCE_CONTEXT_READY` declared; then deep-thinking failure-mode framing applied; then findings-first review + one bounded patch.

## Validation Run Status

Run in the review worktree at `e9376ff9` (Python 3.11.15, Windows).

| Check | Baseline (pre-patch) | Post-patch |
| --- | --- | --- |
| `py_compile` (3 production files) | PASSED | PASSED |
| `pytest` (both target test files) | **45 passed, 1 skipped** (matches dispatcher evidence) | **46 passed, 1 skipped** |
| `git diff --check` | clean | clean |

The 1 skip is the platform-gated directory-symlink test (`test_rebuild_catalog_rejects_symlinked_catalog_component`). `validation_not_run` does **not** apply — focused tests and diff checks ran.

## Findings (ordered by materiality)

### F1 — `record_id_prefix` suffix is positional over the catalog snapshot, not bound to packet identity → reruns are not cleanly idempotent  ·  Severity: **MEDIUM** (rerun-safety / operational traceability)

- **Target & purpose:** `project_ig_reels_grid_from_bronze_catalog` (`source_capture/ig_reels_grid_projection.py:404-430`), whose stated goal is a reliable, rerun-safe downstream projection path.
- **Evidence:** the derived record id is `f"{record_id_prefix}_{index:04d}"` where `index = enumerate(catalog_rows["packet_rows"], start=1)` (`ig_reels_grid_projection.py:405,422`). `packet_rows` is read from the generated `by_source_surface` JSONL, which is written **sorted by `packet_id`** (`catalog.py:1180`). So the numeric suffix is a position in the *current* sorted snapshot, carrying no packet identity. `append_record` is **create-only / no-overwrite** (`root.py:228-269,559-575` → `_atomic_create` → `os.link` raises `DataLakeRootError` on an existing target).
- **Consequence (verified by reasoning over the code):**
  - **Static catalog + same prefix:** index 1 maps to the same first packet → its record path already exists → hard `DataLakeRootError` on the *first* append. Clean only because the collision is first; there is no "skip already-projected, project only new" affordance.
  - **Grown catalog + same prefix:** a newly committed reels packet that sorts earlier shifts every later packet's suffix. `prefix_0001` now maps to the new packet (no existing path → **created**); `prefix_0002` maps to the old first packet, which previously held `prefix_0001`, so `prefix_0002` under that anchor does **not** exist → **created** — a *silent duplicate* projection of an already-projected packet. Net: same prefix on a grown catalog silently re-projects old packets under shifted numbers instead of failing closed or no-op'ing.
  - The derived **path** includes `packet_id` as `raw_anchor`, so there is no cross-packet overwrite or data corruption — the harm is confined to operator-facing traceability and rerun semantics, not integrity.
- **Authority/basis:** code + `root.py` create-only contract; live-evidence shows the prefix scheme produced `…run1_0001` (hyram) and `…run1_0002` (jeremyfragrance), confirming positional numbering across two packets.
- **Impact:** the operator-facing record id does not stably identify a packet across runs; the "rerun safety" property the commission asks about is partial (fail-closed for an unchanged catalog, silent-duplicate for a grown one). This matters most for the **next derived/Silver retrieval index**, which would otherwise inherit ambiguous record ids.
- **`minimum_closure_condition`:** either (a) bind the record id to packet identity (e.g. include `packet_id`/a content hash so the same packet yields a stable, collision-detectable id), **or** (b) explicitly document the positional semantics + the create-only rerun contract and add a regression test that pins both the static-rerun fail-closed and the grown-catalog behavior.
- **`next_authorized_action`:** **home-model adjudication required.** This is a durable derived record-id naming contract (high lock-in); it is deliberately **not patched** here (see Off-Scope). Recommend a decision before the Silver index is built on top.
- **Verification expectation:** after a chosen fix, a multi-packet test that commits ≥2 reels packets, projects with a prefix, then re-projects after committing a third earlier-sorting packet, asserting the intended (no-duplicate or fail-closed) behavior.
- **Patch applied?** No.

### F2 — No-prefix mode silently accumulates duplicate sibling projection records  ·  Severity: **LOW–MEDIUM** (downstream-index correctness)

- **Target & purpose:** `_append_ig_reels_grid_projection` (`ig_reels_grid_projection.py:433-447`) with `record_id=None` → `generate_ulid()` → a fresh unique id every run; `project_ig_reels_grid_from_bronze_catalog(record_id_prefix=None)` and `project_ig_reels_grid_into_lake(record_id=None)` both hit this.
- **Evidence (real lake, read-only):** under `derived/.../projection_ig_reels_grid/`, anchor `01KW9T70AM3SZE4VXKWG17ANZG` holds **3** distinct-ULID sibling records (`01KW9TZ6…`, `01KW9W6Q…`, `01KW9WBJ…`) — i.e. the same packet projected three times, each appending a new record with no dedup. Projection JSON is deterministic (`_projection_json_text` → `model_dump` sorted, no run-time fields), so these duplicates are **byte-identical**, hence harmless to integrity but unbounded in count.
- **Authority/basis:** code + observed lake state (8 total `projection_ig_reels_grid` records = 6 legacy-flat ULID + 2 sharded run1).
- **Impact:** consistent with append-only lane semantics, but the next derived/Silver retrieval index **must dedupe** (by content hash or by stable record id) or it will multi-count the same projection. No idempotence/collision messaging exists for the no-prefix path.
- **`minimum_closure_condition`:** document that no-prefix runs are non-idempotent and that the Silver index must dedupe; or provide an opt-in idempotence guard.
- **`next_authorized_action`:** decision input for the Silver-index design lane; no code patch (append-only is by design).
- **Patch applied?** No.

### F3 — `source_surface_catalog_rows` returns an inconsistent key set on the no-matching-surface path  ·  Severity: **LOW** (return-contract integrity)  ·  **PATCH APPLIED**

- **Target:** `source_surface_catalog_rows` (`catalog.py:340-347` pre-patch).
- **Evidence:** the populated return includes `packet_rows`, `attachment_record_query_rows`, and `attachment_record_rows` (`catalog.py:362-372`), but the `surface_row is None` early return omitted `attachment_record_query_rows`. A consumer iterating `catalog_rows["attachment_record_query_rows"]` would `KeyError` only on the no-match path. The current consumer reads only `packet_rows` and `attachment_record_rows`, so this is latent today — but the helper is exported (`__all__`) and its contract should be uniform.
- **`minimum_closure_condition`:** the empty-surface branch returns the same key set as the populated branch.
- **Patch applied?** **Yes** — added `"attachment_record_query_rows": []` to the empty branch + a regression test (`test_source_surface_catalog_rows_absent_surface_returns_consistent_shape`). Uncommitted working-tree diff below. Post-patch tests: 46 passed, 1 skipped.

### F4 — Test-durability gaps vs commissioned axes  ·  Severity: **LOW** (review-confidence)

- **Evidence:** the suite does **not** cover three commissioned axes:
  1. **Multi-packet projection from one source surface** — `test_project_reels_grid_from_bronze_catalog_uses_source_surface_and_ar_rows` commits **one** reels packet. The live 2-packet behavior (and the per-packet AR-row grouping in `attachment_records_by_packet`) is exercised only in production, not by a regression test.
  2. **Bronze-path rerun** — no test for the create-only collision (same prefix) or no-prefix duplication of `project_ig_reels_grid_from_bronze_catalog` (cf. F1/F2). `test_project_reels_grid_explicit_record_id_is_create_only` covers only the `into_lake` path.
  3. **Runner incompatible-flag rejection** — the runner's `ValueError` guards (`run_ig_reels_grid_projection.py:64-66,80-82,93-98`: `--record-id-prefix` only with `--bronze-source-surface`; `--record-id` only with `--packet-id`; `--data-root` only with `--packet-id`/`--bronze-source-surface`) are untested; only the happy bronze path is.
- **`minimum_closure_condition`:** add the three tests. Note that the multi-packet test should be authored **after** F1 is adjudicated, so it does not cement the positional-suffix semantics under review.
- **`next_authorized_action`:** recommended test additions (test files are in `may_edit`); deferred pending F1 decision to avoid encoding a contested contract. The F3 patch adds one of the missing no-match-path tests.
- **Patch applied?** Partial (F3 test only).

### F5 — Redundant verified raw loads per projection call  ·  Severity: **INFORMATIONAL** (operational cost, not correctness)

- **Evidence:** `project_ig_reels_grid_from_bronze_catalog` calls `source_surface_catalog_rows` → `inspect_catalog` → `_build_entries`, which **loads and hashes every committed raw packet** in the lake (`catalog.py:191,375-416`); then for each projected packet it calls `load_raw_packet` again (`ig_reels_grid_projection.py:407`) and `load_attachment_record_body` re-calls `load_raw_packet` once per AR row (`catalog.py:1136`). Cost is O(catalog) + O(preserved_files per matched packet) verified reads per call. For the reels surface (1 preserved file/packet) the duplication is small; it compounds for packets with many preserved files or large catalogs.
- **Assessment:** the full `inspect_catalog` is the price of the fail-closed staleness guard (a correct, deliberate trade). The re-loads are belt-and-suspenders verification, not a defect.
- **`next_authorized_action`:** none required; note for scale planning. No patch.

### F6 — Confirmations (not defects)

- **Post-run catalog cleanliness is correct by design.** The Bronze catalog indexes only **committed raw packets** (`_iter_committed_packet_ids` walks `raw/` only — `catalog.py:573-589`); appending records under `derived/` cannot change the raw-derived expected snapshot, so census stays `ok`. An operator could *mistakenly* expect the Bronze catalog to index derived projection outputs — it does not, and should not; indexing derived outputs is the future Silver/`derived_retrieval` index's job. The `authority`/`completeness` strings make this explicit.
- **View-only / non-judgment semantics preserved.** Both cited records carry `certification = "view_only; not_cleaned; not_normalized; not_judgment_ready"`, `binding_map = []`, and `projection_method = ig_reels_grid_mechanical_projection`; the row model enforces the forbidden-Judgment-field guard and value/posture coupling (`ig_reels_grid_projection.py:148-171`). No certification/traction/normalization overclaim introduced by the catalog path.
- **Strong verified-read chain.** `load_attachment_record_body` re-resolves the body from raw and checks `relative_packet_path` + `body_sha256` against the manifest **and** re-hashes the bytes (`catalog.py:1122-1157`); `_catalog_generated_path` + `_read_attachment_record_catalog_entry` reject traversal/unsafe `attachment_record_id` (`catalog.py:535-570`). The generated catalog is treated as a hint, never as authority — exactly the property the downstream lane needs.
- **Shared-surface cross-family filtering is handled.** `by_source_surface_path`/`attachment_records_path` are keyed by surface only and may mix families; `source_surface_catalog_rows` re-filters rows by `source_family` **and** `source_surface` (`catalog.py:348-357`), covered by `test_source_surface_attachment_path_is_surface_bucket_not_family_bucket`.

### F7 — Latent `KeyError` if a caller passes bodies missing the (non-slice-referenced) capture file  ·  Severity: **INFORMATIONAL**

- **Evidence:** `build_ig_reels_grid_projection` validates that **slice-referenced** file ids are present (`ig_reels_grid_projection.py:225-228`) but then unconditionally indexes `raw_file_bytes_by_file_id[capture_file.file_id]` in `_load_capture_payload` (`:730`). If a caller supplied a bodies map omitting the capture file while the capture file is not referenced by any slice, this raises a bare `KeyError` rather than a typed, actionable error.
- **Assessment:** **not reachable** via either production caller — the catalog path passes bytes for *all* the packet's preserved files (every preserved file has an AR row), and the directory path loads all files. Robustness wart only.
- **`next_authorized_action`:** optional future hardening (typed error on missing capture body); **not patched** (out of the live path; would be speculative).

## Patch Summary & Unified Diff

One bounded, uncommitted working-tree patch (F3 only). Files within `reviewer_patch_scope.may_edit`. No record-id contract change, no behavior change for existing consumers; pure return-shape consistency + its regression test.

```diff
diff --git a/orca-harness/data_lake/catalog.py b/orca-harness/data_lake/catalog.py
index db5a352a..0080a01a 100644
--- a/orca-harness/data_lake/catalog.py
+++ b/orca-harness/data_lake/catalog.py
@@ -343,6 +343,7 @@ def source_surface_catalog_rows(
             "source_surface": surface,
             "catalog_query_paths": {},
             "packet_rows": [],
+            "attachment_record_query_rows": [],
             "attachment_record_rows": [],
         }
     packet_rows = [
diff --git a/orca-harness/tests/test_data_lake_catalog.py b/orca-harness/tests/test_data_lake_catalog.py
index c95e166c..260bdfd4 100644
--- a/orca-harness/tests/test_data_lake_catalog.py
+++ b/orca-harness/tests/test_data_lake_catalog.py
@@ -731,6 +731,28 @@ def test_source_surface_catalog_rows_require_current_generated_catalog(
         )


+def test_source_surface_catalog_rows_absent_surface_returns_consistent_shape(
+    tmp_path: Path,
+) -> None:
+    # A current catalog with no matching (family, surface) bucket must return the SAME
+    # key set as a populated result, so a downstream consumer that iterates
+    # attachment_record_query_rows does not KeyError on the no-match path.
+    root = DataLakeRoot.for_test(tmp_path / "orca-data")
+    _write_reddit_packet(root, tmp_path)
+    assert rebuild_catalog(root)["status"] == "rebuilt"
+
+    rows = source_surface_catalog_rows(
+        root,
+        source_family="instagram_creator",
+        source_surface="surface_not_present_v0",
+    )
+
+    assert rows["catalog_query_paths"] == {}
+    assert rows["packet_rows"] == []
+    assert rows["attachment_record_query_rows"] == []
+    assert rows["attachment_record_rows"] == []
+
+
 def test_catalog_coverage_census_caps_issue_samples(tmp_path: Path) -> None:
     root = DataLakeRoot.for_test(tmp_path / "orca-data")
     for index in range(30):
```

Patch location: uncommitted in worktree `…/.claude/worktrees/bronze-projection-review-exec` (branch `claude/bronze-projection-review-exec`, base `e9376ff9`). Not committed, not pushed — handed to the home model to adjudicate/keep/discard.

## Live-Operation Evidence — Read-Only Verification

`F:/orca-data-lake` was treated **strictly read-only** (no rebuild, no projection rerun, no writes).

| Evidence item | Result |
| --- | --- |
| Derived shard math for both packets (`ddd`, `f00`) | ✅ matches cited paths (`anchor_shard = sha256(packet_id)[:3]`) |
| Record `…run1_0001.json` (hyram) | ✅ present; SHA256 `2B629ABA…0267EC` match; `packet_id=01KW9T6R7BFDJKG7WSW7PMVSMP`; rows=10; certification + `binding_map=[]` as cited |
| Record `…run1_0002.json` (jeremyfragrance) | ✅ present; SHA256 `730A8159…6047DA52` match; `packet_id=01KWA193403TYNTBJVWAP5W5NE`; rows=37; certification + `binding_map=[]` as cited |
| Projection record count moved 6 → 8 (evidence pt 8) | ✅ confirmed: **8 total** = 6 legacy-flat ULID records + 2 new sharded `run1` records |
| **Observation (not in evidence):** derived layout is **mixed** | The 6 prior records are in the **legacy flat** layout (`derived/<anchor>/…`); the 2 new bronze records are in the **sharded** layout (`derived/<shard>/<anchor>/…`). The `derived/` subtree has not been run through `relocate_to_sharded`. This does **not** affect PR #508 (the bronze path only appends; it does not read existing derived records) but is a live operational state the future Silver index must account for. |

Census evidence items 2–4 and 9 (raw census counts: 101 packets / 222 AR / 7 surfaces, stale→clean) were **not** independently re-verified — a full `inspect_catalog` over the real lake is heavyweight and tangential to the code review; only the derived-record evidence and counts above were re-read.

## Off-Scope Flags

- **F1 record-id contract is intentionally NOT patched.** Binding the derived record id to packet identity is a durable naming-contract / architecture decision (high lock-in, affects the future Silver index). Per the commission ("if the correct fix is architectural … return `NEEDS_ARCHITECTURE_PASS` or an off-scope flag rather than patching around it"), this is flagged for home-model decision, not patched. → **`NEEDS_ARCHITECTURE_PASS` for F1's record-id identity binding.**
- No edits to `F:/orca-data-lake`, generated catalog files, derived records, overlay, repo map, doctrine, unrelated runners, or the review prompt. Real-lake kept read-only.
- Report written to the prompt-pinned path `docs/review-outputs/…` (root). The folder README now prefers `adversarial-artifact-reviews/` for new reports; the prompt's `required_review_report_path`/`downstream_consumers` pin the root path, so the pinned path wins. Relocation is an owner call (see Open Questions).

## Open Questions

1. **F1 decision:** should the derived record id be packet-identity-bound (stable, collision-detectable) or are positional-suffix + create-only-rerun semantics acceptable and merely under-documented? This gates the Silver-index design.
2. **F2 / Silver index:** will the next derived/Silver retrieval index dedupe projection records (by content hash or stable id), given no-prefix runs accumulate byte-identical duplicates?
3. **Mixed derived layout:** is the real lake's coexisting flat + sharded `derived/` intended, or should `relocate_to_sharded` be run before the Silver index reads derived records by key?
4. **Report placement:** keep at `docs/review-outputs/` root (prompt-pinned) or relocate to `adversarial-artifact-reviews/` per the folder README default?

## Residual Risk

- Support models (`source_capture/models.py`, `ig_projection.py`, `ig_reels_grid.py`, `case_models.py`, `writer.py`) were **not separately opened**; their contracts were inferred from call sites and the passing suite. A defect isolated to those modules and not exercised by the focused tests would not be caught here.
- The real-lake raw census numbers (101/222/7) were taken from the dispatcher's evidence, not independently recomputed.
- Findings F1/F2 are reasoned + corroborated by observed lake state but were not reproduced by executing a fresh bronze projection run (real-lake mutation is unauthorized).
- The bounded patch was validated by the focused suite only; no full-repo test run was performed.

## Review-Use Boundary

Findings and the diff are **decision input only.** They are not approval, validation, readiness, mandatory remediation, source promotion, or executor-ready merge authority until separately accepted or authorized. `real-lake mutation`, `formal approval`, `readiness`, `validation pass/fail`, `source promotion`, and `merge authority` are **`NOT_CLAIMED`**.

```yaml
reviewed_by: claude-opus-4.8
authored_by: OpenAI/Codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

---

```text
DELEGATED_CODE_REVIEW_PATCH_RETURN_FOR_HOME_MODEL

Here is the delegated code review-and-patch result. Adjudicate it under the delegated-review-patch return contract.

- original commission: delegated adversarial code review-and-patch of PR #508's Bronze source-surface IG reels-grid projection consumption path + real-lake convergence evidence (prompt: docs/prompts/reviews/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_prompt_v0.md).
- implementation context, diff, reviewed files: PR #508 single commit e9376ff9 (base 86d7686a), +356/−3 over 5 files: data_lake/catalog.py (source_surface_catalog_rows + AR query/body resolvers + path guards), source_capture/ig_reels_grid_projection.py (project_ig_reels_grid_from_bronze_catalog + _append_ig_reels_grid_projection), runners/run_ig_reels_grid_projection.py (--bronze-source-surface / --record-id-prefix CLI branch), and the two target test files. Reviewed at the pinned commit in an isolated worktree.
- live operation evidence inspected: both cited derived records re-read read-only (SHA256, packet_id, row count, certification all match); projection count confirmed 6→8 (6 legacy-flat ULID + 2 new sharded run1); F:/orca-data-lake kept read-only; mixed flat/sharded derived layout observed.
- findings: F1 (MEDIUM) positional record_id_prefix suffix not bound to packet identity -> reruns fail-closed on a static catalog but SILENTLY DUPLICATE on a grown catalog (no clean idempotence); F2 (LOW-MED) no-prefix mode accumulates byte-identical duplicate records (observed: 3 siblings under one anchor) -> Silver index must dedupe; F3 (LOW, PATCHED) inconsistent return-shape on the no-match path; F4 (LOW) missing multi-packet / rerun / runner-flag-rejection tests; F5/F7 informational; F6 confirmations (catalog-clean-by-design, view-only preserved, strong verified-read chain).
- proposed patch / working-tree diff: one bounded uncommitted diff (catalog.py one-line return-shape fix + one regression test). Uncommitted in worktree branch claude/bronze-projection-review-exec.
- citations: file:line anchors throughout (catalog.py, ig_reels_grid_projection.py, run_ig_reels_grid_projection.py, root.py).
- reviewer verdict/recommendation: no blocker/major correctness defect in the merged path; the verified-read + fail-closed + view-only properties hold. Before building the derived/Silver retrieval index, ADJUDICATE F1 (record-id identity binding — flagged NEEDS_ARCHITECTURE_PASS) and F2 (dedupe contract). Findings-only; no readiness/merge claim.
- validation evidence: py_compile PASSED; focused pytest 45→46 passed, 1 skipped; git diff --check clean (pre and post patch). Real-lake raw census numbers not independently recomputed; support models inferred from call sites.
- residual risk / off-scope / not-proven: support models not separately opened; F1/F2 reasoned + lake-state-corroborated but not reproduced via a live rerun (unauthorized); F1 record-id contract NOT patched (off-scope architecture decision); real-lake kept read-only.
```

For this review, real-lake mutation, formal approval, readiness, validation pass/fail, source promotion, and merge authority are `NOT_CLAIMED`.
