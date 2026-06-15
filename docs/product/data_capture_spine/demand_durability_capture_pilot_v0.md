# Demand-Durability Capture Pilot — Result + Series Protocol v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (capture pilot result + runnable series protocol)
scope: >
  Records the live demand-durability capture pilot (what was run, what it proved on real data),
  the runnable protocol for a real over-time series, and the contract-hardening targets the pilot
  identified. Capture-only; INV-1 preserved (no demand verdict). Bounded pilot evidence, not a
  validation or readiness claim.
use_when:
  - Reviewing what the demand-durability capture machinery has been proven to do on live data.
  - Running a real over-time demand-durability series (the protocol below is the runnable shape).
  - Deciding which durability elements to promote in contract hardening.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md   # Lane 1 envelope-delta (Elements 1-5)
  - docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md
  - orca-harness/source_capture/models.py                                          # Capture Envelope of record (schema)
  - orca-harness/runners/run_source_capture_http_packet.py                         # the runner used
  - docs/decisions/distillation_binding_data_capture_v0.md                         # A1c series-diff-on-extracted-values cell
stale_if:
  - The Lane 1 envelope-delta or the price/availability profiles are superseded.
  - models.py is hardened so the durability pins/cold-start/series-diff become first-class fields (then the "rides in capture_context" finding is obsolete).
  - A real over-time series supersedes this pilot's single-window evidence.
```

- Status: `PILOT_RESULT_V0` (bounded live pilot; not validation, not readiness)
- Implementation authorized: the pilot capture below was run under explicit bounded owner authorization (this turn). The **real over-time series** and **contract hardening** are **separate, not yet authorized** here.
- INV-1: preserved — capture records observed facts and their limits only; no demand verdict, no scoring.

## 1. What the pilot ran

A bounded live capture using the **existing harness** (`runners/run_source_capture_http_packet.py` → `fetch_direct_http_capture` → `stage_and_write_packet`), no new runtime built:

- **Target:** Sol de Janeiro Brazilian Bum Bum Cream PDP (`https://www.soldejaneiro.com/products/brazilian-bum-bum-cream`) — a genuinely viral beauty SKU (demand-read relevant); brand DTC on Salesforce Commerce Cloud.
- **Observations:** obs1 (cold-start) + obs2 (recapture, minutes later) → two valid `SourceCapturePacket`s (model-validated on write). Output in gitignored `_scratch/pilot/sdj_obs1`, `sdj_obs2`.
- **Surface / rung:** `direct_http` (stdlib urllib, honest UA), `structured access` mode. HTTP 200, 810 KB real PDP, embedded price JSON. No gate hit (the page served full content; a `captcha` string on the page is an unrelated script reference, not a challenge wall — no gate was defeated).
- **Pins recorded** (in `capture_context`, since not yet schema fields): `session_visibility_pin=logged_out_public`, `locale_pin=en-US`, `currency_pin=USD`, `variant_pin=default-on-page`, `cold_start=true` (obs1), `series_id=pilot_sdj_bumbum_001`.

## 2. What it proved (on live data)

| Element (Lane 1) | Result |
|---|---|
| Capture | HTTP 200, real PDP, 2 schema-valid packets written |
| Price proxy | per-variant prices extractable from embedded JSON (cents): **$12 / $24 / $36 / $44 / $48** |
| Availability proxy | mixed at variant granularity: `in_stock` ("add to cart" ×15) + `waitlist_open` ("Notify Me" ×3) |
| Pins (Element 1) | `variant_pin` load-bearing (5 variants), `currency_pin`=USD, session/locale pinned |
| Cold-start marker (Element 2) | obs1 marked series origin (`series_id`) |
| Series-diff (Element 3) | obs1 vs obs2: raw body sha256 differed (`4c642d15…`≠`e80a1e03…`) but extracted price+availability identical → **no demand-relevant change** |
| Cadence (Element 4) | declared via `cadence.py` `build_cadence_plan`: fixed daily ×14 (offsets `0 → 86400 → … → 1123200s`) |
| Temporal regime (Element 5) | **forward-only** (live SFCC PDP; no native history) → cold-start cap inherent for the pre-coverage window |

**Two structural findings:**

1. **The profiles are implementable on the *shipped* envelope.** The new pins rode in `capture_context` with no schema change — so **contract hardening is optional, not a prerequisite** to begin capturing. Hardening is an enforcement upgrade, not an unblock.
2. **Series-diff must key on extracted values, not raw bytes** (the load-bearing refinement). The raw `PreservedFile.sha256` diverged purely from page chrome (CSRF / cache / session) while the extracted demand-relevant values were byte-identical — so a raw-hash-only series-diff would emit a false "change" on essentially every re-observation. Distilled as `GUARD series-diff-on-extracted-values` (`node:capture-series-diff-change-detection`) in `distillation_binding_data_capture_v0.md` (A1c). Element 3's raw-hash anchor is a coarse "inspect" flag; the extracted-value comparison is the change signal.

## 3. Runnable series protocol (for the real over-time series)

What a real demand-durability series runs, per source SKU:

1. **Select** the SKU + source surface; **probe-then-pin** the cheapest working rung (A1b): `direct_http` first; escalate to `anti_blocking_http` if a naive-UA block appears; **STOP** at any auth / CAPTCHA / Cloudflare *challenge* (no gate defeat) and pin an alternative source or an archive rung.
2. **Hold the pins fixed** across the series: `session_visibility_pin`, `locale_pin`, `currency_pin`, `variant_pin` — a change in any one breaks comparability and must be recorded, not silently absorbed.
3. **Mark cold-start** on obs1 (`series_id`, `cold_start_at`, `pre_coverage_history_posture`); classify the **temporal regime** per slice (forward-only here; retroactive-native if an archive/Keepa addendum extends history backward — record the source as the basis).
4. **Sample on a declared cadence** (`build_cadence_plan`); record realized vs intended timings; record gaps as visible limitations (an un-sampled gap is **never** "no change").
5. **Series-diff on EXTRACTED values** (A1c): extract per-observation price + availability (variant-keyed); the change signal is value inequality across observations; the raw `sha256` is only a coarse "differs → inspect" flag; record `tamper_deletion_visibility` (`source-visibly marked` | `inferred-from-divergence-only` | `cannot_assess`).
6. **Stop conditions:** gate encountered → re-probe / switch source (record the limitation); extraction layer absent for a surface → record raw-hash divergence as inspect-flag + `tamper_deletion_visibility=cannot_assess`, never as a confirmed change.

Capture emits observed facts + limits only; whether the series shows durable vs hollow demand is downstream Judgment (INV-1).

## 4. Contract-hardening targets the pilot identified

For the hardening pass (promote spec prose → enforced `models.py` fields / obligations), the pilot ranks these by demonstrated load-bearing-ness:

- **Pins (Element 1)** — `session_visibility_pin` / `locale_pin` / `currency_pin` / `variant_pin` as first-class `VisibleFact` fields (rode in `capture_context` in the pilot; `variant_pin` proved essential with 5 variants).
- **Cold-start marker (Element 2)** — `series_id` / `cold_start_at` / `pre_coverage_history_posture` as series-origin fields.
- **Series-diff (Element 3) — with the A1c refinement baked in:** the change anchor is the **extracted-value comparison**, not raw `sha256`; harden the extracted-value record + `tamper_deletion_visibility`, and demote raw-hash to an inspect-flag. (Fold the Element-3 spec-text sharpen here.)
- **Cadence (Element 4)** — intended `CadencePlan` + realized timings + gap limitations as series fields.

Hardening is **owner-gated and out of scope for this pilot record**; this section names targets, it does not authorize the schema change.

## 5. Caveats / limits

- **Single window:** only two observations minutes apart → **no over-time change demonstrated**; the durability read accrues across the real series (§3), not from this pilot.
- **One SKU, one surface:** `direct_http` worked cleanly for SdJ (SFCC served 200 + embedded price JSON). Big retailers (Sephora / Ulta / Nordstrom) likely need `anti_blocking_http` or an archive fallback — unproven here.
- **Pins in `capture_context`:** recorded as free-form text, not first-class fields (pending hardening); machine-keyed comparison is therefore not yet enforced.
- **Capture-only:** no demand verdict, no scoring (INV-1). Search-interest + review proxies remain **conditional on sourcing** (AR-04) and were not exercised.
- Pilot artifacts live in gitignored `_scratch/pilot/`; this doc is the durable record of their facts.

## Non-claims

This is not validation, readiness, acceptance, Data Capture Spine acceptance, contract hardening, source-of-truth promotion, buyer proof, judgment-quality evidence, a demand verdict, a real over-time series, runtime/scheduler authorization, or commercial-readiness evidence. It is a bounded live-pilot result + a runnable series protocol + identified hardening targets, recording observed facts and their limits under INV-1.
