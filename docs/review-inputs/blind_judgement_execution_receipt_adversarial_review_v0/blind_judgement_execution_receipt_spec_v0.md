# Blind-Judgment Execution Receipt — Behavior Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Spec
scope: >
  Behavior contract (what-must-be-true) for the separate no-tools execution
  receipt that binds a blind-judgment run's proven isolation + auditable
  live-execution provenance, kept as a sibling artifact to blind_judgement.yaml.
  It is the concrete JSG-04 no-tools execution receipt for a JSG-06 blind-judgment
  run; BlindJudgement and the run_case scorer are unchanged. Docs/spec only — not
  the build, not a runner, not a live-call authorization, not a JSG-04/JSG-06
  clearance. Product-learning grade.
use_when:
  - Scoping or authorizing the blind-judgment execution-receipt build (what the receipt must carry, where it lives).
  - Checking what JSG-04 (no-tools isolation) and JSG-06 (blind judgment) read as their owner isolation/provenance field for a blind-judgment run.
  - Reviewing whether a blind-judgment execution receipt is valid (proven isolation, bound provenance, bound to the judgment, complete).
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/sp5_finalization_receipt_spec_v0.md
  - docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md
  - docs/product/judgment_spine_gate_ownership_map_v0.md
stale_if:
  - The BlindJudgement schema gains an isolation/execution field (then the separate-record shape is reconsidered).
  - contestant_no_tools_execution_contract_v0.md changes its Required Execution Fields, isolation_result semantics, or Receipt Provenance Boundary.
  - ContestantExecutionIsolation (schemas/probe_models.py) changes its fields or derive_isolation_result rule.
  - The conductor changes JSG-04's required receipt or JSG-06's isolation/provenance predicate binding.
  - A blind-judgment execution-receipt mechanism is built (then this spec moves from contract to as-built).
```

## Status

**Spec status:** DRAFT_FOR_CROSS_VENDOR_REVIEW. Docs/spec only; authorizes no
build, no model run, no live call. Authored on the spec-first path; **not yet
reviewed** — the new-seam cross-vendor discovery-bar review (family=vendor
doctrine) gates scoping and any build.

## Frozen input basis (settled; not re-opened here)

- **Shape = separate sibling record** (owner-decided): the isolation receipt +
  provenance is a **separate artifact next to `blind_judgement.yaml`**, NOT a
  field on `BlindJudgement` and NOT the `advisory_phase_1_fields` bag. Rationale
  (owner-accepted): lowest downstream lock-in (the central `BlindJudgement`
  contract, the `run_case` scorer, the reports, and the existing
  `blind_judgement.yaml` artifacts are untouched); matches the harness's own
  probe design (isolation lives in `MemorizationProbeArtifact`, not in
  `ParsedProbeResponse`); mirrors SP-5's separate-`FinalizationReceipt`
  precedent; and the gate reads isolation as an **out-of-band receipt** by design
  (conductor Isolation Topology + by-hand isolation cap; gate-ownership JSG-04
  row), not as a field typed into the judgment.
- **Reuses the existing `ContestantExecutionIsolation`** (schemas/probe_models.py)
  as the isolation receipt; this spec does not redefine isolation fields or
  `derive_isolation_result`.
- **The no-tools execution contract is the controlling doctrine.** This spec
  defines the concrete receipt artifact that satisfies that contract's Required
  Execution Fields + Receipt Provenance Boundary for a blind-judgment run; the
  contract wins on any isolation/provenance conflict.
- **Product-learning grade.** Dry-runner / fake-transport / fixture /
  operator-authored receipts are **permanently non-gate-clearing** (no-tools
  contract Receipt Provenance Boundary + conductor by-hand isolation cap), even
  when their computed `isolation_result` is `proven`.

## Required behavior

- For a blind judgment's **JSG-06** clearance (and the **JSG-04** no-tools
  execution receipt it inherits) to read as satisfied, a **separate execution
  receipt** must exist that:
  - is **bound to the exact blind judgment** it certifies — carrying the same
    `case_id`, `run_id`, and `contestant_id` as the `blind_judgement.yaml`, plus
    the `prompt_hash` and `raw_response_hash` of that execution;
  - carries a `ContestantExecutionIsolation` with **`isolation_result == proven`**;
  - carries the **auditable live-execution provenance** the no-tools contract's
    Receipt Provenance Boundary requires (provider, endpoint URL, UTC run
    timestamp, process exit status, console output), either in-receipt or as a
    bound reference to the out-of-band operator record the contract names.
- The receipt is a **sibling artifact** to `blind_judgement.yaml` in the run
  directory (`runs/<contestant>/<run>/`). `BlindJudgement` and `run_case.py` are
  **unchanged**: the scorer keeps reading the bare `blind_judgement.yaml` and
  does **not** read this receipt.
- A consumer (the conductor / gate) must treat a **missing, invalid,
  identity-mismatched, or non-proven** receipt as **not-cleared (block)** for the
  isolation/provenance predicate, and must **never author, default, type-in, or
  infer** isolation or provenance. The receipt is produced out-of-band by the
  execution runner; the consumer validates only. (A hand-typed
  `isolation_result: proven` is explicitly non-self-certifying and
  non-gate-clearing.)
- Isolation semantics (what makes `isolation_result` `proven` / `not_proven` /
  `violated`) are **owned by** `ContestantExecutionIsolation` + the no-tools
  contract; this spec **does not restate or redefine** them.

## Non-goals

- **Not** a change to `BlindJudgement` or to `run_case.py` (the scorer) — the
  receipt is a separate record; the judgment artifact and scoring path are
  untouched.
- **Not** the receipt/runner build or a live-call authorization — needs separate
  implementation authorization; the deterministic (fake-transport) runner and any
  live call are later, separately-authorized steps.
- **Not** a JSG-04/JSG-06 clearance or unfreeze — this defines the owner field
  the gate reads; it does not advance any gate, and a clean run still requires an
  authorized live execution that produces a `proven` receipt.
- **Not** a redefinition of `ContestantExecutionIsolation` or the no-tools
  contract (reuses / points to them).
- **Not** a claim-tier mint — product-learning grade; not judgment-quality
  evidence.
- **Not** the conductor predicate wiring itself — the precise field-path by which
  JSG-04/JSG-06 resolve to this receipt is confirmed at scoping (see Open
  questions).

## Interfaces / contracts

`ContestantExecutionReceipt` (working name) — a **separate record, sibling to
`blind_judgement.yaml`**, associated to a blind-judgment run by (`case_id`,
`run_id`, `contestant_id`):

| Field | Type | Contract |
| --- | --- | --- |
| `case_id` | str | must equal the certified `blind_judgement.yaml` `case_id` |
| `run_id` | str | must equal the certified judgment's `run_id` |
| `contestant_id` | str | must equal the certified judgment's `contestant_id` |
| `model_family` / `model_id` | str | operator-recorded; `model_snapshot_if_available` optional |
| `execution_surface` | ExecutionSurface | the accepted live surface is `raw_api_no_tools`; dry/fixture surfaces are non-gate-clearing |
| `prompt_hash` | str | hash of the exact prompt sent (binds the receipt to the judged execution) |
| `raw_response_hash` | str | hash of the exact raw response (binds the receipt to the judged execution) |
| `contestant_execution_isolation` | ContestantExecutionIsolation | the existing receipt; `isolation_result` must be `proven` for clearance |
| `execution_provenance` | { provider, endpoint_url, run_timestamp_utc, process_exit_status, console_output } | the no-tools contract's provenance boundary; in-receipt or a bound reference to the out-of-band operator record |
| `created_at` | str (UTC) | timestamp of receipt creation |
| `non_claim_notice` | str | the exact product-learning claim boundary (as `MemorizationProbeArtifact` carries) |

Invariants:

- `isolation_result == proven` is **required** for clearance; `not_proven` or
  `violated` ⇒ block.
- the receipt's (`case_id`, `run_id`, `contestant_id`) must **match** the
  `blind_judgement.yaml` it certifies; `prompt_hash` / `raw_response_hash` bind it
  to that exact execution; mismatch ⇒ invalid ⇒ block.
- the consumer is **read-only** over the receipt (block-don't-repair); it never
  authors/defaults/infers isolation or provenance.
- **dry / fake-transport / fixture / operator-authored** receipts are
  non-gate-clearing regardless of computed `isolation_result` — the receipt must
  record its `execution_surface` and provenance honestly so a dry receipt can
  never be mistaken for a live one.

## Acceptance criteria (testable in principle)

- A valid **live** receipt (present; `case_id`/`run_id`/`contestant_id` match the
  judgment; `isolation_result == proven`; provenance bound; hashes present) ⇒ the
  JSG-04/JSG-06 isolation+provenance predicate reads cleared (subject to the other
  JSG-06 subpredicates and the JSG-04 inheritance).
- Missing receipt ⇒ block (not-cleared); nothing authored.
- `isolation_result` `not_proven` or `violated` ⇒ block.
- receipt↔judgment identity mismatch (`case_id`/`run_id`/`contestant_id` or hash)
  ⇒ invalid ⇒ block.
- `BlindJudgement` + `run_case.py` are unchanged: the scorer reads the bare
  `blind_judgement.yaml` and ignores the receipt; existing `blind_judgement.yaml`
  files still validate.
- A **dry / fake-transport** receipt (e.g. `execution_surface != raw_api_no_tools`,
  or no live provenance) never clears the gate even if its computed
  `isolation_result` is `proven`.

## Open questions (deferred to scoping / the cross-vendor review)

- **Conductor predicate binding (lead item):** the precise field-path by which
  JSG-04 (provenance complete) and JSG-06 (`isolation_result proven`) resolve to
  this sibling receipt. Grounding (conductor Isolation Topology, by-hand isolation
  cap, gate-ownership JSG-04 row) confirms the gate reads an **out-of-band
  receipt** (not a field typed into the judgment), so the sibling shape is sound;
  the exact owner-field path is confirmed against the conductor + gate-ownership
  map at scoping. (This is the item that, had the gate required isolation *inside*
  `BlindJudgement`, would have forced a schema change — grounding shows it does
  not.)
- The receipt's exact filename + schema name (`execution_receipt.yaml` /
  `ContestantExecutionReceipt` are working names) and serialization.
- Which provenance fields live **in-receipt** vs. in the **bound out-of-band
  operator record** the no-tools contract names.
- Whether to add a deterministic `binding_hash` over the receipt↔judgment identity
  (as SP-5 carries) — additive; a scoping decision.
- Whether to link the receipt to a specific judge run id beyond
  `model_family`/`model_id` — additive/non-breaking.

## Non-Claims

- Not validation, readiness, buyer-proof, or judgment-quality evidence;
  product-learning grade.
- Authorizes no build, no model run, no live execution, no JSG-04/JSG-06
  clearance, no fixture admission.
- A behavior contract; the owning sources (the no-tools execution contract,
  `ContestantExecutionIsolation`, the conductor, the gate-ownership map) win on
  any conflict.
