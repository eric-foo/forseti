# Creator Commercial Projection Calibration Delegated Adversarial Artifact Review And Patch

```yaml
retrieval_header_version: 1
artifact_role: Forseti delegated adversarial artifact review-and-patch prompt
scope: >
  Cross-vendor adversarial review and bounded patching of the Creator Signal
  commercial-projection contract, required calibration deck, and spine router.
use_when:
  - Hardening the commercial-projection calibration surface before merge.
  - Testing whether a cold author can derive creator-specific buyer value without copying examples or inventing claims.
authority_boundary: retrieval_only
```

## Goal And Success Signal

**Goal:** make routine cold authors consistently turn audience-triangulation
evidence into creator-specific, maximally commercial hiring propositions while
preserving exact evidence, uncertainty, and the controlling claim ceiling.

**Done looks like:** the controlling contract remains the claim authority; every
commercial-panel author is reliably routed to one subordinate calibration deck;
the deck teaches a reusable evidence-to-buyer-value transformation without
becoming a closed creator taxonomy; its examples calibrate force and specificity
without becoming reusable claims; and its gates reject generic, copied, or
unsupported output.

Treat the goal and success signal as review axes to attack, not a pass bar.

## Commission And Two-Root Preflight

```yaml
forseti_prompt_preflight:
  output_mode: chat-only
  template_kind: review
  edit_permission: patch-only
  branch: codex/audience-commercial-projection-contract
  review_style: findings-first delegated adversarial artifact review-and-patch
  doctrine_change: product_doctrine
  review_destination: current controller chat; return to commissioning Chief Architect
commission:
  access: repo
  target_kind: authored_artifact
  author_home_family: OpenAI
  controller_family: operator_to_fill_must_differ_from_OpenAI
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  launch_checkout: operator_to_fill
  effective_target_worktree: C:/tmp/forseti-audience-commercial-projection-contract
  expected_branch: codex/audience-commercial-projection-contract
  required_ancestry: d94b2daf27189b797fdbacc24267f403d6230972
  dirty_state_allowance: clean at review start; controller-created named-scope edits only thereafter
  untracked_files_in_scope: no
```

Before loading target sources:

1. Record `reviewed_by`, including model/version and vendor lineage. The
   author/home family is OpenAI; the controller must be a different vendor/model
   lineage. Otherwise return `BLOCKED_CONTROLLER_NOT_DECORRELATED` without
   reviewing or patching. This is a who-constraint, not a model recommendation.
2. Record the actual `launch_checkout` and harness write scope. If it is not the
   commissioned worktree, inspect registered Git worktrees for the named branch
   and required ancestry before blocking. A launch-root mismatch is a resolution
   trigger, not an authentication or authorization failure.
3. When exactly one accessible worktree matches, bind it as
   `effective_target_worktree`, use absolute target-rooted workdirs or
   `git -C`, and prove the harness can directly write that root. Merely reading
   it is not proof. Do not ask the operator to reauthorize a reroot when the
   harness already permits direct target writes.
4. Confirm the effective target is on the expected branch, the required commit
   is an ancestor of `HEAD`, the worktree is clean, all named files exist, and
   their clean-filtered Git blob IDs match the target manifest below. Verify
   each with `git hash-object --path=<path> <path>` so Windows line-ending
   checkout differences cannot create a false mismatch. If any identity check
   fails, return `BLOCKED_RECEIVER_REROOT_REQUIRED` with the observed mismatch.
5. Do not switch, reconstruct, copy, or review a substitute checkout, summary,
   context pack, or recreated source. Do not stash, reset, clean, or delete.

### Target manifest

| Label | Path | Git blob ID |
| --- | --- | --- |
| `[spine-router]` | `forseti/product/spines/creator_signal/README.md` | `d04ea5a5ef879eb2fef05c3049ac8d1399be3e55` |
| `[controlling-contract]` | `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md` | `266e4763b7bce30f1ad3023173051800a01afa72` |
| `[calibration-deck]` | `forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md` | `9b4d17bd781b084e02d8dbd425bce5caaf59aa92` |

## Required Reads And Method

After preflight, read:

- `AGENTS.md` and `.agents/workflow-overlay/README.md`;
- `.agents/workflow-overlay/delegated-review-patch.md`: “When it applies”,
  “The loop”, “Access selection rule”, “De-correlation”, “Overlay Interface”,
  and delegate lifecycle hard stop;
- `.agents/workflow-overlay/review-lanes.md`;
- `.agents/workflow-overlay/source-of-truth.md`: Doctrine Change Propagation;
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` ->
  `environment_baseline`;
- the complete `main...HEAD` diff and all three named targets;
- the complete `workflow-adversarial-artifact-review` skill available to the
  controller runtime.

REFERENCE-LOAD the review method before reviewing. Declare
`SOURCE_CONTEXT_READY` only after the real target and authority sources are
loaded. Then APPLY `workflow-adversarial-artifact-review` findings-first. If the
skill is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Named Patch Scope

The controller may patch only:

- `[spine-router]` `forseti/product/spines/creator_signal/README.md`;
- `[controlling-contract]`
  `forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md`;
- `[calibration-deck]`
  `forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md`.

Everything else, including this prompt, is read-only and flag-only. Do not edit
AGENTS.md, overlays, repo maps, tests, runtime/model code, capture or data-lake
artifacts, prior profiles, scratch dogfood, or review outputs. A necessary fix
outside the named set requires re-commissioning; do not widen scope.

Read-only review is insufficient because the commission authorizes the
de-correlated controller to close confirmed defects while the source context is
hot. Patch only findings supported by neutral, decision-sufficient citations.

## Review Questions

Be maximally adversarial and coverage-first. In particular:

1. Does every cold actor creating or materially rewriting a commercial panel
   have a deterministic retrieval route from the spine and controlling contract
   to the calibration deck, without depending on chat memory or an inactive
   distillation binding?
2. Is authority single-sourced: the contract owns claim permission while the
   deck teaches transformation, with no contradiction or silent authority fork?
3. Is a separate deck justified by its distinct future authoring consumer, and
   is it independently usable with authority, currentness, and next-source facts?
4. Can the transformation reliably get from non-obvious evidence to buyer
   tension, creator-specific commercial role, product meaning, mechanism,
   campaign jobs, and wrong-hire boundary without forcing purchase influence?
5. Do the Noel, Cologne Crown, and FB patterns calibrate strength and specificity
   while clearly remaining examples rather than a taxonomy or reusable claims?
6. Do the paid-delta, substitution, mechanism, claim-ceiling, campaign-action,
   and non-copy gates catch generic, copied, unsupported, or commercially weak
   output? Are any gates redundant, gameable, or likely to force fake certainty?
7. Does maximum-defensible-aggression remain commercially forceful without
   fabricating conversion, prevalence, demographics, ROI, or guaranteed
   performance?
8. Is the cold-agent dogfood gate smallest complete, reproducible, and honest
   about what one held-out success can and cannot prove?
9. Are the README routing and both Direction Change Propagation receipts
   complete, non-duplicative, and faithful to the actual touched surfaces?
10. Did the change add unnecessary runtime, schema, model, harness, distillation-
    binding, telemetry, or maintenance commitments?

## Validation

Run from the effective target worktree. Every command may fail; report exact
results and do not weaken a check to obtain green.

```powershell
git diff --check origin/main...HEAD
python .agents/hooks/check_retrieval_header.py --strict forseti/product/spines/creator_signal/README.md forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md
python .agents/hooks/check_dcp_receipt.py --strict --base origin/main
python .agents/hooks/check_dcp_receipt_hygiene.py --strict forseti/product/spines/creator_signal/README.md forseti/product/spines/creator_signal/creator_audience_triangulation_and_commercial_projection_v0.md forseti/product/spines/creator_signal/creator_commercial_projection_calibration_deck_v0.md
python .agents/hooks/check_repo_map_freshness.py --strict --diff origin/main
```

If a listed command is unsupported by the checker version, report it as not run
with the exact CLI mismatch and run the nearest documented diff-scoped strict
form; do not silently substitute. The author observed a successful held-out
Funmi replay after an initial empty transport return: the cold author derived
“scent choreographer who installs a wearing habit,” copied none of the three
example roles, bound exact evidence/video IDs, and passed all six deck gates.
Treat that as bounded author evidence, not general reliability, buyer proof, or
a substitute for this review.

## Controller Return And Hard Stops

Return findings first. Every finding must carry its target label, tight
`file:line` citation, severity (`critical`, `major`, or `minor`), confidence
(`high`, `medium`, or `low`), concrete failure mechanism, affected author/buyer
behavior, `minimum_closure_condition`, and `next_authorized_action`.

Also return:

- `considered_and_defended` for steelman-defeated candidates;
- one bounded unified diff for controller-authored changes, labeled by target;
- neutral, decision-sufficient citations for every change;
- validation commands and observed results, including failures and not-run gates;
- overall verdict and per-target sub-verdicts when materially different;
- residual risks and off-scope flags;
- `reviewed_by` and `authored_by` (`OpenAI GPT-5`), using `unrecorded` rather
  than fabricating any unavailable value.

If a design-level problem prevents a bounded fix, return
`NEEDS_ARCHITECTURE_PASS`, revert any partial controller diff, and return
findings only.

Do not commit, push, open/update a PR, merge, stash, reset, clean, remove a
worktree, run repository hygiene, or perform any lifecycle action. The returned
findings, diff, citations, verdict, and residuals are claims for the home/Chief
Architect to adjudicate, not premises to keep. The home model must accept,
modify, or reject each material change against its citations before anything is
kept.
