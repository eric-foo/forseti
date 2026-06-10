# Judgment Spine Pre-Sale Execution Evidence Tier Policy Patch — Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca adversarial artifact review report
scope: Read-only adversarial artifact review of the pre-sale execution evidence-tier policy patch and its downstream wording in four target files.
use_when:
  - Deciding whether the pre-sale subscription/manual/chat default and API-optional routing patch is safe to keep as doctrine.
  - Checking whether raw-API/harness plumbing was banned, made default, or weakened by the patch.
  - Checking whether advisory subscription/manual/chat use was overpromoted into gate-clearing evidence.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
input_hashes:
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: 39A65D04D71A348C7E2C3075512F1BED335F922270ED1E0497A7F98FA48745ED
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 0EA6D4C180CD36AF6611E42BFEAB92A576C9D0311EE98417CBB5CFFC33776BF5
  docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md: 96C498C6583CF10BE9AA0F7A3DF4043CDB1B389A96A5DB723A21E69C11A536F8
branch_or_commit: main @ 392f7935c029
```

## Commission

Bounded read-only adversarial artifact review of the pre-sale execution
evidence-tier policy patch, commissioned by
`docs/prompts/reviews/judgment_spine_pre_sale_execution_evidence_tier_policy_patch_adversarial_artifact_review_prompt_v0.md`.
Output mode: `review-report` (filesystem-output to this path). The review is
docs-only and read-only. It does not patch files, run any model, authorize any
call, or claim validation, fixture admission, product proof, or judgment
quality.

Patch intent under review:

- subscription/manual/chat execution is the default pre-sale path when adequate
  for advisory learning, demos, scouting, buyer conversation, or owner readback;
- raw API and harness execution remain in-bounds as optional gate-bearing
  plumbing when explicitly accepted for stricter provenance;
- no-case smoke tests remain optional plumbing and permanently non-gate-clearing;
- subscription/manual/chat output is not automatically gate-clearing;
- no runtime code, provider/model call, scoring, validation, fixture admission,
  ledger freeze, product proof, or judgment-quality claim is made.

## Target

Four hash-pinned review targets in `C:\Users\vmon7\Desktop\projects\orca`,
verified against the active dirty/untracked workspace at the expected revision:

| Target | Role | Verified SHA-256 |
| --- | --- | --- |
| docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md | Orca decision record (the patch) | `39A65D04…45ED` |
| docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md | Harness v0.14 execution contract (paired) | `33012246…193C` |
| docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md | Harness v0.14 smoke checklist (paired) | `0EA6D4C1…76BF5` |
| docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md | Orca decision record (concrete one-shot smoke authorization) | `96C498C6…36F8` |

Context-only source (source-access analogy, not a review target):
`docs/product/data_capture_source_access_method_plan_v0.md` (`1C20DA68…4EABB`).

Not in scope: full Judgment Harness review, product review, code/runtime
review, installed-copy/resolver review, or model-family recommendation. Runtime
code was inspected only to the extent of noticing whether a docs claim
mis-describes runtime behavior (none found).

## Authority And Source Hierarchy

Source hierarchy applied (from `.agents/workflow-overlay/source-of-truth.md`):
current-turn user instruction → `AGENTS.md` → `.agents/workflow-overlay/` →
`docs/`. Orca overlay owns lane names, severities, destinations, and gates;
reusable kernel skills supply mechanics only.

Bound authority used for strict findings:

- review lane: **adversarial artifact review** (read-only), report destination
  `docs/review-outputs/adversarial-artifact-reviews/`
  (`.agents/workflow-overlay/review-lanes.md`);
- severity set `critical | major | minor | optional` — bound by the commission
  prompt and permitted by `review-lanes.md` for finding priority only (no
  approval/rejection/readiness authority by themselves);
- output mode `review-report` with bound `required_output_path`
  (`.agents/workflow-overlay/prompt-orchestration.md`);
- doctrine-change propagation contract and receipt shape
  (`.agents/workflow-overlay/source-of-truth.md`);
- retrieval-header contract (`.agents/workflow-overlay/retrieval-metadata.md`);
- validation gates, incl. the doctrine-propagation and review-doctrine gates
  (`.agents/workflow-overlay/validation-gates.md`).

## Method And Gate Status

```yaml
deep_thinking: applied (workflow-deep-thinking reference-loaded, then applied to frame failure modes and decision criteria before findings)
adversarial_artifact_review: applied (workflow-adversarial-artifact-review reference-loaded, then applied after SOURCE_CONTEXT_READY)
source_context: SOURCE_CONTEXT_READY
trigger_gate: pass — commission explicitly names the adversarial artifact review lane
lane_collision: none — single non-code artifact-review lane; no code/installed-copy/postmortem/prompt-orchestration collision
artifact_role_preflight: pass — targets bound as Orca decision records / harness contracts; reviewer permission read-only
output_mode_preflight: pass — review-report + required_output_path bound; output path confirmed absent before write
validation_gates: applicable gates are advisory review gates only; this review claims no PASS/readiness/validation for the patch
hash_preflight: pass — all 12 listed authority + target hashes matched exactly; HEAD 392f7935c029; branch main
```

### Source-read ledger (dirty-state)

All review targets and three of the overlay authority files are **modified or
untracked** in the working tree (expected and allowed by the commission's
`dirty_state_allowed: yes`). Dirty state was used only for advisory critique of
the named hash-pinned content; it is **not** read as repo cleanliness,
source-of-truth promotion, validation, readiness, or acceptance. No strict
finding here depends on a dirty source whose status was not allowed; the
expected revision matched, so no `BLOCKED_SOURCE_REVISION_MISMATCH` /
`BLOCKED_DIRTY_SOURCE_UNDECLARED` applies.

## Deep-Thinking Framing — Failure Modes And Decision Criteria

The real question is not "is the patch nicely worded" but "does this routing
doctrine change open a path that a future agent could walk to a wrong, more
permissive outcome." The decisive failure modes for this patch are asymmetric:

1. **Over-promotion (most dangerous):** advisory subscription/manual/chat output
   silently becoming usable as a clean memorization-probe pass, blind-use
   authorization, fixture admission, product proof, or judgment-quality evidence.
   Criterion: advisory tier must carry an explicit, non-bypassable
   "cannot-clear-gate" boundary in every touched file.
2. **API-default regression:** "API is allowed" drifting into "API is required /
   sequenced for ordinary pre-sale work." Criterion: every file that mentions
   API must state it is optional, not default, and not mandatory for future
   probes/demos/scouts/readbacks.
3. **API-ban overcorrection:** the patch deprecating or invalidating the raw-API
   runner and smoke plumbing. Criterion: gate-bearing API evidence must remain
   available when explicitly authorized.
4. **Gate-bearing dilution:** the new boundary language weakening the structural
   no-tools / provenance bar. Criterion: tool-isolation, hidden-context, and
   prompt/response-hash requirements must be reaffirmed, not relaxed.
5. **Propagation/provenance drift:** a validation-philosophy doctrine change that
   touches paired files and a live-call authorization but leaves dependent
   provenance markers or recheck obligations unreconciled.

Anti-anchoring note: I did not assume the patch was correct because it is
recently authored or because the prompt frames it favourably. Each of the seven
commissioned surfaces was tested against the criteria above. The result is that
failure modes 1–4 are well-defended in the artifact text; the only live issues
are in failure mode 5 (provenance/propagation hygiene), and they are minor.

## Per-Surface Assessment

| # | Surface | Result | Evidence (anchor) |
| --- | --- | --- | --- |
| 1 | Correct tier separation | **Holds** | Policy `execution_evidence_tiers.tier_advisory_subscription_manual_chat.cannot_support_by_itself` lists clean memorization-probe pass, blind-use, fixture validation/admission, scoring readiness, product proof, judgment-quality; contestant contract "Runtime Hook Boundary" + "Pre-Sale Evidence Tier Boundary" reaffirm advisory ≠ gate-clearing. |
| 2 | No API-default regression | **Holds** | Policy "Decision" + "Routing Rule" (lightest tier first); Non-Claims "does not make raw API mandatory"; OpenAI decision "Pre-Sale Default Boundary" ("does not require future scouting, demonstrations, buyer conversations, or owner readbacks to use API"); contestant contract + checklist repeat "does not make raw API the default". |
| 3 | No API-ban overcorrection | **Holds** | Policy "preserves the raw-API runner and no-case smoke-test work as useful plumbing"; `tier_gate_bearing_execution_evidence.current_accepted_surface: raw API`; contestant contract keeps raw API as an accepted gate-eligible surface. |
| 4 | No-case smoke boundary | **Holds (with AR-01 provenance caveat)** | Policy `tier_no_case_smoke.permanently_non_gate_clearing: true`; checklist "permanently non-gate-clearing" + "optional plumbing… should not be selected merely because pre-sale work is underway"; OpenAI decision `authorization_scope: one_shot_no_case_smoke_test_only`, `relationship_to_pre_sale_default: optional_plumbing_not_default_path`, "No retry… authorized". Scope stays bounded; AR-01 affects only provenance freshness, not scope. |
| 5 | Gate-bearing evidence integrity | **Holds** | Contestant contract "Required Execution Fields", "Isolation Result Semantics", "Receipt Provenance Boundary", "Insufficient Evidence" unchanged; "Pre-Sale Evidence Tier Boundary" explicitly states "Gate-bearing claims still require structural evidence under this contract." No weakening of tool-isolation, hidden-context, endpoint, prompt-hash, or response-hash requirements. |
| 6 | Doctrine propagation + retrieval hygiene | **Mostly holds — AR-01, AR-02** | Policy carries a `direction_change_propagation` receipt (trigger `validation_philosophy`) covering controlling + downstream surfaces; retrieval headers are `retrieval_only` with no forbidden authority fields. Two minor defects: stale dependent provenance on the OpenAI authorization (AR-01) and a query-only `stale_language_search` (AR-02). |
| 7 | Claim discipline | **Holds** | All four targets carry explicit Non-Claims and the required boundary line "plumbing works only; not judgment quality." No file claims a live call happened, scoring, validation, fixture admission, readiness, or judgment quality. The OpenAI decision authorizes one *future* one-shot call (separately accepted), and does not execute it. |

## Phase 1 — Correctness Findings

### AR-01 — Pre-sale patch modified the smoke authorization's bound dependencies but did not reconcile its recorded provenance

```yaml
finding_id: AR-01
phase: correctness
severity: minor
artifact_role: Orca decision record (concrete one-shot no-case smoke authorization)
target: docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
anchor: header input_hashes (lines ~21-22) and branch_or_commit (line ~32); cross-ref policy Direction Change Propagation controlling_sources_updated (lines ~133-137)
source_authority: .agents/workflow-overlay/retrieval-metadata.md (input_hashes/branch_or_commit semantics); .agents/workflow-overlay/source-of-truth.md (doctrine-change propagation sufficiency)
```

**Artifact evidence.** The OpenAI smoke-authorization decision records
`input_hashes` for two files this patch modified:

- `no_case_smoke_test_authorization_checklist_v0.md: 7A17255422C546…A8B26D`
- `contestant_no_tools_execution_contract_v0.md: F46AA6A4003E20…BE5EB0F5`

Current verified content hashes are `0EA6D4C1…76BF5` (checklist) and
`3301224649…193C` (contestant contract) — both differ. The decision's
`branch_or_commit: main @ a7c3463658…` is also stale relative to the patch HEAD
`392f7935c029`, even though the decision contains a "Pre-Sale Default Boundary"
section expressing this patch's doctrine. The policy file's
`direction_change_propagation.controlling_sources_updated` lists this OpenAI
decision as updated.

**Requirement strained.** The decision's own `stale_if` includes "Any input
hash changes," and the doctrine-propagation contract requires touched downstream
surfaces to be reconciled (not merely listed). Either (a) the patch edited the
decision's prose but left its `input_hashes`/`branch_or_commit` frozen at the
pre-edit state, so its self-declared `stale_if` has fired without a recorded
recheck; or (b) the decision was not re-edited and the policy receipt's
`controlling_sources_updated` over-states what was reconciled. Both readings
point to the same gap.

**Impact.** Provenance/auditability only. This is a one-shot, permanently
non-gate-clearing smoke authorization; its `authorization_scope` and stop
conditions are unchanged, and the dependency edits were additive pre-sale-default
clarifications that *narrow* rather than expand the authorization. A future
operator obeying the decision's `stale_if` would recheck the current checklist
and contract and find the one-shot, non-gate-clearing scope intact. It does not
create a gate-clearing path, a new live-call authorization, an API default, or
advisory-as-gate-clearing — hence minor, not major. It is the most
decision-relevant finding because it sits on a live-call authorization record
where provenance accuracy matters most.

```yaml
minimum_closure_condition: >
  The OpenAI one-shot smoke authorization's recorded provenance is consistent
  with the patch state: its input_hashes for the checklist and contestant
  contract match current content (or an explicit recheck note records that the
  prior-version authorization still holds against the current versions), its
  branch_or_commit reflects the revision at which it was last materially touched,
  and the policy receipt's controlling_sources_updated reflects only what was
  actually reconciled.
next_authorized_action: >
  Owner/author decision to refresh the dependent provenance and confirm the
  one-shot authorization still holds, or to correct the policy receipt. No
  reviewer patching; no smoke run; this finding is decision input only.
red_green_proof_status: not_applicable (non-executable provenance/metadata finding)
patch_queue_routing: not authorized for this read-only lane
```

## Phase 2 — Friction Findings

### AR-02 — Policy propagation receipt records a `stale_language_search` query but no run/result

```yaml
finding_id: AR-02
phase: friction
severity: minor
artifact_role: Orca decision record (the patch)
target: docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
anchor: Direction Change Propagation -> stale_language_search (lines ~157-163)
source_authority: .agents/workflow-overlay/source-of-truth.md (receipt shape); paired exemplar in contestant contract (stale_language_search_result, lines ~373-380)
```

**Artifact evidence.** The policy file's `direction_change_propagation` receipt
provides a `stale_language_search` `rg` query across the five relevant files but
records neither that it was run nor any result. The paired contestant contract's
receipt demonstrates the stronger pattern: it carries both the query and a dated
`stale_language_search_result` ("Executed on 2026-06-01 …") describing what was
and was not found.

**Requirement strained.** The receipt shape in `source-of-truth.md` specifies
`stale_language_search: "<query or not_run + why>"`, so a bare query is within
the literal contract. But for a `validation_philosophy` doctrine change, a query
with no recorded outcome does not actually demonstrate that stale, contradictory,
or API-default language was checked and cleared across the propagation surfaces.

**Impact.** Auditability/friction only — it does not misroute the next decision,
because the substantive routing language in the five files is internally
consistent (verified during this review: no "API default/required/mandatory" or
"subscription/manual/chat gate-clearing" language was found in the patch text).
The cost is that a future reader cannot confirm from the receipt alone that the
stale-language sweep was performed.

```yaml
minimum_closure_condition: >
  The policy receipt's stale_language_search records either an executed result
  (what was searched and what was/was not found, like the paired contestant
  contract) or an explicit not_run + reason, so propagation auditability is
  demonstrated rather than asserted.
next_authorized_action: >
  Owner/author decision to record the search result or a not_run rationale in
  the receipt. No reviewer patching; decision input only.
red_green_proof_status: not_applicable (non-executable auditability finding)
patch_queue_routing: not authorized for this read-only lane
```

## Optional Hardening (non-required)

- `optional`: The two paired harness files and the smoke authorization could
  each carry a one-line "recheck on dependency change" pointer to the policy
  receipt, so the propagation chain is discoverable from any node. This is a
  convenience for future agents only; it is **not** a blocker, mandatory
  remediation, or readiness condition, and is out of the minimal scope of this
  patch.

## Not-Proven Boundaries And Strict-Only Notes

- This review does **not** assert that the patch is `validated`, `ready`,
  `approved`, or `PASS`. Those are strict lifecycle claims outside an
  adversarial artifact review's authority; the patch's own files correctly make
  no such claim.
- Model existence/availability of `gpt-5.4-mini` is the OpenAI decision's
  external-source claim (OpenAI docs, retrieved 2026-06-01). It was **not**
  independently verified here and is out of review scope (no model-family
  recommendation).
- The OpenAI decision's other `input_hashes` entries
  (`no_case_smoke_test_authorization_pending_parameters_v0.md`, the runner `.py`,
  `artifact-folders.md`, the post-patch recheck) were **not** re-verified: they
  are that decision's own provenance inputs, not pinned review targets, and the
  runner is runtime code excluded from this lane.

## Review-Use Boundary

These findings are decision input for the owner / Chief Architect only. They are
not approval, validation, readiness, acceptance, mandatory remediation, or
executor-ready patch authority. Nothing here authorizes editing any file, running
any model, or executing the authorized smoke test. Remediation becomes mandatory
or executor-ready only if a separately authorized patch, acceptance, or
implementation lane takes it up. AR-01 and AR-02 are both `minor`: they should be
fixed for provenance/auditability hygiene but do not block the patch's doctrine.

## Recommendation

The patch is **substantively sound** on all seven commissioned adversarial
surfaces: it separates advisory from gate-bearing tiers without over-promoting
advisory output, does not make API default, does not ban API, keeps no-case
smoke permanently non-gate-clearing and the OpenAI authorization bounded to one
shot, preserves the structural no-tools/provenance bar for gate-bearing
evidence, and maintains claim discipline. Two `minor` provenance/retrieval-hygiene
defects (AR-01, AR-02) are advisory and non-blocking. No `critical` or `major`
findings.

Required boundary: plumbing works only; not judgment quality.
