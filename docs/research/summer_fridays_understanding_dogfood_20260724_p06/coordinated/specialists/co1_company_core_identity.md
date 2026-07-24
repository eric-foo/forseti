# Summer Fridays p06 — CO1 Company Core And Identity Terminal

```yaml
artifact_role: CO1 terminal receipt
actor: CO1
persisted_by: CO0 from the CO1 collaboration final
subject: Summer Fridays
run: summer_fridays_understanding_dogfood_20260724_p06
status: COMPLETE_WITH_TYPED_RESIDUALS
```

## Completed jobs

- Fresh company-owned authorized-retailer capture and authorization board.
- Exact owned-parent identity adjudication.
- CO2-ready normalized portfolio identity fragment.
- Company-core proposition, founders, channel, geography, price, and
  replenishment evidence capture.
- Explicitly non-seal-bearing context for facts without durable raw evidence.

## Durable artifacts

| Artifact | SHA-256 |
| --- | --- |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\official_authorized_retailers_capture.json` | `b94a61114fb91ec674b36fe21677351cfedac1c8f4372dfa1be6480825f5fb29` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\authorization_board.json` | `2cf90fbe01747f04bf893dafc8a38eb821dd6d17878bd5167d2ae728df5d2421` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\owned_identity_relationships_capture.json` | `e7adb433e2cccc25ee014d64b445dbddbb7e65d66f71c93de37108640beb873f` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\product_identity_ledger.json` | `00756ba1bccd737bc5837aa4023e7860e8dec38ce77a7109a54cc56629ade596` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\portfolio_identity_fragment.json` | `18a871d922b698c1a2f1118c6e50eec85eddfa578785b9ff92feaf75642f54f4` |
| `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06\data\co1\company_core_capture.json` | `c7bca599d156b0f5e9eab62acd485746b446369e22744b0a2a6305b2fe06814a` |

## Identity result

```yaml
source_parents: 139
adjudicated_once: 139
unresolved: 0
normalized_families: 25
family_member_parents: 66
non_family_parents: 73
family_denominator_state: COMPLETE
```

CO0 independently compared the ledger and identity fragment to the released
owned census: all 139 source IDs occur exactly once, with no missing, extra, or
duplicate IDs.

## Retail authorization

The current company-owned source names Sephora and REVOLVE as authorized
retailers. Sephora explicitly carries US market text. Authorization does not
prove current route completeness, stock, fulfillment, or nationwide
availability; CO2 owns retailer-route admission.

## Residuals and ceilings

- The TSG investment/leadership and first-fragrance rows in
  `company_core_capture.json` are `URL_ONLY_NON_SEAL_BEARING`.
- No sales, demand, margin, nationwide availability, or global Product-graph
  claim is made.
- Runtime token telemetry was unavailable.
- No blocker remains in CO1.
