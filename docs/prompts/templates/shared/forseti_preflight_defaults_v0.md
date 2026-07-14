# Forseti Preflight Defaults v0

```yaml
retrieval_header_version: 1
artifact_role: Preflight defaults (repo-constant prompt preflight bindings)
scope: >
  Repo-constant field values that escalated Forseti prompts may reference
  rather than restate. Routine prompts use the inline preflight core instead;
  the `environment_baseline` constant may be pointed at by any Forseti prompt,
  including compact delegated prompts.
use_when:
  - Authoring a prompt that matches the Full orchestration predicate in `.agents/workflow-overlay/prompt-orchestration.md`; not a lane-scoped prompt merely because it is delegated or patch-authorized.
  - Checking which escalated preflight fields are constant vs. per-prompt.
  - Resolving the `environment_baseline` constant pointed at by any Forseti prompt.
authority_boundary: retrieval_only
```

Usage line an escalated prompt may include:

```
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
```

---

## CONSTANTS bound by this artifact (verbatim, single source)

These values do not need restating when an escalated prompt cites this artifact.

| Field | Value |
| --- | --- |
| `agents_md_read` | Required on intake |
| `overlay_readme_read` | `.agents/workflow-overlay/README.md` — required on intake |
| `external_source_boundary` | External workflow source is read-only from Forseti work; `jb` is not Forseti authority |
| `retrieval_header_version` | `1` (for new durable artifacts) |
| `authority_boundary` | `retrieval_only` (for new durable artifacts) |
| `environment_baseline` | Windows host, PowerShell-first: use PowerShell syntax for shell/test commands; use absolute paths resolvable from any cwd; invoke `python`, never `python3`; do not pass Windows drive-letter paths or heredocs through bash |

The REFERENCE-LOAD / SOURCE-LOAD / SOURCE_CONTEXT_READY / APPLY gate language
is owned by `.agents/workflow-overlay/prompt-orchestration.md`'s
Source-Gated Method Contract (pointer, not restatement here).

---

## REQUIRED ESCALATED DELTAS

An escalated prompt referencing this artifact still states the material deltas
below. Routine prompts do not inherit this list.

- **workspace_or_repo**: commissioned target worktree root or repository
  identifier when repository state matters; never default to an unrelated
  parent/launch checkout. Repo-bound review mismatch handling is owned by
  `.agents/workflow-overlay/prompt-orchestration.md` -> "Repo-Bound Review
  Target Resolution".
- **receiver_target_resolution**: for repo-changing cross-lane work, record the
  receiver mechanism, `launch_checkout`, `effective_target_worktree`, resolution
  method, direct write-capability proof, and no-concurrent-writer status. Dirty
  work also records its allowed dirty-file set plus a target manifest or
  equivalent byte identity. Receiver-only observations in an
  operator-couriered prompt may be `operator_to_fill`, but must be completed
  before source loading.

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
- **branch_or_commit_reference**: expected branch plus either an exact detached
  revision/hash pin or required commit ancestry when source stability matters;
  state which semantics apply.
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
