# Distillation Binding — Core-Spine Proof / Method-Validation Harness (prepare-only draft)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: per-spine distillation binding for the Core-Spine proof / method-validation harness (replays at a historical cutoff)
use_when:
  - Distilling a proof / method-validation lesson into a carried rule.
  - Reasoning about at-cutoff memo seal, snippet leakage, or cleaning/judgment boundary discipline.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - docs/product/core_spine/core_spine_v0_proof_protocol_v0.md
  - docs/decisions/distillation_binding_product_proof_v0.md
```

**Status: PREPARE-ONLY DRAFT** (see the index). Distills recorded method-validation outcomes. Reads
recorded outcomes; edits no product file; makes no validation or proof claim. **One proposed item is
held as a hypothesis, not a cell** (see Hypotheses) — it is a design note, not a recorded outcome.

## Harness bound

The agent running a Core-Spine method-validation replay: build an at-cutoff packet from clean
pre-cutoff sources → reason at the cutoff → seal the at-cutoff memo → (later) compare to outcome.
Governed actor: the replay executor. Decision nodes are the cutoff-memo seal and the snippet-handling
boundary.

## Pole / key finding

**Actor-carried.** The lessons are cutoff/seal discipline and leakage judgment; a spoiler keyword
scan is **OVER-EDGE** (cannot reliably tell a spoiler from clean evidence). The strongest recorded
outcome is a *real archived contamination* (a replay that compacted before seal), giving a concrete
under-case.

## A1 — outcome → cell pairs (real, cited)

### GUARD cutoff-memo-seal-before-compaction  (actor-carried; typed-token PARTIAL)
- decision_node: `node:at-cutoff-memo-seal`
- `GUARD cutoff-memo-seal-before-compaction: WHEN a replay's at-cutoff memo is not yet sealed (written + hashed) and context may compact → seal first; a unit compacted before seal is contaminated scratch → UNLESS the memo is already sealed.`
- outcome_class: a replay compacts before the at-cutoff memo is sealed, mixing pre-cutoff reasoning with post-compaction loss of source-ledger fidelity (contaminated output)
- causal_miss: missing boundary — "written + hashed" is the seal; a pre-seal compaction contaminates the unit
- verification: under-case (the MV-05 Phase-4 compaction) → archived as contaminated, rebuilt; over-edge (memo sealed first) → proceed
- substrate: actor-carried; PARTIAL — references the canonical `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL` token (home: prompt-orchestration binding, `node:source-heavy-unit-seal`)
- PROV: real archived contamination `docs/_inbox/contaminated_method_validation_replay_outputs_2026_05_21_phase4_mv05_compaction/` (contamination reason `BLOCKED_COMPACTION_BEFORE_ARTIFACT_SEAL`). tier: probed (recorded failure, archived, then rebuilt). date 2026-05-21.

### GUARD snippet-noise-no-leak  (actor-carried; OVER-EDGE)
- decision_node: `node:snippet-noise-containment`
- `GUARD snippet-noise-no-leak: WHEN pre-seal search results include out-of-window / post-window snippets → use NO leaked fact from those snippets in the at-cutoff memo → UNLESS the snippet content is genuinely clean pre-cutoff.`
- outcome_class: a post-window snippet body (product name, outcome fact) leaks into at-cutoff reasoning
- causal_miss: missing distinction — safe pre-cutoff snippet fields (date/title/URL) vs unsafe post-cutoff snippet bodies
- verification: under-case (a post-window snippet in pre-seal results) → no leaked fact used; over-edge (a clean pre-cutoff snippet) → usable
- substrate: actor-carried; **OVER-EDGE** — a keyword scan is at best a noisy advisory tripwire, never a clear
- PROV: `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md:44` "`snippet-noise: yes`: pre-seal search results included out-of-window or post-window snippets; no leaked fact from those snippets is preserved or used in the at-cutoff memo." tier: probed (recorded replay ledger). date 2026-05-21.

## A2 — core size / budget

Actor-carried; both cells are `silent-wrong-output`-class (a contaminated replay / a leaked spoiler
silently invalidate the proof) → prune-exempt from frequency-only retirement. Budget model-dependent;
not fixed here.

## A3 — spine / decision nodes

`node:proof-input-selection` · `node:at-cutoff-memo-seal` · `node:snippet-noise-containment` ·
`node:cleaning-judgment-boundary` (see Hypotheses) · `node:outcome-calibration` (post-seal only).
Cells index by `decision_node`.

## A4 — slots filled

- **intervention-type set** (closed; owner-extensible): `GUARD`, `SOURCE-RULE`, `TOKEN` (typed `BLOCKED_*`, referenced).
- **verification substrate**: the seal marker + the typed `BLOCKED_*` token (the contamination is recorded when it fires); otherwise replay-ledger review. No deterministic leak engine (over-edge).
- **fire-log capability**: MODERATE — contamination events are archived (a real fire-log of the seal cell); snippet-noise is flagged post-hoc in ledgers, not prevented in real time.
- **tier enum**: {accepted-orca-gate, probed, asserted}.
- **review window**: owner sets (per replay).
- **owner map**: the Core-Spine proof / method-validation owner.

## Secondary finding

The seal cell has a genuine archived fire-log (the `_inbox` contamination directories) — rare for an
actor-carried spine. It is the cleanest Orca example of a `silent-wrong-output` cell whose low firing
frequency is the steady state of a working rule, not evidence of deadness (prune-exemption in action).

## Hypotheses (held off-core; NOT a recorded outcome — no cell installed)

- **Corroboration-vs-amplification destructive-dedup.** `core_spine_v0_corroboration_vs_amplification_discipline_v0.md:37`
  ("Naive or destructive dedup destroys the very repetition that creates aggregate signal") is a
  **proposed design note**, explicitly "proposed, not validated" — a foreseeable risk, not a recorded
  wrong action. Per the doctrine it is held as a **hypothesis** at `node:cleaning-judgment-boundary`,
  not distilled into a core cell. It enters the ingest loop only when an actual destructive-dedup
  miss is recorded.

## Non-claims

Prepare-only; edits no product file; not validation, readiness, proof, or Core-Spine v0 validation;
placement is not authority; the destructive-dedup item is a hypothesis, not a cell.
```
