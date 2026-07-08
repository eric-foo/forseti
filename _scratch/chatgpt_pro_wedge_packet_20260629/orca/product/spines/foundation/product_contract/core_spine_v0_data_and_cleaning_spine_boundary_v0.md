# Core Spine v0 Data Capture And Cleaning Spine Boundary

```yaml
retrieval_header_version: 1
artifact_role: Product architecture boundary note
scope: Canonical boundary for Data Capture Spine, Evidence Candidate Record, Cleaning Spine, Judgment Spine, Decision Artifact, and Outcome Memory in Core Spine v0.
use_when:
  - Deciding whether Data Capture Spine, Evidence Candidate Record, or Cleaning Spine work belongs in core, satellite, Judgment Spine, artifact, outcome, or a deferred runtime lane.
  - Preparing the later Evidence Candidate Record / Evidence Unit (EvidenceUnit) architecture consolidation prompt.
  - Checking whether a proposed source, capture, cleaning, memo, deck, or outcome-memory change exceeds this artifact's planning-only authority or requires separate bounded implementation authorization.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
  - orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
  - orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
```

- Status: PROPOSED_FREEZE
- Artifact type: Product architecture boundary note
- Scope: Product-method architecture for Core Spine v0 Data Capture/Cleaning boundaries
- Source basis: current owner direction, `docs/product/core_spine_v0_product_contract.md`, `docs/product/core_spine_v0_information_production_foundation_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- Proof run authorized: no

## Purpose

This note fixes the product-method boundary between Data Capture Spine, Evidence
Candidate Record, Cleaning Spine, Judgment Spine, Decision Artifact, and Outcome
Memory.

It supersedes the older working alias where "Data Spine" meant Evidence Object
Model / Evidence Unit content contract. In this note, the canonical name is Data
Capture Spine: evidence-grade signal acquisition and preservation. Evidence
Candidate Record owns the pre-cleaning captured-signal receipt.

This is not a runtime design. It may define conceptual capture and preservation
responsibilities, but it does not itself authorize schemas, storage, source
APIs, scrapers, adapters, dashboards, automation, scoring engines, clustering
pipelines, memo generators, deck generators, tests, deployment, proof runs, or
feature planning.

## How To Use This Note

Use this note as a boundary check before creating or patching Core Spine, Data
Capture Spine, Evidence Candidate Record, Judgment Spine, Evidence Unit,
source-family, memo, deck, or outcome-memory artifacts.

Ask three questions:

1. Does this proposed work belong to Data Capture Spine, Evidence Candidate Record,
   Cleaning / Provenance & Normalization, Judgment, Artifact, Outcome Memory,
   Satellite, or a deferred runtime lane?
2. Is the work preserving the Data Capture / Evidence Candidate Record / Cleaning
   split, or is it letting capture, receipt, cleaning, and judgment blur
   together?
3. Is the work non-implementation product architecture, or is it smuggling
   runtime source-system design, implementation, source maps, or proof-run
   execution?

For the next Evidence Candidate Record / Evidence Unit prompt, use this note as
a boundary input. Do not treat it as the completed ECR or Evidence Unit design.

## Decision

Data Capture and Cleaning should be split, with Evidence Candidate Record
between them.

The split is product-method, not runtime:

| Layer | Canonical term | Owns | Must not own |
| --- | --- | --- | --- |
| Data Capture Spine | Evidence-grade signal acquisition and preservation | Source-surface discovery, access-path evaluation, capture obligations, raw-signal preservation, capture fidelity, source visibility, source identity, event/capture timing, cutoff/archive posture, source-envelope removal, mechanical source projection into inspectable rows when needed, projection receipt warnings, and handoff requirements for public/external signals. | Final ECR field schema, storage, IDs, adapters, scraper/API implementation, source truth, cleaning transformations, credibility labels, discounting, Decision Strength, Action Ceiling, semantic filtering, or evidence-row removal due to apparent low value. |
| Evidence Candidate Record | Pre-cleaning captured-signal receipt | The content/receipt contract for a captured signal entering Cleaning: raw observation, mechanical source projection packet reference where used, provenance/timing/capture-context obligations, inspectability reference, preservation posture, and handoff state at a categorical level. | Source discovery, source collection operations, runtime storage, cleaning transformations, integrity labels, signal-use classification, decision-use claims, or certification that a projection is fully normalized. |
| Cleaning Spine | Provenance & Normalization | Non-destructive transformation ledger, normalization, translation, summarization, dedupe mechanics, clustering mechanics, and raw-to-cleaned traceability. | Source acquisition, credibility, discounting effects, integrity labels, exclusion due to judgment, Decision Strength, Action Ceiling. |
| Judgment Spine | Judgment Spine | Signal Integrity, Signal Use Classification, uncertainty, counterevidence, discounting, exclusion, Decision Strength, Action Ceiling. | Capture, source storage, raw transformation history, deck production. |
| Decision Artifact | Reasoning + Communication Artifact | Memo and evidence appendix as reasoning substrate; executive deck as derived communication. | New unsupported claims or claims above Action Ceiling. |
| Outcome Memory | Backtest + Live Outcome Memory | Cutoff-disciplined replay and attribution-tagged live learning. | Calibration or moat claims without leakage and attribution controls. |

The canonical architecture is:

```text
Decision Frame
-> Data Capture Spine: signal discovery, access, capture, preservation, mechanical source projection when needed, handoff
-> Evidence Candidate Record: pre-cleaning receipt of raw capture and projection packet
-> Cleaning Spine: Provenance & Normalization ledger
-> Judgment Spine overlays
-> Reasoning Artifact: memo + evidence appendix
-> Communication Artifact: derived executive deck
-> Outcome Memory: Backtest Memory + Live Outcome Memory
```

The wrong moves are:

- collapsing Data Capture, Evidence Candidate Record, and Cleaning into one blurry
  contract;
- using Data Capture Spine as an Evidence Object Model alias;
- giving Data Capture Spine runtime meaning too early;
- promoting mechanical source projection into a standalone spine layer;
- calling projection "filtering" or "purification" if it removes evidence rows
  instead of only source-envelope noise;
- treating source availability or collection volume as evidence validity;
- letting Cleaning absorb Judgment;
- letting decks drive evidence structure.

## Layer Rules

Decision Frame remains the required starting point. No Data, Evidence Candidate
Record, Cleaning, Judgment, Artifact, or Outcome layer should create
free-floating evidence inventories outside a decision frame.

Data Capture Spine owns evidence-grade acquisition and preservation requirements. It
may say what kinds of source surfaces, capture fidelity, visibility, timing,
archive posture, and preservation obligations Orca must support conceptually.
It must not become a runtime source-system plan, scraper plan, source inventory,
source map, or generic listening platform.

Mechanical Source Projection is a Data Capture-owned helper, not a new spine
layer. When raw source format is too transport-heavy for later inspection, Data
Capture may create a Data Capture Projection Packet: preserved raw source plus
a mechanical row view plus a projection receipt. The projection may remove
source-envelope noise such as API transport, UI, report, award, embed, or
client-voting scaffolding from the working view. It must not remove post,
comment, document, review, or other evidence rows because they appear
low-value, low-score, repetitive, embarrassing, bot-like, deleted, or
unhelpful. Projection self-checks may record counts, omissions, warnings, and
missing-continuation markers, but they do not certify the projection as cleaned
or normalized.

Evidence Candidate Record owns the pre-cleaning captured-signal receipt. This
artifact does not freeze a field architecture; the current IPF Evidence Unit
standard remains the source to cite until the later Evidence Candidate Record /
Evidence Unit consolidation.

Cleaning Spine verifies raw-to-projected traceability where a projection packet
exists and records non-destructive transformation history. It may record
normalization, translation, summarization, dedupe, and clustering mechanics.
Once dedupe or clustering affects independence, credibility, uncertainty,
exclusion, Decision Strength, or Action Ceiling, the effect belongs to Judgment
Spine.

Judgment Spine owns inference and decision-use effects. The consultant-loop CA
lane may train inference, build a case backlog, compare solved cases, and
sharpen judgment rubrics. This note reserves the layer boundary; it does not
claim Judgment Spine is trained, validated, accepted, or ready.

Decision Artifact splits into Reasoning Artifact and Communication Artifact.
The memo plus evidence appendix are the reasoning substrate. The executive deck
is derived communication; every material deck claim should trace back to the
memo or appendix and must not exceed the Action Ceiling.

Outcome Memory splits into Backtest Memory and Live Outcome Memory. Backtest
Memory may support internal calibration only when leakage controls hold. Live
Outcome Memory is attribution-degraded by default until an accepted attribution
discharge protocol exists.

## Inclusion State Rule

The Evidence Candidate Record or later Evidence Unit may carry an inclusion or
handoff state, but the reason for that state must be layer-owned.

| State reason type | Owning layer | Examples |
| --- | --- | --- |
| Capture or preservation blocker | Data Capture Spine | Source inaccessible under allowed boundary, capture fidelity insufficient, archive posture missing, source visibility cannot be established. |
| Receipt/content blocker | Evidence Candidate Record | Raw observation missing, source identity unresolved, event/capture timestamp obligation unmet, inspectability reference absent. |
| Cleaning blocker | Cleaning Spine | Normalization conflict, duplicate cluster unresolved, translation/summarization trace missing. |
| Boundary blocker | Core Boundary Rules / Judgment Spine | Private material, deceptive collection, ordinary-person dossier risk. |
| Integrity exclusion | Judgment Spine | Artificial-amplification risk prevents use, copied/coordinated signal cannot support demand. |
| Decision-use downgrade | Judgment Spine | Signal is useful for attention but weak for demand. |
| Satellite interpretation blocker | Satellite | Costly behavior undefined for the decision family. |

Data Capture Spine and Evidence Candidate Record may record that a source cannot be
inspected or a timestamp is missing. Cleaning may preserve and propagate that
fact. None of those layers may decide that the signal is credible enough,
strong enough, or action-supporting enough; that belongs to Judgment Spine.

## Core Vs Satellite

Core owns market-agnostic evidence accountability:

- Decision Frame requirement;
- Data Capture Spine capture and preservation obligations;
- Evidence Candidate Record / Evidence Unit invariants;
- provenance, timing, visibility, and cutoff discipline;
- transformation ledger semantics;
- Signal Integrity vocabulary and Integrity Effect Rule;
- Signal Use Classification registry shape;
- Decision Strength and Action Ceiling rules;
- memo plus evidence appendix as reasoning substrate;
- executive deck derivation invariant;
- backtest leakage controls;
- public, market-level, non-deceptive boundary rules;
- non-claims.

Satellites own bounded adaptation:

- buyer context, industry constraints, decision owner, and consequence;
- decision-family language, competitor set, source-family relevance, and source
  blind spots;
- source-family access notes and capture feasibility constraints;
- source-family-adapted normalization heuristics;
- costly-behavior examples;
- allowed verb subset within core Action Ceiling rules;
- success criteria, kill criteria, and satellite-specific Signal Use rows;
- communication artifact template and tone.

Satellites adapt context and interpretation. They must not redefine capture
provenance, admissibility, cutoff discipline, preservation discipline,
integrity effects, cleaning traceability, Action Ceilings, memo/appendix
discipline, or non-claims.

## Source-Family Promotion Rule

Source-family rules may exist in satellites before they become core.

Any proposed capture, cleaning, normalization, or interpretation rule must
declare itself as source-invariant core, source-family-adapted satellite, or
unresolved candidate rule.

Empirical source-family heuristics should not be promoted into core until they
survive comparison across at least two non-overlapping source families or an
owner explicitly accepts the exception. This applies to capture-fidelity
heuristics, copied-language thresholds, review-site normalization, forum
thread/comment hierarchy, vendor-managed forum discounts, AI-rewritten-content
suspicion, and similar source-shaped heuristics.

This rule does not require obvious core invariants, such as raw-signal
preservation, raw-claim separation, or non-destructive transformations, to
re-prove themselves across source families.

## Rejected Or Deferred

Rejected:

- unified Data + Cleaning Spine core;
- Data Capture Spine as Evidence Object Model / content-only alias;
- Data Capture Spine as runtime/source-system architecture;
- Cleaning Spine owning credibility, discounting, exclusion, Decision Strength,
  or Action Ceiling;
- source-family-first core;
- decision-family-first top layer;
- deck-driven spine;
- source maps as inventories or collection plans;
- Outcome Memory as moat claim before leakage and attribution controls exist.

Deferred:

- schemas, storage shape, source IDs, source APIs, scrapers, adapters,
  dashboards, automation, scoring engines, clustering pipelines, source-map
  inventories, memo generators, deck generators, software tests,
  implementation planning, and deployment;
- source taxonomy and numeric source-quality rubric;
- final Evidence Candidate Record / Evidence Unit field architecture;
- final memo format and deck back-reference syntax;
- confidence vocabulary beyond Action Ceiling;
- Snapshot Integrity Class enforcement mechanics;
- Live Outcome Memory attribution-discharge protocol.

## Future Work Boundaries

Data Capture Spine setup CA should answer:

- what source surfaces and acquisition modes Orca must be able to reason about;
- what capture fidelity and preservation obligations are core;
- how cutoff, archive posture, source visibility, and capture context should be
  handled conceptually;
- what Data Capture Spine must hand to Evidence Candidate Record categorically, without
  defining ECR fields or schemas;
- what capture capabilities are core, satellite, rejected, or deferred.

Judgment Spine lane:

- may produce inference-training cases, case backlog, solved-case comparisons,
  judgment rubric refinements, and examples of discounting, exclusion, and
  Action Ceiling decisions;
- should patch accepted judgment rules into the appropriate Judgment Spine or
  Core Spine artifact;
- must not move judgment ownership into Cleaning.

### Evidence Candidate Record consolidation — OPENED (scoped to source-visibility; option B seed)

The owner has **OPENED** the reserved ECR consolidation, **bounded to source-visibility**. Ratified as the **seed** (AF-7 **option B**): the ECR **frame** — the receipt/derive layer invariants (INV-1..INV-5) and the three-mode binding rule — plus the **SP-6 source-visibility derivation contract** (the residual-first decision table) over the *derivable subset*, with the archive-vs-current-comparison rows fail-safe to **named residuals** (D1). Design basis: `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` (SHA256 `50DDE207824BCB7CE38DBDDF00C23014CA73E170BB4B62907C209C622174816F`), cross-family reviewed (`accept_with_friction`). The upstream producer state the contract reads — closed posture vocabularies + `PreservedFile.hash_basis` (R2) — is committed at `102a171` (schema-enforcement tests green at HEAD).

**Option B defers (still reserved, NOT ratified here):** declaring `source_visibility_posture` as a standing ECR field; accepting that "the ECR is the object"; the final ECR/Evidence Unit field architecture; the canonical-vs-working object name; SP-5 finalization; the SP-6 sufficiency grade; materiality verdicts; D2 (where any missing archive-date / archive-vs-current comparison facts live); and **JSG-01 unfreeze** (JSG-01 stays FROZEN). This records a derivation-contract seed — not an ECR schema, not ECR fields, and not the capture->ECR handoff boundary (Ob.16 unchanged). *(Superseded for the four JSG-01 source-side fields by the field-schema ratification below: those fields are now declared, and SP-5 and the SP-6 grade are decided.)*

The reserved sub-questions below remain open under option B except where the source-visibility seed addresses them.

### Evidence Candidate Record consolidation — JSG-01 source-side field schema RATIFIED (SP-1 / SP-2 / SP-3 / SP-6)

The owner has **ratified the JSG-01 source-side ECR field schema**, completing the source-visibility open by **declaring the four source-side fields** the conductor's JSG-01 predicate names (`judgment_quality_promotion_operating_model_v0.md:205`). This is the **A-direction** for the source-side scope, superseding option B's field-declaration deferral **for these four fields only** — the full ECR/Evidence Unit field architecture and the canonical object name stay reserved (see *Owner Decisions Remaining*).

**Declared fields (ECR-owned, derived, non-persisted; INV-1..INV-5):**
- **SP-1 `source_identity_state`** — M2 derived-read; clears on `{resolved, family_only}`.
- **SP-2 `inspectability_state`** — M2 over an M1-carried `PreservedFile.{sha256, hash_basis}` anchor; clears only on `inspectable_verifiable`.
- **SP-3 timing/cutoff** — **M1 carried-by-reference** over the producer's already-closed `PacketTiming.cutoff_posture` (NOT a coined parallel field); clears only on `pre_cutoff`.
- **SP-6 `source_visibility_posture`** — the ratified derivation contract. *(Archive-date class `D`-source amended post-ratification — binds to `cutoff_posture`-as-class; see Direction Change Propagation → SP-6 D-source amendment.)*

**Design basis (committed with this ratification):** `ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` (`50DDE207…`) + `ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` (`12799649…`, cross-family reviewed `accept_with_friction`, AR-01 adjudicated-accepted) + the two cross-family review reports (`57AB20A3…`, `3F2C3B44…`). Producer fields bound: R2 (closed posture vocabularies + `PreservedFile.hash_basis`) committed at `102a171`.

**Owner decisions recorded here:**
- **A (process):** ratify after the cross-family review pass — done and adjudicated.
- **B (SP-5 finalization authority):** a **distinct, cross-family, provenance-bound finalizer** (a different model family than the judge; an out-of-band record binding identity / time / inputs). Same-model or same-family self-finalization is **disallowed** (no testee-tester). The finalizer **mechanism is deferred implementation**; until it exists, JSG-01's finalization-provenance subpredicate stays `indeterminate_until_authored`.
- **C (SP-6 visibility-sufficiency grade):** **clears** on `archive_only` and `not_applicable`; `archive_corroborated` **reserved** (dormant until a comparison fact exists); `archive_diverged` defaults to **does-not-clear** (the tunable dial); all else (`current_capture_only`, `archive_post_cutoff_only`, `attempt_failed`, `not_attempted`, every residual) **does not clear**.

**SP-6 coverage note (honest, not an overclaim):** SP-6 ships at **core/honest** capability — it establishes pre-cutoff archives, rejects current look-alikes, and honestly residualizes what it cannot confirm — but the **`archive_corroborated`/`archive_diverged` (corroborated-tier) clears are deferred** behind a capture-side archive-vs-current comparison fact (**D2**, owner-reserved). A pre-cutoff-archive-plus-current-capture case therefore **evaluates determinately but may land on a residual rather than a top-tier clear until D2 exists**.

**Still reserved / NOT ratified here — JSG-01 stays FROZEN:** the field **derivers** (computing each value from a packet — implementation, post-ratification); the **SP-5 finalizer mechanism**; **D2**; **materiality** (downstream); the **full ECR/Evidence Unit field architecture** and **canonical object name**; **JSG-01 unfreeze**. Declaring the schema lifts the conductor's "no ECR field schema" blocker, but JSG-01 clears no case until the derivers and finalizer are built and a case packet carries the fields.

### Evidence Candidate Record consolidation — JSG-01-scoped EvidenceUnit binding contract RATIFIED

The owner has **ratified the JSG-01-scoped EvidenceUnit binding contract**
(owner word in-thread 2026-06-12), opening the reserved packet→EvidenceUnit
binding **for exactly the JSG-01 read surface and nothing broader**: the minimal
composition object that binds, by key (reference-never-merge), the four ratified
derived source-side postures (SP-1/2/3/6) and the current `FinalizationReceipt`
read onto one case-packet evidence unit.

**Ratified (the binding contract):**
- **`Jsg01EvidenceBinding`** — three durable keys (`evidence_id`, `packet_id`,
  `evidence_slice_id`). An **assembly-authored key assertion** (the slice whose
  preserved bytes carry the evidence unit's content), never a selector over the
  strongest posture. No posture, content, or derived value is stored on it.
- **A pure composer** (`compose_jsg01_evidence_record`) that re-derives the four
  postures fresh (re-derive-not-migrate), carries them verbatim — full per-slice
  SP-2/SP-3 vectors with bound-row selection by exact key; **no sibling
  promotion; failing siblings stay visible** — carries the SP-5 validate-only
  consumer's verdict verbatim (BLOCKED carried as a named state, never repaired),
  blocks on key mismatch (`Jsg01BindingError`), and computes **no aggregate
  verdict** (combining subpredicates stays the FROZEN conductor's job).
- **Durable-vs-derived split:** only the binding keys and the receipts (records
  of acts) are durable; everything else re-derives; any materialized snapshot
  carries re-derivation authority.
- **Module home:** a new sibling package `orca-harness/evidence_binding/` —
  deliberately outside `ecr/` so every "binds no `EvidenceUnit`" disclaimer
  there stays true.

**Design basis (committed with this ratification):**
`orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md`
(`FECCA1DF…`; delegated cross-vendor review-and-patch by GPT-5/OpenAI — 2 major
+ 1 minor, all patched — home-model adjudicated 2026-06-12, all reviewer changes
kept) + the delegated review report
`docs/review-outputs/adversarial-artifact-reviews/ecr_jsg01_evidence_unit_binding_plan_delegated_adversarial_artifact_review_patch_v0.md`
(`1E8EB59C…`).

**Explicitly NOT ratified here — JSG-01 stays FROZEN:** the **full ECR/Evidence
Unit field architecture**; the **canonical object name** (`Jsg01*` are working
names); **D2** and the corroborated SP-6 tier; **SP-4 / final-value policing**;
any conductor edit; the **JSG-01 unfreeze**. Per the plan's DRP-01 hardening,
the **unfreeze act** — not this ratification — must state how the frozen
conductor row's D2 wording is consumed: either D2 remains a named blocker, or
the owner records that decision-C's determinate residual behavior is acceptable
for the unfreeze boundary.

Future Evidence Candidate Record / Evidence Unit consolidation should answer:

- whether Evidence Candidate Record is the final canonical object name or a
  working owner-selected name;
- which Evidence Unit fields are frozen core invariants;
- how capture handoff obligations become receipt fields without turning Data
  Spine into an ECR schema;
- how Data Capture Projection Packet references should be receipted without
  turning ECR into a projection schema;
- how transformation ledger references should be represented conceptually;
- how inclusion state, state reason, and layer ownership should be recorded;
- how snapshot/archive status relates to pre-cutoff visibility;
- how Judgment overlays attach without becoming raw transformation history;
- what must remain satellite-specific.

## Owner Decisions Remaining

- Whether Evidence Candidate Record is the final canonical object name or a
  working name for the next consolidation.
- Whether Snapshot Integrity Class becomes a core field, optional field, or
  later extension.
- Whether Reasoning Artifact / Communication Artifact split is accepted.
- Whether Backtest Memory / Live Outcome Memory split is accepted.
- Whether Live Outcome Memory can ever carry moat or calibration weight, and
  under what attribution-discharge protocol.
- Whether the two-source-family promotion bar is accepted for empirical
  source-family heuristics.
- Final source taxonomy and source-quality rubric.
- Final Evidence Candidate Record / Evidence Unit field architecture.
- Final memo format and deck back-reference syntax.
- Confidence vocabulary beyond Action Ceiling.
- Backtest case-selection policy.
- Satellite costly-behavior catalog policy.
- Engagement Logic Registry extension model for satellites.
- When, if ever, runtime/source-system Data Capture Spine planning becomes
  authorized.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Mechanical Source Projection is a Data Capture-owned projection helper and Data Capture Projection Packet, not Cleaning, Judgment, or a standalone spine layer."
  trigger: architecture_doctrine
  controlling_sources_updated:
    - "docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/data_capture_harness_operating_model_architecture_v2.md"
    - "docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md"
    - "docs/product/data_capture_spine_lane_product_thesis_v0.md"
    - "docs/prompts/data_capture_pressure_test_reddit_mechanical_source_projection_worker_prompt_v0.md"
    - "docs/prompts/data_capture_pressure_test_slot3_reddit_manifest_architecture_thread_prompt_v0.md"
    - "docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/README.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Read-pack and source-budget rules remain accurate; they point to this boundary note rather than restating projection doctrine."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Navigation entry for the Data Capture/Cleaning boundary remains accurate and should not fork the doctrine."
    - path: "docs/_inbox/data_capture_pressure_test_operator_supplied_2026_05_29/slot3_reddit_b1/cleansed/"
      reason: "Legacy generated-folder name retained to avoid artifact churn; documentation now states the contents are source-projected, not Cleaning outputs."
  stale_language_search: "rg -n \"mechanical cleanser|cleanser|cleansing|filtering layer|source purification|source-purification\" docs .agents"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not ECR schema design"
    - "not Cleaning implementation"
    - "not Judgment authorization"
```

### ECR consolidation v0 open (source-visibility slice, option B)

```yaml
direction_change_propagation:
  doctrine_changed: "The reserved Evidence Candidate Record / Evidence Unit consolidation is OPENED, bounded to source-visibility. Ratified as a seed (AF-7 option B): the ECR receipt/derive frame (INV-1..INV-5 + three-mode binding rule) and the SP-6 source-visibility derivation contract over the derivable subset (archive-vs-current rows fail-safe to named residuals). Declaring source_visibility_posture as a standing ECR field, accepting 'the ECR is the object', the final field architecture, the canonical object name, and JSG-01 unfreeze remain reserved."
  trigger: architecture_doctrine
  related: lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md"
  design_basis:
    - path: "docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md"
      sha256: "50DDE207824BCB7CE38DBDDF00C23014CA73E170BB4B62907C209C622174816F"
      status: "advisory; cross-family reviewed (accept_with_friction); now tracked (committed as design basis; sha256 above pins the exact committed blob)"
  upstream_dependency:
    - "R2 (closed posture vocabularies + PreservedFile.hash_basis) committed at 102a171; schema-enforcement tests green at HEAD this turn (test_source_capture_packet.py + test_packet_assembly.py, 31 passed)."
  downstream_surfaces_checked:
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Gates ECR schema/design as a future surface; B opens a derived-read contract seed, not ECR schema/fields, so the gate stays accurate."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Navigational; points to this boundary note for ECR status and keeps ECR design/handoff gated, which remains accurate under B."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Ob.16 'does not define ECR fields' and the capture->ECR categorical handoff boundary are unchanged by B; its stale_if (ECR architecture changes the handoff boundary) has not fired."
    - path: "docs/product/jsg01_source_side_receipt_translator_v0.md"
      reason: "JSG-01 source-side consumer is FROZEN and ECR/JSG-lane-owned; coordination is by re-courier, not by editing the consumer."
    - path: "docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md"
      reason: "Adopted slice spec / lane working artifact; the supersession relationship is described, not performed, while JSG-01 is frozen."
  stale_language_search: "rg -n \"R2 .*uncommitted|hash_basis .*not_proven|consolidation .*reserved\" docs"
  non_claims:
    - "not declaring source_visibility_posture as a standing ECR field (option B defers it)"
    - "not the full ECR/Evidence Unit field architecture"
    - "not the canonical ECR object-name decision"
    - "not JSG-01 unfreeze (JSG-01 stays FROZEN)"
    - "not SP-5 finalization, SP-6 sufficiency grade, or materiality"
    - "not validation or readiness; not implementation, capture execution, or a commit"
```

### ECR consolidation v0 — JSG-01 source-side field schema ratified (SP-1/2/3 + SP-6)

```yaml
direction_change_propagation:
  doctrine_changed: "The JSG-01 source-side ECR field schema is RATIFIED: four declared source-side fields (SP-1 source_identity_state, SP-2 inspectability_state, SP-3 carried-by-reference cutoff_posture, SP-6 source_visibility_posture) with closed allowed-values and clear-conditions — completing the source-visibility open by DECLARING the fields (the A-direction) for these four categories, superseding option B's field-declaration deferral for them only. Owner decisions recorded: B = SP-5 finalization authority is a distinct cross-family provenance-bound finalizer (same-model/same-family self-finalization disallowed; mechanism deferred); C = the SP-6 visibility-sufficiency grade. SP-6 ships core/honest with the corroborated-tier (archive_corroborated/archive_diverged) deferred behind a capture-side comparison fact (D2). The field derivers, the SP-5 finalizer mechanism, D2, the full ECR/Evidence Unit field architecture, the canonical object name, and JSG-01 unfreeze remain reserved; JSG-01 stays FROZEN."
  trigger: architecture_doctrine
  related: lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md"
  design_basis:
    - path: "docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md"
      sha256: "50DDE207824BCB7CE38DBDDF00C23014CA73E170BB4B62907C209C622174816F"
      status: "committed; cross-family reviewed (accept_with_friction)"
    - path: "docs/product/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md"
      sha256: "12799649B1FC9B3B4CE9CF667AF61F966A4B7609D72E42BD1037DA5E778AFAB4"
      status: "committed with this ratification; cross-family reviewed (accept_with_friction); AR-01 adjudicated-accepted by the Opus home/CA model"
    - path: "docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_plan_cross_family_review_v0.md"
      sha256: "57AB20A36F15A5823E06DED8E0AE114DF4A1DFF4C09133B31EDD3F30F94D1109"
      status: "committed (SP-6 plan cross-family review)"
    - path: "docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_sp1_sp2_sp3_source_side_reconcile_cross_family_review_v0.md"
      sha256: "3F2C3B44104EC8EF303D680276B369CCC26CA1A218FFD77A0609FA9C4810257A"
      status: "committed with this ratification (SP-1/2/3 reconcile cross-family review; non-Opus delegate)"
  upstream_dependency:
    - "R2 (closed posture vocabularies + PreservedFile.hash_basis) committed at 102a171; SP-2/SP-3 bind to it; schema-enforcement tests green at HEAD."
  owner_decisions:
    - "A: ratify after the cross-family review pass — done and adjudicated."
    - "B (SP-5): distinct cross-family provenance-bound finalizer; same-model/same-family self-finalization disallowed; mechanism deferred."
    - "C (SP-6 grade): clears {archive_only, not_applicable}; archive_corroborated reserved; archive_diverged default does-not-clear; all else does-not-clear."
  downstream_surfaces_checked:
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Gates ECR schema/design as a future surface; declaring the JSG-01 source-side fields names a derived-read schema, not ECR persistence/storage; the gate stays accurate."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Navigational; points to this boundary note for ECR status."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Ob.16 'does not define ECR fields' and the capture->ECR handoff boundary are unchanged; the ECR derives/carries producer fields and defines none in the producer."
    - path: "docs/product/jsg01_source_side_receipt_translator_v0.md"
      reason: "JSG-01 source-side consumer is FROZEN and ECR/JSG-lane-owned; coordination by re-courier, not by editing the consumer; the translator's SP-1..SP-6 are reconciled-from, described not performed."
  non_claims:
    - "not the field derivers (implementation, post-ratification)"
    - "not the SP-5 finalizer mechanism (decided, not built)"
    - "not D2 (the archive-vs-current comparison fact)"
    - "not the full ECR/Evidence Unit field architecture or the canonical object name"
    - "not JSG-01 unfreeze (JSG-01 stays FROZEN)"
    - "not validation, readiness, materiality, or a buyer-grade claim"
```

### ECR consolidation v0 — SP-6 D-source amendment (cutoff_posture binding)

```yaml
direction_change_propagation:
  doctrine_changed: "SP-6's archive-date class D binds to the archive slice's cutoff_posture, consumed as a closed pre/post CLASS (never converted to a timestamp -- AR-03 honored), gated on an archive snapshot body present. This SUPERSEDES the design-basis rule 'D ... never cutoff_posture' (frame doc 2.3) FOR THIS BINDING ONLY. The metadata-file I/O path is dropped: the producer does not persist the cutoff (select_snapshot applies it client-side and discards it), so the ratified timestamp-comparison D-source is unimplementable; cutoff_posture is the producer's contracted pre/post class, backed by select_snapshot's at-or-before guarantee. SP-6 is therefore a pure no-I/O deriver over SourceCapturePacket (CapturePacket). The ratified SP-6 field, its 8-value/6-residual vocabulary, and the decision-C clears grade are UNCHANGED; corroborated/diverged still residualize (D2/M absent); JSG-01 stays FROZEN."
  trigger: architecture_doctrine
  related: lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md"
  evidence:
    - "orca-harness/source_capture/adapters/archive_org.py:156-160 -- select_snapshot applies the cutoff as an in-memory `<= cutoff` filter and discards it; :122-126 -- the CDX request URL carries no cutoff param."
    - "orca-harness/runners/run_source_capture_archive_packet.py:223-232 -- _availability_metadata writes no cutoff field; :268-270 -- the comment claiming the cutoff is 'preserved in the archive availability metadata' is inaccurate."
    - "select_snapshot returns max(snapshot.timestamp <= cutoff_timestamp), so a selected archive body under cutoff_posture=pre_cutoff is genuinely at-or-before the cutoff for runner packets."
  residual:
    - "cutoff_posture can be operator-set (run_source_capture_archive_packet.py:122) -- a producer attestation, the same trust SP-3 already carries by M1-reading this field. mixed/unknown/non-KNOWN -> RESIDUAL_ARCHIVE_DATE_UNKNOWN; never invented."
  superseded:
    - path: "docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md"
      what: "the 2.3 D-input rule 'never cutoff_posture' (metadata-timestamp D-source); superseded for SP-6's D-binding only. Advisory, SHA-pinned design basis -- superseded from this ratified home, not rewritten."
  downstream_surfaces_checked:
    - "docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md (untracked SP-6 plan working artifact; same supersession; re-courier not edit while frozen)"
    - "the ratified SP-6 declaration above (field/vocabulary/grade unchanged; D-source pointer added)"
  intentionally_not_updated:
    - path: "docs/product/judgment_quality_promotion_operating_model_v0.md"
      reason: "JSG-01 conductor is FROZEN; the SP-6 subpredicate it names is unchanged; this amends the source-side deriver's input binding only."
  non_claims:
    - "not the SP-6 deriver (implementation, post-amendment); records the contract amendment only"
    - "not JSG-01 unfreeze, readiness, or validation"
    - "not D2 / the corroborated tier (still deferred)"
```

### ECR consolidation v0 — JSG-01-scoped EvidenceUnit binding contract ratified

```yaml
direction_change_propagation:
  doctrine_changed: "The reserved packet->EvidenceUnit binding is OPENED and RATIFIED for exactly the JSG-01 read surface: a three-key Jsg01EvidenceBinding (evidence_id / packet_id / evidence_slice_id; assembly-authored key assertion, never a posture selector) plus a pure no-aggregate-verdict composer that re-derives SP-1/2/3/6 fresh, carries full per-slice vectors with bound-row selection by exact key (no sibling promotion; failing siblings stay visible), and carries the SP-5 validate-only consumer's verdict verbatim (BLOCKED carried, never repaired); binding keys + receipts durable, everything else re-derived; module home orca-harness/evidence_binding/. The full ECR/Evidence Unit field architecture, the canonical object name, D2/the corroborated tier, SP-4 value policing, and the JSG-01 unfreeze remain reserved; the unfreeze act must state how the frozen conductor row's D2 wording is consumed. Owner-ratified 2026-06-12."
  trigger: architecture_doctrine
  related_triggers: [lifecycle_boundary]
  controlling_sources_updated:
    - "orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md"
  design_basis:
    - path: "orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md"
      sha256: "FECCA1DFA0AFD8583A9B3B6FD138FED3937C70DD7D2584D5B34D0F5CABCB62E9"
      status: "committed with this ratification; delegated cross-vendor review-and-patch (GPT-5 / OpenAI, repo access); home-model adjudicated 2026-06-12 (all reviewer changes kept)"
    - path: "docs/review-outputs/adversarial-artifact-reviews/ecr_jsg01_evidence_unit_binding_plan_delegated_adversarial_artifact_review_patch_v0.md"
      sha256: "1E8EB59C624C6C80300A10C48F622B6448C7C61BB1C4E77F673E16241E61986D"
      status: "committed with this ratification (controller report + home-model adjudication record)"
  upstream_dependency:
    - "ECR derivers built (orca-harness/ecr/); SP-5 model + validate-only consumer committed a37f896; SP-5 producer acting half committed aeedae9 (cross-vendor reviewed + adjudicated)."
  owner_decisions:
    - "Ratify the JSG-01-scoped binding contract as adjudicated (owner word in-thread 2026-06-12); the build proceeds under the existing bounded ECR CA commission."
    - "D2-wording consumption deliberately deferred to the unfreeze act (plan DRP-01): either D2 stays a named blocker, or the owner records decision-C's determinate residual behavior as acceptable for the unfreeze boundary."
  downstream_surfaces_checked:
    - "docs/workflows/ecr_spine_submap_v0.md"  # UPDATED with this ratification: deferred line now records the JSG-01-scoped binding as ratified (build in flight); the full EU schema stays reserved
    - ".agents/workflow-overlay/safety-rules.md"  # checked, NO edit: the separate packet->EvidenceUnit gate is satisfied by this dated owner decision, not by changing the rule
    - "orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md"  # FROZEN conductor; NOT edited; coordination by re-courier (the slice-D unfreeze memo)
    - "docs/research/judgment-spine/judgment_spine_machinery_build_state_gap_map_v0.md"  # build-state map; its binding row updates when the build LANDS (build-state, not ratification state)
  intentionally_not_updated:
    - path: "orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md"
      reason: "JSG-01 conductor is FROZEN; its row is amended only inside the owner's dated unfreeze act."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Navigational and coordinator-owned; routes ECR detail through the submap, which was updated."
  stale_language_search: "rg -n 'Evidence Unit binding' docs/workflows/ecr_spine_submap_v0.md docs/research/judgment-spine/ — submap deferred line updated with this ratification; gap-map binding row intentionally updates at build landing."
  non_claims:
    - "not the full ECR/Evidence Unit field architecture or the canonical object name"
    - "not D2 or the corroborated tier"
    - "not JSG-01 unfreeze (JSG-01 stays FROZEN; the unfreeze act owns the conductor row's D2-wording consumption)"
    - "not validation, readiness, or judgment-quality evidence"
    - "not the build itself (authorized by the owner word; performed and reviewed separately)"
```

## Non-Claims

This artifact does not claim buyer validation, willingness-to-pay, repeatability
proof, product readiness, feature readiness, implementation readiness,
commercial readiness, Core Spine validation, Judgment Spine validation,
Evidence Candidate Record completion, or Evidence Unit design completion.

It does not authorize implementation, runtime design, source maps, schemas,
scrapers, automation, tests, deployment, commits, pushes, PRs, proof runs, or
feature planning.

## Current Verdict

Current verdict: `NEEDS_FOUNDATION_ACCEPTANCE`.

This artifact is a proposed product architecture boundary note. It supports
later Data Capture Spine setup, Judgment Spine, and Evidence Candidate Record /
Evidence Unit work while preserving the non-implementation Core Spine boundary.
