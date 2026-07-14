# TikTok Creator Discovery Enforcement Placement v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract (enforcement placement for TikTok creator discovery scans)
scope: >
  Classifies the Fragranceknowledge/TikTok creator-scanning behaviors into code-enforced
  output/run-shape gates versus doctrine-enforced operator judgment, claim semantics,
  and source-access boundaries, so a cold agent can run the lane without relying on
  chat memory.
use_when:
  - Starting a cold TikTok creator discovery frontier scan.
  - Deciding whether a scan behavior needs a validator/hook/runner gate or a doctrine checklist.
  - Reviewing a TikTok creator discovery register before capture, registry insertion, or next-run launch.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/validation-gates.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
stale_if:
  - A TikTok creator discovery hook or runner lands and supersedes the future-code rows here.
  - Creator Registry adopts a typed weak-edge/discovery frontier intake lane.
  - TikTok capture posture changes source-access or session requirements for suggested-account scans.
```

## Status

Status: `ENFORCEMENT_PLACEMENT_CLASSIFIED_VALIDATOR_AND_RECEIPT_WRITER_BUILT`.

This artifact classifies enforcement placement and now has a validator plus
network-free receipt/register-writer substrate for the TikTok Creator Discovery
Frontier register. It still does not implement hooks, live browser runners,
registry writes, capture execution, or live platform access. A cold agent must
use it to decide what to check mechanically before closeout and what to preserve
as resident doctrine during the scan.

## Rule Of Thumb

Use code for facts that can be checked from files, JSON shape, command arguments,
or durable receipts. Use doctrine for judgment that depends on source meaning,
claim interpretation, owner authorization, platform posture, or whether the next
frontier is worth pursuing.

A code gate may prove shape. It does not prove truth, validation, readiness,
identity, region, endorsement, account safety, or metric quality.

## Enforcement Matrix

| Behavior | Enforcement home | Code status | Cold-agent action | Why |
| --- | --- | --- | --- | --- |
| Load AGENTS.md and workflow overlay before repo work | Doctrine plus existing workflow gates | Existing doctrine; partially hook-backed for durable artifacts | Read AGENTS.md and .agents/workflow-overlay/README.md before scan work | Source hierarchy/judgment trigger; not fully inferable from output JSON. |
| Use intended warmed browser/session; do not close it at lane end | Code plus doctrine/runbook | Existing Chrome CDP session adapter detaches without closing operator Chrome | State intended surface and leave it open unless owner asks otherwise | Session choice and operator intent remain live-context judgment; detach behavior is mechanical. |
| Avoid duplicate/wrong ordinary Chrome tabs | Code plus doctrine/runbook | Existing Chrome CDP session adapter adopts the most recently enumerated non-closed TikTok page regardless of creator/path, never adopts a cross-platform page, and creates only when no TikTok page exists | Verify `page_acquisition_policy=adopt_same_platform_else_create`, platform/exact match counts, and adoption/creation/navigation counts | Platform matching, latest-enumerated selection, and same-path navigation suppression are mechanical; no active-focus claim is made. |
| Keep Suggested-to-grid continuity and minimize deep-capture footprint | Code plus doctrine/runbook | Onboarding suppresses same-profile reloads, performs no sort-tab click, closes the relationship modal, opens every selected video through a currently visible selected grid tile, and closes each overlay back to the retained grid | Require one 8-13 second pre-entry wait, random choice among visible selected tiles, bounded normal-grid pagination only when needed, zero targeted tile scroll, zero direct-video onboarding navigation, and at most one 60-second retry after failed matching-overlay materialization | Viewport intersection, pagination/retry bounds, return-to-grid, and receipt shape are mechanical; the product preference for normal grid-to-overlay use is doctrine. |
| Bind overlay evidence without mandatory direct-video hydration | Code plus doctrine/runbook | The clicked grid identity and overlay URL bind the video; profile-grid responses supply available structured metadata; page-owned comment responses and visible overlay DOM supply initially exposed comments; direct `itemStruct` is optional | Preserve naturally available fields with per-field provenance, distinguish captured/visible-empty/not-visible comments, never zero-fill unavailable optional metrics, and fail on identity mismatch | Evidence availability differs between normal grid overlays and direct URLs; validators must model that reality rather than forcing the direct-page shape. |
| Parent platform profile/grid capture when entering seed profile | Code plus doctrine | Register validator and scan receipt validator built; future runner optional | Require a parent profile/grid packet pointer or explicit not-captured reason in the receipt/register | Presence of packet pointer is mechanical; deciding capture posture is doctrine. |
| Suggested-account graphing on the retained humanized CDP surface | Code plus doctrine | Onboarding runner clicks visible creator `Followers`, waits for the visible relationship dialog, clicks that dialog's `Suggested` tab, and extracts only visible-dialog profile rows; visible `Suggested accounts` + exact `View All` is fallback only | Record the outer UI route separately from CloakBrowser `careful` pointer humanization and preserve `captured`, `visible_empty`, and `not_visible` distinctly before sibling-channel/link-hub work | Route precedence and source-visible outcome semantics are doctrine; action/receipt shape is mechanical. |
| Data-lake placement for packet-grade parent/suggested observations | Code plus doctrine | Existing packet writer; scan receipt and register validators check packet pointers when packet-grade is claimed | Preserve source packet first, then graph register points to packet | File/packet existence is mechanical; whether an observation is packet-grade is judgment. |
| No screenshots emitted to chat by default | Code plus doctrine | Scan receipt validator rejects screenshot chat output; doctrine still owns live chat behavior | Report compact receipt facts, not screenshot payloads | Receipt fields are mechanical; chat behavior is resident. |
| Suggested-account rows become frontier candidates, not registry identities | Doctrine plus register schema | Register validator built | Use tiktok_creator_discovery_frontier_register_v0 with weak edge types | Claim semantics are doctrine; allowed edge vocabulary is mechanical. |
| Suggested-account observed counts are receipt context, not exhaustive graph proof | Doctrine plus optional future schema | Doctrine now; receipt validator checks presence/non-negative only | If filtered, deduped, or intentionally under-sampled, record an accepted residual and do not claim exhaustive suggestion capture | Exact equality would be wrong for bounded scans; completeness is a semantic claim. |
| Edge type must not overclaim follower/following/endorsement/same creator | Code plus doctrine | Register validator built | Require allowed edge_type and required non_claims on every edge | Edge vocabulary/non_claims are mechanically checkable; truth remains doctrine. |
| Candidate next runs default to execution_authorized=false | Code | Register validator built | Reject any next_run_envelope where execution_authorized is true | Boolean gate is mechanical and load-bearing. |
| Same-run unbounded traversal forbidden | Code plus doctrine | Scan receipt validator requires caps and rejects candidate profile opens; live runner still future | Require caps and stop_condition; no candidate profile opens in the discovery scan | Caps are mechanical; live action authorization is doctrine/harness permission. |
| Suggested-list pagination | Code plus doctrine | Current onboarding runner performs no Suggested pagination; scan receipt retains a bound field for other explicitly authorized producers | Record the visible first surface only; no pagination is authorized in this route | The zero-pagination runtime posture is mechanical; any future expansion requires a separate bounded decision. |
| Follow/like/message or candidate-profile action | Code plus doctrine | Scan receipt validator requires zero follow/unfollow actions and zero candidate opens; onboarding route contains no Follow/like/message action | Never click Follow, open candidate profiles, like, message, or run an automated state-changing probe/retry | Account mutation is outside this discovery outcome and would create avoidable account risk. |
| Refresh failure handling: click Refresh once, record outcome | Code plus doctrine | Scan receipt validator caps refresh attempts at one and requires outcome vocabulary | If visible failure occurs, one refresh max; record clicked/outcome | Count/outcome fields are mechanical; identifying visible failure is source judgment. |
| Link hub proves identity evidence but not metrics | Doctrine plus registry schema | Existing registry/preflight doctrine; future checker can reject metric zero-fill | Use link hub for same-creator evidence only; metrics stay null/not_attempted | Meaning boundary is doctrine; null/no-zero fields can be checked. |
| No metric zero-fill from scanning/link hubs | Code | Register validator rejects metric fields in the frontier register | Reject metric fields in scan-frontier output; metric production stays in the metric lanes | Zero-fill is mechanically detectable and should fail closed. |
| Run Creator Registry exact-match preflight before insertion | Code plus doctrine | Existing preflight runner; insertion remains owner-gated | Run/check preflight and route exact hits as updates | Exact-match check is mechanical; insertion authorization is doctrine/current owner approval. |
| Region/country evidence must be source-backed or unknown | Doctrine plus future schema | Future validator can require evidence status/source fields | Mark unknown unless source-visible evidence exists | Source interpretation is judgment; evidence field presence is mechanical. |
| Cross-platform stitching requires link hub/reciprocal/official evidence | Doctrine plus registry linkage schema | Existing registry linkage doctrine; future checker can require match_basis | Do not promote username-similarity-only matches | Evidence sufficiency is judgment; basis field can be checked. |
| Registry/UI capture badges distinguish linked-only/profile/grid/metric/not-started | Code plus doctrine | Future projection/UI/schema work needed | Keep capture_status separate from identity linkage and metrics | Projection consistency is code; semantic separation is doctrine. |
| Discovery frontier graph is not a standing crawler/monitor/registry | Doctrine plus future CI/hook if runtime appears | Doctrine now | Do not add scheduler, dashboard, queue, graph DB, or standing service without owner decision | Detecting new runtime folders is partly placement/code; product boundary is doctrine. |
| Cold agent source-loading route | Doctrine | This artifact plus open_next headers | Open this artifact, frontier spec, MGT scanning model, TikTok capture spec, registry preflight usage | Source ordering is resident judgment aided by retrieval metadata. |

## Minimum Code Gates

The smallest useful code substrate is now implemented under
`forseti-harness/capture_spine/tiktok_creator_discovery_frontier/`: a register
validator, scan receipt validator, and network-free register writer. It checks
shape only:

1. Required wrapper, schema_version, register_id, provenance, nodes, edges,
   next_run_envelopes, non_claims.
2. Unique node_id and edge_id.
3. Edge endpoints point to known nodes.
4. Edge types are in the allowed vocabulary.
5. Required non_claims are present on register, nodes, edges, and envelopes.
6. Every next_run_envelope has `execution_authorized: false`.
7. Caps, exclusions, stop_condition, source_policy_posture, and prior register
   pointer are present.
8. Metric fields are absent, or if later added, cannot be zero-filled when status
   is not_attempted/not_available.
9. Registry insertion/update fields are absent from the frontier register.
10. Packet pointer fields are present when the register claims packet-grade
    observation.
11. Scan receipts record caps, extraction method, refresh outcome, pagination
    bound, browser-close posture, zero candidate opens, zero follow/unfollow
    actions, and no screenshots.
12. CloakBrowser parent-grid receipts cannot leave suggested-account capture as
    not-started/deferred/skipped; they must record attempted, blocked, or empty outcome.
13. The register writer emits weak candidate nodes/edges and unauthorized
    next-run envelopes from validated receipt input.

The validator should not decide whether a creator is on-niche, whether a region
claim is true, whether an identity match is sufficient, or whether a next frontier
is worth scanning. Those stay doctrine/resident judgment.

## Cold-Agent Procedure

1. Read AGENTS.md and .agents/workflow-overlay/README.md.
2. Read this artifact, then the frontier register spec and MGT scanning model.
3. Identify the intended browser/session and current owner authorization. On
   first CDP capture, adopt the latest enumerated non-closed TikTok page even
   when it shows another creator/path; never adopt a cross-platform page, and
   create one only when no TikTok page exists. Never infer focus.
4. If entering a TikTok seed profile, capture or cite a parent platform packet.
5. Click the visible creator `Followers` count, wait for the visible relationship
   dialog, click that dialog's `Suggested` tab, and extract profile rows only from
   that visible dialog.
6. Only when that primary route is not visible, use the visible `Suggested
   accounts` heading and exact `View All` route as fallback. Preserve `captured`,
   `visible_empty`, or `not_visible` truthfully before link-hub or sibling-channel
   work. Never click Follow, open a candidate, like, or message.
7. Keep the acquired page through modal close, grid collection, and all selected
   video captures. Do not reload an already matching creator path or click Latest,
   Popular, or Oldest. After the 8-13 second wait, open each selected video by
   randomly clicking a currently viewport-visible selected grid tile, capture the
   matching overlay, and close back to the grid. If selected tiles are not visible,
   use only bounded normal-grid viewport pagination; never target-scroll a tile.
   If a click does not materialize the matching overlay, wait 60 seconds,
   recompute, and retry once, then stop loudly. Never fall back to direct-video
   navigation. Preserve available grid/API, URL, overlay DOM, comment-response,
   and subtitle-track evidence with provenance; direct `itemStruct` is optional.
8. Record suggested accounts as weak discovery frontier nodes/edges only.
9. Use the receipt-backed register writer, or manually write/update the frontier
   register to the same schema; leave all next-run envelopes unauthorized.
10. If emitted candidate nodes are filtered, deduped, or otherwise a subset of
   observed suggestions, record that residual and do not claim exhaustive
   suggestion capture.
11. Run/check Creator Registry exact-match preflight before any registry proposal.
12. Report compact receipt facts, not screenshots, and state non-verified items.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    TikTok creator discovery makes the visible Followers relationship dialog's
    Suggested tab primary and keeps visible Suggested accounts plus exact View All
    as fallback. Retained CDP now adopts the latest TikTok page at platform scope,
    suppresses same-path reloads, preserves one-page Suggested-to-grid continuity,
    and opens every selected video through a random currently visible selected
    grid tile, returning to the grid after each overlay. Bounded normal-grid
    pagination is allowed only to expose selected tiles; targeted tile scrolling
    and direct-video onboarding navigation are forbidden. One 60-second retry is
    allowed only after failed matching-overlay materialization. Grid/API, URL,
    overlay DOM, comment-response, and subtitle-track evidence are preserved with
    provenance while direct `itemStruct` remains optional. Account mutation and
    candidate opens remain forbidden, with truthful outcome and provenance receipts.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - validation_philosophy
  controlling_sources_updated:
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
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
        Project-wide authority, source loading, DCP, validation, and lifecycle rules
        did not change; this is a TikTok product/source-family precedence change.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        The existing TikTok Scanning and source-capture routes still resolve the
        same controlling sources; no owner or path family moved.
  stale_language_search: >
    rg -n -i "first deep entry|remaining selected videos|direct selected-video|source item detail|adopt_exact_target_else_create|arbitrary TikTok tab|profile suggested|View all.*Following|View all.*Followers|root follow|owner-authorized root follow|allows one.*follow"
    forseti/product/spines/scanning/source_families/tiktok forseti-harness/docs/source_capture_agent_runbook.md
    forseti-harness/source_capture/tiktok forseti-harness/capture_spine/tiktok_creator_discovery_frontier
  non_claims:
    - not validation
    - not readiness
    - not live capture success
    - not Creator Registry mutation or identity proof
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    TikTok creator discovery scan behavior is now classified by enforcement
    placement: shape/output/run-envelope constraints belong in validators, the
    receipt-backed register writer, or existing packet/preflight runners, while
    source-access posture, claim semantics, identity evidence sufficiency, owner
    authorization, count/completeness interpretation, and frontier judgment
    remain doctrine. Cold agents get a source-loading route plus a concrete
    code gate list before further scouting.
  trigger: validation_philosophy
  related_triggers:
    - workflow_authority
    - product_doctrine
  controlling_sources_updated:
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md
    - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
    - docs/review-inputs/creator_graphing_scan_behavior_notes_20260707.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/artifact-folders.md
    - forseti/product/spines/scanning/README.md
    - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        This pass adds lane-local receipt/register code only; no new hook, CI
        gate, or global validation rule is implemented.
    - path: .agents/hooks/
      reason: >
        The user asked to determine code-vs-doctrine placement before more
        scouting, not to build the validator/hook substrate in this pass.
    - path: forseti-harness/runners/
      reason: >
        No live runner implementation is authorized by this classification
        artifact; the receipt/register substrate exists under capture_spine
        only.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not live TikTok access authorization
    - not Creator Registry insertion authorization
    - not proof that hook or runner exists
```

## Non-Claims

Not validation, readiness, implementation, code review, live capture success,
source-access authorization, registry mutation, identity proof, metric proof, or
production graph infrastructure authorization.
