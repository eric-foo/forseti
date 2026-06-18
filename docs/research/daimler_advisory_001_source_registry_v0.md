# Daimler Advisory 001 Source Registry v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Manual source-unit registry for DAIMLER_ADVISORY_001 participant-safe packet rebuild planning.
use_when:
  - Checking which Daimler source families can be converted into claim-level evidence units.
  - Separating participant-safe candidates, missing evidence, date ambiguity, and reveal-only material.
  - Planning the next Daimler packet rebuild without claiming buyer proof, validation, or judgment-quality evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md
  - docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md
  - orca/product/spines/judgment/toolkit_gaps/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md
stale_if:
  - A later source provenance pass retrieves, hashes, and dates external Daimler source bodies.
  - A participant-safe Daimler delta packet supersedes this registry.
  - A durable raw Daimler answer or completed blind execution receipt changes the case claim-tier route.
  - A later accepted Judgment Spine packet or evidence-unit architecture changes the registry vocabulary.
```

## Status

Status: `DAIMLER_ADVISORY_001_MANUAL_SOURCE_REGISTRY_V0`.

Current registry state: `manual_registry_first_pass_no_external_source_body_retrieval`.

This artifact converts the source fanout into a manual source-unit registry. It
does not retrieve external source bodies, verify publication dates, preserve
archives, compile a participant packet, run Daimler, create a raw answer, score
output, admit a fixture, validate Judgment Spine, package buyer proof, or claim
judgment-quality evidence.

## Source Basis

This registry is based on local Orca artifacts read for the current docs-write
phase:

| Source artifact | Role in this registry |
| --- | --- |
| `docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md` | Primary source-family and blocker synthesis from seven source-acquisition lanes. |
| `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` | Current Daimler claim-tier state: `no durable evidence`. |
| `docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | Capability boundaries for provenance, evidence-unit, packet, known-gap, reveal, execution, and calibration handling. |
| `docs/product/source_capture_toolbox/README.md` | Boundary confirming Source Capture Toolbox is Data Capture/source-access specific, not the owner of this Judgment Spine registry. |

No external Daimler PDF, article body, archive snapshot, publication-date record,
or source hash was retrieved in this pass.

## Classification Vocabulary

| Classification | Meaning in this registry | Participant-packet effect |
| --- | --- | --- |
| `verified_pre_cutoff` | Durable source-level record proves public availability before the case cutoff. | May support a load-bearing participant fact after evidence-unit extraction. |
| `date_ambiguous` | Source appears relevant and possibly pre-cutoff, but this registry lacks a durable public-availability basis. | Cannot support a load-bearing participant fact until adjudicated. |
| `participant_safe_candidate` | Source family appears safe in topic and timing from the fanout, subject to the same provenance and extraction burden as every other candidate. The label does not mean packet-safe or verified. | Candidate input only; not packet text yet. |
| `missing_or_unretrieved` | Source detail was not surfaced, is non-public, or has not been extracted into usable form. | Preserve as a known gap; do not infer around it. |
| `reveal_only_excluded` | Post-cutoff or outcome material useful only after a sealed blind judgment. | Prohibited in participant-facing packet material. |

Current assignment note: no source unit in this registry is promoted to
`verified_pre_cutoff`, because this pass did not retrieve and receipt external
source bodies. Every candidate unit requires a confirmed public-availability
basis before participant-packet use, whether or not the row also carries
`date_ambiguous`. The next provenance pass may promote individual units.

## Manual Source-Unit Registry

| Source unit | Source family | Registry classification | Claim families supported or affected | Extraction state | Blocker or handling rule |
| --- | --- | --- | --- | --- | --- |
| `DSU-001` | Daimler Annual Meeting 2019 invitation / agenda | `date_ambiguous`; `participant_safe_candidate` | Governance, shareholder authorization path, milestone framing, employee/pension treatment, withdrawal mechanics | Not extracted into evidence units | Prove pre-cutoff public availability before participant use. |
| `DSU-002` | Daimler Annual Meeting 2019 hive-down and acquisition agreement | `date_ambiguous`; `participant_safe_candidate` | Legal transfer mechanics, non-transferables, mixed contracts, public-law authorizations, IP/software/data treatment | Not extracted; annex-heavy | Requires publication-date hygiene and annex-level extraction. |
| `DSU-003` | Daimler AM 2019 hive-down report / Ausgliederungsbericht | `date_ambiguous`; `participant_safe_candidate` | Hive-down mechanics, 700-plus-subsidiary scale, 60-plus-country scale, employee safeguards, pension contribution, cost/tax framing | Not extracted | Requires source date basis and claim-level evidence-unit extraction. |
| `DSU-004` | Annual Report 2018 including combined Management Report | `participant_safe_candidate` | Liquidity, maturities, bond issuance, ABS use, A-rating posture, governance, divisional performance context | Not extracted | Candidate only until source body, date basis, and relevant passages are captured. |
| `DSU-005` | Q1 2019 results presentation | `participant_safe_candidate` | Liquidity, financing, cost caps, tax treatment, pension funding, divisional performance context | Not extracted | Candidate only; needs passage-level claim mapping. |
| `DSU-006` | Interim Report Q1 2019 | `participant_safe_candidate` | Treasury/rating context, DFS/mobility exposure, cost/tax/pension context | Not extracted | Candidate only; needs passage-level claim mapping. |
| `DSU-007` | Daimler corporate presentations from December 2018 and FY 2018 | `participant_safe_candidate` | Strategic rationale, divisional accountability, partnership optionality, software/platform coordination | Not extracted | Candidate only; distinguish management narrative from evidence. |
| `DSU-008` | 2017 ad hoc release, Q3 2017 report, and July 2018 divisional-structure release | `participant_safe_candidate` | Historical divisional-structure rationale, milestone path, governance setup | Not extracted | Candidate only; preserve as context unless it supports a specific claim. |
| `DSU-009` | Selected pre-cutoff Reuters, Bloomberg, Handelsblatt, WSJ/Fox, and Business Standard investor/press pieces | `date_ambiguous`; `participant_safe_candidate` | Market skepticism, dividend/profit pressure, investor pressure, partnership optionality, labor context | Not extracted; some sources may be paywalled or syndicated | Need clean pre-cutoff copies and source-body extraction before packet use. |
| `DSU-010` | Clean sell-side analyst and proxy-adviser material | `missing_or_unretrieved` | Shareholder skepticism, governance objections, synergy-loss critique | Not surfaced in current fanout | Preserve as a missing evidence class unless later found. |
| `DSU-011` | TSA schedules, service levels, contract inventories, IP trust annex economics, system maps, cybersecurity carveout, dealer/customer consent friction | `missing_or_unretrieved` | IT/IP/contracts/shared services execution risk and synergy preservation | Not publicly surfaced or not extracted | Preserve as known gaps; do not fill with plausible execution detail. |
| `DSU-012` | Strongest "One Credit" design and rating-agency reaction sources identified as post-cutoff | `reveal_only_excluded` | Treasury/rating calibration and later funding interpretation | Quarantined | Do not use in participant-facing material before sealed blind judgment. |
| `DSU-013` | 2019 vote result, 2019 implementation, 2021 truck spin-off, listing, share allocation, later IT carveout, later performance and strategic actions | `reveal_only_excluded` | Outcome calibration and hindsight checks | Quarantined | Calibration-only after sealed blind output; never participant-facing. |

## Claim-Family View

| Claim family | Candidate source units | Current registry posture | Packet implication |
| --- | --- | --- | --- |
| Legal transfer mechanics | `DSU-001`, `DSU-002`, `DSU-003`, `DSU-008` | Promising but not evidence-unit ready. | Extract specific transfer, non-transferable, register-entry, public-law authorization, and withdrawal-trigger claims before use. |
| Governance and accountability | `DSU-001`, `DSU-004`, `DSU-007`, `DSU-008` | Candidate management and governance record. | Separate formal governance facts from management rationale. |
| Treasury, rating, and financing | `DSU-003`, `DSU-004`, `DSU-005`, `DSU-006`, `DSU-012` | Pre-cutoff candidates exist, but strongest reaction material is reveal-only. | Participant packet may use only extracted pre-cutoff facts; DSU-012 rating reaction stays quarantined as reveal-only material. |
| One-time costs, run-rate dis-synergy, tax, and pension | `DSU-001`, `DSU-002`, `DSU-003`, `DSU-004`, `DSU-005`, `DSU-006` | Candidate official/legal basis, not passage-mapped. | Guardrails must be labeled as judgment unless directly supported by extracted units. |
| Employee safeguards and labor stabilization | `DSU-001`, `DSU-003`, `DSU-006`, `DSU-009` | Candidate official and press context. | Packet can show stabilizing commitments only after source-level extraction and uncertainty notes. |
| IT, IP, contracts, data, shared services | `DSU-001`, `DSU-002`, `DSU-003`, `DSU-004`, `DSU-007`, `DSU-011` | High-value area with major missing detail. | Preserve missing TSA, service-level, contract, IP-annex, system-map, and cybersecurity gaps. |
| Investor, analyst, and press reaction | `DSU-009`, `DSU-010` | Useful but weakest current source lane. | Do not overstate market skepticism or proxy-adviser concerns unless clean sources are surfaced. |
| Reveal and calibration | `DSU-012`, `DSU-013` | Quarantined. | Only open after sealed blind answer and scoring/calibration boundary are bound. |

## Candidate Packet Additions After Provenance And Extraction

This section is not participant-packet text and does not clear any fact for
participant use. It lists candidate additions only after source provenance,
evidence-unit extraction, cutoff status, participant visibility, and uncertainty
are resolved.

Candidate additions after provenance and extraction:

- formal hive-down and legal-transfer mechanics;
- subsidiary and jurisdiction scale;
- employee and pension commitments;
- cost, tax, liquidity, and financing context;
- shared governance, treasury, compliance, procurement, IT, software, data, and IP coordination concerns;
- market, investor, and labor-pressure context where clean pre-cutoff sources exist;
- explicit unknowns for TSA schedules, service levels, contract inventories, IP trust annex economics, system maps, cybersecurity carveout, and consent-transfer friction.

Still excluded from participant-facing packet material:

- source titles, source URLs, archive URLs, hashes, retrieval timestamps, and raw locators;
- post-cutoff vote result, implementation status, listing, share allocation, market-debut, IT carveout, performance, or later strategic facts;
- consulting narrative, facilitator notes, source-fanout lane labels, and this registry's internal source IDs;
- unsupported numeric guardrails generated by a model or operator without extracted evidence-unit support.

Packet rebuild requirement: every load-bearing participant fact must trace to an
evidence unit with cutoff status, participant visibility, supported claim, and
uncertainty.

## Known Gaps To Preserve

- Durable pre-cutoff public-availability basis for the AGM invitation, hive-down agreement, and hive-down report.
- Source URL, archive URL when available, retrieval timestamp, content hash, publication-date basis, and ambiguity note for each source unit.
- Passage-level extraction for legal mechanics, treasury/rating, costs, tax, pension, employee safeguards, mixed contracts, IP/software/data treatment, governance, milestones, and withdrawal triggers.
- TSA schedules and service levels.
- Contract-by-contract inventories.
- IP trust annexes and sublicense economics.
- System inventory and application disentanglement maps.
- Cybersecurity carveout plan.
- Dealer/customer concentration and consent-transfer friction.
- Quantified shared-services separation failure scenarios.
- Clean pre-cutoff sell-side or proxy-adviser material if it exists.

## Stronger-Tier Requirements

This registry does not by itself upgrade Daimler. The next stronger path would
require, in order:

1. Source provenance receipts for candidate sources.
2. Claim-level evidence units.
3. A participant-safe delta packet built only from allowed evidence units.
4. A frozen packet and prompt.
5. A sealed blind execution receipt with durable raw output location.
6. Separate reveal/calibration handling after the blind answer is sealed.
7. Scoring or calibration that preserves unsupported claims, overreach,
   underreach, uncertainty quality, and outcome-confounding limits.

Until those gates are complete, Daimler remains below judgment-quality evidence.

## Non-Claims

- Not buyer proof.
- Not product proof.
- Not validation.
- Not fixture admission.
- Not scoring.
- Not blind-use readiness.
- Not judgment-quality evidence.
- Not commercial readiness.
- Not completed product-learning evidence.
- Not a completed source-access, archive-body, media, or browser-snapshot capture.
- Not a participant packet.
- Not a prompt, wrapper, handoff, model run, raw answer, execution receipt, or reveal-calibration record.
- Not schema expansion, runtime work, scraper work, automation, ECR design, Cleaning design, or Judgment implementation authorization.
