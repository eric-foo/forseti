# Aphrodite Depth-Capture ToS-Risk Sanity Check v0

```yaml
retrieval_header_version: 1
artifact_role: Gate check (sanity check — not legal clearance, not capture authorization)
scope: >
  Discharges the Aphrodite carveout charter's pre-build gate 2 (Section 7): does
  the planned depth capture — stratified transcripts plus page-1 visible
  comments across a niche fragrance creator roster — sit inside the owner's
  already-accepted source-access boundary and measured-risk posture, or does it
  cross into the rejected industrial-scraping tier or need a new capture-lane
  decision? Reads the controlling capture-lane sources; defers all
  capture-boundary authority to them and creates none.
use_when:
  - Checking whether Aphrodite depth capture may proceed at foundation stage without a new boundary decision.
  - Scoping the depth-layer build's capture assumptions.
  - Distinguishing the foundation-stage capture question from the Phase-1 commercial-use question.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
  - docs/decisions/wind_caller_calibration_carveout_v0.md
  - forseti/product/spines/creator_signal/aphrodite_carveout_charter_v0.md
stale_if:
  - The source-access boundary decision or measured-risk posture is amended.
  - The carve-out's bounded-session / account-cap posture changes.
  - The planned capture shape materially changes (e.g. moves to industrial-scale scraping or a standing crawler).
```

## Status

`SANITY_CHECK_PASS (foundation-stage capture), WITH TWO CARRIED FLAGS.` Authored
2026-07-04 to discharge charter pre-build gate 2. This is a **sanity check
against already-accepted capture-lane doctrine, not legal clearance and not a
capture authorization.** It creates no source-access authority; the capture
lane's own accepted decisions govern.

## What was checked

Whether the depth-now capture plan (charter Section 6) — cheap metadata on all
videos, deep transcript + page-1 visible comment capture on a stratified
~20–30% slice, across a niche fragrance roster (~500–2,000 creators) — stays
inside the owner's accepted source-access boundary and measured-risk posture.

## Controlling sources read (authority deferred to these; none amended here)

- `data_capture_source_access_method_plan_v0.md` and its controlling standard
  `LOOSEN_SOURCE_ACCESS_TO_DISCOVERABLE_OR_ENTITLED_DISCLOSABLE`.
- `forseti_creator_monitoring_policy_architecture_v0.md` (bounded-budget allocator;
  carve-out conformance).
- `wind_caller_calibration_carveout_v0.md` (bounded-session / account-cap
  posture).

## Findings

1. **In-bounds by content type.** Video transcripts and public comments are
   discoverable/public material, visible through free/account-created access.
   That places them squarely inside the accepted boundary standard
   (discoverable-or-entitled + disclosable). This is not a boundary question.

2. **In-bounds by volume and posture.** Stratified capture (cheap metadata on
   all; deep on a minority slice; page-1 comments only) is bounded and far
   below the one thing the owner's posture explicitly **rejects** — absurd-level
   "Bright-Data-style industrial scraping." The monitoring policy's
   bounded-budget, account-cap (≤10 operating accounts, start ≤5), and
   **no-standing-crawler** rule (human-initiated or pre-authorized, bounded,
   self-terminating sessions) governs and must hold; the depth plan conforms to
   it by design (capture-on-signal, not a 24/7 daemon).

3. **Substrate is already accepted and partly built — this is not a new ask.**
   A YouTube transcript extraction runner already landed
   ([PR #640](https://github.com/eric-foo/orca/pull/640)); the first tranche of
   source-access tooling is authorized. Transcript capture is therefore an
   existing accepted capability, not a new source-access route requiring a
   fresh boundary decision.

4. **The real gate is downstream: commercial use + data rights (FLAG 1).**
   The source-access plan explicitly flags that anti-blocking/automated capture
   carries ToS/reputational/litigation risk (owner-accepted as a disclosable
   posture) and that **"real legal counsel is advisable before commercializing"**
   and **"data-rights sufficiency"** is an open non-claim. Selling vetting
   reports built partly on captured transcripts/comments crosses from *capture*
   into *commercialize*. That question lands at **Phase 1** (when the Vetting
   Sprint actually sells), not Phase 0 (foundation capture), and it is an
   **owner + legal-counsel decision, not an agent one.**

5. **Derived output binds to the provenance contract (FLAG 2), and materiality
   applies.** Any claim derived from this captured content must carry derivation
   provenance per `aphrodite_derived_claim_provenance_contract_v0.md`. The
   source-access plan's materiality gate also applies: a capture used as
   evidence-grade in a sold report must be reacquired/verified through a clean
   disclosable path before final evidence use.

## Verdict

**PASS for foundation-stage depth capture.** The plan sits inside the accepted
source-access boundary and measured-risk posture; it is not the rejected
industrial-scraping tier; the transcript substrate is already accepted/built.
**No new capture-boundary decision is required to continue foundation-stage
depth capture**, provided it conforms to the carve-out's bounded-session /
account-cap / no-standing-crawler posture.

Two flags travel forward, both landing later than foundation:
- **FLAG 1 (Phase-1, owner + legal):** commercial use + data rights for selling
  reports built on captured content. Distinct from the capture question;
  resolve before the first paid sprint sells, not before capture runs.
- **FLAG 2 (build-time):** all derived output binds to the derived-claim
  provenance contract; the materiality-reacquisition rule applies to any claim
  that becomes evidence-grade in a sold report.

## Non-claims

- Not legal clearance and not legal counsel — a sanity check against accepted
  internal doctrine only. Real legal counsel remains advisable before
  commercializing (source-access plan's own standing flag).
- Not a capture authorization, a source-access route authorization, or a
  boundary amendment.
- Not commercial-use or data-rights clearance (FLAG 1 is explicitly deferred).
- Not validation or readiness.
```
