# CSB Prompt Structure Rename Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Read-only adversarial artifact review of commit
  c992fe7efb4bd8cadf53797b380fde25e83834e5 ("docs: rename csb prompt structure
  artifacts") on branch codex/search-surface-mgt-p0-captures-ws.
use_when:
  - Chief Architect adjudication of this review's findings before the rename lands on main.
  - Checking whether the CSB Prompt Structure / Prompt Structure Rules rename
    over- or under-propagated.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
de_correlation_bar: unrecorded
same_vendor_rationale: not_applicable
open_next:
  - orca/product/spines/commission_signal_board/migrations/commission_signal_board_current_main_reconciliation_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md
  - docs/review-outputs/csb_scanning_broad_scout_recency_default_enforcement_adversarial_code_review_v0.md
  - orca/product/spines/commission_signal_board/spine.yaml
  - orca/product/spines/commission_signal_board/migrations/moved_paths_index.md
stale_if:
  - Commit c992fe7efb4bd8cadf53797b380fde25e83834e5 is amended, reverted, or superseded.
  - The CSB Prompt Structure files move again.
  - The branch merges to main (forward obligations in Residual Risks then become live).
```

---

## Review Provenance

- **reviewed_by**: `unrecorded` — the operator/tooling did not supply the reviewing-model provenance field on this commission. The reviewing runtime self-identifies as Claude Opus 4.8 (Anthropic family); per `.agents/workflow-overlay/review-lanes.md` this field is operator/CA-set and is recorded `unrecorded` (never fabricated) when not supplied.
- **authored_by**: `unrecorded` — the authoring model of commit `c992fe7e` was not supplied or accepted by operator/tooling this turn. The git author is `Eric` and the branch namespace is `codex/*`, but the authoring *model* lineage is not a confirmable source fact, so it is recorded `unrecorded`, not inferred.
- **de_correlation_bar**: `unrecorded` — because `authored_by` is unrecorded, author-vs-reviewer vendor relation cannot be established. No `cross_vendor_discovery` / no-new-seam claim is made. (If the operator records the author as a non-Anthropic family, an Anthropic-family review would meet `cross_vendor_discovery`; that recording does not exist here.)

This is a read-only adversarial artifact review. Findings are decision input only — not approval, validation, readiness, mandatory remediation, or executor-ready patch authority.

---

## Commission

- **Commission source**: `docs/prompts/reviews/csb_prompt_structure_rename_adversarial_artifact_review_prompt_v0.md`.
- **Route note honored**: the prompt's Delegated Review-And-Patch route note correctly declined `workflow-delegated-review-patch`'s repo-mode shape (the target is a multi-file rename propagation, not a single high-stakes authored artifact) and routed to read-only adversarial artifact review. No patching is performed in this lane. This is consistent with `.agents/workflow-overlay/delegated-review-patch.md` ("If the inferred target is not a single high-stakes authored artifact … do not stretch this convention").
- **Review target**: the patch delta `c992fe7efb4bd8cadf53797b380fde25e83834e5^ → c992fe7efb4bd8cadf53797b380fde25e83834e5`.
- **Purpose**: adversarially check whether the rename fully eliminates confusing live canonical names without breaking CSB source loading, moved-path resolution, existing prompt/review references, or downstream lane pointers.

### Fitness reference (from commission)

- **Goal**: make CSB future-agent source loading unambiguous by giving the two CSB prompt-structure artifacts role-aligned live filenames.
- **Success signal**: live CSB and adjacent-lane references point to the new filenames; old filenames survive **only** as explicitly historical absent-path resolver entries or frozen snapshots; validators and stale-reference sweeps show no live old-path dependencies.

The success signal is itself the decisive review axis. It is two-sided: it requires both that *live* references move to the new names **and** that old names *survive in frozen snapshots*. The two confirmed findings below are violations of the second clause — over-propagation into pinned/frozen records — which the goal-as-stated does not want.

---

## Source Context: SOURCE_CONTEXT_READY

Required authority sources (all read from the target worktree at HEAD `506d92b8`):

| Source | Why read | State |
| --- | --- | --- |
| `AGENTS.md` (kernel, via session context) + `.agents/workflow-overlay/README.md` | Kernel + overlay entry | clean |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy, DCP contract | clean |
| `.agents/workflow-overlay/source-loading.md` | Read packs, moved-path framing | clean |
| `.agents/workflow-overlay/artifact-roles.md` | Review-output / migration-note / moved-path-index role freshness markers | clean |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial artifact review lane, provenance fields, two-bar de-correlation | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | Output contract, provenance, findings-first | clean |
| `.agents/workflow-overlay/validation-gates.md` | Claim limits, DCP gate | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Route note + de-correlation grounding | clean |
| `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | Review template / output contract | clean |
| Target commit + all 19 changed files (full `git show`) | The review object | committed (HEAD-1) |
| `…/migrations/moved_paths_index.md`, `…/migrations/commission_signal_board_current_main_reconciliation_v0.md` | Resolver + main-state records | committed |
| `docs/review-outputs/csb_scanning_broad_scout_…_review_v0.md` (header + ledger) | Frozen review-output pin target | committed |

Worktree state: branch `codex/search-surface-mgt-p0-captures-ws`, working tree clean, HEAD `506d92b8` (= `c992fe7e` [review target] + `152e6ba0` parent; HEAD adds the review-prompt artifact only). All sources clean/anchored. **Status: `SOURCE_CONTEXT_READY`.**

Method: `workflow-deep-thinking` invoked and applied to frame the dual (under/over-propagation) boundary before findings; `workflow-adversarial-artifact-review` invoked and applied after source readiness. Both available — no advisory-only fallback required.

---

## Commands Run (exact results)

```text
git show --name-status --find-renames c992fe7e
  -> R099 authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md
          -> authority/orca_commission_signal_board_prompt_structure_rules_v0.md
  -> R099 prompts/orca_commission_signal_board_prompt_v0.md
          -> prompts/orca_commission_signal_board_prompt_structure_v0.md
  -> 17 other files Modified (reference updates). 19 files, +50 -52.

git diff --check c992fe7e^ c992fe7e            -> exit 0 (no whitespace/conflict errors)

python -B .agents/hooks/check_commission_signal_board_output.py --selftest
  -> SELFTEST OK (10/10 fixtures pass, exit 0)

Sweep 1 (LIVE old canonical-spine-path, .agents docs orca, md/yaml/py):
  rg "commission_signal_board/(prompts/orca_commission_signal_board_prompt_v0
      |authority/orca_commission_signal_board_prompt_adjudication_packet_v0)"
  -> ONLY 2 hits, both inside the review-prompt file itself
     (csb_prompt_structure_rename_..._prompt_v0.md lines 62, 65 = the
     "intended rename" mapping; not part of commit c992fe7e). No live-source hit.

Sweep 2 (broad old filename / old vocab):
  -> spine.yaml legacy_absent_paths VALUES (docs/... old absent paths) — preserved (correct)
  -> moved_paths_index.md old-absent-path rows — left column preserved (correct)
  -> reconciliation "Historical Paths Not Live" (docs/... ) — historical (correct)
  -> review-prompt self + its rg command strings (expected)

Broad all-filetype sweep (incl. orca-harness, .txt, .json):
  -> old spine paths remain ONLY in review-prompt self and in FROZEN review-INPUT
     snapshots: docs/review-inputs/capture_spine_core_migration_.../{base_files,
     head_files}/...scanning_w3a_proposal_v0.md.snapshot.txt + diff_u80.patch
     (correctly left untouched — frozen snapshots).

git ls-tree -r 13a1becb | rg CSB prompts/authority   -> OLD names
git ls-tree -r 28d896c  | rg CSB prompts/authority   -> OLD names
git ls-tree -r 780091959 (PR#310 main) | rg ...      -> OLD names
git ls-tree -r bc950cdf  (PR#307 main) | rg ...      -> OLD names
git ls-tree -r origin/main (8e3e8c55)  | rg ...      -> OLD names
git merge-base --is-ancestor c992fe7e origin/main    -> NO (rename unmerged; branch ahead)

rg CSB prompt/authority in docs/workflows/orca_repo_map_v0.md  -> no references (no stale nav surface)
rg key consumers of spine.yaml canonical_artifacts.*/legacy_absent_paths.* in .agents, orca-harness -> none
```

---

## Review Scope / Excluded Scope

- **In scope**: the non-code artifact text of the 19-file rename propagation — reference updates, resolver/migration records, manifest keys, role labels, retrieval headers, and the validation non-claims of the patch.
- **Excluded**: implementation correctness of `.agents/hooks/check_commission_signal_board_output.py` or the harness tests (code-review lane; only its selftest pass is noted as evidence). Merge mechanics and any post-merge state (this commit is pre-merge; forward obligations are recorded as residual risks, not current defects).

---

# Findings (findings-first, ordered by severity)

**Critical:** none.

---

## Phase 1 — Correctness

### AR-01 (major · correctness) — Frozen, commit-pinned review outputs rewritten to filenames that did not exist at their pinned commits (fabricated history)

- **Phase**: correctness
- **Reviewed target / role**: two `Review report` (review-output) artifacts, modified by the commit.
- **Location**:
  - `docs/review-outputs/adversarial-artifact-reviews/scanning_csb_capture_judgment_recency_attention_adversarial_artifact_review_v0.md` — the "Target files at commit `13a1becb` (via git show):" list.
  - `docs/review-outputs/csb_scanning_broad_scout_recency_default_enforcement_adversarial_code_review_v0.md` — the Source-Read Ledger rows marked "read this session at HEAD (matches impl commit)" and the "Target files reviewed:" list (pinned via `implementation_under_review: 28d896c79…`).
- **Source authority**: `.agents/workflow-overlay/artifact-roles.md` (Review report freshness marker = "Reviewed artifact path **and revision**"); fitness success signal ("old filenames survive only as … frozen snapshots").
- **Artifact evidence**: the commit rewrites both pinned lists from the old names to `…prompt_structure_v0.md` / `…prompt_structure_rules_v0.md`. `git ls-tree -r 13a1becb` and `git ls-tree -r 28d896c` both return the **old** names. So each review output now asserts, against an explicit "(via git show)" / "at HEAD (matches impl commit)" pin, filenames that demonstrably did not exist at that pinned revision.
- **Strongest defense, and why it fails**: *"Review outputs are living indexes; updating path references keeps them navigable."* It fails three ways: (1) these are not bare pointers — they are explicit at-a-named-commit factual claims ("Target files at commit 13a1becb (via git show)"); (2) the freshness marker pins a review output to the reviewed **revision**, and the revision was left unchanged while the names were swapped, so the record is now internally false; (3) the **same commit** correctly left the frozen review-**input** snapshots (`docs/review-inputs/…/*.snapshot.txt`, `diff_u80.patch`) with the old names — so the patch's own standard is "frozen snapshots keep old names," which these review-output edits violate. The defense is refuted by the patch's own behavior.
- **Secondary defect (same locations)**: in `csb_scanning_broad_scout_…_review_v0.md`, findings AR-02/AR-03 had their **Location** line repointed to `…prompt_structure_rules_v0.md` while the surrounding prose still reads "The adjudication packet's proposed field taxonomy lists…" / "The patch to the adjudication packet…". The half-rewrite leaves the filename and the role prose disagreeing within one finding.
- **Impact**: audit integrity. A CA (or `reviewed_by`/`authored_by` measurement consumer) re-verifying either frozen review against its pinned commit via `git show` finds a name mismatch the record does not disclose; the "(via git show)" provenance is now false.
- **minimum_closure_condition**: each pinned-historical reference in a frozen review output either (a) reflects the filename that actually existed at the pinned commit/revision it cites, or (b) carries an explicit, dated "renamed to `<new>` in `c992fe7e`" annotation that preserves the historical name as the as-reviewed fact; and the AR-02/AR-03 location/prose pair is made internally consistent.
- **next_authorized_action**: CA decision on revert-to-historical-names vs. annotate; no patch authority is created by this review.
- **patch_queue_entry**: not authorized (ordinary adversarial artifact review).
- **red-green proof**: `not_applicable` (non-executable record-accuracy finding; verifiable by `git ls-tree <pinned-commit>` vs. the record).
- **not proven**: that the rewrite was intended as a policy rather than an over-propagation — the inconsistency with the preserved review-input snapshots is evidence against intent, but intent is not a source fact.

---

### AR-02 (major · correctness) — Reconciliation migration note now asserts a false current-main state

- **Phase**: correctness
- **Reviewed target / role**: `Orca migration note` — `orca/product/spines/commission_signal_board/migrations/commission_signal_board_current_main_reconciliation_v0.md`.
- **Location**: the "Current-Main State" block, "The current tree contains these CSB spine files:" list (the authority + prompt lines), against the unchanged header pins `branch_or_commit: origin/main @ bc950cdfeeb3a02f33bf52217d71e049aa9093f2` and "Current landed baseline after PR #310: origin/main at `780091959…`".
- **Source authority**: the doc's own pins; `git ls-tree` of those exact commits; `git merge-base`.
- **Artifact evidence**: the commit rewrites the file list to the **new** names while leaving the `origin/main @ …` pins and the "Observed authoring baseline … Current landed baseline after PR #310" prose unchanged. Verification: `git ls-tree -r 780091959` and `git ls-tree -r bc950cdf` (the doc's own pinned baselines) both contain the **old** names; current `origin/main` (`8e3e8c55`) contains the **old** names; `git merge-base --is-ancestor c992fe7e origin/main` → **NO** (the rename is unmerged). The doc therefore now states that main's current tree contains files that are not on main at any of its cited baselines.
- **Strongest defense, and why it fails**: *"The rename triggers the doc's `stale_if` ('the CSB spine is renamed … or moved'), so updating the names IS the refresh."* It fails because a faithful refresh would re-pin `branch_or_commit` to a revision that actually contains the new names (post-merge main, or this branch) — not swap the file list while leaving the pins on pre-rename main. As written, the pin and the body now contradict each other. The defense, taken seriously, makes the edit a *defective* refresh rather than an acceptable one. (Note also the **internal inconsistency with AR-nothing**: the patch's own `moved_paths_index.md` still treats the old spine paths as live-on-main by *not* adding absent-path rows for them — see Residual R-1 — while this doc rewrites main's file list to the new names. The two main-describing records now disagree.)
- **Impact**: a cold agent restarting CSB work — the doc's stated `use_when` — is told main already carries the role-aligned names. It may conclude the rename has landed, or fail to find the files when operating against real main. The doc's own `git cat-file -e HEAD:<path>` recheck recipe still lists only the `docs/…` historical paths, so it does not catch this.
- **minimum_closure_condition**: the reconciliation note's main-state file list reflects what its pinned `origin/main` baselines actually contain (old names) until a baseline that contains the new names is pinned; OR the doc is re-pinned to a revision that genuinely carries the new names and the baseline prose is updated to match. The pin and the body must agree.
- **next_authorized_action**: CA decision on revert-names-vs-repin; the doc's `stale_if` is already triggered and routes a post-merge refresh.
- **patch_queue_entry**: not authorized.
- **red-green proof**: `not_applicable` (verifiable by `git ls-tree <pinned-baseline>` vs. the record).
- **not proven**: nothing further; the falsity is verified against the doc's own pins.

---

## Phase 2 — Friction / Minor

### AR-03 (minor · friction) — `spine.yaml` YAML key renames exceed the stated "filename/path rename" scope

- **Phase**: friction
- **Reviewed target / role**: `Spine manifest` — `orca/product/spines/commission_signal_board/spine.yaml`.
- **Location**: `canonical_artifacts` (`authority_packet` → `prompt_structure_rules`, `prompt` → `prompt_structure`; the two "Historical key retained for path stability" comments removed) and `legacy_absent_paths` (`adjudication_packet` → `old_prompt_adjudication_packet`, `prompt` → `old_prompt`).
- **Source authority**: commission scope statement ("filename/path rename"); `.agents/workflow-overlay/validation-gates.md` (receipt-field provenance / single-source) — advisory only here.
- **Artifact evidence**: the commission frames the change as a path/name rename, but the patch also renames the YAML map **keys** (not just the path values). A consumer sweep (`rg` over `.agents`, `orca-harness` for `canonical_artifacts.*` / `legacy_absent_paths.*` / `authority_packet` / `adjudication_packet:` key reads) found **no** consumer, and the validator selftest passes — so this is scope-widening, not breakage.
- **Strongest defense, and why it holds partially**: the new keys are role-aligned and the removed comments were only needed because the old keys were misaligned — so the change is internally coherent and arguably an improvement. This defense holds enough to keep the finding **minor**, not major: there is no demonstrated breakage. It does not fully dissolve the finding because (a) it widens the change surface beyond the commission's stated scope without a note, and (b) it introduces a key-prefix inconsistency: `legacy_absent_paths` now has `old_prompt` and `old_prompt_adjudication_packet` but the sibling `playbook` key keeps no `old_` prefix.
- **Impact**: low; future-maintenance/consistency only. Any out-of-tree or future consumer that read `canonical_artifacts.prompt` / `.authority_packet` would silently miss; none exists today.
- **minimum_closure_condition**: the key renames are acknowledged as in-scope (or reverted to value-only changes), and `legacy_absent_paths` key naming is internally consistent (all-`old_` or none).
- **next_authorized_action**: CA note / optional follow-up; no action required for correctness.
- **patch_queue_entry**: not authorized.
- **red-green proof**: `not_applicable`.
- **not proven**: that no consumer exists anywhere outside the swept roots — sweep covered `.agents` and `orca-harness`; a hypothetical external/tooling reader is `not proven` absent, only absent in-repo.

### AR-04 (minor · friction) — New `prompt_structure` name is a strict prefix of `prompt_structure_rules` (substring-match ambiguity)

- **Phase**: friction
- **Reviewed target / role**: the two new canonical filenames (cross-cutting).
- **Location**: `…/prompts/orca_commission_signal_board_prompt_structure_v0.md` vs. `…/authority/orca_commission_signal_board_prompt_structure_rules_v0.md`.
- **Source authority**: the fitness goal ("unambiguous future-agent source loading").
- **Artifact evidence**: `orca_commission_signal_board_prompt_structure` is a literal prefix of `orca_commission_signal_board_prompt_structure_rules`. A substring/prefix `rg` for the prompt name matches the rules file too (observed: a `prompt_structure(_rules)?` sweep returns both). The paired directory (`prompts/` vs `authority/`) and role labels disambiguate for a careful reader, so this is a residual robustness risk, not a live defect.
- **Strongest defense, and why it holds partially**: the directory + role-label pairing already disambiguates, and the rename's primary goal (kill the misleading `prompt` / `adjudication_packet` names) is met — so this stays **minor**. It is not dropped because the stated goal is specifically *unambiguous* loading, and prefix-collision names are marginally less robust for any tool that matches on filename substring (including future stale-reference sweeps for this very pair).
- **Impact**: low; possible future false-positive/false-negative in substring-based sweeps or resolvers.
- **minimum_closure_condition**: accept the residual explicitly, or adopt a non-prefix name for one artifact; no correctness action required.
- **next_authorized_action**: CA note only.
- **patch_queue_entry**: not authorized.
- **red-green proof**: `not_applicable`.

---

## Non-Findings (positives verified)

These were attacked and held up — recorded so the CA can see the negative space was checked, not skipped:

1. **No live stale old-name reference.** Sweep 1 over `.agents docs orca` (md/yaml/py) and the broad all-filetype sweep return old canonical-spine paths only in (a) the review-prompt artifact itself (describing the rename) and (b) frozen review-**input** snapshots — never in a live source surface.
2. **Repo map clean.** `docs/workflows/orca_repo_map_v0.md` (not in the commit) carries no CSB prompt/authority reference, so no stale navigation surface was left behind.
3. **Historical absent paths preserved, not invented.** `moved_paths_index.md` left-column old `docs/…` paths and `spine.yaml legacy_absent_paths` **values** are unchanged; only the canonical-target (right-side) was updated to the new names — the "invented historical paths" failure mode did not occur.
4. **Resolver right-column correctly tracks the rename** within the branch tree.
5. **Frozen review-input snapshots correctly left with old names** (`docs/review-inputs/capture_spine_core_migration_…/*.snapshot.txt`, `diff_u80.patch`) — the correct treatment, and the contrast that makes AR-01 a defect.
6. **Role labels consistent.** "Prompt Structure" ↔ `prompts/…prompt_structure_v0.md`; "Prompt Structure Rules" ↔ `authority/…prompt_structure_rules_v0.md` across README, spine.yaml keys, playbook, and the w3a proposal. The README naming note was correctly updated ("File paths now use role-aligned names").
7. **Precise, non-greedy propagation.** `scanning_w3a_proposal_v0.md` kept the unrelated `orca_demand_scan_gate_adjudication_packet_v0.md` (a different artifact) while updating only the CSB authority reference — "adjudication packet" was not blindly rewritten.
8. **Retrieval headers intact; renames clean.** Both renames are `R099`; only path-reference lines changed inside the renamed files; `git diff --check` exit 0; validator selftest `SELFTEST OK`.

---

## Residual Risks / Forward Obligations / Validation Gaps

- **R-1 (forward obligation, NOT a current defect).** The rename supersedes spine paths that are **live on `origin/main`** today. `moved_paths_index.md` and the reconciliation "Historical Paths Not Live" list add **no** old-spine → new-spine row. This is **correct for this pre-merge commit** — the old spine paths are still present on main, so an "absent" row now would itself be a false claim. The obligation is **at/after merge**: once `c992fe7e` lands on main, `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md` and `…/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md` become absent-on-main with no resolver entry, so old-spine → new-spine rows should be added then (and the reconciliation doc re-pinned — see AR-02). Flagged so the gap is not silently carried past merge.
- **R-2 (fitness-axis tension).** The patch advances the goal for the *live-tree* reader (role-aligned names) but regresses the *historical-integrity* reader (AR-01/AR-02 inject false history into pinned records). The success signal's "old filenames survive … in frozen snapshots" clause is exactly the part violated. The goal as written is sound; the patch's execution over-reaches one half of it.
- **Doctrine-receipt note (advisory).** The commit is a CSB-local naming/manifest change and carries no `direction_change_propagation` receipt. Per `source-of-truth.md`, the DCP contract triggers on product/architecture/workflow/validation/review/output doctrine or a lifecycle boundary; a single-spine artifact rename does not squarely hit those, so a receipt does not appear strictly required and its absence is **not** raised as a finding. Recorded only so the CA can confirm that judgment against its own intent.
- **Validation gaps in this review.** This is read-only and pre-merge: no merge, no post-merge main state, and no runtime behavior were exercised. The validator selftest (`--selftest`) is the only executable evidence and concerns row-shape enforcement, not the rename. `reviewed_by` / `authored_by` are `unrecorded`, so same-vs-cross-vendor coverage for this review is a visible measurement gap, not a captured measurement.

---

## Review-Use Boundary

These findings and non-findings are **decision input only** for the Chief Architect / owner. They are not approval, validation, product proof, readiness, mandatory remediation, or executor-ready patch authority. The `critical/major/minor` labels are finding-priority only and create no rejection, readiness, or remediation authority. No `patch_queue_entry` is emitted (read-only adversarial artifact review). Remediation becomes mandatory or executor-ready only if a separately authorized Orca patch, acceptance, validation, or implementation lane accepts it. The two major findings are verifiable now (`git ls-tree` against the cited pins); the minors and residuals are advisory.

**Next authorized step**: CA adjudication of AR-01 and AR-02 (revert-to-historical-names vs. annotate/re-pin) before the rename lands on main; AR-03/AR-04 and R-1/R-2 are optional/forward.
