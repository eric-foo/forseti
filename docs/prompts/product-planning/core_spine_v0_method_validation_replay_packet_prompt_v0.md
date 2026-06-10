# Core Spine v0 Method Validation Replay Packet Prompt

- Status: DRAFT_PROMPT
- Prompt family: Product planning / method validation replay
- Output mode: file-write
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Edit permission: docs-write for the target replay artifacts only
- Target packet artifact: `docs/product/core_spine_v0_method_validation_replay_packet_v0.md`
- Target per-case artifacts:
  - `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md`
  - `docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md`
  - `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`
  - `docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md`
  - `docs/product/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md`
- Public web/source research: authorized only when this prompt is explicitly launched for replay; if a launch turn forbids browsing or source research, stop as blocked
- Implementation authorized: no
- Feature planning authorized: no
- Source maps, source systems, data spine, automation, dashboards, scoring engines, generated artifacts outside the target docs, staging, commits, pushes, and PRs authorized: no

## Prompt

Use `workflow-deep-thinking`.

You are running Orca's five-case Core Spine v0 method-validation replay. This is
not a case-study writing task, source-map task, data-spine task, feature plan,
implementation plan, or marketing task.

The real question is:

> Can Orca repeatedly improve high-stakes competitive or category-response
> decisions before the outcome is obvious, and does cleaned second-order public
> evidence change or sharpen the valid action ceiling?

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
- `docs/product/core_spine_v0_method_validation_case_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v1.md`

Also check:

- `git status --short --branch`
- `git log --oneline -6`

## Accepted Frame Basis

Use exactly the accepted case-frame lock artifact:

`docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`

The accepted cases are:

1. `MV-01` - Intercom Fin pressure on Zendesk.
2. `MV-03` - Stack Overflow response to ChatGPT.
3. `MV-04` - Unity Runtime Fee.
4. `MV-05` - Reddit API and data pricing.
5. `MV-09` - Thomson Reuters / Casetext legal AI response.

Do not add, remove, or replace cases during replay. If a case becomes blocked,
mark it blocked and preserve the role it would need a later replacement to
maintain.

## Research Boundary

Use only public, non-deceptive, market-level sources.

Allowed research:

- public company, product, pricing, help, policy, filing, announcement, and
  investor sources;
- public competitor, vendor, and official product sources;
- public buyer, operator, practitioner, developer, legal, community, moderator,
  consultant, analyst, review, and discussion sources;
- public archived pages where needed to establish cutoff visibility;
- public post-window outcome sources only after the at-cutoff replay memo for
  that case is sealed.

Disallowed research:

- private data;
- account-gated scraping;
- deceptive access;
- ordinary-person dossiers;
- outreach;
- source maps or source inventories beyond Evidence Units and source ledgers
  needed for the replay;
- broad source farming not tied to a case frame;
- feature, implementation, data-spine, dashboard, scraper, API, scoring, or
  automation planning.

## Replay Order

Run each case through this sequence. Do not skip ahead.

```text
Verification Gate
-> First-Order At-Cutoff Pass
-> Second-Order At-Cutoff Pass
-> Action-Ceiling Movement
-> At-Cutoff Decision Memo
-> Post-Window Outcome Comparison
-> Calibration Label And Method Lesson
```

Do not inspect post-window outcome evidence for a case until that case's
at-cutoff memo is written and sealed in the case artifact.

## Phase 1: Verification Gate

Before interpreting evidence for any case, verify:

- exact cutoff date or cutoff window;
- fair-cutoff rationale;
- whether first-order source families were publicly visible before cutoff;
- whether second-order source families were publicly visible before cutoff;
- what post-window sources must be excluded from at-cutoff reasoning;
- whether archived versions are needed for changed live pages.

If source visibility cannot be established, mark the source or case
`BLOCKED_SOURCE_VISIBILITY`. Do not use unverifiable material as pre-cutoff
evidence.

If a case cannot be replayed without private data, mark it blocked. Do not
repair the case by changing the decision frame.

## Phase 2: First-Order At-Cutoff Pass

Use only first-order official or near-official sources visible before cutoff.

For each case, record:

- included first-order Evidence Units;
- excluded first-order sources and why;
- Signal Integrity effects;
- Signal Use Classification;
- first-order Decision Strength;
- first-order Action Ceiling.

Do not infer buyer demand from company claims, vendor claims, benchmarks,
comparison pages, launch material, or customer stories by default.

## Phase 3: Second-Order At-Cutoff Pass

Add only second-order public sources visible before cutoff and inside the
accepted source-family boundary for the case.

For each case, record:

- included second-order Evidence Units;
- excluded second-order sources and why;
- Signal Integrity effects;
- Signal Use Classification;
- second-order Decision Strength;
- second-order Action Ceiling;
- whether second-order evidence causes `No change`, `Upgrade`, `Downgrade`,
  `Reframe`, or `Blocked`.

Second-order evidence is not automatically stronger than first-order evidence.
It must survive audience-fit, timing, independence, integrity, costly-behavior,
counterevidence, and alternative-explanation checks.

## Phase 4: At-Cutoff Memo

For each unblocked case, write an at-cutoff memo before opening post-window
outcome evidence.

The memo must include:

- decision frame;
- evidence basis;
- Signal Integrity summary;
- Signal Use Classification summary;
- first-order versus second-order movement;
- Decision Strength;
- Action Ceiling;
- recommendation using only allowed case verbs;
- counterevidence;
- alternative explanations;
- uncertainty;
- kill criteria;
- update triggers;
- boundary note.

The recommendation verb must not exceed the Action Ceiling. `Move` and
`Commit` require reliable-bet evidence; they cannot come from hype, engagement,
vendor narrative, benchmark claims, or social proof alone.

## Phase 5: Post-Window Outcome Comparison

Only after the at-cutoff memo is sealed for a case, inspect post-window outcome
evidence for that case.

Compare:

- what Orca would have recommended at cutoff;
- what later happened;
- whether the recommendation was useful, wrong, early, late, overconfident,
  underconfident, inconclusive, or blocked;
- what the evidence standard should learn.

Do not retroactively raise the at-cutoff Action Ceiling because the later
outcome looks similar.

## Case-Specific Role Checks

For `MV-01`, test competitor narrative pressure without importing the prior
SH-01 result as the answer.

For `MV-03`, test whether developer workflow, community, traffic, enterprise
knowledge, or data-value signals change the action ceiling beyond official
policy and product claims.

For `MV-04`, test whether pre-announcement ecosystem evidence should have
capped a broad pricing `Commit` before the Runtime Fee outcome was visible.

For `MV-05`, test whether API/data monetization should have been segmented,
narrowed, held, or committed based on pre-cutoff platform ecosystem evidence.

For `MV-09`, test positive-action judgment: whether public legal-tech,
practitioner, law-firm, workflow, buyer-risk, and incumbent-strategy evidence
could justify a reliable `Test`, bounded `Move`, partner, license, build, or
acquire path before the later outcome was obvious.

## Output Artifacts

Write one per-case artifact for each case, using the target paths listed in the
metadata.

Each per-case artifact must contain:

1. Status, scope, source basis, and non-authority.
2. Repository state checked.
3. Accepted decision frame.
4. Verification gate result.
5. First-order Evidence Units and pass result.
6. Second-order Evidence Units and pass result.
7. Action-ceiling movement.
8. At-cutoff decision memo.
9. Post-window outcome comparison.
10. Calibration label and method lesson.
11. Blockers, residual risks, and not-proven boundaries.
12. Explicit non-claims.
13. Current verdict.

Then write the packet artifact:

`docs/product/core_spine_v0_method_validation_replay_packet_v0.md`

The packet must contain:

1. Status, scope, source basis, and non-authority.
2. Repository state checked.
3. Case status matrix.
4. Cross-case first-order versus second-order movement.
5. Positive-action result.
6. Reverse-case result.
7. False-`Move` or false-`Commit` avoidance result.
8. Cases where Orca was useful, wrong, early, late, overconfident,
   underconfident, inconclusive, or blocked.
9. Strong method signals against the rubric.
10. Weak method signals against the rubric.
11. Evidence-standard lessons.
12. What remains unproven for buyer validation.
13. Explicit non-claims.
14. Current verdict.

## Stop Conditions

Stop and report drift if the work starts to:

- change the five locked cases;
- change accepted cutoff frames instead of marking blockers;
- use post-window evidence in at-cutoff reasoning;
- treat vendor, campaign, benchmark, social, or comparison evidence as demand
  by default;
- treat second-order evidence as inherently true;
- turn replay into case-study prose;
- write marketing copy;
- claim external willingness to pay, product-market fit, feature readiness,
  implementation readiness, or data-spine readiness;
- create source maps, source inventories, dashboards, scrapers, APIs, scoring
  systems, automations, or implementation plans;
- import `jb` authority.

## Final Response

After writing the artifacts, return:

- changed file paths;
- case status matrix;
- which cases were blocked, useful, wrong, early, late, overconfident,
  underconfident, or inconclusive;
- whether second-order evidence caused `No change`, `Upgrade`, `Downgrade`,
  or `Reframe` in each case;
- whether positive-action and reverse-case tests produced usable method signal;
- what remains unauthorized.
