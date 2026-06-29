# Fragrantica Data Lake Raw Packet Admission Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Lane decision record
scope: Verified Data Lake disposition for the Fragrantica current-window direct HTTP packet and bounded downstream Projection/ECR/Cleaning scope.
use_when:
  - Deciding whether to reuse, quarantine, or replay the Fragrantica direct HTTP packet.
  - Scoping Fragrantica mechanical projection, ECR receipt, or Cleaning input without overstating completeness.
  - Checking why this packet is classified as fragrance-native database material rather than retail PDP material.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
input_hashes:
  direct_receipt_sha256: 7294350957F35BBCA04C529EC776611A0B52D043E262E86F2DB2329A0BE17111
  direct_manifest_sha256: 15800A4CB1A8D67EAC68C2D15C0831967E1661F0BB071AFEEDDE0601E4F86D2E
  direct_body_sha256: 62EDE0326B08124BC9A8E54C991FA7BCF531A06177A69C04CAB2D33C5C531273
  direct_metadata_sha256: 916C1E9DA98D66C60DB3B5395CD2FBF692D552648967EC72EA896DFC68E17E0A
  cloakbrowser_receipt_sha256: 9F5EB291774D5C8920616C37585B557F61752826AFFD9559180B29F8B408B027
  cloakbrowser_manifest_sha256: 5617786EE44982F7645B170AB3776CA756DD0F4B59F843AEAB238218D51A0695
stale_if:
  - Fragrantica direct packet files, manifest, source_family, source_surface, or DataLakeRoot raw path semantics change.
  - A later packet captures the full Fragrantica review archive or supersedes this current-window packet.
  - A later owner decision changes generated-packet lifecycle, fixture admission, Data Lake admission, Projection, ECR, or Cleaning boundaries.
```

## Decision

Disposition: `ACCEPT_EXISTING_PACKET_FOR_CURRENT_WINDOW_RAW_USE`.

Accept the existing Fragrantica direct HTTP packet at
`F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV` as the Data Lake raw
packet for this current-window Fragrantica continuation. Do not quarantine or
immediately replay it solely because `ORCA_DATA_ROOT` routed the probe output
to the external lake root.

This is a structural Data Lake reuse decision, not fixture admission and not a
source-completeness claim. A later replay is still allowed if the owner wants a
cleaner deliberate run, a full-archive route, or a separately admitted fixture.

## Basis

The packet passed the raw-admission checks needed for this lane:

- `packet_id=01KW7SGXRZHFTS372X391Z8GHV`.
- `sha256(packet_id)[:3]` recomputes to shard `930`.
- The observed path matches `raw/<packet_shard>/<packet_id>/`.
- Manifest version is `source_capture_packet_manifest_v1`, matching the current
  `SOURCE_CAPTURE_MANIFEST_VERSION` in `orca-harness/source_capture/models.py`.
- `source_family=fragrance_native_database`.
- `source_surface=fragrantica_product_page_direct_http`.
- The manifest is parseable, file handles are unique, slice references resolve,
  preserved bodies exist, recorded sizes match, and stored-body hashes verify.
- `DataLakeRoot.resolve(explicit="F:/orca-data-lake").load_raw_packet(...)`
  returned `LOAD_RAW_PACKET=PASS`.

Reject replay for now because replay would create a second packet for the same
current-window direct HTTP fact without resolving the real open boundary: the
full Fragrantica review archive is still not captured.

## Classification

Lake key:

- `packet_id=01KW7SGXRZHFTS372X391Z8GHV`

Raw physical home:

- `raw/930/01KW7SGXRZHFTS372X391Z8GHV/`

Semantic classification belongs in manifest/projection/attachment metadata, not
the raw path:

- `source_family: fragrance_native_database`
- `source_surface: fragrantica_product_page_direct_http`
- `source_platform: fragrantica`
- `source_object_type: fragrance_product`
- `source_object_site_id: 33519`
- `source_locator: https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html`

Explicit negative classification: not `retail_pdp`, not retailer
verified-purchase review substrate, and not merchant offer, price, or
availability substrate.

## Current-Window Boundary

Fresh byte checks found direct current-window review-card markers consistent
with the handoff's `210` direct-card diagnosis:

- `210` unique `?ccid=<id>#focus-zone` share paths in the direct HTTP body.
- `210` opening `<user-perfume-votes-new` tags and `210` closing
  `</user-perfume-votes-new>` tags in the direct HTTP body.
- The CloakBrowser rendered DOM contains `310` unique `review_<id>` identifiers.
- The CloakBrowser visible text contains `Reviews (3.9K)` and
  `Sign in to access the full review archive`.

Therefore the direct packet is a useful current-window raw packet, but it is
not a complete Fragrantica review archive.

## Packet Lifecycle And Sensitivity

Lifecycle state for this decision: `candidate_evidence`.

Reason for retention: preserve inspectable raw current-window Fragrantica
source bytes for Data Lake by-key access and bounded mechanical downstream
scoping.

Sensitivity and handling note: the packet includes raw third-party source HTML,
review text/handles or profile-visible review-card material, and machine-specific
absolute paths in manifest provenance. It has no recorded credential, cookie,
stored-profile, proxy, CAPTCHA, or session-injection material. This note is not
legal sufficiency, rights clearance, privacy review, publication permission, or
fixture admission.

Allowed downstream use:

- mechanical projection scoping over this packet;
- ECR source-side receipt/posture scoping by raw/projection refs;
- Cleaning input scoping for non-destructive normalization only.

Forbidden claims:

- no fixture admission;
- no full review archive;
- no source completeness proof;
- no review-attached-photo proof;
- no demand, buyer proof, Judgment, credibility, independence, sentiment,
  exclusion, or commercial-readiness claim.

## Downstream Scope

Projection lane may scope a `fragrance_native_database` mechanical projection
with these row groups:

- product snapshot rows;
- current-window review-card rows keyed to raw anchors;
- review-tab/source-order facts where mechanically recoverable;
- source-visible rating/performance vote facts;
- residual/loss ledger entries for full-archive incompleteness, missing linked
  media preservation, no review-attached-photo proof, and no full archive.

ECR lane may consume only raw/projection refs and carried source-visible or
residualized facts. It must not merge projection fields into ECR posture fields
and must not author scent meaning, quality, demand, credibility, independence,
or completeness from prose.

Cleaning lane may define non-destructive normalization only: review text cleanup,
source-language/string normalization, mechanical length bins,
author/display-name normalization with raw refs, and source-visible
rating/performance enum carry. Cleaning must not decide sentiment, credibility,
duplicate effect, independence, demand, exclusion, or action support.

## Stop Or Pivot Conditions

Stop and reopen the source ladder if any of these occur:

- the direct packet path or hashes drift;
- `source_family` or `source_surface` differs from the values above;
- DataLakeRoot can no longer load the packet by key;
- a later Fragrantica packet captures the full archive or supersedes this
  current-window packet;
- the owner asks for fixture admission, publication, legal review, or Judgment
  use.

## Verification Ledger

Observed command outputs from this continuation:

```text
git status --short --branch
## codex/fragrance-native-live-probe...origin/codex/fragrance-native-live-probe
 M docs/research/orca_fragrance_native_database_live_probe_v0.md
?? docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md

git rev-parse --short HEAD
b4641d65

git branch --show-current
codex/fragrance-native-live-probe
```

```text
packet_id=01KW7SGXRZHFTS372X391Z8GHV
expected_shard=930
actual_path=F:\orca-data-lake\raw\930\01KW7SGXRZHFTS372X391Z8GHV
path_matches=True
manifest_version=source_capture_packet_manifest_v1
source_family=fragrance_native_database
source_surface=fragrantica_product_page_direct_http
```

```text
STRUCTURAL_CHECK=PASS
LOAD_RAW_PACKET=PASS
root=F:\orca-data-lake
container=F:\orca-data-lake\raw\930\01KW7SGXRZHFTS372X391Z8GHV
manifest_packet_id=01KW7SGXRZHFTS372X391Z8GHV
manifest_version=source_capture_packet_manifest_v1
source_family=fragrance_native_database
source_surface=fragrantica_product_page_direct_http
body_file_ids=file_01,file_02
body_sizes=file_01:1806640,file_02:515
```

```text
F:\orca-data-lake\raw\930\01KW7SGXRZHFTS372X391Z8GHV\receipt.md|7294350957F35BBCA04C529EC776611A0B52D043E262E86F2DB2329A0BE17111
F:\orca-data-lake\raw\930\01KW7SGXRZHFTS372X391Z8GHV\manifest.json|15800A4CB1A8D67EAC68C2D15C0831967E1661F0BB071AFEEDDE0601E4F86D2E
F:\orca-data-lake\raw\930\01KW7SGXRZHFTS372X391Z8GHV\raw\01_http_response_body.bin|62EDE0326B08124BC9A8E54C991FA7BCF531A06177A69C04CAB2D33C5C531273
F:\orca-data-lake\raw\930\01KW7SGXRZHFTS372X391Z8GHV\raw\02_http_response_metadata.json|916C1E9DA98D66C60DB3B5395CD2FBF692D552648967EC72EA896DFC68E17E0A
```

```text
CloakBrowser receipt hash:
9F5EB291774D5C8920616C37585B557F61752826AFFD9559180B29F8B408B027

CloakBrowser manifest hash:
5617786EE44982F7645B170AB3776CA756DD0F4B59F843AEAB238218D51A0695

CloakBrowser preserved body hashes:
9E37EDA80975B077183DBF615673531C9C8894016B0F08901436D19F5BF107A7
AA072ABEA821F7350469775BDADB9B6D60696752681714192472A34A2C5C4B2E
619658CA8112E5AA29B9E114B8510E749FA6C3F0FC1BD9B238C3CE2187B5CBD4
CCFA6747A870C0567356C61C26D11639B3AFEDFEB671E730B0388FF8D07DEFC5
```

```text
Direct-body count checks:
210 unique ?ccid=<id>#focus-zone share paths
210 opening <user-perfume-votes-new tags
210 closing </user-perfume-votes-new> tags

CloakBrowser checks:
310 unique review_<id> identifiers in rendered DOM
visible text line 63: Reviews (3.9K)
visible text line 3509: Sign in to access the full review archive
```

## Non-Claims

This record is not implementation authorization, storage-engine selection,
projection schema ratification, ECR implementation, Cleaning implementation,
fixture admission, source completeness proof, legal review, privacy review,
rights clearance, Judgment evidence, buyer proof, validation, readiness, or
commercial-readiness evidence.
