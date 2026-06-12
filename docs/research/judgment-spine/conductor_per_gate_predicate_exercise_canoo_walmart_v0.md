# Conductor Per-Gate Predicate Exercise — Canoo/Walmart v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  By-hand docs-analysis that dry-evaluates each Judgment Spine conductor gate
  predicate (JSG-01 through JSG-10) against the real Canoo/Walmart case receipts,
  to (i) confirm each predicate is mechanically checkable against owner-produced
  receipt fields, (ii) record the dry-evaluation outcome reading the real
  receipts, (iii) map the machinery/receipt gaps that block each gate, and
  (iv) compare the hardened conductor's implied per-gate outcomes against the
  case's EXISTING jsg_08 reveal/calibration receipt and jsg_09_10
  classification/closeout. Product-learning cap. Not a run; not validation.
use_when:
  - Prioritizing the Judgment Spine machinery build (which gates cannot yet be
    exercised, and exactly what each needs).
  - Checking whether the hardened conductor's predicates are checkable against a
    real full-gate case before building runners.
  - Understanding why a strict sequential conductor walk halts at JSG-01 while
    the case nonetheless carries meaningful downstream receipts.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md
  - docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md
  - docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
  - docs/research/judgment-spine/cases/canoo-walmart/jsg_08_reveal_calibration_receipt_v0.md
  - docs/research/judgment-spine/cases/canoo-walmart/jsg_09_10_claim_classification_closeout_v0.md
input_hashes:
  docs/product/judgment_quality_promotion_operating_model_v0.md: 49739850CD2E156284D4E8B9ED29F2261FB5DFC84D469029C5F32A71B20E2F15
  docs/research/judgment-spine/cases/canoo-walmart/case_index.md: E940E1EE5B778DDEC0EDBAEB6F4E940C70935C3CFF9921CA61C7FA55AD4C7D46
  docs/research/judgment-spine/cases/canoo-walmart/source_packet_v0.md: 6E2BC0894A36C08B0712C8FE045DF812D3A8857E525CA4412832866FF405E473
  docs/research/judgment-spine/cases/canoo-walmart/participant_packet_v0.md: E0191512B1A5AD292C023304321B6FD870B4C1CF591DDFF8708ACC69D5B3324F
  docs/research/judgment-spine/cases/canoo-walmart/blind_judgments_v0.md: 2DF41433DCFACB31832CD51E65EC424888B7EB8955115D6949A35E8C7F2E8225
  docs/research/judgment-spine/cases/canoo-walmart/facilitator_ledger_v0.md: 6356C45D8E9B75732DB3D146EABFFCE4AD2775BCDD23D0205E26A46222FCE739
  docs/research/judgment-spine/cases/canoo-walmart/jsg_08_reveal_calibration_receipt_v0.md: 6DA7BBF5CF62BD3DE919E429E9F3C9C642FFDAD4B4B44F2F38F0E9CBBFFBB546
  docs/research/judgment-spine/cases/canoo-walmart/jsg_09_10_claim_classification_closeout_v0.md: CC7678A1412229EEAB74A3DA746F5A13F891ED822AA02D683B030F629AF554CD
read_branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 828482e (working tree dirty — concurrent-lane changes)
doctrine_change_check:
  finding: no_doctrine_change
  basis: >
    This artifact applies the existing conductor predicates, transition function,
    and ladder vocabulary to one real case as a read-only dry-evaluation. It
    changes no predicate, no transition rule, no ladder vocabulary, no gate
    ownership, and no lifecycle boundary. It is a satellite Research artifact, not
    a controlling source. No direction_change_propagation receipt is required, and
    it is intentionally not wired into the manifest or repo map.
stale_if:
  - Any input_hash above changes (re-read and re-evaluate).
  - The conductor changes its gate predicates, transition function, by-hand cap,
    or lifecycle states.
  - JSG-01 is unfrozen (the SP-1/2/3/6 derivers, the SP-5/AR-01 finalizer, and D2
    are built and a Canoo/Walmart packet carries the derived fields).
  - A contestant-execution runner, a memorization-probe run, or a JSG-07 scoring
    result is produced for Canoo/Walmart, changing what the execution gates read.
  - The evidence ladder changes closeout-state vocabulary, the weakest-cleared-gate
    rule, the sub-floor rule, or the minimum product-learning receipt fields.
```

## What This Is (And Is Not)

This is a **by-hand, read-only dry-evaluation** of the hardened conductor
(`judgment_quality_promotion_operating_model_v0.md`, hash `49739850…`,
post-Round-17) against the Canoo/Walmart case — the only in-repo case that
carries a full-gate receipt set. For each gate JSG-01→JSG-10 it records (a)
whether the predicate is *mechanically checkable* against the case's
owner-produced receipt fields, (b) the *dry-evaluation outcome* reading the real
receipt, and (c) the *machinery or receipt gap* that blocks the gate.

It is **docs-analysis only**. It is explicitly **not**:

- a run of the Judgment Spine (no model execution, no probe execution, no
  scoring, no fixture admission);
- validation, readiness, or judgment-quality evidence;
- a JSG-09 claim classification or JSG-10 closeout for the case (those already
  exist at `jsg_09_10_claim_classification_closeout_v0.md` and are not changed);
- an unfreezing of JSG-01 (JSG-01 stays FROZEN throughout).

The case ceiling is **product-learning context only**, capped three independent
ways (see "Case Ceiling" below). The sequential run-state below is marked
**illustrative**, not a claimed run.

## Method

The conductor's Seam 1 makes each gate clear-condition a mechanical read of an
owner-produced receipt field (exact field + allowed value), or
`indeterminate_until_authored` when the owner field is not yet authored. So each
gate predicate can be exercised *independently* against the case receipts —
distinct from the sequential transition function, which walks the gates in order
and halts at the first non-clear. This exercise runs the **independent per-gate**
pass (for gap-mapping) and then records what the **sequential** pass would do.

Receipts read (all hashes pinned above): the conductor; the case `case_index`,
`source_packet`, `participant_packet`, `blind_judgments`, `facilitator_ledger`,
`jsg_08_reveal_calibration_receipt`, `jsg_09_10_claim_classification_closeout`.
Absence of a memorization-probe artifact and a scoring-result artifact was
confirmed by directory listing of the case folder and the v0.14 fixture pack.

## Per-Gate Dry-Evaluation

| Gate | Field(s) the predicate reads | Present/readable in Canoo/Walmart? | Dry-eval outcome (reading the real receipt) | Machinery / receipt gap |
| --- | --- | --- | --- | --- |
| **JSG-01** | packing `pre_decision_status`; source-side ECR `source_identity_state` (SP-1), `inspectability_state` (SP-2), `PacketTiming.cutoff_posture` (SP-3), `source_visibility_posture` (SP-6) | **No.** `source_packet_v0` carries prose `cutoff_policy`/`recommended_cutoff` and a dated source manifest, but **none** of the derived SP-1/2/3/6 fields and **no** `pre_decision_status`. The substance (pre-cutoff sources, source identity) exists only as prose. | `indeterminate_until_authored` → **not cleared (FROZEN)**. Matches the conductor's own JSG-01 row exactly. | SP-1/2/3/6 **derivers**; the **SP-5 finalizer** (AR-01 Judgment-authority finalization — an open, unstaffed owner decision); **D2**; a packing `pre_decision_status` emitter. **Gating build.** |
| **JSG-02** | participant-packet freeze receipt present/valid per owner-enumerated fields; product-proof zero-spoiler boundary; packing participant-visible leakage/spoiler admission | **Partial.** `participant_packet_status: candidate_for_blind_judgment_capture` (not frozen); `blind_judgment_status: not_sealed`; a `review_consumed: accept_with_friction` block (AR-01..05). No in-packet freeze hash (the packet's own hash `E0191512…` is pinned only by *downstream* artifacts); leakage/spoiler admission and semantic-leakage are not machine fields. | **not cleared / indeterminate.** Status is "candidate," the freeze receipt is not present-and-valid as machine fields, semantic-leakage is `indeterminate_until_authored`. No affirmative leakage/spoiler block-class failure recorded → **not contamination**. | Owner-enumerated participant-packet **freeze-receipt schema** (in-packet freeze hash + packing leakage/spoiler admission fields + the semantic-leakage admission fields). The zero-spoiler review was done by hand; the machine receipt fields are unauthored. |
| **JSG-03** | frozen **band-input** FacilitatorLedger present/valid (authors, version pins, enum-valid band inputs, `second_label_diffs`); `ledger_freeze_hash` | **No (role mismatch).** The case `facilitator_ledger_v0` is the **reveal/outcome** ledger (`created_facilitator_only`; F-01/F-02/F-03 actual-action + agreement + outcome sources; contrast hooks). It carries **no** `ledger_freeze_hash`, no band inputs, no version pins, no `second_label_diffs`. | `indeterminate_until_authored` → **not cleared.** The case has the reveal/outcome ledger, not the JSG-03 frozen band-input FacilitatorLedger the predicate reads. | A JSG-03 **frozen band-input FacilitatorLedger** (band labeling for scoring). A draft adjacent artifact exists in the *blocked* v0.14 fixture pack (`facilitator_ledger_draft_v0.md`); no cleared case-side JSG-03 receipt. **Naming-collision finding** — see below. |
| **JSG-04** | `isolation_result == "proven"` **and** auditable live-execution provenance (provider, endpoint, UTC timestamp, exit status, console, `prompt_hash`, `raw_response_hash`) | **Yes — and reads not-cleared.** `blind_judgments_v0` is `sealed_user_supplied_blind_llm_result`, `capture_method: user_pasted_from_separate_blind_llm_thread`, `strict_cleanliness_claim: user_supplied_not_independently_verified`. There is **no** `isolation_result` field and **no** provenance fields. | **not cleared** (required fields absent — mechanically determinable without judgment). Absence → **not contamination** → by-hand product-learning cap (Seam 3). Matches existing closeout's "JSG-04 not_cleared." | **Contestant-execution runner** that emits auditable live-execution provenance. Harness reality: no such runner; `run_case.py` scores a *pre-supplied* blind judgment. **Lifts the by-hand cap.** |
| **JSG-05** | gate-interpretation `== pass_valid` read from the **probe artifact**, bound by JSG-04 live provenance | **No (receipt absent).** No memorization-probe artifact exists in the case folder or fixture pack; `band_scorer` hardcodes `memorization_probe_result="not_run"`. | `indeterminate_until_authored` → **not cleared.** Not the confirmed-recognition-with-proven-isolation state → **not contamination.** | A **memorization-probe runner + artifact** (and JSG-04 provenance). Additionally constrained by case selection: Canoo/Walmart is a **2022 pre-cutoff** case — recognition-prone — which the conductor's posture names a poor judgment-quality target regardless of machinery. |
| **JSG-06** | JSG-04 cleared **and** `isolation_result == "proven"` w/ inherited provenance **and** sealed blind-judgment hash present | **Partial.** Sealed blind-output hash **is** present (`blind_judgments_v0` = `2DF41433…`; `sealed_before_reveal: yes` per jsg_08). But JSG-04 is not cleared and there is no `isolation_result == proven`. | **not cleared** (depends on JSG-04; no isolation proof). Matches existing closeout's "JSG-06 not_cleared." Absence → **not contamination.** | Same as JSG-04 (runner + isolation provenance). The seal itself exists; the missing piece is clean isolation proof. |
| **JSG-07** | scoring receipt present/valid (phase-1 version/hash guardrails; packing frozen-input/deterministic-checking; scorer `ScoringResult`/`FailureEvent`); `severity == "blocking"` blocks | **No (receipt absent).** `jsg_08` records `jsg_07_scoring_result: not_scored`, `score_use: none_qualitative_only`. No `ScoringResult`/`FailureEvent` artifact exists. | **not cleared** (scoring absent). Matches existing closeout's "JSG-07 not_present." Absence → **not contamination.** The scoring-integrity-vs-admission contamination discriminator is itself `indeterminate_until_authored` (per the conductor; `FailureEvent.failure_type` is free text). | A **JSG-07 scoring run** (requires a clean blind judgment from the runner + a frozen band-input ledger from JSG-03). Even the existing plumbing was not exercised to record a `ScoringResult` for this case. |
| **JSG-08** | owner-contract Required Receipt Fields complete; `receipt_status == score_linked_outcome_calibration`; `sealed_before_reveal == yes` (for judgment-quality strength) | **Yes — fully checkable.** `jsg_08_reveal_calibration_receipt_v0` exists with owner-enumerated fields populated: `receipt_status: qualitative_outcome_calibration`, `sealed_before_reveal: yes`, `case_id`, `receipt_artifact`, `sealed_blind_output`, `reveal_event`, `calibration_frame`, `comparison_inputs`, `scoring_relationship: not_scored`, `missing_evidence`, `failure_events` (none as contamination), `claim_cap`. | **not cleared at judgment-quality strength** — `receipt_status` is the **valid but weaker** `qualitative_outcome_calibration` (≠ `score_linked_outcome_calibration`), so it caps lower per the contract. `sealed_before_reveal == yes` → **no seal breach**, **not contamination**, **not held** (status is not `absent`). | To clear at judgment-quality strength requires `score_linked_outcome_calibration` → a JSG-07 score → the JSG-04/05/06 clean-execution chain. **The downstream receipt machinery itself works by hand at this gate.** |
| **JSG-09** | classification record present/complete per the ladder `judgment_spine_claim_classification` schema; `claim_cap` owner-consistent | **Yes.** `jsg_09_10_…` carries a complete classification block (`evaluated_claim_surface`, `source_quality_state`, `execution_quality_state`, `closeout_state`, `claim_cap`, `weakest_missing_or_failed_gate`, `receipt_artifact_or_gap`). | **cleared** — a complete, owner-consistent classification record exists. | None for the artifact's existence; it classifies at the product-learning floor. |
| **JSG-10** | `closeout_state` present, drawn from ladder vocabulary; `claim_cap` owner-consistent | **Yes.** Same artifact records `closeout_state: unreceipted_product_learning_context` (valid ladder state) + `claim_cap: qualitative_case_learning_or_product_learning_context_only`. | **cleared** — closeout recorded at the product-learning floor. | None for the artifact's existence. |

### Checkability tally

- **Fully checkable, receipt present:** JSG-08, JSG-09, JSG-10 (the
  reveal/calibration + classification/closeout machinery works by hand today).
- **Checkable, reads not-cleared by mechanical absence:** JSG-04, JSG-06
  (partial — sealed hash present).
- **Receipt absent / role-mismatched → `indeterminate_until_authored`:** JSG-01
  (derived fields unbuilt), JSG-03 (case has reveal ledger, not band-input
  ledger), JSG-05 (no probe artifact), JSG-07 (not scored).
- **Partial:** JSG-02 (candidate packet + by-hand review, but no machine
  freeze-receipt fields).

**Every predicate proved evaluable without conductor judgment** — each gate
resolved to cleared / not-cleared / indeterminate by a mechanical field read.
Seam 1 holds against a real case.

## Illustrative Sequential Run-State (NOT a run)

Walking the conductor's transition function in order over Canoo/Walmart:

- **JSG-01 evaluated first** → `indeterminate_until_authored` (FROZEN) →
  `else_not_cleared_or_indeterminate`: **halt at JSG-01**, do not advance.
- Weakest cleared gate among JSG-01..JSG-08 = **none** (JSG-01 is first and does
  not clear).
- Route the final cap through JSG-09/JSG-10 using the ladder cap rule; name the
  indeterminate gate **JSG-01**.
- Run state: **`halted_at_JSG-01`** (ordinary not-cleared; no contamination).
- Realized closeout selected by product-learning-receipt completeness (Seam 3):
  durable case artifacts exist but the minimum product-learning receipt is
  incomplete → **`unreceipted_product_learning_context`**, **claim cap =
  product-learning**.

A strict run therefore **never reaches JSG-02..JSG-10**; the rich downstream
receipts (JSG-08/09/10) are only visible to the independent per-gate pass above.
This is correct conductor behavior, and it is the central usability finding (see
synthesis).

## Hardened Conductor vs. Existing Canoo/Walmart Closeout

The case already carries an independently-authored `jsg_09_10` closeout (on
`main @ d868fc2e`). Comparing what the hardened conductor implies against what
that closeout recorded is the sharpest test of the Round-17 patch:

**Agreements (strong corroboration):**

1. **Closeout state — AGREE.** Both land at
   `unreceipted_product_learning_context`. The conductor's Seam-3 realized-state
   selection (by product-learning-receipt completeness) and the existing
   closeout's matrix-row reasoning reach the identical state.
2. **Claim cap — AGREE.** Both cap at product-learning context only.
3. **Absence-is-not-contamination — AGREE, verbatim in spirit.** The existing
   closeout's "Why not blocked_or_contaminated" rationale ("execution-process
   gaps … rather than a material defect that breaks the evaluated gate") is
   exactly the conductor's rule that absence / by-hand / unproven isolation
   routes to not-cleared, never to `blocked_or_contaminated`. The Round-17 F3/F4
   hardening (withdrawing the under-specified JSG-07 contamination trigger;
   restoring the `isolation_result == proven` qualifier) is consistent with how
   the case was actually classified.
4. **Cap is path-robust.** The sequential halt (JSG-01) and the existing
   closeout (JSG-04/06/07) reach the **same** product-learning cap by different
   routes — no single gate's resolution changes the ceiling.

**Divergence (informative, not a contradiction):**

- **Named blocker gate differs.** A strict conductor walk *today* names
  **JSG-01** (the first frozen gate, a source-side schema-maturity halt). The
  existing closeout names **JSG-04/JSG-06/JSG-07** (the execution-quality and
  scoring blockers). Both are true. The sequential function surfaces only the
  *first* blocker; the existing closeout (and the per-gate pass) surface the
  *execution-quality* blockers that a run would only formally reach if JSG-01
  cleared. For a **gap map**, you want both attributions; for a **run**, the
  conductor correctly stops at the first.

**Net:** the hardened conductor's implied outcomes agree with the existing
hand-authored closeout on every load-bearing point (state, cap, contamination
handling) and add no contradiction. The exercise **opened no new seam** and the
four seams + Invariant A/B held against a real case.

## Synthesis

1. **Per-gate dry-evaluation is the right tool for machinery-gap mapping; the
   sequential walk is the right tool for running a case.** The sequential
   function correctly halts at JSG-01 and would mask every downstream gap. The
   independent per-gate pass (which Seam 1 makes possible) is what reveals the
   full build backlog. This is a usage distinction, **not** a conductor defect —
   the conductor behaves exactly as specified.
2. **The downstream classification machinery already works by hand**
   (JSG-08/09/10 are fully checkable with complete receipts). The entire gap is
   **upstream**: source-side derivation (JSG-01) and clean execution +
   scoring (JSG-04/05/06/07).

## Machinery-Gap Map (prioritized build backlog)

1. **JSG-01 source-side machinery (gating).** SP-1/2/3/6 derivers + the SP-5/AR-01
   Judgment-authority finalizer (open, unstaffed owner decision) + D2 + a packing
   `pre_decision_status` emitter. *Nothing runs end-to-end through the conductor
   until this clears.*
2. **Contestant-execution runner with auditable live-execution provenance.**
   Unblocks JSG-04, JSG-05, JSG-06; lifts the by-hand product-learning cap.
3. **Memorization-probe runner + artifact (JSG-05).** Mandatory non-recognition
   verifier. Note: a **post-cutoff case** is required for a judgment-quality
   target; Canoo/Walmart (2022) cannot be promoted past product-learning even
   with full machinery.
4. **JSG-07 scoring run.** Requires #2 (clean blind judgment) + a frozen
   band-input FacilitatorLedger (item 6).
5. **JSG-02 participant-packet freeze-receipt schema** (in-packet freeze hash +
   packing leakage/spoiler admission fields + semantic-leakage admission fields).
6. **JSG-03 frozen band-input FacilitatorLedger** (authors, version pins,
   enum-valid band inputs, `second_label_diffs`) — distinct from the existing
   reveal/outcome ledger.
7. **JSG-07 scoring-integrity contamination discriminator** owner enum
   (constrain `FailureEvent.failure_type`) — lifts the JSG-07 contamination
   `indeterminate_until_authored`.

Already complete for this case (no build needed): JSG-08 reveal/calibration
receipt, JSG-09 classification, JSG-10 closeout.

## Findings Worth Naming

- **Naming-collision (JSG-03).** "Facilitator ledger" denotes two different gate
  roles: the JSG-03 **frozen band-input** FacilitatorLedger (scoring inputs) and
  the case's **reveal/outcome** facilitator ledger. The case carries the latter;
  the former does not exist case-side. A future reader could mistake one for the
  other. (Observation only; no edit proposed here.)
- **Case ceiling = product-learning, three independent ways.** (a) by-hand
  execution cannot bind provenance → Seam-3 cap; (b) case-selection posture —
  2022 pre-cutoff, recognition-prone, JSG-05; (c) the existing `jsg_09_10`
  closeout. Building the machinery enables the **path** (validated here); it does
  **not** promote Canoo/Walmart to judgment-quality. A post-cutoff case is
  required for that.

## Non-Claims

- Not a run of the Judgment Spine; no model execution, probe execution, scoring,
  or fixture admission was performed or authorized.
- Not validation, not readiness, not buyer proof, not judgment-quality evidence.
- Not a JSG-09 classification or JSG-10 closeout for the case; the existing
  `jsg_09_10_claim_classification_closeout_v0.md` is unchanged.
- JSG-01 stays FROZEN; this exercise does not unfreeze it.
- The sequential run-state above is **illustrative**, not a claimed run.
- The case ceiling is product-learning context only.
- Not a controlling source; no doctrine change; no `direction_change_propagation`
  receipt; not wired into the manifest or repo map.
- Not an implementation, runtime, test, deployment, commit, push, or PR
  authorization.
```
