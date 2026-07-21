# ATS Job-Posting Board Registry v0

```yaml
retrieval_header_version: 1
artifact_role: Source-family board registry (curated reference; config-in-Git, not lake data)
scope: >
  Manually curated list of public ATS job boards the ats_job_posting capture
  source family targets. Each row names a company, its ATS vendor, the board
  coordinates the runner needs (Greenhouse/Lever token, Ashby jobBoardName, or
  Workday tenant+server+site), the careers URL it was resolved from, when it was
  resolved, and a confidence marker. This is capture-target CONFIG that lives in
  Git; captured postings live in the Data Lake, never here.
use_when:
  - Selecting which boards a commissioned ats_job_posting capture run targets.
  - Adding a newly resolved beauty-brand board (manual seeding, D1).
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_capture_ats_job_posting_port_plan_v0.md
  - forseti-harness/runners/run_source_capture_ats_job_posting_packet.py
```

## What this is

The adjudicated registry-seeding decision (D1) is **manual**: rows are hand-added
after a human confirms the board from the brand's careers page. There is no
agent-assisted careers-page sniffer in v1 (deferred). The capture runner does not
parse this file — an operator reads a row and passes its coordinates as runner
flags — so the registry stays a plain curated reference with no parser to
maintain.

This registry is **capture config**, not lake data (lake physicality contract):
it lists which public boards to capture; the captured postings are preserved in
the Data Lake under `raw/` and projected into `derived/`. It carries no ranking,
relevance, or role-classification judgment — a board's presence here means only
"this is a public board we may capture," decided by a human, not a relevance
model.

`confidence`:

- `verified_live` — a live GET/POST returned HTTP 200 with a parseable board on
  `resolved_at`.
- `unverified` — added from a careers-page reading but not yet fetched.

## Registry

| company | ats_vendor | board coordinates | careers_url | resolved_at | confidence |
| --- | --- | --- | --- | --- | --- |
| Glossier | greenhouse | `board_token=glossier` | https://boards.greenhouse.io/glossier | 2026-07-18 | verified_live (19 postings) |
| ILIA Beauty | greenhouse | `board_token=ilia` | https://boards.greenhouse.io/ilia | 2026-07-18 | verified_live (23 postings) |
| ThirdLove | greenhouse | `board_token=thirdlove` | https://boards.greenhouse.io/thirdlove | 2026-07-18 | verified_live (22 postings) |
| Grove Collaborative | greenhouse | `board_token=grovecollaborative` | https://boards.greenhouse.io/grovecollaborative | 2026-07-18 | verified_live (9 postings) |

### Awaiting manual seeding (D1)

No Lever, Ashby, or Workday **beauty-brand** board is seeded yet. These vendors'
adapters are implemented and tested (and Ashby is proven live end-to-end against
a non-beauty board — Ramp — during the Phase 1 smoke), but a beauty-brand board
for each awaits the manual discovery step: open the brand's careers page, read
off the vendor + coordinates, add a row. Guessing tokens is not the method.

Coordinate shapes for future rows:

- **Lever:** `board_token=<slug>` (from `jobs.lever.co/<slug>`).
- **Ashby:** `job_board_name=<name>` (from `jobs.ashbyhq.com/<name>`).
- **Workday:** `tenant=<t> wd_server=<wd1|wd5|…> site=<siteId>` (from
  `https://<t>.<wd_server>.myworkdayjobs.com/<site>`).

## Capturing a row

Read a row's coordinates and run the capture (writes into the Data Lake when
`FORSETI_DATA_ROOT` is set, or a local `--output` directory):

```
python forseti-harness/runners/run_source_capture_ats_job_posting_packet.py \
  --vendor greenhouse --company "Glossier" --board-token glossier \
  --decision-question "Which roles is Glossier hiring for as of <date>?" \
  --data-root <FORSETI_DATA_ROOT>
```

Re-capture is a new commissioned run (a fresh dated snapshot), never a standing
crawler or scheduler.
