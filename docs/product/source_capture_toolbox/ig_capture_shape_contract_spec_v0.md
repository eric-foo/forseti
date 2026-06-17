```yaml
retrieval_header_version: 1
artifact_role: implementation-facing behavior/contract spec (non-authorizing) — IG capture-shape contract
scope: >
  The behavior contract for the IG capture-shape: what each IG capture packet must preserve, per metric,
  so that momentum series are rebuildable and absence is never stored as an observed value. The smallest
  next build OBJECT of the capture→projection storage lane (the one deliberate, irreversible lock-in).
  Stabilizes required behavior, non-goals, the typed-observation contract, acceptance criteria, and the
  scoping handoff. PROPOSED; authorizes NO build.
use_when:
  - Scoping the IG typed-metric capture field on the source-capture packet (building it only after the separate explicit owner authorization + manifest-bump gate in Non-goals).
  - Checking what an IG capture must record per metric (value + typed posture + coverage) and why.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md   # the backbone this instantiates (capture-shape options, rebuild input set)
  - docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md           # the IG monitoring profile values
  - orca-harness/source_capture/models.py                                                       # the packet model (gated build target; NOT edited by this spec)
  - docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md   # governs the v1→v2 manifest bump
stale_if:
  - The owner overturns the capture-shape (b) decision, the posture enum, or the identity/conflict policy.
  - The backbone's Reframe 1 / rebuild-input-set is amended.
  - The models.py field-add is built (moves this from contract to implemented).
status: PROPOSED — IG capture-shape contract (advisory review AR-01..AR-05 CA-adjudicated + folded); instantiates the cross-vendor-reviewed backbone; authorizes no build
```

# IG Capture-Shape Contract — Spec (PROPOSED, v0)

**Confirm-don't-trust:** load-bearing sources — the backbone + monitoring policy (this lane, committed
`49b5d0b`); `orca-harness/source_capture/models.py` + the IG capture findings (ig-cadence-rails worktree
`@ c365dca2`); `source_capture_packet_schema_evolution_architecture_v0.md` (origin/main,
`ADOPTED_WITH_AMENDMENT_V0`). Re-verify before strict/actionable use.

**Spec status: `SPEC_COMPLETE_READY_FOR_SCOPING`**

## Required behavior

1. Each IG capture packet must record, **per metric in the IG metric set**, a **typed value**, a **typed
   availability posture**, and the capture's **coverage/window boundary** — such that absence, a null, a
   not-applicable metric, or an un-attempted read can **never** be stored as if it were an observed value
   (in particular, never as an observed `0`).
2. The capture shape is a **typed shared observation, discriminated on metric identity** (decision (b)) —
   not a bespoke field per metric (a), and not a single untyped `metric_value` column (c, rejected). Each
   observation carries its own typed value and its own posture.
3. **Value and posture are coupled at write time:** a value is present **iff** posture = `observed`; a
   reason is present **iff** posture ≠ `observed`. A non-observed observation carries no value.
4. **Typing is packet-recoverable via version pinning.** Each packet pins the manifest/registry version
   (the metric→typed-value mapping) and the identity/conflict-policy version. The typed series then
   rebuilds from **the packet plus the immutable, packet-pinned versioned registry + identity/conflict-policy
   definitions** — the backbone's invariant-0 rebuild input set (`packets + versioned registry + versioned
   id/conflict policy`), **not packets alone**. What is excluded is any **live or mutable external registry
   lookup**: the pinned versioned definitions are required, immutable rebuild inputs, not a runtime read.
5. **Identity is the stable numeric id**, never the mutable username; a re-capture of the same entity
   records a typed re-capture relationship.
6. Each capture declares, **at packet level**, **which posts / period it claims to cover** — a claimed
   post-set or discovery boundary plus the attempted set — so a post inside the claimed boundary but
   absent (in-window-missing) is distinguishable from one outside it and from one never attempted. (This
   is a packet-level coverage claim, distinct from the per-metric `coverage_window`; see Interfaces.)

## Non-goals

- **Authorizes no build — the whole typed-capture runtime/persistence surface is separately gated, not
  only `models.py`.** No runtime change is authorized here: not the `models.py` field-add, and not the
  serializers, capture writers, manifest migration / persisted-v1 read-back, projection rebuild readers,
  or tests — all are equally gated. The `models.py` field-add is in addition **double-gated**: (1) separate
  explicit owner authorization, and (2) the v1→v2 breaking `manifest_version` bump must handle
  persisted-v1-packet read-back per the schema-evolution doctrine (whose read-back mechanism is
  build-deferred) **or** confirm no v1 packets need to survive. This spec stabilizes the contract only.
- The derived projection EAV row, the projection store, cross-platform unification, the velocity/momentum
  derivation, and the monitoring **scheduler mechanics** are not defined here (other artifacts; rebuildable
  / deferred).
- `R` (safe reads/day), the at-scale repeated-harvesting behavior, and empirical confirmation that IG's
  logged-out surface distinguishes every posture-reason (private vs blocked vs rate-limited vs hidden) are
  **probe-confirmed at build**, not by this spec.

## Interfaces / contracts

- **Typed observation (per metric, on the capture packet):**
  `{ metric: <closed metric identity>, posture: MetricPosture, value: <typed, present iff observed>,
  reason: <present iff posture ≠ observed>, coverage_window: {start, end} }`.
- **`MetricPosture` (new closed enum):** `observed` / `unavailable_with_reason` / `out_of_capture_window`
  / `not_attempted` / `not_applicable`. (The AR-01 four **plus** `not_applicable`, required because an
  image post genuinely has no `view_count` — a distinct state from blocked/hidden/0.) `reason` is a
  closed-vocabulary token for the non-observed states (e.g. `private`, `blocked`, `rate_limited`,
  `metric_hidden`, `content_type_inapplicable`).
- **Packet identity/time metadata (NOT momentum metrics, no `MetricPosture`):** `numeric_id` (the stable
  identity anchor) and `capture_time` are **required packet metadata**, not posture-bearing observations.
  If `numeric_id` cannot be resolved the packet is **identity-incomplete** — a distinct packet-level
  failure surfaced as such, **not** a metric that is `unavailable_with_reason`; a capture cannot exist
  without a `capture_time`. This keeps the identity anchor from being modeled as an optional/absent metric.
- **IG momentum metric set + value types (each carries `MetricPosture`):** account-level —
  `follower_count` (int ≥ 0); per-post, keyed by `shortcode` + `timestamp` — `view_count` (int ≥ 0),
  `like_count` (int ≥ 0), `comment_count` (int ≥ 0). Each carries a typed value + posture per the coupling
  above.
- **Identity / conflict policy (versioned, concretely identified):** stable key = `numeric_id`;
  `username` = mutable attribute; re-capture relationship ∈ `{supersede, supplement, conflict, mixed}` —
  the **existing `RE_CAPTURE_RELATIONSHIP_VALUES` frozenset in `models.py`** (confirmed), not reinvented
  here. Each packet pins a **concrete identity/conflict-policy version identifier** (a named, immutable v0
  policy artifact, named at build) so two implementers classify the same re-capture identically. The
  **assignment criteria** for the four relationship states are owned by that versioned v0 policy artifact
  (deferred to it), recoverable via the pinned version — not silently undefined and not invented in this
  contract.
- **Version pinning:** each packet carries the `manifest_version` (its metric→type mapping) and the
  identity/conflict-policy version. The pinned versioned definitions are **required, immutable rebuild
  inputs** (backbone invariant 0), retrieved by version — **not a live/mutable external registry lookup**.
- **Packet-level coverage claim (distinct from per-metric `coverage_window`):** each capture packet
  declares its **claimed coverage** — the period and the claimed post-set or discovery boundary (e.g.
  "all grid posts back to cursor X" / "posts in [start,end]") — and its **attempted set**. A post inside
  the claimed boundary but absent from the attempted/observed set is representable as **in-window-missing**
  (post-level `not_attempted` / `unavailable_with_reason`), distinct from a post **outside** the boundary
  (`out_of_capture_window`). The per-metric `coverage_window` narrows coverage **within** an observed post;
  it does not by itself represent a missing post. (Exact encoding → scoping; the contract requires the
  claim to exist.)
- **IG monitoring profile (the contract's monitoring parameters; all R-tunable):** content-unit =
  reel/post; momentum metric = `view_count`; curve window ≈ 30d; age-bucket cadences 0–5d daily / 6–15d
  every 3d / 16–30d weekly; per-creator concurrently-tracked cap K ≈ 30; Tier-C heartbeat ≈ weekly.

## Acceptance criteria

- A **video-post** capture records `view_count` with posture `observed` and a typed integer value —
  including a genuine `0` recorded as observed `0`.
- An **image-post** capture records `view_count` with posture `not_applicable` + reason, and **no value**.
- A **blocked / private / rate-limited / hidden** metric records posture `unavailable_with_reason` + the
  matching reason token, and no value.
- A metric **outside the declared coverage window** records posture `out_of_capture_window`; an
  un-attempted metric records `not_attempted`; neither carries a value.
- No capture can store a **non-observed** metric **with** a value (the coupling invariant rejects it).
- Two captures of the same creator under **different usernames but the same `numeric_id`** resolve to one
  entity; a conflicting re-capture records a typed re-capture relationship.
- A capture whose **`numeric_id` cannot be resolved** is recorded as **identity-incomplete** at packet
  level — never as a momentum metric carrying posture `unavailable_with_reason`.
- A metric's **typed series is reconstructable from packets + the immutable packet-pinned versioned
  registry/policy** (the backbone invariant-0 input set), with **no live/mutable external registry read** —
  not from packets stripped of their pinned definitions.
- A post **missing** from a capture's claimed coverage window is distinguishable from one **not attempted**
  and from one **out of window**, because the packet declares its claimed/attempted post boundary (not only
  per-metric `coverage_window`).

## Later attachment-boundary update

`docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md`
settles the general tenant/source-family attachment target after this IG spec:
current slice-attached `metric_observations` are transitional/incumbent, and
new tenant/source-family payloads target packet/slice-keyed logical extension
envelopes. This update does not authorize IG runtime changes, packet migration,
or a physical storage shape.

## Open questions

- **Resolved by later attachment-boundary artifact:** the general target is
  packet/slice-keyed logical extension envelopes for new tenant/source-family
  payloads. The exact encoding of current IG fields, any dual-read/replay path,
  and any physical storage shape remain separately gated and deferred.
- **Deferred to build/probe:** empirical confirmation that IG's logged-out surface lets capture fill each
  posture-reason in practice. *Safe to defer:* the contract defines the reasons; the probe confirms fill.
- **Deferred to build (gated):** the v1→v2 manifest bump + persisted-v1 read-back handling + the owner
  authorization for the runtime field-add. *Safe to defer:* these gate the build, not the contract's intent.
- **Resolved here:** capture shape = (b); `MetricPosture` = AR-01 four + `not_applicable`; value↔posture
  coupling; identity = `numeric_id` (packet metadata, distinct from posture-bearing metrics);
  version-pinning makes typing packet-recoverable **from packets + the pinned versioned registry/policy**
  (backbone invariant 0, not packets alone); packet-level coverage claim distinguishes in-window-missing
  from out-of-window and not-attempted.
- **Deferred to scoping (added by review fold):** the exact encoding of the packet-level coverage claim
  and the concrete v0 identity/conflict-policy version identifier + its state-assignment criteria. *Safe to
  defer:* the contract requires both to exist and be packet-pinned; their encoding/criteria do not change
  what must be true.

## Advisory review disposition (AR-01..AR-05, CA-adjudicated)

An advisory `no_repo` review returned **5 findings, 0 blocking**, recommending the spec not be treated as
scoping-ready until packet-recoverable typing, coverage/window representation, identity-policy versioning,
and the build-gate scope were tightened. Each was **CA-adjudicated against primary sources this session**
(the backbone's invariant 0 + the `models.py` types), not accepted on the reviewer's say-so — claims to
adjudicate, not premises to inherit:

- **AR-01 (packet-recoverable typing) ACCEPTED** → "packet alone" was an overclaim that contradicted the
  backbone's **invariant 0** (`rebuild = packets + versioned registry + versioned id/conflict policy`,
  packet-pinned, "not packets alone"). RB#4 + version-pinning interface + acceptance reworded to the
  invariant-0 input set; only a **live/mutable** external registry read is excluded.
- **AR-02 (coverage/window not executable) ACCEPTED** → added a **packet-level coverage claim** (claimed
  post-set/discovery boundary + attempted set) distinct from the per-metric `coverage_window`, so an
  in-window-missing post is representable; RB#6 + an interface bullet + acceptance updated.
- **AR-03 (identity/conflict policy versioning) ACCEPTED (modified)** → the relationship vocabulary is the
  **confirmed existing `RE_CAPTURE_RELATIONSHIP_VALUES` frozenset** in `models.py`; the spec now requires a
  **concrete pinned policy-version identifier** and assigns the state-criteria to the versioned v0 policy
  artifact (deferred, not silently undefined).
- **AR-04 (numeric_id conflation) ACCEPTED** → `numeric_id` + `capture_time` split out as **packet
  identity/time metadata** (no `MetricPosture`; unresolved `numeric_id` ⇒ identity-incomplete), separate
  from the posture-bearing momentum metric set — matching the backbone's separate identity plane.
- **AR-05 (build fence too narrow) ACCEPTED** → the no-build fence now covers the **whole
  runtime/persistence surface** (serializers, writers, migration/read-back, projection readers, tests),
  not only `models.py`; the header `use_when` conditions "building" on the separate authorization.

Advisory cross-vendor review, CA-adjudicated — **advisory input, not a formal verdict or owner adoption.**
`authored_by: claude-opus-4-8`; `reviewed_by: <model — operator-couriered; vendor/de-correlation UNCONFIRMED
by CA>`. The acceptances are independently backed by primary-source reads (backbone invariant 0; `models.py`
`VisibleFactStatus` / `RE_CAPTURE_RELATIONSHIP_VALUES` / `SourceCaptureSlice`), so they do not rest on the
reviewer's vendor.

## Downstream handoff

```yaml
spec_handoff:
  status: SPEC_COMPLETE_READY_FOR_SCOPING
  required_behavior: "Per-metric typed value + typed posture on each IG capture packet (shape (b)); value↔posture coupled; numeric_id/capture_time are packet identity/time metadata (not posture metrics); packet-level coverage claim (claimed+attempted post boundary) distinct from per-metric coverage_window; typing packet-recoverable from packets + pinned versioned registry/policy (backbone invariant 0)."
  non_goals: "No build of the whole typed-capture runtime/persistence surface (models.py field-add double-gated; serializers, writers, migration/read-back, projection readers, tests equally gated); no projection store, EAV row, cross-platform unification, velocity layer, or scheduler mechanics; R + at-scale posture fill are probe-confirmed."
  interfaces_contracts: "Typed observation {metric, posture, value, reason, coverage_window}; MetricPosture closed enum (AR-01 four + not_applicable); momentum metric set + int types separate from numeric_id/capture_time packet metadata; concretely-versioned numeric-id identity/conflict policy (RE_CAPTURE_RELATIONSHIP_VALUES); packet-level coverage claim; manifest + policy version-pinning as immutable rebuild inputs."
  acceptance_criteria: "observed-0 vs not_applicable vs unavailable_with_reason vs out_of_capture_window vs not_attempted all distinguishable; no value on non-observed; same numeric_id across usernames = one entity; unresolved numeric_id = identity-incomplete (not a metric posture); series rebuildable from packets + pinned versioned registry/policy (no live registry read); missing-in-window ≠ out-of-window ≠ not-attempted."
  deferred_open_questions:
    - "exact sub-model placement + discriminated-union encoding -> scoping"
    - "empirical IG posture-reason fill -> build/probe"
    - "v1->v2 bump + persisted-v1 read-back + owner authorization -> gated build"
    - "packet-level coverage-claim encoding + concrete v0 identity/conflict-policy version id + state-assignment criteria -> scoping/policy artifact"
  review_timing_advisory:
    adversarial_review: recommended
    highest_value_checkpoint: after_artifact_pre_implementation
    review_target: "this IG capture-shape contract spec"
    why_this_checkpoint: "it binds the one irreversible, un-re-capturable lock-in; reviewing before the build implements it prevents baking a wrong typed shape into manifest v2."
  scoping_may_rely_on: "the (b) decision, the MetricPosture enum + coupling, the momentum metric set + types (separate from numeric_id/capture_time metadata), the concretely-versioned numeric-id identity/conflict policy, the packet-level coverage claim + per-metric coverage_window, and per-packet manifest/policy version pinning as immutable rebuild inputs (backbone invariant 0)."
```
