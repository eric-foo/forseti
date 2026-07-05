# Capture Source-Family Lane Catalog PR #722 Adversarial Artifact Review

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  De-correlated adversarial artifact review of PR #722 (capture source-family
  lane catalog): whether the catalog makes every landed capture-to-lake lane
  cold-discoverable from the Source Capture Playbook/toolbox while preserving
  the owner-ratified three-way authority split (playbook = access method;
  source_families/ = routing home; Data Lake authority = admission/storage/
  Silver).
use_when:
  - Adjudicating PR #722 before merge/ready-for-review.
  - Checking whether the source-family catalog's "home every landed family"
    anchor_goal was actually discharged.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md
  - docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md
branch_or_commit: >
  PR #722, branch codex/capture-playbook-lake-sync. Review target is the
  catalog diff at commit d9cb8d14fafe1b4363de3adef5ca321b84c73683 against base
  e8ca2093ce7fad5d3d8b96b030c874f81655824a. At review time the branch head had
  advanced to e4b3e29ff1d74bb58646d4bd6e7311ec9bca9b05, which adds only the
  review-commission prompt itself (confirmed by `git diff --name-status
  d9cb8d14..HEAD`) and does not touch the reviewed catalog target.
stale_if:
  - PR #722 target commit changes from d9cb8d14 without this report being re-run.
  - source_families/ or the toolbox/playbook are restructured after d9cb8d14.
```

## Commission

- Commissioned by: `docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md`.
- Review purpose: decide whether PR #722 gives future capture lanes a
  cold-discoverable, source-specific route from the playbook/toolbox to every
  landed capture-to-lake family index, while preserving the ratified authority
  split.
- Type: read-only de-correlated adversarial artifact review. **Not** a
  delegated review-and-patch commission (`delegated-review-patch.md`'s "when it
  applies" gate — no CA-named bounded patch target/scope was given). No patch
  execution, no `patch_queue_entry`.
- `de_correlation_bar: self_fallback`.
- `same_vendor_rationale`: not applicable (self_fallback, not same_vendor_sanity).

```yaml
reviewed_by: unrecorded
authored_by: unrecorded
```

`reviewed_by` is `unrecorded` because operator/tooling has not supplied the
reviewing model+version for this record. `authored_by` is `unrecorded` because
the commissioning prompt names the PR's author only as "OpenAI / GPT-family
Codex thread, exact runtime version unrecorded"; this record does not
fabricate a version. Per review-lanes.md, a present `unrecorded` value is a
visible measurement gap, not a captured measurement.

**Non-claim on de-correlation:** this review ran as the same agent/session that
loaded the commission prompt and is not a controller-selected cross-vendor or
same-vendor delegate under `delegated-review-patch.md`'s vendor-lineage
definition. It does not satisfy `cross_vendor_discovery` or
`same_vendor_sanity`; it is a self-fallback pass and must not be represented as
independent discovery review.

## Preflight / Freshness Receipt

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (capture_source_family_lane_catalog_pr722_review_pack, per commission)
  edit_permission: read-only
  target_scope: PR #722 source-family lane catalog target at commit d9cb8d14
  dirty_state_checked: yes
  blocked_if_missing: none — repo access available, target resolves
```

- Workspace: `C:/Users/vmon7/Desktop/projects/orca/worktrees/capture-playbook-lake-sync-codex`.
- Branch: `codex/capture-playbook-lake-sync`. Observed head at review time:
  `e4b3e29f` (`git status --short --branch` showed clean working tree, tracking
  `origin/codex/capture-playbook-lake-sync`).
- PR metadata (`gh pr view 722 --repo eric-foo/orca ...`, re-fetched at review
  time): `state: OPEN`, `isDraft: true`, `headRefOid: e4b3e29f...`,
  `baseRefOid: e8ca2093...` (== `main` tip), `statusCheckRollup`:
  `orca-harness-tests` / `ci` — `COMPLETED` / `SUCCESS`.
- Target-vs-head diff: `git diff --name-status d9cb8d14..HEAD` shows exactly
  one file added — the review-commission prompt itself
  (`docs/prompts/reviews/capture_source_family_lane_catalog_pr722_adversarial_artifact_review_prompt_v0.md`).
  No review-scope contamination (see AR-defended-05).
- Controlling overlay sources (AGENTS.md, `.agents/workflow-overlay/*`) were
  read at their current worktree state: clean, matching the session-start
  capsule's "matches last-fetched origin/main" note.

## Source-Read Ledger

| Source | Why read | Section/evidence used | Status |
| --- | --- | --- | --- |
| `AGENTS.md` | Method/authority reference-load | Kernel + Forseti Project Instructions | clean |
| `.agents/workflow-overlay/README.md`, `source-of-truth.md`, `source-loading.md`, `delegated-review-patch.md`, `review-lanes.md`, `prompt-orchestration.md`, `validation-gates.md`, `artifact-roles.md`, `retrieval-metadata.md` | Method/authority reference-load per commission's Required Method Sequence | full files | clean |
| `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md` | Fitness reference (goal/success signal), ratified authority model, prescribed inventory method | Goal Handoff, Ratified Decision, Exact Next Authorized Action | clean |
| `forseti/product/spines/capture/core/source_capture_toolbox/README.md` | Toolbox pointer wiring + DCP receipt self-check | "Known Source-Family Routing", DCP receipt | clean |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | Playbook pointer wiring | "Known-source routing" paragraph | clean |
| `forseti/product/spines/capture/core/source_families/README.md` | The catalog itself | Lane Index table, Enforcement Candidate, Non-Claims | clean |
| `.../source_families/fragrance_native_database/README.md`, `retail_pdp/README.md`, `social_media/{instagram,tiktok,youtube,reddit}/README.md` | Per-family route maps; misclassification and pointer checks | Route Map / Canonical Classification / Layer Boundaries sections | clean |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Fast Route wiring | new catalog rows | clean |
| `docs/workflows/repo_map_recent_changes/capture_source_family_lane_catalog_v0.md` | Recent-change note | full file | clean |
| `git diff d9cb8d14^..d9cb8d14` (repo map, toolbox README, playbook, retail_pdp/instagram READMEs, handoff, submap) | Exact wire-up diff | full diff | clean |
| `orca-harness/{source_capture,runners,cleaning}` (`git ls-files`) | Independent inventory cross-check against catalog rows (the same method the handoff itself prescribed) | file listing + targeted reads of `price_payload_extraction.py`, `run_source_capture_price_payload_packet.py`, `audience_post_packet.py`, `audience_extractor.py`, `audience_post_input.py`, `reddit_agent_view.py` | clean |
| `docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md` | Checked for a possible owner scope-exclusion of `vendor_pricing_page` | grep for `vendor_pricing_page`/`price_payload`/scope | clean; no match found |
| `python .agents/hooks/check_retrieval_header.py --changed --strict`, `check_repo_map_freshness.py --changed --strict`, `git diff --check d9cb8d14^..d9cb8d14` | Re-run of the home lane's reported validation evidence | exit codes | re-run, all exit 0 |

**Source gaps (not read, named per source-loading economy):** full bodies of
`forseti/product/spines/data_lake/authority/*` contracts (only confirmed the
folder resolves — sufficient for the pointer-vs-restatement check performed,
insufficient for any claim about lake-authority *content*); the LinkedIn
lane-index pattern file (cited as precedent in the handoff, not needed to judge
this PR's own pattern-following); `docs/decisions/dcp_receipts_archive_v0.md`.

## Deep-Thinking Framing (Applied Before Findings)

Real question: not whether the catalog works for the families it names, but
whether it discharged the PR's own stated anchor_goal — "home every landed
family, not only fragrance-DB." That is a fitness-reference question
(review-lanes.md's intent-bearing-target rule), so decision criteria are
anchored to the handoff's bound goal/success-signal, treated as an attack axis,
not a pass bar. A finding that reproduces the exact diagnosed failure class
(an unhomed, code-confirmed, distinct source family) is evaluated as `critical`
because it falsifies the artifact's own closing claim on its own terms, not an
externally-imported bar. A finding that a *seam within an already-homed
family* is invisible from that family's new route map is evaluated as `major`
— same discoverability failure mode, narrower blast radius. See full framing
in the invoking conversation's `workflow-deep-thinking` turn.

## Findings — Correctness (Phase 1)

### AR-01 — `vendor_pricing_page` source family is fully unhomed

- severity: `critical`
- confidence: `high`
- location: `forseti/product/spines/capture/core/source_families/README.md`
  (Lane Index table); `forseti/product/spines/capture/core/source_capture_toolbox/README.md`
  ("Known Source-Family Routing"); `docs/workflows/forseti_repo_map_v0.md`
  (new Quick Index row)
- issue: a fully landed, tested, distinct source family declared literally as
  `source_family="vendor_pricing_page"` has zero row in any of the three
  routing surfaces this PR built or touched.
- evidence: `orca-harness/runners/run_source_capture_price_payload_packet.py:580`
  sets `source_family="vendor_pricing_page"`; its logic lives in
  `orca-harness/source_capture/price_payload_extraction.py` (a real,
  documented "Rung-1.5" JS-hydrated-SPA price extractor, not a stub). The
  family is documented only in implementation-level docs
  (`orca-harness/docs/source_capture_packet.md`, `orca-harness/README.md`),
  never in the product-facing routing layer. `docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md`
  — the one plausibly-relevant named scope decision — was checked and contains
  no mention of `vendor_pricing_page`, `price_payload`, or vendor pricing, so
  no found owner decision places this family out of the catalog's scope.
- strongest defense considered: the family might be intentionally out of
  scope (e.g. belongs to a different product vertical than
  fragrance/retail/social capture). This defense fails on current evidence: no
  scope decision naming it was found, and the catalog's own "Cold-Start Rule"
  states "If a source has no row here, treat it as a new-source probe under
  the playbook" — i.e. the catalog's own contract treats an omission as a gap,
  not a scope boundary, absent an explicit carve-out.
- impact: a cold agent told "capture the vendor pricing page and land it in
  the lake" cannot reach this lane from the toolbox/playbook/repo-map — the
  exact discovery failure the PR was commissioned to fix (fragrance-DB
  precedent), reproduced for a different family inside the same PR that
  claims to have fixed the class.
- `minimum_closure_condition`: either (a) `vendor_pricing_page` gets a lane
  index/row across the catalog, toolbox README, and repo map on the same
  pattern as the other seven families, or (b) an owner-visible scope decision
  is recorded stating why this family is intentionally excluded from
  `source_families/` routing. Closure additionally requires re-running (and
  showing the output of) a full `git ls-files orca-harness/{source_capture,runners,cleaning}`
  sweep against the catalog, since this family was missed by whatever sweep
  the PR performed — a re-run without evidence of a wider sweep does not close
  this finding, it only patches the one instance found.
- `next_authorized_action`: owner/CA decision — patch-before-acceptance or
  explicit scope acceptance. This review lane has no patch authority.
- `not_proven`: whether the PR's authors ran a full-directory inventory sweep
  at all, or ran one scoped only to the families named as candidates in the
  handoff (fragrance purchase-review, Reddit, historical). Both are
  consistent with the evidence; the residual observation below feeds this into
  the closure condition rather than asserting which occurred.

### AR-02 — Audience-post capture/cleaning seam missing from Instagram and YouTube route maps

- severity: `major`
- confidence: `high`
- location: `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md`
  ("Capture-To-Lake Route Map" table, new in this PR);
  `forseti/product/spines/capture/core/source_families/social_media/youtube/README.md`
  (new file, "Route Map" table)
- issue: a real, tested capture-to-cleaning seam spanning both families is
  invisible from either family's newly-authored, table-structured route map.
- evidence: `orca-harness/source_capture/audience_post_packet.py` declares
  `SUPPORTED_PLATFORMS = ("instagram", "youtube")` and documents itself as the
  "AUDIENCE-inference input surface (A4)" — a creator's written post
  caption+bio staged as a `SourceCapturePacket`. Its cleaning-lane consumers
  are `orca-harness/cleaning/audience_extractor.py` (Pass-1 LLM evidence
  extraction) and `orca-harness/cleaning/audience_post_input.py` (the
  packet→PostInput adapter). Tests exist:
  `orca-harness/tests/unit/test_audience_post_packet.py`,
  `test_audience_extractor.py` — this is landed code, not a stub. Neither the
  IG route map's five rows (Access/Grid/Deep-capture/Projection/Product-
  extraction) nor the YouTube route map's six rows (Access/Watch/Captions/
  Creator-observations/Transcript-extraction/Data-Lake) name this module set.
- strongest defense considered: the seam might reasonably fold into the
  existing "Access / method" row (post caption/bio is arguably an access-layer
  artifact). This partially holds for capture, but fails for the cleaning
  half: `audience_extractor.py`/`audience_post_input.py` are cleaning-layer
  code with no analogous row in either family's route map at all (unlike, e.g.,
  IG's explicit "Product extraction / Cleaning" row for transcript products).
  The seam is real and cross-cutting but currently has no assigned row in
  either family index.
- impact: a cold agent following either family's route map to find the
  capture→cleaning path for creator post text would not discover this landed
  seam and risks re-deriving or duplicating it.
- `minimum_closure_condition`: the seam gets a named row (or an explicit
  cross-reference) in both the Instagram and YouTube route maps, pointing to
  `audience_post_packet.py` and its cleaning consumers.
- `next_authorized_action`: owner/CA decision — patch-before-acceptance or
  accept as a named residual for a fast-follow.
- `not_proven`: whether other cross-cutting (multi-family) capture seams
  exist beyond this one; the audience-post seam was found because its
  `SUPPORTED_PLATFORMS` tuple made cross-family scope obvious in the source —
  a systematic sweep for other cross-cutting modules was not performed.

## Findings — Friction (Phase 2)

### AR-03 — Inventory-method evidence gap (minor, high confidence)

- severity: `minor`
- confidence: `high`
- location: `docs/prompts/handoffs/capture_playbook_lake_sync_handoff_v0.md`
  ("Exact Next Authorized Action", step 2) vs. the landed PR's artifacts
- issue: the handoff prescribed the inventory method
  (`git ls-files orca-harness/{source_capture,runners,cleaning}` + `rg`
  sweeps) that this review used to find AR-01 on the first attempt. Nothing in
  the PR's artifacts (catalog, toolbox README, repo-map note) shows that sweep's
  output, only its conclusions (the seven catalogued families). Coverage-first
  note: this is process/evidence friction, not a correctness defect by itself
  — it is reported because it is the plausible root cause connecting AR-01 and
  AR-02 (an incomplete or narrowly-scoped sweep would miss both a whole family
  and a cross-cutting seam the same way).
- `minimum_closure_condition`: the inventory sweep's actual command output (or
  an equivalent artifact) is preserved somewhere retrievable, so a future
  reviewer can check completeness without re-deriving it from scratch.
- `next_authorized_action`: advisory only; owner/CA may fold this into the
  AR-01/AR-02 closure pass rather than treat it as a separate action.

## Considered And Defended (Not Findings)

- Fragrantica/Parfumo/Basenotes classification as `fragrance_native_database`,
  not `retail_pdp` — the family README explicitly states this; verified
  correct, no misclassification.
- Data Lake admission/storage/Silver doctrine restated into playbook or lane
  indexes — spot-checked `fragrance_native_database/README.md` and
  `retail_pdp/README.md`: both are pointer-only ("Start at
  `forseti/product/spines/data_lake/README.md`..."), no fork found.
- Repo-map freshness and retrieval-header hooks — re-run on the current
  worktree (`check_retrieval_header.py --changed --strict`,
  `check_repo_map_freshness.py --changed --strict`, `git diff --check
  d9cb8d14^..d9cb8d14`): all exit 0, corroborating the home lane's reported
  evidence.
- The toolbox README's own DCP-receipt stale-language-search claim — independently
  re-run (`rg` for the six listed stale phrases across the named files): only
  the receipt's own literal matched, confirming the claim rather than
  contradicting it.
- Review-scope contamination — `git diff --name-status d9cb8d14..HEAD` shows
  the one commit ahead of the target only adds the review-commission prompt
  file itself; the catalog target is unmodified by it.
- Enforcement-hook overreach — the catalog's "Enforcement Candidate (Evaluated,
  Not Built)" section matches the handoff's step 5 instruction (evaluate, do
  not necessarily build); no hook was built, no overreach found.
- Cold-route hop count — manually traced for fragrance-native-DB and TikTok:
  playbook → "Known-source routing" pointer → catalog row → family README, 2
  hops, consistent with the cold-lane retrievability budget in
  `source-loading.md`.
- `orca-harness/source_capture/reddit_agent_view.py` (and its `_ab_probe`
  sibling) omitted from the Reddit family's Stage Split table — defended: the
  module's own `NON_CLAIMS` list states "not source capture" and "not Data
  Capture handoff"; it is a downstream agent-consumption view outside the
  catalog's declared capture-to-lake scope, correctly excluded.

## Not-Proven Boundaries

- Whether `vendor_pricing_page` is truly out of the catalog's intended scope
  by an owner decision not yet located in the repo (AR-01's own `not_proven`
  note).
- Whether other multi-family or generic-adapter modules besides
  `audience_post_packet.py` are similarly cross-cutting and under-routed — no
  systematic sweep for this pattern beyond the two found instances.
- Whether the PR's authors actually ran a full-repo inventory sweep and
  scoped it deliberately, or skipped the sweep — AR-03 names the gap, not the
  cause.
- Content-level correctness of the Data Lake authority docs the catalog
  points to (not opened in full; only pointer-vs-restatement was checked).

## Validation Evidence Inspected

| Check | Reported (home lane) | Re-run this review | Result |
| --- | --- | --- | --- |
| `check_retrieval_header.py --changed --strict` | reported clean | re-run | exit 0 |
| `check_repo_map_freshness.py --changed --strict` | reported clean | re-run | exit 0 |
| `git diff --check HEAD~1..HEAD` | reported clean | re-run as `d9cb8d14^..d9cb8d14` | exit 0 |
| cold-route spot checks (TikTok, Fragrantica) | reported done | independently re-traced (fragrance-DB + TikTok) | consistent, 2-hop |
| pre-push doc gates: OK (3 gates) | reported | not re-run (would duplicate the three checks above; no independent gate content beyond them was named) | not re-run, no contradiction found |
| PR state / CI status | n/a | `gh pr view 722` | OPEN, draft, CI `orca-harness-tests` SUCCESS |

None of the above are converted into approval, readiness, or merge-safety
claims; they corroborate the home lane's reported evidence and support this
review's freshness receipt.

## Review-Use Boundary

These findings are decision input only for the Chief Architect / owner
adjudicating PR #722. They are not approval, validation, mandatory
remediation, executor-ready patch authority, or merge readiness. `AR-01` and
`AR-02` are real, source-confirmed gaps against the PR's own stated
anchor_goal; `AR-03` is process friction offered as the likely shared root
cause. Final disposition (accept, accept-with-follow-up, or
patch-before-acceptance) is the adjudicator's call.
