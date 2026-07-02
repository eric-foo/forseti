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

- product context: rendered DOM, visible text, optional screenshot, route receipt, and aggregate counts visible in the captured surface.
- review samples: latest/recent reviews first, plus source-visible high-rating and low-rating buckets only where Parfumo exposes the underlying rating/order/filter fields.
- statement samples: latest/recent statements first; do not infer rating buckets for statements unless the source exposes such fields.
- residuals: preserve declared corpus counts as context and explicitly residualize uncaptured review and statement corpus depth.

The current primary route is `chrome_extension_user_visible_rendered_session`. Direct HTTP/AJAX is only a canary/fallback in the current environment.

## Source Surface

Use `parfumo_product_page_chrome_extension_targeted_rendered_session` for local packets that preserve operator-visible Chrome-extension rendered artifacts for this targeted sample route.

The packet writer may package local rendered artifacts and fixtures without live network access. Live Parfumo capture remains owner-authorized per operation and is outside Batch 1.

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

Projection, Cleaning, Silver MetricObservation promotion, and live route execution are later batches.
