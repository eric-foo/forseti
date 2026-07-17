# Slop-Audit Candidate — Wave-5 Decision Record v0

```yaml
retrieval_header_version: 1
artifact_role: hygiene scoping decision record (owner adjudication input)
scope: >
  Records why wave 5 retains a discovery-only slop-audit candidate, where the
  exemplar-repair hypothesis lives, and which lessons remain evidence or
  pointers rather than standing rules.
use_when:
  - Re-evaluating whether the slop-audit candidate earns its keep.
  - Adjudicating the wave-5 candidate and README-cell scope.
authority_boundary: retrieval_only
branch_or_commit: wave5 lane off origin/main a965cf67 (measured 2026-07-17)
stale_if: >
  The candidate, adoption records, README cells, hooks-audit ledger, or SCI
  kernel change after 2026-07-17; re-read the current owners.
open_next:
  - .agents/skills/slop-audit/SKILL.md
  - .agents/workflow-overlay/skill-adoption.md
  - AGENTS.md
```

Source commission: `docs/prompts/handoffs/slop_audit_skill_authoring_wave5_handoff_v0.md` on branch `claude/wave5-skill-handoff` (not in this tree).
Decision criterion: `AGENTS.md` Smallest Complete Intervention, including
artifact-level distinct-consumer and recurring-toll tests.

**Non-claims.** This is a scoping decision plus resident judgment, not
validation, readiness, or acceptance. It authorizes no deployment and installs
no standing rule. The candidate remains owner-authorized but not accepted,
frozen, deployed, mirrored, activated, or resolver-proven.

## Bound outcome and decision

The bound outcome is a discoverable entry point for a cold agent conducting an
explicit code-slop audit, without installing a second home for project rules.
The smallest complete form is:

- Retain `.agents/skills/slop-audit/SKILL.md` only as a narrow discovery router.
- Keep the exemplar-repair hypothesis at the two existing package adoption
  paragraphs, where hooks and harness contributors already enter.
- Keep this file only as the adjudication record. It is not a cold-agent
  instruction surface.
- Do not promote the CSB reversal into a removal rule. It remains evidence for
  a future owner-gated doctrine decision.

The lane first selected cells-only. On 2026-07-17 the owner identified
discoverability as the missing criterion and authorized the named candidate.
That changes the keep/kill decision for a pointer-only router, not for a
rule-carrying playbook.

## Per-lesson disposition

| Lesson | Disposition | Current home or evidence |
|---|---|---|
| Shared-helper copies | Pointer | Package adoption paragraphs and `.agents/hooks/check_shared_helper_duplication.py` |
| Exemplar-first repair | Package-local hypothesis cells | `.agents/hooks/README.md`; `forseti-harness/README.md` |
| Mechanically gateable duplication | Pointer | Duplication checker and `.agents/workflow-overlay/validation-gates.md` |
| Behavior-preserving refactor review | Existing lane | `workflow-code-review` |
| Live-but-unwired removal risk | Evidence only; no rule adopted | `docs/hygiene/hooks_smallest_complete_audit_ledger_v0.md`, CSB reversal |
| Delegated review-and-patch | Conditional pointer | `workflow-delegated-review-patch`, only when separately commissioned |
| Addition/subtraction and ceremony | Pointer | `AGENTS.md` SCI |
| Workstream operations | Excluded from router | Existing handoff and development-workflow owners |

## Recurring toll and subtraction

The router adds trigger/discovery surface and a pinned-hash update on every
source change. Its benefit is one nameable entry point; it earns that toll only
while the sources remain costly to discover without it.

The hypothesis cell exists in two package READMEs, so future semantic changes
pay a two-location consistency cost. That duplication is accepted because the
existing adoption rule already has two package-specific consumer homes. No
mechanical gate, receipt, or new validation step was added.

Subtraction applied here: the candidate no longer carries the seven lessons,
the scoping record no longer duplicates the router sequence, and the proposed
removal doctrine is not installed.

## Evidence boundary

The cold-agent probe behind exemplar-first repair is author-observed
(2026-07-16), not landed evidence; both README cells therefore label it a
working hypothesis. The CSB reversal is a recorded case, not a generalized
rule. Re-read current sources before any strict freshness, validation,
acceptance, deployment, activation, or resolver claim.
