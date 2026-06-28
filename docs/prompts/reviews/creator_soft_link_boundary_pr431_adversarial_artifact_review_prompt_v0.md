# Creator Soft-Link Boundary PR431 Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Filed prompt for a read-only adversarial artifact review of PR #431's
  channel-neutral creator soft-link boundary patch.
use_when:
  - Dispatching an adversarial reviewer to inspect PR #431 before CA adjudication.
  - Checking whether the soft-link candidate boundary, profile subject split,
    and IG roster ID separation preserve Orca's identity and rollup boundaries.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
stale_if:
  - PR #431 is rebased, amended, merged, or closed before review.
  - Any target file hash below no longer matches the checked-out tree.
  - The delegated review-and-patch or adversarial artifact review overlay changes.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Prompt Preflight Deltas

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_creator_soft_link_boundary_pr431_review
  edit_permission: read-only review; report write only at named destination
  target_scope: PR #431 creator soft-link boundary docs patch
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/delegated-review-patch.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - target files listed below
authorization_basis: >
  Current owner invoked workflow-delegated-review-patch after PR #431 was filed.
  Orca delegated review-and-patch is provisional and single-target; because this
  is a multi-file docs/spec PR, this prompt routes to read-only adversarial
  artifact review instead of pretending patch execution is bound.
objective: >
  Stress-test whether PR #431 correctly makes similar accounts soft-linked for
  human review without treating candidates as final creator identity or
  cross-platform rollup authority.
intended_decision: >
  Decide what the CA should accept, patch, or reject before promoting or relying
  on the soft-link boundary patch.
target_files_or_dirs:
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_v0.md
edit_permission: read-only for source files; write-only for the review report destination
dirty_state_allowance: >
  The reviewer must verify the branch, HEAD, and status. Target files should
  match the pinned hashes below. If they do not, return SOURCE_CONTEXT_INCOMPLETE
  or BLOCKED_SOURCE_MISMATCH unless the CA supplies a new target revision.
controlling_source_state: >
  Overlay and prompt sources were read by the dispatcher. The reviewer must
  fresh-read them in the target worktree before strict review claims.
branch_or_commit_reference:
  branch: codex/channel-neutral-creator-identity-architecture-prompt-pr412
  head: d4343f8ab61a23fd981141ed516e35ddba3f891a
  base: f7d8de6381d0ec0b9ef926cd275127830a7f6036
  pr_url: https://github.com/eric-foo/orca/pull/431
doctrine_change_decision: >
  This prompt does not change product or architecture doctrine. It reviews a
  doctrine-bearing PR. Any needed source change is outside this read-only prompt
  and must return as a finding for CA adjudication or a later bounded patch lane.
isolation_decision: >
  Existing PR branch/worktree. Do not create another worktree unless the
  operator chooses to run the review elsewhere.
validation_gates:
  - The review prompt itself is filed under docs/prompts/reviews/.
  - Reviewer must write the durable report before returning completed YAML.
  - If the reviewer cannot write the report, return status failed with no report_path.
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
```

## Paste-Ready Review Prompt

````markdown
You are performing an adversarial artifact review for Orca.

This prompt was produced as the overlay-correct route-out from an invoked
delegated review-and-patch request. Important boundary: Orca's delegated
review-and-patch convention is provisional and single-target. PR #431 is a
multi-file docs/spec patch, so this commission is read-only adversarial artifact
review. Do not patch source files. Return findings and advisory remediation
direction for CA adjudication.

Do not recommend, rank, prescribe, or imply runtime model choice. If the operator
has intentionally launched you as a de-correlated reviewer, record the observed
provenance fields in the review report:

- authored_by: OpenAI/Codex family; exact model/version unrecorded unless the
  operator supplies it.
- reviewed_by: operator/tooling supplied; use unrecorded if not supplied.
- de_correlation_bar: cross_vendor_discovery, same_vendor_sanity, or self_fallback.
- controller_model_family: operator/tooling supplied or unrecorded.

These fields are provenance only. They are not runtime-model routing and not a
quality recommendation.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-ledger-static-fixture-clean`

Expected branch:
`codex/channel-neutral-creator-identity-architecture-prompt-pr412`

Expected HEAD:
`d4343f8ab61a23fd981141ed516e35ddba3f891a`

PR:
`https://github.com/eric-foo/orca/pull/431`

Prompt source:
`docs/prompts/reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_prompt_v0.md`

Report destination:
`docs/review-outputs/adversarial-artifact-reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_v0.md`

Review purpose:
Adversarially review whether PR #431 correctly implements the owner decision
that very similar accounts should be soft-linked before human review, while
preserving the hard boundary that a soft link is only a reversible candidate
edge/evidence bundle, not a final creator identity, real-world identity claim,
cross-platform rollup authority, outreach authority, or public person-level
surface.

Fitness reference:
The patch succeeds only if a future operator can open one current profile for an
observed account or linked creator/account cluster, move seamlessly from
candidate to reviewed linkage, and still know which facts are account-scoped,
which are creator-cluster-scoped, and which claims remain forbidden. The review
should attack whether that goal and signal are sufficient; do not treat them as
a pass-if-matches bar.

Required method sequence:
1. Read this prompt.
2. Read `AGENTS.md`.
3. Read `.agents/workflow-overlay/README.md`.
4. REFERENCE-LOAD these method/contract sources. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
5. SOURCE-LOAD the task sources below from the repository.
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If incomplete,
   name the missing source and stop unless the missing source cannot change any
   finding.
7. After source context is ready, APPLY `workflow-deep-thinking` to frame the
   boundary problem, failure modes, and decision criteria.
8. Then APPLY `workflow-adversarial-artifact-review` to the loaded target.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only
result. Do not emit formal strict review claims.

Required source context:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`
- `orca-harness/tests/unit/test_creator_public_handle_linkage.py`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

Optional targeted reads when material to a finding:

- `docs/decisions/wind_caller_calibration_carveout_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md`
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/orca_repo_map_v0.md`

Do not bulk-load all prompts, all review outputs, all product docs, all research
corpus, all proof packets, or method-validation replays.

Pinned target hashes at dispatch:

```yaml
target_hashes:
  creator_profile_current_view_spec_v0.md: 815769909F069B0405E5B14562477802CD2DAD6F79E5F7C4A57A1321E67D23AF
  creator_public_handle_linkage_ledger_spec_v0.md: 23ADCB0E6E56AAE17FEB7AF0D72EFC5BA40B2BBED02DCC02462BC685452323A1
  ig_creator_roster_frontier_ledger_spec_v0.md: 0693559FD0EEA3F8B338F387B9163D622288DF2670275697B8DF3EFE8F8D0180
  youtube_creator_observation_ledger_spec_v0.md: 457A6EF5F0AD3861FD1A9781CBBF0FC235113D590FE21956BBA900352B967B4A
  creator_intelligence_profile_surface_v0.md: 5E462277DCCF090661DEE1BBF33C4E192E17A300443723162CFB47236C14F17A
```

Review target:

- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

Read-only context:

- Every other file. Flag issues outside the target list; do not patch.

Review questions:

1. Does the patch make candidate soft links seamless after human review without
   allowing a candidate to masquerade as final identity?
2. Does `candidate_public_account_link` always require `candidate_needs_review`,
   and do final/probable/declared links still require human/non-LLM evidence?
3. Does `creator_profile_current` correctly support `platform_account` subjects
   before linkage and `creator_record` subjects only after evidence spans at
   least two platforms?
4. Are account-primary metric observations and account rollups separated from
   creator-cluster rollups clearly enough to prevent accidental cross-platform
   summing before review?
5. Does the Creator Signal surface label account-scoped and linked-cluster
   profiles honestly for operators and buyers?
6. Does the IG roster doc now avoid overloading its local roster ID with the
   public-handle linkage ledger `creator_record_id`?
7. Does any wording accidentally authorize real-world identity proof, public
   person-level directory behavior, outreach/contact enrichment, source access,
   live capture, SQLite migration, dashboard implementation, buyer proof,
   readiness, or validation?
8. Is the existing validator/documented validator contract sufficient for the
   new soft-link semantics, or does the docs patch claim runtime enforcement that
   the code does not provide?
9. Is there a stale or conflicting use of `creator_record_id`, `platform_account`,
   `profile_subject_kind`, `identity_state`, `candidate_needs_review`, or
   `candidate_public_account_link` that would mislead a future implementation?
10. Is there a design-level defect that should return to architecture planning
    rather than receive a local wording patch?

Review output contract:

Write the full human-readable review report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_v0.md`

The report must include:

- source context status;
- deep-thinking risk frame before findings;
- findings first, ordered by `critical`, `major`, `minor`;
- for each finding: severity, location, issue, evidence, impact,
  minimum_closure_condition, next_authorized_action, and recommended correction
  or advisory remediation direction;
- explicit non-findings for the main review questions that survive inspection;
- validation or static checks run, or explicit not-run reasons;
- residual risk;
- provenance fields: `reviewed_by`, `authored_by`, `de_correlation_bar`, and
  `controller_model_family`;
- recommendation: `accept`, `accept_with_friction`, `patch_before_acceptance`,
  `reject`, or `blocked`.

Do not include `patch_queue_entry`. Do not stage, commit, push, open a PR,
install packages, run live capture, call external services, migrate to SQLite,
or edit source files.

After the report is written, return only this courier summary in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: unrecorded
  authored_by: OpenAI/Codex family, exact model unrecorded
  summary: "<one sentence>"
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "<one concrete next step for CA adjudication>"
```

If the report cannot be written, return the same shape with:

- `status: failed`
- `review_location: chat_only_current_thread`
- `recommendation: blocked`
- no `report_path`

Review-use boundary:
This review is decision input only. It is not approval, validation, readiness,
mandatory remediation, product proof, executor-ready patch authority, source
promotion, or permission to merge PR #431. The commissioning CA decides what is
kept and may accept, modify, or reject any recommendation.
````
