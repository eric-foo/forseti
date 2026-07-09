# Source Provenance + Construction Notes — Topicals Enriched Packet v0 (facilitator-side; NOT participant-facing)

```yaml
artifact_role: Facilitator-side provenance + blind-construction record for participant_packet_enriched_v0.md
case_id: topicals_retail_expansion_2021_v0
packet_variant: enriched_v0
cutoff: 2021-03-15
authority_boundary: retrieval_only
```

## Blind-construction attestation

This enriched packet was constructed by the **main lane agent as blind constructor**. The
constructor **has not read** the facilitator-only sealed outcome
(`docs/research/topicals_sephora_expansion_sealed_outcome_facilitator_only_v0.md`) and has
used only ≤2021-03-15 archive evidence. The packet reuses the case's existing **method-agnostic
sealed outcome + cutoff**; it does not reuse the band-scorer participant packets (a new
information set on the same case). The new qualitative C0–C4 read does not use the
FacilitatorLedger / band-scorer runtime, so the prior fixture's `model_valid` debt does not apply.

## Evidence-unit provenance (E6–E11; E1–E5 are stated premises / base rates)

| EU | Capture dir | Snapshot (≤cutoff) | Body sha256 | Displayed signal (body-verified) | Fidelity | Source |
| --- | --- | --- | --- | --- | --- | --- |
| E6 | `source_captures/e6_careers_20210303` | 20210303084505 | db147fc0…0d981b | 1 Supply Chain Manager role | GO (single point) | brand's own careers page |
| E7 | `source_captures/e7_faded_pdp` | 20210210010815 | 49b3ecab…d32154 | "$36", "Based on 54 Reviews", "<span>Sold out</span>" | GO | brand's own product page |
| E8 | `source_captures/e8_like_butter_pdp` | 20210303090202 | ff2db40f…3497b2 | "$32", "Based on 32 Reviews", "Sold out" | GO | brand's own product page |
| E9 | `source_captures/e9_press_index` | 20210303074312 | 02664e7f…42cb5c | press section w/ press-one/two/three; outlets are logos (no text) | PARTIAL (outlets not text-extractable) | brand's own press page |
| E10 | `source_captures/e10_skininfluencers_post1` | 20210303081931 | d2c56059…df4471 | "Top skininfluencers post 1" placeholder, no creators | PARTIAL→empty (template content) | brand's own blog |
| E11 | `source_captures/e11_nordstrom_brand` | 20201109194021 | 8a03c41a…db07a0 | dedicated Topicals brand page present; no product/rating/review data | PARTIAL (presence GO; review-data JS-blocked) | **independent retailer (Nordstrom)** |

All bodies were captured via `run_source_capture_archive_packet.py` (archive_org adapter,
`--timeout-seconds 60–90`; CDX/body retries applied per the archive-runner resilience learnings).

## Source-independence note (facilitator context; the read makes its own gate call)

- **First-party / brand-controlled:** E6, E7, E8, E9, E10 (all on `mytopicals.com`). E7/E8 carry
  the strongest demand-pressure signal (review volume + sold-outs) but are displayed on the brand's
  own surface.
- **Independent origin:** E11 (Nordstrom) — confirms independent national-retailer *placement* only;
  carries **no** independent costly-behavior volume (review-data not archive-recoverable).
- Independent costly-behavior (third-party retailer reviews, community/Reddit) is **absent** from
  this packet — a structural backtest limit (archives do not preserve JS-rendered third-party
  reviews or recoverable community costly behavior for this brand at this cutoff), not a selection
  miss. This is stated, not hidden.

## Spoiler / blind check (for R6)

- The **decision question is spoiler-free** — it names only the generic "broad national beauty-retail
  account," never the specific retailer or the post-cutoff outcome.
- **Nordstrom is the ≤cutoff EXISTING partner** (E2), independently corroborated by E11; it is **not**
  the post-cutoff expansion target and is not a spoiler.
- No EU references any post-cutoff event, retailer, or result.

## What R6 (independent outcome-aware leakage review) must verify

1. No EU (or the frame/decision question) leaks the post-cutoff outcome or the specific future
   expansion target named in the sealed record.
2. The displayed-signal quotes are verbatim-true to the captured bodies (spot-check the hashes).
3. The "independent vs first-party" labels are factually accurate (E11 independent; E6–E10 brand).
4. Return PASS / FAIL **without** disclosing any outcome content to the blind constructor.

## Non-Claims

- Facilitator-side record; `product_learning`. Not validation, not judgment-quality, not a freeze
  (the freeze is the next step). The enriched packet is a new information set on the existing case;
  it does not alter the original frozen band-scorer fixture (additive only).
```text
This is a blind-construction provenance record. It is not a verdict, not a grade, and not proof of
readiness.
```
