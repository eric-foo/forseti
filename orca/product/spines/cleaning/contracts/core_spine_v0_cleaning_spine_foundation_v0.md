# Core Spine v0 Cleaning Spine Foundation

```yaml
retrieval_header_version: 1
artifact_role: Product-method foundation artifact
scope: >
  Cleaning Spine v0 layer contract for non-destructive transformation of raw,
  projected, and Evidence Candidate Record material into Judgment-usable working
  views without replacing raw evidence or smuggling Judgment.
use_when:
  - Defining what Cleaning may transform after Data Capture, projection, or Evidence Candidate Record.
  - Checking traceability, ledger, raw-pull, dedupe, clustering, translation, or summarization rules before Judgment.
  - Separating Cleaning mechanics from Judgment-owned credibility, independence, salience, and decision-use effects.
authority_boundary: retrieval_only
open_next:
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
stale_if:
  - Owner changes the 2026-06-16 OD-1 / OD-4 / OD-7 direction recorded here.
  - Projection Doctrine v0 is amended, superseded, ratified differently, or rejected.
  - The Data Capture / ECR / Cleaning / Judgment boundary note changes Cleaning ownership.
```

- Status: `FOUNDATION_DRAFT_FROM_PROJECTION_CANDIDATE`
- Source context: `SOURCE_CONTEXT_READY` at authoring.
- Projection doctrine source at authoring: `PR_191` / worktree source. Local `main`
  did not contain `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` on intake.
- Implementation authorized: bounded_substrate_v0 (source-invariant Pydantic models + exact-identity deriver; `orca-harness/cleaning/`; does not authorize broader Cleaning, ECR, or Judgment implementation)
- Runtime schema authorized: bounded_substrate_v0 (in-memory Pydantic schema only; not a persisted storage, API, or final object-model schema)
- Owner OD direction installed: 2026-06-16; see `Owner Directions Installed`.
- Proof run, capture execution, crawler, scraper, API, dashboard, or automation
  authorized: no

## Purpose

Cleaning Spine turns preserved public-source material into smaller,
traceable, Judgment-usable working material. It does this by recording
non-destructive transformations over raw capture, Data Capture Projection
Packet views, and Evidence Candidate Record receipt material.

Cleaning exists to make later review inspectable, not to decide what the
evidence means. Raw remains canonical. Projection and Cleaning are working
views with traceability obligations. Judgment owns credibility, independence
effects, salience, Signal Integrity, Signal Use, Decision Strength, and Action
Ceiling.

## Status / Scope / Non-Claims

This artifact is a foundation draft. It uses Projection Doctrine v0 as a kept
candidate for owner confirmation, not as ratified doctrine. It does not amend
the Data Capture / Evidence Candidate Record / Cleaning / Judgment boundary.

Non-claims:

- Not validation, readiness, buyer proof, Judgment quality, or product proof.
- Not a runtime schema, storage model, API, scraper, crawler, adapter, dashboard,
  automation, test plan, or feature plan.
- Not final object naming for "Projected Unit", "Cleaned Unit", Evidence
  Candidate Record, or Evidence Unit.
- Not a decision that cleaned material can replace raw or projection anchors.
- Not authority for Cleaning to decide credibility, discounting, exclusion,
  independence, support for demand, Decision Strength, or Action Ceiling.

## Authoring Intake Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_cleaning_foundation
  edit_permission: docs-write
  target_scope: orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
    - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
```

Sources loaded for this foundation:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/validation-gates.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
- `orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/workflows/orca_repo_map_v0.md` targeted section only, for path/map
  placement.

## Layer Boundary

Cleaning sits after Data Capture, mechanical source projection where used, and
Evidence Candidate Record receipt material. Its job is the transformation
ledger and the cleaned working view.

| Layer | Cleaning may use | Cleaning must not take over |
| --- | --- | --- |
| Data Capture Spine | Raw packet anchors, source identity, timing, visibility, capture context, and projection packet references. | Source acquisition, access-path decisions, source truth, capture operations, projection ownership, or source-envelope removal authority. |
| Mechanical Source Projection | Data Capture Projection Packet row view, projection receipt, loss ledger, warnings, residuals, and raw anchors. | Projection as a standalone spine layer, projection schema ratification, or deciding salience through compactness. |
| Evidence Candidate Record | Pre-cleaning receipt facts, categorical handoff state, raw/projection references, provenance/timing/capture-context obligations. | Final ECR schema, Evidence Unit design, integrity labels, signal-use claims, or certification that a view is normalized. |
| Judgment Spine | Receives cleaned working material, transform ledger, warnings, residuals, and raw-pull triggers. | Credibility, independence effects, discounting, exclusion, Signal Integrity, Signal Use, Decision Strength, or Action Ceiling. |

Cleaning may carry a mechanical blocker or warning, but the reason must be
layer-owned. Acceptable Cleaning-side reasons include normalization conflict,
duplicate cluster unresolved, translation trace missing, summary trace missing,
projection anchor missing, raw anchor missing, hierarchy preservation uncertain,
or source-family rule unresolved.

Forbidden Cleaning reasons include discounted, excluded, weak, strong, credible,
not credible, supports demand, independent corroboration, artificial
amplification, action supporting, or any equivalent Judgment-use label.

## Inputs Cleaning May Receive

Cleaning may receive:

- Raw capture packet references and source slices.
- Data Capture Projection Packet views, including projection rows, projection
  receipt, loss ledger, warnings, omissions, and residuals.
- Evidence Candidate Record receipt material, including pre-cleaning categorical
  handoff state and provenance/timing/capture-context obligations.
- Source-family adaptation notes when they are clearly marked as source-family
  adaptation or unresolved candidate rules.

Cleaning must preserve the difference among those inputs. A projection view is
not raw. A Cleaning output is not raw. An ECR receipt is not a Judgment claim.

To keep OD-1 maintainable, Cleaning should not require every transform entry to
repeat raw + projection + ECR references. The smallest complete architecture is
a single **Cleaning input handle** keyed to raw. That handle may attach a
projection reference and ECR reference when present, while each transform entry
references the handle by key.

## Allowed Transform Classes

Cleaning may perform these classes only when they are ledgered, traceable, and
non-destructive.

This follows the current boundary-note posture that Cleaning may record
mechanics, with the OD-4 owner direction narrowed for core v0: Cleaning may
code-enforce exact-identity dedupe mechanics. Near-match dedupe, copied-language
grouping, and clustering remain candidate/deferred mechanics unless separately
owner-authorized.

| Transform class | Allowed Cleaning act | Required preservation |
| --- | --- | --- |
| Normalization | Normalize format, units, encoding, whitespace, casing where meaning is not changed, date display, or source-native representation into a working form. | Original value, normalized value, method/rule, raw anchor, projection anchor where applicable, and conflict/residual when meaning could change. |
| Translation | Translate source-language text for reviewer access. | Source-language text paired with translation, translator/method reference, ambiguity notes, and raw/projection anchors. |
| Summarization | Produce a compact summary of rows, chains, bundles, or slices for navigation. | Originals remain addressable; summary links to row/slice anchors; omissions and residuals are visible; summary never replaces evidence rows. |
| Dedupe mechanics | Record exact-identity duplicate membership, mechanical identity basis, counts, and instance links for core v0. Near-match similarity and copied-language grouping remain candidate/deferred unless separately owner-authorized. | Every original instance, source identity, timing, venue, chain location, count, and exact-identity group membership. |
| Clustering mechanics | Candidate/deferred only: group related instances by a declared mechanical basis when separately owner-authorized or explicitly labeled as unresolved routing. | Membership list, grouping basis, counts, raw/projection anchors, warnings, unresolved ambiguity, and candidate/deferred status. |
| Receipt / ledger propagation | Carry capture, projection, ECR, and Cleaning warnings forward. | Warning provenance, layer owner, source anchor, and whether Judgment must reopen raw. |

Cleaning must not remove evidence rows because they appear low-value, low-score,
repetitive, embarrassing, bot-like, deleted, awkward, unhelpful, confusing, or
non-salient. Compactness is never salience.

## Non-Destructive Ledger Contract

Cleaning must leave a minimum transformation ledger that lets a later reviewer
answer: what changed, why it changed mechanically, what raw/projection material
it came from, what was preserved, and what must still be inspected.

This is an illustrative contract, not a frozen runtime schema:

```yaml
cleaning_input_handle_candidate:
  handle_id: "<stable cleaning input handle id>"
  raw_anchor: "<packet/slice/hash or modality-appropriate anchor>"
  projection_anchor: "<projection packet/row/receipt anchor, when used>"
  ecr_ref: "<receipt/read reference, when used>"
  relation: "keyed_siblings_over_raw"

cleaning_transform_ledger_candidate:
  input_handle_id: "<stable cleaning input handle id>"
  transform:
    class: "<normalization | translation | summarization | dedupe_mechanics | clustering_mechanics | propagation>"
    # In core v0, dedupe_mechanics is exact-identity only.
    # Near-match grouping and clustering_mechanics are candidate/deferred unless separately owner-authorized.
    method_or_rule: "<candidate method/rule label>"
    input_grain: "<row | chain | bundle | slice | packet | cluster>"
    output_view: "<candidate cleaned working view reference>"
  preservation:
    originals_addressable: true
    source_identity_preserved: true
    timing_preserved: true
    hierarchy_preserved: true
    semantic_binding_preserved: true
    counts_preserved: true
  residuals_and_warnings:
    omissions: []
    residuals: []
    warnings: []
    raw_pull_triggers: []
  non_claims:
    - no_credibility_decision
    - no_independence_effect
    - no_signal_use_or_action_ceiling
```

Candidate field names above are examples only. OD-7 keeps "Projected Unit" as a
working label, not durable ontology. A future runtime schema would need separate
owner authority.

## Traceability And Raw-Pull Rules

Every Cleaning output must preserve or link:

- raw anchor;
- projection anchor where projection was used;
- source identity and source-family context;
- event, publication, edit, capture, recapture, cutoff, archive, or visibility
  timing as separate facts when available;
- hierarchy, parent/child chain, review rating/text pair, bundle structure,
  variant/price/availability binding, source-visible labels, and layout/media
  cues when they carry meaning;
- counts, cluster membership, duplicate membership, omissions, residuals, and
  warnings;
- the layer owner of every blocker or warning.

Cleaning must pull raw, halt, or escalate when:

- a raw anchor is missing, stale, ambiguous, or inconsistent with the projected
  view;
- a projection anchor is missing where Cleaning is transforming projected
  material;
- translation, summary, normalization, dedupe, or clustering would change
  source meaning rather than expose mechanics;
- hierarchy, bundle structure, timing, labels, media, source-visible layout, or
  domain-native language is needed to understand the signal;
- a source-family adaptation rule would become universal without owner
  acceptance or comparison across at least two non-overlapping families;
- the transform would require deciding credibility, independence effect,
  exclusion, demand support, Signal Integrity, Signal Use, Decision Strength, or
  Action Ceiling;
- installed OD-1, OD-4, or OD-7 direction would need to be changed or widened to
  continue without freezing a schema or object model.

Judgment must reopen raw for at least these claim types or thresholds:

- demand read;
- cutoff or backtest claim;
- sponsored, paid, vendor-moderated, deleted, locked, archived, or
  visibility-dependent claim;
- copied/coordinated or artificial-amplification call;
- media-, layout-, hierarchy-, bundle-, or version-dependent meaning;
- any Move or Commit recommendation;
- any claim that depends on credibility, discounting, exclusion, independence
  effect, Signal Integrity, Signal Use, Decision Strength, or Action Ceiling.

## Dedupe / Clustering Mechanics

Under the current boundary note, Cleaning may record mechanics. Judgment decides
the effect. OD-4 owner direction narrows core v0 to exact-identity dedupe
mechanics; near-match dedupe, visible copied-language grouping, and clustering
remain candidate/deferred unless separately owner-authorized.

Cleaning core v0 may record:

- exact preserved-file byte/hash identity membership;
- exact anchored source-text identity membership when projection or source
  material exposes an M1-carried text span;
- the mechanical identity basis used;
- source, venue, actor, time, chain, and packet/slice anchors for every member;
- duplicate counts and unresolved ambiguity;
- whether the exact-identity group needs Judgment raw pull before independence
  can be weighed.

Cleaning may not promote near-match similarity, copied-language grouping, or
semantic clustering into core v0 merely because it is useful. Those mechanics can
be recorded only as explicitly labeled candidates or deferred routing objects
until their ownership and independence boundary are separately settled.

Cleaning must not decide:

- independent corroboration;
- artificial amplification;
- botting;
- copied/coordinated intent;
- credibility or integrity effect;
- whether duplicates support demand;
- whether a cluster raises or lowers Decision Strength or Action Ceiling.

If dedupe or clustering would hide whether repetition is independent
corroboration or artificial amplification, the transform must be non-destructive
and must preserve the original instances for Judgment.

## Source-Family Adaptation Boundary

Each Cleaning rule must be labeled as one of:

- `source_invariant_core`: required across source families, such as raw
  preservation, non-destructive transforms, raw/projection anchors, no evidence
  row removal, no salience decision, and no Judgment effects.
- `source_family_adaptation`: useful for a family such as threads, review
  surfaces, social/video, retail/PDP, official/package documents, or
  browser-visible access overlays, but not universal yet.
- `unresolved_candidate`: plausible but not accepted; may be used only with a
  warning and must not become a hidden core rule.

Family-specific heuristics should not become core until they survive comparison
across at least two non-overlapping source families or the owner explicitly
accepts the exception.

## Cleaning-To-Judgment Handoff

Acceptable Cleaning outputs for Judgment:

- cleaned working view with raw and projection anchors;
- transformation ledger;
- translation paired with source text;
- summary linked to original rows, chains, bundles, slices, or clusters;
- dedupe and clustering membership with counts and original instances;
- mechanical blocker and warning tokens with layer-owned reasons;
- residuals and raw-pull triggers.

Judgment must treat Cleaning outputs as navigation and mechanics. Judgment
reopens raw whenever a material claim depends on source meaning, credibility,
independence, salience, Signal Integrity, Signal Use, Decision Strength, Action
Ceiling, or the raw-pull triggers above.

Cleaning may make material easier to inspect. It may not make material more
true, more independent, more credible, more important, more demand-supporting,
or more action-supporting.

## Owner Directions Installed

- **OD-1 / pipeline ordering:** Cleaning uses one input handle keyed to raw, with
  optional projection and ECR references attached when present. Projection and
  ECR remain keyed siblings over raw for Cleaning purposes; transform entries
  reference the handle rather than carrying three repeated reference surfaces.
- **OD-4 / where dedupe and clustering live:** Cleaning core v0 may code-enforce
  exact-identity dedupe mechanics only. Near-match dedupe, copied-language
  grouping, and clustering remain candidate/deferred mechanics unless separately
  owner-authorized. Any independence, credibility, uncertainty, exclusion, Signal
  Integrity, Decision Strength, or Action Ceiling effect remains Judgment-owned.
- **OD-7 / naming and object model:** "Projected Unit" is a working label for the
  existing Data Capture Projection Packet row view. This artifact does not
  promote "Projected Unit", "Cleaned Unit", or any new object into canonical
  spine ontology.

## Validation / Review Needed

This artifact should receive adversarial artifact review before owner
ratification or before it is used to authorize implementation. A clean mechanical
checker run on this file means only that the document has required structure and
no obvious diff hygiene issue; it is not validation, readiness, or acceptance.

Future validation or review should attack:

- whether any Cleaning blocker reason still carries Judgment semantics;
- whether the ledger contract accidentally freezes a runtime schema;
- whether an implementation widens beyond the installed OD-1 / OD-4 / OD-7
  directions;
- whether source-family adaptations are clearly separated from source-invariant
  core rules;
- whether Judgment raw-pull triggers are too weak for demand, cutoff, sponsored
  label, copied/coordinated, archive/deleted, Move, or Commit claims.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Added an additive Cleaning Spine foundation draft that records the current
    non-destructive Cleaning contract from existing Projection, boundary,
    corroboration/amplification, and capture-context sources without ratifying
    Projection Doctrine v0 or authorizing runtime implementation. Updated after
    owner direction on 2026-06-16: OD-1 uses a single Cleaning input handle keyed
    to raw with optional projection/ECR references; OD-4 narrows core v0 to
    exact-identity dedupe mechanics only; OD-7 keeps "Projected Unit" as a
    working label, not durable ontology.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/orca_repo_map_v0.md
    - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md
    - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
    - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The artifact was created under an already map-covered Core Spine folder.
        The repo-map freshness checker remains required, but this additive draft
        does not reorganize the Core Spine section or require a new route before
        owner ratification.
    - path: orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
      reason: >
        The foundation preserves that boundary note's ownership split and does
        not amend the Data Capture / ECR / Cleaning / Judgment layer contract.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading already points capture/projection activity at the
        Projection Doctrine and boundary sources; adding this draft does not
        change read-pack policy.
  stale_language_search: >
    rg -n "Open Owner Decisions|OD-4.*effects|dedupe/clustering effects|where dedupe/clustering lives"
    orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    docs/prompts/handoffs/cleaning_spine_projection_doctrine_handoff_prompt_v0.md
  stale_language_search_result: >
    Re-run after the owner-direction patch. Remaining hits are expected
    references to the installed OD-4 direction and this receipt's query text; no
    checked surface should keep an "Open Owner Decisions" section for OD-1/OD-4/
    OD-7 or the narrower "OD-4 / dedupe and clustering effects" heading.
  non_claims:
    - not validation
    - not readiness
    - not owner ratification
    - not source-of-truth promotion
    - not implementation authorization
```
