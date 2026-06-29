# Delegated Adversarial Code Review (Repo Mode) - Creator Profile Current Materializer v0

```yaml
retrieval_header_version: 1
artifact_role: Review report (delegated_code_review_and_patch return, repo mode; decision input for CA adjudication)
scope: >
  Cross-vendor delegated adversarial code review of PR #452, the
  creator-profile-current materializer that derives the checked-in creator
  profile view from the sibling public-handle account ledger and the YouTube
  creator metric seed. Repo-mode discovery pass; no patch applied. Decision
  input for home-model (CA) adjudication, not owner acceptance or validation.
use_when:
  - Adjudicating whether PR #452 can be treated as settled for its v0 scope.
  - Checking source-backed findings on fake-freshness, stale output, source-hash
    honesty, join fail-closed behavior, and scope-smuggling for the materializer.
authority_boundary: retrieval_only
commission_prompt: docs/prompts/reviews/creator_profile_current_materializer_delegated_adversarial_code_review_patch_prompt_v0.md
reviewed_pr: https://github.com/eric-foo/orca/pull/452
reviewed_branch_or_commit: codex/creator-ledger-real-seed @ d8edd7862d9471ccc0b101266387f337d7bba967
reviewed_diff: 2d08b747c720ed6dc0b1031ea5828b01663286b6..d8edd7862d9471ccc0b101266387f337d7bba967
pinned_content_verified: true   # all 5 target files raw-worktree sha256 == commission input_hashes
open_next:
  - orca-harness/capture_spine/creator_profile_current/materialize.py
  - orca-harness/runners/run_creator_profile_current_materialize.py
  - .agents/workflow-overlay/delegated-review-patch.md
stale_if:
  - The CA adjudicates this commission (findings dispositioned).
  - Any reviewed target file changes after d8edd786.
  - PR #452 is rebased onto a different base than 2d08b747.
```

## review_summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_profile_current_materializer_adversarial_code_review_v0.md
  recommendation: accept
  reviewed_by: claude-opus-4.8
  authored_by: openai-codex-gpt-5      # per commission actor/model-family receipt; not self-emitted authority
  de_correlation_bar: cross_vendor_discovery   # Anthropic delegate != OpenAI author; discovery bar satisfied
  same_vendor_rationale: not_applicable
  access_mode: repo
  summary: "The materializer is a genuine deterministic derivation of the checked-in view from the two sibling ledgers, the staleness gate fails closed (adversarially confirmed both directions), the source-hash convention matches the repo LF-normalized standard, and no scheduler/lake/SQLite/engagement scope is smuggled; six minor/advisory residuals remain, none blocking."
  findings_count: 6
  blocking_findings: []
  advisory_findings: [F1-duplicate-rollup-robustness, F2-hardcoded-limitation-desync, F3-runner-untested, F4-counts-pre-validation-keyerror, F5-hash-recipe-duplicated, F6-write-crlf-on-windows]
  patch_status: no_patch_needed
  changed_files: []
  validation_run:
    - "python runners/run_creator_profile_current_materialize.py --check  -> up to date, exit 0"
    - "python runners/run_creator_profile_current_materialize.py --check --account-ledger <modified copy>  -> stale, exit 2 (adversarial)"
    - "python runners/run_creator_profile_current_materialize.py --write --output <scratch copy>  -> generated_at_utc preserved, content-identical modulo EOL"
    - "pytest tests/unit/test_creator_profile_current_static_view.py tests/unit/test_youtube_creator_metric_seed.py -q  -> 22 passed"
  validation_not_run:
    - "full orca-harness pytest (not warranted: no patch; behavior change confined to net-new materializer/runner/tests already covered by the focused suite)"
  residual_risk: "All six residuals are latent or forward-looking (duplicate-rollup defense-in-depth, hardcoded posture text that could desync only if the seed gains observed engagement/like/comment metrics, an untested runner CLI whose core staleness invariant is already protected by the parity test); none affects the current v0 output, which is fully source-backed and validator-clean."
  next_action: "CA adjudicates: accept PR #452 for v0 scope as-is, or separately authorize any subset of the named optional hardening (none is required and none is patch authority under this commission)."
```

## 1. Commission, Lane Binding, And Actor/Model-Family Receipt

- **Commission.** Explicit owner invocation of `workflow-delegated-review-patch`
  for PR #452 via the filed prompt
  `docs/prompts/reviews/creator_profile_current_materializer_delegated_adversarial_code_review_patch_prompt_v0.md`.
- **Lane / mode.** `delegated_code_review_and_patch` sibling mode
  (`.agents/workflow-overlay/delegated-review-patch.md`), `access: repo`,
  base-subagent / repo-mode controller. Review method is `workflow-code-review`
  (deep-thinking first, source-gated) per the contract; `workflow-adversarial-artifact-review`
  was held in reserve for the repo-map route text and was not needed (the route
  text is accurate - see Off-Scope / Non-Findings).
- **Actor / model-family receipt.**
  - `author_home_model_family`: OpenAI / Codex (commissioning lane).
  - `controller_model_family`: Anthropic / Claude (Opus 4.8) - **this review**.
  - `de_correlation`: **cross_vendor_discovery satisfied** (Anthropic != OpenAI).
    The no-tester/testee bar holds: the reviewing runtime is a different vendor
    from the author, so this is a discovery pass, not a self-review.
  - `dispatch_mode`: external-controller-courier; the receiver inspected the
    pinned worktree directly, not a pasted source pack.
- **Authority boundary.** This return is decision input only. It is not owner
  acceptance, validation proof, readiness, `PASS`, source-capture authorization,
  live-lake authorization, SQLite adoption, or permission to keep anything
  without CA adjudication.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

- **Authority reads (current task context):** `AGENTS.md`,
  `.agents/workflow-overlay/README.md`, `source-loading.md`, `review-lanes.md`,
  `delegated-review-patch.md`, `prompt-orchestration.md`, `decision-routing.md`,
  `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`. All read from
  the target worktree; the target worktree `AGENTS.md` is byte-identical to the
  session context copy.
- **Staleness gates (all pass).** PR #452 is `OPEN`, `baseRefName: main` (not
  retargeted); base `2d08b747` is the merge-base with `origin/main` and an
  ancestor of the pinned head; the only commit after `d8edd786` is the prompt
  artifact itself (`a971e9c0`, +257 lines, no target file touched); the four
  named overlay-authority files are byte-identical between the branch head and
  current `origin/main`.
- **Pinned-content integrity verified.** All five target files' raw-worktree
  SHA-256 equal the commission `input_hashes` (the `.py`/`.md` files are CRLF in
  this Windows worktree because they are not covered by `.gitattributes eol=lf` -
  only `social_media/**/*.json` is - and the commission hashed raw worktree
  bytes). The reviewed content is exactly the pinned content.

  | target | repo-convention (LF-normalized) sha256 | commission input_hash (raw-worktree) |
  | --- | --- | --- |
  | `materialize.py` | `b90d12d9...a669c30` | matched (`84088525...a104ff7c`) |
  | runner | `2879d562...e9476c8c` | matched (`a869e73a...044fa8f63`) |
  | tests | `b52f1349...ead13558` | matched (`55878ac6...0824ec31`) |
  | `__init__.py` | `a47fdece...7595e1c5` | matched (`fac68ff1...10104ab9`) |
  | `orca_repo_map_v0.md` | `2bb45d1a...72f957db` | matched (`eca433cf...17f8606e`) |

- **Task source pack loaded:** the pinned diff; the five current target files;
  the two source ledgers (`creator_public_handle_linkage_ledger_v0.json`,
  `youtube_shorts_fragrance_creator_metric_seed_v0.json`) and the materialized
  output (`creator_profile_current_view_v0.json`); the always-on validator
  `creator_profile_current/validation.py`; the adjacent
  `test_youtube_creator_metric_seed.py` (canonical source-hash convention); and
  the product spec `creator_profile_current_view_spec_v0.md` (source-of-truth /
  SQLite / lake boundary).
- **No source gap material to the verdict.** The lake-native record mapping doc
  was available-not-read because no finding turned on it; the validator and the
  spec's "derived view, not a source of truth" section were decision-sufficient.

## 3. Findings (severity order)

No `critical` findings. No `major` findings. Six `minor`/advisory findings.

### F1 - minor - `[creator-profile-materializer-core]`

- **Location:** `materialize.py:138-161` (`build_creator_profile_current_view_document`,
  the four `*_by_*` / `*_index` dict comprehensions and the `set(...) != set(...)` join guard).
- **Issue:** The account<->rollup join is expressed as dict comprehensions keyed
  by id plus a **set-equality** guard. Dict comprehensions silently collapse
  duplicate keys (last-wins), and set equality compares key *sets*, not
  cardinality. A duplicate `profile_subject_id` among the metric-seed rollups
  that preserves the key set (e.g. 31 rollups, 30 distinct subjects) passes the
  guard and silently drops the shadowed rollup.
- **Evidence:** `rollups_by_subject = {rollup["profile_subject_id"]: rollup ...}`
  collapses; `if set(accounts_by_id) != set(rollups_by_subject)` only compares
  presence. The *account*-side duplicate is already caught downstream
  (`validate_creator_profile_current_view` -> `duplicate_profile_subject_id`,
  `validation.py:248`), and a same-cardinality rollup duplicate (30 rollups, 29
  distinct) is caught by the set guard (29 != 30). The one uncaught shape is
  caught only by the *sibling* seed test (`test_youtube_creator_metric_seed.py:152`,
  `len(rollups) == 30`), not by the materializer itself. Current data has no
  duplicates (the passing `set(accounts_by_id) == set(rollups_by_subject)` over
  30/30 in `test_creator_profile_current_static_view.py:159` proves uniqueness).
- **Impact:** Latent only; defense-in-depth gap. No live trigger.
- **minimum_closure_condition:** The materializer fails closed (or is proven to)
  on a duplicate join key on *either* side, rather than relying on a sibling
  file's count test.
- **next_authorized_action:** Optional hardening (CA-authorized), e.g. assert
  `len(accounts_by_id) == len(accounts)` and `len(rollups_by_subject) == len(rollups)`
  before the join. Non-required.
- **Patched:** No.

### F2 - minor - `[creator-profile-materializer-core]`

- **Location:** `materialize.py:272-280` (per-profile `limitations` constant list)
  and `233-290` (hardcoded `identity_state`, `non_claims`, `identity_evidence_summary.summary`).
- **Issue:** Each profile carries hardcoded, data-*independent* posture text that
  asserts data-*dependent* facts - notably "Engagement rate, average likes, and
  average total comments are unavailable until source-backed numerator fields
  exist" - emitted unconditionally for every profile regardless of the rollup's
  actual metric postures. The validator checks these fragments are *present*
  (`_REQUIRED_NON_CLAIM_FRAGMENTS`, `validation.py:149-158`), not that they are
  *accurate* against the metric postures.
- **Evidence:** If a future seed provided an `observed` `engagement_rate` /
  `average_like_count`, `_counts` would report `engagement_rate_observed_profiles > 0`
  (`materialize.py:310-317`) while the same profile still asserts those metrics
  "unavailable" - an internal contradiction the validator would not catch.
  Currently consistent: all 30 rollups have `engagement_rate.posture ==
  "unavailable_with_reason"` and null like/comment values
  (`test_creator_profile_current_static_view.py:140,244-246`).
- **Impact:** Latent "silently stale hand-authored field" risk, contingent on the
  seed gaining observed numerator metrics; v0 scope explicitly fixes them
  unavailable and names the residual.
- **minimum_closure_condition:** The "engagement/likes/comments unavailable"
  limitation is either derived from the actual metric postures, or a validator
  cross-check rejects a profile that asserts a metric unavailable while its
  rollup reports that metric `observed`.
- **next_authorized_action:** Optional hardening (CA-authorized). Non-required.
- **Patched:** No.

### F3 - minor - `[creator-profile-materializer-runner]` / `[creator-profile-materializer-tests]`

- **Location:** `run_creator_profile_current_materialize.py` (whole CLI surface);
  test file has no subprocess test of the runner.
- **Issue:** The runner's operator-facing logic - `--check` staleness exit, the
  `args.check == args.write` mutual-exclusion guard, `--write` timestamp
  preservation via `_existing_generated_at`, and exit-code-2-on-failure - has no
  automated regression test. The only `subprocess` use in the test file is
  `git check-attr`.
- **Evidence:** `test_creator_profile_current_static_view.py` covers the
  materializer core and parity, but never invokes the runner. **Mitigant:** the
  core staleness invariant is already regression-protected - the parity test
  `test_creator_profile_current_materializer_matches_checked_in_view` (line 185)
  fails in CI if a source ledger changes without refreshing the view, which is
  the same invariant `--check` expresses. I confirmed `--check` behavior manually
  in both directions (see Section 8).
- **Impact:** A regression in the runner's unique logic (timestamp preservation,
  arg guard) would not be caught automatically, but could not let a stale view
  pass CI (the parity test still would).
- **minimum_closure_condition:** A test exercises `--check` (green and stale) and
  `--write` (timestamp preserved) for the runner.
- **next_authorized_action:** Optional hardening within the tests target's bounded
  scope (CA-authorized). Non-required.
- **Patched:** No.

### F4 - minor (nit) - `[creator-profile-materializer-core]`

- **Location:** `materialize.py:303-323` (`_counts`), called at `190` before
  `validate_creator_profile_current_view` at `210`.
- **Issue:** `_counts` reaches `rollup["metric_rollups"]["engagement_rate"]["posture"]`
  and `rollup["platform_scope"]` before the validator runs, so a malformed seed
  rollup yields a raw `KeyError` rather than a typed `CreatorProfileCurrentError`.
- **Evidence:** Build order: `_counts(profiles)` -> wrapper -> `validate(...)`.
  The runner's `except Exception` still converts it to exit 2, so it fails closed;
  only the error message class/clarity differs.
- **Impact:** Cosmetic error-quality only; fails closed either way.
- **minimum_closure_condition:** Malformed-rollup input surfaces a typed
  validation error. (Or accept as-is: it already fails closed.)
- **next_authorized_action:** Optional; likely WONTFIX given fail-closed behavior.
- **Patched:** No.

### F5 - informational - cross-cutting (advisory only; touches a flag-only path)

- **Location:** `materialize.py:326-327` (`_sha256_repo_text`),
  `test_creator_profile_current_static_view.py:79-80` (`_sha256`),
  `test_youtube_creator_metric_seed.py:70-71` (`_sha256`).
- **Issue:** The LF-normalized source-hash recipe
  (`sha256(read_bytes().replace(b"\r\n", b"\n"))`) is independently re-implemented
  in three places. Consistent today (verified byte-identical), but a future
  convention change must update all three in lockstep or a silent split appears.
- **Impact:** DRY / maintainability only; no current correctness effect.
- **next_authorized_action:** Optional; a shared helper would close it, but the
  seed test sits outside the bounded target set, so this is flag-only here.
- **Patched:** No.

### F6 - minor - `[creator-profile-materializer-runner]`

- **Location:** `run_creator_profile_current_materialize.py:432`
  (`args.output.write_text(rendered, encoding="utf-8")`).
- **Issue:** `Path.write_text` defaults to `newline=None`, which translates `\n`
  to `os.linesep`, so on Windows `--write` emits **CRLF** working-tree bytes for
  the output JSON, while the checked-in file is LF.
- **Evidence:** Observed `{\r\n` first-line bytes from a scratch `--write` vs
  `{\n` in the checked-in view; content identical after CRLF->LF normalization
  (Section 8). **Absorbed by:** `.gitattributes` marks the output
  (`social_media/**/*.json`) `text eol=lf`, so git renormalizes CRLF->LF on add,
  and `--check` reads with universal-newline translation, so the CRLF working
  copy still verifies "up to date". No git churn, no false stale.
- **Impact:** Cosmetic for the in-repo default path; would only matter for an
  out-of-glob `--output` consumed byte-sensitively.
- **minimum_closure_condition:** `--write` emits LF on all platforms (e.g.
  `write_text(rendered, encoding="utf-8", newline="\n")`), or the reliance on
  `eol=lf` + universal-newline reads is accepted as intentional.
- **next_authorized_action:** Optional hardening (CA-authorized). Non-required.
- **Patched:** No.

## 4. Per-Finding Source Citations (neutral)

- Join + guard: `materialize.py:138-161`. Output duplicate guard:
  `validation.py:248-250`. Current 30/30 uniqueness:
  `test_creator_profile_current_static_view.py:159`; seed rollup count:
  `test_youtube_creator_metric_seed.py:152`.
- Hardcoded posture/limitations: `materialize.py:233-290`; required-fragment
  presence check: `validation.py:149-158, 533-538`; current all-unavailable
  metric state: `test_creator_profile_current_static_view.py:140,244-246`.
- Runner CLI: `run_creator_profile_current_materialize.py:408-447`; parity
  staleness gate that substitutes for a runner test:
  `test_creator_profile_current_static_view.py:185-192`.
- Hash convention identity across three sites: `materialize.py:326-327`,
  `test_creator_profile_current_static_view.py:79-80`,
  `test_youtube_creator_metric_seed.py:70-71`; gitattributes intent:
  `.gitattributes` ("Creator profile source-input hashes are recorded over LF
  repo-text bytes").
- View-is-derived boundary: `creator_profile_current_view_spec_v0.md:110-112,175,182`;
  `view_mode` constant: `materialize.py:167`.

## 5. Unified Diff

None. No target file was changed (`patch_status: no_patch_needed`).

## 6. Controller Verdict And Residual Risk

**Verdict: accept (decision input).** Within the commission-bound target, this is
a correct, honest, and adversarially-survivable v0 materializer:

- It is a **genuine derivation**, not a hand-authored snapshot. The output is
  rebuilt deterministically from the two sibling ledgers and proven to match the
  checked-in view exactly (parity test), while an independent re-derivation test
  (`...rebuilds_from_identity_and_metric_seed`) and the seed's own
  recompute-from-observations test anchor the join semantics to source - so the
  parity test's apparent circularity is broken by independent join verification.
- **Fake freshness and stale output are blocked.** `--check` fails closed on any
  source drift (adversarially confirmed: modified ledger -> exit 2), and the same
  invariant is enforced in CI by the parity test independent of the runner.
- **Source-hash honesty holds.** The hash is the repo's LF-normalized convention
  (byte-identical to the sibling seed test and consistent with `.gitattributes`),
  scoped in `role`/`non_claims`/`limitations` as provenance-of-input, never as
  proof of metric truth; the repo-map even adds "not a claim that all future
  metric rollups are source-backed".
- **No scope smuggling.** The diff adds no scheduler, dashboard, lake, SQLite,
  engagement-rate derivation, cross-platform stitching, live capture, or
  validator-framework change; the view remains a derived export, not a source of
  truth (spec-aligned).

**Residual risk (named).** All six findings are minor/advisory: F1 (duplicate-rollup
defense-in-depth), F2 (hardcoded posture text that could desync only if the seed
gains observed numerator metrics), F3 (untested runner CLI whose core invariant is
already protected), F4 (pre-validation `KeyError` clarity), F5 (triplicated hash
recipe), F6 (CRLF-on-Windows `--write`, absorbed by gitattributes). None affects the
current v0 output. The single non-independent sliver of this repo-mode pass is the
absence of any reviewer-authored patch (there is none), so there is no edited-line
blind spot to record.

## 7. Validation Run Status (exact)

Run by the controller from the pinned worktree:

- `python runners/run_creator_profile_current_materialize.py --check`
  -> `up to date: ...creator_profile_current_view_v0.json`, **exit 0**.
- (adversarial) `... --check --account-ledger <perturbed scratch copy>`
  -> `creator profile current view is stale: ...`, **exit 2**.
- (non-destructive) `... --write --output <scratch copy>` with no
  `--generated-at-utc` -> `generated_at_utc` preserved at `2026-06-28T19:07:16Z`;
  rewrite content-identical to the checked-in view modulo CRLF/LF.
- `python -m pytest tests/unit/test_creator_profile_current_static_view.py tests/unit/test_youtube_creator_metric_seed.py -q`
  -> **22 passed** (matches the commission's stated evidence).

**Not run:** full `orca-harness` pytest - not warranted. No patch was applied, and
the change surface is net-new (`materialize.py`, runner, three test additions, one
package export, one repo-map route) already covered by the focused suite; behavior
does not change beyond the materializer/join/check surface, so the contract's
"full suite only if behavior changes beyond that surface or focused evidence is
ambiguous" condition is not met.

## 8. Off-Scope Flags / Non-Findings

- **Repo-map route text (`[repo-map-route]`) - accurate, no finding.** The added
  capture_spine and runners lines correctly describe the materializer/runner and
  explicitly disclaim live capture, runtime readiness, SQLite adoption, person
  identity proof, and "a claim that all future metric rollups are source-backed".
  `workflow-adversarial-artifact-review` was therefore not required.
- **PR #452 is `mergeable: CONFLICTING` and a draft.** The branch is not rebased
  onto current `main` (`e5dfd03d`); the merge-base is still `2d08b747`. This is a
  merge-mechanics state, not a materializer-correctness issue, and is out of the
  reviewed-diff scope. Flagged for CA awareness only.
- **Commission `input_hashes` are raw-CRLF-worktree hashes (about the prompt
  artifact, not a target file).** They verified the pinned content on this
  Windows checkout but are machine/EOL-specific and would not reproduce on an LF
  checkout; the code's own source-hash convention (for the JSON ledgers) is
  correctly LF-normalized. Informational; the prompt artifact is dispatch
  context, not a patchable target.
- **No `NEEDS_ARCHITECTURE_PASS`.** No design-level defect was found; the
  account-scoped-only / single-platform-only shape is a named v0 residual
  consistent with the spec, not a broken design.
- Read-only / flag-only respected for all non-target paths (source ledgers,
  fixture data, specs, validator architecture, lake/SQLite, schedulers,
  dashboards, identity stitching, engagement derivation, overlay files).

## 9. CA Adjudication Packet

- **Commission:** delegated_code_review_and_patch, repo mode, 5-file bounded
  target, cross_vendor_discovery satisfied.
- **Target:** PR #452 materializer at `d8edd786` (content pin-verified).
- **Authority:** review = decision input only; no formal `PASS`/readiness/validation
  created; patch authority unused (no blocker/major).
- **Decision criteria:** fake-freshness / stale-output / source-hash-honesty /
  join-fail-closed / no-scope-smuggling / view-not-source-of-truth - all met.
- **Evidence:** Sections 2 and 7 (first-hand runs + tests + spec/validator reads).
- **Reviewer recommendation:** **accept** PR #452 for v0 scope as-is. Optionally,
  separately authorize any subset of F1/F2/F3/F6 hardening - each is non-required
  and is not patch authority under this commission.

## 10. Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's
findings, citations, and verdict are claims to adjudicate, not premises to inherit.
It is not owner acceptance, validation proof, readiness, deployment,
source-capture authorization, live-lake authorization, SQLite adoption, or
permission to keep or apply any change without Chief Architect adjudication. No
patch was applied; no `PASS`, severity authority, or readiness is asserted.
