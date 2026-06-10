# Orca File-Write Human Summary Behavior CA Discussion v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Chief Architect discussion of how substantial Orca file-write artifacts should close out in chat when the durable artifact carries detailed value but the owner still needs a usable human summary.
use_when:
  - Deciding how to patch Orca file-write closeout behavior for substantial decision-bearing artifacts.
  - Preparing prompt-orchestration, shared prompt behavior, or targeted active-prompt patches for human summary plus path/hash behavior.
  - Checking why receipt-only file-write closeouts are insufficient for major CA decision artifacts.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
superseded_by:
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
input_hashes:
  - path: .agents/workflow-overlay/communication-style.md
    sha256: 0D7F72216E2791EBB4E986EDF7766F00CF42BAE175B88CF51735ECF886895EEE
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 9E159E3A7CC933083F56C95EBDDED4E19B2F51D55EE8EF774F3BEC62D566834F
  - path: .agents/workflow-overlay/validation-gates.md
    sha256: 4711210EEBD844C4FD22CBB2EE3B8C424B9BA5A8F1B99DFFF437D24B8156A470
  - path: .agents/workflow-overlay/template-registry.md
    sha256: 00A3E05FC7BC4BEE7DD8AE9ECD8B45C84FADB5581A4E301C45DBF4DC9F8A1CC8
  - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    sha256: 1A193C7A813366384DB28F6F8C633E98E3B63CEE52E6954D7D0930C6518C04B5
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: A6510BFF8951C7A2A01087133076C7933D1EF922735A6790237B05BBED503E74
  - path: docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md
    sha256: 8EC6EA1652DE47DDD54BC232EB43896F93E5F738D7FDFFCB4C1ECB406A09F8EB
downstream_consumers:
  - Future Orca chat-output behavior patch route.
  - Future shared prompt behavior contract patch route.
  - Targeted active file-write prompt cleanup, if accepted.
stale_if:
  - Orca chat-output topology changes.
  - File-write output-mode behavior changes.
  - Shared prompt behavior template changes.
  - Owner accepts or rejects a file-write closeout summary patch.
```

## Status And Recommendation

Status: `HISTORICAL_PATCH_DISCUSSION`.

Historical note: the `stale_if` condition for owner acceptance or rejection of
a file-write closeout summary patch has been met. The patch route recommended
by this discussion has been applied in the working tree, and the controlling
current behavior now lives in the Orca overlay and shared behavior contract.
Where this discussion says courier YAML is "conditionally required" or uses the
older "likely to be handed" threshold, treat that as historical framing
superseded by the current overlay threshold: use compact courier YAML only when
requested, required by output mode or output contract, or lane switching /
handoff routing would materially benefit from it.

Recommendation: patch the `file-write` output-mode rule and shared prompt behavior so substantial decision-bearing file-write closeouts must include a concise material human summary, an artifact path/hash/status receipt, and compact courier YAML when lane switching or later handoff routing is expected; then selectively patch active prompts whose closeout clauses can still steer agents toward receipt-only chat.

Source basis: `AGENTS.md`; `.agents/workflow-overlay/README.md`; `.agents/workflow-overlay/source-of-truth.md`; `.agents/workflow-overlay/artifact-roles.md`; `.agents/workflow-overlay/artifact-folders.md`; `.agents/workflow-overlay/communication-style.md`; `.agents/workflow-overlay/prompt-orchestration.md`; `.agents/workflow-overlay/validation-gates.md`; `.agents/workflow-overlay/template-registry.md`; `.agents/workflow-overlay/retrieval-metadata.md`; `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`; `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`; `docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`; targeted searches over `.agents/workflow-overlay/` and `docs/prompts/` for human-summary, courier-YAML, file-write, receipt, review-report, paste-ready-chat, compact, and Chat Closeout language.

Pinned source status: all pinned hashes in the prompt matched the current workspace files at CA run time.

## Problem Frame

Triggering incident:

The major-move folder-integrity CA pass wrote a substantial workflow artifact and returned a compact closeout containing path, SHA256, recommendation, patch implication, and next step. That closeout was routable, but it did not summarize enough of the decision substance for the owner to understand the result without opening the large artifact.

What the owner expected:

The owner expected the chat closeout to include both human-usable decision substance and routable state. In the current turn, the owner stated a preferred candidate shape: human summary with all material facts, artifact written to a specific path when durable or substantial enough to be temporary, and YAML for a human to courier during lane switching. That preference is materially correct about the missing human value, but "all material facts" must be bounded so it does not become full artifact pasteback or source-heavy readback.

What the existing rules already say:

- `communication-style.md` says decision-bearing Orca chat should use human summary first, agent-readable detail second, and compact courier YAML last when useful or required.
- `prompt-orchestration.md` says `file-write` may return compact path/hash/status receipts after a durable artifact is written when that artifact carries the human-readable value.
- `validation-gates.md` already has a chat-output topology gate that calls out the collision between human-readable decision chat and output-mode exceptions.
- The shared prompt behavior contract says compactness must not hide a decision-bearing answer in YAML-only or agent-only structure, while preserving artifact-native tables, paste-ready prompt bodies, and post-artifact receipts when the output mode permits them.

Where the ambiguity or failure mode lives:

The ambiguity is not whether `file-write` can ever close with a receipt. It can. The failure is that "the artifact carries the human-readable value" can be over-applied to substantial decision-bearing artifacts, causing chat to omit the minimum summary needed by the owner to understand the decision, tradeoffs, and next move. Prompt clauses that say "Do not paste the full artifact into chat" are correct, but without a positive summary contract they can accidentally collapse into receipt-only behavior.

## Current Contract Map

`communication-style.md`:

- Owns the general chat-output topology: human summary, agent-readable detail, compact courier YAML.
- Defines courier YAML as routable state, not the decision or report itself.
- Explicitly says output-mode exceptions for `review-report`, `file-write`, and `paste-ready-chat` are owned by `prompt-orchestration.md`.
- Warns not to apply human-summary-first mechanically to compact post-artifact receipts when the durable artifact carries the human-readable value.

`prompt-orchestration.md`:

- Owns output-mode exceptions.
- Defines `file-write` as writing authorized Orca documentation or overlay files and reporting changed files plus validation evidence.
- Says `file-write` may return compact path/hash/status receipt after the durable artifact is written when that artifact carries the human-readable value.
- Says if the write fails or chat itself carries a decision, readable blocker detail must replace a receipt-as-substitute.
- Does not yet distinguish small receipt-worthy writes from substantial decision-bearing CA artifacts where the durable artifact carries the detail but chat still needs material summary.

`validation-gates.md`:

- Already includes a chat-output topology gate for prompt-policy patches, workflow patches, and reusable prompt templates touching chat output shape.
- Correctly preserves `review-report` YAML-only success behavior, `file-write` receipts, `paste-ready-chat`, task-native structured outputs, and avoidance of ritual keys.
- Does not need to become the primary behavioral rule. It should remain a collision gate, not the source of the closeout contract.

Shared prompt behavior contract:

- Requires exactly one output mode.
- Points decision-bearing chat to the general topology and output-mode exceptions.
- Says compactness does not mean hiding a decision-bearing answer in YAML-only or agent-only structure.
- Still lacks a concrete `file-write` closeout clause that future templates inherit.

Relevant active prompt closeout language:

- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` asks for artifact path, SHA256, recommendation, patch implication, and exact next authorized step. It does not ask for a material decision summary.
- `docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md` asks for a compact human-readable summary with artifact path, SHA256, verdict, selected wedge or blocker, patch implications, and next step. It is better, but still could underspecify the decision substance if the artifact is large and multi-criteria.
- Review-report prompts and templates are intentionally different: when a durable review report is written, compact YAML can be the normal chat closeout because the review report is the review artifact and YAML is courier output.

## Options Compared

| Option | Owner comprehension | Artifact economy | Exception preservation | Future prevention | Patch surface | Assessment |
| --- | --- | --- | --- | --- | --- | --- |
| 1. No patch; call prior closeout an agent error | Weak. Existing rules can be read either way for substantial file-write artifacts. | Strong. No added chat burden. | Strong. Nothing changes. | Weak. The same receipt-only failure can recur. | None. | Reject. This was not merely one bad closeout; the rules contain a real ambiguity. |
| 2. Patch only `prompt-orchestration.md` | Strong if it defines substantial decision-bearing `file-write` closeouts. | Strong if it forbids full pasteback and source-heavy readback. | Strong because output-mode exceptions belong here. | Medium. Templates still may fail to inherit a concrete clause. | Narrow. | Necessary but incomplete. This is the canonical place for the rule, but templates need propagation. |
| 3. Patch only `communication-style.md` | Medium. It reinforces human-summary-first chat. | Medium. Risk of over-applying human summary to output-mode exceptions. | Medium-to-weak because file-write exception ownership lives elsewhere. | Medium. | Narrow. | Downgrade. Useful only as a cross-reference, not as the main fix. |
| 4. Patch shared prompt behavior contract | Strong for future templates that include it. | Strong if the clause is concise. | Strong if it points back to output modes. | Strong for new prompts. | Narrow-to-medium. | Necessary with option 2. It turns the rule into inherited prompt behavior. |
| 5. Patch individual active prompts | Strong for known active problem prompts. | Medium. Risk of broad churn if applied indiscriminately. | Strong if targeted. | Weak-to-medium because future templates can still recreate the issue. | Variable. | Use selectively after the source rule is accepted. Do not broad-sync stale one-offs. |
| 6. Hybrid: patch output-mode rules plus shared behavior, then selectively patch active prompts/templates | Strong. It fixes the owner-facing behavior and the inheritance path. | Strong if the summary is bounded and artifact detail stays local. | Strong. Keeps `review-report`, `paste-ready-chat`, source-heavy economy, and artifact-native tables intact. | Strong. Prevents future CA prompts from specifying receipt-only closeouts. | Medium but controlled. | Recommended. |
| 7. Owner-preferred shape: human summary with all material facts, path/status receipt, and courier YAML for lane switching | Strong if "material facts" means decision-critical facts, not exhaustive detail. | Medium-to-strong if bounded; weak if interpreted as all evidence. | Strong if YAML is conditional for lane switching, weak if YAML is mandatory for every file write. | Strong for handoffs and CA decisions. | Medium. | Adopt as the practical closeout shape, with two guardrails: material summary is not full artifact pasteback, and courier YAML is required only when routing/lane switching is expected or the prompt asks for it. |

## Recommended Closeout Contract

Minimum human summary requirement:

For substantial decision-bearing `file-write` artifacts, chat must include a concise material human summary before the artifact receipt. The summary should let the owner understand the decision without opening the artifact. It should normally include:

- recommendation or verdict;
- the key reason it wins;
- the main tradeoff or rejected alternative that matters;
- accepted, deferred, or blocked items;
- patch or behavior implication;
- exact next authorized step.

"Material" does not mean all source facts, all table rows, all option details, or every non-claim. It means the decision-critical facts a human needs to understand what changed and decide the next move. If the artifact is long because of evidence tables, source ledgers, or detailed option comparisons, those details stay in the artifact.

Path/hash/status receipt requirement:

After the human summary, the closeout should state the durable artifact path and SHA256 when the artifact was written and hashed. If the artifact is intentionally temporary but substantial enough to route, name the temporary path and status, and avoid implying durable authority. If the write fails, do not use path/hash receipt language that suggests the artifact exists.

Courier YAML:

Courier YAML should be conditionally required for substantial file-write CA artifacts when lane switching, future prompt handoff, review routing, or another thread/agent is expected to continue from the result. It should be optional for simple same-thread closeouts and discouraged when it would duplicate a two-line human summary without improving routing.

The preferred order is:

1. Human summary with decision-critical material facts.
2. Artifact receipt with path, SHA256, and status.
3. Compact courier YAML when useful or required.

How much detail is enough:

Enough detail means the owner can answer: what was decided, why, what did not change, where the artifact is, and what the next authorized step is. For most substantial CA file-write artifacts, that is five to nine bullets or a short paragraph plus a small receipt block. It is not the full artifact, not a review report pasted into chat, and not a full source-read ledger.

What should stay in the artifact only:

- Full option tables.
- Source-heavy evidence.
- Long current-contract maps.
- Detailed risk registers.
- Full patch-unit descriptions.
- Exhaustive non-claim lists.
- Artifact-native tables and source ledgers.

## Patch Implications

`.agents/workflow-overlay/communication-style.md`:

Needs a small later patch, but not the primary rule. It should cross-reference that substantial decision-bearing file-write artifacts are not receipt-only just because the durable artifact carries the detail. It should keep the general topology and courier YAML ownership clean.

`.agents/workflow-overlay/prompt-orchestration.md`:

Needs the primary later patch. The `file-write` output-mode exception should distinguish:

- receipt-only or receipt-light closeouts for small writes where the artifact is the only meaningful human value;
- substantial decision-bearing file-write closeouts, which require a material human summary plus path/hash/status;
- failed writes, which require readable blocker detail and must not pretend a durable artifact exists;
- optional or required courier YAML based on handoff/lane-switching need.

`.agents/workflow-overlay/validation-gates.md`:

No primary patch required. A small later patch may add this rule to the chat-output topology gate after `prompt-orchestration.md` is patched, but the gate should not become a checklist of mandatory YAML fields.

`docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`:

Needs a later patch so future templates inherit the closeout behavior. The clause should be short and should point to `prompt-orchestration.md` as the owner of output-mode exceptions.

Active prompt artifacts:

Need targeted later patches only where a prompt is active, likely to be reused, and asks for a substantial decision-bearing file-write artifact. The highest-priority example is `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`, whose closeout asks for path/hash/recommendation/patch implication/next step but not enough decision substance. `docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md` may need a smaller tightening because it already asks for a compact human-readable summary.

Do not broad-sync stale prompts or non-Orca prompt artifacts. The targeted patch route should avoid touching unrelated `review-report` prompts that are already aligned with the saved-report exception.

Conceptual patch units:

- `STEP-01`: Patch `prompt-orchestration.md` `file-write` output-mode exception with the substantial decision-bearing closeout rule.
- `STEP-02`: Patch `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` with a concise inherited `file-write` closeout clause.
- `STEP-03`: Patch `communication-style.md` only as a cross-reference to avoid future misreadings of compact post-artifact receipts.
- `STEP-04`: Patch targeted active file-write CA prompts, starting with the major-move folder-integrity prompt, to include a positive `Chat Closeout` contract.
- `STEP-05`: Optionally update `validation-gates.md` only if the patch route needs a check for this exact collision.

## Prompt Structure Guidance

Recommended `Chat Closeout` clause for future substantial `file-write` CA prompts:

```markdown
## Chat Closeout

After writing the artifact, return a compact but substantive human-readable closeout. Do not return a receipt-only response.

Include:

- the recommendation or verdict in plain language;
- the material decision facts needed to understand the result without opening the artifact;
- the main tradeoff, blocker, or deferred item if it changes the next move;
- what should not change or what remains out of scope;
- artifact path and SHA256;
- exact next authorized step;
- compact courier YAML when this result is likely to be handed to another lane, agent, thread, or prompt.

Do not paste the full artifact, full option table, full source ledger, or source-heavy evidence into chat unless the write fails and chat is the only available output.
```

Bad closeout example to avoid:

```text
Wrote docs/workflows/example_discussion_v0.md.
SHA256: <hash>
Recommendation: HYBRID_PATCH_ROUTE_RECOMMENDED.
Next step: Patch prompt behavior.
```

This is routable but not human-useful. It names the result without explaining the material decision.

Good closeout shape:

```text
The recommendation is a hybrid patch route: make prompt-orchestration own the file-write closeout rule, update the shared behavior contract so templates inherit it, and patch only active prompts that can still steer agents toward receipt-only closeouts.

The behavioral gap is that "do not paste the full artifact" and "file-write may return path/hash/status" can be read as permission to omit the material decision summary. The fix should require decision-critical summary, not full artifact pasteback. Review-report YAML-only closeouts, paste-ready prompt bodies, source-heavy evidence economy, and artifact-native tables should remain intact.

Artifact: docs/workflows/example_discussion_v0.md
SHA256: <hash>
Next authorized step: Patch prompt-orchestration and the shared behavior contract.
```

Courier YAML, when lane switching is needed:

```yaml
orca_courier:
  status: artifact_written
  artifact_path: docs/workflows/example_discussion_v0.md
  recommendation: HYBRID_PATCH_ROUTE_RECOMMENDED
  next_authorized_step: Patch prompt-orchestration and shared behavior contract.
```

## Risks And Non-Claims

Overlong chat risk:

If "material facts" is interpreted as every important detail, closeouts will become artifact echoes. The rule must define material summary as decision-critical owner-facing facts, not full evidence or option readback.

Receipt-only risk:

If `file-write` remains under-specified, agents will continue treating path/hash/recommendation as enough even when the artifact is a substantial decision record.

YAML ritual risk:

Adding YAML everywhere would be the wrong fix. YAML is useful when a human needs to courier state across lanes, agents, prompts, or threads. It is wasteful when it merely repeats a simple human closeout.

Review-report exception risk:

Do not weaken the `review-report` rule. YAML-only chat remains valid only after a required durable review report is successfully written, or under the explicit blocked/chat-only shapes already defined by the overlay.

Source-heavy readback risk:

Source ledgers, evidence tables, and detailed comparisons should stay artifact-local after the file is written and hashed. Chat should carry enough summary to route and understand, not enough text to recreate the artifact.

Paste-ready-chat risk:

Do not make paste-ready prompt bodies start with extra closeout prose when the paste-ready body itself is the deliverable. Surrounding CA or routing decisions should still be human-readable, but the prompt body should remain pasteable.

No patch acceptance claim:

This artifact recommends a patch route. It does not apply patches or claim owner acceptance.

No validation/readiness claim:

This artifact does not claim validation, readiness, approval, lifecycle completion, install/deploy/resolver status, merge safety, product readiness, feature readiness, or implementation readiness.

## Exact Next Authorized Step

Authorize a narrow docs-write patch route for `prompt-orchestration.md`, `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`, a small `communication-style.md` cross-reference, and targeted active file-write CA prompt closeout clauses, starting with `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`.
