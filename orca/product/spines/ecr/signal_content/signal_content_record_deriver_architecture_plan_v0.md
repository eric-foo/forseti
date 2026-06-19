# Signal Content Record (SCR) Deriver — Derivation Architecture Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Non-executing architecture routing object for the Signal Content Record (SCR)
  deriver: the extraction contract (raw_observation -> a filled SignalContentRecord),
  the per-field M1/M2/M3 mapping, the honesty/residualize rules, the re-derive
  lifecycle, and the authored-input (signal_family + event-core) resolution. The
  next derived-record kind after the ECR SP-1/2/3/6 source-side derivers. Advisory
  planning only; recommends a target shape and surfaces owner-reserved decisions;
  builds nothing.
use_when:
  - Building or reviewing the SCR deriver against the v0 SignalContentRecord model.
  - Deciding the extraction/authored-input contract before any deriver build.
  - Resolving the signal_event_time honesty gap and the authorship boundary.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
  - orca-harness/signal_content/models.py
  - orca-harness/ecr/__init__.py
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ c912203 (worktree dirty; controlling sources pinned below)
input_pins:
  docs/product/core_spine_v0_signal_content_record_architecture_v0.md: committed 834c930 (controlling owner doc)
  orca-harness/signal_content/models.py: committed 834c930 (the v0 model derived INTO; 17 model tests green)
  orca-harness/ecr/ (SP-6 source-visibility deriver): committed 6329d71 (the pattern reused)
downstream_consumers:
  - The SCR deriver build (separately authorized) — receives this as its behavior spec.
stale_if:
  - signal_content/models.py changes the SignalContentRecord fields, SignalFamily / DecisionRelevance vocabularies, or the SignalEventTimeReference shape.
  - An authored signal-classification input record / SP-5-style finalizer is built (activates the dormant M2 lane).
  - The signal_event_time honesty gap (D2) is resolved by a model amendment.
  - The ECR-consolidation sequencing for this slice changes.
```

- Status: `PROPOSED_ARCHITECTURE_ROUTING_OBJECT` — advisory planning, **non-executing**.
- Gate posture: **JSG-01 stays FROZEN.** This plan does not build, bind, ratify, or unfreeze anything; the final Evidence Unit (EvidenceUnit) field architecture stays owner-reserved.
- Strict-claim boundary: controlling sources are pinned but the worktree is dirty (other-lane churn) → advisory only. No readiness / acceptance / validation / ratification claim. `docs-write` is authorized for this one plan doc; the deriver build is a separate, later authorization.
- Evidence: a standard 3-subagent architecture-planning panel (3 independent lenses) + home adjudication. See the source-read ledger.
- **Amendment v0.1 (owner-ratified).** A cross-vendor adversarial artifact review (`needs-architecture-pass`; 6 findings, all adjudicated ACCEPT) + a 3-subagent architecture-pass panel were adjudicated, and the **owner ratified** the result (D1, D2=b1, D3, D4-a, D5). See **Architecture-Pass Amendment v0.1** below. It supersedes these v0 statements: the deriver **signature** and **per-packet grain** (now per-slice), the per-field rows for `raw_observation` / `signal_event_time` / `ecr_posture_ref_ids` / `decision_relevance`, the **D1/D2/D3 owner-decision block** (now ratified), and the **"edits no model" non-claim** (one additive D2=b1 amendment is now scheduled). Still design-only; JSG-01 FROZEN.

---

## Human Summary

**Decision (lane judgment).** The SCR extraction is a **SPLIT**: a **mechanical carry-shell** (M1-carry of keys / raw text / timing-reference + M2 of a neutral routing tag) that **composes** an authored interpretive core (`signal_family` + the event-core), and **residualizes that core when the authored input is absent** — which is the **default today**, because no authored-classification input record and no SP-5-style finalizer exist in source (grep-confirmed, all three lenses). The deriver **carries-or-residualizes; it never authors.** The authored interpretive lane is **declared-but-dormant** (a named, typed seam — not built), exactly as SP-6's `archive_corroborated` / `archive_diverged` rows are declared-but-dormant behind a missing producer fact. `TARGET_RECOMMENDED`.

**Three source-grounded load-bearing points:**
- **The authored input does not exist → residualize is the default, surfaced as a finding (not a blocker).** Per the brief's own instruction (this is "like SP-5's deferred finalizer… likely needs a provenance-bound authored input, residualized when absent"). The mechanical half is buildable today and emits an honest record from a packet alone.
- **The deriver must not be the author (no testee-tester).** A mechanical family-classifier reading `raw_observation` prose would self-author the interpretation = the exact self-finalization the SP-5 decision (boundary doc decision B, `:303`) forbids ("distinct, cross-family, provenance-bound… same-model/same-family self-finalization disallowed"). So the interpretive core must be *authored-then-carried, or residualized* — never originated by the deriver.
- **One real honesty gap in the green model:** `signal_event_time` is a **required** reference with no unknown/absent path (it must name one of two `PacketTiming` fields). Under absence the deriver would be forced to assert an event-time it does not have — invent-by-construction. This is the one place v0 cannot stay honest-under-absence; it needs a small owner-decided model amendment (D2). The lane **names** it and does not pick the fix.

**Scope / boundary.** Design-only. Nothing built, ratified, or unfrozen. The deriver records the mechanical shell + residualizes the authored core; the authored mechanism, persistence/finalizer, EvidenceUnit binding, Cleaning, and Judgment stay separately gated.

**Next action (smallest complete).** An **owner decision request** (not an artifact, not a build): accept the residualize-default finding (D1), decide the `signal_event_time` honesty amendment (D2), confirm the authorship boundary (D3) — after which the mechanical carry-shell + residualize path is a clean, separately-authorized build slice (the direct sibling of `ecr/deriver.py`). A de-correlated adversarial *artifact* review is recommended before that build.

**What remains blocked.** The authored-classification input record + its provenance binding (the SP-5-style first deferred slice); the M2 interpretive activation; the deriver build; persistence/finalizer; any packet→EvidenceUnit binding; Cleaning; Judgment; commits/pushes; JSG-01 unfreeze.

---

## Architecture-Pass Amendment v0.1 (ratified)

> **Supersedes the v0 statements named in the status header.** Installed after a cross-vendor adversarial artifact review (verdict `needs-architecture-pass`; 6 findings, all adjudicated ACCEPT), a 3-subagent architecture-pass panel, and home adjudication; **owner-ratified** (D1, D2=b1, D3, D4-a, D5). Design-only; one model amendment **scheduled, not applied**; JSG-01 FROZEN. Design basis: the cross-vendor review + the panel adjudication (recorded in the DCP receipt).

**Carry-supplied-or-residualize invariant.** The deriver is a **pure function of its frozen inputs, but NOT packet-only.** It has four frozen input channels — the `SourceCapturePacket` (CapturePacket), caller-supplied `preserved_bodies`, caller-supplied `ecr_posture_refs`, and a caller-supplied `authored_interpretation`. Every emitted value is **carried** from one of these or is a **named residual**; where a frozen input is absent → honest residual. The deriver **never synthesizes, selects, classifies, or infers an interpretive value from packet prose** (`raw_observation`, `locator`, `requested_decision_context`, any packet text). The packet records *that a capture happened* + provenance/timing; the body, the event-time anchor, the ECR posture keys, and the interpretation are inputs the **caller supplies**.

**Amended deriver contract** (supersedes §"Bounded build scope teed up"):

```python
derive_signal_content(
    packet: SourceCapturePacket,
    *,
    preserved_bodies: Mapping[str, str],          # file_id -> verbatim source-language body; caller-supplied, frozen
    ecr_posture_refs: Sequence[str] = (),         # caller-materialized ECR posture KEYS; default empty
    authored_interpretation: AuthoredInterpretation | None = None,  # declared + dormant
) -> list[SignalContentRecord]
```

- Pure; no I/O; no mutation; binds no `EvidenceUnit`. The file-read that produces `preserved_bodies` lives in a **thin caller** (the SP-2 "recompute at the harness, never trust here" precedent).
- **Grain (D5): one record per `SourceCaptureSlice` that has a supplied body**, `references.slice_id` set on every record. A slice with **no supplied body → no record** (the emit gate — `raw_observation` is required non-empty; an empty/invented anchor is never emitted). Supersedes the v0 "per-packet length-1 list."

**Per-field deltas from the v0 table** (only changed rows; all others unchanged):

| Field | v0.1 mode + residual-default |
|---|---|
| `raw_observation` | M1 carry from `preserved_bodies[file_id]` (verbatim, caller-supplied) — **not** from the packet. The emit gate; never invented/empty. |
| `references.slice_id` | M1 (key), **always set** (per-slice grain). |
| `references.ecr_posture_ref_ids` | M1 from caller-supplied `ecr_posture_refs`; **default `[]`; never synthesized** (no `posture_id` exists; the link is already carried by the shared `packet_id`/`slice_id`). |
| `signal_event_time` | **D2 = (b1):** residual carrier is the **v0 default** — `{status: unknown_with_reason, packet_timing_field: None, reason}`; the deriver **never** mechanically selects publication-vs-edit. Requires the model amendment below. |
| `decision_relevance` | **v0 = always `UNRESOLVED`** (family always residual); **never inferred** from prose/context. The brief's "shape-derived" mechanism is **deferred to the authored lane**, not overturned. |
| `content_id` | Deterministic over **`(packet_id, slice_id)` only** — never mixes `raw_observation` bytes (re-derive stability). |

**The one model amendment (D2 = b1) — scheduled, NOT applied here.** `SignalEventTimeReference` (today `{packet_timing_field: SignalEventTimeField}`, required, no residual → a fully-residual record is non-constructible) gains a `VisibleFact`-style shape: `status: SignalEventTimeStatus = KNOWN` (additive default → existing constructions + the 17 tests unchanged), `packet_timing_field: SignalEventTimeField | None = None`, `reason: str | None = None`, with a validator (`KNOWN ⇒ field set, reason None`; non-`KNOWN ⇒ field None, reason non-empty`) mirroring `VisibleFact` / `EcrTimingResidual`. **Anti-scope-creep:** the record's `signal_event_time` field stays **required**; only the *reference object* gains the carrier; do **not** add members to `SignalEventTimeField`. This is the *only* model edit the build is authorized to make.

**Build-time micro-decisions (named, so they cannot re-leak as silent improvisation):**
1. `content_id` basis = `(packet_id, slice_id)` only; body bytes forbidden in the basis.
2. Multi-body slice (`SourceCaptureSlice.preserved_file_ids` is a list): **one record per slice**; the multi-body → single `raw_observation` composition rule (primary vs concatenation) is a **named build decision**, never a file→record fan-out.
3. Referenced-but-unsupplied body = **caller error → no record + a surfaced limitation**, never an empty-anchor record (distinct from "slice has no files" → cleanly no record).
4. Body verification **deferred**: hash-integrity is ECR/SP-2's lane; v0 carries the supplied body verbatim, trusting the frozen input; an optional `sha256`/`size` check vs the packet's `PreservedFile` is a named-deferred caller/harness option, not a v0 deriver bar.
5. `ecr_posture_refs` param kept defaulted `()` for signature stability — the lone speculative element (no v0 consumer); droppable later.

**Amendment non-claims.** No build; no model edit performed (D2=b1 specified, scheduled); no authored-input record/finalizer; no EvidenceUnit binding; no Cleaning/Judgment; no commit/push; JSG-01 FROZEN. The SPLIT, the dormant authored lane, the re-derive-not-migrate lifecycle, the three-honesty-state encoding, and emit-timing are **carried unchanged** from v0.

**Out-of-scope finding (flagged, not fixed here).** The brief (`core_spine_v0_signal_content_record_architecture_v0.md:47`) says "the five families" but `SignalFamily` has four members + `RESIDUAL_FAMILY_UNRESOLVED` — a real source inconsistency that does not affect v0 (family always residual). Routed to separate cleanup.

---

## Architecture Result

| Question | Result | Why |
|---|---|---|
| What is the SCR extraction contract? | `TARGET_RECOMMENDED` → **SPLIT (mechanical carry-shell + residualizing authored core)** | Settles the load-bearing question; lowest downstream lock-in (dormant typed seam, not a built lane or baked input schema); mirrors the SP-6 mechanical-with-named-residuals pattern. |
| Is the interpretive core mechanically derivable from the frozen packet today? | **NO (finding)** — `signal_family` + event-core are not | No authored-classification input / finalizer exists in source. Resolved by residualize-default + a declared-dormant authored lane (D1). |
| Can the v0 model stay honest under absence? | **NO for one field (finding)** — `signal_event_time` has no unknown path | Required reference, two members, no residual. Needs a model amendment (D2). The lane names it; does not pick. |

---

## Decision frame (what the extraction call actually is)

The `SignalContentRecord` v0 model exists and is green (17 model tests). What is undecided is the **deriver's extraction contract**: how a captured `raw_observation` becomes a filled record. The model's fields split cleanly by *where their value can honestly come from*:

- **Provenance / keying / structural facts** the frozen `SourceCapturePacket` already carries (keys, raw text, timing reference, version) — mechanically present.
- **Interpretive facts** — *what kind of signal this is* (`signal_family`) and *what it claims* (the event-core: `subject_entity`, `event_or_claim`) — which the packet does **not** carry. The packet records *that a capture happened* and *its provenance/timing*, never *what the content says*.

The structural fork the contract must answer: is extraction **AUTHORED**, **MECHANICAL (M2-derive)**, or a **SPLIT**? Decisive context: the brief (`core_spine_v0_signal_content_record_architecture_v0.md:66`) names the extraction "like SP-5's deferred finalizer… likely needs a provenance-bound **authored** input, residualized when absent — never invent family or content." And the boundary doc's SP-5 decision establishes the *shape* an authored interpretation must take: cross-family, provenance-bound, no self-authoring.

---

## Resolution: SPLIT (the load-bearing answer), alternatives compared

**The deriver is a mechanical CARRY-shell over the frozen `SourceCapturePacket` (CapturePacket) that COMPOSES a bounded, residualizable authored interpretive core — and residualizes that core when the authored input is absent (the default).** It never originates family or content.

| Criterion | Pure AUTHORED now | Pure MECHANICAL M2 (deriver classifies prose) | **SPLIT (carry + residual; authored lane dormant)** |
|---|---|---|---|
| Honest under absence | ✗ requires an input that does not exist → invents a producer | ✗ classifying family from free text is the force-map / self-authoring leak the SP-5 decision forbids | ✓ residualizes the absent core; never invents |
| Re-derivable from frozen raw | n/a (no producer) | ✗ a prose classifier is non-deterministic → not re-derivable | ✓ the mechanical half is a pure function of the frozen packet |
| Matches the SP-6 precedent | ✗ | ✗ (SP-6 explicitly does **not** compute its missing value) | ✓ identical declared-dormant-behind-missing-input shape |
| Downstream lock-in if wrong | High (bakes an authored-input schema before its producer exists) | **Highest** (bakes a non-deterministic classifier into a "re-derivable" lifecycle — self-contradictory) | **Lowest** (a dormant typed seam *deletes/activates* cleanly; no migration) |
| Owner-reserved / frozen line | crosses (authors an EvidenceUnit-adjacent input record) | crosses (a content classifier ≈ Signal-Use interpretation creep) | stays inside (carry + residual only) |

The SPLIT is the lowest-downstream-lock-in already-complete path (the AGENTS.md tie-breaker): a dormant typed seam is *deleted-or-activated*, never *migrated*.

**The authored input, when it eventually exists, must be a FROZEN, provenance-bound, keyed artifact — not a live model call.** Two lenses converged here: full re-derivability of the *activated* lane requires the authored core to itself be a frozen recorded artifact (keyed `(packet_id, slice_id)`, dated, cross-family-attributed per the SP-5 precedent). A live classifier inside the deriver would break "re-derive, not migrate" and re-create the testee-tester problem. So re-authoring is a new *versioned* authored record, never an in-place mutation; the deriver re-reads the authored core as-of its binding.

---

## Per-field M1 / M2 / M3 mapping

Legend: **M1** = carry by value/key/reference from a frozen producer fact, no judgment. **M2-mech** = compute from *closed* facts (the record's own resolved shape, key existence), never from prose. **M2-interp (dormant)** = bound from the authored input when present; residualizes in v0. **M3** = named residual / honesty stop.

| Field | Type | Mode | v0 behavior + residualize rule |
|---|---|---|---|
| `manifest_version` | `Literal["signal_content_record_v0"]` | structural | Pinned constant; strict-admit v0 only (model test). |
| `content_id` | `str` | M2-mech | Deterministic, stable id for this (packet, slice, event); non-empty; **not** random (re-derive stability). |
| `references.packet_id` | `str` | M1 (key) | The promoted packet's real key; required non-empty; **links, never embeds.** |
| `references.slice_id` | opt `str` | M1 (key) | The slice the event was observed in (when slice-grain). |
| `references.ecr_posture_ref_ids` | by-key list | M1 (key) | The same packet's ECR posture ids (SP-1/2/3/6); deduped; content→integrity link only, **never merged.** |
| `signal_event_time` | `SignalEventTimeReference` | M1 (by-reference) | Names which `PacketTiming` field is the event time; carries **no timestamp**; allowed = `{source_publication_or_event, source_edit_or_version}` only (never capture/recapture/cutoff). **⚠ no unknown path — honesty gap, see D2.** |
| `raw_observation` | `str` (non-empty) | M1 (verbatim) | The load-bearing honesty anchor: verbatim, source-language, pre-interpretation. Always present, even when family/event residualize — this is what keeps every residual honest and the record re-derivable. |
| `signal_family` | `SignalFamily` (closed) | **M3 in v0 / M2-interp dormant** | **DEFAULT `RESIDUAL_FAMILY_UNRESOLVED`** (no authored input exists). M2 fires only when a provenance-bound authored family arrives AND is a closed member; an authored value outside the enum still → residual (never coin, never force). The headline residual. |
| `subject_entity` | `VisibleFact` | **M3 in v0 / M2-interp dormant** | **DEFAULT `unknown_with_reason`.** Note: the packet's *source* identity (SP-1) is **not** the signal's subject — so even a present packet field does not satisfy this; conservative default is residualize. |
| `event_or_claim` | `VisibleFact` | **M3 in v0 / M2-interp dormant** | **DEFAULT `unknown_with_reason`** ("interpretation not authored; raw_observation carries the verbatim substance"). The interpreted claim is authored, not mechanical; the raw substance is never lost (it lives in `raw_observation`). |
| `decision_relevance` | `DecisionRelevance` (closed) | M2-mech (neutral) | Shape-derived neutral routing tag; **forced `UNRESOLVED` whenever `signal_family == RESIDUAL_FAMILY_UNRESOLVED`** (cannot route what is not interpreted). **Never** a graded Signal-Use / Decision-Strength / Action-Ceiling verdict (Judgment-owned). |
| `delta` | `Delta \| None` | M2-interp dormant (optional) | `None` by default. **Absent-vs-uncaptured distinction (load-bearing):** `delta=None` = "no change in this point-in-time signal"; `Delta(before/after = unknown_with_reason)` = "a change exists but was not captured." Never collapse residual into structural absence. |
| `reaction` | `Reaction \| None` | M2-interp dormant (optional) | `None` by default; same-capture only. Aggregate reaction is Judgment-owned — never here. |
| `family_detail` | `FamilyDetailBase \| None` | structural (dormant) | `None` in v0 (empty extension slot); no family payloads built. |

**One-line invariant:** the deriver carries the frozen packet's facts by key/reference (M1), mechanically computes only the neutral key + neutral routing tag (M2-mech), and residualizes the entire authored interpretive core (M3). `raw_observation` is always present, so every residual stays honest.

---

## Residualize + honesty rules (the spine)

The fitness bar — *honest under absence, never invents* — lives here. The model already supplies every primitive (`VisibleFact` 4 statuses; `RESIDUAL_FAMILY_UNRESOLVED`; `UNRESOLVED`); the contract makes their honest use **mandatory**.

1. **Unknown / low-confidence family → `RESIDUAL_FAMILY_UNRESOLVED`** (the mandatory closed-enum residual; the model degrades, it does not error). A non-member or low-confidence authored value degrades to the residual; never coined, never forced.
2. **Absent / uncertain content → `VisibleFact(unknown_with_reason, reason=…)`** for `subject_entity` / `event_or_claim` / `delta.before|after`. The `reason` is load-bearing.
3. **Three honesty states the reason-string must keep distinct** (the brief's "not-extracted ≠ no-such-content"):
   - **NOT-EXTRACTED** — no authored input was bound (the SP-5-echo default). Reason: *"no authored interpretive input bound to packet <id>."* Says *the pipeline owes work.*
   - **EXTRACTED-BUT-ABSENT-CONTENT** — an authored input is present and reports no content of any closed family. Reason: *"authored input present; no content of any closed family observed."* Says *the source genuinely lacks this.*
   - **EXTRACTED-AND-PRESENT** — a confident closed family + `VisibleFact(known, …)`.
   Collapsing state 1 into state 2 is the exact SP-5-echo failure; the contract forbids it.
4. **`decision_relevance` stays a NEUTRAL mechanical routing tag** — shape-derived, forced `UNRESOLVED` when the core residualizes. No graded verdict ever appears on the record (Judgment-owned).
5. **Never invent** family or content. An all-residual-core record is a **valid, honest record** ("captured; not yet interpreted"), not an error and not a failure.
6. **Trust boundary holds:** content references integrity (`ecr_posture_ref_ids`) and provenance (`packet_id`/`slice_id`) by key, one-directional, **never merged.**

---

## Emit timing

The deriver runs **only after** (a) a candidate is **promoted** and (b) a `SourceCapturePacket` **exists** for it — **never** from Reddit candidate-intake discovery rows (those are pure discovery, upstream of capture). This is **type-enforced**: the deriver's required input *is* a `SourceCapturePacket` (and `references.packet_id` is non-empty), so it is structurally incapable of running pre-capture — there is no packet to pass. The mechanical half can emit a fully-residualized record the moment the packet exists; the authored half emits only when an authored interpretation is bound (possibly a later re-derive).

---

## Re-derive lifecycle

- **Derived / re-derivable from the FROZEN raw observable, never persisted-at-capture.** Re-running the deriver over the same frozen packet (and the same frozen authored core, when one exists) yields the same record. `raw_observation` is the durable anchor; the SCR is a *read*, not stored state. *(This is only true because the SPLIT kept the deriver mechanical — a live-classifier core would break it; that is the load-bearing coupling between the resolution and this lifecycle.)*
- **Family-taxonomy change = RE-DERIVE, not a stored-column migration.** Adding/retiring a `SignalFamily` member → re-run over the still-frozen packets; records that were `RESIDUAL_FAMILY_UNRESOLVED` may resolve to the new family on re-derive. No data migration.
- **Read-checked `_vN`, strict-admit, no upgrade-on-load** — the `manifest_version` Literal admits only `_v0`; a `_v1` deriver is a new read, not an in-place mutation. Additive family-enum growth (records that do not fit degrade to the residual).
- **Activating the dormant authored lane is itself a re-derive, not a migration:** when a frozen, provenance-bound authored input later exists, re-run the deriver (now passing it) over the frozen packets to fill the residualized core. The residual record is *superseded by re-derivation*, never rewritten in place.

---

## Core / satellite boundary and invariants later work must preserve

- **Core invariant:** the deriver **carries or residualizes; it never authors.** Family/event-core are bound from a frozen provenance-bound authored input or residualized — never originated from `raw_observation` by the deriver (the no-testee-tester boundary, SP-5 precedent).
- **Core invariant:** `raw_observation` is the always-present, verbatim, pre-interpretation anchor; it is never dropped, even when everything interpretive residualizes.
- **Core invariant:** content links to provenance/integrity **by key, one-directional, never merged.**
- **Core invariant:** `decision_relevance` is a neutral mechanical routing tag; graded Signal-Use / aggregate / sentiment stays Judgment-owned and is never a field here.
- **Core invariant:** never invent family or content; unknown → residual, absent → honest `VisibleFact`.
- **Satellite / deferred:** the authored-input record + its provenance binding; the M2 interpretive activation; `family_detail` payloads; the record grain (per-packet vs per-slice vs per-event); the `signal_event_time` model amendment (D2).

---

## Bounded build scope teed up + what stays deferred

**The v0 build this tees up (smallest complete; a separate, later authorization):**
- One module `orca-harness/signal_content/deriver.py` (sibling to `ecr/deriver.py`), exposing the **Amendment v0.1** signature `derive_signal_content(packet, *, preserved_bodies, ecr_posture_refs=(), authored_interpretation=None) -> list[SignalContentRecord]` — pure, no I/O, no mutation, binds no `EvidenceUnit`. *(v0's packet-only signature is superseded: `raw_observation` is carried from the caller-supplied body, not the packet.)*
- v0 behavior = M1-carry + M2-neutral (`content_id`, `decision_relevance`, the event-time reference) + **M3-residualize the authored core.** With `authored_interpretation=None` (the only state that exists), it emits a **structurally complete, honestly-residual** record.
- The `authored_interpretation` parameter is **declared and dormant** (typed `| None`, defaulted `None`), with a docstring stating it is unbuilt — the named seam.
- Tests mirroring `test_signal_content_models.py` (see validation expectations).

**Deferred (NOT authorized here — each a separate owner gate):**
- The **authored-classification input record** — its schema and (critically) its **provenance binding** (SP-5-style: out-of-band, cross-family, provenance-bound). **The first deferred slice.**
- The M2 interpretive activation; rich `family_detail` payloads; multi-event splitting *within* a body. *(Grain is DECIDED per Amendment v0.1 (D5): one record per body-bearing slice — not per-packet.)*
- Persistence/finalizer; any packet→EvidenceUnit binding; the `EvidenceUnit.content_ref` downstream addition; Cleaning; Judgment; commits/pushes. JSG-01 stays FROZEN; the final EvidenceUnit field architecture stays owner-reserved.
- Any cross-source aggregate (Judgment-owned).

---

## Smallest complete next routing object

```yaml
next_routing_object:
  type: amendment_ratified              # owner ratified D1-D5 (b1) via Architecture-Pass Amendment v0.1; still design-only
  primary_result: TARGET_RECOMMENDED    # SPLIT: mechanical carry-shell + residualizing authored core
  recommend_to_owner:
    deriver_shape: >
      A mechanical CARRY-shell over the frozen SourceCapturePacket that COMPOSES a
      bounded, residualizable authored interpretive core by reference; residualizes
      that core (RESIDUAL_FAMILY_UNRESOLVED / VisibleFact unknown-with-reason) when
      the authored input is absent -- the default, since no authored input exists today.
    first_build_slice: >
      Build the carry-shell + residualize path FIRST, with zero authored input
      (emits honest all-residual-core records keyed to a packet) -- the direct
      sibling of ecr/deriver.py and the smallest complete mechanical slice.
    authored_core_carrier: >
      A thin, FROZEN-once-produced, provenance-bound authored-interpretation input
      keyed (packet_id, slice_id) -- contract only; NOT a persisted SCR field and
      NOT the SP-5 finalizer mechanism (which stays deferred).
  owner_decisions_ratified:                 # all ratified this turn via Architecture-Pass Amendment v0.1
    - D1: ACCEPTED -- no authored interpretive input exists in source (grep-confirmed, re-verified
          by the panel) -> the v0 deriver ships honest-residual. A finding, not a blocker.
    - D2: RATIFIED = path (b1) -- add a VisibleFact-style {status, packet_timing_field|None, reason}
          carrier to SignalEventTimeReference; the residual is the v0 DEFAULT; the deriver never selects
          publication-vs-edit. Additive/non-breaking; scheduled for the build, not applied here.
    - D3: CONFIRMED -- the deriver composes, never authors; the eventual authored mechanism is
          cross-family + provenance-bound (SP-5) and FROZEN-once-produced.
    - D4: RATIFIED = (a), generalized -- every non-packet input (preserved_bodies, ecr_posture_refs,
          authored_interpretation) is an explicit caller-supplied frozen input; the deriver stays pure.
    - D5: RATIFIED -- record grain = one record per SourceCaptureSlice that has a supplied body
          (references.slice_id always set); multi-event splitting within a body stays deferred.
  unchanged:
    - JSG-01 stays FROZEN; final EvidenceUnit field architecture owner-reserved.
    - No deriver built; no persistence/finalizer; no EvidenceUnit binding; no Cleaning/Judgment; no commit.
    - The v0 SCR model is unchanged EXCEPT the one additive D2=b1 amendment to SignalEventTimeReference
      (scheduled for the build, not applied here); the other fields + the 17 green tests are unchanged.
  not_proven:
    - That an authored interpretive input EXISTS or is producible today (it does not; this is the SP-5 echo).
    - That a flat one-record-per-packet grain needs no rollup (inherited from SP-6's
      single-source flat-vs-vector not_proven; re-verify if multi-source packets appear).
```

---

## Validation expectations the build must name

Mirroring `orca-harness/tests/unit/test_signal_content_models.py` (17 green) and the `ecr/` deriver tests, the future deriver build (not authorized here) must satisfy tests able to FAIL:

1. **Round-trip** — every derived record survives `model_validate(model_dump())` under `extra="forbid"`, including all-residual-core records.
2. **Closed-enum** — only closed `SignalFamily` / `DecisionRelevance` members are emitted; a non-member/low-confidence authored family degrades to `RESIDUAL_FAMILY_UNRESOLVED` (not an error, not a coined value); no graded relevance is ever produced.
3. **Residualize-honestly (the headline test)** — given `authored_interpretation=None`, the deriver emits a complete record with `signal_family == RESIDUAL_FAMILY_UNRESOLVED`, `event_or_claim` / `subject_entity` `unknown_with_reason` (with a reason), `decision_relevance == UNRESOLVED`, and a **non-empty `raw_observation`** — plus a dedicated test that the **state-1 (not-extracted)** and **state-2 (extracted-empty)** reason markers are **distinct**.
4. **Never-invent** — a packet with rich `raw_observation` but no authored input does **not** populate `signal_family` from the prose (asserts residualize — guards the self-authoring boundary).
5. **Key-integrity** — `references.packet_id`/`slice_id` are the exact frozen keys; `ecr_posture_ref_ids` by-key, deduped, from the same packet; nothing embedded/merged.
6. **Event-time discipline** — `signal_event_time` references only `{source_publication_or_event, source_edit_or_version}`; the selection rule is covered; and the **D2 gap is guarded** (an xfail/named-gap until resolved, so the build does not silently default the field).
7. **Re-derive determinism + purity** — twice over the same `(frozen packet, frozen authored core)` yields equal records; no I/O, no packet mutation, binds no EvidenceUnit; returns a `list`.

**Missing checkable success bar (named, not invented):** there is **no fixture/oracle for the activated (populated) interpretive path**, because the authored input does not exist. The v0 bar is strictly the **mechanical + residualize-honestly** contract; an extraction-*accuracy* bar belongs to the deferred authored-input mechanism, not this contract. Naming this — rather than fabricating a classifier oracle — is the honest move the fitness function demands.

---

## Quality-gate self-check (gates must be able to fail)

- **The load-bearing authored-input question settled against source** — PASS WITH FINDING. Settled as SPLIT/residualize-default; the finding (no authored input exists) is surfaced as D1, not hidden.
- **Every per-field mode mapped (M1/M2/M3) + honest residual for each interpretive field** — PASS, except `signal_event_time` which cannot residualize in the v0 model — surfaced as D2 (the one honesty gap), not papered over.
- **Never invents family/content; deriver is not the author; decision_relevance neutral; links by key** — PASS (core invariants).
- **JSG-01 not unfrozen; nothing built; EvidenceUnit field architecture owner-reserved; no cross-source aggregate** — PASS.
- **Re-derive-not-migrate preserved; lowest-lock-in shape (dormant seam) chosen** — PASS.

---

## Non-claims

Architecture-planning / design only. Not implementation, validation, a deriver build, persistence/finalizer, any packet→EvidenceUnit binding, Cleaning, Judgment, a JSG-01 unfreeze, or a readiness/acceptance claim. The v0 model is a design basis; this plan derives INTO it. **Amendment v0.1 is owner-ratified** but schedules exactly ONE additive model amendment (D2=b1 to `SignalEventTimeReference`) for the build — specified, not performed here; all other fields unchanged. The recommendation is planning input to a later, separately-authorized build, not the build.

## Doctrine status + direction-change-propagation receipt

Per `.agents/workflow-overlay/source-of-truth.md`, and matching the SP-6 precedent (`jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md`), this advisory routing object **binds no durable rule** future agents must follow: it recommends a target, surfaces owner decisions, edits no controlling source, builds nothing, and keeps JSG-01 frozen. The **doctrine-changing step is the later owner ratification adopting this architecture (and authorizing the build)** — that step carries the binding receipt. The handoff requires a receipt on this doc; it is bound here in **staged** form so the downstream surfaces are ready for that ratification:

```yaml
direction_change_propagation:
  status: ratified_amendment_v0_1     # owner ratified the SCR contract + the v0.1 input-contract amendment this turn
  doctrine_changed: >                  # the SCR carry-supplied-or-residualize deriver contract is ratified
    The SCR deriver contract is ratified: SPLIT (carry-shell + residualizing authored core);
    pure-but-not-packet-only (caller-supplied preserved_bodies / ecr_posture_refs / authored_interpretation);
    per-slice grain (D5); D2=(b1) event-time residual-default; decision_relevance v0-UNRESOLVED.
    One additive model amendment (D2=b1 to SignalEventTimeReference) is SCHEDULED for the build, not applied.
    Still design-only; no build; JSG-01 FROZEN.
  trigger: architecture_doctrine + lifecycle_boundary
  related: the next derived-record kind after ECR SP-1/2/3/6; steps toward Cleaning/binding
  evidence:
    - core_spine_v0_signal_content_record_architecture_v0.md (834c930) — brief :66 "like SP-5's deferred finalizer… authored input, residualized when absent"
    - orca-harness/signal_content/models.py (834c930) — the v0 model + the signal_event_time honesty gap
    - boundary doc decision B (:303) — SP-5 cross-family, provenance-bound, no self-authoring
    - ecr/ SP-6 (6329d71) — the mechanical-with-named-residuals + declared-dormant pattern reused
    - cross-vendor adversarial artifact review (needs-architecture-pass; 6 findings, all adjudicated ACCEPT) + the 3-subagent architecture-pass panel + home adjudication (this turn) — the design basis for Amendment v0.1
  residual: the binding receipt is authored at owner ratification of this architecture, not here
  downstream_surfaces_to_check_on_finalize:
    - the brief (core_spine_v0_signal_content_record_architecture_v0.md)
    - core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - the IPF Evidence Unit Standard
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  non_claims:
    - no readiness/validation; no JSG-01 unfreeze; no build; no model edit PERFORMED (the one additive D2=b1 amendment is scheduled, not applied this turn)
```

## Source-read ledger + advisory disclosure

- Sources (pins verified by the panel's fresh reads): `core_spine_v0_signal_content_record_architecture_v0.md` (834c930, controlling), `orca-harness/signal_content/models.py` + `__init__.py` (834c930; 17 model tests green), `orca-harness/ecr/` (deriver/models/__init__; SP-6 at 6329d71 — the reused pattern), `jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md` (the precedent shape), `orca-harness/source_capture/models.py` (`VisibleFact`, `PacketTiming`, packet/slice keys), `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (SP-5 decision B `:303`; JSG-01 frozen; reserved EvidenceUnit architecture), `orca-harness/tests/unit/test_signal_content_models.py` (the validation discipline). Decisive **negative** finding (all three lenses, grep-confirmed): no authored-classification input record and no SP-5 finalizer mechanism exist anywhere in the harness.
- Methods: `workflow-architecture-planning` + `workflow-deep-thinking` reference-loaded; applied after source-context-ready.
- Advisory sub-lanes (3, owner-authorized, general-purpose): lens A (authored-input-first), lens B (per-field-M1/M2/M3-first), lens C (honesty-under-absence-first). All three independently converged on the SPLIT + residualize-default + no-authored-input-exists; the home thread adjudicated. Lens C contributed the three-state honesty encoding and the `signal_event_time` honesty gap; lenses A+B contributed the frozen-provenance-bound authored-artifact constraint; lens B contributed the per-field table and the absent-vs-uncaptured distinction. Same-vendor panel — a cross-vendor adversarial *artifact* review is recommended before any build. The lane owns this synthesis.
```
