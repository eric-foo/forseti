# Demand-Read Projection Semantics Propagation — Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial review report
scope: >
  Adversarial review of the 15-file demand-read projection-semantics propagation patch
  at commit eca296145ac395e33b6b9c9928e4c96b29566f9d on branch
  codex/demand-read-machinery-settlement-prompt.
authority_boundary: retrieval_only
reviewed_by: claude-sonnet-4-6 (Anthropic / Claude family)
authored_by: OpenAI / GPT-family Codex lane
de_correlation_bar: cross_vendor_discovery
use_when:
  - Adjudicating findings from this adversarial review before merging PR #352.
  - Deciding whether any findings require a patch pass before merge.
stale_if:
  - Commit eca296145ac395e33b6b9c9928e4c96b29566f9d is amended or superseded.
  - The demand-read projection-semantics patch is materially changed after this review.
```

## Source Preflight

**Review commission:** `docs/prompts/reviews/demand_read_projection_semantics_propagation_adversarial_review_prompt_v0.md`
— owner-authorized "just in case" hardening pass after `workflow-delegated-review-patch` invocation.

**Review mode:** read-only adversarial artifact review. Commission boundary holds: no
`patch_queue_entry`, no patch execution. Findings are advisory decision input only.

**Skills applied:** `workflow-deep-thinking` then `workflow-adversarial-artifact-review`
per commission requirement. Both applied; invocations are active in this session.

**Output mode:** `filesystem-output` at bound path
`docs/review-outputs/adversarial-artifact-reviews/demand_read_projection_semantics_propagation_adversarial_review_v0.md`
(relative to the codex worktree root). Destination confirmed to exist.

**De-correlation receipt:**
- `authored_by`: OpenAI / GPT-family Codex lane (commit `eca29614` author)
- `reviewed_by`: claude-sonnet-4-6 (Anthropic / Claude family)
- `de_correlation_bar`: `cross_vendor_discovery` — reviewer is non-OpenAI lineage;
  two-bar de-correlation discovery bar applies.

**Authority sources read (all 10 required):**
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

**Change packet read:** full diff
`c4655c976a3e7bc8a01ed415efbc20f5108908b8..eca296145ac395e33b6b9c9928e4c96b29566f9d`
(95.4 KB, 15 files). All 15 changed files reviewed at full current-file depth where
structural findings depend on it; diff-level analysis sufficient for semantic propagation
findings.

**One out-of-scope file investigated:** `orca/product/satellites/fragrance/judgment_level1/
satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md` — read
to verify DCP propagation scope gap. Not in the 15-file patch set; read to confirm
stale-language hit.

---

## Findings

Findings are ordered by severity and phase. Severity labels are finding-priority only
per review-lanes.md: `critical` = blocks confident merge; `major` = material defect
requiring owner decision before merge; `minor` = clear defect, correctable post-merge
without doctrine risk.

No critical findings.

---

### AR-01 — Major | Phase 1 (Correctness)

**Check category:** Structural damage from the patch (Check 7).

**Location:**
`orca/product/spines/judgment/demand_read/c3_verdict_action/
judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
— `## Interfaces / Contracts` section, "Inputs (read-only, by pointer)" bullet,
approximately line 377–380.

**Issue:** The "Inputs" prose bullet ends mid-sentence at `the **integrity**`. The
continuation — `disposition (real / disqualified-or-held) from C1 + C2 Rule 3; the
**persistence-axis discriminator findings** routed from C2 Rule 3.` — was deleted as
a patch edit artifact. The sentence is structurally broken.

**Evidence:**
```
- **Inputs (read-only, by pointer):** the active `(decision_family, Decision Frame)`
  (C0); the **C2-weighted allowed signals** (each: direction, per-case reasoning,
  qualitative weight band, `signal_id`, travelled caveats); the **integrity
- **Outputs:** the `sealed_call` slots — ...
```
The `- **Outputs:**` bullet follows immediately after `the **integrity**`, making the
inputs list appear to end at the word "integrity" with no continuation.

**Strongest counter-reading:** The `spec_handoff` YAML block (line 476) correctly retains
`integrity disposition (real | disqualified/held) from C1+C2, persistence-axis discriminator
findings from C2 Rule 3` in `interfaces_contracts.inputs_read_only`. The Input Basis prose
(lines 277–281) also correctly names these inputs. A reader who checks the spec_handoff
discovers the complete input list.

**Why the defense fails:** The prose `## Interfaces / Contracts` → `Inputs` section is
the primary human-readable interface contract. A reviewer or agent reading this section
cold sees `the **integrity**` as the terminal word of the inputs list, with no hint
that the sentence is broken. The spec_handoff YAML is a machine-targeted schema; it is
not a substitute for the prose contract's completeness. The deletion removes two
load-bearing inputs — the integrity disposition and persistence-axis discriminators —
from the operative prose, leaving a contract surface with a hole in its stated inputs.

**Impact:** Any future agent sourcing C3's input requirements from the prose interfaces
section will miss the integrity disposition and persistence-axis discriminator findings
as required C3 inputs. These are not optional — C3's demand-state verdicts depend on
consuming the real/disqualified integrity disposition from C1+C2 Rule 3 and the
persistence-axis pattern findings from C2 Rule 3. The broken sentence creates a latent
incorrect-input risk.

**minimum_closure_condition:** The Inputs prose sentence is repaired to correctly name
all three inputs (C2-weighted allowed signals; integrity disposition from C1+C2 Rule 3;
persistence-axis discriminator findings from C2 Rule 3), or a durable note is added
cross-referencing the spec_handoff as the authoritative complete list.

**next_authorized_action:** Owner decision. Patch is advisory only from this lane;
a separate patch-authorized pass would apply the repair. The finding is sufficient to
flag for the PR review before merge.

**Advisory remediation direction:** Restore the deleted continuation in the Inputs
bullet. The correct prose is:
```
  qualitative weight band, `signal_id`, travelled caveats); the **integrity
  disposition** (real / disqualified-or-held) from C1 + C2 Rule 3; the
  **persistence-axis discriminator findings** routed from C2 Rule 3.
```
No doctrine change; pure repair of a patch-artifact sentence truncation.

---

### AR-02 — Major | Phase 1 (Correctness)

**Check category:** Propagation completeness (Check 9) + structural damage (Check 7).

**Location:** `direction_change_propagation` receipt dated 2026-06-23 inside
`orca/product/spines/judgment/demand_read/c3_verdict_action/
judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
(approximately lines 223–262).

**Issue:** The 2026-06-23 DCP receipt is missing two fields that are standard in
the established receipt pattern: `stale_language_search_result` and
`intentionally_not_updated`. As a consequence: (a) there is no confirmation that the
stale-language search was actually executed; (b) surfaces outside the 8 listed search
paths — specifically `orca/product/satellites/` — are neither checked nor explicitly
deferred. A verified stale-language hit exists in a file the search would have missed.

**Evidence:**

*2026-06-23 DCP receipt (committed in this patch):*
```yaml
direction_change_propagation:
  doctrine_changed: >
    Durable demand is now encoded as a forward demand call ...
  trigger: product_doctrine
  related_triggers: [architecture_doctrine]
  controlling_sources_updated: [3 files]
  downstream_surfaces_checked: [12 files]
  stale_language_search: >
    rg -n "observed persistence|...|transient-default|earned-durable"
    docs/decisions/... orca/product/spines/... [8 path prefixes]
  non_claims: [...]
```
No `stale_language_search_result` field. No `intentionally_not_updated` field.

*Pattern established by the prior 2026-06-20 receipt in the same file:*
```yaml
  intentionally_not_updated:
    - path: ALL TEN DOWNSTREAM SURFACES ABOVE
      reason: SEQUENCED REALIGNMENT, NOT SILENTLY FORKED ...
  stale_language_search: >
    rg -i "phase \| narrow|..." (repo-wide)
  stale_language_search_result: >
    Executed 2026-06-20. Eleven files carry the old action vocabulary ...
```
The 2026-06-20 receipt shows `stale_language_search_result` (confirmed execution + result)
and `intentionally_not_updated` (explicit deferral with reason).

*Active stale-language hit in uncovered surface:*
`orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/
fragrance_level1_product_learning_satellite_skeleton_v0.md`, line 279:
```
- C3 trace fields must preserve the transient-default and action-ceiling logic:
```
The phrase `transient-default` is stale under the 2026-06-23 clarification. Under the
new semantics, transient is the call when a durability basis is absent from the
information set — not an unconditional default. The satellite skeleton's line 279 implies
transient is always the first mandated call, which contradicts the calling sequence
clarification. The DCP receipt's `stale_language_search` query includes `transient-default`
as a search term, but its path scope does not cover `orca/product/satellites/`.

**Strongest counter-reading:** The 2026-06-23 receipt's `downstream_surfaces_checked` list
already covers 12 of the 15 patch files plus the 3 controlling sources = the full 15-file
patch set. The satellite skeleton is a pre-existing pending-realignment surface from the
2026-06-20 receipt (its stale action vocabulary was already known). A reader could infer
the satellite skeleton was considered and deferred consistent with the 2026-06-20 receipt's
sequenced-realignment approach.

**Why the defense fails:** Inference is not a receipt. The 2026-06-20 receipt explicitly
named the satellite skeleton for action-vocabulary realignment, not transient/durable
language. The 2026-06-23 receipt introduces a distinct doctrine change (projection
semantics) that creates an additional stale-language category. The satellite skeleton's
`transient-default` is stale under both 2026-06-20 (action vocabulary) and 2026-06-23
(projection semantics) now. The 2026-06-23 receipt's search scope would not find it,
and no `intentionally_not_updated` explicitly defers it. A downstream agent reading the
satellite skeleton and the 2026-06-23 receipt cannot determine whether `transient-default`
at line 279 is "intentionally preserved" or "accidentally missed."

**Impact:** An executor following the satellite skeleton's C3 trace requirements could
interpret `transient-default` as mandating a transient call regardless of whether a
durability basis is in the information set — directly contradicting the 2026-06-23
clarification's operative rule. This is a live semantic mismatch in an implementation-
facing surface. Additionally, the missing `stale_language_search_result` leaves the
DCP completeness gate unprovable.

**minimum_closure_condition:** Either (a) the satellite skeleton's `transient-default`
at line 279 is updated to align with 2026-06-23 semantics AND the `stale_language_search_result`
field is added to the DCP receipt with confirmation of execution and any residual hits
named with disposition; OR (b) an `intentionally_not_updated` field is added explicitly
naming the satellite skeleton (and any other surfaces outside the 8 search paths) with
a sequenced-realignment deferral reason, AND `stale_language_search_result` is populated.

**next_authorized_action:** Owner decision on path (a) vs (b). If path (a): a patch-
authorized pass updates the satellite skeleton and adds the missing DCP receipt fields.
If path (b): the 2026-06-23 DCP receipt is amended with explicit deferral and a search
result is added.

**Advisory remediation direction:**
- Add to the 2026-06-23 DCP receipt:
  ```yaml
    intentionally_not_updated:
      - path: orca/product/satellites/fragrance/judgment_level1/satellite_skeleton/fragrance_level1_product_learning_satellite_skeleton_v0.md
        reason: >
          Carries stale `transient-default` language (line 279). Sequenced for
          satellite-skeleton realignment pass; does not block the 2026-06-23 projection
          clarification from being controlling from this amendment forward.
      - path: [any other out-of-scope paths with stale transient/durable language]
        reason: [...]
    stale_language_search_result: >
      Executed [date]. Paths scoped to the 8 listed prefixes returned [result].
      orca/product/satellites/ was not in scope; transient-default at line 279 of the
      fragrance satellite skeleton found separately and named above.
  ```
- Update satellite skeleton line 279 from `transient-default` to language consistent with
  the calling sequence: "C3 trace fields must name the calling-sequence verdict (transient
  unless a durability basis is in the information set, or durable with a named basis) and
  the action-ceiling logic: ..." — or equivalent.

---

### AR-03 — Minor | Phase 1 (Correctness)

**Check category:** Structural damage from the patch (Check 7).

**Location:**
`orca/product/spines/judgment/demand_read/c3_verdict_action/
judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
— between the `spec_handoff` YAML block (ending ~line 514) and the `## Claim
Classification` section (line 536).

**Issue:** Five source-read ledger bullet entries (approximately lines 516–534) appear
without a `## Source-Read Ledger` section header. The diff removed the header and its
trailing blank line while preserving the bullet content. The document's section structure
in the `## Claim Classification` header vicinity shows: `[spec_handoff YAML]` → `[5 naked
bullets]` → `## Claim Classification`. The bullets are orphaned.

**Evidence:** `grep -n "^## " judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
returns `## Non-Claims` as the last section header before end of file; no
`## Source-Read Ledger` appears. The five bullets (architecture, C2 contract, buyer proof,
far-half, taxonomy) are visible at lines 516–534 without a section heading.

**Strongest counter-reading:** The bullet content is intact, correct, and readable. A reader
sees five pointed source entries with context; the content is not lost.

**Why the defense fails:** The orphaned bullets have no section context. An agent or reader
scanning section headers (common practice for structured documents) would not find a
`## Source-Read Ledger` section and would not know the five bullets constitute one. The
`## Claim Classification` section that follows inherits the orphaned bullets visually as
pre-conditions without the reader knowing they are a ledger.

**Impact:** Minor navigability and document-structure defect. No semantic loss; content
is present and correct.

**minimum_closure_condition:** The `## Source-Read Ledger` heading is restored before the
first orphaned bullet entry.

**next_authorized_action:** Patch-authorized pass may apply the heading restore; advisory
only from this lane. Alternatively: addressed at next C3 contract touch.

---

### AR-04 — Minor | Phase 1 (Correctness)

**Check category:** Structural damage from the patch (Check 7).

**Location:**
`orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
— between section `## 6. Wind-Caller Sub-Procedure` and `## Hard Constraints (carried)`.

**Issue:** The `## 7. Reconciliation Note` section header was deleted. The content that
constituted section 7 — bullets reconciling the demand-read taxonomy, two-axis model, and
wind-caller sub-procedure — remains in the file but is no longer under a named section
heading. The scan spec's numbered sections run 1 through 6; section 7 content is present
but section 7 is unnamed.

**Evidence:** `grep -n "^## " orca_demand_scan_core_spec_v0.md` returns `## 6. Wind-Caller
Sub-Procedure` followed by `## Hard Constraints (carried)` with no `## 7.` entry. The
bullets starting with "**Demand-read taxonomy** — this spec ABSORBS its demand-state model"
are present in the file without a section heading.

**Strongest counter-reading:** The content is unchanged and correct; only the header was
removed. A reader sees the reconciliation bullets between section 6 and Hard Constraints.

**Why the defense fails:** The same issue as AR-03: a structured document that uses numbered
`##` section headings loses navigational integrity when a numbered section's content is
preserved without its heading. The asymmetry between sections 1–6 (headed) and section 7
(content only) is a clarity defect.

**Impact:** Minor structural defect; no semantic content lost.

**minimum_closure_condition:** `## 7. Reconciliation Note` heading is restored before the
first orphaned bullet.

**next_authorized_action:** Patch-authorized pass or next scan spec touch.

---

### AR-05 — Minor | Phase 1 (Correctness)

**Check category:** Stale semantics (Check 1) + under-propagation (Check 3).

**Location:**
`orca/product/spines/foundation/demand_read_taxonomy/
orca_demand_read_taxonomy_adjudication_v0.md`
— Q0 "Refined 2026-06-14" section, approximately lines 316–324.

**Issue:** The Q0 Refined note says "the read opens **transient** and acts in-window (buy
or avoid), then **observes** persistence via monitoring and **earns** the upgrade to durable
— no decay curve to predict; the earlier decay-timing-confidence guardrail is superseded by
observe-don't-predict." This language presents durable as a monitoring-earned upgrade from
transient — the exact framing the 2026-06-23 clarification supersedes. The text has no
`(clarified 2026-06-23)` annotation.

**Evidence:**
- Adjudication file lines 316–324: `**observes** persistence via monitoring and **earns**
  the upgrade to durable — no decay curve to predict`
- Part 1 operative boundary note (line ~214–217): `A transient call is **built-to, not
  proven-at** on its exact lifespan ... (reconciled 2026-06-14, OF-01; clarified 2026-06-23).`
- Status block header: updated to include `clarified 2026-06-23` in the section header.
- The Q0 Refined note itself: no `(clarified 2026-06-23)` annotation.

**Strongest counter-reading:** The Q0 Refined section is a historical decision record
(labeled "Refined 2026-06-14 (owner)"), not an operative definition. The Part 1 read-type
definitions are the operative rules and they are correctly updated. A careful reader would
privilege Part 1 over the historical Q0 record.

**Why the defense fails:** The Q0 Refined text is not labeled "historical" or "superseded"
— it is presented as the active resolved framing of the 2026-06-14 decision. A reader
who encounters the Q0 section before Part 1 (top-to-bottom reading) will see "observes
persistence... earns the upgrade to durable" as the operative calling sequence, potentially
concluding that t=0 durable calls are never appropriate. The 2026-06-23 clarification
explicitly permits t=0 durable when a durability basis is in the information set. The
missing annotation leaves a latent collision between Q0 historical text and the 2026-06-23
active rule.

**Impact:** Minor semantic confusion risk. No operative definition is wrong; the risk is
a future agent or reader anchoring on Q0 Refined over Part 1, leading to incorrect
rejection of valid t=0 durable calls.

**minimum_closure_condition:** A `(clarified 2026-06-23)` note is appended to the Q0
Refined section (specifically to the "earns the upgrade to durable" sentence) indicating
that the calling sequence has been refined: observed persistence remains valid evidence but
durable is callable at t=0 when a durability basis is in the information set.

**next_authorized_action:** Advisory recommendation for the next adjudication file touch.
Low urgency; the Q0 section is a historical record and Part 1 governs.

---

### AR-06 — Minor | Phase 2 (Friction)

**Check category:** Structural damage / redundancy loss (Check 7).

**Location:**
`orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
— LinkedIn org-motion context note, line ~631.

**Issue:** The explicit guardrail "org-level only (hiring composition, headcount), never
person-level" was removed from the scan spec's LinkedIn context bullet and replaced with
"this spec does not absorb the separate LinkedIn/org-motion decision context." The person-
level prohibition is no longer stated at the scan level.

**Evidence:**
- Deleted text: `org-level only (hiring composition, headcount), never person-level.`
- Current text (line 631): `LinkedIn org-motion is a separate context, completely
  unchanged — this spec does not absorb the separate LinkedIn/org-motion decision context.`
- The person-level prohibition still exists in the taxonomy.

**Strongest counter-reading:** The constraint lives in the taxonomy, which governs the
scan. The scan spec correctly defers to the separate LinkedIn/org-motion context. No
semantic gap exists.

**Why this is a friction finding not a correctness finding:** The person-level prohibition
is the most safety-sensitive aspect of LinkedIn org-motion handling. Redundant statement
at the scan level reduced the risk of a scan implementer missing it. The replacement
language points away ("see separate context") rather than stating the constraint inline.
This is a redundancy reduction, not a semantic loss — hence friction, not correctness.

**Impact:** Minor. A future scan implementer reading this file would need to separately
look up the LinkedIn/org-motion decision context to find the person-level prohibition.
Reduced redundancy; no change to the operative rule.

**minimum_closure_condition:** Either the explicit "org-level only, never person-level"
phrase is retained inline (even as a parenthetical), or the pointer to the LinkedIn/org-
motion decision context is explicit about where the person-level constraint lives.

**next_authorized_action:** Advisory; no urgency. Addressable at next scan spec touch.

---

## No Finding: Grading Rubric Standing Rule Change

The grading rubric's shift from "persistence verdict is not graded against realized outcome"
to "graded against the evidence in its information set, not against the realized outcome
label alone" was scrutinized adversarially. This change is logically necessary under the
2026-06-23 semantics: if durable is now callable at t=0 when a durability basis is in the
information set, a grader must be able to assess whether the durability basis was correctly
identified and named. The old rule ("structurally, not graded, because backtest amputates
the monitoring window") was correct only under the old "earned-by-monitoring" definition.

The new rubric explicitly prohibits hindsight outcome-label matching ("MAY NOT grade a
transient label against a realized durable outcome by label match alone") while enabling
evidence-basis grading. This is a correct adaptation to the new semantics. No finding.

## No Finding: CSB, Capture, and Projection Over-Propagation

All three surfaces correctly updated:
- CSB prompt prohibits emitting `durable/transient/manufactured demand-state verdict`; the
  three new handoff fields (`durability_projection_evidence_or_gap`,
  `decay_lifespan_evidence_or_gap`, `manufactured_hype_dedup_risk`) correctly preserve
  evidence without calling the verdict.
- CSB dispatch rules correctly passes durability evidence/decay discriminators through;
  states explicitly the gate-run "does not itself emit the durable/transient verdict."
- Capture obligation contract correctly changed from "never a verdict" to "can support or
  falsify a later durability projection, but never a verdict."
- Projection doctrine correctly extended its label prohibition to include `durable`,
  `transient`, `manufactured`, `weak`, `strong`.

No finding.

## No Finding: Proof Confusion

No surface in the 15-file patch set implies strict proof of demand. Language consistently
uses "call," "basis," "projection," "evidence," and "named basis." The buyer-proof packet
and scan spec explicitly distinguish a demand-state call from validation or buyer-proof
evidence. No finding.

## No Finding: Manufactured-Hype Dedupe Gap

Manufactured demand detection correctly updated (transient-default/earned-durable → calling-
sequence projection). The CSB prompt adds explicit dedupe-risk handoff. No gap. No finding.

## No Finding: Prompt/Overlay Leakage

No `jb` mechanics, model recommendation, readiness claim, or forbidden runtime-model
routing found in the 15-file patch. No finding.

---

## Summary Verdict

The 2026-06-23 projection-semantics doctrine change is coherently propagated across the
15 directly touched files. The semantic content is correct: durable is properly re-encoded
as a forward projection call with a named evidence basis; transient correctly denotes strong
current-window demand without a durability call; weak/attention-only signals are explicitly
excluded from the transient bucket across all surfaces that matter.

**Two material defects require owner decision before confident merge:**

| Finding | Severity | One-Line Summary |
|---------|----------|-----------------|
| AR-01 | Major | C3 Inputs prose ends mid-sentence at "the **integrity**"; integrity disposition and persistence-axis discriminator findings deleted from prose but retained in spec_handoff YAML. |
| AR-02 | Major | 2026-06-23 DCP receipt missing `stale_language_search_result` and `intentionally_not_updated`; fragrance satellite skeleton line 279 has active stale `transient-default` outside the search scope. |
| AR-03 | Minor | C3 `## Source-Read Ledger` heading deleted; 5 source-read bullets orphaned between spec_handoff and Claim Classification. |
| AR-04 | Minor | Scan spec `## 7. Reconciliation Note` heading deleted; content present but unnumbered. |
| AR-05 | Minor | Adjudication Q0 Refined note lacks `(clarified 2026-06-23)`; "earns the upgrade to durable" framing survives without annotation. |
| AR-06 | Minor | Scan spec LinkedIn org-motion person-level guardrail removed from inline statement. |

**Residual risks / test gaps not captured as findings:**
- The DCP receipt's `related_triggers: [architecture_doctrine]` signals architectural
  surfaces may also carry stale language. A repo-wide stale-language search (including
  `orca/product/satellites/` and any conductor/consolidation-map files that reference
  the old transient/durable vocabulary) would close this risk; the current receipt does
  not demonstrate it was run.
- The satellite skeleton's `transient-default` (AR-02 supporting evidence) is the only
  confirmed out-of-scope stale hit found; other satellite files and architectural surfaces
  were not exhaustively searched in this review.

---

## Review-Use Boundary

This review is decision input for the owner or authorized decision-maker. It is not
approval, validation, readiness evidence, buyer-proof evidence, source promotion,
mandatory remediation, merge authorization, or executor-ready instruction. Only a
separately authorized patch, acceptance, lifecycle, or implementation lane can make
remediation mandatory or executor-ready.

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/demand_read_projection_semantics_propagation_adversarial_review_v0.md
  review_location: filesystem_output
  commit_reviewed: eca296145ac395e33b6b9c9928e4c96b29566f9d
  de_correlation_bar: cross_vendor_discovery
  reviewed_by: claude-sonnet-4-6
  authored_by: OpenAI / GPT-family Codex lane
  findings_count:
    major: 2
    minor: 4
    critical: 0
  no_finding_checks:
    - over_propagation
    - proof_confusion
    - grading_confusion
    - manufactured_hype_dedupe_gap
    - prompt_overlay_leakage
  merge_block: false
  owner_decision_requested: true
  note: >
    AR-01 and AR-02 are major findings. AR-01 is a patch-artifact sentence truncation
    correctable with a single prose repair. AR-02 requires the owner to decide between
    patching the satellite skeleton now vs. adding an explicit intentionally_not_updated
    deferral and populating the stale_language_search_result field. Neither finding
    asserts a merge block; that is an owner decision.
```
