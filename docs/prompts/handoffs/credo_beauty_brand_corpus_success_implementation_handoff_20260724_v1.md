# Credo Beauty Brand Corpus Success-Implementation Handoff v1

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Bounded implementation commission for a verified Credo US brand-grid, complete PDP corpus, and selected deep-review capture.
use_when:
  - Dispatching the next retailer-corpus implementation lane after the verified REVOLVE corpus.
  - Extending the existing Credo US/USD PDP assertion into an end-to-end brand corpus.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/decision-routing.md
branch_or_commit: codex/beauty-retailer-expansion-handoffs based on 9d1e64b503abccd48611d31da07d3d124fdf6167
stale_if:
  - The Credo market adapter, shared retail capture contracts, or REVOLVE reference implementation materially changes.
  - Credo no longer exposes a public US brand/PDP surface or the selected proof brand is not currently company-authorized for Credo.
authority_boundary: retrieval_only
```

## Commission Status And Forseti Prompt Preflight

This is an implementation-authorized cold handoff. It is preparation-only until
the receiving lane proves its exact checkout, clean writable worktree, and
single-writer ownership. The handoff transfers hypotheses and constraints, not
authority for strict claims.

```yaml
prompt_preflight:
  output_mode: file-write
  write_destination: bounded receiver implementation worktree, temporary dogfood evidence root, and per-lane PR
  template_kind: none
  input_prompt_source: docs/prompts/handoffs/credo_beauty_brand_corpus_success_implementation_handoff_20260724_v1.md
  edit_permission: implementation-authorized
  targets: Credo-specific capture code and tests; shared retail seams only when required for complete behavior
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
- handoff_path: `docs/prompts/handoffs/credo_beauty_brand_corpus_success_implementation_handoff_20260724_v1.md`
- authoring_base: `9d1e64b503abccd48611d31da07d3d124fdf6167`
- expected_dirty_state_including_handoff_file: authoring lane changed only the three commissioned retailer handoffs before commit; receiving implementation lane must be clean
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against current source before acting

Return exactly one load outcome before planning or editing: `REUSE`,
`PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`,
`BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.

## Goal Handoff

- **Long-term goal:** maintain a panel broad enough to obtain four truthful,
  product-level retailer corpora for indie and mid-market beauty products when
  four authorized public listings actually exist.
- **Anchor goal:** extend Credo's existing US PDP support into the smallest
  complete, no-VPN Credo brand-grid → every-grid-PDP → selected-deep-review
  capture route.
- **Success signal:** one currently authorized representative beauty brand is
  captured from a complete, reconciled Credo US/USD grid through every unique
  PDP, with one high-review PDP captured deeply, hash-verifiable receipts,
  deterministic regression tests, and a completed different-vendor
  review-and-patch adjudication.

## Open Decision / Fork

- **Decision:** which current Credo brand and review substrate should prove the
  route.
- **Recommended first candidate:** Tower 28, because the existing Credo fixture
  and market adapter already bind a Tower 28 PDP and Yotpo-shaped review content.
- **Required check:** a brand-owned current source must independently confirm
  Credo authorization before any live grid/PDP capture. A Credo listing alone
  does not prove authorization.
- **Fallback:** if Tower 28 authorization, grid identity, or sufficient public
  review depth is not provable, select another Credo-listed indie brand only
  after the same official-first check. Record the substitution and evidence.
- **Owner boundary:** the implementation lane may select an evidenced proof
  brand; a shared schema redesign, proxy dependence, login requirement, or
  weakened completeness definition returns to the owner.

## Drift Guard

- Do not treat this as a greenfield retailer: preserve and reuse the existing
  Credo US/USD PDP assertion where it remains truthful.
- Do not infer brand authorization from Credo search or listing presence.
- Do not use a VPN, explicit proxy, ambient environment proxy, persisted browser
  profile, login, CAPTCHA bypass, or marketplace substitute.
- Do not call a transport success, rendered shell, nonempty grid, or selected
  PDP a complete corpus.
- Do not require deep reviews for every PDP. Corpus completeness means exact
  grid-to-PDP coverage; the selected deep PDP separately proves review depth.
- Do not loosen shared packet, market, identity, hash, or residual rules to
  admit Credo.
- Do not modify Sephora, Ulta, Target, Amazon, REVOLVE, Nordstrom, or Space NK
  behavior except for a genuinely shared correction required by this outcome.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- Overlay policy: `.agents/workflow-overlay/source-loading.md`.
- Enter the ladder through the Credo adapter/tests and the merged REVOLVE
  corpus implementation named below.
- Already loaded here: current repository sources at authoring base and the
  REVOLVE receipts; these are weak orientation only.
- Must load first: `AGENTS.md`, overlay README, decision routing, relevant
  implementation/review/validation sections, then the actual Credo and shared
  runtime sources.
- The receiver must stop source loading once authority, invariants, target
  seams, and validation dependencies are bound.

### Earlier-decided concepts and behaviors

- Official-first retailer admission precedes probing; retailer presence is not
  authorization. Verify against the current brand-owned source.
- No-VPN ordinary US-facing `.com` and USD are required; a correctly typed block
  is preferable to fake success.
- REVOLVE commit `85c87a7467a3f2e49df5ce95510c60c354424684`
  is the reference for corpus reconciliation, receipt honesty, shared browser
  reuse, and selected deep review capture—not a file-copy instruction.
- The prior REVOLVE live result reported 37/37 PDPs, a complete corpus receipt,
  and a selected 100-most-relevant + 100-most-recent review substrate. Re-read
  its source and receipts before relying on those claims.

## Active Objective

Success implement one complete Credo brand corpus route, validate it through a
bounded live dogfood run, commission an independent different-vendor
review-and-patch pass, adjudicate its return, and land the verified lane through
the repository PR workflow.

## Exact Next Authorized Action

1. Bind a clean isolated receiver to current `origin/main`; record repo, branch,
   HEAD, dirty state, writable root, and absence of a concurrent writer.
2. Re-run progressive source loading and declare `SOURCE_CONTEXT_READY`, or stop
   with the exact missing/stale source.
3. Write a compact `SUCCESS_CONTRACT` from the planned signals below and
   pressure-test its near-miss and wrong-cause cases.
4. Inspect Credo's current public grid/PDP/review substrates and current
   brand-owned authorization evidence before choosing implementation seams.
5. Implement the smallest complete Credo-specific route, tests, runner, receipts,
   and bounded live proof.
6. After validation, enter de-correlated delegated review-and-patch. The reviewer
   may patch only the bounded diff, must not commit, and the home lane adjudicates
   every returned change.
7. Re-run affected validation, commit, push, open/update the lane PR, observe
   required checks, and self-merge only when current project guards allow it.

## Authority And Source Ledger

- `AGENTS.md` and `.agents/workflow-overlay/README.md`
  - Role: project behavior and overlay routing.
  - Load-bearing: yes.
  - Compare target: current receiver checkout; reread required.
  - Last checked: 2026-07-24 at authoring base.
  - Reuse rule: never substitute packet summary.
- `.agents/workflow-overlay/source-loading.md`,
  `decision-routing.md`, `review-lanes.md`, `delegated-review-patch.md`,
  `validation-gates.md`, and `prompt-orchestration.md`
  - Role: receiver, review, validation, and lifecycle mechanics.
  - Load-bearing: yes.
  - Compare target: current receiver checkout; targeted reread required.
  - Last checked: 2026-07-24 at authoring base.
  - Reuse rule: current overlay wins over generic skill mechanics.
- `forseti-harness/source_capture/adapters/credo_us_market.py`
  - Role: existing fail-closed Credo PDP/US/USD/canonical-product conjunction.
  - Load-bearing: yes.
  - Compare target: receiver revision; current history includes `2c3e306b`.
  - Last checked: 2026-07-24.
  - Reuse rule: preserve unless fresh source proves it stale.
- `forseti-harness/runners/run_source_capture_http_packet.py` and
  `forseti-harness/tests/unit/test_credo_us_market_wiring.py`
  - Role: existing Credo runner wiring, Tower 28/Yotpo-shaped fixture, negative
    market tests, and PDP projection proof.
  - Load-bearing: yes.
  - Compare target: current receiver revision.
  - Last checked: 2026-07-24.
  - Reuse rule: extend rather than duplicate.
- `forseti-harness/source_capture/revolve_*.py`,
  `forseti-harness/runners/run_revolve_brand_corpus.py`, and
  `forseti-harness/tests/unit/test_revolve_capture.py`
  - Role: merged reference implementation and regression shape.
  - Load-bearing: yes for success semantics, no for Credo DOM/provider facts.
  - Compare target: merge commit
    `85c87a7467a3f2e49df5ce95510c60c354424684`, which was an ancestor of the
    authoring base.
  - Last checked: 2026-07-24.
  - Reuse rule: copy invariants, not retailer assumptions.
- `C:\tmp\forseti-revolve-summer-fridays-dogfood-20260723-resume-r14`
  - Role: optional local dogfood example.
  - Load-bearing: no; implementation source remains available without it.
  - Compare targets:
    - `run-receipt.json` SHA-256 `DE2EFFE98A430F79752917B1AC8A190EA44A4B02C0F66F2B618782F8CE34A0B7`
    - `corpus-receipt.json` SHA-256 `147E69779187167D717848703B917694772EF5A64514DC26B2C81BE526DAC7DB`
    - `deep-pdp.json` SHA-256 `4F9C2593D273E795F48E7E3F12FA2321FCD595CC0F46A89F2868BBE360FC4B17`
  - Last checked: 2026-07-24.
  - Reuse rule: ignore if absent or hash-mismatched; never reconstruct.

## Current Task And Workspace State

- Completed: Credo exact PDP route validation, canonical product binding,
  US/USD confirmation, raw packet preservation, and a Tower 28 fixture with
  displayed review content.
- Partially completed: Credo PDP capture/projection.
- Not proven: complete Credo brand grid, pagination/termination, every-grid-PDP
  corpus reconciliation, shared browser lifecycle for a corpus run, and
  provider-bound deep review capture.
- Authoring branch: `codex/beauty-retailer-expansion-handoffs`.
- Authoring base: `9d1e64b503abccd48611d31da07d3d124fdf6167`.
- Related proof: merged REVOLVE PR #1320 at `85c87a74`.

## Planned Success Contract (`PLANNED_NOT_OBSERVED`)

1. **Official-first admission**
   - Given a candidate proof brand, when the retailer route is admitted, then a
     current brand-owned source names Credo or otherwise proves the relationship.
   - Forbidden: treating a Credo listing, search result, or stale packet as
     authorization.
   - Wrong-cause check: remove/contradict the official evidence and confirm
     admission fails before capture starts.
2. **Exact complete grid**
   - Given the canonical Credo brand route, when grid capture terminates, then
     declared/observed pagination, unique products, placements, duplicates, and
     canonical PDP URLs reconcile.
   - Forbidden: early-stop completeness, duplicate inflation, unrelated brand
     rows, access shell, or empty success.
   - Wrong-cause check: delete a later-page product and separately duplicate one
     product; both mutations must make completeness fail for the right reason.
3. **US/USD product identity**
   - Given every unique grid product, when its PDP packet is admitted, then
     requested/final/canonical identity, brand, product identifier, US country,
     USD currency, and source-visible offers agree.
   - Forbidden: accepting split loose signals, redirects to another product,
     SGD/non-US state, or a retailer shell.
4. **One-to-one corpus**
   - Given a complete grid of `N` unique products, when the run closes, then
     exactly `N` hash-valid PDP records exist and every grid identity maps to one
     and only one PDP identity.
   - Forbidden: missing, extra, duplicated, stale-resumed, or cross-brand PDPs;
     `complete` with residuals.
   - Repeat: interrupt and resume once; resumed output must equal a clean run and
     refuse incompatible/stale artifacts.
5. **Selected deep reviews**
   - Given the corpus PDP with the largest verifiable review count, when deep
     capture runs, then the real provider/store/product binding is exact and it
     captures up to 100 native most-relevant and 100 native most-recent reviews
     when both orders exist, with page/order/URL/body hashes and honest shortfall
     residuals.
   - Forbidden: wrong product/store, invented order labels, HTML-only declared
     counts, ambient proxy inheritance, or `complete` after response mismatch.
6. **No hidden transport state**
   - Given an ambient proxy variable and an available persisted browser profile,
     when the default corpus route runs, then neither is used; receipts state the
     observed transport/profile posture.
   - Wrong-cause check: seed `HTTPS_PROXY` and a profile path independently and
     prove the intended guards—not an earlier unrelated validation—reject or
     bypass them.
7. **Owner-visible dogfood proof**
   - Given one bounded authorized brand, when the live run completes, then
     receipts make grid count, PDP count, deep candidate, review counts,
     transport posture, failures, residuals, and hashes independently replayable.
   - Forbidden: claiming broad Credo reliability, scale, or production readiness
     from one brand.

Most plausible false success: reuse the current single-PDP fixture, add a
nonempty brand parser, and call the retailer supported without proving complete
pagination, one-to-one PDP coverage, or provider-bound review depth. Signals
2–5 must reject it.

## Smallest-Complete Implementation Route

1. Preserve the existing direct-PDP market assertion and test baseline.
2. Determine whether Credo's current brand grid and PDP corpus can remain Direct
   HTTP or require rendered capture. Select the cheapest sufficient route from
   current evidence; do not introduce a browser by analogy.
3. Add Credo-local grid parsing/projection and termination rules.
4. Reuse shared retail PDP cleaning/projection only where its contracts exactly
   fit; add Credo-local parsing for source-specific identity or fields.
5. Add a Credo corpus verifier/runner with honest partial receipts and safe
   resume semantics.
6. Discover and bind the current review provider. Reuse shared Yotpo mechanics
   only if live code/data proves Yotpo and the exact store/product keys.
7. Run one bounded full-brand dogfood capture to a new temporary root. Do not
   overwrite or retrofit historical packets.

## Validation And Delegated Patch

Run focused tests first, then directly affected shared tests, then the repository
required gates. At minimum include:

```powershell
python -m pytest -p no:cacheprovider --basetemp <unique> tests/unit/test_credo_us_market_wiring.py tests/unit/test_retail_capture_profiles.py tests/unit/test_retail_grid_projection.py tests/unit/test_retail_pdp_content_cleaning_silver.py tests/unit/test_source_capture_cloakbrowser_snapshot.py <new-credo-tests> -q
git diff --check
```

Record every success signal as `passed`, `failed`, `blocked`, or `not_run`.
Tests alone do not prove the live route.

After local validation, route an independent different-vendor controller through
the current delegated-review-and-patch contract. Bind the exact branch revision,
clean reviewer worktree, changed-file scope, validation commands, and dogfood
receipts. The reviewer returns findings first and either an uncommitted bounded
patch, `NO_PATCH_REQUIRED`, or `NEEDS_ARCHITECTURE_PASS`. The implementation
lane independently adjudicates and revalidates every kept change before landing.

## Frozen Decisions

- No VPN/proxy/profile/login dependence.
- One complete representative brand, not a smoke-test slice.
- Exact corpus coverage and one selected deep PDP are separate claims.
- Optional PDP fields may be honestly absent; identity/coverage defects cannot.
- New shared abstraction requires proof that a complete Credo outcome remains
  false or materially fragile without it.

## Mutable Questions

- Canonical Credo brand-grid route and termination substrate.
- Direct HTTP versus one shared in-memory browser for grid/PDP capture.
- Current review provider, sort vocabulary, pagination, and Q&A exposure.
- Best officially authorized proof brand if Tower 28 is not admissible.

## Superseded / Dangerous-To-Reuse Context

- Retailer listing presence as proof of authorization: rejected after the Ulta
  Summer Fridays misclassification.
- REVOLVE filenames/provider constants as a generic template: dangerous; only
  its verified invariants and receipt semantics transfer.
- Passing the existing Credo single-PDP tests as proof of a brand corpus:
  insufficient.

## Blockers And Risks

- Official authorization absent or ambiguous: stop before live corpus capture.
- Login/CAPTCHA/access-control gate: preserve the typed block and return it.
- No trustworthy grid termination signal: return `NEEDS_ARCHITECTURE_PASS`
  rather than invent completeness.
- Review substrate cannot bind provider/product/order: capture PDP corpus
  honestly but do not claim deep-review success.

## Confirm-Don't-Trust Checklist

- Verify packet path, receiver branch/HEAD/dirty state, and authoring base ancestry.
- Re-read every load-bearing source at the receiver revision.
- Confirm Credo authorization from a current brand-owned source.
- Confirm actual canonical routes, provider, market signals, and seller posture.
- Re-run validation; do not inherit the REVOLVE or handoff pass claims.
- If material drift is safe to re-derive, return `STALE_REREAD_REQUIRED`; if it
  conflicts with authority or another writer, return `BLOCKED_DRIFT`.

## Receiver Return Contract

Return:

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

Credo already has a valuable fail-closed PDP market seam. The commissioned work
is to complete the retailer route around it, not to replace proven behavior or
declare success from a single product.
