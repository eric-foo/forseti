# Creator Registry GT Roadmap v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_roadmap
scope: >
  Registry-adjacent roadmap from the Creator Ledger Mini God Tier operating
  shape toward a fuller God Tier creator-memory system. Defines what to
  optimize for, what graphing/scanning may do now, and which next capabilities
  should stay additive rather than forcing remigration.
use_when:
  - Planning Creator Registry scanning, graphing, or creator-discovery expansion.
  - Deciding whether a creator graph can treat accounts as the same person.
  - Choosing the next Creator Ledger proof loop after the Mini God Tier slice.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
  - docs/workflows/creator_ledger_first_operational_proof_checkpoint_v0.md
  - docs/workflows/creator_ledger_known_account_preflight_checkpoint_v0.md
  - docs/workflows/creator_ledger_observation_sibling_checkpoint_v0.md
  - docs/workflows/creator_ledger_additive_upgrade_intake_rehearsal_v0.md
stale_if:
  - Creator Registry no longer owns known-account preflight for public social creators.
  - Creator Ledger adopts a successor graph, runtime storage, or identity-linking contract.
  - God Tier or Mini God Tier doctrine changes the efficacy/non-claim boundary.
```

## Current State

The Creator Ledger Mini God Tier slice is operational as a bounded creator-memory
system:

- public scans can produce candidate rows;
- candidate rows must clear exact-match preflight before `new_capture` handoff;
- known exact accounts block duplicate `new_capture`;
- exact-unmatched rows can clear row-by-row;
- repeat observations have an additive sibling path;
- metrics, rollups, linkage, audience snapshots, profile-current, and Creator
  Signal interpretation have named owning layers; and
- `creator_profile_current` remains a generated read model, not source truth.

This is enough to start bounded scanning and graph-planning. It is not yet a
full creator graph, crawler, capture system, outreach system, buyer-proof
surface, or cross-platform person-identity graph.

## Optimize For

Optimize the Creator Registry and its graphing work for creator-memory efficacy:

- **avoid duplicate work**: known exact accounts block duplicate capture;
- **increase useful recall**: scans surface plausible public creator accounts
  without losing known-account orientation;
- **preserve source drill-back**: every useful edge or row points to the public
  source, capture packet, receipt, observation, or review state that created it;
- **separate evidence from claims**: public links and handle matches are evidence,
  not person identity proof until promoted under the linkage contract;
- **keep missingness explicit**: absent metrics, absent audience snapshots, no
  capture attempt, out-of-window values, and unverified links stay visible;
- **route upgrades additively**: graph edges, observations, metric facts,
  audience snapshots, and generated views attach beside existing rows;
- **make operator decisions easier**: the next lane should know whether to
  capture new, update existing, investigate a candidate link, or do nothing; and
- **promote mechanical checks only when they pay rent**: add validators when a
  repeated failure class appears, not as audit surface for its own sake.

Do not optimize first for artifact count, audit density, dashboard polish, or
large schema adoption. Those are support functions.

## Scanning Readiness

Bounded public scanning is allowed under the current MGT shape when it stays in
the scan-to-preflight-to-handoff lane:

```text
public/no-login scan
-> candidate rows
-> exact-match preflight receipt
-> capture-request handoff rows only for new_candidate / allowed / can_start_new_capture true
```

Scanning must not:

- run capture;
- mutate the registry;
- write Silver;
- refresh metrics;
- claim source adequacy for the whole niche;
- claim fuzzy duplicate detection; or
- claim cross-platform person identity.

The next practical scan batches should vary platform and niche while preserving
small caps, receipt paths, source-read counts, and explicit non-claims.

## Graphing Readiness

Graphing is ready at the account/evidence layer, not the person-truth layer.

The first graph should represent:

- platform account nodes;
- public handle / URL / channel-id evidence nodes;
- scan candidate nodes;
- preflight receipt rows;
- observation sibling rows;
- metric observation and rollup nodes when source-backed;
- audience snapshot nodes when source-backed;
- linkage-review edges with states such as `candidate`, `soft_link`,
  `rejected_link`, and `promoted_link`; and
- generated profile-current nodes or projections that point back to siblings.

The first graph should not represent:

- "same real person" as truth;
- buyer fit as truth;
- outreach readiness;
- private identity;
- inferred demographics without the owning audience-snapshot layer; or
- metric zeros for missing values.

## Graph Shape Hypothesis

Use per-platform subgraphs first, then a cross-platform linkage overlay:

1. **YouTube account graph**: channel ids, handles, scan candidates, observations,
   RSS/watch/capture packet refs, metric observations, and rollups.
2. **Instagram account graph**: public handles, profile URLs, grid/reel packet
   refs, metric seeds/rollups, and audience/profile evidence when available.
3. **TikTok account graph**: public handles, profile URLs, video packet refs,
   metric seeds/rollups, and missingness.
4. **Cross-platform linkage overlay**: public links found on profiles,
   same-handle candidates, self-declared social links, rejected candidates, and
   promoted account clusters.

This keeps the graph useful before cross-platform identity is proven. A creator
can appear as multiple platform accounts until linkage evidence is promoted.

## Exploration Strategy

Use one account as a public-source expansion seed only when the expansion stays
evidence-bound:

1. Start from an existing or newly scanned public account.
2. Read only public/no-login profile surfaces, visible bio text, source-visible
   location/self-description text, and explicitly visible social links.
3. If the known account profile links to an official public link hub, follow only the
   source-visible public hub links needed to identify sibling public accounts.
4. Convert discovered social links into candidate account rows, not registry
   mutations.
5. Run exact-match preflight per candidate row.
6. If the candidate is known, attach the discovery as linkage or observation
   evidence.
7. If the candidate is new, emit a handoff row only when the preflight receipt
   clears `new_capture`.
8. If the candidate may belong to the same public creator, add candidate-link
   review evidence; do not collapse accounts.

For creator channel graphing, the default probe sequence is platform-agnostic:

```text
known public creator account -> public profile bio/about/channel links
-> official public link hub, if present -> sibling public channel links
-> candidate account rows -> Creator Registry exact-match preflight
-> linkage/update/new-capture routing
```

Low-latency link-hub rule: when a public profile exposes a Linktree or similar
public link hub, try direct HTTP capture of the hub first and inspect structured
public page data such as JSON-LD `sameAs` before browser clicking. If direct HTTP
omits the outbound social graph, attach to one already-open persistent browser
session and DOM-read scripts/app state/buttons; do not repeatedly close and
relaunch the browser for each probe. Click-through to IG/YT/TikTok is reserved
for cases where the hub does not expose enough public account evidence.

If a public bio or official link hub states a region such as `NYC`, record it as
source-visible region evidence (`US / NYC`) with the source pointer. Do not infer
private demographics, residence, legal identity, or outreach/contact permission
from that region text.

This is how a single creator can accelerate registry fill without turning the
registry into a crawler or person dossier.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Creator graphing now explicitly starts from a known public creator account's
    source-visible profile bio, profile/about/channel links, and official public
    link hubs when
    present: known creator channel -> official link hub or sibling public
    channel links -> candidate rows -> exact-match preflight ->
    linkage/update/new-capture routing; source-visible region text such as NYC
    may be recorded as region evidence with a source pointer, but not as private
    demographic, residence, identity, contact, or outreach evidence.
  trigger: workflow_authority
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_gt_roadmap_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Root behavior stays unchanged; the concrete creator graphing sequence is
        source-family behavior owned by the Creator Registry graphing roadmap.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        Source-loading mechanics are unchanged; this patch only specifies which
        public source-visible surfaces count inside the creator graphing probe.
    - path: forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md
      reason: >
        The README already routes graphing/scanning to this roadmap and linkage
        evidence to the linkage spec; no folder-front-door rule changed.
    - path: forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
      reason: >
        Exact-match preflight ordering and receipt semantics are unchanged; the
        new behavior says how to gather candidate rows before that preflight.
  stale_language_search: >
    rg -n "link hub|bio|region|NYC|same-handle|source-visible"
    forseti/product/spines/capture/core/source_families/social_media/creator_registry
    AGENTS.md .agents/workflow-overlay
  stale_language_search_result: >
    Executed 2026-07-07 after edits. Hits are the new graphing/link-hub rule,
    the new linkage-spec evidence interpretation, existing compatible graphing
    language around same-handle candidates, existing compatible source-visible
    metric/source-loading references, and the linkage spec's existing weak
    bio_text_overlap evidence type. No checked surface contradicts the new
    source-visible bio/link-hub graphing behavior.
  non_claims:
    - not validation
    - not readiness
    - not registry mutation
    - not live capture authorization
    - not cross-platform person identity proof
```

## GT Road

The road from MGT to GT should compound in this order:

1. **More receipt-bearing scans** across platforms and niches.
2. **Capture-safe candidate promotion** into capture lanes without registry
   mutation.
3. **Observation sibling growth** for known accounts, especially repeat
   observations that prove update-existing routing.
4. **Platform subgraphs** that make account-level evidence and missingness easy
   to inspect.
5. **Cross-platform linkage overlay** with candidate, rejected, soft, and
   promoted states.
6. **Metric observations and rollups** with source refs, recipe versions, and
   freshness state.
7. **Audience/profile-current joins** through generated views, preserving null
   and not-estimated states.
8. **Creator Signal interpretation** that surfaces influence, freshness,
   missingness, and limitations without becoming source truth.
9. **Mechanical enforcement where repeated drift appears**, especially receipt
   row consistency, no-registry-mutation from scans, linkage-state constraints,
   and graph edge claim ceilings.
10. **Efficacy measurement**: fewer duplicate captures, faster update-existing
    routing, more useful creator recall, cleaner link decisions, and better
    operator actionability.

This roadmap does not claim a full-GT state now. The future GT target is a
creator-memory system that reliably helps Orca decide what to observe, capture,
link, update, or ignore without overclaiming what the evidence proves.

## Accepted Residuals

- No fuzzy identity proof yet.
- No cross-platform person claim yet.
- No runtime graph store or dashboard yet.
- No standing crawler or live social search.
- No registry mutation from scan rows alone.
- No capture, Silver write, metric refresh, or outreach authorization.
- No buyer proof or audience-fit proof.
- Some enforcement remains prose-first until a repeated failure class justifies
  a deterministic validator, runner gate, or generated check.