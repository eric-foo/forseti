# Company Surface First-Company Ingest — Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Unblocks the Company Surface lane: the first completed, owner-ratified
  company now exists (Tower 28, Phase 1 v2 bundle). Commissions the lane to
  exercise its accepted logical-record and mapping contracts against this
  first real company, under those contracts' own authority.
use_when:
  - Dispatching the Company Surface lane's first-company ingest.
  - Checking which Tower 28 artifacts and rows are in scope for the record.
authority_boundary: retrieval_only
open_next:
  - forseti/product/information/company_surface/README.md
  - forseti/product/information/company_surface/company_logical_record_and_view_contract_v0.md
  - forseti/product/information/company_surface/company_surface_silver_mapping_contract_v0.md
  - docs/decisions/forseti_company_intelligence_information_architecture_v0.md
stale_if:
  - The first-company ingest lands and is accepted (packet consumed).
  - Any Company Surface contract in open_next is superseded.
```

## Load Contract

- `packet_version`: 0
- `created_at`: 2026-07-18 Asia/Singapore
- `created_by_lane`: Tower 28 CI/GTM lane; provenance only, not authority
- `load_rule`: confirm-don't-trust. The Company Surface contracts in
  `open_next` are the only authority for record semantics, identity boundary,
  view/correction rules, and the success bar (use the logical-record
  contract's `Logical Record Success Signals` and `Cold-agent reference
  check`). This packet only announces the input and binds its edges.

## What is new (why the lane can start)

The first completed company exists. Owner-ratified 2026-07-18:

- `docs/research/forseti_beauty_tower28_company_intelligence_report_v2.md` —
  the live Phase 1 artifact. Use the revision-note version (post overclaim
  fix-pass, PR #1093): wording carries labeled inference and existence-vs-
  concentration bounds that the record must not silently strengthen.
- `docs/research/forseti_beauty_tower28_company_intelligence_scan_v2.md` and
  `..._csb_v2.md` — supplement receipts (with lake packet IDs) and the sealed
  commission.
- `docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md` +
  `..._scan_v1.md` — audit substrate; v2 reuses v1's OBS-001–029 verbatim
  with original observation dates.
- Preserved source packets live in the canonical lake (`F:\forseti-data-lake`,
  packet IDs in the scan receipts).

## Commission (bounded)

Map the Tower 28 Phase 1 evidence into the Company Surface logical record per
the owning contracts. Boundary application (from the information-architecture
decision, restated here only as a pointer):

- IN: company/Brand/product/SKU/claim/channel identities; the dated typed
  observation rows (OBS/COV grain) with source and provenance links;
  limitations, conflicts, and identity uncertainty as recorded; effective-time
  history (e.g., the v1→v2 ingredients-page claim-wording shift is history
  material, not a correction); proxy relations stated as proxy, never promoted.
- OUT: the Executive Intelligence Brief conclusions, confidence statements,
  chain cards, and any interpretation, priority, pain, ICP, wedge, or GTM
  content. Decision layers stay downstream per the Company Surface boundary.

## Drift Guard

- One company, one bounded ingest — no pool-wide backfill, no new schema
  beyond what the accepted contracts already define, no monitoring.
- Record wording never strengthens report wording: labeled inference stays
  labeled; existence findings never become rates or concentrations.
- No re-capture and no fresh web reads from this lane; the evidence base is
  the bundle plus its lake packets. Gaps stay typed gaps.
- Contract friction (record shapes the contracts cannot express) returns as
  typed feedback for contract adjudication, not as in-lane contract edits.

## Success signal

The logical-record contract's own `Logical Record Success Signals` pass for
Tower 28, plus a short ingest receipt: what mapped, what was excluded by the
boundary, what could not be expressed (typed contract feedback), and pointers
from record rows back to OBS/COV IDs and lake packets.
