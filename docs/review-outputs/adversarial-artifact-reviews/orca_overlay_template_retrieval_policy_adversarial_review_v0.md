# Orca Overlay Template Retrieval Policy — Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the Orca overlay/template patch that replaced runtime model routing with template retrieval.
use_when:
  - Deciding whether to accept the Orca template-retrieval policy as overlay authority.
  - Tracing how runtime model routing was decoupled from Orca review and prompt lanes.
authority_boundary: retrieval_only
input_hashes:
  .agents/workflow-overlay/review-lanes.md: 0AF61CF297330C6D7AC59554F62BCAD268AC2EC359BA4947DD38CBAB7FF264ED
  .agents/workflow-overlay/prompt-orchestration.md: C0AEDBACB6E2FDE985132A1694F2FB142821B5BB1D6371B3BEA2541E0DFBFF84
  .agents/workflow-overlay/template-registry.md: 428334F41E3ECE7AEBD898C5858DB63C7B1F7374F481E9E86CA30BA7CA8C2D64
  .agents/workflow-overlay/artifact-roles.md: C8BD0DA4ACCECC2199E9FEED2A6C2BFBA617092E9A99A9D287AF86327C24DD7F
  docs/prompts/templates/README.md: 5BF41783F8F01B1ECB32D50D89B0FD8F1CD57FB28A3A6A67AE08A635E77EC2BC
  docs/prompts/templates/_generic/gpt_5_5_general_prompt_v0.md: 4BBFB9792C4BD7BC886AD8C883C8DE2C9E35FA73EBD8C6992C7FE7BACEFFCD9A
  docs/prompts/templates/_generic/claude_sonnet_4_6_general_prompt_v0.md: 8C3FE280E1B683B2C94852BBECED027E3F8C81F65BD7646FC0D608333ACC8F86
  docs/prompts/templates/_generic/claude_opus_4_7_adversarial_reasoning_prompt_v0.md: 53B7B386ADADDE0E8A75372AEA61C0A9E08B346CB3C8D52B1015E515CB54AE8D
  docs/prompts/templates/_generic/claude_opus_prompting_best_practices_v0.md: 887EA8569AFFE22344F446A9F2D7A41236D93B36F298F224C5A1515AB70327D5
  docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md: 9700D5935F820969BEC5FA897AAAB73A54BCC069EA4C50ADFE22EB231A0D24C1
  docs/prompts/templates/research/gpt_5_5_evidence_synthesis_v0.md: 6BB31C2D2C314AFC779E2FEEC062C34261342C61E6DEF4DC5B5D9A9CC03971BD
  docs/prompts/templates/review/adversarial_artifact_review_v0.md: 17188D11F4C151103CC746328D02F0DFC94FCF3AAD3F39714A510CEDBA5A60AA
  docs/prompts/templates/wrappers/thin_wrapper_v0.md: 7C449586BFBA073217438C11E5A9DCA57280DAC07892A6B8990BFE4941C7B4B6
```

## Review Target

The Orca overlay/template patch that replaced runtime model routing with prompt-template retrieval. In scope: the thirteen files listed under "Verified Hashes" plus the supporting overlay context required to confirm registry, source-loading, and discovery behavior.

Out of scope: installed workflow-kernel skill source, jb policy, runtime model selection, implementation work, and patch execution.

## Review Purpose

Decide whether the patch successfully removed Orca overlay runtime model-routing authority and replaced it with bounded prompt-template retrieval, without leaving stale executor-lane bindings, broken template-registry paths, hidden model-choice recommendations, review-lane contradictions, or prompt-authority leaks.

## Source Context Status

`SOURCE_CONTEXT_READY`.

`AGENTS.md` and `.agents/workflow-overlay/README.md` were read in the current task context. The two required workflow skills (`workflow-deep-thinking`, `workflow-adversarial-artifact-review`) were `REFERENCE-LOAD`ed before applying review. Required review targets and supporting overlay sources were loaded. All thirteen review-target SHA256 hashes verified against the values supplied in the prompt.

Dirty-state ledger. The git status snapshot at the start of the conversation marked the following review targets as in-scope patch artifacts:

- modified: `review-lanes.md`, `prompt-orchestration.md`, `artifact-roles.md`, `docs/prompts/templates/_generic/gpt_5_5_general_prompt_v0.md`, `docs/prompts/templates/research/gpt_5_5_evidence_synthesis_v0.md`, `docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md`, `docs/prompts/templates/review/adversarial_artifact_review_v0.md`, `docs/prompts/templates/wrappers/thin_wrapper_v0.md`;
- untracked (newly added): `.agents/workflow-overlay/template-registry.md`.

These are treated as in-scope patch artifacts per the prompt, not as already-accepted source-of-truth. Hashes match the supplied expected values, so the working-tree content is what was commissioned for review.

## Verified Hashes

| File | SHA256 | Expected | Match |
| --- | --- | --- | --- |
| `.agents/workflow-overlay/review-lanes.md` | `0AF61CF2…F264ED` | as supplied | yes |
| `.agents/workflow-overlay/prompt-orchestration.md` | `C0AEDBAC…DFBFF84` | as supplied | yes |
| `.agents/workflow-overlay/template-registry.md` | `428334F4…C2D64` | as supplied | yes |
| `.agents/workflow-overlay/artifact-roles.md` | `C8BD0DA4…24DD7F` | as supplied | yes |
| `docs/prompts/templates/README.md` | `5BF41783…7EC2BC` | as supplied | yes |
| `docs/prompts/templates/_generic/gpt_5_5_general_prompt_v0.md` | `4BBFB979…CCD9A` | as supplied | yes |
| `docs/prompts/templates/_generic/claude_sonnet_4_6_general_prompt_v0.md` | `8C3FE280…CC8F86` | as supplied | yes |
| `docs/prompts/templates/_generic/claude_opus_4_7_adversarial_reasoning_prompt_v0.md` | `53B7B386…4AE8D` | as supplied | yes |
| `docs/prompts/templates/_generic/claude_opus_prompting_best_practices_v0.md` | `887EA856…0327D5` | as supplied | yes |
| `docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md` | `9700D593…0D24C1` | as supplied | yes |
| `docs/prompts/templates/research/gpt_5_5_evidence_synthesis_v0.md` | `6BB31C2D…3971BD` | as supplied | yes |
| `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | `17188D11…A60AA` | as supplied | yes |
| `docs/prompts/templates/wrappers/thin_wrapper_v0.md` | `7C449586…1C7B4B6` | as supplied | yes |

All thirteen hashes match.

## Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `REFERENCE-LOAD` `workflow-deep-thinking` and `workflow-adversarial-artifact-review`.
3. `SOURCE-LOAD` thirteen review targets plus supporting overlay sources (`source-loading.md`, `retrieval-metadata.md`, `artifact-folders.md`, `source-of-truth.md`, `communication-style.md`, `safety-rules.md`, `validation-gates.md`, and the registered shared behavior contract `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`).
4. Verify SHA256 hashes of review targets.
5. Cross-check registry paths against the file tree (Glob confirms all ten template files under `docs/prompts/templates/`).
6. Grep the overlay and template tree for any retained model-routing language (`executor lane`, `reviewer model`, `runs on …`, `recommended model`, `model lane`, `model choice`, prior `gpt-5.3`/`gpt-5.4` identifiers).
7. Declare `SOURCE_CONTEXT_READY`.
8. `APPLY` deep-thinking discipline and adversarial artifact review against the loaded source context.
9. Write this durable report and return only the compact YAML summary.

Deep-thinking discipline status. `workflow-deep-thinking` instructions were applied as a private framing pass before findings were drafted. Anchoring on "the patch is fine because it adds disclaimers" was specifically tested against the failure modes named in the prompt (stale executor-lane bindings, hidden model-choice recommendations, prompt authority leaks).

## Executive Verdict

The patch achieves its primary aim. Runtime model-routing authority is removed from Orca overlay lane bindings, template retrieval is consistently framed as prompt posture rather than execution selection, every model-named template carries an explicit non-routing disclaimer, all registered template paths resolve to existing files, and the legacy alias is explicit and unambiguous. Source-loading, review-lane, prompt-validation, and retrieval-metadata gates are intact and consistent.

The friction findings are minor: a shortform-versus-full-form template-ID inconsistency between `review-lanes.md` and the registry, a coverage gap in the `template_retrieval_binding` block, an "executor lane" phrasing in the overlay README that now reads as a write-permission lane rather than a model-bound lane, and one model-target naming asymmetry for the `o3` template. None of these would cause a downstream Chief Architect to route a runtime model, miss a registered template, or misread review authority.

Recommendation: accept with friction. The minor items are worth a single hygiene pass but do not block use of the template-retrieval policy.

## Findings

### Critical

None.

### Major

None.

### Minor

#### AR-01 — Shortform versus full-form template IDs are inconsistent between the lane binding and the registry

- phase: friction
- artifact role: Orca overlay authority (`.agents/workflow-overlay/review-lanes.md` and `.agents/workflow-overlay/template-registry.md`)
- location: `review-lanes.md` lines 88–102 (`template_retrieval_binding` block); `template-registry.md` lines 39–47 (registered template kinds); `prompt-orchestration.md` lines 318–321
- source authority used: the registry table is the canonical template index per `template-registry.md` lines 14–34 and `docs/prompts/templates/README.md` lines 5–14.
- artifact evidence: `review-lanes.md` exposes shortform target keys `gpt55`, `claude_sonnet46`, `claude_opus47` under `template_targets`; the registry and `prompt-orchestration.md` use the full template-kind IDs `generic-gpt55`, `generic-claude-sonnet46`, `generic-claude-opus47`. No mapping is provided.
- requirement strained: registry correctness and overlay terminological consistency (required checks 3 and 4).
- impact: a downstream prompt author or CA who reads `review-lanes.md` and then searches `template-registry.md` for `gpt55` will not find a direct match in the `Template kind` column. The mapping is intuitive but not stated, which is mild discovery friction rather than a broken path.
- blocked state: not blocked; advisory friction.
- minimum_closure_condition: a future overlay edit either harmonizes the keys (e.g., uses `generic-gpt55` in both places) or explicitly states that `gpt55`, `claude_sonnet46`, and `claude_opus47` are aliases for the registered `generic-*` template kinds.
- next_authorized_action: owner decision on whether to apply a follow-up hygiene patch. No patch queue is emitted by this review.
- patch_queue_entry: not authorized by this review lane.
- red-green proof status: not applicable (terminology consistency is not an executable check).
- not-proven boundary: this finding does not claim the registry is broken or that downstream agents will fail; it claims only that the naming is inconsistent.

#### AR-02 — `template_retrieval_binding` lists fewer template targets than the registry actually publishes

- phase: friction
- artifact role: Orca overlay authority (`.agents/workflow-overlay/review-lanes.md`)
- location: `review-lanes.md` lines 92–95 (`template_targets:` enumeration)
- source authority used: the registry table in `template-registry.md` lines 39–47 lists nine registered template kinds, of which `generic-gpt55`, `generic-claude-sonnet46`, `generic-claude-opus47`, the legacy alias `generic-claude-opus`, `research-evidence-lane-o3`, and `research-synthesis-gpt55` are model-named template targets.
- artifact evidence: `review-lanes.md` enumerates only three template targets under `template_targets`. The legacy `generic-claude-opus` alias, the `o3 / o3-deep-research` posture, and the `research-synthesis-gpt55` posture are not represented in that block.
- requirement strained: overlay consistency (required check 4) — `review-lanes.md`, `prompt-orchestration.md`, and `template-registry.md` should agree on the set of template targets if `review-lanes.md` is treated as a discovery surface.
- impact: a reader using the lane binding as a closed enumeration could conclude that only three model-named template targets are accepted, then refuse to use `research-evidence-lane-o3` or the legacy Opus alias even though both are registered. The risk is muted because the `registry:` field in the same block points at `template-registry.md` as the authoritative list.
- blocked state: not blocked; advisory friction.
- minimum_closure_condition: either the `template_targets` block is reframed as an example-only subset (with an explicit "see registry for the complete list" note) or it enumerates every model-named template target the registry publishes.
- next_authorized_action: owner decision on hygiene patch wording.
- patch_queue_entry: not authorized by this review lane.
- red-green proof status: not applicable.

#### AR-03 — `o3 / o3-deep-research` template target value lacks the "prompt posture" suffix used elsewhere

- phase: friction
- artifact role: Prompt template (`docs/prompts/templates/research/o3_evidence_only_research_lane_v0.md`) and Orca overlay authority (`.agents/workflow-overlay/template-registry.md`)
- location: `template-registry.md` line 44 (`Template target` cell reads `o3 / o3-deep-research`); `o3_evidence_only_research_lane_v0.md` line 12 (`Template target: o3 or o3-deep-research prompt posture.`)
- source authority used: every other model-named template target in the registry uses the explicit form `<Model> prompt posture` (lines 40, 41, 42, 43, 45). The template body for the o3 file does use `prompt posture`, but the registry row does not.
- artifact evidence: registry row `o3 / o3-deep-research` could be misread as a runtime model identifier rather than a prompt-posture label; the template body uses the full posture phrasing.
- requirement strained: template-safety framing (required check 5) — model-named template targets should be unambiguously labeled as prompt posture in every discovery surface.
- impact: a CA scanning the registry might briefly read the `o3` row as runtime model routing before reading the template body or the registry rules header that says template targets are prompt-shaping labels only. Risk is low because the template body itself carries the disclaimer.
- blocked state: not blocked; advisory friction.
- minimum_closure_condition: the registry row reads `o3 / o3-deep-research prompt posture` (or equivalent posture-suffixed label) to match the form used by adjacent rows and the template body.
- next_authorized_action: owner decision on a one-line registry tweak.
- patch_queue_entry: not authorized by this review lane.
- red-green proof status: not applicable.

#### AR-04 — Overlay README still refers to `review-lanes.md` as "read-only and executor lane rules"

- phase: friction
- artifact role: Orca overlay authority (`.agents/workflow-overlay/README.md`)
- location: `.agents/workflow-overlay/README.md` line 28
- source authority used: `review-lanes.md` lines 14–29 catalog the current lanes (artifact review, adversarial artifact review, prompt review, patch-queue review, patch/integration execution, deferred workflow-kernel adoption review). Line 83 of `review-lanes.md` explicitly states "Orca no longer binds executor or reviewer lanes to runtime model identifiers."
- artifact evidence: the README's one-line description of `review-lanes.md` retains the phrase "executor lane rules." After the patch, the executor concept survives only as the patch/integration execution lane (a write-permission lane, not a model-bound lane). The phrase is technically accurate but ambiguous against the patch's framing intent.
- requirement strained: overlay consistency (required check 4) — when the rest of the patch is deliberately decoupling lanes from runtime model identity, the README index entry should not echo the older "executor lane" framing without context.
- impact: ambiguous orientation for a fresh agent who reads the index first; they may expect `review-lanes.md` to contain executor-model bindings, then learn the file no longer does. Risk is low because the actual file body makes the new framing clear.
- blocked state: not blocked; advisory friction.
- minimum_closure_condition: the README index entry either drops "executor lane" or replaces it with phrasing that signals write-permission rather than model-bound lane semantics (e.g., "read-only review lanes and patch/integration execution rules").
- next_authorized_action: owner decision on a README phrasing tweak.
- patch_queue_entry: not authorized by this review lane.
- red-green proof status: not applicable.

### Notes

- The defensive lines in `review-lanes.md` (lines 104–110) that quote forbidden phrases such as `run this on Opus`, `recommended model`, and `reviewer model` are correctly framed as prohibitions, not assertions. Grep returns them only because the prohibition text contains the phrase.
- Every template file carries the explicit non-routing disclaimer "This template is prompt-shaping guidance only. It does not recommend, require, rank, or route runtime model choice." That clause is present in the template README, the shared behavior contract, all four `_generic/` templates, both `research/` templates, the `review/` template, and the `wrappers/` template.
- The legacy alias `generic-claude-opus` is explicitly labeled `legacy alias` in the registry status column with a "prefer `generic-claude-opus47` for new prompts" note. The pointed-to file `claude_opus_prompting_best_practices_v0.md` declares its template target as "Claude Opus legacy prompt posture" and disclaims runtime model routing. No ambiguity remains about which Opus scaffold is current.
- The `template_retrieval_binding` block in `review-lanes.md` includes an `authority_order` and a `conflict_rule` that explicitly forbid expanding source-changing authority or runtime model choice through template retrieval. The conflict rule is well constructed.
- `prompt-orchestration.md` line 316 (`Template Retrieval Versus Model Routing`) gives a clear separation between template selection and runtime model choice, and lines 322–334 enumerate the things template retrieval must not do.
- The adversarial artifact review template (`docs/prompts/templates/review/adversarial_artifact_review_v0.md`) is `model-neutral` and requires invocation of `workflow-deep-thinking` then `workflow-adversarial-artifact-review` after `SOURCE_CONTEXT_READY`. It correctly excludes `patch_queue_entry` unless a patch-queue or execution lane is bound and routes `review-report` output to `docs/review-outputs/` or a typed child folder.
- No `jb` policy, jb path, jb lifecycle mechanic, jb product policy, or jb validation habit is imported by any reviewed file. Anti-import wording is repeated in templates and the overlay.

## Closure Check Against Required Checks

| Required check | Result | Evidence |
| --- | --- | --- |
| 1. Runtime model routing removed | pass | `review-lanes.md` lines 75–79, 83–110, 140–141 forbid recommending or implying runtime model choice for lanes; no overlay file binds an executor or reviewer lane to a model identifier; grep finds no `executor model` or `reviewer model` binding outside defensive prohibitions. |
| 2. Template retrieval bounded | pass | The three primary template targets (`gpt55`, `claude_sonnet46`, `claude_opus47`) are bound in `review-lanes.md` lines 88–102 with explicit prompt-posture-only framing and an authority order that forbids source-changing or runtime model choice. Every template file repeats the non-routing disclaimer. |
| 3. Registry paths valid | pass | Glob shows all ten template files registered in `template-registry.md` lines 39–47 exist on disk. Legacy alias `generic-claude-opus` is explicit and points to a real file with the "legacy prompt posture" label. |
| 4. Overlay consistency / prompt orchestration consistent | partial | The four reviewed overlay files agree on the prompt-template-versus-runtime-model distinction and on "template target" terminology. AR-01 (shortform vs full-form IDs), AR-02 (coverage gap in `template_retrieval_binding`), and AR-04 (README "executor lane" phrasing) note minor inconsistencies that do not contradict the policy but introduce friction. |
| 5. Templates safe | pass | Every reviewed template disclaims runtime model routing, ranks, or recommendations and stays within prompt-shape framing. Templates do not create implementation, validation, readiness, review, or lifecycle authority. AR-03 notes one minor labeling asymmetry (`o3` row in the registry omits "prompt posture") that does not break safety because the template body carries the posture framing. |
| 6. Prompt validation compatibility | pass | `prompt-orchestration.md` Section "Prompt Validation Gates" (lines 449–497) preserves source-loading, retrieval-metadata, review-doctrine, source-gated-method, output-mode, and thread-operating-target gates. `validation-gates.md` Section "Prompt Orchestration Gates" (lines 39–136) is internally consistent with the patch. `source-loading.md` and `retrieval-metadata.md` are unchanged in scope. |
| 7. Authority boundaries Orca-local | pass | Templates explicitly disallow importing `jb` policy; overlay README and source-of-truth keep the binding rule that Orca overlay wins for Orca project facts. No external product authority is imported. |
| 8. Dirty/untracked review-target handling | pass | Modified/untracked review targets are treated as in-scope patch artifacts. Hashes match supplied expected values, so working-tree content is the commissioned material. No unrelated dirty file affects this review's confidence. |

## Residual Risk

- The shortform-versus-full-form ID inconsistency (AR-01) could compound if future overlay edits add more aliases without harmonizing names.
- The `template_retrieval_binding` coverage gap (AR-02) could mislead a reader into treating the three named targets as the closed set if the `registry:` field is missed.
- The README index phrasing (AR-04) is mild orientation friction for first-read agents.
- The patch does not change the source-loading or retrieval-metadata contracts. Any future hygiene patch should preserve them.

None of these are correctness blockers for the template-retrieval policy.

## Recommendation

`accept_with_friction`. The patch successfully removes overlay runtime model-routing authority and substitutes bounded prompt-template retrieval. The four minor findings are friction items suitable for a single follow-up hygiene patch; they do not need to land before the policy is used.

## Next Authorized Action

Owner decision: either accept the template-retrieval policy as-is and queue AR-01 through AR-04 as a hygiene patch, or commission a small hygiene patch round before acceptance. This review report is decision input only and does not by itself accept the patch, authorize remediation, or grant edit permission. No patch queue is emitted by this lane.

## Review-Use Boundary

This is a read-only adversarial artifact review. Findings and notes are decision input for the Chief Architect or the Orca owner. They are not approval, validation, mandatory remediation, product proof, or executor-ready instructions. Acceptance of the policy or remediation of the friction findings requires a separate authorized Orca decision, patch, or implementation lane.
