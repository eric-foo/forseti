# Handoff Packet — Target then Amazon Canonical PDP Content

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet
scope: >
  Cold-reader handoff commissioning two sequential implementation lanes: Target
  canonical PDP content first, then Amazon canonical PDP content, benchmarked
  against the landed Sephora and Ulta content routes and bounded by each
  retailer's already-admitted capture envelope.
use_when:
  - Starting the Target canonical PDP content lane.
  - Starting the Amazon canonical PDP content lane after Target lands.
  - Deciding what a retailer content flip must preserve before it is admitted.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
branch_or_commit: >
  Authored against 798b94c48f608dd62bb89faa33cb506d20f5b9f1 (PR #1231). Phase 1
  landed as 6e64b35ffc63e4a9848dd2a4c309dbb0e8898ff5 (PR #1238); this packet was
  revised against that result.
stale_if:
  - The Retail/PDP content cleaning contract changes its content-vs-raw retention rule.
  - A later lane lands an Amazon content schema, making Phase 2 a delta rather than a build.
  - The Amazon pre-v3 capture envelope is renegotiated with the owner.
```

## Phase Status

- **Phase 1 (Target): COMPLETE.** Landed as
  `6e64b35ffc63e4a9848dd2a4c309dbb0e8898ff5` (PR #1238). The route is
  `retail_pdp_target_aggregate_content_v1` /
  `retail_pdp_target_aggregate_parser_v1`; `target_pdp_aggregate` is
  content-eligible and defaults to `content` retention. Evidence:
  `docs/research/forseti_target_canonical_content_capture_proof_v0.md`.
  Do not rebuild it. Read the Phase 1 corrections below before starting Phase 2.
- **Phase 2 (Amazon): NOT STARTED.** Startable now that Phase 1 has landed,
  after the concurrent-writer reconciliation below.

## Phase 1 Corrections — Read Before Phase 2

Phase 1 disproved parts of this packet as originally written. The corrections
generalize, and Amazon is likely to repeat them.

- **"Build from `__NEXT_DATA__` CDUI state" was incomplete.** Target's SSR
  hydrates exactly one CDUI datasource (`ProductDetailWebDatasourceCore`). The
  price, offer, fulfillment, variation, and store datasources are declared in the
  layout and left `null`; `current_retail`, `"price"`, `availability_status`, and
  `child_tcin` occur zero times in the whole document. The offer had to come from
  the rendered DOM. **Expect the same split on Amazon**: plan for page state plus
  rendered DOM from the start, and inventory declared-but-unhydrated modules
  rather than omitting them.
- **A capture profile's product literal can make it unsatisfiable.**
  `target_pdp_aggregate` required `BYOMA Liptide Lip Mask` in visible text — the
  brand-grid fixture product, which never appears on a Target PDP. The profile
  had never qualified a real PDP capture, and the existing Target PDP packets in
  the lake were captured with no profile at all (`pin_confirmed: null`).
  **Check `amazon_pdp_aggregate` for the same defect before assuming it can
  qualify a capture.**
- **Profile requirements merge as a union, not an override.** A CLI
  `--require-visible-text` cannot relax a profile's product pin. "Prove the route
  live against one named product" is only achievable when the profile pins that
  product; otherwise prove offline against the pinned packet.
- **A delegated de-correlated review found three defect classes worth applying to
  Amazon from the start** (PR #1238, second commit): extract price from the
  target product's own module rather than page-globally; scan for session secrets
  by key name plus a length floor, never length alone (a bare-word cookie value
  collided with ordinary product copy and refused legitimate captures); and fail
  loud on any hydrated datasource the parser does not retain instead of reporting
  it as observed.
- **Doc drift is real.** PR #1231 raised Ulta content to v2 in code without
  touching the Retail/PDP contract census. Phase 1 reconciled it. Re-check the
  contract against code before trusting it.

## Load Contract

- packet_version: 2
- mode: max
- updated_at: 2026-07-21 (revised after Phase 1 landed)
- updated_by_lane: Target/Amazon canonical content commission lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- required_revision: `6e64b35ffc63e4a9848dd2a4c309dbb0e8898ff5` (Phase 1, PR #1238)
- revision_mode: `ancestor` — start from current `origin/main`; verify with
  `git merge-base --is-ancestor 6e64b35ffc63e4a9848dd2a4c309dbb0e8898ff5 HEAD`
- source-loading_mode: repo-overlay-bound
- load_rule: confirm-don't-trust; reread the named sources and re-verify the
  named packets before acting
- durable_destination_status: revised in place; this packet remains the single
  Target-then-Amazon commission record

`798b94c4` landed the Ulta PowerReviews adapter, Ulta content v2, and the
Sephora three-role v4 target; `6e64b35f` landed Phase 1 on top of it. A lane that
starts below `6e64b35f` lacks both the benchmarks and the Target route.

## Goal Handoff

- long_term_goal: Capture the deepest useful retailer product, review,
  aggregate, and Q&A evidence at the lowest defensible request footprint, and
  retain it as truthful retailer-local canonical content.
- active_goal: Flip Target, then Amazon, from `raw_unflipped` to a canonical
  content record without adding a single request beyond each retailer's already
  admitted capture envelope.
- success_signal: Each lane either lands a retailer-local content record proven
  against its named packet with raw-to-content equivalence, explicit loss
  ledger, and fail-loud raw fallback, or returns a typed blocker naming exactly
  which required information the source does not expose.

## Receiver Preflight

- Output mode: `file-write`. Two sequential implementation branches from current
  `origin/main`, each landing through its own PR.
- Edit permission · targets · branch: `implementation-authorized`, scoped per
  phase to the retailer's extractor, record model, runner wiring, focused tests,
  and the directly affected Retail/PDP contract rows. Do not open both lanes at
  once.
- One commission may authorize both phases. They remain separate sequential
  branches and PRs; Amazon does not start until Target lands on `main`.

## Naming Convention — Resolve Before First Edit

This commission was requested as `retail_pdp_target_content_v1` and
`retail_pdp_amazon_content_v1`. That is shorthand. The repo-native convention is
`retail_pdp_<retailer>_aggregate_content_vN` with a paired
`retail_pdp_<retailer>_aggregate_parser_vN`, as used by every landed route
(`retail_pdp_projection.py:27-42`). Use the repo-native names. Do not introduce a
second naming family.

## Benchmarks — Verified At `798b94c4`

These are quality benchmarks, not parity targets. A retailer may legitimately
lack what another exposes.

### Sephora

- Content: `retail_pdp_sephora_aggregate_content_v3` /
  `retail_pdp_sephora_aggregate_parser_v3` (`retail_pdp_projection.py:28-29`).
- Companion: `sephora_bazaarvoice_onboarding_v4` — three response roles
  (bounded Most-Answers Q&A; non-incentivized Most Helpful carrying combined
  `Stats`/`FilteredStats`; non-incentivized Most Recent with the bounded 30-day
  continuation and a native `last_seen_review_id` anchor). v4 replaced an
  eight-response v3 route: three response documents versus eight.
- Live proof packet: `01KY25FZCPVRHF6XEPYDEDATN0` (named at
  `retailer_information_extraction_standard_v0.md:176`).

Freshness re-check performed in this work unit: lake packet
`01KY289TYGFGZ3V3QDYT9AVPJ4` (`F:\forseti-data-lake\raw\7c1\...`) is the same
route, same product `P420652`, and same parent lineage as the proof packet,
captured 2026-07-21T11:52:11Z — 49 minutes after it. Both summaries independently
read `record_kind: sephora_bazaarvoice_onboarding_summary_v4`,
`content_qualification.status: passed`, `response_documents: 3`,
`three_response_roles_present: true`,
`summary_duplicates_review_or_answer_bodies: false`,
`combined_statistics_present: true`, `recent_window_coverage_proven: true`,
`age_bucket_vocabulary_exact: true`.

Scope of that claim: this is a direct read of both lake summaries performed
while authoring this handoff. `01KY289TYGFGZ3V3QDYT9AVPJ4` appears in no commit,
doc, or derived record anywhere in the repository, and no comparison receipt
exists for it. Treat it as a corroborating live observation that the v4 route
still qualifies, not as a recorded proof artifact. If you need a citable
comparison, produce one; do not cite this paragraph as one.

### Ulta

- Content: `retail_pdp_ulta_aggregate_content_v2` /
  `retail_pdp_ulta_aggregate_parser_v2` (`retail_pdp_projection.py:40-41`).
- Companion: `ulta_powerreviews_onboarding_v1`
  (`ulta_onboarding_capture.py:42-43`), Most Helpful / Newest roles plus bounded
  Q&A.
- Live proof packet: `01KY20GH02FH8CCSAV2D6M9NKR`.
- Genuine source limitations, recorded at
  `docs/research/forseti_ulta_powerreviews_review_capture_proof_v0.md` §5 "Loss
  Ledger and Non-Claims": bounded 100+100 window of 672 declared reviews with a
  25-row response cap; no source-proven non-incentivized filter (unfiltered
  baseline preserved with per-row `disclosure_code`); syndication filter
  unverified; no aggregate reviewer demographic distributions with denominators;
  linked media bytes not fetched; and a preserved rendered-671-versus-
  structured-672 count disagreement that was deliberately not reconciled.

Ulta is the benchmark precisely because it is honest about what PowerReviews
does not give. Reproduce that discipline, not a field count.

## Frozen Shared Rules

These bind both phases.

- Preserve the deepest useful target-bound information. Compactness never
  authorizes dropping valuable rows. Recommendation, footer, or unrelated-product
  facts must not bind to the target.
- Retain content directly during capture. A successful content-mode run hashes
  and discards the declared disposable rendered DOM and visible text; it does not
  write a full DOM and then discard it, and there is no Projection packet,
  sidecar writer, post-hoc runner, or third qualification packet.
- Preserve raw evidence and exit nonzero when pinning, identity binding,
  extraction, reconstruction, or qualification fails. A failed gate keeps every
  supplied original artifact and returns its typed nonzero failure.
- Add no review, API, or media requests beyond the retailer's already admitted
  capture envelope.
- Keep schemas retailer-local. Do not invent a universal
  Sephora/Ulta/Target/Amazon parser and do not force cosmetic version parity.
  Renaming a current `v1` to `v2` without a real schema or retention change is a
  misleading label and is not allowed.
- Existing raw packets are append-only historical evidence.

Content-mode plumbing already exists in
`forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`:
`--retention-mode {content,raw}` at L1451-1460, the content-eligible profile set
at L1759-1772, per-retailer extraction-spec dispatch at L1780-1826, and the
retention admission gate at L626-661. Note that `amazon_pin_failure` and
`target_pin_failure` are already wired into that admission gate (L634-635) even
though neither profile is content-eligible yet. Extend the existing seam; do not
build a parallel one.

## Phase 1 — Target (landed)

Complete at `6e64b35ffc63e4a9848dd2a4c309dbb0e8898ff5` (PR #1238). The route
builds `retail_pdp_target_aggregate_content_v1` from the Target-owned
`__NEXT_DATA__` CDUI core datasource plus the rendered offer and review regions,
leaves the `target_bazaarvoice_onboarding` companion untouched as the owner of
exact review and Q&A bodies, and retains body-free review identity only.

What it proved, and what a Phase 2 reader should carry:

- reconstruction 29/29 against parent packet `01KXR823YS3V5M9E01QXP71ETC`
  (TCIN `80184023`); qualification `match` / exit 0, and `drift` / exit 1 on a
  corrupted control; Cleaning yields `cleaning_basis == "content_record"`;
  extraction failure preserves every raw input and exits nonzero;
- live dogfood packets `01KY2E0Q5C2V598GSEGG6ABZRM` and
  `01KY2E4GG7J3CN93S6ZA4CRQT2` retained 5.4% of disposable bytes (18.5x);
- Target-native review UUIDs do not join the companion's numeric Bazaarvoice
  ids: 0 of 8 ids overlap while 7 of 8 bodies match by text. No join key exists
  and none was invented;
- the contract's stale Ulta rows and the Target `raw_unflipped` row are
  reconciled.

Full evidence and loss ledger:
`docs/research/forseti_target_canonical_content_capture_proof_v0.md`.

## Phase 2 — Amazon

Target landed on `main` at `6e64b35f`, so this phase is startable. It is a
separate branch and PR, and it requires its own implementation authorization.

### Concurrent-writer reconciliation — harvested 2026-07-21

`.codex/worktrees/amazon-content-mode` (branch `codex/amazon-content-mode`, base
`4c2e6464`) held an uncommitted, never-landed Amazon content-mode attempt that
already defined `retail_pdp_amazon_aggregate_content_v1`. Its base predates Ulta
v2, Sephora v4, the `retail_pdp_content.py` boundary, and the content-eligible
profile gate, so its nine modified files would regress the tree and are not
reusable. The owner directed harvest-then-discard on 2026-07-21.

Its two untracked files were read and harvested here; the code itself is not
carried forward (it imports `build_amazon_pdp_aggregate_content_record` and
sibling symbols that do not exist on `main`). What it knew, and Phase 2 should
reuse:

- **Amazon DOM anchors it bound against**: `#ASIN`, `#averageCustomerReviews`,
  `#acrCustomerReviewText`, `#availability`, `#deliveryBlock`,
  `#pqv-bought-in-last-month`, `#shipFromSoldByAbbreviatedODF_feature_div`,
  and `currencyOfPreference` / `en-US`.
- **It independently anticipated the recommendation-binding defect class** that
  the Phase 1 delegated review later found in Target's price extractor. It
  carried two fail-loud tests — one rejecting a `bought in past month` signal
  that is not target-ASIN bound, one rejecting a seller/shipper block that is not
  target bound. Treat target-binding of every merchandising signal as a required
  gate, not a nicety.
- **It enforced the ZIP `10001` pin at the CLI boundary** for Amazon content
  capture, matching the admitted envelope.
- **It carried a browser-secret fail-loud rejection**, the same class Phase 1
  implemented for Target.
- **It kept `amazon_pdp_aggregate` raw by default** until a live gate passed, and
  preserved all inputs with a typed nonzero exit on projection failure.
- **It carried a parser-fit drift check** over pinned sample packets — a runner
  that rebuilds the record from a preserved packet and reports drift, with cases
  for target-fact perturbation, metadata mismatch, input-hash drift, malformed
  records, and non-sample packets. Phase 1 got equivalent coverage from
  `run_content_qualification.py --route target`; prefer extending that existing
  runner over reintroducing a second one.

Before Phase 2 writes anything, confirm that worktree no longer holds
uncommitted work, so there is exactly one writer for the Amazon identifiers.

### Build

`retail_pdp_amazon_aggregate_content_v1`, strictly inside the owner-approved
pre-v3 envelope recorded at
`amazon_demand_signal_route_candidates_v0.md:82-123` (status
`BOUND_FOR_AMAZON_INFORMATION_CAPTURE__V3_CONTENT_SHAPE_DEFERRED`):

| Action | Bound |
| --- | ---: |
| Anonymous PDP navigation | 1 |
| Bounded scroll to customer reviews | 1 |
| Review portal, authentication, pagination, Bazaarvoice/API probes | 0 |
| Linked review-media downloads | 0 |
| Packet-local parsing passes over preserved bytes | Unbounded/local |

One anonymous US-pinned `amazon_pdp_aggregate` capture, ZIP `10001`, profile
`domcontentloaded` and zero-settle defaults kept, at most one bounded scroll
sufficient to render `#customerReviews`. Do not substitute
`amazon_pdp_distribution`. That envelope binds capture, not content shape: the
content record may change retained shape only after proving the single preserved
PDP reconstructs it, and it must not add requests to imitate Sephora fields
Amazon does not expose.

**Preserve** all target product, variant, offer, merchandising, media, aggregate,
and captured review-row fields — **including exact review bodies.** This is the
one place Amazon deliberately diverges from Target. Amazon has no separate raw
review-response companion: `01KY0S1ZACF3AG467GV6VA8CJN` contains only two files,
a control manifest and a body-free summary, with no raw response bytes of its
own. The bodies exist solely inside the parent PDP DOM, which content mode
discards after hashing. If the content record does not retain them, they are
lost.

**Prove** against parent packet `01KY0PHPN10205MKKCK1GB7YH1` (Laneige Sleeping
Berry, ASIN `B07XXPHQZK`, `cloakbrowser_snapshot`, 2026-07-20T21:22:40Z) and
companion `01KY0S1ZACF3AG467GV6VA8CJN`, written by
`amazon_pdp_review_onboarding_v1`. That route is now at
`amazon_pdp_review_onboarding_v2` / `amazon_review_onboarding_summary_v2`, which
corrects four measured summary defects; the landed v1 packet is append-only and
stays readable as v1 evidence.
Preserve every exposed review row including separately labelled international
rows; use the eight US top-review rows as the default US-market analysis window,
excluding international rows from that analysis by default rather than deleting
them from raw evidence.

### Retain these known losses explicitly

Carry them forward in the loss ledger; do not quietly resolve or paper over them:

- rows are labelled top reviews, not Most Helpful or Most Recent — no role guarantee;
- no monitoring anchor is claimed;
- the exposed rows are not the complete review corpus;
- no age, skin-type, or skin-concern demographic distributions are exposed;
- no customer product Q&A is exposed (brand-authored A+ FAQ entries are not customer Q&A);
- review media references remain source-visible but linked media bytes are not fetched;
- the winning route is Amazon-native rendered PDP content and is not Bazaarvoice.

## Drift Guard

- Do not run the Amazon lane while `codex/amazon-content-mode` still holds uncommitted work; its untracked files were harvested into this packet on 2026-07-21.
- Do not reintroduce the superseded Amazon implementation from that worktree; its base predates every current benchmark.
- Do not reopen Phase 1 except for a defect in the landed, packet-proven route.
- Do not add review-portal, authentication, pagination, API, or extra media requests to either retailer.
- Do not label Target CDUI/Redsky page state or Amazon rendered-PDP content as Bazaarvoice.
- Do not rebuild Target's Bazaarvoice companion or Amazon's review companion; both are reused.
- Do not extract a universal retail PDP parser or force version parity across retailers.
- Do not rewrite existing raw packets; they are append-only.
- Do not treat this handoff's Sephora freshness re-check as a recorded proof artifact.
- If current `main` already contains newer Target or Amazon content work, rederive the remaining delta; do not overwrite or duplicate it.

## Authority And Source Ledger

Blob hashes are observations at `798b94c4`, for staleness comparison only.

- `AGENTS.md` — project behavior kernel, SCI, isolation, and PR lifecycle. Reread before implementation.
- `.agents/workflow-overlay/README.md` — Forseti overlay entrypoint. Reread before implementation.
- `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md` — binding content-vs-raw retention contract and acquisition census. Blob `d21bb68e788475ff0055f2e4599d95a0093a075f`. **Carries the stale Ulta row named in Phase 1.**
- `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md` — authoritative extraction and preservation target. Blob `9506a1e2e6a4528828f50006932f2963439a3e9c`.
- `forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md` — owner-approved Amazon pre-v3 capture envelope. Blob `0286ee509709010cac2ed828d5986d8039e57123`.
- `forseti-harness/source_capture/retail_pdp_projection.py` — record models and retailer extractors. Blob `1a452ee4262b0506506d9d92a40fdd1372991cf7`.
- `forseti-harness/source_capture/retail_pdp_content.py` — content boundary/loader and profile-to-parser map. Blob `6d71cb353778b0d0f99cee63dba8e84494dbf3e4`.
- `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py` — content-mode retention seam and admission gate. Blob `43e56c55294d03c0286a8bf9ad042002a8567129`.
- `forseti-harness/source_capture/target_onboarding_capture.py` — landed Target companion and `__NEXT_DATA__` handling. Blob `7d21065076f99a546b6d4c62650e7a6d63c851b9`.
- `forseti-harness/source_capture/amazon_review_onboarding_capture.py` — landed Amazon native review companion. Blob `bb3ac6c091d2761c1aeee7f795f61d585a7a5326`.
- `forseti-harness/source_capture/ulta_onboarding_capture.py` — landed Ulta PowerReviews companion. Blob `6c8c83e538476ecf5e0521aaeec56834a603bfed`.
- `docs/research/forseti_ulta_powerreviews_review_capture_proof_v0.md` — Ulta loss ledger and non-claims. Blob `03153e4129169ec46e2a0a0e5b54975c371897ca`.
- `docs/workflows/forseti_bazaarvoice_retailer_compatibility_implementation_handoff_v0.md` — sibling lane; records the Target completed result and the Amazon side result. Not this lane's authority.

## Confirm-Don't-Trust Load Checklist

- Verify current `origin/main`, worktree cleanliness, and the source blobs above.
- Verify `798b94c4` is an ancestor of `HEAD`.
- Verify the named packets in the lake before citing them.
- Re-check whether `codex/amazon-content-mode` is still an unreconciled writer.
- Return one outcome:
  - `REUSE`: sources match; begin Target.
  - `PARTIAL_REUSE`: non-load-bearing context drifted; rederive and continue.
  - `STALE_REREAD_REQUIRED`: load-bearing sources moved; reread before acting.
  - `BLOCKED_DRIFT`: owner constraints or the phase order conflict.
  - `BLOCKED_UNVERIFIABLE`: the admitted envelope cannot produce the required content truthfully.

## Non-Claims

This handoff is a commission input. It is not validation, readiness, approval, or
proof that either content route is achievable within its envelope. It admits no
schema, proves no reconstruction, and grants no authority beyond the two bounded
implementation lanes it describes.
