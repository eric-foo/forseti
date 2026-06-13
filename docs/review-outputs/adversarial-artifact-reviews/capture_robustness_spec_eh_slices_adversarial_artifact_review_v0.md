# Capture Robustness Spec E-H Slices Adversarial Artifact Review v0

```yaml
review_summary:
  report_path: docs/review-outputs/adversarial-artifact-reviews/capture_robustness_spec_eh_slices_adversarial_artifact_review_v0.md
  review_type: delegated_adversarial_artifact_review
  access_mode: no_repo_advisory
  authored_by: claude-opus-4.8
  reviewed_by: gpt-5
  de_correlation_bar: cross_vendor_discovery
  target: docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md
  target_slices: [E, F, G, H]
  source_context: SOURCE_CONTEXT_READY
  verdict: NEEDS_PATCH_BEFORE_BUILD_SCOPING
  findings:
    critical: 0
    major: 4
    minor: 1
  patch_queue_entry_emitted: false
  optional_diff_emitted: false
  review_use_boundary: findings_are_decision_input_only
```

## Scope and Method

Commission-bound target: `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md`, slices E-H only. I read the whole spec for context and treated all off-scope material as read-only evidence.

Access mode: advisory/no-repo for the reviewed target. This report does not patch the target spec and does not emit an executor-ready `patch_queue_entry`.

Preflight:

- Pinned worktree checked: `C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\capture-fallback-ladder-spec`.
- Branch observed: `capture-historical-fallback-ladder-spec`.
- HEAD observed: `8f3e036`; commission named `fb23e67` but explicitly allowed squash rewrite when target content is identical/reviewed by content.
- Dirty state observed clean from `git status --short --branch`.

Procedural status:

- `workflow-deep-thinking`: applied before findings to frame failure modes.
- `workflow-adversarial-artifact-review`: applied after source context.
- Orca overlay authorities read: `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/decision-routing.md`.

Source-read ledger:

| Source | Use |
| --- | --- |
| `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md` | Review target and E-H wording |
| `orca-harness/source_capture/adapters/archive_org.py` | Code behavior E-H reason about |
| `orca-harness/runners/run_source_capture_archive_packet.py` | Current archive packet behavior around preserved bodies |
| `docs/product/source_capture_toolbox/capture_recon_index_v0.md` | Capture doctrine seed: blocked/PARTIAL/runner ladder evidence |
| `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` | Capture route, receipt, GO/PARTIAL/NO-GO criteria |
| `docs/decisions/orca_mini_god_tier_doctrine_v0.md` | MGT limitation and standing-infrastructure lens |
| `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md` | H token/profile boundary |
| `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md` | H source-quality finalization boundary |
| `docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md` | Fixture-admission boundary cited by H |

## Verdict

`NEEDS_PATCH_BEFORE_BUILD_SCOPING`.

The E-H additions are directionally right: they identify real robustness holes and mostly preserve the intended no-standing-infrastructure / no-gate-defeat posture. They are not yet robust enough to hand to implementation scoping because the composition points carry material ambiguity: the E-G retry loop lacks a finite cursor and receipt contract; archive.today no-lookahead proof is asserted beyond the observed Wayback evidence; E's owner-deferrable archive.today rung can collapse the promised cross-archive value; and H currently risks turning a negative capture-side floor into automated positive source-quality finalization.

No `NEEDS_ARCHITECTURE_PASS` is required from this review. The failures appear patchable inside slices E-H by tightening contracts, limits, and non-claims.

## Findings

### AR-01 - Major - E/G Re-pick Loop Has No Finite Cursor or Receipt Contract

**Phase:** correctness

**Target slice(s):** E, F, G

**Evidence:**

- E says each archive rung selects the latest pre-cutoff memento, hands it to F, and stops at the first retrieved pre-cutoff body (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:104`).
- G says a post-cutoff served date should signal E to re-select the next-older pre-cutoff snapshot and reach NO-GO only when no pre-cutoff snapshot yields a clean body (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:122`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:124`).
- F's stop condition is "first usable body" or ladder exhaustion, with usability dependent on G (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:114`).
- The playbook requires receipts to log routes tried, skipped-with-reason, why the run stopped, and the verdict (`docs/product/source_capture_toolbox/source_capture_playbook_v0.md:99`, `docs/product/source_capture_toolbox/source_capture_playbook_v0.md:205`).

**Why the strongest defense fails:** The archive list and URL-form variants are bounded, but the temporal candidate sequence inside an archive is not specified as a bounded cursor. A Wayback latest-pre-cutoff candidate can redirect to a post-cutoff body; G then asks E to re-pick, but E does not define candidate ordering, max attempts, duplicate detection, rejected-candidate recording, or when the archive rung is exhausted. Without that, an implementation can loop, starve later archives, or silently skip candidates without an audit trail.

**Impact:** The no-lookahead fix can become non-executable or non-auditable exactly where it matters: repeated redirect-to-nearest behavior near cutoff. This also weakens the honest NO-GO/PARTIAL posture because the receipt cannot prove that "no pre-cutoff snapshot yields a clean body" was actually exhausted.

**Minimum closure condition:** E/G must define a finite, receipt-visible candidate cursor for each archive/form/rung combination, including rejected snapshot IDs, rejection reason, served timestamp when available, duplicate handling, max attempts or complete bounded list semantics, and the exact archive-exhaustion condition before moving to the next archive or returning NO-GO/PARTIAL.

**Next authorized action:** Advisory patch direction only: patch slices E and G to make the E-G retry contract finite and auditable before build scoping.

### AR-02 - Major - Archive.today Served-Time Integrity Is Asserted Without an Archive-Specific Proof Contract

**Phase:** correctness

**Target slice(s):** E, G

**Evidence:**

- E includes archive.today as the general second locate rung, with reachability and anti-bot caveats (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:101`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:104`).
- G states that Memento archives "Wayback, archive.today" carry served date in `Memento-Datetime`, and points to the observed evidence below (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:122`).
- The observed evidence is a live Wayback probe: a Wayback request redirected and the Wayback 200 carried `memento-datetime` / `x-archive-orig-date` (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:125`).
- The playbook requires source-native, independently checkable evidence for GO, and rejects asserted-but-unverifiable capture (`docs/product/source_capture_toolbox/source_capture_playbook_v0.md:95`, `docs/product/source_capture_toolbox/source_capture_playbook_v0.md:195`).

**Why the strongest defense fails:** It is reasonable to expect Memento-style archives to expose datetime metadata, but the target's only concrete observation is Wayback. The slice does not state what happens when archive.today omits, transforms, localizes, blocks, or makes inaccessible the served-date header/body evidence. The line "Memento archives (Wayback, archive.today) carry..." overstates the evidence currently cited by the spec.

**Impact:** A post-cutoff archive.today body, wrong revision body, or unverifiable body can either pass by assumption or fail inconsistently by implementation choice. That is a direct no-lookahead risk because G is supposed to be the body-level cutoff guard for every E-located archive, not only Wayback.

**Minimum closure condition:** G must define an archive-specific served-time proof contract for every locate rung: trusted metadata sources, parser expectations, missing/unparseable metadata behavior, and whether the rung is deferred when served-time proof is unavailable. For archive.today specifically, either bind observed evidence/source support or mark the rung as requiring a pre-build assumption gate. Publisher-history must similarly bind revision timestamp/identity proof rather than relying on opaque revision ID alone.

**Next authorized action:** Advisory patch direction only: patch G and the archive.today parts of E to make missing or untrusted served-time proof a visible verification failure or an explicit deferral.

### AR-03 - Major - Archive.today Deferral Can Collapse E's Claimed Cross-Archive Value for Ordinary Brand Pages

**Phase:** correctness

**Target slice(s):** E

**Evidence:**

- E's goal is to remove the single-archive single-point-of-failure via a bounded cross-archive locate ladder (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:102`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:103`).
- The proposed general locate set is Wayback, archive.today, and publisher version-history; publisher version-history is conditional and N/A for most brand/retailer pages (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:104`).
- E makes archive.today owner-deferrable and says the ladder degrades gracefully to Wayback plus publisher-history without it (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:107`).
- The MGT doctrine requires visible limitations; silent capability drops void the label (`docs/decisions/orca_mini_god_tier_doctrine_v0.md:40`, `docs/decisions/orca_mini_god_tier_doctrine_v0.md:75`).

**Why the strongest defense fails:** "Wayback + publisher-history" is a graceful degradation only for sources that actually have publisher history, such as docs/wiki/GitHub surfaces. For the ordinary brand/retailer pages that motivated archive backtest robustness, deferring archive.today leaves Wayback as the only general archive. That does not remove the single-archive single-point-of-failure; it preserves it while the slice still advertises the broader E goal.

**Impact:** Build scoping can unknowingly accept a v1 that claims cross-archive robustness while providing it only for conditional doc/wiki surfaces. This is an MGT honesty failure: the foregone limitation is not named at the point where the owner-deferrable cut is introduced.

**Minimum closure condition:** E must either make a second general archive rung required for v1, or split the v1 variants explicitly: "Wayback + publisher-history only" must be labeled as not removing the single-archive SPOF for ordinary brand/retailer pages, with acceptance criteria and MGT limitation text downgraded accordingly.

**Next authorized action:** Advisory patch direction only: owner/CA adjudicates whether archive.today is mandatory for v1 or the E goal/acceptance is narrowed.

### AR-04 - Major - H Turns a Negative Floor Into Possible Automated Positive Source-Quality Finalization

**Phase:** correctness

**Target slice(s):** H

**Evidence:**

- H proposes computing the source-quality token from E/F/G evidence and enforcing a mechanical floor, including decision-grade tokens such as `mini_god_tier_met` / `recommended` (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:130`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:131`).
- H acceptance says a clean GO packet is eligible for decision-grade, subject to downstream fixture/Judgment decisions (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:133`).
- The profile says result tokens are operating tokens, not review verdicts, validation states, or Judgment claims (`docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md:65`, `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md:67`).
- The state assembler explicitly forbids source-quality scoring and automated finalization of `mini_god_tier_met` (`docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md:65`, `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md:67`, `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md:124`, `docs/product/source_capture_toolbox/source_quality_state_assembler_v0.md:125`).
- The fixture-admission criteria distinguish source-quality posture from fixture admissibility and admit no packet (`docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md:6`, `docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md:10`, `docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md:26`).

**Why the strongest defense fails:** H says the downstream "good enough for this decision" call remains actor-carried, which is the right boundary. But the proposed capture-time computation still reaches for the same positive tokens and lifecycle states that existing profile/assembler documents keep operator-finalized. A deterministic negative cap is safe; deterministic positive finalization of `mini_god_tier_met` or `recommended` is not.

**Impact:** A packet emitter can become an unauthorized source-quality scorer. That would blur Source Capture, fixture admission, and Judgment ownership even if the slice says "no fixture admission" in non-goals.

**Minimum closure condition:** H must limit capture-time automation to evidence emission, limitation propagation, and negative/sub-floor caps. Any positive `mini_god_tier_met`, `recommended_fixture_admission`, `separately_admitted`, or decision-grade finalization must remain operator/separate-decision finalized, with an explicit `operator_review_required` or equivalent field.

**Next authorized action:** Advisory patch direction only: patch H to separate mechanical floor/cap from positive token finalization.

### AR-05 - Minor - Probe-Then-Pin Re-probe Trigger Does Not Name Verification Degradation as Pin Failure

**Phase:** correctness

**Target slice(s):** F, G, H

**Evidence:**

- F says steady-state fetches directly at the pinned rung and re-probes on failure (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:113`).
- F's stop condition says first usable body means 2xx, non-empty, and passing G verification (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:114`).
- G/H add verification and quality-floor gates downstream of raw body retrieval (`docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:121`, `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md:130`).

**Why the strongest defense mostly holds:** The "passes slice-G verification" phrase covers much of this if implementers read it strictly. The remaining risk is that "pinned rung fails" can be implemented narrowly as transport failure only, while a stale pin can still return HTTP 200, non-empty, wrong body, placeholder body, or newly sub-floor body.

**Impact:** A pinned rung can silently degrade without triggering re-probe, weakening the cheap-working-rung reuse pattern.

**Minimum closure condition:** F must define pin failure as any non-usable result, including G verification failure, served-time/identity/content-integrity failure, and H sub-floor status when H is available. Receipts should record `pin_reused`, `pin_reprobe_reason`, and `pin_replaced_by` when a re-probe occurs.

**Next authorized action:** Advisory patch direction only: tighten F's failure/re-probe wording; no architecture pass required.

## Advisory Remediation Direction

Patch only slices E-H:

- In E, split locate-ladder acceptance by v1 shape: with archive.today as required general cross-archive rung versus Wayback+publisher-history-only as a narrower, visibly limited variant.
- In E/G, add the finite candidate cursor: archive, URL variant, selected timestamp/revision, served timestamp/revision proof, rejection reason, and archive-exhaustion condition.
- In G, make served-time proof archive-specific. Missing/untrusted served time for a Memento archive should be a verification failure or an explicit pre-build assumption gate, not an implementation choice.
- In F, define pin failure as non-usable body, not only transport failure.
- In H, enforce only negative floors and limitation propagation at capture emit time; preserve positive source-quality/lifecycle finalization as operator/separate-decision work.

No unified diff is emitted because the commission is advisory/no-repo for the reviewed target and the safest next step is CA adjudication of the findings before patching E-H.

## Residual Risk

This review did not re-run live archive probes or verify current archive.today/Memento behavior on the network. The findings are source-backed against repo-visible artifacts and the spec's own cited evidence. Any later patch should still run a bounded implementation-scoping source check for the current archive APIs before treating the served-time proof contract as build-ready.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, mandatory remediation, fixture admission, implementation authorization, or executor-ready patch authority. A separate Orca owner/CA adjudication or authorized patch lane must accept and apply any remediation.

DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the delegated-review-patch return contract.

- Original commission: delegated adversarial artifact review-and-patch, Capture-Robustness Spec slices E-H.
- Reviewed artifact and bounded scope: `docs/product/source_capture_toolbox/archive_org_refinement_and_source_family_gap_spec_v0.md`, slices E-H only.
- Findings: AR-01 major E/G finite retry cursor missing; AR-02 major archive.today served-time proof unbound; AR-03 major archive.today deferral collapses ordinary-page cross-archive value; AR-04 major H risks automated positive source-quality finalization; AR-05 minor pin failure should include verification degradation.
- Proposed artifact patch: none emitted; advisory remediation direction only.
- Reviewer verdict: `NEEDS_PATCH_BEFORE_BUILD_SCOPING`.
- Residual risk: no live archive probes rerun; source-backed repo review only.
- Blockers/off-scope/not-proven: no strict validation, readiness, approval, fixture admission, implementation authorization, or patch authority claimed.

## Same-Vendor Post-Patch Recheck (CA-adjudicated, 2026-06-14)

```yaml
recheck:
  de_correlation_bar: same_vendor_sanity
  same_vendor_rationale: bounded post-patch recheck; no no-new-seam claim
  reviewed_by: claude-sonnet-4-6
  authored_by: claude-opus-4.8
  overall: clean
  per_finding:
    AR-01: closed
    AR-02: closed
    AR-03: closed   # name/label branch; full closure was the owner decision, now made
    AR-04: closed
    AR-05: closed
  new_issues: []
  residual: acceptance criterion (a) assumed archive.today present; resolved by the AR-03 (b+) owner decision + acceptance alignment in the same commit
ca_adjudication:
  verdict: recheck accepted; AR-01..05 patches kept/final (two-bar gate cleared)
  ar03_owner_decision: >
    (b+) — v1 Wayback + publisher-history (labeled: SPOF not removed for ordinary brand/retailer
    pages); archive.today committed fast-follow gated on its AR-02 served-time + no-gate-defeat
    probe; Common Crawl per-URL CDX backup second general rung.
```
