# JSG-01 SP-6 Source-Visibility Derivation — Architecture Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Non-executing architecture routing object for the JSG-01 SP-6
  (source_visibility_posture) derivation: the ownership-boundary decision
  (JSG-01-interim reader vs future-ECR-owned), the mechanical derivation-rule
  shape over the frozen capture contract, and the SP-2 verifiability check shape.
  Advisory planning only; recommends but does not select the owner-reserved fork.
use_when:
  - Deciding where the SP-6 derivation lives before JSG-01 unfreeze / ratification.
  - Building or reviewing the SP-6 derivation rule against the capture contract.
  - Preparing the owner decision on whether to open the ECR consolidation for SP-6.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/source_side_receipts/jsg01_source_side_receipt_translator_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
input_hashes:
  docs/product/jsg01_source_side_receipt_translator_v0.md: E8944D13FF8B3FAF62AC24209EC50FDA7C03CC9D4F906687246B2E15C01592B2
branch_or_commit: main @ e4e854e (worktree dirty; SP-6 controlling sources untracked, hash-verified)
downstream_consumers:
  - docs/product/jsg01_source_side_receipt_translator_v0.md  # SP-6 design correction input; not yet wired
stale_if:
  - The owner opens (or declines) the ECR/EvidenceUnit consolidation for source-visibility.
  - The capture-build lane re-couriers a frozen-contract delta (esp. archive vocabulary, archive-snapshot dating, or the capture-context field shape).
  - orca-harness/source_capture/models.py changes the SourceCapturePacket posture fields or PreservedFile shape.
  - The JSG-01 source-side receipt translator is ratified, amended, or rejected.
```

- Status: `PROPOSED_ARCHITECTURE_ROUTING_OBJECT` — advisory planning, **non-executing**.
- Gate posture: **JSG-01 stays FROZEN.** This plan does not bind, ratify, or unfreeze anything.
- Owner-reserved: the A/B ownership call **where it touches the ECR consolidation** (Option B), and any entry into that consolidation, are reserved to the owner. This lane develops and recommends; it does not select Option B and did not enter the consolidation.
- Strict-claim boundary: controlling SP-6 sources are untracked/modified → advisory only. No readiness/acceptance/validation/ratification claim.

---

## Human Summary

**Decision (lane judgment).** Recommend **Option A — a JSG-01-interim, gate-side *derived reader*** as the home for the SP-6 `source_visibility_posture` derivation, **with six guards**, scoped to the subset SP-6 can actually derive mechanically. This aligns with the prompt author's prior (A-interim) but hardens it on two points the prior under-weighted. The opposing question — *whether to open the reserved ECR consolidation so SP-6 becomes an ECR-owned field (Option B)* — is **owner-reserved** and returned as `OPTIONS_COMPARED_NO_SELECTION` / `AUTHORITY_BLOCKED`, not decided here.

**Two hardenings of the A-interim prior, both source-grounded:**
- **Bind upstream, not downstream.** The current translator derives SP-6 toward the *downstream* harness `EvidenceUnit` and coins a parallel `source_visibility_posture` name. Its own DCP receipt flags this as a material acceptance risk: it duplicates the **already-implemented** Source Capture Armory facts (`archive_history_posture` + `access_posture` + `re_capture_relationship`) and collides by-name with `PacketTiming.cutoff_posture`. Option A must read the **upstream `SourceCapturePacket` (CapturePacket) producer** and emit a *derived, non-persisted* value — not a new stored capture field (which would be the fork).
- **SP-6 is not fully mechanically derivable from current producer facts — and this is option-independent.** Of the eight closed SP-6 values, `archive_corroborated` and `archive_diverged` require a recorded archive-vs-current **comparison** the producer does not store (and computing it is unauthorized capture + a downstream materiality judgment). The honest rule emits **named residuals** there, never a guessed value.

**Scope / boundary.** Design-only. Nothing built, ratified, or unfrozen. SP-6 records the **value** only; the sufficiency **grade** (owner residual #2) and finalization authority (owner residual #1) stay owner-reserved; "material" divergence stays a downstream Judgment call.

**Next action (smallest complete).** An **owner decision request** (not an artifact, not a selection): adopt Option A-with-guards as the *interim* home over the derivable subset, and decide the owner-reserved fork — whether the missing inputs (archive-snapshot dating as a first-class fact; a recorded comparison) are added **capture-side** (Armory) or **deferred to the ECR consolidation** (Option B). Plus resolve the SP-2 read-layer (`PreservedFile.sha256` + recomputation basis at the producer, vs `EvidenceUnit.hash_basis` downstream).

**What remains blocked.** Option B selection and ECR-consolidation entry (owner-reserved); JSG-01 unfreeze; the SP-6 sufficiency grade; SP-5 finalization; performing any archive fetch/diff.

---

## Architecture Result

| Question | Result | Why |
|---|---|---|
| Where does the **interim** SP-6 derivation live? | `TARGET_RECOMMENDED` → **Option A (guarded interim reader, upstream-bound)** | Not owner-reserved; no producer-schema change; reversible; fail-safe. Selection threshold met for the *interim* home. |
| Should SP-6 become an **ECR-owned** field now (Option B)? | `OPTIONS_COMPARED_NO_SELECTION` + `AUTHORITY_BLOCKED` | Option B *begins defining the ECR receipt* = enters the reserved consolidation (boundary doc lines 292, 309). Owner-reserved; lane must not select. |
| Is SP-6 fully mechanically derivable today? | **NO (finding)** — 2 of 8 values are not | `archive_corroborated`/`archive_diverged` need a recorded comparison the producer does not store. Resolved by named residuals + an owner-reserved input decision. |

---

## Decision frame (what the A/B call actually is)

JSG-01's source-side subpredicates are `indeterminate_until_authored` because no ECR field schema exists yet. SP-6 (`source_visibility_posture`) was added by AR-01 to record that 2026 live-captured bytes do **not** establish *pre-cutoff visibility* (the Canoo overclaim). The derivation maps frozen-contract capture inputs → one of eight closed SP-6 values or a residual.

The structural fork:
- **Option A** — a JSG-01-side *interim reader rule*: the gate derives SP-6 at evaluation time from already-produced capture facts. No new stored field. Cites IPF-until-consolidation. Explicitly throwaway.
- **Option B** — a *future-ECR-owned rule*: SP-6 becomes the first authored field of the deferred ECR/EvidenceUnit consolidation — i.e., it stops pointing at a future home and *becomes* that home.

Decisive context that reframes both: the **Source Capture Armory `SourceCapturePacket` is the implemented, obligation-contract-bound upstream producer** of the SP-6 inputs (`orca-harness/source_capture/models.py`). The frozen contract is essentially that producer's contract restated. So the real axes are **(1) ownership** (gate-interim vs ECR) and **(2) input-binding** (read the upstream producer vs adapt to the downstream harness EvidenceUnit). The translator chose gate-interim but bound downstream and coined parallel names — the input-binding error is separable from, and more urgent than, the ownership choice.

Questions this decision must answer: where the rule sits without forking the producer; whether the rule is truly mechanical; how `access_posture` free-text is handled; how slice-level postures roll up without hiding a worse state; where SP-2 verifiability binds; and what is owner-reserved.

---

## Option A — JSG-01-interim reader rule (developed)

**Where it sits: a gate-side *derived* value, not a stored capture field.** Decisive criteria:
- **No-fork integrity.** The Armory is the single implemented source-side writer; its design intent is "close postures once, at the source, so downstream readers don't re-interpret free text" (`models.py:48-52`). A *stored* SP-6 field adds a second writer for visibility posture the producer already covers → the DCP-flagged fork. A *derived reader* has no writer and cannot fork.
- **Frozen / docs-only safe.** A reader changes no producer bytes and requires no archive fetch (performing fetch/diff is unauthorized capture, per the translator's own SP-6 scope boundary). It computes from packets that already exist.
- **Reversible / interim.** A derived projection is *deleted*, not migrated, when the consolidation lands; a stored field pre-commits the reserved field architecture.
- **Correction to the translator's framing:** derive from the **upstream `SourceCapturePacket`** (which carries the closed Ob.10/Ob.15 postures + per-slice timing), not the looser downstream `EvidenceUnit` (which re-introduces the AR-01 inability to tell archive-dated bytes from current bytes). This is the DCP receipt's own recommendation.

**Derivation-rule shape:** see the dedicated section below (shared by both options).

**`access_posture` residual handling:** Ob.11 `access_posture` is intentionally open free-text; it is **not** an input to the value and is carried as a verbatim residual annotation only (see below).

**Migrate-to-ECR-later implications:** A is built to be deleted, not migrated. No stored field to reconcile; the derivation table becomes the behavior spec the future ECR field must satisfy; the conductor reference stays a pointer (one-line retirement); the `source_visibility_posture` label stays an internal computed name the consolidation can rename/absorb; no grade is pre-committed.

**Pros:** removes the fork/collision; stays inside frozen/docs-only; mechanical + fail-safe; cleanly reversible; reuses implemented dating mechanics; keeps SP-2 (verifiability) separate from SP-6 (visibility), killing the AR-01 conflation.
**Cons:** recompute-at-evaluation (value can shift if packets mutate; mitigated by write-time-closed postures); honestly residual-heavy on today's fixtures (Canoo → `current_capture_only`; Unity EU-07 archive present but SP-2-fails); depends on a slice/availability **convention** (`archive_snapshot_body`, `archive_availability.selected_snapshot`) that lives in `source_quality.py`, not the obligation contract; interim by construction (defers the reserved question visibly).

---

## Option B — future-ECR-owned rule (developed; owner-reserved, NOT selected)

**How it begins the ECR field architecture:** promote `source_visibility_posture` from "authored-FROM IPF, adapter-TO harness" to "authored-AS an ECR receipt field," with the ECR receipt deriving it from the upstream Armory `VisibleFact`s (status+value+reason) reduced to one closed value. At design altitude B *names* the seed field, the upstream binding, and the reduction shape, then **surfaces the consolidation entry to the owner** — it does not author the field.

**Exact boundary with the reserved consolidation** (cited from `core_spine_v0_data_and_cleaning_spine_boundary_v0.md`):

| Reserved question | Touched? | How |
|---|---|---|
| `:292` "how snapshot/archive status relates to pre-cutoff visibility" | **Directly** | This *is* SP-6's value ladder. B authors it as the ECR's standing answer. |
| `:309` "Final ECR/Evidence Unit (EvidenceUnit) field architecture" | **Begins it** | Declaring an ECR field is the first authored increment — the single most owner-reserved line. |
| `:285` "which Evidence Unit fields are frozen core invariants" | By implication | Proposes a candidate core invariant. |
| `:286-287` "how capture handoff obligations become receipt fields without turning Data Spine into an ECR schema" | **Directly** | The upstream-bind is exactly this reserved mechanism. |
| `:291` inclusion-state/state-reason/layer ownership | Partial | SP-6 is the Capture-blocker arm of the Inclusion State Rule. |
| `:298` ECR canonical-vs-working name | By assumption | B must assume an ECR object to host a field. |
| `:288-290`, `:293` projection/Judgment-overlay refs | **No** | SP-6 is source-visibility only; fenced off. |

**Minimum owner authorization required before B could be selected:** (1) open the ECR consolidation, scoped to source-visibility only; (2) accept an ECR object exists as the field home (resolve `:298` at least provisionally); (3) authorize the upstream rebind (ECR derives from the Armory producer, not the harness EvidenceUnit) — a direction change; (4) confirm the residual split survives (SP-5 finalization + SP-6 grade stay owner-reserved); (5) re-affirm JSG-01 stays frozen during authoring. Items 1–2 are the gating, owner-reserved acts.

**Pros (what B buys that A cannot):** kills the duplication at the root (SP-6 = reduction of the producer's own facts, single source of truth); resolves the `cutoff_posture` name collision into one lineage; directionally correct (binds the receipt to its upstream producer, not a `retrieval_only` downstream consumer); puts the answer to `:292` in its reserved home rather than leaving it provisional.
**Cons:** crosses the owner-reserved line (dominant con); premature-freeze risk (authoring one ECR field while siblings are undesigned); larger blast radius / bigger propagation surface; inherits but does not fix the archive-dating gap; does **not** buy a cleared gate (JSG-01 still frozen; residuals still open).

---

## Adversarial findings on both (from the adversary/integrator lane)

**On Option A:**
- **A-fork gravity (guarded).** A is safe only as a pure projection over existing closed fields; the instant the derivation is non-total it tempts a stored field (the fork). → Guard G-1.
- **`access_posture` force-map (confirmed leak point).** Any branch reading `access_posture.value`/`capture_context.value` free-text to disambiguate is a hidden NLP judgment. → Guard G-2.
- **Materiality leak (confirmed).** `archive_corroborated`/`archive_diverged` import a match/materiality computation the producer doesn't store and the lane may not make. → Guard G-4.
- **Slice-vs-packet rollup (confirmed break).** Packet `{S1 archived, S2 attempt_failed, S3 live-only}` has **no** single SP-6 value that doesn't hide a worse state (violates Ob.10 rollup rule `:299-302`); the flat 8-value enum has no `mixed`/per-slice value. → Guard G-5.
- **SP-2 layer mismatch (confirmed).** Translator SP-2 assumes `EvidenceUnit.hash_basis`, but the upstream `SourceCapturePacket` has **no** `hash_basis` — only `PreservedFile.sha256`. → Guard G-6 + owner decision.
- **Layer leakage (capture-by-stealth).** A reader that re-emits a *capture posture* re-creates a capture-owned fact in the gate. → emit a derived, non-persisted value that is explicitly not the canonical Armory vocabulary; keep the clears/grade decision separate and owner-reserved.

**On Option B:**
- **Enters the reserved consolidation — by construction** (boundary `:292`/`:309`). Not selectable by the lane.
- **`access_posture`:** B's "fix" (close Ob.11) overrides a deliberate implemented design choice = doctrine change.
- **Delta "robustness" is scope expansion in disguise:** B absorbs the archive-dating delta by *adding the missing field* — which is the reserved consolidation work.
- **Institutionalizes the duplication** unless the consolidation also retires the Armory vocabulary (more reserved work).

**Adjudicated disagreement (archive-snapshot dating).** One advisory lane called the dating "fatal/non-mechanical"; another found an implemented mechanism. **Source resolves it** (`source_quality.py:165-169,405-446`): the archive snapshot date is derived from `archive_availability.selected_snapshot.timestamp` (preferred) or the `archive_snapshot_body` slice timing via `_source_time` (`source_edit_or_version`→`source_publication_or_event`, and explicitly **never** `cutoff_posture` — "a posture is not a time," `:435`). So `archive_only` vs `archive_post_cutoff_only` **is** mechanically separable when a snapshot timestamp is recorded, and **fails safe to `RESIDUAL_ARCHIVE_DATE_UNKNOWN`** when it is not. Only `archive_corroborated`/`archive_diverged` remain non-derivable (no stored comparison). The dating mechanism is an implemented **convention**, not a contracted producer field — so it is the top delta-sensitivity to re-verify.

---

## Recommendation with decisive criteria

**Recommend Option A (guarded interim reader, upstream-bound), scoped to the derivable subset; do NOT select Option B.**

Decisive criteria (each met):
1. **Authority** — A does not enter the reserved consolidation; B does. The lane may recommend A; it may not select B.
2. **No-fork** — A as a derived, non-persisted read over the producer's closed facts removes the DCP-flagged duplication/collision; a stored field or a downstream-bound coined field re-creates it.
3. **Fail-safe mechanicalness** — A emits one closed value *or* a named residual for every input combination; it never guesses, force-maps free-text, computes a diff, or asserts materiality/grade.
4. **Reversibility** — A is deleted (not migrated) by the consolidation; the table is the forward spec.
5. **Honesty** — A surfaces (does not hide) that 2 of 8 values are not derivable today and that SP-2 must name its read-layer.

What would change this: an owner ruling that current/live capture is sufficient (relaxes the *grade*, not the *where*); an owner decision to open the consolidation now (moves SP-6 to a stored ECR field — owner-reserved); or a re-couriered delta to the archive vocabulary / archive-dating convention / capture-context shape.

---

## SP-6 derivation-rule shape (design altitude, mechanical + fail-safe)

**Inputs (all read from `SourceCapturePacket`, per-slice then rolled up):**
- `A` = `archive_history_posture` — closed known `{archived, attempt_failed}` (`models.py:54`) + statuses `not_attempted`/`not_applicable`/`unknown_with_reason` (AR-05 union via `VisibleFactStatus`).
- `D` = **archive-snapshot date class** vs the packet cutoff: `{pre_cutoff_dated, post_cutoff_dated, date_unknown}`, sourced from `archive_availability.selected_snapshot.timestamp` (preferred) or the `archive_snapshot_body` slice timing (`_source_time`; never `cutoff_posture`).
- `C` = current-capture presence on a non-archive slice, from `PreservedFile{relative_packet_path, sha256}` + acquisition-receipt scope: `{current_present, current_absent}`.
- `R` = `re_capture_relationship` — closed `{supersede, supplement, conflict, mixed}` (`models.py:55`).
- `M` = **recorded** archive-vs-current comparison result, if and only if an authorized capture step stored one: `{match, differ, absent}`. The rule never computes `M`.
- `X` = `capture_context` VisibleFact — **consumed, not designed**; read only to confirm a cutoff-insensitive/immutable-official source for the `not_applicable` branch.
- `P` = `access_posture` (Ob.11, open free-text) — **never an input to the value**; residual annotation only.

**Output:** exactly one of `{archive_corroborated, archive_only, archive_diverged, current_capture_only, archive_post_cutoff_only, attempt_failed, not_attempted, not_applicable}` **or** a named residual.

**Per-slice decision table (top-down, first match wins; "—" = not examined):**

| # | A | D | C | M | → SP-6 |
|---|---|---|---|---|---|
| 1 | `not_applicable` (X confirms cutoff-insensitive/immutable-official) | — | — | — | `not_applicable` |
| 2 | `not_attempted` | — | — | — | `not_attempted` |
| 3 | `attempt_failed` | — | — | — | `attempt_failed` |
| 4 | `archived` | `post_cutoff_dated` | `current_absent` | — | `archive_post_cutoff_only` |
| 5 | `archived` | `post_cutoff_dated` | `current_present` | — | `RESIDUAL_ARCHIVE_POST_CUTOFF_WITH_CURRENT` (post-cutoff archive can't establish pre-cutoff visibility; current presence doesn't rescue it; don't collapse to `current_capture_only` and hide the archive) |
| 6 | `archived` | `pre_cutoff_dated` | `current_absent` | — | `archive_only` |
| 7 | `archived` | `pre_cutoff_dated` | `current_present` | `match` | `archive_corroborated` |
| 8 | `archived` | `pre_cutoff_dated` | `current_present` | `differ` (or `R=conflict`) | `archive_diverged` |
| 9 | `archived` | `pre_cutoff_dated` | `current_present` | `absent` | `RESIDUAL_COMPARISON_NOT_RECORDED` (can't pick corroborated vs diverged without a recorded diff — that is downstream Judgment) |
| 10 | `archived` | `date_unknown` | — | — | `RESIDUAL_ARCHIVE_DATE_UNKNOWN` (archive exists but snapshot date not a known timing fact) |
| 11 | `not_attempted`/none | — | `current_present` | — | `current_capture_only` |
| 12 | `unknown_with_reason` (status) | — | — | — | `RESIDUAL_ARCHIVE_POSTURE_UNKNOWN` |
| 13 | any | — | `current_absent` AND no archive body | — | `RESIDUAL_NO_VISIBILITY_BASIS` (capture-side blocker, Inclusion State Rule `:165`) |

**Packet rollup (Ob.10 no-hide rule `:299-308`):** compute per relevant slice, then: all-same → that value; any divergence that includes a weaker/limitation state → `RESIDUAL_SLICE_DIVERGENT_VISIBILITY` carrying the per-slice vector (**never** collapse to the strongest slice — that is the forbidden hidden-worse-state). A producer packet-level rollup posture may be read only when it does not contradict the per-slice vector.

**Why this is mechanical (and where it honestly is not):**
- No grade: emits value-or-residual only; which values "clear" at judgment-quality vs product-learning is owner residual #2.
- No materiality verdict: `M` is *read* if recorded, never computed; absent → residual (row 9). Deciding whether a divergence is material stays downstream Judgment.
- No archive fetch; no free-text map (`P`/`X` never select a value).
- **Honest limit:** `archive_corroborated`/`archive_diverged` (rows 7-8) fire only when an upstream authorized comparison recorded `M`; with today's producer (`M=absent`) they route to residual. The flat 8-value enum *implies* these are routinely derivable — they are not. This is the option-independent finding the owner must accept (D1 below).

**`access_posture` handling:** excluded from the table; carried verbatim as an advisory residual annotation beside the value/residual so the downstream grade decision and Judgment see access constraints without the gate pre-judging them. The one legitimate interaction (access prevented the archive attempt) surfaces through the **closed** `archive_history_posture = attempt_failed` (row 3), not through parsing free text. Preserves Ob.11 "Capture does not convert visibility limits into credibility effects."

---

## SP-2 verifiability check shape (against the recomputation basis)

**Constraint (source):** there is **no `hash_basis` field on `SourceCapturePacket`**. `PreservedFile` carries `{file_id, original_path, relative_packet_path, sha256, size_bytes}` (`models.py:86-91`); `hash_basis` exists only on the *downstream* harness `EvidenceUnit` (`case_models.py:61`). So at the producer layer the recomputation-coverage basis must come from `PreservedFile` + an owner-bound acquisition receipt, not a field.

SP-2 check shape (sibling reader to SP-6):
- **Re-checkability anchor:** `PreservedFile.relative_packet_path` resolves to a present byte file AND `PreservedFile.sha256` is non-placeholder (held bytes are re-hashable).
- **Coverage basis (AR-03, load-bearing):** a recorded statement of *what bytes* the `sha256` spans — from the recomputation binding (`relative_packet_path` + slice/encoding) or an owner-bound source-acquisition receipt (e.g., Canoo's "SHA-256 over captured local file bytes"). Absent → `inspectable_reference_only`/`not_inspectable`, never `inspectable_verifiable`. Residual: `RESIDUAL_NO_COVERAGE_BASIS`.
- **Strict separation from SP-6:** SP-2 = "can we re-check the exact bytes we hold?"; SP-6 = "are the bytes the *pre-cutoff* state?" The AR-01 failure was exactly conflating these. The reader surfaces SP-6's archive value **and** SP-2's verifiability state as two independent reads over the same `PreservedFile`/receipt, so an unverifiable archive cannot be laundered into established visibility (the Unity EU-07 case).
- **Owner decision:** which layer JSG-01 reads — the upstream `SourceCapturePacket` (`PreservedFile.sha256` + recomputation basis) or the downstream `EvidenceUnit.hash_basis`. The DCP finding favors upstream; this plan recommends upstream and routes the choice to the owner (D3).

---

## Core / satellite boundary and invariants later work must preserve

- **Core invariant:** SP-6 records a **posture value** (or residual); the sufficiency **grade**, finalization authority, and **materiality** judgment are *not* in the rule. Capture records; Judgment decides (boundary `:173-176`).
- **Core invariant:** the source-side **producer is single-writer** (the Armory). SP-6 is a *read*, never a second writer of visibility posture.
- **Core invariant:** Ob.11 `access_posture` stays open free-text and is never force-mapped into a closed value.
- **Core invariant:** rollups never hide a worse slice state (Ob.10).
- **Satellite / deferred:** the *grade* threshold, the finalization staffing, the ECR field architecture, and whether the missing inputs become capture facts — all owner/consolidation-owned.

---

## Deferred implementation implications + delta-robustness (ranked)

Non-executable notes (do not build now). Most→least delta-sensitive (re-verify on any re-courier):
1. **`archive_history_posture` closed set `{archived, attempt_failed}` (highest)** — rows pivot here; a delta adding values (e.g., `archived_pre_cutoff`) or moving `not_attempted`/`not_applicable` into closed values re-keys the table.
2. **Archive-snapshot **dating** mechanism (high, under-contracted)** — `D` depends on `archive_availability.selected_snapshot.timestamp` / `_source_time`, a `source_quality.py` convention, not obligation-contract text. A first-class archive-date field or a slice rename changes rows 4-10. Verify first.
3. **`capture_context` shape (high; consume-not-design)** — row 1 reads it; re-bind on delta, never redesign.
4. **SP-2 coverage basis / `hash_basis` absence (medium-high)** — if the consolidation adds `hash_basis` to the producer, prefer the field; the receipt becomes fallback.
5. **`re_capture_relationship` set (medium)** — rows 7-9 use `conflict` as a divergence signal.
6. **Ob.9 cutoff vocabulary (medium)** — used only to *class* the archive date, not to grade.
7. **`access_posture` openness (low)** — residual-only, so a delta closing it only enriches the annotation; most delta-robust.
8. **SP-6 value set (low for rule mechanics)** — the grade governs clearing, not the table.

**Cross-cutting robustness:** binding SP-6 to the **upstream producer** (under either A-done-right or B) is materially more robust than the translator's current downstream-EvidenceUnit bind, which is an explicit `stale_if` trigger.

---

## Smallest complete next routing object

```yaml
next_routing_object:
  type: owner_decision_request        # not an artifact write, not a selection
  primary_result: TARGET_RECOMMENDED (Option A interim reader, guarded, upstream-bound)
  reserved_result: OPTIONS_COMPARED_NO_SELECTION + AUTHORITY_BLOCKED (Option B / ECR consolidation)
  recommend_to_owner:
    interim_home: Option A over the derivable subset, bounded by guards G-1..G-6
    eventual_home: Option B (ECR consolidation) — RESERVED; do not enter now
    do_not: select B; close Ob.11; persist a source_visibility_posture capture field;
            compute archive/current diff; branch on access_posture/capture_context free-text
  owner_decisions_required:
    - D1: Accept SP-6 is NOT fully mechanically derivable today (archive_corroborated/
          archive_diverged need a recorded comparison; archive dating is convention-based,
          not a contracted field) -> the interim rule covers the derivable subset and
          emits named residuals elsewhere.
    - D2: Decide where the missing inputs live -- added as CAPTURE (Armory) facts
          (archive-snapshot dating; a recorded comparison) OR deferred to the ECR
          consolidation (Option B). This is the owner-reserved fork; the lane does not pick it.
    - D3: Resolve the SP-2 read-layer: SourceCapturePacket (PreservedFile.sha256 +
          recomputation basis) vs EvidenceUnit.hash_basis.
    - D4: Before any ratification, bind/reference the Armory access_posture +
          archive_history_posture + re_capture_relationship rather than coin parallel
          SP-6 vocabulary (the DCP-flagged acceptance risk).
  unchanged:
    - JSG-01 stays FROZEN (indeterminate). Not unfrozen, bound, or ratified.
    - SP-5 finalization + SP-6 sufficiency grade remain owner residuals.
    - No ECR consolidation entered. No capture execution authorized.
  not_proven:
    - That Option A is fully mechanical (it is not, for archive_corroborated/archive_diverged).
    - That a flat 8-value SP-6 enum is the right shape (Ob.10 rollup implies a
      per-slice / mixed discipline the enum currently lacks).
```

---

## Quality-gate self-check (gates must be able to fail)

- **Both options developed against the frozen contract with cited inputs** — PASS (Options A and B above, cited to `models.py`, the obligation contract, the boundary doc, the translator).
- **Derivation rule is mechanical (one value or named residual; no hidden judgment; no `access_posture` force-map)** — **PASS WITH FINDING.** The rule is mechanical *and fail-safe*, but only by emitting named residuals for `archive_corroborated`/`archive_diverged` (no stored comparison) and for date-unknown archives. The SP-6 flat enum implies more determinacy than current producer facts support — surfaced as D1, not hidden.
- **JSG-01 not unfrozen; ECR consolidation not entered; grade + finalization left owner-reserved; materiality left downstream** — PASS.
- **Delta-robustness named (esp. capture-context shape)** — PASS (ranked list; capture-context #3, archive vocabulary #1, dating mechanism #2).

---

## Owner-reserved note

The A/B ownership decision **where it touches the deferred ECR consolidation** (i.e., Option B) and **any entry into that consolidation** are reserved to the owner. This plan develops Option B and recommends Option A; it **did not select Option B** and **did not enter the consolidation**. Selecting B requires the explicit owner authorization scope enumerated under Option B.

## Non-claims

Architecture-planning / design only. Not implementation, validation, ratification, JSG-01 unfreeze, the ECR consolidation, the sufficiency threshold, or finalization authority. The frozen contract is a design basis, not landed or enforced state. Recommendations about the translator are planning input to an unratified PROPOSED artifact, not edits to it.

## Doctrine status (no DCP receipt required this turn)

This artifact does not change a durable rule future agents must follow: it recommends but binds nothing, JSG-01 stays frozen, the translator stays PROPOSED, the obligation contract and boundary doc are unchanged, and no controlling source's rule is edited. Per `.agents/workflow-overlay/source-of-truth.md`, the **doctrine-changing step would be a later owner ratification adopting Option A or Option B** (architecture_doctrine; related lifecycle_boundary) — that step must carry the `direction_change_propagation` receipt, not this advisory plan.

## Source-read ledger + advisory disclosure

- Sources: `jsg01_source_side_receipt_translator_v0.md` (untracked; SHA256 `E8944D13…92B2` = pin ✓), its adversarial review (untracked; AR-01/AR-03), `core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Ob.8-15), `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (modified; Inclusion State Rule 158-176, reserved consolidation 281-309), `orca-harness/source_capture/models.py`, `orca-harness/source_capture/source_quality.py` (archive-dating mechanism), `orca-harness/schemas/case_models.py` (`EvidenceUnit.hash_basis`).
- Methods: `workflow-deep-thinking` and `workflow-architecture-planning` REFERENCE-LOADED (cache `0.1.49`) before source loading; APPLIED after `SOURCE_CONTEXT_READY`. Resolver behavior not proven in-thread (skill-adoption overlay records `0.1.19`; cache observed at `0.1.49` — advisory mechanics only, non-authority).
- Advisory sub-lanes (3, prompt-authorized, general-purpose): SA-1 Option A architect, SA-2 Option B architect, SA-3 adversary/integrator. Each ran its own source-readiness gate and returned advisory-only, non-verdict output. One SA-1↔SA-3 disagreement (archive-snapshot dating) was adjudicated against `source_quality.py` (dating mechanism exists but is convention-based → fail-safe residual), not merged. The lane owns this synthesis.
