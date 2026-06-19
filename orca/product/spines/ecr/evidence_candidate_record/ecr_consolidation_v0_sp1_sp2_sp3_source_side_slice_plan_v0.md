# ECR Consolidation v0 — Source-Side Fields (SP-1 / SP-2 / SP-3) Reconcile Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Reconcile the three remaining JSG-01 source-side ECR fields — SP-1 source-identity,
  SP-2 inspectability, SP-3 timing/cutoff — from the interim translator into the
  ratified ECR frame (the M1/M2/M3 binding rule + INV-1..5), binding each to the
  committed Source Capture producer fields and FIXING the SP-3 `cutoff_posture`
  name-collision (carry the producer field; do not coin a parallel same-named field).
  Advisory design; recommends but ratifies nothing.
status: PROPOSED_ARCHITECTURE_ROUTING_OBJECT — advisory, non-executing, PRE cross-family review, PRE ratification.
use_when:
  - Preparing the cross-family review of the SP-1/SP-2/SP-3 source-side ECR fields.
  - Completing the JSG-01 source-side field schema the conductor predicate names.
authority_boundary: retrieval_only
gate_posture: JSG-01 stays FROZEN. This plan does not bind, ratify, or unfreeze anything.
relates_to:
  ecr_frame_and_sp6_slice: docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md  # frame inherited from here (ratified seed, committed)
  interim_translator: docs/product/jsg01_source_side_receipt_translator_v0.md  # SP-1/2/3 field definitions reconciled FROM here (PROPOSED)
  conductor_predicate: docs/product/judgment_quality_promotion_operating_model_v0.md  # JSG-01 names source-identity + inspectability + timing/cutoff fields
producer_state: >
  R2 producer fields committed at 102a171 (ancestor of HEAD): closed CUTOFF_POSTURE_VALUES,
  PreservedFile.hash_basis + validators. SP-2 and SP-3 bind directly to these committed fields.
branch_or_commit: main @ HEAD (re-verify producer citations against HEAD before ratification).
stale_if:
  - The ECR frame (INV-1..5 / three-mode binding rule) is amended.
  - models.py changes SourceCapturePacket (CapturePacket) identity fields, PreservedFile/hash_basis, or PacketTiming.cutoff_posture.
  - The owner ratifies, amends, or declines these three fields.
```

- **Status:** advisory design; **non-executing**. Recommends three fields for the owner's source-side ratification consideration alongside the already-ratified SP-6 frame/derivation-contract seed. Designs no derivers; the field *implementation* (computing each value from a packet) is post-ratification.
- **Frame inheritance:** uses the ratified ECR frame verbatim (INV-1..5, the three-mode binding rule, D3 upstream-owned/carried, D4 bind-real-fields-coin-nothing). This plan does **not** redesign the frame; it instantiates it three more times.
- **Why these three:** the conductor's JSG-01 predicate returns `indeterminate_until_authored` for the source-identity, inspectability, and timing/cutoff subpredicates because no ECR field schema names them. SP-6 (source-visibility) is ratified only as the frame/derivation-contract seed; these three would complete the proposed source-side schema candidate the gate could bind to only after owner ratification.

---

## SP-1 — `source_identity_state` (binding mode: **M2 derived-read, with M3 stops**)

- **What the producer owns (inputs):** `SourceCapturePacket.source_family`, `source_surface`, `source_locator` (`models.py:164-166`); actor/audience via `actor_audience_context` (`models.py:169`) under Ob.7 ("mark when actor specificity is unavailable").
- **What the ECR derives (the answer):** a closed identity state — the producer does not store a closed "identity state", so the ECR computes it from the inputs. → **M2**.
- **Closed values:** `resolved` | `family_only` | `unresolved`.
- **Clear-condition:** `clears` on `{resolved, family_only}` (`family_only` carries a visible specificity limitation); `does_not_clear` on `unresolved`.
- **M3 stop:** `unresolved` (placeholder / withheld with no resolving id / missing) → `does_not_clear` as a named limitation; the ECR never invents an identity.
- **D4 / AR-02:** binds the real producer fields; coins no parallel vocabulary. Actor/audience is **mark-if-unavailable** (Ob.7), not a hard field — the harness `EvidenceUnit` carries no actor field, so `resolved` does not require an actor value, only that actor is present *or* explicitly marked unavailable.
- **Provenance:** evaluated against facilitator-side identity (source id + manifest), not the participant-facing string.

## SP-2 — `inspectability_state` (binding mode: **M2 derived-read over an M1-carried integrity anchor**)

- **What the producer owns:** `PreservedFile.sha256` + `PreservedFile.hash_basis` (`models.py:101-102`; closed `HASH_BASIS_VALUES` `:66`; validator `:105-114`) — **R2-committed at 102a171**; plus the inspectable reference (reconstruction floor).
- **What the ECR derives:** the inspectability state — M2 over the producer inputs; the integrity hash itself is **M1-carried-by-reference** (a pointer the harness recomputes, never trusts).
- **Closed values:** `inspectable_verifiable` | `inspectable_reference_only` | `not_inspectable`.
- **Clear-condition:** `clears` **only** on `inspectable_verifiable` = an inspectable observation/excerpt **AND** a non-placeholder `sha256` **AND** a recorded recomputation-coverage basis (`hash_basis`, or an owner-bound acquisition receipt for pre-R2 `v0` packets that lack it). `inspectable_reference_only` and `not_inspectable` `does_not_clear` (reference-only flagged as a visible limitation).
- **Load-bearing consequence of R2:** the `inspectable_verifiable` bar is now satisfiable **in committed source** — `hash_basis` is the primary coverage basis (the acquisition-receipt path is the fallback). A hash with no recorded coverage basis is `not_inspectable` (a hash-shaped string is not verifiability).
- **D3:** the integrity anchor is upstream-owned (`PreservedFile`), carried downstream by reference, recomputed at the harness, **never re-authored** at `EvidenceUnit`.
- **Boundary:** SP-2 answers "can we re-check the exact bytes we hold?" — **not** "are those bytes the pre-cutoff state?" (that is SP-6).

## SP-3 — timing/cutoff (binding mode: **M1 carried-by-reference**) — NAME-COLLISION FIXED

- **The fix (the headline of this slice).** The interim translator named SP-3's "authored ECR field" `cutoff_posture` — colliding by-name with the **producer's** `PacketTiming.cutoff_posture`. The producer **already owns and closes** that field (`models.py:87`; closed `CUTOFF_POSTURE_VALUES = {pre_cutoff, post_cutoff, mixed, unknown}` `:53`; validator `:90-94` — **R2-committed at 102a171**). Under the frame's **D4** rule, when the producer already closes the fact the ECR **carries it by reference (M1)** — it does **not** coin a parallel same-named ECR enum. SP-3 is therefore re-seated from "authored field" to **carried producer value + an ECR-side clear-condition**. (This is the SP-3 analog of SP-6's AR-02 / D4 correction.)
- **What the ECR carries (M1):** the producer's closed `cutoff_posture` value, bound to the real source timestamps (`PacketTiming.source_publication_or_event` / `source_edit_or_version`) — **never** an asserted `pre_decision_status`.
- **Closed values (producer-owned, Ob.9, carried not re-coined):** `pre_cutoff` | `post_cutoff` | `mixed` | `unknown`.
- **Clear-condition (ECR/gate logic over the carried value, not a new field):** `clears` only on `pre_cutoff`; `does_not_clear` otherwise. A placeholder/missing/unparseable timestamp forces `unknown` even when `pre_decision_status == verified_pre_decision`.
- **Boundary:** SP-3 answers "is the claimed date pre-cutoff?" — distinct from SP-6 "are the bytes we hold the pre-cutoff state?".

---

## Invariant check (all three)

- **INV-1 (single source-side writer):** the producer is the only writer; absent facts become named limitations, never invented. ✓
- **INV-2 (receipt/derive only):** SP-1/SP-2 derive a recorded read; SP-3 receipts (carries) a producer fact. No new capture verb. ✓
- **INV-3 (no persisted capture field; no migration):** all three are derived/carried projections, not stored columns. ✓
- **INV-4 (recomputation basis upstream-owned, carried):** SP-2's integrity anchor is `PreservedFile.{sha256, hash_basis}`, carried by reference; recomputed at the harness. ✓
- **INV-5 (categorical handoff, not schema import):** binds the producer's real fields; imports no schema; defines no producer field. ✓

## Scope fences

- Covers **only** SP-1/SP-2/SP-3. SP-4 (the `pre_decision_status` **value** check) is packing/case-level; the **two owner residuals** — SP-5 finalization authority and the SP-6 visibility-sufficiency grade — are owner decisions recorded at ratification, not designed here. The SP-6 standing-field declaration also remains deferred by the ratified seed boundary; this plan does not reopen it.
- **JSG-01 stays FROZEN.** This plan recommends fields; it neither ratifies them nor unfreezes the gate.
- Designs **no derivers**. Computing each value from a packet is implementation, gated behind ratification.

## What the cross-family review must attack

1. **SP-3 M1-carry-not-coin** — confirm the producer already closes `cutoff_posture` and that carrying-by-reference (not coining a parallel field) is the correct frame resolution; flag any place this slip back into a coined enum.
2. **SP-1 M2 derivation + AR-02** — does `resolved` correctly treat actor/audience as mark-if-unavailable (no hard actor field the harness can't carry)? Any value mis-assigned?
3. **SP-2 verifiable bar vs committed `hash_basis`** — replay against committed `models.py`: does `inspectable_verifiable` correctly require a recorded coverage basis, and is the R2 dependency cited at HEAD (not a stale line)?
4. **Citations resolve at HEAD** — spot-check every `models.py:line` against committed source.
5. **Frame fidelity** — INV-1..5 and D3/D4 held for all three; no coined vocabulary; derived/non-persisted preserved.
6. **Cross-family independence** — run by a different model family than this plan's author.

## Non-claims

Advisory architecture/design only. Not implementation, validation, ratification, JSG-01 unfreeze, the SP-5/SP-6-grade owner decisions, or the field derivers. The producer fields are committed (R2 @ 102a171); this plan binds to them and authors no producer fact. This is not proof of readiness.
