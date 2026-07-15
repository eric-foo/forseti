# Company Surface Logical Record And View Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product doctrine contract (Company Surface logical records and views)
scope: >
  Storage-agnostic logical requirements for Company Surface assertions,
  company-linked activity, coverage and failure, append-only correction, and
  reproducible current, historical-restated, and historical-as-known views.
use_when:
  - Designing a Company Surface record, ledger, projection, or consumer view.
  - Deciding which time boundary or evidence cutoff a company view must use.
  - Checking whether company history, uncertainty, coverage, and correction remain inspectable.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/purpose_contract_v0.md
  - forseti/product/information/company_surface/company_identity_boundary_v0.md
  - forseti/product/spines/foundation/ontology/ontology.yaml
  - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
  - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
stale_if:
  - The owner changes the Company Surface purpose or nine success signals.
  - The identity boundary changes subject, relationship, assertion-state, history, or ownership semantics.
  - Foundation changes Brand, Org, owned_by, or subsidiary_of semantics or status.
  - Capture or Data Lake changes a source-receipt, failure, append-only, correction, or physical-ownership boundary consumed here.
```

## Status And Decision

This is the controlling product-doctrine source for the logical Company Surface
record and its time-bounded views. It implements the owner-signed purpose and
accepted identity boundary without choosing a physical schema, identifier
format, store, API, runtime, or materialized view.

Company Surface truth is an append-only set of inspectable records, not one
mutable company row. An upstream observation remains owned by Capture and
physically stored by Data Lake. Company Surface records how that evidence
attaches to a company subject and history without copying or silently upgrading
it. A view is a reproducible projection over records eligible for an explicit
effective boundary and knowledge cutoff. Absence of a record is never evidence
that an activity did not occur or that a source was covered successfully.

The labels below name logical requirements. They are not serialized field names,
a JSON schema, ECR extension, ontology payload, or Data Lake placement decision.

## Logical Record Families

Four families are required. An implementation may use one compatible envelope,
but it may not erase their semantic distinctions.

### Subject assertion

Connects a raw identifier in a stated source context to one Brand or Org. It
preserves the raw identifier and receipt; asserted subject and kind; resolved,
provisional, ambiguous, or unresolved state; competing candidates; applicable
interval and precision; recorded time; limitations; and correction or
supersession references.

Several identifiers may resolve to one subject across time. One identifier may
remain ambiguous between several subjects. Neither permits source rewrite or
subject merge.

### Relationship assertion

Connects Brand owned_by Org or Org subsidiary_of Org. It preserves subject,
relationship and object; effective interval and precision; supporting and
conflicting sources; assertion state and limitation; material source
qualifiers; recorded time; and correction or supersession references.

A minority stake, licence, joint venture, distribution arrangement, or other
relationship absent from Foundation may be preserved as source-backed activity
plus a limitation. owned_by or subsidiary_of must not be overloaded to fake a
fit.

### Company-activity link

Attaches an upstream observation to the Brand or Org it concerns without
duplicating the observation payload. It preserves the observation and receipt
reference, the subject assertion used, the observable activity or source
surface, observation/effective time and precision, recorded time, relevant
capture posture, limitations, alternatives, and later corrections.

It says what evidence concerns which company. It does not say the activity
proves pain, opportunity, traction, contradiction, or an intervention.

### Coverage or failure marker

Makes an attempted, partial, failed, excluded, or not-covered source interval
visible for a subject and surface. It carries the upstream Capture posture and
receipt. It distinguishes available evidence, partial coverage with the missing
boundary named, failed capture, and a surface or interval not covered.

No marker may convert no observation into a resolved negative. Exact
coverage-state labels remain an implementation choice.

## Common Logical Envelope

Every family makes these concepts recoverable:

| Concept | Required meaning |
| --- | --- |
| Stable record reference | Lets later records cite, conflict with, correct, or supersede it. |
| Record family | Keeps resolution, relationships, activity attachment, and coverage/failure distinct. |
| Subject anchors | Names the Brand or Org subjects concerned. |
| Evidence references | Points to supporting and conflicting source/capture material. |
| Semantic state | Uses identity-boundary states where the record resolves meaning. |
| Effective or observation time | Says when company reality applies, with interval and precision. |
| Captured time | Remains recoverable from the upstream receipt. |
| Recorded time | Says when Company Surface committed the record. |
| Limitations and alternatives | Keeps unknowns, conflicts, gaps, and unsupported relations visible. |
| Correction and supersession | Appends change without deleting earlier evidence or as-known history. |

## Time And View Contract

Every view declares two independent boundaries:

1. **effective boundary** — the company-reality time or interval reconstructed;
2. **knowledge cutoff** — the latest Company Surface recorded time it may use.

| View | Effective boundary | Knowledge cutoff | Meaning |
| --- | --- | --- | --- |
| Current | Requested current boundary | Current declared cutoff | Best supported reality at the requested present boundary. |
| Historical, restated | Historical boundary | Later/current cutoff | What later evidence now supports about that period. |
| Historical, as known | Historical boundary | Historical cutoff | What Forseti could reconstruct from records known by then. |

A later-discovered source may change restated history. It cannot appear in an
as-known view whose cutoff predates its Company Surface recorded time.

A view starts from an explicit Brand or Org; admits only records known by its
cutoff; applies only eligible corrections and supersessions; includes activity
intersecting the requested period; carries conflicts, gaps, failures,
alternatives, and limitations; and returns its query boundaries, included
record references, exclusions, and limitations.

Selection reads every required subject and relationship assertion's state and
time precision. The resolved roll-up may attach activity or expand to a related
subject only through resolved assertions whose effective interval is
determinate at the requested boundary under its declared precision.
Provisional, ambiguous, unresolved, or temporally indeterminate assertions
remain visible as alternatives and limitations; they do not enter the resolved
roll-up. Neither convenience nor a missing boundary upgrades an assertion state
or resolves an indeterminate interval.

A later materialized view remains a rebuildable projection, never a second
authority.

## Correction And Conflict Rules

- Correction appends a record that cites what it corrects.
- Supersession changes later eligible selection without erasing the earlier
  record, source, or as-known history.
- Conflicting records coexist until evidence supports resolution.
- An ended relationship remains available to historical views.
- Source unavailability, erasure, or tombstone uses the owning Capture/Data Lake
  mechanism and is carried as a limitation; Company Surface fabricates nothing.
- View exclusion never rewrites the underlying logical history.

## Dogfood Coverage Set

These ten cases are bounded semantic tests, not dossiers, a corpus, or
source-completeness claims.

| Case | Failure mode exercised |
| --- | --- |
| e.l.f. Beauty | Same-name Brand/Org, layered ownership, acquisition, exit, coarse time. |
| Alphabet / Google | New holding-company Org while Google continues as subsidiary. |
| Block / Square | Org legal rename while Square Brand persists. |
| Johnson & Johnson / Kenvue | Separation plus residual minority stake. |
| GE | Staged three-company separation plus continuity as GE Aerospace. |
| Kellogg / Kellanova / WK Kellogg | Same-day Org rename and spin-off. |
| Estée Lauder / DECIEM | Minority, majority, and full-ownership stages. |
| Dove | One raw Brand name for unrelated personal-care and chocolate subjects. |
| Supreme | Brand transfer with completion-versus-announcement date distinction. |
| TOM FORD | Ownership differs from licensed operation. |

### 1. e.l.f. Beauty

The fiscal-2026 10-K and corporate brands page support separate Brand and Org
subjects, layered subsidiaries, rhode entering on 2025-08-05, and Keys Soulcare
leaving in May 2026 with no exact day. A current view excludes Keys Soulcare; a
pre-acquisition view excludes rhode's later relationship. The filing does not
pin every intermediate ownership tier; an unpinned tier stays provisional rather
than being flattened into the registrant.

- https://www.sec.gov/Archives/edgar/data/1600033/000160003326000020/elf-20260331.htm
- https://www.elfbeauty.com/brands

### 2. Alphabet and Google

Alphabet's 2015 10-K says the October 2 reorganization made Google a direct,
wholly owned subsidiary of the new Alphabet holding company. A prior view must
not back-project Alphabet as parent. Google continues as an Org; the parent does
not replace it.

- https://www.sec.gov/Archives/edgar/data/1652044/000165204416000012/goog10-k2015.htm

### 3. Block and Square

Block's announcement distinguishes the corporate rename from continuing Square,
Cash App, TIDAL, and other brands. Square, Inc. became Block, Inc. effective
2021-12-10 while the Square Brand remained. Time-scoped identifiers may map to
one continuing Org; the Brand must not be renamed into Block.

- https://investors.block.xyz/investor-news/news-details/2021/Square-Inc.-Changes-Name-to-Block/default.aspx

### 4. Johnson & Johnson and Kenvue

Johnson & Johnson described the 2023 separation as complete while reporting a
retained 9.5% Kenvue stake on 2023-08-30. Both facts remain visible. The base
vocabulary has no Org equity-stake relationship and does not justify continuing
subsidiary_of. Preserve the stake as activity plus a limitation; do not collapse
it into a clean no-relationship claim.

- https://www.investor.jnj.com/investor-news/news-details/2023/Johnson--Johnson-Announces-Updated-Financials-and-2023-Guidance-Following-Completion-of-the-Kenvue-Separation/default.aspx

### 5. GE

Official materials record GE HealthCare becoming independent in January 2023
and GE Vernova on 2024-04-02. The continuing GE listed company operates as GE
Aerospace. The view creates distinct spun-off Orgs while preserving continuity
of the original Org.

- https://www.ge.com/news/reports/ge-completes-the-separation-of-ge-healthcare
- https://www.ge.com/news/press-releases/ge-aerospace-launches-as-independent-investment-grade-public-company-following

### 6. Kellogg, Kellanova, and WK Kellogg

The 2023 separation created WK Kellogg Co while Kellogg Company changed its name
to Kellanova on 2023-10-02. The view models a new spun-off Org and a continuing
renamed Org, not two renames and not one merged successor.

- https://investor.kellanova.com/news-events/news-details/2023/KELLOGG-COMPANY-BOARD-OF-DIRECTORS-APPROVES-SEPARATION-INTO-TWO-COMPANIES-KELLANOVA-AND-WK-KELLOGG-CO/default.aspx
- https://investor.kellanova.com/files/doc_downloads/kd/2024/k-2023-q4-10-k-final-2-20-24.pdf

### 7. Estée Lauder and DECIEM

Estée Lauder first invested in 2017, became majority owner in 2021, and bought
the remaining interests on 2024-05-31. One timeless edge destroys those stages.
Where binary vocabulary cannot express the share posture precisely, the record
carries the activity, qualifier, and limitation.

- https://www.elcompanies.com/en/news-and-media/newsroom/press-releases/2024/06-03-2024-114511824

### 8. The two Dove brands

Unilever identifies Dove among personal-care brands; Mars identifies DOVE among
chocolate brands. A context-free Dove identifier remains ambiguous between two
unrelated Brand subjects. Category, source context, and owner may resolve an
observation; spelling never creates identity.

- https://www.unilever.com/brands/personal-care/
- https://www.mars.com/our-brands/all-brands

### 9. Supreme

VF reported Supreme becoming its wholly owned subsidiary on 2020-12-28 and
later sold it to EssilorLuxottica. VF's 8-K says completion was 2024-10-01 while
the joint closing release is dated October 2. History preserves acquisition,
transfer, both receipts, and completion-versus-announcement meaning.

- https://www.vfc.com/news/press-release/1741/vf-corporation-completes-acquisition-
- https://www.vfc.com/investors/financial-information/sec-filings/content/0001193125-24-230625/0001193125-24-230625.pdf
- https://www.vfc.com/news/press-release/1841

### 10. TOM FORD

Estée Lauder became sole owner of the Brand and intellectual property on
2023-04-28 while licensing the trademark to Zegna for fashion/accessories and
Marcolin for eyewear. owned_by may carry supported ownership. Licences remain
source-backed activity and limitations until Foundation adopts suitable
vocabulary; licensees are not owners.

- https://www.elcompanies.com/en/news-and-media/newsroom/press-releases/2023/04-28-2023-171511000

## Dogfood Result

The contract passes only if one logical model distinguishes subjects,
relationships, activities, and coverage; represents rename, new parent,
acquisition, stages, transfer, spin-off, split, and unsupported relations;
produces all three view modes; retains exact, coarse, conflicting, and unknown
time; preserves source and capture failures; and refuses convenient answers
when evidence supports ambiguity or absent vocabulary.

## Nine Success Signals Made Testable

| Owner-signed signal | Testable behavior |
| --- | --- |
| Company reality is reconstructable | A bounded view returns company-linked activity for an explicit period and anchor. |
| History is preserved | Append, supersession, effective time, and cutoff reconstruct earlier states. |
| Material statements are inspectable | Records retain evidence, time, state, limitations, and capture posture. |
| Evidence is reusable | Consumers derive views from one history, not separate dossiers. |
| The center is decision-agnostic | No pain score, preferred conclusion, or action enters the record. |
| Acute problems are investigable | Consumers can align changes and contradictions while owning conclusions. |
| Unknowns remain visible | Ambiguity, unsupported relations, gaps, and failure are first-class. |
| New surfaces extend one foundation | New observations and coverage markers reuse the company-link contract. |
| GTM becomes specific | GTM may consume a traceable view; Company Surface supplies no pitch or contact authority. |

## Acceptance Conditions

1. The four record families remain distinguishable.
2. Every material assertion is source-backed, time-bounded, stateful, and inspectable.
3. Effective boundary and knowledge cutoff can produce different correct views.
4. Correction and supersession preserve as-known history.
5. Unsupported relations remain visible without ontology overloading.
6. Missing or failed coverage never becomes a resolved negative.
7. Views are reproducible and never become a second authority.
8. All ten cases fit with their stated residuals.
9. All nine owner-signed signals map to observable behavior.
10. Capture and Data Lake retain their ownership boundaries.

## Ownership Boundary

| Layer | Owns | Does not own |
| --- | --- | --- |
| Foundation | Brand, Org, owned_by, subsidiary_of, and graduation. | Company-specific truth or history. |
| Capture | Observations, raw identifiers, receipts, capture time/posture, and failures. | Company-level resolution or roll-up. |
| Company Surface | Logical assertions, observation attachment, coverage meaning, correction history, and views. | Acquisition, storage, analysis, pain, or action. |
| Data Lake | Physical append-only persistence, tombstones, and generated retrieval when authorized. | Company-specific semantic truth or view meaning. |
| Consumers | Query period and conclusions. | Rewriting history or hiding limitations. |

## Non-Goals And Next Decision

This contract does not establish serialized fields, canonical IDs, schema,
Org graduation, new relationships, matching, scoring, review queues, Data Lake
pathing or materialization, capture routes, access, cadence, scheduler, corpus,
API, UI, dashboard, feed, runtime, pain, GTM, outreach, or intervention.

Before an ontology-governed implementation encodes Org, Foundation must
graduate it. The next implementation decision is then a separate mapping into
Data Lake derived records and generated read models, beginning with one bounded
company observation family rather than a broad corpus.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Company Surface now has a storage-agnostic logical record and temporal-view
    contract: four inspectable record families, append-only correction, dual
    effective/knowledge boundaries, reproducible views, and ten-case dogfood.
  trigger: product_doctrine
  related_triggers: [architecture_doctrine]
  controlling_sources_updated:
    - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
    - forseti/product/information/company_surface/company_identity_boundary_v0.md
    - forseti/product/information/company_surface/purpose_contract_v0.md
    - forseti/product/information/company_surface/README.md
    - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  downstream_surfaces_checked:
    - forseti/product/information/README.md
    - forseti/product/spines/foundation/ontology/ontology.yaml
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
    - docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: Foundation ontology
      reason: Org remains reserved; this unit adds no relationship or graduation.
    - path: company-aggregate capture decision
      reason: Its row already preserves raw identity, time, provenance, limitations, and append-only history while delegating entity_key meaning.
    - path: Data Lake contracts
      reason: Physical persistence and retrieval remain separate Data Lake decisions.
    - path: runtime or stored company data
      reason: No implementation, adapter, matcher, corpus, materialization, or migration is authorized.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: The existing Company Surface front door remains the route; the map is not a per-contract inventory.
  stale_language_search: >
    rg -n -i "[c]ompany Surface record contract.*deferred|[h]istory/current-view.*deferred|[e]xternal entity-resolution owner|[f]oundation/ontology/architecture.md|[d]ata_lake/core/contracts/silver_contract_v0.md"
    forseti/product/information/company_surface
    forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  stale_language_search_result: >
    Run on the authoring worktree (2026-07-15). No hits remain in the Company
    Surface contracts or the linked Capture corpus-intake contract.
  non_claims:
    - not schema, storage mapping, canonical ID, materialized view, or runtime
    - not Org graduation or new relationship vocabulary
    - not stored corpus, source completeness, validation, or readiness proof
    - not buyer proof, GTM, outreach, contact, or intervention authorization
```
