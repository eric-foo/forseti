# Retail/PDP Sidecar Operator Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Product operator playbook
scope: >
  Bounded operator procedure for running Retail/PDP CloakBrowser packet capture
  with the opt-in local projection sidecar for Amazon, Sephora, and Ulta.
use_when:
  - Running or rechecking the Retail/PDP capture-to-projection sidecar smoke.
  - Handing Amazon, Sephora, or Ulta raw packet/projection outputs to review or merge lanes.
  - Checking which sidecar behaviors should be code-enforced before broadening automation.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
  - forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
  - forseti-harness/source_capture/retail_pdp_projection.py
stale_if:
  - The Retail/PDP projection sidecar flag or output shape changes.
  - The canonical Amazon, Sephora, or Ulta smoke targets or capture flags change.
  - Retail/PDP projection row kinds, residual vocabulary, or binding posture changes.
  - Sidecar behavior is promoted into a generic registry, cadence runner, or packet writer.
```

## Status

Status: `OPERATOR_PLAYBOOK_V0`.

This is operator guidance over implemented runners. It is not source discovery,
not a new capture method, not validation proof, not fixture admission, not ECR,
not Cleaning, not Judgment, and not merge approval.

## Preconditions

- Work from `forseti-harness/`.
- Use only bounded, already supplied or repo-visible Retail/PDP URLs. Do not
  search for replacement targets during this smoke.
- Keep outputs under ignored scratch:
  `_test_runs/retail_pdp_sidecar_smoke_<YYYYMMDD>/<retailer>/`.
- Run one capture per retailer at human-rate. Do not retry-loop a retailer.
- Stop on auth walls, CAPTCHA, Cloudflare challenges, or private/entitled gates.
- If CloakBrowser/Playwright fails with a local subprocess permission error
  such as `WinError 5`, rerun the same bounded command with the required local
  tool approval. Do not classify that as a retailer access result.

## Canonical Smoke Targets

| Retailer | URL | Required flags | Expected projection posture |
| --- | --- | --- | --- |
| Sephora | `https://www.sephora.com/product/lip-sleeping-mask-P420652` | `--settle-seconds 5 --scroll-step-px 350 --scroll-passes 1` | ProductPage DOM price, Bazaarvoice config, target review widget. A visible `sephora_ld_json_review_count_differs_from_target_dom` residual is acceptable when JSON-LD and target DOM review counts disagree. |
| Ulta | `https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2645443` | `--settle-seconds 5 --scroll-passes 1` | JSON-LD plus `window.__APOLLO_STATE__`, with requested SKU matching projected SKU. |
| Amazon | `https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK` | `--settle-seconds 4 --delivery-zip 10001 --delivery-zip-setup-timeout-seconds 30` | ASIN, DOM target price input, review nodes, and a packet limitation confirming declared ZIP `10001` when the US storefront pin succeeds. |

## Command Pattern

Each command must include:

- `--source-family retail_pdp`;
- `--retail-pdp-projection-output <path>`;
- an output path under the ignored smoke root;
- a capture context that says this is bounded Retail/PDP sidecar smoke and not
  ECR, Cleaning, Judgment, or source discovery.

Successful sidecar output prints two lines:

1. the packet directory path;
2. the projection JSON path argument.

### Sephora

```powershell
python runners/run_source_capture_cloakbrowser_packet.py `
  --url https://www.sephora.com/product/lip-sleeping-mask-P420652 `
  --source-family retail_pdp `
  --source-surface cloakbrowser_snapshot `
  --decision-question "Retail/PDP sidecar smoke: what source-visible product, offer, and review facts were present for Sephora Laneige Lip Sleeping Mask?" `
  --output _test_runs/retail_pdp_sidecar_smoke_YYYYMMDD/sephora/packet `
  --capture-context "bounded Retail/PDP sidecar smoke capture for Sephora public PDP; no ECR, Cleaning, Judgment, or source discovery" `
  --timeout-seconds 70 `
  --settle-seconds 5 `
  --scroll-step-px 350 `
  --scroll-passes 1 `
  --retail-pdp-projection-output _test_runs/retail_pdp_sidecar_smoke_YYYYMMDD/sephora/retail_pdp_projection.json
```

### Ulta

```powershell
python runners/run_source_capture_cloakbrowser_packet.py `
  --url "https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2645443" `
  --source-family retail_pdp `
  --source-surface cloakbrowser_snapshot `
  --decision-question "Retail/PDP sidecar smoke: what source-visible product, offer, and review facts were present for Ulta Night Shift Overnight Lip Mask?" `
  --output _test_runs/retail_pdp_sidecar_smoke_YYYYMMDD/ulta/packet `
  --capture-context "bounded Retail/PDP sidecar smoke capture for Ulta public PDP; no ECR, Cleaning, Judgment, or source discovery" `
  --timeout-seconds 70 `
  --settle-seconds 5 `
  --scroll-passes 1 `
  --retail-pdp-projection-output _test_runs/retail_pdp_sidecar_smoke_YYYYMMDD/ulta/retail_pdp_projection.json
```

### Amazon

```powershell
python runners/run_source_capture_cloakbrowser_packet.py `
  --url https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK `
  --source-family retail_pdp `
  --source-surface cloakbrowser_snapshot `
  --decision-question "Retail/PDP sidecar smoke: what source-visible product, offer, and review facts were present for Amazon Laneige Lip Sleeping Mask with US storefront pin?" `
  --output _test_runs/retail_pdp_sidecar_smoke_YYYYMMDD/amazon/packet `
  --capture-context "bounded Retail/PDP sidecar smoke capture for Amazon public PDP with declared US delivery ZIP 10001; no ECR, Cleaning, Judgment, source discovery, proxy, or credential use" `
  --timeout-seconds 80 `
  --settle-seconds 4 `
  --delivery-zip 10001 `
  --delivery-zip-setup-timeout-seconds 30 `
  --retail-pdp-projection-output _test_runs/retail_pdp_sidecar_smoke_YYYYMMDD/amazon/retail_pdp_projection.json
```

## Inspection Contract

For each projection, inspect at least:

- `projection_method`;
- `loss_ledger.structure_preserved`;
- top-level `residuals`;
- row kinds present;
- `retail_variant_offer.source_visible_fields`;
- `retail_review_substrate.source_visible_fields`;
- packet `warnings` and `limitations`.

Expected healthy smoke shape:

- `projection_method` is `retail_pdp_mechanical_projection`;
- `structure_preserved` is `true`;
- residuals are visible and interpreted as gaps, not failures;
- packet/projection files remain under `_test_runs/` unless a separate fixture
  admission decision authorizes promotion.

Observed 2026-06-16/17 sidecar smoke on this lane:

| Retailer | Structure | Residuals | Notes |
| --- | --- | --- | --- |
| Sephora | `true` | `sephora_ld_json_review_count_differs_from_target_dom` | DOM target review count and JSON-LD review count differed; residual preserved. |
| Ulta | `true` | none | JSON-LD and Apollo fields agreed for the matching SKU target. |
| Amazon | `true` | none | Packet limitation confirmed declared ZIP `10001` via `currencyOfPreference=USD`; requested URL landed with `?th=1`. |

## Failure Taxonomy

| Symptom | Classification | Operator response |
| --- | --- | --- |
| `WinError 5` / local subprocess permission before browser launch | Local tool/sandbox permission failure | Rerun the same bounded command with the required local approval; do not change retailer URL or flags. |
| Capture command exits non-zero before packet path prints | Capture/access failure | Preserve the stderr text and stop for that retailer unless a new fact justifies one bounded re-probe. |
| Packet writes but projection fails | Sidecar/projection failure | Treat the packet as preserved scratch evidence; inspect projection error against `retail_pdp_projection.py` and tests before changing code. |
| Auth wall, CAPTCHA, Cloudflare challenge, or private account gate | Access-control stop | Stop and report visible limitation. Do not bypass or solve the gate. |
| Projection residual appears | Honest projection gap | Report it. Do not clean, hide, or reinterpret it as a failure. |

## Merge-Conflict Posture

PR lanes touching Retail/PDP projection may conflict in:

- `forseti/product/spines/capture/core/source_capture_toolbox/README.md`;
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`;
- `forseti-harness/source_capture/retail_pdp_projection.py`;
- `forseti-harness/tests/unit/test_retail_pdp_projection.py`.

For a docs-only lane, do not resolve code conflicts by guessing. A later
merge-conflict lane should preserve both:

- main-branch projection/parser/test improvements; and
- this branch's opt-in sidecar contract, tests, and operator playbook pointers.

After code conflict resolution, rerun the focused tests named in the PR and one
bounded sidecar smoke if the projection parser behavior changed.

## Code-Enforceable Follow-Up Flags

Do not implement these in a docs-only turn. They are candidates because they are
mechanically enforceable and would reduce agent variance:

1. **Retail/PDP sidecar smoke runner.** Add a small runner or subcommand that
   executes the three canonical retailer commands, writes to a date-stamped
   `_test_runs/retail_pdp_sidecar_smoke_<YYYYMMDD>/` root, and emits a compact
   JSON summary. This would enforce target URLs, flags, output shape, and
   no-discovery behavior.
2. **Projection summary output.** Add an optional read-only summary writer for
   sidecar runs that records retailer, packet id, projection path,
   `structure_preserved`, row kinds, residuals, warnings, and limitations.
3. **Smoke profile validation.** If a dedicated runner exists, enforce
   retailer-specific required flags such as Sephora progressive scroll and
   Amazon `--delivery-zip 10001` rather than relying on operator memory.
4. **PR readiness check.** Add a lightweight CI or PR-body checker only if the
   team wants ready-for-review Retail/PDP PRs to include sidecar smoke evidence.
   Keep it advisory unless the owner explicitly wants it as a merge gate.

Already enforced by code in the current sidecar:

- `--retail-pdp-projection-output` requires `--source-family retail_pdp`;
- projection runs only after packet write returns success;
- projection failure exits non-zero and does not alter the packet schema;
- packet writer remains projection-unaware.
