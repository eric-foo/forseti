## Orca Product Proof Lead Customer Discovery Prompt v0 - Adversarial Artifact Review

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the Orca Product Proof Lead customer-discovery prompt v0 against accepted product-proof boundary.
use_when:
  - Deciding whether to use the v0 customer-discovery prompt for Product Proof Lead prep.
  - Tracing whether prior-review patches were correctly applied.
  - Locating remaining friction findings against the Orca product-proof overlay.
authority_boundary: retrieval_only
input_hashes:
  - path: docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md
    sha256: E344CB4FF1D72AC758D14EC35DA6DFC191D4660B47B64011655A41EB39A83255
  - path: docs/product/orca_product_proof_lead_charter_v0.md
    sha256: FB77FE195A741CCF1510AB2C6BDB59E9970264DD82E7FF37A4212E9993A59492
  - path: docs/product/orca_buyer_proof_packet_v0.md
    sha256: C0DCE0ED92C641A7B109D28B74D5EDD57EF01281EA9ED776DBD5FC8B2C9EF8DF
  - path: .agents/workflow-overlay/product-proof.md
    sha256: DBA693516B1DE92661D6E2EE6FF6535091A36059B0122EFFB52A00FE6EDFF853
  - path: .agents/workflow-overlay/communication-style.md
    sha256: 632EBF02E0B539888F46F54C8C0AA6AA3756C24D769A9A1262CB798F2AEB343A
branch_or_commit: main @ 3bf5c45
stale_if:
  - Target prompt hash changes.
  - Any boundary artifact hash changes.
```

## Review Header

- Reviewed artifact: `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Branch / HEAD: `main` @ `3bf5c45`
- Dirty state: allowed; target artifact is currently untracked, consistent with prompt expectation.
- Review lane: adversarial artifact review (read-only).
- Source loading mode: strict bound to Orca overlay product-proof authority.
- Deep-thinking discipline: applied prior to findings.
- Prior review present: `docs/review-outputs/adversarial-artifact-reviews/orca_product_proof_lead_customer_discovery_prompt_v0_review.md`. Prior review was not reread; current review verifies stated patches against current artifact text per prompt instruction.

## Source-Read Ledger

| Path | Purpose | State |
| --- | --- | --- |
| `AGENTS.md` | Project authority entrypoint | Clean |
| `.agents/workflow-overlay/README.md` | Overlay binding rule | Modified (untracked sections noted); used only for binding rule |
| `.agents/workflow-overlay/prompt-orchestration.md` | Prompt artifact contract | Modified; used for full-prompt fields, validation gates |
| `.agents/workflow-overlay/review-lanes.md` | Adversarial artifact review lane rules | Modified; used for lane scope and report location |
| `.agents/workflow-overlay/validation-gates.md` | Product Proof Gates (objection/refusal, trust-refusal, pull) | Modified; used for trust-handling gates |
| `.agents/workflow-overlay/artifact-folders.md` | Report destination | Modified; confirms `docs/review-outputs/adversarial-artifact-reviews/` |
| `.agents/workflow-overlay/artifact-roles.md` | Review report role binding | Modified; used for retrieval header field set |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | Untracked; used for forbidden-field check |
| `.agents/workflow-overlay/communication-style.md` | YAML summary shape | Modified; hash matches expected |
| `.agents/workflow-overlay/product-proof.md` | Trust-objection canonical semantics | Untracked; hash matches expected |
| `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md` | Target artifact | Untracked; hash matches expected |
| `docs/product/orca_product_proof_lead_charter_v0.md` | Boundary - Product Proof Lead charter | Untracked; hash matches expected |
| `docs/product/orca_buyer_proof_packet_v0.md` | Boundary - buyer proof packet | Untracked; hash matches expected |

Dirty source relied on: all overlay sections relied on for authority are modified or untracked, which is allowed under the prompt-declared dirty-state allowance. The target artifact and product-proof boundary artifacts are untracked; their hashes match the expected pinned values, so dirty-state is not authority-compromising for this review.

Contaminated archives under `docs/_inbox/` were not read.

## Trigger-Gate Result

User explicitly invoked adversarial artifact review with an Orca-owned prompt artifact target. Lane scope is satisfied.

## Lane-Collision Result

No collision. The target is a non-code artifact (durable prompt). It is not implementation, not an installed copy, and not completed work. The artifact-review lane is correctly selected.

## Artifact-Role Preflight Result

Target prompt declares `artifact_role: Full prompt artifact`. This binding is registered in `.agents/workflow-overlay/artifact-roles.md`. Destination `docs/prompts/product-planning/` is registered in `.agents/workflow-overlay/artifact-folders.md`. Hashes match. Edit permission for this review is read-only with write authority limited to the named report path. No role drift detected.

## Validation-Gate Status

Applicable Orca gates:

- Overlay authority gate: pass. AGENTS.md and overlay README were read.
- Artifact role gate: pass. Target role bound.
- Source-resolution gate: pass. No `jb` policy imported into Orca authority.
- Worktree preflight gate: pass. Hash-pinned, dirty-state allowance honored.
- Output-mode gate: pass for review-report.
- Retrieval-metadata gate (target): pass on structure (assessed in finding AR-08).
- Product Proof Objection/Refusal gate: pass (assessed in findings).
- Trust-refusal gate: pass on substance (assessed in findings).
- Pull-versus-praise gate: pass on substance (assessed in findings).
- Leakage gate: pass. No jb/GAP/CV/compiler paths or templates imported.
- Readback economy gate: pass; review uses targeted reads, no broad echo.

## Review Scope

In scope:

- Whether the v0 prompt is now safe to use for Product Proof Lead customer-discovery prep.
- Trust-objection and trust-refusal handling against `.agents/workflow-overlay/product-proof.md`.
- Disqualifier narrowness, kill criteria alignment, memo gate alignment, Grade D criteria, stop/continue rules, owner-acceptance gating before product-bet planning.
- Live-decision qualification structure.
- Discovery script for leading commercial-pull questions.
- Pull grading rubric and second-memo handling.
- Consulting-risk indicator handling.
- Retrieval metadata and review handoff structure.
- Non-claims preservation.

Out of scope:

- Public web research (forbidden by prompt).
- Buyer outreach or actual discovery execution.
- Memo production.
- Source map, source system, automation, or implementation planning.
- Reread of contaminated `docs/_inbox/` archives.
- Reread of prior review report; patches are verified against current target text only.

## Phase 1 - Correctness Findings

### Non-Finding NF-01 — Trust state classification matches overlay

Target artifact lines 159-164 define `trust_open`, `trust_objection`, and `trust_refusal` consistent with `.agents/workflow-overlay/product-proof.md` lines 25-29. The proceed/block rule at line 164 ("`trust_objection` may proceed to discovery and, if other gates pass, memo production. `trust_refusal` disqualifies or blocks memo production.") is aligned with overlay line 31. Not a finding.

### Non-Finding NF-02 — Initial buyer skepticism preserved as proof material

Disqualifier list at line 176 uses categorical refusal language ("buyer says public-signal evidence cannot affect this decision regardless of evidence quality, explanation, examples, numbers, case logic, or proof memo"). The "regardless of" condition is the canonical disqualifier predicate. Grade D criterion at line 326 requires either `trust_refusal` OR post-readback failure ("the proof memo fails to move a `trust_objection` enough for public-signal evidence to affect the decision"). Stop/Continue rule at line 394 mirrors the same predicate. Initial skepticism is not a kill criterion. Not a finding.

### Non-Finding NF-03 — Memo production gate uses willingness-to-evaluate standard

Memo Production Gate item at line 274 ("Buyer is at least willing to evaluate public-signal evidence after the method, examples, evidence quality, numbers, or case-style explanation are provided") matches the willingness-to-evaluate standard. `trust_objection` correctly passes this gate. Not a finding.

### Non-Finding NF-04 — Live-decision qualification structurally complete

Filter 4 at line 147 requires named decision, owner, timing within 30-90 days, and allocation consequence. Disqualifier at line 172 mirrors the same structure. Memo Production Gate at line 273 mirrors the same. Discovery script questions 199-205 elicit all four. Not a finding.

### Non-Finding NF-05 — Discovery script avoids leading commercial-pull questions

Memo usefulness questions at lines 217-220 and meaningful-next-step questions at lines 232-233 are open-ended ("what would make a memo useful enough", "What commercial next step, if any, would be appropriate"). Memo-readback question 9 at line 294 also uses "if any" framing. No leading "would you pay for this" wording detected. Not a finding.

### Non-Finding NF-06 — Paid-pilot-level pull, second-memo, owner-acceptance handling

Paid-pilot-level pull definition at lines 332-334 mirrors charter line 132 verbatim. Second-memo classification at line 330 correctly downgrades to Grade B unless paired with a commercial next-step signal. Stop/Continue rule at line 391 ("Meeting graduation criteria does not authorize product-bet planning. Owner acceptance of proof evidence is required before any graduation step may proceed.") and Non-Claims line 409 enforce owner-acceptance gating before any product-bet or feature-planning move. Not a finding.

### Non-Finding NF-07 — Non-claims preserved comprehensively

Non-Claims section at lines 397-409 lists all eight non-claims from `.agents/workflow-overlay/product-proof.md` lines 79-89. Hard Boundaries at lines 102-108 repeat them. Output Contract at lines 432-433 reasserts them as forbidden output. Not a finding.

### Finding AR-01 — Disqualifier wording diverges slightly from overlay canonical predicate

- Phase: correctness
- Location: line 176 ("Categorical public-signal refusal: ...or proof memo")
- Source authority: `.agents/workflow-overlay/product-proof.md` lines 28-29 ("...or proof experience")
- Artifact evidence: prompt disqualifier list ends with "or proof memo." Overlay canonical predicate for `trust_refusal` ends with "or proof experience."
- Requirement strained: trust-refusal predicate consistency. `proof experience` is broader than `proof memo` (it includes readback, mechanism walkthrough, examples), so the prompt's narrower predicate could in principle let a buyer who would not be moved by the proof experience but who has not yet rejected a memo specifically pass disqualification.
- Impact: low operational impact in practice because the trust-state classification at lines 159-164 still uses the overlay-canonical "or proof experience" language at line 162. The narrower disqualifier wording is structurally tolerable since the canonical trust-state predicate dominates in any conflict.
- Blocked state: not blocked. Advisory consistency drift.
- Patch-queue authorization: not authorized in this lane.
- Verification gate: re-hash overlay product-proof and prompt after any normalization patch.
- Next authorized action: optional consistency normalization to "or proof experience" in line 176 if the owner wants overlay-canonical phrasing throughout. Not blocking acceptance.

### Finding AR-02 — Consulting-risk indicator field not bound to a trigger condition inside the prompt

- Phase: correctness
- Location: line 353 (per-contact batch note: `Consulting-risk indicator: yes | no | unknown`); line 376 (per-batch note: `Consulting-risk indicators:`)
- Source authority: `docs/product/orca_product_proof_lead_charter_v0.md` line 105 and `docs/product/orca_buyer_proof_packet_v0.md` line 105 ("If it materially exceeds [4-6 hours], classify the result as consulting-risk evidence and record it in the batch notes.")
- Artifact evidence: the prompt requires the operator to set a consulting-risk indicator value but does not declare when it should be marked `yes`. The 4-6 hour rule from the charter and packet is not carried into the prompt body. The prompt's Required first read does include both source artifacts, but a strict operator reading only the prompt would not know the trigger predicate.
- Requirement strained: the prompt should be self-contained for routine operator use. Trigger predicates for graded fields should be visible at the point of use.
- Impact: low to medium. Risk that consulting-risk evidence is silently underclassified, which weakens kill-criterion sensitivity to bespoke-consulting failure mode.
- Blocked state: not blocked.
- Patch-queue authorization: not authorized in this lane.
- Verification gate: prompt body lists trigger predicate near the batch-note format.
- Next authorized action: optional patch to add a one-line definition near the batch note ("Mark `yes` when memo production materially exceeds 4-6 focused hours, or when value depends on bespoke labor with no repeatable decision pattern.") Not blocking acceptance because Required first read covers it indirectly.

### Finding AR-03 — Discovery script does not explicitly require probing the "regardless of" condition before classifying as trust_refusal

- Phase: correctness
- Location: lines 213-215 (Public-signal trust questions)
- Source authority: `.agents/workflow-overlay/product-proof.md` lines 28-29 (canonical predicate uses "regardless of evidence quality, examples, numbers, mechanism, case logic, or proof experience"); prompt lines 162 and 176 (mirrors).
- Artifact evidence: discovery script asks "If you are skeptical, what method, example, evidence quality, numbers, case study, or explanation would you need before deciding whether public signals can affect this decision?" This probes willingness, but the classification responsibility is left implicit. A categorical-sounding initial buyer statement could be misclassified as `trust_refusal` without the "regardless of" condition being explicitly probed.
- Requirement strained: defensive classification discipline. The overlay treats initial skepticism as proof material; the prompt should make it harder to short-circuit to `trust_refusal`.
- Impact: low to medium. Risk of premature disqualification on a candidate who could actually be moved by proof experience. Especially material because `trust_refusal` is the only categorical disqualifier on trust grounds, so misclassifying it directly retires a candidate.
- Blocked state: not blocked.
- Patch-queue authorization: not authorized in this lane.
- Verification gate: discovery script or classification note explicitly requires testing "regardless of evidence quality, examples, numbers, mechanism, case logic, or proof experience" before classifying `trust_refusal`.
- Next authorized action: optional patch adding a one-line classifier rule above or below the Public-signal trust question block ("Classify as `trust_refusal` only when the buyer's position is categorical against all enumerated evidence types - quality, examples, numbers, mechanism, case logic, or proof experience.") Not blocking acceptance because the predicate is present in the trust-state taxonomy and the disqualifier list.

### Finding AR-04 — "Owner" terminology is overloaded between project owner and decision owner

- Phase: correctness
- Location: lines 391 ("Owner acceptance of proof evidence is required before any graduation step may proceed.") and 409 ("graduation itself still requires owner acceptance before any product-bet planning or later feature-planning turn.")
- Source authority: `docs/product/orca_product_proof_lead_charter_v0.md` line 167 (uses "Owner acceptance"); `docs/product/orca_buyer_proof_packet_v0.md` line 318 (uses "owner acceptance of the proof boundary").
- Artifact evidence: the prompt uses "decision owner" (buyer-side), "budget owner" (buyer-side), and bare "owner" (project-side) in the same artifact. Bare "owner" in lines 391 and 409 means project owner (i.e., the Orca operator/user). A naive operator could read "owner acceptance" as the decision-owner buyer's acceptance and conflate proof-graduation gating with buyer behavior.
- Requirement strained: terminology disambiguation.
- Impact: medium. If misinterpreted, an operator could believe graduation criteria are met because the buyer is "accepting" the memo, and proceed to product-bet planning without project-owner authorization, leaking into the bounded scope.
- Blocked state: not blocked.
- Patch-queue authorization: not authorized in this lane.
- Verification gate: bare "owner" replaced with "project owner" or "Orca owner" in graduation-gating contexts.
- Next authorized action: optional patch normalizing "owner acceptance" to "project owner acceptance" or equivalent unambiguous phrasing in lines 391 and 409. Not blocking acceptance because the surrounding sentence ("does not authorize product-bet planning") makes the project-side intent recoverable from context.

### Finding AR-05 — Retrieval header is structurally compliant

- Phase: correctness
- Location: lines 3-29
- Source authority: `.agents/workflow-overlay/retrieval-metadata.md`
- Artifact evidence: required fields present (`retrieval_header_version`, `artifact_role`, `scope`, `use_when`, `authority_boundary: retrieval_only`). Triggered fields used appropriately: `open_next` lists controlling sources; `input_hashes` documents accepted product-proof source artifacts; `branch_or_commit` pins prompt creation revision; `downstream_consumers` is named; `stale_if` lists conditions.
- Forbidden header fields check: no approval status, validation status, readiness, lifecycle, deployment/install/resolver state, edit permission, executor authorization, review verdict, or source-of-truth promotion appear in the retrieval header. (Status, output mode, and edit permission do appear in the artifact body, which is permitted by the contract.)
- Result: not a finding. Header structure passes review checks.

## Phase 2 - Friction Findings

### Finding AR-06 — Role Boundary and Hard Boundaries duplicate exclusions

- Phase: friction
- Location: lines 95-108 (Hard Boundaries) and lines 122-138 (Role Boundary)
- Source authority: prompt-orchestration economy and communication-style readability preferences.
- Artifact evidence: both sections list the same exclusions (product-bet planning, feature planning, implementation planning, source systems, automation, dashboards, source maps, data-spine, CRM, commercial-readiness claims, buyer-validation claims, willingness-to-pay claims, Core Spine v0 validation claims).
- Impact: cognitive friction; prompt is heavier than necessary. The duplicate listing has a mild defensive value (catches operators who skim one section) but contributes to scroll burden across the discovery script.
- Blocked state: not blocked.
- Patch-queue authorization: not authorized in this lane.
- Next authorized action: optional consolidation if a future revision is opened. Not blocking acceptance.

### Finding AR-07 — Discovery script has approximately 25 questions without explicit per-call scoping

- Phase: friction
- Location: lines 184-233
- Source authority: communication-style readability preference for "concise questions."
- Artifact evidence: prompt instructs "Use concise questions" but lists eight question groups with two to four questions each. The memo-readback section at line 284 says "Use 5-8 of these" - the discovery script does not provide a similar scoping rule for the first call.
- Impact: low. Risk that an operator treats the discovery script as a fixed checklist rather than a selectable library, which could exhaust buyer attention on a first contact.
- Blocked state: not blocked.
- Patch-queue authorization: not authorized in this lane.
- Next authorized action: optional one-line scoping rule near the Discovery Script header ("Select 6-10 questions per call. Use the rest in follow-ups."). Not blocking acceptance.

### Finding AR-08 — Repeat signal label used in batch note without local definition

- Phase: friction
- Location: line 375 (per-batch note: `Repeat signal: yes | no | inconclusive`)
- Source authority: `docs/product/orca_product_proof_lead_charter_v0.md` lines 162-163 and `docs/product/orca_buyer_proof_packet_v0.md` line 254 ("Repeat means: At least two independent qualified decision owners in the same buyer segment and decision family produce Grade A or Grade B results...").
- Artifact evidence: the field appears in the per-batch note format without an adjacent definition. The Stop/Continue Rules at lines 388-390 describe the predicate functionally but do not label it "Repeat signal" explicitly.
- Impact: low. An operator who has read the charter or packet recovers the predicate easily; an operator who has only skimmed the prompt may misclassify.
- Blocked state: not blocked.
- Patch-queue authorization: not authorized in this lane.
- Next authorized action: optional inline gloss near the field, or a back-reference to the Stop/Continue Rules. Not blocking acceptance.

## Not-Proven Boundaries

This review does not prove:

- Buyer validation, willingness-to-pay, repeatable demand, product readiness, feature readiness, implementation readiness, commercial readiness, or Core Spine v0 validation. None of these are within review scope and the prompt itself explicitly forbids such claims.
- That prior-review findings beyond those listed in the prompt's stated patches were remediated. The prior review report was not reread, per prompt instruction. Only the patches listed in the current prompt's "Prior Patch Context To Check" section were verified against current artifact text.
- That the prompt will perform correctly under operator misuse. The friction findings (AR-06, AR-07, AR-08) describe conditions that increase misuse risk but do not deterministically cause failure.

## Strict-Only Blockers

None applicable. The review is within bound artifact-review lane authority. No strict claim is being made that exceeds available authority.

## Optional Patch Queue

Not emitted. Findings are advisory only and do not produce executor-ready patch entries in this lane. Patch-execution authority requires a separate authorized lane per `.agents/workflow-overlay/review-lanes.md`.

## Prior-Patch Verification

The prompt's "Prior Patch Context To Check" lists patches that the prior review prompted. Verification against current artifact text:

| Stated patch | Verified location | Status |
| --- | --- | --- |
| Public web research exception removed | Line 99: "Do not run public web research in this customer-discovery preparation or operating prompt." | Verified |
| Leading commercial pull questions replaced with open-ended commercial-next-step wording | Lines 232-233, 294: "What commercial next step, if any, would be appropriate..." | Verified |
| Live decision trigger tightened | Line 147: requires named decision, owner, timing within 30-90 days, allocation consequence | Verified |
| Trust handling added | Lines 159-164 (trust taxonomy); lines 167-182 (disqualifiers); line 326 (Grade D) | Verified |
| Public-signal trust disqualifier narrowed to categorical refusal | Line 176: explicit "regardless of evidence quality, explanation, examples, numbers, case logic, or proof memo" predicate | Verified (with AR-01 wording note) |
| Memo gate updated for willingness-to-evaluate standard | Line 274: "Buyer is at least willing to evaluate public-signal evidence after the method, examples, evidence quality, numbers, or case-style explanation are provided" | Verified |
| Owner acceptance required before product-bet planning | Lines 391, 409 | Verified (with AR-04 disambiguation note) |
| Second-memo request alone classified as Grade B unless paired with paid-pilot-level pull | Line 330 | Verified |
| Consulting-risk indicator added | Lines 353, 376 | Verified (with AR-02 trigger-condition note) |
| 30-90 day follow-up question added | Line 201 | Verified |
| Batch default added for 6-8 targets | Line 386 | Verified |
| `trust_open`, `trust_objection`, `trust_refusal` taxonomy harmonized | Lines 159-164 mirror overlay product-proof.md lines 25-29 | Verified |

All stated patches are present.

## Review-Use Boundary

These findings are decision input for the project owner and any subsequent Chief Architect sequencing. They are not mandatory remediation. Only a separately authorized patch, acceptance, validation, or implementation lane can make remediation executor-ready.

Discovery work under this prompt may proceed at the project owner's discretion with awareness of the four advisory correctness drifts (AR-01 through AR-04) and the three friction items (AR-06 through AR-08). None of these conditions cause the prompt to test the wrong buyer, wrong decision, wrong proof signal, or to assert prohibited readiness claims when the prompt is followed and the Required first reads are loaded.

## Recommendation

`accept_with_friction`.

The prompt is structurally safe to use for Product Proof Lead customer-discovery preparation within the declared scope. All prior-review-stated patches are present in the current artifact. Trust handling, disqualifier narrowness, memo gate, Grade D, kill criteria, stop/continue rules, paid-pilot-level pull, second-memo handling, consulting-risk indicator placement, owner-acceptance gating, non-claims, and retrieval metadata pass the boundary checks against `.agents/workflow-overlay/product-proof.md` and the accepted product-proof boundary artifacts.

The remaining findings are advisory consistency drifts and friction items. They reduce robustness under operator misuse but do not block safe use under the prompt's required-first-read discipline.

## Next Authorized Step

Project owner may accept the prompt for active use, with optional consideration of normalizing patches for AR-01 through AR-04 in a future revision. No further adversarial review is required before first authorized discovery use unless the project owner changes target buyer segment, decision family, proof shape, or non-claim boundary, or unless `.agents/workflow-overlay/product-proof.md` trust-objection semantics change.
