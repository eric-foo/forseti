# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Fragrance-Review Projection Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the fragrance-review projection
  seam catch-up unit — the FIRST projection-family lane on the consumption
  seam (its conventions template the remaining shape-2 projections): a new
  catch-up runner, its S-signal test suite, and two upstream enablers (named
  selection-policy constants; a capture-date as-of resolver). The special
  stakes are DETERMINISM COMPLETENESS (the lane pins a date-relative selection
  policy to the packet's capture date — is that pin sufficient and honest?)
  and the ENVELOPE BOUNDARY (which coverage-builder constants are enumerated
  policy vs covered by the version token — challenge the line drawn).
use_when:
  - Dispatching the commissioned fragrance-review projection catch-up review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/fragrance-review-projection-seam-catchup` (lane head), pinned commit
  `bcc2c863c9dee55b1e60e9bbc9484f1432915308`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[coverage]` `orca-harness/source_capture/fragrance_review_coverage.py` — SHA256 `d50f706f5f231e4fbe81b47bb2f2c11b89d49b6b5669a82d8f73599e3fe75f88`
  - `[lake]` `orca-harness/source_capture/fragrance_review_lake.py` — SHA256 `f5eeaf437d3e71cab942315228391a238fce923bdae4a935018f6d97508ac089`
  - `[runner]` `orca-harness/runners/run_fragrance_review_projection_catchup.py` — SHA256 `58a49c58be25d04b9ee9269eb904a5d0a50aabe633af5054871638adaf1e473a`
  - `[tests]` `orca-harness/tests/unit/test_fragrance_review_projection_catchup.py` — SHA256 `40454da67b9f3c9916c170e49a34e26d38ba64809c6e39e1b380a0e1eb478af1`
- Read-only / flag-only everywhere else — notably
  `orca-harness/runners/run_fragrantica_cleaning_catchup.py` (the adjudicated
  catch-up pattern this mirrors) and
  `docs/review-outputs/adversarial-artifact-reviews/fragrantica_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md`
  plus
  `docs/review-outputs/adversarial-artifact-reviews/basenotes_parfumo_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md`
  (the adjudications whose F-ECR-001 / F-FRAG-001 / F-FRAG-002 conventions this
  unit must inherit), `orca-harness/data_lake/consumption.py`,
  `orca-harness/data_lake/root.py` (availability entry shape + verified reads),
  `orca-harness/data_lake/lane_registry.py`,
  `orca-harness/source_capture/writer.py` +
  `orca-harness/source_capture/packet_assembly.py` (manifest shape incl. slice
  timing), `orca-harness/source_capture/fragrance_rendered_widget_companion.py`,
  `orca-harness/tests/test_fragrance_review_lake_pilot.py`,
  `orca-harness/tests/contract/test_fragrance_review_claim_ceiling_contract.py`,
  the seam-coverage contract test, and
  `orca-harness/data_lake/lake_touchpoint_inventory_v0.json` (unchanged in this
  change — if you believe it should have changed, SAY SO).
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_fragrance_review_projection_catchup.py
  orca-harness/tests/test_fragrance_review_lake_pilot.py
  orca-harness/tests/unit/test_fragrance_review_coverage.py
  orca-harness/tests/contract/test_fragrance_review_claim_ceiling_contract.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the seam-coverage and inventory gate suites. Run them if your runtime
  can; report real results either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/fragrance_review_projection_seam_catchup_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/fragrance_review_projection_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/fragrance-review-projection-seam-catchup; implementation committed at bcc2c863)
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
- branch: claude/fragrance-review-projection-seam-catchup, pinned commit bcc2c863c9dee55b1e60e9bbc9484f1432915308
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [coverage] orca-harness/source_capture/fragrance_review_coverage.py
     (SHA256 d50f706f5f231e4fbe81b47bb2f2c11b89d49b6b5669a82d8f73599e3fe75f88)
  2. [lake] orca-harness/source_capture/fragrance_review_lake.py
     (SHA256 f5eeaf437d3e71cab942315228391a238fce923bdae4a935018f6d97508ac089)
  3. [runner] orca-harness/runners/run_fragrance_review_projection_catchup.py
     (SHA256 58a49c58be25d04b9ee9269eb904a5d0a50aabe633af5054871638adaf1e473a)
  4. [tests] orca-harness/tests/unit/test_fragrance_review_projection_catchup.py
     (SHA256 40454da67b9f3c9916c170e49a34e26d38ba64809c6e39e1b380a0e1eb478af1)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the FIRST projection-family consumption-seam catch-up —
the fragrance-review coverage projection (ack namespace
projection_fragrance_review, consumer "fragrance_review_projection_catchup",
family fragrance_review, ONE in-scope surface: rendered_widget_review). It
mirrors the thrice-reviewed cleaning catch-up shape (policy-only envelope;
skip-if-done on the ACK; F-ECR-001 per-packet fail-visible reconcile;
F-FRAG-002 no-open-world-ack surface gate) and its conventions become the
template for the remaining projection lanes (retail_pdp, ig_reels_grid, the
site projections). Two upstream enablers are part of the target: [coverage]
names the selection-policy literals so the envelope can import rather than
duplicate them (F-FRAG-001), and [lake] adds capture_as_of_date(manifest)
because the coverage builder's selection is recency-windowed and defaults
as_of_date to date.today() — the runner pins it to the packet's own capture
date so derived bytes are a pure function of (immutable raw, policy). The tee
half (write_fragrance_review_capture_packet) is a capture-time producer,
deliberately NOT on the seam.

The failure modes that matter most:
- DETERMINISM COMPLETENESS: is the capture-date pin SUFFICIENT — is any other
  input to build_fragrance_review_coverage run-date- or environment-dependent
  (today() paths, ordering, locale, float formatting)? Is the pin HONEST —
  manifest read hash-verified against the availability entry, single-slice
  rule, loud failure instead of a today() fallback? Could a packet derive
  under one date and ack under another?
- ENVELOPE BOUNDARY (challenge the line): the envelope enumerates coverage
  method/version/certification, the three named selection constants,
  max_selected_rows: None, and the as_of_policy token. Internal builder tables
  (_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES, _VOID_HTML_TAGS, parsing behavior)
  ride the coverage_version token with comment-bound bump discipline — the
  same line the adjudicated fragrantica envelope drew for its projection
  internals. Is anything on the wrong side of that line for THIS lane (a
  constant that is really selection policy but not enumerated, or an
  enumerated constant that is not actually output-shaping)?
- SINGLE-SURFACE GATE CORRECTNESS: with no sibling lane owning other family
  surfaces there is deliberately NO out-of-scope ack branch — every
  non-in-scope surface is a visible, UNACKED unsupported_surface. Is that the
  right F-FRAG-002 instantiation, and does anything else write
  fragrance_review family packets under a different surface?
- UPSTREAM REFACTOR SAFETY: is the [coverage] constants extraction
  byte-behavior-identical (incl. the long_form hoist)? does [lake] leave the
  operator-pointed projection path unchanged?
- ACK HONESTY (evidence dereferenceability: read-back sha256, resolved as_of,
  row counts), IDEMPOTENCE (byte-unchanged reruns, fresh-sibling semantics),
  PER-PACKET ISOLATION and typed failures, RECONCILE FIDELITY to the
  F-ECR-001 shape, CLI exit semantics, TEST ADEQUACY (could a regressed
  runner pass? could the determinism test pass while a today() path
  survives?), SCOPE DISCIPLINE.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
- orca-harness/data_lake/consumption.py
- orca-harness/runners/run_fragrantica_cleaning_catchup.py AND
  docs/review-outputs/adversarial-artifact-reviews/fragrantica_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md
  AND docs/review-outputs/adversarial-artifact-reviews/basenotes_parfumo_cleaning_seam_catchup_delegated_adversarial_code_review_v0.md
  (the adjudicated pattern + inherited conventions; NOT patchable)
- orca-harness/data_lake/root.py (availability entry derivation,
  record_availability, load_raw_packet verified read)
- orca-harness/source_capture/writer.py + orca-harness/source_capture/packet_assembly.py
  (manifest shape: source_slices[].timing.capture_time as a VisibleFact)
- orca-harness/source_capture/fragrance_rendered_widget_companion.py (the
  witness fields and review response kinds the tee preserves)
- orca-harness/tests/test_fragrance_review_lake_pilot.py +
  orca-harness/tests/contract/test_fragrance_review_claim_ceiling_contract.py
  (the pilot's claim ceiling this unit must not exceed)
- orca-harness/data_lake/lane_registry.py (lane registrations; NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the projection's true input
   surface (raw bodies, manifest fields, policy constants, dates) and every
   output-shaping constant from its sources; then the ways a catch-up could
   under-pin determinism, under- or over-enumerate the envelope, mis-gate a
   surface, fake done-ness, or lose failure visibility.
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
residual-risk note — state explicitly whether any finding means acks this
runner would write are untrustworthy; (4) real test results or an explicit
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
