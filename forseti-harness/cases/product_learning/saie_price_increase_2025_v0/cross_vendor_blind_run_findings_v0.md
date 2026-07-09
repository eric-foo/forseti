# Cross-Vendor Blind-Run Findings — saie_price_increase_2025_v0 (dev case)

**Status: product-learning observation record. NOT distilled.**
Observed facts from one by-hand exam run. Derives no harness/method/judgment-quality
claims. Every result is a product-learning observation, not a validated conclusion.

- Case: `saie_price_increase_2025_v0` (Batch 2 **dev** case)
- Harness: `v0_14`
- Recorded: 2026-06-16 (slice 2 dev arm)
- Frozen scoring key freeze hash: `b1f21470303ac1e26b27248c168ad503d0e2e3579546ef0d952e70f1880829ef`

## 1. Scope and cap

By-hand exercise that uses the harness; not judgment-quality. Dev case → may inform
method; run **once**. Packet built outcome-blind in slice 1 (#172); this slice adds the
blind **run** only. Isolation instructed/attested (sub-agent, `tool_uses=0`, web-off by
instruction). `memorization_probe_result` hardcoded `not_run`; recognition collected.
Band inputs facilitator-set (slice 1), owner ratification pending.

## 2. Exam setup

- **Decision question:** at the 2025-06-01 cutoff, should Saie raise DTC prices by $1–4,
  hold, or take a different approach, given tariff cost pressure?
- **Calibrated band from the frozen key: [3, 4], band_status: normal.** Moderate evidence,
  correlated (ceiling 4); floors of 3 from `opportunity_cost: moderate` / `option_value:
  moderate` / `urgency: medium`, dampened to floor 3.
- **Held outcome (hindsight only; roster-stated, not independently verified):** Saie
  **raised** prices and the increase **persisted** into 2026 (named on a later
  tariff-raiser list; brand community posts as action receipts).

## 3. Clean blind run (scored)

| contestant | family | call | vs band [3,4] | recognition | isolation | score id |
|---|---|---|---|---|---|---|
| `claude_sonnet_isolated_subagent_v0` | Anthropic (claude-sonnet-4-6) | **3** | **in-band** | recognized brand = yes; attested no post-2025 info used | sub-agent, `tool_uses=0` | `01KV7TCSVARTGSV0VHT9JYG1S3` |

- **One blocking failure event (`evidence_id_missing`):** as with cocokind, the contestant
  marked its cost-data-gap claim (C4) `load_bearing` with **empty** `evidence_unit_ids`.
  Reported as-is (dev runs once). Substantively in-band; the flag is a citation-discipline miss.
- Evidence-id presence, pre-decision status, and must-address coverage (MA-01…MA-04) passed.

### JSG-08 tell-audit (alignment caveat — read this)
Recognition = yes; attested no outcome use. **Unlike the other two cases, this
contestant's recommendation (raise prices, level 3) DIRECTIONALLY ALIGNS with the actual
held outcome (Saie raised prices).** Disposition: the calibrated band [3,4] — set
outcome-blind in slice 1 — **independently** supports a modest active price move from the
evidence, so the in-band call is supportable without outcome knowledge; and the contestant
explicitly reasoned from the observed $22–$36 price architecture and tariff-pressure
premise. Residual cueing from brand recognition **cannot be fully excluded**. Per the gate
(contamination = demonstrated outcome-USE), there is no demonstrated use → **recorded as
data with this alignment caveat flagged**, not quarantined. This is the case in this slice
most worth a second look if the owner wants to stress-test recognition effects.

## 4. Observations
1. **In-band (3 in [3,4]).** Decision-quality pass on the ladder for this arm.
2. **Recognition + outcome-direction alignment** (see §3). The single most diagnostic fact
   for this case; flagged, not concluded.
3. **Load-bearing absence-claim left uncited** → blocking citation flag (same pattern as
   cocokind).
4. **Dev case_id cue (limitation):** the committed packet's `case_id`
   (`saie_price_increase_2025_v0`, containing "price_increase") is visible to the contestant
   and cues the action direction — relevant given the alignment in §3. Inherited from the
   slice-1-built packet; noted, not corrected.

## 5. Open / not concluded
External arms (GPT-5.5, Grok 4, Gemini) not run. Whether the recognition/alignment is
contamination or independent reasoning is **unresolved** and needs the external arms +/or a
structural memorization probe. No harness/key/method change made or proposed.

## 6. Provenance
- Score: `scores/01KV7TCSVARTGSV0VHT9JYG1S3.yaml` (gitignored).
- Blind judgement: `runs/claude_sonnet_isolated_subagent_v0/run_001/blind_judgement.yaml`.
- Case report: `reports/product_learning/saie_price_increase_2025_v0/case_report.yaml`.
- Packet construction receipt: `packet_construction_receipt_v0.md` (slice-1 outcome-blind build).
