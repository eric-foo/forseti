```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt (docs/prompts/handoffs/) — judgment-lane creator-momentum discriminability backtest commission
scope: >
  Owner-authorized cross-lane commission for the judgment lane to set up the discriminability
  backtest of the creator-momentum wedge on the recommended dataset stack: can EARLY signal sort
  DURABLE from TRANSIENT creator momentum, beating a "hottest-now" baseline. Carries the dataset
  roles + the load-bearing commercial-clear / research-only license split, the blind-backtest
  design, and the ontology-spine / satellite routing as a judgment-lane-owned consideration.
  Product-learning only; not buyer proof.
use_when:
  - The judgment lane picks up the creator-momentum discriminability backtest.
authority_boundary: retrieval_only
authored_by: Main CA (capture-spine / home), 2026-06-12
open_next:
  - docs/research/creator_momentum_data_landscape_v0.md
```

# Judgment Lane Commission — Creator-Momentum Discriminability Backtest v0

## 0. Commission and authorization
Owner-authorized 2026-06-12. This commissions the **judgment lane** to stand up the
discriminability backtest for the creator-momentum wedge. **Product-learning only** — no buyer,
readiness, or validation claims; discriminability is a *possibility* to be tested, not a reliability
claim. Run your own preflight + Cynefin routing. Dataset authority + license facts:
`docs/research/creator_momentum_data_landscape_v0.md` (read first; confirm licenses against the
providers before any shippable use).

## 1. Goal (the make-or-break hypothesis)
Test, cheaply and **blind**, whether **early** signal (a creator's first-window trajectory +
engagement-quality) can **sort DURABLE from TRANSIENT** creator momentum, **beating a naive
"hottest-now" baseline** (rank by current peak engagement). Durable = sustains; transient = real but
short-lived (rideable short-term, not "bad"); manufactured = bought/fake (separate axis, out of
scope here). If early signal can't beat the baseline at predicting durability, the wedge needs a
rethink — so this is the decisive test.

## 2. The dataset stack — by role + LICENSE SPLIT (load-bearing)
| Dataset | Role | License | Use rule |
|---|---|---|---|
| **Global YouTube Trending 2022–25** (Illinois Data Bank) | **backtest spine** — real 3-yr daily trajectory, same videos | **CC-BY (commercial-clear)** | prove the method on real trajectories |
| **tarekmasryo YT/TikTok Trends 2025** | **quality benchmark** (like/comment/share/**save**-rate) | **CC-BY (commercial-clear)** | quality classifier; shippable |
| **ksb2043** (Kim, WWW'20) | IG validation (beauty-categorized) | **research-only** | **validation only** — never a shippable claim |
| **TikTok-10M** (HF) | quality classifier (richest free signals) | **research-only** ("other") | **validation only** |
| **CreatorDB** | commercial history + quality | application-gated | **VERIFY FIRST**: as-of-then history? authenticity historical? commercial-reuse license? — gate before any purchase/reliance |

**Rule (do not violate):** prove/develop anything that could **ship** on the **commercial-clear**
sets (Global-YT-Trending, tarekmasryo). Treat **research-only** sets (ksb2043, TikTok-10M) as
**validation only**. Get any commercial license in writing before relying on it.

## 3. Backtest design (the shape; you own the harness)
- **Blind judge:** the predictor sees only the **early window**; outcome labels are assigned by
  **current lookup AFTER** the prediction (no outcome contamination).
- **Spine:** Global-YT-Trending — label durable vs transient by **trajectory persistence**
  (sustained trending presence vs spike-and-die). *Caveat to carry honestly:* this is trending-list
  **presence** (a visibility proxy), not organic follower trajectory, and YouTube is not the core
  surface — it proves the **method**, not the platform signal.
- **Cross-surface validation:** ksb2043 (IG) — label durable/transient by looking creators up now.
- **Quality classifier (v0):** develop "what high-quality engagement looks like" on
  TikTok-10M / tarekmasryo (engagement-quality, esp. save/share-rate), and fold it into the early
  signal.
- **Baseline to beat:** "hottest-now" (rank by current peak). Report whether early-signal +
  quality-classifier sorting **beats** it, with the numbers.

## 4. Ontology-spine / satellite routing (your call)
Consider whether the **creator/entity + durable/transient LABEL ontology** for this backtest should
be defined **through the ontology spine's satellite** (per your spine/satellite architecture) —
so the entities and labels are canonical and reusable across surfaces — rather than ad-hoc to this
one backtest. This is a **judgment-lane-owned** decision: route it through the satellite if that's
where the ontology belongs, or keep it local and say why. The commission does not prescribe the
architecture.

## 5. Boundaries
Product-learning only; fresh-context blind judge (no outcome leakage). Shippable work on
commercial-clear data only; research-only = validation. No buyer / willingness-to-pay / readiness
claims. The capture moat is **judgment + cleaning**, not the data — anyone can buy the raw forward
data; this tests whether the *judgment* discriminates.

## 6. Return contract
Report: the **discriminability result** — does early signal beat the hottest-now baseline, and by
how much (the numbers / the metric you chose); the **labeled backtest design** (windows, labels,
baseline); the **quality-classifier v0**; the **CreatorDB verify outcome** (the three gates);
your **ontology-spine routing decision**; and the **wedge implication** (deepen / pivot /
forward-build).

## Non-claims
A commission, not validation/readiness/acceptance/buyer-proof; grants no authority outside the
judgment lane's own; license facts are as-found 2026-06 and must be confirmed with each provider
before commercial reliance; the "no buyable longitudinal panel exists" finding is a search result,
not proof of non-existence.

```yaml
thread_operating_target_continuity:
  carried_forward: no
  reason: different_workstream
  changed_from_input: no
  lifecycle_status: not_applicable_cross_lane_commission
```
