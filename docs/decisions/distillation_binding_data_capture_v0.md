# Distillation Binding — Data Capture / Source Capture Harness (prepare-only draft)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: per-spine distillation binding for the Data Capture / Source Capture lane (Reddit Candidate URL Intake, Graph Frontier, Source Capture packets)
use_when:
  - Distilling a Data Capture / Source Capture lane lesson into a carried rule.
  - Reasoning about intake access mode, raw-HTML hygiene, or old-Reddit parsing.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/distillation_doctrine_orca_spine_bindings_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/decisions/distillation_binding_orca_harness_code_v0.md
```

**Status: PREPARE-ONLY DRAFT** (see the index). Distills **lane-level** Data Capture outcomes
(operator/agent judgment). The deterministic **code chokepoints** that enforce parts of this lane
(secret-value reject, content-lossless view) live in the orca-harness code binding and are
**referenced here by their canonical `node` id, not duplicated** (doctrine: one canonical cell, no
leak). Reads recorded outcomes; edits no Data Capture file; authorizes no live fetch, proxy,
crawling, storage, or ECR/Cleaning/Judgment work.

## Harness bound

The agent operating the Data Capture / Source Capture lane: Reddit Candidate URL Intake (consume
operator-supplied or live-fetched source surfaces → candidate rows + provenance), Reddit Graph
Frontier (bounded planning register), and Source Capture Armory packets. Governed actor: the agent
running the lane.

## Pole / key finding

**Mixed.** Lane decisions (access mode, what to persist, how to parse a surface) are actor-carried
judgment; several are partly enforced downstream by the orca-harness chokepoints. The recurring miss
is conflating *operator browser access* with *lane fetch capability*, and persisting raw-input chrome
into durable output.

## A1 — outcome → cell pairs (real, cited)

### GUARD intake-not-live-fetch  (actor-carried)
- decision_node: `node:candidate-intake-access-mode`
- `GUARD intake-not-live-fetch: WHEN Candidate URL Intake consumes operator-supplied saved HTML → record that intake did NOT fetch Reddit / CloakBrowser / .json; a future live fetch is a separate gated pilot → UNLESS a live-access pilot is separately authorized.`
- outcome_class: a no-live operator-supplied-HTML run is mis-read as proof the agent can freely fetch Reddit
- causal_miss: missing distinction — operator browser access happened *outside* the lane; the lane did not fetch
- verification: under-case (operator-saved HTML consumed) → access-mode recorded as no-live; over-edge (an authorized CloakBrowser pilot) → recorded as live-access pilot
- substrate: actor-carried (partial: the live runner writes rows/provenance/receipt only)
- PROV: `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md:48-52` "Candidate URL Intake did not fetch Reddit; did not invoke CloakBrowser/proxy; did not call Reddit `.json`". tier: probed (first pilot). date 2026-06.

### GUARD raw-html-scratch-only  (actor-carried; PARTIAL via code chokepoint)
- decision_node: `node:raw-html-projection`
- `GUARD raw-html-scratch-only: WHEN consuming operator-supplied old-Reddit HTML → do NOT persist account chrome / session-like fields / expanded snippets into candidate output or receipts; treat the raw HTML as scratch → UNLESS it is a clean visible listing link.`
- outcome_class: logged-in chrome / session fields / body-like snippets get persisted into durable candidate output
- causal_miss: treating raw input as durable Capture output instead of scratch
- verification: under-case (HTML with logged-in chrome) → chrome not persisted; over-edge (a clean listing anchor) → persisted
- substrate: actor-carried core; PARTIAL — the orca-harness secret-value chokepoint (`node:no-forbidden-output-fields-chokepoint`, canonical cell `GUARD secret-value-chokepoint`) enforces the credential subset by construction
- PROV: `reddit_candidate_intake_old_reddit_search_surface_handling_v0.md:68-72` "Candidate URL Intake must not persist any of that material into candidate output or receipts ... treat the raw HTML as scratch input only". tier: probed. date 2026-06.

### GUARD old-reddit-anchor-coverage  (actor-carried)
- decision_node: `node:old-reddit-anchor-parse`
- `GUARD old-reddit-anchor-coverage: WHEN parsing old-Reddit result pages → treat BOTH title and search-title anchors as candidate thread anchors → UNLESS the listing class names have changed (stale_if).`
- outcome_class: parsing only `title` anchors yields empty results on search pages that use `search-title`
- causal_miss: missing case — the `search-title` surface (discovered in the first pilot) was not covered
- verification: under-case (a search page using `search-title`) → anchors found; over-edge (changed class names) → flagged stale, not silently empty
- substrate: actor-carried (could be code-enforced in the projection parser)
- PROV: `reddit_candidate_intake_old_reddit_search_surface_handling_v0.md:74-89` "Candidate URL Intake should treat both `title` and `search-title` anchors as candidate thread title anchors"; surface "discovered during the first operator-supplied pilot". tier: probed. date 2026-06.

## A1b — proposed cell (HELD; pending slice-F build verification)

Distilled 2026-06-14 from the backtest/MGT capture-robustness pass. **Held, not installed:** the
decision node is a proposed spine-addition (not yet on A3's accepted spine) and the under-case is
OWED (verifiable only when slice F — body-retrieve escalation — is built). Recorded here so the
lesson is retrievable at that build; it is not an accepted/verified cell and competes for no budget
until its under-case runs. Adding it to this prepare-only binding is **not a doctrine change → no
`direction_change_propagation` receipt owed** (per `distillation_doctrine_orca_spine_bindings_v0.md`).

### GUARD probe-then-pin  (actor-carried) — HELD
- decision_node: `node:capture-rung-selection`  (**PROPOSED** spine-addition)
- `GUARD probe-then-pin: WHEN fetching a source/archive with a multi-rung capture ladder → probe once (escalate cheapest-first) to find the cheapest working rung, pin it (record per source/archive via the capture-recon-index cheapest-GO-rung pattern), then fetch direct at the pinned rung → UNLESS the pinned rung fails OR its output degrades — slice-G verification / quality sub-floor, not just transport (then re-probe).`
- outcome_class: running the full capture escalation ladder on *every* fetch when a source/archive has multiple rungs — a per-fetch cost that should be a one-time discovery cost
- causal_miss: missing distinction between rung DISCOVERY (probe for the cheapest working rung) and STEADY-STATE fetch (reuse the pinned rung); treating the ladder as a per-fetch runtime cost
- verification: under-case (a multi-rung source fetched repeatedly → steady-state goes direct at the pinned rung, no re-walk) — **OWED, verify at slice-F build**; over-edge (pinned rung starts failing → re-probe fires, does not hammer a dead rung) — **OWED, verify at slice-F build**
- substrate: actor-carried (rung selection is lane judgment; the capture-recon-index cheapest-GO-rung record is the pin)
- conflict_check: none — A3 has no rung-selection cell; consistent with the capture-recon-index cheapest-first ladder; contradicts none of the A1 cells
- tier: probed (design-time capture) — **capped; under-case OWED so meets no verified tier yet**
- retirement_test: capture standardizes on a single rung (no ladder), or per-fetch re-walking becomes free
- PROV: slice-F spec (`archive_org_refinement_and_source_family_gap_spec_v0.md` §F, PR #81); `capture_recon_index_v0.md` already records cheapest-GO-rung per source (the pin substrate). blind_spot: slice-F nearly committed to a full ladder per fetch; owner caught it → probe-then-pin. n=1 (design-time catch). date 2026-06.

## A2 — core size / budget

Lane cells are actor-carried and compete for budget; the credential subset of `raw-html-scratch-only`
is code-held (no extra budget). `intake-not-live-fetch` is `silent-wrong-output`-class (a false
capability claim is a silent overreach risk) → prune-exempt from frequency-only retirement. Budget
model-dependent; not fixed here.

## A3 — spine / decision nodes

`node:candidate-intake-access-mode` · `node:raw-html-projection` · `node:old-reddit-anchor-parse` ·
`node:graph-frontier-seed` (planning only; no same-run traversal) · `node:capture-packet-emit` ·
`node:no-forbidden-output-fields-chokepoint` (referenced; canonical home = orca-harness binding) ·
`node:capture-rung-selection` (**PROPOSED** spine-addition — pending owner acceptance; see A1b).

## A4 — slots filled

- **intervention-type set** (closed; owner-extensible): `GUARD`, `SOURCE-RULE`, `CONTRACT-GATE` (chokepoint, referenced).
- **verification substrate**: the orca-harness chokepoint tests for the code-held subset; otherwise lane-side review of runs against the runbook.
- **fire-log capability**: MODERATE at the lane (run receipts), STRONG for the referenced code chokepoints.
- **tier enum**: {accepted-orca-gate, probed, asserted}; recorded cells are probed.
- **review window**: owner sets (per pilot / lane change).
- **owner map**: the Data Capture / Source Capture lane owner.

## Secondary finding

The lane's strongest *recorded* discipline is already in code (the orca-harness chokepoints); the
genuinely actor-carried remainder is access-mode framing and surface coverage — exactly where
judgment, not a substrate, decides. Referencing the canonical code cells (not copying) keeps a cell
from leaking across two spines.

## Scaffold / boundaries (no cell invented)

The proxy / anti-blocking hard stops and the Graph-Frontier "no same-run traversal / no live fetch"
boundaries are guardrails recorded in the source-access authorization and architecture docs, not
recorded *wrong actions*; they are named as boundary slots, not distilled into cells. The current
branch's **ECR deriver** (SP-3/SP-6) work has no distinct recorded outcome yet — deferred sub-node.

## Non-claims

Prepare-only; edits no Data Capture file; authorizes no live Reddit fetch, proxy, broad crawling,
storage, scheduler, dashboard, deployment, ECR, Cleaning, Judgment, fixture admission, or
source-quality scoring; placement is not authority.
```
