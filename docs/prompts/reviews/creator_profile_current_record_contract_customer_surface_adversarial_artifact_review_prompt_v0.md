# Creator Profile Current Record Contract Customer Surface Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Read-only adversarial artifact review prompt for PR #633's
  creator_profile_current record contract, focused on whether a customer-facing
  creator profile can use progressive disclosure for limitations, non_claims,
  and source_drill_back without hiding material caveats.
use_when:
  - Commissioning an independent review of the clean-customer-surface strategy for creator_profile_current.
  - Checking whether the record contract safely supports a simple primary customer UI backed by accessible evidence and caveats.
authority_boundary: retrieval_only
pr: https://github.com/eric-foo/orca/pull/633
branch_or_commit_before_prompt: codex/creator-profile-record-contract @ 5031ecac795bf95fc7a6344cd9ce6b3e30f60d5f
base_commit_before_prompt: e53f03cbbf3308a180cb9e22a967f1bccc9e74c4
review_target: orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
review_target_sha256_before_prompt: B540E3A211790A5F7182F2C5AFBF6B67B098FF0D23BBAF4F83E124F7C55EED86
intended_report_path: docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_record_contract_customer_surface_adversarial_artifact_review_v0.md
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/product-proof.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - PR #633 changes the review target after the target hash above.
  - creator_profile_current_record_contract_v0.md changes Section 1, Section 2, Section 3, Accepted Residuals, or Non-Claims.
  - Creator Signal profile surface policy changes customer-facing claim, limitation, missingness, freshness, or source-drill-back rules.
  - Orca review-lane, prompt-orchestration, delegated-review-patch, or product-proof authority changes before review.
```

## Orca Prompt Preflight

- Output mode: `review-report`; reviewer writes only `docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_record_contract_customer_surface_adversarial_artifact_review_v0.md`.
- Template kind: `review`; read-only adversarial artifact review.
- Authorization basis: current owner request to delegate review after discussing how a customer-facing profile should handle limitations, non_claims, and source_drill_back.
- Edit permission / targets / branch: read-only review of PR #633's record contract on branch `codex/creator-profile-record-contract`; no source edits, no patch queue, no implementation, no dashboard work.
- Reviews: findings-first adversarial artifact review; severity labels allowed as `critical | major | minor` for ordering only.
- Doctrine change: none authorized. If the reviewer finds doctrine change is required, flag it; do not patch.
- De-correlation: author/home model family is OpenAI/GPT. The operator owns the receiving reviewer choice. Record the actual reviewer/controller family in the report; do not fabricate cross-vendor status and do not recommend runtime model choice.
- Review-use boundary: findings are decision input only. They are not approval, validation, readiness, buyer proof, or mandatory remediation.
- Destinations: this prompt is the input artifact; write the report at the intended report path above.

## Objective

Adversarially review whether the record contract supports this intended customer
surface pattern without becoming misleading:

1. The primary customer-facing creator card may stay clean and scanable.
2. It may avoid dumping full `limitations`, `non_claims`, and `source_drill_back`
   on the first screen.
3. It must still carry enough visible trust posture for every shown metric or
   summary, and the full caveats/evidence must be available before the customer
   relies on ranking, comparison, outreach, or a stronger product claim.

The reviewer should attack the boundary between "not shown by default" and
"hidden in a way that causes an overclaim."

## Current Design Hypothesis To Test

The likely product shape is progressive disclosure:

- primary surface: identity, platform accounts, current metric rollups, freshness
  status, sample/trust posture labels, and clean summaries;
- inline cues: compact phrases such as `admitted-pool`, `selected-grid`,
  `source-limited`, `not_attempted`, `stale`, or `unavailable_with_reason` where
  they affect interpretation;
- details drawer or audit view: full `limitations`, `non_claims`,
  `source_drill_back`, calculation recipe, lineage, and source row pointers;
- hard boundary: unavailable, hidden, not_attempted, or not_applicable values
  must never be converted to zero, ranked as observed performance, or used for
  stronger claims.

This hypothesis may be wrong or under-specified. The review should say so if the
record contract or adjacent product surface does not actually support it.

## Required Source Loading

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read these overlay authority files:
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/product-proof.md`
3. REFERENCE-LOAD `workflow-deep-thinking`. Do not apply it until source context is ready.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not apply it until source context is ready.
5. SOURCE-LOAD the review target and comparison pack:
   - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
   - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
   - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
   - `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
   - `docs/workflows/orca_repo_map_v0.md`, targeted only to route placement and lane context
   - PR diff for #633 or local equivalent of `git diff e53f03cbbf3308a180cb9e22a967f1bccc9e74c4..HEAD -- orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md docs/workflows/orca_repo_map_v0.md orca/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
6. Verify the review target hash against `B540E3A211790A5F7182F2C5AFBF6B67B098FF0D23BBAF4F83E124F7C55EED86` or explicitly report target drift.
7. Declare `SOURCE_CONTEXT_READY` only after the target and source pack are read. If any load-bearing source is unavailable, declare `SOURCE_CONTEXT_INCOMPLETE` and write a blocked/advisory report instead of strict findings.
8. After source readiness, APPLY `workflow-deep-thinking` to frame customer-display failure modes, then APPLY `workflow-adversarial-artifact-review` to produce findings.

## Review Axes To Attack

Attack at least these failure modes:

1. The contract says limitations and non_claims are part of the contract, but gives downstream customer surfaces no safe way to collapse them without overclaiming.
2. The contract requires caveats to "travel" but does not distinguish primary UI, detail drawer, audit export, and operator-only evidence use.
3. A customer could see a clean metric card and miss that the number is admitted-pool-only, selected-grid-only, stale, thin, unavailable, or not_attempted.
4. `source_drill_back` can be hidden so deeply that challenged evidence is not actually available at decision time.
5. Section 2 blocks zero-fill and bad comparison, but lacks concrete enough display obligations for ranking, sorting, or creator shortlisting.
6. `non_claims` are too legalistic or too buried to prevent buyer-proof, performance prediction, outreach authorization, actual-audience, or readiness overclaims.
7. The record contract oversteps into Creator Signal product-surface ownership instead of naming only data-model promises.
8. The adjacent Creator Signal surface already owns customer-facing display obligations, making this contract either duplicative, conflicting, or missing a needed cross-reference.
9. Declared-deferred global stats (`posting_cadence`, `recent_velocity`) look populated or formula-ready to a customer before Silver emits accepted source-backed values.
10. The progressive-disclosure hypothesis lets a seller postpone truth "until questioned" rather than preserving a visible trust posture from the start.

## Output Contract

Write a durable report at:

`docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_record_contract_customer_surface_adversarial_artifact_review_v0.md`

The report must include:

- retrieval header;
- target path and target hash checked against `B540E3A211790A5F7182F2C5AFBF6B67B098FF0D23BBAF4F83E124F7C55EED86`, or explicit target drift;
- `reviewed_by`, `controller_family`, `author_home_family`, and `de_correlation_bar` fields, using `unrecorded` only when not supplied by the operator;
- source-read ledger for load-bearing sources;
- compact `review_summary` YAML before detailed findings;
- findings first, ordered by severity;
- for every actionable finding: evidence citation, impact, `minimum_closure_condition`, and `next_authorized_action`;
- explicit answer to whether progressive disclosure is safe here, unsafe, or safe only with named conditions;
- non-findings only when they rule out plausible material failures;
- residual risk and review-use boundary.

Do not emit `patch_queue_entry`. Do not edit source files. Do not claim approval,
validation, readiness, implementation authorization, buyer proof, customer
validation, or mandatory remediation.
