# Subagent Model-Tiering Doctrine v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision/doctrine (delegation model-tiering)
scope: >
  How Orca chooses which model tier a spawned subagent runs on across Claude Code
  and Codex, so mechanical / ordinary delegable work defaults below the chief
  architect tier and the strongest tier is reserved for genuine judgment -- without
  over-restraining escalation.
use_when:
  - Spawning a subagent and choosing its model or runtime tier.
  - Authoring or reviewing custom agent definitions under `.claude/agents/`.
  - Deciding whether a delegated task needs the strongest available judgment tier.
authority_boundary: retrieval_only
open_next:
  - .claude/agents/worker.md          # Claude Code Sonnet default workhorse
  - .claude/agents/mechanical.md      # Claude Code Haiku trivial-rote tier
  - .agents/workflow-overlay/decision-routing.md   # delegation routing owner
stale_if:
  - Claude Code changes the subagent model-resolution order or the agent-definition `model` field.
  - Codex changes the `multi_agent_v1.spawn_agent` model override names or semantics.
  - The tier mapping is re-decided by the owner.
```

## Problem this fixes

A subagent spawned via the Agent/Task tool with **no `model` set** falls through
to the parent's model. When the parent (main loop) is Opus, ordinary delegated
work — captures, builds, rote edits — silently runs on **Opus**, which is
expensive overkill. The failure is an expensive *default*, not a missing gate.

Codex has the same class of failure in a different shape. The
`multi_agent_v1.spawn_agent` tool inherits the parent model when `model` is
omitted, but it also exposes explicit model overrides. If the chief architect
does not classify the delegated task before spawning, mechanical work can run
on a judgment tier or judgment work can be accidentally underpowered.

## Assumption gate (Codex, observed 2026-06-16)

Before applying the Codex mapping, check the actual spawn surface available in
the current session:

- **Subagent spawning available:** yes, via `multi_agent_v1.spawn_agent`.
- **Model override available:** yes, `model` is an optional override; omission
  inherits the parent model.
- **Observed Codex override values:** `gpt-5.3-codex-spark`, `gpt-5.4`,
  `gpt-5.4-mini`, `gpt-5.5`.
- **Reasoning/service overrides:** available but not part of this doctrine;
  omit them unless independently required.
- **Stop condition:** if the tool schema no longer exposes these exact model
  names, do not invent replacements. Omit the model override or stop for an
  owner/tooling decision.

## Decision

Tier by task, default cheap, keep Opus an easy opt-in:

- **Default delegated work → Sonnet.** Most delegable work (build to a stated
  pattern, capture/gather + verify, multi-step research, doc drafting) is
  Sonnet-grade. Route it to the **`worker`** agent type (pinned `model: sonnet`).
- **Trivial rote → Haiku.** Run-a-command, move/rename, precise find-replace →
  the **`mechanical`** type (pinned `model: haiku`).
- **Genuine judgment → Opus.** Novel design, compounding multi-step reasoning,
  subtle correctness on shared/contract-bearing surfaces, adversarial review →
  `general-purpose` (which inherits the main Opus tier) or an explicit
  `model: opus`. This stays available; it is a conscious choice, not the default.

**Do not collapse "mechanical" to Haiku.** Most delegated work needs Sonnet-grade
judgment (e.g. the Wayback capture builds had to pin domains, choose cutoffs,
handle rate-limits). Forcing Haiku there causes wrong results and redo — a false
economy worse than the Opus it avoids. Sonnet is the workhorse; Haiku is only
for genuinely trivial rote.

For Codex sessions, use the same three-way dispatch discipline with Codex model
overrides:

- **Mechanical / trivial rote -> `gpt-5.3-codex-spark`.** Use for exact,
  low-judgment work: grep/inventory, command output collection, line lookup,
  format-only edits, precise find/replace, or verification against explicit
  acceptance criteria.
- **Ordinary delegated work -> `gpt-5.4`.** This is the Codex workhorse for
  bounded implementation, source synthesis, ordinary doc drafting, focused
  review, and anything that is not clearly mechanical or judgment-heavy.
- **Genuine judgment -> `gpt-5.5`.** Use when the task materially depends on
  architecture, doctrine, irreversible tradeoffs, adversarial reasoning,
  cross-surface reconciliation, or subtle correctness on shared contracts.

Do not silently substitute `gpt-5.4-mini` for the ordinary Codex workhorse. It
exists in the tool surface, but the owner-selected Codex rule for this doctrine
is mechanical -> Spark, ordinary -> 5.4, judgment -> 5.5. `gpt-5.4-mini` remains
an operator/tooling option only when separately justified or re-decided.

If a delegated task mixes tiers, split it when the outputs can be cleanly
separated. If it cannot be split without losing the point of the delegation,
route to the highest tier required by any material part of the task. If the
classification is merely uncertain, choose the ordinary workhorse; if the
uncertainty is about doctrine, lock-in, review authority, or irreversible
product/workflow impact, choose the judgment tier.

## Enforcement: pinned agent definitions, NOT a global cap

Verified Claude Code model-resolution order (highest → lowest):

1. `CLAUDE_CODE_SUBAGENT_MODEL` env var
2. per-call `model` arg on the Agent/Task tool
3. the agent definition's `model` frontmatter
4. inherit the parent (main loop) model

Enforcement is **(3)**: pin the model in the agent definition. Once work is
routed to `worker`/`mechanical`, the tier holds even if the orchestrator passes
no `model` — it can no longer silently inherit Opus.

**Rejected: `CLAUDE_CODE_SUBAGENT_MODEL` as a global default.** It sits at the
TOP of resolution and overrides even an explicit `model: opus` request, so
setting it to `sonnet` would make Opus subagents *impossible*. That is
over-restraint (it removes the escalation path), so Orca does **not** set it.
The control we want is "cheap by default, easy to escalate," not "block Opus."

**Hooks (optional, not adopted now).** A PreToolUse hook on the Agent tool can
inspect and even rewrite the model. Reserve it for a future *soft* signal (e.g.
log Opus spawns) if routing discipline proves insufficient — not a hard block,
which would re-introduce the over-restraint this doctrine avoids.

## Enforcement: Codex dispatch payloads, not hooks

In Codex, tiering is applied at the `spawn_agent` call boundary when delegation
is actually authorized. The chief architect classifies the subtask first, then
sets the `model` override only when the classification intentionally differs
from inheriting the parent model.

Codex `agent_type` is role selection (`default`, `explorer`, `worker`), not the
model tier. Do not set `agent_type` to `default`, `null`, empty, or same-as-parent
to express model inheritance. Use `agent_type` only when the role matters:
`explorer` for specific read-only codebase questions, `worker` for bounded
repo-changing execution, and omit it otherwise.

This preserves `.agents/workflow-overlay/decision-routing.md` Subagent Runtime
Payload Safety: inherited runtime defaults are omitted fields; explicit
runtime fields are used only for a real override, never as decorative defaults.

## Operating rule (for the orchestrator)

When spawning from Claude Code, default delegated work to `worker` (Sonnet). Use
`mechanical` (Haiku) for trivial rote. Reach for Opus (`general-purpose` /
explicit `model: opus`) only when the task earns it -- and when it does, do so
without hesitation.

When spawning from Codex, classify every delegated task before the call:

| Dispatch class | Codex model override | Use for |
| --- | --- | --- |
| `mechanical` | `gpt-5.3-codex-spark` | trivial rote, exact extraction, explicit verification, format-only work |
| `ordinary` | `gpt-5.4` | default delegated work; implementation, synthesis, ordinary review |
| `judgment` | `gpt-5.5` | doctrine, architecture, irreversible tradeoffs, adversarial reasoning |

Record the classification in the subagent prompt when it would help later
review: `dispatch_class`, `model_override`, and the one-sentence reason. Do not
turn that receipt into a runtime-model recommendation inside model-neutral
review-lane artifacts; this doctrine governs spawn-time operator/tooling
choice, not review-lane prompt content.

## Non-claims

Advisory delegation doctrine. Not validation, readiness, a cost guarantee, or a
hard gate. It does not change any project's source hierarchy, review lanes, or
lifecycle authority; it governs only which model tier delegated subagents use.
It is not a Codex PreToolUse/PostToolUse hook and does not claim deterministic
runtime enforcement beyond the observed `spawn_agent` payload fields.

## Propagation

- Added: `.claude/agents/worker.md` (sonnet), `.claude/agents/mechanical.md` (haiku).
- Pointer added in `.agents/workflow-overlay/decision-routing.md` (delegation routing owner).
- Amended for Codex: `multi_agent_v1.spawn_agent` assumption gate and
  mechanical/ordinary/judgment model map.
