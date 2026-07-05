---
name: orca-product-lead
description: "Legacy compatibility alias for the Forseti product-lead skill. Use when old prompts, docs, or invocations mention /orca-product-lead; load the sibling forseti-product-lead skill and follow it."
---

# orca-product-lead (legacy compatibility alias)

This is a transition wrapper for the renamed Forseti-local product-lead skill.
It preserves the old `/orca-product-lead` invocation for historical prompts and
operators during the compatibility window.

## Required behavior

- Load and follow the sibling `forseti-product-lead` skill in the same skill
  root: `../forseti-product-lead/SKILL.md`.
- Treat `forseti-product-lead` as the primary skill identity and this file as an
  alias only.
- Do not duplicate product-lead doctrine here; the primary skill and Forseti
  authority sources own the method.
- Defer all Forseti facts, folders, validation gates, artifact roles, output
  contracts, and non-claims to `AGENTS.md`, `.agents/workflow-overlay/`, and the
  primary `forseti-product-lead` skill.
- If the sibling primary skill is missing, fail visibly and report the missing
  path instead of continuing from stale alias behavior.

## Boundary

This wrapper is Forseti-local and project-scoped. It is not plugin, user-level,
installed, or external skill source; it carries no Forseti authority and does
not prove resolver activation. Rollback is governed by
`.agents/workflow-overlay/skill-adoption.md`.