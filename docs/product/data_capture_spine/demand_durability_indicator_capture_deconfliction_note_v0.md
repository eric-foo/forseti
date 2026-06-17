# Demand-Durability Indicator Capture — Reconciliation + Deconfliction Note v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (reconciliation + deconfliction record for the demand-durability indicator capture set)
scope: >
  Records (1) the parallel-lane collision and how it was reconciled, (2) the
  owner-decided proxy->indicator terminology rename and its exact scope, and
  (3) the cross-cutting deconfliction findings that remain a useful cross-check
  over the merged indicator set. Reporting + provenance only — authorizes nothing,
  hardens nothing.
use_when:
  - Understanding why the four capture profiles are named demand_durability_indicator_* and how they relate to the parallel lane's original demand_proxy_* set.
  - Checking the scope of the proxy->indicator rename (capture-spine only; product doctrine untouched).
  - Cross-checking what existing Data Capture Spine surfaces already own vs what is genuinely new.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md       # keystone delta (consumed by all four profiles)
  - docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md
  - docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md
  - docs/product/data_capture_spine/demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md
stale_if:
  - The keystone delta, the obligation contract, or the Source Capture packet schema changes.
  - The source-observability requirements boundary decision is superseded.
  - The company-aggregate/EDGAR org-motion lane or the deleted-comment-retrieval decision changes status.
  - A price-capture mechanism that covers retail/promo (not the narrow SaaS extractor) lands.
  - The proxy->indicator terminology is revisited.
```

- Status: `RECONCILIATION_NOTE_V0`
- Artifact type: Reconciliation + deconfliction record (reporting/provenance only; authorizes nothing; hardens nothing)

## What Happened (collision + reconciliation)

The four demand-durability indicator capture profiles were authored **twice, in
parallel**, against the same commission:

- A coordinated multi-lane effort ("Lane 1" = the Capture Envelope durability
  delta keystone, PR #93; the four profiles via PRs #95/#96) authored them as
  `demand_proxy_*` and **merged them to `main`** while this lane was working.
- This lane independently authored the same four as `demand_durability_indicator_*`
  (unaware of the parallel merge until rebase).

**Reconciliation (owner-decided 2026-06-15):**

- **Kept the merged set** (the `demand_proxy_*` profiles that landed via #95/#96)
  and **dropped this lane's duplicate four** — no duplication on `main`.
- **Renamed** the merged set `demand_proxy_*` → `demand_durability_indicator_*`
  (files + bodies) per the terminology decision below.
- **Landed this lane's two genuinely-additive artifacts** that the parallel lane
  did not produce: this reconciliation note and the standing-capture
  obligation-home decision framing.

Net result: one indicator set on `main`, named `demand_durability_indicator_*`,
plus the two additive notes.

## Terminology Decision — "indicator" (demand) vs "proxy" (network)

Owner decision (2026-06-15): **"proxy" is reserved for the NETWORK sense**
(residential exit IPs, `ProxyProfile` in `orca-harness/source_capture/proxy_profiles.py`);
the demand-side observable is **"demand-durability indicator."**

**Scope finding (this matters):** "repo-wide" turned out to be **capture-spine-only.**
The demand-sense "proxy" appeared in exactly **6 capture-spine files** (the keystone
delta, the four profiles, and this note) — all under `docs/product/data_capture_spine/`.
The owner-locked **product docs do NOT use "proxy" for this concept**: the
buyer-proof packet has zero "proxy" mentions, and the demand-read taxonomy's only
occurrence is **"paid-proxy spend"** (the *manufactured-demand / paid-promotion*
sense), which is a **different meaning and was left untouched**. Network references
(`ProxyProfile`, `proxy_profiles.py`, residential/datacenter proxy) were left
untouched. So the rename changed terminology in the capture-spine lane only and
**touched no product doctrine and no network-proxy code or docs.**

## Session Deltas Applied To The Merged Set

Per the owner's "patch the landed files" decision:

- **Rename** (above) — across all five capture-spine demand files.
- **Cadence rhythm** — the keystone delta's Element 4 now records the
  **hourly-to-daily** sampling rhythm (owner, 2026-06-15) and that `CadencePlan`
  is a seconds-scale within-session jitter planner, so a real hourly/daily cadence
  + scheduler is a separate build step. The four profiles consume Element 4.
- **Price "not handled"** — already reflected in the merged price profile: the
  shipped `price_payload_extraction.py` is **narrow/SaaS-only** (one pricing-page
  shape), beauty/retail needs rendered capture, and only the generic
  `extract_object_at_anchor` is a reusable utility. No further price patch needed.

## Cross-Cutting Deconfliction Findings (still a valid cross-check)

| Surface | Already owns | Relationship |
| --- | --- | --- |
| Source Capture packet schema (`models.py`, manifest `_v1`) | All provenance/immutability (`PacketTiming`, `PreservedFile.sha256`+`hash_basis`, closed posture/`re_capture_relationship` vocabularies) | Consumed as-is; the profiles add no provenance field |
| Obligation contract | Ob.1–16 incl. Ob.6 fidelity, Ob.8 timing, Ob.10 archive, Ob.12 review-surface context, Ob.13 bundled-offer, Ob.15 re-capture; forbidden outputs (no scoring/integrity) | Consumed + cited; re-spec/hardening owner-gated |
| Capture Envelope durability delta (keystone) | The five durability-over-time elements + temporal regimes + cold-start cap | Consumed by all four profiles |
| Source-observability RQ lane (boundary decision, current) | Fidelity/inspectability (RQ-01/03/05 carry-forward, RQ-02 split, RQ-04 deferred) | Complementary: it governs *how faithfully content is preserved*; profiles govern *which series to capture* |
| `price_payload_extraction.py` | SaaS-tier embedded-payload price recovery (one page shape) | **Narrow; price capture for beauty is NOT handled** — net-new |
| `cadence.py` `CadencePlan` | Seconds-scale within-session jitter planner | Vocabulary only; hourly/daily cadence + scheduler is a build step |
| `proxy_profiles.py` `ProxyProfile` | Network exit-IP config + declared geo | Drives rendered `locale_pin`/`currency_pin`; an exit-geo change can silently corrupt a price/availability series (pins must hold it constant) |
| Company-aggregate/EDGAR org-motion lane | Standing, entity-keyed official-first org-motion series | Distribution/org-motion **deferred** — deconflict, do not re-spec; shares the standing-capture obligation-home gap |
| Deleted-comment retrieval decision (`DROPPED`) | — | Hard line: the review profile detects deletion **by disappearance across Orca's own snapshots**, never re-fetches a deleted body from a third-party archive |

## Live Consequence — Standing-Capture Obligation Home (owner-confirmed)

Continuous hourly/daily monitoring of these indicators is **owner-confirmed wanted**
(2026-06-15), which makes them **standing** capture — and the v0 obligation
contract has **no home for standing capture** (commissioned-only; routes
standing/corpus out to a not-yet-written Candidate Signal Intake / Corpus Intake
contract). This is framed, with the owner's selected direction (general contract,
scheduler deferred), in
`demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md`.
The profiles stay "commissioned capture only" until that contract is written
(owner-gated, separate lane — recommended for a delegated/adversarial review).

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The demand-side observable in the capture-spine lane is renamed from "proxy"
    to "demand-durability indicator", reserving "proxy" for the network sense
    (ProxyProfile / residential exit IPs). Applied to the keystone durability
    delta and the four capture profiles (files + bodies); the four profiles are
    renamed demand_proxy_* -> demand_durability_indicator_*. The hourly-to-daily
    sampling rhythm is recorded in the keystone's cadence element.
  trigger: output_authority
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
    - docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md
    - docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md
    - docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md
    - docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md
    - docs/product/data_capture_spine/demand_durability_indicator_capture_deconfliction_note_v0.md
  downstream_surfaces_checked:
    - docs/product/search/orca_demand_read_taxonomy_v0.md
    - docs/product/product_lead/orca_buyer_proof_packet_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: docs/product/search/orca_demand_read_taxonomy_v0.md
      reason: >
        Its only "proxy" is "paid-proxy spend" (manufactured-demand sense), a
        different meaning; renaming it would be wrong. The taxonomy does not name
        the demand observable "proxy".
    - path: docs/product/product_lead/orca_buyer_proof_packet_v0.md
      reason: >
        Zero "proxy" mentions for this concept; nothing to rename.
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      reason: >
        Does not reference the demand-sense "proxy" term (git grep clean); the
        four profiles are not yet registered there — a discoverability pass is a
        separate owner-decided step.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        No demand-sense "proxy" reference (git grep clean); registration of this
        family is a separate discoverability pass.
  stale_language_search: >
    git grep -ilE "demand[ _-]proxy|durability proxy" -- docs/ orca-harness/
  stale_language_search_result: >
    After the rename, no demand-sense "proxy" remains in the six capture-spine
    files (verified). Remaining "proxy" hits repo-wide are the network sense
    (ProxyProfile / proxy_profiles.py) and the taxonomy's "paid-proxy spend" —
    both correctly left untouched.
  non_claims:
    - not validation
    - not readiness
    - not contract hardening
    - not implementation/runtime/scheduler authorization
```

## INV-1 Preservation

This note reports collision/reconciliation/terminology and cross-checks overlap
only. It introduces no weight, score, ranking, threshold, or judgment, and
re-specs none of the consumed surfaces.

## Non-Claims

Not validation, readiness, acceptance, Data Capture Spine acceptance, contract
hardening, source-of-truth promotion, buyer proof, judgment-quality evidence,
implementation/runtime/tooling/scheduler authorization, source-access boundary
amendment, obligation-contract amendment, schema change, ECR/Cleaning/Judgment
design, or commercial-readiness evidence. It records what was reconciled, what was
renamed and how narrowly, and what remains deferred for the demand-durability
indicator capture set.
```
