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
content through ordinary HTTP/browser routes.

It should record when only archive metadata is available and when archive body
retrieval fails or is not attempted.

### Honest Browser Snapshot Adapter

Purpose: preserve visible HTML/text/screenshot artifacts for pages requiring
JavaScript rendering or logged-in/entitled visible access.

It is first-tranche only as an honest browser/headless-browser path. Anti-detect,
proxy rotation, CAPTCHA solving, and no-entitlement bypass remain separately
gated.

### Source Observability Helper

Purpose: inspect operator-authored posture records and emit visible limitation
reports.

This helper already exists under `orca-harness/source_observability/`.

It is not a source capture tool. It does not fetch sources, retrieve archives,
preserve media, automate browsers, call APIs, or validate capture. It can later
consume Source Capture Packet metadata or operator records to help keep
limitations visible.

## Current Build Order

1. Design and document this toolbox entrypoint.
2. Build Source Capture Packet core and CLI with local-file packaging only.
3. Dry-run the packet CLI against an already-local source artifact.
4. Add Direct HTTP fetch adapter.
5. Add Media / Asset Preservation adapter.
6. Add Archive.org availability/body adapter.
7. Add Honest Browser Snapshot adapter.
8. Decide separately whether Reddit API, commercial fetch services, anti-detect,
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

The toolbox is not implemented yet. Current gaps:

- no Source Capture Packet schema/model;
- no implementation-facing packet-core spec derived from the obligation mapping
  above;
- no packet writer;
- no hashing helper for packet artifacts;
- no human-readable receipt writer;
- no CLI runner;
- no local-file packaging mode;
- no output lifecycle rule for packet directories;
- no unit tests or contract tests;
- no no-network/no-deferred-adapter guard tests;
- no Direct HTTP adapter;
- no Media / Asset Preservation adapter;
- no Archive.org availability/body adapter;
- no Honest Browser Snapshot adapter;
- no Source Observability integration point;
- no dry-run packet produced from an existing pressure-test artifact;
- no implementation review of source capture code;
- no accepted fixture policy for generated packets;
- no rights, retention, or sensitivity rule for durably preserved raw source
  files, screenshots, media, entitled content, or paid-access artifacts.

Deferred gaps that are intentionally outside the first tranche:

- Reddit API registration, OAuth setup, API calls, or PRAW/direct-API adapter;
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
