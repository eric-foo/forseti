# Deletion-Evidence Doctrine v0 (Phase-2 deletion safety)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  The deletion-evidence contract for the Phase-2 bloat-cut fan-out: deleting a
  governed artifact carries a complete evidence record in the deletion-evidence
  register, and a STRICT CI gate (check_deletion_evidence.py) fails any PR that
  deletes a governed artifact without one. Adjudication is the existing
  router->human-merge flow; provenance lives in git; the register holds only the
  evidence git cannot derive.
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
see only the last commit of a multi-commit lane).

## The four evidence elements (all required, non-empty)

- **reverse_ref_check** — who/what still references the target; confirmed safe to remove. *(Human-judged; read by the adjudicator.)*
- **successor** — the replacing path, or the literal `none -- pure bloat`. *(Machine-checked: a named path must resolve in the tree.)*
- **semantic_delta** — what meaning is lost vs preserved by the deletion. *(Human-judged.)*
- **rollback** — how to restore (e.g. `git revert <executing merge sha>`). *(Human-judged.)*

## Adjudication, not a record lifecycle

There is **no `proposed -> executed` phase flip**. A git merge runs no code, so
nothing can transition a record; a phase nothing flips is a fiction. Instead:

- **Evidence** is the register record — present and complete, or the gate fails.
- **Adjudication** is the existing flow: the PR-risk router labels a deleting PR
  `risk/manual-review-required`, so the unattended bot will not land it and a
  human merges it. The plan's Phase-2 shape (a propose PR, then a separate
  execute PR — consolidation worksheet) is the "two phases", as two PRs, not two
  states of one record.
- **Provenance** (who merged, when, which commit) is recovered from git, its
  single authoritative home; it is not duplicated into the record.

## Why strict, in CI, pre-merge

Report-mode gives no safety: a green CI lets the in-session self-merge guard
(CLEAN + green + `agent-automerge`, which does not read the router's risk label)
land an unevidenced deletion. Only a **red check** closes that path; the bot
path is already closed by the router. The gate runs as a step in `ci.yml`'s
`orca-harness-tests` job (where the other strict gates run) — the green that
every merge path requires — so it holds regardless of which merge model is live
(self-merge, bot, human, or a future server gate), and regardless of whether
unattended auto-merge is removed. It is **born green**: with no governed
deletions in a diff it exits 0, so adopting strict matches the clean state with
no red-main event.

The gate fails **open** only on infrastructure gaps (no git, no PyYAML, base
unresolvable). A present-but-unparseable register, a governed deletion lacking a
complete record, or a successor that does not resolve are real findings. A
**missing** register is treated as empty (governed deletions then fail) — a
deleted register cannot un-govern the corpus.

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
- **No gate (router + PR template only)** — the self-merge guard ignores the
  router label, so a green deletion can self-merge unevidenced.
- **PreToolUse hook on the delete tool-call** — Claude-Code-scoped only (the bot
  and other harnesses are not guarded) and per-call (it cannot see the merged
  diff or a rename); the merge-time CI gate is harness-agnostic.
- **`governed_roots` declared in the register** — a data file must not own its own
  governance scope (it could narrow or delete it). `GOVERNED_ROOTS` is
  code-owned, in the checker, which the router protects as an `.agents/` surface.

## Worked skeleton (illustrative)

```yaml
- targets: ["orca/product/spines/<area>/<superseded>_v0.md"]
  evidence:
    reverse_ref_check: "0 inbound refs after <successor> superseded it (grep docs/, .agents/, orca/)."
    successor: "orca/product/spines/<area>/<successor>_v2.md"
    semantic_delta: "No unique content lost; v0 is a strict subset of v2."
    rollback: "git revert <executing merge sha>"
```
