# TikTok Full-Grid Bronze Admission — Delegated Adversarial Code Review-and-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial code review-and-patch result)
scope: >
  De-correlated cross-vendor controller review of branch
  codex/tiktok-full-grid-bronze-admission (worktree
  C:\tmp\forseti-tiktok-full-grid-bronze-admission), HEAD
  b890c58aee567ba038d745a4cff9b1ca25d102f6, base
  41b078e3ed3c6bcf1424588a8dc8423f3f1c19fc: preserving the full observed
  onboarding grid window and its bound selection receipt beside
  selected-video deep captures in one TikTok Bronze admission packet,
  bounded to the five named writer/runner/test files in the commission
  prompt.
use_when:
  - Adjudicating whether the TikTok full-grid Bronze admission change is
    settled before merge.
  - Checking whether the new onboarding-evidence validation in
    batch_packet.py actually enforces the fitness contract's nine points.
authority_boundary: retrieval_only
reviewed_by: claude-sonnet-5
authored_by: OpenAI / Codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
mode: delegated_code_review_and_patch
access: repo
review_use_boundary: >
  Findings, patches, citations, verdicts, and test claims are decision
  input for home-model adjudication only; they are not validation,
  readiness, approval, acceptance, or merge authority.
branch_or_commit: codex/tiktok-full-grid-bronze-admission @ b890c58aee567ba038d745a4cff9b1ca25d102f6
```

## 1. Commission, Lane Binding, And Actor/Model-Family Receipt

- commission: `delegated_code_review_and_patch` sibling mode, commissioned via
  the prompt file
  `docs/prompts/reviews/tiktok_full_grid_bronze_admission_delegated_adversarial_code_review_patch_prompt_v0.md`,
  pointed to by the operator's chat instruction "execute".
- review_lane: code (`workflow-code-review`), preceded by inline
  deep-thinking framing of the shared evidence-contract risks (byte-hash
  binding symmetry between capture-time and admission-time checks, the
  self-declared-completeness trust boundary, cross-module validator
  consistency, and schema-version blast radius) per the commission's
  "Required Reads And Method Order".
- mode: `repo` access, `delegated_code_review_and_patch` sibling mode.
  Reviewed and patched directly in the commissioned worktree
  `C:\tmp\forseti-tiktok-full-grid-bronze-admission` (a registered worktree
  of this same repository, distinct from the controller's own active
  worktree `tiktok-grid-selection-review-0ab1c6`), so no shared state was
  disturbed.
- target_kind: bounded 5-file implementation/test diff; everything else
  read-only / flag-only.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI / Codex (per the commission's
    `author_home_model_family` field).
  - controller_model_family: Anthropic / Claude (`claude-sonnet-5`).
  - de_correlation_status: `satisfied` — cross-vendor (Anthropic vs OpenAI
    are different vendors per `.agents/workflow-overlay/delegated-review-patch.md`
    De-correlation criterion).
- target-state preflight (all independently verified live, not inherited
  from the commission's own claims):
  - worktree found via `git worktree list` at the exact commissioned path,
    on branch `codex/tiktok-full-grid-bronze-admission`, HEAD
    `b890c58aee567ba038d745a4cff9b1ca25d102f6`.
  - `git status --short --branch`: clean, no untracked files, at review
    start.
  - `git merge-base --is-ancestor 41b078e3ed3c6bcf1424588a8dc8423f3f1c19fc HEAD`:
    exit 0 (ancestry confirmed).
  - `git diff --name-status <base>...HEAD`: exactly the five named target
    files plus the commission prompt itself (`docs/prompts/reviews/...md`,
    added) — no additional changed code file.
  - `sha256sum` on all five named target files matched the commission's
    pinned hashes exactly, byte for byte.
- this commission is decision input only: not approval, validation,
  readiness, merge authority, or proof of correctness beyond what is
  explicitly evidenced below.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

Source-read ledger:

- Reviewed the full diff from base to HEAD over all five named targets
  (675 lines) plus full current-state reads of all five target files.
- Read-only, out-of-named-scope corroboration reads (to check whether the
  new validation is internally consistent with its producers/consumers,
  not to patch): `source_capture/tiktok/creator_onboarding.py` (full
  `run_tiktok_creator_onboarding` control flow, `build_tiktok_grid_window`,
  `_is_creator_video_url`, `TikTokCreatorOnboardingOutputPaths` and
  `_output_paths`), `source_capture/tiktok/grid_video_selection.py`
  (`build_tiktok_grid_video_selection` shape), `source_capture/tiktok/admission.py`
  (`assert_no_sensitive_tiktok_material`, `_SENSITIVE_KEYS`,
  `_RAW_TIKTOK_URL_RE`, `_collect_sensitive` recursion), `source_capture/packet_assembly.py`
  (`staged_file_id_map`, `stage_and_write_packet`), and
  `source_capture/tiktok/batch_coverage.py` (`_tiktok_batch_capture_preserved_file`,
  to check the schema-version bump's blast radius on the coverage
  consumer).
- Authority: `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/review-lanes.md`,
  `.agents/workflow-overlay/delegated-review-patch.md` (targeted per the
  routine read shape: "When it applies", "The loop", "Access selection
  rule", "De-correlation", "Overlay Interface", and "Code-diff target
  kind").
- Repo-wide `grep` for `tiktok_batch_capture_admission_v0` and
  `capture_schema_version` to check whether any consumer hardcodes the
  pre-diff schema-version literal (none found outside `batch_packet.py`
  itself; the one symbolic reference in
  `tests/unit/test_tiktok_creator_metric_seed.py` imports the constant, so
  it tracks the bump automatically).

No source conflicts found. No missing source blocked a finding.

## 3. Review Questions — Tested, Not Accepted

Numbered against the commission's "Adversarial Questions" list.

1. **Can malformed, author-mismatched, stale-hash, partial, duplicate, or
   unrelated grid/selection inputs publish any packet?** No, for every
   dimension exercised: creator-handle mismatch (grid and selection,
   case-insensitive), `complete != true`, empty items, `window_size`
   mismatch, duplicate `video_id`, non-matching `video_url` (see F1 for a
   confirmed related defect in *how* this was checked), stale
   `grid_window_sha256`, wrong `grid_window_file` name, `coverage.complete
   != true`, coverage count mismatch, duplicate/non-covering
   `ranked_items`, empty/duplicate selected ids, and `selection_count`
   mismatch all raise `ValueError` before `stage_and_write_packet` is
   reached (traced line-by-line in `_validate_onboarding_evidence`,
   `batch_packet.py:209-337` pre-patch numbering). See F2 for the test
   coverage gap this leaves.
2. **Can a selection claim one set while ranked rows or cadence admit
   another?** No. `selected_from_rows` (computed from `ranked_items[].selected
   is True`) must equal `set(selected_ids)` (from `selection_summary`), and
   both must equal `set(admitted_ids)` (from the actually-normalized batch
   `videos` list) — three independent representations of "who was
   selected" are cross-checked for set equality. See F2: the
   `ranked_items`-vs-`selection_summary` leg of this specific check has no
   dedicated test.
3. **Can split recovery runs create duplicates, omit a selected video, or
   admit an unselected video without failing?** No, for the layer this
   diff touches. `admitted_ids` duplicate check (`len(set(admitted_ids)) !=
   len(admitted_ids)`) plus the final `set(admitted_ids) != set(selected_ids)`
   equality check together reject all three failure modes. This relies on
   the pre-existing `_classify_cadence_failures` superseded-failure logic
   (unchanged by this diff, out of the named patch scope) to have already
   deduplicated legitimately-superseded split-run rows before `videos` is
   built; that logic was read for context but not re-audited end-to-end
   since it is untouched code outside the five named files.
4. **Are preserved-file IDs computed after the final staged file list, and
   do manifests/source slices expose all three exact files?** Yes, verified
   by reading `packet_assembly.staged_file_id_map` (assigns `file_{index:02d}`
   in the order of the `staged_artifacts` sequence it is given) against
   `batch_packet.py`'s call site: `staged_artifacts` is built (with the
   grid-window/selection entries conditionally appended) *before*
   `staged_file_id_map(staged_artifacts)` is called, and
   `preserved_file_ids=[file_ids[name] for name, _raw in staged_artifacts]`
   iterates that same final list — not a hardcoded `[file_ids[TIKTOK_BATCH_CAPTURE_JSON_NAME]]`
   as the pre-diff code did. Confirmed by test
   `test_write_tiktok_batch_packet_preserves_complete_onboarding_evidence`,
   which asserts the exact three-entry `relative_packet_path` order, and
   independently by the standalone-runner test
   `test_tiktok_batch_runner_can_re_admit_complete_onboarding_staging`.
5. **Can exact-byte preservation leak material that the parsed safety check
   misses?** No new gap introduced. `assert_no_sensitive_tiktok_material(grid)`
   / `(selection)` runs on the fully parsed JSON object before the raw
   bytes are staged; `_collect_sensitive` (`admission.py:360-388`)
   recursively walks every dict key and list/tuple element, so any string
   value present in the raw bytes is also reachable as a string value in
   the parsed structure the check walks — a JSON round-trip does not hide
   content from a value-level recursive scanner. This was verified
   empirically, not just by reading: my own added test
   (`test_write_tiktok_batch_packet_accepts_scraped_video_url_variants`,
   first draft) supplied a `video_url` containing a query string and the
   check correctly raised `"raw TikTok URL with query string"` before
   admission — the safety check fires *before* my `_is_creator_video_url`
   fix would even be reached for that case.
6. **Does the v1 schema bump break any current batch coverage, projection,
   Silver, inventory, or policy-version consumer?** No consumer found.
   `batch_coverage._tiktok_batch_capture_preserved_file` locates the
   packet's batch-capture file by filename suffix
   (`.endswith(TIKTOK_BATCH_CAPTURE_JSON_NAME)`), not by index or preserved-file
   count, so the two newly-added preserved files do not break it. No
   consumer in the repo hardcodes the literal
   `"tiktok_batch_capture_admission_v0"` string; the one existing test that
   asserts the schema-version value imports the module constant
   symbolically and tracks the bump automatically.
7. **Are path/name checks portable and are TikTok handle comparisons
   correctly case-insensitive?** Yes for handle comparisons (`.lstrip("@").lower()`
   used consistently on both the grid and selection creator-handle
   bindings). Grid-window filename matching uses `Path(...).name`
   (portable, not raw string equality). See F1 for the one path/URL check
   that was *not* appropriately lenient relative to its own producer.
8. **Does the standalone runner truthfully record all four input
   receipts?** Yes.
   `run_source_capture_tiktok_batch_packet.py` conditionally appends
   `grid_window_json`/`selection_result_json` receipts only when the
   corresponding path was actually supplied and read, in the same order
   consumed downstream; `run_source_capture_tiktok_creator_onboarding.py`'s
   admission block always supplies all four (`grid_result_json`,
   `cadence_result_json_1`, `grid_window_json`, `selection_result_json`)
   since supervised onboarding always produces all four artifacts by the
   time it reaches the admission call (see question 9).
9. **Does onboarding wire the full artifacts only after successful
   staging, and does any admission failure remain visible?** Yes, traced
   through `creator_onboarding.run_tiktok_creator_onboarding`: `grid_window_json_path`
   and `selection_json_path` are written mid-flow (before `deep_capture`),
   but the function *raises* on any later-stage failure — including the
   explicit `status != "complete"` check after `deep_capture` — so
   `run_source_capture_tiktok_creator_onboarding.py`'s `main()` never
   reaches its admission block (`paths` is never returned) unless
   onboarding fully succeeded. Admission-time validation failures
   (`ValueError` from `_validate_onboarding_evidence`) propagate through
   the runner's broad `except Exception` to `parser.exit(status=3, ...)`,
   which is visible (non-zero exit, message printed), not swallowed.
10. **Are the tests strong enough to fail on swapped files, stale hashes,
    missing pair members, mismatched IDs, and accidental legacy-shape
    changes?** Partially — see F2 (confirmed test-coverage gap).

## 4. Findings (Ordered By Materiality)

### F1 [major, medium confidence] — `video_url` admission check was stricter than the capture-time validator that produces the value (patched)

- target: `[batch-packet]` (`source_capture/tiktok/batch_packet.py`).
- location (pre-patch): `_validate_onboarding_evidence`, the per-item grid
  loop (`video_url.lower() != f"{creator_profile_url}/video/{video_id}".lower()`).
- issue: the grid-item `video_url` field is populated in
  `creator_onboarding.build_tiktok_grid_window` from `row.get("video_url")`
  — a value scraped verbatim from live TikTok DOM markup — gated only by
  `creator_onboarding._is_creator_video_url`, which tolerates `http` or
  `https` scheme and any `tiktok.com` or `*.tiktok.com` host, checking only
  the URL *path*. The pre-patch admission-time check in `batch_packet.py`
  instead required byte-exact equality against a synthetically
  reconstructed canonical string
  (`f"{creator_profile_url}/video/{video_id}"`, i.e. always `https://www.tiktok.com/...`).
  A legitimately-captured grid item whose scraped href used `http://`, a
  non-`www` `tiktok.com` subdomain, or a trailing slash would be accepted
  by the capture-time validator but rejected by the stricter admission-time
  check, aborting the entire batch admission with a `ValueError` for a
  correct, non-malicious capture.
- evidence: read `creator_onboarding.py:707-720` (`_is_creator_video_url`)
  against the pre-patch `batch_packet.py` equality check; confirmed the
  asymmetry is real by writing a regression test with an
  `http://m.tiktok.com/...` href, which failed against the pre-patch
  equality check and passes after the fix. (A query-string variant was
  also tried first and is independently rejected earlier by
  `assert_no_sensitive_tiktok_material` — see question 5 above — so the
  real-world blast radius of this specific defect is scheme/subdomain/
  trailing-slash variance, not query strings.)
- impact: could have caused correct, non-malicious supervised-onboarding
  admissions to fail outright if TikTok's live grid markup ever emits an
  href in a form `_is_creator_video_url` already accepts but the strict
  admission-time string match did not — i.e., a false-positive rejection
  of the exact feature this commission adds, defeating fitness-contract
  point 7 ("Supervised onboarding passes the full grid and selection to
  the existing writer whenever admission is requested") for no security
  benefit, since the two checks were meant to enforce the same invariant.
  Not runtime-verified against live TikTok markup (no live capture was
  run, per the commission's lifecycle hard stop); confidence is `medium`
  because the risk is demonstrated by code-level inconsistency between two
  validators for the same field, not by an observed live failure.
- minimum_closure_condition: the admission-time `video_url` check accepts
  exactly the set of URLs the capture-time `_is_creator_video_url` check
  accepts (same host/scheme/path tolerance), so no capture that passed
  capture-time validation can fail admission-time validation for the same
  reason.
- next_authorized_action: patch within `[batch-packet]` (named target).
- patched? **yes.** Added a local `_is_creator_video_url` helper in
  `batch_packet.py` (self-contained — not imported from
  `creator_onboarding.py`, to avoid a cross-module private-function
  coupling outside the named patch scope) that mirrors the same
  scheme/host/path tolerance, and replaced the strict-equality check with
  it. The now-unused `creator_profile_url` parameter was removed from
  `_validate_onboarding_evidence` and its call site (it was only consumed
  by the removed check). Two regression tests added:
  `test_write_tiktok_batch_packet_accepts_scraped_video_url_variants`
  (proves the tolerant check still admits a legitimate `http://m.tiktok.com/...`
  href) and `test_write_tiktok_batch_packet_rejects_grid_video_url_for_wrong_creator`
  (proves the loosened check still correctly rejects a video_url pointing
  at a different creator's handle).

### F2 [minor, high confidence] — most `_validate_onboarding_evidence` raise branches have no dedicated negative-path test

- target: `[batch-packet-tests]` (`tests/unit/test_tiktok_batch_admission.py`).
- location: `_validate_onboarding_evidence` has roughly 15 distinct
  `raise ValueError` branches; the diff's new tests exercise the happy
  path plus 3 negative branches directly (pair-required-together,
  stale-hash binding, admitted-vs-selected mismatch) — now 5 with this
  patch's 2 additions (F1's regression tests). The remaining branches —
  grid creator_handle mismatch, empty items, `window_size` mismatch,
  duplicate grid `video_id`, selection-binding creator_handle mismatch,
  `grid_window_file` name mismatch, `coverage.complete != true`, coverage
  count mismatch, duplicate/non-covering `ranked_items`, empty/duplicate
  selected ids, `selection_count` mismatch, and — notably — the internal
  `selected_from_rows != set(selected_ids)` consistency check between
  `ranked_items` and `selection_summary` — have no test that reaches them.
  The one test whose name suggests it covers that last branch
  (`test_write_tiktok_batch_packet_rejects_selection_not_matching_deep_captures`)
  actually falls through to the final admitted-vs-selected check instead
  (traced by hand: after its fixture mutation, `selected_from_rows` still
  equals `set(selected_ids)`, so that specific branch never fires in that
  test).
- evidence: line-by-line enumeration of every `raise ValueError` in
  `_validate_onboarding_evidence` cross-referenced against every
  `pytest.raises` call and its `match=` string in the test file.
- impact: a future accidental regression to any of the untested branches
  (e.g. someone loosens the duplicate-`video_id` check while refactoring)
  would not be caught by this test suite — this is exactly the failure
  mode the delegated-review-and-patch convention exists to guard against
  for "high-stakes authored artifacts... where the author encodes
  guardrails and can reintroduce the exact failure mode those guardrails
  exist to prevent." The guardrails themselves are correct (confirmed by
  question 1 above); only their regression coverage is thin.
- minimum_closure_condition: each `_validate_onboarding_evidence` raise
  branch has at least one dedicated test whose failure would be caused
  specifically by that branch's condition, not incidentally by a
  different, later branch.
- next_authorized_action: owner decision — whether to authorize a broader
  test-hardening pass now or defer it. Not patched in this commission:
  adding ~10 more negative-path tests for branches this diff already
  implements correctly (verified by direct reading, not just by test
  absence) is beyond "the smallest complete TikTok Bronze admission
  change" this commission scopes, and beyond the two tests F1's own fix
  required. Flagged here as coverage-first policy requires, not patched.

## 5. Considered And Defended

- Candidate: `grid.get("complete")` / `coverage.get("complete")` are
  trusted at face value with no independent scroll-exhaustion or
  `window_cap` corroboration; a hand-crafted `grid_window.json` supplied
  through the standalone `--grid-window-json` CLI path could claim
  `complete: true` with very few items. Defended: the fitness contract's
  own wording ("Admission fails... when creator identity, grid
  completeness/size/uniqueness... do not agree") names *completeness* as
  a checked field, and the check does verify it (`complete is True` plus
  `window_size == len(items)`); requiring independent corroboration of
  *how* the producer arrived at that boolean is out of this diff's scope
  and would require re-deriving the producer's own scroll/response-target
  logic inside the consumer, which the fitness contract explicitly
  excludes ("does not claim longitudinal current-view semantics...
  selection correctness, metric validity").
- Candidate: the two hardcoded-`True` fields in `onboarding_evidence`
  (`selection_grid_window_binding_verified`, `selected_deep_capture_coverage_verified`)
  are tautological, since any failing check raises before the dict
  literal is ever constructed, so they can never be observed as `False`.
  Defended: this is a fail-closed design, not a fake-success path — the
  packet simply is never written when either would have been `False`.
  Read as an audit-stamp ("this specific check ran and passed for this
  packet") rather than a variable per-instance signal, the naming is
  reasonable; noted here rather than as a finding since no code path lets
  it lie.
- Candidate: `TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION` bumps from `_v0` to
  `_v1` unconditionally, even for legacy callers that never supply
  onboarding evidence. Defended: no consumer hardcodes the pre-diff
  literal (question 6 above); the bump reflects a genuine schema-shape
  change (a new optional top-level key was added to what the schema can
  contain), which is a defensible bump trigger independent of whether any
  given instance uses the new key.
- Candidate: `--grid-result-json` (legacy profile-list enrichment input)
  and `--grid-window-json` (new onboarding-evidence artifact) are two
  distinct "grid" concepts with similarly-named CLI flags on the
  standalone runner, easy for an operator to transpose. Defended as a
  naming-clarity note, not a code defect: the two flags are independently
  typed (`Path`), independently validated downstream, and a transposition
  would fail loudly (wrong JSON shape) rather than silently.

## 6. Patches Applied

**One.** F1 (major, confirmed) was patched in `batch_packet.py`, with two
regression tests added in `tests/unit/test_tiktok_batch_admission.py`. No
other file in the five-file named scope was touched. F2 (minor, confirmed
test-coverage gap) was reported but not patched — see F2's
`next_authorized_action`. `git status --short` after the patch shows only
`batch_packet.py` and `test_tiktok_batch_admission.py` modified; the other
three named files are untouched. `git diff --check` is clean (exit 0).

```diff
diff --git a/forseti-harness/source_capture/tiktok/batch_packet.py b/forseti-harness/source_capture/tiktok/batch_packet.py
index 3c0912fb..8ed9cb2e 100644
--- a/forseti-harness/source_capture/tiktok/batch_packet.py
+++ b/forseti-harness/source_capture/tiktok/batch_packet.py
@@ -93,7 +93,6 @@ def write_tiktok_batch_packet(
     )
     onboarding_evidence = _validate_onboarding_evidence(
         creator_handle=handle,
-        creator_profile_url=profile_url,
         grid_window_json=grid_window_json,
         selection_result_json=selection_result_json,
         admitted_video_ids=[str(video["video_id"]) for video in payload["videos"]],
@@ -189,10 +188,28 @@ def write_tiktok_batch_packet(
     return 0, result.output_directory


+def _is_creator_video_url(*, video_url: str, creator_handle: str, video_id: str) -> bool:
+    """Match the capture-time tolerance in creator_onboarding._is_creator_video_url.
+
+    Grid hrefs are scraped from live TikTok markup, not synthesized, so this
+    intentionally tolerates http scheme and tiktok.com subdomains that a
+    strict canonical-URL string match would reject even though the upstream
+    capture-time validator already accepted them. A query string is still
+    rejected, but earlier and separately, by assert_no_sensitive_tiktok_material.
+    """
+    parsed = urlparse(video_url)
+    host = (parsed.hostname or "").lower()
+    expected_path = f"/@{creator_handle.lower()}/video/{video_id}"
+    return (
+        parsed.scheme in {"http", "https"}
+        and (host == "tiktok.com" or host.endswith(".tiktok.com"))
+        and parsed.path.rstrip("/").lower() == expected_path.lower()
+    )
+
+
 def _validate_onboarding_evidence(
     *,
     creator_handle: str,
-    creator_profile_url: str,
     grid_window_json: bytes | None,
     selection_result_json: bytes | None,
     admitted_video_ids: Sequence[str],
@@ -233,7 +250,9 @@ def _validate_onboarding_evidence(
             )
         if video_id in grid_ids:
             raise ValueError(f"grid_window_json contains duplicate video_id={video_id}")
-        if video_url.lower() != f"{creator_profile_url}/video/{video_id}".lower():
+        if not _is_creator_video_url(
+            video_url=video_url, creator_handle=creator_handle, video_id=video_id
+        ):
             raise ValueError(
                 f"grid_window_json.items[{index}] video_url does not match creator/video_id"
             )
diff --git a/forseti-harness/tests/unit/test_tiktok_batch_admission.py b/forseti-harness/tests/unit/test_tiktok_batch_admission.py
index c377490f..f70db460 100644
--- a/forseti-harness/tests/unit/test_tiktok_batch_admission.py
+++ b/forseti-harness/tests/unit/test_tiktok_batch_admission.py
@@ -443,6 +443,99 @@ def test_write_tiktok_batch_packet_rejects_selection_not_matching_deep_captures(
     assert not output.exists()


+def test_write_tiktok_batch_packet_accepts_scraped_video_url_variants(
+    tmp_path: Path,
+) -> None:
+    output = tmp_path / "batch_packet"
+    grid = {
+        "schema_version": "tiktok_creator_onboarding_v0",
+        "creator_handle": "funmimonet",
+        "window_size": 2,
+        "window_cap": 30,
+        "minimum_window_size": 2,
+        "complete": True,
+        "items": [
+            {
+                "video_id": VIDEO_1,
+                "video_url": f"http://m.tiktok.com/@funmimonet/video/{VIDEO_1}/",
+                "playCount": 1000,
+                "diggCount": 45,
+            },
+            {
+                "video_id": VIDEO_2,
+                "video_url": f"{PROFILE_URL}/video/{VIDEO_2}",
+                "playCount": 2000,
+                "diggCount": 90,
+            },
+        ],
+    }
+    grid_bytes = (json.dumps(grid, indent=2, sort_keys=True) + "\n").encode("utf-8")
+    selection = {
+        "schema_version": "tiktok_grid_video_selection_v1",
+        "coverage": {
+            "complete": True,
+            "expected_item_count": 2,
+            "observed_item_count": 2,
+        },
+        "onboarding_binding": {
+            "creator_handle": "funmimonet",
+            "grid_window_file": "tiktok_grid_window.json",
+            "grid_window_sha256": hashlib.sha256(grid_bytes).hexdigest(),
+        },
+        "ranked_items": [
+            {"video_id": VIDEO_2, "selected": True},
+            {"video_id": VIDEO_1, "selected": True},
+        ],
+        "selection_summary": {
+            "selection_count": 2,
+            "selected_video_ids_in_review_priority_order": [VIDEO_2, VIDEO_1],
+        },
+    }
+    selection_bytes = (json.dumps(selection, indent=2, sort_keys=True) + "\n").encode("utf-8")
+
+    code, message = write_tiktok_batch_packet(
+        creator_handle="funmimonet",
+        creator_profile_url=PROFILE_URL,
+        grid_result_json=_grid_payload(),
+        cadence_result_jsons=[_cadence_payload()],
+        grid_window_json=grid_bytes,
+        selection_result_json=selection_bytes,
+        output_directory=output,
+        capture_timestamp="2026-06-30T17:02:46Z",
+    )
+
+    assert code == 0
+    assert Path(message) == output.resolve()
+
+
+def test_write_tiktok_batch_packet_rejects_grid_video_url_for_wrong_creator(
+    tmp_path: Path,
+) -> None:
+    output = tmp_path / "batch_packet"
+    grid_window, selection = _onboarding_evidence_payloads()
+    grid_payload = json.loads(grid_window)
+    grid_payload["items"][0]["video_url"] = f"https://www.tiktok.com/@someoneelse/video/{VIDEO_1}"
+    grid_window = (json.dumps(grid_payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
+    selection_payload = json.loads(selection)
+    selection_payload["onboarding_binding"]["grid_window_sha256"] = hashlib.sha256(
+        grid_window
+    ).hexdigest()
+    selection = (json.dumps(selection_payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
+
+    with pytest.raises(ValueError, match="video_url does not match creator/video_id"):
+        write_tiktok_batch_packet(
+            creator_handle="funmimonet",
+            creator_profile_url=PROFILE_URL,
+            grid_result_json=_grid_payload(),
+            cadence_result_jsons=[_cadence_payload()],
+            grid_window_json=grid_window,
+            selection_result_json=selection,
+            output_directory=output,
+        )
+
+    assert not output.exists()
+
+
 def test_write_tiktok_batch_packet_preserves_dom_visible_comment_fallback(tmp_path: Path) -> None:
     output = tmp_path / "batch_packet"
     row = _result_row(VIDEO_1, 1761930827, subtitle=False)
```

## 7. Validation Commands And Observed Results

Run from the commissioned worktree
(`C:\tmp\forseti-tiktok-full-grid-bronze-admission`), after the F1 patch,
`PYTHONDONTWRITEBYTECODE=1`:

```text
$ python -m pytest -p no:cacheprovider -q --basetemp <tmp>/pytest-tiktok-bronze-review \
    forseti-harness/tests/unit/test_tiktok_batch_admission.py \
    forseti-harness/tests/unit/test_tiktok_batch_coverage.py \
    forseti-harness/tests/unit/test_tiktok_batch_projection.py \
    forseti-harness/tests/unit/test_tiktok_live_batch_probe.py \
    forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
........................................................................ [ 69%]
...............................                                          [100%]
(exit 0; 103 dot-progress markers = 101 baseline + 2 new F1 regression tests;
no FAILED lines)

$ python -m pytest -p no:cacheprovider -q --basetemp <tmp>/pytest-tiktok-bronze-review-contract \
    forseti-harness/tests/contract
........................................................................ [ 57%]
.....................................................                    [100%]
(exit 0; 125 dot-progress markers, matches the commission's baseline of
"125 passed"; no FAILED lines)

$ git diff --check
(clean; exit 0)

$ python .agents/hooks/check_review_routing.py --strict
check_review_routing --strict: OK (base: origin/main)
(exit 0)
```

The commission's fourth baseline item — "actual Noel staging proof: one
packet with 29 grid rows, 8 selected/deep captures, three preserved files,
both stored hashes matching, and both linkage verification booleans true" —
was **not rerun**. It requires a live TikTok capture / real staging
fixture that is not available to this controller and is explicitly
out-of-scope under the commission's lifecycle hard stop ("Do not run live
TikTok/browser capture"). The controller's own regression tests
(`test_write_tiktok_batch_packet_preserves_complete_onboarding_evidence`
and this patch's two additions) exercise the same code path with synthetic
fixtures and pass; the live-staging claim itself remains `not proven` by
this review and is carried forward as a residual (§9).

## 8. Overall Advisory Verdict And Sub-Verdicts

- **Overall: accept, one confirmed-and-patched major finding, one
  confirmed-and-reported minor finding.** The diff correctly implements
  the stated fitness contract's admission logic — all nine fitness points
  and eight of ten adversarial questions were traced to a specific,
  correct enforcement in code; the ninth (test-coverage strength) is
  correctly implemented but thinly tested (F2); the one real defect found
  (F1) was an internal-consistency gap between two validators for the same
  field, not a security or admission-correctness hole — it would have
  caused false-positive *rejections* of legitimate captures, not
  false-positive *admissions* of bad ones.
- `[batch-packet]`: correct after F1 patch. Byte-hash binding, coverage
  agreement, ranked-row/selection-summary/admitted-cadence three-way
  cross-check, and preserved-file-id ordering all hold under adversarial
  reading and empirical test verification.
- `[batch-packet-runner]`, `[creator-onboarding-runner]`: correct. Both
  runners wire the full grid/selection pair through unconditionally when
  applicable (onboarding always; standalone runner conditionally on CLI
  flags), record truthful source receipts in the observed order, and
  surface any admission failure with a non-zero exit.
- `[batch-admission-tests]`: correct for what they test (F1's new tests
  included); thin on branch coverage for pre-existing validation logic
  this diff added (F2).
- `[creator-onboarding-tests]`: correct; the new admission-wiring test
  (`test_onboarding_cli_admission_passes_full_grid_and_selection`) verifies
  the exact bytes and receipt-role order passed into the writer.

## 9. Residual Risks And Off-Scope Flags

- The commission's "actual Noel staging proof" baseline item is not
  independently reproduced by this review (§7) — carried forward as
  `not proven` by this controller, not accepted on the commission's word
  alone but also not contradicted.
- F2 (test-coverage gap on ~10 correctly-implemented-but-thinly-tested
  validation branches) is reported, not patched — owner decision needed on
  whether a broader test-hardening pass is warranted.
- `_classify_cadence_failures` (split-recovery superseded-failure
  reconciliation) is depended upon by this diff's admitted-ids uniqueness
  guarantee but is pre-existing, untouched code outside the five named
  files; it was read for context, not independently re-audited end to end
  in this pass.
- No `NEEDS_ARCHITECTURE_PASS` was raised for any target; nothing in this
  diff required design-level escalation.
- This review ran entirely against synthetic/unit-test fixtures; no live
  TikTok capture was performed or is claimed, per the commission's
  lifecycle hard stop.

## 10. Non-Claims

This review is a provisional, opt-in delegated-review-and-patch convention
output per `.agents/workflow-overlay/delegated-review-patch.md`. These
findings are decision input only. This review is not approval, validation,
mandatory remediation, or executor-ready patch authority beyond what is
explicitly evidenced above until the commissioning owner separately accepts
or authorizes it. It does not constitute merge authorization or deployment
authorization. Runtime model choice is not recommended, ranked, or implied
anywhere in this review.

## 11. Courier Instruction And Adjudication Handoff

Return this full report, the applied F1 patch (diff in §6), the reported
F2 finding, and the validation evidence above to the commissioning Chief
Architect.

The commissioning Chief Architect must verify scope and provenance, then
adjudicate F1 (accept/modify/reject the applied patch) and F2 (owner
decision on test-hardening scope) as claims, not premises. F1's patch is
self-closable within the adjudicator's own authority and the commissioned
scope — it is already applied in the working tree; the adjudicator's task
is to accept, modify, or revert it, not to author it fresh. If accepted and
no unresolved material issue remains, collapse lifecycle work (commit,
push, PR) into one land step; this delegate does not commit, push, open or
update a PR, merge, stash, reset, or perform repository hygiene, per the
commission's lifecycle hard stop.

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/tiktok_full_grid_bronze_admission_delegated_adversarial_code_review_v0.md
  recommendation: accept_with_applied_patch
  reviewed_by: claude-sonnet-5
  authored_by: OpenAI / Codex
  summary: "TikTok full-grid Bronze admission diff correctly enforces its fitness contract; one internal-consistency defect (F1, video_url check stricter than its own capture-time producer) was found and patched with regression tests; one test-coverage gap (F2) is reported for owner decision."
  findings_count: 2
  blocking_findings: []
  advisory_findings:
    - F1: major, confirmed, patched with regression tests (video_url admission check loosened to match creator_onboarding._is_creator_video_url tolerance)
    - F2: minor, confirmed, reported not patched (thin negative-path test coverage on ~10 correctly-implemented validation branches)
  next_action: "Chief Architect adjudicates F1 (applied patch) and F2 (owner decision on test-hardening scope); if accepted, batch commit/push/PR into one land step per the commission's lifecycle hard stop."
```
