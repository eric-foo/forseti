# Unity Runtime Fee Reveal Readout

```yaml
retrieval_header_version: 1
artifact_role: reveal_readout
scope: Compact post-reveal learning capsule for the Unity Runtime Fee blind judgment case.
use_when:
  - Learning from the Unity Runtime Fee case before judging a different platform-pricing or monetization case.
  - Reviewing whether the Judgment Spine case capsule transfers useful decision patterns.
  - Comparing sealed at-cutoff judgment, owner blind-read judgment, and revealed outcome without reopening the full product artifacts.
authority_boundary: retrieval_only
```

## Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S1 plus target Judgment Spine and Unity specimen artifacts
  edit_permission: docs-write
  target_scope: Draft a compact Unity reveal readout for future judgment transfer and agent case-memory use.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Capsule

- cutoff: `2023-09-11 23:59 Pacific Time`
- decision_question: Should Unity proceed with a broad runtime/install-based fee
  model, narrow or phase the change, grandfather existing users, change
  messaging, or hold pending further evidence?
- actual_action: Unity announced a broad Runtime Fee on September 12, 2023,
  revised the policy after backlash, updated terms around version protection,
  and later canceled the Runtime Fee effective September 12, 2024.
- highest_leverage_judgment_for_this_case: Hold broad runtime/install fees;
  proceed only if a tiny, customer-accepted, future-version-only or opt-in
  wedge proves the mechanism can exist without ecosystem shock.
- key_transfer_lesson: Commercial pressure does not authorize a pricing
  mechanism that changes the customer bargain unless mechanism psychology,
  implementation cost, segment exposure, and fallback monetization paths have
  been tested.
- transfer_pattern: `commercial_pressure | mechanism_psychology |
  exposed_segments | implementation_cost | trust_guardrails |
  alternative_monetization | evidence_that_would_change_decision`
- pattern_instantiation:
  - commercial_pressure: Unity had visible profitability and monetization
    pressure before cutoff.
  - mechanism_psychology: Runtime or install-based pricing threatened to make
    the engine feel like a retroactive toll surface, not only a price increase.
  - exposed_segments: Current projects, future projects, enterprise accounts,
    and indie or small-team developers needed separate treatment.
  - implementation_cost: Metering, billing, fraud, reinstall counting,
    dispute handling, support, and platform readiness were launch-critical.
  - trust_guardrails: Grandfather existing projects or versions, exempt
    vulnerable segments, and phase any change through future-version,
    opt-in, or clearly contracted boundaries.
  - alternative_monetization: Prefer subscription price or threshold changes,
    enterprise packaging, support/cloud/service packaging, and cost control
    unless a runtime-fee wedge is customer-accepted.
  - evidence_that_would_change_decision: Clean customer consultation,
    segment-level economics, enforceable terms, reliable metering, support and
    dispute readiness, and proof that alternative monetization is inferior.
- tactical_read: A mechanism can be the problem even when the amount charged is
  commercially rational. The customer asks not only "how much?" but "what
  bargain is being changed, who controls the meter, and can I predict exposure?"
- tactical_read_boundary: Do not assert that all runtime fees are invalid.
  Treat mechanism psychology as a hypothesis to test by segment and timing.

## What Happened

After the sealed at-cutoff memo and owner blind read, outcome sources showed
that Unity announced a Runtime Fee based on installs. Public reaction and
Unity's own clarification path centered on install counting, retroactivity,
fraud/reinstall treatment, subscription-service scenarios, charity bundles,
thresholds, existing-project protection, and trust in Unity's metering.

Unity revised the policy after backlash, later clarified version and terms
protection, and ultimately canceled the Runtime Fee for games customers. The
replacement direction leaned toward plan, threshold, and subscription pricing
changes rather than a broad runtime/install fee.

## Blind Judgments Compared

Sealed at-cutoff memo:

- Do not proceed with a broad runtime/install-based fee model at cutoff.
- Proceed only with a narrowed, phased, and explicitly grandfathered
  monetization path.
- Pair any path with segment exemptions, customer testing, and revised
  messaging before broad launch.
- Core reason: public financial pressure justified exploration, but the source
  packet did not prove segment-level elasticity, contract rights, metering
  readiness, customer acceptance, legal enforceability, or launch readiness.

Owner blind-read judgment:

- Do not ship broad.
- If pursuing runtime monetization, start extremely small and minimal.
- Treat the first move as partly psychological: open the category carefully so
  expansion remains possible later.
- Apply any wedge only to high-value or high-switching-cost segments where
  ability to pay is clear.
- Exempt low-revenue or vulnerable developers by default.
- Use grandfathering or transition protection to avoid changing the bargain on
  existing projects.
- Explore alternate monetization and cost reduction rather than consuming
  ecosystem trust for short-term earnings pressure.

## Material Assessment

As a final executive decision for this case under the visible reveal, the
sealed memo was directionally useful because it would have blocked the broad
runtime/install-fee launch and forced segmentation, grandfathering, exemptions,
testing, and messaging before scale.

As strategic counsel, the owner blind-read judgment added material value because
it sharpened the missing mechanism-psychology point. The issue was not only
whether Unity should narrow or phase a fee. The issue was whether introducing
the runtime-fee category itself would shock the ecosystem unless the first wedge
was tiny, future-version-only, opt-in, operationally measurable, and accepted by
customers.

The weakness in the sealed memo was not the broad direction. The weakness was
underweighting mechanism psychology, implementation cost, switching-cost
segmentation, alternative monetization, and the absence of developer/community
signal.

## Transferable Judgment Pattern

Use this structure in future cases where a company has real commercial pressure
but the proposed monetization mechanism may damage trust:

1. Commercial pressure: identify the legitimate revenue or margin reason to act.
2. Mechanism psychology: ask whether the mechanism changes the customer bargain,
   not only the price.
3. Exposed segments: split captive current users, future buyers, high-value
   accounts, small/vulnerable users, and public amplifiers.
4. Implementation cost: price the cost of metering, billing, support, fraud,
   disputes, enforceability, and communication.
5. Trust guardrails: define grandfathering, exemptions, opt-in scope, future
   version limits, and customer readback before launch.
6. Alternative monetization: compare less trust-damaging revenue paths before
   spending platform trust.
7. Evidence that would change the decision: name what would make the broad
   mechanism safe or unnecessary.

### Unity Instantiation

- commercial_pressure: Unity had visible profitability, prior pricing-action,
  enterprise-packaging, runtime, and data-leverage pressure before cutoff.
- mechanism_psychology: Runtime/install fees risked looking like a toll on
  already-built projects and future distribution, not a normal subscription
  change.
- exposed_segments: Current shipped or in-development games, future projects,
  enterprise accounts, indies, small teams, subscription-service games, charity
  bundles, demos, and vulnerable segments required separate treatment.
- implementation_cost: Install counting, fraud, reinstalls, support, disputes,
  platform scenarios, legal terms, and customer communication were central.
- trust_guardrails: Hold broad launch; grandfather existing users/projects;
  phase through new contracts or future versions; exempt low-revenue or
  vulnerable segments; make cost exposure predictable.
- alternative_monetization: Use subscription thresholds, enterprise packaging,
  support/cloud/service value, or cost control unless a runtime wedge passes
  customer acceptance.
- evidence_that_would_change_decision: Segment-level economics, customer
  acceptance, legally clean terms, reliable metering, support readiness, and
  proof that alternatives cannot solve the revenue problem.

## Tactical Reads

This case teaches a mechanism-read primitive, not only a pricing posture.

### Mechanism Psychology Read

When a platform changes monetization, the customer evaluates who controls the
meter, whether the bargain is retroactive, whether future exposure is
predictable, and whether the platform is still stewarding the ecosystem.

In Unity, the runtime/install mechanism carried trust meaning beyond price. It
could be interpreted as charging for distribution reach after developers had
already built on the engine, especially if install counting and version
protection were not clear.

### Switching-Cost Segmentation

High switching costs do not make users safe to tax broadly. They can amplify
anger for current projects and push future projects, reputation, and community
recommendations away from the platform. Current-project captivity and
future-project choice must be separated.

### Implementation Cost As Strategy

Metering, billing, disputes, fraud controls, support load, and enforceability
are not back-office details when the mechanism itself is contested. They decide
whether the strategy is credible.

Boundary: this is not proof that the later backlash was fully predictable at
cutoff. The transferable lesson is that the pre-cutoff evidence was strong
enough to cap broad commitment and force mechanism testing before launch.

## Reusable Lessons

- Separate legitimate commercial pressure from launch authority.
- Mechanism psychology can dominate nominal price level.
- A broad fee is not safer just because customers have high current switching
  costs.
- Segment current projects, future projects, enterprise accounts, indies, and
  public amplifiers separately.
- Grandfathering, exemptions, and future-version limits are mechanism design,
  not communications polish.
- Messaging cannot save a mechanism that customers cannot predict, audit, or
  accept.
- Implementation cost is part of strategic judgment when metering and disputes
  define customer trust.
- Outcome similarity must not be used to upgrade the at-cutoff ceiling after
  reveal.

## Consulting Takeaway

The strongest client-facing recommendation for this case would not be "do not
monetize" or "launch smaller." It would tell the client which category of
monetization is unsafe, what proof would make a tiny wedge acceptable, and which
less trust-damaging monetization paths should be preferred first.

For Unity, that recommendation would be:

> Hold broad runtime/install fees. Introduce a runtime-fee category only if a
> tiny, customer-accepted, future-version-only or opt-in wedge proves the
> mechanism can exist without ecosystem shock. Otherwise use subscription,
> threshold, enterprise-packaging, support/cloud/service, and cost actions that
> do not change the customer bargain as sharply.

## Agent Use Surface

Use this case when a future agent is judging:

- platform pricing changes;
- usage-based or outcome-based monetization;
- API/data/runtime fee introductions;
- packaging changes that may feel retroactive;
- ecosystem-trust decisions under revenue pressure;
- cases where first-order business pressure tempts overcommitment.

Subagent prompts:

- Evidence skeptic: Which launch claims are unsupported, incentive-distorted,
  or missing at cutoff?
- Mechanism psychology: How does the mechanism change the customer bargain,
  meter control, predictability, or trust?
- Segment splitter: Which customer groups are captive now, movable later,
  vulnerable, high-value, or public-signal amplifiers?
- Implementation-cost reviewer: What must be metered, billed, disputed,
  enforced, supported, and explained before launch?
- Alternatives agent: Which less trust-damaging monetization paths could solve
  the commercial pressure?
- Action-ceiling agent: What is the strongest justified verb before reveal:
  watch, probe, test, hold, narrow, phase, grandfather, message, move, or
  commit?
- Anti-overfit agent: When should the Unity lesson not apply?

## Artifact Links

- Pre-cutoff source packet:
  `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- Sealed at-cutoff memo:
  `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- Outcome calibration:
  `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
- Adjacent method-validation replay:
  `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`

## Non-Claims

- No buyer validation.
- No willingness-to-pay proof.
- No repeatability proof.
- No product readiness.
- No feature readiness.
- No implementation readiness.
- No commercial readiness.
- No Core Spine validation.
- No model-training readiness.
- No fine-tuning readiness.
- No participant-safe blind packet in this case folder.
- No proof that this single-case pattern transfers across cases.
