# IG Daily Heartbeat Runner Architecture Prompt - Repo Access v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact - architecture planning commission
scope: >
  Repo-access architecture planning prompt for the Instagram daily heartbeat
  runner/controller: registered-creator daily first-visible-grid monitoring,
  breakout-tag-only deep-capture eligibility, Creator Registry/Silver boundary,
  supervised browser/challenge posture, and source-pack-backed implementation
  scoping boundaries.
use_when:
  - Commissioning an external or fresh architecture pass with direct repository access.
  - Testing whether the daily heartbeat should be a new controller, an extension of an existing IG lane orchestrator, or a narrower runner patch.
  - Preparing multiple model outputs for later Chief Architect adjudication.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
branch_or_commit: >
  Source policy baseline: codex/ig-daily-heartbeat-policy @ 6d5db3d4. This
  prompt is authored on stacked branch codex/ig-heartbeat-architecture-prompts.
stale_if:
  - The IG daily heartbeat operating policy changes.
  - The IG grid runner exposes verified headed/CloakBrowser, asset-policy, challenge-handoff, or roster-heartbeat controls.
  - The Creator Registry index gains active/paused monitoring state or a successor roster source.
  - A daily heartbeat controller lands in code.
```

Paste the body below into ChatGPT Pro, Opus, or another architecture reviewer that has repository access. Runtime model choice is owner/tooling selection, not a Forseti prompt-lane claim.

---

You are reviewing the Forseti repository as an architecture planner. Produce a read-only architecture plan for the Instagram daily heartbeat runner/controller.

## What This Is For

Goal: settle the smallest durable architecture for daily IG creator heartbeat monitoring before implementation scoping.

Done looks like: Codex can adjudicate your report against another model's report and decide whether to build a new heartbeat controller, extend an existing runner, or stop because a source assumption is wrong.

## Forseti Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
authorization_basis: Owner request to prepare architecture-planning prompts for external model couriering; no implementation authority.
objective: >
  Recommend the architecture boundary for a daily IG heartbeat runner/controller
  that monitors registered creators with one first-visible /reels/ grid
  observation per day, uses existing grid capture primitives where possible,
  and preserves the separation between heartbeat, onboarding, deep capture,
  Creator Registry, and Silver-derived monitoring.
intended_decision: >
  Choose among: (A) a new daily heartbeat controller that wraps the existing
  grid packet primitive, (B) extending run_ig_reels_lane_orchestrator.py,
  (C) patching only run_source_capture_ig_reels_grid_packet.py, (D) building a
  cross-platform heartbeat controller now, or (E) blocked/source-incomplete.
target_files_or_dirs:
  - forseti/product/spines/capture/core/source_families/social_media/instagram/
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/
  - forseti-harness/runners/
  - forseti-harness/source_capture/
  - forseti-harness/capture_spine/creator_profile_current/
  - forseti-harness/tests/
source_pack: custom repo-access pack listed below.
repo_map_decision: loaded if needed; otherwise targeted reads are acceptable.
repo_map_reason: The source list below is the controlling pack; use the repo map only to resolve missing/moved paths.
output_mode: chat-only
edit_permission: read-only
dirty_state_allowance: >
  Do not rely on untracked or modified files unless explicitly named in the source list
  or supplied by the operator. Report dirty-state uncertainty instead of using it silently.
controlling_source_state: must be checked by the reviewer before strict claims.
branch_or_commit_reference: >
  Prefer the branch containing ig_daily_heartbeat_operating_policy_v0.md. If absent,
  report SOURCE_CONTEXT_INCOMPLETE instead of reconstructing it from memory.
doctrine_change_decision: >
  This prompt asks for an architecture recommendation only. Do not patch doctrine.
  If the correct answer requires changing product, architecture, workflow,
  validation, review, output, or lifecycle doctrine, name the needed propagation
  surfaces and stop at recommendation.
isolation_decision: no edits; read-only architecture planning.
validation_gates: no validation/readiness claims. Source-read ledger plus cited architecture reasoning required.
thread_operating_target_continuity: no visible active thread_operating_target carried forward.
```

## Hard Boundaries

- Do not edit files.
- Do not run live IG, TikTok, YouTube, browser automation, CloakBrowser, Playwright, or network capture.
- Do not use credentials, cookies, stored browser profiles, proxy endpoints, or session state.
- Do not provide stealth, CAPTCHA-solving, fingerprint-spoofing, or ban-evasion instructions.
- Do not treat DOM parsing as invisible to Instagram. Source access still creates browser/resource behavior.
- Do not import onboarding top-band deep-capture logic into daily heartbeat unless a cited source authorizes it.
- Do not invent breakout criteria. Daily heartbeat may consume breakout tags only if a monitoring/Silver lane produced them.
- Do not treat Creator Registry as metric authority or Silver as account identity authority.
- Do not recommend platform write actions as runner behavior.
- Do not generalize to TikTok or YouTube unless the repo sources prove the same contract applies.

## Source-Gated Method

1. Run Forseti Cynefin routing from `.agents/workflow-overlay/decision-routing.md` before planning. Include allowed next move and disallowed next move.
2. REFERENCE-LOAD architecture-planning method instructions if available. Do not APPLY them yet.
3. SOURCE-LOAD the required source pack below.
4. Declare exactly one: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY architecture planning.
6. Cite a local file path for every load-bearing claim. Use `unknown` when a field is absent.

## Required Source Pack

Authority and prompt rules:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md`

IG policy and source-family docs:

- `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md`

Creator Registry and Silver boundary:

- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`

Harness code and tests:

- `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py`
- `forseti-harness/source_capture/ig_reels_grid_capture.py`
- `forseti-harness/source_capture/ig_reels_grid.py`
- `forseti-harness/source_capture/ig_reels_grid_projection.py`
- `forseti-harness/runners/run_ig_reels_lane_orchestrator.py`
- `forseti-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py`
- `forseti-harness/runners/run_source_capture_ig_reels_deep_capture.py`
- `forseti-harness/source_capture/ig_reels_deep_capture.py`
- `forseti-harness/source_capture/ig_reels_deep_capture_lake.py`
- `forseti-harness/runners/run_source_capture_ig_reels_supervised_browser.py`
- `forseti-harness/source_capture/adapters/browser_snapshot.py`
- `forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py`
- `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
- `forseti-harness/capture_spine/creator_profile_current/materialize.py`
- `forseti-harness/capture_spine/creator_profile_current/validation.py`
- `forseti-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py`
- `forseti-harness/tests/unit/test_ig_reels_lane_orchestrator.py`
- `forseti-harness/tests/unit/test_ig_reels_supervised_browser_runner.py`
- `forseti-harness/tests/unit/test_ig_reels_creator_deep_capture.py`
- `forseti-harness/tests/unit/test_creator_metric_silver_producer.py`
- `forseti-harness/tests/unit/test_creator_registry_index.py`

## Strongest Rule To Test First

The strongest rule is: daily heartbeat is an additive Bronze/source-capture time-series controller over registered IG creators, not onboarding, not metric scoring, and not free-form deep capture.

Test that rule adversarially. If you disagree, show the exact source that gives the heartbeat runner authority to score breakouts, select top-band deep captures, paginate, mutate Creator Registry rows, or perform platform write actions.

## Known Starting Tensions To Verify

Treat these as hypotheses until sourced:

- The current grid packet runner already provides the per-creator primitive: one public `/<handle>/reels/` page load, DOM rows, passive JSON candidates, profile snapshot fields, and raw Source Capture Packet output.
- The daily heartbeat policy wants daily first-visible-grid monitoring for roughly 2.5k registered IG creators/day across 2 egress lanes, with 10-15s owner-set E2E target and owner-attention waits measured separately.
- Current registry index is the known-account preflight surface, but it may not yet carry active/paused monitoring state.
- The current committed index may contain only a small IG set; do not confuse current sample data with final 2.5k posture.
- The current grid runner may still default to `headless=True` and `block_heavy_assets=True`; the policy prefers supervised ordinary asset loading for daily heartbeat and treats heavy-asset blocking as bandwidth mode, not stealth.
- `run_ig_reels_lane_orchestrator.py` sequences grid, deep-capture, product-extract, and projection lanes; that may be wrong for steady-state heartbeat if it deep-captures by top-N instead of consuming externally produced breakout tags.
- `run_source_capture_ig_reels_supervised_browser.py` opens a persistent headed CloakBrowser but writes no packet.
- Browser snapshot infrastructure may already have backend, human challenge handoff, and CloakBrowser concepts that the grid packet runner does not expose.
- Silver producer records MetricObservation and MetricRollupObservation; it should own velocity/EMA/baselines/breakout tags unless sources prove otherwise.

## Architecture Questions

Answer directly:

1. Should daily heartbeat be a new controller around the grid packet primitive, an extension of `run_ig_reels_lane_orchestrator.py`, a patch to the grid runner only, or something else?
2. What exactly is the controller boundary versus the per-creator grid capture primitive?
3. What is the roster source for v0, given Creator Registry has known accounts but may not yet have active monitoring state?
4. How should stable 2-egress partitioning work without rotating every request?
5. What run receipt shape is needed to record per-creator outcome, timing, access gaps, owner-attention waits, asset policy, browser backend/headed state, and deep-capture selection posture?
6. What should happen on CAPTCHA/challenge/login redirect/access block?
7. What asset policy should the architecture expose, and what should remain implementation default until verified?
8. Should the controller launch/own browser sessions, call existing packet functions, or shell out to CLI entrypoints?
9. How should breakout-tag-only deep-capture queuing work without reimplementing monitoring/Silver scoring in the heartbeat runner?
10. Where should moving average, EMA, velocity, baselines, spike/fresh/active breakout tags, and low-momentum retirement live?
11. What must be tested with pure unit/fake-runner tests before any live run?
12. What is explicitly out of scope for the first implementation slice?

## Option Set To Rank

Rank these options and explain what would change your ranking:

- Option A: New `run_source_capture_ig_daily_heartbeat.py` controller that reads the registry/roster, partitions by egress lane, calls the existing grid packet primitive, records run receipts, and only queues deep capture for externally supplied breakout tags.
- Option B: Extend `run_ig_reels_lane_orchestrator.py` with heartbeat mode.
- Option C: Patch only `run_source_capture_ig_reels_grid_packet.py` to add headed/CloakBrowser/asset/challenge knobs, leaving batch scheduling outside Forseti.
- Option D: Build a platform-neutral heartbeat controller now for IG, TikTok, and YouTube.
- Option E: Block implementation scoping because source assumptions are not yet strong enough.

## Expected Output

Return in this exact structure:

```text
SOURCE_CONTEXT_READY_OR_INCOMPLETE:
missing_or_conflicting_sources:

Cynefin:
smallest_complete_outcome:
regime:
why:
current_bottleneck:
allowed_next_move:
disallowed_next_move:

Human Summary:
strongest_rule:
recommendation:
why_this_wins:
strongest_pushback_against_recommendation:

Architecture Plan:
recommended_option_rank:
controller_boundary:
grid_primitive_boundary:
registry_roster_boundary:
silver_monitoring_boundary:
deep_capture_boundary:
browser_session_and_asset_boundary:
challenge_owner_handoff_boundary:
egress_partitioning_model:
run_receipt_contract:
failure_and_missingness_contract:
test_strategy:
first_implementation_slice:
explicit_non_goals:

Adjudication Hooks For Codex:
claims_to_verify:
source_gaps_that_matter:
decisions_that_require_owner_input:
what_would_make_this_plan_wrong:

Source-Read Ledger:
```

Do not add a patch queue. Do not claim readiness. Do not claim the architecture is accepted. This is decision input for later adjudication.
