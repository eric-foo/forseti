# Summer Fridays Understanding p06 — Turn A Acquisition Record

```yaml
artifact_role: manually adjudicated Turn A acquisition record
subject: Summer Fridays
cycle_id: sf_understanding_20260724_p06_co
commission_id: sf_understanding_csb_20260724_p06_co
as_of_date: 2026-07-24
runtime_base_revision: 788d583db84c87ebf7a781c564e7f24d1fbdf3e6
topology: CO0_plus_exactly_CO1_CO2_CO3
seal_owner: CO0
phase_a_aim: complete_decision_useful_understanding
phase_b_posture: future_only_smallest_complete
acquisition_gate: BLOCKED_ACQUISITION_INCOMPLETE
deliver_allowed: false
turn_b_started: false
```

## 1. Execution and provenance receipt

Exactly four analytic actors ran in this arm:

| Actor | Owned job | Terminal |
| --- | --- | --- |
| CO0 | integration, fresh evidence verification, and seal adjudication | this record and the acquisition seal |
| CO1 | owned company core, current retailer authorization, and complete owned-product identity | `docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co1_company_core_identity.md` |
| CO2 | unified Sephora/REVOLVE grids, PDP corpus, reconciliation, and depth pointers | `docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co2_retail_portfolio.md` |
| CO3 | customer/community scout and category-balanced retailer-depth attempt | `docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co3_customer_community_depth.md` |

The raw-input release was mechanical, not a fifth analytic actor. Its manifest
at
`C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\release\raw_input_manifest.json`
has SHA-256
`50c03bf390253d7ee31bf608ed799e471e93901e8057452acc2c472200d8f9b0`.
CO0 and CO2 independently verified all 62 named entries by byte length and
SHA-256 with zero failures. No p05 report, conclusion, acquisition record,
seal, or comparison output was used during p06 acquisition.

The commission-stage CSB is
`docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/commission_board.md`,
SHA-256
`ecf4319ec476c065ed41d3f5eed3a37ab7d7a8b087d0974308b53cbb85640546`.
The CSB validator passed before source-heavy acquisition.

## 2. Acquired company and portfolio substrate

### Owned identity and denominator

The released owned surface contains 139 serialized source parents. CO1
adjudicated every source ID exactly once:

```yaml
source_parents: 139
adjudicated_unique: 139
missing: 0
extra: 0
duplicates: 0
unresolved: 0
normalized_product_families: 25
family_member_parents: 66
non_family_parents: 73
family_denominator_state: COMPLETE
```

The non-family parents are separately typed as bundles/sets, samples/gifts,
merchandise, or explicit legacy/other objects. Shade, flavor, and sellable-size
parents are not counted as independent products when the company-owned surface
evidences a shared family.

Primary evidence:

- identity ledger:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\product_identity_ledger.json`,
  SHA-256
  `00756ba1bccd737bc5837aa4023e7860e8dec38ce77a7109a54cc56629ade596`;
- identity fragment:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\portfolio_identity_fragment.json`,
  SHA-256
  `18a871d922b698c1a2f1118c6e50eec85eddfa578785b9ff92feaf75642f54f4`.

### Current authorization, channel, and owned posture

The current company-owned authorized-retailer surface names Sephora and
REVOLVE. Sephora explicitly carries US market text and is the retail primary;
REVOLVE is the selected secondary. The same source also names Amazon, qualified
to the Summer Fridays storefront for the stated guarantee. Authorization does
not establish current listing, stock, fulfillment, or nationwide
availability.

The durable company core supports the current proposition, founders and first
product, channel/geography posture, public price shape, and US subscription
mechanics. Two contextual facts—the 2024 TSG investment/leadership event and
the first-fragrance launch—remain `URL_ONLY_NON_SEAL_BEARING` because no raw
durable source was preserved in this run.

Primary evidence:

- authorization board:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\authorization_board.json`,
  SHA-256
  `2cf90fbe01747f04bf893dafc8a38eb821dd6d17878bd5167d2ae728df5d2421`;
- company core:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\company_core_capture.json`,
  SHA-256
  `c7bca599d156b0f5e9eab62acd485746b446369e22744b0a2a6305b2fe06814a`.

## 3. Unified authorized-retailer corpus

Sephora's 2026-07-24 refresh reached the page but timed out during the
screenshot step while waiting for fonts. The admitted Sephora grid is therefore
the hash-verified released capture: 44 unique parent listings, complete against
its page-declared count.

REVOLVE refreshed directly without a harness proxy: 37 unique listings,
complete against its page-declared count. The native style-ID set is unchanged
from the released grid. All 21 released Sephora PDP IDs and all 37 released
REVOLVE PDP IDs remain on their admitted grids and are reusable at stable
retailer-native identity.

The deterministic `retail_portfolio_onboarding_v2` run passed with:

```yaml
owned_parent_denominator: 139
retailer_listing_rows: 81
exact_reconciliations: 54
ambiguous_reconciliations: 15
unmatched_reconciliations: 12
verified_required_pdp_baselines: 48
primary_retailer: sephora
```

Ambiguous and unmatched rows are preserved rather than promoted to false exact
matches. A CO0 validation rerun exited `0` and reproduced the onboarding output
byte-for-byte.

Primary evidence:

- route/grid outcome:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\route_grid_outcome.json`,
  SHA-256
  `825820dc04f8c225cf5ce5a3791b365dca2b6a00fc7bfd9382b91c9d4db346db`;
- onboarding:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\retail_portfolio_onboarding.json`,
  SHA-256
  `ff2e716f54dcdc775850480a00b548a435e214b117f27352c281c33b90872d94`;
- depth bundles:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\depth_bundles.json`,
  SHA-256
  `d31406605d3053e734c8f97225724c924df1c69248b2ceca5c20d419eb657afa`.

The US-facing storefront state binds US web context. It does not support
nationwide stock, fulfillment, or absence claims.

## 4. Customer and community evidence

The bounded current community scout produced useful pain, usage, objection,
workaround, and contradiction language:

- Lip Butter Balm splits tint/scent/daytime appeal from durable hydration,
  transfer, reapplication, and price/value jobs.
- Jet Lag Mask is frequently used as a rich moisturizer; irritation and
  tolerance accounts conflict and require cautious interpretation.
- Sunlit Vanilla has a clear summer-gourmand sensory image and a perceived
  longevity/layering seam.
- Newer sunscreen and balm discussion contains change anxiety, but does not
  prove a formula change.

No Reddit root was released. Ten bounded JSON routes returned HTTP 403, so the
Reddit evidence remains URL-bound qualitative scouting, not a terminal raw
corpus or representative sample.

REVOLVE supplied one evidenced Yotpo tenant/store and three `Most Recent`
windows:

| Family | Native-unique rows | Substantive text | Rating-only | Incentive posture |
| --- | ---: | ---: | ---: | --- |
| Lip Butter Balm | 50 | 12 | 38 | 50 source-marked non-incentivized |
| Jet Lag Mask | 50 | 2 | 48 | 50 source-marked non-incentivized |
| Summer Skin Nourishing Body Lotion | 50 | 6 occurrences / 5 unique fingerprints | 44 | 47 non-incentivized, 3 incentivized |
| Sunlit Vanilla | 0 | 0 | 0 | not listed on admitted REVOLVE grid |

All three captured product windows share the same REVOLVE Yotpo tenant and are
one provider/retailer corpus family, not independent evidence families. For Lip
Butter Balm, the released 100 Most Recent and 100 Most Relevant windows overlap
on 99 native IDs; p06 admits only the 50-row Most Recent window.

Primary evidence:

- CO3 terminal:
  `docs/research/summer_fridays_understanding_dogfood_20260724_p06/coordinated/specialists/co3_customer_community_depth.md`,
  SHA-256
  `fc91461440552a583bfcecbe3d87a9de5a825b41d5e544da22a9514dd07b95df`;
- Lip rows:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co3\retailer_depth\revolve\lip-butter-balm-most-recent.json`,
  SHA-256
  `8b202653577eed49c167bcc70995ba6698c948267cba07093b0833f1ebe2da5c`;
- Jet Lag rows:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co3\retailer_depth\revolve\jet-lag-mask-most-recent.json`,
  SHA-256
  `7f132a58d3a1e7112bae7bedca8945259b7ec1dac09c4d97bed1755e1d27e597`;
- body-lotion rows:
  `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co3\retailer_depth\revolve\summer-skin-nourishing-body-lotion-most-recent.json`,
  SHA-256
  `cdfbd23d815a66a3097c57d404d1a19b32a91ff64bfc31684eb6ce9f858f2dc0`.

## 5. Acquisition-gate adjudication

### Passed acquisition jobs

- Complete 139-parent owned identity adjudication and 25-family denominator.
- Current company-owned retailer authorization.
- Complete admitted Sephora and fresh REVOLVE grids.
- Unified two-retailer reconciliation with real ambiguity retained.
- Forty-eight verified PDP baselines.
- Bounded current community scout.
- Provider-bound, native-ID-deduped recent review windows for three REVOLVE
  product families.

### Material unresolved jobs

1. **Category-balanced customer depth is below the commissioned floor.**
   Sephora reviews and Q&A are absent for all four selected families. REVOLVE
   supplies no Sunlit Vanilla listing. Across the three captured REVOLVE
   windows, rating-only rows dominate and the per-category substantive-text
   target is unmet: Lip `12`, Jet Lag `2`, body `5` unique, fragrance `0`.
2. **Two material company-event facts cannot bear the seal.** The TSG
   ownership/leadership event and first-fragrance launch remain URL-only
   context without durable raw capture.

These are core Understanding jobs, not optional polish. A fresh-context
Deliver or Problem-Framing consumer would have a materially stronger portfolio
and customer substrate than p05-era raw inputs alone, but would still lack the
category-balanced customer evidence and durable event chronology required to
treat Phase A acquisition as complete.

### Smallest genuine unblock

One bounded completion batch:

1. preserve hash-verified parent PDP packets or safe page-declared
   Bazaarvoice configuration for the four selected Sephora family listings;
2. capture the commissioned Sephora `Most Recent`, `Most Helpful`, and Q&A
   windows, dedupe by native review/question identity, and retain incentive
   posture;
3. durably capture the two already-identified company-event sources;
4. re-adjudicate only the customer-depth and chronology jobs, then the seal.

No additional retailer, nationwide-availability probe, Reddit retry, new actor,
Turn B report, or broad re-run is required.

## 6. Manual result

```yaml
acquisition_state: BLOCKED_ACQUISITION_INCOMPLETE
gate: fail
deliver_allowed: false
reason: material category-balanced customer depth and durable event chronology remain incomplete
smallest_unblock: one bounded Sephora review/Q&A plus two-source event-capture batch
phase_a_complete: false
phase_b_started: false
turn_b_started: false
company_report_exists: false
```
