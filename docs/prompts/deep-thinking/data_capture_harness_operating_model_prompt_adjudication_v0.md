# Data Capture Harness Operating Model Prompt Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Model-neutral adjudication prompt for comparing the next prompt-routing choice before launching Data Capture Harness operating-model architecture work.
use_when:
  - Asking Opus, ChatGPT, or another reasoning model to adjudicate the prompt-routing choice before launching the architecture lane.
  - Rating whether Orca should launch the current architecture prompt directly or run the adversarial prompt-review lane first.
  - Comparing launch-environment risk around the required three architecture-planning subagents.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/data_capture_harness_operating_model_architecture_prompt_v0.md
  - docs/prompts/reviews/data_capture_harness_operating_model_architecture_prompt_adversarial_review_prompt_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
stale_if:
  - Either compared prompt is materially revised or superseded.
  - The owner changes the requirement to use exactly three architecture-planning subagents.
  - The Data Capture obligation baseline or direction-signal decision is superseded.
```

- Prompt target: Opus, ChatGPT, or another reasoning model.
- Output mode: `paste-ready-chat`.
- Prompt artifact path: `docs/prompts/deep-thinking/data_capture_harness_operating_model_prompt_adjudication_v0.md`.
- Created: 2026-05-28.
- Implementation authorized: no.
- Architecture execution authorized: no.
- Review execution authorized: no.
- Runtime/source-system design authorized: no.
- ECR/Cleaning/Judgment design authorized: no.
- Source-of-truth promotion claimed: no.

## Paste-Ready Prompt

```text
You are adjudicating a prompt-routing decision for Orca. Do not perform the
Data Capture Harness architecture work. Do not perform an adversarial artifact
review. Your task is to judge which prompt-routing proposal is stronger before
the owner launches the next lane.

Context:
Orca accepted the Data Capture obligation baseline and demoted the current
manual harness plus BT2-04 dry run to `Data Capture Harness Direction Signal
v0`. The next intended lane is a bounded Data Capture Harness operating-model
architecture lane. It must preserve commissioned-capture scope, obligation
discharge, failure visibility, raw observable/source-language preservation,
layer discipline, and the boundary against runtime/source-system design, ECR,
Cleaning, Judgment, implementation, validation, readiness, or buyer-proof
claims.

Current owner requirement:
Because this is an architecture prompt, it must explicitly use the standard
architecture-planning three advisory perspectives/subagents:
- directional;
- adversarial;
- grounding.

Decision to adjudicate:
Should Orca launch the current architecture prompt directly, or first run the
adversarial prompt-review prompt / split the launch path because the
three-subagent requirement is launch-environment-sensitive?

Compared prompt artifacts:

Proposal A: Launch the current architecture prompt directly.
- Path: `docs/prompts/product-planning/data_capture_harness_operating_model_architecture_prompt_v0.md`
- SHA256: `2994C6715E4448FA43431D1CC30D4B304DEDA85DF9CA5CFEE460BCD96A770B2F`
- Shape: source-grounded operating-model architecture prompt.
- It requires `workflow-architecture-planning` in standard profile.
- It explicitly requires exactly three advisory architecture subagents:
  directional, adversarial, and grounding.
- It requires each subagent to receive the same source pack or the defined
  bounded source capsule and declare `SOURCE_CONTEXT_READY` /
  `SOURCE_CONTEXT_INCOMPLETE`.
- It defines two evidence modes: `delegated_three_subagents` and
  `plain_model_local_fallback`.
- It says if subagent tooling is unavailable, rejected, or blocked, return
  `BLOCKED_SUBAGENT_UNAVAILABLE` unless the current launch instruction
  explicitly says `plain_model_fallback: authorized`.
- If fallback is authorized, it must state `Subagents launched: none`,
  use local directional/adversarial/grounding passes, and mark delegated
  subagent independence as `not proven`.
- It tiers source loading into a core read pack plus conditional expansion.
- Strength: preserves the owner requirement and prevents fake
  three-subagent evidence.
- Risk: if pasted into plain Opus or ChatGPT without the explicit
  `plain_model_fallback: authorized` launch phrase, it will still block rather
  than produce architecture planning.

Proposal B: Run the adversarial prompt-review prompt before launching the
architecture lane.
- Path: `docs/prompts/reviews/data_capture_harness_operating_model_architecture_prompt_adversarial_review_prompt_v0.md`
- SHA256: `36B2D91E841FBC08FDAD6ED55B7B1A114A976ED8299CBFD9ECBE5BF18E5CBB99`
- Shape: read-only adversarial review prompt focused on the architecture
  prompt's launch efficacy.
- It asks whether the architecture prompt maximizes output quality or causes
  template-filling, overbroad source loading, premature target selection, or
  launch-environment blocking.
- It specifically tests whether the prompt should split into an agent-enabled
  architecture prompt and a plain-model wrapper with local perspectives.
- Strength: reduces launch risk before spending the architecture lane.
- Risk: may add another review step even if the architecture prompt is already
  good enough, delaying the operating-model architecture artifact.

Your task:
1. Rate Proposal A and Proposal B independently.
2. Decide which route should be used next.
3. If both are weak, propose a better third route, but still rate A and B.
4. Be explicit about whether your recommendation changes depending on whether
   the launch environment can actually spawn three delegated subagents.

Assume two launch environments may exist:
- Environment 1: Agent-enabled. The launcher can spawn exactly three advisory
  subagents with source packs/capsules.
- Environment 2: Plain model. The launcher cannot spawn subagents and can only
  run local reasoning in one model context.

Scoring rubric:
Rate each proposal from 1 to 10 on each criterion:
- source-grounding strength;
- compliance with the owner's three-subagent requirement;
- launch-environment robustness;
- risk of fake confidence or fake evidence;
- risk of context bloat / overloading the model;
- boundary discipline against runtime, ECR, Cleaning, Judgment, and
  implementation drift;
- speed to useful architecture output;
- probability of producing the best next artifact for Orca.

Then provide:
- overall score for Proposal A, 1 to 10;
- overall score for Proposal B, 1 to 10;
- winner for Environment 1;
- winner for Environment 2;
- recommended next action;
- minimum patch, if any, before launch;
- one strongest argument against your own recommendation.

Output format:

## Summary
One paragraph with your recommendation.

## Ratings
Markdown table:
`Criterion | Proposal A score | Proposal B score | Notes`

## Environment Split
- Agent-enabled environment:
- Plain-model environment:

## Recommendation
Use exactly one:
- `LAUNCH_A_NOW`
- `RUN_B_REVIEW_FIRST`
- `SPLIT_PROMPTS_BEFORE_LAUNCH`
- `PATCH_A_THEN_LAUNCH`
- `PATCH_B_THEN_REVIEW`
- `BLOCKED_INSUFFICIENT_CONTEXT`

## If Split Is Best
If you choose `SPLIT_PROMPTS_BEFORE_LAUNCH`, define the smallest split:
- agent-enabled architecture prompt:
- plain-model fallback or wrapper:
- what must remain shared:
- what must differ:

## Minimum Patch
Name only the smallest patch needed, if any. Do not provide a full rewritten
prompt unless necessary.

## Self-Critique
Give the strongest argument against your recommendation.

Rules:
- Do not claim validation, approval, readiness, source-of-truth promotion, or
  architecture correctness.
- Do not perform the architecture plan.
- Do not perform the adversarial review.
- Do not design runtime tooling, source systems, ECR, Cleaning, Judgment,
  implementation, tests, packages, deployment, commits, or PRs.
- If you cannot inspect the files directly, state that your answer is based on
  the source capsule above and mark confidence accordingly.
```
