---
retrieval_header_version: 1
artifact_role: Cross-lane redirect/handoff prompt (LinkedIn lane). NOT product authority; not a build authorization.
scope: >
  Redirects the dormant LinkedIn discovery lane to scope a complementary
  company-level headcount AGGREGATE forward-trend capture (the net-adds
  realization signal the org-motion judgment backtest needs), distinct from the
  lane's people-discovery posture and within its privacy rails.
use_when:
  - Handing the LinkedIn lane the company-headcount-aggregate need.
authority_boundary: retrieval_only
stale_if:
  - The LinkedIn lane scopes or declines the capability (this becomes historical).
  - The net-adds source-family decision changes.
---

# LinkedIn Lane - Redirect: company headcount-aggregate forward trend (for org-motion net-adds)

**Context.** The org-motion judgment backtest (judgment spine, Beauty Pie #3) needs a LinkedIn
signal your lane doesn't currently produce, and your lane is built differently (people-discovery),
so this is a **redirect / scope request**, not a handoff of our capture.

**What we need.** A **company-level headcount AGGREGATE, captured forward as a trend**: per target
company, periodic snapshots of `numberOfEmployees` (the company page's JSON-LD integer), company
size band (e.g. "51-200"), and follower **count** (a single integer - not a follower list). A time
series of these = **net headcount adds**, the *realization* signal for org-motion (the
ATS/Greenhouse board gives hiring *intent* / gross postings only; net adds needs a headcount
source). It also calibrates the postings->net "haircut."

**Why it's in scope (and within your rails).** This is **market-level company aggregate** - single
company-level numbers - **not** individuals, **not** follower/connection lists, **not** graphs,
**not** profile/post content. It builds no person's dossier or row, so it doesn't touch your
public-actor-basis / no-individual-lists hard stops.

**The one real difference from your posture.** Your lane is *no-live, planning-only*; a forward
headcount *trend* requires **periodic live snapshots** of the company page - the live/attended
posture, not the planning-only discovery path. Flag whether it extends your live layer or belongs
as a sibling company-aggregate slice.

**Backtest caveat (don't over-promise).** Past-case backtests can't use this (LinkedIn company
pages are sparsely archived pre-~2024); it's a **go-forward** signal. For past UK cases the
backtestable net-adds proxy is Companies House annual employee count; US private cos have no
equivalent (US public -> SEC EDGAR).

**Ask.** Scope this as a company-aggregate forward-capture capability (problem + goal above): own
it as a slice, or route it. **Spec/scope only - not a build authorization.** Don't duplicate our
org-motion capture; just produce the headcount-trend signal we can consume.
