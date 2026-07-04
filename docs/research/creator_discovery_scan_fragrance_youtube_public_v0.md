# Fragrance YouTube Public Creator Discovery Scan v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  First small live scan of public/no-login English-language YouTube fragrance
  creator or reviewer accounts not already present in the Creator Registry by
  exact-match preflight.
use_when:
  - Reviewing the first bounded Creator Registry cold-scan operational run.
  - Carrying preflight-cleared public YouTube fragrance creator/account candidates into a capture-request handoff.
  - Checking the residual receipt-provenance scope note before stronger checker verification exists.
authority_boundary: retrieval_only
open_next:
  - docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json
  - docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md
stale_if:
  - creator_profile_current_view_v0.json changes.
  - The Creator Registry match preflight runner changes receipt fields or exit behavior.
  - Any candidate public YouTube account URL resolves differently or stops being public/no-login visible.
```

## Retrieval Header

Header above is retrieval-only. This artifact is not validation, readiness, capture execution, registry mutation, metric refresh, Silver write, fuzzy duplicate detection, or cross-platform identity proof.

## Launch Variables

```yaml
scan_target: public fragrance creators/reviewers not already in the Creator Registry
platforms_in_scope:
  - youtube
geography_or_market_scope: English-language public creator accounts; no geography restriction
source_access_boundary: public/no-login only
run_cap:
  max_exact_queries: 8
  max_creator_candidate_rows: 10
  max_source_reads: 30
output_artifact_path: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
capture_request_policy: scan_may_emit_capture_requests
boundary: >
  Scan only. Do not run capture, mutate the registry, refresh metrics, or write
  Silver. Capture requests may be emitted as handoff rows only if the Creator
  Registry preflight receipt clears the row for new_capture.
```

## Source Context

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_creator_registry_live_scan
  edit_permission: docs-write for research artifact, candidate batch, receipt, and usage-note scope note
  target_scope:
    - docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    - docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json
    - docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
    - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  dirty_state_checked: yes
  source_context_status: SOURCE_CONTEXT_READY
```

Sources re-read before this scan: `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/artifact-roles.md`, `.agents/workflow-overlay/retrieval-metadata.md`, `.agents/workflow-overlay/validation-gates.md`, `.agents/workflow-overlay/decision-routing.md`, the cold creator discovery scan handoff prompt, the delegated review report, the Creator Registry match preflight usage note, the cold-agent rehearsal record, the match-preflight runner, the registry-match module, the current `creator_profile_current_view_v0.json`, the static Creator Signal projection, and the Source Capture Agent runbook boundary section.

`SOURCE_CONTEXT_READY`: declared for scan-only use. Capture execution remains outside this artifact.

## Registry Orientation

The current registry view reports:

```yaml
profiles_total: 33
platform_account_profiles: 33
creator_record_profiles: 0
cross_platform_rollup_profiles: 0
profiles_with_metric_rollups: 33
engagement_rate_observed_profiles: 31
profiles_with_ideal_audience_profiles: 0
youtube_platform_accounts_observed_by_direct_json_read: 30
```

The static projection is orientation only. The preflight receipt is the handoff evidence for new social creator/account capture requests.

## Scan Moves And Queries

Finalized evidence unit:

```yaml
exact_queries_used_for_finalized_unit: 0
source_reads_used_for_finalized_unit: 10
candidate_rows: 10
```

The finalized unit used direct public YouTube account URL reads after source context and registry orientation. Public YouTube pages exposed only title/footer-level text through the web reader, so this scan treats each source as account-existence and title-or-handle evidence only, not creator quality evidence.

Process residual: before stabilizing the final unit, the operator ran broader exploratory web searches that exceeded the owner-supplied exact-query cap. Those earlier searches are not used as evidence in the candidate rows below. This artifact is therefore a useful first live workflow rehearsal and preflight receipt, but not a cap-perfect discovery pass.

Final source reads:

| Move | URL | Source-visible account title or handle cue |
| --- | --- | --- |
| SR-001 | `https://www.youtube.com/@TheFragranceDecantBoutique` | The Fragrance Decant Boutique |
| SR-002 | `https://www.youtube.com/@BrooklynFragranceLover` | Brooklyn Fragrance Lover |
| SR-003 | `https://www.youtube.com/@ACSmellsGood` | AC Smells Good |
| SR-004 | `https://www.youtube.com/@robes08` | robes08 |
| SR-005 | `https://www.youtube.com/@CeeChroniclesTalkingScents` | CeeChronicles-Talking Scents |
| SR-006 | `https://www.youtube.com/@MrSmelly1977` | MrSmelly1977 |
| SR-007 | `https://www.youtube.com/@MyWorldofFragrance` | My World of Fragrance |
| SR-008 | `https://www.youtube.com/@DeliciousDelights` | Delicious Delights |
| SR-009 | `https://www.youtube.com/@MonaKattan` | Mona Kattan |
| SR-010 | `https://www.youtube.com/@TheNicheFragranceCollector` | The Niche Fragrance Collector |

## Candidate Batch

Candidate batch path: `docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json`.

All ten rows were submitted with `intended_action: new_capture` because the only downstream handoff contemplated by this scan is a possible new social creator/account capture request. That does not run capture.

## Creator Registry Match Preflight Receipt

Command run:

```powershell
python orca-harness\runners\run_creator_registry_match_preflight.py --candidates docs\research\creator_discovery_scan_fragrance_youtube_public_candidates_v0.json --output docs\research\creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json --generated-at-utc 2026-07-04T13:40:00Z
```

Observed exit code: `0`.

Receipt path: `docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json`.

Observed receipt summary:

```json
{"ambiguous_matches":0,"blocked_actions":0,"existing_matches":0,"invalid_candidates":0,"new_candidates":10,"safe_to_capture_new":10,"total_candidates":10}
```

## Existing Registry Matches

None by exact-match preflight.

## New Exact-Unmatched Candidates

| Candidate ID | Platform | Handle or URL | Preflight decision | Action status | Can start new capture | Matched registry profiles | Status | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fragrance_youtube_public_001_the_fragrance_decant_boutique` | youtube | `https://www.youtube.com/@TheFragranceDecantBoutique` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_002_brooklyn_fragrance_lover` | youtube | `https://www.youtube.com/@BrooklynFragranceLover` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_003_ac_smells_good` | youtube | `https://www.youtube.com/@ACSmellsGood` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_004_robes08` | youtube | `https://www.youtube.com/@robes08` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_005_cee_chronicles_talking_scents` | youtube | `https://www.youtube.com/@CeeChroniclesTalkingScents` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_006_mr_smelly_1977` | youtube | `https://www.youtube.com/@MrSmelly1977` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_007_my_world_of_fragrance` | youtube | `https://www.youtube.com/@MyWorldofFragrance` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_008_delicious_delights` | youtube | `https://www.youtube.com/@DeliciousDelights` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_009_mona_kattan` | youtube | `https://www.youtube.com/@MonaKattan` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |
| `fragrance_youtube_public_010_the_niche_fragrance_collector` | youtube | `https://www.youtube.com/@TheNicheFragranceCollector` | `new_candidate` | `allowed` | `true` | none | new_exact_unmatched | eligible_for_capture_request |

## Blocked Or Ambiguous Candidates

None by exact-match preflight.

## Capture Requests

These are handoff rows only. They do not execute capture, bind a route, mutate the registry, refresh metrics, or write Silver.

```yaml
capture_requests:
  - capture_request_id: capreq_fragrance_youtube_public_001
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_001_the_fragrance_decant_boutique]
    urls:
      - url: https://www.youtube.com/@TheFragranceDecantBoutique
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_002
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_002_brooklyn_fragrance_lover]
    urls:
      - url: https://www.youtube.com/@BrooklynFragranceLover
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_003
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_003_ac_smells_good]
    urls:
      - url: https://www.youtube.com/@ACSmellsGood
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_004
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_004_robes08]
    urls:
      - url: https://www.youtube.com/@robes08
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_005
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_005_cee_chronicles_talking_scents]
    urls:
      - url: https://www.youtube.com/@CeeChroniclesTalkingScents
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_006
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_006_mr_smelly_1977]
    urls:
      - url: https://www.youtube.com/@MrSmelly1977
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_007
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_007_my_world_of_fragrance]
    urls:
      - url: https://www.youtube.com/@MyWorldofFragrance
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_008
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_008_delicious_delights]
    urls:
      - url: https://www.youtube.com/@DeliciousDelights
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_009
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_009_mona_kattan]
    urls:
      - url: https://www.youtube.com/@MonaKattan
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
  - capture_request_id: capreq_fragrance_youtube_public_010
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    candidate_or_observation_ids: [fragrance_youtube_public_010_the_niche_fragrance_collector]
    urls:
      - url: https://www.youtube.com/@TheNicheFragranceCollector
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible title/handle cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight: {required_when: new_social_creator_account_capture, receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json, intended_action: new_capture, decision: new_candidate, action_status: allowed, can_start_new_capture: true}
    screening_evidence_summary: Screen-light account title/handle cue only; exact registry preflight found no existing match.
    uncertainty_or_access_limits: YouTube page text was title/footer-level in the web reader; account-content quality not established.
    not_requested: [route expansion, packet commitment by scanning, ECR, Cleaning, or Judgment work]
```

## Non-Claims And Residuals

- Exact-match only: the receipt does not prove fuzzy duplicate absence, cross-platform identity, or display-name uniqueness.
- Source adequacy not proven: title/handle visibility is enough for a first scan handoff row, not enough to claim quality, current activity, channel-wide influence, or commercial fit.
- Receipt provenance residual: until a later checker patch verifies receipt existence/content, `check_csb_scanning_artifact.py` only checks shape and self-consistency. This artifact preserves a real receipt path and cites the runner command, but the checker alone should not be described as proof of receipt authenticity.
- Process residual: the operator ran wider exploratory web searches before stabilizing this final unit, so this is not a clean cap-perfect discovery run.
- No capture, registry mutation, metric refresh, Silver write, ECR, Cleaning, Judgment, outreach, follower graph, comment scraping, channel dossier, or standing monitoring was performed.

## Validation

Validation to run at closeout:

```powershell
git diff --check
python .agents/hooks/check_retrieval_header.py --changed --strict
python .agents/hooks/header_index.py --strict --base origin/main
python .agents/hooks/check_handoff_pointers.py --strict --base origin/main
python .agents/hooks/check_dcp_receipt.py --strict --base origin/main
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict
python .agents/hooks/check_csb_scanning_artifact.py --changed --strict
```

Expected CSB checker posture: this artifact is a creator-discovery scan, not a CSB-first scan artifact; if the checker reports no changed CSB-first scan artifacts, that is a skip, not a pass over this artifact.

## Next Step

Use the ten preflight-cleared rows as candidate handoff input only if the next lane is explicitly authorized for Capture. Before any registry addition, Capture should preserve the public account page and confirm the account is actually a fragrance creator/reviewer rather than relying on title/handle cues alone.