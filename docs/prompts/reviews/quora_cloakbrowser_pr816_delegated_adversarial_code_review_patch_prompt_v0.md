# Quora CloakBrowser PR 816 Delegated Adversarial Code Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Delegated adversarial code review-and-bounded-patch commission for PR #816, covering profile-backed CloakBrowser capture and the source-detail sufficiency gate.
use_when:
  - Commissioning de-correlated review of PR #816 before CA adjudication.
  - Reconstructing the Quora source-capture sufficiency-gate review request.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
branch_or_commit: PR #816 head observed as 11fe885c5574ed4c51038a7dea26233dc51f3ff3 on branch codex/quora-cloakbrowser-patch.
stale_if:
  - PR #816 head changes from 11fe885c5574ed4c51038a7dea26233dc51f3ff3 before review starts.
  - The target worktree has dirty state other than untracked _test_runs/ before the reviewer begins.
  - PR #816 is closed or merged before review starts.
```

preflight_defaults: `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom PR-review prompt pack
  output_mode: review-report
  output_destination: docs/review-outputs/quora_cloakbrowser_pr816_delegated_adversarial_code_review_patch_v0.md
  template_kind: review plus bounded patch commission
  edit_permission: docs-write for this prompt artifact only; delegated reviewer receives bounded patch authority as stated below
  target_scope: PR #816 review prompt for Quora source-capture profile-backed CloakBrowser and source-detail sufficiency-gate patch
  dirty_state_checked: yes - prompt authored in a separate prompt-only worktree off main; target PR worktree observed clean except untracked _test_runs/
  blocked_if_missing: target PR worktree/repo access, expected head SHA, or de-correlated controller
```

## Routing

Smallest complete outcome: a de-correlated reviewer inspects PR #816 for false-success paths and may leave a bounded uncommitted patch in the PR files only.

Regime: Complicated, layer-based.

Why: the task is a multi-file implementation/code diff, so Orca's provisional delegated-review-and-patch convention is used as commission discipline only; the actual review route is repo-bound adversarial code review.

Allowed next move: paste the filed prompt below into a different-vendor controller with repo access to the target worktree.

Disallowed next move: local self-review, same-vendor review presented as delegated, or broadening into unrelated capture/runtime cleanup.

## Paste-Ready Prompt

````text
You are the delegated adversarial code review-and-bounded-patch controller for Forseti PR #816.

Reviewer de-correlation requirement:
- The authored PR was prepared by OpenAI/Codex GPT-5.
- To satisfy this commission, you must be a different vendor/family from OpenAI/Codex/GPT.
- If you are OpenAI/Codex/GPT-family, stop and return BLOCKED_CONTROLLER_NOT_DECORRELATED.
- This is a who-constraint, not a model recommendation. Do not recommend, rank, or imply runtime model choice.

Review target:
- Repository: eric-foo/forseti
- PR: https://github.com/eric-foo/forseti/pull/816
- Target worktree: C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\quora-cloakbrowser-patch
- Branch: codex/quora-cloakbrowser-patch
- Expected HEAD: 11fe885c5574ed4c51038a7dea26233dc51f3ff3
- Local main observed: 8dfec4c39295ff41dfe18f4e69b454bf8d361cf9
- Merge-base observed: 67123f36840f8620d2bb8fff6a0b4b1330bfaeaa
- Review diff: `git diff main...HEAD`

Start gate:
1. Open the target worktree directly. Do not review a summary, alternate checkout, recreated source pack, or pasted diff as a substitute.
2. Run:

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse main
git diff --name-only main...HEAD
```

3. Proceed only if:
   - branch is `codex/quora-cloakbrowser-patch`;
   - HEAD is `11fe885c5574ed4c51038a7dea26233dc51f3ff3`;
   - local main is `8dfec4c39295ff41dfe18f4e69b454bf8d361cf9` or you explicitly record the newer main SHA and still review the PR branch with `main...HEAD`;
   - dirty state before review is clean except untracked `_test_runs/`.
4. If these checks fail, return BLOCKED with the observed state. Do not proceed by reviewing stale or substituted source.

Cynefin routing:
- Smallest complete outcome: find blocker/major false-success, provenance, or persistence bugs in PR #816 and patch only if the fix is local to the PR files.
- Regime: complicated, layer-based.
- Current bottleneck: whether the new "success only when required source details are present" gate actually prevents useless packet success without breaking existing capture runners.
- Riskiest assumption: a 0-exit CloakBrowser Quora run proves useful source capture only when the sufficiency predicates are enforced, not merely because the page loaded.
- Stop or pivot condition: if the correct fix needs new capture doctrine, packet schema change, credential-store policy, or browser-profile security design, return NEEDS_ARCHITECTURE_PASS or an off-scope finding instead of patching.

Required method sequence:
1. Read this prompt.
2. REFERENCE-LOAD `workflow-deep-thinking` if available.
3. REFERENCE-LOAD `workflow-code-review` if available.
4. REFERENCE-LOAD `.agents/workflow-overlay/delegated-review-patch.md` as commission discipline only; do not force this multi-file code diff into the single-artifact provisional convention.
5. Do not APPLY any method yet.
6. SOURCE-LOAD the required sources below.
7. Declare SOURCE_CONTEXT_READY or SOURCE_CONTEXT_INCOMPLETE.
8. APPLY deep-thinking posture to frame the highest-risk false-success paths.
9. APPLY code-review posture to the PR diff.
10. If a bounded fix is needed, patch only the submitted PR files listed below. Leave the diff uncommitted.
11. Fresh-read changed files and run the required validation slice.
12. Write the durable review report to the report path below and return a short courier summary.

Required source reads:
- AGENTS.md
- .agents/workflow-overlay/README.md
- .agents/workflow-overlay/decision-routing.md
- .agents/workflow-overlay/review-lanes.md
- .agents/workflow-overlay/delegated-review-patch.md
- .agents/workflow-overlay/prompt-orchestration.md
- .agents/workflow-overlay/source-loading.md
- The full PR diff from `git diff main...HEAD`
- forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py
- forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
- forseti-harness/runners/run_source_capture_browser_packet.py
- forseti-harness/runners/run_source_capture_authenticated_browser_packet.py
- forseti-harness/source_capture/source_detail_sufficiency.py
- forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
- forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
- forseti-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py
- forseti-harness/tests/unit/test_source_detail_sufficiency.py

Local live-run evidence to inspect if present, but never patch or stage:
- _test_runs\source_capture_quora_b2b_search_auth_browser_sufficiency_fail_probe_20260709\manifest.json
- _test_runs\source_capture_quora_b2b_search_auth_browser_sufficiency_fail_probe_20260709\receipt.md
- _test_runs\source_capture_quora_b2b_search_auth_browser_sufficiency_fail_probe_20260709\raw\02_authenticated_browser_visible_text.txt
- _test_runs\source_capture_quora_b2b_search_auth_browser_sufficiency_fail_probe_20260709\raw\04_authenticated_browser_snapshot_metadata.json
- _test_runs\source_capture_quora_b2b_search_cloak_profile_sufficiency_success_20260709\manifest.json
- _test_runs\source_capture_quora_b2b_search_cloak_profile_sufficiency_success_20260709\receipt.md
- _test_runs\source_capture_quora_b2b_search_cloak_profile_sufficiency_success_20260709\raw\02_cloakbrowser_visible_text.txt
- _test_runs\source_capture_quora_b2b_search_cloak_profile_sufficiency_success_20260709\raw\04_cloakbrowser_snapshot_metadata.json

If these live-run files are absent, mark the live evidence unavailable and continue with code/test review. Do not perform new live Quora, Cloudflare, login, cookie, or CloakBrowser traffic unless the owner explicitly authorizes it in the current turn. Never print cookies, profile contents, or secret-bearing browser state; labels and non-secret metadata only.

What changed in PR #816:
- Fixes CloakBrowser launch compatibility by removing an obsolete launch argument.
- Adds label-indirected profile-backed CloakBrowser capture using a persistent browser context when a caller supplies a user-data label and session mode.
- Adds a source-detail sufficiency gate shared by browser, authenticated browser, and CloakBrowser packet runners.
- Adds CLI predicates:
  - `--require-not-access-blocked`
  - `--require-min-visible-text-bytes`
  - repeatable `--require-visible-text`
  - repeatable `--require-visible-regex`
  - repeatable `--require-rendered-dom-text`
  - repeatable `--require-rendered-dom-regex`
- Preserves packets even when sufficiency fails, but returns nonzero after packet write when required source details are missing.
- Uses the sufficiency gate to make "0 details captured" worthless for the Quora B2B search case: lower rung fails with Cloudflare/0 visible text; profile-backed CloakBrowser passes only when the required visible and rendered details are present.

Observed author-side validation evidence, to verify rather than trust:
- Python compile over the new/changed source files passed.
- Focused unit pytest over these four files completed at 100 percent:
  - tests/unit/test_source_detail_sufficiency.py
  - tests/unit/test_source_capture_browser_snapshot.py
  - tests/unit/test_source_capture_authenticated_browser_snapshot.py
  - tests/unit/test_source_capture_cloakbrowser_snapshot.py
- `git diff --check` passed, with line-ending warnings only.
- Lower rung authenticated browser Quora probe returned nonzero after packet write with `source_detail_sufficiency_failed`, `cloudflare_interstitial`, and visible text byte count 0.
- Profile-backed CloakBrowser Quora probe returned 0 with `source_detail_sufficiency_passed`, `persistent_profile_loaded: true`, visible text byte count 12374, title `Search`, final URL `https://www.quora.com/search?q=B2B+questions`, and visible details including `Results for B2B questions`.

Editable PR scope:
- forseti-harness/source_capture/adapters/cloakbrowser_snapshot.py
- forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
- forseti-harness/runners/run_source_capture_browser_packet.py
- forseti-harness/runners/run_source_capture_authenticated_browser_packet.py
- forseti-harness/source_capture/source_detail_sufficiency.py
- forseti-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
- forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
- forseti-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py
- forseti-harness/tests/unit/test_source_detail_sufficiency.py

Everything else is read-only / flag-only. Do not edit prompts, docs, overlay files, live `_test_runs/`, browser profile folders, auth-state files, cookies, credentials, unrelated adapters, packet schema doctrine, Cleaning, ECR, Judgment, Data Lake, or product artifacts.

Review focus:
1. False success: Can any runner still return success when required source details are absent, the page is blocked/login/security, or visible text is empty?
2. Packet preservation: On sufficiency failure, is the packet still written and inspectable while the process/function return is nonzero and unmistakably failed?
3. Backward compatibility: When no sufficiency requirements are supplied, do browser, authenticated browser, and CloakBrowser packet runners preserve prior behavior and tests?
4. Predicate correctness: Are literal and regex checks applied to the right visible-text and rendered-DOM surfaces, with deterministic failure reasons and no false pass on empty strings?
5. Access-block handling: Does `--require-not-access-blocked` correctly integrate with existing access classification and avoid treating Cloudflare/login/security interstitials as useful source capture?
6. Profile-backed CloakBrowser: Does `user_data_dir` use Playwright persistent context correctly without leaking credentials, widening profile path authority, or confusing "profile loaded" with "source details captured"?
7. Label/session posture: Are profile labels and session modes recorded enough for provenance without exposing raw cookies or local secrets?
8. CloakBrowser compatibility fix: Does removing the obsolete launch argument preserve existing launch behavior and tests while avoiding a silent fallback to a different browser path?
9. Test strength: Would the new tests fail under the old behavior? Do they pin the important invariants, not just one happy Quora-shaped path?
10. Live evidence interpretation: Do the observed Quora probes support only the narrow claim that the sufficiency gate distinguishes useless lower-rung packet success from useful profile-backed capture for this query?

Patch authority:
- You may apply a bounded patch only inside the editable PR scope above.
- Patch only defects that materially affect false-success prevention, profile-backed CloakBrowser persistence/provenance, source-detail sufficiency semantics, or directly adjacent tests.
- Leave any patch as an uncommitted working-tree diff. Do not commit, push, merge, rebase, or update the PR.
- If the correct fix lies outside editable scope, return an off-scope finding with `next_authorized_action`.
- If the problem is design-level, return `NEEDS_ARCHITECTURE_PASS`, stop patching, and revert any partial diff.

Required validation:
- Always run these from the target worktree after review if the environment supports local Python tests. If not, return BLOCKED or NOT_RUN with the concrete reason.

```powershell
git status --short --branch
git diff --check
Push-Location forseti-harness
python -m py_compile source_capture\source_detail_sufficiency.py source_capture\adapters\cloakbrowser_snapshot.py runners\run_source_capture_browser_packet.py runners\run_source_capture_authenticated_browser_packet.py runners\run_source_capture_cloakbrowser_packet.py
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests\unit\test_source_detail_sufficiency.py tests\unit\test_source_capture_browser_snapshot.py tests\unit\test_source_capture_authenticated_browser_snapshot.py tests\unit\test_source_capture_cloakbrowser_snapshot.py
Pop-Location
```

Do not run live Quora or browser-profile captures unless separately authorized.

Report destination:
- Write the durable review report to:
  `docs/review-outputs/quora_cloakbrowser_pr816_delegated_adversarial_code_review_patch_v0.md`
- If you cannot write that report, return a chat-only BLOCKED result and do not pretend the durable report exists.

Report requirements:
- Start with:
  - `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
  - `reviewed_by: <actual reviewer/tooling identity>`
  - `authored_by: OpenAI/Codex GPT-5`
  - `de_correlation_bar: cross_vendor_discovery`
  - `patch_applied: yes/no`
- Findings first, ordered critical, major, minor.
- For each finding: severity, file/line, evidence, risk, minimum_closure_condition, next_authorized_action, and whether you patched it.
- Include the highest-risk false-success paths you considered, even if no findings survive.
- Include patch summary and unified diff if you patched.
- Include validation commands and observed output, or a precise not-run reason.
- Include residual risk.
- Include verdict only as review-routing shorthand, not approval or readiness. Acceptable values:
  - `PATCHED_FOR_CA_ADJUDICATION`
  - `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`
  - `NEEDS_ARCHITECTURE_PASS`
  - `BLOCKED`

Review-use boundary:
Your findings, diff, validation output, and verdict are decision input for CA/home-model adjudication. They are not approval, readiness, validation proof, mandatory remediation, merge authority, or auto-keep authority. The CA decides what, if anything, is kept.
````
