# Source Capture Armory

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Product-facing index and design guide for the bounded Source Capture Armory.
use_when:
  - Scoping, implementing, reviewing, or extending bounded Data Capture source-access tooling.
  - Checking what each Source Capture Armory component does.
  - Distinguishing source capture tooling from Source Observability, ECR, Cleaning, Judgment, or deferred source-access adapters.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/source_families/README.md
stale_if:
  - The source-access tooling build authorization is amended or superseded.
  - The source-access boundary decision materially changes hard stops or disclosability requirements.
  - The Data Capture obligation contract materially changes capture obligations.
  - A first-tranche implementation decision changes the packet shape, adapter set, or output lifecycle.
```

## Status

Status: `SOURCE_CAPTURE_ARMORY_README_V0`.

This folder is the product-facing home for Source Capture Armory design notes,
implementation-facing docs, gap registers, and future scoped specs.

Existing controlling artifacts are not moved into this folder. They remain in
their original product/decision locations because those paths are already cited
by source-loading, reviews, decisions, and propagation receipts. This README
indexes them so future armory work has one entrypoint without breaking
historical references.

## Why This Armory Exists

The Data Capture pressure tests showed repeated source-observability pressure:
source language, source structure, media, archive body state, access posture,
cutoff posture, and acquisition receipts need to stay inspectable.

If each fetcher, archive helper, browser snapshot, or media preserver writes its
own output shape, downstream work inherits adapter-specific mess. The armory
exists to make every capture path emit the same kind of Source Capture Packet (CapturePacket)
before more adapters are added.

The packet is the shared capture container. The Data Capture obligation contract
remains the spine-level authority. Adapters are replaceable ways to fill the
packet without redefining Capture obligations.

## Known Source-Family Routing

The Armory and playbook own source-access method and shared capture tooling.
Known source families now have a separate cold-start route home:

`forseti/product/spines/capture/core/source_families/README.md`

Use that catalog after the access-method read identifies a known family. The
catalog points to the family README, runner/projection/lake/cleaning seams, and
accepted residuals. It does not restate Data Lake raw admission, derived layout,
Silver, ECR, Cleaning, or Judgment authority.

## Controlling Sources

| Source | What It Controls |
| --- | --- |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | Canonical capture method: Step 0 access gate, route catalog/selection, receipt discipline, and recency/current-state / engagement-resonance preservation priority. Recent/current high-attention or source-visible public-reaction markers raise preservation urgency only; they do not prove demand, change access, create a score, or bind a route. |
| `forseti/product/spines/capture/core/source_families/README.md` | Known source-family lane catalog: routes from the generic playbook/Armory into the owning family index for Fragrantica/Parfumo/Basenotes, Retail/PDP, vendor pricing pages, Instagram, TikTok, YouTube, Reddit, creator registry, and cross-archive historical capture pointers. The catalog is routing-only; Data Lake, ECR, Cleaning, and runtime contracts remain in their owning lanes. |
| `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` | Whether bounded source-access tooling builds are authorized, including first/second/third-tranche scope, selected anti-blocking backend, and which adapters remain separately gated. |
| `docs/product/data_capture_source_access_method_plan_v0.md` | Candidate methods, sequence discipline, source-family method notes, and risk posture. |
| `docs/product/data_capture_source_access_boundary_decision_v0.md` | Source-access boundary, entitlement/disclosability standard, and hard stops. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Capture obligations, forbidden Capture outputs, and handoff discipline. |
| `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md` | Source Capture Packet lifecycle, durable citation, retention, and sensitivity handling before any fixture admission. |
| `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md` | Why pressure-test findings support moving from all-tools-deferred to bounded first-tranche tooling. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | Reusable operating profile for the smallest complete source-quality target per bounded source unit; not fixture admission, validation, source discovery, or Judgment authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` | Blank queue template for planning mini god-tier source-quality passes over already-bounded source units; not source selection, source discovery, or fixture admission. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md` | First mixed-source Mini God-Tier trial closeout; helper-input context only, not fixture admission, validation, or Judgment authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md` | One-source CW-P4 Mini God-Tier end-to-end pass evidence; read as operational closeout context only, not fixture admission, validation, or doctrine authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md` | One-source CW-P6 Mini God-Tier limitation-path pass evidence; read as operational closeout context only, not fixture admission, validation, or doctrine authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md` | One-source CW-P1 Mini God-Tier metadata-only negative-path pass evidence; read as operational closeout context only, not fixture admission, validation, or doctrine authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md` | Architecture boundary for a read-only Source Quality State Assembler over already-bounded rows and existing packets; state census only, not source discovery, runner dispatch, scoring, fixture admission, or Judgment authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md` | Slot 3 post-recapture Mini God-Tier source-quality closeout across Reddit batch 1, Reddit batch 2, and WSO; read as operational closeout context only, not fixture admission, validation, source completeness, or Judgment authority. |
| `forseti/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md` | Current operator procedure for bounded Reddit exact-thread capture with implemented Armory tools: old Reddit Direct HTTP batch first, quality summary, exact-URL archive fallback, CloakBrowser/proxy boundaries, warm same-context JSON as future/specialized enrichment, and no broad crawl or commercial-use claims. |
| `forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md` | Durable architectural planning thread for bounded pre-commercial Reddit capture/consolidation: exact old Reddit Direct HTTP as the current exact-thread operator default, CloakBrowser as the anti-blocking/browser-visible route when Direct HTTP is unsuitable or blocked, warm same-context Reddit JSON as a bounded enrichment path, packet-before-parser handoff, provenance-first consolidation shape, archive fallback, and non-implementation stop lines. |
| `forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md` | Advisory routing object that explains why the Reddit planning thread needs Decision-Frame-or-candidate classification, non-promoting success tiers, Armory vocabulary reuse, packet-contamination stops, no source-discovery expansion, and candidate-intake gap visibility. |
| `docs/workflows/screening_read_service_build_receipt_v0.md` | Build receipt and clean-agent usage pointers for the bounded screening-read service and `screening_browser_read` wrapper: orchestrator-invoked, public-only, no packet, no manifest, no ECR. |
| `docs/workflows/screening_read_reusable_findings_v0.md` | Cross-site reuse pattern for public browser/interstitial screening reads and same-shaped structured listing extraction: visible-text `block_shell`, row-local locators, and range sanity. |
| `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md` | Retail/PDP canonical-content, target-binding, Cleaning, residual, and Silver-handoff contract. |
| `forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md` | Five-site fragrance purchase-review row-capture receipt: ignored JSONL corpus location, per-source row counts, extraction substrates, validation read, and packet-window residuals; no raw review bodies in tracked docs. |
| `forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md` | Five-site fragrance purchase-review widget-expansion probe receipt: Judge.me/Yotpo route findings, pagination totals, rating/media filter diagnostics, ignored raw response paths, and current row-completion residuals; no raw review bodies in tracked docs. |
| `forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md` | Focused fragrance purchase-review coverage MGT target: Luckyscent pinned-route receipt, row-selection policy, adaptive cap, adapter shape, drift fallback contract, and accepted residuals; no raw review bodies in tracked docs. |
| `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md` | YouTube-first creator/channel observation ledger contract for admitted Shorts pools: one-platform source-backed observations, data-lake packet refs, metric absence posture, and explicit non-linkage/non-metric boundaries before profile projection or SQLite. |
| `forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json` | Static source-backed seed ledger for the full 200-row fragrance Shorts pool: 31 observed YouTube creator/channel groups, 200 matched raw lake packets, no cross-platform linkage, no metric rollups, no transcript bodies. Verifier: `orca-harness/capture_spine/youtube_creator_observation/`. |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md` | Proposed current-main IG beauty creator roster/frontier ledger contract: append-only public-name observations, depth-1 discovery provenance, privacy invariants, ontology boundary, and current `250 -> 500 -> 1,000` roster gates. Non-authorizing. |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md` | Dedicated Tier-2-B public-handle linkage contract across Instagram, TikTok, and YouTube: static table-shaped ledger, declared/probable/candidate/rejected link states, public evidence thresholds, validator expectations, and non-claims. No live capture, no contact/outreach, no person identity proof. |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json` | Populated static `public_handle_ledger` seed for source-backed YouTube and Instagram public platform accounts, with creator records still empty until public-handle linkage evidence is admitted. Validated by the creator public-handle linkage validator; no invented rows, live capture, contact/outreach, SQLite, or person identity proof. |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md` | Owner-directed target view for a one-stop current creator profile: joins public-handle identity, per-content metric observations, aggregate metric rollups, and ideal-audience snapshots without turning the identity ledger into one giant ledger. No SQLite adoption, dashboard implementation, live capture, or public person-level surface. |

## Armory Components

### Screening Read Service

Purpose: let the screen orchestrator read one public source in screening posture
without generating a Source Capture Packet.

The implementation lives in:

- `orca-harness/source_capture/screening_read.py`;
- `orca-harness/source_capture/screening_browser_read.py`;
- `orca-harness/source_capture/screening_extraction.py`.

It consolidates `reddit_screening_read`, `direct_http`, `anti_blocking_http`,
`block_shell`, and bounded extraction into screen-light records: status, bytes,
content class, block-shell signal/detail, and targeted extracted fields. It also
adds `screening_browser_read`, a thin wrapper over `cloakbrowser_snapshot` that
renders public pages and returns visible text only.

Boundaries: orchestrator-invoked, not walker-direct; public logged-out content
only; human-rate; one source / one question; no standing service, crawler,
scheduler, packet, manifest, ECR, Cleaning, or Judgment. Browser screening reads
classify `block_shell` on visible text, not full DOM.

For the validation receipt and first-act old Reddit search-surface closure, open
`docs/workflows/screening_read_service_build_receipt_v0.md`.

### Source Capture Packet Core

Purpose: create one standard local packet for a captured source or bounded
source set.

The packet core must be contract-derived. The list below is not an exhaustive
schema; it is the minimum product surface the implementation spec must preserve
from the Data Capture obligation contract before adapter-specific fields are
added.

Cardinality rule: a packet may cover one requested source or a bounded source
set, but it must preserve per-source-slice state when archive posture,
visibility, timing, locator, access, media, bundle, or re-capture relationship
differs across slices. Capture-level rollups are allowed only when they do not
hide slice-level divergence.

It should own:

- packet manifest;
- obligation-contract version or equivalent rule surface;
- requested decision context and commissioned capture context;
- source locator, source family, source surface, and source actor/audience
  context where knowable;
- capture mode, operator/category, session identity, and visible mode changes;
- decomposed timing: source publication/event timing, source edit/version timing,
  capture timing, re-capture timing if any, and cutoff posture;
- access posture;
- archive/history posture at capture level or per source slice when states
  differ, including not-attempted, failed, fallback, cache, migrated, or
  archive-only states where relevant;
- preserved raw/source-visible files;
- media/modality posture and pointer-only/unavailable/not-attempted states;
- bundle/package structure where the source presents a multi-term offer,
  package, bargain, or proposal;
- re-capture relationship where applicable, including supersedes, supplements,
  conflicts, or mixed relationships;
- hashes;
- warnings and limitations;
- human-readable receipt.

Packet core concern mapping:

| Contract concern | Packet-core treatment |
| --- | --- |
| Ob3 Commissioning Gate | Carry decision/capture context, operator/category, session identity, capture mode, rule surface, and mode-change visibility. |
| Ob4/Ob5 Capture Mode + Mode Change | Carry mode category and visible mode-change events; mode does not decide quality. |
| Ob7 Source Identity And Actor Context | Carry source family/surface and actor/audience context where knowable; mark unavailable or ambiguous actor context visibly. |
| Ob8 Decomposed Timing | Carry timing as separate categories; do not collapse publication/edit/capture/re-capture/cutoff into one timestamp. |
| Ob10 Archive / Historical Posture | Carry archive/history posture for every capture; record per slice/locator when states differ. Archive success is not required, visible posture is. |
| Ob11 Source Visibility And Access Limits | Carry visible access limits, failed attempts, unavailable source parts, pointer-only states, and source-envelope limitations. |
| Ob13 Bundled-Offer Structure Observables | Carry source-visible bundle structure where applicable; mark `not_applicable` when the source is not a bundled-offer surface. |
| Ob15 Re-Capture Semantics | Carry why re-capture happened and whether the new capture supersedes, supplements, conflicts with, or only partially updates prior capture state. |
| Ob16 Categorical Handoff Readiness | Emit a human-readable receipt and visible limitation state sufficient for downstream layers to inspect capture history without recollecting it. |

It must not own ECR fields, Cleaning transforms, Judgment scoring, credibility,
inclusion, exclusion, discounting, Signal Use, Decision Strength, Action
Ceiling, buyer proof, or commercial meaning.

### Retail/PDP Content and Cleaning Contract

Purpose: route agents to the current Retail/PDP capture-retention, Cleaning,
source-binding, residual, and Silver-handoff boundary.

The contract is at
`forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md`.

Implemented capture-side wiring admits either a family content record or a raw
packet. Current content records are validated and adapted under Cleaning; no
separate persisted Retail/PDP Projection sidecar is written. Scratch
qualification may compare disposable DOM/text with the derived content record,
but qualification output is not a lake packet and cannot admit sample mode.
For new Sephora deep-page packets, `sephora_pdp_aggregate` content v3 is the
sole normal route; older sampled-raw/full-derived and Projection-era methods are
legacy-read-only, while explicit raw remains diagnosis/recovery posture.
For retailer pins, sufficiency failures, content ownership, legacy raw
compatibility, and the Silver handoff, use
`forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md`.

It is product contract context only. It is not capture execution, validation,
readiness, implementation authorization, source completeness proof, or buyer
proof.

### Packet Fixture / Retention / Sensitivity Decision

Purpose: define how generated Source Capture Packets move, or do not move,
from scratch output into durable operational context, retained candidate
evidence, fixture-admission recommendation, or separately admitted fixture
status.

The decision is at
`docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`.
It keeps generated packets scratch by default, allows durable closeout artifacts
to cite recorded packet facts without admitting fixtures, and requires visible
retention and sensitivity handling before raw packet directories or packet
contents are retained beyond scratch.

It is not validation, source completeness proof, fixture admission for any
existing packet, legal sufficiency, rights clearance, production storage
authorization, or Judgment evidence.

### Source Capture CLI

Purpose: give operators and later adapters one command path for writing packets.

First useful mode should package already-local files into a packet. That proves
the packet shape before network/source acquisition is introduced.

The packet core and first local-file CLI mode must perform no network access,
browser automation, API calls, archive lookup, media fetch, scraper execution, or
deferred-adapter behavior. Contract tests should guard this boundary.

Illustrative future runner shape:

```powershell
python orca-harness\runners\run_source_capture_packet.py `
  --source-family "<source family>" `
  --source-locator "<source locator or local provenance pointer>" `
  --input-file "<local raw file>" `
  --output "<packet directory>"
```

For local-only packaging, `--source-locator` may be a file path, supplied
provenance pointer, or explicit `unknown_with_reason`; it must not force a live
URL when no live locator is available.

### Agent Runbook

Purpose: make the existing packet writers safe for bounded agent operation.

The agent runbook should tell agents which runner to use for concrete supplied
inputs, when to stop instead of guessing, how to inspect `manifest.json`,
`receipt.md`, and `raw/`, and how to report warnings and limitations without
deciding source meaning.

It should not authorize inference, source discovery, broad crawling, browser
fallback, API use, ECR, Cleaning, Judgment, validation, readiness, buyer proof,
or commercial-readiness claims.

### Mini God-Tier Source Quality Profile

Purpose: give future agents a reusable smallest-complete target for improving
one bounded source unit's source-quality posture after a source locator is
already selected.

The profile defines required criteria, result tokens, a runner ladder,
source-unit queue fields, and a report block for source-quality passes. It does
not admit fixtures, decide rights or retention, discover sources, rank
credibility, score source quality, or authorize ECR, Cleaning, Judgment, APIs,
crawlers, browser fallback, commercial fetch, or production runtime.

### Source-Unit Queue Template

Purpose: give agents a blank planning surface for applying the Mini God-Tier
Source Quality Profile to already-bounded source units without inventing fields
or result vocabulary.

The queue template records source id, bounded context, locator, current state,
target posture, runner choices, cutoff, row status, profile-owned result token,
packet lifecycle, and visible limitations. It must not be used to discover,
select, rank, score, admit, or judge sources.

### Mixed-Source Trial Closeout

Purpose: preserve the first mixed-source trial results for the Mini God-Tier
profile so future helper automation can be scoped from observed packet friction
rather than thread memory.

The closeout is at
`forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md`.
It records the Canoo/Walmart `CW-P4`, `CW-P1`, and `CW-P6` trial outcomes,
including the important distinction between packet-write success and
source-quality result tokens.

It is trial evidence and helper-input context only. It is not fixture admission,
validation, source completeness proof, Judgment scoring, source discovery, or
authorization for new adapters.

### CW-P4 End-To-End Source Quality Pass Closeout

Purpose: preserve the first one-source Mini God-Tier queue-to-report pass after
the report-skeleton helper existed.

The closeout is at
`forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md`.
It records how `CW-P4` moved from queue posture through scratch packet
inspection, skeleton output, operator-finalized report block, and reported row
status.

It is operational source-quality evidence only. It is not fixture admission,
validation, source completeness proof, Judgment scoring, source discovery, or
authorization for new adapters.

### CW-P6 End-To-End Source Quality Pass Closeout

Purpose: preserve the one-source Mini God-Tier queue-to-report pass for a
preserved current official SEC body where visible limitations still travel.

The closeout is at
`forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md`.
It records how `CW-P6` moved from queue posture through scratch Direct HTTP
packet inspection, skeleton output, operator-finalized report block, and
reported row status while retaining `mini_god_tier_with_visible_limitations`.

It is operational source-quality evidence only. It is not fixture admission,
validation, source completeness proof, Judgment scoring, source discovery, or
authorization for new adapters.

### CW-P1 End-To-End Source Quality Pass Closeout

Purpose: preserve the one-source Mini God-Tier queue-to-report pass for an
Archive.org availability metadata packet where no eligible archive body was
selected or preserved.

The closeout is at
`forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md`.
It records how `CW-P1` moved from queue posture through scratch Archive.org
packet inspection, skeleton output, operator-finalized report block, and
reported row status while retaining `archive_body_not_preserved`.

It is operational source-quality evidence only. It is not fixture admission,
validation, source completeness proof, Judgment scoring, source discovery, or
authorization for new adapters.

### Slot 3 Post-Recapture Source Quality Closeout

Purpose: preserve the post-recapture Slot 3 Mini God-Tier source-quality pass
across Reddit batch 1, Reddit batch 2, and WSO after the state assembler and
report-skeleton helper were available.

The closeout is at
`forseti/product/spines/capture/core/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`.
It records how all three already-bounded source units reached `reported` row
status with `mini_god_tier_with_visible_limitations`, while retaining scratch
lifecycle, local cutoff, WSO hidden/full-comment, archive-body, and
source-completeness non-claims.

It is operational source-quality evidence only. It is not fixture admission,
validation, source completeness proof, Judgment scoring, source discovery, or
authorization for new adapters.

### Reddit Capture Operator Playbook

Purpose: give operators and agents a single current-procedure route for bounded
Reddit exact-thread capture using implemented Source Capture Armory tools.

The playbook is at
`forseti/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`.
It covers required inputs, URL-list shape, old Reddit Direct HTTP batch capture,
budget-window cadence, Reddit consolidation, quality summary interpretation,
exact-URL archive fallback, CloakBrowser/proxy boundaries, warm same-context
`.json` as a future/specialized enrichment path, and stop lines.

It is operational guidance only. It is not validation, readiness, source
completeness proof, source discovery authorization, broad crawling,
monitoring, commercial Reddit authority, ECR, Cleaning, Judgment, or buyer
proof.

### Reddit Pre-Commercial Capture Consolidation Planning Thread

Purpose: preserve the durable planning thread for bounded Reddit
pre-commercial capture and consolidation before Reddit-specific parser,
consolidation, monitoring, or storage implementation.

The planning artifact is at
`forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md`.
It frames the Reddit-specific work as an architectural planning pass: exact old
Reddit Direct HTTP as the current exact-thread operator default when current old
Reddit HTML is the capture target; CloakBrowser as the anti-blocking/browser-
visible route when Direct HTTP is unsuitable or blocked; Source Capture Packet
preservation before BeautifulSoup-style parsing; provenance-first
consolidation; archive fallback; and warm same-context `.json` as a bounded
enrichment path only after the exact old Reddit HTML thread has loaded
successfully in the same browser context.
It also keeps explicit stop lines for Reddit parser/consolidation
implementation, runtime, broad crawling, storage, production monitoring, and
commercial use.

The success-signal routing object is at
`forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md`.
It is advisory context for the planning-thread hardening patch and should be
read when checking why Reddit units must be classified as
`decision_frame_bound` or `candidate_or_scouting`, why success tiers do not
promote silently, and why candidate/scouting units currently have no compliant
Data Capture handoff destination without a separate Candidate Signal Intake /
Corpus Intake contract.

It is planning context only. It is not validation, readiness, live Reddit
capture authorization, CloakBrowser installation proof, parser correctness
proof, storage authorization, production-runtime authorization, ECR, Cleaning,
Judgment, or commercial Reddit authority.

### IG Creator Roster And Frontier Ledger Spec

Purpose: preserve the proposed current-main ledger contract for beauty IG
creator roster entries, public display-name observations, lifecycle events, and
frontier discovery provenance before any implementation prompt or capture
runner is scoped.

The spec is at
`forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md`.
It ports only the old roster-ledger branch's still-useful
ledger/privacy/frontier semantics and aligns roster sizing to current main:
`250 -> 500 -> 1,000`, with the 1,000-creator serious-v0 planning target and
10/30/60 A/B/C allocation.

It is proposed docs-only context. It is not adoption, validation, readiness,
capture authorization, outreach authorization, a crawler, a scheduler/runtime
spec, an ontology amendment, or a public person-level product surface.

### Creator Public-Handle Linkage Ledger Spec

Purpose: define the dedicated Tier-2-B public-handle-to-public-handle linkage shape for creator accounts across Instagram, TikTok, and YouTube before any SQLite/runtime promotion.

The spec is at
`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md`; the current populated product ledger seed is at `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json`. The local validator is `orca-harness/capture_spine/creator_public_handle_linkage/` with synthetic/adversarial tests under `orca-harness/tests/unit/test_creator_public_handle_linkage.py`.

It is static ledger/validator work only. It is not live capture, contact/outreach authorization, non-public-handle joining, real-world identity proof, SQLite adoption, or a public person-level product surface.

### Creator Profile Current View Spec

Purpose: define the dashboard-ready one-stop creator profile view that joins
identity, aggregate influence rollups, and ideal-audience enrichment without
putting mutable metrics or audience fields into the identity linkage ledger.

The spec is at
`forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md`.
It treats average views and engagement rate as metric rollups keyed to the
creator/account spine; individual reels/videos stay in metric observations.
SQLite or another storage engine can physicalize the sibling tables later, after
source-backed row tests.

It is a product/view contract only. It is not a data-lake job, SQLite adoption,
dashboard implementation, live capture authorization, metric-score validation,
or public person-level product surface.

### Source-Quality Example Ladder

Purpose: give future agents a compact retrieval pattern for reading packet
success separately from source-quality status.

| Example | Packet/body posture | Source-quality result | Lesson |
| --- | --- | --- | --- |
| `CW-P4` | Archive.org snapshot body preserved. | `mini_god_tier_met` | A cutoff-compatible archive body can satisfy the clean preserved-body path, while still carrying scratch lifecycle and archive-completeness non-claims. |
| `CW-P6` | Current official SEC Archives body preserved by Direct HTTP. | `mini_god_tier_with_visible_limitations` | A real preserved body can still carry limitations when archive/history, media, and source-envelope posture are incomplete. |
| `CW-P1` | Archive availability metadata exists, but no eligible archive body was selected or preserved. | `archive_body_not_preserved` | Packet or metadata success must not be upgraded into source-body possession. |
| `Slot 3 post-recapture` | Local Reddit JSON and WSO visible-envelope HTML/text/screenshot bodies or body-equivalents preserved in scratch packets. | `mini_god_tier_with_visible_limitations` | Multi-venue recapture can improve body/body-equivalent posture while local cutoff, archive-body, WSO hidden/full-comment, and scratch-lifecycle limits still travel forward. |

Use the ladder as an operating example only. It is not source-quality scoring,
fixture admission, validation, source selection, Judgment evidence, or a
substitute for inspecting the controlling closeout artifacts.

### Source Quality Report-Skeleton Helper

Purpose: turn one existing Source Capture Packet manifest into a Mini God-Tier
report skeleton so agents do not manually rebuild body-posture, provenance,
lifecycle, and conservative result-token guidance from scratch.

The helper is implemented in
`orca-harness/runners/run_source_quality_report_skeleton.py` and reads packet
manifest plus packet-side metadata only. It does not fetch sources, parse raw
source bodies for meaning, infer source-language anchors, score source quality,
admit fixtures, or finalize `mini_god_tier_met`.

### Source Quality State Assembler

Purpose: assemble already-bounded source-unit rows, existing packet paths,
report-skeleton state, lifecycle state, and visible limitations into an
inspectable state census.

The architecture boundary is at
`forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md`.
The helper is implemented in
`orca-harness/runners/run_source_quality_state_assembler.py`.
The name is intentional: this is not a conductor, gate sequencer, scorer,
source selector, runner dispatcher, or fixture-admission surface. Output must
preserve helper suggestions as suggestions, keep operator finalization for
quality-bearing claims, and distinguish state census from verdict.

### Direct HTTP Fetch Adapter

Purpose: retrieve public or discoverable pages where ordinary HTTP access works,
then write the response into the Source Capture Packet shape.

It should preserve response body, final URL, status, useful provenance headers,
hashes, and access failures.

It should ignore ambient proxy configuration so direct HTTP provenance remains
true. If a run uses a proxy, that must happen through an explicit proxy-capable
runner with method provenance, not through shell or process environment drift.

It should not use API registration, browser automation, anti-detect behavior,
proxies, credential bypass, or production crawling.

### Media / Asset Preservation Adapter

Purpose: preserve source-linked images, galleries, screenshots, or other
source-meaningful media when they are inside the source-access boundary.

It should record pointer-only, unavailable, failed, or not-attempted media
states visibly instead of silently dropping them.

### Archive.org Adapter

Purpose: distinguish archive availability from archive-body retrieval.

It may query availability/CDX metadata and retrieve accessible snapshot body
content through ordinary HTTP routes. Browser fallback belongs to the Honest
Browser Snapshot adapter, not this adapter.

It should record when only archive metadata is available and when archive body
retrieval fails or is not attempted.

For a bounded URL whose live/current capture visibly fails with an access block
or non-content interstitial, Archive.org is the preferred first fallback when
the operator requested fallback handling. The fallback remains bound to the same
source unit: first try the exact supplied URL, then a same-thread canonical URL
variant when the source family has an obvious canonical equivalent, and record
`snapshot_count=0` or `archive_body_not_preserved` loudly when no snapshot body
exists. Do not treat archive fallback as permission to crawl the site, discover
related URLs, follow comments/users/recommendations, or infer source content
from archive absence.

### Honest Browser Snapshot Adapter

Purpose: preserve visible HTML/text/screenshot artifacts for pages requiring
JavaScript rendering or browser-visible inspection.

The implemented v0 is anonymous/headless browser capture for one explicitly
supplied URL. It preserves rendered DOM, visible text, a viewport screenshot,
and receipt metadata. The authenticated v0 extension uses Playwright
manual-login storage-state for one explicitly supplied URL, with a fixed
session-mode vocabulary and local ignored `_auth_state/` storage. Bootstrap
writes a local ignored sidecar that binds the saved state file to the declared
session mode, and capture refuses mismatched mode declarations. Packets record
session mode and state label but do not copy, hash, print, or preserve
storage-state JSON, sidecar metadata, cookies, tokens, or credentials.

It is first-tranche only as an honest browser/headless-browser path. Anti-detect,
proxy rotation, CAPTCHA solving, password-driven login automation, direct
profile/cookie import, and no-entitlement bypass remain separately gated.

### CloakBrowser Anti-Blocking Browser Adapter

Purpose: preserve browser-visible source artifacts from public or discoverable
sources that are expected to block ordinary browser/headless capture.

The owner selected CloakBrowser as the primary third-tranche anti-blocking
backend. Anonymous CloakBrowser Snapshot v0 is implemented in
`orca-harness/source_capture/adapters/cloakbrowser_snapshot.py` with runner
`orca-harness/runners/run_source_capture_cloakbrowser_packet.py`. Patchright
remains an optional compatibility fallback if CloakBrowser creates a concrete
operational blocker; it is not the default first probe.

Implemented v0 scope:

- one explicitly supplied ordinary URL;
- anonymous non-persistent CloakBrowser launch;
- rendered DOM, visible text, viewport screenshot, and method-provenance
  metadata preserved into a Source Capture Packet;
- Retail/PDP content extraction after retailer pin, access, and sufficiency
  checks; current content flows directly into Cleaning, while extraction
  failure preserves supplied raw inputs through the typed failure path;
- no stored session, browser profile, raw cookies, storage-state file, proxy,
  credential injection, CAPTCHA service, crawler, target discovery, parser,
  consolidation, storage, dashboard, scheduler, deployment, production runtime,
  ECR, Cleaning, Judgment, buyer proof, or commercial-readiness logic.

For Reddit in the current pre-commercial / personal-project phase, the operating
order is:

1. exact old Reddit Direct HTTP first for supplied thread URLs when current old
   Reddit HTML is the capture target and the bounded batch runner accepts the
   URL;
2. CloakBrowser anti-blocking browser capture for one supplied URL when Direct
   HTTP is unsuitable, blocked, or browser-visible anti-blocking capture is
   explicitly needed;
3. low-volume bounded capture over source sets that are subreddit-bounded,
   thematic, query-based, thread-family scoped, or small monitored thread sets;
4. archive capture for historical thread posture or when live capture is not
   necessary or fails visibly, bounded to the same supplied thread URL and
   same-thread canonical variants.

The Reddit bound is not URL-only. Operators must name the subreddit, theme,
query, thread family, or monitored-thread set and record the method provenance
plainly. This does not authorize broad crawling, site-wide walking, generic
subreddit harvesting, production monitoring, storage, dashboards, schedulers,
deployment, or commercial-scale use.

When Orca goes commercial / enterprise on Reddit, move to the sanctioned
commercial / enterprise API or data-licensing path and stop relying on
anti-blocking as the primary method.

Do not treat cold anonymous Reddit `.json` endpoint access as the primary
capture spine. Current official guidance and developer reports indicate
OAuth/login credentials are expected for Data API traffic, and Orca's bounded
2026-06-08 probes saw direct cold `.json`, browser cold `.json`, and
CloakBrowser+proxy cold `.json` return 403/network-security blocks.

However, Orca also observed a useful bounded exception on 2026-06-08: after the
exact old Reddit HTML thread loaded successfully in a no-proxy CloakBrowser
context, fetching that same thread's `.json` URL inside the same browser context
with browser credentials returned HTTP 200 JSON. Treat this as a future
`old_reddit_html_warmup_then_same_context_json` method shape: HTML remains the
visible access/provenance warm-up, and same-context JSON may become the cleaner
structured extraction body. It remains one supplied thread only unless a
separate bounded batch runner is implemented; it does not authorize cold JSON
probing, link following, subreddit crawling, user/profile capture, storage,
monitoring, or commercial use.

Bounded old Reddit batch capture should use a hard ceiling plus an inspectable
cadence budget when more than a tiny smoke list is run: maximum thread count,
time window, min/max gaps, recorded random seed, planned waits, planned offsets,
actual timestamps, and visible stop reason. This cadence is for low-load
bounded operation and provenance, not a claim to mimic a human or bypass access
controls. The batch runner must stop visibly on blocks; it must not add hidden
retries, proxy escalation, source discovery, monitoring, or browser fallback
inside the Direct HTTP batch lane.

BeautifulSoup-style parsing is appropriate after old Reddit HTML or archived
HTML has been retrieved and preserved. It helps extract posts, comment text,
links, timestamps, nesting cues, and visible metadata from HTML; it does not
fetch the source, bypass blocking, solve JavaScript rendering, or replace packet
provenance.

Observed Reddit block pages such as HTTP `403 Blocked` with a visible
"network security" message are source-access outcomes, not parser failures. The
packet should preserve the block body and the consolidation or quality layer
should mark the row unusable for downstream content extraction unless a bounded
fallback packet preserves a usable source body. Archive absence is also an
outcome: `snapshot_count=0` is not source completeness proof and must not be
upgraded into evidence about the thread content.

### Source Observability Helper

Purpose: inspect operator-authored posture records and emit visible limitation
reports.

This helper already exists under `orca-harness/source_observability/`.

It is not a source capture tool. It does not fetch sources, retrieve archives,
preserve media, automate browsers, call APIs, or validate capture. It can later
consume Source Capture Packet metadata or operator records to help keep
limitations visible.

## Current Build Order

1. Design and document this armory entrypoint. **Done.**
2. Build Source Capture Packet core and CLI with local-file packaging only. **Done.**
3. Dry-run the packet CLI against an already-local source artifact. **Done.**
4. Add Direct HTTP fetch adapter. **Done.**
5. Add Media / Asset Preservation adapter. **Done.**
6. Add Archive.org availability/body adapter. **Done.**
7. Add agent-facing runbook for bounded runner use. **Done.**
8. Add Honest Browser Snapshot adapter. **Done for anonymous/headless v0 and
   manual-login storage-state authenticated v0.**
9. Add Reddit API adapter and credential support. **Authorized by second tranche;
   implementation status should be checked in `orca-harness/source_capture/`
   before use.**
10. Add CloakBrowser anti-blocking browser adapter. **Done for anonymous
    non-persistent v0 over one explicitly supplied URL; not Reddit
    discovery/consolidation, proxy/session behavior, storage, production
    runtime, or commercial use.**
11. Decide separately whether password-driven login automation, direct
    profile/cookie import, commercial fetch services, SERP APIs, broad
    crawler/spider frameworks, storage, dashboards, schedulers, deployment, or
    production runtime should receive their own owner authorization.

## Folder Convention

Use this folder for product-facing Source Capture Armory docs:

```text
forseti/product/spines/capture/core/source_capture_toolbox/
  README.md
  <scoped specs, recon closeouts, and gap notes>
```

Use the harness for implementation:

```text
forseti-harness/source_capture/
forseti-harness/runners/run_source_capture_packet.py
forseti-harness/docs/<implementation usage docs>
forseti-harness/tests/<unit and contract tests>
```

Do not move existing controlling product or decision artifacts into this folder
without a separate reference-migration pass.

## Overall Gaps

Implemented first-tranche pieces:

- Source Capture Packet schema/model;
- implementation-facing packet-core docs derived from the obligation mapping
  above;
- packet writer;
- hashing helper for packet artifacts;
- human-readable receipt writer;
- local-file packet CLI runner;
- local-file packaging mode;
- output lifecycle guidance for packet directories;
- unit and contract tests for packet core;
- no-network/no-deferred-adapter guard tests for packet core;
- Direct HTTP adapter;
- Media / Asset Preservation adapter;
- Archive.org availability/body adapter;
- Honest Browser Snapshot adapter, anonymous/headless v0;
- Authenticated Browser Snapshot adapter, manual-login storage-state v0;
- CloakBrowser Snapshot adapter, anonymous non-persistent v0;
- Source Quality report-skeleton helper for existing Source Capture Packets;
- Source Quality State Assembler for read-only state census over existing
  source-quality rows and packets;
- Source Capture Packet fixture / retention / sensitivity decision;
- agent-facing runbook for bounded runner selection, stops, inspection, and
  reporting.

Remaining current gaps:

- no Source Observability integration point;
- no named packet has been separately admitted as a fixture.

Deferred gaps that are intentionally outside the first tranche:

- password-driven login automation;
- direct browser profile or raw cookie import;
- commercial scraping or fetch-service integration;
- broad crawler/spider frameworks;
- standalone CAPTCHA-solving service integration;
- SERP/discovery API integration;
- persistent storage, database, dashboard, queue, scheduler, deployment,
  production crawler, or broad source-system runtime.

## Non-Claims

This README is not validation, readiness, source-of-truth promotion, legal
sufficiency, source-access boundary amendment, contract hardening,
implementation execution, commercial-scraper authorization, standalone
CAPTCHA-service authorization, production-runtime authorization, final packet
schema, ECR design, Cleaning implementation, Judgment design, buyer proof,
rights-to-process sufficiency, retention policy, or commercial-readiness
evidence. Reddit API and anti-blocking/CloakBrowser build authority comes from
`docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`,
not from this README.

## Direction Change Propagation - Source-Family Lane Catalog

```yaml
direction_change_propagation:
  doctrine_changed: >
    Owner-ratified option 1 for capture playbook/lake synchronization: the
    Source Capture Playbook / Armory owns source-access method and shared
    capture tooling; Capture source-family lane indexes own known-family
    routing homes tying access routes to runners, projection, Data Lake, ECR,
    and Cleaning pointers; Data Lake authority docs remain the sole owner of
    raw admission, storage, derived layout, write boundary, Silver, and
    medallion semantics.
  trigger: workflow_authority
  related_triggers:
    - architecture_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md
    - forseti/product/spines/capture/core/source_capture_toolbox/README.md
    - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - forseti/product/spines/capture/core/source_families/README.md
    - forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md
    - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
    - forseti/product/spines/capture/core/source_families/social_media/instagram/README.md
    - forseti/product/spines/capture/core/source_families/social_media/tiktok/README.md
    - forseti/product/spines/capture/core/source_families/social_media/youtube/README.md
    - forseti/product/spines/capture/core/source_families/social_media/reddit/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/repo_map_recent_changes/capture_source_family_lane_catalog_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/workflows/artifact_retrievability_guide.md
    - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/data_lake/authority/
    - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    - orca-harness/source_capture/
    - orca-harness/runners/
    - orca-harness/cleaning/
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/
      reason: >
        This patch changes retrieval routing only. Data Lake raw admission,
        storage, derived layout, write boundary, Silver, and medallion rules
        remain unchanged and are pointed to from the catalog rather than copied.
    - path: forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
      reason: >
        Recon verdicts and evidence did not change; the catalog routes to
        existing family evidence without changing the evidence base.
    - path: orca-harness/
      reason: >
        Runtime behavior, packet writers, projection helpers, cleaning writers,
        and tests were inventory sources only; this lane was documentation/index
        work under the Drift Guard.
  stale_language_search: >
    rg -n "not yet owner-ratified|ratify BEFORE|Open Decision / Fork|Proposes a three-way authority model|proposed access/routing/lake authority split before ratifying|proposed authority model is ratified" docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md forseti/product/spines/capture/core/source_capture_toolbox/README.md forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md forseti/product/spines/capture/core/source_families docs/workflows/data_capture_spine_consolidation_map_v0.md docs/workflows/forseti_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-05 before receipt insertion: `rg` exited 1 with no matches.
    Re-run after receipt insertion: the only hit is this receipt's own
    `stale_language_search` literal; no active routing surface checked still
    carries the stale unratified-option wording.
  non_claims:
    - not validation
    - not readiness
    - not source-access permission
    - not live capture authorization
    - not lake-write authorization
    - not Data Lake authority change
    - not ECR, Cleaning, Judgment, or buyer proof
    - not runtime implementation
```


## Direction Change Propagation - CloakBrowser Anonymous Snapshot v0

```yaml
direction_change_propagation:
  doctrine_changed: "CloakBrowser is no longer only a selected third-tranche backend: Orca now has an anonymous non-persistent CloakBrowser Snapshot v0 adapter and packet runner for one explicitly supplied URL, while Reddit discovery/consolidation, proxy/session behavior, commercial fetch, storage, dashboards, deployment, and production runtime remain separately gated."
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
    - workflow_authority
  controlling_sources_updated:
    - "orca-harness/source_capture/adapters/cloakbrowser_snapshot.py"
    - "orca-harness/runners/run_source_capture_cloakbrowser_packet.py"
    - "orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py"
    - "orca-harness/tests/contract/test_source_capture_cloakbrowser_snapshot_contract.py"
    - "orca-harness/tests/contract/test_source_capture_browser_snapshot_contract.py"
    - "orca-harness/pyproject.toml"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/README.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
  intentionally_not_updated:
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "The bounded third-tranche CloakBrowser build was already authorized; this patch implements the anonymous v0 runner without changing the authorization boundary."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access hard stops and disclosability requirements did not change."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Method sequencing did not change; the selected CloakBrowser route moved from planned to anonymous v0 implementation."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden downstream outputs did not change."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
      reason: "The Reddit planning thread still owns parser/consolidation/monitoring/storage decisions; this patch implements only the generic one-URL CloakBrowser packet runner."
  stale_language_search: "rg -n \"CloakBrowser.*not implemented|not implemented.*CloakBrowser|future primary backend|STEP-01 adapter contract|once implemented|not an implemented runner|live CloakBrowser engine, packet runner\" forseti/product/spines/capture/core/source_capture_toolbox/README.md orca-harness/docs/source_capture_agent_runbook.md orca-harness/README.md docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md orca-harness/source_capture orca-harness/runners orca-harness/tests"
  stale_language_search_result: "Executed 2026-06-06 after this patch; the only hit is this receipt's own stale_language_search line."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not Reddit source discovery"
    - "not Reddit parser or consolidation implementation"
    - "not proxy, stored session, profile, cookie, credential, or CAPTCHA-service behavior"
    - "not commercial fetch, broad crawling, storage, dashboard, deployment, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory now has a product-facing entrypoint and folder convention: future armory product docs should live under docs/product/source_capture_toolbox while existing controlling authority files remain at their historical paths and are indexed here."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/README.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - "orca-harness/README.md"
    - "orca-harness/docs/source_observability_scalability_note.md"
  intentionally_not_updated:
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access boundary permission and hard stops did not change."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and forbidden outputs did not change."
    - path: "orca-harness/README.md"
      reason: "Harness implementation has not yet added source_capture code; the harness README should change with implementation, not with this product-facing design index."
    - path: "orca-harness/docs/source_observability_scalability_note.md"
      reason: "Source Observability remains a separate helper; this README references it without changing its boundary."
  stale_language_search: "rg -n \"Source Capture Armory|source_capture_toolbox|Source Capture Packet|source_capture\" .agents/workflow-overlay/artifact-folders.md forseti/product/README.md forseti/product/spines/capture/core/source_capture_toolbox/README.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/data_capture_source_access_method_plan_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Source Capture Armory Display Name

```yaml
direction_change_propagation:
  doctrine_changed: "The product-facing display name is now Source Capture Armory; the historical docs/product/source_capture_toolbox path remains stable until a separate migration decision."
  trigger: product_doctrine
  related_triggers:
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/README.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - ".agents/workflow-overlay/source-loading.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/docs/source_capture_packet.md"
    - "orca-harness/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - "CLAUDE.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_state_assembler_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_capture_toolbox_agent_usability_dry_run_closeout_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md"
  intentionally_not_updated:
    - path: "docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md"
      reason: "Judgment toolkit planning is a separate Judgment-lane concept, not the Source Capture Armory display-name surface."
    - path: "docs/review-outputs/**"
      reason: "Review outputs are historical/advisory snapshots and should not be rewritten for display-name harmonization."
    - path: "docs/prompts/**"
      reason: "Prompt and precompact artifacts are historical routing context unless a future prompt-specific pass is authorized; the new CA handoff is the current continuation prompt."
    - path: "docs/_inbox/**"
      reason: "Inbox/raw capture material is non-authoritative scratch or provenance material."
  stale_language_search: "rg -n \"Source Capture Toolbox|SOURCE_CAPTURE_TOOLBOX|source-capture toolbox|current toolbox|toolbox gap|toolbox usability|full toolkit\" .agents/workflow-overlay/artifact-folders.md .agents/workflow-overlay/source-loading.md .agents/workflow-overlay/safety-rules.md forseti/product/README.md docs/product/source_capture_toolbox docs/workflows/orca_repo_map_v0.md docs/product/data_capture_source_access_method_plan_v0.md docs/product/data_capture_source_access_boundary_decision_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md orca-harness/docs/source_capture_agent_runbook.md orca-harness/docs/source_capture_packet.md orca-harness/README.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not path migration"
    - "not source-access boundary amendment"
    - "not new implementation authorization"
    - "not Reddit API, commercial fetch, anti-detect, proxy, storage, dashboard, deployment, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Packet Core Contract Mapping Patch

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Packet core is now explicitly contract-derived: the README maps packet concerns to Data Capture obligations, requires slice-level state where rollups would hide divergence, and states the first local-file CLI mode is no-network."
  trigger: architecture_doctrine
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/artifact-folders.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "The obligation contract remains the authority; this patch maps the armory packet to it without changing Capture obligations."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Authorized first-tranche build surface did not change."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Candidate source-access methods, hard stops, and sequencing did not change."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access boundary permission and hard stops did not change."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading route already points to the armory README; no new read-pack entry is required."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the armory README as the product-facing entrypoint."
  stale_language_search: "rg -n \"packet is the spine|acquisition timestamp and cutoff posture|--source-url|no-network.*implied\" forseti/product/spines/capture/core/source_capture_toolbox/README.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not final packet schema"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Authenticated Browser Snapshot v0

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Armory now treats manual-login Playwright storage-state authenticated browser capture as an implemented first-tranche Browser Snapshot extension, with local ignored session-mode sidecar binding, while password automation, direct profile/cookie import, anti-detect, proxy behavior, CAPTCHA solving, and no-entitlement bypass remain deferred or forbidden."
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
    - "orca-harness/docs/source_capture_packet.md"
    - "orca-harness/README.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/safety-rules.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "The source-access boundary already permits free/account-created, paid, client-provided, and consenting-coworker access when disclosable and hard stops are avoided; this patch implements a bounded tool path without changing permission doctrine."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Method sequencing and hard stops did not change; authenticated v0 stays inside the already authorized first-tranche Source Capture Armory implementation lane."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "The existing tooling authorization controls the bounded first-tranche build surface; no new API, commercial fetch, anti-detect, proxy, production runtime, ECR, Cleaning, or Judgment authority is introduced."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and handoff states did not change; packets remain visible limitation carriers only."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes agents to this armory README for current component status and gaps; it does not encode per-adapter build status."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes this armory README as the component/gap entrypoint; no stale logged-in/session-state status was found there."
  stale_language_search: "rg -n \"logged-in/entitled browser session reuse remains|no logged-in/entitled browser session|session/profile/cookie/storage-state reuse|Login-visible or entitled browser session content \\| none yet|not login/session capture\" forseti/product/spines/capture/core/source_capture_toolbox/README.md orca-harness/docs/source_capture_agent_runbook.md orca-harness/docs/source_capture_packet.md orca-harness/README.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not password automation authorization"
    - "not direct profile or raw cookie import authorization"
    - "not anti-detect, proxy, CAPTCHA, API, commercial fetch, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Blocked URL Archive Fallback

```yaml
direction_change_propagation:
  doctrine_changed: "Source Capture Armory runner guidance now treats visible HTTP block/interstitial packets as source-access outcomes and routes operator-requested archive fallback through exact URL plus same-thread canonical variants only, with snapshot absence recorded loudly."
  trigger: product_doctrine
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  intentionally_not_updated:
    - path: "docs/workflows/data_capture_spine_consolidation_map_v0.md"
      reason: "The consolidation map already routes Armory and Reddit source-access questions to this README, the Reddit planning thread, and the runbook; no new source family or entrypoint was added."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes source-access tooling questions to the Armory README and runbook; no new read-pack or source hierarchy path is needed."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and posture vocabulary did not change; this patch applies existing archive/access visibility rules to blocked URL fallback."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access permission and hard stops did not change; the fallback remains bounded to the same source unit and does not authorize crawling or bypass."
  stale_language_search: "rg -n \"archive fallback|same-thread canonical|snapshot_count=0|network security|ambient proxy|Do not chain runners|archive_body_not_preserved\" forseti/product/spines/capture/core/source_capture_toolbox/README.md orca-harness/docs/source_capture_agent_runbook.md forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md .agents/workflow-overlay/source-loading.md"
  stale_language_search_result: "Executed 2026-06-08 after this patch. Hits are intended owner-surface language in the Armory README, Reddit planning thread, and runbook, plus pre-existing archive_body_not_preserved examples. The consolidation map remains pointer-only."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not new source discovery authority"
    - "not broad crawling"
    - "not proxy, anti-detect, CAPTCHA, API, commercial fetch, storage, dashboard, deployment, or production-runtime authorization"
    - "not ECR, Cleaning, Judgment, buyer proof, or source completeness proof"
```

## Direction Change Propagation - Warm Reddit JSON

```yaml
direction_change_propagation:
  doctrine_changed: "Reddit `.json` posture now distinguishes blocked cold JSON requests from the observed warm same-context JSON enrichment path: load exact old Reddit HTML first, then fetch that same thread's `.json` in the same browser context while preserving both bodies and provenance."
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
    - output_authority
  controlling_sources_updated:
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "orca-harness/docs/source_capture_agent_runbook.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
  intentionally_not_updated:
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations did not change; this patch changes Reddit method ordering and preservation posture."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access permission boundaries and hard stops did not change."
    - path: "orca-harness/runners"
      reason: "This is a docs-method update only; a warm same-context JSON runner remains a separately scoped implementation step."
  stale_language_search: "rg -n \"anonymous `.json`|cold `.json`|warm same-context|same-context JSON|json_fallback|Reddit `.json` is not the spine\" forseti/product/spines/capture/core/source_capture_toolbox/README.md forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_planning_thread_v0.md docs/product/data_capture_source_access_method_plan_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md orca-harness/docs/source_capture_agent_runbook.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not live Reddit capture authorization"
    - "not source discovery, crawling, monitoring, storage, or commercial Reddit authorization"
    - "not ECR, Cleaning, Judgment, buyer proof, or source completeness proof"
```
