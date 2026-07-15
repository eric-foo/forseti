# Company Surface Purpose Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product doctrine contract (Company Surface purpose)
scope: >
  Owner-signed purpose, problem, nine success signals, proof boundary, and
  non-goals for the decision-agnostic Company Surface information domain.
use_when:
  - Explaining why Company Surface exists or what problem it solves.
  - Evaluating work against the accepted Company Surface success signals.
  - Separating observable company reality from downstream analysis, GTM, CSB, or interventions.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/README.md
  - forseti/product/information/company_surface/company_identity_boundary_v0.md
  - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
stale_if:
  - The owner changes Company Surface's purpose, problem, success signals, or non-goals.
  - Company Surface moves, becomes an operational spine, or its ownership boundary changes materially.
```

## Status And Authority

This is the controlling source for the owner-signed Company Surface purpose,
problem, nine success signals, downstream proof boundary, and non-goals. It
establishes purpose doctrine only. Company-identity semantics are controlled by
`company_identity_boundary_v0.md`. This purpose contract does not establish a
record model, history/current-view mechanics, storage representation, consumer
interface, runtime, stored company corpus, source access, validation, readiness,
buyer proof, or GTM authorization.

## Purpose

Company Surface preserves what a company is observably doing and how that
changes over time, so Forseti can reason from reality before deciding what it
means or what to do.

It builds a reusable, inspectable history of each company's externally
observable actions and commitments - for example ads, sponsored creators,
launches, pricing moves, hiring, distribution changes, and product activity.

Company Surface records observable reality once so CSB, GTM analysis, product
analysis, and future interventions can reuse it without rebuilding the evidence
for every decision.

It owns what was observed, when, about which company, from where, and with what
limitations. It does not decide whether an observation represents pain,
opportunity, contradiction, or the correct intervention.

## Problem

Forseti cannot reliably understand a company's current situation from isolated
observations. Relevant evidence is scattered across sources and capture runs,
loses historical context, may not be reliably linked to the correct company,
and often must be collected again for each analysis.

This causes:

- individual ads, sponsorships, hires, or launches to be seen without the company's overall pattern;
- loss of what changed, persisted, or disappeared;
- repeated reconstruction of the same company background;
- acute contradictions to be missed or mistaken for ordinary noise;
- GTM approaches based on generic assumptions rather than evidence of a costly, current problem; and
- conclusions detached from source, timing, failure, and alternative explanations.

The main problem is that Forseti lacks a reusable, source-backed account of
what a company is actually doing over time. Without it, downstream consumers
cannot reliably distinguish acute, material pain from weak signals or generic
company context.

## Needed Change

For any company placed in scope, Forseti must be able to reconstruct its
observable activity and changes from traceable evidence without first choosing
a decision, pain hypothesis, or intervention.

## Nine Success Signals

1. **Company reality is reconstructable.** A consumer can answer what the company is visibly running, doing, or changing for a stated period.
2. **History is preserved.** New observations extend the company record rather than silently replacing prior reality.
3. **Every material statement is inspectable.** Observations retain source, timestamp, company link, provenance, limitations, and relevant capture failures.
4. **Evidence is reusable.** CSB and different analyses can consume the same company history without recapturing it or maintaining separate company dossiers.
5. **The center remains decision-agnostic.** The record contains no canonical pain score, recommended action, or preferred intervention. Different consumers may reach different conclusions from the same evidence.
6. **Acute problems become investigable.** Downstream consumers can identify or reject material contradictions - such as visible spending without corresponding traction, rapid strategy changes, or commitments conflicting with market response - and trace the hypothesis back to evidence.
7. **Unknowns remain visible.** Missing coverage, failed capture, uncertain company identity, and plausible alternative explanations remain explicit rather than becoming false certainty.
8. **New surfaces extend the same foundation.** Adding an observable surface requires a source-specific capture route and mapping, not another company-information architecture.
9. **GTM becomes more relevant and specific.** Downstream GTM can use current, traceable observations to understand what a company is visibly investing in or changing, ask sharper company-specific questions, and avoid generic pitches.

Success signal 9 remains downstream and decision-agnostic: the GTM consumer
owns the pain hypothesis and approach. Company Surface does not infer private
pain, select the pitch, authorize contact, or turn observations into an
outreach list.

## Ownership Boundary

- **Capture** acquires observations and preserves source receipts and failures.
- **Data Lake** owns physical storage.
- **Company Surface** owns the shared meaning and history of company-linked observations.
- **CSB, analyses, GTM, and interventions** consume that information and decide what it means or what to do.

Actual company records do not live in this documentation folder.

## Downstream Product-Proof Signal

The stronger later signal is not that Forseti collected a large amount of
company data. It is that, during a real decision, Company Surface materially
reduces the work required to establish company reality and helps a consumer
change, defend, or reject a consequential prioritization.

Buyer pull, repeat use, willingness to pay, and better decisions remain
downstream proof. This purpose contract does not establish them.

## Non-Goals

Company Surface is not:

- a broad company inventory built for its own sake;
- a social-listening dashboard or monitoring feed;
- the physical data store;
- the capture executor;
- Company Intelligence or a pain-scoring engine;
- an outreach list or person-level dossier;
- the CSB, an analysis conclusion, or an intervention; or
- proof that any identified pain is real or commercially valuable.

Do not encode "barge in" or plausible-deniability outreach as Company Surface
purpose. Those are possible downstream intervention tactics. Encoding them here
would corrupt the decision-agnostic evidence foundation.

## Deferred Decisions

The company-identity boundary is controlled separately by
`company_identity_boundary_v0.md`. The record contract, history/current-view
mechanics, Data Lake representation, consumer interfaces, runtime,
source-specific capture routes, and stored corpus remain deferred. This
contract grants no implementation authority for them.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Company Surface now has an owner-signed purpose contract binding its
    problem, needed change, nine success signals, downstream proof boundary,
    ownership boundary, and non-goals around a decision-agnostic evidence center.
  trigger: product_doctrine
  controlling_sources_updated:
    - forseti/product/information/company_surface/purpose_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/information/company_surface/README.md
    - forseti/product/information/README.md
    - forseti/product/README.md
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
    - docs/workflows/forseti_repo_map_v0.md
    - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
    - forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/commission_signal_board/README.md
    - .agents/workflow-overlay/product-proof.md
    - forseti/product/spines/product_lead/gtm/forseti_demand_signal_gtm_design_v0.md
    - forseti-harness/
  intentionally_not_updated:
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: The T1 route already opens both front doors; a per-contract row would violate its per-file-inventory boundary.
    - path: docs/decisions/forseti_spine_first_target_structure_binding_v0.md
      reason: The placement and ownership split remain accurate; the named mechanics remain deferred.
    - path: product thesis, Core Spine contract, and product-proof authority
      reason: They already keep evidence inspectable, decisions downstream, and buyer-proof claims gated.
    - path: Capture, Data Lake, and CSB controlling surfaces
      reason: Their acquisition, physical-storage, and operational-consumer responsibilities remain unchanged.
    - path: GTM and intervention surfaces
      reason: Company Surface supplies observations only; it binds no pain hypothesis, pitch, outreach, contact, or intervention.
    - path: forseti-harness/, stored data, and schema surfaces
      reason: No Company Surface runtime, stored corpus, or schema exists or is authorized by this docs-only contract.
  stale_language_search: >
    rg -n -i "[f]uture contract|[f]uture owner|[p]lacement only|[c]ontent .*deferred"
    forseti/product/information docs/workflows/forseti_repo_map_v0.md
  non_claims:
    - not validation or readiness
    - not implementation or runtime authorization
    - not buyer proof or willingness-to-pay proof
    - not GTM, outreach, contact, or intervention authorization
```
