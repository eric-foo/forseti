# Adversarial Artifact Review — Orca C2 Rule 3 (Risk-State Weighting) v0

```yaml
retrieval_header_version: 1
artifact_role: >
  Adversarial artifact review record (cross-vendor, advisory; CA-adjudicated).
  Findings-first; advisory only — not validation, readiness, or patch-execution
  authority.
scope: >
  Cross-vendor adversarial review of the PROPOSED C2 Rule 3 (risk-state
  weighting), plus the commissioning-CA adjudication and patch disposition.
authority_boundary: retrieval_only
status: REVIEWED_ADJUDICATED_PATCHED_2026-06-15_RECHECK_OWED_BEFORE_FOLD_IN
authored_by: claude-opus-4.8            # author of the reviewed artifact
reviewed_by: unrecorded                 # operator-run cross_vendor (non-Claude family per commission); exact model+version not supplied — never fabricated
de_correlation_bar: cross_vendor
review_target: docs/decisions/orca_c2_risk_state_weighting_v0.md
reviewed_target_hash: D250635E9ADE768D87BC2022726AC5F6EED65577C63A4C5998F9D96246EFE3FC   # pre-patch revision under review
patched_target_hash:  D506CDC2B1BED609D9F261977D52663C5A3E16920284B8C6F965DEC21B5D221E   # post-adjudication patched revision
adjudicated_by: claude-opus-4.8 (commissioning CA / home model)
open_next:
  - docs/decisions/orca_c2_risk_state_weighting_v0.md
```

## Commission

A cross-family (`cross_vendor`) adversarial artifact review of the PROPOSED C2
Rule 3, run by a non-Claude family (the artifact was authored by `claude-opus-4.8`;
de-correlation is the point), advisory and read-only, to precede folding Rule 3
into the live C2 read-contract.

## Target

`docs/decisions/orca_c2_risk_state_weighting_v0.md` at reviewed hash
`D250635E…` (pre-patch). Patched to `D506CDC2…` after this adjudication.

## Authority / decision criteria (fitness reference)

The rule's claim is **reader-independence + buyer-defensibility**. The review was
asked to *attack* that, specifically to: (1) localize a classification/severity
judgment a reader's disposition would swing; (2) find a dispositive risk that
escapes the 3(a) cap; (3) find an unfalsifiable risk the 3(e) filter fails to stop;
(4) find where advisory-not-prohibition leaks into a hidden hard gate; (5) break the
monotone chain or reversibility boundary; (6) attack the scope line. INV-1
(no scoring), advisory-not-control, consumes-not-reopens G1/G2, and the MGT
qualitative-now stance were hard constraints to respect/attack. The fitness
reference was an attack axis, not a pass-if-matches bar.

## Findings + CA adjudication (findings-first)

Severity is finding-priority only (`critical` / `major` / `minor`), not a verdict.

- **AR-01 — `critical` — 3(a)/3(d)/3(e) — "established" undefined.** No bounded bar
  separates active fingerprint from suspicion; the cap/discount boundary (where
  reader-independence matters most) is reader-dependent.
  **CA: ACCEPTED.** Patch: 3(d) now requires each discriminator set to state a
  **sufficiency bar** (named conjunction = established present); 3(a) keys the cap
  to that bar; absent a bar, the cap is unreachable (→ unconfirmed). Per-risk
  threshold stays in the satellite deck; core owns the requirement.
  *minimum_closure_condition:* a bounded sufficiency standard exists per governed
  risk. *next_authorized_action:* deck authors the per-class bars before fold-in.

- **AR-02 — `major` — 3(a)/scope — dispositive over-anchored to fabrication.**
  Non-fabrication hollow-demand mechanisms (resale/flip, channel sell-in, transient,
  distress) can produce independent, full-price costly behavior, pass both core
  families, and escape the cap — the judge could certify hollow demand "durable."
  **CA: ACCEPTED (most material finding).** Owner decision (2026-06-15): **broaden
  Rule 3 by property.** Patch: dispositive redefined as "defeats durable *end-use*
  demand"; five mechanism classes named (fabrication/astroturfing, non-use/resale,
  channel sell-in≠sell-through, transient/event, distress/scarcity), each with its
  own discriminator family; astroturfing is one class, not the mechanism.
  *minimum_closure_condition:* non-fabrication mechanisms covered or explicitly
  routed, not silently missed → met by broadening. *next_authorized_action:* deck
  authors per-class discriminator families.

- **AR-03 — `major` — 3(d)/3(e) — missing vs inconclusive vs impossible conflated.**
  Hidden hard gate + novelty penalty (thin deck blocks new legitimate risks) and a
  laundering hole (unfalsifiable risk hides as "not yet specified").
  **CA: ACCEPTED.** Patch: explicit three-state discriminator status
  (missing-but-buildable → withhold material/owner-override; inconclusive →
  near-cap/owner bets; impossible → 3(e)); separator = "can you name a runnable
  clearing-check with more data/work?" Yes→buildable, No→impossible.
  *minimum_closure_condition:* the three states carry distinct ceiling consequences
  → met. *next_authorized_action:* none beyond the patch.

- **AR-04 — `major` — 3(b)/FP-FN — reversibility boundary slice-gameable.**
  "Recoverable before cost sinks" was economic-only; readers can reclassify by
  framing the committed portion narrowly/broadly.
  **CA: ACCEPTED.** Patch: recoverability spans economic, reputational, operational,
  and **evidence-contamination** lock-in; the **least-recoverable dimension binds**
  (anti-slicing); a test that manufactures the signal it would measure is material.
  *minimum_closure_condition:* a reversibility test robust to slicing → met.
  *next_authorized_action:* none beyond the patch.

- **AR-05 — `minor` — 3(c) — "never carried" ambiguous; apparent contradiction
  with "verified beats unverified."**
  **CA: ACCEPTED IN PART.** Wording fixed: baseline = the **risk-absent baseline**;
  verified-clean = risk-not-applicable = baseline, both > unverified (bears the
  discount). **Declined** the implied positive credit for verified-clean over
  never-suspected: the no-bonus is a deliberate anti-gaming (manufacture-then-clear)
  choice, preserved. *minimum_closure_condition:* baseline meaning unambiguous →
  met. *next_authorized_action:* none.

- **AR-06 — `minor` — MGT — v2 forward-compatibility over-claimed.**
  **CA: ACCEPTED.** Patch: v2 reframed as an *intended migration hypothesis*; a
  numeric v2 may need to decompose the bundled bands into separate variables
  (likelihood / evidence-quality / severity / action-lock-in). *minimum_closure_condition:*
  the claim no longer asserts a guaranteed structure-preserving upgrade → met.

## Reviewer non-findings (carried)

Monotone chain holds for ordinary cases; no INV-1 scoring leakage; FP/FN asymmetry
owner-owned and coherent; the discount-only example is directionally sound; no
direct G1/G2 reopening — but the origination language **duplicates** the gate's
independence logic. **CA carry-forward:** at fold-in, *reference* the gate's
independence logic; do not re-implement it (recorded in the rule's Non-claims).

## CA synthesis (beyond the review)

The accepted patches **compound** the thin-deck conservatism: more mechanism
classes (AR-02) × a sufficiency bar per set (AR-01) × an honest
missing-discriminator state (AR-03) = more early withholding on material moves. A
more correct rule holds the owner back more until the deck is built. Accepted and
named in the rule's MGT limits.

## Verdict / recommendation (advisory)

Reviewer: do not fold as-is; AR-01..04 are live-contract blockers; smallest closure
is bounded patches, not a rewrite. **CA concurs.** All six adjudicated and patched
in `D506CDC2…`. **Recommended before fold-in:** a bounded same-vendor (same-family)
recheck of the patched revision — verify each accepted finding is closed and scan
the touched scope for patch-caused / newly-visible blocker-or-major issues only
(smallest-complete blast-radius). Then the read-machinery lane folds Rule 3 into the
live C2 contract under its own Direction Change Propagation receipt (owner-gated).

## Non-claims

Advisory only. Not validation, not readiness, not approval, not mandatory
remediation, not executor-ready patch authority. The cross-vendor reviewer had no
repo access and emitted advisory findings; this durable record and the patches were
written CA-side. `reviewed_by` is `unrecorded` (operator-run, exact model+version
not supplied) — a visible provenance gap, not a captured measurement.
