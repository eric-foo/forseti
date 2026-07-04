# Creator Registry Cold-Agent Preflight Rehearsal v0

```yaml
retrieval_header_version: 1
artifact_role: workflow_evidence_record
scope: >
  Cold-agent rehearsal of the Creator Registry match preflight behavior for
  social creator scan-to-capture handoffs after the registry preflight became
  required receipt evidence.
use_when:
  - A scan or capture lane needs the behavioral example for blocking duplicate creator/account capture.
  - A cold agent needs to understand the row-level `can_start_new_capture` field before starting social creator capture.
  - Checking the operational boundary between Creator Registry lookup and actual capture or metric refresh.
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - orca-harness/runners/run_creator_registry_match_preflight.py
  - orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py
authority_boundary: retrieval_only
```

## Status

`REHEARSAL_RECORD_V0`.

This records one no-network, no-capture rehearsal of the committed Creator
Registry match preflight. It is not validation, readiness, live capture
authorization, fuzzy identity matching, cross-platform identity proof, registry
mutation, or Silver metric refresh.

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_creator_registry_preflight_rehearsal
  edit_permission: docs-write
  target_scope:
    - docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/validation-gates.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
    - orca-harness/runners/run_creator_registry_match_preflight.py
    - orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py
```

## Sources Re-Read

- `docs/workflows/creator_registry_record_contract_handoff_v0.md`: confirmed
  the original record-contract lane drift guard still matters here: no capture,
  no lake writes, and no identity-ledger writes.
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`:
  confirmed a social creator/account capture must carry the receipt row's
  `intended_action`, `decision`, `action_status`, and
  `can_start_new_capture`; only `can_start_new_capture: true` on
  `intended_action: new_capture` clears new capture.
- `orca-harness/runners/run_creator_registry_match_preflight.py`: confirmed
  the runner writes a receipt and exits `2` when any requested action is
  blocked.
- `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py`:
  confirmed the receipt wrapper, candidate schema, summary fields, row-level
  decision fields, and the `has_blocking_preflight_results` exit predicate.
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`:
  confirmed the committed registry currently carries `profiles_total: 33`,
  `platform_account_profiles: 33`, `creator_record_profiles: 0`,
  `cross_platform_rollup_profiles: 0`, `profiles_with_metric_rollups: 33`,
  `engagement_rate_observed_profiles: 31`, and
  `profiles_with_ideal_audience_profiles: 0`.

Freshness note: this rehearsal's 33-profile count is historical run evidence.
Later Creator Ledger MGT closure checkpoints use the refreshed 36-profile
receipt/profile-view source; do not use this rehearsal as the current registry
profile-count source.

## Rehearsal Setup

The rehearsal used temporary local candidate JSON files under
`.tmp_creator_registry_rehearsal/`. Those files were scratch inputs and are not
part of this artifact.

Two candidate shapes were tested:

| Candidate | Intended action | Identity facts | Purpose |
| --- | --- | --- | --- |
| `rehearsal_existing_bowtie_new_capture` | `new_capture` | YouTube account `BowTieFragranceGuy`, profile URL `https://www.youtube.com/channel/UCVvzGrPSok_sf8hfDhvTg7w`, `platform_account_id_or_none: acct_yt_fragrance_001`, `platform_public_account_id_or_none: UCVvzGrPSok_sf8hfDhvTg7w` | Prove a known registry row does not clear a duplicate new capture. |
| `rehearsal_synthetic_unique_new_capture` | `new_capture` | Synthetic YouTube handle/profile URL `orca_rehearsal_unique_20260704` | Prove an exact-unmatched row can clear the preflight mechanically. This is not a real creator recommendation. |

## Observed Runner Behavior

Mixed batch command:

```powershell
python orca-harness\runners\run_creator_registry_match_preflight.py `
  --candidates .tmp_creator_registry_rehearsal\mixed_candidates.json `
  --output .tmp_creator_registry_rehearsal\mixed_receipt.json `
  --generated-at-utc 2026-07-04T12:00:00Z
```

Observed mixed-batch exit: `2`.

Observed mixed-batch summary:

```json
{"ambiguous_matches":0,"blocked_actions":1,"existing_matches":1,"invalid_candidates":0,"new_candidates":1,"safe_to_capture_new":1,"total_candidates":2}
```

Synthetic-only command:

```powershell
python orca-harness\runners\run_creator_registry_match_preflight.py `
  --candidates .tmp_creator_registry_rehearsal\synthetic_only_candidates.json `
  --output .tmp_creator_registry_rehearsal\synthetic_only_receipt.json `
  --generated-at-utc 2026-07-04T12:00:01Z
```

Observed synthetic-only exit: `0`.

Observed synthetic-only summary:

```json
{"ambiguous_matches":0,"blocked_actions":0,"existing_matches":0,"invalid_candidates":0,"new_candidates":1,"safe_to_capture_new":1,"total_candidates":1}
```

## Row-Level Results

| Candidate | Decision | Action status | `can_start_new_capture` | Blockers | Matched registry profile |
| --- | --- | --- | --- | --- | --- |
| `rehearsal_existing_bowtie_new_capture` | `existing_match` | `blocked` | `false` | `new_capture_existing_match` | `acct_yt_fragrance_001` / `BowTieFragranceGuy` |
| `rehearsal_synthetic_unique_new_capture` | `new_candidate` | `allowed` | `true` | none | none |

The existing-row match carried these observed match reasons:

```json
["platform_account_id","platform_public_account_id","public_profile_url","same_platform_public_handle"]
```

## Behavioral Before And After

Before this preflight path, a cold scan runner could manually open the registry
or static projection and decide whether a creator looked new. That was useful
orientation, but it was not a mechanical receipt and it could not consistently
feed a capture handoff.

After this preflight path, the cold runner submits candidate accounts to the
registry runner, preserves the receipt, and carries four row fields forward:
`intended_action`, `decision`, `action_status`, and
`can_start_new_capture`. A known account can still be updated or resolved as an
existing identity, but it does not clear a new creator/account capture. An
exact-unmatched account clears only at the row level, through
`can_start_new_capture: true`.

Mixed batches are intentionally strict at the process level: if one requested
action is blocked, the runner exits nonzero even when another row clears. A
cold agent must inspect row-level results instead of treating the whole batch
as all allowed or all blocked.

## Operational Use

For discovery/scanning, this means a runner can use the registry to avoid
recapturing creators already present in the committed profile view. The static
projection is still the readable scan surface, but the runner receipt is the
handoff evidence.

For capture, this means a new social creator/account capture starts only when
the relevant receipt row says `intended_action: new_capture` and
`can_start_new_capture: true`. If the row says `existing_match`, the lane should
work against or update the matched registry identity instead of creating a new
capture target.

For metrics, this does not refresh follower counts, views, engagement, cadence,
or Silver rollups. Existing-account metric refresh remains owned by the
appropriate capture/Silver lane.

## Accepted Residuals

- Exact-match only: fuzzy display-name duplicates can still pass.
- Account-level only: this does not prove cross-platform person identity.
- Source adequacy not proven: a `new_candidate` receipt does not prove the scan
  searched enough or that the candidate is worth capturing.
- Receipt existence is workflow-bound: downstream docs/checkers can require the
  receipt fields, but a local ephemeral receipt path is not itself committed
  registry state.
- Metric freshness is separate: an existing match may still need a stats refresh
  in the relevant capture/Silver lane.

## Next Material Steps

1. Reuse this behavior in the next cold scan/capture handoff prompt: ask the
   runner to produce the candidate batch, run the preflight, and carry the four
   row fields into the handoff before any new social creator capture.
2. Add a small canonical candidate-batch example only if the next cold runner
   stumbles on JSON shape. The runner and usage note are already sufficient for
   a competent agent; an example should be demand-driven, not ceremony.
3. Defer broader enforcement until a real miss appears. The current mechanical
   boundary blocks under-specified scan artifacts and report fields, while the
   preflight runner blocks duplicate `new_capture` at execution time. The next
   higher-value work is live use on a real discovery lane, not another abstract
   rule.
