# Ontology<->Runtime Drift-Check Contract v0 (W2b leak-surface semantics)

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  The contract pinning the leak-surface semantics of the ontology<->runtime
  drift-check (.agents/hooks/check_ontology_drift.py): which TOP-LEVEL class-local
  serialized surfaces count as a self-identifying (payload-leaking) name, which
  names the not_payload_identifier guard protects, how composed_with classes are
  handled, and the nested-payload scope boundary plus its fail-loud readiness
  probe. Resolves the three semantics #268 surfaced, as corrected by an
  owner-ratified architecture pass and implemented in this PR.
use_when:
  - Modifying or reviewing check_ontology_drift.py's not_payload_identifier leak guard.
  - Adding or changing a runtime_binding in ontology.yaml (what the guard checks).
  - Adjudicating whether a drift-check finding is a real leak or a false positive.
authority_boundary: retrieval_only
open_next:
  - .agents/hooks/check_ontology_drift.py
  - orca/product/spines/foundation/ontology/ontology.yaml
  - docs/decisions/adversarial_review_routing_policy_v0.md
stale_if:
  - A runtime binding introduces a Pydantic discriminated union (the --strict readiness check fires in CI; the top-level scope must be revisited / nested recursion added).
  - Pydantic's serialization semantics for alias / serialization_alias / enum / computed fields change.
  - The leak-surface set or interchangeable-name set in check_ontology_drift.py diverges from this contract.
```

## Status

**Contract + implementation (this PR).** It pins the leak-surface semantics of
the ontology<->runtime drift-check and implements the conforming delta in
`.agents/hooks/check_ontology_drift.py`.

**Architecture pass (2026-06-19, owner-ratified).** v0's "flat bindings + nested
tripwire" framing was wrong and was corrected via a 3-lane
`workflow-architecture-planning` pass (directional / adversarial / grounding),
following a cross-vendor `NEEDS_ARCHITECTURE_PASS` review. Two premises were
**false** (verified against primary source):

- **The 3 runtime classes are NOT flat.** `SourceCapturePacket` has 14 nested
  models, `FacilitatorLedger` 6, `CaseReport` 1; only `EvidenceUnit` is flat. So a
  "tripwire on any nested model" would fire on 3 of 4 classes on day one — broken.
  But all four have **zero discriminated unions and zero computed fields**
  (verified), so the dangerous nested case is *latent*, not present.
- **This gate is `--strict` in CI today** (`.github/workflows/ci.yml`), not
  report-mode. A false positive is a red `main` now, so the delta must be
  **non-regressive** (0 findings on the current clean classes).

The ratified target: **top-level class-local detection, complete for that scope,
with a fail-loud `--strict` readiness check instead of a per-binding tripwire, and
recursion deferred until a real producer appears.** The JSON-schema frame was
considered and **rejected** (see *Rejected frames*).

**Non-claims.** Not validation, readiness, or proof. The 3 bindings pass
`--strict` cleanly; these are robustness semantics, not bug fixes.

## Context

`check_ontology_drift.py` (landed #267, hardened #268) checks the scoped
alignment between the ontology SSOT (`ontology.yaml` `runtime_bindings`) and three
runtime Pydantic classes. The `not_payload_identifier` invariant asserts a
binding's name must **not** appear as a self-identifier in the runtime class's
serialized payload — the condition under which the ID-doctrine "the runtime name
is just a forward-only storage alias of the ontology name" reconciliation is safe.

## Scope (the architecture decision)

The guard inspects each runtime class's **own top-level serialized surfaces**
(its fields, its computed fields, their aliases, and the discriminator values in
their annotations) — **not the full nested payload graph.** A name nested inside a
*member* model's payload (e.g. a discriminated-union tag) is **out of scope**, and
that boundary is held honest by a readiness probe (A4), not silently. Rationale:
nested models are normal and present today, but there are **no discriminated
unions or computed fields anywhere in the bound classes**, so the only way a
nested self-identifier could arise is a future change — which the probe catches.

## The contract (leak-surface set)

A name `N` is a **payload-leaking self-identifier surface** on a runtime class
`C` iff `N`, compared case-insensitively, equals any of `C`'s **top-level
serialized surfaces**:

1. a **field name** (`model_fields`) or a **computed-field name**
   (`model_computed_fields`);
2. a serialized **discriminator value** reachable in a (computed-)field's
   annotation: a `Literal` string value (recursing `Optional`/`Union`/
   `Annotated`), **and** — when the annotation is or nests an `Enum` subclass —
   that enum's members' string `.value`s (covers both `Literal[Enum.X]` and a
   plain `field: SomeEnum`, which serializes its member value);
3. a field's or computed-field's **`alias`** or **`serialization_alias`**
   (`alias_generator`-derived aliases are included — Pydantic writes them onto
   `FieldInfo`). **Not** `validation_alias` (input-side; R1).

**Conservative-proxy semantics (A3).** The guard flags any *appearance* of an
interchangeable name in the top-level serialized surfaces. It is a
**flag-to-investigate, not a proof of a type discriminator**: it over-fires by
design so a real self-identifying leak cannot pass silently. A fire means
"reconcile this binding," not "auto-fail."

A binding declaring `not_payload_identifier: true` is **clean** iff none of its
**interchangeable names** — `{ontology concept name, runtime class __name__,
name_alias if present}` — is a leak surface on its runtime class **or** any
`composed_with` class (each composed class scanned against the same **concept**
name set).

## Resolutions

- **R1 — drop `validation_alias`.** It is input-side (proven, Pydantic 2.13:
  a field with `validation_alias="vIN"` shows `vIN` in neither `model_dump()` nor
  `model_dump(by_alias=True)`). Surfaces are field/computed names, discriminator
  values, and `alias`/`serialization_alias`.
- **R2 — check the interchangeable-name SET** `{concept, cls.__name__,
  name_alias?}`, not one name (a concept-name leak disqualifies as much as a
  runtime-name leak).
- **R3 — extend the leak check to `composed_with` classes**, each scanned against
  the **concept's** name set (not the composed class's own name — `CaseReport`
  may legitimately self-identify).

## Architecture-pass decisions

- **A1 — computed fields are a surface** (`model_computed_fields`: name + alias).
  Latent today (0 computed fields) but cheap + top-level.
- **A2 — enum-typed fields are a surface** (their member `.value`s). This is the
  one *live* gap: `SourceCapturePacket.capture_mode` and
  `EvidenceUnit.pre_decision_status` are enum-typed and currently unscanned.
- **A3 — conservative-proxy framing** (above).
- **A4 — nested boundary held by a readiness CHECK, NOT a tripwire.** A
  per-binding "nested model present" tripwire would fire on 3 of 4 classes today.
  Instead, the `--strict` path emits a readiness finding when a bound/composed
  class has a **Pydantic discriminated union** (`FieldInfo.discriminator`) — the
  one nested shape whose serialized tag value the top-level scan cannot see. It is
  **0 today** (non-regressive) and fires in CI the moment one appears, signalling
  "extend the guard with nested recursion." Recursion itself is **deferred** until
  then (building it now = coverage for a zero-instance case). General nested field
  names/values (non-discriminator) stay a **documented** out-of-scope limitation in
  the detector docstring; top-level computed fields are covered by A1. A
  `--selftest` case proves the readiness finding fires on a synthetic discriminated
  union.

## Rejected frames (architecture pass)

- **JSON-schema scan (`model_json_schema()`):** rejected. Under a `--strict` gate
  pinned to a floating `pydantic>=2.13,<3`, it couples a merge-blocker to
  Pydantic's most version-volatile surface; its raise-path has no
  constraint-satisfying default (silent-pass under-fire **or** finding
  false-positive); schema != serialization (metadata `$defs`/`title` false
  positives needing an allowlist that turns the "simple scan" into a schema-dialect
  parser; serializer-injected values invisible).
- **Sample `model_dump(mode=json)`:** rejected — the classes have heavy required
  fields + cross-field validators (fixture-fragile), and a single sample only
  exercises one branch (under-fires).
- **Binding-declared surfaces in `ontology.yaml`:** rejected as primary — a
  hand-listed surface set drifts from the class and cannot catch the *unnoticed*
  drift a CI gate exists for.

## Conformance status (implemented in this PR; non-regressive)

| Surface / check | Before (main) | This PR |
| --- | --- | --- |
| `validation_alias` | included | excluded (R1) |
| computed fields | not inspected | name + alias (A1) |
| enum-typed fields | missed | member `.value`s (A2) |
| names checked | `name_alias` else `cls.__name__` | set `{concept, __name__, name_alias?}` (R2) |
| `composed_with` leak check | import-only | leak-checked vs concept set (R3) |
| nested discriminated-union tag value | silently uncovered | `--strict` readiness finding, 0 today (A4) |
| framing | "type discriminator" | conservative name-collision proxy (A3) |

The delta strengthens the guard, so it is verified **non-regressive**: the 3
bindings stay `--strict`-clean (the new surfaces add no hit on today's classes).
`--selftest` is extended with computed-field, enum-value, concept-name,
`composed_with`, and readiness probes.

## History and governance flags

- v0 reviewed by a cross-vendor controller (`NEEDS_ARCHITECTURE_PASS`); the
  load-bearing findings were independently verified against Pydantic primary
  source; the 3-lane architecture pass set the corrected target (owner-ratified).
- **Flag (not fixed here):** `ontology.yaml`'s `runtime_bindings` comment cites an
  *"MGT name-drift decision 2026-06-19"* that the review could not locate — a
  possible dangling citation to reconcile separately.
- **Corrected:** prior drafts (and the consolidation plan) called this gate
  "report-mode"; it is `--strict` in CI. The frozen-predicate ratchet applies to
  the separate `orca/`-wide report gates, not to this one.
