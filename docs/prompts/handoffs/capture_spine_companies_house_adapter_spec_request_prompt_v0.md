---
retrieval_header_version: 1
artifact_role: Cross-lane spec-request prompt (capture spine). NOT product authority; not a build authorization.
scope: >
  Commissions the capture spine to draft a Companies House adapter spec - the
  cleanest GO net-adds-realization + financial-context + outcome-verification
  source for UK cases (free official API), prioritized #2 in the capture lane's
  own gap spec.
use_when:
  - Handing the capture lane the Companies House adapter spec request.
authority_boundary: retrieval_only
stale_if:
  - The capture lane lands the Companies House spec (this becomes historical).
  - The net-adds source-family decision changes.
---

# Capture Spine - Spec-Draft Request: Companies House adapter (net-adds + financial context)

**Context.** The org-motion judgment backtest needs a REALIZATION signal (net headcount adds +
<=cutoff financial context + outcome verification). Your `archive_org_refinement_and_source_family_gap_spec`
prioritized **Companies House #2** as the cleanest GO (free official API; serves both <=cutoff
context and outcome verification). This commissions the actual adapter spec.

**Problem.** UK companies file annual accounts with Companies House (keyed by company number),
including average employee count and financials, via a free official API. This is the
**backtestable net-adds proxy** (annual, coarse) AND the **outcome-verification** source for UK
cases. The org-motion ATS signal is intent-only; CH provides the realization + financial
corroboration that the WITH-arm and the sealed outcome need. (Beauty Pie's CH accounts already
surfaced the ~212-employee + revenue figures we used to seal that outcome - exactly this data.)

**Goal.** A Companies House adapter spec: fetch filings/accounts by company number; extract
**average employee count** (the net-adds proxy) + key financials; date-bound so it serves both
<=cutoff context (filings before the cutoff) and post-cutoff outcome verification. Honor the
capture doctrine (public official data; market-level).

**Scope note.** UK only. The US-private-company gap (no Companies-House equivalent; SEC EDGAR
covers US *public* only) is explicitly **deferred** per owner direction - not a problem to solve now.

**Deliverable.** A spec draft (problem, goal, API surface, fields extracted, date-bounding,
non-goals, acceptance). **Spec only - not a build authorization.**
