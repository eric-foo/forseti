---
retrieval_header_version: 1
artifact_role: Capture-side source-provenance record (capture-spine deliverable; NOT a fixture, band input, or contestant-visible packet)
scope: >
  Per-evidence-unit provenance for the pre-cutoff Wayback capture set of case
  sundaily_gummy_pivot_v0: the pre-pivot Sundots-era homepage trajectory plus
  the UV-ingestible FAQ explainer, captured via the archive_org adapter.
  Records the selected snapshots, body hashes, and honest coverage limits. This
  is a capture-spine evidence set, not a backtest fixture: no participant
  packets, facilitator ledger, sealed outcome, or evaluation exist for this
  case yet.
use_when:
  - Auditing what the Sundaily / Sundots gummy-pivot case is archive-sourced from so far.
  - Deciding what a later judgment-spine fixture for this case would still need.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/consumer_demand_candidate_pool_handoff_v0.md   # roster row this case came from (candidate #11)
  - docs/decisions/ingestible_beauty_screen1_ledger_v0.md   # the screen that surfaced this candidate (row 1)
---

# Source Provenance Notes — sundaily_gummy_pivot_v0 (v0)

Capture-side record. This is the **capture-spine deliverable** for the
Sundaily (ex-Sundots) ingestible-beauty pivot backtest case: bounded pre-cutoff
Wayback captures produced by the `archive_org` adapter
(`run_source_capture_archive_packet.py`, `select_snapshot <= cutoff`). Every
unit below is `cutoff_posture: pre_cutoff`, body-verified (served body equals
the selected snapshot), `warnings: []`, `limitations: []`. It is **not** a
backtest fixture and asserts no judgment.

## Case context (roster-stated; not independently verified here)

From the consumer-demand candidate pool (candidate #11) and the ingestible
beauty screen-1 ledger (row 1):

- **Decision being backtested:** Sundaily's full pivot — the UV-protectant
  ingestible ("sun protection in a daily gummy") repositioned toward
  skin-health gummies, with the brand renamed **Sundots → Sundaily**; Goop
  distribution/validation followed.
- **Cutoff:** 2018-10-01 (`20181001000000`) — see rationale below. Each unit
  selects the latest snapshot at or before its stated cutoff.
- **Known later outcome:** rename to Sundaily and broader skin-health gummy
  repositioning; Goop stocking/validation reported (per the screen-1 ledger's
  retail-gatekeeper-as-validator observation).

The outcome above is roster-/screen-stated context, **not** an independently
sealed or verified outcome record for this case (Beauty Pie / Topicals have
sealed records; this case does not yet).

### Cutoff rationale and domain pinning (Wayback-verified this run)

The pre-pivot brand operated at **`sundots.com`**. Its real brand homepage
(title *"Sun protection in a daily gummy. Because sunscreen's not enough."*) is
archived as HTML-200 from **2018-03-30 through 2018-09-23** (last pre-pivot
homepage snapshot), with `/pages/faq` archived 2018-03 → 2018-05. The renamed
**Sundaily** brand then appears at **`getsundaily.com`** (HTML-200 from
2018-10-21 / 2018-12-04 onward; a 2018-12 snapshot still carries the *same* UV
"daily gummy" title but the "Sundaily" name and residual "sundots" references —
i.e. captured mid-rename). The rename therefore falls in **fall 2018**, between
`sundots.com`'s last Sept-2018 brand snapshot and `getsundaily.com`'s Oct/Dec-2018
emergence. **`2018-10-01` is the chosen pre-pivot cutoff**: it captures the full
Sundots-era UV-ingestible site while staying before the renamed brand's domain
solidifies.

**Domain-collision note (load-bearing):** `sundaily.com` (the obvious-looking
brand domain) was **not** the beauty brand during this window — in 2018-2019 it
hosted an unrelated Chinese-language video/entertainment site (paths like
`/caijing/`, `/donghua/`, `/eluosi/`, `/gangtai/`). `trysundots.com`,
`thesundaily.co`, `sundaily.co`, and `trysundaily.com` returned **no** pre-2022
HTML-200 Wayback coverage. The pre-pivot decision-relevant domain is
`sundots.com`; the post/brand domain is `getsundaily.com`. The cutoff residual
is small (uncertainty: the exact rename date is not independently confirmed; it
is bracketed to fall 2018 by the two domains' Wayback coverage).

## Captured evidence (real Source Capture packets, body-verified, pre-cutoff)

### Pre-pivot homepage trajectory — `sundots.com` (UV-ingestible "daily gummy" positioning)

| E | source | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E1 | sundots.com homepage, cutoff-proximate (latest pre-pivot) | 2018-09-23 | 79896 | `11ebaa5b…8b0937e8` | `source_captures/e1_homepage_sept2018/` |
| E2 | sundots.com homepage, late-summer | 2018-08-16 | 78028 | `6ac006bf…5eb1b3b9` | `source_captures/e2_homepage_aug2018/` |
| E3 | sundots.com homepage, mid-summer | 2018-07-10 | 90672 | `f1b5197f…d764ac03` | `source_captures/e3_homepage_jul2018/` |
| E4 | sundots.com homepage, spring | 2018-05-08 | 72998 | `1544d4b0…a20d31be` | `source_captures/e4_homepage_may2018/` |
| E5 | sundots.com homepage, launch-era | 2018-04-01 | 53304 | `e7585603…00baddc1` | `source_captures/e5_homepage_apr2018/` |

### Decision-relevant page (UV-ingestible science / explainer)

| E | page | selected snapshot | body bytes | sha256 (body) | packet |
| --- | --- | --- | --- | --- | --- |
| E6 | `/pages/faq` — UV-ingestible how-it-works / science FAQ | 2018-05-08 | 56474 | `180f0202…5958a2a8` | `source_captures/e6_faq/` |

6 body-verified units. Page content is **recorded, not interpreted** — the raw
HTML body is preserved for a later parser/judgment step; what the
positioning/claims/product actually were is not asserted here (capture
preserves bytes + provenance only).

## Honest coverage limits

- **Thin distinct-page coverage on the pre-pivot domain.** Within the pre-cutoff
  window, only the homepage (multiple timepoints) and `/pages/faq` are archived
  as HTML-200 on `sundots.com`. CDX probes for `sundots.com/products*` and
  `sundots.com/collections*` returned **empty** (no Shopify product/collection
  pages archived pre-cutoff). The set is therefore a dense homepage trajectory
  plus the one archived explainer page, not a broad page inventory.
- **No pre-cutoff Sundaily-domain capture.** The renamed brand's domain
  (`getsundaily.com`) only appears archived from 2018-10-21 onward — **after**
  the 2018-10-01 cutoff — so it is correctly excluded from this pre-cutoff set.
  Its existence is documented above as the post/brand domain only, not captured.
- **`sundaily.com` is a domain collision** (unrelated 2018-2019 Chinese-language
  site), and `trysundots.com` / `thesundaily.co` / `sundaily.co` /
  `trysundaily.com` had no pre-2022 HTML-200 coverage — see the domain-pinning
  note. None were captured.
- **Not parsed / not separately captured** (per a bounded discovery sweep): a
  Goop product-listing page (the validation signal is a later outcome, not
  pre-cutoff state), press/news coverage, a careers/Greenhouse/Lever board, and
  an about/our-story page (none found archived as decision-relevant HTML-200
  pre-cutoff on `sundots.com`).
- **Content not parsed** (INV-1): capture records observed facts + limits and
  introduces no weights, scores, ranks, or judgment.
- **Line endings:** capture raw files commit under repo-wide `autocrlf=true` with
  no `.gitattributes` (matching the existing Beauty Pie / Topicals / Kinder Beauty
  precedent). The committed blobs are byte-faithful (blob sha256 = the manifest
  sha256 above); a Windows working-copy checkout shows CRLF-inflated sizes.
  Marking `source_captures/** -text` repo-wide is the correct fix but would
  re-touch the frozen fixtures, so it is left as an owner-gated hygiene call.

## Non-claims

Not validation, not readiness, not a backtest fixture, not a band input, not a
sealed outcome, not contestant-visible, not Cleaning/ECR/Judgment, not buyer
proof. Product-learning tier, capture-only, N=6 pre-cutoff snapshots.
