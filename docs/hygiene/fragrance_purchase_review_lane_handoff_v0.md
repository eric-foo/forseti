# Fragrance Purchase Review Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet
scope: >
  Transfers the fragrance purchase-review retailer capture lane after PR #436
  merged, preserving the lane goal frame, capture substrate, residuals, and
  next-lane fork.
use_when:
  - Starting a fresh lane for fragrance purchase-review capture coverage after PR #436.
  - Re-establishing the row-capture, rendered companion, and widget-fallback boundaries.
  - Deciding whether to expand from fixture coverage into a product-corpus pilot.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/artifact-folders.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md
  - orca-harness/source_capture/fragrance_rendered_widget_companion.py
  - orca-harness/source_capture/fragrance_review_coverage.py
branch_or_commit: codex/fragrance-purchase-review-probes @ 14ddff9a08844cded9f2f650d5f0951e84d059e7
stale_if:
  - PR #436 no longer reports state MERGED with merge commit 57eb81becc6d9ff52c79ac561c6dbd4d3b8fc9c9.
  - Any named capture helper, runner, or fragrance purchase-review Capture doc changes before the receiver acts.
  - The owner redirects from fragrance purchase-review retailer PDP capture to community, native fragrance database, Cleaning, ECR, or Judgment work.
```

## Load Contract

- packet_version: 1
- mode: max
- source_loading_mode: repo-overlay-bound plus live GitHub PR-state verification
- created_at: 2026-06-29 Asia/Singapore
- created_by_lane: Codex current thread, for provenance only; not an authority claim
- workspace: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\fragrance-purchase-review-probes`
- handoff_path: `docs/hygiene/fragrance_purchase_review_lane_handoff_v0.md`
- expected_branch_at_creation: `codex/fragrance-purchase-review-probes`
- expected_head_before_this_handoff_file: `14ddff9a08844cded9f2f650d5f0951e84d059e7`
- merged_pr_compare_target: PR #436 reports `state=MERGED`, `mergedAt=2026-06-29T15:58:01Z`, `mergedBy=eric-foo`, `headRefOid=14ddff9a08844cded9f2f650d5f0951e84d059e7`, `mergeCommit=57eb81becc6d9ff52c79ac561c6dbd4d3b8fc9c9`.
- current_main_compare_target_at_creation: after `git fetch origin main`, `origin/main=59686310e0463164134df64e9d14eb59b5edf014`; PR #436 merge commit `57eb81becc6d9ff52c79ac561c6dbd4d3b8fc9c9` is an ancestor of that ref.
- expected_dirty_state_including_handoff_file: this worktree was clean before writing this handoff; after initial write, this handoff file is the only expected dirty/untracked path. The repository root checkout is on a different dirty lane and was intentionally not used as the handoff write surface.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting. This packet is an orientation artifact, not authority, validation proof, or permission to expand scope.

## Goal Handoff

- long_term_goal: Own fragrance purchase-review retailer PDP capture as a reliable evidence lane for later review-integrity interpretation and product pain/pleasure analysis, distinct from Reddit/community, native fragrance database, Cleaning, ECR, and Judgment lanes.
- anchor_goal: Maintain a bounded, repeatable capture substrate across locked fragrance specialist/retailer sources that preserves row-level review provenance, rating, month/recency, length bucket, media and verified-purchase flags when visible, aggregate rating/count comparison, above-fold shopper context, and honest residuals.
- success_signal: A fresh operator can run one capture command per PDP that renders the product page, passively preserves widget responses fired by that render, uses bounded widget fallback only when needed, emits focused review coverage rows, and leaves enough residuals for the owner to decide whether to expand coverage without re-litigating the source rungs.
- non_goal: This lane has not produced source-wide review archives, durable Attachment Records, Cleaning output, ECR output, Judgment output, pain/pleasure labels, review-integrity scoring, or demand proof.

## Open Decision / Fork

- decision: What should the fresh continuation lane optimize next?
  - A. Product-corpus pilot across the five locked retailers using the merged helper and site registry. Pin a small product URL set, run rendered+widget capture, and report coverage/residuals without interpreting reviews.
  - B. Source-wide route hardening per retailer. Probe pagination, product discovery, and review-widget drift beyond the locked fixtures.
  - C. Downstream interpretation. Feed captured rows into Cleaning/Judgment or pain/pleasure analysis.
- recommendation: Start with A. It compounds the merged capture substrate while keeping claims honest. B is useful after A reveals which retailers are worth broader investment. C is premature until the lane either physicalizes durable Attachment Records or the owner accepts a separate downstream interpretation scope.
- owner of the call: current user / Chief Architect in the new lane.

## Drift Guard

- Do not treat sampled PDP coverage as source-wide retailer coverage. Current evidence is fixture/product-level unless a later lane proves broader coverage.
- Do not store raw review bodies in tracked markdown. Keep raw bodies in ignored scratch outputs or in a later authorized durable Attachment Record path.
- Do not add interpretation fields to source-visible review rows. The focused coverage helper rejects pain, pleasure, sentiment, integrity, demand, strength, and similar downstream labels in `source_visible_fields`.
- Do not treat rendered+widget capture as one literal HTTP request. It is one operator command: browser render, same-load passive widget preservation, and bounded fallback for missing widget pages.
- Do not reopen fragrance community/native database lanes here. This lane is the purchase-review retailer PDP lane.
- Do not call the MGT/SCI lens a validation tier. Here it means focused review coverage under the smallest complete intervention: enough row data for a human/agent reader, with named residuals.

## Inherited Context

### What PR #436 Landed

- Capture docs:
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md`
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md`
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md`
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md`
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md`
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md`
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_rendered_companion_probe_v0.md`
- Runtime and runners:
  - `orca-harness/source_capture/fragrance_review_coverage.py`
  - `orca-harness/runners/run_fragrance_review_coverage.py`
  - `orca-harness/source_capture/fragrance_rendered_widget_companion.py`
  - `orca-harness/runners/run_fragrance_rendered_widget_companion.py`
  - `orca-harness/source_capture/adapters/fragrance_widget_fallback.py`
- Tests:
  - `orca-harness/tests/unit/test_fragrance_review_coverage.py`
  - `orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py`
  - `orca-harness/tests/contract/test_source_capture_packet_no_runtime_imports.py`
- Review prompt/output:
  - `docs/prompts/reviews/fragrance_rendered_widget_companion_adversarial_code_review_prompt_v0.md`
  - `docs/review-outputs/adversarial-artifact-reviews/fragrance_rendered_widget_companion_adversarial_code_review_v0.md`

### Current Capture Shape

- Five locked purchase-review sources are in the v0 registry: Ministry of Scent, Luckyscent / Scent Bar, Twisted Lily, ZGO Perfumery, and Indigo Perfumery.
- Judge.me is the public review-widget substrate for Ministry, Luckyscent, Twisted Lily, and Indigo. Yotpo v3 storefront is the row-positive substrate for the current ZGO fixture.
- The focused coverage row shape preserves row id/key, native review id when present, rating, review month, length bucket, verified-purchase flag when visible, media flag, helpful counts when visible, source app/badge fields, product binding, selected/skipped status, and residuals.
- The rendered companion adds above-fold shopper context: visible product title, price, CTA, size/variant, stock/pickup, and whether rating/review count or review sections are visible in the first viewport.
- The companion now delegates direct fallback URL fetching to `source_capture/adapters/fragrance_widget_fallback.py`; the main companion module no longer owns direct `urllib` transport.

### Latest Lane Smoke Orientation

The previous lane reported a five-source rendered+widget smoke on the final code. Treat these numbers as orientation only unless the receiver reruns or opens the scratch receipts.

| Source | Rows | Selected | Dominant Route | Verified True | Media True | Notable Residual |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| Indigo Perfumery | 13 | 2 | `bounded_fallback` | 12 | 0 | `passive_widget_not_observed_during_render` |
| Ministry of Scent | 4 | 3 | `bounded_fallback` | 3 | 0 | `passive_widget_not_observed_during_render` |
| Twisted Lily | 6 | 6 | `bounded_fallback` | 6 | 0 | `passive_widget_not_observed_during_render` |
| ZGO Perfumery | 1 | 1 | `render_passive` | 1 | 0 | `aggregate_review_count_widget_total_count_mismatch` |
| Luckyscent / Scent Bar | 14 | 8 | `bounded_fallback` | 3 | 0 | `passive_widget_not_observed_during_render` |

### Stale Or Superseded Earlier Beliefs

- "ZGO and Indigo are worthless" is stale. ZGO has a row-positive Yotpo v3 fixture; Indigo has a row-positive Judge.me widget route, though the visible PDP can underexpose rows.
- "Rendered capture alone completes review rows" is false for this lane. Rendered capture adds shopper salience; widget routes still complete row coverage for several sources.
- "The companion should own direct HTTP fallback transport" is stale after the PR #436 CI fix. Fallback transport lives in the adapter module.
- "Source-wide coverage is complete" is false. The lane has fixture/product-level coverage and a substrate for the next pilot.

## Active Objective

Fresh lane should convert the merged fixture-level capture substrate into a bounded product-corpus pilot, unless the owner redirects. The pilot should prove whether the five-source shape remains useful across more real fragrance PDPs before any downstream interpretation lane consumes review text.

## Exact Next Authorized Action

1. Start from current `main`, not the merged feature branch, and verify PR #436 is present by checking that merge commit `57eb81becc6d9ff52c79ac561c6dbd4d3b8fc9c9` is an ancestor of `origin/main` or the local base.
2. Load the packet's `open_next` sources, then inspect the site registry and focused coverage MGT before running or modifying capture.
3. Pick the smallest product-corpus pilot: one or two additional row-positive PDPs per locked retailer, with product URLs recorded before capture, and no source-wide or downstream interpretation claim.
4. Run rendered+widget companion capture for each selected PDP. Preserve route/residuals, aggregate rating/count, selected row count, rating/month/length buckets, verified/media flags, and above-fold context. Keep raw review bodies out of tracked markdown.
5. Return a compact coverage report and decide whether the next move is broader source-route hardening, durable Attachment Record physicalization, or a separate Cleaning/Judgment interpretation lane.

## Authority And Source Ledger

- `AGENTS.md`
  - Role: Orca agent behavior kernel.
  - Load-bearing: yes.
  - Compare target: reread-required before strict workflow, validation, commit, or handoff claims.
- `.agents/workflow-overlay/README.md`
  - Role: Orca overlay entrypoint and binding rule.
  - Load-bearing: yes.
  - Compare target: reread-required before project-authority or overlay claims.
- `.agents/workflow-overlay/decision-routing.md`
  - Role: Cynefin routing for cross-thread and next-lane work.
  - Load-bearing: yes.
  - Compare target: reread-required before planning/delegation in the new lane.
- `.agents/workflow-overlay/artifact-folders.md`
  - Role: accepted artifact placement; confirms `docs/hygiene/` as an accepted home for routing notes.
  - Load-bearing: yes.
  - Compare target: line-level reread-required before rehoming this packet.
- `gh pr view 436 --repo eric-foo/orca --json state,closed,closedAt,mergedAt,mergedBy,mergeCommit,headRefOid,baseRefName,url,title,mergeStateStatus,headRefName`
  - Role: merge-state compare target.
  - Observed output: `state=MERGED`, `mergedAt=2026-06-29T15:58:01Z`, `mergeCommit=57eb81becc6d9ff52c79ac561c6dbd4d3b8fc9c9`, `headRefOid=14ddff9a08844cded9f2f650d5f0951e84d059e7`.
  - Reuse rule: rerun before claiming PR #436 state in a new lane.
- `git fetch origin main`; `git rev-parse origin/main`; `git merge-base --is-ancestor 57eb81becc6d9ff52c79ac561c6dbd4d3b8fc9c9 origin/main`
  - Role: local remote-main compare target.
  - Observed output: `origin/main=59686310e0463164134df64e9d14eb59b5edf014`; merge commit is an ancestor.
  - Reuse rule: rerun before basing new work on main.

## Validation Notes

- PR #436 final pre-merge CI state was reported clean by GitHub checks before merge; do not reuse that as validation for later edits.
- Focused local validations reported in the lane before merge:
  - `orca-harness/tests/contract/test_source_capture_packet_no_runtime_imports.py`
  - `orca-harness/tests/unit/test_fragrance_review_coverage.py`
  - `orca-harness/tests/unit/test_fragrance_rendered_widget_companion.py`
  - repo hygiene hooks including map links, header index, CSB scanning artifact, ontology, deletion evidence, and DCP receipt checks.
- This handoff file itself needs only retrieval/header and placement sanity. It is a local continuation packet, not a PR artifact or a new capture proof.

## Non-Claims

- Not a source-wide retailer review corpus.
- Not a current-state proof unless the receiver reruns live capture.
- Not an authority source over the Capture docs, code, or site registry.
- Not a commitment that all five retailers remain stable.
- Not permission to start Cleaning, ECR, Judgment, pain/pleasure labeling, or review-integrity scoring.
