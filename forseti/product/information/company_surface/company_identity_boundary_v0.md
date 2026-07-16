# Company Surface Identity Boundary Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product doctrine contract (Company Surface identity boundary)
scope: >
  Semantic boundary for deciding what company subject an observation concerns,
  how Brand and Org remain distinct, how company-specific identity and
  relationship assertions retain uncertainty and history, and which layer owns
  each part of that meaning.
use_when:
  - Linking captured company evidence to a reusable Company Surface subject.
  - Deciding whether two identifiers refer to the same brand or organization.
  - Representing brand ownership, organization hierarchy, acquisitions, transfers, or unresolved identity.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/purpose_contract_v0.md
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
  - forseti/product/spines/foundation/ontology/ontology.yaml
  - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
  - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  - forseti/product/spines/data_lake/README.md
stale_if:
  - The owner changes which layer owns company-specific identity resolution.
  - Foundation changes the meaning or status of Brand, Org, owned_by, or subsidiary_of.
  - The logical record/view contract changes identity assertion or temporal-view semantics.
  - Company Surface gains a superseding record, identity, or history contract.
```

## Status And Decision

This is the controlling product-doctrine source for the Company Surface identity
boundary. It resolves what the purpose contract means by linking an observation
to the correct company without yet choosing a physical record shape.

The decision is:

- a company subject may be a market-facing **Brand** or an operating/legal
  **Org**; those are different subjects even when they share a name;
- Foundation owns the common Brand, Org, owned_by, and subsidiary_of
  vocabulary;
- Company Surface owns inspectable, company-specific assertions that connect
  raw identifiers to those subjects and relate those subjects over time;
- identity and relationship claims retain uncertainty, provenance, and history
  rather than being collapsed into one silently mutable company identifier; and
- a company roll-up is a time-bounded view across asserted relationships, not a
  destructive merge of brands and organizations.

This contract did not itself graduate Org or authorize schema, storage, API,
matching, or runtime work. Foundation subsequently graduated Org by dated
owner-authorized amendment on 2026-07-15 after the company-aggregate producer
schema landed. This contract still binds the semantic boundary that physical
records must preserve; the graduation adds no matcher, registry, or canonical
identity resolver.

## Why This Boundary Exists

The word "company" is too ambiguous to serve as an identity model. A source may
name a parent organization, a subsidiary, a consumer brand, a social account,
or a product line. Treating the surface form as a canonical company identifier
would create false joins; treating every surface form as unrelated would make a
company's observable history impossible to reconstruct.

Company Surface therefore separates three things:

1. **Observed identifier** - what an upstream source actually supplied, with
   its source receipt and capture limitations intact.
2. **Subject assertion** - the evidence-backed claim that an identifier refers
   to one Brand or Org subject.
3. **Relationship assertion** - the evidence-backed claim that two subjects
   were related in a stated way for a stated period.

Neither kind of assertion changes the upstream evidence. A later correction
supersedes an assertion; it does not rewrite what the source said.

## Subject And Relationship Semantics

### Subject kinds

| Kind | Meaning in Company Surface | Must not be treated as |
| --- | --- | --- |
| Brand | A market-facing identity under which products, services, or observable activity are presented. | Automatically identical to its owner, parent, legal entity, product, or social account. |
| Org | An operating or legal organization that may own brands or sit in an organization hierarchy. | Automatically identical to every brand it owns or every subsidiary it controls. |

"Company" remains the human query term. It is not a third universal entity type.
A query must identify its anchor subject and may then include related subjects
whose relationship assertions are valid for the requested period.

### Relationship kinds

- Brand owned_by Org expresses ownership without merging the Brand into the
  Org.
- Org subsidiary_of Org expresses organization hierarchy without merging the
  subsidiary into the parent.
- A relationship is valid only for its supported effective interval. Unknown
  starts, unknown ends, and coarse time precision remain explicit.
- A current roll-up may follow only relationships valid at the requested current
  boundary. A historical roll-up uses the relationships valid during the
  requested historical interval.

This contract does not invent additional relationship vocabulary. A later need
for licensing, distribution, minority investment, joint venture, or another
relationship returns to Foundation ontology governance rather than overloading
owned_by or subsidiary_of.

## Assertion States And Evidence

Every subject or relationship assertion has one of four semantic states:

| State | Meaning |
| --- | --- |
| resolved | The cited evidence supports one subject or relationship under the declared scope and time precision, with no material competing candidate left open. |
| provisional | One interpretation is currently best supported, but a named evidence gap or material limitation prevents resolution. |
| ambiguous | Two or more material candidates remain plausible. |
| unresolved | Available evidence is insufficient to select a material candidate. |

The state is itself an inspectable claim, not a confidence score. A usable
assertion preserves enough meaning to recover:

- the raw identifier or subjects being related;
- the asserted subject kind or relationship kind;
- the supporting and conflicting source receipts;
- the observation, effective, and recorded-time distinctions that matter;
- the time precision and any unknown boundary;
- the current assertion state and stated limitation; and
- any assertion it supersedes or corrects.

The exact field names, identifier format, confidence method, and storage model
remain deferred. No downstream consumer may reinterpret absence of evidence as
a resolved negative or upgrade a provisional match merely because a roll-up is
convenient.

## Ownership Boundary

| Layer | Owns | Does not own |
| --- | --- | --- |
| Foundation ontology | Shared subject and relationship vocabulary. | Company-specific matches or relationship truth. |
| Capture | Raw identifiers, observations, source receipts, capture time, and visible failures. | Canonical company identity or cross-source equivalence. |
| Cleaning | Later normalization or candidate suggestions when separately authorized. | The durable meaning of a Company Surface subject or silent canonical merges. |
| Company Surface | Company-specific subject assertions, relationship assertions, their uncertainty, and their history. | Source acquisition, physical storage, operational conclusions, or intervention choice. |
| Data Lake | Physical persistence of captured and derived records. | Canonical identity meaning or cross-packet identity decisions. |
| CSB, analysis, GTM, and interventions | Time-bounded views and conclusions drawn from the accepted evidence. | Rewriting Company Surface identity history to fit a conclusion. |

## History And Correction Rules

1. New evidence appends a new assertion or supersedes a prior assertion; it
   does not erase the prior claim or its evidence.
2. Event time, relationship-effective time, capture time, and assertion-recorded
   time remain distinguishable whenever their difference affects meaning.
3. A relationship ending removes it from later current views but preserves it
   in historical views.
4. A subject correction redirects later resolution without changing the raw
   identifier preserved by Capture.
5. Conflicting evidence fails visible as provisional, ambiguous, or unresolved.
   No default "best guess" may masquerade as resolution.
6. A roll-up must be reproducible from the subject and relationship assertions
   valid for its stated period.

## Dogfood: e.l.f. Beauty

This is a worked semantic test, not a stored company dossier and not proof of
runtime readiness. The bounded sources are e.l.f. Beauty's fiscal-2026 Form
10-K filed with the SEC and its current corporate brands page, both read on
2026-07-15.

The Form 10-K identifies e.l.f. Beauty, Inc. as the registrant and describes it
as a multi-brand beauty company. It names the current portfolio as e.l.f.
Cosmetics, e.l.f. SKIN, rhode, Naturium, and Well People. The current corporate
brands page independently presents those same five market-facing brands.

The same filing also names the operating organizations behind those brands.
e.l.f. Beauty operates through its principal subsidiaries e.l.f. Cosmetics,
Inc. (doing business as "e.l.f. Cosmetics", "e.l.f.", and "e.l.f. SKIN"),
HRBeauty LLC (doing business as "rhode"), Naturium LLC (doing business as
"Naturium"), and Well People, Inc. (doing business as "Well People").

The contract therefore represents that evidence as five Brand subjects and
five Org subjects — the registrant plus four named operating organizations —
not as five brands hanging directly off the registrant. The filing supports
subject distinction and operating-name association; it does not by itself
prove every Brand `owned_by` edge. Any later ownership assertion must carry
relationship-specific evidence and remain provisional where that evidence does
not pin the relationship or tier.

- Brand and Org stay distinct even at the same name. "Naturium" the Brand and
  Naturium LLC the Org are different subjects, as are "Well People" and Well
  People, Inc., and "e.l.f. Cosmetics" and e.l.f. Cosmetics, Inc. The reverse
  case also appears: the Brand "rhode" and its Org HRBeauty LLC share no name,
  so neither a shared name nor a distinct one decides subject identity.
- Operating-name association is not one-to-one. One Org, e.l.f. Cosmetics,
  Inc., conducts business under two of the five brands, so a consumer may not
  infer subject identity or ownership from names alone.
- Ownership is layered. The filing states that on 2025-08-05 rhode became a
  wholly owned subsidiary of e.l.f. Cosmetics, Inc., and that Naturium was
  acquired through that same wholly owned subsidiary. Those are Org
  subsidiary_of Org assertions beneath the registrant, not direct Brand
  `owned_by` claims. The filing calls all four organizations principal
  subsidiaries through which e.l.f. Beauty operates without pinning every
  intermediate tier; an unpinned tier stays provisional rather than being
  flattened into the registrant.

Two history cases exercise the boundary:

- The Form 10-K says the rhode acquisition was completed on 2025-08-05. A
  historical view before that effective date must not treat rhode as owned by
  e.l.f. Beauty; a later view may, subject to the cited assertion.
- The Form 10-K says Keys Soulcare was transferred to Alicia Keys in May 2026
  and is no longer in the portfolio. Company Surface must preserve the prior
  portfolio relationship and end it at month precision. The filing does not
  establish the exact transfer day, so that boundary remains unknown rather
  than being fabricated. The brands page places "Keys Soulcare is born" in its
  2020 timeline. That supports a year-precision public portfolio/origination
  marker, not an exact legal relationship start or day. Company Surface may
  preserve 2020 as coarse supporting evidence while leaving the precise
  effective boundary and relationship kind unresolved.

Sources:

- [e.l.f. Beauty fiscal-2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1600033/000160003326000020/elf-20260331.htm)
- [e.l.f. Beauty current brands page](https://www.elfbeauty.com/brands)

### Dogfood result

The boundary passes this case only if a consumer can produce a current e.l.f.
Beauty portfolio view, reconstruct rhode's entry and Keys Soulcare's exit for
historical views, keep the same-name Brand and Org subjects distinct, inspect
the sources, and see the unresolved time boundaries without collapsing Brand
into Org or inventing precision.

## Acceptance Conditions

This boundary is complete when a downstream record or implementation design can
satisfy all of the following without inventing product intent:

1. Same-name Brand and Org subjects can remain distinct.
2. One raw identifier can remain ambiguous between multiple candidate subjects.
3. A resolved link is inspectable and can be superseded without source rewrite.
4. Ownership and subsidiary relationships are time-bounded assertions, not
   identity equivalence.
5. Current and historical company views can disagree correctly because their
   requested periods differ.
6. Unknown relationship boundaries and conflicting identity evidence stay
   visible.
7. Capture and Data Lake can participate without becoming identity authorities.
8. The e.l.f. Beauty case can be represented with the stated facts and residual
   unknowns, with no separate maintained dossier.

## Non-Goals And Deferred Decisions

This contract does not establish:

- a Company Surface record schema, canonical identifier format, registry, or
  stored corpus;
- an entity-matching algorithm, confidence threshold, deduplication service, or
  human review workflow;
- Org ontology graduation or new ontology relationships;
- current-view materialization, storage layout, API, runtime, scheduler, or UI;
- source-specific capture routes or source-coverage completeness;
- beneficial-ownership, legal-control, or corporate-family truth beyond the
  relationship claim a cited source supports; or
- analysis conclusions, pain scores, GTM authorization, outreach, or
  intervention choice.

The companion `company_logical_record_and_view_contract_v0.md` implements this
boundary and the owner-signed purpose. Foundation subsequently graduated Org
by dated owner-authorized amendment, and
`company_surface_silver_mapping_contract_v0.md` now controls the first physical
mapping into Data Lake records. Neither later decision adds a matcher,
registry, canonical identity resolver, or unsupported relationship fact.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Company Surface now owns inspectable, historical company-specific subject
    and relationship assertions while Foundation owns vocabulary, Capture owns
    raw identifiers and receipts, and Data Lake owns physical persistence.
  trigger: product_doctrine
  related_authority: architecture_doctrine
  controlling_sources_updated:
    - forseti/product/information/company_surface/company_identity_boundary_v0.md
    - docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md
    - forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md
  downstream_surfaces_checked:
    - forseti/product/information/company_surface/purpose_contract_v0.md
    - forseti/product/information/company_surface/README.md
    - forseti/product/information/README.md
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
    - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
    - forseti/product/spines/foundation/ontology/ontology.yaml
    - forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: Foundation ontology
      reason: This semantic contract uses the existing vocabulary but does not satisfy or replace the owning Org-graduation gate.
    - path: Capture and Cleaning contracts or runtime
      reason: Their raw-evidence and possible candidate-normalization roles remain unchanged; no matching implementation is authorized.
    - path: Data Lake contracts or runtime
      reason: Physical persistence remains unchanged and the Lake already disclaims canonical identity ownership.
    - path: docs/decisions/forseti_spine_first_target_structure_binding_v0.md and docs/workflows/forseti_repo_map_v0.md
      reason: Company Surface placement and its T1 front-door route remain accurate; a per-contract inventory row is not required.
    - path: stored company data or a dogfood corpus
      reason: The e.l.f. Beauty example tests semantics inline and authorizes no stored dossier, capture, or readiness claim.
  stale_language_search: >
    rg -n -i "[c]ompany.identity boundary.*deferred|[e]ntity.resolution spine"
    forseti/product/information/company_surface
    docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md
    forseti/product/spines/capture/core/contracts
  stale_language_search_result: >
    Run on the adjudicated worktree (2026-07-15). No hits remain across the
    Company Surface contract, the company-aggregate decision, or Capture core
    contracts. The wider scan closes the stale `entity_key` owner name that the
    earlier two-path scan did not detect.
  non_claims:
    - not a schema, canonical identifier, registry, or runtime
    - not Org ontology graduation
    - not validation, readiness, or source-completeness proof
    - not buyer proof, GTM, outreach, or intervention authorization
```
