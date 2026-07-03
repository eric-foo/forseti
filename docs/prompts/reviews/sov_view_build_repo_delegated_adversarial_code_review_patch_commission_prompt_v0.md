# Repo-Mode Delegated Adversarial Code Review + Patch Commission — SoV Readout View Build (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the share-of-voice readout view
  build (data_lake/sov_readout.py + its runner + its conformance tests),
  dispatched to an external GPT-family controller WITH repository read access.
  Uses the delegated_code_review_and_patch sibling mode of
  .agents/workflow-overlay/delegated-review-patch.md: code-review lane as the
  method, an explicitly named multi-file patchable set, named test obligations,
  delegate-authored diff, home-CA adjudication before any keep.
use_when:
  - Dispatching the commissioned SoV view-build code review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch `claude/sov-view-build`
  (PR head), pinned commit `59225845ba8f497a95ef6865bc27367cf639327c`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface):
  - `orca-harness/data_lake/sov_readout.py` — SHA256 `60F8FCD2887FF7149E33EEF0B3AAD1504A8D662B40D6EA5F3B1C4E408B0205D2`
  - `orca-harness/runners/run_data_lake_sov_readout.py` — SHA256 `B5BA73A636E0B5193AE8E13054BE14B3E8F92565F7A8CA0B0392667F5D00791F`
  - `orca-harness/tests/test_data_lake_sov_readout.py` — SHA256 `092BDE1E3B22BB6130106F8B38BD114FA8068533C335550712C43380590AF654`
  (LF git blob bytes at the pinned commit.)
- Read-only / flag-only in the same change (generated or gate surfaces — flag,
  never patch): `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`,
  `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`.
- Access mode: `repo` — inspect the pinned source in place. No substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; it does not commit, push, open PRs, or write outside
  the named set. Read-only repo access is sufficient.
- Named validation obligation: `python -m pytest orca-harness/tests/test_data_lake_sov_readout.py`
  plus the two gate suites
  (`tests/contract/test_capture_runner_lake_seam_coverage.py`,
  `tests/contract/test_data_lake_inventory_gate.py`). If the runtime cannot
  execute tests, say so and review statically — never assert a pass that was
  not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/sov_view_build_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch
  (this dispatch) → home-CA adjudication of the returned diff (accept/modify/
  reject per change, class sweep + byte/scope checks) → keep decision.
  Repo-mode discovery discharges the independent-review gate for the patched
  set; no separate post-patch cross-vendor re-scan is required.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch overlay Code-diff section +
    repo-mode commission pattern reused from the SoV field-contract dispatch;
    target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/sov_view_build_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/sov-view-build; implementation committed at 59225845ba8f497a95ef6865bc27367cf639327c)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by artifact-folders overlay file.
```

## Paste-ready commission body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT — gate yourself first: the review target was authored by an
Anthropic (Claude-family) model. This commission requires a DIFFERENT vendor /
model lineage (vendor = upstream model developer, not host/reseller/wrapper).
If you are Anthropic/Claude-lineage, or your lineage is unknown or
undisclosable, reply ONLY `BLOCKED_DECORRELATION` (plus your vendor if
permitted) and stop. This is a who-constraint of the commission, never a model
recommendation. State your model identity and version in your output if known
and permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/sov-view-build, pinned commit 59225845ba8f497a95ef6865bc27367cf639327c
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing else):
  1. orca-harness/data_lake/sov_readout.py        (SHA256 60F8FCD2887FF7149E33EEF0B3AAD1504A8D662B40D6EA5F3B1C4E408B0205D2)
  2. orca-harness/runners/run_data_lake_sov_readout.py (SHA256 B5BA73A636E0B5193AE8E13054BE14B3E8F92565F7A8CA0B0392667F5D00791F)
  3. orca-harness/tests/test_data_lake_sov_readout.py  (SHA256 092BDE1E3B22BB6130106F8B38BD114FA8068533C335550712C43380590AF654)
  (LF git blob bytes; confirm the hashes if you can, otherwise confirm you are
  reading the files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`
— do not review from memory, summaries, or a re-created copy. If you can open
the repo but not the pinned commit, review the files on the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the first metric-family view build over the data lake —
the share-of-voice readout computation (on-demand-first), its optional
materialization as a rebuildable manifest-backed cache under
indexes/derived_retrieval/metric_family/, its prove-rebuildability check, its
CLI runner, and its conformance tests. A defect here becomes a plausible but
dishonest buyer-facing number.

CONTRACTS THE CODE MUST IMPLEMENT — read these in the pinned repo (plan your
reads: record a one-line disposition per source — full / targeted <section> /
grep <token> / skip: <reason> — lean on confirmatory sources, expand to full
the moment a source could change a finding):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
  (THE controlling field contract: mention-level refs with
  mention_count == len(mention_refs), window-basis inclusion rules,
  cohort reconciliation, comparison_set-gated zero rows, posture semantics,
  coverage block, forbidden fields)
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (On-Demand-First Metrics Policy; prove-rebuildability semantics; views are
  caches, never authoritative, never read by pickup)
- orca-harness/data_lake/derived_retrieval_views.py (the incumbent view-builder
  pattern; note its by_mention view DEDUPES record refs BY DESIGN — the SoV
  numerator must NOT inherit that)
- orca-harness/data_lake/silver_lineage.py (the read-side lineage gate the
  code must apply)
- orca-harness/cleaning/transcript_product_lake.py +
  orca-harness/schemas/product_mention_models.py (the committed mention record
  shape the readout consumes)
- orca-harness/data_lake/root.py (by-key read API; write-boundary rules)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the load-bearing behaviors,
   contract clauses, and likely failure modes before any finding.
2. MAXIMALLY ADVERSARIAL code review of the named set against the contracts:
   field-contract conformance (can this code emit a readout that a conforming
   reader would misread — silent denominator shrinkage, invented zeros,
   non-recomputable shares, refs that don't dereference, coverage counts that
   lie?); correctness (window boundary conditions, timestamp parsing,
   determinism of materialized bytes, prove-rebuildability soundness);
   failure visibility (silent drops, fake-success paths, swallowed errors);
   test adequacy (do the tests actually pin the contract clauses they claim,
   or can the implementation regress without a test failing?); scope
   discipline (overreach AND underfix). Severity labels critical/major/minor
   are finding-priority only.
3. BOUNDED PATCH: author the smallest complete amendment to the NAMED SET ONLY
   that closes your accepted-quality findings. Return it as a unified diff in
   this chat (do NOT commit, push, or open a PR; do NOT touch any file outside
   the named set — the touchpoint inventory JSON and the seam-coverage counter
   test are generated/gate surfaces: flag, never patch). Run the named tests
   if your runtime can; report real results either way. If the problem is
   design-level rather than patch-level, return `NEEDS_ARCHITECTURE_PASS`
   with findings only and NO diff.

RETURN, in this order:
1. review_summary YAML (status / recommendation / findings_count /
   blocking_findings / advisory_findings / summary), then findings ordered
   critical → major → minor, each with severity / location (file:line) /
   issue / evidence (cite the code AND the conflicting contract clause with
   path) / impact / minimum_closure_condition / next_authorized_action /
   advisory remediation direction.
2. The unified diff for the named set, each hunk annotated with the finding(s)
   it closes, plus per-change source citations — neutral in tone,
   decision-sufficient in substance.
3. Verdict + residual-risk note (one overall verdict; per-file sub-verdicts if
   the files differ materially).
4. Real test-run results, or an explicit statement that tests were not run and why.
5. One-line read-budget audit: initial vs actual per-source dispositions and
   why any source expanded.
6. Adjudicator tail (for the commissioning Chief Architect, not for you to
   act on): your diff, citations, verdict, and test claims are claims to
   adjudicate — accept/modify/reject per change; the CA may veto any change at
   its discretion; nothing is kept until that adjudication, closed per
   .agents/workflow-overlay/communication-style.md -> Review Adjudication
   Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste the body into a GPT-family (non-Anthropic) lane with the GitHub repo
  connected/readable (your stated target: ChatGPT with repo access).
- On return, courier the full output back into the home lane for review-return
  adjudication (accept/modify/reject per change; the CA applies kept hunks;
  repo-mode discovery discharges the independent-review gate — the CA's class
  sweep + byte/scope checks cover the delegate's own edited lines).
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
