# Orca Data Lake MGT Precomputed Gold And Decision-Integrity Retrievability Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (deep-thinking / external architecture reasoning)
scope: >
  Paste-ready prompt for a no-repo ChatGPT Pro architecture pass on Orca Data
  Lake MGT: precomputed gold candidates, on-demand gold, decision-integrity
  retrievability, traceability, and scalability boundaries.
use_when:
  - Asking an external model with no repo access to reason about Data Lake MGT gold and retrievability.
  - Stress-testing precomputed alert records versus on-demand gold assembly.
  - Checking decision-integrity retrieval without turning the lake into Judgment or a person-dossier product.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
stale_if:
  - Data Lake, ECR/SCR, Cleaning, Judgment, or person-dossier boundaries change.
  - A later owner decision selects physical storage, queue/runtime, or gold-view persistence.
```

```yaml
orca_prompt_preflight:
  output_mode: file-write + paste-ready-chat copy
  template_kind: deep-thinking
  edit_permission: docs-write
  target_files:
    - docs/prompts/deep-thinking/orca_data_lake_mgt_precomputed_gold_retrievability_prompt_v0.md
  workspace: C:\tmp\orca-data-lake-mgt-target
  branch: codex/data-lake-mgt-target
  dirty_state: clean before prompt authoring
  reviews: none bound; this is a prompt artifact for external reasoning
  doctrine_change: none; prompt only
  destinations:
    prompt_artifact_path: docs/prompts/deep-thinking/orca_data_lake_mgt_precomputed_gold_retrievability_prompt_v0.md
    downstream_output: chat-only response from ChatGPT Pro
```

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: >
    Establish a thread-local capability target for Orca Data Lake MGT that
    links bronze/silver/gold, admission, tags, lineage, passive availability,
    and visible limitations without selecting implementation.
  output_fit_check: >
    The next produced answer or artifact must clarify precomputed gold
    candidates, on-demand gold, traceability, retrievability, and scalability
    limits without selecting backend, queue, scheduler, or runtime work.
  drift_guard: >
    Do not convert the MGT goal into implementation planning, backend choice,
    queue design, person-dossier design, or artifact completion as a proxy for
    capability fit.
  conflict_behavior: call_out_conflict_before_proceeding
```

## Paste-Ready Prompt

You are ChatGPT Pro. This is a no-repo source-capsule architecture reasoning pass for Orca. Do not claim source readiness beyond this capsule. Do not invent implementation facts. Do not recommend backend, queue, scheduler, scraper, crawler, dashboard, or runtime work unless clearly labeled as deferred and outside the current authorization.

## Objective

The owner wants Orca's Data Lake to become "mini-god-tier" as an owner-invoked capability target: very high practical capability with visible limitations, low lock-in, and no implied validation/readiness claim. The current architecture discussion is about whether Orca should support:

1. Precomputed "gold" or gold-adjacent signals, such as a creator video spiking abnormally and being flagged for attention.
2. On-demand gold retrieval for decision integrity, such as:
   - "I noticed this commenter on an influencer is unusually fast. Are they commenting on other creators with similar speed?"
   - "Could this public reviewer or commenter pattern appear across other products, creators, or surfaces in a way that should be inspected?"
   - "Can Orca retrieve comparable public-signal evidence without deciding that someone is a paid bot, fake reviewer, or manipulation actor?"

Answer as an architecture reasoning pass. The goal is a decision frame and target shape, not implementation.

## Source Capsule

Use only this source capsule as the repo context.

### Mini-God-Tier Lens

"Mini-god-tier" means an owner-invoked capability target, not a claim tier. It should maximize useful capability while naming every important limitation. It does not prove validation, readiness, quality, or production fitness. It cannot be used by an agent to expand scope on its own.

### Data Lake Core Contract

The Data Lake owns raw packet preservation, stable handles, hashes, manifests/reference rules, by-key findability, source-family attachment rules at the lake boundary, logical attachment points, and content-free availability facts.

The Data Lake must not clean, normalize, identify, decide source value, run downstream lanes, own ECR, SCR, Cleaning, Judgment, canonical identity, cross-packet dedupe, downstream scheduling, retry, direct calls, queue behavior, or runtime orchestration.

By-key discovery is authority. Event/queue systems may later optimize discovery, but cannot become the source of truth. Downstream derived records attach append-only and keyed to raw handles. Raw records are not mutated.

Projection owns legible rows. Cleaning owns mechanical transforms. Judgment owns interpretation, credibility, salience, exclusion, Signal Integrity, Signal Use, Decision Strength, and Action Ceiling.

Current physicalization gate: storage engine, Manifest v2, Attachment Record serialization, sidecars, projection cache, queue/runtime, ECR/SCR/Cleaning/Judgment schemas, and validation/readiness are not selected.

### Data Lake Storage Contract

The storage contract defines five dumb record kinds:

1. Raw Packet Store: preserved packets, stable handles, hashes, hash basis.
2. Attachment Record: references and attachment metadata.
3. Availability Index: committed/readable facts by stable keys only. It is not a bus, scheduler, router, retry tracker, priority system, or success tracker.
4. Derived Result Store: append-only lane-owned derived records keyed to raw, including projection receipts, ECR integrity records, SCR content records, Cleaning ledgers, and Judgment outputs.
5. Acknowledgement Log: append-only lane-owned acknowledgement facts. It is not lake-consumed control flow.

Physical choices remain deferred.

### Data Lake Mechanics Map

The raw SourceCapturePacket is canonical. Source Capture writes raw packet truth. Everything downstream reads raw by key. Everything downstream writes a derived view, receipt, record, or ledger. Nothing downstream replaces raw.

Shared handles include packet_id, slice_id, preserved file refs, sha256/hash basis, and sibling derived refs only as refs.

Hard rules:

- Reference never merge.
- Re-derive never migrate.
- Carry supplied facts or residualize.
- Absence is posture.
- One derived record per epistemic kind.
- Projection and Cleaning are mechanics only.
- Judgment owns credibility, salience, exclusion, Signal Integrity, Signal Use, Decision Strength, and Action Ceiling.
- Storage, manifest/cache/runtime schema, and queue behavior are not selected.

### ECR/SCR Boundary

ECR/SCR are retrieval and derived-record layers over captured source slices, not lake authority and not Judgment.

Three stacked layers over a captured source slice:

1. Provenance: capture happened and how to trust the bytes.
2. Integrity: ECR postures such as source-page or source-friction integrity records.
3. Content: Signal Content Record.

Cross-kind invariants include reference-never-merge, one derived record per epistemic kind, carry-supplied-or-residualize, and never authoring facts from prose. The conductor or Judgment lane owns evaluation.

### Cleaning Boundary

Cleaning turns preserved public-source material into smaller traceable Judgment-usable working material via non-destructive transformations over raw/projection/ECR receipt material.

Cleaning exists to make later review inspectable, not to decide meaning. Raw is canonical. Projection and Cleaning are working views.

Allowed Cleaning transform classes include normalization, translation, summarization, exact-identity dedupe mechanics, candidate/deferred clustering mechanics, receipt/ledger propagation, residualization, and raw-pull escalation. Every output must preserve or link raw anchor, projection anchor, source identity/family, timing, hierarchy, counts, cluster/duplicate membership, omissions/residuals/warnings, and layer-owner blockers.

Cleaning must not remove rows because they seem low-value, repetitive, suspicious, bot-like, or inconvenient. Cleaning must not decide independent corroboration, artificial amplification, botting, copied/coordinated intent, credibility/integrity effect, whether duplicates support demand, or whether a cluster raises or lowers decision strength.

Core v0 may code-enforce exact-identity dedupe mechanics only. Near-match, copying, and semantic clustering are deferred unless separately authorized.

### Safety And Person-Dossier Boundary

Orca must not become a person-level dossier product, data broker, fake-review or botting tool, manipulation system, or deceptive competitive-tactics system.

Allowed target: scoped retrieval of public-signal patterns for decision integrity, where the output is bounded to a decision question, source family, observed handle or public source-surface identifier, time window, and traceable evidence.

Forbidden drift: canonical person identity, private/auth-gated/DM data, person dossiers, generalized surveillance, harassment workflows, claims that someone is a paid bot or fake reviewer, or automated adverse-action conclusions.

## User Scenario To Analyze

The owner is considering two related capabilities:

1. Precompute abnormal public-signal movement:
   - Example: a creator video spikes abnormally, maybe viral.
   - Orca flags it for attention.
   - The owner wants this available without waiting for a bespoke query every time.

2. On-demand decision-integrity retrieval:
   - Example: a commenter appears unusually fast under an influencer's post or video.
   - The owner asks whether the same observed public handle or scoped source-surface identifier comments on other creators with similar speed.
   - Example: a reviewer on a retail surface has a suspicious-seeming pattern, and the owner asks whether similar public-source timing or repetition appears across other products or source surfaces.
   - The purpose is decision integrity: "show me comparable public evidence and mechanical patterns so Judgment can decide how much to trust this signal."
   - The Data Lake, ECR, SCR, and Cleaning must not conclude "paid bot," "fake reviewer," "coordinated manipulation," or credibility impact.

## Questions To Answer

1. Should Orca precompute "gold," or should it precompute only gold-candidate alert records and assemble true gold on demand? Give a clear recommendation.
2. If precomputed gold-candidate records are allowed, what exactly should they contain? Include fields, required keys, lineage, thresholds, profile/version refs, residuals, raw-pull flags, and explicit non-claims.
3. What should remain on-demand? Define a Gold Assembly Profile and Gold View Receipt that can assemble a decision-specific view without mutating raw or pretending to be Judgment.
4. What indexes or retrievable keys does the lake need to make the commenter/reviewer scenario possible? Consider packet_id, slice_id, file refs, source family, creator/product/source surface, observed public handle or scoped actor key, comment/review/event ID, timestamp, capture timestamp, event latency, cadence windows, exact duplicate membership, and comparison cohort.
5. How can the architecture support "same observed handle across creators/products" without becoming a canonical identity graph or person dossier?
6. Where do ECR/SCR and Cleaning fit in the bronze/silver/gold model? Is ECR/Cleaning basically silver, with Judgment-owned assembled views as gold?
7. Which derived features are safe as mechanical silver or pre-gold candidates, and which must be deferred to Judgment? Be explicit about botting, paid-review suspicion, artificial amplification, and credibility effects.
8. What should be materialized early versus deferred until tags, lineage, and query shapes are stable?
9. How should traceability, retrievability, and scalability be ordered? The owner thinks scalability should come last because scaling a poor architecture is bad. Evaluate that.
10. What owner decisions or blockers must be settled before implementation, including admission criteria, keyed storage/addressing, profile definitions, allowed identifiers, and person-dossier guardrails?

## Required Output Format

Return these sections:

1. Architecture Read
2. Recommendation
3. Precomputed Candidate Records
4. On-Demand Gold Assembly
5. Retrieval Model For Commenter/Reviewer Integrity Questions
6. Bronze/Silver/Gold Mapping
7. Safety And Person-Dossier Guard
8. Scalability Last, But Not Forgotten
9. Owner Decisions Before Implementation
10. Visible Limitations

Use the labels `recommended`, `viable-but-risky`, `reject`, `deferred`, and `source-gap` where useful.

Do not write code. Do not choose a backend. Do not authorize queue/runtime work. Do not claim validation, readiness, or production fitness.
