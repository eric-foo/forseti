# Packing Spine + Silver Co-Production First Proving Slice — Implementation Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Commissions the first smallest-complete Packing Spine implementation, its
  explicit co-production boundary with Silver, and a TikTok creator-onboarding
  proving slice that turns preserved transcripts, comments, and engagement
  context into reversible Gold-ready evidence assemblies without leaking
  Judgment into Packing or Silver.
use_when:
  - Starting the first implementation lane for the Packing Spine.
  - Replacing transcript/comment bulk handoff with schema-bound, source-reversible evidence units.
  - Coordinating Packing requirements with Silver producers and read surfaces.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_company_intelligence_information_architecture_v0.md
  - docs/research/packing-phase/README.md
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
  - forseti-harness/evidence_binding/tiktok_audience_triangulation.py
branch_or_commit: origin/main at fc403fbd58866996caab6752c17d9280912cef4d when authored
downstream_consumers:
  - Fresh Packing Spine implementation task
  - Silver lane coordinating any required reusable fact or retrieval additions
  - Judgment and Creator Signal lanes consuming the first packed TikTok assembly
stale_if:
  - Packing ownership, the medallion Gold boundary, or final evidence-inclusion ownership changes.
  - The TikTok creator-audience evidence bundle or Silver prerequisite contracts materially change.
  - A Packing Spine implementation lands and supersedes this first-build commission.
```

This is the complete frozen implementation commission. Paste it verbatim into a
fresh implementation task. Do not reconstruct intent from the authoring chat.

## Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated inline.
prompt_behavior: docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md
template_kind: none
template_kind_reason: first-of-kind cross-spine implementation commission
output_mode: file-write
prompt_destination: docs/prompts/handoffs/packing_spine_silver_coproduction_first_proving_slice_handoff_v0.md
input_prompt_source: this frozen handoff artifact
edit_permission: implementation-authorized
workflow_sequence_policy: overlay_owned
workflow_sequence_source: explicit_user_instruction_plus_forseti_overlay
workflow_sequence_status: bound
repo_map_decision: loaded
repo_map_reason: >
  The targeted Silver/Vault route was used to bind the authoritative Silver
  goal, record, and consumption sources; broad repo-map loading is unnecessary.
receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  launch_checkout: receiver_to_observe
  effective_target_worktree: fresh receiving task worktree
  managed_starting_ref: origin/main
  required_revision: fc403fbd58866996caab6752c17d9280912cef4d
  revision_mode: ancestor
dirty_state_allowance: clean receiver worktree; no pre-existing target-file changes
untracked_files_in_scope: only files created by this commission after provenance is established
controlling_source_state: clean at authoring base; receiver must fresh-read and re-check
doctrine_change:
  expected: yes
  dimensions:
    - architecture_doctrine
    - workflow_authority
    - lifecycle_boundary
  closeout_requirement: direction_change_propagation receipt or blocker
```

The user will launch the fresh task. This artifact does not authorize the
current authoring task to create a managed receiver. The receiving task must
bind its own worktree before edits and must not use another active lane's dirty
worktree.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope: first Packing Spine core, Silver interface, TikTok proving adapter, tests, and proof receipt
  dirty_state_checked: required_on_receiver
  blocked_if_missing: >
    Stop if the receiver cannot establish an ancestor of the required revision,
    a clean non-concurrent target, the controlling medallion/Silver/Packing
    sources, or read access to the TikTok proving corpus or an honest fixture fallback.
```

## Execute Through `/fused`

Invoke `/fused` for this commission. REFERENCE-LOAD the fused lane instructions
and the project overlay before applying them. SOURCE-LOAD the bounded sources
below, declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, and only
then APPLY implementation scoping, spec writing, micro-decision locking, and
implementation in order.

Planning and scoping do not reduce the implementation authorization carried by
this commission. Stop at the first fused lane that does not clear.

The highest-value review checkpoint is
`after_all_steps_pre_closeout`. Treat independent delegated review as required
for the first cross-spine implementation because the Silver/Packing/Judgment
ownership boundary and the no-Gold-leak invariant are load-bearing. Do not call
the work unit complete until the review return is adjudicated and any accepted
closure is validated.

## Objective

Build the first smallest-complete Packing Spine and prove it on the existing
TikTok creator-onboarding / creator-audience corpus.

The spine must transform already captured and source-backed evidence into a
decision-bounded, Gold-ready assembly that Judgment can consume by reference.
It must eliminate the current need for Judgment code to perform
platform-adjacent normalized-text dedupe and compaction over an upstream
all-cues/all-comments bundle, without replacing the source with a generic prose
summary, losing the current multiplicity/member-lineage guarantees, or
pre-deciding the Judgment.

The first slice is complete only when:

1. a discoverable Packing Spine front door and owning architecture contract
   exist;
2. a reusable Packing runtime/schema core exists;
3. Silver and Packing ownership are mechanically and doctrinally separated;
4. the TikTok creator-audience path consumes the Packing core rather than a
   platform-specific bulk evidence bundle;
5. every packed semantic unit remains reversible to exact source context;
6. a real existing TikTok lake corpus is rehearsed read-only, or a loud typed
   access blocker is returned after fixture proof;
7. the existing Judgment and Creator Signal boundaries remain intact; and
8. validation plus required delegated review close without hiding residuals.

## Owner Direction

### Do not summarize transcripts away

The full transcript is a preserved source object. It remains retrievable through
Bronze/raw or another honest source-preservation reference. Packing must never
replace it with a prose paragraph that becomes the only durable evidence.

The useful derived object is not “the transcript summary.” It is a set of
schema-bound, atomic, source-grounded evidence units plus relationships and a
case-specific assembly.

Human-readable summaries may exist only as derived renderings over those units.
They must never be the sole evidence, silently discard support, or prevent a
consumer from reopening the exact quote and surrounding context.

### Correct medallion language

- Full captured transcript/comment bytes and source-visible metrics are Bronze.
- Reusable source-backed facts in the official envelope are Silver Authority.
- Generated Silver views are retrieval surfaces, not new authority.
- Packing emits decision-bounded Gold-ready assemblies with
  `judgment_status: not_evaluated`.
- Only Judgment emits Gold interpretation.

Audit any current TikTok artifact or lane colloquially called “Gold.” Do not
preserve a false Gold label merely because it is the richest current dataset.

### Smallest-complete evidence, not numeric completion

No numeric source, transcript, cue, comment, evidence-unit, venue, or packet
target establishes Packing completeness. Counts may describe the corpus or
search/processing hygiene only.

A packed item earns inclusion when it performs a named decision-material job
and is not substitutable by an equal-or-better included item. Packing closes a
draft assembly only when every material requirement is answered,
contradicted, held as a typed gap, or lacks a remaining non-dominated available
input path worth its marginal burden.

Packing must not reopen CSB/Scanning acquisition after an accepted acquisition
closure merely because more material might exist. It may emit a typed upstream
gap when an input promised by the closure is missing, stale, corrupt, or not
inspectable.

## Bound Source Pack

Read project authority first: `AGENTS.md`,
`.agents/workflow-overlay/README.md`, and the targeted owner sections routed
from the overlay for source loading, decision routing, source of truth,
validation, safety, review, and prompt orchestration.

Use this task pack:

### Full task-source reads

1. `docs/decisions/forseti_company_intelligence_information_architecture_v0.md`
   — merged smallest-complete acquisition and lake-first contract.
2. `docs/research/packing-phase/README.md`
   — current Packing boundary and non-ownership.
3. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
   — Bronze/Silver/Gold-ready/Gold authority.
4. `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md`
   — live TikTok/Instagram evidence-to-Judgment and presentation boundary.

### Targeted section reads

1. `docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v3.md`
   — adjudicated target architecture, Packing outputs, visibility boundary,
   block states, and intentionally undecided items.
2. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
   — Silver Authority versus retrieval, record kinds, lineage, append-only
   semantics, explicit missingness, and no-Gold boundary.
3. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
   — canonical root, physicality, location, and access semantics for the
   read-only proving rehearsal.
4. `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`
   — by-reference consumption, acknowledgements, and rebuildable reads.
5. `forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md`
   plus the source/transcript boundary in `tiktok_capture_lane_spec_v0.md`.
6. `forseti-harness/evidence_binding/tiktok_audience_triangulation.py` and
   `forseti-harness/judgment/creator_audience.py`
   — current all-cues/all-comments assembly and receipt behavior; compact-view
   v3 normalized-text grouping, multiplicity, member-lineage expansion; and the
   tactical Judgment-side compaction seam that Packing must absorb without
   regression.
7. `forseti-harness/schemas/tiktok_audience_evidence_models.py`,
   `forseti-harness/judgment/tiktok_audience_triangulation.py`, and
   `forseti-harness/runners/run_tiktok_creator_audience_triangulation.py`
   — current claim, validation, and runner seams.
8. `forseti-harness/cleaning/transcript_product_extractor.py` and
   `forseti-harness/cleaning/transcript_product_lake.py`
   — existing quote-grounded extraction, exact transcript lineage, rejection,
   and Silver write patterns. Reuse principles; do not blindly generalize a
   product-mention schema into all evidence.

Sources available but not loaded by default:

- historical Packing v0-v2 artifacts superseded by v3;
- e.l.f. backtest artifacts;
- unrelated creator-product/GTM surfaces;
- broad lake inventory dumps;
- all other source families.

Do not exceed the source pack merely because files are nearby. Add a source only
when it resolves a named implementation blocker, and record why.

## Architecture Boundary: Silver and Packing Work Together

Before implementation, produce an `interface_delta_matrix` in scoping. For
every required field or behavior, classify it:

| Class | Owner |
| --- | --- |
| Source-preserved bytes, source identity, timestamps, and source-visible metrics | Capture/Bronze |
| Reusable, source-backed, decision-neutral fact or relationship | Silver producer through the official envelope |
| Mechanical normalization, quote location, dedupe candidate, and transformation lineage | Cleaning/ECR or the owning Silver producer |
| Case-specific information job, candidate decision effect, evidence grouping, visibility, assembly, and typed gap | Packing |
| Evidentiary salience, credibility, independence effect, final inclusion/exclusion, claim ceiling, action meaning, and commercial conclusion | Judgment |

Rules:

- Packing consumes Silver by stable record/reference interfaces. It must not
  scrape generated views and copy them into a second authority.
- Silver must not gain `information_job`, case-specific materiality, action
  effect, claim ceiling, credibility, salience, or inclusion fields.
- Packing must not manufacture reusable source facts that should have been
  emitted by Silver.
- When a reusable source fact is missing, either implement the smallest
  upstream Silver addition in the same work unit or emit a typed
  `silver_gap_request`. Choose the same-work-unit route only when no active
  Silver writer overlaps the exact files and the scope can be fully validated.
- If a separate Silver lane is active on overlapping files, do not create
  concurrent writers. Complete non-blocked Packing work and return
  `SILVER_DEPENDENCY_BLOCKED` with the exact required record/view contract,
  target owner, evidence, and resume condition.
- Do not build a generic event bus, registry, warehouse, vector database,
  ontology expansion, or universal extraction framework.

## Required Evidence Representation

Exact schema names may be locked during fused scoping, but the behavior must
support these two layers.

### 1. Reusable source-grounded atom

This is decision-neutral and eligible for Silver only when the owning producer
can truthfully emit it through the Silver contract.

Required semantics:

- stable atom identity;
- source object and creator/platform identity;
- modality, such as transcript/content/comment;
- exact source span or pointer;
- short verbatim quote or source-bound text;
- source text hash and hash basis;
- surrounding-context locator;
- source-effective time, capture time, and cutoff posture;
- reusable semantic type, such as:
  - product or entity mention;
  - explicit claim;
  - comparison;
  - stated experience or outcome;
  - objection or problem;
  - question or uncertainty;
  - behavior or action;
  - description or attribute;
  - audience reaction;
- normalized entities and relationship refs where mechanically supported;
- duplicate, cross-post, repost, or derivative relationship refs;
- source-visible engagement context by reference;
- limitations and explicit missingness;
- producer, schema, policy, and lineage versions.

The atom records what the source says or shows. It does not record why the
current decision should care.

### 2. Packed evidence unit

This is case-specific and Gold-ready, never Silver Authority and never final
Judgment.

Required semantics:

- stable packed-unit identity and assembly identity;
- one or more source-grounded atom/raw refs;
- information requirement and named information job;
- candidate effect on action, action ceiling, rival assessment, or hold;
- case-local relation such as support, weakening, contradiction, context, or
  unresolved;
- support breadth: source objects, distinct videos/posts, creators when
  applicable, time spread, and modality;
- duplicate/derivative cluster and independence limitation;
- engagement-context refs and relative-engagement posture, without converting
  engagement into truth;
- cutoff status and leakage/visibility class;
- source-reversible context;
- limitation, uncertainty, and typed-gap links;
- Packing disposition such as candidate include, display representative,
  dominated with substitute, excluded out of scope, or held;
- `judgment_status: not_evaluated`;
- no final credibility, salience, evidence weight, inclusion/exclusion,
  Decision Strength, Action Ceiling, or commercial verdict.

Exact names are mutable. These ownership semantics are frozen.

## Transcript and Long-Form Content Policy

1. Preserve and address the complete transcript independently of Packing.
2. Do not pass the entire transcript to every downstream Judgment by default.
3. Do not reduce the transcript to one free-text summary.
4. Extract source-grounded candidate atoms with exact quote/span validation.
5. Reject or quarantine any model-produced atom whose pointer cannot be located
   in the source.
6. Keep enough surrounding context to prevent quote-fragment distortion.
7. Assemble only units that perform named information jobs for the current
   case.
8. Keep a complete omitted-item index with typed reasons so compact model
   context does not become invisible deletion.
9. A compact model view may use representatives, but every materially relied-on
   evidence ID and every contradiction/gap must remain recoverable.
10. Never let context-window limits silently become evidence-completeness rules.

Use LLMs only as candidate extractors or drafting aids behind deterministic
identity, pointer, schema, and rejection checks. A model sentence without exact
source support is not a packed evidence unit.

## Repetition, Agreement, Contradiction, and Engagement

- Additional same-direction evidence can materially strengthen the case. Do not
  drop it merely because earlier evidence points the same way.
- Same-direction units earn distinct support value when they broaden source
  objects, time, modality, creator/audience segment, relative-engagement
  distribution, recurrence, or support density.
- Exact duplicates, cross-posts, and reposts remain observable. Preserve their
  propagation and engagement facts, but relate them so they are not silently
  counted as independent origin corroboration.
- Multiple posts by one creator may be material evidence of recurrence or
  creator-specific pattern. Preserve creator clustering so Judgment can
  distinguish recurrence from independence.
- A weak contradictory item does not automatically receive equal standing with
  a large, strong same-direction distribution. Preserve a contradiction when it
  is decision-material, but leave its ultimate weight to Judgment.
- Relative engagement is a source-backed/mechanical context supplied by Silver.
  Packing may route and display it. Judgment decides what it means.
- A representative subset is a rendering convenience only. It must never
  replace the complete materially relied-on support set.

## Participant, Facilitator, and Sealing Boundary

Preserve the v3 Packing-to-Harness boundary:

- Packing constructs a draft participant packet candidate, evidence registry
  candidate, source manifest, gap ledger, visibility map, and admission request.
- Contestant/participant-visible material uses packet-safe source-family labels
  and excludes source URLs, titles, IDs, retrieval timestamps, source hashes,
  hidden labels, outcomes, claim ceilings, and facilitator-only provenance.
- Full provenance, source bytes or inspectable refs, hashes, typed gaps,
  leakage notes, and proposed pre-decision status remain facilitator-only.
- Final evidence `pre_decision_status` and final inclusion/exclusion remain
  Judgment-authority-owned.
- Packing proposes; operator/Judgment freezes; Harness validates and blocks
  rather than repairing.
- Seal the evidence assembly before any outcome reveal. A proving run must not
  use post-cutoff or post-reveal information to improve the packet.

## First Proving Slice: TikTok Creator Onboarding

Use the current TikTok creator-audience path as the first consumer because it
already has:

- source-faithful captured transcripts/comments;
- persisted Silver comment-attention and grid-observation prerequisites;
- a creator-isolated pre-Judgment evidence bundle;
- a compact Judgment view that tactically groups normalized duplicate text
  while preserving multiplicity and member lineage;
- a Judgment claim compiler and validator; and
- existing tests that expose both the upstream bulk handoff and current
  Judgment-side dedupe behavior.

### Lake-first route

Do not recapture TikTok.

Locate the best current corpus through:

1. relevant Silver/current read surface;
2. packet/catalog/Availability inventory;
3. raw packet only when required for verification or context.

Use the canonical Data Lake root named by current `AGENTS.md` and interpret it
through the owning physicality/location contract. Do not infer or substitute a
drive path from an old receipt. Treat absence from a Silver view as neither
absence from the lake nor absence from the external world.

### Migration target

Refactor the current TikTok creator-audience evidence assembly so:

- the TikTok adapter remains responsible for platform-specific source
  admission and identity isolation;
- the Packing core owns source-grounded unit assembly, decision-job binding,
  reversible compaction, relationships, visibility, gap handling, and receipt
  generation;
- the Judgment prompt receives a Packing-produced compact model view and
  evidence registry refs rather than relying on Judgment-owned tactical
  normalized-text grouping over an undifferentiated raw-cue/raw-comment bundle;
- the current compact-view v3 multiplicity, source-item coverage, member
  locations/comment mechanics, and claim-lineage expansion are preserved or
  strengthened;
- all materially relied-on evidence remains available to validation and the
  evidence drawer;
- existing v0 stored artifacts remain readable when compatibility is required;
  and
- new output uses explicit versioned Packing/Gold-ready vocabulary.

The first slice does not need to generalize every source family. It must expose
a clean media-neutral core and one TikTok adapter seam that another platform
can later implement without importing TikTok fields into the core.

### Real-lake rehearsal

Run a read-only rehearsal over one existing creator-isolated TikTok corpus with
transcripts, comments, and Silver engagement context.

Write derived proving outputs only to an isolated test/scratch data root unless
the owner separately authorizes a production-lake write.

The receipt must record:

- selected creator and raw anchor by safe reference;
- source/Silver inputs and hashes;
- decision question or explicit fixture question;
- evidence cutoff;
- atom and packed-unit schemas/policy versions;
- included, represented, dominated, excluded, and held units with typed reasons;
- duplicate/derivative relationships;
- complete materially relied-on support IDs;
- omitted-item index;
- participant/facilitator visibility split;
- gaps and residuals;
- `judgment_status: not_evaluated`;
- output hashes;
- proof that exact source context can be reopened.

Counts may be reported diagnostically. Do not treat reduction ratio, token
savings, unit count, or context size as correctness or completion.

If the real lake cannot be resolved or read, finish the deterministic fixture
proof and stop loudly with `BLOCKED_LIVE_LAKE_REHEARSAL`, naming the attempted
route and missing access fact. Do not fabricate a live proof.

## Required Deliverables

Fused scoping may refine exact names, but the work unit must include:

1. `forseti/product/spines/packing/README.md` as a discoverable Packing Spine
   front door.
2. A Packing authority/architecture contract under the new spine covering
   ownership, Silver interface, evidence-unit semantics, Gold-ready output,
   visibility, sealing, closure, and non-claims.
3. A reusable implementation core and strict schemas under an appropriate
   `forseti-harness/` home.
4. A versioned TikTok creator-audience adapter/migration using the core.
5. Any smallest-complete Silver producer or retrieval change proven necessary
   by the interface delta matrix, subject to the no-concurrent-writer rule.
6. Focused unit and integration tests.
7. A read-only TikTok proving receipt under `docs/workflows/`, or a typed live
   rehearsal blocker plus fixture evidence.
8. Required repo-map, spine-map, lane-registry, inventory, or routing updates
   only where the new durable surfaces would otherwise be undiscoverable or
   mechanically invalid.
9. Inline `direction_change_propagation` evidence for every doctrine-changing
   controlling source.

Do not create a speculative universal Packing registry, UI, scheduler, queue,
monitor, vector store, or multi-platform framework.

## Implementation Decisions To Lock During Fused Scoping

Resolve these before source edits:

1. Exact core home and package name.
2. Exact schema split between reusable Silver atoms and case-local packed
   units.
3. Whether the first slice needs a new Silver record type/producer or can
   consume current transcript/comment raw refs plus existing Silver mechanics.
4. Compatibility posture for existing TikTok audience bundle/snapshot v0/v1
   and compact Judgment view v3.
5. Deterministic identity and content-hash bases.
6. Compact model-view representation and complete omitted-item index.
7. No-concurrent-writer state for every Silver target.
8. Real-lake rehearsal route and scratch output root.
9. Exact validation commands and required review target.

If resolving one decision changes the authorized touchpoints materially, re-run
implementation scoping before editing.

## Validation

Validation must be able to fail and must preserve the failing command/output.

At minimum run:

### Focused behavior

- new Packing schema/core unit tests;
- exact source-pointer and surrounding-context recovery tests;
- deterministic identity/hash tests;
- candidate extraction rejection when a quote/span is absent;
- duplicate/cross-post/repost relationship tests;
- same-direction multi-source support retention tests;
- representative-display versus full-support preservation tests;
- participant/facilitator leakage tests;
- no-Gold-field tests;
- typed gap and blocked-state tests.

### TikTok integration

- the complete existing TikTok audience-triangulation unit file;
- focused TikTok capture/Silver selection tests selected by scoping;
- an end-to-end fixture path from admitted TikTok evidence through Packing into
  the existing Judgment validator;
- backward-read compatibility tests for existing stored versions when retained.

### Silver coupling

When Silver code or contracts change:

- focused Silver record, lineage, reader-selection, lane-registry, and
  compatibility tests for touched surfaces;
- no undeclared Silver lane writes;
- no decision/Judgment fields admitted into Silver;
- current readers remain fail-closed on ambiguous or unsupported records.

### Repository gates

- `git diff --check`;
- current diff-scoped policy gates from `.github/workflows/ci.yml`;
- full harness suite when CI classification or the touched implementation scope
  requires it;
- read-only live-lake rehearsal receipt verification when access exists.

Passing tests are not validation, product readiness, or proof of the evidence
claims. Report `GATE PASS`, `GATE FAIL`, `BLOCKED`, and `NOT RUN` separately.

## Acceptance Conditions

The work unit may close only when all are true:

- the Packing Spine is discoverable and has one controlling boundary;
- the implementation is media-neutral at its core and TikTok-specific only at
  its adapter;
- full transcript/comment source material remains preserved and retrievable;
- packed units are atomic, schema-bound, and reversible to exact source context;
- no generic prose summary is the sole durable evidence;
- Silver contains only reusable source-backed, decision-neutral facts;
- Packing contains case-specific assembly but no final Judgment;
- Gold-ready outputs are explicitly pre-Judgment;
- repeated agreeing evidence, duplicates, reposts, and contradictions follow
  the rules above;
- no numeric evidence or packing target establishes completeness;
- the real TikTok corpus rehearsal succeeds read-only, or the live blocker is
  loud and the fixture proof is complete;
- required DCP, focused tests, repository gates, and delegated review are
  resolved; and
- the implementation branch is committed, pushed, opened as one work-unit PR,
  and its exact remote revision is freshly verified.

## Hard Stops

Stop and report instead of weakening the contract when:

- the medallion layer or final inclusion owner cannot be established;
- transcript source bytes or inspectable refs cannot be resolved;
- a required Silver fact is unavailable and no non-overlapping owner route
  exists;
- a current Silver lane is concurrently editing the same target;
- the real TikTok data root or corpus identity cannot be established;
- source cutoff or sealing cannot be maintained;
- compacting the model view would silently delete materially relied-on evidence;
- the implementation would need a universal infrastructure expansion outside
  this proving slice;
- any gate fails and cannot be repaired within the commissioned scope; or
- delegated review identifies an unresolved material defect.

## Explicit Non-Goals

- No e.l.f. backtest continuation.
- No new TikTok capture or external-source access.
- No GTM, buyer, company-awareness, or causal claim.
- No final Judgment, Gold verdict, Action Ceiling, or commercial projection
  authored by Packing.
- No replacement of Silver Authority with a Packing cache.
- No full-corpus semantic ontology or universal summarizer.
- No multi-platform rollout beyond the media-neutral seam plus TikTok adapter.
- No participant UI or public product surface.

## Receiver Closeout

Return a concise human summary first, then agent-readable lifecycle evidence:

```yaml
closeout:
  status: complete | blocked
  branch:
  base_revision:
  commit_sha:
  push_state:
  pr_url:
  merged: false
  review_routing_status: routed | blocked
  review_return_adjudicated: yes | no
  packing_core:
  silver_changes:
  tiktok_adapter:
  real_lake_rehearsal: pass | blocked | not_run
  validation:
    focused:
    integration:
    silver:
    repository:
  changed_surfaces:
    - file:
      line:
      change:
  residuals:
  next_authorized_step:
```

Every load-bearing lifecycle claim must be freshly verified. Do not report a
commit, push, PR, merge, test, lake read, or review state that was not directly
observed.
