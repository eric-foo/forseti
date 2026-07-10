# Report Zero — Round-1 Delegated Review Adjudication (D-1 criterion 5)

```yaml
retrieval_header_version: 1
artifact_role: Research record (home-lane adjudication of the round-1 cross-vendor adversarial review return; every verdict below was re-verified against the artifacts before acceptance)
scope: >
  Adjudicates the six findings (AR-01..AR-06) returned by the round-1
  cross-vendor review (reviewer: OpenAI GPT-5; artifacts authored by Anthropic
  claude-fable-5; reviewed at commit 1243642b). Records the per-finding
  verdicts, the home-lane re-verification evidence, the diagnosed root causes,
  and the resolution-granularity rule adopted for the patch. The round-1
  reviewer verdict was blocker — criterion 5 round 1 FAILED; the patch this
  record governs feeds the round-2 re-review.
use_when:
  - Reading why the Report Zero artifacts changed after round 1.
  - Commissioning or adjudicating the round-2 review.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/report_zero_output_delegated_adversarial_artifact_review_round2_prompt_v0.md
  - docs/research/report_zero/aphrodite_report_zero_grade_v0.md
stale_if:
  - The round-2 review return is adjudicated.
```

## Round-1 return summary (reviewer's claims, then home-lane verdicts)

Reviewer verdict: **blocker** (1 blocker, 4 major, 1 minor);
`fabrication_check: fail`; confidence high. Controller de-correlation
confirmed (OpenAI GPT-5 vs Anthropic-authored artifacts). The reviewer had
worktree file access at commit `1243642b` (not the zip pack); the zip-identity
and lake-packet residuals it names are accepted as stated.

Home lane re-verified **every** finding against the artifacts before
adjudicating. All six findings are ACCEPTED (one sub-point of AR-01 partially
rejected). Round-1 criterion 5 outcome: **FAILED — not blocker/major-free.**

| Finding | Reviewer severity | Home-lane verdict | Re-verification observed |
| --- | --- | --- | --- |
| AR-01 per-claim provenance not materialized | blocker | **ACCEPTED** (one sub-point partial) | Confirmed: the four run-level fields (`extraction_model`, `extraction_recipe_version`, `extraction_timestamp`, `input_content_hash`) lived only at the JSON root, not on any of the 30 claim objects; `source_refs` were generic strings; 12/15 coded files carried no `video_input_hash` key and 3 carried the pointer string `cite:corpus_record` instead of a hash; "same cue @ms" receipts omit video_id+quote. Recipe v1's own rule ("every emitted claim, no exceptions") makes root-hoisting non-compliant. **Partial rejection:** the "7/30 claims also omit `receipt`" sub-point — the 7 receipt-less claims are exactly the 7 withholds (4 momentum, matched-pair, clone-tail, trajectory); the contract resolves a field-missing claim to `withhold`, which is precisely their state, so absence of receipts on withheld (non-displayed) claims is contract-consistent, not a defect. Patched anyway with explicit `receipt: none — withheld` self-documentation. |
| AR-02 "organic adjacency" built from affiliate-classified videos | major | **ACCEPTED** | Confirmed: `ad.video_disclosure_class` codes 14 affiliate-or-self-brand + 1 gifted + 0 organic, yet `adj.organic_brand_product_presence` rendered `show` and the decision read sold "category-exact organic coverage." Recipe rule: paid/affiliate contexts excluded **or downgraded** — the downgrade branch applies (self-funded product acquisition is evidenced; the surrounding video context is always affiliate-monetized). Both `adj.organic_brand_product_presence` and `adj.organic_attention_stance` downgraded and relabeled **self-funded editorial coverage**; decision read reworded. |
| AR-03 unsupported `aventus-absolu` corpus entry + corrupted tier roll-up | major | **ACCEPTED** | Confirmed: no coded file resolved `product:creed.aventus-absolu`; the two source videos coded their "Absolute Aventus" mentions to base `product:creed.aventus`, so the corpus entry contradicted its own claim storage. (Not an invented coordinate: `aventus-absolu` IS a reference entry — the defect is the coded-vs-corpus contradiction with no reconciliation ledger, plus the arithmetically impossible "9/11 designer" tier roll-up: the 11 observed products resolve 8 designer / 2 niche / 1 luxury.) Closed by adopting the granularity rule below and re-coding both files. |
| AR-04 aggregates do not reconcile with coded records | major | **ACCEPTED** | All three bullets reproduce. (1) Aventus attention 171,041 is wrong; root cause diagnosed exactly: the roll-up summed 36,569+36,307+32,524+**32,530 (tVUqAYGT3SE — not an Aventus video)**+33,111, substituting tVUqAYGT3SE for nySgot9sqMY. Under the adopted granularity rule the correct set is 4 videos = 138,511 (absolu-only nySgot9sqMY moves to the absolu row). (2) `bought_because_of_creator` coded sum is 14, not 12; the two dropped records are the two channel-level attributions without a named purchased product (sw34VzzWlvA c15 "shaped my collection", FBda5R_1GGg c39 category-entry) — a defensible synthesis distinction that was never recorded; fixed by reporting 14 with the composition split displayed (12 product-specific + 2 channel-level). Same recount found `owned_no_creator_causality` coded sum = 157 (was "~150"). All other intent sums reconcile (dupe_request 12 ✓, watchlist 30 ✓, where_to_buy 4 ✓, price 3 ✓, comparison 4 ✓). (3) top-3 share 170,483/552,859 = 30.84% → 30.8%, not 30.7%. |
| AR-05 M4b on-panel allocation disclosure absent | major | **ACCEPTED** | Confirmed: the method sentence lived only in the derived JSON; the buyer-facing report said "attention-weighted" without the rule. Closed by displaying the allocation method beside every view-weighted surface in the report, including the honest disclosure that **no fractional tier/note view-distribution was computed** in this rehearsal (tier alignment is count-based; note chips weight by the once-per-video product-attention rows) — M4b's fractional-division rule applies to distributions that this report does not display. |
| AR-06 run log claims 29 corpus claim types; JSON holds 30 | minor | **ACCEPTED** | Confirmed by count: 30 `claim_type` objects. Run log corrected with an erratum note. |

Reviewer recomputations record: total views 552,859 PASS, Sauvage 51% PASS
(see rule below — the 7-video set stands), watchlist 30 PASS, product audit
10/10 reference matches PASS, withhold/M2/person-boundary/synthetic-disclosure
PASS. The two FAILs (Aventus sum, bought-because) are accepted above.

## The resolution-granularity rule adopted (closes AR-03's "one flanker rule")

**Resolve each mention to the most specific `fragrance_reference_v0.yaml`
entry that covers it; a reference entry is concentration-agnostic for its own
line; a distinct flanker with no reference entry of its own is UNRESOLVED.**

This rule is not new doctrine — it is what the corpus already practiced in its
strictest moment (ctcEju1AvGw codes "Le Male In Blue" as *unresolved —
flanker; reference has ultra-male only*) and what the reference itself
implies by containing `product:creed.aventus-absolu` as its own entry.
Applied consistently:

- **"Absolute Aventus" mentions → `product:creed.aventus-absolu`** (a more
  specific entry exists). Re-coded in `_FUdh1ryqWI.coded.json` (entry split:
  general-Aventus receipts stay on `creed.aventus`; @242560/@304920 absolu
  receipts move) and `nySgot9sqMY.coded.json` (@638200 is absolu-only).
  The corpus row "absolu, 2 videos (90,066 views)" is now substantiated by
  claim storage instead of contradicting it.
- **"Sauvage Elixir" mentions → unresolved flanker** (no reference entry; the
  creator himself distinguishes Elixir from the line's concentrations —
  hzqxkp3OqQw@1070280 "smells nothing like the Sauvage fragrances that came
  before it... the EDT, the EDP, or the parfum"). nySgot9sqMY's Elixir-only
  resolution to base Sauvage is withdrawn; hzqxkp3OqQw keeps its Sauvage
  resolution via its independent base-line receipt (@94840). The Sauvage
  corpus row (7 videos, 283,773, 51%) was therefore already correct — the
  round-1 "eighth video" inconsistency was in nySgot9sqMY's coded file, not
  the roll-up.
- Downstream recomputes: Aventus 4 videos / 138,511 / 25%; tier distribution
  8 designer / 2 niche / 1 luxury over 11 observed products.

## Claim-unit interpretation stated for round 2 (AR-01 closure shape)

The displayable unit under the provenance contract is the **corpus-level
claim object** (what the report renders): all 30 now materialize all seven
fields per claim with structured `source_refs` carrying actual hashes. The
per-video `coded.json` files are **claim storage** (speed-1): each now carries
the full seven-field block at record level with its real `video_input_hash`
(and transcript/watch/comments component hashes), and every inner mention
entry carries its own `receipt` + confidence. If the round-2 reviewer reads
the contract as requiring the four run-constant fields duplicated onto every
inner mention entry as well, that is an owner-level contract-interpretation
decision to surface, not a silent re-litigation.

## Round 2 (appended 2026-07-10): return adjudicated — all four residuals ACCEPTED

Round-2 return (OpenAI GPT-5, over patched commit `f49825c0`): verdict
**blocker** — AR-04 and AR-05 closed; AR-01/02/03/06 residuals remained.
Round-2 criterion 5 outcome: **FAILED.** Home lane re-verified every residual
at the source and accepted all four:

| Residual | Home-lane verdict | Closure applied |
| --- | --- | --- |
| AR-01a: `source_refs` still a prose pointer, not units+hashes | **ACCEPTED** (contract-interpretation capitulated: embed, don't point) | Every corpus claim's `source_refs` now embeds `captured_units` — the actual 15-entry `{video_id: video_input_hash}` map (mechanical scan: 30/30). |
| AR-01b: receipt cleanup incomplete (hzq "same sales-tier cue"; quote-less segment refs) | **ACCEPTED** | Full sweep run (not just the flagged example): every quote-less transcript receipt across all 15 files filled with verbatim cue text drawn from the frozen cues substrate — hzq sales-tier cue, all 13 quote-less 4OdcF9S6hxU tier-list entries (incl. re-grounding the Born-in-Roma receipt to its actual @1333120 mention and the 9PM Night Out tier to the spoken B verdict), ctc/eH/FB dupe-discourse and integrity receipts. Disclosure receipts that cite captured watch-packet FIELDS (e.g. `paid_content_overlay: not_captured`) are field observations, not speech quotes — named here, not converted. |
| AR-01c: M2 like sums not reconstructable | **ACCEPTED** | Exact sums recomputed from the frozen comments substrate: dupe_request **176** (top 63/40/35/26 all cross-validated), bought-because **39**; every contributing intent ref now carries its captured like count (blank captures explicitly marked "no like count captured", counted 0). Corpus claim and report updated from ~approximations to exact. |
| AR-02 residual: similarity claim said "organic clone coverage" at `show` | **ACCEPTED** (relabel; posture kept with stated basis) | Wording replaced with the adjudicated self-funded-editorial classification. `show` retained WITH an explicit `posture_basis`: similarity is measured between reference/intake coordinates and observed coverage — it does not rest on the coverage being organic. Round 3 may contest the posture; the basis is now stated, not implicit. |
| AR-03 residual: hzq kept Elixir material inside resolved base objects | **ACCEPTED** | hzq restructured: Sauvage and Y entries rest on the independent base-line receipt (@94840) only; Sauvage Elixir and Y Elixir material moved to a `flanker_segments_unresolved` array (rule now applied uniformly; base rows unchanged, as the reviewer noted). |
| AR-06 residual: second "29" occurrence in operator_steps | **ACCEPTED** | Corrected with its own erratum note. |

Zip-identity residual: the reviewer looked for the pack at a repo-relative
path; the courier zips live in the session scratchpad (outside the repo, by
design — packs are not repo artifacts). The round-3 pack is
`report_zero_review_pack_round3.zip`; identity remains provable only by the
operator attaching it, which is a named residual, not a defect.

## Non-claims

Adjudication of rounds 1 and 2 only. Not a criterion-5 pass claim (that
requires a blocker/major-free round-3 return), not validation or readiness,
and not a gate-firing claim. `product_learning`-capped.
