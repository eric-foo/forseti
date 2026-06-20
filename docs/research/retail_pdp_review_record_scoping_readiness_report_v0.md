# Retail PDP Review Record Scoping Readiness Report v0

```yaml
retrieval_header_version: 1
artifact_role: Capture-lane scoping-readiness report
scope: >
  Decides whether a retail_pdp individual review_record adapter can move to
  implementation scoping by resolving or sharply routing three blockers:
  Attachment Record writer/storage binding, Sephora native Bazaarvoice review ID
  mapping, and Ulta PowerReviews DOM ID semantics. Includes the 2026-06-21
  probe-first addendum for Sephora/Ulta ID evidence. Non-authorizing decision input.
use_when:
  - Deciding whether the retail_pdp review_record adapter is ready for implementation scoping.
  - Routing the Attachment Record blocker and the Sephora/Ulta native-ID risks to their owning lanes.
  - Checking which bounded verification runs or upstream decisions must precede adapter code.
authority_boundary: retrieval_only
open_next:
  - docs/research/retail_pdp_review_record_capture_recon_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
input_hashes:
  docs/research/retail_pdp_review_record_capture_recon_v0.md: 692aa51bfb42df57017c71c8bd1497805c7cbaa9b75db1683220b8777c33a057
branch_or_commit: codex/retail-pdp-review-recon @ a9dadb90650c9855e93c21a0ffa24ce48b931788
stale_if:
  - The retail PDP review_record recon (input hash above) is superseded or re-patched.
  - The Attachment Record writer/storage physicalization seam is bound, implemented, or changed.
  - A later bounded ID probe supersedes the 2026-06-21 probe-first addendum.
  - Sephora or Ulta review DOM/API substrate is rerun or materially changes.
```

## 1. Status and Non-Authorizing Boundary

- Status: `SCOPING_READINESS_ASSESSED`.
- Primary recommendation label: **`PARTIAL_READY_ATTACHMENT_BLOCKED`**.
- Secondary label: **`SELECTOR_ID_VERIFICATION_RESOLVED_FOR_CURRENT_PACKETS`**
  (Sephora/Ulta current packet identity only; corpus breadth and Attachment Record
  physicalization remain separate).
- Compound form: `SELECTORS_CURRENT_PACKET_RESOLVED__ATTACHMENT_BLOCKED`.

2026-06-21 probe-first addendum: the earlier selector-ID blocker is superseded
for the current Sephora and Ulta packets. Sephora current visible rows can be
keyed from ProductGroup JSON-LD `reviews[].@id` values matched against visible
review text; Ulta DOM numeric suffixes are confirmed as PowerReviews
`review_id` values by a bounded read-API probe. This does **not** make the
adapter implementation-ready because the Attachment Record physical writer/layout
seam remains unbound.

This report is a decision input only. It is **not** implementation authorization,
runtime authorization, source-access boundary amendment, Attachment Record
architecture acceptance, validation, readiness, product proof, fixture
admission, ECR/Cleaning/Judgment, production storage, scheduler work, or PR/merge
authority. `GO`/`PARTIAL`/`READY` language anywhere below describes
source-access and scoping posture, never build authorization.

## 2. Source Readiness and Missing Sources

`SOURCE_CONTEXT_READY` for the scoping-readiness decision, with the material
gaps disclosed below.

Read and reasoned-from directly on this branch (`codex/retail-pdp-review-recon`
@ `a9dadb90`):

- `docs/research/retail_pdp_review_record_capture_recon_v0.md` (the recon; the
  patched/adjudicated version, hash `692aa51b…`).
- `docs/review-outputs/adversarial-artifact-reviews/retail_pdp_review_record_capture_recon_delegated_adversarial_review_v0.md`
  (cross-vendor review that validated the recon's accuracy and bounded the three blockers).
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
  (controlling source for blocker 1).
- Overlay governance: `README.md`, `decision-routing.md`, `retrieval-metadata.md`,
  `validation-gates.md`, `artifact-folders.md`, `source-of-truth.md`.

Confirmed at primary source (not relied on as secondary report):

- `orca-harness/source_capture/retail_pdp_projection.py` exposes exactly five
  aggregate row kinds (`retail_pdp_product`, `retail_variant_offer`,
  `retail_review_substrate`, `retail_embedded_structured_json`,
  `retail_carried_module`; lines 66-70, 300-445) and **no** `review_record` row
  kind or Attachment Record writer.
- `orca-harness/source_capture/models.py` `PreservedFile` (line 108) carries
  `relative_packet_path`, `sha256`, and a validator-bound `hash_basis`
  restricted to `raw_stored_bytes` (lines 57-66, 116-124) = sha256 over the
  complete unmodified stored bytes at the packet-relative path.

Material gaps (do not block the decision, but bound its strict-claim ceiling):

- **Local-scratch packet evidence.** All Sephora/Ulta per-review findings below
  come from `orca-harness/_test_runs/retail_pdp_review_recon_20260620/`, which is
  gitignored and untracked. These are reported local evidence, **not**
  repo-reproducible fixtures, and cannot clear a strict readiness gate.
- **Storage/core lake contracts read via the implementation contract's summary.**
  The Attachment Record *implementation* contract is the most specific blocker-1
  source and was read in full; its faithful "Current Source Evidence" summary of
  `core_spine_v0_data_lake_storage_contract_v0.md` and `…core_contract_v0.md` was
  relied on rather than re-reading those two directly. The adversarial review
  independently verified that contract chain (its Source-Read Ledger).
- **`review_record` source-family definition is branch-only.** The commission
  prompt and the review-capture spec that define `review_record` field semantics
  live only in the `.claude/worktrees/distracted-ishizaka-01eff5` worktree (recon
  finding AR-01); they are not on this branch or `origin/main`. The body shape
  below is therefore scoped from **raw source-visible fields only**, which is
  exactly what the Attachment Record contract requires regardless.

## 3. Cynefin Routing Result

```text
Smallest complete outcome: A non-authorizing readiness report that tells the
  owner/next CA whether retail_pdp review_record adapter implementation scoping
  can start, and if not, exactly which blocker remains and who owns it.
Regime: Mixed (Complicated + Complex).
Why: Blocker 1 and the source-map are reasoned from current contracts/code
  (Complicated); the Sephora/Ulta native-ID identity was Complex before the
  2026-06-21 addendum and is now resolved for the current packets only.
Decomposition: Split and classify — reason the attachment binding and source-map
  from sources; risk-first probe the ID-identity unknowns before adapter work.
Current bottleneck: The Attachment Record physical writer/layout seam is unbound
  and belongs to the Data Lake physicalization lane.
Riskiest assumption: That current-packet ID evidence generalizes to broader
  Sephora pagination/full-corpus coverage. Current visible/embedded rows are
  resolved; full-corpus breadth is not proven.
Stop or pivot condition: If a later packet/API rerun stops exposing matching
  Sephora ProductGroup `reviews[].@id` values or Ulta `review_id` matches, the
  adapter identity key must be redesigned for that retailer.
Allowed next move: Scope a read-only source-map design using current native IDs,
  and separately route the Data Lake physicalization decision.
Disallowed next move: Start adapter implementation; run live capture without
  explicit owner authorization; claim full-corpus coverage from current packets;
  or select an Attachment Record physical backend/layout.
```

## 4. ELI5 Summary of the Three Blockers

- **Writing a review durably (Attachment Record).** We know the *shape* a stored
  review record must take (a small keyed index entry pointing to an immutable,
  hash-checked body). We have *not* yet decided exactly *how/where* those bytes
  get written — that physical decision belongs to the Data Lake lane, and no
  writer exists in the harness today. So we can design the adapter's fields, but
  we cannot finish a durable write path yet.
- **Sephora: which ID belongs to each review.** The visible row containers still
  do not carry IDs, but the same packet's ProductGroup JSON-LD has review `@id`
  values, and six visible review bodies match six of those keyed review objects.
  That is enough for current visible rows, not for the full 22k-review corpus.
- **Ulta: are those numbers real review IDs?** The page shows numbers like
  `pr-rd-review-headline-580013849`. The bounded PowerReviews read confirmed all
  five observed suffixes are native `review_id` values for the current product.

## 5. Attachment Record Binding Analysis (Blocker 1)

**Does the contract bind enough to scope a `review_record` writer?** Partly. The
implementation contract
(`…attachment_record_implementation_contract_v0.md`, status
`BLOCKER_1_IMPLEMENTATION_CONTRACT_RECORDED_V0`) binds the **Required Shape** —
enough to scope the adapter's *body field shape and keying* — but explicitly
**defers** the physical writer seam. So adapter source-map and candidate-body
scoping can proceed; a durable `review_record` write path cannot be scoped to
completion until the Data Lake physicalization lane binds the seam.

**Smallest acceptable Attachment Record shape for retail PDP `review_record`
bodies (raw source-visible fields only):** an immutable, hash-checkable body
carrying the per-review raw source-visible payload (reviewer display label,
rating/stars, title, review text, submission/timestamp, variant attributes,
verified-purchase flag, incentive/recommendation flags, helpful counts, media
presence, and the native-or-candidate review ID) — with **no** normalized,
cleaned, deduped, or judged values. Absent or unverified fields are marked as
per-field residuals, not invented (contract Required Shape items 2-3, 7; recon
"Recommended Minimal Next Scope" items 2-3).

**Required keys in the compact manifest/index entry** (contract Required Shape
item 1): `packet_id`, `slice_id` (when applicable), a packet-scoped
attachment/file key (when needed), source family, payload kind, payload schema
version, replay/version pins, attachment reference, `hash`, `hash_basis`, and an
absence/refusal/residual posture summary.

**What must be hash-checkable, immutable, and packet-relative:** the attachment
body must be immutable and verifiable from the entry under the recorded
`hash_basis` (contract item 3). The current `PreservedFile` discipline is the
viable evidence pattern — packet-relative path + `sha256` + `hash_basis =
raw_stored_bytes` (models.py:57-66, 108-124) — but is evidence of viable
discipline, **not** the final Attachment Record schema.

**Decisions owned by the Data Lake / Attachment Record lane (not the retail_pdp
adapter lane)** — all deferred by the contract:

- exact packet-member vs sidecar vs equivalent body layout;
- exact manifest/index serialization (and any Manifest v2 mechanics);
- physical backend (database, object store, warehouse, lakehouse, queue);
- migration/replay plan for incumbent direct fields;
- the writer seam itself and Availability-Index rebuild mechanics;
- lawful-erasure / retention / WORM mechanics.

The adapter lane owns: per-retailer source mapping, raw-field extraction, residual
marking, and producing **candidate** review bodies that conform to the Required
Shape — strictly packet-local (consume preserved bytes + projection context only;
no fetch, paginate, dedupe, score, identify actors, or downstream calls).

Per the contract's Rejected Shapes, the adapter must not push payload bodies into
new lake-core fields, create un-keyed loose sidecars, or make a mutable DB row
the canonical body. No physical backend/layout may be selected in scoping.

## 6. Sephora ID Mapping Analysis (Blocker 2; Current Packet Resolved)

Packet: `sephora_pdp_review_recon_01` (lip-sleeping-mask P420652), **local-scratch**.

- **Local contradiction audit result (2026-06-21):** the projection's parsed
  ProductGroup JSON-LD row (`retail_embedded_structured_json`, `ld_json[3]`) has
  10 `reviews[]` entries and all 10 carry `@id` values.
- **Visible-row match:** the visible text capture says `Viewing 1-6 of 22k
  reviews`. Six rendered review bodies in that visible section match six
  ProductGroup `reviews[]` bodies with `@id` values:
  `394094611`, `393943407`, `393913515`, `393901635`, `393888454`, and
  `393764708`.
- **What remains true from the prior analysis:** the rendered review-row
  containers themselves still carry no `id`, `data-review-id`, or BV token.
  The key is therefore not attached directly to each rendered container; it is
  available from the ProductGroup JSON-LD review objects for the current
  visible/embedded rows.
- **Readiness impact:** Sephora no longer needs the Bazaarvoice Display API read
  to key the current visible review rows in this packet. A live BV read is only
  optional if the desired scope expands to pagination/full-corpus coverage beyond
  the current visible/embedded rows.

Net: Sephora moves from `GO_WITH_NATIVE_ID_MAPPING_RISK` to
`CURRENT_PACKET_NATIVE_ID_RESOLVED`: current visible rows have native IDs, but
full 22k-review corpus access is not proven by this packet.

## 7. Ulta ID Semantics Analysis (Blocker 3; Current Packet Resolved)

Packet: `ulta_pdp_review_recon_01` (night-shift-overnight-lip-mask, sku 2645443),
**local-scratch**.

- **The DOM numeric IDs:** five unique `id="pr-rd-review-headline-<N>"` tokens —
  `575373729, 576140820, 578859756, 579948269, 580013849`. The values are
  **sparse/large** (gaps up to ~2.7M), the signature of external-system native
  IDs rather than sequential UI ordinals.
- **No corroboration in-packet:** each number appears **only** as the headline
  element `id`, its `data-testid="headline-<N>"`, and `aria-describedby` — never
  in an href/permalink, a `review_id`/`ugc_id` field, Apollo state, or the
  projection JSON. So the "native ID" read is suggestive but unconfirmed from the
  packet alone.
- **JSON-LD cannot key identity:** the 5 schema.org `Review` objects carry
  `name`, `datePublished`, `author.name`, `locationCreated`, `reviewRating` — and
  **no** `@id`, `url`, `identifier`, or `reviewId`. The only quasi-key
  (`datePublished + author.name + name`) is not collision-resistant. An adapter
  cannot reliably key per-review identity off JSON-LD.
- **Bounded read-API probe (2026-06-21):** the path-only read of
  `readservices-b2c.powerreviews.com/m/6406/l/en_US/product/pimprod2046225/reviews`
  reached PowerReviews and returned `401 api key is required for authentication`.
  The source-visible Ulta DOM exposes `api_key: 'daa0f241-...'` and
  `merchant_id: '6406'`, so the corrected read used the same host/path with
  `?apikey=<source-visible DOM value>`.
- **Probe result:** the corrected GET returned `200`, `application/json`,
  `length=131403`, top-level keys `configuration,name,paging,results,native_filter`.
  `paging.total_results=671`, `page_size=5`, and the first returned review has
  `review_id=580013849`.
- **ID comparison:** returned numeric ID candidates include all five DOM suffixes:
  `575373729`, `576140820`, `578859756`, `579948269`, and `580013849`.
- **Readiness impact:** Ulta `pr-rd-review-headline-<N>` suffixes are confirmed as
  native PowerReviews `review_id` values for the current product packet. JSON-LD
  remains unsuitable as an identity fallback because it still carries no ID field.

Net: Ulta moves from `GO_WITH_ID_SEMANTICS_RISK` to
`CURRENT_PACKET_NATIVE_ID_RESOLVED`: bind current PowerReviews rows to the DOM
numeric suffix as native `review_id`, subject to rerun staleness.

## 8. Amazon Partial-Scope Note (Blocker 4 / scope boundary)

From the recon Field Verdicts (packet `amazon_pdp_control_01`, local-scratch) and
the access probes:

- **PDP-embedded top reviews remain usable.** Per-review blocks expose
  `data-reviewid` (a native-looking per-row ID — the most directly attached of the
  three retailers), plus reviewer name, rating, title, date, variant, verified
  badge, and text.
- **All-review pagination remains blocked** under the tested no-gate-defeat routes
  (rendered + direct-HTTP both hit continue-shopping/`opfcaptcha` interstitials).
  Do not claim a full Amazon corpus path under this boundary.
- **Recommendation:** include Amazon only as a **partial source — PDP top reviews
  only** in first scoping; hold full-corpus pagination as blocked. Amazon's
  identity risk is the lowest (ID is attached per row), but its corpus is the
  smallest; Sephora/Ulta current-packet identity is now resolved by the
  2026-06-21 addendum.

## 9. Recommendation Label

**Primary: `PARTIAL_READY_ATTACHMENT_BLOCKED`** — the source side (per-retailer
descriptive-field source-map + the Required-Shape body) is bounded enough to
scope, but the durable write path is blocked because the Attachment Record
physical writer/layout seam is an unbound Data Lake-lane decision.

**Secondary: `SELECTOR_ID_VERIFICATION_RESOLVED_FOR_CURRENT_PACKETS`** — the
review-**identity** key is resolved for the current Sephora and Ulta packets.
Sephora is keyed by ProductGroup JSON-LD `reviews[].@id` matched to visible rows;
Ulta is keyed by PowerReviews `review_id` confirmed against DOM suffixes.

Ruled out: `READY_FOR_IMPLEMENTATION_SCOPING` (write seam unresolved);
`BLOCKED_NEEDS_DATA_LAKE_BINDING_DECISION` as *primary* (the contract already binds
the Required Shape — what is missing is physicalization, not the binding, so the
adapter source-map can still be scoped); `RUN_REQUIRED_NO_AUTHORITY` as the whole
verdict (the ID sub-question has been probed for current packets); `NO_GO_RECON_STALE`
(the recon is the current, adjudicated, hash-stable `692aa51b…` version).

## 10. Minimal Implementation-Scoping Surface and Exact Next Blockers

**Can be scoped now (read-only, no authorization needed)** — a selector-level
source-map design that:

1. Locks per-retailer descriptive-field selectors: Amazon PDP top-review blocks,
   Sephora rendered review rows, Ulta JSON-LD + PowerReviews rows.
2. Defines the `review_record` candidate body against the Attachment Record
   Required Shape, keyed by `packet_id`/`slice_id`/retailer/product-or-SKU/source
   URL and native review ID where current packets bind it, raw source-visible
   fields only.
3. Uses Sephora ProductGroup JSON-LD `reviews[].@id` for current visible/embedded
   rows and Ulta PowerReviews DOM suffixes as confirmed `review_id` values; marks
   absent fields and out-of-current-packet corpus breadth as per-field residuals.
4. Keeps the extractor strictly packet-local.

**Exact remaining blockers before full adapter implementation scoping is `READY`:**

- **B1 (upstream lane/owner):** Data Lake physicalization lane binds the
  Attachment Record writer seam (layout/serialization/backend) per the contract's
  Deferred Decisions. Until then, only candidate bodies, not durable records.
- **B2/B3 status:** current-packet Sephora and Ulta ID verification is resolved
  by the 2026-06-21 addendum. A later live run is needed only if scope expands to
  broader pagination/full-corpus coverage or the retailer substrate changes.

## 11. Evidence Table

| Claim | Tier | Source |
| --- | --- | --- |
| No `review_record` row kind / Attachment Record writer exists in the harness | repo-verifiable | `orca-harness/source_capture/retail_pdp_projection.py:66-70,300-445` |
| Attachment Record Required-Shape keys + immutable hash-checkable body; layout/backend/writer seam deferred | repo-verifiable | `…attachment_record_implementation_contract_v0.md` (Required Shape; Deferred Decisions) |
| `PreservedFile` hash discipline = packet-relative path + sha256 + `hash_basis=raw_stored_bytes` | repo-verifiable | `orca-harness/source_capture/models.py:57-66,108-124` |
| Recon is current, adjudicated, hash-stable | repo-verifiable | `git show HEAD:…recon_v0.md` sha256 `692aa51b…`; HEAD `a9dadb90` |
| Sephora ProductGroup JSON-LD has 10 `reviews[]` entries with 10 `@id` values | local-scratch | `sephora_pdp_review_recon_01/retail_pdp_projection.json`, `ld_json[3]` |
| Sephora visible rendered review section exposes 6 rows and all 6 body-match ProductGroup reviews with `@id` values | local-scratch | `sephora_pdp_review_recon_01/packet/raw/02_cloakbrowser_visible_text.txt` (`Viewing 1-6 of 22k reviews`) |
| Sephora rendered review-row containers carry no ID attribute | local-scratch | `sephora_pdp_review_recon_01` DOM (`data-comp="Review Review BaseComponent"`, no `id`/`data-review-id`) |
| Ulta DOM `pr-rd-review-headline-<N>` IDs are sparse/large; absent elsewhere in packet | local-scratch | `ulta_pdp_review_recon_01` DOM (5 unique tokens; no href/`review_id`/Apollo match) |
| Ulta JSON-LD `Review` objects carry no `@id`/`url`/`identifier`/`reviewId` | local-scratch | `ulta_pdp_review_recon_01` DOM `ld+json[1]` (5 Review objects) |
| Ulta PowerReviews API confirms DOM suffixes as native `review_id` values | bounded live read | `readservices-b2c.powerreviews.com/m/6406/l/en_US/product/pimprod2046225/reviews?apikey=<source-visible DOM value>` returned 200; `paging.total_results=671`; all 5 DOM suffixes matched |
| Amazon PDP top reviews expose `data-reviewid`; all-review pagination blocked | local-scratch | recon Field Verdicts; packets `amazon_pdp_control_01`, `amazon_review_page_*` |
| Attachment Record physical writer/layout seam | unverified upstream decision | Data Lake physicalization lane still required before durable adapter implementation |

## 12. Owner Decisions Needed

1. **Sequence the Data Lake physicalization lane** (B1) that binds the Attachment
   Record writer seam — a separate Data Lake-lane decision, not the adapter lane's.
2. **Confirm first-scope retailer set** — recommended: scope all three
   source-maps; treat Amazon as PDP-top-reviews-only; do not commit a durable
   write path for any retailer until B1 lands.
3. **Optional broader-corpus choice:** decide whether Sephora/Ulta first scope is
   current visible/embedded rows only, or whether pagination/full-corpus coverage
   should be probed before implementation scoping.
4. **Optional hygiene:** register this report in `docs/workflows/orca_repo_map_v0.md`
   to satisfy the forward-only retrieval-header CI orphan gate. Left undone here
   because this commission's edit permission was scoped to the report file only.

## 13. Required Follow-up Prompt / Report / Run

- **Required next:** a Data Lake physicalization scoping/decision prompt for the
  Attachment Record writer seam (B1).
- **Optional next:** a pagination/full-corpus source-access probe if the owner
  wants more than current visible/embedded Sephora/Ulta rows in first scope.
- **After B1:** an `workflow-implementation-scoping` pass producing the
  `STEP-*` route for the retail_pdp `review_record` adapter. Not before.
- **No further run is authorized by this report.** A read-only source-map design patch
  (Section 10) may proceed without a run if the owner prefers to advance scoping
  before the probes.

## 14. Non-Claims

This report is not implementation authorization, runtime authorization,
source-access boundary amendment, Attachment Record architecture acceptance,
validation, readiness, product proof, commercial authorization, fixture
admission, ECR, Cleaning, Judgment, production storage, scheduler work, or PR
merge authority. Local-scratch packet evidence is reported, not repo-reproducible,
and does not clear a strict gate. Verdict tokens describe source-access and
scoping posture only. The two bounded verification runs are recommendations, not
execution authority.
```
