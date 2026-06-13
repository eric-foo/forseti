# Distillation Doctrine — Orca Spine Bindings Index v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Prepare-only adoption record + one-binding-per-spine migration index for Orca's harnesses
  under the agnostic Distillation and Enforcement-Placement doctrines. Carries both §0 cores
  verbatim as referenced provenance; binds nothing into the always-on overlay and authorizes
  no substrate build.
use_when:
  - Distilling an Orca harness lesson into a carried rule (open the matching per-spine binding).
  - Checking how the Distillation / Enforcement-Placement doctrines map onto Orca spines.
  - Re-pinning a §0 core or auditing the core-fidelity check.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/validation-gates.md
  - docs/decisions/overlay_enforcement_placement_classification_v0.md
  - .agents/workflow-overlay/safety-rules.md
stale_if:
  - The agnostic §0 core of either doctrine is amended upstream (re-pin + re-ratify each binding).
  - An owner authorizes binding any §0 core into the always-on overlay (this record is then superseded by that decision).
  - A listed spine's harness materially changes (its binding's cells re-enter the ingest/prune loop).
```

## Status

**PREPARE-ONLY.** This record adopts two agnostic doctrines *as referenced provenance* and
indexes one prepare-only binding per Orca spine. It **edits no always-on overlay rule, wires no
§0 core into the resident instruction core, builds and installs no substrate, and authorizes no
implementation.** It is **not a doctrine change** (no durable governance rule was edited; this is
a prepare-only classification/distillation of *existing recorded* Orca lessons), so **no
`direction_change_propagation` receipt is owed** — the same boundary the sibling
`overlay_enforcement_placement_classification_v0.md` set. No validation, readiness, acceptance, or
proof claim is made. Binding any §0 core into Orca's always-on overlay remains **owner-gated** under
`.agents/workflow-overlay/safety-rules.md`.

Cells are drawn from **real recorded Orca outcomes only**. Where a spine has no recorded outcome
for a slot, the binding **scaffolds the slot and says so** — no cell is invented. Each load-bearing
citation in the per-spine bindings was verified against the cited file this turn.

## Owner directive (this turn)

Source-hierarchy #1 (explicit current-turn instruction): **full inventory** (one binding for every
spine in the table below) delivered as **one file per binding**. This index is the thin spine that
the per-binding files hang off.

## What is already adopted vs. what is new

- **Enforcement-Placement doctrine — already adopted in Orca.** The placement *principle* is bound
  in `.agents/workflow-overlay/validation-gates.md` → "Enforcement Placement"; the per-rule
  classification of the overlay-governance harness is
  `docs/decisions/overlay_enforcement_placement_classification_v0.md` (EP-01…EP-31); substrates are
  built (EP-06 retrieval-header hook `.agents/hooks/check_retrieval_header.py`; EP-01/EP-03
  protected-action `PreToolUse` guard `.agents/hooks/guard_protected_actions.py` + permission floor).
  That classification record explicitly named *"binding the shared distillation doctrine to Orca"*
  as a separate later task — this index is that task, prepare-only.
- **Distillation doctrine — new, prepare-only.** Carried here as referenced provenance and applied
  per spine in the eight bindings. Not wired into the always-on overlay.

## §0-core version-drift finding (re-pin)

Orca's existing inline EP core (in the EP classification record and the paraphrased
validation-gates "Enforcement Placement" section) predates the **accepted** pack's round-6 edit,
which added the **critical-path** qualifier ("fires *whenever that boundary is traversed*", "placing
a check *off the critical path* does not enforce it"). Per the doctrine's own `stale_if` ("the
agnostic core is amended → bindings must re-pin and re-ratify"), the canonical EP §0 below is the
re-pinned accepted text. **Refreshing the overlay's bound EP wording to the critical-path version is
an always-on edit and is therefore owner-gated — not done here.** It is flagged for the owner.

## §0 cores carried verbatim (referenced provenance — NOT installed)

Lifted verbatim from the agnostic doctrines (jb `docs/doctrine/`), carried inline **only because no
cross-repo shared home exists yet**, exactly as the EP classification carried the EP core. These are
**cited as provenance, not imported as Orca authority and not resident** in any always-on core. The
per-spine bindings fill the typed slots; they never weaken a core principle.

### Distillation §0 — installable core (verbatim)

```text
- SLOT TEST — admit to core iff all three: names a recurring loss it prevents ·
  changes an action when read alone · one line with every word load-bearing.
- LOSS — observed recurring, or catastrophic-cost, degradation in correctness,
  defensibility, completeness, calibration, routing, latency, or decision quality.
  Not "could be nicer."
- LESSON CELL (the unit) — one outcome class → one decision node → one causal
  miss (distinction / boundary / case / trigger) → one typed intervention → one
  verification pair → one owner → one retirement test. The full record is one keyed
  LESSON; PROV is one field of it (evidence/provenance), not the record itself.
- NO DECISION NODE, NO LESSON — a lesson that cannot name its decision node — the
  pipeline step where the agent takes or withholds an action — does NOT distill: raise
  BLOCKED_NO_DECISION_NODE and stop (fail loud); do not install, do not silently keep it
  as a note. Hold it as analysis and re-enter only when a node is named.
- VERIFY FIRING — do not credit an installed rule as working because it is present
  or verbally satisfied; require its expected action in the output. Where no checkable
  signal exists, mark compliance unverified, not done.
- INTERVENTION TYPE — install as exactly one bound intervention type; the binding
  owns a per-harness-closed, owner-extensible set. The core fixes no universal enum.
- GUARD FORM — guard is one intervention subtype (the most common), not a default; if
  the bound intervention is a guard, use GUARD <id>: WHEN <predicate> → <action> →
  UNLESS <constraint>. Evidence only in the keyed PROV field.
- EFFICIENCY RANK (ordinal judgment, not a measurement) — rank by behavior-change ÷
  tokens = fire-frequency × loss-cost ÷ resident-lines. Core iff common+loud, or any
  silent/catastrophic-loss class; else triggered SATELLITE.
- DISTILLATION LOAD — when converting an outcome into a lesson, load the binding and
  run the full INGEST + paired PRUNE procedure (§2 f-i / f-ii). No install without a
  decision node, a verification pair, a conflict-check, and owner-gated binding; no
  frequency-only prune without fire-log evidence; silent/catastrophic cells are
  prune-exempt; one-in / one-out under a fixed budget.
- CORE / BINDING SPLIT — core = shape; binding = harness-specific tokens
  (intervention-type set, line budget, verification substrates, fire-log capability,
  review window, owner map), owner-gated. Specific detector: a token is a specific
  (→ binding) iff its meaning would change in another harness/repo.
- LOAD RULE — load the smallest pack that resolves route / blocker / edit-boundary
  / claim; expand only when the decision is undetermined.
```

### Enforcement-Placement §0 — installable core (verbatim, re-pinned to accepted/critical-path)

```text
- ENFORCEMENT PLACEMENT — when a rule must hold at a boundary, prefer enforcing it in a
  deterministic substrate on that boundary's critical path (tool-boundary hook ·
  gate/assertion · schema/typed boundary token · deterministic test) over a resident model
  instruction. A code-enforced rule fires whenever that boundary is traversed, without
  spending resident model-instruction budget; an actor-carried rule is flexible but
  attention-dependent and competes for budget.
- CLASSIFY SUBSTRATE-FIRST — before admitting any rule into the resident instruction core,
  run the substrate test: is there a deterministic boundary on the rule's critical path that can
  enforce it? If yes, harden it there and carry no duplicate in the model — at most a thin
  pointer to that boundary, and only if it changes the actor's action. Skipping the test is the
  recurring miss this doctrine closes.
- RESERVE THE BUDGET — spend always-on instruction budget only on rules whose firing needs
  judgment, salience, prioritization, or framing that no deterministic boundary can decide. Do
  not spend resident budget merely to remember a rule already enforced on the critical path; the
  budget is scarce and degrades with rule count and position.
- ACTOR-CARRIED REMAINDER OWES FIRING — carry as a model instruction only the remainder
  with no deterministic boundary check (judgment, framing, salience); that remainder is still
  subject to VERIFY FIRING — present in the prompt is not the same as fired.
- PLACEMENT IS NOT AUTHORITY — this doctrine decides WHERE a rule is enforced, never
  WHETHER it is correct, validated, bound, or sufficiently covered. Choosing code-enforcement
  does not validate the rule; placing a check off the critical path (or behind an optional /
  non-exhaustive boundary) does not enforce it; and forcing a judgment rule into brittle code to
  "always fire" is the over-edge failure.
```

## Spine inventory → per-spine bindings

Pole = where the spine sits on the code-enforced ↔ actor-carried axis. "Real cells" = count of
verified recorded-outcome→cell pairs; "scaffold/hyp" = slots named without a recorded outcome.

| # | Spine / harness | Pole | Binding | Real cells | Scaffold / hypothesis |
| --- | --- | --- | --- | --- | --- |
| 1 | Overlay-governance | mixed → code-enforced | `distillation_binding_overlay_governance_v0.md` | 3 | EP-04/08–13 partials (per EP classification) |
| 2 | orca-harness code | **code-enforced** (Orca "render" pole) | `distillation_binding_orca_harness_code_v0.md` | 3 | — |
| 3 | Judgment Spine | actor-carried + gate scaffolding | `distillation_binding_judgment_spine_v0.md` | 3 | JSG-01 finalizer unstaffed (blocker, not a cell) |
| 4 | Data Capture / Source Capture | mixed (lane judgment + code chokepoints) | `distillation_binding_data_capture_v0.md` | 3 | live-fetch / proxy hard-stops (boundaries) |
| 5 | Prompt-orchestration | actor-carried (shape→schema partial) | `distillation_binding_prompt_orchestration_v0.md` | 3 | EP-08/09/10/11 receipt-shape schemas |
| 6 | Product-proof / buyer-proof | **actor-carried** (Orca "maximize" pole) | `distillation_binding_product_proof_v0.md` | 3 | pull-vs-praise (rule, no recorded instance yet) |
| 7 | Review / patch lanes | actor-carried (lane-tag partial) | `distillation_binding_review_patch_v0.md` | 3 | reviewer-lane write block (EP-21, over-edge) |
| 8 | Core-Spine proof / method-validation | actor-carried | `distillation_binding_core_spine_proof_v0.md` | 2 | corroboration-vs-amplification (design note → hypothesis) |

The current branch's **ECR deriver** (SP-3/SP-6) work is recent and has no distinct recorded
outcome yet; it is folded under Data Capture as a deferred sub-node rather than given an invented
binding. If ECR accrues its own recorded lessons, it graduates to its own binding via the ingest loop.

## Core-fidelity check (deliverable #3)

- **Both §0 cores are reproduced unchanged.** No core principle was reworded, dropped, split, or
  weakened. The only adjustment is the **EP §0 re-pin to the accepted critical-path text** (an
  upstream amendment Orca's older inline copy had not yet tracked) — a re-pin to the canonical core,
  not an Orca edit of it.
- **Typed slots the bindings fill** (per the CORE / BINDING SPLIT): `intervention-type set`,
  `line budget`, `verification substrate`, `fire-log capability`, `tier enum`, `review window`,
  `owner map`, and the concrete `node:<id>` decision nodes, predicates, paths, and `BLOCKED_*`/
  `FAILED_*` token names. Each is a typed slot the core references but does not define; filling them
  is the binding's whole job.
- **Slots filled, not principles altered.** Nothing in any binding overrides SLOT TEST, NO DECISION
  NODE NO LESSON, VERIFY FIRING, the prune triggers, one-in/one-out, ENFORCEMENT PLACEMENT,
  CLASSIFY SUBSTRATE-FIRST, or PLACEMENT IS NOT AUTHORITY.

## Code-enforce-first summary (applied per binding)

Per the EP §0, each binding classifies its cells substrate-first before counting actor budget:

- **orca-harness code** is Orca's deterministic pole — every cell is code-enforced (a pytest
  contract test that records the failure it prevents), costs zero resident budget, and satisfies
  VERIFY FIRING by construction.
- **Overlay-governance** is mixed and trending code-enforced (two `PreToolUse`/`PostToolUse` hooks
  already built; the rest is the EP classification's PARTIAL/JUDGMENT remainder).
- **Product-proof, Judgment Spine, Prompt-orchestration, Review/patch, Core-Spine proof** are
  largely **actor-carried** (judgment/framing/salience), so their cells compete for the always-on
  budget and each owes VERIFY FIRING. Their OVER-EDGE items (zero-spoiler leak scan, reviewer-lane
  hard-block) are flagged: do not force them into brittle code.

## How to read a binding (so future agents can use them)

Each `distillation_binding_*_v0.md` carries: the harness bound and its spine; the pole / key
finding; **A1** real outcome→cell pairs as `GUARD` lines with a cited `PROV` field; **A2** core
size / budget; **A3** decision nodes (the `node → [cells]` index); **A4** the filled typed slots; a
secondary finding; explicit scaffold/hypothesis slots; and non-claims. A cell that fires in more
than one place references **one canonical `LESSON`/`node` id** rather than copying text.

## Lifecycle

```text
candidate → accepted → bound(orca) → superseded
```

- **candidate** *(current state)* — prepare-only; the eight bindings exist as drafts; nothing is
  bound into Orca's always-on overlay.
- **accepted** — owner ratifies this index + the bindings as Orca's canonical prepare-only
  distillation mapping (still not resident).
- **bound(orca)** — owner authorizes wiring a specific binding's cells (or a §0 core) into the
  always-on overlay and/or building a named substrate; recorded in that decision and listed here.
- **superseded** — a later distillation mapping replaces this; set `superseded_by`.

## Non-claims

- Prepare-only. **Not validated against a live harness; not bound into any always-on core; not a
  doctrine change; no DCP receipt owed; no substrate built.**
- Cells are from **real recorded outcomes only**; scaffolded slots are labeled and contain no
  invented cell. The "destructive-dedup" item (Core-Spine proof) is explicitly held as a
  **hypothesis** (a proposed design note, not a recorded outcome).
- The §0 cores are carried as **referenced provenance**, not as Orca authority; binding them into
  the overlay is owner-gated.
- Not acceptance, readiness, approval, source-of-truth promotion, or implementation/runtime
  authorization. Placement choices decide WHERE a rule would be enforced, never WHETHER it is
  correct (PLACEMENT IS NOT AUTHORITY).
```
