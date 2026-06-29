# Channel-Neutral Creator Identity/Profile Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca architecture-planning prompt
scope: >
  Cross-recipient architecture prompt for deciding the channel-neutral v0
  creator identity/profile spine: any supported public channel may seed a
  platform-account subject, cross-platform creator records require linkage
  evidence, and creator_profile_current must support both single-platform
  observed accounts and linked creator clusters without making YouTube,
  Instagram, or TikTok the authority.
use_when:
  - Commissioning a read-only architecture planning pass before patching the creator ledger/profile contracts.
  - Testing whether the current YouTube-first observation work should be generalized into a channel-neutral account-first spine.
  - Applying Mini God Tier plus Smallest Complete Intervention to the creator identity/profile boundary.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - The creator observation, public-handle linkage, creator profile current view, or Creator Signal surface contracts are superseded.
  - Orca adopts a runtime database/schema for creator identity/profile storage.
  - A later owner decision changes the public-handle linkage evidence threshold or person-identity boundary.
source_base_revision: codex/creator-ledger-static-fixture @ f7d8de6381d0ec0b9ef926cd275127830a7f6036
checkout_requirement: >
  Strict repo-read claims require a checkout containing the named source base
  or a descendant/equivalent revision. If the creator-ledger files are absent,
  classify the checkout as missing the PR-backed source and return
  NEEDS_SOURCE_CONTEXT rather than substituting older main-branch sources.
```

## Orca Prompt Preflight

```yaml
output_mode: file-write for this prompt artifact; paste-ready-chat copy for the courier
prompt_artifact_path: docs/prompts/architecture/channel_neutral_creator_identity_profile_architecture_prompt_v0.md
receiver_output_mode: chat-only architecture report unless the owner explicitly asks for a filed architecture artifact
receiver_write_permission: read-only; no source edits, no ledger rows, no migration, no implementation
template_kind: full-prompt; architecture-planning style; no runtime-model routing
edit_permission_targets_branch: >
  Receiver is read-only. Prompt was authored on a branch derived from
  codex/creator-ledger-static-fixture at f7d8de6381d0ec0b9ef926cd275127830a7f6036.
reviews: not a review prompt; do not emit formal review findings or verdicts
doctrine_change: >
  Receiver may recommend a later architecture-doctrine patch, but this prompt
  itself changes no doctrine. Any accepted patch to creator identity/profile
  contracts must carry the required Orca direction-change propagation.
destinations: >
  Receiver returns a chat architecture report for owner/Codex adjudication.
  No durable output path is required unless separately requested.
```

## Task

You are performing a read-only architecture planning pass for Orca's creator
identity/profile spine.

The owner correction to test is:

```text
Do not make YouTube the authority.
The creator/profile spine should be able to start from any supported public channel.
```

Decide the smallest complete v0 architecture that preserves that correction.

The target is **Mini God Tier plus Smallest Complete Intervention**:

- Capture most of the useful creator-intelligence value now: one-stop profile
  readiness, aggregate influence later, public account linkage, and source
  drill-back.
- Keep the intervention small: no database migration, dashboard, live capture,
  one giant ledger, or person identity graph unless the sources force it.
- Name accepted residuals: what remains below maximal "god tier", why that is
  acceptable now, what risk remains, and what would trigger an upgrade.

## Source Read Contract

If you have repo/filesystem access, first read the required sources below.
Declare exactly one:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

If a listed creator-ledger file is missing, do not infer that Orca rejected the
contract. First check whether the checkout lacks the PR-backed source base named
above. If so, set `SOURCE_CONTEXT_INCOMPLETE` and state that strict claims need
the PR-backed source.

Do not browse the web. Do not use external identity-resolution best practices as
authority. This is an Orca-local architecture decision over public account
surfaces and current ledger/profile contracts.

## Required Reads

Authority and method:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`

Task sources:

- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

Optional, only if they could change the recommendation:

- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json`
- `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`
- `orca-harness/capture_spine/youtube_creator_observation/validation.py`
- `orca-harness/tests/unit/test_creator_public_handle_linkage.py`
- `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py`

## Method Sequencing

1. Run Orca Cynefin routing from `.agents/workflow-overlay/decision-routing.md`.
2. REFERENCE-LOAD `workflow-architecture-planning` if available. Do not APPLY it yet.
3. SOURCE-LOAD the required reads.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY architecture planning in `standard` profile.
6. Use local directional, adversarial, and grounding perspectives unless the owner
   separately authorizes subagents.

Each advisory perspective must stay planning-only and return this terse schema:

```text
perspective:
recommended_core:
strongest_reason:
strongest_risk:
channel_neutrality_position:
identity_linkage_position:
profile_subject_position:
mgt_residual_to_accept_or_reject:
not_proven:
source_cites:
```

## Architecture Question

Answer this exact architecture question:

```text
What is the channel-neutral v0 creator identity/profile architecture that lets
Instagram, TikTok, YouTube, or another supported public channel seed a profile
without claiming cross-platform creator identity until linkage evidence exists?
```

Do not answer the easier YouTube-specific question.

## Options To Compare

Compare these options at minimum:

1. **YouTube-first authority.** YouTube observation rows become the first-class
   creator/profile subjects; other platforms attach later.
2. **Per-platform observation ledgers only.** Each platform keeps its own
   observation ledger; no shared account/profile subject exists yet.
3. **Channel-neutral platform-account core.** Any platform observation can mint
   or update a `platform_account_id`; profile/current views can target either a
   single `platform_account` or a linked `creator_record`.
4. **Public-handle linkage first.** `creator_record_id` is the only creator
   profile subject; single-platform accounts wait until cross-platform linkage.
5. **SQLite/identity graph now.** Move immediately to a database or identity graph
   that stores account nodes, edges, evidence, rollups, and current profiles.

You may add a hybrid only if it materially changes the recommendation.

## Required Decisions

Answer these directly:

- What is the seed object when only one channel is known: `platform_account`,
  `creator_record`, `creator_observation`, or another subject?
- Can a creator profile current view exist before cross-platform linkage? If yes,
  what must it be called so it does not overclaim?
- Should `creator_profile_current` use:
  - `profile_subject_kind: platform_account | creator_record`, and
  - `profile_subject_id`, rather than only `creator_record_id`?
- What field or state distinguishes:
  - `single_platform_observed`
  - `cross_platform_candidate`
  - `probable_public_account_link`
  - `declared_public_account_link`
  - `rejected_public_account_link`
- Where do average views, engagement rate, cadence, velocity, and other aggregate
  influence metrics attach before and after cross-platform linkage?
- How do metric rollups avoid double-counting when a single-platform account later
  merges into a linked creator cluster?
- What is the minimum channel-neutral account observation contract needed so
  Instagram/TikTok/YouTube can all feed the same spine without making any one
  platform authoritative?
- What remains in platform-specific source-family ledgers?
- What remains in the public-handle linkage ledger?
- What belongs in the derived current profile view?
- What must remain forbidden because it would create a real-world identity graph,
  contact surface, person dossier, audience graph, or public creator directory?
- What accepted residuals make this MGT instead of overbuilt maximal
  infrastructure?
- What would trigger a later SQLite/database upgrade?

## Expected Starting Bias, Not A Forced Answer

The likely correct answer is option 3:

```text
Channel-neutral platform-account core.

Any source family may produce platform-account observations.
A profile can initially be a single-platform observed account.
A creator_record is minted only when linkage evidence joins at least two platform accounts.
creator_profile_current supports both subject kinds.
Metrics first attach to platform_account_id, then may roll up to creator_record_id
only after linkage state and deduplication rules permit it.
```

You may disagree, but only if the loaded sources give a stronger reason.

Push back hard on these failure modes:

- YouTube silently becomes the identity authority because the first real fixture is YouTube.
- `creator_record_id` is required too early, forcing single-platform rows into cross-platform identity.
- The current profile surface cannot show useful single-platform creator intelligence.
- Metric rollups are keyed only to `creator_record_id`, making pre-linkage metrics homeless.
- A future merge creates double-counted influence because platform-level rollups were not separable.
- LLM-assisted matching finalizes creator linkage without human review and non-LLM evidence.

## MGT / SCI Criteria

Mini God Tier target:

- One usable current-profile architecture for public creator/account intelligence.
- Channel-neutral seeding from any supported platform.
- Clear path to aggregate influence and ideal-audience display.
- Explicit identity non-claims and source drill-back.
- Named accepted residuals.

Smallest Complete Intervention:

- Prefer docs/spec contract changes over runtime migration.
- Prefer an account-first bridge over a full identity graph.
- Prefer table-shaped/static rows that can map to SQLite later.
- Do not build capture, rollup jobs, dashboard UI, validators, or database tables
  unless the architecture pass proves they are the smallest complete next step.

Accepted residuals must include, at minimum:

- no automatic cross-platform final identity;
- no SQLite/runtime storage yet;
- no live metric rollup computation yet;
- no dashboard implementation yet;
- no real-world identity, contact, or audience-member graph;
- source gaps for TikTok/IG/YouTube parity if the current sources are uneven.

For each residual, state:

- what remains undone;
- why that is acceptable now;
- what risk remains;
- what evidence or owner decision would trigger the upgrade.

## Output Contract

Return a concise architecture report with exactly these headings:

1. `SOURCE_CONTEXT`
2. `CYNEFIN_ROUTING`
3. `ARCHITECTURE_RESULT` - one of `TARGET_RECOMMENDED`, `OPTIONS_COMPARED_NO_SELECTION`, `NEEDS_SOURCE_CONTEXT`, `NEEDS_OWNER_DECISION`, `DEFER_OR_REJECT`, `AUTHORITY_BLOCKED`
4. `ONE_SCREEN_RECOMMENDATION`
5. `OPTION_COMPARISON`
6. `TARGET_ARCHITECTURE`
7. `CORE_OBJECTS_AND_INVARIANTS`
8. `CHANNEL_NEUTRAL_SEED_CONTRACT`
9. `PROFILE_SUBJECT_MODEL`
10. `IDENTITY_LINKAGE_MODEL`
11. `METRIC_AND_ROLLUP_ATTACHMENT`
12. `CORE_VS_SATELLITE`
13. `MGT_ACCEPTED_RESIDUALS`
14. `SCI_CUTS_AND_DEFERRED_WORK`
15. `FORBIDDEN_PATHS_AND_FAKE_SUCCESS`
16. `CONTRACT_PATCH_GUIDANCE`
17. `WHAT_WOULD_CHANGE_THE_ANSWER`
18. `NON_CLAIMS`

For `CONTRACT_PATCH_GUIDANCE`, do not write a patch. Give the smallest later
docs patch target list and the exact contract changes to consider.

## Forbidden Outputs

Do not produce:

- code;
- migration scripts;
- database schema execution;
- real creator rows;
- capture authorization;
- live social-platform scraping instructions;
- dashboard implementation;
- lead-list, contact, outreach, legal-name, demographic, follower-graph, or
  audience-member modeling;
- buyer-proof, validation, readiness, or implementation-start claims;
- a claim that YouTube, Instagram, TikTok, or an LLM is the authority for creator identity.

## Non-Claims

This prompt does not validate or approve the architecture. It does not authorize
source edits, implementation, runtime storage, SQLite migration, live capture,
metric rollup computation, dashboard construction, creator-row population, or
public person-level product surfaces.
