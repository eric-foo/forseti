# Quora B2B Answer-Strategy Pilot v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record — Quora B2B answer-strategy pilot (demand-signal content drafts; not capture, buyer proof, or approved final angle)
scope: >
  First Quora B2B answer-strategy pilot drafted from the PR #825 post-merge
  capture calibration record. Names three admissible candidate surfaces and
  gives one answer-strategy unit for each (source row, evidence boundary,
  searcher intent, answer angle, safe claims, claims to avoid, draft/outline).
use_when:
  - Drafting or extending Quora B2B answer-strategy content from the calibration record.
  - Checking which Quora B2B candidate surfaces have been turned into answer angles and under what evidence boundary.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/quora_b2b_postmerge_capture_calibration_delegated_adversarial_review_patch_v0.md
branch_or_commit: 1a1f3007cd55a6caa2b87c7bc25d6c2344b0d9f7
input_hashes:
  - path: docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md
    sha256: 80399574C4FED31B3D0732509FC580605171CE5C314787BA318DFBA393CD5B6F
stale_if:
  - The calibration record's candidate table is superseded, corrected, or re-run with a different candidate set.
  - The Quora capture is re-run and produces a different admissible candidate set.
```

## Status

`ANSWER_STRATEGY_PILOT_DRAFT`

This is a small answer-strategy content pilot and owner decision input. It is not
a capture run, not a code change, not buyer proof, not market proof, not
source-quality proof, and not an approved final content angle. The final content
angle is owner / Chief Architect owned; this pilot proposes drafts under the
recommended default and preserves the evidence boundary.

## Provenance

- Originating handoff: `docs/workflows/quora_b2b_answer_strategy_pilot_handoff_v0.md`
  — authored by the Codex GPT-5 lane on branch `codex/quora-playbook-handoff`
  (commit `f0cd3387`). That branch is **not merged to `main`**, so the handoff
  packet is not present on this lane's base; it is recorded here as provenance,
  not as an on-`main` pointer. This pilot re-derives its facts from the two
  on-`main` sources named in `open_next`, not from the packet's paraphrase.
- Lane base: `main` at `1a1f3007` (HEAD of this worktree; matches the handoff's
  `expected_head_at_lane_start`).
- Load contract executed (confirm-don't-trust): the calibration record
  (`80399574…CD5B6F`) and the delegated adversarial review
  (`C28566AA…A9A13E`) were re-opened and their working-tree SHA256 matched the
  handoff's recorded hashes exactly; both are byte-identical across HEAD /
  `origin/main` / the codex branch (the post-patch versions with F1–F4 applied).
- Known load-contract delta (surfaced, not silently accepted): the capture
  playbook and recon index on `main` do **not** match the handoff's recorded
  hashes. The handoff's "success-means-details" playbook/recon absorption lives
  only on the unmerged codex branch. That delta is capture-method doctrine, not
  an input to this answer-strategy pilot, and the load-bearing evidence-boundary
  facts it would carry are independently stated in the calibration record's
  Enforcement Placement table (row 1: "success means details, not 200"). It does
  not block this pilot; it is flagged so a future lane does not assume the
  playbook on `main` already carries that rule.

## Evidence Boundary (applies to every unit below)

- **Source is one bounded capture.** All candidate surfaces come from a single
  post-merge Quora B2B search capture recorded in
  `docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md` (packet
  `01KX3XAS9T04NG7GE9FCN546YK`, local ignored profile, no proxy, caller-bound
  detail sufficiency passed). It proves that specific capture at that time. It
  does not prove Quora access is reliable, session-durable, or repeatable.
- **Candidate rows are demand signal, not buyer proof.** "People ask this on
  Quora B2B search results" is a signal that the question surface exists and has
  search demand. It is not evidence that Orca's buyers care, that the market is
  validated, or that any answer converts.
- **Labels are paraphrases; drafts are original composition.** The calibration
  record's candidate labels are concise paraphrases tied to packet line numbers.
  This pilot did **not** re-open the local packet, and the answer drafts below
  are original composition built from standard B2B practice — they do **not**
  quote Quora text and must not be presented as Quora quotations. If exact
  wording is ever needed, open the local packet named in the calibration record;
  do not reconstruct Quora wording from these paraphrases.
- **"Answer snippet includes X"** means the captured Quora result row showed a
  snippet touching theme X. It is corroboration that the surface has real
  discussion; it is not an authority citation and is not reproduced here.

## Candidate Selection

Selected the handoff's **recommended default**: three high-signal
business-operator angles that each have a visible answer snippet in the
calibration record (so the searcher-intent read is grounded, not invented).

| # | Packet lines | Candidate surface (paraphrase) | Calibration row |
| --- | --- | --- | --- |
| A | 30, 37 | B2B customer-discovery questions; snippet touches success measurement, money impact, daily-workflow fit. | row `30, 37` |
| B | 59, 66 | First B2B SaaS sales-hire questions; snippet touches product understanding and outbound cadence. | row `59, 66` |
| C | 113, 120 | Pricing a SaaS B2B offering; snippet ties price to productivity gain and value. | row `113, 120` |

**Available one-swap alternate (owner call, not taken here):** swap unit C for the
marketplace/product-validation seed at packet lines `210, 215` (validating a B2B
marketplace idea; snippet recommends feedback from existing customers, including
negative experiences) if the owner prefers product-validation over monetization
focus. Both clusters are admissible; the pilot was kept small (three units) per
the handoff's Drift Guard — do not widen without owner ask.

---

## Unit A — B2B Customer-Discovery Questions

- **Source row:** calibration record `30, 37` — "B2B customer-discovery
  questions; answer snippet includes success measurement, money impact, and
  daily-workflow fit."
- **Evidence boundary:** demand signal for "what should I ask B2B customers"
  content; snippet corroborates that success-measurement / cost / workflow-fit
  are live themes. Not buyer proof; draft is original composition.
- **Likely searcher intent:** a founder, PM, or early operator who has already
  decided to do customer discovery and now wants a concrete, sequenced question
  set — "what exactly do I ask a B2B customer so I learn something real, not a
  polite yes."
- **Recommended answer angle:** give a short, behavior-first discovery script
  organized by what each question reveals, and warn against leading/hypothetical
  questions. Anchor on the three themes the snippet surfaced: how they measure
  success today, what the problem costs them, and where it shows up in the daily
  workflow.
- **Key claims safe to make:** behavior-over-opinion and "ask about the past,
  not the hypothetical future" are standard, defensible discovery practice
  (Jobs-to-be-Done / *The Mom Test* lineage); quantifying cost-of-problem and
  current success metrics is routine B2B discovery.
- **Claims to avoid:** do not imply these came from Orca's own customers; no
  buyer-proof or market-validation language; do not cite Quora as an authority
  or quote its snippet; no promise that this script "validates" an idea by
  itself.
- **Draft / outline:**
  > **The 3 questions that make B2B discovery calls actually useful**
  >
  > Most discovery calls fail because they ask about the future ("would you use
  > this?") instead of the past ("what did you do last time?"). Fix that with
  > three clusters:
  >
  > 1. **Success, measured.** "How do you measure success on this today? What
  >    number would move if it worked?" — forces a concrete metric instead of a
  >    vibe.
  > 2. **Cost of the problem.** "Walk me through the last time this went wrong —
  >    what did it cost in time or money?" — separates a real, funded pain from a
  >    mild annoyance.
  > 3. **Workflow fit.** "Show me where this lives in your week — which tool,
  >    which handoff, who else touches it?" — reveals whether a fix has to fit an
  >    existing workflow or replace one.
  >
  > Rule of thumb: if the customer is describing something they *already did*,
  > you're learning. If they're speculating about what they *might* do, you're
  > being flattered. (Close with a light, non-promotional pointer to how Orca
  > thinks about this, only if genuinely relevant.)

## Unit B — First B2B SaaS Sales-Hire Questions

- **Source row:** calibration record `59, 66` — "First B2B SaaS sales-hire
  questions; answer snippet includes product understanding and outbound
  cadence."
- **Evidence boundary:** demand signal for "how do I hire my first B2B SaaS
  salesperson" content; snippet corroborates product-understanding and
  outbound-cadence as themes. Not buyer proof; draft is original composition.
- **Likely searcher intent:** a founder about to make a first, high-stakes,
  hard-to-reverse sales hire with no existing playbook or inbound flow — wants
  interview questions and evaluation criteria to avoid picking the wrong profile.
- **Recommended answer angle:** frame the first sales hire as a *builder*, not a
  *closer who needs warm leads*, and give interview probes for the two themes the
  snippet surfaced — can they learn the product deeply enough to sell technical
  value, and do they have the self-directed outbound discipline to create
  pipeline from zero.
- **Key claims safe to make:** the "first sales hire must be a builder /
  founder-adjacent seller, not a coin-operated closer" view is widely held B2B
  SaaS guidance; product fluency and outbound cadence are legitimate,
  commonly-cited evaluation axes for an early-stage seller.
- **Claims to avoid:** no claim about Orca's own hiring; no buyer proof; no
  guaranteed hiring outcome; do not quote Quora; do not present opinion as
  settled fact — label it as a defensible default, not a law.
- **Draft / outline:**
  > **Your first B2B SaaS sales hire is a builder, not a closer**
  >
  > A closer who needs warm inbound will starve at a startup that has none. Your
  > first hire has to *manufacture* pipeline and *learn* a technical product.
  > Interview for both:
  >
  > - **Product understanding:** "Here's our product for 10 minutes — now sell it
  >    back to me and tell me who it's *not* for." Tests whether they can hold
  >    technical value and qualify, not just pitch.
  > - **Outbound cadence:** "Describe your last 2 weeks of outbound: how many
  >    touches, which channels, what you changed when it wasn't working." Tests
  >    self-directed prospecting discipline with no manager and no leads handed to
  >    them.
  > - **Ambiguity tolerance:** "Tell me about a time the playbook didn't exist and
  >    you wrote it." First hires build the motion; they don't inherit it.
  >
  > Score the builder signals higher than raw logo pedigree; a great Nth-hire
  > closer is often the wrong first hire.

## Unit C — Pricing a SaaS B2B Offering

- **Source row:** calibration record `113, 120` — "Pricing a SaaS B2B offering;
  answer snippet ties price to productivity gain and value."
- **Evidence boundary:** demand signal for "how do I price my B2B SaaS" content;
  snippet corroborates the price-to-value / productivity-gain framing. Not buyer
  proof; draft is original composition.
- **Likely searcher intent:** a founder or PM setting or revising B2B SaaS
  pricing, usually stuck between cost-plus, competitor-matching, and "charge what
  it's worth" — wants a method to decide the number, not a single magic price.
- **Recommended answer angle:** teach value-based pricing anchored to the
  buyer's economic/productivity gain (the theme the snippet surfaced): quantify
  the gain, capture a defensible fraction of it, then package/tier so different
  buyers self-select. Contrast explicitly with cost-plus and competitor-matching.
- **Key claims safe to make:** value-based pricing tied to quantified buyer value
  is standard B2B SaaS pricing doctrine; cost-plus under-prices software whose
  marginal cost is ~0; packaging/tiering to willingness-to-pay is routine.
- **Claims to avoid:** no specific dollar figure presented as universally
  correct; no buyer proof or "validated pricing" claim; do not disclose or imply
  Orca's own pricing; do not quote Quora; flag that value quantification requires
  real customer input the reader still has to gather.
- **Draft / outline:**
  > **Price your B2B SaaS to the value it creates, not the cost to build it**
  >
  > Cost-plus pricing is a trap for software: your marginal cost is near zero, so
  > cost tells you almost nothing about the price. Price to *value* instead:
  >
  > 1. **Quantify the gain.** In the buyer's own terms: hours saved × loaded
  >    cost, revenue unlocked, or errors avoided. Get this from discovery, not a
  >    spreadsheet guess.
  > 2. **Capture a fraction.** Charge a defensible slice of that gain (a common
  >    rule of thumb is a small single-digit multiple of price-to-value, i.e. the
  >    buyer keeps most of the surplus). The number matters less than the ratio
  >    being *justifiable to the buyer*.
  > 3. **Package to willingness-to-pay.** Tier so a solo user, a team, and an
  >    enterprise each self-select into a price that matches the value they get —
  >    same product, different value captured.
  >
  > If you can't state the buyer's gain in a sentence with a number in it, you're
  > not ready to price — you're ready to do more discovery (see Unit A).

---

## Non-Claims and Drift Guard (carried from the handoff)

- No live Quora capture, scrape, or re-run was performed to produce this pilot.
- This pilot does not claim Quora access is generally reliable; the underlying
  capture is one bounded CloakBrowser persistent-profile success with a local
  ignored profile, no proxy, and caller-bound detail sufficiency.
- No buyer proof, market proof, source-quality proof, Quora policy guidance, or
  session-durability claim is made or implied.
- No candidate was extracted from a failed packet; all three come from the
  sufficiency-passed PR #825 calibration record.
- This is answer strategy, not source capture: no new capture run, no code
  change, no product-readiness claim. The optional code improvement discussed
  around PR #825 (persisting caller-bound sufficiency requirements as a
  structured receipt field) is explicitly **out of scope** here and would need
  fresh authorization.
- Final content angle is owner / Chief Architect owned. These are drafts and
  decision input, not approved published content.

## Suggested Next Moves (owner decision input, not self-authorized)

- Adjudicate the three drafts and confirm the recommended-default cluster (or
  request the `210, 215` marketplace swap for unit C).
- If kept, decide whether these drafts graduate into actual published answers
  (a separate content-execution step with its own review), and whether the
  originating handoff packet on `codex/quora-playbook-handoff` should be landed to
  `main` so this pilot's provenance chain is fully on-`main`.
- Decide separately (fresh authorization) whether the deferred capture-receipt
  code improvement is worth doing.
