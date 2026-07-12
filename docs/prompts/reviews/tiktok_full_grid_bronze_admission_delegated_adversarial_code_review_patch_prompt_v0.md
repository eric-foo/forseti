# TikTok Full-Grid Bronze Admission — Delegated Adversarial Code Review-and-Patch Commission v0

```yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code review-and-patch commission
scope: >
  Different-vendor review and bounded patch pass for the TikTok batch writer
  change that preserves a complete onboarding grid window and its bound
  selection receipt beside selected-video deep captures in one Bronze packet.
use_when:
  - Reviewing branch codex/tiktok-full-grid-bronze-admission before merge.
authority_boundary: retrieval_only
```

## Forseti Start Preflight

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom bounded TikTok Bronze admission diff
  edit_permission: implementation-authorized
  target_scope: five named TikTok writer/runner/test files plus this review prompt; no live capture, registry mutation, graph projection, or longitudinal grid logic
  dirty_state_checked: yes
  blocked_if_missing: exact target worktree/branch ancestry, clean target state, five target hashes, named overlay/review sources, focused validation route
```

## Goal And Success Signal

Goal: adversarially verify and, only where a confirmed defect requires it, patch
the smallest complete TikTok Bronze admission change so one onboarding packet
preserves the full observed grid, its exact bound selection receipt, and the
selected deep captures without breaking legacy batch or Silver consumers.

Done means the controller has read the real diff and target sources, reported
coverage-first findings, applied only bounded confirmed-defect fixes, rerun the
named validation, written the durable report, and returned the diff as decision
input for Chief Architect adjudication. No controller change is kept merely
because it was proposed.

## Lane And Actor Binding

- target_kind: `delegated_code_review_and_patch`
- access: `repo`
- review_lane: `workflow-code-review`
- mode: `base-subagent`
- operating_contract: `.agents/workflow-overlay/delegated-review-patch.md`
- author_home_model_family: OpenAI / GPT-5 Codex
- controller_model_family: operator must record the actual non-OpenAI vendor/model
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- de_correlation_status: satisfied only when the controller vendor differs from OpenAI
- no tester/testee shortcut: if the receiver is OpenAI-family, stop with
  `BLOCKED_CONTROLLER_NOT_DECORRELATED`; do not self-review or spawn a replacement
  reviewer from this commission.

## Target-State Preflight

Repository target:

- worktree: `C:\tmp\forseti-tiktok-full-grid-bronze-admission`
- branch: `codex/tiktok-full-grid-bronze-admission`
- required base ancestry: `41b078e3ed3c6bcf1424588a8dc8423f3f1c19fc`
- review range: required base through the branch HEAD observed at review start
- dirty-state allowance: clean at review start; the controller's later bounded
  edits and report file are expected review outputs
- untracked files at review start: none allowed

If the launch checkout is not this target, inspect registered worktrees and use
the unique worktree satisfying the branch and ancestry. Do not review a summary,
context pack, recreated copy, alternate branch, or substitute checkout.

Before findings, verify these exact target hashes:

```text
1e87014a16356ab5d157b909a93954612aed20116077d90b0323bb399bd03473  forseti-harness/source_capture/tiktok/batch_packet.py
d5b66f5040906fabe2a9e480ad39655faba8ac7abcce226bec8d6ca81b025261  forseti-harness/runners/run_source_capture_tiktok_batch_packet.py
d66fde49d950a7a4621a77a834775e9614dcb6ca091a71d4a50d8d759e9dd517  forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py
cc689844401028823c2b4a3b194fa8d663ef7025a3c5c5d0b52ef9a733dcef35  forseti-harness/tests/unit/test_tiktok_batch_admission.py
628423f8c201210a556801e76af32c1a1282fd8c83f6dbb291b01ab0d5872b58  forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
```

A hash mismatch, wrong branch/ancestry, disallowed dirt, missing target, or
additional changed code file blocks review. Report the exact mismatch; do not
repair preflight state.

## Editable Scope

The controller may patch only these five files:

1. `forseti-harness/source_capture/tiktok/batch_packet.py`
2. `forseti-harness/runners/run_source_capture_tiktok_batch_packet.py`
3. `forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py`
4. `forseti-harness/tests/unit/test_tiktok_batch_admission.py`
5. `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`

Everything else is read-only and flag-only. Do not widen into grid
supersession/delta projection, link-hub traversal, Creator Registry mutation,
automatic admission policy, browser behavior, selection policy redesign, or
unrelated cleanup. A correct fix requiring architecture or off-scope edits
returns `NEEDS_ARCHITECTURE_PASS`, reverts partial controller edits, and
reports findings only.

## Required Reads And Method Order

Read the following before strict findings:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- the targeted sections and overlay interface in
  `.agents/workflow-overlay/delegated-review-patch.md`
- the complete five-file diff from the required base
- all five target files in full
- directly called packet-assembly and TikTok batch-reader code only where a
  concrete candidate finding requires it

Apply `workflow-deep-thinking` to frame the shared evidence-contract risks,
then apply `workflow-code-review`. If either required method is unavailable,
return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Fitness Contract

The intended behavior is:

1. Existing callers that supply only the selected-video grid result and cadence
   inputs remain supported and preserve the pre-change one-file packet shape.
2. A full onboarding evidence pair is optional for legacy callers but strictly
   both-or-neither.
3. When supplied, the exact sanitized grid-window and selection bytes are
   preserved as separate raw files in the same immutable packet as the batch
   capture payload.
4. Admission fails before packet publication when creator identity, grid
   completeness/size/uniqueness, video URLs, selection coverage, ranked rows,
   byte-hash binding, selected-row truth, or selected-vs-deep-captured IDs do
   not agree.
5. Split recovery cadence input may differ in run order; selected/deep-captured
   identity is therefore compared as a unique set, never by synthetic order.
6. The batch payload carries explicit hashes, schema versions, counts, and true
   verification booleans for the preserved onboarding evidence.
7. Supervised onboarding passes the full grid and selection to the existing
   writer whenever admission is requested.
8. The standalone batch runner accepts the same pair so already-captured
   staging can be admitted without another browser run.
9. The change does not claim longitudinal current-view semantics, deletion,
   supersession, graph updates, selection correctness, metric validity, or
   automatic data-lake admission.

Attack this fitness reference as an alignment axis, not a pass-if-matches bar.

## Adversarial Questions

At minimum, challenge:

- Can malformed, author-mismatched, stale-hash, partial, duplicate, or unrelated
  grid/selection inputs publish any packet?
- Can a selection claim one set while ranked rows or cadence admit another?
- Can split recovery runs create duplicates, omit a selected video, or admit an
  unselected video without failing?
- Are preserved-file IDs computed after the final staged file list, and do
  manifests/source slices expose all three exact files?
- Can exact-byte preservation leak material that the parsed safety check misses?
- Does the v1 schema bump break any current batch coverage, projection, Silver,
  inventory, or policy-version consumer?
- Are path/name checks portable and are TikTok handle comparisons correctly
  case-insensitive?
- Does the standalone runner truthfully record all four input receipts?
- Does onboarding wire the full artifacts only after successful staging, and
  does any admission failure remain visible?
- Are the tests strong enough to fail on swapped files, stale hashes, missing
  pair members, mismatched IDs, and accidental legacy-shape changes?

Report every issue found, including minor and low-confidence findings. Each
actionable finding must include severity (`critical|major|minor`), confidence
(`high|medium|low`), evidence, impact, `minimum_closure_condition`, and
`next_authorized_action`. Put steelman-defeated candidates in
`considered_and_defended`.

## Validation

Baseline evidence from the authoring lane; verify rather than trust:

- focused TikTok writer/onboarding tests: 40 passed
- expanded TikTok admission/coverage/projection/live-batch/onboarding suite:
  101 passed
- full `forseti-harness/tests/contract`: 125 passed
- actual Noel staging proof: one packet with 29 grid rows, 8 selected/deep
  captures, three preserved files, both stored hashes matching, and both
  linkage verification booleans true
- `git diff --check`: exit 0

After any controller patch, rerun at least:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest-tiktok-bronze-review forseti-harness/tests/unit/test_tiktok_batch_admission.py forseti-harness/tests/unit/test_tiktok_batch_coverage.py forseti-harness/tests/unit/test_tiktok_batch_projection.py forseti-harness/tests/unit/test_tiktok_live_batch_probe.py forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest-tiktok-bronze-review-contract forseti-harness/tests/contract
git diff --check
python .agents/hooks/check_review_routing.py --strict
```

Every command must report pass, fail, blocked, or not run with reason. Do not
convert missing tooling or a failed command into success.

## Output Contract

Output mode: `review-report`.

Write the durable report to:

`docs/review-outputs/tiktok_full_grid_bronze_admission_delegated_adversarial_code_review_v0.md`

The report must record `reviewed_by` and `authored_by` using observed
operator/tooling provenance; use `unrecorded` rather than fabrication. Include
findings first, considered-and-defended candidates, the bounded working-tree
diff, validation evidence, verdict, and residual risks. Run the applicable
review-output provenance checker after the write and report its result.

Return a compact courier summary to the commissioning Chief Architect. The
findings, citations, diff, verdict, and residuals are claims to adjudicate, not
premises to inherit. The Chief Architect must accept, modify, or reject each
material change, close self-closable material issues in the same adjudication
turn, and then batch commit/push/PR/merge into one land step only after no
unresolved material issue remains.

## Lifecycle Hard Stop

Do not commit, push, create or update a PR, merge, stash, reset, clean the
worktree, remove worktrees, or perform repository hygiene. Do not run live
TikTok/browser capture or write to a production data lake. Stop after the
bounded review patch, validation, report, and courier summary.
