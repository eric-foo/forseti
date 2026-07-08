# Prompts

```yaml
retrieval_header_version: 1
artifact_role: Prompt folder guide
scope: Prompt artifact folder navigation, accepted prompt families, and retained prompt-location exceptions.
use_when:
  - Deciding where to file a Forseti prompt artifact.
  - Checking whether a nonstandard prompt location is retained for provenance.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/prompt-orchestration.md
```

Store Forseti prompt artifacts here. Prompts should name their source files, expected output mode, and any hash or preflight gates they rely on.

`templates/` stores Forseti-local prompt templates. The authoritative template
registry is `.agents/workflow-overlay/template-registry.md`; template files are
subordinate to that registry and must not import `jb` project policy.

New or materially touched durable prompt artifacts should also include the
retrieval header defined in `.agents/workflow-overlay/retrieval-metadata.md`.
Use it to help future agents find the prompt and its next source, not to grant
authority, validation, readiness, or edit permission.

## Accepted Families

Accepted prompt-family folders are bound by
`.agents/workflow-overlay/artifact-folders.md` and
`.agents/workflow-overlay/prompt-orchestration.md`:

- `product-planning/`
- `feature-planning/`
- `deep-thinking/`
- `handoffs/`
- `reviews/`
- `reruns/`
- `patches/`
- `wrappers/`
- `templates/`

Use these for new prompt artifacts unless the owning overlay or a later owner
decision creates a narrower destination.

## Retained Exceptions

These locations are retained for navigation and provenance. They are not
accepted prompt-family folders and should not receive new prompt artifacts by
default.

| Location | Why retained | Move boundary |
| --- | --- | --- |
| `architecture/` | Nonstandard architecture-prompt bucket with live references and review provenance. | Needs reverse-ref proof and owner decision before any promotion or move. |
| `advisory/` | Daimler advisory prompt exception retained by ORCA-HYGIENE-005; path/hash-pinned in downstream records. | Do not move without a reference-aware pass. |
| root `*.md` prompt files | Data Capture / Judgment prompt exceptions and pinned checker prompts retained at the root. | New prompts should use an accepted family; root prompt triage needs reverse-ref proof. |
| `../research/judgment-spine/harness/v0_14/review_prompts/` | Review prompts bundled with the v0.14 harness spec rather than this prompt tree. | Keep with the spec unless a later owner decision repoints the bundle. |

`hygiene-queue/` is a dead prompt path: ORCA-HYGIENE-001 consolidated it to
`docs/hygiene/` and removed the directory. Do not recreate it as a prompt
family.

Review outputs have their own retained-root exception documented in
`docs/review-outputs/README.md`; new adversarial reports default to
`docs/review-outputs/adversarial-artifact-reviews/`.
