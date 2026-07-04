# JSG-01 Source-Side Receipt Translator v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Proposed first slice of the deferred ECR/EvidenceUnit consolidation: names the
  minimal source-side fields and CLOSED allowed-values for JSG-01's
  source-identity, inspectability, timing/cutoff, and source-visibility posture
  subpredicates in IPF / Data-Capture canonical semantics, with a thin adapter to
  the v0.14 harness EvidenceUnit fields for existing fixtures only.
use_when:
  - Evaluating JSG-01 source-side subpredicates for a packed/fixture case.
  - Deciding whether a source-side ECR receipt is determinate or indeterminate.
  - Preparing the owner ratification of the JSG-01 source-side field slice.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
downstream_consumers:
  - docs/product/judgment_quality_promotion_operating_model_v0.md  # JSG-01 predicate row (reference proposed; not yet wired)
stale_if:
  - The owner ratifies, amends, or rejects this first slice.
  - The full ECR/EvidenceUnit field-architecture consolidation supersedes it.
  - core_spine_v0_information_production_foundation_v0.md changes the Evidence Unit Standard fields or states.
  - core_spine_v0_data_capture_spine_obligation_contract_v0.md changes source-identity, raw-observable/inspectability, timing, cutoff, archive/historical, or re-capture obligations.
  - packing_to_harness_foundation_interface_architecture_v3.md changes pre_decision_status ownership or the hash-verifiability handoff.
  - The v0.14 harness EvidenceUnit field set changes, or case_models.py / pydantic_schema_reference / fixtures are reconciled.
```

- Status: `PROPOSED_FIRST_SLICE_PATCHED_AWAITING_RESCOPED_REVIEW_AND_OWNER_RATIFICATION`
- Artifact type: Product-method interface (JSG-01 source-side receipt translator)
- Gate posture: **JSG-01 stays FROZEN (indeterminate).** Authoring/patching this
  artifact is not its ratification and does not unfreeze the gate.
- Implementation authorized: no. Validation/readiness: not claimed.

## Patch history

- **v0 (initial):** SP-1..SP-5 authored; Canoo/Walmart claimed to "clear
  source-side" with finalization as the single residual.
- **v0 patch (this revision), from independent adversarial review**
  (`docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md`,
  `recommendation: patch_before_acceptance`):
  - **AR-01 (was critical/blocking):** the Canoo "clears" result overclaimed —
    its hashes are over **2026 current/live captured bytes, not pre-cutoff
    archival bytes**, so byte-verifiability + a pre-cutoff publication date do
    **not** establish pre-cutoff *visibility*. Added **SP-6 source-visibility /
    pre-cutoff posture** (Ob.10/Ob.11/Ob.15 + IPF pre-cutoff visibility), which
    also carries the owner's archive-vs-current **comparison** as a recordable
    strength signal. Canoo is re-scored to `current_capture_only` (a visible
    limitation), not a clean clear.
  - **AR-02 (was major):** SP-1 `resolved` required an actor/audience category
    the harness EvidenceUnit cannot carry. Reconciled to Ob.7 ("mark actor when
    unavailable"); the replay now cites the actual identity evidence.
  - **AR-03 (was major):** `hash_basis` was wrongly called non-load-bearing.
    SP-2 now requires a recomputation-coverage basis (the `hash_basis` field or
    an owner-bound equivalent such as a source-acquisition receipt) for
    `inspectable_verifiable`.
  - **Honesty correction:** the v0 "shrinks to ONE residual (finalization)"
    claim was optimistic. The determinate source-side result now leaves **two**
    owner-reserved residuals: finalization authority (SP-5) and the
    visibility-sufficiency threshold (SP-6 grade).
  - SP numbering is preserved (SP-4 value, SP-5 finalization) for continuity with
    the v0 review; SP-6 is appended though it is logically a source-side sibling
    of SP-2/SP-3.

## Purpose

JSG-01's source-side subpredicates are `indeterminate_until_authored` because
"no ECR field schema exists yet" (conductor JSG-01 row,
`docs/product/judgment_quality_promotion_operating_model_v0.md`). This artifact is
a **translator**, not a bind and not a fork:

1. Names the minimal source-side fields + CLOSED allowed-values + cleared
   conditions in **IPF / Data-Capture canonical semantics** (the home the
   boundary doc says to cite until the consolidation — not the harness pydantic).
2. A thin **adapter** maps each authored field to the existing v0.14 harness
   `EvidenceUnit` fields, **for the current fixtures only**.
3. Is the **proposed first slice** of the deferred ECR/EvidenceUnit
   consolidation, requiring owner ratification before it is authoritative.

### Why a translator, not a bind to the harness pydantic

(Unchanged from v0; confirmed by the review as holding.) Binding the gate directly
to the harness pydantic was withdrawn: the boundary doc names the **IPF Evidence
Unit standard** as the cite-home until the consolidation; the harness pydantic is
a downstream consumer schema (`authority_boundary: retrieval_only`); flipping the
gate to determinate on an unratified field-home is a gate-integrity bypass. The
translator keeps IPF canonical and makes the harness the **adapter target**, not
the home.

## Canonical semantics source (authored FROM)

| Source | What it owns here |
| --- | --- |
| `core_spine_v0_information_production_foundation_v0.md` — Evidence Unit (EvidenceUnit) Standard | Source locator/family, actor/audience, event/publication + capture timestamps, pre-cutoff visibility, inspectable-observation requirement, Invalid/Blocked states. |
| `core_spine_v0_data_capture_spine_obligation_contract_v0.md` — Ob.7 (identity/actor), Ob.8 (decomposed timing), Ob.9 (cutoff posture), Ob.10 (archive/historical posture), Ob.11 (source visibility), Ob.12 (reconstruction floor), Ob.15 (re-capture supersede/supplement/conflict), Ob.16 (categorical handoff; does **not** define ECR fields) | Capture obligations; the closed cutoff vocabulary (Ob.9); the archive-posture vocabulary and "visible posture required, success not required, sufficiency downstream" rule (Ob.10); the re-capture relationship vocabulary (Ob.15). |
| `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` — Inclusion State Rule (Receipt/content blocker = ECR-owned; Capture/preservation blocker = "archive posture missing, source visibility cannot be established") | Which blockers are source-side; the cite-IPF-until-consolidation rule. |
| `packing_to_harness_foundation_interface_architecture_v3.md` — AR-01/03/04/05 | `pre_decision_status` is Judgment-finalized; source bytes / inspectable reference must reach the harness so a hash is verifiable; `PreDecisionStatus` enum values; provenance fields are facilitator-only. |
| `.agents/workflow-overlay/validation-gates.md` — receipt-field provenance gate | A subpredicate clears only on an owner-produced/verifiable value; never a self-asserted status; else `indeterminate_until_authored`. |

## Source-side field definitions (CONCRETE — named fields + closed values)

Each subpredicate has an authored field, a CLOSED value set, a cleared-condition,
and a provenance note. Every value maps to exactly one of
`clears` / `does_not_clear` / `indeterminate`.

### SP-1 source-identity

- **Authored ECR field:** `source_identity_state`
- **Canonical basis:** IPF "Source locator or source family" + "Source actor or
  audience type"; Ob.7 ("identify the source surface or source family
  categorically; preserve actor/audience where knowable; **mark when actor
  specificity is unavailable**"); boundary Inclusion State Rule.
- **Closed values:** `resolved` | `family_only` | `unresolved`
  - `resolved` — a specific source locator/citation/archive reference (or a
    resolving source id in the manifest) is present and non-placeholder, AND the
    actor/audience category is either present **or explicitly marked unavailable
    per Ob.7**. [AR-02: actor/audience is mark-if-unavailable, not a hard field
    requirement — the harness EvidenceUnit carries no actor field.]
  - `family_only` — only a source-family/surface label is available, with the
    specificity limitation visible.
  - `unresolved` — identity not established: placeholder, withheld with no
    resolving id, or missing.
- **Cleared-condition:** `clears` on `{resolved, family_only}` (family_only with a
  visible limitation flag); `does_not_clear` on `unresolved`.
- **Provenance note:** evaluated against the **facilitator-side** identity
  (source id + manifest), not the participant-facing string. The replay must cite
  the exact locator/manifest/marked-unavailable evidence behind each value
  [AR-02].

### SP-2 inspectability

- **Authored ECR field:** `inspectability_state`
- **Canonical basis:** IPF inspectable-observation requirement; Ob.12
  reconstruction floor; Ob.16 "the captured signal is inspectable"; AR-03 (source
  bytes / inspectable reference must reach the harness so the hash is
  recomputable).
- **Closed values:** `inspectable_verifiable` | `inspectable_reference_only` |
  `not_inspectable`
  - `inspectable_verifiable` — an inspectable observation/excerpt AND a verifiable
    integrity anchor: a non-placeholder source-byte hash, **plus a recorded
    recomputation-coverage basis** (the `hash_basis` field **or** an owner-bound
    equivalent such as a source-acquisition receipt that states what bytes the
    hash covers). [AR-03: verifiability requires knowing what the hash covers, not
    just that a hash-shaped string exists.]
  - `inspectable_reference_only` — an inspectable reference exists (reconstruction
    floor met) but no byte-verifiable hash with a coverage basis.
  - `not_inspectable` — no inspectable basis, or only a placeholder hash/reference,
    or a hash with no recorded coverage basis.
- **Cleared-condition:** `clears` only on `inspectable_verifiable`;
  `does_not_clear` otherwise (`inspectable_reference_only` flagged as a visible
  limitation).
- **Provenance note:** SP-2 answers "can we re-check the exact bytes we hold?" —
  **not** "are those bytes the pre-cutoff state?" (that is SP-6). Hash + basis are
  facilitator-only (AR-05). The review (NF-02) confirmed the byte-verifiable bar
  is defensible, including failing Unity's archive-only-but-unhashed EU-07.

### SP-3 timing/cutoff

- **Authored ECR field:** `cutoff_posture`
- **Canonical basis:** IPF event/publication + capture timestamps; Ob.8 decomposed
  timing; Ob.9 cutoff posture (closed vocabulary).
- **Closed values (verbatim from Ob.9):** `pre_cutoff` | `post_cutoff` | `mixed` |
  `unknown`
  - `pre_cutoff` — a non-placeholder source/event timestamp precedes the
    decision-frame cutoff.
  - `post_cutoff` — timestamp at/after the cutoff.
  - `mixed` — threaded/mutable source whose chain may include post-cutoff accretion
    and item-level timing does not make the boundary clear (Ob.8).
  - `unknown` — timestamp placeholder/missing/unparseable, or cutoff relationship
    not establishable.
- **Cleared-condition:** `clears` only on `pre_cutoff`; `does_not_clear` otherwise.
- **Provenance note:** binds to the actual source-side timestamp, not an asserted
  `pre_decision_status`. A placeholder timestamp forces `unknown` even when
  `pre_decision_status == verified_pre_decision`. SP-3 answers "is the claimed date
  pre-cutoff?" — distinct from SP-6 "are the bytes we hold the pre-cutoff state?"

### SP-4 pre_decision (VALUE check only)

- **Bound field (not authored here):** `pre_decision_status` (packing-interface
  owned).
- **Closed values (PreDecisionStatus enum):** `verified_pre_decision` |
  `uncertain_timestamp` | `excluded`
- **Cleared-condition (value):** value-check is `value == verified_pre_decision`;
  `{uncertain_timestamp, excluded}` do not clear.
- **NECESSARY-NOT-SUFFICIENT:** value-readable = value-determinate, but does **not**
  clear the pre_decision subpredicate alone because finalization (SP-5) is
  indeterminate. (Confirmed holding by the review, NF-03.)

### SP-5 finalization-provenance — OWNER-RESERVED, NOT AUTHORED HERE

- **Named slot:** `finalized_by` (conceptual; no field, no values, no authority
  defined here).
- **State:** `indeterminate_until_authored`. Who finalizes `pre_decision_status`
  is an explicit open owner decision (packing AR-01 / "Intentionally Undecided").
  This translator does not staff it. **Owner residual #1.**

### SP-6 source-visibility / pre-cutoff posture — NEW (AR-01)

Logically a source-side sibling of SP-2/SP-3; numbered 6 for continuity with the
v0 review.

- **Authored ECR field:** `source_visibility_posture`
- **Canonical basis:** IPF "Pre-cutoff visibility (required for cutoff-sensitive
  claims)"; Ob.10 archive/historical posture (**"Archive success is not required…
  Visible archive posture is required… Sufficiency belongs downstream"**; a missing
  archive attempt is a visible limitation, not silently ignored); Ob.11 source
  visibility; Ob.15 re-capture supersede/supplement/conflict; boundary
  Inclusion State Rule (Capture/preservation blocker).
- **Closed values:**
  - `archive_corroborated` — a **pre-cutoff** dated archive snapshot AND a current
    capture both exist and **match on material content**. Strongest support for
    pre-cutoff visibility.
  - `archive_only` — a **pre-cutoff** dated archive snapshot exists; pre-cutoff
    visibility established by the archive.
  - `archive_diverged` — a pre-cutoff archive and a current capture exist but
    **differ materially**; the current capture is not a reliable pre-cutoff proxy
    and the divergence is itself information.
  - `current_capture_only` — only a live/current capture; the publication date
    asserts pre-cutoff but archival visibility is **not** established. Visible
    limitation.
  - `archive_post_cutoff_only` — only a post-cutoff archive exists; does not
    establish pre-cutoff visibility.
  - `attempt_failed` — an archive attempt was made and failed (Ob.10). Visible
    limitation.
  - `not_attempted` — no archive attempt made (Ob.10). Visible limitation.
  - `not_applicable` — cutoff-insensitive claim, or an inherently immutable/official
    source class where the archival concept adds nothing (must be justified).
- **Recording is DETERMINATE.** The **grade** at which each posture clears
  (judgment-quality vs product-learning) is the **visibility-sufficiency
  threshold** — `indeterminate_until_authored`, **owner residual #2**. Pending the
  threshold, the conservative reading is: `archive_only` / `archive_corroborated`
  (pre-cutoff archive) establish pre-cutoff visibility; all other values are
  recorded visible limitations that do **not** establish archival pre-cutoff
  visibility.
- **Two foot-guns, built in:**
  - A match only helps if the **archive snapshot itself is pre-cutoff**
    (`archive_post_cutoff_only` exists for the failure case).
  - `archive_diverged` means **material** divergence; deciding materiality is a
    downstream **Judgment** call (boundary doc: Capture records, Judgment decides).
    The receipt records the raw comparison and posture only — it does not author a
    materiality verdict.
- **Scope boundary:** **performing** the archive fetch + diff is Data-Capture
  execution and is **not authorized by this docs-only slice**; the receipt only
  *records* the posture when it exists. Requiring the comparison would re-block the
  current fixtures on unauthorized capture work.

## Thin adapter to v0.14 harness EvidenceUnit (existing fixtures only)

Binds **only fields invariant across all three harness representations**
(`pydantic_schema_reference.md`, `orca-harness/schemas/case_models.py`, fixtures).

| Authored ECR field | Harness field(s) / record | Adapter rule | Notes |
| --- | --- | --- | --- |
| `source_identity_state` | `source_id` + `source` (+ manifest) | `resolved` if locator/id non-placeholder and resolves, with actor present or marked-unavailable [AR-02]; `family_only` if only a family label; else `unresolved` | actor/audience not a harness field; mark-if-unavailable per Ob.7 |
| `inspectability_state` | `hash` + coverage basis | `inspectable_verifiable` requires `hash` non-placeholder AND a coverage basis (`hash_basis` **or** acquisition-receipt equivalent) [AR-03]; else `reference_only` / `not_inspectable` | `hash_basis` is **load-bearing**, not optional |
| `cutoff_posture` | `timestamp` vs packet `decision_date_or_cutoff` | parse `timestamp`; non-placeholder and `< cutoff` → `pre_cutoff`; else per Ob.9 | placeholder timestamp → `unknown` |
| `source_visibility_posture` | archive-attempt record / acquisition-receipt `capture_scope` / re-capture relationship | map capture provenance to the SP-6 value; absent an archive, `current_capture_only` / `attempt_failed` / `not_attempted` per what the capture recorded | **no single harness field carries this**; sourced from capture/acquisition records (Ob.10/Ob.15) |
| `pre_decision_status` (SP-4) | `pre_decision_status` | read enum value | — |
| `finalized_by` (SP-5) | — | `indeterminate_until_authored` | owner residual #1 |

### Three-representation drift — corrected (AR-03)

`case_models.py` `EvidenceUnit` carries `source_type` and `hash_basis`, which the
`pydantic_schema_reference.md` shape and the fixture drafts lack. **`hash_basis`
is load-bearing for SP-2** (verifiability needs to know what the hash covers); it
is supplied either by the field or an owner-bound equivalent (e.g., a
source-acquisition receipt). The full ECR/EvidenceUnit consolidation must
reconcile which representation is canonical and whether `source_type`/`hash_basis`
become required. The adapter binds only invariant core fields, so it is stable
meanwhile, but SP-2 now explicitly requires the coverage basis regardless of which
representation supplies it.

## Worked validation replay (Canoo/Walmart + Unity)

Shows determinacy — not judgment quality, not fixture admission. Re-scored after
the patch.

### Canoo/Walmart (`canoo_walmart_2022_v0_14`, CW-E01..CW-E06x; cutoff ≈ Jul 2022)

| Subpredicate | Evaluated value | Outcome |
| --- | --- | --- |
| SP-1 source-identity | `resolved` (source_id CW-P1..P6 resolve in manifest; actor/family from source roles; participant string is a safety alias) | clears |
| SP-2 inspectability | `inspectable_verifiable` (real sha256 + acquisition-receipt coverage basis: "SHA-256 over captured local file bytes") | clears |
| SP-3 timing/cutoff | `pre_cutoff` (2022-01..2022-06 timestamps < cutoff) | clears |
| SP-6 source-visibility | `current_capture_only` (acquisition receipt: 2026 current live web bytes for CW-P1..P5, owner-supplied local SEC file for CW-P6; "not historical archive"; "does not prove pages are unchanged from original publication dates") | **does not establish archival pre-cutoff visibility — recorded limitation; grade pending threshold** |
| SP-4 pre_decision value | `verified_pre_decision` | value clears |
| SP-5 finalization | `indeterminate_until_authored` | residual #1 |

**Result: DETERMINATE — identity, inspectability, timing, and pre-decision value
clear; pre-cutoff *visibility* is `current_capture_only` (a visible limitation).**
Two owner residuals remain: finalization authority (SP-5) and the
visibility-sufficiency threshold (SP-6 grade). This corrects the v0 overclaim
that Canoo "clears source-side" with finalization as the only residual.
**Upgrade path:** a later pre-cutoff archival capture (e.g., Wayback/EDGAR) could
move SP-6 to `archive_only`/`archive_corroborated`.

### Unity (`unity_runtime_fee_2023_v0_14`, EU-01..EU-08; cutoff 2023-09-11)

| Subpredicate | Evaluated value | Outcome |
| --- | --- | --- |
| SP-1 source-identity | `resolved` for EU-01..07 (real SEC/archive locators; actor = filer/marked-unavailable); EU-08 source-gap | mostly clears |
| SP-2 inspectability | `not_inspectable` — `hash: TBD_SOURCE_BYTE_HASH` for every unit (no coverage basis) | does not clear |
| SP-3 timing/cutoff | `unknown` for EU-01..06 (placeholder timestamps); `pre_cutoff` for EU-07 (2023-01-03 archive) | does not clear |
| SP-6 source-visibility | `archive_only` candidate for EU-07 (pre-cutoff Wayback snapshot) but unhashed; `current_capture_only`/gap elsewhere | EU-07 archive exists but SP-2 still fails (no hash) |
| SP-4 pre_decision value | `verified_pre_decision` (EU-01..07); `excluded` (EU-08) | mixed |
| SP-5 finalization | `indeterminate_until_authored` | residual #1 |

**Result: DETERMINATE — source-side does NOT clear** (blocked at SP-2 and SP-3).
Note SP-6 surfaces a real nuance: EU-07 *has* a pre-cutoff archive but cannot be
verified because its hash is `TBD` — so archive existence does not rescue it while
inspectability fails. Matches Unity's "blocked before scoring" posture.

## Conductor adoption (PROPOSED — apply only at owner ratification)

Unchanged in posture from v0 and confirmed holding by the review (NF-04): the
conductor must **reference** this interface — not copy it, not edit its predicate.
**Not applied this turn.** The gate stays frozen until this slice is ratified +
re-reviewed. At ratification the JSG-01 row adopts a reference of this shape:

> Source-side subpredicates (source-identity, inspectability, timing/cutoff,
> source-visibility posture) bind to
> `docs/product/jsg01_source_side_receipt_translator_v0.md` (SP-1, SP-2, SP-3,
> SP-6). `pre_decision_status` value check is SP-4. Finalization-provenance (SP-5)
> and the visibility-sufficiency threshold (SP-6 grade) remain
> `indeterminate_until_authored` (owner-reserved). Until ratification this row is
> unchanged.

## Owner ratification required (this artifact is not the ratification)

Decisions reserved to the owner; this slice resolves none of them:

1. **Field-slice ratification** — accept these source-side fields + closed values
   as the official JSG-01 first slice of the ECR/EvidenceUnit consolidation.
2. **Finalization authority (SP-5)** — who may finalize `pre_decision_status`; the
   operator-set-status-is-a-block-state rule. *Owner residual #1.*
3. **Visibility-sufficiency threshold (SP-6 grade)** — which
   `source_visibility_posture` values clear at judgment-quality grade vs.
   product-learning grade. This is where the owner's "current-capture usually
   won't weaken the position" judgment lives, **visibly**, rather than hardcoded.
   *Owner residual #2.*

Flagged for the owner:

- **SP-3/SP-6 correctness depends on capture discipline.** The value sets are
  defensible (Ob.9/Ob.10), but whether a source is truly `pre_cutoff` /
  `archive_corroborated` etc. is a Data-Capture judgment the receipt *records*, not
  *certifies*.
- **Re-review still required.** The patch changes the determinacy result
  (Canoo downgraded; SP-6 added); a scoped independent re-review of the changed
  provenance rules (SP-2, SP-6, the replay) should run before ratification. The
  v0 review covered the pre-patch artifact only.
- **Performing the archive-vs-current comparison** and **three-representation
  drift** are deferred to capture execution and the full consolidation.

## Adversarial self-review (same-family; NOT the required cross-family re-review)

- **(a) Forks the schema?** No — IPF-semantic fields, harness as adapter target.
- **(b) Real case determinate?** Yes — Canoo determinately *partial* (residuals
  named), Unity determinately does-not-clear. The v0 "clean clear" overclaim is
  corrected.
- **(c) Finalization leak?** No — SP-5 unstaffed; SP-6's grade threshold is a
  *separate* named owner residual, also unstaffed (no self-staffing by stealth).
- **(d) Canonical home?** Yes — SP-6 grounded in Ob.10/Ob.11/Ob.15 + IPF
  pre-cutoff visibility.
- **(e) Inspectability honest?** Strengthened — SP-2 now requires a coverage basis
  (AR-03), and SP-6 separates "re-checkable bytes" from "pre-cutoff bytes."
- **(f) Conductor reference?** Staged pointer, not applied; gate frozen.
- **Residual self-review risk:** same model family as the author; the patched
  SP-2/SP-6/replay must still pass an independent re-review before ratification.

## Non-claims

Path-not-proof. Not: judgment quality; fixture admission; the full
ECR/EvidenceUnit consolidation; finalization authority; the visibility-sufficiency
threshold; performing archive comparison; validation; readiness; gate clearance;
owner ratification. Does not unfreeze JSG-01. Does not authorize capture
execution, model execution, scoring, implementation, runtime, tests, commits, or
PRs.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    PROPOSES (and, after independent review, patches) a first slice of the
    deferred ECR/EvidenceUnit consolidation: a JSG-01 source-side receipt
    translator naming source-identity, inspectability, timing/cutoff, and
    source-visibility/pre-cutoff posture fields with closed allowed-values in
    IPF / Data-Capture canonical semantics, plus a thin adapter to the v0.14
    harness EvidenceUnit fields for existing fixtures. The patch adds SP-6
    source-visibility posture (Ob.10/Ob.11/Ob.15) carrying an archive-vs-current
    comparison signal, requires a hash coverage basis for SP-2 (AR-03),
    reconciles SP-1 actor/audience to mark-if-unavailable (AR-02), corrects the
    Canoo overclaim (AR-01), and names a second owner residual (the
    visibility-sufficiency threshold) alongside finalization. It is PROPOSED and
    not owner-ratified; JSG-01 stays frozen and the conductor predicate is
    unchanged. No new claim tier or closeout_state is minted; no finalization
    authority and no sufficiency threshold are staffed.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/jsg01_source_side_receipt_translator_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/judgment_quality_promotion_operating_model_v0.md
    - docs/product/judgment_spine_gate_ownership_map_v0.md
    - docs/product/core_spine_v0_information_production_foundation_v0.md
    - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
    - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
    - orca-harness/schemas/case_models.py
    - docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md
  intentionally_not_updated:
    - path: docs/product/judgment_quality_promotion_operating_model_v0.md
      reason: >
        Conductor reference is staged, not applied. Gate stays frozen until owner
        ratification + scoped re-review.
    - path: .agents/workflow-overlay/source-loading.md
      reason: Not wired into a read pack as authoritative; the slice is PROPOSED and unratified.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: Navigation entry deferred until ratification.
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: >
        SP-6 binds to existing Ob.10/Ob.11/Ob.15 vocabulary; it does not amend the
        obligation contract. Performing archive comparison stays unauthorized capture work.
  stale_language_search: "rg -n \"jsg01_source_side_receipt_translator|source_identity_state|inspectability_state|cutoff_posture|source_visibility_posture|first slice\" docs/product .agents/workflow-overlay docs/workflows"
  stale_language_search_result: >
    Executed 2026-06-04 across the FULL repo (broader than the v0 sweep, which
    searched only docs/ and missed this). NOT collision-free. `cutoff_posture`
    COLLIDES with orca-harness/source_capture/models.py PacketTiming.cutoff_posture,
    an IMPLEMENTED VisibleFact (status+value), not this artifact's closed enum —
    same name, different shape. SP-6 `source_visibility_posture` is not a literal
    name collision but DUPLICATES the Armory's existing access_posture +
    archive_history_posture + re_capture_relationship VisibleFacts. The Source
    Capture Armory (SourceCapturePacket (CapturePacket), obligation-contract-bound) is the
    implemented source-side producer; this translator coined parallel docs
    vocabulary and adapted to the downstream harness EvidenceUnit instead of
    binding the upstream SourceCapturePacket. FLAGGED as a material acceptance
    risk: before ratification + re-review, the translator should bind/reference
    the Armory capture fields rather than coin parallel names. Other authored
    names (source_identity_state, inspectability_state) and the filename appear
    only in this artifact and its review/prompt records.
  non_claims:
    - not validation
    - not readiness
    - not owner ratification
    - not gate clearance
    - not judgment-quality evidence
    - not the ECR/EvidenceUnit consolidation
    - not finalization authority
    - not the visibility-sufficiency threshold
```
