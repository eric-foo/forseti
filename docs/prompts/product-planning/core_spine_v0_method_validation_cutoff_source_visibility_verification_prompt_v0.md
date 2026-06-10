# Core Spine v0 Method Validation Cutoff Source-Visibility Verification Prompt

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Prompt for verifying method-validation case cutoff timing and broad public source-family visibility before any replay prompt is prepared.
use_when:
  - Verifying the five locked Core Spine v0 method-validation cases before replay prompting.
  - Checking whether cutoff or source-family visibility issues require patching before replay.
  - Preserving the boundary between verification and evidence replay.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine_v0_method_validation_case_locks_v0.md
  - docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md
  - docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md
input_hashes:
  docs/product/core_spine_v0_method_validation_case_locks_v0.md: 5782C9E809269A783B73E29E733CFFF9D9C4BC9E0F95F2C365886CCD387FC4E5
  docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md: F5633E834BE599C1C5ACFDBB9A65DC281F7AF72F18CC19E48A51FE57C4EFC1F0
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: 4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785
  docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md: 749DDCB3FFCBBA81A0F2253A3F1BD76948793B451DA528B67B998BDAF982195A
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - docs/review-outputs/method-validation/core_spine_v0_method_validation_cutoff_source_visibility_verification_report_v0.md
stale_if: Any locked case identity changes, the case-frame locks artifact changes, replay is authorized before this verification runs, or the future verifier sees a materially different frame-lock verdict.
```

## Prompt

Use this prompt in workspace `C:\Users\vmon7\Desktop\projects\orca`.

## Objective

Verify only the cutoff date or cutoff window and broad first-order and
second-order public source-family visibility for the five locked Core Spine v0
method-validation cases:

- `MV-01` - Intercom Fin pressure on Zendesk.
- `MV-03` - Stack Overflow response to ChatGPT.
- `MV-04` - Unity Runtime Fee.
- `MV-05` - Reddit API and data pricing.
- `MV-09` - Thomson Reuters / Casetext legal AI response.

This is a pre-replay verification pass. It may determine whether a future
replay prompt can be prepared, but it does not authorize replay.

## Current State To Preserve

- Five method-validation case identities are locked.
- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md` has
  been patched after adversarial review.
- The owner stated in the prompt-authoring turn that post-patch confirmation is
  all good with no follow-up issues.
- Evidence replay remains unauthorized.
- The next compounding move is cutoff and source-family visibility
  verification only.

Do not reopen case selection, frame-lock acceptance, product planning, feature
planning, implementation planning, or replay authorization unless a required
source is missing or contradictory.

## Required Reads

Read these local sources before verification:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/project-authority.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/communication-style.md`
- `docs/product/core_spine_v0_method_validation_case_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`

Also run and record:

- `git status --short --branch`
- `git log --oneline -6`

Authoring-time repository reference:

- Branch: `main`
- HEAD: `3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c`
- Dirty-state allowance: modified and untracked docs are allowed, including
  the method-validation product artifacts and prompt/review folders. Do not
  require a clean worktree. Do block if a required source file is missing or if
  a required source contradicts the locked case identities or replay boundary.

## Authorized Scope

You may only:

- verify each case cutoff date or cutoff window;
- verify broad first-order public source-family visibility before the cutoff;
- verify broad second-order public source-family visibility before the cutoff;
- mark each case as `VERIFIED_FOR_REPLAY`, `NEEDS_CUTOFF_PATCH`, or `BLOCKED`;
- report what remains unauthorized.

Use narrow public-source timing checks only as needed to establish cutoff and
source-family visibility. Keep findings at the source-family level. You may
name minimal representative public source families or examples when necessary
to justify visibility, but do not create source maps, source inventories,
evidence units, or detailed source collections.

## Forbidden Scope

Do not:

- run evidence replay;
- create evidence units;
- produce at-cutoff recommendations;
- recommend whether any company should watch, probe, test, hold, build, buy,
  partner, move, commit, narrow, phase, or reposition;
- create source maps or source inventories;
- collect detailed source pools;
- write case-study prose;
- draft marketing lessons or outcome narratives;
- perform product planning, feature planning, implementation planning, or
  implementation;
- create software, tests, packages, tooling, automation runtimes, dashboards,
  scrapers, APIs, databases, data spines, source systems, generated artifacts,
  or scoring engines;
- patch source artifacts directly;
- produce an executable patch queue;
- stage, commit, push, or create a pull request.

## Verification Rules

For each case, verify cutoff timing before source-family visibility.

Cutoff status must answer:

- Is the cutoff date or window before the public outcome, announcement, or
  response material that the frame excludes from at-cutoff reasoning?
- Is the cutoff early enough to avoid hindsight contamination?
- Is the cutoff late enough that the relevant first-order and second-order
  public source families could plausibly be visible?
- If the current cutoff is provisional, can it be pinned, narrowed, or left as
  a window without breaking the case role?

Source-family visibility status must answer:

- Were broad first-order source families publicly visible before the verified
  cutoff?
- Were broad second-order source families publicly visible before the verified
  cutoff?
- Are any source families only post-cutoff, private, speculative, or too thin
  to support a later replay prompt?
- Does source-family visibility remain broad enough for the case role without
  turning this verification into evidence replay?

Use `NEEDS_CUTOFF_PATCH` when the case can likely remain in the portfolio but
the cutoff date, cutoff window, outcome-comparison window, or related
source-family timing language needs a docs patch before replay prompting.

Use `BLOCKED` when cutoff timing or source-family visibility cannot support
the case role without hindsight contamination, private evidence, or a role
change. A blocked case must trigger the role-preserving replacement
requirement from the case identity lock and frame-lock contract.

Use `VERIFIED_FOR_REPLAY` only when cutoff and broad source-family visibility
are good enough to prepare a later replay prompt. This label does not
authorize evidence replay.

## Output Mode And Write Boundary

Output mode: `file-write`.

Write exactly one docs-only verification report:

`docs/review-outputs/method-validation/core_spine_v0_method_validation_cutoff_source_visibility_verification_report_v0.md`

Do not write or edit any other file. If that report path is unavailable or
write permission is blocked, stop and return a chat-only blocked report in the
same section shape.

## Required Report Contract

The verification report must include these sections:

1. Repository state checked.
   - Include the actual `git status --short --branch` and
     `git log --oneline -6` output observed by the verifier.
   - State whether required sources were present and whether dirty docs were
     treated as allowed current workspace evidence.

2. Case-by-case cutoff status.
   - For each case, record the cutoff date or window checked, the cutoff
     status, and the rationale at timing level only.
   - Do not include at-cutoff recommendations.

3. Case-by-case source-family visibility status.
   - For each case, separately record first-order and second-order public
     source-family visibility.
   - Keep this at broad source-family level, not evidence-unit level.

4. Any cutoff patches needed.
   - List affected case, affected field, why a patch is needed, and the
     minimum owner decision or docs change required.
   - Do not apply patches and do not produce an executable patch queue.

5. Any blocked cases and role-preserving replacement requirement.
   - If a case is blocked, name the blocked validation role and state that any
     replacement must preserve that role.
   - Do not propose replacement case identities unless separately authorized.

6. Explicit non-claims.
   - State that evidence replay was not run and remains unauthorized.
   - State that no evidence units, source maps, source inventories, data spine,
     feature plan, implementation plan, software, tooling, commit, push, or PR
     were created.
   - State that no at-cutoff recommendation is made for any case.

7. Current verdict.
   - Use exactly one of these verdicts:
     - `CUTOFFS_AND_SOURCE_VISIBILITY_VERIFIED_FOR_REPLAY_PROMPTING`
     - `NEEDS_CUTOFF_PATCH_BEFORE_REPLAY`
     - `BLOCKED_CUTOFF_SOURCE_VISIBILITY`

## Verdict Rules

Use `CUTOFFS_AND_SOURCE_VISIBILITY_VERIFIED_FOR_REPLAY_PROMPTING` only if all
five cases are marked `VERIFIED_FOR_REPLAY`.

Use `NEEDS_CUTOFF_PATCH_BEFORE_REPLAY` if at least one case is
`NEEDS_CUTOFF_PATCH` and no case is `BLOCKED`.

Use `BLOCKED_CUTOFF_SOURCE_VISIBILITY` if any case is `BLOCKED`.

The verdict is only a verification verdict for preparing a later replay prompt.
It does not authorize evidence replay.

## Final Chat Response After The Future Run

After writing the report, return only:

- changed report path;
- report SHA256 hash;
- current verdict;
- whether any blocker prevented completion;
- confirmation that evidence replay remains unauthorized.
