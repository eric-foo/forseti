---
case_id: unity_runtime_fee_2023_v0_14
decision_question: Should Unity proceed with a broad runtime/install-based fee model, narrow or phase the change, grandfather existing users, change messaging, or hold pending further evidence?
decision_date_or_cutoff: "2023-09-11 23:59 Pacific Time"
role_frame: executive or senior monetization/package decision owner accountable for product packaging, developer trust, revenue, customer retention, and launch risk
authority_constraints: >
  Assume responsibility for recommending a monetization and packaging path. Do not assume authority to override legal, contract, finance, engineering, customer-success, platform, or board constraints unless the packet evidence supports it.
capability_constraints: >
  Treat customer-level exposure, contract rights, metering reliability, billing operations, dispute handling, support readiness, communication readiness, and segment-level economics as unknown unless shown in the packet.
permitted_assumptions:
  - Public pre-cutoff company filings can be used to frame business model, revenue pressure, customer risk, and competitive context.
  - Archive visibility checks can be used only to mark source visibility limits when they do not establish substantive facts.
  - Competitor licensing context may be considered when assessing market expectations and perceived customer economics.
forbidden_information_notice: >
  Use only information available at or before the cutoff. Do not use later public events, later company actions, later policy changes, later internal judgments, hidden labels, or non-packet evaluation material.
source_manifest:
  - source_id: S-01
    source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/0001810806-23-000016-index.htm
    retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
    hash: TBD_SOURCE_BYTE_HASH
  - source_id: S-03
    source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
    retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
    hash: TBD_SOURCE_BYTE_HASH
  - source_id: S-04
    source: https://web.archive.org/cdx?url=unity.com/products/compare-plans&from=20230901&to=20230911&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest
    retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
    hash: TBD_SOURCE_BYTE_HASH
  - source_id: S-05
    source: https://web.archive.org/cdx?url=unity.com/products/*pricing*&from=20230101&to=20230911&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest&limit=20
    retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
    hash: TBD_SOURCE_BYTE_HASH
  - source_id: S-06
    source: https://web.archive.org/cdx?url=unrealengine.com/en-US/license&from=20230101&to=20230911&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest&limit=5
    retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
    hash: TBD_SOURCE_BYTE_HASH
  - source_id: S-07
    source: https://web.archive.org/web/20230103153058/https://www.unrealengine.com/en-US/license
    retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
    hash: TBD_SOURCE_BYTE_HASH
---

# Unity Runtime Fee Participant Packet Draft v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Packet-safe draft participant packet for the Unity Runtime Fee v0.14 fixture.
use_when:
  - Reviewing the participant-facing draft before any blind contestant use.
  - Checking packet-safe Unity pre-cutoff facts and uncertainties.
  - Preparing a later clean participant packet only after missing hashes and timestamps are resolved.
authority_boundary: retrieval_only
input_hashes:
  fixture_authoring_prompt: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
  extraction_plan: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  source_packet: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  pydantic_schema_reference: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  case_construction_protocol: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
  post_authoring_review: BB1EAD239DF2A1EE5704B888BD5F1F261B0E2DD2D656E5FCB4330708A19C674C
```

- Status: PARTICIPANT_PACKET_DRAFT_ONLY
- Case ID: `unity_runtime_fee_2023_v0_14`
- Fixture status: draft, not for blind use
- Packet source boundary: pre-cutoff source packet only
- Participant-packet hash: not computed

## Decision Frame

Unity is considering whether and how to change its monetization model for use of Unity technology in games and interactive content.

The decision is not whether monetization pressure exists in general. The decision is which action is justified at the cutoff given visible business pressure, customer and ecosystem risk, missing segment economics, and operational uncertainty.

## Role Frame

Act as an executive or senior monetization/package decision owner accountable for product packaging, developer trust, revenue, customer retention, and launch risk.

Your task is to recommend a bounded decision path at the cutoff. The available choices may include holding, watching defined signals, narrowing the scope, testing a reversible change, creating option value, phasing a rollout, escalating for authority or context, moving on a material but controlled path, or committing to a high-conviction path.

## Authority Constraints

- Do not assume unilateral authority over legal terms, customer contracts, enterprise exceptions, finance targets, platform operations, billing infrastructure, or support readiness.
- Treat authority for broad customer-facing changes as requiring evidence of legal, operational, commercial, and communication readiness.
- Treat narrower tests or customer-readback steps as potentially available only if the packet evidence supports their scope.

## Capability Constraints

- Customer-level exposure is not established.
- Contract rights, notice obligations, and amendment limits are not established.
- Metering, billing, fraud handling, dispute handling, support readiness, and communication readiness are not established.
- Segment-level elasticity, willingness to pay, and switching behavior are not established.
- Exact pre-cutoff Unity pricing, package thresholds, and public terms were not established in this packet.

## Evidence Summaries

### EU-01 - Distinct Create And Grow Surfaces

Unity publicly described its platform as combining Create Solutions and Grow Solutions: tools for creating, running, and monetizing interactive content, alongside user acquisition, engagement, and monetization services.

Decision relevance: a runtime/install-based model would sit near the boundary between creation tooling, runtime or distribution use, and monetization economics.

Limits: this does not identify any planned pricing change, expected fee structure, private rationale, or customer willingness.

### EU-02 - Visible Financial Pressure

Unity reported 2022 revenue of about $1.39 billion, a 25% year-over-year increase, while also reporting a substantial net loss and operating expenses above annual revenue.

Decision relevance: monetization expansion pressure was visible before the cutoff.

Limits: this does not prove cash need, board pressure, target revenue, acceptable mechanism, or timing.

### EU-03 - Revenue Depended On Create And Grow

Unity disclosed material revenue from both Create Solutions and Grow Solutions in 2022. Grow was tied to advertising, user acquisition, and monetization services; Create was tied to subscriptions and platform services.

Decision relevance: a broad runtime/install-based model could affect expectations around Create while attempting to capture monetization value not covered by traditional subscriptions.

Limits: this does not show revenue by cohort, game size, install count, platform, plan, or developer economics.

### EU-04 - High-Value Customers Were Material

Unity disclosed a large number of customers contributing more than $100,000 of trailing-12-month revenue and described these high-value customers as contributing a substantial majority of revenue.

Decision relevance: segmentation and enterprise exposure are relevant.

Limits: this does not prove which customers would face a runtime/install fee, how contracts constrain changes, or how much revenue is exposed to churn.

### EU-05 - Renewal, Retention, And Confidence Risks Were Disclosed

Unity identified risks around customer expansion, renewal, account loss, reductions in use, customers developing in-house alternatives, and customer confidence in Unity monetization products.

Decision relevance: customer trust, retention, and substitution risk were known risk categories before the cutoff.

Limits: this does not quantify churn probability, elasticity, switching cost, or the effect of a specific pricing mechanism.

### EU-06 - Price And Customer Economics Were Competitive Factors

Unity described competition from alternative platforms, in-house tools, and other providers, and listed factors including features, functionality, price, and customer economics.

Decision relevance: any broad fee should be judged by total perceived developer economics versus alternatives.

Limits: this does not establish competitor adoption likelihood, buyer switching thresholds, or an acceptable communication package.

### EU-07 - Alternative Engine Licensing Context

A major alternative engine publicly presented a different licensing frame in an archived official page dated before the cutoff.

Decision relevance: public alternatives could shape developer expectations around engine pricing and monetization mechanics.

Limits: this is contextual only. It does not prove exact operative terms, Unity customer behavior, Unity pricing feasibility, or legal risk.

## Known Uncertainties And Source Gaps

- Private revenue model and target economics for any runtime/install-based model.
- Internal customer data, cohort economics, plan mix, and usage/install distribution.
- Enterprise contract constraints, amendment rights, notice obligations, and grandfathering cost.
- Developer churn, switching, substitution, and in-house engine data.
- Exact elasticity and willingness to pay by customer segment.
- Exact Unity pre-cutoff public pricing, package thresholds, and legal terms. Bounded archive checks did not establish usable pre-cutoff visibility for the attempted Unity pricing and compare-plan URL variants, but that failed visibility check is not affirmative evidence; do not infer that no pre-cutoff pricing or terms evidence existed.
- Legal and terms risk, including enforceability and measurement disputes.
- Launch readiness, metering reliability, dispute handling, support readiness, and billing operations.
- Buyer willingness to accept packaging changes.
- Communications readiness and trust impact.
- Platform-holder, publisher, and downstream customer constraints.
- Pre-cutoff developer, community, or customer signal specific to install-based engine monetization.

## Permitted Assumptions

- Public financial-pressure evidence may be considered when assessing monetization options, timing, and evidence needed before action.
- Segmentation may matter because high-value customers are material, but exact segment exposure is unknown.
- Customer confidence, renewal, account-loss, reduced-use, and substitution risks are decision-relevant because Unity disclosed them as risk categories.
- Competitor licensing context may be considered when assessing market expectations and perceived customer economics.

## Draft Use Boundary

This packet draft is not ready for blind contestant use. It lacks normalized source timestamps, per-source hashes, a participant packet hash, and completed contamination checks. It is a docs-only draft for review and patching before any later clean packet is bound for contestant use.
