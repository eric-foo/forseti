# Demand-Durability Spec Set — No-Repo Cross-Vendor Adversarial Artifact Review (Bundle README)

> **You are the reviewer. This README is your complete instruction set.** You do
> not have repo, skill, or overlay access. Everything you need is in this bundle:
> the five review targets (attached, verbatim), the authority excerpts the
> targets must conform to, and the portable review method to follow. Follow the
> **PORTABLE METHOD** block near the end of this file.

## 1. Commission (what this review is)

- **Review type:** read-only, **advisory-only** adversarial artifact review of a
  set of five design+spec documents (no code). The formal review tooling used
  inside the authoring environment is **not available to you** — say so in your
  output; it bounds your result to advisory critique, not a formal verdict.
- **De-correlation:** this is the **cross-vendor (discovery) bar**. The artifacts
  were authored by **Claude / Anthropic (claude-opus-4.8)**. You must be a
  **different vendor** (e.g., an OpenAI/GPT model). The cross-vendor property is
  satisfied by the operator's model choice, not by anything you do. Do **not**
  name, recommend, or rank any runtime model in your output.
- **Purpose:** find material, decision-relevant failure modes across the set
  **before any of it is built**. Be maximally adversarial within the targets'
  stated purpose; do not retarget or widen beyond the five named targets.

## 2. Targets (attached verbatim; review in this order)

Review the **envelope-delta first** — the four proxy profiles forward-cite it.

| # | File | What it is | Its own contract (must hold) |
|---|------|------------|------------------------------|
| 01 | `01_capture_envelope_durability_delta_spec_v0.md` | **Envelope DELTA** — names the durability-over-time capture facts + temporal-regime/cold-start doctrine the 4 proxies consume. | A **delta on the existing Capture Envelope of record**, NOT a new/second envelope. Must **cite** `models.py SourceCapturePacket` + the obligation contract as the sole envelope authority and not re-derive/fork them. Specs only the 5 new elements (pinning facts, cold-start marker, series-diff, cadence model, three temporal regimes + cold-start-as-inherent-limit cap). |
| 02 | `02_demand_proxy_price_timeseries_capture_profile_v0.md` | Price time-series proxy. | Captures list / effective-sale / promo-mechanism as **separate fields** (no derived "discount"); cites-and-extends `price_payload_extraction.py`, does not re-spec it. INV-1: no scoring. |
| 03 | `03_demand_proxy_availability_restock_capture_profile_v0.md` | Availability / restock proxy. | In-stock/out-of-stock/waitlist + restock signals at variant granularity, under a **flag-don't-conclude** discipline (never classifies scarcity-theater at capture time). INV-1: no scoring. |
| 04 | `04_demand_proxy_search_interest_capture_profile_v0.md` | Search-interest proxy. | **Conditional on sourcing** (AR-04 unsourced gap): a capture obligation that becomes binding only if a sourcing authorization is accepted; must not present search-interest as available. INV-1: no scoring. |
| 05 | `05_demand_proxy_review_velocity_corpus_capture_profile_v0.md` | Review velocity / corpus proxy. | **Conditional on sourcing** (AR-04). Records arrival-cadence history + **farm-detection observables + a flag**, never a credibility/astroturf verdict (that is downstream Judgment). INV-1: no scoring. |

Each attachment carries a `## What This Is (And Is Not)` / deconfliction header
stating its own boundaries; treat those as the target's self-declared contract
and attack whether the body actually holds to it.

## 3. Review focus (the decision-relevant failure modes to attack)

Attack at least these across the set, in addition to the generic checks in the
PORTABLE METHOD block:

1. **INV-1 preservation.** Any element that weights, scores, ranks, combines, or
   judges a captured fact — or smuggles a "durable vs hollow" / credibility /
   astroturf verdict into *capture* — is an INV-1 violation. Capture must stay
   **observed facts and their limits** only. (The series-diff may *detect*
   observed change; it must not *classify* tamper/astroturf/distortion.)
2. **No second-envelope drift.** The delta (01) must cite the envelope of record
   and not re-mint it. Flag any place a proxy (02–05) **re-derives** envelope
   basics (timing, locator, capture mode, content hash, recapture relationship,
   posture vocabularies) instead of citing them.
3. **Cross-set internal consistency.** The three temporal regimes, the
   cold-start marker, the series-diff (Element 3), and the cadence model
   (Element 4) must be referenced coherently and identically by all four
   proxies. Flag any proxy that contradicts the delta's definitions or uses a
   term the delta does not define.
4. **Conditional-on-sourcing scoping.** 04 and 05 must be clearly **conditional**
   (AR-04). Flag any language that treats search-interest or review data as
   already sourced/available, or that would let a downstream reader assume a
   binding obligation.
5. **Deconfliction integrity.** Each proxy must **cite-and-extend**, not
   duplicate, the delta and the existing capture surfaces
   (`price_payload_extraction.py`, the EDGAR/org-motion lane). Flag duplication
   or a forked authority.
6. **Cold-start as inherent-limit cap.** The delta frames the pre-coverage
   window as a **permanent ceiling** (except retroactive-native recovery bounded
   by the source's own history), not a clearable risk. Flag any proxy that
   implies "capture more and the gap closes" for a forward-only source.

## 4. Fitness reference (alignment axis — also attack it)

These are intent-bearing targets. Anchor your decision criteria to this
`fitness_reference`, and **also attack whether the reference itself is right**
(never treat it as a pass-if-matches bar):

- **Goal:** give Orca's beauty-vertical demand-read a *trustworthy
  durability-over-time substrate* — capture that does not silently lie about
  comparability, coverage, tampering, or sampling gaps — **without** capture ever
  scoring or judging demand (that is downstream Judgment).
- **Observable success signal:** a downstream Judgment/ECR consumer can read,
  from the captured series alone, (a) whether two observations are comparable,
  (b) where coverage begins and what is inherently uncoverable, (c) whether a
  value/item changed/was deleted across the series and on what evidence, and
  (d) how regularly the series was sampled and where the gaps are — each as an
  observed fact with its limit, never as a verdict.

If you judge no checkable success bar is actually bound by the targets, name
`no checkable success bar bound` as a finding rather than inventing one.

## 5. Authority excerpts (the binding rules the targets must conform to)

### 5a. Authoring-environment kernel (Orca `AGENTS.md` — foundational behavior + scope discipline)

> **Agent Behavior Kernel.** Surface ambiguity or risky assumptions before
> acting. Default to the smallest complete intervention: solve the actual request
> completely with the narrowest sufficient scope. Every changed line must trace to
> the user request or required validation. Preserve real failure visibility; never
> create fake success paths. For non-trivial changes, define and run relevant
> verification or state why it was not run. … Report only observed facts.
>
> **Smallest Complete Intervention.** `Complete` is load-bearing — do not underfix
> to minimize diff. `Smallest` is also load-bearing — do not add unrelated
> cleanup, speculative abstractions, broad rewrites, extra workflow ceremony, or
> nice-to-have improvements. Prefer the path with materially lower downstream
> lock-in among already-complete paths; never use this to authorize speculative
> cleanup or future-proofing.

Conformance to this kernel is part of the review: attack the targets for **scope
inflation** (specs that do more than "name the durability capture facts + the
doctrine the proxies consume" — e.g., backdoor schema/contract changes, runtime
or scheduler design, ECR/Cleaning/Judgment design) and for **underfix** (a
durability gap left incomplete such that the series can still silently lie).

### 5b. INV-1 — the demand-substrate no-scoring invariant (from target 01, §"INV-1 Preservation")

> This delta is bound by INV-1 (the Demand-Substrate no-scoring invariant).
> Concretely: every new element describes **what is captured** (a fact) or **how
> capture should sample/classify** (doctrine) — never how to weight, score, rank,
> combine, or judge it; no formula, threshold, weight, or numeric scoring rule
> appears; the series-diff detects observed change, it does **not** classify
> tamper/astroturf/distortion (Signal Integrity is Judgment's); the temporal
> regimes and cold-start cap classify *coverage*, not *demand durability* —
> "durable versus hollow" is a downstream Judgment read.

### 5c. Envelope of record — cited, not re-derived (from target 01, §"Envelope Of Record")

> The Capture Envelope of record ALREADY EXISTS and is the **sole** Capture
> Envelope authority: (1) the shipped Source Capture packet schema
> `orca-harness/source_capture/models.py` (`SourceCapturePacket`,
> `SourceCaptureSlice`, `PacketTiming`, `PreservedFile.sha256` + `hash_basis`,
> `re_capture_relationship`, the closed access/archive/media/cutoff posture
> vocabularies as `VisibleFact`, `limitations`); and (2) the obligation contract
> (Ob.3, Ob.4, Ob.6, Ob.8–Ob.11, Ob.15; its discharge vocabulary reused as-is).
> **Conflict rule:** if a target conflicts with the schema or the obligation
> contract, the envelope of record wins — treat the target as stale. Envelope
> basics (timestamp, locator, capture method/mode, retained raw payload, content
> hash, per-capture recapture relationship, posture vocabularies, limitations)
> are **already covered** and must not be re-spec'd; any restatement must be a
> citation, not a new authority.

### 5d. Two-bar de-correlation (Orca `review-lanes.md`, Review Doctrine)

> **Two-bar de-correlation (review tier; family = vendor).** A **cross-vendor**
> delegate (different vendor / model lineage, e.g., Claude ↔ GPT; vendor =
> upstream developer/provider, not host / reseller / wrapper) is the
> **discovery** bar, required to claim the no-new-seam standard for a full or
> doctrine-surface pass. A **same-vendor** delegate is the bounded sanity /
> verification tier (advisory). This review is commissioned at the **cross-vendor
> discovery** bar (`de_correlation_bar: cross_vendor_discovery`).

## 6. PORTABLE METHOD — follow this exactly (paste-equivalent, verbatim)

*Provenance: a faithful, flattened distillation of the Orca adversarial-artifact-review
template + the Review Doctrine in `review-lanes.md`, made self-contained for
reviewers without skill/overlay/repo access. Freshness gate result for this
bundle is recorded in `MANIFEST.md`.*

### 1. Your stance
You are performing a **read-only, advisory-only adversarial artifact review**. The formal review tooling used inside the authoring environment is **not available to you** — state that explicitly in your output, because it bounds your result to advisory critique, not a formal verdict. Within the commission-bound target and purpose, be **maximally adversarial** about material, decision-relevant failure modes; do not soften a real failure mode because remediation would be hard. Do not retarget or widen beyond the named target.

### 2. Target & source-readiness
Review only the material provided to you. If the target carries a content hash, confirm the provided copy matches it and say so; if you cannot confirm, proceed advisory-only and say so. If any claim depends on a source not provided to you, label it `unverifiable from provided sources` rather than assuming. Treat any pasted authority excerpts as the binding rules the target must conform to.

### 3. Method (order matters)
First do a structured reasoning pass: enumerate the target's load-bearing claims, the boundary/decision criteria, and the likely failure modes — **before** listing any finding. Then produce findings. Reasoning-before-findings is required; it frames what to attack.

### 4. Review checks (be maximally adversarial)
- **Authority / hierarchy conformance:** does the target conflict with the provided authority rules, or violate their precedence?
- **Internal consistency:** self-contradiction; sections that undercut each other.
- **Missing required inputs or unbound roles / intent.**
- **Output-mode / destination / interface correctness.**
- **Downstream executability:** can the named next actor actually act on this from the stated sources?
- **Fitness to goal** (intent-bearing targets): does it achieve its stated goal + success signal? **Attack whether the goal and signal are themselves right** — never treat the fitness reference as a pass-if-matches bar. If no checkable success bar is provided, name `no checkable success bar bound` as a finding rather than inventing one.
- **Overclaims:** readiness, validation, approval, or proof claims unsupported by evidence.
- **Leakage** of out-of-scope or unrelated-project policy into the target.
- **Scope discipline:** does the target do *more* than its stated purpose requires (scope inflation, speculative additions, unrequested scope) — or *less* than required (underfix, symptom-only)? Flag both overreach and underfix against the target's actual purpose.

### 5. Severity meaning
Use `critical` / `major` / `minor` as **finding-priority labels only**. They carry no approval, rejection, readiness, validation, or mandatory-remediation authority.

### 6. Output contract
Lead with a compact `review_summary`, then findings:

    review_summary:
      status: review_complete | blocked
      recommendation: <one line; advisory>
      findings_count: <int>
      blocking_findings: []      # the critical/major ones, one line each
      advisory_findings: []      # minor / optional, one line each
      summary: <one line>

Then list findings, ordered `critical` → `major` → `minor`. For each include: `severity`, `location` (which attachment + section), `issue`, `evidence` (cite the target section **and** the conflicting authority excerpt), `impact`, `minimum_closure_condition` (the end state that resolves it — not how to implement), `next_authorized_action` (e.g. owner decision / rerun / re-allocate / no action), and an advisory remediation direction. Do **not** emit executor-ready patch steps. If you find no issues, say so and list residual risks / test gaps.

### 7. Review-use boundary
Your findings are **decision input only** for the commissioning owner — not approval, validation, readiness, product proof, mandatory remediation, or executor-ready instructions. Nothing downstream is bound by this review unless a separate authorized decision accepts it.

## PORTABLE METHOD — end marker

## 7. How to return your review

Return your `review_summary` + findings in chat (the operator couriers it back).
You do not write any files. The operator/Chief Architect will record provenance
(`reviewed_by` = your model+version; `authored_by` = claude-opus-4.8) and
adjudicate every finding before anything is kept — your findings are claims to
adjudicate, not changes to apply.
