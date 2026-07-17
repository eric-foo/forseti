# Slop-Audit Skill — Scoping & Per-Lesson Kill-Decision v0

```yaml
retrieval_header_version: 1
artifact_role: hygiene scoping decision (owner adjudication input)
scope: >
  Wave-5 capstone of the 2026-07 code-slop workstream. Runs the handoff
  packet's kill-criterion against the eight hard-won lessons, records the
  per-lesson keep/pointer/cell decision with evidence, and recommends the
  smallest-complete reusable form. Decision: form (b) — distill the two
  genuinely novel lessons as cells at their decision nodes; NO new skill.
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

## Decision: Form (b) — cells at decision nodes, no new skill

A new `slop-audit` skill fails on four independent gates, any one of which is
sufficient. Sunk cost ("we ran the playbook five times") is explicitly not a
keep-reason (Frozen Decision, packet).

1. **Kill-criterion (no novel glue survives).** The slop-audit orchestration —
   audit → dedup sweep → cross-vendor review → adjudicate as claims → mechanical
   gate — is already fully composed from existing workflow-kernel skills
   (`workflow-code-review`, `workflow-delegated-review-patch`,
   `workflow-distill`) plus the live shared-helper duplication gate. A skill
   would ORCHESTRATE these; the packet's drift guard forbids re-implementing
   them. There is no genuinely novel, non-covered orchestration to hold.
2. **Skill-adoption doctrine (owner-gated + anti-broad).**
   `.agents/workflow-overlay/skill-adoption.md` line 119-120: a new named
   candidate "may be created and iterated only after explicit owner
   authorization for that named candidate" — not held by this lane. Line 127-133:
   accept only skills "specific and narrowly scoped to a real Forseti lane…
   Do not accept broad, generic, or authority-claiming local skills." A
   cross-cutting slop-audit skill is the broad/generic class the doctrine
   rejects (contrast the narrow `forseti-product-lead` / `creator-audience-
   triangulation` lanes).
3. **Authoring discipline (no local-fact leakage).**
   `workflow-skill-authoring-discipline` § Smallest Durable Change: "Do not make
   the skill carry local project facts, local validation commands, local file
   paths… Those are overlay-owned." A slop-audit skill's entire substance IS
   local facts (the specific gate, the specific shared homes, the specific
   READMEs) — so the reusable-skill form is disallowed for exactly the content
   that would make it useful. Those facts already live in their overlay/README
   homes.
4. **SCI kernel (subtraction-equal, ceremony debt).** A fat standing skill every
   agent may load is precisely the surface the updated kernel says to resist.
   This workstream's own hooks audit was a subtraction pass that cut ~1,183
   lines of unwired enforcement (ledger Section 5); applying the same lens to
   this lane's own output rejects a new standing artifact that no named defect
   class requires.

**Consequence.** The two genuinely novel lessons become cells at their decision
nodes (form b). Six of eight lessons are already covered by existing doctrine or
skills and get a pointer, not new surface. Producing "two cells, everything else
already carried" is the subtraction lens applied to our own output — a success,
not an under-delivery (packet, Do Not Forget).

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

- **Authored (installed this lane).** Lesson-2 exemplar-repair cell — one
  sentence appended to the adoption-rule paragraph in `.agents/hooks/README.md`
  and `forseti-harness/README.md` (the docs that own that rule per
  `validation-gates.md:195-196`). No mechanical contract changes; the dup gate
  and its checked delta-comment convention are untouched.
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

The lesson-2 cell adds one advisory sentence to two README adoption paragraphs.
Recurring toll: negligible — it is read, not enforced; it adds no gate, field,
receipt, or sync obligation, and does not change the dup gate's mechanical
contract. The only maintenance obligation is that if the adoption rule is ever
rewritten, the prioritization sentence travels with it. Judged worth paying: it
redirects the expensive "repair every copy" reflex a cold agent would otherwise
follow, at the same decision node where the gate already sends them.

## Not-proven boundary

The cold-agent probe evidence for lesson 2 is author-observed (2026-07-16) and
re-derivable by re-running the probe prompts against current main; it is not a
landed artifact and is marked a hypothesis. Every other cited SHA/path was
verified against `origin/main` at `a965cf67` on 2026-07-17. This document proves
nothing about validation, readiness, or acceptance.
