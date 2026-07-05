# Creator Ledger Additive Upgrade Intake Rehearsal v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: >
  Non-conforming additive-upgrade intake rehearsal for the Creator Ledger,
  using ideal/content-fit audience profile snapshots as the capability that
  does not fit the initial routing matrix cleanly.
use_when:
  - Demonstrating how to route a future Creator Ledger capability that does not map cleanly to one capability-routing row.
  - Planning ideal/content-fit audience profile support without remigrating Creator Registry or creator_profile_current data.
  - Checking that God Tier progress remains efficacy-oriented rather than audit-completeness-oriented.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - orca-harness/capture_spine/creator_profile_current/ideal_audience_snapshot.py
  - orca-harness/capture_spine/creator_profile_current/materialize.py
  - orca-harness/capture_spine/creator_profile_current/validation.py
stale_if:
  - The Creator Ledger capability routing matrix adds an explicit audience-profile row.
  - The ideal-audience snapshot schema or creator_profile_current materializer changes audience join semantics.
  - A later accepted Creator Signal or audience-profile contract supersedes this rehearsal.
```

## Purpose

PR #699's delegated review found one coverage gap: the additive-upgrade-intake
escape hatch was described but not demonstrated for a capability that does not
fit the routing matrix cleanly.

This rehearsal closes that proof-shape gap without changing data. It runs the
intake on a plausible future capability: joining source-backed
ideal/content-fit audience profile snapshots into `creator_profile_current`.
That capability touches content/audience inference, profile-current display, and
Creator Signal usefulness, so it should not be forced into the identity,
metric, observation, or buyer-proof rows by convenience.

This is not implementation, not a snapshot write, not a profile refresh, and not
a claim that ideal-audience support is ready.

## Source Basis

Sources read for this rehearsal:

- `creator_ledger_operational_evolution_contract_v0.md`: owns the routing
  matrix, Additive Upgrade Intake, proof-loop shape, and efficacy-first God Tier
  lens.
- `creator_profile_current_record_contract_v0.md`: states the consumer-visible
  `ideal_audience_profile` surface is nullable/stubbed and not evidence that an
  actual audience was estimated.
- `ideal_audience_snapshot.py`: defines
  `creator_ideal_audience_profile_snapshot_v0`, requires source evidence ids,
  preserves `actual_audience: not_estimated`, and validates subject identity.
- `materialize.py`: can load optional audience snapshot documents, join them by
  profile subject, include their source hashes, and keep the read model as a
  generated profile-current view.
- `validation.py`: validates joined ideal-audience snapshots, subject matching,
  profile counts, and existing non-claim boundaries.

## Non-Conforming Capability

Capability proposal:

> Show an ideal/content-fit audience profile for a known creator account when a
> source-backed Tier-1 audience snapshot exists.

Why it does not fit one initial matrix row cleanly:

- It is not exact known-account lookup or duplicate-capture prevention.
- It is not public-handle linkage or person identity proof.
- It is not a source-visible metric fact or metric rollup.
- It is not a raw source-family observation row, although it depends on
  source-backed evidence records.
- It is not purely operator-facing interpretation, because the current
  materializer already has a structured nullable `ideal_audience_profile` join
  point and source-input hash posture.

Missing owner named by this rehearsal:

`creator_ideal_audience_profile_snapshot_v0` is the candidate owning sibling
record for source-backed ideal/content-fit audience inference. It is consumed by
`creator_profile_current` as a read-model join and by Creator Signal as a future
interpretation input. It is not registry identity, metric truth, actual-audience
measurement, or buyer proof.

## Additive Upgrade Intake

- efficacy target: improve product usefulness and identity decision support by
  letting a profile show content-fit audience texture when source evidence
  exists, while preserving visible missingness when it does not.
- owning layer: a sibling ideal-audience snapshot layer, currently represented
  by `creator_ideal_audience_profile_snapshot_v0`, with profile-current as a
  generated read-model join and Creator Signal as the future presentation layer.
- additive record path: add or preserve a
  `creator_ideal_audience_profile_snapshot_v0` document keyed by
  `profile_subject_kind` and `profile_subject_id`; then pass it into
  `build_creator_profile_current_view_from_files()` via
  `audience_profile_snapshot_path(s)`. Do not rewrite registry rows.
- stable-id posture: existing `platform_account_id` and future
  `creator_record_id` values remain untouched. New
  `audience_profile_snapshot_id` values are snapshot-local and derived from the
  subject, evidence ids, and profile body.
- source and lineage posture: source truth stays in the evidence records named
  by the snapshot's `evidence_ids`; the read model records the snapshot source
  pointer and sha256 as a `source_inputs` entry.
- missingness posture: profiles without snapshots keep
  `ideal_audience_profile: null` and `audience_computed_at_or_none: null`;
  joined snapshots keep `actual_audience: not_estimated`.
- proof checkpoint: the first operational checkpoint should materialize one
  existing profile with a fixture-quality source-backed ideal-audience snapshot,
  verify the view count `profiles_with_ideal_audience_profiles`, and show that
  profiles without snapshots retain explicit null missingness.
- forbidden move check: do not populate actual-audience demographics, do not
  infer buyer proof, do not collapse audience inference into registry identity,
  do not rewrite `creator_profile_current_view_v0.json` by hand, and do not make
  Creator Signal claims until the display contract can preserve limitations and
  non-claims.

## Migration-Stability Evidence

The additive route preserves migration stability because:

- identity rows stay in the public-handle linkage ledger;
- metric observations and rollups stay in metric-owned records;
- audience inference lives in snapshot records with their own schema, evidence
  ids, limitations, and snapshot ids;
- `creator_profile_current` remains a generated read model that joins the
  snapshot by stable subject id; and
- consumers can distinguish "snapshot absent" from "actual audience estimated"
  because both null missingness and `actual_audience: not_estimated` are
  explicit.

## Efficacy Outcome

This rehearsal is proof-shape evidence, not capability validation. It shows that
the Additive Upgrade Intake can route a non-clean capability before build or
handoff:

- the missing owner is named instead of squeezing the feature into the wrong
  matrix row;
- the additive record path is described without remigrating existing data;
- the future proof checkpoint is concrete and small; and
- God Tier progress is judged by whether the ledger becomes more useful without
  overclaiming, not by whether more audit fields exist.

## Accepted Residuals

- no ideal-audience snapshot is written by this rehearsal;
- no `creator_profile_current_view_v0.json` refresh is performed;
- no Creator Signal display contract is changed;
- the initial routing matrix still lacks a first-class audience-profile row;
- actual audience remains not estimated;
- source evidence adequacy for any future snapshot is not evaluated here; and
- no product, buyer-proof, ranking, outreach, or dashboard claim is authorized.

## Non-Claims

- not validation
- not readiness
- not implementation authorization
- not capture authorization
- not registry mutation
- not profile-current refresh
- not actual-audience measurement
- not buyer proof
- not Creator Signal display readiness
- not proof that the Creator Ledger has achieved God Tier
