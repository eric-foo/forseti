# Repo-Mode Delegated Adversarial Code Review + Patch Commission - Forseti Platform Account ID Migration (PR #795)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for a de-correlated adversarial code review
  and bounded patch pass on PR #795, which migrates Silver creator-metric
  account subject references from orca_platform_account_id to
  forseti_platform_account_id while preserving legacy read compatibility and
  correcting live-lake default roots to Forseti.
use_when:
  - Dispatching an independent delegated review-and-patch pass for PR #795.
  - Checking the exact review method, patchable file set, validation obligations,
    and provenance fields bound to the account-id migration review.
stale_if:
  - PR #795 is merged, closed, rebased, or amended past commit a0f08e1badacbfa35bef31aac6f45082459a078d.
  - The delegated review return has already been adjudicated by the commissioning lane.
authority_boundary: retrieval_only
```

## Pinned Fields

- Repository: `https://github.com/eric-foo/forseti`
- PR: `https://github.com/eric-foo/forseti/pull/795`
- Branch: `codex/forseti-platform-account-id-migration`
- Pinned commit: `a0f08e1badacbfa35bef31aac6f45082459a078d`
- Base at commission time: `origin/main` commit `f135dcb6`
- Access mode: `repo`. Inspect the repository/worktree directly. Do not review
  from memory, summaries, copied snippets, or a recreated source pack.
- Patch authorship: the delegate may author a bounded working-tree patch inside
  the Named Target Set only. Do not commit, push, merge, open PRs, rename
  branches, or edit outside the named set.
- Required report path:
  `docs/review-outputs/forseti_platform_account_id_migration_delegated_adversarial_code_review_v0.md`
- Author/home model provenance to record in the report:
  `authored_by: OpenAI/Codex GPT-5`

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch code-diff sibling mode +
    workflow-code-review + PR #795 diff + named target set below)
  edit_permission: docs-write for this prompt artifact only; delegate receives
    patch-only authority inside the Named Target Set in its own worktree
  target_scope: docs/prompts/reviews/forseti_platform_account_id_migration_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (commission branch clean at a0f08e1badacbfa35bef31aac6f45082459a078d)
  blocked_if_missing: AGENTS.md, overlay README, delegated-review-patch overlay,
    review-lanes overlay, prompt-orchestration overlay, workflow-code-review,
    PR #795 diff, or any Named Target Set file
repo_map_decision: not_needed
repo_map_reason: bounded PR diff with explicit source files and context reads.
```

## Paste-Ready Commission Body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT - gate yourself first:
- The reviewed PR was authored by `OpenAI/Codex GPT-5`.
- This commission requires a different vendor/model family for discovery.
- If you are OpenAI-lineage, if your model lineage is unknown, or if your
  lineage cannot be recorded, reply only:
  `BLOCKED_DECORRELATION`
  then stop.
- This is a who-constraint and provenance requirement, not a runtime model
  recommendation. Record your actual reviewer identity in the durable report as
  `reviewed_by`; use `unrecorded` only if the operator cannot supply it.

REPOSITORY ACCESS - read the pinned repository directly:
- repo: https://github.com/eric-foo/forseti
- PR: #795
- branch: codex/forseti-platform-account-id-migration
- pinned commit: a0f08e1badacbfa35bef31aac6f45082459a078d
- base at commission time: origin/main f135dcb6

If you cannot inspect the repo/worktree at the pinned branch or commit, reply
only `BLOCKED_REPO_UNREADABLE` with the missing source. Do not substitute a
summary, memory, or copied code. If the branch has advanced, record the commit
you actually reviewed and explain the delta from the pinned commit before doing
any review.

OPERATING CONTRACT:
- Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
- Read `.agents/workflow-overlay/delegated-review-patch.md`, especially the
  `delegated_code_review_and_patch` sibling mode.
- Read `.agents/workflow-overlay/review-lanes.md` and
  `.agents/workflow-overlay/prompt-orchestration.md`.
- Review method: `workflow-code-review`, after `workflow-deep-thinking`, under
  the Source-Gated Method Contract. This is code review, not artifact review.
- If `workflow-code-review` is unavailable or unresolved after source readiness,
  return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emit strict review-lane
  claims.

WHAT THE TARGET IS:
PR #795 migrates Silver creator-metric subject references from legacy
`subject.ref.orca_platform_account_id` writes to
`subject.ref.forseti_platform_account_id` writes, while preserving legacy-read
fallback for existing lake data. It also corrects live-lake runner default
roots from `ROOT / "orca"` to `ROOT / "forseti"` and updates focused tests.

WHY READ-ONLY REVIEW IS INSUFFICIENT:
This is a compatibility boundary in the data lake. A defect can silently split
old and new Silver rows, make revalidators miss existing accounts, or point
live runners at the wrong root. If you find a concrete bounded defect, author
the smallest complete patch inside the named file set so the commissioning lane
can adjudicate the diff instead of round-tripping through review prose.

NAMED TARGET SET - the ONLY patchable files; cannot silently widen:

Production / reader surface:
1. `forseti-harness/capture_spine/creator_profile_current/silver_subject_ref.py`
2. `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
3. `forseti-harness/capture_spine/creator_profile_current/tiktok_silver_metric_producer.py`
4. `forseti-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`
5. `forseti-harness/capture_spine/creator_profile_current/silver_metric_reader.py`
6. `forseti-harness/capture_spine/creator_profile_current/rollup_formula_revalidation.py`

Runner surface:
7. `forseti-harness/runners/run_creator_metric_rollup_producer.py`
8. `forseti-harness/runners/run_creator_metric_rollup_snapshot.py`
9. `forseti-harness/runners/run_live_lake_freshness_gate.py`
10. `forseti-harness/runners/run_tiktok_batch_metric_rollup_producer.py`
11. `forseti-harness/runners/run_youtube_creator_metric_rollup_producer.py`
12. `forseti-harness/runners/run_youtube_watch_packet_metric_rollup_producer.py`

Focused tests:
13. `forseti-harness/tests/unit/test_creator_metric_silver_discovery.py`
14. `forseti-harness/tests/unit/test_creator_metric_silver_reader.py`
15. `forseti-harness/tests/unit/test_creator_metric_silver_snapshot.py`
16. `forseti-harness/tests/unit/test_tiktok_creator_metric_silver_producer.py`
17. `forseti-harness/tests/unit/test_youtube_creator_metric_rollup_producer_runner.py`
18. `forseti-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`
19. `forseti-harness/tests/unit/test_youtube_watch_packet_metric_rollup_producer_runner.py`

Everything outside that set is read-only / flag-only. A fix that requires an
unnamed file, canonical artifact, overlay file, generated file, data file, or
real lake mutation is a finding requiring recommission or CA action, not an
edit. Do not edit `.agents/**`, `AGENTS.md`, historical compatibility docs,
real lake data, branch metadata, or workflow doctrine.

SOURCE-GATED METHOD:
1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review`. Do not
   APPLY them yet.
2. SOURCE-LOAD the PR diff: `git diff origin/main...HEAD`, the Named Target
   Set, and the read-only context below.
3. Declare `SOURCE_CONTEXT_READY`, or `SOURCE_CONTEXT_INCOMPLETE` with missing
   sources and material gaps.
4. Only after source readiness, APPLY deep thinking to frame failure modes.
5. Then APPLY `workflow-code-review` in findings-first, coverage-first posture.

READ-ONLY CONTEXT TO INSPECT:
- `git diff --stat origin/main...HEAD` and `git diff origin/main...HEAD`.
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md`
  for the historical subject-ref contract and cutover context.
- Any adjacent producer/reader helper imported by the Named Target Set that
  materially affects a finding.
- Existing tests for the same Silver reader/producer/runner surface if a fake
  pass or missing red path is suspected.

ADVERSARIAL AXES TO ATTACK:
- New-write semantics: every producer and runner-created path that writes an
  account subject ref should write `forseti_platform_account_id`, not keep
  silently writing `orca_platform_account_id`.
- Legacy-read compatibility: readers, discovery, snapshots, and revalidation
  must still map existing `orca_platform_account_id` rows to the same account.
- Mixed-row behavior: new and old rows for the same account should not fork,
  double-count, disappear, or produce order-dependent results.
- Missing/invalid refs: no fake success path when neither key is present, both
  keys disagree, or a ref is malformed.
- Runner root defaults: live-lake defaults should point at the Forseti root
  without breaking explicit CLI overrides or temporary-test roots.
- Test adequacy: tests must exercise real helper behavior and catch regressions
  in both new-write and legacy-read behavior; mocks must not make the migration
  look green while production stays wrong.
- Scope discipline: the compatibility escape hatch should be narrow and named;
  long-term Forseti terminology should not erase necessary legacy read support.

VALIDATION OBLIGATIONS:
Run or explicitly report blocked/not-run for these commands from the repo root:

```powershell
python -m py_compile forseti-harness\capture_spine\creator_profile_current\silver_subject_ref.py forseti-harness\capture_spine\creator_profile_current\silver_metric_producer.py forseti-harness\capture_spine\creator_profile_current\tiktok_silver_metric_producer.py forseti-harness\capture_spine\creator_profile_current\youtube_silver_metric_producer.py forseti-harness\capture_spine\creator_profile_current\silver_metric_reader.py forseti-harness\capture_spine\creator_profile_current\rollup_formula_revalidation.py forseti-harness\runners\run_creator_metric_rollup_producer.py forseti-harness\runners\run_creator_metric_rollup_snapshot.py forseti-harness\runners\run_live_lake_freshness_gate.py forseti-harness\runners\run_tiktok_batch_metric_rollup_producer.py forseti-harness\runners\run_youtube_creator_metric_rollup_producer.py forseti-harness\runners\run_youtube_watch_packet_metric_rollup_producer.py
python -m pytest -q -p no:cacheprovider forseti-harness\tests\unit\test_creator_metric_silver_reader.py forseti-harness\tests\unit\test_creator_metric_silver_discovery.py forseti-harness\tests\unit\test_creator_metric_silver_snapshot.py forseti-harness\tests\unit\test_tiktok_creator_metric_silver_producer.py forseti-harness\tests\unit\test_youtube_creator_metric_silver_producer.py forseti-harness\tests\unit\test_youtube_creator_metric_rollup_producer_runner.py forseti-harness\tests\unit\test_youtube_watch_packet_metric_rollup_producer_runner.py
git diff --check
python .agents\hooks\check_silver_lane_registry.py
```

Do not run `registration_integrity.py --selftest`; that check is outside this
commission and has an unrelated known stall/failure mode for this lane.

Commission-time evidence from the author lane, for you to verify rather than
trust:
- The focused pytest command above previously reported 90 passed and 2 skipped.
- `git diff --check` previously exited 0 with only line-ending warnings.
- `check_silver_lane_registry.py` previously reported OK.
- `header_index.py --strict`, `check_repo_map_freshness.py --strict`, and
  `check_review_routing.py --strict` previously passed on the implementation
  commit.

RETURN, in this order:
1. Durable report written to
   `docs/review-outputs/forseti_platform_account_id_migration_delegated_adversarial_code_review_v0.md`.
2. `review_summary` YAML with:
   - `status`
   - `report_path`
   - `reviewed_by`
   - `authored_by: OpenAI/Codex GPT-5`
   - `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded`
   - `access: repo`
   - reviewed branch and commit
   - finding counts by severity
   - `patch_applied: yes | no`
   - validation commands and real results
   - verdict
   - `next_authorized_action`
3. Findings first, ordered critical -> major -> minor. Each actionable finding
   must include severity, confidence, location, evidence, impact,
   `minimum_closure_condition` as an end state, and `next_authorized_action`.
4. `considered_and_defended` for plausible issues you checked and rejected.
5. Unified diff for any bounded patch inside the Named Target Set, left
   uncommitted, or an explicit `patch_applied: no` explanation.
6. Non-findings, not-proven boundaries, residual risks, and validation gaps.
7. Adjudicator tail: the commissioning CA must adjudicate findings, diff,
   verdict, and residuals as claims before keeping any delegated changes.

If a design-level problem cannot be fixed inside the Named Target Set, return
`NEEDS_ARCHITECTURE_PASS`, do not patch, and explain the smallest architecture
question that must be answered.

NON-CLAIMS:
- This output is decision input only. It is not approval, readiness, validation,
  acceptance, merge authority, deployment authority, or a runtime model
  recommendation.
- The commission grants patch authority only inside the Named Target Set in the
  reviewer worktree. It grants no commit, push, PR, branch, merge, install,
  deploy, or lifecycle action.
````

## Operator Notes

- Paste the commission body into a repo-access-capable controller that satisfies
  the different-family who-constraint from the author lane.
- Courier the full return back to the commissioning lane for adjudication.
- If a bounded patch is returned, adjudicate each hunk before keeping it; then
  run byte/scope checks and the named validation gates.
