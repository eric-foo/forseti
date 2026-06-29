# Search-Surface MGT P0 Live Trends Probe v0

```yaml
retrieval_header_version: 1
artifact_role: Research synthesis artifact
scope: Bounded live Google Trends/search-interest probe for the Search-Surface MGT P0 fragrance query set, comparing observed search-interest posture against preserved AI-answer-surface states.
use_when:
  - Checking whether live Google Trends adds useful routing context to the P0 search-surface capture set.
  - Explaining why Q03/Q04 no-AI-box states should be treated as hypotheses, not demand absence.
  - Deciding whether the next P1 move should be direct-source Capture, Scanning frontier work, or a narrow Trends/source-interest repeat.
open_next:
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/search_surface_mgt_pilot_p0_capture_receipt_v0.md
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/search_surface_mgt_pilot_p0_capture_efficacy_review_v0.md
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/capture_manifest.json
  - orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
stale_if:
  - Any Trends panel is re-run with a different query set, topic/entity selection, geography, category, property, or time window.
  - Google Trends changes its normalization, sampling, privacy thresholding, or Explore rendering.
  - The P0 AI-answer-surface states are recaptured or superseded.
authority_boundary: retrieval_only
```

## Boundary

This is a live search-interest correlation probe only. It is not search volume, market sizing, buyer proof, durable-demand proof, willingness-to-pay proof, Product Lead action, Google AI Overview trigger proof, or absence-of-demand evidence.

The probe uses exact Google Trends search terms as typed, not Google Trends topics/entities. Values are normalized relative interest for the selected panel, geography, property, category, and time window.

Google's own Trends FAQ (https://support.google.com/trends/answer/4365533?hl=en) says Trends normalizes search data to the query time and location, scales results from 0 to 100, filters low-volume terms so they may appear as `0`, and should be treated as one data point rather than a scientific poll.

## Observation Method

- Observed at: `2026-06-25T20:57:47+08:00`.
- Route: visible in-app browser, logged-out Google Trends page.
- Geography: United States.
- Property: Web Search.
- Category: All categories.
- Time windows: Past 12 months, then Past 90 days.
- Direct API route: attempted once through shell; blocked by Google with `HTTP 429`, so the accepted observation route is browser-visible Google Trends Explore accessible chart tables.

## AI Answer State Crosswalk

| ID | Query | P0 AI answer-surface state |
| --- | --- | --- |
| Q01 | `niche perfume discovery set` | `ai_overview_shown` |
| Q02 | `perfume samples before buying full bottle` | `ai_overview_shown` |
| Q03 | `pistachio perfume` | `ai_mode_tab_only_no_ai_overview` |
| Q04 | `vanilla skin perfume` | `ai_mode_tab_only_no_ai_overview` |
| Q05 | `Le Labo Santal 33 dupe` | `ai_overview_shown` |
| Q06 | `Baccarat Rouge 540 dupe` | `ai_overview_shown_no_ai_mode_tab` |

## Panel 1 - P0 Q01-Q05, Past 12 Months

Google Trends URL:
`https://trends.google.com/trends/explore?date=today%2012-m&geo=US&q=niche%20perfume%20discovery%20set,perfume%20samples%20before%20buying%20full%20bottle,pistachio%20perfume,vanilla%20skin%20perfume,Le%20Labo%20Santal%2033%20dupe`

Accessible average row observed:

| Term | Average |
| --- | ---: |
| `niche perfume discovery set` | 0 |
| `perfume samples before buying full bottle` | 0 |
| `pistachio perfume` | 56 |
| `vanilla skin perfume` | 37 |
| `Le Labo Santal 33 dupe` | 4 |

Latest weekly row observed, week of `2026-06-21`:

| Term | Value |
| --- | ---: |
| `niche perfume discovery set` | 0 |
| `perfume samples before buying full bottle` | 0 |
| `pistachio perfume` | 35 |
| `vanilla skin perfume` | 24 |
| `Le Labo Santal 33 dupe` | 8 |

Notable peaks in this panel:

| Term | Observed peak | Date |
| --- | ---: | --- |
| `pistachio perfume` | 94 | `2025-12-21` |
| `vanilla skin perfume` | 100 | `2026-04-12` |
| `Le Labo Santal 33 dupe` | 26 | `2026-04-05` |
| `niche perfume discovery set` | 13 | `2026-04-05` |
| `perfume samples before buying full bottle` | 0 | all observed rows in this panel |

## Panel 2 - Add Q06 With Overlap, Past 12 Months

Google Trends URL:
`https://trends.google.com/trends/explore?date=today%2012-m&geo=US&q=niche%20perfume%20discovery%20set,pistachio%20perfume,vanilla%20skin%20perfume,Le%20Labo%20Santal%2033%20dupe,Baccarat%20Rouge%20540%20dupe`

Accessible average row observed:

| Term | Average |
| --- | ---: |
| `niche perfume discovery set` | 0 |
| `pistachio perfume` | 55 |
| `vanilla skin perfume` | 37 |
| `Le Labo Santal 33 dupe` | 4 |
| `Baccarat Rouge 540 dupe` | 58 |

Latest weekly row observed, week of `2026-06-21`:

| Term | Value |
| --- | ---: |
| `niche perfume discovery set` | 0 |
| `pistachio perfume` | 35 |
| `vanilla skin perfume` | 24 |
| `Le Labo Santal 33 dupe` | 8 |
| `Baccarat Rouge 540 dupe` | 50 |

Notable peaks in this panel:

| Term | Observed peak | Date |
| --- | ---: | --- |
| `Baccarat Rouge 540 dupe` | 100 | `2026-04-12` |
| `vanilla skin perfume` | 100 | `2026-04-12` |
| `pistachio perfume` | 94 | `2025-12-21` |
| `Le Labo Santal 33 dupe` | 26 | `2026-04-05` |
| `niche perfume discovery set` | 13 | `2026-04-05` |

## Panel 3 - Currentness Check, Past 90 Days

Google Trends URL:
`https://trends.google.com/trends/explore?date=today%203-m&geo=US&q=niche%20perfume%20discovery%20set,pistachio%20perfume,vanilla%20skin%20perfume,Le%20Labo%20Santal%2033%20dupe,Baccarat%20Rouge%20540%20dupe`

Accessible average row observed:

| Term | Average |
| --- | ---: |
| `niche perfume discovery set` | 0 |
| `pistachio perfume` | 19 |
| `vanilla skin perfume` | 28 |
| `Le Labo Santal 33 dupe` | 1 |
| `Baccarat Rouge 540 dupe` | 31 |

Latest daily row observed, `2026-06-25`:

| Term | Value |
| --- | ---: |
| `niche perfume discovery set` | 0 |
| `pistachio perfume` | 23 |
| `vanilla skin perfume` | 23 |
| `Le Labo Santal 33 dupe` | 10 |
| `Baccarat Rouge 540 dupe` | 42 |

Notable 90-day peaks in this panel:

| Term | Observed peak | Date |
| --- | ---: | --- |
| `vanilla skin perfume` | 100 | `2026-04-12` |
| `Baccarat Rouge 540 dupe` | 83 | `2026-04-11` and `2026-04-22`; latest `2026-06-25` is 42 |
| `pistachio perfume` | 85 | `2026-05-17` |
| `Le Labo Santal 33 dupe` | 10 | `2026-06-25` |
| `niche perfume discovery set` | 0 | all observed rows in this panel |

## Read

The no-AI-box queries, Q03 `pistachio perfume` and Q04 `vanilla skin perfume`, are not low-interest in Trends. In the observed 12-month panels they are among the strongest terms, and in the 90-day panel they remain active. So the no-AI-box state should not be interpreted as "not enough demand" or "not enough attention."

Q06 `Baccarat Rouge 540 dupe` shows both strong Trends posture and an AI Overview. That weakens any simple rule like "high search interest means no AI box" or "dupe terms are too commercial for AI Overview." The better hypothesis is mixed: AI Overview visibility may be affected by query ambiguity, commercial/result density, answerability, product-result layout, freshness, and Google rendering choices, not by search interest alone.

Q01/Q02 exact long-tail discovery/sample phrases are weak or below Trends thresholds in these exact-term panels, yet both showed AI Overview in the P0 SERP receipts. That also weakens any simple rule like "high Trends interest causes AI Overview."

Q05 `Le Labo Santal 33 dupe` is lower-interest than Q06 and the note-trend terms, but still showed AI Overview. This suggests the SERP's comparison/answerability shape may matter more than raw Trends posture for the P0 AI-answer observation.

## Efficacy Implication

The live Trends probe is useful for routing, not proof. It makes the P0 capture more decision-useful because it separates:

- high-interest current trend/note terms with no AI Overview in the receipt: Q03/Q04;
- high-interest dupe/comparison term with AI Overview: Q06;
- lower-interest exact long-tail discovery/sample terms that still showed AI Overview: Q01/Q02;
- lower-interest but answerable comparison term with AI Overview: Q05.

This supports continuing Search-Surface MGT as a front-door method into Scanning and Capture. The next best move is still P1 direct-source capture, not more broad Trends work: preserve buyer-origin/community/retailer/video sources for the discovery/sample and dupe/comparison clusters, while using Q03/Q04 as a trend-language control cluster if useful.

## Non-Claims

- No claim that Google Trends values are absolute search volume.
- No claim that `0` means no searches or no demand.
- No claim that Trends posture explains Google's internal AI Overview trigger.
- No claim that AI Overview shown/not-shown proves demand or demand absence.
- No claim that these panels are comparable to a differently selected topic/entity panel.
- No claim that currentness should become a score boost; it remains attention-priority and routing context only.
