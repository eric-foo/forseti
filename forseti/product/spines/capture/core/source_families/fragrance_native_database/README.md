# Capture Source Family: Fragrance Native Database

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family lane index
scope: >
  Cold-start lane index for fragrance-native database capture routes:
  Fragrantica, Parfumo, and Basenotes. Ties source-access route evidence,
  packet runners, canonical content extraction, Data Lake, ECR, and Cleaning seams
  without re-owning downstream layer contracts.
use_when:
  - Starting Fragrantica, Parfumo, or Basenotes capture-to-lake work.
  - Checking whether a fragrance-native database source should be treated as retail/PDP.
  - Finding the first runner, content extractor, or Cleaning lake writer for a fragrance-native database packet.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_fragrance_native_database_live_probe_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
  - forseti/product/spines/data_lake/README.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - Fragrantica, Parfumo, or Basenotes route posture changes.
  - A fragrance-native database runner, content extractor, or Cleaning lake writer changes source_family/source_surface requirements.
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

Their derived source-classification view carries both
`evidence_shapes: [reference_record, review]`. `reference_record` covers the
source-visible product identity and attributes already retained in
`fragrance_product_snapshot` rows; `review` covers rated/community text.
`reference_record` does not promote either source to merchant, official, or
canonical-product authority.

## Route Map

| Source | Access route / source surface | Packet runner | Content extraction | Cleaning / Silver seam | Residuals to preserve |
| --- | --- | --- | --- | --- | --- |
| Fragrantica | One raw direct-HTTP canary plus content CloakBrowser initial-viewport and deep-scroll current-window packets. | `forseti-harness/runners/run_fragrantica_mgt_capture.py`. | Family extractor in `forseti-harness/source_capture/fragrantica_projection.py`; current captures persist canonical `content_record.json`, while raw packets are historical inputs only. | `forseti-harness/cleaning/fragrantica.py`; lake writer `forseti-harness/cleaning/fragrantica_lake.py`; Cleaning validates and adapts content records directly. | Current-window review capture only; full archive/login prompt remains residual. Active capture may retain a triggered screenshot; successful content extraction hashes then discards DOM/text. |
| Parfumo | Targeted rendered/session route for a bounded high-value review sample; direct HTTP/AJAX is historical/canary. | `forseti-harness/runners/run_parfumo_mgt_capture.py`; the targeted route retains its receipt and any supplied screenshot. | Family extractor in `forseti-harness/source_capture/parfumo_projection.py`; content is canonical and raw is historical compatibility. | `forseti-harness/cleaning/parfumo.py`; lake writer `forseti-harness/cleaning/parfumo_lake.py`; Cleaning owns source-row validation and adaptation. | Latest/high/low review and statement samples only; no full 369-review / 1390-statement corpus; no secret/browser-state export. |
| Basenotes | User-cleared persistent Chrome public-page export. | `forseti-harness/runners/run_basenotes_mgt_capture.py`. | Family extractor in `forseti-harness/source_capture/basenotes_projection.py`; current captures persist canonical content only. | `forseti-harness/cleaning/basenotes.py`; lake writer `forseti-harness/cleaning/basenotes_lake.py`; Cleaning consumes content without rereading discarded DOM/text. | Exact URL, challenge-free DOM/text, and product-detail sufficiency remain fail-closed access proof; a screenshot is never access proof. |

## Basenotes Persistent-Chrome Bundle Contract

The current route is persistent-Chrome and fails closed. In manual mode, the user
opens the exact public product URL in a visible tab and personally completes any
Cloudflare verification before a supported controller exports the three required
public-page artifacts below and, only for a named visual-evidence trigger, the
optional screenshot. Direct existing-Chrome mode creates the same bundle
from the local CDP session and admits it only after observing the exact final URL,
challenge-free source content, and sufficient product/review detail:

- `browser_rendered_dom.html`
- `browser_visible_text.txt`
- `browser_snapshot_metadata.json`
- optional `browser_viewport_screenshot.png`

The optional screenshot requires one explicit trigger:
`route_baseline`, `visual_content`, `access_or_overlay_diagnostic`, or
`owner_requested`. A supplied screenshot without its trigger, or a trigger
without a screenshot, is rejected. Direct CDP does not invoke screenshot capture
when no trigger is supplied. Screenshots are source-media evidence, not proof that
Cloudflare was cleared.

Existing-bundle publication accepts either a human-assisted manual bundle or a
bundle previously generated by direct CDP preflight. Both bundle origins bind the
exact requested/final URL and state `headless: false`,
`persistent_user_session: true`, `cookies_exported: false`,
`credentials_exported: false`, and `proxy_used: false`, plus a non-blank browser
channel and ISO-8601 capture timestamp. Manual metadata requires
`human_cleared_access_gate: true`. Direct metadata records
`human_cleared_access_gate: false` and
`access_readiness_basis: observed_exact_url_challenge_free_sufficient_content`.
The runner rejects challenge text, fewer than 500 visible-text bytes, a missing
caller-bound product path, missing Product/review/reviewBody JSON-LD markers,
symlinks, empty/oversized files, invalid supplied screenshots, missing required
files, trigger mismatches, or unexpected files before packet publication.

The route supports current `content` retention and explicit historical `raw`
retention. Successful content extraction hashes and discards rendered DOM/text,
retains browser metadata, `content_record.json`, and
`content_extraction_metadata.json`, and retains a screenshot only when
intentionally triggered. Extraction failure preserves all supplied artifacts and
exits `4`. Parser qualification is an explicit scratch workflow; it never admits
a sample packet to the lake.

```text
python forseti-harness/runners/run_basenotes_mgt_capture.py \
  --url https://basenotes.com/fragrances/<product> \
  --bundle-directory <three-file-export-with-optional-triggered-screenshot> \
  --output-root <empty-summary-directory> \
  --data-root <forseti-data-root>
```

Direct mode is explicit and loopback-only:

```text
python forseti-harness/runners/run_basenotes_mgt_capture.py \
  --url https://basenotes.com/fragrances/<product> \
  --bundle-directory <fresh-generated-bundle> \
  --output-root <empty-summary-directory> \
  --data-root <forseti-data-root> \
  --cdp-endpoint http://127.0.0.1:9222
```

For append-only publication workflows, direct preflight deliberately performs the
live capture but does not publish a packet:

```text
python forseti-harness/runners/run_basenotes_mgt_capture.py \
  --url https://basenotes.com/fragrances/<product> \
  --bundle-directory <fresh-generated-bundle> \
  --output-root <empty-preflight-output-directory> \
  --cdp-endpoint http://127.0.0.1:9222 \
  --preflight-only
```

After inspecting that validated bundle and confirming publication conditions,
publish the same bundle with the manual-form command above, omitting
`--cdp-endpoint`. The summary distinguishes `bundle_origin_transport` from
`capture_transport` and `capture_performed_this_run`, so a later publication run
does not claim that it performed the earlier CDP capture.

Direct mode attaches to the existing headed browser and determines access from the
observed page rather than a manual readiness assertion. It uses no proxy or
storage-state input, preserves no cookies, credentials, auth state, or profile
bytes, and leaves the operator-owned browser running after detaching. Capture/export
can run unattended while the session continues to yield challenge-free sufficient
content. The runner does not launch a Chrome process, automate the access gate,
claim long-term unattended reliability, or turn the historical proxy route into a
fallback.
## Layer Boundaries

- Raw packet admission, path grammar, derived layout, write boundary, and Silver
  semantics are Data Lake authority. Start at
  `forseti/product/spines/data_lake/README.md` and then open the named authority
  contract for the lake question.
- Canonical content extraction is mechanical, source-anchored, and
  row/residual oriented. Cleaning owns current row validation and adaptation.
  Neither layer may create demand, credibility, sentiment, or completeness
  claims.
- For the Parfumo targeted and Basenotes persistent-Chrome content routes,
  "raw-anchored" means the immutable raw
  packet container: rows bind to JSON pointers in its preserved content record,
  whose capture metadata retains the hashes and byte counts of discarded
  rendered DOM and visible text. Raw and legacy packets retain preserved-file
  anchors.
- Cleaning may normalize and emit audit/Silver records through its own writers.
  It does not repair missing full-corpus coverage or decide Judgment meaning.
- ECR consumes source/content refs and source-visible/residualized facts only.

## Open First For Common Tasks

| Task | Open |
| --- | --- |
| Reconstruct route diagnosis and pinned evidence | `docs/research/orca_fragrance_native_database_live_probe_v0.md` |
| Check current Capture-to-Cleaning ownership | `forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` |
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
