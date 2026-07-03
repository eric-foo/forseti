# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Fragrantica Cleaning Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the Fragrantica Cleaning seam
  catch-up unit (g-reviews/cleaning, fragrantica first): the new catch-up
  runner that gives the Fragrantica Cleaning lane its own work discovery via
  the consumption seam, plus its S-signal test suite. Same
  delegated_code_review_and_patch sibling-mode pattern as the ECR/IG/YT
  commissions; the special stakes are (a) the SHARED-FAMILY SURFACE GATE —
  fragrance_native_database is split across three cleaning lanes by
  source_surface, and this runner acknowledges other lanes' packets with
  out-of-scope evidence, and (b) a policy-only obligation whose
  input-surface claim (projection rebuilt from raw; symbolic ECR ref; no
  committed derived-record inputs) must be verified, not trusted.
use_when:
  - Dispatching the commissioned fragrantica-cleaning catch-up review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/fragrantica-cleaning-seam-catchup` (lane head), pinned commit
  `4134d8bdf3cfa7619f2ac56d4dd17bf92f9e972d`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[frag-runner]` `orca-harness/runners/run_fragrantica_cleaning_catchup.py` — SHA256 `e76254118737efcef7528bd307c3b6b287ba8d06bf76ac7e33d6e5e4ae1a832e`
  - `[frag-tests]` `orca-harness/tests/unit/test_fragrantica_cleaning_catchup.py` — SHA256 `4618c0a29c8d413ac72fca94e0770872f2753484fe899e856f93f8aa8e6b37b8`
- Read-only / flag-only everywhere else — notably `orca-harness/cleaning/fragrantica_lake.py`,
  `orca-harness/cleaning/fragrantica.py`, `orca-harness/cleaning/models.py`,
  `orca-harness/source_capture/fragrantica_projection.py`,
  `orca-harness/data_lake/consumption.py`, `orca-harness/data_lake/lane_registry.py`,
  `orca-harness/runners/run_ecr_catchup.py` (the adjudicated catch-up pattern this
  mirrors), the basenotes/parfumo cleaning modules, the seam-coverage contract
  test, and `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`
  (verified byte-identical in this change — if you believe it should have
  changed, SAY SO).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_fragrantica_cleaning_catchup.py
  orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py
  orca-harness/tests/test_fragrantica_capture_to_silver_e2e.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/fragrantica_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/fragrantica_cleaning_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/fragrantica-cleaning-seam-catchup; implementation committed at 4134d8bd)
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
- branch: claude/fragrantica-cleaning-seam-catchup, pinned commit 4134d8bdf3cfa7619f2ac56d4dd17bf92f9e972d
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [frag-runner] orca-harness/runners/run_fragrantica_cleaning_catchup.py
     (SHA256 e76254118737efcef7528bd307c3b6b287ba8d06bf76ac7e33d6e5e4ae1a832e)
  2. [frag-tests] orca-harness/tests/unit/test_fragrantica_cleaning_catchup.py
     (SHA256 4618c0a29c8d413ac72fca94e0770872f2753484fe899e856f93f8aa8e6b37b8)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the seam catch-up entrypoint for the Fragrantica Cleaning
lane — until this change, the audit pack + post-cleaned Silver records were
derived only when an operator pointed a command at ONE packet; the lane had
no discovery. The runner scans committed fragrance_native_database
availability via the consumption seam (ack namespace
cleaning_fragrantica_audit, consumer "fragrantica_cleaning_catchup"),
SURFACE-GATES the shared family (fragrantica derives; basenotes/parfumo
surfaces are acknowledged with explicit no_cleanable_content_for_surface
evidence and never derived), and acknowledges each derivation with the audit
pack + Silver record ids as evidence. The obligation envelope is POLICY-ONLY
(five pre-existing constants), resting on the claim that the derivation has
no growable derived-record inputs: raw is immutable, the projection is
rebuilt in memory from raw bodies, and the cleaning packet's ECR ref is
symbolic-by-convention. Skip-if-done keys on the ACK; this lane writes no
record-set completion marker (audit + Silver are independent appends with
fresh ULIDs), so a crash mid-derivation leaves unreferenced siblings and no
ack, and the packet re-derives fresh on the next run.

The failure modes that matter most: a WRONG INPUT-SURFACE CLAIM (does the
derivation actually consume any committed derived record — projection, ECR,
anything — that could grow after an ack? is any policy constant that changes
output shape MISSING from the envelope, e.g. a token inside
build_fragrantica_projection or the transform rules?); SURFACE-GATE HONESTY
(is acking another lane's packet under this lane's namespace with
out-of-scope evidence sound and non-interfering? what happens for a NEW
future surface in the family — is acking it out-of-scope safe, or does that
silently pre-close a future lane's... note the ack namespace is
fragrantica's own, so other lanes are unaffected — challenge that reasoning);
ACK HONESTY (can any path ack a packet whose derivation did not complete?
partial audit-without-silvers crash states; is the evidence dereferenceable?);
IDEMPOTENCE (byte-unchanged second run given the availability rebuild and
ULID-fresh record ids); and TEST ADEQUACY (could a regressed runner pass —
e.g. an ack on derive failure, a surface gate that derives anyway, a policy
bump that does not re-derive?).

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
  (minimum obligation envelope incl. the "every input class whose growth must
  re-surface the anchor MUST appear in the snapshot" rule; ack/evidence shape)
- orca-harness/data_lake/consumption.py (the seam helper; obligation_fn is
  called inline in pickup with NO per-item isolation)
- orca-harness/cleaning/fragrantica_lake.py + orca-harness/cleaning/fragrantica.py
  + orca-harness/source_capture/fragrantica_projection.py +
  orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py (the derivation
  this runner drives — VERIFY the no-derived-inputs and symbolic-ECR-ref
  claims against these sources)
- orca-harness/cleaning/basenotes.py + orca-harness/cleaning/parfumo.py (the
  shared-family surfaces the gate must exclude; NOT patchable)
- orca-harness/runners/run_ecr_catchup.py and
  docs/review-outputs/adversarial-artifact-reviews/ecr_seam_catchup_delegated_adversarial_code_review_v0.md
  (the adjudicated catch-up pattern incl. the F-ECR-001 per-packet reconcile
  this runner mirrors; divergences need a reason; NOT patchable)
- orca-harness/data_lake/lane_registry.py (cleaning_fragrantica_audit
  registration; NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the fragrantica cleaning
   derivation's true input surface from its sources (what do the projection
   builder and cleaning-packet builder actually read?), then the ways a
   policy-only obligation, an ack-keyed skip, a surface gate over a shared
   family, or the catch-up loop could fake done-ness, lose failure
   visibility, or violate the seam contract.
2. MAXIMALLY ADVERSARIAL code review of the named set, labels on every
   finding, covering at minimum: input-surface completeness; policy-token
   completeness (is every output-shaping constant in the envelope?);
   surface-gate honesty incl. the future-new-surface case; ack honesty and
   evidence sufficiency (partial-derivation crash states, silver_records
   evidence dereferenceability); idempotence and byte-unchanged reruns;
   per-packet isolation and typed failures; reconcile fidelity to the
   F-ECR-001 adjudicated shape; namespace/boundary discipline; CLI exit
   semantics (note acked_no_cleanable_content counts as success); test
   adequacy (could the pre-runner state or a regressed runner pass?); scope
   discipline. Severity labels are finding-priority only.
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
residual-risk note — state explicitly whether any finding means acks this
runner would write are untrustworthy, and whether the out-of-scope-surface
acks are sound; (4) real test results or an explicit not-run statement;
(5) one-line read-budget audit; (6) adjudicator tail: your diff, citations,
verdict, and test claims are claims to adjudicate — accept/modify/reject per
change; the CA may veto any change; nothing is kept until that adjudication,
which closes per the commissioning overlay's Review Adjudication Next Step.

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
