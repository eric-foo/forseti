# Review-Report Mechanics Runner — Delegated Adversarial Code Review-and-Patch Report v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch report
scope: >
  Findings, patch, and verdict for a commissioned de-correlated review of the
  review-report mechanics runner, tests, and discoverability doc against the
  prompt at
  docs/prompts/reviews/review_report_mechanics_adversarial_code_review_and_patch_prompt_v0.md.
use_when:
  - Adjudicating this delegated review's findings and applied patch.
  - Checking whether the review-report mechanics runner still has a live
    false-GATE-PASS defect after this pass.
authority_boundary: retrieval_only
```

reviewed_by: claude-sonnet-5
authored_by: unrecorded

review_use_boundary: >
  These findings, the applied diff, and the verdict below are decision input
  only. They are not approval, not validation, not mandatory remediation, and
  not executor-ready patch authority. The home/CA model must accept, modify,
  or reject each material change against the citations before anything is
  kept, then follow `.agents/workflow-overlay/communication-style.md`'s
  Review Adjudication Next Step tail.

## Commission

- Prompt: `docs/prompts/reviews/review_report_mechanics_adversarial_code_review_and_patch_prompt_v0.md`
- Target kind: `delegated_code_review_and_patch`, `access: repo`.
- Named patch scope: `.github/scripts/review-report-mechanics.py` (runner),
  `forseti-harness/tests/unit/test_review_report_mechanics.py` (tests),
  `.github/scripts/README.md` (discoverability). No other path was touched.
- Actor/model-family receipt: `author_home_model_family: OpenAI GPT`,
  `controller_model_family: Anthropic Claude (claude-sonnet-5)`,
  `de_correlation_status: confirmed` (cross-vendor; different upstream model
  developer than the recorded author family).
- Observed branch: `codex/review-report-mechanics`.
- Observed HEAD before this pass: `391df71c377a88c0ff09a97f30b68fbe02cfda21`.
- Review base (handoff commit): `722bb5fc3298c9170f011e91a9c6b44389540c22`.
  `git merge-base --is-ancestor` confirmed this base is an ancestor of the
  observed HEAD.
- Dirty state before this pass: clean (`git status --porcelain=v1` empty).
  After this pass, only the three named targets are modified; no other path
  changed.

## Method

`workflow-deep-thinking` was applied first (framing failure modes across the
seven named attack axes: false GATE PASS paths; path/base-ref/ignore
classification; byte-preservation and diff determinism; checker-predicate
non-duplication; receipt scope; post-write/replace/verify-read-only
semantics; test honesty), then `workflow-code-review`'s posture was applied
to the bounded diff: every changed hunk in the three named targets was read
in full, cross-checked against the frozen decisions in
`docs/prompts/handoffs/review_report_mechanics_fused_continuation_handoff_v0.md`,
and against the two checker interfaces the runner loads
(`.agents/hooks/check_review_output_provenance.py`,
`.agents/hooks/check_review_summary.py`). Two of the findings below were not
only reasoned from source but empirically reproduced against the real runner
in a scratch git repository before being classified `CONFIRMED`, and the test
suite was run on this exact Windows machine to observe cross-platform
behavior directly rather than assume it.

## Findings

### RRM-01 — `docs/review-outputs/README.md` silently bypassed both content checkers, producing a false overall `GATE PASS` — **FIXED**

- Target: `[runner]` `.github/scripts/review-report-mechanics.py`
- Evidence (pre-patch): the `report_destination` validation in
  `prepare_inputs()` (was around the `.suffix.lower() != ".md"` check, now at
  `.github/scripts/review-report-mechanics.py:327-328`) accepted any `.md`
  path under `docs/review-outputs/`, including a literal `README.md`
  basename. But both downstream checkers exclude that exact basename from
  their scan scope: `check_review_output_provenance.py:174-177`
  (`is_review_output_scope`: `Path(relposix).name != "README.md"`) and
  `check_review_summary.py:124-133` (`is_in_scope`: same exclusion). Since
  `run_checkers()` (`.github/scripts/review-report-mechanics.py:260-306`)
  hands the report's own relpath straight into `collect_findings` /
  `scan_files` with no basename guard of its own, a report named
  `docs/review-outputs/README.md` produced zero findings from either checker
  by construction, not because its content was clean.
- Failure mechanism and consequence: an author (human or agent) naming a
  delegated review report `README.md` — a highly plausible default, not an
  adversarial edge case — got a receipt claiming
  `"provenance_shape": "GATE PASS"` and `"summary_shape": "GATE PASS"` with
  `"status": "GATE PASS"` overall, even when the report had no retrieval
  header, no `reviewed_by`/`authored_by`, and no review-use-boundary prose.
  This is exactly the "false GATE PASS path for ... checker ... failures"
  attack axis named in the commission, and directly violates
  `AGENTS.md`'s "never create fake success paths."
- Reproduction: verified empirically in a scratch git repository. Assembling
  a draft missing the retrieval header, `reviewed_by`, `authored_by`, and
  `review_use_boundary` under `docs/review-outputs/README.md` returned
  `status: GATE PASS` with `provenance_shape`/`summary_shape` both
  `GATE PASS`; the identical draft assembled under
  `docs/review-outputs/normal_report.md` correctly returned
  `status: GATE FAIL` with `provenance_shape: GATE FAIL`.
- Severity: critical. Confidence: high (read from source, then reproduced
  against the real runner).
- `minimum_closure_condition`: the runner must reject a report path whose
  basename is excluded from the checkers' own scope, so the set of paths the
  runner will write always overlaps the set of paths the checkers will scan.
- `next_authorized_action`: patch was in-scope and safely local; applied
  directly (see Patch below). No further action needed from this finding
  alone; CA adjudication of the applied patch is still required per the
  review-use boundary.
- Outcome: **fixed**. `prepare_inputs()` now raises
  `MechanicsFailure("report_destination", 2, ...)` when `report.name ==
  "README.md"` (`.github/scripts/review-report-mechanics.py:329-335`),
  before any git/diff/write work happens. Proven by
  `test_report_named_readme_is_rejected`
  (`forseti-harness/tests/unit/test_review_report_mechanics.py`), and by
  re-running the same reproduction above post-patch (now `status: GATE FAIL`,
  single `report_destination` gate, report not written).

### RRM-02 — `verify` mode unconditionally recorded `readback_exact: GATE PASS` for a comparison it never ran — **FIXED**

- Target: `[runner]` `.github/scripts/review-report-mechanics.py`
- Evidence (pre-patch): in `execute()`, `expected_report` stays `None` for
  `verify` mode (only `assemble` mode sets it). The gate-recording line ran
  unconditionally after the `if expected_report is not None and not
  verify_assembled_bytes(...)` guard: `if expected_report is not None and
  not verify_assembled_bytes(report_bytes, expected_report): raise ...` /
  `receipt.record("readback_exact", "GATE PASS", 0)` — the `record(...)`
  call was outside the `if`, so it fired even when the comparison inside the
  `if` was never evaluated.
- Failure mechanism and consequence: every `verify` run's receipt claimed a
  `readback_exact: GATE PASS` gate that corresponds to no actual check —
  the byte-for-byte comparison (`verify_assembled_bytes`) that gate name
  describes only exists for `assemble` mode. This is a receipt-shape
  violation of Frozen Decision #9 ("The receipt contains observed paths,
  hashes, exit codes, and gate buckets only") and, more directly, another
  instance of the "false GATE PASS path for ... readback" attack axis: a
  reader of the receipt cannot tell this gate name is meaningless in verify
  mode.
- Reproduction: verified empirically — a `verify` run's receipt gate list
  included `{"name": "readback_exact", "bucket": "GATE PASS", "exit_code":
  0}` even though no `expected_report` bytes existed to compare against for
  that invocation.
- Severity: major. Confidence: high.
- `minimum_closure_condition`: `verify` mode's receipt must not claim a
  `GATE PASS` bucket for a comparison that did not execute; an
  applicable/not-applicable distinction, matching the existing
  `tracked_diff_check_not_applicable` pattern already used in the same
  function, is sufficient.
- `next_authorized_action`: patch was in-scope and safely local; applied
  directly. CA adjudication of the applied patch is still required.
- Outcome: **fixed**. The gate is now recorded as
  `readback_exact_not_applicable` / `INFO` when `expected_report is None`
  (`.github/scripts/review-report-mechanics.py:395-402`), mirroring the
  existing not-applicable pattern already in the file. Proven by a new
  assertion appended to `test_verify_is_read_only_and_rechecks_exact_diff`
  in `forseti-harness/tests/unit/test_review_report_mechanics.py`, which
  asserts `readback_exact_not_applicable` is present and `readback_exact` is
  absent from the verify-mode receipt's gate names.

### RRM-03 — receipt's checker hash set omits a transitively-loaded checker dependency — not patched

- Target: `[runner]` `.github/scripts/review-report-mechanics.py`
- Evidence: `run_checkers()`
  (`.github/scripts/review-report-mechanics.py:260-274`) hashes only the two
  directly-loaded checkers (`check_review_output_provenance.py`,
  `check_review_summary.py`) into `receipt.hashes["checkers"]`. But
  `check_review_output_provenance.py`'s own `_load_retrieval_header_checker()`
  (`.agents/hooks/check_review_output_provenance.py:162-171`) dynamically
  loads a third file, `check_retrieval_header.py`, and that file's
  `header_problems_for_lines()` directly determines part of the
  `provenance_shape` gate's outcome. The receipt's hash list is therefore
  incomplete for a gate it claims to have observed.
- Failure mechanism: a receipt reader cannot use the recorded `checkers`
  hashes to fully reconstruct what code actually ran for `provenance_shape`;
  a change to `check_retrieval_header.py` alone would silently change gate
  behavior with no corresponding hash change in the receipt.
- Severity: minor. Confidence: medium (real gap, but the receipt's stated
  scope — "paths, hashes, exit codes, and gate buckets" — does not
  explicitly promise transitive-closure hashing, so this is a completeness
  gap rather than a contract violation).
- `minimum_closure_condition`: either the receipt records the hash of every
  module actually loaded and executed to produce a gate's verdict (which
  would require the runner or the provenance checker to expose its own
  transitive dependency list), or the runner's docstring/README explicitly
  scopes the `checkers` hash entry to "directly invoked checker entry points
  only" so the receipt's own claim matches its actual coverage.
- `next_authorized_action`: owner decision — this borders a design change
  (discovering transitive dependencies mechanically, or narrowing a claim)
  rather than a same-file bug fix; left to CA/owner rather than patched
  here, per "a necessary off-scope or design-level change is a finding, not
  permission to widen the patch."

### RRM-04 — two file-read/existence paths fall through to the generic `internal_error` bucket instead of a named gate — not patched

- Target: `[runner]` `.github/scripts/review-report-mechanics.py`
- Evidence: (a) `review_root = (root / REVIEW_OUTPUT_ROOT).resolve(strict=True)`
  (`.github/scripts/review-report-mechanics.py:322`) raises a bare
  `FileNotFoundError` if `docs/review-outputs/` does not exist in the target
  worktree, rather than a `MechanicsFailure("report_destination", ...)`; (b)
  `draft_bytes = draft.read_bytes()` (`.github/scripts/review-report-mechanics.py:376`)
  is not wrapped in the same `try/except OSError -> MechanicsFailure`
  pattern used for the later report readback
  (`.github/scripts/review-report-mechanics.py:390-393`), so a permission
  error or a race-condition removal between the earlier `must_exist=True`
  resolve and this read surfaces as the generic top-level
  `except Exception` handler in `main()` instead.
- Failure mechanism and consequence: in both cases the run still ends
  `GATE FAIL` (the top-level catch-all in `main()` guarantees this) — this
  is not a false-pass risk. The gap is diagnostic precision only: the
  receipt's `internal_error` gate name gives an operator less signal than a
  named gate (`report_destination`, or a `draft_read` gate) would.
- Severity: minor. Confidence: low-medium (real but narrow: requires a
  missing `docs/review-outputs/` directory or a mid-run file-removal race,
  neither exercised by the current fixtures, which always pre-create that
  directory).
- `minimum_closure_condition`: wrap both paths in the same
  `MechanicsFailure`-mapped pattern already used for report readback, for
  gate-name symmetry.
- `next_authorized_action`: optional hardening, not required; left to CA to
  schedule or decline, per the review-lane rule that optional hardening is
  never a blocker.

### RRM-05 — checker-failure test coverage proved import-time failure only, not call-time interface drift — **FIXED (test proof added)**

- Target: `[tests]` `forseti-harness/tests/unit/test_review_report_mechanics.py`
- Evidence: `test_checker_failure_is_nonzero_and_written_report_remains_visible`
  replaces a checker file's entire body with a module-level `raise`, which
  fires during `importlib`'s `exec_module()` inside `load_checker()`
  (`.github/scripts/review-report-mechanics.py:246-257`), i.e. before any
  checker function is ever called. `run_checkers()`
  (`.github/scripts/review-report-mechanics.py:276-281`,
  `:288-292`) also wraps the actual *call* to `collect_findings` /
  `report` / `scan_files` in `try/except Exception`, which would equally
  catch an `AttributeError` from a checker that imports cleanly but has had
  a function renamed or removed — a distinct interface-drift shape the
  existing test never exercised.
- Failure mechanism: this was a test-honesty gap relative to the commission's
  named attack axis ("reject mocked success that cannot catch ... checker
  interface drift"), not a runtime defect — the code path was already
  correct, but the frozen-behavior proof required by the handoff's STEP-03
  ("Tests must prove ... checker failure propagation") only covered one of
  two plausible drift shapes.
- Severity: minor. Confidence: medium.
- `minimum_closure_condition`: a test where a checker module imports
  successfully but is missing an expected callable, asserting the same
  fail-visible `GATE FAIL` / report-remains-visible behavior.
- `next_authorized_action`: patch was in-scope (test proof for frozen
  behavior) and safely local; applied directly.
- Outcome: **fixed**. Added
  `test_checker_missing_expected_callable_is_nonzero`, which overwrites
  `check_review_summary.py` with a module that imports cleanly but defines
  no `scan_files`, and asserts `GATE FAIL` plus the written report remaining
  on disk.

## considered_and_defended

- **CRLF / `core.autocrlf` cross-machine diff-byte determinism.** The
  runner's tracked-file diff (`generate_diff`,
  `.github/scripts/review-report-mechanics.py:152-197`) does not pin
  `-c core.autocrlf=false` or any other line-ending normalization when
  invoking `git diff`. In principle, the same logical change could produce
  different diff bytes on machines with different ambient `core.autocrlf`
  defaults (Windows Git installs commonly default `true`; Linux CI commonly
  defaults `false`/`input`). This looked like a live determinism gap.
  Defense: the implementation handoff
  (`docs/prompts/handoffs/review_report_mechanics_fused_continuation_handoff_v0.md`,
  "Superseded / Dangerous-To-Reuse Context") explicitly records that pinning
  `-c core.autocrlf=false` was tried and rejected — it expanded the patch
  into whole-file diffs on a CRLF worktree, which is a worse failure mode
  than the determinism gap. I ran the full test suite on this Windows
  machine (`python -m pytest ... test_review_report_mechanics.py`, 15/15
  passed) and confirmed the tracked/untracked/`--check` code paths behave
  correctly here, including the `/dev/null`-based untracked diff
  (`.github/scripts/review-report-mechanics.py:175-191`), which is a
  cross-platform risk in its own right and passed. The residual
  cross-machine byte-determinism risk is real but already a known,
  deliberately-accepted tradeoff rather than an unconsidered defect; it is
  carried forward as residual risk below rather than reopened as a fresh
  finding.
- **`/dev/null` as a literal untracked-diff sentinel on Windows.** Initially
  flagged as a plausible cross-platform failure point (`generate_diff`,
  `.github/scripts/review-report-mechanics.py:175-191`, `git diff --no-index
  ... -- /dev/null relative`). Defense: empirically confirmed working on
  this Windows machine — `test_assemble_includes_explicit_tracked_and_untracked_paths`
  passed, and Git for Windows special-cases the literal `/dev/null` sentinel
  in its diff machinery independent of the host filesystem. Not reopened as
  a finding.

## Overall Verdict

The runner substantively delivers its frozen contract (deterministic
assemble/verify, byte-preserving token replacement, path containment,
tracked/untracked classification, empty-diff rejection, replace-guard,
checker delegation without predicate duplication, and no review-domain
output in the receipt — all confirmed by direct code reading and by the
pre-existing + new test suite passing 15/15 on this machine). Against the
commission's explicit "false GATE PASS" attack axis, two real, empirically
reproduced false-pass defects were found (RRM-01 critical, RRM-02 major) and
both are now patched with test proof. Three additional minor findings
(RRM-03, RRM-04) are real but bounded diagnostic-quality gaps, not
false-pass risks, and are left for CA/owner disposition rather than patched
here since closing them cleanly borders a design decision. This is decision
input for CA adjudication, not a readiness or approval claim.

## Validation Evidence

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp C:\tmp\pytest-review-report-controller forseti-harness\tests\unit\test_review_report_mechanics.py -q
```

- Pre-patch baseline run: 13/13 passed.
- Post-patch run (15 tests: 13 original + 2 new `test_*` functions, plus one
  new assertion block appended to an existing test): 15/15 passed, observed
  directly on this Windows machine (`win32`).
- `git diff --check` against the three modified files: exit code `0` (only
  advisory `core.autocrlf` line-ending warnings, no whitespace-error
  findings).
- Both RRM-01 and RRM-02 were independently reproduced pre-patch (false
  `GATE PASS`) and re-verified post-patch (`GATE FAIL` for RRM-01's
  reproduction; `readback_exact_not_applicable` present and `readback_exact`
  absent for RRM-02's reproduction) via a standalone scratch-repo script run
  against the real runner, not mocked.
- Dirty-state check after this pass: `git status --porcelain=v1` in the
  target worktree shows exactly the three named targets modified
  (`.github/scripts/README.md`, `.github/scripts/review-report-mechanics.py`,
  `forseti-harness/tests/unit/test_review_report_mechanics.py`) plus this
  report once written; no other path changed.

## Residual Risk

- Cross-machine diff-byte determinism under differing ambient
  `core.autocrlf`/`.gitattributes` normalization is a known, accepted
  tradeoff (see `considered_and_defended`), not eliminated by this pass.
- RRM-03 and RRM-04 remain open as minor diagnostic-quality gaps; neither is
  a false-pass risk, but neither was closed in this commission.
- This pass covers the three named targets only, at the stated commission
  scope (`delegated_code_review_and_patch`, code-review method). It is not a
  claim that every other Forseti surface interacting with these files (CI
  wiring, other consumers of the runner) was reviewed.

## Patch

The following unified diff (zero-context, generated by
`.github/scripts/review-report-mechanics.py` itself against base
`391df71c377a88c0ff09a97f30b68fbe02cfda21`) is left uncommitted in the
working tree for CA adjudication:

```diff
diff --git a/.github/scripts/review-report-mechanics.py b/.github/scripts/review-report-mechanics.py
index 77d8570c..c14065b1 100644
--- a/.github/scripts/review-report-mechanics.py
+++ b/.github/scripts/review-report-mechanics.py
@@ -328,0 +329,7 @@ def prepare_inputs(args: argparse.Namespace, receipt: Receipt) -> tuple[
+    if report.name == "README.md":
+        raise MechanicsFailure(
+            "report_destination",
+            2,
+            "report must not be named README.md; that basename is excluded from "
+            "provenance/summary checker scope and would silently bypass both gates",
+        )
@@ -388,3 +395,8 @@ def execute(args: argparse.Namespace, receipt: Receipt) -> int:
-    if expected_report is not None and not verify_assembled_bytes(report_bytes, expected_report):
-        raise MechanicsFailure("readback_exact", 1, "report readback does not match assembled bytes")
-    receipt.record("readback_exact", "GATE PASS", 0)
+    if expected_report is not None:
+        if not verify_assembled_bytes(report_bytes, expected_report):
+            raise MechanicsFailure("readback_exact", 1, "report readback does not match assembled bytes")
+        receipt.record("readback_exact", "GATE PASS", 0)
+    else:
+        # verify mode has no just-written expected bytes to compare against;
+        # recording GATE PASS here would claim a comparison that never ran.
+        receipt.record("readback_exact_not_applicable", "INFO", 0)
diff --git a/forseti-harness/tests/unit/test_review_report_mechanics.py b/forseti-harness/tests/unit/test_review_report_mechanics.py
index 8c46ef85..51265725 100644
--- a/forseti-harness/tests/unit/test_review_report_mechanics.py
+++ b/forseti-harness/tests/unit/test_review_report_mechanics.py
@@ -276,0 +277,37 @@ def test_checker_failure_is_nonzero_and_written_report_remains_visible(tmp_path:
+def test_checker_missing_expected_callable_is_nonzero(tmp_path: Path) -> None:
+    """Checker interface drift at call-time (module imports fine but lacks the
+    expected callable), distinct from the import-time failure covered above."""
+    root = _init_repo(tmp_path)
+    (root / ".agents" / "hooks" / "check_review_summary.py").write_text(
+        "# drifted checker interface: no scan_files() left to call\n", encoding="utf-8"
+    )
+    result = _assemble(root)
+
+    assert result.returncode != 0
+    assert _receipt(result)["status"] == "GATE FAIL"
+    assert (root / "docs" / "review-outputs" / "report.md").exists()
+
+
+def test_report_named_readme_is_rejected(tmp_path: Path) -> None:
+    """docs/review-outputs/README.md is excluded from both downstream checkers'
+    scope (check_review_output_provenance.py / check_review_summary.py), so
+    accepting that basename would let a report bypass provenance/summary
+    scanning while still reporting GATE PASS."""
+    root = _init_repo(tmp_path)
+    _write_draft(root)
+    result = _run(
+        root,
+        "assemble",
+        "--draft",
+        "drafts/report.md",
+        "--report",
+        "docs/review-outputs/README.md",
+        "--patch",
+        "src/example.txt",
+    )
+
+    assert result.returncode != 0
+    assert _receipt(result)["status"] == "GATE FAIL"
+    assert not (root / "docs" / "review-outputs" / "README.md").exists()
+
+
@@ -331,0 +369,8 @@ def test_verify_is_read_only_and_rechecks_exact_diff(tmp_path: Path) -> None:
+
+    gate_names = {gate["name"] for gate in _receipt(verified)["gates"]}
+    assert "readback_exact_not_applicable" in gate_names
+    assert "readback_exact" not in gate_names, (
+        "verify mode never runs the assembled-bytes comparison readback_exact "
+        "checks; recording that gate name as GATE PASS would claim a "
+        "comparison that never happened"
+    )
diff --git a/.github/scripts/README.md b/.github/scripts/README.md
index e540d636..771eeef2 100644
--- a/.github/scripts/README.md
+++ b/.github/scripts/README.md
@@ -28 +28,4 @@ provenance and summary-shape checkers. Failures remain nonzero and visible; an
-existing report is replaced only when `assemble --replace` is explicit.
+existing report is replaced only when `assemble --replace` is explicit. The
+report path may not be named `README.md`: that basename is excluded from both
+downstream checkers' scope, so the runner rejects it rather than silently
+skipping provenance/summary verification.

```
