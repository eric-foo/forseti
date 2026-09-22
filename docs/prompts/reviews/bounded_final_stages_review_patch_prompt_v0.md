# Bounded final stages: delegated code review and patch

```yaml
retrieval_header_version: 1
artifact_role: Forseti delegated code-review-and-patch courier prompt
scope: Review the bounded complete-case consumer's original-context and correction partition boundaries at the pinned implementation lineage.
use_when:
  - An independent different-vendor controller has direct write access to the named worktree and receives this commission from the operator.
authority_boundary: retrieval_only
```

This is one preparation-only, operator-courier commission. Goal: establish whether
splitting reopened originals and correction inputs preserves every required
evidence, objection, check and answer dependency, including restart behavior.
Done means concrete material defects are patched within scope and validated, or
the remaining uncertainty/design blocker is stated without a false pass.

The owner's success-implement instruction supplies conditional review authority.
Independent historical fit and live final-answer tests pass, but oversized
original-context/correction branches have only author-built fixture coverage.
A bounded review-and-patch pass lets the independent controller reproduce and
repair a discovered interaction at that boundary without a second interpretation
handoff. Ordinary read-only findings alone would leave that repair untested.

Output mode: **chat-only**. Edit permission: **patch-only**. Input prompt source:
`docs/prompts/reviews/bounded_final_stages_review_patch_prompt_v0.md` in the target.
Return the findings, bounded working-tree diff, citations, validation, verdict
and residual risk once in your response; no separate report or duplicate packet.
Lane: bound commission, `delegated_code_review_and_patch`, `workflow-code-review`,
base-subagent mode (you are the controller; do not launch another reviewer).
Renderer: the overlay's Lane-Scoped Delegated Patch Prompt Default.

```yaml
receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  launch_checkout: receiver_to_observe
  effective_target_worktree: C:/Users/vmon7/.codex/worktrees/sf-bounded-final-stages/forseti
  required_revision: 7cb6a042c35b3546068e462b8650f23900744f51
  revision_mode: ancestor
  capability_proof: receiver_to_observe
  no_concurrent_writer_state: receiver_to_observe
branch: codex/bounded-final-stages
base_revision: 3d53e48702be0f90e31ff199292a33ea10b9ba16
author_vendor: OpenAI
author_home_model_family: GPT
controller_model_family: receiver_to_observe
delegate_vendor: receiver_to_observe
current_receiving_actor_role: controller
dispatch_mode: external-controller-courier
delivery: operator_courier_only
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
de_correlation_status: pending-receiver-verification
```

First action: combine target/branch/ancestry/clean-state, authority-pointer and
writer-isolation checks with direct-write capability and upstream-vendor proof.
Bind yourself as `external_direct_write`, record launch checkout and current HEAD
as `reviewed_revision`, and inspect the actual base-to-reviewed diff by your
second latency-bearing tool call. No target-source loading before that binding.
At bind the tree must be clean; afterward only your commissioned edits are
allowed. Unknown lineage, same-vendor, no-repo, self and Codex-managed controller
substitutes are ineligible. A manager-prefixed target path is neutral. If no
eligible controller is available, leave this prompt unexecuted. Missing identity
proof returns `BLOCKED_DECORRELATION_RECEIPT_MISSING`; matching vendor returns
`BLOCKED_CONTROLLER_NOT_DECORRELATED`. Do not replace the controller or recurse.

Patchable files (all other paths, original evidence and saved outputs are
read-only/flag-only):

- [consumer] `forseti-harness/judgment/complete_case_consumer.py`
- [delivery] `forseti-harness/runners/run_semantic_evidence_integration.py`
- [tests] `forseti-harness/tests/unit/test_complete_case_consumer.py`

Limit edits to material defects in actual capacity admission, complete partition
coverage, local objection/repair context, exact corrected-answer review and
unchanged-job reuse at the named boundary. Preserve the supported small route,
source identities, failure visibility, and existing exact-repair authority.
Do not redesign the pipeline, broaden repair policy, change provider settings,
process Summer Fridays, acquire sources, or make provider calls. Flag a needed
change to any other file; do not silently widen scope.

After binding and diff inspection, use the actual owning sources:

- `AGENTS.md` and `.agents/workflow-overlay/README.md`.
- `.agents/workflow-overlay/delegated-review-patch.md`: When it applies, The loop,
  Access selection rule, De-correlation, Code-diff target kind, and Adjudication
  closeout (including its same-turn material-continuation rule for the CA).
- `.agents/workflow-overlay/review-lanes.md`: Review Doctrine; and
  `.agents/workflow-overlay/validation-gates.md`: Task validation route.
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` for remaining
  intake/source-boundary constants.
- `forseti/product/spines/judgment/claim_support/forseti_intelligence_claim_support_contract_v0.md`
  and `forseti_semantic_evidence_integration_contract_v0.md` in the same folder,
  section **Bounded complete-case answer and review**.
- `docs/research/summer_fridays_complete_comparison_20260922/consumer_implementation.md`,
  section **Bounded final stages implementation and validation (2026-09-22)**,
  for exact validation commands, observed failures, evidence paths and limits.

Invoke `workflow-code-review` after intake; the local skill is
`C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.103/skills/workflow-code-review/SKILL.md`.
If unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.
Use that lane's findings schema and Forseti severity contract; include a formal
code-review verdict and scoped residuals. Each finding, citation and diff hunk
must identify its file label above. Explain a concrete failing input/consumer
outcome and the minimum closure condition; do not substitute generic hardening.

Environment: Windows, PowerShell-first; use PowerShell commands and absolute
paths resolvable from any cwd, invoke `python` (never `python3`), and do not pass
Windows drive-letter paths or heredocs through bash. Lifecycle hard stop: do not
commit, push, open/update a PR, merge, stash, reset, clean the worktree or perform
repository hygiene. No such lifecycle authority is granted here.

Validate from the target's `forseti-harness` directory:
`python -m pytest tests/unit/test_complete_case_consumer.py -q -o addopts= --disable-warnings`.
Add/run a focused regression for each accepted defect in the named test file;
use preserved real inputs or an independently designed falsifier where possible.
Run the report's affected intake tests if delivery code changes and `git diff
--check`. Record command, cwd, actual exit/output and not-run reasons. The full
suite remains required CI. Existing evidence is 56 consumer tests, 68 shared/
contract tests and 27 intake tests; all 8,366 historical records fit in three
requests; a live 12-record mixed-source answer passed three independent reviews
and unchanged restart. Those results do not prove the unexercised live reopen/
correction branches. Generated negative controls rejected false claims; their
proposed repairs failed existing admission, so no live corrected pass is claimed.

The delegate's (controller's) citations and changes are decision input only.
The home model / CA reserves final authority over what is kept and may veto any
change at its discretion when it judges the change adds no benefit or is
net-negative — even an individually defensible change may be rejected. This is
the standard "claims to adjudicate, not premises to inherit." Citations must be
neutral in tone but decision-sufficient in substance: the delegate's argument
lives in the verdict and residual-risk note, not in the citations. Thin citations
push the CA back onto its own priors and defeat de-correlation.

On a design-level blocker return `NEEDS_ARCHITECTURE_PASS`: stop patching,
quarantine/revert only your own partial edits and return findings. Never disturb
another actor's changes. Home-model adjudication decides accept/modify/reject
before any patch is kept or the draft is merged. Return both required and reviewed
revisions, your vendor/role receipt, findings/non-findings/not-proven boundaries,
labelled diff and neutral source citations, validation evidence, verdict,
residual risk and next authorized action. This prompt is not review execution,
validation, readiness or automatic acceptance.
