# Data Capture Spine — Posture Vocabulary Enforcement Execution Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Hands the R2 posture-vocabulary enforcement work-unit to the Data Capture /
  capture-build lane: scope, then (on owner authorization) execute the untangle +
  closure + migration + contract amendment, with that lane's own code/migration
  review and DCP receipt.
use_when:
  - Routing the R2 proposal into Data Capture lane scoping/execution.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca-harness/source_capture/models.py
input_hashes:
  docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md: F873C0EA9B61135971058B517DF0C220569FAFDA032D9407B2073216D8920B27
  docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_posture_vocabulary_enforcement_proposal_adversarial_review_v0.md: 0D5182DE3621A7DB3F92B763E31BC4D62D8893DBFCB66BDB617456524C95F93B
branch_or_commit: main @ f9b05e6 (worktree dirty; controlling sources untracked)
```

## Work unit

`DCS-POSTURE-VOCAB-R2` — enforce the Data Capture Spine's existing closed posture
vocabularies at write-time, after untangling the overloaded `cutoff_posture`
field, and add a recomputation-bound hash basis.

## Objective and intended decision

Make the Data Capture Spine's source-fact postures clean at the source (enforced
once, at write-time) so downstream readers stop re-interpreting free text. The
spec is the patched proposal; the closure conditions are the review's accepted
findings. The receiving lane decides the migration representation and the
`source_quality.py` fix within the bounds below.

## Thread operating target continuity

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: >
    This is the upstream foundation the JSG-01 source-side anchor goal turned out
    to require: JSG-01 cannot honestly bind until the Data Capture postures it
    reads are clean at the source. Orientation only; not authority or readiness.
```

## Authorization gate (read first)

This handoff is **docs preparation**. It does **not** by itself authorize source
changes. Bounded implementation authorization for `DCS-POSTURE-VOCAB-R2` is
granted **only when the owner accepts/dispatches this handoff**. Until then:

- the receiving lane may **scope** (produce a non-executing route, read code) but
  must **not** edit code, schemas, tests, or the obligation contract;
- if dispatched **without** an explicit implementation grant, treat it as
  scoping-only and stop at the authorization gate with the route + open questions.

## Receiving-lane preflight

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom   # see Inputs
  edit_permission: docs-write-until-authorized_then-implementation   # code/contract edits ONLY after owner grant
  target_scope:
    - orca-harness/source_capture/models.py
    - orca-harness/source_capture/source_quality.py
    - orca-harness/source_capture/packet_assembly.py
    - orca-harness/tests/unit/test_source_capture_packet.py
    - orca-harness/tests/unit/test_packet_assembly.py
    - orca-harness/reports/source_capture/**/manifest.json   # existing packets (migration)
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md   # Ob.9/10/15 closure (doctrine)
  dirty_state_checked: required_yes
  blocked_if_missing: yes
doctrine_change: yes — amending the obligation contract (Ob.9/10/15) is doctrine; a direction_change_propagation receipt is REQUIRED at closeout.
external_source_boundary: agent-workflow is read-only reusable mechanics; jb is NOT Orca authority.
```

## Inputs (spec + closure conditions — route, do not restate)

- **Spec:** `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md` (SHA256 `F873C0…0B27`). Use its "Proposed changes", "Implementation impact surface", "Pre-ratification conditions", `hash_basis` contract, and Ob.10 representation as the bounded scope.
- **Closure conditions:** the review report (SHA256 `0D5182…F93B`) findings AR-01..AR-05 — confirm each is satisfied by the executed change.
- **Vocabulary source of truth:** the obligation contract Ob.9/Ob.10/Ob.15. Enforce exactly these; invent no values.

## Required sequence

1. **Implementation-scope** (non-executing): produce the `STEP-*` route — untangle `cutoff_posture` (separate capture-context strings and the `source_quality._source_time` fallback from the real cutoff posture) → migration mapping for the named off-vocabulary existing values/tests → `source_quality.py` fix (source/snapshot time not from the closed enum) → schema enforcement in `models.py` → add the recomputation-bound `hash_basis` → obligation-contract amendment (Ob.9/10/15 closed; pin the Ob.10 status/value representation). Name touch points, stop conditions, and the migration decision options.
2. **Authorization gate** — stop; obtain explicit owner bounded-implementation grant (or proceed if this handoff was dispatched as that grant).
3. **Execute** the bounded change only within `target_scope`.
4. **Code/migration review** — broadened read-pack (the implemented code + tests + existing packet manifests); confirm AR-01..AR-05 closure and that no existing packet/test silently breaks.
5. **DCP receipt** — inline `direction_change_propagation` (trigger `product_doctrine` or `architecture_doctrine`) for the obligation-contract amendment, per `.agents/workflow-overlay/source-of-truth.md`, with downstream-surface checks + stale-language sweep.

## Hard constraints / non-goals

- **Do not close `access_posture`** (Ob.11 prose) — leave free-text, flag for a separate vocabulary decision.
- **No materiality/comparison enums in Capture** (`corroborated`/`diverged` stay downstream Judgment).
- **Do not decide sufficiency** — what posture clears at what grade is the downstream JSG-01/owner residual; this work only closes the *value* vocabulary.
- **Do not touch JSG-01** and **do not unfreeze it** — JSG-01 binding is a separate, later step out of this work-unit.
- No `jb` import; `agent-workflow` is reusable mechanics only.

## Validation plan (must be able to fail)

- Existing unit tests pass after migration (or are migrated with a recorded compatibility stance); name any test changed and why.
- Named existing packet manifests are migrated or compatibility-bound; no silent break.
- `source_quality.py` no longer derives source/snapshot time from the closed cutoff enum (show the changed read path).
- `hash_basis` enforces the recomputation-bound contract, not an arbitrary string.
- Obligation contract states Ob.9/10/15 vocabularies as closed; Ob.10 representation pinned.
- Inline DCP receipt present; downstream surfaces checked.
- Report changed files with a fresh-read verification for each lifecycle claim.

## Output mode

`file-write` (under authorization): source/contract changes + inline DCP receipt + a short completion report (changed files, validation evidence, residuals). Scoping-only dispatch returns the non-executing route + open questions, no edits.

## Stop conditions / blockers

- Migration representation ambiguous (how to map the overloaded values) → stop, surface options to owner.
- Untangling reveals deeper coupling than the proposal anticipated → stop, report.
- Authorization not granted → scope only, stop at the gate.

## Non-claims

This handoff prepares and routes the work-unit. It is not validation, readiness,
ratification, JSG-01 unfreeze, or source-of-truth promotion. It does not itself
authorize implementation — owner acceptance does. The obligation-contract
amendment is doctrine and requires its own DCP receipt at closeout.
