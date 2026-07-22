# Reddit Subreddit Registry Lake Cut-Over — Delegated Code Review-And-Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated_code_review_and_patch commission)
scope: >
  Commission for a de-correlated, different-vendor code review-and-patch pass over
  the Reddit Subreddit Registry lake cut-over implementation (stages 1-3a), with
  Chief Architect adjudication before any change is kept.
use_when:
  - Couriering the delegated review of the Reddit registry lake cut-over code.
  - Checking which failure class this commission was raised against, or adjudicating its return.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_lake_cutover_architecture_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
```

## Status

`COMMISSIONED — RETURNED, ADJUDICATED`. The first run returned
`BLOCKED_CONCURRENT_WRITER` (see *Return log*); its four findings were
adjudicated and patched. This artifact is the commission, not a review result;
it asserts no verdict, validation, or readiness.

Output mode: `paste-ready-chat` — this file is the courier body. The
controller's return goes to chat or the lane PR comment and writes no durable
report under `docs/review-outputs/` unless separately commissioned.

## Return log

- **2026-07-22, controller `gpt-5` (OpenAI), reviewed `82e00a77`:**
  `BLOCKED_CONCURRENT_WRITER`. The commissioning lane kept committing after the
  freeze at `bdbb04a7`, so the worktree moved under the controller. No
  commissioned file was patched and validation was not run — correct fail-closed
  behavior, and a process fault on the commissioning side, not the controller's.
  Four findings (RSR-01..RSR-04) were still returned from the read; all four
  were verified against source, accepted, and patched in `55e9b01b`.
  **Freeze discipline for any re-run: the commissioning lane must not commit
  between the freeze revision and the controller's return.**

## Why this was commissioned

Raised under the owner's `success implement` instruction, which is a
**conditional** commission: it activates only when a material failure mode
specific to the diff could pass every bound test and required CI because the
implementation and its validation share an assumption, or because the decisive
path has no independent oracle.

**The named failure class:** the roster-change **predecessor-chain semantics**
in `data_lake/reddit_subreddit_registry.py` (`_ordered_roster_chain`,
`_genesis_row`, and the genesis/delta split) have **no independent oracle.**

Contrast with the rest of the diff, which does:

- the migration fold is oracled by the frozen Git registry — `semantic_parity`
  compares it field-by-field against 35 rows produced by a different code path;
- the observation row effects are oracled by the superseded Git materializer
  `_apply_two_speed_refresh`, whose two-speed rule they mirror.

The chain logic is novel. Nothing pre-existing constrains it, so its
implementation and its tests encode one author's single model of correctness. A
wrong model — about what "exactly one head" means, when a fork is real, or
whether an `add` may follow a baseline — would pass every test in the suite.

Both repo-wide lake gates already caught real defects in this module (a lane
constant collision that regressed `creator_registry`, and a missing
sibling-selection posture), which raises rather than lowers the prior that a
correlated blind spot remains.

## Target state

```yaml
receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  launch_checkout: receiver_to_observe
  effective_target_worktree: "C:\\Users\\vmon7\\Desktop\\projects\\orca\\.claude\\worktrees\\reddit-graphing-lane-d07de4"
  required_revision: "bdbb04a75c7b1b3196ae0d73b3f33c870f1268ac"
  revision_mode: ancestor
  no_concurrent_writer_state: required — verify clean tree at bind
branch: claude/reddit-graphing-lane-d07de4
```

Verify ancestry and clean/no-writer state, record current `HEAD` as
`reviewed_revision`, and return both revisions.

## Target kind and scope

`delegated_code_review_and_patch`. Review method is the code review lane
(`workflow-code-review`), not artifact review.

Patchable file set — this set **cannot silently widen**; touching anything else
requires re-commission:

```text
forseti-harness/data_lake/reddit_subreddit_registry.py          <- primary
forseti-harness/capture_spine/reddit_subreddit_grid/materializer.py
forseti-harness/capture_spine/reddit_subreddit_grid/__init__.py
forseti-harness/runners/run_reddit_subreddit_registry_lake.py
forseti-harness/runners/run_reddit_subreddit_registry_refresh.py
forseti-harness/tests/unit/test_reddit_subreddit_registry_lake.py
forseti-harness/tests/unit/test_reddit_subreddit_grid.py
```

Read-only / flag-only, explicitly including: `data_lake/inventory.py` and
`tests/contract/test_capture_runner_lake_seam_coverage.py` (gate declarations —
flag a wrong declaration, do not re-declare it), the committed registry JSON
(byte-frozen for rollback), all product contracts under `forseti/`, every other
`.agents/workflow-overlay/` file, and every path the safety rules forbid.

## Priority order

1. **Chain and genesis semantics** (the commissioned failure class): is
   "exactly one unsuperseded head" the right invariant? Can a legitimate
   operator sequence produce a false `roster_head_ambiguous`, or a real fork
   escape it? Is the baseline-vs-`add` genesis split coherent, and can the two
   coexist or both be absent in a reachable state?
2. **Fold determinism**: can two lakes with identical records fold to different
   rows? Consider observation ordering ties, `descriptive_changes` accumulation,
   and repeated folds within one process.
3. **Fail-closed completeness**: any path where corrupt, conflicting, or
   partial records yield a plausible row instead of an error.
4. **Cut-over safety**: can anything still mutate the frozen registry JSON, and
   is the superseded Git writer genuinely unreachable from production?

## Validation

```text
python -m pytest forseti-harness/tests/unit forseti-harness/tests/contract -q
```

Run it and report real results. The repo-wide lake gates
(`test_data_lake_inventory_gate.py`, `test_capture_runner_lake_seam_coverage.py`,
`test_silver_lane_registry_guard.py`, `test_silver_reader_selection_gate.py`) are
load-bearing here — a failure is surfaced, never routed around. No live lake and
no Reddit capture: **live Reddit access is separately blocked**, see below.

## Standing blocker (do not attempt to clear)

The 2026-07-22 policy re-check found `www.reddit.com` and `old.reddit.com` both
serving `User-agent: * / Disallow: /`. No live radar pass is authorized, so the
stage-3 live readback is unproven by design, not by oversight. Do not run
capture, and do not treat the missing live proof as a defect to patch.

## Return

- findings, most material first, each with neutral but decision-sufficient
  source citations;
- a unified diff of working-tree edits inside the named file set only;
- real validation results, including anything not run;
- a verdict and a residual-risk note;
- `required_revision` and `reviewed_revision`.

`lifecycle_hard_stop`: working-tree edits only — no commit, push, PR, merge,
stash, reset, branch surgery, or repository hygiene.

`NEEDS_ARCHITECTURE_PASS` if the problem is design-level rather than
patch-level: stop patching, revert any partial diff, return findings only.

## De-correlation

```text
delivery: operator_courier_only
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
author_home_model_family: Anthropic (Claude, Opus 4.8) — authored the code and adjudicates the return
delegate_model_family: operator_to_fill — must be a different upstream vendor lineage, not a lower tier
de_correlation_status: operator-verify-on-receipt
```

Family means vendor lineage, not tier. Verify before any work; if you are
Anthropic-lineage, stop and say so rather than proceeding.

## Adjudication

The returned diff, citations, and verdict are claims for the Chief Architect to
adjudicate, not premises to inherit. It accepts, modifies, or rejects each
change against the citations and the implementation's intent, reverts rejected
hunks, and reserves final authority to veto.

## Non-claims

Not validation, not readiness, not a formal PASS, not ratification of the
cut-over architecture, not capture authorization, and not clearance of the
robots.txt blocker.
