# Shared Social Heartbeat — Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Commission a source-backed, read-only adversarial code review of the pinned
  shared Instagram/TikTok daily heartbeat implementation commit.
use_when:
  - Reviewing implementation commit 30f73db09d5d4bd87a698b47c12341401b055d1a before acceptance or landing.
authority_boundary: retrieval_only
```

## Commission

```yaml
output_mode: review-report
template_kind: repo-code-review
template_binding: >
  The project registry leaves repo-code-review unbound by default; this lane is
  explicitly implementation-authorized and uses workflow-code-review under the
  code-diff target contract in delegated-review-patch.md.
access: repo
review_mode: read-only code; docs-write only for the bound report
report_destination: docs/review-outputs/shared_social_heartbeat_adversarial_code_review_v0.md
workspace: C:\tmp\orca-shared-heartbeat
branch: codex/shared-social-heartbeat-core
target_revision: 30f73db09d5d4bd87a698b47c12341401b055d1a
base_revision: b10010bdfcda38d2ed50e4ec0812666ea2abb630
revision_semantics: exact target commit and exact base-to-target diff
dirty_state_allowance: >
  clean at source-read start; the only later write allowed is the bound review report
receiver_mechanism: >
  worktree-rooted repo reviewer; before source loading, the operator must verify
  that the receiver's actual read/write root is C:\tmp\orca-shared-heartbeat
receiver_write_root_verification: operator_to_fill_before_dispatch
authored_by: OpenAI GPT-5 Codex
reviewed_by: operator_to_fill; record unrecorded in the report if not supplied
author_vendor: OpenAI
delegate_vendor: >
  operator_to_fill; must differ from OpenAI to satisfy the commissioned
  cross-vendor discovery bar, otherwise report same-vendor sanity only
runtime_model_routing: none; this prompt does not select, rank, or recommend a model
patch_authority: none
doctrine_change_decision: no; review of an implementation diff, not doctrine authoring
repo_map_decision: loaded
repo_map_reason: >
  the Data Capture submap routes shared heartbeat control through the platform
  source-family indexes and operator runbook
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable
```

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: >
    exact base-to-target shared heartbeat implementation diff; code and tests
    read-only, with one review-report write at the bound destination
  dirty_state_checked: yes
  blocked_if_missing: >
    exact target commit, clean source-read start, actual receiver root,
    required method instructions, decisive authority sources, or report write capability
```

Preflight constants: `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` v0.
External workflow sources are read-only; `jb` is not Forseti authority.

## What this is for

**Goal:** determine whether the pinned implementation gives Instagram and
TikTok one truthful, shared daily heartbeat control plane without weakening the
existing Instagram lane or inventing TikTok success.

**Done looks like:** the review attacks the shared/core boundary and all
failure-sensitive paths, reports every issue with source evidence, reruns the
bound tests, and leaves the Chief Architect enough information to accept,
patch, or reject the implementation without reconstructing this authoring chat.

This goal is the executor target and review axis to attack, not a pass-if-matches bar.

## Hard boundaries

- Review only `b10010bdfcda38d2ed50e4ec0812666ea2abb630..30f73db09d5d4bd87a698b47c12341401b055d1a`.
- Do not edit implementation, tests, inventory, policies, READMEs, prompts, or
  any file except the bound review report.
- Do not commit, push, open/update a PR, merge, stash, reset, clean a worktree,
  run repository hygiene, launch live capture, write a live Data Lake, mutate
  Creator Registry, or run Silver/Gold/Judgment.
- Findings outside the pinned diff may be mentioned only when the diff newly
  exposes or materially worsens them. Do not widen into platform redesign.
- If a material finding requires architecture rather than a bounded patch,
  return `NEEDS_ARCHITECTURE_PASS`; do not prescribe an implementation by inertia.

## Required method and source sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review`. Do not
   APPLY either method yet; use them only to prepare a neutral read lens.
3. SOURCE-LOAD the exact diff and decisive sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, naming every
   missing, conflicting, excluded, or unexpectedly modified source.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame the
   boundary problem and failure modes, then APPLY `workflow-code-review` to the
   pinned implementation.
6. Write the report, run the report provenance gate, and return the compact
   review courier summary. If either method is unavailable, return advisory-only
   or blocked; do not emit a formal verdict.

## Decisive source pack

Read fully unless the file's own targeted-read rule binds a narrower section:

- exact diff and every changed production/test file in the pinned commit;
- `docs/workflows/tiktok_daily_heartbeat_architecture_planning_handoff_v0.md`;
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`;
- `forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md`;
- `forseti-harness/docs/adapter_author_contract.md`;
- `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`;
- `.agents/workflow-overlay/review-lanes.md`, targeted to code-review authority;
- `.agents/workflow-overlay/communication-style.md`, targeted to Review
  Adjudication Next Step and review courier shape;
- `.agents/workflow-overlay/validation-gates.md`, targeted to review-report and
  code-lane gates.

For each source, record `full`, `targeted <section>`, `grep <token>`, or
`skip: <reason>` before the heavy read. Expand whenever a source could change a
finding, non-finding, verdict, or blocker. The budget is an economy aid, not a
reason to under-read material evidence.

## Named implementation target

The exact target is the whole base-to-target diff, including:

- shared core: `forseti-harness/source_capture/social_heartbeat_run_control.py`;
- Instagram adapter/control/operator changes under `forseti-harness/runners/run_source_capture_ig_daily_heartbeat*.py`;
- TikTok runner/control/operator additions under `forseti-harness/runners/run_source_capture_tiktok_daily_heartbeat*.py`;
- TikTok grid public seam and attempt-lineage changes in
  `source_capture/tiktok/creator_onboarding.py` and `grid_packet.py`;
- browser safety-stop changes in `source_capture/adapters/browser_snapshot.py`;
- Data Lake inventory registration and generated inventory;
- all paired unit and contract tests in the commit;
- operator runbook and source-family routing updates in the commit.

No file in that set is patchable in this review.

## Decision criteria to attack

Review coverage-first. In particular, try to falsify all of these:

1. The core is platform-neutral mechanics rather than Instagram policy renamed.
2. Instagram retains its public CLI/plan namespace and observable behavior while
   using the shared partition, attempt, receipt, and recovery contract.
3. TikTok is genuinely grid-only: no suggested-account discovery, top-video
   selection, deep capture, comments, subtitles, Silver, or scheduler ownership.
4. The frozen daily plan requires an explicit active/daily TikTok roster and a
   stable `platform_account_id`; no Creator Registry mutation or implicit
   activation occurs.
5. The shared core owns canonical bucket/lane selection and prevents duplicate
   terminal attempts; `succeeded` cannot be retried.
6. Receipt cardinality and identity are strict: missing, duplicate, unmatched,
   unknown-status, or attempt-mismatched receipts cannot yield success.
7. A successful attempt means a verified packet whose manifest
   `session_identity` matches the stable attempt ID and whose preserved bytes
   verify; operator exit codes cannot hide receipt-contract failure.
8. Crash recovery never silently recaptures: committed packets reconcile by
   attempt identity; TikTok frozen windows can resume admission; absence of both
   packet and reusable artifact fails visibly.
9. Budget deferrals and platform-context stops remain distinct from attempted
   failures; an unvisited creator is not falsely marked started.
10. Account-safety and unresolved challenge stops suppress pointer actions and
    lazy scrolling in both relevant browser backends.
11. File locks, plan writes, attempt appends, session receipt isolation, and
    ownership-checked unlock behavior are safe under duplicate/concurrent operator runs.
12. Data Lake inventory and operator docs state only what the implementation
    proves, including the unbound numeric-account identity residual.
13. Tests exercise the actual contracts rather than mocking away the risky seam.

## Accepted residuals to challenge, not silently inherit

The author currently accepts these as bounded residuals. Find if any is actually
a material defect for this slice:

- YouTube is not implemented here; a future RSS adapter may consume the core.
- No standing scheduler/service or database-backed control state exists.
- Real multi-creator TikTok throughput, account safety, and 2,500-creator scale
  remain unproven.
- Data-root crash recovery scans raw manifests by `session_identity`; it does
  not override packet-writer ownership of packet IDs.
- TikTok plan identity is stable by numeric account ID, but served grid evidence
  verifies the public handle/video relation rather than the numeric account ID;
  stale roster handle binding remains explicitly unbound.
- A crash before any verified packet or reusable frozen artifact requires an
  explicit retry and may recapture; it is not mislabeled recovery.
- Bucket-scoped lease concurrency and sparse bounded-window observation semantics
  are inherited, not redesigned.
- No live platform or live-lake run is evidence in this change.

## Validation

Run from `C:\tmp\orca-shared-heartbeat\forseti-harness` with the repository's
PowerShell environment baseline:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q `
  tests/unit/test_social_heartbeat_run_control.py `
  tests/unit/test_ig_daily_heartbeat_runner.py `
  tests/unit/test_ig_daily_heartbeat_control.py `
  tests/unit/test_tiktok_daily_heartbeat.py `
  tests/unit/test_tiktok_grid_packet.py `
  tests/unit/test_tiktok_creator_onboarding.py `
  tests/unit/test_source_capture_browser_snapshot.py
python -m pytest -p no:cacheprovider -q tests/contract
python runners/run_source_capture_ig_daily_heartbeat_control.py --help
python runners/run_source_capture_ig_daily_heartbeat_operator.py --help
python runners/run_source_capture_tiktok_daily_heartbeat.py --help
python runners/run_source_capture_tiktok_daily_heartbeat_operator.py --help
```

From the repository root, also run:

```powershell
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/header_index.py --strict
python .agents/hooks/check_repo_map_freshness.py --strict
python .agents/hooks/check_dcp_receipt.py --strict
python .agents/hooks/check_review_output_provenance.py --strict `
  docs/review-outputs/shared_social_heartbeat_adversarial_code_review_v0.md
git diff --check b10010bdfcda38d2ed50e4ec0812666ea2abb630..30f73db09d5d4bd87a698b47c12341401b055d1a
```

Report each command with cwd, exit code, and observed result. A failed or not-run
check stays visible and prevents an unqualified formal verdict.

## Required report shape

Write the durable report to the bound destination. Record `reviewed_by` and
`authored_by`; use `unrecorded` rather than guessing.

List findings first, ordered `critical`, `major`, `minor`. For every finding include:

- severity and confidence (`high`, `medium`, `low`);
- exact file/line location;
- issue, neutral evidence, and impact;
- `minimum_closure_condition` as an end state, not implementation instructions;
- `next_authorized_action` within this read-only commission;
- advisory remediation direction, clearly non-executable.

Report every issue found; do not filter low-confidence or minor findings.
Include `considered_and_defended` for steelman-defeated candidates. Then include:

- formal review verdict: `PASS`, `PASS_WITH_FINDINGS`, or `BLOCKED` (review
  judgment only; never readiness, approval, merge authority, or live proof);
- validation evidence;
- residual risks and not-proven boundaries;
- one-line read-budget audit;
- whether the cross-vendor discovery bar was actually satisfied.

Do not include a patch queue or edit instructions. The Chief Architect must
adjudicate findings, verdict, validation, and residuals as claims before keeping
anything. After adjudication, close any self-closable material issue in the same
turn; otherwise route the smallest complete closure step. Once material issues
are clear, batch commit/push/PR/merge into exactly one land step, then assess
material next moves only against a visible active goal. Do not invent a roadmap
when none exists.

If the report write fails, return a failed blocked courier with
`review_location: chat_only_current_thread`, no `report_path`, and the failed
destination. If report provenance validation fails, the report is not finalized.

## Non-claims

This commission is not implementation acceptance, validation, production
readiness, live capture authorization, a scale proof, a Silver/Gold/Judgment
claim, runtime-model routing, patch authority, or merge authority.
