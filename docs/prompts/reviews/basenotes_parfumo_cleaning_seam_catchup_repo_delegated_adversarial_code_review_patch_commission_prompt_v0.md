# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Basenotes + Parfumo Cleaning Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the basenotes + parfumo
  Cleaning seam catch-up units (g-reviews/cleaning, closing the cleaning
  family): two new catch-up runners mirroring the ADJUDICATED fragrantica
  catch-up (F-FRAG-001/002 closed), plus their S-signal test suites. The
  special stakes are MIRROR FIDELITY against a twice-reviewed pattern
  (divergences need a lane-specific reason) and PER-LANE ENVELOPE
  COMPLETENESS (each lane's output-shaping constants differ — basenotes has
  no metric records; parfumo has two in-scope surfaces and a rating carry
  rule).
use_when:
  - Dispatching the commissioned basenotes/parfumo catch-up review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/basenotes-parfumo-cleaning-seam-catchup` (lane head), pinned commit
  `2fb9513b8b6d201da665f87ea7fcf1039437a4ef`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[bn-runner]` `orca-harness/runners/run_basenotes_cleaning_catchup.py` — SHA256 `657fc7e7819bddc41e3f81cbe7da63ad8d8ded9bfc4e501899730d8179806200`
  - `[bn-tests]` `orca-harness/tests/unit/test_basenotes_cleaning_catchup.py` — SHA256 `9adbf28b97001a4402e88e3ad7724a2e48f0232ad705460ddfe59f3732fd530b`
  - `[pf-runner]` `orca-harness/runners/run_parfumo_cleaning_catchup.py` — SHA256 `33d5eb6c6c99ecb0d423a48aedc34e51e5ba684584472c4d4f731e0812871250`
  - `[pf-tests]` `orca-harness/tests/unit/test_parfumo_cleaning_catchup.py` — SHA256 `2161aaa7452c7e80f79ed9c878a1f86370e937191eca0ef82a2f4e7f0b985e5e`
- Read-only / flag-only everywhere else — notably
  `orca-harness/runners/run_fragrantica_cleaning_catchup.py` (the twice-reviewed
  pattern these mirror) and
  `docs/review-outputs/adversarial-artifact-reviews/fragrantica_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md`
  (the adjudication whose F-FRAG-001/002 conventions these must inherit),
  `orca-harness/cleaning/{basenotes,parfumo}_lake.py`,
  `orca-harness/cleaning/{basenotes,parfumo}.py`,
  `orca-harness/source_capture/{basenotes,parfumo}_projection.py`,
  `orca-harness/runners/run_parfumo_mgt_capture.py`,
  `orca-harness/data_lake/consumption.py`, `orca-harness/data_lake/lane_registry.py`,
  the seam-coverage contract test, and
  `orca-harness/data_lake/lake_touchpoint_inventory_v0.json` (verified
  byte-identical in this change — if you believe it should have changed, SAY SO).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_basenotes_cleaning_catchup.py
  orca-harness/tests/unit/test_parfumo_cleaning_catchup.py
  orca-harness/tests/test_basenotes_native_pipeline_lake.py
  orca-harness/tests/test_parfumo_native_pipeline_lake.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/basenotes_parfumo_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/basenotes_parfumo_cleaning_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/basenotes-parfumo-cleaning-seam-catchup; implementation committed at 2fb9513b)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by artifact-folders overlay file and the in-repo commission pattern.
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
- branch: claude/basenotes-parfumo-cleaning-seam-catchup, pinned commit 2fb9513b8b6d201da665f87ea7fcf1039437a4ef
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [bn-runner] orca-harness/runners/run_basenotes_cleaning_catchup.py
     (SHA256 657fc7e7819bddc41e3f81cbe7da63ad8d8ded9bfc4e501899730d8179806200)
  2. [bn-tests] orca-harness/tests/unit/test_basenotes_cleaning_catchup.py
     (SHA256 9adbf28b97001a4402e88e3ad7724a2e48f0232ad705460ddfe59f3732fd530b)
  3. [pf-runner] orca-harness/runners/run_parfumo_cleaning_catchup.py
     (SHA256 33d5eb6c6c99ecb0d423a48aedc34e51e5ba684584472c4d4f731e0812871250)
  4. [pf-tests] orca-harness/tests/unit/test_parfumo_cleaning_catchup.py
     (SHA256 2161aaa7452c7e80f79ed9c878a1f86370e937191eca0ef82a2f4e7f0b985e5e)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the final two Cleaning seam catch-up entrypoints —
basenotes (ack namespace cleaning_basenotes_audit, consumer
"basenotes_cleaning_catchup", ONE in-scope surface) and parfumo (ack
namespace cleaning_parfumo_audit, consumer "parfumo_cleaning_catchup", TWO
in-scope surfaces: direct HTTP + chrome-extension targeted rendered). Both
mirror the TWICE-REVIEWED fragrantica catch-up whose adjudication
(F-FRAG-001: enumerate every output-shaping constant into the policy-only
envelope; F-FRAG-002: allowlist known other-lane surfaces with explicit
out-of-scope ack evidence, leave unknown surfaces visible and UNACKED as
unsupported_surface) these units inherit by construction. Obligations are
policy-only on the same verified premises (immutable raw, in-memory
projection rebuild, symbolic ECR ref).

The failure modes that matter most: PER-LANE ENVELOPE COMPLETENESS (each
lane's constants differ — did the basenotes envelope miss anything its
audit/silver outputs embed? did parfumo miss a constant tied to its second
surface, its statement rows, or its rating carry path? is any constant in
the envelope NOT actually output-shaping — harmless churn but sloppiness);
MIRROR INFIDELITY (any divergence from the adjudicated fragrantica shape
that re-opens a closed class — check the surface allowlists are mutually
consistent across the three cleaning runners: each lane's in-scope surfaces
are exactly the other lanes' known-out-of-scope entries, no gaps, no
overlap); SURFACE-GATE CORRECTNESS for parfumo's TWO surfaces (does the
rendered-surface path derive correctly — the lake adapter passes
packet.source_surface through; can a rendered packet whose artifact shape
differs from the direct-HTTP shape fake-pass the tests?); ACK HONESTY,
IDEMPOTENCE, and TEST ADEQUACY as before.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
- orca-harness/data_lake/consumption.py
- orca-harness/runners/run_fragrantica_cleaning_catchup.py AND
  docs/review-outputs/adversarial-artifact-reviews/fragrantica_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md
  (the adjudicated pattern + the conventions these units must inherit; NOT patchable)
- orca-harness/cleaning/basenotes_lake.py + orca-harness/cleaning/basenotes.py +
  orca-harness/source_capture/basenotes_projection.py (basenotes derivation —
  VERIFY the envelope enumerates everything its outputs embed)
- orca-harness/cleaning/parfumo_lake.py + orca-harness/cleaning/parfumo.py +
  orca-harness/source_capture/parfumo_projection.py +
  orca-harness/runners/run_parfumo_mgt_capture.py (parfumo derivation incl.
  the two-surface split and the targeted-capture packet shape)
- orca-harness/data_lake/lane_registry.py (lane registrations; NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: per lane, enumerate the derivation's true
   input surface and every output-shaping constant from its sources; then the
   ways a mirrored catch-up could diverge, under-enumerate, mis-gate a
   surface, fake done-ness, or lose failure visibility.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding: per-lane envelope completeness (against the actual audit/silver
   payload builders, not the runner's own claims); cross-runner surface
   allowlist consistency (fragrantica/basenotes/parfumo: in-scope vs
   known-out-of-scope must partition the family's surfaces exactly);
   parfumo two-surface correctness incl. the rendered-capture packet shape;
   ack honesty and evidence dereferenceability; idempotence and
   byte-unchanged reruns; per-packet isolation and typed failures; reconcile
   fidelity to the F-ECR-001 shape; CLI exit semantics; test adequacy (could
   a regressed runner pass?); scope discipline. Severity labels are
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
residual-risk note — state explicitly whether any finding means acks these
runners would write are untrustworthy; (4) real test results or an explicit
not-run statement; (5) one-line read-budget audit; (6) adjudicator tail: your
diff, citations, verdict, and test claims are claims to adjudicate —
accept/modify/reject per change; the CA may veto any change; nothing is kept
until that adjudication, which closes per the commissioning overlay's Review
Adjudication Next Step.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a GPT-family (non-Anthropic) lane with the GitHub repo readable.
- On return, courier the full output back for review-return adjudication; the
  CA adjudicates per labeled change and lands kept hunks in the same
  adjudication landing.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
