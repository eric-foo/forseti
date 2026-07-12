# TikTok PROMOTE Receipt-Evidence Binding Repo Delegated Adversarial Code Review + Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated adversarial code review-and-patch commission, repo mode)
scope: >
  Paste-ready commission for an independent, different-vendor controller to
  adversarially review and, only where warranted, patch the four-file TikTok
  frontier PROMOTE receipt-evidence binding on draft PR #849 before home-model
  adjudication.
use_when:
  - Dispatching the PR #849 review-and-patch commission to a repo-capable controller outside the OpenAI/GPT model lineage.
  - Re-dispatching unchanged after confirming the implementation commit and target-file SHA-256 values still match.
authority_boundary: retrieval_only
```

preflight_defaults: `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` v0 - constants bound; workspace and lane deltas stated below.

## Forseti Prompt Preflight Deltas

```yaml
authorization_basis: >
  Current owner instruction on 2026-07-11: "Delegate review patch too," after
  the implementation lane reported adversarial follow-up review as recommended
  but not commissioned.
objective: >
  Adversarially test whether PR #849 makes PROMOTE depend on independently
  resolvable, candidate-bound Creator Registry preflight receipt evidence
  without introducing fake-pass, stale-evidence, compatibility, or validation
  gaps; apply only the smallest complete in-scope corrections supported by
  findings.
intended_decision: >
  Return a source-backed findings-first review, an uncommitted bounded patch if
  warranted, observed validation evidence, and residual risks for later
  home-model/Chief-Architect adjudication.
output_mode: review-report
review_output_binding:
  mode: filesystem-output
  required_output_path: docs/review-outputs/adversarial-artifact-reviews/tiktok_promote_receipt_evidence_binding_delegated_adversarial_code_review_v0.md
  path_derivation: not allowed
  chat_after_write: compact human summary plus review courier and delegated-code-review return block
  write_failure: FAILED_REVIEW_OUTPUT_WRITE; chat is not an equivalent substitute
template_kind: review plus bounded patch commission
template_source: workflow-prompt-orchestrator review.md plus patch.md, narrowed by the Orca overlay
edit_permission: patch-only within target_files_or_dirs; the required review report is a separate authorized output artifact
target_files_or_dirs:
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py
  - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py
  - forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
read_only_flag_only:
  - every file outside target_files_or_dirs
  - docs/prompts/reviews/tiktok_promote_receipt_evidence_binding_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  - forseti-harness/capture_spine/creator_profile_current/registry_match_preflight.py
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - docs/workflows/creator_onboarding_first_batch_next_material_steps_handoff_v0.md
source_pack: bounded custom repo pack named below; no checkpoint or prior summary substitutes for current source
workspace_path_delta: C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\promote-receipt-evidence-binding
repository: https://github.com/eric-foo/forseti
pull_request: https://github.com/eric-foo/forseti/pull/849
branch_or_commit_reference:
  expected_branch: codex/promote-receipt-evidence-binding
  implementation_commit: 4721a76bdd38659dd02db50d68e2884b820701d3
  base: origin/main
  branch_head_allowance: implementation commit plus this commission-prompt filing only before delegate edits
dirty_state_allowance: clean at intake; delegate's own authorized target-file patch and required report may then remain uncommitted
controlling_source_state: clean at commission authoring; receiver must fresh-read and report any mismatch
doctrine_change_decision: none intended; flag a required doctrine or architecture change and return NEEDS_ARCHITECTURE_PASS without a partial patch
isolation_decision: use the existing named lane worktree; do not create, clone, switch, rebase, or clean another worktree
review_lane: strict workflow-code-review under the delegated_code_review_and_patch sibling mode, with workflow-deep-thinking first
review_posture: findings-first, adversarial, formal durable report; severity labels rank findings but do not create acceptance authority
model_lane_status: author/home is OpenAI GPT-family; controller must be a different vendor/model lineage or block
thread_operating_target_continuity:
  carried_forward: yes
  reason: same PROMOTE receipt-evidence binding workstream and same draft PR
validation_gates:
  - python -m pytest -p no:cacheprovider forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py -q
  - python .agents/hooks/check_retrieval_header.py --changed --strict
  - python .agents/hooks/header_index.py --strict --base origin/main
  - python .agents/hooks/check_map_links.py --strict
  - python .agents/hooks/check_dcp_receipt.py --strict
  - python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/tiktok_promote_receipt_evidence_binding_delegated_adversarial_code_review_v0.md
  - git diff --check
```

## Pinned Target Bytes

These SHA-256 values are over the worktree file bytes at implementation commit
`4721a76bdd38659dd02db50d68e2884b820701d3`:

- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py` — `1ab18405392ff9cde07018ee6f0bca9f1d3bc76c00814b579578874829f30196`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py` — `3f17920114a5ba8e6b5c554b28f9693dedc56e9c8211651f6be043446b2600de`
- `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py` — `604777a309c47639737badd8d3e4ab78c599007ad2ca9bb7145cf4935758d4dd`
- `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md` — `85754cfdce9246fc7758a4e41f5820fe6b9044c056b7957cdda9ea9628d76340`

If a target hash differs before your edits, return `BLOCKED_SOURCE_DRIFT` with
the observed commit and hashes. Do not review or patch substituted bytes.

## Paste-Ready Commission Body

````markdown
You are the independent receiving controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

### 1. De-correlation gate

The implementation author and home adjudicator are OpenAI/GPT-family. Record
your exact model identity/version if known and permitted, plus its upstream
vendor lineage. You must be from a DIFFERENT vendor/model lineage. Host,
reseller, wrapper, and prompt differences do not count. If you are OpenAI/GPT
lineage, or your lineage is unknown or undisclosable, return only:

`BLOCKED_DECORRELATION`

This is a who-constraint, not a runtime-model recommendation.

Record this actor receipt before continuing:

```yaml
de_correlation_receipt:
  author_model_family: OpenAI GPT-family
  home_adjudicator_family: OpenAI GPT-family
  controller_model_identity: <observed identity/version or unrecorded>
  controller_vendor_lineage: <observed upstream vendor or unrecorded>
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: cross_vendor_discovery | BLOCKED_DECORRELATION
```

### 2. Repository and revision gate

- Repository: `https://github.com/eric-foo/forseti`
- Existing worktree when locally available:
  `C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\promote-receipt-evidence-binding`
- Expected branch: `codex/promote-receipt-evidence-binding`
- Implementation commit: `4721a76bdd38659dd02db50d68e2884b820701d3`
- Draft PR: `#849`
- Review baseline: current `origin/main`
- Allowed pre-review branch state: the implementation commit plus the filed
  commission prompt only; the four target blobs must match the pinned hashes.

Use the existing named checkout in place. Do not create, clone, switch, rebase,
reset, clean, commit, push, merge, or modify the PR. If repository access is
unavailable, return `BLOCKED_REPO_UNREADABLE`; do not reconstruct the target
from this prompt. If revision, branch, dirty state, or a target hash differs,
return `BLOCKED_SOURCE_DRIFT` with observed evidence and stop.

The ONLY implementation/contract files you may patch are:

1. `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py`
2. `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py`
3. `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py`
4. `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md`

The required durable review report is separately authorized at:

`docs/review-outputs/adversarial-artifact-reviews/tiktok_promote_receipt_evidence_binding_delegated_adversarial_code_review_v0.md`

Everything else is read-only and flag-only.

### 3. Source-gated method contract

The operating convention is
`.agents/workflow-overlay/delegated-review-patch.md`, provisional opt-in
explicitly commissioned by the owner. Use its
`delegated_code_review_and_patch` sibling mode for this bounded multi-file code
diff.

Run this sequence exactly:

1. `REFERENCE-LOAD` the instructions for `workflow-deep-thinking` and
   `workflow-code-review`; do not apply them yet.
2. `SOURCE-LOAD` the required repository sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing,
   stale, or conflicting paths.
4. Only after `SOURCE_CONTEXT_READY`, `APPLY` workflow-deep-thinking, then
   workflow-code-review, then the bounded patch authority below.

Required source reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- the full `origin/main...4721a76bdd38659dd02db50d68e2884b820701d3`
  diff and all four named target files
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
- `forseti-harness/capture_spine/creator_profile_current/registry_match_preflight.py`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_writer.py`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py`
- `forseti-harness/runners/run_tiktok_creator_discovery_register.py`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py`

The prior handoff packet is a consumed/stale checkpoint for this changed
frontier schema and preflight semantic. It may orient provenance only; it is
not authority and cannot replace any current source above.

### 4. Commission and contract-impact map

The implementation claims to make every `projection_decision: promote` depend
on candidate-bound Creator Registry preflight receipt evidence:

- retain legacy `registry_preflight_status_or_none` only as informational;
- add optional structured evidence to a candidate node, including opaque
  pointer, exact raw-byte SHA-256, candidate id, and copied clearance fields;
- require a caller-supplied repo/lake resolver for PROMOTE;
- resolve exact bytes, verify SHA-256, parse the expected receipt wrapper and
  v0 schema, validate summary/results consistency, select exactly one matching
  candidate row, compare copied fields, require
  `new_capture/new_candidate/allowed/true`, and bind normalized TikTok platform
  plus handle to the selected node;
- fail closed for missing, malformed, unrelated, hash-mismatched, negative, or
  candidate-mismatched evidence;
- preserve non-PROMOTE compatibility and the contract's non-claims.

Judge those claims against the current source. Do not trust this summary.

This is contract-sensitive. The authority order is current user commission,
`AGENTS.md`, Orca overlay, the TikTok frontier product contract, the Creator
Registry usage contract and producing implementation, then tests and prior
checkpoint orientation. The target product contract is patchable only to keep
it congruent with an accepted implementation correction; do not redesign the
Creator Registry receipt schema or broader workflow doctrine.

### 5. Adversarial review focus

Try to defeat the change, especially along these seams:

- Provenance versus self-certification: can a caller manufacture a
  positive-looking receipt plus matching self-supplied hash/resolver and clear
  PROMOTE without an owner-produced, repo/lake-bound, independently verifiable
  provenance fact? Distinguish a real defect from an explicitly accepted
  boundary; cite the owning source either way.
- Staleness: does the implementation actually detect every kind of "stale"
  receipt the product contract claims to fail closed on, including registry
  snapshot drift and receipt age, or only pointer-byte/hash drift? Do not invent
  a freshness policy; surface a contract/implementation mismatch if no owner
  exists.
- Candidate binding: candidate-id uniqueness, normalized platform/handle
  equality, URL/handle normalization, case and `@` handling, wrong-platform
  rows, duplicate or ambiguous rows, and mismatched copied clearance fields.
- Receipt integrity: wrapper/schema checks, exact-byte hashing, UTF-8/BOM
  handling, top-level and nested field types, bool-vs-int confusion, unknown or
  missing keys, summary/result consistency, empty results, duplicate ids, and
  builder-compatible evolution.
- Resolver boundary: exception handling, returned-type enforcement, opaque
  pointer handling, repeated reads/TOCTOU, and whether the API makes safe caller
  behavior possible without hidden filesystem or network authority.
- PROMOTE reachability: every validation entry point and caller path, selected
  node kind, missing resolver/evidence, scalar-only evidence, and any route that
  can avoid `_validate_promote_registry_preflight_evidence` yet still accept a
  PROMOTE register.
- Compatibility and blast radius: non-PROMOTE nodes, dataclass construction,
  dict serialization, register builder/runner/lake writer call sites, older
  v0 registers, enum/string comparisons, and error-code stability where tests
  or callers rely on it.
- Test quality: whether tests genuinely fail against the pre-fix behavior,
  cover the real builder output rather than a permissive fake, assert failure
  codes rather than any exception, and include negative cases for each
  load-bearing boundary. Flag fake-pass-prone tests.
- Contract honesty: no live capture, registry mutation, fuzzy identity proof,
  cross-platform identity proof, source-adequacy proof, freshness proof, or
  Capture authorization may be smuggled into the resulting claim.
- Smallest complete intervention: reject both under-fixes and unrelated
  cleanup. Every proposed edit must close a cited finding inside the named set.

### 6. Bounded patch authority

If the review finds a source-backed, implementation-level defect that can be
closed completely inside the four named target files, apply the smallest
complete patch in the existing worktree and leave it uncommitted. Add or amend
tests for testable corrections. Keep the product contract synchronized only
when its current statement would otherwise become false.

Do not patch read-only sources, the commission prompt, overlay/doctrine,
runner/lake integrations, the Creator Registry builder, unrelated tests, or
generated/provenance artifacts. Do not commit, push, rebase, merge, open or
modify PRs, run live capture, mutate a registry, access a live lake, or perform
network capture.

If the correct closure requires a receipt-schema redesign, new provenance
authority, freshness policy, runner/lake architecture, a patch outside the
named set, or any doctrine change, return `NEEDS_ARCHITECTURE_PASS`, findings
and citations only, with NO partial patch.

### 7. Validation and output contract

Run the focused test first after any patch:

`python -m pytest -p no:cacheprovider forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py -q`

Then run the applicable repository gates named in the prompt preflight. Report
the exact command, exit code, and concise observed output. Never convert a
not-run check into a pass. For a testable fix, provide same-check red/green
evidence when safely possible; otherwise label the replacement evidence as
weaker and say why.

Write the full findings-first report to the exact required output path. Each
finding must include: id, severity, confidence, file/line or stable anchor,
implementation evidence, controlling authority/evidence basis, correctness or
validation impact, `minimum_closure_condition`, `next_authorized_action`, and
red/green status. Include considered-and-defended non-findings where an
adversarial concern is materially important but the implementation is sound.

After the report's final write, run:

`python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/tiktok_promote_receipt_evidence_binding_delegated_adversarial_code_review_v0.md`

Return only a compact human summary, review courier YAML, and this block:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

- original commission and exact target
- de_correlation_receipt
- source_context_status and read ledger
- findings with decision-sufficient citations
- considered-and-defended items
- patch summary and unified diff, if authorized and applied
- exact validation results and not-run checks
- reviewer verdict as decision input only
- residual risks, off-scope flags, and not-proven boundaries
- NEEDS_ARCHITECTURE_PASS state, if triggered
```

Your findings, diff, citations, validation statements, and verdict are claims
for the home model/Chief Architect to adjudicate. They are not acceptance,
approval, readiness, merge authority, source promotion, or proof that no new
seam exists. The home adjudicator may accept, modify, or reject every proposed
change and must fresh-read the resulting diff before any keep decision.
````

## Operator Dispatch and Return

- Route the paste-ready body to a repo-capable controller whose upstream vendor
  lineage differs from OpenAI/GPT. A same-family Codex subagent is forbidden as
  the claimed de-correlated review.
- Courier the full returned summary and durable-report path back to this task.
  The home model then adjudicates every finding and patch before keeping any
  change.
- This filed commission does not itself perform the review, validate the patch,
  authorize merge, or make PR #849 ready.
