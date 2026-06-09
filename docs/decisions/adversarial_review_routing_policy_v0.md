# Adversarial Review Routing Policy v0 — PROPOSED (revised after same-family review; pending cross-family arm + owner acceptance)

> **STATUS NOTICE.** Every rule below is **PROPOSED**, not binding. This record changes no
> existing doctrine and binds nothing until ratified. Read "must / always / never" as
> "the proposed rule is…", not as an in-force mandate.

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Proposed routing policy for review DECORRELATION (which family + agent composition reviews
  which artifact class) layered over the existing review lanes in review-lanes.md, plus the
  same-family substitute spec in two cross-family access modes (no-repo / with-repo). Per-project
  (orca). jb may transfer the principle but is not bound here.
use_when:
  - Choosing the decorrelation family + agent composition for a review, on top of the bound review lane.
  - Composing a same-family review when a cross-family pass is unavailable, token-limited, or repo-blind.
  - Deciding whether a review may be downgraded toward same-family.
authority_boundary: retrieval_only
ratification_status: proposed_draft
revision: r1_post_same_family_review  # same-family arm of Version 1 ran on this doc; findings patched below
review_status:
  same_family_arm: complete (5-lens panel + completeness critic; findings adjudicated + patched into r1)
  cross_family_arm: pending (the residual the same-family panel cannot self-check — see §7)
  owner_acceptance: pending
ratification_gate: >
  Cross-family arm review of this revised doc + owner acceptance, THEN bind into
  .agents/workflow-overlay/ (review-lanes.md + artifact-roles.md) under the Doctrine Change
  Propagation Contract. Until then advisory only.
evidence_base:   # cross-project METHODOLOGY evidence; NOT orca artifact authority (per source-of-truth.md)
  - 2-week review-corpus mining (orca 111 + jb 97 = 208 outputs; single pass, this session)
  - cross-family head-to-head, n=1 (jb session b0711c1a, "Slice A"): no-repo cross-family 7/10 vs same-family 5-agent fan-out 6/10, union 10/10, cross-family cheaper
  - decorrelation principle (3 coverage axes) recorded in jb session ce0150c5
input_hashes:
  AGENTS.md: d5f688aa91412d105a60e907f9647c56cb4a59303e955058aa313665d88d1566
  .agents/workflow-overlay/source-of-truth.md: 6b9badd5243a4bcae7784c73c4eaf917807be9716f509c67cecd5576efa662f9
  .agents/workflow-overlay/artifact-roles.md: a111168d92cda73102276843b67a94f91b925a1c7c9ecc5f853aa16cca2654f8
  .agents/workflow-overlay/review-lanes.md: 0d2d4b6e_read_2026-06-08  # read this turn; re-pin exact sha at ratification
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 73383f2
stale_if:
  - A larger head-to-head (n>1) changes the catch-rate basis.
  - A larger corpus mining pass materially changes the yield rates or their ordering (n per tier is small).
  - Reviewer-attribution (reviewed_by) data shows a materially different current allocation.
  - Owner re-buckets artifact materiality.
  - The cross-family reviewer's access mode or token budget changes.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: routing_analysis_2wk_corpus + n1_head_to_head + decorrelation_principle + review-lanes.md
  edit_permission: docs-write
  target_scope: [docs/decisions/adversarial_review_routing_policy_v0.md]
  dirty_state_checked: yes  # overlay files modified in worktree; this record is additive, writes no overlay file
  blocked_if_missing: no
```

## Decision (proposed)

### 0. Core principle (and the bound that makes same-family OK sometimes)

Review **recall is a union problem**; misses come from **correlated coverage**. Coverage decorrelates along three axes (every observed miss mapped to one): **model-family**, **lens/role**, **vantage** (holistic vs decomposed).

Route to **maximize decorrelation per unit cost, weighted by `lock-in × finding-detectability`.** The principled bound (resolving §0-vs-Tier-B): family-decorrelation buys the most where a missed finding is **irreversible AND of a type same-family would share a blind spot on** (judgment/doctrine). Where a missed finding is **reversible and same-family-detectable** (test-guarded code), the marginal value of family-decorrelation is low, so same-family suffices. Same-family for Tier B is therefore a *derived consequence* of the principle, not an exception to it.

### 1. Decorrelation routing over the existing lanes

These tiers are **not new lanes** — they are a proposed decorrelation-routing layer *over* the lanes in `review-lanes.md` (artifact review, adversarial artifact review, code/impl review, delegated review-and-patch). A tier sets the **decorrelation family + agent composition** for whichever lane is bound.

**Tier is resolved from the reviewed artifact's bound `artifact_role` (artifact-roles.md) → tier map below.** Binding that role→tier map into the overlay is a ratification step (§8). Until then, tier selection is CA judgment, not an operable contract.

| Tier | Artifact class (by lock-in) | Decorrelation routing |
| --- | --- | --- |
| **A** | contracts, decisions, architecture, policy/doctrine, gating plans; **+ anything hitting the escalation triggers below** | cross-family **+** same-family (see §3) |
| **B** | code, implementation, fixture hygiene | same-family, 1–2 agents |
| **C** | post-patch / blast-radius rechecks / closure | light same-family (1 agent) |
| **none** | pure validation / execution / rerun reports | no adversarial review |

**Missing artifact classes (from completeness critic):** prompts/prompt-templates → Tier B unless they bind downstream agent behavior doctrinally → then A; research/synthesis → B; **fixtures-as-data that encode a claim/config consumed at runtime → A** (they carry hidden lock-in); runbooks → A if they bind agent behavior, else B.

**Escalation triggers (override the class default — UP only, never down):**
- **Security / credential / irreversibility:** any artifact touching a security boundary, secret handling, data-loss, or an irreversible side-effect (migration runner, data-write adapter, retention/deletion logic) → **Tier A regardless of being "code".** ("code = LOW" assumes reversible + test-guarded; these break that assumption.)
- **Recheck inherits its patch's tier:** a recheck of a Tier-A-class patch is **Tier A**, not C. Tier C is only for rechecks of Tier-B/none patches. (The "6/46 near-zero recheck yield" was measured on routine patches and does not license light review of high-lock-in rechecks.)
- **Hybrid / cross-tier artifact:** route to the **highest tier any component triggers**, and one agent must review the **cross-component interaction** (the seam neither single-section review covers).
- **Ambiguity → up-tier:** if the router cannot cleanly classify (mixed class, novel artifact, the triggers above plausibly apply), treat as ambiguous and **default up a tier**, flagging the ambiguity. Because cost pressure biases toward the cheaper tier, ambiguity is resolved conservatively by rule, not by the router's discretion.

**Guardrails:** fix compounding-minors regardless of tier (the *adjudicator* — not the same-family finding agent, which shares the D3 calibration blind spot — judges whether minors compound). **Conflict adjudication:** when cross-family and same-family disagree on severity, this is **CA adjudication** (per review-lanes.md, multi-review reconciliation is CA-owned); default to treating the higher-severity claim as live until resolved; for Tier A, an unresolved conflict **escalates to owner**, never auto-dismissed.

**Owner of the routing decision:** the CA / orchestrating thread proposes the tier; the **owner may override**; ambiguity is resolved up-tier-and-flag (above).

### 2. Same-family blind-spot directions (provisional, n=1 — a primary cross-family-arm target)

In the **one** measured head-to-head the same-family fan-out missed three direction classes the cross-family thread caught. **This is n=1** — treat the *list* as a hypothesis to confirm, not a settled taxonomy. As proposed, when same-family does the work these are explicitly cued:

- **D1 — Spec / closed-system integrity** (read the artifact's own tables/vocab against the authoritative source).
- **D2 — Implementation / runtime mechanics** (will it run: types, compile, case, order, exceptions, edge inputs).
- **D3 — Adversarial verdict calibration** (forbidden to be charitable; resist "proceed" drift).

Same-family native strengths (still cued): **D4** domain/product defensibility, **D5** contract/hook-fit/circularity (needs repo access), **D6** holistic internal-contradiction. Backstops: **B1** completeness/anti-correlation critic (loop until two empty passes), **B2** re-read-the-fix (review the *patched* artifact).

> **Known bias (flagged for the cross-family arm):** this D1–D6 split was authored by a same-family model (Opus) and *happens* to keep the high-influence directions (D4/D5/D6) with same-family while conceding only D1/D2/D3 to cross-family. No same-family reviewer (including the author) can reliably self-check this. **Validating or re-allocating D1–D6 is an explicit charge of the cross-family arm (§7).**

### 3. Tier-A composition — two cross-family configurations

"Cross-family" here means a **decorrelation-family property** (a reviewer of a different model family than the author), **not a named model/vendor** — the specific model stays an operator/tooling choice (see §9). Both versions follow the **`adversarial-artifact-review` registry template** for prompt structure, trigger `workflow-deep-thinking` then `workflow-adversarial-artifact-review`, return the compact `review_summary` YAML, and close with the review-use boundary (review-lanes.md).

#### Version 1 — cross-family pass, **NO repo access** (token-limited / paste-only)

**Cross-family reviewer owns** (its proven no-repo strengths, n=1): **D1** integrity (vs the *pasted* authoritative contract), the logic/correctness core, **D3** calibration, **D6** whole-artifact contradiction on the pasted content. **Blind here** (no repo): **D5** hook-fit, **D2** runtime mechanics in real code, **D4** fixture-vs-real-code.

**Same-family backfill is larger in V1 precisely because the cross-family arm is repo-blind** — these agents have repo access and own the repo-grounded directions:

| Agent | Direction |
| --- | --- |
| SF-1 | **D5** contract/hook-fit/circularity (trace real control flow) |
| SF-2 | **D2** implementation/runtime mechanics (read the actual code) |
| SF-3 | **D4** domain/product defensibility vs real fixtures |
| SF-4 | **D6** holistic (kept for family-axis decorrelation) |
| — | **B1** completeness critic; **B2** re-read-the-fix |

**Paste-bundle discipline:** send the artifact + its authoritative contract + minimal interface surface (so D1 works without the repo) — not the repo.

#### Version 2 — cross-family pass, **WITH repo access** (e.g. Codex-style)

Cross-family now also takes **D5/D2/D4 repo-grounded**. **Ordering rule:** task it to review the logic/spec **cold (D6) first**, *then* repo-grounded tracing, so repo access doesn't anchor away its fresh-eyes value. Same-family backfill shrinks to:

| Agent | Direction |
| --- | --- |
| SF-1 | **D4** deep product-domain defensibility (knowledge a generic reviewer lacks) |
| SF-2 | **D6** holistic (family-axis decorrelation — cross-family has its own blind spots) |
| — | **B1** completeness critic; **B2** re-read-the-fix |

**Never cross-family-only** even in V2 (n=1: cross-family alone hit 7/10; the union made 10/10).

### 4. Same-family-ONLY fallback (no cross-family at all) — an explicit, inferior stopgap

The family axis **cannot** be closed with same-family agents. Over-invest in lens + vantage + backstops, and **treat the result as provisional**: ~5–6 distinct-lens agents spanning D1–D6 (D1/D2/D3 non-negotiable) + B1 + B2. **This is deliberately the same headcount §6 calls "waste"** — it is acknowledged as expensive and lower-recall, accepted *only* because no cross-family pass is available. **For the highest-lock-in Tier-A artifacts, require one cross-family pass before ratification** — same-family-only is a stopgap, not an acceptance basis.

**Mid-flow cross-family unavailability** (timeout / malformed / cut off): hold the artifact at same-family-provisional and flag; do **not** silently downgrade to "done."

### 5. Decision rule — how many agents, which directions

- **One agent per distinct direction; zero redundant lenses** (a correlated same-family agent adds ~0 recall and costs tokens). Headcount is not the lever — **family + lens + vantage diversity is.**
- Spend budget on **cross-family diversity first**, then distinct same-family lenses, last (ideally never) on same-family headcount.
- Always include one holistic (D6) + B1 + B2.
- Tier B: 1–2 agents (correctness + runtime/edge). Tier C: 1 light agent.

### 6. Cost / latency

- n=1: **one cross-family thread ≈ a 5-agent same-family fan-out on the core, cheaper** (fan-out ≈465k tokens; single fan-out, may itself have been suboptimal — treat as directional).
- The clear, low-risk savings: keep Tier B (code) and Tier C (rechecks) on cheap same-family; **the "1 cross-family + 1 same-family + B1 + B2" collapse is the Version-2 (repo-access) shape** — Version 1 keeps more same-family agents *because* the cross-family arm is repo-blind, not as waste.
- No latency SLA is set here; Tier-A reviews block ratification, so the owner sets a max review-cycle time at ratification to prevent indefinite deferral.

### 7. Validity / limits (read before trusting this)

- **Cross-family catch-rate basis is n=1** (Slice A). Do **not** treat "union = complete" as proven; B1 + B2 are the standing backstops because of this. Whether union=10/10 repeats is an open question for the cross-family arm.
- **Yield rates are basis-sensitive.** A recompute put the tiers near **HIGH ≈38% / MED ≈45% / LOW ≈46%** (vs the first pass's 32/47/51), the ordering **inverts in the orca-only subset**, and n per tier is small. The robust claim is only **qualitative: high-lock-in is *not* higher-yield than code (often lower) — so yield is not the routing key.** The precise rates and the LOW>MED>HIGH ordering are **not** robust.
- Recheck near-zero yield is **6/46 (~13%)**, measured on routine patches only (does not cover Tier-A-class rechecks — see §1 escalation).
- **Operability is pending:** the tier map, the panel composition, the `reviewed_by` field, and B1/B2 have **no overlay hook yet** — they bind into `review-lanes.md` / `artifact-roles.md` at ratification (§8). As written this is advisory, not executable from orca sources alone.
- **Materiality bucketing is a lock-in rubric** (code = LOW because reversible/test-guarded, not low-stakes) — contestable; the §1 escalation triggers are the pressure-relief.
- **Author / same-family bias** (see §2 box) — the cross-family arm's first job.
- Evidence base is **cross-project methodology** (jb sessions), explicitly **not** orca artifact authority.

### 8. Ratification — what binds where (Doctrine Change Propagation Contract)

On owner acceptance, propagate (DCP receipt required):
- **`review-lanes.md`** — add the decorrelation-routing layer (tiers as family+composition over existing lanes) **and** the model-neutrality amendment in §9.
- **`artifact-roles.md`** — add the `artifact_role → tier` map and the canonical `reviewed_by` field (shape below) to the Review report role.
- Companion low-risk changes that stand alone (no full ratification needed): record `reviewed_by`; formalize the Tier-C recheck downgrade with the §1 escalation guard.

`reviewed_by` canonical shape (proposed): `reviewed_by: { family: cross|same, access: repo|no_repo, lane: <review-lane>, composition: <vN or fallback> }` — model/vendor name optional and operator-owned, never required by the lane.

### 9. Reconciliation with review-lanes.md model-neutrality (owner decision)

`review-lanes.md` (line ~98) forbids review-lane routing from prescribing/implying **runtime model choice**. Per owner direction ("route to cross-family"), this policy introduces **decorrelation FAMILY (cross-family vs same-family, relative to the author)** as a review-routing property — distinct from naming a specific runtime model/vendor, which **remains an operator/tooling choice** (the policy never says "run on GPT-5.5"; it says "a different family than the author"). This is a **proposed amendment** to the model-neutrality rule and must be propagated into `review-lanes.md` at ratification, not assumed in force. Prompt-template target (`adversarial-artifact-review`) binding is already permitted by review-lanes.md and is used as posture only.
