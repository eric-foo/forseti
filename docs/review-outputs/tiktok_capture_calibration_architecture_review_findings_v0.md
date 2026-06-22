# TikTok Capture Calibration Architecture — Delegated Adversarial Review Findings & CA Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Findings and Chief-Architect adjudication of a de-correlated, different-vendor adversarial artifact review-and-patch (repo mode) of the TikTok capture calibration architecture/scoping memo.
review_type: delegated_adversarial_artifact_review_repo_mode
review_date: 2026-06-21
target: docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md
target_sha256_pre_review: 4AA2330A7B8D5BD06AED020AA881669A052A79B10E5E33EADFB20598BFC411FB
target_sha256_post_delegate_patch: 157A5397D16CDBE7BFEBA9BE8FA403B753382F9D4F825EE9BA20A8B7F6269412
authored_by: Claude Opus 4.8 (Anthropic)
reviewed_by: unrecorded (non-Anthropic delegate, repo mode; operator did not record model+version — visible measurement gap, not a captured cross-vendor measurement)
adjudicated_by: Claude Opus 4.8 (Anthropic; commissioning Chief Architect / home model)
access_mode: repo
de_correlation: cross-vendor (author Anthropic vs delegate non-Anthropic) per operator dispatch; delegate vendor unrecorded, so the cross-vendor *discovery* bar is asserted by operator dispatch but not independently provable from this record
authority_boundary: retrieval_only
```

---

## Summary

A de-correlated, different-vendor delegate ran a repo-mode adversarial artifact review of the TikTok capture calibration memo and left a bounded patch in the working tree (only the target memo touched; `git status` clean otherwise). It returned six `major` findings (AR-01..AR-06), no `NEEDS_ARCHITECTURE_PASS`.

**CA decision: all six findings ACCEPTED on substance.** Every on-disk edit is accurate, in-scope, and *honest-down* (it tightens claims and adds residuals; it introduces no new overclaim or false-success path). On independent fresh-read verification, every load-bearing citation the delegate wrote **into** the memo holds. The patched memo is kept.

Two classes of caveat are recorded below: **delegate report-fidelity defects** (which do **not** touch the durable artifact) and a **prompt defect of my own** (a self-contradiction the delegate correctly surfaced).

## Findings and adjudication

All six were verified against source and accepted; the edits are live in the target memo.

- **AR-01 — stale joint IG/TikTok recon claim (major). ACCEPTED.** §2(b) now distinguishes the older playbook framing (`source_capture_playbook_v0.md:288-290`, `:47-49`) from the fresher recon index, which records **Instagram now probed / TikTok no recon** (`capture_recon_index_v0.md:166-173`). CA re-verified both citations; accurate.
- **AR-02 — comment-window precision could fabricate buckets (major). ACCEPTED.** §3 now requires a source-native timezone/epoch/clock basis (not just "sufficient granularity"), and explicitly rejects date-only, relative-age ("2d ago"), locale-only, and mixed-granularity values → `not_applicable`/`unavailable_with_reason`. This hardens the single highest data-integrity trap. Anchored to `ig_capture_shape_contract_spec_v0.md` typed-posture rule + `source_capture/models.py:128-137`; verified.
- **AR-03 — official TikTok API row absent (major). ACCEPTED.** §4 adds Route 7 "Official TikTok APIs" as `CATALOG / OUT-OF-BAND` (Display = user-authorized/self-content; Research = application/eligibility-gated; commercial Orca use likely ineligible), plus a §7 residual. Consistent with external 2026 API facts (probe-time-verifiable, labeled non-architecture-fact). No client secrets/tokens in packets. Accepted as catalog evidence, not a proven route.
- **AR-04 — reuse-map over-stated portability / fixed "four files" (major). ACCEPTED.** §5 drops the rigid four-file promise ("roughly four to five code files plus spec + tests, count contingent on the route"), gates the browser adapters/`auth_state` behind route confirmation, and qualifies the projection as a per-platform satellite. Citations `source_capture/models.py:128-137,:154-158`, `ig_projection.py:25-33,:150-159` re-verified.
- **AR-05 — identity stability implied before proof (major). ACCEPTED.** §3 adds "identity-incomplete" posture and marks stable native user/video/comment ids as `HYPOTHESIS_FOR_PROBE`; §7 adds a TikTok-identity-semantics residual. `models.py:128-137,:154` names the numeric-id identity anchor + conflict-policy as the per-platform satellite — supports the finding.
- **AR-06 — internal-API route boundary too loose (major). ACCEPTED.** §4 Route 4 now restricts to "same-origin, page-emitted requests that work logged-out without invented auth headers/tokens" and forbids replaying a private/signed API. Aligned with `source_capture_playbook_v0.md:64-68,:191`.

## Delegate report-fidelity defects (recorded; do NOT affect the kept artifact)

These are defects in the delegate's **chat report**, not in the patched memo:

1. **Pasted unified diff does not match the real artifact.** The delegate's chat diff references sections that do not exist in the target memo ("Source facts verified:", "Consequence for this memo:", "Proposed lane contract:", a numbered 1–8 route table, "## 5. Reuse Map From IG / Harness"). The actual on-disk memo retains its real structure (§3 TARGET_CAPTURE_SHAPE, §4 ROUTE_OPTIONS, §5 SMALLEST_COMPLETE_PATCH_SEQUENCE, §6 LIVE_PROBE_GATE, §7 NON_CLAIMS) with smaller inline edits. Adjudication was therefore done against the **real on-disk delta** (fresh read), not the pasted diff.
2. **Wrong file paths in some findings citations.** The delegate cited `orca-harness/runners/source_capture/run_source_capture_ig_calls_packet.py` and `orca-harness/tests/test_source_capture_ig_*.py`. The real paths are `orca-harness/runners/run_source_capture_ig_calls_packet.py` and `orca-harness/tests/unit/test_source_capture_ig_*.py` (confirmed by Glob). **The memo body uses the correct paths**, so the artifact is unaffected; only the chat-report citations were wrong.
3. **Minor line-number drift** (±2 lines) on a few citations; substance correct in every case checked.

Net: the delegate's *patching* and *in-memo citations* were sound; its *self-report* (diff rendering + a subset of chat citations) was unreliable. Because this was a `repo`-mode pass, the CA could and did verify against source rather than trust the report — which is exactly the point of repo mode.

## Prompt defect (mine), correctly surfaced by the delegate

My commission contradicted itself: the output contract asked the delegate to "also write a durable findings report," while the hard constraints said "Patch ONLY the target memo … everything else read-only/flag-only." The delegate flagged the conflict and chose the conservative reading (it did not write a second file). That was correct scope discipline. This durable findings report is therefore written by the CA (home model), which holds the authority the delegate's bounded scope did not.

## CA closure verification (repo-mode discharge)

Independently fresh-read and confirmed: `capture_recon_index_v0.md:166-173`; `source_capture_playbook_v0.md:288-290`; `source_capture/models.py:128-137,:154-163`; `ig_projection.py:25-33`; and the corrected IG runner/test paths via Glob. The touched delta introduces no new `blocker`/`major`: every edit lowers or equalizes claim strength. The one non-independent sliver (the delegate's own edited lines) was mechanically re-checked against the cited sources.

## Final kept state

- Target memo `docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md`: **patched and kept**, all six findings folded in; header provenance updated by the CA to record the hardening pass (so the memo no longer claims "no patches applied").
- No other source files edited. No commit, no push. Working tree carries the two session artifacts plus this findings report and the review prompt.

## Validation evidence and gaps

- **Evidence:** source-loading + citation re-verification (fresh reads above); Glob path confirmation; pre/post hashes recorded; working-tree status clean of out-of-scope edits.
- **Not run:** no code tests (doc-only adversarial patch — correct; the memo is a planning artifact, not code).
- **Gap:** `reviewed_by` is `unrecorded` — the operator did not state the delegate's model+version, so the cross-vendor *discovery* bar is asserted by dispatch but not provable from this record. A present `unrecorded` is a visible measurement gap, not a captured measurement.

## Residual risk (unchanged by this pass — the memo still proves none of it)

No TikTok route is proven; official-API eligibility/scope is unproven and time-sensitive; comment timestamps, stable identity semantics, metric semantics, anti-bot survivability, legal/ToS posture, and public-web-vs-mobile-only availability all remain probe-time unknowns. This pass improved the memo's honesty and boundaries; it did not advance feasibility. The memo grants no capture/build authority and asserts no validation or readiness.
