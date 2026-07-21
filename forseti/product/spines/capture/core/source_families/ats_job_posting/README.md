# ATS Job-Posting Capture Source Family

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family index (routing home for ats_job_posting)
scope: >
  Landed capture-to-lake route for the ats_job_posting source family: capture-only,
  point-in-time snapshots of public ATS job boards (Greenhouse, Lever, Workday,
  Ashby) preserved verbatim in the Data Lake, plus one mechanical projection to
  derived rows. Names the adapter, runner, projection, registry, and plan; does not
  restate lake/ECR/Cleaning contracts.
use_when:
  - Capturing, re-capturing, or projecting a public ATS job board already in the registry.
  - Adding a newly resolved board (manual registry seeding, D1).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/ats_job_posting/ats_board_registry_v0.md
  - docs/workflows/forseti_capture_ats_job_posting_port_plan_v0.md
  - forseti/product/spines/capture/core/source_families/README.md
stale_if:
  - The adapter, runner, or projection changes materially.
  - A new ATS vendor lands, or the registry schema changes.
```

## What this family is

Capture-only (Capture spine, ruling 2): FETCH a public ATS board verbatim, preserve
it in `raw/`, and project one derived row per posting. It never ranks, filters by
relevance, classifies roles, gates by geography, or infers pains — a posting carries
only verbatim source facts plus the vendor's verbatim structured country where one is
exposed (Lever `country`, Ashby `address.postalAddress.addressCountry`, Workday
`country.descriptor`/`alpha2Code`). Re-capture is a new commissioned run (a fresh dated
snapshot); there is no scheduler or standing crawler.

## Routing

| Seam | Path |
| --- | --- |
| Adapter (fetch + parse, 4 vendors) | `forseti-harness/source_capture/adapters/ats_job_posting.py` |
| Runner (one packet per board snapshot) | `forseti-harness/runners/run_source_capture_ats_job_posting_packet.py` |
| Projection (derived rows) | `forseti-harness/source_capture/ats_job_posting_projection.py` |
| Board registry (manual, config-in-Git) | `ats_board_registry_v0.md` (this folder) |
| Plan (adjudicated Phase 0/1) | `docs/workflows/forseti_capture_ats_job_posting_port_plan_v0.md` |

The operator reads a registry row and passes its coordinates as runner flags; the
runner does not parse the registry.

## Current posture

Greenhouse and Ashby are live-proven end-to-end (Glossier/ILIA beauty boards on
Greenhouse; Ashby on a non-beauty board). Lever and Workday are contract-tested (no
live smoke against a real beauty board yet). A beauty-brand board for a second vendor
awaits manual registry seeding. Hardened via a cross-vendor delegated review-patch.

## Non-Claims

Not source-access permission, live-network authorization, validation, readiness,
fixture admission, lake/ECR/Cleaning authority, Judgment, ranking, relevance,
classification, geographic gating, scale proof, standing-capture authorization, or
board/route completeness.
