# Deletion-Evidence Doctrine v0 (Phase-2 deletion safety)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  The deletion-evidence contract for the Phase-2 bloat-cut fan-out: deleting a
  governed artifact carries a complete evidence record in the deletion-evidence
  register, and a STRICT CI gate (check_deletion_evidence.py) fails any PR that
  deletes a governed artifact without one. Substantive evidence review plus
  home/Chief Architect adjudication is a resident completion gate; provenance
  lives in git; the register holds only the evidence git cannot derive.
use_when:
  - Proposing or executing a deletion of a governed artifact (under GOVERNED_ROOTS).
  - Reviewing or adjudicating a deletion PR.
  - Modifying the register schema, GOVERNED_ROOTS, or check_deletion_evidence.py.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/deletion_evidence_register_v0.yaml
  - .agents/hooks/check_deletion_evidence.py
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - The register schema or GOVERNED_ROOTS changes (update this doctrine + the checker together).
  - The CI gate's enforcement placement (strict, pre-merge, in ci.yml) changes.
  - The router stops routing deleting PRs to manual review.
  - The completed-work self-merge or resident review/adjudication contract changes.
```

## Status

Decision record + contract. Establishes the deletion-evidence register and its
**strict CI gate**, ahead of the Phase-2 bloat-cut fan-out. **Non-claims:** not
validation, readiness, or proof; the gate enforces that evidence EXISTS and is
machine-consistent, not that the human judgment recorded in it is true.

## The rule

Deleting a **governed artifact** (one under `GOVERNED_ROOTS` in
`.agents/hooks/check_deletion_evidence.py`) requires a complete evidence record
in the register. A PR that deletes a governed artifact without one fails CI.

## What "deletion" means (detection contract)

A governed artifact is "deleted" when, in the PR's net diff (merge-base
`base...HEAD`, rename-aware), it is either removed (`D`) or **renamed out of
every governed root** (`R`, governed -> non-governed: it left its governed
home). A rename that keeps it under a governed root is a **move**, not a
deletion, and needs no record. Base resolution mirrors `header_index.py`
(`$GITHUB_BASE_REF` -> `origin/main`); there is no `HEAD~1` fallback (which would
see only the last commit of a multi-commit lane). The gate computes the diff with
a governed-root pathspec so non-governed review snapshots or archival copies
cannot steal rename pairing from a real governed successor; a true governed ->
non-governed rename still appears as deletion of the governed path under that
pathspec.

## The four evidence elements (all required, non-empty)

- **reverse_ref_check** — who/what still references the target; confirmed safe to remove. *(Judgment-bearing; read by the independent reviewer/adjudicator.)*
- **successor** — the replacing path, or the literal `none -- pure bloat`. *(Machine-checked: a named path must resolve in the tree.)*
- **semantic_delta** — what meaning is lost vs preserved by the deletion. *(Judgment-bearing.)*
- **rollback** — how to restore (e.g. `git revert <executing merge sha>`). *(Judgment-bearing.)*

## Adjudication, not a record lifecycle

There is **no `proposed -> executed` phase flip**. A git merge runs no code, so
nothing can transition a record; a phase nothing flips is a fiction. Instead:

- **Evidence** is the register record — present and complete, or the gate fails.
- **Adjudication** is the existing flow: the PR-risk router labels a deleting PR
  `risk/manual-review-required`, so the unattended bot will not land it. The
  evidence must receive independent substantive review plus home/Chief Architect
  adjudication before the completed lane author may self-merge. The plan's
  Phase-2 shape (a propose PR, then a separate execute PR — consolidation
  worksheet) is the "two phases", as two PRs, not two states of one record.
- **Provenance** (who merged, when, which commit) is recovered from git, its
  single authoritative home; it is not duplicated into the record.

## Why strict, in CI, pre-merge

Report-mode gives no safety: a green CI lets the in-session self-merge guard
(which merges a CLEAN + green + `agent-automerge` PR) land a deletion whose
evidence is missing or mechanically false. Only a **red check** closes that path;
a governed deletion with no complete record, or a successor that does not resolve
in the committed tree, turns CI red. The gate runs as a step in `ci.yml`'s
`orca-harness-tests` job (where the other strict gates run) — the green that
every merge path requires — so it holds regardless of which merge model is live
(self-merge, bot, human, or a future server gate), and regardless of whether
unattended auto-merge is removed. It is **born green**: with no governed
deletions in a diff it exits 0, so adopting strict matches the clean state with
no red-main event.

The gate fails **open** only on infrastructure gaps (no git, no PyYAML, base
unresolvable; PyYAML is pinned in CI so its absence is not an accidental gap). A
present-but-unparseable register, a governed deletion lacking a complete record,
or a successor that does not resolve are real findings. A **missing** register is
treated as empty (governed deletions then fail) — a deleted register cannot
un-govern the corpus.

## Presence vs truth, and resident adjudication

This gate enforces that evidence is **present and machine-consistent** — the
deleted governed path is covered by a complete record, and the declared successor
resolves to a committed file (or is the no-successor literal). It does **not**
verify that the judgment-bearing fields (`reverse_ref_check`, `semantic_delta`) are
**true**. That substantive review and home/Chief Architect adjudication is a
resident completion gate: it must close before the lane author self-merges. The
router's `risk/manual-review-required` label mechanically excludes the PR from
the unattended bot and signals the gate, but it neither certifies that judgment
occurred nor chooses a human merge actor. This is an explicit limitation: the
strict checker proves evidence presence and machine-consistency; the acting lane
must truthfully verify the independent review return and adjudication before
landing its own PR.

## What this does NOT cover (named boundaries)

- **Direct push to main.** This is a pre-merge PR gate. A direct push to main is
  not caught (on a push event the diff against `origin/main` is empty post-push,
  and CI runs after the push has landed). Direct-push-to-main is a separate
  control — `.githooks/pre-push` (`pre_push_guard.py`) and the protected-action
  guard both block it — but those are local / Claude-scoped and bypassable with
  `--no-verify`. A named residual, not closed here.
- **A PR that edits the gate itself.** Because CI runs the PR's own checker and
  workflow, a PR could in principle delete a governed file and neuter the gate in
  the same diff. Such a PR touches `.agents/` or `.github/`, which the router
  flags `risk/manual-review-required`, so unattended auto-merge remains blocked
  and independent review plus home/Chief Architect adjudication is required
  before author landing. That completion truth is resident rather than
  mechanically proven. A `pull_request_target` gate running **main's** checker
  against the PR, or another server-owned check immune to PR-side tampering,
  would close the residual further and is the next hardening if warranted.

## Emergency deletions

A strict gate must not become an availability deadlock. Until the
waiver-registry rail lands, an urgent governed deletion uses the owner's existing
override (`enforce_admins: false` — the owner can merge past a red check). The
waiver-registry rail will upgrade that ad-hoc override into a governed, audited
waiver record, so the emergency path itself stays evidence-bearing.

## Rejected frames (why this shape, not the alternatives)

- **Record phase state machine (`proposed/adjudicated/executed`)** — a merge runs
  no code; nothing flips the record. The lifecycle is two PRs, not two states.
- **Full in-record provenance (`deletion_id` / `proposed_by` / `adjudicator` /
  timestamps)** — self-typed provenance is forgeable and partly temporally
  impossible (the merger and merge SHA are unknown pre-merge). Git is
  provenance's authoritative home; duplicating it invites register-vs-git drift.
- **Report-mode now, strict in Phase-3** — report-mode leaves the self-merge path
  open during the exact phase deletions happen; it is no safety.
- **No gate (router + PR template only)** — routing a deletion to review does
  not guarantee a complete, machine-consistent record exists; the strict gate
  guarantees presence + machine facts (targets match the diff, successor
  resolves) so the adjudicator receives a well-formed record, not a checklist.
- **PreToolUse hook on the delete tool-call** — Claude-Code-scoped only (the bot
  and other harnesses are not guarded) and per-call (it cannot see the merged
  diff or a rename); the merge-time CI gate is harness-agnostic.
- **`governed_roots` declared in the register** — a data file must not own its own
  governance scope (it could narrow or delete it). `GOVERNED_ROOTS` is
  code-owned, in the checker, which the router protects as an `.agents/` surface.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The deletion-evidence strict gate now computes rename-aware deletion detection
    with a governed-root pathspec so non-governed review snapshots or archival
    copies cannot steal rename pairing from a real governed successor; the
    governed-deletion rule is unchanged.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/decisions/deletion_evidence_doctrine_v0.md
    - .agents/hooks/check_deletion_evidence.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/validation-gates.md
    - .github/workflows/ci.yml
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        It already names the deletion-evidence gate as protected friction and
        does not own checker implementation details.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        It owns validation bucket semantics; the strict gate command and
        gate-status meaning are unchanged.
    - path: .github/workflows/ci.yml
      reason: >
        CI still invokes the same strict checker command; only the checker's
        rename-pairing implementation changed.
  stale_language_search: >
    rg -n "rename-aware|governed-root|governed roots|review snapshot|check_deletion_evidence|deletion-evidence"
    docs/decisions/deletion_evidence_doctrine_v0.md .agents/hooks/check_deletion_evidence.py
    .agents/workflow-overlay/validation-gates.md .github/workflows/ci.yml AGENTS.md
  stale_language_search_result: >
    Executed 2026-06-21 during PR #316 CI repair. Hits either define the same
    governed deletion rule, point at the same strict checker, or document the new
    pathspec implementation detail; no checked surface requires repo-wide rename
    pairing for deletion-evidence detection.
  non_claims:
    - not validation
    - not readiness
    - not deletion approval
    - not a narrowed governed scope
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Governed deletions retain independent substantive review plus home/Chief
    Architect adjudication as a required completion gate, while the completed
    lane author remains the merge actor. The manual-review label mechanically
    excludes unattended auto-merge and signals the gate; it does not prove that
    judgment occurred or require a human merger.
  trigger: review_authority
  related_triggers:
    - workflow_authority
    - lifecycle_boundary
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/deletion_evidence_doctrine_v0.md
    - .agents/hooks/check_deletion_evidence.py
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .agents/hooks/guard_protected_actions.py
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/validation-gates.md
    - .github/workflows/pr-risk-router.yml
    - .github/workflows/auto-merge.yml
  intentionally_not_updated:
    - path: AGENTS.md and .agents/workflow-overlay/safety-rules.md
      reason: >
        Both already require completion of commissioned review and home/Chief
        Architect adjudication before own-PR self-merge.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        It already distinguishes mechanically checkable inputs from resident
        judgment and does not claim that a routing label certifies review.
    - path: .github/workflows/pr-risk-router.yml and .github/workflows/auto-merge.yml
      reason: >
        The router still sends deletions to manual review and the unattended bot
        still excludes that label; no workflow behavior changed.
  stale_language_search: >
    rg -n -i "human merger|human adjudicator|human merges|always reads the evidence|refuses (to )?self-merge.*manual|manual.*human merge"
    docs/decisions/deletion_evidence_doctrine_v0.md .agents/hooks/check_deletion_evidence.py
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md .agents/hooks/README.md
  stale_language_search_result: >
    Executed 2026-07-15. Remaining hits are this receipt's search terms and
    explicit statements that the manual-review label does not require a human
    merger; no live statement couples the label to human landing.
  non_claims:
    - not validation or readiness
    - not mechanical proof that independent review or adjudication completed
    - not unattended auto-merge authority for governed deletions
    - not authority to bypass a required owner hold
```

## Worked skeleton (illustrative)

```yaml
- targets: ["orca/product/spines/<area>/<superseded>_v0.md"]
  evidence:
    reverse_ref_check: "0 inbound refs after <successor> superseded it (grep docs/, .agents/, orca/)."
    successor: "orca/product/spines/<area>/<successor>_v2.md"
    semantic_delta: "No unique content lost; v0 is a strict subset of v2."
    rollback: "git revert <executing merge sha>"
```
