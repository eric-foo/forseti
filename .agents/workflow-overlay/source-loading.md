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

Use reusable `agent-workflow` source-loading mechanics as advisory mechanics
only: claim-level source loading, narrow reads, source-read ledgers, evidence
labels, strict/not-proven boundaries, targeted excerpts, and context-budget
discipline. Orca overlay and repo map still choose Orca source files and source
precedence.

## Current Operating Boundary

Orca remains non-implementation unless a later turn explicitly authorizes
implementation.

Architecture work may be future-runtime-aware when the user asks for it. That
means prompts may discuss eventual APIs, scraping, agents, screenshots,
archives, media, or source systems as conceptual requirements, but must not
authorize building, deploying, testing, or operating those systems.

## Orca Start Preflight

Before repo-aware Orca prompt authoring, review setup, handoff creation,
docs-write or overlay maintenance, source-changing work, or completion claims,
record a compact start-preflight receipt. The receipt proves only that the
entrypoint and source-loading route were declared; it does not prove cognition,
validation, approval, readiness, implementation authorization, deployment,
resolver behavior, source-of-truth promotion, or edit permission beyond the
permission value stated in the receipt.

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

## Data Spine CA Read Pack

For a Data Spine setup CA, start with:

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

Do not include method-validation replays, proof-run packets, review outputs,
or research corpus files by default. Use the repo map to decide whether any
one of those is necessary.

### Data Spine CA Capsule Limit

A Data Spine CA prompt should include only:

- one paragraph on Orca's value proposition;
- one paragraph on the current Data/Cleaning/Judgment boundary;
- one paragraph on the non-implementation operating boundary;
- the targeted source pack above;
- the exact files and sections to read;
- the default exclusions;
- the owner decisions or source gaps the CA should surface.

It should not paste the full offer, proof packet, Core Spine contract, boundary
note, or IPF. It should not include method-validation history unless the CA task
explicitly asks how prior cases affected Data Spine source loading.

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
