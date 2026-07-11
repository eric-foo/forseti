# Forseti Research Engine Map v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow navigation artifact (research-engine cross-spine grouping map)
scope: >
  Colloquial cross-spine grouping map. Names the three data-extraction spines --
  Commission Signal Board (CSB), Scanning, and Capture -- collectively as the
  "research engine" and routes a reader to each spine's front door. Map and label
  only; introduces no new spine, authority, or structure.
use_when:
  - Orienting to what "the research engine" means as a colloquial grouping.
  - Finding the front door for CSB, Scanning, or Capture from one place.
  - Deciding whether a task is data extraction (research engine) or downstream provenance/cleaning/judgment.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/README.md
  - forseti/product/spines/scanning/README.md
  - forseti/product/spines/capture/README.md
stale_if:
  - A spine joins or leaves the CSB -> Scanning -> Capture extraction group, or one of them is renamed/retired.
  - The Capture -> ECR handoff stops being the boundary between extraction and downstream provenance/cleaning/judgment.
  - Any spine's front-door README below moves or is renamed.
```

> **What this is.** A colloquial grouping label, not a spine and not authority.
> "Research engine" is a name for three spines that already exist and already own
> their own rules; this map only points at their front doors and states where the
> group ends. It is the map, not the authority: on any conflict, the pointed-to
> spine wins.
>
> **Do not use** this map as validation, readiness, a new spine, a rename, a
> structural change, source-access permission, or any authority over CSB,
> Scanning, or Capture.

## The Research Engine In One Screen

The "research engine" is the front half of the pipeline -- the part that goes out
and brings back raw material. Three spines, in order:

```
CSB ───────────▶ Scanning ───────────▶ Capture ──┊──▶ ECR ▶ Cleaning ▶ Judgment
decide what to    discovery: which      acquisition:    └ downstream: provenance,
look for; signal   venues are worth      turn signals      cleaning, judgment
& route board      it, hidden-venue      into preserved,   (NOT the research engine)
(evidence only)    + exact-query         contextualized
                   discovery             packets
```

The group ends at the **Capture -> ECR handoff**. Capture's job is to make signals
"capturable, inspectable, preserved, contextualized, and safe to hand to Evidence
Candidate Record" -- so the moment a captured packet is handed to ECR, we have left
data extraction and entered provenance/cleaning/judgment. Everything after that
seam (ECR, Cleaning, Judgment, and the shared Data Lake) is *not* the research
engine.

## The Three Lanes

| Lane | What it does | Front door |
| --- | --- | --- |
| **Commission Signal Board (CSB)** | Decides what to look for. An evidence/signals-only board that supplies the starting source-family and signal-route board a scan works from. Does not emit gate verdicts. | `forseti/product/spines/commission_signal_board/README.md` |
| **Scanning** | Discovery side. Tests which venues are actually valuable for the commissioned decision, finds hidden venues, runs bounded exact-query discovery, and emits candidates + `capture_request`s. Cites route state; does not bind capture routes. | `forseti/product/spines/scanning/README.md` |
| **Capture** | Acquisition side. Turns public/external signals into preserved, contextualized packets safe to hand to ECR. Owns route binding, the Source Capture Armory (anti-block toolbox), source families, and packet schema. | `forseti/product/spines/capture/README.md` |

## What Is Deliberately Not In The Group

The downstream spines are provenance/cleaning/judgment, not extraction, and keep
their own front doors:

- **ECR** (Evidence Candidate Record) -- integrity postures over captured slices. `docs/workflows/ecr_spine_submap_v0.md`
- **Cleaning** -- normalization, integrity labels, transformations. `forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- **Judgment** -- claim ladder, demand-read, conductor. `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- **Data Lake** (shared foundation) -- raw-packet preservation and keyed retrievability consumed across the above. `forseti/product/spines/data_lake/README.md`

## Terminology Note

"**Research engine**" (this page) = the CSB -> Scanning -> Capture extraction group.
Do not confuse it with "**answer engine**" (the AEO / answer-engine / search
research work under the Scanning answer-engine source family and
`docs/research/answer_engine/`), which is a source-family method inside Scanning,
not a name for the whole group.

## Non-Claims

This map is not validation, readiness, a new spine, a rename, a structural or
folder change, source-access permission, capture-route authorization, ECR /
Cleaning / Judgment authority, or buyer proof. It is a colloquial navigation label
so a reader can find the three extraction spines and the boundary from one place.
