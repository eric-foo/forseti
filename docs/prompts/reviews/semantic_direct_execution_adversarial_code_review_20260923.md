# Semantic direct execution — adversarial code review and patch

```yaml
retrieval_header_version: 1
artifact_role: Delegated code review-and-patch prompt
scope: Direct semantic provider execution and reuse of completed extraction batches.
use_when:
  - Couriering this implementation to a different-vendor reviewer with direct repository write access.
authority_boundary: retrieval_only
branch_or_commit: codex/semantic-direct-execution; required ancestor 4e19f5808092c040cfc1eed5984ae5fbed27d803
```

Review and patch material defects in this implementation. Done means code
delivers bounded judgment jobs, native validation still decides acceptance,
restart does not repeat completed provider work, and selected saved extraction
can enter independent verification without new extraction or a false verified
claim. Preserve evidence meaning, source coverage within the selected scope,
immutable publication, and existing consumer admission/restart identities.

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
template_kind: none
target_kind: delegated_code_review_and_patch
delivery: operator_courier_only
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
author_vendor: OpenAI
delegate_vendor: receiver_to_observe
output_mode: paste-ready-chat
edit_permission: patch-only
branch: codex/semantic-direct-execution
diff_base: 73213046593cddf07861ee301e3971b80dff4b1e
required_revision: 4e19f5808092c040cfc1eed5984ae5fbed27d803
revision_mode: ancestor
receiver_binding:
  receiver_class: receiver_to_bind
  launch_checkout: receiver_to_observe
  effective_target_worktree: C:/Users/vmon7/.codex/worktrees/semantic-direct-execution/forseti
  required_revision: 4e19f5808092c040cfc1eed5984ae5fbed27d803
  revision_mode: ancestor
  direct_write_capability: receiver_to_verify
  no_concurrent_writer: receiver_to_verify
dirty_state_allowance: tracked tree clean at bind; existing untracked _scratch/ evidence is read-only; afterward only commissioned reviewer edits
```

Preparation only until an eligible receiver binds itself as
`external_direct_write`. First verify the branch, required ancestor, tracked
cleanliness, write capability and writer isolation; record current HEAD as
`reviewed_revision`. No synthetic mutation probe. Stop on a mismatch or
ineligible receiver; do not substitute another checkout or source summary.
Inspect `diff_base...reviewed_revision` by the second latency-bearing tool call.
Later descendants are outside this review binding.

Environment baseline: Windows host, PowerShell-first; use PowerShell syntax,
absolute paths resolvable from any cwd, and `python`, never `python3`. Do not
pass Windows drive-letter paths or heredocs through bash.

Lifecycle hard stop: no commit, push, opening/updating a PR, merge, stash,
reset, cleaning the worktree or repository-hygiene actions are granted.

Decorrelation commission: delivery is `operator_courier_only`, access is
`repo`, eligibility is `different_vendor_lineage_with_direct_repo_access`.
Same-vendor, unknown-lineage, no-repo, self and Codex-managed controller
substitutes are invalid. A manager-prefixed target path is neutral. Without
an eligible controller, this prompt remains unexecuted.

Read `AGENTS.md`, `.agents/workflow-overlay/README.md`, the code-target and
adjudication rules in `.agents/workflow-overlay/delegated-review-patch.md`,
and "Review Prompt Defaults" in
`.agents/workflow-overlay/prompt-orchestration.md`. Apply `workflow-code-review`
after source readiness. For evidence judgments load the claim-support contract
named by AGENTS. Reuse already-read authority; no full repository tour.

Patch authority is limited to these paths under `forseti-harness/`:

- `judgment/complete_case_consumer.py`
- `judgment/extracted_evidence_selection.py`
- `judgment/verified_evidence_selection.py`
- `provider_jobs.py`
- `runners/run_codex_provider_attempt.py`
- `runners/run_codex_provider_job.py`
- `runners/run_semantic_evidence_integration.py`
- `runners/semantic_execution.py`
- `tests/unit/test_codex_provider_launch.py`
- `tests/unit/test_complete_case_consumer.py`
- `tests/unit/test_semantic_evidence_integration.py`
- `tests/unit/test_semantic_execution.py`

Discover defects across that named set, not only changed lines. Everything
else is read-only and flag-only, including the three changed owning documents:
`forseti-harness/README.md`,
`docs/workflows/phase_a_customer_evidence_completion_path_v0.md`, and
`forseti/product/spines/judgment/claim_support/forseti_semantic_evidence_integration_contract_v0.md`.
Do not weaken validators, expand provider permissions, raise ceilings, add
automatic retries, or revive agent dispatch. Design-level blockers require
`NEEDS_ARCHITECTURE_PASS`, not an architectural patch.

Check prompt/schema delivery and tool restrictions at the provider boundary;
accepted/staged/missing output and interrupted-attempt restart behavior;
input hashes, ownership, coverage and meaning across selected-batch rebinding;
independent verification before consolidation; job limits and visible failures;
complete-case budget/restart compatibility; and truthful usage accounting.
Find a concrete failing case before patching; add a regression for accepted
defects. Do not infer cost savings or semantic accuracy from offline tests.

No model calls, new agents, acquisition, extraction, verification execution,
or resuming the owner's run are authorized. The original stopped run at
`C:/Users/vmon7/.codex/tmp/forseti-sf-supervised-20260922` is read-only.
Existing local evidence is `_scratch/sf-saved-16/offline-proof.json` and its
referenced files: 16 batches, 660 rows, 1,456 statements, eight prepared
verification jobs, zero new extraction jobs, unchanged originals. Inspect
the proof rather than treating these author-reported numbers as review results.
Use temporary test directories for any additional offline reproductions.

From the bound worktree's `forseti-harness/`, run the focused offline suite:

```powershell
python -B -m pytest tests/unit/test_semantic_execution.py tests/unit/test_codex_provider_launch.py -q
```

For patches, run the relevant native validator/restart tests in
`test_semantic_evidence_integration.py`, `test_complete_case_consumer.py`,
`test_verified_evidence_selection.py` and `test_provider_jobs.py` as affected.
Use `.agents/workflow-overlay/validation-gates.md` for any newly triggered
checks; required CI owns broad coverage. Report actual commands and failures,
including checks not run. Finish with `git diff --check`.

Return one findings-first chat packet: `delegate_vendor`, required and reviewed
revisions, findings with neutral source/line citations, bounded changes,
validation evidence, review recommendation and residual uncertainty. No separate
report file or duplicate return block. Chief Architect adjudication is required
before returned changes are accepted; the delegated-review-patch adjudication
closeout and same-turn material-continuation rule apply. No landing or readiness
claim is authorized by this review alone.
