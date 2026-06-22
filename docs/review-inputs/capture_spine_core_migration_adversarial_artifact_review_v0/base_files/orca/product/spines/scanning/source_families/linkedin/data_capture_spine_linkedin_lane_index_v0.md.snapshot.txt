```yaml
retrieval_header_version: 1
artifact_role: LinkedIn lane entry map (retrieval-only canonical index)
scope: >
  THE entry point for LinkedIn access in Orca. LinkedIn access is no-live,
  planning-only discovery under strict privacy rails -- this map ties the
  authority docs, the built harness slices, the rails, the deferred work, and the
  review provenance into one cold-start path.
use_when:
  - Starting cold on anything that touches LinkedIn discovery / access.
  - Choosing the source pack before building or reviewing a LinkedIn lane slice.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md
  - docs/workflows/linkedin_lane_operator_pilot_plan_v0.md
```

# LinkedIn Lane — Entry Map (v0)

**This is the canonical way to access LinkedIn in Orca.** All LinkedIn work is
**no-live, planning-only discovery** under strict privacy rails. It decides *who
is worth looking at* and hands a pointer forward; it never performs live access,
contact harvesting, graph capture, or content capture. If a task touches
LinkedIn, **start here**, then open the authority docs below — do not invent a
different path.

## The stages (one pipeline)

Discovery → Bounded Watch → Graph Frontier → Semantic Projection → Promotion →
(downstream Source Capture / Outreach — **separate** lanes, separately authorized).

## Authority (source of truth — read before building/reviewing)

- **Architecture:** `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md`
  — Candidate Row Schema, frontier node/edge vocab, person-basis rules, Hard
  Stops, Non-Claims, and the owner-accepted **D1** (influence + trajectory
  *corroborate* a basis, never replace it) and **D5** (owner-present
  attended-automation POC variant) additions.
- **Operator pilot + acceptance gate:** `docs/workflows/linkedin_lane_operator_pilot_plan_v0.md`.

## Built harness (no-live; frozen dataclass + StrEnum + module-level `validate_*`)

- **Slice 1 — candidate records:** `orca-harness/capture_spine/linkedin_lane/`
  (`RunEnvelope` + `CandidateRow` + validators). Tests:
  `orca-harness/tests/unit/test_linkedin_lane.py`.
- **Slice 2 — graph frontier:** `orca-harness/capture_spine/linkedin_graph_frontier/`
  (`FrontierNode`/`Edge`/`Decision` + `NextRunEnvelope` + validators; reuses
  slice-1's `LinkedInLaneError` + forbidden-output-field walk). Tests:
  `orca-harness/tests/unit/test_linkedin_graph_frontier.py`.
- Pattern siblings: `orca-harness/capture_spine/reddit_candidate_intake/`,
  `orca-harness/capture_spine/reddit_graph_frontier/`.
- Test interpreter: `C:\Users\vmon7\AppData\Local\Programs\Python\Python312\python.exe -m pytest <file>`
  (the sandbox default `python` lacks pytest).

## The hard rails (at a glance — architecture/pilot are authoritative)

- People qualify **only** on a concrete, org-chart-independent **public-actor
  basis**; junior / ordinary / non-public staff are **out**.
- **No** contact harvesting; **no** follower/connection/commenter lists or
  graphs; **no** profile body / post content capture; **no** Source Capture Packet (CapturePacket) output or Data Capture
  handoff.
- Every row is **planning-only**; **promotion is a separate gated step**.
- Each **frontier hop = a new, separately-authorized run** (no same-run traversal).
- No-live by default; an **owner-present attended-automation** / supervised-assist
  mode is opt-in, POC-risk-tagged, with `no-entitlement gate bypass` still a hard
  stop (a presence check is not per-action supervision and does not cure ToS).
- Validators enforce these in code (fail-closed key allowlists, excluded-basis
  gate, forbidden-field walk, person-privacy gate), **hardened via cross-vendor
  (GPT-5.5) delegated review + same-vendor recheck** (provenance below).

## Deferred / next

- **Slice 3 — Promotion** (register builder + `PromotionReceipt`, the gated
  pursue decision). Not built.
- **Open product question (the next move):** whether to include junior/ordinary
  people as **anonymized aggregate** "bottom-level" signal — a *feel* for
  bottom-level data **without** building any individual's dossier or row. Needs a
  deep-think + assumption-gate first (privacy-design lock-in). **Not yet decided.**
- **Bounded Watch / influence trajectory:** `orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_influence_trajectory_watch_spec_v0.md`.
- **Out-of-lane, legally-gated future lanes** (relationship-graph analytics;
  contact/outreach): `orca/product/spines/capture/operating_model/data_capture_spine_future_exploration_lanes_v0.md`.

## Review provenance

- Slice 1: `docs/review-outputs/linkedin_lane_harness_slice1_v0_no_repo_review_bundle.zip`.
- Slice 2: `docs/review-outputs/linkedin_graph_frontier_slice2_v0_no_repo_review_bundle.zip`.
- Both: cross-vendor (OpenAI/GPT-5.5) `cross_vendor_discovery` review + same-vendor
  bounded recheck; `authored_by: claude-opus-4.8`.
- Known follow-up: slice 1's `non_claims` check shares slice 2's F4 positive-claim
  weakness (logged, not yet patched).

## Non-claims

Not live LinkedIn access; not validation or readiness; not promotion / capture /
outreach execution; not commercial use. A no-live planning harness with its
privacy/safety rules enforced in code and independently stress-tested — nothing
more.
