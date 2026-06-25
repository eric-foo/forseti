# Search-Surface MGT Pilot P0 Capture Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Preserved Google search-surface screenshots, AI-answer-surface states, and raw observables for Search-Surface MGT P0 US indie/DTC fragrance queries.
use_when:
  - Reviewing the Search-Surface MGT P0 capture set before any judgment pass.
  - Checking query-level SERP modules, AI Overview / AI Mode states, autocomplete, PAA/PAS, product, video, forum, and location/session-state signals.
  - Verifying that later product-proof or Product Lead work does not overclaim this capture set.
open_next:
  - .agents/workflow-overlay/product-proof.md
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/capture_manifest.json
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/hashes_sha256.txt
stale_if:
  - Any P0 query is recaptured or judged from a different Google session state without a new receipt.
  - Google SERP modules, localization, personalization controls, or result rendering materially change.
authority_boundary: retrieval_only
```

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 + capture playbook/recon index
  edit_permission: docs-write
  target_scope: docs/research capture receipt preservation for Search-Surface MGT P0 fragrance queries, including first-class AI-answer-surface states
  dirty_state_checked: yes - main checkout dirty, work isolated to branch codex/search-surface-mgt-p0-captures-ws in worktrees/search-surface-mgt-p0-captures
  blocked_if_missing: screenshots/raw observables, exact URLs, AI Overview / AI Mode shown-or-not-shown state, session-state/location notes, and explicit non-claims
```

## Boundary

This is capture-only. It is not Judgment evidence until reviewed. It is not Product Lead action, durable-demand proof, willingness-to-pay proof, buyer proof, or product readiness.

The judgment questions in the commission are intentionally not answered here. This artifact preserves the surfaces for a later review pass.

## Capture Route And Session State

Successful route: fresh visible Chrome profile, logged out, one query per profile for queries 03-06 and a short visible batch for queries 01-02. Google parameters were `hl=en&gl=us&pws=0`; browser language was `en-US`; no mobile emulation was used.

Observed viewport in the successful receipts: `1264x625`, DPR `1`. The Chrome window was launched with `--window-size=1280,720`; browser chrome reduced the page viewport.

Logged-out signal: `Sign in` visible and `Google Account` not visible in every successful `serp_full.json`. Consent text was not visible in the successful receipts.

Location signals: Google footer reported `Unknown - Can't determine location` / `Update location`; browser timezone was `Asia/Singapore`. Failed Google `/sorry/` pages exposed IP `121.7.247.114` and timestamps around `2026-06-24T15:04:49Z` to `2026-06-24T15:04:52Z`. Treat the receipts as US-parameterized, not physically US-located.

Session-state warning: do not compare queries as if they came from one identical SERP session. Queries 01-02 came from one visible batch; queries 03-06 came from separate fresh visible profiles. A headless batch route was blocked by Google CAPTCHA and is preserved separately as route-failure evidence.

## Preserved Files

- Manifest: `docs/research/search_surface_mgt_pilot_p0_receipts_v0/capture_manifest.json`
- Hash ledger: `docs/research/search_surface_mgt_pilot_p0_receipts_v0/hashes_sha256.txt`
- Route-failure logs: `headless_batch_blocked_run_index.json`; `visible_batch_partial_run_index.json`
- Per-query folders: `docs/research/search_surface_mgt_pilot_p0_receipts_v0/receipts/<query_id>/`
- Per SERP: `serp_top.png/html/txt/json` and `serp_full.png/html/txt/json`
- Autocomplete for query 01: `autocomplete.png/html/txt/json`

## P0 Capture Index

| ID | Query | Successful final URL | Key modules preserved in `serp_full` | AI answer-surface state | Notes |
| --- | --- | --- | --- | --- | --- |
| 01 | `niche perfume discovery set` | `https://www.google.com/search?q=niche+perfume+discovery+set&hl=en&gl=us&pws=0&sei=j_I7au_9GKqhseMPx92nsQY` | products/shopping, Popular products, More products, videos, forums, PAS | `ai_overview_shown` | PAA not observed. Autocomplete captured. Possible non-US signal: `perfumelounge.eu` result cluster. |
| 02 | `perfume samples before buying full bottle` | `https://www.google.com/search?q=perfume+samples+before+buying+full+bottle&hl=en&gl=us&pws=0` | PAA, products/shopping, videos, forums, PAS | `ai_overview_shown` | Popular products / More products not observed. |
| 03 | `pistachio perfume` | `https://www.google.com/search?q=pistachio%20perfume&hl=en&gl=us&pws=0&sei=1PM7asqPHYGE4-EPhOf6-A0` | PAA, products/shopping, Popular products, More products, videos, forums, PAS | `ai_mode_tab_only_no_ai_overview` | Short-video/currentness surface preserved in screenshot/text. |
| 04 | `vanilla skin perfume` | `https://www.google.com/search?q=vanilla%20skin%20perfume&hl=en&gl=us&pws=0&sei=GvQ7asGQJZfb4-EPubHZ6QQ` | PAA, products/shopping, Popular products, More products, videos, forums | `ai_mode_tab_only_no_ai_overview` | PAS not observed by extractor. |
| 05 | `Le Labo Santal 33 dupe` | `https://www.google.com/search?q=Le+Labo+Santal+33+dupe&hl=en&gl=us&pws=0&sei=YPQ7aprbHarE4-EPm8yZuQE` | PAA, products/shopping, Popular products, videos, forums, Discussions and forums, PAS | `ai_overview_shown` | Possible non-US signals: UK editor line; India clone forum line. |
| 06 | `Baccarat Rouge 540 dupe` | `https://www.google.com/search?q=Baccarat%20Rouge%20540%20dupe&hl=en&gl=us&pws=0&sei=ofQ7avHENfCHjuMP18n0uA0` | PAA, products/shopping, More products, videos, forums, PAS | `ai_overview_shown_no_ai_mode_tab` | Popular products not observed. |

## AI Answer Surface Module

`capture_manifest.json` now carries `ai_answer_surface_module` for every query. The module is derived from preserved `serp_top` / `serp_full` text plus screenshot pointers; no recapture or live Trends pull was performed.

Observed states in P0:

- `ai_overview_shown`: Q01, Q02, Q05.
- `ai_overview_shown_no_ai_mode_tab`: Q06.
- `ai_mode_tab_only_no_ai_overview`: Q03, Q04. This is the no-AI-box state for this receipt: the AI Mode tab was visible, but no AI Overview box text was observed in `serp_top.txt` or `serp_full.txt`.

Interpretation boundary: AI Overview shown/not shown is a visibility observation only. It is not buyer proof, durable-demand proof, demand absence, gate evidence, or evidence of Google's internal trigger logic.

Trends-correlation follow-up is allowed as an explanatory probe only: compare search-interest/trend posture against `ai_answer_surface_module.observed_state` to form hypotheses about why an AI box may be shown or not shown. It cannot prove causality, demand, absence-of-demand, or scoring priority.

## Query 01 Autocomplete

Captured suggestions for `niche perfume discovery set`:

- `niche perfume discovery set`
- `niche perfume discovery set sale`
- `niche perfume discovery set men`
- `niche perfume discovery sets reddit`
- `niche perfume discovery kit`
- `best niche perfume discovery sets`
- `niche perfume house discovery set`
- `men's niche fragrance discovery set`
- `shop deals on niche perfume discovery sets`
- `niche parfum discovery set`

## Query-Level Extracts

Detailed organic rows, snippets/container text, PAA lines, PAS/related lines, product/shopping lines, video/forum lines, AI answer-surface states, and possible non-US signals are recorded in `capture_manifest.json` and each query's `serp_full.json`. The screenshots are the primary visual observables; JSON extraction is a bounded convenience view over the page state.

## Verification Notes

Hash ledger created with SHA-256 for every preserved file. Recompute with:

```powershell
Get-ChildItem docs\research\search_surface_mgt_pilot_p0_receipts_v0 -Recurse -File | Get-FileHash -Algorithm SHA256
```

Placement: `docs/research/` is the accepted folder for public/source research artifacts and evidence gathering. The raw PNG/HTML/TXT/JSON files are preserved observables, not independent Orca authority.

## Non-Claims

- Not judgment evidence until reviewed.
- Not durable-demand proof.
- Not absence-of-demand when an AI Overview box is not shown.
- Not buyer proof.
- Not willingness-to-pay proof.
- Not Product Lead action.
- Not proof of US physical location.
- Not a comparison across identical Google sessions.
- Not a P1 capture set; P1 queries remain uncaptured.
