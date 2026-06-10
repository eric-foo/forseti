# Core Spine v0 Method Validation Case-Frame Locks Prompt

- Status: DRAFT_PROMPT
- Prompt family: Product planning
- Output mode: file-write
- Target artifact: `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Edit permission: docs-write for the target artifact only
- Implementation authorized: no
- Feature planning authorized: no
- Evidence replay authorized: no
- Source maps, source systems, data spine, automation, dashboards, scoring engines, generated artifacts, staging, commits, pushes, and PRs authorized: no

## Prompt

Use `workflow-deep-thinking`.

You are preparing case-frame locks for Orca's five-case Core Spine v0
method-validation pass. You are not running evidence replay, producing case
studies, building source maps, planning features, or designing implementation.

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

Also check:

- `git status --short --branch`
- `git log --oneline -6`

## Locked Cases

Use exactly these five case identities:

1. `MV-01` - Intercom Fin pressure on Zendesk.
2. `MV-03` - Stack Overflow response to ChatGPT.
3. `MV-04` - Unity Runtime Fee.
4. `MV-05` - Reddit API and data pricing.
5. `MV-09` - Thomson Reuters / Casetext legal AI response.

Do not replace, add, or remove cases unless a case is blocked. If a case is
blocked, state the blocker and the validation role that any replacement would
need to preserve.

## Research Boundary

Use only public, non-deceptive, market-level sources.

This prompt may use shallow web/source research only to verify:

- plausible cutoff date or cutoff window;
- fair-cutoff rationale;
- whether first-order and second-order public source families appear likely to
  exist;
- broad post-window outcome window for later calibration.

Do not collect full evidence pools. Do not interpret evidence units. Do not
produce at-cutoff recommendations. Do not inspect sources for the purpose of
making the case persuasive.

If web/source research is unavailable or not authorized in the launch turn,
draft the case-frame locks from repo-visible information and clearly mark
cutoff, source-family, and outcome-window fields as `NEEDS_VERIFICATION`.

## Case-Frame Fields

For each case, lock or mark blocked:

- case ID and name;
- validation role;
- decision question;
- decision owner or context;
- cutoff date or cutoff window;
- fair-cutoff rationale;
- why the later outcome was not obvious at cutoff;
- allowed action verbs;
- first-order source-family boundary;
- second-order source-family boundary;
- post-window exclusion rule;
- expected outcome-comparison window;
- reliable-bet, costly-behavior, or action-threshold standard for the case;
- upgrade conditions;
- downgrade conditions;
- reframe conditions;
- blocked conditions;
- result labels that matter for the case.

## Safe Detail Rule

Include only controlled case-frame detail. Avoid case-study prose.

Safe:

- decision frame;
- cutoff logic;
- source-family boundaries;
- allowed action verbs;
- exclusion rules;
- result semantics.

Unsafe before replay:

- rich narrative arcs;
- likely Orca recommendation;
- detailed source inventories;
- post-window causal explanations;
- marketing lessons;
- product or feature implications;
- claims that the later outcome was obvious.

## Output Artifact Shape

Write `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
with these sections:

1. Status, scope, source basis, and non-authority.
2. Repository state checked.
3. Frame-locking rules.
4. Portfolio-level balance check.
5. `MV-01` case frame.
6. `MV-03` case frame.
7. `MV-04` case frame.
8. `MV-05` case frame.
9. `MV-09` case frame.
10. Blockers and verification needs.
11. Explicit non-claims.
12. Current verdict.

Use the verdict:

`CASE_FRAMES_LOCKED_AWAITING_EVIDENCE_REPLAY_AUTHORIZATION`

only if every case has a usable cutoff or clearly marked verification need,
decision frame, source-family boundary, and post-window exclusion rule.

Use:

`BLOCKED_CASE_FRAME_LOCKS`

if one or more cases cannot be framed without full evidence replay, private
data, or unresolved owner input.

## Stop Conditions

Stop and report drift if the work starts to:

- produce evidence units;
- run at-cutoff recommendations;
- inspect post-window evidence to infer pre-cutoff recommendations;
- write case studies;
- create source maps or inventories;
- design a data spine, dashboard, scraper, API, scoring system, or automation;
- plan features or implementation;
- claim external willingness to pay;
- import `jb` authority.

## Final Response

After writing the artifact, return:

- changed file path;
- whether each case frame is locked, marked `NEEDS_VERIFICATION`, or blocked;
- any blockers;
- what remains unauthorized.
