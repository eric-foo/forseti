# Core Spine v0 Data Capture Spine Archive / History With Recapture Pressure Test

```yaml
retrieval_header_version: 1
artifact_role: Product-method pressure-test fixture
scope: Archive/history and recapture pressure test for Data Capture Spine v0 obligations using Unity Runtime Fee source-state changes.
use_when:
  - Continuing Data Capture Spine setup pressure tests after the archive/history recapture fixture.
  - Checking whether archive/history and recapture obligations require a contract patch before full-fixture synthesis.
  - Preparing categorical downstream notes for future ECR or Cleaning work without designing those layers.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md
input_hashes:
  fixture_plan: D4BC5D2983F8EC490AD3154A3C748014A71B123364D73AFF8E8C2743297C0584
  contract: ED11CD3995E47A2DC1BF277966D59E66BE798128EBECCBFE3D4574AA82FC10CB
  context_note: DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D
  blueprint: 102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B
  docs_changelog_fixture: AE61EE89E0704F68B353D71CEB3BC8EDAC2E1F66A68C5A8C78A29B62028758F6
branch_or_commit: main@5e999c1
stale_if:
  - The Data Capture obligation contract is materially patched.
  - The remaining fixture plan is superseded or reframed.
  - Unity materially changes the current blog URL, pricing page, cancellation page, discussion migration, or accessible archive snapshots used here.
  - A later archive/history recapture pressure-test artifact supersedes this fixture.
```

- Status: PRESSURE_TEST_FIXTURE_V0
- Artifact type: Data Capture Spine setup pressure test
- Captured: 2026-05-25
- External surfaces refreshed: 2026-05-25
- Candidate: Unity Runtime Fee announcement and recapture slice, bounded to the original September 2023 blog URL, the accompanying Unity forum/discussion surface, archived 2023 snapshots, and current Unity cancellation/pricing recapture pages.
- Fixture posture: primary archive/history with recapture pressure-test fixture, not a formal adversarial review.
- Data Capture status claimed: setup / pressure-test mode only
- Implementation authorized: no
- Runtime/source-system design authorized: no
- ECR/Cleaning design authorized: no
- Source-of-truth promotion claimed: no

Non-claims: this artifact does not claim Data Capture closure, acceptance,
formal validation, source-of-truth promotion, ECR/Cleaning readiness,
runtime/tooling readiness, implementation readiness, Unity source correctness,
legal interpretation, commercial interpretation, or archive capture completion.

## 1. Retrieval Header And Non-Claims

Purpose: pressure-test whether the draft Data Capture obligation contract can
preserve archive/history and recapture context when a public source changes
state after the relevant decision window.

Use when: deciding whether the archive/history fixture exposed a material
contract patch before full-fixture synthesis.

Do not use for: Unity Runtime Fee advice, legal analysis, credibility,
Decision Strength, Action Ceiling, ECR field design, Cleaning transformation
design, runtime scraping, source maps, dashboards, APIs, storage, automation,
or readiness claims.

Authority boundary: current user instruction, `AGENTS.md`, and the Orca
overlay control this artifact. Local Data Capture docs are setup sources, not
acceptance, validation, or source-of-truth promotion evidence. External Unity,
Internet Archive, Google, Reddit, and forum/community pages are mutable public
sources and only support the bounded fixture slice recorded here.

Recheck recipe: recompute the local hashes above, re-open the external URLs in
the source-read ledger, and treat changed page title, current URL content,
archive availability, cache behavior, discussion access state, migration state,
or cancellation/pricing wording as source-state change. Do not silently reuse
this fixture for a strict claim.

## 2. Start Preflight And Source-Read Ledger

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 target deepening for Data Capture setup / pressure-test packet plus retrieval-header guidance and external archive/history candidate sources
  edit_permission: docs-write
  target_scope: archive/history with recapture pressure-test fixture artifact only
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README; source-loading; repo map; fixture plan; obligation contract; context note; architecture blueprint; docs/changelog fixture
```

Dirty state note: `git status --short` showed many pre-existing modified and
untracked files. Relevant source statuses are recorded in the ledger. This
artifact treats modified or untracked setup docs as repo-visible task sources,
not as proof of acceptance, validation, readiness, or source-of-truth
promotion.

| Source | Why read | Scope read | Supports | Status |
| --- | --- | --- | --- | --- |
| Current user instruction | Controlling task and hard boundaries | Full current instruction | Output path, required sections, candidate admission rule, forbidden ECR/Cleaning/runtime moves | user-stated |
| `AGENTS.md` | Workspace authority | Full file | Orca overlay requirement and docs-write boundary | clean |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Full file | Forseti authority boundary and missing-authority rule | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack and ledger rules | Full file | Start preflight, bounded reads, Data Capture setup packet, not-proven boundaries | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source precedence | Full file | Conflict order and known-source status | modified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Durable artifact header | Full file | Retrieval header shape and forbidden header claims | clean |
| `docs/workflows/artifact_retrievability_guide.md` | Body-opening shape | Full file | Source-loading surface, stale/recheck pattern, non-claims | clean |
| `docs/workflows/orca_repo_map_v0.md` | Data Capture pressure-test navigation | Full file | Pressure-test packet and contract hash check | modified |
| `docs/product/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md` | Controlling fixture plan | Full file | Archive/history fixture target, admission gates, patch-before-next rule | untracked; hash verified |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Contract under test | Full file | Core archive/history, source visibility, recapture, failure, and forbidden-output obligations | untracked; hash verified |
| `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md` | Context-preservation source | Full file | Archive/history context rules and core/satellite boundary | modified; hash recorded |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Layer boundary | Full file | Commissioned capture, archive/history concept, source-family satellites, rejected patterns | untracked; hash recorded |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` | Prior pressure fixture | Full file | Sequence state and archive/history handoff boundary | untracked; hash verified |
| `workflow-deep-thinking` skill | User-requested reasoning discipline | Full skill file | Careful option selection, uncertainty handling, and strict non-claim discipline | local skill, not Forseti authority |
| `https://blog.unity.com/news/plan-pricing-and-packaging-updates` | Original blog URL current recapture | Live fetch by shell | Same historical URL now resolves to a page titled `Unity is Canceling the Runtime Fee` | external mutable; current-state recapture |
| `https://web.archive.org/web/20230912135629/https://blog.unity.com/news/plan-pricing-and-packaging-updates` | Original announcement archive | Archived snapshot by shell | September 12, 2023 blog state introducing a January 1, 2024 Runtime Fee | external archive snapshot |
| `https://web.archive.org/web/20231002005030/https://blog.unity.com/news/plan-pricing-and-packaging-updates` | Later archived revised blog state | Archived snapshot by shell | Same blog URL after update/outdated posture appeared | external archive snapshot |
| `https://forum.unity.com/threads/unity-plan-pricing-and-packaging-updates.1482750/` | Original forum URL current exact access | Shell fetch | Exact old forum URL returned HTTP 403 in this capture path | external mutable; access failed |
| `https://web.archive.org/web/20230913160222/https://forum.unity.com/threads/unity-plan-pricing-and-packaging-updates.1482750/` | Forum prior-window archive | Archived snapshot by shell | September 13, 2023 forum Q/A around reinstall/redownload/hardware-change counting | external archive snapshot |
| `https://discussions.unity.com/t/unity-plan-pricing-and-packaging-updates/927079` | Migrated current discussion | Browser/web text and shell fetch | Web text exposed edits, updates, outdated/closed posture, and migrated discussion context; shell fetch returned HTTP 403 | external mutable; client-dependent access |
| `https://unity.com/products/pricing-updates` | Current pricing recapture | Live web/shell fetch | Current cancellation, pricing, and Editor Software Terms posture | external mutable |
| `https://unity.com/runtime-fee-estimator` | Current cancellation recapture | Live web/shell fetch | Current cancellation page title and Runtime Fee cancellation posture | external mutable |
| `https://webcache.googleusercontent.com/search?q=cache:https://blog.unity.com/news/plan-pricing-and-packaging-updates` | Cache fallback test | Shell fetch | Exact cache attempt returned a generic Google Search page, not the cached source page | external cache attempt_failed/degraded |
| Reddit and search-result surfaces referencing the Wayback forum URL | Candidate corroboration and discovery | Search snippets and visible Reddit result | Shows the archived forum snapshot was publicly cited as preserving removed/replaced install-count Q/A | external community surface; not official proof |

## 3. Candidate Selected And Why It Admits As An Archive / History Fixture

Selected candidate: Unity Runtime Fee announcement and recapture slice, bounded
to the September 2023 original blog URL, the official forum/discussion thread
around the announcement, archived 2023 snapshots, and current Unity
cancellation/pricing pages.

Fixture URLs:

- Original blog URL, current recapture:
  `https://blog.unity.com/news/plan-pricing-and-packaging-updates`
- Original blog archive, September 12, 2023:
  `https://web.archive.org/web/20230912135629/https://blog.unity.com/news/plan-pricing-and-packaging-updates`
- Revised/outdated blog archive, October 2, 2023:
  `https://web.archive.org/web/20231002005030/https://blog.unity.com/news/plan-pricing-and-packaging-updates`
- Original forum URL:
  `https://forum.unity.com/threads/unity-plan-pricing-and-packaging-updates.1482750/`
- Forum archive, September 13, 2023:
  `https://web.archive.org/web/20230913160222/https://forum.unity.com/threads/unity-plan-pricing-and-packaging-updates.1482750/`
- Migrated current discussion:
  `https://discussions.unity.com/t/unity-plan-pricing-and-packaging-updates/927079`
- Current pricing updates page:
  `https://unity.com/products/pricing-updates`
- Current cancellation page:
  `https://unity.com/runtime-fee-estimator`

Why it admits:

- It is a public company announcement and official discussion surface where the
  current source state materially differs from the prior-window state.
- The original blog URL is live in 2026, but the retrieved page title is now
  `Unity is Canceling the Runtime Fee`, not the September 2023 announcement.
- The archived September 2023 blog snapshot preserves the original
  announcement state that introduced a January 1, 2024 Runtime Fee.
- The later archived blog snapshot preserves an updated/outdated posture after
  Unity's September 2023 changes.
- The old forum URL produced an HTTP 403 in the shell capture path, while an
  archived snapshot preserved prior-window official-thread Q/A.
- The migrated current discussion exposes edited/update posture and a current
  discussion surface, but shell access to that URL also returned HTTP 403. This
  makes failed/degraded access visible instead of hypothetical.
- The current pricing and cancellation pages preserve the later source state:
  Runtime Fee cancellation and current pricing/terms posture.
- A Google cache fallback attempt did not return the cached page content,
  making cache attempt failure/degradation visible.

This is not merely a current page with an archive URL. The historical source
state is load-bearing because a 2026 capture of the original blog URL would
produce the opposite policy posture from a September 2023 prior-window capture.

## 4. Archive / History Capture Slice: What Was Preserved And Why

The slice preserved only the source context needed to make archive/history and
recapture risk inspectable:

- source family: public company blog, pricing page, cancellation page, official
  forum/discussion thread, archive snapshots, cache attempt, and community
  discovery/corroboration surfaces;
- bounded topic: Unity Runtime Fee announcement, install-count/reinstall
  clarification, later policy revision, and cancellation/current-pricing state;
- original announcement posture: the September 12, 2023 archived blog snapshot
  carries the original plan-pricing-and-packaging announcement and January 1,
  2024 effective-date posture;
- archived forum posture: the September 13, 2023 forum snapshot carries Q/A
  about reinstall/redownload/hardware-change counting and future installs;
- current URL replacement posture: the original blog URL now retrieved as a
  cancellation page rather than the original announcement;
- later current-state posture: Unity's current pricing updates and
  cancellation pages describe cancellation and current plan/terms posture;
- migrated discussion posture: the current discussion surface shows edits,
  September updates, outdated/closed posture, and related links;
- failed/degraded access posture: the old forum URL and current migrated
  discussion returned HTTP 403 in the shell capture path; Google cache returned
  a generic Google Search page instead of cached source content.

Preservation rationale:

- the same URL can carry different source states across time, so URL identity
  alone cannot preserve the raw observable;
- the prior-window archive is needed to avoid converting the current
  cancellation page into false evidence about September 2023 public visibility;
- the forum snapshot is needed because current edited/migrated discussion
  surfaces do not preserve every prior answer as current live state;
- cache and access failures must remain visible even when an archive snapshot
  succeeds elsewhere;
- the recapture relationship matters because current Unity pages supersede
  current policy state but do not erase prior-window announcement history.

## 5. Archive Posture States Tested

```text
archive_posture_states_tested:
  archived:
    - September 12, 2023 Wayback snapshot of the original Unity blog URL.
    - October 2, 2023 Wayback snapshot of the same blog URL after update/outdated posture appeared.
    - September 13, 2023 Wayback snapshot of the original Unity forum URL.
    posture_effect: prior-window and revised historical states are inspectable through archive/history mode.

  attempt_failed:
    - Old forum URL exact shell access returned HTTP 403.
    - Current migrated discussion exact shell access returned HTTP 403, despite web text being inspectable through another retrieval path.
    - Google cache URL returned a generic Google Search page, not the cached source page.
    posture_effect: failed or degraded access remains visible and must not disappear because other surfaces were accessible.

  not_attempted:
    - Full Wayback timeline enumeration was not attempted.
    - Full screenshot/PDF capture was not attempted.
    - Full Unity legal/TOS GitHub history reconstruction was not attempted.
    - Full community mirror exhaust was not attempted.
    posture_effect: bounded fixture scope is visible instead of pretending archive completion.

  not_applicable:
    - Current cancellation and pricing pages were used to establish current recapture posture, not to prove September 2023 prior-window visibility.
    - Archive proof was not applicable to the narrow claim that the current live page now describes cancellation/current pricing state.
    posture_effect: current-state recapture and prior-window archive proof remain separate.
```

The contract currently contains all four posture labels. The fixture exposed a
granularity problem: one source slice can legitimately require all four states
at once. A single capture-level `archived` label would be materially too loose.

## 6. Prior-Window, Deleted, Edited, Cached, Or Visibility-Shift Posture

Prior-window posture:

- The September 12 and September 13, 2023 archive snapshots are prior-window
  sources for a decision about what Unity publicly communicated during the
  initial Runtime Fee announcement period.
- The October 2, 2023 archive snapshot is a later-window historical source
  showing revised/outdated posture after Unity's September 2023 policy changes.

Edited posture:

- The migrated current discussion exposes visible edit/update markers,
  including September 13, September 17, and September 22 updates.
- The current discussion state differs from the archived prior-window forum
  snapshot around install-count clarification.
- The fixture does not assert every edit delta. It records that edit posture is
  load-bearing and source-visible enough to require preservation.

Cached posture:

- A Google cache fallback was attempted for the original blog URL.
- The fetch returned a generic Google Search page rather than cached source
  content, so cache posture is `attempt_failed` or degraded for this fixture.

Archive-only posture:

- The September 2023 original announcement state is not what a 2026 live fetch
  of the original blog URL returns.
- The September 2023 old forum Q/A state was accessible through Wayback in the
  shell capture path, while the old live forum URL returned HTTP 403.

Visibility-shift posture:

- The original blog URL remained reachable but resolved to a cancellation-page
  state rather than original announcement state.
- The original forum URL and migrated discussion had client-dependent access:
  shell access failed with HTTP 403, while web text for the migrated discussion
  was inspectable through another retrieval path.
- The public discussion surface appears migrated from the old forum URL to
  `discussions.unity.com`, so source identity must distinguish original URL,
  archived old URL, and migrated current URL.

Deleted posture:

- Deletion is not proven by this fixture. The fixture proves replacement,
  migration, archive-only historical state, edit/update posture, and failed or
  degraded access. It does not claim the original material was deleted from
  Unity systems.

## 7. Recapture Semantics: Prior Capture, New Capture, Change Reason, Supersede / Supplement / Conflict Posture

Prior capture:

- September 12, 2023 archived blog snapshot: original announcement posture.
- September 13, 2023 archived forum snapshot: original official-thread Q/A
  posture, including reinstall/redownload/hardware-change counting language.
- October 2, 2023 archived blog snapshot: later revised/outdated historical
  posture after Unity signaled changes.

New capture:

- 2026 live recapture of the original blog URL: current page title was
  `Unity is Canceling the Runtime Fee`.
- 2026 current pricing page: current pricing/plan/terms posture and Runtime
  Fee cancellation wording.
- 2026 current cancellation page: cancellation-state page.
- 2026 migrated discussion surface: edited/outdated current discussion posture.

Why recapture happened:

- The fixture deliberately tested whether a current capture could overwrite or
  flatten a prior-window source state.
- The same source family had public evidence of policy reversal, URL content
  replacement, discussion migration, edits, and access differences.

What source state changed, if known:

- The policy state changed from announced Runtime Fee to revised policy and
  later cancellation.
- The original blog URL's current retrieved content changed from the historical
  announcement to a cancellation page.
- The forum/discussion surface changed through migration, edits, closure or
  outdated posture, and client-dependent access.
- The exact internal CMS, redirect, deletion, and migration mechanics are
  source-limited in this fixture.

Supersede / supplement / conflict posture:

- Current capture supersedes prior capture only for current Unity policy
  posture: the Runtime Fee is now canceled.
- Current capture supplements prior capture by explaining why the historical
  prior-window state is no longer current.
- Current capture conflicts with prior capture if the question is naively
  stated as "what does this URL say?" without a date. The URL-level answer is
  time-dependent.
- Current capture does not supersede the prior-window historical observable.
  The September 2023 archived announcement remains the relevant observable for
  a September 2023 cutoff question.

Cutoff posture change or clarification:

- For a September 12-13, 2023 decision window, 2026 live pages are post-window
  material and must be marked as cutoff leakage risk.
- The September 12 and September 13 archive snapshots clarify prior-window
  visibility, within the limits of the snapshots.
- The October 2 archive clarifies that a later September/October source state
  existed, but it is post-window for an initial-announcement cutoff.
- For a 2026 current-policy decision, the current pages are the relevant
  current-state capture; the 2023 archive becomes history, not current policy.

## 8. Obligations Tested

Tested obligations:

- Commissioning Gate.
- Boundary Compliance.
- Capture-Event Provenance.
- Capture Mode Disclosure.
- Mode-Change Rule.
- Raw Observable Preservation.
- Source Identity And Actor Context.
- Decomposed Timing.
- Cutoff Posture.
- Archive / Historical Posture.
- Source Visibility And Access Limits.
- Related Context Preservation for public company announcement, policy/pricing,
  official discussion, and historical archive surfaces.
- Capture Failure And Blocker Visibility.
- Re-Capture Semantics.
- Categorical Handoff Sufficiency.
- Forbidden Outputs From Capture.

Not materially tested:

- Bundled-Offer Structure Observables, because the candidate did not present a
  multi-term public-sector package, regulatory bargain, settlement, or
  counterparty bundle.
- Review-surface moderation and rating-text obligations, because this was not
  a review surface.
- Multimodal capture sufficiency, because the fixture used text and source
  access posture. A rendered capture could become required if layout, banners,
  redirect UI, or archive controls become load-bearing in a later run.

## 9. Obligations That Held

Commissioning Gate held for setup pressure testing. The current user supplied
a specific product-method decision: pressure-test archive/history and recapture
obligations for Data Capture setup. This is enough to run the fixture. It is
not a buyer Decision Frame and does not make Unity material ECR-ready.

Boundary Compliance held. The inspected material was public blog, pricing,
cancellation, discussion, archive, cache-attempt, and community-discovery
content accessed without private credentials, deception, ordinary-person
dossiers, or intrusive collection.

Capture-Event Provenance held at product-method level. The artifact records
capture date, operator category, local source hashes, external URLs, external
mutability limits, and the obligation-contract source used for the fixture.

Capture Mode Disclosure held. The mode was mixed: local repo reading, public
web inspection, archive/history fetches, cache fallback attempt, and human-led
obligation assessment. No runtime archive tooling design, scraper, API, source
map, dashboard, storage, automation, or implementation plan was created.

Mode-Change Rule held. The candidate started as public web/source inspection,
then escalated to archive/history fetches because live current URLs no longer
preserved prior-window state. That mode change is visible.

Raw Observable Preservation held for the pressure-test slice. The artifact
preserves the load-bearing title/date/source-state relationships and exact
URLs. It does not claim to be a full raw snapshot package.

Source Identity And Actor Context held. The contract was sufficient to
separate Unity blog, Unity pricing page, Unity cancellation page, old Unity
forum URL, migrated Unity discussion, Wayback archive snapshots, Google cache
attempt, and community discovery surfaces. Capture did not decide credibility,
representativeness, or legal effect.

Decomposed Timing held. The fixture required separate source publication,
archive snapshot, current recapture, and cutoff timing. The contract already
requires those timing categories to remain separate.

Cutoff Posture held. The contract forced current Unity pages to be marked as
post-window material for any September 2023 cutoff instead of treating current
URL content as historical evidence.

Source Visibility And Access Limits held. The contract had a place to record
HTTP 403 access failures, client-dependent access, migrated discussion state,
cache degradation, and archive-only recovery without converting those limits
into credibility or exclusion judgments.

Capture Failure And Blocker Visibility held. The contract had discharge states
for archive/cache non-attempts, failed exact access, full timeline
non-enumeration, source-limited CMS mechanics, and unproven deletion.

Re-Capture Semantics held conceptually. The contract asks why recapture
happened, what changed, whether the new capture supersedes, supplements, or
conflicts, and whether cutoff posture changed or became clearer. This is the
right conceptual surface for the candidate.

Forbidden Outputs From Capture held. The fixture did not assign credibility,
weight, exclusion, Decision Strength, Action Ceiling, Signal Use
Classification, source-quality score, Cleaning transformation, ECR schema, or
runtime-source effect.

Categorical Handoff Sufficiency held as a boundary. The contract can carry
archive/history and recapture context categorically downstream without
defining ECR fields, keys, IDs, tables, schemas, storage, or Cleaning
transformations.

## 10. Obligations Partial, Blocked, Unavailable, Not Attempted, Or Source-Limited

Archive / Historical Posture: partial at contract granularity. The contract
has the right posture states, but the fixture required multiple states in one
bounded capture: archived, attempt_failed, not_attempted, and not_applicable.
If the contract is read as one rollup posture per capture, it can hide
failed cache access, failed exact access, and non-attempted timeline work
behind a single successful `archived` label.

Re-Capture Semantics: partial at relationship granularity. The current capture
both supersedes current policy posture and supplements or conflicts with
prior-window source state depending on the decision cutoff. A single
supersede/supplement/conflict label is too lossy unless the relationship is
preserved per source-state claim or capture slice.

Raw Observable Preservation: partial in this pressure-test artifact. The
artifact preserved the load-bearing text relationships and URLs, but it did
not embed full page bodies, screenshots, or archive captures. A real
commissioned capture would need the relevant raw snapshot body or a visible
limitation.

Exact deletion: unavailable_by_source in this fixture. The fixture observed
replacement, migration, archive-only historical state, and access failure. It
does not prove that Unity deleted the original content internally.

Source-state mechanism: source-limited. The fixture observed current retrieved
content and archived historical content, but did not prove whether the change
was redirect, CMS replacement, canonical URL reuse, content deletion, migration
rewrite, or another mechanism.

Full archive timeline: not_attempted. The fixture did not enumerate every
Wayback snapshot or compare all archive timestamps.

Full legal/TOS history: not_attempted. The current discussion and community
surfaces referenced terms-history concerns, but the fixture did not reconstruct
Unity legal repository history or TOS deltas.

Cache fallback: attempt_failed/degraded. The Google cache URL returned a
generic Google Search page rather than cached source content.

Live discussion access: degraded. The migrated discussion was inspectable via
web text, but shell access returned HTTP 403. The old forum URL also returned
HTTP 403 in shell. The capture therefore cannot treat "current live access" as
uniform across retrieval modes.

Multimodal capture: not_attempted/not_applicable for this slice. Text and
source access posture carried the load-bearing signal.

Bundled-Offer Structure Observables: not_applicable.

## 11. Material Patch Decision

Material patch decision: the obligation contract needs a narrow core patch
before full-fixture synthesis.

Patch reason: the current contract contains the necessary concepts, but this
fixture shows that archive/history posture and recapture relationship must be
recorded at the source-slice or access-attempt level when multiple historical
and current surfaces are used. A single capture-level archive posture can
falsely imply completion when only one of several archive/cache/access attempts
succeeded.

Recommended contract patch, conceptually:

- Archive/history posture should not be only one rollup label when cutoff,
  deletion, edit, cache, prior-window, archive-only, or visibility-shift risk
  is load-bearing. Each material source locator, archive/cache attempt, or
  fallback source surface should have visible posture, with a rollup allowed
  only if it does not hide failed, degraded, unavailable, or not-attempted
  states.
- Failed exact access and degraded fallback should remain visible even when
  another archive or current surface succeeds.
- Re-capture semantics should distinguish current-policy supersession from
  prior-window historical preservation. A new capture may supersede current
  state, supplement history, and conflict with prior capture for a different
  cutoff question at the same time.
- Prior capture history must remain inspectable when a current URL changes
  content, redirects, migrates, or becomes archive-only for the historical
  observable.

This is a core obligation patch, not merely Unity-specific satellite guidance,
because the risk generalizes to any mutable public URL, policy page, forum
thread, archive snapshot, cache, deleted page, or recapture event.

Do not treat this patch recommendation as acceptance, validation, readiness,
or source-of-truth promotion.

## 12. Source-Family Satellite Guidance

Archive/history satellites should preserve:

- original live URL, current live URL state, migrated URL, archived snapshot
  URL, cache attempt URL, and mirror/community URL as separate source surfaces
  when each carries different state;
- archive snapshot timestamp separately from source publication time, update
  time, current capture time, and recapture time;
- whether a current URL preserves the same content, a revised version, a
  cancellation/reversal page, a redirect, a migration, an error page, or a
  login/gating/access failure;
- whether an archive is official version history, third-party archive,
  search-engine cache, browser cache, community quote, mirror, screenshot, PDF,
  or current repository history;
- whether each archive/cache access was successful, failed, degraded,
  not attempted, source-limited, or not applicable to the specific claim;
- whether community reposts or snippets are only discovery/corroboration
  surfaces rather than official source proof;
- whether current recapture should supersede current-state policy, supplement
  history, or conflict with prior-window interpretation;
- when deletion is not proven and the safer state is replacement, migration,
  archive-only historical state, failed access, or unknown source mechanism.

Satellite rules should not require every source family to enumerate all
archives or mirrors. They should require the capture to expose which
archive/history routes were used, failed, unnecessary, not attempted, or
source-limited for the commissioned decision.

Satellite rules must not promote themselves into core unless they survive
comparison across at least two non-overlapping source families or the owner
accepts a specific invariant.

## 13. Downstream ECR / Cleaning Notes, Categorical Only

ECR should receive archive/history context categorically: source carrier,
source actor or publisher category, original URL, current URL state, archive
snapshot state, cache/fallback state, capture timing, recapture timing, cutoff
posture, visible source-state change, access limits, failed attempts, and
whether current capture supersedes, supplements, or conflicts with prior
capture for the relevant cutoff.

Cleaning should not collapse the 2023 announcement, 2023 revised/outdated
state, 2026 cancellation state, forum snapshot, migrated discussion, and cache
failure into one "Unity says" summary. It should preserve the relationship
among historical observable, current-state recapture, access failure, and
archive-only recovery before any downstream reduction.

Cleaning should not normalize URL identity into source-state identity. The
same URL can carry different source states across time.

These are categorical carry-forward notes only. They do not define ECR fields,
keys, IDs, tables, schemas, storage, file formats, Cleaning transformations,
dedupe rules, clustering, dashboards, APIs, scrapers, source maps, or runtime
tooling.

## 14. Not-Proven Boundaries And Next Routing Object

This fixture does not prove:

- Data Capture Spine is accepted, validated, complete, closed, hardened,
  source-of-truth promoted, implementation-ready, runtime-ready, ECR-ready, or
  Cleaning-ready.
- Unity source correctness, legal interpretation, business impact,
  credibility, or current commercial recommendation.
- The original Unity content was deleted internally.
- The exact CMS, redirect, migration, or source-management mechanism that
  changed the live URL state.
- Full Wayback timeline reconstruction, full cache reconstruction, full TOS
  history reconstruction, full community mirror collection, or full raw page
  preservation.
- Any source should be included, excluded, weighted, discounted, deduplicated,
  clustered, or treated as decision-useful.
- Any Decision Strength, Action Ceiling, Signal Use Classification, buyer
  proof, product readiness, commercial readiness, or Core Spine validation
  result.
- Future ECR, Cleaning, Judgment, source maps, APIs, scrapers, storage,
  dashboards, automation, tests, deployment, or runtime systems are authorized.

Next routing object: narrow obligation-contract patch before full-fixture
synthesis.

Patch target: clarify that archive/history posture and recapture relationship
must be preserved per material source slice, locator, archive/cache attempt, or
fallback surface when multiple states coexist. The patch should not design ECR,
Cleaning, runtime tooling, source maps, schemas, dashboards, APIs, scrapers,
storage, or automation.

After that patch is made, the next setup move can be full-fixture synthesis of
the Reddit, Milwaukee, ClickUp, Kubernetes docs/changelog, and Unity
archive/history fixtures. That future synthesis still must not claim Data
Capture closure, acceptance, formal validation, source-of-truth promotion,
ECR/Cleaning readiness, runtime/tooling readiness, or implementation readiness.
