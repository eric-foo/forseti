# Report Zero — Bounded-Effort Run Log (D-1 criterion 6)

```yaml
retrieval_header_version: 1
artifact_role: Research record (bounded-effort receipt for the Report Zero hand-run — recorded during the run, not reconstructed)
scope: >
  What the D-1 dress-rehearsal extraction actually cost: reads, steps, time,
  exceptions. Proves repeatability posture rather than a heroic one-off.
use_when:
  - Grading D-1 criterion 6.
  - Sizing the speed-2 durable build (this is the sizing input).
authority_boundary: retrieval_only
```

```yaml
report_zero_run_log:
  extraction_recipe_version: aphrodite-rehearsal-extraction-v1
  extraction_model: claude-fable-5 (hand-run, model-in-session; NO API key, no daemon runner)
  corpus_record: docs/research/aphrodite_report_zero_corpus_v0.md
  corpus_input_hash: 0362007ee16d7466ef0ca3ef9973d841727d24f0bb75ca5aa15843c219871ed5
  buyer_intake_sha256: 3adf664bb9a478e1e739345c34430f59c7837f33ec0afb7bf1ff5b17ac3eb73b
  started_at: "2026-07-09T18:38:40Z"   # corpus freeze committed; extraction began immediately after
  ended_at: "2026-07-10T03:52:00Z"     # corpus-level claims + panel projection written
  wall_clock_note: >
    ~9.2h wall clock INCLUDING one session interruption/resume mid-run (after
    video 14's substrate read) and the operator conversation cadence of an
    interactive session; active extraction effort was the large majority.
  videos_read: 15 of 15 (full transcripts + full 40-comment samples + watch subsets, in recipe order)
  video_ids: [ctcEju1AvGw, m-cJ9GVzzbc, eH93HPAWucE, 8QpC36Q_eeM, q0oiKqeghks, FBda5R_1GGg, 4OdcF9S6hxU, V7q8PrAebz8, _FUdh1ryqWI, hzqxkp3OqQw, sw34VzzWlvA, lecfbS6qOIw, nySgot9sqMY, tVUqAYGT3SE, 1N44B-O7VzE]
  transcript_words_read: 53749
  transcript_segments_coded: ~160 product-mention segments (per-video product_mentions arrays)
  comments_coded: 600 (40 x 15; intent label + texture per comment)
  claims_emitted:
    corpus_level: 29 claim types (aphrodite_report_zero_derived_claims_v1.json)
    per_video_records: 15 coded.json files (rehearsal-grade claim storage, speed-1)
    panels_projected: 5 (aphrodite_report_zero_sprint_report_v0.md)
  withholds_emitted: 7 honest withholds (clone-tail rollup, niche-share trajectory, matched reception pairs, 4 momentum types) + 5 reference products displayed as not-observed
  unresolved_product_mentions: ~150+ distinct products; resolved coverage 11/16 reference products, <10% of distinct mentions
  operator_steps:
    - lane setup off origin/main (668b0e0d) + fresh reads of charter/panel-design/provenance-contract/recipe-adjudication/ontology
    - recipe v1 authored from the adjudicated second opinion (M1-M4 normative) and committed (b4acdd32)
    - lake located via ORCA_DATA_ROOT (F:\orca-data-lake); 54 packets found+verified by a delegated Sonnet worker (read-only)
    - corpus freeze: canonical-pick (newest complete per video), mechanical normalization (authors dropped), five-hash chain computed by scratch script; corpus record + synthetic intake committed (a04270b6)
    - hand-run extraction: per-video read (cues -> comments -> watch) then immediate persist of coded.json, 15 iterations
    - corpus-level synthesis: 29 claim types aggregated from the 15 coded records
    - panel projection: five-panel sprint report for the synthetic buyer, dupe-first reading order
  exceptions_or_surprises:
    - comment like_count arrives as strings incl. whitespace and K-suffix; freeze script initially crashed -> fixed by hashing VERBATIM raw strings (lossless) with parsed ints as convenience fields
    - captured comments carry NO platform comment_id -> positional refs (video_id#cNN) minted at freeze; named limitation
    - paidContentOverlay absent from all watch captures (recorded not_captured; never treated as organic proof)
    - short_description truncated ~500 chars in capture -> affiliate inventories are lower bounds
    - 4OdcF9S6hxU transcript (5,410 words) exceeded the single-read cap -> tail handled via targeted grep extraction (documented in its coded.json)
    - one session interruption/resume occurred after video 14's substrate read; durable state (coded files, corpus record) made resume lossless
    - ASR garbles pervasive on clone-house names (Hawas/Has, Rasasi/Rasi, Erba Pura/Herbapura) -> resolved via title/description anchoring, recorded per-video; unresolvable garbles left unresolved rather than guessed
  effort_shape_for_speed2_sizing: >
    The dominant cost is the model reading 54k transcript words + 600 comments
    and coding stance/intent/disclosure — roughly linear in corpus size. The
    mechanical layers (freeze, hashing, normalization) are minutes. Ontology
    resolution was cheap at 16 reference products but is the binding constraint
    on value (resolved coverage <10% of discourse); growing the reference tail
    is the highest-leverage speed-2 investment, ahead of automation.
  non_claims: [not validation, not readiness, not buyer proof, product_learning-capped]
```
