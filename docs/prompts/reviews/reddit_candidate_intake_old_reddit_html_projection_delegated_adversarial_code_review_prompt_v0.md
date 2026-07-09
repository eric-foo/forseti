# Reddit Candidate Intake Old Reddit HTML Projection Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated review-and-patch prompt
scope: De-correlated adversarial review-and-patch commission for the old Reddit HTML static-projection and Reddit .json refusal slice of Candidate URL Intake.
use_when:
  - Launching a delegated, de-correlated adversarial review-and-patch pass after the old Reddit HTML projection implementation slice.
  - Checking that the implementation and controlling docs preserve Candidate URL Intake as bounded Capture Spine provenance-only intake.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
input_hashes:
  candidate_url_intake_contract: 1D2BD160E94DF7A016ECB172FD0179244A135D1308CBFC0CA10D00692964E308
  reddit_candidate_url_intake_architecture: 3FC8E780AA984BFAD5ECBBCCA94CBCCCB1C61014B96E94DA4B508D6D6401E592
  reddit_candidate_url_intake_default_policy_decision: 5FFD5A945865A11CEE2A760204E7F5C6BF7CA3B772523CFDB08816C4BDC6E47A
  validation_py: 55249B3402030469FCF281E4868401CAE3B1434DF1F6D19D0648BADD2F67EB12
  projection_py: C22C2C582A7C8BE9950C3E1DE925BFCDD3E0923A13ED6ED310902D71EFB4F83D
  package_init_py: EFF628E4166D6550E5B485FA9C2CDD7EFFAE3E4A5D71D05173831A8661D0968C
  unit_test_py: C2FACFE2F17292D06D0B96624064E017BF8D7DF55E9E15CD6176EB248AF7F762
  contract_test_py: EF4A251E69D61B30BD92A6571C0F897871D246963FCAD62C303784265C42D0AE
branch_or_commit:
  branch: ecr-sp3-timing-deriver-slice1
  head: 14490ce878946f5f2073cabd27c5be0389ee147f
stale_if:
  - Any target product doc, implementation file, or test file changes before the delegated review runs.
  - The Candidate URL Intake parent contract, Reddit architecture, or default-policy decision changes.
  - Orca delegated-review, review-lane, prompt-orchestration, source-loading, or validation-gate authority changes.
```

## Prompt Status

Status: `READY_FOR_DELEGATED_REVIEW_PATCH_PROMPT_WITH_RECEIPT_GATE`.

This prompt does not run the delegated review. It does not validate, accept,
stage, commit, or claim implementation readiness. It renders the commission
that a de-correlated controller can use to review and, if warranted, propose a
bounded patch. Any controller diff, citations, and verdict remain claims for
Chief Architect adjudication.

## Launch Prompt

````text
You are the controller for a delegated adversarial review-and-patch commission
for Orca.

This is a `workflow-delegated-review-patch` commission in `base-subagent` mode.
De-correlation is a who-constraint, not a model recommendation. Do not add a
Recommended model block, do not rank runtime models, and do not treat this
commission as runtime model routing.

## Actor / Model-Family Receipt Gate

Before reading implementation or product sources, complete this receipt with
actual operator/tooling facts:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex current lane
  controller_model_family: <fill actual different-family controller>
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied | blocked
```

If `controller_model_family` is missing, same-family as
`author_home_model_family`, ambiguous, or still a placeholder, stop before
review and return `BLOCKED_DECORRELATION_RECEIPT_MISSING` or
`BLOCKED_CONTROLLER_NOT_DECORRELATED`.

If `current_receiving_actor_role` is `controller`, proceed as the controller
after the receipt is satisfied. Do not launch a replacement controller and do
not spawn recursive or unrelated subagents.

## Commission

Target:
- docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
- docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
- docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
- orca-harness/capture_spine/reddit_candidate_intake/validation.py
- orca-harness/capture_spine/reddit_candidate_intake/projection.py
- orca-harness/capture_spine/reddit_candidate_intake/__init__.py
- orca-harness/tests/unit/test_reddit_candidate_intake.py
- orca-harness/tests/contract/test_reddit_candidate_intake_contract.py

Required durable review report path:
- docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_v0.md

Workspace:
- C:\Users\vmon7\Desktop\projects\orca

Pinned source state at prompt creation:
- branch: ecr-sp3-timing-deriver-slice1
- head: 14490ce878946f5f2073cabd27c5be0389ee147f
- target hashes are recorded in the prompt retrieval header.

Dirty-state allowance:
- The target files may be modified, added, or untracked in the working tree.
- Unrelated dirty or untracked files are out of scope. Do not inspect or patch
  them unless a target-scope issue cannot be understood without one narrow
  adjacent read.
- Do not create, clone, request, or switch worktrees. Read the current working
  tree in place.

## Required Authority Sources

Read and follow:
- AGENTS.md
- .agents/workflow-overlay/README.md
- .agents/workflow-overlay/decision-routing.md
- .agents/workflow-overlay/delegated-review-patch.md
- .agents/workflow-overlay/source-of-truth.md
- .agents/workflow-overlay/source-loading.md
- .agents/workflow-overlay/review-lanes.md
- .agents/workflow-overlay/prompt-orchestration.md
- .agents/workflow-overlay/validation-gates.md
- docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
- docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
- docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
- docs/decisions/reddit_candidate_intake_no_live_access_delegated_review_adjudication_decision_v0.md if present

Then inspect only the target implementation and tests listed above, plus
minimal adjacent package/test configuration if needed to understand import or
test execution behavior.

Do not bulk-load unrelated Source Capture Armory adapters, Source Capture
Packet assembly, ECR, Cleaning, Judgment, source-quality, research corpus,
`_inbox`, historical review outputs, or unrelated prompt artifacts unless a
directly material target issue cannot be assessed without one narrow adjacent
read.

## Source-Gated Method Contract

REFERENCE-LOAD:
- workflow-delegated-review-patch
- workflow-deep-thinking
- workflow-code-review
- workflow-adversarial-artifact-review

Do not APPLY these methods before source readiness. SOURCE-LOAD the required
sources and declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.

After source readiness, APPLY:
1. `workflow-delegated-review-patch` to enforce receipt, role, scope, patch,
   citation, escalation, and CA-adjudication boundaries.
2. `workflow-deep-thinking` to frame the boundary problem, fake-pass paths, and
   decision criteria.
3. `workflow-code-review` to review code, tests, package boundaries, and
   implementation behavior.
4. `workflow-adversarial-artifact-review` only for the product/decision-doc
   claims that govern this slice.

If a required review lane is unavailable, unresolved, or cannot be applied
after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the
reason and do not patch that lane's target. Do not silently emulate a review
lane inline.

## Cynefin Routing

Run Orca Cynefin routing before review.

Expected routing:
- Smallest complete outcome: review the old Reddit static HTML projection and
  Reddit `.json` refusal slice for boundary leaks, fake-pass tests, and doc/code
  mismatch.
- Regime: complicated.
- Decomposition: risk-first mixed code/doc review over a small target slice.
- Current bottleneck: proving the local projection helper did not smuggle in
  live access, parser-runner behavior, raw Reddit payload persistence,
  thread-page capture, user/profile/body/comment capture, Armory capture, or
  Data Capture handoff.
- Riskiest assumption: tests pass because the happy-path fixture is narrow
  rather than because forbidden input surfaces and forbidden outputs are
  mechanically impossible or refused.
- Stop or pivot condition: if a correct fix requires live Reddit access,
  CloakBrowser/proxy invocation, Reddit `.json` intake, thread-page input,
  broad traversal, parser/consolidation runner design, source-access doctrine
  change, Source Capture Armory behavior, or Data Capture promotion, return
  `NEEDS_ARCHITECTURE_PASS`, leave no kept partial diff, and return findings
  only.
- Allowed next move: review and, if explicitly useful, patch only the target
  files listed in this prompt.
- Disallowed next move: live Reddit access, `.json` intake, thread body/comment
  retrieval, user/profile capture, CloakBrowser/proxy execution, Source Capture
  Packet generation, ECR/Cleaning/Judgment/source-quality work, fixture
  admission, Data Capture handoff claims, or unrelated package/dependency
  changes.

## Patch Authority

This is a delegated patch-authorized adversarial review only inside the bounded
target:
- docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
- docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
- docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
- orca-harness/capture_spine/reddit_candidate_intake/validation.py
- orca-harness/capture_spine/reddit_candidate_intake/projection.py
- orca-harness/capture_spine/reddit_candidate_intake/__init__.py
- orca-harness/tests/unit/test_reddit_candidate_intake.py
- orca-harness/tests/contract/test_reddit_candidate_intake_contract.py

Everything else is read-only / flag-only.

Do not stage, commit, push, install dependencies, run live network access, run
browser/CloakBrowser/proxy tooling, or invoke Source Capture Armory runners.

If the correct fix requires changing a parent architecture decision, Source
Capture Armory, source_capture adapters, runner behavior, source-access
authorization, package dependencies, or product policy outside the target, do
not patch it. Flag it as off-scope.

If a design-level problem is found, return `NEEDS_ARCHITECTURE_PASS`, stop
patching, revert any partial diff, and report findings only. A partial patch
must not survive by inertia.

## Review Criteria

Review for material boundary failures first:
- Reddit `.json` URLs are refused for every Reddit input surface in this slice.
- Old Reddit listing/search HTML URLs are the only accepted Reddit HTML intake
  inputs for static projection.
- Thread pages are refused as intake input.
- Old Reddit thread URLs remain valid candidate thread outputs.
- Projection accepts static `html_text` only and never performs live fetches.
- Projection emits typed `CandidateThreadUrlRow` rows only.
- Raw HTML, parser output, raw Reddit payloads, screenshots, cookies, sessions,
  body text, selftext, comments, user names, author rows, profile URLs, or user
  metadata are not persisted or output.
- The code imports no HTTP, browser, CloakBrowser, proxy, Reddit API, archive,
  socket, webbrowser, or Source Capture Armory runtime modules.
- The lane does not emit Source Capture Packets, packet manifests, fixture
  admission records, ECR, Cleaning, Judgment, source-quality scoring, or Data
  Capture handoff claims.
- `source_surface` is enforced against the declared run-envelope allowlist.
- The cap uses `max_threads_per_subreddit` and cannot be treated as completion
  or sufficiency.
- Empty results and blocked/refused inputs remain honest outcomes.
- Related/cross-post/outbound surfaces are not extracted or traversed by this
  smallest slice unless the docs explicitly bind them as candidate-only,
  declared-and-capped future surfaces.
- Docs and code agree that transient projection is allowed, while raw
  HTML/parser-output persistence and parser/consolidation runner behavior are
  not allowed.
- Tests fail on `.json` input, thread-page input, raw HTML persistence,
  user/profile/body/comment leakage, undeclared source surfaces, and live-access
  imports.

Also check ordinary implementation quality where it affects the boundary:
- clear error codes;
- stable candidate-row shape;
- robust old Reddit URL canonicalization;
- no mutable default pitfalls;
- no false-positive acceptance of non-old-Reddit URLs;
- no test-only behavior that hides production failure;
- no broad package export that pulls capture/runtime dependencies.

## Output Contract

Write the full review report to:
- docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_v0.md

Report structure:
1. Commission, lane binding, and actor/model-family receipt.
2. Source context status.
3. Cynefin routing result.
4. Findings first, ordered by severity: critical, major, minor.
5. For each finding: location, issue, evidence, impact,
   minimum_closure_condition, next_authorized_action, and whether patched.
6. Unified diff for any target-file changes.
7. Per-change neutral source citations that are decision-sufficient in
   substance.
8. Controller verdict and residual-risk note.
9. Validation run status, including exact commands run or not run.
10. Off-scope flags.
11. CA adjudication packet.
12. Review-use boundary.

Controller output contract:
- invoke the selected review lanes; if unavailable, return
  `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch the affected lane;
- return findings plus any bounded unified diff;
- keep citation authority with the controller;
- keep citations neutral in tone and decision-sufficient in substance;
- return `NEEDS_ARCHITECTURE_PASS` for design-level problems, with no kept
  partial diff;
- do not commit, stage, or claim acceptance.

CA adjudication packet:
- state that the diff, citations, and verdict are claims to adjudicate, not
  premises to inherit;
- list each proposed change with its citation and intended closure condition;
- state whether each change is ready for Chief Architect accept / modify /
  reject adjudication;
- state any rejected/off-scope/design-level findings separately;
- do not claim a patch is kept, accepted, validated, or ready until the Chief
  Architect adjudicates it.

If you patch implementation or tests, run the narrowest relevant validation
available from `orca-harness`:
- python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py

If you patch docs only, run targeted readback plus the smallest relevant stale
language search for the changed claim. If no issues are found, say so clearly
and name residual risks/test gaps.

After writing the report, return a compact chat summary with:
- report path;
- whether patches were applied;
- changed files;
- validation evidence;
- verdict/recommendation;
- next action: Chief Architect adjudication if any diff was proposed.

Review-use boundary:
This delegated review-and-patch result is decision input only. The controller's
diff, citations, and verdict are claims to adjudicate, not premises to inherit.
It is not owner acceptance, validation proof, readiness, deployment,
source-access authorization, live Reddit authorization, Source Capture Armory
authorization, Data Capture handoff authorization, or permission to keep any
patch without Chief Architect adjudication.
````

## Prompt-Orchestrator Receipt

```yaml
prompt_orchestrator_receipt:
  requested_template_kind: review
  delegated_review_patch_overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  selected_review_lanes:
    - workflow-code-review
    - workflow-adversarial-artifact-review
  mode: base-subagent
  terminal_output_mode: orchestrated_prompt_saved_to_file
  output_mode: saved-artifact
  downstream_review_output_mode: review-report
  downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_v0.md
  actor_model_family_receipt_required: true
  actor_model_family_receipt_status: required_at_courier_runtime
  patch_authority: bounded target files only
  ca_adjudication_required_before_keep: true
  needs_architecture_pass_valve: true
  source_context_status: prompt_author_sources_loaded_for_prompt_creation
  validation_status: prompt_artifact_written_only; delegated_review_not_run
  non_claims:
    - review not run by this prompt artifact
    - delegated patch not applied or kept by this prompt artifact
    - no auto-keep; all delegated diffs require Chief Architect adjudication
    - no validation/readiness/acceptance claim
    - no live Reddit, CloakBrowser, proxy, or Source Capture Armory authorization
    - no Reddit .json intake authorization
    - no runtime model recommendation or model ranking
```
