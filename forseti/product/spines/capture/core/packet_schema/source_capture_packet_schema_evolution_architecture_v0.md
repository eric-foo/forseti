# Source Capture Packet Schema Evolution + Validation Placement — Architecture Routing Object v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: >
  Non-executing architecture recommendation for Source Capture packet schema
  evolution: where strict current-schema validation belongs, how persisted
  hash-pinned packets survive future breaking schema changes, and the
  owner-reserved trigger that should move the chosen mechanism from deferred to
  built. Output of the architecture-planning pass surfaced by the R2
  posture-vocabulary closure.
use_when:
  - Deciding or reviewing how Source Capture packets should handle schema
    version skew on read-back, admission, or consume.
  - Before authoring an implementation-scoping lane for packet read-back or a
    fixture-admission / ECR consume gate.
authority_boundary: retrieval_only
open_next:
  - orca-harness/source_capture/models.py
  - orca-harness/source_capture/source_quality.py
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md
input_hashes:
  orca-harness/source_capture/models.py: 3B89A19BAEAB90762C34FE0C95517A005D383933E48057C1ADD12E004A3A7245
branch_or_commit: main @ d69aeee (worktree dirty; controlling overlay/doc/code sources uncommitted/untracked)
downstream_consumers:
  - Owner decision on adopting this target architecture and/or authorizing the lenient-read slice.
  - A future implementation-scoping lane for the lenient read-back slice (gated on owner acceptance).
  - The fixture-admission frontier lane (AC-10) — coordinate, not absorb.
stale_if:
  - R2 posture-vocabulary closure is reopened or superseded.
  - A second breaking manifest_version bump (v1 -> v2) is proposed or landed.
  - AC-10 resolves (a named downstream consumer of Source Capture output appears).
  - orca-harness/source_capture/models.py SHA256 drifts from the pinned input_hash above.
```

## Status

`ADOPTED_WITH_AMENDMENT_V0` — adjudicated 2026-06-05; direction adopted, build NOT authorized; see **Adjudication & Amendment** at end (reviewed as v0 @ `8FDD1FDA…E7E9`). Planning-only, NON-EXECUTING. This
routing object **recommends** a target architecture and an owner-reserved build
trigger. It asserts no binding rule, changes no source/schema/code/contract,
authorizes no build, and does not admit any packet. Adoption and any build
authorization are owner decisions (see Owner-Reserved / Separate-Lane Note).
Architecture result: **`TARGET_RECOMMENDED`** (with the build owner-gated and the
satellite machinery deferred).

## Start Preflight (completed)

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (Source Capture packet schema-evolution pack named by the prompt)
  edit_permission: docs-write   # this plan only; read-only for all source/code
  target_scope:
    - docs/product/source_capture_packet_schema_evolution_architecture_v0.md
  dirty_state_checked: yes   # main @ d69aeee; worktree broadly dirty incl. controlling overlay sources and untracked packet reports
  blocked_if_missing: no (all named sources present and read)
external_source_boundary: agent-workflow reusable mechanics only; jb is NOT Orca authority.
doctrine_propagation_expected: none for this artifact (asserts no binding rule); owner adoption / build authorization would carry the receipt — see note below.
```

## Source Readiness — `SOURCE_CONTEXT_READY`

Method sequence followed: read authority (`AGENTS.md`, overlay `README`,
`prompt-orchestration`, `source-of-truth`); `REFERENCE-LOAD`ed
`workflow-deep-thinking` then `workflow-architecture-planning` from the
`agent-workflow` source repo (procedural guidance only; not applied before
source readiness); `SOURCE-LOAD`ed the pack; declared `SOURCE_CONTEXT_READY`;
then `APPLY`ed deep-thinking to frame failure modes and architecture-planning to
compare options and name this routing object.

Anchor hash confirmed (this lane **and** independently by all three subagents):
`orca-harness/source_capture/models.py` SHA256 =
`3B89A19BAEAB90762C34FE0C95517A005D383933E48057C1ADD12E004A3A7245` — exact match,
no drift.

Source-read ledger (decisive facts, verified against source):

| Source | Decisive fact |
| --- | --- |
| `orca-harness/source_capture/models.py` | `SourceCapturePacket(StrictModel)`; `StrictModel` = `extra="forbid"` (`schemas/case_models.py:11`). `manifest_version` is a plain `str` (`models.py:162`) with **no validator and no reader**. `SOURCE_CAPTURE_MANIFEST_VERSION="source_capture_packet_manifest_v1"` (`models.py:12`). R2 closed-vocab + `hash_basis` validators present (`models.py:53-66,82-94,105-114,185-199`). |
| `orca-harness/source_capture/source_quality.py` | **Only** production read-back: `SourceCapturePacket.model_validate(...)` at `:99` (strict; raises on a v0 packet). The multi-row census path `_assemble_source_quality_row` (`:509-525`) **already** wraps it in try/except → degrades to `manifest_uninspectable` + visible stop (coarse: lumps "old-but-honest" with "corrupt"). |
| `orca-harness/source_capture/writer.py` | Stamps `manifest_version` + `obligation_contract_version` (`:134-135`); model construction (`:132`) = the write-time strict gate. Hard-codes `hash_basis="raw_stored_bytes"` (`:266-267`). |
| R2 implementation adversarial review | R2-01/R2-02: all three on-disk packets fail current schema (`hash_basis` absent; two carry off-vocab `known cutoff_posture`). Stored bytes match recorded `sha256` (NF-04) — the packets are **honest under v0**, not corrupt. |
| `…/source_capture_packet_fixture_admission_criteria_v0.md` | **AC-10** (named downstream consumer) blocks **all four** units; Open Question: the higher-leverage move may be deciding *whether Source Capture output is consumed at all*. |
| obligation contract / data-and-cleaning boundary | R2 closure scoped the three v0 packets out as frozen evidence; reserved ECR / Capture→Cleaning handoff boundary; ECR field architecture explicitly deferred. |
| 3 v0 packets under `orca-harness/reports/source_capture/slot3_reddit_batch1_*/manifest.json` | Declare `manifest_version: …_v0`; scratch dry-run evidence; **no live consumer**. (`dry_run` fails on `hash_basis` only; the other two also on `cutoff_posture`.) |

Dirty-state boundary: the worktree is broadly dirty and several controlling
overlay sources are modified/untracked. Per `prompt-orchestration` gate 1, this
blocks strict readiness/acceptance/validation/`PASS` claims. This artifact makes
none — it is an advisory planning recommendation only.

---

# Human Summary

**Decision.** Reframe "where does strict validation belong" away from a single
A/B/C pick. The honest target is a **decomposition + hybrid**: strict
current-schema validation **stays at write** (already true — `writer.py:132`);
**read-back-for-inspection becomes lenient and honest** (parse + report
conformance, never crash); strict current-schema validation is **reserved at a
deferred admission/consume gate**; and `manifest_version` is made **read-time
load-bearing as a reported, cross-checked signal** (version-*aware*), while full
version-*dispatch* to per-version schemas and any upgrade/reject machinery are
**deferred** until a real off-version consumer exists. Option **A (validate
current on every read) is rejected** because `extra="forbid"` makes it strictly
worse as the schema evolves.

**Target Architecture (one line).** Two readers, two purposes, never
cross-wired: *inspection reads leniently-and-honestly; admission/consume reads
strictly-and-refuses* — over a write-once, hash-pinned, bump-on-breaking-change
packet corpus, with per-version models / adapters / dispatch reserved as
satellite.

**Why This Wins.** It kills the only live defect (an inspection tool crashing on
structurally-honest, validly-versioned historical evidence) with a one-site,
no-mutation change; it preserves the write-once/hash-pin invariant *by
construction*; it is delta-robust across both add-required and remove-field
futures (the `extra="forbid"` bidirectional landmine); it defers exactly what
AC-10 says must be deferred (a strict gate has no consumer to serve yet) without
pretending it is done; and it converts `manifest_version` from
stamped-but-ignored into a latent integrity signal.

**Core / Satellite Boundary.**
- **Core (recommend now, owner-gated):** (1) standing invariants — write-once +
  hash-pin (already binding) and **bump-on-breaking-change** of
  `SOURCE_CAPTURE_MANIFEST_VERSION`; (2) lenient + honest read-back for
  inspection at `source_quality.py:99`, returning a conformance report typed so
  no caller can mistake it for a validated packet; (3) the rule that the *only*
  place a packet must satisfy the current strict schema is write (today) and a
  future admission/consume gate.
- **Satellite (defer; build only at trigger):** per-version frozen models, a
  version→schema registry, upgrade-on-load adapter chains, version *dispatch*,
  and the strict admission/consume gate itself.

**Deferred Implementation Implications.** When a consumer is named: decide the
admission/consume gate's strict semantics (current-schema-required vs
accept-at-declared-version-with-translation) and whether old packets are
replayed / accepted / refused; if (and only if) that consumer must read an
off-version packet whose lenient report is insufficient, decide reject (default)
vs upgrade (exception, lossless/derivable deltas only — R2 is not one).

**What We Are Not Doing.** No in-place packet mutation (rejected — breaks
evidence integrity); no `hash_basis` backfill (would manufacture provenance); no
upgrade-on-load by default; no semver; no version/compat registry yet; not
reopening R2; not unfreezing JSG-01; not closing `access_posture` (Ob.11); not
deciding the fixture-admission frontier; not authorizing any build.

**Boundary.** Advisory planning only; not validation, readiness, ratification,
acceptance, or build authorization. Build authorization, the admission/consume
gate, and AC-10 resolution are owner-reserved / separate-lane.

**Next.** Owner decision: (a) adopt / amend / reject this target architecture,
and (b) optionally authorize the **lenient-read slice** as a bounded
implementation unit (it has *no* AC-10 dependency and is pure correctness). Only
on owner acceptance does an implementation-scoping lane open — for the lenient
slice **only**.

---

# The Three Coupled Questions (commission core)

## Q1 — Validation-placement model

Not a clean A/B/C choice; the source forces a decomposition. Restating the
prompt's options and the verdict on each:

- **(A) Strict current-schema validation on every read-back** *(current
  behavior, `source_quality.py:99`)* — **REJECT.** Under `extra="forbid"`
  (`case_models.py:11`) every-read-strict gets *worse* as the schema evolves: a
  future **removed** field makes an old, once-valid packet fail because the
  surviving key is now forbidden — the same hard failure as a new **required**
  field. Every-read-strict also conflates "older version" with "actually
  broken" and crashes on packets whose bytes are provably honest (review NF-04).
- **(B) Strict validation at an admission/consume gate + lenient
  read-back-for-inspection** — **ADOPT, split by buildability.** The *lenient
  read* half is buildable now and is pure correctness. The *strict
  admission/consume gate* half is **reserved/deferred**: AC-10 says there is no
  named consumer, so a strict gate would guard an empty room. Critical honesty
  correction (SA-2): strict validation does **not "move"** today — it **stays at
  write** (`writer.py:132`); read goes lenient; the admission gate is a reserved
  *slot*, not a relocation. Treating it as a relocation would be "a regression
  dressed as architecture" (relaxed read + a gate that never fires).
- **(C) Version-aware read (validate against the declared `manifest_version`'s
  schema)** — **ADOPT IN LIMITED FORM (reporting), DEFER FULL DISPATCH.** Make
  the read *version-aware* by reading + cross-checking + reporting the declared
  version (the field is currently stamped but never read). Do **not** build
  version *dispatch* to per-version schemas yet: there is only one current
  schema (v1) and no frozen v0 model to dispatch *to*, and no off-version
  consumer that cares which schema ran.

**Net Q1 answer:** **B (lenient read + reserved strict admission gate) +
C-as-reporting**, with A rejected. The reject-vs-lenient tension between the
candidate lanes dissolves once read is split by purpose: **inspection reads
leniently-and-honestly; the (deferred) admission/consume gate reads
strictly-and-refuses.** Two readers, two purposes, never cross-wired.

## Q2 — Version-evolution mechanism

- **Versioning scheme:** keep the opaque `_vN` string; **make it checked at
  read** (the core fix — it is honest and monotonic-breaking today: v0→v1 was a
  breaking bump). **Do not adopt semver** (false precision for a schema whose
  every change so far is breaking; there is no minor/patch notion).
- **Off-version mechanism:** **clear-reject-with-message is the default at the
  strict gate; lenient-conformance-report at inspection; upgrade-on-load is
  deferred and is the exception, never the default.** Upgrade re-introduces
  mutation-by-proxy (a maintenance-bearing in-memory rewrite) and is
  *information-impossible* for R2 specifically — a v0→v1 upgrade would have to
  invent `hash_basis` and lossily rewrite an off-vocab `cutoff_posture`
  narrative, manufacturing capture facts against the obligation contract's
  no-silent-omission rule.
- **Registry / per-version models:** **not warranted yet.** Reserve frozen
  per-version models *only* if upgrade is ever needed — and even then, parse old
  bytes with a **frozen historical model**, never by loosening the current model
  to swallow old keys (that would silently re-open `extra="forbid"` and defeat
  R2's tightening).
- **Standing discipline (free, adopt as doctrine when owner accepts):**
  **bump-on-breaking-change** of `SOURCE_CAPTURE_MANIFEST_VERSION` on any
  required-add / vocab-narrow / field-remove. R2 already complied; this costs
  ~nothing and is what keeps every future option open.

## Q3 — Build trigger (owner-reserved — recommend, do not authorize)

Two-phase, split exactly on the AC-10 boundary:

- **Phase 1 — lenient read-back slice:** eligible **now**, on owner go only. No
  AC-10 dependency; pure correctness; one production site
  (`source_quality.py:99`) plus enriching the existing census degradation;
  mutates no packets; the three existing v0 packets become the ready-made
  regression corpus.
- **Phase 2 — strict admission/consume gate (+ any version dispatch /
  translation):** trigger = **AC-10 resolution — the first named downstream
  consumer of Source Capture output.** Build the off-version **upgrade/reject
  machinery** only when that consumer must read a packet whose declared version
  ≠ current **and** the lenient conformance report is insufficient for its need.

**What must NOT trigger the satellite:** the mere continued *existence* of the
three frozen v0 packets (scoped out, no consumer). The deeper owner question the
admission doc already surfaces gates everything strict: *will Source Capture
output be consumed at all?* Until that resolves, only Phase 1 is justified.

---

# Agent Detail

**Profile / Evidence Mode / Source Mode.** `workflow-architecture-planning`
**standard** profile (architecture decision shapes later work). Evidence mode:
three delegated lane subagents (explicitly authorized by the prompt). Source
mode: full repo read access; anchor hash pinned and confirmed four times (this
lane + SA-1/SA-2/SA-3 independently).

**Subagents launched: 3 (general-purpose).** Delegation runtime:
inherited/default agent type and model. Each ran its own source-readiness gate,
confirmed the anchor hash, did source-backed option work, and returned
advisory-only (non-verdict) input. Synthesis and the routing object are owned by
this lane; agreement between lanes is **not** treated as proof.

- **SA-1 — version-aware-read architect:** recommended a single current model +
  shared read-only loader treating `manifest_version` as authoritative dispatch
  input, with **clear-reject** as the off-version default; defer frozen
  per-version models and adapter chains.
- **SA-2 — validation-at-admission architect:** showed strict validation should
  **stay at write**, read should go **lenient + three-state honest**
  (`conforms_current` / `conforms_declared_not_current` / `nonconforming`), and
  the strict admission/consume gate is necessarily **AC-10-deferred**.
- **SA-3 — adversary / integrator:** attacked both, endorsed the hybrid with
  sharpenings (below), and proposed the smallest-complete synthesis adopted
  here.

## Candidate models developed (cited to source)

### Model A — Version-aware read
Read-back dispatches on `manifest_version` and validates against the declared
version's schema. Two sub-shapes with opposite cost curves: **A-reject**
(dispatch; off-version ⇒ clear message; O(1) forever) and **A-upgrade**
(dispatch; off-version ⇒ in-memory adapter chain to current; O(N) adapters,
each a place evidence semantics can be silently rewritten). Write-once held *iff*
the loader is read-only and upgrades stay in-memory (never re-serialized).
**Pros:** makes `manifest_version` load-bearing; clear fail-safe behavior;
delta-robust under add *and* remove (reject is symmetric). **Cons:** A-upgrade is
mutation-by-proxy and rots (old-packet adapters get no test pressure); dispatch
is speculative while there is one schema and no off-version consumer.

### Model B — Validation-at-admission + lenient read
Strict current-schema validation fires at write (kept) and at a reserved
admission/consume gate; read-back-for-inspection becomes lenient (parse + report
conformance, never crash). Lenient read returns a conformance report
(`{declared_manifest_version, conforms_to_current, missing_required, off_vocab,
extra_keys, claim_shape_mismatch}` + best-effort projected view in the project's
own `VisibleFact` idiom), **typed so it can never be mistaken for a validated
`SourceCapturePacket`.** **Pros:** smallest correct change now; reuses the
existing census degradation pattern (`source_quality.py:509-525`); read cost
becomes version-count-independent; write-once held by construction (read is
read-only; no `hash_basis` invention). **Cons:** the strict gate is *not
delivered* today (AC-10) — only the lenient half is real now; risk that the
reserved gate rots if its trigger is not tied hard to AC-10.

### Recommended model — the sharpened hybrid (B + C-as-reporting)
Lenient + honest version-*aware* read for inspection (parse, cross-check the
declared version against shape, report; **do not crash, do not dispatch, do not
upgrade**) **+** strict current-schema validation at write (kept) and a
**reserved** admission/consume gate **+** bump-on-breaking-change discipline **+**
write-once/hash-pin invariant, with per-version models / dispatch / upgrade-reject
machinery **deferred** until a real off-version consumer exists.

## Adversarial findings (SA-3, on the merits)

- **Mutation-by-proxy (vs A-upgrade):** upgrade-on-load becomes a hidden rewrite
  the moment a delta is not a pure structural rename — i.e., adds a
  non-derivable required field or narrows a vocabulary with no faithful image.
  **R2 is both at once**, so for R2 upgrade is a semantic rewrite, not a
  migration. Verdict: never make upgrade the default.
- **Malformed-downstream (vs naive B):** "never crash" is a fake-success path
  *iff* the lenient reader returns a `SourceCapturePacket`-typed object (or a
  dict) that a caller treats as valid. Concrete seam: `source_quality.py`
  helpers (e.g. `_first_non_metadata_file` indexing `preserved_by_id[file_id]`,
  `:342`) assume invariants the strict `model_validate` currently guarantees
  (`:202-219`). **Guard (hard design rule):** the lenient reader must return a
  *different type* (a conformance report) for any non-conforming packet, forcing
  every call site to branch; the admission/consume gate must use the **strict**
  path, never the lenient one.
- **Write-once / hash-pin:** held substantively in the hybrid (read-only;
  reports about bytes, never replacements). Residual hazard is **status
  laundering** — a conformance report cited as if it were validation; fence it
  the way the admission doc's G-1 fences the source-quality token ("token is not
  admissibility").
- **Delta-robustness / bidirectional skew:** under `extra="forbid"`, a future
  **removed** field breaks old packets as hard as a new **required** field
  (a surviving key becomes forbidden). A-reject and lenient-report are
  direction-agnostic and flat-cost; A-upgrade must handle *both* directions
  (inject-missing **and** strip-removed), doubling adapter surface as N grows.
- **Version-string honesty (the sharpest, and new):** `manifest_version` is an
  unchecked free `str`, so a packet can **claim** a version it does not conform
  to. "Validate against what it claims" is therefore **not** safe on its own.
  The unchecked field is a latent **integrity** signal: a claim/shape mismatch
  is a *corruption* signal (someone touched a write-once packet), distinct from
  an *off-version* signal. The read must report `claim_shape_mismatch`
  separately. Invariant: **version selects (or, today, *reports*) the schema; the
  schema still judges the content — the string is never trusted alone.**

## Architecture Option Comparison

| Axis | A: every-read strict (current) | A-upgrade (version dispatch + adapters) | B/hybrid: lenient honest read + reserved strict gate (RECOMMENDED) |
| --- | --- | --- | --- |
| Live defect (crash on honest v0) | Fails (crashes) | Fixed (but heavy) | Fixed (one site, light) |
| Cost as N versions grows | Worsens (forbid + skew) | O(N) adapters, rot-prone | Flat (version-agnostic read) |
| Write-once / hash-pin | Held | Held only if never re-serialized; semantic-rewrite risk | Held by construction |
| `hash_basis` honesty | n/a | Must invent it (dishonest) | Reports absence (honest) |
| AC-10 dependency | none | none | Lenient half none; strict gate deferred to AC-10 |
| Version-string honesty | ignores field | trusts claim (unsafe) | reports + cross-checks (safe) |
| Maintenance surface | low but fragile | high | low + small loader/report |
| Fake-success risk | low (loud crash) | high (laundered upgrade) | low *iff* report is un-mistakable-for-valid |

## Architecture Result — `TARGET_RECOMMENDED`

Minimum selection threshold met: stable invariant clear (write-once + hash-pin +
bump-on-breaking-change + strict-stays-at-write); core/satellite split clear
enough to prevent boundary leakage; non-goals known; no unresolved *upstream*
blocker can materially change the *recommended core* (AC-10 gates the *deferred
satellite*, not the lenient-read core). The **build** is owner-gated and most of
the mechanism is intentionally deferred — deferral is part of the selected
architecture, not a non-selection.

## Target Architecture Detail (design altitude — no code)

- **Where validation fires:** **write** (`writer.py:132`, kept strict) and a
  **reserved** admission/consume gate (deferred, strict, AC-10-triggered).
  Inspection read-back does **not** re-run the write gate.
- **How a read encounters an off-version packet:** the inspection reader parses
  permissively (not `try/except` around the strict model — a genuinely
  non-strict parse, e.g. raw-dict diff or `model_construct`-style, so
  `extra="forbid"` skew is *reported*, not *raised*), reads `manifest_version`,
  cross-checks declared-version against shape, and returns a conformance report
  with a best-effort projected view. It never crashes, never upgrades, never
  returns a strict-model instance for a non-conforming packet. The admission/
  consume gate (when built) uses the strict path and **refuses** (reject /
  replay), never lenient.
- **Versioning scheme:** opaque `_vN` string, made read-checked;
  bump-on-breaking-change; no semver; no write-version/read-compat split yet.
- **Registry needed yet?** No. One current schema; no frozen per-version models;
  reserve them (and dispatch/adapters) for a future off-version consumer only.

## Delta-Robustness (reasoned across ≥ two future breaking versions)

- **v0→v1 (real):** add required `hash_basis` + narrow `cutoff_posture`. v0 fails
  current two ways. Hybrid: lenient read **reports** non-conformance + projected
  view; no crash, no invented fields.
- **v1→v2 add-required (e.g. `acquisition_receipt_id`):** same shape; lenient
  read reports; a *non-derivable* added-required field makes upgrade
  information-impossible ⇒ reject is the only honest gate behavior.
- **v1→v2 remove-field (the `extra="forbid"` landmine):** a v1 packet fed to a v2
  strict model fails on the *surviving, now-forbidden* key. Hybrid lenient read
  is unaffected (diff, don't validate-strict); if upgrade is ever needed, parse
  with a **frozen v1 model** then drop the field via adapter — never loosen the
  current model.

## Write-once / hash-pin invariant — holds under the recommended model

By construction: the inspection reader is read-only — it never writes
`manifest.json`, never re-serializes, never touches `raw/`; the only manifest
writer is `writer.py` at capture time. No persisted packet is mutated to fit a
new schema (the rejected "in-place migration"). `hash_basis` is never
synthesized onto disk; absence is reported. Any future need to make an old
packet current is satisfied by **replay into a new packet** (new `packet_id`,
new hash, honest `hash_basis`), never by mutating the pinned original.
**Falsifiable build guard (for the eventual implementation lane):** snapshot the
manifest bytes + every preserved-file `sha256` before and after a load and assert
identical — so write-once is *proven*, not asserted.

## Bloat-Cut Queue (what to NOT build now)

- Version→schema **registry** and frozen per-version model classes.
- Upgrade-on-load **adapter chains** and any version *dispatch*.
- The strict **admission/consume gate** (no consumer — AC-10).
- semver / write-version + read-compat-range machinery.
- Any migration/replay of the three frozen v0 packets (scoped out, no consumer).

## Blockers / Not-Proven Boundaries

- Dirty worktree (incl. controlling overlay sources) ⇒ no strict
  readiness/acceptance/validation/`PASS` claims; this is advisory planning only.
- AC-10 unresolved (no named consumer) ⇒ the strict admission/consume gate and
  any version-translation cannot be specified beyond "strict, current-schema,
  refuse-or-replay"; they must be co-designed with the ECR when AC-10 resolves.
- "Full suite green" from the R2 closure is taken as reported, not re-verified
  here (no tests run in this planning pass).
- Single production read-back (`source_quality.py:99`) verified by repo search
  within `orca-harness`; readers outside `orca-harness` were not enumerated
  (does not change the recommendation, but would enlarge the lenient-read call
  surface and the negative-fixture set).

## What Would Change The Recommendation

- A named downstream consumer appears (AC-10 resolves) → Phase 2 activates;
  decide the admission/consume gate's strict semantics and old-packet
  disposition.
- A second breaking bump (v1→v2) is proposed → at least the version-reporting
  read and bump discipline must exist before it lands; revisit whether frozen
  per-version models are now warranted.
- Evidence that an off-version packet's *content* (not just non-crash) must be
  consumed → reconsider upgrade-on-load for that *specific* lossless/derivable
  delta only.

---

# Quality Gates (self-check — these can fail)

- **Each model developed against current schema + read-back call sites, cited:**
  PASS (models.py / source_quality.py / writer.py + docs cited with `file:line`).
- **Write-once/hash-pin shown to hold under each model (no in-place mutation):**
  PASS (read-only inspection; replay-not-mutate; no `hash_basis` backfill;
  falsifiable guard named).
- **R2 not reopened; JSG-01 not unfrozen; `access_posture` not closed;
  fixture-admission coordinated-with not decided:** PASS (all explicitly held;
  AC-10 treated as the separate lane's gate).
- **A build trigger is named (not silently "build now" or "never"):** PASS
  (two-phase, AC-10-split, owner-reserved).
- **Delta-robustness across ≥ two future breaking versions reasoned:** PASS
  (v0→v1, v1→v2 add, v1→v2 remove under `extra="forbid"`).

# Smallest Complete Next Routing Object

An **owner decision** (not an artifact-by-default): adopt / amend / reject this
target architecture, and decide whether to authorize the **lenient-read slice**
as a bounded implementation unit. *On owner acceptance only*, the next object is
an implementation-scoping lane for the **lenient-read slice only** — touch point
`source_quality.py:99` (+ a shared parse helper); behavior contract =
"parse-and-report, never crash, output un-mistakable-for-validated, consistent
with the existing census degradation at `:509-525`, no `hash_basis` invention,
the three v0 packets stay byte-frozen"; explicit non-goals = no schema dispatch,
no upgrade adapters, no admission gate, no packet mutation; validation
expectation = the three on-disk v0 packets become inspectable-with-visible-
non-conformance and a v1 packet still reports conforming. Everything else stays a
*named deferred* with its AC-10 trigger attached, not a step.

# Owner-Reserved / Separate-Lane Note

- **Build authorization** for either phase is **owner-reserved** (this lane
  recommends a trigger; it does not authorize a build).
- The **fixture-admission frontier** (AC-10) is its **own lane**; this routing
  object coordinates with it and does **not** decide or absorb it.
- The **ECR / consume gate** field architecture is reserved by the
  data-and-cleaning boundary and is out of scope here.

# Doctrine Propagation

This artifact asserts **no binding rule** (it is a non-binding architecture
*recommendation*), so it carries **no** `direction_change_propagation` receipt —
mirroring the fixture-admission-criteria proposal's treatment. If the owner
**adopts** this target architecture as durable doctrine, or **authorizes the
build**, that acceptance is the doctrine-changing / `lifecycle_boundary` step and
must carry a `direction_change_propagation` receipt per
`.agents/workflow-overlay/source-of-truth.md` at that point (likely surfaces to
check: the obligation contract's versioning language,
`.agents/workflow-overlay/source-loading.md` read packs, and the repo map).

# Non-Claims

Architecture-planning / design only. Not implementation, not validation, not
ratification, not acceptance, not a build authorization, not an R2 reopen, not a
JSG-01 unfreeze, not an `access_posture` closure, not the fixture-admission
decision, not ECR/Cleaning/Judgment design, not buyer proof, not
source-of-truth promotion. The current state described here is a design basis,
not a commitment to keep it.

---

# Adjudication & Amendment (2026-06-05)

Adjudicated by the capture-build lane under explicit owner delegation ("your call and
adjudication holds authority"), consuming the **independent cross-family** adversarial
review (Codex / GPT-5) at
`docs/review-outputs/adversarial-artifact-reviews/source_capture_packet_schema_evolution_architecture_adversarial_artifact_review_v0.md`
(recommendation `sound_with_friction`). This routing object was reviewed as **v0 @ SHA256
`8FDD1FDA…E7E9`**; that review report is frozen and its `file:line` citations refer to the
pre-amendment body above (unchanged except the Status token on line 41).

**Adjudication: ADOPT the target architecture as the recommended direction, with both
findings carried.** The central decision is sound and independently confirmed: strict
every-read is the wrong long-term model under `extra="forbid"`; new-write strictness is
centralized at `writer.py:132`; the single production read-back at `source_quality.py:99`
holds under whole-repo search; AC-10 correctly gates the admission/consume **satellite**,
not the inspection-read fix. The six non-findings stand.

**AR-01 (major) — carried as a BINDING amendment to Phase 1.** The Phase-1 lenient read may
report only what is knowable **without** the deferred per-version machinery: the declared
version *as a fact*, and **current-schema** conformance. It must **not** promise general
declared-version *shape* validation — there is no frozen v0 model to validate a v0-declaring
packet against (`manifest_version` is an unchecked `str`; `models.py:162`). The
`claim_shape_mismatch` field as written overpromises and is **superseded**, for any
implementation-scoping lane, by this honest field set:
- `declared_manifest_version`
- `declares_current_manifest_version`
- `conforms_to_current_schema`
- `current_schema_errors`
- `declared_version_shape_validation: not_available_without_per_version_schema` (for any non-current declared version)

The "claim vs shape" integrity signal survives **only** in its bounded current-version form —
"declares the current version **but fails the current shape**" (a corruption signal). General
cross-version shape validation is a **deferred-satellite** capability (it needs the per-version
frozen models this object defers). The body invariant ("today, *reports* the schema; the string
is never trusted alone") governs; the Model-B / Phase-1 field list is read subject to this
amendment.

**AR-02 (minor) — carried as wording hygiene.** Separate the **already-binding** invariants
(write-once + hash-pin — evidence integrity, in force now) from the **proposed** discipline
(`bump-on-breaking-change` of `SOURCE_CAPTURE_MANIFEST_VERSION`). The latter is a *recommended*
rule, not yet binding doctrine; it becomes durable doctrine **only** on explicit owner adoption,
which — like build authorization — is a `lifecycle_boundary` / doctrine step that **must carry a
`direction_change_propagation` receipt** per `.agents/workflow-overlay/source-of-truth.md` (the
Doctrine Propagation section above already names the surfaces). R2's v0→v1 bump complied with the
discipline as a one-off; that compliance is not itself adoption of the rule.

**Boundaries held (what this adjudication does NOT do):**
- It does **not** authorize any **build.** Both phases stay owner-reserved. The Phase-1
  lenient-read slice is the recommended next unit but needs an explicit owner build-go before an
  implementation-scoping lane opens.
- It adopts a **direction**, asserts no binding rule, and changes no code/schema/contract — so it
  carries **no DCP receipt** itself. The receipt attaches at owner doctrine-adoption / build
  authorization.
- It does **not** reopen R2, unfreeze JSG-01, close `access_posture`, or decide the AC-10
  fixture-admission frontier.

**Owner's next discrete decisions (not exercised here):** (1) authorize the Phase-1 lenient-read
slice as a bounded implementation unit → opens an implementation-scoping lane for that slice only,
carrying the AR-01 amendment; (2) optionally adopt `bump-on-breaking-change` as durable doctrine →
DCP receipt.
