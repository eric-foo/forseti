# Forseti Efficiency Front Doors - Adversarial Implementation Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Source-read-only adversarial implementation/code review of the Forseti
  efficiency front-door and package-guard change packet pinned to commit
  928b3c3642c95e88db5ae312e1fae7f371f2aa52.
use_when:
  - Dispatching an independent implementation/code review of the efficiency 3/4 branch before merge or follow-on patching.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
branch_or_commit: codex/forseti-efficiency-3-4-impl target commit 928b3c3642c95e88db5ae312e1fae7f371f2aa52; base bc8d5f715023d33b5f985e59dd7d379dd8ad26cb
stale_if:
  - The target commit or base commit is unavailable in the receiving worktree.
  - The review is widened to branch HEAD after this prompt artifact is added.
```

## Commission

Run a source-read-only adversarial implementation/code review of the Forseti
efficiency front-door and package-guard change packet:

```text
base:   bc8d5f715023d33b5f985e59dd7d379dd8ad26cb
target: 928b3c3642c95e88db5ae312e1fae7f371f2aa52
range:  bc8d5f715023d33b5f985e59dd7d379dd8ad26cb..928b3c3642c95e88db5ae312e1fae7f371f2aa52
```

The author/home model family is OpenAI/Codex. If this is dispatched to satisfy a
cross-vendor discovery bar, the reviewing controller must be from a different
upstream vendor or model lineage. This is a who-constraint and measurement field,
not a runtime model recommendation. If the runtime is same-vendor, proceed only
as bounded sanity review and record that `cross_vendor_discovery` was not met.

## Route Decision

This request came through the delegated-review-patch route, but the target is a
multi-file implementation/code change packet, not a single high-stakes authored
artifact. Per `.agents/workflow-overlay/delegated-review-patch.md`, do not stretch
the delegated review-and-patch convention to fit it. Route the review through the
implementation/code review lane. Patch execution is not bound by this prompt.

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
v0 - repo constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: read-only
  target_scope:
    - docs/research/README.md
    - docs/research/answer_engine/README.md
    - docs/workflows/forseti_repo_map_v0.md
    - forseti/product/README.md
    - forseti/product/spines/creator_signal/README.md
    - forseti/product/spines/foundation/ontology/README.md
    - orca-harness/pyproject.toml
    - orca-harness/tests/contract/test_packaging_imports.py
    - orca/product/spines/capture/README.md
    - orca/product/spines/judgment/README.md
  dirty_state_checked: required_yes
  blocked_if_missing: yes

authorization_basis: current owner request to run delegated review/patch routing for the completed efficiency 3/4 branch.
objective: find bugs, regressions, overclaims, route drift, or efficiency defects in the pinned change packet before merge or follow-on patching.
intended_decision: whether the change can proceed to CA adjudication as-is, needs a bounded patch authorization, or needs architecture/routing correction.
output_mode: review-report
review_report_path: docs/review-outputs/forseti_efficiency_front_doors_adversarial_implementation_review_v0.md
edit_permission: read-only
patch_execution_authority: unbound; no source edits and no patch_queue_entry
dirty_state_allowance: review the exact target commit/range; if current worktree differs, use git to inspect the pinned range and report the drift
branch_or_commit_reference: codex/forseti-efficiency-3-4-impl target 928b3c3642c95e88db5ae312e1fae7f371f2aa52
doctrine_change_decision: no new doctrine change is authorized by this review prompt; flag any doctrine implications instead of patching them
isolation_decision: read-only review; no branch or worktree edits by the reviewer
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
```

## Cynefin Routing

Smallest complete outcome: a findings-first implementation/code review report
for the pinned diff, with closure conditions and no source edits.

Regime: Complicated.

Why: The target is bounded and source-visible, but correctness depends on repo
navigation doctrine, package configuration, and validation evidence.

Decomposition: Layer-based - verify package guard, route/front-door correctness,
identity/legacy-root boundaries, validation evidence, then blast radius.

Current bottleneck: Whether the new front doors and package guard actually make
navigation and packaging safer without creating new stale routes or false
confidence.

Riskiest assumption: The new README/front-door paths are only navigational and
do not accidentally promote research, legacy roots, or compatibility packages
into stronger authority.

Stop or pivot condition: If the diff cannot be inspected at the pinned target,
or if a fix requires changing off-scope workflow doctrine, return `BLOCKED` or
`NEEDS_ARCHITECTURE_PASS` rather than reviewing a substitute source.

Allowed next move: review the pinned diff and write the report.

Disallowed next move: edit source files, retarget to branch HEAD, review old
prompts/reviews for cleanup, or create an executor-ready patch queue.

## Required Method Sequence

1. Read this prompt.
2. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/review-lanes.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`, and
   `.agents/workflow-overlay/delegated-review-patch.md`.
4. REFERENCE-LOAD `workflow-deep-thinking`.
5. REFERENCE-LOAD `workflow-code-review`.
6. Do not APPLY either method yet.
7. SOURCE-LOAD the pinned diff and target files listed below.
8. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
9. APPLY deep-thinking to frame highest-risk failure modes.
10. APPLY workflow-code-review to produce findings.
11. Write the review report to the output path before returning a chat summary.

If `workflow-code-review` is unavailable or not applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`
or advisory-only findings. Do not emit strict review claims.

## Review Target

Review exactly this committed change packet:

```powershell
git diff --stat bc8d5f715023d33b5f985e59dd7d379dd8ad26cb..928b3c3642c95e88db5ae312e1fae7f371f2aa52
git diff --name-only bc8d5f715023d33b5f985e59dd7d379dd8ad26cb..928b3c3642c95e88db5ae312e1fae7f371f2aa52
git diff bc8d5f715023d33b5f985e59dd7d379dd8ad26cb..928b3c3642c95e88db5ae312e1fae7f371f2aa52 -- <target paths>
```

Target files:

- `docs/research/README.md`
- `docs/research/answer_engine/README.md`
- `docs/workflows/forseti_repo_map_v0.md`
- `forseti/product/README.md`
- `forseti/product/spines/creator_signal/README.md`
- `forseti/product/spines/foundation/ontology/README.md`
- `orca-harness/pyproject.toml`
- `orca-harness/tests/contract/test_packaging_imports.py`
- `orca/product/spines/capture/README.md`
- `orca/product/spines/judgment/README.md`

Read-only context may include:

- `AGENTS.md`
- `.agents/workflow-overlay/*` files named in this prompt
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- adjacent `README.md` files only when needed to confirm route boundaries
- `orca-harness/evidence_binding/__init__.py`
- `orca-harness/reports/__init__.py`
- `orca-harness/signal_content/__init__.py`

Do not review or clean up previous prompts, previous reviews, stale review
outputs, or historical prompt artifacts. If one is load-bearing to a finding,
cite only the specific line and explain why it changes this target review.

## Observed Implementation Context

The change packet claims to:

- add retrieval-only front doors for Creator Signal, Foundation ontology,
  Judgment, Capture, and Answer Engine research;
- update the Forseti repo map, Forseti product front door, and research front
  door to route through those entries;
- keep `orca/product/` and `orca-harness/` as intentional legacy compatibility
  roots rather than inventing `forseti-harness/`;
- add `evidence_binding`, `reports`, and `signal_content` to
  `orca-harness/pyproject.toml` package discovery;
- add a dependency-free package configuration guard at
  `orca-harness/tests/contract/test_packaging_imports.py`.

Validation reported by the implementer before this prompt:

```text
python -m pytest -p no:cacheprovider -q tests\contract\test_packaging_imports.py tests\unit\test_evidence_binding.py tests\unit\test_signal_content_models.py
39 passed

check_retrieval_header.py --changed: exit 0
check_repo_map_freshness.py --changed: exit 0
git diff --check: exit 0
route Test-Path sweep for new/edited open_next entries: all True
```

Treat this validation as context to inspect, not proof to inherit.

## Attack Questions

Find material bugs, false-success paths, authority drift, or bloat. Focus on:

1. Package guard correctness: does the test actually fail if a required package
   is omitted from `pyproject.toml`, and does it verify the intended package roots
   without relying on installation side effects?
2. Package discovery blast radius: does adding `evidence_binding`, `reports`, and
   `signal_content` to setuptools include only the intended import packages, or
   could it package reports/test artifacts unintentionally?
3. Route correctness: do every new and edited `open_next` or path references
   resolve at the pinned commit, and do they point to the narrowest useful front
   door rather than duplicating doctrine?
4. Identity boundary: do the Forseti front doors make Forseti the front-door
   identity while preserving `orca/product/` and `orca-harness/` only as explicit
   legacy compatibility roots?
5. Legacy-root overclaim: does any new text imply `orca/product/` or
   `orca-harness/` is deprecated, renamed, validated, or ready beyond the actual
   compatibility statement?
6. Research boundary: does `docs/research/answer_engine/README.md` stay research
   and evidence-routing only, without promoting research notes into product
   authority or proof?
7. Navigation efficiency: do the new front doors reduce cold-lane search and
   bloat, or do they create another layer of mostly duplicate navigation text?
8. Stale or impossible route: does any new path reference non-existent files,
   old `docs/product/` lanes, fake `forseti-harness/`, or stale Aphrodite D-1
   targets?
9. Review/use boundary: do the new docs avoid claiming validation, readiness,
   acceptance, source-of-truth promotion, deployment, resolver behavior, or
   merge state?
10. Validation sufficiency: are the reported checks the right minimum for the
    change, or is there a missing cheap check that would catch a realistic
    regression inside the target scope?

## Output Contract

Write the durable review report to:

`docs/review-outputs/forseti_efficiency_front_doors_adversarial_implementation_review_v0.md`

Start with:

```yaml
review_summary:
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  reviewed_by: operator_to_fill_or_unrecorded
  authored_by: OpenAI/Codex
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
  same_vendor_rationale: required_if_same_vendor_sanity
  target_range: bc8d5f715023d33b5f985e59dd7d379dd8ad26cb..928b3c3642c95e88db5ae312e1fae7f371f2aa52
  report_path: docs/review-outputs/forseti_efficiency_front_doors_adversarial_implementation_review_v0.md
```

Then list findings first, ordered by severity. For each finding include:

- id
- severity: `critical`, `major`, or `minor`
- affected file and line
- evidence with `file:line`
- risk
- minimum_closure_condition
- next_authorized_action

Then include:

- non-findings / seams that held
- validation evidence inspected and validation gaps
- residual risk
- verdict: `ACCEPTABLE_FOR_CA_ADJUDICATION`, `PATCH_BEFORE_CA_ADJUDICATION`,
  `NEEDS_ARCHITECTURE_PASS`, or `BLOCKED`

No `patch_queue_entry`, no source edits, no commits, no pushes, and no
executor-ready how-to. Advisory remediation direction is allowed when needed.

## Review-Use Boundary

Findings are decision input for the CA/owner only. They are not approval,
validation, readiness, mandatory remediation, patch authority, merge authority,
or proof that the branch should land. The CA adjudicates any returned findings
or recommended changes before anything is kept.
