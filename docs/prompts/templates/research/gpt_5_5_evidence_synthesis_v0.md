# GPT-5.5 Evidence Synthesis Template v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: GPT-5.5 synthesis template for prior evidence-only research outputs.
use_when:
  - Synthesizing, scoring, tiering, or recommending from gathered evidence.
authority_boundary: retrieval_only
```

Template target: GPT-5.5 prompt posture.

This template is prompt-shaping guidance only. It does not recommend, require,
rank, or route runtime model choice.

Output mode: `paste-ready-chat`

Use shared contract:
`docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md`

```text
You are synthesizing prior evidence-only research lane outputs for Forseti.

Objective:
[FILL_SYNTHESIS_OBJECTIVE]

Inputs:
[PASTE_OR_LIST_EVIDENCE_ONLY_LANE_OUTPUTS]

Source rule:
Use only cited evidence from the inputs and stable public URLs. Do not use
uncited claims. Do not treat marketing claims as independently verified unless
external evidence is supplied.

Decision boundary:
[FILL_DECISION_OR_DATE_BOUNDARY]

Synthesis tasks:
[FILL_SCORING_OR_CLASSIFICATION_TASKS]

Separate:
- public benchmark value;
- actual backtestability;
- external outcome evidence;
- anonymous marketing claims.

Required output:
[FILL_REQUIRED_OUTPUT_SHAPE]

If the synthesis produces a decision, recommendation, or routing result, start
with a human-readable summary before detailed evidence tables or classifications.
If the required output is a structured artifact, preserve that structure and use
compact routing YAML only at the end when requested or required.

Non-claims:
Do not claim buyer validation, willingness to pay, product readiness, feature
readiness, implementation readiness, commercial readiness, corpus exhaustiveness,
or verified external outcomes unless the supplied evidence explicitly proves it.
```
