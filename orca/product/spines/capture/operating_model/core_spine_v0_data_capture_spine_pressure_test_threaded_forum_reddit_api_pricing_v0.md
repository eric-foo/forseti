# Core Spine v0 Data Capture Spine Pressure Test - Threaded Forum Reddit API Pricing

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Pressure-test of the draft Data Capture Spine Obligation Contract against MV-05 Reddit API/data pricing threaded-forum and package/segmentation capture surfaces.
use_when:
  - Checking how Data Capture Spine v0 handles threaded-forum capture.
  - Checking how Data Capture Spine v0 handles API/data pricing package or segmentation observables.
  - Preparing future ECR or Cleaning design notes about related-chain preservation.
open_next:
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
input_hashes:
  docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md: 4F27F8D2A1099A03FC2E13457502F126DA73009B5E485F5B7B43F994D01128E5
  docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md: 102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B
  docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md: DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D
  docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md: AFB12D3DEC79F0FCDDC07AAC6976CB6528828105690A733873E2101C10CE1930
branch_or_commit: main at 5e999c1 with dirty/untracked workspace sources
stale_if:
  - The Data Capture Spine Obligation Contract is patched on threaded-forum capture.
  - The Data Capture Spine Obligation Contract changes bundled-offer or multi-term proposal obligations.
  - MV-05 is superseded by a later accepted replay or source-loading artifact.
  - Future ECR or Cleaning architecture accepts a different related-chain boundary.
authority_boundary: retrieval_only
```

- Status: PRESSURE_TEST_REFRESHED_V0
- Source pack: custom S4, bounded to Data Capture contract/context/blueprint, this artifact, and the MV-05 Reddit capture surface.
- Implementation authorized: no.
- Contract patch applied here: no.
- Reddit judgment rerun: no.
- Refresh reason: the Data Capture contract now includes bundled-offer / multi-term proposal preservation; prior artifact hash before this refresh was `D033EB52FCA24DBBB7B090D7DD379F49EEB87D67765608C5C3AE7E133CE4B83B`.

## Purpose

This artifact pressure-tests whether the draft Data Capture Spine Obligation Contract handles threaded-forum capture and package/segmentation preservation correctly using MV-05 Reddit API/data pricing as the case.

It does not decide whether Reddit should price APIs, rescore source credibility, rerun MV-05, redesign ECR, redesign Cleaning, design runtime capture, create source maps, or specify scrapers, APIs, storage, dashboards, or tests.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S4
  edit_permission: docs-write for this pressure-test artifact only
  target_scope:
    - docs/product/core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
    - docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md
    - docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - Orca overlay authority
    - Data Capture obligation contract
    - MV-05 Reddit replay artifact
```

No required source was missing. The workspace was dirty and several target product-method files were untracked. The current user instruction bounded these files as the source pack for this pressure test; that does not prove broader acceptance, validation, readiness, source-of-truth promotion, or product-method hardening.

## Source Context

SOURCE_CONTEXT_READY was declared before applying the method.

Refresh read note: this refresh read `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/artifact-folders.md`, `.agents/workflow-overlay/artifact-roles.md`, `.agents/workflow-overlay/validation-gates.md`, targeted Data Capture contract/context/blueprint sections, this artifact, and only MV-05 sections needed to inspect the Reddit API/data pricing capture surface. Contaminated archive bodies and public web research were not read.

| Source | Why opened | Status in git state | Use in this artifact |
| --- | --- | --- | --- |
| `AGENTS.md` | Orca project instructions and overlay requirement | tracked, supplied/read | Controlling project work boundary. |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | modified | Overlay route; dirty status prevents strict acceptance claims. |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | modified | Current-turn instruction, AGENTS, overlay, then docs. |
| `.agents/workflow-overlay/source-loading.md` | Custom S4 source loading and preflight | modified | Source loading, dirty/untracked handling, and readiness boundary. |
| `.agents/workflow-overlay/artifact-folders.md` | Destination folder authority | modified | Confirms `docs/product/` is an accepted product artifact location. |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact role and permission boundary | modified | Confirms docs-only product artifact role. |
| `.agents/workflow-overlay/safety-rules.md` | Forbidden implementation/runtime/source-system drift | modified | Prevents implementation, runtime, commits, or external mutation. |
| `.agents/workflow-overlay/validation-gates.md` | Completion-gate and dirty-state strict-claim limits | modified | Prevents readiness or validation overclaims. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Header rules for durable artifacts | modified | Shapes this artifact header. |
| `docs/workflows/artifact_retrievability_guide.md` | Body-opening guidance | tracked/read | Shapes purpose, stale, source, and non-claim sections. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Target contract under pressure test | untracked | Primary object tested. |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Data Capture architecture boundary | untracked | Confirms capture/ECR/Cleaning/Judgment layer split. |
| `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md` | Context preservation rule | modified/read | Confirms related chain versus source exhaust rule. |
| `docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md` | Threaded-forum case | untracked | Case evidence surface for this pressure test only. |

## Case Boundary

MV-05 is not a pure Data Capture artifact. It is a method-validation replay with first-order and second-order evidence units (EvidenceUnit), Signal Integrity labels, Signal Use Classification, Decision Strength, Action Ceiling, an at-cutoff memo, and post-window calibration.

For this pressure test, only the capture-relevant surfaces are used:

- the accepted decision frame;
- the compact source-read ledger;
- blocked and unused source handling;
- anti-leakage ledger;
- post-window source opening only after seal;
- explicit not-proven and source-visibility boundaries;
- source limitations implied by live Reddit pages, comment accretion, thread context, related-chain preservation, and API/data pricing segmentation.

The downstream MV-05 judgment sections are treated as downstream material, not as Capture obligations.

## Core Finding

The draft contract handles the main threaded-forum principle correctly: Capture should preserve the smallest related chain that makes the source claim inspectable and fairly situated, not the entire unrelated forum.

The pressure point is discharge specificity. The contract says the right thing at the principle level, but MV-05 shows that live Reddit-style threads need a clearer minimum capture receipt. A compact source-read ledger with title/date/claim is enough for method replay traceability, but it is not enough by itself to satisfy Data Capture raw observable and related-chain obligations.

The current contract adds a second pressure dimension that the original artifact did not cover: Reddit API pricing is also a package/segmentation capture surface. Capture must preserve source-visible structure across categories and terms instead of flattening AI/data access, third-party apps, moderator tools, accessibility, research, rate limits, exemptions, effective dates, and later official clarifications into a single "API pricing" summary.

Recommended contract change status: the prior threaded-source clarification remains useful. The bundled-offer / multi-term obligation itself is no longer missing from the contract; this artifact now refreshes the Reddit case to test that added obligation.

## Bundle / Package Structure Refresh

Prior findings that remain valid:

- threaded-forum discharge specificity still matters;
- source-read ledgers and short title/date/claim rows are not raw observable preservation when thread context or package structure carries meaning;
- cutoff posture, post-window seal discipline, blocked-source visibility, and layer separation remain valid findings;
- Capture must not decide credibility, representativeness, discounting, exclusion, Signal Use Classification, Decision Strength, Action Ceiling, app economics, shutdown likelihood, or Reddit motive.

Prior findings that are stale or incomplete:

- the artifact is stale where it frames MV-05 only as a threaded-forum case;
- the obligations table was stale because it omitted Bundled-Offer Structure Observables;
- the contract-patch recommendation was incomplete because it addressed related-chain discharge but not package/segmentation preservation;
- the bottom line was incomplete because Reddit remains useful as a fixture for both threaded-source context and multi-term policy/package capture.

Does Reddit API pricing create a package/segmentation capture obligation? Yes. MV-05's capture surface shows API/data pricing across source-visible use categories rather than one undifferentiated term: AI/data access, large commercial use, third-party apps, moderator and governance-critical tooling, accessibility, research, rate limits or higher limits, contract/approval/premium access, exemptions, migration or effective-date posture, and official or post-window clarifications where visible.

What raw observable structure must Capture preserve:

- which categories and terms appear together in the same official update, thread, developer post, report, or post-window clarification;
- source-visible framing such as commercial use, higher limits, approval, premium access, exemption, assurance, safeguard, migration path, or unresolved pricing uncertainty;
- dependencies and severability, including what appears bundled together, what appears exempted, what is conditional, and what remains unknown;
- visible timing and sequence, including pre-cutoff official direction, Pushshift access change, Apollo pricing uncertainty, and post-window clarifications opened only after seal;
- packaging cues where visible, including headings, labels, bullet grouping, nesting, order, proximity, and official/developer wording;
- source-visible limits when exact prices, eligibility, effective dates, exemption rules, or term dependencies are unavailable.

Capture must preserve that structure without inferring Reddit motive, private costs, app economics, willingness to pay, shutdown likelihood, credibility, representativeness, Decision Strength, or Action Ceiling.

## 1. Obligations Tested

| Obligation | MV-05 pressure-test surface | Result |
| --- | --- | --- |
| Commissioning Gate | Accepted decision frame with decision question, owner/context, cutoff, allowed verbs, reliable-bet threshold | Held cleanly. |
| Boundary Compliance | Public Reddit, RedditInc, public reporting, blocked direct fetches, no private access | Held for boundary; visibility limits remain separate. |
| Capture-Event Provenance | Repository state checked, source-read ledger, anti-leakage ledger | Partial. Capture session identity and contract-version surface are not complete. |
| Capture Mode Disclosure | Opened pages, failed fetches, post-seal opens, public source loading | Partial. Capture mode categories are not explicitly discharged per source. |
| Mode-Change Rule | Failed direct fetches, blocked Reddit candidates, post-window opens after seal | Partial. Failure and timing are visible, but mode changes are not named as mode changes. |
| Raw Observable Preservation | Ledger records short title/date/claim only | Partial. Adequate for replay summary, not enough for Data Capture handoff. |
| Source Identity And Actor Context | Official Reddit sources, r/reddit, r/Devvit, Apollo developer, reporting sources | Mostly held categorically; exact actor/source-carrier separation should be stricter for threads. |
| Decomposed Timing | Source dates, cutoff, post-window seal, post-window open status | Held for cutoff discipline; partial for per-comment timing, edits, and live-thread accretion. |
| Cutoff Posture | Pre-cutoff sources, post-window-only sources, seal marker, anti-leakage ledger | Held cleanly. |
| Archive / Historical Posture | Visibility basis and blocked fetches recorded | Partial. Archive posture is not discharged per Reddit source. |
| Source Visibility And Access Limits | Blocked NYT, blocked Reddit result opens, snippet noise, usable public pages | Held for blockers; partial for live Reddit page limitations and dynamic thread state. |
| Related Context Preservation | Threaded sources include official update, Pushshift access thread, Apollo thread | Conceptually held by contract; not fully discharged by MV-05 artifact body. |
| Bundled-Offer Structure Observables | API/data pricing appears across AI/data access, third-party apps, moderator tooling, accessibility, research, rate limits, exemptions, and post-window clarifications where visible | Newly tested; partial. Reddit creates a package/segmentation capture obligation, but MV-05 does not preserve enough source-visible bundle structure for full handoff. |
| Capture Failure And Blocker Visibility | Blocked/unused rows and source-visibility blocker section | Held cleanly. |
| Re-Capture Semantics | Post-window sources opened after seal; no actual recapture | Mostly not tested. Future live-thread recapture remains open. |
| Categorical Handoff Sufficiency | MV-05 has enough to support replay audit, not a raw capture handoff | Partial. ECR/Cleaning could not reconstruct full related chains without re-fetching. |

## 2. Obligations That Held Cleanly

Commissioning Gate held cleanly. The accepted decision frame gave Capture a bounded reason to exist: Reddit API/data pricing before a 2023-05-30 cutoff, with specific owner context and allowed decision verbs. This is the difference between commissioned capture and broad forum mining.

Boundary Compliance held cleanly. MV-05 used public surfaces and recorded failed or blocked access instead of working around them. Nothing in the capture-relevant material requires private access, deceptive collection, ordinary-person dossiers, or out-of-bound acquisition.

Cutoff Posture held cleanly. The case clearly separates pre-cutoff evidence from post-window outcome sources, records a seal marker, and states that post-window sources were opened only after seal. This is one of the strongest contract fits.

Capture Failure And Blocker Visibility held cleanly. Blocked direct-source attempts and unused Reddit candidates are visible. That is exactly what Capture should do: preserve failure and non-use status without turning failure into a hidden filter.

The captured-but-unusable boundary also held conceptually. MV-05 shows that a source can be captured and still later be downgraded, capped, excluded, or used only narrowly by downstream Judgment. Capture should not make those calls.

## 3. Obligations Needing Tightening, Splitting, Or Satellite Movement

Raw Observable Preservation needs tightening for threaded forums. MV-05's compact ledger intentionally preserves only short title/date/claim. That is not enough for a commissioned Data Capture handoff if the source claim depends on thread context. The contract should state that a ledger row is not a substitute for preserving the raw related-chain observable.

Related Context Preservation needs a sharper threaded-source floor. The current contract already says "preserve the related chain, not the entire forum." The pressure test shows that future operators need to know what makes the chain minimally inspectable: original post or parent claim, direct replies that change meaning, official or moderator responses, visible corrections/rebuttals/confirmations, deletion/edit/lock posture, comment timing where visible, and a reasoned boundary for excluding unrelated comments.

Decomposed Timing and Cutoff Posture need a live-thread cross-rule. A Reddit thread can be pre-cutoff by original post date but mixed by later comment accretion, edits, updates, or post-cutoff official replies. Capture should record per-item or per-chain timing where visible, or mark the timing as mixed/unknown. A single thread publication date is not enough when the related chain crosses the cutoff.

Archive / Historical Posture needs a threaded-forum limitation rule. For live mutable pages, `not_attempted` may be acceptable only if it is explicit and paired with a limitation. If archive/history access fails, the failure should be visible per source or per related chain.

Capture-Event Provenance and Capture Mode Disclosure should not force runtime design, but they should require enough session/mode detail to distinguish live web open, archive/history open, structured access, agent-assisted enumeration, and human judgment about related-chain boundaries.

Source Identity And Actor Context should split source carrier from actor more explicitly for threaded sources. A subreddit, a platform account, a moderator, an app developer, a reporter, and a commenter are different actor contexts even when they share the same carrier surface.

Re-Capture Semantics was not really tested. Live Reddit pages create a plausible recapture need when a thread is edited, locked, deleted, receives official replies, or changes meaning after initial capture. That should stay as core recapture semantics with source-family examples in satellite.

Bundled-Offer Structure Observables now need to be treated as an additional stress dimension, not a replacement for the threaded-forum finding. Reddit API/data pricing is a policy/package signal because the source-visible structure separates or bundles different user categories, access rights, limits, exemptions, timing, and clarifications. The original artifact is stale where it omitted this obligation.

## 4. Threaded-Forum Satellite Guidance That Emerged

Threaded-forum satellite guidance should cover how to identify the smallest related chain without turning Capture into forum exhaust.

Minimum threaded-chain guidance:

- preserve the original post, linked update, or parent claim that makes the captured comment interpretable;
- preserve the specific comment or reply path that carries the signal;
- preserve direct corrections, rebuttals, confirmations, official replies, moderator replies, and resolution or lock state when visible;
- preserve visible edit, deletion, removal, locked, pinned/stickied, sorted, collapsed, or unavailable-state posture when it changes meaning;
- preserve source-visible actor category, such as official platform account, developer, moderator, maintainer, app developer, end user, reporter, or unknown commenter;
- preserve timing separately for thread creation, relevant comment or update timing, capture timing, cutoff posture, and post-window accretion where visible;
- mark when live-page capture cannot determine whether comments were present before the cutoff;
- record why unrelated comments, neighboring subreddit discussion, or broad forum history were outside the related chain.

Reddit-specific guidance should stay satellite, not core. Examples include subreddit conventions, permalink behavior, visible moderation states, Pushshift-specific context, API-update subreddit identity, Devvit audience context, Apollo app-developer audience context, and how Reddit exposes deleted or edited comments.

## 5. Future ECR / Cleaning Note

Future ECR and Cleaning work should preserve the distinction between related-chain preservation and full-forum exhaust.

Capture's job is to preserve enough chain context to make later stripping defensible. ECR or Cleaning may later reduce the material to a smaller evidence slice, normalized excerpt, or receipt, but the reduction should remain traceable to the related chain that Capture preserved.

For MV-05-like threaded sources:

- ECR should not need to re-fetch Reddit to know what the source was claiming.
- Cleaning should not carry an entire subreddit, unrelated thread branches, or broad forum history.
- Cleaning should not erase the parent claim, direct reply path, official response, correction, or timing fact that made the slice fair.
- Post-window outcome sources should remain visibly post-window and should not be merged into pre-cutoff chain context.
- Blocked or unused Reddit candidates should remain failure/provenance material, not negative evidence and not source-quality scoring.
- Package/segmentation structure should remain visible enough that downstream reduction does not flatten distinct access categories, exemptions, rate-limit posture, timing, or official/developer clarifications into one generic "pricing" term.

This pressure test does not design ECR fields, receipt IDs, storage keys, schemas, source maps, dedupe logic, or transformation rules.

## 6. Layer Separation Check

Capture stayed separate from Judgment, Cleaning, and ECR in this pressure test.

The contract preserves the layer split: Capture records raw observables, context, timing, visibility, archive/cutoff posture, and limits. It does not decide credibility, representativeness, discounting, exclusion, Signal Use Classification, Decision Strength, or Action Ceiling.

MV-05 itself is a mixed replay artifact with downstream judgment sections. This pressure test did not reuse those sections as Capture. It used them only as a boundary reminder: the existence of Signal Integrity, Decision Strength, Action Ceiling, and at-cutoff recommendation sections shows why Capture must have a cleaner handoff surface than a replay memo.

Capture also stayed separate from Cleaning. No semantic dedupe, normalization, clustering, excerpt stripping, or source transformation is specified here.

Capture stayed separate from ECR. This artifact recommends preserving enough related-chain context for future ECR work, but it does not define ECR fields, records, IDs, schemas, or data types.

## 7. Contract Patch Recommendation

Patch recommended: yes for threaded-source discharge specificity; no for adding the bundled-offer obligation itself, because the current contract already includes it.

Bundle refresh status: the prior artifact was stale because it did not test Bundled-Offer Structure Observables. This refresh treats Reddit API pricing as a package/segmentation capture surface, but it does not recommend another contract patch until more bundled or multi-term proposal cases are compared.

Recommended patch 1: add a threaded-source discharge floor under Related Context Preservation.

```text
For threaded sources, a related-chain capture is not satisfied by a title/date/claim ledger row alone. Preserve the original post or parent claim, the specific signal-bearing comment or reply path, direct corrections/rebuttals/confirmations, official or moderator responses where visible, resolution/lock/edit/deletion posture where visible, and the boundary reason for excluding unrelated thread branches or forum material.
```

Recommended patch 2: add a live-thread timing cross-rule under Decomposed Timing or Cutoff Posture.

```text
For live or mutable threaded pages, distinguish thread creation timing from relevant comment/update timing, capture timing, and cutoff posture. If the captured page may include post-cutoff accretion or edits, mark the chain as mixed or unknown unless item-level timing makes the boundary clear.
```

Recommended patch 3: add a raw-observable warning under Raw Observable Preservation.

```text
Source-read ledgers, summaries, and title/date/claim rows are provenance aids. They do not by themselves preserve the raw observable when source meaning depends on thread context, modality, layout, edits, or related replies.
```

Recommended patch 4: keep source-family implementation details in satellite guidance.

```text
Core owns the related-chain obligation and timing/visibility limits. Satellite guidance owns Reddit-specific mechanics, subreddit conventions, comment sorting, permalink behavior, platform moderation cues, Pushshift context, and source-family escalation rules.
```

Do not patch in source maps, runtime capture, scrapers, API plans, storage, dashboards, ECR schema, Cleaning transformations, or Judgment criteria.

## Source-Specific Pressure Notes

### API Pricing Package / Segmentation Surface

Reddit API/data pricing should be captured as a source-visible package or segmentation surface where the source presents different treatment for AI/data access, commercial use, third-party apps, moderator tooling, accessibility, research, rate limits, higher-limit or premium access, exemptions, migration windows, effective dates, and later official clarifications.

Capture should preserve which terms appear together, which terms appear exempted or conditional, where exact prices or eligibility are unknown, and whether the source is pre-cutoff, post-window-only, mixed, or unknown. It should not infer Reddit motive, app-level economics, shutdown likelihood, credibility, representativeness, Decision Strength, or Action Ceiling.

### r/reddit API Update Thread

The r/reddit API update thread is an official or near-official platform thread. For Data Capture, the minimally fair slice would include the official post, the parts of the thread that explain API direction and developer/moderator assurances, any visible official clarifications, direct corrections or rebuttals, timing, and visible lock/edit/deletion posture.

The entire r/reddit forum is not required. Unrelated community reaction branches are not required unless they directly alter the source claim being captured.

### r/Devvit / Pushshift Access Thread

The r/Devvit Pushshift access thread is a threaded-source case where actor and audience context matter. Capture should preserve the official or platform-facing post, Pushshift access/change claim, moderator/tooling dependency context, visible official replies or clarifications, direct user/moderator responses that change the operational-risk reading, and timing/cutoff posture.

This is not a reason to promote Pushshift mechanics into core. The core obligation is to preserve the related chain and visible limits; Pushshift and Devvit conventions belong in satellite guidance.

### Apollo App Developer Thread

The Apollo developer thread is a direct developer-stakeholder thread. Capture should preserve the developer's original post and update, visible relationship to Reddit calls, explicit pricing-uncertainty posture, direct replies that materially clarify or dispute the claim, and timing around pre-cutoff versus post-cutoff knowledge.

The capture should not infer app-level economics, shutdown likelihood, credibility, or representativeness. Those are downstream Judgment or post-window calibration matters.

### Blocked / Unused Reddit Candidates

Blocked or unused Reddit candidates were handled correctly as capture failures or non-use rows. Future Capture should preserve the locator, access attempt, failure mode, timing, and whether the candidate was unused because it was inaccessible, out of scope, post-window, duplicative by exact locator, or not needed after bounded source loading.

It should not silently omit blocked Reddit candidates, and it should not treat blocked candidates as evidence against or for the decision.

### Post-Window Sources After Seal

Post-window sources opened after seal were handled correctly for leakage control. For future Capture, a live thread opened after seal must still carry timing posture: post-window-only, mixed, or unknown. Post-window outcome sources should not be folded into a pre-cutoff related chain.

## Not-Proven Boundaries

- Not proven: MV-05 as written satisfies full Data Capture handoff obligations.
- Not proven: the untracked Data Capture contract or MV-05 replay is accepted Orca source-of-truth beyond this current-turn bounded pressure-test source pack.
- Not proven: a future ECR or Cleaning design can use these recommendations without its own source-gated design work.
- Not proven: live Reddit pages preserve the same content, comments, edits, moderation state, or visibility observed during MV-05.
- Not proven: archive/history posture was sufficient for each Reddit source.
- Not proven: exact per-comment cutoff status for all related Reddit thread material.
- Not proven: MV-05 preserves source-visible package membership, dependencies, exemptions, effective dates, or pricing-term sequence enough for full Data Capture handoff.
- Not proven: Reddit motive, private costs, app economics, exact prices, willingness to pay, shutdown likelihood, or post-window official clarifications were visible before cutoff unless directly source-visible in the bounded replay.
- Not performed: Reddit judgment rerun, source credibility scoring, source-map creation, runtime capture design, API/scraper/storage/dashboard design, or contract patch application.

## Explicit Non-Claims

- No Reddit judgment rerun.
- No product readiness.
- No feature readiness.
- No implementation readiness.
- No data-pipeline readiness.
- No model-training readiness.
- No buyer validation.
- No repeatability proof.
- No source-of-truth promotion.
- No claim about Reddit motive unless directly source-visible.
- No claim that public evidence proved private willingness to pay.
- No claim that app shutdowns, protests, or later data deals were visible before cutoff.
- No ECR, Cleaning, runtime capture, source map, scraper, API, storage, dashboard, test, commit, push, or PR authorization.

## Bottom Line

The obligation contract remains directionally sound for threaded forums, and Reddit remains useful as a Data Capture fixture for two reasons: it stresses related-chain preservation in live threaded sources, and it now also stresses package/segmentation preservation for API/data pricing terms. Capture should preserve the smallest fair related chain and the source-visible package structure; it should not preserve the entire unrelated forum, flatten the policy package into a generic pricing summary, or infer downstream judgment effects.
