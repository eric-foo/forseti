# Engagement Resonance Enforcement P1–P3 Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review output (implementation/code review + bounded artifact-leakage check)
scope: >
  Adversarial implementation/code review of the first three engagement-resonance
  enforcement checkers (P1 DCP receipt hygiene, P2 registry/list sync, P3 stale
  doctrine phrase sweep) plus the .agents/hooks/README.md rows, on branch
  codex/search-surface-mgt-p0-captures-ws, diff range 182ee24c..6fffd769.
use_when:
  - CA adjudication of whether the P1–P3 checker batch is fit to land / wire.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
source_context_status: SOURCE_CONTEXT_READY
commissioned_by: docs/prompts/reviews/engagement_resonance_enforcement_p1_p3_adversarial_code_review_prompt_v0.md
recommendation: accept_with_friction
```

## 0. Commission, Target, Authority

- **Commission.** Independent, de-correlated adversarial implementation/code review of the P1–P3 checker batch (commits `e88ed222`, `51f839e5`, `6fffd769`); read-only review lane; recommend fixes, do not patch. Findings are decision input only.
- **Target (confirmed).** Workspace `C:\Users\vmon7\Desktop\projects\orca\worktrees\search-surface-mgt-p0-captures`, branch `codex/search-surface-mgt-p0-captures-ws`. HEAD is `f32318e8` (one later prompt-only commit, `docs: add P1-P3 enforcement review prompt`); the four target files are **unchanged since the expected target head `6fffd769`** (`git diff 6fffd769..HEAD` over the targets is empty). The batch is exactly the three named commits, +1286 lines across 4 files. Worktree clean except the explicitly-allowed untracked `docs/prompts/hygiene-queue/`. `workspace_preflight` gate **passes**.
  - `.agents/hooks/check_dcp_receipt_hygiene.py` (+445)
  - `.agents/hooks/check_registry_list_sync.py` (+361)
  - `.agents/hooks/check_engagement_stale_phrases.py` (+471)
  - `.agents/hooks/README.md` (+9)
- **Authority used (read in full).** `source-of-truth.md` (DCP receipt contract §"Doctrine Change Propagation Contract", lines 106–131), `validation-gates.md` (Enforcement Placement, lines 214–249; bucket policy, lines 13–22), `review-lanes.md` (lane + provenance + two-bar de-correlation), `delegated-review-patch.md`, `engagement_logic_registry_v0.md`, `core_spine_v0_information_production_foundation_v0.md`, `engagement_resonance_enforcement_goal_handoff_v0.md`, overlay `README.md`, `docs/decisions/dcp_receipts_archive_v0.md`; adjacent `check_doc_terms.py` (full) and `check_commission_signal_board_output.py` / `check_csb_scanning_artifact.py` (targeted). Method: `workflow-deep-thinking` → `workflow-code-review` (zero-config findings + repo-visible authority) → bounded `workflow-adversarial-artifact-review` for the README.
- **De-correlation.** Author vendor = OpenAI/GPT (`openai-gpt-5-codex`); reviewer vendor = Anthropic/Claude (`claude-opus-4.8`). Different vendor lineage → **`cross_vendor_discovery`** (the discovery bar; review-lanes.md lines 122–137). `reviewed_by` is the model actually performing this review; not fabricated. No `same_vendor_rationale` needed.

## 1. Decision Criteria (fitness axis — attacked, not assumed)

Goal (prompt Fitness Reference + goal handoff): three narrow, deterministic checkers that let future agents run a shape/leakage check instead of re-reading broad doctrine, **without** any proof/validation/readiness/acceptance/resonance-judgment claim, without scoring engines / schema-runtime / broad CI gates, and with false positives bounded to mechanical, source-visible failures. The batch is judged against that bar and against its cited rule authority — not "pass if it matches its own selftest."

## 2. Findings (severity-ordered; findings-first)

Severity uses `major` / `minor` / `advisory` (review-lanes.md lines 73–76); labels carry no approval, rejection, readiness, validation, or mandatory-remediation authority. No `critical` finding exists — the core detection logic is sound. No `patch_queue_entry` is emitted (read-only lane; advisory remediation direction only).

### CR-01 (major) — Empty selection returns exit 2 (usage) in the DCP and stale checkers; inconsistent with the registry checker and a false-`GATE FAIL` risk once wired

- **Phase:** correctness (code).
- **Location:** `check_dcp_receipt_hygiene.py:437`–`439` (`if not relpaths: parser.print_usage(...); return 2`); `check_engagement_stale_phrases.py:463`–`465` (same). Contrast `check_registry_list_sync.py:350`–`355` (`if not selected: if args.paths or args.changed or args.staged: print "...OK"; return 0`).
- **Evidence (empirically confirmed).** With nothing staged: `check_dcp_receipt_hygiene.py --staged --strict` → prints usage, **exit 2**; `check_engagement_stale_phrases.py --staged --strict` → usage, **exit 2**; `check_registry_list_sync.py --staged --strict` → `no registered binding files selected -- OK`, **exit 0**. The same `if not relpaths` path is hit by `--changed` on a clean tree and by `--changed`/`--staged` when **git is unavailable** (`git_lines` returns `[]`). Because the guard precedes the `--strict` check, exit 2 occurs even in advisory mode.
- **Impact.** The README markets these as "manual / commit / CI candidate" with a `--strict` gate. validation-gates.md (lines 20–22) buckets "unknown nonzero exits … default to `GATE FAIL`," and any `--strict` exit ≠ 0 in a pre-commit/CI runner blocks. So a commit that changes **no** in-scope durable doc (DCP) or **no** live doctrine (stale) would be reported/blocked as a gate failure — the most common no-op path. The registry checker already models the correct behavior, so this is also an intra-batch inconsistency. The prompt's robustness question ("…robust when … selected files are unrelated?") is answered **no** for two of three checkers.
- **Bound / not-overstated.** Latent today: the three new checkers are **not** wired into `.claude/settings.json` (README lines 50–58 register only guard + retrieval-header + repo-map). The defect bites only when promoted to a `--strict` commit/CI gate. Fix is trivial and localized.
- **minimum_closure_condition:** when a selection mode (`--staged` / `--changed` / `--live`) is explicitly requested but the resulting selection is empty, the DCP and stale checkers exit 0 (nothing in scope = pass); exit 2 (usage) is reserved for "no mode and no paths at all," matching `check_registry_list_sync.py`.
- **next_authorized_action:** CA decision → separate patch turn (mirror the registry checker's guard). Verification = red-green: `--staged --strict` (nothing staged) exits 2 before, 0 after.

### CR-02 (minor) — README rule-authority sentence (lines 27–29) does not match the three new checkers' cited authority (misleading doc)

- **Phase:** correctness (artifact / doctrine-leakage check on README).
- **Location:** `.agents/hooks/README.md:27`–`29`: "Rule authority lives in the overlay (`.agents/workflow-overlay/safety-rules.md`, `validation-gates.md`) — the scripts reference it, they don't restate it."
- **Evidence.** The three new checkers cite different owning authority: DCP → `source-of-truth.md` (`check_dcp_receipt_hygiene.py:36`, and validation-gates.md:35–42 explicitly **defers** receipt mechanics to source-of-truth.md); registry → `engagement_logic_registry_v0.md` + `core_spine_v0_information_production_foundation_v0.md` (`check_registry_list_sync.py:11`–`12`); stale → `engagement_resonance_enforcement_goal_handoff_v0.md` + the registry (`check_engagement_stale_phrases.py:9`–`11`). Neither safety-rules.md nor validation-gates.md is the cited authority for any of the three. The blanket sentence was accurate for the older guard/retrieval rows it sits under, not for the new rows.
- **Strongest defense, and why it fails.** "validation-gates.md carries enforcement-placement authority, so it's not wrong." It fails because the sentence claims that is *where the rule authority lives* and that *the scripts reference it* — but the scripts reference source-of-truth.md / the product docs / the goal handoff, so a reader using the README to locate (e.g.) the DCP rule is misdirected. This also sits in mild tension with the goal-handoff secondary signal "Checkers cite their owning doctrine" — the scripts do; the README summary doesn't match them.
- **minimum_closure_condition:** the README's authority sentence reflects that each new checker names its own `RULE_AUTHORITY` (source-of-truth.md / the two product docs / the goal handoff), or is scoped to the guard/retrieval hooks it actually describes.
- **next_authorized_action:** CA decision → doc patch turn (navigation doc; low risk). No red-green test applicable (`not_applicable`; prose accuracy).

### CR-03 (minor) — Selftests are fully synthetic; none pin live-doc shape, so a real heading/format drift breaks `--live`/scope with no selftest failure

- **Phase:** correctness (test coverage / regression resilience).
- **Location:** `check_dcp_receipt_hygiene.py:264`–`403`; `check_registry_list_sync.py:237`–`319`; `check_engagement_stale_phrases.py:364`–`430` — all exercise pure functions over inline synthetic fixtures only.
- **Evidence.** The registry checker's `--live` correctness depends entirely on the live Foundation heading being exactly `Allowed Signal Uses` and the registry heading exactly `Signal Use Classification` with `- ` bullets (`check_registry_list_sync.py:58`–`64`, `121`–`153`). No selftest asserts the live docs still parse. A heading rename, a `-`→`*` bullet switch, or a section restructure would silently degrade the registry check from "containment" to a `source_list_missing` / `registry_list_missing` error, and degrade DCP/stale scope, with the selftest still green. The sibling `check_doc_terms.py:328`–`336` guards exactly this with a live-faithfulness assertion (reads the real `ontology.yaml`, asserts head-nouns and canonical count).
- **Partial mitigation.** `--live` is self-revealing when actually run (the registry `--live` would emit `source_list_missing` on a renamed heading — a visible signal, not silent corruption). The gap is that a **selftest-only** CI step passes while `--live` is broken.
- **minimum_closure_condition:** add a live-faithfulness assertion (at minimum: the registry binding's live headings resolve to non-empty bullet lists; ideally the known binding parses end-to-end), or record the gap as an accepted residual with rationale, consistent with `check_doc_terms.py`.
- **next_authorized_action:** CA decision; **optional hardening** (clearly optional, non-blocking). Verification = the new assertion fails against a renamed-heading fixture and passes against the live docs.

### CR-04 (minor) — DCP scope includes `docs/prompts/`; example/historical receipts there are guarded only by the heading-region heuristic, and the archive-pointer match is wording-brittle

- **Phase:** correctness (scope + parsing residuals; merged).
- **Evidence.**
  - **Scope asymmetry.** DCP `SCOPE_PREFIXES` includes `docs/` and `EXCLUDED_PREFIXES` excludes only `docs/_inbox/`, `docs/review-inputs/`, `docs/review-outputs/` (`check_dcp_receipt_hygiene.py:40`–`49`). The stale checker additionally excludes `docs/prompts/`, `docs/hygiene/`, `docs/migration/` (`check_engagement_stale_phrases.py:41`–`48`). So prompt/handoff records under `docs/prompts/` are **in** DCP scope. This is partly by-design — the DCP contract explicitly permits receipts "inline in the changed artifact, **prompt**, handoff" (source-of-truth.md:106), so checking prompts is defensible — but it means a historical/template prompt that shows example receipts can be flagged.
  - **Example-vs-active relies on one heuristic.** `dcp_scan_region` (`:142`–`157`) excludes a schema example **only** when it precedes the first `## Direction Change Propagation` heading. A doc with example receipts but **no** such heading is scanned wholesale; a single example block then trips `missing_dcp_archive_pointer`. (The same heuristic is what *correctly* excludes the two schema examples in source-of-truth.md, so it is a deliberate trade-off — but it is the only guard.) Symmetric false-negative: real receipts placed **before** the first DCP heading are silently un-counted (potentially to 0).
  - **Pointer brittleness.** `ARCHIVE_POINTER_LINE_RE` (`:56`–`58`) requires the literal word "older receipt(s)" or "archived" **and** the exact archive path on one line. A valid pointer with other wording (e.g., "see the DCP archive at …") or split across lines → false `missing_dcp_archive_pointer`.
  - **No live false positive observed today:** the one in-scope untracked prompt (`docs/prompts/hygiene-queue/precompact_search_surface_trends_next.md`) ran clean (`--changed --strict` exit 0), and this review prompt itself is not flagged.
- **minimum_closure_condition:** CA decides whether `docs/prompts/` is intended DCP scope (accept the heading-region heuristic as the example guard) or should be excluded like the stale checker; optionally broaden the pointer match / count receipts independent of heading position. Either way, the residual is documented.
- **next_authorized_action:** CA decision on intended DCP scope; **optional** parsing hardening. Belongs to the goal-handoff "accepted residuals" class (lines 96–101, 183–189).

### CR-05 (advisory / context) — Run against live overlay files, the DCP checker flags real pre-existing receipt-hygiene debt in its own authority files; surfaces the file-scoped (not line-scoped) forward-only residual

- **Phase:** correctness signal + risk (not a checker defect).
- **Evidence (empirical probe, `--strict`, explicit absolute paths — also exercises the `to_relposix` absolute branch).**
  - `.agents/workflow-overlay/source-of-truth.md` → `too_many_inline_dcp_receipts: Found 3`, exit 1 (3 inline receipts > the 2 its own §Doctrine-Change contract sets; the two schema examples at the file's lines 116/137 are correctly excluded as pre-heading).
  - `.agents/workflow-overlay/validation-gates.md` → `too_many_inline_dcp_receipts: Found 3` **and** `missing_dcp_archive_pointer`, exit 1 (3 inline + no archive-pointer line).
  - `delegated-review-patch.md` and `engagement_logic_registry_v0.md` → exit 0 (2 inline + pointer, clean).
  - `docs/decisions/dcp_receipts_archive_v0.md` → **exit 0** despite 21+ receipts and H3 `### Direction Change Propagation …` headings — the `is_authorized_archive` short-circuit holds (no false positive).
- **Reading.** (i) **Positive:** strong evidence the DCP checker is non-trivial — true positives on real violations, correct exclusion of the authorized archive, correct pass on clean files. (ii) **Risk:** the checker is **file-scoped, not diff-scoped** — it counts all receipts in a changed file, not just the touched hunk. So a future edit to source-of-truth.md or validation-gates.md (for any reason) under `--changed --strict` would surface this pre-existing debt as a blocking finding. This is consistent with the existing forward-only file-granular pattern (header_index.py), so it is a residual to document, not necessarily to change. (iii) **Separate out-of-scope debt:** source-of-truth.md and validation-gates.md currently violate the 2-inline rule (validation-gates.md also lacks the required pointer). This is **not** the batch's responsibility and **not** actionable in this read-only lane; flagged for CA awareness only. (delegated-review-patch.md carries a stale self-note at its lines 279–283 claiming a >2 overflow, but it actually holds 2 inline + pointer and passes — also out of scope.)
- **minimum_closure_condition:** none for the checker (behavior correct); optionally document the file-vs-diff scope in the README. The overlay-file debt closes via a separate hygiene pass (rotate older receipts to the archive) — explicitly out of scope here.
- **next_authorized_action:** CA awareness; optional separate hygiene lane for the overlay files.

## 3. What Holds (verified — stated after findings)

- **Selftests.** All three `--selftest` pass, exit 0 (DCP 11/11, registry 6/6, stale 7/7). No timeout (smoke probe clean).
- **Advisory/strict contract, no fake fail-open success.** `report()` in each: findings + `--strict` → exit 1; findings without `--strict` → advisory message, exit 0; clean → exit 0. A strict finding correctly exits non-zero (no fake success path). The one wrong exit is the empty-selection path (CR-01), which is over-strict, not fail-open.
- **P2 headline drift detection (the core deliverable).** `check_registry_list_sync.py --live` flags exactly `actor-strategy evidence` missing from the registry (Foundation `Allowed Signal Uses`:`…foundation…:267–283` has it; registry `Signal Use Classification`:`…registry…:163–179` has `competitor-strategy evidence` instead); `--live` exit 0 (advisory), `--live --strict` **exit 1** — matches the prompt's stated expectation. One-direction containment only (Foundation ⊆ registry); no bidirectional enforcement, no auto-promotion, no category-correctness decision. The specific drift token is **not** hardcoded into the live binding (only into fixtures) — it is detected dynamically.
- **P3 leakage sweep.** `--live --strict` → `OK (326 files checked, 0 skipped)`, exit 0, with 16 self-reference/DCP matches correctly ignored. Zero false positives across 326 live doctrine files; the current non-claim wording ("not proof / numeric score boost", "must not interpret whether engagement proves demand") is not flagged; live/excluded scoping (excludes prompts, reviews, hygiene, migration, archive) and the DCP-fence self-reference exemption both work.
- **P1 shape checks.** Verified true-positive and correct-exclusion behavior on real files (CR-05). `--changed --strict` clean on the current tree; `git diff --check 182ee24c..6fffd769` clean.
- **No overclaim leakage.** Targeted search confirms every `validation|readiness|proof|acceptance|score|scoring|ontology|schema|CI|runtime` hit in checker source is a BOUNDARY disclaimer, a curated stale *pattern*, a selftest fixture, or an appropriately tentative README "candidate" row. The README rows + footer make no validation/readiness/proof/acceptance/CI-promotion claim; "When" column reads "manual / commit / CI candidate." Boundary docstrings are present and faithful in all three scripts.
- **Pattern reuse.** The advisory/strict `report()` shape and the enforcement-placement model (validation-gates.md:214–233: write-time hook + portable `--strict` checker that references authority and never restates it) are followed; this matches the goal-handoff secondary signal. P4–P6 are correctly **not** implemented in this batch.

## 4. Review-Question Coverage (prompt §"Review questions")

- DCP enforces exactly the claimed shape (≤2 inline, pointer-after-receipts, no unauthorized standalone) — **yes**, faithful to source-of-truth.md:106–111 (incl. pointer required even for one receipt). Heading-region / pointer-wording / pre-heading-receipt edges → **CR-04**.
- DCP false-flags schema examples / authorized archive / non-md checker names / historical records — examples & archive & `.py` names **correctly excluded** (selftest + live probe); **historical prompt records under `docs/prompts/` are NOT excluded** → **CR-04**.
- Registry enforces only the one accepted binding, no bidirectional/auto-promotion/ontology — **yes**; makes the known live drift visible without asserting product correctness — **yes** (CR-07 residual: cannot distinguish renamed-vs-missing, by design).
- Stale flags curated phrases in live doctrine; excludes historical/self-reference; avoids false positives on current non-claim wording — **yes, all three** (326-file live run + selftests).
- Advisory/strict preserved, no fake fail-open — **yes**, except the empty-selection over-strict exit-2 → **CR-01**.
- Modes scoped/robust (git-unavailable, absolute, directory, unrelated selection) — absolute paths **verified**; directory handled by `iter_md_under`; **empty/unrelated selection NOT robust for DCP+stale** → **CR-01**.
- Selftests catch regressions vs confirm strings — behavior-based (good) but **no live-faithfulness pin** → **CR-03**.
- README describes substrates, not validation/readiness/CI-promotion — **yes**, but authority pointer inaccurate → **CR-02**.
- Batch avoids runtime/schema/broad-grep/scoring/dashboards/doctrine-rewrite — **yes**.

## 5. Residual Risks & Not-Assessed Gaps

- **CR-07 (advisory residual).** registry-sync is pure string containment: `actor-strategy evidence` vs `competitor-strategy evidence` is reported as "missing," not "possibly renamed." Correct shape behavior; the prompt explicitly forbids vocabulary adjudication here. A reader should not over-read the finding as "category genuinely absent."
- **No fail-open wrapper.** Unlike `check_doc_terms.py` (and the guard), the three new checkers have no top-level `try/except → exit 0`; an unhandled internal exception would exit non-zero. Low stakes (not in the tool-blocking path), but inconsistent with sibling non-guard checkers.
- **Not assessed.** `--include-excluded` paths beyond selftest; passing a directory arg to DCP/registry (only stale globs dirs); non-UTF-8 / CRLF inputs; `core.quotepath`-quoted git output for non-ASCII paths; behavior under a real `--strict` commit/CI wrapper (not yet wired). Authority files `source-loading.md`, `prompt-orchestration.md`, `safety-rules.md`, `project-authority.md`, `artifact-roles.md` were not read in full (not decision-bearing for judging this Python; bindings triangulated via the files read in full); target `AGENTS.md` taken from session kernel context (same repo file). `check_commission_signal_board_output.py` / `check_csb_scanning_artifact.py` read via targeted search only.

## 6. Recommendation & Review-Use Boundary

- **Recommendation: `accept_with_friction`.** The batch achieves its goal — three narrow, deterministic, correctly-bounded checkers that detect real mechanical failures (registry drift, DCP shape, stale leakage) with no proof/validation/readiness/scoring claims and bounded false positives. Land as a manual/candidate substrate. **Close CR-01 before wiring any of these as a `--strict` commit/CI gate** (it converts no-op commits into `GATE FAIL`). CR-02–CR-04 are low-risk doc/robustness refinements; CR-05/CR-07 are accepted-residual context.
- **Review-use boundary.** These findings are decision input only. They are **not** approval, validation, readiness, mandatory remediation, or patch authority until the CA adjudicates them and separately authorizes any patch. A passing checker (including the green selftests and the clean 326-file sweep) is not proof, validation, readiness, acceptance, buyer proof, or resonance judgment. `cross_vendor_discovery` records that a different-vendor reviewer ran the pass; it is a who-property, not a correctness guarantee or a no-new-seam claim about un-run modes.
