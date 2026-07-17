---
name: slop-audit
description: "Route an explicitly commissioned Forseti code-slop hygiene audit to the few sources needed for its bound failure. Do not trigger for a single obvious inline dedup, generic code review (use workflow-code-review), artifact/prose review, or feature/runtime work."
---

# slop-audit (Forseti-local candidate source)

## Boundary

This candidate is a discovery router, not Forseti authority, validation,
readiness, acceptance, or a mandatory playbook. Current project facts come only
from `AGENTS.md`, `.agents/workflow-overlay/`, and the owning sources below. If
a pointer is stale, resolve the current owner; do not reconstruct its rule here.

## Failure and trigger

Use this router when an explicit code-slop audit (duplication, bloat, ceremony,
or drift) would otherwise require a cold agent to rediscover the relevant
Forseti sources. Do not invoke it for a single obvious inline dedup, generic
implementation review, non-code artifact review, or feature/runtime work.

## Route

Apply only the stops needed by the bound task:

1. Bind the concrete failure and code surface before widening the audit.
2. For shared-helper duplication, read the adoption-rule paragraph and its
   mechanical backstop in the relevant package:
   `.agents/hooks/README.md` plus
   `.agents/hooks/check_shared_helper_duplication.py`, or
   `forseti-harness/README.md` plus the same checker.
3. For removal or completeness claims, read the CSB reversal in
   `docs/hygiene/hooks_smallest_complete_audit_ledger_v0.md` and the decision
   record in `docs/hygiene/slop_audit_skill_scoping_v0.md`. They are evidence and
   adjudication input, not standing authority.
4. Apply `AGENTS.md` Smallest Complete Intervention to every proposed addition
   and subtraction.
5. Route implementation review through `workflow-code-review`. Use
   `workflow-delegated-review-patch` only when a separate commission grants that
   lane and its bounded patch authority.

This skill is Forseti-local candidate source only. It is not deployed, mirrored,
accepted, or frozen; `.agents/workflow-overlay/skill-adoption.md` owns those
states.
