# Ulta Category Bestseller Behavioral-Parity Success-Implementation Handoff 2026-07-25 v1

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Bounded implementation commission to reproduce the proven Sephora category
  bestseller-grid behavioral outcomes on Ulta across five beauty categories,
  using Ulta-native ordering, continuation, identity, and market evidence.
use_when:
  - Extending the category bestseller intelligence capture from Sephora to Ulta.
  - Proving Makeup, Skincare, Hair, Fragrance, and Bath & Body top-window capture on Ulta.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
stale_if:
  - Ulta category routes, native ordering, continuation UI, storefront markers, or product-card substrate change materially.
  - Another lane already lands complete Ulta category bestseller support.
authority_boundary: retrieval_only
```

## Commission Status And Prompt Preflight

This is an implementation-authorized cold handoff. It is preparation-only
until the receiving worktree and exact starting revision are independently
bound. The receiver must not treat existing Ulta brand-grid support as proof
that category grids or bestseller order already work.

```yaml
forseti_start_preflight:
  agents_read: required_by_receiver
  overlay_read: required_by_receiver
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope: >
    Ulta-native category bestseller discovery, bounded continuation, truthful
    US-route confirmation, mechanical grid projection, five-category dogfood,
    focused tests, and directly required shared wiring only.
  dirty_state_checked: receiver_to_verify
  blocked_if_missing: >
    A verified clean isolated receiver, public Ulta category routes, a
    retailer-native order that can be proven, or a truthful bounded
    continuation/termination signal.

prompt_preflight:
  output_mode: file-write
  write_destination: receiver implementation worktree, temporary dogfood evidence roots, and per-lane PR
  template_kind: handoff
  template_source: workflow-handoff max packet plus project prompt contract
  input_prompt_source: docs/prompts/handoffs/ulta_category_bestseller_behavioral_parity_success_implementation_handoff_20260725_v1.md
  edit_permission: implementation-authorized
  targets:
    - Ulta-local category capture adapter/parser/projection code and focused tests
    - existing shared retail runner/profile seams only when required for complete behavior
  branch: fresh codex/ branch from current origin/main in an isolated clean worktree
  dirty_state_allowance: none before work; stop on unexpected modified or untracked paths
  reviews: success-contract validation followed by de-correlated delegated review-and-patch for non-trivial runtime changes
  doctrine_change: none expected; return to owner if a standing cross-retailer contract or capture-risk boundary must change
  report_destination: receiver chat, branch diff, test output, temporary dogfood receipts, PR checks, and delegated-review adjudication
  external_source_boundary: public Ulta pages only; no login, account, profile, cookie export, credential injection, or access-control defeat
  repo_map_decision: not_needed
  repo_map_reason: current Ulta and Sephora seams plus the exact output behavior are named below

receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  managed_starting_ref: current_origin_main_at_dispatch
  required_revision: current_origin_main_at_dispatch
  revision_mode: exact
  capability_proof: receiver_must_prove
  no_concurrent_writer_state: receiver_must_prove

thread_operating_target_continuity:
  carried_forward: no
  reason: new_ulta_category_capture_workstream
  changed_from_input: no
  lifecycle_status: not_supplied
  if_changed_reason: not_applicable
```

## Load Contract

- packet_version: `workflow-handoff-max-v0`
- mode: `max`
- source_loading_mode: `repo-overlay-bound`
- created_at: `2026-07-25T01:43:20+08:00`
- created_by_lane: `codex/sephora-intelligence-ulta-handoffs`; provenance only
- authoring_workspace: `C:\tmp\forseti-sephora-intelligence-ulta-handoffs`
- handoff_path: `docs/prompts/handoffs/ulta_category_bestseller_behavioral_parity_success_implementation_handoff_20260725_v1.md`
- expected_authoring_branch: `codex/sephora-intelligence-ulta-handoffs`
- expected_authoring_head_before_handoff_write: `b806b2ec64cf1855565610efd7a4c116b47c87ef`
- expected_dirty_state_after_both_handoff_writes: exactly the two handoff files commissioned in this work unit
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting

Return exactly one load outcome before planning, probing, or editing:
`REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`,
`BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.

## Goal Handoff

- long_term_goal: Build comparable retailer bestseller/category observations that can later expose latent beauty-market problems and budding trends for competitive intelligence and go-to-market value creation.
- anchor_goal: Success implement the smallest complete Ulta-native equivalent of the proven Sephora five-category bestseller capture, preserving Ulta-specific route truth and failure visibility.
- success_signal: Makeup, Skincare, Hair, Fragrance, and Bath & Body each produce a reconciled, ordered, identity-bound, duplicate-visible, US-route-confirmed bounded grid projection and receipt—or an honest typed blocker proving which required native behavior Ulta does not expose.

## Open Decision / Fork

- decision: What Ulta-native surface and bound can truthfully reproduce the Sephora behavioral outcome?
  - options:
    - Category pages with a verifiable retailer-native bestseller sort and bounded load-more/pagination.
    - A retailer-owned bestsellers hub partitioned into the five categories, if that is the only native ranked surface.
    - Typed blocked outcome if no source-visible native ordering can support the requested claim.
  - already constrained / off the table:
    - Do not synthesize bestseller order from rating, review count, price, search order, or hand sorting.
    - Do not force Sephora's PageJSON, 60-row page, 12-page, or shipping-shell mechanics onto Ulta.
    - Do not reduce the commission to one category smoke test after the route is chosen.
  - trade-offs:
    - Reusing existing Ulta load-more/card extraction can minimize implementation, but current completeness and subject binding are brand-grid-shaped.
    - A category-specific adapter/projection is warranted if category identity, sort, continuation, or terminal-state semantics differ.
  - owner of the call: implementation receiver for retailer-local mechanics; owner escalation for a standing shared abstraction or weakened success claim.
  - recommendation: >
      Probe one representative category only long enough to bind the native
      substrate and ordering, then implement and dogfood all five categories
      in the same work unit. Fail visibly if Ulta exposes no defensible native
      bestseller order.

## Drift Guard

- No deep PDP or review-corpus capture in this work unit.
- No brand-authorization gate: this is a retailer category surface, not a brand corpus.
- No login, account creation, stored browser profile, cookies, credential injection, VPN, or proxy by default.
- Do not defeat an authentication/access-control gate. Public anti-bot friction follows the owner-authorized, human-rate capture playbook.
- Keep visible challenge/login/CAPTCHA classification separate from hidden residual DOM markers.
- Any block/CAPTCHA/login classification must preserve a diagnostic screenshot and the source-visible reason; a screenshot alone is not proof of a block.
- Do not call an arbitrary category order “bestselling.”
- Do not call a first page, first load-more slice, or fixed click count complete.
- Do not claim currency or delivery eligibility from a dollar glyph or US country route.
- Do not weaken current Ulta brand-grid, PDP, Sephora, or shared retail behavior.
- Do not build a generic cross-retailer category framework unless the Ulta result would otherwise remain false or fragile and the owner accepts the lock-in.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- capture-method entrypoint: `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` plus `capture_recon_index_v0.md`
- source-family entrypoint: `forseti/product/spines/capture/core/source_families/retail_pdp/README.md`
- targets to enter the implementation ladder:
  - `forseti-harness/source_capture/retail_capture_profiles.py`
  - `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`
  - `forseti-harness/source_capture/adapters/ulta_us_market.py`
  - `forseti-harness/source_capture/ulta_brand_grid.py`
  - `forseti-harness/source_capture/ulta_grid_projection.py`
  - `forseti-harness/source_capture/adapters/sephora_catalog_traversal.py`
  - `forseti-harness/source_capture/sephora_catalog_grid.py`
  - focused tests named in the source ledger
- already loaded by sender: current files at authoring HEAD plus five live Sephora projections; weak orientation only
- must load first: repository instructions/overlay and the capture playbook, then current Ulta call sites/tests before any live probe
- load rule: re-run progressive source loading and lake-first preflight; do not inherit source semantics from this packet

### Earlier-decided concepts and behaviors

- Existing Ulta support captures a complete `/brand/<slug>` grid using a rendered “You have viewed N of N” terminal signal and a bounded load-more profile.
  - verify pointer: `ulta_brand_grid.py`, `ulta_grid_projection.py`, and `retail_capture_profiles.py`
  - compare target: current receiver revision
- Existing Ulta grid market confirmation establishes the US country route while leaving grid currency and delivery location unpinned.
  - verify pointer: `adapters/ulta_us_market.py`
  - compare target: current receiver revision
- Existing Ulta projection still derives requested subject from `/brand/<slug>` and reconciles rendered brand heading to that slug.
  - verify pointer: `_requested_brand_slug` and completeness logic in `ulta_grid_projection.py`
  - compare target: authoring SHA-256 below; receiver reread required
- Sephora is the behavioral reference only: five categories, top 720 placements, contiguous ranks, exact identities, no duplicates, complete receipts, 12/12 serialized US pages, and no access block.
  - verify pointer: five pinned projections in the sibling Sephora interpretation handoff
  - compare target: exact projection hashes; never copy Sephora source mechanics

## Active Objective

Success implement one complete Ulta category bestseller capture route and
dogfood it across Makeup, Skincare, Hair, Fragrance, and Bath & Body. Preserve
truthful partial/block outcomes, validate the owner-visible behavior, commission
de-correlated review-and-patch for the non-trivial runtime diff, adjudicate it,
and land the lane through the repository PR workflow.

## Exact Next Authorized Action

1. Bind an isolated clean receiver at exact current `origin/main`; prove repo, branch, HEAD, writable root, dirty state, and one writer.
2. Re-run source loading, lake-first preflight, and the public/access-controlled classification.
3. Inspect current Ulta category/bestseller surfaces in one representative category. Record the actual substrate, native ordering control/state, declared count, continuation/termination, category identity, market evidence, and block posture.
4. Bind a compact success contract and the plausible false-success path before editing.
5. Implement the smallest complete Ulta-local category route, reusing current card extraction, packet, content-retention, projection models, and browser lifecycle where their semantics actually fit.
6. Add category-aware subject binding, native-order proof, continuation/termination reconciliation, placement/rank identity, duplicate accounting, market scope, and typed failure receipts.
7. Dogfood the final route across all five named categories to new temporary roots at a human-rate cadence.
8. Run focused and affected tests, wrong-cause perturbations, `git diff --check`, and current required gates.
9. Route the validated non-trivial diff through a different-vendor delegated review-and-patch pass; adjudicate and revalidate any patch.
10. Commit, push, open the per-lane PR, observe checks, and self-merge only when repository guards permit.

## Authority And Source Ledger

- `AGENTS.md` and `.agents/workflow-overlay/{README,source-loading,decision-routing,prompt-orchestration,validation-gates,delegated-review-patch}.md`
  - Role: repository authority, receiver isolation, source loading, validation, prompt, review, and lifecycle rules.
  - Load-bearing: yes.
  - Compare target: current receiver checkout; reread-required.
  - Last checked: 2026-07-25 at authoring HEAD.
  - Reuse rule: current source wins.
- `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
  - Role: access gate, substrate-first route selection, instrument check, human-rate bound, receipt, and screenshot triggers.
  - Load-bearing: yes.
  - Compare target: SHA-256 `aac268200599b047c1a1a806635fb8f609ecbb53e5659073fd569615460f830b8`.
  - Last checked: 2026-07-25.
  - Reuse rule: hash and reread before live work.
- `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
  - Role: prior Ulta embedded-state and blocked-is-hypothesis orientation.
  - Load-bearing: no for current Ulta facts; yes for avoiding known false diagnosis.
  - Compare target: SHA-256 `22ba2475317a731fc1aeb55c6437a07bc0ef1b916859c6af21a9cbf53504493e`.
  - Last checked: 2026-07-25.
  - Reuse rule: current live source decides route.
- `forseti/product/spines/capture/core/source_families/retail_pdp/README.md`
  - Role: current Retail/PDP source-family route map and non-claims.
  - Load-bearing: yes.
  - Compare target: SHA-256 `a858c3d575b758fee8f9bfb88aa3ce269484d48a9b401c7fc3191774338950d6`.
  - Last checked: 2026-07-25.
  - Reuse rule: hash and reread relevant grid sections.
- `forseti-harness/source_capture/adapters/sephora_catalog_traversal.py`
  - Role: proven behavioral reference for bounded multi-page category traversal and truthful persistent-shell limitation.
  - Load-bearing: yes for success semantics; no for Ulta selectors or substrate.
  - Compare target: authoring SHA-256 `24523a09cd4a3ab93f58d26873629ba664120ca11d199e46ec8c62791b8c9baa`.
  - Last checked: 2026-07-25.
  - Reuse rule: transfer invariants only.
- `forseti-harness/source_capture/adapters/ulta_us_market.py`
  - Role: current Ulta PDP/brand-grid US-route confirmation.
  - Load-bearing: yes.
  - Compare target: authoring SHA-256 `3691b0a65ec388ccbf2fd4c83e48373e699ab3acf8f4cdd0837159fe634cf986`.
  - Last checked: 2026-07-25.
  - Reuse rule: reread and extend only if category surface requires a real semantic delta.
- `forseti-harness/source_capture/ulta_brand_grid.py`
  - Role: current rendered Ulta product-card extraction and terminal control state.
  - Load-bearing: yes.
  - Compare target: authoring SHA-256 `379b50befd5c2692c6141a18e74846e34d2bbf785507152e2261908649164c28`.
  - Last checked: 2026-07-25.
  - Reuse rule: preserve brand-grid compatibility; do not assume category fit.
- `forseti-harness/source_capture/ulta_grid_projection.py`
  - Role: current Ulta grid projection, identity, duplicate merge, and brand-shaped completeness.
  - Load-bearing: yes.
  - Compare target: authoring SHA-256 `36c11f7c27a97f5db7cfc4b8fae6ea5030b726f0a05af147d16ac69e01ad9cb9`.
  - Last checked: 2026-07-25.
  - Reuse rule: preserve brand-grid behavior while introducing truthful category semantics.
- `forseti-harness/source_capture/retail_capture_profiles.py` and `runners/run_source_capture_cloakbrowser_packet.py`
  - Role: current Ulta load-more defaults, market flag, content extraction, packet/projection wiring, and CLI.
  - Load-bearing: yes.
  - Compare targets:
    - profile SHA-256 `02451ab209f5b577a27add8c6de68822d67828731c4036286f4760065510a865`
    - runner SHA-256 `f2c80af7080538f82891e16e0238358329eed42d274a0d17feef5e42d18034bc`
  - Last checked: 2026-07-25.
  - Reuse rule: change only proven necessary seams.
- focused tests:
  - `tests/unit/test_ulta_us_market_wiring.py`
  - `tests/unit/test_retail_capture_profiles.py`
  - `tests/unit/test_retail_grid_projection.py`
  - `tests/unit/test_source_capture_cloakbrowser_snapshot.py`
  - `tests/unit/test_sephora_catalog_traversal.py`
  - Role: current contracts and regression boundaries.
  - Load-bearing: yes for validation scope, no as product authority.
  - Compare target: current receiver revision; reread-required.
  - Last checked: 2026-07-25.
  - Reuse rule: extend focused tests and run affected existing tests.

## Planned Success Contract (`PLANNED_NOT_OBSERVED`)

### S1 — Native bestseller identity

- Given a current public Ulta category or bestsellers surface,
- when the route claims bestseller order,
- then a retailer-owned control, serialized state, request parameter, or other source-native evidence must bind that exact order.
- Forbidden: inferred order from ratings, reviews, price, sponsored placement, or default DOM sequence.
- Wrong-cause check: remove or change the native sort evidence while leaving cards intact; admission must fail for sort, not for missing cards.

### S2 — Five exact category subjects

- Makeup, Skincare, Hair, Fragrance, and Bath & Body each bind to the requested Ulta subject through source-visible route/state.
- Category identity must not reuse `/brand/<slug>` semantics.
- Wrong-cause check: feed a valid ordered grid from the wrong category; subject binding must fail.

### S3 — Bounded top-window completeness

- For each category, capture the largest defensible retailer-native ordered window needed to cover at least the top quartile of the declared category cohort, capped at 720 placements unless current source proves a smaller terminal corpus.
- Reconcile declared count, requested bound, continuation activations/pages, terminal state, captured placements, unique parents, and duplicates.
- If a category cannot reach the top quartile within the 720 cap, preserve the exact achieved window and return partial rather than widening silently.
- Wrong-cause check: stop one continuation early and leave the control present; completeness must fail.

### S4 — Ordered identity and duplicates

- Every retained placement has stable Ulta product identity, canonical product URL, category, rank/position, and raw anchor.
- Ranks/positions are contiguous for the retained native window.
- Duplicate parent products remain visible as multiple placements and affect completeness; they are not silently erased.
- Wrong-cause check: duplicate one placement and remove another; duplicate and missing-rank failures must remain distinguishable.

### S5 — Truthful US route

- Every admitted category capture satisfies the current Ulta grid US-country conjunction.
- Currency and delivery eligibility remain independently typed and may stay unpinned.
- Forbidden: USD from `$`, US delivery from country route, or shopper origin from page state.

### S6 — Access and screenshot truth

- Visible source content and title decide challenge/login/CAPTCHA posture before residual full-DOM markers.
- A classified block preserves one diagnostic screenshot and the exact visible reason.
- A normal repeated semantic refresh does not require a screenshot unless the route changed, a visual fact matters, or diagnosis is needed.
- Wrong-cause check: hidden challenge-script text under a valid rendered category must not become a false CAPTCHA.

### S7 — Safe transport and lifecycle

- Default route uses no login, profile persistence, raw cookies, credentials, VPN, or proxy.
- One browser/context/tab is reused across a bounded multi-page/load-more run unless Ulta-specific evidence makes reuse unsafe.
- Packet/content/projection failures remain nonzero and preserve diagnosable source evidence.

### S8 — Full dogfood

- All five categories run through the final implementation, not a fixture-only or one-category proof.
- Each run reports category, native sort evidence, declared cohort, captured window, window share, identities, ranks, duplicates, market scope, access posture, screenshot trigger, hashes, residuals, and exact terminal condition.
- No result claims Ulta sales, market share, category-wide completeness beyond its declared bound, or platform-wide route stability.

Most plausible false success: reuse the current Ulta brand-grid profile against
one category URL, click “Load more” ten times, project whatever cards remain,
and label the result bestselling and complete without proving native sort,
category identity, terminal state, or the top-quartile bound. S1-S5 reject it.

## Smallest-Complete Implementation Route

1. Probe one representative category to identify source-native order and continuation.
2. Decide whether the current card extractor can accept an explicit category subject or whether a category-local content record is cleaner.
3. Add only the Ulta-local category semantics and necessary runner/profile options.
4. Keep current brand-grid and PDP behavior byte-compatible unless a failing shared invariant proves otherwise.
5. Use one mechanical projection path that records category, rank, order evidence, declared total, achieved share, and termination.
6. Add focused positive, wrong-category, wrong-sort, premature-stop, duplicate, market, hidden-challenge, visible-block, and cap/terminal tests.
7. Dogfood all five categories at human rate to new temporary roots.

Do not split this into a one-category implementation cycle followed by four
future handoffs. The probe is a design input; the commissioned proof unit is
all five categories.

## Validation

At minimum run the focused affected suites from `forseti-harness` with a unique
`--basetemp`, including:

```powershell
python -m pytest -p no:cacheprovider -q --basetemp <unique> `
  tests/unit/test_ulta_us_market_wiring.py `
  tests/unit/test_retail_capture_profiles.py `
  tests/unit/test_retail_grid_projection.py `
  tests/unit/test_source_capture_cloakbrowser_snapshot.py `
  tests/unit/test_sephora_catalog_traversal.py `
  <new-or-extended-ulta-category-tests>
git diff --check
```

Then run current affected contract and broad gates required by the repository.
Preserve actual commands, exits, output, and not-run reasons. For each live
dogfood, verify the projection and receipt from fresh reads; an exit code alone
is not success.

The non-trivial runtime diff enters the current de-correlated delegated
review-and-patch lane after validation. Bind the immutable validated revision,
clean reviewer worktree, exact changed files, dogfood roots/hashes, and
validation commands. Reviewer claims remain claims until adjudicated.

## Frozen Decisions

- Ulta is the next retailer.
- Same five semantic categories as Sephora.
- Grid-only; no deep PDP or review capture.
- Native retailer order, category identity, top-window completeness, duplicates, and truthful market scope are mandatory.
- Top quartile is the target; 720 placements is the default upper bound, not a forced count.
- Real block, partial, absent-native-sort, and terminal outcomes remain visible.

## Mutable Questions

- Exact canonical Ulta category URLs and category identifiers.
- Native bestseller control/state and whether it survives continuation.
- Category declared-count substrate.
- Load-more versus pagination versus internal state extraction.
- Whether existing `ulta_brand_grid.py` can truthfully become subject-aware without forking brand behavior.
- Actual human-rate cadence and whether screenshots trigger during the changed-route baseline.

## Superseded / Dangerous-To-Reuse Context

- Existing Ulta brand-grid completeness as category readiness: not proven.
- Ten load-more clicks as completeness: false unless source-visible terminal state and requested bound reconcile.
- Sephora `BEST_SELLING` query/PageJSON as Ulta semantics: unsafe analogy.
- Default category order as bestseller order: unproven.
- Dollar glyph as USD and US route as delivery eligibility: false.
- Hidden challenge strings as a CAPTCHA classification: known false-positive risk.

## Blockers And Risks

- No source-native bestseller order: return `BLOCKED_NO_NATIVE_BESTSELLER_ORDER` with current visible/state evidence and an instrument control; do not synthesize order.
- Category surface is access-controlled: stop unless the owner has legitimate entitled access; never defeat auth.
- Public anti-bot friction: re-probe only through a different hypothesis at human rate and preserve receipts.
- No trustworthy declared count or terminal state: return partial or `NEEDS_ARCHITECTURE_PASS`; do not call a click cap complete.
- Required shared abstraction or weakened success claim: stop for owner decision.

## Workspace State

- authoring branch: `codex/sephora-intelligence-ulta-handoffs`
- authoring HEAD before packet write: `b806b2ec64cf1855565610efd7a4c116b47c87ef`
- dirty state before packet write: clean
- expected dirty state after both packet writes: the two commissioned handoff files only
- current Ulta code at authoring HEAD supports brand grids and PDPs; category bestseller parity is not claimed

## Confirm-Don't-Trust Checklist

- Verify handoff path, receiver revision, clean state, and writer isolation.
- Confirm no Ulta category implementation landed after authoring.
- Hash/reread current playbook, Retail/PDP index, Ulta code, call sites, and focused tests.
- Inspect live public Ulta source before choosing selectors or state fields.
- Prove the native order, subject, declared count, continuation, market, and access posture independently.
- Re-run wrong-cause tests, all five dogfoods, and delegated review adjudication.

## Receiver Return Contract

```yaml
load_outcome:
source_context_status:
receiver_binding:
success_contract:
ulta_probe:
  access_classification:
  category_surface:
  native_order:
  declared_count:
  continuation:
implementation:
dogfood:
  makeup:
  skincare:
  hair:
  fragrance:
  bath_and_body:
  transport:
validation:
wrong_cause_checks:
delegated_review:
  decorrelation:
  findings:
  patch:
  adjudication:
residuals:
lifecycle:
verdict: BLOCKED | NEEDS_ARCHITECTURE_PASS | PATCH_ADJUDICATION_REQUIRED | READY_TO_LAND | LANDED
exact_next_action:
```

## Do Not Forget

The goal is behavioral parity, not code parity. Reuse the working Ulta capture
spine aggressively, but derive ordering, category identity, continuation, and
termination from Ulta's current source rather than from Sephora's implementation.
