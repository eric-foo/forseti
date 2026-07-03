# Session-Start Hook Latency Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed cross-recipient prompt for a read-only adversarial code review of the
  session-start hook latency change: IN_SCOPE_PREFIXES-scoped header-index
  walk and concurrent capsule gather with --no-optional-locks git reads.
use_when:
  - Commissioning a de-correlated reviewer for PR 611 (claude/hook-guard-latency).
  - Checking whether the perf change preserves hook behavior, fail-open contracts, and result equivalence.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/validation-gates.md
  - .agents/hooks/header_index.py
  - .agents/hooks/session_context_capsule.py
  - .agents/hooks/check_retrieval_header.py
  - orca-harness/tests/unit/test_hook_internal_error_gating.py
authoring_branch: claude/hook-guard-latency
authoring_base_observed: origin/main @ f751040954d256bf6e014cc4e121593ea34085a3
stale_if:
  - The reviewer cannot identify the PR/branch head being reviewed.
  - Either target hook file differs from the PR/branch head under review.
  - The implementation diff includes files outside the declared target scope, except this prompt artifact.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/session_start_hook_latency_adversarial_code_review_prompt_v0.md`
- review_report_destination: `docs/review-outputs/session_start_hook_latency_adversarial_code_review_v0.md`
- template_kind: `review`; Orca has no bound repo-code-review template, so this prompt uses the overlay review contract directly.
- authorization_basis: owner selected the delegated cross-vendor review route for PR 611's review-routing disposition (this thread, 2026-07-03).
- edit_permission: `read-only`; reviewer may write only the review report at the destination above.
- expected_worktree: repo-backed checkout or worktree for branch `claude/hook-guard-latency`.
- expected_branch: `claude/hook-guard-latency` unless the dispatcher supplies a PR checkout that resolves to the same branch head.
- expected_head: derive from `git rev-parse HEAD` at dispatch; the reviewed code commit is `7d850595536d00f69a5bbc4a400706f78c8e39fd`; this prompt artifact may sit in commits above it.
- expected_pr: `https://github.com/eric-foo/orca/pull/611`
- dirty_state_allowance: prompt/report docs may be dirty or untracked. Target hook files must be clean relative to the reviewed head.
- target_files_or_dirs:
  - `.agents/hooks/header_index.py` (walk_durable_mds only)
  - `.agents/hooks/session_context_capsule.py` (imports, _git, gather only)
  - Read-only compatibility context: `.agents/hooks/check_retrieval_header.py` (IN_SCOPE_PREFIXES / EXCLUDED_PREFIXES / scope_folder), `orca-harness/tests/unit/test_hook_internal_error_gating.py`.
- validation_gates:
  - Verify branch, HEAD, target diff, and dirty state before strict findings.
  - Run only offline tests/compilation/checks; no network, no gh mutations.
- doctrine_change_decision: no doctrine change requested. Return `NEEDS_ARCHITECTURE_PASS` for design-level concerns; do not edit doctrine.
- isolation_decision: reviewer uses existing PR/worktree; no new writing branch required for read-only review.

## Commission

You are the de-correlated controller for a read-only adversarial code review. The reviewed patch was authored by an Anthropic/Claude-family agent. To satisfy the discovery bar, your controller vendor/model lineage must be different from Anthropic/Claude-family. This is a who-constraint, not a runtime model recommendation.

If you are Anthropic/Claude-family, same-vendor, self-reviewing, or your lineage is unknown, stop and return:

```text
BLOCKED_CONTROLLER_NOT_DECORRELATED
```

If you do not have filesystem access to the expected repo/worktree, stop and request a repo-backed source capsule or no-repo handoff. Do not review from this prompt summary alone.

Your task is to decide whether this latency change is behavior-preserving and truthfully claimed before merge. These hooks are session-start infrastructure: the capsule's output is injected into every session's context, and header_index feeds both the capsule health line and advisory retrieval tooling. A silent misreport (wrong tree counts, dropped in-scope file, phantom-clean capsule) is worse than slowness. Findings are decision input only; they are not approval, validation, mandatory remediation, merge authority, or patch authority.

## Required Method Sequence

1. Read this prompt.
2. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
3. REFERENCE-LOAD `workflow-code-review`. Do not APPLY it yet.
4. SOURCE-LOAD the authority and task sources below.
5. Declare `SOURCE_CONTEXT_READY` with a compact source-read ledger, or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and blocked claims.
6. Only after source readiness, APPLY `workflow-deep-thinking` to frame the highest-risk failure modes.
7. Then APPLY `workflow-code-review` to review the implementation.
8. Write findings first. Do not patch.

If either method is unavailable, name that fact. You may still provide advisory-only critique, but do not emit strict review claims, readiness claims, validation claims, mandatory remediation, or merge recommendations as if the method contract was satisfied.

## Confirm-Do-Not-Trust Load Contract

Do not trust any implementation facts in this prompt until you verify them from the repo and files.

Before strict or actionable claims:

1. Run `git rev-parse HEAD` and record the reviewed target commit.
2. Run `git status --short --branch` and confirm the reviewed branch/head and that the two target hook files are clean relative to that head. Prompt/report docs may be dirty only if you explicitly exclude them from source findings.
3. Run `git diff --name-only origin/main...HEAD` or the PR base equivalent and confirm the implementation target diff is limited to:
   - `.agents/hooks/header_index.py`
   - `.agents/hooks/session_context_capsule.py`
   - this prompt artifact, if included in the branch.
4. Read the target files and required context below. Do not make source-backed claims from commit messages, PR text, prior thread summaries, or this prompt alone.

If the branch, HEAD, target scope, or disallowed dirty state does not match, return `BLOCKED_TARGET_MISMATCH` with observed values.

## Required Authority Sources

Read these before strict findings:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-loading.md` (apply its Routine Read Shapes; bounded reads are the compliant act)
4. `.agents/workflow-overlay/review-lanes.md`
5. `.agents/workflow-overlay/validation-gates.md`

Then source-load the code and compatibility context:

1. `.agents/hooks/header_index.py`
2. `.agents/hooks/session_context_capsule.py`
3. `.agents/hooks/check_retrieval_header.py` (scope_folder, IN_SCOPE_PREFIXES, EXCLUDED_PREFIXES — the equivalence argument rests on these)
4. `orca-harness/tests/unit/test_hook_internal_error_gating.py`

## Observed Patch Intent To Verify

Treat this as orientation only until source-verified:

- `header_index.walk_durable_mds` walks only the nine `IN_SCOPE_PREFIXES` roots instead of `os.walk(root)` over the whole repo, keeping the per-file `scope_folder` filter. Claimed byte-identical result sets: 898 files in the authoring worktree, 659 in the main checkout; main-checkout walk 6064ms -> 33ms (the old walk recursed into nested worktree copies).
- `session_context_capsule.gather` submits its eight child calls (six `_git` reads + `retrieval_health_line` + `ontology_expansion_line`) to a `ThreadPoolExecutor(max_workers=8)` and collects results after the pool exits, preserving the exact output construction. Capsule `--hook` claimed 1264-5662ms (median 2427) -> 820-956ms (median 834) in the authoring worktree.
- `_git` gains the global `--no-optional-locks` flag so concurrent `git status` reads cannot take `index.lock` for an opportunistic refresh and make a sibling call fail into `""` (which would silently misreport tree state).

## Observed Validation To Verify

Prompt-author observed validation (all in the authoring worktree at commit `7d850595`):

- Walk equivalence: old-vs-new `walk_durable_mds` output byte-identical in the authoring worktree (898 files) and against the main checkout root (659 files, `identical=True`).
- `python .agents/hooks/header_index.py --selftest` -> `SELFTEST OK`.
- `python .agents/hooks/session_context_capsule.py --selftest` -> `SELFTEST OK`.
- `session_context_capsule.py --check` output identical before/after modulo true tree-state changes (it reported this change's own two modified files).
- Hook-mode smoke: `'{"source":"startup"}' | python .agents/hooks/session_context_capsule.py --hook` -> exit 0, capsule first line correct.
- `python -m pytest orca-harness/tests/unit/test_hook_internal_error_gating.py -q` -> 22 passed.
- `python -m pytest orca-harness/tests -q` -> exit 0 (1 unrelated skip).

No main-checkout capsule end-to-end run was performed (the main checkout runs the pre-change code until merge). Do not upgrade the authoring-worktree timings into main-checkout capsule claims beyond the isolated walk benchmark.

## Review Checks

Be adversarial inside this target. Focus on silent misreport paths, equivalence gaps, and concurrency hazards.

Answer at least:

1. Is the walk-scope equivalence argument airtight? `scope_folder()` must accept nothing outside `IN_SCOPE_PREFIXES`. Can a prefix entry (trailing slash, case, path-separator form) make `root / prefix` miss a directory that the old whole-repo walk would have reached? Windows case-insensitivity?
2. Does the new walk change behavior when an `IN_SCOPE_PREFIXES` entry is later added that does not exist on disk, is a file, or is a symlink/junction?
3. Are the `.git*`/`node_modules`/`__pycache__` prunes still equivalent now that they apply only inside in-scope roots?
4. ThreadPoolExecutor semantics: does the `with` block guarantee all futures complete before `.result()` calls? Can an exception in one child leak, deadlock, or bypass the module's fail-open contract (`main()`'s top-level try/except)? Is exit ever nonzero on a child failure?
5. Can eight concurrent subprocesses on Windows (six git + two nested `python` spawns) interleave badly: shared stdio inheritance, `timeout=5` per child now overlapping, orphaned children on timeout, CPU contention inflating the 5s timeouts into false fail-opens?
6. `--no-optional-locks`: does it change any *output* of `rev-parse`/`log`/`status --porcelain`/`diff --name-only`? Are there git versions where the flag is unsupported and the call now fails into `""` (silent misreport) — and is that a real concern for this machine/CI?
7. Concurrent `git status` + `git diff` on the same repo without optional locks: any remaining lock or racy-index path that could intermittently return nonzero -> `""` -> phantom-clean capsule?
8. Does the capsule's output construction remain byte-identical given identical child outputs (ordering, strip semantics, None sentinels)?
9. Do the selftests and the internal-error gating tests still cover what they covered before, or did the change move logic out from under them (e.g., gather no longer exercised by any test)?
10. Is any issue design-level enough to return `NEEDS_ARCHITECTURE_PASS` instead of a patch request?

## Drift Guard

Do not perform or request:

- patching source files;
- broad repo cleanup, prompt-template changes, or overlay doctrine changes;
- merge, commit, push, or PR state changes;
- network access or `gh` mutations;
- changes to hook registration in `.claude/settings.json`.

## Allowed Validation

You may run offline validation from the reviewed worktree:

```powershell
python .agents/hooks/header_index.py --selftest
python .agents/hooks/session_context_capsule.py --selftest
python -m pytest orca-harness/tests/unit/test_hook_internal_error_gating.py -q
python -m compileall -q .agents\hooks\header_index.py .agents\hooks\session_context_capsule.py
```

You may reproduce the walk-equivalence probe by importing `header_index` via `importlib` and comparing the new `walk_durable_mds(root)` against an inline reimplementation of the old whole-repo walk. If blocked by local tooling, report `not_run`; do not treat that as a code finding.

## Output Contract

Write the durable report to:

`docs/review-outputs/session_start_hook_latency_adversarial_code_review_v0.md`

The report must include:

- retrieval header with `authority_boundary: retrieval_only`;
- `reviewed_by` and `authored_by` fields in the body; use `unrecorded` only if not supplied, never fabricate;
- `de_correlation_bar: cross_vendor_discovery`;
- source-read ledger with file paths and line references for load-bearing claims;
- findings first, ordered by severity: `critical`, `major`, `minor`;
- for each finding: severity, location, issue, evidence with file:line cites, impact, minimum closure condition, next authorized action, and whether a patch is requested from the authoring lane;
- explicit answers to the Review Checks above;
- validation commands and observed outputs, or `not_run` reasons;
- residual risks;
- review-use boundary.

Do not include `patch_queue_entry`. Do not edit source files.

After writing the report, return this compact chat summary:

```yaml
review_summary:
  status: completed | failed | blocked
  review_location: durable_report | chat_only_current_thread
  report_path:
  reviewed_by:
  authored_by: Anthropic/Claude-family
  de_correlation_bar: cross_vendor_discovery
  target_commit: <observed git rev-parse HEAD>
  pr: https://github.com/eric-foo/orca/pull/611
  validation_run:
    selftests: run | not_run
    pytest_gating: run | not_run
    compileall: run | not_run
    walk_equivalence_probe: run | not_run
  top_findings:
    - severity:
      issue:
      location:
  recommendation: merge_after_green | patch_before_merge | keep_draft | needs_architecture_pass | blocked
  next_action:
```

Review-use boundary:
This review is decision input only. It is not approval, validation, readiness, mandatory remediation, implementation authorization, merge authority, or executor-ready patch authority until separately accepted or authorized by the Orca owner / Chief Architect.
