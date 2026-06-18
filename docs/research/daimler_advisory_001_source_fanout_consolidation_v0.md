# Daimler Advisory 001 Source Fanout Consolidation v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Consolidation of seven source-acquisition lanes for upgrading DAIMLER_ADVISORY_001 from advisory product-learning context toward a judgment-quality candidate.
use_when:
  - Checking which Daimler source directions are worth consolidating before rebuilding the participant packet.
  - Distinguishing source-improvement blockers from execution, scoring, validation, buyer-proof, or judgment-quality claims.
  - Deciding whether to spec tooling after the Daimler source fanout.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
stale_if:
  - A later source-acquisition pass verifies or rejects the pre-cutoff status of the AGM legal PDFs.
  - A Daimler source registry, participant-safe delta packet, or reveal calibration artifact supersedes this synthesis.
  - A later owner decision changes Daimler from source-upgrade candidate to abandoned, deferred, buyer-facing, or gate-bearing work.
```

## Status

Status: `DAIMLER_ADVISORY_001_SOURCE_FANOUT_CONSOLIDATED_V0`.

This is a research synthesis. It does not authorize source acquisition
implementation, scraping, archive retrieval, media capture, schema expansion,
runtime work, model execution, scoring, fixture admission, buyer proof,
validation, or judgment-quality claims.

## Bottom Line

The seven-lane fanout found that Daimler is more upgradeable than the current
participant packet shows, but the current state still does not become
judgment-quality evidence.

The strongest new finding is that public pre-cutoff official and legal material
can support a much richer participant packet: formal hive-down mechanics,
treasury/rating context, IT/IP/software allocation, mixed-contract handling,
employee/pension commitments, cost estimates, and governance guardrails.

The strongest remaining blocker is not "more search." It is consolidation:
prove pre-cutoff availability of the key legal PDFs, extract claim-level
evidence units, build a participant-safe packet delta, and keep reveal material
quarantined.

## Lane Results

| Lane | Direction | Main useful sources | What improves | Main blocker |
| --- | --- | --- | --- | --- |
| 1 | Official governance and AGM materials | AGM invitation/agenda, hive-down report, Annual Report 2018, corporate presentations, ad hoc releases | Formal structure, governance, IP/software allocation, employee/pension treatment, withdrawal mechanics, milestone path | Official materials are strong on paper design but thin on practical execution friction and third-party consent reality. |
| 2 | Legal transaction mechanics | AGM invitation, hive-down agreement/report, 2017 ad hoc, Q3 2017 report, July 2018 structure release | Partial universal succession, non-transferables, register-entry timing, employee safeguards through 2029, EUR 3.0bn pension contribution, 700+ subsidiaries/60+ countries scale | Key AGM legal PDFs need publication-date hygiene; annex-heavy detail is not yet extracted into participant-safe form. |
| 3 | Treasury, rating, and financing | Q1 2019 results/interim report, Annual Financial Report 2018, hive-down report, pre-cutoff corporate presentations | Liquidity, maturities, bond issuance, ABS use, A-rating protection, tax treatment, cost caps, pension funding, DFS/mobility exposure | Strongest "One Credit" design and rating-agency reaction sources are post-cutoff and must remain reveal-only. |
| 4 | IT, IP, contracts, and shared services | AGM invitation, hive-down agreement, Annual Report 2018, corporate presentations, Sustainability Report 2018 | Central parent governance, compliance oversight, treasury, formal IP custody, software categories, customer-data access, mixed-contract internal compensation | Actual TSA schedules, service levels, contract inventories, IP trust annexes, system maps, and cybersecurity carveout detail remain missing or non-public. |
| 5 | Investor and analyst pre-cutoff reaction | WSJ/Fox excerpt, Reuters mirrors, management countermotion response, Geely/BAIC partnership pieces, AGM governance materials | Market skepticism, dividend/profit pressure, partnership optionality, shareholder/governance concerns | Clean pre-cutoff sell-side and proxy-adviser material was not surfaced; synergy-loss objections remain weak in open sources. |
| 6 | Independent business press pre-cutoff | Reuters, Bloomberg, Handelsblatt, Business Standard, AP/Seattle Times reveal-only item | Strategic rationale, investor pressure, cost urgency, alliance/optionality logic, labor-protection context | Heavy reliance on paywalled or syndicated sources; limited standalone economics and downside-execution analysis. |
| 7 | Reveal/calibration lane | 2019 voting results, 2019 implementation history, 2021 spin-off vote, share allocation notice, Reuters market-debut article, later Daimler Truck/Mercedes materials | Calibration of vote result, implementation, later truck listing, IT carveout, strategic consequences, later performance | All reveal material is post-cutoff and not participant-facing; it cannot prove ex ante recommendation quality or causation. |

## Priority Source Stack

### Participant-Safe Pre-Cutoff Candidates

Use these first when rebuilding the packet, after provenance checks:

1. `Daimler Annual Meeting 2019 Invitation / Agenda`
2. `Daimler Annual Meeting 2019 Hive-down and Acquisition Agreement`
3. `Daimler AM 2019 Hive-down Report / Ausgliederungsbericht`
4. `Annual Report 2018 incl. combined Management Report Daimler AG`
5. `Q1 2019 Results Presentation`
6. `Interim Report Q1 2019`
7. `Daimler Corporate Presentation December 2018`
8. `Daimler Corporate Presentation FY 2018`
9. `2017 ad hoc release on divisional structure`
10. Selected pre-cutoff Reuters/Bloomberg/Handelsblatt investor-pressure pieces

### Quarantined Reveal Candidates

Do not place these in participant-facing material:

1. 2019 AGM voting result and approval margin.
2. 2019-11-01 implementation status.
3. 2021 truck spin-off vote and rename vote.
4. 2021 spin-off legal effectiveness, listing, and share allocation.
5. Later market-debut valuation and performance commentary.
6. Later IT carveout completion and application-count reduction.
7. Later Daimler Truck strategic actions, capital allocation, buybacks, targets,
   and Mercedes-Benz retained-stake changes.

## Blockers To Clear

### B1: Pre-Cutoff Provenance Hygiene

Problem: the most important AGM legal PDFs appear to be pre-meeting materials,
but multiple lanes flagged current-host date ambiguity.

Closure condition:

- Record durable evidence that the AGM invitation, hive-down agreement, and
  hive-down report were publicly available before `2019-05-21 23:59 CEST`.
- Record source URL, archive URL if available, retrieval timestamp, file hash,
  publication date basis, and any ambiguity.

### B2: Claim-Level Evidence Registry

Problem: sources are now identified, but claims are not yet mapped to evidence
units.

Closure condition:

- Create source-backed evidence units for at least these claim families:
  treasury/rating, one-time and running costs, tax treatment, pension funding,
  employee safeguards, legal transfer mechanics, public-law authorization
  handling, mixed contracts, IP/software/data treatment, governance, milestones,
  and withdrawal triggers.
- For each evidence unit, preserve source ID, source class, date status,
  participant visibility, summary, supported claim, excluded/reveal status, and
  uncertainty.

### B3: Participant-Safe Delta Packet

Problem: the current participant packet is too compressed relative to the
available source base.

Closure condition:

- Add only pre-cutoff, participant-safe facts from the registry.
- Preserve blind constraints: no source titles, raw locators, source hashes,
  vote result, implementation status, consulting narrative, later outcomes, or
  reveal facts.
- Explicitly label unavailable detail rather than filling it from inference.

### B4: Irreducible Public-Record Gaps

Problem: some details may not be publicly available in enough specificity.

Likely remaining gaps:

- TSA schedules and service levels.
- Contract-by-contract inventories.
- IP trust annexes and sublicense economics.
- System inventory and application disentanglement maps.
- Cybersecurity carveout plan.
- Dealer/customer concentration and consent-transfer friction.
- Quantified execution-failure scenarios for shared-services separation.

Closure condition:

- Either find pre-cutoff public evidence, or label these as known missing
  evidence so the blind participant sees uncertainty rather than invented
  certainty.

### B5: Reveal Calibration Separation

Problem: reveal facts are useful but dangerous.

Closure condition:

- Maintain a separate reveal/calibration artifact after the blind judgment is
  sealed.
- Keep post-cutoff vote, implementation, listing, performance, IT carveout, and
  strategic outcome facts out of all participant-facing packets.

### B6: Execution And Scoring Controls

Problem: stronger sources alone do not produce judgment-quality evidence.

Closure condition:

- Freeze the improved packet.
- Run a sealed blind judgment under accepted execution controls.
- Capture raw output and provenance.
- Score or calibrate only against a separately controlled reveal set.
- Preserve failure events and non-claims.

## Tooling Implications

The subagents did not return formal tool specifications. They returned source
blockers and workflow frictions.

Tooling that might be justified after one manual consolidation pass:

1. Source provenance/date checker:
   - verifies PDF availability date basis;
   - captures URL, archive URL, retrieval timestamp, hash, and ambiguity;
   - labels `pre_cutoff`, `date_ambiguous`, or `reveal_only`.
2. Evidence-unit extraction ledger:
   - maps source passages to claim families;
   - records participant visibility and uncertainty;
   - prevents unsupported guardrails from becoming packet facts.
3. Participant-safe packet leakage checker:
   - checks packet text for source titles, URLs, hashes, reveal dates, vote
     results, implementation facts, consulting narrative, and post-cutoff terms.
4. Reveal quarantine ledger:
   - stores post-cutoff facts separately for calibration;
   - prevents reveal facts from flowing back into participant-facing material.

Hard pushback: do not build these tools before the first manual consolidation.
The current blockers are not yet tool-spec blockers. They are source hygiene,
evidence mapping, packet extraction, and execution-control blockers. Build a
tool only after the manual pass shows repeated friction that a tool can remove.

## Current Judgment-Worthy Assessment

Current assessment: `not_judgment_quality_evidence`.

Upgradeable assessment: `plausible_judgment_quality_candidate_after_source_registry_packet_rebuild_and_controlled_execution`.

Reason: source availability now looks strong enough to justify a serious packet
rebuild, but the evidence has not been transformed into a clean claim-level
registry, participant-safe packet, sealed execution, or calibrated scoring
artifact.

## Non-Claims

- Not buyer proof.
- Not product proof.
- Not validation.
- Not fixture admission.
- Not scoring.
- Not blind-use readiness.
- Not judgment-quality evidence.
- Not commercial readiness.
- Not source-access implementation authorization.
- Not archive/body/media retrieval completion.
- Not schema, runtime, scraper, miner, automation, ECR, Cleaning, or Judgment
  implementation authorization.
