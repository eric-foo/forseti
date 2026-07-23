# Nordstrom Beauty Brand Corpus Success-Implementation Handoff v1

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Bounded implementation commission for a verified Nordstrom US brand-grid, complete PDP corpus, and selected deep-review capture.
use_when:
  - Dispatching Nordstrom as an established indie and mid-market beauty corpus route.
  - Completing the existing Nordstrom US preference, PDP aggregation, and review-window machinery.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
branch_or_commit: codex/beauty-retailer-expansion-handoffs based on 9d1e64b503abccd48611d31da07d3d124fdf6167
stale_if:
  - Nordstrom country preference, PDP projection, review posture, marketplace seller semantics, or shared corpus contracts change.
  - The selected proof brand is not currently company-authorized for the observed Nordstrom seller/listing.
authority_boundary: retrieval_only
```

## Commission Status And Forseti Prompt Preflight

This is an implementation-authorized cold handoff. It remains preparation-only
until a clean, exact, isolated receiver is proven.

```yaml
prompt_preflight:
  output_mode: file-write
  write_destination: bounded receiver implementation worktree, temporary dogfood evidence root, and per-lane PR
  template_kind: none
  input_prompt_source: docs/prompts/handoffs/nordstrom_beauty_brand_corpus_success_implementation_handoff_20260724_v1.md
  edit_permission: implementation-authorized
  targets: Nordstrom capture code and tests; shared retail seams only when required for complete behavior
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
- handoff_path: `docs/prompts/handoffs/nordstrom_beauty_brand_corpus_success_implementation_handoff_20260724_v1.md`
- authoring_base: `9d1e64b503abccd48611d31da07d3d124fdf6167`
- expected_dirty_state_including_handoff_file: authoring lane changed only the three commissioned retailer handoffs before commit; receiving implementation lane must be clean
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against current source before acting

Return exactly one load outcome before planning or editing: `REUSE`,
`PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`,
`BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.

## Goal Handoff

- **Long-term goal:** maintain a retailer panel capable of four truthful,
  product-level corpora for indie and mid-market beauty products when four
  authorized public listings exist.
- **Anchor goal:** complete Nordstrom's existing US PDP/review support into an
  exact brand-grid → every-grid-PDP → selected-deep-review corpus route.
- **Success signal:** one currently authorized representative brand completes
  a reconciled Nordstrom US/USD grid and every unique PDP; one review-rich PDP
  completes a provider-bound deep capture; seller posture, hashes, transport,
  residuals, tests, and independent review are all observable.

## Open Decision / Fork

- **Recommended first candidate:** Kosas, because Nordstrom currently exposes a
  substantial public Kosas assortment and the brand is representative of the
  intended established-indie/mid-market segment.
- **Required check:** current brand-owned evidence must confirm Nordstrom
  authorization for the selected product relationship.
- **Marketplace fork:** Nordstrom now includes marketplace inventory. The
  implementation must distinguish Nordstrom-owned/wholesale inventory from a
  marketplace seller and bind the observed seller. A Nordstrom host alone is
  not sufficient seller or authorization evidence.
- **Fallback:** select ILIA, OSEA, Nécessaire, RMS Beauty, True Botanicals, or
  another evidenced brand only after current official-first verification and a
  public review-depth check.
- **Owner boundary:** schema redesign, accepting unbound marketplace inventory,
  proxy dependence, or weakened corpus completeness requires owner direction.

## Drift Guard

- Nordstrom is not greenfield. Preserve its country-preference plugin, fail-
  closed US confirmation, aggregate PDP record, review-window observation, and
  existing tests where still truthful.
- Do not recode established PDP/review behavior merely to resemble REVOLVE.
- Do not count marketplace rows without exact seller identity and current brand
  authorization.
- No VPN, proxy, ambient proxy, persisted profile, login, or gate bypass.
- A populated brand page is not a complete grid until termination and duplicate
  behavior reconcile.
- Corpus completeness and selected deep-review completeness remain distinct.
- Off-retailer changes are read-only unless a shared defect blocks this exact
  outcome.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- Overlay policy: `.agents/workflow-overlay/source-loading.md`.
- Enter through the existing Nordstrom adapter, shared PDP content/projection,
  CloakBrowser runner, Nordstrom tests, and merged REVOLVE corpus reference.
- Already loaded here: repository sources at the authoring base and optional
  REVOLVE receipts; neither is authority in the receiving lane.
- Must load first: project instructions/overlay, then actual Nordstrom call
  graph and tests before choosing new files or abstractions.

### Earlier-decided concepts and behaviors

- Official brand authorization and exact seller identity precede admission.
- No-VPN US/USD is a conjunctive source observation, not a requested locale or
  dollar-looking price.
- REVOLVE merge `85c87a7467a3f2e49df5ce95510c60c354424684`
  supplies verified corpus/replay/deep-receipt patterns only.
- Nordstrom already has more deep PDP machinery than Credo or Space NK; the
  expected smallest complete move is grid/corpus orchestration plus any precise
  deep-review gap, not a new standalone PDP stack.

## Active Objective

Success implement one complete Nordstrom brand corpus route, prove it with one
bounded authorized brand, commission and adjudicate a different-vendor delegated
review-and-patch pass, and land the verified lane through the normal PR flow.

## Exact Next Authorized Action

1. Prove a clean isolated receiver at exact current `origin/main`, with one
   writer and a writable root.
2. Re-run source loading and declare `SOURCE_CONTEXT_READY` or stop.
3. Bind and pressure-test the planned `SUCCESS_CONTRACT`.
4. Freshly verify the proof brand, canonical brand route, seller posture,
   pagination, PDP shape, review provider, and native sort/continuation behavior.
5. Extend the existing Nordstrom stack into the smallest complete grid/corpus/
   deep runner and tests; run one bounded full-brand dogfood.
6. Dispatch independent different-vendor review-and-patch against an immutable
   revision and adjudicate every returned change.
7. Revalidate, commit, push, open/update the PR, observe required checks, and
   self-merge only when current guards permit.

## Authority And Source Ledger

- `AGENTS.md`, overlay README, source loading, decision routing, review lanes,
  delegated review patch, validation gates, and prompt orchestration
  - Role: current project workflow authority.
  - Load-bearing: yes.
  - Compare target: current receiver revision; reread required.
  - Last checked: 2026-07-24 at authoring base.
  - Reuse rule: current repository source wins.
- `forseti-harness/source_capture/adapters/nordstrom_country_preference.py`
  - Role: country-preference UI, US storefront confirmation, review-window and
    review-posture observation.
  - Load-bearing: yes.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: follow imports/callers before editing.
- `forseti-harness/source_capture/retail_pdp_content.py`,
  `retail_pdp_projection.py`, and `retail_capture_profiles.py`
  - Role: Nordstrom aggregate PDP content, strict projected record, identities,
    variants, media, reviews, omissions, and product-ID derivation.
  - Load-bearing: yes.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: do not fork these contracts without a demonstrated mismatch.
- `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`
  - Role: current Nordstrom country setup, PDP extraction, review posture, and
    failure preservation.
  - Load-bearing: yes.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: compose the corpus runner around proven behavior where possible.
- `forseti-harness/tests/unit/test_nordstrom_country_preference_wiring.py` and
  `test_nordstrom_pdp_content_standard.py`
  - Role: existing Nordstrom behavior and negative-path regression authority.
  - Load-bearing: yes.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: preserve and extend.
- REVOLVE source/runner/tests at merge `85c87a7467a3f2e49df5ce95510c60c354424684`
  - Role: corpus, resume, receipt, browser reuse, and deep-review reference.
  - Load-bearing: yes for semantics, no for Nordstrom DOM/provider details.
  - Compare target: merge commit; ancestor of authoring base.
  - Last checked: 2026-07-24.
  - Reuse rule: copy invariants, not constants or parsers.
- Optional REVOLVE dogfood root:
  `C:\tmp\forseti-revolve-summer-fridays-dogfood-20260723-resume-r14`
  - Role: replayable example only.
  - Load-bearing: no.
  - Compare targets:
    - `run-receipt.json` SHA-256 `DE2EFFE98A430F79752917B1AC8A190EA44A4B02C0F66F2B618782F8CE34A0B7`
    - `corpus-receipt.json` SHA-256 `147E69779187167D717848703B917694772EF5A64514DC26B2C81BE526DAC7DB`
    - `deep-pdp.json` SHA-256 `4F9C2593D273E795F48E7E3F12FA2321FCD595CC0F46A89F2868BBE360FC4B17`
  - Last checked: 2026-07-24.
  - Reuse rule: ignore if missing/mismatched.

## Current Task And Workspace State

- Completed: Nordstrom country-preference attempt, US storefront confirmation,
  aggregate PDP extraction/projection, product identity, variants/media/review
  fields, a recent-review posture, failure preservation, and focused tests.
- Partially completed: individual Nordstrom PDP and review-window capture.
- Not proven: complete brand grid and termination, one-to-one full PDP corpus,
  corpus resume/reconciliation, exact seller posture across the corpus, and a
  selected deep-review receipt matching the REVOLVE-level bar.
- Authoring branch/base: `codex/beauty-retailer-expansion-handoffs` at
  `9d1e64b503abccd48611d31da07d3d124fdf6167`.

## Planned Success Contract (`PLANNED_NOT_OBSERVED`)

1. **Official relationship and seller**
   - Given a candidate product, admission requires current brand-owned retailer
     evidence plus observed Nordstrom seller/fulfillment posture.
   - Forbidden: host-only authorization or collapsing marketplace and Nordstrom
     wholesale inventory.
   - Wrong-cause check: mutate seller identity and independently remove brand
     evidence; each must fail at its own boundary.
2. **Complete exact brand grid**
   - Reconcile declared/observed pages or continuation, placements, unique
     Nordstrom product IDs, duplicate rows, brand identity, canonical URLs, and
     termination.
   - Wrong-cause check: missing later-page product and duplicated product each
     fail with distinct residuals.
3. **US/USD exact PDP**
   - Every grid product maps to one requested/final/canonical Nordstrom product
     ID with US/USD confirmation, selected variant/offer, brand, and seller.
   - Forbidden: country preference attempted but not confirmed, wrong product,
     currency conflict, or access shell.
4. **One-to-one corpus**
   - `N` unique grid IDs produce exactly `N` hash-valid PDP records and a
     complete receipt with no identity/coverage residual.
   - Repeat: interrupted resume equals clean run and rejects stale/incompatible
     packets.
5. **Selected deep reviews**
   - The largest verifiable review-count PDP captures provider-bound pages up to
     100 native helpful/relevant and 100 native recent reviews when those orders
     exist, with exact ordering, continuation, IDs, URLs, hashes, and shortfalls.
   - Forbidden: highlighted-review cards substituted for the main list, invented
     ordering, unbound provider response, or false completion.
6. **No hidden transport state**
   - One shared in-memory browser may be reused, but no persisted profile,
     explicit/ambient proxy, or cross-run state may be used.
   - Seed proxy/profile perturbations and prove the intended guards.
7. **Dogfood truth**
   - One complete authorized brand produces replayable run/grid/corpus/deep
     receipts and honestly labels any unsupported optional field.
   - Forbidden: broad Nordstrom scale/reliability claim from one proof brand.

Most plausible false success: wrap the existing Nordstrom single-PDP machinery
in a loop over the first visible grid rows while ignoring pagination, duplicate
IDs, marketplace seller drift, or missing later PDPs. Signals 1–5 reject it.

## Smallest-Complete Implementation Route

1. Preserve the focused Nordstrom baseline and identify the exact missing
   grid/corpus/deep seams.
2. Add Nordstrom-local brand-grid parsing, canonical URL/product-ID projection,
   and truthful termination.
3. Compose existing US preference and PDP aggregate extraction in one shared
   in-memory browser lifecycle where live evidence requires rendered capture.
4. Add corpus reconciliation, honest receipts, and safe resume.
5. Extend review capture only for the gap between current rendered-window
   posture and the selected deep-review success signal; do not replace proven
   PDP content unnecessarily.
6. Capture seller posture in grid/PDP/corpus identity and reject contradictions.
7. Run one complete authorized brand dogfood to a new temporary root.

## Validation And Delegated Patch

At minimum run:

```powershell
python -m pytest -p no:cacheprovider --basetemp <unique> tests/unit/test_nordstrom_country_preference_wiring.py tests/unit/test_nordstrom_pdp_content_standard.py tests/unit/test_retail_capture_profiles.py tests/unit/test_retail_grid_projection.py tests/unit/test_retail_pdp_content_cleaning_silver.py tests/unit/test_source_capture_cloakbrowser_snapshot.py <new-nordstrom-tests> -q
git diff --check
```

Run the current repository's affected contract and broad gates after focused
success. Report every planned signal and live step honestly.

Then commission a different-vendor controller under the current delegated
review-and-patch contract. The review binds the exact immutable revision,
changed files, current dogfood receipts, and validation commands. It may return
an uncommitted bounded patch, `NO_PATCH_REQUIRED`, or
`NEEDS_ARCHITECTURE_PASS`; it may not commit, push, merge, or expand scope.
The implementation lane adjudicates and revalidates before landing.

## Frozen Decisions

- Existing Nordstrom capabilities are reuse candidates, not throwaway code.
- Marketplace inventory is a distinct seller posture and never silently equals
  Nordstrom-owned inventory.
- No VPN/proxy/profile/login dependence.
- One full representative brand is the proof unit.
- Shared abstraction requires a current completeness defect it uniquely fixes.

## Mutable Questions

- Canonical Nordstrom brand-grid route and full-grid termination.
- Whether one country setup can be safely reused across the whole browser run.
- Current review provider, native sort labels, continuation, and response API.
- Proof brand after official-first and seller checks.

## Superseded / Dangerous-To-Reuse Context

- Nordstrom's large brand directory as proof that every listing is Nordstrom-
  owned or brand-authorized: false after Nordstrom Marketplace.
- Existing single-PDP/review tests as proof of corpus completeness: insufficient.
- REVOLVE Yotpo/store/style constants: retailer-specific and unsafe to copy.

## Blockers And Risks

- Seller or authorization cannot be bound: stop before corpus admission.
- Country preference cannot be confirmed conjunctively: preserve diagnostic
  packet and return blocked.
- Grid termination cannot be proven: return `NEEDS_ARCHITECTURE_PASS`.
- Review provider/order cannot be bound: do not claim deep-review completion.

## Confirm-Don't-Trust Checklist

- Verify packet, base ancestry, receiver identity/state, and no other writer.
- Re-read the entire current Nordstrom call graph needed by the chosen route.
- Fresh-check official authorization, seller, canonical URLs, market, provider,
  pagination, and sort vocabulary.
- Re-run focused/shared/broad validation and receipt replay.
- Stop on authority conflict, unknown writer, or non-reconstructable evidence.

## Receiver Return Contract

```yaml
load_outcome:
source_context_status:
receiver_binding:
success_contract:
official_authorization:
selected_brand:
seller_posture:
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

The Nordstrom commission is a completion job around substantial existing PDP
machinery. The main novel risk is seller truth plus complete grid-to-PDP
reconciliation, not merely extracting another product page.
