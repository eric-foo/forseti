# Creator Signal Multi-Creator Library Display Contract Authoring Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Handoff prompt for authoring the Creator Signal multi-creator library/catalog
  display contract over creator_profile_current rows before any static
  projection or runtime UI implementation.
use_when:
  - Starting the docs-write lane for the multi-creator Creator Signal library surface.
  - Checking what must be settled before projecting creator_profile_current into a customer-scannable multi-creator view.
  - Preserving the PR #636 review guards without reusing leaderboard framing.
authority_boundary: retrieval_only
branch_or_commit: origin/main@b09b7b907a851116cea2c41bf12cc6f0ac85ce2b
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/workflows/creator_registry_record_contract_handoff_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md
```

## Prompt Preflight

```yaml
output_mode: file-write
template_kind: handoff
template_source: none; direct Orca handoff prompt authored through prompt-orchestration contract
prompt_artifact_path: docs/prompts/handoffs/creator_signal_multi_creator_library_display_contract_authoring_prompt_v0.md
downstream_output_artifact_path: orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
downstream_output_note: target contract file does not exist yet; this prompt commissions creating it
edit_permission: docs-write
edit_targets:
  - orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md
  - docs/workflows/orca_repo_map_v0.md
branch_baseline: origin/main@b09b7b907a851116cea2c41bf12cc6f0ac85ce2b
dirty_state_allowance: clean worktree required before edits
receiving_lane_repo_access: required
runtime_or_implementation_authority: not authorized
review_authority: not authorized in this lane; commission a separate adversarial artifact review after the contract draft lands
```

## Orca Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: >
    Create the Creator Signal multi-creator library/catalog display contract.
    Do not create runtime code, a dashboard, data-lake writes, capture jobs,
    SQLite/API surfaces, identity-ledger rows, or outreach/lead-list mechanics.
  dirty_state_checked: required before downstream edits
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/validation-gates.md
```

## Cynefin Routing

Smallest complete outcome: author one Creator Signal product contract that defines how a customer/operator may scan a multi-creator library/catalog over the current creator_profile_current rows, including visible guardrails for sorting, missingness, sample support, non-claims, and drill-back.

Regime: Mixed complicated/complex.

Why: The source hierarchy and row facts are knowable, but sorted multi-creator display can create product claims the data contract does not authorize.

Decomposition: risk-first, then layer-based. First close rank/sort claim risk in the display contract; only then let a static projection consume that contract.

Current bottleneck: a binding multi-creator display contract in the Creator Signal spine.

Riskiest assumption: the current rows can be sorted as a library without implying a global leaderboard, lead list, buyer proof, or cross-platform merit rank.

Stop or pivot condition: the draft tries to define one mixed-platform global rank, rank `posting_cadence` or `recent_velocity` while they are `not_attempted`, hide sample-support posture, omit a reachable non-claims mechanism, or create outreach/lead-list authority.

Allowed next move: write the Creator Signal multi-creator library surface contract.

Disallowed next move: build the static projection, UI, API, dashboard, capture job, data-lake physicalization, identity linkage, or outreach workflow in this lane.

## Fused Assumption Gate For Steps 2 And 3

This gate accepts the owner direction: use a library/catalog surface, not customer-facing leaderboard framing, over the current Silver-backed registry rows.

```yaml
assumption_gate:
  status: READY_WITH_VERIFIED_LEDGER
  applies_to: >
    Step 2: author the multi-creator Creator Signal library display contract.
    Step 3: after that contract lands, create a static projection over
    creator_profile_current that consumes the contract.
  load_bearing_assumptions:
    - assumption: The new display contract belongs in Creator Signal, not Capture, Silver, or the creator registry record contract.
      why_load_bearing: Wrong home would mix data-record semantics with product display and make later projection consume the wrong authority.
      verify_by: source_read
      verdict: verified_real
      evidence: >
        creator_profile_current_record_contract_v0 says multi-creator ranking,
        grid, shortlist, lead-list, or outreach surfaces require a separate
        accepted Creator Signal or successor display contract. The existing
        Creator Signal profile surface says Creator Signal owns first-screen IA,
        product-facing non-claims, limitation/missingness/freshness/source-drill-back
        display, and product language.
    - assumption: The default can be a sorted library/catalog only if sorting is structurally platform-scoped and claim-guarded.
      why_load_bearing: A naive mixed-platform sorted list would violate the record contract's comparison rules and read as a leaderboard/merit rank.
      verify_by: source_read
      verdict: verified_real
      evidence: >
        The landed PR #636 review recommends the contextual ranked scan shape
        only conditionally, requiring platform-scoped default sort, visible
        sample-support cues, declared-deferred field visibility, and reachable
        non_claims. Current data has 33 rows: 30 YouTube and 3 Instagram.
    - assumption: The static projection can use the current rows for row-treatment testing, but it cannot exercise populated ideal-audience or global cadence/velocity states.
      why_load_bearing: If the projection pretends those states exist, it will create fake product coverage and bad fixtures.
      verify_by: source_read
      verdict: verified_real
      evidence: >
        Current creator_profile_current view counts show 33 profiles, 0 creator_record
        profiles, 0 cross-platform rollup profiles, 0 ideal-audience profiles,
        posting_cadence not_attempted for all 33 rows, and recent_velocity
        not_attempted for all 33 rows.
  prerequisites:
    - item: Platform-scoped default navigation is mandatory: tabs, sections, or an equivalent filter must keep YouTube and Instagram sorting separate by default.
      triage: blocker
      owner: agent
      order: 1
      basis: Required to close PR #636 MC-01 before any sorted default is safe.
    - item: Declared-deferred metrics must be visible at scan-row or column-family level and non-sortable while not_attempted.
      triage: blocker
      owner: agent
      order: 2
      basis: Required to close PR #636 MC-02 and the record contract's formula-only non-claim.
    - item: Sample-support cue must be visible on every sorted/scanned row.
      triage: blocker
      owner: agent
      order: 3
      basis: Required to close PR #636 MC-03; current rows include 2 thin-n and 1 limited-n row.
    - item: A reachable claim-boundaries/non-claims mechanism must be defined for the library surface.
      triage: blocker
      owner: agent
      order: 4
      basis: Required to close PR #636 MC-04 and to avoid leaderboard/lead-list/buyer-proof implications.
    - item: Literal customer-facing leaderboard language stays out of the target contract except as forbidden-language context.
      triage: already-decided
      owner: owner
      order: 5
      basis: Owner accepted library/catalog framing after PR #636 landed.
    - item: Static projection over current rows.
      triage: deferrable
      owner: agent
      order: 6
      basis: Safe only after this display contract lands, because projection must consume settled row, sort, and disclosure semantics.
    - item: UI/dashboard/API/SQLite/data-lake/capture implementation.
      triage: deferrable
      owner: owner
      order: 7
      basis: Explicitly outside the current docs-write lane and not required to settle the display contract.
  next_authorized_step: >
    Author the downstream display-contract file only, then commit, push, and
    open a PR for review. Do not execute Step 3 in the same lane.
```

## Receiver Task

You are the downstream docs-write lane. Your job is to author:

`orca/product/spines/creator_signal/creator_signal_multi_creator_library_surface_v0.md`

That target file does not exist yet; create it. Keep the branch clean except for that target contract and a minimal repo-map update only if a validation gate requires map reachability.

### Required Source Loading

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
- `docs/workflows/creator_registry_record_contract_handoff_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/creator_signal_multi_creator_ranked_scan_default_adversarial_artifact_review_v0.md`
- `orca-harness/capture_spine/creator_profile_current/materialize.py` targeted to `_profile_limitations`, `_build_platform_account_profile`, and `_counts`
- `orca-harness/capture_spine/creator_profile_current/validation.py` targeted to posture/value coupling and sample-support validation

After reading, declare either:

```text
SOURCE_CONTEXT_READY
```

or:

```text
SOURCE_CONTEXT_INCOMPLETE: <missing source, conflict, or stale baseline>
```

Do not draft the contract before that declaration.

### Verified Data Posture To Reconfirm

Reconfirm these from `creator_profile_current_view_v0.json` in your worktree before using them:

```text
profiles_total=33
platforms=instagram:3,youtube:30
creator_record_profiles=0
cross_platform_rollup_profiles=0
profiles_with_ideal_audience_profiles=0
posting_cadence=not_attempted:33
recent_velocity=not_attempted:33
sample_adequacy=limited_n_4_to_7:1,stronger_admitted_pool_n_8_plus:30,thin_n_1_to_3:2
```

If any value differs on your baseline, re-derive the contract from the live source and state the drift.

## Contract Requirements

The target contract must include these sections or direct equivalents:

1. Status, purpose, and authority boundary.
2. Source basis and current data posture.
3. Ownership split:
   - Capture/registry owns source rows, current read model, posture/value coupling, and source pointers.
   - Creator Signal owns product display, library navigation, claim-boundary language, and customer/operator scan behavior.
4. Default view:
   - name it `Creator Library`, `Creator Signal Library`, or a similarly neutral library/catalog term;
   - organize rows by platform by default, through tabs, sections, or an equivalent visible platform filter;
   - do not define one mixed-platform global rank.
5. Row model:
   - identity/account handle and platform;
   - current metric rollups;
   - selected sort metric and posture;
   - sample-support cue;
   - freshness cue;
   - declared-deferred metric state;
   - missingness/limitations cue;
   - claim-boundaries/non-claims affordance;
   - source drill-back affordance.
6. Sorting semantics:
   - call the behavior sorting/filtering inside a library, not ranking creators as winners;
   - allow sorting only by observed metrics;
   - keep sorting platform-scoped by default;
   - forbid treating null, unavailable, not_attempted, out_of_window, or not_applicable as zero;
   - forbid `posting_cadence` and `recent_velocity` sorting while they remain `not_attempted`;
   - forbid composite scores unless a later accepted contract creates them.
7. Display tiers:
   - always-visible row cues for platform, selected metric posture, sample support, freshness, missingness, and claim boundary;
   - details drawer or equivalent for full limitations, non_claims, source_drill_back, calculation recipe/version, and lineage.
8. Non-claims:
   - not leaderboard;
   - not lead list;
   - not outreach authorization;
   - not buyer proof or product proof;
   - not performance guarantee;
   - not cross-platform identity proof;
   - not universal/channel-wide creator influence;
   - not dashboard/API/SQLite/data-lake/capture authorization.
9. Static projection handoff boundary:
   - Step 3 may create a static projection only after this contract lands;
   - the projection may exercise current row display, platform separation, observed metric sorting, sample-support cues, deferred metric states, and non-claims affordances;
   - the projection may not invent populated ideal-audience, creator_record, cross-platform rollup, cadence, velocity, outreach, or lead-list states.

## Hard Constraints

- Do not use the literal customer-facing word `leaderboard` except in a forbidden-language/non-claim note.
- Do not create or edit capture, data-lake, dashboard, SQLite, API, identity-ledger, or runtime implementation files.
- Do not run capture or write to any external lake.
- Do not infer cross-platform identity or create creator_record rows.
- Do not claim validation, readiness, buyer proof, product proof, implementation authorization, or source-of-truth promotion.
- Do not convert formulas, field names, or declared-deferred fields into populated values.
- Do not call a sorted table a lead list, outreach list, recommended creators list, or priority queue.

## Validation To Run

Run the smallest complete docs validation set before completion:

```powershell
git diff --check
python .agents/hooks/check_retrieval_header.py --changed --strict
python .agents/hooks/header_index.py --strict --base origin/main
python .agents/hooks/check_handoff_pointers.py --strict --base origin/main
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_dcp_receipt.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict
```

If a command is unavailable or fails because the repo baseline is stale, report the observed failure and do not claim completion. If a gate exposes that `docs/workflows/orca_repo_map_v0.md` must mention the new Creator Signal contract, make the smallest map update needed for reachability and re-run the gate.

## Completion Contract

Before closing:

- fresh-read the written target file and report its observed line count;
- run `git status --short --branch`;
- report every validation command as pass/fail/not-run with observed output;
- commit, push, and open a PR per the Orca PR flow if validation is clean;
- do not self-merge;
- recommend a separate adversarial artifact review prompt for the drafted contract after the PR is ready or landed.

## ELI5 For The Receiver

We are making a customer-scannable creator library from the current creator registry rows. It can sort inside a platform, but it must not pretend to be a universal winner board. The customer can see the easy table first, but the row still needs visible warnings for missing data, thin samples, unavailable cadence/velocity, and what the table does not prove.
