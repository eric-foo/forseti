# Engagement Resonance Enforcement P4-P6 Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Adversarial implementation/code review of the Priority 4 through Priority 6
  engagement-resonance enforcement checker batch on branch
  codex/search-surface-mgt-p0-captures-ws (commits 4d62a7b2, 801a07fc,
  64a13b7a), per the filed route-out prompt.
use_when:
  - CA adjudication of the P4-P6 checker batch before it is relied upon as enforcement.
  - Deciding whether AR-01..AR-07 warrant a separate patch turn.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: openai-gpt-5-codex
de_correlation_bar: cross_vendor_discovery
review_use_boundary: >
  Findings are decision input only. They are not approval, validation,
  readiness, mandatory remediation, or executor-ready patch authority until the
  CA adjudicates them. No source files were edited in this review lane.
```

## Provenance & De-correlation

- `authored_by`: `openai-gpt-5-codex` (implementation author; home model family OpenAI/GPT).
- `reviewed_by`: `claude-opus-4.8` (Anthropic).
- `de_correlation_bar`: `cross_vendor_discovery` — reviewer vendor (Anthropic/Claude) differs from author vendor (OpenAI/GPT); the discovery bar is met.
- `source_context_status`: **`SOURCE_CONTEXT_READY`**.

## Source Context

| Check | Expected | Observed | Result |
|---|---|---|---|
| Workspace | `...\worktrees\search-surface-mgt-p0-captures` | present | OK |
| Branch | `codex/search-surface-mgt-p0-captures-ws` | match | OK |
| Target head | `64a13b7a...` | object present; current HEAD `37c31858` | OK (see carrier note) |
| Base before batch | `eee9aa7b...` | object present | OK |
| Post-target commit(s) | prompt-only carrier | `37c31858 docs: add P4-P6 enforcement review prompt` — adds only the prompt file | OK; implementation target intact |
| Changed files in range | 15 named target files | exact match, 986 insertions / 9 deletions | OK |
| Working tree | clean + documented allowance | only `?? docs/prompts/hygiene-queue/` (pre-existing) | OK |

Commits in range (reverse): `4d62a7b2 hooks: flag CSB engagement overclaims`; `801a07fc hooks: flag scanning engagement overclaims`; `64a13b7a hooks: check review output provenance`.

The diff is **purely additive for the two modified checkers**: the only deletions are docstring lines (replaced by expanded docstrings); no validation logic was removed. `REQUIRED_ROW_COLUMNS` = 11 in **both** base and head (no new schema columns).

### Method
Reference-loaded `workflow-deep-thinking`, `workflow-code-review`, `workflow-adversarial-artifact-review`, then source-loaded and applied after readiness. The three checkers, three test files, six fixtures, three changed docs were read in full. Authority anchored to the goal-handoff fitness reference (`docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md`), `review-lanes.md`, and the shared retrieval-header predicate. See Not-Assessed for authority files referenced but not fully re-read.

## Fitness Verdict (axis attacked, not pass-if-matches)

The batch is well-aligned with its stated fitness reference and exhibits strong boundary discipline:

- **Class coverage matches/exceeds the goal frame.** CSB-output checker carries all 6 P4 classes (`engagement_as_proof`, `graph_weight`, `commit_scale`, `credibility`, `action_ceiling`, `final_resonance_weight`); scanning checker carries 8 (adds `gate_clearance`, `route_binding`, `amplification`). Verified by code + selftest + pytest.
- **No proof/validation/CI/scoring leakage.** Every `proof`/`validation`/`CI`/`readiness`/`scoring` token in the checkers and docs sits in boundary/non-claim context (`not validation`, `not CI enforcement`, `never receipt truth`, `does not grade signal quality`) or is the forbidden-term list of a detector pattern.
- **No new schema columns, no Capture-route binding, no model routing, no runtime/scoring infrastructure.**
- **Faithful authority citation and reuse.** The provenance checker mechanizes `review-lanes.md` requirements (it does not invent them) and **reuses** the canonical `header_problems_for_lines` predicate from `check_retrieval_header.py` rather than restating header rules — structurally preventing header drift.

The findings below are where the axis bends: a conditional false-negative that defeats the P4 core success signal, and false-positive / scope classes that strain the goal's secondary signal *"false positives stay bounded to mechanical, source-visible failures."*

## Findings (severity-ordered)

Findings-first. Each finding cites file/line and (where testable) a same-function red-green repro run against the shipped code.

---

### AR-01 (major) — CSB-output nonclaim window masks a genuine overclaim adjacent to a negation (false negative)

- **Reviewed target:** `.agents/hooks/check_commission_signal_board_output.py:170-172` (`_is_nonclaim_context`), used at `:180`; negation set `:86-90`.
- **Evidence (red-green, shipped functions):**
  - Input: `"Engagement does not prove demand. High engagement proves demand."`
  - `check_commission_signal_board_output._validate_engagement_overclaims(...)` → `[]` (the real overclaim is **masked**).
  - `check_csb_scanning_artifact._validate_engagement_overclaims(...)` on the same input → flags `engagement_as_proof`.
- **Root cause:** the CSB-output `_is_nonclaim_context` searches a **fixed ±50-char window** (`text[start-50 : end+50]`) for any negation token. When a legitimate disclaimer ("engagement does not prove demand") sits within ~50 chars of a real overclaim, the disclaimer's negation suppresses the overclaim.
- **Why this matters / why the likely defense fails:** the sibling **scanning** checker, authored in the *same batch*, uses a **sentence-bounded** `_is_nonclaim_context` (`check_csb_scanning_artifact.py:660-666`) **and** ships a regression test for exactly this case (`test_csb_scanning_artifact_validator.py:158-165`, `test_engagement_nonclaim_sentence_does_not_mask_later_overclaim`). The CSB-output checker received neither. The goal frame pre-accepts "will not parse arbitrary prose perfectly," but disclaimer-adjacent overclaims are a realistic (not adversarial) authoring pattern, and the sibling proves the bar was set higher. This conditionally defeats the P4 core success signal ("a CSB output that treats engagement as proof ... is flagged").
- **Impact:** false negative in a safety checker — silently passes a genuine overclaim.
- **minimum_closure_condition:** the CSB-output checker flags a real overclaim even when a negation appears earlier in the same vicinity (e.g., by porting the sentence-bounded `_is_nonclaim_context`), with a regression test mirroring the scanning checker's masking-distinction test.
- **next_authorized_action:** CA adjudication → bounded patch turn (out of this read-only lane).
- **red-green status:** available — the scanning masking-distinction test is a ready template; a CSB analogue would fail pre-fix and pass post-fix.

---

### AR-02 (major) — Provenance checker treats `docs/review-outputs/README.md` as a review output, contradicting the retrieval-metadata README exclusion (false positive on a real file)

- **Reviewed target:** `.agents/hooks/check_review_output_provenance.py:119-120` (`is_review_output_scope`).
- **Evidence (real committed file):**
  - `check_review_output_provenance.py --strict docs/review-outputs/README.md` → **exit 1**, 4 findings (`review_output_retrieval_header_invalid`, `missing_reviewed_by`, `missing_authored_by`, `missing_review_use_boundary`).
  - `check_retrieval_header.py --strict docs/review-outputs/README.md` → **exit 0** (it deliberately excludes `README.md`, `check_retrieval_header.py:128`/`:89-94`).
- **Root cause:** `is_review_output_scope` = `startswith("docs/review-outputs/") and endswith(".md")` with no `README.md` / excluded-prefix carve-out. The checker reuses the retrieval-header *predicate* but not its *scope exclusions*, so it requires a retrieval header on a directory index that the retrieval-metadata contract says is out of scope.
- **Why the defense fails:** "it only bites when the README is changed" is true, but `--changed`/`--staged --strict` would fail the moment that README (or any `docs/review-outputs/**/README.md`) is touched, and the requirement contradicts the owning contract's own exclusion. This is over-enforcement against correct repo state, not a judgment call.
- **Impact:** latent false positive on real committed files; a strict gate would fail on a directory index.
- **minimum_closure_condition:** `is_review_output_scope` excludes `README.md` (and mirrors `EXCLUDED_PREFIXES`), or delegates to the header checker's `scope_folder` for the header dimension; the real `docs/review-outputs/README.md` passes `--strict`.
- **next_authorized_action:** CA adjudication → bounded patch turn.
- **red-green status:** available — strict run on `docs/review-outputs/README.md` fails pre-fix, passes post-fix.

---

### AR-03 (minor) — Engagement patterns match across sentence boundaries (cross-sentence false positive, both engagement checkers)

- **Reviewed target:** `check_commission_signal_board_output.py:91-138` and `check_csb_scanning_artifact.py:165-231` — the `.{0,80}` gaps between signal and claim.
- **Evidence:** Input `"Engagement is high. Our research proves demand."` → **both** checkers flag `engagement_as_proof`, although the proof is attributed to research, not engagement.
- **Root cause:** `.` (no `re.DOTALL`) still matches the literal period, so `.{0,80}` spans sentence boundaries on a single line, coupling an engagement mention in one sentence to a proof/demand claim in the next. The scanning checker's sentence-bounded *nonclaim* window does not help, because the issue is the *match* span (there is no negation to suppress).
- **Impact:** over-enforcement; strains the goal's "false positives stay bounded to mechanical, source-visible failures."
- **minimum_closure_condition:** the signal↔claim gap is constrained to within a sentence (e.g., `[^.\n]{0,80}` or a sentence-bounded match) so adjacent unrelated sentences are not coupled.
- **next_authorized_action:** CA decision; couple with AR-01's regex pass if accepted.

---

### AR-04 (minor, pre-existing) — Scanning `FORBIDDEN_TEXT_PATTERNS` lack a nonclaim guard (false positive on canonical boundary disclaimers)

- **Reviewed target:** `check_csb_scanning_artifact.py:232-245` (`FORBIDDEN_TEXT_PATTERNS`), `:696-703` (`_validate_forbidden_text`).
- **Evidence:** `_validate_forbidden_text("This scan does not bind the Capture route.")` → `['scanning_binds_capture']`; `_validate_forbidden_text("Recency is not proof of demand here.")` → `['recency_as_proof']`. Both are legitimate boundary disclaimers (the scanning README itself says "Scanning cites route state; Capture owns route binding").
- **Scope honesty:** `FORBIDDEN_TEXT_PATTERNS` are **pre-existing in base `eee9aa7b`** (not introduced by this batch). The batch added the *guarded* `ENGAGEMENT_OVERCLAIM_PATTERNS` (with `_is_nonclaim_context`) **next to** these unguarded pre-existing patterns, making the inconsistency newly adjacent and visible.
- **Impact:** penalizes correct boundary-writing — the opposite of intent — but it is a pre-existing defect outside the strict diff.
- **minimum_closure_condition:** `_validate_forbidden_text` routes matches through `_is_nonclaim_context` (or an equivalent negation guard), consistent with the engagement patterns; or an explicit decision to leave pre-existing behavior unchanged.
- **next_authorized_action:** CA decision (note: pre-existing, out of strict diff scope; reasonable same-file consistency fix).

---

### AR-05 (minor) — Review-use boundary predicate passes on unrelated occurrences (false pass)

- **Reviewed target:** `check_review_output_provenance.py:46-51` (`DECISION_INPUT_RE`, `NON_APPROVAL_RE`), `:130-131` (`_has_review_use_boundary`).
- **Evidence:** `_has_review_use_boundary("The user's decision input guided the work. Separately, no approval was needed for the refactor.")` → `True`.
- **Root cause:** the predicate is two independent whole-text `search` calls (`decision input` present AND a negation-near-forbidden-term present). They need not be related, in the same sentence, or constitute an actual review-use boundary.
- **Impact:** false pass — a review output lacking a real boundary statement can satisfy the shape check if the two phrases appear unrelatedly. (Bounded: review outputs rarely contain both incidentally; the existing `sp5_...` review output passes legitimately.)
- **minimum_closure_condition:** the boundary is detected only when the decision-input framing and the non-approval clause are proximate (single sentence/clause) or expressed as one combined pattern.
- **next_authorized_action:** CA decision.

---

### AR-06 (minor) — CSB-output overclaim scan (and handoff cross-check) skipped on a zero-row board (false-pass path)

- **Reviewed target:** `check_commission_signal_board_output.py:429` (`if packet_findings or not rows: return findings`); overclaim scan is downstream at `:447`.
- **Evidence:** a Section 4 table with header + separator but **zero data rows** plus a valid Section 8 packet → `parse_signal_rows` returns 0 rows with no findings, and `validate_text(...)` returns `[]` **even with** overclaim prose (`"This board assigns final resonance weight. High engagement proves demand."`). Confirmed by constructing the case from `valid_empty_backtest_output.txt` (which itself has 3 rows and is unaffected).
- **Root cause:** the overclaim scan is gated behind successful row+packet parsing; a zero-row board short-circuits before the scan. The engagement scan is a pure text scan with no dependence on row structure.
- **Impact:** degenerate but real false-pass path (and a zero-row board is silently accepted with no "board has no rows" finding). Low likelihood (zero-row boards are unusual). Note: the scanning checker calls its overclaim scan **unconditionally** (`check_csb_scanning_artifact.py:729`) — another CSB-vs-scanning asymmetry.
- **minimum_closure_condition:** `_validate_engagement_overclaims(text)` runs unconditionally on the document text (independent of row/packet parse outcome), or zero-row boards are explicitly flagged.
- **next_authorized_action:** CA decision.

---

### AR-07 (minor) — Test/fixture suites are positive-case heavy; the false-pass/false-positive classes are uncovered

- **Reviewed target:** the three unit suites + six fixtures.
- **Evidence:** overclaim "positive" tests inject **clean** phrases ("High engagement proves demand") with no adjacent negation, so they never exercise AR-01/AR-03. No fixture/test covers AR-02 (README scope), AR-04 (boundary-disclaimer FP), AR-05 (unrelated-occurrence pass), or AR-06 (zero-row skip). The lone adversarial-edge test is the scanning masking-distinction test (`test_csb_scanning_artifact_validator.py:158`).
- **Impact:** the suites validate intended detection but do not guard the regression surface where the real defects live; selftests pass *because* the fixtures avoid these edges.
- **minimum_closure_condition:** negative/edge fixtures for the masking, cross-sentence, boundary-disclaimer, unrelated-boundary, README-scope, and zero-row classes accompany the corresponding fixes.
- **next_authorized_action:** CA decision; bundle with AR-01/AR-02 as red-green proof.

## Validation Run

All commands run from the target workspace root; Python 3.11.15.

| Command | Exit | Material output |
|---|---|---|
| `check_commission_signal_board_output.py --selftest` | 0 | `SELFTEST OK` (11 fixtures; `bad_engagement_overclaim_output.txt` → engagement_as_proof + engagement_commit_scale_shortcut) |
| `check_csb_scanning_artifact.py --selftest` | 0 | `SELFTEST OK` (3 fixtures; `bad_engagement_overclaim.md` → 4 engagement codes) |
| `check_review_output_provenance.py --selftest` | 0 | `SELFTEST OK` (4 fixtures) |
| `pytest -q` (3 unit files) | 0 | **111 passed** (100%) |
| `py_compile` (3 checkers) | 0 | clean |
| `check_review_output_provenance.py --changed --strict` | 0 | no review-output files in tree changes (scope filter correct) |
| `check_review_output_provenance.py --strict docs/.../sp5_finalization_...md` | 0 | existing review output **passes** (no false-fail on real wording) |
| `check_retrieval_header.py --staged --strict` | 0 | trivially empty (clean tree, batch committed) |
| `check_dcp_receipt_hygiene.py --staged --strict` | 0 | "no DCP receipt candidate files selected -- OK" |
| `check_engagement_stale_phrases.py --staged --strict` | 0 | "no live doctrine files selected -- OK" |
| `git diff --check eee9aa7b..64a13b7a` | 0 | no whitespace errors |
| Leakage search 1 (proof/validation/CI/scoring/...) | n/a | all hits in boundary/non-claim context |
| Leakage search 2 (class tokens + provenance fields) | n/a | 6 CSB classes, 8 scanning classes, provenance fields present/tested |

Smoke-probe gate honored: each changed-checker selftest completed well under 30s; no `VALIDATION_HOOK_TIMEOUT`.

**Caveat:** the `--staged --strict` gates were trivially empty in this run because the batch is already committed and the working tree is clean; they were not re-staged to reproduce the author's non-empty staged runs. The documented `check_retrieval_header.py --changed --strict` dirty-state caveat (untracked `docs/prompts/hygiene-queue/...` lacking a header) remains a pre-existing, out-of-target condition and was not re-run.

## Bounded Artifact / Doctrine Leakage Check (README + playbook)

Applied `workflow-adversarial-artifact-review` discipline (advisory, bounded) to the documentation parts.

- **Phase 1 (correctness):** `.agents/hooks/README.md`, `scanning/README.md`, and the CSB playbook accurately describe the checkers; all preserve boundary non-claims ("not validation", "not readiness", "not CI enforcement", "does not grade signal quality", "Do not treat validator pass as approval or readiness"); labels are "candidate", not promoted. The scanning README added a DCP archive pointer (`docs/decisions/dcp_receipts_archive_v0.md`) — pointer target **exists**. No proof/validation/readiness/acceptance leakage; no CI-promotion implication. One alignment note: the playbook frames the overclaim scan as running "Before the handoff-row cross-check" (after structure passes) but does not disclose the zero-row/packet-fail skip (AR-06); the docs imply coverage that AR-06 shows is conditional.
- **Phase 2 (friction):** none material.

## Recommendation

**`patch_before_acceptance`** — scoped to the two **major** findings (AR-01, AR-02) before the P4 and P6 checkers are relied upon as enforcement surfaces.

Rationale: the batch is a genuine, additive, fully-green improvement with strong boundary discipline and faithful authority reuse. But AR-01 conditionally defeats the P4 core success signal (a real overclaim is silently masked when adjacent to a disclaimer — and the sibling checker proves the higher bar was achievable in the same batch), and AR-02 is a contract-contradicting false positive on a real committed file. Both fixes are cheap and known. AR-03–AR-07 are accept-with-friction follow-ups. Nothing here breaks the committed green state; this is decision input for the CA, not a gate the reviewer imposes.

## Residual Risks & Not-Assessed

- **de_correlation_bar not mechanically enforced.** `review-lanes.md:122-137` states the same-vendor `de_correlation_bar` / `same_vendor_rationale` should be "mechanically detectable," but the P6 checker does not check them. This is **outside** the goal-handoff P6 SCI scope (so not a defect), but it is a named-in-authority mechanical gap and a natural upgrade trigger.
- **Git-unavailable indistinguishable from no-files.** `git_lines` returns `[]` on a missing/failed git, yielding exit 0 ("no files selected"); a strict gate could silently no-op where git is absent.
- **Rigid `\bdecision\s+input\b` bigram.** The existing `sp5_...` review output passes, but boundary wording omitting that exact phrase (e.g., "findings inform the decision") would false-fail. Latent, not currently observed.
- **Common-word engagement tokens** (`views?`, `shares?`, `likes?`, `comments?`) could false-positive in unrelated prose; bounded by the required proof/demand co-occurrence; not observed in fixtures.
- **Authority not fully re-read:** `source-loading.md`, `prompt-orchestration.md`, `validation-gates.md`, `source-of-truth.md`, `delegated-review-patch.md`, `engagement_logic_registry_v0.md`, and the CSB prompt-structure-rules were referenced but not fully re-read; class-coverage and boundary judgments are anchored to the goal-handoff fitness reference, `review-lanes.md`, and the shared retrieval-header predicate (drift structurally prevented by predicate reuse). `AGENTS.md` was available via the session kernel.
- **Not in scope (per prompt):** no P7+ surfaces, no doctrine rewrite, no CI wiring, no runtime/scoring work, **no patch execution** — recommendations only.

## Review-Use Boundary

These findings are **decision input only**. They are not approval, validation, readiness, mandatory remediation, or executor-ready patch authority until the CA adjudicates them. Patch execution belongs to a separate, explicitly authorized turn. No source files were edited in this review lane; only this report was written under `docs/review-outputs/`.
