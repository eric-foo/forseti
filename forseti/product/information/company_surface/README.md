# Company Surface

```yaml
retrieval_header_version: 1
artifact_role: Company Surface placement front door
scope: >
  Retrieval-only boundary for the Company Surface information domain: its
  relationship to Capture, Data Lake, and the Commission Signal Board. Content,
  record, identity, storage, and consumer-interface design remain deferred.
use_when:
  - Starting Company Surface product-contract work.
  - Deciding whether company evidence belongs to Capture, Company Surface, Data Lake, or CSB.
  - Checking what the Company Surface folder currently authorizes.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - forseti/product/spines/data_lake/README.md
  - forseti/product/spines/commission_signal_board/README.md
stale_if:
  - Company Surface becomes an operational spine or moves to another product axis.
  - An accepted Company Surface contract supersedes this placement-only boundary.
  - Capture, Data Lake, or Commission Signal Board ownership changes materially.
```

Company Surface is the product-information home for a future, reusable account
of what can be observed about a company over time. It is deliberately not named
Company Intelligence: interpretation and action belong to downstream consumers.

## Relationship To Operational Spines

| Area | Relationship |
| --- | --- |
| Capture | Upstream supplier that acquires observations and preserves source receipts and failures. |
| Data Lake | Physical storage owner for captured and derived records; company data does not live in this folder. |
| Commission Signal Board | Operational consumer that may review Company Surface information, form hypotheses, and commission work. |
| Company Surface | Future owner of the shared meaning and history of company-linked observations, without owning capture execution, storage mechanics, or operational decisions. |

## Deferred Content

This folder currently authorizes placement only. The next design phase must
separately decide the Company Surface record contract, company-identity boundary,
history/current-view behavior, Data Lake representation, CSB consumption seam,
and analysis non-claims. No runtime folder, schema, company corpus, source route,
dashboard, scheduler, pain score, or intervention is authorized here.
