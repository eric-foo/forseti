# Data Lake v4.1 Silver Vault Delegated Adversarial Artifact Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Repo-mode delegated adversarial artifact review-and-patch commission for the
  Data Lake v4.1 Silver Vault record contract.
use_when:
  - Commissioning a de-correlated controller to stress-test and patch the Silver
    Vault v4.1 contract before treating it as the forward foundation.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
```

## Commission

You are the de-correlated controller for a bounded adversarial artifact
review-and-patch pass. The author/home model family is OpenAI/Codex. The
controller must be a different vendor or model lineage from the author/home
family to claim `cross_vendor_discovery`. This is a who-constraint, not a model
recommendation.

If you cannot record a different controller family, return
`BLOCKED_CONTROLLER_NOT_DECORRELATED` before review or patch work. If you are the
authoring or adjudicating model, do not self-review and do not launch a
same-family substitute reviewer.

This commission uses `repo` access mode. Review the target in the repository,
patch only the submitted target file if needed, write the report path named
below, and leave all changes uncommitted and unstaged for CA adjudication.

Your output is decision input only. The CA/home model decides what is kept.

## Orca Prompt Preflight

```yaml
output_mode:
  prompt_artifact: file-write
  downstream_review: review-report
  delegated_patch: working-tree diff only, uncommitted and unstaged
template_kind: review + bounded patch commission
template_source:
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
edit_permission:
  target_file: patch-only
  report_file: write-only at the named report destination
  all_other_files: read-only / flag-only
workspace:
  path: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\data-lake-v4-1-silver-vault-foundation
  branch: codex/data-lake-v4-1-silver-vault-foundation
target_revision_under_review:
  git_commit: cee573bce811f297940f0f15acb54306fa56ce89
  note: >
    This is the target contract revision under review. The prompt artifact may
    live in a later commit on the same branch; if so, verify the target file hash
    below rather than failing on the prompt-add commit.
target_file_hash:
  path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  sha256: 620E5C91E3B817206E524B7A49C84F17F0F508AF9D3213134DD4FAD76967DC07
dirty_state_allowance: >
  The target file should match the pinned hash before your patch. If it does not,
  return BLOCKED_SOURCE_MISMATCH unless the CA explicitly supplies a newer hash.
doctrine_change: >
  This prompt does not itself change doctrine. It commissions review of a
  doctrine-bearing data lake contract. Any patch that materially changes product,
  architecture, workflow, validation, review, output, or lifecycle doctrine must
  either stay inside the named target's existing scope or return
  NEEDS_ARCHITECTURE_PASS.
fitness_reference:
  goal: >
    Make the Silver Vault v4.1 record contract durable enough to be the forward
    foundation for Orca's semantic Silver layer and client-facing Creator Vault
    read models, without migrating or building runtime code in this pass.
  success_signal: >
    A fresh, de-correlated reviewer can use the contract to identify what records
    go into Silver, what remains raw/bronze or Gold, how source refs and time
    series work, how generated envelopes/read tables relate to authority, and
    what a client carveout may read without creating a dossier or false metric.
```

## Required Method Sequence

1. Read this prompt.
2. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review`.
5. REFERENCE-LOAD `workflow-delegated-review-patch`.
6. Do not APPLY any method yet.
7. SOURCE-LOAD the target and required context below from the repository.
8. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
9. APPLY `workflow-deep-thinking` to frame the boundary problem, failure modes,
   and decision criteria.
10. APPLY `workflow-adversarial-artifact-review` to review the target.
11. APPLY the delegated review-and-patch contract only after source readiness:
    patch only the target file if the defect is patch-level.
12. Fresh-read the changed target file and report path before returning.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after `SOURCE_CONTEXT_READY`, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`
or advisory-only findings. Do not patch and do not emit strict review claims.

## Required Source Context

Required reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`

Pinned context hashes at commission time:

```yaml
source_hashes:
  silver_vault_record_contract: 620E5C91E3B817206E524B7A49C84F17F0F508AF9D3213134DD4FAD76967DC07
  v4_1_forward_epoch_contract: B8FCF9BBDC7F6C88A9DAD9C4D06BF38C16574FD9E5B5434C0B94416D2C2FAD9D
  physicality_location_contract: 54E9059D67D75E4F9280EB3412D92D77099B2A76F6E80FE1BEADFDF0B622BA3A
  medallion_gold_readiness_contract: 5664051651B348959254AE6913F9274EAF67280022B42BBC618BC5A375D4D5EE
  derived_layout_index_rebuild_contract: 6EE1EA42CAF0A86D145A736C0DFBBBE3BCF3456FE0B44D2DE2192B6DE4443E37
```

Optional targeted reads if a finding depends on them:

- `docs/workflows/orca_repo_map_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- Relevant `orca-harness` model or projection files only if the target contract
  makes a claim about an existing concrete implementation field.

Do not bulk-load review outputs, prompts, proof packets, research corpus files,
or all product docs by default.

## Review Target

Editable target:

- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

Read-only / flag-only context:

- Every other file, including the other Data Lake v4.1 contracts.

Report destination:

- `docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_silver_vault_delegated_review_patch_v0.md`

## Review Purpose

Stress-test whether the Silver Vault v4.1 record contract is the right forward
foundation for the semantic Silver layer and generated Creator Vault read
models. Be hostile to anything that would break compounding data capture,
SQL/retrieval, time series, carveout sync, or the Silver/Gold boundary.

Heavily apply:

- Smallest Complete Intervention: patch only what is required for a coherent,
  durable contract; do not broaden into runtime implementation, migration work,
  query-engine selection, or unrelated data-lake refactors.
- Mini God Tier, owner-invoked: push the contract to a high capability bar for
  the first foundation, but require explicit accepted residuals. Do not use MGT
  as validation, readiness, proof, or scope expansion.

## Review Questions

Attack these axes directly:

1. Does the contract preserve the v4.1 decision that physical lake folders are
   `raw/`, `derived/`, and `indexes/`, while medallion words remain semantic
   labels (`raw (bronze)`, `derived (silver-derived)`, `indexes (read models)`)
   rather than extra folder ceremony?
2. Does it keep `raw` untouched and packet-shaped while making Silver authority
   semantic through records, not mutable creator/content envelopes?
3. Does it correctly treat `indexes/` envelopes and query tables as generated
   read models, never source authority?
4. Does the common header include the load-bearing integrity fields:
   `content_hash`, explicit `content_hash_basis`, and `raw_refs` with `sha256`
   plus `hash_basis` where hash-checkable?
5. Are `record_kind`, `payload_kind`, `producer_row_kind`, `entity_key`,
   `relationship_key`, and source refs clear enough to prevent lane taxonomy
   from being frozen into lake paths?
6. Are entity records identity-only, with follower counts, display names, prices,
   availability, handles, captions, transcripts, comments, and all other
   time-varying facts modeled as observations or detail refs?
7. Do metric observations preserve the live posture contract: observed requires
   value and no reason; non-observed requires reason and no value; absence can
   never become observed zero?
8. Does `coverage_window` survive as a first-class requirement for durability,
   spike, and time-series questions?
9. Does the IG grid-primary policy stay enforceable through
   `selection_policy_version`, with per-reel detail capture enriching audio,
   transcript, and comments without overwriting grid metric snapshots?
10. Does the contract preserve live source field names such as
    `source_publication_or_event` and `source_surface_count_candidates` instead
    of inventing parallel vocabulary?
11. Are correction, supersession, invalidation, conflict, and ignore-prior
    modeled as append-only relationship records, with latest/winner status only
    generated in read models?
12. Does the Creator Vault remain a governed generated view over Silver records,
    not a mutable profile, dossier, actor score, Gold judgment, or privacy leak?
13. Does the carveout story work both ways: a client-facing Creator Vault can
    sync from the same Silver records, while full Orca can use that data without
    latency-heavy bespoke requests or duplicate capture as the default?
14. Does the contract make time series queryable through observation records or
    query tables, without hiding missing captures, posture, source surface, or
    policy version?
15. Does it leave query engine selection bounded: SQL/read tables are allowed
    now, graph/vector indexes remain engine-gated unless later selected?
16. Does it correctly exclude campaign/coordination/manufactured-demand judgment
    from Silver v0 while allowing mechanical source evidence that Gold can later
    judge?
17. Does it identify where product, retail, review, SEO, creator, and content
    facts can cross-reference without creating a single overbroad Silver object?
18. Does it avoid migration/runtime claims for the current tiny lake while still
    making the forward epoch unambiguous?
19. Are accepted residuals named well enough for the foundation to be "mini god
    tier but small" without pretending it is maximal?
20. Is there any design-level defect that cannot be patched inside the target
    file without revisiting the v4.1 architecture?

## Patch Boundary

Patch only the editable target file. Patch only defects that materially affect
the Silver Vault v4.1 foundation, source integrity, posture semantics, time
series, generated read models, Creator Vault carveout, or Silver/Gold boundary.

Do not edit:

- other Data Lake v4.1 contracts;
- overlay files;
- prompts other than this prompt;
- review outputs other than the named report destination;
- runtime code, lake data, migration scripts, SQL implementation, graph/vector
  engine decisions, capture runners, or `orca-harness` files.

If the correct fix requires changing the v4.1 architecture, medallion boundary,
query-engine decision, capture-runner behavior, or any off-target contract,
return `NEEDS_ARCHITECTURE_PASS` with findings only. Do not patch around a
broken design.

## Required Validation

For this artifact pass, validation means document and repository hygiene, not
runtime tests.

Run after any patch, or state why it could not be run:

```powershell
git diff --check
```

Also fresh-read:

- the patched target section(s);
- the report file after writing it;
- `git diff --stat`;
- `git status --short --branch`.

Do not run live capture, network capture, data migration, data deletion, or lake
archive commands.

## Output Contract

Write the human-readable review report to:

`docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_silver_vault_delegated_review_patch_v0.md`

The report must include:

1. Actor receipt:
   - `authored_by`: OpenAI/Codex family; exact model/version `unrecorded` unless
     operator supplies it.
   - `reviewed_by`: operator/tooling-supplied; use `unrecorded` if not supplied.
   - `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or
     `self_fallback`.
   - `controller_model_family`: recorded family or `unrecorded`; if not
     different from OpenAI/Codex, do not claim cross-vendor discovery.
2. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
3. Findings first, ordered by severity: `critical`, `major`, `minor`.
4. For each finding:
   - target location;
   - evidence with source citation;
   - impact;
   - minimum closure condition;
   - whether you patched it.
5. Patch summary, if any.
6. Unified diff, if any.
7. Validation command and observed output, or not-run reason.
8. Accepted residuals and remaining risk.
9. Verdict: `PATCHED_FOR_CA_ADJUDICATION`,
   `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, or
   `BLOCKED`.

Then return a compact courier message in chat:

```yaml
review_summary:
  status: completed | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_silver_vault_delegated_review_patch_v0.md
  recommendation: PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_NEEDED_FOR_CA_ADJUDICATION | NEEDS_ARCHITECTURE_PASS | BLOCKED
  summary: "<one paragraph>"
  next_action: "<what CA should adjudicate next>"
```

Reminder: your diff, citations, and verdict are claims to adjudicate, not
premises to inherit. The CA/home model decides what is kept and may reject any
patch even if individually defensible.
