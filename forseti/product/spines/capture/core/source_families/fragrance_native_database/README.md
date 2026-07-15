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
| Basenotes | User-cleared persistent Chrome public-page export. Surface: `basenotes_product_page_user_cleared_persistent_chrome_current_window`. | `forseti-harness/runners/run_basenotes_mgt_capture.py` | `forseti-harness/source_capture/basenotes_projection.py`; runner `run_basenotes_projection.py`; lane `projection_basenotes`. | `forseti-harness/cleaning/basenotes.py`; lake writer `forseti-harness/cleaning/basenotes_lake.py`. | Fresh anonymous direct, no-proxy CloakBrowser, fresh headed-Chrome, and same-cleared-profile headless-Chrome contexts are Cloudflare-challenged. A separate direct headed CloakBrowser attempt remained in the human-verification loop after the user checked the box, so no cleared CloakBrowser state existed for a valid headless-reuse test. The user-visible persistent Chrome session requires a user-completed gate and exports no cookie, credential, or profile data. In-page JSON-LD review subset is not full corpus; `/reviews/` and sentiment sub-URLs remain archive gates. |

## Basenotes Persistent-Chrome Bundle Contract

The current route is operator-assisted and fails closed. The user opens the exact
public product URL in a visible persistent Chrome tab and personally completes any
Cloudflare verification. A supported browser controller then exports exactly these
public-page artifacts, with no extra files:

- `browser_rendered_dom.html`
- `browser_visible_text.txt`
- `browser_viewport_screenshot.png`
- `browser_snapshot_metadata.json`

Metadata must bind the exact requested/final URL and state `headless: false`,
`persistent_user_session: true`, `human_cleared_access_gate: true`,
`cookies_exported: false`, `credentials_exported: false`, and `proxy_used: false`,
plus a non-blank browser channel and ISO-8601 capture timestamp. The runner rejects
challenge text, fewer than 500 visible-text bytes, a missing caller-bound product
path, missing Product/review/reviewBody JSON-LD markers, symlinks, empty/oversized
files, non-PNG screenshots, missing files, or unexpected files before packet
publication.

```text
python forseti-harness/runners/run_basenotes_mgt_capture.py \
  --url https://basenotes.com/fragrances/<product> \
  --bundle-directory <four-file-export> \
  --output-root <empty-summary-directory> \
  --data-root <forseti-data-root>
```

The runner validates and publishes the export; it does not launch Chrome, inspect
or export browser state, automate the access gate, claim unattended reliability,
or turn the historical proxy route into a fallback.
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
## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Basenotes user-cleared persistent Chrome public-page export replaces the
    inoperable CloakBrowser plus reddit-res-01 executable default; the exact
    source surface, projection admission, Cleaning partition, and producer
    versions now bind the proven user-assisted route while the proxy observation
    remains historical evidence only.
  trigger: product_doctrine
  related_triggers: [output_authority, validation_philosophy]
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md
    - docs/research/orca_fragrance_native_database_live_probe_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/safety-rules.md
    - docs/workflows/forseti_repo_map_v0.md
    - forseti-harness/runners/run_basenotes_mgt_capture.py
    - forseti-harness/data_lake/inventory.py
    - forseti-harness/data_lake/lake_touchpoint_inventory_v0.json
    - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
    - forseti-harness/tests/contract/test_data_lake_inventory_gate.py
    - forseti-harness/source_capture/basenotes_projection.py
    - forseti-harness/cleaning/basenotes.py
    - forseti-harness/cleaning/basenotes_lake.py
    - forseti-harness/runners/run_basenotes_cleaning_catchup.py
    - forseti-harness/runners/run_fragrantica_cleaning_catchup.py
    - forseti-harness/runners/run_parfumo_cleaning_catchup.py
    - forseti-harness/data_lake/lane_registry.py
    - forseti-harness/tests/contract/test_cleaning_family_surface_partition.py
    - forseti-harness/tests/contract/test_policy_module_version_pins.py
  intentionally_not_updated:
    - {path: AGENTS.md, reason: "No project-wide capture authorization, lifecycle, safety, or workflow rule changed; the bounded route remains source-family owned."}
    - {path: CLAUDE.md, reason: "The shim continues to import AGENTS.md and must not duplicate a source-family route."}
    - {path: .agents/workflow-overlay, reason: "Source-loading, routing, DCP, validation, and safety mechanics are unchanged."}
    - {path: docs/workflows/forseti_repo_map_v0.md, reason: "No repository route, artifact family, or open-next hierarchy changed."}
    - {path: forseti-harness/data_lake/lane_registry.py, reason: "Projection, Cleaning audit, and Silver lane identifiers and roles are unchanged."}
    - {path: historical Basenotes proxy addendum, reason: "The dated 2026-06-30 observation remains point-in-time evidence and is explicitly superseded only as the executable default."}
  stale_language_search: 'rg -n "basenotes_product_page_cloakbrowser_deep_scroll_current_window|basenotes_native_cloakbrowser_residential_proxy_v0|PROXY_PROFILE_LABEL|reddit-res-01" forseti-harness forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md docs/research/orca_fragrance_native_database_live_probe_v0.md'
  stale_language_search_result: >
    Executed 2026-07-16 after propagation. No retired source-surface, capture-profile,
    or proxy-label constant remains in live harness code or the source-family route
    map. Remaining reddit-res-01 hits are the dated 2026-06-30 historical addendum
    and the 2026-07-16 failure/disposition text that explicitly denies it current
    executable-default status.
  non_claims:
    - not unattended capture proof
    - not headless-route proof
    - not full review-corpus completeness
    - not scale or production readiness
```
