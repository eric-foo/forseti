# o3 Evidence-Only Research Lane Template v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: Evidence-only public research lane template for o3 or o3-deep-research.
use_when:
  - Launching a bounded public research lane where reasoning is deferred.
authority_boundary: retrieval_only
```

Template target: o3 or o3-deep-research prompt posture.

This template is prompt-shaping guidance only. It does not recommend, require,
rank, or route runtime model choice.

Output mode: `paste-ready-chat`

Use shared contract:
`docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

```text
You are running an evidence-gathering-only public research lane for Forseti.

Goal:
[FILL_EVIDENCE_GOAL]

Reasoning boundary:
Do not reason, score, rank, recommend, synthesize, or infer strategic value.
Collect only source-backed evidence. Label missing fields as `not_found`.

Date boundary:
[FILL_DATE_BOUNDARY]

Target source universe:
[FILL_TARGET_SOURCES_OR_DOMAINS]

Inclusion criteria:
[FILL_INCLUSION_CRITERIA]

Reject or downgrade from output:
[FILL_REJECT_CRITERIA]

Evidence fields to collect:
[FILL_FIELD_LIST]

Citation rules:
- Return stable public URLs.
- Use short excerpts only when needed to prove that a field exists.
- Do not copy long source passages.
- Separate source-visible evidence from interpretation.

Output:
Return a structured table or grouped tables using only the requested fields.
Do not add scoring, tiers, recommendations, or synthesis.

This evidence table is the task-native artifact shape. Do not add a human
decision summary, agent-detail section, or courier YAML unless the launch
instruction separately asks for routing context; if it does, keep that context
brief and outside the evidence table.

Non-claims:
This output is evidence gathering only. It does not prove buyer validation,
willingness to pay, product readiness, feature readiness, implementation
readiness, commercial readiness, or backtest success.
```
