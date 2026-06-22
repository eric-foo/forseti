# Scanning Intelligent Walk MGT Operating Model — Delegated Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial artifact review report
scope: >
  Durable review report for the delegated review-and-patch commission on
  orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md.
  Records findings, unified diff, per-change citations, controller verdict,
  residual risk, validation/readback evidence, and Chief Architect adjudication packet.
use_when:
  - Chief Architect adjudicating the delegated review-and-patch diff and verdict.
  - Checking what was changed, why, and what remains for CA decision.
authority_boundary: retrieval_only
reviewed_by: claude-sonnet-4-6 (Anthropic)
authored_by: unrecorded (OpenAI / GPT-family Codex lane)
de_correlation_bar: cross_vendor_discovery
```

---

## 1. Commission, Lane Binding, and Actor/Model-Family Receipt

**Commission prompt:**
`docs/prompts/reviews/scanning_intelligent_walk_mgt_delegated_adversarial_artifact_review_and_patch_prompt_v0.md`

**Lane binding:**
- overlay_status: `provisional_opt_in` (`.agents/workflow-overlay/delegated-review-patch.md`)
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`
- review_lane: `workflow-adversarial-artifact-review` (non-code artifact)
- mode: `base-subagent`

**Actor / model-family receipt:**

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT-family Codex lane
  controller_model_family: Anthropic / Claude (claude-sonnet-4-6)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: repo
  de_correlation_status: satisfied
```

De-correlation: author is OpenAI/GPT-family; controller is Anthropic/Claude. Different vendor/model lineage. Cross-vendor discovery bar satisfied. No `Recommended model` block — this is a who-constraint only, not a performance recommendation.

---

## 2. Source Context Status and Target Hash Verification

**Target hash verification:**
```
pinned:   35E57952D9092F5B91E67BDB43FDD4EA5FAE6006D07CF47D3F0B54A41374BA74
observed: 35E57952D9092F5B91E67BDB43FDD4EA5FAE6006D07CF47D3F0B54A41374BA74
status:   MATCH — target is not stale
```

**Branch / commit:** `codex/screening-read-service-build` (HEAD is later than `60a69dd` per commission note; target hash matched pre-patch, confirming integrity.)

**SOURCE_CONTEXT_READY** — all required authority sources loaded.

**Source-read ledger:**

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` | Agent behavior kernel; overlay pointer | Supplied in session context |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Read |
| `.agents/workflow-overlay/delegated-review-patch.md` | Governance contract for this commission | Read |
| `.agents/workflow-overlay/review-lanes.md` | Review lane authority, severity labels | Read |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy, conflict rules | Read |
| `.agents/workflow-overlay/source-loading.md` | Source-loading budgets | Read |
| `.agents/workflow-overlay/validation-gates.md` | Validation gate requirements | Read |
| `.agents/workflow-overlay/safety-rules.md` | Forbidden drift, scope discipline | Read |
| `docs/decisions/orca_mini_god_tier_doctrine_v0.md` | MGT accepted-residuals contract | Read |
| `docs/decisions/orca_venue_registry_rejection_decision_v0.md` | Rejected shapes this model must not reintroduce | Read |
| `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` | Dry rule, Walker Equipment Kit, source of the ordinary stop rule | Read |
| `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` | Adjacent scan method (PROPOSED); alignment check | Read |
| `orca/product/spines/scanning/admissibility_checkability/orca_demand_scan_gate_adjudication_packet_v0.md` | Pipeline context, gate architecture decision | Read |
| `docs/decisions/screening_reddit_read_route_decision_v0.md` | Reddit source-family restriction (build wired) | Read |
| `docs/workflows/screening_read_service_build_receipt_v0.md` | Screening-read service boundary | Read |
| **TARGET** `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | Subject of review | Read (and patched) |

**Dirty-state allowance:** The target file is the only modified file under this commission. No unrelated dirty or untracked files were inspected or patched. All other sources were read-only.

**Skills invoked (REFERENCE-LOAD then APPLIED):**
- `workflow-delegated-review-patch` — governance contract (loaded; applied for receipt and adjudication framing)
- `workflow-deep-thinking` — reasoning discipline (loaded; applied for failure mode framing)
- `workflow-adversarial-artifact-review` — review method (loaded; applied for two-phase correctness + friction review)

---

## 3. Findings — Ordered by Severity

### MAJOR — MJR-01: Branch-aware pivot stop conditions depend on unguaranteed caps

**Finding ID:** MJR-01
**Phase:** correctness
**Target:** `[scan-mgt-model]`
**Location:** "Branch Decay, Pivot, And Stop" section, paragraph beginning "For ordinary vertical walks…"
**Source authority:** VEG Walker Equipment Kit (Step 4 / per-move self-check); `docs/decisions/orca_venue_registry_rejection_decision_v0.md` (Shape C: walk runs only inside an authorized batch screen; no standing crawler).

**Artifact evidence:**
The branch-aware pivot mechanic fires when a scan is "explicitly declared MGT/intelligent-walk" and allows continuing to a "declared or freshly surfaced frontier" while "the run remains inside caps." The stop conditions list includes "the run budget, cap, or source-policy boundary is reached" and "all declared and discovered frontiers have decayed to minimal or zero expected value." The word "discovered" means frontiers may be generated during the walk through pointers and cross-references surfaced by each read.

**Strongest reading in defense:** The artifact says "the run remains inside caps" as a condition for pivot continuation, implying caps must exist. The VEG's Walker Equipment Kit has a per-move cap check ("(c) move cap reached -> STOP NOW"). These together suggest caps are assumed.

**Why defense fails:** "The run remains inside caps" is conditional — it states what happens IF caps are set, not that caps MUST be set. Neither the target nor the commission language mandates that a cap be included in an MGT scan authorization. A scan commission without a stated cap would have no triggering condition for stop condition 2 ("run budget or cap reached") and would rely solely on the frontier-exhaustion stop condition (stop condition 3). That condition contains a discovery-regeneration gap: if each pivot step surfaces new "discovered" frontiers (via pointers, cross-references — both of which the Frontier Selection section explicitly names as frontier sources) faster than existing frontiers decay, the "all frontiers decayed" condition is never reached. This is functionally identical to the generic crawler pattern the artifact explicitly forbids.

**Impact:** Without mandatory caps, a scan prompt invoking the MGT operating model could produce an indefinitely running walk, violating the bounded-walk claim and reopening the rejected generic-crawler shape.

**Blocked state:** Not blocked (wording deficiency, patchable).

**Minimum closure condition:** The artifact must either (a) explicitly state that a run cap (move budget or equivalent) is required for any MGT invocation, or (b) define a default cap that applies when none is stated.

**Next authorized action:** Chief Architect adjudication of the proposed patch (see diff below).

**Patched:** YES — see diff hunk 1.

---

### MAJOR — MJR-02: "Explicitly declared" MGT trigger lacks authorization definition

**Finding ID:** MJR-02
**Phase:** correctness
**Target:** `[scan-mgt-model]`
**Location:** "Branch Decay, Pivot, And Stop" section, same paragraph as MJR-01.
**Source authority:** `AGENTS.md` kernel ("The operating vocabulary here is **bounded intelligent walk**" ... avoiding shapes that are explicitly out of bounds); VEG Step 4 amendment ("explicitly declared MGT / intelligent-walk scan") — the VEG uses the same phrase but also does not define it.

**Artifact evidence:**
The artifact creates a bifurcation: ordinary walks use the standard dry rule; "explicitly declared MGT / intelligent-walk scans with multiple frontiers" use the branch-aware variant. However, the artifact provides no definition of what "explicitly declared" means in practice: who may declare, what authorization is required, or how the declaration is verified.

**Strongest reading in defense:** The target's opening section says "Scanning owns, inside an authorized run," and the status section says "MGT_TARGET_OWNER_INVOKED." These imply authorization is required. An authorized run presumably includes an explicit declaration.

**Why defense fails:** "Authorized run" and "explicitly declared MGT scan" are separable constraints. A scan can be authorized without being declared MGT. The target does not connect the MGT declaration to the authorization mechanism. Without this connection, any authorized scan could self-declare as MGT at runtime to access the branch-aware behavior, bypassing the standard dry rule without any additional operator intent. This is a runtime-assertion loophole: the walk itself could claim MGT status without the commission having intended it.

**Impact:** Future scan prompts could silently invoke MGT branch-aware behavior without operator intention, weakening stop conditions for any scan that asserts MGT status. The declaration is currently a soft runtime claim rather than a commission-bound gate.

**Blocked state:** Not blocked (wording deficiency, patchable).

**Minimum closure condition:** The artifact must define that an "explicitly declared" MGT scan is one whose authorizing commission document invokes this operating model by name; the declaration must appear in the commission, not be asserted at runtime.

**Next authorized action:** Chief Architect adjudication of the proposed patch (see diff below).

**Patched:** YES — see diff hunk 1 (same hunk as MJR-01).

---

### MINOR — MNR-01: Observation promotion trigger not specified, creating prompt-author gap

**Finding ID:** MNR-01
**Phase:** friction
**Target:** `[scan-mgt-model]`
**Location:** "Minimum Evidence, Not Quotas" section, before the observation schema.
**Source authority:** The artifact's own philosophy ("minimum evidence, not quotas") and the VEG Walker Equipment Kit ("YIELD CLASSES per move: CANDIDATE | EVIDENCE | INFLUENCE-OBS | VENUE-DRY | ACCESS-NOTE").

**Artifact evidence:**
The target specifies what fields are required when promoting a move note to an observation (the minimum schema). It does not specify when to promote — what makes a move-level signal worth elevating to an observation.

**Strongest reading in defense:** This is an intentional design choice. The "minimum evidence, not quotas" philosophy explicitly rejects fixed thresholds. The minimum schema documents what judgment produces, not what triggers it. Adding a promotion trigger could reintroduce the quota pattern the section opposes.

**Why defense is mostly correct but incomplete:** The design is correct for what it excludes (quotas). However, a prompt author designing a scan using only the target as a standalone source (per the `use_when`: "designing a scanning lane") has no guidance on when to promote. Without a promotion rationale, authors may either never promote (losing signal) or over-promote (inflating the observation log and defeating the "minimum" intent). The scan-core spec provides more detail but may not be in context for every prompt author.

**Impact:** Minor risk of inconsistent promotion practices across scan prompts; does not violate any boundary but could reduce inter-scan comparability.

**Optional hardening:** Add a brief promotion rationale sentence alongside the schema.

**Next authorized action:** Chief Architect may accept, modify, or reject this optional harden. It is not a blocker.

**Patched:** YES (as optional hardening) — see diff hunk 2.

---

## 4. Unified Diff

```diff
diff --git a/orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md b/orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
index fac1b5a2..34015426 100644
--- a/orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
+++ b/orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
@@ -137,6 +137,18 @@ branch; they do not automatically end the whole run while another declared or
 freshly surfaced frontier has non-trivial expected value and the run remains
 inside caps.

+A scan is **explicitly declared** MGT when the scan authorization or commission
+document invokes this operating model and the branch-aware rule by name. The
+declaration must appear in the authorizing commission, not be asserted at
+runtime by the walk itself. An authorized scan that does not carry an explicit
+MGT declaration uses the ordinary dry rule.
+
+A **run cap** (move budget, read limit, or equivalent) must be stated in any
+MGT scan commission. Caps are the primary enforcement mechanism that makes
+branch-aware pivot behavior bounded rather than open-ended. A scan commission
+without a stated cap does not qualify as a bounded intelligent walk under this
+model and must not invoke the branch-aware dry rule.
+
 ## Shared Vocabulary

 Source-family lanes should emit into this vocabulary instead of inventing
@@ -164,6 +176,8 @@ Quotas are collection hygiene, not inference. A scan may set collection
 coverage targets, but a quota does not decide whether demand is real, durable,
 manufactured, or action-worthy.

+Promote a move note to an observation when the signal is worth carrying for downstream gate or capture evaluation: it ties to a specific URL and a possible gate role, decision window, or candidate. Do not promote every observed item; do not suppress signal that may support a candidate entry.
+
 Minimum promotion from move note to observation:
```

---

## 5. Per-Change Source Citations

**Hunk 1a (MJR-02 — "explicitly declared" definition):**

Source: VEG Walker Equipment Kit, Step 4 amendment: "explicitly declared MGT / intelligent-walk scan: last two moves on the active branch both VENUE-DRY -> close that branch and pivot only if another declared or freshly surfaced frontier has non-trivial expected value; otherwise STOP NOW." The Kit uses "explicitly declared" as a modifier but does not define it. The patch closes this gap: the declaration belongs in the commission document, not the runtime walk assertion. Source: `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md`, Step 4 and Walker Equipment Kit.

**Hunk 1b (MJR-01 — mandatory cap requirement):**

Source 1: VEG Walker Equipment Kit, per-move self-check (c): "move cap reached -> STOP NOW" — caps are already the operative stop trigger in the VEG; the patch makes this mandatory for MGT commissions rather than contingent on the commission having set one.
Source 2: Venue registry rejection decision, Shape C: "a thin exploration procedure... runs ONLY inside an authorized batch screen: it starts when the screen starts and stops when the screen stops." Caps are the mechanism that makes "starts when the screen starts and stops when the screen stops" enforceable for multi-frontier walks. Source: `docs/decisions/orca_venue_registry_rejection_decision_v0.md` and `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` (Step 4 stop rule).

**Hunk 2 (MNR-01 — observation promotion rationale):**

Source: Target artifact's own "Minimum Evidence, Not Quotas" section: "A scan may set collection coverage targets, but a quota does not decide whether demand is real." The added sentence operationalizes the "minimum evidence" philosophy by naming the positive promotion criterion (signal worth carrying for downstream evaluation) alongside the negative criterion (not every move; not suppressed signal). No external authority required; the sentence derives from the artifact's own stated philosophy.

---

## 6. Controller Verdict and Residual-Risk Note

**Verdict:** PATCH_APPLIED — two major findings addressed by bounded wording additions; one minor finding addressed as optional hardening.

The target artifact is structurally sound. It correctly distinguishes bounded intelligent walk from generic crawling through stop conditions, hard boundaries, screen-light vocabulary, and explicit non-claims. No design-level problem was found that would require NEEDS_ARCHITECTURE_PASS; both major findings were patch-level wording deficiencies.

**Residual risk after patching:**

1. **"explicitly declared" declaration form not specified.** The patch states that the declaration must appear in the authorizing commission document and invoke this operating model by name, but does not prescribe a specific field name or format. Future commission prompts may declare MGT in varying ways. The CA may wish to specify a standard field (e.g., a YAML field `walk_mode: mgt_intelligent_walk`) in a future prompt template, but this goes beyond the target artifact's scope.

2. **Cap value not defaulted.** The patch requires that a cap must be stated but does not specify a default value when none is supplied. If a commission author forgets to state a cap, the prohibition ("must not invoke the branch-aware dry rule") is the enforcement, but there is no fallback default. A CA decision on a standard default cap (e.g., "20 moves") could further strengthen this, but is off-scope for the target artifact.

3. **Scan-core spec alignment.** The Demand Scan-Core Spec (`PROPOSED_PENDING_ADJUDICATION`) is the downstream consumer of the observation schema. If the spec is adjudicated with changes to the observation schema, the target's "Minimum Evidence" section may drift. This is already named in `stale_if` and is an accepted residual of the operating model.

4. **One non-independent sliver.** The controller authored the patched lines (hunk 1a, 1b, hunk 2). Per the delegated-review-patch convention, the CA should verify these specific additions mechanically (read the patched paragraphs; confirm they close MJR-01 and MJR-02 without introducing new scope or forbidden language). A full re-scan of the patched artifact for the controller's own blind spots in these specific lines is the one non-independent residual.

---

## 7. Validation/Readback Status

**Targeted readback of patched sections:** Run. Lines 140–150 (MJR-01/02 fix) and lines 179 (MNR-01 fix) were read back from the patched file. Both patches appear correctly in context with no formatting errors or unintended changes to surrounding text.

**`git diff --check`:** Exited 0. No whitespace errors.

**Stale language search:**

```
rg -n "generic crawler approval|standing monitor|standing registry|
packet-grade scanning|route binding by scanning|live scan authorization|
scan-core ratification|readiness|validation|ready|approved|authorized"
orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
```

Results: All hits fall in correct contexts (non-claims section, stop conditions, VEG walk reference, MGT status declaration, accepted residuals). No stale language introducing overclaims was found:
- "scan-core ratification" appears twice in non-claims (correctly denying it)
- "readiness" appears in non-claims and in the accepted residual row (correctly denying it)
- "authorized" appears in "authorized run," "authorized target," "authorized scan," "authorized commission" — all correct operational uses
- "standing monitoring" appears in a stop condition (fires a stop, not a standing commitment)
- "generic crawler approval," "packet-grade scanning," "route binding by scanning," "live scan authorization," "standing registry" — NOT FOUND

---

## 8. Off-Scope Flags

**OFF-SCOPE-1:** The Demand Scan-Core Spec's observation schema (`orca_demand_scan_core_spec_v0.md`) has a richer `observation_id` / `gate_family` / `origination_ref` schema than the minimum schema in the target. As the scan-core spec moves from PROPOSED to adjudicated, the target's minimum schema should be reconciled for consistency. This is off-scope for the current patch (scan-core spec is read-only context). Routing: commissioning CA lane at scan-core adjudication time.

**OFF-SCOPE-2:** The VEG's Walker Equipment Kit uses the phrase "explicitly declared MGT / intelligent-walk scan" but — like the target — does not define the declaration mechanism. The patch here defines the mechanism in the target; a parallel clarification in the VEG's Step 4 or Walker Equipment Kit would make the definition discoverable from both sources. This is off-scope (VEG is read-only context). Routing: VEG maintenance, next amendment cycle.

**OFF-SCOPE-3:** The "run cap" requirement is now stated in the target, but no standard cap value or cap-field naming convention exists for MGT scan commissions. A future scan prompt template could define this convention. Off-scope for this artifact. Routing: prompt template registry at first MGT commission authoring.

---

## 9. Chief Architect Adjudication Packet

```yaml
ca_adjudication_packet:
  controller_verdict: PATCH_APPLIED
  de_correlation_bar_claimed: cross_vendor_discovery
  de_correlation_satisfied: true
  diff_and_verdict_status: claims_to_adjudicate_not_premises_to_inherit

  proposed_changes:
    - change_id: C1
      finding: MJR-01
      location: "Branch Decay, Pivot, And Stop — paragraph 3 (added after cap-mention sentence)"
      description: >
        Added mandatory run-cap requirement: "A run cap (move budget, read limit, or equivalent)
        must be stated in any MGT scan commission." Includes prohibition: a commission without
        a stated cap must not invoke the branch-aware dry rule.
      citation_sources:
        - VEG Walker Equipment Kit stop check (c): "move cap reached -> STOP NOW"
        - Venue registry rejection decision, Shape C: walk runs only inside an authorized batch screen
      intended_closure: Closes the loophole where capless MGT commissions could produce indefinitely running walks.
      ca_adjudication: accept / modify / reject

    - change_id: C2
      finding: MJR-02
      location: "Branch Decay, Pivot, And Stop — paragraph 2 (added after MGT dry rule sentence)"
      description: >
        Added definition of "explicitly declared" MGT: declaration must appear in the authorizing
        commission document and invoke this operating model by name; cannot be self-asserted at
        runtime by the walk.
      citation_sources:
        - VEG Walker Equipment Kit Step 4: uses "explicitly declared" without defining it
        - AGENTS.md kernel: "bounded intelligent walk" operates inside an authorized run
      intended_closure: Closes runtime-assertion loophole; requires declaration to be commission-bound.
      ca_adjudication: accept / modify / reject

    - change_id: C3
      finding: MNR-01 (optional hardening)
      location: "Minimum Evidence, Not Quotas — added sentence before observation schema"
      description: >
        Added a promotion rationale: "Promote a move note to an observation when the signal is worth
        carrying for downstream gate or capture evaluation: it ties to a specific URL and a possible
        gate role, decision window, or candidate. Do not promote every observed item; do not suppress
        signal that may support a candidate entry."
      citation_sources:
        - Target artifact's own "Minimum Evidence, Not Quotas" section philosophy
      intended_closure: Reduces prompt-author ambiguity about when to promote without introducing a quota.
      ca_adjudication: accept / modify / reject (optional; CA may reject without requiring a finding-closure note)

  rejected_or_off_scope_findings:
    - finding: Source-family adapter rule adequacy
      status: no_finding — the normalization correctly preserves local restrictions; "local restrictions always carry" is enforceable
    - finding: Capture request not_requested field enforceability
      status: no_finding — hard boundaries section is the normative enforcement; not_requested is correct advisory documentation
    - finding: Gate packaging inference vs quotas
      status: no_finding — gate packaging correctly frames scanning as supplying inputs, not replacing inference
    - finding: Non-claims adequacy
      status: no_finding — non-claims section is comprehensive and covers all required exclusions
    - finding: Accepted residuals against Mini God Tier doctrine
      status: no_finding — all 7 residuals carry the required four components (named, bounded, why acceptable, remaining risk, upgrade trigger)

  off_scope_flags:
    - OFF-SCOPE-1: Scan-core spec schema reconciliation (at adjudication time)
    - OFF-SCOPE-2: VEG Walker Equipment Kit "explicitly declared" clarification (next VEG amendment)
    - OFF-SCOPE-3: Standard cap-field naming convention for MGT commissions (prompt template registry)

  non_independent_sliver:
    - scope: The controller's own added lines (C1, C2, C3)
    - recommended_ca_check: >
        Read patched paragraphs (lines ~140–150, line ~179 in the patched file).
        Confirm they close MJR-01 and MJR-02 without introducing new scope creep,
        forbidden language, or crawling-adjacent behavior.
    - class_sweep_for: capless-crawl loophole, runtime self-declaration, quota-by-back-door

  residual_risk_named:
    - Declaration form not standardized (form-only, not definition-only)
    - Cap value not defaulted (prohibition without fallback)
    - Scan-core spec alignment deferred
    - Non-independent sliver on controller-authored lines

  ca_authority_statement: >
    The diff, citations, and verdict above are decision input only. The CA
    reserves final authority to accept, modify, or reject any change at
    discretion, even an individually defensible one. No change is kept until
    the CA adjudicates it. The delegated review discharges a cross_vendor_discovery
    pass for the patched artifact (C1, C2, C3 plus the full-artifact adversarial
    discovery above). The one non-independent sliver (controller's own added lines)
    requires mechanical CA verification per the class sweep above.
```

---

## 10. Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations, and verdict are claims to adjudicate, not premises to inherit.

This report is not owner acceptance, validation proof, readiness, scan authorization, capture authorization, crawler approval, registry approval, monitor approval, source-access authorization, buyer proof, or permission to keep any patch without Chief Architect adjudication.

`reviewed_by: claude-sonnet-4-6 (Anthropic)`
`authored_by: unrecorded (OpenAI / GPT-family Codex lane)`
`de_correlation_bar: cross_vendor_discovery`
`ca_adjudication_required: yes — all three proposed changes (C1, C2, C3)`

---

## Delegated Artifact Review Return (for Home Model)

```text
DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Commission: scanning_intelligent_walk_mgt_delegated_adversarial_artifact_review_and_patch_prompt_v0
Target: [scan-mgt-model]
  orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md

Bounded patch scope: wording, boundaries, fields, accepted residuals, non-claims, or
source-loading surface in the target file only.

Controller: Anthropic / Claude (claude-sonnet-4-6) — de-correlated from
OpenAI / GPT-family Codex author. De-correlation bar: cross_vendor_discovery.

Findings:
- MJR-01 (major/correctness): Branch-aware pivot stop conditions depend on unguaranteed caps.
  Without a mandatory cap requirement, the frontier-exhaustion stop condition has a
  discovery-regeneration loophole equivalent to a generic crawler. PATCHED (hunk 1b).
- MJR-02 (major/correctness): "Explicitly declared" MGT trigger is undefined, allowing any
  scan to self-assert MGT status at runtime and bypass the standard dry rule. PATCHED (hunk 1a).
- MNR-01 (minor/friction): Observation promotion trigger not specified; prompt-author gap on
  when to promote a move note. PATCHED as optional hardening (hunk 2).

No critical findings. No NEEDS_ARCHITECTURE_PASS. Artifact is structurally sound.

Proposed diff: see Section 4 above.
Citations: see Section 5 above.

Verdict: PATCH_APPLIED — two major wording deficiencies closed; one minor optional hardening applied.

Residual risk: declaration form not standardized; cap value not defaulted; scan-core spec
alignment deferred; non-independent sliver on controller-authored lines.

CA adjudication required: All three proposed changes (C1, C2, C3).
Non-independent sliver check: Read patched lines ~140–150 and ~179 to verify no scope creep,
forbidden language, or capless-crawl / runtime-assertion loophole was introduced.
```
