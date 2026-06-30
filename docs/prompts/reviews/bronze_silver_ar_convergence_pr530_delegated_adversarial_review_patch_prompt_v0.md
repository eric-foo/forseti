# Delegated Adversarial Review-and-Patch Prompt - PR #530 Bronze/Silver/AR Convergence v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission)
scope: >
  Controller prompt for a de-correlated adversarial artifact review with bounded
  documentation patch authority for PR #530's Bronze MGT declaration and
  Silver/Attachment Record intake-boundary convergence slice.
use_when:
  - Commissioning an independent controller review of PR #530 before owner merge.
  - Checking whether the Bronze MGT declaration, full-GT upgrade path, Silver raw-ref intake boundary, and AR consumption contract avoid false authority or runtime implementation claims.
  - Adjudicating the returned diff, findings, or no-patch result before keeping any delegated changes.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/source-loading.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
input_hashes:
  docs/decisions/dcp_receipts_archive_v0.md: 08D921F7CDF9A6832F4213EC7E3776D5CDED60C647EE710B9EDD2FDBF3C9147F
  docs/workflows/orca_repo_map_v0.md: B90994C8B1FC5DF8624E4B8A8F4FB1E711EFF869714125FB6699F42771019E5D
  orca/product/spines/data_lake/README.md: 60C166826DDE06AFFF49DF6E30956AA64804460BA33D5CACF1F92EA6B9DC447C
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md: 459B9F59400CB9091622A238811C2B12F60AECB5272B4DEF5ADD4E3217F22321
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md: CA9D336522B3DC8C99BAB22A86EB358120F6418A770E013FEDCB63299D38DF38
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md: 5744F283AA076CBFA811044E8B589CD0F840A7AC05FEBE0B81F5F17C44919005
branch_or_commit: codex/bronze-silver-ar-convergence @ c2d908263682788c5c7b7a47e817259dc7391d41
stale_if:
  - Any target hash changes before the controller starts.
  - The PR branch advances with target-document changes beyond the prompt artifact.
  - Home-model adjudication for this commission completes.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  authorization_basis: current owner request to delegate patch review for PR #530
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_pr530_artifact_diff
  repo_map_decision: loaded
  repo_map_reason: PR #530 touches Data Lake routing and repo-map wording
  edit_permission: patch-only for the six named target docs plus review-report file-write
  target_scope:
    patchable_targets:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\decisions\dcp_receipts_archive_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\workflows\orca_repo_map_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\README.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\AGENTS.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\README.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\source-of-truth.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\source-loading.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\review-lanes.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\prompt-orchestration.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\.agents\workflow-overlay\delegated-review-patch.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\data_lake\catalog.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_core_contract_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_storage_contract_v0.md
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  excluded_from_review_target:
    - this prompt artifact
    - runtime code, tests, runners, CI, overlay doctrine, and unrelated product spines
    - any attempt to implement Silver producers, AR runtime behavior, Manifest v2, lake-doctor, or storage/backend changes
  dirty_state_checked: yes_by_dispatcher_before_prompt_file
  branch_or_commit_reference: PR #530 local branch codex/bronze-silver-ar-convergence, target commit c2d908263682788c5c7b7a47e817259dc7391d41, base codex/bronze-mgt-baseline
  controlling_source_state: target hashes recorded above from dispatcher working tree; GitHub PR/CI state verified by dispatcher but must be rechecked by the controller if material
  output_mode: file-write prompt artifact plus paste-ready delivery copy
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\prompts\reviews\bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_prompt_v0.md
  reviewer_output_mode: review-report plus working-tree patch if warranted
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\review-outputs\bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_v0.md
  doctrine_change_decision: this prompt does not change doctrine; target docs do, and any delegated patch to them must preserve or repair their DCP receipts rather than bypassing them
  isolation_decision: use the existing isolated PR worktree; do not create or switch branches/worktrees
  thread_operating_target_continuity:
    carried_forward: no
    reason: no_visible_active_target
    changed_from_input: no
    lifecycle_status: not_applicable
  validation_gates:
    - verify PR #530 metadata, target commit, and target-file hashes before review
    - inspect PR #530 diff from codex/bronze-mgt-baseline to c2d908263682788c5c7b7a47e817259dc7391d41
    - inspect the six target files in full or by enough line windows to support findings
    - run doc/prompt hygiene checks if any target or review report is changed
  blocked_if_missing:
    - controller cannot open the pinned repo/worktree or equivalent branch revision
    - controller cannot prove de-correlation from the author/home family
    - controller cannot verify target hashes or distinguish target files from context-only files
```

## Commission

Run a delegated, de-correlated adversarial artifact review-and-patch pass for
PR #530's Bronze/Silver/Attachment Record convergence slice. This is a bounded
documentation/contract hardening commission for exactly the six named target
files, not permission to implement Silver, mutate Bronze runtime code, change
storage layout, edit overlay doctrine, or widen the lake contract.

PR locator for orientation: `https://github.com/eric-foo/orca/pull/530`.
Do not trust PR status from this prompt. Recheck branch/head/CI if those facts
matter to your report.

Targets that may be patched:

- `[dcp-archive]` `docs/decisions/dcp_receipts_archive_v0.md`
- `[repo-map]` `docs/workflows/orca_repo_map_v0.md`
- `[lake-readme]` `orca/product/spines/data_lake/README.md`
- `[ar-contract]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `[bronze-mgt]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
- `[silver-contract]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

Why read-only review is insufficient: this slice is a high-stakes authority
and routing surface. If it overclaims Bronze GT, under-specifies the Silver
raw-ref boundary, hides AR residuals, misstates DCP propagation, or creates a
stale route in the Data Lake README/repo map, the correct hardening may be a
small bounded doc patch inside the submitted target files. A findings-only
review would force a second round trip for obvious wording, receipt, or routing
repairs inside the commissioned scope.

If your runtime or local overlay interpretation does not accept bounded patch
authority for this six-file artifact/documentation diff, return
`BLOCKED_UNBOUND_PATCH_AUTHORITY` and perform no patch. Do not silently
downgrade to ordinary self-review or patch outside the scope.

## Actor / Model-Family Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT (Codex based on GPT-5 authored the PR #530 patch and this commission)
  controller_model_family: operator_to_fill; must be non-OpenAI vendor lineage for cross-vendor discovery
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: verify_at_run_start
```

This is a who-constraint, not a model recommendation. Vendor means upstream
model developer/provider, not hosting platform, wrapper, reseller, or tier. If
your lineage is OpenAI or unknown/undisclosed, stop before review and return
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. No tester/testee shortcut: you are the
controller; do not dispatch subagents or a replacement controller.

## Worktree Preflight

- Workspace:
  `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline`
- Branch:
  `codex/bronze-silver-ar-convergence`
- Base branch:
  `codex/bronze-mgt-baseline`
- Expected target commit:
  `c2d908263682788c5c7b7a47e817259dc7391d41`
- Expected implementation diff:
  `6 files changed, 288 insertions(+), 73 deletions(-)`
- GitHub PR metadata observed by dispatcher:
  PR #530 open draft, base `codex/bronze-mgt-baseline`, head
  `codex/bronze-silver-ar-convergence`, head OID
  `c2d908263682788c5c7b7a47e817259dc7391d41`.
- GitHub CI observed by dispatcher:
  `orca-harness-tests` state `SUCCESS`.
- Target file hash pins:
  - `[dcp-archive]` SHA256 `08D921F7CDF9A6832F4213EC7E3776D5CDED60C647EE710B9EDD2FDBF3C9147F`
  - `[repo-map]` SHA256 `B90994C8B1FC5DF8624E4B8A8F4FB1E711EFF869714125FB6699F42771019E5D`
  - `[lake-readme]` SHA256 `60C166826DDE06AFFF49DF6E30956AA64804460BA33D5CACF1F92EA6B9DC447C`
  - `[ar-contract]` SHA256 `459B9F59400CB9091622A238811C2B12F60AECB5272B4DEF5ADD4E3217F22321`
  - `[bronze-mgt]` SHA256 `CA9D336522B3DC8C99BAB22A86EB358120F6418A770E013FEDCB63299D38DF38`
  - `[silver-contract]` SHA256 `5744F283AA076CBFA811044E8B589CD0F840A7AC05FEBE0B81F5F17C44919005`
- Dirty-state allowance:
  clean target files at those hashes. A later branch advance that only adds this
  prompt artifact may be ignored for target review. Any target-file hash
  mismatch returns `HASH_MISMATCH` before review.
- Permitted writes:
  the six target files and the review report path only. No commit, push,
  staging, branch operation, runtime implementation, test/code edit, or overlay
  edit.

## Source-Gated Method Contract

1. Authority reads: `AGENTS.md`; `.agents/workflow-overlay/README.md`;
   `.agents/workflow-overlay/source-of-truth.md`;
   `.agents/workflow-overlay/source-loading.md`;
   `.agents/workflow-overlay/review-lanes.md`;
   `.agents/workflow-overlay/prompt-orchestration.md`;
   `.agents/workflow-overlay/validation-gates.md`;
   `.agents/workflow-overlay/delegated-review-patch.md`.
2. REFERENCE-LOAD methods before applying them:
   `workflow-deep-thinking` and `workflow-adversarial-artifact-review`.
   Do not APPLY them yet. Use them only to prepare neutral source-reading
   lenses. If a required review skill is unavailable, return
   `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.
3. SOURCE-LOAD the six target files, the PR #530 diff against
   `codex/bronze-mgt-baseline`, and the context-only lake/catalog/overlay
   sources needed to verify the claims. Do not substitute this prompt, a
   summary, or an alternate checkout for source loading.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing
   sources, conflicts, and excluded sources.
5. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure
   modes, then APPLY `workflow-adversarial-artifact-review` to the doctrine,
   routing, retrieval, DCP, and false-authority semantics. Then decide whether a
   bounded patch is warranted.

## Fitness Reference

Goal: make PR #530 leave Bronze honestly declared as MGT, not full GT, while
giving Silver and future AR consumers a stable, source-backed intake boundary
that does not rely on folder semantics or runtime implementation promises.

Done looks like: downstream Silver work can cite public Bronze packet/catalog/AR
surfaces for source-backed `raw_refs`; missing AR remains visible residual
instead of inferred absence; the full-GT path is named without making it a
precondition; and the docs do not claim validation, readiness, runtime
implementation, storage/backend selection, Manifest v2 selection, or Bronze full
GT.

Attack the bar itself. If this goal or success signal is too weak, too broad, or
misplaced, name that as a finding.

## Review Axes To Attack

Prioritize material correctness, false-authority, and downstream coordination
risks:

- Does `[bronze-mgt]` clearly declare Bronze MGT after PR #525 without quietly
  upgrading it to full GT or implying validation/readiness/proof?
- Is the full-GT upgrade path accurate and useful, or does it omit a material
  blocker such as deterministic writer discovery, Manifest v2/migration,
  storage/backend/retention posture, lake-doctor enforcement, multi-family
  consumer proof, or independent review?
- Is the "worth it long term" stance defensible: not a Silver prerequisite now,
  but likely worth doing when scale, latency, compliance, or reliability promises
  make residuals expensive?
- Does `[silver-contract]` bind Silver source-backed `raw_refs` to public Bronze
  packet/catalog/AR surfaces without forcing private raw path semantics,
  treating generated catalog files as authority, or making Silver declare Bronze
  GT?
- Does `[silver-contract]` handle the missing-AR case honestly: fallback raw
  packet refs only when a producer contract allows them, visible residual/posture,
  no inferred absence?
- Does `[ar-contract]` define AR as a typed raw-payload ref Silver may carry,
  while preserving the raw body as Bronze evidence and avoiding runtime AR
  implementation authorization, Manifest v2 selection, body-store layout
  selection, backend selection, or migration authority?
- Do `[lake-readme]` and `[repo-map]` route future agents to the right controlling
  sources without duplicating/forking the contracts or overclaiming Bronze/Silver
  state?
- Does `[dcp-archive]` preserve receipt history cleanly after cycling a Silver
  receipt out of the inline two-receipt window? Check fence balance, retrieval
  header validity, and whether archive placement changes source authority.
- Do all DCP receipts in changed target files have valid trigger vocabulary,
  truthful controlling-source lists, honest intentionally-not-updated reasons,
  and non-claims that cover the actual risk surface?
- Does the patch accidentally create a new doctrine surface without a DCP
  receipt or create a DCP receipt that claims more propagation than was checked?
- Are labels such as MGT, GT, Silver, AR, raw refs, catalog, generated read
  state, and authority used consistently across the six files and adjacent lake
  contracts?

## Validation Evidence To Inspect

Dispatcher-observed validation from the implementation turn:

```powershell
git diff --check codex/bronze-mgt-baseline...HEAD
python .agents/hooks/check_dcp_receipt.py --strict --base codex/bronze-mgt-baseline
python .agents/hooks/header_index.py --strict --base codex/bronze-mgt-baseline
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_repo_map_freshness.py --strict
python .agents/hooks/check_retrieval_header.py --strict <changed files>
python .agents/hooks/check_dcp_receipt_hygiene.py --strict <changed files>
python .agents/hooks/check_dcp_receipt.py --audit
```

Observed results in that turn:

- committed local checks above passed;
- `check_map_links --strict` reported `OK (0 findings)` plus annotated
  nonresolving debt;
- DCP audit reported every real receipt in the repo shape-valid;
- GitHub PR #530 `orca-harness-tests` reported `SUCCESS`.

Treat these as evidence to inspect, not as formal validation proof. If you have
repo execution access, rerun at least:

```powershell
git diff --check codex/bronze-mgt-baseline...HEAD
python .agents/hooks/check_dcp_receipt.py --strict --base codex/bronze-mgt-baseline
python .agents/hooks/header_index.py --strict --base codex/bronze-mgt-baseline
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_repo_map_freshness.py --strict
```

If you patch docs, also run the relevant prompt/report/doc hygiene checks you
can run in your environment. If a check is unavailable, report
`validation_not_run` with the reason.

## Bounded Patch Scope

Patch only the six target files:

- `[dcp-archive]` `docs/decisions/dcp_receipts_archive_v0.md`
- `[repo-map]` `docs/workflows/orca_repo_map_v0.md`
- `[lake-readme]` `orca/product/spines/data_lake/README.md`
- `[ar-contract]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
- `[bronze-mgt]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
- `[silver-contract]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`

Apply the smallest complete patch for accepted material findings inside those
files. Do not patch runtime code, tests, runners, lake catalog code, overlay
files, prompt files, CI, unrelated product doctrine, or review-output ledgers.
If the correct fix belongs outside the six target files, flag it with a closure
condition and leave the working tree unchanged outside scope.

Design-level problem -> return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert
any partial diff, and return findings only.

## Output Contract

Write a durable report to:

`C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\review-outputs\bronze_silver_ar_convergence_pr530_delegated_adversarial_review_patch_v0.md`

If the report cannot be written, return `FAILED_REVIEW_OUTPUT_WRITE` and do not
claim a report path. If no patch is warranted, leave no target diff and state
`NO_PATCH_NEEDED`.

Report contents:

- compact `review_summary` YAML;
- actor/model-family receipt and de-correlation status;
- source-read ledger;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered by materiality, with file/line or stable structural
  anchors, issue, evidence, impact, `minimum_closure_condition`,
  `next_authorized_action`, and verification expectation;
- bounded patch diff or `NO_PATCH_NEEDED`;
- per-change neutral citations, tagged with the relevant target label;
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

Here is the delegated review-and-patch result for PR #530. Adjudicate it under
the delegated-review-patch return contract.

Include:
- original commission and target labels
- reviewed branch/head, target hashes, and dirty-state result
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
mandatory remediation, source promotion, Bronze full GT declaration, Silver
implementation authorization, AR runtime implementation authorization, runtime
model routing, or permission to edit outside the six target files.