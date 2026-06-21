# Data Lake Physicality Location + Data Root — MGT / SCI Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: >
  Cross-recipient architecture prompt for deciding Orca's Data Lake physical
  location boundary: repo-vs-operational-data separation, ORCA_DATA_ROOT, local
  data-root directory grammar, packet_id-addressed raw layout, append-only
  derived/acknowledgement records, rebuildable indexes, and accepted residuals
  under Mini God Tier plus Smallest Complete Intervention.
use_when:
  - Asking an external model or architecture lane to stress-test the physical data-root direction.
  - Preparing a later Data Lake physicality decision contract.
  - Checking whether a proposal selects too much physical backend/runtime machinery too early.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - .gitignore
source_base_revision: codex/data-lake-medallion-contract @ ffb22cae
prompt_branch: codex/data-lake-physicality-location-prompt
checkout_requirement: >
  Strict repo-read claims require a checkout that contains this prompt's named
  source base, especially the medallion gold-readiness contract. If the
  medallion contract is absent, first classify whether the checkout is missing
  the stacked source before treating the contract as absent from Orca.
input_hashes:
  docs/decisions/orca_mini_god_tier_doctrine_v0.md: 76B624FA1173ADDDE7F8FF1A7B09C5495723D9DD3523588B42E06EA93634B68F
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md: 4C2B4033B02F508CAB3AE73BBB8B7BB4B6ECF7B1F8714384F35E4A75442CAA78
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md: C19C4817747DB1839AD6CD5665FA863B92A64F81CB2DA71429672D0252D1E85F
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md: 5664051651B348959254AE6913F9274EAF67280022B42BBC618BC5A375D4D5EE
  .gitignore: 147AD46B344DA41B78F3C05D8CC4BF9A836D483F38FE8BBA391ABA160B8FF59D
```

## Orca Prompt Preflight

```yaml
output_mode: paste-ready-chat
prompt_artifact_path: docs/prompts/architecture/data_lake_physicality_location_mgt_sci_prompt_v0.md
receiver_output_mode: chat-only architecture report
receiver_write_permission: read-only; no repo edits; no implementation; no backend/runtime selection
template_kind: full-prompt; architecture-planning style; no model-specific template
template_source: Orca local architecture prompt style + prompt-orchestration overlay
edit_permission_targets_branch: >
  Receiver is read-only. This filed prompt artifact is docs-only on
  codex/data-lake-physicality-location-prompt, stacked on
  codex/data-lake-medallion-contract.
reviews: not a formal review prompt; findings-first risk section still required
doctrine_change: >
  Receiver may recommend wording for a later physicality decision contract but
  must not claim the doctrine is changed by this prompt or by its answer.
destinations: >
  Prompt artifact is this file. Receiver returns a chat report for owner/Codex
  adjudication; no durable output path is required unless separately requested.
```

## Task

You are evaluating Orca's Data Lake **physicality location** direction through two lenses:

1. **Mini God Tier (MGT):** capture most of the useful physical-data organization now, with named accepted residuals, without pretending this is validated/readiness/production proof.
2. **Smallest Complete Intervention (SCI):** lock only the minimum durable architecture decisions needed to prevent bad physical drift; do not select a storage engine, queue, scheduler, cache, runtime, migration, or implementation plan unless explicitly required for the location decision.

Decide whether the following owner-proposed location direction should be accepted as Orca's v0 physical data-root target, accepted with changes, rejected, or blocked:

```text
Real Orca data should not live in the Git repository.

Use a separate data root, preferably on the HDD:

C:\src\orca\          # Git repo: code, schemas, contracts, tests
D:\orca-data\         # Operational data
  raw\
  attachments\
  derived\
  acknowledgements\
  indexes\

Point the repo to it through configuration, such as:

ORCA_DATA_ROOT=D:\orca-data

The repo should only contain small test fixtures and example manifests. Orca's
existing .gitignore already treats captures, test runs, scores, reports, and
logs as local/generated state rather than source-controlled material.

A packet_id-addressed layout under D:\orca-data\raw\ is a sensible eventual
shape; raw stays immutable, derived records stay append-only, and indexes remain
rebuildable.
```

Important clarification: treat `C:\src\orca\` as an illustrative repo path, not a claim that the current checkout must move there. The current user's repo may live elsewhere. The architecture question is the boundary: **Git repo for code/contracts/tests; external data root for operational data.**

## Source Read Contract

If you have repository/filesystem access, first confirm the checkout contains the named source base or a descendant/equivalent revision. Then read the named source files above before making strict claims. Confirm hashes when possible. If a hash differs, report drift and reason from the current file content you read.

If the medallion gold-readiness contract is absent, do not immediately infer that Orca lacks the contract. First check whether the checkout is missing the stacked source. If the checkout does not contain the named source base, set `source_readiness: PARTIAL_REPO_READ_STACK_MISMATCH`, treat medallion-specific claims as capsule-backed, and state that strict repo-grounding requires the stacked source.

Use one `source_readiness` value:

- `FULL_REPO_READ` — required files were read from a checkout containing the named source base; hash drift, if any, is explained from current content.
- `PARTIAL_REPO_READ_STACK_MISMATCH` — repo access exists, but the checkout does not contain one or more stacked prompt sources; distinguish checkout mismatch from source absence.
- `CAPSULE_ONLY` — no repo/filesystem access; cite capsule sections only.

`MovementCandidateRecord` and `GoldReadyAssemblyReceipt` are proposed physicality names for logical-home analysis, not claims that repo classes already exist. Do not downgrade the architecture solely because grep finds no current code or docs using those names.

If you do not have repo/filesystem access, use only the source capsule below. In that case:

- set `source_readiness: CAPSULE_ONLY`;
- do not invent file:line citations;
- cite capsule section names instead;
- state which claims would require repo confirmation before becoming strict.

Do not browse the web. Do not use external architecture fashion as authority. This is an Orca-local architecture decision.

## Source Capsule

### A. Mini God Tier Doctrine

MGT is owner-invoked only. It chooses the capability target, not scope expansion. It requires accepted residuals: the foregone part of maximal capability must be named, bounded, justified, and given upgrade triggers. MGT is not validation, readiness, proof, or build authorization. SCI still governs the intervention: minimal complete step, lower lock-in when two complete options both work.

### B. Data Lake Core Contract

The Data Lake preserves raw `SourceCapturePacket` truth, stable packet/slice/file handles, hashes, manifests, and by-key availability. It owns by-key findability and logical attachment points for downstream derived results. It must not own Cleaning, ECR, SCR interpretation, Judgment, canonical identity, source value, queueing, scheduling, retry, orchestration, or downstream calls. Raw bytes/hashes/packet identity are not rewritten by derived lanes.

### C. Data Lake Storage Contract

The lake has five dumb record-kind slots:

- Raw Packet Store;
- Attachment Record;
- Availability Index;
- Derived Result Store;
- Acknowledgement Log.

Availability Index is content-free committed/readable-by-key state, not an analytical reverse index, event bus, scheduler, router, priority system, or success tracker. Derived Result Store holds append-only lane-owned derived records keyed to raw. Acknowledgement Log holds append-only lane-owned completion/ack facts keyed to raw. Physical backend, exact layout, serialization, manifest version, cache, queue, scheduler, runtime, migration, validation, and readiness remain deferred.

### D. Medallion Gold-Readiness Contract

Bronze is raw capture. Silver is projection/ECR/SCR/Cleaning/mechanical derived features. Pre-gold is mechanical movement candidates such as Spike/Movement Alerts. Gold-ready is decision-bounded evidence assembly. Gold is Judgment-only. Candidate records and evidence assemblies are non-Judgment, append-only, keyed to raw, and must not claim botting, fake review, paid activity, coordination, manipulation, virality, credibility effect, exclusion, Signal Integrity, Signal Use, Decision Strength, or Action Ceiling.

Before implementing Spike Alert records, blockers remain: physical home and write boundary for derived records and assembly receipts; derivation owner; profile/version contract; allowed source-family identifier scopes; access/audit/retention guardrails for actor-related retrieval.

### E. `.gitignore` Observed Boundary

The repo ignores local/generated state including logs, scratch, test runs, auth/proxy/credential folders, source capture reports, scores, and memory logs. This supports the proposed boundary that operational data should not become source-controlled material, while small fixtures/examples may remain in repo.

## Questions To Answer

1. Should Orca accept the external data-root boundary as a v0 physicality decision?
2. Is `ORCA_DATA_ROOT=D:\orca-data` the right level of commitment, or should the contract say `ORCA_DATA_ROOT=<operator-configured external data root>` with `D:\orca-data` as the local preferred example?
3. Should the first directory grammar be exactly `raw/ attachments/ derived/ acknowledgements/ indexes/`, or should any slot be renamed/split/deferred? In particular, should `indexes/` be internally split into content-free availability versus rebuildable derived retrieval subslots?
4. What does each directory own, and what must each directory not become?
5. Where should proposed `MovementCandidateRecord`, proposed `GoldReadyAssemblyReceipt`, lane-owned derived retrieval artifacts, and passive availability facts logically live under that root, and what naming prevents derived retrieval from becoming lake authority?
6. Should `D:\orca-data\raw\<packet_id>\...` be locked now as an eventual shape, or only as a recommended layout pending packet-admission/key-rule decisions?
7. What minimum configuration contract is needed now: env var only, config file fallback, per-run override, test-fixture override, or something else?
8. What must stay in the Git repo: schemas, contracts, tests, small fixtures, example manifests, config templates? What must never be committed?
9. What accepted residuals make this MGT rather than overbuilt maximal infrastructure?
10. What blockers must remain before implementation: admission criteria, packet/slice/object/event key rules, retention, access/audit, write-once enforcement, index rebuild command, migration/replay policy, or other?

## Required Analysis Discipline

- Push back hard on any phrase that leaks Judgment or gold semantics into physical storage.
- Push back hard on any physical layout that creates a hidden actor/profile/dossier system.
- Keep Availability Index content-free.
- Keep analytical reverse lookups as lane-owned rebuildable derived retrieval artifacts, not lake authority.
- If `indexes/` contains both availability and derived-retrieval artifacts, require explicit subslot naming or equivalent wording that keeps content-free availability separate from analytical derived retrieval.
- Prefer a simple filesystem root and config boundary if it satisfies MGT; do not escalate to a database/object-store architecture unless the source facts force it.
- Distinguish **location contract** from **storage engine**. A directory grammar may be acceptable even while backend/serialization remain deferred.
- Distinguish **eventual shape** from **implementation-ready schema**.

## Output Contract

Return a concise architecture report with these exact headings:

1. `source_readiness`
2. `verdict` — one of `ACCEPT`, `ACCEPT_WITH_CHANGES`, `REJECT`, `BLOCKED`
3. `one_screen_recommendation`
4. `physical_root_contract`
5. `directory_slot_contract`
6. `record_home_mapping`
7. `configuration_contract`
8. `git_boundary`
9. `risks_and_pushback`
10. `mgt_accepted_residuals`
11. `implementation_blockers`
12. `contract_wording_patch`
13. `non_claims`

For every strict recommendation or contract wording change, include source citations: `file:line` when repo access exists, or capsule section names when repo access is unavailable.

For `record_home_mapping`, include at least:

- Raw Packet Store;
- Attachment Record;
- Availability Index;
- Derived Result Store;
- Acknowledgement Log;
- proposed MovementCandidateRecord;
- proposed GoldReadyAssemblyReceipt;
- lane-owned derived retrieval artifacts for commenter/reviewer timing questions.

For `contract_wording_patch`, provide paste-ready wording for a later Orca decision contract. Keep it implementation-neutral.

## Forbidden Outputs

Do not produce:

- backend/storage-engine selection;
- queue/scheduler/runtime design;
- migration script or implementation plan;
- actor/person profile design;
- cross-platform identity resolution;
- bot/fake/paid/coordinated/credibility labels;
- a claim that this is validated, ready, production-fit, or approved for implementation;
- instructions to move the Git repo to `C:\src\orca\`.

## Expected Starting Bias

The likely correct answer is `ACCEPT_WITH_CHANGES`:

- accept external operational data root;
- prefer `ORCA_DATA_ROOT=<operator-configured external data root>` with `D:\orca-data` as the owner's local default/example;
- accept the five-directory grammar as a v0 logical data-root grammar;
- treat `attachments/` as a logical slot while deferring whether attachment bodies are sibling files or packet members;
- lock raw immutable, derived/ack append-only, indexes rebuildable;
- split or explicitly label `indexes/` so content-free availability cannot be confused with rebuildable derived retrieval;
- require fail-closed data-root resolution when the configured root is unset, unresolvable, or inside the repo;
- keep packet_id-addressed raw layout as target direction, but gate final path grammar on packet-admission and key-rule decisions;
- reject any wording that says candidate/receipt records are existing code classes, gold, Judgment, actor profile, or analytical truth in the Availability Index.

You may disagree, but if you do, explain the decisive source-backed reason.
