# Adversarial Artifact Review + Adjudication — Data Lake Consumption Seam Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned no_repo cross-vendor adversarial artifact
  review of core_spine_v0_data_lake_consumption_seam_contract_v0.md and the
  home-CA review-return adjudication that closed it: reviewer identity and
  de-correlation bar, the seven findings, per-finding accept/modify decisions,
  the amendments applied, and the bounded same-vendor post-patch recheck
  disposition.
use_when:
  - Checking what the seam-contract review found and what the CA kept, modified, or rejected.
  - Verifying the de-correlation provenance behind the seam contract's adjudicated amendment pass.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5.5 Pro (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: no_repo (advisory findings only; CA applied amendments)
  dispatch: docs/prompts/wrappers/data_lake_consumption_seam_contract_norepo_adversarial_artifact_review_wrapper_v0.md
  bundle: docs/review-inputs/data_lake_consumption_seam_contract_norepo_adversarial_artifact_review_bundle_v0/
  target_hash_at_review: C3D5A74B74273982C7E0192BB52504B0754E4F92DBF641DD39332B2B18D6C159 (commit a7812c4d)
  reviewer_recommendation: AMEND_BEFORE_KEEP
  findings: 6 major + 1 minor
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, formal
  lane verdict, acceptance, or view-build authorization. Closure of findings is
  bounded by the same-vendor mechanical-tier recheck recorded below.
```

## Reviewer summary (verbatim substance)

`review_summary.status: review_complete`; recommendation `AMEND_BEFORE_KEEP:
resolve ack correction identity, namespace-history semantics, mandatory
reconcile, obligation/evidence sufficiency, and view/metric disclosure gaps.`
Reviewer confirmed both bundle hashes matched their pins and stated the
formal-tooling boundary (advisory critique, not a formal verdict). Read-budget
audit: wrapper, README, and target read in full; repository/code/tests skipped
as unverifiable in no_repo mode.

## Adjudication (per finding: claim → decision → applied change)

1. **Ack corrections unrepresentable for same-fingerprint obligations (major)
   — ACCEPTED.** Real contract gap: the deterministic `ack_<fp>` id plus
   "corrections = new fingerprint" left wrong-evidence acks uncorrectable.
   Applied: append-only retraction fact class
   (`acknowledgement_retraction` at `unack_<fp>_<k>`, mandatory reason;
   re-ack at `ack_<fp>_<k>`; acknowledged ⇔ ack facts > retraction facts) in
   the contract, the helper (`retract_ack`, `find_retractions`, counted
   `is_acknowledged`), and conformance obligation 7 with tests.
2. **Registry evolution vs historical acks (major) — ACCEPTED-MODIFIED.** The
   failure shape in code is loud (an unregistered active namespace raises),
   not the silent invalidation the finding projected — but the contract was
   silent on history. Applied: namespace rule rescoped to write/active-consumer
   admissibility; historical acks remain valid history across registry
   evolution; rename/retire = deliberate migration with a stated
   completion-history disposition. Doc amendment only; no code change needed.
3. **Optional reconcile contradiction (major) — ACCEPTED.** Genuine internal
   inconsistency ("Always reconcile" vs "may run best-effort"). Applied:
   empty pickup is a no-work claim valid only over a reconciled surface;
   helper `pickup` now reconciles by default (fail-loud) with a visible
   opt-out; the transcript runner opts out visibly and reconciles itself
   (best-effort, daemon isolation preserved); conformance test proves the
   stale-surface miss under opt-out and the default recovery.
4. **Obligation fingerprints too lane-defined (major) — ACCEPTED-MODIFIED.**
   Full input enumeration stays lane-owned by design (rejecting the implied
   central enumeration), but a checkable minimum envelope is right. Applied:
   `obligation_schema` + non-empty `consumer` + policy tokens required;
   helper-validated on every write and pickup decision; lane tests own the
   input-family pinning.
5. **Evidence semantics unbound (major) — ACCEPTED-MODIFIED.** Deep
   sufficiency stays lane-owned, but shape is now bound: non-empty list of
   mappings each with non-empty `kind` plus a dereferenceable ref or explicit
   basis; helper-validated; empty/shapeless evidence never acks.
6. **`undone` view conceals grown-obligation backlog (major) —
   ACCEPTED-MODIFIED.** The weaker semantics stay (accepted residual stands;
   fingerprint-aware views need lane-side obligation functions the lake must
   not host), but zero rows are now unmistakable: `zero_rows_meaning` field +
   per-namespace `anchors_with_acks` counts in the view body.
7. **Metric posture/coverage fields unbound (minor) — ACCEPTED.** Applied: a
   field-level posture/reason/coverage gate — a named family may not get a
   view until its owning decision binds those fields. Attached to the
   owner-named first families.

Nothing was rejected outright; findings 2, 4, 5, 6 were kept with modified
remedies (the reviewer's minimum_closure_conditions are met; the advisory
remediation directions were adapted to lake-boundary constraints).

## Owner metric-family naming (same return, second item)

The owner couriered the cross-vendor decision input (GPT-5.5 Pro ranking) and
directed processing: first families named in the contract as
`source_backed_brand_line_share_of_voice` and `movement_threshold_crossings`,
view-build-blocked behind the finding-7 gate. Naming is selection only.

## Post-patch recheck (required before keep, no_repo loop)

Bounded same-vendor, mechanical-tier recheck (who-constraint per
`.agents/workflow-overlay/delegated-review-patch.md`): closure-of-findings plus
new blocker/major in the touched delta only.

```yaml
post_patch_recheck:
  status: closure_gaps_found_then_closed
  recheck_model_tier: same-vendor mechanical tier (Anthropic Sonnet worker lane)
  scope: amended contract sections + consumption.py/derived_retrieval_views.py delta + new tests
  returned: >
    F1/F3/F4/F5/F7 closed (per-finding closure conditions verified against
    contract wording, code, and tests; double retract/re-ack cycle manually
    verified collision-free). Two gaps: (F2) the per-anchor history readers
    (find_acks/find_retractions) still hard-gated on current LANE_ROLES,
    contradicting the contract's history-stability promise, with no
    registry-evolution test; (F6) the new zero_rows_meaning /
    anchors_with_acks disclosure fields untested. No new blocker/major in the
    touched delta.
  ca_gap_closure: >
    Same turn: history readers deliberately ungated (active writer/consumer
    paths keep the loud gate) with a registry-evolution test
    (test_history_survives_registry_evolution) pinning history readability +
    loud active-path failure; disclosure-field assertions added to
    test_rebuild_builds_views_and_manifests. Affected suites re-run green.
```

## Validation evidence

Affected suites after amendments: 67 passed (consumption conformance, indexes
rebuild, rebuild proof, transcript runner, caption runner, seam-coverage
contract, silver-lane guard). Full-suite result recorded on the lane branch at
closeout. Not validation/readiness claims — test evidence on the implementing
branch only.
