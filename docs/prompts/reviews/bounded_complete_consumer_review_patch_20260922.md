# Bounded complete-case consumer review and patch courier

```yaml
retrieval_header_version: 1
artifact_role: Review scope packet for an exact-commit operator courier
scope: Consumer persistence, exact membership, identity attribution, and bounded delivery.
use_when:
  - Commissioning the independent review of the bounded complete-case consumer.
authority_boundary: retrieval_only
```

Review and patch only the named implementation boundary below. Done means
source-backed findings and a minimal bounded patch, if needed, with the named
tests run and remaining uncertainties explicit. Do not turn historical sizing
or synthetic quality evidence into current Summer Fridays readiness.

```yaml
delivery: operator_courier_only
target_kind: delegated_code_review_and_patch
access: repo
delegate_eligibility: different_vendor_lineage_with_direct_repo_access
worktree: C:/Users/vmon7/.codex/worktrees/sf-bounded-consumer/forseti
branch: codex/bounded-complete-consumer
diff_base: a9384f6aa323f1d703cd82eca5d7bc8c20115c47
revision_mode: exact
output_mode: file-write
edit_permission: bounded_implementation_authorized
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md
environment_baseline: >
  Windows host, PowerShell-first: use PowerShell syntax for shell/test commands;
  use absolute paths resolvable from any cwd; invoke python, never python3;
  do not pass Windows drive-letter paths or heredocs through bash.
lifecycle_hard_stop: >
  A delegate or receiver does not commit, push, open or update a PR, merge,
  stash, reset, clean the worktree, or run repository-hygiene actions unless
  the commission explicitly grants that action.
decorrelation_commission: >
  delivery: operator_courier_only; access: repo;
  delegate_eligibility: different_vendor_lineage_with_direct_repo_access;
  same-vendor, unknown-lineage, no-repo, self, and Codex-managed controller
  substitutes are invalid; a manager-prefixed target path is neutral;
  if no eligible controller is available the prompt remains unexecuted.
```

This scope packet is consumed only with the accompanying operator courier's
exact `required_revision` and single `receiver_binding`. That commit must contain
this packet and the implementation. The courier remains preparation-only until
an eligible external receiver binds; neither this file nor its historical raw
hashes substitutes for the immutable commit. Do not infer a pin from mutable HEAD.

Before source loading, verify the target, branch, exact commit, clean worktree,
different-vendor lineage, direct write capability and absence of another writer
in one combined intake; then inspect the actual named diff by the second tool
call. Only receiver-owned commissioned edits may be dirty afterward. Stop on a
mismatch. The author supplies the frozen commit in the transport after the last
authoring edit; the receiver cannot commit, publish, push or merge. Required CI,
returned review and home-actor adjudication remain separate landing conditions.

Patchable targets and historical validated raw-file SHA256 (the courier's commit
pin is authoritative; Git checkout line-ending conversion may change raw hashes):

- `forseti-harness/judgment/complete_case_consumer.py`:
  `44edd5bbfa920459781b8a431dc01983d2960665a24a28ee6170f0f712c4edaa`
- `forseti-harness/runners/run_semantic_evidence_integration.py`:
  `d9d00c965386c801381534080211981355c760aecbf0a6575b549bd8f1d134a3`
- `forseti-harness/tests/unit/test_complete_case_consumer.py`:
  `4393941acd7fae6034827f5d73813698a41951e419b5b9fd6e53a9ca7d18b99a`
- `forseti-harness/judgment/verified_evidence_selection.py`:
  `02abf596454c1fb4a0cb68cc468cc901c71710c64ff8bbf0e6e01cbc683f68fd`
- `forseti-harness/tests/unit/test_verified_evidence_selection.py`:
  `3a2d69be0752f9c17ef9080b9cd2c4d57933052e3a8420ca3cb1d13ff6a610dc`
- `forseti-harness/judgment/semantic_evidence_integration.py`:
  `42c72ad83723a0aeca8d25cba3cf36135e17bc6a7897e3ffe20c7b991031af04`

Read-only supporting authored documents:

- `forseti/product/spines/judgment/claim_support/forseti_semantic_evidence_integration_contract_v0.md`
  — **Bounded complete-case answer and review** and **Supported completion**.
- `docs/workflows/phase_a_customer_evidence_completion_path_v0.md`
  — **Supported operating route** and **Before changing Phase A evidence machinery**.
- `docs/research/summer_fridays_complete_comparison_20260922/consumer_implementation.md`
  — bound success contract, exact test/evidence locations, and limitations.

The carried review scope remains consumer persistence and supported restart /
recovery. The earlier response-before-receipt interruption now has an injected
failure and successful recovery test; partial staging is explicitly rejected.
The parent fresh-process proof also exposed JSON ordering that reissued identical
judgments; the patch canonicalizes object transport and revalidates old ordering
variants against exact context, schema, capacity and expanded evidence. Review
that concrete recovery boundary, including conflicting saved judgments and the
immutable validated complete/selected start. Also review the concrete large-intake
failure found by the parent: pre-capture bounded chunk retrieval now checks exact
job identity, byte offsets, individual chunk and full-section hashes before any
completion marker. Keep existing small/default intake and native replay exact.
Check that exact correction and
recheck resume preserve their original/accepted artifacts. Do not claim the old
interruption scenario remains untested or expand into general model quality.
Concurrent writers are not a separately commissioned capability. Bounded patch
authority is granted only for the six named code/test files; all other targets
remain read-only.

Invoke `workflow-code-review` under `.agents/workflow-overlay/review-lanes.md`.
Read `AGENTS.md`, the overlay README, applicable validation/safety rules, and the
claim-support contract before evidence judgments. This is the receiver executing
an externally authored courier; it does not authorize the author to dispatch its
own reviewer. Unknown lineage, same-vendor lineage, and no direct repo access are
ineligible. Do not substitute self-review or another controller. If the required
review lane is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`.

Preserve the supported normal policy-v2 consolidation route, existing finite
replay, original inputs/accepted response bytes, complete exact inventory,
legitimate repeated citations versus duplicate results, role-owned opposition,
known repeated/distinct identities and unknown identity, reasoned unused/no-action
evidence, and explicit failures for oversized rows/aggregate requests/output.
Trace scoped invalidation, lost/corrupt accepted artifacts, and submission identity
only as they affect that publication/recovery boundary and exact restart reuse. Preserve measured actor
delivery and source-origin attribution while patching. Do not add
a retrieval system, registry, new consolidation pipeline, universal review gate,
or acquisition. No provider jobs are authorized. Off-target sources remain
read-only; return `NEEDS_ARCHITECTURE_PASS` for a required design change rather
than patching beyond scope. Stop patching and revert only your own partial edits
for that design change; leave the authored implementation intact.

Run from `forseti-harness/`:

```text
python -X utf8 -m pytest tests/unit/test_complete_case_consumer.py tests/unit/test_verified_evidence_selection.py tests/unit/test_review_evidence.py -q
python -X utf8 -m pytest tests/contract/test_data_lake_inventory_gate.py tests/contract/test_policy_module_version_pins.py tests/unit/test_semantic_evidence_integration.py -k "advance or judgment_job or judgment_worker or route_1_6_multisource_dogfood or policy_module or inventory" -q
```

Apply `.agents/workflow-overlay/validation-gates.md` -> **Document-pinned
projection falsifier** to affected identity, compatibility or proof pins in the
implementation report. At immutable `reviewed_revision`, rebuild affected current
public-path, legacy-reuse and complete-delivery fixtures from their saved bound
inputs and compare their pinned semantics; retain historical sizing/quality pins
as historical observations. If your patch changes their producing bytes, rerun
once after patches settle and identify that result as working-tree evidence tied
to the diff. Missing saved inputs/tools is `not-run` and withholds only the
particular dependent proof or compatibility claim.

Run `git diff --check` at the repository root. A failure remains visible; do not
weaken expectations or repair source fixtures to produce a pass. Broaden only
for a concrete affected boundary. Return your actual `delegate_vendor`, findings
and considered/defended candidates, citations for every change, exact modified
paths, test outcomes, diff, and residuals. No acceptance/readiness claim follows
from a returned patch. The home actor adjudicates every change using
`.agents/workflow-overlay/delegated-review-patch.md` — **Adjudication closeout**
and its same-turn material-continuation rule — before any change is kept.
