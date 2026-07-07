# Forseti Demand-Gate Definition Closures — APPLIED v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (amendment proposal — demand-gate definition closures; ratified, recheck-cleared, APPLIED to live instruments 2026-06-14)
scope: >
  Carries the dated amendments to the Demand-Substrate Hard Gate (buyer-proof
  packet G1 + G2) and the discovery brief, encoding owner-LOCKED decisions on
  P2 (independence), P3 (venue-family binding), and P4 (costly-behavior floor).
  APPLIED 2026-06-14: the ratified wording is now live in the buyer-proof packet
  (Demand-Substrate Hard Gate) and the discovery brief (qualification objective
  #3 + slot column); the live apply carries a direction_change_propagation
  receipt in the buyer-proof packet. Cross-vendor delegated adversarial review
  applied 2026-06-13 (GPT-5; 7 findings accepted); bounded same-vendor recheck
  cleared 2026-06-13.
use_when:
  - Reviewing whether the applied amendment wording faithfully encodes the owner's locked decisions.
  - Tracing the ratified demand-gate definition closures now live in the packet/brief.
authority_boundary: retrieval_only
status: APPLIED_TO_LIVE_INSTRUMENTS_2026-06-14 (decisions ratified + encoding recheck cleared 2026-06-13; live apply carries the DCP receipt in the buyer-proof packet)
authored_by: claude-opus-4.8
reviewed_by: gpt-5
de_correlation_bar: cross_vendor_discovery
locked_by: owner (in-thread, 2026-06-13)
applies_to:
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md            # Demand-Substrate Hard Gate G1 + G2 (APPLIED 2026-06-14)
  - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_consumer_demand_target_selection_brief_v0.md  # qualification objective #3 + slot column (APPLIED 2026-06-14)
ripple_surfaces:
  - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md          # retail = org-motion (already states it; cite, confirm before claiming)
  - docs/prompts/product-planning/orca_ontology_backbone_architecture_pass_commission_prompt_v0.md  # derived_from / diverges_from links (folded in 2026-06-13)
review_report: docs/review-outputs/adversarial-artifact-reviews/demand_gate_definition_closures_cross_vendor_adversarial_artifact_review_v0.md
open_next:
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
  - forseti/product/spines/product_lead/icp_wedge/forseti_discovery_consumer_demand_target_selection_brief_v0.md
```

## Fitness Reference (what the wording must faithfully encode)

Owner-LOCKED (in-thread, 2026-06-13) and **owner-RATIFIED 2026-06-13**. The
amendment wording must faithfully encode these decisions; the decisions
themselves are ratified (review may flag them as decision-level, owner-owned,
but not re-litigate them as encoding). Ratification is of the P2/P3/P4
*decisions*; keeping the *encoding* still requires the bounded recheck to close
and the live-packet apply to carry its DCP receipt.

- **P2 (independence) — LOCKED:** independence is *de-correlation by
  origination*, not a raw venue count. Manipulable sources are admitted as
  *sentiment input*; *costly behavior is the truth-test*; *divergence is an
  integrity signal, preserved, never averaged away*. The number tiers the
  commitment (enough independent origins for the commitment claimed), not a
  binary pass.
- **P3 (venue-family binding) — LOCKED:** bind the named families to maintained
  venue (Venue) card-set roles; only forums/community sourced today (owner-owned
  sourcing gap); *retail presence is org-motion (G4 corroboration), not a G1
  demand family*.
- **P4 (costly-behavior floor) — LOCKED:** floor = ≥1 gradeable costly-behavior
  instance evidenced in ≥1 qualifying family, distinguishable from attention;
  tiered ceiling; absence of demand is not a pass; numeric floor (P4-B)
  deferred.

## Proposed Amendment ① — Buyer-Proof Packet, Demand-Substrate Hard Gate, G1

> **Amendment — Independence, Manipulation, Venue Families (PROPOSED 2026-06-13, owner-decided; review-applied)**
>
> - **Independence = de-correlation by origination (no shared ancestry).** An
>   "independent venue family" means traceable to a *distinct origination
>   event*. Per the venue-chain (community originates → trade press launders →
>   BoF/WWD terminate), signals on the same `derived_from` chain are **one**
>   family. Independence requires **no shared origination ancestry**: collapse
>   to one family any signals that derive from each other **or** that trace to a
>   **common upstream origination event or a shared coordinated origination**.
>   Pairwise "neither derives from the other" is **insufficient** — two
>   laundered siblings of one event satisfy it while violating independence.
>   *(AR-01)*
> - **Verb-tiered by commitment, not a hard count or verb label.** Replace "at
>   least two" with **enough effectively-independent origins for the commitment
>   claimed**, tiered by *commitment/reversibility*, not verb name: one origin
>   (or laundered/shared-origination copies of one) authorizes only
>   **low-commitment, reversible responses** (monitor / probe / hold; a watchful or low-cost
>   posture); **any material or irreversible commitment — commit or scale — requires
>   ≥2 independent origins that converge.** A costly or scaling position is a
>   material action and needs the ≥2 bar. *(AR-02)*
> - **Two distinct maintained card sets.** Maintained cards split into **G1
>   demand-family cards** (today only **forums/community** is sourced;
>   review-surface and search-interest are **unsourced gaps**, owner-owned) and
>   **G4 org-motion corroboration cards** (including **retail presence**). Retail
>   presence is a **G4 corroboration card** — preserved as G4 evidence,
>   **excluded from the G1 independent-origin count**; it is neither a deprecated
>   label nor a sourcing gap. *(AR-04)*
> - **Manipulated sentiment is admissible input; floor vs ceiling ordering.**
>   Manipulable sources are admitted as *sentiment input*. **Costly behavior
>   (G2) clears the FLOOR** (is there real demand at all?); **divergence
>   constrains the CEILING** (how bold). Converted costly behavior can clear the
>   floor while divergence caps the verb. **Defeater:** if the divergence pattern
>   indicates the costly-behavior instance is itself likely
>   manufactured/coordinated (e.g., the only costly signal sits inside the same
>   coordinated layer that divergence flags), divergence **defeats the floor**,
>   not merely the ceiling. Divergence (`diverges_from`) is preserved as signal,
>   never averaged away. *(AR-03)*

## Proposed Amendment ② — Buyer-Proof Packet, Demand-Substrate Hard Gate, G2

> **Amendment — Costly-Behavior Floor + Ceiling Tiering (PROPOSED 2026-06-13, owner-decided; review-applied)**
>
> - **Floor (clears G2), with a "gradeable" definition.** A costly-behavior
>   instance is **gradeable** when it is (a) **attributable to identifiable
>   buyer actions**, not aggregate mood/attention; (b) **statable with a
>   direction and rough magnitude**; (c) **corroborable/checkable**, not a single
>   unverifiable rumor. Floor = **≥1 gradeable** costly-behavior instance
>   (payment, switching/dupe-adoption, workaround/stockpiling/secondary-market
>   premium, churn, durable buyer pressure) **evidenced in ≥1 qualifying
>   demand-venue family**, distinguishable from attention volume. *(AR-05;
>   full numeric sufficiency deferred — P4-B; the single-instance interim floor
>   is an owner-accepted calibration risk — see DLF-01.)*
> - **Floor vs ceiling; evidence vs corroboration.** The floor needs the
>   instance **evidenced in ≥1 qualifying family**; a **second independent family
>   is not required at the floor** but **raises the verb ceiling** (per G1
>   verb-tiering). "Corroboration" = the ≥2-independent-origin step that raises
>   the ceiling, **not** a floor requirement. *(AR-06)*
> - **Ceiling tiering:** the strength/amount of costly behavior scales the
>   action ceiling — one gradeable instance → hold/low-commitment; a corroborated
>   pattern across ≥2 independent origins → material action.
> - **Guard:** absence of demand ("velocity miss," "low sales," falling
>   engagement) is **not** a G2 pass.

## Proposed Amendment ③ — Discovery Brief (ripple)

> - **Qualification objective #3** ("at least two independent venue families
>   visible") re-words to: "enough effectively-independent **demand-venue
>   origins** visible for the intended **commitment** (laundered copies /
>   shared-origination siblings collapse to one); **org-motion including retail
>   presence is corroboration, not a demand family**."
> - **Slot-table column header + guidance.** Header: "Independent demand-venue
>   origins visible (laundered / shared-origination copies = one; org-motion /
>   retail excluded — see corroboration column)." Adjacent slot guidance: "1
>   origin → hold / low-commitment ceiling; ≥2 independent → material-action
>   eligible." *(AR-07)*

## Delegated Review Adjudication (2026-06-13)

Cross-vendor delegated adversarial review (reviewer `gpt-5`; author family
Claude Opus-class; `de_correlation_bar: cross_vendor_discovery`;
`access: no_repo`, advisory findings, CA-applied). Full findings + per-finding
adjudication in the review report (see `review_report`). Summary: **7 findings
(5 major + 2 minor) accepted**; AR-05 accepted with full numeric sufficiency
owner-deferred; **DLF-01 routed to owner** (single-instance floor calibration
risk). Encoding fixes AR-01/02/03/04/05/06/07 applied above.

**Owner decision (2026-06-13): ACCEPTED.** The single gradeable instance stands
as the interim G2 floor (with the qualitative "gradeable" definition above); the
numeric threshold stays deferred to P4-B. Basis: the verb-tiering already bounds
the risk — a single instance earns only hold / low-commitment, never a material
action (that needs ≥2 independent origins).

**Keep status:** the bounded same-vendor recheck **CLEARED 2026-06-13** (reviewer
`claude-sonnet-4-6`, `de_correlation_bar: same_vendor_sanity`; all 7 findings
`closed`; no new major in the touched scope; target hash confirmed) —
CA-adjudicated as accepted. **The encoding is kept.** **Applied 2026-06-14:** the
ratified wording is now live in the buyer-proof packet (G1 + G2, with three
adjacent stale "≥2 venue families" sentences reconciled to verb-tiering under
owner-approved scope) and the discovery brief (qualification objective #3 + slot
column), in a fresh worktree/branch off `origin/main`, carrying a
`direction_change_propagation` receipt in the buyer-proof packet. Remaining: the
gate-run commission criteria (scan → gate-run → filled discovery slot).

## Ripple / DCP Surfaces (to check at apply time)

- **Demand-read taxonomy** — already classifies retail placements as org-motion;
  expected **cite, no edit** — confirm against live text before claiming it.
- **Ontology backbone commission** — `derived_from` / `diverges_from` links
  folded in (2026-06-13); no further change owed here.
- Applying ① + ② edits the buyer-proof packet (doctrine change) → owner go +
  DCP receipt + fresh worktree/branch off `origin/main`.

## Non-Claims

APPLIED to the live packet/brief 2026-06-14 (the doctrine change carries its DCP
receipt in the buyer-proof packet). Still not validation, not readiness, not gate
clearance, not buyer proof, and not a scoring engine — applying the gate's
definition is not the same as a candidate having passed it. The locked decisions
are the owner's; this doc encoded them and that encoding is now live. Review
applied was advisory input adjudicated by the CA, not a formal PASS.
```
