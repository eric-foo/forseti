---
name: slop-audit
description: "Route a Forseti code-slop hygiene pass (duplication, bloat, ceremony, drift) through its hard-won sequence and durable homes, or steer a cold agent about to write a duplicate helper, an oversized function, or an unwired checker. A thin router: it points at existing gates and workflow-kernel skills and never re-implements them. Do not trigger for a single obvious inline dedup you just do, generic code review (use workflow-code-review), artifact/prose review, or feature/runtime work."
---

# slop-audit (Forseti-local candidate source)

## Status and authority

Forseti-local candidate router for the code-slop hygiene lane. It is not
project, product, or enforcement authority and validates, gates, or accepts
nothing on its own. It POINTS at the durable homes that own each rule and at the
existing workflow-kernel skills; it never re-implements them or restates the
facts they own. Every project fact (gate names, shared homes, validation
commands, safety, lifecycle) defers to `AGENTS.md`, `.agents/workflow-overlay/`,
and the READMEs named below. It fails visibly when a home it points at is
missing rather than inventing the rule.

## Named failure this prevents

A cold agent facing a slop-shaped task re-derives the playbook from scratch or
skips a hard-won step — attempts an exhaustive repair instead of exemplar
repair, tries to gate a non-def-nameable duplication class, or cuts an
unwired-but-live artifact — because the sequence and its lessons live in
scattered homes (a dup-gate README, a delegated-review skill, the SCI kernel, a
hygiene ledger) with no discoverable entry point. This skill is that entry
point; it holds no facts a home already owns.

## Trigger boundary

Use when commissioned to sweep code slop (duplication, bloat, ceremony, drift)
across a surface, OR when about to write a duplicate helper, an oversized
function, or an unwired checker and you want the carried lessons before you do.

Negative triggers: a single obvious inline dedup you just perform; generic
implementation/code review (use `workflow-code-review`); non-code artifact or
prose review (use `workflow-adversarial-artifact-review`); feature, runtime, or
product work. Sunk cost ("we ran this playbook before") is not a trigger.

## Smallest complete run (route, do not re-implement)

Apply only the steps the bound task needs; each step points at the home that
owns the rule and the evidence. Confirm each home still exists before relying on
it (homes move).

1. **Diagnose the dominant signature first.** The recurring slop shape is
   "a shared home exists but the copied helpers were never deleted." Check the
   shared-helper adoption rule and its mechanical backstop before writing a new
   private helper. Home: the adoption-rule paragraphs in `.agents/hooks/README.md`
   and `forseti-harness/README.md`; gate: `.agents/hooks/check_shared_helper_duplication.py`.
2. **Exemplar repair, not exhaustive repair.** Fix the few copied-from exemplars
   rather than every copy — cold agents adopt the nearest existing file. Home:
   the same two adoption-rule paragraphs (the exemplar-repair sentence).
3. **Gate only def-nameable classes.** A one-regex-row-per-named-helper gate with
   a delta-comment escape hatch is the durable backstop; inline-block duplication
   is not def-nameable and stays with exemplar repair, never a new regex row.
   Home: the dup gate above and `.agents/workflow-overlay/validation-gates.md`
   (Enforcement Placement).
4. **Behavior-preservation is only as safe as the tests that would catch a
   change.** Weak coverage gates a refactor; prove byte-identical effective
   behavior before splitting. Home: the decomposition / test-fixture handoffs
   under `docs/prompts/handoffs/`.
5. **Cross-vendor delegated review before merge, adjudicated as claims.** Do not
   inherit findings; accept/modify/reject each as a hypothesis. Route:
   `workflow-delegated-review-patch` (do not re-implement it here).
6. **Unwired is not unused.** Before cutting an artifact as "unused," run a usage
   census, not only a wiring census: a spine playbook that runs it by hand, a
   unit test that loads it, or an architecture decision that retains it keeps it
   live with zero automated wiring. Home:
   `docs/hygiene/hooks_smallest_complete_audit_ledger_v0.md` (the CSB reversal);
   the forward rule is an owner-gated overlay recommendation in
   `docs/hygiene/slop_audit_skill_scoping_v0.md`.
7. **The audit is itself subject to SCI.** Subtraction weighs equally with
   addition; any new gate, skill, or artifact this pass produces must name its
   own recurring toll and the defect class it catches so the owner can weigh it.
   Home: `AGENTS.md` (Smallest Complete Intervention) and the overlay README
   Behavioral Admission.

## What this skill is not

Not a rigid step-by-step script — apply only what the task needs. Not authority,
validation, readiness, or acceptance. Not deployed, mirrored, or frozen (that is
a separate governance action under the Protected Skill Boundary in
`.agents/workflow-overlay/skill-adoption.md`). It does not re-implement the gates
or skills it points at; if a pointed-at home has moved, resolve the new home,
do not restate its rule here.
