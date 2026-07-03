# Forseti Preflight Defaults v0

```yaml
retrieval_header_version: 1
artifact_role: Preflight defaults (repo-constant prompt preflight bindings)
scope: >
  Repo-constant preflight field values that every Forseti repo-aware prompt may
  reference rather than restate. Does not remove the requirement to state
  per-prompt deltas.
use_when:
  - Authoring a new Forseti repo-aware prompt and referencing constant fields.
  - Checking which preflight fields are repo-constant vs. per-prompt required.
authority_boundary: retrieval_only
```

Usage line a prompt includes:

```
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 — constants bound; deltas stated below.
```

---

## CONSTANTS bound by this artifact (verbatim, single source)

These values are repo-constant and do not need restating per prompt when a
prompt cites this artifact.

| Field | Value |
| --- | --- |
| `workspace_path` | `C:\Users\vmon7\Desktop\projects\orca` |
| `agents_md_read` | Required on intake |
| `overlay_readme_read` | `.agents/workflow-overlay/README.md` — required on intake |
| `external_source_boundary` | External workflow source is read-only from Forseti work; `jb` is not Forseti authority |
| `retrieval_header_version` | `1` (for new durable artifacts) |
| `authority_boundary` | `retrieval_only` (for new durable artifacts) |

The REFERENCE-LOAD / SOURCE-LOAD / SOURCE_CONTEXT_READY / APPLY gate language
is owned by `.agents/workflow-overlay/prompt-orchestration.md`'s
Source-Gated Method Contract (pointer, not restatement here).

---

## REQUIRED PER-PROMPT DELTAS

A prompt referencing this artifact MUST still state each of the following. They
are never defaulted by this artifact.

- **authorization_basis**: what authorizes this unit of work (current turn,
  accepted handoff, owner decision, etc.).
- **objective / intended_decision**: the specific goal and the decision this
  work unit must produce or inform.
- **target_files_or_dirs**: concrete file or directory paths in scope.
- **source_pack / bounded_reads**: selected source pack from
  `.agents/workflow-overlay/source-loading.md`, or a named bounded custom
  source pack.
- **output_mode**: exactly one of `chat-only`, `file-write`, `review-report`,
  `paste-ready-chat`, or `patch-queue`.
- **edit_permission**: `read-only`, `patch-only`, or `docs-write`.
- **dirty_state_allowance**: whether modified or untracked files are in scope.
- **controlling_source_state**: when strict claims depend on overlay,
  source-loading, repo-map, prompt-policy, validation, or artifact-role files —
  clean, modified, untracked, stale, or not checked.
- **branch_or_commit_reference**: expected branch, detached revision, or commit
  hash when source stability matters.
- **doctrine_change_decision**: whether this work changes product doctrine,
  architecture doctrine, workflow authority, validation philosophy, review
  authority, output authority, or a lifecycle boundary; if yes, which
  propagation surfaces must be checked before closeout.
- **isolation_decision**: worktree off main, branch off main, or neither
  (read-only work), with one-line rationale.
- **validation_gates**: required validation gates and where evidence is
  recorded.
- **thread_operating_target_continuity**: when the prompt continues the same
  workstream with a visible active `thread_operating_target`, whether it is
  carried forward verbatim with continuity disclosure or explicitly omitted
  with reason.
