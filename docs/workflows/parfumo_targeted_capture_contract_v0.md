# Parfumo Targeted Capture Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow contract
scope: Target contract for the Parfumo fragrance-native capture lane after full-corpus capture was downgraded.
use_when:
  - Building or reviewing Parfumo capture packet shape.
  - Checking whether Parfumo implementation has drifted back to full-corpus capture.
  - Distinguishing Parfumo source-visible rating buckets from Fragrantica vote buckets.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_fragrance_native_database_live_probe_v0.md
  - docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
stale_if:
  - Parfumo Chrome-extension/user-visible route stops reaching real product DOM.
  - Direct HTTP/AJAX becomes reliably reachable again and is explicitly reselected.
  - The owner re-authorizes full 369-review / 1390-statement exhaustion as the target.
```

## Contract

Parfumo v0 targets a bounded, high-value product-page sample, not full corpus exhaustion.

Required capture shape:

- product context: rendered DOM and visible text as projector inputs, optional screenshot as source media evidence, route receipt as access provenance, and aggregate counts visible in the captured surface.
- review samples: latest/recent reviews first, plus source-visible high-rating and low-rating buckets only where Parfumo exposes the underlying rating/order/filter fields.
- statement samples: latest/recent statements first; do not infer rating buckets for statements unless the source exposes such fields.
- residuals: preserve declared corpus counts as context and explicitly residualize uncaptured review and statement corpus depth.

The current primary route is `chrome_extension_user_visible_rendered_session`. Direct HTTP/AJAX is only a canary/fallback in the current environment.

## Source Surface

Use `parfumo_product_page_chrome_extension_targeted_rendered_session` for local
packets that preserve operator-visible Chrome rendered artifacts for this
targeted sample route. The stable route ID is historical; the local bundle may
come from an extension or a retained extension-free Chrome CDP session when the
receipt names the actual transport.

The packet writer may package local rendered artifacts and fixtures without live network access. Live Parfumo capture remains owner-authorized per operation.

## Capture Artifact Modes

The pinned targeted-rendered route defaults to `content` mode:

- `content`: project in flight; preserve `content_record.json`, the route
  receipt, capture plan, content-capture metadata, and any supplied screenshot;
  hash and discard rendered DOM and visible text after projection succeeds.
- `sample`: preserve the same content record plus rendered DOM and visible text
  so `run_parfumo_parser_fit_check.py` can re-project and require an exact
  `match`.
- `raw`: preserve the pre-flip local-artifact packet shape and do not run the
  content projector.

`content_capture_metadata.json` is the provenance floor for discarded projector
inputs: mode, parser version, projection status, and each input role's filename,
SHA-256, byte count, and preservation state. A projector failure is loud: all
supplied artifacts are preserved as fallback and the runner exits `4`.

The screenshot is not a discardable projector input. When supplied, it remains
preserved in every mode because it is source media evidence. The route receipt
and capture plan also remain preserved because they establish access and capture
scope rather than page-content payload.

Projection and Cleaning prefer a valid content record and bind rows to its
packet-local JSON pointers. Raw and legacy packets retain the existing raw
projection path. The shared projection runner therefore remains available for
raw, legacy, and direct-HTTP canary packets; only its standard use for the pinned
targeted route retires.

## Non-Goals

- No full 369-review / 1390-statement exhaustion.
- No Basenotes work.
- No cookie, storage state, Cloudflare clearance, proxy endpoint, or exit-IP export.
- No CAPTCHA solving service, stealth/fingerprint tooling, retry storm, or anti-bot escalation in code.
- No Silver writes from raw writer; Silver remains through `append_silver_record`.
- No Fragrantica rating-scale inheritance. Operator shorthand such as 1/4/5 star must map only to Parfumo source-visible values.

## Batch 1 Acceptance

Batch 1 is complete when fixture/local rendered artifacts can be packaged into a Parfumo source-capture packet with:

- source_family `fragrance_native_database`;
- source_surface `parfumo_product_page_chrome_extension_targeted_rendered_session`;
- separate source slices for product context, latest/recent reviews, source-visible high-rating reviews, source-visible low-rating reviews, and latest/recent statements;
- summary non-claims that explicitly deny full-corpus capture and browser-secret export;
- a guard that rejects obvious cookie/storage/Cloudflare-token strings in supplied text artifacts.

The original Batch 1 packet-shape acceptance remains historical. The current
targeted route adds capture-time content projection without changing the bounded
sample, secret-export, Silver-write, or full-corpus boundaries above.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The pinned Parfumo targeted-rendered route now defaults to hybrid content mode while retaining route provenance and supplied screenshots."
  trigger: product_doctrine
  related_triggers: [output_authority]
  controlling_sources_updated:
    - docs/workflows/parfumo_targeted_capture_contract_v0.md
    - forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md
    - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/capture/core/source_capture_toolbox/content_mode_lane_flip_handoff_v0.md
    - forseti-harness/runners/run_parfumo_mgt_capture.py
    - forseti-harness/source_capture/parfumo_projection.py
    - forseti-harness/cleaning/parfumo_lake.py
    - forseti-harness/runners/run_parfumo_cleaning_catchup.py
  intentionally_not_updated:
    - {path: AGENTS.md, reason: "No project-wide authorization, isolation, landing, or safety rule changed."}
    - {path: .agents/workflow-overlay, reason: "Source hierarchy, validation, review, and lifecycle mechanics are unchanged."}
    - {path: docs/workflows/forseti_repo_map_v0.md, reason: "No artifact family, owner, or retrieval route moved."}
    - {path: forseti-harness/source_capture/content_capture.py, reason: "The HTTP ContentCaptureSpec seam is unchanged; the pinned local-artifact route remains family-owned."}
  stale_language_search: 'rg -n "projection is Batch [2]|Parfumo: first Phase B flip \\(HTTP seam drop[-]in\\)|NEAREST DROP[-]IN" docs/workflows/parfumo_targeted_capture_contract_v0.md forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md forseti/product/spines/capture/core/source_capture_toolbox'
  non_claims:
    - not live-route validation
    - not full Parfumo family retirement
    - not corpus completeness
```
