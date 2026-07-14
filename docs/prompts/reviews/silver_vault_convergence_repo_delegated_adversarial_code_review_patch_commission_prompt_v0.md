# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Silver Vault Convergence (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready commission for a de-correlated adversarial code review and
  bounded patch of the official-Silver convergence implementation pinned below.
use_when:
  - Dispatching the Silver convergence implementation to an independent repo-capable controller.
  - Re-dispatching unchanged after confirming the implementation commit remains an ancestor of branch HEAD.
authority_boundary: retrieval_only
```

## What this is for

**Goal:** ensure product mentions and quote-backed TikTok audience evidence are
written and read as official Silver facts, while synthesized audience profiles
remain non-authoritative analysis and historical records remain immutable.

**Done looks like:** every current producer and reader uses the new
envelope-valid lanes, reruns remain idempotent, old records remain audit-readable
but cannot become current authority, and malformed lineage/hash/policy records
fail visibly without any live-lake write or recapture.

This goal and signal are the controller's review axis to attack, not a pass bar.

## Forseti start preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0
forseti_start_preflight:
  agents_md_read: yes
  overlay_readme_read: yes
  authorization_basis: owner-invoked fused implementation turn for Part 2 plus its required review-routing checkpoint
  workspace_or_repo: C:/Users/vmon7/.codex/worktrees/f75f/orca
  isolation_decision: branch off fresh origin/main for the bounded implementation work
  branch_or_commit_reference:
    branch: codex/silver-vault-convergence
    base_commit: 3b41ca9853b5ebf72fc37075d050494d35ddf00d
    implementation_commit: cd636b68fd7e2f8bf9caf633e758353494127800
    semantics: review the exact base..implementation diff; a later prompt-only descendant is allowed
  dirty_state_allowance: receiver starts clean; only the named target set may become modified
  untracked_files_in_scope: no
  controlling_source_state: overlay and prompt-policy sources clean at implementation commit; implementation target is pinned
  source_pack: bounded custom pack named in this prompt
  repo_map_decision: not_needed
  repo_map_reason: exact target files and controlling contracts are named; no repository route, owner, or artifact family moved
  receiver_mechanism: operator-couriered independent repo-mode controller
  receiver_write_root_capability: operator_to_fill_and_verify_before_dispatch
  edit_permission: patch-only
  output_mode: paste-ready-chat
  template_kind: review plus explicitly commissioned bounded patch
  template_source: project overlay delegated_code_review_and_patch target kind plus workflow-code-review
  doctrine_change_decision: no workflow/review doctrine change; verify the implementation's Silver authority-contract propagation within the named docs
  validation_evidence_at_dispatch:
    - full forseti-harness suite exited 0 at implementation commit (224.7 seconds)
    - strict Silver lane registry guard exited 0
    - git diff --check exited 0
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: null
```

The operator must verify the receiving controller can write the commissioned
worktree/branch before dispatch. If it cannot, stop with
`BLOCKED_RECEIVER_REROOT_REQUIRED`; discovering a path is not write capability.

## Paste-ready commission

````markdown
You are the independent controller for a REPO-MODE DELEGATED ADVERSARIAL CODE
REVIEW AND BOUNDED PATCH. The author/home model is OpenAI GPT-5-family. You must
be from a different upstream vendor/model lineage. This is a who-constraint,
not a model recommendation. Before reviewing, record:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI GPT-5-family
  controller_model_family: <your actual family or unrecorded>
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied | blocked
```

If your family is OpenAI/GPT lineage, unknown, or cannot be disclosed, return
`BLOCKED_DECORRELATION` and do not review or patch.

### Repository preflight

- Worktree: `C:/Users/vmon7/.codex/worktrees/f75f/orca`, or the operator-verified
  worktree rooted on `codex/silver-vault-convergence`.
- Base: `3b41ca9853b5ebf72fc37075d050494d35ddf00d`.
- Exact implementation revision:
  `cd636b68fd7e2f8bf9caf633e758353494127800`.
- Review `base..implementation revision`. A later descendant containing only
  this commission prompt is allowed. Do not review a substitute checkout,
  context summary, or recreated source.
- Start clean. If the branch/revision, cleanliness, or verified write-root
  capability does not match, return the nearest explicit blocker and stop.

### Authority and method order

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD, without applying yet:
   - `workflow-code-review`;
   - `.agents/workflow-overlay/delegated-review-patch.md`, targeted sections
     “The loop”, “Delegate lifecycle hard stop”, “De-correlation”,
     “Code-diff target kind”, and “Adjudication closeout”;
   - `.agents/workflow-overlay/prompt-orchestration.md`, targeted sections
     “Source-Gated Method Contract” and “Review Prompt Defaults”.
3. SOURCE-LOAD the exact diff, every named target, and the controlling sources
   below. Record `full`, `targeted <section>`, `grep <token>`, or `skip: <reason>`
   for each source.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. Do not produce
   findings, a verdict, or patches before that declaration.
5. APPLY `workflow-code-review` to the loaded source context. If unavailable,
   return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

Do not apply a deep-thinking method: this is a bounded technical code review
with an exact revision, file set, authority, and validation route.

### Review target and patch boundary

These are the only patchable files; every finding, citation, and diff hunk must
carry the applicable label. Everything else is read-only/flag-only.

- `[front-door]`
  - `.agents/hooks/check_silver_lane_registry.py`
  - `forseti-harness/data_lake/silver_record.py`
  - `forseti-harness/data_lake/lane_registry.py`
  - `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json`
- `[product-producer]`
  - `forseti-harness/cleaning/transcript_product_lake.py`
  - `forseti-harness/runners/run_transcript_product_extract.py`
  - `forseti-harness/runners/run_tiktok_product_extract.py`
  - `forseti-harness/runners/run_ig_reels_product_extract.py`
  - `forseti-harness/runners/run_ig_reels_operator_product_extract.py`
- `[audience-producer]`
  - `forseti-harness/cleaning/tiktok_audience_evidence_lake.py`
  - `forseti-harness/runners/run_tiktok_audience_evidence_extract.py`
- `[readers]`
  - `forseti-harness/data_lake/derived_retrieval_views.py`
  - `forseti-harness/data_lake/sov_readout.py`
  - `forseti-harness/runners/run_sov_extraction_quality_eval.py`
- `[tests]`
  - `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - `forseti-harness/tests/contract/test_policy_module_version_pins.py`
  - `forseti-harness/tests/test_data_lake_indexes_rebuild.py`
  - `forseti-harness/tests/test_data_lake_sov_readout.py`
  - `forseti-harness/tests/test_sov_extraction_quality_eval.py`
  - `forseti-harness/tests/unit/test_ig_reels_operator_product_extract.py`
  - `forseti-harness/tests/unit/test_ig_reels_product_extract.py`
  - `forseti-harness/tests/unit/test_silver_lane_registry_guard.py`
  - `forseti-harness/tests/unit/test_silver_record.py`
  - `forseti-harness/tests/unit/test_tiktok_product_extract.py`
  - `forseti-harness/tests/unit/test_transcript_product_lake.py`
  - `forseti-harness/tests/unit/test_youtube_caption_product_extract.py`
- `[authority-docs]`
  - `docs/decisions/silver_vault_legacy_record_convergence_v0.md`
  - `forseti/product/spines/data_lake/README.md`
  - `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`
  - `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md`
  - `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md`

Why read-only review is insufficient: confirmed implementation defects inside
this set should be corrected in the same de-correlated pass and validated before
the home model adjudicates. Patch only confirmed defects and make the smallest
complete correction. Do not widen the schema or architecture.

### Controlling sources and frozen decisions

Read and judge the target against:

- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_contract_v0.md`;
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`;
- `docs/decisions/silver_vault_legacy_record_convergence_v0.md`;
- `forseti-harness/data_lake/root.py` and
  `forseti-harness/data_lake/silver_lineage.py` (read-only);
- the exact implementation diff and tests.

Frozen decisions:

- Official fact lanes are `transcript_product_mentions_silver` and
  `tiktok_audience_evidence_silver`.
- Synthesized audience profiles are non-authoritative analysis, not Silver
  Authority.
- Historical grammar-B records remain append-only and audit-readable; no rewrite.
- Current readers select official lanes only; no legacy fallback.
- New output schema versions make old acknowledgements re-surface for
  re-derivation without recapture.
- Common Silver validation covers header, lineage/reference shape, content
  hash/basis, policy fingerprinting, write-target binding, and validates all set
  members before publication.
- Preserve idempotency, completion-before-acknowledgement, and second-cycle-zero.
- No live data-lake writes, platform recapture, Creator Registry mutation,
  automatic LLM cadence, or Gold/Judgment claims.

### Adversarial checks

Be coverage-first and report every issue found with `critical|major|minor`
priority and `high|medium|low` confidence. In particular, attack:

- whether any producer can bypass the validating Silver front door or publish a
  completion marker after a partial/invalid member write;
- whether content hashes and policy fingerprints are canonical, deterministic,
  and actually verified on both write and read paths;
- whether exact transcript/comment quote citations and raw/derived lineage are
  sufficient and fail closed;
- whether schema-version obligation changes reliably re-surface old anchors and
  preserve rerun idempotency/second-cycle-zero;
- whether any current reader, SoV/index builder, operator packet, or quality
  evaluator still reads or reports the retired grammar-B authority;
- whether audience profile records can accidentally masquerade as Silver facts;
- whether zero-row evidence sets, malformed rows, equal identities, or partial
  record sets create fake success or silent loss;
- whether the lane registry, guard, inventory, docs, and tests agree on roles,
  completions, and retirement semantics.

For every actionable finding provide: label, severity, confidence, file:line,
issue, decision-sufficient neutral evidence, impact,
`minimum_closure_condition`, and `next_authorized_action`. Put defeated
candidates in `considered_and_defended`. Optional hardening must be explicitly
optional and non-required.

### Bounded patch and validation

Patch only confirmed defects inside the named set. If the correct fix requires
an unlisted file, a new architecture/schema decision, live-lake mutation, or
scope expansion, do not edit: return `NEEDS_ARCHITECTURE_PASS` or an off-scope
finding and leave no partial patch.

After any patch, run at minimum:

```powershell
python .agents/hooks/check_silver_lane_registry.py --strict
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest_silver_review forseti-harness/tests
git diff --check
```

Report actual exit status and output summary. If a command is not run, say
`not_run` with the reason. Never translate failure or not-run into success.

### Return contract and hard stop

Return, in order:

1. actor/model receipt, source-read ledger, and readiness declaration;
2. findings first, plus `considered_and_defended`;
3. bounded unified diff with labeled hunks and per-change neutral citations;
4. validation evidence with pass/fail/blocked/not-run semantics;
5. verdict and residual-risk note;
6. `reviewed_by` and `authored_by` (`unrecorded` is allowed; never fabricate);
7. adjudicator note: the diff, citations, verdict, and test claims are claims to
   adjudicate, not premises to inherit. The home/CA accepts, modifies, or rejects
   each change and may veto any change before keep, then follows
   `.agents/workflow-overlay/communication-style.md` → “Review Adjudication Next Step”.

Do not commit, push, open/update a PR, merge, stash, reset, clean a worktree, run
repo hygiene, write a durable review report, or edit outside the named target.
Your output is decision input only: no approval, readiness, acceptance, or
go-live claim.
````

## Dispatch status

- `prompt_verdict: PASS_WITH_WARNINGS`
- Warning: the operator must fill and verify the independent controller's
  model-family receipt and actual repo write root before dispatch.
- Output destination: controller returns findings/diff in chat; the operator
  couriers the full return to the home/CA for adjudication.
- No durable review report is commissioned.
