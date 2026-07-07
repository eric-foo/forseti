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
  - A TikTok creator discovery validator, hook, or runner lands and supersedes the future-code rows here.
  - Creator Registry adopts a typed weak-edge/discovery frontier intake lane.
  - TikTok capture posture changes source-access or session requirements for suggested-account scans.
```

## Status

Status: `ENFORCEMENT_PLACEMENT_CLASSIFIED_NOT_BUILT`.

This artifact classifies enforcement placement only. It does not implement hooks,
validators, runners, registry writes, capture execution, or live platform access.
A cold agent must use it to decide what to check mechanically before closeout and
what to preserve as resident doctrine during the scan.

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
| Use intended warmed browser/session; do not close it at lane end | Doctrine/runbook | Doctrine only | State intended surface and leave it open unless owner asks otherwise | Session choice and operator intent are live-context judgment. |
| Avoid duplicate/wrong ordinary Chrome TikTok tabs | Doctrine/runbook | Doctrine only | Verify active surface; avoid reading from wrong tab | Mechanical detection is environment-specific; current safest form is operator checklist. |
| Parent platform profile/grid capture when entering seed profile | Code plus doctrine | Future runner/validator needed | Require a parent profile/grid packet pointer or explicit not-captured reason in the register | Presence of packet pointer is mechanical; deciding capture posture is doctrine. |
| Data-lake placement for packet-grade parent/suggested observations | Code plus doctrine | Existing packet writer; future register validator should require packet pointer when packet-grade | Preserve source packet first, then graph register points to packet | File/packet existence is mechanical; whether an observation is packet-grade is judgment. |
| No screenshots emitted to chat by default | Doctrine; optional code for artifacts | Doctrine now; future checker can reject screenshot paths in chat-facing receipts if formalized | Report compact receipt facts, not screenshot payloads | Chat behavior is resident; artifact byte policy can later be checked. |
| Suggested-account rows become frontier candidates, not registry identities | Doctrine plus register schema | Spec now; future validator should restrict edge types/non_claims | Use tiktok_creator_discovery_frontier_register_v0 with weak edge types | Claim semantics are doctrine; allowed edge vocabulary is mechanical. |
| Edge type must not overclaim follower/following/endorsement/same creator | Code plus doctrine | Future validator needed | Require allowed edge_type and required non_claims on every edge | Edge vocabulary/non_claims are mechanically checkable; truth remains doctrine. |
| Candidate next runs default to execution_authorized=false | Code | Future validator needed | Reject any next_run_envelope where execution_authorized is true | Boolean gate is mechanical and load-bearing. |
| Same-run unbounded traversal forbidden | Code plus doctrine | Future runner cap/validator needed | Require caps and stop_condition; no candidate profile opens unless current owner launch authorizes it | Caps are mechanical; live action authorization is doctrine/harness permission. |
| Bounded Suggested tab pagination only with explicit bound | Code plus doctrine | Future runner/receipt validator needed | Record pagination bound used; if absent, treat as no pagination authorized | Bound presence is mechanical; deciding bound is operator judgment. |
| Do not follow/unfollow to force recommendations | Doctrine plus future action receipt | Doctrine now; future runner can record/forbid action flag | Do not perform follow/unfollow during discovery scans unless a separate owner action authorizes it | Live UI action semantics are posture/judgment; receipt flags can be checked. |
| Refresh failure handling: click Refresh once, record outcome | Code plus doctrine | Future runner receipt validator needed | If visible failure occurs, one refresh max; record clicked/outcome | Count/outcome fields are mechanical; identifying visible failure is source judgment. |
| Link hub proves identity evidence but not metrics | Doctrine plus registry schema | Existing registry/preflight doctrine; future checker can reject metric zero-fill | Use link hub for same-creator evidence only; metrics stay null/not_attempted | Meaning boundary is doctrine; null/no-zero fields can be checked. |
| No metric zero-fill from scanning/link hubs | Code | Future registry/register validator needed | Reject metric fields set to 0 when status is not_attempted/not_available | Zero-fill is mechanically detectable and should fail closed. |
| Run Creator Registry exact-match preflight before insertion | Code plus doctrine | Existing preflight runner; insertion remains owner-gated | Run/check preflight and route exact hits as updates | Exact-match check is mechanical; insertion authorization is doctrine/current owner approval. |
| Region/country evidence must be source-backed or unknown | Doctrine plus future schema | Future validator can require evidence status/source fields | Mark unknown unless source-visible evidence exists | Source interpretation is judgment; evidence field presence is mechanical. |
| Cross-platform stitching requires link hub/reciprocal/official evidence | Doctrine plus registry linkage schema | Existing registry linkage doctrine; future checker can require match_basis | Do not promote username-similarity-only matches | Evidence sufficiency is judgment; basis field can be checked. |
| Registry/UI capture badges distinguish linked-only/profile/grid/metric/not-started | Code plus doctrine | Future projection/UI/schema work needed | Keep capture_status separate from identity linkage and metrics | Projection consistency is code; semantic separation is doctrine. |
| Discovery frontier graph is not a standing crawler/monitor/registry | Doctrine plus future CI/hook if runtime appears | Doctrine now | Do not add scheduler, dashboard, queue, graph DB, or standing service without owner decision | Detecting new runtime folders is partly placement/code; product boundary is doctrine. |
| Cold agent source-loading route | Doctrine | This artifact plus open_next headers | Open this artifact, frontier spec, MGT scanning model, TikTok capture spec, registry preflight usage | Source ordering is resident judgment aided by retrieval metadata. |

## Minimum Future Code Gates

If this lane repeats, the smallest useful code substrate is a JSON validator for
`tiktok_creator_discovery_frontier_register_v0`. It should check shape only:

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

The validator should not decide whether a creator is on-niche, whether a region
claim is true, whether an identity match is sufficient, or whether a next frontier
is worth scanning. Those stay doctrine/resident judgment.

## Cold-Agent Procedure

1. Read AGENTS.md and .agents/workflow-overlay/README.md.
2. Read this artifact, then the frontier register spec and MGT scanning model.
3. Identify the intended browser/session and current owner authorization.
4. If entering a TikTok seed profile, capture or cite a parent platform packet
   before graphing extracted candidates.
5. Record suggested accounts as weak discovery frontier nodes/edges only.
6. Write or update a frontier register; leave all next-run envelopes unauthorized.
7. Run/check Creator Registry exact-match preflight before any registry proposal.
8. Report compact receipt facts, not screenshots, and state non-verified items.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    TikTok creator discovery scan behavior is now classified by enforcement
    placement: shape/output/run-envelope constraints belong in future validators
    or existing packet/preflight runners, while source-access posture, claim
    semantics, identity evidence sufficiency, owner authorization, and frontier
    judgment remain doctrine. Cold agents get a source-loading route plus a
    concrete future-code gate list before further scouting.
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
        This pass classifies lane-local enforcement placement only; no new hook,
        CI gate, or global validation rule is implemented.
    - path: .agents/hooks/
      reason: >
        The user asked to determine code-vs-doctrine placement before more
        scouting, not to build the validator/hook substrate in this pass.
    - path: forseti-harness/
      reason: >
        No runner or validator implementation is authorized by this classification
        artifact; future-code gates are named for later bounded build work.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not live TikTok access authorization
    - not Creator Registry insertion authorization
    - not proof that future validators exist
```

## Non-Claims

Not validation, readiness, implementation, code review, live capture success,
source-access authorization, registry mutation, identity proof, metric proof, or
production graph infrastructure authorization.
