# Demand-Gate Definition Closures — Cross-Vendor Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (delegated adversarial artifact review + home-model adjudication)
scope: >
  Cross-vendor delegated adversarial review of the encoding in
  docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md
  (the P2/P3/P4 Demand-Substrate Hard Gate amendment wording), plus the
  commissioning home model's per-finding adjudication. no_repo, advisory
  (findings, not a diff); the CA applied accepted findings to the proposal.
authority_boundary: retrieval_only
reviewed_by: gpt-5
authored_by: claude-opus-4.8
de_correlation_bar: cross_vendor_discovery
access_mode: no_repo
review_lane: workflow-adversarial-artifact-review (delegated; advisory)
target: docs/product/product_lead/orca_demand_gate_definition_closures_proposal_v0.md
target_hash_at_review: 9A22C41191F09FA4   # sha256[:16] at dispatch; reviewer reported target_hash_confirmed:no (worked from inlined verbatim body)
commission: workflow-delegated-review-patch (provisional opt-in; CA commission in-thread 2026-06-13)
```

## Commission

Cross-vendor (discovery-bar) adversarial review of whether the proposed
amendment wording **faithfully encodes** the owner-locked P2/P3/P4 decisions,
and what failure modes / ambiguities / lock-in / ripple breakage the wording
opens. Bounded: attack the encoding, not the locked decisions. `no_repo`
advisory — reviewer returned findings; the CA (Claude Opus-class) adjudicates
and applies within the proposal.

## Reviewer Summary (verbatim)

```yaml
review_summary:
  reviewed_by: GPT-5
  authored_by: claude-opus-4.8
  de_correlation_bar: cross_vendor_discovery
  target_hash_confirmed: no   # reviewer used the inlined verbatim body; could not confirm attachment bytes
  source_context: ready
  verdict: advisory_findings_only
  finding_counts: {critical: 0, major: 5, minor: 2}
  decision_level_flags: 1
```

Measurement note: `target_hash_confirmed: no` — the reviewer worked from the
inlined verbatim target body (a known `no_repo` limitation when the reviewer
cannot open the attached file). The inlined body was a faithful copy of the
target at `9A22C41191F09FA4`; the encoding reviewed matches the dispatched text.

## Findings + Home-Model Adjudication

All severities are finding-priority only (no approval/rejection authority).
Adjudication treats each finding as a claim. All 7 findings **accepted**.

### AR-01 (major) — independence under-encodes: common-ancestor case
- **Reviewer:** "neither derived from the other" misses the common-ancestor case
  — two venues can both derive from the same upstream origination event without
  either deriving from the other, letting laundered siblings count as
  independent.
- **Closure condition (reviewer):** collapse any shared origination ancestry /
  shared coordinated origination event to one family, not only direct
  venue-to-venue derivation.
- **Adjudication: ACCEPT.** Real defect — the pairwise test passes laundered
  siblings of one event. Applied: G1 now requires *no shared origination
  ancestry* (collapse derive-from-each-other **or** common upstream / coordinated
  origination).

### AR-02 (major) — verb ladder bypass: "defend" can be a material action
- **Reviewer:** "defend" can itself be an action, so "required to act" doesn't
  cleanly bind; an operator could justify a material defensive action from one
  origin while claiming ≥2 only governs "bolder" moves.
- **Closure condition (reviewer):** bind the verb tiers so one-origin outputs
  cannot authorize any action above the intended hold/defend ceiling.
- **Adjudication: ACCEPT.** Applied: tier by **commitment/reversibility**, not
  verb label — one origin → reversible/low-cost only (incl. cheap defends); any
  material/irreversible commitment (act, phase, narrow, **costly defend**)
  requires ≥2 independent origins.

### AR-03 (major) — costly-behavior truth-test vs divergence: no ordering rule
- **Reviewer:** converted-but-divergent sentiment could read both as "durable
  demand" and as an astroturf tell; needs an ordering rule.
- **Closure condition (reviewer):** state whether converted costly behavior
  clears the floor while divergence constrains the ceiling, or whether certain
  divergence defeats the floor.
- **Adjudication: ACCEPT.** Applied: costly behavior clears the **floor**,
  divergence caps the **ceiling**; **defeater** clause — if the lone costly
  signal sits inside the coordinated layer divergence flags, divergence defeats
  the floor.

### AR-04 (major) — retail card-set instability
- **Reviewer:** retail presence is both a card-role family and removed from G1;
  unclear if it's a deprecated label, a G4-only card, or a non-card gap — risk
  of double-count in G1 or loss as G4 evidence.
- **Closure condition (reviewer):** distinguish the maintained demand-family
  card set from G4/org-motion cards.
- **Adjudication: ACCEPT.** Applied: two distinct card sets — **G1 demand-family
  cards** vs **G4 org-motion cards**; retail = G4 card (kept as evidence,
  excluded from G1 count); not deprecated, not a gap.

### AR-05 (major) — "gradeable" / "distinguishable from attention" undefined
- **Reviewer:** these carry most of G2's work but relocate the ambiguity;
  operators still need to know what makes an instance gradeable vs anecdotal.
- **Closure condition (reviewer):** define minimal properties of a gradeable
  instance, without the deferred numeric threshold.
- **Adjudication: ACCEPT (partial).** Applied a qualitative definition:
  gradeable = (a) attributable to identifiable buyer actions; (b) statable with
  direction + rough magnitude; (c) corroborable/checkable. **Full numeric
  sufficiency stays owner-deferred (P4-B)** — see DLF-01.

### AR-06 (minor) — "corroborated in ≥1 family" ambiguous (evidence vs corroboration)
- **Reviewer:** unclear whether the same family can both evidence and corroborate
  the instance; "corroborated" implies independent support.
- **Closure condition (reviewer):** make clear whether one family can both
  evidence and corroborate.
- **Adjudication: ACCEPT.** Applied: floor = evidenced in ≥1 family; a 2nd
  independent family isn't required at the floor — it raises the ceiling.
  "Corroboration" reassigned to the ≥2-origin ceiling step.

### AR-07 (minor) — slot header preserves ambiguity + omits retail/G4 exclusion
- **Reviewer:** operators scan the slot header; it kept "enough for the verb" and
  dropped the retail exclusion.
- **Closure condition (reviewer):** header/guidance must prevent retail being
  counted as a demand family and preserve the one-origin ceiling / ≥2-to-act
  rule.
- **Adjudication: ACCEPT.** Applied: header excludes org-motion/retail and
  carries "1 origin → hold/low-commitment; ≥2 → material-action eligible."

### DLF-01 (decision-level flag) — single-instance floor is fragile
- **Reviewer:** a single gradeable instance is a fragile floor for a hard gate
  unless "gradeable" is strong; main remaining design risk; not an encoding
  defect if the owner intentionally accepts the calibration risk.
- **Adjudication: ROUTE TO OWNER.** Not the CA's to resolve. The AR-05
  qualitative definition mitigates it; whether to accept the single-instance
  interim floor (numeric threshold deferred to P4-B) is the owner's call.

## Residual Risk (reviewer, accepted)

Even with the findings closed, consistent grading depends on future maintained
venue-card definitions (P3 sourcing) and worked examples of gradeable costly
behavior; without them, operators can comply with the words while applying
inconsistent thresholds. **Accepted and routed** to the backtest distill-tail
(the calibration deck), not to the wording — this is the known scan-time /
calibration dependency, not an encoding defect.

## Keep Status

`no_repo` mode: the CA applied the 7 accepted findings to the proposal. A
**bounded same-vendor recheck** (closure of the 7 findings + any new
blocker/major in the touched wording) is owed before these amendments are kept.
The live-packet/brief apply is owner-gated and carries a DCP receipt. Nothing
here is a formal PASS, validation, readiness, or gate clearance.

## operator_closeout_source

```yaml
operator_closeout_source:
  what_happened: >
    A cross-vendor (GPT-5) advisory adversarial review of the demand-gate
    amendment wording returned 7 findings (5 major, 2 minor) + 1 decision-level
    flag. The home model (Claude Opus-class) adjudicated all 7 as accepted and
    applied the encoding fixes to the PROPOSED proposal doc.
  what_changed: >
    G1 independence now collapses shared origination ancestry (not just pairwise);
    verb tier bound to commitment/reversibility (closes the "defend" bypass);
    floor-vs-ceiling ordering + defeater added; G1/G4 card sets split (retail =
    G4, excluded from G1); "gradeable" defined qualitatively; evidence-vs-
    corroboration clarified; brief slot header hardened.
  what_is_owed_before_keep:
    - bounded same-vendor recheck (closure + touched-wording blast radius)
    - owner decision on DLF-01 / AR-05 numeric-floor deferral
    - owner go + DCP receipt for the live-packet/brief apply (off origin/main)
  validation_evidence: none (advisory review; not validation, not readiness)
  residual_risk: >
    consistent operator grading still depends on the venue-card definitions and
    worked gradeable-behavior examples produced by the backtest distill-tail.
```
