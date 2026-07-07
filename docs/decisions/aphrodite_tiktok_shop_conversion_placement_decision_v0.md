# Decision — Placement + feasibility of TikTok-Shop creator-attributed conversion capture (v0)

```yaml
retrieval_header_version: 1
artifact_role: Decision record (proposed placement + probe-scope recommendation)
scope: >
  Recommends where a creator-attributed conversion/purchase signal (TikTok Shop
  and similar creator-commerce surfaces) belongs in the source-family taxonomy
  and ontology, and gives a go / no-go / scoped-probe recommendation with named
  limits. Authorizes no capture build; mutates no taxonomy or ontology authority.
use_when:
  - The capture or ontology lane weighs adopting a creator-attributed conversion source.
  - Deciding placement or feasibility for TikTok-Shop / affiliate creator-commerce signals.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_product_thesis_consumer_demand_v0.md
  - forseti/product/spines/capture/core/source_families/README.md
  - forseti/product/spines/foundation/ontology/ontology.yaml
stale_if:
  - The capture/ontology lane adopts, amends, or rejects this recommendation (record the disposition here or in a successor).
  - The entity-resolution spine's build state changes (currently agreed-but-not-built).
```

## Status

`PROPOSED` — a recommendation prepared to answer the scratch cross-lane handoff
(uncommitted, `docs/_inbox/aphrodite_tiktok_shop_conversion_placement_handoff_v0.md`
in a sibling worktree). It is **not ratified doctrine**: it mints no source
family and no ontology type, edits no taxonomy or ontology authority file, and
authorizes no capture build. Adoption is a separate capture + ontology-lane +
owner step (see **If adopted**). Minting a source family is `architecture_doctrine`
(high lock-in); per the Decision Priority rule this record surfaces that fork
rather than auto-deciding it.

## What this decides

Three things, at recommendation grade: (1) **placement** of a creator-attributed
conversion/purchase signal in the source-family taxonomy; (2) the **ontology
record type**; (3) a **go / no-go / scoped-probe** recommendation on capture
feasibility, with named limits.

## Why it matters (grounded)

Aphrodite's fit read today rests on intent/engagement proxies. The controlling
product thesis is emphatic that demand means **costly behavior — payment,
switching, workarounds, churn — never engagement/resonance volume alone**
([thesis:139](docs/decisions/orca_product_thesis_consumer_demand_v0.md)), and
that the moat is **backtestable outcome memory** ([thesis:169](docs/decisions/orca_product_thesis_consumer_demand_v0.md)).
A creator-attributed purchase signal, if capturable, upgrades the fit panel from
intent-proxy to costly-behavior grade and creates outcome memory. That upside is
what justifies a probe — not a build.

## Decision 1 — Placement

**Recommendation:** place attributed creator-commerce/conversion as a **new
sibling family under `social_media/`** (name owner/capture-lane's call —
`attributed_commerce` reads mechanism-true; `tiktok_shop` matches the existing
brand-named convention), scoped to platform-attributed conversion/purchase
events, keyed to `creator_registry` identity, carrying costly-behavior/commerce
semantics. **Do not mint it now** — this is the placement *recommendation*.

**Rationale (on the real taxonomy shape):**
- The existing taxonomy already sits per-platform capture (`social_media/{tiktok,
  instagram,youtube,reddit}`) **and** a cross-platform identity layer
  (`social_media/creator_registry`) as `social_media/` siblings; an
  attributed-commerce sibling is structurally consistent with that.
- The signal is genuinely distinct from both neighbors: `retail_pdp` is
  merchant-PDP / review-widget-shaped (Ulta/Sephora), with no creator attribution
  and no native conversion feed; `social_media/tiktok` is **content-only**
  (videos/comments, sessioned browser). Attributed conversion (units / affiliate
  sales tied to a creator) is neither.
- **Correction to the handoff's premise:** its rationale rests on "source families
  are named by mechanism, not brand." That principle was **not found stated** in
  the source-families tree (searched), and the observed naming is a **mix** —
  `social_media/{tiktok,instagram,youtube}` are brand-named, while `retail_pdp` /
  `vendor_pricing_page` / `fragrance_native_database` are mechanism-named. So the
  placement stands on taxonomic fit and semantic distinctness, not on a
  mechanism-not-brand rule.

**Alternatives:**
- *Extend `retail_pdp`* — rejected: wrong mechanism (merchant-PDP/review widget)
  and wrong semantics (no creator attribution, no attributed-conversion feed).
- *Option C — no new capture family; surface under `social_media/tiktok` + ontology
  only.* If TikTok-Shop data is captured through the **same** sessioned-browser
  TikTok route (new page, same mechanism), the novelty could live entirely in the
  ontology (new Observation type, Decision 2) plus `creator_registry`, with no new
  capture family — **lower lock-in.** The hinge is whether TikTok-Shop / affiliate
  capture is a **distinct route** (shop/affiliate dashboards, creator storefronts)
  versus the same content route. That is a capture-lane fact and is **currently
  unknown**; the probe (Decision 3) should answer it.

**Fork surfaced:** new-sibling-family vs Option C should be settled by the capture
lane once the capture-route question is answered. This record recommends the
new-sibling placement but mints nothing.

## Decision 2 — Ontology record type

**Recommendation:** record the signal as a **new costly-behavior conversion
`Observation` variant** (e.g. `conversion_event` / `units_sold_or_affiliate_sale`)
— an ontology object captured to Bronze and referenced in Silver Authority
(`derived/`) — that:
- uses the existing typed link `Observation —supports→ TrendVector`;
- carries the existing Observation state `integrity_flags` for gameability
  (inflated/returned counts, incentivized/coordinated buys);
- is **attributed to a `creator_registry` identity** (`platform_account_id`) via a
  creator-attribution link, resolved cross-platform by the entity-resolution spine
  (unbuilt — see Decision 3, limit 3).

**Why not the handoff's two framings:**
- *`WindCaller → Call → TrendVector` as the primary type* — that chain is the
  **influence / trend-origination** layer (a wind-caller's early public *call*
  opening a trend). The attributed **seller** here is not necessarily a wind-caller.
  If a given attributed creator *is* a wind-caller, the conversion Observation can
  additionally feed `Call —graded_by→ Outcome`, but the primary record is the
  Observation, not the WindCaller.
- *A "Creator Vault field" as the authority record* — Creator Vault is a
  **generated Silver read layer** (a view/read-model over Silver Vault records),
  not an authority type; making it the source-of-truth inverts the Bronze→Silver
  authority ordering. Creator Vault should instead **surface an aggregate** of
  these observations as a computed read — which is exactly the aggregate,
  attributed-commerce, creator-level read Aphrodite is allowed to sell (its A1
  carve: creator-level reads and aggregate attributed-commerce; never
  person-level dossiers, contact, or export).

## Decision 3 — Capture feasibility

**Recommendation: SCOPED PROBE** (not go, not no-go). Authorize a bounded,
read-only feasibility probe under the measured-ToS posture; authorize **no**
build, pipeline, standing monitor, or crawler.

**Named limits (attribution, coverage, ToS, and the structural dependency):**
1. **Attribution coverage / missingness.** TikTok Shop links sales to creators
   natively **only for shop-active creators**; many fragrance reviewers are
   YouTube-first / not shop-active → structural missingness. The probe must
   **measure coverage against the actual fragrance-niche creator roster** before
   any grade claim.
2. **Gameability.** Inflated/returned sold counts and incentivized/coordinated buys
   must be **integrity-labelable** (thesis manufactured-demand discipline;
   `Observation.integrity_flags`). If they can't be labelled, the signal cannot
   carry a costly-behavior grade.
3. **Cross-platform entity resolution (hard dependency, not a probe deliverable).**
   The TikTok-Shop-creator ↔ YouTube-roster-creator join depends on the
   entity-resolution spine, which is **agreed but not built** (no global stable-ID
   resolver; v0 owns the ID *grammar* only). Without it, attributed conversion
   cannot roll into the existing creator roster.
4. **ToS + capture-lane alignment.** TikTok live is a **thesis-level owner-word GO
   (2026-06-12)**, but the owning capture-lane records still carry the
   pre-ratification NO-GO and owe their own dated alignment; **no dedicated
   legal-notes doc was found** (contra the handoff's "with legal notes"). Any probe
   stays within the measured-ToS / no-standing-crawler / account-cap posture
   (≤10 operating accounts, start ≤5; bounded, self-terminating sessions). The
   TikTok-Shop route binding is capture-lane-owned and must be set there.
5. **Person-level boundary.** The signal must stay **aggregate / attributed-commerce**
   (creator-level reads within Aphrodite's carve), never person-level dossiers,
   contact enrichment, or export — consistent with both the Aphrodite carve and the
   thesis product boundary (org-level / bounded creator-calibration only).

**Probe stop/pivot condition:** if coverage on the target roster is too thin, **or**
sold-counts cannot be integrity-labelled, the costly-behavior-upgrade rationale
collapses → **no-go / defer** to the current intent proxies.

## Non-claims

- Not doctrine. Mutates no taxonomy (`source_families/`) or ontology
  (`ontology.yaml`) authority; mints no family and no type.
- Authorizes no capture, build, pipeline, live-source call, or account use.
- Not validation, readiness, buyer proof, or feasibility proof. The feasibility
  answer is **"probe,"** not "go."
- A recommendation pending capture + ontology-lane + owner adoption; the
  external-platform premises (TikTok Shop natively links sales to creators via
  affiliate/creator-shop links) are the handoff's assumptions, to be confirmed by
  the probe.

## If adopted

- Promote per the handoff (to `docs/prompts/handoffs/` with a retrieval header, or
  fold the disposition into a capture/ontology-lane decision record); record the
  adoption/amendment/rejection disposition here or in a successor (`stale_if`).
- Adoption that actually **mints the family and/or the Observation type is a
  doctrine change**: `architecture_doctrine` (primary), related `output_authority` —
  and must run the Doctrine Change Propagation Contract
  (`.agents/workflow-overlay/source-of-truth.md`) at that time. This record
  deliberately does not.

## Source basis

- Product thesis — costly behavior / moat / measured-ToS / entity-spine-not-built /
  person-level boundary: [orca_product_thesis_consumer_demand_v0.md](docs/decisions/orca_product_thesis_consumer_demand_v0.md) (:139, :169, :189–198, :206–216, :240–242).
- Source families + `retail_pdp` / `social_media/*` / `creator_registry` shape:
  [source_families/README.md](forseti/product/spines/capture/core/source_families/README.md)
  and per-family READMEs (`retail_pdp/`, `social_media/{tiktok,instagram}/`, `social_media/creator_registry/`).
- Ontology types + `Observation` (deferred, `integrity_flags`) + `TrendVector` links:
  [ontology.yaml](forseti/product/spines/foundation/ontology/ontology.yaml);
  no global resolver: `forseti_ontology_backbone_architecture_v0.md:305–321`.
- Creator Vault as generated Silver read layer:
  `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md:8–12,62`.
- Aphrodite A1 carve (sells creator-level + aggregate attributed-commerce; not
  person-level): `forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md:56–83,103–177`.
- Capture ToS posture:
  `forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md:76`;
  `forseti/product/spines/creator_signal/aphrodite_depth_capture_tos_risk_sanity_check_v0.md:64–68`.
