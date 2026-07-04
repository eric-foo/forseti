# Prompts

Store Forseti prompt artifacts here. Prompts should name their source files, expected output mode, and any hash or preflight gates they rely on.

`templates/` stores Forseti-local prompt templates. The authoritative template
registry is `.agents/workflow-overlay/template-registry.md`; template files are
subordinate to that registry and must not import `jb` project policy.

New or materially touched durable prompt artifacts should also include the
retrieval header defined in `.agents/workflow-overlay/retrieval-metadata.md`.
Use it to help future agents find the prompt and its next source, not to grant
authority, validation, readiness, or edit permission.
