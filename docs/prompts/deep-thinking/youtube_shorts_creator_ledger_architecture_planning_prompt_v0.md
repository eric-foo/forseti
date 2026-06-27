# YouTube Shorts Creator Ledger Infrastructure Architecture Planning Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: >
  Prompt for a fresh Chief Architect lane to run standard architecture planning,
  with exactly three delegated advisory subagents, on the future real creator
  ledger infrastructure for YouTube Shorts creator discovery, capture, lake
  attachment, and projected niche/sub-niche lookup.
use_when:
  - Commissioning the creator-ledger infrastructure placement and derivation architecture pass.
  - Deciding whether the durable ledger is primary, derived, materialized, or split across spines.
  - Checking the required source pack and subagent contract for this architecture commission.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/youtube_shorts_creator_index_decision_path_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/scanning/README.md
branch_or_commit: codex/youtube-shorts-tone-viability-prompt @ 0305edb82052ba66fc955ad273aa3f3c86f8738d
stale_if:
  - docs/workflows/youtube_shorts_creator_index_decision_path_v0.md changes.
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json changes.
  - Capture, Data Lake, Scanning, Projection, or artifact-folder contracts change.
  - The commissioned architecture lane returns its recommendation.
```

Paste the body below into a fresh Chief Architect thread in this workspace.

---

You are the Chief Architect for Orca.

## Objective And Intended Decision

Run a planning-only architecture pass for the future **real creator-ledger
infrastructure**: a ledger/index that can answer "show all creators under niche
or sub-niche X, with important source-backed observed stats."

The intended decision is:

1. where the durable creator-ledger infrastructure belongs across Scanning,
   Capture, Data Lake, domain satellites, and Projection;
2. whether the queryable ledger should be primary, derived, materialized, or
   split;
3. which contracts must exist before any runtime capture, scheduler, crawler,
   database table, or permanent ledger implementation.

This is an architecture-planning commission only. Do not build, edit runtime
code, create a crawler, create a permanent table, write an implementation route,
or claim validation/readiness.

## Fitness Reference

- Goal: decide the architecture placement and derivation model for Orca's future
  creator ledger infrastructure.
- Done looks like: a source-backed architecture result that either recommends a
  target architecture or explicitly declines to select one, with core/satellite
  boundaries, non-claims, and the smallest complete next routing object.

## Preflight

- Prompt artifact input:
  `docs/prompts/deep-thinking/youtube_shorts_creator_ledger_architecture_planning_prompt_v0.md`.
- preflight_defaults:
  `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants
  bound; deltas stated here.
- Workspace:
  `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-shorts-tone-viability-prompt`.
- Expected branch:
  `codex/youtube-shorts-tone-viability-prompt`.
- Expected authoring head:
  `0305edb82052ba66fc955ad273aa3f3c86f8738d`.
- Dirty-state allowance:
  worktree should be clean except ignored `docs/hygiene/precompact_*` files;
  re-run `git status --short --branch --ignored=matching docs/hygiene/precompact_youtube_shorts_creator_infrastructure.md`
  before acting.
- Authorization basis:
  current owner instruction asked for a prompt commissioning architecture
  planning using the standard 3-subagent mode.
- Prompt authoring output mode:
  filed prompt artifact plus paste-ready copy.
- Receiving-lane output mode:
  chat-only architecture recommendation. Do not write files unless the owner in
  your thread explicitly redirects you to save a recommendation artifact.
- Edit permission:
  read-only.
- Target files or dirs:
  source files named in the required reads and source-load pack below.
- Source pack:
  custom S3 target deepening; load authority first, then task sources.
- Controlling source state:
  not trusted from this prompt; re-check live state in your thread.
- Doctrine change decision:
  the architecture recommendation may propose later doctrine or contract
  changes, but this prompt authorizes recommendation only. Any accepted
  source-changing doctrine edit would require the Orca Doctrine Change
  Propagation Contract in `.agents/workflow-overlay/source-of-truth.md`.
- Isolation decision:
  no new branch or worktree for this read-only architecture pass.
- Validation gates:
  no validation, readiness, approval, or implementation claim is in scope.
- thread_operating_target_continuity:
  carried_forward: no; reason: no visible active thread operating target was
  supplied with this commission.

## Required Reads

Authority and operating rules:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md` - run Cynefin routing before
  architecture planning.
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/workflows/orca_repo_map_v0.md`

Method instructions:

- REFERENCE-LOAD `workflow-architecture-planning` if available. If the skill is
  available only as a local file, use
  `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.87\skills\workflow-architecture-planning\SKILL.md`.
- Do not APPLY architecture planning before `SOURCE_CONTEXT_READY`.
- Treat workflow skill text as method guidance only, not Orca project authority.

Task sources:

- `docs/workflows/youtube_shorts_creator_index_decision_path_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_product_talk_posture_pilot30_v0.md`
- `docs/review-inputs/youtube_shorts_fragrance_product_talk_posture_pilot30_v0.json`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md`
- `orca/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md`
- `orca/product/spines/capture/core/operating_model/orca_capture_projection_storage_spine_architecture_v0.md`
- `orca/product/spines/data_lake/README.md`
- `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`
- `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`
- `orca/product/spines/scanning/README.md`

If any required task source is missing, declare `SOURCE_CONTEXT_INCOMPLETE` and
name the missing path. Do not fill gaps from memory.

## Source Facts To Reconfirm, Not Trust

- Current 200-row fragrance creator ledger records observed YouTube
  handles/channels only. It is not identity verification, not creator ranking,
  not buyer proof, and not proof of independent creator status.
- The current workflow decision record says the durable target is real
  creator-ledger infrastructure, not a one-off workflow index.
- The prior candidate split was: Scanning discovers candidate creators; Capture
  owns creator-observation contracts; Data Lake stores raw/source-backed
  attachments; Projection owns the queryable ledger view.
- The architecture pass must treat that split as a candidate, not as an
  untouchable answer.

## Architecture Question

Decide the target architecture for the future creator ledger:

- What is the source of truth for creator observations?
- What is the source of truth, if any, for niche/sub-niche membership?
- Is the queryable creator ledger a derived/materialized projection, a primary
  table, a Data Lake view, a Capture-owned index, a domain-satellite artifact,
  or another shape?
- What must Data Lake store to make the ledger reproducible without becoming the
  semantic owner?
- What must Capture define before recurring capture or projection exists?
- What belongs in Scanning, and what must Scanning not own?
- What stats are allowed as observed metrics, and what is explicitly not
  claimed?
- What is the smallest complete next routing object after the recommendation?

## Required Workflow

1. Run Orca Cynefin routing before planning. This should classify the work as
   architecture planning unless live source drift changes that.
2. REFERENCE-LOAD `workflow-architecture-planning`. Do not APPLY it yet.
3. SOURCE-LOAD the required source pack above under
   `.agents/workflow-overlay/source-loading.md`.
4. Declare either `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-architecture-planning` in
   **standard** profile.
6. Launch exactly three delegated advisory subagents after source readiness:
   Directional, Adversarial, and Grounding.
7. If the host cannot launch subagents, return
   `BLOCKED_SUBAGENTS_UNAVAILABLE`. Do not silently replace the delegated
   lanes with local passes unless the owner explicitly redirects you.
8. Synthesize the three advisory outputs yourself. Subagents provide inputs,
   not verdicts.

## Three Subagent Dispatches

Use inherited/default agent type and model unless the host explicitly supports a
different override shape. Do not combine forked context with unsupported runtime
override fields. Each subagent must use the same source-loaded context or receive
a bounded source capsule. Each subagent output must be terse, cite file paths or
sections for load-bearing claims, and include this sentence:

`This is advisory input only. It is not a verdict, not implementation authority, and not proof of readiness.`

### Directional Subagent

Mission: make the strongest source-backed case for the best target architecture
for the real creator ledger.

Return exactly:

- `recommended_shape:`
- `core_owner:`
- `satellite_owners:`
- `derived_or_primary:`
- `source_of_truth_boundary:`
- `data_lake_role:`
- `capture_role:`
- `projection_role:`
- `strongest_evidence:`
- `biggest_tradeoff:`
- `smallest_next_object:`
- advisory sentence above

### Adversarial Subagent

Mission: attack the likely target architecture and identify coupling, fake
success, boundary leakage, identity mistakes, brittle derivation, future
rigidity, and overfitting to the current 200-row fragrance evidence.

Return exactly:

- `target_attacked:`
- `blocker_or_major_risks:`
- `data_lake_misplacement_risk:`
- `capture_contract_gap:`
- `projection_fake_success_risk:`
- `identity_or_niche_membership_risk:`
- `what_would_make_target_wrong:`
- `minimum_fix_before_acceptance:`
- advisory sentence above

### Grounding Subagent

Mission: keep the result repo-native, source-bounded, anti-bloat, reversible
where possible, and planning-only.

Return exactly:

- `repo_native_home_options:`
- `accepted_folder_or_spine_constraints:`
- `must_cut_or_defer:`
- `non_claims_required:`
- `source_gaps:`
- `validation_or_readiness_claims_forbidden:`
- `smallest_complete_next_routing_object:`
- advisory sentence above

## Options To Compare

Compare materially different options. Include at least these unless source
loading proves one is impossible:

- Capture-owned creator-observation contract plus Data Lake attachments plus
  Projection-owned queryable ledger.
- Data Lake-centered creator table or view.
- Projection-first derived ledger over capture/lake evidence.
- Scanning-led creator index/frontier.
- Domain-satellite-led ledger for fragrance first.
- No-selection/defer until missing contract or owner decision is resolved.

Do not make the current recommendation the default. Treat it as one candidate.

## Output Contract

Start with a short human summary, then provide agent detail.

Required result shape:

```text
Human Summary:
Decision:
Target Architecture:
Why This Wins:
Core / Satellite Boundary:
Derived vs Primary Ledger:
What Data Lake Owns:
What Capture Owns:
What Scanning Owns:
What Projection Owns:
What Domain Satellites Own:
What We Are Not Doing:
Next:

Agent Detail:
Profile / Evidence Mode / Source Mode:
Subagents Launched:
Source-Read Ledger:
SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE:
Cynefin Routing:
Questions This Must Answer:
Architecture Option Comparison:
Directional Advisory Input:
Adversarial Advisory Input:
Grounding Advisory Input:
Architecture Result:
Target Architecture Detail:
Deferred Implementation Implications:
Bloat-Cut Queue:
Blockers / Not-Proven Boundaries:
What Would Change The Recommendation:
```

Return exactly one architecture result from the `workflow-architecture-planning`
vocabulary: `TARGET_RECOMMENDED`, `OPTIONS_COMPARED_NO_SELECTION`,
`NEEDS_ARCHITECTURE_QUESTION`, `NEEDS_PRODUCT_DECISION`,
`NEEDS_FEATURE_PLANNING`, `NEEDS_SOURCE_CONTEXT`, `DEFER_OR_REJECT`, or
`AUTHORITY_BLOCKED`.

## Hard Boundaries

- Do not perform implementation scoping.
- Do not author runtime code, crawler code, scheduler code, a database table, or
  a permanent ledger implementation.
- Do not claim validation, approval, readiness, source-of-truth promotion, or
  buyer proof.
- Do not treat this prompt as authority over Orca overlay files.
- Do not import `jb` policy, paths, lifecycle mechanics, validation habits, or
  prompt templates.
- Do not collapse creator identity, handle, channel, niche membership, and
  projected ledger row into one unqualified source-of-truth object.
- Do not make absence or hidden stats equal observed zero.
- Do not treat the current 200-row fragrance creator ledger as the recurring
  infrastructure schema.
