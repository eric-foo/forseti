# Bronze Data Lake Doctor — Delegated Adversarial Code Review-and-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch output (decision input only)
scope: >
  Cross-vendor delegated adversarial code review-and-patch of PR #478, the
  Bronze v4.1 data-lake doctor runner and focused tests.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8 (Anthropic)
authored_by: OpenAI Codex / GPT-5
de_correlation_bar: cross_vendor_discovery
reviewed_commit: 924321bafed3214321cc5817bdc10b8280724f1c
base_commit: efc4ed7cd83642acf8119f83f38d50b82b023d14
pr: https://github.com/eric-foo/orca/pull/478
prompt: docs/prompts/reviews/bronze_data_lake_doctor_delegated_adversarial_code_review_patch_prompt_v0.md
worktree: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-v41-clean-verify
status: completed
recommendation: accept_with_friction
```

## Home-Model Adjudication Addendum (Codex)

- Decision: accept the delegated F1/F2 patch with one home-model modification before final acceptance.
- Modification: F1 closure was extended to surface legacy-flat `raw/<packet_id>/` containers that are packet-id-named but missing `manifest.json`; without this, the same fake-clean class still existed outside sharded raw layout.
- Added home-model regression test: `test_inspect_data_lake_reports_legacy_flat_missing_manifest`.
- Final validation after adjudication: `tests/test_data_lake_doctor.py` = 9 passed; broader capture/silver/lake seam suite = 140 passed, 1 skipped; `git diff --check` clean.

## 1. Commission, Lane Binding, and Actor/Model-Family Receipt

- **Commission**: explicit owner invocation `prompt - delegate review patch`, filed prompt
  `docs/prompts/reviews/bronze_data_lake_doctor_delegated_adversarial_code_review_patch_prompt_v0.md`,
  to determine whether the Bronze data-lake doctor runner is safe to keep, needs bounded
  patching, or must route back for architecture/scoping.
- **Lane**: `delegated_code_review_and_patch` sibling mode, `repo` access, `base-subagent`
  controller, per `.agents/workflow-overlay/delegated-review-patch.md`. Review method is
  `workflow-code-review` (deep-thinking first, source-gated), per Review Prompt Defaults in
  `.agents/workflow-overlay/prompt-orchestration.md`. Not a bound/formal review lane; output is
  decision input for CA adjudication.
- **Actor/model-family receipt**:
  - `author_home_model_family`: OpenAI / Codex / GPT-5 (the commissioning/implementation lane).
  - `controller_model_family`: Anthropic / Claude Opus 4.8 (this review).
  - `de_correlation_status`: **satisfied** — author vendor (OpenAI) ≠ delegate vendor (Anthropic),
    so the `cross_vendor_discovery` bar is met. No `same_vendor_sanity` fallback needed; no
    self-review (the subagent-authority "no tester/testee shortcut" gate is cleared because the
    receiving family differs from the author family).
  - `dispatch_mode`: external-controller-courier; the receiver inspected the pinned worktree
    directly (no substituted summary or recreated source pack).
- **No runtime-model recommendation** is made anywhere in this report; the family receipt is a
  who-constraint only.

### Controlling source state (stale_if gate — all conditions hold)

- PR #478 base = `main` @ `efc4ed7cd83642acf8119f83f38d50b82b023d14`, state OPEN/draft —
  not retargeted, base unchanged (`gh pr view 478`).
- Worktree HEAD `23444d04` = pinned `924321ba` + exactly one later commit
  (`23444d04 Add Bronze doctor delegated review prompt`, 244 insertions, the prompt artifact
  only). **No target file changed since the pin** (`git diff --name-only 924321ba..HEAD -- <targets>`
  empty). The `dirty_state_allowance` "ignore the prompt-file commit" exception applies.
- `input_hashes` verified byte-for-byte at the working tree (= pinned state for the targets):
  - `docs/workflows/orca_repo_map_v0.md` = `5b2897bf…4db9` ✓
  - `orca-harness/runners/run_data_lake_doctor.py` = `5c68a7e3…44a8` ✓
  - `orca-harness/tests/test_data_lake_doctor.py` = `92153922…1222` ✓
- Overlay authority (delegated-review-patch, review-lanes, prompt-orchestration, source-loading)
  read at branch state (based on `efc4ed7c`); unchanged relative to the pin.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

- **Governance read**: `AGENTS.md`; `.agents/workflow-overlay/{README,delegated-review-patch,
  review-lanes,prompt-orchestration,decision-routing,source-loading}.md`;
  `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`.
- **Implementation read (full)**: pinned target diff; `orca-harness/runners/run_data_lake_doctor.py`;
  `orca-harness/tests/test_data_lake_doctor.py`; `orca-harness/data_lake/root.py` (the controlling
  v4.1 API: `load_raw_packet`, `rebuild_availability`, `record_availability`,
  `_availability_entry_from_raw`, `raw_shard`, `resolve`, `for_test`, `find_packet`, markers,
  `LAKE_SUBDIRECTORIES`).
- **Deliberately not read (with reason)**:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md` —
    no finding depends on storage-contract doctrine vs. implementation behavior; the doctor is
    judged against `root.py`'s actual API and the report's own invariants.
  - `tests/test_data_lake_sharding.py`, `tests/test_data_lake_availability.py` — `root.py` is the
    primary source; both were instead **executed** in the broader seam suite (139 passed).
- No source conflicts; no missing finding-bearing source.

## 3. Findings (severity-ordered)

No **critical** findings. Two **major** (both patched within bounded scope), four **minor**
(flagged; not patched).

### F1 — MAJOR — manifest-less raw container is a silent false-clean — PATCHED

- **target label**: `[bronze-doctor-runner]`
- **location**: `orca-harness/runners/run_data_lake_doctor.py`, `_raw_candidates`
  (pre-patch lines 90–94: `manifest = container / "manifest.json"` / `if not manifest.is_file(): continue`).
- **issue**: A directory `raw/<shard>/<packet_id>/` whose name is a valid Crockford-26 packet id
  but which has **no `manifest.json`** was silently skipped — neither counted, nor classified
  `malformed`, nor surfaced anywhere in the report.
- **evidence**: The pre-patch container loop `continue`d on a missing manifest before any
  classification. Independently, `DataLakeRoot.rebuild_availability` (`root.py:922-929`) also
  requires `(container / "manifest.json").is_file()` to index, so it likewise skips such a
  container. The two skips compound: no raw-candidate entry → no `missing_availability` flag
  either. Constructed false-clean: a lake with one good packet plus one manifest-less container
  (e.g. `allocate_raw_packet_dir` followed by a crash before the manifest write, an interrupted
  publish, or a manually deleted manifest) reports `status: "ok"`, `raw_packet_count: 1`, all
  issue lists empty.
- **impact**: The doctor's single most important promise — "make raw corruption visible" — fails
  for a plausible partial-write/partial-delete corruption class. A fake success path
  (`AGENTS.md` kernel: "Preserve real failure visibility; never create fake success paths").
- **minimum_closure_condition**: A packet-id-named raw container with no manifest, or any
  non-conforming directory under a shard dir, is reported as an issue and flips `status` to
  `issues_found` without being counted as a valid packet.
- **next_authorized_action**: CA adjudicates the applied patch (below).
- **patched**: **yes** — name-check reordered ahead of the manifest check; a manifest-less
  packet-id container now lands in a new `missing_manifest_raw_containers` report key (added to
  `issue_keys`); a non-packet-id directory now lands in `malformed_raw_containers` regardless of
  whether it has a manifest (previously a manifest-less non-packet dir also vanished). Regression
  test `test_inspect_data_lake_reports_missing_manifest_container` added.

### F2 — MAJOR — the two most dangerous false-passes were untested — PATCHED

- **target label**: `[bronze-doctor-tests]`
- **location**: `orca-harness/tests/test_data_lake_doctor.py` (pre-patch: 5 tests).
- **issue**: Two failure modes the prompt explicitly names as "most dangerous false passes" had
  **no test coverage**:
  - (F2a) a committed, indexed packet whose preserved **body bytes are corrupt** — caught only by
    the `load_raw_packet` read-verification pass (`run_data_lake_doctor.py:211-222`), since the
    availability index still matches the untouched manifest. No test corrupted a body, so a future
    edit that dropped the read-verification loop would keep all 5 tests green while body corruption
    went silent.
  - (F2b) a `--packet-id` lookup for a **missing/unreadable** packet ("CLI output hiding packet
    errors"). The only CLI test (`test_main_prints_json_packet_lookup`) exercised the happy path
    only; the error path (`_packet_report` → `{"error": …}` → `status: issues_found` → exit 1) was
    unverified.
- **evidence**: Pre-patch test file asserted clean/missing/stale/wrong-shard/CLI-success only;
  `read_failures` and the packet-error path appear in no assertion.
- **impact**: The corruption-detection crux and the operator's by-key error signal were
  regression-unprotected — a silent guarantee, not a tested one.
- **minimum_closure_condition**: Tests assert that (a) a corrupt body yields a non-empty
  `read_failures`, `verified_raw_packet_count < raw_packet_count`, and `issues_found` while the
  index reads clean; and (b) `main` with an absent `--packet-id` returns exit 1 with
  `packet.error` present.
- **next_authorized_action**: CA adjudicates the applied patch.
- **patched**: **yes** — added `test_inspect_data_lake_reports_read_failure_on_corrupt_body`
  (F2a) and `test_main_packet_lookup_reports_missing_packet_error` (F2b), plus the F1 regression
  test. Import of `generate_ulid` added. All 8 doctor tests pass.

### F3 — MINOR — read-only doctor inherits `resolve()`'s writability precondition — NOT PATCHED (off-scope)

- **target label**: `[bronze-doctor-runner]` (root cause off-scope in `root.py`)
- **location**: `main` → `DataLakeRoot.resolve` (`root.py:416-417`, `os.access(path, os.W_OK)`).
- **issue**: The doctor's default mode is read-only, but its only entry into a root is the
  production `resolve`, which fails closed when the root is not writable. An operator pointing the
  doctor at a genuinely read-only / archived / permission-restricted root gets exit 2
  "data root is not writable" instead of a clean read-only inspection.
- **impact**: Bounded — the v4.1 lake is a single-operator local lake normally on writable media,
  and `--rebuild-availability` legitimately needs write. The gap is inspecting an archived/read-only
  copy.
- **minimum_closure_condition**: Either `root.py` exposes a read-only resolve path (off-scope), or
  the doctor documents that inspection requires a writable root.
- **next_authorized_action**: owner decision — accept the limitation, or commission a separate
  `root.py` change (a new commission; outside this PR's named target set).
- **patched**: **no** — fixing it requires editing `orca-harness/data_lake/root.py`, which is
  explicitly read-only/flag-only for this commission.

### F4 — MINOR — `_expected_availability` duplicates root.py's private entry builder (drift risk) — NOT PATCHED

- **target label**: `[bronze-doctor-runner]`
- **location**: `run_data_lake_doctor.py:56-66` (`_expected_availability`) vs.
  `root.py:284-299` (`_availability_entry_from_raw`).
- **issue**: The doctor re-implements the 6-field availability entry rather than calling a shared
  function (root.py's builder is underscore-private; there is no public "expected entry" API). If
  `root.py` changes the entry schema, the doctor's recomputation drifts.
- **impact**: Asymmetric. A **format change** to one of the 6 shared fields would make the doctor
  flag every entry `stale` (a false-positive storm) — but this is **caught today** by
  `test_inspect_data_lake_reports_clean_root` (drift → stale → that test fails), so it cannot ship
  silently. A **new field** added in `root.py` would be silently unchecked by the doctor (it
  compares only its 6 known fields) — lower harm (under-validation, not a false alarm), and not
  caught by the clean test.
- **minimum_closure_condition**: Either `root.py` exposes a public expected-entry helper the doctor
  reuses (off-scope), or a parity assertion pins the duplication.
- **next_authorized_action**: owner decision; optional in-scope hardening noted in §"Optional".
- **patched**: **no** — the clean-root test already guards the dangerous (false-stale) drift; the
  full fix needs a `root.py` API addition (off-scope). Flagged rather than over-built.

### F5 — MINOR — stray non-directory entries under `raw/` are not surfaced — NOT PATCHED (intentional)

- **target label**: `[bronze-doctor-runner]`
- **location**: `_raw_candidates` (`if not first.is_dir(): continue`; `if not container.is_dir(): continue`).
- **issue**: A plain **file** directly under `raw/` or under a shard dir is silently skipped.
- **assessment**: This is a **deliberate non-finding**. Stray files there are most often OS cruft
  (`.DS_Store`, `Thumbs.db`); flagging them would generate operator-facing false issues. Genuine
  packet corruption manifests as directories (handled by F1) or as read/hash failures (handled by
  `load_raw_packet`). Surfacing stray files is not worth the false-positive noise.
- **next_authorized_action**: none; recorded so the bounded blind spot is explicit, not accidental.
- **patched**: **no** (intentional; surfacing it would widen scope and add noise).

### F6 — MINOR — repo-map row omits malformed/missing-manifest from the doctor's enumerated outputs — NOT PATCHED

- **target label**: `[repo-map-route]`
- **location**: `docs/workflows/orca_repo_map_v0.md` (the `run_data_lake_doctor.py` row).
- **issue**: The row enumerates "availability-index gaps/staleness/orphans, wrong-shard or
  legacy-flat raw packets, read/hash failures, and unexpected top-level folders" but omits
  `malformed_raw_containers` and (post-F1) `missing_manifest_raw_containers`.
- **assessment**: **Not an overclaim** — the row claims no Bronze validation, lake readiness,
  Silver coordination, deployment, or live-data-root safety; it is an accurate, bounded,
  illustrative-not-exhaustive route description. The omission is minor incompleteness.
- **minimum_closure_condition**: (optional) the row notes the malformed/missing-manifest signals,
  or remains accurate as an illustrative enumeration.
- **next_authorized_action**: owner decision; optional.
- **patched**: **no** — smallest-complete: the row is accurate and not made wrong by the F1 fix;
  editing it would widen scope beyond closing a blocker/major.

### Non-findings confirmed (review breadth)

Each prompt review-question was checked and the doctor passed, except where noted above:

- **Read-only by default; mutation gated**: only `rebuild_availability()` writes, only under
  `--rebuild-availability` (`run_data_lake_doctor.py:173`); test 2 confirms a dry run does not
  recreate a deleted availability file.
- **No silent init/migrate/repair/delete/move of raw**: `resolve` never initializes; the doctor
  never calls `initialize`/`relocate_to_sharded`/`allocate_*`; `rebuild_availability` touches only
  `indexes/availability` (`root.py:905-933`), never `raw/`.
- **Availability anomalies without trusting the index as authority**: missing, stale (incl.
  `manifest_sha256`), unreadable, invalid-name, and orphan are all derived by comparing the index
  against truth recomputed from raw (`run_data_lake_doctor.py:112-132, 197-224`).
- **Read verification depth**: `load_raw_packet` (`root.py:797-883`) fails closed on missing
  packet/manifest, non-object manifest, empty/!list `preserved_files`, missing/invalid `file_id`,
  duplicate `file_id`, absolute/escaping/unsafe `relative_packet_path`, missing file, `size_bytes`
  mismatch, and `sha256` mismatch — the doctor's `read_failures` / `verified_raw_packet_count` rest
  on a sound backstop (now tested — F2a).
- **Packet lookup reports missing/unreadable as an issue, not fake success**: `_packet_report`
  returns `{"error": …}` and `status` flips to `issues_found` → exit 1 (now tested — F2b).
- **`--rebuild-availability` still surfaces raw corruption the rebuild skips**: rebuild indexes by
  manifest only, so a valid-manifest/corrupt-body packet is re-indexed yet still fails the doctor's
  read pass (`read_failures`); wrong-shard packets the rebuild skips remain in
  `wrong_shard_packets`. Confirmed by construction.
- **No semantic Bronze folders; traceability intact**: `semantic_folder_violations` flags only
  unexpected top-level **directories** (`_ALLOWED_ROOT_DIRS` derived from `LAKE_SUBDIRECTORIES`, so
  `.staging`/`raw`/`indexes`/etc. allowed; the marker files are not directories, so not misflagged);
  the report carries packet ids, container relpaths, and field lists for operator traceability and
  creates no semantic folders.
- **Production `resolve` boundary intact; tests do not weaken the outside-repo guard**: tests use
  `for_test` (the documented test-only bypass); `test_main_prints_json_packet_lookup` and the new
  F2b test monkeypatch `resolve` transiently (auto-reverted), leaving the guard logic untouched.
- **Patch stayed in PR scope**: only the two named code files were touched; no `root.py`,
  architecture, semantic-folder, capture/Silver runner, or CI changes.

## 4. Findings Table (compact)

| ID | Severity | Target | Patched | One-line |
| --- | --- | --- | --- | --- |
| F1 | major | `[bronze-doctor-runner]` | yes | Manifest-less raw container was a silent false-clean. |
| F2 | major | `[bronze-doctor-tests]` | yes | Corrupt-body read-failure and missing-packet CLI error were untested. |
| F3 | minor | `[bronze-doctor-runner]` | no (off-scope) | Read-only doctor inherits `resolve()`'s writable-root requirement. |
| F4 | minor | `[bronze-doctor-runner]` | no | Doctor re-implements root.py's availability entry (drift risk; clean test guards the dangerous case). |
| F5 | minor | `[bronze-doctor-runner]` | no (intentional) | Stray files under `raw/` not surfaced (avoids OS-cruft noise). |
| F6 | minor | `[repo-map-route]` | no | Repo-map row omits malformed/missing-manifest (illustrative, not an overclaim). |

## 5. Unified Diff (applied to the two named target files; uncommitted working tree)

```diff
diff --git a/orca-harness/runners/run_data_lake_doctor.py b/orca-harness/runners/run_data_lake_doctor.py
--- a/orca-harness/runners/run_data_lake_doctor.py
+++ b/orca-harness/runners/run_data_lake_doctor.py
@@ def _raw_candidates
-def _raw_candidates(root: DataLakeRoot) -> tuple[list[_RawCandidate], list[str], list[str], list[str]]:
+def _raw_candidates(
+    root: DataLakeRoot,
+) -> tuple[list[_RawCandidate], list[str], list[str], list[str], list[str]]:
     valid: list[_RawCandidate] = []
     wrong_shard: list[str] = []
     legacy_flat: list[str] = []
     malformed: list[str] = []
+    missing_manifest: list[str] = []
     raw_dir = root.path / "raw"
     if not raw_dir.is_dir():
-        return valid, wrong_shard, legacy_flat, malformed
+        return valid, wrong_shard, legacy_flat, malformed, missing_manifest
@@ container loop
         for container in sorted(first.iterdir()):
             if not container.is_dir():
                 continue
-            manifest = container / "manifest.json"
-            if not manifest.is_file():
-                continue
             if not _PACKET_ID.fullmatch(container.name):
+                # Any non-packet-id directory under a shard dir is a
+                # non-conforming raw container; surface it instead of skipping
+                # (previously a manifest-less stray here vanished from the report).
                 malformed.append(_rel(root, container))
                 continue
+            manifest = container / "manifest.json"
+            if not manifest.is_file():
+                # A packet-id-named container with no manifest is a partial or
+                # corrupted committed packet (aborted allocate, half publish, or
+                # a deleted manifest). It must stay visible: skipping it silently
+                # lets a corrupt packet read as a clean lake, and rebuild_availability
+                # also skips it, so absence here would hide it entirely.
+                missing_manifest.append(_rel(root, container))
+                continue
             if first.name != raw_shard(container.name):
                 wrong_shard.append(_rel(root, container))
                 continue
             valid.append(...)
-    return valid, wrong_shard, legacy_flat, malformed
+    return valid, wrong_shard, legacy_flat, malformed, missing_manifest
@@ inspect_data_lake
-    raw_candidates, wrong_shard, legacy_flat, malformed = _raw_candidates(root)
+    raw_candidates, wrong_shard, legacy_flat, malformed, missing_manifest = _raw_candidates(root)
@@ report dict
         "malformed_raw_containers": malformed,
+        "missing_manifest_raw_containers": missing_manifest,
@@ issue_keys
         "malformed_raw_containers",
+        "missing_manifest_raw_containers",

diff --git a/orca-harness/tests/test_data_lake_doctor.py b/orca-harness/tests/test_data_lake_doctor.py
--- a/orca-harness/tests/test_data_lake_doctor.py
+++ b/orca-harness/tests/test_data_lake_doctor.py
@@ imports
 from data_lake.root import DataLakeRoot, raw_shard
+from harness_utils import generate_ulid
 from runners import run_data_lake_doctor as doctor
@@ appended after test_main_prints_json_packet_lookup
+def test_inspect_data_lake_reports_read_failure_on_corrupt_body(tmp_path): ...   # F2a
+def test_inspect_data_lake_reports_missing_manifest_container(tmp_path): ...      # F1 regression
+def test_main_packet_lookup_reports_missing_packet_error(tmp_path, monkeypatch, capsys): ...  # F2b
```

(The full, exact diff is the working-tree `git diff` of the two files; the abbreviation above
omits only unchanged context lines and test bodies.)

## 6. Per-Change Neutral Source Citations

- **F1 patch** — `run_data_lake_doctor.py` `_raw_candidates`: the pre-patch loop skipped a
  manifest-less container (`if not manifest.is_file(): continue`) before classification.
  `root.py:922-929` (`rebuild_availability`) gates indexing on `(container / "manifest.json").is_file()`,
  so a manifest-less container is also un-indexed; with no raw candidate emitted, the doctor's
  `missing_availability` derivation (`run_data_lake_doctor.py:197-199`, keyed off `raw_candidates`)
  cannot flag it either. `_PACKET_ID` (`run_data_lake_doctor.py:26`) and `raw_shard`
  (`root.py:95-98`) define the packet-id grammar and shard mapping used by the reordered checks.
- **F2a test** — `load_raw_packet` re-hashes each preserved file against the manifest `sha256` and
  raises on size/sha mismatch (`root.py:861-881`); the doctor records that as a `read_failure` and
  withholds the `verified_raw_packet_count` increment (`run_data_lake_doctor.py:211-222`). The
  availability entry's `manifest_sha256` is computed from the manifest, not the body
  (`root.py:298`, `_availability_entry_from_raw`), so a body-only corruption leaves the index
  matching — the assertion that `missing_availability`/`stale_availability` stay empty is
  source-correct.
- **F2b test** — `_packet_report` returns `{"packet_id", "error"}` on `DataLakeRootError`
  (`run_data_lake_doctor.py:145-149`); `has_issue` includes `packet.get("error")`
  (`run_data_lake_doctor.py:264-266`); `main` returns `0 if status == "ok" else 1`
  (`run_data_lake_doctor.py:307`). `find_packet` raises via `_validate_packet_id` / returns `None`
  for an absent id (`root.py:791-795, 806-808`), so a fresh `generate_ulid()` lookup yields the
  error path.
- **F3 citation** — `resolve` requires `os.access(path, os.W_OK)` (`root.py:416-417`); the doctor's
  `main` resolves via this production path (`run_data_lake_doctor.py:297`).
- **F4 citation** — doctor `_expected_availability` (`run_data_lake_doctor.py:56-66`) and root
  `_availability_entry_from_raw` (`root.py:284-299`) compute the same 6 fields independently;
  `_AVAILABILITY_FIELDS` (`run_data_lake_doctor.py:27-34`) is the doctor's comparison set;
  `test_inspect_data_lake_reports_clean_root` asserts `status == "ok"` (no stale), which fails on a
  shared-field format drift.

## 7. Controller Verdict and Residual Risk

- **Verdict**: `accept_with_friction`. The doctor is structurally sound for its stated job —
  read-only by default, mutation correctly gated to the rebuildable index, the common corruption
  classes surfaced, the production resolve boundary intact, no semantic Bronze folders, and a sound
  `load_raw_packet` read backstop. The one real false-clean (F1) and the two untested
  most-dangerous false-passes (F2) are closed by a bounded patch inside the two named files; the
  remaining items are minor and either off-scope or intentional. No `NEEDS_ARCHITECTURE_PASS`: this
  is patch-level, not design-level.
- **Residual risk**: (a) F3/F4 root causes live in `root.py` and are left as owner decisions — the
  doctor cannot inspect a read-only root, and a future `root.py` availability-schema change could
  drift the doctor (the dangerous false-stale variant is test-guarded; a new-field variant is not).
  (b) The patch is **uncommitted working-tree change** in `worktrees/bronze-v41-clean-verify`; it is
  decision input, not a kept change, until CA adjudication and commit. (c) F1's regression test and
  the corrupt-body test pin the new guarantees, but coverage of `legacy_flat`, `orphan`, and
  `semantic_folder_violations` paths remains indirect (not added — outside the major-issue bar).

## 8. Validation Run Status

All commands run from `worktrees/bronze-v41-clean-verify/orca-harness` unless noted. Real results:

- `python -m compileall -q runners/run_data_lake_doctor.py tests/test_data_lake_doctor.py` →
  **pass** (`COMPILE_OK`).
- `python -m pytest -p no:cacheprovider --no-header tests/test_data_lake_doctor.py` →
  **`8 passed in 1.45s`** (baseline pre-patch was `5 passed`; +3 new tests).
- Broader lake seam suite (the 16-file set named in the prompt) →
  **`139 passed, 1 skipped in 12.46s`** (baseline pre-patch `136 passed, 1 skipped`; +3 new tests,
  no regressions; the 1 skip is pre-existing). Run because the patch changes inspection
  classification logic, not only wording.
- `git diff --check` (repo root) → **clean** (`WHITESPACE_CLEAN`).
- **Not run** (correctly): `check_repo_map_freshness.py` and `check_map_links.py` — the repo-map
  route (`docs/workflows/orca_repo_map_v0.md`) was **not** changed (F6 left unpatched), so the
  repo-map hooks do not apply.

## 9. Off-Scope Flags

- **F3 / F4 root cause** in `orca-harness/data_lake/root.py` — read-only/flag-only for this
  commission; a read-only resolve path and/or a public expected-availability helper would each be a
  separate commission touching `root.py`. Not patched.
- No other file outside the named two-file set was modified. No staging, commit, push, PR,
  dependency install, network access, live `ORCA_DATA_ROOT` access, or live capture occurred.

## 10. CA Adjudication Packet

- **Commission**: delegated `repo`-mode code review-and-patch, PR #478, three named targets
  (two code + repo-map); patch bounded to the two code files; repo-map flag-only outcome (F6).
- **Target**: `run_data_lake_doctor.py`, `test_data_lake_doctor.py` (patched);
  `orca_repo_map_v0.md` (reviewed, not patched).
- **Authority**: provisional `delegated_code_review_and_patch`; decision input only; CA holds final
  keep/veto.
- **Decision criteria**: false-clean elimination, read-only/gated-mutation integrity, corruption
  visibility (raw/index/shard/read), no semantic Bronze folders, production-boundary integrity,
  in-scope patch.
- **Evidence**: §6 citations; §8 validation (8 doctor tests + 139/1-skip seam suite green;
  whitespace clean).
- **Reviewer recommendation**: `accept_with_friction` — keep F1+F2 patches after adjudication;
  decide F3/F4 as owner items (likely a separate `root.py` commission); F5 accept as intentional;
  F6 optional.
- **Next moves for the CA** (admin batched; material deep-thought):
  - *Admin (one step, no deep-thinking)*: review the working-tree diff in
    `worktrees/bronze-v41-clean-verify`; if accepted, stage/commit the two files to
    `codex/bronze-v41-clean-verify` and let PR #478 update — these are the harness-gated push/PR
    actions, owner-gated.
  - *Material*: decide whether F3 (read-only-root inspection) and F4 (availability-schema drift)
    warrant a `root.py` commission now or are accepted residuals for the v4.1 single-operator
    deployment.

### Optional (non-required) hardening

- F4: a parity assertion test (capture a packet, assert the doctor's `_expected_availability`
  equals the stored `read_availability` entry for all of `_AVAILABILITY_FIELDS`) would also pin the
  new-field drift variant. Deliberately not added — the clean-root test already guards the
  dangerous false-stale variant, and the new-field variant is low-harm under-validation.
- F6: optionally extend the repo-map row to mention malformed/missing-manifest signals. Not
  required; the row is accurate as an illustrative enumeration.

## 11. Review-Use Boundary

This delegated review-and-patch result is **decision input only**. The diff, citations, and verdict
are claims for the commissioning Chief Architect to adjudicate, not premises to inherit. This is not
owner acceptance, validation proof, readiness, deployment, live data-lake safety, source-capture
authorization, Silver coordination proof, or permission to keep any patch without CA adjudication.
The patch is an uncommitted working-tree change until the CA accepts and commits it.
