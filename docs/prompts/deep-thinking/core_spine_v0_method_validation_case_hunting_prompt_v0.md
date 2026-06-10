# Core Spine v0 Method Validation Case-Hunting Prompt

- Status: DRAFT_PROMPT
- Prompt family: Deep reasoning
- Output mode: chat-only
- Intended use: Case hunting only; do not execute evidence replay
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Edit permission: read-only
- Implementation authorized: no
- Feature planning authorized: no
- Evidence collection authorized by this prompt: only if the launch turn explicitly authorizes web/source research; otherwise use repo-visible sources and clearly mark uncertainty

## Prompt

Use `workflow-deep-thinking`.

You are helping Orca select historical cases for a five-case method validation
run. You are not running the validation, collecting full evidence, producing
decision memos, planning features, designing a data spine, or proposing
implementation.

## Required Reads

Read:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/project-authority.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/communication-style.md`

Then read:

- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine_v0_proof_protocol_v0.md`
- `docs/product/core_spine_v0_first_proof_run_packet_v0.md`
- `docs/product/core_spine_v0_method_validation_rubric_v0.md`

Also check:

- `git status --short --branch`
- `git log --oneline -6`

## Real Problem

Frame the task this way:

> Which historical cases are best suited to test whether Orca can improve
> AI-era competitive or category-response decisions before the outcome is obvious,
> especially when the evidence environment is polluted and second-order public
> data may change the correct action ceiling?

Do not select cases because the later outcome is famous. Select cases because
they stress Orca's judgment layer.

Only consider AI-era cases. For this prompt, treat AI era operationally as cases
whose decision cutoff is on or after the public generative-AI market inflection
on `2022-11-30`, unless a later accepted Orca source defines a different
boundary.

## Search / Source Boundary

If the launch instruction explicitly authorizes web or source research, use
public sources only and keep the search shallow enough for case hunting. Do not
perform full evidence collection.

If web/source research is not explicitly authorized, do not browse. Work from
repo-visible sources, general memory, and clearly marked assumptions. Mark
candidate timing, cutoff, and source availability as `needs verification`.

Do not use private, deceptive, intrusive, person-level, login-only, or
non-public evidence.

## Case-Hunting Criteria

Find 10 to 15 candidate cases, then recommend a five-case portfolio.

Strong candidates should have:

- a real competitive, category, technology, pricing, packaging, or platform-response decision;
- an AI-era decision cutoff under the boundary above;
- public evidence before a plausible cutoff date;
- a later outcome that can be used for calibration;
- polluted public evidence such as vendor claims, campaign language, benchmarks, review-platform bias, bots, social proof, or noisy community evidence;
- plausible second-order evidence from users, operators, buyers, partners, consultants, reviews, procurement-adjacent discussion, workflows, jobs, or implementation friction;
- multiple plausible actions at cutoff, such as `Watch`, `Probe`, `Test`, `Hold`, `Move`, or `Commit`;
- a real chance that Orca could be useful, wrong, early, late, overconfident, or underconfident.

The five-case portfolio must include:

- at least one SH-01-like competitor narrative pressure case;
- at least one AI or technology-disruption case;
- at least one pricing, packaging, or business-model disruption case;
- at least one reverse case where a company made a visible move that later performed badly, and Orca should be tested on whether it would have advised `Hold`, `Probe`, `Test`, or a narrower move;
- at least one case where second-order public evidence is likely to matter more than official first-order claims.

Avoid five cases from the same category.

## Candidate Evaluation

For each candidate, classify:

- candidate case ID;
- company or category;
- decision question;
- likely decision owner;
- plausible cutoff window;
- later outcome window;
- why the outcome was not obvious at cutoff;
- first-order evidence likely available before cutoff;
- second-order evidence likely available before cutoff;
- evidence pollution type;
- likely action-ceiling tension;
- whether the case is a reverse-case candidate;
- why this case would test Orca rather than generic hindsight;
- exclusion or blocker risk.

Use the source-use ladder from
`docs/product/core_spine_v0_method_validation_rubric_v0.md`.

## Output Shape

Return concise sections:

**Problem Frame**

State what case hunting is trying to optimize for.

**Candidate Pool**

Provide a table of 10 to 15 candidate cases.

**Recommended Five-Case Portfolio**

Pick exactly five. Explain why this set is balanced and what each case tests.

**Reverse-Case Candidate**

Name the strongest reverse case and why it matters commercially.

**Second-Order Data Test**

Explain which cases are most likely to show whether second-order evidence
upgrades, downgrades, reframes, or does not change the action ceiling.

**Blocked Or Risky Candidates**

Name candidates that look tempting but should be downgraded because they are
too famous, too outcome-obvious, too source-poor, too private-data-dependent,
or too similar to existing cases.

**Recommended Locks Before Validation**

List the exact decisions that must be locked before any evidence replay:

- final case list;
- cutoff date for each case;
- fair-cutoff rationale;
- decision question for each case;
- first-order and second-order source families;
- post-window exclusion rule;
- result labels and pass/fail criteria.

**Non-Claims**

State that this case-hunting output does not prove Orca works, does not prove
external willingness to pay, does not authorize source systems, and does not
authorize feature planning or implementation.

## Stop Conditions

Stop and call out drift if the work starts to:

- run full evidence collection;
- interpret a case as if selected;
- use post-window outcomes to justify pre-cutoff recommendations;
- design a data spine, source map, scraper, dashboard, scoring system, API, or automation;
- plan features or implementation;
- import `jb` authority;
- claim external buyer willingness to pay.
