# Orca Demand Scan-Core + Gate-Run Adjudication Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Decision-prep consolidation (advisory owner decision surface — NOT a decision record, NOT doctrine, NOT validation, NOT readiness)
scope: >
  Consolidates the four owner decisions that currently block the first live
  forward-mode demand scan into one pass: (1) adopt the PROPOSED scan-core
  spec (folding its two open major review findings); (2) ratify the PROPOSED
  gate-run commission criteria; (3) decide the gate architecture (keep the
  demand gate as a separate inference layer vs. fuse it into the commission;
  quotas-as-collection-hygiene, not a gate substitute); (4) decide the
  forums-only demand-venue sourcing gap. Presents each fork with state,
  options, and (for #3) a recommendation. Owner decides; nothing here ratifies
  itself.
use_when:
  - Clearing the scan-core / gate-run / gate-architecture / sourcing decisions in one owner pass before authorizing a first scan.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  - forseti/product/spines/commission_signal_board/dispatch_rules/orca_demand_gate_run_commission_criteria_v0.md
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/orca_demand_scan_core_spec_delegated_adversarial_review_patch_review_v0.md
base: origin/main @ ada92695 (four cited statuses re-verified 2026-06-17; advance expected — re-confirm if the base moved)
```

## Why this packet

Every upstream piece of the demand pipeline is built, but the first live
forward-mode scan cannot be authorized because four things sit unresolved —
two are PROPOSED artifacts awaiting owner word, one is an architecture question
the owner raised, and one is a standing sourcing gap. Resolving them piecemeal
re-loads the same context four times. This packet is one decision surface so
the owner can clear all four and unblock (or consciously defer) the first scan.

This artifact is advisory. It asserts no readiness, runs no scan, ratifies
nothing, and does not reopen the owner-RATIFIED P2/P3/P4 gate decisions — those
are settled; #3 below is about *where the gate logic lives*, not *whether* to
have it.

## Current pipeline state (read from origin/main)

| Piece | State | Source |
| --- | --- | --- |
| First commercial target class | **Locked, owner co-ratified** — US-market tractioned indie/DTC beauty & personal-care operators; named decision owner; live 30-90 day demand-allocation decision (DecisionEvent); first bias retail/channel expansion. | `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` (Commercial Target Selection Amendment 2026-06-16); PR #203. |
| Demand-Substrate Hard Gate | **Live on main** — G1 = de-correlation by origination + verb-tiering; G2 = ≥1 gradeable costly-behavior floor; G4 org-motion corroboration; divergence/defeater. (Old "≥2 venue families" raw count is gone from the gate.) | `forseti_buyer_proof_packet_v0.md`; PR #90. |
| Scan-core spec (the hunting method) | **PROPOSED_PENDING_ADJUDICATION** — authored, re-derived against the amended gate, adversarially reviewed (2 open major findings). Authorizes no scan execution. | `orca_demand_scan_core_spec_v0.md`; PR #168. |
| Gate-run commission criteria | **PROPOSED** — "owner ratification owed before these criteria govern an actual commission." | `orca_demand_gate_run_commission_criteria_v0.md`; PR #90. |
| Demand-venue (Venue) sourcing | **Forums/community is the only sourced G1 demand-family card.** Review-surface + search-interest are unsourced, owner-owned gaps. Retail presence is G4 corroboration, excluded from the G1 origin count. | `forseti_buyer_proof_packet_v0.md` (Two distinct maintained card sets, AR-04). |
| Actual forward scan run | **None.** The only executed scan (discovery batch 0: Sentry/Clerk/Vercel/dev-tools) is SUPERSEDED / off-target. No candidate pool exists for the beauty beachhead. | `orca_discovery_batch_0_candidate_context_scan_v0.md` (SUPERSEDED banner). |

## Decision 1 — Adopt the scan-core spec

The spec is the hunting method: how a scan recognizes each read type (convergence
/ divergence / brand-decision event) per venue class and walks the venue card
set, with a candidate-observation (Observation) schema. It is `PROPOSED_PENDING_ADJUDICATION`
and went through a cross-family delegated adversarial review (controller OpenAI
GPT-5 vs. Anthropic home; de-correlation satisfied).

Two open **major** findings (recommendation: `advisory_keep_after_CA_
adjudication_of_diff` — the design is sound; both are patch-level schema
checkability weaknesses, no architecture pass needed):

- **F1 — observation-level gate-family field.** The observation schema lacked a
  per-observation gate-family field, so the two-family Hard Gate is not
  *mechanically checkable* across laundered/evidence venues. (Directly couples
  to Decision 3 and to G1 origin de-correlation — the field is what makes the
  collapse-to-origin step auditable.)
- **F2 — org-motion route state.** The org-motion route state was too weak to
  enforce the capture-lane binding / no-outside-route stop condition.

**Options:**
- (a) **Adopt with the two fixes folded in** *(narrowest complete)* — patch the
  observation schema (gate-family field) + strengthen org-motion route state,
  then adopt as the operating method.
- (b) Adopt as-is, track F1/F2 as residuals — leaves the gate not mechanically
  checkable at the observation level; not recommended given F1 couples to G1.
- (c) Send back for a wider revision — only if the owner sees a design gap the
  reviewer didn't (reviewer found none).

## Decision 2 — Ratify the gate-run commission criteria

The criteria define the runnable shape for taking **one** candidate through the
live gate: Stage A (dated, provenance-noted scan input), Stage B (ordered
in-session gate-run: origin de-correlation → costly-behavior floor → integrity/
divergence/defeater → verb-tier the ceiling → owner+consequence check), Stage C
(determinate `admit @ <ceiling>` / `hold` / `fail` / `insufficient-input`). It
is explicitly **not** a scoring engine and **not** the scan itself.

Status: PROPOSED — ratification owed before it can govern a commission.

**Options:**
- (a) **Ratify** so it governs gate-runs (qualitative, LLM-in-session; no
  scoring engine) — unblocks authoring a scan→gate-run commission.
- (b) Ratify conditional on Decision 3 (if the owner chooses to fuse, the
  criteria become the commission's acceptance contract rather than a standalone
  artifact — same logic, different packaging).
- (c) Defer pending Decision 3.

## Decision 3 — Gate architecture (owner-raised: "is the gate ceremony?")

**Question:** if the commission packet is emboldened with explicit per-source
quotas ("10 from X, 10 from Y …"), can the demand gate be retired as ceremony?

**Finding — no, but the instinct catches a real ceremony cost.** A quota and the
gate are different operations:

- A **quota answers "did I collect enough?"** — collection completeness.
- The **gate answers "does what I collected mean real demand, and how bold may I
  act?"** — inference + integrity judgment.

Critically, **"10 from X, 10 from Y" is the raw count-gate that was already tried
and rejected.** The pre-amendment demand gate *was* a raw count ("at least two
independent venue families"); AR-01 killed it because two laundered siblings of
one coordinated origination event satisfy the count while being a single real
signal. Moving quotas into the commission **relocates the proven-broken count**
and drops the layer that fixes it — the opposite of removing ceremony.

Three gate operations a quota structurally cannot perform:
1. **Origin de-correlation** — collapse N laundered copies to 1 origin. A count
   sees N.
2. **Costly-behavior floor** — "10 from search interest" can be 10 points of
   pure attention; the floor asks whether even one is *gradeable costly
   behavior*. A judgment, not a tally.
3. **Manufactured-demand defeater** — the case where every quota is met but the
   only costly signal sits inside the coordinated layer divergence flags. A
   quota **passes** it; the gate **fails** it. This is the highest-value catch
   in the system and the exact one a count is blind to.

The gate is non-ceremony precisely because the wedge's read sits *by design* on
a hostile, manipulable substrate. If sources were trustworthy, quotas would
suffice and the gate *would* be ceremony — they are designed-untrustworthy, so
the integrity judgment is the differentiated product.

**The real ceremony cost the instinct is right about:** running a commission and
a gate as two separate rituals is wasteful.

**Recommendation — keep the gate as the inference layer; fuse the ritual; quotas
as hygiene, not substitute:**
- Make the gate the **acceptance contract of one authorized gate-run
  commission** (scan-with-origination-provenance → in-session gate-run →
  verdict as a single unit). Stage A of the gate-run criteria already specifies
  the scan's required carry — the coupling is half-built.
- Keep **quotas as soft collection-breadth targets inside the commission**
  ("reach for ≥2 candidate origins so the ceiling isn't capped at
  hold/low-commitment") — collection hygiene that guides the hunt, never a
  pass-threshold that adjudicates it.
- Net: one ritual instead of two, judgment intact, count-fallacy stays dead.

**Options:**
- (a) **Keep + fuse** *(recommended)* — gate stays as the inference layer; gate
  and commission become one authorized unit; quotas live in the commission as
  soft breadth targets.
- (b) Keep both as separate steps (status quo) — accepts the two-ritual ceremony
  cost.
- (c) Replace the gate with a quota'd commission — **not recommended**; revives
  the rejected raw-count gate and drops origin de-correlation, the costly floor,
  and the defeater.

## Decision 4 — Demand-venue sourcing gap

Today only **forums/community** is a sourced G1 demand-family card.
**Review-surface** and **search-interest** are unsourced, owner-owned gaps.
Consequence: a gate-run today can legitimately draw demand-*origin* signal from
one card only — which caps the achievable ceiling (a single origin → only
hold/low-commitment), no matter how strong the costly behavior, until a second
independent demand-family origin is sourceable.

**Options:**
- (a) **Source review-surface and/or search-interest now** (which, and under
  what capture-lane route binding) — raises the achievable ceiling toward
  material-action eligibility; the bigger lift.
- (b) **Proceed forums-only at a capped ceiling** — run first scans honestly
  bounded to hold/low-commitment verdicts; cheapest path to a first real run,
  defers sourcing.
- (c) Defer scanning until ≥2 demand-family cards are sourced — slowest; avoids
  capped-ceiling runs entirely.

(This decision is independent of #3: it's about *how many demand-family origins
exist to count*, not *where the counting logic lives*.)

## Sequencing — what unblocks the first scan

Once the owner resolves the four above, the path to a first authorized scan run
is: adopt scan-core (D1) → ratify/fuse gate-run logic (D2 + D3) → resolve
sourcing posture (D4) → author a **scan→gate-run commission** (via
`.agents/workflow-overlay/prompt-orchestration.md`, referencing the ratified
criteria) → that commission, separately authorized, runs the first dated
candidate scan against the beauty target class. The scan-core spec authorizes no
execution on its own; a scan runs only under that explicit, owner-authorized
commission.

## Non-claims

- Advisory decision-prep only — not a decision record, not doctrine, not
  validation, not readiness, not buyer proof, not scan authorization.
- Does not reopen the owner-RATIFIED P2/P3/P4 gate decisions. Decision 3 is
  about gate *packaging/location*, not gate *existence*.
- The recommendation in Decision 3 is a reasoned default for owner adjudication,
  not a ratified direction.
- Cited statuses (PROPOSED / live / forums-only / no-scan) are read from
  `origin/main @ ada92695`; re-confirm if the base advanced.
```
