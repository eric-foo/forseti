# Delegated Adversarial Artifact Review + Bounded Patch - Phase-1 Pilot Ledger Doctrine v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Delegated adversarial artifact review and bounded patch of the Phase-1 pilot ledger doctrine.
use_when:
  - Inspecting findings or the proposed bounded patch before CA adjudication.
  - Tracing prospective-loop ledger changes to this review.
authority_boundary: retrieval_only
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/prospective_loop_phase1_pilot_ledger_delegated_adversarial_artifact_review_v0.md
  target: docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md
  recommendation: adjudicate_diff
  finding_counts:
    critical: 0
    major: 4
    minor: 0
  patch_status: uncommitted_working_tree_patch_applied
  advisory_bound: advisory decision input only; no formal review-lane verdict, validation, readiness, ratification, or pilot authorization claim
```

## Advisory-Only Bound

This run follows the commissioned delegated review-and-patch prompt, but the formal Orca review skills are not applied as strict review authority in this runtime. Findings, diff, recommendation, and residual risk are advisory decision input for the commissioning Chief Architect only. The provisional delegated-review-and-patch convention creates no validation, readiness, acceptance, ratification, pilot authorization, mandatory remediation, or product-proof claim.

Actor/model-family receipt: the reviewed artifact records `authored_by: claude-fable-5[1m]`; this controller is OpenAI-family / non-Anthropic, satisfying the commission's cross-vendor who-constraint for discovery in repo mode. Concrete runtime identity is recorded as `reviewed_by: OpenAI GPT-5 Codex (exact runtime version unrecorded)`.

## Reasoning-Before-Findings Pass

The ledger's fitness bar is not "looks careful"; it must be safe for the owner to sign and then run a real shadow decision through without inventing semantics or opening a selection channel. The load-bearing failure modes are:

- A signed ledger could appear to authorize a first seal while a required structural precondition remains loose.
- The run shape could drift from the Phase-0 book, creating a parallel protocol under the name of consuming the book.
- The decision-selection criteria could let the owner fill rows that are real but already decision-known, outcome-aligned, or only selectively scoreable.
- Claim caps and OWNER-FILL emptiness must remain intact; hardening must not fill the decision list or advance the draft status.

Decision criteria applied: no seal before signature and ledger-home binding; exact book fidelity for entry mechanics; pre-declared report-all set; no self-reference or favorable-alignment selection; product-learning cap only.

## Findings

### Major 1 - Run-shape drift invented a non-book entry

Location: target original `Pilot Design`, run-shape bullet around lines 81-84.

Issue: The ledger said the chain was `01_intake` -> `02_sealed_call` -> `04_actual_path` -> `0M_resolution_<seal-entry>`. The Phase-0 semantics spec defines the folder entries as `01_intake.md`, `02_sealed_call.md`, optional assisted-mode `03_disclosure.md`, optional `0N_update_seal.md`, and `0M_resolution.md`. `actual_path` is a decision-object field, not an entry file.

Evidence: Target original run-shape bullet invented `04_actual_path`. The semantics spec's "The Book: Entry Mechanics" defines the folder shape without that file and separately defines `actual_path` as passive observation. The target architecture also defines `actual_path` inside the decision object.

Impact: This is a firewall defect: the pilot would claim to run the book while creating a new entry protocol and new naming semantics at first real seal.

Minimum closure condition: The ledger must consume the book's exact entry mechanics and explicitly not invent an `actual_path` entry.

Next authorized action: Bounded target patch.

Advisory remediation: Patched the run-shape bullet to name the book's entries exactly and state that `actual_path` is a field, not a file.

### Major 2 - Selection criteria contradicted unscoreable-by-design admission

Location: target original `Decision Selection Criteria`, criterion 2 around lines 97-100; table header around line 118.

Issue: The criteria said every candidate qualifies only if all criteria hold, then criterion 2 was named `Scoreable`, while the table allowed `Scoreable? (Y / unscoreable_by_design)` and the body allowed non-scoreable rows to be logged. That made it unclear whether unscoreable decisions are allowed members, excluded members, or optional after-the-fact exceptions.

Evidence: The Phase-0 semantics spec says missing or unmeasurable expected outcomes make a decision `unscoreable_by_design`, loggable for memory and permanently excluded from calibration. The target ledger already requires report-all including `unscoreable_by_design` outcomes.

Impact: Ambiguity here can become selection bias: unscoreable cases could be included or excluded after their convenience is visible, weakening the report-all and calibration boundaries.

Minimum closure condition: The criterion must distinguish outcome-declarable rows from calibration-counting rows, and require any `unscoreable_by_design` admission to be fixed at signature.

Next authorized action: Bounded target patch.

Advisory remediation: Patched criterion 2 to `Outcome-declarable`, with scoreable rows and explicitly admitted `unscoreable_by_design` rows both fixed at signature; unscoreable rows remain reportable but excluded from calibration.

### Major 3 - "Outcome not yet knowable" did not bar already-made org decisions

Location: target original `Decision Selection Criteria`, criteria 4-5 around lines 105-109.

Issue: The old wording barred outcome knowledge but did not explicitly bar a decision whose org actual path was already made or irreversibly committed before seal. A future outcome can still be unknown even when the decision itself is already known, which would make the passive actual-path comparator non-prospective.

Evidence: The target architecture's shadow mode depends on Orca sealing before the org decides normally and on later comparing the sealed call to the uninfluenced actual path. The semantics spec defines `actual_path` as passive observation when the org decides.

Impact: A row could pass the literal old criterion while the actual path was already known, turning the pilot into a retrospective or confirmatory exercise under prospective wording.

Minimum closure condition: Criteria must require both the org decision and its outcome signal to be not yet knowable/committed at intake, and must block favorable-alignment inspection before the set is fixed.

Next authorized action: Bounded target patch.

Advisory remediation: Patched criterion 4 to require the org decision not be made or irreversibly committed, and criterion 5 to bar pre-fix inspection of expected direction, actual path, or outcome signal for favorable alignment.

### Major 4 - Ledger-home binding was not an explicit no-seal condition

Location: target original retrieval header line 5, Status lines 33-37, Owner Decisions Required lines 167-171, and sign-off block lines 181-189.

Issue: The artifact role and Status text said no seal until decision list and signature, while ledger-home binding was named elsewhere as a separate amendment at signature and the sign-off block carried `ledger_home_bound: false`. That left a path where status could advance and a first seal could be attempted before the ledger home existed as an authorized artifact folder.

Evidence: The Phase-0 semantics spec's proposed ledger home is explicitly proposal-only and says the owner binds it at pilot-ledger sign-off with an artifact-folders amendment. The target ledger's own execution rules require one folder of chained entries per decision under the ledger home.

Impact: A first seal without a bound home would create either an unowned location or a later relocation problem for hash-chained entries, weakening durable ordering and artifact-role boundaries.

Minimum closure condition: The draft must state that ledger-home binding is a signing/no-seal precondition, not a loose follow-up checkbox.

Next authorized action: Bounded target patch.

Advisory remediation: Patched the artifact role, Status, OWNER-FILL instruction, ledger-home owner decision, and sign-off status comment to make `ledger_home_bound: true` part of the pre-first-seal authorization boundary.

## Unified Diff

```diff
diff --git a/docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md b/docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md
index fedce6a..bd3a44e 100644
--- a/docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md
+++ b/docs/decisions/prospective_decision_loop_phase1_dogfood_pilot_ledger_v0.md
@@ -2,7 +2,7 @@

 ```yaml
 retrieval_header_version: 1
-artifact_role: DRAFT decision record (pre-declared dogfood shadow pilot ledger; binds nothing and authorizes no seal until the owner fixes the decision list and signs)
+artifact_role: DRAFT decision record (pre-declared dogfood shadow pilot ledger; binds nothing and authorizes no seal until the owner fixes the decision list, binds the ledger home, and signs)
 scope: >
   Pre-declared ledger for the Phase-1 dogfood shadow pilot of the prospective
   decision loop: the counterparty-free first run, on real Orca-INTERNAL
@@ -34,7 +34,8 @@ stale_if:
 closeout_state or claim tier. This artifact **authorizes no seal**. Two
 owner-owned inputs are unfilled by design (the decision list and the per-decision
 mode); the agent must not invent them. Signing = fixing those slots + the
-sign-off block below. Until then nothing in the loop may be sealed.
+sign-off block below + the ledger-home binding amendment. Until then nothing in
+the loop may be sealed.

 ## Authorization Basis And Cap

@@ -79,10 +80,11 @@ favorability:
   abandoned, and `breached_quarantined` outcomes. Selective reporting voids the
   pilot's anti-cherry-pick property.
 - **Run shape mirrors the hardened book.** Each decision is one folder of
-  write-once hash-chained entries (`01_intake` → `02_sealed_call` →
-  `04_actual_path` → `0M_resolution_<seal-entry>`), per the semantics spec's
-  entry mechanics and dual-hash chain rule. The pilot does **not** re-derive the
-  chain shape.
+  write-once hash-chained entries exactly as the semantics spec defines:
+  `01_intake.md` → `02_sealed_call.md` → optional `0N_update_seal.md` →
+  `0M_resolution.md`; shadow mode omits `03_disclosure.md`. `actual_path` is a
+  decision-object field recorded in the run record, not a separately invented
+  `04_actual_path` entry. The pilot does **not** re-derive the chain shape.
 - **Mechanical resolution.** Resolution applies the `resolution_criteria` sealed
   into each call; it never authors or amends them. A decision whose outcome
   criterion cannot be pre-specified is admitted as `unscoreable_by_design` —
@@ -94,26 +96,30 @@ A candidate decision qualifies for the pre-declared set only if **all** hold:

 1. **Real and live** — an actual Orca operating decision with a genuine owner
    and a near-term `decision_deadline`, not a hypothetical.
-2. **Scoreable** — its `expected_outcome` admits a named observable metric, a
-   predicted band, and a measurement window that closes in a tractable horizon.
-   If not, it may still be logged `unscoreable_by_design` but does not count
-   toward the calibration set.
+2. **Outcome-declarable** — its `expected_outcome` either admits a named
+   observable metric, a predicted band, and a measurement window that closes in
+   a tractable horizon, or is explicitly admitted at signature as
+   `unscoreable_by_design` for protocol-falsification / decision-memory only.
+   `unscoreable_by_design` rows are reported but never count toward the
+   calibration set.
 3. **Not self-referential** — not a decision *about the loop itself* (e.g., "do
    we build N9", "do we ratify the target"). Shadowing the loop's own
    governance would contaminate the pilot with reflexivity. Pilot decisions are
    ordinary Orca product/research/operating calls.
-4. **Outcome not yet knowable at intake** — the decision is open and its outcome
-   has not begun arriving, so the seal is genuinely prospective.
+4. **Decision and outcome not yet knowable at intake** — the org decision has
+   not been made or irreversibly committed, and its outcome has not begun
+   arriving, so both the sealed call and the passive actual-path observation are
+   genuinely prospective.
 5. **Owner-fixed before reveal** — the full set is fixed at signature, before
-   any member's gate-0/outcome is examined, so membership cannot correlate with
-   favorability.
+   any member's expected direction, actual path, or outcome signal is examined
+   for favorable alignment, so membership cannot correlate with favorability.

 ## Pre-Declared Decision Set (OWNER-FILL — do not fabricate)

 > The agent has intentionally left this list empty. These are real Orca
 > operating decisions only the owner can name. Fill 3-5 rows (suggested range;
 > owner fixes N) at signature, fix the per-decision mode (`shadow` for Phase 1),
-> then the set is frozen and amended only by dated note.
+> bind the ledger home, then the set is frozen and amended only by dated note.

 | # | Decision (one-line brief) | Decision family | Mode | Decision deadline | Scoreable? (Y / unscoreable_by_design) |
 | --- | --- | --- | --- | --- | --- |
@@ -168,7 +174,8 @@ amendments (owner-gated); and the single-operator-residual honesty note.
    `docs/product/judgment_spine/decision_ledger/` with a permanent
    location-confers-no-evidence-tier boundary. Binding it is a separate
    `artifact-folders.md` amendment with its own propagation receipt, executed at
-   signature — not by this draft.
+   signature — not by this draft. No first seal is authorized while
+   `ledger_home_bound` remains false.
 4. **Recommended gate before first seal:** a de-correlated cross-vendor review
    of this ledger's doctrine (authorization basis, selection criteria,
    anti-cherry-pick completeness, firewall-preservation) plus a post-fill check
@@ -180,7 +187,7 @@ amendments (owner-gated); and the single-operator-residual honesty note.

 ```yaml
 pilot_signoff:
-  status: DRAFT_PENDING_OWNER_SIGNOFF   # advance to PILOT_ACTIVE_OWNER_SIGNED on signature
+  status: DRAFT_PENDING_OWNER_SIGNOFF   # advance only after table fixed + ledger_home_bound true + owner signature
   owner: <owner-fill>
   signoff_date: <owner-fill>
   target_ratification_state: ratified | amended | proposed_stack   # owner decision 1
```

## Per-Change Neutral Citations

- Artifact-role/status/sign-off ledger-home condition: target original header and Status limited the no-seal condition to decision-list/signature; target Owner Decisions Required already made ledger-home binding an at-signature amendment; Phase-0 semantics spec says proposed ledger home is owner-bound at pilot-ledger sign-off.
- Run-shape hunk: target original run-shape invented `04_actual_path`; Phase-0 semantics spec folder shape names `01_intake.md`, `02_sealed_call.md`, optional `03_disclosure.md`, optional `0N_update_seal.md`, and `0M_resolution.md`; target architecture places `actual_path` inside `decision_object_v0`.
- Outcome-declarable hunk: target original table allowed `unscoreable_by_design`; Phase-0 semantics spec treats unmeasurable decisions as loggable for memory, excluded from calibration; target Pilot Design requires report-all including `unscoreable_by_design`.
- Decision/outcome-not-knowable hunk: target architecture shadow mode depends on a seal before the org decides normally and a later passive actual-path comparison; Phase-0 semantics spec records `actual_path` when the org decides.

## Verdict As Decision Input

Advisory recommendation: keep the bounded patch subject to home-model hunk adjudication. The patch closes four major doctrine defects without filling OWNER-FILL slots, advancing draft status, weakening claim caps, authorizing a seal, or editing adjacent sources.

No `NEEDS_ARCHITECTURE_PASS`: the defects were local ledger wording and precondition defects, not evidence that the Phase-1 ledger concept or Phase-0 book is structurally broken.

## Residual Risk Note

- The owner-filled decision list remains unreviewed. The commissioned post-fill check is still required before first seal unless the owner explicitly waives it with reason; this report does not inspect nonexistent rows.
- Target architecture ratification remains pending. If the owner signs while it remains proposed, the PROPOSED-stack product-learning ceiling still applies.
- This report is advisory decision input only under the provisional convention. Nothing here authorizes pilot execution, validates the loop, or promotes the target.

## Provenance And Non-Claims

```yaml
authored_by: claude-fable-5[1m]
reviewed_by: OpenAI GPT-5 Codex (exact runtime version unrecorded)
de_correlation_bar: cross_vendor_discovery
access_mode: repo
non_claims:
  - advisory decision input only
  - provisional delegated review-and-patch convention
  - no validation
  - no readiness
  - no pilot authorization
  - no ratification
  - no product-proof or judgment-quality claim
  - nothing kept until home-model adjudication
```

## Home-Model Adjudication (2026-06-13, appended by the commissioning lane)

```yaml
home_model_adjudication:
  adjudicator: claude-fable-5[1m] (author/home model; correlation disclosed — every hunk re-checked against the LANDED sources on origin/main directly)
  diff_verified: working-tree diff matched the report's Unified Diff before adjudication
  load_bearing_discovery: >
    Verifying Major 1 against origin/main revealed that the Phase-0 semantics
    spec's own cross-vendor adjudication (commit d847f6f: AR-01 evidence_unit_ids
    vocabulary fix + AR-02 04_actual_path / per-seal-resolution / dual-hash chain
    + the spec review report) was DROPPED by the PR #46 squash-merge. main's spec
    blob is byte-identical to the pre-adjudication a3ddd6d. The fixes survive on
    origin/phase0-semantics-spec-v0 @ d847f6f and are being re-landed via a
    separate PR. This reframes Major 1 (see below).
  per_finding:
    - finding: Major 1 (run-shape drift / "invented" 04_actual_path)
      decision: modified
      basis: >
        The controller correctly observed that the ledger referenced entries the
        LANDED main spec lacks — but that is because main's spec is stale (lost
        adjudication), not because the ledger invented anything. The controller's
        patch (revert to the old shape) would propagate the un-hardened shape
        forward. REJECTED that remedy; instead rewrote the run-shape bullet to
        reference the spec's entry-mechanics section BY POINTER with no restated
        filenames (robust to the spec revision), and added a no-seal precondition
        that the adjudication-hardened spec must be on main first.
    - finding: Major 2 (Scoreable -> Outcome-declarable)
      decision: accepted
      basis: distinguishes outcome-declarable members from calibration-counting members and fixes unscoreable admission at signature; tightens the report-all / anti-cherry-pick boundary; consistent with the spec's unscoreable_by_design gate
    - finding: Major 3 (bar already-committed org decisions)
      decision: accepted
      basis: genuine gap — a decision whose org actual-path is already committed makes the shadow comparator retrospective; criterion 4/5 rewrite preserves prospective integrity. Directly strengthens the firewall.
    - finding: Major 4 (ledger-home binding as no-seal precondition)
      decision: accepted
      basis: makes ledger_home_bound a hard pre-seal gate rather than a loose checkbox; consistent with the spec's proposal-only ledger home
  vetoes:
    - the controller's specific run-shape restatement (replaced by a pointer reference; see Major 1)
  modifications:
    - Major 1 run-shape bullet rewritten to a pointer reference
    - added owner-decision precondition: adjudication-hardened spec must be on main before first seal
  kept_state: Major 2/3/4 hunks kept as written; Major 1 hunk replaced; report committed on the pilot-ledger branch (PR #48)
  separate_followup:
    - re-land the dropped Phase-0 semantics-spec adjudication (d847f6f) onto main via its own PR
  non_claims:
    - adjudication is a keep-decision only; not validation, readiness, ratification, or pilot authorization
    - the ledger remains DRAFT_PENDING_OWNER_SIGNOFF at product-learning tier
```
