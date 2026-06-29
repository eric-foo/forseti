# Core Spine v0 Data Lake Medallion Gold-Readiness Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Medallion-semantics and gold-readiness contract for Orca's Data Lake:
  bronze/silver/pre-gold/gold layer meanings, Spike Alert vocabulary,
  source-object movement as the first precomputed candidate class, and
  on-demand non-dossier actor timing retrieval for decision integrity.
use_when:
  - Deciding whether a Data Lake, Cleaning, ECR/SCR, or Judgment change leaks gold semantics into a non-Judgment layer.
  - Scoping Spike Alert or Movement Alert candidate records.
  - Checking whether commenter/reviewer timing retrieval remains decision-bounded and non-dossier.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
downstream_consumers:
  - data lake physicality lane
  - spike alert candidate-record lane
  - gold-ready evidence assembly lane
  - ECR/SCR source-side derived-record lanes
  - Cleaning spine foundation lane
  - Judgment spine lanes
stale_if:
  - Judgment ownership of credibility, salience, exclusion, Signal Integrity, Signal Use, Decision Strength, or Action Ceiling changes.
  - Data Lake derived-record or physical storage ownership changes.
  - The owner authorizes persistent actor profiles, cross-platform identity resolution, or person-dossier behavior.
  - The Spike Alert or actor timing retrieval direction is superseded.
authority_boundary: retrieval_only
```

## Status

`TARGET_MEDALLION_GOLD_READINESS_CONTRACT_RECORDED_V0`.

This is an architecture contract. It is not implementation authority,
validation, readiness, backend selection, physical storage selection, queue
design, schema finalization, or Judgment run authorization.

Owner direction recorded 2026-06-21:

- `Spike Alert` is acceptable user-facing vocabulary.
- The strict meaning is "outside usual range" / "usual-range threshold crossed."
- The first precomputed candidate class is source-object movement.
- Actor/commenter/reviewer timing retrieval is valuable for decision integrity
  and astroturfing inspection, but must remain on-demand, event-centric,
  exact-identifier scoped, and non-dossier.
- Candidate records do not claim botting, fake review, paid activity,
  coordination, manipulation, virality, credibility effect, exclusion, Signal
  Integrity, Signal Use, Decision Strength, or Action Ceiling.

## Purpose

This contract locks the non-physical Data Lake Medallion Semantics lane so later
architecture, scoping, prompt, or fused work cannot invent where gold begins.

The central rule:

```text
Gold does not leak out of Judgment.
Everything before Judgment may be bronze, silver, pre-gold, or gold-ready.
Only Judgment writes gold interpretation.
```

## Medallion Map

| Layer | Orca meaning | Owned by | Must not become |
| --- | --- | --- | --- |
| Bronze | Raw `SourceCapturePacket` bundles, preserved files, packet/slice/file handles, hashes, and source-visible attachment material. | Source Capture and Data Lake. | Cleaned truth, entity identity, salience, or Judgment input by shortcut. |
| Silver | Projection rows/receipts, ECR integrity records, SCR content records, Cleaning ledgers/views, and mechanical derived features over raw. | Projection, ECR/SCR, Cleaning, or a future mechanical derivation owner. | Credibility, bot/fake/paid labels, source value, Signal Integrity, or action meaning. |
| Pre-gold | Mechanical candidate records such as Spike Alerts or Movement Alerts. | Future designated mechanical derivation owner; stored as append-only derived records. | Gold, Judgment, or proof that the movement is viral, artificial, coordinated, paid, credible, or not credible. |
| Gold-ready | Decision-bounded evidence assemblies and receipts that gather raw/silver/pre-gold evidence for a specific question. | Future assembly owner; Judgment consumes by reference. | Final verdict, credibility call, exclusion, Signal Use, Decision Strength, or Action Ceiling. |
| Gold | Judgment-owned interpretation and decision-use output. | Judgment. | Data Lake, Cleaning, ECR/SCR, or precompute output. |

Do not collapse these into generic bronze/silver/gold storage tiers. In Orca,
the layer name is an epistemic boundary first and a storage convenience second.

## Public-Reaction Engagement Placement

Public-reaction engagement follows the same epistemic boundary:

- **Bronze:** source-visible raw facts such as upvotes, helpful votes, likes,
  views, shares, comment counts, reply counts, score state, visible sort/rank,
  metric posture, and source-exposed missingness in raw packets or attachment
  material.
- **Silver:** Projection rows, ECR/SCR records, Cleaning ledgers/views, or
  mechanical `engagement_context` records that normalize, preserve, summarize,
  or group those raw facts without deciding meaning. Silver may preserve
  source-visible resonance qualifiers such as direction, visible audience-fit
  basis, baseline context, and discount reasons, but not their Judgment effect.
- **Pre-gold:** mechanical candidate alerts only, such as an outside-usual-range
  engagement movement, resonance-context candidate, or Spike/Movement Alert,
  still with explicit non-claims.
- **Gold-ready:** a decision-bounded evidence assembly that gathers raw,
  Silver, and any Pre-gold engagement evidence for a specific Judgment question
  with `judgment_status: not_evaluated` or equivalent.
- **Gold:** Judgment-owned interpretation of what the engagement means for
  resonance weight, credibility, independence, Signal Integrity, Signal Use,
  Decision Strength, Action Ceiling, demand support, or exclusion.

## Spike Alert Contract

Use this vocabulary:

- User-facing: `Spike Alert`.
- Broader user-facing when needed: `Movement Alert`.
- Strict internal meaning: `usual-range threshold crossed`.

`Spike Alert` means:

```text
This source object moved outside its declared usual range under a declared
profile, baseline, window, cohort, and threshold.
```

It does not mean:

- viral;
- suspicious;
- bot-like;
- fake;
- paid;
- coordinated;
- manipulated;
- artificially amplified;
- credible or not credible;
- should be excluded or discounted.

The first precomputed candidate class is **source-object movement**. Source
objects include a video, post, product page, review thread, comment thread,
retail page, or other bounded public source object. This is intentionally not
an actor/person profile.

Minimum candidate-record contract for later scoping:

- raw anchors: packet/slice/file refs, hashes, and hash basis;
- source object key and source family/surface;
- observation window and baseline window;
- profile/version that defines "usual range";
- observed value, threshold, and threshold result;
- cohort/version when comparison uses a cohort;
- coverage limits, residuals, missingness, and raw-pull flags;
- explicit non-claims.

Field names and physical representation remain deferred.

## Actor Timing Retrieval Contract

Actor/commenter/reviewer timing retrieval is allowed only as on-demand
decision-integrity evidence assembly.

Allowed question shape:

```text
Given this observed public identifier on this source surface, within this
decision question, source family, and time window, show event-level timing,
cadence, exact repetition, and comparable source-object occurrences.
```

Allowed identifier shape:

```text
source family + source surface namespace + identifier kind + exact observed
public identifier + observation time
```

That key means "the exact public identifier observed in this namespace." It
does not mean person, canonical identity, platform-spanning identity, household,
account owner, employment identity, legal identity, or targetable lead.

Allowed outputs:

- event rows;
- source-object groupings;
- visible timing and capture timing;
- mechanically defined latency;
- cadence windows;
- exact duplicate or exact repeated-text membership;
- raw/projection/ECR/SCR/Cleaning refs;
- coverage limits, residuals, omissions, and raw-pull flags.

Rejected outputs:

- persistent all-history actor profile;
- unrestricted "show everything this person did";
- cross-platform identity merge;
- actor risk score;
- bot/fake/paid/coordinated/manipulation label;
- credibility or exclusion recommendation;
- adverse-action or outreach surface.

This preserves the decision-integrity value of timing evidence for astroturfing
inspection without building a person dossier.

## Gold-Ready Assembly Contract

Gold-ready assembly may gather evidence for a bounded question, but it remains
pre-Judgment.

A future `GoldReadyEvidenceView` or equivalent view may contain:

- the bounded decision question class;
- source families and source surfaces allowed by the selected profile;
- supplied source object or exact namespace-scoped identifier;
- time window and comparison cohort;
- raw anchors and derived-record refs;
- Spike Alert / Movement Alert candidate refs when relevant;
- mechanical timing, cadence, count, and exact repetition features;
- residuals, omissions, missing fields, and raw-pull flags;
- `judgment_status: not_evaluated` or equivalent non-Judgment marker.

Each invocation should leave an append-only assembly receipt keyed to raw and
derived refs. The receipt explains what was retrieved and which profile/version
was used. It does not decide meaning.

## Hard Boundaries

1. Data Lake owns raw preservation, by-key findability, attachment references,
   passive availability, and logical derived attachment points. It does not own
   medallion interpretation.
2. Projection, ECR/SCR, Cleaning, and mechanical derivation may produce silver
   or pre-gold records only when the record is traceable, append-only, and
   non-Judgment.
3. Cleaning may preserve exact mechanical duplicate/timing/context evidence, but
   it must not decide independence, credibility, artificial amplification,
   botting, copying intent, exclusion, or demand support.
4. Judgment alone owns gold interpretation: credibility, salience, exclusion,
   Signal Integrity, Signal Use, Decision Strength, and Action Ceiling.
5. Physical storage, backend, manifest version, queue, cache, scheduler,
   persistence, and migration remain outside this contract.

## Acceptance Criteria

This contract is satisfied when a later lane can rely on these conditions
without reopening intent:

1. Any non-Judgment alert uses `Spike Alert`, `Movement Alert`, or strict
   "usual-range threshold crossed" wording, not viral/suspicious/bot/fake/paid
   language.
2. The first precomputed candidate class is source-object movement, not
   actor/person scoring.
3. Actor timing retrieval is on-demand, exact namespace-scoped, event-centric,
   bounded by decision question/source family/time window, and non-dossier.
4. Gold-ready evidence views and receipts are clearly marked pre-Judgment and
   carry `judgment_status: not_evaluated` or equivalent non-claim.
5. All candidate, timing, and assembly outputs are append-only derived records
   or receipts keyed to raw, with residuals and raw-pull flags.
6. No field, label, or output from this lane claims botting, fake review, paid
   activity, coordination, manipulation, virality, credibility effect,
   exclusion, Signal Integrity, Signal Use, Decision Strength, or Action
   Ceiling.
7. No backend, physical store, queue, scheduler, runtime, cache, or migration is
   selected by this contract.

## Downstream Handoff

Implementation scoping may rely on the medallion semantics above, but only for
documentation/spec or narrow record-contract work. It may not scope backend,
queue, scheduler, runtime, persistent storage, actor profiles, or Judgment
evaluation from this contract.

Before source-changing implementation of Spike Alert records, the following
remain owner or lane blockers:

- physical home and write boundary for derived records and assembly receipts;
- mechanical derivation owner for Spike Alert / Movement Alert candidate
  records;
- profile/version contract for usual-range baselines, windows, cohorts, and
  thresholds;
- allowed source-family identifier scopes for actor timing retrieval;
- access/audit/retention guardrails for actor-related on-demand retrieval.

## Visible Limitations

This mini-god-tier shape intentionally gives up:

- precomputed gold;
- persistent reusable gold views before query shapes stabilize;
- persistent actor histories;
- cross-platform identity resolution;
- near-match, semantic, or intent clustering by default;
- bot/fake/paid/coordinated labels outside Judgment;
- storage/backend/queue/runtime selection;
- validation/readiness/production-fitness claims.

The payoff is high-value decision-integrity retrieval with low lock-in: Orca
can flag source-object movement and assemble bounded evidence without turning
the lake into Judgment or a dossier system.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Medallion Gold-Readiness Contract v0 locks the non-physical
    medallion semantics lane: Bronze is raw capture; Silver is projection,
    ECR/SCR, Cleaning, and mechanical derived features; Pre-gold is mechanical
    Spike/Movement Alerts; Gold-ready is decision-bounded evidence assembly;
    Gold remains Judgment-only, while actor timing retrieval is allowed only as
    on-demand exact-identifier event evidence and not as a dossier.
  trigger: architecture_doctrine
  related_triggers:
    - product_doctrine
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - orca/product/spines/data_lake/README.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - docs/workflows/ecr_spine_submap_v0.md
    - docs/decisions/data_capture_spine_deleted_comment_signal_retrieval_scoped_doctrine_decision_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
      reason: >
        The core contract already owns lake/store boundaries and excludes
        Judgment, Cleaning, ECR/SCR semantics, physical storage, and queue
        design. This additive contract owns medallion/gold-readiness semantics
        without reopening the core boundary.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        The storage contract remains the non-selecting physicalization blocker
        owner. This contract references derived records and receipts logically
        but does not choose their physical home.
    - path: orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
      reason: >
        The mechanics map remains the raw-to-derived flow map. This contract
        adds medallion/gold-readiness semantics without changing the flow.
    - path: orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
      reason: >
        Cleaning already forbids credibility, independence, botting,
        artificial-amplification, exclusion, and Decision Strength effects.
        This contract consumes that boundary for the Data Lake medallion lane.
  stale_language_search: >
    rg -n "Spike Alert|Movement Alert|GoldReady|gold-ready|pre-gold|usual-range|person dossier|dossier|bot-like|fake review|paid activity|coordination|virality"
    orca/product/spines/data_lake docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-06-21 after edits. Hits were confined to this contract and
    the Data Lake README pointer text. No searched live data-lake source uses
    Spike Alert as Judgment, gold-ready as gold, or actor timing retrieval as
    persistent actor profiling.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not backend selection
    - not physical storage selection
    - not queue/runtime design
    - not Judgment run authorization
    - not person-dossier authorization
```
