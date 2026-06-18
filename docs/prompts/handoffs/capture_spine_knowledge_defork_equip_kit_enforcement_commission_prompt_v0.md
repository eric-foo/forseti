# Capture Spine — Knowledge De-Fork + Capture Equipment Kit + Consult-Enforcement Design — Commission Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Implementation/design handoff prompt (cross-lane commission to the Capture Spine CA)
scope: >
  Commission the Capture Spine CA to (1) map the forked capture/escalation knowledge surfaces to one
  canonical home per lesson, (2) author a Capture Equipment Kit mirroring the Walker Equipment Kit, and
  (3) design (not build) the capture-consult enforcement. Design + doc-sync + overlay maintenance only.
use_when:
  - Routing the capture-knowledge de-fork / equip-kit / consult-enforcement design to the capture lane.
  - Checking the bound problem, deliverables, fitness reference, and boundaries for that commission.
authority_boundary: retrieval_only
branch_or_commit: ea2c79b
open_next:
  - orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md
downstream_consumers:
  - The capture-consult enforcement build (a later, separately authorized turn).
  - Future capture-probe subagents (consumers of the Capture Equipment Kit).
stale_if:
  - Any of the four named knowledge homes is restructured or re-homed before the commission runs.
  - The owner amends the capture risk posture or the screening-vs-packet-grade boundary.
```

## Orca Start Preflight (prompt author)

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes (prompt-orchestration, artifact-folders, retrieval-metadata; source-loading policy applied)
  source_pack: custom (S0 overlay prompt-mechanics + the four capture-knowledge homes below + Walker Equipment Kit)
  repo_map_decision: not_needed
  repo_map_reason: target homes are known by direct read; no repo-map routing required to author this commission.
  workspace: C:/Users/vmon7/Desktop/projects/orca-worktrees/orca-capture-commission-wt
  expected_branch_head: capture-knowledge-defork-commission-v0 @ ea2c79b (off origin/main)
  dirty_state_checked: yes (clean worktree off origin/main; this prompt file is new/untracked)
  controlling_source_state: overlay prompt-orchestration / artifact-folders / retrieval-metadata clean at ea2c79b
  target_scope: docs/prompts/handoffs/ (this commission prompt only)
  edit_permission: docs-write (this prompt artifact only; the receiving CA's edit authority is bound below)
  output_mode: file-write
  doctrine_change: none for authoring this prompt; the COMMISSIONED work changes output authority across
    capture surfaces and therefore requires a direction_change_propagation receipt at the CA's closeout.
  blocked_if_missing: none (problem, sources, and recs are inlined; self-contained for the capture CA)
```

---

## Commission

You are the **Capture Spine Chief Architect**. You are commissioned to resolve a structural problem in
the capture lane's own knowledge surfaces, then design (not build) the enforcement that keeps it solved.
This is **design + documentation-sync + overlay maintenance only**. It authorizes **no runtime build**,
**no capture run**, and **no merge to main**. The owner approved the direction in principle; the de-fork
edits, the kit authoring, and the enforcement *design* are your bounded lane.

### The problem

Capture/escalation knowledge is **forked across four hand-synced homes**, with **no single canonical home
per lesson**:

| Home | Path | Role today |
| --- | --- | --- |
| Evidence base | `docs/product/source_capture_toolbox/capture_recon_index_v0.md` | Per-source probe findings; lessons are *born* here (e.g. Pattern 5 "archive availability != body retrieval -> PARTIAL"; Pattern 1 "blocked is a hypothesis"). |
| Method | `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` | Substrate-first diagnosis + route catalog; restates "availability != body — check both"; Guardrail 4 "blocked is a symptom". |
| Tool manifest | `docs/product/source_capture_toolbox/README.md` (Source Capture Armory) | Adapter/runner manifest **plus its own parallel** Source-Quality Example Ladder (e.g. CW-P1 = archive availability != body). |
| Equip block | `docs/product/core_spine/orca_vertical_exploration_guide_v0.md` (Walker Equipment Kit, ~line 120) | Self-contained WALK CONTRACT pasted into every screening/discovery walk subagent — "walkers deploy equipped, not naked"; carries READ ESCALATION + KNOWN WALLS distilled from playbook+recon. |

The **same two lessons** (availability != body; blocked-is-a-hypothesis) are independently restated in
3–4 vocabularies (recon "Pattern N" / playbook route-cell / Armory "CW-P#" / kit "READ ESCALATION"),
kept aligned by **manual** dated-note sync + `direction_change_propagation` receipts + reverse-pointer
prose. They are **consistent today, not contradictory** — do not "fix a contradiction" that is not there.
The real defects are:

- **(a) Canonical ambiguity** — no single home a tool's consult-entry can point at.
- **(b) Drift risk** — N hand-synced copies will eventually diverge.
- **(c) No capture-lane equip-at-spawn** — the *working* enforcement model already exists for screening
  (the Walker Equipment Kit: a self-contained block pasted into every walk subagent), but the capture lane
  has **no equivalent**, so capture-probe subagents deploy "naked" and can skip the playbook + recon index.

**Named failure (the motivating incident — cite it):** an agent ran `run_source_capture_archive_packet.py`
directly, **skipped the playbook and the recon index**, and hit the **exact documented trap** — the archive
body redirected to a **post-cutoff snapshot** (availability != body). The tools and the lesson were already
in place; nothing forced consulting them.

### Fitness reference (anchor your design to this; attack it, don't rubber-stamp it)

```yaml
fitness_reference:
  goal: >
    A capture lane where every escalation lesson has exactly one canonical home, every other surface points
    rather than copies, and a capture-probe subagent cannot deploy without the distilled consult-surface.
  success_signal: >
    - The "availability != body" lesson resolves to ONE canonical home + N explicit pointers (zero parallel copies).
    - A capture-probe subagent cannot deploy without the Capture Equipment Kit.
    - A fresh agent reaching for a run_source_capture_* runner surfaces the matching consult-entry/trap BEFORE running.
```

## Deliverables

### D1 — Knowledge-surface map (canonical home per lesson; point, don't copy)

Produce a map that assigns **one canonical home per lesson** and converts every other appearance to a
**pointer**:

- **Recon index** = where lessons are born (evidence).
- **Playbook** = the method; it should *cite* recon patterns, not re-prose them.
- **Armory Example Ladder** = **de-fork it**: replace the parallel CW-# lesson list with a pointer at the
  playbook/recon canonical patterns. (This is the redundant fourth copy at the root of the problem.)
- **Kits** (Walker + the new Capture kit) = the **only legitimate leaf-copies** — self-contained for
  spawned agents — each carrying a **provenance line + dated-sync** back to the canonical source patterns.

Make the existing **bidirectional manual sync obligation** (the playbook and Walker Kit already declare
"keep in sync" by dated note) **structural** rather than dated-note-only: a pointer that cannot silently
drift is better than two copies promising to stay aligned.

### D2 — Capture Equipment Kit (mirror the Walker Equipment Kit)

Author a **self-contained paste-block** for every capture-probe subagent, the capture-side analogue of the
Walker Equipment Kit. Distill it from the playbook + recon index: at minimum the Step-0 access-control gate,
the two-axis bar (got-through vs got-the-real-thing), the route-catalog pointer, the **KNOWN traps**
(including availability != body), and the receipt/verdict contract (playbook Step 3). Carry the same
provenance + dated-sync discipline as D1. Operating line: **"capture probes deploy equipped, not naked."**

### D3 — Capture-consult enforcement **design** (design only — no build)

Design the enforcement; the owner approved these in principle. **Name the foregone limitation of each:**

1. **Equip-at-spawn** — the Capture Equipment Kit (D2) bound/pasted into every capture-probe subagent.
   *(Limitation: only as current as the kit; "add a tool" must pair with "add its consult-entry.")*
2. **Advisory, fail-open PreToolUse hook** for **direct (main-thread)** `run_source_capture_*` invocations,
   surfacing the matching consult-entry/trap. Mirror the existing fail-open posture of
   `check_prompt_provenance.py`. **A hard block is rejected as theater** — the precondition (did the agent
   actually read it?) is unverifiable, so a hard block enforces ceremony, not consultation.
   *(Limitation: advisory = a loud, effortful nudge, not a guarantee; it lowers skip-rate, it does not eliminate it.)*
3. **Post-run two-axis GO/PARTIAL verdict + receipt** (playbook Step 3) emitted after a runner completes.
   *(Limitation: catches the trap after the run, not before; pairs with #1/#2 to cover both sides.)*

Deliver the **design** (placement, data flow, the manifest the hook reads, the kit-binding shape). **Do not
build the hook** — building it is a separate, owner-authorized turn.

### D4 — Consider agent profiles (suggestion, not mandate)

Consider whether **reusable agent profiles** (subagent definitions that bake in tool grants + the equipment
kit + posture) are the right substrate so that **equip-at-spawn becomes a profile property** rather than a
manual paste — e.g. a `capture-probe` profile and a `walker/screening` profile. Recommend for/against with
reasons; this is an option to evaluate, not a required deliverable.

## Method (source-gated)

`REFERENCE-LOAD` `workflow-deep-thinking` and `workflow-architecture-planning` as procedural guidance only —
do **not** `APPLY` them yet. `SOURCE-LOAD` the four homes below (+ the Walker Equipment Kit). Declare
`SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the gap). Only then `APPLY`: frame the de-fork
boundary and failure modes first, then produce D1–D4. Be adversarial about your own map — the easy error is
to create a *fifth* surface that itself needs syncing.

### Source hierarchy / required reads

1. `docs/product/source_capture_toolbox/capture_recon_index_v0.md` — evidence base (lessons born here).
2. `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` — method (route catalog; Guardrails).
3. `docs/product/source_capture_toolbox/README.md` — Source Capture Armory tool manifest + Example Ladder.
4. `docs/product/core_spine/orca_vertical_exploration_guide_v0.md` — Walker Equipment Kit (the mirror target).
5. Overlay: `.agents/workflow-overlay/source-of-truth.md` (Doctrine Change Propagation Contract),
   `.agents/workflow-overlay/artifact-folders.md` (destinations).

## Boundaries / non-claims

- **Design + doc-sync + overlay maintenance only.** No runtime build of the hook; it is named as a design
  target. No capture run is authorized by this commission. This prompt is **non-authorizing** for capture.
- **No merge to main.** Land via the per-lane PR flow; the owner CLI-merges (protected-action guard).
- **Preserve the screening-vs-packet-grade boundary.** The Walker Equipment Kit is **screening-read only**
  (public pages, no logins, no bulk, URLs + short quotes); **packet-grade capture still routes through the
  investigation method.** The Capture Equipment Kit is the packet-grade analogue and must not collapse that
  distinction.
- **Cross-lane edit boundary.** The capture lane owns the recon index, playbook, Armory README, and the new
  Capture Equipment Kit. The **Walker Equipment Kit lives in a discovery-lane-owned file**
  (`orca_vertical_exploration_guide_v0.md`) — **coordinate with the discovery lane** before editing it; if
  coordination is not in scope this turn, deliver the Walker-side change as a **proposed** pointer for that
  lane to apply, not a unilateral edit.
- **Doctrine propagation.** The de-fork changes output authority across multiple controlling sources; the
  closeout must carry a `direction_change_propagation` receipt (or a `direction_change_propagation_blocker`)
  per `.agents/workflow-overlay/source-of-truth.md`.

## Output contract

- **Output mode:** `file-write` (your lane), findings/design-first. Recommended destinations (you bind the
  final paths):
  - D1 map → `docs/product/source_capture_toolbox/capture_knowledge_surface_map_v0.md` (new; the
    canonical-home authority).
  - D2 Capture Equipment Kit → a canonical block in the playbook **or** a new
    `docs/product/source_capture_toolbox/capture_equipment_kit_v0.md` (mirror how the Walker Kit lives in its
    guide); state your choice and why.
  - D3 enforcement design → a design note under `docs/product/source_capture_toolbox/` or a
    `docs/decisions/` record; D4 may ride D3.
  - De-fork pointer edits → the Armory README (ladder → pointer), recon/playbook cross-citations, and the
    **proposed** Walker-side pointer.
- **Closeout:** a short headed human summary (what is now canonical, what now points, what was deliberately
  left as a leaf-copy and why), then path/status receipts and the propagation receipt. State the **named
  residual** honestly: advisory enforcement is a nudge; sync is now structural for the de-forked surfaces but
  the kits remain deliberate copies under dated-sync.

## Hard constraints recap

- You design and document; you do not build the hook, run a capture, or merge.
- Do not create a fifth parallel knowledge surface; canonical-home-plus-pointers is the whole point.
- Keep the risk posture and screening/packet boundary intact; coordinate cross-lane edits.
- This commission is product-learning-adjacent infrastructure, not a validation, readiness, or
  capture-authorization claim.
