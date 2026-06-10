# Daimler Advisory 001 Browser Source Body Capture DSU-001 to DSU-003 Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Browser-enabled current official source-body capture receipt for DAIMLER_ADVISORY_001 DSU-001 through DSU-003. One bounded pass only; no evidence-unit extraction.
use_when:
  - Checking whether DSU-001 through DSU-003 current official PDF bodies were locally preserved after the prior 403-only capture pass.
  - Deciding whether a future source-body extraction pass may use the locally preserved current PDF bodies with explicit version-identity limits.
  - Preventing current-body preservation from being promoted into pre-cutoff version identity, buyer proof, or judgment-quality evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md
  - docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md
  - docs/research/daimler_advisory_001_source_registry_v0.md
input_hashes:
  docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md: sha256:6591A94AFC65620B8BE6DAAEFFA9B8703F603DD849AFA431F1DE466056BD1C84
  docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md: sha256:36E02BBB06676ED3CA668D91CB5725DC54E23CD34B8105018F05BE67A87C362D
  docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_001_provenance_official_legal_core_adversarial_review_v0.md: sha256:74A80F8071C942873123BDA6659F7654C1D9B6E14CA6B0376C175A316D50F4F7
stale_if:
  - A pre-cutoff archive body is found for DSU-001, DSU-002, or DSU-003.
  - Mercedes-Benz Group current official PDF bodies change after the hashes recorded here.
  - A later receipt proves or rejects pre-cutoff version identity for any captured current body.
  - The Daimler source registry is updated for DSU-001 through DSU-003.
downstream_consumers:
  - Future Daimler current-body extraction pass, if separately authorized.
  - Future Daimler source-registry reconciliation pass.
```

Status: `DAIMLER_ADVISORY_001_BROWSER_SOURCE_BODY_CAPTURE_DSU_001_003_RECEIPT_V0`.

Scope boundary: this artifact records one bounded browser-enabled source-body capture pass for DSU-001, DSU-002, and DSU-003. It captures current official PDF bodies only. It does not attempt DSU-004 or later registry units, does not extract evidence units, does not update the source registry, and does not change Daimler's claim-tier state.

## Start Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write plus per-operation approved browser escalation
  target_scope: DAIMLER_ADVISORY_001 DSU-001 through DSU-003 browser-enabled current source-body capture receipt.
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md
preflight_notes:
  target_receipt_path_preexisted: no
  compaction_before_browser_source_attempt: yes
  precompact_source_outputs_used_as_authority: no
  prior_capture_receipt_status: current official PDF direct fetches and no-header curl returned HTTP 403; no source bodies captured
  current_task_boundary: browser-enabled body access attempt only
  worktree_state: dirty; target browser_attempts and source_bodies folders untracked
  forbidden_methods_not_used:
    - anti-detect browsers
    - proxies
    - commercial fetch services
    - credentials
    - paid APIs
```

## Source List

| DSU | Title | Current official URL |
| --- | --- | --- |
| `DSU-001` | Daimler Annual Meeting 2019 invitation / agenda | `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-agenda-2019.pdf` |
| `DSU-002` | Daimler Annual Meeting 2019 hive-down and acquisition agreement | `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownagreement-2019.pdf?r=dai` |
| `DSU-003` | Daimler AM 2019 hive-down report / Ausgliederungsbericht | `https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownreport-2019.pdf` |

## Capture Method Summary

| Step | Method | Result |
| --- | --- | --- |
| Browser runtime check | Bundled Node runtime plus `playwright-core` | `playwright-core` was usable; bundled Chromium executable was missing. |
| Headless installed Chrome | Local Chrome executable through Playwright, temporary profile | Browser launched after per-operation escalation, but all three URLs returned `403 Access Denied`; no source bodies. |
| Visible installed Chrome page render | Local Chrome executable through Playwright, temporary profile | All three current official PDFs rendered in Chrome PDF viewer. |
| Visible installed Chrome response body save | `response.body()` after PDF viewer render | Produced 536-byte Chrome PDF-viewer HTML shells, not PDF bodies. These were quarantined as invalid viewer shells. |
| Direct Chrome-header fetch | `Invoke-WebRequest` with ordinary Chrome 148 user agent and PDF accept headers | Returned HTTP 403 for all three after escalation; no files promoted. |
| Visible installed Chrome PDF-viewer download button | Clicked the built-in viewer download button and saved Playwright download bytes | Succeeded for all three DSUs. Saved bodies begin with `%PDF` and have SHA256 hashes below. |

## Captured Current Official PDF Bodies

These are current official PDF bodies captured on 2026-06-02 from Mercedes-Benz Group URLs through visible local Chrome. They are not pre-cutoff archive bodies.

| DSU | Local path | Size bytes | SHA256 | Magic |
| --- | --- | ---: | --- | --- |
| `DSU-001` | `docs/research/daimler_advisory_001/source_bodies/dsu_001_agenda_current_visible_chrome_download_20260602.pdf` | 2689478 | `AD2DD0669EBE1DBB5BFD7BA725FF811206F11F8E7EE49B87F623D27FD4C5A843` | `%PDF` |
| `DSU-002` | `docs/research/daimler_advisory_001/source_bodies/dsu_002_hivedownagreement_current_visible_chrome_download_20260602.pdf` | 1330478 | `88ADB707844353D2064ADBE98C28288199FF3109C85645B5E8F008EB80E3B379` | `%PDF` |
| `DSU-003` | `docs/research/daimler_advisory_001/source_bodies/dsu_003_hivedownreport_current_visible_chrome_download_20260602.pdf` | 4121124 | `E8D1C83D829A6926AF75D0C1EF122110F56631795770244F3E4B10F63FE52A55` | `%PDF` |

Observed browser download metadata:

| DSU | HTTP status | Content type | Suggested filename |
| --- | ---: | --- | --- |
| `DSU-001` | 200 | `application/pdf` | `daimler-ir-am-agenda-2019.pdf` |
| `DSU-002` | 200 | `application/pdf` | `daimler-ir-am-hivedownagreement-2019.pdf` |
| `DSU-003` | 200 | `application/pdf` | `daimler-ir-am-hivedownreport-2019.pdf` |

## Preserved Browser Attempt Evidence

| Artifact class | Local path or folder | Meaning |
| --- | --- | --- |
| Headless 403 screenshots | `docs/research/daimler_advisory_001/browser_attempts/dsu-001_browser_attempt_20260602.png`; `docs/research/daimler_advisory_001/browser_attempts/dsu-002_browser_attempt_20260602.png`; `docs/research/daimler_advisory_001/browser_attempts/dsu-003_browser_attempt_20260602.png` | Shows ordinary headless Chrome received access-denied pages. |
| Visible Chrome pre-download screenshots | `docs/research/daimler_advisory_001/browser_attempts/dsu-001_visible_chrome_before_download_20260602.png`; `docs/research/daimler_advisory_001/browser_attempts/dsu-002_visible_chrome_before_download_20260602.png`; `docs/research/daimler_advisory_001/browser_attempts/dsu-003_visible_chrome_before_download_20260602.png` | Shows visible Chrome rendered the PDF viewer before download. |
| Invalid viewer shells | `docs/research/daimler_advisory_001/browser_attempts/invalid_viewer_shells/` | Contains three 536-byte HTML viewer shells moved out of `source_bodies`; these are not counted as source bodies. |
| Direct header-fetch quarantine | `docs/research/daimler_advisory_001/browser_attempts/chrome_header_fetch_quarantine/` | Created for guarded direct fetches; no files were promoted because escalated direct fetches returned 403. |

## Version Identity and Extraction Gate

This pass clears the local current-body preservation gap for DSU-001 through DSU-003. It does not clear pre-cutoff version identity.

| DSU | Current body preservation | Pre-cutoff version identity | Extraction posture |
| --- | --- | --- | --- |
| `DSU-001` | `captured_current_official_body` | `not_proven` | `candidate_current_body_available_version_identity_unproven` |
| `DSU-002` | `captured_current_official_body` | `not_proven` | `candidate_current_body_available_version_identity_unproven` |
| `DSU-003` | `captured_current_official_body` | `not_proven` | `candidate_current_body_available_version_identity_unproven` |

The prior source-body receipt found no pre-cutoff Archive.org mementos for tested URL forms and recorded post-cutoff CDX metadata only. This receipt does not change that archive result. A future extraction pass may use these current bodies only if it keeps the pre-cutoff identity gap visible or separately obtains stronger identity evidence.

## Decision Delta

Delta from `docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md`:

- Changed: DSU-001 through DSU-003 current official PDF bodies are now locally preserved with SHA256 hashes.
- Changed: direct body-access failure is narrower than the prior receipt stated; visible Chrome plus viewer download can retrieve the current bodies.
- Not changed: no pre-cutoff archive body has been found.
- Not changed: pre-cutoff version identity remains unproven.
- Not changed: Daimler claim-tier state remains `no durable evidence` unless a separate run/output receipt supersedes it.
- Not changed: no evidence-unit extraction, scoring, fixture admission, registry update, or buyer-facing proof is authorized by this receipt.

## Non-Claims

This artifact does not claim:

- evidence-unit extraction for any DSU.
- pre-cutoff version identity for any captured current PDF body.
- that the captured current PDF bodies are identical to the PDF bodies available before the 2019-05-21 cutoff.
- participant packet readiness.
- buyer proof.
- validation.
- scoring.
- fixture admission.
- Judgment Spine validation.
- judgment-quality evidence.
- a Daimler model run.
- a Daimler claim-tier change from `no durable evidence`.
- a registry update.
- any ECR, Cleaning, Judgment, schema, or code work.
- a source-access method-plan amendment.
- commercial readiness.
- that direct fetches with other permitted browser/manual methods must fail.
- that no pre-cutoff archives exist beyond the URL forms and date ranges queried in the prior receipt.

## Stop Receipt

```yaml
route_step_stop: BROWSER_SOURCE_BODY_CAPTURE_PASS_DSU_001_TO_DSU_003
receipt_path: docs/research/daimler_advisory_001_browser_source_body_capture_dsu_001_003_receipt_v0.md
source_bodies_folder: docs/research/daimler_advisory_001/source_bodies/
source_bodies_captured: 3
sha256_values_computed: 3
scope_completed:
  - preflight reads and prior receipt hash verification
  - target path collision check
  - browser runtime check
  - headless installed Chrome attempt
  - visible installed Chrome render attempt
  - invalid PDF-viewer shell quarantine
  - direct Chrome-header fetch attempt
  - visible Chrome PDF-viewer download capture for DSU-001 through DSU-003
  - local PDF magic-byte, size, and SHA256 readback
not_completed_in_this_pass:
  - pre-cutoff archive body discovery
  - pre-cutoff version identity proof
  - evidence-unit extraction
  - participant packet rebuild
  - model run
  - scoring
  - registry update
  - claim-tier change from no durable evidence
compaction_before_artifact_write: yes
```
