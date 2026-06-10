# Delegated Review-and-Patch Commission — Judgment Conductor (`no_repo` / advisory)

```yaml
retrieval_header_version: 1
artifact_role: Review-input bundle brief (delegated review-and-patch commission; no_repo, advisory)
scope: >
  Self-contained commission brief, fitness reference, owner-source map, and findings-only output
  contract shipped inside the no_repo delegated-review bundle for the judgment conductor; orients a
  repo-blind reviewer. Not Orca authority; advisory only.
use_when:
  - Running the commissioned no_repo adversarial review of the judgment conductor from this bundle.
  - Checking the review's fitness reference, owner-source map, known residuals, or output contract.
authority_boundary: retrieval_only
```

> This brief travels inside the bundle so it is self-contained for a reviewer with **no repo access**.
> Governing convention: Orca `.agents/workflow-overlay/delegated-review-patch.md` (provisional, `no_repo` mode).

## What this is

A **de-correlated, no-repo adversarial artifact review** of ONE high-stakes Orca artifact: the
**Judgment Quality Promotion Operating Model** ("the conductor"). You have **no repo access** —
everything you need is in this bundle (`sources/`). You return **FINDINGS ONLY** — no diff, no patch.
The commissioning home model (the author's lane) adjudicates every finding, applies any accepted change
itself within bounded scope, and then commissions a **separate de-correlated post-patch re-review** before
anything is kept.

## Review target

`sources/judgment_quality_promotion_operating_model_v0.md` — a case-agnostic conductor that sequences
Judgment Spine gates **JSG-01 → JSG-10** over owner-produced receipts. It is supposed to *route and verify
receipts*, never to compute judgment quality.

## Decision criteria / fitness reference (ATTACK axes — NOT pass-if-matches bars)

The conductor's goal is to be airtight on **four seams** and to **survive this review with NO new seam**.
Attack each; treat the reference as something to break, not a checklist to confirm.

1. **Seam 1 — mechanical predicate, no LLM discretion.** Every gate clear-condition must be a mechanical read
   of an owner-produced receipt field (exact field + allowed value). No predicate may require judgment.
   Hunt for discretion smuggled in (e.g. "complete per the routed owner sources" completeness-judgments).
2. **Seam 2 — total fail/blocked transitions.** The transition function must be total over
   `[cleared, contaminated_or_blocked, held, not_cleared_or_indeterminate]`, name the affected gate, and cap
   correctly: weakest-cleared for not-cleared; the `blocked_or_contaminated` cap for **affirmative**
   contamination (NOT weakest-cleared). Hunt for undefined/contradictory routing, or **absence mis-routed as
   contamination**.
3. **Seam 3 — by-hand isolation cap.** By-hand JSG-04/05/06 cannot bind auditable live-execution provenance →
   cannot clear at judgment-quality strength → the run **caps at product-learning**. Hunt for any path that
   lets a by-hand / self-asserted receipt clear, or over-claims above product-learning.
4. **Seam 4 — named `sealed_awaiting_outcome`.** A live post-cutoff case with no outcome is **held** (not
   failed, not closed), resolves to an existing ladder state, and mints **no new** claim vocabulary. Hunt for
   lifecycle states that invent vocabulary or mis-resolve to the ladder.

Plus two invariants:

- **Invariant A (no-authority):** the conductor is subject/assistant, **never the gavel**. A gate that needs
  the conductor to exercise judgment to clear is NOT cleared. Verdicts, scores, and claim tiers live in their
  owner sources, never in the conductor.
- **Invariant B (route-don't-restate):** the conductor holds **only** routing/lifecycle. Every predicate must
  check an OWNER-produced field and cite the owner; it must never duplicate, paraphrase, or contradict owner
  semantics. **Restatement, paraphrase-clear, or contradiction of an owner source is a finding** — verify each
  predicate against the provided owner source.

**Success signal:** this review opens **no new seam** (and confirms the four hold).

## Owner sources provided (verify route-don't-restate fidelity against these)

| Bundle file (`sources/`) | Original repo path | What it owns |
| --- | --- | --- |
| `judgment_quality_promotion_operating_model_v0.md` | docs/product/ | **THE TARGET** (conductor) |
| `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | docs/product/ | JSG-01 owner surface — pipeline Capture→ECR→Cleaning→Judgment (ECR is pre-cleaning) |
| `core_spine_v0_data_capture_spine_obligation_contract_v0.md` | docs/product/ | JSG-01 source-identity obligation owner; explicitly does NOT define ECR fields/schema |
| `judgment_spine_evidence_ladder_architecture_v0.md` | docs/product/ | claim tiers, closeout states, weakest-cleared-gate, sub-floor |
| `judgment_spine_gate_ownership_map_v0.md` | docs/product/ | gate ownership, required receipts, gate dependencies |
| `judgment_spine_reveal_calibration_owner_contract_v0.md` | docs/product/ | JSG-08 satisfaction states + required receipt fields |
| `contestant_no_tools_execution_contract_v0.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-04/05/06 isolation + live-execution provenance boundary |
| `memorization_probe_protocol.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-05 recognition-verdict semantics |
| `phase_1_infrastructure_architecture.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-07 scorer / version / hash guardrails |
| `packing_to_harness_foundation_interface_architecture_v3.md` | docs/research/judgment-spine/harness/v0_14/ | frozen packet/ledger + deterministic-checking boundary |
| `band_input_labeling_rubric.md` | docs/research/judgment-spine/harness/v0_14/ | JSG-03 ledger band inputs |
| `validation-gates.md` | .agents/workflow-overlay/ | the **"Receipt-field provenance gate"** the conductor's Seam-1 sub-rule cites |
| `product-proof.md` | .agents/workflow-overlay/ | JSG-02 zero-spoiler participant boundary |
| `band_scorer.py` | orca-harness/scoring/ | Seam-3 reality: hardcodes `memorization_probe_result="not_run"` |
| `run_case.py` | orca-harness/runners/ | Seam-3 reality: scores a pre-supplied blind judgment; executes no contestant |
| `scoring_models.py` | orca-harness/schemas/ | JSG-07 schema — defines `ScoringResult`/`FailureEvent` (load-bearing for the JSG-07 scoring-integrity discriminator) |

## Scoped-out surfaces (NOT predicate owners — do NOT block on these)

Bundle **revision 2** added the three JSG-01 / JSG-07 predicate-owner sources above after a no-repo
reviewer correctly returned `SOURCE_CONTEXT_INCOMPLETE`. The following are intentionally **excluded**
and must **not** trigger another `SOURCE_CONTEXT_INCOMPLETE`: the conductor cites them only as
`downstream_consumers`, `input_hashes` provenance pins, `stale_language_search` targets, or
`downstream_surfaces_checked` — the dependency points the **other way** (they consume or record the
conductor; no gate predicate routes to them), and they sit outside this commission's bounded scope (the
four seams + Invariant A/B, not wiring/provenance bookkeeping):
`.agents/workflow-overlay/source-loading.md`, `docs/workflows/orca_repo_map_v0.md`,
`docs/research/judgment-spine/manifest_v0.md`, `AGENTS.md`, `.agents/workflow-overlay/README.md`,
`.agents/workflow-overlay/source-of-truth.md`. The ECR source-identity field-schema owner is
intentionally **nonexistent**; verify JSG-01 correctly routes those sub-predicates to
`indeterminate_until_authored` (confirm against the obligation contract, which defines no ECR fields).
Declare `SOURCE_CONTEXT_READY` once the `sources/` owner set is read.

## Known residuals (probe adversarially — do NOT just confirm; also look beyond them)

1. **JSG-07 scoring-integrity contamination discriminator** — churned across rounds 9/11/13/16, currently
   parked `indeterminate_until_authored`. Is the *current* state self-consistent and owner-grounded?
2. **"complete per the routed owner sources"** predicates (JSG-02/03/07) — does verifying "completeness"
   require conductor judgment (an Invariant A leak)?
3. **Stale self-note** — the conductor's Round-14 propagation note says the gate-ownership-map "lossy
   restatement … is NOT changed here," but a later Round-15 gate-map patch fixed it; the note now reads stale.
4. **Stale `input_hashes`** — the conductor's pinned hashes were computed on a dirty worktree; the bundled
   `00_HASH_MANIFEST.txt` records the **actual current bytes** you are reviewing. Review the bytes, not the pins.

## Output contract (`no_repo` / advisory)

Return **FINDINGS ONLY**. For each finding:

- `title`
- `severity`: `critical` | `major` | `minor` (priority only — you hold **no** formal verdict/validation authority)
- `location`: exact conductor section / line
- `seam_or_invariant_broken`
- `evidence`: cite the provided owner-source file + section — **neutral in tone, decision-sufficient in substance**
- `minimum_closure_condition`: the required end state (not how to implement it)
- `next_authorized_action`

Then a `residual_risk` note and an explicit **`NEW_SEAMS`** section (anything beyond the four seams + the four
known residuals).

**Do NOT emit:** a unified diff, a patch, `PASS`/ready/validated/approved claims, severity as authority, or any
runtime-model recommendation.

## Boundaries

- This is **advisory** (`no_repo`): de-correlated review only. The home/CA model adjudicates every finding,
  applies any accepted change within bounded scope, and runs a **required de-correlated post-patch re-review**
  before anything is kept.
- **De-correlation (operator note):** review this with a **different, non-Opus model family** than the author
  (author = Claude Opus-class). This is a commission who-constraint, **not** a model recommendation.
- Confirm the bytes you reviewed against `00_HASH_MANIFEST.txt`.
