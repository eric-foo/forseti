# CO2 — Unified Retail Portfolio Corpus

## Terminal state

`COMPLETE_WITH_TYPED_DEPTH_GAPS`

CO2 produced one unified Sephora/REVOLVE portfolio corpus. The deterministic
onboarding runner accepted the commission and emitted
`retail_portfolio_onboarding_v2`.

## Durable artifacts

| Artifact | SHA-256 |
|---|---|
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\route_grid_outcome.json` | `825820dc04f8c225cf5ce5a3791b365dca2b6a00fc7bfd9382b91c9d4db346db` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\retail_portfolio_commission.json` | `401b6a3aef7e958dc4c9c114bce15282b5aa67b6af067526eae6a032c98b2a91` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\retail_portfolio_onboarding.json` | `ff2e716f54dcdc775850480a00b548a435e214b117f27352c281c33b90872d94` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co2\depth_bundles.json` | `d31406605d3053e734c8f97225724c924df1c69248b2ceca5c20d419eb657afa` |

## Route and corpus result

- The CO1 authorization board names Sephora and REVOLVE as authorized
  retailers. Sephora remains primary because its admitted grid is complete.
- Sephora's direct refresh reached the page but failed during the screenshot
  step while waiting for fonts. CO2 therefore admitted the hash-verified
  released 44-row complete grid and preserved the refresh failure as typed
  evidence.
- REVOLVE's direct, no-harness-proxy refresh completed at 37/37 rows. Its native
  style-ID set is unchanged from the released grid: 37 unchanged, zero added,
  zero removed.
- `SUMR-WU102` changed from the released `PREORDER` badge to a fresh `QUICK`
  badge with observed availability `available`; its fresh PDP packet is
  preserved separately.
- All 21 released Sephora PDP IDs remain on the admitted Sephora grid. All 37
  released REVOLVE PDP IDs remain on the fresh REVOLVE grid. The released
  packets are therefore reusable at stable retailer-native identity.
- The unified onboarding contains 139 owned parents, 81 retailer listing
  reconciliations, and 48 required verified PDP baselines. Reconciliation is 54
  exact, 15 ambiguous, and 12 unmatched. Ambiguous and unmatched rows are
  retained explicitly rather than converted into false exact matches.

## Four family depth bundles

1. Lip Butter Balm — Sephora `P455936`; REVOLVE `SUMR-WU76`.
2. Jet Lag Mask — Sephora `P429952`; REVOLVE `SUMR-WU1`.
3. Sunlit Vanilla Eau de Parfum — Sephora `P520746`; no REVOLVE listing on the
   admitted grid.
4. Summer Skin Nourishing Body Lotion — Sephora `P469189`; REVOLVE
   `SUMR-WU11`.

The bundle file provides exact grid/PDP pointers where released evidence
exists. It types absent PDP or review-depth packets as gaps. Only the released
REVOLVE Lip Butter Balm deep PDP is available to CO2 as a review-depth pointer;
the other three families require a separate customer-depth corpus. The
released receipt does not establish a review-provider tenant or cross-retailer
corpus identity, so no independence is inferred. Retailer review rows must not
be pooled as independent merely because the retailer names differ.

## Claim limits

- The US-facing surfaces bind US web context, not nationwide stock,
  fulfillment, or absence.
- The Sephora snapshot is the admitted released capture, not a successful
  2026-07-24 refresh.
- The REVOLVE direct result proves that route for this run; it is not a
  permanent reachability guarantee.
- No p05 conclusions, reports, seals, or review outputs were used.
- CO2 did not start Turn B and performed no Git lifecycle action.
