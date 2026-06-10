# Daimler Advisory Run 001 Manual Execution Handoff Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Orca thin wrapper prompt
scope: Wrapper for a fresh Chief Architect to load the DAIMLER_ADVISORY_001 handoff packet and continue the same advisory execution lane.
use_when:
  - Starting a new CA thread for DAIMLER_ADVISORY_001 manual advisory execution.
  - Ensuring source-loading and confirm-don't-trust sequencing before any prompt paste or run.
  - Preserving the non-gate-clearing manual subscription/chat boundary.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/handoffs/daimler_advisory_run_001_manual_execution_handoff_v0.md
input_hashes:
  docs/prompts/handoffs/daimler_advisory_run_001_manual_execution_handoff_v0.md: 7218E35191702429A40EFD38404BDE2F7ECC9AD7091617900F35FA27FCF42DFF
branch_or_commit: main @ 829bbe0dc9545cc34f7174cd7f3058824f5fd331
stale_if:
  - handoff packet hash changes.
  - DAIMLER_ADVISORY_001 authorization record changes.
  - prompt-prep artifact changes.
  - owner changes from manual subscription/chat to API or gate-bearing execution.
```

## Wrapper Prompt

Paste the following into the fresh CA lane:

```text
You are continuing the same Orca Judgment Spine advisory execution lane in
workspace:

C:\Users\vmon7\Desktop\projects\orca

First, read `AGENTS.md` and `.agents/workflow-overlay/README.md`. Follow the
Orca overlay when project-specific rules conflict with reusable workflow
mechanics.

Then load this handoff packet:

docs/prompts/handoffs/daimler_advisory_run_001_manual_execution_handoff_v0.md

Expected handoff SHA256:

7218E35191702429A40EFD38404BDE2F7ECC9AD7091617900F35FA27FCF42DFF

Use the handoff packet's confirm-don't-trust load contract. Do not continue
from the sender's claims by trust. Re-verify the load-bearing facts first:

1. Confirm branch and HEAD, or report drift:
   - expected branch: main
   - expected HEAD: 829bbe0dc9545cc34f7174cd7f3058824f5fd331

2. Recompute the SHA256 hashes named in the handoff for:
   - docs/decisions/daimler_advisory_run_001_authorization_record_v0.md
   - docs/prompts/advisory/daimler_advisory_run_001_prompt_prep_v0.md
   - docs/workflows/daimler_advisory_runbook_v0.md
   - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md

3. Return exactly one load outcome before acting:
   - REUSE
   - PARTIAL_REUSE
   - STALE_REREAD_REQUIRED
   - BLOCKED_DRIFT
   - BLOCKED_MISSING_PACKET
   - BLOCKED_UNVERIFIABLE

If and only if the load outcome permits continuation, proceed from the handoff's
Exact Next Authorized Action:

1. Ask the owner to name the concrete manual subscription/chat surface if they
   have not already named it.
2. Tell the owner to paste only the fenced **Model-Facing Prompt Body** from:
   docs/prompts/advisory/daimler_advisory_run_001_prompt_prep_v0.md
3. After the owner pastes the model response back, conduct an owner readback
   focused only on what the response teaches about the Judgment Spine product
   experience.

Hard boundaries:

- Do not paste the authorization record, runbook, handoff packet, review
  reports, hashes, source registry material, probe results, facilitator ledger
  material, or operator-only notes into the model-facing context.
- Do not select the model/provider yourself if the owner has not named the
  concrete manual subscription/chat surface.
- Do not use API execution.
- Do not claim validation, fixture admission, scoring, clean no-tools evidence,
  product proof, buyer validation, blind-use readiness, or judgment quality.
- Do not run an adversarial review or create more plumbing by default; the
  current frontier is one bounded advisory answer and owner readback.

Close out with the load outcome, the selected surface if owner supplied one,
whether any prompt paste/run happened, and all non-claims that remain material.

Required boundary: plumbing works only; not judgment quality.
```

## Non-Claims

- This wrapper does not run the advisory pass.
- This wrapper does not select a model or provider.
- This wrapper does not authorize API or gate-bearing execution.
- This wrapper does not validate the fixture, admit the fixture, score outputs,
  freeze a ledger, prove product value, or prove judgment quality.

Required boundary: plumbing works only; not judgment quality.
