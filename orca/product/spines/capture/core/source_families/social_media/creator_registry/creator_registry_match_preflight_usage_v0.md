# Creator Registry Match Preflight Usage v0

```yaml
retrieval_header_version: 1
artifact_role: Operator-facing usage note
scope: >
  How discovery and capture lanes use the Creator Registry match preflight
  before starting new social creator capture.
use_when:
  - A scan lane has candidate creator/account handles or profile URLs.
  - A capture lane is about to start a new social creator capture.
  - A cold agent needs to distinguish already-known creators/accounts from new candidates.
authority_boundary: usage_guidance_only
```

## Required Preflight

Before starting a new social creator capture, pass the candidate account batch
through `orca-harness/runners/run_creator_registry_match_preflight.py` against
the current `creator_profile_current_view_v0.json`.

The preflight emits a receipt for each candidate:

- `existing_match`: do not create a new creator/account capture; update or work
  against the matched registry identity.
- `new_candidate`: a new capture may proceed for candidates whose
  `intended_action` is `new_capture`.
- `ambiguous_match`: stop and resolve identity before capture.
- `invalid_candidate`: fix the candidate input before capture.

The runner exits nonzero when a requested action is blocked, including
`new_capture` on an existing or ambiguous candidate.

## Candidate Input

Candidate rows must provide:

- `candidate_id`
- `intended_action`: `classify`, `new_capture`, or `update_existing`
- at least one matchable identity: platform handle, profile URL,
  `platform_account_id_or_none`, `profile_subject_id_or_none`, or
  `platform_public_account_id_or_none`

For handle-only candidates, provide `platform`. Profile URLs may infer platform
for known social hosts. Unsupported platforms or unknown profile URL hosts are invalid candidates.

## Non-Claims

This preflight is exact-match enforcement only:

- not fuzzy display-name matching
- not cross-platform creator identity proof
- not proof that discovery searched enough
- not silver metric refresh
- not registry mutation
- not live social search

## Accepted Residuals

Fuzzy duplicates may still pass. This is accepted until exact preflight fails to
prevent repeated duplicate captures.

Cross-platform identity remains outside this runner. Use the public-handle
linkage workflow for creator-level promotion.

Metric freshness is not handled here. If the candidate already exists but stats
are stale, update the existing identity in the relevant capture/metric lane.
