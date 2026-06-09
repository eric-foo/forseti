# Orca Repo Map v0

```yaml
retrieval_header_version: 1
artifact_role: Repository map
scope: Compact navigation map for Orca source loading and prompt setup.
use_when:
  - Choosing a bounded source pack before a CA prompt, review prompt, or product artifact.
  - Orienting a new thread without bulk-loading the repository.
  - Deciding which product, prompt, review, research, or workflow files are adjacent to a task.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
stale_if:
  - New top-level folders (under the repo root or docs/) are added.
  - orca-harness/ packages, adapters, runners, fixtures, or its build authorizations are added or reorganized.
  - Core Spine, Data Capture Spine, Cleaning Spine, Judgment Spine, offer, proof, or prompt families are materially reorganized.
  - Reddit CloakBrowser/proxy allowance, Candidate URL Intake, Reddit Graph Frontier Lane, or Source Capture Armory routing changes.
  - .agents/workflow-overlay/source-of-truth.md changes source hierarchy or the doctrine-change propagation contract.
  - A later repo-map artifact supersedes this file.
```

- Status: ACTIVE_RETRIEVAL_MAP (retrieval-only; source authority remains in `.agents/workflow-overlay/source-of-truth.md`)
- Artifact type: Workflow navigation artifact
- Scope: Repo navigation and source-pack selection
- Refreshed: 2026-06-09 (Signal Content Record v0 + ECR harness modules registered; Reddit Graph Frontier / CloakBrowser routes preserved)
- Implementation authorized: no

## How To Use This Map

Use this map to choose files. Do not treat it as product authority.

For source precedence, open `.agents/workflow-overlay/source-of-truth.md`.
For source-loading budgets, open `.agents/workflow-overlay/source-loading.md`.
For artifact retrievability, body-opening shape, stale/recheck patterns, and
temporary-artifact anti-rot guidance, open
`docs/workflows/artifact_retrievability_guide.md`.

Start-route cue: when a task may change product doctrine, architecture
doctrine, workflow authority, validation philosophy, review authority, output
authority, or a lifecycle boundary, open the Doctrine Change Propagation
Contract in `.agents/workflow-overlay/source-of-truth.md` before selecting
downstream surfaces. That contract owns primary `trigger` plus
`related_triggers` grammar for multi-dimensional doctrine changes. Use this map
to identify likely downstream surfaces; do not treat the map itself as
propagation evidence.

## Active Hooks (IMPORTANT)

ORCA enforces load-bearing, mechanically-checkable rules at **tool
boundaries**, not by instruction alone. The owning principle is
`.agents/workflow-overlay/validation-gates.md` -> "Enforcement Placement"
(cross-referenced from `decision-routing.md`); the per-rule classification is
`docs/decisions/overlay_enforcement_placement_classification_v0.md`.

**Retrieval-header check.** A PostToolUse hook (matcher `Write|Edit`) in the
tracked `.claude/settings.json` runs:

```
python .agents/hooks/check_retrieval_header.py --hook
```

When a newly written or edited `*.md` in a durable in-scope folder (the folders
`.agents/workflow-overlay/retrieval-metadata.md` enumerates) is missing its
retrieval header, the hook returns a non-blocking advisory warning. It is
forward-only (only the file just touched), advisory (never blocks the edit),
and references the rule authority rather than restating it.

**Portable CLI / commit / CI backstop** (runs outside Claude Code too):

```
# advisory (exit 0): warn on any changed in-scope file missing its header
python  .agents/hooks/check_retrieval_header.py --changed          # Windows
python3 .agents/hooks/check_retrieval_header.py --changed          # POSIX
# strict gate (exit 1 on violation): for a pre-commit hook or CI
python3 .agents/hooks/check_retrieval_header.py --staged --strict
# explicit paths also work:
python3 .agents/hooks/check_retrieval_header.py path/to/artifact.md
```

**Reinstall (fresh clone, or if local settings were reset).** The checker
script is tracked at `.agents/hooks/check_retrieval_header.py`. The hook lives
in the tracked `.claude/settings.json`; if it is missing (for example only
present in a gitignored `.claude/settings.local.json`, or settings were reset),
re-add:

```json
"hooks": {
  "PostToolUse": [
    { "matcher": "Write|Edit",
      "hooks": [ { "type": "command",
                   "command": "python .agents/hooks/check_retrieval_header.py --hook",
                   "timeout": 10 } ] } ]
}
```

Hooks load at session start, so **restart the Claude Code session** after
editing settings. The command uses a path relative to the project root (where
Claude Code runs hooks); if your environment runs hooks from another directory,
use an absolute path or `"$CLAUDE_PROJECT_DIR/.agents/hooks/check_retrieval_header.py"`.
On POSIX, use `python3` if `python` is unavailable.

**Repo-map freshness check.** A second PostToolUse hook (matcher `Write|Edit`)
in the tracked `.claude/settings.json` runs:

```
python .agents/hooks/check_repo_map_freshness.py --hook
```

It reads THIS map as its own spec and, forward-only on the file just touched,
emits a non-blocking advisory when an edit adds navigable structure this map
does not yet cover -- the mechanically-detectable subset of the `stale_if:` block
above: a new top-level area (#1) or a new `orca-harness/` runner/adapter (#2).
Edits to `source-of-truth.md` get a coarser advisory nudge (#5). It stays silent
on ordinary content in already-mapped folders (a new `docs/decisions/*` is
reachable by convention, not a map event) and cannot see judgment-shaped
staleness -- "a spine was reorganized" (#3) or "routing doctrine changed" (#4) --
which stays with the Doctrine Change Propagation contract in
`.agents/workflow-overlay/source-of-truth.md` (which already lists this map as a
downstream surface).

**Portable CLI / commit / CI backstop** (runs outside Claude Code too):

```
# advisory (exit 0): report structural drift in the working tree
python  .agents/hooks/check_repo_map_freshness.py --changed          # Windows
python3 .agents/hooks/check_repo_map_freshness.py --changed          # POSIX
# strict gate (exit 1): block a commit that adds new structure without
# updating this map / a submap and without an acknowledgment
python .agents/hooks/check_repo_map_freshness.py --commit-msg "$1"   # commit-msg hook
python3 .agents/hooks/check_repo_map_freshness.py --changed --strict --message "$PR_BODY"  # CI
python .agents/hooks/check_repo_map_freshness.py --selftest          # self-check logic
```

To acknowledge a legitimate non-map change so the strict gate passes: for a
one-off, put `repo-map-ack: <reason>` in the commit message; for a recurring
class (generated scratch), add a backtick'd token to the "Generated/gitignored
scratch ... do not enumerate" list (this checker reads that list as its exclusion
source). Updating this map or a submap in the same change also satisfies the
gate. The check enforces map *shape*, never the truth of a route, and fails OPEN
on internal error. Reinstall = re-add the second PostToolUse entry beside the
retrieval-header hook in `.claude/settings.json`, then restart the session.

**Permission floor (protected paths + git lifecycle).** A second
enforcement-placement substrate (EP-01 + EP-03 in
`docs/decisions/overlay_enforcement_placement_classification_v0.md`), built as
Claude Code `permissions` rules — no script:

- **`ask` — git lifecycle, shared/tracked in `.claude/settings.json`:**
  `git push`, `git commit`, `git remote`, `gh pr`, `git reset --hard`,
  `git clean`, for both the `Bash` and `PowerShell` tools. Claude Code prompts for
  explicit approval; the approval is the authorization (`safety-rules.md`
  "...unless explicitly authorized"). Travels with the repo.
- **`deny` — protected paths, machine-local in `.claude/settings.local.json`:**
  writes/edits to external / installed-skill roots — `agent-workflow`, `jb*`,
  `~/.codex/{plugins,skills}`, `~/.claude/{plugins,skills}`, `~/.agents/skills`.
  Hard-blocked. Machine-specific absolute paths, so NOT tracked; a fresh clone
  re-adds its own external paths.
- Authority: `safety-rules.md` (the rules) + validation-gates "Enforcement
  Placement" (the placement principle). Config enforces existing rules; it
  changes no doctrine. EP-02 (impl-dir blocking) was deliberately excluded.
- Limits: Claude-Code-only (Codex unaffected — the resident instruction stays);
  `deny` is machine-local; restart the session to load; not a security boundary.

**Reinstall the permission floor (fresh clone, or if local settings were
reset).** The `ask` git-lifecycle rules live in the tracked
`.claude/settings.json`; the `deny` path rules live in the gitignored
`.claude/settings.local.json`, so a clone does NOT recover them — re-add both
(adjust the absolute paths to the local machine). In `.claude/settings.json`:

```json
"permissions": {
  "ask": [
    "Bash(git push*)", "PowerShell(git push*)",
    "Bash(git commit*)", "PowerShell(git commit*)",
    "Bash(git remote*)", "PowerShell(git remote*)",
    "Bash(gh pr*)", "PowerShell(gh pr*)",
    "Bash(git reset --hard*)", "PowerShell(git reset --hard*)",
    "Bash(git clean*)", "PowerShell(git clean*)"
  ]
}
```

In `.claude/settings.local.json` (machine-specific absolute paths):

```json
"permissions": {
  "deny": [
    "Edit(//c/Users/vmon7/Desktop/projects/agent-workflow/**)", "Write(//c/Users/vmon7/Desktop/projects/agent-workflow/**)",
    "Edit(//c/Users/vmon7/Desktop/projects/jb*/**)", "Write(//c/Users/vmon7/Desktop/projects/jb*/**)",
    "Edit(//c/Users/vmon7/.codex/plugins/**)", "Write(//c/Users/vmon7/.codex/plugins/**)",
    "Edit(//c/Users/vmon7/.codex/skills/**)", "Write(//c/Users/vmon7/.codex/skills/**)",
    "Edit(//c/Users/vmon7/.claude/plugins/**)", "Write(//c/Users/vmon7/.claude/plugins/**)",
    "Edit(//c/Users/vmon7/.claude/skills/**)", "Write(//c/Users/vmon7/.claude/skills/**)",
    "Edit(//c/Users/vmon7/.agents/skills/**)", "Write(//c/Users/vmon7/.agents/skills/**)"
  ]
}
```

Restart the Claude Code session after editing settings.

**Protected-action guard (PreToolUse) — the auto-mode enforcement.** The `ask`
config rules above are inert in auto / bypass mode (no human to prompt), so the
real enforcement of EP-01 + EP-03 is a `PreToolUse` hook that fires in ALL
permission modes:

- script: `.agents/hooks/guard_protected_actions.py` (tracked); matcher
  `Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit` in `.claude/settings.json`.
- blocks (exit 2): writes/edits into protected roots (`agent-workflow`, `jb*`,
  `~/.codex/{plugins,skills}`, `~/.claude/{plugins,skills}`, `~/.agents/skills`);
  and main-affecting git — landing a PR to `main` (`gh pr merge`), push to
  `main`, force-push, bare/ambiguous push — plus `reset --hard` / `clean`, via
  Bash or PowerShell. **Allows** an explicit non-main, non-force lane push
  (`git push -u origin <lane>`) so lanes prep PRs (per-lane PR flow in
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`); a
  human/authorized action lands the PR to `main`. Narrow: `commit`, generic
  deletion, and *mentions* of these in quoted strings are NOT blocked.
- references authority (`safety-rules.md`), fails OPEN on internal error, and has
  a selftest: `python .agents/hooks/guard_protected_actions.py --selftest`.
- authorized exception: run the action yourself, or temporarily remove the hook.

Reinstall the PreToolUse guard in `.claude/settings.json`:

```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit",
      "hooks": [ { "type": "command",
                   "command": "python .agents/hooks/guard_protected_actions.py",
                   "timeout": 10 } ] } ]
}
```

Restart the Claude Code session after editing settings.

**Future agents: reuse this pattern.** To enforce the next load-bearing,
deterministically-checkable rule, do not add another instruction -- add a
sibling checker under `.agents/hooks/` that references the rule's authority
(never restates it), advisory + forward-only with a `--strict` gate, wire a
PostToolUse hook the same way, and document it here. See
`.agents/workflow-overlay/validation-gates.md` -> "Enforcement Placement".

This note is navigation and discoverability only; the hook and checker are
advisory tooling, not validation, readiness, or source-of-truth promotion.

## Reddit CloakBrowser / Proxy Allowance Quick Route

If a new CA is deciding whether bounded pre-commercial Reddit work may use
CloakBrowser, anti-blocking, residential/rotating proxies, or old Reddit HTML,
do not block by default. Open these in order:

| Question | Open |
| --- | --- |
| Is CloakBrowser/proxy-backed Reddit access allowed at all? | `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` |
| What is the Reddit-specific capture/intake route? | `docs/workflows/data_capture_spine_consolidation_map_v0.md` |
| Is this Candidate URL Intake rather than Armory capture? | `docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`, then `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md` |
| Is bounded graph/frontier scouting accepted? | `docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` |
| How should old Reddit search/listing HTML be saved, parsed, and interpreted? | `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md` |
| What are the proxy and anti-blocking hard stops? | `docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md` |
| What is implemented now? | `docs/product/source_capture_toolbox/README.md`, then `orca-harness/docs/source_capture_agent_runbook.md` and the named runner/adapter files |

Current map-level summary: CloakBrowser is the approved primary anti-blocking
route for bounded pre-commercial Reddit capture, and residential/rotating
proxies are not blanket stop conditions inside that pre-commercial/free
anti-blocking posture. Candidate URL Intake may record this approved downstream
route, but it does not invoke CloakBrowser, configure proxies, emit Source
Capture Packets, fetch bodies/comments/profiles, auto-promote URLs, or authorize
broad crawling, storage, scheduler/dashboard, deployment, production runtime,
commercial fetch, ECR, Cleaning, Judgment, fixture admission, or source-quality
scoring. For no-live operator-supplied old Reddit HTML pilots, open
`docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`
before interpreting empty results, `search-title` anchors, raw HTML input
hygiene, or candidate-subreddit discovery with visible volume.

Reddit Candidate URL Intake is also the bounded first-contact sourcing path for
declared Reddit source surfaces when a run envelope and live access
authorization are supplied. The implemented runner is
`orca-harness/runners/run_reddit_candidate_intake_live.py`; it writes candidate
rows, provenance, and a live-run receipt only.

Reddit Graph Frontier is accepted only as a bounded planning lane with a Graph
Frontier Register. It may choose the next candidate seed and prepare a fresh
bounded run, but it does not authorize same-run traversal, Graph Frontier-owned
live Reddit fetch, automatic capture, broad crawling, Source Capture, Data
Capture, storage, scheduler, dashboard, or production runtime. Operator-facing
nickname: "crawling graph." The runner is
`orca-harness/runners/run_reddit_graph_frontier_register.py`.

## Top-Level Structure

| Path | Role |
| --- | --- |
| `AGENTS.md` | Canonical root instructions, global behavior, and triggers to Orca owner docs. |
| `.agents/workflow-overlay/` | Orca overlay authority for project facts, folders, source rules, prompt rules, validation, safety, and review lanes. |
| `orca-harness/` | Bounded authorized implementation backing Data Capture source acquisition and the v0.14 Judgment Harness (capture adapters, source-observability, schemas, scoring, runners, fixtures, tests). Navigation context only; not runtime, acceptance, or readiness. See the Orca Harness section. |
| `docs/decisions/` | Decision records. |
| `docs/product/` | Product contracts, Core Spine artifacts, proof plans, source/evidence standards, offer, buyer-proof, and decision artifacts. |
| `docs/prompts/` | Prompt artifacts, wrappers, reruns, reviews, and local templates. |
| `docs/research/` | Research artifacts and consulting-judgment corpus material. |
| `docs/review-inputs/` | Prepared review inputs. |
| `docs/review-outputs/` | Review reports and adversarial artifact reviews. |
| `docs/workflows/` | Workflow records, operational notes, and repo maps. |
| `docs/migration/` | Import and migration records. |
| `docs/hygiene/` | Triage and cleanup queues. |
| `docs/_inbox/` | Non-authoritative scratch and parked material. |
| `slot1_*` / `slot2_*` `_CAPTURE_operator_workfile.md` (repo root) | Loose Data Capture pressure-test operator workfiles parked at the repo root; un-triaged drift, not authoritative. Route through `docs/hygiene/queue.md`. |

## Overlay Files

| Path | Use for |
| --- | --- |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule. |
| `.agents/workflow-overlay/project-authority.md` | Project identity, stage, and forbidden drift. |
| `.agents/workflow-overlay/source-of-truth.md` | Source precedence, conflict rules, and doctrine-change propagation contract, including primary and related trigger grammar. |
| `.agents/workflow-overlay/source-loading.md` | Read packs, context budgets, and prompt source capsules. |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted artifact folders and folder rules. |
| `.agents/workflow-overlay/artifact-roles.md` | Artifact role bindings and permissions. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval-header contract. |
| `.agents/workflow-overlay/prompt-orchestration.md` | Prompt artifact, wrapper, preflight, and rerun rules. |
| `.agents/workflow-overlay/template-registry.md` | Orca-local prompt template registry. |
| `.agents/workflow-overlay/product-proof.md` | Buyer-proof semantics and non-claims. |
| `.agents/workflow-overlay/communication-style.md` | Orca response style. |
| `.agents/workflow-overlay/validation-gates.md` | Validation gate expectations. |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules. |
| `.agents/workflow-overlay/delegated-review-patch.md` | Provisional, opt-in Delegated Review-and-Patch convention for high-stakes authored artifacts; not a bound review lane. |
| `.agents/workflow-overlay/safety-rules.md` | Safety and forbidden drift. |
| `.agents/workflow-overlay/skill-adoption.md` | Skill source and adoption status. |

## Workflow Navigation Files

| Path | Use for |
| --- | --- |
| `docs/workflows/artifact_retrievability_guide.md` | Operational guidance for durable artifact headers, body-opening source surfaces, stale/recheck patterns, repo-map/index treatment, report-only retrieval checks, and hygiene anti-rot. |
| `docs/workflows/orca_repo_map_v0.md` | Compact navigation map for bounded source-pack selection and prompt setup. |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Data Capture Spine repo submap. Open before enumerating capture owner docs. |
| `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | Judgment Spine submap. Open before enumerating Judgment owners across `docs/research/judgment-spine/` and `docs/product/judgment_spine_*`. |

## Orca Harness

`orca-harness/` is bounded, authorized implementation backing Data Capture
source acquisition and the v0.14 Judgment Harness. It is navigation context
here, not a runtime, acceptance, or readiness claim. Build scope is controlled
by the authorization decisions named below; surfaces outside them (production
runtime, commercial fetch, broad crawling, ECR, Cleaning, Judgment
design) remain gated.

| Path | Use for |
| --- | --- |
| `orca-harness/capture_spine/` | Capture Spine local support for Reddit Candidate URL Intake projection and Reddit Graph Frontier register/receipt helpers. Not Source Capture Armory execution, Source Capture Packet output, storage, scheduler, dashboard, or production runtime. |
| `orca-harness/source_capture/` | Source-capture packet core: models, writer, CLI support, and plaintext receipts. |
| `orca-harness/source_capture/adapters/` | Bounded capture adapters (direct HTTP, media/asset, Archive.org, browser snapshot, authenticated browser, Reddit API where present). CloakBrowser Snapshot anonymous non-persistent v0 now has a live engine and packet runner for one explicitly supplied URL; Reddit discovery/consolidation, proxy/session behavior, commercial fetch, broad crawling, storage, dashboards, deployment, and production runtime remain separately gated. |
| `orca-harness/source_observability/` | Local operator-record posture checker and limitation reporter. |
| `orca-harness/ecr/` | Evidence Candidate Record source-side integrity postures (SP-1/2/3/6): per-packet/slice derived records keyed to the `SourceCapturePacket`; bind no `EvidenceUnit`; JSG-01 frozen. Boundary context: `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`. |
| `orca-harness/signal_content/` | Signal Content Record (v0): the second derived-record kind (content — "what a signal says"), parallel to `ecr/`; wedge-agnostic StrictModel + validators, references packet/ECR by key, no deriver/persistence/binding. Direction: `docs/product/core_spine_v0_signal_content_record_architecture_v0.md`. |
| `orca-harness/schemas/` | Pydantic v2 models for cases, judgments, scoring, and probes (v0.14). |
| `orca-harness/scoring/` | Deterministic band scorer and mapping table (v0.14 Step A); not judgment-quality proof. |
| `orca-harness/reports/` | Report-rendering code (case and source-observability reports); generated dry-run outputs under it are gitignored. |
| `orca-harness/runners/` | CLI entrypoints for case runs, memorization probe, bounded Candidate URL Intake live first-contact sourcing, Reddit Graph Frontier / crawling graph register preparation, source-capture packets, and source-observability reports. |
| `orca-harness/cases/` | Tracked deterministic fixture case(s) (e.g. TR/Casetext v0.14) with evidence, packet, and ledger; generated `scores/` and run outputs are gitignored. |
| `orca-harness/config/` | Static YAML config (contestants, models, prompts) consumed by runners. |
| `orca-harness/docs/` | Harness operating docs: source-capture packet and agent runbook, source-observability record guide, and scalability note. |
| `orca-harness/tests/` | `unit/`, `contract/`, and `integration/` tests, including no-LLM-import and no-tools contract guards. |
| `orca-harness/harness_utils.py`, `Makefile`, `pyproject.toml` | Shared utilities, dev shortcuts, and package metadata (optional `[browser]` Playwright extra). |

Controlling build authority:
`docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
(source-capture armory) and
`docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md`
(local source-observability support).

Generated/gitignored scratch — do not enumerate or treat as authoritative:
`orca-harness/_test_runs/`, `_auth_state/`, `pytest_*` temp dirs,
`reports/source_observability/*_dry_run.*`, `cases/*/*/scores/`, and
`memory/logs/`.

## Product Anchor Files

Use these before broad product architecture or CA setup:

| Path | Use for |
| --- | --- |
| `docs/decisions/turn_08_product_thesis_v0.md` | Orca thesis, value proposition, strategic center, broad product boundary. |
| `docs/product/orca_offer_hypothesis_v0.md` | Offer hypothesis, buyer-facing language, first proof offer, ICP boundary. |
| `docs/product/orca_buyer_proof_packet_v0.md` | First buyer-proof packet, proof gates, pull signals, kill/graduation criteria. |
| `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md` | Selected first ICP wedge and decision-family focus. |
| `docs/product/orca_product_proof_lead_charter_v0.md` | Product proof lead role and proof execution boundary. |

## Judgment Spine

The Judgment Spine spans **both** trees — `docs/research/judgment-spine/` (thesis, manifest, cases, harness) and `docs/product/judgment_spine_*` plus the conductor. **Open the consolidation map first**: it is the single `retrieval_only` entry that orients across both trees and routes one hop to every owner. Do not pre-load the owners from here.

| Path | Use for |
| --- | --- |
| `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | **Judgment Spine entry map — open first.** Per-area summary, owner-native status, and one pointer for thesis, cases/manifest, conductor, gate ownership, evidence ladder, JSG-08, and the harness; routes to the owners rather than restating them. The path toward judgment-quality evidence, not proof; by-hand runs cap at product-learning. |

## Data Capture Spine

The Data Capture Spine spans product authority, source-access decisions, Source
Capture Armory docs, source-quality support, and `orca-harness/` implementation.
**Open the repo submap first** for capture/armory work: it is the
`retrieval_only` entry that orients across these surfaces and routes one hop to
the owner sources. Do not pre-load all capture artifacts from this map.

| Path | Use for |
| --- | --- |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | **Data Capture Spine repo submap — open first.** Routes to Capture obligations, source-access boundary, build authorization, method plan, Source Capture Armory README, packet lifecycle, harness runners, source-quality support, and current Reddit pre-commercial routing. Map only; not validation, readiness, source-access permission, or implementation authority. |
| `docs/product/data_capture_spine_future_exploration_lanes_v0.md` | Capture-spine-level backlog of deferred, legally-gated capabilities (relationship-graph analytics; contact/outreach) surfaced during LinkedIn discovery design — non-authorizing, out of scope for all discovery lanes. |

## Core Spine Files

| Path | Use for |
| --- | --- |
| `docs/product/core_spine_v0_product_contract.md` | Core Spine product contract and eight primitives. |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | Manual information-production foundation and Evidence Unit standard. |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Data Capture/Cleaning/Judgment boundary and Evidence Candidate Record setup context. |
| `docs/product/core_spine_v0_signal_content_record_architecture_v0.md` | Signal Content Record (v0) architecture DIRECTION — the second derived-record kind ("what a signal says"), parallel to the ECR integrity postures and structuring the IPF Evidence Unit content vocabulary; records the owner carrier/lifecycle/decision-relevance-tag decisions and the bounded content-field ratification. Direction only; the final Evidence Unit field architecture stays owner-reserved and JSG-01 frozen. v0 model lives in `orca-harness/signal_content/`. |
| `docs/product/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | Proposed Core Spine design note on placing independent-corroboration vs artificial-amplification discipline across the Cleaning/Judgment boundary; proposed, not validated. |
| `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` | Daimler advisory claim-tier classification decision recording the current no-durable-evidence state, required product-learning receipt before any evidence claim, and blocked buyer-proof/judgment-quality claims. |
| `docs/product/engagement_logic_registry_v0.md` | Signal-use and engagement interpretation registry. |
| `docs/product/core_spine_v0_proof_protocol_v0.md` | Core proof protocol. |
| `docs/product/core_spine_v0_proof_input_selection_v0.md` | Proof input-selection rules. |
| `docs/product/core_spine_v0_proof_packet_preflight_v0.md` | Proof packet preflight. |
| `docs/product/core_spine_v0_proof_case_selection_brief_v0.md` | Early proof case-selection brief; status BLOCKED_OWNER_CANDIDATES_NEEDED. For current case/backtest selection see the heavyweight discovery pass (`docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` and `..._results_part_2_v0.md`), which produced the candidates the brief was blocked on. |

For Data Capture / Source Capture Armory detail, open the repo submap at
`docs/workflows/data_capture_spine_consolidation_map_v0.md`; this repo map
intentionally does not duplicate the owner-doc inventory.

## Data Capture Harness Operating Model

Route Data Capture operating-model and commissioning-plan questions through the
repo submap at
`docs/workflows/data_capture_spine_consolidation_map_v0.md` first. That submap
owns the one-hop pointers to v2 operating-model architecture, owner acceptance,
obligation baseline, lane thesis, and commissioning plan. This repo map does
not duplicate that inventory.

## Method Validation And Replay Files

Use only when method-validation history, replay evidence, or case-frame locks
are directly relevant. Do not include by default in Data Capture Spine CA prompts.

Key files:

- `docs/product/core_spine_v0_method_validation_replay_packet_v0.md`
- `docs/product/core_spine_v0_method_validation_rubric_v0.md`
- `docs/product/core_spine_v0_method_validation_case_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md`
- `docs/product/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md`

## First Proof And Discovery Files

Use for customer discovery, target selection, first proof packet prep, or live
proof readiness questions.

Key files:

- `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`
- `docs/product/core_spine_v0_first_proof_run_charter_v0.md`
- `docs/product/core_spine_v0_first_proof_run_locks_v0.md`
- `docs/product/core_spine_v0_first_proof_run_packet_v0.md`
- `docs/product/core_spine_v0_first_proof_run_jb_client0_slice_v0.md`
- `docs/product/core_spine_v0_first_proof_run_bt204_backtest_slice_v0.md`
- `docs/product/core_spine_v0_first_proof_run_sh01_shadow_slice_v0.md`
- `docs/product/orca_discovery_batch_0_target_selection_brief_v0.md`
- `docs/product/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md`
- `docs/product/orca_discovery_batch_0_candidate_context_scan_v0.md`
- `docs/product/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md` (discovery-scope charter), `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` (READY_FOR_OWNER_CASE_SELECTION), and `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md` (backtest candidates; proposes BT2-01 Chegg/ChatGPT) — the heavyweight proof-case discovery pass that produced the candidates the older case-selection brief was blocked on.

## Backtest Specimens

Use when the task is specifically about historical cutoff discipline or the
Unity runtime-fee specimen:

- `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`

## Prompt Families

| Path | Use for |
| --- | --- |
| `docs/prompts/product-planning/` | Product planning prompt drafts. |
| `docs/prompts/feature-planning/` | Feature planning prompt drafts. |
| `docs/prompts/deep-thinking/` | Deep reasoning prompt drafts. |
| `docs/prompts/handoffs/` | Handoff prompt drafts. |
| `docs/prompts/reviews/` | Review prompts. |
| `docs/prompts/reruns/` | Rerun prompts. |
| `docs/prompts/patches/` | Patch prompts (accepted family; no drafts created yet). |
| `docs/prompts/wrappers/` | Thin wrapper prompts. |
| `docs/prompts/templates/` | Local prompt templates. |
| `docs/prompts/hygiene-queue/` | Current drift/parking area; not listed as an accepted prompt-family folder in the overlay. |

A few Data Capture pressure-test prompts currently sit unfiled at the
`docs/prompts/` root rather than in a typed family folder; treat them as drift
pending hygiene triage.

## Research And Review Areas

| Path | Use for |
| --- | --- |
| `docs/research/consulting-judgment-corpus/` | Consulting-judgment corpus, prompts, lane outputs, synthesis, candidate screens, backtestability, and reject patterns. |
| `docs/research/judgment-spine/` | Judgment Spine corpus (parent contract, manifest, case tracks, harness, case-learning). **Open the consolidation map first** — see the Judgment Spine section above; it routes to every owner across both trees instead of enumerating them here. |
| `docs/research/daimler_advisory_001_source_registry_v0.md` | Manual Daimler source-unit registry separating participant-safe candidates, date ambiguity, missing evidence, and reveal-only material before any packet rebuild or judgment-quality claim. |
| `docs/research/packing-phase/` | Boundary note for decision-packet construction between cleaned evidence and Judgment Harness inputs. |
| `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md` | Decision record on pre-sale Judgment Spine model-execution evidence tiers (subscription/manual/chat default; raw API/harness as optional gate-bearing plumbing) and how to read no-case smoke-test / raw-API runner artifacts relative to buyer proof. |
| `docs/review-outputs/` (root) | Flat collection of harness implementation/code-review outputs (source-capture adapters, source-observability helper, no-tools probe and execution-foundation); advisory findings only, co-located at the folder root rather than a typed subfolder. |
| `docs/review-outputs/adversarial-artifact-reviews/` | Adversarial artifact review reports, including the Daimler advisory and Canoo/Walmart Judgment Spine fixture-review families. |
| `docs/review-outputs/method-validation/` | Method-validation review outputs. |
| `docs/review-outputs/proof/` | Proof review outputs (currently a README placeholder). |

## Daimler Advisory & Probe Lane

Daimler is the selected internal advisory proof slice and first Judgment Spine
v0.14 fixture candidate. The whole lane is facilitator-only and carries no
durable evidence and no judgment-quality, buyer-proof, blind-use, or
fixture-admission claim. See also the mapped Daimler claim-tier classification
(Core Spine Files) and source registry (Research And Review Areas).

| Path | Use for |
| --- | --- |
| `docs/decisions/advisory_proof_slice_definition_v0.md` and `docs/decisions/advisory_runbook_scope_daimler_v0.md` | Define Daimler as the non-gate-clearing advisory proof slice and scope a future operator-facing advisory runbook; docs-only, no model execution or participant-packet exposure authorized. |
| `docs/decisions/daimler_advisory_run_authorization_decision_v0.md` and `docs/decisions/daimler_advisory_run_001_authorization_record_v0.md` | Advisory-run authorization state (gates currently closed) and the specific DAIMLER_ADVISORY_001 authorization for participant-safe prompt preparation only; not model-run authorization. |
| `docs/decisions/daimler_v0_14_probe_execution_authorization_decision_v0.md` and `docs/decisions/daimler_v0_14_backup_probe_authorization_decision_v0.md` | Bounded public-identifiers-only memorization-probe authorizations for the primary (GPT-5.5) and backup (Claude Opus) families; no scoring, blind-use, or fixture admission. |
| `docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md` | Facilitator-only gate outcome: no selected target family cleared the memorization-probe gate (GPT-5.5 access-blocked; Claude Opus failed with a tool-isolation caveat); blind-use/fixture-admission not authorized. |
| `docs/product/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | Toolkit capability specs inferred from the Daimler source fanout (cutoff provenance, evidence registry, packet compiler, isolation checker); planning only, not build/runtime authorization or a judgment-quality claim. |

## Inbox Warning

`docs/_inbox/` is non-authoritative. It currently contains contaminated
method-validation replay outputs and compacted-run material. Do not read or
promote those files unless the task explicitly concerns contamination,
recovery, hygiene, or comparison against canonical promoted files.

## Recommended Read Packs

### Data Capture Spine Setup CA

Use the canonical read-pack rule in
`.agents/workflow-overlay/source-loading.md#data-capture-spine-ca-read-pack`.
This map is only a navigation aid and must not fork the Data Capture Spine
source-loading rule.

Navigation pointers for that pack live in the Product Anchor Files and Core
Spine Files sections above. Do not read the target files in full by default.
Use the targeted sections named by `source-loading.md`, then expand only when a
concrete source gap could change the Data Capture Spine CA prompt.

Exclude by default:

- method-validation replays;
- first proof run packets;
- review outputs;
- research corpus;
- `docs/_inbox/`.

### Data Capture Setup / Pressure-Test Packet

Use this packet when continuing Data Capture Spine setup, obligation-contract
pressure testing, or source-family fixture checks. This is a navigation pointer
only; it does not claim that Data Capture Spine is closed, source-of-truth
promoted, accepted, formally validated, ready for ECR/Cleaning handoff,
implementation-ready, runtime-ready, or Cleaning-complete.

Start with:

- `docs/workflows/data_capture_spine_consolidation_map_v0.md` for orientation.
- `.agents/workflow-overlay/source-loading.md#data-capture-intake-surface--msp-pressure-test-target-pack` for the canonical pressure-test read-pack rule.

Then open only the controlling owner doc named by the submap or source-loading
pack for the current claim. Do not bulk-load all capture sessions, historical
fixture files, review outputs, or Source Capture Armory docs from this repo map.

For strict source-pinning claims, compute fresh hashes from the current target
files. Do not rely on historical hashes recorded in older prompts, reviews, or
map versions unless the task is explicitly reviewing that older state.

### Offer Or Buyer Proof Work

Start with:

- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`
- `.agents/workflow-overlay/product-proof.md`

### Core Spine Evidence Standard Work

Start with:

- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- **Open `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` first** for any Judgment Spine work; it routes to the ladder, gate ownership map, conductor, and JSG-08 owner contract below.
- `docs/product/judgment_spine_evidence_ladder_architecture_v0.md` when the work classifies Judgment Spine claim tier, proof tier, buyer-proof boundary, or judgment-quality boundary.
- `docs/product/judgment_spine_gate_ownership_map_v0.md` when the work needs to route or block Judgment Spine gate ownership before claim promotion.
- `docs/product/judgment_quality_promotion_operating_model_v0.md` — **the Judgment Spine conductor; open this FIRST for the judgment run lane** (running or planning any case through gates JSG-01 to JSG-10). It sequences the gates and routes to the evidence ladder, gate ownership map, and JSG-08 owner contract rather than restating them; use it to decide a run lifecycle state or check what a partial or by-hand run can claim. It is the path toward judgment-quality evidence, not proof — by-hand runs cap at product-learning.
- `docs/product/engagement_logic_registry_v0.md`
- nearest boundary or proof artifact named by the request.

### Prompt Or Review Prompt Work

Start with:

- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/template-registry.md`
- relevant prompt template under `docs/prompts/templates/`
- the target source artifact being prompted or reviewed.

## New Thread Guidance

Use a new thread or compact handoff when the next task needs more than one
recommended read pack, more than six full artifacts, or both repo-map refresh
and CA prompt drafting. The handoff should cite this map, the source-loading
overlay, the target read pack, and the files excluded by default.

## Direction Change Propagation - Reddit CloakBrowser / Proxy Allowance Quick Route

```yaml
direction_change_propagation:
  doctrine_changed: "The top-level repo map now exposes a Reddit CloakBrowser/proxy allowance quick route so new CA lanes see that CloakBrowser is the approved primary anti-blocking route and residential/rotating proxies are not blanket stop conditions for bounded pre-commercial Reddit capture, while Candidate URL Intake remains non-executing rows/provenance only."
  trigger: workflow_authority
  related_triggers:
    - architecture_doctrine
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
    - "docs/product/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
    - "docs/product/source_capture_toolbox/README.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "The canonical read-pack still routes Data Capture work through the consolidation sub-map. This patch adds a top-level anti-friction cue, not a new source-loading pack."
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "The Armory README already records CloakBrowser implementation limits and non-claims. This patch changes repo-map discoverability, not Armory implementation."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "The authorization already controls CloakBrowser/proxy allowance. This patch does not change the owner decision."
  stale_language_search: "rg -n \"Reddit CloakBrowser / Proxy Allowance Quick Route|CloakBrowser is the approved primary|residential/rotating|Candidate URL Intake may record this approved downstream route|approved primary anti-blocking route|not blanket stop\" docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/product/data_capture_spine_candidate_url_intake_contract_v0.md docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md docs/product/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
  stale_language_search_result: "Executed 2026-06-06 after this patch. Hits were the new repo-map quick route, the Data Capture sub-map allowance summary, the parent Candidate URL Intake downstream access posture, the Reddit Candidate URL Intake specialization, and controlling source-access authorization / Reddit success-signal hard-stop language. No checked surface required a new CA to block CloakBrowser or residential/rotating proxies by default for bounded pre-commercial Reddit capture."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not source-access boundary amendment"
    - "not implementation authorization"
    - "not live Reddit authorization"
    - "not proxy implementation proof"
    - "not Source Capture Packet generation"
    - "not broad crawling, storage, dashboard, scheduler, deployment, production runtime, ECR, Cleaning, Judgment, fixture admission, source-quality scoring, or commercial authorization"
```

## Direction Change Propagation - Reddit Graph Frontier Route

```yaml
direction_change_propagation:
  doctrine_changed: >
    The top-level repo map now exposes Reddit Graph Frontier as an accepted
    bounded planning lane with a Graph Frontier Register, while preserving the
    no-same-run-traversal, no-Graph-Frontier-owned-live-fetch, no-capture,
    no-storage, no-scheduler, no-dashboard, and no-production-runtime
    boundaries.
  trigger: workflow_authority
  related_triggers:
    - architecture_doctrine
    - output_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/workflows/data_capture_spine_consolidation_map_v0.md"
    - "docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md"
    - "docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  intentionally_not_updated:
    - path: "docs/product/source_capture_toolbox/README.md"
      reason: "Graph Frontier is not Source Capture Armory and does not emit Source Capture Packets."
    - path: "orca-harness/docs/source_capture_agent_runbook.md"
      reason: "No runner behavior changed and this patch does not authorize implementation execution."
  stale_language_search: "rg -n \"Future Crawler-Graph|future crawler|may be architected|architected or rejected|candidate_graph_ledger|crawler_graph_exploration_lane|should wait for an architecture decision|Commission the separate crawler-graph|accepted Reddit Graph Frontier|Graph Frontier Register\" docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/product/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md"
  stale_language_search_result: "Executed 2026-06-08 after this patch. Active route surfaces now point to accepted Reddit Graph Frontier and Graph Frontier Register language; the old future-question wording is not present in the active route surfaces checked."
  non_claims:
    - "not validation"
    - "not readiness"
    - "not Graph Frontier-owned live Reddit fetch authorization"
    - "not implementation authorization"
    - "not broad crawling authorization"
    - "not Source Capture"
    - "not Data Capture"
```

## Not-Proven Boundaries

This map does not prove acceptance, validation, readiness, buyer pull,
implementation authorization, source correctness, or freshness of every listed
artifact. Listing `orca-harness/` reflects authorized, bounded implementation
only; it does not assert runtime readiness, that its build scope is validated,
or that any gated surface (production runtime, API/commercial fetch, ECR,
Cleaning, Judgment) is authorized. Check the target artifact, retrieval header,
and current `git status` before strict claims.
