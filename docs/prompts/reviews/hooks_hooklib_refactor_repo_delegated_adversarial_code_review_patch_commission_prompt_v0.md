# Hooks _hooklib Refactor — Delegated Adversarial Code Review-And-Patch Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact (delegated review-and-patch commission)
scope: >
  Commission prompt for the de-correlated adversarial code review-and-patch of
  the .agents/hooks shared-helper refactor (_hooklib.py extraction, six wired
  advisory hooks migrated, once-per-session prompt-preflight throttle, repo-map
  read pre-gate, README/settings cleanup) on lane
  claude/code-hooks-optimization-2e26b3.
use_when:
  - Dispatching the delegated review of the hooks _hooklib refactor lane.
  - Adjudicating the return (this prompt binds the return contract).
authority_boundary: retrieval_only
```

Operator paste-instruction (who-constraint, not a model recommendation): the
author and adjudicator is Anthropic/Claude; paste the body below into a
different-family controller with repo access. Same-family defeats
de-correlation. Record the actual controller in the report's `reviewed_by`.

**Goal:** the shared `_hooklib.py` removes accidental helper drift across the
wired advisory hooks without changing any hook's observable gating behavior,
except the two intended changes (once-per-session prompt-preflight throttle;
repo-map full-read pre-gate). **Done looks like:** a reviewer attacking the
migration finds no path/scope/event input on which a migrated hook now stays
silent where it previously advised (or vice versa) beyond the two intended
changes, no way for a `_hooklib` defect to escalate an advisory hook into a
blocking failure, and every claimed selftest result reproduces. (Executor
target + axis to attack, not a review pass bar.)

---

# Adversarial Delegated Code Review-And-Patch: Hooks _hooklib Refactor

You are the de-correlated CONTROLLER under
`.agents/workflow-overlay/delegated-review-patch.md`
(`delegated_code_review_and_patch`, `access: repo`, base-subagent). Review and
patch directly in your working tree; do NOT commit; the commissioning Chief
Architect adjudicates every hunk before anything is kept.

## Preflight (verify before review)
- Repo: https://github.com/eric-foo/forseti ; branch
  `claude/code-hooks-optimization-2e26b3` (base `origin/main` @ `c33f5301`);
  expected head: the lane PR's current head, containing commits `47d3beb0`
  (settings indentation) and `876c068f` (the refactor) — clean tree required;
  mismatch => STOP with the blocker.
- `AGENTS.md` and `.agents/workflow-overlay/README.md` read: required first.
- Required reads next: `.agents/workflow-overlay/delegated-review-patch.md`;
  `.agents/hooks/README.md` (post-refactor state — the hooks table, the
  `_hooklib` porting note, and the guard standalone exception);
  `.agents/workflow-overlay/retrieval-metadata.md` (Applicability — the
  authority behind `_hooklib.DURABLE_DOC_PREFIXES`);
  `.agents/workflow-overlay/validation-gates.md` (Enforcement Placement).
- repo_map_decision: not_needed (targets exhaustive below). Source pack:
  bounded custom (the reads above plus the named diff). Edit permission:
  patch-only inside the named set. Dirty-state allowance: clean tree only;
  untracked files out of scope.
- Output mode: review-report; write the durable report at
  `docs/review-outputs/hooks_hooklib_refactor_delegated_adversarial_code_review_v0.md`
  with a valid retrieval header, non-blank `reviewed_by:` (your
  model+version), `authored_by: Anthropic Claude (Fable 5)`, and a
  `review_use_boundary:` stating findings are decision input and not approval,
  validation, readiness, mandatory remediation, or patch authority.
- Doctrine change: none authorized from this commission; flag doctrine defects,
  do not rewrite overlay files.
- External-source boundary: `jb`, external workflow source, and installed
  skills are not Forseti authority.

## Method (Source-Gated Method Contract)
1. REFERENCE-LOAD `workflow-deep-thinking` then `workflow-code-review`; do not
   APPLY yet.
2. SOURCE-LOAD: `git diff origin/main...HEAD`, every named file in full, the
   pre-refactor versions of the six migrated hooks
   (`git show origin/main:.agents/hooks/<file>` for each), and the required
   reads above.
3. Declare SOURCE_CONTEXT_READY, then APPLY.

## Patchable named file set (CANNOT widen; label every finding/hunk)
- [hooklib] `.agents/hooks/_hooklib.py`
- [retrieval-header] `.agents/hooks/check_retrieval_header.py`
- [full-gt] `.agents/hooks/check_full_gt_claims.py`
- [prompt-preflight] `.agents/hooks/check_prompt_provenance.py`
- [repo-map] `.agents/hooks/check_repo_map_freshness.py`
- [google-route] `.agents/hooks/check_search_surface_google_route.py`
- [shared-dirty] `.agents/hooks/check_shared_files_dirty.py`
- [sci] `.agents/hooks/remind_sci.py`
- [readme] `.agents/hooks/README.md`

Read-and-flag-only (NO patch): `.agents/hooks/guard_protected_actions.py`
(the standalone hard gate — its deliberate duplication of `_hooklib` helpers
is a documented exception, not a defect to "fix"), `.claude/settings.json`,
`.agents/hooks/header_index.py`, `.agents/hooks/check_review_output_provenance.py`,
`.agents/hooks/pre_push_guard.py`, every other checker,
`.agents/workflow-overlay/**`, `docs/**`, `forseti-harness/**`, and everything
else. Design-level problem => `NEEDS_ARCHITECTURE_PASS`, stop patching, revert
partials.

## Review emphasis (be maximally adversarial on material failure modes)
1. **Behavior-preservation of the helper unification.** The shared
   `to_relposix` returns `None` for empty, rooted-but-not-absolute (`/docs/...`
   on Windows), and outside-repo targets. Diff each migrated hook's OLD private
   variant against the shared one and hunt for an input class whose
   classification changed: [retrieval-header] and [sci] previously passed
   rooted strings through as out-of-scope text; [repo-map] previously fed them
   to `_area_of`. Prove each such change is silence-preserving (was no-advice,
   stays no-advice) or flag it.
2. **Event-parsing superset drift** [repo-map] [google-route]: the shared
   `candidate_paths` reads `file_path`/`path`/`notebook_path` plus patch
   headers in `command`/`patch`/`input`. [repo-map] previously read only
   `file_path` + `command`/`patch`. Can the widened key set make the repo-map
   hook fire (advise or exit-2 block) on an event where it previously stayed
   silent and should have? Check both Claude wiring (`Write|Edit|MultiEdit`)
   and the Codex adapter wiring (`apply_patch|Edit|Write`).
3. **The repo-map cheap-skip pre-gate.** `run_hook` now drops paths passing
   `is_excluded(rel, ())` (DEFAULT excludes only) before reading the map, and
   reads the map once only when a path survives. Attack: is there a path that
   the default excludes drop but that could have produced a structural trigger,
   `advisory_only` nudge, or commit interrupt under the old order? (Note the
   commit-interrupt branch runs before the skip.) Also confirm the map-derived
   `extra` exclusions still apply to surviving paths.
4. **The once-per-session throttle** [prompt-preflight]: state-file semantics
   (`_hooklib.mark_session_once` — tempdir marker, sha1-16 key). Attack: hash
   collisions across (name, session) pairs; marker persistence across `/clear`
   or OS temp cleanup mid-session; the no-session_id fail-open (must emit the
   FULL checklist, never throttle through the shared bucket); any error path
   that could suppress the reminder entirely rather than degrade to full.
5. **Import blast radius.** Every migrated hook does
   `sys.path.insert(0, <hooks dir>)` then imports `_hooklib` at module top. If
   `_hooklib` is broken (syntax error, missing file), each migrated hook dies
   at import with a nonzero exit BEFORE its fail-open `__main__` wrapper.
   Confirm no wiring treats that exit as blocking (PostToolUse exit 2 is the
   only block; import death is exit 1), that the repo-map commit interrupt
   (the one intended exit-2) cannot be produced spuriously by import failure,
   and that `sys.path.insert(0, ...)` cannot shadow a stdlib module used by
   any hook (audit the hooks directory's filenames).
6. **Consumer contract stability**: `header_index.py` and
   `check_review_output_provenance.py` import `check_relpath`/`scope_folder`
   from [retrieval-header] via `spec_from_file_location`; confirm the
   re-exported names and `IN_SCOPE_PREFIXES`/`EXCLUDED_PREFIXES` assignments
   keep their contract from any cwd. Confirm [full-gt]'s selftest monkeypatch
   of `globals()["_git"]` still exercises the production call path with the
   imported alias.
7. **Scope-vocabulary reconciliation truth**: `_hooklib.DURABLE_DOC_PREFIXES`
   must equal the retrieval-metadata Applicability list; [sci] adds
   `forseti/product/`; [google-route] deliberately keeps its own list with a
   delta comment. Verify each against the pre-refactor lists — no folder
   silently gained or lost coverage.
8. **Selftest fail-capability**: do the migrated selftests still exercise the
   SAME code paths production uses (not stale local copies), and can each
   still fail if `_hooklib` regresses?
9. **[readme] accuracy**: the hooks table rows, the wiring description, and
   the verify list must match the actual `.claude/settings.json` wiring and
   script behavior post-refactor.

## Validation obligations (run; report real results; never mask failures)
- All selftests green with any patch applied:
  `python .agents/hooks/_hooklib.py --selftest` and `--selftest` for
  `guard_protected_actions`, `check_retrieval_header`, `check_placement`,
  `check_full_gt_claims`, `check_prompt_provenance`, `check_repo_map_freshness`,
  `check_search_surface_google_route`, `check_shared_files_dirty`,
  `check_token_burn`, `remind_sci`, `pre_push_guard`,
  `check_review_output_provenance`, `header_index`.
- `python -m pytest forseti-harness/tests/unit/test_hook_internal_error_gating.py`
  — green with any patch.
- `python -c "import json; json.load(open('.claude/settings.json'))"` — parses.
- Live probes (delete artifacts / temp markers after): a synthetic
  PostToolUse event for a `docs/prompts/**` path piped twice with the same
  `session_id` must emit the full checklist then the short pointer, and a
  missing `session_id` must emit the full checklist; a synthetic event for a
  new top-level area must still produce the repo-map structural advisory; a
  synthetic event for `.claude/settings.json` must stay silent without a map
  read (verify via the code path, e.g. tracing or a temporary probe).
- The report itself must pass
  `python .agents/hooks/check_review_output_provenance.py --strict <report path>`.

## Return contract (findings-first)
Findings with severity `critical`/`major`/`minor` and `confidence`, `[label]`,
neutral decision-sufficient file:line citations, `minimum_closure_condition`,
`next_authorized_action`; unified uncommitted working-tree diff with
label-tagged hunks; one overall verdict + per-surface sub-verdicts where they
differ; residual-risk note (named: advisory hooks fail open by design, so a
`_hooklib` regression degrades to silence rather than blocking — silence is
the failure mode to bound; the throttle trades repeat-nudge coverage for
context tokens; the ~7 ms import cost is measured on one machine only);
explicit non-findings; `considered_and_defended` one-liners for
steelman-defeated candidates; no runtime-model recommendations; no
PASS/readiness claims. End with the adjudicator tail per
`.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next
Step (template:
`docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`).
