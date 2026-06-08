# Data Capture Spine Reddit Candidate URL Intake Default Policy — Delegated Adversarial Review-and-Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Delegated adversarial review-and-patch result for the bounded Reddit Candidate URL Intake default-policy decision artifact.
use_when:
  - Adjudicating (Chief Architect) the delegated diff proposed against the Reddit Candidate URL Intake default-policy decision before anything is kept.
  - Checking the findings, citations, verdict, and residual risk from the de-correlated controller pass.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
input_hashes:
  target_sha256_at_review_start: 437BA729A30A00B75E0ADFA40669E1B106461C1608E77C49802904FE75A0D9B8
  target_sha256_after_patch: C3C24FF684DB3216FAE439DFDFFD39C9AAEFE9D6340A2B85BF14C6EBF104E507
branch_or_commit:
  branch: ecr-sp3-timing-deriver-slice1
  head: d857c581257ec74cc5eac8b53e7357556c2d1887
  target_git_state: untracked at review start
stale_if:
  - The Chief Architect accepts, modifies, or rejects the proposed diff (this report becomes a historical adjudication input).
  - The target default-policy decision, parent Candidate URL Intake contract, or Reddit Candidate URL Intake architecture changes after this review.
```

## 1. Commission And Receipt

Commission: Chief Architect delegated adversarial review-and-patch hardening pass on exactly one high-stakes authored artifact before owner acceptance, under the provisional Orca Delegated Review-and-Patch convention (`.agents/workflow-overlay/delegated-review-patch.md`).

- Target artifact (sole patch authority): `docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md`.
- Everything else: read-only / flag-only.
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`.

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex current lane
  controller_model_family: Anthropic / Claude Opus 4.8
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied
  de_correlation_basis: >
    Controller family (Anthropic) differs from author/home family (OpenAI/Codex).
    The non-Opus-delegate-for-Opus-author constraint is not triggered: the recorded
    author/home family is OpenAI/Codex, not Opus-class.
```

Pinned source state at prompt creation: branch `ecr-sp3-timing-deriver-slice1`, head `d857c58…`, target_sha256 `437BA729…D9B8`.
Observed at review start: hash matched the pin exactly; target untracked (`??`) in the working tree, consistent with the prompt's dirty-state allowance. No `BLOCKED_TARGET_UNAVAILABLE`, no `BLOCKED_SOURCE_REVISION_MISMATCH`.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

Source-read ledger (controlling + grounding):

| Source | Why read | Supports | Git state |
| --- | --- | --- | --- |
| `docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md` | Review target | All findings | untracked; hash pinned/matched |
| `docs/product/data_capture_spine_candidate_url_intake_contract_v0.md` | Parent contract (caps/surfaces/promotion/traversal authority) | AR-01, AR-04 | tracked (read clean in tree) |
| `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md` | Reddit specialization (allowlist-and-cap rule, Next Authorized Step) | AR-01, AR-02 | tracked |
| `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` | CloakBrowser/proxy + commercial-reroute authority | Access-method check (held) | tracked |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Routing/coherence of the default-policy area | Coherence check (held) | modified in tree (advisory only) |
| `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md` | Adjacent Reddit success-signal posture | Non-conflict check (held) | tracked |
| Overlay authority: `AGENTS.md`, `.agents/workflow-overlay/{README,decision-routing,source-of-truth,source-loading,retrieval-metadata,artifact-roles,review-lanes,delegated-review-patch,prompt-orchestration,validation-gates,communication-style}.md` | Authority, lane, patch scope, output binding | Whole review | overlay read in task context |

Dirty/unanchored note: the Data Capture sub-map is modified in the working tree; it was used only for advisory coherence, and no strict claim in this report depends on it. The target itself is untracked but hash-pinned and matched, so review provenance is anchored.

Method sequence honored: `REFERENCE-LOAD` of `workflow-deep-thinking` and `workflow-adversarial-artifact-review` preceded analysis; `APPLY` followed the `SOURCE_CONTEXT_READY` declaration. `workflow-adversarial-artifact-review` was available and applied — no `BLOCKED_REVIEW_LANE_UNAVAILABLE`.

Output binding: `filesystem-output`, `required_output_path` = this file (commission-bound). No `BLOCKED_OUTPUT_MODE_MISSING` / `BLOCKED_OUTPUT_DESTINATION_UNBOUND`.

## 3. Cynefin Routing Result

- Smallest complete outcome: harden only the target default-policy decision and write this report.
- Regime: complicated.
- Decomposition: layer-based with adversarial boundary checks.
- Current bottleneck: preventing the defaults from silently authorizing broad Reddit crawling, same-run expansion, capture, packet output, auto-promotion, monitoring-without-frame, or implementation/commercial use — while staying complete enough for no-live-access scoping.
- Riskiest assumption: the default caps/surfaces/outbound/continuation rules are complete enough for no-live-access scoping without being mistaken for sufficiency, coverage, or runtime authorization.
- Stop/pivot: if a defect were design-level across the parent contract or Reddit architecture rather than patchable inside the target, return `NEEDS_ARCHITECTURE_PASS` and do not patch.
- Result: all three material defects are within the default-policy artifact's own remit and patchable in-target. `NEEDS_ARCHITECTURE_PASS` not triggered. Allowed next move taken: review and patch only the target.

## 4. Findings (severity order)

No `critical` findings. The artifact is heavily disclaimed and routes every downstream action through a promotion gate plus separate authorization; no clause directly authorizes a forbidden action (live capture, packets, broad crawl, monitoring-without-frame, commercial use). The material defects are boundary-relaxation and completeness issues at `major`/`minor`.

### AR-01 — major — correctness/boundary — PATCHED

- Phase: correctness.
- Location: `## Default Candidate Surfaces` (default-on list + the "Default-off does not mean forbidden" paragraph); cross-reference `## Default Run Modes And Caps` table.
- Issue: the target makes the cross-post and related-subreddit discovery surfaces **default-on**, but supplies **no default cap** for the candidate rows they produce, and scopes the "must … set a surface-specific cap" obligation only to *default-off* surfaces — leaving default-on discovery surfaces cap-unspecified and relaxing the parent architecture's allowlist-and-cap rule.
- Source authority / evidence:
  - Reddit architecture: candidate subreddit rows "may come from declared Reddit search/listing surfaces, cross-post surfaces, recommendation surfaces, related-subreddit surfaces, or 'more like this' surfaces **only when that surface is named in `candidate_surface_allowlist` and capped before the run**."
  - Parent contract, Candidate Surfaces And Traversal: "Candidate surfaces **must be allowlisted and capped before the run**." Source-family artifacts "must not remove the parent … cap semantics … or no-same-run-traversal rule."
  - Target cap table caps subreddits / threads-per-subreddit / pages / window only — no cap for cross-post or related-subreddit candidate rows.
- Impact: a default-on discovery surface with no default numeric cap permits unbounded candidate-row enumeration of related subreddits / cross-posts by default — the single closest path by which the defaults could drift toward open-ended discovery — and removes the parent's allowlist-and-cap guard for exactly those surfaces. It also leaves ambiguous whether `Default max subreddits` bounds discovered subreddits or only seeds. (Same-run traversal remains forbidden everywhere, so the leak is enumeration breadth and parent-rule relaxation, not entry.)
- minimum_closure_condition: cross-post and related-subreddit surfaces are either moved to default-off (allowlist + surface cap required), or kept default-on but explicitly bound to a cap and treated as default-allowlisted-and-capped, so the parent's "named in allowlist and capped" requirement is no longer relaxed; and it is explicit whether the global subreddit cap bounds discovered subreddits.
- Patch applied: kept the author's default-on intent (lowest lock-in) and bound the default-on discovery surfaces to the existing global caps (no new numeric policy invented) — discovered candidate subreddit rows count against `Default max subreddits`; cross-post/related candidate thread rows count against `Default max threads per subreddit` and `Default max pages/result surfaces`; states they are default-allowlisted-and-capped; reinforces no same-run traversal.
- next_authorized_action: Chief Architect adjudication — accept the cap-binding as written, or choose default-off, or set distinct per-surface numeric caps (a policy number choice reserved to the owner).
- Strict claims not proven: that the chosen cap binding is the owner's intended numeric policy (owner decision).

### AR-02 — major — correctness/boundary — PATCHED

- Phase: correctness.
- Location: `## Implementation-Scoping Gate`, opening sentence.
- Issue: the gate authorizes no-live-access scoping "after owner acceptance of **this default policy**" alone, omitting the parent-acceptance preconditions the Reddit architecture requires before any implementation scoping.
- Source authority / evidence:
  - Reddit architecture, Next Authorized Step: "Implementation scoping is not allowed from this artifact alone. A future implementation lane requires: 1. owner acceptance of this architecture contract; 2. owner acceptance of the Reddit Candidate URL Intake default-policy decision; …"
  - Parent contract, Next Authorized Step: requires owner acceptance of the parent contract and the accepted source-family specialization before an implementation lane.
  - Both parent artifacts are currently `TARGET_RECOMMENDED` (pending acceptance).
- Impact: reading only the target, a scoper could begin no-live-access scoping once the default policy alone is accepted, while the parent architecture (and parent contract) remain unaccepted or in flux — under-conditioning the highest-stakes gate in the artifact.
- minimum_closure_condition: the implementation-scoping gate names the upstream acceptances the parent architecture requires (at minimum the parent Candidate URL Intake contract and the Reddit Candidate URL Intake architecture) in addition to this default policy.
- Patch applied: the gate now reads "After owner acceptance of this default policy **and of the parent Candidate URL Intake contract and Reddit Candidate URL Intake architecture that this decision specializes**, no-live-access implementation scoping may proceed for: …".
- next_authorized_action: Chief Architect adjudication of the added precondition.
- Strict claims not proven: none beyond owner acceptance, which the artifact already disclaims.

### AR-03 — major — correctness/boundary — PATCHED

- Phase: correctness.
- Location: `## Promotion Receipt Ownership`, receipt field list.
- Issue: the operator-owned promotion receipt may exist before any Decision Frame and records a "selected downstream capture method" and "approved downstream access route," with "Decision Frame … if present" (i.e., optionally absent). The guard that it is planning-only and grants no capture authority lives only in surrounding prose, not as a field of the receipt — so a receipt that travels or is excerpted without that prose is the artifact's most mistakable-for-authorization object.
- Source authority / evidence:
  - Parent contract promotion gate requires recording "Decision Frame or approved capture-unit authority," "confirmation that Source Capture Armory execution has not happened yet," and "known limitations from the intake provenance receipt."
  - Target prose: "Before that point, the receipt is planning context only" and "Promotion does not authorize capture, packet generation, body/comment fetch …" — correct, but not part of the receipt schema itself.
- Impact: the seam where promotion could be read as capture authorization is held only by adjacent prose; the prompt's own review criteria flag auto-promotion / capture-authority leakage and using approved access routes as execution authority as top failure modes.
- minimum_closure_condition: the non-authorization boundary travels as a required field of the promotion receipt, so the receipt cannot be read as capture/access authorization on its own.
- Patch applied: added a required field `capture_not_yet_authorized: yes` stating the receipt is planning context only and is not capture, packet, body/comment/profile, Source Capture Armory, or source-access authorization, and confers no access until a Decision Frame or approved capture-unit authority accepts the unit.
- next_authorized_action: Chief Architect adjudication; CA may judge the existing prose sufficient and veto, or keep the field.
- Strict claims not proven: none.

### AR-04 — minor — correctness/completeness — PATCHED

- Phase: correctness.
- Location: `## Promotion Receipt Ownership`, receipt field list.
- Issue: the operator promotion receipt omitted the parent promotion gate's required "known limitations from the intake provenance receipt" field; a source-family artifact "must not remove the parent … promotion gate" fields.
- Source authority / evidence: parent contract promotion gate field list includes "known limitations from the intake provenance receipt."
- Impact: a promoted unit could lose the originating run's recorded limitations (caps, coverage_claim, empty/blocked/capped posture) at the promotion boundary, weakening downstream honesty about what the candidate set does and does not represent.
- minimum_closure_condition: the receipt records the known limitations carried from the originating run's provenance receipt (or explicitly states none).
- Patch applied: added a field "known limitations carried from the originating run's provenance receipt (declared caps, `coverage_claim`, and any empty/blocked/capped stop reason)."
- next_authorized_action: Chief Architect adjudication.
- Strict claims not proven: none.

### AR-05 — minor — friction/clarity — NOT PATCHED (residual)

- Phase: friction.
- Location: `## Default Run Modes And Caps`, `high_recall_pass` row.
- Issue: the label `high_recall_pass` could be read by a hasty operator as a recall achievement rather than an attempt.
- Why not patched: the closed `coverage_claim` token is `high_recall_attempt_with_limits` (an attempt, not achievement), and the Decision section already states "No cap is evidence of … high recall by itself." Renaming the enum is out of scope and would conflict with the parent contract and Reddit architecture, which both define `high_recall_pass` / `high_recall_attempt_with_limits` as the closed enum. Deliberately left as residual rather than introducing a cross-artifact vocabulary conflict.
- next_authorized_action: none required; owner may note the residual.

## 5. Unified Diff (target file only)

The target is untracked, so `git diff` renders it as a new-file add; the three focused hunks below are the substantive changes this pass made (verified present in the working tree; post-patch sha256 `C3C24FF6…E507`).

```diff
--- a/docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
+++ b/docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
@@ ## Default Candidate Surfaces @@
 Default-off does not mean forbidden. It means the operator must declare the
 surface in `candidate_surface_allowlist`, set a surface-specific cap, and accept
 that same-run traversal remains forbidden.
+
+Default-on does not mean uncapped or exempt from the parent allowlist-and-cap
+rule. The default-on cross-post and related-subreddit surfaces are treated as
+default-allowlisted and remain capped: discovered candidate subreddit rows count
+against `Default max subreddits`, and cross-post or related candidate thread rows
+count against `Default max threads per subreddit` and `Default max
+pages/result surfaces`. An operator may set a tighter surface-specific cap but
+may not exceed these caps without a scope amendment or later owner decision.
+Producing a candidate row for a discovered cross-post or related subreddit never
+authorizes same-run traversal into it; entering it requires a new `run_id` or an
+explicit scope amendment.
@@ ## Promotion Receipt Ownership @@
 - exact promoted URL;
 - originating `run_id`;
 - candidate row pointer;
 - reason for promotion;
+- known limitations carried from the originating run's provenance receipt
+  (declared caps, `coverage_claim`, and any empty/blocked/capped stop reason);
 - selected downstream capture method or method family;
 - approved downstream access route if already source-backed;
 - Decision Frame or approved capture-unit authority, if present;
 - non-promotion of non-selected candidate rows;
-- confirmation that Source Capture Armory execution has not happened yet.
+- confirmation that Source Capture Armory execution has not happened yet;
+- `capture_not_yet_authorized: yes` — the receipt is planning context only and
+  is not capture, packet, body/comment/profile, Source Capture Armory, or
+  source-access authorization; it confers no access until a Decision Frame or
+  approved capture-unit authority accepts the promoted unit.
@@ ## Implementation-Scoping Gate @@
-After owner acceptance of this default policy, no-live-access implementation
-scoping may proceed for:
+After owner acceptance of this default policy and of the parent Candidate URL
+Intake contract and Reddit Candidate URL Intake architecture that this decision
+specializes, no-live-access implementation scoping may proceed for:
```

## 6. Per-Change Citations (neutral)

- AR-01 cap-binding: Reddit architecture, candidate subreddit row note — surfaces are usable "only when … named in `candidate_surface_allowlist` and capped before the run." Parent contract, Candidate Surfaces And Traversal — "Candidate surfaces must be allowlisted and capped before the run"; Source-Family Specialization Requirements — source-family artifacts "must not remove the parent … cap semantics … or no-same-run-traversal rule." Target cap table enumerates caps for subreddits, threads-per-subreddit, pages, and window only.
- AR-02 gate precondition: Reddit architecture, Next Authorized Step — implementation scoping "requires: 1. owner acceptance of this architecture contract; 2. owner acceptance of the Reddit Candidate URL Intake default-policy decision." Parent contract, Next Authorized Step — requires owner acceptance of the parent contract and the source-family specialization. Both parents carry `Status: TARGET_RECOMMENDED`.
- AR-03 non-authorization field: Parent contract, Promotion Gate — receipt "must record … confirmation that Source Capture Armory execution has not happened yet." Target prose — "Before that point, the receipt is planning context only" / "Promotion does not authorize capture …" (present in surrounding text, not in the receipt field list).
- AR-04 known-limitations field: Parent contract, Promotion Gate — receipt "must record … known limitations from the intake provenance receipt."

## 7. Verdict (relative to the commissioned target)

`patch_before_acceptance`. The target is a sound, well-disclaimed default-policy decision; three material boundary findings (AR-01, AR-02, AR-03) and one completeness finding (AR-04) were patched in-target to close a discovery-surface cap gap that relaxed the parent rule, to align the implementation-scoping gate with the parent-acceptance preconditions, and to make the no-capture-authority boundary travel with the promotion receipt. No design-level defect was found; `NEEDS_ARCHITECTURE_PASS` not triggered. The diff and this verdict are decision input for Chief Architect adjudication, not owner acceptance.

## 8. Residual-Risk Note

- AR-05 (label connotation of `high_recall_pass`) is left unpatched by design; the closed coverage token and the explicit no-recall disclaimer mitigate it, and renaming would conflict with the parent enum.
- The AR-01 cap-binding reuses the existing global caps rather than inventing per-surface numeric caps; if the owner wants distinct numeric ceilings for discovery surfaces, that is a separate owner number choice not made here.
- Doctrine-propagation refresh is deferred to acceptance: this delegated pass changed doctrine-bearing body text (a `product_doctrine` artifact) but is a *proposed* diff, not a committed/accepted change. The target's existing `direction_change_propagation` receipt was intentionally left untouched and is **not** re-run for the new clauses. If the Chief Architect keeps any of these clauses, the CA must refresh that receipt's `doctrine_changed` and re-run the `stale_language_search` to cover the added cap-binding, gate precondition, and promotion-receipt fields before any completion/acceptance claim. This report makes no validation, readiness, or acceptance claim.
- The target remains untracked; nothing here was staged or committed.

## 9. Off-Scope Flags

- None requiring another file's edit. The patches are wholly inside the commissioned target. The parent Candidate URL Intake contract and Reddit Candidate URL Intake architecture are internally consistent with the patched target and need no change for these findings; the AR-02 alignment was a defect in the target's restatement of the parent precondition, not in the parents.
- No live Reddit, CloakBrowser, proxy, packet-runner, browser-snapshot, storage, scheduler, dashboard, ECR, Cleaning, Judgment, fixture-admission, or source-quality path was invoked.

## 10. Review-Use Boundary

These findings, the diff, the citations, the verdict, and the residual-risk note are decision input for Chief Architect / home-model adjudication only. They are not owner acceptance, validation, readiness, implementation authorization, source-access boundary amendment, or automatic promotion. The Chief Architect decides what is kept and may accept, modify, or reject each change.

---

```text
DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Adjudicate under the delegated-review-patch return contract (.agents/workflow-overlay/delegated-review-patch.md).

- Original commission: harden the single artifact docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md before owner acceptance; patch authority for the target file only; everything else flag-only.
- Reviewed artifact + bounded patch scope: the target default-policy decision; three in-target patches (Default Candidate Surfaces cap-binding; Implementation-Scoping Gate precondition; Promotion Receipt Ownership two added fields).
- De-correlation: satisfied (controller Anthropic vs author/home OpenAI/Codex; non-Opus-author, so no non-Opus-delegate constraint triggered).
- Findings: AR-01 major (default-on discovery surfaces uncapped + parent allowlist-and-cap relaxation) PATCHED; AR-02 major (implementation-scoping gate under-conditioned vs parent acceptances) PATCHED; AR-03 major (promotion receipt could read as capture authority; guard was prose-only) PATCHED; AR-04 minor (receipt omitted parent's known-limitations field) PATCHED; AR-05 minor (high_recall_pass label connotation) NOT PATCHED / residual.
- Proposed patch: see the unified diff (Section 5); target post-patch sha256 C3C24FF684DB3216FAE439DFDFFD39C9AAEFE9D6340A2B85BF14C6EBF104E507.
- Citations: Section 6 (neutral, parent contract + Reddit architecture).
- Reviewer verdict: patch_before_acceptance; NEEDS_ARCHITECTURE_PASS not triggered.
- Residual risk: AR-05 left by design; AR-01 reuses global caps (numeric per-surface caps are an owner choice); the target's direction_change_propagation receipt must be refreshed by the home model at acceptance for the added clauses; target untracked, nothing staged/committed.
- Blockers / off-scope / not-proven: no blockers; no off-scope edits; not validation, not readiness, not owner acceptance, not implementation authorization, not live-access/CloakBrowser/proxy/packet authorization.
- Next action: Chief Architect adjudication of the delegated diff before anything is kept.
```
