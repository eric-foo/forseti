# Creator Registry Operational Sequence Delegated Review Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Delegated adversarial mixed code/artifact review-and-patch prompt for the
  recent Creator Registry operational sequence: merged PRs #654, #660, #667,
  plus open PR #669's cold scan handoff prompt.
use_when:
  - Commissioning an independent de-correlated controller to check whether the
    Creator Registry is now operationally usable by cold creator-discovery lanes.
  - Hardening the integration seam across usage guidance, source-capture runbook,
    scan artifact enforcement, rehearsal evidence, and the cold scan handoff
    prompt before PR #669 is treated as launch-ready.
  - Adjudicating the returned diff, findings, or no-patch result before keeping
    any delegated changes.
authority_boundary: retrieval_only
branch_or_commit: >
  Prompt artifact authored on codex/creator-registry-operational-sequence-review-prompt
  from origin/main@0e475892f821e8aea711e8cdc3a7163838abcb60; review target is
  origin/codex/creator-registry-cold-scan-handoff@991f67040f38ab09e346248d675e17dbb071955f
  unless PR #669 has merged before controller start.
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - .agents/hooks/check_csb_scanning_artifact.py
input_hashes:
  pr669_handoff_prompt_sha256: EB238966ECE84ED80FEBDB26196D1C11E521B61E3437B7720CCE0720318F8F5C
  rehearsal_record_sha256: A03CAD71888C405CBFF4F4178681DE14A0F43D2B8CC416218059BB9025E36915
  match_preflight_usage_sha256: 3EBB5C4D183CB85BC50E690645C049662C9CAE01D04A814D204BAD8A7269816F
  csb_checker_sha256: 6DAC82950E6A36E64415225FE5974A05D26621C4E704140949747D4CE8A9A95D
  csb_checker_tests_sha256: 3BF1912B27BB19D0CDE147ED9267896BC9C18BF294BA54722983678953D54FD2
  scanning_mgt_operating_model_sha256: A58D8966EA082944F97C48EB4DE2D86DDE44026777748C4E55BF2888FDA226AF
  demand_scan_core_spec_sha256: 20092E25E578E7B4DDCABF7F7C3B9EF51CB134D1BD36D9362B52CCAA07016A6E
stale_if:
  - PR #669 branch advances with material changes before controller start.
  - PR #669 merges, requiring target retarget to the merge commit on origin/main.
  - The Creator Registry match preflight usage note, runner, CSB checker, or scan-core capture_request block changes before controller start.
  - Current live product-spine paths no longer resolve under forseti/product/...
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
forseti_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_creator_registry_operational_sequence_review_patch
  edit_permission: patch-only inside named target set plus review-report file-write
  target_scope:
    primary_review_branch: origin/codex/creator-registry-cold-scan-handoff@991f67040f38ab09e346248d675e17dbb071955f
    merged_context_prs:
      - PR #654 merged 2026-07-04T09:41:34Z, merge 988b9a76a77b0bf34c834c4cfa1bc759fea40d64
      - PR #660 merged 2026-07-04T11:18:59Z, merge 77d2f9988533e1cc7eac4578759bc77e1a24f81d
      - PR #667 merged 2026-07-04T11:35:27Z, merge ef2bcf184992c7c29d631190b2deb9487bc265b6
    open_pr_target:
      - PR #669 open at 991f67040f38ab09e346248d675e17dbb071955f
  excluded_from_review_target:
    - this commission prompt
    - live capture execution
    - registry data mutation
    - identity-ledger writes
    - Silver metric refresh implementation
    - fuzzy or cross-platform identity architecture
  dirty_state_checked: yes - prompt worktree rebased onto origin/main@0e475892; PR #669 merge-base observed at ef2bcf18
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md on PR #669 branch origin/codex/creator-registry-cold-scan-handoff
output_mode: review-report plus bounded working-tree patch if warranted
required_review_report_path: docs/review-outputs/adversarial-artifact-reviews/creator_registry_operational_sequence_delegated_review_patch_v0.md
template_kind: delegated_code_review_and_patch mixed with artifact-review checks for docs/prompts
doctrine_change_decision: no new doctrine requested; flag doctrine or architecture gaps rather than editing overlay doctrine
model_lane: unbound; prompt is model-neutral and must not prescribe runtime model choice
non_claims:
  - not validation
  - not readiness
  - not capture authorization
  - not scan authorization
  - not registry mutation
  - not fuzzy duplicate detection
  - not cross-platform identity proof
```

## Commission

Run a delegated, de-correlated adversarial review-and-patch pass over the recent
Creator Registry operational sequence:

- PR #654: bound Creator Registry match preflight into source-capture usage and
  runbook surfaces.
- PR #660: bound Creator Registry receipt fields into CSB scan/capture handoff
  artifacts, checker behavior, fixtures, tests, and scan-core docs.
- PR #667: added the cold-agent preflight rehearsal record.
- PR #669: adds the reusable cold creator discovery scan handoff prompt and is
  still open at the target head unless it has merged before controller start.

The intended outcome is narrow: a cold creator-discovery scan lane can use the
Creator Registry as its first anti-duplicate checkpoint, distinguish known
accounts from exact-unmatched candidates, and only emit new social
creator/account capture requests that carry a row-level preflight receipt with
`intended_action: new_capture` and `can_start_new_capture: true`.

Why read-only review is insufficient: this sequence is itself an operational
turnstile. If a prompt, checker, or runbook leaves an escape hatch, the correct
hardening may be a small bounded patch to the handoff prompt, scan docs, usage
note, runbook, checker, or tests. A findings-only pass would force another
round trip for obvious fixes inside the submitted scope.

If your runtime or overlay interpretation does not accept bounded patch
authority for this mixed code/doc diff, return `BLOCKED_UNBOUND_PATCH_AUTHORITY`
and perform no patch. Do not downgrade to self-review or patch outside scope.

## Actor / Model-Family Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT (Codex based on GPT-5 authored this commission and the PR #669 prompt)
  controller_model_family: operator_to_fill; must be non-OpenAI vendor lineage for cross-vendor discovery
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: repo
  de_correlation_status: verify_at_run_start
```

This is a who-constraint, not a model recommendation. Vendor means upstream
model developer/provider, not hosting platform, wrapper, reseller, or tier. If
your lineage is OpenAI or unknown/undisclosed, stop before review and return
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. No tester/testee shortcut: you are the
controller; do not dispatch subagents or a replacement controller.

## Worktree Preflight

- Preferred target workspace:
  `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-cold-scan-handoff`
- Preferred target branch:
  `codex/creator-registry-cold-scan-handoff`
- Expected open PR:
  `https://github.com/eric-foo/orca/pull/669`
- Expected open PR head:
  `991f67040f38ab09e346248d675e17dbb071955f`
- Expected PR #669 merge-base observed at prompt authoring:
  `ef2bcf184992c7c29d631190b2deb9487bc265b6`
- If PR #669 has merged before you start:
  retarget to `origin/main` at or after the PR #669 merge commit, record the
  observed merge commit, and review the same sequence as landed state. Do not
  proceed on a stale open-branch assumption.
- Dirty-state allowance:
  the target worktree should be clean at start. If dirty, report the dirty
  files and stop unless they are exactly your own permitted patch output from
  the current run.
- Permitted writes:
  bounded target files listed below and the durable review report path only.
  Do not commit, push, merge, open or close PRs, stage files, run live capture,
  mutate the registry, write the external data lake, or edit context-only files.

## Source-Gated Method Contract

1. Authority reads: `AGENTS.md`; `.agents/workflow-overlay/README.md`;
   `.agents/workflow-overlay/source-of-truth.md`;
   `.agents/workflow-overlay/source-loading.md`;
   `.agents/workflow-overlay/review-lanes.md`;
   `.agents/workflow-overlay/prompt-orchestration.md`;
   `.agents/workflow-overlay/validation-gates.md`;
   `.agents/workflow-overlay/delegated-review-patch.md`.
2. REFERENCE-LOAD methods before applying them:
   `workflow-deep-thinking`, `workflow-code-review`, and
   `workflow-adversarial-artifact-review`. Do not APPLY them yet. Use them only
   to prepare neutral source-reading lenses. If a required review skill is
   unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.
3. SOURCE-LOAD the target branch, the PR #669 diff against `origin/main`, and
   the merged context files below. Do not substitute this prompt, a chat
   summary, a PR description, or an alternate checkout for source loading.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing
   sources, conflicts, and excluded sources.
5. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure
   modes, then APPLY `workflow-code-review` to checker/test mechanics and
   `workflow-adversarial-artifact-review` to prompts, runbooks, usage notes,
   rehearsal evidence, and overclaim/path-drift semantics. Then decide whether
   a bounded patch is warranted.

## Required Source Reads

Authority and routing:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`

Target and changed-task sources:

- `[pr669-handoff]` `docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md` on PR #669 branch `origin/codex/creator-registry-cold-scan-handoff`
- `[rehearsal]` `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md`
- `[usage]` `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `[runbook]` `orca-harness/docs/source_capture_agent_runbook.md`
- `[scan-operating-model]` `forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `[scan-core-spec]` `forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `[checker]` `.agents/hooks/check_csb_scanning_artifact.py`
- `[checker-tests]` `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
- `[checker-fixture-valid]` `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md`
- `[checker-fixture-bad]` `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md`
- `[repo-map]` `docs/workflows/forseti_repo_map_v0.md`
- `[compat-map]` `docs/workflows/orca_repo_map_v0.md`

Behavioral sources:

- `orca-harness/runners/run_creator_registry_match_preflight.py`
- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
- `orca-harness/tests/unit/test_creator_registry_match_preflight.py`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md` if any source uses old `orca/product/...` paths.

Prior review reports are source context only, not authority:

- `docs/review-outputs/adversarial-artifact-reviews/creator_registry_operational_preflight_delegated_review_patch_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_registry_match_preflight_enforcement_adversarial_code_review_v0.md`

Before reviewing, record in the report:

- current branch and observed HEAD SHA;
- dirty state;
- PR #669 state observed at start: open or merged;
- diff target used (`origin/main...HEAD` for open PR #669, or landed merge range
  if PR #669 is merged);
- whether every named source exists;
- any source gap and whether it blocks strict findings.

## Fitness Reference

Goal: make Creator Registry operationally usable for cold social creator
discovery scans without recapturing already-known accounts.

Done looks like:

- a cold scan lane can read the registry/projection for orientation;
- every possible new social creator/account capture request runs the match
  preflight runner with `intended_action: new_capture`;
- the scan artifact preserves row-level receipt fields;
- Capture receives no new social creator/account request unless the receipt row
  says `decision: new_candidate`, `action_status: allowed`, and
  `can_start_new_capture: true`;
- existing matches route to update-existing or matched-identity work;
- ambiguous or invalid rows stop;
- docs and prompts avoid claiming fuzzy identity, cross-platform identity proof,
  metric freshness, registry mutation, capture authorization, scan quality,
  validation, readiness, or buyer proof.

Attack the bar itself. If this goal or success signal is too weak, too broad, or
misplaced, name that as a finding.

## Bounded Patch Scope

Patch only these files if a confirmed finding can be closed by the smallest
complete edit inside this set:

- `[pr669-handoff]` `docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md` on PR #669 branch `origin/codex/creator-registry-cold-scan-handoff`
- `[rehearsal]` `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md`
- `[usage]` `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `[runbook]` `orca-harness/docs/source_capture_agent_runbook.md`
- `[scan-operating-model]` `forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`
- `[scan-core-spec]` `forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `[checker]` `.agents/hooks/check_csb_scanning_artifact.py`
- `[checker-tests]` `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
- `[checker-fixture-valid]` `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md`
- `[checker-fixture-bad]` `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md`
- `[hooks-readme]` `.agents/hooks/README.md`
- `[repo-map]` `docs/workflows/forseti_repo_map_v0.md`
- `[compat-map]` `docs/workflows/orca_repo_map_v0.md`

Everything outside that set is read-only. Flag out-of-scope defects in the
report with `next_authorized_action: CA decision or separate lane`; do not edit
them.

Historical review reports and DCP receipts are read-only unless the exact
problem is an active non-historical operational pointer that now misroutes cold
agents. Do not rewrite history merely to replace old `orca/product/...` strings
inside historical receipt text.

Return `NEEDS_ARCHITECTURE_PASS` and stop patching if the smallest correct fix
requires fuzzy identity matching, cross-platform identity architecture, registry
schema redesign, public-handle ledger mutation, live capture execution, metric
refresh automation, Silver lane implementation, or CI architecture outside the
named target set.

## Review Axes To Attack

Prioritize these failure modes:

1. A cold scan prompt can still produce or imply a new social creator/account
   capture request without a real match-preflight receipt row.
2. A row from `intended_action: classify` or `update_existing` can be made to
   look like `new_capture` clearance.
3. `decision: new_candidate` plus `action_status: allowed` clears new capture
   when `can_start_new_capture` is missing, false, malformed, or not from the
   authoritative receipt row.
4. `required_when: not_applicable` can be used as an escape hatch while still
   carrying clearance-shaped metadata.
5. The cold scan handoff treats the readable registry/projection as sufficient
   handoff evidence instead of orientation only.
6. The runbook, usage note, scan-core docs, checker, and open handoff disagree
   about field names, required fields, exit behavior, or non-claims.
7. Current operational docs still point cold agents at pre-migration
   `orca/product/...` paths when live sources are under `forseti/product/...`;
   separate true operational breakage from historical receipt text.
8. The checker accepts placeholders such as `null_or_path`, empty receipt paths,
   or vague local paths for new social creator/account capture.
9. The checker is too broad and blocks non-social or scan-only rows that should
   use explicit `not_applicable`.
10. Tests prove the happy path but miss row-level mixed-batch, malformed truthy,
    or clearance-shaped bypasses.
11. The rehearsal overstates what its synthetic exact-unmatched row proves:
    exact runner behavior only, not source adequacy or candidate quality.
12. The sequence overclaims operational readiness, validation, capture
    authorization, registry mutation, metric refresh, fuzzy identity, or
    cross-platform identity proof.
13. PR #669's launch variables or output contract are underspecified enough that
    a cold agent would invent scan target, source access, run caps, or capture
    request policy.
14. The review/report/prompt validation gates are satisfied cosmetically but
    would fail `check_handoff_pointers.py`, `header_index.py`, review-routing,
    map links, or review-output provenance after a real patch.

## Validation Obligations

After any patch, run the tight gates below and record observed results. If a
command is not run, record `not_run` with the reason. Do not claim validation,
readiness, approval, or merge safety from these checks; they are observed gate
results only.

```powershell
git diff --check
python -m py_compile .agents\hooks\check_csb_scanning_artifact.py orca-harness\runners\run_creator_registry_match_preflight.py orca-harness\capture_spine\creator_profile_current\registry_match_preflight.py
python -m pytest -q orca-harness\tests\unit\test_csb_scanning_artifact_validator.py
python -m pytest -q orca-harness\tests\unit\test_creator_registry_match_preflight.py
python .agents\hooks\check_csb_scanning_artifact.py --selftest
python .agents\hooks\check_csb_scanning_artifact.py --diff origin/main --strict
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\header_index.py --strict --base origin/main
python .agents\hooks\check_handoff_pointers.py --strict --base origin/main
python .agents\hooks\check_dcp_receipt.py --strict --base origin/main
python .agents\hooks\check_review_routing.py --strict --base origin/main
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_full_gt_claims.py --changed --strict
```

If you change only docs and do not touch `.agents/hooks/` or runner code, still
run the focused checker/test commands when cheap; otherwise record why not.

For the delegated review report itself, after the final report write run:

```powershell
python .agents\hooks\check_review_output_provenance.py --strict docs\review-outputs\adversarial-artifact-reviews\creator_registry_operational_sequence_delegated_review_patch_v0.md
```

If the report changes after that command, rerun it before closeout.

## Output Contract

Write the durable report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_registry_operational_sequence_delegated_review_patch_v0.md`

If the report cannot be written, return `FAILED_REVIEW_OUTPUT_WRITE` and do not
claim a report path. If no patch is warranted, leave no target diff and state
`NO_PATCH_NEEDED`.

Report contents:

- compact `review_summary` YAML with `status`, `report_path`,
  `recommendation`, `reviewed_by`, `authored_by`, `de_correlation_bar`,
  `same_vendor_rationale` when applicable, `findings_count`,
  `blocking_findings`, `advisory_findings`, and `next_action`;
- actor/model-family receipt and de-correlation status;
- source-read ledger;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered by materiality, with artifact label, file/line or
  stable structural anchor, issue, evidence, impact,
  `minimum_closure_condition`, `next_authorized_action`, and verification
  expectation;
- bounded patch diff or `NO_PATCH_NEEDED`;
- per-change neutral citations tagged with the artifact labels above;
- off-scope flags, if any;
- validation run status;
- verdict-as-decision-input and residual-risk note;
- provenance fields:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate model identity. Do not recommend, prescribe, rank, or imply a
runtime model choice.

Close with this courier block so the home model can adjudicate:

```text
DELEGATED_REVIEW_PATCH_RETURN_FOR_HOME_MODEL

Here is the delegated review-and-patch result for the Creator Registry
operational sequence (#654/#660/#667 plus open or merged #669). Adjudicate it
under the delegated-review-patch return contract.

Include:
- original commission and target labels
- reviewed branch/head, PR #669 state, target hashes, and dirty-state result
- source readiness status and reviewed files
- findings and implementation evidence
- bounded patch diff or NO_PATCH_NEEDED
- citations
- reviewer verdict as decision input
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

The delegate's diff, findings, and verdict are claims to adjudicate, not
premises to inherit. This commission is not approval, validation, readiness,
mandatory remediation, source promotion, capture authorization, scan
authorization, registry mutation, runtime model routing, or permission to edit
outside the named target files.
