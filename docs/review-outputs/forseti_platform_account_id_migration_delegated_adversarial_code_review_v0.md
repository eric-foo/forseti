# Delegated Adversarial Code Review — Forseti Platform Account ID Migration (PR #795)

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated code review-and-patch return, repo access mode)
scope: >
  Delegated adversarial code review + bounded patch return for PR #795 (Silver
  creator-metric account subject-ref migration from orca_platform_account_id to
  forseti_platform_account_id, plus live-lake default-root corrections),
  commissioned via
  docs/prompts/reviews/forseti_platform_account_id_migration_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md.
use_when:
  - Adjudicating this delegated review's findings, diff, verdict, and residuals.
  - Checking what was found, what was patched, and what validation ran for PR #795.
stale_if:
  - PR #795 is merged, closed, rebased, or amended past the commit reviewed below.
  - This return has already been adjudicated by the commissioning lane.
branch_or_commit: codex/forseti-platform-account-id-migration
authority_boundary: retrieval_only
```

## Commission

Commissioned by:
`docs/prompts/reviews/forseti_platform_account_id_migration_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md`,
under the `delegated_code_review_and_patch` sibling mode of
`.agents/workflow-overlay/delegated-review-patch.md`. Repo access mode.

## WHO-CONSTRAINT gate

```yaml
reviewed_by: claude-sonnet-5
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery
```

- Reviewed PR authored by: `OpenAI/Codex GPT-5`.
- Reviewer (this pass): Claude (Anthropic) — Sonnet 5, model id `claude-sonnet-5`.
- Vendor differs from the author vendor (Anthropic vs OpenAI) → cross-vendor
  discovery bar is satisfied. Not blocked.

## Target and commit state

- Repository: `https://github.com/eric-foo/forseti`
- PR: #795, branch `codex/forseti-platform-account-id-migration`
- Pinned commission commit: `a0f08e1badacbfa35bef31aac6f45082459a078d`
- **Delta from pinned commit:** the branch had advanced one commit past the pin,
  to `f8017bc51a659bf1f6f8cf0d617c7228f43d9b9c` — `docs: add delegated review
  prompt for account id migration`, i.e. the commission prompt artifact itself.
  It touches no file in `forseti-harness/` and is unrelated to the migration.
  **Reviewed content is the pinned commit `a0f08e1b`** (diffed against
  `origin/main` at `f135dcb6`, matching the commission's recorded base); the
  working tree used for review and patching was the branch tip, whose only
  delta from the pin is that unrelated docs commit.
- `git diff --stat origin/main...a0f08e1b`: 19 files changed, 208
  insertions(+), 26 deletions(-) — matches the Named Target Set exactly (no
  file outside the commissioned 19 is touched).

## Source-Gated Method Contract

- `REFERENCE-LOAD`: `workflow-deep-thinking`, `workflow-code-review` (method
  guidance only, not applied to any conclusion before source readiness).
- `SOURCE-LOAD`: full `git diff origin/main...a0f08e1b`; all 19 Named Target
  Set files read in full; `silver_envelope_core.required_subject_native_id`;
  adjacent non-target-set consumers (`silver_metric_snapshot.py`,
  `live_lake_freshness_gate.py`, `materialize.py`) grepped for direct legacy-key
  access; the historical contract doc
  `creator_profile_current_lake_cutover_architecture_v0.md`; repo-wide grep for
  any remaining `orca_platform_account_id` / `ROOT / "orca"` reference.
- `SOURCE_CONTEXT_READY`: declared. No missing sources or excluded material.
- `APPLY`: `workflow-deep-thinking` used to frame the failure-mode axes below
  before finding review; `workflow-code-review` applied in findings-first,
  coverage-first posture per `.agents/workflow-overlay/review-lanes.md`.

## Deep-thinking frame (failure modes attacked)

1. New-write correctness: does every write site emit `forseti_platform_account_id`
   and never re-emit the legacy key?
2. Legacy-read correctness: do all read/discovery/revalidation sites resolve a
   legacy-only record to the same account?
3. Mixed-row / disagreement handling: what happens when both keys are present,
   or neither is?
4. Failure-visibility regression: does the migration's `raise`-based helper
   change any *caller's* documented crash-vs-report contract?
5. Runner default-root correctness and CLI-override preservation.
6. Test-coverage symmetry across the three platform producers.
7. Scope discipline: does the diff match the Named Target Set exactly?

## Findings

### F1 — CRITICAL — Malformed rollup record crashes the whole lake-wide revalidation walk instead of being recorded as a per-record failure

- **File:** `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py:126-131` (pre-patch)
- **Confidence:** high
- **Severity:** critical
- **Evidence:** `revalidate_creator_metric_rollups` builds each
  `RollupRevalidationFinding` with
  `account_id=str(_platform_account_id_from_subject_ref(...))`, uncaught. The
  module's own docstring states: *"raising is reserved for an unreadable lake,
  not a failed check (failures stay visible per record so one bad record
  cannot hide the rest)."* `platform_account_id_from_subject_ref` (new in this
  PR) raises `KeyError` when a record's subject ref carries neither
  `forseti_platform_account_id` nor legacy `orca_platform_account_id` — a
  reachable state for any pre-existing or corrupted lake record. Before this
  migration, the equivalent line used
  `.get("orca_platform_account_id", "")` (never raised). Reproduced directly:
  a single rollup record with an empty `subject.ref` mapping placed in a test
  lake made `revalidate_creator_metric_rollups` raise `KeyError` and abort
  before returning a `RollupRevalidationReport`, discarding every other
  finding computed in the same pass.
- **Failure scenario:** any real or synthetic lake containing one rollup
  record whose subject ref lost/never carried an account-id key (a plausible
  corruption/incomplete-write case — exactly the class of defect this module
  exists to surface) causes the *entire* revalidation pass to raise instead of
  reporting a per-record failure, silently discarding all other findings from
  that run.
- **Impact:** defeats the purpose of a lake-wide, all-records validation gate;
  one bad record can now hide every other real defect in the same run,
  directly contradicting the module's stated invariant.
- **minimum_closure_condition:** a subject ref that cannot resolve to an
  account id is recorded as a per-record failure in
  `RollupRevalidationFinding.failures`, and the walk continues to completion
  and reports on every other record in the lake.
- **next_authorized_action:** **PATCHED** (see Patch below). CA adjudicates;
  if kept, a regression test in `tests/unit/test_rollup_formula_revalidation.py`
  is recommended but that file is **not** in the Named Target Set and was
  **not** touched — a separate commission/authorization is needed to add it.

### F2 — MINOR — No disagreement handling when both account-id keys are present with different values

- **File:** `forseti-harness/capture_spine/creator_profile_current/silver_subject_ref.py:24-38`
- **Confidence:** medium
- **Severity:** minor
- **Evidence:** `platform_account_id_from_subject_ref` checks
  `FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY` first and only falls back to the
  legacy key when the forseti key is absent (`None`); if both keys are present
  and disagree, the forseti value wins silently with no flag or error.
- **Failure scenario:** a future migration tool, manual repair, or partial
  rewrite that leaves both keys present with different values would be read
  as the forseti value with no visible signal that the record is internally
  inconsistent. Not reachable today: every write site in the Named Target Set
  writes the forseti key only (verified — see Considered and Defended #2), so
  this requires out-of-band record mutation.
- **minimum_closure_condition:** either an explicit accepted-residual note (no
  code change needed), or a disagreement check that raises/flags when both
  keys are present and differ.
- **next_authorized_action:** owner decision (accept as named residual, or
  authorize a follow-up hardening patch). Not patched in this pass — no
  reachable production trigger today, and adding it would exceed the
  smallest-complete-intervention bound for a confirmed defect.

### F3 — MINOR — Instagram producer lacks an explicit "no legacy key" test assertion that TikTok/YouTube producers have

- **Files:** `forseti-harness/tests/unit/test_creator_metric_silver_reader.py`,
  `test_creator_metric_silver_discovery.py`, `test_creator_metric_silver_snapshot.py`
  (all in the Named Target Set)
- **Confidence:** high
- **Severity:** minor (test-coverage asymmetry only; the IG write sites
  themselves were read directly and are correct — see Considered and Defended #2)
- **Evidence:** `test_tiktok_creator_metric_silver_producer.py` and
  `test_youtube_creator_metric_silver_producer.py` both added
  `assert LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY not in ref` (and `rollup_ref`)
  after the migration. No equivalent assertion exists anywhere in the IG-facing
  test files, which only round-trip through the fallback-permissive reader
  helper — a test that would still pass even if the IG producer accidentally
  re-emitted the legacy key.
- **minimum_closure_condition:** an assertion equivalent to the TikTok/YouTube
  ones exists for IG-produced observation/rollup subject refs.
- **next_authorized_action:** optional hardening, not applied in this pass
  (labeled non-required per `.agents/workflow-overlay/review-lanes.md`
  "Optional hardening" rule; adding new test assertions beyond the confirmed
  F1 defect was judged outside this patch's smallest-complete-intervention
  bound). Owner may authorize as a follow-up.

### F4 — MINOR — Historical architecture doc still references the legacy field name (out of Named Target Set, flag-only)

- **File:** `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md:241`
- **Confidence:** high
- **Severity:** minor
- **Evidence:** the doc still reads `map each rollup to its account via
  subject.ref.orca_platform_account_id`. The equivalent docstring inside
  `silver_metric_reader.py` (in the Named Target Set) *was* updated by this PR
  to `subject.ref.forseti_platform_account_id`, so the two now disagree.
- **minimum_closure_condition:** doc updated to the current field name, or an
  explicit note marking it a historical snapshot.
- **next_authorized_action:** owner decision / separate doc-update commission
  — this file is outside the Named Target Set and was not patched.

### F5 — Validation-evidence discrepancy (not a code defect)

- **Confidence:** high (directly observed, reproducible)
- **Evidence:** the commission recorded prior evidence that the exact named
  pytest command (7 files) *"previously reported 90 passed and 2 skipped."*
  Running that exact command against the pinned/reviewed commit produced **69
  passed, 2 skipped** (71 collected). Widening to include the two
  revalidation-focused test files that exist in the repo but are **not** in
  the Named Target Set (`test_rollup_formula_revalidation.py`,
  `test_tiktok_batch_metric_rollup_producer_runner.py`) produced **88 passed,
  2 skipped** (90 total) — closer to, but still not exactly matching, the
  claimed figure.
- **next_authorized_action:** CA should reconcile with the author lane which
  exact command/file set produced "90 passed, 2 skipped" before treating that
  specific evidence line as confirmed. This does not block acceptance: every
  test in the actual Named Target Set passes, both before and after the F1
  patch (see Validation below).

## Considered and Defended

1. **Reader/discovery sites (`_seed_rollup_from_silver_record`,
   `_rollup_record_account` in `silver_metric_reader.py`) also raise
   `KeyError`/`TypeError` on a malformed subject ref, uncaught, same as the
   pre-patch revalidator.** Defended: unlike the revalidator, neither module's
   docstring promises per-record resilience; both are documented as fail-closed
   discovery/read paths, and a raise here does not silently discard a
   partially-built batch report the way it did in `revalidate_creator_metric_rollups`
   — there is no report object whose other entries get lost. Crashing loudly on
   unreadable lake data matches `AGENTS.md`'s "no fake success path" rule for
   these two modules; only the revalidator's own explicit contrary contract
   made this reachable as a defect.
2. **Could a write site in the Named Target Set ever re-emit the legacy
   `orca_platform_account_id` key, making F2 reachable in production?**
   Defended: read all six subject-builder functions
   (`_observation_subject`/`_rollup_subject` × IG/TikTok/YouTube) directly;
   every one calls `platform_account_ref_field`, which only ever sets
   `FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY`. A repo-wide grep for
   `orca_platform_account_id` in `forseti-harness/` returns exactly one hit —
   the retained legacy-key-name constant itself.
3. **Could the `ROOT / "forseti" / ...` default-path corrections silently
   break an operator's existing `--data-root` workflow?** Defended: `ROOT` only
   feeds `DEFAULT_ACCOUNT_LEDGER` / `_SOCIAL_MEDIA` fallback constants; every
   runner's `--data-root` and `--account-ledger` CLI flags remain fully
   overridable, and all touched runners' testable cores run against
   `DataLakeRoot.for_test`, independent of `ROOT`.
4. **Did the migration miss any other `orca_platform_account_id` or
   `ROOT / "orca"` occurrence in scope?** Defended: repo-wide grep across
   `forseti-harness/` found zero remaining production references to either
   pattern outside the retained legacy-compat constant name.
5. **Explicit-null `forseti_platform_account_id` key silently falls through to
   the legacy key.** Defended: `platform_account_ref_field` (the only writer)
   always routes through `required_subject_native_id`, which rejects
   non-str/empty values at write time — no writer in the Named Target Set can
   ever produce a null/empty forseti key. Only external record corruption could
   trigger this, and that class of corruption is already caught by the
   revalidator's independent content-hash check.

## Validation

Run from the repo root at the reviewed commit (working tree = branch tip,
whose only delta from the pin is the unrelated docs commit noted above):

```text
python -m py_compile <all 12 named production/runner files>   -> exit 0, no output
git diff --check origin/main...a0f08e1b                        -> exit 0, clean
python .agents/hooks/check_silver_lane_registry.py             -> exit 0, "OK (no silver-lane write violations)"
python .agents/hooks/header_index.py --strict                  -> exit 0, OK
python .agents/hooks/check_repo_map_freshness.py --strict       -> exit 0
python .agents/hooks/check_review_routing.py --strict           -> exit 0, OK
python -m pytest -q -p no:cacheprovider <named 7 test files>   -> 69 passed, 2 skipped (see F5)
```

Post-patch re-validation (after applying the F1 fix to
`rollup_formula_revalidation.py`):

```text
python -m py_compile rollup_formula_revalidation.py                                -> exit 0
python -m pytest <named 7 files> + test_rollup_formula_revalidation.py
  + test_tiktok_batch_metric_rollup_producer_runner.py                              -> 88 passed, 2 skipped, 0 failed
git diff --check                                                                    -> exit 0, clean
git status --porcelain                                                              -> only rollup_formula_revalidation.py modified
```

`registration_integrity.py --selftest` was not run per the commission's
explicit exclusion.

## Patch

One bounded patch inside the Named Target Set, applied to the working tree and
**left uncommitted** (patch-only authority; no commit/push/PR):

```diff
diff --git a/forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py b/forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py
index 316faab4..57f5cd1f 100644
--- a/forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py
+++ b/forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py
@@ -119,16 +119,22 @@ def revalidate_creator_metric_rollups(
         if platform is not None and observation.get("platform_scope") != platform:
             continue
         failures = _revalidate_one_rollup(rollup, observations_by_record_id)
+        try:
+            account_id = _platform_account_id_from_subject_ref(
+                observation.get("subject", {}).get("ref", {}),
+                what="rollup subject ref",
+            )
+        except (KeyError, TypeError, ValueError) as exc:
+            # A malformed/missing subject ref is a per-record FAILURE, not a
+            # walk-ending crash: raising here is reserved for an unreadable
+            # lake, not a failed check (module docstring above).
+            account_id = ""
+            failures = [*failures, f"rollup subject ref account id unresolved: {exc}"]
         findings.append(
             RollupRevalidationFinding(
                 record_id=str(rollup.get("record_id")),
                 raw_anchor=str(rollup.get("raw_anchor")),
-                account_id=str(
-                    _platform_account_id_from_subject_ref(
-                        observation.get("subject", {}).get("ref", {}),
-                        what="rollup subject ref",
-                    )
-                ),
+                account_id=account_id,
                 recipe_version=str(observation.get("calculation_recipe_version")),
                 failures=tuple(failures),
             )
```

Resolves F1 only. Closes F1's `minimum_closure_condition` exactly: the
malformed-ref case now becomes a per-record `failures` entry with
`account_id=""` instead of an escaping exception, and the walk completes and
reports on every other record (confirmed by the pre/post repro above and by
the full targeted + revalidation test suite passing with 0 failures
post-patch). F2, F3, F4, F5 are left unpatched per their own
`next_authorized_action` (no reachable production trigger, out-of-scope file,
or process/evidence item, respectively).

## Non-findings, not-proven boundaries, residual risks

- **Not proven / out of scope:** whether the historical architecture doc (F4)
  or any other non-Named-Target-Set document still references the legacy key
  name elsewhere in the repo — only the one file explicitly listed in the
  commission's read-only context was checked.
- **Residual risk (named, not hidden):** F2's silent-preference behavior means
  a future tool that writes both keys with different values would fail
  silently rather than loudly; acceptable today only because no in-scope
  writer can produce that state.
- **Residual risk:** `registration_integrity.py --selftest` was excluded per
  commission instruction and was not independently verified by this review.
- **Not proven:** real-lake behavior (all testing used `DataLakeRoot.for_test`
  temp lakes, per the module boundaries documented in each file — none of the
  reviewed modules write to a production lake themselves).

## Review-use boundary

This review's findings are decision input only. They are not approval, not
validation, not mandatory remediation, and not executor-ready patch authority
until separately accepted or authorized by the commissioning Chief Architect.
The patch above is a bounded, uncommitted working-tree diff inside the Named
Target Set only; it grants no commit, push, PR, merge, install, or deploy
authority.

## Adjudicator tail

Per `.agents/workflow-overlay/communication-style.md` → **Review Adjudication
Next Step**: the commissioning Chief Architect must first adjudicate F1–F5,
the patch diff, and the residuals above as claims (not premises). F1's fix is
self-closable (already applied on the lane branch, inside the commissioned
scope) — if the CA accepts F1, no further closure round-trip is needed for it.
F4 and F3 need an owner decision or a separate commission before any further
edit (they sit outside the Named Target Set or outside this patch's
smallest-complete bound, respectively). F5 needs reconciliation with the
author lane, not a code change. Once adjudicated, admin/lifecycle steps
(commit, push, PR) collapse into one batched land step per that doctrine; this
review does not perform that step.
