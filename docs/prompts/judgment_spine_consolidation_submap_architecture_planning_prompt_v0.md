# Judgment Spine Consolidation Submap — Architecture-Planning Prompt (v0)

```yaml
retrieval_header_version: 1
artifact_role: Orca prompt artifact (architecture-planning brief, posted out for independent runs)
scope: Decide the information/retrieval-topology architecture for the Judgment Spine consolidation submap — entry-point, routing, authority boundary, internal structure, frozen-excerpt scope, generalizability, versioning.
use_when:
  - Running or re-running the Judgment Spine consolidation-submap architecture pass.
  - Adjudicating independent outputs of this pass.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/README.md
  - .agents/workflow-overlay/artifact-folders.md
```

> Planning-only architecture brief. It is posted out for independent runs; outputs
> return to the Orca CA for adjudication between runs. This is the consolidation
> map's **design** pass — it authors nothing, edits nothing, and claims no readiness.
> The map's *shape* is already settled (≈80% retrievable map + ≈20% frozen-primitive
> excerpts); this pass settles the **topology** around it.

---

## 1. Objective and Intended Decision

Settle the target information/retrieval-topology architecture for a durable Judgment
Spine **consolidation submap** — the single, always-findable entry point a downstream
ECR or Cleaning lane (and future maintainers) open first to orient and route into the
live spine source. The intended decision is the target architecture + boundaries +
invariants + the smallest-complete next routing object — not the artifact's prose.

## 2. Receiver Start Preflight (orca_start_preflight)

Establish and state before APPLY:

- `AGENTS.md` and `.agents/workflow-overlay/README.md` read or supplied in this context.
- Source pack: custom — the Judgment Spine corpus + overlay folder/metadata authority (Section 4).
- Workspace: the Orca repo (read access to the `docs/` tree required) or be supplied the tree.
- Branch/revision: `main`. The judgment-spine corpus is largely **untracked working-tree WIP** — read working-tree content, not HEAD.
- Dirty-state: untracked files ARE in scope; read the working tree.
- Controlling-source state: planning-only pass; no strict claims depend on overlay cleanliness, so it is not gating here.
- Doctrine change: none in this pass. Adopting the output (e.g., a new accepted submap folder or a reusable template) is a **separate** decision requiring the Doctrine Change Propagation Contract — do not perform it here.
- Target: read-only over `docs/research/judgment-spine/**`, `docs/research/judgment-spine/README.md`, `docs/workflows/orca_repo_map_v0.md`, and the conductor / gate-map / JSG docs.
- Edit permission: `read-only`.
- Output mode: `chat-only`.
- External source boundary: `agent-workflow` is read-only reusable source; `jb` is not Orca authority.

## 3. Source-Gated Method Sequence (do not shortcut)

1. Read authority: `AGENTS.md`, `.agents/workflow-overlay/README.md`, `source-of-truth.md`, `artifact-folders.md`, `retrieval-metadata.md`, `prompt-orchestration.md`.
2. `REFERENCE-LOAD` `workflow-deep-thinking` then `workflow-architecture-planning` — guidance only. Do **not** `APPLY` yet; before source readiness, only neutral source-reading lenses are allowed.
3. `SOURCE-LOAD` the Judgment Spine corpus and the named files (Section 4).
4. Declare `SOURCE_CONTEXT_READY`, or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, gaps, exclusions, and conflicts.
5. Only then `APPLY`: run the three lenses (Section 7) and synthesize (Section 8).

## 4. Orca Source Hierarchy and Required Reads

- Overlay authority (placement/topology/headers): `artifact-folders.md`, `retrieval-metadata.md`, `prompt-orchestration.md`, `source-of-truth.md`.
- Corpus: `docs/research/judgment-spine/**` — thesis, `README.md`, harness `v0_14/` specs + `index.md`, fixtures, cases.
- Controlling spine contracts (locate exact paths during SOURCE-LOAD; do not assume): the judgment-quality conductor / operating model, the gate map, and gates JSG-01…JSG-10.
- Parent map (read-only, do **not** edit): `docs/workflows/orca_repo_map_v0.md`.

## 5. Accepted Inputs (do not re-litigate; flag only if a lens proves one wrong)

- Shape: retrievable map (per-area `{2–4 line summary, current status, pointer to the source-of-truth doc}`) + a small frozen-excerpt sliver.
- The spine's own core invariant: **route-don't-restate** (dependents point to owner fields, never copy).
- The corpus is **active** (conductor "test-worthy, not proven"; ECR mid-setup; 3 gates deferred) and woven with **path + content-hash provenance pins**.
- Candidate frozen primitives for the 20% sliver (VALIDATE which are truly frozen): thesis one-liner; conductor invariants A (no-authority / LLM-never-the-gavel) and B (route-don't-restate); the 5 seams; the 4-value outcome precedence `[cleared, contaminated_or_blocked, held, not_cleared_or_indeterminate]`.

## 6. Architecture Decisions To Settle (working recs to validate or revise)

1. **Entry-point topology** — one rich entry vs two. Rec: dedicated `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` as the rich submap; `docs/research/judgment-spine/README.md` stays the thin door + one-line pointer.
2. **Routing** — repo-map → submap → spine docs, single hop each, no layer re-listing another's contents. `orca_repo_map_v0.md` gets ONE "Judgment Spine → submap" entry.
3. **Authority boundary** — submap is `retrieval_only`, one-way (map → source docs); source docs never cite the submap as authority.
4. **Submap internal structure** — section-per-area for headers/grep; per-area `{summary, status, pointer}`; the frozen-excerpt set + how each is labeled (`excerpt — verify against <source>`) so it cannot drift silently.
5. **Status-field discipline** — how the submap reports proven / test-worthy / deferred without itself becoming an overclaim.
6. **Generalizability** — is this the reusable template for future submaps (capture spine, etc.)? Define the core/satellite pattern once.
7. **Versioning** — v0 lifecycle and how it relates to the README door.

## 7. Run As Three Independent Lenses

Run THREE independent architecture passes from the lenses below — as separate
**sub-agents** if the runtime supports them, otherwise as three **isolated internal
passes** that do not share reasoning until synthesis. Each is read-only and
planning-only.

- **Lens 1 — Cold-reader / retrieval** (downstream consumer): optimize for an ECR/Cleaning lane opening this cold. Owns #1, #4 (consumer view), status legibility. Q: can a zero-context reader orient in one read and route correctly?
- **Lens 2 — Provenance / drift-integrity** (adversarial maintainer): optimize for staying true over time against the active, hash-pinned corpus. Owns #3, the frozen-excerpt scope in #4, #5. Q: where does this drift, overclaim, or break pins — and what is the minimal sliver that won't rot?
- **Lens 3 — Repo-topology / nesting** (systems architect): optimize for how the submap nests in the whole doc graph. Owns #2, #6, #7, the core/satellite boundary. Q: does it nest cleanly, route single-hop, and generalize to other spines without recreating restate one layer up?

## 8. Each Lens Returns / Synthesis

Each lens returns (structured): target proposal for its owned decisions; boundaries/invariants it asserts; top failure modes it defends against; explicit disagreements or tensions to flag.

Synthesis (orchestrator, after all three): converge to ONE target architecture —
core/satellite boundaries, invariants, the routing object, submap internal structure,
validated frozen-excerpt set, versioning, generalizability. List decisions RESOLVED
vs OPEN (owner-needed). Surface cross-lens conflicts instead of averaging them. Name
the smallest-complete next step (build the submap). No edits.

## 9. Output Contract

- Output mode: `chat-only`, planning-only. No file edits, saves, or commits.
- Deliver: the synthesized target architecture; the RESOLVED-vs-OPEN decision ledger across all seven items; named cross-lens conflicts; the smallest-complete next routing object.
- Completeness gates (the output may fail these): all 7 decisions addressed; each is RESOLVED with rationale or OPEN with a precise owner-question; the routing object + next step are named; route-don't-restate is honored; no readiness / validation / source-of-truth claims appear (the submap is `retrieval_only`).

## 10. Hard Constraints / Non-Claims / Forbidden Imports

- Planning-only. No readiness, validation, approval, lifecycle, deployment, or source-of-truth claims. The submap is `retrieval_only`; it maps, it is not the territory.
- Honor route-don't-restate. Do not propose collapsing the corpus into a monolith.
- Do **not** modify `docs/workflows/orca_repo_map_v0.md` (it carries uncommitted concurrent-lane changes); its pointer is a later, isolated edit.
- Do **not** create a new accepted folder or change overlay doctrine in this pass; if the topology implies one, name it as an OPEN owner decision with required propagation.
- Do not import `jb` policy; `agent-workflow` is read-only reusable source only.

## 11. Assumptions, Unknowns, Blocked Conditions

- Unknown until source read: which candidate primitives are truly frozen (resolve in Lens 2) and the exact conductor / gate-map / JSG paths (locate in SOURCE-LOAD).
- If the receiver lacks read access to the Orca `docs/` tree, return `SOURCE_CONTEXT_INCOMPLETE` and request the judgment-spine tree + the two named files rather than guessing.

---

**Downstream:** this prompt is run independently (multiple runs and/or receivers);
each receiver returns its single best synthesis. The Orca CA adjudicates between the
returned outputs and only then authorizes building the submap.
