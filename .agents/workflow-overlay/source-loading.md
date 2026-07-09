# Source Loading

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Source-loading budgets, read packs, and context-bloat controls for Forseti prompts and workflow artifacts.
use_when:
  - Preparing Chief Architect prompts, review prompts, product prompts, or handoffs that cite Forseti source.
  - Deciding which files to read before producing a Forseti artifact.
  - Preventing context blow-up before a first artifact or first CA output.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/retrieval-metadata.md
  - docs/workflows/forseti_repo_map_v0.md
  - docs/workflows/artifact_retrievability_guide.md
```

## Rule

Source hierarchy decides authority. Source loading decides what to read.

Do not convert the source hierarchy into a read-all list. Load the smallest
source pack that can answer the current question, then expand only when a
missing source could materially change the output.

Use Forseti-owned source-loading mechanics: claim-level source loading, narrow
reads, source-read ledgers, evidence labels, strict/not-proven boundaries,
targeted excerpts, and context-budget discipline. The Forseti overlay and repo map
choose Forseti source files and source precedence. Legacy Orca-named paths remain
valid only as compatibility routes until migrated.

This file is the canonical Forseti owner for source-loading budgets, source-pack
tiers, source-capsule rules, and Data Capture Spine CA read-pack limits. Repo maps,
prompt artifacts, wrappers, and review requests may point here or summarize the
current rule for convenience, but they must not fork the rule. If another
retrieval or navigation artifact conflicts with this file, load
`.agents/workflow-overlay/source-of-truth.md` and resolve the conflict before
claiming readiness.

## Current Operating Boundary

Forseti is no longer globally docs-first by default. Documentation remains the
authority layer for project facts, decisions, prompts, reviews, migration notes,
and overlay maintenance, but implementation is permitted when a current turn or
accepted handoff explicitly authorizes a bounded implementation scope.

Architecture and product-method work may be future-runtime-aware when the user
asks for it. That means prompts may discuss eventual APIs, scraping, agents,
screenshots, archives, media, or source systems as conceptual requirements.
They must not authorize building, deploying, testing, or operating those
systems unless the current turn or accepted handoff explicitly grants bounded
implementation authority.

## Forseti Start Preflight

Before repo-aware Forseti prompt authoring, review setup, handoff creation,
docs-write or overlay maintenance, source-changing work, or completion claims,
record a compact start-preflight receipt. The receipt proves only that the
entrypoint and source-loading route were declared; it does not prove cognition,
validation, approval, readiness, implementation authorization, deployment,
resolver behavior, source-of-truth promotion, or edit permission beyond the
permission value stated in the receipt.

Start-route cue: when `target_scope` would change product doctrine,
architecture doctrine, workflow authority, validation philosophy, review
authority, output authority, or a lifecycle boundary, route through the
Doctrine Change Propagation Contract in
`.agents/workflow-overlay/source-of-truth.md`. If more than one doctrine
dimension applies, use the source-of-truth primary `trigger` plus
`related_triggers` grammar. The start preflight may name the expected
propagation surfaces, but it is not a substitute for the required
`direction_change_propagation` receipt or blocker at closeout.

Minimum receipt fields:

```text
orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: S0/S1/S2/S3/S4/custom
  edit_permission: read-only/docs-write/patch-only/implementation-authorized
  target_scope:
  dirty_state_checked: yes/no/not_applicable
  blocked_if_missing:
```

Use the smallest source pack that can support the task. `agents_read: yes`
means `AGENTS.md` was read or supplied in the current task context.
`overlay_read: yes` means `.agents/workflow-overlay/README.md` was read or
supplied in the current task context. If either field is `no` for a task that
requires Forseti project authority, stop and load the missing source before
continuing.

Do not require the receipt for tiny chat-only answers that do not create or
materially touch artifacts, route another agent, make completion/readiness
claims, depend on repository state, or change source. If a lightweight answer
turns into one of those tasks, record the receipt before continuing.

### Ordinary-Start Quick Path

For tiny, non-doctrine Forseti work, use the direct path:

1. Read the current user instruction.
2. Use `AGENTS.md` and `.agents/workflow-overlay/README.md` only when project
   authority is needed for the answer or edit.
3. Skip the repo map unless choosing among multiple possible source files would
   otherwise require broad search.
4. Skip Cynefin routing when `.agents/workflow-overlay/decision-routing.md`
   bypass conditions apply.
5. Stop and upgrade to the normal start preflight when the task becomes
   repo-aware prompt authoring, review setup, handoff creation, docs-write or
   overlay maintenance, source-changing work, completion/readiness claims,
   doctrine change, cross-thread work, delegation, or messy-worktree routing.

This quick path changes startup cost only. It does not weaken source hierarchy,
strict-claim rules, validation gates, implementation authorization, doctrine
propagation, or repo-map authority boundaries.

## Default Read Order

Use this order unless the user gives a narrower source pack:

1. Current user instruction.
2. `AGENTS.md`.
3. `.agents/workflow-overlay/README.md`.
4. `.agents/workflow-overlay/source-of-truth.md`.
5. This file, when source budgeting or prompt setup matters.
6. `docs/workflows/forseti_repo_map_v0.md`, when choosing among many docs.
7. The one to four target artifacts named by the request, repo map, retrieval
   headers, or nearest accepted product artifact.

Stop when the next file would only add background instead of changing the
decision, prompt, or artifact.

If more than four target artifacts appear necessary, switch to a source capsule
or new-thread handoff instead of bulk-reading.

## Source Pack Tiers

Use source packs instead of whole-folder reads.

| Tier | Use when | Default contents |
| --- | --- | --- |
| `S0 overlay` | Any Forseti project work. | Current instruction, `AGENTS.md`, overlay README, source-of-truth, and source-loading when relevant. |
| `S1 map` | Choosing files or preventing context bloat. | `S0` plus `docs/workflows/forseti_repo_map_v0.md`. |
| `S2 product anchor` | Product architecture, value proposition, offer, or CA setup. | `S1` plus product thesis, offer hypothesis, buyer proof packet, Core Spine product contract, and the nearest boundary note. |
| `S3 target deepening` | A specific artifact family needs details. | `S2` plus only the named target artifact, its `open_next` files, and targeted sections from adjacent artifacts. |
| `S4 historical/review` | Reviewing prior outcomes, adversarial reports, replays, or method-validation history. | Explicitly named review, replay, research, or historical files only. Never default. |

Do not load `S4` material unless the request explicitly depends on prior
reviews, method-validation history, contaminated outputs, or research corpus
details.

## Targeted Read Protocol

Prefer targeted sections over full files whenever a file is long, historical,
or adjacent rather than controlling.

### High-Context Guard

Before the route, blocker, edit boundary, source-loading unit, or strict claim is
known, do not widen source loading to prove general familiarity.

Use cheap orientation first:

- scan headings before opening long files;
- read exact section windows instead of full adjacent artifacts;
- cap search output to the smallest hit set that can identify the next source;
- summarize repository state by branch, HEAD, dirty/untracked status, and affected
  target paths when those paths are known;
- avoid broad whole-worktree status dumps unless whole-worktree state is itself
  decision-bearing;
- record plausible background sources as `available not read` or `not loaded
  because not decision-bearing` instead of opening them.

This guard does not weaken source authority. Strict claims still require the
controlling source, and skipped sources must be reopened when they could
materially change the current claim, route, blocker, or edit boundary.

For each source read, keep a compact ledger entry:

- file or source;
- why it was read;
- exact section or line range when targeted;
- what claim or decision it supports;
- status: clean, dirty, untracked, stale, user-stated, or not checked.

Apply source loading at the claim level:

- advisory claims may use repo-visible evidence with labels and gaps;
- strict claims about acceptance, readiness, validation, proof, authority,
  source-of-truth status, deployment, install, resolver behavior, or
  implementation authorization require controlling source;
- reading more source can improve confidence, but it cannot create missing
  authority.

Treat prior-thread memory, summaries, and context packets as orientation unless
they point to fresh source-visible artifacts. Do not let them carry strict
claims into a new CA prompt.

## Prompt Source Capsules

Chief Architect and model-lane prompts should not paste full Orca history.

Prefer a source capsule with:

- task objective;
- one-paragraph product anchor;
- boundary rules;
- source pack file list;
- short excerpts only for decisive lines;
- explicit source gaps and owner decisions;
- instructions to read named local files when the lane has filesystem access.

When a lane cannot access the repo, include a curated source capsule instead of
full documents. Keep the capsule focused on the decision the CA must make, not
on preserving every prior artifact.

Capsules should be shorter than the prompt's task instructions. If the capsule
becomes the dominant artifact, stop and create a narrower read pack or new
thread handoff.

### Source Capsule Contract

A source capsule must be a bounded decision aid, not a pasted archive.

Required fields:

```text
source_capsule:
  task_objective:
  source_pack_name:
  files_read:
  targeted_sections_read:
  sources_available_not_read:
  sources_excluded_by_default:
  decisive_excerpts:
  source_gaps:
  dirty_or_untracked_notes:
  non_claims:
```

Budget rules:

- Use at most four full-file reads.
- Use at most eight targeted section reads.
- Include at most ten decisive excerpts.
- Each excerpt should be the shortest quote or paraphrase that can carry the
  decision.
- Prefer paraphrase plus file path over long quotation.
- If the capsule needs more than ten excerpts, split the work or start a new
  thread.
- If any capsule budget would be exceeded, stop and narrow the question, split
  the source-loading unit, or create a new-thread handoff. Do not compress a
  broader archive into the capsule and call it bounded.

These budgets are also the ratified cold-lane retrievability bar (owner-ratified 2026-06-13): a cold lane navigating from the standard entry points should reach its decisive sources within this same budget. Exceeding it on a routine task is a retrievability defect signal, not a license to read more.

`sources_available_not_read` should name files that were relevant but skipped
because they would add background rather than change the current decision.

`sources_excluded_by_default` should name high-risk or high-volume areas such
as `_inbox`, review outputs, method-validation replays, proof-run packets, all
prompts, all research corpus files, or all product files.

`dirty_or_untracked_notes` must say when a source is modified or untracked. Such
sources may support advisory work, but strict claims about acceptance,
source-of-truth status, validation, readiness, or proof remain `not proven`
unless controlling authority accepts them.

When the receiving lane has repo access, the capsule should point to files and
sections instead of carrying long excerpts. When the receiving lane has no repo
access, the capsule may include short excerpts, but should still avoid full
documents.

Every CA or model-lane handoff using a source capsule must state whether the
receiving lane has repo access. Repo-access capsules should use paths, section
names, and short paraphrases. No-repo-access capsules may carry short decisive
excerpts, but must still honor the same budgets and exclusions.

## Data Capture Spine CA Read Pack

This section is the canonical read-pack rule for Data Capture Spine setup CA
prompts. Older prompts may call this the Data Spine CA read pack; treat that as
a deprecated shorthand for Data Capture Spine. Repo maps and prompt artifacts
should reference this section instead of restating the full pack.

Start with:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md` — the
  `retrieval_only` front door. It routes one hop to capture obligations,
  source-access authority, armory components, packet lifecycle, harness
  implementation, and source-quality support without bulk-loading every artifact.

Then open only the targeted sections needed for the CA prompt:

- `docs/decisions/orca_product_thesis_consumer_demand_v0.md`: thesis (the
  bet), value proposition, strategic center, and central-read sections.
- `forseti/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md`: core offer
  hypothesis, mechanism, fit diagnostic, and non-claims sections.
- `forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`: proof standard,
  target buyer, signal surface, disqualifiers, and not-build boundaries.
- `forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`:
  purpose, decision, layer rules, and future ECR/Evidence Unit boundaries.
- `forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md`: product bet,
  core rule, frozen primitives, and explicit non-goals only.
- `forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md`:
  Evidence Unit standard and boundary rules only.

Do not read these files in full by default. Use the targeted sections above,
then expand only when a specific source gap would change the CA prompt. Do not
include method-validation replays, proof-run packets, review outputs, or
research corpus files by default.

### Data Capture Spine CA Capsule Limit

A Data Capture Spine CA prompt should include only: one paragraph on Orca's
value proposition; one paragraph on the current Data Capture / ECR / Cleaning /
Judgment boundary; one paragraph on the bounded-implementation authorization
boundary; the targeted source pack above; the exact files and sections to read;
the default exclusions; and the owner decisions or source gaps the CA should
surface. Do not paste the full offer, proof packet, Core Spine contract,
boundary note, or IPF. Do not include method-validation history unless the CA
task explicitly asks how prior cases affected Data Capture Spine source loading.

## Data Capture Intake Surface / MSP Pressure-Test Target Pack

Use this pack when the task is to prepare, review, route, or verify the bounded
Data Capture pressure-test gate around Raw Capture, Mechanical Source
Projection, categorical ECR receipt, and Cleaning handoff.

Start with:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md` — the
  `retrieval_only` front door for Data Capture Spine / Source Capture Armory.
  It routes one hop to capture obligations, source-access authority, armory
  components, packet lifecycle, harness implementation, source-quality support,
  and current Reddit pre-commercial ordering without bulk-loading every artifact.

Then open the intake surface consolidation as the pressure-test anchor:

- `forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_intake_surface_consolidation_v0.md`

Then open only the controlling source for the current claim. Key owners:

- **Pressure-test closeout state and authorization-chain walk** (slot status,
  RQ status, CloakBrowser selection, Reddit ordering, tranche build authority):
  `forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_closeout_synthesis_v0.md`
  — the "Intake Surface / MSP Pressure-Test State" section carries the verbatim
  authorization-chain narrative relocated from this pack on 2026-06-13.
- **Source-observability scoping / RQ boundary**: open the requirements-boundary
  decision and source-access tooling authorization named by the consolidation map.
- **Post-batch patch planning, obligation-contract patch, adversarial review**:
  open the post-batch patch plan, patch proposal, owner decision, and review
  output named by the consolidation map.
- **Slot 3 WSO continuation or cross-venue synthesis**: open
  `forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md`
  before treating Reddit capture as complete venue coverage.
- **Source Capture Packet lifecycle / fixture admission**:
  `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
- **Source Quality State Assembler boundary**:
  `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md`

Capsule note: embedded state narrative (slot-by-slot history, authorization
boundaries, CloakBrowser selection, Reddit ordering) now lives in the closeout
synthesis. Do not use this pack to design ECR schema, Cleaning implementation,
or Judgment behavior.

## Source Capture Method (auto-load for capture-spine activity)

Any capture-spine activity — onboarding a source, running or commissioning a capture probe,
choosing or judging a capture route, or checking a "blocked" / NO-GO call — starts with the
**canonical capture-method playbook**
`forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` and its `open_next`
`forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`. It is the canonical method (the
retired `capture_investigation_playbook_v0.md` is its pre-rename name); load it before picking a
route, and do not re-derive the access-control gate (Step 0) or the route catalog from scratch.

Scanning / screening activity reads the screening-side distillation of this method — the **Walker
Equipment Kit** in `forseti/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` (public pages,
no logins, URLs + short quotes) — and escalates to the full playbook only for packet-grade capture.

For raw-to-Judgment projection views, also open
`forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`; it constrains projection
as a view over raw, not Cleaning, Judgment, or a new spine layer.

## ECR Source-Side Spine Read Pack

Use this pack when the task touches the ECR source-side derived-record spine —
the integrity postures (ECR SP-1/2/3/6) or the Signal Content Record — including
their plans, models, or deriver code.

Start with:

- `docs/workflows/ecr_spine_submap_v0.md` for orientation. It is the
  `retrieval_only` front door: it states the cross-kind invariants and routes one
  hop to every owner (the SCR direction + deriver plan, the ECR frame + SP-1/2/3
  and SP-6 slices, the receipt-translator origin, the schema-evolution doctrine,
  and the built `forseti-harness/ecr/` + `forseti-harness/signal_content/` code).

Then open only the controlling owner doc named by the submap for the current
claim. Do not bulk-load every ECR/SCR plan or all derived-record code from this
pack. This is a navigation pointer only; it does not claim ECR/SCR is validated,
ratified, ready for Evidence-Unit binding, or that JSG-01 is unfrozen (the gate
stays FROZEN). This pack must not fork the source-loading rule; the submap
routes, the owner docs decide.

## Judgment Spine Evidence Ladder Read Pack

Use this pack when classifying what a Judgment Spine run, case, model answer,
memo, deck, or proof artifact can claim, or when checking whether a lower-tier
signal is being overclaimed.

Start with:

- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` — the
  `retrieval_only` front door. It orients across thesis, cases, manifest,
  conductor, gate ownership, evidence ladder, JSG-08, and harness surfaces, and
  routes one hop to each owner without bulk-loading the corpus. Per-claim-type
  owner pointers (evidence ladder, gate ownership map, reveal/calibration
  contract, conductor) live in that map's Fast Route table.

Then open only the controlling source for the claim being considered:

- **Claim-tier classification or overclaim check**: evidence ladder at
  `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`.
- **Gate ownership (source identity, packet freeze, no-tools, scoring, reveal,
  closeout, or promotion blockers)**: gate ownership map at
  `forseti/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md`.
- **JSG-08 reveal/calibration receipt**: owner contract at
  `forseti/product/spines/judgment/conductor/judgment_spine_reveal_calibration_owner_contract_v0.md`.
- **Running or planning a case through JSG-01→JSG-10**: conductor at
  `forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md`.
- **Buyer-proof claims**: `.agents/workflow-overlay/product-proof.md` and
  `forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`.
- **Judgment-quality, blind-use, fixture-admission, scoring, or calibration
  claims**: `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md`
  and the specific case/run artifact.
- **Pre-sale manual subscription/chat routing claims**:
  `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`.

Do not bulk-load all Judgment Spine research, all harness specs, all proof-run
packets, all review outputs, or all case artifacts by default. Strict Buyer-Proof
or Judgment-Quality claims remain not proven until the controlling tier gate is
satisfied.

## Expansion Rules

Expand source loading only when one of these is true:

- a named artifact's retrieval header says to open another file;
- a material source conflict appears;
- a strict claim depends on authority, validation, readiness, acceptance, or
  proof status;
- a source gap could change the recommendation;
- the user explicitly asks for a broader source review.

When expanding, prefer targeted section reads over full-file reads.

Do not follow every retrieval-header `open_next` automatically. Open it only
when it can change the current task; otherwise list it as an available source
not read.

If expansion would exceed the source-capsule budget, require more than one
`S3` artifact family, or pull `S4` history by default, stop and return the
specific source gap or new-thread handoff requirement instead of broadening the
read pack inside the same prompt.

## Artifact Body Shape

When creating or materially touching a durable human-authored workflow
artifact, use `.agents/workflow-overlay/retrieval-metadata.md` for the header
contract and `docs/workflows/artifact_retrievability_guide.md` for operational
body-shape guidance.

For long or decision-bearing artifacts, put a compact source-loading surface
near the top: purpose, use when, do not use for, authority boundary, next source
when material, stale conditions, recheck recipe when provenance matters, and
strict claims that remain not proven.

The guide is subordinate to this overlay. It may help shape artifact bodies,
fresh-agent checks, and report-only retrieval findings, but it does not change
source hierarchy, accepted folders, validation gates, artifact roles,
implementation authorization, or the rule that `open_next` is conditional.

## New Thread Triggers

Start a new thread or create a compact handoff prompt before continuing when:

- more than one `S3` family is needed for the first artifact;
- the prompt would need more than six full artifacts pasted inline;
- the lane cannot access repo files and the source capsule would become longer
  than the intended CA task;
- a repo map refresh and a CA prompt are both needed and would compete for
  context;
- the current thread has substantial unrelated history that could bias the CA.

The handoff should name the source pack, the target output, the non-goals, and
the files explicitly excluded from default loading.

## Files Not To Bulk-Load By Default

Do not bulk-load these by default:

- `docs/_inbox/`, especially contaminated method-validation outputs;
- all method-validation replays;
- all proof-run packets;
- all review outputs;
- all prompts;
- all research corpus files;
- all product files.

Use the repo map to select a narrow source pack instead.

## Not-Proven Boundaries

Source loading does not prove acceptance, readiness, validation, buyer pull,
implementation authorization, deployment, resolver behavior, or source-of-truth
promotion.

If a claim needs one of those statuses, load the controlling authority or mark
the claim `not proven`.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Spine read packs (Data Capture Spine CA, Data Capture Intake Surface / MSP
    Pressure-Test Target, Judgment Spine Evidence Ladder) reshaped to
    front-door pointer form matching the ECR pack model: each pack now leads
    with its retrieval_only front-door submap and routes to owner docs on
    demand. Embedded spine state (slot-by-slot pressure-test authorization-chain
    walk, CloakBrowser selection, Reddit ordering, RQ status) relocated verbatim
    to the spine-owned closeout synthesis. Source-loading.md is navigation only;
    state of the work lives in the spine-owned doc it belongs to.
  trigger: workflow_authority
  related_triggers:
    - architecture_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/source-loading.md
    - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_closeout_synthesis_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/README.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Prompt orchestration binds source-loading as the read-pack authority and
        points here; it does not reproduce pack contents. The front-door reshape
        does not change the binding rule.
    - path: .agents/workflow-overlay/README.md
      reason: >
        The overlay index already names source-loading.md as the read-pack owner.
        No section owner or overlay path changed.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map already points to the section anchors
        (source-loading.md#data-capture-intake-surface--msp-pressure-test-target-pack
        etc.) and does not reproduce pack contents. Section headings are
        unchanged so existing anchors remain valid.
    - path: docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
      reason: >
        The Judgment Spine consolidation map is the front door this pack now
        points to; it is not a downstream consumer of pack contents. No changes
        needed there.
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      reason: >
        The Data Capture Spine consolidation map is the front door this pack now
        points to; it is not a downstream consumer of pack contents. No changes
        needed there.
  stale_language_search: >
    rg -n "MSP|pressure-test|read pack" .agents/workflow-overlay/
  stale_language_search_result: >
    Executed 2026-06-13 after edits. Hits in .agents/workflow-overlay/:
    artifact-folders.md:197 ("read packs reference unchanged paths until
    Phase-2 apply" — DCP receipt comment, not stale); README.md:19 ("read
    packs, and context-bloat controls" — description of source-loading.md,
    accurate); source-loading.md — section title "Data Capture Intake Surface /
    MSP Pressure-Test Target Pack" (correct, kept), "pressure-test" in navigation
    text (correct nav context, not state prose), "read pack" in capsule-limit
    prose and Expansion Rules (both accurate descriptions of navigation artifacts,
    not stale); source-of-truth.md — references to source-loading.md description
    (accurate). No hit retained the inline authorization-chain state narrative
    or bulk file-list in source-loading.md; none points to a stale-language
    conflict requiring a further fix.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation authorization
    - not ECR or Judgment design
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Source-loading now binds the canonical capture-method playbook
    (source_capture_playbook_v0.md + its open_next recon-index) as a required start-read for
    capture-spine activity, and points scanning/screening activity at the screening-side Walker
    Equipment Kit (escalating to the playbook only for packet-grade capture). Previously the
    playbook was canonical but referenced by no overlay surface and reachable only one hop from a
    pack — not an auto-load start-read.
  trigger: workflow_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/source-loading.md
  downstream_surfaces_checked:
    - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    - forseti/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
      reason: >
        It is the target being bound and is already canonical; no content change is needed to make
        it a start-read.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map already routes to the playbook / recon-index; adding a source-loading
        start-read does not change the map's pointers.
  stale_language_search: >
    rg -n "capture_investigation_playbook|source_capture_playbook" .agents/workflow-overlay/
  stale_language_search_result: >
    Executed 2026-06-14 in the worktree. No matches in .agents/workflow-overlay/ — the overlay
    referenced neither the canonical nor the retired playbook name before this edit, so this adds
    the first overlay binding and there is no stale retired-name reference to repoint.
  non_claims:
    - not validation
    - not readiness
    - not authorization to capture, build, or run (the playbook stays non-authorizing doctrine;
      per-probe network approval still required)
```
