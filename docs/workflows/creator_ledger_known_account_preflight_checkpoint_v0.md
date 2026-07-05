# Creator Ledger Known-Account Preflight Proof Checkpoint v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: >
  Second operational proof-loop checkpoint for the Creator Ledger: applies the
  migration-stable, efficacy-first contract to a known-account preflight probe
  that allows update-existing routing, blocks duplicate new capture, and leaves
  registry/profile data untouched.
use_when:
  - Checking whether the Creator Ledger has proof for known-account duplicate prevention, not only new-candidate scan handoff.
  - Planning a future repeat-observation or update-existing lane without remigrating registry data.
  - Separating exact-match operational efficacy from fuzzy identity, capture, metric, or Silver claims.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - docs/workflows/creator_ledger_known_account_preflight_receipt_v0.json
  - docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md
  - orca-harness/runners/run_creator_registry_match_preflight.py
  - orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json
stale_if:
  - The Creator Ledger operational evolution contract changes its intake or proof-loop fields.
  - The Creator Registry match-preflight runner changes row-level action semantics.
  - The preserved known-account preflight receipt is amended or replaced.
```

## Purpose

This checkpoint applies the Creator Ledger proof loop to a fresh read-only
Creator Registry match-preflight probe. It is not a scan, not Capture, not
registry mutation, not a metric refresh, not a Silver write, and not a claim that
the Creator Ledger has achieved God Tier.

The point is to prove a second operational efficacy path: known accounts can be
routed toward existing work while duplicate new-capture requests are blocked,
using a preserved receipt rather than rewriting existing registry/profile rows.

## Source Basis

Sources read or executed for this checkpoint:

- `creator_ledger_operational_evolution_contract_v0.md`: owns the additive
  upgrade intake, proof-loop fields, and efficacy-first God Tier lens.
- `creator_registry_match_preflight_usage_v0.md`: owns preflight usage,
  row-level clearance semantics, and non-claims.
- `creator_registry_cold_agent_preflight_rehearsal_v0.md`: prior rehearsal of
  blocked duplicate capture and row-level `can_start_new_capture` behavior.
- `run_creator_registry_match_preflight.py`: runner invoked for this probe.
- `registry_match_preflight.py`: exact-match logic and action-disposition owner.
- `creator_profile_current_view_v0.json`: registry source used by the runner.
- `creator_ledger_known_account_preflight_receipt_v0.json`: preserved receipt
  emitted by the runner for this checkpoint.

Observed command shape:

```powershell
python orca-harness/runners/run_creator_registry_match_preflight.py `
  --candidates .tmp_creator_ledger_proof\known_account_preflight_candidates_v0.json `
  --registry forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json `
  --output docs/workflows/creator_ledger_known_account_preflight_receipt_v0.json `
  --generated-at-utc 2026-07-04T16:00:05Z
```

Observed runner exit: `2`. This is expected because one row intentionally
requested `new_capture` for an existing account and was blocked.

Observed receipt summary:

```yaml
schema_version: creator_registry_match_preflight_receipt_v0
generated_at_utc: 2026-07-04T16:00:05Z
total_candidates: 3
existing_matches: 2
new_candidates: 1
ambiguous_matches: 0
invalid_candidates: 0
blocked_actions: 1
safe_to_capture_new: 1
registry_source_pointer: forseti\product\spines\capture\core\source_families\social_media\creator_registry\creator_profile_current_view_v0.json
registry_source_generated_at_utc: 2026-07-03T09:04:50Z
registry_source_profiles_total: 36
registry_source_sha256: a0998cb1100dbeccb8e77768f847ba0f688edcf0105b6485abbffd02f0ac1e49
```

## Additive Upgrade Intake Applied

- efficacy target: duplicate-work prevention and known-account routing;
- owning layer: Creator Registry exact-match preflight over
  `creator_profile_current` account identities;
- additive record path: a preserved workflow receipt and checkpoint beside the
  registry, not a rewrite of the registry or profile-current JSON;
- stable-id posture: existing `platform_account_id` values
  `acct_yt_fragrance_001` and `acct_yt_fragrance_002` remain untouched;
- source and lineage posture: the receipt carries registry source pointer, hash,
  generated timestamp, and profile count;
- missingness posture: fuzzy identity, source adequacy, metric freshness,
  capture execution, and Silver refresh remain explicit residuals;
- proof checkpoint: this record plus the preserved receipt; and
- forbidden move check: no historical rows were rewritten, no profile-current
  row became source truth, and no sibling records were collapsed into a
  convenience blob.

## Proof Loop Checkpoint

### Owning Layer

Primary owning layer: Creator Registry exact-match preflight over
`creator_profile_current` account identities.

Supporting layers:

- runner receipt as row-level workflow evidence;
- preflight usage note as the semantic owner for action fields;
- prior cold-agent rehearsal as background behavior evidence; and
- Creator Ledger operational evolution contract as the upgrade rule.

### Additive Path

This proof adds only:

- a generated preflight receipt under `docs/workflows/`; and
- this checkpoint record that summarizes the observed receipt.

It does not add, remove, or rewrite any registry index rows, linkage rows,
profile-current rows, metric observations, capture records, or Silver records.

### Migration-Stability Evidence

This proof preserves migration stability because:

- existing registry/profile rows are read-only inputs;
- the receipt records the registry source pointer, hash, profile count, and
  generated timestamp used at run time;
- matched account ids are stable ledger ids, not replaced by probe ids;
- the synthetic unmatched row stays a probe candidate, not an admitted creator;
  and
- row-level action semantics carry the next action without remigrating data.

### Efficacy Outcome

The preserved receipt shows three useful row-level outcomes:

| Candidate | Intended action | Decision | Action status | `can_start_new_capture` | Next action |
| --- | --- | --- | --- | --- | --- |
| `proof_existing_bowtie_update_existing` | `update_existing` | `existing_match` | `allowed` | `false` | `update_existing` |
| `proof_existing_chaos_new_capture_blocked` | `new_capture` | `existing_match` | `blocked` | `false` | `update_existing` or `resolve_identity_if_not_same` |
| `proof_synthetic_unique_new_capture_allowed` | `new_capture` | `new_candidate` | `allowed` | `true` | `new_capture` |

This makes the ledger more operational in two ways:

- a known account can be routed to `update_existing` instead of recaptured as a
  new account; and
- a duplicate `new_capture` request against a known account is blocked while a
  genuinely exact-unmatched row still clears at row level.

That is efficacy evidence. It is not evidence that the known account was
actually updated, that Capture ran, or that the synthetic candidate is worth
capturing.

### Accepted Residuals

Accepted residuals for this checkpoint:

- exact-match only; no fuzzy display-name duplicate detection;
- account-level only; no cross-platform person identity proof;
- no repeat-observation attachment record is written yet;
- no capture execution, registry mutation, metric refresh, or Silver write;
- the synthetic unmatched row is a mechanical clearance probe, not a real creator
  recommendation; and
- local runner execution plus preserved receipt is workflow evidence, not runtime
  deployment or validation.

## Operational Meaning

This is the second concrete proof-loop checkpoint for the Creator Ledger. The
first checkpoint showed additive new-candidate scan-to-handoff behavior. This
one shows exact known-account routing: the same preflight surface can distinguish
`update_existing`, blocked duplicate `new_capture`, and allowed exact-unmatched
`new_capture` without remigrating existing data.

The next stronger proof should attach a repeat observation or capture-refresh
handoff to an existing `platform_account_id` as an additive sibling record or
workflow checkpoint. That would move from preflight routing to actual
repeat-observation evidence while preserving the same stable-id contract.

## Non-Claims

- not validation
- not readiness
- not capture authorization
- not registry mutation
- not Silver write authorization
- not fuzzy duplicate detection
- not cross-platform identity proof
- not repeat-observation attachment execution
- not dashboard implementation
- not storage-engine adoption
- not buyer proof
- not proof that the Creator Ledger has achieved God Tier
