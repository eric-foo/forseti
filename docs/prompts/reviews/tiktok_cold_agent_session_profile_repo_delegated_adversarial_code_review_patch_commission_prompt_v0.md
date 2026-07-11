# Repo-Mode Delegated Adversarial Code Review + Patch Commission — TikTok Cold-Agent Session Profile (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for a de-correlated cross-vendor adversarial
  code review and bounded patch of the TikTok cold-agent logical session
  profile, stable auth-state resolution, pre-action owner handoff, and
  diagnostic challenge classification implementation.
use_when:
  - Dispatching this commission to a repo-capable controller from a different vendor/model lineage than the OpenAI author.
  - Re-dispatching unchanged after verifying worktree, branch, base HEAD, dirty target set, and hashes.
authority_boundary: retrieval_only
```

## What this is for

**Goal:** A cold agent can invoke TikTok capture with
`--session-profile chowdakr_sg_tiktok`, use the validated cookie-backed session,
and receive owner handoff before any scripted pointer action when a challenge is visible.

**Done looks like:** the profile validates before browser launch with no
logged-out fallback or secret/path leakage; an uncleared challenge suppresses
scripted pointer actions; TikTok slider diagnostics are classified; explicit
legacy session invocations remain compatible.

This is the executor target and review axis to attack, not a pass-if-matches bar.

## Commission binding

- Overlay: `provisional_opt_in`; explicitly owner-commissioned.
- Contract: `.agents/workflow-overlay/delegated-review-patch.md`.
- Target kind: `delegated_code_review_and_patch`.
- Method: `workflow-code-review` after `workflow-deep-thinking` and source readiness.
- Mode: `base-subagent`; access: `repo`.
- Author/home family: OpenAI (Codex, GPT-5 family).
- Controller: must record a different upstream vendor/model lineage. Unknown or
  undisclosed lineage does not clear de-correlation.
- Receiving role: `controller`; dispatch: `external-controller-courier`.
- Who-constraint only; not a runtime model recommendation.
- Why patch authority is included: the owner commissioned one independent
  review-and-patch pass, and defects in secret resolution, challenge ordering,
  or false-success classification need bounded closure before CA adjudication.
- CA adjudicates every returned claim and diff before anything is kept.

## Repository preflight

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 (fused + delegated code review + TikTok cold-agent controlling sources)
  edit_permission: implementation-authorized
  target_scope: the explicitly named target set below
  dirty_state_checked: yes
  blocked_if_missing: wrong worktree/branch/base, target hash mismatch, disallowed dirty path, unavailable review method, or failed de-correlation
repo_map_decision: not_needed
repo_map_reason: exact targets and controlling TikTok sources are directly bound.
```

- Workspace: `C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\cold-agent-tiktok-session-profile`
- Branch: `codex/cold-agent-tiktok-session-profile`
- Base HEAD: `122e7116c49fd3a9985a932193bfa88bd4ef8350`
- Dirty state: allowed only for the named target set plus this prompt. New
  runner/profile/test files are expected untracked before commit.
- Run-authoritative prompt:
  `docs/prompts/reviews/tiktok_cold_agent_session_profile_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md`
- Output mode: `review-report`
- Report:
  `docs/review-outputs/adversarial-artifact-reviews/tiktok_cold_agent_session_profile_delegated_adversarial_code_review_v0.md`

Wrong source state → `BLOCKED_SOURCE_STATE_MISMATCH`. Do not substitute another
checkout, a summary, a context pack, or recreated source.

## Entire patchable target set

Verify current filesystem SHA256:

- [goal] `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md` — `3848433d09735d53eec11dec6340b0893578773a667fb9aad0dade254ef751e8`
- [playbook] `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md` — `3004f137d75a19a368215085b3781a2318f018413e85b1c437fb7d63f46396fe`
- [runbook] `forseti-harness/docs/source_capture_agent_runbook.md` — `5ecd4135d0715d4de6556b8f3fb9eca14f767376f616e2a1781e3c74afcf1543`
- [live-runner] `forseti-harness/runners/run_source_capture_tiktok_live_batch_probe.py` — `6d0dbbc6559a58ec09874cd1adf8005b61d71c09f63c19c21903cfd271dd5b6e`
- [profile-preflight] `forseti-harness/runners/check_source_capture_session_profile.py` — `01dda3bd40817066ec578a30a020cb92957adbdf3b61640ca467d8627de5c858`
- [browser-adapter] `forseti-harness/source_capture/adapters/browser_snapshot.py` — `56e96ef42a93205618b33905852c51a0902c49f7625c9d27a6a6241c44a7f54f`
- [session-profile] `forseti-harness/source_capture/session_profiles.py` — `917945322ba9a785bd513baa989217b4bec85634151d00ed69ed11003a4f6290`
- [rendered-access] `forseti-harness/source_capture/rendered_access.py` — `146e89878aaf96037db1a05b07462f4cc726467512dce5b73977961ea22a8354`
- [tiktok-probe] `forseti-harness/source_capture/tiktok/live_batch_probe.py` — `6bf6f7ff6ce6e6babf5d9e792b40cf373021ef9cdca24f0a39a09060d7a77871`
- [rendered-tests] `forseti-harness/tests/unit/test_rendered_access.py` — `6dfb24b45ecd27d892a3621592a61130df8cd5c8ed2b2c58f504ad0505ebba45`
- [profile-tests] `forseti-harness/tests/unit/test_source_capture_session_profiles.py` — `e0425aace128ee1c6a139faf0bef59a8b3b108c16094f9a9f8c3bddbc193c8a8`
- [adapter-tests] `forseti-harness/tests/unit/test_source_capture_browser_snapshot.py` — `10bbbdb37d23fad9d1dddeffe62b0cc36ce1f01f334635517a5947784a958596`
- [probe-tests] `forseti-harness/tests/unit/test_tiktok_live_batch_probe.py` — `e91a2898ca05cf0c9797c2ab1c2b07bee08921c8dc6ac84b73e9cadba39bc9fb`

Everything else is read-only/flag-only. Do not inspect or edit real
cookie/storage-state files, `%LOCALAPPDATA%\Forseti`, any `_auth_state`, live
outputs, registry/lake data, automation, unrelated tests, overlay authority,
generated/hash-pinned artifacts, or this prompt. Do not commit, push, open a PR,
or perform live TikTok/network capture.

## Required method sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review`.
3. Do not APPLY either method yet.
4. SOURCE-LOAD this commission, the target set, safety/review/delegated-review
   overlay contracts, the TikTok goal/playbook/runbook, the provenance
   architecture decision, and the TikTok capture lane spec.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only then APPLY deep-thinking to frame failure modes, then APPLY code review
   findings-first and coverage-first.
7. Patch only the named set when justified; fresh-read changed targets; run validation.
8. Write the report and run the report provenance gate.

Unavailable method → `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not patch.

## Adversarial questions

1. Does profile config and stable auth state validate before browser launch, and
   is the exact resolved root threaded through the live writer's second validation?
2. Do missing, malformed, unreadable, legacy, and mismatched states fail closed
   without logged-out fallback, secret/path leakage, or raw tracebacks?
3. Is stable-root behavior profile-only while explicit legacy `--state-label`
   retains worktree-local semantics?
4. Can profile/manual conflicts override policy, enable a diagnostic backend, or
   turn on X/Close?
5. In both browser engines, does visible challenge detection occur before
   post-load scripts and pointer actions; do uncleared markers suppress actions;
   and do cleared markers resume the route exactly once?
6. Does owner handoff keep the browser open, forbid agent solving, and preserve
   source-access-intervention/non-clean receipt semantics?
7. Did the move from after-close to page-load handoff leave stale receipt
   consumers, misleading fields, or missing downstream tests?
8. Are explicit diagnostic and separately authorized X/Close routes intact and
   excluded from `chowdakr_sg_tiktok`?
9. Can TikTok visible/DOM markers false-positive ordinary source content or
   produce an empty limitation receipt?
10. Would tests fail under old behavior, and do they cover root precedence,
    pre-browser blocking, non-disclosure, runner binding, pre-action order,
    uncleared suppression, backend parity, and diagnostic classification?
11. Are goal/playbook/runbook synchronized without making the rotating local
    binding durable authority?
12. Does any correct fix require `NEEDS_ARCHITECTURE_PASS`?

Report every issue with severity (`critical`/`major`/`minor`) and confidence
(`high`/`medium`/`low`). Do not filter low-confidence or awkward findings.
List steelman-defeated candidates under `considered_and_defended`.

## Patch and validation boundary

Patch only defects affecting the named behavior or its tests/contracts. Label
every finding, citation, and diff hunk with its target tag. Flag off-scope issues.
Design-level issue → `NEEDS_ARCHITECTURE_PASS`, findings only, no partial diff.

Run from `forseti-harness`:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider -q --basetemp pytest_cold_session_profile_review `
  tests/unit/test_source_capture_session_profiles.py `
  tests/unit/test_rendered_access.py `
  tests/unit/test_tiktok_live_batch_probe.py `
  tests/unit/test_source_capture_browser_snapshot.py `
  tests/unit/test_source_capture_authenticated_browser_snapshot.py `
  tests/unit/test_source_capture_cloakbrowser_snapshot.py `
  tests/contract/test_source_capture_browser_snapshot_contract.py
```

Author evidence: 213 tests collected and the slice exited 0. Verify; do not inherit.
Do not inspect real session state or run live network capture.

After report write, run from worktree root:

```powershell
python .agents/hooks/check_review_output_provenance.py --strict `
  docs/review-outputs/adversarial-artifact-reviews/tiktok_cold_agent_session_profile_delegated_adversarial_code_review_v0.md
```

Nonzero/unavailable is visible failure.

## Controller output

Record `reviewed_by` (actual identity or `unrecorded`),
`authored_by: gpt-5-codex`, `de_correlation_bar: cross_vendor_discovery` only
when established, `access: repo`, and source readiness.

Return findings first. Each finding includes target tag, severity, confidence,
file:line, neutral evidence, impact, `minimum_closure_condition`,
`next_authorized_action`, and patched/not-patched. Then return
`considered_and_defended`, patch summary, labeled unified diff or no-patch
reason, observed validation or not-run reason, residual risk/off-scope flags,
and verdict: `PATCHED_FOR_CA_ADJUDICATION`,
`NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, or `BLOCKED`.
Include overlay-compatible `review_summary` YAML.

Findings, citations, diff, verdict, and residuals are claims to adjudicate.
Nothing is kept until home/CA adjudication. The return must direct CA to
`communication-style.md` → Review Adjudication Next Step: adjudicate claims;
close self-closable material issues now; route only issues needing another
lane/owner/architecture/review; then exactly one land step plus 1–5 material moves.

## Dispatch note

Paste this commission into an independent repo-access lane satisfying the
different-vendor who-constraint. Courier the complete return to home CA
adjudication.

Non-claims: provisional convention; no runtime model recommendation; no
validation, readiness, approval, acceptance, live TikTok success, CAPTCHA
solving authority, auto-keep, commit, push, merge, registry/lake mutation, or
automation authority.
