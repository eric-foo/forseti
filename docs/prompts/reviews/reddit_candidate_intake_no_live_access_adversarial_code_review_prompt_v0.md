# Reddit Candidate Intake No-Live-Access Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated review-and-patch prompt
scope: De-correlated adversarial code review-and-patch commission for the no-live-access Reddit Candidate URL Intake implementation slice.
use_when:
  - Launching a delegated, de-correlated adversarial review-and-patch pass of the isolated Capture Spine Reddit Candidate URL Intake package after fused implementation.
  - Checking that the implementation enforces no-live-access, old-Reddit-first, candidate-row-only boundaries.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
input_hashes:
  models_py: A8A008E46D313D60A53C5921B62ED9D6BD04BAA983644031335B259F952F3572
  validation_py: 4E076C9E518545000A7AC92969127B5A13121DFF18193020E8648C8784D68789
  writer_py: 79E779CA275D79B69D528F25D168024D070A1959F127D3675F2E96BDE6A89A4A
  unit_test_py: 1AF2A46FB633B70BE00600473005200C89ACB7DE034507EF600B038D7EF719EB
  contract_test_py: C3881D61E8E270CC7FC065BE2D472D90C9F90F0A3C274249183F87E1176524A3
  pyproject_toml: 7F7AAAB7010BB426E1365DE9849660EFF7C36FC76F71097E898F856FBCA6C280
branch_or_commit:
  branch: ecr-sp3-timing-deriver-slice1
  head: 7d2d2310af3d72f70e326542515f2439932d52b7
stale_if:
  - Any target implementation or test file changes before review runs.
  - The Candidate URL Intake parent contract, Reddit architecture, or default-policy decision changes.
  - Orca review-lane or prompt-orchestration authority changes.
```

## Prompt Status

Status: `READY_FOR_DELEGATED_REVIEW_PATCH_PROMPT_WITH_RECEIPT_GATE`.

This prompt does not run the review. It does not validate, accept, stage,
commit, or claim implementation readiness.

This prompt is a rendered delegated review-and-patch commission, not a model
recommendation. The controller must be de-correlated from the author/home model
family, and the receiving lane must record the actor/model-family receipt before
review or patch work begins. If the receipt cannot prove de-correlation, the
run blocks before review.

## Launch Prompt

````text
You are the controller for a delegated adversarial code review-and-patch
commission for Orca.

This is a `workflow-delegated-review-patch` commission in `base-subagent` mode.
De-correlation is a who-constraint, not a model recommendation. Do not add a
Recommended model block, do not rank runtime models, and do not treat this
commission as runtime model routing.

## Actor / Model-Family Receipt Gate

Before reading implementation sources, complete this receipt with actual
operator/tooling facts:

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
not spawn recursive or unrelated subagents. If your runtime cannot apply
`workflow-code-review`, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the
reason and do not patch.

Review target:
- orca-harness/capture_spine/reddit_candidate_intake/
- orca-harness/tests/unit/test_reddit_candidate_intake.py
- orca-harness/tests/contract/test_reddit_candidate_intake_contract.py
- orca-harness/pyproject.toml only for `capture_spine` / `capture_spine.*` package discovery

Required durable review report path:
- docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_v0.md

Workspace:
- C:\Users\vmon7\Desktop\projects\orca

Pinned source state at prompt creation:
- branch: ecr-sp3-timing-deriver-slice1
- head: 7d2d2310af3d72f70e326542515f2439932d52b7
- target hashes are recorded in the prompt retrieval header.

Dirty-state allowance:
- The implementation target is newly added/untracked in this working tree.
- `orca-harness/pyproject.toml` is modified. Review only the `capture_spine` package-discovery addition for this target.
- An existing `cloakbrowser` optional-dependency diff may be present in `pyproject.toml`; treat it as out of scope for this review unless it directly corrupts `capture_spine` package discovery.
- Do not create, clone, request, or switch worktrees. Read the current working tree in place.

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

Then inspect only the target implementation and tests listed above, plus minimal adjacent packaging/test configuration needed to understand them.

Do not bulk-load unrelated source_capture adapters, Reddit consolidation, packet assembly, ECR, Cleaning, Judgment, source-quality, research corpus, `_inbox`, or historical review outputs unless a directly material issue in the target cannot be assessed without one narrow adjacent read.

## Source-Gated Method Contract

REFERENCE-LOAD:
- workflow-delegated-review-patch
- workflow-deep-thinking
- workflow-code-review

Do not APPLY these methods before source readiness. SOURCE-LOAD the required
sources and declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.

After source readiness, APPLY:
1. workflow-delegated-review-patch to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
2. workflow-deep-thinking to frame the boundary problem, fake-pass paths, and review criteria.
3. workflow-code-review to produce findings.

If `workflow-code-review` is unavailable, unresolved, or cannot be applied
after source readiness, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` with the
reason and do not emit strict review claims. Do not silently emulate the review
lane inline.

## Cynefin Routing

Run Orca Cynefin routing before review.

Expected routing:
- Smallest complete outcome: review the no-live-access implementation slice for boundary enforcement and fake-pass risks.
- Regime: complicated.
- Decomposition: risk-first code review over a small source slice.
- Current bottleneck: proving the local package did not smuggle in live access, Armory capture, packet-shaped output, same-run traversal, or broader source_capture coupling.
- Riskiest assumption: tests pass because labels are present rather than because forbidden behaviors are mechanically impossible or refused.
- Stop or pivot condition: if the implementation belongs in Source Capture Armory, requires live Reddit/CloakBrowser/proxy execution to be meaningful, or exposes a design-level problem rather than a patch-level defect, return `NEEDS_ARCHITECTURE_PASS`, leave no kept partial diff, and return findings only.
- Allowed next move: review and, if explicitly useful, patch only the target files.
- Disallowed next move: live Reddit access, CloakBrowser/proxy invocation, Source Capture Packet generation, broad crawler behavior, ECR/Cleaning/Judgment/source-quality work, or unrelated pyproject dependency changes.

## Patch Authority

This is a delegated patch-authorized adversarial review only inside the bounded
target:
- orca-harness/capture_spine/reddit_candidate_intake/**
- orca-harness/tests/unit/test_reddit_candidate_intake.py
- orca-harness/tests/contract/test_reddit_candidate_intake_contract.py
- orca-harness/pyproject.toml only for package discovery lines required by `capture_spine`

Everything else is read-only / flag-only.

Do not stage, commit, push, install dependencies, run live network access, run browser/CloakBrowser/proxy tooling, or invoke Source Capture Armory runners.

If the correct fix requires changing a parent architecture doc, Source Capture
Armory, source_capture adapters, runner behavior, source-access authorization,
or product policy, do not patch it. Flag it as off-scope.

If a design-level problem is found, return `NEEDS_ARCHITECTURE_PASS`, stop
patching, revert any partial diff, and report findings only. A partial patch
must not survive by inertia.

## Review Criteria

Review for material boundary failures first:
- no live Reddit, HTTP, browser, CloakBrowser, proxy, Reddit API, archive, parser, socket, or webbrowser imports;
- no dependency on `source_capture` or Source Capture Armory components;
- no Source Capture Packet writer, packet manifest, packet lifecycle state, or packet-shaped output;
- no body/comment/profile/raw HTML/screenshot/session/cookie/secret output fields;
- old Reddit thread/listing URL shapes are default-valid;
- new Reddit URLs are non-default and refused or require a later explicit amendment;
- run envelope requires declared topic/query or seed, caps, stop condition, `cap_type`, and `coverage_claim`;
- `coverage_claim` cannot mismatch `cap_type`;
- `caps_reached` is not represented as completion or sufficiency;
- `empty_result` and `blocked_result` can remain valid terminal outcomes;
- related/cross-post candidates cannot authorize same-run traversal;
- outbound rows require separate source-family intake and are not fetched;
- promotion receipt requires known limitations and `capture_not_yet_authorized: yes`;
- local writer emits candidate rows and provenance only;
- tests would fail on forbidden fields, live-access imports, same-run traversal, new Reddit defaulting, and promotion authorization leakage.

Also check ordinary implementation quality where it affects the boundary:
- clear error codes;
- stable JSON shape;
- no mutable default pitfalls;
- no false-positive regex acceptance of non-old-Reddit URLs;
- no test-only behavior that hides production failure;
- no broad package export that pulls capture/runtime dependencies.

## Output Contract

Write the full review report to:
- docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_v0.md

Report structure:
1. Commission, lane binding, and actor/model-family receipt.
2. Source context status.
3. Cynefin routing result.
4. Findings first, ordered by severity: critical, major, minor.
5. For each finding: location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and whether patched.
6. Unified diff for any target-file changes.
7. Per-change neutral source citations that are decision-sufficient in substance.
8. Controller verdict and residual-risk note.
9. Validation run status, including exact commands run or not run.
10. Off-scope flags.
11. CA adjudication packet.
12. Review-use boundary.

Controller output contract:
- invoke `workflow-code-review`; if unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch;
- return findings plus any bounded unified diff;
- keep citation authority with the controller;
- keep citations neutral in tone and decision-sufficient in substance;
- return `NEEDS_ARCHITECTURE_PASS` for design-level problems, with no kept partial diff;
- do not commit, stage, or claim acceptance.

CA adjudication packet:
- state that the diff, citations, and verdict are claims to adjudicate, not premises to inherit;
- list each proposed change with its citation and intended closure condition;
- state whether each change is ready for Chief Architect accept / modify / reject adjudication;
- state any rejected/off-scope/design-level findings separately;
- do not claim a patch is kept, accepted, validated, or ready until the Chief Architect adjudicates it.

If you patch, run the narrowest relevant validation available, normally:
- python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py

If no issues are found, say so clearly and name residual risks/test gaps.

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
authorization, or permission to keep any patch without Chief Architect
adjudication.
````

## Prompt-Orchestrator Receipt

```yaml
prompt_orchestrator_receipt:
  requested_template_kind: review
  delegated_review_patch_overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  selected_review_lane: workflow-code-review
  mode: base-subagent
  terminal_output_mode: orchestrated_prompt_saved_to_file
  output_mode: saved-artifact
  downstream_review_output_mode: review-report
  downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_v0.md
  actor_model_family_receipt_required: true
  actor_model_family_receipt_status: required_at_courier_runtime
  patch_authority: bounded target files only
  ca_adjudication_required_before_keep: true
  needs_architecture_pass_valve: true
  non_claims:
    - review not run by this prompt artifact
    - delegated patch not applied or kept by this prompt artifact
    - no auto-keep; all delegated diffs require Chief Architect adjudication
    - no validation/readiness/acceptance claim
    - no live Reddit, CloakBrowser, proxy, or Source Capture Armory authorization
    - no runtime model recommendation or model ranking
```
