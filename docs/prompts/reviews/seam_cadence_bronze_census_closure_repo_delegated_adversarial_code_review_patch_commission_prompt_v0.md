# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Seam Cadence / Bronze Census Closure (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the bronze census closure
  bridge unit: the seam cadence runner (the EXECUTABLE completion signal for
  bronze consumption — two cycles over every seam catch-up entrypoint, exit
  nonzero if the second cycle performs work or emits status), its behavioral
  test suite, the cadence coverage contract gate, and the census-closure
  decision record. The special stake is FAKE-PASS EXIT SEMANTICS: this
  executable's exit 0 will be treated as "bronze consumption is closed", so
  any path by which it can exit 0 while work, failure, or a silently skipped
  lane remains is the highest-value finding.
use_when:
  - Dispatching the commissioned seam-cadence review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/bronze-census-closure` (lane head), pinned commit
  `cd863dcc4c96cb3bd0888d2e7c548a3e6418ac4a`.
- Review target (the explicitly named multi-file set; the ONLY patchable
  surface; LF git blob bytes at the pinned commit):
  - `[cadence-runner]` `orca-harness/runners/run_seam_cadence.py` — SHA256 `d9453c177b6451f92417e78dfa5de89427ea69c19e2cec5ad2beef6ee509e568`
  - `[cadence-tests]` `orca-harness/tests/unit/test_seam_cadence.py` — SHA256 `237e37540555a06a9a425fa00c586f238ff2f83d6b91f8507bc7b05feb94a8e3`
  - `[coverage-gate]` `orca-harness/tests/contract/test_seam_cadence_coverage.py` — SHA256 `ec259dac6a3ff5d028e08e35debcd415656c5a0fd5ad9bcad10a2648495b6b2b`
  - `[census-record]` `docs/decisions/bronze_consumer_census_closure_record_v0.md` — SHA256 `5aa1d8ad12e099f38f2174ac9fc1978b01446a770c2d364fdf74dcb4ee68b605`
- Read-only / flag-only everywhere else — notably the seven composed catch-up
  runners (`run_ecr_catchup.py`, `run_{fragrantica,basenotes,parfumo}_cleaning_catchup.py`,
  `run_fragrance_review_projection_catchup.py`,
  `run_ig_reels_grid_projection_catchup.py`, `run_asr_transcript_catchup.py` —
  the cadence composes their public `pending_packets`/`run_catchup`; their
  internals are NOT patchable here), `orca-harness/data_lake/consumption.py`,
  `orca-harness/data_lake/root.py`, the two classified-out LLM extract runners
  (`run_transcript_product_extract.py`, `run_ig_reels_product_extract.py`),
  the sibling gates (`test_catchup_runner_seam_coverage.py`,
  `test_capture_runner_lake_seam_coverage.py`), and the prior adjudication
  conventions (F-ECR-001, F-FRAG-001/002, F-SH-001, F-IGRC-001/002, F-ASR-001
  under `docs/review-outputs/adversarial-artifact-reviews/`).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_seam_cadence.py
  orca-harness/tests/contract/test_seam_cadence_coverage.py
  orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
  orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  (run with `ORCA_DATA_ROOT` unset). Run them if your runtime can; report real
  results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/seam_cadence_bronze_census_closure_delegated_adversarial_code_review_v0.md`
  with `reviewed_by` / `authored_by` / `de_correlation_bar: cross_vendor_discovery`
  / `access: repo` recorded.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"): de-correlated discovery review + delegate-authored bounded patch →
  home-CA adjudication (accept/modify/reject per change, class sweep +
  byte/scope checks, own full-suite run) → keep decision. Repo-mode discovery
  discharges the independent-review gate for the patched set.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; target files + controlling contracts pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/seam_cadence_bronze_census_closure_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/bronze-census-closure; implementation committed at cd863dcc)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by the artifact-folders overlay file and the in-repo commission pattern.
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
- branch: claude/bronze-census-closure, pinned commit cd863dcc4c96cb3bd0888d2e7c548a3e6418ac4a
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [cadence-runner] orca-harness/runners/run_seam_cadence.py
     (SHA256 d9453c177b6451f92417e78dfa5de89427ea69c19e2cec5ad2beef6ee509e568)
  2. [cadence-tests] orca-harness/tests/unit/test_seam_cadence.py
     (SHA256 237e37540555a06a9a425fa00c586f238ff2f83d6b91f8507bc7b05feb94a8e3)
  3. [coverage-gate] orca-harness/tests/contract/test_seam_cadence_coverage.py
     (SHA256 ec259dac6a3ff5d028e08e35debcd415656c5a0fd5ad9bcad10a2648495b6b2b)
  4. [census-record] docs/decisions/bronze_consumer_census_closure_record_v0.md
     (SHA256 5aa1d8ad12e099f38f2174ac9fc1978b01446a770c2d364fdf74dcb4ee68b605)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the bronze census closure bridge unit. Every
bronze-deriving lane is on the consumption seam or classified out; the missing
piece was the COMPLETION SIGNAL as an executable. run_seam_cadence.py
orchestrates the seven seam catch-up entrypoints (ECR;
fragrantica/basenotes/parfumo cleaning; fragrance-review + ig-reels-grid
projections; ASR) through their public pending_packets/run_catchup surfaces:
`--run` executes every entrypoint TWICE and exits nonzero if the SECOND cycle
performs any work or emits any status; `--check` is a compute-free pending
pass; `--skip-asr` skips only ASR execution and must print a visible
skipped_asr_compute marker with the live pending count EVERY cycle. The
runner is deliberately NOT a seam consumer (no data_lake.consumption import,
no acks, no lake writes of its own). The coverage gate pins
CADENCE_ENTRYPOINTS + CLASSIFIED_OUT_SEAM_CONSUMERS (the two owner-gated LLM
extract runners) to the discovered seam-consumer surface. The census record
classifies every derived-record writer into the four census shapes and states
the live dry-run is BLOCKED pending an owner read grant (never simulated).

The failure modes that matter most:
- FAKE-PASS EXIT SEMANTICS (the highest-value class): enumerate every path by
  which `--run` can exit 0 while committed work remains, a failure occurred,
  or a lane went silently unchecked. Examples to attack: exceptions raised
  OUTSIDE an entrypoint call (argparse, DataLakeRoot.resolve, the print/JSON
  layer); a runner whose run_catchup returns [] despite failing; cycle
  accounting that could miss entries; the skip-asr marker accounting
  (healthy marker excluded from cycle-2 accounting BY DESIGN — is the
  boundary between marker and real work airtight?); ordering effects where
  an earlier entrypoint's cycle-2 work is created by a later entrypoint's
  cycle-1 writes (derived-record cascades: does any catch-up lane consume
  another lane's DERIVED output such that two cycles are insufficient?).
- GATE SOUNDNESS (F-SH-001 class): does the coverage gate actually fail on
  each drift case (new seam consumer; registry entry removed; classify-out
  stale; cadence runner itself importing the seam)? Can it be satisfied by
  import-only presence? Is the AST discovery predicate equivalent to the
  sibling gate's, and could a consumer import style evade both?
- CONSUMER-FACING CORRECTNESS (F-IGRC-001 class): the cadence composes seven
  runner surfaces — verify each composition call matches the composed
  runner's real signature and semantics (ASR transcriber policy tokens vs
  its record-id rule; the uniform six's pending/run contracts), and that
  entrypoint_failed isolation cannot swallow or reorder a real status.
- ENVELOPE COMPLETENESS (F-FRAG-001/F-IGRC-002 class): the CadenceContext
  carries model/compute-type into the ASR obligation — can a cadence
  invocation fingerprint work under a policy it did not run (e.g. --skip-asr
  reporting pending under the default policy while the owner's real cadence
  uses another model)?
- CENSUS-RECORD TRUTH ([census-record]): every classification row must match
  the code at the pinned commit (writers, entrypoints, test files,
  classify-out reasons); the record must not overclaim (no bronze-closure,
  validation, readiness, or live-lake claim; the dry-run status must remain
  blocked-pending-grant); carried secondary reports must stay labeled.
- TEST ADEQUACY ([cadence-tests]): do the tests actually pin the exit
  semantics (could a mutant that always returns 0 survive?); monkeypatched
  registry tests vs the real registry; Windows/POSIX portability; leakage of
  ORCA_DATA_ROOT.
- SCOPE DISCIPLINE: the unit is additive-only (no existing file edited) —
  flag anything that SHOULD have required an existing-file change instead of
  patching those files.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
- orca-harness/data_lake/consumption.py (pickup/ack/reconcile semantics; NOT patchable)
- the seven composed catch-up runners (public surfaces; NOT patchable)
- orca-harness/tests/contract/test_catchup_runner_seam_coverage.py (the
  sibling gate whose discovery predicate the coverage gate mirrors; NOT patchable)
- runners/run_{transcript,ig_reels}_product_extract.py (the classified-out
  extract runners; NOT patchable)
- docs/prompts/handoffs/data_lake_silver_vault_lane_handoff_prompt_v0.md (unit (a) spec; resolve on PR #662, branch claude/silver-vault-lane-handoff)
  — if unreadable from your access, say so and judge against the census
  record's own stated contract
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the full exit-code lattice of
   `--run` (every path to 0 and to 1), the cycle-2 accounting boundary
   (entrypoint entries vs cadence-level marker), and the cross-lane
   derived-record cascade question (can cycle 2 legitimately create work for
   cycle 3?).
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding, along the failure modes above. Severity labels are
   finding-priority only.
3. BOUNDED PATCH: smallest complete amendment to the NAMED SET ONLY closing
   your accepted-quality findings; unified diff in chat, each hunk prefixed
   with its label; run the named tests if your runtime can and report real
   results. Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only,
   NO diff.

RETURN, in order: (1) review_summary YAML + findings (label / severity /
file:line / issue / evidence incl. the conflicting source with path / impact /
minimum_closure_condition / next_authorized_action / advisory direction);
(2) unified diff, hunks labeled and annotated with findings + per-change
citations, neutral tone, decision-sufficient substance; (3) verdict +
residual-risk note — state explicitly whether any finding means an exit-0 from
this runner is UNTRUSTWORTHY as the bronze completion signal; (4) real test
results or an explicit not-run statement; (5) one-line read-budget audit;
(6) adjudicator tail: your diff, citations, verdict, and test claims are
claims to adjudicate — accept/modify/reject per change; the CA may veto any
change; nothing is kept until that adjudication, which closes per the
commissioning overlay's Review Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a non-Anthropic lane with the GitHub repo readable (repo mode;
  cross-vendor discovery bar).
- On return, courier the full output back for review-return adjudication; the
  CA adjudicates per labeled change with fresh verification, class sweep,
  byte/scope checks, and its own full-suite run, then lands kept hunks in the
  same adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
