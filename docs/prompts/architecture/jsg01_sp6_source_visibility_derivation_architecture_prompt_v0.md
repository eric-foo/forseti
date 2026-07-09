# JSG-01 SP-6 Source-Visibility Derivation — Architecture Planning Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: >
  Thin architecture-planning prompt for the JSG-01 SP-6 (source_visibility_posture)
  derivation: the ownership-boundary decision (JSG-01-interim vs future-ECR-owned)
  and the derivation-rule shape, designed against a frozen capture contract.
  Non-executing; uses 3 subagents for option development + synthesis.
use_when:
  - Running or dispatching the SP-6 derivation architecture decision.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/source_side_receipts/jsg01_source_side_receipt_translator_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
input_hashes:
  docs/product/jsg01_source_side_receipt_translator_v0.md: E8944D13FF8B3FAF62AC24209EC50FDA7C03CC9D4F906687246B2E15C01592B2
branch_or_commit: main @ f9b05e6 (worktree dirty; controlling sources untracked)
```

## Commission

Make the **thin architecture decision** for SP-6 (`source_visibility_posture`):

1. **Ownership boundary** — where the SP-6 derivation lives: **(A)** a JSG-01-side
   *interim* reader rule, or **(B)** a *future-ECR-owned* rule that begins defining
   the ECR receipt.
2. **Derivation-rule shape** — the decision-table that maps the frozen-contract
   inputs → SP-6's closed values + the `access_posture` free-text **residual**.
3. **SP-2 verifiability check shape** — against the recomputation-bound `hash_basis`.

Output is a **non-executing architecture routing object**: both options developed,
adversarial findings, a recommendation with decisive criteria, the rule shape at
design altitude, deferred implications, and the smallest complete next step.

## Authorization / boundary (read first)

- **Design-only, NON-EXECUTING.** No source, schema, code, or contract changes.
- **JSG-01 stays FROZEN.** Do not bind, unfreeze, or treat postures as enforced.
- **The A/B call is OWNER-RESERVED where it touches the deferred ECR consolidation.**
  Option B *starts defining the ECR receipt*, which the owner has reserved. The
  lane develops and recommends; it must **not** select Option B or enter the ECR
  consolidation without explicit owner authorization.
- **Consume-not-design** the new capture-context field (its name/shape is
  capture-lane-owned).
- SP-6 records the **value** only — the sufficiency grade and the finalization
  authority stay **owner residuals**; "material" divergence (corroborated vs
  diverged) is a **downstream Judgment** call, not a captured value.
- Build against the **frozen contract** below; treat it stable until the
  capture-build lane re-couriers a delta. Flag the parts most sensitive to a delta.
- No `jb` import; `agent-workflow` is reusable mechanics only.

## Preflight (orca_start_preflight)

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: docs-write   # the architecture PLAN only; read-only for all source/code
  target_scope: [the SP-6 architecture plan artifact under docs/ or chat]
  dirty_state_checked: required_yes
  blocked_if_missing: yes
external_source_boundary: agent-workflow reusable mechanics only; jb is NOT Orca authority.
```

## Source pack / required reads

- **SP-6 definition + AR-01:** `docs/product/jsg01_source_side_receipt_translator_v0.md` (SHA256 `E8944D13…92B2`) — SP-6 closed values, the composite-derivation note, the AR-01 "still needs derivation" residual.
- **AR-01 source:** `docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md`.
- **Input vocabularies:** `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` Ob.9/Ob.10/Ob.11/Ob.15.
- **Layering + reserved ECR:** `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`.
- **The frozen contract** (embedded below — design basis, not landed/enforced).

## FROZEN CONTRACT (embedded — couriered from the capture-build lane; design basis only)

```text
- cutoff_posture (Ob.9): known value in {pre_cutoff, post_cutoff, mixed, unknown}; carries ONLY cutoff posture (overloaded capture-context moved OUT).
- archive_history_posture (Ob.10): AR-05 union — known/archived, known/attempt_failed, not_attempted/<reason>, not_applicable/<reason>.
- re_capture_relationship (Ob.15): known value in {supersede, supplement, conflict, mixed}.
- NEW dedicated capture-context field (migration Option B): the formerly-overloaded capture-context strings live HERE; consume it, do not design it (name/shape capture-lane-owned).
- hash_basis: recomputation-bound — identifies what bytes/coverage the sha256 covers (relative_packet_path + slice/encoding) or an owner-bound acquisition receipt.
- UNCHANGED: access_posture stays free-text (Ob.11). SP-6 derivation still needs its own rule/residual (multi-field map over archive-attempt + acquisition-receipt scope + re_capture, with access_posture free-text). R2 does NOT produce SP-6 (AR-01).
- Treat as stable until re-couriered; enforcement is NOT real until "landed + cross-family reviewed".
```

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, prompt-orchestration, source-of-truth).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-architecture-planning`. Do **not** APPLY yet.
3. `SOURCE-LOAD` the pack + frozen contract.
4. Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE`.
5. APPLY deep-thinking to frame failure modes, then architecture-planning to compare options and name the routing object.

## Subagents — 3 standard (general-purpose), explicitly authorized

Each subagent receives this source pack + the embedded frozen contract (or runs
its own source-readiness gate), does **source-backed** option work, applies no
method before `SOURCE_CONTEXT_READY`, and discloses its approach. Subagents are
advisory; the architecture lane synthesizes and owns the routing object.

- **SA-1 — Option A architect (JSG-01-interim reader rule):** develop SP-6 as a JSG-01-side interim derivation — the decision-table rule, the `access_posture` residual, where it sits, migrate-to-ECR-later implications, pros/cons.
- **SA-2 — Option B architect (future-ECR-owned rule):** develop SP-6 as an ECR-owned derivation — how it begins defining the ECR receipt, the boundary with the reserved consolidation, what owner authorization it requires, pros/cons.
- **SA-3 — Adversary / integrator:** attack both — layer-boundary leakage, mishandled `access_posture` free-text residual, robustness to a re-couriered contract delta, whether the rule is truly mechanical (no hidden judgment), and any accidental entry into the reserved ECR consolidation. Propose the smallest-complete synthesis + the next routing object.

The lane then synthesizes SA-1..SA-3 into the recommendation. The A/B ownership
decision (especially B) is **surfaced for the owner, not decided by the lane.**

## Output (non-executing architecture routing object)

- Option A and Option B, each developed (where SP-6 lives; derivation-rule shape; residual handling; pros/cons).
- Adversarial findings on both.
- Recommendation with decisive criteria (author's prior: A-interim — but the lane judges and may differ).
- The SP-6 **derivation-rule shape**: a decision table — every input combination over `{archive_history_posture, re_capture_relationship, acquisition-receipt capture scope, the new capture-context field, access_posture}` → exactly one SP-6 value `{archive_corroborated, archive_only, archive_diverged, current_capture_only, archive_post_cutoff_only, attempt_failed, not_attempted, not_applicable}` **or** a named residual.
- The SP-2 verifiability check shape against `hash_basis`.
- Deferred implications + the **smallest complete next routing object**.
- Explicit note: A/B ownership (and any ECR-consolidation entry) is owner-reserved.

Output mode: `file-write` the plan to `docs/` (or `chat-only`). **No** source, code,
schema, or contract change. Do not execute implementation.

## Quality gates (must be able to fail)

- Both options developed against the frozen contract with cited inputs.
- The derivation rule is **mechanical**: every input combination resolves to exactly one SP-6 value or a named residual; no hidden judgment, no `access_posture` force-mapping.
- JSG-01 not unfrozen; ECR consolidation not entered; sufficiency grade + finalization left as owner residuals; materiality left downstream.
- Delta-robustness: sensitivity to a re-couriered contract delta (esp. the new capture-context field's shape) is named.

## Non-claims

Architecture-planning / design only. Not implementation, not validation, not
ratification, not JSG-01 unfreeze, not the ECR consolidation, not the
sufficiency threshold or finalization authority. The frozen contract is a design
basis, not landed or enforced state.
```
