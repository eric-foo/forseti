---
retrieval_header_version: 1
artifact_role: Orca adversarial implementation review report (decision input; read-only)
scope: >
  Read-only adversarial mixed implementation review of the creator public-handle
  linkage ledger scaffold update at diff 0e4881c6..a5c6e4bf (empty
  public_handle_ledger JSON scaffold, scaffold load+validate unit test, and three
  discovery pointers). Findings are decision input only; not approval, validation,
  readiness, or patch authority.
use_when:
  - Deciding whether the empty product ledger scaffold is safe as the next static,
    source-backed row-admission surface before SQLite promotion or real population.
  - Checking whether the scaffold, validator test, and discovery pointers preserve
    the public-handle-only and pre-SQLite boundary.
authority_boundary: retrieval_only
review_type: adversarial_mixed_implementation_review
output_mode: review-report
edit_permission: read-only
target_branch: codex/creator-ledger-static-fixture
target_base_commit: 0e4881c6d10bec966aa029ad1ec3435dc2cc6708
target_implementation_commit: a5c6e4bf468452dc9d6af3ac0f7a595349c6597c
commission_prompt: docs/prompts/reviews/creator_public_handle_linkage_ledger_scaffold_adversarial_implementation_review_prompt_v0.md
authored_by: GPT-5 / Codex home model (OpenAI lineage)
reviewed_by: claude-opus-4-8 (Anthropic lineage)
de_correlation_bar: cross_vendor_discovery
recommendation: no_blocker_or_major_findings
---

# Creator Public-Handle Linkage Ledger Scaffold — Adversarial Implementation Review v0

> Decision input only. This review is read-only advisory critique. It is **not**
> approval, validation, readiness, a formal PASS, mandatory remediation, or
> executor-ready patch authority. The two minor findings are clearly labeled
> optional / non-required. The commissioning CA adjudicates what (if anything) to act on.

## Commission / Provenance Receipt

- **Commission:** `docs/prompts/reviews/creator_public_handle_linkage_ledger_scaffold_adversarial_implementation_review_prompt_v0.md` (filed route-out from `workflow-delegated-review-patch`; a multi-file implementation/doc/test diff, correctly routed to a **read-only mixed implementation review**, not the single-target patch convention).
- **Target diff:** `0e4881c6d10bec966aa029ad1ec3435dc2cc6708..a5c6e4bf468452dc9d6af3ac0f7a595349c6597c` on `codex/creator-ledger-static-fixture` (worktree HEAD `62177e93`, which adds only the commission prompt; implementation surface equals the pinned `a5c6e4bf`; worktree clean).
- **Authority (read-only):** no patch authority, no working-tree edits, no patch queue, no runtime model recommendation, no validation/readiness/approval/no-new-seam claim. The only write is this durable report.
- **`authored_by`:** GPT-5 / Codex home model (OpenAI lineage) — from the commission and the prior delegated review record.
- **`reviewed_by`:** claude-opus-4-8 (Anthropic lineage) — reviewer self-disclosed (the model+version that performed this review); operator/CA may confirm on the durable record. Not fabricated; not a runtime-model recommendation, ranking, or selection.
- **`de_correlation_bar`:** `cross_vendor_discovery` — factual who-descriptor (author vendor OpenAI ≠ reviewer vendor Anthropic; both lineages disclosed) and full-diff discovery was performed. **Caveat:** this is a read-only *advisory* lane; it asserts **no** no-new-seam / PASS / readiness / validation standard regardless of the bar. The bar records who ran it, not a strict outcome.

## Source Context Status — `SOURCE_CONTEXT_READY`

**Method sequence (per commission + `.agents/workflow-overlay/`):** Read `AGENTS.md`; overlay `README.md`, `source-loading.md`, `review-lanes.md`, `delegated-review-patch.md`, `prompt-orchestration.md`, `safety-rules.md`, `validation-gates.md`. REFERENCE-LOADed `workflow-deep-thinking`, `workflow-code-review`, `workflow-adversarial-artifact-review` before source readiness; APPLIED only after this declaration. Both review skills were available in this runtime (no `BLOCKED_REVIEW_LANE_UNAVAILABLE`).

**Source-read ledger (decisive reads):**

| Source | Why read | Supports | State |
| --- | --- | --- | --- |
| Diff `0e4881c6..a5c6e4bf` (full + name-status) | Define exact change surface | Scope: 5 files, +54/−5; validator/models NOT touched | clean |
| `…/creator_public_handle_linkage_ledger_v0.json` (new, 22 lines) | The reviewed artifact | Q1, Q2, Q5, Q7 | clean |
| `…/creator_public_handle_linkage_ledger_spec_v0.md` (full) | Spec Status/open_next edit; contract | Q2, Q4, Q5, Q7 | clean |
| `orca-harness/tests/unit/test_creator_public_handle_linkage.py` (full) | Scaffold test + cross-tree path | Q1, Q3 | clean |
| `orca-harness/capture_spine/creator_public_handle_linkage/validation.py` (full) | Validator behavior for empty/real mode + guards | Q1, Q5, Q7 | clean (unchanged by diff) |
| `…/creator_public_handle_linkage/models.py` (full) | Allowed modes, default non-claims, enums | Q1 | clean (unchanged by diff) |
| `…/fixtures/creator_public_handle_linkage/valid_synthetic_ledger.json` | Synthetic-mode contrast; guard exercise | Q1, Q3 | clean |
| `docs/review-outputs/…delegated_adversarial_code_review_patch_v0.md` | Prior hardening (CR-01..03, AR-01) to avoid re-litigation | Q1, residuals | clean |
| `docs/decisions/wind_caller_calibration_carveout_v0.md` (full) | Controlling authority / fitness reference | Q7, R2 | clean |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` (changed row) | Pointer truthfulness | Q4 | clean |
| `orca/product/spines/capture/core/source_capture_toolbox/README.md` (changed rows) | Pointer truthfulness | Q4 | clean |

**Available, not read in full (not decision-bearing for these findings):** `ig_creator_roster_frontier_ledger_spec_v0.md`, `ig_creator_ideal_audience_inference_spec_v0.md`. Justification: the empty scaffold cannot absorb Tier-2-A audience/demographic attributes because the validator's forbidden-field sweep runs **unconditionally in all modes** (see Q7/R2); what those specs *want* to store cannot enter this ledger regardless of their content, and the prior delegated review already verified code-level separation (no import/wiring). Reading them could not change a finding.

**Fitness reference (intent-bearing target):** `docs/decisions/wind_caller_calibration_carveout_v0.md` — Tier-2-B public-handle↔public-handle stitching ACTIVATED (council-cleared 2026-06-22), built through a dedicated linkage spec; Tier-2-A aggregate audience demographics COUNCIL-CONFIRMED (2026-06-23) with the **remaining gate named as "a schema home (the ledger currently forbids demographic fields)"**; Tier-3 (contact/outreach, special-category, private, resale, external person-level surface) absolute. Treated as an axis to attack, not a pass bar.

## Recommendation — `no_blocker_or_major_findings`

The empty scaffold is safe as the next static, source-backed row-admission surface before SQLite/real population. No critical or major findings. Two **minor / optional** advisory findings and four named residual risks follow. Independent verification confirms the scaffold validates, the doc pointers resolve, and the new file adds no placement blocker.

## Findings (severity order; finding-priority labels only — no approval/rejection/readiness authority)

No `critical`. No `major`.

### AR-IM-01 — `minor` (optional hardening) — JSON does not self-document its empty / pre-SQLite / scaffold lifecycle status

- **Phase:** correctness (boundary representation). **Review target:** is the product JSON a truthful empty/manual-ready ledger that cannot be over-read (Q2)?
- **Location:** `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json` — `ledger_mode: "public_handle_ledger"` (L5), `source_policy_posture` (L11), `non_claims` (L13–19).
- **Evidence:** the artifact's only lifecycle signal is the three empty lists. `ledger_mode` reads as the production mode (the synthetic fixture uses `synthetic_fixture`), and `source_policy_posture` describes linkage **scope** ("Tier-2-B public-handle-to-public-handle linkage only; … no live platform capture; no contact, outreach, audience, follower, or person-identity surface"), not **lifecycle**. The "empty until source-backed public-handle evidence" and "no SQLite" framing lives only in adjacent docs (spec L39–42; toolbox README; consolidation map row), not in the artifact.
- **Strongest defense (why it partially holds):** a reader opening only the JSON sees empty `platform_accounts`/`account_link_evidence`/`creator_records` → "already populated" is **not** inferable; `source_policy_posture` explicitly says "no live platform capture" → "live capture authorized" is **not** inferable; it is a JSON file → "SQLite begun" is **not** inferable. The core over-read vectors the goal names are already negated **by the artifact itself**. The residual is narrower: nothing in the file states it is a *scaffold* / *pre-SQLite* / *rows require source-backed public-handle evidence*; detached from its docs, that status is not self-evident.
- **Impact:** low. The representation is truthful, merely under-documented in-artifact. Misread risk, not a false statement.
- **minimum_closure_condition:** the artifact self-states its empty-scaffold / pre-SQLite / source-backed-evidence-required lifecycle (e.g., extend `source_policy_posture`, or add `non_claims` such as "not SQLite migration" and "empty scaffold; rows require source-backed public-handle evidence"). The validator permits this — `_validate_non_claims` requires the five defaults as a **subset** and does not forbid additional entries (validation.py L580–586); `source_policy_posture` is a free string (L213–217).
- **next_authorized_action:** owner/author decision to add the optional in-artifact lifecycle line, or accept the in-doc framing as sufficient. No patch authority in this lane.
- **patch_queue_entry:** not authorized (read-only lane). Advisory direction only. Red-green: not applicable (non-executable representation hardening).

### CR-IM-02 — `minor` (optional hardening) — scaffold test couples a harness "unit" test to the repo-root product tree via `parents[3]`

- **Review target:** does the scaffold test locate the product file robustly and assert the right minimum invariants without becoming brittle (Q3)?
- **Location:** `orca-harness/tests/unit/test_creator_public_handle_linkage.py` L22–32 (`PRODUCT_LEDGER_PATH`), L62–69 (`test_product_public_handle_ledger_scaffold_loads_and_validates`).
- **Evidence:** `PRODUCT_LEDGER_PATH = Path(__file__).resolve().parents[3] / "orca" / "product" / … / "creator_public_handle_linkage_ledger_v0.json"`. From `orca-harness/tests/unit/`, `parents[3]` resolves to repo root; the path is correct in-repo. The test calls `load_creator_public_handle_linkage_ledger(PRODUCT_LEDGER_PATH)` (load **and** validate) then asserts `ledger_mode == "public_handle_ledger"` and the three lists are `[]`.
- **Strongest defense (why it mostly holds — this is NOT fake success):** the cross-tree reach is a deliberate guard so the committed product scaffold cannot silently drift out of validity. It is a **real, failable** gate — it would fail (a validator `CreatorPublicHandleLinkageError`, or `FileNotFoundError`) if the JSON were absent, malformed, mode-wrong, or non-empty. Independently re-ran the focused suite: **22 passed**.
- **Residual:** it is categorically an integration/contract check sitting in the `unit/` folder, and it reaches out of `orca-harness/` into the repo-root `orca/product/` tree. It would break with `FileNotFoundError` if the harness is ever packaged/extracted standalone, or the product JSON relocates — even though the validator logic is unchanged. Low-probability in a monorepo; surfaced because it presents as a confusing unit-test failure rather than the structural cause.
- **Impact:** low. Locality/brittleness, not a correctness defect today.
- **minimum_closure_condition:** the cross-tree dependency is acknowledged (e.g., a comment marking it a product-artifact contract check, or centralizing the repo-root resolution) so a future harness-packaging change does not surface as a mysterious unit-test failure.
- **next_authorized_action:** owner/author decision; no patch authority here.
- **patch_queue_entry:** not authorized. Advisory only. Red-green: not applicable (test-structure note, current behavior verified green).

## Non-Findings / Verified-Clean (mapped to Review Questions)

- **Q1 — Empty scaffold validates; no guard weakening.** The diff touches neither `validation.py` nor `models.py` (name-status: only the JSON, the test, the spec, the map, and the README changed). `validate_creator_public_handle_linkage_ledger` accepts the empty real-mode ledger: `_ALLOWED_LEDGER_MODES` already includes `public_handle_ledger` (validation.py L85; models.py L56 — pre-existing, not introduced here); `_require` treats `[]` as present (not `None`, not empty-string; L595–599); empty `platform_accounts`/`account_link_evidence`/`creator_records` short-circuit their loops and return empty maps (L265–269, L322–329, L383–389). Forbidden person/audience/contact data is blocked in **all** modes by the unconditional `assert_no_forbidden_output_fields` sweep (L192, L235–249) over `_FORBIDDEN_OUTPUT_FIELDS` (L117–169). Synthetic-fixture guards are mode-gated (L316–318) and untouched — **not weakened**. The prior delegated review's CR-01/02/03 hardening is present in this validator (`_require_str` scalar typing L602–611; independence-family check L466–479; `urlparse` host check L563–565), so those are closed and out of this diff's scope. **Independently re-ran focused suite: 22 passed.**
- **Q2 — Truthful empty/manual-ready representation.** Three record lists empty; `source_policy_posture` states "no live platform capture; no contact, outreach, audience, follower, or person-identity surface"; the five required non_claims present. "Already populated / live-capture authorized / SQLite begun" are not inferable. (Only residual: in-artifact lifecycle self-documentation → AR-IM-01.)
- **Q3 — Real, failable scaffold gate.** Loads+validates and asserts mode + three empty lists; would fail on malformed/mode-wrong/non-empty input. (Cross-tree coupling → CR-IM-02.)
- **Q4 — Pointers truthful; no stale paths; no authority grant.** Consolidation-map row now lists the JSON with a truthful note ("static ledger/validator only; empty until source-backed public-handle evidence; no live capture, no contact/outreach, no SQLite"); toolbox README row + prose truthful ("Empty static `public_handle_ledger` scaffold … no invented rows, live capture, contact/outreach, SQLite, or person identity proof"); spec `open_next` adds the JSON (L17). `authority_pointers` retains the required `wind_caller_calibration_carveout_v0.md` pointer, which the validator enforces (L255–259). None of the edits grant runtime/capture authority. **Independently re-ran `check_map_links --changed --strict`: OK (0 findings)**, 33 annotated nonresolving debt entries (matches author).
- **Q5 — Relational/table-shaped migration path preserved.** `creator_records`, `platform_accounts`, and `account_link_evidence` are all present as explicit empty lists, each required by `_require` (L198–212) — so they stay explicit even when empty, and a future SQLite migration maps one list → one table without a contract change. Spec "Ledger Shape" (L59–69) intact.
- **Q6 — `check_placement.py`: no new blocker (independently verified).** Re-ran `check_placement.py --changed --strict`: exit 1, but driven entirely by **11 pre-existing top-level-area violations** (`.gitattributes`, `.githooks/*`, `.github/*`) + 4 freshness + 960 legacy-tolerated warn-only. The new JSON `creator_public_handle_linkage_ledger_v0.json` is **not present anywhere in the output** (grep: 0 hits); the prompt/report paths are also unflagged; the `creator_public_handle_linkage` orca-harness files appear only as pre-existing `LEGACY` (warn-only) entries. The new product JSON lands clean under `orca/product/spines/capture/core/source_families/social_media/`. **Correction carried for the CA:** the prior delegated review cleared placement by reasoning "this branch adds **no new files**" — that reasoning does **not** cover this diff, which adds one new file; I verified the new file directly instead of inheriting that reasoning.
- **Q7 — Public-handle↔public-handle stitching preserved; LLM evidence assistive-only.** Validator forbids `confirmed_public_account_link` (L428–429), requires human review for declared/probable links (L458–465), blocks LLM-only final links and `llm`/`model` review actors (L490–497), and rejects non-public-handle evidence types (closed enum; e.g. `email_match` → `invalid_evidence_type`, test L158–162). The scaffold's `source_policy_posture` asserts "public-handle-to-public-handle linkage only; no non-public-handle joins." Empty now; future rows inherit these guards.

## Residual Risks (named; not defects of this diff)

- **R1 — `public_handle_ledger` real-mode hygiene is weaker by design (no-person-identity / no-live-capture boundary).** Real mode skips the synthetic-only guards (`_validate_synthetic_account`: `synthetic_`/`fixture_` handle prefix, `example.test` host, `synthetic_fixture` marker, `synthetic_fixture:` source pointers — L316–318, L557–572). For the **empty** scaffold this is inert (no rows). When the first real row is admitted, real-mode integrity rests on the unconditional forbidden-field sweep + the four structural allowlists + the link-state evidence thresholds + the LLM-only block + the ≥2-platform requirement — **not** on the synthetic markers. Defensible (real handles/URLs are real) and already named by the prior delegated review; carried so the CA notes it before real population.
- **R2 — Tier-2-A audience-absorption misread (watch item).** The carve-out (2026-06-23, L165–175) names Tier-2-A's remaining gate as "a schema home (the ledger currently forbids demographic fields)," and this empty ledger is now the freshest adjacent schema → a future agent could misread it as that home. **Structurally blocked today:** the unconditional forbidden-field sweep denylists `age`, `gender`, `ethnicity`, `followers`, `follower_graph`, `audience_graph`, `contact`, `email`, etc. in all modes (L117–169, L192, L235–249), and the nested-blob bypass that would have smuggled `age_band_*`/`gender_skew` under a scalar key is **closed** by CR-01's `_require_str` typing (tests L194–226). Mitigated further by the prior review's AR-01 disjointness note. Not a defect of this diff; a boundary the CA should re-affirm when the Tier-2-A schema-home decision is actually made (it must be a **separate** artifact, not this ledger).
- **R3 — No new `direction_change_propagation` receipt for this scaffold-landing diff.** The diff edits the spec Status (L36–42) + `open_next` (L17), the consolidation-map row, and the toolbox README, and adds the new JSON, but carries no new DCP receipt for *this* change. **Assessment: not strictly required.** No newly-changed enumerated doctrine dimension (product/architecture/workflow/validation/review/output/lifecycle) — the static-ledger-before-SQLite doctrine was already propagated by the spec's existing receipt (spec L206–246), and `check_dcp_receipt.py` (EP-09) validates only receipts that are *present* and never forces presence (validation-gates.md). The spec's existing receipt's `controlling_sources_updated` predates and does not list the new JSON, which is consistent with dated-historical receipts not being retro-edited. Surfaced for CA judgment; not a blocker.
- **R4 — Inherited, out of this diff's scope.** Loose timestamp formats (`created_at`/`updated_at`/`observed_at`/`handle_observed_at` are string-typed but not format-validated) and the `review_actor` LLM-name heuristic are unchanged prior-review residuals; not touched here. Acceptable for v0.

## Validation Evidence Inspected + Gaps

**Independently re-run (this review, target worktree, clean env where applicable):**
- Focused unit suite — `python -m pytest … orca-harness/tests/unit/test_creator_public_handle_linkage.py` → **22 passed** (confirms author's report; confirms the empty scaffold validates and all guards fire).
- `check_map_links.py --changed --strict` → **OK (0 findings)**, 33 annotated nonresolving debt (matches author).
- `check_placement.py --changed --strict` → **exit 1 from pre-existing top-level debt only**; new JSON and prompt/report paths not implicated (Q6 independently verified).

**Author-reported, accepted, not independently re-run (with reason):**
- Full `orca-harness/tests/unit` suite (1587 passed, 1 skipped, clean env). The prompt's `ORCA_DATA_ROOT` caveat is an **environmental test-isolation** issue (14 source-capture/data-lake tests write under `F:\orca-data-lake` unless `ORCA_DATA_ROOT` is cleared), **not** hidden ledger success — accepted as stated.
- `check_retrieval_header.py --changed --strict` (author exit 0) and `check_repo_map_freshness.py --changed --strict` (author exit 0). Not re-run; the adjacent map-link surface I did re-run passed.
- `python -m json.tool` on the JSON — superfluous: the focused unit test already parses and loads the file.

**Gaps (do not affect the no-blocker recommendation):** retrieval-header and full-suite checks are author-reported rather than reviewer-reproduced; the diff is docs + one empty JSON + one additive test, and the load-bearing surfaces (focused tests, map-links, placement) were independently verified. No strict PASS/readiness/validation claim is made by this review regardless.

## Review-Use Boundary

These findings and residuals are decision input for the commissioning CA only. They are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until separately accepted or authorized under the per-lane PR flow. Both findings are explicitly optional/non-required. No `NEEDS_ARCHITECTURE_PASS`: every item is a local representation/test-locality nicety or a named forward residual, not a design-level defect; the Tier-2-A schema home remains a correctly-deferred separate decision.

## Courier Summary For The Commissioning CA

```yaml
review_summary:
  commission: docs/prompts/reviews/creator_public_handle_linkage_ledger_scaffold_adversarial_implementation_review_prompt_v0.md
  target: diff 0e4881c6..a5c6e4bf (codex/creator-ledger-static-fixture) — empty public_handle_ledger JSON + scaffold test + 3 doc pointers
  authority: read-only adversarial mixed implementation review; no patch/validation/readiness authority
  fitness_reference: docs/decisions/wind_caller_calibration_carveout_v0.md (Tier-2-B active public-handle-only; Tier-2-A council-confirmed, schema-home still separate; Tier-3 absolute)
  source_context: SOURCE_CONTEXT_READY
  reviewed_by: claude-opus-4-8 (Anthropic lineage)   # reviewer self-disclosed; operator/CA may confirm
  authored_by: GPT-5 / Codex home model (OpenAI lineage)
  de_correlation_bar: cross_vendor_discovery          # factual who-descriptor; advisory lane makes no no-new-seam/PASS claim
  recommendation: no_blocker_or_major_findings
  findings:
    - id: AR-IM-01
      severity: minor
      optional: true
      summary: JSON does not self-document empty/pre-SQLite/scaffold lifecycle; truthful but under-documented in-artifact (Q2).
      minimum_closure_condition: artifact self-states empty-scaffold/pre-SQLite/source-backed-evidence-required status (validator allows extra non_claims / free posture string).
      next_authorized_action: owner/author optional add, or accept in-doc framing.
    - id: CR-IM-02
      severity: minor
      optional: true
      summary: scaffold test reaches harness→product tree via parents[3]; correct & green (22 passed) but brittle to harness packaging/relocation (Q3).
      minimum_closure_condition: cross-tree dependency acknowledged / repo-root resolution centralized.
      next_authorized_action: owner/author optional refactor.
  residual_risks:
    - R1 public_handle_ledger real-mode skips synthetic-only guards (by design; inert while empty; matters at first real row).
    - R2 Tier-2-A audience-absorption misread — structurally blocked today (unconditional forbidden-field sweep + closed CR-01 nested-blob hole); CA re-affirm at schema-home decision.
    - R3 no new DCP receipt for this diff — assessed not strictly required (no new doctrine dimension; EP-09 never forces presence); CA judgment.
    - R4 inherited loose-timestamp / review_actor-heuristic residuals; out of this diff's scope.
  verified_clean: [Q1 empty validates/no guard weakening, Q2 truthful empty, Q4 pointers truthful + map_links OK, Q5 relational lists explicit when empty, Q6 no new placement blocker (verified — corrects prior 'no new files' reasoning), Q7 public-handle-only + LLM-assistive-only preserved]
  independent_validation: [focused tests 22 passed, check_map_links --strict OK 0 findings, check_placement exit1 from pre-existing top-level debt only — new JSON not implicated]
  non_claims: [not approval, not validation, not readiness, not mandatory remediation, not patch authority, not no-new-seam, not runtime/SQLite/live-capture authorization]
  next_authorized_action: CA adjudicates the two optional findings and the residuals; no blocker to proceeding with the scaffold as the next static row-admission surface.
```
