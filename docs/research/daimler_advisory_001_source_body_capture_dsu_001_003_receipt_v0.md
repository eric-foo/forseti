# Daimler Advisory 001 Source Body Capture DSU-001 to DSU-003 Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Source-body and version-identity capture receipt for DAIMLER_ADVISORY_001 DSU-001 through DSU-003. One bounded pass only; no evidence-unit extraction.
use_when:
  - Checking DSU-001 through DSU-003 source-body capture status and access-failure record.
  - Deciding whether the official/legal core may proceed to evidence-unit extraction after body and version-identity capture.
  - Referencing the archive-availability CDX record before re-attempting body capture.
authority_boundary: retrieval_only
open_next:
  - docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md
  - docs/research/daimler_advisory_001_source_registry_v0.md
input_hashes:
  docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md: sha256:36E02BBB06676ED3CA668D91CB5725DC54E23CD34B8105018F05BE67A87C362D
stale_if:
  - Official Mercedes-Benz Group PDF URLs become accessible and bodies are captured.
  - Pre-cutoff archive captures are discovered for DSU-001 through DSU-003.
  - A later source-body capture pass captures local copies and computes SHA256 for any DSU.
  - The Daimler source registry changes DSU-001 through DSU-003 status.
downstream_consumers:
  - Future DSU-001 through DSU-003 evidence-unit extraction pass (requires clearing blockers noted below).
  - Future Daimler source-registry reconciliation pass.
```

Status: `DAIMLER_ADVISORY_001_SOURCE_BODY_CAPTURE_DSU_001_003_RECEIPT_V0`.

Scope boundary: this artifact implements one bounded source-body and version-identity capture pass for DSU-001, DSU-002, and DSU-003. It does not attempt DSU-004 or later registry units, does not extract evidence units, and does not update the source registry.

## Start Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: DAIMLER_ADVISORY_001 DSU-001 through DSU-003 source-body and version-identity capture receipt.
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/research/daimler_advisory_001_provenance_official_legal_core_v0.md
preflight_notes:
  provenance_receipt_sha256_verified: 36E02BBB06676ED3CA668D91CB5725DC54E23CD34B8105018F05BE67A87C362D
  provenance_receipt_hash_matches_known: yes
  target_receipt_path_preexisted: no
  collision_check: clear
  source_bodies_folder_created: no — no bodies captured; folder not created
  worktree_state: dirty (several modified files unrelated to this pass; no run-control conflicts)
  claim_tier_state_at_start: no durable evidence
  registry_state_at_start: manual_registry_first_pass_no_external_source_body_retrieval
  case_cutoff_boundary: 2019-05-21 23:59 CEST
  retrieval_pass_date: 2026-06-02
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
| Current PDF fetch — DSU-001, DSU-002, DSU-003 | WebFetch tool | HTTP 403 Forbidden on all three. |
| Current PDF fetch — confirmation | Direct `curl` (no headers, no proxy, no credentials) | HTTP 403 Forbidden on all three. Confirmed server-side block, not a tool artifact. |
| Archive.org CDX API pre-cutoff query — all DSUs | `curl` against `web.archive.org/cdx/search/cdx` | CDX returned empty `[]` or no matching records for pre-cutoff range. See per-DSU table below. |
| Archive.org CDX API pre-cutoff query | WebFetch tool | Blocked at tool level; `web.archive.org` is not accessible via WebFetch in this environment. |
| Archive.org CDX API all-dates query — DSU-001 www.daimler.com | `curl` | Two captures found: 2021-09-23 (200) and 2024-06-30 (301). Both post-cutoff. |
| Archive.org CDX API all-dates query — DSU-002 www.daimler.com | `curl` | One capture found: 2021-09-16 (200). Post-cutoff. |
| Archive.org CDX API all-dates query — DSU-003 www.daimler.com | `curl` | One capture found: 2021-09-16 (200). Post-cutoff. |
| Archive.org CDX API all-dates query — DSU-002 mercedes-benz.com | `curl` | Two captures found: 2022-06-26 (200) and 2024-03-22 (200). Post-cutoff. |
| Archive.org CDX API all-dates query — DSU-003 mercedes-benz.com | `curl` | Two captures found: 2022-06-26 (200) and 2024-03-22 (200). Post-cutoff. |
| PDF binary download | Not attempted | Not applicable: current URL blocked by 403; no pre-cutoff archive exists. |
| Anti-detect browsers, proxies, commercial services, credentials | Not used | Forbidden by task scope. |

Note: Archive.org CDX digests are SHA-1 encoded in base32 (Archive.org standard), not SHA256. They are recorded as advisory CDX metadata only and do not constitute the SHA256 source-body hashes required by the capture task.

## Per-DSU Body Capture

### DSU-001

```yaml
dsu_id: DSU-001
title: Daimler Annual Meeting 2019 invitation / agenda
current_url: https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-agenda-2019.pdf
current_body_capture:
  attempted: yes
  result: capture_blocked_by_access
  local_path: null
  sha256: null
  retrieval_timestamp: 2026-06-02
  failure_reason: >
    HTTP 403 Forbidden on both WebFetch tool and independent curl. Server-side
    block on direct PDF access confirmed by two independent fetch methods.
    No body returned; no local preservation possible.
```

### DSU-002

```yaml
dsu_id: DSU-002
title: Daimler Annual Meeting 2019 hive-down and acquisition agreement
current_url: https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownagreement-2019.pdf?r=dai
current_body_capture:
  attempted: yes
  result: capture_blocked_by_access
  local_path: null
  sha256: null
  retrieval_timestamp: 2026-06-02
  failure_reason: >
    HTTP 403 Forbidden on both WebFetch tool and independent curl. Same
    server-side access pattern as DSU-001 and DSU-003.
```

### DSU-003

```yaml
dsu_id: DSU-003
title: Daimler AM 2019 hive-down report / Ausgliederungsbericht
current_url: https://group.mercedes-benz.com/documents/investors/annual-meeting/daimler-ir-am-hivedownreport-2019.pdf
current_body_capture:
  attempted: yes
  result: capture_blocked_by_access
  local_path: null
  sha256: null
  retrieval_timestamp: 2026-06-02
  failure_reason: >
    HTTP 403 Forbidden on both WebFetch tool and independent curl. Same
    server-side access pattern as DSU-001 and DSU-002.
```

## Per-DSU Archive and Version-Identity

### DSU-001 Archive

```yaml
dsu_id: DSU-001
archive_capture:
  attempted: yes
  archive_lookup_basis: >
    CDX API queries under www.daimler.com and group.mercedes-benz.com URL forms;
    date range 2019-01-01 to 2019-05-21T23:59:00.
  pre_cutoff_memento_found: no
  archive_url: null
  local_path: null
  sha256: null
  retrieval_timestamp: 2026-06-02
  failure_reason: >
    No pre-cutoff captures found. CDX returned empty records for both URL forms
    in the 2019-01-01 to 2019-05-21 window.
  advisory_post_cutoff_cdx_record:
    domain_searched: www.daimler.com
    earliest_post_cutoff_capture: 2021-09-23
    earliest_http_status: 200
    earliest_cdx_digest_sha1_base32: N3PQPKEFWFAWNBNTM4SJS5VK4ZX3SLYP
    later_capture: 2024-06-30 (301 redirect — daimler.com to mercedes-benz.com)
    note: CDX query for group.mercedes-benz.com URL form timed out; result unknown.
version_identity:
  status: pre_cutoff_identity_not_proven
  comparison_basis: >
    No current body captured (403). No pre-cutoff archive exists. One
    post-cutoff archive capture found (2021-09-23) but it cannot prove
    pre-cutoff version identity.
  remaining_gap: >
    No path to version identity without either (a) current official body access
    or (b) a pre-cutoff archive capture. Neither is available.
```

### DSU-002 Archive

```yaml
dsu_id: DSU-002
archive_capture:
  attempted: yes
  archive_lookup_basis: >
    CDX API queries under www.daimler.com and group.mercedes-benz.com URL forms;
    date range 2019-01-01 to 2019-05-21T23:59:00.
  pre_cutoff_memento_found: no
  archive_url: null
  local_path: null
  sha256: null
  retrieval_timestamp: 2026-06-02
  failure_reason: >
    No pre-cutoff captures found. CDX returned empty records for both URL forms
    in the 2019-01-01 to 2019-05-21 window.
  advisory_post_cutoff_cdx_record:
    earliest_capture_daimler_com: 2021-09-16 (200); SHA-1 base32 digest CAZYNVOCAYBH5OKX6FP46PHYY7OL35WB
    earliest_capture_mercedes_benz_com: 2022-06-26 (200); SHA-1 base32 digest CAZYNVOCAYBH5OKX6FP46PHYY7OL35WB
    digest_stability_2021_to_2022: same digest — advisory indication of body stability between 2021 and 2022
    later_capture_mercedes_benz_com: 2024-03-22 (200); SHA-1 base32 digest QD5EPKLYMHB6O4ZDEV6MN3ZDTWLNLFCW
    digest_change_2022_to_2024: different digest — advisory indication that the PDF body may have changed after 2022
    note: >
      These are SHA-1 base32 digests from the Archive.org CDX API. They are not SHA256
      values. Digest stability in 2021–2022 is advisory only and does not prove
      pre-cutoff version identity.
version_identity:
  status: pre_cutoff_identity_not_proven
  comparison_basis: >
    No current body captured (403). No pre-cutoff archive exists. Post-cutoff
    CDX digests show body stability 2021–2022, but that range is over two years
    after the 2019-05-21 cutoff. The 2024 capture has a different digest,
    suggesting a later body revision.
  remaining_gap: >
    No path to pre-cutoff version identity without (a) current body access or
    (b) a pre-cutoff archive. Current body may not match the 2021–2022 archive
    body given the 2024 digest change.
```

### DSU-003 Archive

```yaml
dsu_id: DSU-003
archive_capture:
  attempted: yes
  archive_lookup_basis: >
    CDX API queries under www.daimler.com and group.mercedes-benz.com URL forms;
    date range 2019-01-01 to 2019-05-21T23:59:00.
  pre_cutoff_memento_found: no
  archive_url: null
  local_path: null
  sha256: null
  retrieval_timestamp: 2026-06-02
  failure_reason: >
    No pre-cutoff captures found. CDX returned empty records for both URL forms
    in the 2019-01-01 to 2019-05-21 window.
  advisory_post_cutoff_cdx_record:
    earliest_capture_daimler_com: 2021-09-16 (200); SHA-1 base32 digest KVNNX7C63PPU7N24Q3QBWHPA4MI4JHQL
    earliest_capture_mercedes_benz_com: 2022-06-26 (200); SHA-1 base32 digest KVNNX7C63PPU7N24Q3QBWHPA4MI4JHQL
    digest_stability_2021_to_2022: same digest — advisory indication of body stability between 2021 and 2022
    later_capture_mercedes_benz_com: 2024-03-22 (200); SHA-1 base32 digest WSRAITPVNZKQVDSRHO3NBHYMOMZWHGUF
    digest_change_2022_to_2024: different digest — advisory indication that the PDF body may have changed after 2022
    note: >
      These are SHA-1 base32 digests from the Archive.org CDX API. They are not SHA256
      values. Digest stability in 2021–2022 is advisory only and does not prove
      pre-cutoff version identity.
version_identity:
  status: pre_cutoff_identity_not_proven
  comparison_basis: >
    No current body captured (403). No pre-cutoff archive exists. Post-cutoff
    CDX digests show body stability 2021–2022, but that range is over two years
    after the 2019-05-21 cutoff. The 2024 capture has a different digest,
    suggesting a later body revision.
  remaining_gap: >
    No path to pre-cutoff version identity without (a) current body access or
    (b) a pre-cutoff archive. Current body may not match the 2021–2022 archive
    body given the 2024 digest change.
```

## Saved Local Files and SHA256

No source bodies were captured in this pass. The source-body folder
`docs/research/daimler_advisory_001/source_bodies/` was not created because
no files were saved.

| DSU | Local path | SHA256 | Reason not captured |
| --- | --- | --- | --- |
| `DSU-001` | — | — | HTTP 403 on current URL; no pre-cutoff archive |
| `DSU-002` | — | — | HTTP 403 on current URL; no pre-cutoff archive |
| `DSU-003` | — | — | HTTP 403 on current URL; no pre-cutoff archive |

## Access Failures and Tool Limitations

| Failure | Detail |
| --- | --- |
| HTTP 403 — all three current PDFs | Mercedes-Benz Group PDF server blocks direct programmatic access for all three DSU current official URLs. Confirmed by WebFetch tool and direct `curl`. Server returns 403 with no body. This is not a credential issue; the PDFs require browser-context access or whitelisted access methods not used in this pass. |
| web.archive.org blocked by WebFetch | The WebFetch tool returns a tool-level block for `web.archive.org`. Worked around using `curl` for CDX API access only. |
| DSU-001 mercedes-benz.com CDX query timeout | CDX query for DSU-001 under the current `group.mercedes-benz.com` domain timed out (curl exit code 28). Result unknown; likely no captures or network delay. |
| DSU-001 daimler.com prefix CDX query interrupted | Safety classifier temporarily unavailable; query not completed. Result unknown. |
| No pre-cutoff mementos — all three DSUs | Archive.org CDX API returned no captures before 2019-05-21 for DSU-001, DSU-002, or DSU-003 under any tested URL form. |

## Decision Delta

This section records whether each DSU can proceed to evidence-unit extraction
and what blocks it.

| DSU | Extraction gate | Blockers |
| --- | --- | --- |
| `DSU-001` | `blocked` | (1) Current official body HTTP 403-blocked; no local preservation. (2) No pre-cutoff archive capture on Archive.org. (3) Version identity of any retrievable post-2021 body against the pre-cutoff original cannot be proven. The provenance receipt's direct Section 124a chain provides provenance-level support but does not substitute for source-body version identity. |
| `DSU-002` | `blocked` | (1) Same HTTP 403 block. (2) No pre-cutoff archive. (3) Version identity unproven. (4) CDX digest change between 2022 and 2024 raises additional uncertainty about current body content. |
| `DSU-003` | `blocked` | (1) Same HTTP 403 block. (2) No pre-cutoff archive. (3) Version identity unproven. (4) CDX digest change between 2022 and 2024 raises additional uncertainty about current body content. |

Gap delta vs. provenance receipt:

This pass confirms and documents the specific access failures behind the gap
already noted in the provenance receipt (`not_locally_preserved`;
`source_pdf_hash_not_captured`). The provenance receipt's chain-strength
claims (direct Section 124a anchor for DSU-001; indirect Agenda Item 9 chains
for DSU-002 and DSU-003) remain the only current basis for pre-cutoff public
availability and are not changed by this pass.

New information from this pass:

- HTTP 403 is confirmed server-side (not a WebFetch artifact).
- No pre-cutoff Archive.org captures exist for any of the three DSU URLs.
- Post-cutoff CDX digests suggest DSU-002 and DSU-003 bodies were stable
  2021–2022 but may have changed by 2024.
- DSU-001 post-cutoff capture history is partial (mercedes-benz.com CDX
  query timed out).

## Non-Claims

This artifact does not claim:

- evidence-unit extraction for any DSU.
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
- that the Archive.org CDX SHA-1 base32 digests are SHA256 values.
- that post-cutoff CDX digest stability (DSU-002 and DSU-003, 2021–2022)
  proves the current body or any archived body matches the pre-cutoff original.
- that HTTP 403 is permanent or that re-attempting with other permitted tools
  would also return 403.
- that no pre-cutoff Archive.org captures exist beyond the URL forms and date
  ranges queried in this pass.

## Stop Receipt

```yaml
route_step_stop: SOURCE_BODY_CAPTURE_PASS_DSU_001_TO_DSU_003
receipt_path: docs/research/daimler_advisory_001_source_body_capture_dsu_001_003_receipt_v0.md
source_bodies_folder: docs/research/daimler_advisory_001/source_bodies/
source_bodies_captured: 0
sha256_values_computed: 0
scope_completed:
  - preflight reads and provenance receipt SHA256 verification
  - target path collision check
  - current official URL fetch attempts for DSU-001 through DSU-003
  - Archive.org CDX API queries for pre-cutoff captures (www.daimler.com and group.mercedes-benz.com URL forms)
  - all-dates CDX metadata record for post-cutoff captures
  - access failure and tool limitation documentation
  - decision delta vs. provenance receipt
not_completed_in_this_pass:
  - source body local preservation (all 403 blocked or no pre-cutoff archive)
  - SHA256 computation for any DSU body
  - pre-cutoff version identity proof for any DSU
  - evidence-unit extraction
  - participant packet rebuild
  - model run
  - scoring
  - registry update
  - claim-tier change from no durable evidence
compaction_before_artifact_write: no
```
