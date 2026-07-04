# Core Spine v0 — Signal Content Record Architecture Direction v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture direction brief
scope: Owner-decided DIRECTION for the wedge-agnostic Signal Content Record — now deprecated/dormant as a default standalone pre-Judgment layer, retained as a compatibility/future-revival contract over the existing provenance (SourceCapturePacket) and integrity (ECR postures) layers. Locks direction + invariants + shape, not the field-by-field schema.
use_when:
  - Scoping or reviewing the deprecated/dormant signal-content contract of the Data/Cleaning/ECR spine.
  - Checking what the bounded content-field ratification does and does not authorize.
  - Checking why current SCR v0 is not a default generated handoff layer before Judgment.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
  - orca-harness/ecr/__init__.py
stale_if:
  - The owner settles the final Evidence Candidate Record / Evidence Unit (EvidenceUnit) field architecture (currently reserved).
  - The carrier, lifecycle, decision_relevance posture, deprecation/dormancy, revival, or deletion posture below is changed by a later owner decision.
  - The IPF Evidence Unit Standard content vocabulary changes.
```

## Status

`OWNER_DECIDED_DIRECTION` — recorded 2026-06-09. Bounded content-field ratification GRANTED.

`DEPRECATED_AS_STANDALONE_PRE_JUDGMENT_LAYER` — amended by current owner direction. The original SCR contract remains as retained compatibility/future-revival surface, but current v0 SCR must not be treated as a default generated layer between an evidence pack and Judgment.

This is **not** the final Evidence Unit field architecture (owner-reserved), **not** a schema, **not** code, and **not** a JSG-01 unfreeze (the gate stays FROZEN). It is a direction record + a bounded authorization, for owner sign-off and later commit.

## Current Demotion

Current owner decision: **deprecate and demote SCR as a standalone pre-Judgment artifact; do not delete it yet.**

Default route:

```text
Evidence pack -> Judgment-authored signal interpretation
```

Cleaning may prepare traceable working views, transformations, summaries, translations, dedupe mechanics, warnings, residuals, and raw-pull triggers. Cleaning must not secretly decide signal meaning, graded relevance, Signal Use, Decision Strength, or Action Ceiling.

SCR remains available only as:

- a retained compatibility contract for existing docs/code/tests/imports;
- a historical boundary showing why a deriver must carry or residualize and must not author from prose;
- a possible future revival surface if Orca needs a frozen reusable source-side content object shared across multiple Judgment runs.

Deletion condition: delete SCR only after no active docs/code/tests/runners consume it and Judgment's evidence-pack path has cleanly replaced it. If a future rich SCR becomes worth feeding whole into Judgment, that is a revival case, not a deletion trigger.

## What this locks

Historically, this locked the wedge-agnostic **Signal Content Record** — the structured *"what a signal says"* layer. That contract is now retained as a deprecated/dormant compatibility surface, not as a default pre-Judgment handoff. The current product route is that Judgment determines the signal interpretation from the evidence pack; SCR is revived only if a separately accepted need appears for a frozen reusable source-side content object.

## Owner decisions (settled 2026-06-09)

1. **Carrier — option (b), durable, now dormant for default routing.** A parallel derived `SignalContentRecord`, keyed to the `SourceCapturePacket` (CapturePacket), composed by the Evidence Unit (EvidenceUnit) **by reference** — the **second derived-record kind** after the ECR integrity postures. This carrier is retained for compatibility and possible revival, but current default Judgment routing does not require SCR generation.
2. **Lifecycle — derived / re-derivable.** An M2-style derived-read, **not** persisted-at-capture, so a future family-taxonomy change is a *re-derive from the still-frozen raw observable*, never a stored-column migration.
3. **`decision_relevance` — a neutral mechanical routing tag only.** Shape-derived (`decide_candidate` / `confirm_only` / `context_only` / `unresolved`). The graded Signal Use Classification / Decision Strength / Action Ceiling stay Judgment-owned (verified boundary doc:77).
4. **Authority — bounded content-field ratification GRANTED.** The content analogue of the SP-1/2/3/6 source-side *integrity* exception. It does **not** settle the final Evidence Unit field architecture (reserved — verified boundary doc:131-133, 253-254) and does **not** unfreeze JSG-01 (the gate stays FROZEN; the source-side fields were ratified, the gate was not — boundary doc:289, ecr `__init__`.py:26).

## Boundary invariants (load-bearing)

- **Downward (content ↔ integrity):** the record **references** provenance (`packet_id` / `slice_id`) and integrity (ECR postures SP-1/2/3/6) by key; it never embeds, copies, or merges them. One-directional: content → provenance, never the reverse. Content = "what's said"; integrity = "can I trust the saying" — **linked, never collapsed.**
- **Upward (single-row ↔ aggregate):** one record = one observed event/claim from one source slice. Any cross-source aggregate (price-sensitivity curve, sentiment trend, "switching is accelerating") is **derived and Judgment-owned**, never a field on the record (grounded in Judgment's ownership of Signal Use Classification + the Inclusion State Rule — boundary doc:77, :158).
- **Durable structural invariant:** **one derived record per epistemic kind, composed by the Evidence Unit (EvidenceUnit), never merged.** Future kinds (e.g. corroboration) follow the same shape rather than sprawling.

## The shape (direction, not the field-by-field schema)

- **Common spine (family-invariant):** `content_id` · `signal_family` (closed enum: the four content-row families + `RESIDUAL_FAMILY_UNRESOLVED`; signal-quality meta is not a content row — see Family 5 below) · `subject_entity` (who/what the signal is *about* — not the source) · `event_or_claim` (the observed substance, raw, pre-interpretation) · `signal_event_time` (by reference to `PacketTiming`, distinct from capture time and cutoff) · `decision_relevance` (the neutral tag, #3) · `raw_observation` (verbatim, source-language anchor).
- **Two optional generic sub-objects** (family richness lives in their *values*, no wedge-named columns): `delta` (`dimension·before·after·change_basis`) · `reaction` (`kind·direction·observed_magnitude_state·excerpt_ref`) — thin and local (only co-observed reaction; aggregate reaction is Judgment's).
- **Honesty surface:** reuse the existing `VisibleFact` known/unknown-with-reason pattern + the ECR `M3` named-residual discipline, so "no delta for this family" and "delta not captured" stay distinguishable.
- **Family / satellite:** family-specific fields ride a typed `family_detail` payload discriminated by `signal_family`; they promote to the common spine only under the existing two-non-overlapping-families rule.
- **Family 5 (signal-quality meta) is not a fifth record:** source-trust quality → ECR postures; content-completeness → the per-field `VisibleFact` status; decide-vs-confirm → the one spine tag; graded relevance → Judgment.
- **Downstream (additive):** the Evidence Unit keeps its ID/provenance shape and gains an optional `content_ref` (or `summary` backed by the record); `EvidenceUsed.evidence_unit_ids: list[str]` is **unchanged** (verified case_models.py:110,123) — the proof this is a non-breaking addition.

## Carry-don't-coin + evolution

- **Carry, don't coin:** structure the IPF Evidence Unit Standard content vocabulary (the IPF standard remains the source to cite — boundary doc:132); reuse `VisibleFact`; **reference** packet/ECR ids rather than restating them. Same `M1`-carry / `M2`-derive / `M3`-residual discipline the ECR derivers use.
- **Evolution:** inherit the adopted capture-packet schema-evolution doctrine verbatim — read-checked `_vN`, bump-on-breaking, **additive family-enum growth**, lenient-read / strict-admit, no upgrade-on-load, and **re-derive-not-migrate** (the derived lifecycle from #2 is what makes re-derive safe).

## Placement (filesystem)

Follow the ECR convention: derived-record **code** as a sibling module beside `orca-harness/ecr/` (it is the same kind of thing); the **contract** doc in `docs/product/` (this file), referencing the IPF standard rather than restating it.

## Deferred — NOT authorized here

- Default SCR generation before Judgment is no longer the route; the current default is evidence pack -> Judgment-authored signal interpretation.

- The field-by-field schema (an ADR / implementation slice), routed to the **ECR-consolidation lane** as the next derived-record kind after SP-6, using the `M1`/`M2`/`M3` binding rule.
- The interpretive extraction step (raw text → `signal_family` + event-core): like SP-5's deferred finalizer, it likely needs a provenance-bound **authored** input, residualized when absent — never invent family or content.
- Persistence/finalizer, any packet→`EvidenceUnit` binding, Cleaning, Judgment, commits/pushes — each separately gated (boundary doc / `safety-rules.md`), unchanged.
- Emit-timing: the record is produced **after** a candidate is promoted and a `SourceCapturePacket` exists — **not** from the Reddit candidate-intake discovery rows (those are pure discovery, upstream of capture).

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca core spine gains a second derived-record kind — a wedge-agnostic Signal
    Content Record (parallel, packet-keyed, composed-by-reference, never merged),
    derived/re-derivable, carrying a neutral decide-vs-confirm routing tag — under
    a bounded content-field ratification that does NOT settle the reserved final
    Evidence Unit field architecture and does NOT unfreeze JSG-01.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  status: DRAFT_PENDING_OWNER_SIGNOFF_AND_COMMIT
  controlling_sources_updated:
    - docs/product/core_spine_v0_signal_content_record_architecture_v0.md
  downstream_surfaces_to_check_on_finalize:
    - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - docs/product/core_spine_v0_information_production_foundation_v0.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  intentionally_not_updated:
    - path: orca-harness/ecr/
      reason: "No code; this is a direction record. The field-by-field schema is a separately-routed ECR-consolidation slice."
  non_claims:
    - not the final Evidence Unit field architecture (owner-reserved)
    - not a JSG-01 unfreeze (stays FROZEN)
    - not a schema, not code, not validation, not readiness, not implementation authorization
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    SCR v0 is deprecated/dormant as a standalone pre-Judgment generated layer:
    the default route is evidence pack -> Judgment-authored signal interpretation;
    Cleaning may prepare traceable working views but must not decide signal meaning;
    SCR is retained only for compatibility/history or future explicit revival as a
    frozen reusable source-side content object.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
    - forseti/product/spines/ecr/signal_content/signal_content_record_deriver_architecture_plan_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  intentionally_not_updated:
    - path: orca-harness/signal_content/
      reason: >
        Code/tests/imports are retained for compatibility and historical validation.
        This patch changes routing/default-use doctrine only; deletion requires the
        separate no-active-consumer condition recorded above.
  stale_language_search: >
    rg -n "Build/review the SCR deriver|default SCR|SCR generation|first_build_slice|The v0 build this tees up|TARGET_RECOMMENDED|second derived-record kind|routes to the SCR direction|built Signal Content Record|default pre-Judgment|standalone pre-Judgment"
    .agents/workflow-overlay/source-loading.md docs/workflows/ecr_spine_submap_v0.md
    docs/workflows/orca_repo_map_v0.md forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
    forseti/product/spines/ecr/signal_content/signal_content_record_deriver_architecture_plan_v0.md
  stale_language_search_result: >
    Executed in the scr-deprecation worktree after edits. No active route surface
    keeps "Build/review the SCR deriver", "first_build_slice", "The v0 build this
    tees up", "routes to the SCR direction", or "built Signal Content Record".
    Remaining hits are intentional deprecation/default-route language, the older
    historical receipt recording the original second-derived-record decision, and
    deriver-plan TARGET_RECOMMENDED rows that are now paired with current demotion
    language or renamed TARGET_RECOMMENDED_HISTORICAL.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not deletion of SCR code/tests/docs
```

Older direction-change receipts, if any, are archived in `docs/decisions/dcp_receipts_archive_v0.md`.

## Non-Claims

Planning / direction only. **Not** the final Evidence Unit field architecture (owner-reserved). **Not** a JSG-01 unfreeze (FROZEN). **Not** a schema, not code, not validation, not readiness, not implementation authorization. Wedge-agnostic — no wedge is baked into core; all wedge-specific richness lives in satellite `family_detail` values. The trust boundary is preserved (content linked-not-merged to integrity), and the content↔judgment line is fixed as a neutral routing tag — surfaced, not silently drawn.
