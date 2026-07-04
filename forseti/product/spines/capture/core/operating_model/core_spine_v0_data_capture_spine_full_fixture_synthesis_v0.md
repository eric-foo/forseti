# Core Spine v0 Data Capture Spine Full-Fixture Synthesis

```yaml
retrieval_header_version: 1
artifact_role: Product-method synthesis artifact
scope: Full planned Data Capture Spine pressure-fixture synthesis across threaded/community, public-sector package, review surface, docs/changelog/versioned page, and archive/history recapture fixtures.
use_when:
  - Checking what the planned Data Capture Spine fixture set tested, what held, and what required patching.
  - Preparing advisory downstream ECR or Cleaning design input without designing those layers or claiming readiness.
  - Routing a full adversarial artifact review of this synthesis.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md
input_hashes:
  patched_obligation_contract: A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF
  remaining_fixture_plan: D4BC5D2983F8EC490AD3154A3C748014A71B123364D73AFF8E8C2743297C0584
  context_preservation_note: DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D
  architecture_blueprint: 102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B
  reddit_threaded_fixture: AFD177CA51A1374011702B59A3ED90A3C9CE792223B64235B0F5CEE458526206
  milwaukee_package_fixture: 3C556E05D1653B732386E820FE6348FB95C66A31E38CA26A5BB3BD5B0CB93B92
  clickup_review_fixture: 85AF08DAED6F3E2E89AA317CD3C2AEEC756CE8F1B311E1EB0D4EED55A95AF9C6
  kubernetes_docs_fixture: AE61EE89E0704F68B353D71CEB3BC8EDAC2E1F66A68C5A8C78A29B62028758F6
  unity_archive_fixture: 7962B20EE1DDB3F7E920A0BFA78DB47B2DA489D9A35A81FA630686C84626F3EC
branch_or_commit: main@5e999c1 with dirty/untracked workspace sources
stale_if:
  - The Data Capture obligation contract is materially patched after the hash above.
  - Any fixture artifact listed above is materially revised or superseded.
  - Owner accepts, rejects, or reframes Data Capture Spine v0.
  - A full adversarial artifact review supersedes this synthesis.
```

- Artifact state: SYNTHESIS_DRAFT_V0.
- Created: 2026-05-25.
- Scope: synthesis of the planned Data Capture Spine fixture set only.
- Implementation authorized: no.
- Runtime/source-system design authorized: no.
- ECR/Cleaning design authorized: no.
- Source-of-truth promotion claimed: no.

## 1. Retrieval Header And Non-Claims

Purpose: give a future reviewer one artifact that explains what the full
planned Data Capture Spine fixture set tested, what the obligation contract
survived, what required patching, what remains satellite, what remains not
proven, and whether advisory downstream design input is justified without
overclaiming acceptance or readiness.

Use when: checking the post-fixture state before downstream ECR/Cleaning
discussion, owner acceptance, or full adversarial artifact review.

Do not use for: Data Capture closure, owner acceptance, formal validation,
source-of-truth promotion, ECR readiness, Cleaning readiness, runtime/tooling
readiness, implementation readiness, source maps, schemas, storage, APIs,
scrapers, dashboards, automation, proof runs, credibility labels, weighting,
exclusion, Decision Strength, Action Ceiling, or Cleaning transformations.

Authority boundary: current user instruction, `AGENTS.md`, and the Orca
overlay control this artifact. The local Data Capture docs are setup and
pressure-test sources. This synthesis does not promote them to accepted
source-of-truth status.

Recheck recipe: recompute the input hashes in the retrieval header, especially
the patched obligation contract. If any hash differs, inspect the changed
artifact before relying on this synthesis. Do not silently reuse this synthesis
after a contract or fixture patch.

Non-claims: this artifact does not claim Data Capture closure, owner
acceptance, formal validation, source-of-truth promotion, ECR/Cleaning
readiness, runtime/tooling readiness, implementation readiness, buyer proof,
commercial readiness, Core Spine validation, Judgment Spine validation, or
runtime feasibility.

## 2. Start Preflight And Source-Read Ledger

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom full-fixture synthesis pack explicitly named by current user instruction
  edit_permission: docs-write
  target_scope: docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md; overlay README; source-loading; repo map; fixture plan; patched obligation contract; context note; architecture blueprint; all five fixture artifacts
```

Dirty state note: `git status --short` showed many pre-existing modified and
untracked files. This synthesis keeps the edit scoped to the requested new
artifact. The target Data Capture sources are repo-visible and hash-verified,
but their modified or untracked status does not prove acceptance, validation,
readiness, or source-of-truth promotion.

Hash verification result: all current-turn user-pinned hashes matched. The
fixture plan and some fixture headers still carry older internal contract
hashes from earlier pressure-test moments. This synthesis treats those older
header hashes as stale provenance and uses the current verified patched
contract hash:
`A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF`.

| Source | Why read | Status | Hash / provenance |
| --- | --- | --- | --- |
| Current user instruction | Controlling task, hard boundaries, output path, required sections | user-stated | current turn |
| `AGENTS.md` | Orca project instructions and overlay requirement | clean | read |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | modified | read |
| `.agents/workflow-overlay/source-loading.md` | Start preflight, source-pack, ledger, not-proven boundaries | modified | read |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | modified | read |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | clean | read |
| `docs/workflows/artifact_retrievability_guide.md` | Body-opening and stale/recheck guidance | clean | read |
| `docs/workflows/orca_repo_map_v0.md` | Data Capture setup/pressure-test navigation | modified | read |
| `docs/product/core_spine_v0_data_capture_spine_remaining_fixture_plan_v0.md` | Planned fixture set and stop condition | untracked | `D4BC5D2983F8EC490AD3154A3C748014A71B123364D73AFF8E8C2743297C0584` |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Patched obligation contract under synthesis | untracked | `A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF` |
| `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md` | Core/satellite context-preservation boundary | modified | `DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D` |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Data Capture architecture and layer split | untracked | `102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B` |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` | Threaded/community and package/segmentation fixture | untracked | `AFD177CA51A1374011702B59A3ED90A3C9CE792223B64235B0F5CEE458526206` |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md` | Public-sector package/bundle fixture | untracked | `3C556E05D1653B732386E820FE6348FB95C66A31E38CA26A5BB3BD5B0CB93B92` |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` | Review-surface fixture | untracked | `85AF08DAED6F3E2E89AA317CD3C2AEEC756CE8F1B311E1EB0D4EED55A95AF9C6` |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` | Docs/changelog/versioned-page fixture | untracked | `AE61EE89E0704F68B353D71CEB3BC8EDAC2E1F66A68C5A8C78A29B62028758F6` |
| `docs/product/core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` | Archive/history recapture fixture and material patch finding | untracked | `7962B20EE1DDB3F7E920A0BFA78DB47B2DA489D9A35A81FA630686C84626F3EC` |
| `workflow-deep-thinking` skill | User-requested reasoning discipline | local skill, not Orca authority | read |

## 3. Fixture Set Summary

The fixture plan called for the existing Reddit and Milwaukee pressure
fixtures plus three remaining families: review surface, docs/changelog or
versioned page, and archive/history with recapture. All planned fixture
families have landed.

| Fixture | Source-family pressure | What it tested | Synthesis result |
| --- | --- | --- | --- |
| Reddit API/data pricing | Threaded/community chain plus API/data pricing package or segmentation | Related-chain preservation, live-thread timing, source-visible package/segmentation structure, blocked-source visibility, and downstream boundary discipline | Core direction held. The current contract covers threaded-chain and package/segmentation preservation; the case remains partial as a full raw capture handoff. |
| Milwaukee fiscal crossroads | Public-sector package/bundle | Bundle-as-presented preservation for WRS/new-hire pension reform inside a broader state package | Contract-level obligation held. Source-level capture sufficiency is not proven because the fixture used a reveal readout rather than full raw package source text. |
| ClickUp review surfaces | Review surface with recency and long-context tension | Rating/text coupling, recent negative context, long positive context, platform labels, sorting/filtering/moderation posture, visible source limits | No material core patch required. Review-specific handling remains satellite guidance. |
| Kubernetes v1.32 deprecated API docs | Docs/changelog/versioned public page | Event timing, page update timing, live current versus static snapshot posture, cutoff leakage, metadata-scope risk | No material core patch required. Docs/version mechanics remain satellite guidance. |
| Unity Runtime Fee archive/history | Archive/history and recapture | Same-URL source-state changes, archive snapshots, failed exact access, cache attempt failure, migration, current recapture, supersede/supplement/conflict relationships | One material core defect found. The obligation contract was patched narrowly for per-slice archive/history posture and recapture relationship granularity. |

This fixture set is evidence for pressure-tested contract stability, not proof
by fixture count. The meaningful result is that distinct source-family failure
modes were compared and only one material core contract defect remained, which
was patched narrowly.

## 4. Adversarial Preflight Before Synthesis

What could be overclaimed:

- Treating five fixture artifacts as formal validation or acceptance.
- Treating setup pressure-test work as Data Capture closure.
- Treating the patched contract as source-of-truth promoted.
- Treating fixture usefulness as source-level capture sufficiency.
- Treating review, docs, archive, Reddit, Kubernetes, Unity, ClickUp, or
  Milwaukee-specific guidance as core law.
- Treating advisory downstream input as ECR/Cleaning readiness.
- Treating external page observations inside fixture artifacts as stable
  current source truth after 2026-05-25.
- Treating no-patch findings in review/docs fixtures as proof that future
  source families cannot break the contract.

Weakest fixture: Milwaukee is the weakest by evidence depth. It was useful
because it pressured public-sector bundle preservation outside Reddit-style
threaded sources, but it relied on a targeted reveal readout rather than full
raw package text, headings, ordering, dependencies, draft/vote sequence, or
source-language reconstruction. It supports the existence of the obligation;
it does not prove full Milwaukee source-level capture sufficiency.

Archive patch sufficiency: the patch appears sufficient for the defect the
Unity fixture found. It prevents one rollup `archived` posture from hiding
failed exact access, degraded cache access, migrated current pages,
not-attempted timelines, or mixed recapture relationships. It also lets a
current recapture supersede current-state posture while supplementing or
conflicting with prior-window history. This is sufficient for advisory
synthesis; it is not proven across a broader archive corpus or accepted as
final.

Satellite guidance promotion risk: the accumulated satellite guidance is
valuable but dangerous if copied into core. Reddit platform conventions,
Trustpilot/G2 labels, Kubernetes version-menu and GitHub-source mechanics,
Unity/Wayback/cache patterns, and Milwaukee public-sector negotiation cues are
source-family adaptation. Core may own the invariant obligation to preserve
visible posture, timing, context, and limits; it should not own every platform
mechanic.

Is "stable enough for advisory downstream design input" justified? Yes, but
only in the constrained wording below. The planned fixture set is complete,
the one material core defect has been patched, and no unpatched material core
defect is visible from the read artifacts. The stronger claim is not justified
because owner acceptance, adversarial review, formal validation, source-of-truth
promotion, ECR/Cleaning design, and runtime feasibility are not proven.

Allowed strongest phrasing:

```text
Data Capture Spine obligation contract is pressure-tested across the planned fixture set and appears stable enough for advisory downstream design input, subject to owner acceptance and adversarial review.
```

## 5. Cross-Fixture Obligation Coverage Table

In this table, `held` means the obligation-contract rule remained applicable
and was not invalidated by the fixture. It does not mean every fixture fully
discharged a production capture packet. Partial raw capture, source-limited
metadata, reveal-readout depth, unavailable access, and not-attempted routes
remain source-visible limitations where the fixture recorded them.

| Core obligation area | Fixtures that materially exercised it | Coverage synthesis |
| --- | --- | --- |
| Commissioning Gate | All five | Held for setup pressure testing. These were product-method pressure tests, not buyer Decision Frames or ECR-ready captures. |
| Boundary Compliance | All five | Held at the fixture level: public, market-level, non-deceptive sources and local docs. No private, deceptive, or intrusive collection was authorized. |
| Capture-Event Provenance | All five | Held at product-method level through source ledgers, hashes, dates, and mutable-source warnings. Runtime-grade provenance was not designed or claimed. |
| Capture Mode Disclosure | Reddit, ClickUp, Kubernetes, Unity | Held categorically. Unity especially tested mixed mode with archive/history and fallback attempts. No mode was treated as quality proof. |
| Mode-Change Rule | Reddit, Kubernetes, Unity | Held conceptually. Unity showed why escalation from live/current capture to archive/history must be visible. |
| Raw Observable Preservation | All five | Core obligation held, but many fixture artifacts were not full raw capture packages. They tested whether the contract would require raw preservation or visible limitation. |
| Source Identity And Actor Context | All five | Held. The contract separated carrier from actor across platforms, forums, docs, company pages, archives, and public-sector packages without credibility decisions. |
| Decomposed Timing | Reddit, ClickUp, Kubernetes, Unity | Held. Timing had to separate event/publication, page edit/version, capture, recapture, thread/item timing, and cutoff posture. |
| Cutoff Posture | Reddit, Kubernetes, Unity | Held. Kubernetes and Unity most strongly tested cutoff leakage from live/current pages into prior windows. |
| Archive / Historical Posture | Kubernetes, Unity, partially Reddit/ClickUp | Required patch after Unity. The patched contract now requires per-slice or per-locator posture when states differ. |
| Source Visibility And Access Limits | All five | Held. Blocked Reddit candidates, review-platform constraints, Kubernetes metadata limits, Unity 403/cache failures, and Milwaukee source gaps remained visible. |
| Related Context Preservation | Reddit, ClickUp, Kubernetes, Unity, Milwaukee | Held as core invariant with source-family branches. The smallest fair source slice differs by family and remains satellite-specific. |
| Bundled-Offer Structure Observables | Reddit, Milwaukee | Held as core at the obligation level across two non-overlapping source families: API/data pricing segmentation and public-sector package structure. Milwaukee is the shallow leg: it used reveal-readout depth, so full public-sector raw source-level capture sufficiency remains not proven. |
| Capture Failure And Blocker Visibility | All five | Held. The fixtures repeatedly used partial, unavailable, blocked, not-attempted, or source-limited states instead of silent omission. |
| Re-Capture Semantics | Unity, partially Kubernetes/Reddit | Required patch after Unity. Recapture relationships must be preserved at the relevant source-state or locator level when mixed. |
| Categorical Handoff Sufficiency | All five | Held as a boundary. The contract can say what downstream layers must be able to inspect categorically without defining fields, IDs, schema, storage, or transformations. |
| Forbidden Capture Outputs | All five | Held. Fixtures avoided credibility, representativeness, inclusion/exclusion, Decision Strength, Action Ceiling, Signal Use Classification, source scoring, ECR design, and Cleaning design. |

## 6. What Held Across Fixtures

The commissioned-capture boundary held. Data Capture remained a product-method
obligation for a decision-framed or setup pressure-test capture, not standing
or opportunistic corpus intake.

The layer split held. Capture records visible source facts, source-state
relationships, raw observables, context, timing, access limits, archive/cutoff
posture, and blockers. It does not make Judgment, Cleaning, ECR, credibility,
discounting, exclusion, Decision Strength, or Action Ceiling decisions.

The raw-observable and related-context principle held. The fixture-specific
answer changed by source family, but the invariant did not: preserve enough of
what the source showed, said, and surrounded the signal with so downstream
inspection does not require recollecting source history.

The timing and cutoff discipline held. Reddit, Kubernetes, and Unity all showed
that a single timestamp is insufficient. Thread timing, release timing, page
update timing, archive snapshot timing, capture timing, recapture timing, and
decision cutoff posture can diverge.

The failure-visibility rule held. Blocked access, not-attempted archive
routes, source-limited metadata, partial raw capture, platform sorting limits,
and missing raw package text were allowed as visible limitations. They were not
converted into hidden filters.

Bundle/package preservation held as a cross-family obligation at the
contract-invariant level. Reddit API/data pricing and Milwaukee public-sector
package structure are different enough to support the core invariant that
source-visible bundle membership, framing, dependencies, packaging cues, and
sequence must not be flattened into isolated terms. Milwaukee remains the
shallower leg and does not prove full raw public-sector package capture
sufficiency.

Mode subordination held. Human-led, agent-assisted, structured public access,
archive/history, mixed, or rendered capture modes matter only because they
expose limits and repeatability. No mode itself proves capture quality.

## 7. What Failed Or Required Patch

One material core contract defect emerged: archive/history posture and
recapture relationships were too lossy if read as one rollup label per
capture. Unity showed that the same bounded capture can contain archived
historical state, failed exact access, cache attempt failure, not-attempted
timeline work, migrated current discussion state, and current cancellation
recapture. A single `archived` label could hide material source-state limits.

The archive/history defect required a narrow core patch. It generalized beyond
Unity because any mutable public URL, policy page, docs page, forum thread,
cache, migration, or archive snapshot can create the same failure mode.

Milwaukee exposed an evidence-depth limitation, not a contract defect. It
confirmed that public-sector package structure must be preserved, but it did
not prove raw Milwaukee package capture sufficiency.

ClickUp and Kubernetes produced no material core patch requirement. Both
surfaced satellite guidance and partial fixture limitations, but the current
contract already had the needed core obligations.

Reddit remained partial as a full raw handoff, but the current contract now
contains the related-chain, live-thread timing, raw-observable warning, and
package/segmentation obligations needed to handle the pressure it created.

## 8. Patch Incorporated From Archive/History Fixture Round

This section lists the narrow Unity/archive-history-driven patch incorporated
after the final fixture. It is not a complete history of every obligation added
or sharpened during the full pressure-test arc.

Earlier Reddit-driven pressure-test work is already reflected in the current
contract through related-chain preservation, live-thread timing, raw-observable
warning, and package/segmentation obligations. Those earlier changes are
credited in Sections 6 and 7; the bullets below are the archive/history round.

Exact contract areas patched from the archive/history fixture round:

- `Archive / Historical Posture`: requires archive/history posture per
  relevant source slice, source locator, archive/cache attempt, or fallback
  access path when cutoff, deletion, edit, cache, prior-window, migration,
  fallback, or visibility-shift risk is load-bearing. A rollup posture is
  allowed only when it does not hide failed, degraded, unavailable,
  not-attempted, fallback, migrated, or conflicting source states.
- `Source Visibility And Access Limits`: requires preservation of the
  relationship among original locator, current locator, migrated locator,
  archive/cache locator, fallback locator, and failed access attempt when
  visibility shifts.
- `Re-Capture Semantics`: requires recapture to preserve why it happened, what
  source state changed, whether the new capture supersedes, supplements, or
  conflicts with prior capture, and the relationship per material source slice
  or locator when changed, migrated, archived, cached, fallback, or
  failed-access states coexist.
- `Categorical Handoff Sufficiency`: requires downstream handoff to keep
  original, historical/archive/cache, current/migrated, fallback, failed
  access, changed-source-state, and supersede/supplement/conflict
  relationships visible at the relevant source-slice level.
- `Capture Failure And Blocker Visibility`: carries exact-access failure,
  archive attempt failure, fallback success, and changed-source-state
  limitations as visible capture facts rather than hidden collection defects.

Why the patch stayed product-method and did not become runtime, schema, or
tooling:

- It defines what must remain visible, not how to store it.
- It does not introduce ECR fields, IDs, tables, keys, data types, schemas,
  receipts, file formats, or storage.
- It does not design archive tooling, cache services, source maps, dashboards,
  scrapers, APIs, adapters, automation, or tests.
- It does not define Cleaning transformations, dedupe, clustering,
  normalization, summarization, or exclusion mechanics.
- It preserves the obligation boundary: Capture exposes posture and limits;
  downstream layers decide sufficiency and use.

## 9. Satellite Guidance Accumulated

The guidance below is source-family adaptation. It should help future capture
operators preserve the core obligations in each family, but it is not promoted
to core unless separately supported by cross-family comparison or owner
sign-off for a specific invariant.

Threaded/community satellite guidance:

- Preserve the original post or parent claim, signal-bearing comment or reply
  path, direct corrections, rebuttals, confirmations, official or moderator
  responses, resolution/lock/edit/deletion posture, and boundary reason for
  excluding unrelated thread branches.
- Preserve thread creation timing separately from relevant comment, reply,
  update, edit, capture, and cutoff timing where visible.
- Keep Reddit-specific mechanics, subreddit conventions, Pushshift context,
  sorting behavior, permalink behavior, and moderation cues in satellite.

Bundle/package/public-sector satellite guidance:

- Preserve bundle membership, source-visible framing, dependencies,
  severability, conditionality, sunsets, fallback posture, sequence, and
  packaging cues where visible.
- Keep public-sector negotiation conventions, WRS-specific interpretation,
  state/city motive questions, and package-as-Judgment-signal primitives out
  of Capture core.

Review-surface satellite guidance:

- Preserve rating and full visible text together, title, review date,
  experience timing where labelled, recency, reviewer-visible actor context,
  verification/invite/incentive labels, vendor response, sort/filter posture,
  moderation language, removal or score-inclusion posture, and platform
  summaries as platform artifacts.
- Escalate to rendered or expanded capture when text extraction hides labels,
  truncation, badge state, response placement, or filter state.
- Do not convert review labels into credibility, independence,
  representativeness, inclusion, discounting, or exclusion.

Docs/changelog/versioned-page satellite guidance:

- Preserve live docs, release notes, changelogs, policies, pricing pages,
  API references, official prior-version snapshots, repository source, cache,
  and archive surfaces as distinct source states.
- Preserve exact tense when it carries signal, such as future-state versus
  current-state wording.
- Preserve event timing separately from page publication, page last-modified,
  section-level update, version posture, capture timing, and recapture timing.
- Treat page-level metadata scope, static snapshot banners, version menus,
  current support state, and cutoff leakage as visible posture, not automatic
  historical proof.

Archive/history and recapture satellite guidance:

- Preserve original live URL, current URL state, migrated URL, archived
  snapshot URL, cache attempt URL, fallback/mirror/community URL, and failed
  access attempt separately when they carry different states.
- Preserve archive snapshot timestamp separately from source publication,
  update, capture, recapture, and decision cutoff timing.
- Distinguish replacement, migration, archive-only state, cache failure,
  degraded access, current-state supersession, historical supplement, and
  conflict by cutoff question.
- Do not require every capture to enumerate every archive. Require visible
  posture for routes used, failed, source-limited, not attempted, or
  unnecessary for the commissioned decision.

## 10. Core Obligation Implications

What should remain core:

- Commissioned-capture gate and rejection of free-floating standing corpus
  capture inside Data Capture Spine v0.
- Public, market-level, non-deceptive, non-intrusive boundary compliance.
- Capture-event provenance, capture mode disclosure, and mode-change
  visibility.
- Raw observable preservation and source claim separated from Orca
  interpretation.
- Source identity, source carrier, and visible actor category preservation
  where knowable.
- Decomposed timing and cutoff posture.
- Archive/history posture and recapture relationship visibility at the
  relevant source-slice or locator level when multiple states coexist. This is
  a core rule from the Unity fixture plus generalized mutable-source reasoning,
  pending owner acceptance; it is not proven across a broader archive corpus.
- Source visibility and access-limit visibility.
- Related context preservation and fairness boundary.
- Bundle/package structure preservation as source-visible observable when the
  source presents a multi-term proposal.
- Failure and blocker visibility.
- Categorical handoff sufficiency without ECR, Cleaning, Judgment, or runtime
  design.
- Forbidden Capture outputs: credibility, weighting, discounting, exclusion,
  Decision Strength, Action Ceiling, Signal Use Classification, Cleaning
  transformations, ECR schema, source scoring, and source maps as core.

What should remain satellite:

- Platform-specific review labels and moderation mechanics.
- Reddit-specific thread, subreddit, API-pricing, and Pushshift mechanics.
- Kubernetes-specific version menu, release-page, GitHub-source, and docs-site
  conventions.
- Unity-specific Wayback/cache/forum migration mechanics.
- Milwaukee-specific public-sector package, pension-reform, and negotiation
  interpretation cues.
- Rendered-capture escalation heuristics by source family.
- Archive-route selection playbooks and human-escalation defaults by source
  family.

What remains open:

- Owner acceptance or rejection of the patched contract.
- Full adversarial review of this synthesis and the patched contract state.
- Whether multimodal/dynamic-page capture needs a separate required fixture.
- Which source families require archive attempts rather than visible
  archive/history posture only.
- What recapture threshold avoids churn while preserving meaningful source
  changes.
- Which source families require human-led capture by default until a future
  engine can discharge obligations.
- Where ECR later draws the line between related context and irrelevant source
  exhaust.
- Runtime/source-system feasibility, if later authorized.

## 11. Downstream ECR / Cleaning Advisory Notes

These notes are categorical only. They do not define fields, IDs, keys, tables,
schemas, storage, file formats, transformations, source maps, APIs, scrapers,
dashboards, automation, or runtime behavior.

Future ECR work should expect Data Capture to preserve categories sufficient
to inspect:

- raw observable and related source context;
- source carrier and visible actor category;
- source claim versus Orca interpretation;
- capture provenance and mode;
- event, edit/version, capture, recapture, and cutoff timing;
- archive/history, cache, fallback, migration, and access posture;
- source visibility limits, blockers, and failure states;
- review rating/text/label context where review surfaces are used;
- docs/version/current/future/deprecated/removed posture where versioned pages
  are used;
- bundle membership, framing, dependencies, packaging cues, and sequence where
  multi-term proposals are used;
- recapture supersede/supplement/conflict relationship at the relevant source
  state.

Future Cleaning work should preserve source-state relationships before any
reduction. It should not flatten:

- threaded related chains into isolated claims;
- review text into sentiment or platform summary;
- versioned docs into a single current-state statement;
- historical and current pages into one source identity;
- package structure into unordered terms;
- failure and access limits into absence;
- post-window material into pre-cutoff context.

These are advisory carry-forward categories only. They are not Cleaning
transformations and not ECR design.

## 12. Readiness / Non-Readiness Statement

What can be said:

```text
Data Capture Spine obligation contract is pressure-tested across the planned fixture set and appears stable enough for advisory downstream design input, subject to owner acceptance and adversarial review.
```

What must not be said:

- Data Capture Spine is closed.
- The owner has accepted the contract or this synthesis.
- The contract is formally validated.
- Any artifact is promoted to source of truth by this synthesis.
- ECR is ready, designed, or authorized.
- Cleaning is ready, designed, or authorized.
- Runtime tooling, archive services, source maps, scrapers, APIs, dashboards,
  storage, tests, automation, or implementation are ready or authorized.
- Fixture count proves correctness.
- Satellite guidance has become core without cross-fixture comparison or
  explicit owner sign-off.
- Captured signals are credible, representative, included, excluded,
  discounted, weighted, or decision-useful.

## 13. Remaining Not-Proven Boundaries

Not proven:

- owner acceptance;
- formal validation;
- source-of-truth promotion;
- Data Capture closure;
- ECR schema, receipt architecture, field design, storage, or handoff format;
- Cleaning Spine design, transformations, dedupe, clustering, normalization,
  summarization, or exclusion mechanics;
- Judgment Spine readiness;
- runtime or source-system feasibility;
- archive tooling choice or archive service reliability;
- source rights or data-rights sufficiency;
- buyer proof, willingness to pay, commercial readiness, or repeatable demand;
- implementation readiness;
- complete raw source-level capture sufficiency for Milwaukee;
- complete raw review-body preservation for ClickUp beyond fixture slice;
- exact historical visibility for every Kubernetes or Unity source state
  beyond what the fixture artifacts recorded;
- deletion where the fixture only showed replacement, migration, archive-only
  state, or failed/degraded access;
- multimodal sufficiency, unless separately admitted and tested.

## 14. Recommended Next Routing Object

Recommended next routing object: full adversarial artifact review of this
synthesis.

The review should inspect:

- whether this synthesis overclaims the fixture set;
- whether Milwaukee weakness is adequately bounded;
- whether the archive/history patch is stated as sufficient only for the
  observed defect;
- whether satellite guidance is kept out of core;
- whether downstream ECR/Cleaning notes stay categorical;
- whether the allowed stability statement is justified without implying
  acceptance, validation, readiness, or source-of-truth promotion.

Do not route directly to ECR/Cleaning design as if Data Capture were accepted.
Any advisory downstream design input should be treated only as constrained
input under the claim above, still subject to owner acceptance and adversarial
review.

```yaml
data_capture_fixture_synthesis:
  status: SYNTHESIS_DRAFT_V0
  artifact_path: docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md
  patched_contract_hash: A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF
  fixture_hashes:
    remaining_fixture_plan: D4BC5D2983F8EC490AD3154A3C748014A71B123364D73AFF8E8C2743297C0584
    reddit_threaded_forum_api_pricing: AFD177CA51A1374011702B59A3ED90A3C9CE792223B64235B0F5CEE458526206
    milwaukee_public_sector_package: 3C556E05D1653B732386E820FE6348FB95C66A31E38CA26A5BB3BD5B0CB93B92
    clickup_review_surface: 85AF08DAED6F3E2E89AA317CD3C2AEEC756CE8F1B311E1EB0D4EED55A95AF9C6
    kubernetes_docs_changelog_versioned_page: AE61EE89E0704F68B353D71CEB3BC8EDAC2E1F66A68C5A8C78A29B62028758F6
    unity_archive_history_recapture: 7962B20EE1DDB3F7E920A0BFA78DB47B2DA489D9A35A81FA630686C84626F3EC
  recommendation: Route to full adversarial artifact review before any owner acceptance, promotion, or stronger downstream move.
  next_routing_object: Full adversarial artifact review of this synthesis.
  strict_claims_not_made:
    - Data Capture closure
    - owner acceptance
    - formal validation
    - source-of-truth promotion
    - ECR/Cleaning readiness
    - runtime/tooling readiness
    - implementation readiness
```
