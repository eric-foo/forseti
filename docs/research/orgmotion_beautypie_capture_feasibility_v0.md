---
retrieval_header_version: 1
artifact_role: Research feasibility / evidence-gathering record (NOT product authority, NOT a capture-spine artifact)
scope: >
  Gate-0 feasibility finding for the org-motion Beauty Pie pilot (batch-1 case #3):
  whether <=cutoff org-motion evidence is archive-backtestable for Beauty Pie's
  March-2023 GBP5-tier-elimination repricing, a preview of the decision-relevant
  signal, the sealed-outcome recoverability check, and the owner-accepted ATS-led
  scope. Read-only by-hand archive probe; feeds the dated ledger amendment and the
  Phase-4 capture.
use_when:
  - Deciding whether and how to run the org-motion Beauty Pie pilot.
  - Constructing the Phase-4 org-motion capture (this record says what to re-capture, via the adapter).
  - Auditing the gate-0 feasibility basis and its provenance limits.
authority_boundary: retrieval_only
open_next:
  - docs/research/orgmotion_demand_signal_wedge_discovery_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  - docs/product/source_capture_toolbox/capture_investigation_playbook_v0.md
stale_if:
  - The batch-1 ledger amends case #3, the cutoff, or the org-motion admission.
  - A Phase-4 capture via the adapter supersedes these by-hand feasibility numbers.
  - The pinned scoring key changes.
---

# Org-Motion Beauty Pie -- Gate-0 Capture Feasibility (v0)

## Status & non-claims

DISCOVERY / FEASIBILITY EVIDENCE. Not validation, not a `SourceCapturePacket`,
not an `EvidenceUnit`, not judgment-quality evidence, not a scoring-key change,
not a JSG-01 unfreeze, not live-API authorization. The product-learning cap
holds; N=1. The numbers below come from a **read-only by-hand archive probe**,
NOT a capture-spine capture (see Provenance & limits).

## Verdict

Gate-0 = **PASS via the hiring-composition (ATS) leg.** Beauty Pie's org-motion
is archive-backtestable <=cutoff through its public Greenhouse board; the
LinkedIn headcount-trend leg is NOT (no usable pre-cutoff coverage). Owner
accepted the **ATS-led scope** (2026-06-11): org-motion for this case = hiring
composition, optionally + a single Nov-2022 LinkedIn headcount point.

## Case frame

- Case: batch-1 #3 -- Beauty Pie eliminates the GBP5/mo entry tier, moves those
  members to GBP10/mo (the doubling), and scraps monthly spending limits.
- Decision / announcement: ~late-Feb / **2 March 2023** (member email; the
  backlash thread opens 2 Mar 2023).
- Cutoff (memo-at-cutoff, anti-leakage): **<= 2023-02** (pre-announcement).
  Distinct from the Sept-2021 "Beauty Pie Plus GBP59 annual" relaunch -- a
  different, earlier event not to be conflated with this case.

## Evidence -- org-motion availability <=cutoff

Probe: read-only Wayback CDX (date-bounded, `<=cutoff` applied by hand),
2026-06-11.

**Greenhouse `boards.eu.greenhouse.io/beautypie` -- VIABLE (strong).**
- 13 status-200 board snapshots <= 2023-03-01, spanning 2022-01-23 -> 2023-01-31.
- 8 distinct pre-cutoff months: 2022-01, -05, -06, -07, -08, -09, -10, 2023-01.
- Body size grows 3.9KB -> 6.4KB across the window (expanding job list).
- Cutoff-proximate snapshot (2023-01-31, 18KB) carries 8 dated job listings:
  Product Lead (Acquisition); Product Lead (Core Shopping Experience); Product
  Lead (Retention); Demand Planning Analyst; Inventory Planning & Analysis
  Manager; Senior Engineer; Senior UX Designer; Mid-Weight Digital Designer
  (maternity-cover FTC).
- Non-EU `boards.greenhouse.io/beautypie` = 0 snapshots (wrong host form for an
  EU-Greenhouse company; the EU host is canonical here).

**LinkedIn -- NOT viable for a trend.**
- `linkedin.com/company/beauty-pie*` (bare + www): first capture 2025-04 -- two
  years post-cutoff.
- `uk.linkedin.com/company/beauty-pie`: exactly one pre-cutoff snapshot
  (2022-11) -- a point-in-time level, not a trend; uk-host extraction unverified.

## Decision-relevant read (preview, not a verdict)

At the cutoff Beauty Pie was advertising a product/growth + **retention** +
demand/inventory build-out (three Product Leads including Retention; demand and
inventory planning; engineering and UX), with the openings count growing through
2022 -> Jan-2023 -- i.e. staffing a growth/retention machine at the moment it
pushed an unpopular price increase. This is the raw signal the WITH arm will
carry. It must be presented as facts (counts, departments, trajectory per
snapshot), never as an editorial "they were confidently expanding" (the
anti-steering lesson).

## Sealed-outcome recoverability (calibration target)

Recoverable -- and firmed in Phase 2. The medium-term result is established and
**sealed** in the facilitator-only outcome record
(`orgmotion_beautypie_sealed_outcome_facilitator_only_v0.md`). **To keep THIS
research-tier doc safe for an outcome-blind constructor to read, the post-cutoff
outcome (reaction, results, trajectory) is NOT restated here** -- it lives only in
the sealed record. The gate-0 "Covent Garden pop-up" signpost is **retracted** as
an over-read -- that pop-up was a June-2022 marketing activation, not a
post-backlash response.

## Scope decision (owner-accepted 2026-06-11)

Org-motion for case #3 = **hiring composition (ATS), optionally + the single
Nov-2022 LinkedIn point** -- not the hiring+headcount-trend fusion the discovery
note imagined. Rationale: the ATS leg is the better-validated, less-noisy half
and is directly decision-relevant here; requiring LinkedIn headcount trends
would likely disqualify most of the batch (Wayback LinkedIn company-page
coverage is sparse before ~2024).

## Provenance & limits (load-bearing)

- These numbers are from **direct Wayback CDX reads via PowerShell
  `Invoke-WebRequest`**, with the `<=cutoff` bound applied **by hand**. This is
  the archive.org rung of the capture catalog done manually -- adequate for a
  feasibility gate, **NOT** a capture-spine artifact.
- It used **no** `archive_org.py select_snapshot` (mechanical anti-leakage),
  produced **no** `SourceCapturePacket`, and ran **no** ECR derivation.
- Therefore the Jan-2023 job list above is **feasibility evidence, not a
  captured `EvidenceUnit`.** Phase-4 MUST re-capture the org-motion evidence
  through the Capture Investigation Playbook + `archive_org.py` adapter
  (-> `SourceCapturePacket` -> ECR) before anything binds into the judgment
  packet. JSG-01 stays frozen: ECR derives integrity context but binds no
  `EvidenceUnit`.

## Next

1. Dated ledger amendment recording the ATS-led org-motion admission into
   batch-1 case #3 (owner-signed).
2. Phase-4 capture via the playbook + adapter -- trajectory subset: the
   2023-01-31 snapshot as primary reading + ~3 earlier points (e.g. 2022-01,
   2022-mid, 2022-10) for the openings trend.
3. Phase 2 seals the outcome; Phases 3/5 build the baseline vs augmented packets
   with org-motion as the only delta.
