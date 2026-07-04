# Prospective Decision Loop — Phase-0 Semantics Spec v0 (the book, hand-runnable)

```yaml
retrieval_header_version: 1
artifact_role: PROPOSED Phase-0 semantics spec (consumes the target architecture landed via PR #34 @ 53d5b4b; owner ratification statement pending — binds nothing, builds nothing, authorizes no seal)
scope: >
  Hand-runnable operational semantics for the prospective decision loop's
  decision object and seal/disclosure/resolution protocols ("the book"):
  per-field fill-rules, the write-once hash-chained entry mechanics, the hash
  convention, the proposed ledger home, and a worked end-to-end paper example.
use_when:
  - Running a decision through intake -> seal -> (disclose) -> resolve by hand under a signed pilot ledger.
  - Drafting or signing the Phase-1 dogfood pilot ledger.
  - Checking what any decision-object field means, who fills it, when, and from what.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md
input_hashes:
  forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md: 71D0460CE5FE1F15FFE713F2CA523CDBA2BA7435428E4EC266DAB3ECB5E0E9D5
branch_or_commit: phase0-semantics-spec-v0 off origin/main @ 64c442a (target architecture landed via PR #34 @ 53d5b4b)
stale_if:
  - The owner ratifies/amends/rejects the target architecture (reconcile or retire with it).
  - The pilot ledger is signed with a different ledger home or entry shape than proposed here.
  - The near-half signal-reliability ledger lands as a durable artifact (reconcile the N7 fields).
  - Harness vocabulary changes in orca-harness/schemas/judgement_models.py (re-pin the trace table).
```

## Status

`PROPOSED` — Phase-0 docs contract, product-learning tier. The consumed target
architecture is landed on main (PR #34 @ 53d5b4b); the owner's explicit
ratification statement is still pending. Nothing here is runnable as evidence
until (a) that ratification statement and (b) the signed Phase-1 pilot ledger. The worked example below is
**illustration, never evidence** (`example_not_a_sealed_decision`).

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_phase0_semantics (adjudicated target + harness judgement_models.py + batch-1 ledger + overlay validation/retrieval contracts, all read this thread)
  edit_permission: docs-write
  target_scope:
    - forseti/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_phase0_semantics_spec_v0.md (new, this file only)
  dirty_state_checked: yes (worktree clean at bac084f before branch)
  blocked_if_missing: no
```

## What This Spec Does

The target architecture froze the decision-object **shape** and the firewall
**invariants**. This spec makes them **hand-runnable**: for every field, who
fills it, when, from what source, and what counts as filled; and for the book,
exactly what an operator does with files, hashes, commits, and pushes. The test
of completeness: an operator can run a real decision (DecisionEvent) through the loop using
only this document, with zero invented semantics.

## Vocabulary Trace Table (zero unmapped names allowed)

Every field name below traces to one owning source. No new vocabulary is minted.

| Field / term | Owning source |
| --- | --- |
| decision_object_v0 groups (identity, mode, frame, sealed_call, disclosure, actual_path, updates, resolution, learning_extraction, integrity) | Target architecture §1 (adjudicated) |
| claimed_floor, claimed_ceiling, reasoning | `ContestantBandClaim`, orca-harness/schemas/judgement_models.py |
| statement, evidence_unit_ids, would_flip_if_false | `LoadBearingAssumption`, judgement_models.py |
| claim_text, claim_role: load_bearing / supporting / contextual, evidence_unit_ids | `EvidenceUsed`, judgement_models.py |
| signal_id | Target architecture §1 `signals_used` / pending near-half signal-reliability interface |
| 0–8 action-intensity ladder | `RecommendedAction.ladder_level`, judgement_models.py |
| seal-before-disclose, mechanical resolution, append-only, quarantine-as-data | Target architecture (firewall translation, adjudicated) |
| unscoreable_by_design | Target architecture §1 intake gate |
| example_not_a_sealed_decision | This spec (label only; carries no claim) |

### The action-vocabulary decision (explicit, as the assumption gate required)

**Decision: reuse the 0–8 action-intensity ladder as the shared scale.
Per-decision action labels are satellite.** Rationale: the adjudicated target
froze `confidence_band` as the contestant band-claim shape, and band
floor/ceiling values are defined *over ladder levels* — band reuse entails the
ladder. What level N concretely means for a given decision ("level 4 = run the
blog screen first at full budget") is stated per decision in `frame.options`,
never globally. The harness `judgement_class` → level constraints (abstain=0,
wait=1, escalate=6, recommend∈{2,3,4,5,7,8}) are harness-owned validation,
inherited as-is and not redefined here.

## Decision-Object Field Semantics (fill-rules)

Format per field: **filled by / when / from what / filled means**.

### identity
- `decision_id` — operator / at intake / pattern `dl-<counterparty>-<yyyymmdd>-<slug>` / unique in the index.
- `decision_family` — operator / at intake / the ledger's declared family list / one named family (keys memory and lesson routing).
- `counterparty` — operator / at intake / `orca-internal` for dogfood, org name otherwise.
- `decision_owner` — operator / at intake / the human who will actually decide.
- `intake_timestamp` — operator / at intake / wall clock, ISO-8601 with timezone (operator-asserted; ordering proof comes from the chain, not this field).

### mode
- `declared_mode` — operator / **at intake, before any seal exists** / the signed pilot ledger's per-decision declaration / `shadow` or `assisted`; immutable after intake except by dated amendment entry. A decision whose mode is declared after its seal is a firewall breach (see Breach Route).

### frame (a genuine decision brief — decision-framing, never test-framing)
- `question` — operator with the decision owner / at intake / the owner's words / one decidable question ("what is the best way forward on X by <deadline>?").
- `options_considered` — operator / at intake / the owner's real option set / 2+ options, each with its action label and its 0–8 ladder level stated ("level 4 = <concrete action>").
- `constraints` — operator / at intake / owner-stated limits (budget, deadline, irreversibles).
- `decision_deadline` — operator / at intake / when the org must decide.
- `information_set_ref` — sealing actor / at seal / **an enumerated list of every input the sealed call used** (paths, URLs, doc titles), each with a hash where hashable / filled means the list is complete *for what was used*. This proves what WAS seen — never that nothing else was (disclosed residual, inherited from the target).

### sealed_call (the ONLY scoreable forecast; authored by the org-blind sealing actor)
- `recommendation` — sealing actor / at seal / from the frame only / one option + its ladder level + the concrete action shape.
- `confidence_band` — sealing actor / at seal / `{claimed_floor: 0–8, claimed_ceiling: 0–8, reasoning: required}` / floor ≤ recommended level ≤ ceiling, with the reasoning naming what widens or narrows the band.
- `expected_outcome` — sealing actor / at seal / `{metric, band, measurement_window}` / REQUIRED: a named observable metric, the predicted band on it, and when it is read. Missing or unmeasurable → the decision is `unscoreable_by_design` (loggable for memory; permanently excluded from calibration and judgment claims).
- `resolution_criteria` — sealing actor / at seal / mechanical instructions a third party could apply: where the metric is read, how the band is compared, what counts as in/over/under / filled means resolution requires zero judgment. Resolution may **apply** these; it may never author or amend them.
- `leading_indicators` — sealing actor / at seal / `[{signal, expected_direction, check_window}]` / observable early signals; empty allowed with the line "none identified".
- `kill_or_adjust_triggers` — sealing actor / at seal / `[{condition, pre_committed_response}]` / conditions concrete enough that firing is observable.
- `signals_used` — sealing actor / at seal / `[{signal_id, claim_text, claim_role, evidence_unit_ids}]` with `claim_role` ∈ load_bearing/supporting/contextual / every load-bearing input named; `signal_id` is the live-loop signal key, while `claim_text`, `claim_role`, and `evidence_unit_ids` reuse the harness evidence vocabulary (this is the live signal pre-commitment; rows flow to the near-half reliability ledger at resolution). Values in `evidence_unit_ids` at this tier are retrieval handles (paths, sections, URLs); no `EvidenceUnit` is bound by any live-loop entry — JSG-01 stays frozen.
- `assumptions` — sealing actor / at seal / `[{statement, evidence_unit_ids, would_flip_if_false}]` / every assumption whose falsity would change the call carries `would_flip_if_false: true`.
- `lessons_consulted` — sealing actor / at seal / retrieval handles of validated lessons used; `pending_interface` until the near-half ledger exists (N7); never invented.
- `reasoning_trace` — sealing actor / at seal / REQUIRED full trace from frame to recommendation / filled means a reader can derive the call from the brief (the derivability standard; doubles as the lesson-extraction and audit surface).
- `seal.content_hash` — operator / immediately after committing the sealed-call file / the hash convention below.
- `seal.seal_timestamp` — operator / at commit / ISO-8601 (corroboration only; the chain is the proof).
- `seal.sealing_actor` — operator / at seal / who authored the call. **Norm: an org-blind subagent given only the frame** (single-operator authorship is a named, disclosed residual at product-learning tier).

### disclosure (assisted mode only; structurally absent in shadow)
- `disclosed_to`, `disclosure_timestamp`, `owner_response (accepted|modified|rejected)`, `owner_response_reasons`, `modification_delta` — operator / at and after disclosure / disclosure_timestamp strictly after seal_timestamp AND the disclosure entry embeds the sealed-call hash (chain proof). Post-resolution *presentation* of a shadow record never fills these fields and never reclassifies the route (adjudicated AR-02 rule).

### actual_path (passive observation)
- `org_decision`, `org_decision_timestamp`, `divergence_from_recommendation` — operator / when the org decides / observation, owner statement, or org record / divergence stated as: same option, different option, different level on same option, or no-decision-by-deadline.

### updates
- optional re-seals / sealing actor + operator / **only before the relevant outcome/resolution signal is known** / each update is a complete new sealed-call entry embedding the prior seal's hash; it never edits or replaces an earlier scoreable call — every prior seal still resolves (adjudicated AR-03 rule).

### resolution
- `outcome_record` (Outcome) — resolution actor / when `measurement_window` closes / the metric source named in `resolution_criteria`.
- `score` — resolution actor / same / mechanical application: in-band / over / under per the criteria; nothing else.
- `indicator_outcomes` — per indicator: led / did not lead / not observable, with lead time when led.
- `trigger_outcomes` — per trigger: fired correctly / fired wrongly / should have fired / correctly silent.
- `assumption_outcomes` — per assumption: held / failed / untested.
- `resolution_actor`, `resolution_timestamp` — operator / at resolution / the resolution entry embeds the sealed-call hash (chain proof; the actor is necessarily outcome-aware — harmless because the criteria are pre-specified).

### learning_extraction
- `signal_reliability_rows` — resolution actor / at resolution / one row per `signals_used` entry: did the load-bearing signal point the right way / destination: the near-half ledger (pending interface; rows accumulate in the entry until it exists).
- `lesson_candidates` — resolution actor / at resolution / candidates only; **validation is owned by the near-half adversarial postmortem, never by this loop**.
- `calibration_row` — resolution actor / at resolution / `{claimed_floor, claimed_ceiling, resolved_level_or_band_outcome}`.

### integrity
- `firewall_state` — operator / any time a breach is confirmed / `clean` or `breached_quarantined` with `breach_note` naming the broken invariant. Quarantine = recorded-as-data, never deleted.

## The Book: Entry Mechanics (write-once, hash-chained)

**Folder shape (per decision):**

```text
<ledger_home>/<decision_id>/
  01_intake.md          # identity + mode + frame
  02_sealed_call.md     # sealed_call (embeds the SHA256 of 01_intake.md)
  03_disclosure.md      # assisted only (embeds the SHA256 of 02_sealed_call.md)
  04_actual_path.md     # passive observation when the org decides (embeds the latest prior entry SHA256)
  0N_update_seal.md     # optional re-seals before org-decision/outcome/resolution signal is known (each embeds the prior scoreable seal's SHA256 and the latest prior entry SHA256)
  0M_resolution_<seal-entry>.md # resolution + learning_extraction for one scoreable seal/update (embeds that seal/update SHA256 and the latest prior entry SHA256)
<ledger_home>/index.md  # one line per entry: decision_id -> file -> hash -> status
```

**The chain rule (the ordering proof):** every entry after the first embeds the
hash of the latest prior ledger entry it follows. A disclosure containing the
seal's hash can only have been written after the seal existed; an update seal
also embeds the prior scoreable seal hash it supersedes-by-reference; a
resolution embeds the specific seal/update hash it resolves. Ordering is proven
by content, not by timestamps or git history, so it survives squash-merges and
branch deletion.

**Hash convention (binding):** SHA256 over **git blob bytes** (LF as stored),
never CRLF working-tree bytes. Verified recipe (cross-platform):

```text
python -c "import subprocess,hashlib;print(hashlib.sha256(subprocess.run(['git','cat-file','blob','<rev>:<path>'],capture_output=True,check=True).stdout).hexdigest())"
```

(PowerShell pipes re-encode bytes — do not hash via `git cat-file ... | Get-FileHash`.)

**Operator sequence per entry:** write the entry file → commit → compute the
blob hash at that commit → record it in `index.md` (and embed it in the next
entry when one follows) → **push the lane branch promptly** (origin holds the
ordering corroboration) → land via small PR (a human lands; main's history is
the public anchor).

**Write-once rule:** entry files are never edited after their hash is recorded.
New information = new entry. **Breach route:** any diff touching an existing
hashed entry, any mode declared after seal, any disclosure preceding seal, or
any resolution criteria authored post-outcome → append a quarantine entry
naming the breach, set `firewall_state: breached_quarantined`, keep everything.

## Proposed Ledger Home (proposal only — owner binds at pilot-ledger sign-off)

`docs/product/judgment_spine/decision_ledger/` — following the narrow-folder
precedent (the smoke-tests binding): a bound folder with a permanent boundary
note that **location confers no evidence tier** — entries are product-learning
records and the folder is plumbing, not proof. The binding itself requires an
artifact-folders amendment with its own propagation receipt, executed at ledger
sign-off, not by this spec.

## Worked Example (`example_not_a_sealed_decision` — every value illustrative)

**Decision:** which venue family should batch-2 case screening prioritize first.

- **identity:** `dl-orca-internal-20260615-batch2-venue-priority`; family
  `internal-operating`; counterparty `orca-internal`; owner: Eric.
- **mode:** `shadow`, declared at intake (the owner will order the screen
  normally; the sealed call stays dark until resolution).
- **frame:** question: "Which venue family does the batch-2 screen run first:
  subscription-box review blogs, Reddit beauty communities, or trade press?"
  Options with ladder labels: level 3 = trade press first (lowest commitment);
  level 4 = blogs first at full screen budget; level 5 = blogs + Reddit in
  parallel (highest spend). Constraints: two research-agent passes of budget;
  deadline: before the batch-2 ledger declaration. `information_set_ref`:
  [batch-1 ledger Screen Provenance section @ its blob hash; the case-finder
  frame doc @ its blob hash].
- **sealed_call** (authored by an org-blind subagent from the frame above):
  recommendation: level 4 — blogs first at full budget. confidence_band:
  `{claimed_floor: 3, claimed_ceiling: 5, reasoning: "blog yield is proven on
  batch-1 but single-batch; parallel (5) wins if blog yield has saturated;
  trade-press-first (3) wins only if blogs duplicate batch-1 candidates"}`.
  expected_outcome: `{metric: Tier-A-qualifying candidates from the first
  screen pass, band: ">=3", measurement_window: first pass complete, <=3 weeks}`.
  resolution_criteria: "count candidates marked Tier-A in the batch-2 screen
  provenance section, attributed by venue family; >=3 from blogs = in-band;
  0-2 = under; >=3 from a non-blog family while blogs <3 = under + signal row
  against the load-bearing signal." leading_indicators: `[{signal: candidate-URL
  density in first 10 blog sources checked, expected_direction: higher than
  Reddit equivalents, check_window: first screening day}]`.
  kill_or_adjust_triggers: `[{condition: first pass yields 0 qualifying blog
  candidates, pre_committed_response: reprioritize Reddit immediately}]`.
  signals_used: `[{signal_id: batch1-screen-venue-yield, claim_text: "blogs
  (mysubscriptionaddiction, hellosubscription) produced multiple Tier-A
  candidates in batch-1", claim_role: load_bearing, evidence_unit_ids:
  [batch-1 Screen Provenance]}]`. assumptions:
  `[{statement: "decision-shaped events (repricing, channel entry) surface in
  dedicated review blogs before general communities", evidence_unit_ids: [batch-1
  Screen Provenance], would_flip_if_false: true}]`. lessons_consulted:
  `pending_interface (near-half ledger not yet durable)`. reasoning_trace:
  "batch-1's only proven candidate venues are blogs; the family constraint
  (beauty consumer-demand) matches blog coverage; Reddit yielded evidence but
  fewer decision-shaped events; therefore level 4, not 5 — parallel spend is
  unjustified while blog yield is unprobed for saturation." seal: commit the
  file, compute blob hash via the recipe, record in index, push.
- **actual_path (illustrative):** org decided level 5 (parallel) two days
  later; divergence: different level on same primary option.
- **resolution (illustrative, window closed):** outcome_record: blogs produced
  4 Tier-A candidates, Reddit 1 → score: in-band. indicator_outcomes: URL
  density led, ~1 day. trigger_outcomes: correctly silent.
  assumption_outcomes: held. calibration_row: `{3, 5, resolved: in-band at
  recommended level}`. signal_reliability_rows: `batch1-screen-venue-yield:
  pointed correctly (1 of 1 pre-committed uses)`. lesson_candidates: "parallel
  spend added 1 candidate over blogs-first — candidate lesson: blogs-first
  sufficient at current family constraint" → routed to near-half validation,
  not self-adopted. **divergence read:** org chose higher spend; outcome
  favored the sealed call's economy — recorded, claims nothing at N=1.

The example exercises every field group including a divergence and a silent
trigger; disclosure stays empty (shadow). It creates no registry entry.

## Residuals (inherited, disclosed, not solved here)

Operator-asserted timestamps (chain + push corroborate ordering, not clocks);
information-set completeness unprovable (enumerated-inputs only); dogfood
single-operator memory bridge (org-blind sealing subagent is the norm, not a
gate); index drift until a later owner-gated write-boundary checker; external
notarization deferred to the prospective gate family (ladder owner's territory).

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: Phase-0 semantics spec (design/docs contract)
  source_quality_state: design/control artifacts only (adjudicated target + harness schemas, read this thread)
  execution_quality_state: no run, no seal, no resolution exists; the worked example is labeled illustration
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no signed pilot ledger; target architecture unratified; prospective gate family unauthored
  receipt_artifact_or_gap: first real receipts would be chain entries under an owner-signed pilot ledger
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Non-Claims

- Spec completion is not loop validation, pilot authorization, ratification, or
  readiness; no seal may be made before the owner-signed Phase-1 ledger exists.
- The proposed ledger home is a proposal; the owner binds it (or another) at
  ledger sign-off with its own propagation receipt.
- Mints no evidence-ladder vocabulary; the 0–8 ladder, band claim, assumption,
  and claim-role shapes remain owned by their harness/architecture sources.
- The near-half interface stays `pending_interface`; nothing here creates the
  reliability ledger or validates lessons.
- The worked example is illustration (`example_not_a_sealed_decision`) and can
  never be cited as a sealed call, calibration data, or any evidence tier.
