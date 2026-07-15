# Company Surface

```yaml
retrieval_header_version: 1
artifact_role: Company Surface front door
scope: >
  Retrieval-only entry point for the Company Surface information domain: its
  accepted purpose, identity boundary, logical record and view contract,
  relationship to Capture, Data Lake, and the Commission Signal Board, and
  still-deferred mechanics.
use_when:
  - Starting Company Surface product or contract work.
  - Deciding whether company evidence belongs to Capture, Company Surface, Data Lake, or CSB.
  - Checking what the Company Surface folder currently authorizes.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/purpose_contract_v0.md
  - forseti/product/information/company_surface/company_identity_boundary_v0.md
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
  - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
  - forseti/product/spines/data_lake/README.md
  - forseti/product/spines/commission_signal_board/README.md
stale_if:
  - Company Surface becomes an operational spine or moves to another product axis.
  - The Company Surface purpose or identity contract is superseded or its ownership boundary changes.
  - The Company Surface logical record or temporal-view contract is superseded.
  - Capture, Data Lake, or Commission Signal Board ownership changes materially.
```

Company Surface preserves what a company is observably doing and how that
changes over time so downstream consumers can reason from reality. Its accepted
purpose, problem, success signals, and non-goals are controlled by
`purpose_contract_v0.md`. The semantic company-identity boundary is controlled
by `company_identity_boundary_v0.md`. The storage-agnostic record families,
correction rules, and current/history view semantics are controlled by
`company_logical_record_and_view_contract_v0.md`. It is deliberately not named
Company Intelligence: interpretation and action belong to downstream consumers.

## Relationship To Operational Spines

| Area | Relationship |
| --- | --- |
| Capture | Upstream supplier that acquires observations and preserves source receipts and failures. |
| Data Lake | Physical storage owner for captured and derived records; company data does not live in this folder. |
| Commission Signal Board | Operational consumer that may review Company Surface information, form hypotheses, and commission work. |
| Company Surface | Owner of the shared meaning and history of company-linked observations, without owning capture execution, storage mechanics, or operational decisions. |

## Accepted Purpose And Deferred Mechanics

The purpose, identity boundary, and logical record/view contracts are accepted
product doctrine. Data Lake representation, consumer interfaces, and runtime
remain deferred. No
runtime folder, schema, company corpus, source route, dashboard, scheduler, pain
score, or intervention is authorized here.
