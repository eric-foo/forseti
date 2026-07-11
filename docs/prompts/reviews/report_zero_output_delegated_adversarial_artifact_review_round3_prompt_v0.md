# Delegated Adversarial Artifact Review — Report Zero, ROUND 3 (residual-closure verification)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt (round-3 delegated cross-vendor review of the Report Zero output after the round-2 residuals were patched; couriered externally with the round-3 zip source pack)
scope: >
  The route-out prompt commissioning the round-3 de-correlated, non-Anthropic
  review. Round 2 verified AR-04/AR-05 closed and all recomputations passing;
  four residuals (AR-01a/b/c, AR-02 wording, AR-03 hzq, AR-06 second
  occurrence) were adjudicated and patched. Blocker/major-free on THIS round
  is the D-1 criterion-5 bar; the home lane adjudicates the return.
use_when:
  - Couriering the round-3 pack for review.
  - Adjudicating the round-3 return against the D-1 gate.
authority_boundary: retrieval_only
open_next:
  - docs/research/report_zero/aphrodite_report_zero_review_round1_adjudication_v0.md
  - docs/research/report_zero/aphrodite_report_zero_grade_v0.md
stale_if:
  - The round-3 return is adjudicated.
```

Operator instruction: paste the prompt below into a fresh NON-Anthropic model
session and attach `report_zero_review_pack_round3.zip` (25 files at the
round-3 patched state). Bring the return back for home-lane adjudication.

---

````markdown
# Adversarial Artifact Review — "Report Zero" ROUND 3: verify the round-2 residual closures (zip attached)

## Commission

commission_mode: delegated cross-vendor adversarial artifact review (round 3 — residual-closure verification)
terminal_output_mode: paste-ready-chat (no repo access; everything you need is in the attached zip)
output_mode: paste-ready-chat
review_posture: adversarial — verify each claimed closure yourself
no_runtime_model_recommendation: true

actor_receipt:
  artifact_author_family: Anthropic / Claude (claude-fable-5 authored the artifacts and both patches)
  prior_rounds: round 1 blocker (AR-01..06, all accepted+patched); round 2 blocker (AR-04/05 closed; AR-01a/b/c, AR-02, AR-03, AR-06 residuals accepted+patched)
  controller_requirement: you MUST be a non-Anthropic model family; if Anthropic-family, return BLOCKED_CONTROLLER_NOT_DECORRELATED and stop.
  home_lane: adjudicates your return; your findings are claims, not accepted truth.

## The four residual closures to verify (adjudication record has the detail)

1. **AR-01a:** every corpus claim's `source_refs` now embeds `captured_units`
   — the actual 15-entry {video_id: video_input_hash} map. Verify 30/30 and
   that the hashes match the corpus record table.
2. **AR-01b:** every quote-less transcript receipt was filled with verbatim
   cue text (hzq sales-tier cue; the 13 4OdcF9S6hxU tier-list entries; ctc/eH/
   FB discourse receipts). Note the declared boundary: disclosure receipts
   citing captured watch-packet FIELDS (e.g. `paid_content_overlay:
   not_captured`) are field observations, not speech quotes — that
   classification is adjudicated; flag only if a SPEECH receipt still lacks a
   verbatim quote.
3. **AR-01c:** M2 like sums are now exact and reconstructable: dupe_request
   176, bought-because 39; every contributing intent ref carries its captured
   like count (blank captures marked and counted 0). Recompute both sums from
   the coded files alone.
4. **AR-02:** `adj.similarity_to_buyer_coordinates` no longer says "organic";
   it states a `posture_basis` for keeping `show` (similarity rests on
   coordinates, not organic-ness). Judge whether the stated basis holds; the
   relabel itself is adjudicated.
5. **AR-03:** hzqxkp3OqQw restructured — Sauvage/Y entries rest on the base
   receipt @94840 only; Elixir material moved to `flanker_segments_unresolved`.
   Verify no resolved object still carries flanker-only evidence anywhere.
6. **AR-06:** both run-log occurrences now read 30.

## Also: regression sweep

The round-2 patch touched 12 coded files + the derived claims + report + run
log. Re-verify: all 11 attention rows (they should be UNCHANGED from your
round-2 recompute), total views 552,859, tier 8/2/1, intent totals (14/12/30/
4/4/3/157), withhold texts, synthetic-buyer disclosure, person-level boundary,
and that the 4OdcF9S6hxU receipt rewrites did not alter any tier value except
the two grounding corrections the adjudication record names (9PM Night Out
"(mid)"→"B (spoken)"; Born-in-Roma tier now explicitly attributed to the c11
comment index).

## Verdict + return contract

Return, in order:
- `review_summary` YAML: {round: 3, verdict: blocker|major|minor|clean,
  counts, closure_check: {AR-01a..AR-06: closed|not_closed},
  fabrication_check: pass|fail, confidence}
- Findings by severity (file + location, defect, contract, minimum fix).
- Your recomputations (M2 sums, spot attention rows) with numbers.
- Residual-risk note (lake packets, zip identity — both are known residuals).
- Adjudication note: findings are claims for the home lane.

Do not rewrite artifacts, review strategy, or re-litigate adjudicated rule
choices (granularity rule, field-observation receipt class, similarity
posture basis) — but DO flag inconsistent application or a basis that does
not hold. Findings only.
````
