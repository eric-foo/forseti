# Source-Access Method Plan Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Plan-only prompt for a new Orca thread to design the Data Capture source-access method (how to reach blocked sources), under the loosened source-access boundary, without building anything.
use_when:
  - Spinning up a new thread to plan how Orca Data Capture reaches sources that block honest WebFetch.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_source_access_boundary_decision_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/README.md
stale_if:
  - The source-access boundary decision is amended or superseded.
  - The obligation contract is materially revised.
  - The owner authorizes building source-access tooling (this prompt is plan-only).
```

> **Paste this whole body into a new Claude session.** It is self-contained. The new session has none of this conversation's context.

---

## Objective

Plan — **do not build** — how Orca Data Capture should reach public sources that block honest automated fetching, so that future pressure-test captures and the eventual product can acquire source material defensibly. Produce a docs-only method plan that compares candidate methods, runs each through the loosened source-access boundary, and recommends an approach. **No code, no installs, no tooling, no runtime.**

## Required Preflight

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md` and follow the Orca overlay. Do not import `jb` rules.
3. Treat the worktree as dirty/untracked unless your own preflight proves otherwise.
4. This is **docs-only planning.** You may not write, build, install, run, stage, commit, or push code. Orca is in its non-implementation phase per `.agents/workflow-overlay/safety-rules.md`, and this prompt does NOT authorize exiting it.

```text
orca_start_preflight:
  agents_read: required
  overlay_read: required
  source_pack: custom source-access method planning pack (named below)
  workspace: C:\Users\vmon7\Desktop\projects\orca
  dirty_state_allowance: dirty/untracked expected; do not treat as validation
  edit_permission: docs-write (plan artifact only)
  output_mode: file-write
  target_scope:
    - docs/product/data_capture_source_access_method_plan_v0.md
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_source_access_boundary_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

## Context (why this thread exists)

Orca ran a Data Capture pressure test against 3 source-family slots. The source-mechanical subagent runs hit hard tool-layer blocks:

- `tealhq.com` returned HTTP 403 to all WebFetch attempts.
- `reddit.com` / `www.reddit.com` / `old.reddit.com` were blocked at the host level.
- `wallstreetoasis.com` returned 403.
- `web.archive.org` snapshot-content fetches were blocked at the tool layer (the `archive.org/wayback/available` JSON API still worked).
- `mergersandinquisitions.com` (slot 1) fetched fine, but content came back as paraphrase, not verbatim.

Full detail: `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/README.md` and the slot files beside it.

The owner has loosened the source-access boundary. The controlling standard is in `docs/product/data_capture_source_access_boundary_decision_v0.md`: a method is in-bounds if it accesses **public / market-level data** and Orca would **fully disclose how it was obtained.** Aggressive anti-blocking techniques (anti-detect browsers, proxy rotation, CAPTCHA/challenge handling) are permitted. The only hard line is **authentication / paywall bypass and access to private / non-public data**, which stays out regardless of disclosure.

## Source Hierarchy / Required Reads

1. Owner instruction (this prompt).
2. `AGENTS.md`, `.agents/workflow-overlay/README.md`, `safety-rules.md`.
3. `docs/product/data_capture_source_access_boundary_decision_v0.md` (the standard).
4. `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Obligation 2 + the agent allow/forbid line + capture modes).
5. `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/` (what blocked, what worked).
6. `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` (the slots, the no-runtime line).

## Source-Gated Method Sequence

1. Read authority + this prompt.
2. `REFERENCE-LOAD` `workflow-deep-thinking` (option comparison) — do not `APPLY` yet.
3. `SOURCE-LOAD` the context above.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only then `APPLY` deep-thinking to compare methods and recommend.

## Task

Produce a docs-only **source-access method plan** that:

1. **Enumerates candidate methods** for reaching the blocked sources. At minimum consider: official/sanctioned APIs (e.g., the Reddit API); honest JS-rendering headless browsers; honest crawlers such as crawl4ai in non-cloaking mode; rate-limited polite fetching with honest identification; archive/cache access via the wayback availability API + alternate archive hosts; commercial fetch/SERP services; and manual human-browser capture as a fallback.
2. **Runs each candidate through the loosened boundary standard** (public-data-only + fully disclosable; aggressive anti-blocking techniques permitted; hard line only on auth/paywall bypass and private/non-public data). Mark each method in-bounds / out-of-bounds with the reason.
3. **Maps method-to-source.** For each blocked source (Teal, Reddit, WSO, web.archive.org content, and the general production need), recommend the most defensible method that actually works for that source. Reddit specifically: evaluate the official API as the sanctioned route.
4. **Names what a build would entail** for the recommended method(s) — dependencies, rough effort, rough cost, legal/ToS flags — **without building or installing anything.** This is so the owner can later authorize a bounded build with eyes open.
5. **Flags legal/ToS/reputational risk** per source and per method. Note where real legal counsel is advisable before commercializing. You are not a lawyer; flag uncertainty.
6. **States sequencing.** Recommend whether building should wait until after the slot-1 capture discipline test completes (the commissioning plan's position) or proceed sooner, and why.

## Hard Constraints

- **Docs-only. No build.** No code, no installs (no `pip install crawl4ai`, no npm, nothing), no running scrapers, no API calls to test, no runtime, no automation, no tests, no packages.
- Do not exit Orca's non-implementation phase. This prompt does not authorize it; only the owner can, in a separate decision.
- Do not edit the obligation contract, the boundary decision, or any other accepted artifact. Reference them.
- Do not import `jb` rules. Do not edit installed/global/plugin skills.
- Do not commit, push, stage, or create PRs.
- Honor the agent allow/forbid line from the obligation contract when reasoning about what methods are even allowed.

## Output Mode And Contract

- Output mode: `file-write`.
- Write the plan to: `docs/product/data_capture_source_access_method_plan_v0.md`.
- Include the retrieval header per `.agents/workflow-overlay/retrieval-metadata.md`.
- Structure: status; source readiness; candidate methods table (method × boundary verdict × works-for-which-source × risk); method-to-source recommendation; what-a-build-would-entail (named, not built); legal/ToS/reputational flags; sequencing recommendation; non-claims; next authorized step.
- Close with a short headed human summary first, then the path/status receipt.

## Validation Gates

- Preflight complete; source pack, edit permission, target scope, dirty-state recorded.
- Boundary standard applied to every candidate method (public-data + disclosable; only auth/paywall bypass and private-data access are out).
- No build/install/runtime actions taken or authorized.
- Non-claims preserved: no implementation/runtime/tooling authorization, no legal sufficiency, no validation/readiness/buyer-proof claims.

## Non-Claims / Assumptions

This plan, when produced, does not authorize building anything, does not claim legal sufficiency, and does not exit the non-implementation phase. It is a docs-only method plan to inform a later, separately-authorized build decision.

`thread_operating_target_continuity:` new workstream (source-access method), branched from the Data Capture pressure-test lane; the parent lane's no-runtime line and the loosened boundary both carry forward.
