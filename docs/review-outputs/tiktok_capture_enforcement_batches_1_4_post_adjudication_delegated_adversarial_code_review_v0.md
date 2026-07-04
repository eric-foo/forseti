# TikTok Capture Enforcement Batches 1-4 Post-Adjudication Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial code review-and-patch pass on the TikTok cold-agent
  capture enforcement BATCH-01 through BATCH-04 implementation, focused on the
  post-adjudication patch (fb078dd0) for human challenge handoff routing and
  interrupted-warmup provenance binding.
authority_boundary: retrieval_only
```

## De-Correlation Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/GPT-family Codex/GPT-5
  controller_model_family: Anthropic Claude (Sonnet 5)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_bar: cross_vendor_discovery
  de_correlation_status: satisfied
```

## Method

Read `open_next` authority sources (goal doc, provenance ADR, blocker playbook,
capture-lane spec) and the full task-specific source pack (all named source/test
files under `orca-harness/`) as source, not summaries. Ran `git rev-parse HEAD`,
`git status --short --branch`, `git show --stat --oneline fb078dd0`, and read the
full `git diff origin/main...fb078dd08539c1392002dc0ca145a41a02656ddc` content
(3358 lines). Read the `fb078dd0` commit content directly (`git show`) since it is
the specific post-adjudication patch this prompt targets. Did not inspect cookies,
auth-state contents, storage-state contents, proxy credentials, raw proxy
endpoints, exit IPs, signed subtitle URLs, device IDs, or tokens. Did not run a
live TikTok probe, launch a browser, refresh auth-state, or open a proxy profile.

`SOURCE_CONTEXT_READY`: all named source-pack files were read; strict findings
are not blocked.

## Findings

No critical or major findings. Two minor observations are recorded for
completeness; neither blocks the recommendation below.

### Finding 1 (minor, confidence: medium): `owner_attention_route` field is not covered by the batch-admission's `_summarize_contracts` allow-list, but this is intentional and correctly handled elsewhere

- File/line: `orca-harness/source_capture/tiktok/live_batch_probe.py:819-823` (`_with_manual_challenge_attention_required`); `orca-harness/source_capture/tiktok/batch_packet.py:665-692` (`_validate_staging_contracts`).
- Why it matters for the cold-agent TikTok capture goal: a cold agent inspecting a failure receipt needs to know whether a run stopped because handoff was disabled (`fail_closed_no_handoff_prompt`) versus because handoff was attempted and still didn't clear (`harness_human_challenge_handoff_prompt`). Both values are only reachable on a `failures[]` entry (never on a `results[]` row that also carries `admitted_comment_response_count`), and `_validate_staging_contracts` already rejects admission whenever any completed row carries `owner_attention_required=True` or `manual_challenge_attention_required=True` regardless of which route string is set. So the two-value distinction is diagnostic-only, not an admission-gating field, and its absence from `_summarize_contracts`'s cross-cadence rollup does not create an admission bypass.
- `minimum_closure_condition`: none required for merge safety. If a future batch wants `owner_attention_route` surfaced in the batch-summary receipt (for faster cold-agent triage without opening `cadence_result.json`), that would be a small additive change to `_summarize_batch` in `batch_packet.py`.
- `next_authorized_action`: no action needed now; optionally flag as a follow-up enhancement in a future batch, not a defect in this one.

### Finding 2 (minor, confidence: medium): subtitle-fetch redirect handler races the final-host check by one hop

- File/line: `orca-harness/source_capture/tiktok/live_batch_probe.py:2062-2088` (`_TikTokSubtitleRedirectHandler`, `_fetch_subtitle_webvtt`).
- Why it matters: `_TikTokSubtitleRedirectHandler.redirect_request` validates each redirect's `newurl` against the allowlist before following it, and `_fetch_subtitle_webvtt` re-checks `response.geturl()` after the request completes. Both checks use the same `_is_supported_subtitle_url` predicate against `TIKTOK_SUBTITLE_ALLOWED_HOST_SUFFIXES`. This is correctly fail-closed (a disallowed redirect target raises before the body is read), but the two checks are structurally duplicated rather than sharing one gate; a future edit to one predicate list without the other would silently reopen a gap. This is a maintainability observation, not a live exploitable defect today — both checks currently agree.
- `minimum_closure_condition`: none required now; the current behavior is fail-closed and tested indirectly via `test_live_probe_rejects_unanchored_subtitle_host_without_fetch`.
- `next_authorized_action`: no action needed; optional future refactor to have `_fetch_subtitle_webvtt`'s post-fetch check simply reuse the same guard already enforced by the redirect handler (already true) — recorded only so a future editor does not diverge the two checks.

## Adversarial Attack Results On The 8 Review-Focus Claims

1. **BATCH-01 provenance is code-backed, not label-string-backed.** Confirmed. `source_access_provenance.py` validates schema version, sha256 bindings, enum membership, and runs `assert_no_forbidden_source_access_material` (rejects cookie/token/proxy-endpoint/IP/path patterns) on every provenance payload at write and read time. `auth_state.py::validate_auth_state_provenance_requirement` fails closed (`ValueError`) on missing/legacy-only/mismatched sidecars before `live_batch_probe.py` reaches browser launch (`run_tiktok_live_batch_probe` line 337-343). A `noproxy`-style label alone cannot clear the gate; only a produced+validated sidecar field can.
2. **Interrupted-warmup regression coverage is real, not brittle.** In `fb078dd0`, `run_source_capture_cloakbrowser_profile_warmup.py` now calls `assert_browser_user_data_provenance_compatible` + `write_browser_user_data_provenance` **before** `warmup_engine.warm_profile(...)`. The new test `test_cloakbrowser_profile_warmup_binds_provenance_before_external_browser_action` uses a real `_FailingWarmupEngine` that raises mid-call, confirms the provenance sidecar is already durably written with the correct posture after the failure, then confirms a second warmup attempt on the same label with a *different* proxy profile is rejected by `assert_browser_user_data_provenance_compatible` before the engine is even invoked (`blocked_engine.user_data_dirs == []`). This is a genuine regression test on real code paths, not a tautology.
3. **Blocker typing/routing correctness, including `platform_challenge_observed` detail.** Confirmed. `blocker_triage.py::classify_tiktok_blocker` always attaches `matched_marker` and `challenge_kind` (via `_challenge_kind_from_text`) alongside the `platform_challenge_observed` reason string; `TikTokBlockerTriage.to_receipt()` serializes both fields when present. `test_live_probe_stops_on_platform_challenge` pins `matched_marker == "verify to continue"` and `challenge_kind == "slider"` on the same fixture, proving the kind is derived independently of which literal marker matched first. Intro/OK overlays, retry, and comment-route sequencing all match the playbook's named action substrate (`tiktok_dismiss_benign_overlay_pointer_v0`, `tiktok_retry_visible_error_pointer_v0`, the comments -> You-may-like -> comments double pass).
4. **Transcript/admission sanitization and rejection of owner-attention-as-clean-capture.** Confirmed. Subtitle capture only persists `body_sha256`, cue text/timing, and a `url_present_but_redacted` boolean — never a raw URL (`_sanitize_subtitle_infos`, `_subtitle_capture_from_item_struct`). `assert_no_sensitive_tiktok_material` runs on every row and the full payload before writing staging JSON. `batch_packet.py::_validate_staging_contracts` independently rejects (a) nonzero `challenge_count`, (b) any non-empty `failures`, (c) any completed row with `agent_may_solve_challenge=True`, `owner_attention_counts_as_clean_capture=True`, or `owner_attention_required`/`manual_challenge_attention_required=True`, and (d) any `human_challenge_handoff_attempts[*].captcha_solving_by_agent=True`. Verified against real fixture-based rejection tests (`test_tiktok_batch_rejects_agent_challenge_solving_receipt`, `test_tiktok_batch_rejects_owner_attention_clean_capture_claim`), not tautological assertions.
5. **Owner challenge handoff routing and non-clean-capture semantics.** Confirmed, and this is the file-scope of the reviewed patch. `_run_human_challenge_handoff` in `browser_snapshot.py` never programmatically manipulates the challenge: it polls page text, shows a Windows `MessageBoxW` (falling back to stdout print) and blocks until either the marker clears or the timeout elapses; it hard-codes `captcha_solving_by_agent: False` in its own receipt. In `live_batch_probe.py`, `_with_manual_challenge_attention_required` sets `owner_attention_required=True` unconditionally when a challenge is not accepted, with `owner_attention_route` distinguishing `harness_human_challenge_handoff_prompt` (handoff enabled) from `fail_closed_no_handoff_prompt` (handoff disabled) — both routes correctly set `agent_may_solve_challenge=False` and `owner_attention_counts_as_clean_capture=False`, and both are rejected by the admission gate regardless of route. The new test `test_live_probe_close_not_accepted_reports_handoff_prompt_route_when_enabled` pins the enabled-handoff route and all four non-clean-capture receipt fields.
6. **BATCH-04 cold-agent command and receipts.** Confirmed. `run_source_capture_tiktok_live_batch_probe.py --help` epilog (verified live via `--help` execution) exposes exactly the copyable command from the goal doc/runbook/README, including `--require-harness-proxy-posture no_proxy_profile_loaded`, `--allow-challenge-close-followthrough`, `--human-challenge-handoff`, and `--admit-output`; bronze `--data-root` requires an explicit flag value and the runner passes `DataLakeRoot.resolve(explicit=args.data_root)` — the ambient-`ORCA_DATA_ROOT`-fallback code path in `data_lake/root.py` is only reachable when `explicit` is `None`, which cannot happen on this call site once `--data-root` triggers the branch at all. `_staging_summary`/`_admission_summary` in the runner emit distinct typed `outcome` values (`staging_complete`, `owner_attention_required`, `fail_closed_*`, `local_packet_admitted`, `bronze_packet_admitted`, `fail_closed_admission_*`) with no secret fields.
7. **Failure visibility / no fake success.** Confirmed. No path sets `admitted_comment_response_count` or writes a completed `results[]` row while a challenge/owner-attention/close-not-accepted condition is active — all of those paths append to `failures[]` and `break` the loop instead. `write_auth_state_metadata`/export runner discard unbound state files on any exception (`_discard_unbound_state`). `main()` in the CLI runner catches `ValueError` and generic exceptions around the admission chain and prints a `fail_closed_admission_*` summary line plus a nonzero exit before re-raising via `parser.exit`, so admission-path failures cannot silently print a zero exit code.
8. **Test placement honesty.** Confirmed. All four target test files use `_FakeObservationEngine` / `_FakeWarmupEngine`-style fakes; no test opens a real browser or hits the network. `COMPLETE_LANE_NOTE` in `admission.py` explicitly states the SCI layer "enforces sanitized single-video and parsed-batch admission only" and does not claim live success. Goal doc, ADR, and capture-lane spec all carry explicit `non_claims` blocks (not validation, not readiness, not live capture success, not CAPTCHA-bypass authorization, not scale/account-safety proof) that were independently re-verified: an `rg` for `no_proxy_profile_loaded`/`full-network no-proxy egress` across the runner/docs turned up only the intended disclaimer text and no unqualified proof claim.

## Patch Summary

No patch was applied. The post-adjudication commit `fb078dd0` already implements
a correct, tested fix for both defects named in the review prompt (interrupted
CloakBrowser warmup provenance ordering; human-challenge-handoff route labeling
and non-clean-capture semantics). No bounded, in-scope defect was found in the
`bounded_patch_scope` file list that would justify a code change.

- Files changed: none.
- Diff summary: none (read-only review).
- Validation commands and observed results:
  - `python -m py_compile orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py orca-harness\runners\run_source_capture_cloakbrowser_profile_warmup.py orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py` -> exit 0, no output (clean compile).
  - `python -m pytest orca-harness\tests\unit\test_tiktok_live_batch_probe.py orca-harness\tests\unit\test_tiktok_blocker_triage.py orca-harness\tests\unit\test_tiktok_batch_admission.py orca-harness\tests\unit\test_source_capture_authenticated_browser_snapshot.py -q` -> exit 0; all collected tests passed (two dot-progress lines, `67%` then `100%`, no `F`/`E` markers).
  - `python orca-harness\runners\run_source_capture_tiktok_live_batch_probe.py --help` -> exit 0; help text printed, matches the documented cold-agent command in the runbook/README.
  - `python .agents\hooks\check_dcp_receipt.py --strict` -> `check_dcp_receipt --strict: OK -- every real receipt in the changed .md files is shape-valid (base: origin/main)`.
  - `python .agents\hooks\check_handoff_pointers.py --strict` -> `check_handoff_pointers --strict: OK (0 findings in 8 changed file(s) vs origin/main)`.
  - `git diff --check` -> exit 0, no output (no whitespace errors).
- Residual risks: the two minor findings above (diagnostic-field rollup gap; duplicated-but-currently-consistent redirect/final-host allowlist check). Neither is exploitable today and neither blocks merge.
- Off-scope flags: none. No defect was found requiring an edit outside `bounded_patch_scope`, and no doctrine/architecture change is implicated.

## Non-Claims

This review and its findings are decision input only. They are not approval,
validation, mandatory remediation, executor-ready patch authority, merge authority, account-safety proof,
no-proxy network proof, CAPTCHA-bypass proof, live TikTok success, scale
readiness, or readiness to merge until the home model adjudicates these
findings and required gates pass.

```yaml
review_summary:
  reviewed_by: Claude Sonnet 5 (Anthropic)
  authored_by: OpenAI/GPT-family Codex/GPT-5
  de_correlation_bar: cross_vendor_discovery
  de_correlation_status: satisfied
  target_commit: fb078dd08539c1392002dc0ca145a41a02656ddc
  recommendation: keep
  patches_applied: 0
  validation: >
    py_compile clean (exit 0); full four-file pytest suite passed (exit 0,
    all dots, no failures); runner --help exit 0 and matches documented
    cold-agent command; check_dcp_receipt --strict OK; check_handoff_pointers
    --strict OK; git diff --check clean (no whitespace errors).
  next_action: none; no patch required, home model may proceed to its own merge-readiness decision.
```
