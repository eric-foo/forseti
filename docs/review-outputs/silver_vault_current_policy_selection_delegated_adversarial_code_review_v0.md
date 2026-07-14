# Silver Vault Current-Policy Selection — Delegated Adversarial Code Review-and-Patch Result v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial code review-and-patch result)
scope: >
  Cross-vendor controller review and bounded patch of branch
  codex/silver-current-policy-selection: exact-policy product-mention identity,
  the shared current-record selector, consumer convergence, residual visibility,
  contracts, and focused tests.
use_when:
  - Adjudicating whether the Silver current-policy-selection slice is settled.
  - Checking the exact-policy selector, consumer delegation, and fail-closed siblings.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: OpenAI/Codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: not_applicable
```

## 1. Commission, Lane, And Actor/Model-Family Receipt

- commission: `delegated_code_review_and_patch` for branch
  `codex/silver-current-policy-selection`, commissioned via
  `docs/prompts/reviews/silver_vault_current_policy_selection_delegated_adversarial_code_review_patch_prompt_v0.md`.
- review_lane: code (`workflow-code-review`); `workflow-deep-thinking` framed the
  failure modes first; the delegated-review-patch convention bounded
  receipt/role/scope/adjudication.
- author vendor: OpenAI / Codex. controller vendor: Anthropic (Claude, Opus 4.8).
  These differ, so the `cross_vendor_discovery` de-correlation bar is satisfied.
- controller identity was observed by this reviewer as the running model; the
  operator did not additionally attest it. It is not OpenAI, which is the
  binding constraint the commission names.

## 2. Receiving Preflight (fresh reads)

- launch_checkout: `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\silver-vault-policy-review-c4808b`
  (branch `claude/silver-vault-policy-review-c4808b`).
- effective_target_worktree: `C:\tmp\forseti-silver-current-policy-selection`.
- current branch of target: `codex/silver-current-policy-selection`.
- observed HEAD: `6cadf68936ef390d76ea4f7c0435fe8c115a5e73`.
- clean/dirty at start: clean (`git status --porcelain` empty before patch).
- direct-write proof: the target worktree's git dir is
  `C:/Users/vmon7/Desktop/projects/orca/.git/worktrees/silver-current-policy-selection`,
  a registered linked worktree whose checked-out branch is
  `codex/silver-current-policy-selection`; edits in the target worktree were made
  and read back (Section 6 patch), so writes land on that branch.
- no other writer: the target tree was clean at start and only this reviewer
  wrote to it (two files); confirmed by `git status --short` after the patch.
- base reachable: `git cat-file -t 702df6188f5c72efe4b6f4ea45c0751ef5c496ba` → `commit`.
- SHA-256 target check: all 18 commissioned files matched the manifest exactly
  (lowercase SHA-256, verified with `Get-FileHash`). The prompt file itself is
  review-routing infrastructure and is not a code-review target.
- diff scope base..HEAD: the 18 manifest files plus the added prompt file; no
  unexpected target.

Preflight verdict: `TARGET_STATE_OK` — no `BLOCKED_TARGET_STATE_MISMATCH`.

## 3. Source-Read Ledger And SOURCE_CONTEXT_READY

Read completely before findings (status: clean unless noted):

- `AGENTS.md` — kernel behavior; confirmed byte-identical to the review base on
  the target branch.
- `.agents/workflow-overlay/README.md`, `source-loading.md`,
  `decision-routing.md`, `review-lanes.md`, `delegated-review-patch.md`,
  `validation-gates.md` — overlay authority for lane, de-correlation, patch, and
  validation boundaries.
- Target manifest (18 files): all read via full file or full base..HEAD diff.
- Nearest imported helpers judged directly:
  `data_lake/sibling_selection.py` (the shared `select_current_record_per_subject`
  rule), plus `silver_lineage.py` / `silver_record.py` call surfaces referenced
  by the selector.
- Guard/consumer corroboration:
  `tests/contract/test_silver_reader_selection_gate.py`,
  `tests/unit/test_silver_lane_registry_guard.py`, and a repo-wide `.lane_dir(`
  scan to confirm consumer delegation.

`SOURCE_CONTEXT_READY` — declared after the reads above. `workflow-deep-thinking`
then `workflow-code-review` applied, overlay taking precedence.

## 4. Findings (ordered by correctness impact)

### F1 — Malformed stored product-mention policy aborts the whole rebuild-proof run instead of a per-view `failed_unreadable_manifest` (PATCHED)

- location: `forseti-harness/data_lake/derived_retrieval_views.py`,
  `prove_derived_retrieval_rebuildability` (policy extraction ~line 288) and
  `_generate` (`normalize_product_mention_policy`, ~line 207).
- severity: minor. confidence: high. verdict: CONFIRMED.
- evidence: the by_mention branch reads
  `stored_manifest["selection_policy_versions"]["product_mention_policy"]` inside
  a `try/except (ValueError, KeyError)` that records `failed_unreadable_manifest`
  for a missing key. But validation of that value happens later, in `_generate`
  via `normalize_product_mention_policy`, which is called **outside** the try. A
  manifest whose policy is present but malformed (e.g. `policy_fingerprint_sha256`
  not lowercase 64-hex, or not a mapping) therefore raises
  `ProductMentionPolicyError` (a `ValueError`) uncaught out of
  `prove_derived_retrieval_rebuildability`. The runner catches it generically and
  reports a whole-run error, losing the per-view accounting the proof exists to
  produce — inconsistent with the two sibling manifest-corruption forms
  (unparseable JSON, missing key) that already yield `failed_unreadable_manifest`.
- failure scenario: a tampered/corrupted by_mention `manifest.json` whose
  `product_mention_policy.policy_fingerprint_sha256` is not 64-hex →
  `prove_derived_retrieval_rebuildability(root)` raises instead of returning
  `{"results": {"by_mention": "failed_unreadable_manifest", ...}, "status": "failed"}`.
- red proof (pre-patch): the new regression test raised
  `ProductMentionPolicyError: policy_fingerprint_sha256 must be lowercase 64-hex`
  at `_generate` (line 207) via `prove_...` (line 297); pytest exit 1.
- authority basis: the proof flow's own established intent (per-view
  `failed_unreadable_manifest` for unreadable manifests) plus the commission's
  fitness item 7 ("structured runner failures remain visible") and the Patch
  Authority instruction to preserve real failure visibility.
- minimum_closure_condition: a present-but-malformed stored policy for a proved
  view is classified as that view's `failed_unreadable_manifest`, not an uncaught
  raise that discards the other views' per-view results.
- next_authorized_action: patch applied within the target file; CA adjudicates
  keep/veto.
- verification expectation: the added regression test passes and the full focused
  suite stays green (Section 7).

## 5. considered_and_defended (candidates that survived the attack)

- Prefix-collision on completion identity (adversarial q1): the record id embeds
  `__p{fingerprint[:12]}` but the `digest[:16]` is `sha256(full_fingerprint \x00
  [source_key \x00] joined_text)`, so two fingerprints sharing a 12-char prefix
  still yield distinct ids. Held.
- Policy omission / partial / mismatch (q2): `normalize_product_mention_policy`
  requires both fields, non-empty version, exact lowercase 64-hex fingerprint;
  the SoV spec normaliser raises `SovSpecError`, and the quality-eval and
  derived-retrieval runners make both CLI args required. Mismatch becomes a
  `policy_mismatch` residual, never evidence. Held.
- Residual direct lane walk (q3): all three consumers delegate to
  `select_product_mention_records`; a repo-wide `.lane_dir(` scan shows only
  `data_lake/product_mention_selection.py` walks the mentions lane, and the seam
  census pin (`test_capture_runner_lake_seam_coverage.py`) moved the lane_dir
  touchpoint to the selector and dropped the three consumer entries. Held.
- Distinct same-policy siblings tie-broken (q5): because `subject_key` embeds the
  raw anchor, same-subject records share one anchor; all candidates carry
  `derivation_rank=0`, so `_apply_anchor_rank` sees `len(winners) > 1` and raises
  `ambiguous_sibling_derivation`. That propagates as a `ValueError` caught by
  each runner's `except (DataLakeRootError, ValueError)` → structured error, exit
  nonzero. Fail-closed, never counted twice. Held. (Corollary: the
  `same_policy_bypassed` residual loop is effectively unreachable for this
  selector, because `result.bypassed` is always empty here — a latent
  dead/misleading branch, not a runtime defect; behavior matches the contract's
  fail-closed rule. Left unpatched to avoid cleanup beyond the confirmed-defect
  bar.)
- Subject-key collapse/split (q6): identity is raw anchor + subject ref
  (namespace/kind/native_id) + transcript/source provenance anchors, and
  explicitly excludes model — distinct source observations stay distinct;
  model/output metadata cannot split one observation. Held.
- Selector nondeterminism (q7): every walk and residual set is sorted by
  record_ref / raw_anchor / status; identical-content collapse keeps the
  lexically smallest ref; by_mention dedupes refs (`if ref not in refs`). Held.
- Rebuild/proof policy mismatch (q8): proof regenerates each view from the exact
  policy stored in that view's manifest and byte-compares; a divergent policy
  surfaces as `failed_drift_or_non_regenerable`. Held (with F1 hardening the
  malformed-policy edge).
- Denominators hiding lake-wide exclusions (q9): SoV coverage carries
  `selection_residual_count_lake_wide` + `selection_residuals_by_status`, and
  quality-eval carries `mention_records_total = len(source_refs)` plus
  `mention_records_by_selection_status`; residuals are disclosed lake-wide. Held.
- Tests prove production paths (q12):
  `test_rubric_version_reextracts_to_distinct_policy_identity` drives the real
  `run_extraction`, asserts `status == "extracted"`, `transport.calls == 2`, and
  two distinct `policy_version`s; SoV/rebuild tests exercise real
  `compute_sov_readout` / `rebuild_derived_retrieval`. Held. (Minor: the
  record-id collision test uses fully-disjoint fingerprints rather than a shared
  prefix; the property still holds by construction. Not a defect.)

## 6. Patch Summary And Changed-File Scope

Confirmed defects patched: 1 (F1). Changed files (both inside the 18-file named
target set):

- `forseti-harness/data_lake/derived_retrieval_views.py`
- `forseti-harness/tests/test_data_lake_rebuild_proof.py`

```diff
diff --git a/forseti-harness/data_lake/derived_retrieval_views.py b/forseti-harness/data_lake/derived_retrieval_views.py
--- a/forseti-harness/data_lake/derived_retrieval_views.py
+++ b/forseti-harness/data_lake/derived_retrieval_views.py
@@ -286,7 +286,9 @@ def prove_derived_retrieval_rebuildability(root) -> dict:
                 "generated_at": stored_manifest["generated_at"],
             }
             product_mention_policy = (
-                stored_manifest["selection_policy_versions"]["product_mention_policy"]
+                normalize_product_mention_policy(
+                    stored_manifest["selection_policy_versions"]["product_mention_policy"]
+                )
                 if view_name == "by_mention"
                 else None
             )
         except (ValueError, KeyError):
```

```diff
diff --git a/forseti-harness/tests/test_data_lake_rebuild_proof.py b/forseti-harness/tests/test_data_lake_rebuild_proof.py
--- a/forseti-harness/tests/test_data_lake_rebuild_proof.py
+++ b/forseti-harness/tests/test_data_lake_rebuild_proof.py
@@ -1,9 +1,13 @@
 from __future__ import annotations

+import json
 import shutil
 from pathlib import Path

-from data_lake.derived_retrieval_views import rebuild_derived_retrieval
+from data_lake.derived_retrieval_views import (
+    prove_derived_retrieval_rebuildability,
+    rebuild_derived_retrieval,
+)
 from data_lake.root import DataLakeRoot
 from source_capture.models import known_fact
 from source_capture.writer import write_local_source_capture_packet
@@ -58,3 +62,34 @@ def test_indexes_rebuild_byte_identical_from_authoritative_truth(tmp_path: Path)

     after = _snapshot(root.path / "indexes")
     assert after == before, "an index did not rebuild byte-identically -> it is smuggling non-rebuildable state"
+
+
+def test_prove_classifies_malformed_stored_policy_as_unreadable_manifest(tmp_path: Path) -> None:
+    # A by_mention manifest whose stored product_mention_policy is present but
+    # malformed (not lowercase 64-hex) is manifest corruption. Prove must classify
+    # it as a per-view failed_unreadable_manifest -- consistent with a missing key
+    # -- rather than raising and aborting the whole proof run.
+    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
+    _capture(root, tmp_path, "alpha")
+    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
+    ... (manifest corruption + prove assertions; full body in the working tree)
```

The `normalize_product_mention_policy` symbol is already imported at the top of
`derived_retrieval_views.py`, and `_generate` re-normalises idempotently, so the
change adds no new import and no behavior change on the valid-policy path.

Patches and this report are left uncommitted. No commit, push, PR, merge, stash,
reset, clean, or production capture was performed. No edit touched any file
outside the named target set, so no `NEEDS_ARCHITECTURE_PASS` arose.

## 7. Validation (commands, exit codes, observed results, not-run checks)

Focused suite (from `forseti-harness/`, `PYTHONDONTWRITEBYTECODE=1`,
`--basetemp` under `C:\tmp`):

```text
python -m pytest -p no:cacheprovider -q --basetemp <tmp> \
  tests/unit/test_transcript_product_lake.py tests/unit/test_sibling_selection.py \
  tests/test_data_lake_indexes_rebuild.py tests/test_data_lake_rebuild_proof.py \
  tests/test_data_lake_sov_readout.py tests/test_sov_extraction_quality_eval.py \
  tests/contract/test_silver_reader_selection_gate.py \
  tests/contract/test_capture_runner_lake_seam_coverage.py \
  tests/unit/test_silver_lane_registry_guard.py
```

- pre-patch: 105 passed, exit 0 (reproduced the reported author-side count).
- post-patch (with the added regression test): 106 passed, 15 warnings, exit 0.
- targeted red/green for F1:
  `tests/test_data_lake_rebuild_proof.py::test_prove_classifies_malformed_stored_policy_as_unreadable_manifest`
  — exit 1 (raised `ProductMentionPolicyError`) before the fix; exit 0 after.

Repo-root gates (from repo root):

```text
$py = @(git diff --name-only --diff-filter=ACMRT 702df6188f5c72efe4b6f4ea45c0751ef5c496ba -- '*.py')
python -m py_compile $py        # 15 files, exit 0
git diff --check 702df6188f5c72efe4b6f4ea45c0751ef5c496ba   # exit 0
```

- `py_compile`: exit 0 over all 15 changed Python files.
- `git diff --check`: exit 0 (no whitespace errors; the CRLF notice git prints is
  informational, not a diff-check failure).

Warnings observed: `datetime.datetime.utcnow()` DeprecationWarnings from
`source_capture/transcript/*` — pre-existing, unrelated to this change.

Not-run checks: the full harness pytest suite (only the commissioned focused set
was run); any CI-only gates; production capture (forbidden by the commission).
No skipped or blocked check was converted into success.

## 8. Reviewer Verdict, Residual Risk, Off-Scope, Not-Proven

- verdict: the slice meets the commissioned fitness contract on the exercised
  paths. Identity binds version + full fingerprint; a policy change forces a
  distinct record and completion marker (proven via the real `run_extraction`
  path); exact version + 64-hex fingerprint is required with no newest/prefix
  fallback; all three read-side consumers delegate to one selector; residuals and
  lake-wide exclusions stay visible; distinct same-policy siblings fail closed;
  contracts and focused tests state the same behavior as the runtime. One minor
  failure-visibility defect (F1) was found and patched.
- residual risk: (a) the selector is lake-wide, so an ambiguous same-policy
  subject anywhere aborts a cohort-scoped SoV/quality-eval readout as a
  structured error — this is the contract's intended fail-closed posture, but it
  couples unrelated subjects into one readout's availability; (b) a byte-identical
  same-subject duplicate is collapsed by the shared rule without an explicit
  residual (it is represented by the selected byte-identical record); (c) the
  `same_policy_bypassed` residual branch is effectively unreachable for this
  selector. None blocks the commissioned outcome; all are recorded for the
  adjudicator.
- off-scope flags: legacy-lane and live-population migration remain out of scope
  and were not touched; the change alters current product-mention identity and
  reads only.
- not-proven boundaries: only the commissioned focused suite and the two
  repo-root gates were run; no full-suite, CI, live-lake, or production-capture
  evidence is claimed. The author-side "15 files compiled / diff --check passed"
  claims were independently reproduced above; the author-side "105 tests" count
  was reproduced pre-patch.

## 9. Review-Use Boundary

These findings and the applied patch are decision input only. This review is not
approval, validation, mandatory remediation, readiness, source-of-truth
promotion, or executor-ready patch authority until the commissioning Chief
Architect (home model) separately adjudicates and accepts them. Runtime model
choice is not recommended, ranked, or implied anywhere in this review.

## 10. Courier Block

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission and target: delegated_code_review_and_patch for branch
  codex/silver-current-policy-selection (HEAD 6cadf68), base
  702df6188f5c72efe4b6f4ea45c0751ef5c496ba, the 18 named target files; prompt
  docs/prompts/reviews/silver_vault_current_policy_selection_delegated_adversarial_code_review_patch_prompt_v0.md.
- implementation context, diff, and reviewed files: exact-policy product-mention
  identity + shared current-record selector + three converged read consumers +
  two contracts + focused tests; full base..HEAD diff and the nearest selector
  helper (sibling_selection.py) were read.
- findings and implementation evidence: 1 CONFIRMED minor defect (F1 — malformed
  stored policy aborted the rebuild-proof run instead of a per-view
  failed_unreadable_manifest), with red/green proof; all other attacked seams
  survived (Section 5).
- applied patch or exact requested edits: F1 patched in
  data_lake/derived_retrieval_views.py; regression test added in
  tests/test_data_lake_rebuild_proof.py. Both inside the named target set.
  Uncommitted.
- citations: overlay authority (review-lanes, delegated-review-patch,
  validation-gates); selector semantics (sibling_selection.py); seam census
  (test_capture_runner_lake_seam_coverage.py; test_silver_reader_selection_gate.py).
- reviewer verdict: fitness contract met on exercised paths; one minor defect
  found and patched.
- validation evidence and not-run checks: focused suite 105 passed pre-patch /
  106 passed post-patch (exit 0); F1 red exit 1 -> green exit 0; py_compile exit
  0 (15 files); git diff --check exit 0. Not run: full suite, CI-only gates,
  production capture.
- residual risk: lake-wide fail-closed couples unrelated subjects into a readout;
  byte-identical duplicate collapse carries no explicit residual;
  same_policy_bypassed branch unreachable for this selector.
- blockers, off-scope flags, and not-proven boundaries: no blocker; legacy/live
  migration out of scope and untouched; only focused-suite + two root gates
  proven.
```
