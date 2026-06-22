# Core Spine v0 Data Capture Spine Remaining Fixture Plan

```yaml
retrieval_header_version: 1
artifact_role: Product-method fixture plan
scope: Planning-only fixture architecture for remaining Data Capture Spine pressure tests before downstream ECR/Cleaning design input.
use_when:
  - Continuing Data Capture Spine setup and pressure testing.
  - Deciding which remaining fixture thread to run next.
  - Checking whether Data Capture Spine has enough pressure-test coverage for advisory downstream design input.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
  - docs/workflows/orca_repo_map_v0.md
input_hashes:
  contract: ED11CD3995E47A2DC1BF277966D59E66BE798128EBECCBFE3D4574AA82FC10CB
  context_note: DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D
  blueprint: 102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B
  reddit_fixture: AFD177CA51A1374011702B59A3ED90A3C9CE792223B64235B0F5CEE458526206
  milwaukee_fixture: 3C556E05D1653B732386E820FE6348FB95C66A31E38CA26A5BB3BD5B0CB93B92
stale_if:
  - The Data Capture obligation contract is materially patched.
  - Any remaining fixture thread changes the fixture order or acceptance gate.
  - Orca promotes or rejects Data Capture Spine v0 as accepted source.
```

- Status: PLAN_DRAFT_V0
- Artifact type: Product-method fixture plan
- Scope: Remaining Data Capture Spine pressure-test architecture only
- Source basis: current Data Capture obligation contract, context note, blueprint, Reddit pressure fixture, Milwaukee pressure fixture, and owner-accepted synthesis outcome
- Implementation authorized: no
- Runtime/source-system design authorized: no
- ECR/Cleaning design authorized: no
- Source-of-truth promotion claimed: no

## Purpose

This note fixes the remaining fixture architecture for Data Capture Spine setup.
It prevents two mistakes:

- moving to ECR/Cleaning design as if Data Capture Spine were closed; and
- continuing pressure tests without a clear stop condition.

Data Capture Spine remains in setup and pressure-test mode. Existing fixtures
are useful, but they do not prove acceptance, formal validation, runtime
readiness, ECR/Cleaning readiness, or source-of-truth promotion.

## Current Coverage

Current meaningful coverage:

| Fixture | Coverage | Use |
| --- | --- | --- |
| Reddit API/data pricing | Threaded/community chain plus package/segmentation pressure | Tests related-chain preservation, live/mutable thread limits, source-visible segmentation, and summary-flattening risk. |
| Milwaukee fiscal crossroads | Public-sector package/bundle pressure | Tests bundle-as-presented preservation, trade/package structure, public-sector source framing, and package flattening risk. |

Still missing:

- review surface with recency and long-context tension;
- docs/changelog/versioned page with version and timing risk;
- archive/history case with deleted, edited, cached, prior-window, or
  visibility-shift risk, including a recapture sub-case;
- multimodal/dynamic case only if a candidate proves it is required.

## Decision

Run **three separate remaining fixture threads**:

1. Review surface.
2. Docs/changelog/versioned public page.
3. Archive/history with recapture sub-case.

Do not combine docs/changelog and archive/history by default. A single source
may contain both versioning and archive signals, but the fixture outcomes must
be recorded separately. One collapsed case must not count as proof that both
families were pressure-tested.

Do not add multimodal/dynamic as a required fixture yet. Add it only if a
candidate shows the Data Capture obligations cannot be evaluated without layout,
rendered state, interaction state, video, audio, or other non-text signal.

## Fixture Order

### 1. Review Surface

Run first because it is the cleanest independent missing family and does not
depend on docs/archive lessons.

The fixture must test:

- rating plus review text preservation;
- recency posture;
- visible experience timing;
- long positive and long negative context;
- recent low-rating or one-star reviews when they describe live regression,
  support failure, quality break, pricing shock, or operational pain;
- long five-star reviews when they explain concrete fit, success conditions,
  buyer context, adoption context, or high-value use;
- verified, unverified, invited, incentivized, platform-moderated, or
  vendor-responded posture where visible;
- sorting, filtering, removal, or moderation constraints where visible;
- fair slice boundaries without Capture deciding credibility, discounting,
  representativeness, inclusion, Decision Strength, or Action Ceiling.

Material failure examples:

- a ledger row preserves star rating but drops long-context text;
- Capture cannot expose recency or experience timing;
- platform sorting/moderation changes what is visible, but Capture treats the
  surface as neutral;
- positive long-context reviews are ignored while negative reviews are
  over-preserved, or the reverse;
- Capture starts weighing review credibility instead of recording visible
  constraints.

### 2. Docs / Changelog / Versioned Page

Run second because it directly serves Orca's likely SaaS/API/pricing wedge and
sharpens what the archive/history fixture still needs to prove.

The fixture must test:

- publication or event timing versus capture timing;
- last-edit, update, version, release, deprecation, future/current, beta,
  removed, or migration-state posture where visible;
- whether the source appears edited, backfilled, silently changed, or materially
  updated after the relevant decision window;
- whether page content describes current behavior, future behavior, deprecated
  behavior, or removed behavior;
- cache, archive, prior-version, or version-history posture where visible;
- cutoff leakage risk when live docs include post-window information.

Material failure examples:

- Capture collapses publication, last-edit, capture, and cutoff timing into one
  generic timestamp;
- a future or beta docs state is treated as current behavior;
- a live docs page contains post-window material and Capture does not mark it;
- a changelog entry is summarized without preserving version/deprecation
  posture.

### 3. Archive / History With Recapture Sub-Case

Run third because it should deliberately pressure archive posture and recapture
after review and docs/versioning lessons are visible.

The fixture must test:

- archive posture states: `archived`, `attempt_failed`, `not_attempted`,
  `not_applicable`;
- deleted, edited, cached, archive-only, prior-window, or visibility-shifted
  public material;
- failed access visibility;
- whether exact access failed, degraded, or required fallback mode;
- relationship between original capture and recapture;
- why recapture happened;
- what source state changed, if known;
- whether the new capture supersedes, supplements, or conflicts with prior
  capture;
- whether cutoff posture changed or became clearer.

Material failure examples:

- archive/history posture is missing or implied rather than explicit;
- an archive attempt failure disappears from the capture record;
- recapture overwrites earlier capture history;
- a source-state change is preserved as a new fact without preserving the
  relationship to the earlier capture;
- prior-window visibility is asserted without visible archive/cache basis.

## Candidate Admission Gates

A fixture candidate should be rejected or reframed if it cannot make the target
risk load-bearing.

Review-surface candidates must expose enough of the review surface to test
rating/text, recency, long-context, and moderation/incentive/sorting posture.

Docs/changelog candidates must expose version, timing, update, future/current,
deprecation, migration, or live-page mutation risk. A static blog post is not
enough unless it has visible version/cutoff complications.

Archive/history candidates must expose deleted, edited, cached, archive-only,
prior-window, failed-access, or recapture-relevant behavior. A normal current
page with an archive URL is not enough.

Multimodal/dynamic candidates should be admitted only when text-only capture
would lose the signal.

## Patch-Before-Next Rule

After each fixture, decide whether the finding is material.

Patch before the next fixture when a finding shows that an obligation:

- looked satisfied on paper but was partial, blocked, or silently omitted in
  practice;
- is too strict to apply across source families;
- is too loose to preserve downstream inspectability;
- belongs in satellite but is currently written as core;
- belongs in core but is currently only a satellite note;
- creates leakage into ECR, Cleaning, Judgment, runtime tooling, or source maps.

Do not halt the sequence for minor satellite observations, terminology
improvements, or candidate-specific quirks that do not change the core
obligation contract.

## Stop Condition

After the three remaining fixtures land and material contract patches settle,
Data Capture Spine may be treated as:

```text
stable enough for advisory downstream design input
```

It must not be described as accepted, validated, complete, source-of-truth
promoted, implementation-ready, runtime-ready, or Cleaning/ECR-ready.

Advisory downstream notes may then discuss what ECR or Cleaning must preserve
or inspect categorically. They must not define ECR fields, keys, IDs, schemas,
tables, storage, Cleaning transformations, runtime tooling, source maps,
dashboards, or readiness claims.

## What Remains Not Proven

Even after these fixtures:

- Data Capture acceptance is not proven;
- formal validation is not proven;
- source-of-truth promotion is not proven;
- ECR schema is not designed;
- Cleaning Spine is not designed;
- Judgment Spine readiness is not proven;
- runtime/source-system feasibility is not proven;
- archive tooling is not chosen;
- source maps, APIs, storage, dashboards, and automation are not authorized;
- standing or opportunistic corpus intake remains out of scope;
- multimodal sufficiency remains untested unless separately admitted;
- buyer proof, commercial readiness, repeatability, and implementation
  readiness are not claimed.

## Next Routing Object

Next routing object: **review-surface pressure-test thread**.

The review-surface fixture should produce a durable pressure-test artifact that
answers:

- which Data Capture obligations were tested;
- which obligations held;
- which obligations failed, were partial, or were source-limited;
- whether any obligation should be patched before the docs/changelog fixture;
- what source-family satellite guidance emerged;
- which downstream ECR/Cleaning notes should be carried without designing those
  layers.

The review-surface fixture should not run public web research in the setup
thread. It should run as a separate source-loading unit with its own preflight,
source ledger, artifact path, and non-claims.
