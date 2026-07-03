# Repo-Mode Delegated Adversarial Artifact Review + Patch Commission — Share-of-Voice Field Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor review
  AND bounded patch of
  core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md,
  dispatched to an external GPT-family controller WITH repository read access.
  Supersedes the no_repo bundle dispatch for this commission (the repo-mode
  loop is strictly stronger: de-correlated patch authorship, and per the
  overlay it discharges the downstream independent-review gate for the patched
  artifact).
use_when:
  - Dispatching the commissioned SoV field-contract review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch `main`, pinned commit
  `cf43db5f26f2eebc91854ce88f1c4678bb9a360c` (the PR #600 merge commit).
- Review target (single named artifact; whole file; the ONLY patchable surface):
  `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md`
  — content SHA256 `33C7F793AB049A9EE3655A7194FF39B8E3B83307D8B1C63E1A3D97FB24792F4B`
  (LF file bytes; git blob `8c3f8306` on `main`).
- Access mode: `repo` (overlay default) — the reviewer inspects the pinned
  source in place. No substitute source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; it does not commit, push, open PRs, or write outside
  the named target. Read-only repo access is sufficient — the diff in chat IS
  the patch return.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/sov_field_contract_adversarial_artifact_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode loop per
  `.agents/workflow-overlay/delegated-review-patch.md`: de-correlated discovery
  review + delegate-authored bounded patch (this dispatch) → home-CA
  adjudication of the returned diff (accept/modify/reject per change, class
  sweep + byte checks) → keep decision. Repo-mode discovery discharges the
  independent-review gate for the patched artifact; no separate post-patch
  cross-vendor re-scan is required.
- Supersession: the no_repo bundle + wrapper
  (`docs/prompts/wrappers/sov_field_contract_norepo_adversarial_artifact_review_wrapper_v0.md`)
  is superseded for this commission — do not also dispatch it (a duplicate
  review would double-count findings).

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch overlay binding + review prompt
    defaults, loaded this thread; target + authority contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact + supersession note only)
  target_scope: docs/prompts/reviews/sov_field_contract_repo_adversarial_artifact_review_patch_commission_prompt_v0.md,
    docs/prompts/wrappers/sov_field_contract_norepo_adversarial_artifact_review_wrapper_v0.md (supersession note)
  dirty_state_checked: yes (lane claude/sov-field-contract; PR #600 merged as cf43db5f)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by artifact-folders overlay file.
```

## Paste-ready commission body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL ARTIFACT REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT — gate yourself first: the review target was authored by an
Anthropic (Claude-family) model. This commission requires a DIFFERENT vendor /
model lineage (vendor = upstream model developer, not host/reseller/wrapper).
If you are Anthropic/Claude-lineage, or your lineage is unknown or
undisclosable, reply ONLY `BLOCKED_DECORRELATION` (plus your vendor if
permitted) and stop. This is a who-constraint of the commission, never a model
recommendation. State your model identity and version in your output if known
and permitted.

REPOSITORY ACCESS — you are expected to read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: main, pinned commit cf43db5f26f2eebc91854ce88f1c4678bb9a360c
- REVIEW TARGET (the single artifact you review AND may patch):
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
  (content SHA256 33C7F793AB049A9EE3655A7194FF39B8E3B83307D8B1C63E1A3D97FB24792F4B
  over LF bytes; confirm the hash if you can, otherwise confirm you are reading
  the file at the pinned commit and say so)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`
— do not review from memory, summaries, or a re-created copy. If you can open
the repo but not the pinned commit, review the file on current `main` and state
the commit you actually read.

WHAT THE TARGET IS: the field-level contract every share-of-voice computation
or view over this data lake must conform to — readout identity, grouping,
numerator/denominator/coverage fields, window basis, posture semantics, and
forbidden fields. It gates the family's first buyer-facing view build. A defect
here becomes a dishonest-but-plausible buyer readout.

AUTHORITY SOURCES the target must conform to — read these in the pinned repo
(plan your reads: record a one-line disposition per source — full / targeted
<section> / grep <token> / skip: <reason> — default lean on confirmatory
sources, expand to full the moment a source could change a finding):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (its On-Demand-First Metrics Policy + field-level gate are the commissioning
  authority for this target)
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  (Metric Observation Records posture table; Generated Read Models manifest
  obligations)
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  (indexes rebuildable-or-not-an-index; on-demand analysis rules)
- orca-harness/data_lake/silver_record.py (METRIC_POSTURE_KINDS + posture
  coupling enforcement — the live vocabulary the target claims to bind to)
- orca-harness/cleaning/transcript_product_lake.py (the committed mention
  record shape the target's numerator/refs depend on)
- orca-harness/data_lake/derived_retrieval_views.py (the incumbent view-builder
  pattern a SoV view would follow)
- AGENTS.md (root): the Smallest Complete Intervention rule and
  failure-visibility kernel — conformance is part of the review.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the target's load-bearing claims,
   decision criteria, and likely failure modes before any finding.
2. MAXIMALLY ADVERSARIAL review of the target against the authority sources:
   authority conformance; internal consistency; missing inputs/unbound intent;
   downstream executability (can a view builder act on this without inventing
   semantics?); fitness to goal — attack the goal too: can a CONFORMING readout
   still mislead a buyer (silent denominator shrinkage, fragmentation gaming,
   cohort cherry-picking, window-basis abuse, zero/posture leaks, coverage
   fields present but decision-useless)?; overclaims; leakage; scope discipline
   (overreach AND underfix). Severity labels critical/major/minor are
   finding-priority only.
3. BOUNDED PATCH: author the smallest complete amendment to THE TARGET FILE
   ONLY that closes your accepted-quality findings. Return it as a unified
   diff in this chat (do NOT commit, push, or open a PR; do NOT touch any
   other file). Everything outside the target is READ-ONLY — flag issues
   there, never patch them. If the target's problem is design-level rather
   than amendment-level, return `NEEDS_ARCHITECTURE_PASS` with findings only
   and NO diff.

RETURN, in this order:
1. review_summary YAML (status / recommendation / findings_count /
   blocking_findings / advisory_findings / summary), then findings ordered
   critical → major → minor, each with severity / location / issue / evidence
   (cite target section AND the conflicting in-repo authority with path) /
   impact / minimum_closure_condition / next_authorized_action / advisory
   remediation direction.
2. The unified diff for the target file, each hunk annotated with the
   finding(s) it closes, plus per-change source citations — neutral in tone,
   decision-sufficient in substance (your argument lives in the verdict and
   residual, not the citations).
3. Verdict + residual-risk note.
4. One-line read-budget audit: initial vs actual per-source dispositions and
   why any source expanded.
5. Adjudicator tail (for the commissioning Chief Architect, not for you to
   act on): your diff, citations, and verdict are claims to adjudicate —
   accept/modify/reject per change; the CA may veto any change at its
   discretion; nothing is kept until that adjudication.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste the body into a GPT-family (non-Anthropic) lane with the GitHub repo
  connected/readable — your stated target: ChatGPT 5.5 with repo access.
- On return, courier the full output back into the home lane for review-return
  adjudication (accept/modify/reject per change; CA applies kept hunks; repo-
  mode discovery discharges the independent-review gate, so no separate
  cross-vendor re-scan is required — the CA's class sweep + byte checks cover
  the delegate's own edited lines).
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
