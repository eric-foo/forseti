# Orca Claim Defense Doctrine Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the claim-defense doctrine.
use_when:
  - Inspecting doctrine review findings before adjudication or patching.
  - Tracing claim-defense changes to this review evidence.
authority_boundary: retrieval_only
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/orca_claim_defense_doctrine_adversarial_artifact_review_v0.md
  recommendation: patch_before_acceptance
  reviewed_by: gpt-5_codex_exact_runtime_version_unexposed
  authored_by: claude-fable-5
  summary: "Three major claim-defense defects were found and patched in the target: one Row-1 attainment-leak phrase, one missing self-grading triage class, and two receipt rows that overclaimed pre-declaration against retro-known batch cases."
  findings_count: 3
  blocking_findings:
    - AR-01: Row-1 approved wording still implied universal judgment-quality attainment.
    - AR-02: Debunking triage lacked the self-grading/independence attack invited by the PSA analogy.
    - AR-03: Receipts inventory overstated the batch ledger's pre-run key/ledger protections despite retro-known dev cases.
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Commissioning home model adjudicates the proposed diff; owner sign-off remains required before the doctrine becomes operative."
```

## Source Context

`SOURCE_CONTEXT_READY`.

Sources read:

- `AGENTS.md` and `.agents/workflow-overlay/README.md` for Orca authority and overlay precedence.
- `.agents/workflow-overlay/decision-routing.md`; Cynefin routing classified the work as complicated, bounded to a single doctrine target plus required report output.
- `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/communication-style.md`, and `.agents/workflow-overlay/retrieval-metadata.md` for the commissioned repo-mode review-and-patch contract, severity/report shape, and metadata checks.
- `docs/product/product_lead/orca_claim_defense_doctrine_v0.md`; pinned pre-review SHA256 verified as `6740154B08C0329D21AFC52C6967FF1AE1F21B45A4449B52EFC86A82A31B4FE1`.
- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` for tier semantics and receipt caps.
- `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md` for advisory/manual/chat versus gate-bearing execution semantics.
- `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` for batch-1 key pins, retro-known cases, recognition checks, swap policy, and all-results rule.

Method application:

- `workflow-deep-thinking` applied: the dominant failure mode is not whether the doctrine says "not validation" in isolation, but whether approved fragments can be composed into attainment, independence, or clean-provenance claims before receipts exist.
- `workflow-adversarial-artifact-review` applied under the Orca delegated review-and-patch overlay exception; the reusable skill is normally read-only, but the explicit commission authorizes patching this single target file in repo mode.

Review target and bounded patch scope:

- Editable target: `docs/product/product_lead/orca_claim_defense_doctrine_v0.md`.
- Report output: `docs/review-outputs/adversarial-artifact-reviews/orca_claim_defense_doctrine_adversarial_artifact_review_v0.md`.
- Excluded scope: all ladder, tier-policy, ledger, overlay, prompt, hygiene, harness, and external workflow sources.

## Findings

### AR-01 — Major — Row-1 approved phrase implied current universal judgment-quality attainment

Evidence citation:

- Pre-patch target Row 1 approved wording included `"Judgment-quality discipline on every engagement."` at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:85`.
- The same Row 1 caps current claims at `product_learning` and says the basis is `completed_product_learning_evidence` at best at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:76`.
- The ladder states product-learning cannot support a `judgment-quality claim` by itself at `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md:95-102`.
- The execution-tier policy likewise says advisory subscription/manual/chat use cannot support a `judgment-quality claim` by itself at `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md:69-75`.

Why the strongest defense fails:

The phrase could be defended as process discipline, not attainment. That defense is too weak for an allowlist-first external wording table: a marketer can place "Judgment-quality discipline on every engagement" next to "Built to the Orca Judgment-Quality Standard" and create a reader-level impression that every engagement already carries judgment-quality evidence. The artifact's fatal failure mode is attainment blur; approved wording must survive composition, not only literal parsing.

Impact:

This could ship as a present-tense quality claim before a `completed_judgment_quality_evidence` receipt exists.

Minimum closure condition:

The Row-1 approved fragment must describe claim-labeling discipline tied to receipts, without using a phrase that implies every engagement has judgment quality.

Next authorized action:

Target-file wording patch only; home-model adjudication decides whether to keep, modify, or reject the hunk.

Patch applied:

Replaced the phrase with `"Judgment-evidence discipline: every claim is framed, labeled, and limited by its receipt."`

### AR-02 — Major — Triage missed the self-grading/independence attack invited by the PSA analogy

Evidence citation:

- The claim spine positions Orca as "the grader, not the contestant" and invokes PSA at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:48-56`.
- The pre-patch triage table claimed four classes and covered Provenance, Method, Overclaim, and Category only at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:126-133`.
- The spine itself admits the PSA caveat: PSA grades third parties' assets, while today Orca grades its own calls, with receipts machinery and later reality-as-co-grader as the integrity substitute at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:51-54`.

Why the strongest defense fails:

The self-grading attack is not cleanly Provenance, Method, Overclaim, or Category. It is an independence/conflict-of-interest attack: "you are grading yourself." Leaving it unclassified invites the worst possible PSA leakage, where the doctrine borrows PSA's trusted-grader posture but has no mechanical response to the fact that PSA's third-party independence is not currently true for Orca.

Impact:

A foreseeable external criticism would either be forced into the wrong class or answered by prose improvisation, undercutting the artifact's goal that claims decisions become mechanical.

Minimum closure condition:

The triage table must include a class that directly handles "you grade yourselves / no independent auditor" and forbids borrowing third-party certification credibility.

Next authorized action:

Target-file wording patch only; home-model adjudication decides whether to keep, modify, or reject the hunk.

Patch applied:

Changed the heading from "four attack classes" to "attack classes" and added an `Independence` row.

### AR-03 — Major — Receipts inventory overstated pre-declaration against retro-known dev cases

Evidence citation:

- Pre-patch receipts inventory said the answer to "Tuned the key after seeing results" was "Scoring-key SHA256 pins recorded in the batch ledger before any run" at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:155`.
- It also answered "Cherry-picked the cases" with "Pre-declared ledger; all-results reporting rule; swaps recorded as findings" at `docs/product/product_lead/orca_claim_defense_doctrine_v0.md:156`.
- The batch ledger records cases 1 and 2 as `RETRO`, run before the ledger existed, with results known and fixture quarantined at `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:58-63`.
- The batch ledger caps the batch at product-learning and excludes fixture admission, buyer contact, JQ-lane builds, and scoring-key changes at `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:47-56`.
- The ledger freezes the scoring key for the batch and says owner-accepted key changes stop the batch at `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:88-94`.
- It requires all results, failures, exclusions, swaps, and quarantines to be reported; selective reporting voids the anti-cherry-pick property at `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:112-113`.

Why the strongest defense fails:

The ledger does create prospective protections for the new batch cases, but "before any run" is false for the retro-known dev cases. The doctrine cannot answer a contamination/tuning attack by overstating the receipt. The honest defense is stronger: prospective cases are pre-declared and pinned, while retro-known cases are disclosed, quarantined/reported, and barred from clean-evidence use.

Impact:

This is a direct receipts-inventory honesty defect. If shipped unchanged, the doctrine would create exactly the kind of overclaim it is meant to prevent.

Minimum closure condition:

The receipts inventory and Row-1 backtest wording must distinguish prospective pre-declared cases from retro-known/quarantined cases, and must keep the claim cap at product-learning.

Next authorized action:

Target-file wording patch only; home-model adjudication decides whether to keep, modify, or reject the hunks.

Patch applied:

Reworded the Row-1 backtest phrase and the two relevant receipts rows to separate prospective pre-declaration from retro-known/quarantined evidence.

## Non-Findings

- Retrieval metadata is present and uses the required `retrieval_header_version: 1`, `artifact_role`, `scope`, `use_when`, and `authority_boundary: retrieval_only` shape. The `open_next` and `stale_if` fields have clear retrieval value for this doctrine.
- The target correctly states that it is `PROPOSED_PENDING_OWNER_SIGNOFF` and that the wording table is proposed until owner sign-off.
- The target's subordination section correctly says the evidence ladder and tier policy control tier and execution-surface semantics, that row activation happens only on named ladder closeout receipts, and that the doctrine mints no tiers.
- Row 2 and Row 3 do not appear to redefine the ladder tiers; they cite closeout receipts and preserve the ladder's buyer-proof and judgment-quality limitations.
- The execution-surface boundary is materially consistent with the tier policy: manual/chat surfaces are not described as gate-bearing in the patched wording.

## Not-Proven Boundaries

- This review does not prove the doctrine is ready, adopted, validated, or safe to use externally.
- This review does not prove the Judgment-Quality Standard, buyer proof, product readiness, commercial readiness, fixture admission, clean no-tools evidence, or judgment-quality evidence.
- This review does not approve the target, require adoption of the patch, or make remediation mandatory.
- This review does not inspect or change public marketing copy, the future public Judgment-Quality Standard document, batch-1 execution artifacts, harness code, scoring keys, or any ledger outside the single target.
- The current review found no design-level defect requiring `NEEDS_ARCHITECTURE_PASS`; that is a decision-input judgment, not validation.

## Unified Diff With Per-Change Citations

```diff
diff --git a/docs/product/product_lead/orca_claim_defense_doctrine_v0.md b/docs/product/product_lead/orca_claim_defense_doctrine_v0.md
--- a/docs/product/product_lead/orca_claim_defense_doctrine_v0.md
+++ b/docs/product/product_lead/orca_claim_defense_doctrine_v0.md
@@
-- "Judgment-quality discipline on every engagement."
-- "Backtested development results under pre-declared ledgers, pinned scoring
-  keys, and per-model recognition checks — reported in full, labeled
-  product-learning."
+- "Judgment-evidence discipline: every claim is framed, labeled, and limited
+  by its receipt."
+- "Backtest results labeled product-learning, with prospective cases run under
+  pre-declared ledgers, pinned scoring keys, and per-model recognition checks;
+  retro-known cases disclosed as such and quarantined/reported, not laundered
+  into clean evidence."
@@
-## Debunking Triage (four attack classes; answer per class, never across)
+## Debunking Triage (attack classes; answer per class, never across)
@@
 | Provenance | "contaminated / cherry-picked / tuned after results" | The one receipt that kills it (see inventory), within days | Argue without artifacts |
 | Method | "your scoring key / rubric is wrong" | Openness: the key is versioned and pinned; disagreement is recorded AS evidence (e.g., the floor-4 contest); invite the specific critique into the next dated key proposal | Defend the key as beyond critique |
+| Independence | "you grade yourselves / no independent auditor" | Name the self-grading caveat directly: today the integrity substitute is receipts machinery, and sealed-call maturity adds reality as co-grader; do not claim third-party certification | Borrow PSA's third-party-independence credibility |
 | Overclaim | "you said more than you have" | Quote the claim's tier label and this table; if we actually overclaimed: concede, correct in place, dated amendment | Reinterpret our own words after the fact |
 | Category | "LLMs can't judge" | Reframe to the measurable contract — calls versus outcomes under the Standard; decline the philosophy debate | Argue in the abstract |
@@
-| "Tuned the key after seeing results" | Scoring-key SHA256 pins recorded in the batch ledger before any run |
-| "Cherry-picked the cases" | Pre-declared ledger; all-results reporting rule; swaps recorded as findings |
+| "Tuned the key after seeing results" | Scoring-key SHA256 pins recorded in the batch ledger for prospective batch runs; retro-known dev cases are disclosed as retro/quarantined and cannot carry clean evidence |
+| "Cherry-picked the cases" | Pre-declared ledger for prospective cases; all-results reporting rule; swaps and retro-known/quarantined cases recorded as findings |
```

Per-change citations:

- Row-1 wording: the ladder says product-learning cannot support a judgment-quality claim by itself (`docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md:95-102`), and the tier policy says advisory/manual/chat use cannot support a judgment-quality claim (`docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md:69-75`).
- Independence triage: the target's own PSA leak-check states the self-grading caveat and receipts/reality-as-co-grader substitute (`docs/product/product_lead/orca_claim_defense_doctrine_v0.md:51-54`).
- Receipts wording: the batch ledger includes retro-known/quarantined dev cases (`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:58-63`), key freezing/stopping rules (`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:88-94`), and all-results reporting including quarantines (`docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md:112-113`).

## Verdict And Residual Risk

Verdict: `PATCH_BEFORE_ACCEPTANCE` as decision input. The patch closes the three highest-risk wording defects visible in the named source set without changing the doctrine's architecture or any upstream source.

Residual risk: the doctrine remains a proposed internal policy. A future public Judgment-Quality Standard document and any external marketing copy still need their own claim-by-claim review because approved fragments can create new implications when placed in headlines, decks, sales scripts, or proof packets.

## Provenance

```yaml
authored_by: claude-fable-5
reviewed_by: gpt-5_codex_exact_runtime_version_unexposed
de_correlation_bar: cross_vendor_discovery
```

## Review-Use Boundary

These findings, diff, and verdict are DECISION INPUT ONLY. They are not approval, validation, readiness, mandatory remediation, or adoption. The commissioning home model adjudicates every change (accept / modify / reject, reverting rejected hunks) before anything is kept, and the owner's sign-off remains the adoption gate for the doctrine itself. This review does not claim the doctrine is adopted, valid, ready, or safe, and it does not touch judgment-spine batch-1 execution or artifacts in any way.
