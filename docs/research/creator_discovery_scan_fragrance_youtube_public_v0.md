# Fragrance YouTube Creator Discovery Scan v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  Bounded public/no-login YouTube scan for English-language fragrance
  creators/reviewers not already present in the Creator Registry, with exact
  Creator Registry match-preflight receipt preserved before any capture-request
  handoff rows.
use_when:
  - Checking the first live receipt-bearing Creator Registry cold discovery scan.
  - Reviewing fragrance YouTube creator candidates that cleared exact-match preflight for possible new_capture handoff.
  - Testing receipt-content verification against a real scan artifact and receipt pair.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md
  - docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json
  - docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
stale_if:
  - The Creator Registry profile-current view changes before these rows are handed to Capture.
  - Any candidate channel handle or canonical channel URL stops resolving publicly without login.
  - The Creator Registry match-preflight receipt fields or checker linkage contract changes.
```

## Launch Variables

```yaml
scan_target: "public fragrance creators/reviewers not already in the Creator Registry"
platforms_in_scope: ["youtube"]
geography_or_market_scope: "English-language public creator accounts; no geography restriction"
source_access_boundary: "public/no-login only"
run_cap:
  max_exact_queries: 8
  max_creator_candidate_rows: 10
  max_source_reads: 30
output_artifact_path: "docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md"
capture_request_policy: "scan_may_emit_capture_requests"
boundary: >
  Scan only. Do not run capture, mutate the registry, refresh metrics, or write
  Silver. Capture requests may be emitted as handoff rows only if the Creator
  Registry preflight receipt clears the row for new_capture.
```

## Source Context

`SOURCE_CONTEXT_READY`.

Project and lane sources reread before the scan:

- `AGENTS.md` and `.agents/workflow-overlay/README.md` for Orca/Forseti project authority.
- `docs/workflows/creator_registry_operational_next_steps_handoff_v0.md` from the active Creator Ledger/Registry worktree because the named packet is not present on this branch.
- `.agents/workflow-overlay/source-loading.md`, `artifact-roles.md`, `retrieval-metadata.md`, and `validation-gates.md` for research artifact shape and completion gates.
- `docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md` for launch shape and output sections.
- `forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` and `orca_demand_scan_core_spec_v0.md` for scan/capture boundaries.
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`, `orca-harness/runners/run_creator_registry_match_preflight.py`, and `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py` for the exact-match receipt contract.
- `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md` for expected mixed-batch and row-level preflight behavior.

The static multi-creator projection was treated as orientation only. Its visible snapshot says 33 profiles, while the current profile-current JSON below says 36 profiles, so current counts come from the JSON view and not from the static projection.

## Registry Orientation

Current registry view inspected:

- Path: `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_v0.json`
- `generated_at_utc`: `2026-07-03T09:04:50Z`
- `profiles_total`: 36
- `platform_account_profiles`: 36
- Platform split: 30 YouTube profiles, 3 Instagram profiles, and 3 TikTok
  profiles. The YouTube handle list below is the 30-profile YouTube subset; the
  full 36-profile registry view was still used by exact-match preflight.
- YouTube handles observed in the current registry before filtering:
  `BowTieFragranceGuy`, `ChaosFragrances`, `Cubaknow`, `CurlyFragrance`,
  `CurlyScents`, `DemiRawling`, `FragranceKnowledge`, `FragranceView`,
  `funmimonet`, `GentsScents`, `JeremyFragrance`, `JusDeRose`, `MilaLeBlanc`,
  `MonikaCioch`, `OliviaOlfactory`, `PostCologne`, `ProfessorPerfume`,
  `Redolessence`, `ScentedMoments`, `Scenteno`, `SchoolofScent`,
  `SimplyPutScents`, `SokiLondon`, `TheFragranceApprentice`, `ThePerfumeGuy`,
  `ThePerfumeNest`, `TheScented`, `TheScentinel`, `TiffBenson`, and
  `TLTGReviews`.

## Scan Moves And Queries

Exact public queries used: 4 of 8.

| Query | Result use |
| --- | --- |
| `fragrance reviewer` | Produced public YouTube channel handles including AROMATIX, Cal Cologne, Eau D' Erica, Erin Nicole TV, FBFragrances, FRAG-MENTAL, FragranceFlan, K&A Fragrances, and known registry rows filtered out. |
| `perfume reviewer` | Produced overlapping and additional public YouTube handles including AdrianneMG, Perfumerism, The Perfume Reviewer, and known registry rows filtered out. |
| `niche perfume review` | Produced additional niche-fragrance handles and known registry rows filtered out. |
| `fragrance reviews channel` | Produced additional handles including Aaron Terence Hughes and known registry rows filtered out. |

Public source reads used: 14 of 30.

- 4 public YouTube search-result pages.
- 10 public YouTube channel pages for capped candidate rows.

No login, browser session, comment scraping, follower graph read, transcript read, channel dossier, or capture tool was used.

## Candidate Batch

Candidate batch path:
`docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json`

Selection rule: keep up to 10 public YouTube channels whose public result/page metadata indicates fragrance, perfume, scent, or fragrance-review relevance and whose handle was not already in the current registry handle list above.

| Candidate ID | Public account | Public metadata basis | Source |
| --- | --- | --- | --- |
| `fragrance_youtube_scan_001_aaron_terence_hughes` | Aaron Terence Hughes / `@AaronTerenceHughes` | Channel metadata describes a fragrance review channel. | `https://www.youtube.com/@AaronTerenceHughes` |
| `fragrance_youtube_scan_002_aromatix` | AROMATIX / `@aromatixrrt` | Public channel result appeared for fragrance-review query; metadata describes reviews and feedback. | `https://www.youtube.com/@aromatixrrt` |
| `fragrance_youtube_scan_003_cal_cologne` | Cal Cologne / `@CalCologne` | Channel metadata describes fragrance collecting and fragrance content. | `https://www.youtube.com/@CalCologne` |
| `fragrance_youtube_scan_004_eau_d_erica` | Eau D' Erica / `@eauderica` | Public channel result appeared in fragrance-review query set; channel page resolved publicly. | `https://www.youtube.com/@eauderica` |
| `fragrance_youtube_scan_005_erin_nicole_tv` | Erin Nicole TV / `@ErinNicoleTV` | Channel metadata includes luxury beauty, fragrance, and lifestyle. | `https://www.youtube.com/@ErinNicoleTV` |
| `fragrance_youtube_scan_006_fbfragrances` | FBFragrances / `@FBFragrances` | Channel metadata describes helping men smell better through fragrance knowledge and advice. | `https://www.youtube.com/@FBFragrances` |
| `fragrance_youtube_scan_007_fragmental` | FRAG-MENTAL / `@FRAGMENTAL` | Channel metadata describes a fragrance journey. | `https://www.youtube.com/@FRAGMENTAL` |
| `fragrance_youtube_scan_008_fragrance_flan` | FragranceFlan / `@FragranceFlan` | Channel metadata describes all things fragrance. | `https://www.youtube.com/@FragranceFlan` |
| `fragrance_youtube_scan_009_ka_fragrances` | K&A Fragrances / `@KAFragrances` | Public channel result appeared for fragrance-review queries; channel name and metadata are fragrance-oriented. | `https://www.youtube.com/@KAFragrances` |
| `fragrance_youtube_scan_010_the_perfume_reviewer` | The Perfume Reviewer / `@theperfumereviewr` | Channel metadata describes perfume reviews. | `https://www.youtube.com/@theperfumereviewr` |

## Creator Registry Match Preflight Receipt

Preflight command:

```powershell
python orca-harness\runners\run_creator_registry_match_preflight.py `
  --candidates docs\research\creator_discovery_scan_fragrance_youtube_public_candidates_v0.json `
  --registry forseti\product\spines\capture\core\source_families\social_media\creator_registry\creator_profile_current_view_v0.json `
  --output docs\research\creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json `
  --generated-at-utc 2026-07-04T18:30:00Z
```

Observed exit code: `0`.

Receipt path:
`docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json`

Receipt summary:

```json
{
  "ambiguous_matches": 0,
  "blocked_actions": 0,
  "existing_matches": 0,
  "invalid_candidates": 0,
  "new_candidates": 10,
  "safe_to_capture_new": 10,
  "total_candidates": 10
}
```

## Existing Registry Matches

None. The receipt has `existing_matches: 0`, and every candidate row has an empty `matched_registry_profiles` list.

## New Exact-Unmatched Candidates

All 10 candidate rows cleared exact-match preflight row-by-row for `intended_action: new_capture`.

| Candidate ID | Decision | Action status | `can_start_new_capture` |
| --- | --- | --- | --- |
| `fragrance_youtube_scan_001_aaron_terence_hughes` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_002_aromatix` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_003_cal_cologne` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_004_eau_d_erica` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_005_erin_nicole_tv` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_006_fbfragrances` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_007_fragmental` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_008_fragrance_flan` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_009_ka_fragrances` | `new_candidate` | `allowed` | `true` |
| `fragrance_youtube_scan_010_the_perfume_reviewer` | `new_candidate` | `allowed` | `true` |

## Blocked Or Ambiguous Candidates

None in this capped batch.

## Capture Requests

These are handoff rows only. No capture was run.

```yaml
capture_requests:
  - capture_request_id: fragrance_youtube_scan_001_aaron_terence_hughes
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@AaronTerenceHughes
    display_name: Aaron Terence Hughes
    candidate_or_observation_ids:
      - fragrance_youtube_scan_001_aaron_terence_hughes
    urls:
      - url: https://www.youtube.com/@AaronTerenceHughes
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_001_aaron_terence_hughes
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_002_aromatix
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@aromatixrrt
    display_name: AROMATIX
    candidate_or_observation_ids:
      - fragrance_youtube_scan_002_aromatix
    urls:
      - url: https://www.youtube.com/@aromatixrrt
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_002_aromatix
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_003_cal_cologne
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@CalCologne
    display_name: Cal Cologne
    candidate_or_observation_ids:
      - fragrance_youtube_scan_003_cal_cologne
    urls:
      - url: https://www.youtube.com/@CalCologne
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_003_cal_cologne
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_004_eau_d_erica
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@eauderica
    display_name: "Eau D' Erica"
    candidate_or_observation_ids:
      - fragrance_youtube_scan_004_eau_d_erica
    urls:
      - url: https://www.youtube.com/@eauderica
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_004_eau_d_erica
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_005_erin_nicole_tv
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@ErinNicoleTV
    display_name: Erin Nicole TV
    candidate_or_observation_ids:
      - fragrance_youtube_scan_005_erin_nicole_tv
    urls:
      - url: https://www.youtube.com/@ErinNicoleTV
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_005_erin_nicole_tv
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_006_fbfragrances
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@FBFragrances
    display_name: FBFragrances
    candidate_or_observation_ids:
      - fragrance_youtube_scan_006_fbfragrances
    urls:
      - url: https://www.youtube.com/@FBFragrances
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_006_fbfragrances
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_007_fragmental
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@FRAGMENTAL
    display_name: FRAG-MENTAL
    candidate_or_observation_ids:
      - fragrance_youtube_scan_007_fragmental
    urls:
      - url: https://www.youtube.com/@FRAGMENTAL
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_007_fragmental
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_008_fragrance_flan
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@FragranceFlan
    display_name: FragranceFlan
    candidate_or_observation_ids:
      - fragrance_youtube_scan_008_fragrance_flan
    urls:
      - url: https://www.youtube.com/@FragranceFlan
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_008_fragrance_flan
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_009_ka_fragrances
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@KAFragrances
    display_name: "K&A Fragrances"
    candidate_or_observation_ids:
      - fragrance_youtube_scan_009_ka_fragrances
    urls:
      - url: https://www.youtube.com/@KAFragrances
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_009_ka_fragrances
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
  - capture_request_id: fragrance_youtube_scan_010_the_perfume_reviewer
    source_scan: docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md
    platform: youtube
    public_profile_url: https://www.youtube.com/@theperfumereviewr
    display_name: The Perfume Reviewer
    candidate_or_observation_ids:
      - fragrance_youtube_scan_010_the_perfume_reviewer
    urls:
      - url: https://www.youtube.com/@theperfumereviewr
        venue: youtube_public_account
        observation_supported: public fragrance-account candidate from source-visible metadata
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm whether it is a creator/reviewer account worth adding to the Creator Registry.
    decision_window: current public/no-login account state as of 2026-07-04
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json
      candidate_id: fragrance_youtube_scan_010_the_perfume_reviewer
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: Screen-light public YouTube account metadata indicates fragrance or perfume-review relevance; exact registry preflight found no existing match.
    uncertainty_or_access_limits: Public/no-login channel page and search-result metadata only; account-content quality, activity, and creator fit were not established.
    not_requested: [capture execution, route expansion, registry mutation, metric refresh, Silver write, ECR, Cleaning, or Judgment work]
```

## Non-Claims And Residuals

Non-claims:

- Not capture execution.
- Not Creator Registry mutation.
- Not Silver write, metric refresh, ECR, cleaning, or Judgment work.
- Not fuzzy identity proof.
- Not cross-platform person identity proof.
- Not buyer proof, audience-fit proof, creator-quality ranking, or outreach authorization.
- Not channel-wide influence measurement.
- Not source adequacy proof beyond this capped public/no-login scan.

Accepted residuals:

- Exact preflight can miss fuzzy duplicates, renamed channels, or cross-platform same-person relationships.
- English-language posture is inferred from public result/channel metadata only; no video transcript or comment read was performed.
- Source quality is scan-grade only. Capture must reacquire under its own provenance rules before using any candidate.
- The static projection was stale for current counts and used only as a warning/orientation surface.
- Capture-request rows are allowed to be emitted because the receipt clears them row-by-row, but they remain requests and do not authorize capture by themselves.

## Validation

- Exact public queries used: 4 of 8.
- Candidate rows emitted: 10 of 10.
- Public source reads used: 14 of 30.
- Candidate batch written: `docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json`.
- Preflight receipt written: `docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json`.
- Preflight command exit code: `0`.
- Receipt schema: `creator_registry_match_preflight_receipt_v0`.
- Receipt summary: 10 total candidates, 10 `new_candidate`, 10 `safe_to_capture_new`, 0 existing, 0 ambiguous, 0 invalid, 0 blocked.

## Next Step

Use this artifact and receipt pair to verify the receipt-content checker against one real scan artifact. If the checker passes, the next material MGT step is owner adjudication on whether any of these handoff rows should enter a capture lane. Do not run capture from this scan artifact alone.
