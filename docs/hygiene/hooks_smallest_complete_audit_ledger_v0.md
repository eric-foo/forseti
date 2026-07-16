# Hooks Smallest-Complete Audit — Toll-vs-Defect Ledger v0

```yaml
retrieval_header_version: 1
artifact_role: hygiene triage ledger (owner adjudication input)
scope: >
  Ranked toll-vs-defect ledger for the full Forseti enforcement surface: 38
  .agents/hooks files (20,634 raw lines at baseline), 21 CI hook gate steps
  (23 hook invocations) in .github/workflows/ci.yml, and the 27 policy pins
  (23 module hash pins + 4 record-schema token-stamp sites) in
  forseti-harness/tests/contract/test_policy_module_version_pins.py. Each row
  states what the item enforces, the recurring toll every future work unit
  pays, the evidence it still catches a live defect class, and a verdict.
use_when:
  - Owner adjudication of the propose-remove / propose-wire / propose-merge list.
  - Deciding whether a hook, CI gate, or pin still pays for its recurring toll.
authority_boundary: retrieval_only
branch_or_commit: claude/hooks-audit-handoff-context-44c325 (base origin/main a52873ca, measured 2026-07-17)
stale_if: >
  Any hook file, ci.yml hook step, or the pin file changes after 2026-07-17;
  re-measure counts and re-verify evidence citations before relying on rows.
open_next:
  - .agents/hooks/README.md
```

Commissioned by the Goal Handoff lane of
`docs/prompts/handoffs/hooks_smallest_complete_audit_handoff_v0.md` (branch
`claude/handoffs-decomp-and-hooks`). Measured against the updated Smallest
Complete Intervention kernel (AGENTS.md): subtraction weighs equally with
addition; ceremony debt (the recurring toll a required step installs) is
named per item so the owner can weigh it.

**Non-claims.** This ledger is a search result plus resident judgment, not
proof. `no-evidence-of-catch` means git history and durable docs show no
verified real catch — it does not prove the item is useless (deterrence and
silent prevention leave no receipts). Nothing here is validation, readiness,
or acceptance. No gate, pin, or hook was removed by this lane; every
`propose-*` row is owner-gated.

**Verdict vocabulary.** `keep-as-is` / `simplify-internal (EXECUTED)` /
`propose-simplify` (behavior-adjacent, not executed) / `propose-remove` /
`propose-wire` / `propose-merge-with <X>` (all `propose-*` owner-gated).

**Evidence vocabulary.** `CATCH` = a verified real defect the item fired on,
with citation. `no-catch` = no evidence found in history/docs. `FP-amended` =
the item was later loosened because it mis-fired on legitimate work (toll
evidence). All evidence gathered 2026-07-17 by history/doc search agents;
every cited SHA was verified with `git show` before citing.

## Measurement Baseline (2026-07-17, live at origin/main a52873ca)

- `.agents/hooks/*.py`: 38 files, 20,634 raw lines (matches the handoff packet).
- CI: 21 hook gate steps issuing 23 hook invocations (two steps pair `--selftest` + `--strict`: ontology tag validity, harness coupling).
- Pins: 23 entries in `POLICY_MODULE_PINS` + 4 in `RECORD_SCHEMA_TOKEN_FIELD_SITES` = 27.
- Baseline selftests: 37/38 green; `remind_sci.py` was RED (stale AGENTS.md mirror — fixed in this lane).
- Wiring census: 30 of 38 files are wired somewhere (settings.json / ci.yml / .githooks / capsule-child); **check_commission_signal_board_output.py (1,264 lines), check_doc_terms.py (371), check_dcp_receipt_hygiene.py (415), check_registry_list_sync.py (349), check_engagement_stale_phrases.py (463) are not wired into any automated path** (the CSB checker is exercised only by a harness unit test; the last three are honest "CI candidate" manual tools).

## Section 0 — Systemic findings (cross-cutting)

- **S1. Advisory fail-open hides its own breakage.** Two PostToolUse advisories shipped broken and nobody noticed until 2b1d1adb: `check_search_surface_google_route --hook` no-oped on *every* edit (absolute-path bug) and `check_full_gt_claims --hook` re-flagged grandfathered lines. Fail-open is correct for advisories, but it means an advisory's real firing rate is unobservable. Owner option (not executed): a periodic `--check` run in CI as a canary, or accept the class.
- **S2. Doctrine-text mirroring is a standing sync toll.** `remind_sci.py` embeds AGENTS.md's SCI text verbatim; it had silently drifted (baseline selftest RED). Fixed here, and its selftest does guard the sync — but every future AGENTS.md SCI edit now pays a hook re-sync. Named so the owner can weigh mirror-vs-pointer next time the section changes.
- **S3. The scaffold itself had drifted.** `resolve_base_ref` existed in 14 private copies (7 AST-identical), `parse_name_status` in 7 (3 identical), and history shows the drift class is real (d715975c fixed a base-ref bug present in only some copies). The identical copies were hoisted to `_hooklib` in this lane; deliberate variants stay local (see Section 4).
- **S4. Fail-closed asymmetry is intact everywhere it is documented.** No touched or surveyed hook flips advisory→gating or gating→advisory; `check_harness_coupling` is the one deliberate fail-closed-on-infra-gap exception and its README row says so. Four files (`check_ontology_drift`, `check_ontology_tag_validity`, `check_retrieval_header`, `check_registry_list_sync`, `check_engagement_stale_phrases`, `check_full_gt_claims` outside `--hook`) lack the standard `__main__` gating/advisory exception wrapper — a consistency gap, flagged not fixed (changing crash-path exit codes is not behavior-preserving). Worst instance: `check_doc_terms.py` swallows even a `--selftest` crash as exit 0 (a fake-success path).

## Section 1 — Hooks (38 files), ranked: highest toll-vs-thinnest evidence first

Format: **file (lines)** — enforces | recurring toll | evidence | verdict.

### 1a. Owner-decision rows (the actual reductions — see Section 5)

1. **check_commission_signal_board_output.py (1,264)** — CSB classifier-handoff / one-company report shape | zero automated toll (UNWIRED; only a harness unit test exercises it) | no-catch | **propose-remove OR propose-wire** (owner: decide against CSB workstream status). 1,264 lines of unwired checker is pure maintenance surface; it also duplicates ~150 lines of engagement-overclaim engine with `check_csb_scanning_artifact.py` (merge only if kept).
2. **check_doc_terms.py (371)** — ontology-term usage report (always exit 0) | zero automated toll (UNWIRED) | no-catch; swallows selftest crashes as exit 0 (S4) | **propose-remove** (recommendation: cut — report-only, unwired, no usage evidence found; `check_ontology_tag_validity` covers the enforced slice).
3. **check_csb_scanning_artifact.py (1,394)** — full mechanical receipt shape for CSB-first scan artifacts (CI `--strict`) | heaviest per-artifact toll on the surface: caps/accounting/preflight/closeout shape on every changed scan artifact | no-catch; FP-amended (e16b5e39 grandfathering); one delegated review (AR-07, PR #725) records it *missing* a real regression | **keep-as-is, flagged**: highest-toll no-catch gate. If CSB scanning stays a live workstream, keep (receipts are its data integrity); if the workstream winds down, this is the biggest single cut. Overclaim-engine merge is contingent on row 1.
4. **check_review_routing.py (498)** — every commit touching code roots must carry a review disposition (CI `--strict` + commit-msg advisory) | a `review_routing_status:` line or review artifact on *every* code commit (this lane paid it 12×) | no-catch; its own detector had a review-found false-negative gap (EP-35 report) | **keep, honest flag**: pure process ceremony with zero catches so far; it exists to make review-skipping visible, which by nature rarely "fires". Owner may accept the toll or cut. Recommendation: keep (cheap per commit, and the disposition trail is used by adjudication).
5. **check_handoff_pointers.py (534→502)** — handoff paths referenced in changed durable docs must resolve or carry a pin/exemption (CI `--strict` + pre-push mirror) | pin/exemption markers on handoff references; the backlog was closed by *annotating* 16/17 items rather than fixing them (603a9aa3) — the toll absorbed the gate | no-catch | **keep, low-confidence; propose-merge-with check_map_links as a later option** (partial overlap with C4 inline-path checking; different scoping — diff vs whole-tree — so the merge is not free).
6. **remind_sci.py (314→312)** — SCI reminder injected before durable-artifact commits | ~3KB context injection per durable commit (fired 12× in this lane alone) + the S2 sync toll | no-catch (no evidence the nudge ever changed a commit) | **keep, optional-cut**: now self-guarding (selftest catches mirror drift, proven live). If the owner wants context-toll down, this is the cheapest advisory cut; recommendation: keep — the packet's own kernel-update workstream considered commit-time SCI salience load-bearing.
7. **check_dcp_receipt_hygiene.py (415), check_registry_list_sync.py (349), check_engagement_stale_phrases.py (463)** — DCP storage shape / vocabulary containment / stale-phrase leakage; all UNWIRED manual "CI candidates" | zero automated toll | no-catch; first two FP-amended pre-merge (eee9aa7b) | **owner: wire or retire each**. Recommendation: keep `check_dcp_receipt_hygiene` manual (receipt sprawl is a real historical class); retire or wire `check_registry_list_sync` and `check_engagement_stale_phrases` — three unwired 350-460-line checkers that never run is surface without function.
8. **check_ontology_expansion.py (282)** — deferred-ontology-type due-nudge, reached only via the session capsule | one capsule line when due | no-catch; FP-amended (6cf19a76 removed a wrong trigger) | **keep-as-is** (it is the capsule's data source; near-zero cost).

### 1b. Keep-as-is: catch-evidenced

9. **guard_protected_actions.py (674)** — hard EP-01/EP-03 gate, fail-closed merge auth | one subprocess per tool call; `gh pr view` round-trip per merge | **CATCH**: published-branch rebase incident TD-2026-07-14-001 (fd8ba2cc); live false-green race caught by fail-closed design (a5aa51f1) | **keep-as-is, UNTOUCHABLE** (import-free by documented design; verified still import-free).
10. **check_shared_helper_duplication.py (477)** — added private copies of shared helpers must name their delta (CI `--strict` + PostToolUse advisory) | a delta comment per deliberate divergence | **CATCH**: its new pattern row surfaced the same unguarded path-traversal in `tiktok/batch_coverage.py` (3c969ea1) within a day of landing; FP-amended once (06deadf5) | **keep-as-is** — youngest gate on the surface, already paid for itself. Assessed to the same standard as the rest per the packet: real catch, modest toll, honest verdict is keep.
11. **check_map_links.py (1,322)** — map/open_next/inline/router path resolution (CI `--strict`) | every durable-doc link must resolve; drove the 479-pointer migration cleanup | **CATCH** (0f29cd9c, PR #255 gating); FP-amended (`nonresolving:` scheme) | **keep-as-is**; size is legitimate five-check breadth, no chassis found.
12. **header_index.py (833)** — retrieval-header forward-only gate + index/health | header on changed durable docs; one `--health` call per session start | **CATCH** (e43ffef1 blocked a headerless edit) | **keep-as-is**; internal dedup candidates (twin import shims, index/report walkers) noted as propose-simplify, low value.
13. **check_retrieval_header.py (434)** — write-time header advisory | one advisory per headerless durable write | **CATCH** (the PR #613 miss shape, per EP classification doc) | **keep-as-is**; `--strict` exists but is unwired (row is honest about this).
14. **pre_push_guard.py (218)** — local push safety + mirrors ten strict CI gates | ~10 subprocess gate runs per push | **CATCH-class** (e061b5d9: mirrors added after PR #613 cost a red CI round) | **keep-as-is**.
15. **check_review_output_provenance.py (480)** — review-output provenance/boundary shape (CI `--diff --strict`) | shape fields on every changed review output | **CATCH** (bdbe5e6e: CI blocked an adjudication record missing reviewed_by/authored_by/boundary) | **keep-as-is**.
16. **check_ontology_tag_validity.py (528)** — `Word (Capitalized)` parentheticals must be roster-valid (CI selftest+strict) | rewording or allowlisting any type-like parenthetical | **CATCH with dual reading** (92aebc99: fired on "(Capture)" in prose; the doc was reworded to satisfy the checker — as much FP-toll as catch) | **keep-as-is**; propose-simplify: ~41 lines of selftest-only tempdir plumbing + the legacy `ORCA_HOOK_TMPDIR` fallback (not executed: selftest-behavior edits).

### 1c. Keep-as-is: no-catch but cheap, or load-bearing by design

17. **_hooklib.py (275→~350)** — shared helper home | none (library) | n/a | **keep**; gained `resolve_base_ref` + `parse_name_status` this lane.
18. **check_dcp_receipt.py (596→584)** — DCP receipt/blocker shape (CI `--strict`) | well-formed receipt per changed doc carrying one | no-catch | **keep-as-is** (shape gate for a live doctrine contract; silent when no receipts).
19. **check_deletion_evidence.py (473→453)** — governed deletions need a complete evidence record (CI `--strict`) | only on product-tree deletions (rare) | no-catch | **keep-as-is** (guards the irreversibility class the kernel cares most about).
20. **check_source_input_hashes.py (550) / check_hash_pin_freshness.py (561)** — JSON / markdown provenance-hash freshness twins (CI + pre-push) | re-hash on every pin-touching change | no-catch (d715975c fixed the hooks' own base-ref bug, not an external catch) | **keep-as-is** both; deliberately parallel grammars, merge not recommended.
21. **check_prompt_output_mode.py (1,607→1,555)** — EP-11 output-mode token + EP-38/EP-19 commission shells (CI `--strict`) | one token per prompt artifact; exact shell vocabulary on commission prompts | no-catch (all shells born-green on synthetic fixtures) | **keep-as-is** after this lane's internal simplification; **propose-split** (owner option): move the two shells into their own checker + CI step so each README row describes 100% of one gate — same net gates, better contract legibility. NOTE: the handoff packet's "1,560 lines around five strings" characterization was STALE — re-measured, the shells are ~480 lines of real rule logic and the selftest is the behavior spec.
22. **check_review_summary.py (891→862)** — `review_summary` block shape (CI `--strict`) | shape on changed review closeouts | no-catch; enum check advisory-by-design at birth | **keep-as-is**; its 253-line selftest is disproportionate but is the spec — not touched.
23. **check_harness_coupling.py (198)** — runs the two harness contract test files when the diff touches harness code (CI + pre-push; deliberate fail-closed) | two pytest files re-run on harness changes | no-catch | **keep-as-is**; note: `--strict` flag is parsed but never read — it is a wired-in-CI accepted token, so it must stay accepted; do not remove.
24. **check_fragrance_reference.py (367)** — reference-YAML self-invariants (CI `--strict`) | only when the data file is edited | no-catch | **keep-as-is**.
25. **check_ontology_ssot.py (204) / check_ontology_drift.py (425)** — ontology.yaml faithfulness / runtime-binding alignment (CI `--strict`) | only on ontology or bound-model edits | no-catch (drift hardening was proactive) | **keep-as-is** both.
26. **check_silver_lane_registry.py (400)** — silver-lane write contract, full-tree AST scan (CI `--strict`) | a full `forseti-harness/` AST scan per CI run (only non-diff-scoped code gate) | no-catch; FP-loosened same-day as creation (7e846d81) | **keep-as-is**; propose-simplify: diff-scope it like its siblings (not executed: changes scan scope = behavior).
27. **check_full_gt_claims.py (467)** — unballasted full-GT claim language on added lines (PostToolUse + CI) | ballast wording per claim-shaped line | no-catch; FP-amended (2b1d1adb) | **keep-as-is** (claim-inflation erosion guard; cheap).
28. **check_search_surface_google_route.py (524)** — Google route parameterization/leak policy (PostToolUse + CI) | regex scan per write + CI | no-catch; was silently broken until 2b1d1adb (S1) | **keep-as-is**.
29. **check_placement.py (443)** — written path must have a declared home (PostToolUse advisory; `--strict` exists, unwired in CI) | one advisory per undeclared-location write | no-catch | **keep-as-is**; README row's "commit/CI" half describes capability, not wiring — noted, left.
30. **check_repo_map_freshness.py (636→635)** — repo-map structural staleness + map-dirty commit interrupt (PostToolUse + commit-msg; documented CI mode unwired) | narrow; fires on new top-level areas and dirty-map edits | no-catch; FP-loosened (3eb6ec58 per-file→per-directory) | **keep-as-is**.
31. **check_prompt_provenance.py (222)** — prompt-preflight reminder on prompt writes (PostToolUse, once-per-session throttle) | ~380 tokens once per session | no-catch | **keep-as-is** (cheapest advisory on the surface).
32. **check_shared_files_dirty.py (155→150)** — turn-end warning for dirty commit-once-whole files (Stop) | one scoped git-status per turn | no-catch | **keep-as-is**.
33. **check_token_burn.py (399)** — turn-size rung warnings (Stop) | one bounded tail-read per turn | no-catch | **keep-as-is**; its private read_event/state-path near-dups of `_hooklib` are noted as propose-simplify (needs adding an import to a deliberately import-light file; low value).
34. **session_context_capsule.py (334→322)** — session-start lane-state capsule | 8 concurrent subprocesses per session start + fixed context block | no-catch (motivating mistake class predates it; documented in 1c0b5839) | **keep-as-is** after this lane's internal dedup; its `_git` divergence carries the required delta comment.
35. **check_dcp_receipt.py duplicate README row** — was a docs defect, fixed this lane (see Section 4).

## Section 2 — CI Gate Steps (21 steps / 23 invocations)

Every step maps 1:1 onto a Section-1 hook row; per-step verdict = the hook's
verdict. Steps whose hook row is `keep-as-is` with catch evidence:
`check_map_links`, `header_index`, `check_review_output_provenance`,
`check_ontology_tag_validity` (dual reading), `check_shared_helper_duplication`.
Steps flagged for the owner:

- **CSB-first scanning artifact check** (`check_csb_scanning_artifact --diff --strict`) — heaviest toll, no catch (row 3).
- **review-routing disposition** — pure ceremony, no catch (row 4).
- **handoff-pointer resolution** — backlog absorbed by annotation (row 5).
- **silver-lane write contract** — only full-tree (non-diff-scoped) code scan (row 26).
- No step invokes a hook this audit marks `propose-remove`; the unwired checkers are, consistently, also the un-gated ones.
- The two `--selftest`+`--strict` paired steps (ontology tag validity, harness coupling) are cheap and self-verifying — keep.

## Section 3 — Policy Pins (23 hash pins + 4 token-stamp sites)

**What the pin gate enforces.** Every listed derivation-policy module's
LF-normalized source hash is pinned; any byte change fails CI until the pin
is re-stated, forcing an explicit output-shaping / not-output-shaping decision
(and a version-token bump when output-shaping) in the commit. Rule authority:
the pin file's own docstring.

**Recurring toll.** Every touch to any of the 23 modules — including pure
refactors and comment edits — pays a pin recompute plus a stated decision.
Full history: 13 commits ever touched the pin file; **all 13 are mechanical,
deliberate bumps accompanying already-reviewed changes.**

**Evidence.** `no-evidence-of-catch` in 13 paid tolls: no commit or doc shows
a pin mismatch itself surfacing unintended drift. The one real bug adjacent to
a bump (raw_refs TypeError in `cleaning/_shared.py`, 78f54e8e) was found by a
delegated review lane, not the pin. Caveat: this gate is deterrence-shaped —
its catch would only appear the day someone edits a policy module *without*
thinking about re-derivation, and the ritual exists precisely to make that
impossible to do silently.

**The 4 token-stamp sites** (`RECORD_SCHEMA_TOKEN_FIELD_SITES`): near-zero
toll (text containment), guards a pin update that drops the payload field.

**Verdict: keep-as-is (all 27).** Recommendation: keep — the toll is confined
to 23 harness files and the docstring's threat model (comment-bound discipline
failing silently) is credible even with zero catches; the mechanism is the
cheapest form of the guarantee. One maintenance note for the owner: when a
pinned module is retired, `test_pinned_modules_exist` already forces the pin's
deliberate retirement — no extra process needed. No pin removal is
recommended at this time.

## Section 4 — Executed in This Lane (behavior-preserving; all selftests green before each commit)

| Commit | File(s) | Change | Net lines |
|---|---|---|---|
| d9e7ae01 | remind_sci.py | re-sync stale `_SCI_VERBATIM` mirror (baseline selftest RED→green); adopt `_hooklib.git_out` | −2 |
| b9480c9f | check_shared_files_dirty.py | `git_porcelain` → `_hooklib.git_out`; drop subprocess import | −5 |
| b1f36e90 | session_context_capsule.py | collapse two copy-pasted child-health helpers into one parameterized helper | −12 |
| 96057aaf | check_repo_map_freshness.py | delete dead `HEAD_LINES_FOR_HOOK` constant | −1 |
| 58852ac1 | _hooklib.py | add canonical `resolve_base_ref` + `parse_name_status` + 5 selftest cases | +72 |
| 2df6255d | check_dcp_receipt.py | adopt shared `resolve_base_ref` | −12 |
| bb3d1108 | check_deletion_evidence.py | adopt shared `resolve_base_ref`; drop now-unused os import | −18 |
| 8dd56688 | check_handoff_pointers.py | adopt both shared helpers | −30 |
| fb812d51 | check_review_routing.py | adopt shared `resolve_base_ref` | −11 |
| 9ae5eb79 | check_review_summary.py | adopt both shared helpers | −29 |
| 17a8cd00 | check_prompt_output_mode.py | adopt both shared helpers; collapse 11 field regexes into a byte-identical-pattern factory | −52 |
| e29fc580 | .agents/hooks/README.md | contract-table truth alignment (dup row removed; 6 missing CI-gate rows added; 3 false/stale claims fixed) | +6 |
| 1017d78e | .agents/hooks/README.md | document the EP-38/EP-19 shells in check_prompt_output_mode's row | ±0 |

Deliberate variants left local (each already carries or does not need a delta
comment): `resolve_base_ref` in check_full_gt_claims (bare GITHUB_BASE_REF
handling), check_harness_coupling (raising contract), header_index (different
signature), the hash-pin/source-input pair, the csb/tag-validity pair, the
shared-helper-dup/google-route pair; `parse_name_status` variants in
check_review_routing, check_hash_pin_freshness/check_source_input_hashes,
check_ontology_tag_validity.

## Section 5 — Owner Decision List (kept/cut, ranked by surface at stake)

Owner-gated; nothing below was executed. One line each; details in Section 1.

1. **check_commission_signal_board_output.py — WIRE or CUT** (1,264 unwired lines). Recommendation: decide with CSB workstream status; if kept, wire `--strict` on changed board outputs and merge the duplicated overclaim engine with the scanning checker.
2. **check_doc_terms.py — CUT** (371 unwired report-only lines, fake-success selftest wrapper). Recommendation: cut.
3. **check_registry_list_sync.py + check_engagement_stale_phrases.py — WIRE or CUT** (812 unwired lines between them). Recommendation: cut unless someone runs them; their defect classes are narrow and partially covered elsewhere.
4. **check_dcp_receipt_hygiene.py — keep manual or WIRE** (415 lines). Recommendation: keep manual, low priority.
5. **check_csb_scanning_artifact.py — keep or CUT-with-workstream** (1,394 lines, heaviest toll, no catch, one recorded miss). Recommendation: keep while CSB scanning is live.
6. **check_review_routing.py ceremony — keep or CUT** (a disposition line on every code commit, zero catches). Recommendation: keep.
7. **check_handoff_pointers.py — keep or MERGE into check_map_links** later. Recommendation: keep for now.
8. **remind_sci.py context toll — keep or CUT**. Recommendation: keep (now self-guarding).
9. **check_prompt_output_mode.py — optional SPLIT** of the EP-38/EP-19 shells into their own checker + CI step. Recommendation: worthwhile next time the shells change; not urgent.
10. **Policy pins — keep all 27.** No removal recommended.
11. **S1 advisory-canary option** — a CI `--check` canary for PostToolUse advisories, or accept that advisories can break silently. Recommendation: accept for now (adding a canary is new ceremony; weigh against S1's two real incidents).

Not-proven boundary: `no-catch` rows are search results, not proof of
uselessness; several gates are deterrence-shaped. The owner weighs them.
