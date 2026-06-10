# Judgment Spine Toolkit Blocker Specs From Daimler Source Fanout v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Planning specifications for toolkit capabilities implied by DAIMLER_ADVISORY_001 source-fanout blockers.
use_when:
  - Planning Judgment Spine tooling or operator aids after Daimler source consolidation.
  - Distinguishing protocol/checker/toolkit needs from implementation authorization.
  - Checking which blocker specs must be handled before claiming judgment-quality evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/daimler_advisory_001_source_fanout_consolidation_v0.md
  - docs/product/judgment_spine_evidence_ladder_architecture_v0.md
  - docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md
stale_if:
  - A later accepted toolkit architecture supersedes these blocker specs.
  - A completed Daimler source registry or participant-safe packet rebuild changes the blocker set.
  - Judgment Spine evidence-tier or execution-control doctrine changes.
```

## Status

Status: `JUDGMENT_SPINE_TOOLKIT_BLOCKER_SPECS_FROM_DAIMLER_SOURCE_FANOUT_V0`.

This artifact records capability specs for future toolkit planning. It is not an
implementation plan, build authorization, schema amendment, runtime
authorization, source-access authorization, validation record, scoring record,
fixture-admission record, buyer-proof artifact, or judgment-quality claim.

## Design Premise

The Daimler source fanout showed that Judgment Spine quality is difficult
because source coverage alone is not enough. A judgment-quality lane needs a
toolkit that preserves four boundaries at the same time:

- source facts versus source availability claims;
- pre-cutoff participant-safe facts versus reveal/calibration facts;
- supported claims versus model- or operator-inferred judgment;
- product-learning evidence versus gate-bearing judgment-quality evidence.

The blockers below are therefore toolkit capability specs. Some may later
become tools. Some should remain protocols or checklists. None authorize
implementation by themselves.

## Capability Specs

### C1: Cutoff Provenance Spec

Blocker: key sources can look pre-cutoff but still have ambiguous publication
or archive status.

Required capability: classify a source's cutoff status before it can support a
participant-facing claim.

Minimum fields:

```yaml
cutoff_provenance_record:
  source_id:
  canonical_title:
  publisher:
  canonical_url:
  archive_url:
  source_type:
  document_date:
  public_availability_basis:
  retrieval_timestamp:
  content_hash:
  cutoff_boundary:
  cutoff_status: verified_pre_cutoff | date_ambiguous | post_cutoff_reveal | excluded
  ambiguity_note:
  participant_visibility: allowed | prohibited | conditional
```

Pass condition:

- `verified_pre_cutoff` requires a durable basis for public availability before
  the case cutoff.
- `date_ambiguous` cannot enter a participant packet as a load-bearing fact
  unless a later adjudication resolves it.
- `post_cutoff_reveal` must be quarantined.

Likely future tool shape: provenance/date checker.

Do not automate first: use one manual Daimler pass to learn which publication
date bases are reliable enough to encode.

### C2: Evidence Unit Registry Spec

Blocker: sources are identified, but load-bearing claims are not mapped to
specific evidence units.

Required capability: convert sources into claim-level evidence units that can
drive packet construction, scoring, and later review.

Minimum fields:

```yaml
evidence_unit:
  evidence_unit_id:
  source_id:
  source_class:
  cutoff_status:
  participant_visibility:
  claim_family:
  supported_claim:
  evidence_summary:
  strength: direct | contextual | weak | excluded
  uncertainty:
  excluded_or_reveal_reason:
  source_location_hint:
  quote_policy:
```

Initial Daimler claim families:

- treasury/rating;
- one-time costs and running costs;
- tax treatment;
- pension funding;
- employee safeguards;
- legal transfer mechanics;
- public-law authorization handling;
- mixed contracts;
- IP/software/data treatment;
- governance and accountability;
- milestones and withdrawal triggers;
- market skepticism and investor pressure;
- partnership optionality;
- irreducible missing evidence.

Pass condition:

- Every participant-packet load-bearing fact traces to one or more evidence
  units.
- Every evidence unit has a cutoff status and participant visibility.
- Guardrails are labeled as model/operator judgment unless directly supported
  by evidence units.

Likely future tool shape: evidence-unit extraction ledger and registry checker.

### C3: Participant-Safe Packet Compiler Spec

Blocker: better source detail can contaminate a blind packet by leaking source
titles, URLs, hashes, vote results, implementation facts, consulting narrative,
or facilitator-only context.

Required capability: compile participant-facing packet text only from evidence
units marked participant-safe.

Packet compiler rules:

- Include only evidence units with `participant_visibility: allowed`.
- Exclude source titles, URLs, raw locators, hashes, retrieval timestamps, and
  facilitator-only registry details.
- Exclude post-cutoff vote, implementation, listing, performance, consulting,
  market-debut, and reveal facts.
- Preserve known unknowns explicitly.
- Preserve case cutoff and role frame.
- Keep model-facing task instructions separate from operator notes.

Pass condition:

- Packet facts trace to allowed evidence units.
- Leakage scan finds no reveal facts or source-provenance artifacts.
- Missing decisive details remain visible instead of being filled by inference.

Likely future tool shape: participant-safe packet compiler plus leakage checker.

### C4: Known-Gap And Unknowns Spec

Blocker: models and operators are tempted to convert missing decisive detail
into plausible but unsupported judgment.

Required capability: represent missing evidence as first-class packet material.

Minimum fields:

```yaml
known_gap:
  gap_id:
  claim_family:
  missing_detail:
  search_status: not_searched | searched_not_found | publicly_unavailable | available_but_not_extracted | reveal_only
  participant_visibility:
  why_it_matters:
  allowed_packet_wording:
  blocked_inference:
```

Daimler gaps that must remain explicit unless closed:

- TSA schedules and service levels.
- Contract-by-contract inventories.
- IP trust annexes and sublicense economics.
- System inventory and application disentanglement maps.
- Cybersecurity carveout plan.
- Dealer/customer concentration and consent-transfer friction.
- Quantified shared-services separation failure scenarios.
- Clean sell-side or proxy-adviser material if unavailable.

Pass condition:

- The packet tells the blind participant what is unknown and why it matters.
- Known gaps are not phrased as evidence of failure or safety unless supported.
- Revealed facts do not backfill pre-cutoff gaps.

Likely future tool shape: known-gap ledger and packet-unknowns checker.

### C5: Reveal Quarantine Spec

Blocker: reveal facts are necessary for calibration but toxic to blind packet
construction.

Required capability: store and use post-cutoff facts only after blind judgment
is sealed.

Minimum fields:

```yaml
reveal_fact:
  reveal_fact_id:
  source_id:
  reveal_date:
  fact_summary:
  calibration_use:
  confounding_risk:
  participant_visibility: prohibited
  quarantine_reason:
```

Pass condition:

- Reveal facts cannot be referenced by participant-facing packet artifacts.
- Reveal facts can be opened only in calibration, scoring, or post-reveal
  analysis lanes.
- Calibration claims must separate outcome observation from causation claims.

Likely future tool shape: reveal quarantine ledger and packet/reveal
cross-contamination checker.

### C6: Blind Execution Receipt Spec

Blocker: a better packet still does not become judgment-quality evidence unless
the run is controlled and receipted.

Required capability: bind packet, prompt, execution surface, raw output, and
non-claims.

Minimum fields:

```yaml
blind_execution_receipt:
  case_id:
  packet_artifact:
  packet_hash:
  prompt_artifact:
  prompt_hash:
  model_or_execution_surface:
  execution_tier:
  no_tools_or_manual_boundary:
  raw_output_location:
  run_timestamp:
  operator:
  stop_events:
  contamination_events:
  non_claims:
    - not buyer proof
    - not validation
    - not fixture admission
    - not scoring by itself
    - not judgment-quality evidence until scoring/calibration gates pass
```

Pass condition:

- A raw output location exists.
- Packet and prompt are frozen before execution.
- Execution tier is explicit.
- Any contamination or stop event remains visible.

Likely future tool shape: blind execution receipt writer/checker.

### C7: Scoring And Calibration Spec

Blocker: "good answer" is subjective unless the blind judgment is compared
against a controlled reveal and scoring rubric.

Required capability: score or calibrate a sealed answer after reveal without
turning later outcomes into hindsight proof.

Minimum fields:

```yaml
judgment_calibration_record:
  case_id:
  blind_execution_receipt:
  reveal_set:
  decision_match:
  rationale_quality:
  risk_identification:
  benefit_identification:
  guardrail_quality:
  unsupported_claims:
  overreach:
  underreach:
  abstention_or_uncertainty_quality:
  outcome_confounding:
  lesson_candidate_status:
  non_claims:
```

Pass condition:

- Scoring references a sealed blind answer, not a reconstructed answer.
- Reveal facts are separated from pre-cutoff packet facts.
- Outcome calibration does not claim causation unless separately supported.
- Lessons remain candidates until repeated or otherwise justified.

Likely future tool shape: calibration ledger and scoring-assist checker.

## Cross-Cutting Toolkit Invariants

- No source enters a participant packet without cutoff status and participant
  visibility.
- No participant-packet load-bearing claim lacks an evidence-unit trace.
- No reveal fact enters participant-facing material.
- No missing evidence is silently filled with plausible inference.
- No manual advisory answer becomes judgment-quality evidence by quality of
  prose alone.
- No tooling output upgrades evidence tier without the separate receipt,
  execution, scoring, and calibration gates.

## Tooling Planning Implications

The likely first toolkit capability is a combined provenance/evidence-unit
ledger checker, not a scraper.

Why: the Daimler fanout did not fail because no one could search. It failed
because discovered material had to be classified, de-duplicated, mapped to
claims, separated by cutoff visibility, and transformed into participant-safe
packet text.

Recommended future planning order:

1. Manually run C1 through C5 on Daimler.
2. Rebuild the Daimler participant packet from the resulting evidence units.
3. Run a controlled blind pass with C6.
4. Calibrate with C7.
5. Only then decide which repeated frictions justify automation.

## Relation To Source Capture Toolbox

Do not move this artifact into `docs/product/source_capture_toolbox/` as-is.

The Source Capture Toolbox is the current Data Capture home for first-tranche
source-access and capture-support tooling: Source Capture Packet core/CLI,
direct HTTP fetch, media/asset preservation, Archive.org availability/body
retrieval, and honest browser snapshot support.

This artifact is broader and later-stage. It includes Judgment Spine packet
construction, known-gap handling, reveal quarantine, blind execution receipts,
and scoring/calibration capability specs. Those are not Source Capture Toolbox
responsibilities.

Expected relationship:

- C1 Cutoff Provenance may consume Source Capture Packet metadata once the
  toolbox exists.
- C2 Evidence Unit Registry may use captured source artifacts as inputs.
- C3 through C7 remain Judgment Spine packet, reveal, execution, and calibration
  concerns.

Placement decision: keep this artifact under `docs/product/` as a Judgment
Spine toolkit-planning artifact unless a later accepted cross-spine toolkit
architecture creates a new home.

## Not Yet Tool Specs

These are not yet implementation-ready tool specs because they do not bind:

- exact file formats;
- CLI behavior;
- parser libraries;
- source-fetch mechanics;
- artifact paths for generated outputs;
- schema compatibility with existing harness code;
- test fixtures;
- failure-code vocabulary;
- migration or rollout plan.

Those should be scoped only after the manual Daimler consolidation proves which
fields and checks survive real use.

## Non-Claims

- Not implementation authorization.
- Not source-access tooling authorization.
- Not scraper, miner, crawler, archive, browser, or media retrieval scope.
- Not schema expansion authorization.
- Not runtime or package work.
- Not validation.
- Not fixture admission.
- Not scoring.
- Not buyer proof.
- Not product proof.
- Not blind-use readiness.
- Not judgment-quality evidence.
