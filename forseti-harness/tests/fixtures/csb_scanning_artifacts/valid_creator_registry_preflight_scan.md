<!-- fixture_expected: pass -->
# Creator Registry Preflight Receipt Pass Fixture

```yaml
capture_requests:
  - capture_request_id: capreq_fixture_creator_registry_ok
    source_scan: forseti-harness/tests/fixtures/csb_scanning_artifacts/valid_creator_registry_preflight_scan.md
    candidate_or_observation_ids: [fixture_creator_ok]
    urls:
      - url: https://www.youtube.com/@FixtureCreator
        venue: youtube_public_account
        observation_supported: fixture account cue
        gate_role: influence
    what_capture_should_verify: Preserve the public account page and confirm creator status.
    decision_window: fixture
    route_binding_state: unknown
    creator_registry_match_preflight:
      required_when: new_social_creator_account_capture
      receipt_path: forseti-harness/tests/fixtures/csb_scanning_artifacts/valid_creator_registry_preflight_receipt.json
      intended_action: new_capture
      decision: new_candidate
      action_status: allowed
      can_start_new_capture: true
    screening_evidence_summary: fixture only
    uncertainty_or_access_limits: fixture only
    not_requested: [route_expansion, packet_commitment_by_scanning, ecr_cleaning_or_judgment_work]
```
