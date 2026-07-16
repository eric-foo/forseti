# Creator Audience Triangulation Onboarding — Delegated Review and Patch Commission

```yaml
retrieval_header_version: 1
artifact_role: delegated_review_dispatch_prompt
scope: Cross-vendor code review-and-patch commission for the creator-audience triangulation onboarding cutover.
use_when:
  - Dispatching the bounded review of the pinned audience-triangulation implementation revision.
  - Verifying the review scope, two-root receiver contract, or return requirements for this lane.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
stale_if:
  - The pinned implementation revision, named target scope, or accepted cutover decisions change.
```

Paste this prompt into a fresh external controller from a different vendor/model lineage than the OpenAI/GPT authoring lane.

## Forseti Prompt Preflight

- **output_mode:** `paste-ready-chat`; return the review result to the commissioning Chief Architect in chat. Repository patches are permitted only as bounded below.
- **template_kind:** `none` (eligible lane-scoped delegated patch prompt).
- **edit_permission · targets · branch:** `patch-only`; target worktree `C:\Users\vmon7\Desktop\projects\forseti-worktrees\5d17\orca`; branch `codex/creator-audience-triangulation-onboarding`; exact implementation revision `f64ff829320f8aa61da0d6664faf580eaefa6b44`; target files are exactly the added, modified, or deleted paths reported by `git diff-tree --no-commit-id --name-status -r f64ff829320f8aa61da0d6664faf580eaefa6b44`. The branch may contain one later prompt-only commit adding this commission, but no later code/product/test changes are allowed before review.
- **reviews:** findings-first, coverage-first delegated code review and bounded patch pass; formal verdict required.
- **doctrine_change:** no product, architecture, workflow, validation, review, or lifecycle direction change is authorized. If correct closure requires one, return `NEEDS_ARCHITECTURE_PASS` instead of patching it.
- **destinations:** this file is the run-authoritative input. Patch the effective target worktree directly; return the report in the couriered chat. Do not create a durable review report.

## Commission

### Goal and done condition

Adversarially review and, where authorized, patch the smallest-complete TikTok creator-audience triangulation onboarding cutover. Done means the implementation truthfully requires both transcript and captured-comment evidence, consumes persisted mechanical Silver facts, keeps semantic inference in Judgment through one creator-isolated subscription context with zero model API calls, validates exact claim/evidence closure, projects the accepted snapshot into Creator Registry, preserves capture-time provenance, and removes the superseded executable ideal-audience path without breaking unrelated active extraction lanes.

Treat these as accepted design decisions, not review invitations:

1. Both transcript and comment modalities are mandatory; absence of either fails visibly as `INCOMPLETE_AUDIENCE_EVIDENCE` and writes no partial Judgment/profile.
2. Silver persists mechanical facts and lineage only; audience conclusions remain Judgment.
3. One creator is interpreted in one cold subscription context. API-level model batching and model API calls are forbidden.
4. The old executable ideal-audience path is directly retired without compatibility aliases. Historical Git evidence is sufficient; current executable/product authority must not retain a competing path.
5. Aggressive commercial language is allowed, but every claim must retain evidence closure and must not manufacture majority, demographic, or guaranteed-outcome certainty.

### Author and reviewer independence

- `authored_by`: OpenAI / GPT family.
- Required delegate: a different vendor/model lineage, normally Anthropic / Claude family. Record the actual `reviewed_by` model/version; never invent it.
- `de_correlation_bar`: `cross_vendor_discovery`.
- The delegate reviews and patches; the commissioning Chief Architect adjudicates every finding and returned change before it is kept.

### Mandatory two-root receiving preflight

Before loading target sources:

1. Record `launch_checkout` and its harness write scope.
2. If it is not the commissioned worktree, inspect `git worktree list --porcelain` for the named branch/revision. A launch/target mismatch is a resolution trigger, **not** an automatic blocker.
3. Resolve exactly one accessible worktree containing implementation revision `f64ff829320f8aa61da0d6664faf580eaefa6b44` on branch `codex/creator-audience-triangulation-onboarding`. Confirm that any descendant commits change only this prompt before treating the current branch tip as the patch base.
4. Prove direct write capability in that target under the active harness and confirm no concurrent writer. Read access or the existence of the path is not write proof.
5. Bind the resolved path as `effective_target_worktree`; use target-rooted workdirs, absolute paths, and `git -C <effective_target_worktree>`. Never reconstruct or check out the target into the launch checkout.
6. Recheck revision/ancestry and dirty state immediately before the first edit. The expected initial target is clean. Stop as `BLOCKED_TARGET_DRIFT_DURING_REVIEW` if target code/product/test bytes changed.
7. Return `BLOCKED_RECEIVER_REROOT_REQUIRED` only if the target is absent, ambiguous, inaccessible, mismatched, not demonstrably writable, concurrently changing, or the harness actually requires a target-rooted receiver you cannot provide. State the failed capability fact.

### Source loading and method

Read completely before findings or edits:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/prompt-orchestration.md` sections `Lane-Scoped Delegated Patch Prompt Default` and `Repo-Bound Review Target Resolution`
4. `.agents/workflow-overlay/delegated-review-patch.md` review/patch authority, access-selection, return, and hard-stop rules
5. `.agents/workflow-overlay/review-lanes.md` review doctrine and rules
6. the available `workflow-deep-thinking` and `workflow-code-review` skills, then apply them in that order after target source context is ready
7. the exact implementation diff and every current owner it touches, including the controlling triangulation product contract and relevant Bronze/Silver/Cleaning/Judgment/Creator Registry boundaries

Use `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md#environment_baseline` for repo-constant environment facts. Do not import policy from another repository.

### Review priorities

Search coverage-first for every failure mode, including low-confidence and low-severity candidates. Concentrate on:

- evidence-ID and raw-pointer correctness across embedded batch/grid/comment artifacts;
- capture-time comparability and protection against grid/comment observation-time mismatch;
- creator isolation, packet-scoped processing, duplicate handling, engagement salience versus truth, and outsized-video/comment safeguards;
- strict schema closure, malformed-output visibility, canonical IDs/hashes, no partial writes, and no hidden API path;
- the prepare/validate subscription boundary and the claim that model API calls remain zero;
- Creator Registry materialization/validation, identity-only creators, generated static view consistency, and stale old-field removal;
- active imports and data-lake lane/inventory/policy-pin consistency after legacy deletion and transport extraction;
- whether the new local skill triggers during full onboarding/on-demand generation but not comparisons, copy critique, or unrelated maintenance;
- test adequacy for the accepted decisions and the real onboarding packet shape.

Do not restore the old architecture merely because the diff is large. Do not widen comment capture, perform live capture, call any model API, mutate live lakes/Creator Registry, or publish profiles as validated truth.

### Patch authority

You may directly patch only a defect necessary to make the accepted cutover correct, coherent, and testable. Keep patches within the implementation revision's changed path set, plus directly corresponding tests in that set. You may not add product scope, schemas for speculative futures, compatibility aliases, new capture behavior, review artifacts, commits, or lifecycle actions. If a material issue cannot be closed inside those bounds, report it and use `NEEDS_ARCHITECTURE_PASS` when it is design-level.

### Validation

Observed authoring baseline after rebase onto `origin/main` (`71e85f80ca9eb6240e2a988b22689628f7166524`):

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q forseti-harness/tests/unit forseti-harness/tests/contract --basetemp C:/tmp/pytest_tri_final3
```

This completed exit `0`, with four expected skips and only pre-existing `datetime.utcnow()` deprecation warnings. The earlier two-minute rerun timed out at 50% with no failures; it is not validation evidence and must not be reported as a pass.

At minimum, run the targeted triangulation, comment/grid producer, registry static-view, lane-registry, policy-pin, and lake-seam tests. If you patch, rerun every materially affected test and the full unit+contract command above. Report each command as `passed`, `failed`, `blocked`, or `not_run`; never convert a timeout or missing dependency into success.

### Return contract

Return, in this order:

1. `reviewed_by`, `authored_by`, `de_correlation_bar`, `launch_checkout`, `effective_target_worktree`, resolution method, direct-write proof, no-concurrent-writer receipt, target revision/ancestry, and pre-edit dirty state.
2. Findings ordered by severity. Each finding includes confidence, exact neutral file/line citations, why it violates an accepted decision/source, `minimum_closure_condition`, whether patched, and `next_authorized_action`. Include low-confidence/minor findings rather than filtering them out.
3. `considered_and_defended`: one line per plausible candidate defeated by a concrete steelman defense.
4. Bounded diff summary with exact files changed and why each line group was necessary; say `no patch` if none.
5. Validation evidence with actual command/result summaries.
6. Formal verdict: `PASS_PATCHED`, `PASS_NO_PATCH`, `BLOCKED`, or `NEEDS_ARCHITECTURE_PASS`.
7. Residual risks and not-proven boundaries.

Review findings and patches are decision input only until the commissioning Chief Architect adjudicates them. Hard stop: do **not** commit, push, open/update a PR, merge, stash, reset, clean the worktree, delete branches, run repository hygiene, or perform any other lifecycle action.
