# Summer Fridays Turn A Evidence-World Adversarial Review Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt and cold-reader handoff
scope: >
  Read-only adversarial review of the Summer Fridays Understanding Turn A
  evidence world at its previously passing revision, to identify only material
  evidence omissions and propose the smallest complete owner-adjudicable
  acquisition reopening before Deliver.
use_when:
  - Challenging whether the Summer Fridays Turn A evidence world was merely sufficient or genuinely strong across the bound question.
  - Deciding whether portfolio concentration, customer coverage, attention trajectory, or another evidence class materially warrants more acquisition.
  - Preparing an owner decision on the exact bounded scope of reopened Turn A.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_beauty_summer_fridays_current_understanding_two_turn_handoff_v0.md
  - docs/research/forseti_beauty_summer_fridays_current_understanding_commission_board_v0.md
  - docs/research/forseti_beauty_summer_fridays_current_understanding_scan_receipt_v0.md
  - docs/workflows/forseti_beauty_summer_fridays_current_understanding_acquisition_seal_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/forseti_beauty_summer_fridays_turn_a_evidence_world_gap_review_v0.md # nonresolving: expected output created by running this prompt
branch_or_commit: review target commit 4f3e3476309b78777e4254814b23cfa1b6b34dc9
stale_if:
  - The owner changes the bound question or cancels the Turn A reopening.
  - The exact review target commit becomes unavailable.
  - The report destination is occupied by a different review.
```

## Load Contract

```yaml
packet_version: 1
mode: max
created_at: "2026-07-21"
created_by_lane: codex/summer-fridays-understanding-handoff
source_loading_mode: repo-overlay-bound
workspace: C:\tmp\forseti-summer-fridays-understanding-handoff
handoff_path: docs/prompts/reviews/forseti_beauty_summer_fridays_turn_a_evidence_world_adversarial_review_handoff_v0.md
expected_branch: codex/summer-fridays-understanding-handoff
required_review_revision: 4f3e3476309b78777e4254814b23cfa1b6b34dc9
revision_mode: exact
expected_head: dispatch commit supplied by the courier; it must contain this handoff and descend from required_review_revision
expected_dirty_state_including_handoff_file: clean at dispatch
load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority
```

## Goal Handoff

```yaml
goal_handoff:
  long_term_goal: >
    Produce consistently decision-useful company Understanding reports from
    rich, provenance-secure acquisition and concise delivery.
  anchor_goal: >
    Complete one current-state Summer Fridays Understanding phase through the
    canonical two-turn Acquire & Seal then Deliver lifecycle.
  success_signal: >
    Turn A earns an unblocked acquisition seal under the current
    lead-to-angle-to-material-seam rule, and Turn B produces a decision-neutral
    report optimized toward the six qualitative outcome signals without
    numerical scoring, evidence quotas, or unsupported conclusions.
```

The exact text above is carried from the original handoff. The owner has
reopened Turn A, so the success signal is not currently satisfied even though
the exact review target previously contained a passing seal.

## Open Decision / Fork

```yaml
decision: Which materially missing evidence, if any, should be acquired before Deliver?
options:
  - no_material_addition_found
  - bounded_turn_a_supplement
  - broader_turn_a_evidence_world_rebuild
already_constrained_or_off_the_table:
  - continuing to Deliver before this review and owner adjudication
  - treating a source, page, product, review, thread, query, or route count as completion
  - broad maximalist scanning without a claim or material-seam job
  - treating search interest, social views, review volume, or retailer placement as sales, adoption, representative approval, or commercial importance
  - changing the bound question, entering Problem Framing, recommending action, or inferring pain, buyer, urgency, willingness to pay, offer, or wedge
owner_of_the_call: current user after the review return
sender_recommendation: >
  Expect a bounded supplement rather than a full rebuild because provenance and
  route integrity are strong, while portfolio/hero concentration and
  cross-product customer coverage appear materially underdeveloped. The
  reviewer must try to defeat this recommendation and may conclude that no
  addition is material.
```

## Drift Guard

- Review the original Turn A evidence world; do not perform new acquisition,
  patch its artifacts, synthesize the Deliver report, or alter doctrine.
- The bound question remains:

  > What does current public evidence show about how Summer Fridays'
  > proposition is expressed across owned claims, assortment, US retail
  > presentation, and customer/community experience; which material seams
  > align, conflict, or remain unproven?

- Separate capture integrity from evidence completeness. Hash-verified packets
  can be excellent captures of an evidence world that is still too narrow.
- Do not presume that Summer Fridays has one hero product, two hero products, or
  any exact count. Define the threshold and evidence needed before assigning
  hero status.
- Do not presume search trends or social metrics are material. Admit them only
  when they would change interpretation of the bound question, and preserve
  their attention-not-demand boundary.
- Do not broaden into an exhaustive company, market, competitor, or financial
  analysis. Any proposed addition must name the claim or material seam it could
  change and a stopping rule.
- Current Deliver authorization is withdrawn by the owner-reopened acquisition
  seal. The passing seal at the review target is historical review evidence,
  not current lifecycle authority.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- Overlay source-loading policy:
  `.agents/workflow-overlay/source-loading.md`.
- Targets to enter the ladder:
  the exact review revision, original two-turn handoff, Commission Signal
  Board, scan receipt, acquisition seal, admitted capture packets, and the
  current owner-reopened seal.
- Already loaded by the sender:
  these artifacts and the named capture-route authorities were read during
  acquisition and prompt authoring. This is weak prior-thread orientation, not
  authority.
- Must load first:
  `AGENTS.md`, `.agents/workflow-overlay/README.md`, this handoff, the exact
  review target state, and the current acquisition seal.
- Load rule:
  re-run progressive source loading per the overlay. Do not treat this packet's
  loaded set, summaries, or candidate gaps as source readiness.

### Earlier-decided concepts and behaviors

- The commission is current-state, US-market, `Understanding`, forward mode,
  and decision-neutral.
  - Decided in:
    `docs/workflows/forseti_beauty_summer_fridays_current_understanding_two_turn_handoff_v0.md`.
  - Compare target:
    blob `0cbd6767ecb43472621474cd336d3794d34a36d6`.
  - Verify before:
    setting the review boundary.
- Acquisition follows lead to angle to material seam; source or route counts do
  not prove completion.
  - Decided in:
    `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md`.
  - Compare target:
    blob `97fcb86e0cf489d8da7324b2875ccbc2d8b6ddb0`.
  - Verify before:
    deciding whether an omitted evidence class is material.
- Deliver is allowed only by an internally consistent passing acquisition seal;
  an inadequate evidence world uses `BLOCKED_ACQUISITION_INCOMPLETE`.
  - Decided in:
    `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`.
  - Compare target:
    blob `220084fbd20f7fb1edc7ec9d9bc772c5aae51188`.
  - Verify before:
    making any lifecycle recommendation.
- External online evidence acquisition routes through the Capture spine.
  Diagnostic scouting that is not admitted as evidence may orient gap analysis,
  but it cannot support a strict finding about Summer Fridays.
  - Decided in:
    `.agents/workflow-overlay/safety-rules.md`.
  - Compare target:
    reread-required.
  - Verify before:
    any external scouting or proposed capture route.

## Active Objective

Independently attack the exact Turn A evidence world preserved at commit
`4f3e3476309b78777e4254814b23cfa1b6b34dc9`. Decide which additional public
evidence, if any, could materially strengthen the answer to the unchanged bound
question, then write an owner-adjudicable review report that proposes the
smallest complete reopened acquisition scope and explicitly rejects
non-material accumulation.

## Forseti Prompt Preflight

```yaml
output_mode: review-report
report_destination: docs/review-outputs/adversarial-artifact-reviews/forseti_beauty_summer_fridays_turn_a_evidence_world_gap_review_v0.md
template_kind: none
edit_permission: read-only review; only the report destination may be created or updated
review_target: exact Turn A evidence world at 4f3e3476309b78777e4254814b23cfa1b6b34dc9
review_style: findings-first, maximally adversarial and coverage-first
formal_recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
patch_queue_authorized: false
doctrine_change: none
input_destination: this filed handoff at the dispatch commit supplied by the courier
workspace_binding: receiver_to_bind; direct repository and named packet access required before SOURCE_CONTEXT_READY
```

## Exact Next Authorized Action

1. Verify the handoff, branch, dispatch commit, exact review revision, current
   owner-reopened seal, report-path availability, and packet accessibility.
2. Load the named authorities and target artifacts. Inspect primary packet
   contents and derived views where available; do not rely only on the scan
   receipt's summaries.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. After source readiness, apply
   `workflow-adversarial-artifact-review`. If unavailable or not applied, return
   only a blocked or advisory-only result.
5. Test the supplied candidate gaps, add any reviewer-discovered gaps, and
   steelman why each candidate might be non-material.
6. Write the durable report. Stop without acquisition, artifact patches,
   Deliver synthesis, commit, push, PR, or merge.

## Authority And Source Ledger

### Repository and review authority

| Source | Role | Load-bearing | Compare target | Last checked | Reuse rule |
| --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | Canonical shared project instructions | yes | blob `be4aa8894d49e679a648c9676099b8481a20a2ed` | 2026-07-21 | Re-read if blob differs. |
| `.agents/workflow-overlay/README.md` | Forseti overlay entrypoint | yes | blob `e05f8e6ff90f5366c363ab00bd064b3c1f7910af` | 2026-07-21 | Re-read if blob differs. |
| `.agents/workflow-overlay/source-loading.md` | Progressive source-loading authority | yes | blob `ed938909d541fbce8ead7df2af7e8bb9a69c3dc7` | 2026-07-21 | Re-read if blob differs. |
| `.agents/workflow-overlay/review-lanes.md` | Review authority and lifecycle boundaries | yes | blob `b3c7d9f8068a853d5cdb37ad69e5c98b446bb81b` | 2026-07-21 | Re-read if blob differs. |
| `.agents/workflow-overlay/prompt-orchestration.md` | Review prompt and output-mode rules | yes | blob `6513db6805402d10f3e93d0fdee19ed094e3fe53` | 2026-07-21 | Re-read targeted review/output sections if blob differs. |

### Commission and evidence-world sources

| Source | Role | Load-bearing | Compare target | Last checked | Reuse rule |
| --- | --- | --- | --- | --- | --- |
| `docs/workflows/forseti_beauty_summer_fridays_current_understanding_two_turn_handoff_v0.md` | Bound question, scope, lifecycle, and Drift Guard | yes | blob `0cbd6767ecb43472621474cd336d3794d34a36d6` at the review target | 2026-07-21 | Use exact target bytes; re-read current file only for later routing. |
| `docs/research/forseti_beauty_summer_fridays_current_understanding_commission_board_v0.md` | Sealed pre-scan coverage and route obligations | yes | blob `f258df8d0d4bc4bce589b98f121b7b6429f4e21e` | 2026-07-21 | Use exact target bytes. |
| `docs/research/forseti_beauty_summer_fridays_current_understanding_scan_receipt_v0.md` | Turn A walk, observations, seams, gaps, and provenance index | yes | blob `fef49303c553c54feaa8b3ea72522b5e8bc12f09` | 2026-07-21 | Use exact target bytes and verify claims against packets. |
| `docs/workflows/forseti_beauty_summer_fridays_current_understanding_acquisition_seal_v0.md` | Historical passing seal at target; current owner hold at dispatch | yes | target blob `d1b7d8fc2c64ebbfca1b9210e243478235500dc9`; current file reread-required | 2026-07-21 | Compare exact target with current dispatch state. |
| `forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md` | Material-seam and stopping authority | yes | blob `97fcb86e0cf489d8da7324b2875ccbc2d8b6ddb0` | 2026-07-21 | Re-read if blob differs. |
| `forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` | Acquisition seal and evidence-sufficiency authority | yes | blob `220084fbd20f7fb1edc7ec9d9bc772c5aae51188` | 2026-07-21 | Re-read if blob differs. |

### Capture packets and route authorities

- Local acquisition root:
  `_acquisition/summer_fridays_current_understanding/`.
  - Role: original owned, retailer-grid, trade, first-rung Reddit, recovered
    Reddit packets, consolidations, and cleaned agent views.
  - Load-bearing: yes.
  - Compare target: manifest packet IDs and SHA-256 values in the scan receipt;
    recompute before strict provenance findings.
  - Boundary: `_acquisition/` is placement-excluded but preserved. Absence or
    inaccessibility blocks a claim that primary local packet contents were
    reviewed.
- Exact Sephora P455936 parent:
  `F:\forseti-data-lake\raw\e93\01KY07CC8RJM5VG1WDKZZ6XWZR\manifest.json`.
  - Load-bearing: yes.
  - Compare target:
    manifest SHA-256
    `EE8A799D7CB47CD06B5AA2230CBCF1BAF995E3820CC5C2147C7647754305D110`.
- Exact Sephora Bazaarvoice companion:
  `F:\forseti-data-lake\raw\b99\01KY07DWJ3FQY94ZSWBKEJCZ9N\manifest.json`.
  - Load-bearing: yes.
  - Compare target:
    manifest SHA-256
    `ABE435B259FA95735430C257D1011EED80E8923DBD88B06F6773586FBC8A0C1A`.
- Reddit route:
  `forseti/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md`
  plus
  `forseti/product/spines/capture/core/source_families/social_media/reddit/README.md`.
  - Load-bearing: yes for evaluating whether the four packets were captured
    correctly; not authority for whether four threads were enough.
  - Compare target: reread-required.
- Sephora route:
  `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`.
  - Load-bearing: yes for evaluating the parent/companion route and its limits;
    not authority for portfolio selection.
  - Compare target: reread-required.

### Unadmitted sender scouting

On 2026-07-21, diagnostic web scouting—not Capture evidence—observed that:

- the official Summer Fridays US site exposed a dedicated “Jet Lag Mask & Lip
  Butter Balm” collection;
- its “Best Selling Products” page reported 25 results; and
- its “Shop All Products & Collections” page reported 22 results.

Those counts mix products, variants, sets, minis, and tools and cannot establish
a hero-product count. They orient the portfolio-concentration question only.
The reviewer may re-scout these pages diagnostically, but any resulting strict
Summer Fridays claim requires a later Capture-spine packet:

- `https://summerfridays.com/collections/jet-lag-mask-lip-butter-balm`
- `https://summerfridays.com/collections/best-sellers`
- `https://summerfridays.com/collections/all`

## Current Task State

- Completed:
  - The original Turn A acquired owned, retailer, community, partner, and trade
    evidence and preserved a passing state at the exact review revision.
  - The Sephora Bazaarvoice and four Reddit capture failures were recovered
    through current owning routes with hash-verified packets.
  - The owner explicitly reopened Turn A before Deliver.
- Partially completed:
  - Portfolio architecture and the number or concentration of hero franchises
    have not been established.
  - Cross-product customer evidence is much deeper for Lip Butter Balm than for
    other products or franchises.
- Broken or uncertain:
  - It is unknown whether search trends, social attention, creator evidence,
    broader retailer evidence, or another evidence class would materially
    change the bounded answer rather than merely add volume.
  - No independent adversarial gap review has yet been run.

## Workspace State

```yaml
branch: codex/summer-fridays-understanding-handoff
review_target_head: 4f3e3476309b78777e4254814b23cfa1b6b34dc9
dirty_state_before_handoff_authoring: clean
dirty_state_after_handoff_authoring: this handoff is newly added and the current acquisition seal is modified until the dispatch commit
target_review_artifacts:
  - docs/workflows/forseti_beauty_summer_fridays_current_understanding_two_turn_handoff_v0.md
  - docs/research/forseti_beauty_summer_fridays_current_understanding_commission_board_v0.md
  - docs/research/forseti_beauty_summer_fridays_current_understanding_scan_receipt_v0.md
  - docs/workflows/forseti_beauty_summer_fridays_current_understanding_acquisition_seal_v0.md
report_artifact: docs/review-outputs/adversarial-artifact-reviews/forseti_beauty_summer_fridays_turn_a_evidence_world_gap_review_v0.md
```

## Changed / Inspected / Tested Files

- `docs/workflows/forseti_beauty_summer_fridays_current_understanding_acquisition_seal_v0.md`
  - Status: modified after the review target.
  - Role: current lifecycle authority.
  - Important observation: the owner-reopen receipt changes the three gate
    fields to the valid blocked state; it does not rewrite the evidence world at
    the exact review target.
- `docs/prompts/reviews/forseti_beauty_summer_fridays_turn_a_evidence_world_adversarial_review_handoff_v0.md`
  - Status: added after the review target.
  - Role: current read-only review commission and cold-reader packet.
  - Important observation: it is routing material, not part of the Turn A
    evidence world being reviewed.
- The Commission Signal Board, scan receipt, original two-turn handoff, and
  passing seal were inspected at the exact review target and remain unchanged
  there.
- Prompt output-mode, retrieval-header, repo-map, link, and diff-shape gates are
  authoring validations only. The receiver must not treat them as review
  success.

## Frozen Decisions

- The bound question, current-state posture, US market, decision-neutral use,
  and prohibited conclusions remain unchanged.
- Turn A is reopened and Deliver is held until this review returns and the owner
  adjudicates its proposed scope.
- The original passing evidence world is reviewed exactly at
  `4f3e3476309b78777e4254814b23cfa1b6b34dc9`; later lifecycle edits do not
  rewrite that target.
- The review is not new acquisition. Diagnostic scouting is not evidence.
- New acquisition, if accepted later, must use the Capture spine and update the
  scan receipt, provenance index, material seams/gaps, and seal coherently.

## Mutable Questions

1. How should “hero product” or “hero franchise” be operationalized from public
   evidence without pretending merchandising order equals commercial
   importance?
2. Does current evidence support at least two established franchises—Lip Butter
   Balm and Jet Lag Mask—and which additional products are merely best sellers,
   extensions, launches, or variants?
3. Is one deeply captured Lip Butter Balm review corpus too concentrated for a
   company-level customer/community understanding?
4. Which representative products or franchises would add genuinely distinct
   experience seams: Jet Lag, complexion/makeup, sunscreen, fragrance, body, or
   another category?
5. Would branded and product-level search trends reveal a materially different
   attention hierarchy or trajectory? What comparison window and controls would
   prevent launch spikes or relative Google Trends indices from being laundered
   into demand or sales?
6. Is creator/social evidence material to how the proposition is publicly
   expressed, or would it only repeat owned messaging and self-selected UGC?
7. Is the current US retail presentation too Sephora-centric to answer the
   bound question, given the authorized-retailer and travel-retail evidence?
8. Did assortment breadth, launch cadence, price architecture, or category
   migration from skincare into makeup/fragrance create a material seam that
   the original walk underdeveloped?
9. Is more independent operating context necessary to interpret the proposition
   and extensions, or outside the bound question?
10. Would comparator evidence clarify an otherwise ambiguous Summer Fridays
    seam, or merely broaden into uncommissioned competitive analysis?
11. What material omission has the sender not anticipated?

## Superseded / Dangerous-To-Reuse Context

- “Summer Fridays has one hero product.”
  - Dangerous because the existing evidence was deep on one product but did not
    establish portfolio concentration.
  - Current replacement: hero count is unknown; at least Lip Butter Balm and Jet
    Lag Mask are hypotheses requiring independent, capture-backed assessment.
- “A passing acquisition seal means the evidence was god tier.”
  - Dangerous because the seal proves decision-useful sufficiency under the
    bound commission, not maximal or highest-quality evidence coverage.
  - Current replacement: capture integrity and evidence completeness are
    separate review axes.
- “Search trends should be added.”
  - Dangerous because attention data can be irrelevant to the bound question or
    mistaken for sales, adoption, demand, or importance.
  - Current replacement: admit search trends only if the reviewer names a
    material interpretive job and safeguards the inference boundary.
- The passing lifecycle fields in the exact review target.
  - Historical review evidence only.
  - Current replacement: the dispatch commit's owner-reopened blocked seal.

## Materiality Test

An omitted evidence class is material only if it could do at least one of the
following:

1. change the answer to how the proposition is expressed across a named bound
   surface;
2. reveal, reverse, or close a material alignment/conflict/unproven seam;
3. materially change confidence or uncertainty in a load-bearing judgment;
4. show that product-specific evidence was improperly generalized to the
   company; or
5. reveal a current product/category/channel expression that makes the existing
   company picture misleading.

It is not material merely because it is available, current, popular, numerical,
independent, or absent from the source list. Repetition, source counts, exhaustive
coverage, and commercial-performance questions outside the bound question do
not earn acquisition.

## Adversarial Review Axes

Treat these as attack surfaces, not a checklist and not predetermined additions.

1. **Portfolio and hero-franchise architecture.** Distinguish franchise,
   product, variant, set, mini, and merchandising label. Determine what public
   evidence could establish relative centrality without claiming internal sales.
2. **Assortment architecture and evolution.** Test whether the skincare-to-lip,
   makeup, sunscreen, body, and fragrance expansion was captured deeply enough
   to explain the current proposition rather than list categories.
3. **Customer evidence concentration.** Test whether deep Lip Butter Balm
   retailer evidence plus four Reddit threads can support a company-level
   experience layer. Identify only representative additional product surfaces
   with distinct information jobs.
4. **Retail presentation.** Test whether exact Sephora P455936 depth and a
   rendered brand grid adequately represent current US retail expression,
   ranking, badges, product-family prominence, and channel breadth.
5. **Attention trajectory.** Test the material value and inferential limits of
   Google Trends or another capture-compatible search-interest source for the
   brand and major product terms across defensible time windows.
6. **Creator and social expression.** Test whether founder/brand/creator content
   is a material public-expression surface or a dominated repetition of owned
   claims and self-selected community evidence.
7. **Launch cadence and current change.** Test whether new launches,
   reformulations, collaborations, or category moves create a current seam the
   static snapshot obscures.
8. **Independent operating context.** Test whether the limited CEO,
   travel-retail, and partner origins are enough to interpret the proposition's
   expansion without drifting into business-performance analysis.
9. **Comparator necessity.** Admit comparator work only for a named ambiguity
   that Summer Fridays evidence cannot resolve by itself.
10. **Provenance and support.** Dereference every relied-on observation and
    packet; recompute material counts/ranges and distinguish retrieval dates
    from publication or event dates.
11. **Novel omissions.** Search for a material evidence class or seam not named
    above. Do not reward the sender's candidate list by default.

## Diagnostic Scouting Boundary

The reviewer may perform bounded online scouting only to test whether a proposed
evidence route plausibly exists and could have a distinct material job. Such
scouting:

- is not admitted evidence;
- must not be cited as support for a strict Summer Fridays conclusion;
- must not become a broad scan;
- must not use ad hoc downloads as a substitute for Capture;
- must record the exact URL/query and why it changed or defeated a gap
  candidate; and
- must route any accepted future evidence acquisition through current Capture
  authority.

## Required Report Shape

At the top, include:

```yaml
review_summary:
  status: completed | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/forseti_beauty_summer_fridays_turn_a_evidence_world_gap_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_revision: 4f3e3476309b78777e4254814b23cfa1b6b34dc9
  reviewed_by: unrecorded
  authored_by: unrecorded
  blocking_findings: []
  advisory_findings: []
```

Recommendation semantics:

- `accept`: no additional acquisition is materially justified; owner may
  reseal from the original evidence world after adjudication.
- `accept_with_friction`: no required addition, but optional non-material
  hardening is worth knowing.
- `patch_before_acceptance`: a bounded additional acquisition set is materially
  justified before resealing.
- `reject`: the original evidence world is structurally too concentrated or
  misframed for the bound question and needs a broader Turn A rebuild.
- `blocked`: source readiness, packet access, method availability, or the report
  write failed.

Write findings first, ordered by `critical`, `major`, then `minor`. Every
actionable finding must include:

- finding id, such as `SF-A-AR-01`;
- severity and confidence;
- target location or seam;
- omitted evidence class or unsupported generalization;
- source evidence;
- strongest defense of the original evidence world and whether it survives;
- why the omission is material under the Materiality Test;
- the exact claim, uncertainty, or seam the additional evidence could change;
- smallest acquisition unit;
- source family and route authority to re-verify before execution;
- stopping condition;
- residual limitation after successful capture;
- `minimum_closure_condition`;
- `next_authorized_action`;
- `patch_queue_authorized: false`.

Also include:

1. `hero_product_assessment`:
   define hero product/franchise, state what the current evidence does and does
   not establish, and name the minimum public evidence needed for a defensible
   count or concentration judgment.
2. `candidate_gap_dispositions`:
   one disposition for every supplied attack axis:
   `material_required`, `material_conditional`, `non_material`, or `blocked`.
3. `reviewer_discovered_gaps`:
   any material omission not supplied by the sender.
4. `proposed_reopened_turn_a_scope`:
   - `must_capture`;
   - `should_capture_if_distinct_job_survives`;
   - `do_not_capture`;
   - ordering and stopping logic.
5. `considered_and_defended`:
   steelman-defeated candidate findings, one line each.
6. `not_proven_boundaries`.
7. `owner_adjudication_questions`:
   only choices that materially change acquisition scope.

If primary packet contents are unavailable, say exactly which audit dimensions
were not performed. Do not imply provenance accuracy from receipt text alone.

## Review-Use Boundary

This report is decision input for the owner. It does not itself authorize new
acquisition, reseal Turn A, start Deliver, patch artifacts, validate evidence,
or establish a hero-product count. After the review returns, the owner
adjudicates the proposed scope. Only an accepted bounded acquisition commission
may execute additional Capture.

## Commands And Verification Evidence

- Review target and branch were freshly observed before authoring:

  ```text
  branch: codex/summer-fridays-understanding-handoff
  head: 4f3e3476309b78777e4254814b23cfa1b6b34dc9
  origin head: 4f3e3476309b78777e4254814b23cfa1b6b34dc9
  working tree: clean
  ```

- Re-run target:
  receiver verifies the dispatch commit, exact review target, current seal,
  report-path availability, and packet access before `SOURCE_CONTEXT_READY`.

## Blockers And Risks

- Missing local `_acquisition/` or `F:\forseti-data-lake` packet access:
  review may still identify artifact-level gaps but cannot claim full primary
  provenance or capture-content audit.
- Current web surfaces can drift:
  unadmitted scouting must be rechecked and captured later if accepted.
- “Hero” has no self-executing public definition:
  merchandising, awards, review volume, search interest, and editorial language
  are different signals and must not be silently collapsed.
- Search/social data can seduce the review into an uncommissioned demand or
  popularity study:
  preserve the unchanged bound question and attention-not-sales boundary.
- The supplied gap candidates can anchor the reviewer:
  the report must include steelman defeats and novel-omission analysis.

## Confirm-Don't-Trust Load Checklist

Before acting, verify:

1. this handoff exists at the dispatch commit;
2. the exact review target commit exists and is an ancestor of the dispatch
   commit;
3. the target artifacts match the recorded blobs;
4. the current seal is blocked and `deliver_allowed: false`;
5. the report destination is available or intentionally the same review;
6. the required overlay and method sources are available;
7. the local and data-lake packets needed for primary audit are accessible; and
8. no concurrent writer is mutating the reviewed snapshot.

Return exactly one load outcome before source review:

- `REUSE`;
- `PARTIAL_REUSE`;
- `STALE_REREAD_REQUIRED`;
- `BLOCKED_DRIFT`;
- `BLOCKED_MISSING_PACKET`; or
- `BLOCKED_UNVERIFIABLE`.

## Do Not Forget

The reviewer is not being asked to collect more. The reviewer is being asked to
make it difficult for weakly justified collection to survive while still
finding the material evidence our first Turn A may have missed.
