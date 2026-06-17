# Packing Phase To v0.14 Judgment Harness Foundation Interface Architecture (Adjudicated, Review-Corrected) v3

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Adjudicated docs-only target architecture for the Packing Phase -> v0.14 Harness Foundation interface; v3 = v2 with corrections from an independent adversarial review (AR-01..AR-05) and the Daimler pressure-test refinement (D2).
use_when:
  - Deciding whether a packed case can be admitted, rejected, quarantined, adapter-blocked, or held draft before v0.14 harness execution.
  - Separating Packing-owned bundle construction from operator labeling/freeze, Judgment-owned evidence inclusion, and Harness-owned admission/scoring.
  - Preparing later owner review or a separately authorized implementation-scoping lane without authorizing implementation, probes, scoring, validation, or product proof.
authority_boundary: retrieval_only
supersedes: docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v2.md
open_next:
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v2.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_daimler_pressure_test_v0.md
  - docs/research/packing-phase/README.md
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
input_hashes:
  superseded_v2__packing_to_harness_foundation_interface_architecture_v2.md: 5110C2DADA8741273A9830373EDCF1313B4EE0832ABEED6E96244215E5393C74
  candidate_v1__packing_to_harness_foundation_interface_architecture_v1.md: 88B15FF87C7746C91AAC30E467BF0E278D5311FDFB00FC53CB481848BE5604D0
  docs/research/packing-phase/README.md: 46E79573EDFFE48F084E49A746A925A71BC9D00C07E7EDAF1C0624ED4D2FA80D
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md: 4AF1F45964DBB560D7C6E02827BC30A9161D4433EA754580239C122DAEF532A5
branch_or_commit: main @ b7627d3389eeaa8456c65974039ada0e519617bc (dirty; controlling sources untracked)
stale_if:
  - v0.14 is superseded by a later harness version.
  - Pydantic FacilitatorLedger schema adds case_family, decision_shape, memorization_probe_required, or known_fame_risk as first-class fields.
  - Packing-phase README ownership or the Core Spine Inclusion State Rule changes layer ownership.
  - The band-input labeling rubric changes the labeling actor or freeze workflow.
  - A third case exposes a generic interface field missing here.
```

- Status: TARGET_RECOMMENDED (adjudicated; candidate accepted with modifications; review-corrected)
- Lineage: v1 (GPT candidate) -> v2 (adjudicated) -> v3 (this; v2 + independent-review corrections AR-01..AR-05, which absorb Daimler refinement D2)
- Implementation, runtime, probe execution, scoring, validation, proof, lesson promotion: not authorized
- Strict acceptance, validation, readiness, source-of-truth promotion, harness superiority: not proven

## Changes From v2 (Independent Adversarial Review)

v3 incorporates findings from one independent cold-context adversarial review of v2 (advisory; it diffed v2 against the v1 candidate and attacked the changes without access to the adjudicator's reasoning). The review was **context-independent but not model-independent** (same model family as the adjudicator); a **model-diverse (GPT-5.5) pass is deferred to the gate** — i.e., before this interface is bound into a running case-admission or implementation-scoping lane. Corrections:

- **AR-01 (major) — pre_decision_status ownership over-read, corrected.** v2 bound *final* evidence `pre_decision_status` to the "operator labeling step under Judgment authority." But the band-input labeling rubric (v2's cited source for that step) governs only the 14 band-input enums — it never covers evidence inclusion. The Core Spine Inclusion State Rule assigns integrity-exclusion / decision-use-downgrade to **Judgment Spine**. v3 keeps the sourced claim (final inclusion is Judgment-authority-owned, not Packing) and demotes the unsourced fusion (that the band-labeling operator *is* that Judgment authority) to an explicit open owner decision.
- **AR-05 (major) — contestant-visible source manifest could leak provenance, corrected.** The Pydantic participant-packet frontmatter carries a `source_manifest` with `source_id`/`source`/`retrieval_timestamp`/`hash` inside the contestant-facing packet. v3 separates a **packet-safe, source-class-labeled** contestant-visible manifest from **facilitator-only provenance** (IDs, timestamps, source-byte hashes). This is the same issue as Daimler pressure-test finding D2; two independent paths found it.
- **AR-03 (minor->major) — hash-gate verifiability, corrected.** v2's `bytes_available` rule routed missing bytes to `adapter_blocked`, but Harness hash *recomputation* needs the source bytes (or an inspectable reference) to actually reach the Harness, which v2 never required as a handoff item. v3 names source-bytes / inspectable-reference as a required Packing handoff so a `bytes_available: true` hash can be verified rather than trusted.
- **AR-02 (minor) — admission crosswalk coherence, corrected.** v2 let a Packing `reject_request`/`quarantine_request` map to exactly one Harness decision, letting Packing unilaterally force a terminal decision. v3 maps each request to a set of possible Harness decisions and lets the Harness override.
- **AR-04 (minor) — disclosure, corrected.** `bytes_available` and the `proposed` pre-decision status are interface vocabulary, not v0.14 Pydantic schema fields (the `PreDecisionStatus` enum has only `verified_pre_decision`/`uncertain_timestamp`/`excluded`). v3 labels them as interface vocabulary wherever introduced.

Confirmed holding by the review (unchanged from v2): M2 (operator-freeze), M6 (generalized leakage surface — independently judged the better abstraction, converging with Daimler D1), M7, M8; and no unsupported strict claims.

## Adjudication Receipt

v3 is the review-corrected adjudication of the GPT candidate (v1). It is an adjudicated architecture recommendation only — **not** owner acceptance, validation, readiness, implementation/scoring authorization, probe pass, product proof, lesson promotion, or harness superiority.

```yaml
adjudication:
  candidate_path: docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v1.md
  candidate_sha256: 88B15FF87C7746C91AAC30E467BF0E278D5311FDFB00FC53CB481848BE5604D0
  disposition: modified_accept
  architecture_result: TARGET_RECOMMENDED
  selected_target: block_first_hybrid_harness_entry_bundle_interface
  review_status: independent cold-context subagent review applied (AR-01..AR-05); model-diverse review deferred to gate
  empirical_check: Daimler second-case pressure test passed (interface fits; M6 validated; D2 == AR-05)
```

## Source Context Receipt

```yaml
source_context_status: SOURCE_CONTEXT_READY
profile: standard
hash_drift_handling:
  pinned_hashes_matched: 3 of 5 (bridge foundation, Unity plan, thesis contract)
  pinned_hashes_drifted: 2 of 5 (packing README, v0.14 index) -- immaterial navigation-pointer additions; re-pinned to current hashes; advisory-only; strict claims not proven
workspace: main @ b7627d3389eeaa8456c65974039ada0e519617bc; dirty; controlling sources untracked
```

Per the overlay control-plane source-state gate, untracked/modified controlling sources support advisory architecture work but do not establish strict acceptance/validation/readiness. This artifact makes no strict claim.

## Architecture Question

What target architecture should govern the boundary between Packing Phase outputs and Judgment Harness Foundation inputs so that Packing can transform cleaned evidence into judgment-ready case artifacts; the Harness can freeze inputs and run deterministic checks without absorbing Packing / Cleaning / Data Capture / Judgment / lesson-promotion responsibilities; future implementation scoping has a stable interface; and missing provenance, leakage, unresolved adapters, or missing labels block admission instead of being silently repaired?

Inferred: label freezing and final evidence inclusion are distinct from both Packing drafting and Harness mechanics — they form an operator/Judgment middle zone (rubric: operator resolves/freezes band inputs; Core Spine: Judgment owns evidence inclusion/exclusion).

## Options Compared

Unchanged from the candidate and v2 (the option set is not in dispute):

| Option | Shape | Result |
| --- | --- | --- |
| AO-1 Cleaning feeds Harness directly | Cleaning normalized evidence straight to harness fixtures. | Rejected (collapses cleaned-vs-judgment-ready distinction). |
| AO-2 Packing emits formal HEB | Packing emits the bundle; Harness consumes. | Retained only inside the hybrid. |
| AO-3 Harness owns packing/admission | Harness constructs/repairs packets, labels, admission. | Rejected (collapses layers; block-don't-repair inversion). |
| AO-4 Manual per-case fixtures | No general interface. | Rejected as target; exemplar-only. |
| AO-5 Hybrid (block-first HEB) | Packing builds bundle; operator/Judgment middle zone freezes/finalizes; Harness admits/scores; small block-first adapters. | **Selected.** |

## Adjudicated Target Architecture

`TARGET_RECOMMENDED` — block-first hybrid Harness Entry Bundle interface, with three operating zones plus a small adapter set:

1. **Packing** builds the draft Harness Entry Bundle (HEB) — a named admission object, not an implementation package and not a scoreable fixture. Packing produces candidates and drafts, never frozen truth.
2. **Operator labeling + Judgment zone.** Band-input labels are labeled, second-labeled, diffed, resolved, and frozen by the **operator** per the band-input labeling rubric (emitting `ledger_freeze_hash`, `committed_at`, `labeling_rubric_version`). **Final evidence `pre_decision_status` (integrity-exclusion / decision-use-downgrade) is Judgment-authority-owned per the Core Spine Inclusion State Rule.** [AR-01] Whether the band-labeling operator *is* the Judgment authority that finalizes evidence inclusion, or whether that is a separate Judgment step, is an explicit open owner decision (see "What Is Intentionally Undecided") — this artifact does not assume they are the same actor.
3. **Harness Foundation** admits and scores mechanically (recompute hashes, validate schemas, deterministic action-band derivation, deterministic scoring, append-only failure logging). **Block, don't repair.**

Plus a small **adapter layer** (source-visibility gap, optional `legacy_prior_judgment` such as a sealed memo, protocol-to-Pydantic field carry). Adapters surface and block; they never infer or repair.

Two invariants: **block-don't-repair** and **structure is not admission**.

## Core / Satellite Boundary

Core (interface-invariant in v0.14): HEB interface; admission-state model; Packing/operator-Judgment/Harness zone split; Judgment-owned final evidence inclusion [AR-01]; contestant-visible vs facilitator-only boundary (incl. the packet-safe manifest split [AR-05]); Harness freeze inputs; deterministic checking/scoring boundary; report meaning/non-meaning; inadmissibility states; non-claims.

Satellite (per-case): Unity/Daimler specifics; `legacy_prior_judgment` adapter content; source-visibility-gap adapter content; case-family evidence-adapter choices; future file layout, runtime, tests, CI; parent lesson promotion and product-proof interpretation.

## Packing-Owned Outputs

Packing produces the draft HEB and self-checks admissibility. Packing owns:

- participant-packet candidate (Pydantic-shaped frontmatter + packet body; excludes outcome, frozen labels, derived floor/ceiling, must-address items, hidden/decoy labels, post-decision interpretation);
- a **packet-safe, source-class-labeled source manifest** for the contestant view (class/source-family labels, no URLs/titles) **[AR-05]**;
- evidence-registry candidate: one `EvidenceUnit`-shaped entry per unit with full provenance (`source_id`, `source`, `timestamp`, `retrieval_timestamp`, source-byte `hash`), a `bytes_available` declaration *(interface vocabulary, not a v0.14 schema field — AR-04)*, **a source-bytes payload or inspectable reference so the Harness can recompute and verify each hash [AR-03]**, and a **proposed** `pre_decision_status` + `pre_decision_basis` *(“proposed” is interface vocabulary; final status is Judgment-owned — AR-01/AR-04)*. This provenance is **facilitator-only**, not part of the contestant-visible manifest **[AR-05]**;
- provenance/cleaning receipt (hashes or justified gaps, retrieval timestamps, cleaning-trace status, cutoff basis);
- visibility boundary (contestant-visible / facilitator-only / parent-only / excluded);
- leakage/spoiler receipt: `outcome_leakage_classes` exclusions + case-conditional `memorization_probe_required` / `known_fame_risk` seeds;
- adapter/gap ledger (with a per-gap "blocks admission?" flag);
- facilitator-ledger work queue (drafts only, explicitly not frozen scoring truth);
- draft admission **request** + inadmissibility self-check.

Packing does **not** own: source acquisition/preservation; cleaning mechanics; frozen labels; **final `pre_decision_status` (Judgment-owned, AR-01)**; action-band derivation; scoring; probe execution; model runs; failure logging; lesson promotion; product-proof claims.

## Harness-Owned Freeze / Admission / Scoring Surfaces

The Harness freezes/admits only after required inputs exist, and **blocks rather than repairs**. v0.14 binding of the abstract frozen-scoring-inputs slot: canonical `case_id`; `participant_packet_hash`; evidence registry **with source bytes/inspectable references so each `bytes_available: true` hash can be recomputed and verified [AR-03]**; frozen `FacilitatorLedger` (operator output: `labeling_rubric_version: v0_14`, `mapping_table_version_pin: v0_14_mvp`, `ledger_authors`, `second_label_diffs` (present even if empty), `frozen_band_inputs`, `must_address_items`, `underreach_observability`, `leakage_audit_notes` (carrying the protocol-to-Pydantic interim content), `spoiler_inventory` (sealed facilitator-only; never enumerated in the ledger body or any participant packet), `committed_at`, `ledger_freeze_hash`); final Judgment-owned `pre_decision_status` per unit [AR-01]; memorization-probe result for the target model family before packet exposure; schema-valid `BlindJudgement` + run metadata when scoring is requested.

The Harness recomputes/verifies hashes, validates schemas, applies `judgement_class_ladder_mapping`, runs deterministic band derivation and scoring, writes append-only failure events (`not_a_rule: true`, `promotion_allowed: false`; raises on `promotion_allowed=True`). It must not author labels, finalize `pre_decision_status`, run probes, repair missing hashes, accept draft bundles, promote failures to rules, or claim baseline superiority.

## Admission State Model

Packing emits a **request**; the Harness emits a **decision**. Each request maps to a *set* of possible Harness decisions; the Harness may override a request it disagrees with **[AR-02]**.

| Packing request | Meaning | Harness decision set | Owner of decision |
| --- | --- | --- | --- |
| `draft_only` | Not ready; docs inspection only. | `draft_only` | Packing self-declares; Harness confirms |
| `admit_candidate` | Packing believes inputs complete. | `admit_for_freeze` / `adapter_blocked` / `quarantine` / `score_blocked` / `reject` / `draft_only` | Harness |
| `quarantine_request` | Packing flags a material risk. | `quarantine` / `adapter_blocked` / (Harness may downgrade to `admit_for_freeze` if risk is immaterial) | Harness/operator; Judgment authority when the risk is integrity/decision-use |
| `reject_request` | Packing believes the case should not proceed. | `reject` / `quarantine` / `draft_only` / (Harness may override toward `admit_for_freeze` with recorded reason) | Harness/operator |

Harness decision states: `admit_for_freeze` (complete enough for a later authorized freeze; not validation/score-readiness), `adapter_blocked` (unresolved case-specific adapter gap), `quarantine` (material risk; retained, cannot proceed until review), `reject` (should not be used for the requested path), `score_blocked` (frozen upstream but missing valid BlindJudgement/run-metadata/probe/version), `draft_only` (confirmed not admissible).

A well-structured bundle may still receive a non-admit decision. **Structure is not admission.**

## Contestant-Visible Boundary

Contestants see only the rendered prompt built from the frozen participant packet: packet-safe case identity, decision question, cutoff, role frame, authority/capability constraints, known uncertainties, permitted assumptions, the whitelist-only information boundary ("decide using only the information in this brief"; no enumerated forbidden-category list), packet-safe evidence summaries, and the **packet-safe, source-class-labeled source manifest (no source URLs, titles, IDs, retrieval timestamps, or source-byte hashes) [AR-05]**.

Full provenance (`source_id`, `retrieval_timestamp`, source-byte `hash`) is **facilitator-only evidence-registry content and must never appear in the contestant-visible manifest [AR-05]** — this preserves the overlay zero-spoiler gate.

Contestants do **not** see: any `outcome_leakage_class`; frozen band inputs; derived floor/ceiling; the facilitator ledger; must-address items; hidden/decoy labels; probe result or `known_fame_risk`; any `legacy_prior_judgment`; other contestants' outputs; or source identifiers/provenance. Semantic leakage remains partly operator/review work; admission checks declared boundaries and hard markers only.

## Deterministic Checking Boundary

Deterministic at scoring time (schema-backed): schema validation; hash recomputation/verification; pure enum-to-action-band mapping from frozen `BandInputs`; inclusive band scoring; overreach/underreach distances; underreach-primary gate; evidence-ID presence; excluded/post-decision citation checks; load-bearing-claim citation presence; must-address coverage; mapping-version mismatch refusal; probe result carried into `ScoringResult`; append-only failure logging.

Subjective at labeling time (operator/Judgment, not scoring): each `BandInputs` value; must-address selection; underreach-observability; leakage-audit content; `decision_shape`; `legacy_prior_judgment` treatment; final `pre_decision_status` (Judgment authority).

Phase 1 does not check: semantic relevance; direct-vs-inferential support; contradiction; cross-run improvement; memory compounding; baseline superiority.

## Report Meaning And Non-Meaning

A v0.14 `ScoringResult`/`CaseReport` means fixed inputs and a fixed contestant output were mechanically processed under the v0.14 mapping/scoring/version/hash contract, with shallow evidence-ID/must-address/probe fields reported and failure events appended non-promotionally. It does **not** mean product-readiness, baseline superiority, proven judgment quality, semantic support, lesson promotion, memory compounding, sealed-memo comparability, absence of memorization, or validation of Packing/operator labeling.

## Inadmissibility / Block States

Required end states a future admission gate must enforce (this artifact defines, does not enforce):

- **Packing-side:** missing frontmatter field; forbidden item in packet; `EvidenceUnit` missing required provenance; `bytes_available: true` without a verifiable source-byte hash *or without source bytes/inspectable reference for recomputation* [AR-03]; `bytes_available: false` without justification; missing proposed `pre_decision_status`; source-visibility gap with no adapter decision; missing leakage/spoiler receipt; missing visibility boundary or parent-only list; `legacy_prior_judgment` present without adapter inputs; draft-vs-frozen marker absent/draft; any work-queue item presented as frozen truth; **source identifiers/provenance present in the contestant-visible manifest [AR-05]**.
- **Operator/Judgment labeling-step:** any `BandInputs` field not enum-valid; `second_label_diffs` absent; rubric quarantine triggers met; must-address promoted verbatim from Packing candidates; `underreach_observability.basis` non-enum; `mapping_table_version_pin`/`labeling_rubric_version` wrong; `ledger_freeze_hash`/`committed_at` missing/invalid; **final `pre_decision_status` not finalized by Judgment authority [AR-01]**; protocol-to-Pydantic content absent from `leakage_audit_notes`.
- **Probe:** no probe artifact for the target model family; `fail` -> reject/quarantine; `ambiguous` without review -> quarantine.
- **Run-binding / scoring (`score_blocked`):** `decision_shape` not frozen; packet/ledger hash missing/mismatched; `prompt_hash`/`harness_version` missing; `BlindJudgement` violates ladder mapping; `legacy_prior_judgment` asserted as `BlindJudgement` without required fields + contamination caveat.
- **Cross-cutting:** any `outcome_leakage_class` in participant-facing content; any `promotion_allowed=True`; any write to forbidden Phase-1 memory dirs; any superiority computation.

**Block-don't-repair is the invariant; silent repair is itself a block-class failure.**

## Deferred Implementation Implications

Non-executable. A later authorized implementation-scoping lane would inherit: model the HEB as an admission surface; keep adapters block-first; require a `bytes_available` declaration + inspectable reference so hashes are verifiable [AR-03]; separate packet-safe manifest from facilitator-only provenance [AR-05]; keep `pre_decision_status` finalization with Judgment authority [AR-01]; require version/hash before scoring; keep scoring pure; keep semantic checking out of Phase 1; keep failure logs append-only; one contestant runner. Before code, reopen `phase_1_infrastructure_architecture.md`, recheck hashes, bind one fixture scope, obtain explicit authorization.

## What Is Intentionally Undecided

- **Whether the band-labeling operator is the Judgment authority that finalizes evidence `pre_decision_status`, or whether finalization is a distinct Judgment step (possibly a fourth named role) [AR-01].** v3 binds the *authority* (Judgment) but not the *staffing*.
- Whether `case_family`/`decision_shape`/`memorization_probe_required`/`known_fame_risk` become first-class Pydantic fields or remain protocol metadata via the adapter slot.
- Exact serialized bundle format; whether `legacy_prior_judgment` outputs an explicit advisory-baseline record type.
- Whether Unity, Daimler, or another case is exercised end-to-end first.
- Any runtime layout, validation commands, tests, CI, packages, runners.

## What Would Change The Recommendation

Owner authorization of Packing-owned labeling or Harness-owned packet construction; a v0.15+ harness; a `FacilitatorLedger` revision adding the four protocol fields; a Core Spine boundary patch reassigning ownership; a third case exposing a missing generic field; evidence the adapter layer can't stay block-first; or formal-bundle overhead exceeding its boundary-safety value.

## Bloat-Cut Queue

Do not invent: Cleaning->Harness direct handoff; Harness-owned packing; Harness repair of provenance/labels/gaps/leakage; per-case manual fixtures as the general interface; Unity-specific fields as interface fields; a new leakage/evidence schema; a Packing-side validator/scorer/runner/hashing routine separate from `ledger_freeze_hash`/`EvidenceUnit.hash`; new ladder/judgement-class vocab; a new bundle file shape; a `legacy_prior_judgment` conversion engine; a Packing->Cleaning re-clean back-channel; memory/rules/retrieval dirs; lesson-promotion mechanics; product-/buyer-proof claims; broad repo-map/manifest rewrites from this artifact alone.

## Non-Claims

Does not claim: Judgment Spine or v0.14 harness validation/readiness/superiority; Packing/operator-labeling validation; probe pass; score-readiness or case admission; `legacy_prior_judgment` comparability; semantic support beyond shallow checks; source-of-truth promotion of any source or this artifact; acceptance/approval; implementation/runtime authorization; buyer/product/feature/commercial readiness; model-training readiness, memory compounding, or rule-promotion authority; that Unity is probe-safe/best-first; that Daimler is manifest-accepted; that dirty/untracked sources are accepted authority; that any subagent/review output is a verdict or proof.

## Version And Collision Note

Lineage at this stem: `_v0` (off-spec architecture-planning attempt, wrong prompt), `_v1` (consumed GPT candidate), `_v2` (adjudicated), `_v3` (this; review-corrected, current recommended). v3 `supersedes` v2 for retrieval routing only — not owner acceptance. v0/v1 disposition is an owner decision (tracked in `docs/hygiene/queue.md` ORCA-HYGIENE-002).

## Source-Read Ledger

| Source | Why | State |
| --- | --- | --- |
| v2 (superseded) + v1 (candidate) | Baseline + adjudicated predecessor; hashed | created this session; hashes recorded |
| packing README; v0.14 index | Packing ownership; spec roles | untracked; re-pinned (immaterial nav drift) |
| bridge foundation; Unity plan; thesis contract | Min harness-entry shape; non-claims; layer boundaries | untracked; hashes match pin |
| core_spine boundary note | Inclusion State Rule (AR-01); layer table | untracked; read |
| band_input_labeling_rubric | Freeze owner (M2); enums; quarantine | untracked; read |
| pydantic_schema_reference | Schema surface; PreDecisionStatus enum (AR-04); source-byte hash rule (AR-03); manifest fields (AR-05) | untracked; read |
| Daimler packet/safety receipt/preflight | Second-case pressure test (D2 == AR-05) | untracked; hashed in pressure-test note |
| Independent adversarial review (cold subagent) | AR-01..AR-05 | advisory; applied |

## Next Authorized Step

Docs-only. v3 may be used to bind a future Unity/Daimler case-admission CA prompt or fed as the frozen interface input to a separately authorized implementation-scoping prompt (which must reopen `phase_1_infrastructure_architecture.md`, recheck source state, bind one fixture scope, and obtain explicit bounded implementation authorization). At that gate, run a model-diverse (GPT-5.5) independent review of v3's deltas before binding. Do not route directly to implementation, probe execution, scoring, proof-run, product proof, or lesson promotion.
