# TikTok Creator Discovery Frontier Register v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract (scanning source-family adapter)
scope: >
  Defines the bounded TikTok Creator Discovery Frontier Register: how TikTok
  suggested-account, profile-carousel, and creator-adjacent discovery edges are
  recorded as scanning/frontier structure without becoming Creator Registry
  identity proof, follower-graph capture, live traversal, or capture execution.
use_when:
  - Recording TikTok suggested-account creator discovery from an owner-authorized seed profile.
  - Deciding whether a TikTok creator recommendation edge belongs in Creator Registry or scanning frontier memory.
  - Preparing a bounded next creator scan from prior TikTok discovery edges.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_selector_v0.md
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
stale_if:
  - TikTok suggested-account surfaces move behind a different access posture.
  - A dedicated TikTok discovery harness/schema supersedes this review-input register shape.
  - Creator Registry adopts a first-class cross-platform discovery graph with typed weak edges.
  - The advisory frontier selector is promoted beyond an advisory heuristic (see the selector doc's own `stale_if`).
```

## Status

Status: `SPEC_PROPOSED_MGT_FRONTIER_ADAPTER`.

This is a Mini God Tier scanning/frontier adapter: it targets most of the useful
creator-discovery graph value while stopping before standing crawler, monitor,
registry, dashboard, database, or runtime infrastructure. It is not validation,
readiness, live access authorization, registry insertion authorization, or
source-access proof.

## Why This Exists

TikTok suggested-account surfaces are useful because they reveal adjacent creator
candidates from the platform's own recommendation context. They are not useful
as identity proof by themselves.

The register lets Forseti remember:

- which creator seed produced which candidate handles;
- which weak platform edge exposed a candidate;
- whether a candidate was already seen, held, blocked, or selected for a later
  bounded scan;
- which source packet backs the observation;
- which next-run envelope would scan a candidate if the owner launches it.

It deliberately does not say that the candidates are the same creator, followers,
friends, endorsed accounts, US-based, on-niche, or capture-ready.

## Edge Vocabulary

An edge is a typed relation between two nodes. The type is the claim boundary.

For this register:

- `discovered_from_run` means the node was observed during one bounded discovery
  run.
- `platform_suggested_account_relation` means TikTok displayed the candidate as
  a suggested/related account from the primary visible Followers relationship
  dialog's Suggested tab, or from the visible seed-profile Suggested accounts /
  exact View All fallback.
- `already_seen` means the candidate was already present in this or another
  register and should not be re-added as a fresh candidate.
- `selected_as_next_frontier` means a human/agent selected that node for a later
  bounded scan; it does not authorize execution.
- `rejected_for_frontier` means the node was deliberately not pursued in the
  current planning pass.
- `blocked_or_empty` means the source-visible surface was unavailable, empty, or
  blocked in a way that should remain visible.

Identity edges are out of scope here. Same-creator claims belong in Creator
Registry linkage evidence after source-visible proof and preflight.

## Register Shape

The register mirrors the existing Reddit/LinkedIn Graph Frontier pattern while
using TikTok creator node types:

```yaml
tiktok_creator_discovery_frontier_register:
  schema_version: tiktok_creator_discovery_frontier_register_v0
  register_id:
  source_run_id:
  root_seed:
    platform: tiktok
    handle:
    url:
  provenance:
    source_surface:
    source_packet_id_or_none:
    source_packet_path_or_none:
    parent_grid_packet_id_or_none:
    parent_grid_packet_path_or_none:
    captured_at_utc:
    method_mode:
    access_mode:
    caps_applied:
    stop_reason:
  nodes:
    - node_id:
      node_type: run | tiktok_creator_seed | tiktok_creator_candidate
      platform: tiktok
      handle_or_none:
      display_name_or_none:
      source_url_or_locator:
      run_id:
      source_surface:
      timestamp:
      method_mode:
      access_mode:
      caps_applied:
      exclusions:
      stop_reason:
      registry_preflight_status_or_none:
      registry_preflight_receipt_evidence_or_none:
        receipt_pointer:
        receipt_sha256:
        candidate_id:
        intended_action:
        decision:
        action_status:
        can_start_new_capture:
      platform_capture_status:
      cross_platform_graph_status:
      non_claims:
  edges:
    - edge_id:
      edge_type:
      from_node_id:
      to_node_id:
      run_id:
      source_surface:
      source_packet_id_or_none:
      observed_sections:
      timestamp:
      method_mode:
      stop_reason:
      confidence:
      non_claims:
  frontier_decisions:
    - decision_id:
      selected_node_id:
      projection_decision: promote | hold | reject | already_seen
      frontier_selection_reason:
      frontier_selection_actor:
      frontier_selection_timestamp:
      next_run_id_or_none:
      non_claims:
  next_run_envelopes:
    - schema_version: tiktok_creator_discovery_next_run_envelope_v0
      next_run_id:
      selected_node_id:
      prior_register_pointer:
      declared_seed_or_surface:
      candidate_surface_allowlist:
      caps:
      exclusions:
      method_mode:
      access_mode:
      source_policy_posture:
      stop_condition:
      execution_authorized: false
      non_claims:
  accepted_residuals:
  non_claims:
```

## Receipt-Backed Writing

The preferred code path is the network-free builder under
`forseti-harness/capture_spine/tiktok_creator_discovery_frontier/`. It consumes a
validated `tiktok_creator_discovery_scan_receipt_v1` plus already-observed
suggested-account rows, then emits this register shape. The receipt records caps,
packet/lake pointers, refresh outcome, pagination bound, browser-close posture,
no follow/open/screenshot actions, and (v1, 2026-07-10) a required
source-visible link-hub outcome (`captured` with an absolute http(s) URL,
`blocked`, `deferred_not_authorized`, or `none_visible`) so a visible Linktree
can no longer be silently skipped. A validated register may be persisted to the
data lake as a derived record anchored to its committed parent-grid packet via
`runners/run_tiktok_creator_discovery_register.py` (lake write is the default;
an explicit `--output` file is the local escape). The builder still does not
launch TikTok, create a live runner, prove source truth, authorize next runs,
or mutate Creator Registry.

The builder prepends a default scope-limit `accepted_residuals` entry for
suggested-account registers: suggested handles are recommendation targets only;
candidate account sizes, regions, sibling channels, and quality remain unknown
until a later authorized candidate-profile run captures them. This is an
anti-overclaim label, not a new blocker or capture restraint.

When the scan uses the retained Chrome CDP surface patched with CloakBrowser
`resolve_config("careful")` and captures a parent profile/grid packet,
suggested-account graphing is the next same-surface step. Click the visible
creator `Followers` count, wait for the visible relationship dialog, click that
dialog's `Suggested` tab, and extract profile rows only from that visible dialog.
Only when the primary route is not visible may the runner use the visible
`Suggested accounts` heading plus exact `View All` fallback. Record `captured`,
`visible_empty`, or `not_visible` distinctly, keep the outer route separate from
the humanized pointer-layer disclosure, and record a packet before link-hub or
sibling-channel work. Never click Follow, open a candidate profile, like, or
message.

On first capture, the CDP adapter adopts the most recently enumerated non-closed
TikTok page, regardless of its current creator/path. It never adopts a
cross-platform page and creates one page only when no TikTok page exists. The
acquired page is reused until detach; it navigates to the requested creator when
the adopted TikTok path differs and suppresses `goto` when normalized TikTok
host/path already matches (scheme, query, and fragment do not affect that
comparison). Receipts carry
`page_acquisition_policy=adopt_same_platform_else_create`, platform and exact
match counts, adoption/creation/navigation counts, and same-URL suppression
count. Duplicate platform matches use the latest enumerated page; active focus
is never inferred.

The creator grid is established once on that acquired page. Suggested primary,
fallback, modal close, grid collection, and every onboarding deep capture remain
on the same page without reloading the same creator or clicking Latest, Popular,
or Oldest. Acquisition reads the initial exact-creator DOM order. An already-
loaded window of at least 27 videos uses zero acquisition wheels; otherwise use
bounded adaptive normal 20-35 percent viewport mouse-wheel bursts only until the
first positive exact-video-ID batch delta. It performs no further wheel action
after initial sufficiency or that first new batch and requires the ordered
sequence to remain unchanged for two consecutive passive DOM polls. It never
scrolls to page bottom, repeats wheel bursts until a response count reaches 30,
loads another batch after sufficiency, or accepts a stabilized one-batch window
below 27 videos. Freeze up to 30 stabilized rows. Fixed-count onboarding ranks by reach: prefer structured profile-grid
`playCount`, else use the exact tile's compact view footer as explicitly rounded
DOM evidence with raw text and field provenance. Naturally available engagement
metrics are preserved but do not gate fixed-count membership; pinning remains
recorded without displacing reach rank.

After the existing randomized 8-13 second wait, each selected video is opened by
randomly choosing among currently viewport-visible selected grid tiles.
Resolve the chosen tile's link-routed view-count footer immediately before the
pointer action, then click a randomized point within that footer's central 70
percent (15-85 percent on each axis). The footer itself must intersect the
viewport; partial thumbnail visibility does not make an off-screen footer
actionable. Do not cache absolute screen coordinates or click the hover-preview
`<video>` body, which may consume the click as playback.
After capture, close the overlay back to the creator grid before choosing the next
tile. If fewer selected tiles are currently visible, bounded normal-grid viewport
pagination may expose them. Remember stable video identities and logical grid
positions, compare them with the freshly observed visible position range, and use
receipt-backed 20-35 percent viewport mouse-wheel bursts in the required
direction; never target-scroll a tile into view. Once the live grid has loaded
through the frozen window's logical bound, zero live/frozen video-ID overlap
stops as `frozen_window_identity_drift`. Repeating a prior non-consecutive grid
state stops as `progress_cycle`; changed scroll position alone is not useful
progress when it cycles. The receipt distinguishes the CloakBrowser-humanized
cursor move from the raw bounded wheel burst. If a pointer
click does not materialize the matching visible video overlay, wait 60 seconds,
recompute the visible subset, and retry once; a second failure stops loudly.
The overlay URL plus clicked grid identity bind the video, profile-grid responses
provide structured video metadata, and page-owned comment responses or visible
overlay DOM provide initially exposed comments. Direct-video `itemStruct` is
optional on this route. Direct-video navigation remains a separate diagnostic or
future collector capability and is never an onboarding fallback.

Close the primary relationship dialog or collapse fallback Suggested accounts
through its exact profile toggle immediately after extracting its rows. A
page-wide generic Close/X target is forbidden. Grid collection, wheel pagination,
and tile clicks must not begin while the route surface, a blocking modal, or page
scroll lock remains; a required close that cannot be verified stops loudly before
the grid phase.

With `--data-root`, a captured non-empty suggested result must produce a non-null
frontier artifact or fail loudly. Validated external-profile evidence may become
sibling-channel linkage only through the existing Creator Registry identity
contracts; the discovery frontier does not infer such edges. A historical
recapture is written as a separate Bronze supplement with
`re_capture_relationship: supplement` and never rewrites prior provenance.


## PROMOTE Receipt-Evidence Binding

`PROMOTE` is receipt-gated. The selected candidate node must carry
`registry_preflight_receipt_evidence_or_none` with:

- an opaque repo/lake `receipt_pointer` and the SHA-256 of the exact receipt
  bytes;
- the selected `candidate_id`; and
- copied receipt-row clearance fields: `intended_action`, `decision`,
  `action_status`, and `can_start_new_capture`.

The validator does not guess how repo or lake pointers resolve. Its caller must
supply a resolver that returns the exact receipt bytes for the opaque pointer.
Validation fails closed when the resolver or artifact is absent, the hash is
stale, the JSON or receipt schema is malformed, the candidate row is missing or
duplicated, the copied fields differ from that row, the row is not
`new_capture` / `new_candidate` / `allowed` with
`can_start_new_capture: true`, or the row's normalized TikTok platform and
handle do not match the selected frontier node.

`registry_preflight_status_or_none` remains in v0 as a legacy informational
field so historical registers and current readers do not require a breaking
schema migration. It never clears `PROMOTE`; a scalar string, including a
plausible or positive-looking status, is not receipt evidence. The new evidence
field is additive and optional for non-PROMOTE nodes, so the register keeps its
v0 schema version. A future incompatible removal or meaning change requires a
schema-version decision rather than silently redefining v0.

This binding proves only that the cited exact-match preflight receipt cleared
this candidate for new capture under that receipt's registry snapshot. It does
not prove fuzzy duplicate absence, cross-platform identity, discovery quality,
capture authorization, registry mutation authorization, or source truth.

## Count And Completeness Semantics

`suggested_accounts_observed` is receipt/cap context for source-visible suggested
rows in the scan. The emitted candidate nodes are the rows selected for graphing
after any operator filtering, deduping, or bounded under-sampling. A count mismatch
is not itself a validator failure.

Cold agents must not claim the register exhausts all source-visible suggestions
unless the receipt/register explicitly records that all observed rows were
included. When rows were filtered, deduped, not paginated, or otherwise
under-sampled, record an `accepted_residuals` entry such as:
`Candidate nodes are a filtered/deduped subset of suggested_accounts_observed;
not exhaustive.`

If exact completeness becomes product-critical, add an explicit future field or
mode such as `candidate_rows_mode: exhaustive|filtered_subset` before enforcing
count equality in code.

## Cross-Platform Linkage

Cross-platform linkage is allowed as a separate strong-edge layer only after a
candidate's own source-visible evidence supports it:

1. TikTok discovery frontier sees `@candidate` from a weak recommendation edge.
2. A later bounded candidate scan captures that candidate's TikTok profile/grid
   and bio link hub, if source-visible.
3. Link hub, reciprocal links, or official profile references can create
   Creator Registry linkage evidence for the candidate's IG/YT/TikTok accounts.
4. Registry exact-match preflight routes known accounts as updates and unknown
   accounts as candidates.

Routine onboarding dogfood selects a Suggested/frontier candidate that is absent
from the Creator Registry and uses `new_capture`. An exact match means choose a
different eligible candidate; `update_existing` is reserved for a run whose
stated subject is recapture or an existing-creator regression. The registry is
identity/current-profile authority, not dogfood-run history.

The discovery frontier can point to registry candidate IDs when known, but it
must not create them by itself.

## MGT Accepted Residuals

| Residual | Why acceptable now | Remaining risk | Upgrade trigger |
| --- | --- | --- | --- |
| No standing TikTok crawler | Keeps the lane bounded and avoids crawler/runtime lock-in. | Some adjacent creators will be missed between owner-launched runs. | Repeated missed high-value creators or sustained multi-operator discovery cadence. |
| No Suggested pagination in onboarding | Keeps capture posture safe and session-visible. | The register may under-sample a suggested list. | Owner authorizes a separate bounded pagination probe with explicit caps and source-access posture. |
| Candidate count may differ from observed suggestion count | Allows bounded filtering/deduping without making false completeness claims. | A cold agent could overstate recall if it ignores accepted_residuals. | Exact completeness becomes product-critical and receives an explicit schema mode. |
| No ranking model | Superseded: `tiktok_creator_discovery_frontier_selector_v0.md` now provides an advisory duplicate-pressure ranker (frequency/expanded/fragrance heuristic scoring) over caller-supplied registers; it is not a quality model. | Ordering reflects duplicate-pressure heuristics only, not creator quality. | A quality-bearing or learned ranking model would need a separate decision. |
| No registry mutation | Preserves identity quality and duplicate safety. | Extra preflight step before onboarding. | Registry adopts a typed weak-edge intake lane with deterministic duplicate routing. |
| No full graph database | JSON registers are enough for current owner-launched scans. | Cross-run querying is manual or script-assisted. | Same vertical reaches repeated weekly scans or multi-root snowball management. |

## Enforcement Placement

For code-versus-doctrine placement before further scouting, open `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md`. The frontier spec defines the target shape; the enforcement-placement artifact classifies which behaviors need future validators/hooks/runners and which remain resident doctrine for cold agents.

## Hard Stops

- No same-run unbounded traversal.
- No standing crawler, monitor, dashboard, queue, or graph database.
- No follower/following graph claim unless that source-visible relationship was
  separately captured and typed.
- No registry insertion from recommendation edges alone.
- No contact enrichment.
- No private identity inference.
- No screenshots in chat by default.
- No Follow, like, message, candidate-profile open, or automated state-changing
  soft-restriction probe/retry.
- No metric zero-fill from discovery/link-hub observations.
- No CAPTCHA solving, proxy/account-rotation plan, forged signatures, or
  platform API replay.

## Non-Claims

Not validation, readiness, capture success, account-safety proof, source-access
authorization, Creator Registry identity proof, follower graph, endorsement
proof, country/region evidence, metric rollup, commercial permission, or
production infrastructure authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Followers-dialog Suggested capture is the primary TikTok discovery route and
    profile Suggested accounts/View All is fallback. Retained CDP acquisition now
    reuses the latest non-closed TikTok page at platform scope, suppresses same-path
    reloads, keeps Suggested-to-grid work on that page, closes and verifies the
    Suggested surface before any grid wheel or tile action using the
    relationship-dialog close for the primary route or the exact profile
    Suggested-accounts toggle for fallback; a generic page Close/X search is
    forbidden, and blocking-modal or scroll-lock residue fails loud. Grid
    acquisition accepts an already-loaded 27-video initial window with zero
    wheels; otherwise it uses bounded adaptive 20-35 percent viewport wheel
    bursts only until the first positive exact-video-ID batch delta, then zero
    further wheels and two consecutive stable passive DOM polls. It freezes up
    to 30 stabilized rows, fails when the one-batch window remains below 27, and
    does not page-bottom-scroll or chase a response count.
    Fixed-count reach selection prefers structured playCount and may use an
    explicitly rounded, provenance-bearing grid view footer when it is absent;
    optional engagement metrics no longer gate membership. The runner opens every
    selected video through a random currently visible selected grid tile,
    returning to the grid between overlays. Each chosen tile's link-routed view-count footer is
    freshly measured and clicked at a randomized point inside its 15-85 percent
    safe inset; the hover-preview body is not a click target. Bounded normal-grid
    pagination remembers logical positions and uses receipt-backed 20-35 percent
    viewport mouse-wheel bursts without caching screen coordinates. Live/frozen
    video-ID divergence stops once the frozen bound is loaded, and repeated
    non-consecutive grid state stops as a progress cycle instead of reversing
    indefinitely. Targeted tile scrolling and direct-video onboarding navigation
    are forbidden. Routine dogfood selects a Suggested/frontier candidate absent
    from the Creator Registry with `new_capture`; `update_existing` is reserved
    for an explicitly recapture-specific test. A failed overlay
    materialization gets one receipt-backed 60-second retry. Grid/API plus overlay
    evidence replaces a mandatory direct `itemStruct`.
    Account mutations and candidate
    opens remain forbidden; captured data-root runs fail loud without a frontier,
    and historical recaptures supplement rather than rewrite Bronze provenance.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - validation_philosophy
  controlling_sources_updated:
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md
    - forseti-harness/docs/source_capture_agent_runbook.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/forseti_repo_map_v0.md
    - forseti-harness/source_capture/adapters/browser_snapshot.py
    - forseti-harness/source_capture/tiktok/creator_onboarding.py
    - forseti-harness/source_capture/tiktok/batch_packet.py
    - forseti-harness/source_capture/tiktok/blocker_triage.py
    - forseti-harness/source_capture/tiktok/live_batch_probe.py
    - forseti-harness/source_capture/tiktok/grid_video_selection.py
    - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py
    - forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py
    - forseti-harness/tests/unit/test_source_capture_browser_snapshot.py
    - forseti-harness/tests/unit/test_tiktok_batch_admission.py
    - forseti-harness/tests/unit/test_tiktok_blocker_triage.py
    - forseti-harness/tests/unit/test_tiktok_creator_onboarding.py
    - forseti-harness/tests/unit/test_tiktok_grid_video_selection.py
    - forseti-harness/tests/unit/test_tiktok_live_batch_probe.py
  intentionally_not_updated:
    - path: AGENTS.md and .agents/workflow-overlay/
      reason: >
        Global behavior, authority, source-loading, and validation doctrine remain
        unchanged; this is a bounded TikTok product/source-family route change.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        Existing TikTok and source-capture index entries still resolve all controlling
        sources; no path or owner changed.
  stale_language_search: >
    rg -n -i "response_target_reached|scrollTo\(0, document.body.scrollHeight\)|playCount/diggCount.*fixed|fixed.*diggCount|required.*30.*grid|first deep entry|remaining selected videos|direct selected-video|source item detail|adopt_exact_target_else_create|arbitrary TikTok tab|profile suggested|View all.*Following|View all.*Followers|root follow|owner-authorized root follow|allows one.*follow|small mouse-wheel|update_existing.*dogfood|dogfood.*update_existing|identity drift|progress cycle|scroll.*suggested.*open|suggested.*open.*scroll|tiktok_suggested_surface_close_before_grid_v0"
    forseti/product/spines/scanning/source_families/tiktok forseti-harness/docs/source_capture_agent_runbook.md
    forseti-harness/source_capture/tiktok forseti-harness/capture_spine/tiktok_creator_discovery_frontier
  stale_language_search_result: >
    Executed 2026-07-15. Live hits outside the two receipt queries are the
    selection implementation's explicit fraction-mode playCount/diggCount list,
    the retained direct-page diagnostic helper, and accepted doctrine statements
    naming profile Suggested fallback or progress-cycle safeguards. No live
    onboarding source retains response-target/page-bottom acquisition, makes
    diggCount a fixed-count membership requirement, or uses the retired generic
    Suggested-surface close action.
  non_claims:
    - not validation
    - not readiness
    - not live capture success
    - not Creator Registry identity proof or mutation
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    TikTok frontier PROMOTE decisions now require a candidate-bound Creator
    Registry preflight receipt pointer, raw-byte SHA-256, copied clearance
    fields, and caller-resolved receipt verification; the legacy scalar status
    remains informational and cannot clear PROMOTE.
  trigger: architecture_doctrine
  related_triggers:
    - validation_philosophy
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
    - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py
    - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/creator_onboarding_first_batch_next_material_steps_handoff_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
    - forseti-harness/capture_spine/creator_profile_current/registry_match_preflight.py
    - forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_writer.py
    - forseti-harness/runners/run_tiktok_creator_discovery_register.py
    - forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py
  intentionally_not_updated:
    - path: AGENTS.md and .agents/workflow-overlay/
      reason: >
        Project-wide implementation authority, source loading, and receipt-field
        provenance rules already route this source-family binding without
        restating its schema.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        The existing Scanning spine and harness capture_spine/runners family-level
        entries still route to the target roots; no path family or owner changed,
        so a new file-level map row would add duplicate navigation.
    - path: forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
      reason: >
        The usage contract already owns the candidate-specific clearance fields
        and exact-match non-claims consumed here.
    - path: forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_writer.py
      reason: >
        The network-free builder emits no PROMOTE decisions. Its retained scalar
        field is legacy informational data and no longer clears the validator gate.
    - path: docs/workflows/creator_onboarding_first_batch_next_material_steps_handoff_v0.md
      reason: >
        This consumed checkpoint now meets its own stale_if conditions because
        the frontier schema and preflight semantics changed. It retains other
        excluded future batches, so this PROMOTE-only lane does not rewrite or
        delete their handoff; any future lane must re-ground and refresh it.
    - path: docs/prompts/reviews/tiktok_scanner_hardening_delegated_adversarial_code_review_patch_prompt_v0.md and docs/review-outputs/tiktok_scanner_hardening_delegated_adversarial_code_review_v0.md
      reason: >
        These are historical commission/review provenance for the defect, not
        live schema authority; rewriting them would falsify what was reviewed.
  stale_language_search: >
    rg -n "registry_preflight_status_or_none|registry_preflight_receipt_evidence_or_none|promote_requires_registry_preflight|PROMOTE.*preflight|preflight.*PROMOTE"
    AGENTS.md .agents forseti forseti-harness docs/workflows docs/decisions docs/prompts docs/review-outputs
  stale_language_search_result: >
    Executed 2026-07-11 after rebasing onto origin/main. Live hits are the
    updated product contract, model, validator, focused tests, and the builder's
    explicitly retained legacy informational field. The creator-onboarding
    handoff hit now meets that checkpoint's own stale_if conditions; remaining
    prompt/review hits are historical defect provenance. No checked live
    authority surface still says a scalar status clears PROMOTE.
  non_claims:
    - not validation
    - not readiness
    - not fuzzy duplicate detection
    - not capture authorization
    - not registry mutation authorization
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
