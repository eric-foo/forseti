# Harness Test-Authoring Discipline v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: >
  Standing test-authoring discipline for forseti-harness/tests, derived from the
  2026-07-20 six-cluster test-stock audit. Governs the FORM of new tests and the
  MECHANISM cost they add, plus a loud-under-coverage convention for validator
  test files. It does not cap test count and installs no new CI gate.
use_when:
  - Adding, extending, or reviewing tests under forseti-harness/tests.
  - Deciding whether a new test belongs as a sibling file or a parametrized row.
  - Adding a test that spawns a subprocess or materializes a heavyweight fixture.
  - Authoring or reviewing tests for a rule/finding-code validator.
authority_boundary: retrieval_only
open_next:
  - forseti-harness/README.md
  - .agents/workflow-overlay/validation-gates.md
stale_if:
  - A roster-completeness CI gate for validator finding-codes is later adopted (fold the deferred candidate below into it).
  - The suite's runner defaults (-n auto --dist=loadfile) change.
```

## Status

Accepted 2026-07-20, owner-directed (eric-foo: "write the binding doc"), on the
evidence of the six-cluster test-stock audit landed with the harness-suite-latency
lane (PR #1184). This is behavioral discipline, not a mechanically enforced gate.

## Why this exists (the audit finding)

The audit full-read 1,967 of 3,978 tests across the six highest-redundancy-likelihood
clusters and adversarially verified every load-bearing claim. The stock is
**~99.7% legitimate**: clean-cut candidates were ~0.3%, and 3 of 4 proposed
deletions were rejected on full-read because the "superset" tests also pinned
distinct facts. A count ceiling would therefore have been the wrong rule.

The real, compounding defect classes are three, and each traces to independent
agent threads copying the *shape* of an existing test without seeing the others:

1. **Copy-paste shape proliferation.** Per-family test files diverged until
   coverage went *asymmetric* — e.g. basenotes/parfumo cleaning-catchup each
   tested only one foreign surface; the retail pre-capture exclusion covered 5 of
   15 flag pairs by accident of which file picked which partner. The redundancy
   was a maintenance surface, and the copies hid gaps.
2. **Mechanism cost.** The same expensive pattern was copied at scale: 48
   subprocess hook-spawns, a 677KB seed fixture materialized (226 file-writes,
   ~1.05s) at 7 call sites, a full-repo AST census re-run ~5×. This is what made
   the serial suite 9 minutes; none of it was coverage.
3. **Silent under-coverage in validators.** The commission-signal-board validator
   had 84 of 128 finding codes with no test; the CSB validator 21 of 58. In a repo
   where tests are the only reviewer, under-coverage is the live risk, and it
   accumulates invisibly.

## The discipline

Four rules. Each is subordinate to the Smallest Complete Intervention and
Behavioral Admission doctrines: prefer the lower-ceremony path, and do not add a
standing mechanism unless it catches a named defect at the lowest-cost boundary.

1. **Extend the table, not the file.** When a per-family/per-site/per-retailer
   parametrized test already exists for a behavior, add the new case as a row in
   that table (or convert the first sibling into one). Do not add a new sibling
   test file that re-proves the shared behavior with one literal swapped — that is
   where the asymmetric-coverage gaps came from. A genuinely different pipeline,
   error taxonomy, or architecture still earns its own file (the audit kept those).

2. **Hook and checker tests default in-process.** A test of a hook/checker's
   exit-code or stderr contract runs it via `runpy.run_path(..., run_name="__main__")`
   with patched `sys.argv` (pattern: `test_session_capsule_gather.py`), not a
   `subprocess.run([sys.executable, ...])` spawn. Keep a real subprocess only when
   the *entrypoint itself* is under test — a hard process crash, real OS file-lock
   contention, PATH/shebang wiring — and say so in the test.

3. **Scope heavyweight fixtures at creation.** A fixture that parses a large file
   or writes many records exposes a way to materialize only what the caller
   asserts on (e.g. `limit_to_platform_account_ids`), or is built once and
   shared/deep-copied (module- or session-scoped). A test that asserts counts,
   exclusions, or a census over the whole input keeps the full fixture and says
   why. Never let a caller that checks one account pay to build thirty.

4. **Validator test files carry a roster check.** A test file for a validator that
   emits a closed set of finding-codes (or enforces a closed field/flag set)
   includes one assertion that every declared code/flag has at least one covering
   test — so a new code added without a test fails loudly instead of joining the
   silent-gap backlog. Import the source's constant; never re-list it by hand.

## Deferred, deliberately not built here

A CI gate that mechanically enforces rule 4 (cross-reference each validator's
finding-code roster against its test file) is a plausible future checker but is
**not** built by this record. Per Behavioral Admission, the standing per-PR cost
of another checker is not yet justified against the discipline above: the named
gaps are known and fixable in-place, and a resident convention catches the class
at author time. Adopt the gate only if the backlog reappears after this discipline
is live; if adopted, fold this record's `stale_if` into it.

## Non-claims

- Not a test-count target, budget, or ceiling. The audit lane *added* 21 net
  tests (gap-closers > cuts) while cutting wall-clock; count was never the metric.
- Not validation, readiness, or approval of any test or of the suite.
- Not a new CI gate and not an edit to any existing gate; the roster-check rule is
  resident authoring discipline until and unless the deferred gate above is
  separately adopted.
- The audit covered 49% of the suite (the highest-likelihood clusters); this
  record asserts nothing about the unaudited remainder.
```yaml
direction_change_propagation:
  doctrine_changed: >
    Establishes new standing test-authoring discipline for forseti-harness/tests
    (form over count, in-process hook probes, scoped heavyweight fixtures,
    validator roster checks). Net-new decision record; changes no prior doctrine.
  trigger: workflow_authority
  controlling_sources_updated:
    - docs/decisions/harness_test_authoring_discipline_v0.md
    - forseti-harness/README.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        No gate is added or changed; this record is resident discipline, so the
        validation-gates surface has nothing mechanical to bind. It stays the
        pointer target via open_next.
    - path: docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
      reason: >
        CI contract (single target, no test-selection reduction, full suite
        required) is unchanged; this discipline governs test authoring, not CI.
  non_claims:
    - not validation or readiness
    - not a CI gate or a change to any gate
    - not a test-count policy
```
