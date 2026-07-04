# Capture Source Family: Fragrance Native Database

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane index
scope: >
  Cold-start lane index for fragrance-native database capture routes:
  Fragrantica, Parfumo, and Basenotes. Ties source-access route evidence,
  packet runners, mechanical projection, Data Lake, ECR, and Cleaning seams
  without re-owning downstream layer contracts.
use_when:
  - Starting Fragrantica, Parfumo, or Basenotes capture-to-lake work.
  - Checking whether a fragrance-native database source should be treated as retail/PDP.
  - Finding the first runner, projection helper, or Cleaning lake writer for a fragrance-native database packet.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_fragrance_native_database_live_probe_v0.md
  - docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
  - forseti/product/spines/data_lake/README.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - Fragrantica, Parfumo, or Basenotes route posture changes.
  - A fragrance-native database runner, projection helper, or Cleaning lake writer changes source_family/source_surface requirements.
  - Data Lake raw/derived/Silver authority changes.
```

## Canonical Classification

Fragrantica, Parfumo, and Basenotes belong to:

```yaml
source_family: fragrance_native_database
```

Do not classify them as `retail_pdp`. They are specialist/enthusiast fragrance
databases with product pages and community text, not merchant PDPs with
verified-purchase/offer/availability semantics.

## Route Map

| Source | Access route / source surface | Packet runner | Projection | Cleaning / Silver seam | Residuals to preserve |
| --- | --- | --- | --- | --- | --- |
| Fragrantica | Direct HTTP plus optional rendered current-window diagnostics. Primary direct surface: `fragrantica_product_page_direct_http`. | `orca-harness/runners/run_fragrantica_mgt_capture.py` | `orca-harness/source_capture/fragrantica_projection.py`; runner `run_fragrantica_projection.py`; lane `projection_fragrantica`. | `orca-harness/cleaning/fragrantica.py`; lake writer `orca-harness/cleaning/fragrantica_lake.py`. | Current-window review capture only; full archive/login prompt remains residual; no review-attached photo or linked-media proof unless separately captured. |
| Parfumo | Targeted rendered/session route for high-value sample; direct HTTP/AJAX is historical/canary. Targeted surface: `parfumo_product_page_chrome_extension_targeted_rendered_session`. | `orca-harness/runners/run_parfumo_mgt_capture.py` | `orca-harness/source_capture/parfumo_projection.py`; runner `run_parfumo_projection.py`; lane `projection_parfumo`. | `orca-harness/cleaning/parfumo.py`; lake writer `orca-harness/cleaning/parfumo_lake.py`. | Targeted latest/high/low review and statement samples only; no full 369-review / 1390-statement corpus; no secret/browser-state export. |
| Basenotes | Residential-proxy CloakBrowser product-page route. Surface: `basenotes_product_page_cloakbrowser_deep_scroll_current_window`. | `orca-harness/runners/run_basenotes_mgt_capture.py` | `orca-harness/source_capture/basenotes_projection.py`; runner `run_basenotes_projection.py`; lane `projection_basenotes`. | `orca-harness/cleaning/basenotes.py`; lake writer `orca-harness/cleaning/basenotes_lake.py`. | Anonymous direct/anti-block/browser routes are Cloudflare-challenged in the observed environment; in-page JSON-LD review subset is not full corpus; `/reviews/` and sentiment sub-URLs remain archive gates. |

## Layer Boundaries

- Raw packet admission, path grammar, derived layout, write boundary, and Silver
  semantics are Data Lake authority. Start at
  `forseti/product/spines/data_lake/README.md` and then open the named authority
  contract for the lake question.
- Projection is mechanical, raw-anchored, and row/residual oriented. It must not
  create demand, credibility, sentiment, or completeness claims.
- Cleaning may normalize and emit audit/Silver records through its own writers.
  It does not repair missing full-corpus coverage or decide Judgment meaning.
- ECR consumes source/projection refs and source-visible/residualized facts only.

## Open First For Common Tasks

| Task | Open |
| --- | --- |
| Reconstruct route diagnosis and pinned evidence | `docs/research/orca_fragrance_native_database_live_probe_v0.md` |
| Continue Fragrantica raw/projection/ECR/Cleaning handoff | `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md` |
| Check Parfumo targeted-sample contract | `docs/workflows/parfumo_targeted_capture_contract_v0.md` |
| Inspect actual runner source_family/source_surface strings | `run_*_mgt_capture.py` for the named source, then the matching projection helper |
| Check lake layout/admission/Silver rules | `forseti/product/spines/data_lake/README.md` -> `authority/` |

## Non-Claims

Not live capture authorization, validation, readiness, fixture admission,
complete database coverage, full review/statement corpus proof, ECR readiness,
Cleaning readiness, Judgment, demand proof, buyer proof, legal advice, or
commercial-readiness evidence.
