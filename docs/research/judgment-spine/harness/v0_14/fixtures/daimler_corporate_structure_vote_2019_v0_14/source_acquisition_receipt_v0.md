# Daimler Source Acquisition Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Facilitator-only source-acquisition receipt for Daimler S1-S7 current-live and owner-supplied source-byte captures.
use_when:
  - Checking which Daimler S1-S7 source hashes and retrieval timestamps were captured after owner source-acquisition authorization.
  - Separating successful public byte retrievals and owner-supplied captures from optional canonical-source residue before evidence-registry drafting.
  - Preserving participant-safe source-manifest boundaries by keeping titles, URLs, hashes, and retrieval timestamps facilitator-only.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/source_acquisition_and_manifest_plan_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
input_hashes:
  fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  source_acquisition_and_manifest_plan_v0.md: D85D69F16308138AFB639DA3BD2229A43A13EE96653D9CF8B62E69122B8C5BDD
  participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  post_patch_recheck_v0.md: BD32C40BE7A7E2129871C787177D929FD497347F0764ED1B00B7D904ED8CE741
branch_or_commit: main @ a2aebdd
stale_if:
  - Owner requires canonical Mercedes-Benz Group bytes instead of accessible public distribution or mirror bytes.
  - Owner authorizes storing raw source bytes in the fixture folder.
  - Owner supplies canonical Mercedes-Benz Group bytes for S1, canonical issuer-domain annual-report bytes for S4A, or original Reuters/Investing bytes for S7.
```

## Acquisition Boundary

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_daimler_source_acquisition_plan_plus_case_seed
  edit_permission: docs-write for facilitator-only source-acquisition receipt
  target_scope: Acquire current-live public and owner-supplied source hashes and retrieval timestamps for Daimler S1-S7 where retrievable, and record remaining optional canonical-source residue.
  dirty_state_checked: yes
  blocked_if_missing: no
source_acquisition_status: S1_S7_HASH_TIMESTAMP_GATE_COMPLETE_FOR_CURRENT_SOURCE_SET
source_byte_storage_status: hashes_recorded_raw_bytes_not_stored_in_repo
raw_byte_storage_basis: source_acquisition_plan_default_defers_raw_byte_storage_without_explicit_owner_storage_decision
owner_supplied_capture_status: four_pdf_files_hashed_from_downloads
participant_visibility: facilitator_internal_only
```

The owner authorized source acquisition in chat after the post-patch Daimler fixture-entry recheck, and later supplied the four blocked Mercedes-Benz PDF captures from the browser download path. This receipt records the smallest complete acquisition pass under the existing storage policy: compute hashes and retrieval timestamps from successful current-live HTTP response bytes and owner-supplied local PDF bytes, but do not store raw source bytes in the repository.

This receipt is facilitator-only because it contains source titles, URLs, retrieval timestamps, and hashes. None of this material is participant-facing.

No runtime code, memorization probe, contestant exposure, model run, scoring, schema implementation, ledger freeze, validation, product proof, fixture admission, blind-use readiness, or judgment-quality claim is authorized or performed here.

## Captured Source Bytes

Hashes below are SHA-256 over successful current-live HTTP response bytes or owner-supplied local PDF bytes. Raw bytes were not retained in the repository.

| Source ID | Source class | Retrieval source | Retrieval timestamp | HTTP status | Content type | Bytes | SHA-256 | Capture status |
| --- | --- | --- | --- | ---: | --- | ---: | --- | --- |
| DCSV-S1 | S1 official issuer disclosure from October 2017 | `https://www.prnewswire.com/news-releases/daimler-board-of-management-decides-on-first-steps-to-strengthen-the-divisional-structure-300536970.html` | `2026-05-30T16:20:46Z` | 200 | `text/html; charset=UTF-8` | 213668 | `3B2F49C6B4225B26B0E2F51E9ACEB19344F6D2CD5BAB400D562F0AB1910EA85A` | captured from official PRNewswire distribution; canonical Mercedes-Benz Group page blocked programmatic retrieval |
| DCSV-S2 | S2 official investor presentation from May 2018 | `C:\Users\vmon7\Downloads\daimler-ir-corporatepresentation-may-2018.pdf` | `2026-05-30T16:40:53.5951509Z` | n/a | `application/pdf` | 16367610 | `ECED20BD57F7162FD94E0D0D5E75E5C91574624F349F89D0A3D616A6C4FCDCCF` | owner-supplied local PDF capture of official Mercedes-Benz Group investor presentation; PDF signature verified |
| DCSV-S3 | S3 official corporate-structure release from July 2018 | `https://www.daimlertruck.com/en/newsroom/pressrelease/consistent-continuation-of-strategy-daimler-lines-up-for-the-future-40772994` | `2026-05-30T16:19:30Z` | 200 | `text/html; charset=utf-8` | 177034 | `7DD023357E42D5428F646E978A057A55FAA499EBBE466942ACD4A990D6AA2383` | captured from official Daimler Truck page |
| DCSV-S3-ALT | S3 official corporate-structure release alternate distribution | `https://www.prnewswire.com/news-releases/consistent-continuation-of-strategy-daimler-lines-up-for-the-future-300687039.html` | `2026-05-30T16:20:48Z` | 200 | `text/html; charset=UTF-8` | 211703 | `2A6017ECC2AB538A2E51246F20EB48B1A239AAD28766B3F9DD55F626B718EED9` | captured as corroborating official distribution, not needed if DCSV-S3 remains accepted |
| DCSV-S4A | S4 official 2018 annual reporting material | `https://www.annualreports.com/HostedData/AnnualReportArchive/d/NYSE_DAI_2018.pdf` | `2026-05-30T16:24:05Z` | 200 | `application/pdf` | 11875500 | `A6A8A534AA6F91BAA131A96E9C674892FA61F782E1C0D99D52F197830D481D6A` | captured from public mirror of official annual report; canonical Mercedes-Benz Group PDF blocked programmatic retrieval |
| DCSV-S4B | S4 official pre-vote annual-meeting material | `C:\Users\vmon7\Downloads\daimler-ir-am-agenda-2019.pdf` | `2026-05-30T16:40:59.4868089Z` | n/a | `application/pdf` | 2689478 | `AD2DD0669EBE1DBB5BFD7BA725FF811206F11F8E7EE49B87F623D27FD4C5A843` | owner-supplied local PDF capture of official Mercedes-Benz Group AGM agenda/invitation; PDF signature verified |
| DCSV-S5 | S5 official hive-down legal materials before vote | `C:\Users\vmon7\Downloads\daimler-ir-am-hivedownreport-2019.pdf` | `2026-05-30T16:41:03.3973838Z` | n/a | `application/pdf` | 4121124 | `E8D1C83D829A6926AF75D0C1EF122110F56631795770244F3E4B10F63FE52A55` | owner-supplied local PDF capture of official Mercedes-Benz Group hive-down report; PDF signature verified |
| DCSV-S6 | S6 official divisional business updates before cutoff | `C:\Users\vmon7\Downloads\daimler-ir-cmddtstrategydaum-20180606.pdf` | `2026-05-30T16:41:06.8947056Z` | n/a | `application/pdf` | 4064281 | `BFC5122922BF2755D81BE46B1B58AFDA5E1622C598D07E7544B5E02B56069895` | owner-supplied local PDF capture of official Mercedes-Benz Group divisional update; PDF signature verified |
| DCSV-S7 | S7 independent business press before cutoff | `https://autto.at/en/news/daimler-split-business-cars-trucks-mobility-units-20180730.html` | `2026-05-30T16:21:31Z` | 200 | `text/html; charset=utf-8` | 23437 | `58E9A350C8B5B6AF58122812BBCF72431DEB120B85B0BB5AC9BDDADC2E3727B7` | captured from accessible independent business-press mirror; original Reuters/Investing page blocked programmatic retrieval |

## Remaining Optional Source Residue

The rows below were located as source candidates but did not produce usable source-byte hashes in this pass. They no longer block the S1-S7 hash/timestamp gate for the current source set, but they remain optional residue if the owner later requires canonical issuer-domain or original wire-service bytes. A 403 denial page hash is not a source-byte hash and must not be used in an evidence registry as if it were the target source.

| Source ID | Source class | Blocked source | Retrieval attempt timestamp | Result | Required next action if owner requires this exact artifact |
| --- | --- | --- | --- | --- | --- |
| DCSV-S1-CANONICAL | S1 official issuer disclosure from October 2017 | `https://group.mercedes-benz.com/investors/reports-news/ad-hoc/adhoc-release-316518.html` | `2026-05-30T16:19:30Z` | Mercedes-Benz Group endpoint returned HTTP 403 Access Denied to programmatic retrieval. | Use DCSV-S1 PRNewswire distribution unless owner requires canonical issuer-domain bytes; if canonical bytes are required, owner/browser-supplied capture is needed. |
| DCSV-S7-ORIGINAL | S7 independent business press before cutoff | `https://uk.investing.com/news/stock-market-news/daimler-to-split-business-into-cars-trucks-mobility-units-1260883` | `2026-05-30T16:19:33Z` | Investing/Reuters mirror returned HTTP 403 to programmatic retrieval. | Use DCSV-S7 accessible mirror unless owner requires the original Investing/Reuters page bytes; if original bytes are required, owner/browser-supplied capture is needed. |

## Evidence Registry Impact

```yaml
source_hash_timestamp_gate: complete_for_current_source_set
fillable_now_from_current_pass:
  DCSV-S1:
    hash_status: captured_from_official_distribution
    retrieval_timestamp_status: captured
    raw_bytes_retained: false
  DCSV-S2:
    hash_status: captured_from_owner_supplied_local_pdf
    retrieval_timestamp_status: captured_from_local_file_timestamp
    raw_bytes_retained: false
  DCSV-S3:
    hash_status: captured_from_official_daimler_truck_page
    retrieval_timestamp_status: captured
    raw_bytes_retained: false
  DCSV-S4A:
    hash_status: captured_from_public_mirror_of_official_annual_report
    retrieval_timestamp_status: captured
    raw_bytes_retained: false
  DCSV-S4B:
    hash_status: captured_from_owner_supplied_local_pdf
    retrieval_timestamp_status: captured_from_local_file_timestamp
    raw_bytes_retained: false
  DCSV-S5:
    hash_status: captured_from_owner_supplied_local_pdf
    retrieval_timestamp_status: captured_from_local_file_timestamp
    raw_bytes_retained: false
  DCSV-S6:
    hash_status: captured_from_owner_supplied_local_pdf
    retrieval_timestamp_status: captured_from_local_file_timestamp
    raw_bytes_retained: false
  DCSV-S7:
    hash_status: captured_from_accessible_independent_press_mirror
    retrieval_timestamp_status: captured
    raw_bytes_retained: false
blocked_after_owner_supplied_capture: []
optional_canonical_residue:
  - DCSV-S1-CANONICAL
  - DCSV-S4A-CANONICAL, if owner requires issuer-domain annual-report bytes instead of annualreports.com mirror bytes
  - DCSV-S7-ORIGINAL
```

The evidence registry may mark source hashes and normalized retrieval timestamps captured for the current S1-S7 source set. It must not treat this as fixture admission, blind-use readiness, ledger freeze, validation, or judgment-quality proof. S1, S4A, and S7 still need owner acceptance if canonical issuer-domain or original wire-service page bytes are required instead of accessible public distribution or mirror bytes.

## Participant-Safe Boundary

Participant-facing source manifest material may use only S1-S7 labels and high-level source-class descriptions. It must not include the URLs, titles, outlet names, retrieval timestamps, byte sizes, source hashes, 403 failure details, or mirror/provenance notes in this receipt.

## Non-Claims

- Not canonical-source closure if owner later requires canonical or original bytes for S1, S4A, or S7.
- Not a historical archive capture.
- Not a raw-byte repository archive.
- Not a frozen evidence registry.
- Not participant-packet readiness.
- Not blind-use readiness.
- Not memorization-probe pass.
- Not model-run authorization.
- Not scoring readiness.
- Not ledger freeze.
- Not schema or runtime implementation.
- Not validation.
- Not product proof.
- Not fixture admission.
- Not judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
