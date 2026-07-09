---
name: forseti-product-lead
description: "Orca product-lead reasoning for any Orca product decision - value prop, offer, ICP/wedge, buyer-proof, positioning, packaging, pull/kill/graduation. Prepares the decision for owner sign-off."
---

# forseti-product-lead (Forseti-local, accepted)

A distilled, all-encompassing product-lead method for Orca. It is a thin
**router into Orca's own product authority**, not a new authority. When a
section says "see X," open X — do not rely on this file's paraphrase for a
frozen decision.

## Status and boundary

- Status: **Forseti-local, ACCEPTED (frozen) + DEPLOYED/ACTIVATED 2026-06-08;
  refreshed + re-frozen 2026-06-12** (authorized skill-edit: thesis/wedge
  citations re-routed after the consumer-demand ratification; sha re-pinned
  in skill-adoption.md). Deployed for the Claude Code runtime as a PROJECT-level copy at
  `.claude/skills/forseti-product-lead/SKILL.md` (this project only; NOT
  user-global/personal, NOT a plugin, NOT external). This `.agents/skills/` file
  remains the canonical, cross-runtime source-of-record; the `.claude/skills/`
  copy is the runtime deployment copy and must be kept identical (the source
  sha256 pinned in skill-adoption.md governs). It carries no Forseti authority and
  decides nothing on its own.
- It defers all Forseti facts, folders, validation gates, artifact roles, output
  contracts, and non-claims to `AGENTS.md` and `.agents/workflow-overlay/`. If
  required authority is missing or stale, **fail visibly** — do not invent it.
- It does not replace, and must not import, the jb-scoped `product-lead` skill
  or any jb authority (`AGENTS.md` forbids jb-as-Orca-authority; the
  validation-gates leakage rule forbids copying jb product-lead rules).
- Rollback: delete `.agents/skills/forseti-product-lead/` (purely additive). Never
  edit plugin, user-level, installed, or external skill source from this lane.

## Use when / do not use

Use when the turn is an Orca product decision or review such as: confirming or
revising the value proposition or offer; selecting or adjusting an ICP / first-
proof wedge; designing or reviewing a buyer-proof loop; framing positioning,
packaging, or deliverable shape; or judging buyer pull, kill, or graduation.

Do not use for: running outreach or live buyer contact; producing a memo or
executive deck; commercial-frame / pricing lock; roadmap, feature scope,
implementation, tooling, dashboard, data-spine, scoring, or automation work;
or generic repo orientation. Each of those is owned by a separate lane and
needs its own explicit owner authorization.

## Load step (smallest sufficient source pack)

1. `AGENTS.md` and `.agents/workflow-overlay/README.md` first (authority entry).
2. The **`S2 product anchor`** pack from
   `.agents/workflow-overlay/source-loading.md` (thesis, offer hypothesis, buyer
   proof packet, Core Spine product contract, nearest boundary note), then only
   the nearest controlling product doc(s) for the specific decision. Use
   `docs/workflows/orca_repo_map_v0.md` to choose among many docs.
3. Controlling product sources, opened as the decision needs them:
   - Current product thesis and first-proof wedge: resolve BOTH through the
     repo map's "Product Anchor Files" table (route, don't restate — wedge
     facts pinned in this file have rotted before). At the 2026-06-12
     refresh they are
     `docs/decisions/orca_product_thesis_consumer_demand_v0.md`
     (consumer-demand decision intelligence; beauty first vertical; US-first
     geography; OWNER_LOCKED) and
     `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` (beauty
     operator first door; OWNER_LOCKED_DIRECTION) — but the repo-map row and
     the records' own supersession banners govern, not this line.
   - `forseti/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md` — offer
     hypothesis (broad offer + first-proof offer layer).
   - `forseti/product/spines/product_lead/proof_charter/orca_product_proof_lead_charter_v0.md` —
     proof-lead ownership and exclusions.
   - `forseti/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md` — proof
     standard, demand-substrate hard gate, qualification, rubric,
     kill / graduation.
   - `.agents/workflow-overlay/product-proof.md` — trust, pull-vs-praise, claim
     tiers, non-claims.
   - Superseded wedge-chain records (pricing-first, break-in-first, the v0
     ICP wedge) are history; their banners route forward — treat none of
     them as current.
4. Verify any pinned `input_hashes` before treating a source-heavy artifact as
   stable; record dirty / untracked / stale state. Strict claims need the
   controlling source — reading more cannot create missing authority.

## Method

0. **Route.** For non-trivial product decisions, run the Cynefin router
   (`.agents/workflow-overlay/decision-routing.md`) and state the smallest
   complete outcome before planning or delegating.
1. **Frame the layer.** Separate the broad offer boundary from the current
   first-proof lane / wedge. Name which layer the decision touches; do not let a
   first-proof choice silently narrow the whole value proposition, or vice versa.
2. **Compare ICP / wedge / segment candidates** on a fixed grid: buyer or sponsor
   type, company stage, decision owner / context, decision family, urgency
   trigger, consequence-if-wrong, public-signal availability, paid-first
   plausibility, repeatability, and disqualifiers. A wedge can be right for proof
   yet small standalone if it generalizes — keep "good proof wedge" and "durable
   market" as separate questions.
3. **Apply proof semantics** for buyer / proof decisions: `trust_open` /
   `trust_objection` / `trust_refusal` (only refusal disqualifies; objection is
   proof material); pull versus praise (budget-adjacent behavior, not approval
   language); and the kill / graduation gates verbatim from the buyer-proof
   packet. Classify the Judgment-Spine claim tier and `closeout_state`
   (`.agents/workflow-overlay/product-proof.md` +
   `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`) before any
   proof, readiness, or judgment-quality claim; missing evidence is not a pass.
4. **Keep deck-first without weakening the substrate.** Lead buyer-facing framing
   with the executive deck, but the internal memo + evidence appendix remain the
   reasoning substrate and proof gate; a deck is produced only after the memo and
   appendix pass the same gates.
5. **State patch implications, do not apply them.** Name the controlling sources a
   decision would change; leave the edit to a separately authorized patch lane.
6. **Close for sign-off.** Preserve product-proof non-claims, separate now / next
   / later, and end with the decision framed for owner sign-off plus the exact
   next authorized step. Freeze nothing without explicit owner sign-off.

## Guardrails — what must not become skill behavior

- Do not auto-lock the current first-proof wedge (whichever the repo map
  routes to) as Orca's permanent ICP; a wedge is a revisable first-proof
  selection whose pivot and kill conditions live in its own record.
- Do not treat candidate-context scans as qualified buyers.
- Do not turn deck-first framing into deck production.
- Do not launch outreach, public research, memo / deck production, commercial-
  frame decisions, implementation planning, or new skill creation from a
  product-lead pass — each needs separate owner authorization.
- Do not upgrade paid-first plausibility into willingness-to-pay proof.
- Do not own roadmap, feature scope, implementation, tooling, dashboards, data-
  spine, scoring, automation, or final commercial terms — route these to their
  gated lanes and the proof-lead charter's exclusions.

## Non-claims

Outputs of this skill do not assert buyer validation, willingness to pay, paid
conversion, repeatability, ROI, product / feature / implementation / commercial
readiness, Core Spine v0 validation, or proof-lane graduation. They are
decision preparation for owner sign-off, nothing more.

## Output shape

Follow `.agents/workflow-overlay/communication-style.md`: human summary first
(decision, scope, accepted / deferred, blocker, next authorized step), then
agent-readable detail (source reads, dirty-state notes, gaps), then compact
courier state only when useful.

## Adoption record (per `.agents/workflow-overlay/skill-adoption.md`)

- Candidate name: `forseti-product-lead` (shadow name; distinct from the resolver-
  visible jb-scoped `product-lead`).
- Source path: `.agents/skills/forseti-product-lead/SKILL.md` (Forseti-local).
- Authorization: owner instruction in the Product Lead CA lane to create a
  reusable product-lead skill; the candidate was pre-named in
  `forseti/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md` ("Product Lead
  Candidate Skill Notes"), which lists this skill as a downstream consumer.
- Collision status (checked 2026-06-07): resolver-visible `product-lead` exists
  and is jb-scoped → shadow name avoids the collision; no repo-local skill
  source existed; `.agents/skills/` did not previously exist; no other
  `forseti-product-lead` exists except the naming note in the ICP wedge decision.
  (Checked via repo grep + globs and the resolver-visible skill list, not a
  fresh plugin-manifest read.)
- Trigger examples: "make an Orca product decision", "review this ICP / wedge",
  "design the buyer-proof loop", "is this buyer pull or praise?", "frame Orca's
  packaging / deliverable", "what should the next product move be (decision
  framing)?"
- Source boundary: not Forseti authority; defers all Forseti facts to `AGENTS.md` and
  `.agents/workflow-overlay/`; fails visibly when that authority is missing.
- Overlay loaded when authored: README, decision-routing, skill-adoption,
  source-of-truth, project-authority, safety-rules, product-proof,
  artifact-folders, communication-style, validation-gates, source-loading,
  retrieval-metadata, plus the product corpus above.
- Rollback path: delete `.agents/skills/forseti-product-lead/`; no edits to
  plugin / user-level / installed / external skill source.
- Validation notes: ACCEPTED (frozen) 2026-06-08, registered in
  `.agents/workflow-overlay/skill-adoption.md` (Accepted Orca-Local Candidate
  Skills), with `.agents/skills/` in `artifact-folders.md` and the source sha256
  pinned in skill-adoption. DEPLOYED/ACTIVATED 2026-06-08 for the Claude Code
  runtime as a project-level copy at `.claude/skills/forseti-product-lead/SKILL.md`
  (collision-checked: no `forseti-product-lead` / `product-lead` in project
  `.claude/skills/` or user `~/.claude/skills/`). Project scope only — not
  user-global, not plugin, not external. A one-time Claude Code restart is
  required to start watching the newly-created `.claude/skills/` directory.
  Codex / other-runtime activation is a separate target, not done here.
- Refresh record: 2026-06-12, owner-authorized in-thread ("go" on the
  deep-think rollout-readiness assessment) — stale thesis/wedge citations
  re-routed through the repo-map product-anchor rows (route-don't-restate),
  pre-migration flat `docs/product/` paths updated to their `product_lead/`
  and `judgment_spine/` homes, and the wedge guardrail generalized. Both
  copies updated identically; new source sha256 re-pinned in
  skill-adoption.md (closes ORCA-HYGIENE-019).
