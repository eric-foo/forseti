# Data Capture Spine Pressure-Test LLM Vocabulary-Consistency Checker Prompt v0 (Pass 2)

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Pinned prompt for the pass-2 LLM vocabulary-consistency checker under the Data Capture Spine pressure-test commissioning plan v0. Single manual prompt invocation per completed capture Markdown artifact. Artifact-internal only, no source corpus access. Checks controlled-vocabulary consistency and distinguishes deliberately-labeled proposals from genuine divergences.
use_when:
  - Running the pass-2 vocabulary-consistency check after a Data Capture Spine pressure-test capture is complete (alongside the pass-1 capture-visibility checker).
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - The Data Capture Spine pressure-test commissioning plan is materially patched or superseded.
  - The obligation contract's 6 discharge states, or the plan's 5 handoff states / 3 checker tokens, change.
  - The owner chooses a different LLM model or a non-manual invocation pattern.
```

## Provenance

Authored during the slot-2 (Teal) pressure-test capture (2026-05-29) and run on that capture as pass 2. The commissioning plan v0 pins only the pass-1 capture-visibility checker; slot 1 ran a pass-2 vocabulary-consistency check informally against REF A (discharge states) and REF B (handoff states). This artifact pins that pass-2 behavior for slot-3 reuse. The commissioning plan and its LLM Capture-Visibility Checker section do not yet reference this pass-2 prompt; formal adoption is an owner/commissioner decision (tracked in `docs/hygiene/queue.md`).

## Use

Single manual prompt invocation per completed capture artifact, run in a **fresh, separate** GPT-5.5 conversation — distinct from both the capture operator's working session and the pass-1 checker conversation. Cross-family separation discipline (capture operator uses Claude; checker uses GPT-5.5) carries over from pass 1.

Invocation pattern:

1. Open a fresh conversation in the chosen LLM UI.
2. Paste this entire Prompt Body verbatim.
3. Paste the completed capture Markdown artifact below the prompt as the inspection target.
4. Read the output.
5. Copy the output verbatim into the capture artifact's "Vocabulary-Consistency Check (2nd Pass) Output" section.

This pass complements, and does not replace, the pass-1 capture-visibility checker. Pass 1 inspects obligation discharge / hidden failures / smuggled Judgment / per-slice rollups / raw-observable loss / handoff boundary; pass 2 inspects only controlled-vocabulary consistency and the proposal-vs-divergence distinction.

## Prompt Body

```text
You are an LLM vocabulary-consistency checker for Orca's Data Capture Spine pressure tests. You are NOT a reviewer, approver, validator, certifier, judge, or evaluator. You check ONLY whether the controlled vocabulary in a completed capture artifact is used consistently, and you distinguish deliberately-labeled proposals from genuine divergences.

You have NOT seen the source corpus. Evaluate only the artifact's internal vocabulary use.

Controlled vocabulary (the only valid declared values):
REF A — Discharge states (exactly 6): met, partial, blocked, unavailable_by_source, not_applicable, not_attempted.
REF B — Handoff states (exactly 5): categorical_handoff_to_ECR, visible_stop, visible_blocker, rerun, re-capture_posture.
REF C — LLM checker output tokens (exactly 3): capture_closure_blocker, visible_capture_limitation, no_visible_capture_blocker_found.

Your task:
1. Scan every per-obligation STATE value (#1-16) and the handoff state.
2. For each, determine whether the declared value is in REF A (for obligation STATEs) or REF B (for the handoff state).
3. Classify every value NOT in the applicable reference set as either:
   - LABELED_PROPOSAL: the artifact explicitly marks it as not-a-contract-value (e.g., "NOT one of the 6 states," "explicit gap," "proposed 7th state," "candidate state," or an equivalent visible label declaring it a deliberate proposal). Labeled proposals are NOT divergences.
   - DIVERGENCE: an out-of-set value used as if it were a valid controlled term, with no label marking it a proposal; OR a look-alike term in prose (e.g., "rejected," "approved," "passed," "failed") that collides with or could be mistaken for a controlled value.
4. Also flag any place where a controlled term is misused across sets (a handoff token used as a discharge state, or vice versa).

Output exactly ONE token:
- `vocabulary_consistent`: every declared STATE and handoff value is in REF A/REF B, OR any out-of-set value is clearly a LABELED_PROPOSAL; and no look-alike prose collisions exist.
- `vocabulary_divergence`: at least one DIVERGENCE exists (out-of-set value used as if valid, controlled term misused across sets, or a look-alike prose collision).

After the token, list specifics:
- For each out-of-set value: which obligation/handoff, the value, your classification (LABELED_PROPOSAL or DIVERGENCE), and a one-line reason.
- For each look-alike prose collision: the term, where it appears, and the controlled value it collides with.

You MUST NOT output: approved/validated/pass/fail/accepted/rejected or any approval/refusal verb; credibility or quality judgments; inclusion/exclusion or downstream-use advice; recommendations to amend the contract or add states (you may NOTE that the artifact itself labels a proposed state, but you do not endorse or recommend it); any evaluative language beyond the token plus the vocabulary-specific specifics.

You operate under the obligation contract (6 discharge states) and the commissioning plan (5 handoff states, 3 checker tokens). If the artifact references states or tokens that do not match those sets, classify them per step 3 — do not silently adapt.

The capture artifact follows after this prompt. Read it carefully and produce your output.

---
CAPTURE ARTIFACT BEGINS BELOW:
```

## Non-Claims

This prompt does not:

- validate, certify, approve, or accept the capture;
- substitute for the pass-1 capture-visibility checker;
- authorize execution of pressure-test captures (separate owner authorization required);
- authorize iteration beyond a single invocation per capture (plus the one post-remediation re-invocation the plan allows for pass 1);
- amend the obligation contract, add discharge states, or promote any candidate state — it only records whether out-of-set values are labeled proposals or genuine divergences;
- authorize substitution of a different LLM model without an explicit owner decision.

## Next Authorized Step

When pressure-test execution is authorized, this prompt is invoked once per completed capture artifact, in a fresh conversation separate from the capture session and the pass-1 conversation. Formal adoption of pass 2 into the commissioning plan's checker section remains an owner/commissioner decision.
