# Prospective Decision Loop — Phase-1 Dogfood Pilot Ledger v0 (DRAFT, awaiting owner signature)

```yaml
retrieval_header_version: 1
artifact_role: DRAFT decision record (pre-declared dogfood shadow pilot ledger; binds nothing and authorizes no seal until the owner fixes the decision list, binds the ledger home, and signs)
scope: >
  Pre-declared ledger for the Phase-1 dogfood shadow pilot of the prospective
  decision loop: the counterparty-free first run, on real Orca-INTERNAL
  operating decisions, by hand, shadow mode only. Pre-commits the decision set,
  per-decision mode, selection criteria, run discipline, and report-all rule
  before any outcome is knowable. Caps at product-learning. Its PURPOSE is
  protocol falsification (does the book survive a real intake -> seal ->
  resolve?), not evidence accumulation.
use_when:
  - Deciding whether to authorize, amend, or sign the Phase-1 dogfood pilot.
  - Running, sealing, or resolving any pilot decision once signed.
  - Checking what the pilot may claim and what fixing/signing it commits.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_phase0_semantics_spec_v0.md
  - forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md
input_hashes:
  docs/product/judgment_spine/prospective_decision_loop_phase0_semantics_spec_v0.md: <FILL_AT_SIGNATURE — blob-bytes SHA256 of the spec at the signing commit>
branch_or_commit: prospective-loop-phase1-pilot-ledger-v0 off origin/main @ d6d360e (semantics spec landed via PR #46; target architecture via PR #34)
stale_if:
  - The owner signs (status advances; this draft's open slots are filled by dated amendment, never silent rewrite).
  - The semantics spec or target architecture is amended (re-pin input_hashes; reconcile the run shape).
  - The owner ratifies/amends/rejects the target architecture (update the authorization basis line).
```

## Status

`DRAFT_PENDING_OWNER_SIGNOFF` — a draft-local label, not an evidence-ladder
closeout_state or claim tier. This artifact **authorizes no seal**. Two
owner-owned inputs are unfilled by design (the decision list and the per-decision
mode); the agent must not invent them. Signing = fixing those slots + the
sign-off block below + the ledger-home binding amendment. Until then nothing in
the loop may be sealed.

## Authorization Basis And Cap

- **Consumes:** the Phase-0 semantics spec ("the book") and the target
  architecture, both landed on `main`. The pilot runs the book as written; it
  re-derives no semantics.
- **Ratification dependency (open):** the target architecture is landed but the
  owner's explicit ratify/amend/reject statement is still pending (see Owner
  Decisions Required). The pilot is a DRAFT regardless; if the owner signs while
  the target is unratified, the pilot is explicitly a **PROPOSED-stack**
  product-learning exercise and its results cannot be cited above that until the
  target is ratified.
- **Covers (once signed):** by-hand intake, org-blind sealed calls, passive
  actual-path observation, and mechanical resolution of a pre-declared set of
  real Orca-internal operating decisions, **shadow mode only**, at
  product-learning tier.
- **Does NOT cover:** assisted mode (deferred — needs the disclosure machinery
  and a counterparty per the architecture); any external counterparty; any
  code, storage, tooling, or integration (the entire counterparty-blocked
  B-column stays blocked); promotion of any result above product-learning;
  binding the ledger-home folder (a separate artifact-folders amendment, below).
- **Claim cap:** product-learning per the evidence ladder; the by-hand surface
  is permanently non-gate-clearing per the pre-sale execution evidence-tier
  policy. The pilot's existence proves selection discipline only — never result
  quality.

## Pilot Design (pre-committed before any outcome is knowable)

These rules are fixed **now**, in the draft, so that — exactly as the batch-1
org-motion pre-commitment established — inclusion cannot correlate with
favorability:

- **Shadow only.** The org (Orca) decides normally; the sealed call stays dark
  until that decision's resolution. No decision is disclosed before its seal.
- **Org-blind sealing.** Each sealed call is authored by a sealing actor given
  only the decision brief (`frame`) — the norm is an **org-blind subagent**, not
  the same human who owns the decision. The single-operator memory bridge (owner
  = decision owner = pilot operator) is a **named, disclosed residual** at
  product-learning tier, not a gate (per the architecture's owner-decision-4).
- **Pre-declared set, report-all.** Every decision intaken under this ledger is
  reported at resolution — in-band / over / under, plus `unscoreable_by_design`,
  abandoned, and `breached_quarantined` outcomes. Selective reporting voids the
  pilot's anti-cherry-pick property.
- **Run shape mirrors the book — by pointer, not restatement.** Each decision
  is one folder of write-once hash-chained entries exactly as the Phase-0
  semantics spec's "The Book: Entry Mechanics" section defines, under that
  spec's chain rule. The pilot **restates no entry filenames and forks
  nothing**: whatever that section defines at the consumed spec revision
  governs, and `input_hashes` pins that revision at signature. Sign against the
  **adjudication-hardened spec revision** (the AR-01 vocabulary fix + the AR-02
  `actual_path`-observation / per-seal-resolution / dual-hash chain), which must
  be on `main` before first seal (see Owner Decisions Required). The pilot does
  **not** re-derive the chain shape. (Restating filenames here was the original
  AR-1 defect and is deliberately not reintroduced.)
- **Mechanical resolution.** Resolution applies the `resolution_criteria` sealed
  into each call; it never authors or amends them. A decision whose outcome
  criterion cannot be pre-specified is admitted as `unscoreable_by_design` —
  logged for decision-memory, permanently excluded from calibration.

## Decision Selection Criteria (the bar each pilot decision must clear)

A candidate decision qualifies for the pre-declared set only if **all** hold:

1. **Real and live** — an actual Orca operating decision with a genuine owner
   and a near-term `decision_deadline`, not a hypothetical.
2. **Outcome-declarable** — its `expected_outcome` either admits a named
   observable metric, a predicted band, and a measurement window that closes in
   a tractable horizon, or is explicitly admitted at signature as
   `unscoreable_by_design` for protocol-falsification / decision-memory only.
   `unscoreable_by_design` rows are reported but never count toward the
   calibration set.
3. **Not self-referential** — not a decision *about the loop itself* (e.g., "do
   we build N9", "do we ratify the target"). Shadowing the loop's own
   governance would contaminate the pilot with reflexivity. Pilot decisions are
   ordinary Orca product/research/operating calls.
4. **Decision and outcome not yet knowable at intake** — the org decision has
   not been made or irreversibly committed, and its outcome has not begun
   arriving, so both the sealed call and the passive actual-path observation are
   genuinely prospective.
5. **Owner-fixed before reveal** — the full set is fixed at signature, before
   any member's expected direction, actual path, or outcome signal is examined
   for favorable alignment, so membership cannot correlate with favorability.

## Pre-Declared Decision Set (OWNER-FILL — do not fabricate)

> The agent has intentionally left this list empty. These are real Orca
> operating decisions only the owner can name. Fill 3–5 rows (suggested range;
> owner fixes N) at signature, fix the per-decision mode (`shadow` for Phase 1),
> bind the ledger home, then the set is frozen and amended only by dated note.

| # | Decision (one-line brief) | Decision family | Mode | Decision deadline | Scoreable? (Y / unscoreable_by_design) |
| --- | --- | --- | --- | --- | --- |
| 1 | `<owner-fill>` | `<owner-fill>` | shadow | `<owner-fill>` | `<owner-fill>` |
| 2 | `<owner-fill>` | `<owner-fill>` | shadow | `<owner-fill>` | `<owner-fill>` |
| 3 | `<owner-fill>` | `<owner-fill>` | shadow | `<owner-fill>` | `<owner-fill>` |
| … | `<add rows to owner-chosen N>` | | shadow | | |

Candidate-shape illustrations (NOT pre-selected; the owner replaces or confirms
— offered only to show the criteria in use, carry no commitment, and must not be
treated as a fixed set): a near-term research-direction call with a measurable
yield (e.g., a batch-2 screening priority — though reusing the spec's worked
example verbatim is discouraged, to keep illustration and evidence separate); a
pricing or packaging direction call with an observable downstream signal; a
build-sequencing call with a measurable completion/throughput outcome. Each
would still have to clear all five criteria above at signature.

## Execution Rules (apply once signed)

- Contestant/sealing runs happen only in fresh isolated sessions (org-blind
  subagent or fresh chat surface); the sealing actor sees only the `frame`.
- The planning/operating thread is outcome-aware for the org's actual path; no
  sealed call may be primed from it.
- One folder of chained entries per decision under the ledger home; `index.md`
  carries one line per entry (decision_id → file → blob-hash → status).
- Resolution closes each decision at its measurement window with the mechanical
  score and the learning-extraction rows (signal-reliability rows accumulate
  toward the pending near-half interface; lesson candidates route to near-half
  validation, never self-adopted).
- Breach route: any edit to a hashed entry, any mode declared after seal, any
  disclosure (N/A in shadow) before seal, or any post-outcome criteria edit →
  append a quarantine entry, set `firewall_state: breached_quarantined`, keep
  everything.

## Closing Artifact

The pilot closes with one distillation record: did the book survive real intake
→ seal → resolve without invented semantics (the protocol-falsification
verdict); per-decision in/over/under and `unscoreable_by_design` counts; the
first calibration rows; signal-reliability rows emitted toward the near-half
ledger; book-friction findings and any proposed (not applied) semantics
amendments (owner-gated); and the single-operator-residual honesty note.

## Owner Decisions Required (surfaced, not assumed)

1. **Ratification of the target architecture** (open since it landed): ratify,
   amend, or leave PROPOSED. Sets the pilot's authorization-basis line; the
   pilot can run either way but its claim ceiling differs.
2. **The decision list + per-decision mode** (the OWNER-FILL table): the real
   Orca-internal decisions to shadow, fixed before reveal.
3. **Ledger-home binding:** the semantics spec proposes
   `docs/product/judgment_spine/decision_ledger/` with a permanent
   location-confers-no-evidence-tier boundary. Binding it is a separate
   `artifact-folders.md` amendment with its own propagation receipt, executed at
   signature — not by this draft. No first seal is authorized while
   `ledger_home_bound` remains false.
4. **Adjudication-hardened spec must be on `main` (no-seal precondition):** the
   Phase-0 semantics spec's cross-vendor adjudication (AR-01 vocabulary fix +
   AR-02 chain hardening) was dropped by the PR #46 squash-merge; `main`
   currently carries the pre-adjudication spec. It is being re-landed via a
   separate PR. The pilot's run-shape pointer resolves to the hardened spec only
   once that PR lands; **no first seal while `main` carries the un-hardened
   spec.** `input_hashes` is pinned at signature to the hardened revision.
5. **Recommended gate before first seal:** a de-correlated cross-vendor review
   of this ledger's doctrine (authorization basis, selection criteria,
   anti-cherry-pick completeness, firewall-preservation) plus a post-fill check
   of the chosen decision list for scoreability and cherry-pick discipline. The
   prior two slices each had a finding only the cross-vendor pass caught;
   running it before the first real seal is cheap insurance.

## Sign-Off Block (OWNER-FILL at signature)

```yaml
pilot_signoff:
  status: DRAFT_PENDING_OWNER_SIGNOFF   # advance only after table fixed + ledger_home_bound true + owner signature
  owner: <owner-fill>
  signoff_date: <owner-fill>
  target_ratification_state: ratified | amended | proposed_stack   # owner decision 1
  decision_set_fixed: false   # -> true when the table is filled and frozen
  ledger_home_bound: false    # -> true when the artifact-folders amendment lands
  pre_first_seal_review: not_run | waived_with_reason | completed   # owner decision 4
  non_claims_affirmed: true
```

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: Phase-1 dogfood pilot ledger (DRAFT pre-declaration; no run exists)
  source_quality_state: design/control artifacts only (semantics spec + target architecture, landed; no decisions fixed)
  execution_quality_state: no run, no seal, no resolution; the decision set is unfilled
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: unsigned; decision set unfilled; target ratification pending; prospective gate family unauthored
  receipt_artifact_or_gap: first receipts would be chained entries under the signed ledger home
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Non-Claims

- This draft authorizes no seal, no run, and no pilot; it is unsigned and its
  decision set is unfilled.
- Signing it is a product-learning dogfood authorization only — not validation,
  readiness, ratification of the target, buyer proof, or judgment-quality.
- The pilot's purpose is protocol falsification at small N; its calibration
  output is weak by construction and is not a judgment-quality claim.
- Mints no evidence-ladder or ledger vocabulary; `shadow`, the decision-object
  shape, and the chain mechanics remain owned by the architecture and spec.
- The near-half interface stays `pending_interface`; the pilot emits rows toward
  it but does not create the reliability ledger or validate any lesson.
- The candidate-shape illustrations are not a pre-selected set and carry no
  commitment.
```
