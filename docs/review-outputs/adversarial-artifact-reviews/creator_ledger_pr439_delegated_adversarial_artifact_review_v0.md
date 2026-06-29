# Creator Ledger PR439 Delegated Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: adversarial_artifact_review_output
scope: >
  De-correlated (cross-vendor) read-only adversarial artifact review of PR #439
  (creator metric source audit): the source-backed YouTube view_count metric
  seed, the static creator_profile_current export, the spec/surface contract
  edits, and the two rederivation test files. Decision input for CA
  adjudication only; not approval, validation, readiness, or patch authority.
use_when:
  - Adjudicating whether PR #439 is safe to treat as the current creator-ledger/profile base.
  - Checking which creator-metric failure modes were attacked and which held.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_prompt_v0.md
  - orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
stale_if:
  - The review target commit changes from 23dce2d4ede2418fb3e73e325b045dc61b5fa03b.
  - Any PR #439 target artifact changes after 23dce2d4ede2418fb3e73e325b045dc61b5fa03b.
  - A later capture route adds source-backed like_count, total comment_count, subscriber_count, or engagement_rate rows.
```

## Review Summary (courier)

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: claude-opus-4.8
  authored_by: openai-gpt-family-codex (exact version unrecorded)
  de_correlation_bar: cross_vendor_discovery
  summary: >
    PR #439's source-backedness, missingness discipline, identity/cross-platform
    boundaries, and claim non-claims hold under attack and are confirmed by 8/8
    passing rederivation tests; the one material gap is an unnamed
    representativeness residual (n=1..3 account averages presented with uniform
    posture "observed", plus unnamed within-pool selection bias).
  findings_count: 2
  blocking_findings: []
  advisory_findings:
    - AR-01: average_views/median_views representativeness residual is unnamed (small per-account n incl. n=1; within-pool admission selection bias); posture uniformly "observed"
    - AR-02: per-observation drill-back uses non-portable absolute machine-local lake paths
  prior_findings_remediated: []
  next_action: >
    CA adjudicates AR-01 (name the representativeness residual in
    accepted_residuals/limitations and/or carry a per-rollup sample-adequacy
    signal; decide whether the Creator Signal surface needs a thin-sample
    withhold rule) before this seed is built on as the influence base.
```

## Provenance And De-correlation

- `reviewed_by`: claude-opus-4.8 (Anthropic / Claude vendor family).
- `authored_by`: openai-gpt-family-codex; exact runtime version unrecorded (not supplied; not fabricated).
- `de_correlation_bar`: `cross_vendor_discovery` — the reviewer vendor (Anthropic/Claude) differs from the author vendor (OpenAI/GPT-family Codex), satisfying the discovery bar in `.agents/workflow-overlay/delegated-review-patch.md` and the two-bar rule in `.agents/workflow-overlay/review-lanes.md`. This is a who-constraint record only, not a runtime-model recommendation.
- Access posture: read-only over the existing PR branch. No artifact under review was edited; no `patch_queue_entry` is emitted (PR #439 is a multi-file artifact set, which the convention routes to read-only review, not single-target delegated patch).

## Commission, Target, Authority, Decision Criteria

- **Commission.** Owner instruction to run a de-correlated delegated review for PR #439, executed as adversarial artifact review per `docs/prompts/reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_prompt_v0.md`. Decision asked: is PR #439 safe for the CA to adjudicate as the current creator-ledger/profile base?
- **Target (pinned).** Branch `codex/creator-metric-source-audit` at commit `23dce2d4ede2418fb3e73e325b045dc61b5fa03b`; base `codex/channel-neutral-creator-identity-architecture-prompt-pr412` at `824852fceca6c80ad410bf6fea002e51bd36a05f`. The PR diff (base→pinned) is exactly the prompt's 8 declared files (16,369 insertions, 5 deletions). The worktree HEAD (`359d461d`) is one commit ahead of the pinned target; that commit changes only the review prompt file, so every reviewed artifact in the working tree is byte-identical to its pinned-commit state (staleness gate passes).
- **Authority.** `.agents/workflow-overlay/` (review-lanes, delegated-review-patch, validation-gates, source-of-truth, communication-style) and `docs/decisions/orca_mini_god_tier_doctrine_v0.md`. Findings-first, advisory; strict verdict/approval/readiness authority is not bound to this lane and is not claimed.
- **Decision criteria (fitness reference).** `creator_profile_current_view_spec_v0.md` + `creator_intelligence_profile_surface_v0.md` + the MGT accepted-residuals doctrine. The fitness reference was attacked as an alignment axis, not used as a pass-if-matches bar.

## Source-Read Ledger And Validation Evidence

Reviewed at the pinned commit state (working tree == pinned for all targets):

- All 8 PR target files read directly (spec, surface, audit, live probe, both test files; seed and export read by head + tail + targeted greps and verified by the rederivation tests below).
- Source-pack files verified present and tracked at the pinned commit: the YouTube Shorts fragrance creator observation ledger, the public-handle linkage ledger, the 5 YouTube capture inputs, the live probe receipt, and the creator ledger review-input. Their content was verified by executable cross-derivation (the tests re-read them) plus SHA-256 currency checks, rather than full manual read.
- `.agents/workflow-overlay/source-loading.md` and `.agents/workflow-overlay/prompt-orchestration.md` were referenced via the overlay README index, the embedded DCP receipts in `source-of-truth.md`, and the "Prompt Orchestration Gates" restatement in `validation-gates.md`, not full-text read. Non-decisive for a read-only execution review; noted for honesty.

Validation evidence (per the prompt's `validation_gates_to_inspect`):

- **Tests named in the PR — RERUN, GATE PASS.** `python -m pytest orca-harness/tests/unit/test_youtube_creator_metric_seed.py orca-harness/tests/unit/test_creator_profile_current_static_view.py` → `8 passed`. These tests independently re-read the 5 source capture files and assert `observation.metric_value_or_none == source.view_count` (`test_youtube_creator_metric_seed.py:186`), recompute `average_views`/`median_views`/min/max (`:217-221`), and recompute SHA-256 against live file bytes (`:228-233`); the export tests rebuild from identity + seed and recompute hashes (`test_creator_profile_current_static_view.py:98-153`). This is genuine re-derivation, clearing the receipt-field non-self-certification gate.
- **`git diff --check` (base→pinned) — RERUN, GATE PASS.** Exit 0; no whitespace or conflict-marker errors.
- **Retrieval-header check, map-link check, placement advisory — NOT RUN** as tool invocations. Retrieval headers on the touched docs were confirmed present by direct read; map-reachability of the changed docs was not machine-checked.

## Findings

Ordered by severity. No `critical` findings. Findings are decision input only (see Review-Use Boundary).

### AR-01 — major — average influence is presented without a representativeness residual

- **Phase:** correctness.
- **Target / role:** `youtube_shorts_fragrance_creator_metric_seed_v0.json` (metric rollups) and `creator_profile_current_view_v0.json` (current_metric_rollups); source-family metric seed + static profile export.
- **Location:** seed `metric_rollups[*]` (`observation_count`, `metric_rollups.average_views/median_views`) and `accepted_residuals` (lines 11307–11313), `limitations` per rollup (e.g. profile lines 131–136, 159–165); export uniform posture enforced by `test_creator_profile_current_static_view.py:93-94`.
- **Source authority:** `creator_profile_current_view_spec_v0.md` "Aggregate Influence Rules" (state window/scope/source rows — satisfied) and `creator_intelligence_profile_surface_v0.md` "Aggregate influence rules" (surface must withhold/downgrade thin claims); MGT doctrine (material residuals must be named).
- **Issue.** The per-account view rollups span a wide sample-size range — observed distribution across the 30 rollups: n=1 (×2), n=2 (×1), n=3 (×3), n=4 (×2), n=5 (×5), n=6 (×3), n=7 (×2), n=8 (×3), n=9 (×3), n=10 (×2), n=11 (×1), n=12 (×3); total 196 observations. For the two n=1 accounts, `average_views` and `median_views` equal a single video's view count (min == max == mean == median), yet they carry `posture: observed`, identical to the n=12 accounts. Two representativeness residuals are unnamed: (a) **small-n** — an "average" over 1–3 admitted Shorts is statistically thin; and (b) **within-pool selection bias** — the pool is the *admitted fragrance, transcript-bearing* Shorts subset, so even setting n aside the average is not an unbiased estimate of an account's fragrance-Shorts performance. The artifact names the pool *boundary* ("admitted-pool averages, not full-channel creator averages", `accepted_residuals[0]`) but not the small-n or selection-bias *representativeness* residual.
- **Evidence.** `observation_count: 1` occurs twice (grep over `metric_rollups[*].observation_count`); `average_views`/`median_views` carry `posture: observed` for every profile (test-enforced, `:93-94`); `accepted_residuals` (seed 11307–11313) and per-rollup `limitations` (e.g. 131–136) contain no small-n or selection-bias caveat; the surface contract's withhold list (`creator_intelligence_profile_surface_v0.md` "Aggregate influence rules") enumerates stale/blocked/hidden/recipe-missing but not small-n.
- **Strongest defense, and why it does not fully hold.** Defense: `observation_count`, `view_count_min`, `view_count_max` are present on every rollup, so n=1 is fully transparent; the spec requires stating the feeding rows (done) and sets no minimum-n; the data is real and source-backed; the seed is explicitly "not the final answer" with 12 non_claims. This defense downgrades severity but does not close the finding: the MGT fitness reference requires material residuals to be *named*, not merely *derivable*; uniform `posture: observed` conflates "this number was observed" with "this average is representative"; and the downstream Creator Signal surface — whose job is to withhold thin influence claims — is given neither a withhold rule nor a per-rollup flag to act on, so the residual can propagate as an apparently-equal "observed average."
- **Impact.** A future surface/dashboard or downstream consumer can present an n=1 admitted-pool figure as a creator "average view" with the same confidence as a well-sampled one, overstating influence — the exact over-claim the spec/surface forbid. This is a disclosure/claim-shape gap, not a data-correctness defect (the underlying values are real and source-backed).
- **minimum_closure_condition.** The representativeness residual is named explicitly in `accepted_residuals` (and/or per-rollup `limitations`) — covering both small per-account n and within-pool admission selection — so a builder cannot treat any admitted-pool average as a representative creator average; optionally a per-rollup sample-adequacy signal (or a non-uniform posture) is carried so a surface can withhold/annotate thin or biased averages.
- **next_authorized_action.** CA decision: accept the residual as-is for this static seed step, or request a docs-only patch (no patch authority is bound to this review lane) adding the named residual and, if desired, a sample-adequacy field plus a surface withhold rule.
- **patch_queue_entry:** not authorized (read-only adversarial artifact review; advisory remediation only).
- **Advisory remediation direction.** Add one residual line such as "per-account averages cover 1–12 admitted Shorts; small-n and admission-filtered selection mean an admitted-pool average is not a representative creator average"; optionally emit `observation_count`-derived adequacy (e.g. `sample_adequacy: thin|adequate`) and extend the surface's withhold list to small-n.
- **Strict claims remaining `not proven`:** any readiness/validation/approval of the rollup as a representative influence measure.

### AR-02 — minor — per-observation drill-back uses non-portable absolute machine-local paths

- **Phase:** friction.
- **Target / role:** `youtube_shorts_fragrance_creator_metric_seed_v0.json` `metric_observations[*].source_packet_pointer_or_none`.
- **Location:** e.g. observation `yt_fragrance_short_view_obs_v0_001`, `source_packet_pointer_or_none: "F:\\orca-data-lake\\raw\\b62\\01KW1KZ9850GXWYRQPPYYWFKKC"` (seed line 117); appears as a per-observation provenance field.
- **Source authority:** `creator_profile_current_view_spec_v0.md` (observations carry a `source_pointer`); general provenance reproducibility.
- **Issue.** The authoritative provenance fields are repo-relative and correct (`source_pointer`, `source_field` → the checked-in capture JSON). The additional `source_packet_pointer_or_none` records an absolute machine-local lake path that will not resolve on another host or in CI.
- **Strongest defense, and why it partially holds.** Defense: this is optional drill-back (`_or_none`), not load-bearing; the repo-relative `source_pointer` is the real provenance, and `accepted_residuals[3]` already states the lake has no typed `metric_observations` for these rows. The defense largely holds — hence minor — but the absolute path is still non-portable provenance that reads as authoritative and would dangle if ever relied upon.
- **Impact.** Low: a reproducibility/portability smell; no current consumer depends on it.
- **minimum_closure_condition.** Absolute machine-local pointers are either dropped, relativized, or explicitly labeled as non-portable local-only drill-back.
- **next_authorized_action.** CA decision; optional docs-only hardening. No blocker.
- **patch_queue_entry:** not authorized (advisory only).
- **Advisory remediation direction.** Prefer a stable packet id (the `source_packet_id_or_none` already present) over an absolute `F:\` path, or mark the field local-only.

## Non-Findings: Failure Modes Attacked That Held

These are reported so the CA can see what was adversarially tested and confirmed, not as approval.

- **Source-backedness is not self-certifying.** Seed view counts re-derive from the 5 named capture files and source hashes are recomputed against live bytes — both confirmed by passing tests (`test_youtube_creator_metric_seed.py:186,228-233`). The hash pins are verified, not asserted.
- **No fake-success / no observed zeroes.** Zero view_counts are stored as `0` (grep: none); likes/comments/subscribers/engagement are held `unavailable_with_reason`/`not_attempted` with reasons and `null` values (export 87–104; test `:171-174`); the seed's `selection_policy.metric_value_rule` states absent metrics are not zero-filled (68–73).
- **Identity and cross-platform boundaries hold.** All 30 profiles are `single_platform_observed`, `creator_record_id` null, 0 cross-platform rollups, 0 ideal-audience joins (export counts 25–33; test `:79-95`). The 4 Scentbird brand rows are preserved as exclusions with source pointers, not creator rollups (seed 11265–11306).
- **Claim boundary holds.** Seed `non_claims` (12) and per-profile `non_claims` (8, test-enforced) disclaim channel-wide influence, engagement rate, buyer proof, cross-platform rollup, and SQLite/data-lake physicalization. The rollup window is labeled `custom` + "admitted_fragrance_shorts_pool200_v0; not a full creator-channel window."
- **Static export is not a second source of truth.** It hash-pins its immediate inputs (linkage ledger + seed), carries freshness, limitations, and source drill-back, and the test rebuilds it from the siblings and fails on hash drift — so a hand-edit diverging from source is caught.
- **Live probe is correctly bounded.** Framed as route sanity (2/3 exposed viewCount, 1/3 null, like/comment counts absent) and explicitly "not used as the 200-row seed source" (seed 50–54); the seed is sourced from checked-in captures, not the probe.
- **Spec/surface edits are tight.** Spec (+11/-5) converts "a future static/manual artifact, if needed" into "the first static export" and tightens the second-source-of-truth wording; surface (+5) adds one testing-sequence sentence. No claim-boundary regression, no scope creep.
- **MGT residuals largely named.** Explicit `accepted_residuals` (5) cover the admitted-pool boundary, capture-time drift + the probe miss, absent like/comment/subscriber/engagement, the lake gap, and the cross-platform block. AR-01 is the one material residual not yet named.

## Residual-Risk Note

- **Capture trust root, thin live anchor.** Source-backedness means "backed by the checked-in capture artifacts," verified transitively (seed == captures) and by integrity hashes, but live-reconfirmed for only ~2 videos via a 3-video probe (1 of which returned no current view count, and that video is itself a seeded row). The artifacts honestly label values as capture-time and disclose the probe miss; they do not claim live verification. Bounded and named, not zero.
- **Identity provenance upstream-chain hop.** The export's `identity_evidence_summary.source_pointers` point to `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json`, which sits outside the export's hash-pinned `source_inputs`. The displayed handle/account travels through the hash-pinned linkage ledger (test asserts `platform_accounts == [account]`), so the export's *immediate* inputs are correctly pinned; this is an upstream-chain observation about a pre-existing review-input, not a defect PR #439 introduced.
- **Severity calibration.** AR-01 is held at major because the commission explicitly elevates "silent residual that should be explicit before the PR is built on"; it is framed as a disclosure/claim-shape gap, not a data-correctness break, and closure is cheap.

## Review-Use Boundary

These findings and non-findings are decision input for CA adjudication only. They are not approval, validation, product proof, readiness, mandatory remediation, or patch authority. Only a separately authorized acceptance, patch, validation, or implementation lane can make any remediation mandatory or executor-ready. No artifact under review was edited.

## Delegated Review Return Courier

```text
DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: de-correlated review of PR #439 (creator metric source
  audit); decide if it is safe to adjudicate as the current creator-ledger/
  profile base. Read-only (multi-file artifact set; not single-target patch).
- reviewed artifact set: 8 PR #439 files at commit 23dce2d4 (metric seed,
  static profile export, spec +11/-5, surface +5, 2 rederivation tests, audit
  note, live probe receipt). Bounded patch scope: none (read-only).
- findings: AR-01 (major) representativeness residual unnamed — n=1..3 account
  averages with uniform posture "observed" + unnamed within-pool selection
  bias; AR-02 (minor) non-portable absolute lake drill-back paths.
- source evidence: 8/8 rederivation tests pass; git diff --check clean;
  observation_count distribution shows n=1 ×2; accepted_residuals/limitations
  carry no small-n or selection-bias caveat; uniform observed posture is
  test-enforced.
- proposed edits: none authorized (advisory only). Advisory direction in AR-01/
  AR-02 remediation fields.
- citations: file:line anchors in each finding and the non-findings section.
- reviewer verdict: accept_with_friction — boundaries and source-backedness
  hold; AR-01 is the one residual to name before building on the influence base.
- residual risk: capture trust root with thin live anchor; identity provenance
  upstream-chain hop outside the export's hash-pinned inputs.
- blockers / off-scope / not-proven: no strict PASS/readiness/validation/approval
  is claimed; patch authority not bound; YouTube capture architecture, lake
  migration, dashboard design, and creator-signal strategy were out of scope.
```
