# Company Surface Logical-Record Success Signals Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial artifact review-and-patch prompt
scope: >
  Operator-couriered, de-correlated review-and-patch commission for the
  Company Surface logical-record success signals and their cold-agent front
  door. The two submitted files are the only patchable product artifacts;
  every other source is read-only or flag-only context.
use_when:
  - Launching the fused post-implementation review of the Company Surface logical-record success signals.
  - Testing whether a cold agent can use the Company Surface front door and owning contract without inheriting chat or review conclusions.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - forseti/product/information/company_surface/README.md
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
input_hashes_sha256_worktree:
  company_surface_readme: 1F84F2710CAC21A246826606A549B537A31654C9646B03D81C2953AE1CE6BFE7
  company_logical_record_and_view_contract: C5946B9DF2038F7960AABBEA11A4F1D6F1E16D0E705B9BD5FA9E703293BB648F
  company_surface_purpose_contract: E85068DA1718D5743DBE1DD7CDAF2D86101721A031275D38200A8B1F0790FA0C
  company_identity_boundary: C1EBAD7C27F0A71C430CB5194C2E6F9142632A82140282001035E7F8414AC019
  corpus_intake_contract: 3F79570AB5E547751B05C3CE2565FD43ED5EEC4589E5AF75EE9195FC9A9C9140
  silver_vault_record_contract: 0B9447AFC434551D1AC543C722EB026DA166130ABC8770B134A21794B4108696
  foundation_ontology: 5288C0E98D40F294E67F5FA78C0EAF2831AA2C208361A4B2F90E72DCD33D2C71
  foundation_ontology_backbone: B8152A0E7CB73BE2D3DCD0312A37027A3B897F251A290BA64B3693D978B9B913
  delegated_review_patch_overlay: A9369F8B4D7F641971E0C13B92B9CC9B8F3EF2D2A6AC2F1FB4E98BC97A364EFB
  review_lanes_overlay: 099FDDE09E721A827C98B085767815AA6974543E464FDBD30A2504B1C0ABBFE6
  prompt_orchestration_overlay: C7E86A38653567F27899A2BC4C1DDC969EA87FD22E9226C0507535B94063FC8C
  adversarial_artifact_review_template: B3186C622A4C2C386AB0110F8164414A26F880E95A5E9789FC7D0EC873DAD41F
target_git_blobs_index:
  company_surface_readme: f19a1bfb32e59b1741e502aac535280897cc2f6c
  company_logical_record_and_view_contract: eba46ca258ed79ae6964f60aeab7bea5bd75efd5
branch_or_commit:
  branch: codex/company-surface-logical-record-success-signals
  pre_prompt_head: c294927f685173eec4bfe9f2c06fc87010899264
  origin_main_observed_at_prompt_authoring: 3bb7e6f531758df93d8f88c8c6c0bf332e91493c
stale_if:
  - Either submitted target Git blob differs before review begins.
  - A load-bearing controlling-source hash differs and the changed source bears on a finding or non-finding.
  - The receiving controller is the same vendor/family as the OpenAI/GPT author lane while claiming de-correlated discovery.
  - The named branch or worktree no longer contains the submitted change.
```

## Prompt Status

Status: `ROUTE_OUT_PROMPT_OPERATOR_FIELDS_TO_FILL`.

This is the rendered prompt required by the fused recommended-review
checkpoint. It does not run the review, keep a patch, validate the contract,
or authorize implementation. The operator couriers it to a different-family
controller and later returns the controller's report and uncommitted diff to
the OpenAI/GPT home lane for adjudication.

```yaml
operator_to_fill:
  controller_model_family: ""
  reviewed_by_value_for_report: ""
  controller_report_destination_confirmed: yes | no
```

## Binding Receipt

```yaml
delegated_review_patch_overlay_interface:
  status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  protected_path_list: .agents/workflow-overlay/safety-rules.md
  model_ladder: operator-owned; no concrete controller model is selected here
  prompt_orchestrator_available: yes; full fused prompt contract applied
  access: repo
  mode: base-subagent
  source_context_fields: .agents/workflow-overlay/prompt-orchestration.md
  output_destinations:
    delegate_return: durable report plus uncommitted bounded target diff or explicit no-patch result
    durable_review_report: docs/review-outputs/adversarial-artifact-reviews/company_surface_logical_record_success_signals_delegated_adversarial_review_patch_v0.md
    patch_application: the two submitted target files only; home-model adjudication before keep
```

The convention is provisional and opt-in. The prompt is strict about receipt,
source loading, scope, and output shape; it creates no formal Forseti review
lane, validation, readiness, or automatic keep authority.

## Launch Prompt

````text
You are the controller for a Forseti delegated adversarial artifact
review-and-patch commission.

This is `workflow-delegated-review-patch` in `base-subagent`, `repo` mode.
De-correlation is a who-constraint, not a model recommendation. Do not add a
Recommended model block or rank models.

### Actor / Model-Family Receipt Gate

Before reading the targets, complete this with actual facts:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT-family Codex lane
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: repo
  de_correlation_status: satisfied | blocked
```

If the controller family is missing, undisclosed, ambiguous, or OpenAI/GPT,
stop before review with `BLOCKED_CONTROLLER_NOT_DECORRELATED`. You are already
the controller: do not launch a replacement controller or recursive reviewer.

### Forseti Prompt Preflight

```yaml
forseti_start_preflight:
  agents_read: required_before_review
  overlay_read: required_before_review
  workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\company-surface-logical-record-success-signals
  expected_branch: codex/company-surface-logical-record-success-signals
  branch_reference: verify current branch; target Git blobs below are decisive
  source_pack: bounded Company Surface logical-record success-signal pack
  repo_map_decision: not_needed; Company Surface README is the commissioned cold-agent entry point
  output_mode: review-report plus bounded uncommitted patch
  edit_permission: patch only the two submitted targets and write the one report
  doctrine_change_decision: local clarification only; off-target doctrine change requires NEEDS_ARCHITECTURE_PASS
  isolation_decision: use this existing review target worktree; do not create or switch branches or worktrees
```

Fail loud if the worktree, branch, target Git blobs, or dirty-state allowance does
not match. The branch may have a later commit because this prompt is committed
with the target. Proceed only when both target Git blob IDs match:

- `[logical-record-contract]`
  `forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md`
  — `eba46ca258ed79ae6964f60aeab7bea5bd75efd5`
- `[company-surface-front-door]`
  `forseti/product/information/company_surface/README.md`
  — `f19a1bfb32e59b1741e502aac535280897cc2f6c`

Expected dirty state at review start: clean. Your only permitted writes are
the two submitted targets and the report path below. Do not stage, commit,
push, open or modify a PR, or perform branch operations.

### Source-Gated Method Contract

Read first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

REFERENCE-LOAD `workflow-delegated-review-patch` and
`workflow-adversarial-artifact-review`; do not apply either before source
readiness. Then fully read both submitted targets plus:

- `forseti/product/information/company_surface/purpose_contract_v0.md`
- `forseti/product/information/company_surface/company_identity_boundary_v0.md`
- `forseti/product/spines/foundation/ontology/ontology.yaml`
- `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md`
- `forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md`
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

Declare `SOURCE_CONTEXT_READY` only after the target Git blobs and load-bearing
sources are confirmed. If a necessary source is unavailable or stale, return
`SOURCE_CONTEXT_INCOMPLETE` or the precise preflight blocker; do not substitute
chat, review history, summaries, or another checkout. After readiness, APPLY
`workflow-adversarial-artifact-review`, then apply this commission's bounded
patch rules.

### Objective And Fitness Reference

Adversarially decide whether the ten logical-record success signals and the
cold-agent reference check are the smallest complete, source-faithful
acceptance bar for later Company Surface mapping or implementation.

The core success condition is not that the prose sounds sensible. A fresh
agent starting at the README must be able to recover authoritative records
versus rebuildable views; layer ownership; uncertainty, time, coverage,
correction, and lineage obligations; blocked/deferred decisions; and the next
bounded mapping decision—without inventing schema, a producer, a Silver fit,
Org graduation, evidence readiness, or GTM meaning.

Treat that fitness reference as an axis to attack, not a promised pass result.

### Review Questions

1. Does every LRS signal follow from the purpose, identity, Foundation,
   Capture-rebind, and Silver authorities, or does any signal invent policy?
2. Are the signals record-specific and observable enough to reject a bad
   future mapping, rather than merely restating aspirations?
3. Does LRS-01 allow unresolved/provisional entry without fabricating a Silver
   entity while preserving Brand-versus-Org and the Org graduation gate?
4. Do LRS-02, LRS-03, and LRS-08 preserve reference-not-copy lineage and stop
   persistence or resolved identity from laundering evidence readiness?
5. Do LRS-04 through LRS-06 make append-only correction, two-dimensional time,
   and coverage gaps falsifiable without prescribing a physical schema?
6. Does LRS-07 accurately express the unresolved Data Lake mapping seam, or
   does it overclaim a deterministic raw-anchor rule, producer obligation,
   Silver incompatibility route, or amendment policy?
7. Does LRS-09 prevent a parallel registry/dossier while still allowing
   source-family-specific Capture routes and future lawful extensions?
8. Can LRS-10 and the five-question cold-agent check actually be completed
   from the README and routed owning sources, with no hidden dependence on
   this prompt, a PR, a review report, or authoring chat?
9. Does the new section conflict with or duplicate the existing nine
   purpose-level success signals and acceptance conditions?
10. Are the DCP receipt, non-claims, intentionally-not-updated list, retrieval
    header, and README routing truthful after the edit?
11. What is the highest-risk plausible false positive: a future agent declares
    the record contract satisfied even though ownership, uncertainty,
    evidence status, or physical compatibility has silently failed?
12. Is any necessary correction design-level or off-scope, requiring
    `NEEDS_ARCHITECTURE_PASS` rather than a local wording patch?

### Bounded Patch Scope

- Patch only `[logical-record-contract]` and
  `[company-surface-front-door]`, directly in the working tree.
- Permitted changes are the smallest complete wording, ordering, retrieval,
  source-citation, acceptance-condition, DCP-receipt, or non-claim corrections
  justified by findings about the added success signals and cold-agent route.
- Do not add serialized schemas, canonical IDs, producer implementations,
  storage paths, materialized views, Silver amendments, Org vocabulary,
  Company Surface runtime, GTM policy, outreach logic, or readiness claims.
- All other files are read-only and flag-only. Do not patch overlays,
  Foundation, Capture, Data Lake, GTM, repo maps, prompts, tests, or code.
- Every finding, citation, and diff hunk must carry either
  `[logical-record-contract]` or `[company-surface-front-door]`.
- On a design-level problem, return `NEEDS_ARCHITECTURE_PASS`, revert partial
  target edits, and return findings only.
- The controller's citations, diff, and verdict are claims for the OpenAI/GPT
  home lane to adjudicate, not premises to keep automatically.

### Required Validation

After any patch, run or give an explicit not-run reason:

```powershell
git diff --check
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\check_dcp_receipt.py --changed --strict
python .agents\hooks\check_dcp_receipt_hygiene.py --changed --strict
python .agents\hooks\header_index.py --strict --base origin/main
```

Fresh-read both targets, the written report, `git diff --stat`, and
`git status --short --branch`. Do not run product/runtime tests, captures,
network probes, migrations, or storage writes.

### Output Contract

Write the durable report to exactly:

`docs/review-outputs/adversarial-artifact-reviews/company_surface_logical_record_success_signals_delegated_adversarial_review_patch_v0.md`

The report must contain:

1. the completed actor/model-family receipt and target-hash checks;
2. `SOURCE_CONTEXT_READY` or the precise blocker;
3. a source-read ledger;
4. findings first, ordered `critical`, `major`, `minor`;
5. for every finding: target label and location, issue, neutral
   decision-sufficient source citation, impact, minimum closure condition,
   next authorized action, and whether it was patched;
6. a patch summary and unified diff, or explicit no-patch result;
7. validation commands with observed output or not-run reasons;
8. residual risk and one verdict:
   `PATCHED_FOR_CA_ADJUDICATION`,
   `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`,
   `NEEDS_ARCHITECTURE_PASS`, or `BLOCKED`.

Then return only this compact courier message in chat:

```yaml
review_summary:
  status: completed | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/company_surface_logical_record_success_signals_delegated_adversarial_review_patch_v0.md
  recommendation: PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_NEEDED_FOR_CA_ADJUDICATION | NEEDS_ARCHITECTURE_PASS | BLOCKED
  summary: "<one paragraph>"
  next_action: "Home/OpenAI-GPT lane adjudicates every finding and hunk before keep."
```

This commission creates no validation, implementation, runtime, readiness,
owner-acceptance, commit, push, PR, merge, or automatic-keep authority.
````
