# Source Capture Packet Fixture Admission Criteria v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Proposed owner-gated criteria a Source Capture Packet must satisfy to cross scratch -> separately_admitted, with a current four-unit evaluation. Admits no packet.
use_when:
  - Deciding what a separate Source Capture Packet fixture-admission decision must assert.
  - Checking whether an already-closed source unit is admissible, borderline, or not-yet under the accepted lifecycle decision.
  - Distinguishing source-quality posture (for example mini_god_tier_met) from fixture admissibility.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
  - docs/product/source_capture_toolbox/README.md
  - docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
stale_if:
  - The accepted lifecycle/retention/sensitivity decision is amended or superseded.
  - The Mini God-Tier profile changes lifecycle vocabulary or result tokens.
  - An owner acceptance decision adopts, amends, or rejects these criteria; this proposal is then superseded by that decision.
```

## Status

Status: `PROPOSED_SOURCE_CAPTURE_PACKET_FIXTURE_ADMISSION_CRITERIA_V0`.

This is an owner-gated proposal. It defines what a separate Source Capture Packet
fixture-admission decision would have to assert, and evaluates the four
already-closed source units against those criteria. It admits no packet, accepts
no criteria as binding, and creates no new lifecycle authority. Adoption is an
owner decision (see Owner Acceptance Gate).

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom - Source Capture fixture-admission criteria proposal
  edit_permission: docs-write
  target_scope:
    - docs/product/source_capture_toolbox/source_capture_packet_fixture_admission_criteria_v0.md
  dirty_state_checked: yes - broad unrelated dirty state; lifecycle decision and Armory README carry display-name-only (Toolbox->Armory) working-tree drift; this proposal isolates the admission-criteria gap and makes no admission, validation, readiness, rights, or downstream-consumption claim
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
    - docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
```

## Purpose And Boundary

The accepted lifecycle decision keeps generated Source Capture Packets `scratch`
by default and names four lifecycle states (`scratch`, `candidate_evidence`,
`recommended_fixture_admission`, `separately_admitted`), but it does not
enumerate the conditions a packet must satisfy to be admitted. The Source Capture
Armory README records the matching gap: "no named packet has been separately
admitted as a fixture." This proposal closes the criteria gap only.

What this is:

- a proposed checklist of what a packet must be able to assert to be admissible;
- a current evaluation of the four already-closed source units against that
  checklist.

What this is not:

- not an admission of any packet; the lifecycle decision reserves admission for a
  separate owner authorization;
- not an accepted or binding standard; status is `PROPOSED_*` and adoption is
  owner-gated;
- not the Judgment Spine fixture-admission gate (`JSG-*`); that is a separate lane
  and is out of scope here;
- not rights clearance, legal sufficiency, privacy review, retention-duration
  policy, source completeness, validation, readiness, or downstream-consumption
  design.

## Source Basis

- `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
  - Accepted lifecycle/retention/sensitivity decision; controlling source for the
    criteria below. Working-tree note: this file currently carries a
    display-name-only Toolbox->Armory edit over committed HEAD `aa17aed`; the
    lifecycle rule itself is unchanged.
- `docs/product/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md`
  - Owner of source-quality result-token and lifecycle vocabulary.
- `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`
  and the `CW-P4`, `CW-P6`, `CW-P1` end-to-end pass closeouts in the same folder
  - The four already-closed source units evaluated below.
- `docs/product/source_capture_toolbox/README.md`
  - Source Capture Armory index naming the admission gap.

## Admissibility Criteria

A packet is admissible only when an admission decision can assert all of the
following from packet-side evidence, not from source-quality posture. Each is a
pass condition; any unmet item caps the packet at `borderline` or `not-yet`.

Carried directly from the lifecycle decision Retention Rule:

- AC-1 Packet path and packet or manifest hash are recorded.
- AC-2 Lifecycle state is stated and is being moved deliberately, not assumed.
- AC-3 Reason for retention or admission is stated.
- AC-4 Source-access basis and capture mode are recorded.
- AC-5 The note states whether raw HTML, text, screenshots, images, media,
  archive bodies, account-visible, entitled, client-provided,
  consenting-coworker, or machine-specific provenance material is included.
- AC-6 A sensitivity and sharing note is present (Sensitivity Rule).
- AC-7 Allowed downstream use is stated.
- AC-8 Forbidden claims and non-claims are stated.
- AC-9 The note states whether a later fixture-admission decision is still
  required; for `separately_admitted`, it cites the separate admission decision.

Two preconditions implied by the decision but stated here as explicit admission
gates:

- AC-10 Named downstream use: the admission names the concrete downstream consumer
  or use it is admitted for. Admission without a named consumer is refused; this
  prevents admitting a fixture into a vacuum.
- AC-11 Raw-body retrievability: the packet scratch directory is still present, or
  a retained copy is made as part of admission. A packet whose raw body can no
  longer be reinspected is not admissible on closeout-recorded hashes alone,
  because the lifecycle decision permits scratch `_test_runs/` cleanup.

## Hard Guardrails

- G-1 Token is not admissibility. `mini_god_tier_met`,
  `mini_god_tier_with_visible_limitations`, exit code `0`, a preserved body, or a
  screenshot does not itself clear admission. This restates the lifecycle decision
  Citation Rule; source-quality tokens describe posture only.
- G-2 Contamination stop. If the packet contains credentials, cookies, raw
  browser-profile material, Playwright storage-state JSON, session sidecars,
  authorization headers, or secrets, stop and treat the packet as contaminated
  scratch; it is not admissible until a separate owner decision says how to
  dispose, redact, or isolate it.
- G-3 No rights clearance here. Meeting AC-5 and AC-6 records sensitivity
  handling; it does not clear legal rights, privacy, or publication permission.
  Those remain separate owner decisions.
- G-4 Proposal only. These criteria are not binding until owner-accepted; do not
  cite this file as the authority that admitted a packet.

## Four-Unit Evaluation

Current standing of the four already-closed source units against the criteria.
All four remain `scratch`; none is admitted.

| Source unit | Source-quality token (posture only) | Admissibility | Single gating reason |
| --- | --- | --- | --- |
| `CW-P4` | `mini_god_tier_met` | borderline | Cleanest body posture and smallest sensitivity surface, but no named downstream use (AC-10) and scratch-dir retrievability unconfirmed (AC-11); token does not imply admission (G-1). |
| `CW-P6` | `mini_god_tier_with_visible_limitations` | not-yet | Preserved body but visible archive/media/source-envelope limitations; no named downstream use (AC-10); AC-11 unconfirmed. |
| `CW-P1` | `archive_body_not_preserved` | not-yet | No eligible archive body was preserved, so there is no source body to admit (fails the substance behind AC-5/AC-11), independent of any consumer. |
| `Slot 3` (B1/B2/WSO) | `mini_god_tier_with_visible_limitations` (x3) | not-yet | Raw third-party/user-authored content raises the AC-6 sensitivity bar; no named downstream use (AC-10); scratch `_test_runs/` retrievability must be confirmed or a retained copy made (AC-11). |

No unit is admissible today: every one is blocked at least by the absence of a
named downstream use (AC-10). That is the same signal the planning step surfaced;
admission cannot complete until a downstream consumer exists.

## Owner Acceptance Gate

Adopting these criteria as the binding admission standard is a `lifecycle_boundary`
doctrine change. If the owner accepts, that acceptance must be recorded as a
separate `docs/decisions/` decision carrying a `direction_change_propagation`
receipt at that point; this proposal does not carry one because it asserts no
binding rule. The owner may instead amend, narrow, or reject these criteria, or
request an adversarial artifact review before acceptance.

## Open Question

Is there a named downstream consumer (Cleaning/ECR intake, a participant-packet
path, or another use) that any Source Capture Packet would be admitted for? Until
one is named, AC-10 blocks every unit, and the higher-leverage move may be to
decide whether Source Capture output will be consumed at all rather than to admit
a packet into a vacuum.

## Non-Claims

This proposal is not fixture admission for any packet, not an accepted standard,
not validation, readiness, rights clearance, legal sufficiency, privacy review,
retention-duration policy, source completeness, source-quality scoring, the
Judgment Spine fixture-admission gate, ECR/Cleaning/Judgment design, buyer proof,
commercial-readiness evidence, or source-of-truth promotion.
