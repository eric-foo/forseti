# Adversarial Artifact Review — Choice-Mechanism Chain Design Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Read-only adversarial review of the choice-mechanism chain design proposal
  against the bound owner rulings, the Tower 28 v1 evidence rows, and the
  current CSB company competitive-intelligence output contract.
use_when:
  - Adjudicating the proposal into the CSB company-profile contract synthesis pass.
  - Checking provenance defects and design failure modes found in this review.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_choice_mechanism_chain_design_proposal_v0.md
  - docs/decisions/forseti_ci_report_external_review_adjudication_ledger_v0.md
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md
branch_or_commit: claude/forseti-choice-mechanism-design-9b6962@ae2890e6
input_hashes:
  proposal_sha256: 82996afaa06f74bcd8b1a619e29120cb86974cf09074f14532dbcc2e12ae929a
  adjudication_ledger_sha256: ad06ca0aecde0deb7a7314ef8f5bd5070a6f44cc710b964f63c57a203b4226c1
  tower28_v1_report_sha256: 8ae25fc30848bbb95b354c6c77beb9b9e36d8438f7f6aff2466d3a874e5a6d0b
  csb_prompt_structure_sha256: 1022a961d649d8b7eff9e0a3987790be63ea45818a0916e3688002b7f96e5153
stale_if:
  - The proposal, binding ledger rulings, Tower 28 evidence rows, or CSB company-output contract changes.
```

```yaml
review_receipt:
  reviewed_by: unrecorded
  authored_by: claude-fable-5
  review_target: docs/workflows/forseti_choice_mechanism_chain_design_proposal_v0.md
  review_target_revision: ae2890e6
  output_mode: review-report
  write_boundary: report_only
  patch_authority: none
  recommendation: patch_before_acceptance
  recommendation_authority: advisory_decision_input_only
```

## Review frame

**Boundary problem.** Determine whether the proposal gives the owner a
one-pass-adjudicable D1-D4 design that can enter the existing CSB
company-profile contract without rework, hidden schema, evidence overclaim, or
drift into scanning, capture, monitoring, or contract execution.

**Failure modes attacked.** Binding-ruling deviation; non-deterministic
classification; holding-state leakage; decision-weight/prevalence leakage;
semantic citation mismatch; current-state/date laundering; hidden schema or
recurring toll; card rules that fail on their own worked example; omission of
cross-cutting accepted rulings; and design-pass drift.

**Decision criteria.** Ledger items 4, 9, 10, and 12; the commission's D1
no-restated-restraint-caveats rule; D2 reproducibility between independent
scanners; D3 separation of stated-sample composition from population
prevalence; D4 containment and cell-level provenance; semantic match to every
cited Tower 28 row; and adoption into the current company-output contract with
only the commissioned six-field per-review record as added durable structure.

## Findings

### Critical

None.

### Major

#### AR-01 — The six-field record cannot represent the classifier's own state machine

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** D2, lines 117-184
- **issue:** The only commissioned durable record has one `class` field, but
  the method requires an expected-background holding state outside the five
  classes, permits a secondary class “when it changes the read,” and graduates
  on repetition across independent venues. The record contains neither a
  background-state encoding, a secondary-class encoding, a source/venue
  reference, nor an observation/review identifier from which independence can
  be recovered. Its undifferentiated `date` also does not say publication,
  observation, or event date.
- **evidence:** Proposal lines 119, 155-169, and 173-184. The CSB observation
  contract distinguishes `publication_date`, `event_or_effective_date`, and
  `observation_at` and carries venue/lineage fields; the proposed row does not.
- **strongest defense:** The row could be interpreted as a compact child record
  nested under an existing observation, with background and secondary routing
  kept in prose. That relationship is not specified, and two scanners cannot
  safely infer the same hidden container or state encoding.
- **impact:** The classifier is not reproducible as written; the one
  commissioned exception is insufficient to execute its own graduation and
  tie-break rules without extra uncommissioned structure or analyst memory.
- **minimum_closure_condition:** The design must state, without adding fields
  beyond the commissioned six, how background holding, primary versus
  secondary routing, venue independence, claim-set identity, source identity,
  and the meaning of `date` resolve through existing report records.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch; this review may only identify the gap.
- **recommended correction:** Bind the six-field row to an existing
  observation/review container and define the allowed `class` values and
  holding/secondary semantics explicitly.

#### AR-02 — Graduation and amplification do not preserve claim relativity

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** D2 lines 125-184; D3 lines 220-229
- **issue:** D2 says classification is relative to a brand's load-bearing claim
  set, yet ingredient specificity alone graduates a reaction complaint and the
  routing sentence only explains “named label + named counter” or
  repetition/direct attack. An ingredient-specific reaction where the brand
  has no relevant skin-safety claim is left unrouted. D3 then says an
  `implicit / none` claim makes the complaint an ordinary defect, while D2 can
  treat attacks on load-bearing positioning as core-positioning threats.
  Finally, D3 calls `"non-comedogenic"` an ingredient-level claim even though
  the cited row supports a label/performance claim attacked by an
  ingredient-specific complaint.
- **evidence:** Proposal lines 127-130, 173-184, 220-229, and the complaint
  card at line 303.
- **strongest defense:** Ledger item 4 deliberately allows any one of
  ingredient specificity, independent repetition, or direct claim attack to
  graduate a background theme. The proposal must honor that ruling, but it
  still has to say which claim the graduated theme attacks and where it routes
  when no relevant claim exists; the owner ruling is not permission to erase
  claim relativity.
- **impact:** Independent scanners can assign different classes and
  amplification levels to the same review, especially for implicit
  positioning and ingredient-named reactions.
- **minimum_closure_condition:** Every graduation route must resolve to a named
  load-bearing claim or explicitly remain non-claim-attacking, and claim
  specificity must be kept distinct from complaint specificity.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Add a claim-relative routing rule that preserves
  the three binding graduation triggers while eliminating the unrouted
  ingredient-specific and implicit-positioning cases.

#### AR-03 — D1 installs the restraint-caveat surface the commission forbids

- **phase:** friction
- **friction_label:** maintenance drift and recurring review cost
- **severity:** major
- **confidence:** high
- **location:** D1 lines 65-104; repeated again at lines 321-329
- **issue:** The proposal explicitly makes seven `CANNOT see` columns and two
  structural restraint rules “load-bearing,” then repeats the limitations in
  the residuals. The commission binds D1's no-restated-restraint-caveats ruling
  and the ledger permits at most a definition line for lens-status vocabulary.
- **evidence:** Proposal lines 69-76, every D1 route-class table, and lines
  323-329; adjudication ledger lines 58-61.
- **strongest defense:** A capability boundary can prevent overclaim. Here the
  same boundaries are already carried by observation fields, fact-domain
  rules, and the report's visible limitations; turning them into a per-lens
  matrix is the recurring form surface the owner ruled against.
- **impact:** Contract adoption would add ceremony debt and duplicate
  constraints rather than remaining guidance for better conclusions.
- **minimum_closure_condition:** D1 must convey the positive acquisition/use
  lenses without requiring repeated per-lens restraint caveats; any necessary
  shared boundary must fit the commissioned definition-line ceiling.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Collapse repeated `CANNOT see` material to the
  smallest shared definition and let existing observation limitations carry
  row-specific boundaries.

#### AR-04 — The design omits the accepted “is it strengthening?” question

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** The chain, lines 59-63; D4 lines 233-244; worked mechanism sentence, lines 292-296
- **issue:** Ledger item 10 requires the central promise to ask where value
  resides, what drives it, whether it is strengthening, and what threatens it.
  The proposed chain and card cover value/buy/experience/threat/substitute but
  omit the strengthening question entirely.
- **evidence:** Adjudication ledger line 74 versus proposal lines 61-63 and
  237-244.
- **strongest defense:** Co-movement is out of scope because the current report
  has no time series. That defeats a positive strengthening claim, not the
  required question; the design can and should render the answer unknown or
  unsupported at this evidence state.
- **impact:** The card cannot fully express the owner-accepted front-page voice,
  so the contract pass must redesign it rather than adjudicate it in one pass.
- **minimum_closure_condition:** D4 must preserve the strengthening question
  with an honest unknown/not-observable rendering when no longitudinal evidence
  exists, without creating monitoring cadence.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Add the question to the mechanism/card guidance
  and bind its point-in-time unknown state to the existing longitudinal
  boundary.

#### AR-05 — The accepted preservation trigger is absent

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Provenance/non-claims lines 45-51 and 379-386; D4 structural rules lines 258-270
- **issue:** Ledger item 12 requires conclusion-bearing, disputable, or volatile
  observations to emit a preservation request through the existing capture
  seam. The proposal says it performs no capture—which is correct for this
  design lane—but provides no guidance-level trigger at all, even though its
  worked conclusion depends on rotating brand copy, a historical retailer
  quote, a live community thread, and snippet-level dupe pages.
- **evidence:** Adjudication ledger lines 76 and 80-98; proposal lines 45-51,
  258-270, and 379-386.
- **strongest defense:** Preservation is a cross-cutting contract-pass item
  rather than a choice-mechanism field. The design nevertheless claims to slot
  into that pass without rework and its D4 shipping rules are the exact place
  where conclusion-bearing evidence is selected; silence leaves the accepted
  trigger unapplied.
- **impact:** A contract executor can adopt the card while failing to preserve
  the evidence on which its most aggressive conclusion depends.
- **minimum_closure_condition:** The design must point D4 conclusion-bearing
  inputs to the already accepted preservation trigger without performing
  capture or adding a new seam.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Add a guidance-only pointer from card shipping to
  the existing CR capture-request trigger in ledger item 12.

#### AR-06 — A 2024 customer-quoted retailer claim is laundered into a current claim

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Worked example lines 292-303 and 310-313
- **issue:** The mechanism and front-page claim use present tense—Tower 28's
  promise is “carried to `non-comedogenic` on its Sephora PDP”—and the claim
  cell is marked `verified`. OBS-023 is a customer-community post published
  2024-04-25 that quotes then-visible PDP copy; it is not a 2026 Sephora PDP
  read. OBS-003 is a 2026 brand ingredients-page read and explicitly says the
  brand page does not use that wording.
- **evidence:** Tower 28 OBS-023 lines 958-985 and OBS-003 lines 398-425;
  proposal lines 292-300 and 310-311.
- **strongest defense:** The claim cell says “PDP copy quoted in-thread,” which
  correctly describes the immediate evidence. The present-tense mechanism and
  compressed row discard that qualifier, while the `verified` mark does not
  distinguish verified historical quotation from verified current retailer
  state.
- **impact:** The example commits the exact date-anchor laundering the review
  was commissioned to catch and can make an expired retailer claim look
  current.
- **minimum_closure_condition:** Every use of the retailer wording must carry
  its 2024 quoted-copy time anchor, or a current Sephora PDP read must support
  present tense.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Recast the example as a documented 2024
  retailer-copy/customer-complaint contradiction and keep current brand copy
  separate.

#### AR-07 — The worked chain infers buy motive, defection, and conversion from citing

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Chain line 61-63; worked example lines 292-304 and 310-314
- **issue:** “Why customers buy,” “where defectors go,” “sells on,” and “the
  complaint that converts a skeptical sensitive-skin buyer to the organized
  cheaper substitute” are demand and switching conclusions. OBS-020 establishes
  that an eczema venue discusses the brand and ingredient class, not that Swipe
  buyers choose it to avoid breakouts. OBS-027 establishes dupe-page citing and
  price gaps, not switching. OBS-024 shows one reviewer preferring Typology,
  not conversion to NYX.
- **evidence:** Tower 28 OBS-020 lines 874-901, OBS-024 lines 986-1013, and
  OBS-027 lines 1070-1097; proposal lines 61-63, 292-304, and 312.
- **strongest defense:** “Sells on” might be read as positioning shorthand, and
  the substitute cell itself says citing is not volume. The consequence
  sentence makes the causal conversion explicit, and the buy-reason clause
  assigns a specific motivation that its cited row does not carry.
- **impact:** The worked example fails the explicit semantic-match goal and the
  owner rule to describe substitution citing without inferring demand capture
  or switching.
- **minimum_closure_condition:** The chain and example must distinguish brand
  claim, reported motivation, venue relevance, named alternatives, and observed
  switching; no conversion or defection claim may survive without a row that
  states it.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Replace causal buyer/defector language with the
  literal observed claim, need-state discussion, comparison citing, price gap,
  and the single Typology preference.

#### AR-08 — A customer allegation is promoted into an ingredient contradiction and positioning failure

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Worked complaint and compressed row, lines 303 and 311-314
- **issue:** OBS-023 records a customer's assertion that
  Polyglyceryl-3 Diisostearate clogged pores; the row explicitly says this is
  not a test result. The proposal calls it a “named-ingredient contradiction,”
  says the hero is “exposed,” and predicts a “rate-bearing positioning
  failure.” The evidence establishes a specific allegation against quoted
  claim copy, not that the ingredient invalidates the claim or that positioning
  failed.
- **evidence:** OBS-023 `ambiguity_limitation` at report line 981; proposal
  lines 303 and 311-314.
- **strongest defense:** `Substantiation risk` is a routing class, not a verdict,
  and a named allegation is decision-relevant at n=1. That supports routing the
  item for a claims-file check; it does not support converting the allegation
  into a factual contradiction before the check.
- **impact:** Aggressiveness is achieved through evidence overclaim rather than
  through the consequence/admission fields, violating ledger item 9.
- **minimum_closure_condition:** The card must describe the evidence as a named
  customer allegation/claim attack and reserve contradiction or substantiation
  failure for evidence that verifies the ingredient/claim relationship.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Keep the aggressive action recommendation
  (“pressure-test first”) but remove factual contradiction/failure language not
  supported by OBS-023.

#### AR-09 — The worked confidence marks violate the proposal's weakest-input rule

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Confidence marks lines 246-256; worked card lines 300-304
- **issue:** The proposal says a cell inherits the weakest mark among
  load-bearing inputs. The buy-reason cell includes title-only OBS-020 but is
  marked `proxy`, not `thin`. The substitute cell is marked `corroborated`
  despite OBS-021 being a single historical title, OBS-026 being undated title
  evidence with `current_state_use: not_applicable`, and OBS-027 being partly
  snippet-level. These rows describe different signals and all carry empty
  `independent_corroboration_ids`; they do not corroborate one common switching
  claim.
- **evidence:** Proposal lines 248-256 and 301-304; Tower 28 OBS-020,
  OBS-021, OBS-026, and OBS-027.
- **strongest defense:** Multiple independent venues do show a broader
  comparison/substitution environment. That can support a carefully named
  composite, but it does not satisfy the artifact's own same-signal
  `corroborated` definition or weakest-input inheritance rule.
- **impact:** D4's confidence system overstates the example and is not
  self-consistent enough for independent authors to apply.
- **minimum_closure_condition:** Every worked cell must follow one explicit
  aggregation rule that preserves the weakest load-bearing limitation and does
  not call heterogeneous signals corroboration.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Use split marks by evidence function or lower
  the cell mark to the weakest input; do not add schema fields.

#### AR-10 — A denominator is required, but the sample is not reproducibly defined

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** D2 lines 108-123; D3 lines 187-200; worked next observable line 314
- **issue:** The micro-frame names venue, date range, and negative/all base, but
  omits selection route, sort/order, inclusion/exclusion handling, and whether
  the sample is consecutive or convenience-selected. The admission rule is
  also ambiguous about whether a visible verified-purchase marker is required.
  A denominator over an undefined convenience sample can look more
  proportional than it is. Line 314 then calls the future result a
  “rate-bearing positioning failure,” although D3 correctly limits the number
  to sampled composition.
- **evidence:** Proposal lines 110-123, 189-200, and 314; Tower 28 GAP-008 and
  REQ-004 confirm that sampling has not yet been performed.
- **strongest defense:** The frame says “stated sample” and requires a date
  range. That is not a complete sample definition when platform ordering and
  admission choices can change `N`.
- **impact:** Two scanners can report different `k/N` values while both
  satisfying the visible template, and downstream readers can mistake
  convenience-sample composition for a complaint rate.
- **minimum_closure_condition:** The design must make the sample reproducible
  enough to interpret `N`, and all output must remain “composition of this
  stated sample,” never a rate-bearing positioning conclusion.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Bind the minimum sample-definition prose outside
  the six-field review row and replace “rate-bearing positioning failure” with
  the literal sampled-composition claim.

#### AR-11 — The commissioned record has no insertion seam in the current contract

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Proposal lines 117-123 and 233-283; CSB prompt structure lines 694-874
- **issue:** The current company-output contract makes Sections 2 and 5-8
  narrative and types Sections 1, 3, 4, 9, and 10. Its observation row has no
  `star`, `class`, `claim_attacked`, or `specificity` fields. The proposal calls
  the six-field row durable but does not say where it lives, how it links to an
  OBS row, or which company section consumes it.
- **evidence:** CSB company contract lines 694-700, 755-787, and 805-874;
  proposal lines 117-123.
- **strongest defense:** The owner has commissioned this one durable-record
  exception, so a contract addition is allowed. The missing issue is not
  permission; it is the design's failure to specify the allowed addition well
  enough for the contract pass to adopt it without reconstructing an
  integration decision.
- **impact:** The proposal does not satisfy the “slots into the contract-pass PR
  without rework” success signal and risks either hidden schema expansion or a
  non-durable prose-only classifier.
- **minimum_closure_condition:** The proposal must bind the exact contract
  section/container and existing-record linkage for the six fields, with no
  additional ledger or validator fields.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Name the intended Section 7/observation-linked
  placement and serialization boundary as part of the design, leaving actual
  contract editing to the contract pass.

#### AR-12 — `CR-001` and `CR-002` do not dereference to report rows

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** Worked example lines 313-314 and limits lines 323-325, 358-359
- **issue:** The proposal cites `CR-001` and `CR-002` as if they were
  completion-ledger rows in the Tower 28 report. Section 10 contains request
  rows `REQ-001` and `REQ-002`; those descriptions merely refer to scan-side
  `CR-001` and `CR-002`. The CR tokens appear elsewhere only as access-limit
  annotations, not report rows with status, owner, and description.
- **evidence:** Tower 28 Section 10 lines 1406-1418; repository search of the
  report finds CR mentions but no CR row.
- **strongest defense:** A reader familiar with the scan receipt may resolve the
  external CR lineage. The commission explicitly requires every cited ID to
  resolve in the Tower 28 report, and the proposal's source pack does not make
  the scan receipt part of the worked card.
- **impact:** Provenance breaks at the exact next-observable/capture boundary,
  and the card can send an executor to a non-row identifier.
- **minimum_closure_condition:** Every report citation must use the actual
  report row (`REQ-001`/`REQ-002`) or explicitly identify and load the external
  scan artifact that owns the CR row.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Cite the Tower report's request IDs in the card
  and treat scan CR identifiers as nested provenance, not report rows.

#### AR-13 — D4's semantic-mispointing guard is asserted, not designed

- **phase:** correctness
- **severity:** major
- **confidence:** high
- **location:** D4 structural rule 2, lines 263-266; worked card lines 301-304
- **issue:** Requiring a clause after every ID does not make a mispointed ID
  visibly self-correcting; an author can write a fluent but broader clause. The
  worked example demonstrates the bypass: OBS-020 is turned into a
  concealer-specific no-breakout buy reason, and heterogeneous substitute rows
  are turned into corroborated defection pressure.
- **evidence:** Proposal rule at lines 263-266 versus OBS-020 and the worked
  buy-reason/substitute cells.
- **strongest defense:** Manual verification against the ledger can catch the
  defect. That is a review instruction, not a structural property of the card,
  and it failed in the example that claims every row was directly verified.
- **impact:** D4 does not catch what it claims to catch; a contract adopter can
  satisfy the format while laundering semantics.
- **minimum_closure_condition:** The design must state the actual semantic check
  and its ceiling without claiming the clause format itself prevents
  mispointing.
- **next_authorized_action:** Owner adjudication or a separately authorized
  proposal patch.
- **recommended correction:** Require the clause to stay within the row's
  excerpt, time anchor, fact domain, and ambiguity limitation, and describe this
  as author/review discipline rather than an automatic structural catch.

### Minor

- **AR-14 | minor | high | D1 L2, line 83 |** “Which heroes hold” implies
  temporal durability from a point-in-time aggregate rating state. **Advisory
  direction:** say which products are observed higher/lower at the read date.
- **AR-15 | minor | medium | D2 admission rule, lines 108-115 |** “Verified
  purchase where the surface exposes that marker” can mean either “record the
  marker when present” or “exclude all non-verified reviews,” producing
  different samples. **Advisory direction:** choose one reading and make it
  part of the stated sample definition.
- **AR-16 | minor | high | worked mechanism sentence, line 292 |** “Flagship”
  is not an observed Tower 28 row value; brand-labeled Bestseller and
  brand-supplied top-3 are weaker, specifically bounded claims. **Advisory
  direction:** use “hero selected for this example” or cite only the observed
  labels.

## Provenance accuracy audit

| Cited ID | Actual row disposition | Semantic match to proposal use |
| --- | --- | --- |
| OBS-001 | Current Tower 28 homepage mission copy, observed 2026-07-16 | Matches sensitive-skin mission; does not by itself make Swipe-specific buyer motive |
| OBS-003 | Current brand ingredients/philosophy page; no `non-comedogenic` wording | Matches current brand-page avoidance; only supports divergence against the historical customer-quoted retailer wording |
| OBS-004 | Current DTC catalog state | Exact match for Swipe `$24`, `21 shades`, and brand-labeled Bestseller |
| OBS-008 | Current Sephora assortment state | Matches Swipe `$24` and observed makeup assortment; no performance or sell-through support |
| OBS-009 | Current Sephora aggregate rating/count state | Exact match for `4.34 (3,652)`; reception proxy only |
| OBS-012 | BeautyMatter article published 2026-04-30 | Matches the brand-supplied top-3 Sephora NA concealer claim; one origin and unaudited |
| OBS-017 | Reddit listing title published 2026-06-06 | Exact match for the dated rejection title and companion title-level threads; bodies unread |
| OBS-020 | Eczema-community listing titles | Mismatch for “buyers want a concealer that won't break them out”; supports venue relevance only |
| OBS-021 | Pale-olive request title published 2026-01-05 | Matches historical edge exclusion; no current-pressure or switching-volume support |
| OBS-023 | Browser-read community complaint published 2024-04-25 | Matches the named complaint, quoted then-PDP wording, and 2025 sidebar recurrence pointers; does not verify the customer's ingredient assertion or current Sephora copy |
| OBS-024 | Independent blog review published 2026-04-16 | Matches one reviewer's positive eczema experience and preference for Typology; gifting status and independence unproven |
| OBS-025 | Undated search-index TikTok topic titles | Matches unverified breakout-theme existence; no content, date, volume, or authenticity support |
| OBS-026 | Undated YouTube comparison titles | Matches comparison/value-skepticism genre; `current_state_use: not_applicable`, content and dates largely unverified |
| OBS-027 | Dupe aggregator/search state observed 2026-07-16 | Exact match for NYX `$12` versus Swipe `$24`; page citing, not switching |
| GAP-008 | Open coverage gap in Section 10 | Exact match: Sephora per-review text sampling not performed |
| CR-001 | No CR row in the Tower 28 report | Untraceable as a report-row citation; appears only as a scan-side token inside limitations and REQ-001 text |
| CR-002 | No CR row in the Tower 28 report | Untraceable as a report-row citation; appears only as a scan-side token inside limitations and REQ-002 text |
| REQ-004 | Requested bounded scan extension in Section 10 | Matches future per-review sampling, but also includes AEO work and is not completed |

### Quoted figure and date trace

| Value | Trace result |
| --- | --- |
| `$24` Swipe | Traced to OBS-004, OBS-008, and OBS-027 |
| `$12` NYX | Traced to OBS-027 |
| `21 shades` | Traced to OBS-004 |
| `4.34 / 3,652` | Traced to OBS-009 |
| `2024-04-25` | Traced to OBS-023 publication date; it dates the complaint post, not the breakout event or current PDP state |
| `2026-06-06` | Traced to OBS-017 publication date and title excerpt |
| 2025 recurrence pointers | Traced to OBS-023 sidebar pointers (`2025-07-21` creasing and further `2025-06` concealer threads); those thread bodies were unread |

No cited figure above was untraceable. The material date failure is not an
incorrect literal date; it is the proposal's loss of the 2024 source anchor
when it rewrites quoted retailer copy in present tense.

## Considered and defended

- **Candidate: the worked complaint cell states a bare complaint rate.**
  **Defense held:** it states one verified instance plus one unread title and
  explicitly says no sampled proportion; GAP-008 is correctly cited.
- **Candidate: amplification numerically inflates prevalence.** **Defense
  held:** the D3 table contains no multiplier and repeatedly says the marker is
  decision weight, not incidence. The separate overclaim in the worked
  consequence is reported in AR-08.
- **Candidate: the standing category-background sentence creates forbidden
  comparator tracking.** **Defense held:** it explicitly says no comparator
  base rate is tracked or claimed, matching ledger item 4.
- **Candidate: the D4 card necessarily creates uncommissioned schema.**
  **Defense held:** the proposal consistently frames cells and confidence marks
  as presentation guidance. The unresolved durable insertion problem is limited
  to the commissioned D2 row and is reported in AR-11.
- **Candidate: the undated TikTok theme is presented as a current trend.**
  **Defense held:** the complaint cell calls it unverified indexed theme
  evidence and does not assign a date or volume.
- **Candidate: monitoring cadence drift.** **Defense held:** the proposal is
  explicitly point-in-time and names co-movement/monitoring as out of scope.

## Source-read ledger

| Source | Actual disposition | Authority/evidence use | Revision state |
| --- | --- | --- | --- |
| `AGENTS.md` | full | Project behavior and write boundary | Clean at `ae2890e6` |
| `.agents/workflow-overlay/README.md` | full | Overlay entrypoint | Clean at `ae2890e6` |
| `.agents/workflow-overlay/source-of-truth.md` | full | Source hierarchy and conflict rule | Clean at `ae2890e6` |
| `.agents/workflow-overlay/source-loading.md` | targeted: source packs, targeted-read protocol, High-Context Guard | Read-budget control | Clean at `ae2890e6` |
| `.agents/workflow-overlay/review-lanes.md` | expanded from targeted to full | Lane authority, severity/confidence, provenance, report destination, review-use boundary | Clean at `ae2890e6` |
| `.agents/workflow-overlay/artifact-roles.md` | targeted: role bindings and failure states | Review-report role and permitted destination | Clean at `ae2890e6` |
| `.agents/workflow-overlay/communication-style.md` | targeted: CA consumption and adversarial summary | Closeout shape | Clean at `ae2890e6` |
| `.agents/workflow-overlay/retrieval-metadata.md` | targeted: applicability through review checks | Durable report header | Clean at `ae2890e6` |
| `workflow-adversarial-artifact-review` | full, reference-loaded before evidence; applied only after `SOURCE_CONTEXT_READY` | Task-local review mechanics | External skill; not Forseti authority |
| `workflow-deep-thinking` | full | Required adversarial reasoning discipline | External skill; not Forseti authority |
| Proposal | full | Commission-bound review target | Clean, SHA-256 recorded above |
| Adjudication ledger | full | Binding owner rulings, especially items 4, 9, 10, 12 | Clean, SHA-256 recorded above |
| Tower 28 v1 report | targeted Section 4 exact rows for every cited OBS; targeted Section 10 completion rows | Semantic provenance and quoted-value trace | Clean, SHA-256 recorded above |
| CSB prompt structure | targeted lines 694-900 | Existing company-output contract and insertion seam | Clean, SHA-256 recorded above |
| Optional commissioning handoff | skipped: prompt says non-blocking; ledger and proposal provenance carry the commission | None | Not read |

**Checks not performed.** The review did not re-browse the original public URLs,
revalidate live page state, inspect the separate scan receipt that owns the
CR identifiers, perform new scanning or capture, sample Sephora review bodies,
or verify whether Polyglyceryl-3 Diisostearate is comedogenic. Those omissions
are deliberate review boundaries, not implied passes.

**Read-budget audit:** initial dispositions were followed except
`review-lanes.md` expanded from targeted to full because the formal lane
binding, provenance fields, and report rules were distributed across its
sections; `source-of-truth.md` and the targeted artifact-role section were
added because source hierarchy and durable report role were load-bearing.
Tower 28 remained targeted to every cited row and quoted-value anchor; the
optional handoff remained skipped.

## Review-use boundary

This is a read-only adversarial review. Findings and defended candidates are
decision input for the Chief Architect's adjudication only. They are not
approval, validation, product proof, mandatory remediation, or executor-ready
instructions. No `patch_queue_entry` is emitted, and no source artifact was
edited.
