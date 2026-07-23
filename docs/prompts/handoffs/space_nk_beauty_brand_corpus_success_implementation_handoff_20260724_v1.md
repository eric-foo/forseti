# Space NK Beauty Brand Corpus Success-Implementation Handoff v1

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Bounded greenfield implementation commission for a verified Space NK US brand-grid, complete PDP corpus, and selected deep-review capture.
use_when:
  - Dispatching Space NK as a trend-led and international prestige/indie retailer route.
  - Building the third retailer expansion lane from the verified shared retail and REVOLVE corpus contracts.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
branch_or_commit: codex/beauty-retailer-expansion-handoffs based on 9d1e64b503abccd48611d31da07d3d124fdf6167
stale_if:
  - Space NK's US domain/locale, brand/PDP route, review provider, or regionalization materially changes.
  - A current brand-owned source does not authorize Space NK for the selected proof brand.
authority_boundary: retrieval_only
```

## Commission Status And Forseti Prompt Preflight

This is an implementation-authorized cold handoff. It is preparation-only until
the receiving worktree and revision are independently bound.

```yaml
prompt_preflight:
  output_mode: file-write
  write_destination: bounded receiver implementation worktree, temporary dogfood evidence root, and per-lane PR
  template_kind: none
  input_prompt_source: docs/prompts/handoffs/space_nk_beauty_brand_corpus_success_implementation_handoff_20260724_v1.md
  edit_permission: implementation-authorized
  targets: Space NK capture code and tests; shared retail seams only when required for complete behavior
  branch: fresh codex/ branch from current origin/main in a clean isolated worktree
  dirty_state_allowance: none before work; stop on unexpected modified or untracked paths
  reviews: success-implement validation followed by mandatory de-correlated delegated review-and-patch
  doctrine_change: none
  report_destination: receiver chat, branch diff, validation output, PR checks, and temporary capture receipts

receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  managed_starting_ref: current_origin_main_at_dispatch
  required_revision: current_origin_main_at_dispatch
  revision_mode: exact
  capability_proof: receiver_must_prove
  no_concurrent_writer_state: receiver_must_prove
```

## Load Contract

- packet_version: `workflow-handoff-max-v0`
- mode: `max`
- created_at: `2026-07-24`
- created_by_lane: `codex/beauty-retailer-expansion-handoffs`
- authoring_workspace: `C:\tmp\forseti-beauty-retailer-expansion-handoffs`
- handoff_path: `docs/prompts/handoffs/space_nk_beauty_brand_corpus_success_implementation_handoff_20260724_v1.md`
- authoring_base: `9d1e64b503abccd48611d31da07d3d124fdf6167`
- expected_dirty_state_including_handoff_file: authoring lane changed only the three commissioned retailer handoffs before commit; receiving implementation lane must be clean
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against current source before acting

Return exactly one load outcome before planning or editing: `REUSE`,
`PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`,
`BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.

## Goal Handoff

- **Long-term goal:** maintain enough complementary retailer routes to obtain
  four truthful product-level corpora for indie and mid-market beauty products
  whenever four authorized public listings exist.
- **Anchor goal:** build the smallest complete no-VPN Space NK US/USD
  brand-grid → every-grid-PDP → selected-deep-review route on the shared retail
  spine.
- **Success signal:** one currently authorized representative brand completes
  a reconciled Space NK US grid, every unique PDP, and one provider-bound deep
  review capture with truthful receipts, hashes, negative tests, live dogfood,
  and independent review-and-patch adjudication.

## Open Decision / Fork

- **Recommended first candidate:** Summer Fridays, because the existing Forseti
  evidence already includes verified Sephora and REVOLVE Summer Fridays grids/
  corpora and Space NK currently exposes a Summer Fridays brand assortment.
- **Required check:** fresh brand-owned evidence must name or otherwise prove
  Space NK authorization. The Space NK directory alone is insufficient.
- **Fallback:** choose a different currently authorized Space NK indie brand
  with manageable grid size and sufficient public review depth; preserve the
  official-first decision record.
- **Regionalization fork:** determine the actual US route, locale/currency
  state, and canonical behavior from current source. Do not assume `/us/`,
  `.com`, language, or displayed currency alone proves a US surface.
- **Owner boundary:** a new standing browser framework, proxy dependence,
  weakening shared identity/completeness, or provider-wide abstraction returns
  to the owner.

## Drift Guard

- Space NK has no retailer-specific runtime files in the authoring checkout;
  confirm that absence at the receiver revision before treating this as
  greenfield.
- Greenfield does not mean build a parallel capture framework. Reuse shared
  packet, browser, projection, PDP cleaning, receipt, and failure semantics.
- Do not use Summer Fridays merely because prior corpora exist; official Space
  NK authorization is a fresh gate.
- No VPN, proxy, ambient proxy, profile persistence, login, or access-control
  bypass.
- Do not collapse UK/international and US evidence or silently convert prices.
- Do not call a partial grid or one PDP a retailer corpus.
- Do not modify existing retailers except for a proven shared defect required
  by the Space NK outcome.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- Overlay policy: `.agents/workflow-overlay/source-loading.md`.
- Enter through shared retail capture/projection/PDP/browser sources and the
  merged REVOLVE implementation.
- Already loaded here: current authoring tree and optional local REVOLVE
  receipts; both are orientation only.
- Must load first: project instructions/overlay, then current shared contracts,
  call sites, and tests before introducing Space NK files.
- Expand reads only along actual imports/callers or a source-visible Space NK
  requirement.

### Earlier-decided concepts and behaviors

- Official-first admission prevents repeating the Ulta Summer Fridays error.
- A no-VPN US/USD route must be source-confirmed and may truthfully remain
  blocked.
- REVOLVE merge `85c87a7467a3f2e49df5ce95510c60c354424684`
  is the verified reference for a full-grid corpus and selected deep PDP.
- Existing shared retail adapters are candidates, not automatic fits; retailer-
  specific market, identity, pagination, and provider semantics remain local.

## Active Objective

Success implement one complete Space NK brand corpus route, dogfood it with one
authorized representative brand, route the validated diff through a
different-vendor delegated review-and-patch pass, adjudicate the return, and
land the lane through the repository PR workflow.

## Exact Next Authorized Action

1. Bind an isolated clean receiver at exact current `origin/main`; prove repo,
   branch, HEAD, writable root, dirty state, and one writer.
2. Re-run source loading and return `SOURCE_CONTEXT_READY` or the precise block.
3. Bind the planned success signals and establish a pre-change absence/baseline.
4. Freshly inspect official authorization and Space NK's US brand/grid/PDP/
   review source behavior before choosing filenames or provider mechanics.
5. Implement the smallest complete retailer-local route and only the necessary
   shared deltas; run deterministic tests and one full-brand dogfood.
6. Commission independent different-vendor review-and-patch at the immutable
   validated revision; adjudicate and revalidate any patch.
7. Commit, push, PR, observe checks, and self-merge only when current guards
   permit.

## Authority And Source Ledger

- `AGENTS.md`, `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/decision-routing.md`,
  `.agents/workflow-overlay/prompt-orchestration.md`,
  `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/validation.md`,
  `.agents/workflow-overlay/delegated-review-and-patch.md`, and
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`
  - Role: project authority, source loading, receiver isolation, review,
    validation, prompt, and lifecycle rules.
  - Load-bearing: yes.
  - Compare target: current receiver checkout; reread required.
  - Last checked: 2026-07-24 at authoring base.
  - Reuse rule: current overlay wins.
- `forseti-harness/source_capture/retail_capture_profiles.py`,
  `retail_grid_projection.py`, `retail_pdp_content.py`,
  `retail_pdp_projection.py`, and
  `adapters/cloakbrowser_snapshot.py`
  - Role: shared capture, projection, PDP, identity, browser-reuse, and failure
    contracts.
  - Load-bearing: yes.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: follow real call sites and preserve cross-retailer invariants.
- `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py` and
  `run_source_capture_http_packet.py`
  - Role: available sanctioned packet routes.
  - Load-bearing: yes for route composition, no for assuming which route works.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: choose cheapest sufficient current route.
- REVOLVE source, runner, and tests at
  `85c87a7467a3f2e49df5ce95510c60c354424684`
  - Role: verified corpus/deep capture reference.
  - Load-bearing: yes for success semantics, no for Space NK facts.
  - Compare target: merge commit; ancestor of authoring base.
  - Last checked: 2026-07-24.
  - Reuse rule: transfer invariants only.
- Existing Sephora Summer Fridays grid implementation and tests
  - Role: alternate prior proof for Summer Fridays brand-grid identity and
    US-facing retail capture.
  - Load-bearing: no for Space NK implementation.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: never reuse Sephora DOM/parser assumptions.
- Optional REVOLVE dogfood root:
  `C:\tmp\forseti-revolve-summer-fridays-dogfood-20260723-resume-r14`
  - Role: local replay example.
  - Load-bearing: no.
  - Compare targets:
    - `run-receipt.json` SHA-256 `DE2EFFE98A430F79752917B1AC8A190EA44A4B02C0F66F2B618782F8CE34A0B7`
    - `corpus-receipt.json` SHA-256 `147E69779187167D717848703B917694772EF5A64514DC26B2C81BE526DAC7DB`
    - `deep-pdp.json` SHA-256 `4F9C2593D273E795F48E7E3F12FA2321FCD595CC0F46A89F2868BBE360FC4B17`
  - Last checked: 2026-07-24.
  - Reuse rule: ignore if absent/mismatched.

## Current Task And Workspace State

- Completed elsewhere: shared retail grid/PDP/packet machinery and verified
  retailer-specific routes for Sephora, Ulta, Target, Amazon, and REVOLVE.
- Completed reference: REVOLVE Summer Fridays 37/37 PDP corpus and selected deep
  review receipt at merge `85c87a74`.
- Not present at authoring base: Space NK market adapter, grid parser/projection,
  PDP parser, corpus verifier/runner, deep-review adapter, and focused tests.
- Not proven: Space NK route reachability, official proof brand, US/USD binding,
  pagination, product identity, provider, review depth, or corpus completeness.
- Authoring branch/base: `codex/beauty-retailer-expansion-handoffs` at
  `9d1e64b503abccd48611d31da07d3d124fdf6167`.

## Planned Success Contract (`PLANNED_NOT_OBSERVED`)

1. **Official-first admission**
   - Current brand-owned evidence must authorize Space NK before live capture.
   - Wrong-cause check: absent/contradictory evidence blocks before route work.
2. **Exact US/USD surface**
   - Requested/final/canonical route, region/country, currency, language where
     relevant, and product offers form one consistent US conjunction.
   - Forbidden: UK/international shell, converted display price, redirect, or
     loose split signals.
3. **Complete exact grid**
   - Pagination/continuation, declared or observed counts, placements, unique
     product IDs, duplicate rows, brand identity, and canonical PDP URLs
     reconcile.
   - Wrong-cause check: remove a late product and duplicate another; both fail
     at distinct completeness checks.
4. **One-to-one PDP corpus**
   - `N` unique grid products produce exactly `N` hash-valid, identity-bound
     US/USD PDP records; missing/extra/duplicate/stale rows make the corpus
     partial.
   - Repeat: interrupt/resume once and compare with a clean run.
5. **Selected deep reviews**
   - Select the largest verifiable review-count PDP; bind current provider,
     store/product, native order labels, continuation/pages, review IDs, URLs,
     and body hashes; capture up to 100 relevant/helpful and 100 recent when
     both orders are genuinely exposed.
   - Forbidden: invented orders, wrong product/provider, highlighted snippets
     substituted for main reviews, or completion with unresolved mismatches.
6. **No hidden transport state**
   - Default capture uses no VPN, explicit/ambient proxy, persisted profile, or
     cross-run storage. One shared in-memory browser is allowed when required.
   - Seed proxy/profile perturbations and prove the intended guards.
7. **Replayable dogfood**
   - One complete authorized brand produces honest grid/corpus/deep receipts
     with counts, hashes, residuals, transport, and failures.
   - Forbidden: universal Space NK reliability or scale claims.

Most plausible false success: copy REVOLVE's models, parse the first Space NK
brand page and one PDP, then mark complete without proving regional state,
pagination, identity, or actual review-provider bindings. Signals 2–6 reject it.

## Smallest-Complete Implementation Route

1. Confirm the greenfield baseline and current shared contracts.
2. Probe only the canonical authorized brand/grid and one representative PDP
   enough to select Direct HTTP versus rendered capture.
3. Add Space NK-local market, grid, PDP, corpus, and deep-provider modules only
   where source semantics require them.
4. Reuse shared packet/projection/browser/content helpers without weakening
   their existing retailer contracts.
5. Add a single corpus runner with honest failure/partial receipts and safe
   resume.
6. Add deterministic fixtures for positive, negative, near-miss, provider,
   pagination, market, identity, proxy/profile, and resume behavior.
7. Run one bounded complete brand dogfood to a new temporary root.

Do not split this into separate grid-only and single-PDP implementation cycles.
The commissioned unit is one complete, fully verifiable brand corpus.

## Validation And Delegated Patch

At minimum run:

```powershell
python -m pytest -p no:cacheprovider --basetemp <unique> tests/unit/test_retail_capture_profiles.py tests/unit/test_retail_grid_projection.py tests/unit/test_retail_pdp_content_cleaning_silver.py tests/unit/test_source_capture_cloakbrowser_snapshot.py tests/unit/test_revolve_capture.py <new-space-nk-tests> -q
git diff --check
```

Add current affected contract and broad gates after focused success. Preserve
actual exits/output and label skipped live work.

Then commission an independent different-vendor controller using the current
delegated-review-and-patch rules. Bind exact revision, clean reviewer worktree,
bounded changed files, dogfood receipts, and commands. Reviewer outputs are
claims until the implementation lane adjudicates them. The reviewer may patch
within scope but may not commit; design-level findings return
`NEEDS_ARCHITECTURE_PASS`; an empty finding set returns `NO_PATCH_REQUIRED`.

## Frozen Decisions

- Official authorization precedes probing.
- US/USD must be directly observed; no VPN/proxy/profile/login dependence.
- Full representative brand corpus plus one selected deep PDP is the proof unit.
- Space NK remains retailer-local unless shared behavior is provably required.
- Real block/partial outcomes remain visible.

## Mutable Questions

- Canonical US brand/PDP route and regional state.
- Direct versus rendered capture and safe browser reuse.
- Grid pagination/termination and stable product identity.
- Review provider, native order vocabulary, Q&A, and deep limits.
- Proof brand if Summer Fridays authorization is not current.

## Superseded / Dangerous-To-Reuse Context

- Space NK directory presence as proof of brand authorization: insufficient.
- REVOLVE/Sephora Summer Fridays parsers as Space NK implementation templates:
  unsafe.
- A successful first page or PDP as a complete retailer route: false.
- VPN reachability history from unrelated retailers: not part of this contract.

## Blockers And Risks

- Official authorization absent: stop and choose an evidenced alternative or
  return blocked.
- US route regionalizes without a source-visible conjunction: preserve the
  block; do not infer.
- Access control/login/CAPTCHA: stop without bypass.
- No trustworthy grid termination or provider identity: return
  `NEEDS_ARCHITECTURE_PASS`.

## Confirm-Don't-Trust Checklist

- Verify handoff path, authoring base ancestry, receiver revision/state, and
  writer isolation.
- Reconfirm whether any Space NK support appeared after authoring.
- Fresh-read official brand authorization and live retailer source.
- Bind market, identity, pagination, seller, provider, order, and transport from
  current evidence.
- Re-run all required tests, live proof, receipt replay, and delegated review.

## Receiver Return Contract

```yaml
load_outcome:
source_context_status:
receiver_binding:
success_contract:
official_authorization:
selected_brand:
implementation:
dogfood:
  grid:
  corpus:
  deep_reviews:
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

Space NK is the only greenfield member of this three-retailer expansion. Reuse
the verified shared spine aggressively, but bind every retailer-specific fact
from Space NK's current source rather than analogy.
