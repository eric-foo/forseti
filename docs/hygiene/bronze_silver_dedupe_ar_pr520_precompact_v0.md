# Pre-Compact Checkpoint

## Current objective

Continue the Orca Bronze/Silver lake convergence after PR #520, preserving the exact state of the Bronze Attachment Record and Silver projection discovery work so the next turn can resume without re-discovering the lane. The immediate next goal is to recover from the now-merged PR #520 boundary, update local base state, and choose the next material lake step under disciplined assumption-gate/fused routing.

## Current state

- What has been completed:
  - PR #520 implemented the Bronze/Silver convergence work unit: Bronze Attachment Record physicalization hardening plus Silver projection discovery/dedupe for Instagram Reels creator metric seed materialization.
  - Follow-up patch addressed accepted delegated-review findings F1, F2, and F3.
  - GitHub fresh read verified PR #520 is `MERGED`, head `9b0aecd568c70a5afbcbfc330f4594de52efa6f1`, merge commit `47ac025088d0e6a6bad4bbce96b7c34aac892edc`, base `codex/bronze-v41-clean-verify`.
  - PR worktree `worktrees/bronze-silver-dedupe-ar` is clean on `codex/bronze-silver-dedupe-ar...origin/codex/bronze-silver-dedupe-ar`.
- What is partially completed:
  - Bronze AR is now Mini God Tier / 90-95% doctrine shape for this slice, not full God Tier. It has typed, manifest-equivalent physicalized entries, but no copied body store, no full Manifest v2, and not every future source family has exercised it.
  - Silver projection discovery now has exact-content SHA256 dedupe and lake-native discovery, but F4/F5 residuals were accepted: full unfiltered `derived/` scan and supplied-file post-dedupe count semantics.
  - Other capture/projection lanes that interact with lake layout should rebase/verify after the PR #520 merge commit is in their base.
- What is currently broken or uncertain:
  - Unknown whether all local lanes have fetched the PR #520 merge commit.
  - Unknown whether CI was rerun after the final `9b0aecd` push and merge; local validation passed.
  - Main checkout `C:\Users\vmon7\Desktop\projects\orca` is dirty/untracked from unrelated lanes; do not treat it as clean or revert it.

## Important files and symbols

- `orca-harness/data_lake/catalog.py`
  - Relevant functions/classes/components: Bronze catalog source-surface and Attachment Record reporting.
  - Current role in the task: Bronze-side typed record/index surface.
  - Important changes or observations: Promoted AR entry behavior toward manifest-equivalent physicalized typed entries with schema v2 concepts, structured body references, replay/version pins, and physicalization semantics.
- `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py`
  - Relevant functions/classes/components: `discover_lake_projection_files`, exact-content dedupe, `_source_packet_pointer`.
  - Current role in the task: Silver/derived projection discovery feeding creator metric seed materialization.
  - Important changes or observations: Supports flat and sharded `derived/` layouts, dedupes exact-content duplicates by SHA256, and no longer assumes `projection.packet_id == raw_anchor` when discriminating sharded pointers.
- `orca-harness/runners/run_instagram_reels_creator_metric_seed_materialize.py`
  - Relevant functions/classes/components: `--from-lake`, `--data-root`, explicit `--projection` mode.
  - Current role in the task: Operator-facing materialization runner source-mode boundary.
  - Important changes or observations: Runner can discover projection files from the lake or consume explicit projection paths; invalid mixed modes are now tested.
- `orca-harness/tests/unit/test_instagram_reels_creator_metric_seed.py`
  - Relevant functions/classes/components: projection discovery/dedupe tests, source packet pointer tests, runner mode tests.
  - Current role in the task: Focused durability coverage for the PR #520 slice.
  - Important changes or observations: Expanded to 10 tests; includes divergent projection/raw anchors, legacy flat pointer assertion, explicit projection path mode, lake discovery mode, and invalid source-mode combinations.
- `orca-harness/tests/test_data_lake_catalog.py`
  - Relevant functions/classes/components: catalog inspection and AR-related tests.
  - Current role in the task: Bronze catalog regression coverage.
  - Important changes or observations: Passed locally with one expected symlink skip.
- `docs/prompts/reviews/bronze_silver_dedupe_ar_pr520_adversarial_code_review_prompt_v0.md`
  - Relevant functions/classes/components: delegated review prompt.
  - Current role in the task: Durable review commission artifact for PR #520.
  - Important changes or observations: Added by commit `e5b43b4c`.
- `docs/review-outputs/bronze_silver_dedupe_ar_pr520_adversarial_code_review_v0.md`
  - Relevant functions/classes/components: delegated review output.
  - Current role in the task: Adversarial review evidence and accepted residual ledger.
  - Important changes or observations: Cross-vendor review returned `accept_with_friction`; no blockers/majors; accepted findings F1/F2/F3 were patched.
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
  - Relevant functions/classes/components: typed Attachment Record implementation contract.
  - Current role in the task: Architectural authority for AR entry shape.
  - Important changes or observations: Contract is the reason AR entry is lake-owned and typed rather than inherited from capture body `file_id` or staging paths.
- `worktrees/bronze-silver-dedupe-ar`
  - Relevant functions/classes/components: PR #520 lane worktree.
  - Current role in the task: Clean source of the just-merged PR #520 branch.
  - Important changes or observations: Last observed log: `9b0aecd5 Address PR 520 review durability findings`, `e5b43b4c Add PR 520 delegated review prompt`, `1cacaa6e Harden Bronze AR and Silver projection discovery`.

## Decisions made

- Decision: Treat AR as Mini God Tier / 90-95% for now, not full GT.
  - Reason: Full GT would require broader manifest evolution, copied body storage decisions, richer cross-family guarantees, and more migration/rebuild tooling; that would have slowed the current convergence slice.
  - Consequence: Current AR shape is intentionally high-quality and extensible, but future full-GT promotion remains possible.
- Decision: Physicalize typed AR entries over preserved bodies without inheriting positional body `file_id` or staging-path semantics.
  - Reason: Body bytes are the evidence box; AR entry is the typed index card that downstream lanes can search and coordinate against.
  - Consequence: Capture lanes preserve raw evidence; bronze owns typed discoverability and provenance binding.
- Decision: Keep source-family-specific provenance out of lake-core fields unless it belongs in generic AR metadata.
  - Reason: Prevents `fragrance_review`, `instagram_creator`, `youtube`, and future lanes from each forcing one-off core fields.
  - Consequence: New capture lanes should map their facts into the generic AR/source-surface/provenance shape, not fork the core schema.
- Decision: Use exact-content SHA256 dedupe for discovered Silver projection files.
  - Reason: Preserves deterministic handling of duplicate projection payloads across flat/sharded derived layouts without semantic guessing.
  - Consequence: Distinct payloads remain distinct; exact duplicates collapse for materialization.
- Decision: Patch delegated-review F1/F2/F3 and accept F4/F5 as named residuals.
  - Reason: F1/F2/F3 were durability gaps with tight fixes; F4/F5 were acceptable operational semantics for this slice.
  - Consequence: Next work should not rediscover F1/F2/F3 as open, but should remember F4/F5 if expanding scale or reporting semantics.

## Superseded / Ignore

- Prior instruction, idea, artifact, or finding: Treating preserved raw bodies as the typed Attachment Record.
  - Why superseded: The contract and PR #520 implementation separate preserved evidence bodies from typed AR entries.
  - Current replacement: Raw body remains replay evidence; AR entry is lake-owned typed discoverability/provenance.
- Prior instruction, idea, artifact, or finding: Old concern that runner source-mode behavior was untested.
  - Why superseded: Follow-up patch added invalid-combo, explicit projection path, and `--from-lake` discovery wiring tests.
  - Current replacement: Keep the new tests as the regression anchor; only expand if source modes change again.
- Prior instruction, idea, artifact, or finding: Old concern that `_source_packet_pointer` relied on raw anchor equality.
  - Why superseded: Follow-up patch changed the discriminator and added divergent-anchor coverage.
  - Current replacement: Sharded pointer shape is detected from the projection path layout around the projection lane component.
- Prior instruction, idea, artifact, or finding: Any assumption that PR #520 is still open.
  - Why superseded: Fresh GitHub read after escalation verified `MERGED`.
  - Current replacement: Resume from PR #520 merge commit `47ac025088d0e6a6bad4bbce96b7c34aac892edc`, but fetch/reverify locally before basing new work.

## Commands and results

- Command:
  ```bash
  git status --short --branch
  ```
  Result:
  - Passed/failed/not run: Passed in `worktrees/bronze-silver-dedupe-ar`.
  - Important output: `## codex/bronze-silver-dedupe-ar...origin/codex/bronze-silver-dedupe-ar`
- Command:
  ```bash
  git log --oneline -5
  ```
  Result:
  - Passed/failed/not run: Passed in `worktrees/bronze-silver-dedupe-ar`.
  - Important output: `9b0aecd5 Address PR 520 review durability findings`; `e5b43b4c Add PR 520 delegated review prompt`; `1cacaa6e Harden Bronze AR and Silver projection discovery`; `eb29555a Merge pull request #516...`; `0a4593ed Stabilize Bronze catalog projection record ids`.
- Command:
  ```bash
  gh pr view 520 --json state,mergeCommit,headRefOid,headRefName,baseRefName,url
  ```
  Result:
  - Passed/failed/not run: Passed after sandbox escalation; the first sandboxed run failed with proxy connection refusal.
  - Important output: `state: MERGED`, `mergeCommit.oid: 47ac025088d0e6a6bad4bbce96b7c34aac892edc`, `headRefOid: 9b0aecd568c70a5afbcbfc330f4594de52efa6f1`, `baseRefName: codex/bronze-v41-clean-verify`, `url: https://github.com/eric-foo/orca/pull/520`.
- Command:
  ```bash
  python -m py_compile orca-harness\capture_spine\creator_profile_current\instagram_metric_seed.py orca-harness\runners\run_instagram_reels_creator_metric_seed_materialize.py orca-harness\tests\unit\test_instagram_reels_creator_metric_seed.py
  ```
  Result:
  - Passed/failed/not run: Passed before checkpoint.
  - Important output: Exit code 0.
- Command:
  ```bash
  python -m pytest -q orca-harness\tests\unit\test_instagram_reels_creator_metric_seed.py
  ```
  Result:
  - Passed/failed/not run: Passed before checkpoint.
  - Important output: `.......... [100%]`.
- Command:
  ```bash
  python -m pytest -q orca-harness\tests\test_data_lake_catalog.py
  ```
  Result:
  - Passed/failed/not run: Passed before checkpoint.
  - Important output: `...........s.............. [100%]`.
- Command:
  ```bash
  python .agents\hooks\check_retrieval_header.py --changed --strict
  ```
  Result:
  - Passed/failed/not run: Passed before checkpoint.
  - Important output: Exit code 0.
- Command:
  ```bash
  git diff --check
  ```
  Result:
  - Passed/failed/not run: Passed before checkpoint.
  - Important output: Exit code 0.
- Command:
  ```bash
  Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; python -m pytest -q orca-harness\tests
  ```
  Result:
  - Passed/failed/not run: Passed before checkpoint.
  - Important output: Full `orca-harness\tests` passed; one warning about unknown pytest mark in `test_reddit_screening_read_live.py:17`.

## Known issues and risks

- Issue: Local branches/worktrees may not include PR #520 merge commit yet.
  - Evidence: PR #520 was just verified merged remotely; no post-merge local fetch/rebase was performed before checkpoint.
  - Likely next action: Fetch and update the intended base before starting the next lake work unit.
- Issue: Main checkout has unrelated dirty/untracked state.
  - Evidence: Earlier lane state showed many untracked scratch/docs/worktree artifacts on `C:\Users\vmon7\Desktop\projects\orca`.
  - Likely next action: Do not clean or revert it; use isolated worktree/branch for new repo-changing work.
- Issue: F4 full unfiltered `derived/` scan remains accepted residual.
  - Evidence: Delegated review finding accepted as non-blocking for PR #520.
  - Likely next action: Revisit only when scaling lake discovery, adding source-family filters, or if runtime cost/noise appears.
- Issue: F5 `source_projection_files_supplied` post-dedupe semantics remains accepted residual.
  - Evidence: Delegated review finding accepted as non-blocking for PR #520.
  - Likely next action: Revisit if operator reporting needs pre/post-dedupe distinction.
- Issue: Other capture/projection lanes can conflict if continued before rebasing onto the lake convergence base.
  - Evidence: User asked whether interacting lanes should wait until Bronze/Silver is stronger; answer was yes for lake-interacting work.
  - Likely next action: Pause or rebase lake-touching lanes after PR #520 is fetched into their base.

## Constraints and user preferences

- Constraint/preference: Use assumption gate + fused discipline when the user asks for it.
  - Source or reason: Repeated user instruction: "assumption gate fused" / "disciplined."
- Constraint/preference: Aim for Mini God Tier / 90-95%, not 80/20.
  - Source or reason: User explicitly chose MGT doctrine and 90-95% target for AR.
- Constraint/preference: Admin/review/prompt work counts as one batched step, not the whole roadmap.
  - Source or reason: User repeatedly asked that admin is one step and wanted material next steps.
- Constraint/preference: Push back hard when an assumption is wrong or suboptimal.
  - Source or reason: `AGENTS.md` user instruction.
- Constraint/preference: Default allowed work is docs, decisions, prompts, reviews, migration notes, and overlay maintenance; implementation/runtime work requires explicit bounded authorization.
  - Source or reason: `AGENTS.md`.
- Constraint/preference: Do not mutate live external lake roots or archive/delete data without explicit operator action.
  - Source or reason: Prior lake workflow constraints and protected-action guard.
- Constraint/preference: Preserve raw authority; derived/Silver/projection outputs must be traceable back to raw evidence and typed AR/source-surface indexes.
  - Source or reason: Bronze/Silver lake architecture direction established across PRs #494, #499, #505, #510, #516, #520.

## Next steps

1. Run recovery checks: fetch/reverify PR #520 merge commit locally, confirm desired base branch contains `47ac025088d0e6a6bad4bbce96b7c34aac892edc`, and inspect the branch/worktree state before editing.
2. Start the next isolated work unit from the updated lake base; likely next material step is real lake convergence after PR #520: wire the next downstream Silver/consumer read path to use the typed AR/source-surface/projection indexes instead of lane-local assumptions.
3. Run focused tests for the touched lake/catalog/runner surfaces plus `check_retrieval_header --changed --strict` and `git diff --check`; if code is touched, run the relevant `orca-harness` focused tests before PR.

## Do not forget

- PR #520 is now verified merged remotely; earlier open-status concern is superseded, but local base still needs fetch/reverify.
- PR #520 made AR MGT, not full GT; do not oversell as complete God Tier.
- Other lake-interacting lanes should wait or rebase onto the PR #520 base before continuing.
- F1/F2/F3 from the delegated review were patched; F4/F5 remain accepted residuals.
- Do not revert dirty/untracked state in the main checkout.
