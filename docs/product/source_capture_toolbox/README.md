# Source Capture Toolbox

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Product-facing index and design guide for the bounded Source Capture Toolbox.
use_when:
  - Scoping, implementing, reviewing, or extending first-tranche Data Capture source-access tooling.
  - Checking what each Source Capture Toolbox component does.
  - Distinguishing source capture tooling from Source Observability, ECR, Cleaning, Judgment, or deferred source-access adapters.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
  - docs/product/data_capture_source_access_method_plan_v0.md
  - docs/product/data_capture_source_access_boundary_decision_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - The source-access tooling build authorization is amended or superseded.
  - The source-access boundary decision materially changes hard stops or disclosability requirements.
  - The Data Capture obligation contract materially changes capture obligations.
  - A first-tranche implementation decision changes the packet shape, adapter set, or output lifecycle.
```

## Status

Status: `SOURCE_CAPTURE_TOOLBOX_README_V0`.

This folder is the product-facing home for Source Capture Toolbox design notes,
implementation-facing docs, gap registers, and future scoped specs.

Existing controlling artifacts are not moved into this folder. They remain in
their original product/decision locations because those paths are already cited
by source-loading, reviews, decisions, and propagation receipts. This README
indexes them so future toolbox work has one entrypoint without breaking
historical references.

## Why This Toolbox Exists

The Data Capture pressure tests showed repeated source-observability pressure:
source language, source structure, media, archive body state, access posture,
cutoff posture, and acquisition receipts need to stay inspectable.

If each fetcher, archive helper, browser snapshot, or media preserver writes its
own output shape, downstream work inherits adapter-specific mess. The toolbox
exists to make every capture path emit the same kind of Source Capture Packet
before more adapters are added.

The packet is the shared capture container. The Data Capture obligation contract
remains the spine-level authority. Adapters are replaceable ways to fill the
packet without redefining Capture obligations.

## Controlling Sources

| Source | What It Controls |
| --- | --- |
| `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` | Whether first-tranche source-access tooling builds are authorized and which adapters remain separately gated. |
| `docs/product/data_capture_source_access_method_plan_v0.md` | Candidate methods, sequence discipline, source-family method notes, and risk posture. |
| `docs/product/data_capture_source_access_boundary_decision_v0.md` | Source-access boundary, entitlement/disclosability standard, and hard stops. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Capture obligations, forbidden Capture outputs, and handoff discipline. |
| `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md` | Why pressure-test findings support moving from all-tools-deferred to bounded first-tranche tooling. |
| `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | Reusable operating profile for the smallest complete source-quality target per bounded source unit; not fixture admission, validation, source discovery, or Judgment authority. |
| `docs/product/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md` | Blank queue template for planning mini god-tier source-quality passes over already-bounded source units; not source selection, source discovery, or fixture admission. |
| `docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md` | First mixed-source Mini God-Tier trial closeout; helper-input context only, not fixture admission, validation, or Judgment authority. |
| `docs/product/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md` | One-source CW-P4 Mini God-Tier end-to-end pass evidence; read as operational closeout context only, not fixture admission, validation, or doctrine authority. |
| `docs/product/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md` | One-source CW-P6 Mini God-Tier limitation-path pass evidence; read as operational closeout context only, not fixture admission, validation, or doctrine authority. |
| `docs/product/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md` | One-source CW-P1 Mini God-Tier metadata-only negative-path pass evidence; read as operational closeout context only, not fixture admission, validation, or doctrine authority. |
| `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` | Architecture boundary for a read-only Source Quality State Assembler over already-bounded rows and existing packets; state census only, not source discovery, runner dispatch, scoring, fixture admission, or Judgment authority. |

## Toolbox Components

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
`docs/product/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md`.
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
`docs/product/source_capture_toolbox/source_quality_cw_p4_end_to_end_pass_closeout_v0.md`.
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
`docs/product/source_capture_toolbox/source_quality_cw_p6_end_to_end_pass_closeout_v0.md`.
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
`docs/product/source_capture_toolbox/source_quality_cw_p1_end_to_end_pass_closeout_v0.md`.
It records how `CW-P1` moved from queue posture through scratch Archive.org
packet inspection, skeleton output, operator-finalized report block, and
reported row status while retaining `archive_body_not_preserved`.

It is operational source-quality evidence only. It is not fixture admission,
validation, source completeness proof, Judgment scoring, source discovery, or
authorization for new adapters.

### Source-Quality Example Ladder

Purpose: give future agents a compact retrieval pattern for reading packet
success separately from source-quality status.

| Example | Packet/body posture | Source-quality result | Lesson |
| --- | --- | --- | --- |
| `CW-P4` | Archive.org snapshot body preserved. | `mini_god_tier_met` | A cutoff-compatible archive body can satisfy the clean preserved-body path, while still carrying scratch lifecycle and archive-completeness non-claims. |
| `CW-P6` | Current official SEC Archives body preserved by Direct HTTP. | `mini_god_tier_with_visible_limitations` | A real preserved body can still carry limitations when archive/history, media, and source-envelope posture are incomplete. |
| `CW-P1` | Archive availability metadata exists, but no eligible archive body was selected or preserved. | `archive_body_not_preserved` | Packet or metadata success must not be upgraded into source-body possession. |

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
`docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md`.
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

### Source Observability Helper

Purpose: inspect operator-authored posture records and emit visible limitation
reports.

This helper already exists under `orca-harness/source_observability/`.

It is not a source capture tool. It does not fetch sources, retrieve archives,
preserve media, automate browsers, call APIs, or validate capture. It can later
consume Source Capture Packet metadata or operator records to help keep
limitations visible.

## Current Build Order

1. Design and document this toolbox entrypoint. **Done.**
2. Build Source Capture Packet core and CLI with local-file packaging only. **Done.**
3. Dry-run the packet CLI against an already-local source artifact. **Done.**
4. Add Direct HTTP fetch adapter. **Done.**
5. Add Media / Asset Preservation adapter. **Done.**
6. Add Archive.org availability/body adapter. **Done.**
7. Add agent-facing runbook for bounded runner use. **Done.**
8. Add Honest Browser Snapshot adapter. **Done for anonymous/headless v0 and
   manual-login storage-state authenticated v0.**
9. Decide separately whether password-driven login automation, direct
   profile/cookie import, Reddit API, commercial fetch services, anti-detect,
   proxies, SERP APIs, storage, dashboards, schedulers, deployment, or production
   runtime should receive their own owner authorization.

## Folder Convention

Use this folder for product-facing Source Capture Toolbox docs:

```text
docs/product/source_capture_toolbox/
  README.md
  <future scoped specs and gap notes>
```

Use the harness for implementation:

```text
orca-harness/source_capture/
orca-harness/runners/run_source_capture_packet.py
orca-harness/docs/<implementation usage docs>
orca-harness/tests/<unit and contract tests>
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
- Source Quality report-skeleton helper for existing Source Capture Packets;
- agent-facing runbook for bounded runner selection, stops, inspection, and
  reporting.

Recorded architecture boundaries that are not implemented tooling:

- Source Quality State Assembler architecture boundary for a read-only
  multi-row state census over existing packets.

Remaining current gaps:

- no Source Observability integration point;
- no accepted fixture policy for generated packets;
- no rights, retention, or sensitivity rule for durably preserved raw source
  files, screenshots, media, entitled content, or paid-access artifacts.

Deferred gaps that are intentionally outside the first tranche:

- Reddit API registration, OAuth setup, API calls, or PRAW/direct-API adapter;
- password-driven login automation;
- direct browser profile or raw cookie import;
- commercial scraping or fetch-service integration;
- anti-detect browser implementation;
- residential, rotating, or managed proxy integration;
- CAPTCHA-solving or challenge-handling service integration;
- SERP/discovery API integration;
- persistent storage, database, dashboard, queue, scheduler, deployment,
  production crawler, or broad source-system runtime.

## Non-Claims

This README is not validation, readiness, source-of-truth promotion, legal
sufficiency, source-access boundary amendment, contract hardening,
implementation execution, API authorization, commercial-scraper authorization,
anti-detect authorization, proxy authorization, production-runtime
authorization, final packet schema, ECR design, Cleaning implementation,
Judgment design, buyer proof, rights-to-process sufficiency, retention policy,
or commercial-readiness evidence.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Toolbox now has a product-facing entrypoint and folder convention: future toolbox product docs should live under docs/product/source_capture_toolbox while existing controlling authority files remain at their historical paths and are indexed here."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/README.md"
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
  stale_language_search: "rg -n \"Source Capture Toolbox|source_capture_toolbox|Source Capture Packet|source_capture\" .agents/workflow-overlay/artifact-folders.md docs/product/README.md docs/product/source_capture_toolbox/README.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/data_capture_source_access_method_plan_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution"
    - "not source-access boundary amendment"
    - "not ECR, Cleaning, or Judgment design"
```

## Direction Change Propagation - Packet Core Contract Mapping Patch

```yaml
direction_change_propagation:
  doctrine_changed: "The Source Capture Packet core is now explicitly contract-derived: the README maps packet concerns to Data Capture obligations, requires slice-level state where rollups would hide divergence, and states the first local-file CLI mode is no-network."
  trigger: architecture_doctrine
  controlling_sources_updated:
    - "docs/product/source_capture_toolbox/README.md"
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
      reason: "The obligation contract remains the authority; this patch maps the toolbox packet to it without changing Capture obligations."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "Authorized first-tranche build surface did not change."
    - path: "docs/product/data_capture_source_access_method_plan_v0.md"
      reason: "Candidate source-access methods, hard stops, and sequencing did not change."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Source-access boundary permission and hard stops did not change."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading route already points to the toolbox README; no new read-pack entry is required."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes the toolbox README as the product-facing entrypoint."
  stale_language_search: "rg -n \"packet is the spine|acquisition timestamp and cutoff posture|--source-url|no-network.*implied\" docs/product/source_capture_toolbox/README.md"
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
  doctrine_changed: "The Source Capture Toolbox now treats manual-login Playwright storage-state authenticated browser capture as an implemented first-tranche Browser Snapshot extension, with local ignored session-mode sidecar binding, while password automation, direct profile/cookie import, anti-detect, proxy behavior, CAPTCHA solving, and no-entitlement bypass remain deferred or forbidden."
  trigger: lifecycle_boundary
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - "docs/product/source_capture_toolbox/README.md"
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
      reason: "Method sequencing and hard stops did not change; authenticated v0 stays inside the already authorized first-tranche Source Capture Toolbox implementation lane."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "The existing tooling authorization controls the bounded first-tranche build surface; no new API, commercial fetch, anti-detect, proxy, production runtime, ECR, Cleaning, or Judgment authority is introduced."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "Capture obligations and handoff states did not change; packets remain visible limitation carriers only."
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "Source-loading already routes agents to this toolbox README for current component status and gaps; it does not encode per-adapter build status."
    - path: "docs/workflows/orca_repo_map_v0.md"
      reason: "Repo map already indexes this toolbox README as the component/gap entrypoint; no stale logged-in/session-state status was found there."
  stale_language_search: "rg -n \"logged-in/entitled browser session reuse remains|no logged-in/entitled browser session|session/profile/cookie/storage-state reuse|Login-visible or entitled browser session content \\| none yet|not login/session capture\" docs/product/source_capture_toolbox/README.md orca-harness/docs/source_capture_agent_runbook.md orca-harness/docs/source_capture_packet.md orca-harness/README.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not password automation authorization"
    - "not direct profile or raw cookie import authorization"
    - "not anti-detect, proxy, CAPTCHA, API, commercial fetch, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```
