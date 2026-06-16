# Demand-Durability Series Writer (Step 2) — Cross-Vendor Adversarial Code Review + CA Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (cross-vendor adversarial code review + home-model adjudication record)
scope: >
  Records the no_repo cross-vendor adversarial code review of the demand-durability series writer
  (PR #128) and the CA's home-model adjudication of its 3 findings + the applied bounded patch.
  Decision input only — not validation, readiness, a formal review-lane verdict, or merge authority.
authority_boundary: retrieval_only
branch_or_commit: demand-durability-series-writer-step2 (reviewed @ a0b22531 → patched @ b8939840)
reviewed_by: OpenAI GPT-5 Codex (exact runtime version unrecorded)
authored_by: Anthropic Claude / exact model unrecorded (the step-2 build lane)
de_correlation_bar: cross_vendor_discovery
use_when:
  - Checking how the cross-vendor code review of the step-2 writer was adjudicated and what was kept.
  - Tracing the PR #128 input-validation hardening back to its review findings.
stale_if:
  - PR #128 is re-reviewed, materially re-patched, or merged.
  - A finding's adjudication is reopened by the owner.
```

## Commission

- Lane: delegated review-and-patch (`provisional_opt_in`); access `no_repo`; mode base-subagent; review lane **code** (`workflow-code-review`).
- Target: PR #128 (`demand-durability-series-writer-step2`) reviewed @ `a0b22531`; bundle `docs/review-inputs/step2_series_writer_no_repo_adversarial_code_review_bundle_v0/`; wrapper `docs/prompts/wrappers/step2_series_writer_no_repo_adversarial_code_review_wrapper_v0.md`.
- Reviewer confirmed all 4 attachment hashes MATCH; `cross_vendor_discovery`; advisory no-repo (`workflow-code-review` reference-loaded; no formal verdict).

## Reviewer findings (verbatim summary)

- Critical: none.
- **Major 1** — partial cadence flags silently discarded (`_build_intended_cadence` returns `None` without `--intended-cadence-mode` even when other cadence flags are set → false-success packet).
- **Major 2** — CLI permits incoherent partial demand-durability packets (durability fields all independently optional; `series_id`-less durability facts possible).
- **Minor 1** — the two new tests don't prove the false-success boundaries (no negative coverage).
- Off-scope flags: `models.py`/`packet_assembly.py`/`cadence.py`/`build_optional_fact` not loaded (no-repo boundary); no INV-1 smuggling or Element-3 found in the 3 attached files.

## CA adjudication (claims to adjudicate, not premises to inherit)

All three findings **verified real against the actual code** before adjudication (the reviewer was repo-blind). Verdict + remedy:

| Finding | Verdict | Remedy kept |
| --- | --- | --- |
| **Major 1** | **Accept** — a fake-success path (AGENTS kernel: "never create fake success paths") | `_build_intended_cadence` raises `ValueError("cadence flags require --intended-cadence-mode")` when any of the 6 cadence subflags is set without mode; `None` only when mode-absent and no subflag → exit 2 (visible). |
| **Major 2** | **Accept, MODIFIED** | New `_require_series_identity` gate: any durability field set ⇒ `--series-id` required (the identity anchor Ob.17 names), failing fast before capture. **Rejected the reviewer's "require Element-1 pin facts" closure** — Ob.17 says an absent pin is `unknown_with_reason`/`not_applicable`/`unavailable_by_source`, *never written as a fact*, so requiring pins-as-facts would violate Ob.17. Pins stay honest-gappable; bare `--series-id` stays permitted. |
| **Minor 1** | **Accept** | Two negative subprocess tests added (cadence subflag without mode → non-zero + error; durability field without `series_id` → non-zero + error); the two existing tests unchanged. |

No finding rejected on substance; one closure condition (Major 2's pins-as-facts) modified for Ob.17 conformance. **No `NEEDS_ARCHITECTURE_PASS`** — runner-level input validation, within the 2 bounded files.

## What was kept (final state)

Patch commit `b8939840` on PR #128: `run_source_capture_http_packet.py` (+73, the two gates) and `test_source_capture_direct_http.py` (+65, two negative tests). `writer.py`, `models.py`, and `SOURCE_CAPTURE_MANIFEST_VERSION` untouched. Additive input-validation only; INV-1 preserved.

## Post-patch recheck (bounded; same-vendor sanity)

- `de_correlation_bar` for the recheck: **`same_vendor_sanity`** (the CA, Anthropic, verified its own/the lane's patch; bounded verification, not a cross-vendor discovery / no-new-seam claim).
- Result (verified against primary source): PR #128 HEAD = `b8939840`; diff scope = the 2 bounded files only; both gates present and correct; both negative tests present; INV-1 preserved (input-coherence only). Suite: **865 passed / 2 skipped** (863 + 2 new), reported by the patch lane via JUnit XML (the `-q` summary line did not flush to redirected stdout on this Windows/pytest setup). No new blocker/major in the touched delta.

## Residual risk / not-proven

- This review is advisory; neither pass ran independent of the bundle. `models.py` / `packet_assembly.py` / `cadence.py` / `build_optional_fact` behavior was carried in as authority, not independently re-proven by the cross-vendor reviewer (no-repo boundary).
- The suite-green claim rests on the patch lane's observed JUnit XML, not a CA re-run; the CA independently verified the code diff, gate logic, and test presence.
- PR #128 merge stays **owner-gated**. A novel cross-vendor-shared blind spot absent from both passes remains bounded-but-nonzero.

## operator_closeout_source

```yaml
operator_closeout_source:
  what_ran: cross-vendor (OpenAI GPT-5 Codex) no_repo adversarial code review of PR #128 (demand-durability series writer).
  reviewer_findings: 0 critical, 2 major, 1 minor — all input-coherence / failure-visibility; verified real.
  ca_adjudication: all 3 accepted; Major 2 closure modified to respect Ob.17 (pins stay honest gaps, not required facts); not an architecture pass.
  applied: patch b8939840 — visible-fail on partial cadence (Major 1), series-id-required coherence gate (Major 2), 2 negative tests (Minor 1); 2 files, +136/-2; no schema/manifest change; INV-1 preserved.
  recheck: same_vendor_sanity bounded recheck passed; closure verified against primary source; suite 865/2.
  final_state: PR #128 OPEN @ b8939840, hardened; merge owner-gated.
  blocked_next_step: owner merge of PR #128; then step 3 (cadence runner) may begin.
  not_claimed: validation, readiness, merge, no-new-seam, CA-independent suite re-run.
```

## Non-Claims

Decision input only. Not validation, readiness, formal `PASS`, proof the review ran, a no-new-seam claim, patch authority beyond the bounded CA-adjudicated application recorded here, merge authority, or runtime model routing. PR #128 landing to `main` stays owner-gated.
