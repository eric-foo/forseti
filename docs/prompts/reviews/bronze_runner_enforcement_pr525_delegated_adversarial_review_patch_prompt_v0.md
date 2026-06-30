# Delegated Adversarial Review-and-Patch Prompt - PR #525 Bronze Runner Enforcement v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated review-and-patch commission)
scope: >
  Controller prompt for a de-correlated adversarial mixed code/doc review with
  bounded patch authority for PR #525's Bronze writer runner enforcement slice.
use_when:
  - Commissioning an independent controller review of PR #525 before owner merge.
  - Checking whether Bronze writer runner coverage enforcement correctly includes current packet writers and raw-packet orchestrators without over-broadening to every lake-touching runner.
  - Adjudicating the returned diff, findings, or no-patch result before keeping any delegated changes.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/source-loading.md
  - orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md
input_hashes:
  orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py: 673FA90929E3C3CCD8BE87C766CA180ADA6870B39C1B6069EE962DBFFAD7D4D6
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md: A1D2A4A3D74E87AA500951FDA8E910F82F163E13116439F54F56BE0F58C1A657
branch_or_commit: codex/bronze-runner-enforcement @ 7fb4812fc459a8c8cc2e544cc84ebe52376e2f00
stale_if:
  - Either target hash changes before the controller starts.
  - The PR branch advances with implementation changes beyond the prompt artifact.
  - Home-model adjudication for this commission completes.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_pr525_mixed_code_doc_diff
  edit_permission: patch-only for two named target files plus review-report file-write
  target_scope:
    implementation_targets:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca\product\spines\data_lake\authority\core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md
    context_only:
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\packet_assembly.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\writer.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\transcript\asr_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\transcript\ig_reels_audio_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\transcript\caption_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\source_capture\youtube_watch_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\runners\run_fragrantica_mgt_capture.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\runners\run_source_capture_youtube_asr_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\runners\run_source_capture_ig_reels_audio_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\runners\run_source_capture_youtube_caption_packet.py
      - C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\orca-harness\runners\run_source_capture_youtube_watch_packet.py
  excluded_from_review_target:
    - this prompt artifact
    - unrelated runner families that neither write raw SourceCapturePacket bodies nor orchestrate raw-packet subrunners
    - Silver-only or derived-only lake writers
    - lake catalog code, AR implementation, source_capture runtime implementation, CI configuration, overlay files, repo map, and unrelated product doctrine
  dirty_state_checked: yes_by_dispatcher_before_prompt_file
  branch_or_commit_reference: PR #525 local branch codex/bronze-runner-enforcement, implementation commit 7fb4812fc459a8c8cc2e544cc84ebe52376e2f00, base codex/bronze-mgt-baseline
  controlling_source_state: target hashes recorded above from dispatcher working tree; GitHub PR/CI state must be rechecked by the controller if it matters
  output_mode: file-write prompt artifact plus paste-ready delivery copy
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\prompts\reviews\bronze_runner_enforcement_pr525_delegated_adversarial_review_patch_prompt_v0.md
  reviewer_output_mode: review-report plus working-tree patch if warranted
  required_review_report_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\review-outputs\bronze_runner_enforcement_pr525_delegated_adversarial_review_patch_v0.md
  doctrine_change_decision: no new doctrine requested by this prompt; flag any doctrine or architecture problem instead of patching outside the target files
  isolation_decision: use the existing isolated PR worktree; do not create or switch branches/worktrees
  validation_gates:
    - verify commit and target-file hashes before review
    - inspect PR #525 diff from codex/bronze-mgt-baseline to 7fb4812fc459a8c8cc2e544cc84ebe52376e2f00
    - rerun the focused pytest command if repo execution is available
    - run prompt/report hygiene checks only if the controller changes durable docs
  blocked_if_missing:
    - controller cannot open the pinned repo/worktree or equivalent branch revision
    - controller cannot prove de-correlation from the author/home family
    - controller cannot verify the target hashes or distinguish target files from context-only files
```

## Commission

Run a delegated, de-correlated adversarial mixed code/doc review-and-patch pass
for PR #525's Bronze writer runner enforcement slice. This is a separate
bounded patch commission for exactly the two named target files, not broad
permission to edit the lake, runners, source_capture implementation, CI, or
overlay doctrine.

PR locator for orientation: `https://github.com/eric-foo/orca/pull/525`.
Do not trust PR status from this prompt. Recheck branch/head/CI if those facts
matter to your report.

Targets that may be patched:

- `[runner-contract]` `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- `[propagation-contract]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md`

Why read-only review is insufficient: this slice is itself an enforcement
surface. If the detector misses a current packet writer, over-includes a
derived-only or audit runner, encodes a false completeness claim, or documents
a broader guarantee than the tests actually enforce, the correct hardening may
be a small bounded patch to the test contract or the propagation contract text.
A findings-only review would force a second round trip for the smallest obvious
fixes inside the submitted scope.

If your runtime or local overlay interpretation does not accept bounded patch
authority for this two-file implementation/code-doc diff, return
`BLOCKED_UNBOUND_PATCH_AUTHORITY` and perform no patch. Do not silently downgrade
to ordinary self-review or patch outside the scope.

## Actor / Model-Family Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT (Codex based on GPT-5 authored the PR #525 patch and this commission)
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
  `codex/bronze-runner-enforcement`
- Base branch:
  `codex/bronze-mgt-baseline`
- Expected implementation commit:
  `7fb4812fc459a8c8cc2e544cc84ebe52376e2f00`
- Expected implementation diff:
  `2 files changed, 201 insertions(+), 11 deletions(-)`
- Target file hash pins:
  - `[runner-contract]` SHA256 `673FA90929E3C3CCD8BE87C766CA180ADA6870B39C1B6069EE962DBFFAD7D4D6`
  - `[propagation-contract]` SHA256 `A1D2A4A3D74E87AA500951FDA8E910F82F163E13116439F54F56BE0F58C1A657`
- Dirty-state allowance:
  clean target files at those hashes. A later branch advance that only adds this
  prompt artifact may be ignored for implementation review. Any target-file hash
  mismatch returns `HASH_MISMATCH` before review.
- Permitted writes:
  the two target files and the review report path only. No commit, push,
  staging, branch operation, runner execution that mutates the lake, or edit to
  context-only files.

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
   `workflow-adversarial-artifact-review`.
   Do not APPLY them yet. Use them only to prepare neutral source-reading lenses.
   If a required review skill is unavailable, return
   `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.
3. SOURCE-LOAD the target files, the PR #525 diff against
   `codex/bronze-mgt-baseline`, and the context-only writer/runner files listed
   in preflight. Do not substitute this prompt, a summary, or an alternate
   checkout for source loading.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing
   sources, conflicts, and excluded sources.
5. Only after that declaration, APPLY `workflow-deep-thinking` to frame failure
   modes, then APPLY `workflow-code-review` to the test/code mechanics and
   `workflow-adversarial-artifact-review` to the authority/overclaim semantics
   in the propagation contract. Then decide whether a bounded patch is warranted.

## Fitness Reference

Goal: make Bronze enforcement catch every current runner that writes raw
`SourceCapturePacket` data or orchestrates raw-packet subrunners, without
converting that seam into a false guarantee over every lake-touching,
derived-only, Silver-only, audit, catalog, or report runner.

Done looks like: future capture lanes can add packet writers and runners without
silently bypassing `--data-root` / `ORCA_DATA_ROOT` propagation; ASR-style
indirect packet writers remain covered; explicit raw-packet orchestrators such
as fragrance stay covered; and the docs state the exact enforcement boundary
without claiming Bronze completeness, runner readiness, or Silver/AR coverage.

Attack the bar itself. If this goal or success signal is too weak, too broad, or
misplaced, name that as a finding.

## Review Axes To Attack

Prioritize material correctness and false-completeness risks:

- Does `_source_capture_packet_writer_names()` really find current indirect
  packet writers that eventually call `write_local_source_capture_packet` or
  `stage_and_write_packet`, including ASR/caption/watch paths, without relying
  on fragile filename assumptions?
- Can the detector miss alias imports, wrapper indirection, renamed functions,
  module-qualified calls, or future source families in a way that makes the
  expected runner snapshot look stronger than it is?
- Does `BRONZE_PACKET_ORCHESTRATORS` cover only true raw-packet orchestrators,
  and does the fragrance MGT runner forwarding test prove `data_root=` reaches
  the packet subrunners that need it?
- Does the explicit current runner snapshot include all and only current Bronze
  raw packet writer runners? Pay special attention to ASR, caption, YouTube
  watch, IG reels grid/audio, media, archive, browser, authenticated browser,
  cloakbrowser, historical, antiblock, price payload, IG calls, and fragrance
  MGT capture.
- Does the test suite avoid over-broadening into every lake-touching runner,
  every derived-only writer, Silver Vault writer, catalog/audit/report runner,
  materializer, projection entrypoint, or future AR implementation?
- Does the propagation contract align with the code-backed layer, including
  "raw SourceCapturePacket producers and explicit raw-packet orchestrators" as
  the seam? Does it avoid implying full Bronze GT/MGT readiness by itself?
- Is the future-lane failure mode ergonomic: when a future runner is added, does
  the test failure tell the implementer whether to add data-root propagation,
  mark it as an orchestrator, or leave it out because it is not a raw Bronze
  writer?
- Does the DCP receipt and doc wording honestly state what changed and what did
  not change, without claiming validation, readiness, or source promotion?

## Validation Evidence To Inspect

Dispatcher-observed validation from the implementation turn:

```powershell
python -m py_compile orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py
python -m pytest -q orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py
python -m pytest -q orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py orca-harness\tests\test_data_lake_catalog.py
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\check_dcp_receipt.py --changed --strict
python .agents\hooks\header_index.py --strict
python .agents\hooks\check_map_links.py --strict
git diff --check
git diff --cached --check
```

Observed results in that turn:

- focused runner seam tests: `9 passed`
- runner seam plus catalog tests: `.....................s.............. [100%]`
- retrieval header, DCP receipt, header index, map links, and whitespace checks:
  passed; `check_map_links --strict` reported `OK (0 findings)` plus annotated
  nonresolving debt.

Treat these as evidence to inspect, not as formal validation proof. If you have
repo execution access, rerun at least:

```powershell
python -m pytest -q orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py
```

If you patch docs, also run the relevant prompt/report/doc hygiene checks you
can run in your environment. If a check is unavailable, report `validation_not_run`
with the reason.

## Bounded Patch Scope

Patch only the two target files:

- `[runner-contract]` `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- `[propagation-contract]` `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md`

Apply the smallest complete patch for accepted material findings inside those
files. Do not patch runners, source_capture writers, lake runtime code, catalog
code, AR contracts, Silver contracts, repo map, overlay files, CI, prompt files,
or review-output ledgers. If the correct fix belongs outside the two target
files, flag it with a closure condition and leave the working tree unchanged
outside scope.

Design-level problem -> return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert
any partial diff, and return findings only.

## Output Contract

Write a durable report to:

`C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-mgt-baseline\docs\review-outputs\bronze_runner_enforcement_pr525_delegated_adversarial_review_patch_v0.md`

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
- per-change neutral citations, tagged `[runner-contract]` or
  `[propagation-contract]`;
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

Here is the delegated review-and-patch result for PR #525. Adjudicate it under
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
mandatory remediation, source promotion, Bronze GT/MGT declaration, runtime
model routing, or permission to edit outside the two target files.
