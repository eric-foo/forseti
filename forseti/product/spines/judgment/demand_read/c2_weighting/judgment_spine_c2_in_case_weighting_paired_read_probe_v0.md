# Judgment-Spine C2 In-Case Weighting Paired-Read Probe v0 (PROPOSED — blind paired-read test of the Instruction Core)

```yaml
retrieval_header_version: 1
artifact_role: Feasibility probe (design/docs experiment — tests whether the in-case evidence-weighting doctrine's Instruction Core, embedded verbatim in a model-facing prompt, produces decision-relative merits weighting and framing-stable reads; binds no case, populates no ledger, runs no production machinery)
scope: >
  The owner-authorized "cheap probe" of
  judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md: one synthetic
  retail-demand case, eight evidence items with planted weighting traps, two
  isolated blind readers (Sonnet-tier subagents, fresh contexts, tools
  forbidden), one framing each (opportunity vs caution, different item order,
  identical item text), audited against pre-registered expectations and the
  doctrine's Acceptance Criteria / FM-1..FM-10. Method follows probe v2's blind
  protocol (author does not author the reads; readers blind to each other and
  to the test purpose).
use_when:
  - Checking whether the in-case weighting Instruction Core has any instruction-following evidence behind it, and at what claim tier.
  - Designing the next weighting probe or the first real-case read under the doctrine.
  - Auditing a weighting trace and wanting a worked example of the audit method.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md  # the doctrine under test
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_weighting_paired_read_probe_v1.md  # round two: the hardened-core re-run this Disposition anticipated
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_qualitative_read_feasibility_probe_v2.md   # the blind-protocol precedent this follows
stale_if:
  - The owner adjudicates the doctrine (adopt / amend / reject) — re-read which obligations survived before reusing this probe's expectations.
  - INV-1 (no-scoring boundary) is amended by the owner.
  - A later probe or real-case read supersedes these observations.
```

## Status

`PROPOSED` — design/docs feasibility experiment, `product_learning` tier. The
case is synthetic (`example_not_a_real_case`): the product, brand, venues, and
figures are constructed for the probe. **This binds no signal, admits no case,
populates no ledger row, runs no conductor gate, and edits no doctrine.**
Authored 2026-07-10 in the judgment evidence-weighting lane (worktree
`judgment-evidence-weighting-d1fd49`), on explicit owner authorization for the
cheap probe ("please, proceed with the cheap probe").

Pre-registration integrity: the Method, Case, and Pre-Registered Audit
Expectations sections below were written and committed **before** the author
consumed either reader's output. Observed Reads and Audit sections are filled
in a subsequent commit; the lane's commit history is the ordering evidence.

## Probe Question

Two properties of the doctrine's Instruction Core, embedded as-is in a
model-facing prompt with **no repo access**:

1. **Instruction-following:** does a mid-tier (Sonnet-class) reader produce the
   per-item derivation the doctrine requires — claim + fitness target before
   weight, placement, moving axes, cap/discount/neutral classifications,
   direction + qualitative level + `load_bearing / supporting / not_relied_on`
   partition, weights before verdict, closing steelman + missing-evidence
   lines — without exhibiting FM-1..FM-10?
2. **Framing stability (the doctrine's paired-read test):** across an
   opportunity framing and a caution framing of the same packet, do the reads
   agree on per-item direction, the load-bearing set, and verdict direction,
   with any level differences within one qualitative band and attributable to
   declared classifications?

## Method

- **Readers:** two isolated subagents (Claude Sonnet tier via the repo's
  pinned `worker` type), fresh contexts, spawned in parallel. Each received:
  the decision frame in its framing, the Instruction Core verbatim (one
  adaptation, below), and the eight-item packet. Each was forbidden to read
  files, repos, or the web and to use tools.
- **Blindness:** neither reader knows the other exists, that framing stability
  is being tested, that the items contain planted traps, or that an audit
  rubric exists. The author did not author the reads (probe v2's blind
  protocol).
- **Framings:** identical item texts, verbatim. Framing A ("opportunity"):
  items ordered E1→E8; question "should the retailer commit to the large
  reorder?" Framing B ("caution"): items ordered E5, E8, E2, E6, E3, E7, E4,
  E1 (concerns-leaning first); question "how much winter inventory exposure,
  if any, is justified?" **Named limitation (as in probe v2):** two manipulanda
  travel together — item order AND question valence — so any drift is
  attributable to the framing bundle, not to one factor.
- **Named deviation from verbatim embedding:** Instruction Core step 10 tells
  the model to "route it to the risk-state rule (Rule 3, C2 ledger read
  contract)" — a repo pointer a no-repo reader cannot resolve. The reader
  prompts replaced that clause with "flag it explicitly as an integrity risk
  requiring separate verification, and say what the verification would be."
  This is the trim/adapt behavior the doctrine's consumption rule permits, and
  it is itself probe evidence: the core's step 10 is not fully self-contained
  for no-repo readers.
- **Named caveats:** same model family across readers and auditor
  (Claude; readers Sonnet-tier, auditor the lane's main-tier model), single
  synthetic case, and the packet author is the expectation author. This probe
  therefore tests within-family instruction-following and framing stability on
  one constructed case — not model-independence, not multi-case reliability,
  not real-world accuracy.
- **Audit:** the author audits both traces against the Pre-Registered Audit
  Expectations below plus the doctrine's Acceptance Criteria and FM-1..FM-10.
  No numeric scoring anywhere (INV-1): the audit is a judgment read of the
  traces, recorded per criterion as met / not met / partial with cites.

## The Case (synthetic; `example_not_a_real_case`)

**Decision frame (shared):** a mid-size housewares retailer must decide within
two weeks about winter inventory for the "GripMug", a $34 insulated travel mug
from small brand Corvo that became popular on social media roughly three
months ago. Horizon: October–February. Overcommit → markdown losses;
undercommit → missed sales and possibly losing the allocation.

**Evidence items (verbatim as given to both readers):**

- **E1.** A thread on r/BuyItForLife with 240 comments accumulated over the
  past six weeks. Dozens of users post long-term use reports (3+ months) with
  photos of daily wear; several report buying second units as gifts; a few
  complain the lid gasket wears out. The thread was started organically by a
  user, not the brand.
- **E2.** A TikTok video with 2.1M views by a lifestyle influencer praising
  the GripMug's look and feel. The caption discloses "#ad — partner: Corvo".
  Comments are mostly emoji and "want one".
- **E3.** Three product-roundup blog posts on three different websites, each
  naming the GripMug "the travel mug of the year". Their product descriptions
  repeat several identical sentences; all three match wording in Corvo's
  downloadable press kit.
- **E4.** A report from an independent distributor covering 40 independent
  boutiques: the last three restock cycles each sold through in under 9 days
  at full price, with reorder requests from 31 of the 40 boutiques. Figures
  are dated within the past month and the distributor's report includes
  per-store tables.
- **E5.** A widely shared essay by a product-design commentator arguing the
  GripMug is "this year's fidget spinner": a fad that will crash. The essay
  reasons by analogy to two earlier viral drinkware products that collapsed
  after one season. It is well written and confident but cites no sales data
  for the GripMug itself.
- **E6.** Corvo's own Instagram account (480k followers) shows repeated
  "SOLD OUT — restock Friday" banners and stories of queues at a pop-up. All
  of this content is produced and posted by Corvo itself.
- **E7.** Google Trends: search interest for "GripMug" rose roughly 8x over
  ten weeks and has plateaued at about 5x the pre-viral baseline for the last
  two weeks.
- **E8.** A line from a 2019 industry report: "the insulated drinkware
  category is growing about 4% annually."

## Pre-Registered Audit Expectations (written before consuming any read)

Each item plants a specific temptation. Expected good-read behavior, per the
doctrine:

| Item | Planted temptation | Expected direction | Expected role | Expected reasoning marks |
| --- | --- | --- | --- | --- |
| E1 | The "Reddit both ways" test: prestige-ladder readers under-weight it; anti-prestige readers over-weight it | supports (current real demand; some durability signal) | `load_bearing` candidate (or strong supporting) | Near-phenomenon placement for a demand claim; costly behavior noted (repurchases, photos); selection caveat (BIFL venue selects durability enthusiasts) stated, classified discount/neutral |
| E2 | Fluency/engagement + disclosed incentive (FM-3 bait) | supports at most weakly | `not_relied_on` (or weak supporting) | #ad incentive discount stated; engagement-only (cheap talk) placement; must NOT be load-bearing |
| E3 | Volume-as-weight (FM-2 bait): three sites, one press-kit origin | supports at most weakly | `not_relied_on` | Shared origin recognized → treated as ~one promotional item, promotion placement; must not count as three independent supports |
| E4 | None (the anchor) | supports | `load_bearing` (expected weakest-of-set anchor or strongest item) | Costly behavior (full-price sell-through, reorders), checkable specifics, temporal fit; independence from E1 notable |
| E5 | Opposed + fluent (FM-3, FM-4 bait): confident essay, no product data | opposes (durability of demand) | supporting-level opposition (not load-bearing for the verdict; not silently dropped) | Placement interpretation/opinion-by-analogy; no product data noted; must NOT be averaged into a middle verdict — expected to surface as divergence feeding confidence + counterfactual/missing evidence |
| E6 | Integrity trap (step 10): self-reported scarcity can be staged | not weighed as support | routed out as integrity risk | Flagged as manufactured-scarcity risk requiring separate verification (e.g., independent sell-through confirms — which E4 partially provides; a good read may note that) |
| E7 | Attention ≠ demand | supports (attention sustained; durability hint from plateau above baseline) | supporting | Aggregation/direct trace of attention, not purchases; cannot carry commit-grade alone |
| E8 | Stale + wrong altitude (role-fit bait) | hedges/weak supports | `not_relied_on` | 2019 category-level stat: temporal fit and role fit discounts stated |

**Paired-read pass criteria (pre-registered):**

1. Per-item direction identical across A and B for all eight items.
2. The `load_bearing` set identical across A and B (expected: E4 certainly;
   E1 likely; nothing else).
3. Verdict direction identical (expected: commit-leaning with named hedges /
   meaningful exposure justified — not avoid, not unconditional maximal
   commit); the recommendation wording may differ with the framing's question.
4. Any per-item level difference within one qualitative band, and every band
   difference attributable to a declared cap/discount/neutral classification,
   not silent drift.
5. E5 flagged as divergence in both (not averaged, not dropped); E6
   integrity-routed in both; E3 collapsed to one origin in both.
6. No FM-1..FM-10 pattern in either trace; instruction-following marks
   present per item (claim + fitness target before weight; closing
   load-bearing/steelman/missing-evidence lines present).

**Pre-registered failure interpretation:** a miss on criteria 1–3 or a
repeated FM pattern = the Instruction Core does not yet operationalize the
doctrine at Sonnet tier (route: harden the core's wording, not the axes). A
miss only on level bands with declared classifications = the doctrine's
expected tolerance behavior (pass with the known one-band give). Auditor
misses (expectations wrong, not reads wrong) are recorded as expectation
errors, not read failures.

## Observed Reads (compressed per probe v2 convention; full verbatim traces attached to the lane PR as a comment)

Both readers produced complete per-item derivations (claim + fitness target
stated before every weight) and complete instruction-11 closings. Compressed
comparison — direction / qualitative level / role per reader:

| Item | Reader A (opportunity) | Reader B (caution) | Agree? |
| --- | --- | --- | --- |
| E1 Reddit thread | supports; substantial; **load_bearing** for quality/durability, not_relied_on for demand-trend ("no volume or trajectory data here") | supports; medium-high for organic-grounding + quality, medium for persistence; **load_bearing** for organic grounding | direction ✓; role set ✓ (both load-bearing; different primary sub-claim — see Finding P-2) |
| E2 TikTok #ad | nominally supports awareness; low; not_relied_on ("cannot discriminate real demand amplified from paid campaign manufacturing appearance") | nominally supports; low; not_relied_on (placement + incentive cap) | ✓ |
| E3 press-kit trio | "collapse to one promotional source reprinted three times, not three data points"; negligible; not_relied_on; integrity-flagged (fake independence) with named verification | "must not be read as three independent data points"; low; not_relied_on; reclassified to promotion via the wording tell | direction ✓; level adjacent (negligible vs low); trap avoided by both |
| E4 distributor report | strongly supports; high; **load_bearing** ("strongest costly-behavior evidence in the packet"; two layers: full-price consumers + 31/40 boutique reorders) | strongly supports; high; **load_bearing** ("closest analogue to the retailer's own decision"); discounts declared (channel incentive, sample framing, summer→winter gap) | ✓ |
| E5 fad essay | opposes; low-to-moderate as direct evidence, moderate as general caution; supporting, "must be carried into the verdict's confidence, not averaged away" | opposes; low-medium; supporting for risk-framing, not_relied_on for current trajectory; dedicated conflict-handling section | ✓ |
| E6 brand scarcity | nominally supports; low; not_relied_on; integrity-flagged (manufactured scarcity), verification named (check production volumes via the E4 channel) | nominally supports; low; not_relied_on; integrity-flagged, verification named (batch size vs claimed sellouts); noted as non-additive with E4 | ✓ |
| E7 search trend | moderately supports; moderate; supporting ("does not raise the verdict's ceiling on its own") | supports current-trajectory claim, hedges persistence claim; medium-high for trajectory, low for persistence; **load_bearing for the trajectory sub-claim only** | direction ✓; level within one band; **role label differs** — Finding P-1 |
| E8 2019 category stat | nominally mildly supportive; negligible; not_relied_on ("'industry report' framing should not lend it more authority than its staleness allows" — explicit anti-source-class move) | mildly supports category-not-dying; very low; not_relied_on (temporal cap) | ✓ |

**Closings (instruction 11), both complete:**

- A: load-bearing = {E4, E1}; ceiling rests on the weaker ("if E4 fails a
  boutique spot-check, or E1's gasket defect scales into winter returns").
  Steelman = E5 + what would make it strong (GripMug-specific deceleration
  data, or demonstrated mechanism match to the two collapsed comparators).
  Missing evidence: later Trends/restock reads; spot-verification of E4 and
  Corvo production volumes behind E6; a denominator on E1's gasket complaints.
- B: load-bearing = {E4, E7, E1}; ceiling explicitly rests on the weakest =
  E1 (most anecdotal, unresolved astroturf flag). Steelman = E5 + what would
  make it strong (same substance as A). Missing evidence: cycle-over-cycle
  distributor deltas; competitor/allocation evidence; commercial terms;
  clarification whether E4's 40 boutiques are the full book.

**Verdicts:** A — confirm the allocation, commit a strong majority of volume,
negotiate staging/reopeners keyed to the next Trends/restock/return reads.
B — commit meaningful non-maximal exposure in two tranches, base tranche
anchored to E4, reserve tranche released on an early-fall sell-through read.
Both: bounded commit — neither avoid nor unconditional maximum. Both carry
E5's surviving concern into confidence wording (A: "moderately high that
committing is right; only moderate at full unhedged scale"; B:
"moderate-to-good on current demand being real; low-to-moderate on
unattenuated persistence through winter").

## Audit Against Pre-Registered Criteria

1. **Per-item direction identical — PASS (8/8).** No item flipped direction
   across framings.
2. **Load-bearing set identical — PARTIAL.** Ceiling-determining subset
   identical ({E4, E1}; both effectively rest the ceiling on E1/weaker-of-two)
   and matches the pre-registered expectation ("E4 certainly; E1 likely;
   nothing else"). Flat set labels differ on E7: A supporting; B load-bearing
   for the current-trajectory sub-claim only. The difference is declared, not
   silent, and traces to per-claim decomposition granularity (instruction 1
   invites per-claim weighing; instruction 11 asks for one flat load-bearing
   list). See Finding P-1.
3. **Verdict direction identical — PASS.** Both bounded-commit with staged
   exposure; matches the pre-registered expected direction.
4. **Levels within one band, attributable — PASS.** Largest gap: E7
   (moderate vs medium-high on the trajectory sub-claim), attributable to B's
   declared per-claim split; E3 negligible-vs-low adjacent; all others same
   band. No silent drift found.
5. **Trap handling — PASS.** E5 divergence-flagged and not averaged in both
   (A: "carried into the verdict's confidence, not averaged away"; B:
   dedicated conflict section downgrading E5 from "already fading" —
   contradicted — to "could still fade by winter" — not ruled out). E6
   integrity-routed in both with named verifications. E3 collapsed to one
   origin in both.
6. **FM sweep + instruction-following marks — PASS.** No FM-1..FM-10 pattern
   found in either trace. Notable positive instances: anti-FM-1 (A's explicit
   refusal of E8's "industry report" authority; both judged E2 on placement
   "regardless of genuine hands-on contact" / "however polished"); anti-FM-8
   (both denied E1 a prevalence reading: "can show a cohort exists without
   telling us how large"); anti-FM-10 (both split E1's quality claim from its
   demand claim and E7's trajectory claim from persistence). Numeric facts
   from the packet were cited but no weight was numeric or computed. Claim +
   fitness target precede every weight; closings complete.

**Framing-drift observation (contrast with probe v2):** probe v2 found a
systematic half-notch valence drift (strengths-first read higher than
concerns-first). Here, no directional drift appeared: the caution-framed
reader B did not read lower across the board (it elevated E7 for the
trajectory sub-claim). Consistent with v2's cross-model addendum — forced
cap/discount/neutral classification plus explicit fitness-target derivation
appears to anchor the dial. One case, two same-family readers: suggestive,
not proven.

**Auditor expectation errors (pre-registered rule):** the expectation table
oversimplified per-claim structure twice — E1's expected direction named the
demand claim where reader A weighed it primarily on quality/durability (both
legitimate claims the item bears on), and E7's expected role ("supporting")
did not anticipate a per-sub-claim load-bearing elevation. Recorded as
expectation simplifications, not read failures.

## Findings And Implications For The Doctrine

- **P-1 (main finding — wording hardening candidate).** Instruction Core step
  11 and Required Behavior 4 ask for one flat `load_bearing /
  supporting / not_relied_on` list, but instruction 1 mandates per-claim
  weighing — so two faithful readers can emit different flat sets while
  agreeing on every fact (observed on E7). The partition that matters
  downstream is the set carrying the **verdict** (whose weakest member the
  trace's ceiling rationale must cite; C3's own contract derives its cap by
  its own rules and declares no partition input). Candidate fix: step 11 and
  Required Behavior 4 say "the load-bearing items **for the verdict**";
  per-sub-claim role splits stay legal and declared. Minimum closure: the
  doctrine wording pins which partition the paired-read comparison is judged
  on.
- **P-2 (observation, no fix required).** Both readers made E1 load-bearing
  but for different primary sub-claims (quality/durability vs organic
  grounding). Facts and direction identical; the variance is which sub-claim
  a multi-claim item leads with. Same root as P-1; covered by its fix.
- **P-3 (wording hardening candidate).** Step 10's "do not weigh **it**
  here" is ambiguous between the risk and the item. Both readers resolved it
  sensibly (merits-weigh the item; route the risk with a named verification)
  — which matches the doctrine's intent — but a strict reader could exclude
  the whole item. Candidate fix: "do not let the risk move the weight here —
  flag it for separate verification; weigh the item's non-risk merits
  normally."
- **P-4 (banked at dispatch).** Step 10's repo pointer ("Rule 3, C2 ledger
  read contract") is not self-contained for no-repo readers; the probe prompt
  had to adapt it. Candidate fix: the Instruction Core carries the
  self-contained flag-and-verify wording, with the repo pointer as a
  bracketed annotation for repo-capable readers.
- **P-5 (positive result, product_learning).** At Sonnet reader tier, the
  Instruction Core produced full per-item derivations, caught all six planted
  traps in both framings, and held direction/verdict/level stability within
  the doctrine's declared tolerance on this case. The instruction content is
  followable as-is by a mid-tier model with no repo access.

## Disposition (same lane, post-probe)

The doctrine was hardened in the same lane after this probe, folding P-1, P-3,
and P-4 (plus two delegated checker reviews) into its wording — see the
doctrine's second `direction_change_propagation` receipt. This probe's
observations are against the **pre-hardening** Instruction Core; the
pre-registered sections above are preserved verbatim as the point-in-time
record. The hardened core (verdict-carrying partition wording, self-contained
step 10, widened step-11 missing-evidence scope, new FM-11..FM-14) has **no**
probe evidence yet; a re-run under the hardened wording is the natural next
probe (v1) if the owner wants one before a real-case read.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: in-case weighting Instruction Core feasibility (instruction-following + framing stability, one synthetic case, Sonnet-tier readers)
  source_quality_state: synthetic constructed case; blind isolated reads per probe v2 protocol; same-model-family readers and auditor
  execution_quality_state: two blind reads dispatched; audit pending at pre-registration commit
  closeout_state: no_durable_evidence
  claim_cap: product_learning only
  weakest_missing_or_failed_gate: single synthetic case; same-family readers; auditor = packet author; no real-case read; no cross-family grading
  receipt_artifact_or_gap: this artifact is the probe record; a de-correlated grading or a real-case read under the doctrine would be the next-stronger evidence
  non_claims:
    - not validation, readiness, or buyer proof
    - not judgment-quality evidence
    - not case admission, ledger population, or conductor involvement
    - not model-independence or real-world reliability
```

## Non-Claims

- Synthetic paper experiment; binds, populates, and runs nothing on the real
  machinery; the GripMug, Corvo, and all figures are fictional.
- Tests within-Claude-family instruction-following and framing stability on
  one constructed case at Sonnet reader tier; not model-independent, not
  multi-case, not a demand read of any real product.
- `product_learning`; the doctrine remains PROPOSED and unaudited by any
  formal review lane; this probe's outcome adjusts confidence, never claim
  tier.

```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
