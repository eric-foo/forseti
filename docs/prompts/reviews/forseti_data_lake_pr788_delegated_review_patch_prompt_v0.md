# Forseti Data Lake PR 788 Delegated Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Delegated review-and-bounded-patch commission for Forseti Data Lake PR #788.
use_when:
  - Commissioning de-correlated review of PR #788 before human-gated merge.
  - Verifying Data Lake live references, runner help text, and bronze/silver lake test sync after the Orca to Forseti migration.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
branch_or_commit: PR #788 head observed as 4790864778bb64d62bc7a212ad17de3e88eb4d9d on 2026-07-08.
stale_if:
  - PR #788 head changes from 4790864778bb64d62bc7a212ad17de3e88eb4d9d before review starts.
  - PR #788 is closed or merged before review starts.
```

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom PR-review prompt pack
  edit_permission: docs-write for this prompt only; delegated reviewer receives bounded patch authority as stated below
  target_scope: PR #788 review prompt for Forseti Data Lake live reference sync only
  dirty_state_checked: yes - authored in a separate clean worktree because the root checkout had unrelated untracked files
  blocked_if_missing: PR #788 diff or repository access
```

## Paste-Ready Prompt

````text
You are the delegated review-and-bounded-patch controller for Forseti PR #788.

Review target:
- Repository: eric-foo/forseti
- PR: https://github.com/eric-foo/forseti/pull/788
- Branch: codex/forseti-data-lake-live-ref-sync
- Observed PR head: 4790864778bb64d62bc7a212ad17de3e88eb4d9d
- Base: origin/main at the time you run the review

Reviewer de-correlation requirement:
- The authored PR was prepared by OpenAI/Codex GPT-5.
- Use a different model family/vendor for discovery if available.
- Record your actual reviewer identity/tooling in the report.

Hard boundaries:
- Do not merge the PR.
- Do not push.
- Do not commit.
- Do not run registration_integrity.py --selftest.
- Do not rewrite historical provenance, committed evidence paths, or compatibility aliases merely because they contain "Orca".
- Do not widen the review into unrelated Forseti migration cleanup.

Required source reads before findings:
- AGENTS.md
- .agents/workflow-overlay/README.md
- .agents/workflow-overlay/review-lanes.md
- .agents/workflow-overlay/delegated-review-patch.md
- .agents/workflow-overlay/validation-gates.md
- .agents/workflow-overlay/prompt-orchestration.md
- The full PR #788 diff against origin/main.

Workflow posture:
- Use workflow-deep-thinking first if available.
- Use workflow-code-review for runner/test/code surfaces.
- Use workflow-adversarial-artifact-review for docs/authority/workflow surfaces.
- Use workflow-delegated-review-patch only as the review-and-patch commissioning discipline, not as authority to merge or broaden scope.
- If these skills are unavailable in your environment, read the overlay sources above and perform the source-bound equivalent manually. Mark skill availability clearly in the report. Do not claim approval, validation, readiness, or mandatory remediation authority.

What changed in PR #788:
- This is a symmetric text-only migration/reference-sync diff: observed author-side shape was 63 files changed, 326 insertions, 326 deletions.
- Live Data Lake docs under forseti/product/spines/data_lake/** were updated from stale live Orca wording to Forseti where the text is current authority or workflow guidance.
- Live path references were updated:
  - orca-harness -> forseti-harness where they refer to current code/test paths.
  - docs/workflows/orca_repo_map_v0.md -> docs/workflows/forseti_repo_map_v0.md where they refer to current repo-map paths.
  - docs/decisions/orca_data_lake_derived_retrieval_activation_proposal_v0.md -> docs/decisions/forseti_data_lake_derived_retrieval_activation_proposal_v0.md where the new decision file exists and the old path no longer does.
- One current command placeholder was changed from <ORCA_DATA_ROOT> to <FORSETI_DATA_ROOT>.
- The TikTok live batch probe runner help text was updated to say explicit Forseti data lake root, and to state that FORSETI_DATA_ROOT and legacy ORCA_DATA_ROOT are not read by that explicit-root-only runner path.
- Data Lake tests under forseti-harness/tests/** changed tmp_path / "orca-data" fixture roots to tmp_path / "forseti-data".

Intentional residuals that must not be flagged by word match alone:
- ORCA_DATA_ROOT remains as a legacy compatibility alias where the code/docs intentionally discuss migration compatibility.
- .orca-* paths may remain where they are existing storage/control filenames or compatibility/provenance.
- Old evidence paths such as F:\orca-data-lake may remain where they identify committed external evidence or historical provenance.
- Product JSON/source evidence pointers should not be renamed unless the underlying lake bytes actually moved; changing those strings can falsify provenance.
- Historical prompts, reviews, migration records, and old point-in-time body prose are not the target unless PR #788 changed them into live current guidance.

Primary review question:
Does PR #788 complete the current Data Lake live-reference sync without creating confusion between Forseti's current Data Lake identity and intentionally preserved Orca compatibility/provenance surfaces?

Required checks:
1. Confirm the diff is scoped to PR #788 and no unrelated files are changed.
2. Confirm live Data Lake docs now read as Forseti-first current authority where they should.
3. Confirm bronze/silver Data Lake runners, runner help text, tests, and inventory gates are synchronized with the same Forseti-first root/path language.
4. Confirm legacy ORCA_DATA_ROOT and .orca-* references remain only where compatibility/provenance requires them.
5. Confirm evidence provenance was not falsified by renaming old lake paths, committed source paths, or historical evidence strings.
6. Confirm no stale live path references remain for orca-harness, docs/workflows/orca_repo_map_v0.md, or the old derived-retrieval decision path in the Data Lake live spine.
7. Confirm the author's validation evidence by rerunning the material checks below, not by trusting this prompt.

Commands to run from repository root unless stated otherwise:

```powershell
git status --short --branch
git diff --stat origin/main...HEAD
git diff --check origin/main...HEAD
python .agents/hooks/check_review_routing.py --strict --base origin/main
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_placement.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict --base origin/main
```

Run the Data Lake test subset from forseti-harness:

```powershell
Push-Location forseti-harness
$tests = git -C .. diff --name-only origin/main...HEAD -- 'forseti-harness/tests' | ForEach-Object { $_ -replace '^forseti-harness/', '' }
$extra = @(
  'tests/contract/test_capture_runner_lake_seam_coverage.py',
  'tests/contract/test_data_lake_inventory_gate.py'
)
$all = @($extra + $tests | Select-Object -Unique)
python -m pytest -q @all
Pop-Location
```

Run targeted stale-live-reference scans from repository root:

```powershell
rg -n "orca-harness|docs/workflows/orca_repo_map_v0\.md|docs/decisions/orca_data_lake_derived_retrieval_activation_proposal_v0\.md|Orca's data lake|Orca meaning|In Orca|Orca full|<ORCA_DATA_ROOT>|Orca source data|Every time Orca|product claim Orca|collapse Orca|Orca may say|Orca must not|Time Orca|Orca project facts|low lock-in: Orca" forseti/product/spines/data_lake
rg -n "Orca data lake|Orca's data lake|orca-harness|Defaults to ORCA_DATA_ROOT" forseti-harness/runners forseti-harness/data_lake forseti-harness/capture_spine forseti-harness/cleaning forseti-harness/source_capture forseti-harness/youtube_capture -g "*.py"
rg -n --fixed-strings 'tmp_path / "orca-data"' forseti-harness/tests
```

Interpreting scan results:
- The three rg commands above should return no forbidden live hits unless a hit is clearly compatibility/provenance/historical and should be documented as intentionally preserved.
- Do not treat a raw "Orca" hit as a defect unless it is live current guidance, live runner UX, a current root/path example, or a current Data Lake authority statement.

Patch authority:
- You may apply a bounded patch only if the defect is inside a file touched by PR #788, the fix is mechanical and local, and the correction does not require a new doctrine or owner decision.
- You may patch missing Forseti-first wording, stale current path references, or incorrect runner/test wording inside PR #788's touched scope.
- You may not patch historical provenance, external evidence strings, source JSON evidence pointers, branch metadata, merge metadata, or unrelated migration residue.
- Leave any patch as an uncommitted diff. Do not commit, push, or merge.
- If a necessary fix is outside PR #788's touched files, report it as an out-of-scope follow-up instead of patching it.

Report destination:
- Write the durable review report to:
  docs/review-outputs/adversarial-artifact-reviews/forseti_data_lake_pr788_delegated_adversarial_review_patch_v0.md
- If you cannot write that report, return a chat-only blocked/advisory result and do not pretend the durable report exists.

Report requirements:
- Findings first, ordered critical, major, minor.
- Include file/line evidence for each finding where possible.
- Include command results with PASS/FAIL/BLOCKED and short evidence.
- Include a section named "Intentional Residuals Checked" covering ORCA_DATA_ROOT, .orca-* paths, old evidence paths, and product JSON/source evidence pointers.
- Include patch_applied: yes/no.
- If patch_applied is yes, list every changed file and leave the diff uncommitted.
- Include verdict only as review-routing shorthand, not approval or readiness. Acceptable values: block, accept_with_friction, accept_no_findings.

Review-use boundary:
This review is decision input for the commissioning owner. It is not approval, validation proof, readiness, product proof, merge authority, or mandatory-remediation authority. Human merge remains the only landing gate.
````
