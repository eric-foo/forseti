# Company Surface -> Silver Architecture Planning Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Source-backed adversarial review and Chief Architect adjudication of the
  couriered Company Surface to Silver architecture planning result.
use_when:
  - Authoring the Company Surface logical record and history/current-view contract.
  - Checking which Silver, identity, S5, or temporary-pool claims survived review.
authority_boundary: retrieval_only
input_hashes:
  external_attachment_pasted_text_txt: 8A62614B82C970F8AB188DF57C18342B5F676528B2351E0BB70008930051172C
branch_or_commit: origin/main @ 55af05592c195 plus Beauty GTM @ eb0a4e0ba1b0
stale_if:
  - Company Surface purpose, identity, Silver, Corpus Intake, ontology, or Beauty GTM authority changes.
```

```yaml
review_summary:
  status: completed
  review_location: this_file
  recommendation: patch_before_acceptance
  reviewed_by: unrecorded
  authored_by: unrecorded
  summary: >
    Accept the hybrid direction, but not the architecture result as written:
    seven material claims overstate Silver gates, assume producers that do not
    yet exist, or assign authority to the wrong layer.
  findings_count: 8
  blocking_findings: []
  advisory_findings:
    - CSAR-01: The mandatory Silver vocabulary amendment is not established.
    - CSAR-02: The result treats unbuilt source-family Silver producers as existing.
    - CSAR-03: Identifier-to-subject assertion endpoints are not yet modeled.
    - CSAR-04: Canonical company-subject identifiers are assigned to the wrong owner.
    - CSAR-05: A multi-packet anchor amendment is asserted before an anchor rule is tested.
    - CSAR-06: The S5 protection is sound, but its proposed Silver field is not yet required.
    - CSAR-07: The temporary-pool storage and eight-company limits are overstated.
    - CSAR-08: The result hides the decision under avoidable architecture jargon.
  prior_findings_remediated: []
  next_action: >
    Author the Company Surface logical record and history/current-view contract,
    preserving the accepted hybrid direction while resolving the record shapes,
    identifier owner, anchor choice, and Org gate without presuming a Silver amendment.
```

## Commission And Boundary

- Commission: adversarially review the couriered Company Surface -> Silver
  architecture planning result, adjudicate its claims, and explain the result
  plainly.
- Reviewed target: external attachment `pasted-text.txt`, 233 lines,
  SHA-256 `8A62614B82C970F8AB188DF57C18342B5F676528B2351E0BB70008930051172C`.
- Purpose: determine which parts of the proposed architecture are safe to carry
  into the next Company Surface contract.
- Output mode: durable report plus chat explanation. The review is read-only
  with respect to the reviewed target and all product/architecture sources.
- Excluded: implementation, schemas, runtime, ontology graduation, Silver
  amendment, GTM execution, pool construction, and patching the couriered text.
- Review-use boundary: review findings are decision input only; they are not
  approval, validation, mandatory remediation, or patch authority.

## Source Preflight And Ledger

The source hierarchy was Forseti `AGENTS.md`, the Forseti workflow overlay, then
accepted Forseti product and architecture sources. The installed review skills
supplied mechanics only. Deep-thinking discipline ran before source preflight.

The base workspace was detached and contained unrelated untracked directories.
No authority claim relied on that dirty state. Product sources were read from
`origin/main` at `55af05592c19523f1f2f494e88119f9a744cbc79`; the Company Surface
merge `309061bc53e2491c7fee7918562bb6c42875b6e2` was confirmed in its ancestry.
The active Beauty GTM contract was read from exact Git object
`eb0a4e0ba1b0fa45b233f0a3753f08b276fb655a`, because it is not on `origin/main`.

| Source | Authority used |
| --- | --- |
| `forseti/product/information/company_surface/purpose_contract_v0.md` | Company Surface purpose, ownership, non-goals, deferred mechanics |
| `forseti/product/information/company_surface/company_identity_boundary_v0.md` | identity ownership, uncertainty, history, next unresolved contract |
| `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` | Silver envelope, record kinds, producer ownership, relationships, generated views, residual producer gaps |
| `forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` | standing-capture substrate and Decision-Frame rebind gate |
| `forseti/product/spines/capture/core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md` | raw-handle-keyed source-family payload boundary |
| `forseti/product/spines/foundation/ontology/ontology.yaml` | Brand adopted; Org and its dependent edges reserved |
| `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md` | dated graduation rule for Org |
| Beauty GTM contract at `eb0a4e0b` | temporary pool, serial company research, stop-by-eight boundary |

The courier's stale Silver pointer warning is correct. Its source-loading report
was treated as orientation, not proof. No implementation or validation gate ran.

## Phase 1 - Correctness Findings

### CSAR-01 - The mandatory Silver vocabulary amendment is not established

- Confidence: high.
- Anchor: `Human Summary`, `Silver Conformance Matrix`, and `Ontology Gate`.
- Evidence: the Silver contract closes only `record_kind` to entity,
  relationship, and observation. `payload_kind` is shown with an ellipsis;
  lane namespaces are producer-owned; relationship edge types are explicitly a
  *minimum* list. The campaign clause requires a future source-captured object
  contract, not necessarily an amendment to the central Silver contract.
- Strongest defense: a central amendment would prevent an unreviewed producer
  from inventing semantics. That caution is valid, but the current source does
  not turn it into the mandatory upstream gate claimed by the courier.
- Impact: the result creates a false dependency and sends the next decision to
  the Data Lake owner before the Company Surface record contract has even
  defined its payloads.
- Minimum closure condition: treat Silver amendment need as an open conformance
  question. Define the Company Surface producer payloads first, then amend the
  Silver authority only if its owner confirms the generic envelope cannot admit
  them without a core change.
- Next authorized action: carry the question into the logical record contract;
  do not commission a Silver amendment yet.
- Patch queue: not authorized. Strict readiness and conformance remain not proven.

### CSAR-02 - The result treats unbuilt source-family Silver producers as existing

- Confidence: high.
- Anchor: target diagram and the repeated phrase `existing source-family producer lanes`.
- Evidence: the Silver contract's accepted residual says its generic schema
  spans review, retail, and SEO without committing per-domain producers, and
  that each domain still needs a producer lane and per-lane record contract.
  The tenant payload boundary describes raw capture envelopes and projections,
  not authoritative Silver producers.
- Strongest defense: the diagram can be read as a target-state abstraction.
  That defense fails because the prose repeatedly says the lanes exist "as
  today" and uses them as a cold-company prerequisite.
- Impact: implementers could assume captured company evidence is already
  available as Silver entities and links when much of it may still exist only
  in Bronze/raw or non-authoritative projection form.
- Minimum closure condition: distinguish landed Silver producers from future
  producer contracts and state what the first Company Surface slice does when a
  needed source family has no Silver producer.
- Next authorized action: make this dependency explicit in the logical record
  contract and first proving-slice plan.
- Patch queue: not authorized. Producer availability remains not proven.

### CSAR-03 - Identifier-to-subject assertion endpoints are not yet modeled

- Confidence: high.
- Anchor: the proposed `subject attribution assertion` relationship record.
- Evidence: Capture owns the observed raw identifier. Silver relationship
  records connect entities or records; the example endpoints are entity keys.
  The courier proposes a raw identifier -> Brand/Org relationship without
  deciding whether the raw identifier is an entity, a record reference, or
  evidence attached to another assertion shape.
- Strongest defense: an existing platform account or listing entity could be
  the left endpoint. That works only for source families with a landed Silver
  entity producer and does not solve identifiers that exist only in raw capture.
- Impact: the advertised three-record-family design can deadlock the first cold
  company or force premature source-family Silver implementation.
- Minimum closure condition: the logical record contract must choose a lawful,
  inspectable representation for observed-identifier-to-subject assertions and
  pressure-test it against the e.l.f. case plus one raw-only identifier.
- Next authorized action: preserve the record family as a candidate, not a
  settled Silver relationship shape.
- Patch queue: not authorized. Exact record shape remains not proven.

### CSAR-04 - Canonical company-subject identifiers are assigned to the wrong owner

- Confidence: high.
- Anchor: `Exact preceding decisions` under the ontology gate.
- Evidence: the identity contract makes Company Surface the owner of
  company-specific identity meaning and explicitly defers the canonical
  identifier format to its next record decision. Capture carries an externally
  resolved key and never mints it. Data Lake owns physical persistence and does
  not own cross-packet identity decisions.
- Strongest defense: Data Lake must enforce a serializable `entity_key` shape.
  That is envelope conformance, not authority to decide what company subject
  the key denotes or how its identity lifecycle works.
- Impact: routing the identifier decision to Data Lake would leak semantic
  authority into storage and could produce a technically tidy but wrong global
  company ID.
- Minimum closure condition: Company Surface owns the subject-key semantics and
  identifier lifecycle, constrained by Foundation namespaces and Silver
  serialization requirements.
- Next authorized action: decide it inside the logical record contract, with
  Data Lake consulted only for storage conformance.
- Patch queue: not authorized. Canonical format remains deferred.

### CSAR-05 - A multi-packet anchor amendment is asserted before an anchor rule is tested

- Confidence: medium.
- Anchor: the proposed `multi-packet anchor rule` precondition.
- Evidence: Silver requires a packet-or-narrower raw anchor and separately
  permits multiple `raw_refs`. The contract does not state that a record citing
  several packets needs a broader physical anchor.
- Strongest defense: choosing one packet as the physical anchor could be
  arbitrary and make retrieval surprising. That is a real design issue, but it
  first calls for a deterministic primary-anchor rule, not automatically a core
  grammar amendment.
- Impact: the courier turns a solvable record-design choice into a mandatory
  upstream architecture change.
- Minimum closure condition: define and test a deterministic primary anchor
  against a multi-source identity assertion; escalate to a Silver amendment
  only if that cannot preserve findability and lineage.
- Next authorized action: resolve in the record contract or its dogfood case.
- Patch queue: not authorized. Need for a core amendment remains not proven.

### CSAR-06 - The S5 protection is sound, but its proposed Silver field is not yet required

- Confidence: medium.
- Anchor: `substrate provenance class` invariant and S5 flow language.
- Evidence: Corpus Intake says standing rows remain substrate until a
  Decision-Frame recapture/rebind re-discharges commissioned obligations and
  preserves an auditable corpus-to-evidence link. It does not require every
  reusable Silver identity assertion to carry a new `provenance_class` field.
- Strongest defense: an explicit marker is a strong way to prevent laundering.
  That remains a good candidate, but the gate attaches to decision use, not to
  whether a company identity assertion may exist or be `resolved`.
- Impact: the result risks conflating "resolved identity" with "decision-ready
  evidence" and prematurely freezes one field-level implementation.
- Minimum closure condition: preserve source lineage so consumers can enforce
  S5 at Decision-Frame assembly; decide in the logical record contract whether
  an explicit substrate marker is necessary in addition to those refs.
- Next authorized action: retain the anti-laundering invariant, defer the exact field.
- Patch queue: not authorized. Field necessity remains not proven.

### CSAR-07 - The temporary-pool storage and eight-company limits are overstated

- Confidence: high.
- Anchor: `The 20-company pool never touches any of this`, `must never be
  lake-persisted`, and `at most eight companies ever`.
- Evidence: the Beauty GTM contract calls the pool run-local research
  scaffolding rather than a CRM, registry, lead list, ICP, or monitor. It says
  the current run stops by eight deep investigations. It does not establish a
  universal physical-storage prohibition or cap Company Surface forever at
  eight companies.
- Strongest defense: refusing to mint authoritative company records from pool
  membership prevents registry creep. That defense supports a narrower rule,
  not the courier's absolutes.
- Impact: later agents could discard legitimate run artifacts or mistake a
  one-run research cap for a permanent Company Surface corpus limit.
- Minimum closure condition: pool membership alone creates no Company Surface
  or Silver authority. Captured evidence from selected company cycles may enter
  the normal flow. The eight-company cap applies only to this Beauty GTM run.
- Next authorized action: use the narrower boundary in the next contract.
- Patch queue: not authorized. No storage implementation is authorized.

## Phase 2 - Friction Finding

### CSAR-08 - The result hides the owner decision under avoidable jargon

- Confidence: high.
- Anchor: the full artifact, especially the matrix and fourteen invariants.
- Evidence: the core decision is one paragraph, but it is surrounded by several
  near-duplicate gate lists, record matrices, and terms such as "substrate
  provenance class", "ontology-governed payload", and "derived grammar" before
  the basic flow is made plain.
- Strongest defense: the detail preserves downstream implementation constraints.
  That belongs in the next logical record contract. An architecture decision
  should expose the choice and the real blockers first.
- Impact: the owner can accept the right diagram while missing that several
  alleged preconditions are unsupported.
- Minimum closure condition: state the accepted direction, actual blockers, and
  next artifact in plain language; keep detailed field choices deferred.
- Next authorized action: use the plain adjudication below as the controlling
  chat interpretation of this review.
- Patch queue: not authorized.

## Considered And Defended

- Hybrid placement survived: keeping Company Surface assertions in Silver and
  making current/history roll-ups rebuildable views best fits the accepted
  ownership split without creating a second store.
- Separate Company Surface store was correctly rejected: Data Lake owns physical
  persistence, and a new store would duplicate truth and lifecycle.
- Generated-view-only was correctly rejected: generated views cannot be the
  durable authority for identity assertions that must be corrected and replayed.
- Org gating survived: Brand is adopted; Org and its dependent ownership edges
  remain reserved until a dated Foundation amendment.
- The proposed next artifact survived: the identity contract explicitly names
  the logical record and history/current-view contract as the next unresolved
  Company Surface content decision.

## Chief Architect Adjudication

Accept the architectural direction, but reject the couriered result as a source
to follow verbatim.

The corrected decision is:

1. Capture stores source evidence in the Data Lake under its existing rules.
2. Source-specific facts stay owned by their source-family contracts; do not
   copy them into a company dossier.
3. Company Surface should add only the durable company identity and relationship
   meaning needed to connect that evidence over time.
4. Those durable derived records should target Silver; current and historical
   company pictures should be rebuildable, non-authoritative views.
5. The next Company Surface logical record contract must decide the exact record
   shapes, identifier lifecycle, raw-only identifier handling, anchor choice,
   history/view behavior, and S5 lineage guard.
6. Do not presume a core Silver amendment. Ask for one only if the completed
   producer contract cannot conform to the generic Silver envelope.
7. Org records and `owned_by` / `subsidiary_of` edges remain blocked until the
   explicit Foundation graduation. Brand work may be designed now, but producer
   implementation remains separately unauthorized.
8. The 20-company pool does not mint company authority. Only captured evidence
   from selected research cycles may enter the Company Surface flow, and the
   eight-company limit belongs to this GTM run only.

Seven correctness findings are accepted as net-new material decision changes.
The friction finding is accepted as presentation guidance. The review is closed
by this adjudication because the target is a couriered planning result rather
than a source artifact that requires patching. The next authorized material move
is the already-named logical record and history/current-view contract; no
implementation, Silver amendment, Org graduation, or GTM execution is authorized.
