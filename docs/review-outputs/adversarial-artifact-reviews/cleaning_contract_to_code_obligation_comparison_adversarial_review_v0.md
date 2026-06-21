# Cleaning Contract-to-Code Obligation Comparison Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review report
scope: >
  Read-only adversarial review of the Cleaning contract-to-code reconciliation
  checklist (cleaning_contract_to_code_reconciliation_checklist_v0.md) against
  the current Cleaning Spine contracts, orca-harness/cleaning/ code, and focused
  unit tests.
use_when:
  - Rechecking the Cleaning contract-to-code checklist review findings before home-lane adjudication.
  - Comparing same-vendor and cross-vendor review reports for the Cleaning hardening patch.
authority_boundary: retrieval_only
authored_by: gpt-5-codex
reviewed_by: unrecorded
review_prompt: docs/prompts/reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_prompt_v0.md
primary_target: docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
secondary_target: docs/workflows/orca_repo_map_v0.md (checklist route line)
output_mode: review-report
template_kind: adversarial-artifact-review
review_lane: docs/review-outputs/adversarial-artifact-reviews/
edit_permission: read-only for review targets; docs-write only for this report
runtime_model_routing: unbound
de_correlation_boundary: >
  Suitable for de-correlated reviewer chosen by operator. Does not itself
  prove de-correlation or claim a delegated review has run.
review_use_boundary: >
  Findings are decision input only — not approval, validation, readiness,
  product proof, mandatory remediation, patch authority, or permission to
  keep any change.
stale_if:
  - docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md changes
  - orca/product/spines/cleaning/contracts/ changes
  - orca-harness/cleaning/ or the focused Cleaning tests are patched
  - The branch advances past bc950cdfeeb3a02f33bf52217d71e049aa9093f2
```

## Source-Read Ledger

**`SOURCE_CONTEXT_READY`**

All 13 required sources were read. Sources 1–8 (authority and method) were loaded before context compaction; sources 9–13 (code and test) were loaded in the current turn. Dirty-state allowance per the review prompt covers the untracked checklist and modified repo map.

| # | Source | Status at read | Role |
|---|--------|---------------|------|
| 1 | `AGENTS.md` | clean | Agent kernel / behavior authority |
| 2 | `.agents/workflow-overlay/README.md` | clean | Overlay entrypoint |
| 3 | `.agents/workflow-overlay/source-of-truth.md` | clean | Source hierarchy and conflict rules |
| 4 | `.agents/workflow-overlay/source-loading.md` | clean | Source capsule and load protocol |
| 5 | `.agents/workflow-overlay/review-lanes.md` | clean | Review lane binding and output destination |
| 6 | `.agents/workflow-overlay/prompt-orchestration.md` | clean | Prompt preflight and method contract |
| 7 | `.agents/workflow-overlay/validation-gates.md` | clean | Gate semantics |
| 8 | `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | clean | Report template |
| 9 | `docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md` | untracked (allowed) | Primary review target |
| 10 | `docs/workflows/orca_repo_map_v0.md` | modified (allowed) | Secondary target — checklist route line |
| 11 | `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md` | clean | Cleaning layer authority |
| 12 | `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` | clean | Foundation authority (OD-1/4/7, NDLC, transform classes) |
| 13 | `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | clean | Layer boundary authority |
| 14 | `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` | clean | Projection doctrine authority |
| 15 | `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | clean | Corroboration/amplification design note |
| 16 | `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md` | clean | Migration proposal (advisory) |
| 17 | `orca-harness/cleaning/models.py` | clean | Code evidence |
| 18 | `orca-harness/cleaning/core.py` | clean | Code evidence |
| 19 | `orca-harness/cleaning/projection.py` | clean | Code evidence |
| 20 | `orca-harness/tests/unit/test_cleaning_core.py` | clean | Test evidence |
| 21 | `orca-harness/tests/unit/test_cleaning_projection_integration.py` | clean | Test evidence |

Method skills `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were REFERENCE-LOADed before source loading; this report is the APPLY step.

**Gap in source pack:** `orca-harness/cleaning/__init__.py` was not in the required source list and was not read. Row 8 evidence and the AR-01 and AR-02 findings below are bounded by this gap.

---

## Findings

**No CRITICAL findings. No MAJOR findings. Three MINOR findings follow.**

---

### AR-01 — Minor · Correctness

**Checklist row:** Row 8 (runtime boundary — bounded substrate only)

**Issue:** Row 8's evidence that no Cleaning runner exists cannot be independently reproduced from the source-read ledger.

**Artifact evidence:** Row 8 states "`rg --files orca-harness | rg "cleaning"` shows only the package and two focused tests" as basis for "no Cleaning runner was observed."

**Source authority:** `core_spine_v0_cleaning_spine_readme_v0.md` implementation/runtime authorization; repo map `orca-harness/cleaning/` row.

**Strongest defense:** The three code files in the source pack (`models.py`, `core.py`, `projection.py`) confirm the bounded substrate shape described. The shell-command evidence is consistent with what the source pack shows; no runner, scheduler, or API module appears in any of the read files.

**Why the defense is insufficient:** The shell command output is not reproducible from the source-read ledger. `orca-harness/cleaning/__init__.py` was not in the source pack and was not read in this review. If a runner or additional module file exists in the package directory outside the three read files, this review cannot confirm or refute its absence. A cold lane cannot verify the runner-absence claim without re-running the search against current worktree state.

**Impact:** Low. The three files read are sufficient to establish bounded substrate shape. Runner absence is consistent with what was read but is not confirmed-absent.

**Minimum closure condition:** Before acting on Row 8's runtime-boundary claim, a reader should re-run `git ls-files orca-harness/cleaning/` (or equivalent) against the current branch and confirm no runner, scheduler, API module, or `__init__.py` re-export surface is present beyond the known three files.

**Next authorized action:** Advisory. The home lane may accept Row 8 as-is (claim is plausible and source-consistent) or annotate it with a note that runner absence requires fresh verification against current worktree file listing before step 2.

**patch_queue_entry:** Not authorized by this review lane.

**Red-green proof status:** Not applicable (file-listing claim, not an executable behavioral check).

---

### AR-02 — Minor · Correctness

**Checklist row:** Candidate Patch Queue (step 1)

**Issue:** The patch queue omits a prerequisite `__init__.py` export check for `CleaningEcrRef`.

**Artifact evidence:** The patch queue step 1 specifies: "valid `CleaningInputHandle` with `CleaningEcrRef(packet_id = raw_anchor.packet_id)`; invalid `CleaningEcrRef(packet_id != raw_anchor.packet_id)` rejects with the existing packet-id coupling error."

**Source authority:** `orca-harness/tests/unit/test_cleaning_core.py` import list (code evidence).

**Strongest defense:** The test author will discover the import path when writing the test and resolve it then. The behavioral test spec (valid + invalid coupling) is correctly identified and complete.

**Why the defense is insufficient:** The existing `test_cleaning_core.py` import block (`from cleaning import (...)`) does not include `CleaningEcrRef`. This means either `CleaningEcrRef` is not yet re-exported from `cleaning/__init__.py`, or it simply hasn't been needed in existing tests. An executor following the patch queue cold would write the test, attempt `from cleaning import CleaningEcrRef`, and potentially encounter an `ImportError` before the behavioral test can run. This is a friction gap in the minimum-closure spec, not a logic error in the test plan.

**Impact:** Low friction. The executor is unlikely to be blocked for long. But the patch queue's completeness claim is not fully executable without the prerequisite import verification.

**Minimum closure condition:** The patch queue step 1 should be prefaced with: verify that `CleaningEcrRef` is exported from `cleaning/__init__.py` (or confirm the direct import path `from cleaning.models import CleaningEcrRef`) before writing the tests.

**Next authorized action:** Advisory. The home lane may add a one-line import prerequisite to the patch queue spec, or leave it for the executor to discover. No checklist row changes required.

**patch_queue_entry:** Not authorized by this review lane.

**Red-green proof status:** Not applicable (import/export verification, not a behavioral gate at checklist level).

---

### AR-03 — Minor · Correctness

**Checklist row:** Row 6 (no Judgment claims — "Covered for listed vocabulary and ledger fields")

**Issue:** `_JUDGMENT_TOKENS` has a word-boundary gap for certain inflected forms; the checklist qualifier "for listed vocabulary" is present but does not identify the specific gap.

**Artifact evidence:** Row 6 claims "Covered for listed vocabulary and ledger fields" and its patch rule says "If adding new text-bearing fields, route them through the same no-Judgment vocabulary discipline."

**Source authority:**
- `core_spine_v0_cleaning_spine_foundation_v0.md` — Forbidden Cleaning reasons: "discounted, excluded, weak, strong, credible, not credible, supports demand, independent corroboration, artificial amplification, action supporting."
- `orca-harness/cleaning/models.py` — `_JUDGMENT_TOKENS` (lines 28–48) and `_find_token_matches` (lines 61–64).

**Code behavior analysis:** `_find_token_matches` checks whether `f"_{token}_"` appears as a substring of the padded-normalized input. For input `"discounted"`: normalized = `"discounted"`, padded = `"_discounted_"`. Token `"discount"` produces the check string `"_discount_"`. Is `"_discount_"` a substring of `"_discounted_"`?

- `"_discounted_"` chars: `_`, `d`, `i`, `s`, `c`, `o`, `u`, `n`, `t`, `e`, `d`, `_`
- `"_discount_"` requires: `_`, `d`, `i`, `s`, `c`, `o`, `u`, `n`, `t`, `_`
- At position 0 in `"_discounted_"`, char 9 is `e` but `"_discount_"` needs `_` at position 9. No match.

Confirmed: `"discounted"` bypasses the `discount` token guard. The foundation-listed forbidden reason "discounted" can appear in a `method_or_rule` value without the validator raising. The same boundary gap applies to other inflected forms whose suffix breaks the `_{token}_` substring pattern (e.g., `"discounting"` similarly bypasses `discount`).

**Strongest defense:** The token vocabulary is belt-and-suspenders defense, not the primary protection. Cleaning's primary protection is structural — it does not perform operations that produce these method names (credibility scoring, exclusion decisions, discount application). The checklist qualifier "for listed vocabulary" correctly acknowledges the scope of the guard. A Cleaning transform with `method_or_rule="discounted_review_text"` would be violating the layer boundary independent of whether the vocabulary guard catches it.

**Why this is a finding:** The checklist qualifier "for listed vocabulary" reads as if the listed vocabulary is correctly handled by the guard. A reader following Row 6's patch rule ("route new text-bearing fields through the same no-Judgment vocabulary discipline") might assume the guard already handles all foundation-forbidden forms including their inflected variants. The specific gap between the foundation's "discounted" and the guard's `discount` token is not surfaced. This could lead future authors to believe their inflected-form additions are caught when they are not.

**Impact:** Low behavioral risk (layer-boundary rules dominate). Medium documentation risk: Row 6's qualifier could mislead a future author about the exhaustiveness of the token guard.

**Minimum closure condition:** The home lane should either (a) add a note to Row 6 stating that `_JUDGMENT_TOKENS` does not catch inflected or derived forms of all foundation-forbidden terms (for example, `"discounted"` bypasses the `discount` token check due to the `_{token}_` substring pattern), or (b) accept the existing qualifier as sufficient and rely on the layer-boundary rules as the primary protection, treating the token guard as a spot-check rather than a complete fence.

**Next authorized action:** Advisory. No code patch is required to close this finding at the checklist level; a row-6 annotation suffices. Whether to patch `_JUDGMENT_TOKENS` to add inflected forms is a separate implementation decision for the home lane, outside the scope of this checklist review.

**patch_queue_entry:** Not authorized by this review lane.

**Red-green proof status:** Testable if the home lane chooses to add a regression test (e.g., `CleaningTransform(method_or_rule="discounted_text", transform_class=NORMALIZATION, ...)` should raise but currently does not). The test would be red before any fix and green after. Current status: `not_currently_tested`.

---

## Non-Findings

The following checklist rows and claims were checked and found sound.

**Row 1 (CleaningInputHandle keyed to raw / OD-1):** Code evidence verified. `CleaningInputHandle` (models.py:178–200) has required `raw_anchor: CleaningRawAnchor`, optional `projection_ref: CleaningProjectionRef | None`, optional `ecr_ref: CleaningEcrRef | None`, and `relation: CleaningRelation = CleaningRelation.KEYED_SIBLINGS_OVER_RAW` as default. The `validate_refs_stay_keyed_to_raw` model validator enforces `projection_ref.packet_id == raw_anchor.packet_id` and `ecr_ref.packet_id == raw_anchor.packet_id` when the refs are present (models.py:195–199). Fit rating "Mostly covered — ECR-ref focused test missing" is accurate.

**Row 2 (projection refs must not claim cleaned or Judgment-ready):** Code and test evidence verified. `CleaningProjectionRef.validate_projection_is_not_cleaning_or_judgment` (models.py:153–160) requires both `"not_cleaned"` and `"not_judgment_ready"` in the lowercased certification string or raises. `test_projection_ref_must_not_claim_cleaned_or_judgment_ready` (test_cleaning_core.py:228–236) exercises this path. Integration tests confirm both `REDDIT_PROJECTION_CERTIFICATION` and `RETAIL_PDP_PROJECTION_CERTIFICATION` satisfy the validator (test_cleaning_projection_integration.py:55, 87). Fit "Covered for current substrate" is accurate.

**Row 3 (ECR ref as pre-cleaning receipt):** Schema and coupling evidence verified. `CleaningEcrRef` carries `packet_id`, `ref_id`, optional `posture_kind`, optional `status` (models.py:164–175); `validate_refs_stay_keyed_to_raw` enforces the packet_id coupling when `ecr_ref` is set (models.py:198–199). Neither test file creates a `CleaningInputHandle` with a non-None `ecr_ref` — confirmed by examining both test files in full. Fit "Partially covered — schema and coupling exist; focused test coverage is missing" is accurate. AR-02 addresses a friction gap in the patch queue spec; it does not change the fit rating.

**Row 4 (non-destructive transform ledger):** All three cited tests exist and behave as described. `CleaningPreservationCheck.validate_all_required_preservation_holds` rejects any field set to False (models.py:211–230). `CleaningTransformLedgerEntry` binds to a `CleaningPreservationCheck` and enforces all `REQUIRED_NON_CLAIMS` (models.py:282–317). `test_transform_ledger_requires_preservation_and_non_claims` (test_cleaning_core.py:120–135), `test_preservation_check_rejects_hidden_loss` (lines 169–178), and `test_packet_rejects_unknown_transform_handle` (lines 181–197) all verified and behavior matches description. Fit "Covered for current in-memory substrate" is accurate.

**Row 5 (exact-identity dedupe only / OD-4):** Code and test evidence verified. `CleaningTransform.validate_transform_contract` requires `method_or_rule="exact_identity"` for `dedupe_mechanics` and rejects deferred tokens (`_DEFERRED_DEDUPE_TOKENS`: cluster, clustering, copied_language, near_match, similarity) in any transform class (models.py:256–279). `derive_exact_identity_duplicate_groups` groups only by full 9-tuple raw-anchor identity (core.py:15–59). Both cited tests exercise the rejection paths correctly and exist at the lines named (test_cleaning_core.py:150–166, 200–209). Fit "Covered" is accurate.

**Row 6 (no Judgment claims):** Core code evidence verified with the constraint stated in AR-03. `REQUIRED_NON_CLAIMS`, `_JUDGMENT_TOKENS`, and `_find_token_matches` are present and wired to all text-bearing fields — `method_or_rule`, `omissions`, `residuals`, `warnings`, `raw_pull_triggers` — through field and model validators (models.py:241–316). Both cited tests verify rejection at the named lines (test_cleaning_core.py:138–147, 213–225). The qualifier "for listed vocabulary and ledger fields" is present and load-bearing; AR-03 is a gap in the qualifier's precision, not a false coverage claim. Fit "Covered for listed vocabulary and ledger fields" is accurate with the AR-03 annotation.

**Row 7 (source-family adaptation at edge):** Code evidence verified. `models.py` docstring (lines 1–7) states adapters can feed the models but the core does not parse sources. `projection.py` uses `Any`-typed parameters for `projection_packet` and `projection_row` with no source-family-specific model fields; it normalizes all projection rows generically to `CleaningInputHandle`. `core.py` operates only on raw-anchor identity tuples. Integration tests cover Reddit and retail/PDP (two non-overlapping families) through the same generic adapter call (test_cleaning_projection_integration.py:31–88). Fit "Covered for current scope" is accurate.

**Row 8 (runtime boundary as bounded substrate):** Code-shape evidence partially verified; see AR-01 for the scope of what is not independently confirmed. The three files read (`models.py`, `core.py`, `projection.py`) are consistent with the bounded substrate claim. No persistence, runner, scheduler, or API code appears in any read file. Fit "Covered as navigation/code-shape evidence, not readiness" is accurate; the "not readiness" qualifier is appropriately placed and matches the repo map's `orca-harness/cleaning/` row description.

**Repo-map route (secondary target):** The checklist route entry correctly classifies the artifact as `retrieval_only` with a scope description that matches the checklist's own stated purpose. The stale conditions in both the checklist retrieval header and the review prompt's `stale_if` are consistent with each other. No retrieval defect found. A cold lane can find the checklist through the repo map and understand its authority limits from the route alone.

**Candidate patch queue (overall):** The two-step queue (ECR-ref unit coverage + re-run focused tests) correctly targets the only actionable coverage gap named in the checklist. The behavioral test spec (valid ECR ref accepted; invalid ECR ref rejected) is the minimum complete closure for the Row 3 gap. AR-02 notes a prerequisite not in the queue; it does not invalidate the queue's test logic or its scoping as test-only.

**Non-claims section:** The checklist's non-claims are complete and accurately scoped. They correctly exclude validation, readiness, owner ratification, buyer proof, product proof, and authority to widen Cleaning. They are not themselves authority; they are self-limiting metadata consistent with the authority sources.

**Authority sourcing:** No row relies on the handoff packet, W3a proposal, or a secondary source for contract-level obligations. The handoff is correctly classified as "orientation only, not present in this clean worktree." All obligation-to-code mappings cite the correct primary contract sources.

**Boundary drift:** Not observed in the checklist or in the code. The checklist does not absorb ECR implementation, Judgment mechanics, near-match dedupe, clustering, source acquisition, persistence, runners, APIs, or product proof into Cleaning's scope. Code enforces these limits via validators, the bounded transform class set, and the `_JUDGMENT_TOKENS` guard.

---

## Residual Risks and Not-Proven Boundaries

1. **Branch pin staleness.** The checklist is pinned to `bc950cdfeeb3a02f33bf52217d71e049aa9093f2`. Per its own `stale_if` conditions, any code or contract change before step 2 requires a checklist refresh. This review cannot verify the branch has not advanced since authorship.

2. **ECR behavioral completeness beyond packet-id coupling.** `CleaningEcrRef.posture_kind` and `.status` are optional and validated only for non-blank strings on `packet_id` and `ref_id`. If the ECR layer eventually requires specific status vocabularies, posture constraints, or ref_id format rules, the current schema would not enforce them. The checklist does not claim otherwise; this is a not-proven boundary the home lane should track as the ECR contract evolves.

3. **`_JUDGMENT_TOKENS` non-exhaustiveness.** As noted in AR-03, the token guard does not catch all inflected forms of foundation-forbidden terms. The primary layer-boundary rules and schema restrictions are the dominant protection, but the guard cannot be treated as a complete vocabulary fence for all possible derivations.

4. **`CleaningEcrRef` import availability.** `cleaning/__init__.py` was not in the source pack and was not read. Whether `CleaningEcrRef` is exported from the package and importable via `from cleaning import CleaningEcrRef` is not proven in this review. The patch queue executor must verify this before writing ECR-ref tests.

5. **Runner-absence claim.** As noted in AR-01, the absence of a Cleaning runner in `orca-harness/cleaning/` is source-consistent but not independently verified from the files read. A fresh `git ls-files orca-harness/cleaning/` against the current branch is the correct verification step before relying on Row 8's runtime-boundary claim.

---

## Final Recommendation

**`accept_with_friction`**

The checklist accurately and completely maps the current Cleaning Spine obligations to the current bounded implementation and focused tests. The one true coverage gap (ECR-ref focused test) is correctly identified in both Row 1 and Row 3, and the candidate patch queue correctly targets a test-only fix as the smallest complete next step.

All three findings (AR-01, AR-02, AR-03) are minor and advisory. None change the checklist's fit ratings, none invalidate the patch queue, and none reveal a contract obligation that was missed or a code behavior that contradicts the checklist's claims. AR-01 and AR-02 create small friction for a cold executor picking up the patch queue without re-running file searches or checking exports; AR-03 is a code observation about the token guard's inflected-form coverage that may warrant a row-6 annotation at the home lane's discretion.

The checklist can guide step 2 after the home lane reviews these advisory findings. If the home lane adds a one-line import prerequisite to the patch queue spec and an annotation to Row 6, or decides those gaps are acceptable executor-discovery items, step 2 can proceed without further checklist revision.

---

## Review-Use Boundary

This is a read-only adversarial review. Findings are decision input for the home lane. They are not approval, validation, readiness evidence, product proof, mandatory remediation, patch authority, or permission to keep any change. The home lane must adjudicate each finding before editing the checklist, code, tests, or repo map.
