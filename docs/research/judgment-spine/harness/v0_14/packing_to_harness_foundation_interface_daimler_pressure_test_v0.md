# Packing -> Harness Foundation Interface: Daimler Second-Case Pressure Test v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Second-case (non-Unity) pressure test of the adjudicated Packing -> v0.14 Harness Foundation interface (v2), checking interface genericness and the M6 leakage-surface generalization against the Daimler carve-out case.
use_when:
  - Checking whether the v2 interface fits a case other than Unity before leaning on it.
  - Deciding whether M6 (generalized leakage surface) holds beyond n=1.
  - Sourcing the recommended D2 refinement (packet-safe vs facilitator-only source manifest) for a future interface revision.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/packing_to_harness_foundation_interface_architecture_v2.md
  - docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md
  - docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md
input_hashes:
  interface_under_test__packing_to_harness_foundation_interface_architecture_v2.md: 5110C2DADA8741273A9830373EDCF1313B4EE0832ABEED6E96244215E5393C74
  docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md: 744F31FAE74231F4269E5D23F8ECBAF93C1A9D1BAAA0FA3DA268AF7901187E0E
  docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md: E60B496101E154401EA9D6E0E5C2EC58701A7EF1E1FBEC4C01A9C5E392D0347F
branch_or_commit: main @ b7627d3389eeaa8456c65974039ada0e519617bc (dirty; controlling sources untracked)
stale_if:
  - The v2 interface artifact is revised (re-run against the new version).
  - A third case exposes a generic field this test did not stress.
```

- Status: PRESSURE_TEST_COMPLETE
- Interface under test: `packing_to_harness_foundation_interface_architecture_v2.md` (adjudicated)
- Test case: Daimler carve-out (Tier-0 candidate; lower fame than Unity; no sealed memo; not score-ready)
- Result: INTERFACE_FITS — M6 empirically validated; one refinement (D2) recommended; no interface-breaking defect found
- Implementation, probe execution, scoring, validation, readiness, acceptance, source-of-truth promotion: not authorized / not proven

## Why This Test

The adjudicated v2 interface was derived primarily against Unity. Its single largest open risk was **n=1**: modification M6 generalized the leakage/spoiler surface (and the bundle shape) from one case. The only real way to test that abstraction is to push a *different* case through the interface. Daimler is the right second case: it is lower-fame, has **no sealed memo** (so it stresses M6's optional `legacy_prior_judgment` slot), and is not score-ready (so it stresses the block-first admission states for clean reasons). This is an interface-genericness test, not a Daimler score run.

## What Was Checked

Daimler's existing artifacts (participant packet, safety receipt, preflight) were mapped onto v2's Packing-owned outputs, HEB surfaces, the M6-generalized leakage surface, the M3 admission-state model, the M4 `bytes_available` hash gate, and the contestant-visible boundary.

## Findings

**D1 — M6 validated (the main open risk closes).** Daimler has no sealed memo, no reveal, no outcome calibration of its own yet, and its excluded material is exactly outcome-class: final vote result, later implementation status, later corporate actions, outcome metrics, consulting-firm narrative, post-cutoff press (safety receipt "Zero-Spoiler Rule Applied" / "Excluded Source Classes"). These map cleanly onto M6's generalized `outcome_leakage_classes`. The optional `legacy_prior_judgment` slot is correctly **absent** for Daimler. Under v1's original hardcoded surface ("sealed memo / calibration / reveal exclusions, known fame risk"), Daimler would have carried awkward not-applicable slots. M6 fits n=2 better than the candidate's hardcoded surface would have. The riskiest modification holds.

**D2 — New refinement: separate the packet-safe source manifest from facilitator-only provenance (recommended for a future v3).** Daimler's zero-spoiler discipline withholds source URLs/titles from the participant view and uses **source-CLASS labels** instead (safety receipt S1–S7: "intentionally source-family labels, not participant-facing source URLs or title lists"). But the v0.14 `ParticipantPacket` frontmatter and v2's evidence registry expect a `source_manifest` with `source_id`/`source`/`retrieval_timestamp`/`hash`. v2's contestant-visible boundary says contestants see a "packet-safe source manifest" but does not define that *packet-safe = class-labeled* and that full provenance (`source_id`, `retrieval_timestamp`, source-byte `hash`) is **facilitator-only evidence-registry** content, not contestant-visible. Daimler makes this split explicit in a way Unity (which shipped an EU source packet) did not force. This is a clarification, not a contradiction — the interface still fits — but a future v3 should state: the contestant-visible manifest is class-labeled/packet-safe; provenance IDs/timestamps/hashes live in the facilitator-only registry. Leaving it implicit risks a future operator exposing source identifiers to a contestant.

**D3 — M4 validated in the opposite direction.** Unity exercised `bytes_available: false` (EU-08 source-visibility gap → adapter_blocked). Daimler's sources (official disclosures, investor presentations, annual reports, pre-cutoff business press) are retrievable, so `bytes_available: true` and source-byte hashes are required and obtainable. M4's split is now exercised both ways across two cases; it generalizes.

**D4 — Block-first model and adapters are correctly case-conditional.** Daimler needs **fewer** adapters than Unity: no source-visibility-gap adapter, no `legacy_prior_judgment` adapter. The adapters are optional/case-conditional, not Unity-mandatory. Daimler is currently inadmissible for clean, enumerable reasons (no evidence registry with IDs/hashes, no frozen facilitator ledger, no blind judgment), which is exactly what the Packing-side and run-binding block states are for. The admission-state model (M3) classifies Daimler cleanly (`draft_only` now; `score_blocked` if a freeze were attempted without a ledger/judgment).

**D5 — Frontmatter conversion is an expected Packing step, not an interface defect.** Daimler's packet would need light reframing into the Pydantic frontmatter shape (`authority_constraints`, `capability_constraints`, `permitted_assumptions`, `forbidden_information_notice` as named fields). The bridge foundation already anticipates this ("converted to v0.14 frontmatter and source-manifest shape"). This is Packing conversion work, not a gap in the interface.

## Verdict

The v2 interface **fits** the Daimler case. The single modification flagged during adjudication as an n=1 guess (M6) is empirically validated against a second, structurally different case. One genuine refinement (D2) surfaced and is recommended for a future revision. No interface-breaking defect was found. The interface's block-first posture, adapter optionality, and admission-state model all behaved correctly on a case that is intentionally not score-ready.

This raises confidence that v2 is generic enough to be leaned on for case-admission prompt binding. It does **not** prove the interface is complete: only two cases (Unity, Daimler) have been examined, and a third case could still expose a missing generic field.

## Recommended Next Step

- Fold D2 into a v3 interface revision when convenient (small clarification to the contestant-visible boundary and evidence-registry sections). Not blocking.
- v2 may be used to bind a future Daimler or Unity case-admission CA prompt without re-deriving the boundary.

## Non-Claims

This test does not claim: Daimler case admission, score-readiness, or probe pass; Judgment Spine or v0.14 harness validation; interface completeness beyond the two cases examined; implementation authorization; source-of-truth promotion of v2, this note, or any Daimler artifact; acceptance or owner approval; that the Daimler packet is ready for blind use; that dirty/untracked sources are accepted authority.

## Source-Read Ledger

| Source | Why read | State |
| --- | --- | --- |
| `..._architecture_v2.md` (interface under test) | The interface being pressure-tested; hashed | created this session; hash recorded |
| Daimler `participant_packet_v0.md` | Contestant-visible packet shape, zero-spoiler boundary, known-unknowns | untracked; hashed (matches the value embedded in the safety receipt) |
| Daimler `safety_receipt_v0.md` | Included/excluded source classes; participant/facilitator split; S1–S7 class labels (D2) | untracked; hashed |
| Daimler `case_02_preflight_v0.md` | Tier-0 classification, fame/leakage risk, cutoff options | untracked; hashed |
