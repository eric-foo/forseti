---
retrieval_header_version: 1
artifact_role: Research feasibility / evidence-gathering record (NOT product authority, NOT a capture-spine artifact)
scope: >
  Gate-0 feasibility finding for the org-motion Topicals case (batch-1 case #4 /
  repeatability "case #2"): whether <=cutoff org-motion evidence is
  archive-backtestable for Topicals' 2021 expansion from DTC into nationwide
  Sephora retail distribution, a preview of the decision-relevant signal, and the
  sealed-outcome recoverability check. Read-only by-hand archive probe; feeds the
  dated ledger amendment and the Phase-4 capture.
use_when:
  - Deciding whether and how to run the org-motion Topicals case.
  - Constructing the Phase-4 org-motion capture (this record says what to re-capture, via the adapter).
  - Auditing the gate-0 feasibility basis and its provenance limits.
authority_boundary: retrieval_only
open_next:
  - docs/research/orgmotion_beautypie_capture_feasibility_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
stale_if:
  - The batch-1 ledger amends case #4, the cutoff, or the org-motion admission.
  - A Phase-4 capture via the adapter supersedes these by-hand feasibility numbers.
  - The pinned scoring key changes.
---

# Org-Motion Topicals -- Gate-0 Capture Feasibility (v0)

## Status & non-claims

DISCOVERY / FEASIBILITY EVIDENCE. Not validation, not a `SourceCapturePacket`,
not an `EvidenceUnit`, not judgment-quality evidence, not a scoring-key change,
not a JSG-01 unfreeze, not live-API authorization. The product-learning cap
holds; N=1. The numbers below come from a **read-only by-hand archive probe**,
NOT a capture-spine capture (see Provenance & limits). This document is written
to be safe for an outcome-blind constructor to read: the post-cutoff outcome is
NOT stated anywhere here.

## Verdict

Gate-0 = **PASS (THIN) via the hiring-composition leg -- the brand's own
careers page, NOT a third-party ATS board.** Topicals' org-motion is
archive-backtestable `<=cutoff` only through the corporate careers page
(`mytopicals.com/pages/careers`), and only as a **single pre-cutoff snapshot**
(2021-03-03) carrying a **single visible role**. There is **no** public ATS
board (Greenhouse / Lever / Ashby / Workable) for Topicals under any tested
slug. The **LinkedIn** headcount-trend leg is **NOT** viable (zero pre-cutoff
company-page coverage). Because the careers leg is a one-snapshot / one-role
point-in-time, this case clears gate-0 only weakly: it supports a
*cutoff-proximate composition read*, not a multi-point hiring *trajectory*.

## Case frame

- Case: batch-1 #4 / repeatability "case #2" -- **Topicals** (DTC skincare,
  founded 2020 by Olamide Olowe and Claudia Teng; DTC launch 2020-08-07, online
  + Nordstrom) expands from direct-to-consumer into **Sephora retail
  distribution** at ~month 9 of brand life.
- Decision / announcement: the Sephora expansion went **public ~2021-03-23 ..
  2021-03-29** (earliest broad press: Refinery29 "Now Available At Sephora",
  updated 2021-03-23; ARS Counsel post 2021-03-29). The brand's own homepage did
  NOT carry a "Sephora" mention in its 2021-02 / 2021-03 / 2021-04 snapshots --
  the announcement ran through press and Sephora's own channels.
- Cutoff (memo-at-cutoff, anti-leakage): **<= 2021-03-15** (pre-announcement).
- **Disambiguation (load-bearing).** Keep this expansion distinct from
  neighbouring Topicals milestones: (a) the **2020-08-07 DTC + Nordstrom**
  launch; (b) the brand's seed financing (~$2.6M, disclosed early 2021); (c) the
  Sephora **Accelerate** BIPOC-brand program selection that framed the 2021
  Sephora entry; and (d) **later** distribution moves (Sephora Canada; Sephora
  UK, ~2024) and **later** funding rounds. This case is the 2021 DTC->Sephora
  retail expansion only. Trade sources sometimes compress "Sephora.com online
  launch" and "nationwide Sephora shelves" into one event and gloss it as "~9
  months after launch"; the cutoff above sits before all public Sephora signal,
  so it is clean regardless of how that compression is read.

## Evidence -- org-motion availability <=cutoff

Probe: read-only Wayback CDX (date-bounded, `<=cutoff` applied by hand), via
PowerShell `Invoke-WebRequest` over HTTPS, 2026-06-14. (HTTP/port-80 and a burst
of `curl` calls were intermittently refused by archive.org; HTTPS
`Invoke-WebRequest` was the reliable path.)

**Corporate careers page `mytopicals.com/pages/careers` -- VIABLE but THIN.**
- **1** status-200 careers snapshot `<= 2021-03-15`: **2021-03-03** (CDX
  length 30,026). **1** distinct pre-cutoff month: 2021-03.
- **No 2020 careers coverage at all** -- the careers page's first-ever Wayback
  capture is 2021-03-03. So there is no pre-2021 hiring baseline to trend
  against.
- For context only (post-cutoff, NOT part of the `<=cutoff` evidence): the next
  careers snapshot is 2021-05-06, and the page is captured repeatedly thereafter
  -- i.e. coverage exists going forward, but only one snapshot precedes the
  cutoff.
- Cutoff-proximate snapshot (2021-03-03) carries **one visible job listing:
  Supply Chain Manager (Full Time)** -- a single role, with a detailed
  overview/experience/qualities body (reports into CEO + CPO; supply-chain /
  inventory / vendor-negotiation / database focus). No other roles are listed on
  that snapshot.

**Third-party ATS boards -- NONE found.**
- 0 snapshots for each tested slug `<= 2021-06`: `boards.greenhouse.io/topicals`,
  `boards-api.greenhouse.io/v1/boards/topicals`,
  `boards.greenhouse.io/embed/job_board?for=topicals`, `grnh.se/topicals`,
  `jobs.lever.co/topicals`, `jobs.ashbyhq.com/topicals`,
  `topicals.workable.com`, `apply.workable.com/topicals`.
- Implication: at this brand-stage Topicals appears to have hired via its own
  Shopify-site careers page, not a hosted ATS board. The careers page IS the
  org-motion surface here.

**LinkedIn -- NOT viable.**
- 0 pre-cutoff snapshots for `linkedin.com/company/topicals` (bare + www),
  `linkedin.com/company/mytopicals`, `linkedin.com/company/topicals-skincare`
  across 2018-2021. No usable company-page headcount level or trend `<=cutoff`.

**Corporate-site liveness (context, not org-motion).** The homepage
`mytopicals.com` is well-covered `<=cutoff` (monthly-ish snapshots from
2020-08), so the site itself is archive-backtestable; the *gap* is specifically
the careers/hiring surface before 2021-03.

## LinkedIn viability

Not viable for this case. No `<=cutoff` LinkedIn company-page coverage exists
under any tested slug, so neither a headcount level nor a trend is recoverable
for the pre-expansion window. The org-motion read here must rest on the careers
page alone.

## Decision-relevant read (preview, not a verdict)

At the cutoff, the one archive-backtestable org-motion datum is a single open
role -- **Supply Chain Manager (Full Time)** -- on the brand's careers page
(2021-03-03), reporting into the CEO and CPO, focused on inventory, vendor
negotiation, shipment-cost optimization, and supply-chain database build-out for
a young DTC product company. Presented as facts only: **one listed role, in
supply chain / operations, at a single pre-cutoff snapshot, with no earlier
hiring baseline archived.** There is no archived multi-role or multi-month
hiring pattern `<=cutoff` from which to read a staffing *trajectory*. This is the
raw signal the WITH arm would carry. It must be presented as facts (the role,
its department, its single-snapshot timing), never as an editorial reading of
intent or confidence (the anti-steering lesson) -- and the thinness (n=1
snapshot, 1 role) must travel with it.

## Sealed-outcome recoverability (calibration target)

Recoverable. The post-cutoff result is established and **sealed** in the
facilitator-only outcome record
(`topicals_sephora_expansion_sealed_outcome_facilitator_only_v0.md`). **To keep
THIS research-tier doc safe for an outcome-blind constructor to read, the
post-cutoff outcome (whether/how the expansion proceeded, results, trajectory)
is NOT restated here** -- it lives only in the sealed record.

## Provenance & limits (load-bearing)

- These numbers are from **direct Wayback CDX reads via PowerShell
  `Invoke-WebRequest` (HTTPS)**, with the `<=cutoff` bound applied **by hand**.
  This is the archive.org rung of the capture catalog done manually -- adequate
  for a feasibility gate, **NOT** a capture-spine artifact.
- It used **no** `archive_org.py select_snapshot` (mechanical anti-leakage),
  produced **no** `SourceCapturePacket`, and ran **no** ECR derivation.
- Therefore the 2021-03-03 single-role read above is **feasibility evidence, not
  a captured `EvidenceUnit`.** Phase-4 MUST re-capture the org-motion evidence
  through the Capture Investigation Playbook + `archive_org.py` adapter
  (-> `SourceCapturePacket` -> ECR) before anything binds into the judgment
  packet. JSG-01 stays frozen: ECR derives integrity context but binds no
  `EvidenceUnit`.
- **Thinness is the headline limit.** Unlike the Beauty Pie case (multi-month,
  multi-role Greenhouse trajectory), Topicals' `<=cutoff` org-motion is a single
  careers snapshot with a single role. This case can carry a cutoff-proximate
  *composition point*, not a hiring *trend*. Whether that is sufficient
  org-motion signal for the WITH/WITHOUT contrast is an owner scoping call, not a
  gate-0 fact.

## Next

1. Owner scoping call: accept Topicals into the repeatability lane on a
   **single-snapshot, single-role careers-page** org-motion basis (composition
   point, not trajectory), or down-rank it as too thin and prefer a
   richer-coverage case.
2. If accepted: dated ledger amendment recording the careers-page (not ATS) org-
   motion admission into batch-1 case #4, with the cutoff `<= 2021-03-15` and the
   announcement window (~2021-03-23..29).
3. Phase-4 capture via the playbook + adapter -- primary reading: the 2021-03-03
   careers snapshot. (Any post-cutoff careers snapshots are reveal-side only and
   must not enter the blind packet.)
4. Phase 2 seals the outcome (done; see sealed record); Phases 3/5 build the
   baseline vs augmented packets with org-motion as the only delta.
