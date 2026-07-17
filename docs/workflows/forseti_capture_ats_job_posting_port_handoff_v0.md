# ATS Job-Posting Capture Port — Plan-First Implementation Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Commissions a plan-first port of ATS job-posting capture mechanics (from the
  jb workspace's curated-jobs-v2 lane, as reference only) into forseti-harness
  source_capture as a new commission-bounded source family for the
  job-posting-residue lens. Phase 0 returns a plan for owner adjudication;
  implementation is authorized only after that plan is adjudicated.
use_when:
  - Dispatching the ATS port lane.
  - Adjudicating the returned Phase 0 plan or the Phase 1 implementation.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/product_lead/gtm/forseti_gtm_silent_pain_taxonomy_v0.md
stale_if:
  - Phase 1 lands and is adjudicated (packet consumed).
  - The owner reverses any ruling recorded below.
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-18 Asia/Singapore
- `created_by_lane`: Tower 28 CI/GTM lane, from an Opus subagent evaluation of
  the jb ATS setup (chat, 2026-07-18); provenance only, not authority
- `load_rule`: confirm-don't-trust; re-verify every jb claim below by direct
  read before relying on it
- `jb boundary (hard)`: everything under `C:\Users\vmon7\Desktop\projects\jb`
  is READ-ONLY reference. jb is never Forseti authority (AGENTS.md, Forseti
  Routing). Port mechanics as new Python in forseti-harness; record provenance
  in the plan document, not in code comments.

## Owner rulings (2026-07-18, binding)

1. **Plan first.** Phase 0 produces a plan; no implementation, no adapter
   code, no registry file before the owner adjudicates that plan.
2. **Capture-only first slice.** The capture layer preserves postings; it
   never ranks, filters by relevance, classifies roles, or infers pains.
   The residue-to-pain reading is a later downstream lens over `derived/`
   rows — out of this handoff's scope entirely.
3. **Ashby scan authorized.** A bounded, read-only access-posture scan of
   Ashby's public job-board endpoint (jb-scan style: endpoint shape, auth
   posture, response fields, polite-access verdict) is authorized inside
   Phase 0. Scan only — the Ashby adapter itself is Phase 1.
4. **Workday is in scope for v1** (alongside Greenhouse, Lever, Ashby).
5. **Registry seeding undecided.** The plan must present both options —
   manual per-company entries vs agent-assisted careers-page sniffing — with
   build effort and per-run toll for each; the owner picks at plan review.
6. **Study jb's geography and job-filter mechanics before porting.** The
   plan must examine how jb gates geography (the US market gate) and how its
   filtering actually works in the running system — including the lower
   workflow on the n8n canvas (the post-adapter shared-spine side: CW1/CW2
   routing and the Workflow-B recheck), not just the adapter exports — and
   state what, if anything, ports. Constraint: any ported scoping must stay
   mechanical and commission-declared (e.g., a location field extracted
   verbatim; a commission that names its geographic bound); anything that
   smells like relevance filtering or classification stays downstream, per
   ruling 2.

## Phase 0 — Plan (return for owner adjudication)

The plan covers, at minimum:

- **Adapter designs** for Greenhouse, Lever, Workday, Ashby (post-scan):
  endpoint, request shape, pagination, fields captured, failure kinds —
  following the existing `forseti-harness/source_capture/adapters/`
  pattern (`direct_http.py` is the exemplar: stdlib fetch, frozen dataclass
  result, honest failure kinds). Reference endpoints from the jb evaluation:
  Greenhouse `GET boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true`;
  Lever `GET api.lever.co/v0/postings/{token}?mode=json`; Workday
  `POST /wday/cxs/{tenant}/{site}/jobs` plus per-job detail; Ashby from the
  Phase 0 scan. Verify each against the jb sources before design.
- **jb mechanics review** per ruling 6, with the port/no-port verdict per
  mechanism and the reason.
- **Registry shape and seeding** per ruling 5: a versioned reference file in
  the repo (`{company, ats_vendor, board_token|tenant+site, careers_url,
  resolved_at, confidence}`), captured data in the lake, never config in the
  lake.
- **Storage and projection contract**: verbatim ATS JSON preserved as
  SourceCapturePackets in `raw/`; one mechanical projection into `derived/`
  (`company, title, description, posted_date, source_url, ats_vendor,
  ats_job_id, captured_at`); description depth (full text vs truncation)
  stated and justified; no medallion folder names (the lake contract forbids
  literal bronze/silver directories).
- **Run mechanics**: commission-bounded (target list + as-of date), per-company
  typed discharge state (met / partial / blocked / unavailable_by_source),
  polite rate limits (jb used 1.5-2s for Workday), honest UA, no scheduler,
  no standing crawler.
- **Validation approach** for Phase 1: selftest shape plus one bounded smoke
  capture against 2-3 real public boards, named in the plan.
- **Effort order** and what v1 excludes.

## Phase 1 — Implement (only after plan adjudication)

Implement exactly the adjudicated plan in forseti-harness. Any discovered
deviation returns to the owner as a plan amendment, not a silent change.
Validation runs before the lane reports done; jb remains untouched.

## Reference pointers (verify by direct read; jb read-only)

- jb route card: `jb\curated-jobs-v2\README.md`; lane decomposition:
  `decisions\curated_jobs_v2_ats_lane_decomposition_v1.md`; endpoint
  research: `decisions\curated_jobs_v2_q1b_ats_us_fetch_research_v1.md`;
  Lever scan: `adapters\scans\curated_jobs_v2_lever_public_surface_scan_v1.md`;
  adapter/spine field contract:
  `decisions\curated_jobs_v2_common_post_adapter_spine_interface_contract_v1.md`.
  Note: jb's load-bearing routing wrappers live only in the n8n database, not
  git (`runtime\README.md`) — ruling 6's review must account for that.
- Forseti: `forseti-harness/source_capture/adapters/direct_http.py`
  (exemplar); capture operating model and lake physicality contract in
  `open_next`.

## Drift Guard

- No classification, ranking, or pain inference anywhere in capture (ruling 2).
- No standing crawler or scheduler; dated point-in-time snapshots only;
  re-observation is a new commission.
- Public, unauthenticated surfaces only; honor each surface's access posture;
  bot-blocks return typed gaps, never workarounds.
- No new spine: this is a source family inside the existing Capture spine.
- jb untouched, cited as provenance only.

## Success signal

Phase 0: a plan the owner can adjudicate in one pass, with the registry
decision framed for a single ruling and every jb-derived claim re-verified.
Phase 1: capture-only adapters and projection matching the adjudicated plan,
validation green, and a bounded smoke capture demonstrating dated snapshots
for at least two ATS vendors on real beauty-brand boards.
