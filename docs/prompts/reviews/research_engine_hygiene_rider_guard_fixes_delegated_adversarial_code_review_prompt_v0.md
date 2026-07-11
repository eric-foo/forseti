# Research-Engine Hygiene-Rider Guard Fixes — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (delegated adversarial code review request)
scope: >
  Findings-first adversarial code review of the 2026-07-10 hygiene-rider guard
  fixes on the research-engine strategy lane: HOOK-1 path relativization, HOOK-8
  --hook output-channel + diff-scoping change, and the check_csb_scanning_artifact
  version-scoped legacy grandfathering. Read-only; findings only.
use_when:
  - Running an independent review of the hygiene-rider hook changes before/after merge of PR #837.
authority_boundary: retrieval_only
```

## Output Mode / Contract (Forseti Prompt Preflight, inline)

- **Output mode:** findings-first review, chat or review-output artifact. No
  patch application in this pass.
- **Edit permission:** READ-ONLY. Reviewer proposes findings; does not edit,
  stage, commit, or push. Any patch is a separate routed pass.
- **Targets (branch `claude/research-engine-strategy-3a7619`, commit `e16b5e39`):**
  - `.agents/hooks/check_search_surface_google_route.py` — new `_relativize()`;
    `analyze_file` now relativizes absolute hook-payload paths before `in_scope()`.
  - `.agents/hooks/check_full_gt_claims.py` — `run_hook()` now emits
    `hookSpecificOutput.additionalContext` JSON on stdout (was stderr) and scans
    only lines changed vs HEAD via new `_added_lines_vs_head()` (whole-file
    fallback for new/untracked files).
  - `.agents/hooks/check_csb_scanning_artifact.py` — new
    `PRE_CONTRACT_LEGACY_ARTIFACTS` frozenset; `auto_targets()` skips those 3
    paths; selftest asserts skip + that a current-contract artifact still targets.
  - `.agents/hooks/header_index.py` — `orca` → `forseti` path repoints (report
    walk + repo-map fallback).
- **No runtime-model routing.** Reviewer is not directed to any model tier.
- **Doctrine-change:** none claimed; these are guard bug-fixes + owner-adjudicated
  grandfathering, not a doctrine change.

## What To Adversarially Check

1. **HOOK-1 relativization correctness.** Does `_relativize()` correctly keep
   out-of-repo absolute paths OUT of scope (no false-positive findings on
   unrelated files)? Any symlink / case-fold / mixed-separator escape? Does it
   preserve prior behavior for repo-relative inputs?
2. **HOOK-8 output + scope change.** Is the stdout `additionalContext` JSON shape
   correct for a PostToolUse hook (matches sibling hooks)? Does the diff-vs-HEAD
   scoping ever MISS an added full-GT claim it previously caught (e.g. staged but
   not committed, or a rename)? Is the untracked-file whole-file fallback sound?
   Confirm it still always exits 0 (advisory) and fails open.
3. **CSB grandfather blast radius.** Can the `PRE_CONTRACT_LEGACY_ARTIFACTS` skip
   over-match (prefix vs exact)? Confirm it is exact-path only and cannot mask a
   NEW artifact. Confirm explicit-path invocation still validates strictly.
   Is grandfathering the right call vs retrofitting the 3 artifacts?
4. **Regressions.** Any selftest that passes but asserts the wrong thing? Any
   fail-open path that now fails closed (or vice versa)?

## Boundary

Findings only. Not validation, not readiness, not approval, not authorization to
merge. A patch pass, if warranted, is separately routed via
`workflow-delegated-review-patch`.
