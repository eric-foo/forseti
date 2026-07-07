# Forseti Repo Map v0

```yaml
retrieval_header_version: 1
artifact_role: Repository map
scope: Compact navigation map for Forseti source loading and prompt setup.
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
  - New direct forseti-harness/ areas/packages, fixtures, or build authorizations are added, or existing harness areas are reorganized.
  - Core Spine, Data Capture Spine, Cleaning Spine, Judgment Spine, offer, proof, or prompt families are materially reorganized.
  - Reddit CloakBrowser/proxy allowance, Candidate URL Intake, Reddit Graph Frontier Lane, or Source Capture Armory routing changes.
  - .agents/workflow-overlay/source-of-truth.md changes source hierarchy or the doctrine-change propagation contract.
  - A later repo-map artifact supersedes this file.
```

- Status: ACTIVE_RETRIEVAL_MAP (retrieval-only; source authority remains in `.agents/workflow-overlay/source-of-truth.md`)
- Artifact type: Workflow navigation artifact
- Scope: Repo navigation and source-pack selection
- Refreshed: 2026-07-01 (current navigation baseline; detailed recent-change notes now live under `docs/workflows/repo_map_recent_changes/` to avoid top-hunk conflicts in parallel PRs).
- Recent map-change notes: use `docs/workflows/repo_map_recent_changes/` for optional one-file-per-change context; do not append chronology to this metadata block.
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

Cold fact lookup: check the Decisive-File Quick Index below FIRST; if a row
matches your question, open that file directly instead of walking the doctrine
chain.

## Decisive-File Quick Index (Cold Retrieval)

Fact-lookup shortcuts only (added 2026-07-04 after a measured cold-retrieval
run exceeded the source-loading read budget by verifying through the doctrine
chain). Each row names the single decisive file for a common question — open it
directly. Authority, precedence, and doctrine questions still route via
`.agents/workflow-overlay/source-of-truth.md`; these rows do not change source
hierarchy.

| Question | Open this file directly | Why it is decisive |
| --- | --- | --- |
| Fragrance facts: resolve a fragrance/house to canonical ids, note families, tier, dupes, per-fact provenance | `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml` | Self-describing DATA SSOT: facts, per-fact provenance, and the extension pattern live in-file; the backbone doc and object cards are authority/rationale surfaces, not the fact source. |
| Ontology type roster, namespaces, typed links, dimensions, deferred set | `forseti/product/spines/foundation/ontology/ontology.yaml` | Machine-readable SSOT of the adopted backbone; open the backbone doc only for rationale or conflict adjudication. |
| Any LinkedIn task | `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md` | The lane's canonical cold-start index (its own row says "open first"). |
| ECR spine orientation | `docs/workflows/ecr_spine_submap_v0.md` | Delegated submap for the ECR spine. |
| Data Capture spine orientation | `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Delegated Data Capture submap. |
| Source-capture access routes / anti-blocking playbook | `forseti/product/spines/capture/core/source_capture_toolbox/README.md` | Armory index over the tested per-source capture routes. |
| Known source capture-to-lake route (TikTok, YouTube, Instagram, Reddit, fragrance-native database, Retail/PDP, vendor pricing page) | `forseti/product/spines/capture/core/source_families/README.md` | Source-family lane catalog routes from the generic playbook/Armory into the owning family index and onward to runners/projection/lake/cleaning seams without duplicating lake doctrine. |

## Active Hooks (IMPORTANT)

Forseti enforces load-bearing, mechanically-checkable rules at **tool
boundaries**, not by instruction alone. The owning principle is
`.agents/workflow-overlay/validation-gates.md` -> "Enforcement Placement"
(cross-referenced from `.agents/workflow-overlay/decision-routing.md`); the per-rule classification is
`docs/decisions/overlay_enforcement_placement_classification_v0.md`.

**Retrieval-header check.** A PostToolUse hook (matcher `Write|Edit|MultiEdit`) in the
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
    { "matcher": "Write|Edit|MultiEdit",
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

**Repo-map freshness check.** A second PostToolUse hook (matcher
`Write|Edit|MultiEdit` in `.claude/settings.json`; `apply_patch|Edit|Write` in
`.codex/hooks.json`) runs:

```
python .agents/hooks/check_repo_map_freshness.py --hook
```

It reads THIS map as its own spec and, forward-only on the file just touched,
emits a non-blocking advisory when an edit adds navigable structure this map
does not yet cover -- the mechanically-detectable subset of the `stale_if:` block
above: a new top-level area (#1) or a new direct `forseti-harness/` area (#2).
Individual runner/adapter files under already-mapped harness areas are
discoverable by directory and do not force map edits.
When the file just touched IS this repo map and Git still shows it dirty after
the edit, the hook exits 2 as a blocking commit interrupt with the explicit-path
commit command. Edits to `.agents/workflow-overlay/source-of-truth.md` get a
coarser advisory nudge (#5). It stays silent
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
retrieval-header hook in `.claude/settings.json` and `.codex/hooks.json`, then
restart the relevant session.

**Placement check (EP-04) — built and wired.** A third substrate,
`.agents/hooks/check_placement.py`, enforces placement shape at the write
boundary: it reads `repo-structure.yaml` as its ONLY rule source (authority
stays in `.agents/workflow-overlay/artifact-folders.md`; binding in
`docs/decisions/orca_repo_structure_binding_v0.md`), WARNs on unplaced writes,
flags writes to the now-retired product-docs role, and
checks map<->tree consistency in both directions. `_inbox` age and declared legacy
debt are WARN-only. A pass is placement shape only — never validation,
readiness, or authority.

```
python .agents/hooks/check_placement.py --check      # advisory tree report (exit 0)
python .agents/hooks/check_placement.py --strict     # commit/CI gate (exit 1 on violation or stale map)
python .agents/hooks/check_placement.py --selftest   # decision-logic self-check
```

WIRED as a PostToolUse (`Write|Edit|MultiEdit`) entry in `.claude/settings.json`,
beside the other PostToolUse hooks. Reinstall (if settings were reset) = re-add
`{ "type": "command", "command": "python .agents/hooks/check_placement.py --hook", "timeout": 10 }`
to the PostToolUse array, then restart the session (hooks load at session start).

**Prompt-preflight reminder (advisory).** A PostToolUse hook (matcher
`Write|Edit|MultiEdit` in `.claude/settings.json`,
`python .agents/hooks/check_prompt_provenance.py --hook`): after a canonical
prompt write under `docs/prompts/**`, injects the **Forseti Prompt Preflight**
(output mode · template kind · edit-permission+targets+branch · reviews
findings-first + no runtime-model routing · doctrine-change -> propagation
receipt · destinations) so a routine prompt applies the contract inline with no
skill reload; fused / delegated-review-patch / novel prompts still author
through `workflow-prompt-orchestrator` (rule owned by
`.agents/workflow-overlay/prompt-orchestration.md`). Remind only, never blocks,
exit 0; it cannot verify the contract was applied. It does not fire for
lane-scoped prompts attached to a lane PR body/comment or kept in ignored
`docs/_inbox/` scratch; those are accepted only under prompt-orchestration.md
classification and must carry preflight manually.
`python .agents/hooks/check_prompt_provenance.py --selftest` checks the decision
logic.

**Google search-surface route guard (advisory + CI).**
`.agents/hooks/check_search_surface_google_route.py` checks the parameterized
Google route shell for changed durable docs: Google Search capture URLs use
`hl=en&gl=us&pws=0`, route-using artifacts carry the physical-locality
non-claim, and blocked Google pages with visible exit-IP content are not
preserved in durable docs. Wired in `.claude/settings.json`,
`.codex/hooks.json`, and `.github/workflows/ci.yml`. Authority:
`docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md` plus
the enforcement-placement principle in `.agents/workflow-overlay/validation-gates.md`.
Shape only; US-parameterized is not physically US-local. It is not
physical-locality proof, validation, readiness, demand proof, Judgment evidence, or Product Lead evidence.

**SCI reminder (advisory).** A PreToolUse hook (matcher `Bash|PowerShell`
in `.claude/settings.json`, gated to `git commit`) runs:

```
python .agents/hooks/remind_sci.py --hook
```

RIGHT BEFORE a `git commit` (run through the Bash/PowerShell tool) that has durable-artifact changes pending (the same durable-artifact
folder set the retrieval-header hook uses -- decisions, product, prompts,
workflows, migration, hygiene, review-inputs/outputs, the workflow overlay, and
the product corpus; scratch, inbox, skill copies, project config, and code are
excluded), it injects the Smallest Complete Intervention rule as non-blocking
`additionalContext`. The rule is OWNED by `AGENTS.md`; the hook carries that
section's text INLINE as a verbatim mirror (no fetch round-trip) and must be kept
in sync with it. Forward-only, advisory, fails open.
`python .agents/hooks/remind_sci.py --selftest` checks the scope logic. Reinstall
= re-add the PreToolUse entry (matcher `Bash|PowerShell`) in
`.claude/settings.json`, then restart the session.

**Permission floor (protected paths + git lifecycle).** A second
enforcement-placement substrate (EP-01 + EP-03 in
`docs/decisions/overlay_enforcement_placement_classification_v0.md`), built as
Claude Code `permissions` rules — no script:

- **`ask` — git lifecycle, shared/tracked in `.claude/settings.json`:**
  `git push`, `git remote`, `gh pr`, `git reset --hard`, `git clean`, for both
  the `Bash` and `PowerShell` tools (`git commit` is in `allow` — auto-approved,
  not prompted). Claude Code prompts for
  explicit approval; the approval is the authorization (`.agents/workflow-overlay/safety-rules.md`
  "...unless explicitly authorized"). Travels with the repo.
- **`deny` — protected paths, machine-local in `.claude/settings.local.json`:**
  writes/edits to external / installed-skill roots — `agent-workflow`, `jb*`,
  `~/.codex/{plugins,skills}`, `~/.claude/{plugins,skills}`, `~/.agents/skills`.
  Hard-blocked. Machine-specific absolute paths, so NOT tracked; a fresh clone
  re-adds its own external paths.
- Authority: `.agents/workflow-overlay/safety-rules.md` (the rules) + validation-gates "Enforcement
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
  "allow": [
    "Bash(git commit*)", "PowerShell(git commit*)"
  ],
  "ask": [
    "Bash(git push*)", "PowerShell(git push*)",
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
- references authority (`.agents/workflow-overlay/safety-rules.md`), fails OPEN on internal error, and has
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

**Repo-map commit interrupt + Stop-warn backstop.** Two complementary
substrates for the high-contention commit-once-whole shared files
(the repo map, `.claude/settings.json`, `.agents/workflow-overlay/source-of-truth.md`):

- **Per-edit (PostToolUse).** The repo-map-freshness hook
  (`.agents/hooks/check_repo_map_freshness.py`) exits 2 when the edited file IS
  the repo map and Git still shows it dirty after the edit. The interrupt tells
  the agent to commit it immediately, explicit-path
  (`git commit --only -- docs/workflows/forseti_repo_map_v0.md`), before other
  lanes' edits interleave. Distinct from its structural/freshness trigger
  (which fires on OTHER files adding navigation and remains advisory unless run
  in strict commit/CI mode).
- **Turn-end (Stop).** `.agents/hooks/check_shared_files_dirty.py` (a `Stop` hook, no matcher)
  warns when any of the three shared files is left dirty at end of turn, listing
  them plus the explicit-path commit. Exit 0, never blocks, never auto-commits
  (unsafe on a shared branch), guards `stop_hook_active`, fails open. CLI:
  `--check` (live tree), `--selftest` (logic). A second `Stop` hook,
  `.agents/hooks/check_token_burn.py`, warns (advisory, exit 0) when one turn's
  input context crosses a rung (200k warn / 500k alarm) — the quadratic-burn
  leading indicator. Reinstall = re-add both `Stop` hooks in
  `.claude/settings.json`, then restart the session.

These put the "edit the repo map -> commit it immediately, explicit-path" norm on
the substrate, not a heavy resident banner. The per-edit repo-map interrupt
blocks; the Stop backstop only warns. Neither auto-commits.

**Session-start lane capsule (SessionStart).** `.agents/hooks/session_context_capsule.py --hook`
(a `SessionStart` hook in `.claude/settings.json`; fires on startup/resume/clear/compact)
prints a compact, report-only lane-state capsule — repo root, branch, HEAD, last 3 commit
subjects, dirty/untracked counts, config-surface dirt, doctrine state vs last-fetched
`origin/main`, and pointers to the two source-loading entry artifacts (this map and the
overlay README) — so a new or re-oriented lane does not re-derive mechanical state turn by
turn. Observed git state only; loads no doctrine, asserts nothing beyond git output; exit 0,
fails open. Reinstall = re-add the `SessionStart` entry, then restart the session.

**Scan artifact checker (portable + CI diff-scoped).** `.agents/hooks/check_csb_scanning_artifact.py`
checks future CSB-first scanning artifacts for minimum reviewable receipt shape:
source context, caps, broad-scout accounting, CSB-row accountability, exact-query
accounting, venue/hidden-venue accounting, observations, negatives/access notes,
capture-request accounting including the Creator Registry preflight block,
candidate closeout, and obvious recency/Capture overclaim leakage. It also
verifies cited Creator Registry match-preflight receipt JSON content for detected
`docs/research/` scan artifacts carrying `creator_registry_match_preflight`
markers or for explicit checker paths. CI runs `--diff origin/main --strict`
forward-only over changed `docs/research/` artifacts that look like CSB-first or
Creator Registry preflight scan outputs; explicit paths remain available when
producing or reviewing scan artifacts. It is not wired as an automatic
PostToolUse hook. Fixtures live under
`forseti-harness/tests/fixtures/csb_scanning_artifacts/`; focused tests live at
`forseti-harness/tests/unit/test_csb_scanning_artifact_validator.py`. A pass is
receipt-shape/receipt-content consistency only, never scan-quality validation,
buyer proof, candidate approval, or Capture route authorization.

**Doctrine-change receipt-shape gate (EP-09) + retrieval-header forbidden-field
scan (EP-07).** Two further substrates built under owner authorization, following
this pattern:

- `.agents/hooks/check_dcp_receipt.py` — diff-scoped, forward-only CI gate
  (registered in `.github/workflows/ci.yml`, a sibling to the deletion-evidence
  gate): validates the SHAPE of any real `direction_change_propagation` receipt
  or `direction_change_propagation_blocker` in changed `.md` files — required
  keys, `trigger`/`related_triggers` drawn only from the seven controlled trigger
  values, `non_claims` non-empty — referencing `source-of-truth.md` (Doctrine
  Change Propagation Contract). It skips contract templates and non-receipt
  note-markers, never requires a receipt to be *present* (doctrine-ness is
  judgment), and never asserts a listed surface was truly updated/checked. The
  inline-cap / archive-pointer / no-standalone rules are intentionally not gated
  (not born-green). `--audit` = whole-repo advisory backlog; `--selftest` present.
- `.agents/hooks/check_retrieval_header.py` — its shared predicate
  (`header_problems_for_lines`) now also rejects status-leak header keys
  (approval / validation / readiness / lifecycle / deployment / install /
  resolver / publication / source-of-truth), flowing through both the write-time
  `--hook` and the `header_index.py --strict` CI gate. Born-green;
  `edit_permission` / `verdict` / `status` are intentionally allowed (review and
  prompt frontmatter use them). `--selftest` present.

Both enforce shape, never truth; a clean run is not validation, readiness, or
approval.

**Review-routing disposition gate (EP-35).** `.agents/hooks/check_review_routing.py`
— diff-scoped, forward-only CI gate (registered in `.github/workflows/ci.yml`)
plus a local `.githooks/commit-msg` advisory: a change touching code roots
(`forseti-harness/`, `.agents/hooks/`) must add a review artifact under
`docs/prompts/reviews/` / `docs/review-outputs/` in the same change, or carry a
shape-valid `review_routing_status:` commit-message line
(`routed <existing path>` / `blocked -- reason` / `not_needed -- reason`).
Rule owner: `.agents/workflow-overlay/validation-gates.md` (Review-routing
disposition gate). Disposition presence/shape only — never review quality,
reason truth, or whether review should have been recommended (resident
judgment). `--audit` = per-commit advisory history view; `--selftest` present.

**Local pre-push doc-gate mirror.** `.agents/hooks/pre_push_guard.py` (the
policy behind the tracked `.githooks/pre-push` adapter, installed via
`.github/scripts/install-local-hooks.ps1`) blocks pushes targeting `main`,
branch deletes, and non-fast-forward updates, and — for allowed lane pushes —
mirrors the strict CI doc gates (`check_map_links.py --strict`,
`header_index.py --strict`, `check_review_routing.py --strict`; diff-scoped
base `origin/main`, same as CI) so a durable-doc gate miss (e.g. a headerless
`docs/review-outputs/` report, PR #613) fails at the push boundary instead of
costing a red CI round. Blocks on any gate failure; the checkers' infra-gap
fail-opens are unchanged; bypassable with `--no-verify`; CI stays the
authoritative gate. `python .agents/hooks/pre_push_guard.py --selftest`
checks the decision logic. Rule owner:
`.agents/workflow-overlay/validation-gates.md` -> "Enforcement Placement"
(Local pre-push doc-gate mirror).

**Handoff-pointer resolution gate (EP-36).** `.agents/hooks/check_handoff_pointers.py`
— diff-scoped, forward-only CI gate (registered in `.github/workflows/ci.yml`):
handoff-packet paths (`docs/workflows/*handoff*.md`, `docs/prompts/handoffs/*.md`)
referenced in changed durable `.md` files must resolve in the same tree, or the
pointer line must carry an explicit pin (`branch` / `PR #N` / `origin/<ref>`)
or exemption marker (`does not exist yet`, `nonresolving:`, superseded/removed
wording). Practical consequence: a handoff packet merges no later than the
first main-bound artifact that points at it, or the pointer pins the authoring
branch — cold receiving lanes resolve required reads from `origin/main`. No
write-time hook by design (the defect is merge topology, invisible at the
write boundary). Rule owner: `.agents/workflow-overlay/validation-gates.md`
(Handoff-pointer resolution gate). Pointer shape only — never packet content
freshness, pin truth, or source-choice correctness. `--audit` = whole-corpus
backlog view (never gated); `--selftest` present.

**Full-GT claim tripwire.** `.agents/hooks/check_full_gt_claims.py` — diff-scoped,
forward-only CI gate (registered in `.github/workflows/ci.yml` as
`--changed --strict`): ADDED lines of changed `.md` files must not carry
unballasted "full God Tier" claim language outside the claim-owning/record
surfaces (the two Bronze declarations, data_lake README + spine workflows,
repo map, DCP archive, `docs/review-outputs/**`, `docs/prompts/**`,
`docs/hygiene/**`). A line passes with bounding ballast (negation / ceiling /
fixture / claim-tier wording) or the deliberate `full-gt-claim-ack` token.
Rule authority: the Bronze full-GT declaration's Erosion Guards (claim
inflation), referenced never restated. Shape only — never claim truth. `.py`
surfaces out of scope (tests + declaration govern). PostToolUse `--hook` mode
exists; registration in `.claude/settings.json` is owner-gated. `--selftest`
present. Companion tier-2 schema gate:
`forseti-harness/tests/contract/test_data_lake_core_field_gate.py` pins the
lake-core field/key sets per the write-boundary contract's No-New-Core-Field
Enforcement (any drift fails; update the pin only with the cited owner
decision).

**Review-output provenance gate.** `.agents/hooks/check_review_output_provenance.py`
— diff-scoped, forward-only CI gate (registered in `.github/workflows/ci.yml`
as `--diff origin/main --strict`): changed/added `docs/review-outputs/*.md`
must carry a valid retrieval header, non-blank `reviewed_by`/`authored_by`
(value `unrecorded` allowed, never blank/absent), and a review-use-boundary
statement (findings are decision input, not approval/validation/readiness).
Rule owners: `.agents/workflow-overlay/review-lanes.md` +
`.agents/workflow-overlay/retrieval-metadata.md` (referenced, never restated).
Shape only — never review quality, provenance truth, or de-correlation truth.
`--changed`/`--staged` are working-tree modes for local use; `--diff` is the
CI mode (a CI checkout's working tree is always clean). `--selftest` present
(fixtures under `forseti-harness/tests/fixtures/review_outputs/`).

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
| Is this Candidate URL Intake rather than Armory capture? | `forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md`, then `forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md` |
| Is bounded graph/frontier scouting accepted? | `forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` |
| How should old Reddit search/listing HTML be saved, parsed, and interpreted? | `docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md` |
| What are the proxy and anti-blocking hard stops? | `forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md` |
| What is implemented now? | `docs/workflows/screening_read_service_build_receipt_v0.md`, `docs/workflows/screening_read_reusable_findings_v0.md`, `forseti/product/spines/capture/core/source_capture_toolbox/README.md`, then `forseti-harness/README.md` and the named runner/adapter files |

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

For screening posture, the capture-harness service is now wired on the PR branch:
`source_capture.screening_read.screening_read(...)` covers bounded public
Reddit/direct/anti-block HTTP reads, while
`source_capture.screening_browser_read.screening_browser_read(...)` covers public
browser/interstitial reads and returns visible text only. These are
orchestrator-invoked, not walker-direct; no packet, manifest, ECR, Cleaning, or
Judgment output.
For same-shaped listing pages, reuse `StructuredListingExtractionSpec` and the
row-local locator/range-sanity pattern in
`docs/workflows/screening_read_reusable_findings_v0.md`.

Reddit Candidate URL Intake is also the bounded first-contact sourcing path for
declared Reddit source surfaces when a run envelope and live access
authorization are supplied. The implemented runner is
`forseti-harness/runners/run_reddit_candidate_intake_live.py`; it writes candidate
rows, provenance, and a live-run receipt only.

Reddit Graph Frontier is accepted only as a bounded planning lane with a Graph
Frontier Register. It may choose the next candidate seed and prepare a fresh
bounded run, but it does not authorize same-run traversal, Graph Frontier-owned
live Reddit fetch, automatic capture, broad crawling, Source Capture, Data
Capture, storage, scheduler, dashboard, or production runtime. Operator-facing
nickname: "crawling graph." The runner is
`forseti-harness/runners/run_reddit_graph_frontier_register.py`.

## Top-Level Structure

| Path | Role |
| --- | --- |
| `AGENTS.md` | Canonical root instructions, global behavior, and triggers to Forseti owner docs. |
| `docs/decisions/forseti_rename_migration_policy_v0.md` | Canonical rename policy: Forseti is the project/product name, Orca is the legacy alias, and lowercase compatibility paths remain until explicit migration. |
| `docs/decisions/forseti_compatibility_migration_boundary_v0.md` | Boundary decision for the remaining Forseti rename batches: narrow runtime/tooling label repairs and classified stale-reference audit now; root paths, package/import names, skill IDs, CI check IDs, and the repo-map path remain compatibility identifiers until a separately accepted migration plan exists. |
| `docs/decisions/forseti_harness_identity_migration_plan_v0.md` | Migration plan and execution record for retiring the `orca-harness/` runtime root, `orca-harness` distribution label, and `orca-harness-tests` CI check as compatibility identifiers without changing Python import namespaces or historical provenance. |
| `docs/migration/forseti_harness_runtime_migration_v0/moved_paths_index.md` | Retrieval-only moved-path index resolving historical `orca-harness/` path references to live `forseti-harness/` successors. |
| `docs/decisions/forseti_skill_preflight_identity_migration_plan_v0.md` | Skill/preflight identity migration plan and execution record: `forseti-product-lead` is now the primary accepted/deployed product-lead skill ID, `/orca-product-lead` remains a thin compatibility wrapper, `forseti_start_preflight` stays primary, and `orca_start_preflight` remains a deferred legacy alias. |
| `docs/decisions/forseti_external_identity_path_migration_decision_v0.md` | Post-audit migration decision and execution record for external repo identity: `eric-foo/Forseti` moved to `eric-foo/ForsetiWeb`, this repo moved from `eric-foo/orca` to `eric-foo/forseti`, and local/source slug cutover is tracked there. |
| `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md` | Repo-map successor migration decision: makes `docs/workflows/forseti_repo_map_v0.md` the live map, retains `docs/workflows/orca_repo_map_v0.md` as a compatibility pointer, and records the external repo slug collision discovered before Phase 1. |
| `docs/decisions/forseti_ontology_filename_migration_decision_v0.md` | Bounded ontology filename migration decision: live ontology GT ladder and ontology backbone filenames use Forseti names; historical old filenames resolve through the ontology filename moved-path index. |
| `docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md` | Retrieval-only moved-path index resolving old ontology GT ladder and ontology backbone filenames to their Forseti successors. |
| `docs/decisions/forseti_product_lead_authority_filename_migration_decision_v0.md` | Bounded product-lead authority filename migration decision: live product thesis, offer hypothesis, buyer-proof packet, product-proof charter, and claim-defense doctrine filenames use Forseti names; historical old filenames resolve through the product-lead authority filename moved-path index. |
| `docs/migration/forseti_product_lead_authority_filename_migration_v0/moved_paths_index.md` | Retrieval-only moved-path index resolving old product-lead authority filenames to their Forseti successors. |
| `docs/decisions/forseti_demand_read_taxonomy_filename_migration_decision_v0.md` | Bounded demand-read taxonomy filename migration decision: live proposed demand-read grammar and adjudication-prep companion filenames use Forseti names; historical old filenames resolve through the demand-read taxonomy filename moved-path index. |
| `docs/migration/forseti_demand_read_taxonomy_filename_migration_v0/moved_paths_index.md` | Retrieval-only moved-path index resolving old demand-read taxonomy filenames to their Forseti successors. |
| `docs/decisions/forseti_vertical_exploration_filename_migration_decision_v0.md` | Bounded vertical-exploration filename migration decision: live WHERE-side vertical-exploration procedure and memorization-resistant case-finder frame filenames use Forseti names; historical old filenames resolve through the vertical-exploration filename moved-path index. |
| `docs/migration/forseti_vertical_exploration_filename_migration_v0/moved_paths_index.md` | Retrieval-only moved-path index resolving old vertical-exploration filenames to their Forseti successors. |
| `docs/workflows/forseti_rename_residual_inventory_v0.md` | Current-main census and sampled classification of residual Orca/ORCA/orca_start_preflight hits after the authority rename; inventory only, not final validation. |
| `docs/workflows/forseti_rename_stale_reference_audit_v0.md` | Final Step 5 classified stale-reference audit for the Forseti rename continuation; records the bounded runtime/tooling label repair and remaining residual classes without claiming path/package migration. |
| `docs/workflows/forseti_post_harness_migration_status_v0.md` | Current Forseti migration status ledger: product root, repo-map path, harness root, package label, CI check, GitHub repo slug, product-lead skill ID, fresh local `projects/forseti` clone, PR #753/#755/#756/#758/#759/#760/#763 main convergence, the ontology, product-lead authority, and demand-read taxonomy filename families are landed, and the vertical-exploration filename family is covered by this migration lane; legacy active `projects/orca` workspace closeout, start-preflight alias, compatibility-wrapper retirement, and other lowercase filename families remain separate migration units. |
| `docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md` | Fused-ready handoff for Step 4 runtime/tooling bounded repair and Step 5 stale-reference audit under the compatibility boundary; explicitly forbids broad path/package migration and the prior stalled registration-integrity selftest retry. |
| `repo-structure.yaml` | Machine structure map (router only): homes + scratch/tolerance declarations consumed by `check_placement.py` and agents. Placement authority stays in `.agents/workflow-overlay/artifact-folders.md`; binding/parameters in `docs/decisions/orca_repo_structure_binding_v0.md`. |
| `.github/` | GitHub Actions workflows and local operational scripts for lane setup, merge-when-green, lane health, and local hook installation. Local automation only; not validation, readiness, or server-side branch protection. |
| `.githooks/` | Tracked local Git hook adapters installed via `.github/scripts/install-local-hooks.ps1`; catches local Git push/commit boundaries where enabled. Bypassable with `--no-verify`; not a server-side lock. |
| `.agents/workflow-overlay/` | Forseti overlay authority for project facts, folders, source rules, prompt rules, validation, safety, and review lanes. |
| `.agents/hooks/` | Portable enforcement/checker scripts for protected actions, retrieval headers, repo-map freshness, CSB-first scanning artifact receipt shape, and local Git pre-push policy. Harness adapters invoke some scripts; passing checks are not validation or readiness. |
| `forseti-harness/` | Bounded authorized implementation backing Data Capture source acquisition and the v0.14 Judgment Harness (capture adapters, source-observability, schemas, scoring, runners, fixtures, tests). Navigation context only; not runtime, acceptance, or readiness. See the Forseti Harness section. |
| `forseti/` | Declared top-level product-tree root. Product substance lives under `forseti/product/`; runtime remains under `forseti-harness/`. Historical `orca/product/` paths resolve through `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`. |
| `forseti/product/` | Spine-first product tree: product contracts, Core Spine artifacts, proof plans, source/evidence standards, offer, buyer-proof, demand-signal method/surface docs, satellites, case families, and shared product registries. Historical `docs/product/` references resolve through `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md`; historical `orca/product/` references resolve through `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md`. |
| `forseti/product/spines/data_lake/` | Data Lake shared-foundation spine (promotion-bound 2026-06-18; contracts + mechanics landed by R2). Owns cross-layer storage contracts (raw-packet preservation, keyed retrievability, Attachment Record, passive Availability Index), the engine/backend selection boundary, the medallion/gold-readiness contract consumed by projection/ECR/cleaning/judgment, and the post-PR-525 Bronze MGT baseline declaration that lets Silver consume public Bronze catalog/AR surfaces without declaring Bronze full GT. Binding: `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`. |
| `forseti/product/spines/data_lake/authority/` | Data Lake contracts/invariants: core, storage and engine-selection boundary, Attachment-Record implementation, Bronze MGT baseline declaration, medallion/gold-readiness, and capture-propagation classification contracts. |
| `forseti/product/spines/data_lake/workflows/` | Data Lake operational/read-flow docs: the canonical mechanics map (supersedes the retired `shared/data_lake_mechanics/`) plus Bronze full-GT upgrade scoping and physicalization decision records. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md` | Signal-first Bronze MGT to full-GT upgrade scoping record for batches A-D: discovery/Manifest fork, AR physicalization fork, retention/lawful-erasure/backend lock-in posture, and lake-doctor/CI plus representative proof threshold. Non-runtime; does not declare full GT. |
| `forseti/product/spines/foundation/` | Foundation spine: product contract, IPF/evidence standard, ontology (backbone + SSOT + cards + fragrance reference data), demand-read taxonomy, vertical-exploration. For fragrance FACT lookup go straight to `ontology/fragrance_reference_v0.yaml` (self-describing: facts + per-fact provenance + extension pattern in-file; see the Decisive-File Quick Index). |
| `forseti/product/spines/foundation/ontology/forseti_ontology_backbone_architecture_v0.md` | Adopted ontology backbone prose/rationale authority: type roster rationale, ID grammar, links, dimensions, action gates, and dated amendments. For machine-readable SSOT open `ontology.yaml`; for old filename resolution use `docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md`. |
| `docs/decisions/forseti_ontology_gt_foundation_ladder_v0.md` | Ontology foundation GT ladder and trigger-gated infrastructure roadmap; records R0 done and R1-R7 triggers/non-claims. Old filename resolves through `docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md`. |
| `forseti/product/spines/scanning/` | Scanning (discovery-side) spine: open `forseti/product/spines/scanning/README.md` first. It routes to the MGT intelligent-walk model, default CSB broad-scout phase, recency/current-state frontier priority, proposed scan-core schema, admissibility/checkability surfaces, and source-family adapters. |
| `forseti/product/spines/capture/` | Capture (acquisition-side) spine: `core/` reusable acquisition layer containing source-access/candidate/corpus/obligation contracts, operating_model, packet_schema, Source Capture Toolbox, demand_durability_indicators, and source_families. Open `forseti/product/spines/capture/core/source_families/README.md` for known source-family capture-to-lake route homes (`fragrance_native_database`, `retail_pdp`, `social_media/{instagram,tiktok,youtube,reddit}`, creator_registry, and cross-archive pointers). Dense - open the Data Capture submap. |
| `forseti/product/spines/creator_signal/` | Creator Signal product/signal spine (promotion-bound 2026-06-28). Owns product-facing creator intelligence surfaces: profile IA, aggregate influence display, ideal/content-fit audience display, freshness, limitations, and source drill-back over Capture-owned creator records. Binding: `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md`. |
| `forseti/product/spines/ecr/` | Evidence Candidate Record spine: evidence_candidate_record (SP-1/2/3/6 slices), signal_content (SCR direction + deriver, now deprecated/dormant as default pre-Judgment layer). |
| `forseti/product/spines/cleaning/` | Cleaning spine: cleaning-layer contracts. |
| `forseti/product/spines/judgment/` | Judgment spine: conductor, claim_ladder, demand_read (core/c2_weighting/c3_verdict_action/grading), learning_loops (near_half/far_half), source_side_receipts, toolkit_gaps. Demand-read C2 treats recency/currentness as qualitative attention/relevance, not proof or scoring. Dense — submap candidate. |
| `forseti/product/spines/product_lead/` | Product-Lead spine: offer, buyer_proof, proof_charter, icp_wedge. |
| `forseti/product/spines/commission_signal_board/` | Commission Signal Board pilot spine: authority, dispatch_rules, harness + tests + migrations + prompts + workflows (#261); prompt rows carry recency/currentness as attention metadata, not proof. |
| `forseti/product/satellites/beauty/` | Beauty satellite: domain venue/card assets. |
| `forseti/product/satellites/fragrance/` | Fragrance satellite: Level-1 judgment organizers (casebook_admission, named_case_screens, reconciliation, satellite_skeleton). |
| `forseti/product/case_families/product_learning/` | Product-learning case corpora: fragrance + other_verticals (SaaS/tech method-validation + first-proof-run families). |
| `forseti/product/shared/engagement_registry/` | Shared engagement-logic registry. |
| `forseti/product/shared/projection_doctrine/` | Shared projection doctrine (raw->view constraint, not Cleaning/Judgment). |
| `docs/decisions/` | Decision records. |
| `docs/decisions/consultant_loop/` | Consultant-loop judgment records. |
| `docs/prompts/` | Prompt artifacts, wrappers, reruns, reviews, and local templates. |
| `docs/research/` | Research artifacts and consulting-judgment corpus material, including answer-engine probe evidence under `docs/research/answer_engine/`. |
| `docs/review-inputs/` | Prepared review inputs. |
| `docs/review-outputs/` | Review reports and adversarial artifact reviews. |
| `docs/workflows/` | Workflow records, operational notes, and repo maps. |
| `docs/migration/` | Import and migration records. |
| `docs/hygiene/` | Triage and cleanup queues. Hygiene packets are operational/burn-after-read artifacts, not retrieval-indexed by design (owner-ratified default 2026-06-13). |
| `docs/_inbox/` | Non-authoritative scratch and parked material. |
| (root strays) | Quarantined 2026-06-11: `slot1_mi`/`slot2_teal` operator workfiles and `di_dd.html` moved from the repo root to `docs/_inbox/`; see `docs/hygiene/queue.md` ORCA-HYGIENE-010. The root is now fully enumerated by `repo-structure.yaml` `known_top_level`. |

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
| `.agents/workflow-overlay/template-registry.md` | Forseti-local prompt template registry. |
| `.agents/workflow-overlay/product-proof.md` | Buyer-proof semantics and non-claims. |
| `.agents/workflow-overlay/communication-style.md` | Forseti response style. |
| `.agents/workflow-overlay/validation-gates.md` | Validation gate expectations. |
| `.agents/workflow-overlay/review-lanes.md` | Review lane rules. |
| `.agents/workflow-overlay/delegated-review-patch.md` | Provisional, opt-in Delegated Review-and-Patch convention for high-stakes authored artifacts (and bounded multi-file code diffs via the `delegated_code_review_and_patch` sibling mode); not a bound review lane. |
| `.agents/workflow-overlay/safety-rules.md` | Safety and forbidden drift. |
| `.agents/workflow-overlay/skill-adoption.md` | Skill source and adoption status. |

## Workflow Navigation Files

| Path | Use for |
| --- | --- |
| `docs/workflows/artifact_retrievability_guide.md` | Operational guidance for durable artifact headers, body-opening source surfaces, stale/recheck patterns, repo-map/index treatment, report-only retrieval checks, and hygiene anti-rot. |
| `docs/decisions/orca_doctrine_index_v0.md` | **Doctrine index (router, not authority)** — one place to find every binding doctrine across the kernel, overlay, decision records, and product lanes, with explicit doctrine naming and subset grouping. On conflict the doctrine's own record wins. |
| `docs/workflows/forseti_repo_map_v0.md` | Compact navigation map for bounded source-pack selection and prompt setup. |
| `docs/workflows/orca_repo_map_v0.md` | Legacy compatibility pointer to the live Forseti repo map; kept so older links resolve. |
| `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md` | Cold-agent rehearsal of Creator Registry match preflight behavior: known account blocks duplicate `new_capture`, exact-unmatched row clears via `can_start_new_capture`, mixed batches exit nonzero when any requested action is blocked. |
| `docs/workflows/creator_registry_operational_next_steps_handoff_v0.md` | Cold-reader handoff for continuing the Creator Registry operational lane after PR #669 merged: use the cold creator discovery scan handoff prompt on a real target, keep scan/capture/registry boundaries intact, and route the receipt-provenance checker gap to an explicit decision. |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_ledger_operational_evolution_contract_v0.md` | Creator Ledger operational evolution contract: migration-stable additive upgrade rule, capability routing matrix, and upgrade-intake shape for registry/linkage/observation/metric/profile-current layers, with efficacy-first God Tier criteria and Mini God Tier accepted residuals. |
| `docs/workflows/creator_ledger_first_operational_proof_checkpoint_v0.md` | First operational proof-loop checkpoint for the Creator Ledger: applies the efficacy-first, migration-stable proof loop to the first public YouTube fragrance creator scan, preserved preflight receipt, and current receipt-content checker state. |
| `docs/workflows/creator_ledger_known_account_preflight_checkpoint_v0.md` | Second operational proof-loop checkpoint for the Creator Ledger: known-account preflight proof that allows update-existing routing, blocks duplicate new capture, preserves a receipt, and avoids registry/capture/Silver mutation. |
| `docs/workflows/creator_ledger_observation_sibling_checkpoint_v0.md` | Third operational proof-loop checkpoint for the Creator Ledger: binds the YouTube creator-observation ledger as a source-backed sibling evidence layer for repeat-observation and metric-upgrade work without remigrating registry/profile data. |
| `docs/workflows/creator_ledger_additive_upgrade_intake_rehearsal_v0.md` | Additive-upgrade-intake rehearsal for a Creator Ledger capability that does not fit the initial routing matrix cleanly: routes ideal/content-fit audience profile snapshots as sibling evidence joined into profile-current without registry/profile data remigration. |
| `docs/workflows/repo_map_recent_changes/` | Low-conflict, one-file-per-change notes for repo-map-affecting additions; retrieval-only context, not a substitute for updating actual map routes when navigation changes. |
| `docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md` | Post-PR #537/#540 Bronze/Silver consumer-proof closeout: two source-family Silver producers consume public Bronze source-surface catalog / Attachment Record rows for source-backed `raw_refs`; routes the lane away from default third-family proof expansion and toward full-GT residual scoping. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md` | Data Lake spine scoping record that turns the PR #542 consumer-proof boundary into A-D full-GT success signals and review timing without selecting runtime physicalization choices or claiming Bronze full GT. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md` | Superseded as the active continuation anchor by the physicalization decision brief; remains the historical planning-only next material decision packet after the Bronze full-GT A-D scoping record: Batch A raw-writer/non-raw-touchpoint source inventory plus Manifest/equivalent decision request, Batch B/C physicalization gates, and Batch D proof/CI threshold hardening before any third-proof work. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md` | Historical Bronze full-GT physicalization gate framing (its stale_if self-fired when both gates were owner-ratified 2026-07-02): framed Gate 1 (AR body layout) and Gate 2 (retention/lawful-erasure/backend lock-in); its decision-request and option ledgers are superseded by the ratified gate ADRs; no runtime implementation, backend selection, third proof, or Bronze full-GT claim. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_plan_v0.md` | Batch plan for the Gate ADR work unit, BATCH_COMPLETE: brief reviewed, both gate ADRs authored, B5 delegated review-patch executed and adjudicated, both gates owner-ratified 2026-07-02; contract fold-in and implementation scoping continue in the post-ratification lane; do not re-run the batch. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md` | Gate 1 ADR owner-ratified 2026-07-02: packet-member ratified as the default Attachment Record body home with the eight required outputs; attachments/ sidecar reserved behind a reopen trigger; external bodies locked behind Gate 2 plus a backend/physicalization ADR; entry serialization stays deferred to A2 behind A1. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md` | Gate 2 ADR owner-ratified 2026-07-02: lawful erasure explicitly deferred with the full accepted-residual record - residual scope, claim ceiling, tombstone/supersession unavailability posture, forbidden backend classes/operations while deferred, and four revisit triggers (T1-T4); standing doctrine for every backend-adjacent step. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_scoping_route_v0.md` | Historical implementation-scoping route for the physicalization proof scope (its single owner yes/no was granted 2026-07-02 under /fused, firing its stale_if): STEP-01..06 for the A1 inventory gate plus six-invariant proof gate; the physicalization proof closeout record is the continuation anchor. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_closeout_v0.md` | Physicalization proof-scope closeout (2026-07-02): A1 deterministic touchpoint inventory gate (`data_lake/inventory.py` + checked-in `lake_touchpoint_inventory_v0.json` + contract gate test) and CI-owned PROOF-01..06 fixture-lake proofs of write-once, append-only, read-by-key, hash verification, public AR resolution, and byte-identical index rebuild under the ratified packet-member relationship, each fail-capable via seeded violations; MGT items 1 closed / 4 partially closed; residuals: A2 owner decision, third-proof threshold, final de-correlated review, backend locked behind Gate 2 T3; not production validation or a Bronze full-GT claim. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md` | A2 ADR owner-ratified 2026-07-03: A2-F2 packet index — the durable canonical object is the versioned entry schema plus deterministic derivation rule, never a materialized row; Manifest v2 reserved behind revisit triggers T-A2-1..3; hybrid-forever and packet-member AR file rejected; attachment_record_id locked to query-locator; fold-in and implementation landed via the A2 implementation closeout; not backend (Gate 2 T3), retention, or full-GT. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_implementation_closeout_v0.md` | A2 implementation closeout (2026-07-03, fused Lane A): pinned serializer `data_lake/attachment_record_entry.py` (versioned entry schema + deterministic derivation rule, entry_serialization_v1 / derivation_rule_v1 pins, canonical bytes, centralized manifest-version dispatch failing closed on unknown formats), catalog rows delegated onto it (AR schema _3, catalog schema _3), zero-index by-key derivation, CI-owned PROOF-07 + fail-capable serializer tests; residuals: engine/incremental rebuild behind T-A2-1, replay tooling owner-gated, third-proof threshold and final de-correlated review still open; not production validation or a Bronze full-GT claim. |
| `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md` | Bronze full-GT declaration owner-ratified 2026-07-03, successor-for-claim-tier to the MGT baseline: full God Tier for typed raw-truth retrievability/physicalization at fixture-proof tier under the Gate 2 claim ceiling; evidence = three ratified ADRs, A1 inventory gate + CI-owned PROOF-01..07, three adjudicated cross-vendor reviews; named exclusions: production-lake validation, real-lane fixture breadth, backend/engine (Gate 2 T3), migration/replay tooling, erasure capability, Silver breadth beyond two proven families, Silver-side review. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_lake_owner_explainer_v0.md` | Owner-facing plain-language Bronze lake explainer: what the lake is, its invariants, Attachment Records, Silver relation, MGT versus full GT (status note: full GT ratified 2026-07-03), and the two physicalization gates; orientation only, contracts win, live state via the active continuation anchor. |
| `forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_consumption_seam_scoping_route_v0.md` | Consumption seam v0 scoping route (executed 2026-07-02 under owner-granted bounded authorization): STEP-01..06 route record behind the landed seam contract `authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`, shared pickup/ack helper, derived_retrieval rebuild runner (undone/by_mention), and transcript-lane proving migration; contract subsequently hardened by cross-vendor delegated review adjudication, with first metric families owner-named (share-of-voice, movement-threshold) behind a field-level gate. |
| `docs/workflows/youtube_shorts_creator_index_decision_path_v0.md` | Source-backed workflow decision path for planned creator-ledger infrastructure: keeps the 200-row fragrance ledger as evidence, assigns recurring creator-observation contract ownership to Capture source-family architecture, limits Data Lake to keyed storage/attachment, and defers queryable niche/sub-niche creator views to projection. |
| `docs/workflows/ig_behavioral_live_validation_receipt_v0.md` | Bounded live IG validation receipt after PR #441/#447: public logged-out grid packet projected through the IG behavioral lake adapter, with standalone-audio residuals and a follow-on no-write deep-capture route diagnostic. Not shared-core, production readiness, canonical F-lake validation, or full durable media validation. |
| `docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md` | Bounded canonical F-lake IG receipt: public deep-capture writes, no-network product extraction writes, exact Silver lineage verification, and behavioral-completeness residual downgrade observed after PR #460 follow-up patches. Not shared-core, production readiness, logged-in/proxy access, durable media/video preservation, or Judgment/gold verdict. |
| `docs/workflows/ig_youtube_behavioral_e2e_closeout_receipt_v0.md` | Evidence-first IG/YT behavioral closeout receipt: canonical F-lake IG projection matrix, expanded 31-video YouTube caption-route F-lake e2e evidence, remaining ASR/no-caption residual, and non-claims. For detailed YouTube corpus measurement, open `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`. |
| `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md` | Expanded canonical YouTube F-lake measurement corpus: 31 caption-route watch+caption videos, projection status counts, product-extraction boundary, ASR/no-caption gap, and next non-admin steps before statistical full-path completeness claims. |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Data Capture Spine repo submap. Open before enumerating capture owner docs. |
| `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md` | Current cold-agent entry contract for TikTok capture: sanctioned CloakBrowser live-runner path, source-access provenance gate, blocker/action taxonomy, local-admission preference, owner handoff boundary, batch implementation status, and non-claims. Start here before using older TikTok handoffs. |
| `docs/workflows/tiktok_ui_movement_blocker_substrate_playbook_v0.md` | Cold-agent playbook mapping TikTok live UI blocker classes to the bounded `BrowserPagePointerAction` substrate: benign overlay dismissal, visible retry, comments -> You may like / More like this -> comments routing, X-able slider/captcha close follow-through, owner handoff, and no-solve/no-clean-capture semantics. |
| `docs/review-outputs/tiktok_capture_enforcement_batches_1_4_post_adjudication_delegated_adversarial_code_review_v0.md` | Completed cross-vendor delegated adversarial code review for TikTok capture enforcement BATCH-01..04 and post-adjudication hardening: recommendation `keep`, patches_applied `0`, with minor non-blocking notes only. Decision input, not validation/readiness/merge authority. |
| `docs/workflows/tiktok_session_provenance_pr709_handoff_v0.md` | Current cold-reader handoff for PR #709 after main-merge conflict resolution: expected branch/head, conflict-resolution decisions, validation evidence, PR verification next step, stale PR689 handoff warning, and TikTok no-solve/no-secret drift guard. |
| `docs/workflows/tiktok_live_microbatch_owner_gated_handoff_v0.md` | Historical cold-lane handoff for the owner-gated TikTok live micro-batch after bounded pointer-action and blocker-triage patches: use for its specific microbatch context only; current cold-agent route starts at `docs/workflows/tiktok_cold_agent_capture_enforcement_goal_v0.md`. |
| `docs/decisions/tiktok_auth_state_provenance_sidecar_architecture_v0.md` | Architecture decision for TikTok sessioned auth-state provenance: extend the ignored auth-state sidecar with typed category-only provenance, merge warmup/export evidence forward, enforce requested claims in the live runner, and distinguish `no_proxy_profile_loaded` from unproven full-network no-proxy egress. |
| `forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_capture_propagation_classification_contract_v0.md` | Accepted Data Lake / Capture propagation classification contract: classifies lake semantics, raw packet-runner seams, behavioral projection shape, source-family-local acquisition routes, and downstream residual/completeness semantics into same-class checks. |
| `docs/decisions/data_lake_capture_propagation_classification_contract_proposal_v0.md` | Prepare-only proposal for narrow Data Lake / Capture propagation classification: generic lake/storage and packet-runner checks, platform behavioral parity checks, source-family-local acquisition routes, and downstream residual/Gold-boundary propagation. Proposal only; not accepted doctrine. |
| `docs/workflows/ecr_spine_submap_v0.md` | ECR source-side spine repo submap (integrity postures SP-1/2/3/6 + deprecated/dormant Signal Content Record contract). Open before enumerating ECR/SCR owner docs. |
| `docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md` | Contract-to-code checklist for the bounded Cleaning substrate in `forseti-harness/cleaning/` against the Cleaning README/foundation/boundary/projection sources. Retrieval-only; not validation, readiness, or production Cleaning authorization. |
| `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | Judgment Spine submap. Open before enumerating Judgment owners across `docs/research/judgment-spine/` and `forseti/product/spines/judgment/`. |
| `forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md` | Operator playbook for the bounded Amazon/Sephora/Ulta Retail/PDP CloakBrowser sidecar smoke: canonical URLs, flags, scratch outputs, expected residuals, failure taxonomy, and code-enforceable follow-up flags. |

## Forseti Harness

`forseti-harness/` is bounded, authorized implementation backing Data Capture
source acquisition and the v0.14 Judgment Harness. It is navigation context
here, not a runtime, acceptance, or readiness claim. Build scope is controlled
by the authorization decisions named below; surfaces outside them (production
runtime, commercial fetch, broad crawling, ECR, Cleaning, Judgment
design) remain gated.

Current Parfumo native fragrance route (2026-06-30): direct-HTTP capture
wrapper `forseti-harness/runners/run_parfumo_mgt_capture.py` (preflightable;
live network capture still requires owner authorization), mechanical projection
`forseti-harness/source_capture/parfumo_projection.py` plus
`forseti-harness/runners/run_parfumo_projection.py`, and Cleaning audit/Silver
adapters `forseti-harness/cleaning/parfumo.py` and `forseti-harness/cleaning/parfumo_lake.py`; tests live in `forseti-harness/tests/test_parfumo_native_pipeline_lake.py` and `forseti-harness/tests/unit/test_parfumo_*`.

Current Basenotes native fragrance route (2026-06-30): rendered CloakBrowser capture through the residential proxy profile `reddit-res-01` (anonymous egress is Cloudflare-challenged at the headless-automation / TLS-fingerprint layer, NOT by IP; route pinned in `docs/research/orca_fragrance_native_database_live_probe_v0.md` PIN-003 + the Proxy Route Verification Addendum; live network capture still requires owner authorization), wrapper `forseti-harness/runners/run_basenotes_mgt_capture.py`, mechanical projection `forseti-harness/source_capture/basenotes_projection.py` (reviews parsed from schema.org JSON-LD) plus `forseti-harness/runners/run_basenotes_projection.py`, and Cleaning audit/Silver adapters `forseti-harness/cleaning/basenotes.py` and `forseti-harness/cleaning/basenotes_lake.py`; tests live in `forseti-harness/tests/test_basenotes_native_pipeline_lake.py` and `forseti-harness/tests/unit/test_basenotes_*`. Silver routes through the `append_silver_record` front-door (no Silver-via-raw exception); no anti-bot evasion is used or authorized (the residential proxy is an existing owner-authorized capture route, not evasion). Full review corpus is a named residual: in-page JSON-LD carries a subset (about 6 of 18), with `/reviews/` plus sentiment sub-URLs as the archive gate.

| Path | Use for |
| --- | --- |
| `forseti-harness/capture_spine/` | Capture-spine planning/validation/materialization helpers: Reddit Graph Frontier, LinkedIn lane/frontier validators, `creator_public_handle_linkage/` for the static public-handle linkage ledger validator, `youtube_creator_observation/` for the YouTube creator observation ledger rebuild verifier and its archived-lake evidence check (the seed ledger is bound to the retired `orca-canonical` v0 root per the lake-identity-drift decision packet), and `creator_profile_current/` for deriving the checked-in creator-profile-current view from sibling account-linkage and metric-seed/snapshot ledgers plus exact-match Creator Registry preflight receipts, including `youtube_metric_seed.py` for rebuilding the committed YouTube metric seed from checked-in review inputs plus ledgers, `registry_match_preflight.py` for fail-closed candidate account matching, and `live_lake_freshness_gate.py` — the AR-02 check that the committed IG rollup snapshot still matches the live external lake. Navigation context only; not live capture, runtime readiness, SQLite adoption, person identity proof, fuzzy duplicate detection, cross-platform identity proof, or a claim that all future metric rollups are source-backed. |
| `forseti-harness/source_capture/` | Source-capture packet core: models, writer, CLI support, plaintext receipts, bounded mechanical projection helpers including Fragrantica current-window projection (`fragrantica_projection.py`), the no-network fragrance purchase-review focused coverage helper (`fragrance_review_coverage.py`; saved widget/PDP files only, selected reader bodies plus skipped metadata/hashes), the rendered+widget fragrance purchase-review capture helper (`fragrance_rendered_widget_companion.py`; PDP above-fold render plus passive widget response preservation, optional bounded widget fallback URL completion, emits the focused coverage subreceipt; not ECR, Cleaning, or Judgment), the network-free fragrance purchase-review discovery core (`fragrance_review_discovery.py`; enumerates products via Shopify products.json or storefront sitemap and finds review-positive PDPs via a cadence-limited Judge.me per-product probe or the Yotpo store-level reviews feed; injected transport, emits candidate PDP URLs only — not capture, rows, registry promotion, or scoring), the fragrance purchase-review preserved-body lake tee + projection (`fragrance_review_lake.py`; tees EXACT raw review widget-response bytes into write-once `PreservedFile` lake bodies — one preserved file per review widget response, capture metadata in the manifest only — and re-derives the focused review coverage view into an append-only `derived/<packet_id>/projection_fragrance_review/` record; mirrors the Retail/PDP lake pilot; preserves raw bytes only, NOT a durable typed Attachment Record, which stays data-lake-lane-owned), the `block_shell` honest-success classifier (block-shell / empty / content-unverified; no positive content class), the bounded Reddit screening-read entry `screening_reddit_read.py` (entitlement-gated, screen-light, adapter-not-runner: wires `fetch_direct_http_capture` only, never the packet/ECR runner; returns a screen-light record, no disk artifact / no ECR), the cross-archive historical-capture LOCATE orchestrator `historical_capture.py` (slice E: ordered Wayback -> archive.today -> publisher-history ladder above the adapters; stops at the first verified pre-cutoff body; neutral `archives_tried`/`archive_selected` facts, INV-1), `source_capture/tiktok/` for TikTok SCI single-video admission, parsed-batch admission, admitted-batch coverage/projection, blocker triage, and the one-creator live staging probe (`admission.py`, `video_packet.py`, `batch_packet.py`, `batch_coverage.py`, `batch_projection.py`, `blocker_triage.py`, `live_batch_probe.py`; packetization/projection stay network-free; live probe is headed/sessioned staging only with fake-engine tests, stops on missing hydration as a possible empty/stripped-shell block signal, emits classification-only blocker-triage receipts, and preserves sanitized subtitle URL-present receipts through batch admission; no raw signed URL/session/body persistence, no blocker action execution, no live-run or cross-creator-ceiling claim, no product extraction/persisted derived lane), and `lane_orchestration.py` for shared vertical lane receipts (status/message/outputs/residuals only; no acquisition-method standardization). |
| `forseti-harness/data_lake/` | Data Lake filesystem root and generated-index helpers: v4.1 sharded raw/derived/ack layout, availability index rebuilds, verified raw-packet reads, and Bronze Catalog v0 (`catalog.py`), which rebuilds non-authoritative retrieval indexes from committed raw packet manifests under `indexes/derived_retrieval/bronze_catalog/v0` with universal packet facets, source-family extractors such as IG reels-grid creator/shortcode facets, self-describing `source_surfaces.json` coverage that marks observed lanes as `registered` or `universal_only` without implying completeness/readiness, generated `attachment_records/` entries over preserved raw body files with stable record IDs, body-sha/path references, source-surface/payload/body-sha buckets, resolver-verified byte reads, an inspect-only Bronze coverage census over observed source-family/source-surface + Attachment Record counts, and additive `bronze_baseline_status` markers that expose the post-PR-525 MGT baseline without claiming full GT. Also the A1 lake touchpoint inventory (`inventory.py` single-sourcing the seam-test AST discovery plus the checked-in `lake_touchpoint_inventory_v0.json`, diffed fail-capably by `tests/contract/test_data_lake_inventory_gate.py`) and the pinned A2 entry serializer (`attachment_record_entry.py`: canonical versioned AttachmentRecordEntry schema + deterministic derivation rule, centralized manifest-version dispatch, zero-index by-key derivation; catalog rows are this plus catalog-only decorations). Retrieval coverage only; not Manifest v2, a body-copy store, a capture-lane registry, Silver readiness, or final Attachment Record physicalization. |
| `forseti-harness/source_capture/youtube_watch_packet.py` | Network-free SourceCapturePacket writer for YouTube watch-page metadata/comments capture; stores raw watch HTML, youtubei next page JSON, explicit availability/comment states, metric observations, and preserved route receipts. |
| `forseti-harness/youtube_capture/` | Incumbent bounded YouTube public-metadata fetchers reused by the packet writers and runners: `capture_youtube_v0.py` (watch-page metadata + bounded youtubei comment sampling; posture-backed view/like/total-comment metric receipts — total comment count reads the exact-integer Comments engagement-panel badge in served HTML and fails closed on rounded K/M text — plus fail-closed video/comments availability states), `shorts_scroll_capture_v0.py` (Shorts shelf scroll capture), and the Chrome-impersonating `stealth_client.py` transport. Captured `packets/` output is gitignored; navigation context only, not live-capture authorization. |
| `forseti-harness/source_capture/adapters/` | Bounded capture adapters (direct HTTP, media/asset, Archive.org, archive.today (`archive_today`: Memento TimeMap locate+body rung, served-time verification, no-gate-defeat STOP on a challenge), browser snapshot, authenticated browser, Reddit API where present, fragrance widget fallback transport (`fragrance_widget_fallback.py`; bounded widget URL fetches for the rendered companion only), fragrance discovery fetch transport (`fragrance_discovery_fetch.py`; verified-TLS stdlib `urllib` reads for products.json/sitemap/widget-count/Yotpo-feed discovery), and a header-complete anti-blocking HTTP rung-1 adapter `anti_blocking_http`). CloakBrowser Snapshot anonymous non-persistent v0 now has a live engine and packet runner for one explicitly supplied URL; verify any adapter's presence in code before use. Reddit discovery/consolidation, proxy/session behavior, commercial fetch, broad crawling, storage, dashboards, deployment, and production runtime remain separately gated. |
| `forseti-harness/source_capture/transcript/` | Cross-source transcript ACQUISITION (Capture layer): per-platform fetchers returning RAW artifacts + capture metadata for SourceCapturePacket staging (`youtube_captions.py`: YouTube captions via yt-dlp default token-free client; `caption_packet.py`: network-free packet builder; `audio_asr.py` + `asr_packet.py`: VAD-gated faster-whisper ASR fallback when captions are absent, writing the transcript as a `transcript_asr` derived record keyed to the audio packet; `ig_reels_audio_packet.py`: the Instagram-Reels analogue — anonymous yt-dlp bestaudio fetch + IG audio/`transcript_asr` writer (`source_family=instagram_creator`, `source_surface=ig_reels_audio`; Reels have no caption API so ASR is the only route; audience-restricted = typed skip; spec under `…/source_families/social_media/instagram/`)). The readable/clean transcript is a downstream Cleaning transform. Navigation context only; not Cleaning, Judgment, or readiness. |
| `forseti-harness/source_observability/` | Local operator-record posture checker and limitation reporter. |
| `forseti-harness/ecr/` | Evidence Candidate Record source-side integrity postures (SP-1/2/3/6): per-packet/slice derived records keyed to the `SourceCapturePacket`; bind no `EvidenceUnit`; JSG-01 frozen. Boundary context: `forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`. |
| `forseti-harness/signal_content/` | Signal Content Record (v0): retained compatibility/history code for the deprecated/dormant content contract; not default pre-Judgment generation. Direction + deprecation posture: `forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md`. |
| `forseti-harness/evidence_binding/` | JSG-01-scoped EvidenceUnit binding (owner-ratified 2026-06-12): the three-key `Jsg01EvidenceBinding` + the pure `compose_jsg01_evidence_record` composer + verifier; references packet/ECR/receipt by key, binds no posture/value, computes no aggregate verdict. Design basis: `forseti/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md`. Navigation context only; not a JSG-01 unfreeze, validation, or readiness. |
| `forseti-harness/cleaning/` | Bounded local Cleaning-layer code (models, core, projection, source-family adapters/lake writers including Fragrantica projection→Cleaning and append-only Cleaning derived records) and the YouTube transcript→product Pass-1 LLM lane (`transcript_product_extractor.py`: mention extraction with the CE5/CE9 quote-locator — the model gives a quote, code locates it in the cues to both verify it and assign the timestamp; `transcript_product_lake.py`: silver mentions persist + timing-preserving json3→cues). Navigation context only — not the gated production Cleaning lane, acceptance, or readiness. |
| `forseti-harness/schemas/` | Pydantic v2 models for cases, judgments, scoring, and probes (v0.14), plus the YouTube transcript→product extraction models (`product_mention_models.py`: `ProductMention` / `StatedRating`, finite-guarded floats, verdict-free by construction). |
| `forseti-harness/scoring/` | Deterministic, LLM-free scoring: the v0.14 band scorer + mapping table, the Pass-2 product-verdict fusion `product_fusion.py` — per-product creator verdict via a tunable, documented `FusionConfig` knob set — its calibration sensitivity harness `product_fusion_sensitivity.py`, and the sibling `audience_fusion.py`. The fusion's UNCALIBRATED v0 calibration surface + findings: `docs/decisions/product_verdict_fusion_calibration_surface_v0.md`; the corpus procedure: `docs/workflows/product_verdict_calibration_labeling_protocol_v0.md`, whose blind answer-key machinery (Phase B labeling worklist + label loader) is `calibration_corpus.py`; the Pass-1 note-adjective stance rubric (0.1→0.4) fix is blind-validated (non-circular re-extraction): methodology + per-product audit table in `docs/decisions/pass1_actionable_stance_calibration_v0.md`, summary record in `docs/decisions/product_verdict_pass1_note_stance_calibration_validation_v0.md`. Not judgment-quality proof. |
| `forseti-harness/reports/` | Report-rendering code (case and source-observability reports); generated dry-run outputs under it are gitignored. |
| `forseti-harness/runners/` | CLI entrypoints for case runs, memorization probe, bounded Candidate URL Intake live first-contact sourcing, Reddit Graph Frontier / crawling graph register preparation, source-capture packets (incl. TikTok SCI single-video and parsed-batch admission runners `run_source_capture_tiktok_video_packet.py` and `run_source_capture_tiktok_batch_packet.py`, the text-free admitted-batch coverage/projection runners `run_tiktok_batch_coverage.py` / `run_tiktok_batch_projection.py`, and the headed/sessioned one-creator live staging runner `run_source_capture_tiktok_live_batch_probe.py`, plus the cross-archive `run_source_capture_historical_packet.py`, which runs the slice-E locate ladder and writes the selected rung's body plus a thin `archive_locate_metadata.json` ladder receipt), IG public creator capture (`run_source_capture_ig_reels_grid_packet.py` is the optimized `/reels/` grid default; `run_source_capture_ig_calls_packet.py` is legacy item-page fallback), the locked-list IG calls batch circuit guard `run_source_capture_ig_calls_batch.py` (wraps the per-profile IG calls packet runner, stops/cooldowns on circuit-break signals, no source discovery or comment capture), offline projection materialization such as `run_ig_creator_momentum_projection.py` and `run_ig_reels_grid_projection.py` (projects existing IG `/reels/` grid packets or appends by-key lake-derived records), Fragrantica Mini God Tier anonymous capture (`run_fragrantica_mgt_capture.py`: direct HTTP + initial viewport + bounded deep-scroll packets with a local bundle summary; no login/archive/projection/ECR/Cleaning claim), Fragrantica current-window packet projection (`run_fragrantica_projection.py`), creator-profile-current materialization/checking (`run_creator_profile_current_materialize.py`: deterministic account-ledger + metric-seed/snapshot -> checked-in creator profile view, with `--check` for staleness and `--write` for refresh), Creator Registry match preflight (`run_creator_registry_match_preflight.py`: exact-match candidate account receipts that block unsafe `new_capture`; no fuzzy/cross-platform/live/mutation claim), and the standalone live-lake freshness gate (`run_live_lake_freshness_gate.py`: re-runs latest-per-account selection against the live lake and reports FRESH or `snapshot_behind_lake`; operator-local, exit 0/2), local Retail/PDP packet-directory projection (`run_retail_pdp_projection.py`; no capture, ECR, Cleaning, or Judgment), the no-network fragrance purchase-review focused coverage runner (`run_fragrance_review_coverage.py`; saved widget/PDP files only, selected reader bodies plus skipped metadata/hashes; no capture, ECR, Cleaning, or Judgment), the rendered+widget fragrance purchase-review capture runner (`run_fragrance_rendered_widget_companion.py`; one PDP render plus same-load widget response preservation, optional bounded widget fallback URLs in the same operator command; emits a rendered companion plus focused review coverage subreceipt; not ECR, Cleaning, or Judgment), the fragrance purchase-review discovery runner (`run_fragrance_review_discovery.py`; per-retailer review-positive new-PDP discovery via cadence-limited Judge.me probe or the Yotpo store-level reviews feed; emits candidate PDP URLs only, not capture, ECR, Cleaning, or Judgment), the fragrance purchase-review preserved-body lake tee runner (`run_fragrance_review_lake_packet.py`; reads an existing rendered-widget companion receipt and preserves its raw review widget-response bytes into a Source Capture Packet via the standard `--data-root`/`--output` lake seam; no network capture, ECR, Cleaning, or Judgment), the opt-in Retail/PDP CloakBrowser projection sidecar (`run_source_capture_cloakbrowser_packet.py --source-family retail_pdp --retail-pdp-projection-output <path>`), the no-network Capture/ECR/Cleaning smoke stitcher (`run_capture_ecr_cleaning_smoke.py`; consumes existing packet/projection/consolidation artifacts only), the no-network Cleaning periodic audit runner (`run_cleaning_spine_periodic_audit.py`; consumes frozen smoke manifests plus existing packet/projection/ECR/Cleaning outputs and classifies capture preflight, projection, and Cleaning breakpoints without scheduling or live capture), the daemon-ready YouTube transcript product extraction runner `run_transcript_product_extract.py` (idempotent scan of committed transcripts → silver product-mentions lake lane; injected transport, offline-testable), the Instagram-Reels transcript lane (`run_source_capture_ig_reels_audio_packet.py`: anonymous yt-dlp bestaudio capture + ASR `transcript_asr` write, `access_gated` typed skip for audience-restricted Reels; `run_ig_reels_product_extract.py`: the daemon-ready IG analogue discovering `instagram_creator`/`ig_reels_audio` packets → silver product-mentions; `run_source_capture_ig_reels_deep_capture.py`: the ONE-render reel deep-capture deriving BOTH audience comments and the creator transcript from a single anonymous browser render, collapsing the comments+audio double-fetch; `run_source_capture_ig_reels_creator_deep_capture.py`: scans a creator's `/reels/` grid, ranks reels by engagement, and deep-captures + persists the top-N via the silver lake adapter `source_capture/ig_reels_deep_capture_lake.py`; `run_ig_reels_operator_product_extract.py`: exports/imports operator Codex-assisted strict-JSON product extraction packets into the same silver product-mentions lane; `run_ig_reels_lane_orchestrator.py`: sequences requested IG grid, deep-capture, operator-product, and projection lanes with shared receipts and no YouTube/TikTok acquisition coupling), and source-observability reports. Retail/PDP binding/residual implementation lives in `forseti-harness/source_capture/retail_pdp_projection.py`; the fragrance review preserved-body lake tee + projection lives in `forseti-harness/source_capture/fragrance_review_lake.py`. The runners named here are illustrative, not exhaustive; enumerate with `git ls-files forseti-harness/runners/*.py`. |
| `forseti-harness/runners/run_source_capture_youtube_watch_packet.py` | CLI entrypoint for YouTube watch-page metadata/comments SourceCapturePacket writes; wraps the incumbent watch fetcher, supports data-lake mode, preserves availability states and metric route receipts, and makes no transcript/Cleaning/Judgment claim. |
| `forseti-harness/runners/_youtube_cli.py` | Shared argv normalization helper for YouTube capture runners; allows a valid leading-dash 11-character YouTube id to pass as `--video-id -...` while preserving ordinary argparse errors for registered option strings such as `--data-root`. Used by the watch, caption, and ASR packet runners. |
| `forseti-harness/runners/run_data_lake_doctor.py` | CLI entrypoint for v4.1 Data Lake operator inspection: verifies root/epoch context through `DataLakeRoot.resolve`, reports raw packet counts, availability-index gaps/staleness/orphans, wrong-shard or legacy-flat raw packets, read/hash failures, and unexpected top-level folders; writes only when `--rebuild-availability` is explicitly set. |
| `forseti-harness/runners/run_data_lake_catalog.py` | CLI entrypoint for the generated Bronze Catalog v0: inspect-only by default, `--census` emits a read-only observed Bronze source-surface / Attachment Record coverage census, nonzero on missing/stale/orphaned generated catalog files, reports self-describing source-surface and generated Attachment Record coverage, and replaces `indexes/derived_retrieval/bronze_catalog/v0` from verified raw packets only when `--rebuild` is explicitly set. |
| `forseti-harness/cases/` | Tracked deterministic fixture case(s) (e.g. TR/Casetext v0.14) with evidence, packet, and ledger; generated `scores/` and run outputs are gitignored. |
| `forseti-harness/config/` | Static YAML config (contestants, models, prompts) consumed by runners. |
| `forseti-harness/docs/` | Harness operating docs: source-capture packet and agent runbook, source-observability record guide, and scalability note. |
| `forseti-harness/tests/` | `unit/`, `contract/`, and `integration/` tests plus fixtures, including no-LLM-import, no-tools contract guards, Fragrantica projection/Cleaning/lake tests, data-lake doctor inspection tests, Bronze Catalog rebuild/inspect/stale/orphan tests, Commission Signal Board validator fixtures, CSB-first scanning artifact checker fixtures, creator public-handle linkage synthetic/adversarial fixtures, and TikTok SCI single-video, parsed-batch admission, admitted-batch coverage/projection, live batch probe parser/runner, and blocker-triage tests. |
| `forseti-harness/harness_utils.py`, `forseti-harness/Makefile`, `forseti-harness/pyproject.toml` | Shared utilities, dev shortcuts, and package metadata (optional `[browser]` Playwright extra). |

Controlling build authority:
`docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
(source-capture armory) and
`docs/decisions/data_capture_spine_source_observability_local_support_implementation_execution_authorization_v0.md`
(local source-observability support).

Generated/gitignored scratch — do not enumerate or treat as authoritative:
`forseti-harness/_test_runs/` (scratch; does not exist yet on a fresh clone), `_auth_state/`, `pytest_*` temp dirs,
`reports/source_observability/*_dry_run.*`, `cases/*/*/scores/`, and
`memory/logs/`.

## Product Anchor Files

Use these before broad product architecture or CA setup:

| Path | Use for |
| --- | --- |
| `docs/decisions/forseti_product_thesis_consumer_demand_v0.md` | Forseti thesis (consumer-demand decision intelligence, beauty first; owner-ratified 2026-06-12; supersedes `docs/decisions/turn_08_product_thesis_v0.md`), value proposition, strategic center, product boundary. |
| `forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md` | Offer hypothesis, buyer-facing language, first proof offer, ICP boundary. |
| `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md` | First buyer-proof packet, proof gates, pull signals, kill/graduation criteria. |
| `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md` | Current first-proof ICP wedge (beauty operator door; owner co-ratified 2026-06-12; supersedes pricing-first) and decision-family focus. |
| `forseti/product/spines/product_lead/proof_charter/forseti_product_proof_lead_charter_v0.md` | Product proof lead role and proof execution boundary. |
| `forseti/product/spines/product_lead/proof_charter/forseti_claim_defense_doctrine_v0.md` | Operative external-claims policy (owner-signed 2026-06-11): built-to vs proven-at, per-tier wording table, debunking triage. Read before any externally visible sentence about Forseti's judgment evidence. |

## Judgment Spine

The Judgment Spine spans **both** trees — `docs/research/judgment-spine/` (thesis, manifest, cases, harness) and `forseti/product/spines/judgment/`. **Open the consolidation map first**: it is the single `retrieval_only` entry that orients across both trees and routes one hop to every owner. Do not pre-load the owners from here.

| Path | Use for |
| --- | --- |
| `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | **Judgment Spine entry map — open first.** Per-area summary, owner-native status, and one pointer for thesis, cases/manifest, conductor, gate ownership, evidence ladder, JSG-08, harness, current decomposition, and fragrance Level 1 product-learning organizers; routes to the owners rather than restating them. Use the current-state/decomposition and fragrance Level 1 routes for backtest product-learning setup; use the conductor for the JSG run lane. Both are product-learning/not-proof unless owner gates say otherwise. |

## Data Capture Spine

The Data Capture Spine spans product authority, source-access decisions, Source
Capture Armory docs, source-quality support, and `forseti-harness/` implementation.
**Open the repo submap first** for capture/armory work: it is the
`retrieval_only` entry that orients across these surfaces and routes one hop to
the owner sources. Do not pre-load all capture artifacts from this map.

| Path | Use for |
| --- | --- |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | **Data Capture Spine repo submap — open first.** Routes to Capture obligations, source-access boundary, build authorization, method plan, Source Capture Armory README, packet lifecycle, harness runners, source-quality support, and current Reddit pre-commercial routing. Map only; not validation, readiness, source-access permission, or implementation authority. |
| `forseti/product/spines/capture/core/contracts/corpus_intake/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md` | **Corpus Intake (standing-capture) obligation contract — owner-ratified 2026-06-15.** The standing sibling of the v0 commissioned obligation contract: the obligation home for recurring capture of an approved public signal into an append-only corpus before a Decision Frame. Ratified, not pressure-tested; authorizes no build, scheduler, runtime, or source access. |
| `forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md` | **LinkedIn lane entry map — open first for any LinkedIn task.** THE canonical cold-start index for LinkedIn access (no-live, planning-only): ties the authority docs + the slice-1/slice-2 harness + the hard rails + deferred work + cross-vendor review provenance. |
| `forseti/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md` | Capture-spine-level backlog of deferred, legally-gated capabilities (relationship-graph analytics; contact/outreach) surfaced during LinkedIn discovery design — non-authorizing, out of scope for all discovery lanes. |
| `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | **Capture-investigation method (the playbook).** The repeatable "read the problem -> point to the route" method for deciding whether/how a NEW source is capturable, within entitlement, by the cheapest route. Recency/currentness can raise preservation urgency/source-drift priority without changing proof or route binding. The IG lane now records standalone anonymous `yt-dlp` empty media as a route-specific failure whose next matching route is browser-rendered deep-capture, while full durable media/video preservation remains unproven. MVP = entitlement gate (Step 0) + read + route catalog + pointer + guardrails; per-source recipe cards are a growing tail authored BY probes. Review-hardened draft (de-correlated artifact review, AR-01..AR-07 adjudicated) with a later owner risk-posture amendment (status `RISK_POSTURE_AMENDED_V0` - check the Risk Posture section before applying); non-authorizing, not validation/readiness. |
| `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` | Capture recon consolidation index - the per-source probe findings (forums / pricing / archive / PDF / reviews / embedded-state / social routes) the playbook distills from, incl. worktree-pending findings, IG public-web route probes, and the explicit remaining TikTok recon gap. Non-authorizing. |
| `forseti/product/spines/capture/core/source_families/README.md` | **Capture source-family lane catalog - open first after the generic Source Capture Playbook identifies a known source/platform.** Routes to family indexes for fragrance native database, Retail/PDP, Instagram, TikTok, YouTube, Reddit, creator registry, and the cross-archive historical route; retrieval-only, not Data Lake/ECR/Cleaning authority. |

## Creator Signal Spine

Creator Signal is the high-level product/signal spine for the creator intelligence
profile surface. It consumes Capture-owned identity, metric, rollup, and
ideal-audience records; it owns operator/buyer presentation and claim language.
Map only: not validation, readiness, buyer proof, runtime, storage, dashboard,
live capture, outreach, or public-directory authority.

| Path | Use for |
| --- | --- |
| `forseti/product/spines/creator_signal/README.md` | Creator Signal spine front-door and ownership boundary. |
| `forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md` | Product-facing one-stop creator intelligence profile surface contract. |
| `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` | Spine-promotion binding and DCP receipt. |

## ECR Source-Side Spine

The ECR source-side spine spans the integrity postures (ECR SP-1/2/3/6) and the
deprecated/dormant sibling content contract (Signal Content Record), their shared
deriver discipline, and the boundary to the JSG-01 conductor. **Open the repo
submap first**: it is the `retrieval_only` entry that states the cross-kind
invariants and routes one hop to every owner. Do not pre-load the ECR/SCR owner
docs from this map.

| Path | Use for |
| --- | --- |
| `docs/workflows/ecr_spine_submap_v0.md` | **ECR source-side spine repo submap — open first.** Routes to the SCR deprecation/direction + deriver plan, the ECR frame + SP-1/2/3 + SP-6 slices, the receipt-translator origin, the schema-evolution doctrine, and the built `forseti-harness/ecr/` + retained `forseti-harness/signal_content/` code. States the reference-never-merge / per-kind-grain / carry-or-residualize / re-derive-not-migrate / conductor-boundary invariants. Map only; not validation, readiness, ratification, a JSG-01 unfreeze, or Evidence-Unit binding. |

## Core Spine Files

| Path | Use for |
| --- | --- |
| `forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md` | Core Spine product contract and eight primitives. |
| `forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md` | Manual information-production foundation and Evidence Unit standard. |
| `forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Data Capture/Cleaning/Judgment boundary and Evidence Candidate Record setup context. |
| `forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | Signal Content Record (v0) architecture DIRECTION + deprecation posture — retained compatibility/future-revival contract for the content object, no longer a default standalone pre-Judgment generated layer. Current default route is evidence pack -> Judgment-authored signal interpretation. Direction only; the final Evidence Unit field architecture stays owner-reserved. v0 model lives in `forseti-harness/signal_content/`. |
| `forseti/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md` | Proposed Core Spine design note on placing independent-corroboration vs artificial-amplification discipline across the Cleaning/Judgment boundary; proposed, not validated. |
| `docs/decisions/daimler_advisory_001_claim_tier_classification_decision_v0.md` | Daimler advisory claim-tier classification decision recording the current no-durable-evidence state, required product-learning receipt before any evidence claim, and blocked buyer-proof/judgment-quality claims. |
| `forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md` | Signal-use and engagement interpretation registry. |
| `forseti/product/spines/foundation/product_contract/core_spine_v0_proof_protocol_v0.md` | Core proof protocol. |
| `forseti/product/spines/foundation/product_contract/core_spine_v0_proof_input_selection_v0.md` | Proof input-selection rules. |
| `forseti/product/spines/foundation/product_contract/core_spine_v0_proof_packet_preflight_v0.md` | Proof packet preflight. |
| `forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md` | WHERE-side vertical exploration guide (owner-adopted Shape C; renamed 2026-06-11 from the venue exploration procedure): batch-scoped walk steps, commons split, influence yield, promote-on-reuse trigger. Subordinate to the case-finder frame; amendments are dated notes. |
| `forseti/product/satellites/beauty/beauty_venue_card_set_v0.md` | Beauty venue card-set (promoted 2026-06-11; the ONE maintained venue asset — 12-card hard cap, per-card review dates): read FIRST at Step 0 of any beauty/personal-care screen, fragrance included. Binding terms: `docs/decisions/beauty_venue_card_set_promotion_decision_v0.md`. |

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

- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_replay_packet_v0.md`
- `forseti/product/spines/foundation/product_contract/core_spine_v0_method_validation_rubric_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_locks_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md`

## Proof-Case Discovery Files

Use for customer discovery, target selection, and proof-case candidate
discovery. (The jb-era first-proof-run set — packet preparation, run charter,
locks, packet, and the jb/bt204/sh01 slices — was scrapped in PR #303; a fresh
proof rebuilds on the discovery candidates below.)

Key files:

- `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_target_selection_brief_v0.md`
- `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_qualification_prep_sentry_clerk_v0.md`
- `forseti/product/spines/product_lead/icp_wedge/orca_discovery_batch_0_candidate_context_scan_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md` (discovery-scope charter), `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md` (READY_FOR_OWNER_CASE_SELECTION), and `forseti/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md` (backtest candidates; proposes BT2-01 Chegg/ChatGPT) — the heavyweight proof-case discovery pass that produced the candidates the older case-selection brief was blocked on.

## Backtest Specimens

Use when the task is specifically about historical cutoff discipline or the
Unity runtime-fee specimen:

- `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- `forseti/product/case_families/product_learning/other_verticals/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`

## Prompt Families

| Path | Use for |
| --- | --- |
| `docs/prompts/product-planning/` | Product planning prompt drafts. |
| `docs/prompts/feature-planning/` | Feature planning prompt drafts. |
| `docs/prompts/deep-thinking/` | Deep reasoning prompt drafts. |
| `docs/prompts/handoffs/` | Handoff prompt drafts. |
| `docs/prompts/reviews/` | Review prompts, including the delegated adversarial review-patch prompt for the Bronze full-GT A-D scoping artifact. |
| `docs/prompts/reviews/creator_registry_operational_sequence_delegated_review_patch_prompt_v0.md` | Filed prompt for independent delegated adversarial review-and-patch of the Creator Registry operational sequence across merged PRs #654/#660/#667 and open PR #669; patch scope is limited to the named usage, runbook, scan, checker, rehearsal, map, and handoff-prompt surfaces and all findings remain CA-adjudicated decision input. |
| `docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_prompt_v0.md` | Filed prompt for independent delegated adversarial review-and-patch of the Bronze full-GT A-D scoping artifact; patch scope is limited to the scoping artifact and all findings remain CA-adjudicated decision input. |
| `docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_prompt_v0.md` | Filed prompt for cross-vendor delegated adversarial review-and-patch of the landed physicalization decision brief (PR #557) before Gate 1/Gate 2 ADR authoring relies on it; patch scope is the brief only and all findings remain CA-adjudicated decision input. |
| `docs/prompts/reruns/` | Rerun prompts. |
| `docs/prompts/patches/` | Patch prompts (accepted family). |
| `docs/prompts/wrappers/` | Thin wrapper prompts. |
| `docs/prompts/templates/` | Local prompt templates. |
| `docs/prompts/architecture/` | Architecture prompt family. |
| `docs/prompts/advisory/` | Advisory prompt family. |
| `docs/prompts/hygiene-queue/` | Drift/parking area (created on first artifact; does not exist yet); not listed as an accepted prompt-family folder in the overlay. |

A few Data Capture pressure-test prompts currently sit unfiled at the
`docs/prompts/` root rather than in a typed family folder; treat them as drift
pending hygiene triage.

## Research And Review Areas

| Path | Use for |
| --- | --- |
| `docs/research/consulting-judgment-corpus/` | Consulting-judgment corpus, prompts, lane outputs, synthesis, candidate screens, backtestability, and reject patterns. |
| `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md` | AEO Phase-0 feasibility probe evidence rehomed from the scanning product spine; use as research evidence for the answer-engine source-class spec, not as product-spine authority. |
| `docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md` | Fresh CSB-first Imaginary Authors discovery follow-up focused on public buyer-origin venue value, exact-query negatives, capture-preservation triage, and no-candidate closeout. |
| `docs/research/orca_discovery_candidate_scan_imaginary_authors_buyer_language_rerun_v0.md` | Bounded buyer-language rerun for the Imaginary Authors CSB-first scan; records Parfumo as a high-value public community/review venue, two low-commitment candidate entries, and a preservation-only capture_request. |
| `docs/research/orca_discovery_candidate_scan_imaginary_authors_broad_scout_deep_scan_v0.md` | Fresh CSB broad-scout plus main deep-scan artifact for Imaginary Authors; confirms Parfumo as the high-value public buyer-language venue, carries two hold-low-commitment candidate entries, and records preservation-only capture requests. |
| `docs/research/orca_discovery_candidate_scan_beauty_neutral_chatgptpro_v0.md` | Clean advisory intake of the neutral ChatGPT Pro beauty/personal-care niche answer; use before any no-contact verification scan or owner niche-selection decision. |
| `docs/research/orca_discovery_candidate_scan_food_vs_fragrance_chatgptpro_v0.md` | Advisory intake of the ChatGPT Pro food-vs-fragrance category answer; use before deciding whether to keep fragrance as the first no-contact verification scan or reopen food as a comparator category. |
| `docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md` | Bounded public/no-login YouTube fragrance creator discovery scan using Creator Registry exact-match preflight; carries candidate batch and receipt pointers plus capture-request handoff rows only, with no capture, registry mutation, metric refresh, or Silver write. |
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
| `forseti/product/spines/judgment/toolkit_gaps/judgment_spine_toolkit_blocker_specs_from_daimler_source_fanout_v0.md` | Toolkit capability specs inferred from the Daimler source fanout (cutoff provenance, evidence registry, packet compiler, isolation checker); planning only, not build/runtime authorization or a judgment-quality claim. |

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
Use the targeted sections named by `.agents/workflow-overlay/source-loading.md`, then expand only when a
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

- `docs/decisions/forseti_product_thesis_consumer_demand_v0.md`
- `forseti/product/spines/product_lead/offer/forseti_offer_hypothesis_v0.md`
- `forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md`
- `docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`
- `.agents/workflow-overlay/product-proof.md`

### Core Spine Evidence Standard Work

Start with:

- `forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md`
- `forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md`
- **Open `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` first** for any Judgment Spine work; it routes to the ladder, gate ownership map, conductor, JSG-08 owner contract, current-state/decomposition, and fragrance Level 1 product-learning organizers.
- `forseti/product/spines/judgment/judgment_current_state_and_decomposition_v0.md` when the work is Level 1 backtesting-first product learning: core/satellite split, commission gate, source registry, outcome labels, forecast/action/log/evaluation artifacts, satellite fill, or fragrance backtest setup.
- `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md` when the work classifies Judgment Spine claim tier, proof tier, buyer-proof boundary, or judgment-quality boundary.
- `forseti/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md` when the work needs to route or block Judgment Spine gate ownership before claim promotion.
- `forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md` — **the Judgment Spine conductor; open this FIRST for the judgment run lane** (running or planning any case through gates JSG-01 to JSG-10). It sequences the gates and routes to the evidence ladder, gate ownership map, and JSG-08 owner contract rather than restating them; use it to decide a run lifecycle state or check what a partial or by-hand run can claim. It is the path toward judgment-quality evidence, not proof — by-hand runs cap at product-learning.
- `forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md`
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
    - "forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md"
    - "forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
    - "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
  intentionally_not_updated:
    - path: ".agents/workflow-overlay/source-loading.md"
      reason: "The canonical read-pack still routes Data Capture work through the consolidation sub-map. This patch adds a top-level anti-friction cue, not a new source-loading pack."
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "The Armory README already records CloakBrowser implementation limits and non-claims. This patch changes repo-map discoverability, not Armory implementation."
    - path: "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
      reason: "The authorization already controls CloakBrowser/proxy allowance. This patch does not change the owner decision."
  stale_language_search: "rg -n \"Reddit CloakBrowser / Proxy Allowance Quick Route|CloakBrowser is the approved primary|residential/rotating|Candidate URL Intake may record this approved downstream route|approved primary anti-blocking route|not blanket stop\" docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md forseti/product/spines/capture/core/source_capture_toolbox/reddit_precommercial_capture_consolidation_success_signal_architecture_v0.md"
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
    - "forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md"
    - "forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md"
    - "docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/decision-routing.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - "docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md"
    - "docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md"
  intentionally_not_updated:
    - path: "forseti/product/spines/capture/core/source_capture_toolbox/README.md"
      reason: "Graph Frontier is not Source Capture Armory and does not emit Source Capture Packets."
    - path: "forseti-harness/docs/source_capture_agent_runbook.md"
      reason: "No runner behavior changed and this patch does not authorize implementation execution."
  stale_language_search: "rg -n \"Future Crawler-Graph|future crawler|may be architected|architected or rejected|candidate_graph_ledger|crawler_graph_exploration_lane|should wait for an architecture decision|Commission the separate crawler-graph|accepted Reddit Graph Frontier|Graph Frontier Register\" docs/workflows/orca_repo_map_v0.md docs/workflows/data_capture_spine_consolidation_map_v0.md forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md docs/workflows/reddit_candidate_intake_to_projection_lane_handoff_v0.md"
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

Older receipts, when cycled out, are archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.

## Workstream Status Pointers

Owner-ratified 2026-06-13. Status values are verbatim from each owning doc's
status field. Open the owning doc for authority; this table is navigation only.

| Workstream | Owning doc | Status |
| --- | --- | --- |
| Beauty vertical satellite | `forseti/product/satellites/beauty/beauty_venue_card_set_v0.md` | venue card set promoted; no separate beauty vertical satellite owner doc exists |
| Data capture spine | `forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md` | `PROPOSED_ARCHITECTURE_V2` |
| Creator Signal spine | `docs/decisions/orca_creator_signal_spine_promotion_binding_v0.md` | owner-accepted spine-promotion binding v0; surface contract promoted, no runtime/storage/dashboard authority |
| Judgment spine | `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md` | no status field |
| ECR | `docs/workflows/ecr_spine_submap_v0.md` | no status field |
| Signal content | `forseti/product/spines/ecr/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | `OWNER_DECIDED_DIRECTION`; `DEPRECATED_AS_STANDALONE_PRE_JUDGMENT_LAYER` |
| Source capture toolbox | `forseti/product/spines/capture/core/source_capture_toolbox/README.md` | `SOURCE_CAPTURE_ARMORY_README_V0` |
| Core spine | `forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md` | `PROPOSED_FREEZE` |
| Search lane | `docs/decisions/orca_search_product_lane_binding_v0.md` | owner-authorized v0; demand-signal intelligence (search-led): search/answer-engine surfaces + demand-scan/read/gate method |
| Spine-first target structure | `docs/decisions/orca_spine_first_target_structure_binding_v0.md` | executed by spine-first migration; current product tree routes through `forseti/product/` |
| Spine-first blocker authorization | `docs/decisions/orca_spine_first_blocker_authorization_v0.md` | B1-B7 execution settlement consumed by the spine-first migration |
| Aphrodite fragrance sub-ontology | `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml` | `DATED_DATA_2026-07-04` |

## Not-Proven Boundaries

This map does not prove acceptance, validation, readiness, buyer pull,
implementation authorization, source correctness, or freshness of every listed
artifact. Listing `forseti-harness/` reflects authorized, bounded implementation
only; it does not assert runtime readiness, that its build scope is validated,
or that any gated surface (production runtime, API/commercial fetch, ECR,
Cleaning, Judgment) is authorized. Check the target artifact, retrieval header,
and current `git status` before strict claims.
