# Unity Runtime Fee Evidence Registry Draft v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Draft v0.14 EvidenceUnit registry mapping for the Unity Runtime Fee fixture.
use_when:
  - Reviewing how Unity EU-01 through EU-08 map toward v0.14 EvidenceUnit fields.
  - Finding missing source hashes, retrieval timestamps, and adapter decisions before scoring.
  - Checking that the source packet hash is not being substituted for per-source hashes.
authority_boundary: retrieval_only
input_hashes:
  fixture_authoring_prompt: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
  extraction_plan: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  source_packet: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  pydantic_schema_reference: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  case_construction_protocol: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
  post_authoring_review: BB1EAD239DF2A1EE5704B888BD5F1F261B0E2DD2D656E5FCB4330708A19C674C
open_next:
  - docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
```

- Status: EVIDENCE_REGISTRY_DRAFT_ONLY
- Case ID: `unity_runtime_fee_2023_v0_14`
- Fixture status: blocked before scoring
- Registry freeze status: not frozen
- Source packet hash use: provenance only; does not replace per-source hashes

## v0.14 EvidenceUnit Field Contract

```yaml
evidence_unit_required_fields:
  evidence_id:
  source_id:
  source:
  timestamp:
  retrieval_timestamp:
  hash:
  pre_decision_status:
  pre_decision_basis:
  summary:
```

`hash` must be `sha256(source_bytes)` when source bytes are available. The Unity source packet hash is useful provenance, but it is not a substitute for source-byte hashes for S-01 if retained as a participant source-manifest locator, S-03, S-04, S-05, S-06, S-07, or any other retained source.

## Draft Evidence Units

### EU-01

```yaml
evidence_id: EU-01
source_id: S-03
source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
timestamp: TBD_EXACT_SOURCE_TIMESTAMP_NOT_NORMALIZED
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet.
summary: Unity publicly described its platform as combining Create Solutions and Grow Solutions, including tools for creating, running, and monetizing interactive content, user acquisition, engagement, and monetization services.
missing_or_unsafe_fields:
  - exact publication or filing timestamp must be normalized
  - retrieval timestamp must be recovered or marked unavailable
  - source-byte hash must be computed from canonical source bytes
```

### EU-02

```yaml
evidence_id: EU-02
source_id: S-03
source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
timestamp: TBD_EXACT_SOURCE_TIMESTAMP_NOT_NORMALIZED
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet.
summary: Unity reported about $1.39 billion in 2022 revenue, 25% year-over-year revenue growth, a substantial net loss, and operating expenses exceeding annual revenue.
missing_or_unsafe_fields:
  - exact publication or filing timestamp must be normalized
  - retrieval timestamp must be recovered or marked unavailable
  - source-byte hash must be computed from canonical source bytes
```

### EU-03

```yaml
evidence_id: EU-03
source_id: S-03
source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
timestamp: TBD_EXACT_SOURCE_TIMESTAMP_NOT_NORMALIZED
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet.
summary: Unity disclosed material revenue from both Create Solutions and Grow Solutions, with Grow tied to advertising, user acquisition, and monetization services and Create tied to subscriptions and platform services.
missing_or_unsafe_fields:
  - exact publication or filing timestamp must be normalized
  - retrieval timestamp must be recovered or marked unavailable
  - source-byte hash must be computed from canonical source bytes
```

### EU-04

```yaml
evidence_id: EU-04
source_id: S-03
source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
timestamp: TBD_EXACT_SOURCE_TIMESTAMP_NOT_NORMALIZED
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet.
summary: Unity disclosed a large number of customers contributing more than $100,000 of trailing-12-month revenue and described high-value customers as contributing a substantial majority of revenue.
missing_or_unsafe_fields:
  - exact publication or filing timestamp must be normalized
  - retrieval timestamp must be recovered or marked unavailable
  - source-byte hash must be computed from canonical source bytes
```

### EU-05

```yaml
evidence_id: EU-05
source_id: S-03
source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
timestamp: TBD_EXACT_SOURCE_TIMESTAMP_NOT_NORMALIZED
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet.
summary: Unity identified risks around customer expansion, renewal, cancellations, reductions in use, customers developing in-house alternatives, and customer confidence in Unity monetization products.
missing_or_unsafe_fields:
  - exact publication or filing timestamp must be normalized
  - retrieval timestamp must be recovered or marked unavailable
  - source-byte hash must be computed from canonical source bytes
```

### EU-06

```yaml
evidence_id: EU-06
source_id: S-03
source: https://www.sec.gov/Archives/edgar/data/1810806/000181080623000016/unity-20221231.htm
timestamp: TBD_EXACT_SOURCE_TIMESTAMP_NOT_NORMALIZED
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Unity 2022 Form 10-K filing body was visible before the 2023-09-11 cutoff according to the source packet.
summary: Unity described competition from alternative platforms, in-house tools, and other providers, and listed features, functionality, price, and customer economics as competitive factors.
missing_or_unsafe_fields:
  - exact publication or filing timestamp must be normalized
  - retrieval timestamp must be recovered or marked unavailable
  - source-byte hash must be computed from canonical source bytes
```

### EU-07

```yaml
evidence_id: EU-07
source_id: S-07
source: https://web.archive.org/web/20230103153058/https://www.unrealengine.com/en-US/license
timestamp: "2023-01-03 15:30:58 UTC"
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH
pre_decision_status: verified_pre_decision
pre_decision_basis: Internet Archive snapshot timestamp was before the 2023-09-11 cutoff.
summary: A major alternative engine publicly presented a different licensing frame, useful only as contextual evidence about public engine-pricing expectations.
missing_or_unsafe_fields:
  - archive CDX digest or source-byte hash must be recovered
  - retrieval timestamp must be recovered or marked unavailable
  - summary must preserve competitor-context limit and not imply Unity customer switching
```

### EU-08

```yaml
evidence_id: EU-08
source_id: S-04_S-05
source: bounded Internet Archive CDX lookups for Unity compare-plans and pricing URL variants
timestamp: 2023-01-01_to_2023-09-11_lookup_windows
retrieval_timestamp: TBD_ORIGINAL_RETRIEVAL_TIMESTAMP_NOT_NORMALIZED
hash: TBD_SOURCE_BYTE_HASH_OR_CDX_RESPONSE_HASH
pre_decision_status: excluded
pre_decision_basis: The source packet reports bounded pre-cutoff archive lookups that did not return usable 200 snapshots; this is a visibility gap, not affirmative pricing evidence.
summary: Exact pre-cutoff Unity pricing, package thresholds, and terms visibility were not established in this source-loading run.
adapter_decision_status: UNRESOLVED
draft_registry_treatment: Provisional excluded EvidenceUnit candidate or facilitator-only source-gap note. Operator must decide before registry freeze; participant_packet_draft_v0.md must not treat EU-08 as an evidence summary until that adapter decision is made.
missing_or_unsafe_fields:
  - decide whether EU-08 remains an excluded EvidenceUnit or moves to a facilitator-only source-gap note
  - hash CDX responses if retained as registry evidence
  - do not treat negative lookup as proof that no pre-cutoff Unity pricing or terms page existed
```

## Registry-Level Missing Fields

- Stable per-source source-byte hashes are missing, including S-01 if retained as a participant source-manifest locator.
- Original retrieval timestamps are not normalized.
- Exact source timestamps for S-03 are not normalized.
- S-04 and S-05 CDX response treatment is unresolved.
- EU-08 adapter decision is unresolved.
- `source_type` exists in the case-construction protocol but not in the Pydantic `EvidenceUnit`; any later serialized object must choose which surface it is satisfying.
- Source packet hash `FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24` is packet provenance only, not a substitute for per-source source-byte hashes.

## Not Ready For Scoring

This draft registry cannot support evidence ID checks, must-address coverage checks, or scoring until per-source hashes, timestamps, retrieval timestamps, pre-decision bases, and EU-08 treatment are resolved and the registry is frozen as an accepted fixture input.
