# SoV Extraction-Quality Eval Report (v0) — 2026-07-03 substrate

```yaml
retrieval_header_version: 1
artifact_role: Operational measurement record (docs/workflows/)
scope: >
  First measured baseline for whether share-of-voice numbers over the current
  lake can be trusted at the extraction layer: substrate snapshot, transcript
  resolvability, brand knowledge-leak scan (upper bound), unknown-brand rate,
  and the structural findings a SoV consumer needs (orphaned IG-reels records,
  missing window-timing fields). Produced by the read-only runner
  orca-harness/runners/run_sov_extraction_quality_eval.py.
use_when:
  - Deciding how far to trust brand-level SoV readouts over today's evidence.
  - Prioritizing the brand-catalog / canonicalization and cohort-pilot decisions.
  - Re-running the eval after the substrate grows (recheck recipe below).
stale_if:
  - New capture/extraction batches land (rerun; rates are substrate-bound).
  - The extractor rubric or mention record shape changes.
  - A Cleaning-owned brand canonicalization decision lands.
authority_boundary: retrieval_only
non_claims:
  - not extractor recall/precision (ground-truth labeling deferred; owner labeling-source decision open)
  - not validation, readiness, acceptance, or buyer-proof evidence
  - leak matching is casefold substring; spelling/diacritic variants count as leaks (upper bound)
run_provenance: >
  2026-07-03, read-only over F:\orca-data-lake (524 committed packets), runner
  landed in the same change set as this report; rerun with
  `python orca-harness/runners/run_sov_extraction_quality_eval.py --root <ORCA_DATA_ROOT>`.
```

## The numbers (2026-07-03 run)

| Measure | Value |
| --- | --- |
| Committed packets (total / youtube) | 524 / 465 |
| Mention records visible by-key (committed anchors) | 31 — all `source_backed_complete` |
| Mention records on disk but OUTSIDE committed availability | 15 (see F3) |
| Mentions in scope (named-brand / unknown-or-blank) | 102 / 20 (unknown rate 16.4%) |
| Records with resolvable caption transcript | 23/23 attempted (`resolved_caption_json3`); 0 unscannable named mentions |
| Named mentions scanned for brand-in-transcript | 102 |
| Brand present in transcript | 93 |
| **Brand absent from transcript ("leaked")** | **9 → leak rate 8.8% (upper bound)** |
| Records with `captured_at` / `observed_at` (in scope) | 0 / 0 (see F4) |

## Findings

- **F1 — leak rate 8.8% is an upper bound, and most of it looks like surface-form
  variance, not invented brands.** The nine leaked samples are dominated by
  abbreviation/spelling/diacritic mismatches between the emitted brand and the
  spoken text: `YSL` vs "Yves Saint Laurent" (both directions), `Bvlgari` vs
  "Bulgari", `Stephane Humbert Lucas` vs "Stéphane…". These are honest
  attributions the exact-substring check cannot match — the same variance that
  fragments SoV rows under `exact_string_v0` grouping. A genuine
  knowledge-leak share (brand truly never derivable from the transcript)
  requires the deferred ground-truth pass. Consequence: the highest-leverage
  fix is a **versioned brand/line catalog** (Cleaning-owned canonicalization,
  the field contract's existing upgrade trigger) — it collapses variant rows
  AND turns most of this leak class into matchable attributions. Per-mention
  web search at extraction time stays rejected: unauditable, non-rebuildable,
  token-costly; a web search's proper place is offline catalog curation.
- **F2 — unknown-brand rate 16.4%** (20/122 in-scope mentions). Visible as
  `unknown` rows per the contract; brand-level SoV is usable with that
  disclosure, and the catalog would attribute a share of these (line named,
  brand unstated).
- **F3 — 15 of 46 on-disk mention records are invisible to every by-key
  consumer.** They are IG-reels ASR-route records anchored by platform
  shortcode (e.g. `DF3CdyJv79A`) instead of a committed packet id, so
  availability-walking consumers (including the SoV readout) never see them.
  They also hold all the `captured_at` values observed on disk. Owner decision
  needed (separate unit): migrate/re-anchor, backfill, or accept as
  out-of-lake-scope for metrics.
- **F4 — window-timing fields are absent from the in-scope substrate.** 0/31
  records carry `captured_at` or `observed_at`. `capture_time` SoV windows
  work solely via the packet-manifest `timing.capture_time` fallback
  (universally present, by design); `source_publication_time` readouts are
  fully `unavailable_with_reason` today and stay so until publication evidence
  lands on records or manifests.
- **F5 — small sample, one batch.** All rates come from a single
  operator-dispatched youtube caption batch (31 records / 122 mentions);
  ongoing tier-1 monitoring is not yet running. Treat every rate as a
  small-sample estimate.

## Advisory reading (not a verdict)

- Brand-level SoV over caption-route YouTube evidence: **usable now at
  product-learning tier** with the two disclosures a readout already carries
  (unknown-rate, fragmentation) plus this report's leak upper bound. Not
  buyer-proof tier.
- Publication-time SoV windows: **not usable** until publication timing
  evidence exists (F4).
- Highest-leverage next moves, in order: (1) versioned brand/line catalog
  decision (Cleaning-owned; collapses F1+F2 and de-fragments SoV rows);
  (2) fully-transcribed pilot cohort + first real SoV readout; (3) ground-truth
  labeling pass (recall/precision; owner labeling-source decision open);
  (4) F3 orphan disposition.

## Recheck recipe

```text
python orca-harness/runners/run_sov_extraction_quality_eval.py --root <ORCA_DATA_ROOT>
# JSON to stdout; leaked_samples carries clickable refs (anchor/record/mention_id)
# for spot-checking any leak against its transcript.
```
