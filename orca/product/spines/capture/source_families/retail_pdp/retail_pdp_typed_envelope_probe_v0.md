# Retail/PDP Typed Envelope Probe v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture probe
scope: >
  Bounded non-IG fit check for whether Retail/PDP source-family payloads can
  live in packet/slice-keyed typed envelopes instead of new SourceCaptureSlice
  fields.
use_when:
  - Checking the first non-IG typed-envelope probe for the data-lake mechanics map.
  - Planning envelope physical storage after payload-boundary acceptance.
  - Reviewing Retail/PDP projection boundaries before ECR, Cleaning, or Judgment sequencing.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md
  - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
branch_or_commit:
  - Stacked on codex/data-lake-mechanics-map at 482b499c; verify PR #225 and PR #226 landing state before treating this as mainline context.
stale_if:
  - The payload-boundary lane or data-lake mechanics map is rejected or materially changed.
  - Retail/PDP projection row kinds, binding map, residual vocabulary, or raw-anchor model materially change.
  - A later accepted storage, manifest, sidecar, projection-cache, or envelope-serialization decision supersedes this logical probe.
```

## Status

`NON_IG_ENVELOPE_PROBE_RETAIL_PDP_V0`.

Mini god tier lens: prove the useful thing and stop. This artifact answers one
question: **can a non-IG source family fit the packet/slice-keyed typed-envelope
boundary without adding new core slice fields?**

Answer: **yes, logically.** This does not select physical storage, serialize an
envelope, migrate incumbent fields, wire ECR/Cleaning, or claim readiness.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (payload boundary + data-lake mechanics + Retail/PDP Armory playbooks + projection code/tests)
  edit_permission: docs-write
  target_scope:
    - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md
    - orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  dirty_state_checked: yes
  isolation: worktree branch codex/non-ig-envelope-probe-retail-pdp stacked on codex/data-lake-mechanics-map
external_source_boundary: local Orca sources only
doctrine_propagation_expected: architecture_doctrine
```

## Result

Retail/PDP passes the logical envelope fit check:

```text
SourceCapturePacket stays canonical.
Retail/PDP-specific payload gets a packet/slice-keyed logical envelope.
Projection remains a re-derivable view.
ECR, Cleaning, and Judgment consume by key/ref instead of copying raw truth.
```

The probe is strong because Retail/PDP is not IG-like: it has product pages,
retailers, SKUs, prices, availability, review substrate, embedded structured
JSON, carried modules, and source-specific residual traps. If that payload can
stay out of core slice fields, the boundary is doing useful work.

## Evidence

| Check | Finding |
| --- | --- |
| Raw key exists | `RetailProjectionRawRef` carries `packet_id` and `slice_id`. |
| Raw file anchor exists | `RetailProjectionRawAnchor` carries `file_id`, relative packet path, `sha256`, `hash_basis`, anchor kind, and anchor value. |
| Source-family payload is separable | Allowed rows are Retail/PDP-specific: product, variant offer, review substrate, embedded structured JSON, and carried module. |
| Absence/traps are retained | Residuals cover rendered-DOM absence, Amazon fallback price, Sephora DOM/JSON traps, and Ulta requested-vs-rendered SKU mismatches. |
| Projection is derived | The helper writes projection JSON from an existing packet directory; it does not fetch, clean, run ECR, or judge. |
| Judgment leakage is guarded | Projection models reject Judgment-smuggling field names and certify `view_only; not_cleaned; not_normalized; not_judgment_ready`. |
| Capture opt-in is bounded | CloakBrowser packet capture may write a Retail/PDP projection sidecar only with `--source-family retail_pdp --retail-pdp-projection-output <path>`. |

## Logical Envelope Shape

This is a slot test, not a final schema:

```yaml
retail_pdp_payload_envelope:
  packet_id: raw packet key
  slice_id: raw slice key
  source_family: retail_pdp
  payload_kind: retail_pdp_product_page_payload
  payload_schema_version: retail_pdp_payload_v0
  source_locator_ref: source locator from the packet/slice
  pins:
    locale_pin: carried or unknown/not-applicable posture
    currency_pin: carried or unknown/not-applicable posture
    variant_pin: carried or unknown/not-applicable posture
  preserved_file_refs:
    - file_id
    - relative_packet_path
    - sha256
    - hash_basis
    - anchor_kind
    - anchor_value
  source_visible_payload:
    - product context
    - variant offer substrate
    - review substrate
    - embedded structured JSON refs
    - carried modules
  residuals: source-visible gaps, mismatches, and fallback warnings
  limitations: packet/capture limitations that must ride forward
```

Derived projection receipts may point at this envelope, but they are not the
envelope and must not become source truth.

## Flow Impact

```text
Source Capture
  -> SourceCapturePacket [canonical raw authority]
       |- stable core facts: where, when, how, packet/slice/file keys
       |- Retail/PDP typed envelope: retailer/product/SKU/price/review substrate
  -> Retail/PDP projection view [derived, re-runnable]
  -> ECR/SCR by raw key/ref
  -> Cleaning by raw handle + sibling refs
  -> Judgment by full derivation chain + raw pull-in when needed
```

## Rules Locked By This Probe

1. Do not add Retail/PDP product, price, review, retailer-module, or SKU-detail
   fields directly to `SourceCaptureSlice`.
2. Do not treat Retail/PDP projection JSON as canonical source truth.
3. Do not let ECR, SCR, or Cleaning become the capture-payload home.
4. Carry source-visible residuals forward; do not convert them into exclusion,
   credibility, or strength labels.
5. Keep final physical representation open until the storage lane selects it.

## Clears

This clears the data-lake mechanics gate that required one non-IG family to
show logical packet/slice-keyed envelopes can work without direct new
`SourceCaptureSlice` fields.

It clears only that logical gate.

## Does Not Clear

Foregone on purpose:

- no universal envelope schema;
- no storage engine;
- no manifest v2;
- no sidecar serialization contract;
- no projection cache;
- no migration of incumbent fields;
- no live Retail/PDP smoke in this pass;
- no ECR or Evidence Unit final schema;
- no Cleaning runtime schema;
- no Judgment authorization;
- no validation/readiness claim.

## Next Gate

Open the physical envelope/storage lane next. Its job is to pick one durable
representation for typed envelopes: manifest child, immutable sidecar, hash-
pinned envelope bundle, or another low-lock-in form. It should use this probe as
input, not as implementation authority.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    This artifact records Retail/PDP as the first non-IG logical fit probe for
    the packet/slice-keyed typed-envelope boundary: its source-family payload
    can live outside direct SourceCaptureSlice fields while raw packet truth
    remains canonical and projection remains derived.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md
    - orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - orca/product/shared/data_lake_mechanics/core_spine_v0_data_lake_mechanics_map_v0.md
    - orca/product/spines/capture/source_capture_toolbox/README.md
    - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
    - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md
    - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
    - orca-harness/source_capture/retail_pdp_projection.py
    - orca-harness/runners/run_source_capture_cloakbrowser_packet.py
    - orca-harness/runners/run_retail_pdp_projection.py
    - orca-harness/tests/unit/test_retail_pdp_projection.py
    - orca-harness/tests/unit/test_source_capture_cloakbrowser_snapshot.py
  intentionally_not_updated:
    - path: orca-harness/source_capture/retail_pdp_projection.py
      reason: Probe is architecture-only; existing helper already demonstrates the logical shape.
    - path: orca-harness/source_capture/models.py
      reason: No new SourceCaptureSlice field or schema migration is authorized.
    - path: docs/workflows/ecr_spine_submap_v0.md
      reason: This probe keeps ECR by-key consumption unchanged and does not bind final Evidence Unit shape.
  stale_language_search: >
    rg -n "Retail/PDP.*envelope|retail_pdp.*SourceCaptureSlice|retail_pdp_product_page_payload|retail_pdp_projection|not_judgment_ready"
    docs/product docs/workflows orca-harness/source_capture orca-harness/runners orca-harness/tests
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not storage selection
    - not manifest or sidecar contract
    - not ECR, Cleaning, or Judgment design
```
