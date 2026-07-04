# Repo-Mode Delegated Adversarial Code Review + Patch Commission — IG Reels-Grid Projection Seam Catch-Up (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the IG reels-grid projection
  seam catch-up unit: the catch-up runner for the one projection lane with a
  real committed-record consumer (the creator-profile spine), its test suite,
  the F-SH-001 runtime reconcile-surfacing rider tests for the YT/IG extract
  runners, and the two gate-membership updates. The special stakes are
  THREE-ENTRYPOINT COHERENCE (operator-pointed, Bronze-catalog proof path,
  and now the seam runner all write the same lane — can they double-claim,
  collide, or diverge?) and CONSUMER-FACING CORRECTNESS (the downstream
  creator-metric seed walks this lane's records — could a catch-up-derived
  record differ from what the consumer expects?).
use_when:
  - Dispatching the commissioned ig-reels-grid catch-up review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/ig-reels-grid-projection-seam-catchup` (lane head), pinned commit
  `393cc21e738bb69fe3f5d1e9876ac09bdf86f78c`.
- Review target (the explicitly named multi-file set; the ONLY patchable surface;
  LF git blob bytes at the pinned commit):
  - `[runner]` `orca-harness/runners/run_ig_reels_grid_projection_catchup.py` — SHA256 `376ecf3d832d09c0120bdf4f3a9a113823dcc671f987e7bb7a0a30f39aca0a9b`
  - `[tests]` `orca-harness/tests/unit/test_ig_reels_grid_projection_catchup.py` — SHA256 `f365224ad6572c6e87c6e5dd8aa12563257a6ce1bd1a4a36e30bab268c381d74`
  - `[rider]` `orca-harness/tests/unit/test_extract_runner_reconcile_surfacing.py` — SHA256 `4b986b3495ab924cb6cc24e1875d37bd00fce72cd264ca0e582e7714b22a1473`
  - `[gate-consumer]` `orca-harness/tests/contract/test_catchup_runner_seam_coverage.py` — SHA256 `fd43ec4ba69f823dd2574f2a3b114637ab55e673227dc4eeb3ddc4462aed598b`
  - `[gate-pins]` `orca-harness/tests/contract/test_policy_module_version_pins.py` — SHA256 `87f180da2ada764eabc0fd8c9af1e7fc9e7004caf20e841a149d1e4d8c8a80aa`
- Read-only / flag-only everywhere else — notably
  `orca-harness/source_capture/ig_reels_grid_projection.py` (the deriver, the
  Bronze-catalog proof path, and the policy constants the envelope imports),
  `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py`
  (the downstream consumer that walks this lane's committed records),
  `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py` (the
  capture writer whose surface/policy the gate mirrors),
  `orca-harness/runners/run_{transcript,ig_reels}_product_extract.py` (the
  rider's subjects; NOT patchable here),
  `orca-harness/data_lake/consumption.py`, the fragrance-review catch-up
  runner + its adjudication (the template), the seam-hardening adjudication
  (F-SH-001), and `orca-harness/data_lake/lane_registry.py`.
- Access mode: `repo` — inspect the pinned source in place; no substitute
  source, summary, or re-created copy.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, PRs, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/unit/test_ig_reels_grid_projection_catchup.py
  orca-harness/tests/unit/test_extract_runner_reconcile_surfacing.py
  orca-harness/tests/unit/test_source_capture_ig_reels_projection.py
  orca-harness/tests/unit/test_ig_reels_product_extract.py
  orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
  orca-harness/tests/contract/test_policy_module_version_pins.py
  orca-harness/tests/contract/test_cleaning_family_surface_partition.py
  orca-harness/tests/test_data_lake_consumption.py`
  plus the producer seam-coverage and inventory gate suites. Run them if your
  runtime can; report real results either way — never assert a pass that was
  not run.
- Output mode: `paste-ready-chat` (body below). Return: chat findings + diff.
  Durable report written by the home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/ig_reels_grid_projection_seam_catchup_delegated_adversarial_code_review_v0.md`
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
  target_scope: docs/prompts/reviews/ig_reels_grid_projection_seam_catchup_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/ig-reels-grid-projection-seam-catchup; implementation committed at 393cc21e)
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
- branch: claude/ig-reels-grid-projection-seam-catchup, pinned commit 393cc21e738bb69fe3f5d1e9876ac09bdf86f78c
- REVIEW TARGET (the named multi-file set you review AND may patch — nothing
  else; every finding, diff hunk, and citation must carry the target's label):
  1. [runner] orca-harness/runners/run_ig_reels_grid_projection_catchup.py
     (SHA256 376ecf3d832d09c0120bdf4f3a9a113823dcc671f987e7bb7a0a30f39aca0a9b)
  2. [tests] orca-harness/tests/unit/test_ig_reels_grid_projection_catchup.py
     (SHA256 f365224ad6572c6e87c6e5dd8aa12563257a6ce1bd1a4a36e30bab268c381d74)
  3. [rider] orca-harness/tests/unit/test_extract_runner_reconcile_surfacing.py
     (SHA256 4b986b3495ab924cb6cc24e1875d37bd00fce72cd264ca0e582e7714b22a1473)
  4. [gate-consumer] orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
     (SHA256 fd43ec4ba69f823dd2574f2a3b114637ab55e673227dc4eeb3ddc4462aed598b)
  5. [gate-pins] orca-harness/tests/contract/test_policy_module_version_pins.py
     (SHA256 87f180da2ada764eabc0fd8c9af1e7fc9e7004caf20e841a149d1e4d8c8a80aa)
  (LF git blob bytes; confirm the hashes if you can, else confirm you read the
  files at the pinned commit and say so.)
If you cannot open the repository at all, reply ONLY `BLOCKED_REPO_UNREADABLE`.
If you can open the repo but not the pinned commit, review the branch head and
state the commit you actually read.

WHAT THE TARGET IS: the first projection-family catch-up for a lane with a
REAL committed-record consumer — the creator-profile spine's
instagram_metric_seed walks derived/<pkt>/projection_ig_reels_grid/ to build
creator metric seeds, so a grid packet without its projection record is
invisible to creator metrics. The lane already had two non-seam entrypoints:
the operator-pointed project_ig_reels_grid_into_lake (no discovery; fresh
ULID sibling ids) and the Bronze-catalog proof path
project_ig_reels_grid_from_bronze_catalog (catalog discovery; STABLE record
ids keyed on packet+AR identity; skip-if-done on record existence). The new
[runner] adds the seam entrypoint (ack namespace projection_ig_reels_grid,
consumer ig_reels_grid_projection_catchup, policy-only envelope, shared
per-packet reconcile, cleaning-style out-of-scope acks for
ig_reels_audio/ig_reels_deep_capture_render_audio/ig_calls_browser_snapshot,
unsupported_surface for unknowns). [rider] discharges the F-SH-001
adjudication residual (runtime proof of YT/IG reconcile-failure surfacing).
[gate-consumer]/[gate-pins] carry the membership updates.

The failure modes that matter most:
- THREE-ENTRYPOINT COHERENCE: the catalog path writes stable-id records and
  fails closed on existing ids; the seam path writes fresh ULID siblings and
  keys done-ness on the ACK. Can running both produce a state that breaks
  either (catalog path failing closed because of seam-written records? the
  consumer double-counting rows because two records exist for one packet)?
  Read instagram_metric_seed's walk: how does it treat MULTIPLE records under
  one packet's lane dir — and does the ack-keyed re-derive-on-policy-bump
  behavior (two siblings) change what the consumer computes?
- CONSUMER-FACING CORRECTNESS: does a catch-up-derived record differ in ANY
  byte-shape from operator/catalog-derived ones (same _projection_json_text
  path — verify)? Could the consumer's _source_packet_pointer or row parsing
  break on catch-up-written records?
- ENVELOPE COMPLETENESS (F-FRAG-001): the envelope enumerates
  method/version/certification, the surface-preference map, both metric-key
  maps, the capture-file basename, and the static-view rule. Is anything
  output-shaping missing (e.g. the compact-count parser in _int_or_none, the
  shortcode join rules, ig_projection's shared forbidden-name guard) that
  should instead be enumerated or ride IG_REELS_PROJECTION_VERSION (now
  pinned in [gate-pins])? Anything enumerated that is not output-shaping?
- SURFACE GATE: is {ig_reels_audio, ig_reels_deep_capture_render_audio,
  ig_calls_browser_snapshot} the complete set of KNOWN other-lane
  instagram_creator surfaces (sweep the writers), and is acking them
  out-of-scope in THIS lane's namespace honest (they remain available to
  their own lanes)?
- RIDER ADEQUACY: do the four runtime tests actually pin the F-SH-001
  channels (poisoned transport proving no extraction), or could a regressed
  swallow still pass them?
- ACK HONESTY, IDEMPOTENCE, PER-PACKET ISOLATION, RECONCILE FIDELITY, CLI
  exit semantics, TEST ADEQUACY (could a regressed runner pass?), SCOPE
  DISCIPLINE.

CONTRACTS AND SOURCES the code must be judged against — read in the pinned repo
(record a one-line read disposition per source: full / targeted <section> /
grep <token> / skip: <reason>):
- orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md
- orca-harness/data_lake/consumption.py (incl. reconcile_availability_per_packet)
- orca-harness/source_capture/ig_reels_grid_projection.py (deriver + catalog
  path + policy constants; NOT patchable)
- orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py
  (the downstream consumer; NOT patchable)
- orca-harness/runners/run_source_capture_ig_reels_grid_packet.py +
  orca-harness/source_capture/transcript/ig_reels_audio_packet.py +
  orca-harness/runners/run_source_capture_ig_calls_packet.py (family surface
  writers — verify the out-of-scope set is complete)
- orca-harness/runners/run_fragrance_review_projection_catchup.py AND
  docs/review-outputs/adversarial-artifact-reviews/fragrance_review_projection_seam_catchup_delegated_adversarial_code_review_v0.md
  AND docs/review-outputs/adversarial-artifact-reviews/seam_hardening_doctrine_to_code_delegated_adversarial_code_review_v0.md
  (the template + the F-SH-001 convention; NOT patchable)
- orca-harness/data_lake/lane_registry.py (NOT patchable)
- AGENTS.md (root): Smallest Complete Intervention + failure-visibility kernel.

TASK (order matters):
1. Structured reasoning pass FIRST: enumerate the projection's true input
   surface and every output-shaping constant from its sources; map all three
   entrypoints' record-id/done-ness semantics and the consumer's read
   behavior; then the ways the catch-up could double-claim, under-enumerate,
   mis-gate a surface, fake done-ness, or lose failure visibility.
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
runner would write are untrustworthy OR the downstream creator-metric seed
could compute wrong values from catch-up-written records; (4) real test
results or an explicit not-run statement; (5) one-line read-budget audit;
(6) adjudicator tail: your diff, citations, verdict, and test claims are
claims to adjudicate — accept/modify/reject per change; the CA may veto any
change; nothing is kept until that adjudication, which closes per the
commissioning overlay's Review Adjudication Next Step.

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
