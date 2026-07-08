# Fused Delegated Review Gate Tightening Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Cross-lane prompt to evaluate and, if authorized, tighten fused delegated-review checkpoint behavior.
use_when:
  - Asking an agent-workflow lane to settle whether fused is too lenient when delegated review exposes multiple material defects.
  - Preparing a source-backed patch or patch proposal for fused / implementation-scoping review gate semantics.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/decision-routing.md
```

## Orca Prompt Preflight

- Output mode: `file-write` for this Orca prompt artifact at `docs/prompts/patches/fused_delegated_review_gate_tightening_patch_prompt_v0.md`; paste-ready copy may be couriered to the receiving agent-workflow lane.
- Template kind: `patch` / workflow-doctrine settlement prompt; no Orca-local implementation authority is granted by this file.
- Edit permission / targets / branch: current Orca lane is docs-write only for this prompt. The receiving lane must bind its own canonical source repo, branch, dirty-state allowance, edit authority, target files, and validation before patching.
- Reviews: findings-first if the receiving lane performs review. Any formal verdict, severity, or patch queue must be explicitly bound by that lane.
- Doctrine change: this prompt asks about workflow authority / review authority semantics. Any source-changing resolution must carry the receiving repo's doctrine-change propagation or equivalent closeout evidence.
- Destinations: this prompt is the input artifact. Receiving-lane output destination is unbound here; if the receiver writes a report or patch artifact, it must name its exact path before claiming it exists.

## Cynefin Routing Seed

Smallest complete outcome: decide whether fused's `recommended` delegated-review path is too permissive for high-risk or error-dense work, and produce the smallest source-backed patch or patch proposal that fixes the gate without making routine fused lanes grind to a halt.

Regime: Complicated with a workflow-doctrine edge.

Why: the existing skills already encode review timing, but the boundary between `recommended` and hard checkpoint behavior may be miscalibrated for source-critical or fake-pass-prone lanes.

Decomposition: risk-first source read, then smallest complete contract patch.

Current bottleneck: identify the canonical source of the review-timing rule and decide whether the fix belongs in `workflow-implementation-scoping`, `fused`, `workflow-delegated-review-patch`, or their interaction.

Riskiest assumption: that "recommended post-implementation review" is enough when the expected or observed review defect density is high.

Stop or pivot condition: if the receiving lane cannot verify canonical source authority or write authority, stop with a patch proposal instead of editing installed or copied skill files.

Allowed next move: source-load the named skill sources, classify the gap, then patch only the bound canonical source or return a patch proposal.

Disallowed next move: do not edit installed/user-level/plugin cache copies unless the lane explicitly establishes that they are the canonical editable source; do not add broad review ceremony to all fused runs.

## Objective

Settle this concern:

> The fused skill appears too lenient when delegated review can discover many material defects. The current distinction between `adversarial_review: recommended` and `required_by_bound_gate` may let source-critical work proceed too far before a hard checkpoint exists.

The goal is not "always require review." The goal is to prevent false-closeout or late-review failure in lanes where review-risk is structurally high: reusable workflow-kernel behavior, source-critical parsers, authority/review-routing semantics, validation/evaluator/fake-pass surfaces, hard lifecycle surfaces, or an already-observed pattern where delegated review found multiple material defects.

## Source-Gated Method Contract

1. REFERENCE-LOAD the method/skill instructions named below. Do not APPLY them yet.
2. SOURCE-LOAD the task-specific skill sources and any receiving-repo overlay authority.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY the methods to diagnose the gate and propose or make a patch.
5. Every load-bearing claim must cite `file:line` or the receiving lane's equivalent source reference. If line numbers are unavailable, cite path plus the exact heading and say line numbers unavailable.

If you do not have repo/filesystem access to the named sources, stop and request a source capsule. Do not infer current skill behavior from this prompt alone.

## Required Source Reads

Resolve the canonical editable source first. The local observed copies were:

- `C:/Users/vmon7/.codex/skills/fused/SKILL.md`
- `C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.85/skills/fused/SKILL.md`
- `C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.85/skills/workflow-implementation-scoping/SKILL.md`
- `C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.85/skills/workflow-delegated-review-patch/SKILL.md`
- `C:/Users/vmon7/.codex/skills/workflow-prompt-orchestrator/SKILL.md` or the canonical prompt-orchestrator source available to your lane.

Use these as case-study inputs only if available; they are not authority over the agent-workflow source:

- `docs/review-outputs/instagram_reels_grid_parser_advisory_code_review_v0.md`
- `docs/prompts/reviews/instagram_reels_grid_parser_adversarial_code_review_prompt_v0.md`
- `orca-harness/source_capture/ig_reels_grid.py`
- `orca-harness/tests/unit/test_ig_reels_grid.py`

## Observed Case Study To Verify, Not Trust Blindly

In the Orca IG parser lane, a delegated/adversarial review surfaced multiple material issues after the first implementation direction, including:

- ambiguous hidden numeric engagement values could be misclassified as likes/comments;
- device timestamps or invalid epochs could be treated as publication fallback;
- recursive media matching risked false joins;
- play-count / view-count candidate provenance needed preservation;
- DOM row dedup needed normalized shortcode/path handling.

These were patch-worthy issues, not style nits. Verify against the review output and diff if those sources are in your accessible workspace. If unavailable, treat this section as an anecdotal risk signal, not proof.

## Settlement Questions

Answer these in order:

1. Where is the current gate actually defined: implementation-scoping's Review Timing Advisory, fused's checkpoint routing, delegated-review-patch's terminal/orchestrator behavior, or a combination?
2. Is the existing `recommended` -> post-implementation delegated-review handoff sufficient for high-risk source-critical lanes, given that the review may find multiple material defects?
3. Should the system add a harder gate, expand the meaning of an existing gate, or change closeout semantics after recommended review returns material findings?
4. What is the smallest complete patch that prevents false closeout without requiring adversarial review for routine, local, reversible changes?
5. What exact validation or fixture can fail if the gate regresses?

## Candidate Direction To Challenge

Do not accept this blindly, but use it as the hypothesis to test:

- Keep `recommended` non-blocking for normal fused lanes.
- Introduce or tighten an explicit escalation rule for source-critical / fake-pass-prone / reusable-kernel lanes where review is not just helpful but risk-bearing before dependent work or closeout.
- Prefer placing the primary risk classification in `workflow-implementation-scoping`, because it already emits the Review Timing Advisory and checkpoint.
- Make `fused` preserve and enforce the stronger checkpoint without adding a parallel status family.
- Make `workflow-delegated-review-patch` keep its role: render or route the delegated prompt and require home-model adjudication, but not own initial risk classification unless its own source says otherwise.
- After a delegated review returns multiple blocker/major/material findings, require explicit home-model adjudication before any final closeout claim. Do not let "review was routed" equal "review was resolved."

Possible vocabulary options to evaluate:

- Expand `required_by_bound_gate` so the "bound gate" may come from loaded workflow-kernel risk rules, not only repo-local external authority.
- Add a new value only if necessary, such as `required_by_risk_gate`, but avoid parallel status vocabulary unless the current schema cannot express the distinction.
- Add a material-findings return rule instead of a pre-implementation gate if that better matches existing fused sequencing.

## Patch Constraints

- Preserve fused's purpose: a low-latency one-turn sequence for routine implementation lanes.
- Do not make adversarial review mandatory for every `recommended` case.
- Do not weaken existing `required_by_bound_gate` semantics.
- Do not collapse delegated review into self-review or local same-family review.
- Do not treat prompt rendering, review execution, patching, and home-model adjudication as the same step.
- Do not add a model recommendation block.
- Do not claim deployment, resolver visibility, install status, validation success, readiness, or acceptance unless observed and bound.
- Do not import Orca project-specific paths, policies, or product facts into the reusable agent-workflow source except as a clearly labeled motivating example.

## Expected Output

Return findings first, then the patch/proposal.

Use this shape:

```text
SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE:
- canonical source resolved:
- sources read:
- sources unavailable:

Findings:
- [severity] <finding> — <file:line evidence> — minimum closure condition:

Settlement:
- gate owner:
- chosen rule:
- rejected alternatives:
- compatibility with routine fused lanes:

Patch:
- applied | proposed_only | blocked:
- touched files:
- diff summary:

Validation:
- command or check:
- observed result or not-run reason:
- regression case this now catches:

Residuals:
- accepted residual risks:
- owner decisions needed:

Closeout Boundary:
- no validation/readiness/deployment/resolver claim unless observed:
```

If you patch, keep the diff smallest-complete and run the relevant local validation or explain why it could not run. If you cannot patch because the editable source is unbound, return a precise patch proposal with target file, target section, and exact replacement text or diff hunk.

## Non-Goals

- No IG capture design changes.
- No Orca data-lake changes.
- No broad workflow-kernel rewrite.
- No skill install/deploy/promotion.
- No commit/push/PR unless separately authorized by the receiving lane and its lifecycle rules.

## Dispatcher Notes

This prompt is intentionally strict on source loading because the failure mode is process drift: a workflow skill can look correct while routing review too late. The receiving lane should push back on the hypothesis if the source says the real defect is elsewhere, for example a closeout/adjudication failure rather than a fused checkpoint failure.
