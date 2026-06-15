---
retrieval_header_version: 1
artifact_role: Lane working log (authorizations + issue log + phase progress) for Judgment-Spine repeatability case #2 (Topicals). NOT validation/readiness/judgment-quality evidence.
scope: >
  Running log for the Topicals (batch-1 case #4) judgment-spine repeatability lane:
  owner authorizations, standing blindness rules, a problem/issue log to deal with
  in future, and phase progress. Lives on branch jsg-case2-topicals-v0.
use_when:
  - Resuming or auditing the Topicals case-#2 lane.
  - Checking what the owner authorized and what problems are logged-but-deferred.
authority_boundary: retrieval_only
---

# Topicals — Judgment-Spine Case #2 Lane Log (v0)

Case: batch-1 **#4** Topicals — DTC → nationwide Sephora expansion at ~month 9
(2020–21). Lane goal: prove the judgment-spine **method repeats past N=1** (Beauty
Pie = the frozen N=1). One frozen case proves *method*, not *judgment quality*.

## Standing Rules (this lane)

- **OUTCOME-BLIND, permanently.** The main lane agent and the owner NEVER read
  `docs/research/topicals_sephora_expansion_sealed_outcome_facilitator_only_v0.md`
  or any `*sealed_outcome*` file. Only the delegated outcome-aware subagent (gate-0
  + the eventual firewalled freeze) may touch it.
- **Capture routes through the Source-Capture Armory Runner Ladder** (armory runners
  + archive_org adapter), never ad-hoc fetches that enter evidence. Gate-0 by-hand
  archive reads were exempt scouting and bind nothing.
- **Log every problem we face** (owner directive 2026-06-14) — record in the Issue
  Log below, deal with later; do not silently drop or block on it.

## Authorizations (owner, in-thread)

- **2026-06-14** — Case #2 = **Topicals** (batch-1 case #4). Owner selected.
- **2026-06-14** — Org-motion treatment = **Option A**: run the paired with/without on
  the single cutoff-proximate org-motion point, labeled honestly as a *single point*
  (not a trajectory); record the blind org-motion prediction before reveal. Owner
  accepts org-motion "will probably be dismissed" — that is a valid reportable result.
- **2026-06-14** — **Phase-4 capture authorized** (org-motion unit via the armory
  `archive_org` adapter → SourceCapturePacket → ECR).

## Issue Log (log-now, deal-with-later)

- **ISSUE-01 — Org-motion is THIN (single point, not a trajectory).** Archive-backtestable
  only via the brand's own careers page: 1 snapshot ≤cutoff (2021-03-03), 1 role
  (Supply Chain Manager), no 2020 baseline; no third-party ATS board; no pre-cutoff
  LinkedIn. Owner-accepted (Option A). Future handling: record the blind org-motion
  prediction and report whether it moved the call; **never inflate the single point
  into a trajectory**.
- **ISSUE-02 — Feasibility doc blind-safety. RESOLVED 2026-06-14.** An independent outcome-aware
  reviewer (separate subagent) checked the feasibility doc + the captured packet against the
  sealed answer key: **PASS, no leak** (returned no outcome content; main agent stays blind).
  The main agent still has not read the feasibility doc directly; it is now cleared for the
  blind constructor to consume. (This was the input blind-safety check; the R6 *pre-freeze*
  review of the constructed packet is separate and still pending.)
- **ISSUE-03 — FacilitatorLedger schema drift (L4) expected.** The frozen Topicals
  fixture will be freeze-valid but NOT `model_valid` (same construction-vs-runtime drift
  as Beauty Pie). Deferred debt; do NOT do the schema fix while blind; shape-only when
  the batch runs model-validation gates.
- **ISSUE-04 — Non-ATS capture path. RESOLVED 2026-06-14.** Org-motion target was the brand's
  own Shopify careers page (not a Greenhouse/Lever board); `archive_org` captured the
  2021-03-03 Wayback snapshot cleanly (exit 0, status 200, 129KB real body, signal present).
- **ISSUE-05 — Stale charter reference.** The batch-1 charter's case-#3 amendment cites
  `docs/product/source_capture_toolbox/capture_investigation_playbook_v0.md`, which does not
  exist; the actual file is `source_capture_playbook_v0.md`. Provenance/cosmetic only — log for
  a future charter-reference cleanup; does not block capture.
- **ISSUE-06 — Case-slug spoiler leak (caught by R6). FIXED 2026-06-14.** The blind constructor
  inherited the case-dir slug into the participant packets' `case_id` front-matter, naming the
  specific retail account (the spoiler) on a participant-readable surface. Root cause: the case-dir
  name embedded the retailer. Fix: renamed the case dir to a generic decision-type slug
  (`topicals_retail_expansion_2021_v0`, matching the Beauty Pie `…_repricing_…` pattern), set both
  packets' `case_id` generic, made the facilitator-side provenance slug consistent; grep-verified the
  retailer name + old slug are absent from every case surface. **Reusable lesson:** case-dir/slug
  naming must follow the decision TYPE, never the specific spoiler (R5: spoilers live only in the
  sealed record) — candidate for a distill cell.
- **ISSUE-07 — L2 span C11 NBSP mismatch. FIXED 2026-06-14.** C11's quoted span used an ASCII space
  where the captured body has U+00A0 (non-breaking space), so it was not a true verbatim substring.
  Fixed by trimming the span to `2-4 years experience in Supply Chain Management or relevant role`
  (grep-verified verbatim in the body). 12/13 spans were already exact.
- **ISSUE-08 — Captured-evidence storage location (fixture-admission decision).** The augmented packet +
  provenance reference the org-motion capture at
  `orca-harness/reports/source_capture/topicals_case2_careers_archive/` (armory scratch), whereas the
  frozen Beauty Pie fixture keeps captured evidence inside the case dir (`source_captures/`). The
  evidence is hash-pinned in the ledger + provenance (body sha256 `db147fc0…`) regardless of location,
  so the freeze is valid. For a durable, self-contained, committable fixture, OWNER to decide: (a)
  commit the capture packet in place; (b) relocate into the case dir `source_captures/` and re-freeze
  (changes packet/ledger hashes); or (c) leave as scratch (evidence stays hash-pinned only). Does not
  affect the repeatability proof.
- **ISSUE-08 RESOLVED 2026-06-14 → relocated to case dir + re-froze.** `reports/source_capture/` is
  gitignored scratch (`.gitignore:34`), so commit-in-place was doctrinally impossible. Per the folder
  doctrine + the frozen Beauty Pie layout, fixture evidence belongs in the case dir; moved to
  `source_captures/e6_careers_20210303/` (committable) and **re-froze** → new `ledger_freeze_hash
  e25319b3…` (was `d184cdd0…`), independently re-verified FREEZE_VALID; captured body unchanged
  (`db147fc0…`).
- **FUTURE — capture directly into the case dir.** Point the armory `--output` inside the case
  `source_captures/` from the start, so a frozen fixture is self-contained without a later
  relocate+re-freeze. (Reusable lesson; distill candidate.)
- **FUTURE (Q2) — memory-resistance ≠ search-resistance (owner direction 2026-06-14).** Search-
  resistance is already covered by the web-off execution rule; the live risk is the contestant model's
  TRAINING-MEMORY recognition. For future cases adopt **partial anonymization + red herrings** (decoy
  specifics that lead memory astray) — judged high-value at ~no cost; full anonymization not required;
  keep the same R5 decision frame. Belongs in the conductor R5 / case-frame-template construction
  protocol (a routed-out owner change); logged here for propagation. Guardrail: red herrings must not
  alter any decision-relevant fact.

## Phase Progress

- **Gate-0 feasibility — DONE.** PASS (thin). Cutoff ≤ 2021-03-15. Artifacts:
  `docs/research/orgmotion_topicals_capture_feasibility_v0.md` (blind-safe) +
  `docs/research/topicals_sephora_expansion_sealed_outcome_facilitator_only_v0.md`
  (facilitator-only sealed; never opened by main agent).
- **Phase-4 capture (org-motion unit) — DONE & verified (2026-06-14).** Archive.org runner
  captured the single ≤cutoff careers snapshot **20210303084505** (status 200, text/html) into
  a Source Capture Packet. Body preserved 129094 bytes, sha256
  `db147fc02195e872957d588be376a935aee0fda584960dbd10d063912a0d981b`; grep-confirmed the body
  carries the **Supply Chain Manager** listing (reports to CEO/CPO; inventory/vendor/shipment/
  supply-chain build-out). Packet ID `01KV2M7XPZENAJJ74H1QVWCW6E` at
  `orca-harness/reports/source_capture/topicals_case2_careers_archive/` — discovery-grade,
  uncommitted, NOT fixture admission. `snapshot_count=1` reflects collapse=digest unique rows.
- **Phases 3/5 (blind baseline + augmented packet build, R5 decision-framing) — DONE (2026-06-14).**
  Blind constructor built `participant_packet_baseline.md`, `participant_packet_augmented.md`,
  `source_provenance_notes_v0.md` in case dir
  `orca-harness/cases/product_learning/topicals_retail_expansion_2021_v0/` (renamed from a
  retailer-naming slug — ISSUE-06). Org-motion (E6 = the Supply Chain Manager listing) is the only
  baseline↔augmented delta; 13 L2 spans bound to the captured body.
- **R6 independent pre-freeze leakage review — DONE: PASS after remediation (2026-06-14).** Independent
  outcome-aware reviewer FAILED the first pass on two findings (ISSUE-06 slug leak; ISSUE-07 C11 span);
  it found no other leak in the three files. Both remediated and grep-verified. Gate cleared for freeze.
- **JSG-02 firewalled freeze — DONE & independently verified (2026-06-14).** `ledger_freeze_hash =
  e25319b34d134cc48d36f770096f1bfeb9686ab2d351231d574a911b2e8f579c`; `facilitator_ledger.yaml` sha256
  `da1e714141ad5b9b…` (10,555 bytes). Validated twice: the outcome-aware freeze subagent (positive
  control — reproduced Beauty Pie's stored hash first), and an independent blind-safe recompute by the
  main agent using the harness's own `harness_utils.canonical_yaml_hash` → FREEZE_VALID. `model_valid =
  no` — the expected L4 schema-drift debt (same family as the frozen Beauty Pie exemplar; ISSUE-03).
  Main agent + owner stayed blind (outcome lives only in the sealed `embedded_outcome` block).
- **Blind org-motion prediction — DONE (2026-06-14).** Pre-registered blind in
  `org_motion_blind_prediction_v0.md`: weak upward (toward a more aggressive distribution stance) if it
  moves the call at all; magnitude small / possibly nil (single thin point). Bound into the freeze.

## Milestone — Repeatability proof reached (2026-06-14)

A second freeze-valid fixture (`topicals_retail_expansion_2021_v0`) was built **outcome-blind**
(constructor + main agent + owner blind), with **no faked evidence** (L3-honest provenance, L2
body-verified spans), **org-motion as the only paired delta**, **R6-cleared**, and **independently
freeze-verified**. This demonstrates the judgment-spine method **REPRODUCES past N=1** (Beauty Pie =
N=1). Caps: freeze-valid, **not** `model_valid` (L4 debt); product-learning tier; this proves *method
repeatability*, **not** judgment quality — calibration needs N≥K + running contestants + reveal
(JSG-08).
