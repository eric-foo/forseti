# Source Loading

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Source-loading budgets, read packs, and context-bloat controls for Orca prompts and workflow artifacts.
use_when:
  - Preparing Chief Architect prompts, review prompts, product prompts, or handoffs that cite Orca source.
  - Deciding which files to read before producing an Orca artifact.
  - Preventing context blow-up before a first artifact or first CA output.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/retrieval-metadata.md
  - docs/workflows/orca_repo_map_v0.md
  - docs/workflows/artifact_retrievability_guide.md
```

## Rule

Source hierarchy decides authority. Source loading decides what to read.

Do not convert the source hierarchy into a read-all list. Load the smallest
source pack that can answer the current question, then expand only when a
missing source could materially change the output.

Use Orca-owned source-loading mechanics: claim-level source loading, narrow
reads, source-read ledgers, evidence labels, strict/not-proven boundaries,
targeted excerpts, and context-budget discipline. Orca overlay and repo map
choose Orca source files and source precedence.

This file is the canonical Orca owner for source-loading budgets, source-pack
tiers, source-capsule rules, and Data Capture Spine CA read-pack limits. Repo maps,
prompt artifacts, wrappers, and review requests may point here or summarize the
current rule for convenience, but they must not fork the rule. If another
retrieval or navigation artifact conflicts with this file, load
`.agents/workflow-overlay/source-of-truth.md` and resolve the conflict before
claiming readiness.

## Current Operating Boundary

Orca is no longer globally docs-first by default. Documentation remains the
authority layer for project facts, decisions, prompts, reviews, migration notes,
and overlay maintenance, but implementation is permitted when a current turn or
accepted handoff explicitly authorizes a bounded implementation scope.

Architecture and product-method work may be future-runtime-aware when the user
asks for it. That means prompts may discuss eventual APIs, scraping, agents,
screenshots, archives, media, or source systems as conceptual requirements.
They must not authorize building, deploying, testing, or operating those
systems unless the current turn or accepted handoff explicitly grants bounded
implementation authority.

## Orca Start Preflight

Before repo-aware Orca prompt authoring, review setup, handoff creation,
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
requires Orca project authority, stop and load the missing source before
continuing.

Do not require the receipt for tiny chat-only answers that do not create or
materially touch artifacts, route another agent, make completion/readiness
claims, depend on repository state, or change source. If a lightweight answer
turns into one of those tasks, record the receipt before continuing.

## Default Read Order

Use this order unless the user gives a narrower source pack:

1. Current user instruction.
2. `AGENTS.md`.
3. `.agents/workflow-overlay/README.md`.
4. `.agents/workflow-overlay/source-of-truth.md`.
5. This file, when source budgeting or prompt setup matters.
6. `docs/workflows/orca_repo_map_v0.md`, when choosing among many docs.
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
| `S0 overlay` | Any Orca project work. | Current instruction, `AGENTS.md`, overlay README, source-of-truth, and source-loading when relevant. |
| `S1 map` | Choosing files or preventing context bloat. | `S0` plus `docs/workflows/orca_repo_map_v0.md`. |
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
a deprecated shorthand for Data Capture Spine.
Repo maps and prompt artifacts should reference this section instead of
restating the full pack.

For a Data Capture Spine setup CA, start with these targeted sections:

- `docs/decisions/turn_08_product_thesis_v0.md`: thesis, value proposition,
  strategic center, and current theory sections.
- `docs/product/orca_offer_hypothesis_v0.md`: core offer hypothesis,
  mechanism, fit diagnostic, and non-claims sections.
- `docs/product/orca_buyer_proof_packet_v0.md`: proof standard, target buyer,
  signal surface, disqualifiers, and not-build boundaries.
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`:
  purpose, decision, layer rules, and future ECR/Evidence Unit boundaries.
- `docs/product/core_spine_v0_product_contract.md`: product bet, core rule,
  frozen primitives, and explicit non-goals only.
- `docs/product/core_spine_v0_information_production_foundation_v0.md`:
  Evidence Unit standard and boundary rules only.

Do not read these six files in full by default. Use the targeted sections
above, then expand only when a specific source gap would change the CA prompt.
If a prompt author cannot locate the named sections, the prompt must report a
source gap instead of widening to full-file reads by default.

Do not include method-validation replays, proof-run packets, review outputs,
or research corpus files by default. Use the repo map to decide whether any
one of those is necessary.

### Data Capture Spine CA Capsule Limit

A Data Capture Spine CA prompt should include only:

- one paragraph on Orca's value proposition;
- one paragraph on the current Data Capture / Evidence Candidate Record /
  Cleaning / Judgment boundary;
- one paragraph on the bounded-implementation authorization boundary;
- the targeted source pack above;
- the exact files and sections to read;
- the default exclusions;
- the owner decisions or source gaps the CA should surface.

It should not paste the full offer, proof packet, Core Spine contract, boundary
note, or IPF. It should not include method-validation history unless the CA task
explicitly asks how prior cases affected Data Capture Spine source loading.

## Data Capture Intake Surface / MSP Pressure-Test Target Pack

Use this pack when the task is to prepare, review, route, or verify the bounded
Data Capture pressure-test gate around Raw Capture, Mechanical Source
Projection, categorical ECR receipt, and Cleaning handoff.

Start with:

- `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`

For post-batch patch planning, review, or owner decision, also open:

- `docs/product/data_capture_spine_post_batch_patch_plan_v0.md`
- `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md`
- `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`
- `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md`

For all-slot source-observability scoping authorization or follow-on scoping,
also open:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md` first for
  Data Capture Spine / Source Capture Armory orientation; it routes one hop to
  capture obligations, source-access authority, armory components, packet
  lifecycle, harness implementation, source-quality support, and current Reddit
  pre-commercial ordering without bulk-loading every capture artifact.
- `docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md`
- `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md`
- `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md`
- `docs/decisions/data_capture_spine_source_observability_requirements_support_implementation_scoping_authorization_v0.md`
- `docs/decisions/data_capture_spine_source_observability_local_support_implementation_scoping_authorization_v0.md`
- `docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md`
- `docs/decisions/data_capture_spine_source_observability_support_closeout_decision_v0.md`
- `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md`
- `docs/product/source_capture_toolbox/README.md`
- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md` when deciding whether generated Source Capture Packets remain scratch, may be cited by durable closeouts, require retention/sensitivity handling, or require a cited separate admission decision before `separately_admitted` can be used.
- `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` when checking whether already-bounded source-quality rows and existing Source Capture Packets may be assembled into a state census without runner dispatch, source discovery, scoring, fixture admission, or Judgment authority.
- `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md`

Then open only the controlling source needed for the current claim:

- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v2.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`
- `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`

For Slot 3 WSO continuation or cross-venue Slot 3 synthesis, also open
`docs/product/data_capture_spine_pressure_test_slot3_reddit_subbatch_control_note_v0.md`
before treating Reddit capture as complete venue coverage. That note records
the Reddit sub-batch checker outcomes, source-language-anchor lesson, media and
cutoff limitations, and the open WSO-run versus WSO-defer control decision.

The accepted consolidation is the bounded pressure-test target, not a final
Capture Spine contract and not pressure-test validation. The first N=3 batch
classification decision classifies that batch as patchable and authorizes
docs-only patch planning, not contract hardening or runtime/source-system
implementation. The post-batch patch plan sequences the currently authorized
docs-only patch candidates for owner gating after adversarial review; the owner
decision accepts that plan for downstream docs-only patch drafts, but neither
artifact amends the obligation contract or source-access method plan. The
obligation-contract patch proposal owner decision accepted PCP-01 through PCP-08
as bounded authority for docs-only obligation-contract amendment drafting; that
package is now consumed by the amended controlling obligation contract. The
proposal and owner decision remain historical amendment inputs and do not amend
the source-access method plan or authorize runtime/source-system
implementation. The source-observability scoping authorization permits one
bounded docs-only requirements scoping lane from the all-slot pressure-test
synthesis; the resulting source-observability requirements scoping artifact is
candidate decision input, not governing doctrine. The post-Slot-3-recapture
requirements-boundary decision is the current source for RQ status after
recapture: RQ-01, RQ-03, and RQ-05 carry forward; RQ-02 is split into
visibility-now/body-retrieval-default-deferred; RQ-04 remains deferred candidate
context. The requirements-support implementation-scoping authorization permits
one bounded scoping lane for RQ-01, RQ-03, RQ-05, and RQ-02 visibility-only
support; it does not authorize implementation execution, RQ-04/source-access
handling, archive/media retrieval, source-access method-plan amendment, or
contract hardening. The local support
implementation-scoping authorization permits one bounded implementation-scoping
lane for local source-observability support, not implementation execution. The
local support implementation-execution authorization separately records and
bounds the implemented local operator-record/checker/report/docs/tests surface;
it does not authorize further implementation expansion. The support closeout
decision records that the current local helper proved sufficient for the
accepted post-recapture Slot 3 dry-use without schema or code expansion, while
leaving a later helper-semantics vocabulary patch as candidate-only if repeated
future friction warrants it. The pressure-test closeout synthesis records the
first Data Capture pressure-test foundation as good enough for bounded next
planning while carrying Slot 1, Slot 2, Slot 3, and Source Observability
limitations forward; it is not validation, readiness, pressure-test discharge,
contract hardening, or source-access method-plan amendment. The Source Capture
Armory README is the product-facing entrypoint for bounded tooling docs
and gaps. The Source Quality State Assembler architecture is a read-only
multi-row state-census boundary over already-bounded source-quality rows and
existing Source Capture Packets; it does not authorize source discovery, runner
dispatch, source-quality scoring, fixture admission, or Judgment behavior. A
Source Capture Packet fixture/retention/sensitivity decision controls how
generated packets move from scratch output to durable operational context,
candidate evidence, fixture-admission recommendation, or separate fixture
admission; it does not admit any current packet, prove source completeness,
clear rights, or authorize production storage. Later owner decisions now
authorize bounded source-access tooling build surfaces: first-tranche Source
Capture Packet core/CLI, direct HTTP fetch, media/asset preservation,
Archive.org availability/body retrieval, and honest browser snapshot support;
second-tranche Reddit API adapter and owner-named source adapters; and
third-tranche anti-blocking/proxy/JS-challenge support. CloakBrowser is the
selected primary anti-blocking browser backend for the next implementation lane.
For Reddit pre-commercial capture, the current order is CloakBrowser
anti-blocking first once implemented, then low-volume bounded
subreddit/thematic/thread-family capture, then archive capture; commercial use
moves to the sanctioned commercial / enterprise API or data-licensing path. That
authorization does not cover commercial fetch services, SERP APIs, broad
crawler/spider frameworks, storage, dashboards, schedulers, deployment,
production runtime, contract hardening, source-access boundary change, or
ECR/Cleaning/Judgment design. Do not use this pack to design ECR schema,
Cleaning implementation, or Judgment behavior.

## Judgment Spine Evidence Ladder Read Pack

Use this pack when classifying what a Judgment Spine run, case, model answer,
memo, deck, or proof artifact can claim, or when checking whether a lower-tier
signal is being overclaimed.

Start with:

- `docs/product/judgment_spine_evidence_ladder_architecture_v0.md`
- `docs/product/judgment_spine_gate_ownership_map_v0.md` when the work asks
  which gate owns source identity, packet freeze, no-tools isolation,
  memorization probe, sealed output, scoring, reveal/calibration, claim
  classification, closeout, or judgment-quality promotion blockers.
- `docs/product/judgment_spine_reveal_calibration_owner_contract_v0.md` when
  the work asks whether reveal/calibration material is absent, reveal-only,
  qualitative calibration, score-linked calibration, contaminated, or strong
  enough to satisfy `JSG-08` for a stronger claim.
- `docs/product/judgment_quality_promotion_operating_model_v0.md` when the work
  needs to run or plan a case through gates JSG-01 to JSG-10, decide a run's
  lifecycle state, or check what a partial or by-hand run can claim. This is the
  conductor: it sequences and verifies gate receipts and never computes judgment
  quality.

Then open only the controlling source for the stronger claim being considered:

- For buyer-proof claims, open `.agents/workflow-overlay/product-proof.md` and
  `docs/product/orca_buyer_proof_packet_v0.md`.
- For judgment-quality, blind-use, fixture-admission, clean no-tools, scoring,
  probe, or calibration claims, open
  `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md`
  and the specific case/run/probe/scoring/reveal/calibration artifact.
- For pre-sale manual subscription/chat routing claims, open
  `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`.

Do not bulk-load all Judgment Spine research, all harness specs, all proof-run
packets, all review outputs, or all case artifacts by default. Product-Learning
evidence may guide design and patch priorities, but strict Buyer-Proof or
Judgment-Quality claims remain not proven until the controlling tier gate is
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
