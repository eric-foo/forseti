# Cleaning Contract-to-Code Obligation Comparison Adversarial Review — Cross-Vendor (Claude) v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review report
scope: >
  Read-only cross-vendor adversarial review of the Cleaning contract-to-code
  reconciliation checklist (cleaning_contract_to_code_reconciliation_checklist_v0.md)
  against the current Cleaning Spine contracts, orca-harness/cleaning/ code, and
  focused unit tests. Independent de-correlated pass alongside the prior
  same-vendor report; preserves and does not overwrite it.
use_when:
  - Rechecking the Cleaning contract-to-code checklist review findings before home-lane adjudication.
  - Comparing same-vendor and cross-vendor review reports for the Cleaning hardening patch.
authority_boundary: retrieval_only
authored_by: gpt-5-codex
reviewed_by: claude-opus-4.8
de_correlation_bar: cross_vendor_discovery
de_correlation_note: >
  Checklist authored by gpt-5-codex (OpenAI); this review performed by
  claude-opus-4.8 (Anthropic) — cross-vendor discovery bar per review-lanes.md.
  The prior report at the canonical destination
  (cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md) was
  authored by gpt-5-codex (same vendor as the checklist). This cross-vendor pass
  is written to a differentiated path to preserve that report for same-vs-cross
  comparison, not to replace it.
review_prompt: docs/prompts/reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_prompt_v0.md
primary_target: docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
secondary_target: docs/workflows/orca_repo_map_v0.md (checklist route line)
output_mode: review-report
template_kind: adversarial-artifact-review
review_lane: docs/review-outputs/adversarial-artifact-reviews/
edit_permission: read-only for review targets; docs-write only for this report
runtime_model_routing: unbound
reviewed_at_commit: bc950cdfeeb3a02f33bf52217d71e049aa9093f2
origin_main_at_review: 631c5e89de59848fada59d45e52668ae2dba85b5
review_use_boundary: >
  Findings are decision input only — not approval, validation, readiness,
  product proof, mandatory remediation, patch authority, or permission to keep
  any change. The home lane adjudicates each finding.
stale_if:
  - docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md changes
  - orca/product/spines/cleaning/contracts/ changes
  - orca-harness/cleaning/ or the focused Cleaning tests are patched
  - The branch advances past bc950cdfeeb3a02f33bf52217d71e049aa9093f2 in a way that touches the Cleaning surfaces
```

## Review Method Status

- `workflow-deep-thinking`: invoked and applied (failure-mode framing, anti-anchoring verification pass).
- `workflow-adversarial-artifact-review`: invoked and applied after `SOURCE_CONTEXT_READY`.
- Commission-bound target: the reconciliation checklist. Purpose: confirm the checklist accurately and completely maps current Cleaning obligations to current code/tests before the home lane picks the next patch. Fitness reference (prompt-bound): the next Cleaning patch must target real contract-to-code drift, not a false gap or an overclaimed coverage row.
- Lane-collision: clean. This is non-code artifact review of the checklist; code/tests were read as **evidence for the checklist's claims**, not reviewed as an implementation lane.
- Output binding: `filesystem-output`. The prompt's named `required_output_path` was occupied by an untracked prior report this reviewer did not author; per the AGENTS.md overwrite guard this report is written to a differentiated cross-vendor path in the same lane folder. See `de_correlation_note`.

## Source-Read Ledger

**`SOURCE_CONTEXT_READY`**

All 13 prompt-required task sources were read this turn, plus three checks the prompt allowed the reviewer to run (`__init__.py`, `git ls-files`, an empirical validator test). Reads were performed against the codex worktree at `bc950cdf` (the checklist's pinned commit), which matches the prompt's `branch_or_commit_reference`.

| # | Source | Status at read | Role |
|---|--------|----------------|------|
| 1 | `AGENTS.md` | in active context | Agent kernel / behavior authority |
| 2 | `.agents/workflow-overlay/README.md` | clean | Overlay entrypoint / authority gate |
| 3 | `.agents/workflow-overlay/source-of-truth.md` | clean | Source hierarchy + conflict rules |
| 4 | `.agents/workflow-overlay/review-lanes.md` | clean | Review-lane binding, severity labels, reviewed_by/authored_by, two-bar de-correlation |
| 5 | `.agents/workflow-overlay/validation-gates.md` | clean | Gate semantics |
| 6 | `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | clean | Report template |
| 7 | `docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md` | untracked (allowed) | **Primary review target** |
| 8 | `docs/workflows/orca_repo_map_v0.md` (route line :459, targeted) | modified (allowed) | Secondary target — checklist route line |
| 9 | `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md` | clean | Cleaning entrypoint authority |
| 10 | `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` | clean | Cleaning layer contract (OD-1/4/7, forbidden reasons, raw-pull rules) |
| 11 | `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | clean | Layer boundary authority |
| 12 | `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` | clean | Projection doctrine (OD-1/4, certification, raw-pull triggers) |
| 13 | `orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | clean | Corroboration/amplification design note |
| 14 | `docs/migration/phase2_proposals/cleaning_w3a_proposal_v0.md` | clean | Migration proposal (advisory; 0 deletion candidates) |
| 15 | `orca-harness/cleaning/models.py` | clean | Code evidence |
| 16 | `orca-harness/cleaning/core.py` | clean | Code evidence |
| 17 | `orca-harness/cleaning/projection.py` | clean | Code evidence |
| 18 | `orca-harness/cleaning/__init__.py` | clean | Code evidence (export-surface check; not in prompt's list — read to resolve patch-queue executability) |
| 19 | `orca-harness/tests/unit/test_cleaning_core.py` | clean | Test evidence |
| 20 | `orca-harness/tests/unit/test_cleaning_projection_integration.py` | clean | Test evidence |

Reviewer-run checks (the prompt permits the reviewer to confirm evidence):
- `git ls-files orca-harness/cleaning/` → exactly `__init__.py`, `core.py`, `models.py`, `projection.py`; runner/persistence grep (`runner|scheduler|FastAPI|flask|uvicorn|@app|def main|__main__|persist|database|sqlite|psycopg`) → no matches.
- Empirical validator test (executed) — see AR-01 evidence.
- `git diff --stat bc950cdf 631c5e89 -- orca-harness/cleaning/ <focused tests> orca/product/spines/cleaning/contracts/` → empty (the reviewed Cleaning surfaces are byte-identical between the checklist's pinned commit and current `origin/main`).

**Honest read-scope note (bounds no finding):** `.agents/workflow-overlay/source-loading.md` and `.agents/workflow-overlay/prompt-orchestration.md` (authority sources 4 and 6 in the prompt's Required Source Order) were not separately re-read this turn; AGENTS.md routes to them and no finding below depends on them. Method skills `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were loaded and applied.

---

## Findings

**No CRITICAL findings. One MAJOR finding (AR-01). One MINOR finding (AR-02).**

---

### AR-01 — Major · Correctness (Phase 1)

**Checklist row:** Row 6 — "Cleaning may record mechanics but must not make Judgment claims or effects." Fit: *"Covered for listed vocabulary and ledger fields."*

**Issue:** Row 6 presents the no-Judgment-vocabulary obligation as covered and cites the Judgment-token validators as the code anchor, but the cited guard does **not** catch two of the forbidden Cleaning reasons the foundation **explicitly enumerates**. The qualifier "for listed vocabulary" does not disclose that the listed vocabulary under-covers the foundation's own enumeration — including a wedge-critical term that has no token at all.

**Source authority:**
- `core_spine_v0_cleaning_spine_foundation_v0.md` (Layer Boundary): *"Forbidden Cleaning reasons include discounted, excluded, weak, strong, credible, not credible, supports demand, independent corroboration, **artificial amplification**, action supporting, or any equivalent Judgment-use label."*
- Reinforced as Judgment-owned in `core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (Inclusion State Rule → "Integrity exclusion … Artificial-amplification risk … Judgment Spine") and `core_spine_v0_projection_doctrine_v0.md` (§11 OD-4 "amplification … effects stay Judgment-owned"; §8 trigger 4 "Copied/coordinated or artificial-amplification call").

**Artifact evidence:** Row 6 code anchor — *"Required non-claims; Judgment-token validators on transform methods and warnings/residuals/raw-pull triggers."* Fit — *"Covered for listed vocabulary and ledger fields."*

**Code evidence:** `orca-harness/cleaning/models.py` — `_JUDGMENT_TOKENS` (lines 28–48) contains no `amplification`/`artificial` token; `_find_token_matches` (lines 61–64) matches a token only as the boundary-padded substring `f"_{token}_"`; `validate_method_or_rule` (lines 242–253) and `reject_judgment_warning_reasons` (lines 299–310) both gate via `_find_token_matches(..., _JUDGMENT_TOKENS)`.

**Empirical evidence (executed against the package at `bc950cdf`):**
```
_find_token_matches("artificial amplification", _JUDGMENT_TOKENS) -> []
_find_token_matches("discounted",               _JUDGMENT_TOKENS) -> []
CleaningTransform(method_or_rule="artificial_amplification", class=NORMALIZATION, ...) -> ACCEPTED (no raise)
CleaningTransform(method_or_rule="discounted",               class=NORMALIZATION, ...) -> ACCEPTED (no raise)
CleaningTransform(method_or_rule="discounting",              ...)                       -> ACCEPTED (no raise)
# contrast — the guard works for listed bare tokens:
CleaningTransform(method_or_rule="credibility", ...)                  -> REJECTED (method_or_rule)
CleaningTransform(method_or_rule="discount_format_normalization", ...) -> REJECTED (method_or_rule)
```
Two foundation-enumerated forbidden reasons pass the validator: `"artificial amplification"` (no token exists) and `"discounted"`/`"discounting"` (the foundation's inflected form escapes the `_{token}_` boundary around the `discount` token). The same `_JUDGMENT_TOKENS`/`_find_token_matches` path backs the warnings/residuals/raw_pull_triggers validator, so the gap spans both surfaces Row 6 claims ("methods" and "ledger fields").

**Strongest defense, and why it fails:** The strongest reading is (a) the qualifier "for listed vocabulary" scopes the claim to the listed tokens; (b) the foundation ends its list with "or any equivalent Judgment-use label," which no finite token set can fully enforce; and (c) the **primary** boundary protection is structural — bounded transform classes, exact-identity-only dedupe, non-destructive preservation — so Cleaning does not actually *perform* an amplification or discount decision, making the token guard belt-and-suspenders. Points (b) and (c) are genuinely true and are why this is **major, not critical** — there is no evidence Cleaning currently produces these effects. The defense fails on the specific claim Row 6 makes: the gap is not in the open-ended "equivalent" catch-all, it is in two reasons the foundation **names explicitly**, one of which ("artificial amplification") is affirmed as Judgment-owned in three separate contracts and has **no token at all**. The checklist cites the token validators as the proof of coverage; "for listed vocabulary" reads to a home lane as "the cited guard handles the forbidden vocabulary," when it does not. Precisely because the structural fence is the real protection, the faithful map would label the token guard a non-exhaustive spot-check — which Row 6 does not do.

**Impact:** Decision-relevant for the next-patch choice. The candidate patch queue (ECR-ref test only) contains no guard-hardening item, partly because Row 6 reads as covered; a corrected Row 6 would surface guard hardening as a legitimate candidate. Secondary risk: a future author following Row 6's patch rule ("route new text-bearing fields through the same no-Judgment vocabulary discipline") may believe inflected/amplification additions are caught when they are not. Low *current* behavioral risk; medium map-accuracy risk.

**minimum_closure_condition:** Row 6 either (a) discloses that `_JUDGMENT_TOKENS` does not cover all foundation-enumerated forbidden reasons — naming at least "artificial amplification" (no token) and the "discounted"/"discounting" inflection (escapes `_{token}_`) — and reframes the cited guard as a non-exhaustive spot-check rather than a complete fence; or (b) the home lane explicitly accepts the gap and records the token guard as belt-and-suspenders with the structural layer boundary as the primary protection. Whether to harden the code guard is a separate implementation decision, outside this checklist-review scope.

**next_authorized_action:** Advisory. Home lane annotates Row 6 and/or adds a guard-hardening candidate to the patch queue. No code patch is authorized by this review lane.

**patch_queue_entry:** Not overlay-authorized (adversarial artifact review lane; `patch_queue_entry` is reserved for patch-queue/execution lanes per review-lanes.md).

**Red-green proof status (for a future, separately authorized code fix):** Testable. `CleaningTransform(method_or_rule="artificial_amplification", transform_class=NORMALIZATION, original_value="x", transformed_value="x")` should raise but currently does not (same for `"discounted"`); a regression test would be red against the unfixed guard and green after a fix. Current status: `not_currently_tested`.

---

### AR-02 — Minor · Correctness/completeness (Phase 1)

**Checklist location:** Whole-checklist completeness — the foundation's "Traceability And Raw-Pull Rules" obligation ("Cleaning must pull raw, halt, or escalate when …") has no checklist row and is not classified.

**Issue:** The checklist states it "maps current contract obligations to current code and tests," but one prominent foundation obligation — raw-pull triggering — is neither mapped nor classified as out-of-substrate/deferred. The substrate carries the data field but not the triggering logic, so a reader cannot tell from the checklist whether this obligation is "covered," "deferred," or "missed."

**Source authority:** `core_spine_v0_cleaning_spine_foundation_v0.md` "Traceability And Raw-Pull Rules" ("Cleaning must pull raw, halt, or escalate when …"); `core_spine_v0_projection_doctrine_v0.md` §8 Raw Pull-In Trigger Table.

**Code evidence:** `models.py` — `CleaningTransformLedgerEntry.raw_pull_triggers: list[str]` (line 289) exists as a free list field; no validator or logic decides *when* triggers must fire. `git ls-files` confirms no Cleaning runner/behavioral logic in the package.

**Strongest defense, and why a residual remains:** The checklist's scope is explicitly "the bounded Cleaning substrate already present" (in-memory models + exact-identity deriver), and raw-pull *triggering* is runtime/behavioral logic the substrate intentionally does not implement (README/foundation authorize bounded substrate only, no runner). Row 8 covers "bounded substrate only," and Row 6 lists `raw_pull_triggers` among the ledger fields. So the **field** is mapped and the **logic** is out-of-substrate by design — this defense largely holds, which is why the finding is **minor**. The residual: the checklist never *classifies* raw-pull triggering as deferred/out-of-substrate, so for one of the foundation's most prominent obligations the map is silent rather than explicit. A reader who already knows the substrate is models-only will infer it; a reader who does not cannot distinguish a deliberate scope boundary from an omission.

**Impact:** Low. Completeness/disclosure gap, not a false-coverage claim. Does not affect the existing ECR-ref patch.

**minimum_closure_condition:** The checklist adds a row or note classifying the raw-pull-trigger obligation as out-of-substrate/deferred (field present as `raw_pull_triggers`; triggering logic not implemented and not in bounded-substrate-v0 scope), OR the home lane records that the existing scope statement plus Row 8 adequately bound the omission.

**next_authorized_action:** Advisory. Home lane adds the classification or accepts the omission as scope-bounded.

**patch_queue_entry:** Not authorized.

**Red-green proof status:** `not_applicable` (completeness/classification finding, not an executable check).

---

## Phase 2 — Friction

No avoidable-friction findings. The checklist is compact, has a working retrieval header, a recheck recipe, and a two-step candidate patch queue. The non-claims section is appropriately scoped and not padded. No redundant ceremony to trim.

---

## Non-Findings (checked and found sound)

- **Row 1 (input handle keyed to raw; projection/ECR optional keyed siblings / OD-1):** `CleaningInputHandle` (models.py:178–200) — `raw_anchor` required; `projection_ref`/`ecr_ref` optional; `relation = KEYED_SIBLINGS_OVER_RAW` default; `validate_refs_stay_keyed_to_raw` (195–199) enforces `packet_id` coupling for both refs when present. OD-1 citation verified against foundation OD-1 and projection doctrine §11 OD-1. Fit "Mostly covered — focused ECR-ref test missing" is accurate (confirmed: no test constructs `ecr_ref`).
- **Row 2 (projection refs must not claim cleaned/Judgment-ready):** `CleaningProjectionRef.validate_projection_is_not_cleaning_or_judgment` (models.py:153–161) requires both `not_cleaned` and `not_judgment_ready` in the cert; `test_projection_ref_must_not_claim_cleaned_or_judgment_ready` (test_cleaning_core.py:228–236) exercises it; projection-doctrine certification/non-claims citation verified (§1, §3 Rule 6, §4). Fit "Covered for current substrate" accurate. (See residual risk 2 for a substring-presence weakness that does not make the row false.)
- **Row 3 (ECR ref as pre-cleaning receipt):** `CleaningEcrRef` schema (models.py:164–175) + packet-id coupling (198–199) verified; neither test file constructs a handle with `ecr_ref`. Fit "Partially covered — schema and coupling exist; focused test missing" accurate.
- **Row 4 (non-destructive transform ledger):** `CleaningPreservationCheck.validate_all_required_preservation_holds` (211–230) and `CleaningTransformLedgerEntry` non-claims (282–317) verified; `test_transform_ledger_requires_preservation_and_non_claims`, `test_preservation_check_rejects_hidden_loss`, `test_packet_rejects_unknown_transform_handle` exist and behave as described. Fit "Covered" accurate.
- **Row 5 (exact-identity dedupe only / OD-4):** `validate_transform_contract` (255–279) requires `exact_identity` for `dedupe_mechanics` and rejects `_DEFERRED_DEDUPE_TOKENS`; `derive_exact_identity_duplicate_groups` (core.py:15–59) groups only by the full 9-tuple raw-anchor identity; both cited tests verified. Fit "Covered" accurate. (The Projection Doctrine §7 table's older "mechanical similarity score" wording is superseded by foundation OD-4 and the doctrine's own §11 OD-4 "exact identity … only"; the checklist correctly tracks the controlling foundation — not a defect.)
- **Row 7 (source-family adaptation at the edge):** models docstring (1–7), `projection.py` `Any`-typed projection params with no source-family-specific model fields, `core.py` operating only on raw-anchor identity; integration tests cover two non-overlapping families (Reddit, retail/PDP). Fit "Covered for current scope" accurate.
- **Row 8 (runtime boundary = bounded substrate only):** **independently verified** — `git ls-files orca-harness/cleaning/` returns exactly the four files the row names (`__init__.py`, `core.py`, `models.py`, `projection.py`) and the runner/persistence grep is empty. Row 8's runner-absence claim is reproduced, not merely consistent.
- **Repo-map route (secondary target):** `orca_repo_map_v0.md:459` classifies the checklist as retrieval-only ("not validation, readiness, or production Cleaning authorization") with an accurate scope description; a cold lane can find it and read its authority limit from the route alone. No retrieval defect.
- **Candidate patch queue:** The ECR-ref test gap is real (no test constructs `ecr_ref`) and the test is **fully import-executable** — `CleaningEcrRef` is exported from `cleaning/__init__.py` (line 15; `__all__` line 38), so `from cleaning import CleaningEcrRef` works. The two-step queue is the smallest complete closure for the Row 3 gap.
- **Authority sourcing:** No row relies on the handoff packet, the W3a proposal (a 0-deletion-candidate ontology scan), or a secondary source where a contract should control. The absent handoff is correctly labeled "orientation only."
- **Boundary drift:** None. No row absorbs ECR, Judgment, near-match/copied-language/clustering, source acquisition, persistence, runners, or APIs into Cleaning; the non-claims explicitly disclaim them.

### Clearances of the prior same-vendor report's open items
The prior report (gpt-5-codex) left two minor findings bounded on un-read sources. Both resolve with direct evidence in this pass and become non-findings:
- **Prior AR-01 (runner-absence not reproducible):** resolved — `git ls-files` + grep reproduce runner absence (above).
- **Prior AR-02 (patch queue may hit `ImportError` on `CleaningEcrRef`):** moot — `CleaningEcrRef` is exported from `__init__.py`; the import works.
The prior report's AR-03 (the `discounted` inflection) is **confirmed and subsumed** into AR-01 here, which escalates it to major by adding the complete, enumerated, wedge-critical "artificial amplification" omission and the empirical end-to-end accept evidence.

---

## Residual Risks and Not-Proven Boundaries

1. **Branch-pin freshness — closed for the reviewed surfaces.** The checklist is pinned to `bc950cdf`. `origin/main` has advanced to `631c5e89` (the prompt recorded `78009195`), but `git diff --stat` shows the Cleaning package, focused tests, and Cleaning contracts are byte-identical between `bc950cdf` and `631c5e89`. The checklist remains code-current for what it maps. Its own `stale_if` still governs any future change.
2. **Substring-presence validator weakness (Row 2), not-proven boundary.** `CleaningProjectionRef`'s cert validator checks *presence* of `not_cleaned`/`not_judgment_ready` but does not forbid contradictory positive claims in the same string (same substring-matching fragility class as AR-01). Low practical risk; the row's "covered for current substrate" is not made false by it, but a reader should not read it as forbidding positive cleaned/judgment-ready assertions.
3. **`relation` field is decorative (Row 1).** `CleaningInputHandle.relation` is a single-value enum not referenced by `validate_refs_stay_keyed_to_raw`; the enforced keying is the `packet_id` coupling, which Row 1 also cites. Not a defect — noted so the home lane does not treat `relation` as the enforcement mechanism.
4. **Token-guard false positives (inverse of AR-01).** Tokens such as `demand`/`weak` can over-reject legitimate method names (e.g., `on_demand_normalization`, `weak_reference_cleanup`). Tangential to the checklist's coverage claims; a code-precision note, not a checklist finding.
5. **ECR behavioral completeness beyond packet-id coupling.** `CleaningEcrRef.posture_kind`/`.status` are optional and unconstrained beyond non-blank. The checklist does not claim otherwise; a not-proven boundary to track as the ECR contract evolves.

---

## Final Recommendation

**`accept_with_friction`**

The checklist accurately maps the structural Cleaning obligations to the bounded substrate, and the one true coverage gap it names (ECR-ref focused test) is correct, smallest-complete, and import-executable — so the named step-2 patch can proceed. The friction is AR-01 (major): Row 6 overstates the no-Judgment-vocabulary coverage by citing a token guard that, as empirically demonstrated, accepts two foundation-enumerated forbidden reasons ("artificial amplification" — unlisted; "discounted"/"discounting" — inflection escapes the token boundary). Before the home lane treats the no-Judgment fence as complete, Row 6 should be corrected (disclose the gap and reframe the guard as a spot-check), and guard hardening should be weighed as a second patch candidate. AR-02 (minor) asks the checklist to classify the unmapped raw-pull-trigger obligation as out-of-substrate/deferred. Neither finding invalidates the existing patch queue or reveals a missed structural obligation or a code behavior that contradicts a structural claim.

---

## Review-Use Boundary

This is a read-only adversarial review. Findings are decision input for the home lane — not approval, validation, readiness evidence, product proof, mandatory remediation, patch authority, or permission to keep any change. The home lane must adjudicate each finding before editing the checklist, code, tests, or repo map. This cross-vendor report sits alongside the prior same-vendor report; reconciling the two is Chief Architect / owner adjudication, not a synthesis this lane performs.
