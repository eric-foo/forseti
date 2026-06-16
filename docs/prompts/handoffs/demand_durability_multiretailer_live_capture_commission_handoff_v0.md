# COMMISSION — Live-Capture the Demand-Durability Multi-Retailer Series (Amazon recon + Sephora/Ulta verification)

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane commission handoff (build commission; what-to-do, not a build)
scope: >
  Commissions a fresh Orca capture-spine executor lane to run the LIVE half of the demand-durability
  multi-retailer rendered capture: Amazon recon (GO/PARTIAL/NO-GO), bounded live Sephora + Ulta
  verification through the cadence runner via the merged rendered writer, and a per-retailer recon
  verdicts + measured-ToS posture doc. The wiring (rendered writer + `--writer`/`--writer-arg`) is
  already built; this lane proves it live within the source-access boundary.
authority_boundary: retrieval_only
use_when:
  - Spinning up the live-capture follow-on after PR #146 (the rendered-capture wiring) merges.
  - Checking the scope, preconditions, forks, and landing rules for that lane.
open_next:
  - docs/product/data_capture_spine/demand_durability_multi_retailer_rendered_capture_spec_v0.md   # the binding spec
  - docs/product/source_capture_toolbox/source_capture_playbook_v0.md                              # USE to assess Amazon
  - docs/product/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md         # anti-block ladder
  - docs/product/source_capture_toolbox/capture_recon_index_v0.md                                  # recon state
  - orca-harness/runners/run_source_capture_durability_series.py                                   # the cadence runner (--writer / --writer-arg)
  - orca-harness/runners/run_source_capture_cloakbrowser_packet.py                                 # the rendered writer
  - docs/product/data_capture_spine/data_capture_source_access_boundary_decision_v0.md             # the boundary
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md     # Ob.6 fidelity, Ob.17 durability
stale_if:
  - PR #146 changes the rendered writer's interface or the runner's --writer/--writer-arg wiring.
  - The source-access boundary decision changes hard stops or the measured-ToS posture.
  - A retailer's recon verdict lands or changes.
```

You are a fresh **Orca capture-spine executor lane**. You are commissioned to run the **LIVE half** of the demand-durability multi-retailer rendered capture. Owner-authorized 2026-06-15; **landing to `main` stays owner-gated**. This is a build commission, not a discussion.

## Start preflight + source-loading (do this first)
- Read `AGENTS.md` + `.agents/workflow-overlay/README.md`, then follow the overlay (source-loading, dev-workflow per-lane PR, safety-rules). Record the `orca_start_preflight` receipt.
- Repo: `C:\Users\vmon7\Desktop\projects\orca`. Isolation: a **fresh worktree/branch off latest `origin/main`** (`git fetch origin main` first). **Windows long-path note:** use a SHORT worktree base path (e.g. `C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-<short>-wt`) and `git config core.longpaths true` — a deep `.claude/worktrees/<long-name>/` base overflows `MAX_PATH` on this repo's long capture-fixture paths.
- Edit permission: **bounded build for this commission only** (live capture + a verdicts doc + any small capture-glue code), within the source-access boundary + no-gate-defeat (see Authorization). Output: capture packets + a verdicts doc + (if any code) a per-lane PR.
- **Source-gated method contract:** `REFERENCE-LOAD` the capture **playbook** + anti-block **ladder** as procedural guidance — do **not** `APPLY` them yet. Then `SOURCE-LOAD` the spec + recon index + the merged wiring and declare `SOURCE_CONTEXT_READY` (or `SOURCE_CONTEXT_INCOMPLETE` with the gap) before any assessment, verdict, or capture.

## PRECONDITION — confirm the wiring is on `origin/main` FIRST (confirm-don't-trust)
This lane **consumes the merged rendered-capture wiring**: the cadence runner's `run-slot --writer cloakbrowser` selector + the `--writer-arg` capture-knob passthrough, and the rendered writer's Ob.17 durability flags. That wiring is **PR #146** (branch `rendered-multiretailer-capture-v0`). **Confirm `run-slot --writer cloakbrowser` exists on `origin/main`** (`git cat-file`/`--help` on the runner) before building; **if absent, the owner must merge #146 before you start** (mirror the #136 gate). Do not re-implement the wiring — consume it.

## Read the binding spec FIRST (what-must-be-true)
`docs/product/data_capture_spine/demand_durability_multi_retailer_rendered_capture_spec_v0.md` (on `origin/main` via #136). Then follow its `open_next`. The spec's acceptance signal governs: *each authorized retailer produces a valid durability-series observation packet (Ob.17 fields set) via the rendered path, invoked by the cadence runner through the writer seam, with the per-retailer ToS posture + recon verdict recorded; gap≠no-change honored; no gate defeated; one-series-per-retailer shape.*

## Recon state you inherit (do NOT re-probe Sephora/Ulta substrate)
- **Sephora = GO** — Bazaarvoice reviews are first-party-rendered, lazy-loaded on **progressive scroll**; the cloak adapter passes the bot wall legitimately. Capture via `--writer cloakbrowser --writer-arg=--scroll-step-px=350` (and a settle if needed). Recon already on `main`.
- **Ulta = GO** — price/availability live in `__APOLLO_STATE__` embedded-JSON in the rendered DOM; default rendered capture (`--writer cloakbrowser`, no scroll needed) preserves it. (The Ulta demand-*projection* worktree is a separate downstream lane — **do NOT merge it**; consume the substrate diagnosis only. INV-1.)
- **Amazon = the ONLY un-assessed retailer.**

## The commission (what to settle live)
1. **Amazon recon.** Run the playbook's anti-block **ladder** against an Amazon PDP (probe-then-pin; **escalate-and-re-probe before recording NO-GO**; **STOP at any auth / CAPTCHA / Cloudflare *challenge*** — never defeat a gate). Author an honest **GO / PARTIAL / NO-GO** verdict (NO-GO is a first-class, successful diagnosis). Amazon's ToS is the most restrictive on automation — record the measured pre-commercial posture explicitly (commercial scale routes through a provider, not Orca's own path). **PAUSE at Amazon NO-GO** (owner fork).
2. **Live verification — Sephora + Ulta.** Bounded **single-SKU** live captures through the cadence runner via the rendered writer, each producing a **valid Ob.17 durability-series observation packet** (the acceptance signal). Use `run-slot --writer cloakbrowser` (+ `--writer-arg=--scroll-step-px=…` for Sephora). **One series PER retailer** — each retailer its own `series_id` + its own US-storefront pins (locale/currency/variant); the same SKU across retailers is **parallel per-retailer series compared downstream**, never one `series_id` spanning retailers.
3. **Per-retailer verdicts + measured-ToS posture doc.** Record Sephora=GO, Ulta=GO, Amazon=<verdict>, each with its measured-ToS posture, storefront/locale pins (**US storefront** — owner has no preference → US default), the rendered method used, and honest limitations. INV-1: observed facts + limits only — **no demand verdict, no scoring, no durable-vs-hollow judgment.**

## Bounded build authorization (owner, 2026-06-15)
You are authorized to run **bounded, measured, public live captures** (Sephora/Ulta verification + Amazon recon) and author the verdicts doc, within the source-access boundary + no-gate-defeat, **without re-requesting per-turn authorization**, **bounded to this commission only** (not broader capture-spine work). The **CloakBrowser runtime is installed locally** (`cloakbrowser 0.3.31`, Chromium cached) — the named prerequisite is met. Landing to `main` stays owner-gated.

## Hard constraints
- **Source-access boundary + NO-GATE-DEFEAT:** anti-bot OK; **STOP at any auth / CAPTCHA / Cloudflare *challenge*** — record the limitation, escalate-and-re-probe per the ladder before NO-GO, **never defeat a gate**.
- **Bounded/measured volume** — no industrial scraping; commissioned-series volume only (single SKU per retailer for this verification).
- **INV-1** — capture records observed facts + limits only; **no demand verdict, no scoring**.
- **Additive** — consume the merged wiring; **no schema change, no `SOURCE_CAPTURE_MANIFEST_VERSION` bump, no change to the runner's state model.** A retailer the rendered path cannot reach is recorded as an **un-observed gap, never a fake success** (the runner now enforces packet-existence + access-failed → gap).
- **One generic rendered writer** (already merged) — do **not** add per-retailer adapters.

## PAUSE and report at any owner-decision fork
- Amazon **NO-GO** (report the honest diagnosis + what was tried).
- A **proxy / geo** need (proxy is **gated**, not a default `--writer-arg` knob — it is an owner decision, not a per-slot knob).
- A **source-access tooling tranche** needing owner authorization.
- A storefront/locale ambiguity beyond the US default.

## Landing
Fresh worktree/branch off latest `origin/main`; if any code is written, run the offline suite green (`orca-harness/.venv/Scripts/python.exe -m pytest`); per-lane PR via `gh pr create --base main`; **explicit push** `git push -u origin <lane>` (never a bare push). **Do NOT self-merge.** Capture packets are bounded series artifacts; the verdicts doc lands under `docs/` (or `docs/product/data_capture_spine/`).

## Closeout
**End with review-handoff facts: branch, HEAD, PR number (if any), changed files, captured packet locations, and the three per-retailer verdicts.** Then **recommend a delegated CROSS-VENDOR review** (`workflow-delegated-review-patch`) of any new capture code.

## Non-claims
Not validation, not readiness, not commercial-scale capture, not a demand verdict, not ECR/Cleaning/Judgment. The rendered-capture wiring's correctness is PR #146's concern (already reviewed cross-vendor); this lane proves the live path within the boundary.
