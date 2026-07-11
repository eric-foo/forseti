# Forseti Terminal Candidate-Universe Reset — Cross-Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Temporary cross-lane handoff packet (single-consumption; non-authoritative)
scope: >
  Transfers the owner-ratified evidence-adjudication terminal-capability reset
  into a fresh, read-only product-planning lane that independently regenerates
  and screens Forseti's candidate universe before selecting any terminal market,
  first wedge, buyer, product form, or proving ground.
use_when:
  - Starting the fresh candidate-universe product-planning task commissioned on 2026-07-12.
  - Recovering the exact accepted/discarded boundaries after thread transfer.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_thesis_evidence_adjudication_v0.md
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/forseti_repo_map_v0.md
stale_if:
  - The owner changes the evidence-adjudication terminal-capability direction.
  - A later owner decision selects a terminal market or first wedge.
  - The receiver has consumed this packet; then delete it under the overlay's single-consumption rule.
```

## Load Contract

```text
forseti_start_preflight:
  agents_read: required
  overlay_read: required
  source_pack: S2 product anchor, then Judgment weighting sources and candidate-specific sources only as needed
  edit_permission: read-only except deletion of this consumed handoff packet
  target_scope: independently regenerated terminal-company candidate universe, screening, shortlist, proving grounds, GTM and recommendation
  dirty_state_checked: required
  blocked_if_missing: controlling evidence-adjudication thesis, enough current primary market evidence, or a verifiable workspace revision
repo_map_decision: use the Forseti source-loading policy; the repo map is required to resolve current product anchors
receiver_output_mode: chat-only
external_market_research: authorized; prefer current primary sources
```

Confirm, do not trust, this packet. Before analysis, verify:

- workspace project: `C:\Users\vmon7\Desktop\projects\orca`;
- expected branch: `codex/evidence-adjudication-terminal-reset`;
- expected HEAD: `reread-required` — resolve the branch HEAD after the draft PR is opened;
- expected dirty state: clean, except any receiver-created deletion of this packet;
- the new thesis exists and is current in the overlay and repo map;
- the former consumer-demand thesis and beauty-first wedge are explicitly historical;
- the offer, buyer-proof, proof-charter, consumer-demand discovery instrument,
  Sleipnir exploration, and demand-signal GTM design no longer route as live
  buyer/wedge authority.

If the branch, HEAD, authority routing, or dirty state differs materially,
stop and return the nearest blocker instead of reconstructing intent from this
summary.

## Goal Handoff

```yaml
goal_handoff:
  long_term_goal: Determine the greatest sustainable revenue- and profit-generating terminal company Forseti can realistically become.
  anchor_goal: Independently regenerate and screen the candidate universe around consequential evidence-adjudication problems under the corrected human-judgment and decision-relative source-weighting rules.
  success_signal: A de-anchored, evidence-backed shortlist and one recommendation with transferable pre-purchase proof, GTM, economics, fatal risks and reversal conditions — or NO_DIRECTION_CLEARS.
```

```yaml
workflow_sequence_policy: overlay_owned
workflow_sequence_source: explicit_user_instruction
workflow_sequence_status: bound
thread_operating_target_continuity: omitted
continuity_disclosure: No active thread_operating_target was supplied or inferred.
```

## Open Decision / Fork

The open decision is not product form. It is:

> Which consequential decision family gives Forseti the strongest reachable
> terminal-company path and first wedge when its epistemic heart is
> decision-relative evidence weighting, accountable human judgment is allowed
> now, and outcome-calibrated AI judgment is the compounding destination?

The receiver must distinguish:

- greatest theoretical terminal value;
- best reachable terminal company for Forseti;
- best initial wedge;
- easiest demonstration;
- strongest transferable buyer proof.

Do not equate a clean score with a valuable market, or a valuable market with a
reachable first sale.

## Drift Guard

### Accepted and controlling

- The terminal capability hypothesis is institutional evidence adjudication
  and decision learning for consequential decisions.
- Evidence weight belongs to `(evidence item, claim, decision frame)`, not to a
  static source class.
- The commercial product is the better decision and action trace, not “source
  weighting” sold by itself.
- Human analyst judgment is commercially admissible now where competence and
  evidence support it. Do not impose a zero-judgment screen.
- AI's adopted advantage hypothesis is scalable, explicit, high-dimensional
  reweighting and trace preservation — not magical numeric precision.
- A small item may tip a close decision without a fabricated “5%” weight.
- Public information is eligible for discovery, but retrievability, rights,
  cost, completeness and durability remain source-specific gates.
- CSB means **Commission Signal Board**. It structures the information need;
  Scanning discovers and Capture retrieves/preserves.
- Provenance is mandatory trust infrastructure and must never be proposed as
  the moat.
- Aphrodite Signals is a concurrent vertical candidate, not Forseti's terminal
  company or the anchor for this universe. Studio is a separate lane.

### Discarded as direction

- the prior top-three ranking and finalist verdicts;
- consumer-demand / beauty-first as Forseti's current wedge;
- the earnings-print proving ground as a current anchor;
- offers reduced to evidence-state maintenance because judgment was excluded;
- inherited assumptions about industry, buyer, product form, delivery form,
  data source, or proving ground;
- exact quantitative evidence weights without an accepted calibrated method.

### Preserve only as factual input, after fresh verification

- incumbent capabilities and substitutes;
- evidence of existing buyer expenditure;
- data requirements and public/privileged-data boundaries;
- source-access, credential, regulatory and distribution barriers;
- observed buyer workflows and recurring manual work;
- proof objectivity and resolution-speed findings.

M&A/event-driven intelligence, consumer-investor intelligence, beauty
retailer-account intelligence, broad CI/AlphaSense-like research, creator
signals, and other prior lanes may re-enter only after independent generation.
Their prior rankings and verdicts do not transfer.

## Exact Next Authorized Action

1. Complete the preflight and declare `SOURCE_CONTEXT_READY` or
   `SOURCE_CONTEXT_INCOMPLETE`.
2. Reference-load the Forseti product-lead and product-planning methods. Do not
   apply them until the smallest S2 product-anchor pack is loaded.
3. Generate a broad candidate universe from buyer decisions, existing spend,
   Forseti capability, attainable proof, credibility bootstrap, defensibility
   and scalable economics — before opening prior candidate conclusions.
4. Screen every serious candidate on the corrected contract in the controlling
   thesis plus the user's required evaluation grid.
5. Use current external market evidence, prioritizing primary sources. Expand
   the source pack only when a missing source could change the decision.
6. Compare the independently generated finalists with preserved factual inputs
   from prior lanes only after generation.
7. Return the capability/constraint inventory, broad universe, screening table,
   finalists, one recommendation (or `NO_DIRECTION_CLEARS`) and the smallest
   reversal evidence.

Do not select or design product form beyond what is necessary to test a
candidate's economics and proof transfer. Product-form handoff follows only
after the candidate/wedge decision.

## Candidate Evaluation Contract

For every serious candidate, assess:

- exact buyer and decision owner;
- consequential problem and current substitute;
- evidence of existing expenditure;
- revenue ceiling and plausible profit structure;
- frequency and urgency;
- whether the output changes an actual decision;
- first-purchase trust requirement;
- pre-purchase proving ground and why proof transfers;
- resolution speed and objectivity;
- public, purchasable and privileged data requirements;
- credentials and domain-competence requirements;
- defensibility and outcome-learning potential;
- distribution difficulty and GTM path;
- regulatory exposure;
- direct incumbents, substitutes and the “Moby Dick” competitor;
- strongest failure reason and earliest honest kill test.

Explicitly test whether Forseti's source weighting is materially useful in the
decision rather than merely intellectually interesting, and whether a strong
human analyst can deliver enough value before autonomous Judgment maturity.

## Authority / Source Ledger

| Source | Receiver treatment |
| --- | --- |
| `AGENTS.md` | Global project behavior and routing triggers; reread. |
| `.agents/workflow-overlay/README.md` | Overlay entry; reread. |
| `.agents/workflow-overlay/source-loading.md` | Controls smallest source pack and expansion. |
| `.agents/workflow-overlay/product-proof.md` | Controls proof/non-claim semantics. |
| `docs/workflows/forseti_repo_map_v0.md` | Resolves current product anchors. |
| `docs/decisions/forseti_product_thesis_evidence_adjudication_v0.md` | Controlling terminal-capability thesis and reset contract. |
| `docs/research/judgment-spine/judgment_spine_thesis_v0.md` | Judgment system role; thesis-level amendment. |
| `forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_in_case_evidence_weighting_doctrine_v0.md` | Detailed proposed weighting contract; do not silently ratify all details. |
| `forseti/product/spines/judgment/learning_loops/near_half/near_half_signal_reliability_ledger_v0.md` | Proposed outcome-memory substrate; contains no real validating rows. |
| Former consumer-demand thesis/wedge and prior lane reports | Historical/factual compare targets only; open after independent generation. |
| User-provided thread summaries of M&A, consumer-investor and retailer-account work | Orientation only; verify any market claim against current sources. |

## Non-Claims And Boundaries

This packet is not product authority, buyer validation, willingness-to-pay
proof, Judgment-quality evidence, readiness, outreach authorization,
implementation permission, source-acquisition authorization, or a product-form
decision. No repository edits are authorized except deleting this packet after
successful consumption. The receiving lane returns planning advice in chat.

After successful load, delete this single-consumption packet and record that
the deletion is lifecycle cleanup, not a doctrine change. If read-only runtime
constraints prevent deletion, report that narrow cleanup debt rather than
claiming it was removed.
