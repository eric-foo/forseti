# Aphrodite Breakout Acceleration False Positive ChatGPT Pro Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Deep-thinking prompt
scope: >
  Prompt for stress-testing whether Aphrodite should use early creator
  acceleration as a breakout precursor despite paid, bot, algorithmic, and
  small-sample false positives.
use_when:
  - Asking ChatGPT Pro or another external reasoning model to critique the
    rising-creators acceleration design before any build handoff.
  - Separating momentum, acceleration, manipulation-risk posture, and early
    sponsorship decision value.
  - Designing the held-out validation bar for "sponsor them earlier" scouting.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/creator_signal/aphrodite_rising_creators_breakout_view_design_v0.md
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
  - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
  - docs/research/aphrodite_silver_metric_monitoring_inventory_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - docs/review-inputs/aphrodite_breakout_acceleration_chatgpt_pro_source_pack_manifest_v0.md
branch_or_commit: claude/aphrodite-moat-domination-sharpening @ 65dff1a3 source-read base
stale_if:
  - Aphrodite's rising-creators design, five-panel sprint design, or forbidden set changes.
  - A creator velocity, acceleration, spike, breakout, or anomaly recipe lands with an implemented recipe/version/runner.
  - Data-lake metric precompute or derived-claim provenance policy changes.
  - Owner authorizes implementation rather than advisory stress-testing.
```

## Forseti Prompt Preflight

```yaml
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated below.
forseti_start_preflight:
  authorization_basis: owner current-turn request to prompt ChatGPT Pro; "zip up source files if required"
  objective: >
    Stress-test acceleration as a brittle but potentially high-value early
    breakout precursor, especially whether it can be separated from paid,
    bot-like, algorithmic, and small-sample artifacts well enough to support
    earlier sponsorship scouting.
  intended_decision: >
    Decide whether Aphrodite should pursue acceleration as a validation-gated
    internal ranked watchlist, downgrade it to velocity/momentum only, or reject
    it until more history exists.
  cynefin_route: complex
  cynefin_basis: >
    The core uncertainty is not how to compute a formula; it is whether apparent
    early acceleration is signal, manipulation, paid distribution, platform
    allocation, or sample noise. The safe move is risk-first advisory stress
    testing before implementation.
  allowed_next_move: >
    Read-only ChatGPT Pro decision memo with formulas, false-positive model,
    held-out validation, sponsor-decision economics, and kill criteria.
  disallowed_next_move: >
    Building or exposing a product-facing acceleration score, declaring botting
    or paid manipulation from weak public evidence, or authorizing outreach.
  source_pack: custom_s2_creator_signal_acceleration_false_positive
  repo_map_decision: not_needed
  repo_map_reason: bounded to named Aphrodite, Creator Signal, Data Lake, and prompt-policy sources; repo-wide map would not change the prompt shape.
  edit_permission: read-only for receiver; author docs-write only for this prompt and source pack artifacts
  target_files_or_dirs:
    - docs/prompts/deep-thinking/aphrodite_breakout_acceleration_false_positive_chatgpt_pro_prompt_v0.md
    - docs/review-inputs/aphrodite_breakout_acceleration_chatgpt_pro_source_pack_manifest_v0.md
    - docs/review-inputs/aphrodite_breakout_acceleration_chatgpt_pro_source_pack_v0.zip
  source_hierarchy: >
    AGENTS.md and .agents/workflow-overlay/ govern workflow; accepted Forseti
    product/docs sources govern Aphrodite product constraints; external model
    output is advisory only until owner adjudication.
  output_mode: paste-ready-chat
  prompt_artifact_path: docs/prompts/deep-thinking/aphrodite_breakout_acceleration_false_positive_chatgpt_pro_prompt_v0.md
  receiver_output: chat-only decision memo; no files, code, capture, implementation, outreach, or runtime work
  template_kind: deep-thinking
  template_source: no bound project-local deep-thinking template used; prompt follows Forseti prompt-orchestration preflight directly
  branch_or_commit_reference: claude/aphrodite-moat-domination-sharpening @ 65dff1a3 source-read base
  dirty_state_allowance: none for receiver; author changes are limited to this prompt and source pack artifacts
  controlling_source_state: clean before prompt authoring; strict acceptance still requires fresh validation after write
  doctrine_change_decision: none; advisory prompt only, no product doctrine change unless owner later adjudicates and promotes a decision
  isolation_decision: existing clean worktree on claude/aphrodite-moat-domination-sharpening because this continues the active Aphrodite documentation lane
  thread_operating_target_continuity: continues the Aphrodite rising-creators / moat-domination lane; no runtime target is created
  validation_gates:
    - prompt artifact has retrieval header and explicit preflight
    - source boundary names Forseti authority and excludes jb/external workflow authority
    - receiver task is read-only and advisory
    - false-positive handling avoids unsupported bot/paid accusations
    - source bundle manifest records included files and hashes
    - git diff --check
    - placement check if available
```

## Paste-Ready Prompt

You are advising on Forseti/Aphrodite's creator-scouting product strategy.

We are considering an internal "rising creators" view for fragrance creators. The tempting idea is acceleration: find small or under-radar creators whose recent content is moving faster than their own prior baseline, then sponsor them earlier than everyone else.

The owner concern is the whole point of this prompt:

> Acceleration could be an early breakout signal, but it could also be paid distribution, bot-like activity, platform allocation, giveaway traffic, one-post noise, or a lifecycle artifact. It feels brittle. If we get it right, identifying next breakout creators early enough to sponsor them is extremely valuable. But we have to really calculate this.

Your task is to stress-test the idea before any build. Be direct and skeptical. If acceleration is too fragile, say so. Do not produce an implementation roadmap for a bad metric.

If you received `aphrodite_breakout_acceleration_chatgpt_pro_source_pack_v0.zip`, open the prompt and source files in the package. Use the source pack as the controlling context. If you do not have the zip or repo access, use the source capsule below and mark repo-verification gaps explicitly.

### Hard Boundaries

Do not write code.

Do not recommend outreach, contact enrichment, lead-list export, creator contact scraping, a customer-facing creator score, or a public person-level directory.

Do not call a creator "botting", "fake", "paid", or "manipulated" from weak public indicators. Use posture language such as `anomaly_risk`, `paid_distribution_possible`, `unsupported_manipulation_claim`, `downgrade`, or `withhold`.

Do not treat missing metrics as zero. Do not treat a withheld anomaly screen as proof that there is no manipulation.

Do not allow two data points to be called acceleration. Two comparable observations can show velocity/delta. Acceleration needs at least three comparable windows or enough per-content publication-time observations to compare slopes.

Do not let the sponsorship overlay contaminate the acceleration score. Rising evidence and sponsorability/ad-load evidence must remain separable.

### Source Capsule

Current Aphrodite doctrine:

- The moat is an evidence graph over creator x brand x product x content x time x proof. Its first time-axis product is momentum: weeks-scale moving averages, follower deltas, and breakout frequency versus a creator's own baseline.
- The forbidden set includes no outreach, no contact enrichment, no lead-list export, no public person-level directory, no demographics without gates, no single vanity score, no unstamped/LLM-only claims, and no zero-filled metrics.
- The latest rising-creators design distinguishes:
  - momentum: "is the creator moving now?"
  - acceleration: "is the creator moving faster than they were moving before?"
- Minimum posture:
  - one capture point: `withhold_rising_state`;
  - two comparable capture cycles: velocity/delta only, not acceleration;
  - at least three comparable windows or enough per-video publication-time observations to compare slopes: acceleration may be shown with sample support and limitations.
- Proposed acceleration features are deterministic, recipe-versioned, and posture-coupled:
  - early per-content velocity lift;
  - fast/slow window crossover;
  - self-breakout rate;
  - follower-cycle delta;
  - engagement-quality shift;
  - fit-relevant participation;
  - consistency/noise guard.
- The sellable cut is not "rising" alone. It is:

```text
rising_creator + low_or_moderate_recent_ad_load + sponsored_content_still_performs
```

- Ad-load and ad-reception stay separate from acceleration. The prime bucket is `prime_sponsorable_rising`, but it still does not prove creator acceptance or sponsor ROI.
- The internal rank may use a numeric sort key for deterministic ordering. The buyer-facing surface must not expose a single vanity score. It should show bands, components, receipts, and limits.
- The signal does not ship as trusted unless it beats base rate on held-out history. Required comparisons include raw popularity, raw momentum/velocity, recent cadence, random small-base eligible creators, and a manual recent-high-view heuristic.
- Required held-out reporting includes base breakout rate, precision at top K, lift over base rate at top K, recall among eventual breakouts, false positives, and false negatives.
- Leakage controls include no post-cutoff views/followers/sponsorship/manual knowledge in features, no post-cutoff identity collapses, and no tuning on the held-out period after seeing outcomes.
- Current metric inventory says SMA, EMA, compatible-window velocity, capture-window delta, spike/breakout, decay/plateau, and active-watch expiry are proposed/deferred unless a later recipe/version/runner lands.
- `recent_velocity` exists as a contract field but is currently `not_attempted`; population requires a named recipe, at least two compatible rollup observations, compatible scope/window/content-kind rules, observed numeric values, positive elapsed time, source record ids, and limitations.
- Data Lake posture: metrics are computed on demand by default; precomputed metrics may exist only as rebuildable, manifest-backed, non-authoritative views. Missing/hidden/blocked evidence is posture plus reason, never numeric zero.
- Derived claims must be claim objects with source refs, model/recipe version, input hash, timestamp, receipt, confidence/abstention, and `show | downgrade | withhold` posture. Derived claims must not be blended with observed metrics or collapsed into a vanity score.

### Core Question

Can acceleration be made strong enough for Aphrodite to identify and sponsor the next breakout creators earlier, or is it too brittle/manipulation-prone to trust beyond an internal watchlist?

### Definitions To Use Or Improve

Start from this distinction and critique it:

```text
level/popularity = how big the creator already is
momentum/velocity = how much the creator is moving now versus baseline
acceleration = whether movement itself is increasing versus prior movement
```

Candidate formula family:

```text
age_normalized_content_velocity =
  observed_metric_delta_or_level / elapsed_time_since_publish_or_capture

relative_velocity_lift =
  recent_age_normalized_velocity / trailing_creator_baseline_velocity

acceleration_posture =
  change in relative_velocity_lift across comparable windows,
  or fast-window relative lift minus slow-window relative lift,
  with minimum history and uncertainty gates
```

You may reject or revise this, but preserve the product boundary: creator-specific baselines, compatible windows, source-visible metrics only, no zero-fill, no acceleration from two points.

### What To Calculate

Give a concrete reasoning framework, not hand-wavy "use ML later." We need to know what would have to be true mathematically and operationally for acceleration to be useful.

Address:

1. Base-rate math:
   - If only a small percent of under-radar creators break out, what precision at top K is needed for the view to beat scouting heuristics?
   - How should we think about expected value of earlier sponsorship versus false positives, opportunity cost, brand risk, and analyst review time?
   - How does the required precision change if sponsorship cost is low versus high?

2. Acceleration versus momentum:
   - When does acceleration add information beyond raw current momentum?
   - When is it just noisy momentum with extra math?
   - What ablations would prove acceleration is contributing incremental lift?

3. Manipulation and paid-distribution false positives:
   - What public or source-backed signals can downgrade acceleration without making unsupported accusations?
   - Which anomalies are meaningful versus unreliable?
   - How should the system distinguish "paid distribution likely", "bot-like anomaly possible", "algorithmic boost", "giveaway/controversy spike", "irrelevant viral post", and "true niche-fit breakout" when evidence is thin?
   - What should be withheld rather than shown?

4. Small-base brittleness:
   - How should minimum sample size, shrinkage, confidence bands, winsorization, content-kind compatibility, elapsed-time normalization, and repeated-evidence rules work?
   - What is the right posture for one lucky video?
   - What minimum history is needed before acceleration can move above watchlist.

5. Sponsor-earlier decision value:
   - What is the actual decision this signal enables?
   - What would make "sponsor earlier" rational before the creator is obvious?
   - How should acceleration interact with ad-load, sponsored-vs-organic performance, disclosure hygiene, fit relevance, and brand adjacency?

6. Validation:
   - Design a held-out backtest with historical cutoffs, frozen inputs, feature windows, outcome labels, baselines, leakage controls, and success thresholds.
   - Include a forward-holdout fallback if historical snapshots cannot be reconstructed.
   - Include false-positive review: paid-looking spikes, suspicious engagement, one-post virality, irrelevant content, and platform shocks.

### Verdict Options

Pick one:

- `GO_VALIDATION_GATED_INTERNAL_WATCHLIST`: acceleration is worth pursuing only as an internal, receipt-backed, non-authoritative watchlist until held-out lift is proven.
- `GO_VELOCITY_ONLY_FOR_NOW`: acceleration language is too brittle now; use velocity/momentum posture and collect more history.
- `NO_GO`: acceleration is too noisy/manipulation-prone to pursue for this product at current data depth.
- `NEEDS_OWNER_DECISION`: one or two owner choices materially determine the route.

### Required Output

Return a concise but rigorous decision memo with these sections:

1. **Verdict**
   Pick one verdict and state the strongest reason.

2. **Acceleration vs Momentum**
   Explain the distinction in practical terms. Name exactly what extra evidence acceleration must add beyond momentum.

3. **False Positive Model**
   List the main ways early acceleration can be fake or non-actionable. Separate paid distribution, bot-like anomaly risk, algorithm boost, controversy/giveaway traffic, irrelevant viral content, and small-sample noise.

4. **Signal Design**
   Propose the smallest defensible feature set and formulas/postures. Include minimum data requirements and withhold rules.

5. **Manipulation-Risk / Paid-Risk Screens**
   Name the screens that are evidence-backed enough to use, the ones that are too speculative, and how each should affect posture.

6. **Sponsor-Earlier Economics**
   Give a simple expected-value or decision-threshold framework. Explain what precision/lift would be needed for early sponsorship to be rational.

7. **Validation Plan**
   Define historical cutoffs, feature windows, outcome labels, baselines, leakage controls, metrics, and ship/kill thresholds. Include ablations proving acceleration beats momentum.

8. **Display / Product Boundary**
   State how the signal may be shown internally and what must never be shown externally. Include no vanity score, no accusations, no outreach authorization, and no zero-fill.

9. **Kill Criteria**
   State when Aphrodite should abandon acceleration, keep it as watchlist only, or revert to momentum.

10. **Next Step**
   Give one smallest next step. It must not be "build the whole lane."

### Answer Style

Be adversarial and quantitative. Push back hard on attractive but weak assumptions. Prefer a boring defensible watchlist over an impressive unvalidated score. If the honest answer is "acceleration might be overpowered only after a backtest proves incremental lift over momentum," say that plainly.
