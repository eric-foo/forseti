# Core Spine v0 Projection Doctrine

```yaml
retrieval_header_version: 1
artifact_role: Product architecture draft (view contract over the Data-Capture-owned Mechanical Source Projection helper)
scope: >
  Raw-to-Judgment view contract for Orca: how source lanes project a raw capture
  into a compact, Judgment-readable view (the Projected Unit) without replacing raw
  evidence, erasing semantic source structure, or letting projection or Cleaning
  perform Judgment. A view contract over the existing Data Capture Projection
  Packet — NOT a new spine layer.
use_when:
  - A source lane is deciding what it may mechanically present to make a raw capture legible.
  - Checking what a projected view must preserve or anchor, and what it may remove.
  - Deciding when Judgment must pull the raw anchor instead of trusting the view.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
stale_if:
  - The owner changes the 2026-06-16 OD-1/2/3/4/5/6/7 directions recorded here.
  - The owner amends or supersedes the vendor-CA kept candidate.
  - The boundary note changes the Mechanical Source Projection / Data Capture Projection Packet doctrine.
```

- Status: `CANDIDATE_KEPT_BY_VENDOR_CA_FOR_OWNER_CONFIRMATION`
- Artifact type: Product architecture draft (view contract)
- Vendor-CA closeout: `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md`
- Implementation authorized: no by this doctrine artifact. The bounded Reddit projection helper in the same lane was separately owner-authorized on 2026-06-16 and does not generalize schema/object authority.
- Owner OD direction installed: 2026-06-16; see section 11.
- Feature planning authorized: no
- Proof run / capture execution authorized: no

## Provenance

```yaml
provenance:
  authored_by: claude-opus-4.8
  reviewed_by: openai/gpt-5-codex
  de_correlation_bar: cross_vendor_discovery   # different vendor (Anthropic author vs OpenAI reviewer); discovery bar met
  review_access_mode: no_repo_inline           # reviewer saw inline text; citations not repo-verified by the reviewer
  author_ca_adjudication: incorporated 2026-06-16 (all six findings accepted; F1 escalation scope tightened; fitness attack elevated to a rule)
  ca_authority: TRANSFERRED to the vendor lane (OpenAI / GPT) per owner instruction 2026-06-16 — "the vendor will be the new CA for this lane too"
  vendor_ca_closeout: kept 2026-06-16; see docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md
  de_correlation_note: >
    The vendor (GPT) was both the discovery reviewer and is now the CA. The author!=CA axis is
    preserved and strengthened (Claude author vs GPT CA). The reviewer==CA correlation (GPT adjudicates
    GPT's own review) is recorded for owner awareness; it is the owner's call and is not blocked here.
```

## 1. Purpose and Non-Claims

**Purpose.** Give Orca's source lanes one contract for turning a raw capture into a
compact, Judgment-readable view — the *Projected Unit* — without (a) replacing raw
evidence, (b) erasing semantic source structure, or (c) letting projection or
Cleaning perform Judgment.

**What this is.** A **view contract** governing the already-accepted
Data-Capture-owned **Mechanical Source Projection** helper and its **Data Capture
Projection Packet** (`core_spine_v0_data_and_cleaning_spine_boundary_v0.md`). The
*Projected Unit* is a **working name (see OD-7) for the mechanical row view +
projection receipt of the existing Data Capture Projection Packet — not a new object
and not a new pipeline layer.** Its §2 pipeline position and §4 field list are a
**candidate shape, not a ratified schema**: OD-1 installs the Cleaning-facing
input-handle direction, and OD-7 keeps "Projected Unit" as a working label. The
field list still must not be implemented as a standing persisted object.

**Non-claims (load-bearing).**
- **Not a new spine layer.** Promoting Mechanical Source Projection to a standalone
  layer is a named wrong move in the boundary note. The Projected Unit is a derived,
  re-derivable view over raw — not an owner of the signal.
- **Not the source of truth.** The raw capture packet stays canonical; the view is
  always reachable-back to raw and never survives without it.
- **Not ECR / Cleaning / Judgment design, not a schema, not runtime/crawler design,
  not capture execution.**
- **Not validation, readiness, buyer proof, Judgment quality, or platform coverage.**
- **Does not amend accepted doctrine.** Where implementation would widen beyond
  the installed OD-1 input-handle direction or the boundary note, it routes to a
  separate owner decision and Direction Change Propagation receipt.

## 2. Pipeline: artifacts and views over one raw packet

Read this as **one raw packet with derived views keyed to it**, *not* six sequential
owning layers. Ownership is annotated per stage.

```text
Decision Frame  (required upstream; no free-floating evidence)
  -> [1] RAW CAPTURE PACKET            owner: Data Capture Spine
        SourceCapturePacket (CapturePacket) — preserved bytes + hashes; identity/timing/visibility/
        cutoff/archive posture; fidelity + related-context + bundle structure. CANONICAL.
        (key: packet_id / slice_id / sha256+hash_basis)
        |-> [2] ECR RECEIPT             owner: ECR
        |       pre-cleaning receipt + derived integrity reads SP-1/2/3/6;
        |       carry-or-residualize, never author.
        \-> [3] PROJECTED UNIT          owner: source lane (Data-Capture-owned projection helper)
                the Data Capture Projection Packet's row view (WORKING NAME; not a new
                object/layer; candidate re-derived view, working label only): rows + loss ledger +
                raw anchors + projection receipt. Removes source-envelope noise ONLY.
  -> [4] CLEANING TRANSFORM LEDGER      owner: Cleaning Spine
        non-destructive ledger: normalization/translation/summarization, dedupe MECHANICS,
        clustering MECHANICS; raw-to-cleaned trace. Decides NO credibility/exclusion/strength.
  -> [5] JUDGMENT PACKET                owner: Judgment Spine
        Signal Integrity, Signal Use, uncertainty, counterevidence, discounting,
        exclusion, Decision Strength, Action Ceiling.
  -> [6] RAW PULL-IN                    owner: Judgment Spine (pulls), Data Capture (serves)
        Judgment re-opens [1] when a trigger fires (§8). The view is advisory; raw is authority.
```

**Ordering direction (OD-1, owner direction 2026-06-16):** Cleaning should not
force every transform entry to repeat raw + projection + ECR references. Treat
the Data Capture Projection Packet row view and ECR receipt/read as keyed
siblings over raw for Cleaning purposes, then let Cleaning consume a single
input handle keyed to raw that may attach projection and ECR references when
present. Projection does not own ECR; ECR does not own projection.

## 3. Projection Doctrine Rules

1. **Mechanical, not interpretive.** Projection is a deterministic transform of raw
   into rows. It may add short context notes but must not replace the observable with
   interpretation (obligation contract Ob.6).
2. **Raw is canonical; projection is a view.** Every Projected Unit carries durable
   back-references to raw (`packet_id`, `slice_id`, `sha256`/`hash_basis`) and is
   re-derivable from raw. Raw is never deleted while a projection exists
   (reference-never-merge; re-derive-not-migrate — `ecr_spine_submap_v0.md`).
3. **Remove only source-envelope noise.** Permitted removals are mechanically
   identifiable transport/chrome/scaffolding categories (§5). Removing *evidence rows*
   because they look low-value / low-score / repetitive / embarrassing / bot-like /
   deleted / unhelpful is forbidden (boundary note).
4. **Loss is recorded, never silent.** Every collapse, reorder, flatten, or removal is
   written to a **loss ledger** (§4, §6).
5. **Preserve semantic binding.** Projection keeps the source-meaning bindings intact:
   reply->parent, rating->text, variant->price, term->bundle, channel->call, label->item
   (§6, §9). Flattening a binding changes meaning and is forbidden.
6. **No certification.** Projection self-checks record counts/omissions/warnings/
   missing-continuation markers but do NOT certify the unit as cleaned, normalized,
   deduped, or Judgment-ready (boundary note).
7. **Carry-or-residualize; never author from prose.** Every projected field value is
   carried from the packet or mechanically computed from it; anything absent is emitted
   as a **named residual**, never inferred from prose or invented (`ecr_spine_submap_v0.md`).
8. **Closed, schema-shaped vocabulary.** Projection field/posture values come from
   closed sets (the precedent set by `cutoff_posture` / `archive_history_posture`
   enforcement). Free-text interpretive labels are out of scope.
9. **No downstream effects.** Projection emits none of: credibility, integrity
   classification, discounting, exclusion, Signal Use, Decision Strength, Action
   Ceiling, or semantic dedupe/clustering effects (obligation contract "Forbidden Outputs").
10. **Projection may not decide salience.** What counts as decision-material is
    **frame-bound** (carried from the Decision Frame), **carried** from source-visible
    facts, or **residualized** — never projection's own call. "Compact" may never be
    achieved by judging some evidence unimportant. *(Added per the cross-vendor review's
    fitness attack: "compact + Judgment-readable" is inherently lossy, so the rule that
    salience is not projection's to decide is the load-bearing guard.)*

## 4. Candidate Projected-Unit Fields

> **Candidate shape, NOT a ratified schema.** These are the projection receipt's
> fields for a re-derived view. They must not be implemented as a standing
> persisted object; "Projected Unit" remains a working label for the existing Data
> Capture Projection Packet row view, not durable ontology.

| Field | Why required | Obligating source |
| --- | --- | --- |
| `raw_ref` (`packet_id` + `slice_id`) | Anchors the view to canonical raw; enables pull-in and re-derivation; prevents source-of-truth drift. | reference-never-merge (`ecr_spine_submap_v0.md`); projection receipt (boundary note) |
| `raw_anchor` (`sha256` + `hash_basis`, M1-carried) | Byte-integrity anchor; the view derives from the preserved bytes, never recomputed at projection. | SP-2 inspectability anchor; R2 `hash_basis` |
| `projection_method` + `projection_version` | Makes the mechanical transform auditable and re-runnable; ties to a closed rule surface. | Ob.3 / Ob.4 provenance + mode disclosure |
| `rows[]` with `row_kind` + `parent_row_id` (when nested) | The evidence rows, with the nesting key that reconstructs a tree from flattened rows. | Ob.12 related-context; Ob.6 visible-structure |
| `binding_map` | Preserves source-meaning bindings (reply->parent, rating->text, variant->price, term->bundle, label->item). | Ob.6, Ob.12, Ob.13 |
| `fidelity_state[]` (per dimension: preserved / limited / not_applicable / not_attempted / access_failed / cannot_assess) | Reports per-dimension fidelity (fact, source-language, structure, modality, frame-keyed) so Judgment decides materiality. | Ob.6 |
| `loss_ledger` | Records every removal/collapse/reorder by category, count, and modality-appropriate raw anchor (§6). | boundary note |
| `access_modality_overlay` | Visibility/modality/archive/media state at capture (gated/blocked/deleted/archive-only; HTTP/rendered/screenshot; media present/pointer/failed). | Ob.10, Ob.11, Ob.6 modality |
| `capture_context_ref` | Pointer to capture-context narrative (why choices were made), kept **separate** from posture/field values. | Ob.9 (narrative belongs in `capture_context`) |
| `certification: "view_only; not_cleaned; not_normalized; not_judgment_ready"` | Stops downstream from treating the view as authority or as cleaned. | boundary note; non-claims |
| `residuals[]` (named) | Every absent input surfaced as a named residual rather than silently dropped or prose-filled. | carry-or-residualize (`ecr_spine_submap_v0.md`) |

## 5. What Projection MAY Remove (source-envelope noise only)

Permitted because each is mechanically identifiable and carries no evidentiary signal
— each removal is still logged to the loss ledger with a category, count, and raw anchor.

| Category | Examples |
| --- | --- |
| API / transport envelope | HTTP headers, pagination tokens, rate-limit metadata, request/response wrappers |
| UI chrome / navigation | nav bars, breadcrumbs, sort/filter UI, cookie banners, tracking pixels |
| Report / export scaffolding | cover pages, TOC pages, running headers/footers, page numbers |
| Award / badge / embed scaffolding | decorative award widgets, social embeds, unrelated cross-promo embeds |
| Client-voting / engagement wrappers | reader-injected vote buttons, client-side polling overlays, inline ad slots |

**Hard line:** removing the above must not also remove or reorder an evidence row, a
binding, or a structural cue. If a "noise" element is load-bearing for meaning in a
given frame (e.g., a badge that *is* the sponsored label), it is **not** noise — see §6/§9.

## 6. What Projection MUST Preserve or Anchor

**Preserve (in the view):**
- **Evidence rows** — posts, comments, replies, documents, reviews — regardless of
  apparent value/score/repetition/embarrassment/bot-likeness/deletion (boundary note).
- **Semantic bindings** — reply->parent, rating->text, variant->price, variant->availability,
  term->bundle, channel->call, label->item.
- **Thread / related-context hierarchy** — original/parent claim, signal-bearing reply
  path, corrections/rebuttals/confirmations, official/moderator responses, resolution/
  lock/edit/deletion posture (Ob.12).
- **Bundle / offer structure** — which terms appear together, source-visible framing
  (concession/requirement/condition/sweetener/penalty/sunset), dependencies,
  severability, and sequence across drafts (Ob.13). The atomic unit is the bundle as presented.
- **Visible structure & emphasis** — layout, headings, nesting, grouping, proximity,
  bullet order, emphasis — when they carry signal (Ob.6).
- **Decomposed timing** — publication/edit/capture/re-capture/cutoff kept separate,
  never collapsed (Ob.8).
- **Version/edit/deprecation history** for docs/changelogs/pricing/policy pages (Ob.12).
- **Archive-vs-current / recapture relationship** per slice — never erase prior capture
  history (Ob.10, Ob.15).

**Anchor (back to raw) — modality-appropriate:**
- Durable `packet_id`/`slice_id` on every row; M1-carried `sha256`+`hash_basis`;
  carried (not re-derived) `cutoff_posture`/`archive_history_posture`.
- For each removal/collapse, a **modality-appropriate raw anchor**: byte range,
  packet/slice key, DOM node/path, screenshot region, video/audio timestamp, frame
  hash, or rendered-text span — **or a named residual** when exact anchoring is
  unavailable. *(Per F6: byte ranges alone do not fit multimodal/DOM/screenshot/video evidence.)*

**Loss ledger shape (illustrative, not a schema):**
```yaml
loss_ledger:
  removed: [{category: UI_CHROME, count: 2, raw_anchor: "<byte range | dom path | screenshot region | ...>", reason: "navigation bar"}]
  preserved_evidence_rows: <count>
  preserved_bindings: <count>            # reply->parent, variant->price, term->bundle ...
  timing: separate_not_collapsed         # Ob.8 attestation
  hierarchy_preserved: true|false        # Ob.12 attestation
  structure_preserved: true|false        # Ob.6/Ob.13 attestation
  certification: "removes_source_envelope_only; does_not_certify_cleaning"
```

## 7. Cleaning-Owned Transformations vs Judgment-Owned Inference

The bright line (boundary note): **Cleaning owns the *mechanics*; the moment a transform
affects independence, credibility, uncertainty, exclusion, Decision Strength, or Action
Ceiling, the *effect* is Judgment's.**

| Act | Cleaning may own (mechanics, ledgered, non-destructive) | Judgment owns (inference/effect) |
| --- | --- | --- |
| Normalization | unit/format/encoding/whitespace normalization with ledger | whether a normalized value is credible/usable |
| Translation | translate text, keep source language paired | whether translation changes meaning materially |
| Summarization | a summary that **links back to** rows; never replaces them | whether the summary supports a claim |
| Dedupe | record cluster **membership** + a **mechanical similarity score**; originals preserved; emits NO independence / copied-coordinated / credibility label | whether duplicates mean "copied/coordinated" or "independent corroboration" |
| Clustering | record cluster **mechanics**, keep instances inspectable | whether a cluster is one campaign or N independent sources |
| Inclusion state | propagate a **mechanical, layer-owned status token only** (e.g., `normalization-conflict`, `duplicate-cluster-unresolved`, `translation-trace-missing`) | deciding included/discounted/excluded on credibility/demand grounds |
| Integrity | — (none) | Signal Integrity labels + Integrity Effect (IPF) |
| Demand | — (none) | Demand Rule: engagement != demand (IPF) |
| Strength/Ceiling | — (none) | Decision Strength, Action Ceiling (IPF) |

**Cleaning inclusion-state is mechanical-token-only.** Cleaning must NOT carry
`discounted / excluded / weak / strong / demand-use / credibility / action-supporting`
reasons; those are **Judgment-authored** annotations only. *(Per F4: a neutral-sounding
"inclusion-state reason" must not become a channel for smuggled exclusion/discounting.)*

**Anti-smuggling guard.** Any note of the form *"we removed low-value/bot rows," "0.98
similar so it's one opinion," or "the thread was confusing so we canonicalized it"* is a
Judgment call wearing a Cleaning costume — the mechanics are allowed; the implied
**decision** is deferred to Judgment, with originals preserved so Judgment can re-inspect.

## 8. Raw Pull-In Trigger Table

Pull-in is a first-class Judgment act: the view is advisory, raw is authority. The
gate is split into the **triggering claim type** and the **minimum Action-Ceiling
threshold** (closed IPF rungs only: Watch / Probe / Test / Hold / Move / Commit).
`Always` = claim-type-triggered, ceiling-independent.

| # | Trigger | Why view/Cleaning insufficient | What raw to pull | Triggering claim type | Min Action-Ceiling |
| --- | --- | --- | --- | --- | --- |
| 1 | Cutoff-boundary / backtest claim | collapsed view can't prove pre/post & accretion | per-item timing (Ob.8) + closed `cutoff_posture` (Ob.9) | backtest / cutoff claim | **Always** |
| 2 | Demand read | engagement != demand; costly-behavior + independence must be seen at source | rows + source identity (Ob.7) + modality if layout carries it | demand read | **Always** |
| 3 | Sponsored / paid / vendor-moderated label dependence | Cleaning strips labels; presence/absence is the signal | raw media/visible-structure with badge (Ob.6) + actor (Ob.7) | sponsored-label-dependent read | **Always** |
| 4 | Copied/coordinated or artificial-amplification call | dedupe corrupts independence; re-count from originals | per-instance packets, never merged; cluster links to originals | integrity (independence) call | **Always** (blocks Move/Commit) |
| 5 | Media-dependent meaning | text-only drops visual hierarchy/emphasis/state | preserved media body (Ob.6) + raw anchor | — | Test |
| 6 | Thread hierarchy / correction | flatten/reorder loses who-answered-whom & resolution | original->reply chain + lock/edit/deletion posture (Ob.12) | — | Probe |
| 7 | Archive-vs-current divergence | view may show only current; archive may contradict | both slices + `archive_history_posture` + SP-6 (Ob.10) | — | Move |
| 8 | Deleted/locked content as evidence | deletion posture != the deleted content | archived snapshot body of the deleted/locked state (Ob.10/15) | — | Test |
| 9 | Bundled-offer flattening | separable vs interdependent terms change the read | source-visible bundle structure + framing + sequence (Ob.13) | demand read -> **Always**; else | Move |
| 10 | Version/changelog cutoff | normalized timestamps hide version-at-cutoff | decomposed timing + version/edit/deprecation (Ob.8/12) | — | Test |
| 11 | Gated/ephemeral visibility / fallback access | "was it visible pre-cutoff?"; degraded provenance | visibility facts + access-failed/fallback per locator (Ob.11/Ob.2) | — | caps at Hold/Probe; cannot support Move |
| 12 | Any Move or Commit recommendation | ceiling needs integrity+independence+costly-behavior at source | full per-row packets for the load-bearing set | — | **Move / Commit** |

**Default-to-raw (always open raw regardless of view quality):** any Move/Commit (12);
any demand claim (2); any sponsored-label-dependent read (3); any cutoff/backtest claim
(1); any copied/coordinated or amplification integrity call (4); any archive-only or
deleted-content claim (7,8).

*(Per F5: the gate is no longer a single column mixing ceiling rungs with non-ceiling
terms. "Demand" is a Signal-Use claim type, not an Action-Ceiling rung; "Test+" is now
"Test"; "Hold/Probe (cannot Move alone)" is rendered as a ceiling cap. Any term not in
the closed IPF rung set is owner-open vocabulary.)*

## 9. Projection Families by Information Shape (not platform)

Five content families + one cross-cutting overlay.

> **The "candidate source-envelope" column is frame-conditional, not a blanket safe-list.**
> An item is collapsible **only when it is non-load-bearing for the decision frame,
> logged in the loss ledger, and raw-anchored**; otherwise it is a raw-pull candidate
> and must be carried. *(Per F2: helpful-votes, follower counts, recommendations,
> shipping/loyalty, legal boilerplate, signature names, and filing IDs can be evidence
> in one frame and noise in another — projection may not decide that, per Rule 10.)*

| Family | Must survive (binding/structure) | Candidate source-envelope (collapse only if non-load-bearing for the frame, logged, raw-anchored) |
| --- | --- | --- |
| **Thread / Discussion** (`THREADED_CHAIN`) | parent->reply nesting; related-chain (corrections/confirmations/official-mod responses); per-item edit/delete/lock state; decomposed timing; parent claim for orphaned replies | unrelated branches, pagination & voting chrome; user dossiers/karma are out of bounds (charter, not a collapse) |
| **Review Surface** (`RATED_TEXT_RECENCY`) | rating<->text pairing; recency & experience-timing (when used != publish date); long-context detail; visible moderation/incentive/verified posture; sort-position | gallery embeds, upsell modules; **helpful-vote counts and reviewer-profile facts are frame-sensitive — carry unless proven non-load-bearing (they can be social-proof/integrity signal)** |
| **Social / Video** (`CHANNEL_PUBLIC_OUTPUT`) | channel identity; the channel's **raw public output, captions/framing, and timestamps**; **raw engagement counts + captured baseline facts**; sponsorship/paid label (raw source-visible) | profile aesthetics; **follower counts and reshare volume are frame-sensitive — carry unless proven non-load-bearing** |
| **Retail / PDP** (`VARIANT_PRICE_AVAILABILITY`) | SKU->variant->price binding; variant->availability binding; bundle/multi-pack structure; review-substrate location; per-retailer/locale series; embedded structured JSON verbatim | hero imagery, cart/notify button states; **shipping/loyalty and recommendation modules are frame-sensitive — carry unless proven non-load-bearing** |
| **Org-Motion / Official** (`PACKAGE_STRUCTURE_MEMO`) | document version/amendment; multi-term grouping & line-item adjacency; per-term framing language; dependencies/severability; sequence across drafts; visibility/supersession posture | running headers/footers; **legal boilerplate, signature-block names, and filing index IDs are frame-sensitive — carry unless proven non-load-bearing (IDs are retrieval anchors; boilerplate can carry a binding term)** |
| **Browser-Visible / Access-Mode Overlay** (cross-cutting; rides every family) | visibility state (public/gated/deleted/blocked/ephemeral); capture modality (HTTP/rendered/screenshot/multimodal); archive posture; media availability; layout-dependent meaning | external link resolution, related-URL expansion, discovery beyond the bounded slice |

**Interpretation never enters projection.** Projection carries raw engagement counts,
source-visible labels, timestamps, captions, and captured baseline facts; it must NOT
emit an `anomaly`, `wind-caller`, independence, or demand-relevance label unless that
label is supplied by an upstream accepted source as raw/categorical input — otherwise
it is residualized. The "engagement anomaly," "wind-caller / call-record grade," and
independence determinations are Judgment / outcome-memory, not projection labels.
*(Per F3.)*

**Promotion discipline.** Per the boundary note, any family-specific projection rule is
a **satellite** rule until it survives >=2 non-overlapping families or the owner accepts
it as core. Only the obvious invariants (raw preservation, raw-claim separation,
non-destructive transforms, no-evidence-row-removal, no-salience-decision) are core
without re-proof.

## 10. Specimen Bench Recommendation (smallest set before durable Cleaning Spine design)

Goal: the **fewest messy real captures** that, between them, stress every projection
rule and every default-to-raw trigger — *before* committing durable Cleaning Spine
design. Reuse **existing captures only** (no new external collection). The obligation
contract already names a pressure-test mix; this bench = that mix **plus three
projection-specific stressors**.

**Backbone (from the accepted pressure-test mix — these files are present on `main`):**
1. **One threaded forum/community chain** — `core_spine_v0_data_capture_spine_pressure_test_threaded_forum_reddit_api_pricing_v0.md` — stresses hierarchy preservation + reply-refutes-parent pull-in (trigger 6).
2. **One review surface with recency/long-context tension** — `core_spine_v0_data_capture_spine_pressure_test_review_surface_v0.md` — stresses rating<->text binding + recency + incentive label.
3. **One bundled/multi-term offer** — `core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md` (or the Reddit-API-pricing bundle) — stresses bundle-structure non-flattening (trigger 9).
4. **One changelog/docs/pricing/API page with version risk** — `core_spine_v0_data_capture_spine_pressure_test_docs_changelog_versioned_page_v0.md` — stresses version-at-cutoff (trigger 10).
5. **One archive/history case** — `core_spine_v0_data_capture_spine_pressure_test_archive_history_recapture_v0.md` — stresses archive-vs-current + deleted-content body (triggers 7, 8).
6. **One multimodal/dynamic page** — stresses media-dependent meaning (trigger 5) + the access/modality overlay.

**Projection-specific stressors (the rules most likely to fail silently):**
7. **One dedupe-independence trap** — a set where near-identical rows are actually
   independent (different users/timing/venues) *and* a counter-set that is actually one
   coordinated campaign. The single most important specimen: where Cleaning most readily
   smuggles Judgment (trigger 4).
8. **One sponsored/paid-label specimen** — where a demand read flips depending on whether
   a sponsorship label is preserved (trigger 3).

**Why 8, not more:** each specimen breaks a *distinct* rule or trigger; coverage of all
12 triggers and all 6 families is reached at 8. Adding platforms adds cost without
breaking a new rule — and "all-platform coverage as a prerequisite" is an explicit drift cue.

**Provenance caveat:** the backbone files are confirmed **present on `main`**; their
*contents* were not read in this pass, so confirm each actually exhibits the named
stressor (one cheap Read each) before locking the bench. Specimens 7 and 8 still need a
source selected from existing captures.

## 11. Owner Directions Installed

Owner direction recorded 2026-06-16:

- **OD-1 — Pipeline ordering.** For Cleaning architecture, use one Cleaning input
  handle keyed to raw, with optional projection and ECR references attached when
  present. Projection and ECR are keyed siblings over raw for this purpose;
  neither formally owns the other, and Cleaning transform rows must not carry
  brittle triplicate references.
- **OD-2 — Standing object vs re-derived view.** Projection is re-derived-on-read,
  following the ECR `re-derive-not-migrate` precedent. Persistence requires a
  separate bounded reason.
- **OD-3 — Loss-ledger enforcement.** Loss-ledger obligations are code/schema
  enforced at the producer/write boundary, not merely advisory.
- **OD-4 — Where dedupe/clustering lives.** Cleaning core v0 may record exact
  identity dedupe mechanics only. Near-match dedupe, copied-language grouping,
  and clustering remain candidate/deferred mechanics unless separately owner
  authorized; all independence, credibility, amplification, exclusion, Signal
  Integrity, Decision Strength, or Action Ceiling effects stay Judgment-owned.
- **OD-5 — Projection vocabulary closure.** Behavior-bearing projection fields
  get closed allowed-value sets before code depends on them. Free-form fields are
  for notes only.
- **OD-6 — Family-rule promotion bar.** The >=2-source-family promotion bar
  applies to projection-family rules unless the owner explicitly accepts an
  exception.
- **OD-7 — Naming.** "Projected Unit" is a working label for the existing Data
  Capture Projection Packet row view. It is not durable ontology and should not
  create a second canonical object name.

## 12. Next Authorized Step (smallest complete)

1. **Carry owner OD direction into the Cleaning foundation.** Use the single
   input-handle pattern for OD-1, exact-identity-only core dedupe for OD-4, and
   "Projected Unit" only as a working label for OD-7.
2. **Specimen-bench confirmation** — read-only pass over the §10 backbone files
   (present on `main`) to confirm each exhibits its stressor; select sources for
   specimens 7 and 8 from existing captures. No new external capture.
3. **Bounded source-lane enforcement.** The Reddit helper is the first owner-authorized
   projection enforcement slice. It is a source-family implementation of the view
   doctrine, not a general projection schema, not a Cleaning transform, and not proof
   that other source families are covered.

**Explicitly not next by doctrine alone:** collecting new data, designing a crawler,
writing schema/ECR/Cleaning/Judgment code, generalizing the Reddit helper to other
families without owner authorization, or claiming validation/readiness/buyer-proof.

## Review and Adjudication Provenance

Cross-vendor delegated adversarial artifact review (no_repo, inline), reviewer
`openai/gpt-5-codex`, author `claude-opus-4.8`, `de_correlation_bar:
cross_vendor_discovery`. Author-CA (Claude) adjudication 2026-06-16: all six findings
**accepted**; F1 escalation scope tightened (resolve by reframe; the genuine
ordering/naming question stays owner-gated); the fitness attack elevated to Rule 10.
**CA authority for this lane transferred to the vendor (OpenAI/GPT) per owner 2026-06-16
— the dispositions below are vendor-CA confirmed by the closeout named above, with final
owner confirmation still outside this artifact.**

| Finding | Severity | Disposition | Where folded in |
| --- | --- | --- | --- |
| F1 — Projected Unit behaves like a new object/layer (numbered slot + field schema) before OD-1/OD-7 | critical | Accepted; reframed as the non-canonical view of the existing Data Capture Projection Packet; §2/§4 now carry the installed OD-1 input-handle direction and OD-7 working-label limit, without promoting a standing object | §1, §2 node [3], §4 header |
| F2 — "safe to collapse" overclaims; frame-blind | major | Accepted; column reframed to frame-conditional + logged + raw-anchored; risky examples become carry-unless-non-load-bearing | §9 column |
| F3 — interpretation smuggled into projection (`anomaly`, `call record`) | major | Accepted; projection carries raw counts/labels/timestamps/captions/baseline only; interpretive labels residualized | §9 Social/Video + closing note; §3 Rule 7/10 |
| F4 — `layer-owned inclusion-state reason` too loose | major | Accepted; narrowed to mechanical status tokens; discount/exclude/strength reasons are Judgment-authored only | §7 |
| F5 — raw-pull gate column mixes ceiling and non-ceiling terms | major | Accepted; split into triggering claim type + min Action-Ceiling (closed IPF rungs) | §8 |
| F6 — loss ledger too byte-range-centric for multimodal | minor | Accepted; generalized to modality-appropriate raw anchor or named residual | §4, §6 |
| fitness attack — compact+readable is lossy; salience must not be projection's call | — | Accepted; elevated to §3 Rule 10 | §3 |

**Validation gaps (honest):** the review was no_repo/inline, so the reviewer did not
verify this draft's citations against the actual repo files during discovery. The
vendor-CA closeout confirmed the folded-in closure conditions against the persisted
artifact bytes and found no new blocker/major in the touched delta. This document remains
a candidate kept for owner confirmation; it is not validation, readiness, ratification,
or buyer-proof.

## Non-Claims

This draft does not claim buyer validation, willingness-to-pay, repeatability proof,
product readiness, feature readiness, implementation readiness, Core Spine validation,
Cleaning Spine validation, Judgment Spine validation, Evidence Candidate Record
completion, or Evidence Unit (EvidenceUnit) design completion. It does not authorize implementation,
runtime design, schemas, scrapers, automation, tests, deployment, proof runs, or feature
planning. It does not amend the boundary note or the obligation contract; doctrine
changes route through the owner and a Direction Change Propagation receipt.
