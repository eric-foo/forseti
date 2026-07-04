# ECR Consolidation v0 — Thin Frame + Source-Visibility Slice — Architecture Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Non-executing architecture routing object for the owner-opened ECR/EvidenceUnit
  consolidation, BOUNDED to the smallest-complete increment: a thin Evidence
  Candidate Record (ECR) frame plus the source-visibility slice (SP-6 as the first
  authored ECR field). Designs the frame + slice only; sibling ECR fields are
  named-but-deferred. Advisory planning only; recommends but ratifies nothing and
  does not enter the full field-architecture consolidation.
use_when:
  - Preparing the owner ratification of ECR consolidation v0 (frame + source-visibility slice).
  - Building or reviewing the SP-6 ECR field against the upstream Source Capture producer.
  - Checking the ECR layering invariants / binding rule before any sibling ECR field is designed.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/source_side_receipts/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/judgment/source_side_receipts/jsg01_source_side_receipt_translator_v0.md
input_hashes:
  docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md: 03310806D8B4475CC281FF65F2247B59702D3B4036DF6C38A9A1383EDB7102AB
  docs/product/jsg01_source_side_receipt_translator_v0.md: E8944D13FF8B3FAF62AC24209EC50FDA7C03CC9D4F906687246B2E15C01592B2
  docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md: F873C0EA9B61135971058B517DF0C220569FAFDA032D9407B2073216D8920B27
branch_or_commit: >
  main @ 02d2ff0. R2 posture-closure + PreservedFile.hash_basis are now COMMITTED
  (present in HEAD, verified by reading the committed source; models.py landed at
  102a171, an ancestor of HEAD). SP-6/ECR controlling docs remain untracked ->
  still advisory. NB: source_quality.py carries an unrelated, uncommitted
  schema-evolution delta, so R2 line citations below resolve against the HEAD blob,
  not the dirtied working tree.
stale_if:
  - The owner ratifies, amends, or declines ECR consolidation v0 (the frame and/or the SP-6 slice).
  - The committed R2 (closed posture vocabularies + PreservedFile.hash_basis, landed at 102a171) is reverted or further amended.
  - orca-harness/source_capture/models.py changes SourceCapturePacket (CapturePacket) posture fields, PreservedFile, or hash_basis.
  - The capture lane adds a first-class archive-snapshot-date fact or a recorded archive-vs-current comparison fact.
  - The boundary doc's reserved-consolidation status (lines 281-309) is edited to record the open.
```

- Status: `PROPOSED_ARCHITECTURE_ROUTING_OBJECT` — advisory planning, **non-executing**.
- Gate posture: **JSG-01 stays FROZEN.** This plan does not bind, ratify, or unfreeze anything.
- Scope: the owner has OPENED the reserved ECR consolidation, **scoped to source-visibility**. This lane designs the **frame + SP-6 slice** and nothing wider; sibling ECR fields are named-but-deferred, never designed.
- Strict-claim boundary: the SP-6/ECR controlling docs are untracked -> **advisory only. No readiness / acceptance / validation / ratification claim.** R2 / `hash_basis` is now committed (`102a171`) and its citations were re-verified against HEAD this turn; the only residual is that R2's own test suite was not re-run this turn (its implementation review settled on record).

---

## Human Summary

**Decision (lane synthesis).** Recommend a **thin ECR frame** — a derived-projection layer over the upstream `SourceCapturePacket` (CapturePacket), with one stable invariant (the ECR stores no new capture fact and authors no capture truth) and a **three-mode binding rule** — and, instantiating that frame, **SP-6 `source_visibility_posture` as the first ECR field**: an ECR-owned, **derived, non-persisted** value-or-residual reduction of the producer's already-closed facts. Architecture result: `TARGET_RECOMMENDED` for the frame + slice **design**, advisory. The full ECR field architecture stays owner-reserved and is **not** designed here.

**The frame in one line.** ECR = receipt/derive layer between Capture and Cleaning; a capture fact becomes an ECR field in exactly one of three modes — **carried-by-reference** (producer owns and closes the fact; ECR points + downstream recomputes), **derived-read** (producer owns the inputs; ECR computes a recorded read), or **named-residual** (producer holds neither; ECR records the gap and stops, never coining a parallel field). The mode is chosen by *where the fact's authority already lives*, so the slice pre-commits no sibling field's shape.

**The slice in one line.** SP-6 is **M2-with-M3-stops today**: the adopted residual-first decision table (per slice, then an Ob.10 no-hide rollup) reads the producer's closed `archive_history_posture` / `re_capture_relationship` facts, archive-date metadata/timing convention, and `PreservedFile` references to emit one closed value *or* a named residual. The `source_visibility_posture` label is retained from the existing SP-6/ECR language, while the inputs are bound to real producer fields rather than coined in parallel; it derives from the **upstream** packet (not the downstream `EvidenceUnit`) — which is exactly the fix for the interim translator's flagged error.

**Decisive correction carried forward (verified against committed HEAD).** The prompt and the adopted SP-6 plan (both pinned at `e4e854e`) assume "no `hash_basis` on `SourceCapturePacket`." That is now superseded **in committed source**: `PreservedFile.hash_basis` exists, **closed** to `{raw_stored_bytes}` and recomputation-bound (R2 landed at `102a171`). So the SP-2-sibling verifiability basis re-points to **upstream `PreservedFile.{sha256, hash_basis}` as primary** (acquisition-receipt as fallback); this now rests on **committed** producer state (re-verified against HEAD this turn), the only residual being that R2's test suite was not re-run this turn. **D1 is unchanged**: no stored visibility posture and no recorded archive-vs-current comparison exist, so `archive_corroborated`/`archive_diverged` still route to a named residual today.

**Scope / boundary.** Design-only. Nothing built, ratified, or unfrozen. The SP-6 **sufficiency grade**, SP-5 **finalization**, **materiality** verdicts, the **full field architecture**, and the **boundary-doc edit recording the open** all stay owner-reserved/downstream.

**Next action (smallest complete).** The independent cross-family review is done (`accept_with_friction`) and R2 is now committed, so the remaining step is **owner ratification + boundary-doc update + a `direction_change_propagation` receipt**. Per owner direction this turn, ratification targets **AF-7 option B** (ratify the derivation contract as the seed; defer the field declaration). The earlier "commit R2 first" precondition is met; an optional fresh suite-green at HEAD is the only residual evidence.

**What remains blocked.** The full ECR field architecture (siblings); JSG-01 unfreeze; the SP-6 grade; SP-5 finalization; performing any archive fetch/diff; editing/ratifying the boundary doc. (R2/`hash_basis` is no longer "not landed" — it is committed at `102a171`.)

---

## Architecture Result

| Question | Result | Why |
|---|---|---|
| Design a thin ECR frame that can host one field without pre-committing the rest? | `TARGET_RECOMMENDED` (advisory) | Selection threshold met: stable invariant (no stored capture fact; single source-side writer), clear core/satellite split (frame fixes *where authority lives*, not field shapes), known non-goals, no unresolved upstream blocker that changes the frame. |
| Design SP-6 as the first ECR field (source-visibility slice)? | `TARGET_RECOMMENDED` (advisory) | Instantiates the frame as an M2 derived-read over producer facts where inputs exist, with M3 named-residual stops where the producer lacks a recorded comparison; reversible (deleted, not migrated); fail-safe; removes the translator's duplication/collision. |
| Author the full ECR field architecture (siblings) now? | `DEFER` / owner-reserved | Out of scope (overbuild). Siblings named-but-deferred only. Boundary doc :309 reserves the final field architecture. |
| Is SP-6 fully mechanically derivable today? | **NO (D1, unchanged)** | `archive_corroborated`/`archive_diverged` need a recorded comparison the producer does not store; emit named residuals. |
| Does the upstream producer now carry a recomputation basis (re D3)? | **YES (committed)** | `PreservedFile.hash_basis = raw_stored_bytes` exists and is enforced in committed source (R2 at `102a171`); re-points SP-2 basis primary/fallback. Residual: R2 suite not re-run this turn. |

---

## Part 1 — The thin ECR frame

### 1.1 Provisional object name

**`EvidenceCandidateRecord` (`ECR`)** — retain the boundary doc's existing layer term as the canonical object name, **provisionally**.

- **Decisive criterion: minimize coined vocabulary against the very error this lane corrects.** The in-scope failure is the interim translator's parallel-name coinage (`jsg01_source_side_receipt_translator_v0.md:443-453`). The boundary doc already uses "Evidence Candidate Record" throughout (`core_spine_v0_data_and_cleaning_spine_boundary_v0.md:36,72-75,131,281`) and reserves only whether it is the **final canonical** name or a **working** name (`:283-284,298-299`). Minting a new object name now would itself be the coinage/scope-creep the frame must resist.
- This resolves the canonical-vs-working-name question **only provisionally**; the final name stays owner-reserved. No frame invariant below is keyed to the literal string "ECR" — the frame must survive an owner rename.

### 1.2 Layering invariants (future work must preserve all five)

```text
Data Capture Spine (Armory / SourceCapturePacket (CapturePacket))  -- PRODUCES capture facts (single source-side writer)
   v
Evidence Candidate Record (ECR)                    -- RECEIPTS / DERIVES (authors no capture fact; stores none)
   v
Packing (harness entry bundle)                     -- ASSEMBLES the admission bundle
   v
Harness Foundation (EvidenceUnit)                  -- CONSUMES carried references (recomputes, never re-authors)
```

- **INV-1 — Single source-side writer.** The Armory (`SourceCapturePacket` and members) is the only source-side writer of capture facts. If a fact is not in the producer, the ECR records its absence as a named residual; it never invents it. (Boundary `:74-75`; the producer enforces closed posture vocabularies at write-time, `orca-harness/source_capture/models.py:90-94,129-143,185-199`.) This is the invariant the translator violated by coining `source_visibility_posture` outside the producer.
- **INV-2 — Receipt/derive, not re-author.** The ECR has exactly two verbs — **receipt** (point at a producer fact by reference) and **derive** (compute a recorded read over producer facts). It has no "author a new capture fact" verb and no "store a capture truth" verb.
- **INV-3 — No persisted capture field; no migration.** ECR fields are derived projections, not stored columns. An ECR field is deleted (not migrated) if the full consolidation later supersedes it. (Closes the fork risk: a *stored* field would add a second writer for posture the producer already owns.)
- **INV-4 — Recomputation basis is upstream-owned and carried by reference (D3).** The verifiability/recomputation anchor lives at the producer (`PreservedFile.sha256` + `PreservedFile.hash_basis`, `models.py:97-114`). The ECR carries a *reference*; the harness *recomputes* against the carried bytes/reference and **never re-authors** the basis at `EvidenceUnit`. The downstream `EvidenceUnit.hash_basis` (`orca-harness/schemas/case_models.py:61`) is a carried value, not an authoring home (it is an un-closed `str`, strictly weaker than the upstream closed token).
- **INV-5 — Categorical handoff, not schema import.** Capture hands the ECR *categorical* context (boundary `:268`; obligation contract Ob.16 explicitly does not define ECR fields). The ECR turns categorical handoff into receipt fields **without** importing the producer's schema and **without** Capture defining ECR fields. Field shapes never flow up into Data Capture.

### 1.3 The binding rule (general; instantiable by SP-6; non-sibling-committing)

> **A capture fact becomes an ECR field only via one of three binding modes, and the mode is chosen by where the fact's authority already lives. The ECR field names *what is received or derived*; it never re-states a producer fact in parallel vocabulary, and it never adds a field to `SourceCapturePacket`.**

| Mode | When to use | What the ECR field is | Source basis |
|---|---|---|---|
| **M1 — carried-by-reference** | The producer already owns and **closes** the fact. | A pointer + carried value; downstream **recomputes**, does not trust. | Upstream `PreservedFile.hash_basis` (`models.py:57-66,102`) plus downstream transport/recompute surfaces (`case_models.py:61`; `packing_to_harness_foundation_interface_architecture_v3.md:123,135,137,178`). |
| **M2 — derived-read** | The producer owns the **inputs** but not the answer. | A deterministic, recorded read over producer facts (a read, never a new fact). | An archive-date class read from `selected_snapshot.timestamp` / `PacketTiming` slice timing (`source_quality.py:169,405-412,434-446`). |
| **M3 — named-residual** | The producer holds neither the fact nor derivable inputs. | `indeterminate_until_authored` / a named visible-limitation residual — then **stop**. Never coin a parallel field; never perform unauthorized capture. | The verified absence of any stored `source_visibility_posture` / comparison field -> SP-6's comparison-dependent rows are M3 today. |

The rule is **concrete enough** that SP-6 instantiates it (M2 where archive/timing/current-presence inputs exist; M3 where the producer lacks the recorded comparison or date basis), yet **general enough** that it pre-commits no sibling field's shape (each sibling independently re-runs the where-does-authority-live test). The rule's own fence: M1 values are recomputed-not-trusted; M2 derivations are reads-not-facts; M3 residuals are stops-not-invitations-to-coin.

### 1.4 Sibling ECR field areas — NAMED-BUT-DEFERRED (none designed)

Area + why deferred (from boundary `:75,163-171,285-294`). **None designed below.**

- **Raw-observation / raw-claim receipt** — the inspectable observation and claim-vs-interpretation separation; sibling content field, not source-visibility.
- **Inspectability reference (SP-2 sibling)** — the reconstruction-floor pointer; the slice needs only its *carried basis* (INV-4), not this field's design. **Highest care: do not design it to build SP-6** (overbuild STOP held — see 3.x).
- **Source-identity (SP-1 sibling)** — identity/actor receipt; separate field.
- **Cutoff/timing (SP-3 sibling)** — the cutoff-relationship read; separate field (SP-6 reads archive-date/timing convention inputs only and does not mint a same-named `cutoff_posture` enum).
- **Projection-packet reference** — how a Data Capture Projection Packet is receipted without turning ECR into a projection schema (boundary `:288-289`).
- **Transformation-ledger reference** — how Cleaning's ledger is referenced conceptually (boundary `:290`).
- **Inclusion-state + state-reason + layer-ownership** — recording inclusion/handoff state with a layer-owned reason (boundary `:160-176,291`); spans layers; designing it would pull in Judgment ownership.
- **Snapshot/archive <-> pre-cutoff-visibility relation** — boundary `:292`; **directly adjacent to SP-6 and the highest collision risk**; named as the bordering deferred area, not designed.
- **Judgment-overlay attachment** — boundary `:293`; Judgment-owned, hard out-of-scope.
- **Frozen-core-invariant field set** — which Evidence Unit fields are frozen core invariants (boundary `:285`); this is the full field architecture, owner-reserved.

### 1.5 Three-representation accounting (roles fixed; fields not reconciled)

| Representation | Role | What the frame does with it |
|---|---|---|
| **IPF Evidence Unit standard** (`core_spine_v0_information_production_foundation_v0.md`) | **Canonical-to-cite** (semantic home) | ECR field *semantics* are authored in IPF terms; boundary `:131-134` fixes IPF as the cite-home until the consolidation. |
| **`SourceCapturePacket`** (CapturePacket) (`orca-harness/source_capture/models.py`) | **Producer** (sole source-side writer) | ECR binds to its real fields by reference/derive (D4); never writes into it. |
| **Harness `EvidenceUnit`** (`case_models.py` + `pydantic_schema_reference.md`) | **Downstream consumer** (carried-reference target) | ECR carried references land here; the harness recomputes, never re-authors (D3). |

**Representation-drift reconciliation is DEFERRED** (named, not resolved): (a) the pydantic doc shape lacks `source_type`/`hash_basis` that the `case_models.py` impl has; (b) the producer's `cutoff_posture` (a `VisibleFact`) vs the translator's coined same-named closed enum — a same-name/different-shape collision (`jsg01_source_side_receipt_translator_v0.md:443-453`). Choosing the canonical representation and whether `source_type`/`hash_basis` become required is the **full consolidation's** job (boundary `:285`), owner-reserved. The frame's only commitment: **IPF cites, Armory produces, EvidenceUnit consumes** — and the "no parallel names" clause stops the slice from adding a fourth drift.

### 1.6 Core / satellite boundary

- **Core (frame-invariant):** the object sits between Capture and Cleaning as a receipt, not a writer; INV-1..INV-5; the three-mode binding rule as the only sanctioned ways a capture fact becomes an ECR field; the three-representation role assignment; D3 and D4 as non-negotiable.
- **Satellite / per-field:** which binding mode each individual sibling uses; per-source-family capture-feasibility specifics; the SP-6 value-set membership and the SP-6 grade threshold (owner-reserved); per-case fixture-adapter content.

---

## Part 2 — The source-visibility slice (SP-6 as the first ECR field)

### 2.1 Field definition

- **Field name (D4 — retain label, bind real inputs):** `source_visibility_posture`, re-seated as an **ECR-owned, derived, non-persisted** field — the reduction of already-produced `SourceCapturePacket` facts to one visibility posture or a named residual. Explicitly **not** a stored capture fact (no second writer; grep confirms none exists) and **not** a downstream-coined name bound to `EvidenceUnit` (the translator's error). D4 is satisfied by binding the derivation to the real Armory fields (`archive_history_posture`, `re_capture_relationship`, timing/archive metadata, `PreservedFile`) rather than inventing parallel producer vocabulary.
- **Closed value set** (8, ECR-owned; from the adopted plan / translator `:214-232`): `archive_corroborated` · `archive_only` · `archive_diverged` · `current_capture_only` · `archive_post_cutoff_only` · `attempt_failed` · `not_attempted` · `not_applicable`.
- **Named-residual set** (the D1 honesty surface): `RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT` · `RESIDUAL_COMPARISON_NOT_RECORDED` · `RESIDUAL_ARCHIVE_DATE_UNKNOWN` · `RESIDUAL_ARCHIVE_POSTURE_UNKNOWN` · `RESIDUAL_NO_VISIBILITY_BASIS` · `RESIDUAL_SLICE_DIVERGENT_VISIBILITY` (rollup).
- **Shape recommendation (per the adversary's F3):** evaluate **per relevant slice** -> emit value-or-residual per slice -> apply an **Ob.10 no-hide rollup**. Carry the per-slice vector; do **not** present a packet-flat single value (the producer is per-slice, `models.py:117-143`; the no-hide rollup mirrors the producer's own honesty validator `packet_assembly.py`). Whether the ratified field should carry a structured per-slice vector vs a flat value + residual is an owner/architecture refinement the adopted plan itself marked `not_proven`.

### 2.2 Derivation spec (residual-first) — promoted from the adopted SP-6 plan

Inputs (all read from `SourceCapturePacket`; see 2.3). Per-slice, first-match-wins; "—" = not examined.

| # | A `archive_history_posture` | D archive-date class | C current present | M recorded comparison | -> result | Fires to a value today? |
|---|---|---|---|---|---|---|
| 1 | `not_applicable` (X confirms immutable/official) | — | — | — | `not_applicable` | yes |
| 2 | `not_attempted` | — | — | — | `not_attempted` | yes |
| 3 | `attempt_failed` | — | — | — | `attempt_failed` | yes |
| 4 | `archived` | `post_cutoff_dated` | `current_absent` | — | `archive_post_cutoff_only` | yes (when D resolvable) |
| 5 | `archived` | `post_cutoff_dated` | `current_present` | — | `RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT` | residual |
| 6 | `archived` | `pre_cutoff_dated` | `current_absent` | — | `archive_only` | yes (when D resolvable) |
| 7 | `archived` | `pre_cutoff_dated` | `current_present` | `match` | `archive_corroborated` | **no -> row 9 today** |
| 8 | `archived` | `pre_cutoff_dated` | `current_present` | `differ` / `R=conflict` | `archive_diverged` | **no -> row 9 today** |
| 9 | `archived` | `pre_cutoff_dated` | `current_present` | `absent` | `RESIDUAL_COMPARISON_NOT_RECORDED` | **yes (live path)** |
| 10 | `archived` | `date_unknown` | — | — | `RESIDUAL_ARCHIVE_DATE_UNKNOWN` | residual |
| 11 | none / `not_attempted` | — | `current_present` | — | `current_capture_only` | yes |
| 12 | `unknown_with_reason` (status) | — | — | — | `RESIDUAL_ARCHIVE_POSTURE_UNKNOWN` | residual |
| 13 | any | — | `current_absent` AND no archive body | — | `RESIDUAL_NO_VISIBILITY_BASIS` | residual |

**Rollup (Ob.10 no-hide):** all relevant slices same -> that value; any divergence including a weaker/limitation state -> `RESIDUAL_SLICE_DIVERGENT_VISIBILITY` carrying the per-slice vector; never collapse to the strongest slice.

**D1 (unchanged), citing the producer:** rows 1-4/6/11 fire to a closed value today; rows 5/10/12/13 fire fail-safe to a residual; **rows 7-8 do not fire today** — they require a *recorded* `M` (archive-vs-current comparison) the producer does not store, so a `{archived, pre_cutoff, current_present}` slice routes to **row 9 -> `RESIDUAL_COMPARISON_NOT_RECORDED`**. The field never computes `M`, never diffs, never asserts materiality (downstream Judgment; boundary `:173-176`).

### 2.3 Upstream references (each input -> exact producer path)

| Var | Binds to | Source | Note |
|---|---|---|---|
| **A** | `SourceCaptureSlice.archive_history_posture` (rollup: packet-level) | `models.py:122,176`; closed set `:54`; validators `:132-136,188-192` | Closed `{archived, attempt_failed}` on `known`; other states via `VisibleFactStatus`. |
| **D** | `archive_availability.selected_snapshot.timestamp` else `archive_snapshot_body` slice timing via `_source_time` | `source_quality.py:169,405-412,434-446` | **Implemented convention, not a contracted field** (top delta-sensitivity). Never `cutoff_posture`. |
| **C** | `PreservedFile{relative_packet_path, sha256}` via a non-archive slice's `preserved_file_ids` | `models.py:97-103,127,202-219` | Current-capture body presence. |
| **R** | `SourceCaptureSlice.re_capture_relationship` (rollup: packet-level) | `models.py:124,178`; closed set `:55`; validators `:138-142,193-198` | `conflict` is a divergence signal in row 8 only when `M` is also present; never alone. |
| **M** | *No producer field* — read only if an authorized capture step recorded it | absent (grep) | The rule never computes `M`. Absent -> row 9. The D1 gap. |
| **X** | `SourceCapturePacket.capture_context` (`VisibleFact`) | `models.py:168` | **Consumed, not designed**; confirms an immutable/official source for row 1 only. Selects no other value. |
| **P** | `access_posture` (Ob.11, OPEN) | `models.py:121,175`; left open `:52` | **Never an input to the value.** Residual annotation only. The one legitimate access->visibility interaction surfaces through the *closed* `archive_history_posture = attempt_failed` (row 3). |

### 2.4 Recomputation / verifiability basis (D3) + the `hash_basis` correction

This is the **SP-2 sibling read**, kept strictly separate from SP-6 (SP-6 = "are the bytes the pre-cutoff state?"; SP-2 = "can we re-check the exact bytes we hold?" — the AR-01 conflation was merging them). **Only the carried basis is named here; the SP-2 field itself is a deferred sibling, not designed.**

- **Primary basis (corrected):** upstream `PreservedFile.sha256` + `PreservedFile.hash_basis` (`models.py:102`), carried downstream by reference. `hash_basis` is now a **closed, recomputation-bound, upstream-owned** token (`HASH_BASIS_VALUES = {raw_stored_bytes}`, `:66`; AR-04 validator `:105-114`) meaning `sha256 == sha256(read_bytes(packet_dir / relative_packet_path))`.
- **Re-ranks the adopted plan's fallback.** The plan (pinned at `e4e854e`) asserts "no `hash_basis` on `SourceCapturePacket`" and falls back to an owner-bound acquisition receipt (`jsg01_sp6_..._v0.md:202-208`). In committed source the closed `PreservedFile.hash_basis` is the **primary**; the acquisition-receipt path becomes the **fallback** (for pre-R2 `v0` packets that lack `hash_basis`).
- **R2 status (was adversary F8 fence; now resolved):** R2 is **committed** — `git show HEAD:...models.py` returns the closed posture vocabularies + `PreservedFile.hash_basis` + validators (landed at `102a171`, an ancestor of HEAD; re-verified by reading the committed source this turn). The earlier "uncommitted / `not_proven`" fence is lifted. Residual: R2's own test suite was not re-run this turn (its implementation review settled on record, manifest `v0->v1`). The ECR slice still must not strict-bind "SP-2 clears because `hash_basis` is enforced" — that is the deferred SP-2 sibling's call, not this slice's.
- **Not re-authored downstream (D3 core):** `EvidenceUnit.hash_basis` is an un-closed `str` (`case_models.py:61`) — a transport, not the authoring home. The ECR carries the upstream `PreservedFile.{sha256, hash_basis}` by reference. This is the structural fix for the translator's three-representation drift: one owner (the producer), carried by reference, no downstream re-authoring.

### 2.5 Supersession of the interim translator SP-6

- **What it replaces.** The translator authored `source_visibility_posture` as a docs-coined field bound *to* the downstream `EvidenceUnit` (`jsg01_source_side_receipt_translator_v0.md:252-264`) — its own sweep flags this as duplicating the Armory's `archive_history_posture`/`access_posture`/`re_capture_relationship` and colliding by-name with `PacketTiming.cutoff_posture` (`:443-453`). The ECR field supersedes that definition: **same name, re-seated to derive FROM the upstream producer facts**, killing the duplication at the root.
- **What the adapter becomes.** The translator's thin `EvidenceUnit` adapter row for `source_visibility_posture` (which itself notes "no single harness field carries this," `:262`) is **retired, not migrated**: the value derives upstream and is carried by reference; the adapter row collapses to a pointer.
- **How the three errors resolve.** Parallel-name/duplication -> resolved by **binding, not coining** (D4). `cutoff_posture` by-name collision -> resolved by keeping the producer's implemented `PacketTiming.cutoff_posture` as a real `VisibleFact` and not minting a same-named ECR enum; SP-6's `D` input uses archive-date metadata/timing convention and never treats `cutoff_posture` as a timestamp. Downstream-bind -> resolved by the **upstream rebind** (D3).
- **CRITICAL supersession boundary (verified).** This supersession is a **target relationship this plan describes; it is NOT an edit performed here.** The obligation contract's R2 propagation receipt records the `jsg01_*` docs as `intentionally_not_updated` because the JSG-01 source-side consumer is **FROZEN and ECR/JSG-lane-owned; coordination is by re-courier, not by editing the consumer.** The act of rewriting/retiring the translator's SP-6 is owner/ECR-lane-reserved and gated on JSG-01 unfreeze + ratification — outside this advisory slice.

---

## Part 3 — Adversarial findings (synthesized from the adversary/integrator lane)

Severity = priority only, not a verdict. Each has a minimum closure condition.

- **AF-1 — The owner-opened scope is doctrinally load-bearing and currently unwritten (critical; scope-creep / JSG-01-integrity).** Declaring an ECR field is the act the boundary doc reserves (`:292,309`; adopted plan Option-B table). The "source-visibility only" bound lives only in the prompt; the boundary doc still reads `PROPOSED_FREEZE` with the consolidation reserved. **Closure:** the design states the owner-opened scope verbatim as a fenced boundary (done: Status block + 1.4), cites that boundary `:288-290,293` stay OUT, and records that the **boundary-doc edit recording the open is itself owner-reserved/downstream** (done: §5 routing object). Without the last clause the design would leak into editing the reserved doc.
- **AF-2 — A *stored* SP-6 field would pre-commit siblings and re-create the producer fork (critical; premature-freeze / layer-violation).** **Closure:** INV-3 (no persisted capture field; no migration); SP-6 is a derived read, deleted not migrated. Block any proposal to persist SP-6 to a packet or ECR record.
- **AF-3 — A packet-flat 8-value enum is inconsistent with the per-slice rollup and the eventual consolidation (major; consolidation-inconsistency).** **Closure:** design the field as a per-slice vector + Ob.10 no-hide rollup (2.1); the flat-vs-structured final shape is an owner/architecture refinement (plan `not_proven`).
- **AF-4 — `archive_corroborated`/`archive_diverged` import a comparison + materiality the producer lacks and Judgment owns (critical; layer-violation / residual-leakage).** **Closure:** rows 7-8 route to `RESIDUAL_COMPARISON_NOT_RECORDED` whenever `M` is unrecorded (today: always); state D1 as a finding the owner must ratify; the slice covers the derivable subset only.
- **AF-5 — `access_posture` (Ob.11) free-text must never select a value (major; layer-violation).** **Closure:** `P` is a residual annotation, never an input; closing Ob.11 is a separate capture-lane decision the ECR may not make.
- **AF-6 — Residual ownership: grade, finalization, materiality, and the boundary-doc edit stay owner-reserved/downstream (major; residual-leakage).** **Closure:** the field emits value-or-residual with no `clears`/grade, no materiality, no finalization staffing, no boundary-doc edit, no JSG-01 unfreeze.
- **AF-7 — Anti-anchoring: "author the field now" is a candidate, not a given (major; scope-creep / premature-freeze).** The adopted plan recommended the gate-interim reader and explicitly did **not** enter the consolidation; "opened the consolidation" does not strictly entail "declare a field this turn," and a field presupposes accepting the ECR object exists. **Closure (owner choice surfaced):** at ratification the owner picks **(A) ratify the declared ECR field** (this plan's commission/recommendation) or **(B) ratify only the derivation contract (the 13-row spec) as the seed, deferring the field declaration**. The frame is identical and reversible either way. This plan designs (A) per the commission while naming (B) as the strictly-smaller alternative. **Owner direction (provisional, "for now"): B** — ratify the derivation contract as the seed; defer declaring `source_visibility_posture` as a standing ECR field and defer "the ECR is the object." Formal ratification (boundary-doc edit + DCP) is still pending and owner-gated.
- **AF-8 — R2 / `hash_basis` dependency (RESOLVED on the commit side).** R2 has since been **committed** (`102a171`, an ancestor of HEAD; re-verified by reading the committed source this turn) — the earlier "working-tree-only / uncommitted / `not_proven`" hazard is lifted. **Strengthens** D3's direction: a real closed coverage token now exists upstream, in committed source. **Residual closure:** still re-point D3 to upstream `PreservedFile.{sha256, hash_basis}` as primary (done, 2.4); still do not strict-bind "SP-2 clears because `hash_basis` is enforced" (the deferred SP-2 sibling's call); a fresh suite-green at HEAD was not run this turn; re-verify the archive-dating convention (`source_quality.py`) is unchanged on any re-courier.
- **AF-9 — The slice must not become a backdoor to the capture->EvidenceUnit bridge (minor-major; scope-creep).** **Closure:** SP-6 reads the upstream packet and emits a derived value; it does not design, populate, or adapt to `EvidenceUnit`; the bridge (`packing_to_harness_foundation_interface_architecture_v3.md`) stays a one-line deferred implication.

**Anti-anchoring note.** All three advisory lanes converged on the derived-projection design. Convergence among same-family lanes is **not** proof; it is preserved here only because each lane independently verified the load-bearing source facts (producer absences, `hash_basis` presence, the reserved boundary lines). Of the live owner choices: AF-7 = B per owner direction this turn (recorded), AF-8 is resolved on the commit side (R2 committed at `102a171`), and the flat-vs-vector shape stays open.

---

## Recommendation with decisive criteria

**Recommend the thin frame (1.1-1.6) and SP-6 as the first ECR field (2.1-2.5), as an advisory design for owner ratification; do not design siblings. Per owner direction this turn, ratification targets AF-7 option B — ratify the derivation contract as the seed, defer the field declaration. (R2/`hash_basis` is now committed at `102a171`, not working-tree-only.)**

Decisive criteria (each met):
1. **Authority / scope** — designs only the owner-opened source-visibility increment; the full field architecture and the boundary-doc edit stay owner-reserved.
2. **No-fork / single-writer** — derived projection over the producer's closed facts; no second writer; no stored capture field (INV-1, INV-3).
3. **Upstream-owned / carried (D3)** — verifiability basis lives at the producer and is carried by reference; never re-authored downstream.
4. **Fail-safe mechanicalness (D1)** — one closed value or one named residual per unit; never guesses, diffs, force-maps free text, or asserts materiality/grade.
5. **Reversibility** — the field is deleted, not migrated, if the full consolidation supersedes it; the table is the forward spec.
6. **Premature-freeze held** — the three-mode binding rule fixes *where authority lives*, not sibling field shapes; siblings named-but-deferred.

**What would change this:** an owner decision to add the missing facts capture-side (a first-class archive-date fact and/or a recorded comparison) moves the currently residual SP-6 rows toward M1/M2 (frame unchanged); a **revert or amendment of the committed R2** (`102a171`); a re-couriered delta to the archive-dating convention or the closed posture vocabularies. (AF-7 option B is now the owner's chosen direction, recorded above.)

---

## Deferred implementation implications (non-executable; do not build now)

- **Capture->ECR->harness bridge** — `packing_to_harness_foundation_interface_architecture_v3.md` (finalization owner-reserved); the missing capture->EvidenceUnit bridge is named, not designed.
- **Sibling ECR fields** — the 1.4 list; each picks its binding mode by the same rule when separately authorized.
- **Capture-side missing facts** — a first-class archive-snapshot-date fact and a recorded archive-vs-current comparison fact are **Armory (capture-side) + owner decisions**, not ECR work (D1/D2 fork).
- **R2 commit + revalidation** — DONE on the commit side: the closed posture vocabularies + `PreservedFile.hash_basis` are committed (`102a171`) and re-verified against HEAD this turn. Residual: a fresh suite-green at HEAD was not run this turn (R2's implementation review settled on record).
- **Boundary-doc update + DCP** — at ratification the owner edits the boundary doc to record the opened-and-bounded consolidation and carries a `direction_change_propagation` receipt (`architecture_doctrine`; related `lifecycle_boundary`). Not done here.

---

## Smallest complete next routing object

```yaml
next_routing_object:
  type: independent_cross_family_review -> owner_ratification
  primary_result: TARGET_RECOMMENDED (thin ECR frame + SP-6 as first ECR field; advisory)
  recommend_to_owner:
    ratify: the frame invariants (INV-1..INV-5) + the three-mode binding rule + SP-6 derivation contract over the derivable subset
    choose (AF-7): owner direction this turn = (B) ratify only the derivation contract as the seed (defer the field declaration); (A) declare the ECR field remains the deferred larger commitment
    do_not: design sibling ECR fields; persist any SP-6 capture field; compute archive/current diff;
            branch on access_posture/capture_context free-text; edit/ratify the boundary doc here;
            strict-bind "SP-2 clears because hash_basis is enforced" (the deferred SP-2 sibling's call)
  review_must_recheck:
    - D1 residuals (rows 7-9) still route correctly with today's producer
    - the per-slice vector + Ob.10 no-hide rollup shape (AF-3)
    - the now-committed R2 / hash_basis dependency (102a171) and the SP-2 basis re-point (AF-8 resolved on the commit side)
    - model-diverse / cross-family (the adopted plan and translator both flag same-family self-review risk)
  preconditions_before_ratification:
    - R2 commit DONE (102a171); residual = optional fresh suite-green at HEAD (review settled on record)
    - owner resolves D2 (where the missing archive-date / comparison facts live: capture-side vs deferred)
  unchanged:
    - JSG-01 stays FROZEN (indeterminate). Not unfrozen, bound, or ratified.
    - SP-5 finalization + SP-6 sufficiency grade + materiality remain owner-reserved/downstream.
    - Full ECR field architecture not designed. No capture execution authorized. No boundary-doc edit performed.
  not_proven:
    - That R2's test suite is green at HEAD (committed at 102a171 and re-verified by read, but suite not re-run this turn).
    - That SP-6 is fully mechanical (it is not, for archive_corroborated/archive_diverged).
    - That a flat 8-value field shape is correct (per-slice vector + no-hide rollup recommended).
```

---

## Quality-gate self-check (gates must be able to fail)

- **Frame holistic enough to host the slice without pre-committing sibling field shapes** — PASS. The binding rule selects a mode by where-authority-lives; siblings re-run the test independently.
- **Slice designs only source-visibility; siblings named-deferred, not designed** — PASS. SP-2 appears only as a deferred sibling whose *carried basis* the slice references (overbuild STOP held — the slice needed only the reference, not SP-2's design).
- **No scope creep into the full consolidation** — PASS, with AF-1 fenced (scope stated verbatim; boundary-doc edit deferred) and AF-7 surfaced as an owner choice.
- **Upstream-owned/carried (D3) preserved; no downstream re-authoring; no new capture fact authored** — PASS (INV-1..INV-5; 2.3/2.4).
- **Three representations accounted for without designing all their fields** — PASS (roles fixed; drift reconciliation deferred).
- **JSG-01 not unfrozen; finalization + sufficiency grade + materiality owner-reserved; D1 residuals preserved** — PASS.
- **R2 / hash_basis correction carried without overclaiming** — PASS. R2 is committed (`102a171`) and re-verified against HEAD; the correction re-points the SP-2 basis on committed source. Residual (not hidden): R2's suite was not re-run this turn.

---

## Doctrine status (no DCP receipt required this turn)

This artifact does not change a durable rule future agents must follow: it recommends but binds nothing, JSG-01 stays frozen, the translator stays PROPOSED and is not edited, the boundary doc and obligation contract are unchanged, and no controlling source's rule is edited. Per `.agents/workflow-overlay/source-of-truth.md`, the **doctrine-changing step is the LATER owner ratification** that opens-and-records the consolidation (boundary-doc edit) and adopts the frame + slice — that step must carry the `direction_change_propagation` receipt (`architecture_doctrine`; related `lifecycle_boundary`), not this advisory plan.

## Non-claims

Architecture-planning / design only. Not implementation, validation, ratification, JSG-01 unfreeze, the full ECR field architecture, the boundary-doc edit, the SP-6 sufficiency grade, materiality, SP-5 finalization, or capture execution. The owner opening the consolidation is authorized **scoped to source-visibility**; this lane designs that scoped increment and nothing wider. R2 / `PreservedFile.hash_basis` is committed (`102a171`) and re-verified against HEAD this turn; this plan itself remains advisory (untracked) and ratifies nothing.

## Source-read ledger + advisory disclosure

- **Hash-pinned (verified = prompt pins, 3/3 match):** `jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` (`03310806…02AB`), `jsg01_source_side_receipt_translator_v0.md` (`E8944D13…92B2`), `data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` (`F873C0EA…0B27`). All untracked at `02d2ff0`.
- **Read directly (lane):** the three pinned docs; `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (modified; reserved consolidation 281-309, Inclusion State Rule 158-176, ECR owns/must-not 74-75); `orca-harness/source_capture/models.py` (modified; SourceCapturePacket/VisibleFact/PreservedFile/SourceCaptureSlice/PacketTiming + the verified hash_basis + closed vocabularies); `orca-harness/source_capture/source_quality.py` (modified; archive-dating + `_source_time` decoupling); `orca-harness/schemas/case_models.py` (`EvidenceUnit.hash_basis:61`).
- **Read by subagents (each ran its own source-readiness gate):** the IPF Evidence Unit standard; `pydantic_schema_reference.md`; `packet_assembly.py`; the obligation contract (Ob.7-16 + the R2 closure note); the packing bridge; `adapters/archive_org.py`. SA-3 (at the time of the design run) verified via `git show HEAD:` that the R2 changes were then uncommitted; they have since been committed (`102a171`) and re-verified against HEAD this turn.
- **Methods:** `workflow-deep-thinking` and `workflow-architecture-planning` REFERENCE-LOADED (source `agent-workflow` cache `0.1.50`) before source loading; APPLIED after `SOURCE_CONTEXT_READY`. Resolver behavior not proven in-thread (skill-adoption overlay records `0.1.19`; cache observed at `0.1.50` — advisory mechanics only, non-authority).
- **Advisory sub-lanes (3, prompt-authorized, general-purpose, inherited model):** SA-1 ECR frame architect; SA-2 source-visibility slice architect; SA-3 adversary/integrator. Each returned advisory-only, non-verdict output and ran its own readiness gate. The lane owns this synthesis and did not treat lane agreement as proof; the convergence is preserved only on independently verified source, and the live owner choices (AF-7, AF-8, field shape) are left open.
- **Advisory disclosure:** the SP-6/ECR controlling docs are untracked (R2 itself is now committed, `102a171`) -> this is advisory architecture planning. No readiness, acceptance, validation, or ratification is claimed.

This is advisory input only. It is not a verdict, not implementation authority, and not proof of readiness.
