# Creator Signal Multi-Creator Static Projection Implementation Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Implementation handoff for Step 3: create one populated, source-backed,
  static Markdown projection of the Creator Signal Library over the current
  creator_profile_current rows after PR #638 landed the multi-creator display
  contract.
use_when:
  - Starting the implementation lane for the Creator Signal multi-creator static projection.
  - Checking what a static projection may render from creator_profile_current without becoming a leaderboard, lead list, dashboard, or outreach surface.
  - Preserving the accepted library/catalog contract while producing a populated artifact from current rows.
authority_boundary: retrieval_only
branch_or_commit: origin/main@0f460b01362a849e40174d11dd89e4804f5f9d19
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_independent_adversarial_artifact_review_v0.md
stale_if:
  - PR #638 is not present in the receiver's main-branch history.
  - The Creator Signal multi-creator library contract changes after origin/main@0f460b01362a849e40174d11dd89e4804f5f9d19.
  - creator_profile_current_view_v0.json changes platform mix, metric postures, sample support, identity state, or deferred-field posture.
  - A later accepted contract authorizes cross-platform rollups, creator_record subjects, populated ideal-audience rows, or posting_cadence/recent_velocity population.
```

## Prompt Preflight

```yaml
output_mode: file-write
template_kind: handoff
template_source: none; direct Orca implementation handoff authored through workflow-prompt-orchestrator contract
prompt_artifact_path: docs/prompts/handoffs/creator_signal_multi_creator_static_projection_implementation_handoff_prompt_v0.md
downstream_output_artifact_path: orca/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md
downstream_output_note: target file should not exist yet; this prompt commissions creating exactly one populated static projection artifact
edit_permission: implementation-authorized
edit_permission_boundary: >
  Bounded to a static Markdown product projection artifact only. No runtime app,
  dashboard, API, SQLite table, data-lake write, capture job, browser fetch,
  identity-linkage edit, outreach workflow, or reusable generator is authorized.
edit_targets:
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md
  - docs/workflows/orca_repo_map_v0.md # only if a validation gate proves a map update is required
branch_baseline: origin/main@0f460b01362a849e40174d11dd89e4804f5f9d19
merged_contract_commit: 5b5a2f49b8dc2c3e87a0feee207d1b3e36409a53
dirty_state_allowance: clean worktree required before edits
receiving_lane_repo_access: required
review_authority: not authorized in this lane; commission a separate adversarial review after the projection implementation is ready
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope: >
    Create one populated static Markdown projection over the current
    creator_profile_current rows, consuming the landed Creator Signal
    multi-creator library display contract. Do not create runtime code,
    reusable generator code, a dashboard, storage changes, capture jobs,
    SQLite/API surfaces, identity-ledger rows, CRM/outreach mechanics, or any
    source data.
  dirty_state_checked: required before downstream edits
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
```

## Authorization Basis

The owner confirmed PR #638 was merged and asked to write this prompt for the
next lane. Local authoring source state observed PR #638 in main history as:

```text
5b5a2f49 docs(creator-signal): multi-creator library display contract prompt + authored contract v0 (#638)
```

The merged contract says the static projection may be built only after the
contract lands. The contract file still carries the status token
`PR_REVIEW_PRODUCT_SURFACE_CONTRACT_V0`, but its body states it becomes accepted
after owner/maintainer acceptance and merge. On intake, verify PR #638 is present
in main history and the contract exists. If both are true, the Step 3 landed
condition is satisfied for this bounded static projection. Do not edit the
contract status token in this lane unless the current owner explicitly redirects.

## Cynefin Routing

Smallest complete outcome: create one source-backed static Markdown projection
of the Creator Signal Library over the current 33 committed
`creator_profile_current` rows, with platform-scoped tables, populated metric
states, source/drill-back pointers, and visible non-claims/limitations.

Regime: Mixed clear/complicated.

Why: The target is bounded and the source JSON is committed, but the projection
can still create false product claims if row order, copy, or hidden caveats make
it read as a leaderboard, lead list, buyer proof, or cross-platform rank.

Decomposition: layer-based with risk-first claim guards: verify source and
contract state, derive row facts from JSON, render platform-scoped library
sections, then validate the artifact against forbidden claims.

Current bottleneck: a populated static artifact that proves the contract can be
rendered without inventing data or implying rank.

Riskiest assumption: sorting or table order can be useful without creating a
winner/loser or lead-priority impression.

Stop or pivot condition: PR #638 is absent from main history; the target contract
is missing; the static projection target already exists; current data has
populated `creator_record`, ideal-audience, cross-platform rollup,
`posting_cadence`, or `recent_velocity` states; or the implementation needs
runtime code/dashboard/API/lake/capture work.

Allowed next move: author the one static Markdown projection artifact.

Disallowed next move: build a dashboard, app, API, SQLite table, data-lake job,
capture job, reusable generator, identity-linkage state, lead list, outreach
workflow, buyer-proof claim, or delegated review in this same lane.

## Receiver Task

Create this file:

```text
orca/product/spines/creator_signal/creator_signal_multi_creator_library_static_projection_v0.md
```

The file must be a populated static projection, not a plan. It should be
readable in GitHub Markdown and should show the current rows using only the
committed `creator_profile_current_view_v0.json` data and the landed display
contract.

If the file already exists, stop with:

```text
TARGET_COLLISION: creator_signal_multi_creator_library_static_projection_v0.md already exists
```

Do not silently overwrite, fork, or version-bump it.

## Required Source Loading

Read these before making actionable claims or edits:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_library_surface_v0_independent_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md`

After reading, declare either:

```text
SOURCE_CONTEXT_READY
```

or:

```text
SOURCE_CONTEXT_INCOMPLETE: <missing source, conflict, or stale baseline>
```

Do not create the projection before that declaration.

## Source Facts To Reconfirm

Reconfirm these from `creator_profile_current_view_v0.json` in the receiving
worktree before using them:

```text
profiles_total=33
counts={"creator_record_profiles":0,"cross_platform_rollup_profiles":0,"engagement_rate_observed_profiles":31,"platform_account_profiles":33,"profiles_total":33,"profiles_with_ideal_audience_profiles":0,"profiles_with_metric_rollups":33}
platforms=instagram:3,youtube:30
average_views=observed:33
median_views=observed:33
average_like_count=observed:32,unavailable_with_reason:1
average_comment_count=observed:32,unavailable_with_reason:1
engagement_rate=observed:31,unavailable_with_reason:2
posting_cadence=not_attempted:33
recent_velocity=not_attempted:33
sample_adequacy=limited_n_4_to_7:1,stronger_admitted_pool_n_8_plus:30,thin_n_1_to_3:2
identity_state=single_platform_observed:33
link_state_or_none=null:33
review_state_or_none=null:33
```

If the counts differ but the same contract-safe postures hold, rederive the
projection from live source and name the drift. If the drift introduces
populated creator records, cross-platform rollups, ideal-audience rows,
`posting_cadence`, `recent_velocity`, non-null link/review states, or a new
metric posture not covered by the contract, stop and return
`SOURCE_CONTEXT_INCOMPLETE` with the drift.

## Projection Requirements

The target projection must include these sections or direct equivalents:

1. Retrieval header.
   - `artifact_role`: `product_signal_static_projection`
   - `authority_boundary`: `retrieval_only`
   - `scope`: one concise statement that this is a static Creator Signal
     Library projection over the current committed rows.
   - `use_when`: include implementation review and customer/operator scan
     inspection.
2. Status and non-authority.
   - State that this is a static source-backed projection, not a dashboard,
     API, CRM list, capture job, data-lake write, source of truth, buyer proof,
     product proof, or outreach authorization.
3. Source snapshot.
   - Name `origin/main@0f460b01362a849e40174d11dd89e4804f5f9d19` or the
     receiver's actual checked commit if newer.
   - Name the input view file and generated timestamp from the JSON.
   - Include the reconfirmed data posture counts.
4. First-screen library framing.
   - Use `Creator Signal Library` or library/catalog language.
   - Do not use customer-facing `leaderboard`, `rank`, `top`, `best`,
     `recommended`, `priority`, `lead list`, or `winner`.
   - Include a visible "what this does not prove" affordance near the library
     framing.
5. Platform-scoped sections.
   - Render YouTube and Instagram as separate sections, tabs-equivalent
     headings, or clearly separated tables.
   - Do not render one all-platform combined table.
   - Do not include a global ordinal, rank number, or row number column.
6. Selected metric behavior.
   - Use an observed metric only. Default to `average_views` unless source
     loading gives a better observed metric and explains why.
   - Sorting, if shown, must be within each platform section only.
   - `posting_cadence` and `recent_velocity` must not be selectable or shown as
     populated values while `not_attempted`.
   - Null, unavailable, out-of-window, not-attempted, and not-applicable states
     must never render as zero.
7. Row table.
   - Include all current rows exactly once.
   - Each row must show platform, public handle/display name when present,
     profile subject id, selected metric value and posture, sample-support cue,
     freshness cue, `posting_cadence` deferred state, `recent_velocity`
     deferred state, missingness/limitations cue, and a source/details anchor.
   - Compact cues are acceptable, but the row must not require opening the full
     details section to learn that cadence/velocity are unavailable, sample
     support is limited/thin/admitted-pool-only, or a displayed metric is
     unavailable.
8. Details section.
   - Provide a details-drawer equivalent in Markdown for every row or a compact
     indexed details table that preserves the same information.
   - Include full or materially complete limitations, non-claims,
     source_drill_back pointers, metric rollup pointer, calculation recipe
     version, and additional metric family values/postures.
9. Non-claims and accepted residuals.
   - State at library level that this is not a leaderboard, lead list,
     outreach list, recommended-creators list, buyer proof, performance
     guarantee, cross-platform identity proof, dashboard/API/SQLite/data-lake
     authorization, or live capture authorization.
   - State that ideal-audience rows are exercised only in the always-null
     current state.
   - State that every profile is `platform_account` scoped and
     `single_platform_observed`.
10. Source drill-back.
   - Use Markdown anchors for row details and preserve source pointers as code
     paths or JSON pointers.
   - Do not convert source pointers into fake public URLs or claim source
     access that the JSON does not carry.

## Recommended Row Ordering

Use this projection order unless source loading gives a better contract-safe
reason:

1. YouTube section.
2. Instagram section.
3. Within each section, sort by `average_views` descending as the selected
   observed scan metric.
4. Do not display ordinal positions. The table order is a selected metric sort,
   not a creator ranking.

If the receiver chooses handle/profile-subject alphabetical order instead,
it must still include a small platform-scoped observed-metric sort example or
sort-control note so the projection exercises the contract's sorting semantics.

## Hard Constraints

- Do not create or edit capture, data-lake, dashboard, SQLite, API,
  identity-ledger, CRM, outreach, or runtime implementation files.
- Do not run capture, browser, live network fetches, or write to any external
  lake.
- Do not create a reusable generator or helper script as a committed artifact.
  A temporary local derivation script is allowed only if it is not committed and
  the final projection is freshly read and verified.
- Do not infer cross-platform identity or create `creator_record` rows.
- Do not invent populated ideal-audience, `posting_cadence`,
  `recent_velocity`, link-state, review-state, outreach, or lead-list states.
- Do not display unavailable or deferred values as zero.
- Do not claim validation, readiness, buyer proof, product proof, customer
  acceptance, implementation readiness, or source-of-truth promotion.
- Do not write the adversarial review prompt or review report in this lane.

## Validation To Run

Run the smallest complete validation set before completion:

```powershell
git diff --check
python .agents/hooks/check_retrieval_header.py --changed --strict
python .agents/hooks/header_index.py --strict --base origin/main
python .agents/hooks/check_handoff_pointers.py --strict --base origin/main
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_dcp_receipt.py --strict --base origin/main
python .agents/hooks/check_full_gt_claims.py --changed --strict
```

Also run a projection-specific row-count check of your choice that verifies the
target artifact accounts for the same number of current profiles as the source
JSON. Report the exact command and observed output. If code roots
(`orca-harness/`, `.agents/hooks/`) are touched despite this prompt's boundary,
run:

```powershell
python .agents/hooks/check_review_routing.py --strict --base origin/main
```

If any command fails, patch the projection if the failure is in scope; otherwise
report the blocker and stop. Do not claim completion with failing validation.

## Completion Contract

Before closing:

- fresh-read the written projection file and report its observed line count;
- report the source JSON profile count and the projection row count you
  verified;
- run `git status --short --branch`;
- report every validation command as pass/fail/not-run with observed output;
- commit, push, and open or update a PR per the Orca PR flow if validation is
  clean;
- do not self-merge;
- return to the Chief Architect/owner for a separate adversarial review prompt
  after the projection implementation is ready.

## ELI5 For The Receiver

Make a frozen, filled-in Creator Signal Library page from the current 33 creator
rows. It should be useful to scan, but it must never look like "these are the
best creators" or "contact these people first." Keep YouTube and Instagram
separate, show the caveats on every row, and only use facts that already exist
in the committed creator-profile-current JSON.
