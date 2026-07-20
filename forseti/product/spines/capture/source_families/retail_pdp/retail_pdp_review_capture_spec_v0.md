# Retail/PDP Review-Record Capture — Spec v0 (what to capture from reviews)

```yaml
retrieval_header_version: 1
artifact_role: Product spec (commission input to the capture-spine lane; what-must-be-true, not a build)
scope: >
  Stabilizes WHAT the capture-spine must preserve from retailer PDP reviews so two
  downstream consumers can be served from the same raw capture: (1) the demand read
  (review velocity, content/pain-point shift, persistence) and (2) the
  manufactured-demand integrity discrimination (the WITHIN-CATEGORY co-review
  graph, burst/templating, verified-purchase share, account-youth, syndication
  de-correlation). Extends the current Retail/PDP capture, which preserves only the
  AGGREGATE review substrate (count + rating), to preserve INDIVIDUAL source-visible
  review records. Capture-side only: raw-canonical, source-visible facts + limits,
  no graph, no dedup, no identity, no integrity verdict (all downstream). Lands as
  source-family Attachment Records per the data-lake contract. What-must-be-true,
  not a build; capture execution stays capture-lane + owner-gated.
use_when:
  - Scoping or reviewing what retailer PDP review capture must preserve (fields, per-retailer substrate, storage shape).
  - Bounding the review-corpus scope so the within-category co-review graph is reachable without an unbounded crawl.
  - Checking the capture/downstream boundary for reviews (what capture must NOT do).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/demand_durability_multi_retailer_rendered_capture_spec_v0.md  # per-retailer rendered capture, measured-ToS, one-series-per-retailer
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md                           # Attachment Records (source-family payload home); lake owns no identity/dedup/judgment
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md                        # record-kind slots; raw canonical; append-only derived; physicalization deferred
  - forseti/product/spines/judgment/demand_read/integrity/judgment_spine_manufactured_demand_detection_design_v0.md  # the DOWNSTREAM consumer (co-review graph, evidentiary hierarchy, INV-1)
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md  # measured-ToS / no-gate-defeat posture
stale_if:
  - The Retail/PDP projection contract changes the review-substrate row family or required bindings.
  - The data-lake Attachment Record boundary or the source-family payload rules change.
  - A retailer's review-substrate source (Sephora Bazaarvoice, Ulta Apollo, Amazon DOM) recon verdict changes.
  - The manufactured-demand design amends the tells the co-review graph / per-review fields must support.
```

## Status

`SPEC_V0` — **commission input to the capture-spine lane**, owner-requested 2026-06-20. This is a
**what-must-be-true** spec, **not** an architecture, route, build, or capture execution. The
capture-spine lane owns the adapter architecture + build under its own scoping; **capture
execution and landing to `main` stay owner-gated.** Caps at `product_learning` / design input;
`no_durable_evidence`.

## Why (the gap this closes)

Today the Retail/PDP projection preserves only the **aggregate** review substrate — a
`retail_review_substrate` row carrying review **count + rating** and how it was located
(`retail_pdp_content_cleaning_contract_v0.md`). That is enough for "how much / how highly reviewed,"
but **not** for either downstream consumer that needs the **individual reviews**:

- the **demand read** wants review **velocity over time**, **content/pain-point shift**, and
  **persistence after a push** — all per-review, dated;
- the **manufactured-demand integrity read** wants the **within-category co-review graph**
  (reviewer × product), **burst/templating**, **verified-purchase share**, **account-youth**, and
  **syndication de-correlation** — all per-review (see the integrity design's evidentiary
  hierarchy: the co-review network is the strongest *public-data* tell).

So capture must preserve the **individual source-visible review records**, not just their
summary. Everything interpretive (the graph, dedup, identity, the integrity verdict) stays
**downstream** — this spec only fixes what raw capture must carry.

## Required Behavior — what to capture from reviews

When an authorized retailer PDP review surface is captured, the raw packet must **preserve the
source-visible review records verbatim** (raw canonical; absence/fallback **residualized**, never
fabricated — same discipline as the projection contract). Per **individual review**, preserve the
source-visible fields below where the retailer exposes them; residualize when absent.

| Field (source-visible) | Serves demand read | Serves integrity read | Per-retailer note |
| --- | --- | --- | --- |
| `source_native_review_id` | link/dedup key (downstream) | stable per-review key | Bazaarvoice/Apollo/Amazon expose a review id |
| `product_sku_key` (→ the PDP slice/variant) | ties review to the SKU | ties review to the product node | use the projection contract's variant binding |
| `reviewer_display_name` + `source_native_reviewer_id` | — | **the co-review graph key** (account → products) | Bazaarvoice author id; Amazon profile id; Ulta Apollo author ref |
| `rating` (stars) | sentiment level | post-campaign sentiment-**shift** input (not static bimodality — see histogram note) | — |
| `review_timestamp` (posted date/time) | **velocity + persistence** | **burst alignment** (timing) | preserve native precision (date vs datetime) |
| `review_text_verbatim` (+ `title`) | pain-point / content shift | **templated/duplicate language** | preserve bytes, not paraphrase |
| `verified_purchase_flag` | — | **verified-purchase share** — strong **low-side flag**, but **not** a high-side clearance (reimbursement makes fakes *verified*) | Amazon explicit; Bazaarvoice/PowerReviews "verified buyer" common; **coverage varies per retailer — residualize where absent** |
| `incentive_disclosure_flag` + `incentive_disclosure_text` (e.g. incentivized, sponsored, gifted, complimentary, received free sample, sweepstakes, or paid partnership) | — | **incentive distortion** | preserve the source's exact flag and label when exposed; a false flag or absent label means only **not marked incentivized**, never confirmed organic or explicitly non-incentivized |
| `syndication_source_flag` (native vs syndicated review) | — | **de-correlation** (a syndicated review echoed across retailers is **one** review, not independent corroboration) | **Bazaarvoice exposes syndication source** — high value |
| `helpful_votes` / `total_votes` | engagement quality | vote-manipulation context | — |
| `reviewer_profile_metadata` (badges, reviewer rank, #reviews, tenure/age) | — | **account-youth / history depth** | capture only what is source-exposed; **no person-level dossier** (product boundary) |
| `media_attached_flag` (photo/video) | effortful UGC (costly behavior) | staged-media context | — |
| `brand_response_present` | engagement | — | — |
| `per_review_residual` (absent/fallback/mismatch posture) | gap visibility | gap visibility | per the projection contract's residual discipline |

Extend the **aggregate** substrate (in addition to the current count + rating):

- `rating_distribution_histogram` (5/4/3/2/1 counts) — for the **demand** read (sentiment spread)
  and the **post-campaign rating *shift*** (a 5★ launch wall that later deteriorates to 1★ — the
  meaningful integrity signal, per the Amazon decay finding). **Not** a static-bimodality verdict:
  genuinely polarizing products (a strong active some react to) are bimodal *without* any
  manufacturing, so static shape is **not** trusted as a tell. Bazaarvoice and Amazon expose the
  breakdown.
- `review_cadence` is **derivable** from the per-review timestamps (do not store a separate
  computed series in raw — it is a re-derivable view).

For any downstream incentive-filtered approval read, Capture must also preserve the
source-visible total, captured-row count, sort/filter/window, and truncation posture.
Capture does not calculate approval, exclude rows from the raw packet, or translate
an absent incentive marker into an organic-review claim. Those are downstream
derivation and claim-boundary decisions.

**Capture mechanics — substrate-first, per retailer** (consume existing recon; do not re-invent):

- **Sephora → the Bazaarvoice review API + progressive scroll.** Bazaarvoice returns **structured
  review JSON** (review id, author id, rating, text, badges, **syndication source**) — the richest
  and most graph-ready substrate; preserve the JSON verbatim.
- **Ulta → `window.__APOLLO_STATE__` embedded JSON** for the review records.
- **Amazon → rendered DOM** (review pagination); **recon still open** (the projection contract's
  open Amazon source-access question) — author an honest GO/PARTIAL/NO-GO; Amazon's automation ToS
  is the most restrictive (measured pre-commercial; commercial scale routes through a provider,
  not Orca's own path).
- **Posture:** public pages, **measured-ToS / honest-anti-blocking**, **no-gate-defeat** (stop at
  auth/CAPTCHA/Cloudflare challenge and record the limitation). **One series per retailer** (same
  SKU across retailers = parallel per-retailer series, compared downstream — never one series
  spanning retailers).

## Corpus Scope — reachable graph without blowing up the lake

The co-review graph needs **reviewer histories** (which other products a reviewer touched), not
all products. Bound the capture as an **in-niche ego-graph**, not an industry crawl:

1. **Seed** = the candidate SKU + its close in-niche competitors (the owner's "top ~10% of the
   similar niche" is a reasonable seed heuristic — the high-review SKUs where brokers operate).
2. **One hop along reviewers** = for reviewers who appear on the seed set, pull their **other
   in-niche reviews** (the edges that form the graph). **Within-category only** — cross-industry /
   cross-product is **explicitly out of scope** (owner, 2026-06-20).
3. **Stop** = bounded, measured, commissioned-set volume; no unbounded crawl; no second hop unless
   separately authorized.

**Pre-positioning (forward-only option value).** Because manufactured detection is **forward-only**
and the decay/persistence series **cannot be reconstructed later** (reviews get deleted/edited;
timestamps are point-in-time), capturing a **bounded in-subniche roster on a bounded cadence** —
*before* a specific target exists — has real option value: it builds the longitudinal substrate the
persistence read depends on. Discipline: a **named bounded roster** (not "everything") on
**periodic attended / self-terminating runs** (the demand-durability cadence shape), **not a
standing crawler** (the thesis's no-standing-monitor boundary). Capture execution stays owner-gated.

**Lake-bloat is bounded by this scope, not by lake mechanics.** Raw review records are text (not
media) and land **once, append-only, by key** as Attachment Records (below). The compact co-review
**edges** (`reviewer_id × product × timestamp × rating × verified`) are a **derived/projection
view**, re-derivable from raw — they are not a second raw store.

**Honest within-category caveat (carry into the downstream graph, not capture):** within a
category, legitimate co-review is *common* (a skincare enthusiast really does review ten serums),
so within-category overlap is **noisier than the cross-industry signal** and is **not dispositive
alone** — it separates a broker roster from a genuine community only when combined with timing
sync, the post-campaign rating shift, account-youth, and verified-purchase share. Evadable by a broker who
spreads across category-diverse accounts (costs them efficiency). This is a *judgment*
calibration; capture just preserves the fields.

## Storage Shape (lands per the data-lake contract — selects no engine)

- Individual review records are a **new source-family payload** → land as **Attachment Records**
  (source-family `retail_pdp`, a `review_record` payload kind), keyed to `packet_id` / `slice_id`
  — **not** new direct `SourceCaptureSlice`/`SourceCapturePacket` fields (data-lake core contract:
  incumbent direct fields are legacy/transitional only).
- **Raw is canonical**; the Attachment Record carries the source-visible body + posture; it
  **must not** carry cleaned values, dedupe decisions, canonical reviewer/product identity,
  credibility, or any Judgment label (data-lake boundary).
- The co-review **graph / edges / dedup / reviewer-identity** are **append-only derived records**
  (Derived Result Store) or a projection view keyed back to raw — **re-derive, never migrate**.
- Physical representation (engine, sidecar/member layout, manifest version) stays **deferred** to
  the data-lake physicalization lane — this spec selects none.

## Non-Goals (the capture/downstream boundary — load-bearing)

- **No co-review graph, dedup, reviewer-identity resolution, or entity resolution.** Capture
  preserves reviewer ids + edges as raw facts; building/identifying the graph is **entity
  resolution + Judgment**, downstream.
- **No integrity verdict / scoring.** No manufactured/real label, no co-review-density score, no
  reliability tier assigned at capture — INV-1; the manufactured-demand design consumes this raw
  downstream and stays qualitative.
- **No first-party submission telemetry.** Reviewer **IP, device fingerprint, per-device
  submission velocity** are captured server-side by the review host (Bazaarvoice/PowerReviews) at
  the reviewer's submission and are **never sent to a page reader** — they are **not reachable via
  F12 or scraping** and are out of scope. (Public review **timestamps** give the aggregate burst;
  the per-device telemetry does not.)
- **No cross-industry / cross-product corpus.** Within-category ego-graph only.
- **No new packet schema, manifest bump, or direct-field promotion.** Attachment Records only.
- **No person-level dossier in any sold or external surface** (product boundary) — capture only
  source-exposed public review-author fields, for internal integrity judgment.
- **No ECR / Cleaning / Judgment**, no salience/credibility/demand decision (projection-contract
  boundary).
- **No capture execution / build.** Commission input only; the capture-spine lane owns the build;
  capture execution + landing stay owner-gated.

## Acceptance Signal (how "settled" is recognized)

For an authorized retailer + bounded in-niche seed set, capture produces raw packets whose
preserved bytes carry the **per-review fields above** (verbatim, residualized where absent) plus
the extended aggregate substrate, landing as `retail_pdp` `review_record` Attachment Records keyed
to the packet/slice; the within-category corpus stays bounded to the ego-graph; per-retailer
posture + recon verdict recorded; **no graph, identity, or integrity label produced at capture**;
no gate defeated. A retailer that recons NO-GO/PARTIAL is recorded as such.

## Open Questions for the capture-spine lane

- **Amazon review recon** — GO/PARTIAL/NO-GO under the boundary (review pagination is the hardest
  anti-bot + ToS case; NO-GO acceptable).
- **Bazaarvoice review-API shape per Sephora SKU** — exact exposed fields (author id stability,
  syndication-source field name, badge vocabulary) — confirm in recon, do not assume.
- **Adapter shape** — per-retailer review adapters vs one rendered+embedded-JSON review extractor
  behind the existing writer seam (smallest-complete call — capture-lane owned).
- **Ego-graph hop budget / seed size** — the exact "top N%" and reviewer-hop cap (a corpus-scope
  parameter; owner/capture-lane tunable).
- **Candidate retailer extensions — Target, Walmart** (Bazaarvoice / PowerReviews-backed, "verified
  buyer" badges, `review_record`-compatible). **Add only where the retailer is strong for *online*
  reviews in the target subniche** — the focus is the online review substrate, not in-store. General
  assessment (per-SKU online review strength is a recon question): **Target.com** is a genuine online
  masstige / clean-beauty channel with substantial review volume — a solid add for mass / masstige /
  clean subniches; **Walmart.com** carries high drugstore/mass review *volume* but is value-skewed and
  lower signal-richness — add only for drugstore/mass subniches; for prestige / clinical /
  indie-prestige, Sephora/Ulta/Amazon dominate and these add little. More retailers also strengthen
  the within-category co-review graph. Each needs its own adapter + GO/PARTIAL/NO-GO recon + ToS
  posture; **subniche-fit + online-review strength** gate the decision — not "scrape every retailer."
  The Retail/PDP projection contract (currently Amazon/Sephora/Ulta) extends with them.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: retail PDP review-record capture spec (commission-input design artifact)
  source_quality_state: design/control artifacts only (retail_pdp projection contract + demand-durability capture spec + data-lake core/storage contracts + manufactured-demand design, read fresh on the worktree off origin/main); no capture run, no review records, no graph
  execution_quality_state: no capture executed, no review record preserved, no adapter built
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no capture exists; Amazon review recon open; Bazaarvoice review-API field shape unconfirmed; capture execution owner-gated
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not capture execution or build authorization
    - not ECR, Cleaning, Judgment, or buyer proof
```

## Non-Claims

- Commission-input spec only; **authorizes no capture, scrape, run, adapter build, schema change,
  or storage implementation.** Capture execution + landing stay owner-gated; the capture-spine
  lane owns the build.
- **Capture-side only:** raw-canonical source-visible facts + limits; **no graph, dedup, identity,
  integrity verdict, or scoring** (INV-1; all downstream).
- Lands per the data-lake Attachment Record boundary; **selects no storage engine** (physicalization
  deferred). Mints no vocabulary; reuses the projection contract's row/residual discipline, the
  data-lake record kinds, and the manufactured-demand design's tells.
- Does not change the design's forward/live, not-backtestable boundary for manufactured detection.
- `SPEC_V0` PROPOSED; on adoption owes a dated pointer via the Doctrine-Change Propagation Contract.

```text
This is advisory design input only. It is not a verdict, not implementation authority, not capture
execution, and not proof of readiness.
```
</content>
