# Scanning Spine Bloat Cut + Precursor Vocab — Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Read-only adversarial artifact review of the scanning-spine bloat-cut and
  precursor-vocabulary change packet at commit
  8e70605c1e24ad38997d7c94bcdbd67da1728f3f (parent 777a3988).
use_when:
  - Adjudicating whether the scanning-spine vocabulary-alignment packet is safe to merge.
  - Checking residual receipt-completeness and inheritance-claim risks before acceptance.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - docs/prompts/reviews/scanning_spine_bloat_cut_precursor_vocab_adversarial_review_prompt_v0.md
branch_or_commit: 8e70605c1e24ad38997d7c94bcdbd67da1728f3f
input_hashes:
  - target_commit: 8e70605c1e24ad38997d7c94bcdbd67da1728f3f
  - target_parent: 777a3988b2ad10e5c37269fa1ca80bd0f1d5724d
stale_if:
  - The target commit is rebased, amended, or superseded.
  - A later commit re-homes the AEO probe evidence again or changes scanning vocabulary.
```

## Provenance

```yaml
reviewed_by: claude-opus-4-8            # this review was performed by Claude Opus 4.8
authored_by: gpt-5-codex               # per the filing prompt's stated change-packet author provenance
de_correlation_bar: cross_vendor_discovery
de_correlation_note: >
  Reviewer vendor (Anthropic / Claude Opus 4.8) differs from the stated author
  vendor (OpenAI / gpt-5-codex), so the cross-vendor discovery bar is satisfied.
  Caveat: the bar rests on the prompt's stated authorship; the git committer of
  8e70605c is "Eric <fooyuquan@gmail.com>". If the true drafting author were not
  gpt-5-codex, re-evaluate the bar. Provenance is an observed record, not a model
  recommendation.
```

## Recommendation

`accept_with_friction`. The packet meets its stated fitness goal: the scanning
spine now has one retrieval-only front door, precursor vocabulary is defined
and consistently fenced off from demand-proof / gate-clearance / capture
authority, and the moved AEO probe leaves no live stale routing back into
product-spine authority. The single non-clean item is a minor
propagation-evidence completeness gap in the new README's `direction_change_propagation`
receipt (AR-01); it is advisory, not blocking. Three further observations are
optional hardening only.

## Method And Source Context

- **Method sequence.** Reference-loaded `workflow-deep-thinking` and
  `workflow-adversarial-artifact-review`; source-loaded the required authority
  sources and the change packet; declared `SOURCE_CONTEXT_READY`; applied
  deep-thinking framing to set failure modes, then applied adversarial artifact
  review. Both skills were available and applied.
- **Deep-thinking discipline.** Used to frame the eight commissioned attack
  axes as candidates to break (not a pass bar), to separate "no live control
  lost" from "claim slightly imprecise," and to downgrade findings whose strongest
  defense holds.
- **Trigger gate.** Adversarial artifact review of non-code docs/product-spine
  artifacts — in lane.
- **Lane collision.** Routed correctly. The request arrived via
  `workflow-delegated-review-patch`, but that convention is provisional and
  single-target for patch authority; a multi-file docs packet is explicitly
  out of its scope (`delegated-review-patch.md:39-49,133-137`), so this is
  read-only adversarial artifact review with no patch authority. Verified, not
  assumed.
- **Artifact-role / output binding.** Review report role →
  `docs/review-outputs/adversarial-artifact-reviews/` (artifact-roles.md;
  review-lanes.md "Current Lanes"). `filesystem-output` to the prompt-named path.
- **Fitness reference.** Bound by the prompt (goal: "easier to enter and harder
  to misuse"; signal: one front door, precursor signals not treated as proof,
  no live stale AEO routing). Attacked as an alignment axis, not a match bar —
  see Confirmations. The goal/signal are well-formed and observable; no
  `no checkable success bar` gap.
- **Validation gates.** Treated as claims to inspect. Reran the one the prompt
  flagged (placement checker) — reproduced exactly.

### Source-read ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` (kernel) | Authority boundary, smallest-complete, deletion/claim discipline | In session context |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy; DCP receipt contract | Clean @ HEAD 7effd159 |
| `.agents/workflow-overlay/artifact-roles.md` | Research-artifact + review-report role bindings | Clean |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract for README/report | Clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Verify route-out boundary | Clean |
| `.agents/workflow-overlay/review-lanes.md` | Output binding, two-bar de-correlation, findings doctrine | Clean |
| `.agents/workflow-overlay/communication-style.md` | Courier YAML + failed-write shape | Clean |
| `.agents/workflow-overlay/source-loading.md` | Verify "no scanning read pack" receipt claim | Targeted grep (1 incidental hit, line 604) |
| Target commit `8e70605c` full diff + 12 changed files | Review object | Clean working tree @ HEAD |
| `docs/research/answer_engine/aeo_..._phase0_v0.md` | Verify GO-vs-RE-ROUTE for the status rename | Clean |

Dirty-source names: none. The target worktree is clean at HEAD `7effd159`
(which is `8e70605c` + the commit that filed the review prompt). The commit
diff was read from the shared object DB.

Not separately opened (no finding depends on them; reason recorded):
`validation-gates.md`, `prompt-orchestration.md`, overlay `README.md`.

## Review Scope

- **In scope:** the 12-file change packet at `8e70605c` (docs / product-spine
  vocabulary alignment, scanning front-door README, AEO probe rehome, migration
  resolver + repo-map edits).
- **Excluded:** the entire repository outside the packet; the filing review
  prompt itself; historical `docs/review-inputs/**` snapshots (frozen, examined
  only to confirm old-path hits are non-live); implementation/runtime/code
  correctness (no code in this packet).

## Findings

No `critical` findings. No `major` findings.

### AR-01 (minor, correctness-leaning) — README propagation receipt under-records the move it documents

- **Phase:** correctness.
- **Commission target / purpose:** scanning-spine cleanup packet; whether the
  direction-change propagation receipt is complete enough for future agents
  (axis 7) and whether stale references survive (axes 5–6).
- **Artifact role:** Scanning spine front-door index (controlling source of this
  doctrine change).
- **Location:** `orca/product/spines/scanning/README.md:108` (the
  `direction_change_propagation.stale_language_search` line, inside the receipt
  beginning at the `## Direction Change Propagation` block).
- **Source authority:** `.agents/workflow-overlay/source-of-truth.md:113-131`
  (DCP receipt shape) and the file's sibling receipts in `source-of-truth.md`
  and `linkedin/...architecture_v0.md`, which pair `stale_language_search` with a
  recorded `stale_language_search_result`.
- **Evidence:** the recorded search is
  `rg -n "precursor_signal|precursor_surface|capture-needs list|crawler|monitor|registry|atlas|route binding" orca/product/spines/scanning docs/workflows/orca_repo_map_v0.md`.
  This receipt's own `doctrine_changed` states the change "rehomes the AEO
  Phase-0 probe artifacts," yet the recorded query (a) does **not** search for
  the old AEO path
  `orca/product/spines/scanning/source_families/answer_engine/aeo_capture_feasibility_probe_phase0`,
  the packet's primary dangling-reference risk, (b) scopes only to
  `orca/product/spines/scanning` + the repo map, omitting the rest of `docs/`
  where a stale AEO pointer could live, and (c) records no
  `stale_language_search_result`, unlike the file's sibling receipts.
- **Strongest defense, and why it only partly holds:** the canonical receipt
  field in `source-of-truth.md` requires only the query (or `not_run` + why), so
  the field is *technically* satisfied, and the real-world outcome is in fact
  clean — I independently ran the old-path grep and found hits **only** in frozen
  `docs/review-inputs/**` snapshots, no live routing reference (so nothing is
  actually broken). The defense holds for "is the repo correct" but fails for
  "is the durable propagation evidence sufficient": for a non-additive change
  that *moves a file*, a stale-language search that never searches the old path
  cannot evidence the move's main risk, so a future agent auditing via the
  receipt would not see the move verified.
- **Impact:** low. Routing is correct today; the gap is in the audit trail, not
  the live tree. A future agent relying on the receipt re-derives less than it
  thinks it has.
- **`minimum_closure_condition`:** the README receipt's `stale_language_search`
  covers the rehomed AEO path across `docs/` (not just the scanning spine), and
  records the result (live hits only in frozen review-input/migration snapshots),
  matching the depth of the file's sibling receipts.
- **`next_authorized_action`:** owner/CA decision — accept as-is (the outcome is
  verified clean here) or commission a one-line receipt edit. No patch authority
  is conferred by this review.
- **`patch_queue_entry`:** not authorized (read-only adversarial artifact review).
- **Red-green proof:** `not_applicable` (documentation receipt completeness,
  not an executable check).
- **Advisory remediation direction:** widen the recorded query to include the
  old AEO spine path and the broader `docs/` tree, and append a one-line
  `stale_language_search_result` noting hits are confined to frozen snapshots.

## Confirmations (axes attacked that held)

These are not findings; they record the adversarial checks whose strongest
break-attempt failed, so the CA sees coverage rather than silence.

- **Front door does not become a new authority layer (axis 1).**
  `README` carries `authority_boundary: retrieval_only`, opens by routing to the
  MGT model "first," and its normative restatements are faithful to the
  controlling source (README "precursor signals … do not prove demand, clear a
  gate, authorize capture, or create a standing source map" matches MGT
  `precursor_signal` "not proof, gate clearance, or capture authorization" and
  `precursor_surface` "not a registry, atlas, monitor, or standing source map").
  No softening or strengthening detected.
- **Precursor vocabulary stays separate from gate proof / promotion / capture
  (axis 2).** Fenced consistently in four places:
  `scan_core/...mgt_operating_model_v0.md:164-183,196-198,208` (signal_stage vs
  gate_role; "do not mint … source-access authority or gate proof"),
  `scan_core/orca_demand_scan_core_spec_v0.md` (§3 "a precursor by itself is not
  gate proof"; promotion-rule gating), the README boundary, and the answer-engine
  adapter ("`precursor_signal` unless promoted … never absence-of-demand by
  itself").
- **`capture_request` alias keeps "capture-needs list" searchable, not
  authoritative (axis 3).** Verified by grep: live `capture-needs list` survives
  only as the explicit alias at
  `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md:530`
  and inside the README search-query string; every other hit is a frozen
  review-input snapshot.
- **Adapters map local terms without losing source-specific hard stops (axis 4).**
  Reddit and the LinkedIn lane index only *added* vocabulary sections. The
  LinkedIn architecture file replaced an inline hard-stop paragraph
  (`...linkedin_discovery_planning_lane_architecture_v0.md:51-53`) with an
  "inherited from README/MGT" pointer, but its dedicated **Hard Stops**
  (`:376-402`) and **Non-Claims** (`:445-467`) sections, plus "No implementation
  is authorized by this artifact alone" (`:429`), preserve every substantive
  stop from the removed paragraph (autonomous scraping, bulk export, contact
  harvesting, lead-list, profile-body harvesting, storage/scheduler/dashboard/
  production-runtime, commercial use, ECR/Cleaning/Judgment/buyer-proof). See
  AR-OBS-1 for the one literal item not re-enumerated.
- **AEO move removes product-spine authority leakage; resolver paths coherent
  (axes 5–6).** The probe + evidence moved to `docs/research/answer_engine/`,
  re-roled "Research/probe feasibility report … NOT product-spine authority";
  the answer-engine *delta spec* (product authority) correctly stays in the
  spine and its `open_next` now points to the research home. Grep confirms no
  live reference to the old spine AEO path; the repo map, `moved_paths_index.md`,
  and `moves_manifest.csv` resolver rows all point to the current home.
- **Status rename is accurate, not inflated (axis 8).** The delta spec status
  `..._AFTER_PHASE0_GO` is backed by the probe report's actual verdict —
  `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md:31,217`
  reads "GO (qualified)" (AI Overview fired 10/10) — and the spec still marks
  owner adjudication as pending and keeps the infeasibility re-route `stale_if`.
- **Placement / advisory-debt claim is accurate (axis 8).** Reran
  `python .agents/hooks/check_placement.py --check` in the target worktree:
  `summary: 11 violation(s), 4 freshness, 869 legacy-tolerated`, exactly as the
  dispatcher reported. All 11 violations and 4 freshness warnings are
  pre-existing repo-infra entries (`.gitattributes`, `.githooks/*`, `.github/*`).
  The new README and the moved `docs/research/answer_engine/*` files introduced
  **zero** new placement debt.
- **"No scanning read pack" receipt claim is accurate.** `source-loading.md`
  has only one incidental scanning mention (line 604), no scanning source pack;
  the one-hop path is supplied via the (updated) repo map, and source-loading.md
  is listed in the receipt's `downstream_surfaces_checked` and
  `intentionally_not_updated` with a stated reason — satisfying the DCP contract.

## Optional Hardening (non-required, non-blocking)

Each defense below holds; these are recorded as residual risk, not findings.

- **AR-OBS-1 — LinkedIn "inherited" claim is slightly imprecise.** The replaced
  paragraph's "commits, pushes, or PRs" is the one item not re-enumerated in the
  LinkedIn Hard Stops/Non-Claims, and the named inherited sources (README, MGT
  model) do not enumerate it either; it is covered only by the general "not
  implementation authorization" non-claim and the global overlay/harness
  protected-action guard. No actual control is lost (git lifecycle is globally
  governed, never conferred by this product doc). Optional: add "commits/pushes/
  PRs" to the LinkedIn Hard Stops, or accept the global-guard coverage.
- **AR-OBS-2 — README duplicates the canonical vocabulary and boundary lists.**
  The "Shared Output Vocabulary" and "Boundary" sections restate the MGT model's
  enumerations rather than pointing to them, against `source-of-truth.md`'s
  "prefer pointing over duplicating" preference. Defense holds: a front-door
  index has genuine orientation value in listing the terms, and the README's
  `stale_if` ("MGT … changes its shared vocabulary or hard boundaries") is the
  desync guard the contract would want. Optional: trim to a pointer if the
  duplication later drifts.
- **AR-OBS-3 — `moves_manifest.csv` records the final research home, not the
  spine-first intermediate.** The AEO rows were edited from the spine
  destination to `docs/research/answer_engine/`, so the spine-first migration
  manifest now records a two-hop move as one. Defense holds: as a live resolver,
  pointing to the current home is the maintainable choice and avoids a dangling
  pointer to the now-empty spine location. Optional only if the manifest is later
  treated as an immutable historical record rather than a resolver.

## Not-Proven Boundaries

- `authored_by: gpt-5-codex` rests on the prompt's stated provenance; the git
  committer is `Eric`. Cross-vendor de-correlation is asserted on that basis.
- This review did not open `validation-gates.md`, `prompt-orchestration.md`, or
  the overlay README; their bearing was covered via `review-lanes.md` +
  `communication-style.md`. No strict claim here depends on the unopened files.
- The `--changed` header/freshness checks were `not_run` (clean post-commit tree
  yields no changed set); only the repo-wide placement check was reproducible and
  was rerun.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness,
acceptance of commit `8e70605c`, mandatory remediation, product proof, merge
authorization, or executor-ready patch authority. AR-01 and the AR-OBS items are
findings and advisory direction for the Chief Architect to adjudicate; none
becomes mandatory or executor-ready without a separate accepted patch or
execution lane.

## Delegated Artifact Review Return Courier

```text
DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: read-only adversarial artifact review of the scanning
  spine bloat-cut + precursor vocab change packet (filing prompt
  docs/prompts/reviews/scanning_spine_bloat_cut_precursor_vocab_adversarial_review_prompt_v0.md).
- reviewed artifact / scope: commit 8e70605c (12 files), read-only; no patch
  scope bound (multi-file packet → route-out to read-only artifact review).
- findings: AR-01 (minor) README propagation receipt under-records the AEO move;
  three optional-hardening observations (AR-OBS-1/2/3).
- proposed artifact patch: none authorized (read-only); advisory remediation
  direction only, recorded per finding.
- citations: README.md:108; linkedin ...architecture_v0.md:51-53,376-402,445-467,429;
  mgt_operating_model_v0.md:164-183,196-198,208; demand_scan_core_spec_v0.md:530;
  aeo ...phase0_v0.md:31,217; delegated-review-patch.md:39-49,133-137;
  source-loading.md:604; placement-check rerun (11/4/869).
- reviewer verdict: accept_with_friction.
- residual risk: provenance rests on stated gpt-5-codex authorship (git
  committer is Eric); receipt audit-trail gap (AR-01) is evidence-completeness,
  not a live broken reference.
- blockers / off-scope / not-proven: none blocking; not-proven boundaries listed
  above.
```
