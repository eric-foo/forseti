---
name: forseti-product-lead
description: "Prepare explicit owner sign-off on Forseti's own product direction: its value proposition or offer, ICP/first-proof wedge, buyer-proof design, offer positioning/packaging/deliverable shape, or pull/kill/graduation. Trigger only when the user explicitly asks to make or review one of those decisions, asks for product-lead decision framing, or invokes /forseti-product-lead. Do not infer from routine creator/audience profiles, copywriting or commercial-language refinement, feature/runtime work, or ordinary artifact review."
---

# forseti-product-lead (Forseti-local, accepted)

A distilled, all-encompassing product-lead method for Forseti. It is a thin
**router into Forseti's own product authority**, not a new authority. When a
section says "see X," open X — do not rely on this file's paraphrase for a
frozen decision.

## Status and boundary

- Status: **Forseti-local, ACCEPTED (frozen) + DEPLOYED/ACTIVATED as the
  primary product-lead skill identity on 2026-07-05** after the Forseti
  repo/project identity cutover. Deployed for the Claude Code runtime as a
  PROJECT-level copy at `.claude/skills/forseti-product-lead/SKILL.md` (this
  project only; NOT user-global/personal, NOT a plugin, NOT external). This
  `.agents/skills/forseti-product-lead/SKILL.md` file remains the canonical,
  cross-runtime source-of-record; the `.claude/skills/forseti-product-lead/`
  copy is the runtime deployment copy and must be kept identical. The legacy
  `orca-product-lead` source/deployment folders remain as thin compatibility
  wrappers for one transition window. It carries no Forseti authority and
  decides nothing on its own.
- It defers all Forseti facts, folders, validation gates, artifact roles, output
  contracts, and non-claims to `AGENTS.md` and `.agents/workflow-overlay/`. If
  required authority is missing or stale, **fail visibly** — do not invent it.
- It does not replace, and must not import, the jb-scoped `product-lead` skill
  or any jb authority (`AGENTS.md` forbids jb-as-Forseti-authority; the
  validation-gates leakage rule forbids copying jb product-lead rules).
- Rollback: delete `.agents/skills/forseti-product-lead/` and `.claude/skills/forseti-product-lead/`, then restore the full-method legacy `orca-product-lead` copies from the previous commit if necessary. Never
  edit plugin, user-level, installed, or external skill source from this lane.

## Use when / do not use

Use only when the turn explicitly asks for an owner-signoff decision or review
about Forseti's own product direction, such as: confirming or revising the
Forseti value proposition or offer; selecting or adjusting an ICP / first-proof
wedge; designing or reviewing a buyer-proof loop; framing Forseti's offer
positioning, packaging, or deliverable shape; or judging buyer pull, kill, or
graduation.

Do not use for: running outreach or live buyer contact; producing a memo or
executive deck; commercial-frame / pricing lock; roadmap, feature scope,
implementation, tooling, dashboard, data-spine, scoring, or automation work;
or generic repo orientation. Each of those is owned by a separate lane and
needs its own explicit owner authorization.

Do not auto-trigger merely because a task mentions clients, commercial value,
positioning, packaging, or buyers. Routine requests such as “make this creator
profile more compelling to brands,” “rewrite this commercial line,” “compare
these audience profiles,” or “improve this client-facing artifact” stay with the
owning creator, evidence, copy, or artifact lane unless the user explicitly
escalates the question to Forseti's product direction.

## Load step (smallest sufficient source pack)

1. `AGENTS.md` and `.agents/workflow-overlay/README.md` first (authority entry).
2. The **`S2 product anchor`** pack from
   `.agents/workflow-overlay/source-loading.md` (thesis, offer hypothesis, buyer
   proof packet, Core Spine product contract, nearest boundary note), then only
   the nearest controlling product doc(s) for the specific decision. Use
   `docs/workflows/forseti_repo_map_v0.md` to choose among many docs.
3. Controlling product sources, opened as the decision needs them:
   - Current product thesis and first-proof wedge: resolve BOTH through the
     repo map's "Product Anchor Files" table (route, don't restate — wedge
     facts pinned in this file have rotted before). As of the 2026-06-20
     refresh they are
     `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
     (evidence-backed strategic decisions for consumer-market leaders; demand
     integrity and durability as first reads; beauty first vertical; US-first
     geography; OWNER_LOCKED) and
     `docs/decisions/forseti_icp_wedge_consumer_demand_first_v0.md` (beauty
     operator first door; OWNER_LOCKED_DIRECTION) — but the repo-map row and
     the records' own supersession banners govern, not this line.
   - `forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md` — offer
     hypothesis (broad offer + first-proof offer layer).
   - `forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md` —
     proof-lead ownership and exclusions.
   - `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md` — proof
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
  routes to) as Forseti's permanent ICP; a wedge is a revisable first-proof
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

- Candidate name: `forseti-product-lead` (primary Forseti-local product-lead
  skill; migrated from the legacy `orca-product-lead` command/path).
- Compatibility alias: `/orca-product-lead` remains as a thin wrapper in both
  `.agents/skills/orca-product-lead/` and `.claude/skills/orca-product-lead/`.
  The wrapper must load the sibling `forseti-product-lead` skill and must not
  duplicate product-lead doctrine.
- Source path: `.agents/skills/forseti-product-lead/SKILL.md` (Forseti-local).
- Deployment path: `.claude/skills/forseti-product-lead/SKILL.md` (project-level
  Claude Code runtime copy, byte-identical to source). Project scope only — not
  user-global, not plugin, not external.
- Authorization: owner-approved Forseti migration continuation after product
  root, repo-map, harness, CI, and external repo identity cutovers landed.
- Collision status (checked 2026-07-05): no repo-local, project-level Claude,
  user-level Codex, user-level Agents, or user-level Claude skill folder named
  `forseti-product-lead`; active in-thread resolver did not expose a
  `forseti-product-lead` skill before this change. Existing `product-lead`
  remains jb-scoped and is not imported.
- Positive trigger examples: "make a Forseti product decision", "review this
  ICP / wedge", "design the buyer-proof loop", "is this buyer pull or praise?",
  "frame Forseti's offer packaging / deliverable", "what should the next
  Forseti product move be (decision framing)?"
- Negative trigger examples: "make this creator profile more compelling to
  brands", "rewrite this commercial line", "compare these audience profiles",
  and routine client-facing copy or artifact refinement without an explicit
  Forseti product-direction decision.
- Source boundary: not Forseti authority; defers all Forseti facts to `AGENTS.md`
  and `.agents/workflow-overlay/`; fails visibly when that authority is missing.
- Overlay loaded for migration: README, decision-routing, source-of-truth,
  skill-adoption, artifact-folders, validation-gates, source-loading, and the
  skill/preflight identity migration plan.
- Rollback path: delete `.agents/skills/forseti-product-lead/` and
  `.claude/skills/forseti-product-lead/`; restore the full-method
  `orca-product-lead` copies from the previous commit; revert the skill-adoption,
  artifact-folder, repo-map, and status-doc updates. Do not edit plugin,
  user-level, installed, or external skill source.
- Validation notes: migrated 2026-07-05 with source/deployment copies
  hash-verified byte-identical and wrapper copies hash-verified byte-identical.
  Resolver activation in the current running thread is not claimed; a fresh
  resolver/session may be required to observe the new primary skill.
