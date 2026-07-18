# Company Surface First-Company Ingest Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow operational record (executed first-company ingest receipt)
scope: >
  Observed-fact receipt for the bounded Tower 28 Beauty Phase 1 v2 ingest into
  the accepted Company Surface logical-record and Silver mapping contracts.
  Records the exact mapped observations and coverage, explicit exclusions and
  contract friction, canonical Silver identities, and generated-view hashes.
use_when:
  - Verifying the first real-company Company Surface ingest.
  - Tracing Tower 28 Company Surface records to OBS/COV rows and Bronze packets.
  - Checking what remained outside or unexpressible under the accepted contract.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
  - forseti/product/information/company_surface/company_surface_silver_mapping_contract_v0.md
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v2.md
  - docs/research/forseti_beauty_tower28_company_intelligence_scan_v2.md
stale_if:
  - Any listed canonical Silver record is unavailable or fails source verification.
  - The Company Surface logical-record or Silver mapping contract is superseded.
  - A later receipt explicitly supersedes this bounded 2026-07-18 ingest.
```

## Run Boundary

- Company: Tower 28 Beauty, Brand anchor `brand:tower-28-beauty`.
- Input: owner-ratified Phase 1 v2 report after PR #1093's overclaim fix.
- Handoff consumed:
  `docs/workflows/forseti_company_surface_first_company_ingest_handoff_v0.md`.
- Canonical root: `F:\forseti-data-lake`; verified root UUID
  `01KW7N6ERSVVANCEZ8SD6YW3EQ`.
- Recorded window begins `2026-07-18T04:11:03Z`; record order increments by
  one second so the failed-then-successful coverage history has an inspectable
  knowledge cutoff.
- No live web read, re-capture, new schema, generic adapter, matcher,
  monitoring, GTM field, or decision field was added.

The first temporary-lake run wrote all 16 records, then its verifier failed on
an incorrect nested view-entry key. The canonical lake was untouched. The
verifier alone was corrected and a fresh temporary lake passed before the
canonical append.

## Mapped Logical Records

Thirteen logical records mapped to thirteen primary Silver records. Observation
payloads remain upstream; Company Surface stores attachment, evidence, time,
state, and limitations.

| Logical reference | Source row | Bronze raw anchor | Silver record |
| --- | --- | --- | --- |
| `company.subject.tower28.brand` | OBS-038 first-party Brand identity | `01KXRKNR8FF5NAZJQYY32RFZWG` | `company_a9eb4eee2d436f169b4cb220.json` |
| `company.activity.tower28.obs-031` | OBS-031 retailer PDP claim state | `01KXRM2S8VCVDC8D3DA3CCDY0K` | `company_9ed645b7e7bdd6ee3f1bfcef.json` |
| `company.activity.tower28.obs-036` | OBS-036 Amazon SOS seller state | `01KXRKTXCYFRW23GVWP5JSKJDH` | `company_cf2a604409cafe78c6cf3964.json` |
| `company.activity.tower28.obs-037` | OBS-037 Amazon SunnyDays seller state | `01KXRKYNNEBFN7Q375AKR4N2K9` | `company_5cd08222bf419fa53b915074.json` |
| `company.activity.tower28.obs-038` | OBS-038 authorized-seller-list state | `01KXRKNR8FF5NAZJQYY32RFZWG` | `company_bcb05fe0b7332300e2c47c5c.json` |
| `company.activity.tower28.obs-041` | OBS-041 NEA directory listing | `01KXRMGB4WEVBF19G464PSHZNJ` | `company_0f600f8be65e0a89f625981f.json` |
| `company.activity.tower28.obs-042` | OBS-042 NRS directory listing | `01KXRM4HZJVVRVFAGFFX6VY5DD` | `company_a89eff0d52394d3e2993bf3c.json` |
| `company.activity.tower28.obs-043` | OBS-043 NPF directory listing | `01KXRMJBBSE3BP9RF0PAEQ3B7H` | `company_3049e6888bc1dd41cbd72a4f.json` |
| `company.coverage.tower28.cov-021` | COV-021 bounded Sephora sample | `01KXRM2S8VCVDC8D3DA3CCDY0K` | `company_a31857f23c7d49188a7aa9f6.json` |
| `company.coverage.tower28.cov-022.sunnydays-us-pin-attempt-1` | COV-022 failed US-pin attempt | `01KXRKWZJXDRM7JYESMASJESWG` | `company_eadb9af725c5fc6aae98135d.json` |
| `company.coverage.tower28.cov-022.sunnydays-us-pin-attempt-2` | COV-022 successful retry, still partial overall | `01KXRKYNNEBFN7Q375AKR4N2K9` | `company_75fac737fddc024fe100499b.json` |
| `company.coverage.tower28.cov-023` | COV-023 three certifier directories | `01KXRMGB4WEVBF19G464PSHZNJ` | `company_02442a33ece777b667a37810.json` |
| `company.coverage.tower28.cov-024` | COV-024 first-party preservation coverage | `01KXRKNR8FF5NAZJQYY32RFZWG` | `company_6383be562dc9e694e6008a17.json` |

Three companion edges complete the physical set:

| Edge | Silver record |
| --- | --- |
| OBS-038 conflicts with OBS-036 | `company_edge_c677ea8c301b54beb79ed0b7.json` |
| OBS-038 conflicts with OBS-037 | `company_edge_00f57f87917efa5b8f7aeff7.json` |
| Successful COV-022 retry supersedes failed attempt | `company_edge_c5ba2b3b622821d3307824fa.json` |

## Packet Evidence

Every selected preserved file was rehashed before both dry-run and canonical
write. COV-022 folds the successful search and the later soft-block into the
partial-coverage record rather than minting a redundant sixth coverage marker.

| Packet | Use | Selected raw SHA-256 |
| --- | --- | --- |
| `01KXRKN8DZYY66P44N32R2GQ6A` | Amazon search success and second-seller limitation | `9cb92425d3b6fce04237306988bbec9067cb8c714d4a02335c7e60754409bdce` |
| `01KXRKNT543FVHGJNRMB8X76RK` | Amazon profile-less search soft-block | `1cc2599cfba29cdb93be4280f5c5a31ee672db3191aff4426641a4a42f5fff1a` |
| `01KXRKNR8FF5NAZJQYY32RFZWG` | First-party stores page / OBS-038 | `da2bcd9883b4f9e29b20b3f96e8e00cea917d4c8bbfe6ff4ae06322ba2302b70` |
| `01KXRKPW08AEP94X5G29YTR3EH` | Ingredients page / COV-024 history limitation | `57e59cc649ec3dc5754e43a8f19b41ef52f38aae0d33b6c63bc2c9e343fcdc12` |
| `01KXRKTXCYFRW23GVWP5JSKJDH` | Amazon SOS PDP / OBS-036 | `273738d746d253f5e427021ec236370190ba9fb146719ec6497e4781e135686f` |
| `01KXRKWZJXDRM7JYESMASJESWG` | SunnyDays failed US-pin attempt | `4bb5912eb9b3b778189e5f0aaa752bba53735f13e8fe98ce16617cc0007306e0` |
| `01KXRKYNNEBFN7Q375AKR4N2K9` | SunnyDays successful retry / OBS-037 | `d7de5539dbfa2bcd3d42328f45ec4d7c79170aa3fddc434c1d5e00540414149f` |
| `01KXRM2S8VCVDC8D3DA3CCDY0K` | Sephora SOS PDP / OBS-031 | `623d58e53a4ef2f48081579fe5d322edea795c3ef25ddade6917d27b9d6454ff` |
| `01KXRM4HZJVVRVFAGFFX6VY5DD` | NRS directory / OBS-042 | `cbaf51bcd8dd39a3fcda79ec634fbd8f15da71df87f41a2b67789c131935d275` |
| `01KXRMGB4WEVBF19G464PSHZNJ` | NEA directory / OBS-041 | `6bc8061e49767e4c51c76830102ccd1a282310a32a76b7c7f14b83b002ec0dea` |
| `01KXRMJBBSE3BP9RF0PAEQ3B7H` | NPF directory / OBS-043 | `97cb8e676e065f1e6313109c6738118537fdeab562b2be51660008d60cf32de1` |

## Exclusions And Typed Friction

- Imported only report candidates CSC-001 and CSC-002, not all 43 OBS rows or
  the report narrative.
- Executive Brief conclusions, confidence, chain cards, interpretation,
  priority, pain, buyer, ICP, wedge, GTM, outreach, and contact authority remain
  downstream.
- Product, SKU, claim, and channel details remain in the referenced upstream
  observations. The accepted Company Surface subject grammar supports Brand and
  Org only; this ingest did not mint new canonical entity types.
- No `relationship_assertion` was emitted: the bounded candidate evidence
  supports no accepted `owned_by` or `subsidiary_of` claim.
- Proxy relations were not promoted into accepted relationships.
- OBS-003 to OBS-039 was not emitted as activity history. OBS-003 has no lawful
  Bronze packet anchor; OBS-039 therefore remains COV-024 evidence for an
  unresolved historical claim-location gap, not a fabricated historical record.
- Amazon seller display remains seller-of-record evidence. It was not
  strengthened into a direct claim that Tower 28 operates or authorizes every
  Amazon listing.
- Review examples and directory listings remain existence/recognition evidence,
  never prevalence, concentration, efficacy, comedogenicity, demand, or
  sell-through claims.

## Generated Views And Observed Behavior

The current view contains eight resolved records (one Brand assertion plus seven
activity links), four visible coverage markers, zero residuals, two conflicts,
and one superseded-record exclusion.

At knowledge cutoff `2026-07-18T04:11:12.500000Z`,
`historical_as_known` exposes the failed COV-022 attempt. Under the later cutoff,
`historical_restated` excludes that failed attempt and exposes the successful
partial retry. This is coverage/knowledge history, not invented company history.

| Generated file | SHA-256 |
| --- | --- |
| `manifests/current.json` | `8da0c66a692cf12e2d450a63e2987cfedfb58f10d192cfaf4a73e795479f14bb` |
| `manifests/historical_as_known.json` | `9497a8c4bd9bf0da26146922788cc8a04a1214001fc6713e09dddbce8117a285` |
| `manifests/historical_restated.json` | `acc5fab1c854e62b4c0498b775ef54a00027ca2f6b14b71d0dec0b5910eff107` |
| `views/current.json` | `072427f8c03c988c896b73829e8c679b0c9c717c4e152ac24280cde3a26f145f` |
| `views/historical_as_known.json` | `e111c7266bb5dfa8e583e1ede91098b37d13e6e8b15f1d4f234916bf60136455` |
| `views/historical_restated.json` | `cb7174450719ab1057905963f7a984b79fe147739ea5ce8f1f0f415986565cda` |

Dry-run and canonical hashes matched for all six files. The public rebuild proof
returned `status=proven`.

## Validation

- PASS: eleven selected raw packet members rehashed to their manifests.
- PASS: 13 logical records validated before write.
- PASS: mapping preview produced 13 primaries and three companion edges with no
  target collision.
- PASS: fresh temporary-lake append, physical source verification, three view
  modes, temporal assertions, and deterministic rebuild proof.
- PASS: canonical append and fresh readback found exactly the same 16 Silver
  records and six generated-file hashes.
- PASS: 41 focused Company Surface, Data Lake physicalization, and Silver
  census tests.
- PASS: the complete 3,724-test / 273-file harness corpus partitioned
  deterministically across eight groups; every group exited zero, with seven
  visible skips.
- INFO: the first monolithic full-harness invocation exceeded its 60-second
  window without emitting a failure; it was not retried, and the complete
  partitioned corpus passed.
- PASS: all 24 current commit-level CI policy commands against the lane base,
  including retrieval, placement, ontology, Silver-lane, review/provenance,
  hash, deletion-evidence, prompt, handoff, claim, and harness-coupling gates.

## Non-Claims

This receipt is a dated execution record, not current-market evidence, broad
Company Surface readiness, a 60-company backfill, monitoring readiness, product
or Org identity graduation, buyer proof, GTM validation, or outreach authority.
