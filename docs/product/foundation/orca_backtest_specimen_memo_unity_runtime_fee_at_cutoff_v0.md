# Orca Backtest Specimen - Unity Runtime Fee At-Cutoff Memo v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact - sealed at-cutoff decision memo specimen
scope: Phase 2 internal-only at-cutoff memo for the Unity runtime/install-based monetization backtest specimen.
use_when:
  - Conducting blind owner readback before any outcome calibration.
  - Reviewing whether the sealed source packet supports a decision-useful action ceiling.
  - Preparing later authorized adversarial review or outcome calibration.
authority_boundary: retrieval_only
cutoff: 2023-09-11 23:59 Pacific Time
input_source_packet:
  path: docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md
  sha256: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
stale_if: Any post-cutoff outcome fact is introduced, the source packet hash changes, the cutoff changes, or later clean pre-cutoff source loading materially changes the evidence base.
```

## Internal-Only Boundary

This is an internal Orca backtest specimen only. It is not buyer-facing, not a client memo, not a sales artifact, not a product, not outcome calibration, and not validation or readiness evidence.

This memo is written as if at `2023-09-11 23:59 Pacific Time`. It uses only the sealed Phase 0 + Phase 1 source packet identified in the retrieval header. It does not include or rely on any later outcome fact.

## Decision Frame

Decision question: Should Unity proceed with a broad runtime/install-based fee model, narrow or phase the change, grandfather existing users, change messaging, or hold pending further evidence?

Assumed decision-owner role type: executive or senior monetization/package decision owner accountable for product packaging, developer trust, revenue, customer retention, and launch risk.

Decision family: pricing / packaging / monetization.

Cutoff: `2023-09-11 23:59 Pacific Time`.

Known at cutoff from the sealed source packet:

- Unity has distinct Create and Grow monetization surfaces, so an install/runtime fee would touch the boundary between creation tooling, runtime/distribution use, and monetization economics. Evidence: EU-01, EU-03.
- Unity had visible financial pressure: revenue growth alongside substantial losses and operating expenses above annual revenue. Evidence: EU-02.
- Unity had a material high-value customer base, but the packet does not show which cohorts would face the fee or how enterprise contracts constrain changes. Evidence: EU-04.
- Unity publicly disclosed customer renewal, retention, confidence, competition, price, and customer-economics risks. Evidence: EU-05, EU-06.
- A major alternative engine publicly presented a different licensing frame, making market expectations relevant but not determinative. Evidence: EU-07.
- Exact pre-cutoff Unity pricing pages, plan thresholds, legal terms, elasticity, launch readiness, and acceptance evidence were not established in the packet. Evidence: EU-08 and Evidence Gaps.

Not proven at cutoff:

- Private revenue target, fee mechanics, customer-level exposure, install/runtime usage distribution, elasticity, legal enforceability, enterprise amendment rights, developer switching behavior, buyer acceptance, communications readiness, metering readiness, support readiness, or launch readiness.

## Executive Recommendation

Recommended action ceiling: Do not proceed with a broad runtime/install-based fee model at cutoff. Proceed only with a narrowed, phased, and explicitly grandfathered monetization path, paired with segment exemptions, customer testing, and revised messaging before any broad launch.

Recommended now:

- Hold the broad model.
- Narrow any fee exposure to clearly defined high-value segments where contract rights, economics, and customer communication are understood.
- Phase rollout behind customer testing and operational readiness checks.
- Grandfather existing users or existing projects unless legal, contract, and customer-readback evidence supports a narrower exception.
- Exempt low-revenue or vulnerable segments unless data proves the revenue upside outweighs trust and ecosystem risk.
- Reframe messaging around predictable customer economics and product value, not only Unity revenue capture.

Could become viable if:

- Unity can prove segment-level revenue upside, elasticity, legal/contract enforceability, customer acceptance, metering reliability, support readiness, and communications readiness before launch.

Confidence: moderate. The evidence is strong enough to reject a broad immediate action ceiling, but not strong enough to prescribe the exact fee design.

## Why This Recommendation

First-order evidence:

- Unity's own filing shows the business spans Create and Grow, making a runtime/install charge a cross-surface monetization decision rather than a simple price increase. EU-01, EU-03.
- Unity's own filing shows financial pressure that could justify exploring monetization expansion. EU-02.
- Unity's own filing also flags customer confidence, renewal, cancellation, reduced use, in-house alternatives, competition, price, and customer economics as risk categories. EU-05, EU-06.
- Unity disclosed material high-value customer concentration, supporting segmentation analysis but not proving broad applicability. EU-04.

Second-order interpretation:

- A broad runtime/install fee could create revenue upside, but the packet does not prove the necessary customer-level facts to launch broadly: who pays, how much, under which contract rights, with what elasticity, and with what operational dispute process.
- The strongest support is for a segmented monetization review, not a broad immediate model. High-value customer concentration makes segmentation plausible; missing plan, terms, contract, and elasticity evidence makes broad rollout unsafe.
- Competitive and customer-economics evidence means the decision should be judged by total perceived developer economics, not only Unity's need for revenue.

Key risks:

- Trust risk: Unity's own risk disclosures make customer confidence and renewal relevant. A monetization change tied to runtime or installs could alter expectations about the Create relationship. EU-05.
- Switching/substitution risk: Unity disclosed competition from alternatives and in-house tools; market context shows at least one major alternative engine publicly framed licensing differently. EU-06, EU-07.
- Enterprise packaging risk: high-value customers matter, but the packet does not prove contract rights, grandfathering cost, or segment-specific exposure. EU-04.
- Legal/terms risk: exact pre-cutoff Unity terms and enforceability were not established. EU-08.
- Revenue risk: visible losses support monetization exploration, but not an untested broad rollout. EU-02.

Why broader/faster action is unsafe at cutoff:

- The packet has first-order evidence of motivation and risk, but not first-order evidence that a broad runtime/install model is acceptable, enforceable, measurable, or economically efficient by segment.
- The decision has asymmetric failure modes: a broad fee can affect trust and customer economics across Create users, while the packet only supports targeted monetization exploration.

## Options Table

| Option | At-cutoff assessment | Evidence support | Main risk | Action ceiling |
| --- | --- | --- | --- | --- |
| Broad runtime/install fee | Not supported for immediate launch | Financial pressure and cross-surface monetization need exist, but customer economics, terms, and elasticity are unknown. EU-01, EU-02, EU-03, EU-08 | Trust, switching, legal, communications, and customer-economics risk | Hold |
| Narrower segment-specific fee | Plausible if limited to well-understood high-value segments | High-value customer concentration supports segmentation analysis. EU-04 | Contract constraints and customer acceptance unknown | Proceed only under named evidence conditions |
| Phased rollout | Stronger than broad launch | Risk disclosures support controlling rollout exposure. EU-05, EU-06 | May delay revenue and still fail if testing is weak | Phase |
| Grandfather existing users | Recommended default | Packet lacks proof that existing contracts/projects can absorb a changed runtime/install burden | Foregone revenue and package complexity | Grandfather unless contrary evidence is proven |
| Exempt low-revenue or vulnerable segments | Recommended default | Packet does not prove low-segment economics or elasticity; competitive context matters. EU-06, EU-07, EU-08 | Exemptions may narrow revenue base | Exempt pending segment data |
| Messaging/positioning-first approach | Necessary but insufficient alone | Customer confidence and customer economics are known risk categories. EU-05, EU-06 | Messaging cannot solve bad economics or weak terms | Message after design and evidence gates |
| Hold pending more evidence | Supported for broad model | Missing evidence is material to launch safety. EU-08 and Evidence Gaps | Revenue opportunity delayed | Hold broad launch; continue narrowed evidence work |

## Risk Register

| Risk | At-cutoff signal | Severity for broad launch | Mitigation implied by action ceiling |
| --- | --- | --- | --- |
| Pricing risk | Price and customer economics are disclosed competitive factors. EU-06 | High | Segment, test elasticity, and define predictable economics before launch |
| Trust risk | Customer confidence, renewal, cancellation, and reduced-use risks are disclosed. EU-05 | High | Grandfather, phase, and message around customer predictability |
| Developer ecosystem risk | Create users depend on tooling and runtime expectations; exact acceptance is not proven. EU-01, EU-08 | High | Exempt vulnerable segments and test before broad rollout |
| Switching/substitution risk | Unity disclosed alternatives and in-house tools; competitor licensing context exists. EU-06, EU-07 | Medium-high | Avoid broad surprise changes; compare total economics by segment |
| Enterprise packaging risk | High-value customers are material, but contract constraints are unknown. EU-04 | High | Limit to accounts with known contract rights and readback |
| Legal/terms risk | Exact pre-cutoff Unity pricing and terms visibility was not established. EU-08 | High | Obtain legal/terms analysis before fee exposure |
| Communications risk | Customer confidence is a disclosed risk category; messaging readiness is a packet gap. EU-05 | High | Reframe, test, and prepare support/dispute handling before launch |
| Revenue risk | Financial pressure supports monetization exploration, but revenue capture is unproven by segment. EU-02, EU-04 | Medium | Keep monetization work active, but gate broad launch on economics |

## Evidence Appendix

- EU-01, first-order: Unity has distinct Create and Grow monetization surfaces. Limit: no planned pricing change, fee structure, private rationale, or customer willingness proven.
- EU-02, first-order: Unity had visible financial pressure before cutoff. Limit: no cash need, board pressure, target revenue, acceptable mechanism, or timing proven.
- EU-03, first-order: Unity revenue depended on both Create and Grow businesses. Limit: no revenue by cohort, game size, install count, platform, plan, or developer economics.
- EU-04, first-order: High-value customer base was material. Limit: no proof of which customers would face a runtime/install fee, contract constraints, or exposed churn.
- EU-05, first-order: Renewal, retention, customer-confidence, cancellation, reduced-use, and in-house alternative risks were disclosed. Limit: no quantification of churn, elasticity, switching cost, or fee-specific effect.
- EU-06, first-order: Price and customer economics were public competitive factors. Limit: no competitor adoption likelihood, switching threshold, or acceptable communications package.
- EU-07, contextual: A major alternative engine publicly presented a different licensing frame. Limit: competitor context only; no proof of Unity customer switching, Unity pricing feasibility, or legal constraints.
- EU-08, second-order: Exact pre-cutoff Unity pricing/terms visibility was not established in the source packet. Limit: negative archive lookup results do not prove the evidence did not exist; they only bound this run.

No URLs were reopened for this memo. No new evidence was added.

## What Would Change The Recommendation

The action ceiling could move from hold/narrow/phase toward broader launch only if Unity had clean evidence showing:

- real elasticity or revenue sensitivity by customer segment.
- segment-specific install/runtime usage distribution and fee exposure.
- developer churn and switching evidence under the proposed model.
- enterprise contract constraints, amendment rights, notice obligations, and grandfathering cost.
- legal/terms analysis supporting enforceability and dispute handling.
- customer acceptance of grandfathering, exemptions, and fee mechanics.
- launch communication readiness, including support and escalation paths.
- metering, billing, dispute, fraud, and platform-readiness evidence.
- proof that low-revenue or vulnerable segments are either unaffected or protected.

Evidence that would strengthen a hold recommendation:

- high expected churn, weak enforceability, unmeasurable installs, customer rejection in readbacks, inability to grandfather, or communications/support unreadiness.

## Deck Conversion Notes

Future slide titles only:

1. Decision at Cutoff: Broad Launch Is Not the Supported Ceiling
2. What the Public Record Supports
3. The Missing Evidence That Blocks Broad Rollout
4. Option Set and Recommended Action Ceiling
5. Risk Register by Launch Path
6. Conditions for a Broader Model to Become Viable
7. Seal and Non-Claims

## Anti-Leakage Ledger

- source packet used: `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- source packet SHA256 used: `FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24`
- public web pages opened in Phase 2: none.
- post-cutoff/outcome sources opened: none.
- prior replay artifacts read: none.
- contaminated archive bodies read: none.
- source packet leakage status carried forward: `snippet-noise: yes`; no leaked facts preserved.
- outcome calibration performed: none.

## Strict Non-Claims

- no buyer validation.
- no WTP proof.
- no repeatability proof.
- no product readiness.
- no feature readiness.
- no implementation readiness.
- no commercial readiness.
- no Foundation Layer validation.
- no outcome calibration.

AT_CUTOFF_MEMO_SEALED_NO_OUTCOME_SOURCES_OPENED
