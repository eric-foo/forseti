# Core Spine v0 Data Capture Spine Pressure-Test Synthesis Usage Note

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Navigation and use note for the Data Capture obligation-contract pressure-test synthesis after optional adversarial clarifications.
use_when:
  - Opening the Data Capture pressure-test synthesis after the adversarial clarification patch.
  - Deciding how to treat the pressure-test sublane before owner acceptance.
  - Preparing same-lane Data Capture operating or tooling architecture without overclaiming Data Capture completion.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md
  - forseti/product/spines/capture/core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
input_hashes:
  patched_obligation_contract: A9B4D61226571ADCADD96504D361A7EBEB00775C315708AE53495E2F60EEE1DF
  post_clarification_synthesis: 46103142927A7EA7A4B61F10E0EF029614814F36438F4359C4B69B838E6C6126
  adversarial_review_report: 03268EBE7DDFCF2BB2C3C35EC8AC627623788CA6DBEC8756179017BD8545F34E
stale_if:
  - The obligation contract is materially patched after the hash above.
  - The full-fixture synthesis is materially revised after the hash above.
  - Owner accepts, rejects, or reframes Data Capture Spine v0.
  - A later adversarial review supersedes the current review report.
```

- Status: USE_NOTE_DRAFT_V0.
- Created: 2026-05-25.
- Scope: navigation and status interpretation for the Data Capture pressure-test synthesis.
- Implementation authorized: no.
- Runtime/source-system design authorized: no.
- ECR/Cleaning design authorized: no.
- Source-of-truth promotion claimed: no.

## 1. What This Note Is

This note tells future agents how to use the current Data Capture pressure-test
synthesis without inflating its status.

The pressure-test sublane is:

```text
Data Capture obligation-contract pressure testing.
```

Its current status is:

```text
Overpowered enough for an owner acceptance decision as the Data Capture
obligation baseline candidate.
```

That is an engineering-quality classification, not a formal lifecycle claim.
The formal claim remains weaker:

```text
The Data Capture obligation contract is pressure-tested across the planned
fixture set and appears stable enough for advisory use, subject to owner
acceptance and any fresh review needed after the clarification patch.
```

## 2. How To Read The Current Packet

Open the packet in this order:

1. `core_spine_v0_data_capture_spine_obligation_contract_v0.md` - current
   patched obligation contract.
2. `core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md` - current
   post-clarification synthesis of what the planned fixtures proved and did
   not prove.
3. `core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`
   - adversarial review that produced the optional clarification findings.
4. `core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` - broader
   Data Capture setup architecture and boundary context.

Important hash boundary: the adversarial review report reviewed the
pre-clarification synthesis hash recorded inside that report. The current
synthesis has since been patched to apply the optional clarifications. Use the
review for rationale and finding traceability; do not treat it as a fresh
hash-matched review of the post-clarification synthesis unless a later review
does that explicitly.

## 3. What The Pressure Tests Learned

The core learning is:

```text
The Data Capture obligation contract mostly held across messy source families,
but archive/history and recapture were too coarse until patched.
```

Specific learning:

- Obligation-first architecture held. Data Capture should be defined by
  capture obligations, not by a favored capture mode, scraper, API, source map,
  or generic source platform.
- Core/satellite split held. Core says what must remain visible; satellite
  explains how a source family makes that hard.
- One material core defect surfaced. Archive/history posture and recapture
  relationships must remain visible per source slice, locator, access attempt,
  archive/cache attempt, fallback path, or changed source state when multiple
  states coexist.
- Most source-family complexity remained satellite. Review surfaces,
  docs/changelog pages, threaded forums, and public-sector packages produced
  guidance but did not require broad core rewrites.
- Raw source-level capture sufficiency remains not proven for every fixture.
  Milwaukee is especially useful but shallow because it relied on
  reveal-readout depth rather than full raw package reconstruction.

## 4. What Future Agents May Treat As Stable

Future agents may treat these as stable advisory premises unless a stale
condition triggers:

- Data Capture v0 is commissioned-capture-oriented, not standing corpus intake.
- Data Capture records capture facts, context, timing, access limits,
  archive/cutoff posture, source-state relationships, blockers, and raw
  observables.
- Data Capture does not decide credibility, discounting, exclusion,
  representativeness, Signal Use Classification, Decision Strength, Action
  Ceiling, Cleaning transformations, ECR schema, runtime tooling, or source
  maps as core.
- The planned pressure fixture set has landed.
- The Unity archive/history defect was the only material core defect found by
  the planned fixture set.
- The Unity defect was patched narrowly in the obligation contract.
- The optional adversarial clarification findings were applied to the synthesis
  in the post-clarification hash listed above.

## 5. What Future Agents Must Not Infer

Do not infer any of the following from this note, the synthesis, or the review:

- Data Capture Spine is complete.
- The owner has accepted the obligation contract or synthesis.
- The contract is source-of-truth promoted.
- The fixture set is formal validation.
- Data Capture is ECR-ready or Cleaning-ready.
- Runtime/tooling/source-system architecture is designed.
- Implementation, automation, scraping, storage, APIs, dashboards, tests, or
  deployment are authorized.
- Raw source-level capture sufficiency is proven for every fixture.
- Satellite source-family guidance has become core without cross-family support
  or owner sign-off for a specific invariant.

## 6. How This Applies To The Overall Data Capture Spine

This packet strongly stabilizes one sublane:

```text
Obligation-contract pressure testing.
```

It does not finish the whole Data Capture Spine.

The broader Data Capture Spine still needs same-lane work before it can be
called overpowered as a spine:

- owner acceptance or rejection of the obligation baseline candidate;
- operating/tooling architecture for commissioned capture;
- clear human/agent role boundaries in the operating model;
- organization of satellite source-family guidance into a usable reference
  layer;
- decisions about multimodal/dynamic capture fixtures, if owner deems them
  required;
- eventual end-to-end commissioned capture dry run under the accepted operating
  model, if and when that is authorized.

## 7. Correct Next-Use Patterns

Good uses:

- Use the synthesis to decide whether to accept the current obligation contract
  as the Data Capture obligation baseline.
- Use the synthesis and this note as input to same-lane Data Capture
  operating/tooling architecture.
- Use the adversarial review to understand why the post-clarification synthesis
  says `held` at contract level, caveats Milwaukee depth, scopes the Unity
  patch, and keeps satellite guidance out of core.
- Use the contract hash and synthesis hash when preparing strict prompts or
  reviews.

Bad uses:

- Routing directly to ECR or Cleaning because the pressure-test sublane looks
  strong.
- Calling the Data Capture Spine done because the obligation-contract sublane
  is strong.
- Treating the adversarial review as a fresh review of the post-clarification
  synthesis hash.
- Treating source-family playbooks as already built.
- Treating capture tooling or data farming as authorized.

## 8. Owner Decision Surface

The clean owner decision is:

```text
Accept, reject, or patch the post-clarification synthesis as the current Data
Capture obligation baseline candidate.
```

If accepted, the next same-lane architecture work can start from the obligation
baseline without reopening the full fixture program.

If rejected, the owner should identify whether the rejection concerns the
contract itself, the synthesis wording, fixture coverage, optional review
clarifications, or the broader Data Capture lane boundary.
