# Capture Spine README

```yaml
retrieval_header_version: 1
artifact_role: Capture spine front-door index
scope: >
  Retrieval-only entry point for the Capture (acquisition-side) spine: what the
  spine is, its core acquisition layers, canonical artifacts, load order, and
  boundaries. Map only; routes to owning contracts and the Data Capture submap
  for deep routing. Does not fork or restate owner authority.
use_when:
  - Starting any Capture-lane task cold.
  - Finding which Capture layer or owner doc owns a capture question before source-access, packet, armory, source-family, or demand-durability work.
  - Deciding whether a task is acquisition (Capture-side) or downstream provenance/cleaning/judgment (ECR / Cleaning / Judgment).
authority_boundary: retrieval_only
open_next:
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - forseti/product/spines/capture/core/source_families/README.md
stale_if:
  - The Capture spine is renamed, retired, or merged into another spine.
  - The Capture -> Evidence Candidate Record handoff stops being the boundary between acquisition and downstream provenance/cleaning/judgment.
  - The Data Capture submap moves, is renamed, or is superseded as the deep-routing front door.
  - A layer owner named below (obligation contract, Source Capture Toolbox, source-families catalog) moves to a new path.
```

> **What this is.** A retrieval-only front door for the Capture spine. It tells a
> cold reader what the spine is and which owner to open for a capture question.
> It is the map, not the authority: on any conflict, the pointed-to owner source
> wins.
>
> **Do not use** this README as validation, readiness, source-access permission,
> capture-route authorization, implementation authorization, fixture admission,
> source-quality proof, or ECR / Cleaning / Judgment authority.

## What The Capture Spine Is

The Capture spine is the **acquisition side** of the research engine
(`CSB -> Scanning -> Capture`). It is the product-method layer — formally the
**Data Capture Spine** — that makes public/external signals **capturable,
inspectable, preserved, contextualized, and safe to hand to Evidence Candidate
Record (ECR)**.

Core principle (from the architecture blueprint):

```text
Capture is the obligation. Mode is subordinate.
```

Capture modes (human-led, agent-assisted, structured access, archive/history,
automated extraction, multimodal, or mixed) may vary; a mode is acceptable only
when it can discharge the evidence-grade capture obligations for the
decision-framed signal. Capture v0 is **commissioned-capture-only**: capture for
a Decision Frame that already exists. Standing/opportunistic collection before a
Decision Frame is a separate **Corpus Intake / Candidate Signal Intake** lane and
is not ECR-ready evidence until rebound under a Decision Frame.

Where Capture sits, and where it stops:

```text
CSB -> Scanning -> Capture ──┊──▶ ECR ▶ Cleaning ▶ Judgment
decide     discovery   acquisition:   └ downstream: provenance,
what to    (venues,    preserve +       cleaning, judgment
look for   candidates, contextualize    (NOT the Capture spine)
           capture_    packets safe
           requests)   to hand to ECR
```

Capture records capture facts, capture limits, and capture posture. It does
**not** decide credibility, discounting, exclusion, Signal Use Classification,
Decision Strength, Action Ceiling, cleaning, or judgment. The moment a captured
packet is handed to ECR, the work has left acquisition.

## Core Layers

All reusable acquisition machinery lives under `core/`. Each row points to the
owning source; this README does not restate them.

| Layer | What it owns | Open |
| --- | --- | --- |
| Contracts — obligations | What a captured signal must preserve and what it must not decide, before categorical handoff to ECR. | `core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md` |
| Contracts — source-access boundary | Discoverable-or-entitled + disclosable standard, owner-accepted anti-blocking posture, and hard stops; method plan. | `core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md` |
| Contracts — candidate / corpus intake | Bounded candidate-URL intake before promotion, and the standing-capture Corpus Intake obligation home. | `core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md`, `core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` |
| Operating model | Owner-accepted v2 operating-model architecture, obligation baseline, lane thesis, and bounded pressure-test commissioning/closeout. | `core/operating_model/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md` |
| Packet schema | Source Capture Packet core-facts vs typed-attachment split and the schema-evolution boundary. | `core/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md`, `core/packet_schema/source_capture_core_payload_split_explainer_v0.md` |
| Source Capture Toolbox (Armory) | Source-access method, shared capture tooling, anti-block ladder, packet core, source-quality support. | `core/source_capture_toolbox/README.md` |
| Source families | Known capture-to-lake route homes (fragrance-native DB, retail/PDP, vendor pricing, social IG/TikTok/YouTube/Reddit, creator registry, cross-archive). | `core/source_families/README.md` |
| Source taxonomy | Re-derivable multi-axis classification over incumbent source-family/source-surface strings, including unknown residual posture. | `core/source_taxonomy/source_classification_compatibility_contract_v0.md` |
| Demand-durability indicators | Capture profiles for durability indicators (price time-series, availability/restock, search interest, review velocity) plus the shared capture-envelope durability delta they consume. | `core/demand_durability_indicators/demand_durability_indicator_capture_deconfliction_note_v0.md` |

The blueprint (`core/operating_model/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`)
is the canonical layer-split rationale — open it to decide whether a capture rule
belongs in core, satellite, deferred runtime, or another layer.

## Load Order / Where To Start

1. **Deep routing:** open the Data Capture submap,
   `docs/workflows/data_capture_spine_consolidation_map_v0.md`. It is the
   `retrieval_only` router that reaches every capture owner (obligations,
   source-access authority, armory components, packet lifecycle, source families,
   harness implementation, source-quality support) in one hop, plus the current
   bounded Reddit pre-commercial ordering.
2. **Lake-first radar preflight:** before external capture in a recurring or
   actively radarred source family, inspect the relevant Silver/current view,
   then packet or catalog inventory, then raw material when necessary. Reuse an
   appropriate existing packet unless recapture materially improves currentness,
   fidelity, provenance, cutoff compliance, inspectability, or fills a named
   gap. Lake inspection is not proof of current external reality; absence from
   Silver is not absence from the lake or the world, and a missing read model
   does not block acquisition.
3. **What a packet must preserve:** open the obligation contract, then the
   blueprint, for capture obligations, discharge states, and the ECR handoff
   boundary.
4. **Method + tooling:** open the Source Capture Toolbox (Armory) README for
   source-access method, the anti-block ladder, the packet core, and
   source-quality support.
5. **A known platform:** open the source-families catalog for the owning family
   index and its runner / projection / lake / cleaning seams. If a source has no
   row there, treat it as a new-source probe under the Source Capture Playbook.
6. **Standing durability indicators:** open the demand-durability-indicators
   layer only for recurring price / availability / search-interest / review-
   velocity capture profiles; these are indicator capture profiles, not demand
   proof.

## Boundaries

This front door — and the Capture spine it indexes — does **not** authorize:

- source access, scraping, crawling, scaling, storage, dashboards, schedulers,
  deployment, or production runtime (build authority lives in the source-access
  tooling authorization decision, not here);
- ECR, Cleaning, or Judgment work — those downstream spines keep their own front
  doors (`docs/workflows/ecr_spine_submap_v0.md`,
  `forseti/product/spines/cleaning/`, and the Judgment consolidation map);
- fixture admission, source-quality scoring, buyer proof, or commercial-readiness
  claims;
- implementation authorization for any code root — that requires an explicit
  bounded grant in the current turn or an accepted handoff.

Capture fulfills a bounded request or returns typed failure/route exhaustion.
It does not decide evidence-world completeness, marginal acquisition closure,
or final packet inclusion. No number of captures or targets establishes
completion.

## Automatic Checks / Enforcement

This README is a `retrieval_only` front door. Its retrieval-header shape is
**review-enforced**, not hook-enforced: the generic
`.agents/hooks/check_retrieval_header.py` deliberately skips `README.md` front
doors (it targets non-README durable artifacts), exactly as it does for the CSB
and Scanning spine READMEs. Its placement and reachability are covered by
`check_placement.py`, `check_map_links.py`, and
`check_repo_map_freshness.py`.

**No separate Capture output-artifact validator is built or warranted by this
front-door work.** The CSB and Scanning spine validators
(`.agents/hooks/check_commission_signal_board_output.py`,
`.agents/hooks/check_csb_scanning_artifact.py`) each check a single
prompt-shaped **output artifact** that carries overclaim risk — a CSB board
output, a CSB-first scan artifact — not their spine README. Capture has no
equivalent single text-output format: its outputs are **Source Capture Packets**
(multi-file directories) and typed source-family artifacts, already guarded by
the `forseti-harness/tests/` contract and unit suite (packet core, no-network /
no-deferred-adapter guards, per-adapter and per-source-family contract tests).
A bespoke Capture output-artifact validator would therefore have no single
target to validate that the harness suite does not already cover. This mirrors
the source-families catalog's own "Enforcement Candidate (Evaluated, Not Built)"
decision. Building
or wiring any code-root check (script, tests, CI) requires separate explicit
bounded implementation authorization; none is granted by this front-door work.

## Onward

For deep routing across every capture owner, open the Data Capture submap:

```text
docs/workflows/data_capture_spine_consolidation_map_v0.md
```
