# Slop-Audit Skill — Scoping & Per-Lesson Kill-Decision v0

```yaml
retrieval_header_version: 1
artifact_role: hygiene scoping decision (owner adjudication input)
scope: >
  Wave-5 capstone of the 2026-07 code-slop workstream. Runs the handoff
  packet's kill-criterion against the eight hard-won lessons, records the
  per-lesson keep/pointer/cell decision with evidence, and recommends the
  smallest-complete reusable form. Decision: form (c) — a THIN router skill for
  discovery (owner-steered 2026-07-17 on the brittleness of scattered pointers)
  PLUS the two genuinely novel lessons as cells at their decision nodes; the
  skill re-implements nothing and the cells are its targets.
use_when:
  - Owner adjudication of whether a slop-audit skill (or which cells) earns its keep.
  - A future cold agent facing a slop-audit-shaped task wants the carried lessons.
authority_boundary: retrieval_only
branch_or_commit: wave5 lane off origin/main a965cf67 (measured 2026-07-17)
stale_if: >
  The dup gate, its README adoption paragraphs, the hooks-audit ledger, or the
  AGENTS.md SCI kernel change after 2026-07-17; re-verify the cited SHAs/paths.
open_next:
  - .agents/hooks/README.md
  - forseti-harness/README.md
  - docs/hygiene/hooks_smallest_complete_audit_ledger_v0.md
```

Commissioned by the Goal Handoff lane of the wave5 slop-audit handoff packet
`docs/prompts/handoffs/slop_audit_skill_authoring_wave5_handoff_v0.md` (branch `claude/wave5-skill-handoff`, authoritative — not yet on main). Measured against the updated
Smallest Complete Intervention kernel (`AGENTS.md`, commit `cd046d05` — "Center
AGENTS kernel on Smallest Complete Intervention (#1019)"): subtraction weighs
equally with addition; a new gate/skill is ceremony debt whose recurring toll
must be named and judged worth paying.

**Non-claims.** This is a scoping decision plus resident judgment, not
validation, readiness, or acceptance. It authorizes no deployment and installs
no standing skill. Anything it recommends for an overlay/AGENTS.md surface is a
doctrine change that stays owner-gated. Cross-vendor delegated review
(`workflow-delegated-review-patch`), adjudicated as claims, is the acceptance
path for anything produced here.

## Decision: Form (c) — a thin router skill + the two cells

**Decision history (honest).** This lane first chose form (b) — cells only, no
skill — on a four-gate case against a new standing skill. The owner adjudicated
(2026-07-17): scattered pointers are brittle because they have no discoverable
entry point. That is correct, and it is the one axis the four-gate case
under-weighted. The four gates below still hold — but only against a FAT rigid
playbook skill. A THIN router (option c) satisfies every one of them and closes
the discovery gap. The corrected decision is (c): a thin `slop-audit` router that
holds the sequence and points at the durable homes, plus the two novel cells the
router points at.

The four gates, re-read against a thin router:

1. **Kill-criterion — the novel glue is discovery, not orchestration.** The
   individual steps (cross-vendor review, code review, distillation, the dup
   gate) are each covered by an existing skill or gate, and the router
   re-implements none of them. What did NOT exist is a nameable entry point that
   holds the slop-specific SEQUENCE and its lessons together — diagnose the
   dominant signature → exemplar (not exhaustive) repair → gate only def-nameable
   classes → coverage-gated behavior preservation → cross-vendor review as claims
   → unwired≠unused → SCI-on-itself. That sequence + discovery IS the glue a thin
   router legitimately holds; it is not re-implementation.
2. **Skill-adoption doctrine (owner-gated + anti-broad).**
   `.agents/workflow-overlay/skill-adoption.md:119-120` requires explicit owner
   authorization for a named candidate — now given (2026-07-17). The anti-broad
   rule (`:127-133`) rejects "broad, generic, or authority-claiming" skills; the
   router stays narrow (one task shape), claims no authority, and defers every
   fact — the same shape doctrine already accepts for `creator-audience-
   triangulation`. Recorded as a Forseti-local candidate, not accepted/frozen or
   deployed.
3. **Authoring discipline (no local-fact leakage).**
   `workflow-skill-authoring-discipline`: a skill must not CARRY local project
   facts. The router does not inline them — it POINTS at the homes that own the
   gate names, shared homes, and validation. That is the compliant shape, not the
   forbidden one. If a fat skill had inlined those facts it would fail this gate;
   the thin router passes it precisely by staying a router.
4. **SCI kernel (subtraction-equal, ceremony debt).** A router loaded only on an
   explicit `slop-audit` trigger is on-demand, not always-on; its recurring toll
   is a few KB read when invoked, not a per-turn tax. Named and judged worth
   paying against the discovery defect it prevents (see toll section below). The
   FAT-skill version this gate rejects is exactly what was NOT built.

**Consequence.** Form (c): one thin router skill (discovery) + two cells at their
decision nodes (the novel principles). Six of eight lessons remain existing-
covered and the router POINTS at them rather than re-encoding — so the router
stays thin and the facts stay single-sourced in their homes.

## Per-lesson kill-decision catalogue

Kill-criterion applied per lesson: (1) already covered by an existing skill or
doctrine surface? → pointer. (2) what does every future agent PAY to keep it
standing? (3) what recurring defect class does it prevent, with evidence it
recurs? Verdict vocabulary: `pointer` (existing-covers) / `cell`
(novel-decision-node install) / `recommend-cell` (novel but doctrine-gated home
— owner installs).

| # | Lesson (gist) | Verdict | Home / pointer | Evidence |
|---|---|---|---|---|
| 1 | "Shared home exists but the copies were never deleted" is the dominant slop signature | **pointer** | The dup gate + the two README adoption paragraphs already detect and govern this exact class | `.agents/hooks/check_shared_helper_duplication.py` (on main); README adoption paragraphs |
| 2 | Exemplar repair beats exhaustive repair — cold agents copy the nearest file, so fix the 3-5 exemplars | **cell** | README adoption paragraphs (rule-owning docs) | Cold-agent probes 2026-07-16 (hypothesis — re-derivable, not landed) |
| 3 | Mechanical gate, one regex row per def-nameable class, delta-comment escape hatch; LIMIT: inline-block dup is not def-nameable and must NOT be gated | **pointer** (+ LIMIT folded into cell 2) | Gate + its README row already encode the mechanism; the "don't gate non-mechanical classes" limit rides with cell 2 | Gate row `.agents/hooks/README.md`; validation-gates.md "Enforcement Placement" |
| 4 | Behavior-preservation is only as safe as the tests that would catch a change; prove byte-identical kwargs | **pointer** | Already carried operationally by the decomposition/test-fixture handoffs; generic refactor-safety wisdom, no standing-doctrine gap | decomposition + test-fixture-sugar handoffs (#1037 lineage) |
| 5 | "Unwired ≠ unused" — a completeness/removal assessment must census product-workflow consumers (playbooks, unit tests, architecture decisions), not just harness wiring | **recommend-cell** (doctrine-gated home) | overlay `validation-gates.md` completeness gate OR `AGENTS.md` "removals keep their evidence gates" — a doctrine change, owner-gated | Ledger Section 5 CSB reversal (`hooks_smallest_complete_audit_ledger_v0.md:196-205`, on main via PR #1051) |
| 6 | Cross-vendor delegated review before merge, adjudicated as claims | **pointer** | `workflow-delegated-review-patch` skill (exists, used heavily this workstream) | skill-adoption.md recognition table |
| 7 | Subtraction weighs equally with addition; a new gate/skill is ceremony debt | **pointer** | `AGENTS.md` SCI kernel + overlay README "Behavioral Admission" already install it | `AGENTS.md` (cd046d05); `.agents/workflow-overlay/README.md:15-30` |
| 8 | Operational lessons: foreground validation, commit-per-work-unit, branch-pinned handoffs, delete `_scratch`, pin-contract tests in scope, partition file ownership, merge treadmill | **pointer** | Lane-runner / dev-workflow operational surface, not slop-specific; `workflow-handoff` already binds branch-pinned packets | `workflow-handoff`; dev-workflow doctrine |

### Why lessons 2 and 5 are the only cells

- **Lesson 2 (cell).** The existing adoption rule governs *when to migrate* a
  stale copy; it does not carry the *repair-prioritization* insight — that cold
  agents copy the nearest existing file, so repairing the few copied-from
  exemplars redirects all future code at a fraction of the cost of fixing every
  copy. Genuinely novel, low toll (one sentence in each rule-owning README), and
  evidenced by two cold-agent probes. Installed this lane (see below). The
  lesson-3 LIMIT (inline-block duplication is not def-nameable and must stay with
  exemplar repair, not a gate) rides with the same sentence — it is the reason
  the gate stops at def-nameable classes.
- **Lesson 5 (recommend-cell).** The sharpest lesson and the highest-cost defect
  class: a wiring census nearly cut a 1,264-line validator
  (`check_commission_signal_board_output.py`) that a live pilot spine's playbook
  requires by hand, a unit test loads, and an architecture decision explicitly
  retained. The ledger records it as a one-off "audit-method limitation"; the
  forward *rule* ("a usage census is not a wiring census — before cutting an
  artifact as unused, census manual/product-workflow consumers, not just
  settings/CI/githooks wiring") does not yet exist as standing doctrine. Its only
  correct homes are overlay authority (`validation-gates.md`) or the SCI kernel
  (`AGENTS.md`) — both doctrine changes that require owner adjudication and a
  `direction_change_propagation` receipt (`validation-gates.md:65-70`). This lane
  therefore recommends it rather than unilaterally editing overlay authority.

## What this lane authored vs. recommended vs. pointed at

- **Authored (installed this lane).**
  - The thin `slop-audit` router skill at `.agents/skills/slop-audit/SKILL.md`,
    registered as a Forseti-local candidate in
    `.agents/workflow-overlay/skill-adoption.md` (source path, LF sha256, scope,
    collision, boundary, rollback). Candidate only — NOT deployed, mirrored to
    `.claude/skills/`, or accepted/frozen; that is a separate governance action
    under the Protected Skill Boundary.
  - Lesson-2 exemplar-repair cell — one sentence appended to the adoption-rule
    paragraph in `.agents/hooks/README.md` and `forseti-harness/README.md` (the
    docs that own that rule per `validation-gates.md:195-196`). No mechanical
    contract changes; the dup gate and its checked delta-comment convention are
    untouched.
- **Recommended (owner-gated, NOT installed).** Lesson-5 unwired≠unused cell.
  Proposed target: a new bullet in `validation-gates.md` "Current Gates" (or a
  clause on the AGENTS.md removals-keep-evidence sentence). Proposed wording:
  > Before removing an artifact as "unused," run a usage census, not only a
  > wiring census: a wiring census (settings.json / ci.yml / .githooks /
  > capsule) is not a usage census. Manual/product-workflow consumers — a
  > spine playbook that runs it by hand, a unit test that loads it, an
  > architecture decision that explicitly retains it — keep an artifact live
  > even with zero automated wiring.

  Named toll: every future removal claim pays one usage-census step. Defect
  class caught: cutting a live-but-unwired artifact (evidence: the CSB
  reversal). Owner weighs the toll and, if accepted, adds the
  `direction_change_propagation` receipt the overlay's doctrine-change gate
  requires.
- **Pointed at (no new surface).** Lessons 1, 3, 4, 6, 7, 8 — each already lives
  at a decision node listed in the catalogue above.

## Named recurring toll of what was installed

- **The router skill.** On-demand only (fires on an explicit `slop-audit`
  invocation or its narrow description trigger), so it costs nothing per turn —
  a few KB read when invoked. Maintenance obligation: it is a router, so if a
  home it points at moves, the pointer must be re-resolved (the skill fails
  visibly rather than restating the rule). Its sha256 pin in `skill-adoption.md`
  is reread-required on any source change (freshness-gated by
  `check_hash_pin_freshness.py`). Judged worth paying: it prevents the discovery
  defect — a cold agent re-deriving the playbook or skipping a hard-won step
  because the lessons had no entry point.
- **The lesson-2 cell.** One advisory sentence in two README adoption
  paragraphs. Negligible — read, not enforced; no gate, field, receipt, or sync
  obligation; no change to the dup gate's mechanical contract. Only obligation:
  the sentence travels with the adoption rule if that is ever rewritten. Judged
  worth paying: it redirects the expensive "repair every copy" reflex at the same
  node the gate already routes to.

Both stay candidates pending the cross-vendor delegated review the operator
routes; neither is a deployment, acceptance, or readiness claim.

## Not-proven boundary

The cold-agent probe evidence for lesson 2 is author-observed (2026-07-16) and
re-derivable by re-running the probe prompts against current main; it is not a
landed artifact and is marked a hypothesis. Every other cited SHA/path was
verified against `origin/main` at `a965cf67` on 2026-07-17. This document proves
nothing about validation, readiness, or acceptance.
