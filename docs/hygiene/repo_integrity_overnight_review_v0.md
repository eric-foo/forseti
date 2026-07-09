# Repo Integrity — Overnight Tiered Hygiene Review (v0)

```yaml
retrieval_header_version: 1
artifact_role: Workflow integrity-review report
scope: Overnight tiered repo hygiene run — actions taken (changelog) + risky findings surfaced; advisory only.
use_when:
  - Reviewing what the overnight hygiene run changed and which risky items need owner judgment.
authority_boundary: retrieval_only
```

Run date: **2026-06-09** · Branch: **`ecr-sp3-timing-deriver-slice1`** · HEAD: **`c912203`** (ahead 19 of origin) · Worktree state: **heavy multi-lane dirty** (12 modified tracked + ~289 untracked).

This is an **advisory** report. It makes **no** validation, readiness, acceptance, PASS, or "repo is clean" claim. "Tier C" items are surfaced for owner judgment, not verdicts.

---

## 1. Owner Summary (read this first)

### (a) What was auto-fixed / archived / deleted

**Nothing.** Zero Tier A fixes, zero Tier B archives/deletes. **No commits were made. One file was written: this report.**

This is the correct outcome for tonight's repo state, not a skipped job. Two structural facts forced it:
- **The worktree is mid-flight across many lanes** (~289 untracked + 12 modified files from ECR/capture, judgment-spine, daimler-advisory, product-lead, and an overlay/hooks-infrastructure lane). Under the run's rails, **every modified or untracked path is another lane's work and off-limits** — so the safe-action surface shrinks to the *committed-clean* baseline only.
- **The committed-clean baseline is in good shape.** The natural home for a structural fix — the repo map — is itself **modified by another lane** (off-limits). Every concrete fix-candidate the fan-out raised was verified by me and **collapsed** (false positive, off-limits, code-logic, doctrine, or uncertain-origin). Nothing cleared the HIGH-confidence + committed-clean + own-work + deterministic bar that Tier A/B requires.

So per the contract ("when unsure, surface, don't act"), the value delivered is the whole-repo context plus the Tier C list below — not manufactured edits to a shared, in-flight tree.

### (b) Top risky / judgment items to look at (Tier C — owner decision)

1. **3 files sit at the repo ROOT** (not an accepted folder): [`di_dd.html`](di_dd.html) (242 KB saved web page — *dataintelo.com* "Due Diligence Services Market Research Report 2034"; untracked, **not** gitignored), [`slot1_mi_CAPTURE_operator_workfile.md`](slot1_mi_CAPTURE_operator_workfile.md), [`slot2_teal_CAPTURE_operator_workfile.md`](slot2_teal_CAPTURE_operator_workfile.md) (capture-lane operator workfiles). Decide: relocate (→ `docs/research/` or `docs/_inbox/`), gitignore, or delete. <!-- # nonresolving: untracked root operator workfiles, never committed -->
2. **`milwaukee_initial_judgement.md` uses a non-standard retrieval-header value** `authority_boundary: non_authoritative` (the controlled contract value is exactly `retrieval_only`). Untracked (consultant-loop lane). 3 other untracked files use non-standard boundary values; ~30 untracked durable docs are missing headers entirely (full list in §3, Area 2).
3. **Possible code-logic gap** in [`forseti-harness/capture_spine/reddit_candidate_intake/validation.py:193`](forseti-harness/capture_spine/reddit_candidate_intake/validation.py) — `validate_promotion_receipt()` may fall through and return `None` (no error raised) when its final guard is false. Committed-clean code → judgment call for the harness lane (looks intentional per its test, but worth confirming).
4. **2 untracked binary `.zip` review bundles** in `docs/review-outputs/` are not gitignored (commit-by-accident risk). Decide track-vs-ignore.
5. **`di_dd.html` + the `.zip` bundles are unignored scratch-shaped files** — a `.gitignore` decision is waiting, but I did not make it (uncertain origin / not HIGH-confidence-disposable / possibly another lane's).

Nothing in this list is urgent or destructive; all are owner-judgment hygiene.

---

## 2. Action Changelog (Tier A / Tier B)

| # | File | Action | Reason | Commit SHA | Revert |
|---|------|--------|--------|------------|--------|
| — | — | **(none)** | No finding cleared the HIGH-confidence + committed-clean + own-work + deterministic bar for Tier A/B. | — | — |

**Why empty (evidence):**
- The repo map (`docs/workflows/orca_repo_map_v0.md`), the usual home for structural fixes, is **modified by another lane** → editing it would violate "no other-lane edits."
- The one committed-clean "broken cross-reference" candidate — `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` lines 439/442 citing two `ecr_consolidation_v0_*cross_family_review_v0.md` files — was **verified valid**: both targets exist. (This was the 3rd false-positive existence claim from the fan-out; the other two were `.agents/workflow-overlay/source-loading.md` and `docs/workflows/orca_repo_map_v0.md`, both of which also exist.)
- All 37 retrieval-header warnings land on **untracked/modified (off-limits)** files; none on committed-clean files. The contract also says *do not backfill headers into old untouched files by default*, so committed-clean header gaps are not a fixable defect here.
- The only disposal-shaped items (`di_dd.html`, `.zip` bundles, root workfiles) are **uncertain-origin or other-lane**, so they fail the Tier B "HIGHLY confident + not another lane's + reversible" gate.

---

## 3. Surfaced Findings (Tier C) — by the 7 areas

Severity scale: critical / major / minor. Git-state in brackets. All items are advisory; "off-limits" = another lane's modified/untracked work the run may not touch.

### Area 1 — Structural health
- **C1-a · minor · [untracked]** — Three durable-ish files at the **repo root** (not an accepted artifact folder): `di_dd.html` (242 KB external web capture, *dataintelo* due-diligence market report), `slot1_mi_CAPTURE_operator_workfile.md`, `slot2_teal_CAPTURE_operator_workfile.md`. *Recommended:* owner relocates the capture workfiles under `docs/` (capture lane) and triages `di_dd.html` (gitignore / move to `docs/research/` or `docs/_inbox/` / delete).
- **C1-b · minor · [modified — off-limits]** — `docs/workflows/orca_repo_map_v0.md:~54` carries a bare-basename reference "`decision-routing.md`"; the file exists at `.agents/workflow-overlay/decision-routing.md`. Almost certainly prose, not a broken link, but worth a glance when that lane settles the map. *Recommended:* the repo-map lane confirms it reads as a cross-reference, not a path.
- **Baseline (no action):** the committed-clean navigation backbone is healthy — repo map + both consolidation submaps + `docs/STRUCTURE.md`: 40+ outbound targets all verified to exist. No misfiled committed docs, no oversized committed artifacts found.

### Area 2 — Retrieval-header compliance
*(Authoritative source: `check_retrieval_header.py --changed`, run read-only. 37 advisory warnings — ALL on untracked/modified, off-limits files. The PostToolUse hook will re-fire for each owning lane at its own write/commit boundary, so these route themselves; listed here for visibility only.)*
- **C2-a · minor · [untracked]** — Non-standard `authority_boundary` values (contract requires exactly `retrieval_only`; put richer semantics in the body, not the header):
  - `docs/decisions/consultant_loop/milwaukee_initial_judgement.md` → `non_authoritative`
  - `docs/review-outputs/direct_http_no_proxy_delegated_adversarial_code_review_patch_v0.md` → `findings_and_verdict_for_CA_adjudication_only`
  - `docs/prompts/deep-thinking/reddit_crawler_graph_exploration_architecture_ca_prompt_v0.md` → `prompt_only`
  - `docs/review-outputs/adversarial-artifact-reviews/source_quality_slot3_post_recapture_scratch_pass_adversarial_artifact_review_v0.md` → header present but `authority_boundary` missing.
- **C2-b · minor · [untracked]** — ~30 in-scope durable docs missing a retrieval header, notably the `docs/product/core_spine_v0_method_validation_*` set (rubric, replay packet, case/frame locks, mv01/mv03/mv04/mv09 replays), several `docs/review-outputs/no_tools_*` reports, several `docs/prompts/reviews/*` and `docs/prompts/handoffs/*`, and `docs/hygiene/checkpoint_icp_convergence_lock.md`. These belong to their authoring lanes. *Recommended:* each lane adds the 5-field header when it next materially touches the file (per the contract's forward-only rule).
- **C2-c · minor · [committed-clean]** — Some pre-adoption committed docs (≈29 in `docs/product/`, 2 in `docs/workflows/` — `orca_bootstrap_record.md`, `turn_08_workflow_bedrock_maximization.md`) lack headers. The contract says **do not backfill old untouched files by default** → **not a defect, no action**; add at next material touch only.

### Area 3 — Staleness
- **C3-a · minor · [gitignored / untracked]** — Lingering single-consumption checkpoints. Per overlay (`source-of-truth.md` → Checkpoint Artifacts), precompact/lane-state checkpoints are burn-after-consumption. `docs/hygiene/precompact_*` (12 files; **gitignored**, so no commit risk) include apparently-superseded v0–v2 generations (jsg01, judgment_spine) alongside current ones; `docs/hygiene/checkpoint_icp_convergence_lock.md` (**untracked, not ignored**) reads as a spent lock. *Recommended:* owning lanes burn spent checkpoints; harmless to leave (gitignored ones won't be committed).
- **Baseline (no action):** version chains checked and found **intentional, not duplicates** — `packing_to_harness_foundation_interface_architecture_v0..v3` (v3 current, history retained on purpose), `core_spine_v0_method_validation_case_locks / case_frame_locks / case_frame_lock_contract` (sequential), the daimler / no-case-smoke decision chains, and the `*_adversarial_review` → `*_post_patch_recheck` pairs. No superseded-but-unmarked artifacts found.

### Area 4 — Doctrine / source-of-truth integrity *(always Tier C)*
- **C4-a · informational · [modified + untracked — off-limits]** — An **overlay/enforcement-infrastructure lane is mid-flight**: modified `.agents/workflow-overlay/{source-of-truth,validation-gates,decision-routing}.md` + `.claude/settings.json`, plus untracked `.agents/hooks/` (`check_retrieval_header.py` EP-06, `check_repo_map_freshness.py`, `guard_protected_actions.py`). The committed doctrine already carries matching `direction_change_propagation` receipts in `source-of-truth.md`. This is live doctrine work by another lane — **off-limits, no action**. No missing-propagation-receipt defect was found in committed-clean doctrine. *Recommended:* let that lane land its own commit; do not co-edit.

### Area 5 — Git hygiene
- **C5-a · minor · [untracked]** — Unignored scratch-shaped files: `di_dd.html` (root) and 2 review bundles `docs/review-outputs/ecr_sp6_no_repo_review_bundle.zip`, `docs/review-outputs/signal_content_v0_no_repo_review_bundle.zip` are untracked and **not** gitignored (accidental-commit risk). *Recommended:* if disposable, add to `.gitignore`; if durable review evidence, track deliberately. (Not acted on: uncertain origin, not HIGH-confidence-disposable.)
- **C5-b · minor · [local branch]** — `dcp-restatement-integrity-port` is a local branch holding **unmerged** work (commit `0a44245`; verified **not** merged into HEAD via `git branch --merged`). **Keep** — it is *not* a stale/merged-cleanup candidate. (Branch deletion is unauthorized anyway.)
- **Branch/worktree/ref state (no action):** current branch ahead 19 of origin; `main` behind 1 (informational); 2 `.codex/worktrees/` other-lane worktrees (`data-capture-sourcing-architecture`, `orca-doctrine-health`) — **off-limits**; **no stashes**; **no stale remote-tracking refs**.
- **Dirty-state classification:** 12 modified + ~289 untracked, classified overwhelmingly **keep-worthy / mid-work-hold** (other lanes). **Zero** files were HIGH-confidence-disposable-and-owned-by-this-run → **no Tier B disposal**.

### Area 6 — Safety / governance smells *(always Tier C — code/logic)*
- **C6-a · minor · [committed-clean code]** — `forseti-harness/capture_spine/reddit_candidate_intake/validation.py:193-201` (`validate_promotion_receipt`): an early `return` covers one branch, but the function may fall through and return `None` without raising when the final condition is false (silent non-failure). The harness inventory notes a test appears to exercise this as intended. *Recommended:* harness lane confirms the intended postcondition / adds an explicit terminal guard if a failure path was meant. (Code logic — surfaced only, never edited.)
- **Baseline (no action):** **no** self-certified gates (`authorized = True` / `*_authorized_for_this_run = True` / self-asserted `valid`), **no** credential/secret literals, and **no** bare `except: pass` / success-on-error handlers were found in the harness. Research/decision authorization fields consistently cite **external owner instructions** (not self-assertion) and carry explicit non-claims — consistent with the non-self-certification gate.

### Area 7 — Test / validation health *(cheap/static only — suites NOT run)*
- **C7-a · minor · [committed-clean]** — `orca-harness/tests/unit/test_local_secret_store.py:63` — `pytest.skip("symlink creation not permitted on this host")`: a legitimate platform-specific skip; noted only.
- **Baseline (no action):** static inspection found no `xfail`/dead/no-op tests, fixtures resolve, and harness docs↔code references (`adapter_author_contract.md` → modules/exports) verify. **Suites were not executed** (rails: static-only).

---

## 4. Subagent coverage + Not inspected

**Phase-1 read-only fan-out covered (8 inventory subagents + lead reads):**
- `docs/decisions/` (incl. `consultant_loop/`) · `docs/product/` (incl. `source_capture_toolbox/`) · `docs/workflows/` + `docs/migration/` + `docs/STRUCTURE.md` + repo map + both consolidation submaps · `docs/prompts/` (all typed children) · `docs/review-inputs/` + `docs/review-outputs/` (incl. adversarial-artifact-reviews/, method-validation/, proof/) · `docs/research/` (judgment-spine harness/cases, daimler-advisory, consulting-judgment-corpus, packing-phase) · `orca-harness/` code+tests+docs · `docs/hygiene/` + whole-repo git/worktree/branch/ref state.
- **Lead read directly:** `AGENTS.md`/`CLAUDE.md`, all `.agents/workflow-overlay/*` authority files, all 3 `.agents/hooks/*` scripts, `.gitignore`; and independently re-verified every concrete fix-candidate (existence checks, git-state, branch-merge, file classification).

**Not inspected / out of scope (by design):**
- The 2 `.codex/worktrees/` other-lane worktrees — off-limits, not entered.
- `.claude/` settings/skill copies beyond noting modified state — installed/skill copies, not edited.
- Binary/large blobs not opened beyond classification: the 3 PDFs under `docs/research/daimler_advisory_001/`, the 2 `.zip` review bundles, the Canoo/Walmart HTML source-captures, and the body of `di_dd.html` (header only).
- Full contents of the ~289 untracked mid-work files — sampled, not exhaustively read (off-limits; the fan-out inventoried roles/cross-refs rather than auditing each).
- **Test suites not run** (static inspection only).
- **Methodology caveat:** subagent *existence* checks proved unreliable (≥3 false-positive "missing file" claims); every cross-reference finding above was re-verified by the lead before classification.

---

## 5. Attestation

- **Write/delete/commit actions that occurred:** exactly **one file write** — this report at `docs/hygiene/repo_integrity_overnight_review_v0.md`. **No** edits, **no** deletions, **no** archives, **no** moves, **no** commits, **no** staging.
- All output was **own-file-only** and fully reversible (a single new, untracked report file; delete it to revert).
- **No** other-lane file (modified or untracked) was touched. **No** network access, **no** sandbox escalation, **no** skill install/deploy/shadow, **no** edits to `.agents/skills/` or `.claude/`. **No** branch/worktree/stash operation. **No** `git add -A`/`-u`/`.`, **no** push, **no** destructive clean.
- The retrieval-header and repo-map-freshness hooks were run/triggered in **read-only/report mode** only.
- This report asserts **no** verdict, readiness, validation, acceptance, or "clean/PASS" status. Findings are advisory; Tier C items await owner judgment.

**Post-run coordination addendum (2026-06-09).** The review run recorded above made no commits. Under a later branch-`ecr-sp3-timing-deriver-slice1` coordination request for each lane to commit its own work, this report (own file, single explicit path) was staged for a `docs(hygiene)` commit. Because multiple lanes were committing concurrently against one shared working tree and `.git/index`, the staged file was first swept into an unrelated concurrent commit by another lane — `0ed0ed1` *docs(decisions): record declined adversarial-review tier-routing policy* (bundled alongside `docs/decisions/adversarial_review_routing_policy_v0.md`) — rather than this lane's own commit. This lane then committed this corrected record separately, path-limited, to restore accurate provenance. No other lane's file was deliberately staged by this lane; the three shared doctrine/config files, the hooks cluster, and the loose root scratch were left untouched; and no merge, push, rebase, stash, or clean was performed.
```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: different_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: "Fresh unattended tiered-hygiene anchor; not the capture lane's anchor — capture target intentionally not carried."
```
