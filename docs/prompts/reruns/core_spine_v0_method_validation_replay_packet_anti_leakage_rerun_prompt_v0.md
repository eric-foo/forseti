# Core Spine v0 Method Validation Replay Packet Anti-Leakage Rerun Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Rerun or patch prompt
scope: Anti-leakage rerun wrapper for the Core Spine v0 method-validation replay packet prompt after a contaminated launch.
use_when:
  - Relaunching the method-validation replay after post-window evidence was opened too early.
  - Preserving accepted case-frame locks while tightening replay sequencing.
  - Preventing outcome-source leakage before at-cutoff memos are sealed.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md
  - docs/product/foundation/core_spine_v0_method_validation_case_frame_locks_v0.md
input_hashes:
  docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md: 0506819eebeb952ac8b40e2af84a65873efa88e52c5a08cceb6a7fa432270469
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: 4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785
branch_or_commit: main at 3bf5c45, dirty workspace allowed
stale_if: The base replay prompt or accepted case-frame lock artifact changes materially.
```

- Status: DRAFT_RERUN_PROMPT
- Prompt family: Rerun / method validation replay
- Output mode: file-write, inherited from the base replay prompt
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Base prompt:
  `docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md`
- Fresh-run note: for a new uncontaminated launch, use
  `docs/prompts/wrappers/core_spine_v0_method_validation_fresh_replay_source_loading_wrapper_v0.md`
  before this contaminated-launch rerun prompt.
- Prior failed run: contaminated launch reported by the Chief Architect; any
  existing replay artifacts in the workspace are output-collision candidates,
  not admissible replay evidence
- Failure being retried: post-window outcome material was inspected before
  at-cutoff case memos were sealed
- Edit permission: docs-write for the replay artifacts named in the base prompt
  only
- Public web/source research: authorized only inside the anti-leakage sequence
  below
- Implementation authorized: no
- Feature planning authorized: no
- Source maps, source systems, data spine, automation, dashboards, scoring
  engines, generated artifacts outside the target docs, staging, commits,
  pushes, and PRs authorized: no

## Launch Prompt

Use `workflow-deep-thinking`.

You are relaunching the Core Spine v0 method-validation replay after a prior
attempt stopped correctly because post-window outcome sources were opened
before at-cutoff memos were sealed.

Do not continue the prior contaminated thread. Start from this prompt, the base
prompt, and the accepted repo artifacts only. Do not use notes, URLs, snippets,
source titles, or observations from the failed launch as evidence.

## Required Reads

Read this rerun prompt first.

Then read:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/project-authority.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/prompt-orchestration.md`

Then read the base replay prompt:

- `docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md`

Then read the accepted frame source:

- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`

Read the base prompt's other required product sources as needed to execute the
base prompt. Treat review reports as process sources only; do not use review
prose as case evidence or as a substitute for pre-cutoff source verification.

Also check:

- `git status --short --branch`
- `git log --oneline -6`

## Frozen Decisions

Do not change:

- the five accepted cases;
- accepted decision frames;
- accepted cutoff windows, except to mark verification failure or record a more
  exact date inside the accepted window;
- target replay artifact paths from the base prompt;
- output artifact shape from the base prompt;
- non-authority boundaries.

## Mutable Fields

Only these fields may change from the base prompt:

- launch sequencing;
- anti-leakage browsing discipline;
- per-case isolation mechanics;
- blocked-state handling when contamination or source visibility failure occurs.

Do not reopen case selection, case-frame locks, product thesis, method rubric,
or output destination.

## Anti-Leakage Rule

The model may already have general world knowledge about famous outcomes. That
knowledge is not admissible evidence.

For each case, admissible at-cutoff reasoning may use only:

- the accepted decision frame;
- source-family boundaries from the accepted frame;
- public sources verified as visible before the case cutoff;
- archived versions or timestamped sources when live pages changed;
- Signal Integrity and Signal Use Classification applied to those pre-cutoff
  sources.

Post-window facts, outcome pages, later retrospectives, later announcements,
later product pages, later controversy reporting, and later integrations are
sealed until the at-cutoff memo for that same case is written.

## Case Isolation Sequence

Run one case at a time. For each case, complete the full sealed sequence before
starting the next case.

```text
1. Read accepted frame for this case only.
2. Verify cutoff and pre-cutoff source visibility.
3. Build first-order pre-cutoff Evidence Units.
4. Build second-order pre-cutoff Evidence Units.
5. Write and seal the at-cutoff memo in the case artifact.
6. Only after sealing, open post-window outcome sources for that case.
7. Write outcome comparison and calibration.
8. Move to the next case.
```

Do not batch-open post-window materials across cases. Do not browse outcome
windows for later cases while working on an earlier case.

## Search Discipline Before Sealing

Before a case's at-cutoff memo is sealed:

- search only for pre-cutoff source families named in the accepted frame;
- use date-limited queries or archived sources where available;
- avoid outcome search terms such as "announcement", "acquisition",
  "cancellation", "rollback", "blackout", "shutdown", "lawsuit", "reversal",
  "partnership", "integration", "launch response", or similar terms unless
  they are pre-cutoff source-family terms in the accepted frame;
- do not open known post-window result pages;
- do not open search results whose visible title or snippet clearly identifies
  a post-window outcome;
- if a search result snippet reveals outcome information, ignore it as
  inadmissible environmental noise and do not record it;
- if you accidentally open a post-window outcome source before sealing the
  at-cutoff memo, stop that case and mark it `BLOCKED_BY_LEAKAGE` unless you
  can restart the case in a fresh context without carrying the leaked content.

## Verification Gate Hardening

The Verification Gate may verify that a cutoff precedes a named announcement or
outcome window using the accepted frame artifact. It must not open outcome
sources to learn what happened before the at-cutoff memo is sealed.

For changed live pages, prefer:

- public archives;
- timestamped official pages;
- dated policy or pricing pages;
- dated blog posts;
- dated community posts;
- public filings visible before cutoff.

If source visibility cannot be proven without opening post-window outcome
material, mark the source `BLOCKED_SOURCE_VISIBILITY`.

## Output Behavior

Follow the base prompt's output artifacts and final response contract.

Additionally, each case artifact must include an "Anti-Leakage Ledger" with:

- whether the case was run in a fresh context;
- whether any post-window search result snippets were seen before sealing;
- whether any post-window pages were opened before sealing;
- blocked sources caused by visibility or leakage risk;
- the exact point at which the at-cutoff memo was sealed.

The packet artifact must include a cross-case leakage summary.

## Stop Conditions

Stop the whole rerun if:

- the launch context includes the failed run's source list, URLs, notes, or
  post-window observations as usable evidence;
- the work starts by opening outcome sources;
- post-window outcome evidence is opened before any at-cutoff memo is sealed
  and the case cannot be restarted cleanly;
- the agent tries to repair leakage by merely promising not to use leaked
  information;
- the work turns into a case study, source map, data-spine design, feature
  plan, implementation plan, dashboard, scraper, API, scoring system, or
  automation plan.

## Final Response

In addition to the base prompt's final response fields, include:

- whether the anti-leakage rerun completed from a fresh context;
- any `BLOCKED_BY_LEAKAGE` cases;
- any `BLOCKED_SOURCE_VISIBILITY` cases;
- whether every at-cutoff memo was sealed before post-window outcome sources
  were opened for that same case.
