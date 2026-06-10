# Orca Overlay Template Retrieval Policy — Hygiene Patch Adversarial Recheck v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Narrow adversarial recheck of the hygiene patch that followed the orca overlay template retrieval policy adversarial review v0.
use_when:
  - Deciding whether AR-01 through AR-04 are closed after the hygiene patch.
  - Tracing whether the hygiene patch introduced new runtime model-routing authority or registry drift.
authority_boundary: retrieval_only
supersedes:
  - docs/review-outputs/adversarial-artifact-reviews/orca_overlay_template_retrieval_policy_adversarial_review_v0.md
input_hashes:
  prior_review: 4646DE39BD880A1703226E1A39D786B6EC96708F4777CB03085006362DDD08D7
  .agents/workflow-overlay/README.md: 68D8E9CF4ECADC39DA932CBB11CE82B4FEB6CA891B444F3453436395C2E160D2
  .agents/workflow-overlay/review-lanes.md: 2977812826E75DA42805181BE5CC7BA81F41F49068123776AF8966CFBB29B199
  .agents/workflow-overlay/template-registry.md: 2AE3A28EF76E9F63CC5E9F21E0F005F3C20B86D05F0B5C24FF93F73DB75382A1
branch_or_commit: main @ b7627d3
```

The `supersedes` field is retrieval-only routing guidance: the prior review report remains valid historical evidence; this recheck is the current decision artifact for AR-01 through AR-04 closure.

## Recheck Target

The hygiene patch that followed `docs/review-outputs/adversarial-artifact-reviews/orca_overlay_template_retrieval_policy_adversarial_review_v0.md`. Patched files:

- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/template-registry.md`

Out of scope: the other ten files from the prior policy review (no closure check requires them), installed workflow-kernel skill source, jb policy, runtime model selection, implementation work, and patch execution.

## Recheck Purpose

Confirm whether AR-01 through AR-04 from the prior review are closed by the hygiene patch and whether the patch introduced new runtime model-routing authority, broken registry references, or weakened authority boundaries.

## Source Context Status

`SOURCE_CONTEXT_READY`.

- `AGENTS.md` and `.agents/workflow-overlay/README.md` were read in the current task context.
- `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were `REFERENCE-LOAD`ed earlier in this conversation; their procedural guidance is in context and was applied as a private framing pass before findings were drafted.
- Prior review report `orca_overlay_template_retrieval_policy_adversarial_review_v0.md` was reread; its SHA256 matches the supplied `4646DE39…D08D7`.
- The three patched files were read; their SHA256 hashes match the supplied expected values.
- Branch `main` at commit `b7627d3` matches the expected branch/head.

Dirty-state ledger. The three patched files are in-scope patch artifacts; their working-tree hashes match the supplied expected values, so the recheck is reading the commissioned content. Other dirty files in the workspace are out of scope for this recheck.

## Verified Hashes

| File | SHA256 | Expected | Match |
| --- | --- | --- | --- |
| `docs/review-outputs/adversarial-artifact-reviews/orca_overlay_template_retrieval_policy_adversarial_review_v0.md` | `4646DE39…D08D7` | as supplied | yes |
| `.agents/workflow-overlay/README.md` | `68D8E9CF…160D2` | as supplied | yes |
| `.agents/workflow-overlay/review-lanes.md` | `29778128…9B199` | as supplied | yes |
| `.agents/workflow-overlay/template-registry.md` | `2AE3A28E…82A1` | as supplied | yes |

All four hashes match.

## Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Confirm `workflow-deep-thinking` and `workflow-adversarial-artifact-review` are `REFERENCE-LOAD`ed and in conversation context.
3. Read prior review report and verify its hash.
4. Read only the three patched files and verify their hashes.
5. Verify branch/head against `main` at `b7627d3`.
6. Declare `SOURCE_CONTEXT_READY`.
7. Apply deep-thinking framing pass against the four prior closure conditions and against drift failure modes (new runtime model routing, weakened boundaries, broken registry references).
8. Run closure check for each AR finding against the supplied closure conditions.
9. Scan for patch-caused drift inside the three touched files.
10. Write this durable recheck report and return only the compact YAML summary.

## Executive Verdict

The hygiene patch closes all four prior findings against the supplied closure conditions. The `template_retrieval_binding` block in `review-lanes.md` now uses full registry IDs (`generic-gpt55`, `generic-claude-sonnet46`, `generic-claude-opus47`), enumerates all nine registered template kinds, and adds an explicit `template_ids_authority: registry_registered_templates` field deferring to the registry. The `template-registry.md` row for `research-evidence-lane-o3` now reads `o3 / o3-deep-research prompt posture`, matching the form used by adjacent rows. The overlay `README.md` index entry for `review-lanes.md` now reads `read-only review lanes, patch/integration execution boundaries, and template retrieval rules`, dropping the "executor lane" framing while not reintroducing runtime model-routing semantics.

No new runtime model-routing authority is created. The patch does not rank, recommend, require, or route runtime models. Review-lane, template-registry, prompt-orchestration, and source-loading authority boundaries are preserved.

Recommendation: hygiene patch accepted.

## Closure Check

### AR-01 — Shortform versus full-form template IDs

- Prior state: `review-lanes.md` `template_retrieval_binding` used shortform keys `gpt55`, `claude_sonnet46`, `claude_opus47`.
- Patched state: `review-lanes.md` lines 88–109 now use full registry IDs `generic-gpt55`, `generic-claude-sonnet46`, `generic-claude-opus47`. The block field is renamed from `template_targets` to `template_ids` and a new `template_ids_authority: registry_registered_templates` field defers to the registry.
- Closure condition 1 (no shortform binding keys): met — the shortforms `gpt55`, `claude_sonnet46`, `claude_opus47` no longer appear as binding keys in `review-lanes.md`.
- Closure condition 2 (registry-style IDs): met — keys match registry IDs verbatim.
- Verdict: closed.

### AR-02 — Coverage gap in `template_retrieval_binding`

- Prior state: only three template targets listed under `template_targets`.
- Patched state: `template_ids` enumerates all nine registered template kinds (`shared-behavior-contract`, `generic-gpt55`, `generic-claude-sonnet46`, `generic-claude-opus47`, `generic-claude-opus`, `research-evidence-lane-o3`, `research-synthesis-gpt55`, `adversarial-artifact-review`, `thin-wrapper`). The set matches the nine rows in `template-registry.md` verbatim.
- Closure condition 1 (defer to registry or list full current set): met by both mechanisms — `template_ids_authority: registry_registered_templates` defers authority to the registry, and the enumeration is complete.
- Closure condition 2 (no partial list creates a competing template authority): met — the `template_ids_authority` field makes the registry canonical, so even if the enumeration drifts in future, downstream agents have a stated tiebreaker.
- Verdict: closed.

### AR-03 — `o3` registry row label

- Prior state: `template-registry.md` line 44 `Template target` cell read `o3 / o3-deep-research`.
- Patched state: same row now reads `o3 / o3-deep-research prompt posture`.
- Closure condition 1 (label makes prompt-posture status explicit): met.
- Closure condition 2 (does not imply runtime model routing): met — the suffix matches the form used by adjacent rows, and the row sits under the registry's `Registry Rules` section which already binds "Template targets are prompt-shaping labels only."
- Verdict: closed.

### AR-04 — README "executor lane" phrasing

- Prior state: `README.md` line 28 read `- \`review-lanes.md\`: read-only and executor lane rules.`
- Patched state: same line now reads `- \`review-lanes.md\`: read-only review lanes, patch/integration execution boundaries, and template retrieval rules.`
- Closure condition 1 (no "read-only and executor lane rules" phrasing): met.
- Closure condition 2 (replacement does not reintroduce runtime model-routing authority): met — "patch/integration execution boundaries" describes a write-permission lane (per `review-lanes.md` line 27), and "template retrieval rules" matches the new Template Retrieval Binding section in `review-lanes.md`. No model identifier appears in the replacement wording.
- Verdict: closed.

## Patch-Caused Drift Check

- New runtime model-routing authority: none. `review-lanes.md` lines 75–79, 83–86, 111–117, and 147–148 continue to forbid recommending, prescribing, ranking, or implying runtime model choice for lanes. The Template Retrieval Binding section is strengthened, not weakened.
- Ranking, recommending, requiring, or routing runtime models: none. The block uses prompt-posture labels and explicitly disclaims runtime model selection.
- Weakened authority boundaries (review-lane, template-registry, prompt-orchestration, source-loading): none observed. The Current Lanes catalog (lines 14–29), Review Doctrine (lines 30–79), and Rules (lines 119–149) are preserved verbatim. The `template-registry.md` Registry Rules and Registered Templates sections are unchanged except for the single AR-03 row-label edit. `prompt-orchestration.md` and `source-loading.md` were not touched by this hygiene patch.
- Broken registry references or conflicting template terminology: none. The nine `template_ids` keys in `review-lanes.md` match the nine rows in `template-registry.md` verbatim.

Observation, not a finding: three of the nine entries in `review-lanes.md` `template_ids` use hybrid value labels that combine the registry's `Template target` column with additional descriptive text (`model-neutral template include` for `shared-behavior-contract`, `model-neutral review template` for `adversarial-artifact-review`, `model-neutral wrapper template` for `thin-wrapper`). The six model-named entries use clean prompt-posture labels that match the registry exactly. Because the block declares `template_ids_authority: registry_registered_templates`, any value-label drift is non-binding — a downstream agent who needs the canonical Template target value follows the authority field to the registry. This does not affect the closure of AR-01 or AR-02 and is recorded here only as residual risk should future hygiene work want to harmonize value labels.

## New Findings

None. No new blocker or major issue is introduced by the hygiene patch inside the touched scope. The hybrid-label observation above does not meet the recheck finding bar.

## Residual Risk

- The `template_ids` block in `review-lanes.md` could drift out of sync with the registry if a future overlay edit adds or removes a template kind from one file but not the other. The `template_ids_authority: registry_registered_templates` field mitigates this by stating the registry as canonical, but explicit cross-file maintenance discipline is still required.
- The hybrid value labels for `shared-behavior-contract`, `adversarial-artifact-review`, and `thin-wrapper` are slight friction. Not a closure issue; flagged here for future hygiene authors.
- The patch scope was deliberately narrow (three files). No drift was introduced in `prompt-orchestration.md`, `template-registry.md` rules header, or other overlay files.

## Recommendation

`hygiene_patch_accepted`. All four AR findings are closed against their supplied closure conditions. No new runtime model-routing authority, broken registry reference, or weakened boundary was introduced. The hygiene patch may be accepted as-is.

## Next Authorized Action

Owner decision to accept the hygiene patch and the underlying template-retrieval policy. This recheck report is decision input only; it does not by itself accept the patch, authorize remediation, grant edit permission, or supersede any Orca overlay artifact. No patch queue is emitted by this lane.

## Review-Use Boundary

This is a read-only adversarial recheck. Findings, closure verdicts, and observations are decision input for the Chief Architect or the Orca owner. They are not approval, validation, mandatory remediation, product proof, or executor-ready instructions. Acceptance of the hygiene patch or the underlying policy requires a separate authorized Orca decision, patch, or implementation lane.
