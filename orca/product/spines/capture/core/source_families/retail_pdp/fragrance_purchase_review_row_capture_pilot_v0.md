# Fragrance Purchase-Review Row Capture Pilot v0

```yaml
retrieval_header_version: 1
artifact_role: Capture row-corpus receipt / packet-window pilot
scope: Records the first packet-local candidate review-row corpus extracted from the five locked fragrance purchase-review fixtures.
use_when:
  - Checking whether row capture has been performed for the five locked fragrance retailer fixtures.
  - Finding the ignored local JSONL row-corpus artifact and its validation summary.
  - Preserving row-count and residual context without committing verbatim review bodies.
authority_boundary: retrieval_only; no Attachment Record storage, ECR, Cleaning, Judgment, pain/pleasure labeling, integrity scoring, or source-wide corpus authority.
open_next:
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md
stale_if:
  - The ignored row-corpus artifact is regenerated.
  - Any locked fixture, packet path, row contract, or source route changes.
  - This packet-window receipt is used as current full fixture coverage after the widget expansion probe.
  - Durable Attachment Record physicalization is authorized.
```

## Decision

The first row-capture pilot is complete for the five locked fragrance purchase-
review fixtures. The corpus is packet-local and lives under ignored test output,
because it contains verbatim customer-review bodies.

Raw row artifact:

`orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/row_corpus/candidate_fragrance_review_rows_v0.jsonl`

Summary artifact:

`orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/row_corpus/candidate_fragrance_review_rows_v0_summary.json`

Do not promote these rows into tracked source files, Attachment Records, ECR,
Cleaning, Judgment, pain/pleasure labels, or integrity scores without the owning
lane explicitly binding that next step.

## Inputs

| Source | Packet path | Extraction substrate |
| --- | --- | --- |
| Ministry of Scent | `orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/ministry/direct_http_packet` | Static Judge.me DOM rows. |
| Luckyscent / Scent Bar | `orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/luckyscent/cloakbrowser_packet` | Rendered Judge.me DOM rows. |
| Twisted Lily | `orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/twistedlily/cloakbrowser_packet` | Embedded Judge.me widget JSON. |
| ZGO Perfumery | `orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/zgo_known_reviewed/direct_http_packet` | Static Yotpo review section. |
| Indigo Perfumery | `orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/indigo_known_review_candidate/cloakbrowser_packet` | Rendered JSON-LD / Judge.me `Review` objects. |

## Row Counts

| Source ID | Rows emitted |
| --- | ---: |
| `fragrance_retail_ministry_of_scent` | 4 |
| `fragrance_retail_luckyscent` | 10 |
| `fragrance_retail_twisted_lily` | 5 |
| `fragrance_retail_zgo` | 1 |
| `fragrance_retail_indigo` | 5 |
| **Total** | **25** |

## Later Widget Probe

This receipt remains the original 25-row packet-window pilot. Later bounded
widget-expansion probes found better current row-completion routes for the
Judge.me fixtures and for ZGO's Yotpo v3 storefront route, but did not rewrite this raw JSONL corpus.

| Source ID | Original emitted rows | Widget fixture total observed later | Current interpretation |
| --- | ---: | ---: | --- |
| `fragrance_retail_ministry_of_scent` | 4 | 4 | Widget route confirms no pagination gain. |
| `fragrance_retail_luckyscent` | 10 | 14 | Widget page 2 exposes 4 missing rows. |
| `fragrance_retail_twisted_lily` | 5 | 6 | Widget page 2 exposes 1 missing row. |
| `fragrance_retail_zgo` | 1 | 1 | Yotpo v3 storefront endpoint now confirms the same 1-row fixture with native id, date, verified flag, rating, aggregate, and media absence diagnostics. |
| `fragrance_retail_indigo` | 5 | 13 | Direct Judge.me widget endpoint supersedes schema-only row completion. |

For current pagination, rating-filter, media-filter, and widget-route posture,
open `fragrance_purchase_review_widget_expansion_probe_v0.md`. Do not treat
the 25-row JSONL as full known fixture coverage after that probe.

## Steps Performed

1. Read the row contract and the five fixture packet manifests.
2. Extracted rows only from packet-preserved material that contained body text.
3. Preserved route, packet id, slice id, capture time, source URL, product binding,
   raw row anchor, body hash, rating/date/reviewer fields where source-visible,
   and per-field residuals.
4. Kept raw review bodies in ignored `_test_runs/` output rather than tracked docs.
5. Validated row count, source count, required fields, schema version, substrate
   counts, and candidate-key uniqueness.

## Validation Read

Fresh validation output after corpus generation:

```text
row_count 25
source_counts {"fragrance_retail_indigo": 5, "fragrance_retail_luckyscent": 10, "fragrance_retail_ministry_of_scent": 4, "fragrance_retail_twisted_lily": 5, "fragrance_retail_zgo": 1}
unique_keys 25
missing_required 0
schema_versions ['candidate_fragrance_review_row_v0']
substrates {"json_ld_judgeme_review_objects": 5, "judge_me_dom_static_html": 4, "judge_me_embedded_json": 5, "judge_me_rendered_dom": 10, "yotpo_static_review_section": 1}
```

`git status --ignored=matching` showed the raw row-corpus output under ignored
`orca-harness/_test_runs/`, so the verbatim corpus is not staged or tracked.

## Residuals

- Packet-window corpus only; not source-wide review coverage.
- No pagination expansion. Twisted Lily emitted the five loaded page-1 Judge.me
  rows while the widget reported six aggregate reviews. Luckyscent emitted the
  ten rendered rows while the aggregate substrate reported fourteen reviews.
- Indigo emitted schema-only rows from rendered JSON-LD / Judge.me review objects;
  visible text still did not expose visible review-row bodies.
- ZGO emitted one static Yotpo-section row with date absent in the original packet-window corpus; later Yotpo v3 probing recovered the native review id and created datetime for the same 1-row fixture.
- No pain/pleasure labeling, sentiment, review-integrity score, dedupe,
  reviewer identity resolution, product normalization, or buyer-proof claim.
