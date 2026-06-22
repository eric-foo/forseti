# TikTok Capture Calibration Architecture — Delegated Adversarial Artifact Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: Commission a de-correlated, different-vendor adversarial artifact review-and-bounded-patch (repo mode) of the TikTok capture calibration architecture/scoping memo; CA (home model) adjudicates the working-tree diff before keep.
use_when:
  - A repo-access, non-Anthropic coding agent in this worktree is commissioned to verify-and-patch the TikTok calibration memo.
authority_boundary: retrieval_only
review_type: delegated_adversarial_artifact_review_repo_mode
access: repo
dispatch_mode: external-controller-courier
output_mode: review-report
edit_permission: patch-only
patch_scope: docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md (the single target memo; everything else read-only / flag-only)
durable_report_destination: docs/review-outputs/adversarial-artifact-reviews/tiktok_capture_calibration_architecture_review_findings_v0.md
target: docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md
target_sha256: 4AA2330A7B8D5BD06AED020AA881669A052A79B10E5E33EADFB20598BFC411FB
authored_by: Claude Opus 4.8 (Anthropic)
reviewed_by: unrecorded   # operator/CA sets to the actual non-Anthropic reviewer model+version on the durable findings record
```

---

## Operator dispatch instruction (de-correlation who-constraint)

Run this prompt in a **non-Anthropic** coding agent that has read/write access to **this worktree** (for example an OpenAI/GPT-based or Google/Gemini-based agent — Codex, Gemini CLI, Cursor on a non-Claude model, etc.). **Do not** run it in a Claude / Anthropic agent — the memo was authored by Claude Opus 4.8, and a same-vendor reviewer defeats the de-correlation that is the entire point of this pass. Model families are named only to express the difference constraint; this is not a model-quality ranking or a runtime-model recommendation.

Repo preflight the delegate must confirm before any edit:

- worktree: `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\brave-maxwell-69cf0f`
- branch: `claude/brave-maxwell-69cf0f` (off `main`); base recent commit `6f79445e`
- dirty-state: tree was clean except for the two artifacts authored this session (the target memo and this prompt); the delegate may modify **only** the target memo
- target file: `docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md`, SHA256 `4AA2330A7B8D5BD06AED020AA881669A052A79B10E5E33EADFB20598BFC411FB` — confirm this matches before reviewing; if it does not match, declare `SOURCE_CONTEXT_INCOMPLETE` and stop (do not review a drifted copy)
- **edit only the target memo. Do not commit, do not push, do not stage.** Leave the patched memo in the working tree for the commissioning Chief Architect (Anthropic home model) to adjudicate hunk-by-hunk before anything is kept.

## You are

A de-correlated adversarial reviewer **with repo access**, commissioned to review **and bounded-patch** a single Orca planning artifact: an architecture/scoping memo designing (not building) a TikTok public creator/video/comment capture calibration lane for anti-bot / data-integrity analysis. The memo is read-only **planning** (no code, no live TikTok, no implementation). Your job is to attack it for material defects, verify its claims against the actual repo, and patch the memo within scope — before Orca relies on it to commission a live probe.

Because you have repo access, you must do what a repo-blind reviewer could not: **verify the memo's `path:line` citations and its code-reuse claims against the actual source**, and correct or flag any that are wrong, stale, or overstated.

## What this is for (alignment axis — attack it, do not grade against it)

- **Goal:** a TikTok capture calibration plan that is *safe to commission a probe from without overclaiming* — every unproven element labeled a probe-hypothesis, no false-success path, residuals and limitations named honestly.
- **Done looks like:** the memo survives a de-correlated adversarial read **with citations verified against source** and shows **no material overclaim, no missing load-bearing residual/limitation, no false-success path, no unsafe route, and no wrong/unsupported citation** that a downstream probe or builder could act on as if proven.

Treat that goal/signal as an axis you must also attack (could the goal itself hide a risk?), never as a pass-if-matches bar.

## Source-gated method contract

1. **REFERENCE-LOAD** (read as procedural guidance only; do **not** apply yet): an adversarial-artifact-review method + a deep-thinking risk-framing pass. If Orca skills `workflow-deep-thinking` and `workflow-adversarial-artifact-review` are available in your runtime, reference-load them; otherwise apply the equivalent discipline — deep-think failure modes and decision criteria first, then a maximally adversarial findings pass.
2. **SOURCE-LOAD** the actual repo context needed to verify the memo. At minimum read: `AGENTS.md`; `.agents/workflow-overlay/{README,source-loading,safety-rules}.md`; `orca/product/spines/capture/core/source_capture_toolbox/{source_capture_playbook_v0,capture_recon_index_v0}.md`; the IG architecture docs the memo cites under `orca/product/spines/capture/core/source_families/social_media/instagram/` (`orca_creator_momentum_pipeline_architecture_v0.md`, `orca_creator_monitoring_policy_architecture_v0.md`, `ig_capture_shape_contract_spec_v0.md`, `ig_wind_caller_calls_capture_build_architecture_v0.md`, and the cited IG probe-recon files); the harness `orca-harness/source_capture/**` and the IG runners/tests the memo's reuse map names; and the GO/authorization decision docs (`docs/decisions/orca_consumer_demand_ratification_decision_memo_v0.md`, `docs/decisions/orca_product_thesis_consumer_demand_v0.md`). Spot-check the memo's specific `path:line` citations against these files.
3. Declare **`SOURCE_CONTEXT_READY`** (target hash matches and the verification sources are loaded) or **`SOURCE_CONTEXT_INCOMPLETE`** (name what is missing).
4. Only then **APPLY**: deep-think the risk frame, list findings, verify citations, and author the bounded patch.

Do not produce findings, patches, or verdicts before declaring `SOURCE_CONTEXT_READY`.

## Attack surface — be maximally adversarial about these

1. **Overclaim / false-success paths.** The memo's core honesty move is "owner GO = authorization posture, NOT a working technical route," labeling TikTok-external surfaces `HYPOTHESIS_FOR_PROBE`. Hunt for any place a hypothesis is silently used as fact: a route presented as more proven than the evidence supports, a field listed as capturable without the hypothesis label, a "smallest complete patch sequence" that reads as buildable rather than contingent.
2. **Citation verification (repo-access duty).** For each load-bearing `path:line` citation, confirm the cited file actually says what the memo claims. Flag and patch any citation that is wrong, stale, points to the wrong line/file, or is too thin to support the claim. Where a claim has no citation but needs one, flag it.
3. **The comment-window integrity trap.** The memo claims the 30/60-minute post-relative comment windows are defensible *only* if both the comment and the video carry source-native timestamps at sufficient granularity, else `not_applicable`/`unavailable_with_reason`. Attack this: is the rule sufficient to prevent fabricated precision? Partial-granularity, timezone, or clock-skew cases it misses? Could a builder still bucket coarse "2d ago" strings?
4. **Safety-boundary leakage.** Public/logged-out routes are in scope; the auth/access-control line is the hard stop (Route 4 internal-API = NO-GO if signed+auth-only; own-account discouraged; no cookies/storage-state/exit-IPs). Find any route/field/step that could cross an access-control wall, harvest private-individual data, or leak a credential/exit-IP without the memo flagging it. Cross-check against `.agents/workflow-overlay/safety-rules.md` and the playbook's Step-0 access-control line.
5. **Missing routes / residuals / limitations.** Is any load-bearing risk *absent* from `NON_CLAIMS_AND_RESIDUALS`, or any viable route absent from `ROUTE_OPTIONS`? Specifically assess whether an **official TikTok API** row is missing (as of mid-2026: Display API = the authenticated user's *own* content only; Research API = free but eligibility-gated to academic/non-profit researchers — so likely own-account-only / ineligible for Orca's commercial use, i.e. effectively NO-GO/CATALOG for the target data, which *reinforces* the public-web-probe-or-vendor framing). Also check for legal/ToS exposure beyond the authorization posture, mobile-app-only `CATALOG_GAP`, anti-bot fidelity unproven, identity-model assumptions, and the vendor-data first-party-content prohibition. Treat external API facts as probe-time-verifiable, not architecture fact.
6. **Reuse-map correctness, verified against code.** The memo claims only ~4 satellite files are new per platform and the rest of the harness is reused unchanged. Read the actual `orca-harness/source_capture/**` and IG modules: does anything it calls "reused unchanged" carry an IG-specific assumption that would silently mis-handle TikTok (metric semantics, identity, content-unit, block markers)? Is anything it calls "new/not-portable" actually generic? Correct any mis-stated file or claim.
7. **Route ranking and probe-gate safety.** Is the cheapest-first ranking defensible? Does `LIVE_PROBE_GATE` have a gap that would let a probe start or continue past a wall? Are the stop conditions complete?
8. **Internal contradiction / scope drift.** Anywhere the memo contradicts itself, drifts beyond read-only planning, or implies build/validation/readiness it explicitly disclaims.

## Output contract (repo mode — bounded patch + findings)

Patch the **single target memo** in the working tree (do **not** commit/push), and return to the commissioning Chief Architect:

- a **unified diff** of your changes to the target memo only;
- **findings**, each with: `id` (AR-01…), short title, `severity` ∈ {`critical`, `major`, `minor`} (finding-priority only, not a formal gate verdict); `location` (memo section + short verbatim quote); `why_it_matters`; `minimum_closure_condition` (required end state, not how-to); `next_authorized_action`; and the **source citation you verified** (`path:line`, neutral in tone, decision-sufficient in substance) backing the fix;
- a short **deep-thinking risk frame** before the findings;
- explicit **non-findings**: attack surfaces you probed and found sound, and citations you verified as correct;
- a **verdict** (one overall; per-section sub-verdicts if they differ materially) and a **residual-risk note** (what stays unproven even after the patch);
- also write a durable findings report to `docs/review-outputs/adversarial-artifact-reviews/tiktok_capture_calibration_architecture_review_findings_v0.md` with `authored_by: Claude Opus 4.8 (Anthropic)` and `reviewed_by: <your model+version>`.

**Escalation valve:** if the memo's problem is design-level rather than wording-level (e.g., the whole route framing is unsafe), return **`NEEDS_ARCHITECTURE_PASS`**, **stop patching, revert any partial diff** (leave the target memo at its original bytes), and return findings only.

## Hard constraints (edit-only-the-submitted-scope)

- Patch **only** `docs/review-outputs/tiktok_capture_calibration_architecture_review_v0.md`. **Everything else is read-only / flag-only**: all other Orca sources, the overlay, `AGENTS.md`/`CLAUDE.md`, the harness code, decisions, and any protected path per `.agents/workflow-overlay/safety-rules.md`. If the correct fix lies outside the target memo, **flag it for the CA — do not edit it.**
- Do **not** commit, push, stage, or create a branch/PR. Leave the working-tree patch for CA adjudication.
- Do not broaden into redesigning TikTok capture, proposing live-probe execution, or cross-platform architecture; do not recommend, rank, or imply any runtime model choice.
- Do not request or include any raw cookies, storage-state, passwords, profile paths, proxy credentials, or exit IPs.
- Your diff, citations, and verdict are **decision input only** — the CA adjudicates each hunk and may reject or modify any change, even a defensible one.
- If the target's SHA256 ≠ `4AA2330A7B8D5BD06AED020AA881669A052A79B10E5E33EADFB20598BFC411FB`, declare `SOURCE_CONTEXT_INCOMPLETE` and stop.

## CA-side adjudication note (not for the delegate to perform)

The Orca Chief Architect (Anthropic, home model) will adjudicate the working-tree diff hunk-by-hunk against the verified citations and the memo's intent, accept/modify/reject (reverting rejected hunks), set `reviewed_by`/`authored_by` on the durable record, and run a bounded same-vendor post-patch recheck (closure-of-findings + any new blocker/major in the touched delta) before anything is kept. Repo-mode discovery + CA closure verification is the stronger form; the delegate's diff and verdict remain claims to adjudicate, not premises to inherit.
```
