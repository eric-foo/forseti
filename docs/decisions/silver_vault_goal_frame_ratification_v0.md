# Silver/Vault Goal Frame — Owner Ratification (v0)

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record (docs/decisions/; owner ratification of the silver/vault lane goal frame)
scope: >
  Records the owner's 2026-07-04 ratification of the silver/vault lane's
  proposed goal frame — mission, the five behavioral V-signals, and the unit
  order — as proposed by the parent lane handoff. Quotes the ratified frame
  verbatim so it stands alone; downstream lanes cite this record instead of
  re-asking.
use_when:
  - Resolving the ratification gate in silver/vault unit handoffs (unit (b) onward).
  - Checking what the silver lane's ratified optimization target is.
stale_if:
  - The owner re-frames or supersedes this ratification in a later decision record.
authority_boundary: retrieval_only
```

## Ratification

**Ratified by the owner, 2026-07-04**, in the bronze census closure thread
(same session that observed the bronze exit-0 closure), on the proposal
carried by
`docs/prompts/handoffs/data_lake_silver_vault_lane_handoff_prompt_v0.md` (authored on PR #662, branch `claude/silver-vault-lane-handoff`).
Owner's words: "sure let's ratify it. i dont see anyhting wrong with it."
Ratified as proposed — no re-frame, no re-ordering.

## The ratified frame (verbatim from the proposal)

**Mission:** make Silver the trustworthy READ layer of the lake — every
silver record lineage-anchored and policy-fingerprinted, sibling
supersession EXPLICIT, every silver consumer enumerated and reading through
a defined selection rule, and the vault record shapes schema-versioned —
optimizing for behavioral signals, not artifact existence.

**Behavioral signals (V-signals, ratified as drafts to be met):**

- V1 lineage-closed: every committed silver record resolves to (raw anchor,
  deriving policy fingerprint) — no orphan silver.
- V2 selection-defined: for any (anchor, lane) with N siblings, one defined,
  tested rule names the current record; a policy bump changes what every
  reader sees, atomically per read (kills the F-IGRC-001 class generally).
- V3 consumer-enumerated: a silver census + a silver-reader contract gate
  (mirror of the consumer seam gate) — every reader of silver lanes is
  declared and uses the selection rule, never `lane_dir` free-walks.
- V4 vault-versioned: silver/vault record shapes carry schema version
  tokens (closing the weak-envelope class), pinned in the pin gate.
- V5 second-cycle-zero: silver derivation cadence (the bronze cadence
  runner already proves the deriving half).

**Unit order after the bronze bridge:** (b) silver census gating read —
build-vs-classify ledger to the owner before any code; (c)
supersession/selection design — an owner-steered high-lock-in fork,
explicitly NOT pre-decided by this ratification; (d) vault schema-version
tokens for the weak-envelope record shapes.

## What this ratification does and does not commit

- Commits the lane's optimization target: the mission and V1–V5 above.
- Does NOT choose the V2 mechanism (selection helper vs. append-only
  supersession facts vs. latest-policy-fingerprint convention) — that fork
  stays owner-steered at unit (c), fed by unit (b)'s evidence.
- Does NOT commit a build list — unit (b)'s build-vs-classify ledger decides
  what gets built (the projection-sweep precedent is expected to kill
  builds).

## Non-claims

Ratification of a target, not validation, readiness, design acceptance, or
proof. No V-signal is met by this record's existence.
