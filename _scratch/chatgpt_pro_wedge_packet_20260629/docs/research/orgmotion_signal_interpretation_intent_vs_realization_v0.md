---
retrieval_header_version: 1
artifact_role: Research method note (org-motion signal interpretation; NOT product authority, NOT a capture spec)
scope: >
  How to read the org-motion signal for judgment backtests: hiring INTENT
  (ATS/postings, gross) vs REALIZATION (headcount, net adds), the net-adds
  preference, the intent->net haircut, and where each datum comes from. Feeds
  packet construction (what the WITH arm may claim) and the capture spine's
  source-family priorities.
use_when:
  - Constructing an org-motion WITH-arm (deciding what the signal claims).
  - Specifying or prioritizing org-motion capture sources.
authority_boundary: retrieval_only
open_next:
  - docs/research/orgmotion_demand_signal_wedge_discovery_v0.md
  - docs/research/orgmotion_beautypie_capture_feasibility_v0.md
stale_if:
  - A capture spec ratifies different source-family semantics.
  - Empirical fill/backfill rates land and replace the placeholder haircut.
---

# Org-Motion Signal Interpretation - Intent vs Realization (v0)

## The core distinction

- **Hiring INTENT (gross).** Source: the public ATS board (Greenhouse / Lever /
  Ashby) - dated job postings, departments, seniority. Archive-backtestable
  <=cutoff. Tells you what a company is *trying* to staff. It is NOT realized
  headcount.
- **Hiring REALIZATION (net adds).** Source: a headcount *level* over time -
  LinkedIn company page `numberOfEmployees` / size band / follower count (a
  company-level aggregate), or Companies House annual average-employee-count
  (UK). A trend of these = NET adds.

**Net adds is the preferred read** (owner, 2026-06-11): a *filled* role is not
growth if it is a backfill (headcount stays flat). Gross postings overstate
expansion.

## The intent -> net haircut

ATS postings are intent; to estimate realized NET adds from them, discount by:

- a **fill rate** - not every req is filled; some are frozen or cancelled after a
  funding crunch or reorg; some are evergreen / pipeline posts (rarer at a
  mid-size brand than at a big company); and
- a **backfill rate** - filled-but-replacing-a-departure = no net add.

Calibrating the haircut requires realized-headcount data (LinkedIn / CH) to
compare gross postings against actual net deltas across companies. Until that
lands, use a **conservative placeholder haircut** and label the WITH-arm signal
as *"hiring intent in functions X, base-rate-discounted,"* never *"they added N
people."*

## Where the data lives (and the geographic asymmetry)

| Signal | Source | Backtestable <=cutoff? |
| --- | --- | --- |
| Intent (gross postings) | public ATS board (archived) | Yes |
| Net adds (headcount) - UK | Companies House annual employee count | Yes (annual, coarse) |
| Net adds (headcount) - any | LinkedIn company aggregate | Forward/live only (sparse archives pre-~2024) |
| Net adds - US public | SEC EDGAR (10-K employee count) | Yes |
| Net adds - US private | (no public registry) | No - lean on LinkedIn-live / third-party |

So UK private companies have a backtestable net-adds proxy (CH); **US private
companies do not** (no Companies-House equivalent; state filings carry no
headcount) - a known coverage gap, deferred.

## Boundary

Method / semantics only. Not a capture spec (the capture spine owns adapters and
priorities) and not product authority. For an N=1 pilot the ATS-intent-only read
(haircut-discounted) is the honest ceiling until a realization source is captured.
