# Creator Profile Current Record Contract v0

```yaml
retrieval_header_version: 1
artifact_role: source_capture_family_architecture_contract
scope: >
  Consumer-facing per-profile record contract for creator_profile_current:
  visible field surface, interpretation promises, and declared-deferred global
  metric recipes for posting_cadence and recent_velocity.
use_when:
  - Explaining what one creator_profile_current profile record exposes to a downstream reader.
  - Checking how consumers may interpret current_metric_rollups, source_drill_back, freshness, limitations, and non_claims.
  - Deciding how posting_cadence or recent_velocity may become populated from Silver history without changing the v0 record surface.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - orca-harness/capture_spine/creator_profile_current/materialize.py
  - orca-harness/capture_spine/creator_profile_current/validation.py
stale_if:
  - creator_profile_current_view_spec_v0.md changes the profile, metric rollup, or aggregate influence record shape.
  - creator_profile_current_view_v0.json changes current_metric_rollups metric keys or posture/value field names.
  - creator_metric_silver_record_contract_v0.md changes MetricRollupObservation posture or lineage semantics.
  - creator_intelligence_profile_surface_v0.md changes customer-facing claim, limitation, missingness, freshness, non-claim, or source-drill-back display policy.
```

## Purpose

This contract pins the v0 shape a downstream reader sees when opening one
`creator_profile_current` profile, and the promises that prevent that reader
from overinterpreting missing, stale, or source-limited data.

Use this as the consumer contract for the read model. Do not use it as capture
cadence policy, discovery scale policy, identity-linkage write authority, buyer
proof, dashboard readiness, live capture authorization, or lake-write
authorization.

## Source Basis

The record surface is derived from:

- `creator_profile_current_view_v0.json` at `origin/main` blob
  `ae065ecfe38f30d0998d9fab8babdd8f136a1429`.
- `creator_profile_current_view_spec_v0.md` at `origin/main` blob
  `72368b858630764f44f490e6fc71bd203b111dd3`.
- `materialize.py` at `origin/main` blob
  `4eb0f91ec4ce95327712da00d195a4338ceb279d`.
- `validation.py` at `origin/main` blob
  `70a1caa689d3183bc31f74e4c9f7c3881217f61d`.

Recheck those sources before making strict claims if the view/spec/materializer
or Silver record contract changes.

## Section 1 - Per-Creator Visible Record Surface

Section 1 is the visible per-profile surface: the parts a downstream reader can
open for one creator/account profile. In the current committed view these are
account-scoped `platform_account` profiles; `creator_record` profiles remain
absent until promoted public-handle linkage exists.

### Subject And Identity

Each profile exposes:

- `profile_subject_kind`
- `profile_subject_id`
- `platform_account_id_or_none`
- `creator_record_id_or_none`
- `identity_state`
- `link_state_or_none`
- `review_state_or_none`
- `platform_accounts`
- `identity_evidence_summary`

For current single-platform rows, the subject is one public platform account.
The profile does not claim public person identity, outreach authorization, or a
cross-platform creator record.

### current_metric_rollups

`current_metric_rollups` is the metric panel for the profile. It is a list of
the latest allowed rollup records by subject/platform/window. The current
materialized view carries one account-scoped rollup per profile.

Each rollup exposes:

- `metric_rollup_id`
- `metric_rollup_pointer`
- `platform_scope`
- `platform_account_ids`
- `rollup_window`
- `rollup_window_description`
- `content_kind_inclusion_rule`
- `metric_rollups`
- `source_metric_observation_ids`
- `observation_count`
- `view_count_min`
- `view_count_max`
- `sample_support`
- `calculation_recipe_version`
- `computed_at`
- `freshness_state`
- `limitations`

The nested `metric_rollups` map is the computed-stat field set:

- `average_views`
- `median_views`
- `average_like_count`
- `average_comment_count`
- `engagement_rate`
- `posting_cadence`
- `recent_velocity`

In v0, `average_views` and `median_views` are observed where source-backed.
`average_like_count`, `average_comment_count`, and `engagement_rate` are
observed only when their source-visible numerator and denominator inputs exist.
`posting_cadence` and `recent_velocity` are contract fields, but they remain
declared-deferred as `not_attempted` until Silver history can support them.

### source_drill_back

`source_drill_back` is the evidence pointer panel. It connects the visible
profile back to the sibling source rows instead of making the read model a
second source of truth.

It exposes:

- `identity_ledger_pointer`
- `metric_rollup_pointer`
- `metric_snapshot_pointer`
- `source_metric_observation_ids`

Consumers must use these pointers for audit or source drill-back. They must not
infer unsupported identity linkage, hidden source fields, or unlisted metric
inputs from the current profile row.

### freshness

`freshness` is the timestamp panel for the read model:

- `identity_updated_at`
- `metrics_computed_at_or_none`
- `audience_computed_at_or_none`
- `profile_view_computed_at`

Consumers may treat these as record freshness signals only. They do not prove
that the underlying source surface is complete, representative, or unchanged
after capture.

### limitations

`limitations` is a visible warning panel. It must travel with the profile and
with each rollup because the current rollups are admitted-pool or selected-grid
statistics, not channel-wide creator averages.

Consumers must surface or enforce these limitations before ranking, comparing,
or summarizing creators. A metric with a large value and a thin/source-limited
sample is still source-limited.

A collapsed customer surface may summarize limitations, but the summary must
carry every material missingness state that affects interpretation. If a
metric in `current_metric_rollups` is `unavailable_with_reason`, `out_of_window`,
`not_attempted`, or `not_applicable`, the customer surface must show that
posture either adjacent to the metric or in an always-reachable
limitations/missingness panel. Raw JSON-only posture is not enough for a
customer-facing surface.

### non_claims

`non_claims` is the hard negative promise panel. It names what the profile does
not authorize or prove, including channel-wide influence, buyer proof,
person-level identity, contact/outreach authorization, cross-platform rollups,
dashboard readiness, SQLite adoption, and data-lake physicalization.

Consumers must not treat absent non-claim handling as permission to make the
claim elsewhere. If a downstream surface wants to make one of these claims, it
needs its own controlling source and proof.

`non_claims` may be collapsed behind a claim-boundaries/details affordance, but
it must not be omitted. A customer-facing surface that presents profile metrics,
summaries, ranking inputs, or outreach-adjacent interpretation must make
`non_claims` reachable before the customer relies on that interpretation.

### Nullable Or Stubbed Surfaces

`ideal_audience_profile`, `wind_calling_summary`, and review/linkage fields may
be null. Null means the surface is not joined, not applicable, or not authorized
for this profile state. It does not mean negative evidence about the creator.

## Section 2 - Consumer Interpretation Contract

Section 2 is the reader promise. It states how a downstream consumer may
interpret the visible surface from Section 1.

### Read Model Boundary

`creator_profile_current` is a current read model over sibling identity and
metric records. It is not the source of truth for identity, raw metrics,
audience inference, buyer proof, outreach permission, or capture cadence.

The current materializer reads platform account identity rows and platform
metric rollup snapshots, then copies the allowed rollup payload into
`current_metric_rollups`. It does not compute global longitudinal stats inside
the registry read model.

### Progressive Disclosure Boundary

This contract permits a clean first screen only as progressive disclosure, not
as omission. A downstream single-profile customer surface may keep full
`limitations`, `non_claims`, `source_drill_back`, formulas, and source row
pointers in a details panel when all of these are true:

- the primary surface keeps visible trust posture for every metric or summary it
  shows, including freshness, sample/representativeness, and non-observed
  metric posture when material;
- the details panel exposes full `limitations`, `non_claims`, `source_drill_back`,
  calculation recipe/version, and lineage before ranking, comparison,
  shortlisting, outreach-adjacent interpretation, or any stronger product claim;
- `not_attempted`, `unavailable_with_reason`, `out_of_window`, and
  `not_applicable` values remain null-with-reason and are not displayed as zero,
  ranked, averaged, or converted into a comparable score; and
- claim-boundary cues are available from the start, even when the full text is
  collapsed.

This contract does not define a multi-creator ranking, grid, shortlist, lead
list, or outreach workflow. Those surfaces require a separate accepted Creator
Signal or successor display contract before implementation. Until then, this
contract authorizes only per-profile interpretation plus manually checked
comparisons that satisfy the rules below.

### Posture And Value Coupling

Every metric value must obey:

```text
observed -> numeric value and no reason
non-observed -> null value and a reason
```

Non-observed includes `unavailable_with_reason`, `out_of_window`,
`not_attempted`, and `not_applicable`. A non-observed metric is never a numeric
zero and must not be ranked, averaged, or displayed as zero performance.

### Metric Comparison Rules

Consumers may compare metric values only when:

- both metrics are `observed`;
- platform scope and content-kind inclusion are compatible;
- rollup windows are compatible or explicitly normalized;
- sample support and representativeness posture are visible; and
- limitations do not rule out the comparison.

If any condition fails, the consumer may show the field with its posture and
reason, but must not convert it into a comparable score.

### Lineage Promise

`source_drill_back` promises that the current profile points back to identity
and metric source rows. It does not promise that every upstream source remains
live, complete, representative, or source-visible after capture.

Any strict audit, refresh, or rebuild must use the source pointers and the
owning Silver/Capture records, not the profile row alone.

### Freshness Promise

`freshness` promises when the read model was assembled and when joined identity,
metric, or audience data was computed. It does not promise capture cadence,
future refresh timing, source availability, or that a stale source should be
treated as current.

### Identity And Cross-Platform Promise

Single-platform profiles are account profiles. Cross-platform rollups or
`creator_record` profiles require promoted public-handle linkage. Candidate or
rejected links may support review/disambiguation context only; they must not
collapse accounts or produce cross-platform aggregate influence.

### Limitation And Non-Claim Promise

Limitations and non-claims are part of the contract, not UI footnotes. A
consumer that cannot preserve them should withhold the affected interpretation
rather than silently downgrade or overclaim it.

## Section 3 - Declared-Deferred Global Metric Recipes

The v0 contract includes global stats as declared-deferred fields. That means
the field names, source ownership, lineage expectations, and activation
conditions are pinned now, while numeric population waits for Silver-side
longitudinal inputs.

This is not a registry-side computation mandate. Silver owns the longitudinal
history and rollup production. The registry stores and presents the latest
accepted rollup result once Silver can emit it with posture/value coupling and
source lineage.

### posting_cadence

Storage surface:

`current_metric_rollups[].metric_rollups.posting_cadence`

Current v0 posture:

- `posture: not_attempted`
- `value_or_none: null`
- `posture_reason_or_none`: cadence recipe is out of scope for the current live
  metric document or metric seed

Recipe target:

```text
posting_cadence = observed_content_count / window_days
```

Required before first observed population:

- a named `calculation_recipe_version`;
- a stable subject (`platform_account` or promoted `creator_record`);
- source-backed content records or MetricObservation/MetricRollupObservation
  history for that subject;
- source-backed publication timestamps, or an explicitly named recipe that
  says it is capture cadence rather than posting cadence;
- a declared window such as 30d, 90d, lifetime_known, or custom;
- source record ids used in the count;
- posture/value coupling for the resulting rate; and
- limitations when the observed set is admitted-pool-only, selected-grid-only,
  or otherwise non-representative.

If publication timestamps are unavailable, the field must remain non-observed
with a reason. Capture timing must not be smuggled in as posting behavior.

### recent_velocity

Storage surface:

`current_metric_rollups[].metric_rollups.recent_velocity`

Current v0 posture:

- `posture: not_attempted`
- `value_or_none: null`
- `posture_reason_or_none`: velocity recipe is out of scope for the current live
  metric document or metric seed

Recipe target:

```text
recent_velocity =
  (latest_compatible_rollup_value - prior_compatible_rollup_value)
  / elapsed_days_between_rollups
```

Default metric target:

`average_views`, unless a later accepted recipe version names a different base
metric such as engagement_rate.

Required before first observed population:

- a named `calculation_recipe_version`;
- at least two compatible Silver rollup observations for the same subject;
- compatible platform scope, content-kind inclusion rule, selection policy,
  and rollup window;
- observed numeric values for the base metric in both rollups;
- a positive elapsed time between rollup computations or window endpoints;
- source record ids for both rollups and their underlying observations;
- posture/value coupling for the resulting rate; and
- limitations when source population changes make the trend directional rather
  than representative.

If compatible history does not exist, the field must remain non-observed with a
reason. A single capture cycle cannot produce recent velocity.

### First Population Rule

No schema change is required when these fields first become populated. The first
population is allowed only when the Silver-side producer emits accepted
recipe-backed values with lineage and posture/value coupling. At that point the
registry read model may copy the observed numeric value into the existing field.

If the recipe changes, update the rollup `calculation_recipe_version` and
recheck consumer compatibility before comparing old and new values.

While `posting_cadence` or `recent_velocity` remain `not_attempted`, a customer
surface that shows aggregate influence must expose that declared-deferred state
either beside the metric family or in the limitations/missingness panel. A
formula or field name alone must not imply the value is populated, formula-ready
for ranking, or expected to be treated as zero.

## Accepted Residuals

- Global stats are declared-deferred, not populated.
- The current view is platform-account scoped; no `creator_record` profiles or
  cross-platform rollups exist in the committed view.
- Current rollups remain source-pool limited and are not representative
  channel-wide creator averages.
- The contract does not create a lake producer, dashboard, API, SQLite table,
  capture cadence policy, or live capture run.

## Non-Claims

- not validation
- not readiness
- not buyer proof
- not capture cadence policy
- not discovery scale policy
- not identity write authority
- not live capture authorization
- not lake-write authorization
- not dashboard implementation
- not SQLite or backend selection
- not cross-platform identity proof
