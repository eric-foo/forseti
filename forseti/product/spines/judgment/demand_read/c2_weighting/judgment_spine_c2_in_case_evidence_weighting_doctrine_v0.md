# Judgment-Spine C2 In-Case Evidence-Weighting Doctrine v0 (PROPOSED — how a model is told to weight presented evidence on its merits)

```yaml
retrieval_header_version: 1
artifact_role: Implementation-facing behavior/contract spec (PROPOSED merits-basis instruction doctrine — what a judgment read must be instructed to do when assigning qualitative weight to presented evidence; binds no case, builds nothing, runs nothing)
scope: >
  The market-agnostic doctrine for the IN-CASE MERITS half of C2 weighting: how
  a model performing a judgment read is instructed to assign a qualitative,
  decision-relative weight to each presented evidence item from the item's own
  properties — the half the C2 ledger read contract names ("weights the signal
  on its in-case merits") but does not specify. Owns the decision-relative
  fitness principle (no static source ladder), the merits axes, the per-item
  trace obligations, the load-bearing partition C3's weakest-evidence cap
  consumes, the model-facing instruction core, and the named failure modes.
  Consumes by pointer: the C1 gate, C2 de-correlation/divergence sub-steps, the
  ledger read contract (reliability prior + Rule 3), and the C3 verdict/ceiling
  contract.
use_when:
  - Authoring or reviewing a judgment prompt that instructs a model to weight presented evidence (Level 1 backtest reads, demand reads, sealed contestant calls).
  - Auditing whether a reasoning trace weighted evidence decision-relatively on stated merits rather than by source prestige, volume, or fluency.
  - Deciding whether a weighting behavior belongs to the merits basis (here), the reliability prior (ledger read contract), or cross-item structure (C2 a/b).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md   # the sibling half: reliability prior, caveat travel, Rule 3 risk-state weighting
  - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md # the C0-C4 core whose C2 this instructs; INV-1..6
  - forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md # consumes the load-bearing partition (weakest-evidence cap)
  - forseti/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md # first intended consumer surface (c2_weighting trace slots)
stale_if:
  - The owner lifts the no-scoring boundary (INV-1); numeric weighting becomes admissible and the qualitative-only obligations here relax.
  - The core architecture amends C2's step shape or moves the merits basis to another step.
  - The C2 ledger read contract materially amends the shared seams consumed here (per-case justification, caveat classification, band tolerance, Rule 3 scope).
  - The C3 contract changes or retires the weakest-load-bearing-evidence cap the partition feeds.
  - The owner adjudicates this proposal (adopt / amend / reject).
```

## Status

`PROPOSED` — merits-basis instruction doctrine, `product_learning` tier. It
**stabilizes what a judgment read must be told to do** when it assigns weight to
presented evidence; it **binds no case, authors no prompt, runs no read, edits
no sibling contract, and mints no numeric weighting.** Authored 2026-07-10 in
the judgment evidence-weighting lane (worktree
`judgment-evidence-weighting-d1fd49` off `origin/main`) on owner request for a
"harness / basic level / doctrine of how to tell a model to effectively assign
weights to evidence presented."

## The Gap This Fills

The C2 ledger read contract fixes how the reliability **prior** is read
(track-record tally → qualitative prior, caveats travel, Rule 3 risk states).
Its absence rule then says: with no ledger row, "C2 weights the signal on its
**in-case merits**." Nothing in the spine specifies what in-case-merits
weighting is or how a model is instructed to do it.

The merits basis is not only the no-row fallback. Even with a ledger row, the
prior "informs — but never determines" the weight; the required per-case
justification **is** a merits read. So every weighted item always carries a
merits basis; the ledger prior and any fired lesson modulate it. This doctrine
owns that basis. Per weighted item:

```text
weight-in-trace = merits basis (THIS DOCTRINE)
                  interpreted with the reliability prior   (ledger read contract)
                  and any fired lesson override            (near-half lesson library)
                  under cross-item structure               (C2 a de-correlate / b divergence)
```

Each contributor stays a **separate trace entry** (the sibling's
double-counting guard, extended): merits, prior, and lesson are never merged
into one inflated weight.

## Core Principle — Weight Is Decision-Relative Fitness

**A weight is a property of the triple (evidence item, claim, decision frame) —
never of the source class alone.** The same source is weak for one claim and
load-bearing for another:

- Decision frame: "does ingredient X cause benefit Y?" — a Reddit thread of
  user anecdotes is remote testimony about a causal claim its authors cannot
  competently observe. Weak context at best; never load-bearing.
- Decision frame: "is there real, organic user demand / complaint volume for
  X?" — the same thread **is close to the phenomenon itself** (people
  organically talking is the thing being measured). With independence and
  integrity checks it can be load-bearing.

Therefore a **static source ladder is prohibited in both directions**. A fixed
source-class → weight mapping ("peer-reviewed = high, forum = low" — or its
inverse, "Reddit = authentic = high") fails twice: it is decision-blind, and it
is a deterministic apply-rule, which INV-1 forbids. Source identity may enter
the weight only through the merits axes below, derived per case and explained
in the trace.

The read derives, per item: *what would strong evidence for this claim look
like, and how close does this item come?* — it never looks the answer up.

## The Merits Axes

The derivation vocabulary. Axes are **not a scorecard**: no per-axis scores, no
summation, no fixed order of importance. The trace cites the axes that
materially move the item's weight, with reasons; axes that do not move it need
no mention.

| Axis | Question the read answers | What moving it looks like |
| --- | --- | --- |
| **Role fit** | For the claim this item bears on, what would strongly probative evidence look like, and is this item that kind of thing? | The governing axis; the others refine it. An item excellent in general but unfit for this claim carries little here. |
| **Proximity** | Relative to this claim, is the item the phenomenon itself, a direct trace or measurement, first-hand testimony, a secondhand report, an aggregation, an interpretation/opinion, or promotion? | Closer can carry more; remote placement caps what the item can carry regardless of polish. Placement is claim-relative: the same Reddit post is "the phenomenon" for a demand claim and "remote hearsay" for a causal claim. |
| **Competence** | Could this source actually observe or measure what it asserts? | A user competently reports their own purchase or experience; the same user cannot competently report market-wide prevalence or causation. Claims beyond the source's vantage are discounted to what the vantage supports. |
| **Incentive skew** | Does the source gain from the claim being believed (vendor, affiliate, PR-seeded, engagement-farming)? | Ordinary bias is a stated **discount**, not a defeater. A **dispositive integrity risk** — the demand may not be real (bots, coordination, staging) — is not weighed here: route to Rule 3 in the ledger read contract / the C1 gate. |
| **Checkability** | Does the item carry checkable specifics (dates, quantities, artifacts, links) — and were any checked? | Checked specifics can raise carry; unfalsifiable vibes cap low however confident the prose. |
| **Selection exposure** | How did this item reach the read — what did the venue, ranking algorithm, or scan query select for? | Genuine items can still be unrepresentative (complaint-selecting venues, virality-selected posts, query-echo). Selection exposure discounts prevalence-type claims hardest. |
| **Temporal fit** | Does the item's time window fit the decision horizon? | Consumes the core's recency rule: same-strength newer signals normally deserve more read attention than older context — an attention/relevance input, never a numeric rule or gate proof. |

Within equal proximity, **gradeable costly behavior outranks talk**: what an
actor paid, risked, or gave up carries more than what anyone merely said
(buyer-proof costly-behavior rule, consumed; the C3 contract owns its ceiling
consequences — engagement/resonance-only evidence cannot carry Commit-grade).

## Required Behavior

When a judgment read weights presented evidence, it must:

1. **Derive before weighing.** For each item, name the claim inside the
   decision frame the item bears on, and state in one line what strongly
   probative evidence for that claim would look like (the **fitness target**).
   Place the item against the fitness target. An item bearing on several
   claims is weighed per claim, not once globally. This obligation is what
   makes "for this decision, Reddit isn't that empirical" a derived, auditable
   statement instead of a prejudice.
2. **Weigh the item, not the source class.** Source identity contributes only
   through the merits axes, derived per case. No static ladder in either
   direction (prestige or anti-prestige).
3. **State the moving axes.** Cite, with a one-line reason each, the axes that
   materially moved this item's weight. Classify every consideration whose
   bearing is genuinely uncertain as **cap / discount / neutral, with the
   reason** — the sibling contract's ambiguity rule, applied to the merits
   basis. A consideration that silently moves, or silently fails to move, a
   weight is non-compliant.
4. **Emit direction, qualitative level, and role.** Per item: `direction`
   (supports / opposes / hedges), a qualitative weight level in words with its
   justification, and the **load-bearing partition** — `load_bearing` /
   `supporting` / `not_relied_on`, each with a reason. The partition is the
   output C3's weakest-load-bearing-evidence cap consumes: the verdict's
   ceiling rests on the weakest `load_bearing` item, so overweighting surfaces
   as an inflated ceiling and is auditable there.
5. **Honor the band tolerance.** The reproducible outputs are direction +
   reasoning + partition. The level carries the two-sided ≈one-band tolerance
   (owner decision 2026-06-14, consumed from the sibling): faithful re-reads
   may sit one band apart without conflict when direction, load-bearing facts,
   and counterfactual agree. Consistency is judged on direction + reasoning,
   never exact level.
6. **Weigh before the verdict.** Weights are assigned before the verdict is
   formed, and no weight rationale may cite the verdict or the desired action
   ("strong because the call needs it" is a defect). The trace must read
   correctly in evidence-first order.
7. **Never average opposed strong items.** Strong-supports plus strong-opposes
   does not yield a moderate weight or a hedged middle verdict by arithmetic
   of any kind. Conflict between strong items is information: flag it as
   divergence (C2 sub-step b owns the mapping) and carry it into the verdict's
   confidence and the C4 counterfactual.
8. **Name the missing evidence.** Per read, state which evidence the decision
   frame needed that the presented set lacks, and which single missing item
   would most change the assigned weights. Absence lowers what the present set
   can carry — never silently. (Feeds C4; C4 owns the counterfactual step.)
9. **Keep merits, prior, and lesson as separate entries.** Where a ledger
   prior or a fired lesson also informs an item, the trace carries each at its
   own level alongside the merits basis — never summed, merged, or treated as
   mutually reinforcing into a single inflated weight (extends the sibling's
   double-counting guard).
10. **Keep stakes out of weights.** Irreversibility and stakes raise the
    sufficiency bar at C3 (and harden Rule 3's FP/FN asymmetry for integrity
    risks); they never raise an item's evidential weight. Weight = what this
    item can carry; sufficiency = whether the carried set clears the
    decision's bar. The two must not be blended in the trace.

## The Instruction Core (the harness block)

The model-facing instruction content a judgment prompt embeds verbatim or cites
in full. It is instruction **content**, not a prompt artifact: it has no
receiver, run, or output mode of its own, and prompt authoring that carries it
still applies the prompt contract (`.agents/workflow-overlay/prompt-orchestration.md`).

```text
EVIDENCE-WEIGHTING INSTRUCTION CORE
(owning doctrine: judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md)

For every evidence item you are given, before forming any verdict:

1. Name the claim inside the decision frame this item bears on. An item
   bearing on several claims is weighed per claim, not once globally.
2. State, in one line, what strongly probative evidence for that claim would
   look like. This is the fitness target. Judge the item against the fitness
   target — never against a general source-quality ladder. The same source
   can be near-worthless for one claim and load-bearing for another.
3. Place the item relative to this claim: the phenomenon itself, a direct
   trace or measurement, first-hand testimony, a secondhand report, an
   aggregation, an interpretation or opinion, or promotion. Closer placement
   can carry more; remote placement caps what the item can carry, however
   polished it reads.
4. Check — and mention only where it materially moves this item: could the
   source actually observe what it asserts (competence); does it gain from
   being believed (incentive); does it carry checkable specifics, and were
   they checked (checkability); what did the venue, algorithm, or search
   that surfaced it select for (selection); does its time window fit the
   decision horizon (temporal fit)?
5. Prefer gradeable costly behavior over talk: what an actor paid, risked,
   or gave up outranks what anyone merely said, at equal placement.
6. Classify every consideration whose bearing is uncertain as cap, discount,
   or neutral — with the reason. A consideration that silently moves, or
   silently fails to move, a weight is a defect.
7. Assign, in words, not numbers: direction (supports / opposes / hedges), a
   qualitative weight level with a one-line justification, and the role —
   load_bearing / supporting / not_relied_on, with a reason. Numeric or
   ordinal scores, formulas, and source-class lookup tables are prohibited.
8. Do all of the above before forming the verdict. A weight justified by the
   conclusion it enables is a defect.
9. Never average opposed strong items into a middle weight or a hedged
   middle verdict. Conflict between strong items is information: flag the
   divergence and carry it into the verdict's confidence and the
   counterfactual.
10. If a known integrity risk could mean the signal is not real (bots,
    coordination, staging), do not weigh it here — route it to the
    risk-state rule (Rule 3, C2 ledger read contract).
11. End with: the load_bearing items (the verdict's ceiling rests on the
    weakest of these); the strongest item you discounted and what would make
    it strong; and the missing evidence that would most change these
    weights.
```

Prompts should cite this doctrine rather than fork the wording; a prompt that
must trim for context keeps obligations 1–2, 6–8, and 11 at minimum and cites
the rest by pointer. Trimming is a prompt-authoring decision under the prompt
contract, not a change to this doctrine.

## Named Failure Modes

The audit vocabulary. A trace exhibiting any of these fails the merits-basis
audit (Acceptance Criteria below):

- **FM-1 Static source ladder.** Weight read off source class, in either
  direction ("peer-reviewed so strong" / "Reddit so authentic"), without a
  per-claim fitness derivation.
- **FM-2 Volume-as-weight.** Count of similar items treated as strength
  without independence; owned by C2 sub-step (a) — listed here because it
  surfaces in merits traces as "many posts say."
- **FM-3 Fluency-as-weight.** Confident, detailed, well-written prose weighted
  above hesitant primary testimony with no axis cited beyond polish.
- **FM-4 Conflict averaging.** Opposed strong items resolved into a middle
  weight or hedged verdict instead of a flagged divergence.
- **FM-5 Verdict-referencing rationale.** A weight justified by the conclusion
  it enables, or weights visibly assigned after and fitted to the verdict.
- **FM-6 Silent movement.** A weight that moved (or conspicuously did not)
  with no stated reason; an ambiguous consideration left unclassified.
- **FM-7 Numeric weighting.** Scores, percentages, formulas, ordinal ranks, or
  any arithmetic on weights (INV-1 violation).
- **FM-8 Prevalence leap.** Testimony or venue chatter read as population
  statistics without competence/selection discounts ("everyone is
  complaining").
- **FM-9 Absence blindness.** Only presented items weighed; no statement of
  what the decision needed but the set lacks.
- **FM-10 Cross-claim weight transfer.** An item's earned weight on one claim
  reused on a different claim without re-derivation (a source strong on "users
  are talking" quietly treated as strong on "the product works").

## Worked Contrast (canonical example)

Same evidence item, two decision frames — the derivation, not a rule about
Reddit:

| | Frame A: "ingredient X causes benefit Y" | Frame B: "organic user demand exists for X" |
| --- | --- | --- |
| Fitness target | Controlled comparison or expert synthesis of such | Unprompted real-user activity at cost or effort |
| Placement of a 40-comment Reddit thread | Remote: anecdotes about a causal mechanism authors cannot observe | Near: the thread **is** the phenomenon (organic talk), some comments carry costly behavior (repurchase reports) |
| Moving axes | Competence (vantage cannot support causation), selection (virality) | Selection (venue amplifies complaints/hype), integrity → route Rule 3, independence → C2(a) |
| Weight outcome | `not_relied_on` for the causal claim; at most weak context | Candidate `load_bearing` for the demand claim after de-correlation and Rule 3 clear |

Satellite preview (illustrative, non-binding — the fragrance rubric slot stays
satellite-owned): for a "durable fragrance demand" claim, Fragrantica hype
threads are talk (resonance; caps low), restock-tracking and documented
sell-throughs are costly behavior (can carry Commit-grade under C3's
independence rules).

## Acceptance Criteria

- **Fitness derivation present:** for each weighted item, the trace names the
  claim and the fitness target before the weight; a trace that weights by
  source class with no per-claim derivation fails (FM-1).
- **Partition present and consumed:** every item carries
  `load_bearing / supporting / not_relied_on` with a reason, and the verdict's
  ceiling cites the weakest `load_bearing` item; a verdict ceiling resting on
  an item the trace did not mark load-bearing fails.
- **Moving axes stated:** each weight cites its moving axes with reasons;
  ambiguous considerations are classified cap/discount/neutral; silent
  movement fails (FM-6).
- **Verdict-blind rationale:** no weight rationale references the verdict or
  desired action; weights precede the verdict in the trace (FM-5).
- **No conflict averaging:** opposed strong items produce a flagged divergence,
  never an averaged middle (FM-4).
- **Entry separation:** where a ledger prior or lesson also informed an item,
  merits, prior, and lesson appear as separate entries; a single merged weight
  fails.
- **Missing-evidence line present:** the read states what the decision needed
  that the set lacks (FM-9).
- **INV-1 disqualifier:** no numeric/ordinal weight, formula, arithmetic, or
  source-class lookup anywhere in the weighting trace (FM-7); an auditor must
  find interpretation, not computation.
- **Band tolerance honored:** two faithful reads agreeing on direction,
  load-bearing facts, and partition that differ by one qualitative band are
  both compliant; failing an adjacent-band read on level alone is itself a
  violation.
- **Rule 3 routing:** a dispositive integrity risk weighed as an ordinary
  incentive discount here (instead of routed to Rule 3) fails; an ordinary
  bias escalated to a cap without the Rule 3 basis also fails.

## Enforcement Posture

These are **trace obligations audited as judgment, not gated as code** — the
same posture as the sibling contract's items 7–8 and INV-1 itself (read the
trace; run no scorer):

- **Per read:** a review / tell-audit of the reasoning trace flags any FM-1
  through FM-10 pattern; such a trace fails review.
- **Pre-use and ongoing:** the blind paired-read method (probe v2, consumed
  from the sibling): run the same case under ≥2 framings; pass requires
  agreement on direction + load-bearing facts + partition, the level within
  the two-sided tolerance, and every band difference attributable to a
  declared classification, not silent drift.

## Non-Goals

- **No numeric/ordinal weighting, formula, or deterministic apply-rule**
  (INV-1; graduates only when the owner explicitly lifts the no-scoring
  boundary).
- **No ownership of the sibling seams:** the C1 gate, C2 sub-steps (a)
  de-correlation and (b) divergence, the C2(c) ledger read (prior, caveat
  travel, Rule 3), the lesson library, the C3 verdict/action ceiling, and the
  C4 counterfactual are consumed by pointer, not restated or amended.
- **No per-vertical source rubric.** Which venues matter for fragrance (or any
  vertical) and their discriminator tells are the satellite's rubric slot;
  this doctrine is the market-agnostic method that rubric instantiates.
  Satellites add domain instances and tells, not new axes or new arithmetic.
- **No level lexicon minted.** Weight levels are stated in plain qualitative
  words under the band tolerance; a fixed mandatory level enum is deliberately
  not created (it would drift toward an ordinal scale).
- **No prompt artifact, no run, no build.** This doctrine authors no prompt,
  authorizes no case run, and creates no schema field; trace obligations ride
  inside the existing free-text trace surfaces (e.g., the satellite skeleton's
  `qualitative_read` / `direction_reasoning`), and any schema extension is the
  skeleton owner's call.
- **No retroactive grading authority.** Past reads are not re-graded by this
  doctrine's arrival; it governs reads instructed under it.

## Interfaces

- **Weighting unit:** the obligations apply to whatever granularity the mode
  presents — an allowed signal, or the evidence items carrying it (packet
  `EvidenceUnit`-level in backtest mode). Each weighed thing gets the same
  derivation; a signal's weight rests on its items' merits.
- **Mode placement:** the mode shells own where the reading surface sits (the
  sealed C3/C4 contestant over a frozen packet in backtest; the sealed call in
  live). This doctrine governs the instruction content for that surface,
  wherever the shell puts it; it does not move the isolation topology.
- **Output surface:** the C2 merits portion of the required reasoning trace —
  per item: claim + fitness target, moving axes with reasons, ambiguous-
  consideration classifications, direction, qualitative level, partition role;
  per read: divergence flags (by pointer to C2(b)), missing-evidence line, the
  steelman line (strongest discounted item and what would make it strong).
- **Downstream consumer:** C3 reads the partition (`load_bearing` set) for its
  weakest-evidence ceiling cap; C4 reads the missing-evidence line.
- **Prompt consumption:** judgment prompts embed or cite the Instruction Core
  and apply the prompt contract; the `docs/prompts/**` preflight and
  provenance rules are unchanged by this doctrine.

## Open Questions

- **Default level lexicon — deliberately open.** Free qualitative wording plus
  the band tolerance is the v0 position (a minted enum risks ordinal drift).
  Revisit only if paired-read audits show cross-read legibility failures
  attributable to wording variance, and then as an owner decision.
- **Axis extensions.** Whether satellites may propose additional merits axes
  (versus only domain tells under the existing axes) is deferred to the first
  satellite rubric that needs one; default is tells-only.

## Source-Read Ledger

- `forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md`
  — full read; the sibling half consumed here (per-case justification seam,
  absence rule, caveat classification, band tolerance, Rule 3 scope,
  enforcement posture).
- `forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md`
  — full read; C2 step shape (a/b/c), INV-1..6, recency-attention rule,
  isolation topology, costly-behavior and engagement-cap language.
- `forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
  — targeted read (weakest-load-bearing / independence-cap sections) to align
  the partition output with the cap that consumes it.
- `forseti/product/spines/judgment/judgment_current_state_and_decomposition_v0.md`
  — full read; core-vs-satellite weighting ownership, SCV loop, claim caps.
- `forseti/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md`
  — targeted read (weighting slots and boundary lines) for the first consumer
  surface and its field names.
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` — full
  read; orientation and routing conventions.
- `forseti/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md`
  — targeted check (no weighting/credibility language found; no conflict).
- `.agents/workflow-overlay/README.md`, `decision-routing.md`,
  `artifact-folders.md`, `prompt-orchestration.md`, `validation-gates.md`,
  `retrieval-metadata.md`, `source-loading.md` (preflight receipt shape) —
  overlay authority for placement, routing, prompt boundary, gates, and
  header contract.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: C2 in-case evidence-weighting doctrine (merits-basis instruction contract)
  source_quality_state: design/control artifacts only (sibling C2 contract, core architecture, C3 contract, decomposition map, satellite skeleton — read fresh in-lane); no read has run under this doctrine
  execution_quality_state: no judgment read executed under these instructions; no trace audited against the failure modes; no paired-read test run
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no read exists to test against; adversarial review of this doctrine not yet run; owner adjudication pending
  receipt_artifact_or_gap: first real test comes from a Level 1 or demand-read trace authored under a prompt that carries the Instruction Core, audited against the Acceptance Criteria (owner-gated)
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    New PROPOSED core surface: the in-case merits half of C2 weighting now has
    an owning doctrine (decision-relative fitness principle, merits axes,
    per-item trace obligations, load-bearing partition, model-facing
    Instruction Core, named failure modes). The current-state/decomposition
    map's Weighting row and open_next are refreshed to route to it. Owner-directed
    cold-start findability follow-up (2026-07-10, same lane): the Judgment
    consolidation map gains a Fast Route row for evidence weighting, and the
    sibling ledger read contract gains one retrieval-header open_next line to
    this doctrine (header-only; headers are retrieval_only and carry no
    authority). PROPOSED only — owner adjudication pending; adoption owes a
    dated pointer per the Doctrine-Change Propagation Contract.
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md
    - forseti/product/spines/judgment/judgment_current_state_and_decomposition_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md   # Fast Route row only (findability follow-up)
    - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md   # retrieval-header open_next line only (findability follow-up); doctrine body untouched
  downstream_surfaces_checked:
    - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md   # consumed by pointer; its absence rule now has an owning specification; not edited (consume, don't reopen)
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md # C2 step shape unchanged; merits basis sits inside existing C2 "qualitative, LLM-in-session, explained"
    - forseti/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md # weakest-load-bearing cap consumed unchanged; partition feeds it
    - forseti/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md # fields unchanged; rubric slot stays satellite-owned
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md # no weighting area row; routes via the decomposition map, which is updated
    - forseti/product/spines/judgment/demand_read/grading/judgment_spine_demand_read_grading_rubric_v0.md # no weighting/credibility language; no conflict
    - forseti/product/spines/judgment/demand_read/core/judgment_spine_first_demand_read_scope_v0.md # its C2 step says "weight on in-case merits" per the C2 contract — a consumer of the seam this doctrine specifies; consistent, not edited
  intentionally_not_updated:
    - path: forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md (doctrine body)
      reason: settled reviewed spec; its "in-case merits" line is a seam this doctrine fills by pointer, not a defect to edit. The findability follow-up added one retrieval-header open_next line only; no Required Behavior, rule, or non-goal text changed.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: stays thin by convention (the current-state map's own rule); it already routes Judgment work to the consolidation map and names demand_read/c2_weighting at directory level.
  stale_language_search: >
    rg -in "in-case merits|in_case_evidence|static source ladder|source-quality ladder"
    forseti/product/spines/judgment docs/research/judgment-spine
  stale_language_search_result: >
    Executed 2026-07-10 after edits. Hits: this doctrine (13 — its own subject
    language), the sibling ledger contract (3 — intended-keep "in-case merits"
    seam lines), the refreshed decomposition-map Weighting row (1), and
    judgment_spine_first_demand_read_scope_v0.md (1 — its C2 step instruction
    "weight on in-case merits" per the C2 contract, a consumer of the seam this
    doctrine now specifies; consistent, not edited). docs/research/judgment-spine:
    zero hits. No surface carries a static source ladder or a conflicting
    merits-weighting rule.
  non_claims:
    - not validation
    - not readiness
    - not owner adoption
    - not a live fold to origin/main (per-lane PR pending)
```

## Non-Claims

- Instruction doctrine only; binds no case, authors no prompt, runs no read,
  builds no schema, edits no sibling contract, and does not move the isolation
  topology.
- Mints no evidence-ladder vocabulary and no numeric or ordinal weighting;
  INV-1 holds — traces show interpretation, never arithmetic.
- A weight assigned under this doctrine is `product_learning` reasoning about
  evidence use — never judgment-quality evidence, source-family admission,
  validation, or proof.
- PROPOSED only; not owner-adopted. On adoption it owes a dated pointer via
  the Doctrine-Change Propagation Contract
  (`.agents/workflow-overlay/source-of-truth.md`).

```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
