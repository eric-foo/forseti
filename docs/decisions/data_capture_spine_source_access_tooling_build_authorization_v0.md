# Data Capture Spine Source-Access Tooling Build Authorization v0

```yaml
retrieval_header_version: 1
artifact_role: Product decision
scope: Owner authorization for bounded first-tranche Data Capture source-access tooling builds after the first pressure-test foundation closeout.
use_when:
  - Checking whether Data Capture source-access tooling builds are now allowed.
  - Scoping or implementing the first tranche of local source-access/capture-support tools.
  - Distinguishing first-tranche build authority from later API, proxy, anti-detect, commercial fetch, storage, dashboard, or downstream-spine work.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/README.md
  - docs/product/data_capture_source_access_method_plan_v0.md
  - docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md
  - docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md
stale_if:
  - A later owner decision supersedes the first-tranche build scope.
  - The source-access boundary decision materially changes hard stops or disclosability requirements.
  - The Data Capture obligation contract, Data Capture/Cleaning/Judgment boundary, or source-access method plan materially changes source-acquisition obligations.
  - First-tranche implementation exposes an access, fidelity, provenance, rights, or boundary issue that cannot be represented by the authorized packet/adapter surface.
```

## Status And Decision

Status: `AUTHORIZED_BOUNDED_SOURCE_ACCESS_TOOLING_BUILD_V0`.

Owner decision:
`AUTHORIZE_BOUNDED_SOURCE_ACCESS_TOOLING_BUILD_FIRST_TRANCHE`.

Data Capture source-access tooling builds are now allowed inside the bounded
first tranche below. This decision supersedes prior "not build tools now" and
`defer_until_separate_owner_authorization` language for this first tranche only.

This is not blanket authorization for every source-access method named in the
method plan. The authorization is deliberately narrow enough that implementation
can start without silently selecting high-risk adapters, downstream schema, or
production infrastructure.

## Source Basis

Decision inputs:

- Current owner instruction: "first, update docs to state building out tools are okay".
- `docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md`.
- `docs/product/data_capture_source_access_method_plan_v0.md`.
- `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md`.
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.
- `.agents/workflow-overlay/source-loading.md`.

The pressure-test foundation is good enough to stop treating all source-access
tooling as premature. The strongest repeated pressure is not a need for
Judgment, Cleaning, or ECR design; it is source observability, source-language
fidelity, archive/media preservation, and inspectable acquisition receipts.

## Authorized First-Tranche Build Surface

The first tranche may build local source-access/capture-support tooling for:

1. **Source Capture Packet core and CLI**
   - create a local packet for one requested source or small source set;
   - preserve raw/source-visible artifacts where available;
   - record locator, acquisition time, cutoff posture, access posture, hashes,
     warnings, and limitation notes;
   - emit a human-inspectable packet receipt.

2. **Direct HTTP fetch adapter**
   - retrieve public or discoverable pages when normal HTTP access works;
   - preserve response body, headers useful for provenance, final URL, status,
     and hash;
   - record access failures visibly rather than hiding them.

3. **Media / asset preservation adapter**
   - fetch and preserve source-linked images, galleries, screenshots, or other
     media artifacts when they carry source meaning and remain inside the
     source-access boundary;
   - record pointer-only or unavailable media explicitly when preservation fails.

4. **Archive.org availability and snapshot adapter**
   - query archive availability/CDX metadata;
   - retrieve snapshot body content when accessible through ordinary HTTP/browser
     routes;
   - distinguish archive availability from archive-body retrieval.

5. **Honest browser snapshot adapter**
   - use a normal browser/headless-browser path for pages that require
     JavaScript rendering or logged-in/entitled visible access;
   - preserve visible HTML/text/screenshot artifacts and receipt metadata;
   - avoid anti-detect, proxy rotation, or no-entitlement bypass in this tranche.

These tools should produce capture-support artifacts. They must not decide
credibility, usefulness, inclusion, exclusion, discounting, Signal Use, Decision
Strength, Action Ceiling, buyer proof, or commercial meaning.

## Deferred Or Separately Authorized Build Surface

The following remain in-bounds method candidates under the source-access method
plan, but are not authorized for first-tranche implementation by this decision:

- Reddit API registration, OAuth setup, API calls, or PRAW/direct-API adapter
  implementation unless a later owner/post-sale/scale/source-specific decision
  chooses it;
- commercial scraping or fetch-service integration;
- anti-detect browser implementation;
- residential, rotating, or managed proxy integration;
- CAPTCHA-solving or challenge-handling service integration;
- SERP/discovery API integration;
- persistent storage, database, dashboard, queue, scheduler, deployment,
  production crawler, or broad source-system runtime.

If any deferred surface becomes necessary, write a separate owner authorization
that names the adapter, source family, risk posture, and non-claims.

## Boundary Guards

This authorization does not change the source-access boundary. The hard stops
remain:

- no-entitlement gate bypass;
- stolen credentials, stolen cookies, or nonconsensual sessions;
- security exploits, malware, credential stuffing, or obvious cross-account,
  private, admin, or confidential spillover once noticed;
- methods Orca would refuse to disclose internally;
- anything clearly illegal or too morally compromising for Orca to own.

The first tranche may use free/account-created access and legitimately entitled
paid/client/coworker access where it stays within the boundary and records the
access posture visibly.

## Non-Claims

This decision is not validation, readiness, pressure-test discharge, source
adequacy, capture closure, source-of-truth promotion, contract hardening,
source-access boundary amendment, ECR design, Cleaning implementation, Judgment
design, buyer proof, commercial-readiness evidence, API authorization,
commercial-scraper authorization, anti-detect authorization, proxy
authorization, production-runtime authorization, storage authorization,
dashboard authorization, deployment authorization, or legal sufficiency.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Data Capture source-access tooling is no longer globally deferred: the owner authorized a bounded first-tranche build surface for local Source Capture Packet core, direct HTTP, media/asset preservation, archive availability/body retrieval, and honest browser snapshot support, while leaving API/commercial/anti-detect/proxy/production runtime surfaces separately gated."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
    - "docs/product/data_capture_source_access_boundary_decision_v0.md"
    - "docs/product/data_capture_source_access_method_plan_v0.md"
    - "docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
    - "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "Top-level rule already permits bounded implementation when a current turn or accepted handoff explicitly authorizes it."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Source hierarchy and propagation mechanics did not change; this decision uses the existing lifecycle_boundary trigger."
    - path: "docs/product/data_capture_source_access_boundary_decision_v0.md"
      reason: "Boundary permission and hard stops did not change; only build authority changed."
    - path: "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
      reason: "The requirements-boundary decision remains accurate for RQ classification and already says implementation needs separate owner authorization; this later decision supplies that authorization for a different first-tranche source-access scope."
    - path: "docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md"
      reason: "The prior local-helper execution authorization remains accurate for that helper and does not need to become source-access build authority."
    - path: "docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md"
      reason: "The obligation contract already allows runtime work when the current turn or accepted handoff authorizes it; this decision does not amend Capture obligations or harden the contract."
  stale_language_search: "rg -n \"not build tools now|defer_until_separate_owner_authorization|No build, no install, no runtime authorized|No build authorization|build_authorization: NOT GRANTED|source-access implementation, runtime/tooling\" docs/product/data_capture_source_access_method_plan_v0.md docs/product/data_capture_spine_pressure_test_closeout_synthesis_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not API, commercial-scraper, anti-detect, proxy, or production-runtime authorization"
    - "not ECR, Cleaning, or Judgment design"
```
