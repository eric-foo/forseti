# Pre-Compact Checkpoint

## Current objective

Continue the Data Lake v4.1 runner-blocker lane without anchoring on stale thread momentum. The immediate state is: fused implementation was requested, but it stopped at the assumption gate; a second-opinion adversarial review prompt has been filed and pushed to test whether that stop is correct.

## Current state

- What has been completed:
  - Capture runner v4.1 audit addendum committed and pushed on branch `codex/ig-reels-capture-spine`.
  - Blocker adversarial review prompt committed and pushed.
  - Delegate blocker adversarial review report committed and pushed; it confirmed the blocker is source-backed.
  - Fused implementation attempt was stopped by `workflow-assumption-gate`, not by implementation failure.
  - Second-opinion adversarial review prompt filed, committed, and pushed at HEAD `49f8bc81`.
- What is partially completed:
  - v4.1 forward-epoch contract exists on this branch, but source checks showed it is not on `origin/main`.
  - A review prompt exists for the second opinion; the durable report has not been returned yet.
- What is currently broken or uncertain:
  - `packet_shard` is named by the v4.1 contract but no derivation grammar was found in contract or harness source.
  - `DataLakeRoot` still appears to be v0/unsharded in the current source evidence.
  - Current branch is heavily polluted relative to `main`; do not create a PR without rechecking and separating scope.

## Important files and symbols

- `docs/prompts/reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_prompt_v0.md`
  - Relevant functions/classes/components: N/A.
  - Current role in the task: Filed prompt for second-opinion adversarial review of the fused assumption gate.
  - Important changes or observations: Committed in `49f8bc81`; SHA256 observed as `2CA01E7606C4F1DB50B6196AC685F46C09F24DB56115A1B68ABD9C61B97116BF`.
- `docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_v0.md`
  - Relevant functions/classes/components: N/A.
  - Current role in the task: Required output path for the pending second-opinion review.
  - Important changes or observations: Did not exist when prompt was authored.
- `docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md`
  - Relevant functions/classes/components: N/A.
  - Current role in the task: Prior adversarial review report.
  - Important changes or observations: Confirms addendum blocker claim is source-backed; flags `packet_shard` undefined and contract not on `origin/main`.
- `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`
  - Relevant functions/classes/components: N/A.
  - Current role in the task: Audit addendum that explains why current runners are not v4.1-compliant.
  - Important changes or observations: Earlier freshness labels are stale; use current source reads before strict claims.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`
  - Relevant functions/classes/components: `packet_shard`, `.orca-lake-epoch.json`, v4.1 root marker, forward writer obligations.
  - Current role in the task: Controlling candidate contract for v4.1 Data Lake forward writers.
  - Important changes or observations: It requires `raw/<packet_shard>/<packet_id>/`; no derivation rule was found.
- `orca-harness/data_lake/root.py`
  - Relevant functions/classes/components: `ROOT_MARKER_CONTRACT_VERSION`, `allocate_raw_packet_dir`, `stage_raw_packet`, `publish_raw_packet`, availability refs.
  - Current role in the task: Shared write path blocking all runner compliance.
  - Important changes or observations: Source checks observed `ROOT_MARKER_CONTRACT_VERSION = "v0"`, unsharded availability refs, and unsharded raw write entry points.
- `orca-harness/source_capture/writer.py`
  - Relevant functions/classes/components: `write_local_source_capture_packet`, lake-path write flow.
  - Current role in the task: Shared Source Capture packet writer that calls `DataLakeRoot`.
  - Important changes or observations: Existing seamed runners inherit `DataLakeRoot` behavior.
- `orca-harness/source_capture/packet_assembly.py`
  - Relevant functions/classes/components: `stage_and_write_packet`.
  - Current role in the task: Shared staged packet writer for some runners.
  - Important changes or observations: Existing seamed runners inherit `DataLakeRoot` behavior.
- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - Relevant functions/classes/components: `_PRODUCER_TOKENS`, `_SEAM_TOKEN`, `KNOWN_UNSYNCED`.
  - Current role in the task: Seam inventory test, not v4.1 behavior proof.
  - Important changes or observations: Current source check observed 12 packet-producing runners, 3 with `data_root`, 9 unsynced.

## Decisions made

- Decision: Do not claim the blocker is cleared.
  - Reason: Current source evidence still shows v0/unsharded `DataLakeRoot`, undefined `packet_shard`, and 9 unsynced direct packet runners.
  - Consequence: Fused implementation must not start until the assumption gate clears or the owner makes a precise durable-layout decision.
- Decision: Do not default `packet_shard` in code.
  - Reason: Shard grammar becomes durable lake layout; guessing would bake in storage semantics.
  - Consequence: Either the contract must define the rule, or the owner must explicitly authorize a branch-only/default rule before implementation.
- Decision: Commission a second opinion.
  - Reason: The gate may be correctly cautious, but it may also be overblocking if owner "fused go" can authorize branch-only implementation.
  - Consequence: The second-opinion prompt asks the reviewer to attack both sides.
- Decision: No PR was created.
  - Reason: `git diff --stat main..HEAD` observed a broad polluted branch, not a clean PR surface.
  - Consequence: Keep branch/push facts separate from PR readiness.

## Superseded / Ignore

- Prior instruction, idea, artifact, or finding: "All runners now drop into v4.1."
  - Why superseded: Source-backed audit and review say no current runner is fully v4.1-compliant.
  - Current replacement: Treat v4.1 runner support as blocked pending shared root semantics and runner seam work.
- Prior instruction, idea, artifact, or finding: "Blocker cleared by the review."
  - Why superseded: Review confirmed the blocker; it did not patch code or authorize implementation.
  - Current replacement: Blocker remains until contract/shard/root implementation conditions are satisfied.
- Prior instruction, idea, artifact, or finding: "Fused go means implement anyway."
  - Why superseded: Fused sequencing stops at the first gate that does not clear; assumption gate blocked.
  - Current replacement: Rerun fused only after second opinion or explicit owner decision clears the gate.
- Prior instruction, idea, artifact, or finding: Old handoff active objective was read-only audit/report only.
  - Why superseded: That lane completed addendum/review/prompt outputs; current active state is second-opinion decision before possible implementation.
  - Current replacement: Continue only with the second-opinion review or owner decision, then re-enter pre-implementation gates.
- Prior instruction, idea, artifact, or finding: Live root evidence proves v4.1 behavior.
  - Why superseded: Live root was legacy/mixed evidence only; it is not a v4.1 validation target.
  - Current replacement: Use repo source and targeted tests for v4.1 behavior; do not write to `F:\orca-data-lake`.

## Commands and results

- Command:
  ```bash
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: Passed.
  - Important output: branch `codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine`; unrelated untracked files remain in `.codex/hooks/`, `_scratch/`, `docs/hygiene/`, `docs/prompts/deep-thinking/`, `docs/prompts/patches/`, `docs/prompts/product-planning/`, `docs/workflows/`, and `worktrees/`.
- Command:
  ```bash
  git log --oneline --decorate -5
  ```
  Result:
  - Passed/failed/not run: Passed.
  - Important output: `49f8bc81` HEAD/origin is `docs: add v4.1 assumption gate second-opinion prompt`; earlier commits include `b82551f5`, `558265a3`, `3628dbac`, `f95c33ae`.
- Command:
  ```bash
  git rev-parse --short HEAD; git rev-parse --short origin/codex/ig-reels-capture-spine
  ```
  Result:
  - Passed/failed/not run: Passed.
  - Important output: both returned `49f8bc81`.
- Command:
  ```bash
  git diff --stat main..HEAD
  ```
  Result:
  - Passed/failed/not run: Passed.
  - Important output: `320 files changed, 4117 insertions(+), 101718 deletions(-)`. This is why PR creation remains unsafe/misleading without lane cleanup.
- Command:
  ```bash
  git diff --check -- docs/prompts/reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_prompt_v0.md
  ```
  Result:
  - Passed/failed/not run: Passed.
  - Important output: no whitespace errors printed.

## Known issues and risks

- Issue: `packet_shard` rule missing.
  - Evidence: v4.1 contract uses `raw/<packet_shard>/<packet_id>/`; prompt-author checks found no derivation grammar in the contract or harness source.
  - Likely next action: Await second-opinion report or owner explicitly defines the rule.
- Issue: v4.1 contract not on `origin/main`.
  - Evidence: prompt-author `git cat-file` check reported the contract exists on disk/branch but not in `origin/main`.
  - Likely next action: Owner decides whether to land contract first or authorize branch-only implementation.
- Issue: `DataLakeRoot` still v0/unsharded.
  - Evidence: source checks observed v0 marker and unsharded raw paths in `root.py`.
  - Likely next action: After shard/authority decision, patch shared `DataLakeRoot` before broad runner wiring.
- Issue: Runner seam coverage is incomplete.
  - Evidence: source check observed 12 producers, 3 seamed, 9 unsynced.
  - Likely next action: Wire remaining direct packet runners only after shared root behavior is v4.1.
- Issue: Dirty/untracked worktree noise.
  - Evidence: `git status` shows many unrelated untracked files.
  - Likely next action: Ignore unrelated files; do not revert; inspect target paths before any future edit.
- Issue: Branch is polluted relative to `main`.
  - Evidence: `main..HEAD` diff stat is broad and includes many deletions outside this lane.
  - Likely next action: Do not open PR without separating or rebasing lane scope.

## Constraints and user preferences

- Constraint/preference: User asked for precompact "to get rid of anchoring."
  - Source or reason: Current user instruction. Next thread should trust this checkpoint and fresh source reads over conversational momentum.
- Constraint/preference: Follow Orca confirm-don't-trust source loading.
  - Source or reason: User's earlier packet instruction and AGENTS/overlay behavior.
- Constraint/preference: Push back hard when the user's input would cause a bad technical decision.
  - Source or reason: User-supplied AGENTS instruction.
- Constraint/preference: Implementation/runtime work requires explicit bounded authorization and gates still apply.
  - Source or reason: AGENTS.md and fused/assumption-gate contracts.
- Constraint/preference: Do not write to `F:\orca-data-lake` or run live capture by default.
  - Source or reason: Audit/review lane drift guards and prompt constraints.
- Constraint/preference: Do not import `jb` policy or external workflow authority.
  - Source or reason: AGENTS.md and Orca overlay.
- Constraint/preference: Use `apply_patch` for manual file edits; do not revert unrelated user changes.
  - Source or reason: developer instructions.

## Next steps

1. If continuing with review, send/execute the filed second-opinion prompt and require the report at `docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_v0.md`.
2. On review return, adjudicate findings before resuming fused; do not treat reviewer output as automatically accepted.
3. If owner bypasses review, require a precise owner decision on `packet_shard` derivation and contract authority, then rerun assumption gate before implementation.
4. After gate clears, patch shared `DataLakeRoot` v4.1 behavior first, then tests, then existing seamed runners, then remaining unsynced direct packet runners.
5. Before any PR, recheck branch pollution and isolate lane scope.

## Do not forget

- Critical detail: The current blocker is not "runner wiring" first; it is durable shared root/path semantics first.
- Critical detail: A plausible default was discussed but not accepted: first three lowercase hex chars of `sha256(packet_id)` as `packet_shard`.
- Critical detail: The second-opinion prompt must attack whether the gate is overblocking; do not anchor on the previous gate result as final truth.
- Critical detail: Do not claim v4.1 readiness, validation, or implementation completion until source changes and tests actually prove it.
- Critical detail: The current pushed HEAD is `49f8bc81` on `codex/ig-reels-capture-spine`.
