# Creator Public-Handle Linkage Ledger Spec v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_spec
scope: >
  Dedicated linkage spec for Tier-2-B public-handle-to-public-handle creator
  account joins across Instagram, TikTok, and YouTube. Defines the static
  table-shaped ledger contract and validator expectations for public account
  linkage only. This is not capture machinery, not a crawler, not SQLite, not
  a person identity service, and not a contact or outreach surface.
use_when:
  - Designing or reviewing public creator account linkage across IG, TikTok, and YouTube.
  - Checking the evidence threshold for declared, probable, candidate, or rejected public-handle links.
  - Validating a static creator public-handle linkage fixture before any database migration.
open_next:
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
  - orca-harness/capture_spine/creator_public_handle_linkage/validation.py
stale_if:
  - Wind-caller Tier-2-B public-handle stitching authorization changes.
  - Non-public-handle joins, contact data, audience/follower graphs, or person-level product surfaces are authorized elsewhere.
  - The ledger moves from static files/fixtures to SQLite or another database schema.
  - The validator's schema version or accepted link-state vocabulary changes.
authority_boundary: retrieval_only
```

## Status

This is the dedicated public-handle linkage spec requested by the current
wind-caller carve-out. The controlling decision says Tier-2-B public-handle
stitching is activated for public-handle-to-public-handle joins, while
non-public-handle joins remain gated and Tier-3 exclusions remain absolute.

This spec does not populate any real creator rows. The first implementation
uses a synthetic fixture and validator so the linkage semantics can be tested
hard before promoting the shape to SQLite or a runtime store.

## Source Reconciliation

Fresh source read on current main:

- `docs/decisions/wind_caller_calibration_carveout_v0.md` says Tier-2-B
  cross-platform PUBLIC-handle stitching is activated for
  public-handle-to-public-handle joins and must build through a dedicated
  linkage spec.
- `ig_creator_roster_frontier_ledger_spec_v0.md` points to that carve-out and
  lifts the old cross-platform stitching forbiddance only for public-handle
  joins.
- Older future-exploration language that says Tier-2-B is deferred is
  superseded for public-handle joins only. It still describes the residual
  risk for non-public-handle joins and audience/follower graph work.

## Ledger Shape

Use a static table-shaped ledger first:

- `creator_records`: ledger-local public account clusters.
- `platform_accounts`: one row per public platform account.
- `account_link_evidence`: append-only evidence rows supporting or defeating a
  proposed account link.

The ledger is intentionally relational even when stored as JSON. SQLite can
come later by mapping each list to a table without changing the core contract.

## Creator Record Contract

`creator_record_id` is a ledger-local public account cluster id. It is not proof
of real-world identity and must not be exposed as a person identity claim.

Required fields:

```yaml
creator_record:
  creator_record_id: required stable ledger-local id
  link_state: required enum
  platform_account_ids: required list of at least two account ids across at least two platforms
  evidence_ids: required list of supporting or defeating evidence ids
  review_state: required enum
  link_rationale: required short reason
  limitations: required short limitation note
  created_at: required timestamp
  updated_at: required timestamp
  non_claims: required list
```

Allowed `link_state` values:

- `declared_public_account_link`: a public source declares or mutually links
  the accounts.
- `probable_public_account_link`: no declaring source, but at least three
  independent weak public evidence families point the same way and a human
  reviewer accepts the probability.
- `candidate_public_account_link`: interesting but not final.
- `rejected_public_account_link`: preserved rejected link with disconfirming
  evidence.

Do not use `confirmed_public_account_link`. The ledger should not claim
certainty about a person behind the accounts.

## Platform Account Contract

Required fields:

```yaml
platform_account:
  platform_account_id: required ledger-local account id
  platform: required enum instagram, tiktok, youtube
  platform_public_account_id_or_none: nullable public platform id
  public_handle: required normalized public handle, stored without "@"
  public_profile_url: required public profile URL
  handle_source_pointer: required source pointer
  handle_observed_at: required timestamp
  public_display_name_or_none: nullable public display-name cache
  display_name_source_pointer_or_none: required if display name is stored
  display_name_source_field_or_none: required if display name is stored
```

Only public account-surface fields are allowed. Contact fields, real/legal
names, exact location, demographic/person attributes, follower lists, audience
graphs, private handles, session state, raw HTML, screenshots, and downstream
ECR/Cleaning/Judgment outputs are forbidden.

## Evidence Contract

Required fields:

```yaml
account_link_evidence:
  evidence_id: required stable evidence id
  evidence_type: required enum
  evidence_strength: required enum strong, weak, disconfirming
  account_ids: required list of at least two platform_account ids
  source_pointer: required pointer
  source_field: required source field
  observed_at: required timestamp
  review_actor: required non-empty actor id
  llm_assisted: required boolean
  independence_key: required evidence-family key
  notes: optional short note
```

Strong evidence types:

- `self_declared_cross_link`
- `mutual_profile_link`
- `official_link_hub`

Weak evidence types:

- `handle_similarity`
- `public_display_name_similarity`
- `bio_text_overlap`
- `shared_public_link_destination`
- `content_topic_overlap`

Disconfirming evidence types:

- `conflicting_self_declaration`
- `conflicting_public_link_hub`
- `different_public_entity_signal`
- `operator_rejected_match`

LLMs may assist review, but an LLM-only evidence bundle must not finalize a
declared or probable link. Final links require human review and at least one
non-LLM-assisted evidence row.

## Validator Contract

The v0 validator must fail closed on:

- unknown top-level, creator-record, account, or evidence fields;
- missing source pointers for handles or display names;
- any legal name, inferred real name, contact, private, demographic, audience
  graph, follower graph, raw capture, session, or downstream-stage field;
- a creator record that links only one platform;
- a declared link with no strong public evidence;
- a probable link with fewer than three independent weak evidence types;
- any declared/probable link that includes disconfirming evidence;
- any final link whose evidence is LLM-only;
- `confirmed_public_account_link` wording;
- synthetic fixtures that contain real-looking handles, non-`example.test`
  profile URLs, or non-synthetic source pointers.

## Non-Claims

This spec is not:

- a database build;
- SQLite adoption;
- runtime capture authorization;
- live IG, TikTok, or YouTube capture authorization;
- a person identity graph;
- legal-name, real-name, contact, audience-graph, follower-graph, or outreach
  authorization;
- a public person-level product surface;
- buyer proof, validation, readiness, or commercial-scale authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - output_authority
    - lifecycle_boundary
  doctrine_changed: >
    Adds the dedicated Tier-2-B public-handle linkage spec required by the
    wind-caller carve-out and binds the first implementation to a static
    table-shaped ledger plus validator before any SQLite/runtime promotion.
  controlling_sources_updated:
    - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
    - orca-harness/capture_spine/creator_public_handle_linkage/
    - orca-harness/tests/unit/test_creator_public_handle_linkage.py
    - orca-harness/tests/fixtures/creator_public_handle_linkage/valid_synthetic_ledger.json
  downstream_surfaces_checked:
    - docs/decisions/wind_caller_calibration_carveout_v0.md
    - orca/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md
    - orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - orca/product/spines/capture/core/source_capture_toolbox/README.md
  intentionally_not_updated:
    - path: orca/product/spines/capture/core/source_families/social_media/tiktok/
      reason: No TikTok-specific capture behavior changes; this is a cross-platform public-handle ledger contract.
    - path: orca/product/spines/capture/core/source_families/social_media/youtube/
      reason: No YouTube-specific capture behavior changes; this is a cross-platform public-handle ledger contract.
  stale_language_search: >
    rg -n "cross-platform public-handle stitching|confirmed_public_account_link|creator_public_handle_linkage"
    docs orca orca-harness -g "*.md" -g "*.py" -g "*.json"
  non_claims:
    - not real-world identity proof
    - not non-public-handle join
    - not contact or outreach authorization
    - not follower or audience graph
    - not public person-level product surface
    - not SQLite migration
    - not runtime capture authorization
    - not validation or readiness
```

