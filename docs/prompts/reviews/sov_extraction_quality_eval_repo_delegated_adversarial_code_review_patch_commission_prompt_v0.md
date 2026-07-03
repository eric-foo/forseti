# Repo-Mode Delegated Adversarial Code Review + Patch Commission — SoV Extraction-Quality Eval (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the SoV extraction-quality eval
  (measurement runner + its tests), dispatched to an external GPT-family
  controller WITH repository read access. Same delegated_code_review_and_patch
  sibling-mode pattern as the SoV view-build commission; the special stake here
  is measurement honesty — an eval that can misclassify or silently drop
  records produces a false confidence number about the extraction layer.
use_when:
  - Dispatching the commissioned eval-runner code review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/sov-extraction-quality-eval` (PR head), pinned commit
  `2822d2c11ae98aeb5e399f9f379643d2b9a2ee87`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface):
  - `orca-harness/runners/run_sov_extraction_quality_eval.py` — SHA256 `9F857155C8964C720000AAAE27B4DEE362FAEBA204010B1F91DD7FB76E9B237C`
  - `orca-harness/tests/test_sov_extraction_quality_eval.py` — SHA256 `E900D9A61599AF54886940C6FB371C9C7F4771BB350E7E802C37255C906A8FF4`
  (LF git blob bytes at the pinned commit.)
- Read-only / flag-only in the same change (flag, never patch):
  `docs/workflows/sov_extraction_quality_eval_report_v0.md` (the measured
  baseline — if the code is wrong, its numbers are wrong: SAY SO),
  `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`,
  `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`.
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/test_sov_extraction_quality_eval.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/sov_extraction_quality_eval_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch →
  home-CA adjudication (accept/modify/reject per change, class sweep +
  byte/scope checks) → keep decision. Repo-mode discovery discharges the
  independent-review gate for the patched set.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/sov_extraction_quality_eval_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/sov-extraction-quality-eval; implementation committed at 2822d2c1)
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
permitted) and stop. Who-constraint only, never a model recommendation. State
your model identity and version in your output if known and permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/sov-extraction-quality-eval, pinned commit 2822d2c11ae98aeb5e399f9f379643d2b9a2ee87
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing else):
  1. orca-harness/runners/run_sov_extraction_quality_eval.py
     (SHA256 9F857155C8964C720000AAAE27B4DEE362FAEBA204010B1F91DD7FB76E9B237C)
  2. orca-harness/tests/test_sov_extraction_quality_eval.py
     (SHA256 E900D9A61599AF54886940C6FB371C9C7F4771BB350E7E802C37255C906A8FF4)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: a read-only MEASUREMENT instrument — the extraction-quality
eval whose published baseline (docs/workflows/sov_extraction_quality_eval_report_v0.md:
leak rate 8.8% upper bound, unknown-brand 16.4%, 15 orphaned records) feeds the
owner's go/no-go on trusting brand-level share-of-voice. The failure mode that
matters most is a MEASUREMENT LIE: a disposition that silently drops records, a
leak check that mismatches for mechanical reasons, a denominator that excludes
what it claims to include, or a report field whose name promises more than the
code computes. If the code is wrong, the published baseline is wrong — say so
explicitly in findings.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca-harness/data_lake/silver_lineage.py (gate statuses the eval counts by)
- orca-harness/cleaning/transcript_product_lake.py (cues_from_json3 semantics —
  rolling-duplicate collapse, fail-closed empty on corrupt json3 — and the
  mention record shape)
- orca-harness/data_lake/root.py (load_raw_packet fail-closed hash-verified
  read; list_available/read_availability by-key semantics)
- orca-harness/data_lake/sov_readout.py (the consumer whose trust question this
  eval informs; NOT patchable here)
- orca-harness/runners/run_transcript_product_extract.py (how records and
  raw_refs are actually written — what refs the eval should expect)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the measurement's load-bearing
   behaviors and the ways this eval could produce a wrong-but-plausible number.
2. MAXIMALLY ADVERSARIAL code review of the named set: disposition completeness
   (does every record/mention land in exactly one counted class — can anything
   be dropped or double-counted?); leak-check mechanics (casefold substring
   over joined cue text — mismatches from cue joining, rolling-caption
   collapse, whitespace, empty-transcript handling); denominator honesty
   (named vs unknown classification; does 'scanned' mean what the report says?);
   read-only guarantees (--out inside-lake refusal, no writes anywhere); CLI
   failure paths; test adequacy (can the implementation regress without a test
   failing?); scope discipline. Severity labels are finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY closing
   your accepted-quality findings; unified diff in chat; run the named tests if
   your runtime can and report real results. Everything else — including the
   published report doc — is READ-ONLY: flag, never patch. Design-level
   problem → `NEEDS_ARCHITECTURE_PASS`, findings only, NO diff.

RETURN, in order: (1) review_summary YAML + findings (severity / file:line /
issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks annotated with findings + per-change citations,
neutral tone, decision-sufficient substance; (3) verdict + residual-risk note
— state explicitly whether any finding invalidates the published baseline
numbers; (4) real test results or an explicit not-run statement; (5) one-line
read-budget audit; (6) adjudicator tail: your diff, citations, verdict, and
test claims are claims to adjudicate — accept/modify/reject per change; the CA
may veto any change; nothing is kept until that adjudication.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable.
- On return, courier the full output back for review-return adjudication; if a
  kept finding changes the eval's numbers, the CA re-runs the eval and amends
  the report in the same adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
