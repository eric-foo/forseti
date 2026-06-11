```yaml
retrieval_header_version: 1
artifact_role: Capture-spine spec draft (non-authorizing) — archive_org adapter refinements + source-family gap specs
scope: >
  Spec drafts (problem / goal / proposed shape / non-goals / acceptance) for the archive_org
  adapter refinements (date-bound CDX, trajectory capture, URL-form sweep) and the source-family
  gaps (LinkedIn forward trend, exec moves, Companies House, demand-side signals) surfaced by the
  org-motion Beauty Pie backtest pilot. Spec only — no implementation, no change to existing
  adapter behavior until a separate authorized build turn. Each gap carries its entitlement and
  cross-lane-ownership boundary.
use_when:
  - The capture-spine lane opens a build turn for any archive_org refinement or source-family adapter below.
  - The org-motion / judgment lane needs the capture-side seam + entitlement posture for these signals.
authority_boundary: retrieval_only
open_next:
  - docs/product/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md
stale_if:
  - The archive_org adapter changes build_cdx_availability_url / select_snapshot signatures.
  - The owner changes the capture risk posture (entitlement hard line) these specs hold.
  - A build turn lands any item below (move that item from spec to its decision record).
```

# archive_org Refinements + Source-Family Gap Specs (v0)

## Provenance and return lane

Couriered from the **judgment lane** (org-motion Beauty Pie backtest pilot, batch-1 case #3),
2026-06-11, which exercised the archive.org path by hand and surfaced these gaps. This doc is the
capture-spine **spec-draft** reply; **it returns to the judgment lane**. Spec only — preserves
existing `archive_org` behavior; no implementation until a separate authorized build turn.

## Hygiene check (asked first by the commission) — RESOLVED

**Canonical playbook = `docs/product/source_capture_toolbox/source_capture_playbook_v0.md`.**
Verified against primary source (directory listing, 2026-06-11): `source_capture_playbook_v0.md`
exists; **`capture_investigation_playbook_v0.md` no longer exists on disk** — it was the
pre-rename name (capture_investigation → capture_runner → source_capture) and is retired. Any
remaining reference to `capture_investigation_playbook_v0.md` is stale and should be repointed.
(Known loose end, capture-spine-owned: the canonical file's internal H1 still reads
"Capture-Investigation Playbook" — title-only drift, not a content fork.)

## Guardrails honored throughout

Public content only · never defeat an auth/access-control gate · market-level signal only, no
individual dossiers. Where a commissioned signal lives behind one of those lines, the spec says
**NO-GO/CATALOG_GAP under posture** and names the forward-commercial path — it does **not** spec a
gate-defeat. This aligns with the owner's affirmed sequence: *get proof → get commercial → invest
in the vendor's product, the vendor bears the ToS* (moat = judgment + cleaning, not a capture farm).

## Prioritization (capture-spine call — commission delegated this)

1. **A — date-bound CDX** — cheapest, code-anchored, removes a live latency/timeout footgun, and unblocks B.
2. **Companies House adapter** — cleanest GO (official free API, no entitlement risk); serves *both* ≤cutoff financial context and outcome verification.
3. **B — trajectory capture** — the core org-motion-trend enabler; depends on A; reuses the just-landed `archive_snapshot_time` typed timing field.
4. **D — URL-form sweep** — removes false NO-GOs; medium effort.
5. **LinkedIn public-surface trend sentinel** — entitlement-bounded; pre-commercial bridge only.
6. **Demand-side signals** — *cross-lane handoff to the demand spine*, not a capture-spine build (see item).
7. **Exec moves / departures** — mostly NO-GO under posture; public-proxy only; lowest capture-spine value.

---

## Part 1 — archive_org adapter + playbook refinements

### A. Date-bound the CDX availability query
- **Problem (code-verified):** `build_cdx_availability_url` (`orca-harness/source_capture/adapters/archive_org.py:114-128`) issues the CDX query with only `url/output/fl/collapse` — **no `&from=`/`&to=`**. `select_snapshot` (:149-161) filters `snapshot.timestamp <= cutoff_timestamp` **client-side** after `parse_availability_snapshots` has parsed *every* returned row. On a heavily-archived URL this pulls the full snapshot history each call → latency/timeout, and contradicts the discovery note's own "date-bound the CDX query" lesson.
- **Goal:** accept an optional date window and apply `&from=`/`&to=` (Wayback 14-digit form) on the CDX call; **keep** the `<=cutoff` client-side selection as the anti-leakage guarantee. Defense-in-depth: server-side window for cost, client-side `<=cutoff` for correctness.
- **Proposed shape:** add `from_timestamp` / `to_timestamp` (or a `window` tuple) to `fetch_archive_org_capture` + `build_cdx_availability_url`; when a `cutoff_timestamp` is supplied, default `to` = cutoff (never widen past cutoff server-side), leave `from` operator-supplied/None; validate via the existing `_validate_wayback_timestamp`.
- **Non-goals:** no change to `select_snapshot`'s `<=cutoff` rule (it stays the leak guard); no body-fetch-path change; no caching.
- **Acceptance:** CDX URL carries `from`/`to` when a window is given; a heavily-archived fixture returns within budget; the `<=cutoff` guard still excludes a post-cutoff snapshot even when the server window is wider; absent window → behavior byte-identical to today.

### B. First-class trajectory / time-series capture
- **Problem:** `select_snapshot` returns **one** snapshot (`max(eligible)`) and `fetch_archive_org_capture` fetches one body. A trend (org-motion hiring/headcount) needs a *series*; today that is N manual runs at N cutoffs.
- **Goal:** a trajectory mode capturing N snapshots across a date range at intervals into **one bundled receipt**, `<=cutoff` guard preserved **per snapshot**; at minimum, a documented helper + receipt shape for the N-run pattern.
- **Proposed shape:** `select_snapshot_series(snapshots, *, interval, from, to)` buckets the already-parsed list into intervals and selects one-per-bucket (max within bucket, each `<=` its bucket cutoff); `fetch_archive_org_trajectory` fetches each selected body and emits a bundled result (per-snapshot bodies + a manifest of selected timestamps + per-snapshot timing). **Reuses the typed `archive_snapshot_time` field** from the two-date timing contract (orca#24) for each series member, so each member dates to its own snapshot time, not fetch time.
- **Non-goals:** no scheduler/standing job; no new network behavior beyond N direct-HTTP body fetches (same rung); **no differencing/curve math** — that is the demand-projection consumer's job.
- **Acceptance:** a multi-snapshot fixture yields one bundled receipt with K members at the requested intervals; each member's selected timestamp `<=` its bucket cutoff; the single-snapshot path is unchanged.

### D. URL-form sweep before concluding "no coverage"
- **Problem:** archive coverage is URL-form-sensitive. Gate-0 evidence: `uk.linkedin.com/company/…` held a pre-cutoff snapshot the bare/`www` hosts did not; trailing-slash and `boards.eu` vs `boards` also flip results. Today `parse_availability_snapshots`→`[]`→`select_snapshot`→`None` returns NO_SNAPSHOTS on the *first* form, with no variant retry.
- **Goal:** a bounded variant-sweep (host/path forms) before returning NO_SNAPSHOTS, with the tried variants recorded in the receipt.
- **Proposed shape:** `url_form_variants(original_url)` generates a *capped* set (host: bare ↔ `www` ↔ known cc-subdomains e.g. `uk.`; path: trailing-slash on/off) feeding an ordered CDX sweep that stops at the first form with a pre-cutoff snapshot; record `variants_tried` + `variant_selected` in the availability metadata.
- **Non-goals:** no semantic URL rewriting; **no unbounded subdomain enumeration**; no change to selection once a form hits; a found snapshot remains subject to the entitlement gate (Part 2).
- **Acceptance:** a fixture where only `uk.` holds a pre-cutoff memento now returns it; `variants_tried` recorded; a truly-absent URL still returns an honest NO_SNAPSHOTS *after* the bounded sweep.

---

## Part 2 — source-family gaps (capture seam + entitlement + ownership)

### LinkedIn headcount / follower TREND (forward / live company page)
- **Problem:** not archive-backtestable (Wayback didn't capture mid-size company pages pre-2025) — the missing second org-motion leg.
- **Goal:** forward/live public company-page capture (size band, `numberOfEmployees`, follower count) building a go-forward trend; **market-level only, no individual dossiers**.
- **Proposed shape:** a forward sentinel reading the **public logged-out** company page (size band / follower count are visible there) at human rate, into a trajectory receipt (reuse B's series shape). **Entitlement hard line:** logged-out public fields only; **never** an authenticated read; if the public page gates a field behind login, that field is **NO-GO under posture** (do not defeat the gate). Per proof→commercial→vendor, the durable forward path is a commercial people-data vendor that bears the ToS — the public sentinel is the **pre-commercial bridge only**.
- **Non-goals:** no auth; no per-person tracking; no employee-list scraping.
- **Acceptance:** public size-band + follower count captured logged-out into a dated series; any login-gated field recorded as entitlement-NO-GO, not captured.
- **Ownership flag:** trend math/consumption is the org-motion/judgment lane's; capture spine owns only the public-surface read + receipt.

### Senior moves / departures
- **Problem:** behind LinkedIn auth; logged-out archive bytes don't carry it.
- **Goal (as commissioned):** a forward exec-moves signal using **entitled/public access only**.
- **Honest spec answer:** under the entitlement hard line this is largely **NO-GO / CATALOG_GAP for self-capture** — the signal lives behind auth and the posture forbids defeating it. In-posture capture-side options are narrow: **(a)** a public proxy — company "leadership"/team pages + press/PR + Companies House director appointments/terminations (next item); **(b)** a commercial people-moves vendor that bears ToS (forward-commercial path). Spec **(a)** as the public-proxy capture seam; name **(b)** as the forward path. **Do not** spec an authenticated LinkedIn capture.
- **Acceptance:** an exec-move proxy assembled from public filings/PR/leadership pages only; the LinkedIn-auth route explicitly recorded as out-of-posture.
- **Ownership flag:** signal definition is the judgment/org-motion lane's; capture spine holds the line and supplies the public proxy.

### Companies House filings
- **Problem:** a different source-family (structured UK filings) not primed; needed for ≤cutoff financial context **and** outcome verification.
- **Goal:** a CH adapter (accounts / filing history by company number).
- **Proposed shape:** a structured-API adapter against the **official Companies House public API** (free, registration-keyed — entitlement is a *free API key*, not a gate-defeat → clean GO). Methods: filing history + accounts by company number; map the **filing date as a real typed source date** into the packet timing contract (feeds ECR cleanly, exactly like the `archive_snapshot_time` fix). The cleanest GO in Part 2.
- **Non-goals:** no scraping the CH website (use the API); no paid data products.
- **Acceptance:** filings/accounts retrieved by company number via the official API with a key; filing dates typed into the packet; rate/posture documented.
- **Ownership flag:** capture spine owns the adapter; *which* filings matter is the org-motion/judgment lane's.

### Demand-side signals (the demand spine)
- **Problem:** the fusion's other half (search / social / review-velocity / traffic); without it backtests test org-motion against a thin baseline.
- **Goal:** a demand-signal capture.
- **Ownership flag (load-bearing):** this is the **demand-projection / demand-spine lane's** territory — note the active consumer-demand pivot (the wave of `docs/product/product_lead/*` + `*_consumer_demand_*` artifacts now on the branch). Capture spine should **not** design the demand spine's product. Capture-side answer: capture spine supplies the *capture seam* for whichever demand surfaces that lane selects — review-velocity already has recon (Bazaarvoice/Sephora GO; Reddit GO), and the creator-momentum surfaces are catalogued in `docs/research/creator_momentum_data_landscape_v0.md` — reusing the playbook routes. **Demand-signal selection + projection is a cross-lane handoff to the demand spine, not a capture-spine spec.**
- **Acceptance:** capture spine provides per-surface capture recipes on request; demand-signal *definition* deferred to the demand spine.

*(ATS / job-boards intentionally excluded per the commission — built elsewhere.)*

## Non-claims

Spec drafts only — not implementation, not validation, not readiness, not acceptance, not ECR
ratification, not a capture authorization. Code line numbers are evidentiary for the 2026-06-11
read of `archive_org.py` and must be re-verified at build time. Entitlement verdicts (LinkedIn
NO-GO-under-posture; Companies House GO) are posture calls under the current capture risk posture,
not legal advice. Each item moves from spec to its own decision record when a build turn lands it.
