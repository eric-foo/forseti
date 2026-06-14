# Demand-Durability Indicator Capture — Deconfliction Note v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (deconfliction note for the demand-durability indicator capture profile set)
scope: >
  Records, per indicator and cross-cutting, what the EXISTING Data Capture Spine /
  source-observability / source-access-tooling / shipped-harness surfaces already
  cover versus what the four demand-durability indicator capture profiles genuinely
  add. The structural-integrity anchor for the profile set; ensures nothing is
  silently re-specced. Reporting only — authorizes nothing.
use_when:
  - Reviewing whether the four demand-durability indicator capture profiles duplicate existing capture work.
  - Checking what already exists for price / availability / search-interest / review capture.
  - Tracing the keystone-already-exists, price-not-handled, and rename findings.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md       # the keystone (ALREADY EXISTED; consumed, not re-authored). Still says "proxy".
  - docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_search_interest_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md
stale_if:
  - The keystone durability delta, the obligation contract, or the Source Capture packet schema changes.
  - The source-observability requirements boundary decision is superseded.
  - The company-aggregate/EDGAR org-motion lane or the deleted-comment-retrieval decision changes status.
  - price_payload_extraction.py / cadence.py / proxy_profiles.py change what they provide.
  - A new dedicated capture lane for any of the four indicators lands, or a price-capture mechanism that covers retail/promo lands.
  - The "indicator vs proxy" terminology is reconciled upstream (keystone delta / taxonomy / buyer-proof packet).
```

- Status: `DECONFLICTION_NOTE_V0`
- Artifact type: Deconfliction / overlap report (reporting only; authorizes nothing; hardens nothing)

## Why This Note Exists

The commission required, as a validation gate, that **each indicator states its overlap
(or non-overlap) with existing capture lanes and nothing is silently re-specced.** This
note is that gate, made standalone. It also records the **load-bearing structural
finding** that reshaped the deliverable set: the keystone Capture Envelope spec the
commission listed as deliverable #1 **already existed**, so it was **consumed, not
re-authored** — re-authoring it would have been the exact duplication this note guards
against.

Source basis was pinned to the worktree's `origin/main` HEAD at authoring; all
file:line and "already covered" claims below were verified against the worktree copies of
the named sources (the shipped harness code was read, not assumed).

Scope note (owner, 2026-06-15): **demand-durability reading is one decision Orca can help
with, not Orca's whole job** — the engine is outside-in market & competitive intelligence;
beauty consumer-demand allocation is its first application. These four indicators capture
inputs for that one decision-type.

## Terminology — "indicator" (demand side) vs "proxy" (network)

Owner direction (2026-06-15): **"proxy" is reserved for the NETWORK sense** (residential
exit IPs, `ProxyProfile` in `orca-harness/source_capture/proxy_profiles.py`), which is the
more widely-recognised meaning. The demand-side observable formerly called a
"demand-durability proxy" is renamed **"demand-durability indicator"** in this profile set
(files `demand_durability_indicator_*`).

**Upstream ripple (flagged, NOT changed here):** the keystone delta
(`capture_envelope_durability_delta_spec_v0.md`), the demand-read taxonomy, and the
buyer-proof packet still use "proxy" for this same concept. Reconciling that wording is a
**separate, owner-gated pass** (it touches a committed/locked surface set and is
doctrine-adjacent); this commission's scope was the four profiles + this note, so the
upstream rename was not performed. Until it is, "indicator" (here) and "proxy" (upstream)
denote the same concept.

## The Reshaping Finding — Keystone Already Existed

`docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md`
(`DELTA_SPEC_DRAFT_V0`) already exists on `origin/main` and already covers the
commission's entire keystone **and** its cross-cutting requirement:

- It correctly treats the **Capture Envelope of record as already existing** (the shipped
  `orca-harness/source_capture/models.py` packet schema + the obligation contract) and
  re-specs no provenance.
- It specs the five durability-over-time elements: (1) logged-out/locale/currency/variant
  **pinning**, (2) per-series **cold-start marker**, (3) series-level **recapture-diff**,
  (4) **cadence** model (references `cadence.py`), and (5) the **three temporal regimes +
  cold-start-as-inherent-limit-cap** cross-cutting doctrine.

**Consequence:** the four profiles **consume** this delta; this note + the four profiles
are the remaining work the delta was written to feed. No new keystone was authored.
**Coupling consequence:** the keystone is a `DRAFT`, so the four profiles depend on a
draft — if it is revised, their citations need a re-sync pass (owner: "make it durable
later"). Foundation check: the delta's schema and `cadence.py` claims were verified
accurate against the shipped code.

## Cross-Cutting Overlaps (apply to all four indicators)

| Surface | What it already owns | Relationship of the profiles |
| --- | --- | --- |
| **Source Capture packet schema** — `orca-harness/source_capture/models.py` (manifest `_v1`) | All provenance/immutability: `PacketTiming` (decomposed timing incl. `archive_snapshot_time`), `PreservedFile.sha256` + closed `hash_basis=raw_stored_bytes`, closed `re_capture_relationship` (Ob.15), closed `cutoff_posture`/`archive_history_posture` + open `access_posture`/`media_modality_posture` as `VisibleFact`, capture mode/session | **Consumed as-is.** Profiles add **no** provenance field. |
| **Obligation contract** — `core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Capture obligations Ob.1–16, incl. Ob.3 provenance, Ob.6 raw-observable fidelity, Ob.8 decomposed timing, Ob.10 archive posture, Ob.12 **review-surface related-context**, Ob.13 bundled-offer structure, Ob.15 re-capture; the discharge vocabulary; forbidden outputs (no credibility/integrity/scoring) | **Consumed + cited.** Re-speccing it (or hardening it) is owner-gated and out of scope; re-statement would also violate INV-1's no-ECR-by-stealth. |
| **Capture Envelope durability delta** — `capture_envelope_durability_delta_spec_v0.md` | The five durability-over-time elements + temporal regimes + cold-start cap | **Consumed.** Each profile binds the elements; none re-derives them. (Still uses "proxy" wording.) |
| **Source-observability RQ lane** — `data_capture_spine_source_observability_requirements_boundary_decision_v0.md` (current; supersedes the `..._scoping_v0` doc as standalone basis) | Fidelity/inspectability requirements: RQ-01 verbatim/structure (carry-forward-modified), RQ-02 archive-body (split: visibility-now/retrieval-default-deferred), RQ-03 media/multimodal (modality-triggered), RQ-04 access-failure (deferred), RQ-05 source-language anchors (carry-forward) | **Complementary, consumed.** That lane governs *how faithfully a source's content is preserved*; the profiles govern *which demand-signal series to capture*. The review profile consumes RQ-05/RQ-01; archive-body retrieval stays RQ-02-deferred. |
| **Source-access method plan + boundary** — `data_capture_source_access_method_plan_v0.md`, boundary decision | The 11 in-bounds capture methods, discoverable-or-entitled + disclosable standard, measured-ToS accepted, industrial Bright-Data-style scraping rejected, route bindings capture-lane-owned | **Consumed.** Each profile's capture-method options draw from this vocabulary; none amends the boundary or authorizes a method. |
| **`cadence.py` — `CadencePlan`** | A planning primitive (`fixed`/`bounded_jitter`, slot offsets/waits, `to_dict()`) | **Vocabulary borrowed; primitive does NOT fit.** It is intra-session-jitter-scaled (seconds, anti-block spacing between fetches). A durability series needs an **hourly-to-daily** sampling cadence (owner, 2026-06-15) executed by a scheduler/runtime that does not yet exist — a different mechanism, not just a longer interval. The profiles use `CadencePlan` for vocabulary only; building the time-scale primitive is a build/hardening step (out of scope). |
| **`proxy_profiles.py` — `ProxyProfile`** | *Network* proxy config (residential/mobile/datacenter exit IPs + declared `timezone`/`locale` geo for CloakBrowser) | **The reason "proxy" is reserved for network** (above). Its declared exit-geo `locale`/`timezone` is a **driver** of the rendered `locale_pin`/`currency_pin` — the price/availability profiles record the *effective* rendered values and hold exit-geo constant, or a network-route change silently corrupts the series. |

## Per-Indicator Deconfliction

### Price time-series
- **Already covered — do NOT re-spec:** envelope/provenance; durability elements.
- **NOT covered — price capture is genuinely new here (owner, 2026-06-15: "price is not
  handled").** The shipped `orca-harness/source_capture/price_payload_extraction.py` is a
  **narrow, source-specific** extractor (bound to one SaaS pricing-page shape —
  OpenAI/ChatGPT tiers) and does **not** handle Orca's demand-durability price capture
  (retail/beauty, promo separation, multi-source). Only its generic
  `extract_object_at_anchor` brace-matcher is reusable as a **utility**. Do not treat the
  existing extractor as "price handled." Its browser-free recovery is **proven on one
  SaaS source only and unproven for beauty retail**, so **rendered capture may well be
  required** for beauty — the commission's "price requires rendered capture" is therefore
  *open*, not a settled over-statement.
- **Genuinely new:** the **list/effective/promo separation** for retail/beauty;
  member-vs-logged-out pinning for membership brands; the price regime classification; the
  event-triggered-pricing / price-driven-rerouting read-trace.

### Availability / restock
- **Already covered — do NOT re-spec:** envelope/provenance; durability elements; the
  source-agnostic embedded-payload brace-matcher (`extract_object_at_anchor`) is a
  reusable utility.
- **Genuinely new:** the **variant-granular `stock_state` vocabulary**, restock/sellout
  event binding to the series-diff, the **forward-only hard cold-start cap** framing (no
  retroactive source exists), and the **scarcity-theater flag-don't-conclude** integrity
  posture. **No existing capture lane covers availability/restock** as a dedicated
  indicator (confirmed by source sweep).

### Search interest
- **Already covered — do NOT re-spec:** envelope/provenance; durability elements.
- **Genuinely new:** the **relative/re-normalized series facts**, the **entity/topic-ID
  (not raw string)** pin, the **pull-date** pin + per-pull snapshot discipline, and the
  explicit **attention-caps-ceiling / cannot-clear-the-floor** read-trace. **No existing
  capture lane covers search interest** — and it is a **named G1 *unsourced gap*** in the
  Demand-Substrate Hard Gate. This profile scopes the capture side of that gap; it does
  not close the gate's sourcing decision (owner-owned).

### Review velocity / corpus
- **Already covered — do NOT re-spec:** envelope/provenance; **Ob.12 review-surface
  related-context** — *cited and extended* for the durability series, not restated;
  RQ-05/RQ-01 source-language/verbatim; durability elements; the deletion-by-disappearance
  facility (delta Element 3 series-diff).
- **Genuinely new:** the **review arrival-cadence series**, **per-review reviewer-metadata
  for farm-detection-enablement** (corpus, not count), the **`truncation_posture`**
  first-class limitation, and the read-trace tying review velocity to the costly-behavior
  floor with J-curve/FTC/farm flags.
- **Explicitly OUT (do NOT re-spec — owner-dropped):** deleted-review **body retrieval**
  from third-party archives is `DROPPED`
  (`docs/decisions/data_capture_spine_deleted_comment_signal_retrieval_scoped_doctrine_decision_v0.md`,
  2026-06-08). The review profile authorizes only **detecting a deletion by its
  disappearance across Orca's own forward snapshots** (using text Orca already captured
  before deletion), never re-fetching a deleted body — staying inside the existing no-body
  hard stop.

## Deferred (commission scope) — Distribution / Org-Motion + Repurchase

- **Distribution / org-motion is DEFERRED and is NOT re-specced here.** It is owned by the
  **company-aggregate forward-signal capture lane**
  (`docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md` +
  the shipped `feat(company-aggregate)` EDGAR/headcount work): an append-only,
  entity-keyed, official-first (EDGAR/Companies House) + LinkedIn-fallback observation
  series. If org-motion is later folded in, the task is to **deconflict with that lane**,
  not redesign it. It shares the **standing-capture obligation-home gap** below.
- **Repurchase indicators are DEFERRED** — they piggyback on the price + review profiles;
  no separate scraper spec was stood up.

## Live Consequence — Standing-Capture Obligation Home (owner-confirmed)

**Owner decision (2026-06-15): continuous monitoring of these indicators IS wanted.** That
makes the following a **confirmed prerequisite/blocker**, not a hypothetical:

- The v0 obligation contract scopes **commissioned capture only** (tied to a specific
  Decision Frame). Standing/opportunistic corpus capture is **explicitly routed out** of
  v0 to a "Candidate Signal Intake / Corpus Intake contract" that **does not yet exist**.
- The company-aggregate/EDGAR lane already hit this and surfaced it as a build blocker
  (its forward series is standing capture).
- The taxonomy's calling sequence (open transient → **monitor over time** → earn durable)
  and the recurring-decision retainer model both require continuous monitoring. So the
  four indicators are clean for the **one-Decision-Frame** case (where these profiles sit
  today), but **continuous monitoring of them is blocked until a standing-capture
  obligation home is written.**
- **Gating next step (owner-gated, out of this commission's scope):** write the
  standing-capture / corpus-intake obligation home (light or full, per the
  company-aggregate lane's owner refinement — "clarification, not necessarily a heavyweight
  new contract"). The four profiles keep "commissioned capture only" until it lands.

## Structural-Integrity Findings (for the owner / a later reviewer)

1. **Foundation verified.** The keystone delta's claims about the shipped schema
   (`models.py`) and `cadence.py` are accurate; the four profiles rest on real primitives.
2. **Keystone is a draft.** The four profiles are coupled to `DELTA_SPEC_DRAFT_V0`;
   revising it triggers a re-sync (owner: durable later).
3. **Cadence — confirmed hourly-to-daily need.** `CadencePlan` is a within-session
   seconds-scale jitter planner; the indicators need **hourly-to-daily** sampling (owner,
   2026-06-15) plus a scheduler/runtime to execute it — a build/hardening step. (Hourly/
   daily is also why the monitoring is unambiguously *standing* capture — see below.)
4. **Price is NOT handled.** The shipped extractor is narrow/source-specific; treat price
   capture for the demand-durability indicator as genuinely new (owner-confirmed).
5. **Network exit-geo can corrupt a series silently.** A `ProxyProfile` exit-IP change can
   flip rendered currency/locale/stock; pins must record the *effective* values and hold
   exit-geo constant.
6. **Terminology split applied here, ripple pending upstream** (keystone/taxonomy/buyer-
   proof still say "proxy").
7. **Standing-capture obligation home is the owner-confirmed gating blocker** for
   continuous monitoring (above).

## INV-1 Preservation

This note reports overlap and structure only. It introduces no weight, score, ranking,
threshold, or judgment, and re-specs none of the consumed surfaces.

## Non-Claims

Not validation, readiness, acceptance, pressure-test discharge, Data Capture Spine
acceptance, contract hardening, source-of-truth promotion, buyer proof, judgment-quality
evidence, implementation/runtime/tooling authorization, source-access boundary amendment,
obligation-contract amendment, schema change, ECR/Cleaning/Judgment design, or
commercial-readiness evidence. It is a reporting artifact that records what exists, what is
new, and what is deferred for the demand-durability indicator capture profile set.
```
