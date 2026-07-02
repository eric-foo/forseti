# Session-Start Hook Latency Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Read-only adversarial code review report for PR 611 session-start hook latency change.
use_when:
  - Deciding whether PR 611's hook latency change needs patching before merge.
  - Checking the behavior-preservation evidence for scoped header-index walking and concurrent capsule gather.
stale_if:
  - PR 611 target hook files change after target commit c5d628948ad63add15ca50eee7f58f120413e9e8.
  - The review prompt is superseded or the branch head changes.
open_next:
  - docs/prompts/reviews/session_start_hook_latency_adversarial_code_review_prompt_v0.md
  - .agents/hooks/header_index.py
  - .agents/hooks/session_context_capsule.py
  - .agents/hooks/check_retrieval_header.py
  - orca-harness/tests/unit/test_hook_internal_error_gating.py
authority_boundary: retrieval_only
```

## Findings

No `critical`, `major`, or `minor` findings.

No patch is requested from the authoring lane by this review. The reviewed code path is behavior-preserving on the observed branch under the checks run here: the target diff is limited to the commissioned hook files plus this prompt artifact, the two target hook files are clean relative to the reviewed head, old-vs-new `walk_durable_mds` result sets are identical in this worktree, local Git supports `--no-optional-locks`, and the concurrent capsule path emitted coherent live state.

## Review Metadata

```yaml
reviewed_by: GPT-5 (Codex)
authored_by: Anthropic/Claude-family
de_correlation_bar: cross_vendor_discovery
pr: https://github.com/eric-foo/orca/pull/611
review_prompt: docs/prompts/reviews/session_start_hook_latency_adversarial_code_review_prompt_v0.md
target_branch: claude/hook-guard-latency
target_commit_observed: c5d628948ad63add15ca50eee7f58f120413e9e8
reviewed_code_commit: 7d850595536d00f69a5bbc4a400706f78c8e39fd
merge_base_observed: f751040954d256bf6e014cc4e121593ea34085a3
output_mode: review-report
report_path: docs/review-outputs/session_start_hook_latency_adversarial_code_review_v0.md
```

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom review prompt + required authority/code sources
  edit_permission: read-only plus review report write
  target_scope: PR 611 hook latency change in .agents/hooks/header_index.py and .agents/hooks/session_context_capsule.py
  dirty_state_checked: yes
  blocked_if_missing: branch/head mismatch, target hook dirt, target diff outside allowed scope, missing required sources
```

## Confirm-Do-Not-Trust Results

```text
git rev-parse HEAD
c5d628948ad63add15ca50eee7f58f120413e9e8

git status --short --branch
## claude/hook-guard-latency...origin/claude/hook-guard-latency

git diff --name-only origin/main...HEAD
.agents/hooks/header_index.py
.agents/hooks/session_context_capsule.py
docs/prompts/reviews/session_start_hook_latency_adversarial_code_review_prompt_v0.md

git diff --name-only -- .agents/hooks/header_index.py .agents/hooks/session_context_capsule.py
<no output>

git ls-files --others --exclude-standard
<no output before report write>
```

The prompt permits prompt/report docs to be dirty or untracked and requires target hook files to be clean. At review time before this report write, the target hook files had no unstaged diff and there were no untracked files.

## Source-Read Ledger

- `docs/prompts/reviews/session_start_hook_latency_adversarial_code_review_prompt_v0.md`: read fully. Binds destination, read-only permission, expected branch/head, target scope, method sequence, review checks, allowed validation, output contract, and review-use boundary. Load-bearing lines: 38, 41, 43-48, 84-98, 100-114, 139-164, 166-176, 179-225.
- `AGENTS.md`: read fully. Binds smallest complete intervention, fresh-read verification, Orca overlay authority, review routing, and allowed documentation/review work.
- `.agents/workflow-overlay/README.md`: read fully. Binds Orca overlay as project authority and routes review/validation/source-loading authority.
- `.agents/workflow-overlay/source-loading.md`: read fully. Binds start preflight and source-read ledger expectations. Load-bearing line: 77 for `orca_start_preflight`.
- `.agents/workflow-overlay/review-lanes.md`: read fully. Binds read-only review conduct, findings-first review output, provenance fields, de-correlation bar, and no executor-ready patch handoff in ordinary read-only reviews. Load-bearing lines: 76, 93-96, 113-143, 182.
- `.agents/workflow-overlay/validation-gates.md`: read fully. Binds failure-visible validation and git status reporting. Load-bearing lines: 19, 49-58, 94.
- `.agents/hooks/check_retrieval_header.py`: read fully for `IN_SCOPE_PREFIXES`, `EXCLUDED_PREFIXES`, and `scope_folder`. Load-bearing lines: 76-86, 90-95, 150-160.
- `.agents/hooks/header_index.py`: read fully for changed walk behavior and error contracts. Load-bearing lines: 242-268.
- `.agents/hooks/session_context_capsule.py`: read fully for `--no-optional-locks`, child process timeouts, concurrent gather, output ordering, and top-level fail-open behavior. Load-bearing lines: 146-158, 161-181, 184-202, 205-232, 324-339.
- `orca-harness/tests/unit/test_hook_internal_error_gating.py`: read fully for internal-error gating coverage. Load-bearing lines: 31-45, 56-62, 65-83.

## Deep-Thinking Failure-Mode Frame

The highest-risk failure modes were:

1. Scoped walk silently drops or duplicates files that the prior whole-repo walk would have returned.
2. Concurrent capsule gather turns a child failure or timeout into a coherent-looking but false clean capsule.
3. `--no-optional-locks` is unsupported or output-affecting in the active Git environment.
4. Validation still exercises only pure helpers while the changed concurrent path escapes automated coverage.

The review conclusion below is calibrated to observed branch/source evidence and local offline validation only. It is not merge authority or readiness proof.

## Review Checks

1. Walk-scope equivalence is airtight for the current constants. `scope_folder()` accepts only `.md` paths under the nine current `IN_SCOPE_PREFIXES` and rejects `README.md` plus excluded prefixes (`check_retrieval_header.py:76-95`, `check_retrieval_header.py:150-160`). The new walk iterates exactly those current roots, then applies `scope_folder()` again before appending (`header_index.py:252-268`). The old-vs-new probe found `old_count=899`, `new_count=899`, `identical=True`. Current prefix spelling and casing are directory-like and match the repo. Future non-directory, overlapping, symlink/junction, or case-mismatched prefix changes would need re-review because the equivalence argument depends on the present directory-prefix convention.
2. Missing current prefix directories remain equivalent: no accepted descendants can exist if the directory is absent. A future prefix that points to a file or violates the trailing directory-prefix convention could be non-equivalent; current constants do not do that.
3. `.git*`, `node_modules`, and `__pycache__` pruning is equivalent for accepted files. The prior walk pruned these names globally, but only paths accepted by `scope_folder()` could enter the result; the new walk applies the same prune inside the only accepted roots (`header_index.py:256-261`).
4. `ThreadPoolExecutor` semantics are acceptable. Exiting the `with ThreadPoolExecutor(max_workers=8)` block waits for all submitted futures; `.result()` calls then collect outputs in the same order used by the old serial construction (`session_context_capsule.py:205-232`). `_git`, `retrieval_health_line`, and `ontology_expansion_line` catch the declared subprocess and timeout failures and return fail-open sentinels (`session_context_capsule.py:146-181`, `session_context_capsule.py:184-202`). An unexpected child exception would re-raise at `.result()` and be caught by the module-level fail-open handler (`session_context_capsule.py:334-339`), so the hook still exits 0.
5. Concurrent subprocess interleaving risk is bounded by `capture_output=True`, so child stdout/stderr does not share the parent stream (`session_context_capsule.py:154-155`, `session_context_capsule.py:173-176`, `session_context_capsule.py:193-197`). Each child keeps its own 5 second timeout. A severely loaded Windows machine could still cause fail-open omissions or empty git outputs; the live `--check` run did not reproduce that and completed with populated branch/head/tree/retrieval health.
6. `--no-optional-locks` is supported in this reviewed environment: `git --version` reported `git version 2.54.0.windows.1`, and `git --no-optional-locks status --porcelain` exited 0 with no output on the clean tree. The affected commands are read-only status/diff/log/rev-parse calls (`session_context_capsule.py:146-158`, `session_context_capsule.py:210-216`). No local evidence showed output differences. Very old Git versions without the flag would fail into empty strings, which is a compatibility residual, not a reproduced branch finding.
7. Remaining lock/racy-index risk is reduced, not eliminated. `--no-optional-locks` addresses opportunistic index-refresh locking on the concurrent git reads. A non-optional failure would still fail open to `""` (`session_context_capsule.py:146-158`), but no such failure was observed in the validation probes.
8. Output construction remains byte-identical when child outputs are identical. Futures are read back in the original sequence and passed to the unchanged `build_capsule` call (`session_context_capsule.py:219-232`). Strip/list semantics match the old diff for branch, head, subjects, status, config dirt, doctrine, retrieval health, and expansion.
9. Existing selftests still cover pure helper behavior and internal-error gates still cover the listed CI hook scripts. The changed concurrent `gather()` path is not unit-covered by `session_context_capsule.py --selftest`; it was exercised here by a live `python .agents/hooks/session_context_capsule.py --check` run. This is a test-depth residual, not a patch-before-merge finding.
10. No issue found here is design-level enough to return `NEEDS_ARCHITECTURE_PASS`.

## Validation

```text
python .agents/hooks/header_index.py --selftest
...
SELFTEST OK
```

```text
python .agents/hooks/session_context_capsule.py --selftest
SELFTEST OK
```

```text
python -m pytest orca-harness/tests/unit/test_hook_internal_error_gating.py -q
......................                                                   [100%]
```

```text
python -m compileall -q .agents\hooks\header_index.py .agents\hooks\session_context_capsule.py
<exit 0, no output>
```

```text
walk-equivalence probe
old_count=899
new_count=899
identical=True
```

```text
git --version
git version 2.54.0.windows.1

git --no-optional-locks status --porcelain
<exit 0, no output>
```

```text
python .agents/hooks/session_context_capsule.py --check
[lane-state capsule | source=check]
repo: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\objective-mirzakhani-fc351f
branch: claude/hook-guard-latency @ c5d62894 Add adversarial code-review commission for PR 611 (review routing)
tree: 0 modified, 0 untracked
config-surface dirt (CLAUDE.md/AGENTS.md/.claude/.agents): clean
doctrine state: DIFFERS from last-fetched origin/main (2 files: .agents/hooks/header_index.py, .agents/hooks/session_context_capsule.py)
retrieval health: 35 missing headers, 0 orphans
```

No network, `gh`, source patching, merge, commit, push, PR mutation, hook registration change, broad cleanup, prompt-template change, or overlay doctrine change was performed.

## Residual Risks

- Future edits to `IN_SCOPE_PREFIXES` need a same-check equivalence probe if they add overlapping prefixes, non-directory prefixes, symlink/junction prefixes, or casing that differs from the worktree's actual directory names. The current branch does not contain those conditions.
- The fail-open contract still means a git failure can collapse to empty output, and `tree_counts("")` renders as `0 modified, 0 untracked`. That behavior predates this patch; this review only verified the latency change did not reproduce it locally.
- `session_context_capsule.py --selftest` does not unit-test `gather()` concurrency. The live `--check` run is useful evidence, but it is weaker than an automated equivalence test.

## Recommendation

`merge_after_green`

Meaning: this review found no patch-before-merge issue in the commissioned target, and the local validation listed above passed. Merge still depends on the normal owner/CI/branch-protection gates; this review is not approval, readiness, validation, or merge authority.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness, mandatory remediation, implementation authorization, merge authority, or executor-ready patch authority until separately accepted or authorized by the Orca owner / Chief Architect.
