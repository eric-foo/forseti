# Creator Profile Current Validator — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: same-model adversarial code review output
scope: Review findings for creator_profile_current reusable validator hardening.
use_when:
  - Adjudicating PR 439 creator profile validator review findings.
  - Auditing accepted or deferred validator hardening findings for creator-profile current view.
authority_boundary: retrieval_only
```
```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/creator_profile_current_validator_adversarial_code_review_v0.md
  recommendation: patch_before_merge
  reviewed_by: claude-opus-4-8
  authored_by: unrecorded
  de_correlation_bar: self_fallback
  same_vendor_rationale: "In-session same-model (home) review, not a de-correlated delegate; provides bounded verification only, NOT cross-vendor discovery / no-new-seam assurance. authored_by unknown, so same-vs-cross family is an unmeasured gap."
  summary: "The validator soundly guards the headline metric-posture, sample-support, identity-boundary, and cross-platform-linkage surfaces (confirmed by tests + an in-memory probe), but four required-but-unvalidated profile substructures accept arbitrary content — a confirmed false-pass for metric/audience smuggling and provenance drift that the smuggling test does not cover."
  findings_count: 4
  blocking_findings: ["CPV-01"]
  advisory_findings: ["CPV-02", "CPV-03", "CPV-04"]
  prior_findings_remediated: []
  next_action: "Chief Architect: decide CPV-01 — either patch the four required-but-unvalidated profile substructures (reject unknown keys + reconcile source_drill_back observation ids) before relying on validate_creator_profile_current_view as a creator-profile safety gate, or record CPV-01 as an explicit accepted v0 residual. CPV-02..04 are advisory."
```

> **`blocking_findings` is a reviewer recommendation, decision input only.** Severity
> labels (`critical`/`major`/`minor`) are for finding priority; per
> `.agents/workflow-overlay/review-lanes.md` they do not by themselves create
> approval, rejection, readiness, or mandatory remediation. The Chief Architect may
> close CPV-01 by patch OR by recording it as an accepted v0 residual.

## Commission

- **Target:** the validator commit that added `capture_spine.creator_profile_current`, pinned to `da2987c6a3891064a9ba82b152a3b5025f54be52` (`da2987c6^..da2987c6`), three files: `creator_profile_current/__init__.py`, `creator_profile_current/validation.py`, `tests/unit/test_creator_profile_current_static_view.py`.
- **Purpose:** read-only adversarial code review — does the code + tests protect the current creator-profile aggregate view from misleading identity/metric claims, without overclaiming validation, dashboard/SQLite readiness, or Silver-lake derivation?
- **Authority / lane:** read-only implementation/code review (`workflow-code-review` strict mode, lane bound by `.agents/workflow-overlay/review-lanes.md` + this prompt). No patch authority; no `patch_queue_entry`.
- **Routing note:** routed from a `workflow-delegated-review-patch` invocation but the target is a multi-file code diff, so this is an adversarial **code** review, not patch execution.

## Source-State Note (read first)

The bound worktree (`codex/creator-metric-source-audit`) was **clean** but its **HEAD was `aea5f459`, one commit ahead of the bound `da2987c6`**. That one commit (`aea5f459 "docs: add creator profile validator review prompt"`) adds **only** the 192-line review-prompt doc and touches nothing in `orca-harness/` or `orca/product/` (verified: `git show --name-only aea5f459` ∩ `orca-harness|orca/product` = ∅; `da2987c6..HEAD` diff of the three target files is empty). `da2987c6` is an ancestor of HEAD.

Because the Target Sources pin the review diff to the **explicit immutable SHA** `da2987c6^..da2987c6`, and the only divergence is the prompt commit itself, this review was run against the exact bound bytes — no substitute source pack. A hard `BLOCKED_WRONG_SOURCE_STATE` was judged to be no-value ceremony here (it would force resetting HEAD or re-pinning to review byte-identical code). This nuance is surfaced rather than silently absorbed; if the owner intended a strict HEAD==SHA gate, re-pin and re-run.

## Method / Provenance Posture

- Methods loaded under the Source-Gated Method Contract: `AGENTS.md`, overlay README, `source-loading.md`, `prompt-orchestration.md`, `review-lanes.md` read; `workflow-deep-thinking` and `workflow-code-review` `REFERENCE-LOAD`ed, then `APPLY`ed only after `SOURCE_CONTEXT_READY`.
- **This is a same-model in-session review (`self_fallback`).** It is bounded verification, not a cross-vendor de-correlated discovery pass; the no-new-seam standard is not claimed.

---

## Findings (findings-first)

### CPV-01 — Required-but-unvalidated profile substructures accept arbitrary content (confirmed false-pass) — `major`

- **Reviewed target / role:** `validate_creator_profile_current_view` structural gate.
- **Location:**
  - `_ALLOWED_PROFILE_KEYS` lists `identity_evidence_summary`, `current_metric_rollups`, `ideal_audience_profile`, `wind_calling_summary`, `source_drill_back` — `orca-harness/capture_spine/creator_profile_current/validation.py:44`.
  - `_validate_profiles` requires **all** profile keys present (`validation.py:217`) but only dispatches validators for `identity_boundary`, `platform_accounts`, `non_claims`, `limitations`, `current_metric_rollups`, `freshness` (`validation.py:226`). **No validator is called for `identity_evidence_summary`, `source_drill_back`, `ideal_audience_profile`, or `wind_calling_summary`.** `ideal_audience_profile` is touched only by the `is not None` count (`validation.py:424`).
  - The shared forbidden-field scan (`validation.py:154` → `creator_public_handle_linkage/validation.py:235`) catches forbidden field **names** + value patterns, but its `_FORBIDDEN_OUTPUT_FIELDS` set (`creator_public_handle_linkage/validation.py:117`) **excludes metric names** like `subscriber_count`, `like_count`, `comment_count`, `view_count`, `average_views`, `engagement_rate`. Those names are only in the YouTube-specific set (`youtube_creator_observation/validation.py:110`), which is **not applied** by this validator.
  - False-confidence test: `test_creator_profile_validator_rejects_metric_smuggling_into_identity_account` mutates only the **allowlisted** `platform_accounts` node (`tests/unit/test_creator_profile_current_static_view.py:229`).
- **Evidence (in-memory probe, observed):** with the real fixture as baseline (accepted), the validator **ACCEPTED** every one of these mutations:
  - `subscriber_count: 1_000_000` + `average_views: 999_999` injected into `source_drill_back`;
  - `engagement_rate: 0.42` injected into `identity_evidence_summary`;
  - `ideal_audience_profile` replaced with an arbitrary object `{"freeform": ..., "like_count": 5}` (with the count bumped to match);
  - `source_drill_back.source_metric_observation_ids` replaced with `["unrelated_observation_id"]` (provenance drift).
  Controls confirm the guards that DO exist: the same smuggle into `platform_accounts[0]` → rejected `unknown_field`; zero-filling a non-observed metric → rejected `metric_value_for_non_observed_posture`.
- **Why it matters (creator-profile aggregate safety):** the validator's purpose is to stop misleading identity/metric claims. The headline `current_metric_rollups` surface is well guarded, but raw audience/engagement numbers and drifted provenance can ride inside the four auxiliary nodes undetected — exactly the "metric posture leakage" and "source-backedness leakage" axes — and the test suite's smuggling test gives false assurance because it only exercises an allowlisted node. Latent (the current 30-profile fixture is internally clean), but a generator bug, hand-edit, or future field addition would pass.
- **minimum_closure_condition:** the four required substructures are no longer free-form: each is either `_reject_unknown_keys`-allowlisted and shape-validated, or explicitly typed (e.g., `ideal_audience_profile` must be `None` in v0; `wind_calling_summary` must be `None`/typed); and a negative test covers smuggling into at least one previously-unguarded node. (Alternatively: CPV-01 is recorded as an explicit accepted v0 residual naming these nodes as un-gated.)
- **next_authorized_action:** Chief Architect decision (patch vs recorded residual). This review lane may not edit or patch.

### CPV-02 — Reusable validator enforces a narrower non-claim set than the fixture test (SQLite / cross-platform / channel-wide / engagement non-claims are test-only) — `minor`

- **Location:** `_REQUIRED_NON_CLAIM_FRAGMENTS` = `buyer proof`, `public person-level identity`, `contact or outreach authorization`, `dashboard readiness` (`validation.py:128`), enforced at `validation.py:452`. The fixture test additionally asserts `channel-wide creator influence`, `engagement rate`, `cross-platform rollup`, and `not SQLite or data-lake physicalization` (`tests/unit/test_creator_profile_current_static_view.py:190`) — **none of which the validator requires.**
- **Why it matters:** the commission explicitly cares about not overclaiming **SQLite readiness** and **cross-platform** rollups. A non-fixture caller of `validate_creator_profile_current_view` would accept a view that omits the `not SQLite or data-lake physicalization`, `not cross-platform rollup`, `not channel-wide creator influence`, and `not engagement rate` non-claims; that protection lives only in the fixture-specific test, not in the reusable gate.
- **minimum_closure_condition:** the reusable validator's required-non-claim set covers the postures the commission requires not be overclaimed (at minimum the SQLite/data-lake and cross-platform non-claims), or the asymmetry is documented as intentional (validator = structural floor; fixture test = full posture set).
- **next_authorized_action:** Chief Architect decision; advisory.

### CPV-03 — Validator binds metric *posture/structure* but not metric *magnitude/derivation*; numeric source-backedness is test-only — `minor`

- **Location:** `_validate_metric_values` checks posture/shape only (`validation.py:327`); an `observed` metric just needs `isinstance(value, (int, float))` (`validation.py:341`) — which **also accepts `bool`** (`isinstance(True, int) is True`; probe confirmed `average_views: True` accepted). No magnitude/sign/sanity check and no source cross-check exist in the validator. Numeric derivation from the seed is enforced only by `test_creator_profile_current_rebuilds_from_identity_and_metric_seed` (`tests/unit/...:130`) and `source_inputs` content-hash freshness only by `test_creator_profile_current_source_hashes_are_current` (`...:170`) — neither is reachable from `validate_/load_`. The sibling YouTube validator, by contrast, ships a reusable `validate_source_rebuild` + hash recompute (`youtube_creator_observation/validation.py:187`, `:427`); this validator ships no equivalent.
- **Why it matters:** a standalone caller of `load_creator_profile_current_view` gets structural + posture protection, **not** "source-backed metrics." A structurally-valid but numerically-fabricated `average_views` (or a `bool` smuggled as numeric) passes the validator; only the fixture-bound rebuild test catches magnitude drift. The validator must not be presented as a source-backedness guarantee.
- **minimum_closure_condition:** either the validator gains a reusable source-rebuild/hash check (parity with the sibling) **or** the validator's structural-only scope is stated so acceptance does not read `validate_*` as proof of source-backed magnitudes; and `observed` numeric values explicitly exclude `bool`.
- **next_authorized_action:** Chief Architect decision; advisory.

### CPV-04 — Brittle exact-substring matching for required caveats/non-claims (false-fail + weak guarantee) — `minor`

- **Location:** `_validate_rollup_limitations` requires the literal substrings `"not a representative creator average"` and `"selection can bias view averages"` (`validation.py:387`); `_validate_profile_non_claims` requires literal fragments (`validation.py:452`).
- **Why it matters:** this is the "false fail: overfits today's fixture" axis. A valid future view that phrases the same caveat differently (e.g., "not representative of the creator's average") is rejected; conversely a substring match is satisfied even when embedded inside misleading prose, so it is a weak guarantee in both directions.
- **minimum_closure_condition:** required caveats/non-claims are matched by a stable key/enum or a documented canonical-phrase contract rather than free-text substring search, or the brittleness is accepted as a v0 fixture-coupling residual.
- **next_authorized_action:** Chief Architect decision; advisory.

---

## Non-Findings (scary-looking risks already covered)

- **Import / package risk:** `pyproject.toml:37` includes `capture_spine.*`, which covers the new `capture_spine.creator_profile_current` subpackage; the commit adds a real `__init__.py`; the focused suite imports and runs (`13 passed`). Not importable-broken.
- **Metric zero-fill on the headline rollup surface:** guarded — non-observed metrics must have null value + a reason (`validation.py:345`); probe control rejected a zero-fill (`metric_value_for_non_observed_posture`).
- **Cross-platform rollup without promoted linkage:** guarded — `cross_platform` scope requires a `creator_record` profile in a promoted link state (`validation.py:317`); probe control rejected the single-platform case.
- **Identity boundary:** `platform_account` vs `creator_record` subject-id/linkage mirroring and the `single_platform_observed` link/review-state prohibition are enforced (`validation.py:236`).
- **Sample-support honesty:** `sample_adequacy`, `surface_handling`, and `representativeness_posture` are derived-checked from `observation_count` and a hardcoded non-representative posture (`validation.py:368`), so thin pools cannot be labeled "stronger" or "representative."
- **Counts cross-check + ordering:** the 7 derived counts are recomputed and compared (`validation.py:403`); profiles (and therefore every rollup's `engagement_rate.posture`) are validated before counts read them (`validation.py:187`), so no `KeyError`. *Coverage note:* there is no negative test mutating a count — the logic is present and correct but untested for the mismatch path.
- **`observation_count` ↔ `source_metric_observation_ids` tie:** enforced (`validation.py:364`), preventing observation-id list/length drift inside a rollup. (Distinct from CPV-01's `source_drill_back` id drift, which is the *unvalidated* copy.)

## Validation Evidence

Reran in the bound worktree (`PYTHONPATH=orca-harness`, observed Python 3.11.15):

```text
python -m pytest orca-harness/tests/unit/test_creator_profile_current_static_view.py \
                 orca-harness/tests/unit/test_youtube_creator_metric_seed.py -q
  -> 13 passed (exit 0)   # matches commissioning-lane evidence
```

In-memory adversarial probe (scratchpad only; no repo file written), `validate_creator_profile_current_view`:

```text
[OK]         baseline real 30-profile fixture: accepted        (no false-fail)
[FALSE-PASS] subscriber_count+average_views in source_drill_back: ACCEPTED
[FALSE-PASS] engagement_rate number in identity_evidence_summary: ACCEPTED
[FALSE-PASS] arbitrary ideal_audience_profile object (count bumped): ACCEPTED
[FALSE-PASS] source_drill_back observation-id drift vs rollup: ACCEPTED
[FALSE-PASS] observed average_views value = True (bool-as-numeric): ACCEPTED
[guard-ok]   metric smuggled into allowlisted platform_accounts[0]: rejected unknown_field
[guard-ok]   zero-fill engagement_rate (non-observed): rejected metric_value_for_non_observed_posture
[guard-ok]   cross_platform scope on single-platform profile: rejected cross_platform_rollup_without_promoted_linkage
```

Not rerun (relied on commissioning-lane evidence): `git diff --check` (reported exit 0, CRLF warnings only), `check_retrieval_header.py --changed --strict` (exit 0), `check_map_links.py --strict` (exit 0), `check_placement.py --check` (exit 0, legacy-tolerated). These gate header/placement hygiene, not validator correctness, and are out of this review's decision path.

## Review-Use Boundary

These findings are decision input only. They are **not** approval, validation, readiness, merge safety, mandatory remediation, or patch authority until the Chief Architect separately accepts or authorizes action. This review makes no SQLite, dashboard, capture-lane, or Silver-lake recommendation, and asserts no dashboard/SQLite/Silver-lake readiness. The review was a same-model in-session pass (`self_fallback`): bounded verification, not cross-vendor discovery.
```
